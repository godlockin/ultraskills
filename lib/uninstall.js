// @ts-check
import { rm, access } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import { assertSafeSkillId, assertSafeWriteTarget, resolveWithin } from './path-safety.js';
import { readManifest, saveManifest } from './manifest.js';

function confirm(message) { return new Promise(resolve => { const rl = createInterface({ input: process.stdin, output: process.stdout }); rl.question(`${message} [y/N] `, answer => { rl.close(); resolve(answer.trim().toLowerCase() === 'y'); }); }); }

/** @param {string} id @param {string} cwd @param {{ yes?: boolean }} [opts] */
export async function uninstall(id, cwd, opts = {}) {
  const safeId = assertSafeSkillId(id);
  const skillsRoot = resolveWithin(cwd, '.claude', 'skills');
  const targetDir = resolveWithin(skillsRoot, safeId);
  await assertSafeWriteTarget(cwd, targetDir);
  try { await access(targetDir); } catch { process.stderr.write(`Skill "${id}" is not installed.\n`); process.exit(1); }
  if (!process.stdin.isTTY && !opts.yes) { process.stderr.write(`Use --yes to confirm uninstall of "${id}".\n`); process.exit(1); }
  if (process.stdin.isTTY && !opts.yes && !(await confirm(`Remove .claude/skills/${id}/?`))) { console.log('Aborted.'); return; }
  await rm(targetDir, { recursive: true, force: true });
  const manifest = await readManifest(cwd);
  await saveManifest(cwd, { version: 1, skills: manifest.skills.filter(entry => entry.id !== id) });
  console.log(`Uninstalled ${id}`);
}
