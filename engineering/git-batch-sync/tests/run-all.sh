#!/usr/bin/env bash
# run-all.sh — orchestrate unit + structural + integration tests
set -o pipefail
TEST_DIR="$(cd "$(dirname "$0")" && pwd)"

total=0; passed=0; failed=0
failed_tests=()

run() {
  local level="$1"
  local script="$2"
  total=$((total+1))
  echo
  echo "══════════ $level: $(basename "$script") ══════════"
  if bash "$script"; then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    failed_tests+=("$level/$(basename "$script")")
  fi
}

# Unit
for s in "$TEST_DIR/unit/"*.sh; do
  [ -f "$s" ] && run "unit" "$s"
done

# Structural
for s in "$TEST_DIR/structural/"*.sh; do
  [ -f "$s" ] && run "structural" "$s"
done

# Integration (slower)
for s in "$TEST_DIR/integration/"*.sh; do
  [ -f "$s" ] && run "integration" "$s"
done

echo
echo "════════════════════════════════════════"
echo "Total: $total   PASSED: $passed   FAILED: $failed"
if [ $failed -gt 0 ]; then
  echo
  echo "Failed:"
  for t in "${failed_tests[@]}"; do
    echo "  - $t"
  done
fi
exit $failed
