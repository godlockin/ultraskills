---
name: "media-downloader"
description: "Downloads high-quality video and audio from YouTube, Bilibili, and 1000+ other sites using yt-dlp. Invoke when user wants to archive media content."
version: 1.0.0
tags: [productivity, media, archiving, automation]
---

# Media Downloader

## 🎯 目标 (Goal)

To provide a reliable, high-quality, and versatile mechanism for downloading audio and video content from the web for offline archiving, research, or content creation usage.

## 🧠 核心理念 (Core Concepts)

- **Quality First**: Default to the highest available video/audio bitrate unless specified otherwise.
- **Universal Compatibility**: Leverage `yt-dlp`'s massive extractor library to support virtually any site.
- **Respectful Archiving**: Handle cookies and user-agent strings correctly to respect site policies and throttle limits.

## ⭐ 脚本优先原则

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 下载视频 | `python3 scripts/download.py <url>` | 手动拼 yt-dlp 参数 |
| 仅下载音频 | `python3 scripts/download.py <url> --audio-only` | — |
| 指定分辨率 | `python3 scripts/download.py <url> --quality 720` | — |

## 🚀 使用流程 (Workflow)

### 1. Analysis (分析)

Identify the source platform and media type.

- Is it a single video, a playlist, or a live stream?
- Does it require authentication (e.g., Bilibili 1080p+, YouTube Premium)?

### 2. Composition (构建命令)

Construct the optimized `yt-dlp` command.

- Select format (`-f "bv+ba/b"`).
- Set output template (`-o`).
- Add specific extractors (e.g., `--cookies-from-browser`).

### 3. Execution (执行)

Run the command and monitor for errors (geo-blocking, DRM).

## ✅ 检查清单 (Checklist)

- [ ] Is `yt-dlp` installed and updated? (`yt-dlp -U`)
- [ ] Is FFmpeg installed for merging video/audio streams?
- [ ] For Bilibili/YouTube, are cookies needed for 1080p?
- [ ] Is the output filename safe (no restricted characters)?
