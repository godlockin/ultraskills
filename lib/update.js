/**
 * update.js — re-fetch index + re-download all installed skills
 */
import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { fetchIndex } from './cache.js';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';

export async function updateSkills({ yes = false } = {}) {
  console.log('Refreshing index...');
  const index = await fetchIndex({ refresh: true });
  const skills = index.skills ?? [];
  const skillMap = Object.fromEntries(skills.map(s => [s.id, s]));

  const skillsDir = join(process.cwd(), '.claude', 'skills');
  let entries;
  try {
    entries = await readdir(skillsDir, { withFileTypes: true });
  } catch {
    console.log('No installed skills found (.claude/skills/ does not exist).');
    return;
  }

  const installed = entries.filter(e => e.isDirectory()).map(e => e.name);
  if (!installed.length) { console.log('No installed skills to update.'); return; }

  let updated = 0, skipped = 0;
  for (const id of installed) {
    if (!skillMap[id]) {
      console.warn(`  ⚠ skill "${id}" not found in current index, skipping.`);
      skipped++;
      continue;
    }
    const skill = skillMap[id];
    try {
      const url = BASE_RAW_URL + skill.path.replace(/^\.\//, '');
      const res = await fetch(url, { signal: AbortSignal.timeout(10000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const content = await res.text();
      const destDir = join(skillsDir, id);
      await mkdir(destDir, { recursive: true });
      await writeFile(join(destDir, 'SKILL.md'), content, 'utf8');
      console.log(`  ✓ ${id}`);
      updated++;
    } catch (err) {
      console.error(`  ✗ ${id}: ${err.message}`);
    }
  }
  console.log(`\nDone. Updated: ${updated}, skipped: ${skipped}.`);
}
