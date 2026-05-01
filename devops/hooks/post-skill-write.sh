#!/usr/bin/env bash
# post-skill-write.sh — PostToolUse hook
# Triggered after Write/Edit. If a SKILL.md or index.json was touched,
# run validate_skills.py and optionally mark arena rebuild as pending.
#
# Called by Claude Code with tool input on stdin (JSON).

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PENDING_FLAG="$REPO_DIR/.claude/arena-rebuild-pending"

# Read tool input from stdin
INPUT="$(cat)"

# Extract file_path from JSON (handles both Write and Edit tool schemas)
FILE_PATH="$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
# Write tool uses 'file_path'; Edit tool uses 'file_path'
print(d.get('file_path', ''))
" 2>/dev/null)"

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Check if the touched file is skill-related
BASENAME="$(basename "$FILE_PATH")"
if [[ "$BASENAME" != "SKILL.md" && "$BASENAME" != "index.json" ]]; then
  exit 0
fi

echo ""
echo "🔍 Skill file changed: $FILE_PATH"

# Mark arena rebuild as pending (heavy; deferred to Stop hook)
if [[ "$BASENAME" == "SKILL.md" ]]; then
  touch "$PENDING_FLAG"
fi

# Run validation immediately (lightweight, ~1s)
echo "Running validate_skills.py..."
python3 "$REPO_DIR/devops/skill-arena/scripts/validate_skills.py" 2>&1 | \
  grep -E "^(ERRORS|Result|  ✗)" | head -30
echo ""
