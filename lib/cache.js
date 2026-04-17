// @ts-check
/**
 * cache.js — index.json fetch + 24hr TTL disk cache
 * ~/.ultraskills/index.json + ~/.ultraskills/index-fetched-at
 * Node 18+ native fetch; zero external deps.
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir } from 'node:os';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';
const CACHE_DIR = join(homedir(), '.ultraskills');
const INDEX_FILE = join(CACHE_DIR, 'index.json');
const TIMESTAMP_FILE = join(CACHE_DIR, 'index-fetched-at');
const TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

/**
 * @typedef {{ id: string, path: string, description?: string, tags?: string[], name?: string, arena?: { category?: string, score?: number, is_winner?: boolean, rank?: number } }} Skill
 * @typedef {{ version: string, skills: Skill[] }} SkillIndex
 */

/** mkdir -p ~/.ultraskills/ — silent */
export async function ensureCacheDir() {
  await mkdir(CACHE_DIR, { recursive: true });
}

/**
 * Returns true if cache is missing or older than TTL.
 * @returns {Promise<boolean>}
 */
export async function isCacheStale() {
  try {
    const ts = await readFile(TIMESTAMP_FILE, 'utf8');
    const age = Date.now() - parseInt(ts, 10);
    return age > TTL_MS;
  } catch {
    return true; // file missing → stale
  }
}

/**
 * Fetch fresh index from GitHub, write to disk, update timestamp.
 * @returns {Promise<SkillIndex>}
 */
export async function fetchAndCacheIndex() {
  process.stderr.write('Fetching skill index...\n');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10_000);
  try {
    const res = await fetch(`${BASE_RAW_URL}index.json`, { signal: controller.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = /** @type {SkillIndex} */ (await res.json());
    await ensureCacheDir();
    await Promise.all([
      writeFile(INDEX_FILE, JSON.stringify(data), 'utf8'),
      writeFile(TIMESTAMP_FILE, String(Date.now()), 'utf8'),
    ]);
    return data;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Load index — from disk cache when fresh, else fetch.
 * On network failure, falls back to stale cache if available.
 * @param {boolean} [forceRefresh]
 * @returns {Promise<SkillIndex>}
 */
export async function loadIndex(forceRefresh = false) {
  await ensureCacheDir();

  if (!forceRefresh && !(await isCacheStale())) {
    try {
      const raw = await readFile(INDEX_FILE, 'utf8');
      return /** @type {SkillIndex} */ (JSON.parse(raw));
    } catch {
      // fall through to fetch
    }
  }

  try {
    return await fetchAndCacheIndex();
  } catch (err) {
    // Network failure — try stale cache as fallback
    try {
      const raw = await readFile(INDEX_FILE, 'utf8');
      process.stderr.write(`Warning: Could not reach GitHub (${/** @type {Error} */(err).message}). Using cached index (may be stale).\n`);
      return /** @type {SkillIndex} */ (JSON.parse(raw));
    } catch {
      throw new Error('No index available. Run with internet connection first.');
    }
  }
}

/**
 * Legacy alias for bin/ultraskills.js compatibility.
 * @param {{ refresh?: boolean }} [opts]
 * @returns {Promise<SkillIndex>}
 */
export async function fetchIndex({ refresh = false } = {}) {
  return loadIndex(refresh);
}
