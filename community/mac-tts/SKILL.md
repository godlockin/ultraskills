---
name: mac-tts
description: 在 Mac 本地把文字合成为高质量语音 (TTS)。三档后端：edge-tts (免费微软神经语音 / 多语种最佳) > kokoro-tts (本地开源 82M / 自然度高) > macOS say (兜底)。输出 wav/mp3。Trigger on TTS / 文字转语音 / 语音合成 / text-to-speech / 配音 / voiceover / read aloud / 朗读。
version: 1.0.0
created_at: 2026-04-25
entry_point: scripts/tts.sh
dependencies: ["python>=3.9", "ffmpeg (optional, for mp3 transcoding)"]
backends: ["edge-tts (default, free, MS neural voices)", "kokoro-tts (offline, 82M)", "say (macOS built-in fallback)"]
tags: [tts, text-to-speech, voice, audio, voiceover, mac, dubbing]
---

# mac-tts

Mac 本地文字转语音 skill。三档后端按"质量 × 自由度 × 是否需要联网"递进：

| 后端 | 质量 | 联网 | Cost | Mac 跑 | 用法 |
|---|---|---|---|---|---|
| **edge-tts** ⭐ | ★★★★☆ MS Azure 神经语音 | 是 | 免费 | ✅ 即装即用 | 默认；多语种最佳 |
| **kokoro-tts** | ★★★★☆ 自然度极高 | 否 | 免费 | ✅ MPS 加速 | 离线/隐私敏感 |
| **macOS say** | ★★☆☆☆ 系统机械 | 否 | 免费 | ✅ 内置 | 兜底/调试 |

## When to use

- 给 mac-whisper 转录稿配回音 / 制作有声书
- 给 magazine-web-ppt / remotion 视频做配音
- 朗读文章/笔记/邮件
- 多语言听写练习

## When NOT to use

- 要克隆特定人声 → 用 XTTS-v2 / Tortoise（Mac 慢）
- 要实时低延迟 (<200ms) → 这套不适合
- 要商用大规模 → 选 ElevenLabs / OpenAI TTS API

## Quick Start

```bash
# 一次性安装
bash scripts/install.sh

# 默认（edge-tts，自动选中文女声）
bash scripts/tts.sh "你好，这是一段测试" -o test.mp3

# 指定语音 + 语速
bash scripts/tts.sh "Hello world" --voice en-US-AriaNeural --rate +20% -o out.wav

# 切到 kokoro 离线
bash scripts/tts.sh "离线合成" --backend kokoro -o out.wav

# 兜底用 say
bash scripts/tts.sh "fallback" --backend say -o out.aiff
```

## 推荐声音（edge-tts，常用）

| 语种 | 声音 ID | 备注 |
|---|---|---|
| 中文女 | `zh-CN-XiaoxiaoNeural` | **默认**，自然温和 |
| 中文男 | `zh-CN-YunxiNeural` | 沉稳 |
| 中文（粤） | `zh-HK-HiuGaaiNeural` | 粤语女 |
| 中文（台） | `zh-TW-HsiaoChenNeural` | 台普女 |
| 英文女 | `en-US-AriaNeural` | 默认英女 |
| 英文男 | `en-US-GuyNeural` | 标准英男 |
| 英文（英） | `en-GB-SoniaNeural` | 英式女 |
| 日文 | `ja-JP-NanamiNeural` | 日女 |
| 韩文 | `ko-KR-SunHiNeural` | 韩女 |

完整列表：`bash scripts/tts.sh --list-voices` 或 `edge-tts --list-voices | grep zh-CN`

## 输出

| 后端 | 默认输出格式 | 自动转换 |
|---|---|---|
| edge-tts | mp3 | 可转 wav（需 ffmpeg） |
| kokoro | wav | 可转 mp3（需 ffmpeg） |
| say | aiff | 可转 wav/mp3（需 ffmpeg） |

后缀决定格式：`-o out.mp3` / `-o out.wav` / `-o out.aiff`。

## Workflow

### Step 1 · 准备文本

支持纯文本或 `-` 从 stdin 读：
```bash
cat article.txt | bash scripts/tts.sh - -o article.mp3
```

长文本（>5000 字）会被自动分段合成再拼接（避免单次请求超时）。

### Step 2 · 选 backend & 语音

- 不知道选啥 → 默认 edge-tts + 默认语音（按文本语言自动选）
- 隐私敏感 → `--backend kokoro`
- 一切都不行 → `--backend say`

### Step 3 · 调节语速 / 音调（仅 edge-tts）

```bash
--rate +20%      # 加速 20%
--rate -10%      # 减速 10%
--pitch +50Hz    # 提高音调
--pitch -100Hz   # 降低音调
--volume +20%    # 加大音量
```

## 常见组合

```bash
# 1) whisper 转录稿 → tts 重新配音
bash ~/.../mac-whisper/scripts/transcribe.sh in.mp4 --format txt
bash ~/.../mac-tts/scripts/tts.sh in.txt --voice zh-CN-YunxiNeural -o out.mp3

# 2) 长文章批量合成
for f in *.txt; do
  bash scripts/tts.sh "$f" -o "${f%.txt}.mp3"
done

# 3) 给 remotion 视频配音
bash scripts/tts.sh script.txt --voice en-US-AriaNeural -o narration.mp3
# 然后在 Remotion Composition 里 import audio
```

## License

- This skill: MIT
- edge-tts: GPL-3.0 (Python wrapper around free MS public service)
- kokoro: Apache 2.0

## 隐私说明

| 后端 | 数据外送 | 隐私风险 |
|------|----------|----------|
| edge-tts | 文本 POST 到 `speech.platform.bing.com`（微软） | ⚠️ 敏感内容（PII、内部资料、未公开文本）请改用本地后端 |
| kokoro-tts | 全本地推理 | ✅ 隐私敏感场景首选 |
| say | 全本地（macOS 内置） | ✅ 无网络请求 |

> edge-tts 是「免费」第三方公共服务，不等于零数据收集。微软会记录 IP 与请求文本；处理 PII / 商业秘密 / 未公开内容时，必须走本地后端。

## macOS 兼容性

`scripts/tts.sh` 的 `say` 声音名硬编码（`Tingting` / `Kyoko` / `Yuna`）在 macOS 13+ 已被 Siri Natural Voices（`zh-CN_Xiaoxiao` 等）取代。修复：

1. 先用 `say -v "$VOICE" ?` 检查声音存在；
2. 否则 fallback：`say -v ? | grep -i "${LANG_HINT}" | head -1 | cut -d' ' -f1`；
3. 仅在 fallback 失败时报错，不要静默落到默认英文。

> `--rate +20%` / `--pitch +50Hz` / `--volume +20%` **只适用于 edge-tts**；`say` 仅支持 `-r rate (wpm)`。脚本对不支持的参数应输出警告，而不是静默忽略。

## 长文本与降级

- `say` 对 > 5KB 文本不稳定；脚本应写临时文件 `say -v "$VOICE" -f <text> -o <aiff>` 而不是命令行直传。
- edge-tts 网络失败（超时、防火墙）应 fallback 到 `kokoro` 或 `say`，不要直接 exit 1。
- 输出文件覆盖默认需 `--force`，否则报错。
