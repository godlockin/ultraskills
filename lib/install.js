// @ts-check
/**
 * install.js — resolve skill, download SKILL.md, write to .claude/skills/[id]/
 * Node 18+ native fetch + readline; zero external deps.
 */

import { writeFile, readFile, mkdir, access } from 'node:fs/promises';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { assertSafeSkillId, resolveWithin } from './path-safety.js';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';

// ── Helpers ──────────────────────────────────────────────────────────────────

/** @param {string} question @returns {Promise<string>} */
function prompt(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, ans => { rl.close(); resolve(ans.trim()); });
  });
}

/** @param {string} p @returns {Promise<boolean>} */
async function fileExists(p) {
  try { await access(p); return true; } catch { return false; }
}

// ── Core resolution logic ────────────────────────────────────────────────────

/**
 * Resolve query against skills list.
 * Step 1: exact id match → [skill]
 * Step 2: arena.category substring match → top-3 by score
 * Step 3: description substring match → top-5 by score
 * @param {string} query
 * @param {import('./cache.js').Skill[]} skills
 * @returns {import('./cache.js').Skill[]}
 */
export function resolveSkill(query, skills) {
  const q = query.toLowerCase();

  // Step 1: exact id
  const exact = skills.find(s => s.id.toLowerCase() === q);
  if (exact) return [exact];

  // Step 2: arena.category substring
  const catMatches = skills
    .filter(s => (s.arena?.category ?? '').toLowerCase().includes(q))
    .sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0))
    .slice(0, 3);
  if (catMatches.length) return catMatches;

  // Step 3: description substring
  const descMatches = skills
    .filter(s => (s.description ?? '').toLowerCase().includes(q))
    .sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0))
    .slice(0, 5);
  return descMatches;
}

// ── URL builder ───────────────────────────────────────────────────────────────

/**
 * Build raw GitHub URL for a skill's SKILL.md.
 * Strips leading `./`, URL-encodes each path segment, appends /SKILL.md.
 * @param {string} skillPath  e.g. "./community/剪口播"
 * @returns {string}
 */
export function buildRawUrl(skillPath) {
  const stripped = skillPath.replace(/^\.\//, '');
  const encoded = stripped.split('/').map(seg => encodeURIComponent(seg)).join('/');
  return `${BASE_RAW_URL}${encoded}/SKILL.md`;
}

// ── Download ──────────────────────────────────────────────────────────────────

/**
 * @param {import('./cache.js').Skill} skill
 * @returns {Promise<string>}
 */
export async function downloadSkill(skill) {
  if ((skill.path ?? '').startsWith('./external/')) {
    throw new Error(`"${skill.id}" is an external skill — available in v2.`);
  }

  const url = buildRawUrl(skill.path);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10_000);
  try {
    const res = await fetch(url, { signal: controller.signal });
    if (!res.ok) throw new Error(`Failed to download: HTTP ${res.status}`);
    return res.text();
  } finally {
    clearTimeout(timer);
  }
}

// ── Write skill to disk ───────────────────────────────────────────────────────

/**
 * @param {string} id
 * @param {string} content
 * @param {string} cwd
 * @param {{ yes?: boolean }} [opts]
 * @returns {Promise<{ installed?: boolean, skipped?: boolean, path?: string }>}
 */
export async function writeSkill(id, content, cwd, opts = {}) {
  const safeId = assertSafeSkillId(id);
  const skillsRoot = resolveWithin(cwd, '.claude', 'skills');
  const targetDir = resolveWithin(skillsRoot, safeId);
  const targetFile = resolveWithin(targetDir, 'SKILL.md');

  await mkdir(targetDir, { recursive: true });

  if (await fileExists(targetFile)) {
    if (opts.yes) {
      // overwrite silently
    } else if (!process.stdin.isTTY) {
      process.stderr.write(`Skipping ${id}: already installed (use --yes to overwrite)\n`);
      return { skipped: true };
    } else {
      const ans = await prompt(`"${id}" already installed. Overwrite? [y/N] `);
      if (!ans.toLowerCase().startsWith('y')) {
        return { skipped: true };
      }
    }
  }

  await writeFile(targetFile, content, 'utf8');
  return { installed: true, path: targetFile };
}

// ── Manifest ──────────────────────────────────────────────────────────────────

/**
 * @param {string} cwd
 * @param {{ id: string, path: string, arena?: { score?: number } }} skill
 */
export async function writeManifest(cwd, skill) {
  const manifestPath = join(cwd, '.claude', 'skills', '.ultraskills-manifest.json');

  /** @type {Record<string, unknown>} */
  let manifest = {};
  try {
    const raw = await readFile(manifestPath, 'utf8');
    manifest = JSON.parse(raw);
  } catch {
    // start fresh
  }

  manifest[skill.id] = {
    id: skill.id,
    installedAt: new Date().toISOString(),
    path: skill.path,
    score: skill.arena?.score,
  };

  await writeFile(manifestPath, JSON.stringify(manifest, null, 2), 'utf8');
}

// ── Main install command ──────────────────────────────────────────────────────

/**
 * @param {string} query
 * @param {import('./cache.js').SkillIndex} index
 * @param {string} cwd
 * @param {{ yes?: boolean }} [opts]
 */
export async function install(query, index, cwd, opts = {}) {
  const skills = index.skills ?? [];
  const matches = resolveSkill(query, skills);

  if (!matches.length) {
    console.error(`Skill "${query}" not found.`);
    // Show top-5 description matches as suggestions
    const suggestions = skills
      .filter(s => (s.description ?? '').toLowerCase().includes(query.toLowerCase().split(' ')[0]))
      .sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0))
      .slice(0, 5);
    if (suggestions.length) {
      console.error('\nDid you mean:');
      suggestions.forEach(s => console.error(`  ${s.id.padEnd(35)} ${(s.description ?? '').slice(0, 60)}`));
    }
    console.error(`\nTry: npx ultraskills search ${query}`);
    process.exit(1);
  }

  /** @type {import('./cache.js').Skill} */
  let skill;

  if (matches.length === 1) {
    skill = matches[0];
  } else if (opts.yes || !process.stdin.isTTY) {
    skill = matches[0]; // highest score
    console.log(`Multiple matches — auto-selecting: ${skill.id} (score: ${skill.arena?.score ?? '?'})`);
  } else {
    console.log(`Multiple matches for "${query}":`);
    matches.forEach((s, i) => {
      const winner = s.arena?.is_winner ? ' ★' : '';
      const score = s.arena?.score ?? '?';
      console.log(`  ${i + 1}. ${s.id} (score: ${score}${winner}) — ${(s.description ?? '').slice(0, 60)}`);
    });
    const ans = await prompt(`Pick [1-${matches.length}] (default 1): `);
    const idx = Math.max(0, Math.min(parseInt(ans || '1', 10) - 1, matches.length - 1));
    skill = matches[idx];
  }

  process.stdout.write(`Downloading ${skill.id}...\n`);
  const content = await downloadSkill(skill);

  const result = await writeSkill(skill.id, content, cwd, opts);

  if (result.skipped) {
    console.log(`Skipped ${skill.id}.`);
    return;
  }

  await writeManifest(cwd, skill);
  console.log(`✓ Installed ${skill.id}`);
  console.log(`  Path: ${result.path}`);
  console.log(`  Restart Claude Code or run /skills reload to activate.`);
}
