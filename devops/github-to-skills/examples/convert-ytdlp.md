# 示例：将 yt-dlp 转换为 Skill

## 场景

将流行的视频下载工具 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 封装为 AI Skill，使 AI 助手能够帮助用户下载视频。

## 执行步骤

### 1. 获取仓库信息

```bash
python scripts/fetch_github_info.py https://github.com/yt-dlp/yt-dlp > /tmp/ytdlp_info.json
```

输出示例：

```json
{
  "name": "yt-dlp",
  "url": "https://github.com/yt-dlp/yt-dlp",
  "latest_hash": "2024.08.06",
  "readme": "# yt-dlp\n\nA feature-rich command-line audio/video downloader..."
}
```

### 2. 生成 Skill 脚手架

```bash
python scripts/create_github_skill.py /tmp/ytdlp_info.json ~/.claude/skills/
```

输出：

```
✅ Skill scaffolded at: /Users/xxx/.claude/skills/yt-dlp

📋 Next steps:
1. Review SKILL.md and refine the description
2. Implement the actual logic in scripts/wrapper.py
3. Add real examples to examples/
```

### 3. 生成的目录结构

```
~/.claude/skills/yt-dlp/
├── SKILL.md              # 包含 github_url 和 github_hash
├── scripts/
│   └── wrapper.py        # 待实现的调用逻辑
├── examples/
│   └── basic-usage.md    # 基础示例模板
└── references/           # 参考文档目录
```

### 4. 实现 wrapper.py

编辑 `scripts/wrapper.py`，实现实际的调用逻辑：

```python
#!/usr/bin/env python3
import subprocess
import sys

def download_video(url: str, output_dir: str = "."):
    """下载视频到指定目录。"""
    cmd = [
        "yt-dlp",
        "-o", f"{output_dir}/%(title)s.%(ext)s",
        url
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wrapper.py <video_url> [output_dir]")
        sys.exit(1)
    
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "."
    download_video(url, output)
```

## 结果

现在 AI 助手可以通过自然语言触发此 Skill：

> "帮我下载这个视频: <https://www.youtube.com/watch?v=xxx>"

AI 将调用 yt-dlp Skill 完成下载任务。
