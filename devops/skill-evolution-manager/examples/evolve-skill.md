# 示例：进化一个 Skill

## 场景

用户在使用 yt-dlp skill 时发现了一些问题和偏好，希望将这些经验保存到 skill 中，避免下次重复犯错。

## 用户反馈

> "yt-dlp 默认下载最高画质太慢了，我希望默认 1080p 就好。
> 另外在 Windows 上，ffmpeg 路径有空格时需要用引号包起来，这个坑害我调了半天。"

## 进化步骤

### 1. Agent 分析对话

Agent 识别出：

- **Preference**: 用户希望默认 1080p 画质
- **Fix**: Windows 下 ffmpeg 路径有空格需要引号

### 2. 构建经验 JSON

```json
{
  "preferences": [
    "默认下载 1080p 画质，不要最高画质"
  ],
  "fixes": [
    "Windows 下 ffmpeg 路径如果有空格，需要用双引号包裹"
  ],
  "custom_prompts": "下载前先确认用户期望的画质，默认推荐 1080p"
}
```

### 3. 持久化经验

```bash
python scripts/merge_evolution.py ~/.claude/skills/yt-dlp/ '{"preferences": ["默认下载 1080p 画质，不要最高画质"], "fixes": ["Windows 下 ffmpeg 路径如果有空格，需要用双引号包裹"], "custom_prompts": "下载前先确认用户期望的画质，默认推荐 1080p"}'
```

输出：

```
✅ Successfully merged evolution data for yt-dlp
```

### 4. 缝合到文档

```bash
python scripts/smart_stitch.py ~/.claude/skills/yt-dlp/
```

输出：

```
ℹ️  Appending new evolution section...
✅ Successfully stitched evolution data into /Users/xxx/.claude/skills/yt-dlp/SKILL.md
```

### 5. 查看结果

SKILL.md 末尾新增：

```markdown
## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.
> Last updated: 2024-01-15T10:30:00

### User Preferences
- 默认下载 1080p 画质，不要最高画质

### Known Fixes & Workarounds
- Windows 下 ffmpeg 路径如果有空格，需要用双引号包裹

### Custom Instruction Injection

下载前先确认用户期望的画质，默认推荐 1080p
```

## 后续更新

当 `skill-manager` 更新 yt-dlp 的 SKILL.md 时，这些经验可能被覆盖。
但因为 `evolution.json` 文件还在，只需运行：

```bash
python scripts/smart_stitch.py ~/.claude/skills/yt-dlp/
```

即可恢复所有用户经验！
