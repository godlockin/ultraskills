# Troubleshooting

Common issues and how to fix them.

## Table of contents

- [fetch fails with "Connection closed by 127.0.0.1 port 7890"](#proxy)
- [fetch fails with "Could not read from remote repository"](#auth)
- [fetch fails with "Could not resolve host"](#dns)
- ["up-to-date" reported but repo is actually behind](#silent-fail)
- [rebase conflict, code conflict, abort — what now?](#rebase-abort)
- [Dirty worktree blocks rebase](#dirty)
- [Detached HEAD, skipped](#detached)
- [Push rejected after successful update](#push-rejected)
- [Too slow on huge trees](#slow)
- [All repos show "up-to-date" but I just pushed](#stale-refs)
- [Script says "no git repos under $ROOT"](#no-repos)
- ["Permission denied" when running the script](#permission)
- [macOS bash 3.2 errors](#bash32)
- [Submodule changes don't propagate](#submodule)
- [Mono-repo / lerna / pnpm workspace — should I use this?](#monorepo)

## <a id="proxy"></a>`Connection closed by 127.0.0.1 port 7890`

**Cause**: System has HTTP proxy (Clash / Surge / V2RayN) configured but proxy process is down or not accepting connections.

**Fix**:
```bash
# 1. Verify proxy is alive
nc -zv 127.0.0.1 7890
# or
curl -x http://127.0.0.1:7890 https://github.com -I

# 2a. If proxy should work — restart it
# (Clash: pkill clash && open -a Clash)
# (Surge: System Preferences → Network → toggle off/on)
# (V2RayN: tray icon → restart)

# 2b. If you want to bypass proxy temporarily
git config --global --unset http.proxy
git config --global --unset https.proxy
bash git-batch-sync.sh ~/code

# 3. Re-run after fix
bash git-batch-sync.sh ~/code
```

The script auto-records these in retry queue. After fixing proxy, re-run to retry.

## <a id="auth"></a>`Could not read from remote repository`

**Cause**: SSH key missing, HTTPS credential missing, or remote is private without access.

**Fix**:
```bash
# Test single repo
cd /path/to/repo
git fetch origin
# Read the actual error message

# SSH: check key is loaded
ssh-add -l
# If empty:
ssh-add ~/.ssh/id_ed25519

# HTTPS: cache credential
git config --global credential.helper osxkeychain  # macOS
git config --global credential.helper cache          # Linux

# Or check if repo still exists
git ls-remote origin HEAD
```

## <a id="dns"></a>`Could not resolve host github.com`

**Cause**: DNS issue, network down, or VPN interfering.

**Fix**:
```bash
# Test DNS
nslookup github.com
# or
dig github.com

# If broken: try public DNS
sudo dscacheutil -flushcache  # macOS flush
# Add 1.1.1.1 / 8.8.8.8 in System Preferences → Network → DNS

# Test connectivity
curl -I https://github.com
```

## <a id="silent-fail"></a>"up-to-date" reported but repo is actually behind

**Cause**: `git fetch` failed silently (network blip), then `rev-list HEAD..upstream` returned 0 commits.

**Fixed in v2.0.0**: Script now detects fetch failure patterns and queues retry. If you see `⚠ fetch failed → retry queue`, the repo is NOT marked as up-to-date.

If on v1.x, upgrade or check manually:
```bash
cd /path/to/repo
git fetch origin
git status -sb  # shows ahead/behind with arrow
```

## <a id="rebase-abort"></a>Rebase aborted, code conflict — what now?

**Cause**: Same line in your local commit and incoming commit, both changed differently. Cannot auto-merge.

**Fix**:
```bash
# The script already did:
# 1. Listed conflicting files
# 2. Ran `git rebase --abort`
# 3. Showed file list in output
#
# To resolve manually:
cd /path/to/repo
git status  # see current state
# Three options:
#   a) Rebase again, resolve manually:
git rebase origin/main  # or upstream/main
# Edit files to resolve <<<<<<< markers
git add <resolved-files>
git rebase --continue

#   b) Reset and merge instead:
git fetch origin
git merge origin/main  # creates merge commit
# Resolve in editor, git commit

#   c) Skip the conflicting commit (if it's not yours):
git rebase --skip  # only if you're sure the commit is no longer needed
```

## <a id="dirty"></a>Dirty worktree blocks rebase

**Cause**: Uncommitted changes (`git status` shows files).

**Fix**: Script auto-stashes. If `stash pop` conflicts:
```bash
cd /path/to/repo
git stash list  # find the stash
git stash show stash@{0}  # see what was stashed
# Manually merge:
git stash pop  # or git stash apply then resolve
```

To prevent: commit or stash before running the skill.

## <a id="detached"></a>`— detached HEAD, skip`

**Cause**: HEAD points to a commit, not a branch.

**Fix**:
```bash
cd /path/to/repo
git status  # should say "HEAD detached at <commit>"
# Get back to a branch:
git checkout main  # or master
# Or create branch from current state:
git switch -c my-experiment
```

## <a id="push-rejected"></a>`push rejected (non-fast-forward)`

**Cause**: Origin has commits you don't have locally.

**Fix**:
```bash
cd /path/to/repo
git fetch origin
# See what's blocking:
git log --oneline HEAD..origin/main
# Option A: pull then push (may merge)
git pull --rebase origin main
git push origin main
# Option B: force-push (DANGEROUS — overwrites remote history)
git push --force-with-lease origin main  # safer than --force
```

The skill's `--push` does plain `git push` (no force), so rejected state is recoverable.

## <a id="slow"></a>Too slow on huge trees (>1000 repos)

**Cause**: `fd` / `rg` not installed → falling back to `find` / `grep`.

**Fix**:
```bash
bash git-batch-sync.sh --install-deps  # installs fd + rg
```

Other options:
- Increase depth: `--max-depth=5` (skip deep-nested)
- Use skiplist for repos you know are slow: `--skiplist=huge-mono.txt`
- Use allowlist to scope: `--allowlist=urgent.txt`

## <a id="stale-refs"></a>All repos "up-to-date" but I just pushed

**Cause**: `--no-fetch` was passed, using cached refs.

**Fix**: Re-run without `--no-fetch`:
```bash
bash git-batch-sync.sh ~/code  # default: fetches
```

## <a id="no-repos"></a>`no git repos under $ROOT (after filters)`

**Cause**: Filters (allowlist + skiplist) exclude everything.

**Fix**:
```bash
# 1. Check ROOT is correct
ls $ROOT/.git  # should be a directory

# 2. Without filters, count repos
bash git-batch-sync.sh --summary
# Should show "Repos found: N"

# 3. Then add filters one at a time
bash git-batch-sync.sh --summary --skiplist=mine.txt
bash git-batch-sync.sh --summary --allowlist=mine.txt
```

Common mistake: ROOT is a single repo's parent (e.g. `~/code/myrepo`), but `--allowlist` lists siblings — won't match.

## <a id="permission"></a>`Permission denied`

**Cause**: Script not executable.

**Fix**:
```bash
chmod +x scripts/git-batch-sync.sh
# Or run via bash:
bash scripts/git-batch-sync.sh ~/code
```

## <a id="bash32"></a>macOS bash 3.2 errors

**Symptom**: `A[@]: unbound variable` or `mapfile: command not found`.

**Fix**: Already handled in v2.0.0 (uses `while-read`, `set -o pipefail`). If you see these errors, you're on v1.x — upgrade.

To verify your version:
```bash
bash --version
# GNU bash, version 3.2.57 → macOS default
# GNU bash, version 5.x → via brew install bash
```

If on Linux with bash 5+, the script works but ignores some compatibility shims.

## <a id="submodule"></a>Submodule changes don't propagate

**Cause**: Submodules are nested repos with their own refs.

**Fix**:
```bash
# Sync submodules explicitly
git submodule update --init --recursive

# Or use the dedicated tool (not this skill):
bash git-batch-sync.sh ~/code
# Then in each repo:
git submodule update --remote
```

This skill does NOT recurse into submodules. Use `git submodule` for that.

## <a id="monorepo"></a>Mono-repo / lerna / pnpm workspace — should I use this?

**Answer**: Probably not.

This skill treats each `.git/` as a unit. A monorepo is ONE repo with many packages. Just `git pull` inside it.

**Use this skill if**: you have ≥3 separate git repos in a directory tree.
**Don't use if**: you have 1 big repo with packages/, services/, apps/ subdirs.

If unsure:
```bash
find ~/code -maxdepth 3 -name '.git' -type d | wc -l
# < 3 → don't need this skill
# ≥ 3 → yes
```
