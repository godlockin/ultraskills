# 示例：检查 Skills 更新

## 场景

定期检查已安装的 GitHub Skills 是否有新版本可用。

## 执行步骤

### 1. 运行扫描检查

```bash
python scripts/scan_and_check.py ~/.claude/skills/
```

### 2. 输出示例

```json
[
  {
    "name": "yt-dlp",
    "dir": "/Users/xxx/.claude/skills/yt-dlp",
    "github_url": "https://github.com/yt-dlp/yt-dlp",
    "local_hash": "abc123def456",
    "local_version": "0.1.0",
    "remote_hash": "789xyz000111",
    "status": "outdated",
    "message": "New commits available"
  },
  {
    "name": "ffmpeg-tool",
    "dir": "/Users/xxx/.claude/skills/ffmpeg-tool",
    "github_url": "https://github.com/FFmpeg/FFmpeg",
    "local_hash": "111222333444",
    "local_version": "0.2.0",
    "remote_hash": "111222333444",
    "status": "current",
    "message": "Up to date"
  }
]
```

### 3. 更新过时的 Skill

发现 `yt-dlp` 过时后，执行更新流程：

```bash
# Step 1: 备份
python scripts/update_helper.py ~/.claude/skills/yt-dlp/

# Step 2: 获取新信息 (使用 github-to-skills)
python ../github-to-skills/scripts/fetch_github_info.py https://github.com/yt-dlp/yt-dlp > /tmp/new_info.json

# Step 3: Agent 分析差异并更新 SKILL.md

# Step 4: 对齐经验 (使用 skill-evolution-manager)
python ../skill-evolution-manager/scripts/smart_stitch.py ~/.claude/skills/yt-dlp/
```

## 自动化提示

可以设置定时任务每周运行一次检查：

```bash
# 添加到 crontab
0 9 * * 1 python /path/to/scan_and_check.py ~/.claude/skills/ > /tmp/skill_status.json
```
