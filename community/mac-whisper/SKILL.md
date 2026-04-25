---
name: mac-whisper
description: 在 Apple Silicon Mac (M1/M2/M3/M4) 本地跑 SOTA 语音转文字（Whisper large-v3-turbo via MLX）。用于将音频/视频转成文本/SRT/VTT/JSON。10-20× 实时速度，99 语言（含中英文），完全离线。Trigger on 语音转文字 / transcribe / audio to text / SRT / 字幕生成 / speech-to-text / ASR / 听写。
version: 1.0.0
created_at: 2026-04-25
entry_point: scripts/transcribe.sh
dependencies: ["python>=3.9", "ffmpeg (for non-wav input)"]
backends: ["mlx-whisper (preferred)", "whisper.cpp (fallback)"]
tags: [asr, speech-to-text, whisper, mlx, transcription, srt, subtitles, mac, apple-silicon]
---

# mac-whisper

Apple Silicon 本地 SOTA 语音转文字 skill。封装两条路径：
- **首选 `mlx-whisper`** — Apple 官方 MLX 框架，M 系列最快（~10–20× 实时）
- **回退 `whisper.cpp`** — 不想装 Python 的纯 C++ 路线（`brew install whisper-cpp`）

默认模型：`mlx-community/whisper-large-v3-turbo`（~2GB，准确率近 large-v3，速度快 8×）。

## When to use

- 用户给一段音频/视频要文字稿
- 要 SRT/VTT 字幕（自动加时间戳）
- 要中文、多语种识别
- 要本地、隐私敏感、不想走 OpenAI API

## When NOT to use

- 需要词级时间戳 + 说话人分离 → 用 WhisperX
- 需要超低延迟流式 (<200ms) → 用 NVIDIA Parakeet streaming（Mac 跑不了）
- 中文场景且要情感/事件标注 → 考虑 SenseVoice / FunASR

## Quick Start

```bash
# 一次性安装（首跑会自动下载模型）
pip install -U mlx-whisper

# 转写（自动检测语言）
bash scripts/transcribe.sh audio.mp3

# 指定中文，输出 SRT 字幕
bash scripts/transcribe.sh audio.mp3 --lang zh --format srt

# 指定输出目录
bash scripts/transcribe.sh audio.mp3 --out ./out
```

## Workflow

### Step 1 · 检查输入

支持任何 ffmpeg 能解的格式（mp3/m4a/wav/mp4/mov/mkv/...）。视频会自动抽音轨。
**长音频建议先切片**（>1h）以便重试与并行。

### Step 2 · 选模型

| 模型 | 大小 | 速度 (M2) | 适用 |
|---|---|---|---|
| `whisper-large-v3-turbo` ⭐ | ~1.5GB | 10–20× 实时 | **默认**，质量/速度最佳平衡 |
| `whisper-large-v3` | ~3GB | 5–8× 实时 | 多语种最高准确率 |
| `whisper-medium` | ~800MB | 15–25× 实时 | 内存紧张时 |
| `whisper-small` | ~250MB | 30–50× 实时 | 实时/轻量场景 |

切换：`--model mlx-community/whisper-large-v3`

### Step 3 · 转写

```bash
bash scripts/transcribe.sh <audio> [--lang zh|en|...] [--format txt|srt|vtt|json|all] [--model <hf_repo>] [--out <dir>]
```

### Step 4 · 输出

默认在音频同目录生成 `<basename>.<format>`。`--format all` 同时输出 txt+srt+vtt+json。

## Files

```
mac-whisper/
├── SKILL.md              ← 本文件
├── README.md             ← 使用速记
└── scripts/
    ├── transcribe.sh     ← 主入口（自动选 backend）
    └── install.sh        ← 一次性安装 mlx-whisper / whisper-cpp
```

## Tips

- **首跑慢**：第一次会下模型（~1.5GB），后续从 `~/.cache/huggingface/` 走
- **中文标点**：mlx-whisper 自带，如不理想加 `--initial-prompt "以下是普通话内容,带标点。"`
- **降噪**：极脏音频先 `ffmpeg -af "afftdn,highpass=f=80"` 处理
- **批量**：`for f in *.m4a; do bash scripts/transcribe.sh "$f" --format srt; done`

## License

- This skill: MIT
- mlx-whisper: MIT (Apple)
- Whisper weights: MIT (OpenAI)
