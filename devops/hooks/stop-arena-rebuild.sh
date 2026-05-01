#!/usr/bin/env bash
# stop-arena-rebuild.sh — Stop hook
# If any SKILL.md was written this session (flagged by post-skill-write.sh),
# run the full arena pipeline to rebuild index.json.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PENDING_FLAG="$REPO_DIR/.claude/arena-rebuild-pending"

if [ ! -f "$PENDING_FLAG" ]; then
  exit 0
fi

rm -f "$PENDING_FLAG"

echo ""
echo "⚙️  SKILL.md changes detected — running arena pipeline..."
echo "   (arena_scan → arena_cluster_score → arena_build_index)"
echo ""

cd "$REPO_DIR"

python3 scripts/arena_scan.py 2>&1 | tail -3
python3 scripts/arena_cluster_score.py 2>&1 | tail -3
python3 scripts/arena_build_index.py 2>&1 | tail -3

echo ""
echo "✓ Arena pipeline complete. index.json rebuilt."
echo "  Run validate_skills.py to confirm."
