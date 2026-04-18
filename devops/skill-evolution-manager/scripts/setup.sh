#!/usr/bin/env bash
# setup.sh — Auto-Evolution 引导配置脚本
# 将 auto-evolve + consolidate hooks 安装到 ~/.claude/hooks，
# 并注册 Stop hook、crontab、CLAUDE.md 指令。
#
# Usage:
#   bash setup.sh              # 交互式安装
#   bash setup.sh --yes        # 全部默认确认

set -euo pipefail

YES=false
[[ "${1:-}" == "--yes" ]] && YES=true

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
PENDING="$HOME/.claude/pending-evolutions.jsonl"

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✅ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $*${NC}"; }
err()  { echo -e "${RED}❌ $*${NC}"; }
step() { echo -e "\n${YELLOW}▶ $*${NC}"; }

confirm() {
  $YES && return 0
  read -r -p "   $1 [Y/n] " ans
  [[ -z "$ans" || "$ans" =~ ^[Yy] ]]
}

# ── Header ───────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║      UltraSkils Auto-Evolution — 引导配置脚本        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  功能：每个 Claude 对话 turn 结束后，自动将发现的"
echo "        经验教训写入对应 skill 的 evolution.json，"
echo "        并每天 2 次由 LLM 整理压缩。"
echo ""

# ── Preflight ────────────────────────────────────────────────────────────────
step "检查依赖"

if ! command -v python3 &>/dev/null; then
  err "python3 未找到，请先安装 Python 3.8+"
  exit 1
fi
ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"

if ! command -v claude &>/dev/null; then
  warn "claude CLI 未找到 — consolidate 步骤将跳过（需要 LLM 整理）"
  warn "安装后重新运行此脚本即可启用。"
  NO_CLAUDE=true
else
  ok "claude $(claude --version 2>/dev/null | head -1)"
  NO_CLAUDE=false
fi

# ── Step 1: Copy hooks ───────────────────────────────────────────────────────
step "安装 hook 脚本到 $HOOKS_DIR"

mkdir -p "$HOOKS_DIR"

copy_hook() {
  local src="$1" dst="$2"
  if [[ -f "$dst" ]]; then
    warn "已存在：$dst"
    confirm "覆盖？" || { echo "   跳过。"; return; }
  fi
  cp "$src" "$dst"
  chmod +x "$dst"
  ok "已安装：$dst"
}

copy_hook "$SKILL_DIR/hooks/auto-evolve.sh"          "$HOOKS_DIR/auto-evolve.sh"
copy_hook "$SKILL_DIR/hooks/consolidate-evolutions.sh" "$HOOKS_DIR/consolidate-evolutions.sh"

# patch MERGE_SCRIPT path in auto-evolve.sh to point to this install
sed -i.bak "s|MERGE_SCRIPT=.*|MERGE_SCRIPT=\"$SKILL_DIR/scripts/merge_evolution.py\"|" \
  "$HOOKS_DIR/auto-evolve.sh" && rm -f "$HOOKS_DIR/auto-evolve.sh.bak"
# patch SEARCH_ROOTS in consolidate-evolutions.sh
sed -i.bak "s|\"\\$HOME/working/sourcecode/tools/llm_apps/ultraskills\"|\"$SKILL_DIR/..\"|" \
  "$HOOKS_DIR/consolidate-evolutions.sh" && rm -f "$HOOKS_DIR/consolidate-evolutions.sh.bak"

# ── Step 2: Register Stop hook ───────────────────────────────────────────────
step "注册 Claude Code Stop hook"

if [[ ! -f "$SETTINGS" ]]; then
  echo '{"hooks":{}}' > "$SETTINGS"
fi

# Check if already registered
if grep -q "auto-evolve.sh" "$SETTINGS" 2>/dev/null; then
  ok "Stop hook 已存在，跳过。"
else
  confirm "写入 Stop hook 到 $SETTINGS？" || { warn "跳过 Stop hook 注册。"; }
  python3 - "$SETTINGS" "$HOOKS_DIR/auto-evolve.sh" << 'PYEOF'
import sys, json

settings_path = sys.argv[1]
hook_cmd = sys.argv[2]

with open(settings_path) as f:
    data = json.load(f)

hooks = data.setdefault("hooks", {})
stop_hooks = hooks.setdefault("Stop", [])

# Check not already there
for entry in stop_hooks:
    for h in entry.get("hooks", []):
        if hook_cmd in h.get("command", ""):
            print("already registered")
            sys.exit(0)

stop_hooks.append({"hooks": [{"type": "command", "command": hook_cmd}]})

with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
print("registered")
PYEOF
  ok "Stop hook 已注册到 $SETTINGS"
fi

# ── Step 3: Crontab ──────────────────────────────────────────────────────────
step "设置定时整理 crontab（每天 09:00 + 21:00）"

if $NO_CLAUDE; then
  warn "claude CLI 缺失，跳过 crontab 配置。"
else
  CRON_LINE_AM="0 9 * * * $HOOKS_DIR/consolidate-evolutions.sh >> $HOME/.claude/hooks/consolidate-evolutions.log 2>&1"
  CRON_LINE_PM="0 21 * * * $HOOKS_DIR/consolidate-evolutions.sh >> $HOME/.claude/hooks/consolidate-evolutions.log 2>&1"

  existing=$(crontab -l 2>/dev/null || true)
  need_add=false
  echo "$existing" | grep -q "consolidate-evolutions.sh" || need_add=true

  if $need_add; then
    confirm "添加 crontab 条目（09:00 + 21:00）？" || { warn "跳过 crontab。"; }
    (echo "$existing"; echo "$CRON_LINE_AM"; echo "$CRON_LINE_PM") | crontab -
    ok "crontab 已添加"
  else
    ok "crontab 已存在，跳过。"
  fi
fi

# ── Step 4: CLAUDE.md instructions ──────────────────────────────────────────
step "添加 Auto-Evolution 指令到 $CLAUDE_MD"

if grep -q "Auto-Evolution" "$CLAUDE_MD" 2>/dev/null; then
  ok "CLAUDE.md 中已有 Auto-Evolution 指令，跳过。"
else
  confirm "追加写入规则到 $CLAUDE_MD？" || { warn "跳过 CLAUDE.md 更新。"; }
  cat >> "$CLAUDE_MD" << 'MDEOF'

## Auto-Evolution

任务过程中发现以下情况时，**立即**追加一行到 `~/.claude/pending-evolutions.jsonl`：

- skill用法有坑（参数错误、顺序错误、版本差异）
- 用户纠正了某个行为或输出
- 发现某命令/工具的非显而易见的规则
- 某个假设被证伪

格式（单行JSON）：
```
{"skill_dir": "/绝对路径/到/skill目录", "fixes": ["具体问题描述"], "preferences": ["用户偏好"]}
```

示例：
```
{"skill_dir": "/Users/chenchen/working/sourcecode/tools/llm_apps/ultraskills/devops/skill-evolution-manager", "fixes": ["merge_evolution.py需要skill_dir为绝对路径"]}
```

每turn结束时Stop hook自动flush到对应skill的evolution.json，无需手动触发。
MDEOF
  ok "CLAUDE.md 已更新"
fi

# ── Step 5: Touch pending file ───────────────────────────────────────────────
touch "$PENDING"
ok "pending-evolutions.jsonl 就绪：$PENDING"

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║                   安装完成 🎉                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  流程总览："
echo "  Claude 发现坑 → 写 pending-evolutions.jsonl"
echo "  Turn 结束     → auto-evolve.sh flush → evolution.json"
echo "  阈值 >15 条   → consolidate-evolutions.sh (background)"
echo "  09:00 / 21:00 → consolidate-evolutions.sh (cron, LLM整理)"
echo ""
echo "  日志："
echo "    $HOOKS_DIR/auto-evolve.log"
echo "    $HOOKS_DIR/consolidate-evolutions.log"
echo ""
if $NO_CLAUDE; then
  warn "提醒：安装 claude CLI 后运行 bash $0 重新配置 crontab。"
fi
