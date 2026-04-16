import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, rm, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const TMP = join(tmpdir(), 'ultraskills-install-' + process.pid);

const skills = [
  { id: 'code-review', name: 'Code Review', description: 'Review PRs', path: './community/code-review/SKILL.md', tags: [], arena: { score: 9.0 } },
  { id: 'external-skill', name: 'External', description: 'External skill', path: './external/some/SKILL.md', tags: [], arena: { score: 7.0 } },
  { id: 'no-match-other', name: 'Other', description: 'unrelated', path: './community/other/SKILL.md', tags: [], arena: { score: 5.0 } },
];

const MOCK_CONTENT = '# Code Review Skill\nDo reviews.';

// Inline installable logic (mirrors lib/install.js)
const ALLOWED_PREFIXES = ['./community/', './devops/', './engineering/', './creative/'];

async function installTestable(skillId, { yes = false, cwd = TMP, skills: sk = skills, fetcher } = {}) {
  const { resolveSkill } = await import('../lib/search.js');
  const { mkdir: mkd, writeFile: wf, access } = await import('node:fs/promises');

  const matches = resolveSkill(skillId, sk);
  if (!matches.length) throw Object.assign(new Error(`not_found`), { code: 'NOT_FOUND' });

  const skill = yes ? matches[0] : matches[0]; // auto-pick in tests

  if (!ALLOWED_PREFIXES.some(p => skill.path?.startsWith(p))) {
    throw Object.assign(new Error('external'), { code: 'EXTERNAL' });
  }

  const destDir = join(cwd, '.claude', 'skills', skill.id);
  const destFile = join(destDir, 'SKILL.md');

  let exists = false;
  try { await access(destFile); exists = true; } catch {}

  if (exists && !yes) throw Object.assign(new Error('conflict'), { code: 'CONFLICT' });

  const content = await fetcher(skill.path);
  await mkd(destDir, { recursive: true });
  await wf(destFile, content, 'utf8');
  return skill.id;
}

test('happy path — installs SKILL.md', async () => {
  await rm(TMP, { recursive: true, force: true });
  await mkdir(TMP, { recursive: true });
  const fetcher = async () => MOCK_CONTENT;
  const id = await installTestable('code-review', { yes: true, cwd: TMP, fetcher });
  assert.equal(id, 'code-review');
  const written = await readFile(join(TMP, '.claude', 'skills', 'code-review', 'SKILL.md'), 'utf8');
  assert.equal(written, MOCK_CONTENT);
});

test('conflict + yes — overwrites', async () => {
  const destDir = join(TMP, '.claude', 'skills', 'code-review');
  await mkdir(destDir, { recursive: true });
  await writeFile(join(destDir, 'SKILL.md'), 'old content');
  const fetcher = async () => 'new content';
  const id = await installTestable('code-review', { yes: true, cwd: TMP, fetcher });
  const written = await readFile(join(destDir, 'SKILL.md'), 'utf8');
  assert.equal(written, 'new content');
});

test('conflict + no — throws CONFLICT', async () => {
  await assert.rejects(
    () => installTestable('code-review', { yes: false, cwd: TMP, fetcher: async () => '' }),
    err => err.code === 'CONFLICT'
  );
});

test('external path — throws EXTERNAL', async () => {
  await assert.rejects(
    () => installTestable('external-skill', { yes: true, cwd: TMP, fetcher: async () => '' }),
    err => err.code === 'EXTERNAL'
  );
});

test('no match — throws NOT_FOUND', async () => {
  await assert.rejects(
    () => installTestable('zzz-does-not-exist', { yes: true, cwd: TMP, fetcher: async () => '' }),
    err => err.code === 'NOT_FOUND'
  );
});
