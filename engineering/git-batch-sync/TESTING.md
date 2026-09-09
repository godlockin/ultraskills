# Testing

## Strategy

| Level | Type | Speed | Purpose |
|---|---|---|---|
| **Unit** | Single function / single flag | < 1s | Sanity check flag parsing, syntax |
| **Structural** | File layout, frontmatter, --help | < 5s | Ensure all flags appear in help |
| **Integration** | Real git repos in temp dirs | 30s-2min | Verify pull/rebase/push behavior |
| **E2E** | Against user's source tree | 5-30min | Catch surprises in real environment |

We run **unit + structural + integration** in CI. **E2E** is manual (depends on user's tree).

## Quick run

```bash
# All tests
bash tests/run-all.sh

# Specific level
bash tests/run-unit.sh
bash tests/run-structural.sh
bash tests/run-integration.sh
```

## Test files

```
tests/
├── run-all.sh                # orchestrates everything
├── run-unit.sh               # syntax checks, --help, --version
├── run-structural.sh         # frontmatter, file presence
├── run-integration.sh        # real git in tmp dirs
├── unit/
│   ├── test-syntax.sh
│   ├── test-help-flag.sh
│   ├── test-install-deps-mode.sh
│   ├── test-migrate-tools.sh
│   └── test-version-flag.sh
├── structural/
│   ├── test-frontmatter.sh
│   ├── test-files-present.sh
│   └── test-help-content.sh
├── integration/
│   ├── test-real-repo.sh
│   ├── test-allowlist.sh
│   ├── test-skiplist.sh
│   ├── test-fd-fallback.sh
│   ├── test-conflict-ff-only.sh
│   └── test-retry-pass.sh
└── fixtures/
    └── (auto-generated temp git repos)
```

## Writing new tests

Each test is a self-contained bash script that:

1. Returns exit 0 on pass, non-zero on fail
2. Prints clear `✓` or `✗` per assertion
3. Cleans up its own fixtures (trap EXIT)
4. Is independent (no shared state with other tests)

```bash
#!/bin/bash
# tests/unit/test-new-flag.sh
set -o pipefail

SCRIPT="$(dirname "$0")/../../scripts/git-batch-sync.sh"

# Test 1: --new-flag is accepted
out=$(bash "$SCRIPT" --new-flag 2>&1)
if [[ $? -ne 0 ]]; then
  echo "✗ --new-flag should exit 0"
  exit 1
fi
echo "✓ --new-flag accepted"

# Test 2: --new-flag produces expected output
if ! grep -q "expected output" <<< "$out"; then
  echo "✗ --new-flag should print 'expected output'"
  exit 1
fi
echo "✓ --new-flag output correct"

echo "PASS"
```

## Integration test pattern

Most integration tests use **local bare repos** as fake remotes:

```bash
# tests/integration/test-real-repo.sh
set -o pipefail

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# Create a fake remote
git init --bare "$TMP/remote.git" >/dev/null

# Create a local clone with one commit
git clone "$TMP/remote.git" "$TMP/local" >/dev/null
cd "$TMP/local"
git -c user.email=t@t -c user.name=t commit --allow-empty -m "initial" >/dev/null
git push origin main >/dev/null

# Add a second commit to remote (simulate incoming)
git clone "$TMP/remote.git" "$TMP/writer" >/dev/null
cd "$TMP/writer"
git -c user.email=t@t -c user.name=t commit --allow-empty -m "remote commit" >/dev/null
git push origin main >/dev/null

# Run the skill against TMP/local's parent
cd "$TMP"
bash "$SKILL_SCRIPT" "$TMP" --no-fetch  # pre-fetched
# ... assert state ...
```

## Coverage matrix

| Behavior | Test |
|---|---|
| `bash -n` on every script | unit/syntax |
| `--help` exits 0 with expected sections | unit/help-flag |
| `--install-deps` doesn't actually `brew install` (mock) | unit/install-deps |
| `--migrate-tools` lists 13+ pairs | unit/migrate-tools |
| `--version` (if added) | unit/version-flag |
| Frontmatter has name / description / version / tags | structural/frontmatter |
| SKILL.md, CHANGELOG.md, etc. all exist | structural/files-present |
| `--help` mentions every flag in source | structural/help-content |
| Empty repo tree → exit 2 | integration/empty |
| Single repo, no upstream → skip | integration/no-upstream |
| Single repo, fast-forwardable → updated | integration/ff-only |
| Single repo, diverged, rebase succeeds | integration/rebase-success |
| Single repo, code conflict → abort + report | integration/conflict |
| Lockfile conflict → auto-resolve | integration/lockfile-conflict |
| Fork with upstream → rebase upstream | integration/fork |
| Fetch fail → record + retry | integration/retry |
| `--allowlist` filters correctly | integration/allowlist |
| `--skiplist` filters correctly | integration/skiplist |
| fd missing → find fallback | integration/fd-fallback |
| bash 3.2 compat (run with bash 3.2 explicitly) | integration/bash32 |

## CI integration

```yaml
# .github/workflows/test.yml (when externalized)
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest  # bash 3.2 compat
    steps:
      - uses: actions/checkout@v4
      - run: brew install fd ripgrep
      - run: bash tests/run-all.sh
      - run: bash tests/integration/test-real-repo.sh  # must pass
```

## What this skill does NOT test

- **Network behavior** — too flaky for CI. Manual test only.
- **Real remote conflicts** — too unpredictable. Test creates fake local conflicts.
- **Performance benchmarks** — too env-dependent. Use `--bench` for relative numbers only.
- **macOS / Linux differences beyond bash 3.2** — not specifically tested.
