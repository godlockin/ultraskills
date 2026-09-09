#!/usr/bin/env bash
# install-deps.sh — 一键安装/检测 git-batch-sync 所需 rust 工具
# Usage: install-deps.sh [--core-only] [--with-optional]
set -u

CORE=(fd ripgrep)              # 必需 (有降级但性能差)
OPTIONAL=(eza bat delta dust procs hyperfine tokei just)

core_only=0
with_optional=0
for arg in "$@"; do
  case "$arg" in
    --core-only)     core_only=1 ;;
    --with-optional) with_optional=1 ;;
  esac
done

C_GRN=$'\033[32m'; C_YEL=$'\033[33m'; C_BLU=$'\033[34m'; C_OFF=$'\033[0m'
ok()  { echo "${C_GRN}✓${C_OFF} $*"; }
miss(){ echo "${C_YEL}✗${C_OFF} $*"; }
info(){ echo "${C_BLU}▶${C_OFF} $*"; }

echo "=== git-batch-sync deps installer ==="
echo "检测系统..."

if ! command -v brew >/dev/null 2>&1; then
  miss "Homebrew 缺失"
  echo "  安装: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  exit 1
fi
ok "brew: $(brew --version | head -1)"

# 平台检查
OS=$(uname -s)
ARCH=$(uname -m)
info "OS=$OS ARCH=$ARCH"
echo

install_one() {
  local t="$1"
  if command -v "$t" >/dev/null 2>&1; then
    ok "$t: $(command -v $t) ($($t --version 2>/dev/null | head -1 | cut -d' ' -f1-3))"
  else
    info "brew install $t"
    brew install "$t" 2>&1 | tail -3
  fi
}

info "[CORE]"
for t in "${CORE[@]}"; do install_one "$t"; done

if [ $core_only -eq 0 ]; then
  echo
  info "[OPTIONAL]"
  for t in "${OPTIONAL[@]}"; do install_one "$t"; done
fi

echo
ok "完成。验证: bash <(dirname \"\$0\")/git-batch-sync.sh --summary"
