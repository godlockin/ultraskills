#!/usr/bin/env bash
# setup_lightpanda.sh — 下载 lightpanda 二进制到 external/lightpanda/bin/
#
# 调用时机:
#   - 项目初始化 (install.sh / setup.sh) 时自动调用
#   - 用户手动: ./scripts/setup_lightpanda.sh [--force]
#
# 行为:
#   1. 检测 OS + arch (darwin/linux × arm64/amd64)
#   2. 从 GitHub releases 下载对应 binary
#   3. 写到 external/lightpanda/bin/lightpanda
#   4. chmod +x
#   5. 验证版本 (lightpanda --version)
#
# 失败处理: 任何 step 失败立即退出, 不污染工作树

set -euo pipefail

# 路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LP_DIR="$REPO_ROOT/external/lightpanda"
BIN_DIR="$LP_DIR/bin"
BIN_PATH="$BIN_DIR/lightpanda"

# 配置
GITHUB_API="https://api.github.com/repos/lightpanda-io/browser/releases/latest"
BASE_URL="https://github.com/lightpanda-io/browser/releases/download/nightly"
FORCE=0

# 参数
[[ "${1:-}" == "--force" ]] && FORCE=1

# 检测平台
detect_platform() {
    local os arch
    case "$(uname -s)" in
        Darwin) os="macos" ;;
        Linux)  os="linux" ;;
        *) echo "✗ Unsupported OS: $(uname -s)"; return 1 ;;
    esac
    case "$(uname -m)" in
        arm64|aarch64) arch="aarch64" ;;
        x86_64|amd64)  arch="x86_64"  ;;
        *) echo "✗ Unsupported arch: $(uname -m)"; return 1 ;;
    esac
    echo "${arch}-${os}"
}

main() {
    # 1. 已存在且不强制 → 跳过
    if [[ -x "$BIN_PATH" && $FORCE -eq 0 ]]; then
        echo "✓ lightpanda already installed: $BIN_PATH"
        "$BIN_PATH" --version 2>&1 | head -1 || true
        return 0
    fi

    # 2. 检查目录
    if [[ ! -d "$LP_DIR" ]]; then
        echo "✗ external/lightpanda/ not found"
        echo "  Run: git submodule add https://github.com/lightpanda-io/browser.git external/lightpanda"
        return 1
    fi

    # 3. 检测平台
    local platform
    platform=$(detect_platform) || return 1
    local binary_name="lightpanda-${platform}"
    local download_url="${BASE_URL}/${binary_name}"
    echo "→ Platform: $platform"
    echo "→ URL: $download_url"

    # 4. 下载
    mkdir -p "$BIN_DIR"
    echo "→ Downloading..."
    if ! curl -fSL --retry 2 --max-time 120 -o "$BIN_PATH.tmp" "$download_url"; then
        echo "✗ Download failed"
        rm -f "$BIN_PATH.tmp"
        return 1
    fi

    # 5. chmod + 验证
    chmod +x "$BIN_PATH.tmp"
    mv "$BIN_PATH.tmp" "$BIN_PATH"

    echo "✓ Installed: $BIN_PATH"
    echo ""
    echo "=== Version ==="
    "$BIN_PATH" --version 2>&1 | head -3 || echo "(no --version flag)"
    echo ""
    echo "=== Quick Start ==="
    echo "  $BIN_PATH serve --host 127.0.0.1 --port 9222  # CDP server"
    echo "  curl http://127.0.0.1:9222/json/version        # verify"
}

main "$@"
