#!/bin/bash
set -e

PROJECT_ROOT="${1:-.}"
cd "$PROJECT_ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 CodeGraph Booster - 智能初始化"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: 统计项目文件数
echo "[1/4] 分析项目规模..."
FILE_COUNT=$(find . -type f \( \
  -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.mjs" \
  -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \
  -o -name "*.cs" -o -name "*.php" -o -name "*.rb" -o -name "*.c" -o -name "*.cpp" \
  -o -name "*.swift" -o -name "*.kt" -o -name "*.dart" \
\) 2>/dev/null | wc -l | tr -d ' ')

echo "   源代码文件数: $FILE_COUNT"

# Step 2: 决策阈值检查
if [ "$FILE_COUNT" -lt 500 ]; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "⏭️  跳过 CodeGraph 初始化"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "原因: 项目规模 ($FILE_COUNT 文件) < 500 阈值"
  echo ""
  echo "💡 建议: 使用原生工具探索"
  echo "   • grep/Grep 工具搜索代码"
  echo "   • LSP 追踪定义/引用"
  echo "   • Read 直接阅读文件"
  echo ""
  echo "📊 CodeGraph 收益预估: <20% (初始化开销>收益)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 0
fi

echo "   ✓ 项目规模达标 (≥500 文件)"
echo "   预期收益: 30-50% 成本削减 | 70%+ 工具调用削减"

# Step 3: 检查现有索引
echo ""
echo "[2/4] 检查现有索引..."
if [ -d ".codegraph" ]; then
  echo "   ✓ 发现现有索引: .codegraph/"
  
  # 验证索引健康度
  if command -v codegraph &>/dev/null; then
    echo "   运行健康检查..."
    codegraph status 2>&1 | head -n 10 || echo "   ⚠️  索引可能损坏,建议重建"
  fi
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ CodeGraph 已就绪"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 0
fi

echo "   索引不存在,开始初始化..."

# Step 4: 安装 CodeGraph
echo ""
echo "[3/4] 安装 CodeGraph MCP Server..."
if ! command -v codegraph &>/dev/null; then
  echo "   正在下载安装脚本..."
  if [ "$(uname)" = "Darwin" ] || [ "$(uname)" = "Linux" ]; then
    curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
  else
    # Windows PowerShell
    echo "   Windows 系统检测到,请手动运行:"
    echo "   irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex"
    exit 1
  fi
else
  echo "   ✓ CodeGraph 已安装: $(codegraph --version 2>&1 | head -n1)"
fi

# Step 5: 初始化索引
echo ""
echo "[4/4] 构建代码索引..."
echo "   这可能需要 1-3 分钟,取决于项目大小..."
echo ""

codegraph init -i --quiet

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ CodeGraph 初始化完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 索引统计:"
codegraph status 2>&1 | grep -E "(symbols|edges|languages)" || true
echo ""
echo "💡 下一步:"
echo "   • Agent 将自动使用 CodeGraph 工具"
echo "   • Explore agent 会优先调用 codegraph_explore"
echo "   • 文件修改会自动同步到索引(2秒 debounce)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
