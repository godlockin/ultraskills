#!/usr/bin/env bash
# consolidate-evolutions.sh — LLM-powered consolidation of evolution.json files
# Usage: consolidate-evolutions.sh [--threshold-only]
# --threshold-only: only process files exceeding THRESHOLD, skip scheduled full run

THRESHOLD=15          # trigger consolidation when fixes+preferences > this
SEARCH_ROOTS=(
  "$HOME/.claude/skills"
  "$HOME/working/sourcecode/tools/llm_apps/ultraskills"
)
LOG="$HOME/.claude/hooks/consolidate-evolutions.log"
STAMP=$(date '+%Y-%m-%dT%H:%M:%S')

threshold_only=false
[[ "$1" == "--threshold-only" ]] && threshold_only=true

log() { echo "[$STAMP] $*" >> "$LOG"; }

consolidate_file() {
  local evo_file="$1"
  local skill_dir
  skill_dir=$(dirname "$evo_file")
  local skill_name
  skill_name=$(basename "$skill_dir")

  # Count total items — pass path as argument, never interpolate into python string
  local count
  count=$(python3 - "$evo_file" << 'PY' 2>/dev/null
import sys, json
try:
    d = json.load(open(sys.argv[1]))
    n = len(d.get('fixes', [])) + len(d.get('preferences', [])) + len(d.get('contexts', []))
    print(n)
except Exception:
    print(0)
PY
)

  [[ -z "$count" || "$count" -eq 0 ]] && return

  if $threshold_only && [[ "$count" -le "$THRESHOLD" ]]; then
    return
  fi

  log "Consolidating $skill_name ($count items)..."

  local NOW
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Call claude to consolidate — pipe file directly, no bash variable expansion in prompt
  local result
  result=$(claude -p "You are consolidating an AI skill's evolution.json file.

Rules:
- Merge semantically duplicate entries into one clear statement
- Extract patterns from multiple similar fixes into a single rule
- Remove outdated or contradictory entries (keep the newer intent)
- Keep total fixes+preferences+contexts under 10 items
- Preserve all unique insights, do not lose important learnings
- Output ONLY valid JSON, no explanation, matching this schema:
  {\"last_updated\": \"<iso>\", \"fixes\": [...], \"preferences\": [...], \"contexts\": [...], \"custom_prompts\": \"...\"}
- Omit empty arrays/fields
- last_updated should be $NOW

Input evolution.json is provided via stdin." < "$evo_file" 2>/dev/null)

  # Validate JSON
  if echo "$result" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
    # Backup original
    cp "$evo_file" "${evo_file}.bak"
    echo "$result" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps(d, indent=2, ensure_ascii=False))
" > "$evo_file"
    # Count after — pass path as argument
    local after
    after=$(python3 - "$evo_file" << 'PY' 2>/dev/null
import sys, json
try:
    d = json.load(open(sys.argv[1]))
    print(len(d.get('fixes',[])) + len(d.get('preferences',[])) + len(d.get('contexts',[])))
except Exception:
    print('?')
PY
)
    log "✅ $skill_name consolidated ($count → $after items)"
  else
    log "⚠️  $skill_name: LLM returned invalid JSON, skipping"
  fi
}

# Find all evolution.json files
for root in "${SEARCH_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  while IFS= read -r evo_file; do
    consolidate_file "$evo_file"
  done < <(find "$root" -name "evolution.json" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null)
done

log "Done."
