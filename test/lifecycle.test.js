import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { buildRawUrl, selectSkill, writeManifest } from '../lib/install.js';
import { readManifestForUpdate } from '../lib/update.js';
import { uninstall } from '../lib/uninstall.js';

const skill = (id, score = 1) => ({ id, path: `./community/${id}/SKILL.md`, description: id, arena: { score } });

test('buildRawUrl does not append SKILL.md twice', () => {
  assert.equal(buildRawUrl('./community/foo/SKILL.md'), 'https://raw.githubusercontent.com/godlockin/ultraskills/main/community/foo/SKILL.md');
  assert.equal(buildRawUrl('./community/foo'), 'https://raw.githubusercontent.com/godlockin/ultraskills/main/community/foo/SKILL.md');
});

test('manifest install writes versioned array schema and migrates legacy object', async () => {
  const cwd = await mkdtemp(join(tmpdir(), 'ultraskills-lifecycle-'));
  const dir = join(cwd, '.claude', 'skills');
  await mkdir(dir, { recursive: true });
  await writeFile(join(dir, '.ultraskills-manifest.json'), JSON.stringify({ old: { path: './community/old', installedAt: '2026-01-01', score: 2 } }));
  await writeManifest(cwd, skill('new', 9));
  const manifest = JSON.parse(await readFile(join(dir, '.ultraskills-manifest.json'), 'utf8'));
  assert.equal(manifest.version, 1);
  assert.deepEqual(manifest.skills.map(entry => entry.id), ['old', 'new']);
  assert.equal(manifest.skills[1].score, 9);
});

test('update manifest reader safely migrates legacy object format', async () => {
  const cwd = await mkdtemp(join(tmpdir(), 'ultraskills-lifecycle-'));
  const dir = join(cwd, '.claude', 'skills');
  await mkdir(dir, { recursive: true });
  await writeFile(join(dir, '.ultraskills-manifest.json'), JSON.stringify({ old: { installedAt: '2026-01-01' } }));
  const result = await readManifestForUpdate(cwd);
  assert.deepEqual(result.ids, ['old']);
  assert.equal(result.entries[0].id, 'old');
});

test('interactive selection retries invalid and returns valid match', async () => {
  const answers = ['not-a-number', '99', '2'];
  const originalTTY = process.stdin.isTTY;
  Object.defineProperty(process.stdin, 'isTTY', { value: true, configurable: true });
  try {
    const selected = await selectSkill([skill('one'), skill('two')], {}, async () => answers.shift() ?? '');
    assert.equal(selected.id, 'two');
  } finally {
    Object.defineProperty(process.stdin, 'isTTY', { value: originalTTY, configurable: true });
  }
});

test('uninstall removes skill and writes canonical manifest', async () => {
  const cwd = await mkdtemp(join(tmpdir(), 'ultraskills-lifecycle-'));
  const dir = join(cwd, '.claude', 'skills');
  await mkdir(join(dir, 'one'), { recursive: true });
  await writeFile(join(dir, 'one', 'SKILL.md'), 'content');
  await writeFile(join(dir, '.ultraskills-manifest.json'), JSON.stringify({ one: { path: './community/one' } }));
  await uninstall('one', cwd, { yes: true });
  await assert.rejects(() => access(join(dir, 'one')));
  const manifest = JSON.parse(await readFile(join(dir, '.ultraskills-manifest.json'), 'utf8'));
  assert.deepEqual(manifest, { version: 1, skills: [] });
});

test('CLI binds uninstall export with cwd and yes option', async () => {
  const cli = await readFile(new URL('../bin/ultraskills.js', import.meta.url), 'utf8');
  assert.match(cli, /const \{ uninstall \} = await import\('\.\.\/lib\/uninstall\.js'\)/);
  assert.match(cli, /await uninstall\(skillId, process\.cwd\(\), \{ yes \}\)/);
});
