/**
 * search.js — skill resolution & search
 * Resolution order: exact id → id prefix/contains → description/name/tags substr
 */

function normalize(s) {
  return String(s ?? '').toLowerCase();
}

function score(skill) {
  return skill?.arena?.score ?? 0;
}

/**
 * resolveSkill(query, skills) → ordered matches
 * Step 1: exact id match → [that skill]
 * Step 2: id contains query → top-5 by score
 * Step 3: description/name/tags substring → top-5 by score
 */
export function resolveSkill(query, skills) {
  const q = normalize(query);

  // Step 1: exact id
  const exact = skills.find(s => normalize(s.id) === q);
  if (exact) return [exact];

  // Step 2: id contains
  const idMatches = skills
    .filter(s => normalize(s.id).includes(q))
    .sort((a, b) => score(b) - score(a))
    .slice(0, 5);
  if (idMatches.length) return idMatches;

  // Step 3: description / name / tags substring
  const descMatches = skills
    .filter(s =>
      normalize(s.description).includes(q) ||
      normalize(s.name).includes(q) ||
      (Array.isArray(s.tags) && s.tags.some(t => normalize(t).includes(q)))
    )
    .sort((a, b) => score(b) - score(a))
    .slice(0, 5);

  return descMatches;
}

/**
 * searchSkills(query, skills) → top-10 across all fields (for 'search' command)
 */
export function searchSkills(query, skills) {
  const q = normalize(query);
  return skills
    .filter(s =>
      normalize(s.id).includes(q) ||
      normalize(s.name).includes(q) ||
      normalize(s.description).includes(q) ||
      (Array.isArray(s.tags) && s.tags.some(t => normalize(t).includes(q)))
    )
    .sort((a, b) => score(b) - score(a))
    .slice(0, 10);
}
