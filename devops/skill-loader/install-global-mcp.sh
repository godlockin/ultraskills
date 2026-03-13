#!/bin/bash
# install-global-mcp.sh - 全局安装 Skills MCP Server

set -e

SKILL_LOADER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="${PYTHON_CMD:-python3}"

# 检测 Python 路径
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python not found. Please set PYTHON_CMD env var."
    exit 1
fi

PYTHON_PATH="$(which $PYTHON_CMD)"
echo "✓ 使用 Python: $PYTHON_PATH"

# 创建全局 MCP 配置
MCP_CONFIG="$HOME/.claude/mcp.json"

# 备份现有配置
if [ -f "$MCP_CONFIG" ]; then
    cp "$MCP_CONFIG" "${MCP_CONFIG}.bak"
    echo "✓ 已备份现有配置：${MCP_CONFIG}.bak"
fi

# 写入新配置
cat > "$MCP_CONFIG" << EOF
{
  "mcpServers": {
    "skills-discovery": {
      "command": "$PYTHON_PATH",
      "args": ["$SKILL_LOADER_DIR/mcp_server.py"],
      "cwd": "$SKILL_LOADER_DIR"
    }
  }
}
EOF

echo ""
echo "✅ 全局 MCP 配置已安装到：$MCP_CONFIG"
echo ""
echo "配置内容:"
cat "$MCP_CONFIG"
echo ""
echo "📝 下一步:"
echo "   1. 重启 Claude Code"
echo "   2. 运行 /mcp 确认 skills-discovery 已加载"
echo "   3. 使用 /search_skills query=\"...\" 搜索技能"
echo ""
echo "🔧 卸载命令:"
echo "   rm ~/.claude/mcp.json"
