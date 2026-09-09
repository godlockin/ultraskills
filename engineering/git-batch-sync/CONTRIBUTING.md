# Contributing to git-batch-sync

Thank you for your interest in contributing! This document explains how to set up the dev environment, run tests, and submit changes that meet S-Tier standards.

## Table of contents

- [Code of conduct](#code-of-conduct)
- [What to contribute](#what-to-contribute)
- [Dev setup](#dev-setup)
- [Test strategy](#test-strategy)
- [Style guide](#style-guide)
- [Submitting changes](#submitting-changes)
- [Release process](#release-process)

## Code of conduct

Be respectful. Disagree on ideas, not people. Assume good faith. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) (informally).

## What to contribute

| Type | Examples | Difficulty |
|---|---|---|
| Bug fix | `bash 3.2 compat`, edge cases in filter logic | Easy |
| Doc | Clarify, add example, fix typo | Easy |
| Tool addition | New rust tool integration (e.g., `ouch`, `zellij`) | Medium |
| New flag | New behavior on top of existing flow | Medium |
| Architecture | Replace bash with python, add caching, parallelize | Hard |
| New conflict heuristic | Safer pattern matching, user-configurable patterns | Hard |

Before opening a large PR, open an issue describing what + why.

## Dev setup

```bash
# Clone (when this becomes its own repo)
git clone https://github.com/chenchen/git-batch-sync
cd git-batch-sync
ln -s . scripts/git-batch-sync.sh  # optional

# Install runtime deps (macOS)
brew install fd ripgrep eza bat delta dust tokei hyperfine just

# Install runtime deps (Linux)
# Most are in apt: fd-find, ripgrep
# Some need snap/manual: eza (snap), bat (apt), delta (cargo install), hyperfine (cargo install)

# Smoke test
bash scripts/git-batch-sync.sh --help
bash scripts/git-batch-sync.sh --migrate-tools
bash scripts/git-batch-sync.sh --summary --root=/tmp/nonexistent  # should exit 2
```

## Test strategy

See [`TESTING.md`](TESTING.md) for full details. Quick start:

```bash
# Unit / structural tests (fast, < 5s)
bash tests/test-syntax.sh           # bash -n every script
bash tests/test-help-flag.sh       # --help exits 0
bash tests/test-install-deps.sh    # dry-run install-deps mode
bash tests/test-allowlist.sh       # allowlist filter logic
bash tests/test-skiplist.sh        # skiplist filter logic
bash tests/test-fallback.sh        # fd missing → find fallback

# Integration tests (slow, 30s-5min)
bash tests/integration/test-real-repo.sh     # create temp repos, simulate pull
bash tests/integration/test-conflict.sh     # force conflict, verify autoresolve
bash tests/integration/test-fork.sh         # mock upstream remote, test rebase
bash tests/integration/test-retry.sh        # mock network failure, test retry pass

# Or all at once
bash tests/run-all.sh
```

Tests must pass before merge.

## Style guide

### Bash

- **bash 3.2 compatible** (macOS default `/bin/bash` is 3.2; no `mapfile`, no `declare -g`, no associative arrays)
- Use `set -o pipefail` (NOT `set -u` — incompatible with empty array `${ARR[@]}`)
- Use `[[ ]]` for tests, `[ ]` for POSIX
- Quote all variables: `"$var"` not `$var`
- Arrays: append with `+=`, iterate with `for x in "${arr[@]}"` (guarded with `${#arr[@]}` first if relying on emptiness)
- Indent: 2 spaces
- Function names: `snake_case`
- Constants: `UPPER_SNAKE_CASE` at top of file
- Use `command -v` not `which`

### Markdown

- ATX headings (`#`, `##`)
- Code blocks fenced with ` ``` `
- Tables when comparing ≥3 items
- Examples have Command + Output + Notes structure
- Trigger keywords in SKILL.md description only (not in body)

### Commit messages

[Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add --allowlist flag
fix: bash 3.2 unset variable on empty array
docs: clarify skiplist precedence
chore: bump version to 2.1.0
test: add integration test for fork rebase
refactor: extract autoresolve into function
```

## Submitting changes

1. **Branch off `main`**: `git checkout -b feat/my-change`
2. **Write tests first** for new behavior (TDD):
   - Run existing tests to confirm they pass
   - Add new test(s) for your change
   - Confirm new tests fail without your code change
3. **Implement**
4. **Update docs**: SKILL.md (if user-facing), CHANGELOG.md (always), INTERNALS.md (if design decision)
5. **Run all tests**: `bash tests/run-all.sh`
6. **Self-review** with the [checklist](#self-review-checklist) below
7. **Commit + push** + open PR

### Self-review checklist

- [ ] `bash -n` passes on every script
- [ ] All `tests/*.sh` pass
- [ ] SKILL.md frontmatter version bumped if user-facing change
- [ ] CHANGELOG.md updated under `[Unreleased]` section
- [ ] Trigger keywords updated in description (if new use case)
- [ ] No `set -u` (use `set -o pipefail`)
- [ ] No `mapfile` (use `while-read`)
- [ ] All new flags appear in `--help` output
- [ ] Examples updated if behavior changed
- [ ] No hardcoded paths to user-specific data
- [ ] No accidental `git push --force` or destructive ops in any test
- [ ] macOS bash 3.2 tested (Linux bash 4+ is permissive, hides issues)

## Release process

Maintainers only:

1. Update `CHANGELOG.md`: move `[Unreleased]` items to new version block, add date
2. Bump `version` in `SKILL.md` frontmatter
3. Commit: `chore: release vX.Y.Z`
4. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z release notes"`
5. Push: `git push --follow-tags`
6. (When external) GitHub release with excerpt from CHANGELOG

### Versioning rules

- **Major (X.0.0)**: breaking flag semantics, removed features, output format change
- **Minor (0.X.0)**: new flags, new behavior, new examples, non-breaking improvements
- **Patch (0.0.X)**: bug fixes, docs, tests, refactors with no behavior change

## Questions?

Open an issue or check [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) first.
