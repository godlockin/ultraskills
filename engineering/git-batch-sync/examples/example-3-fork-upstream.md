# Example 3 — Fork sync with upstream + push

Forks have an `upstream` remote. Use `--sync-upstream` to pull from upstream first, then optionally `--push` to update origin.

## Setup

```bash
# Once: add upstream to a fork
cd ~/code/fork-of-lib
git remote add upstream https://github.com/original/lib.git
git fetch upstream
```

The skill auto-detects forks via `git config --get remote.upstream.url`.

## Command

```bash
# Full fork sync: upstream → rebase → origin pull → push
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream --push

# Or via justfile
just --justfile $SKILL_DIR/scripts/justfile sync-fork-push
```

## Output (one fork repo)

```
[3/42] my_projects/fork-of-lib
  ⊟ fork upstream: https://github.com/original/lib.git
  branch=main ahead=0 behind=12
  upstream/main ahead by 8
  ✓ upstream rebased                       ← rebase upstream/main
  post-upstream: ahead=8 behind=0
  ✓ fast-forwarded                         ← ff from origin/main (now also includes upstream)
  ✓ pushed → origin/main                   ← push back
```

## What happens step by step

1. Detect fork (remote.upstream.url exists) → mark `⊟ fork`
2. `git fetch origin --prune --tags` (refresh origin refs)
3. `git fetch upstream --prune --tags` (refresh upstream refs)
4. `git rebase upstream/<branch>` (preferred over merge — keeps history clean)
5. If rebase conflict on lockfiles → autoresolve; on code → abort + report
6. Refresh ahead/behind against origin
7. Run normal `git pull --ff-only` flow
8. If `--push`: `git push origin <branch>`

## Variants

```bash
# Just sync upstream, don't touch origin or push
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream

# Sync everything but no push
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream

# Dry-run first to verify what will happen
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream --push --dry-run
```

## When `--push` is useful

- After rebase, you want your fork's main to reflect upstream's main
- Useful in CI/maintenance workflows where you want forks to track automatically
- Not useful if you've made local commits you don't want on origin yet (use `--push` only after review)

## Risk

- `--push` does plain `git push origin <branch>` — non-fast-forward push will fail (no force)
- For rebased pushes to work, your local must be a descendant of origin's tip
- If origin has commits you don't have, the script will pull-then-push flow handles it; if pull fails, push is skipped (and you'll see `push failed`)
