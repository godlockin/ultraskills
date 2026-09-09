#!/usr/bin/env bash
# test-help-flag.sh — --help exits 0 and contains key sections
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$SCRIPT_DIR/scripts/git-batch-sync.sh"

out=$(bash "$SCRIPT" --help 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  echo "✗ --help exited $rc, expected 0"
  exit 1
fi
echo "✓ --help exits 0"

# Required sections
for section in "Main run" "Filters" "Tools & diagnostics" "Conflict policy" "Examples"; do
  if ! grep -q "$section" <<< "$out"; then
    echo "✗ --help missing section: $section"
    exit 1
  fi
  echo "✓ contains '$section'"
done

# Required flag mentions
for flag in "--summary" "--dry-run" "--sync-upstream" "--push" "--skiplist" "--allowlist" "--install-deps" "--migrate-tools" "--bench" "--stats"; do
  if ! grep -qF -- "$flag" <<< "$out"; then
    echo "✗ --help missing flag: $flag"
    exit 1
  fi
done
echo "✓ all required flags documented"

echo "PASS"
