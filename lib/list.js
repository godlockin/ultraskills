/**
 * list.js — tabular skill listing
 */

export function listSkills(category, skills) {
  let filtered = skills;
  if (category) {
    const q = category.toLowerCase();
    filtered = skills.filter(s =>
      String(s.arena?.category ?? '').toLowerCase().includes(q) ||
      String(s.source_dir ?? '').toLowerCase().includes(q) ||
      String(s.tags?.join(' ') ?? '').toLowerCase().includes(q)
    );
  }

  filtered = [...filtered].sort((a, b) => (b.arena?.score ?? 0) - (a.arena?.score ?? 0));

  if (!filtered.length) {
    console.log(category ? `No skills found for "${category}".` : 'No skills in index.');
    return;
  }

  const col = (s, n) => String(s ?? '').slice(0, n).padEnd(n);
  console.log(`${col('cluster', 20)} ${col('id', 30)} ${'score'.padEnd(7)} winner`);
  console.log('-'.repeat(65));
  for (const s of filtered) {
    const cluster = s.arena?.category ?? s.source_dir ?? '';
    const winner = s.arena?.is_winner ? '★' : '';
    const scoreStr = s.arena?.score != null ? String(s.arena.score) : '-';
    console.log(`${col(cluster, 20)} ${col(s.id, 30)} ${scoreStr.padEnd(7)} ${winner}`);
  }
}
