#!/usr/bin/env bash
# auto-evolve.sh — Stop hook: flush pending-evolutions.jsonl into skill evolution.json
# Runs after every Claude turn. Zero network, pure local.

PENDING="$HOME/.claude/pending-evolutions.jsonl"
MERGE_SCRIPT="$HOME/working/sourcecode/tools/llm_apps/ultraskills/devops/skill-evolution-manager/scripts/merge_evolution.py"
LOG="$HOME/.claude/hooks/auto-evolve.log"

# Nothing to do
[ ! -f "$PENDING" ] && exit 0
[ ! -s "$PENDING" ] && exit 0
[ ! -f "$MERGE_SCRIPT" ] && exit 0

# Process each line
while IFS= read -r line; do
  [ -z "$line" ] && continue

  # Extract skill_dir and data fields
  skill_dir=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('skill_dir',''))" 2>/dev/null)
  data=$(echo "$line" | python3 -c "
import sys, json
d = json.load(sys.stdin)
d.pop('skill_dir', None)
print(json.dumps(d, ensure_ascii=False))
" 2>/dev/null)

  [ -z "$skill_dir" ] && continue
  [ ! -d "$skill_dir" ] && continue

  python3 "$MERGE_SCRIPT" "$skill_dir" "$data" >> "$LOG" 2>&1

done < "$PENDING"

# Clear processed entries
> "$PENDING"

# Threshold check: consolidate any evolution.json that exceeds limit
CONSOLIDATE="$HOME/.claude/hooks/consolidate-evolutions.sh"
[ -x "$CONSOLIDATE" ] && "$CONSOLIDATE" --threshold-only >> "$LOG" 2>&1 &
