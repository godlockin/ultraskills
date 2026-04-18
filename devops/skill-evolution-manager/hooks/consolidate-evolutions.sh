#!/usr/bin/env bash
# consolidate-evolutions.sh — LLM-powered consolidation of evolution.json → lessons DB
# Usage: consolidate-evolutions.sh [--threshold-only]
# --threshold-only: only process files exceeding THRESHOLD, skip scheduled full run
#
# Flow per skill:
#   evolution.json (raw accumulated)
#     + ~/.claude/lessons/by-skill/{id}.md (existing lessons)
#   → claude -p (merge + dedup + refine)
#   → ~/.claude/lessons/by-skill/{id}.md (updated)
#   → ~/.claude/lessons/index.json (updated)
#   → evolution.json cleared (lists wiped, custom_prompts preserved)

THRESHOLD=15          # trigger when fixes+preferences+contexts > this
SEARCH_ROOTS=(
  "$HOME/.claude/skills"
  "$HOME/working/sourcecode/tools/llm_apps/ultraskills"
)
LESSONS_DIR="$HOME/.claude/lessons"
LOG="$HOME/.claude/hooks/consolidate-evolutions.log"
STAMP=$(date '+%Y-%m-%dT%H:%M:%S')

threshold_only=false
[[ "$1" == "--threshold-only" ]] && threshold_only=true

log() { echo "[$STAMP] $*" >> "$LOG"; }

# Ensure lessons dir structure exists
mkdir -p "$LESSONS_DIR/by-skill"
[ ! -f "$LESSONS_DIR/index.json" ] && echo '{"version":1,"lessons":[]}' > "$LESSONS_DIR/index.json"

consolidate_file() {
  local evo_file="$1"
  local skill_dir
  skill_dir=$(dirname "$evo_file")
  local skill_id
  skill_id=$(basename "$skill_dir")

  # Count total items — pass path as argument
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

  log "Consolidating $skill_id ($count items) → lessons DB..."

  local lessons_file="$LESSONS_DIR/by-skill/${skill_id}.md"
  local NOW
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Build combined context: existing lessons + new evolution data → tmpfile
  local tmpfile
  tmpfile=$(mktemp /tmp/evo-consolidate-XXXXXX)
  {
    echo "=== EXISTING LESSONS (previously consolidated) ==="
    if [ -f "$lessons_file" ]; then
      cat "$lessons_file"
    else
      echo "(none yet)"
    fi
    echo ""
    echo "=== NEW RAW EVOLUTION DATA ==="
    cat "$evo_file"
  } > "$tmpfile"

  # Call claude: merge existing lessons + new evolution data → markdown lessons
  local result
  result=$(claude -p "You are maintaining an AI skill's lessons-learned database.

Task: Merge the EXISTING LESSONS with NEW RAW EVOLUTION DATA into a clean, actionable lessons file.

Rules:
- Combine both sources into unified insights
- Merge semantically duplicate entries into one clear statement
- Extract patterns from multiple similar fixes into a single rule
- Remove outdated or contradictory entries (keep the newer intent)
- Keep total lessons under 15 bullet points
- Preserve all unique insights
- Group by theme if helpful (e.g. ## Usage, ## Gotchas, ## Preferences)
- Write in concise imperative style (e.g. 'Always pass path as sys.argv[1]')
- Output ONLY valid markdown, no JSON, no explanation
- First line must be exactly: ## Lessons: SKILL_ID_PLACEHOLDER (updated: TIMESTAMP_PLACEHOLDER)

Input is provided via stdin." < "$tmpfile" 2>/dev/null)

  rm -f "$tmpfile"

  if [ -z "$result" ]; then
    log "⚠️  $skill_id: LLM returned empty, skipping"
    return
  fi

  # Write to lessons DB
  echo "$result" > "$lessons_file"

  # Update index.json — extract keywords, upsert entry
  python3 - "$LESSONS_DIR/index.json" "$skill_id" "$lessons_file" "$NOW" << 'PY' 2>/dev/null
import sys, json, re

index_path, skill_id, lessons_file, now = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

try:
    content = open(lessons_file, encoding='utf-8').read()
    stopwords = {'always','never','should','must','when','with','from','have','this','that',
                 'then','than','just','also','note','make','sure','only','each','some','such',
                 'will','been','into','over','more','most','many','both','after','before',
                 'other','these','those','their','there','where','which','about','first',
                 'every','using','being','doing','having','skill','lesson','lessons'}
    words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', content)
    keywords = list(dict.fromkeys(w.lower() for w in words if w.lower() not in stopwords))[:20]
except Exception:
    keywords = []

try:
    idx = json.load(open(index_path, encoding='utf-8'))
except Exception:
    idx = {"version": 1, "lessons": []}

idx['lessons'] = [l for l in idx.get('lessons', []) if l.get('id') != skill_id]
idx['lessons'].append({
    "id": skill_id,
    "path": lessons_file,
    "updated": now,
    "keywords": keywords
})

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)
print(f"index updated: {skill_id}")
PY

  # Clear evolution.json — wipe accumulated lists, preserve custom_prompts
  python3 - "$evo_file" "$NOW" << 'PY' 2>/dev/null
import sys, json
evo_path, now = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(evo_path, encoding='utf-8'))
except Exception:
    d = {}
cleared = {"last_updated": now, "last_consolidated": now}
if d.get("custom_prompts"):
    cleared["custom_prompts"] = d["custom_prompts"]
with open(evo_path, 'w', encoding='utf-8') as f:
    json.dump(cleared, f, indent=2, ensure_ascii=False)
print("evolution.json cleared")
PY

  log "✅ $skill_id: → $lessons_file, evolution.json cleared"
}

# Find all evolution.json files
for root in "${SEARCH_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  while IFS= read -r evo_file; do
    consolidate_file "$evo_file"
  done < <(find "$root" -name "evolution.json" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null)
done

log "Done."
