// @ts-check

import { constants } from 'node:fs';
import { open, readFile, writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { assertSafeWriteTarget, resolveWithin } from './path-safety.js';

export const MANIFEST_NAME = '.ultraskills-manifest.json';
export const MANIFEST_VERSION = 1;

/** @param {unknown} id @returns {string} */
export function assertSafeSkillId(id) {
  if (typeof id !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id) || id === '.' || id === '..') {
    throw new Error(`Unsafe skill id: ${String(id)}`);
  }
  return id;
}

/** @typedef {{ id: string, path?: string, installedAt?: string, score?: number }} ManifestEntry */
/** @typedef {{ version: 1, skills: ManifestEntry[] }} Manifest */

/** @param {unknown} value @returns {Manifest} */
export function normalizeManifest(value) {
  /** @type {ManifestEntry[]} */
  const skills = [];
  if (value && typeof value === 'object') {
    const record = /** @type {Record<string, unknown>} */ (value);
    const source = Array.isArray(record.skills)
      ? record.skills.map(entry => ({ entry }))
      : Object.entries(record).map(([id, entry]) => ({ id, entry }));
    for (const item of source) {
      if (!item.entry || typeof item.entry !== 'object') continue;
      const e = /** @type {Record<string, unknown>} */ (item.entry);
      const id = typeof item.id === 'string' ? item.id : e.id;
      if (typeof id !== 'string') continue;
      skills.push({ id, ...(typeof e.path === 'string' ? { path: e.path } : {}), ...(typeof e.installedAt === 'string' ? { installedAt: e.installedAt } : {}), ...(typeof e.score === 'number' ? { score: e.score } : {}) });
    }
  }
  return { version: MANIFEST_VERSION, skills };
}

/** @param {string} cwd @returns {Promise<string>} */
async function manifestPath(cwd) {
  const skillsRoot = resolveWithin(cwd, '.claude', 'skills');
  await mkdir(skillsRoot, { recursive: true });
  const path = resolveWithin(skillsRoot, MANIFEST_NAME);
  await assertSafeWriteTarget(cwd, path);
  return path;
}

/** @param {string} cwd @returns {Promise<Manifest>} */
export async function readManifest(cwd) {
  const path = join(cwd, '.claude', 'skills', MANIFEST_NAME);
  try { return normalizeManifest(JSON.parse(await readFile(path, 'utf8'))); } catch { return { version: MANIFEST_VERSION, skills: [] }; }
}

/** @param {string} cwd @param {Manifest} manifest @returns {Promise<void>} */
export async function saveManifest(cwd, manifest) {
  const path = await manifestPath(cwd);
  const data = JSON.stringify(normalizeManifest(manifest), null, 2);
  const noFollow = typeof constants.O_NOFOLLOW === 'number' ? constants.O_NOFOLLOW : 0;
  if (noFollow) {
    const handle = await open(path, constants.O_WRONLY | constants.O_CREAT | constants.O_TRUNC | noFollow, 0o600);
    try { await handle.writeFile(data, 'utf8'); } finally { await handle.close(); }
    return;
  }
  await writeFile(path, data, { encoding: 'utf8', mode: 0o600, flag: 'w' });
}
