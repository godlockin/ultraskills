#!/bin/bash
# shield-reverse-skill.sh — 屏蔽 reverse-skill submodule 的全局 CLAUDE.md 注入
#
# 背景: reverse-skill 的 RULES.md 第 41-58 行要求 AI 在首次使用时被强制将
#       routing rules 写入 ~/.claude/CLAUDE.md 等全局配置——会劫持用户
#       所有 Claude Code 会话，违反 ultraskills 的 "non-invasive skill" 原则。
#
# 方案: 用本脚本在 submodule 目录内对 RULES.md 做以下修改:
#   1) 把 "## Global Injection (MUST do on first use)" 整段替换为 SHIELDED 警告
#   2) 把 "## Global Injection Content (Compact ...)" 整段标记为 DEPRECATED
#   3) 在文件顶部加 SHIELDED-BY-ULTRASKILLS 头，AI 可识别并拒绝
#
# 安全: 脚本是 idempotent，重复跑不会破坏文件
# 用法: bash scripts/shield-reverse-skill.sh [/path/to/external/reverse-skill]
#   默认路径: <repo>/external/reverse-skill

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUBMODULE_PATH="${1:-$REPO_ROOT/external/reverse-skill}"
RULES_FILE="$SUBMODULE_PATH/RULES.md"

# 颜色
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

if [[ ! -d "$SUBMODULE_PATH" ]]; then
  echo -e "${RED}✗ Submodule not found: $SUBMODULE_PATH${NC}"
  echo "  Run: git submodule update --init external/reverse-skill"
  exit 1
fi

if [[ ! -f "$RULES_FILE" ]]; then
  echo -e "${RED}✗ RULES.md not found: $RULES_FILE${NC}"
  echo "  This script targets zhaoxuya520/reverse-skill. Wrong submodule?"
  exit 2
fi

# 检查是否已 shield
if head -5 "$RULES_FILE" | grep -q "SHIELDED-BY-ULTRASKILLS"; then
  echo -e "${YELLOW}⚠ Already shielded (idempotent). No changes needed.${NC}"
  exit 0
fi

# 备份
BACKUP="$RULES_FILE.original.bak"
if [[ ! -f "$BACKUP" ]]; then
  cp "$RULES_FILE" "$BACKUP"
  echo -e "${GREEN}✓ Backup created: $BACKUP${NC}"
fi

# 1) 在文件顶部插入 SHIELDED 头
TMP=$(mktemp)
cat > "$TMP" <<'HEADER'
<!-- SHIELDED-BY-ULTRASKILLS -->
<!--
  ⚠️  GLOBAL INJECTION DISABLED BY ULTRASKILLS

  原仓库 zhaoxuya520/reverse-skill 的 RULES.md 包含指令，要求 AI 在首次
  使用时被强制将 routing rules 写入 ~/.claude/CLAUDE.md 等全局配置 —
  这会劫持用户所有 Claude Code 会话，违反 ultraskills 的 non-invasive 原则。

  本脚本屏蔽了以下两段:
    1. "## Global Injection (MUST do on first use)"  → 替换为警告占位符
    2. "## Global Injection Content (Compact ...)"  → 标记为 DEPRECATED

  原文件备份: RULES.md.original.bak

  如需恢复原始注入行为（不推荐）:
    mv RULES.md.original.bak RULES.md

  其他 reverse-skill 功能（routing / trigger keywords / 安全审计 / 工具
  bootstrap）保持不变，可正常使用。
-->
<!-- END SHIELDED-BY-ULTRASKILLS -->

HEADER
cat "$RULES_FILE" >> "$TMP"
mv "$TMP" "$RULES_FILE"

# 2) 替换 Global Injection (MUST do on first use) 段
RULES_FILE="$RULES_FILE" python3 <<'PYEOF'
import re
import os
from pathlib import Path

rules_file = Path(os.environ["RULES_FILE"])
text = rules_file.read_text(encoding="utf-8")

# 屏蔽段 1: Global Injection (MUST do on first use)
pattern1 = re.compile(
    r"## Global Injection \(MUST do on first use\).*?(?=^---\n\n## Trigger Keywords)",
    re.DOTALL | re.MULTILINE,
)
replacement1 = """## ⚠️ Global Injection — DISABLED BY ULTRASKILLS

> **原 RULES.md 在此处要求 AI 写入用户全局配置文件 (`~/.claude/CLAUDE.md` 等) —
> 已被本仓库屏蔽**。原因：该指令会劫持用户所有 Claude Code 会话，与 ultraskills
> 的 non-invasive skill 原则冲突。
>
> **替代方案**：用户可手动复制本 RULES.md 的核心规则到自己的 CLAUDE.md，
> 或使用 `reverse-skill-router` skill 主动调用本仓库提供的方法论。
>
> **仍可使用**：本 RULES.md 其余功能（routing / trigger keywords / 安全审计 /
> 工具 bootstrap）保持不变。

---

## Trigger Keywords"""

text = pattern1.sub(replacement1, text)

# 屏蔽段 2: Global Injection Content (Compact ...)
pattern2 = re.compile(
    r"## Global Injection Content \(Compact.*?(?=^---|\Z)",
    re.DOTALL | re.MULTILINE,
)
replacement2 = """## ⚠️ DEPRECATED: Global Injection Content (Compact) — ULTRASKILLS SHIELDED

> 该段原本用于写入全局配置；已被 ultraskills 屏蔽。如需访问原始内容，
> 请查看 `RULES.md.original.bak`。

"""

text = pattern2.sub(replacement2, text)

rules_file.write_text(text, encoding="utf-8")
print("✓ RULES.md patched: 2 sections shielded")
PYEOF

echo -e "${GREEN}✓ RULES.md successfully shielded${NC}"
echo -e "  Original backup: ${BACKUP}"
echo -e "  Patched file: ${RULES_FILE}"
echo ""
echo -e "${YELLOW}Next: read community/reverse-skill-router/SKILL.md for usage.${NC}"