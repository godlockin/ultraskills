---
name: Media Downloader
description: 使用 yt-dlp 下载网络视频/音频，涵盖 YouTube、Bilibili 等主流平台，处理认证、格式选择、合并等完整流程
version: 1.0.0
tags: [yt-dlp, youtube, bilibili, ffmpeg, media, download]
---

# Media Downloader

> 使用 yt-dlp 从 YouTube、Bilibili、Twitter 等 1000+ 平台下载最高画质视频/音频，自动处理 bot 检测、格式合并、Cookie 认证。

## 🎯 目标 (Goal)

* 最高画质下载（自动选择最佳 video+audio 流）
* 绕过 bot 检测（Cookie 认证）
* 自动合并视频+音频流（FFmpeg）
* 支持单视频、播放列表、直播回放

## 🧠 核心理念 (Core Concepts)

**为什么需要 Cookie？**
YouTube 等平台检测无 Cookie 的请求为爬虫行为，返回 "Sign in to confirm you're not a bot" 错误。需要从已登录浏览器提取 Cookie 传给 yt-dlp。

**视频+音频分流**
现代平台（YouTube 1080p+）将视频流和音频流分开存储。yt-dlp 下载后需要 FFmpeg 合并。`-f "bv+ba/b"` 格式选择器：优先分流 best video + best audio，回退到单流 best。

**格式 ID vs 格式选择器**
- 通用：`-f "bv+ba/b"` 自动选最佳
- 指定画质：`-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]"`
- 仅音频：`-f "ba/b"` + `-x --audio-format mp3`

## 🚀 使用流程 (Workflow)

### Step 1: 环境检查

```bash
# 验证工具安装
yt-dlp --version          # 需要较新版本（2024+）
ffmpeg -version           # 合并视频+音频必须
which yt-dlp              # 确认路径正确

# 更新 yt-dlp（平台经常更新反爬策略）
yt-dlp -U
```

### Step 2: 先获取视频信息（可选但推荐）

```bash
# 列出所有可用格式（不下载）
yt-dlp --list-formats "URL"

# 获取视频标题、时长、上传者等元数据
yt-dlp --dump-json "URL" | jq '{title, duration, uploader}'
```

### Step 3: 构建下载命令

**标准下载（最高画质）**：
```bash
yt-dlp \
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  -o "%(title)s.%(ext)s" \
  "URL"
```

**需要认证时（YouTube bot 检测）**：
```bash
# 方式一：从浏览器提取 Cookie（推荐）
yt-dlp \
  --cookies-from-browser chrome \   # 或 firefox / safari / edge
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  -o "%(title)s.%(ext)s" \
  "URL"

# 方式二：导出 Cookie 文件
# 浏览器安装 "Get cookies.txt LOCALLY" 扩展，导出 cookies.txt
yt-dlp \
  --cookies cookies.txt \
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  "URL"
```

**指定输出目录**：
```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  -o "~/Downloads/%(uploader)s/%(title)s.%(ext)s" \
  "URL"
```

**下载播放列表**：
```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  -o "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s" \
  --yes-playlist \
  "PLAYLIST_URL"
```

**仅提取音频（MP3）**：
```bash
yt-dlp \
  --cookies-from-browser chrome \
  -x --audio-format mp3 --audio-quality 0 \
  -o "%(title)s.%(ext)s" \
  "URL"
```

**限速（避免触发速率限制）**：
```bash
yt-dlp \
  --cookies-from-browser chrome \
  --rate-limit 2M \          # 限制 2MB/s
  --sleep-interval 2 \       # 请求间隔 2s
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  "URL"
```

### Step 4: 验证结果

```bash
# 检查文件完整性
ls -lh "%(title)s.mp4"

# 用 ffprobe 检查视频信息
ffprobe -v quiet -print_format json -show_format -show_streams "file.mp4" | jq '{duration: .format.duration, size: .format.size}'
```

## ⚠️ 常见错误与解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Sign in to confirm you're not a bot` | YouTube bot 检测 | 添加 `--cookies-from-browser chrome` |
| `ERROR: Unable to extract ...` | yt-dlp 版本过旧，平台更新了 | `yt-dlp -U` 更新 |
| `Requested format is not available` | 指定格式不存在 | 用 `--list-formats` 查看可用格式 |
| `ffmpeg not found` | 未安装 FFmpeg | `brew install ffmpeg`（Mac）/ `apt install ffmpeg`（Linux）|
| `403 Forbidden` | IP 被封 / 需要登录内容 | 换网络 / 用 cookies 认证 |
| `Video unavailable` | 地区限制 | 配合 VPN 或代理：`--proxy socks5://127.0.0.1:1080` |
| 下载速度极慢（< 100KB/s） | YouTube 速率限制（常见） | 正常现象，等待或重试；或用 `--concurrent-fragments 4` |
| `Name collision` (rtk) | rtk 命令冲突 | 直接用 `/usr/local/bin/yt-dlp` 绝对路径 |

## 💡 最佳实践 (Best Practices)

**Do**:
- 下载前用 `--list-formats` 确认格式可用
- 用 `%(title)s` 模板命名，避免硬编码文件名
- 大文件下载加 `--no-part`（断点续传时用原文件名）
- 定期 `yt-dlp -U` 更新（平台反爬更新频繁）
- YouTube 1080p+ 必须分流下载，务必安装 FFmpeg

**Don't**:
- 不要同时开多个并发下载（触发速率限制）
- 不要跳过格式选择器（默认可能不是最高画质）
- 不要在公共/公司网络下载（IP 封禁风险）
- 不要将 cookies.txt 提交到 git

## 🖥️ 平台特化命令

### Bilibili（B站）

```bash
# B站 1080p+ 需要大会员 Cookie
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  --merge-output-format mp4 \
  -o "%(title)s.%(ext)s" \
  "https://www.bilibili.com/video/BVxxxxxxxx"
```

### Twitter / X

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  "https://twitter.com/xxx/status/xxx"
```

### 通用平台（Instagram、TikTok 等）

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -o "%(uploader)s_%(title)s.%(ext)s" \
  "URL"
```

## 📚 资源引用

* [yt-dlp 官方 GitHub](https://github.com/yt-dlp/yt-dlp)
* [Cookie 导出指南](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
* [YouTube Cookie 特别说明](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)
* [格式选择器文档](https://github.com/yt-dlp/yt-dlp#format-selection)
