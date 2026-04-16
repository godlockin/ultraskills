/**
 * info.js — show skill detail
 */
import { resolveSkill } from './search.js';

export function infoSkill(skillId, skills) {
  const matches = resolveSkill(skillId, skills);
  if (!matches.length) {
    console.error(`Skill "${skillId}" not found. Try: npx ultraskills search ${skillId}`);
    process.exit(1);
  }
  const s = matches[0];
  const a = s.arena ?? {};
  console.log(`id:          ${s.id}`);
  console.log(`name:        ${s.name}`);
  console.log(`description: ${s.description}`);
  console.log(`cluster:     ${a.category ?? '-'}`);
  console.log(`score:       ${a.score ?? '-'}`);
  console.log(`rank:        ${a.rank ?? '-'}`);
  console.log(`winner:      ${a.is_winner ? 'yes ★' : 'no'}`);
  console.log(`path:        ${s.path}`);
}
