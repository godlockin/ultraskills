#!/bin/bash
# AI 使用量数据采集 - 定时任务脚本
# 每天运行一次，采集各工具的 token/credit 使用量

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTOR_PY="$SCRIPT_DIR/collector.py"
AI_STATS_DIR="$HOME/.claude/ai-stats"

# 确保数据库已初始化
python3 "$COLLECTOR_PY" init

# 采集自动数据（Claude Code 等）
python3 "$COLLECTOR_PY" collect

# 同步手动记录文件到数据库
# 优先使用 ~/.claude/ai-stats/manual_usage.json，如果不存在则使用脚本目录下的
if [ -f "$AI_STATS_DIR/manual_usage.json" ]; then
    MANUAL_FILE="$AI_STATS_DIR/manual_usage.json"
elif [ -f "$SCRIPT_DIR/manual_usage.json" ]; then
    MANUAL_FILE="$SCRIPT_DIR/manual_usage.json"
else
    MANUAL_FILE=""
fi

if [ -n "$MANUAL_FILE" ] && [ -f "$MANUAL_FILE" ]; then
    echo "📖 读取手动记录文件：$MANUAL_FILE"
    # 读取所有日期的手动记录并同步到数据库（不仅是今天）
    jq -r '.daily[] | .date as $date | .tools[] | "\($date) \(.name) \(.credits)"' "$MANUAL_FILE" 2>/dev/null | while read -r line; do
        date=$(echo "$line" | awk '{print $1}')
        tool=$(echo "$line" | awk '{print $2}')
        credits=$(echo "$line" | awk '{print $3}')
        if [ -n "$date" ] && [ -n "$tool" ] && [ -n "$credits" ]; then
            python3 "$COLLECTOR_PY" add --tool "$tool" --credits "$credits" --date "$date"
        fi
    done
    echo "✅ 手动记录已同步到数据库"
fi

echo "✅ 数据采集完成 ($(date '+%Y-%m-%d %H:%M:%S'))"
