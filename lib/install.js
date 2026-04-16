/**
 * install.js — resolve skill + fetch SKILL.md → .claude/skills/[id]/
 */

import { writeFile, mkdir, access } from 'node:fs/promises';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { fetchIndex } from './cache.js';
import { resolveSkill } from './search.js';

const BASE_RAW_URL = 'https://raw.githubusercontent.com/godlockin/ultraskills/main/';
const ALLOWED_PREFIXES = ['./community/', './devops/', './engineering/', './creative/'];

function prompt(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, ans => { rl.close(); resolve(ans.trim()); });
  });
}

async function fileExists(p) {
  try { await access(p); return true; } catch { return false; }
}

async function fetchSkillMd(path) {
  const url = BASE_RAW_URL + path.replace(/^\.\//, '');
  const res = await fetch(url, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`Failed to download ${path}. Check your connection.`);
  return res.text();
}

export async function installSkill(skillId, { yes = false, refresh = false } = {}) {
  const index = await fetchIndex({ refresh });
  const skills = index.skills ?? [];

  const matches = resolveSkill(skillId, skills);

  if (!matches.length) {
    console.error(`Skill "${skillId}" not found.`);
    console.error(`Try: npx ultraskills search ${skillId}`);
    process.exit(1);
  }

  let skill;
  if (matches.length === 1) {
    skill = matches[0];
  } else if (yes) {
    skill = matches[0];
    console.log(`Multiple matches — auto-selecting: ${skill.id}`);
  } else {
    console.log(`Multiple matches for "${skillId}":`);
    matches.forEach((s, i) => {
      const winner = s.arena?.is_winner ? ' ★' : '';
      console.log(`  ${i + 1}. ${s.id} (score: ${s.arena?.score ?? '?'}${winner}) — ${s.description?.slice(0, 60)}`);
    });
    const ans = await prompt(`Pick [1-${matches.length}] (default 1): `);
    const idx = parseInt(ans || '1', 10) - 1;
    skill = matches[Math.max(0, Math.min(idx, matches.length - 1))];
  }

  // Scope check
  const isAllowed = ALLOWED_PREFIXES.some(p => skill.path?.startsWith(p));
  if (!isAllowed) {
    console.error(`"${skill.id}" is an external skill — available in v2.`);
    process.exit(1);
  }

  // Conflict check
  const destDir = join(process.cwd(), '.claude', 'skills', skill.id);
  const destFile = join(destDir, 'SKILL.md');

  if (await fileExists(destFile)) {
    if (!yes) {
      const ans = await prompt(`${skill.id} already installed. Overwrite? [y/N] `);
      if (!ans.toLowerCase().startsWith('y')) {
        console.log('Skipped.');
        return;
      }
    }
  }

  // Fetch + write
  const content = await fetchSkillMd(skill.path);
  await mkdir(destDir, { recursive: true });
  await writeFile(destFile, content, 'utf8');

  console.log(`✓ Installed ${skill.id}. Restart Claude Code or run /skills reload to activate.`);
}
