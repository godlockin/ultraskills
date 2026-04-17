// @ts-check
/**
 * info.js — detailed skill info by exact id
 */

/**
 * @typedef {{ id: string, description: string, path: string, tags: string[], arena: { category: string, score: number, is_winner: boolean, rank: number } }} Skill
 */

/**
 * info — print skill detail card
 * @param {string} id
 * @param {{ skills: Skill[] }} index
 */
export function info(id, index) {
  const skills = index.skills ?? [];
  const skill = skills.find(s => s.id === id);

  if (!skill) {
    process.stderr.write(`Skill "${id}" not found.\ntry: npx ultraskills search ${id}\n`);
    process.exit(1);
  }

  const a = skill.arena ?? {};
  const lpad = (/** @type {string} */ label) => label.padEnd(13);

  console.log(`${lpad('id:')}         ${skill.id}`);
  console.log(`${lpad('description:')} ${skill.description ?? '-'}`);
  console.log(`${lpad('category:')}   ${a.category ?? '-'}`);
  console.log(`${lpad('score:')}      ${a.score != null ? a.score.toFixed(1) + ' / 100' : '-'}`);
  console.log(`${lpad('rank:')}       ${a.rank != null ? a.rank + ' in category' : '-'}`);
  console.log(`${lpad('winner:')}     ${a.is_winner ? '★ yes' : 'no'}`);
  console.log(`${lpad('path:')}       ${skill.path ?? '-'}`);
  console.log(`${lpad('install:')}    npx ultraskills install ${skill.id}`);
}
