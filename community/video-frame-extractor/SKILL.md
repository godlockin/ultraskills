---
name: "video-frame-extractor"
description: "Extract image frames from video files via ffmpeg. Modes: at exact timestamps, at fixed FPS, every N seconds, all frames, keyframes only, or scene changes. Trigger on 抽帧 / extract frames / video to images / screenshot from video / 截图视频帧 / 指定时间抽帧."
version: 1.1.0
updated_at: 2026-04-25
tags: [video, ffmpeg, frame, image, extract, screenshot]
---

# Video Frame Extractor

Extract images from video using `ffmpeg`. Six modes — pick by intent.

## Prerequisites

`ffmpeg` installed (`brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux).

## Mode picker

| 用户意图 | 用 Mode |
|---|---|
| "抽第 1:23 处那一帧 / 截图这个时间点" | **1. 时间戳** |
| "抽 5s / 10s / 30s 这几个位置" | **2. 多时间戳** |
| "每秒一张 / 每 5 秒一张" | **3. 固定 FPS** |
| "把整段视频抽成图" | **4. 全部帧** ⚠️ 大 |
| "只抽场景变化点" | **5. 场景检测** |
| "只抽关键帧 (I-frame)" | **6. 关键帧** |

---

## Mode 1 · 指定时间戳（精确单帧）

```bash
# 把 -ss 放在 -i 前 = 快速 seek (less precise on some codecs)
# 把 -ss 放在 -i 后 = 精确 seek (decode from start, slower but frame-accurate)
ffmpeg -ss 00:01:23.456 -i video.mp4 -frames:v 1 -q:v 2 out.jpg

# 帧精确版（推荐用于剪辑/分析）
ffmpeg -i video.mp4 -ss 00:01:23.456 -frames:v 1 -q:v 2 out.jpg
```

时间格式：`HH:MM:SS.mmm` 或纯秒 `83.456`。
`-q:v 2` = JPEG 高质量（1=最好，31=最差）；要无损用 PNG：去掉 `-q:v` 改 `out.png`。

## Mode 2 · 多个指定时间戳

**方案 A — 循环（最简单、可靠）：**
```bash
for t in 5 10 30 75.5; do
  ffmpeg -ss "$t" -i video.mp4 -frames:v 1 -q:v 2 "frame_${t}s.jpg"
done
```

**方案 B — 单次 ffmpeg 调用（用 select filter）：**
```bash
ffmpeg -i video.mp4 -vf "select='eq(t,5)+eq(t,10)+eq(t,30)+eq(t,75.5)'" \
       -vsync vfr -q:v 2 frame_%03d.jpg
```
注意：`eq(t,5)` 要求时间正好是 5.0；如果取不到帧，把表达式改成 `between(t,5,5.05)` 容错 50ms。

## Mode 3 · 固定 FPS（按节奏抽样）

```bash
ffmpeg -i video.mp4 -vf fps=1     frame_%04d.jpg   # 每秒 1 张
ffmpeg -i video.mp4 -vf fps=0.5   frame_%04d.jpg   # 每 2 秒 1 张
ffmpeg -i video.mp4 -vf fps=1/5   frame_%04d.jpg   # 每 5 秒 1 张
ffmpeg -i video.mp4 -vf fps=2     frame_%04d.jpg   # 每秒 2 张
```

## Mode 4 · 全部帧 ⚠️

```bash
ffmpeg -i video.mp4 frame_%06d.png
```
30fps 1 小时视频 = 108000 张图，几十 GB。**用前确认。**

## Mode 5 · 场景变化（自动找镜头切换）

```bash
# 阈值 0.4 = 中等敏感；0.2 更敏感，0.6 更保守
ffmpeg -i video.mp4 -vf "select='gt(scene,0.4)',showinfo" \
       -vsync vfr -q:v 2 scene_%03d.jpg
```
`showinfo` 会把每张抽到的帧的 PTS（时间）打到 stderr，便于回查时间点。

## Mode 6 · 关键帧 (I-frame)

```bash
ffmpeg -i video.mp4 -vf "select='eq(pict_type,PICT_TYPE_I)'" \
       -vsync vfr -q:v 2 keyframe_%03d.jpg
```

---

## 通用选项

| 需求 | 加这个 |
|---|---|
| 限制输出张数 | `-frames:v N` |
| 缩放（宽 720，高自适应） | `-vf "scale=720:-2"`（与 `select`/`fps` 链接：`-vf "fps=1,scale=720:-2"`） |
| 输出 PNG 无损 | 改后缀 `.png`，去掉 `-q:v` |
| 输出 WebP | 改后缀 `.webp`，加 `-quality 85` |
| 提速（仅当不需要帧精确） | `-ss` 放 `-i` 前 |
| 处理一段区间 | `-ss <start> -to <end>` |

## Workflow（建议执行顺序）

1. **确认输入**：用户给 `video.mp4` 路径，必要时 `ffprobe -i video.mp4` 看时长/帧率
2. **确定模式**：按 Mode picker 选
3. **建输出目录**：`mkdir -p frames/`
4. **跑命令**：套上面模板，路径加引号
5. **回报**：列出生成数量 + 大小（`ls -la frames/ | wc -l && du -sh frames/`）

## Examples

```bash
# 抽 1:23 那一帧
ffmpeg -ss 00:01:23 -i lecture.mp4 -frames:v 1 -q:v 2 cover.jpg

# 视频开头每 10 秒抽一张，存到 thumbs/
mkdir -p thumbs
ffmpeg -i lecture.mp4 -t 600 -vf "fps=1/10,scale=480:-2" thumbs/t_%04d.jpg

# 找所有镜头切换点
mkdir -p scenes
ffmpeg -i film.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr scenes/s_%03d.jpg 2>scenes.log
grep "pts_time" scenes.log | awk '{print $4}'   # 列出每张的时间戳
```
