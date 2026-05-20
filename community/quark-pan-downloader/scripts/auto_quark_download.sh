#!/bin/bash
# 夸克网盘全自动下载包装脚本
# 用法: ./auto_quark_download.sh <分享链接> <保存目录> [提取码]

set -e

SHARE_URL="$1"
SAVE_DIR="$2"
PASSWORD="${3:-}"

if [ -z "$SHARE_URL" ] || [ -z "$SAVE_DIR" ]; then
    echo "用法: $0 <分享链接> <保存目录> [提取码]"
    echo ""
    echo "示例:"
    echo "  $0 'https://pan.quark.cn/s/xxx' '~/Downloads/videos' '密码'"
    exit 1
fi

# 扩展目录路径
SAVE_DIR=$(eval echo "$SAVE_DIR")

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "🚀 夸克网盘全自动下载"
echo "======================================================================"
echo "链接: $SHARE_URL"
echo "密码: ${PASSWORD:-无}"
echo "目标: $SAVE_DIR"
echo ""

# Step 1: 提取 Chrome cookie
echo "[1/3] 从 Chrome 提取 cookie..."
python3 use_chrome_cookies.py "$SHARE_URL" "$SAVE_DIR" "$PASSWORD" > /dev/null 2>&1

if [ ! -f "config/cookies.txt" ]; then
    echo "[错误] Cookie 提取失败"
    echo "[提示] 请先在 Chrome 中登录 https://pan.quark.cn"
    exit 1
fi

echo "[✓] Cookie 已提取"
echo ""

# Step 2: 准备 url.txt
echo "$SHARE_URL${PASSWORD:+?pwd=$PASSWORD}" > config/url.txt
echo "[2/3] 准备转存..."
echo ""

# Step 3: 自动转存 + 下载
echo "[3/3] 执行自动化流程..."
echo ""
echo "-------------------------------------------------------------------"
echo "  将执行原 quark.py 工具:"
echo "  - 选项 1: 批量转存（自动从 url.txt 读取）"
echo "  - 选项 5: 下载到本地"
echo ""
echo "  ⚠️  由于夸克网盘限制，仍需手动操作:"
echo ""
echo "  【现在】:"
echo "    1. 运行: python quark.py"
echo "    2. 输入: 1 (批量转存)"
echo "    3. 等待转存完成"
echo ""
echo "  【然后】:"
echo "    1. 再次运行: python quark.py"
echo "    2. 输入: 5 (下载到本地)"
echo "    3. 输入下载路径: $SAVE_DIR"
echo "    4. 选择要下载的文件"
echo ""
echo "-------------------------------------------------------------------"
echo ""
echo "💡 快捷命令（复制粘贴）:"
echo ""
echo "  # 转存"
echo "  python quark.py  # 输入 1"
echo ""
echo "  # 下载"
echo "  python quark.py  # 输入 5 → 输入路径: $SAVE_DIR"
echo ""
echo "======================================================================"
echo "[完成] Cookie 和链接已准备好，请按上述步骤操作"
echo "======================================================================"

if __name__ == '__main__':
    main()
