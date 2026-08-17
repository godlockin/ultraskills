// @ts-check
import { readFile, mkdir, readdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fetchIndex } from './cache.js';
import { buildRawUrl } from './install.js';
import { assertSafeSkillId, assertSafeWriteTarget, resolveWithin } from './path-safety.js';
import { readManifest as readCanonicalManifest, saveManifest } from './manifest.js';

/** @param {string} cwd @returns {Promise<{ ids: string[], entries: import('./manifest.js').ManifestEntry[], hasManifest: boolean }>} */
export async function readManifestForUpdate(cwd) {
  const manifest = await readCanonicalManifest(cwd);
  if (manifest.skills.length) return { ids: manifest.skills.map(entry => assertSafeSkillId(entry.id)), entries: manifest.skills, hasManifest: true };
  const skillsDir = resolveWithin(cwd, '.claude', 'skills');
  try {
    const entries = await readdir(skillsDir, { withFileTypes: true }); const ids = [];
    for (const dir of entries.filter(e => e.isDirectory())) { try { const id = assertSafeSkillId(dir.name); await readFile(resolveWithin(skillsDir, id, 'SKILL.md'), 'utf8'); ids.push(id); } catch { /* skip invalid or incomplete entries */ } }
    return { ids, entries: ids.map(id => ({ id })), hasManifest: false };
  } catch { return { ids: [], entries: [], hasManifest: false }; }
}
export const readManifest = readManifestForUpdate;

/** @param {{ skills: Array<{ id: string, path: string, arena?: { score?: number } }> }} index @param {string} cwd @param {{ yes?: boolean }} [opts] */
export async function update(index, cwd, opts = {}) {
  const skillMap = Object.fromEntries((index.skills ?? []).map(s => [s.id, s]));
  const { ids, entries } = await readManifestForUpdate(cwd);
  if (!ids.length) { console.log('No skills installed. Run: npx ultraskills install <skill>'); return; }
  const skillsDir = resolveWithin(cwd, '.claude', 'skills'); let updated = 0; let skipped = 0; let notFound = 0;
  for (const id of ids) {
    const skill = skillMap[id]; if (!skill) { process.stderr.write(`  skill "${id}" not found in current index, skipping\n`); notFound++; continue; }
    try { const res = await fetch(buildRawUrl(skill.path), { signal: AbortSignal.timeout(15000) }); if (!res.ok) throw new Error(`HTTP ${res.status}`); const content = await res.text(); const destDir = resolveWithin(skillsDir, id); await mkdir(destDir, { recursive: true }); const dest = resolveWithin(destDir, 'SKILL.md'); await assertSafeWriteTarget(cwd, dest); await writeFile(dest, content, 'utf8'); console.log(`  ✓ ${id}`); updated++; }
    catch (/** @type {unknown} */ error) { const message = error instanceof Error ? error.message : String(error); process.stderr.write(`  ✗ ${id}: ${message}\n`); skipped++; }
  }
  const freshEntries = entries.map(entry => { const skill = skillMap[entry.id]; return skill ? { ...entry, path: skill.path, ...(typeof skill.arena?.score === 'number' ? { score: skill.arena.score } : {}) } : entry; });
  await saveManifest(cwd, { version: 1, skills: freshEntries });
  console.log(`\nDone. Updated: ${updated}, skipped: ${skipped}, not-found: ${notFound}.`);
}

/** @param {string} cwd @param {{ yes?: boolean }} [opts] */
export async function updateCommand(cwd, opts = {}) { console.log('Refreshing index...'); await update(await fetchIndex({ refresh: true }), cwd, opts); }
