# AI Stats - AI 使用量统计

## 安装

```bash
# 1. 安装依赖
cd ~/.claude/stats
pip3 install -r requirements.txt

# 2. 重新加载 shell 配置
source ~/.zshrc

# 3. 安装定时任务（每天凌晨 3:00 自动采集）
./install-cron.sh
```

## 命令

### 基本命令

```bash
aistats              # 查看今日 Markdown 报表
aistats collect      # 采集数据到数据库
aistats-web          # 启动 Web 界面 (http://localhost:5000)
aistats-add --tool Trae --credits 500  # 添加手动记录
```

### CLI 统计命令

```bash
aistats-cli summary              # 本月汇总统计
aistats-cli summary --period all # 全部历史统计
aistats-cli today                # 今日统计
aistats-cli tools                # 列出所有工具
aistats-cli models               # 列出所有模型
aistats-cli export --period monthly  # 导出 JSON 数据
```

## 文件结构

```
~/.claude/stats/
├── collector.py       # 数据采集
├── web.py             # Web 服务
├── cli.py             # CLI 统计工具
├── collect-daily.sh   # 定时任务脚本
├── install-cron.sh    # 安装定时任务
├── ai_usage.db        # SQLite 数据库
└── static/index.html  # Web 前端
```
