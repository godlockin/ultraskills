#!/usr/bin/env bash
# install.sh — 注入 ultraskills Skill Fallback 到 ~/.claude/CLAUDE.md
#
# 安装后，Claude Code 在任何项目中找不到 skill 时会自动搜索本仓库。
#
# Usage:
#   ./install.sh           # 注入 Skill Fallback section
#   ./install.sh --remove  # 移除注入的 section
#   ./install.sh --check   # 检查是否已安装

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
MARKER_START="## Skill Fallback — ultraskills"
MARKER_END="<!-- /ultraskills-fallback -->"

check_installed() {
  [ -f "$CLAUDE_MD" ] && grep -qF "$MARKER_START" "$CLAUDE_MD"
}

do_install() {
  if check_installed; then
    echo "✓ 已安装，无需重复注入。"
    echo "  位置: $CLAUDE_MD"
    return 0
  fi

  mkdir -p "$HOME/.claude"
  [ -f "$CLAUDE_MD" ] || touch "$CLAUDE_MD"

  cat >> "$CLAUDE_MD" << SECTION

$MARKER_START

当需要某 skill 但不在已加载列表中时，**必须主动搜索 ultraskills 仓库**：

\`\`\`bash
python3 $REPO_DIR/devops/ultraskills-hub/scripts/search.py "<关键词>"
\`\`\`

**流程：**
1. 运行上述搜索命令（关键词从用户请求中提取）
2. 取返回 JSON 中 match_score 最高且相关的结果的 \`path\` 字段
3. 用 Read 工具读取该 path（SKILL.md 绝对路径）
4. 将读到的内容作为当前任务的指导直接执行

**触发条件（满足任一即搜索）：**
- 用户请求的 skill 不在已加载列表中
- 任务涉及特定领域/方法论，但不确定用哪个 skill
- 用户说"找个 skill"/"有没有相关的 skill"

不要创建 symlink，直接 Read + 执行。搜索无结果则正常回答。
$MARKER_END
SECTION

  echo "✓ 已注入 Skill Fallback 到 $CLAUDE_MD"
  echo "  ultraskills 路径: $REPO_DIR"
  echo ""
  echo "  下次新开 Claude Code session 即生效。"
}

do_remove() {
  if ! check_installed; then
    echo "未安装，无需移除。"
    return 0
  fi

  python3 - "$CLAUDE_MD" "$MARKER_START" "$MARKER_END" << 'PY'
import sys
path, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
si = content.find(start)
ei = content.find(end)
if si == -1 or ei == -1:
    sys.exit(0)
# Remove from the newline before marker_start to end of marker_end line
before = content[:si].rstrip("\n")
after = content[ei + len(end):]
result = before + after
with open(path, "w", encoding="utf-8") as f:
    f.write(result)
PY

  echo "✓ 已从 $CLAUDE_MD 移除 Skill Fallback section。"
}

do_check() {
  if check_installed; then
    echo "✓ 已安装"
    grep -n "$MARKER_START" "$CLAUDE_MD"
  else
    echo "✗ 未安装"
  fi
}

case "${1:-}" in
  --remove) do_remove ;;
  --check)  do_check ;;
  *)        do_install ;;
esac
