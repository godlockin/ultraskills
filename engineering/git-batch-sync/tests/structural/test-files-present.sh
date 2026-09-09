#!/usr/bin/env bash
# test-files-present.sh — required S-Tier files exist
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

declare -a REQUIRED=(
  "SKILL.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "INTERNALS.md"
  "TROUBLESHOOTING.md"
  "TESTING.md"
  "scripts/git-batch-sync.sh"
  "scripts/install-deps.sh"
  "scripts/justfile"
  "references/tools-mapping.md"
)
declare -a OPTIONAL=(
  "examples/example-1-summary.md"
  "examples/example-2-conflict.md"
  "examples/example-3-fork-upstream.md"
  "examples/example-4-bench.md"
)

fail=0
for f in "${REQUIRED[@]}"; do
  if [ ! -f "$SCRIPT_DIR/$f" ]; then
    echo "✗ missing required: $f"
    fail=$((fail+1))
  else
    echo "✓ $f"
  fi
done

# Optional examples — warn but don't fail
for f in "${OPTIONAL[@]}"; do
  if [ ! -f "$SCRIPT_DIR/$f" ]; then
    echo "  (optional) missing: $f"
  else
    echo "✓ $f"
  fi
done

exit $fail
