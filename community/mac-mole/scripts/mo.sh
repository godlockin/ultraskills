#!/usr/bin/env bash
# mac-mole 安全包装：破坏性命令强制 dry-run 门控
# 用法:
#   mo.sh preview clean          # 只 dry-run，输出摘要
#   mo.sh exec clean             # 真删（调用方必须已获用户确认）
#   mo.sh status | history ...   # 只读命令直接透传
set -euo pipefail

MO="${MO:-mo}"
cmd="${1:-help}"; shift || true

is_destructive() {
  case "$1" in
    clean|uninstall|optimize|purge|installer|remove) return 0 ;;
    *) return 1 ;;
  esac
}

case "$cmd" in
  preview)
    target="${1:?usage: mo.sh preview <clean|uninstall|optimize|purge|installer>}"
    is_destructive "$target" || { echo "非破坏性命令无需 preview: $target" >&2; exit 1; }
    exec "$MO" "$target" --dry-run
    ;;
  exec)
    target="${1:?usage: mo.sh exec <clean|uninstall|optimize|purge|installer>}"
    is_destructive "$target" || exec "$MO" "$target"
    # 门控：要求环境变量 MOLE_CONFIRMED=YES（由调用方在用户确认后显式设置）
    [ "${MOLE_CONFIRMED:-}" = "YES" ] || {
      echo "REFUSED: 用户未确认。先 'mo.sh preview $target' 展示 dry-run，获用户同意后 MOLE_CONFIRMED=YES 再 exec。" >&2
      exit 2
    }
    exec "$MO" "$target"
    ;;
  status|history|analyze)
    exec "$MO" "$cmd" "$@"
    ;;
  *)
    exec "$MO" "$cmd" "$@"
    ;;
esac
