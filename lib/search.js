// @ts-check
/**
 * search.js — 4-tier ranked skill search
 * Tier 1: exact id  Tier 2: id contains  Tier 3: tag contains  Tier 4: description contains
 */

/** @param {string} s */
const n = (s) => String(s ?? '').toLowerCase();

/** @param {{ arena?: { score?: number } }} skill */
const getScore = (skill) => skill?.arena?.score ?? 0;

/**
 * @typedef {{ id: string, description: string, tags: string[], path: string, arena: { category: string, score: number, is_winner: boolean, rank: number } }} Skill
 * @typedef {{ tier: number, skill: Skill }} RankedResult
 */

/**
 * searchSkills — 4-tier ranking, returns flat Skill[] (each skill in highest tier only)
 * @param {string} query
 * @param {Skill[]} skills
 * @returns {Skill[]}
 */
export function searchSkills(query, skills) {
  const q = n(query);
  const seen = new Set();
  /** @type {Skill[]} */
  const results = [];

  // Tier 1: exact id
  for (const s of skills) {
    if (n(s.id) === q) {
      seen.add(s.id);
      results.push(s);
    }
  }

  // Tier 2: id contains
  const t2 = skills
    .filter(s => !seen.has(s.id) && n(s.id).includes(q))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t2) { seen.add(s.id); results.push(s); }

  // Tier 3: tag contains
  const t3 = skills
    .filter(s => !seen.has(s.id) && Array.isArray(s.tags) && s.tags.some(t => n(t).includes(q)))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t3) { seen.add(s.id); results.push(s); }

  // Tier 4: description contains
  const t4 = skills
    .filter(s => !seen.has(s.id) && n(s.description).includes(q))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t4) { seen.add(s.id); results.push(s); }

  return results;
}

/**
 * formatSearchResults — aligned tabular output
 * @param {Skill[]} results
 * @param {number} [limit]
 */
export function formatSearchResults(results, limit = 20) {
  if (!results.length) {
    console.log('No skills found.');
    return;
  }

  const shown = results.slice(0, limit);
  const col = (/** @type {string|number} */ v, /** @type {number} */ w) =>
    String(v ?? '').slice(0, w).padEnd(w);

  console.log(`${'id'.padEnd(32)} ${'score'.padEnd(7)} ${'category'.padEnd(20)} winner`);
  console.log('-'.repeat(68));
  for (const s of shown) {
    const score = s.arena?.score != null ? s.arena.score.toFixed(1) : '-';
    const cat   = s.arena?.category ?? '-';
    const win   = s.arena?.is_winner ? '★' : '';
    console.log(`${col(s.id, 32)} ${score.padEnd(7)} ${col(cat, 20)} ${win}`);
  }

  const rest = results.length - shown.length;
  if (rest > 0) {
    console.log(`\n... and ${rest} more.`);
  }
}

/**
 * resolveSkill — for install: find best-matching skills by id/tag/description
 * Returns up to 5 candidates sorted by arena score (highest first).
 * @param {string} query
 * @param {Skill[]} skills
 * @returns {Skill[]}
 */
export function resolveSkill(query, skills) {
  const q = n(query);
  const seen = new Set();
  /** @type {Skill[]} */
  const results = [];

  // Exact id match (tier 1) — return immediately, single match
  for (const s of skills) {
    if (n(s.id) === q) return [s];
  }

  // id contains
  const t2 = skills.filter(s => !seen.has(s.id) && n(s.id).includes(q))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t2) { seen.add(s.id); results.push(s); }

  // tag contains
  const t3 = skills.filter(s => !seen.has(s.id) && Array.isArray(s.tags) && s.tags.some(t => n(t).includes(q)))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t3) { seen.add(s.id); results.push(s); }

  // description contains
  const t4 = skills.filter(s => !seen.has(s.id) && n(s.description).includes(q))
    .sort((a, b) => getScore(b) - getScore(a));
  for (const s of t4) { seen.add(s.id); results.push(s); }

  return results.slice(0, 5);
}

/**
 * search — main entry point for 'search' command
 * @param {string} query
 * @param {{ skills: Skill[] }} index
 * @param {{ limit?: number }} [opts]
 */
export function search(query, index, opts = {}) {
  const results = searchSkills(query, index.skills ?? []);
  formatSearchResults(results, opts.limit ?? 20);
}
