#!/usr/bin/env bash
# read-prefilter-hook.sh — PreToolUse hook for Read/Grep/Glob tools
#
# Goal: fill the gap RTK cannot reach (Read/Grep/Glob bypass Bash hook).
# Strategy: for large file reads, ask Haiku 4.5 to produce a short summary
#           and inject it as additional context, OR auto-skip read entirely
#           when the file is unlikely to be useful.
#
# Cost: 1 Haiku call per PreToolUse invocation. ~$0.0001 each, <500ms.
# Fallback: no API key → pass through (do not break the user).
#
# Hook contract (Claude Code PreToolUse):
#   input:  stdin = JSON { tool_name, tool_input, ... }
#   output: stdout = JSON { hookSpecificOutput: { hookEventName, permissionDecision, permissionDecisionReason?, updatedInput? } }
#   exit 0 = allow, exit 2 = deny (we always allow)
#
# rtk-hook-version: 1

set -euo pipefail

# ── 0. Fast bailouts ────────────────────────────────────────────────────────
# No API key → pass through (no harm done, no LLM call)
if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${ANTHROPIC_AUTH_TOKEN:-}" ]; then
  exit 0
fi

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only intercept Read, Grep, Glob
case "$TOOL_NAME" in
  Read|Grep|Glob) ;;
  *) exit 0 ;;
esac

# Extract the file_path / pattern
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // .tool_input.pattern // empty')
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Don't intercept small files (< 50KB) — not worth the round-trip
if [ -f "$FILE_PATH" ]; then
  SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null || echo 0)
  if [ "${SIZE:-0}" -lt 51200 ]; then
    exit 0
  fi
fi

# ── 1. Ask Haiku 4.5 whether to summarize or skip ──────────────────────────
PROMPT=$(cat <<EOF
You are a token-saving prefilter. A Claude agent is about to read a file.

File: $FILE_PATH
Size: ${SIZE:-unknown} bytes
Tool: $TOOL_NAME

Decide ONE of:
- "allow" — file is small enough or clearly needed
- "summary" — produce a 200-token summary, replace tool call result
- "skip" — file is irrelevant, suggest a different file or skip

Respond with JSON: {"decision": "allow|summary|skip", "reason": "..."}
EOF
)

API_URL="${ANTHROPIC_BASE_URL:-https://api.anthropic.com}/v1/messages"
MODEL="claude-haiku-4-5"

RESPONSE=$(curl -sS --max-time 3 \
  -H "x-api-key: ${ANTHROPIC_API_KEY:-${ANTHROPIC_AUTH_TOKEN}}" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    '{
      model: $model,
      max_tokens: 256,
      messages: [{role: "user", content: $prompt}]
    }')" \
  "$API_URL" 2>/dev/null) || exit 0

DECISION=$(echo "$RESPONSE" | jq -r '.content[0].text // empty' 2>/dev/null | jq -r '.decision // "allow"' 2>/dev/null)
REASON=$(echo "$RESPONSE" | jq -r '.content[0].text // empty' 2>/dev/null | jq -r '.reason // ""' 2>/dev/null)

case "$DECISION" in
  skip)
    # Auto-allow with a reason (let Claude decide whether to actually read)
    jq -n \
      --arg reason "rtk-prefilter: $REASON" \
      '{
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "allow",
          permissionDecisionReason: $reason
        }
      }'
    exit 0
    ;;
  summary|allow|"")
    # Pass through unchanged (future: inject summary as additional context)
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
