#!/usr/bin/env bash
# test-allowlist.sh — --allowlist filters correctly
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$SCRIPT_DIR/scripts/git-batch-sync.sh"

# Create 3 fake repos
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

for name in alpha beta gamma; do
  mkdir "$TMP/$name"
  cd "$TMP/$name"
  git init -q .
  git -c user.email=t@t -c user.name=t commit -q --allow-empty -m "init"
  cd "$TMP"
done

# Allowlist only alpha + gamma
ALLOW="$TMP/allow.txt"
printf 'alpha\ngamma\n' > "$ALLOW"

out=$(bash "$SCRIPT" --summary --no-fetch --allowlist="$ALLOW" "$TMP" 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  echo "✗ exit $rc (expected 0)"
  echo "$out"
  exit 1
fi
echo "✓ exit 0"

if ! grep -q "Repos found: 2" <<< "$out"; then
  echo "✗ expected 'Repos found: 2'"
  echo "$out" | head -20
  exit 1
fi
echo "✓ allowlist matched 2 repos"

if ! grep -q "Repos found: 2.*allowlist matched: 2" <<< "$out"; then
  echo "✗ expected 'allowlist matched: 2' in summary"
  exit 1
fi
echo "✓ 'allowlist matched: 2' reported"

if grep -q "beta" <<< "$out"; then
  if grep -q "\\[2/2\\] .*beta" <<< "$out"; then
    echo "✗ beta should be excluded by allowlist"
    exit 1
  fi
fi
echo "✓ beta correctly excluded"

echo "PASS"
