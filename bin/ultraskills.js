#!/usr/bin/env node
// @ts-check
/**
 * ultraskills — CLI entry point
 * Lazy-loads index only for commands that need it.
 * Node 18+ required; zero external deps.
 */

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {{ version: string }} */
const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf8'));

const USAGE = `
ultraskills v${pkg.version}

Usage:
  npx ultraskills install <skill-id>   Install skill by id or keyword
  npx ultraskills search <query>       Search skills by keyword
  npx ultraskills list [category]      List all skills (optionally filtered)
  npx ultraskills update               Re-fetch index + update installed skills
  npx ultraskills uninstall <skill-id> Remove installed skill
  npx ultraskills info <skill-id>      Show skill detail

Global flags:
  --refresh    Force re-fetch index (bypass 24hr cache)
  --yes, -y    Non-interactive (auto-confirm prompts)
  --version    Show version
  --help, -h   Show this help
`.trim();

// ── Parse argv FIRST, before any dynamic imports ────────────────────────────
const args = process.argv.slice(2);
const refresh = args.includes('--refresh');
const yes = args.includes('--yes') || args.includes('-y');
const filtered = args.filter(a => !['--refresh', '--yes', '-y'].includes(a));
const [cmd, ...rest] = filtered;

// ── Short-circuit: no index needed ──────────────────────────────────────────
if (!cmd || cmd === '--help' || cmd === '-h') {
  console.log(USAGE);
  process.exit(0);
}

if (cmd === '--version' || cmd === '-v') {
  console.log(pkg.version);
  process.exit(0);
}

// ── Lazy loader — only called by commands that need index ───────────────────
/** @returns {Promise<import('../lib/cache.js').SkillIndex>} */
async function loadIndex() {
  const { fetchIndex } = await import('../lib/cache.js');
  return fetchIndex({ refresh });
}

// ── Command router ───────────────────────────────────────────────────────────
async function main() {
  switch (cmd) {
    case 'install': {
      const query = rest.join(' ').trim();
      if (!query) { console.error('Usage: ultraskills install <skill-id>'); process.exit(1); }
      const { install } = await import('../lib/install.js');
      const index = await loadIndex();
      await install(query, index, process.cwd(), { yes });
      break;
    }

    case 'search': {
      const query = rest.join(' ').trim();
      if (!query) { console.error('Usage: ultraskills search <query>'); process.exit(1); }
      const { searchSkills } = await import('../lib/search.js');
      const index = await loadIndex();
      const results = searchSkills(query, index.skills ?? []);
      if (!results.length) { console.log(`No results for "${query}".`); break; }
      results.forEach(s => {
        const winner = s.arena?.is_winner ? ' ★' : '';
        const score = String(s.arena?.score ?? '-').padEnd(4);
        console.log(`${s.id.padEnd(40)} score:${score}  ${(s.description ?? '').slice(0, 55)}${winner}`);
      });
      break;
    }

    case 'list': {
      const category = rest[0] ?? '';
      const { listSkills } = await import('../lib/list.js');
      const index = await loadIndex();
      listSkills(category, index.skills ?? []);
      break;
    }

    case 'update': {
      const { updateCommand } = await import('../lib/update.js');
      await updateCommand(process.cwd(), { yes });
      break;
    }

    case 'uninstall': {
      const skillId = rest[0];
      if (!skillId) { console.error('Usage: ultraskills uninstall <skill-id>'); process.exit(1); }
      const { uninstall } = await import('../lib/uninstall.js');
      await uninstall(skillId, process.cwd(), { yes });
      break;
    }

    case 'info': {
      const skillId = rest[0];
      if (!skillId) { console.error('Usage: ultraskills info <skill-id>'); process.exit(1); }
      const { info } = await import('../lib/info.js');
      const index = await loadIndex();
      info(skillId, index);
      break;
    }

    default:
      console.error(`Unknown command: ${cmd}\n`);
      console.error(USAGE);
      process.exit(1);
  }
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
