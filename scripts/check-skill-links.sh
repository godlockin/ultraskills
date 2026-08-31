#!/usr/bin/env bash
# 检查 skill 目录内所有 markdown 的本地链接是否有效
# Usage: bash scripts/check-skill-links.sh <skill-dir> [<skill-dir> ...]
#
# exit 0 = 无断链 / exit 1 = 有断链

set -uo pipefail

REPORT="$(mktemp)"
trap 'rm -f "$REPORT"' EXIT

for ROOT in "$@"; do
  if [ ! -d "$ROOT" ]; then
    echo "SKIP  $ROOT (不存在)"
    continue
  fi
  ROOT="$(cd "$ROOT" && pwd)"
  BASE="$(basename "$ROOT")"
  while IFS= read -r md; do
    dir="$(dirname "$md")"
    rel_md="${md#"$ROOT"/}"
    # 提取 markdown 链接里的本地路径(排除 http/https/mailto/纯 anchor)
    while IFS= read -r link; do
      [ -z "$link" ] && continue
      case "$link" in
        /*) target="$link" ;;
        *)  target="$dir/$link" ;;
      esac
      if [ ! -e "$target" ]; then
        echo "BROKEN  $BASE/$rel_md → $link" >> "$REPORT"
      fi
    done < <(
      grep -oE '\]\([^)]+\)' "$md" 2>/dev/null \
        | sed -E 's/^\]\(//; s/\)$//' \
        | grep -vE '^(https?:|mailto:|#)' \
        | sed -E 's/#.*$//' \
        | grep -v '^$'
    )
  done < <(find "$ROOT" -name '*.md' -type f)
done

BROKEN=0
if [ -s "$REPORT" ]; then
  cat "$REPORT"
  BROKEN="$(wc -l < "$REPORT" | tr -d ' ')"
fi

echo "---"
if [ "$BROKEN" -eq 0 ]; then
  echo "link check: 未发现断链"
else
  echo "link check: $BROKEN 处断链"
  exit 1
fi
