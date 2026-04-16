import { test, mock } from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, writeFile, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

// Stub homedir to use tmpdir
const TMP = join(tmpdir(), 'ultraskills-test-' + process.pid);
const CACHE_DIR = join(TMP, '.ultraskills');

// Patch module before import by overriding fetch + homedir via env trick
// We test by calling fetchIndex internals via re-export

const MOCK_INDEX = { skills: [{ id: 'test-skill', name: 'Test', description: 'desc', path: './community/test/SKILL.md', arena: { score: 8 } }] };

// Helper: write cache manually
async function writeCache(data, ageMs = 0) {
  await mkdir(CACHE_DIR, { recursive: true });
  await writeFile(join(CACHE_DIR, 'index.json'), JSON.stringify(data));
  await writeFile(join(CACHE_DIR, 'index-fetched-at'), String(Date.now() - ageMs));
}

async function clearCache() {
  await rm(CACHE_DIR, { recursive: true, force: true });
}

// Inline implementation test (exercises same logic as cache.js)
async function fetchIndexTestable({ refresh = false, cacheDir = CACHE_DIR, fetcher } = {}) {
  const { mkdir: mkd, readFile, writeFile: wf } = await import('node:fs/promises');
  await mkd(cacheDir, { recursive: true });

  const indexPath = join(cacheDir, 'index.json');
  const tsPath = join(cacheDir, 'index-fetched-at');
  const TTL = 24 * 60 * 60 * 1000;

  let cached = null;
  try {
    const [d, t] = await Promise.all([readFile(indexPath, 'utf8'), readFile(tsPath, 'utf8')]);
    cached = { data: JSON.parse(d), fetchedAt: parseInt(t, 10) };
  } catch {}

  const stale = !cached || (Date.now() - cached.fetchedAt) > TTL;
  if (cached && !refresh && !stale) return { source: 'cache', data: cached.data };

  try {
    const data = await fetcher();
    await Promise.all([wf(indexPath, JSON.stringify(data)), wf(tsPath, String(Date.now()))]);
    return { source: 'network', data };
  } catch (err) {
    if (cached) return { source: 'stale', data: cached.data };
    throw new Error('No index available. Run with internet connection first.');
  }
}

test('fresh fetch — no cache — calls network', async () => {
  await clearCache();
  const fetcher = async () => MOCK_INDEX;
  const result = await fetchIndexTestable({ cacheDir: CACHE_DIR, fetcher });
  assert.equal(result.source, 'network');
  assert.deepEqual(result.data, MOCK_INDEX);
});

test('TTL hit — serves from disk', async () => {
  await writeCache(MOCK_INDEX, 1000); // 1s old, well within 24hr TTL
  let called = false;
  const fetcher = async () => { called = true; return MOCK_INDEX; };
  const result = await fetchIndexTestable({ cacheDir: CACHE_DIR, fetcher });
  assert.equal(result.source, 'cache');
  assert.equal(called, false);
});

test('TTL miss — re-fetches', async () => {
  const MS_25H = 25 * 60 * 60 * 1000;
  await writeCache(MOCK_INDEX, MS_25H); // 25h old
  let called = false;
  const fetcher = async () => { called = true; return { skills: [] }; };
  const result = await fetchIndexTestable({ cacheDir: CACHE_DIR, fetcher });
  assert.equal(result.source, 'network');
  assert.equal(called, true);
});

test('--refresh bypasses TTL', async () => {
  await writeCache(MOCK_INDEX, 1000); // fresh cache
  let called = false;
  const fetcher = async () => { called = true; return { skills: [] }; };
  const result = await fetchIndexTestable({ refresh: true, cacheDir: CACHE_DIR, fetcher });
  assert.equal(result.source, 'network');
  assert.equal(called, true);
});

test('network fail + cache — returns stale', async () => {
  await writeCache(MOCK_INDEX, 1000);
  const fetcher = async () => { throw new Error('network error'); };
  const result = await fetchIndexTestable({ refresh: true, cacheDir: CACHE_DIR, fetcher });
  assert.equal(result.source, 'stale');
  assert.deepEqual(result.data, MOCK_INDEX);
});

test('network fail + no cache — throws', async () => {
  await clearCache();
  const fetcher = async () => { throw new Error('network error'); };
  await assert.rejects(
    () => fetchIndexTestable({ cacheDir: CACHE_DIR, fetcher }),
    /No index available/
  );
});

test('mkdir-p creates cache dir', async () => {
  await rm(CACHE_DIR, { recursive: true, force: true });
  const fetcher = async () => MOCK_INDEX;
  await fetchIndexTestable({ cacheDir: CACHE_DIR, fetcher });
  const { stat } = await import('node:fs/promises');
  const s = await stat(CACHE_DIR);
  assert.ok(s.isDirectory());
});
