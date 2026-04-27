---
name: video-analyzer
description: 把一个本地视频文件拆成"转录稿 + 关键帧截图 + 章节摘要"。串联 mac-whisper（语音转文字）+ video-frame-extractor（关键帧/定时抽帧）+ LLM（分章节）。一条命令产出 Markdown 报告。Trigger on 视频拆解 / 视频分析 / video summary / video chapters / 提取视频要点 / video-to-notes / 视频转笔记。
version: 1.0.0
created_at: 2026-04-27
entry_point: scripts/analyze.sh
dependencies: ["mac-whisper skill", "video-frame-extractor skill", "ffmpeg", "python>=3.9"]
tags: [video, analysis, summary, transcription, chapters, multimodal]
---

# video-analyzer

输入一个 mp4/mov/mkv → 输出一个 Markdown 报告：

```
report/
├── transcript.txt       # 全文字幕（mac-whisper）
├── transcript.srt       # 带时间戳
├── frames/              # 关键帧截图（默认场景检测）
│   ├── 00_00_05_120.jpg
│   └── ...
├── chapters.json        # 自动分章节 + 时间戳 + 关键帧
└── REPORT.md            # 整合报告：章节 / 摘要 / 截图 / 引文
```

## 何时用

- 长视频拆解笔记（讲座/会议/podcast）
- 给 PPT/博客做截图选材
- 找视频里某句话出现的时间点
- 给团队做视频内容审查报告

## 何时不用

- 视频里没语音 → 用 [`video-frame-extractor`](../video-frame-extractor/) 单独抽帧
- 只要字幕 → 用 [`mac-whisper`](../mac-whisper/) 直接转录
- 实时直播流 → 不适合（本工具是批处理）

## 依赖的其他 skill

| Skill | 角色 |
|---|---|
| [`mac-whisper`](../mac-whisper/) | 语音 → 文字（带时间戳）|
| [`video-frame-extractor`](../video-frame-extractor/) | 关键帧 / 场景切分 / 定时截图 |
| LLM (Claude/GPT) | 章节划分 + 摘要 |

## Quick Start

```bash
# 一次性安装（会调用上面两个 skill 的 install.sh）
bash scripts/install.sh

# 默认：场景检测抽帧 + whisper 转写 + LLM 分章节
bash scripts/analyze.sh lecture.mp4 -o lecture_report/

# 指定语言 + 抽帧策略
bash scripts/analyze.sh talk.mp4 \
  --lang zh \
  --frame-mode scene \
  --scene-threshold 0.3 \
  -o talk_report/

# 跳过 LLM 章节（仅转写 + 抽帧）
bash scripts/analyze.sh raw.mp4 --no-chapters -o raw/

# 给 LLM 用本地 ollama
bash scripts/analyze.sh in.mp4 --llm ollama --llm-model qwen2.5:14b -o out/
```

## CLI 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `-o, --output <dir>` | `<video>_report/` | 输出目录 |
| `--lang <code>` | auto | whisper 语言（zh/en/ja/...） |
| `--whisper-model` | `mlx-community/whisper-large-v3-turbo` | 转写模型 |
| `--frame-mode <m>` | `scene` | scene / fps / keyframes / timestamps |
| `--fps <n>` | 1 (mode=fps 时) | 每秒抽 n 张 |
| `--scene-threshold <f>` | 0.3 | 场景检测阈值（0–1） |
| `--max-frames <n>` | 100 | 抽帧上限 |
| `--llm <provider>` | `claude-cli` | claude-cli / openai / ollama / none |
| `--llm-model <id>` | provider-default | 例如 gpt-4o-mini / qwen2.5:14b |
| `--no-chapters` | off | 跳过章节划分 |
| `--keep-audio` | off | 保留中间音频文件 |

## Workflow

```
            ┌──────────────────┐
input.mp4 ──┤ 1) ffmpeg → wav  │── audio.wav
            └──────────────────┘
                       │
            ┌──────────┴────────┐
            │                   │
   ┌────────▼────────┐  ┌──────▼─────────────┐
   │ 2) mac-whisper  │  │ 3) frame-extractor │
   │  → transcript   │  │  → frames/*.jpg     │
   │  + segments.json│  │  + frames.json      │
   └────────┬────────┘  └──────┬─────────────┘
            │                  │
            └────────┬─────────┘
                     ▼
         ┌────────────────────────┐
         │ 4) LLM chapterize      │
         │   - 输入: transcript   │
         │     + frame timestamps │
         │   - 输出: chapters.json│
         └────────┬───────────────┘
                  ▼
         ┌────────────────────┐
         │ 5) 渲染 REPORT.md   │
         │   章节 + 截图 + 引文 │
         └────────────────────┘
```

## 输出报告示例

```markdown
# REPORT — lecture.mp4
duration: 47:23 · language: zh · 8 chapters · 32 frames

## 1. 引言（00:00–03:21）
讲者介绍背景，强调三个核心问题。
![](frames/00_00_12_400.jpg)
> "今天我们要讨论的，是为什么 AI 还做不好长任务……"

## 2. 历史回顾（03:21–11:50）
...
```

## 与其他 skill 组合

```bash
# 1) 拆解 → 生成博客
bash scripts/analyze.sh talk.mp4 -o out/
# 然后让 magazine-web-ppt 把 REPORT.md 转成网页 PPT

# 2) 拆解 → 重配音
bash scripts/analyze.sh talk.mp4 -o out/
bash ~/.../mac-tts/scripts/tts.sh out/transcript.txt --voice zh-CN-YunxiNeural -o redub.mp3

# 3) 拆解 → 用我自己的声音重配
bash ~/.../mac-voice-clone/scripts/clone.sh --ref-audio me.wav \
  --ref-text "$(head -c 200 ref.txt)" --text "$(cat out/transcript.txt)" -o redub.wav
```

## License

This skill: MIT
