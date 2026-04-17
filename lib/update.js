// @ts-check
/**
 * update.js — re-download all installed skills using fresh index
 */

import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { fetchIndex } from './cache.js';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';
const MANIFEST_NAME = '.ultraskills-manifest.json';

/**
 * @typedef {{ id: string, installedAt?: number }} ManifestEntry
 * @typedef {{ skills: ManifestEntry[] }} Manifest
 */

/**
 * readManifest — read manifest or fallback to scanning SKILL.md dirs
 * @param {string} cwd
 * @returns {Promise<{ ids: string[], hasManifest: boolean }>}
 */
export async function readManifest(cwd) {
  const manifestPath = join(cwd, '.claude', 'skills', MANIFEST_NAME);
  try {
    const raw = await readFile(manifestPath, 'utf8');
    /** @type {Manifest} */
    const m = JSON.parse(raw);
    const ids = (m.skills ?? []).map(e => e.id).filter(Boolean);
    return { ids, hasManifest: true };
  } catch {
    // Fallback: scan .claude/skills/*/SKILL.md
    const skillsDir = join(cwd, '.claude', 'skills');
    try {
      const entries = await readdir(skillsDir, { withFileTypes: true });
      const dirs = entries.filter(e => e.isDirectory()).map(e => e.name);
      const ids = [];
      for (const dir of dirs) {
        try {
          await readFile(join(skillsDir, dir, 'SKILL.md'), 'utf8');
          ids.push(dir);
        } catch { /* no SKILL.md, skip */ }
      }
      return { ids, hasManifest: false };
    } catch {
      return { ids: [], hasManifest: false };
    }
  }
}

/**
 * updateManifest — write back manifest after update
 * @param {string} cwd
 * @param {string[]} ids
 */
async function updateManifest(cwd, ids) {
  const manifestPath = join(cwd, '.claude', 'skills', MANIFEST_NAME);
  /** @type {Manifest} */
  const m = { skills: ids.map(id => ({ id, installedAt: Date.now() })) };
  await writeFile(manifestPath, JSON.stringify(m, null, 2), 'utf8');
}

/**
 * update — force-refresh index + re-download all installed skills
 * @param {{ skills: Array<{ id: string, path: string }> }} index  (fresh, caller must pass fetchIndex({ refresh:true }))
 * @param {string} cwd
 * @param {{ yes?: boolean }} [opts]
 */
export async function update(index, cwd, opts = {}) {
  const skills = index.skills ?? [];
  const skillMap = Object.fromEntries(skills.map(s => [s.id, s]));

  const { ids } = await readManifest(cwd);

  if (!ids.length) {
    console.log('No skills installed. Run: npx ultraskills install <skill>');
    return;
  }

  const skillsDir = join(cwd, '.claude', 'skills');
  let updated = 0, skipped = 0, notFound = 0;

  for (const id of ids) {
    if (!skillMap[id]) {
      process.stderr.write(`  ⚠ skill "${id}" not found in current index, skipping\n`);
      notFound++;
      continue;
    }
    const skill = skillMap[id];
    try {
      const rawPath = skill.path.replace(/^\.\//, '');
      const encodedPath = rawPath.split('/').map(encodeURIComponent).join('/');
      const skillMdUrl = `${BASE_RAW_URL}${encodedPath}/SKILL.md`;
      const res = await fetch(skillMdUrl, { signal: AbortSignal.timeout(15000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const content = await res.text();
      const destDir = join(skillsDir, id);
      await mkdir(destDir, { recursive: true });
      await writeFile(join(destDir, 'SKILL.md'), content, 'utf8');
      console.log(`  ✓ ${id}`);
      updated++;
    } catch (/** @type {unknown} */ err) {
      const e = /** @type {{ message?: string }} */ (err);
      process.stderr.write(`  ✗ ${id}: ${e.message ?? String(err)}\n`);
      skipped++;
    }
  }

  // Refresh manifest with same ids (timestamps updated)
  try { await updateManifest(cwd, ids); } catch { /* non-fatal */ }

  console.log(`\nDone. Updated: ${updated}, skipped: ${skipped}, not-found: ${notFound}.`);
}

/**
 * updateCommand — convenience wrapper that fetches fresh index then calls update()
 * @param {string} cwd
 * @param {{ yes?: boolean }} [opts]
 */
export async function updateCommand(cwd, opts = {}) {
  console.log('Refreshing index...');
  const index = await fetchIndex({ refresh: true });
  await update(index, cwd, opts);
}
