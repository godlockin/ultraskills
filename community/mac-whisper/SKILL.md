---
name: mac-whisper
description: 在 Apple Silicon Mac (M1/M2/M3/M4) 本地跑 SOTA 语音转文字（Whisper large-v3-turbo via MLX）。用于将音频/视频转成文本/SRT/VTT/JSON。10-20× 实时速度，99 语言（含中英文），完全离线。Trigger on 语音转文字 / transcribe / audio to text / SRT / 字幕生成 / speech-to-text / ASR / 听写。
version: 1.1.0
created_at: 2026-04-25
entry_point: scripts/transcribe.sh
dependencies: ["python>=3.9", "ffmpeg (for non-wav input)"]
backends: ["mlx-whisper (arm64 only, preferred)", "faster-whisper (cross-platform fallback)", "whisper.cpp (offline, low-RAM)"]
tags: [asr, speech-to-text, whisper, mlx, transcription, srt, subtitles, mac, apple-silicon]
---

# mac-whisper

Apple Silicon 本地 SOTA 语音转文字 skill。封装三条路径，按平台自动选择：
- **首选 `mlx-whisper`** — Apple 官方 MLX 框架，M 系列最快（~10–20× 实时；**仅 arm64 原生 Python**）
- **自动回退 `faster-whisper`** — CTranslate2 后端，x86_64 / arm64 / Linux 全平台，速度约 3–5× 实时
- **离线兜底 `whisper.cpp`** — 纯 C++ 二进制，低内存（`brew install whisper-cpp`）

默认模型：`mlx-community/whisper-large-v3-turbo`（~2GB，准确率近 large-v3，速度快 8×）。`faster-whisper` 走 `Systran/faster-whisper-large-v3`（已本地缓存时直接用）。

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
# 一次性安装（自动选 backend：mlx → faster → cpp）
bash scripts/install.sh

# 转写（自动检测 backend + 语言）
bash scripts/transcribe.sh audio.mp3

# 指定中文，输出 SRT 字幕
bash scripts/transcribe.sh audio.mp3 --lang zh --format srt

# 强制用 faster-whisper 跑 MPS GPU（float16）
bash scripts/transcribe.sh audio.mp3 --backend faster --compute-type float16

# 用小模型快速草稿
bash scripts/transcribe.sh audio.mp3 --model Systran/faster-whisper-small

# 完整 flag 列表：bash scripts/transcribe.sh --help
```

## CLI Flags

| Flag | 取值 | 默认 | 说明 |
|---|---|---|---|
| `--lang` | `zh`/`en`/`ja`/... | auto | 强制语言，省去检测 |
| `--format` | `txt`/`srt`/`vtt`/`json`/`all` | `txt` | 输出格式；`all` 一次出 4 种 |
| `--model` | HF repo id | 按 backend 选 | 覆盖默认模型（见下表） |
| `--backend` | `mlx`/`faster`/`cpp` | auto | 强制后端；不合法或不可用会报错 |
| `--compute-type` | `int8`/`float16`/`float32` | `int8` | faster-whisper 专用；`float16` 跑 GPU/MPS |
| `--out` | 路径 | 同输入目录 | 输出目录 |
| `--prompt` | 文本 | — | 初始 prompt（改善中文标点/术语） |

**默认模型 per backend**（不传 `--model` 时）：

| Backend | 默认模型 | 大小 | 速度 (M2) |
|---|---|---|---|
| mlx | `mlx-community/whisper-large-v3-turbo` | ~1.5GB | 10–20× 实时 |
| faster | `Systran/faster-whisper-large-v3` | ~3GB | 3–5× 实时 (CPU int8) |
| cpp | `$WHISPER_CPP_MODEL` 或 `~/.cache/whisper.cpp/ggml-large-v3-turbo-q5_0.bin` | ~570MB | 2–4× 实时 |

## Workflow

### Step 1 · 检查输入

支持任何 ffmpeg 能解的格式（mp3/m4a/wav/mp4/mov/mkv/...）。视频会自动抽音轨。
**长音频建议先切片**（>1h）以便重试与并行。

### Step 2 · 选模型

| 模型 | 大小 | 速度 (M2) | 适用 |
|---|---|---|---|
| `whisper-large-v3-turbo` ⭐ | ~1.5GB | 10–20× 实时 | **默认（mlx）**，质量/速度最佳平衡 |
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
    ├── transcribe.sh     ← 主入口（自动选 backend：mlx → faster → cpp）
    └── install.sh        ← 一次性安装（按环境自动选 backend）
```

## Environment & Backend Selection

`transcribe.sh` 启动时会自动探测，按以下顺序选择 backend：

| 条件 | Backend | 速度 | 备注 |
|---|---|---|---|
| `uname -m=arm64` 且 Python 也是 `arm64` 原生 + `mlx_whisper` 已装 | **mlx-whisper** | 10–20× 实时 | 最快，但 mlx 不支持 Rosetta x86_64 |
| `faster_whisper` Python 包已装 | **faster-whisper** | 3–5× 实时（CPU int8） | 跨平台兜底，x86_64/Linux 唯一选择 |
| `whisper-cli` 或 `whisper-cpp` 已装 | **whisper.cpp** | 2–4× 实时 | 离线、低内存；需手动下 ggml 模型 |

**触发自动降级的常见情况**：
1. 当前 shell 的 `python3` 是 x86_64（Rosetta）— mlx 装不上也跑不了 → 自动走 faster-whisper
2. macOS 上没装 MLX 框架（`pip install mlx-whisper` 失败）→ 跳过 mlx，尝试 faster-whisper
3. Linux 服务器 / CI 环境 → 直接 faster-whisper
4. 啥都没装 → 报错并提示 `bash scripts/install.sh`

**手动指定 backend**（一般不需要）：用 `--backend` flag。
```bash
# 强制 faster-whisper 跑 GPU
bash scripts/transcribe.sh audio.mp3 --backend faster --compute-type float16

# 强制 whisper.cpp（低内存 / 完全离线）
bash scripts/transcribe.sh audio.mp3 --backend cpp --lang zh

# 强制 mlx（不兼容时会清晰报错）
bash scripts/transcribe.sh audio.mp3 --backend mlx
```
不合法（backend 拼错、backend 不可用、mlx 在 x86_64 上）时脚本会立即报错并指出原因。

**自检脚本**（排查"为什么没走 mlx"）：
```bash
uname -m                                        # 期望 arm64
python3 -c "import platform; print(platform.machine())"  # 期望 arm64
which mlx_whisper && mlx_whisper --help | head -3
```

## Tips

- **首跑慢**：第一次会下模型（~1.5GB），后续从 `~/.cache/huggingface/` 走
- **中文标点**：mlx-whisper 自带；faster-whisper 也支持，可加 `--prompt "以下是普通话内容,带标点。"`
- **降噪**：极脏音频先 `ffmpeg -af "afftdn,highpass=f=80"` 处理
- **批量**：`for f in *.m4a; do bash scripts/transcribe.sh "$f" --format srt; done`
- **conda + faster-whisper 的 OMP 冲突**：脚本已自动设 `KMP_DUPLICATE_LIB_OK=TRUE`，无需手动 export

## License

- This skill: MIT
- mlx-whisper: MIT (Apple)
- Whisper weights: MIT (OpenAI)
