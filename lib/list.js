// @ts-check
/**
 * list.js — tabular skill listing with category filter + winner filter
 */

/**
 * @typedef {{ id: string, arena: { category: string, score: number, is_winner: boolean, rank: number } }} Skill
 */

/**
 * listSkills — filter by category substring, sort by score desc, print table
 * Signature: listSkills(category, skills, limit?)
 * @param {string} category  substring filter ('' = no filter)
 * @param {Skill[]} skillsArr
 * @param {number} [limit]
 */
export function listSkills(category, skillsArr, limit = 50) {
  let skills = skillsArr ?? [];

  if (category) {
    const q = category.toLowerCase();
    skills = skills.filter(s =>
      String(s.arena?.category ?? '').toLowerCase().includes(q)
    );
  }

  if (!skills.length) {
    const msg = category ? `No skills found for category "${category}".` : 'No skills in index.';
    console.log(msg);
    return;
  }

  // Sort: score desc (highest first)
  const sorted = [...skills].sort((a, b) =>
    (b.arena?.score ?? 0) - (a.arena?.score ?? 0)
  );

  const total = sorted.length;
  const shown = sorted.slice(0, limit);

  const col = (/** @type {string|number} */ v, /** @type {number} */ w) =>
    String(v ?? '').slice(0, w).padEnd(w);

  console.log(`${'category'.padEnd(22)} ${'id'.padEnd(32)} ${'score'.padEnd(8)}`);
  console.log('-'.repeat(65));
  for (const s of shown) {
    const cat   = s.arena?.category ?? '-';
    const score = s.arena?.score != null ? s.arena.score.toFixed(1) : '-';
    const win   = s.arena?.is_winner ? ' ★' : '';
    console.log(`${col(cat, 22)} ${col(s.id, 32)} ${score}${win}`);
  }

  if (total > limit) {
    console.log(`\nShowing ${limit} of ${total}. Use --category to filter.`);
  }
}
