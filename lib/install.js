// @ts-check
/** Install and manage a single skill. */
import { writeFile, mkdir, access } from 'node:fs/promises';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { assertSafeSkillId, assertSafeWriteTarget, resolveWithin } from './path-safety.js';
import { readManifest, saveManifest } from './manifest.js';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';

/** @param {string} question @returns {Promise<string>} */
function prompt(question) { const rl = createInterface({ input: process.stdin, output: process.stdout }); return new Promise(resolve => rl.question(question, ans => { rl.close(); resolve(ans.trim()); })); }
/** @param {string} p @returns {Promise<boolean>} */
async function fileExists(p) { try { await access(p); return true; } catch { return false; } }

/** @param {string} query @param {import('./cache.js').Skill[]} skills @returns {import('./cache.js').Skill[]} */
export function resolveSkill(query, skills) {
  const q = query.toLowerCase();
  const exact = skills.find(s => s.id.toLowerCase() === q);
  if (exact) return [exact];
  const cat = skills.filter(s => (s.arena?.category ?? '').toLowerCase().includes(q)).sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0)).slice(0, 3);
  if (cat.length) return cat;
  return skills.filter(s => (s.description ?? '').toLowerCase().includes(q)).sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0)).slice(0, 5);
}

/** @param {string} skillPath @returns {string} */
export function buildRawUrl(skillPath) {
  const stripped = skillPath.replace(/^\.\//, '');
  const encoded = stripped.split('/').map(seg => encodeURIComponent(seg)).join('/');
  return `${BASE_RAW_URL}${encoded.endsWith('/SKILL.md') ? encoded : `${encoded}/SKILL.md`}`;
}

/** @param {import('./cache.js').Skill} skill @returns {Promise<string>} */
export async function downloadSkill(skill) {
  if ((skill.path ?? '').startsWith('./external/')) throw new Error(`"${skill.id}" is an external skill — available in v2.`);
  const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), 10_000);
  try { const res = await fetch(buildRawUrl(skill.path), { signal: controller.signal }); if (!res.ok) throw new Error(`Failed to download: HTTP ${res.status}`); return res.text(); } finally { clearTimeout(timer); }
}

/** @param {string} id @param {string} content @param {string} cwd @param {{ yes?: boolean }} [opts] @returns {Promise<{ installed?: boolean, skipped?: boolean, path?: string }>} */
export async function writeSkill(id, content, cwd, opts = {}) {
  const safeId = assertSafeSkillId(id);
  const skillsRoot = resolveWithin(cwd, '.claude', 'skills');
  const targetDir = resolveWithin(skillsRoot, safeId);
  const targetFile = resolveWithin(targetDir, 'SKILL.md');
  await mkdir(skillsRoot, { recursive: true });
  await assertSafeWriteTarget(cwd, skillsRoot);
  await mkdir(targetDir, { recursive: true });
  await assertSafeWriteTarget(cwd, targetFile);
  if (await fileExists(targetFile)) {
    if (!opts.yes && !process.stdin.isTTY) { process.stderr.write(`Skipping ${id}: already installed (use --yes to overwrite)\n`); return { skipped: true }; }
    if (!opts.yes && !(await prompt(`"${id}" already installed. Overwrite? [y/N] `)).toLowerCase().startsWith('y')) return { skipped: true };
  }
  await writeFile(targetFile, content, 'utf8');
  return { installed: true, path: targetFile };
}

/** @param {string} cwd @param {{ id: string, path: string, arena?: { score?: number } }} skill */
export async function writeManifest(cwd, skill) {
  const manifest = await readManifest(cwd);
  const entry = { id: skill.id, installedAt: new Date().toISOString(), path: skill.path, ...(typeof skill.arena?.score === 'number' ? { score: skill.arena.score } : {}) };
  await saveManifest(cwd, { version: 1, skills: [...manifest.skills.filter(item => item.id !== skill.id), entry] });
}

/** @param {import('./cache.js').Skill[]} matches @param {{ yes?: boolean }} opts @param {(question: string) => Promise<string>} [promptFn] @returns {Promise<import('./cache.js').Skill>} */
export async function selectSkill(matches, opts, promptFn = prompt) {
  if (matches.length === 1) return matches[0];
  if (opts.yes || !process.stdin.isTTY) { const skill = matches[0]; console.log(`Multiple matches — auto-selecting: ${skill.id} (score: ${skill.arena?.score ?? '?'})`); return skill; }
  console.log(`Multiple matches for "${matches[0].id}":`); matches.forEach((s, i) => console.log(`  ${i + 1}. ${s.id} (score: ${s.arena?.score ?? '?'}) — ${(s.description ?? '').slice(0, 60)}`));
  while (true) { const ans = await promptFn(`Pick [1-${matches.length}] (default 1): `); if (!ans) return matches[0]; const n = Number.parseInt(ans, 10); if (Number.isInteger(n) && n >= 1 && n <= matches.length) return matches[n - 1]; console.error(`Invalid choice. Enter a number from 1 to ${matches.length}, or press Enter to cancel.`); }
}

/** @param {string} query @param {import('./cache.js').SkillIndex} index @param {string} cwd @param {{ yes?: boolean }} [opts] */
export async function install(query, index, cwd, opts = {}) {
  const matches = resolveSkill(query, index.skills ?? []); if (!matches.length) { console.error(`Skill "${query}" not found.`); process.exit(1); }
  const skill = await selectSkill(matches, opts); process.stdout.write(`Downloading ${skill.id}...\n`); const result = await writeSkill(skill.id, await downloadSkill(skill), cwd, opts);
  if (result.skipped) { console.log(`Skipped ${skill.id}.`); return; }
  await writeManifest(cwd, skill); console.log(`✓ Installed ${skill.id}`); console.log(`  Path: ${result.path}`); console.log('  Restart Claude Code or run /skills reload to activate.');
}
