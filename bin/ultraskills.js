#!/usr/bin/env node
/**
 * ultraskills — CLI entry point
 * Node 18+ required
 */

import { fetchIndex } from '../lib/cache.js';
import { installSkill } from '../lib/install.js';
import { listSkills } from '../lib/list.js';
import { infoSkill } from '../lib/info.js';
import { searchSkills } from '../lib/search.js';
import { updateSkills } from '../lib/update.js';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf8'));

const USAGE = `
ultraskills v${pkg.version}

Usage:
  npx ultraskills install <skill-id>   Install best-scored skill
  npx ultraskills search <query>       Search skills by keyword
  npx ultraskills list [category]      List all skills (optionally filtered)
  npx ultraskills update               Re-fetch index + update installed skills
  npx ultraskills info <skill-id>      Show skill detail

Global flags:
  --refresh    Force re-fetch index (bypass 24hr cache)
  --yes, -y    Non-interactive (auto-confirm prompts)
  --version    Show version
  --help, -h   Show this help
`.trim();

const args = process.argv.slice(2);

// Parse global flags
const refresh = args.includes('--refresh');
const yes = args.includes('--yes') || args.includes('-y');
const filtered = args.filter(a => !['--refresh', '--yes', '-y'].includes(a));

const [cmd, ...rest] = filtered;

if (!cmd || cmd === '--help' || cmd === '-h') {
  console.log(USAGE);
  process.exit(0);
}

if (cmd === '--version' || cmd === '-v') {
  console.log(pkg.version);
  process.exit(0);
}

async function main() {
  switch (cmd) {
    case 'install': {
      const skillId = rest[0];
      if (!skillId) { console.error('Usage: ultraskills install <skill-id>'); process.exit(1); }
      await installSkill(skillId, { yes, refresh });
      break;
    }
    case 'search': {
      const query = rest.join(' ');
      if (!query) { console.error('Usage: ultraskills search <query>'); process.exit(1); }
      const index = await fetchIndex({ refresh });
      const results = searchSkills(query, index.skills ?? []);
      if (!results.length) { console.log(`No results for "${query}".`); break; }
      results.forEach(s => {
        const winner = s.arena?.is_winner ? ' ★' : '';
        console.log(`${s.id.padEnd(35)} score:${String(s.arena?.score ?? '-').padEnd(6)} ${s.description?.slice(0, 55) ?? ''}${winner}`);
      });
      break;
    }
    case 'list': {
      const category = rest[0] ?? '';
      const index = await fetchIndex({ refresh });
      listSkills(category, index.skills ?? []);
      break;
    }
    case 'update': {
      await updateSkills({ yes });
      break;
    }
    case 'info': {
      const skillId = rest[0];
      if (!skillId) { console.error('Usage: ultraskills info <skill-id>'); process.exit(1); }
      const index = await fetchIndex({ refresh });
      infoSkill(skillId, index.skills ?? []);
      break;
    }
    default:
      console.error(`Unknown command: ${cmd}\n`);
      console.error(USAGE);
      process.exit(1);
  }
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
