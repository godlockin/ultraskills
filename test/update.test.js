/**
 * test/update.test.js — test update flow via testable inline logic
 * Uses node:test + assert (Node 18+ built-in). No network calls.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import { readdir, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

// ---------------------------------------------------------------------------
// readManifest — inline the logic from update.js (no export there yet)
// Tests the manifest-reading pattern used internally
// ---------------------------------------------------------------------------

async function readManifest(cwd) {
  const manifestPath = join(cwd, '.claude', 'skills', '.ultraskills-manifest.json');
  try {
    const raw = await readFile(manifestPath, 'utf8');
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function writeManifest(cwd, data) {
  const dir = join(cwd, '.claude', 'skills');
  await mkdir(dir, { recursive: true });
  await writeFile(join(dir, '.ultraskills-manifest.json'), JSON.stringify(data, null, 2), 'utf8');
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

test('readManifest returns empty object when .claude/skills does not exist', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const manifest = await readManifest(tmp);
  assert.deepEqual(manifest, {});
});

test('readManifest returns empty object when manifest file missing', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  mkdirSync(join(tmp, '.claude', 'skills'), { recursive: true });
  const manifest = await readManifest(tmp);
  assert.deepEqual(manifest, {});
});

test('readManifest reads existing manifest correctly', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  await writeManifest(tmp, { 'bdi-mental-states': { installedAt: '2026-01-01' } });
  const manifest = await readManifest(tmp);
  assert.ok('bdi-mental-states' in manifest);
  assert.equal(manifest['bdi-mental-states'].installedAt, '2026-01-01');
});

test('readManifest handles multiple skills', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const data = {
    'code-review': { installedAt: '2026-01-01', version: '1.0.0' },
    'git-workflow': { installedAt: '2026-02-01', version: '1.1.0' },
  };
  await writeManifest(tmp, data);
  const manifest = await readManifest(tmp);
  assert.equal(Object.keys(manifest).length, 2);
  assert.ok('code-review' in manifest);
  assert.ok('git-workflow' in manifest);
});

// ---------------------------------------------------------------------------
// updateTestable — inline the update-skills logic for testability
// ---------------------------------------------------------------------------

async function updateTestable({ cwd, skillMap, fetcher }) {
  const skillsDir = join(cwd, '.claude', 'skills');
  let entries;
  try {
    entries = await readdir(skillsDir, { withFileTypes: true });
  } catch {
    return { updated: 0, skipped: 0, errors: [], reason: 'no_dir' };
  }

  const installed = entries.filter(e => e.isDirectory()).map(e => e.name);
  if (!installed.length) return { updated: 0, skipped: 0, errors: [], reason: 'none_installed' };

  let updated = 0, skipped = 0;
  const errors = [];

  for (const id of installed) {
    if (!skillMap[id]) { skipped++; continue; }
    const skill = skillMap[id];
    try {
      const content = await fetcher(skill.path);
      const destDir = join(skillsDir, id);
      await mkdir(destDir, { recursive: true });
      await writeFile(join(destDir, 'SKILL.md'), content, 'utf8');
      updated++;
    } catch (err) {
      errors.push({ id, message: err.message });
    }
  }
  return { updated, skipped, errors };
}

test('updateTestable — no .claude/skills — reports no_dir', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const result = await updateTestable({ cwd: tmp, skillMap: {}, fetcher: async () => '' });
  assert.equal(result.reason, 'no_dir');
});

test('updateTestable — empty skills dir — reports none_installed', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  await mkdir(join(tmp, '.claude', 'skills'), { recursive: true });
  const result = await updateTestable({ cwd: tmp, skillMap: {}, fetcher: async () => '' });
  assert.equal(result.reason, 'none_installed');
});

test('updateTestable — skill not in index — skips it', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const skillDir = join(tmp, '.claude', 'skills', 'orphan-skill');
  mkdirSync(skillDir, { recursive: true });
  writeFileSync(join(skillDir, 'SKILL.md'), 'old');
  const result = await updateTestable({ cwd: tmp, skillMap: {}, fetcher: async () => '' });
  assert.equal(result.skipped, 1);
  assert.equal(result.updated, 0);
});

test('updateTestable — happy path — overwrites SKILL.md', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const skillDir = join(tmp, '.claude', 'skills', 'code-review');
  mkdirSync(skillDir, { recursive: true });
  writeFileSync(join(skillDir, 'SKILL.md'), 'old content');

  const skillMap = { 'code-review': { id: 'code-review', path: './community/code-review' } };
  const fetcher = async () => 'new content';
  const result = await updateTestable({ cwd: tmp, skillMap, fetcher });

  assert.equal(result.updated, 1);
  assert.equal(result.errors.length, 0);
  const written = await readFile(join(skillDir, 'SKILL.md'), 'utf8');
  assert.equal(written, 'new content');
});

test('updateTestable — fetch error — records in errors', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const skillDir = join(tmp, '.claude', 'skills', 'code-review');
  mkdirSync(skillDir, { recursive: true });
  writeFileSync(join(skillDir, 'SKILL.md'), 'old content');

  const skillMap = { 'code-review': { id: 'code-review', path: './community/code-review' } };
  const fetcher = async () => { throw new Error('network timeout'); };
  const result = await updateTestable({ cwd: tmp, skillMap, fetcher });

  assert.equal(result.updated, 0);
  assert.equal(result.errors.length, 1);
  assert.equal(result.errors[0].id, 'code-review');
  assert.ok(result.errors[0].message.includes('network timeout'));
});

test('updateTestable — mixed: 1 updated, 1 skipped, 1 error', async () => {
  const tmp = mkdtempSync(join(tmpdir(), 'ultraskills-update-test-'));
  const skillsDir = join(tmp, '.claude', 'skills');

  // installed: code-review (in index), orphan (not in index), bad-fetch (will error)
  for (const id of ['code-review', 'orphan', 'bad-fetch']) {
    mkdirSync(join(skillsDir, id), { recursive: true });
    writeFileSync(join(skillsDir, id, 'SKILL.md'), 'old');
  }

  const skillMap = {
    'code-review': { path: './community/code-review' },
    'bad-fetch': { path: './community/bad-fetch' },
  };
  const fetcher = async (path) => {
    if (path.includes('bad-fetch')) throw new Error('404');
    return 'updated content';
  };

  const result = await updateTestable({ cwd: tmp, skillMap, fetcher });
  assert.equal(result.updated, 1);
  assert.equal(result.skipped, 1);
  assert.equal(result.errors.length, 1);
});
