#!/usr/bin/env bash
# test-frontmatter.sh — SKILL.md has required YAML frontmatter fields
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_MD="$SCRIPT_DIR/SKILL.md"

if [ ! -f "$SKILL_MD" ]; then
  echo "✗ SKILL.md missing"
  exit 1
fi
echo "✓ SKILL.md exists"

# Extract frontmatter
fm=$(awk '/^---$/{c++; next} c==1' "$SKILL_MD")
if [ -z "$fm" ]; then
  echo "✗ no YAML frontmatter"
  exit 1
fi
echo "✓ frontmatter present"

# Required fields
for field in "name:" "description:" "version:" "tags:"; do
  if ! grep -q "^$field" <<< "$fm"; then
    echo "✗ missing field: $field"
    exit 1
  fi
  echo "✓ field '$field' present"
done

# Version must be semver-ish
version=$(grep "^version:" <<< "$fm" | awk '{print $2}')
if ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
  echo "✗ version '$version' not semver (X.Y.Z)"
  exit 1
fi
echo "✓ version = $version"

echo "PASS"
