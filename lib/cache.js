/**
 * cache.js — index.json fetch + 24hr TTL cache
 * Node 18+ native fetch, no external deps
 */

import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir } from 'node:os';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';
const CACHE_DIR = join(homedir(), '.ultraskills');
const CACHE_INDEX = join(CACHE_DIR, 'index.json');
const CACHE_TS = join(CACHE_DIR, 'index-fetched-at');
const TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

async function ensureCacheDir() {
  await mkdir(CACHE_DIR, { recursive: true });
}

async function readCache() {
  try {
    const [data, ts] = await Promise.all([
      readFile(CACHE_INDEX, 'utf8'),
      readFile(CACHE_TS, 'utf8'),
    ]);
    return { data: JSON.parse(data), fetchedAt: parseInt(ts, 10) };
  } catch {
    return null;
  }
}

async function writeCache(data) {
  await ensureCacheDir();
  await Promise.all([
    writeFile(CACHE_INDEX, JSON.stringify(data), 'utf8'),
    writeFile(CACHE_TS, String(Date.now()), 'utf8'),
  ]);
}

export async function fetchIndex({ refresh = false } = {}) {
  await ensureCacheDir();

  const cached = await readCache();
  const age = cached ? Date.now() - cached.fetchedAt : Infinity;
  const stale = age > TTL_MS;

  if (cached && !refresh && !stale) {
    return cached.data;
  }

  // Fetch fresh
  try {
    const res = await fetch(`${BASE_RAW_URL}index.json`, {
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    await writeCache(data);
    return data;
  } catch (err) {
    if (cached) {
      process.stderr.write('Could not reach GitHub. Using cached index (may be stale).\n');
      return cached.data;
    }
    throw new Error('No index available. Run with internet connection first.');
  }
}
