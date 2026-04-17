// @ts-check
/**
 * uninstall.js — remove installed skill + update manifest
 */

import { rm, access, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { createInterface } from 'node:readline';

const MANIFEST_NAME = '.ultraskills-manifest.json';

/**
 * @typedef {{ id: string, installedAt?: number }} ManifestEntry
 * @typedef {{ skills: ManifestEntry[] }} Manifest
 */

/**
 * confirm — readline Y/N prompt, resolves true if user types y/Y
 * @param {string} message
 * @returns {Promise<boolean>}
 */
function confirm(message) {
  return new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    rl.question(`${message} [y/N] `, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

/**
 * removeFromManifest — delete entry for id, write back
 * @param {string} manifestPath
 * @param {string} id
 */
async function removeFromManifest(manifestPath, id) {
  try {
    const raw = await readFile(manifestPath, 'utf8');
    /** @type {Manifest} */
    const m = JSON.parse(raw);
    m.skills = (m.skills ?? []).filter(e => e.id !== id);
    await writeFile(manifestPath, JSON.stringify(m, null, 2), 'utf8');
  } catch {
    // manifest missing or invalid — non-fatal
  }
}

/**
 * uninstall — remove skill directory + update manifest
 * @param {string} id
 * @param {string} cwd
 * @param {{ yes?: boolean }} [opts]
 */
export async function uninstall(id, cwd, opts = {}) {
  const targetDir = join(cwd, '.claude', 'skills', id);
  const manifestPath = join(cwd, '.claude', 'skills', MANIFEST_NAME);

  // Check skill exists
  try {
    await access(targetDir);
  } catch {
    process.stderr.write(`Skill "${id}" is not installed.\n`);
    process.exit(1);
  }

  // Confirm
  const isTTY = Boolean(process.stdin.isTTY);

  if (!isTTY && !opts.yes) {
    process.stderr.write(`Use --yes to confirm uninstall of "${id}".\n`);
    process.exit(1);
  }

  if (isTTY && !opts.yes) {
    const ok = await confirm(`Remove .claude/skills/${id}/?`);
    if (!ok) {
      console.log('Aborted.');
      return;
    }
  }

  // Remove directory
  await rm(targetDir, { recursive: true, force: true });

  // Update manifest
  await removeFromManifest(manifestPath, id);

  console.log(`Uninstalled ${id}`);
}
