# Changelog

All notable changes to this skill are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [Semantic Versioning](https://semver.org/).

## [2.0.0] — 2026-09-09

### Added — S-Tier release

#### Core features
- **Blacklist (`--skiplist`)** — skip paths in a file, supports prefix matching (`study/tigerobo` skips subtree)
- **Allowlist (`--allowlist`)** — whitelist mode, applied before skiplist, with precedence rules
- **fork upstream sync (`--sync-upstream`)** — auto-detect forks via `remote.upstream.url`, rebase to upstream, then pull origin
- **fork push (`--push`)** — push back to origin after successful update
- **fetch failure retry** — record `Connection closed` / `Could not read` failures, auto-retry once at end of run
- **failed-list export** — write still-failing repos to `/tmp/claude-tasks/git-batch-sync-failed-*.txt`

#### Tooling
- **`--install-deps`** — one-click brew install of fd / ripgrep / eza / bat / delta / dust / tokei / hyperfine / just
- **`--migrate-tools`** — output legacy tool vs rust replacement status table
- **`install-deps.sh`** standalone helper with `--core-only` / `--with-optional` flags
- **`tools-mapping.md`** — comprehensive POSIX → rust tool mapping reference (13 pairs)

#### Diagnostics
- **`--stats`** — `tokei` LOC summary
- **`--bench`** — `hyperfine` fd-vs-find live benchmark
- **`--migrate-tools`** — installation audit
- **`--help` / `-h`** — full usage reference
- fork detection with `⊟ fork upstream: <url>` indicator

#### Output
- Color-coded output (auto-disable on non-tty)
- Progress indicator `[i/TOTAL]`
- Per-repo status block (dirty / fork / ahead / behind)
- Final summary with `Forks / Updated / Pushed / FetchFailed / Conflicts / Skipped / Errors / Elapsed`
- `dust` top-level directory size summary when available

### Fixed
- macOS bash 3.2 + `set -u` + empty array `${ARR[@]}` → unbound variable crash
  - Changed to `set -o pipefail`; documented in script header
- ROOT argument parsing — first positional arg was being consumed by flag (e.g. `--summary` became ROOT)
  - Now: default first, then `--root=`, then first non-flag arg overrides
- `mapfile` not available on macOS bash 3.2 → replaced with while-read loop

### Changed
- Default scan root: `~/working/sourcecode` (was `$HOME` prefix)
- Default scan depth: `max-depth=8`
- Output log: `/tmp/claude-tasks/git-batch-sync-YYYYMMDD-HHMMSS.log` (was `git-mass-update-*.log`)

### Documentation
- Added: `LICENSE` (MIT)
- Added: `CHANGELOG.md` (this file)
- Added: `CONTRIBUTING.md` (skill-level contributing guide)
- Added: `INTERNALS.md` (design rationale)
- Added: `TROUBLESHOOTING.md` (common issues + fixes)
- Added: `TESTING.md` (test strategy + integration tests)
- Added: `references/tools-mapping.md` (POSIX → rust tool table)
- Added: 4 examples covering summary / conflict / fork / bench workflows
- Restructured SKILL.md per S-Tier template: 🎯 Goal / 🧠 Core Concepts / 🚀 Workflow / ✅ Checklist
- Added 6 new trigger keywords: `黑名单 同步`, `白名单 同步`, `install fd/rg`, `migrate to fd`

### Performance
- `fd --type=dir --hidden --no-ignore --glob '.git'` for repo discovery (10-30x faster than `find`)
- `rg -q` for conflict pattern detection (10-100x faster than `grep -qiE`)
- All tool calls degrade gracefully when modern tools missing

## [1.0.0] — 2026-09-08

### Added
- Initial release: bulk sync (`git fetch` + `pull --ff-only` → rebase --autostash)
- `find`-based repo discovery
- `grep -qiE` conflict detection
- Heuristic autoresolve for lockfiles (package-lock.json, yarn.lock, Cargo.lock, etc.)
- Plain bash output, no color

### Notes
- Local skill for single user (chenchen)
- Tested on `/Users/chenchen/working/sourcecode` (253 repos)
- Basic retry-on-fetch-fail logic (sleep + retry, no proxy awareness)

[Unreleased]: https://github.com/chenchen/git-batch-sync/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/chenchen/git-batch-sync/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/chenchen/git-batch-sync/releases/tag/v1.0.0
