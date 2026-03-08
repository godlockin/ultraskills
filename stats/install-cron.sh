#!/bin/bash
# 安装定时任务 - AI 使用量统计
# 每天凌晨 3:00 自动采集统计数据

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTOR_SCRIPT="$SCRIPT_DIR/collect-daily.sh"
PLIST_FILE="$HOME/Library/LaunchAgents/com.claude.ai-stats.plist"
LOG_FILE="$SCRIPT_DIR/cron.log"
ERR_FILE="$SCRIPT_DIR/cron.err"

# 检查脚本是否存在
if [ ! -f "$COLLECTOR_SCRIPT" ]; then
    echo "❌ 脚本不存在：$COLLECTOR_SCRIPT"
    exit 1
fi

# 添加执行权限
chmod +x "$COLLECTOR_SCRIPT"

# 创建日志文件（确保 launchd 有写入权限）
touch "$LOG_FILE" "$ERR_FILE"
chmod 644 "$LOG_FILE" "$ERR_FILE"

# 创建 launchd plist 文件
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.ai-stats</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$COLLECTOR_SCRIPT</string>
    </array>
    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>
    <key>StandardErrorPath</key>
    <string>$ERR_FILE</string>
    <key>RunAtLoad</key>
    <false/>
    <key>CalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
EOF

# 卸载旧的（如果存在）
launchctl unload "$PLIST_FILE" 2>/dev/null || true

# 等待一下再加载
sleep 0.5

# 加载新的
launchctl load "$PLIST_FILE"

echo "✅ 已安装定时任务：每天凌晨 3:00 自动采集数据"
echo ""
echo "查看定时任务状态：launchctl list | grep claude"
echo "查看采集日志：tail -f $LOG_FILE"
echo ""
echo "手动运行一次测试：bash $COLLECTOR_SCRIPT"
