#!/usr/bin/env bash
# test-syntax.sh — bash -n on every script
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
pass=0; fail=0
for f in "$SCRIPT_DIR"/scripts/*.sh; do
  if bash -n "$f" 2>/dev/null; then
    echo "✓ $(basename "$f")"
    pass=$((pass+1))
  else
    echo "✗ $(basename "$f") — syntax error"
    bash -n "$f"
    fail=$((fail+1))
  fi
done
echo
echo "PASS: $pass  FAIL: $fail"
exit $fail
