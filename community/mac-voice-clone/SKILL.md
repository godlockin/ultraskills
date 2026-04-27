---
name: mac-voice-clone
description: 在 Mac 本地把"一段参考音频 + 文字"合成成"用参考人声朗读这段文字"的克隆语音。三档后端：F5-TTS (默认/最佳/MIT) > VoxCPM2 (openbmb 2B/Apache-2.0/可商用) > GPT-SoVITS (中文最强/few-shot)。Trigger on voice clone / 声音克隆 / 语音克隆 / clone my voice / 模仿声音 / TTS with reference audio / zero-shot TTS。
version: 1.0.0
created_at: 2026-04-27
entry_point: scripts/clone.sh
dependencies: ["python>=3.10", "torch>=2.4 (MPS)", "ffmpeg"]
backends: ["f5-tts (default, MIT, zero-shot 10s ref)", "voxcpm (openbmb 2B, Apache-2.0, 30 langs)", "gpt-sovits (zh best, few-shot fine-tune)"]
tags: [tts, voice-clone, voice-cloning, zero-shot, mac, apple-silicon]
---

# mac-voice-clone

Mac 本地**零样本语音克隆**：给一段 6–30s 的参考音频 + 想合成的文字 → 输出"用那个声音朗读这段文字"的音频。

## 与 mac-tts 的区别

| Skill | 输入 | 用途 |
|---|---|---|
| **mac-tts** | 文字 + 预制声音 ID | 日常 TTS，质量稳定 |
| **mac-voice-clone**（本 skill） | 文字 + **参考音频** | 模仿任意人声，做配音/有声书/角色扮演 |

## 后端对比

| 后端 | 质量 | 速度 (M2) | 中文 | License | 显存/内存 | 用法 |
|---|---|---|---|---|---|---|
| **F5-TTS** ⭐ | ★★★★★ | 实时 ~1x | 良 | **MIT** | ~4GB | 默认；10s 参考音 + 转写 |
| **VoxCPM2** | ★★★★★ | MPS ~0.5x | 优 | **Apache-2.0** 商用 | ~8GB 统一内存 | 30 语种、48kHz |
| **GPT-SoVITS** | ★★★★★ | 快 (~2x) | **顶级** | MIT | ~4GB | 中文克隆最强；需短训练 |

> 注：F5-TTS / VoxCPM 是 **zero-shot**（直接给参考音）。GPT-SoVITS 需要 5–30 分钟微调，但中文质感无对手。

## 何时不要用本 skill

- 只是想读文字 → 用 [`mac-tts`](../mac-tts/) 更轻量
- 要克隆 + 实时低延迟（<200ms）→ 不适合，本地都达不到
- 商用大规模 → 直接用 ElevenLabs / OpenAI Voice API

## 快速开始

```bash
# 一次性安装（默认装 F5-TTS）
bash scripts/install.sh

# 用 F5-TTS 克隆（默认）
bash scripts/clone.sh \
  --ref-audio sample.wav \
  --ref-text "这是参考音频里说的话" \
  --text "我要合成的新内容" \
  -o cloned.wav

# 切到 VoxCPM2（可商用、多语种）
bash scripts/clone.sh \
  --backend voxcpm \
  --ref-audio sample.wav \
  --text "Hello, this is a cloned voice." \
  -o out.wav

# 切到 GPT-SoVITS（中文最强）
bash scripts/clone.sh \
  --backend gpt-sovits \
  --ref-audio zh_sample.wav \
  --ref-text "你好世界" \
  --text "今天天气不错" \
  -o zh_out.wav
```

## 参考音频要求

| 项 | 要求 |
|---|---|
| 时长 | F5/VoxCPM: 6–15s；GPT-SoVITS: 单条 5–10s（多条更好） |
| 质量 | 16kHz+，单声道，无背景音乐 |
| 内容 | 完整句子，一致情绪 |
| 转写 | F5-TTS 必填；VoxCPM 可选；GPT-SoVITS 必填 |

不干净的样本会污染克隆效果。先用 ffmpeg 降噪：
```bash
ffmpeg -i raw.wav -af "highpass=f=80,lowpass=f=8000,afftdn=nf=-25" clean.wav
```

## Workflow

### Step 1 · 准备样本
- 录 10s 干净人声（可用 mac-whisper 转写得到 ref-text）
- 必要时切片：`ffmpeg -i src.mp3 -ss 5 -t 12 -ac 1 -ar 24000 sample.wav`

### Step 2 · 选后端
- 不知道选啥 → 默认 F5-TTS
- 中文为主 → `--backend gpt-sovits`
- 多语种 / 商用 → `--backend voxcpm`

### Step 3 · 长文本
长文本（>500 字）自动按句号分段合成再拼接，避免单次推理 OOM。

## 与其他 skill 组合

```bash
# 1) 录一段自己声音 → 让 AI 写稿 → 合成"自己读"
bash scripts/clone.sh --ref-audio me.wav --ref-text "$(cat ref.txt)" \
  --text "$(cat new_script.txt)" -o narration.wav

# 2) 配合 mac-whisper：从视频提取人声 + 转写做参考
bash ~/.../mac-whisper/scripts/transcribe.sh interview.mp4 --format txt
# → 得到 ref-text，截前 12s 音频做 ref-audio

# 3) 合成完用 video-frame-extractor 或 remotion 做配视频
```

## License

- This skill: MIT
- F5-TTS: MIT
- VoxCPM: Apache-2.0
- GPT-SoVITS: MIT

## 安全 & 伦理

⚠️ **不要克隆未授权的声音**。本地工具不审查输入，但克隆他人声音用于欺诈/伪造在多数司法管辖区违法。仅克隆：
- 你自己的声音
- 已获授权的音色
- 公有领域 / Creative Commons 音源
