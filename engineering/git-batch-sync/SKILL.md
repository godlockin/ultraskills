---
name: git-batch-sync
description: Batch-sync (fetch + pull + smart conflict resolve) all git repos under a directory tree. Forks also sync from upstream. Supports blacklist/allowlist filtering, tool migration hints, and one-click rust tool install. Use when user wants to update many git projects at once, sync all local clones, keep forks in sync with upstream, scan for outdated repos, fix merge conflicts across multiple repos, install fd/rg/eza/bat, or migrate from find/grep to rust equivalents. Triggers: "update all repos", "sync all git projects", "批量更新 git", "扫所有 git 项目", "修复所有冲突", "git pull across repos", "find all git repos", "sync fork upstream", "同步上游", "fork 同步", "install fd/rg", "migrate to fd", "黑名单 同步", "白名单 同步".
github_url: ""
github_hash: ""
version: 2.0.0
created_at: 2026-09-08T00:00:00Z
entry_point: SKILL.md
dependencies: [git, fd, ripgrep]
optional_dependencies: [eza, bat, delta, dust, tokei, hyperfine, just]
tags: [git, devops, batch, sync, fork, upstream, conflict-resolve, fd, ripgrep, rust-cli, allowlist, skiplist, tool-migration]
allowed_tools: [Bash, Read]
---

# git-batch-sync

## 🎯 Goal (目标)

Bulk-sync all git repositories under a directory tree in one command, with intelligent fork-upstream handling, blacklist/allowlist filtering, and automatic recovery from network failures. Designed for developers who keep ≥3 local clones (work projects, OSS forks, research code) and need to keep them all current without 200+ manual `git pull` invocations.

## 🧠 Core Concepts (核心理念)

### Why this exists

Three painful realities for anyone with many git repos:

1. **Reputation rot**: Repos you haven't touched in 6 months fall behind; rebasing 50 stale branches at once is miserable.
2. **Fork drift**: Forks diverge from upstream silently; tracking it manually is error-prone.
3. **Conflict whack-a-mole**: N repos means N×conflicts probability; lockfile conflicts are mechanical and should auto-resolve, but code conflicts must surface to humans.

### Design principles

- **Linear history by default**: `ff-only` first, `rebase --autostash` as fallback. Never create merge commits during bulk sync.
- **Lockfiles auto-resolve, code conflicts abort**: Lockfiles are regenerable from manifests; code needs judgment. See `INTERNALS.md` for rationale.
- **Fail fast on network, recover silently**: One proxy blip shouldn't block the whole batch — record and retry at the end.
- **Degrade gracefully**: Missing `fd`/`rg`/`bat`/etc. → fall back to POSIX equivalents, never fail.
- **No surprises**: `--push` is opt-in (rebase rewrites history). Code conflicts abort + report, never auto-merge.

## 🚀 Workflow (使用流程)

### Decision tree

```
Q1: Is this skill right for me?
├── ≥3 git repos under one directory → YES
└── 1-2 repos → use `git` directly

Q2: Just want to see what's outdated?
└── `git-batch-sync.sh --summary`

Q3: Need to also sync forks from upstream?
└── add `--sync-upstream`

Q4: Want to push back to origin after?
└── add `--push` (use with caution)

Q5: Need to exclude some repos (legacy, broken, internal)?
└── write a skiplist → `--skiplist=file`

Q6: Need to limit to a subset (work repos only)?
└── write an allowlist → `--allowlist=file`

Q7: Missing modern tools (fd/rg/bat)?
└── `git-batch-sync.sh --install-deps`

Q8: What got skipped/failed? Need help debugging?
└── see TROUBLESHOOTING.md
```

### Step-by-step

1. **Discover** — `--summary` to see all repos + their state (read-only, safe)
2. **Dry-run** — `--dry-run` to preview what would change
3. **Filter** — write skiplist/allowlist to scope the run
4. **Real run** — bare command, observe summary
5. **Recover** — read failed list from `/tmp/claude-tasks/git-batch-sync-failed-*.txt`, retry or fix manually

## ✅ Checklist (验证清单)

After any sync run, verify:

- [ ] Summary block shows `Updated: N` matching expected count
- [ ] `FetchFailed: 0` (or all `retry_failed` paths investigated)
- [ ] `Conflicts: 0` (or all conflicts auto-resolved lockfiles)
- [ ] No unexpected `Pushed: N` (only if `--push` was used)
- [ ] `Skiplist` excludes count matches your skiplist intent
- [ ] Failed repos list (if any) reviewed and either fixed or moved to skiplist

When reviewing changes:

- [ ] For each repo: `git log -1 origin/<branch>` shows expected recent commits
- [ ] For forks (with `--sync-upstream`): `git log -1 upstream/<branch>` is ancestor of local HEAD
- [ ] No accidental `git push --force` (this skill never does this)

---

# Detailed reference (below)

## When to use

| Trigger | Action |
|---|---|
| "扫所有 git 项目" / "find all git repos" | `--summary` mode |
| "批量更新 git" / "update all repos" | default update flow |
| "修复冲突" / "fix conflicts across repos" | run update + handle conflicts |
| "哪个 repo 落后了" / "outdated check" | `--summary` (shows behind count) |
| "fork 同步上游" / "sync fork upstream" / "同步上游" | add `--sync-upstream` |
| "把 fork 推到 origin" | add `--sync-upstream --push` |
| "fd vs find 真实速度" / benchmark | `--bench` |
| "扫了多少代码" / code stats | `--stats` |

## Fork handling

When `remote.upstream.url` is configured, the repo is treated as a fork. Output line shows:

```
[i/N] my-fork
  ⊟ fork upstream: https://github.com/original/repo.git
```

With `--sync-upstream`:
1. `git fetch upstream --prune --tags`
2. `git rebase upstream/<branch>` (preferred over merge — keeps history clean)
3. Auto-resolve lockfiles same as origin rebase; abort + report on code conflict
4. After upstream sync, refresh `ahead`/`behind` against `origin/<branch>`
5. Then run the normal origin pull flow

With `--push`:
- `git push origin <branch>` after successful update (works for both upstream-synced and direct pull flows)

Typical fork workflow:
```bash
# Sync fork with upstream + origin, then push
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream --push

# Just sync upstream locally, don't push
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream
```

## When NOT to use

- Single repo operations → use `git` directly (this skill is bulk)
- Submodule-only changes → use `git submodule update`
- Push / PR operations → not in scope (local sync only, except via `--push`)

## Blacklist & allowlist

### Blacklist (`--skiplist`)

Skip paths listed in the file. Supports prefix matching (e.g. `study/tigerobo` skips the whole subtree).

```bash
# ~/.gbs-skiplist:
study/tigerobo       # ← skip entire subtree
ikea                 # ← skip entire subtree
my_projects/old-x    # ← skip single repo
```

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code \
  --skiplist=/Users/chenchen/working/sourcecode/.git-batch-sync-skiplist
```

### Allowlist (`--allowlist`)

Whitelist: only sync listed paths. Applied **before** skiplist. Skiplist can further exclude from the allowed set.

```bash
# ~/work-repos.txt:
# Only sync these paths (and their subtrees)
my_projects
research/LLM
study/work-related
```

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code \
  --allowlist=~/work-repos.txt \
  --skiplist=~/.gbs-skiplist \
  --sync-upstream --push
```

### Precedence

1. `--allowlist` first (whitelist filter) — non-matching paths → `SKIPPED_BY_ALLOWLIST`
2. `--skiplist` second (blacklist filter) — matching paths → `SKIPPED_BY_LIST`
3. Final REPOS = allowlist ∩ ¬skiplist

Both empty → all repos synced.

## Tool dependency check & install

The skill detects fd / ripgrep / eza / bat / delta / dust / tokei / hyperfine / just on startup.

### Install missing

```bash
# 一键安装全部 (core + optional)
bash $SKILL_DIR/scripts/git-batch-sync.sh --install-deps

# 仅核心 (fd + ripgrep)
bash $SKILL_DIR/scripts/install-deps.sh --core-only

# 或 via justfile
just --justfile $SKILL_DIR/scripts/justfile install-deps
```

| Category | Tools | Required? |
|---|---|---|
| CORE | fd, ripgrep | Yes (degrade to find/grep, but 10-100x slower) |
| OPTIONAL | eza, bat, delta, dust, procs, hyperfine, tokei, just | No (UX/stats/bench) |

If `--install-deps` is run on macOS without brew, it errors with install instructions for Homebrew.

### Inspect current tools

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh --migrate-tools
```

Outputs a 3-column table: legacy tool, rust replacement, install status. See `references/tools-mapping.md` for full mapping.

## Tool migration (rust replacements)

The skill auto-replaces slow tools with rust equivalents:

| When user has... | Skill uses | Speed gain |
|---|---|---|
| `find` | `fd` (via fd --type=dir --hidden --no-ignore --glob '.git') | 10-30x |
| `grep` | `rg` (conflict pattern detection) | 10-100x |
| `cat` | `bat` (log display) | UX |
| `ls` | `eza` (when listing dirs) | UX |
| `diff` | `delta` (rebase diffs) | UX |
| `du -sh` | `dust` (tree summary) | UX |
| `time` | `hyperfine` (when --bench) | UX |
| `wc -l` | `tokei` (when --stats) | UX |
| `make` | `just` (recipe runner) | UX |

When a tool is missing, the skill degrades gracefully and prints `brew install X` hint. Full table in `references/tools-mapping.md`.

## Quick start

```bash
# 1. Summary: list all repos and their state (read-only, safe)
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/working/sourcecode --summary

# 2. Dry-run: see what would happen, no changes
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/working/sourcecode --dry-run

# 3. Real run
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/working/sourcecode

# Or via justfile
cd ~/working/sourcecode
just --justfile $SKILL_DIR/scripts/justfile summary
just --justfile $SKILL_DIR/scripts/justfile update
```

## Command reference

| Flag | Effect |
|---|---|
| `--summary` | Read-only scan, list dirty/ahead/behind per repo |
| `--dry-run` | Show what would happen, no fetch/pull |
| `--no-fetch` | Skip fetch (use cached remote refs) |
| `--sync-upstream` | For forks: fetch + rebase `upstream/<branch>` before origin pull |
| `--push` | After update, `git push origin <branch>` |
| `--skiplist=<file>` | Blacklist: skip these paths (prefix match) |
| `--allowlist=<file>` | Whitelist: only sync these paths |
| `--install-deps` | Install fd/rg/eza/bat/delta/dust/tokei/hyperfine/just via brew |
| `--migrate-tools` | Show legacy tool vs rust replacement table |
| `--stats` | After scan, run `tokei` for LOC summary |
| `--bench` | After scan, run `hyperfine` fd-vs-find |
| `--max-depth=N` | Limit scan depth (default 8) |
| `--root=PATH` | Override scan root |
| `-h`, `--help` | Show full help |

Exit codes: `0` = all OK/updated, `1` = errors or conflicts unresolved, `2` = no repos found.

## Conflict resolution policy

| File pattern | Strategy |
|---|---|
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | `--theirs` (auto-regen from new package.json) |
| `Cargo.lock`, `poetry.lock`, `composer.lock`, `Gemfile.lock`, `go.sum` | `--theirs` |
| `*.min.js`, `*.min.css`, `dist/*`, `build/*` | `--theirs` (generated) |
| `.DS_Store`, `.idea/*`, `.vscode/*` | `--theirs` (tooling) |
| **Everything else** | rebase **abort**, list for manual fix |

Code conflicts are NEVER auto-merged. The script rebase-aborts and prints the file list so you can `cd` into the repo and resolve manually.

## Tooling

| Tool | Role | Fallback |
|---|---|---|
| `fd` | scan `.git` dirs | `find` with explicit exclusions |
| `rg` (ripgrep) | conflict pattern detection | `grep -qiE` |
| `eza` | optional dir visualization | `ls` |
| `bat` | optional log/cat | `cat` |
| `delta` | optional diff highlighting | inline ANSI |
| `dust` | optional tree summary | `du -sh` |
| `tokei` | optional LOC stats | skip if missing |
| `hyperfine` | optional fd-vs-find benchmark | skip if missing |
| `just` | optional recipe runner | use `bash` directly |

All optional tools degrade gracefully — script prints `tool missing → brew install X` and continues.

## Output

Each repo gets a status line:
- `[i/TOTAL] repo-name`
  - `✓ up-to-date` (green)
  - `✓ fast-forwarded` (green)
  - `↻ rebased` (green)
  - `⚠ CONFLICT` (yellow) + auto/manual breakdown
  - `✗ error` (red)
  - `— skip` (detached HEAD / no upstream)

Final summary block:
```
Total          : 50
Forks          : 3 (synced=2)
Up-to-date     : 32
Updated        : 15
Pushed         : 8
Dirty          : 3
Conflicts      : 0
Skipped        : 0
Errors         : 0
Elapsed        : 47s
Log            : /tmp/claude-tasks/git-batch-sync-20260908-233715.log
```

## Risks & limits

- **Code conflicts auto-abort** rebase, never auto-merge — by design
- **Dirty state stash** then pop — if pop conflicts, run `git stash list` to recover
- **No push** — this skill is pull-side only
- **Slow on huge trees** — use `--max-depth=5` for ≥1000 repos
- **Default scan excludes** `node_modules` `.venv` `vendor` `target` `.gradle` `__pycache__` to avoid crawling build dirs
- **Log always written** to `/tmp/claude-tasks/git-batch-sync-*.log` even on tty

## Performance notes

With `fd`, scanning 50 repos takes ~0.05s vs ~0.5s with `find` (10x). Conflict detection with `rg` is 10-100x faster than `grep -r`. Run `--bench` to see live numbers on your machine.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | This file |
| `scripts/git-batch-sync.sh` | Main script (bash 3.2 compat, ~420 lines) |
| `scripts/install-deps.sh` | One-click brew installer for rust tools |
| `scripts/justfile` | just recipes (12+ commands) |
| `references/tools-mapping.md` | POSIX → rust tool replacement table |
| `examples/example-1-summary.md` | Read-only scan workflow |
| `examples/example-2-conflict.md` | Conflict handling walkthrough |
| `examples/example-3-fork-upstream.md` | Fork sync with `--sync-upstream --push` |
| `examples/example-4-bench.md` | Benchmark + stats workflow |

## Post-install

The skill is local — no deployment step. To use globally:

```bash
# Add to PATH or alias
echo 'alias gbs="bash ~/.claude/skills/git-batch-sync/scripts/git-batch-sync.sh"' >> ~/.zshrc
source ~/.zshrc
gbs ~/working/sourcecode --summary
```

Or copy `scripts/justfile` to your source dir and use `just` directly.
