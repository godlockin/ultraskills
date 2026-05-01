---
name: audio-clean
description: 在 Mac 本地清理音频：人声/伴奏分离 (demucs) + 降噪 (rnnoise/noisereduce) + 响度归一化 (ffmpeg loudnorm EBU R128)。一条命令把粗糙录音变干净播客/配音素材。Trigger on 音频清理 / audio clean / denoise / 降噪 / 去伴奏 / vocal isolate / 分离人声 / 响度归一 / loudness normalize / mastering / 母带处理。
version: 1.0.0
created_at: 2026-04-29
entry_point: scripts/clean.sh
dependencies: ["python>=3.10", "ffmpeg", "demucs (auto-install)", "noisereduce (auto-install)"]
tags: [audio, clean, denoise, demucs, mastering, loudness, vocal-isolation, mac, apple-silicon, community]
---

# audio-clean

把粗糙音频变干净的本地处理流水线。三档能力，按需组合：

| 阶段 | 工具 | 解决什么 |
|---|---|---|
| **separate** | demucs (htdemucs / mdx_extra) | 4 轨分离 (vocals / drums / bass / other) — 拿干声 / 去 BGM |
| **denoise** | RNNoise (via ffmpeg arnndn) 或 noisereduce | 去稳态噪声（空调、底噪、嘶声） |
| **normalize** | ffmpeg `loudnorm` (EBU R128) | 响度归一（播客 -16 LUFS / 流媒体 -14 LUFS / 影视 -23 LUFS） |

## 为什么本地

- 上传到云端 = 隐私 + 等待 + 可能限时长
- 这套全本地、Apple Silicon MPS 加速（demucs 用 PyTorch）
- 一条命令搞定，跟 `mac-whisper` / `mac-tts` 串起来即得字幕/配音流水线

## Quick Start

```bash
# 一次性安装
bash scripts/install.sh

# 单步：去伴奏（拿干净人声）
bash scripts/clean.sh separate input.mp3 -o vocals.wav

# 单步：降噪
bash scripts/clean.sh denoise raw.wav -o cleaned.wav

# 单步：响度归一（默认播客 -16 LUFS）
bash scripts/clean.sh normalize cleaned.wav -o final.wav --lufs -16

# 流水线：separate → denoise → normalize
bash scripts/clean.sh pipeline interview.mp3 -o final.wav --lufs -14

# 仅人声 + 归一（跳过降噪）
bash scripts/clean.sh pipeline song.mp3 -o vocals.wav --steps separate,normalize
```

## 命令详解

### `separate` — 人声/伴奏分离

```
clean.sh separate <input> -o <output> [--model htdemucs|mdx_extra] [--stem vocals|drums|bass|other|all]
```

- 默认输出 vocals 单轨。要全部 4 轨用 `--stem all`（输出文件夹）
- `htdemucs`（默认）：质量高，慢。`mdx_extra`：快，质量略次
- 4-5 分钟歌曲：M2 Pro CPU 约 1-2 分钟，MPS 30 秒

### `denoise` — 降噪

```
clean.sh denoise <input> -o <output> [--method rnnoise|spectral] [--strength 0-1]
```

- `rnnoise`（默认，质量好）：基于 RNN，对话首选
- `spectral`：noisereduce 谱减，对稳态背景音
- 强度 0=不动 / 1=最大；默认 0.7

### `normalize` — 响度归一（EBU R128）

```
clean.sh normalize <input> -o <output> [--lufs -23|-16|-14] [--tp -1.0] [--lra 11]
```

| 目标 | LUFS | 用途 |
|---|---|---|
| `-23` | 默认 | 影视广播 (EBU R128) |
| `-16` | 推荐 | 播客 (Apple Podcasts) |
| `-14` | 流媒体 | Spotify / YouTube |
| `-19` | 中性 | 有声书 |

True peak `--tp -1.0`（默认）防削波。LRA 控制动态范围（11=标准）。

### `pipeline` — 三步串

```
clean.sh pipeline <input> -o <output> [--steps separate,denoise,normalize] [--lufs -16]
```

中间产物在 `/tmp/` 自动清理。失败保留供调试。

## 反模式

- ❌ 用 `loudnorm` 处理已经母带过的曲子 → 二次压缩失真
- ❌ 把 `--strength 1` 当万能 → 把语音也压扁，伪影
- ❌ demucs 处理纯说话音频 → 浪费 GPU，直接 denoise 就行
- ❌ 流媒体 audio 又用 -23 LUFS → 比别人都安静

## 与其他 skill 串

```bash
# 完整：视频 → 干净配音 → 字幕
yt-dlp video.mp4 → ffmpeg -i video.mp4 -vn audio.wav
   → audio-clean pipeline audio.wav -o clean.wav --steps denoise,normalize
   → mac-whisper clean.wav --srt
   → ffmpeg burn subs back to video
```

## 模型 / 缓存

- demucs 模型：~80MB-300MB，首次下载到 `~/.cache/torch/hub/`
- RNNoise model：随 ffmpeg 内置或 `~/.cache/audio-clean/rnnoise.rnnn`

## License

MIT. demucs (MIT, Meta), noisereduce (MIT), ffmpeg (LGPL).
