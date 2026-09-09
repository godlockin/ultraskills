# Internals

This document captures **why** the script makes the choices it does — the design rationale that isn't obvious from reading the code.

## Table of contents

1. [Why bash 3.2 (not bash 4+ / python / go)](#why-bash-32)
2. [Why rebase --autostash (not merge)](#why-rebase)
3. [Why lockfiles auto-resolve with --theirs](#why-lockfiles)
4. [Why allowlist before skiplist](#why-allowlist-first)
5. [Why fd (not find), rg (not grep)](#why-fd-rg)
6. [Why skip detect when fetch fails silently](#why-fetch-fail-detection)
7. [Why single retry pass (not exponential backoff)](#why-single-retry)
8. [Why no auto-push by default](#why-no-auto-push)

## <a id="why-bash-32"></a>Why bash 3.2 (not bash 4+ / python / go)

**Choice**: Stay bash 3.2 compatible.

**Why**:
- macOS ships `/bin/bash` 3.2 as default (licensing — Apple won't ship GPL v3)
- Bash 4+ features (`mapfile`, associative arrays, `declare -g`) require `brew install bash` and PATH override
- Python would need venv + shebang + arg parsing + install ceremony
- Go would need compilation, releases for 3 OSes, dependency mgmt

**Trade-off accepted**: Live with bash 3.2 quirks:
- No `mapfile` → use `while-read` loops
- No associative arrays → use parallel indexed arrays
- `set -u` + empty array `${ARR[@]}` triggers unbound → use `set -o pipefail` instead
- Limited regex in `case` → use bash glob patterns or `[[ =~ ]]`

**Escape hatch**: When bash 3.2 becomes truly limiting (e.g., need for JSON / YAML parsing), split out a `lib.sh` companion or migrate to python.

## <a id="why-rebase"></a>Why rebase --autostash (not merge)

**Choice**: `git pull --ff-only` first; on failure, `git pull --rebase --autostash`.

**Why**:
- **ff-only first**: Fast-forward is the safe, no-history-rewrite option. Try it always.
- **rebase over merge**: Linear history is easier to read + bisect + revert. Avoids `Merge branch 'main' of ...` noise.
- **--autostash**: Auto-stashes uncommitted changes, reapplies after rebase. Cleaner than manual stash/pop for dirty worktrees.

**Why NOT merge**:
- Merge creates merge commits → noisy history
- For local sync, there's no semantic benefit — the remote already has the linear history
- Merge conflicts are identical to rebase conflicts (no easier)

**Why NOT just rebase**: ff-only is a strict subset and a strict improvement when possible. Always try it first.

## <a id="why-lockfiles"></a>Why lockfiles auto-resolve with `--theirs`

**Choice**: Auto-resolve `package-lock.json`, `yarn.lock`, `Cargo.lock`, `go.sum`, etc. with `--theirs`.

**Why**: Lockfiles are **deterministically regenerated** from `package.json` / `Cargo.toml`. When sync conflicts on lockfile, the local one is **stale** (since the manifest has new deps). Keeping local lockfile means:
- `cargo build` may fail with "lockfile out of sync"
- `npm ci` may refuse to install
- User has to manually `rm` and regenerate

**Strategy**: Take the remote lockfile (which is consistent with remote manifest), then on next `cargo build` / `npm install`, the tool will re-resolve if needed.

**Why NOT auto-resolve all conflicts**: Code conflicts need human judgment — two divergent implementations can't be merged by heuristic. Lockfiles are special because they're regenerable.

**Edge cases**:
- If user has hand-edited lockfile (rare, but possible for `npm shrinkwrap`), `--theirs` will lose that edit
- Workaround: add the lockfile to skiplist OR remove it from `AUTORESOLVE_PATTERNS[]` in script

## <a id="why-allowlist-first"></a>Why allowlist before skiplist

**Choice**: Filter order is `allowlist` → `skiplist` → repos.

**Why**:
- **Allowlist is a positive constraint**: "Sync only these"
- **Skiplist is a negative constraint**: "Skip these"
- In boolean logic: `final = allowlist ∧ ¬skiplist`
- If skiplist applied first, allowlist couldn't "rescue" a repo that skiplist blocked
- Most users compose: "sync my work projects, except legacy ones" → allowlist=work, skiplist=legacy

**Example**:
```
allowlist:    research/LLM
skiplist:     research/LLM/deprecated

Result:       research/LLM/{transformers,OpenBB}   ✓ synced
              research/LLM/deprecated              ✗ skipped
```

If skiplist applied first (rejected deprecated), then allowlist (kept research/LLM/*), we'd skip deprecated anyway — but the *intent* differs:
- "Sync all of research, except deprecated" → both filters agree
- "Sync only LLM, even if it appears in skiplist" → allowlist should win

We chose the latter semantics because allowlist is more specific.

## <a id="why-fd-rg"></a>Why fd (not find), rg (not grep)

**Choice**: `fd` for file discovery, `rg` for content search.

**Why**:
- **fd**: 10-30x faster (multi-threaded, Rust), respects `.gitignore` by default, simpler flags
- **rg**: 10-100x faster, auto-skips binary, respects `.gitignore`
- **Auto-degrade**: If missing, fallback to `find` / `grep` so script never breaks

**Trade-off**: Users without `fd` / `rg` see slower scans (especially on >100 repos). `install-deps.sh` solves this.

**Bench numbers** (on user's `/Users/chenchen/working/sourcecode`):

| Operation | fd | find | Speedup |
|---|---|---|---|
| Discover 253 `.git` dirs | 51ms | 587ms | 11.5x |
| Detect rebase conflict in 1000-line output | 3ms | 280ms | 93x |

(See `examples/example-4-bench.md` for full benchmark.)

## <a id="why-fetch-fail-detection"></a>Why skip detect when fetch fails silently

**Choice**: When `git fetch` fails (network, DNS, auth), script logs `↪ fetch failed → retry queue` and continues, instead of crashing.

**Why**:
- **One bad repo shouldn't block the whole batch**
- 50/253 repos failing means 203 should still update
- Without detection, `git fetch` failure → exit code 1 → `git pull --ff-only` thinks "no new commits" → silently marks as up-to-date (WRONG!)

**Bug it prevents**: Original v1.0 printed "up-to-date" for repos that never successfully fetched. User thought they were clean; they weren't.

**Detection pattern**: grep fetch output for `Connection closed | Could not read | fatal: unable to access | Could not resolve | Connection reset | timed out`.

## <a id="why-single-retry"></a>Why single retry pass (not exponential backoff)

**Choice**: At end of main loop, retry failed-fetches exactly once with `sleep 1` between.

**Why**:
- **Most fetch failures are transient** (proxy reconnect, DNS cache, rate limit)
- One retry after the rest of the batch succeeds catches most
- Exponential backoff (1s, 2s, 4s, 8s) would take 15s × N failed = minutes wasted on permanent failures
- For *permanent* failures (auth, dead repo), no amount of retry helps

**Trade-off**: We don't catch intermittent failures that take >1s to recover. Acceptable because:
- True network outage would fail all fetches, retry also fails → no harm done
- Transient blip recovers quickly with sleep 1

**Future**: Add `--retry-attempts=N` and `--retry-delay=S` flags if needed.

## <a id="why-no-auto-push"></a>Why no auto-push by default

**Choice**: `--push` is opt-in.

**Why**:
- **Push is destructive**: Cannot be undone (well, can be reverted, but creates noise)
- **One wrong push affects origin**, not just local
- **CI/CD pipelines often push from specific machines**, not bulk tools
- **Fork rebase can rewrite local commits** → pushing rewrites history on origin, breaking anyone else tracking the fork

**When `--push` makes sense**:
- After rebase, you want fork's main to match upstream's main
- Solo fork where you're the only contributor
- CI maintenance job

**Why not default-on**: Most users want to *review* the local state before pushing. Auto-push violates "Fail Fast, Ask First" principle.

## Future design ideas

These were considered and deferred:

| Idea | Reason deferred |
|---|---|
| Parallel fetch | Network bottleneck (most connections single-threaded anyway); race conditions on shared `~/.gitconfig` |
| Cache state in SQLite | Premature — text log is enough for now |
| Auto-detect CI environment | Adds complexity; explicit `--push` is clearer |
| Plugin system for custom heuristics | Premature; `AUTORESOLVE_PATTERNS[]` array is editable in source |
| Replace bash with python | Cross-platform benefit, but lose zero-dep install; revisit at v3 |
| Web UI for status | UI is the terminal; `--summary` is already readable |
