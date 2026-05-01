---
name: video-translate
description: 把视频翻译成另一种语言：抽音轨 → mac-whisper 转录 → LLM 翻译 → mac-tts 配音 (可选 mac-voice-clone 保留原声) → 时间轴对齐 → 字幕烧录回视频。串联 mac-whisper / mac-tts / mac-voice-clone / audio-clean / video-frame-extractor。Trigger on 视频翻译 / video translate / dub video / 视频配音 / 字幕翻译 / 翻译视频 / localize video / 视频本地化 / re-voice / cross-lingual dubbing。
version: 1.0.0
created_at: 2026-04-29
entry_point: scripts/translate.sh
dependencies: ["ffmpeg", "mac-whisper skill", "mac-tts skill (or mac-voice-clone)", "LLM (claude-cli/openai/ollama)"]
tags: [video, translate, dubbing, localization, subtitles, cross-lingual, mac, apple-silicon, community]
---

# video-translate

把一个语言的视频，变成另一个语言。orchestrator skill — 串联现有的 4 个底层 skill，自己只做调度 + 时间轴对齐 + 烧录。

## 流水线

```
video.mp4
   ↓ ffmpeg
audio.wav (原语言)
   ↓ mac-whisper --format json
segments.json (带时间戳的逐句转录)
   ↓ LLM translate (per-segment, preserve timing)
segments_translated.json
   ↓ mac-tts (or mac-voice-clone) per segment
voice_clips/*.wav
   ↓ ffmpeg concat + atempo (squeeze to fit original timing)
dub.wav (新语言配音)
   ↓ ffmpeg mux
video_translated.mp4 (可选烧录字幕)
```

## 三种产出模式

| 模式 | 产物 | 用途 |
|---|---|---|
| `subs` | `.srt` + `.vtt` | 只要翻译字幕，最快 |
| `dub` | `.mp4` 替换音轨 | 配音视频 |
| `dub-cloned` | `.mp4` 用原说话人音色 | 真"原声译制"，需要 mac-voice-clone |

## Quick Start

```bash
# 一次性安装（验证依赖 skill）
bash scripts/install.sh

# 中文视频 → 英文字幕
bash scripts/translate.sh subs zh.mp4 --to en -o en.srt

# 英文视频 → 中文配音（默认女声）
bash scripts/translate.sh dub en.mp4 --from en --to zh -o zh.mp4

# 英文视频 → 中文配音 + 保留原声音色
bash scripts/translate.sh dub-cloned en.mp4 --from en --to zh -o zh.mp4

# 已经有 SRT，只要 dub
bash scripts/translate.sh dub-from-srt zh.srt en.mp4 --to zh -o zh.mp4
```

## 选项

```
translate.sh <mode> <input> [options]

Modes:
  subs            video → translated .srt + .vtt
  dub             video → video with new-language voiceover
  dub-cloned      video → video with cloned original voice in new language

Options:
  --from <lang>       source lang (default: auto-detect via whisper)
  --to <lang>         target lang (default: en)
  --voice <name>      tts voice name (default: language-default)
  --llm <backend>     translation backend: claude-cli|openai|ollama (default: claude-cli)
  --burn-subs         burn translated subs into output video
  --keep-bgm          keep original BGM (uses audio-clean separate to extract bgm first)
  -o, --output <path> output path
```

## LLM 翻译

每段翻译时给 LLM 上下文：

```
Translate the following ZH segments to EN. Preserve numbering and meaning.
Keep each translation roughly the same speaking duration as the original.

[1] 你好，今天我们来聊一下设计模式
[2] 这个其实是个老话题了
...
```

返回严格 JSON 数组：`[{"id":1,"text":"..."}, ...]`

## 时间轴对齐

新音频长度可能 ≠ 原音频长度。对齐策略：

| 偏差 | 处理 |
|---|---|
| < 5% | 直接用 |
| 5-20% | `ffmpeg atempo=ratio` 加速/减速（pitch 不变） |
| > 20% | 分两段，加 200ms 静音填充，避免 chipmunk 效果 |

如果 `--keep-bgm`：先用 `audio-clean separate --stem all` 抽出 vocals 和 instrumental，把新配音叠回 instrumental 上。

## 反模式

- ❌ 用 word-level whisper 时间戳做 atempo → 太碎，听感卡顿。用 segment-level
- ❌ LLM 翻译时不给上下文/不保留编号 → 错位
- ❌ dub-cloned 用 5s 以下的参考音 → 克隆质量差
- ❌ 视频太长一次跑完 → OOM。`--chunk 10min` 分块

## 与其他 skill 的关系

| 依赖 skill | 必需？ | 用途 |
|---|---|---|
| ffmpeg | 必需 | 抽音轨、混音、烧字幕 |
| mac-whisper | 必需 | 转录 |
| mac-tts | dub 模式必需 | 配音 |
| mac-voice-clone | dub-cloned 模式必需 | 克隆原声 |
| audio-clean | 可选 | --keep-bgm 时分离 BGM |
| LLM (claude-cli/openai/ollama) | 必需 | 翻译 |

## License

MIT.
