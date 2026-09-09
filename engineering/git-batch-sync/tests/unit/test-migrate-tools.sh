#!/usr/bin/env bash
# test-migrate-tools.sh — output 13+ pairs and proper format
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$SCRIPT_DIR/scripts/git-batch-sync.sh"

out=$(bash "$SCRIPT" --migrate-tools 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  echo "✗ --migrate-tools exited $rc"
  exit 1
fi
echo "✓ --migrate-tools exits 0"

# Required pairs (POSIX → Rust)
declare -a REQUIRED=( "find:fd" "grep:rg" "cat:bat" "ls:eza" "diff:delta" "du:dust" "ps:procs" "time:hyperfine" "wc:tokei" "make:just" )
for pair in "${REQUIRED[@]}"; do
  legacy="${pair%:*}"; modern="${pair#*:}"
  if ! grep -qE "$legacy[[:space:]]+$modern" <<< "$out"; then
    echo "✗ missing pair: $legacy → $modern"
    exit 1
  fi
  echo "✓ $legacy → $modern listed"
done

if ! grep -q "tool migration" <<< "$out"; then
  echo "✗ missing header"
  exit 1
fi
echo "PASS"
