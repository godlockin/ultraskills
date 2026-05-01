---
name: mac-voice-clone
description: 在 Mac 本地把"一段参考音频 + 文字"合成成"用参考人声朗读这段文字"的克隆语音。四档后端：IndexTTS-2 ⭐ (Bilibili/Apache-2.0/最强 prosody) > F5-TTS (轻量/MIT) > VoxCPM2 (openbmb 2B/Apache-2.0/可商用) > GPT-SoVITS (中文最强/few-shot)。Trigger on voice clone / 声音克隆 / 语音克隆 / clone my voice / 模仿声音 / TTS with reference audio / zero-shot TTS / IndexTTS / index-tts。
version: 1.1.0
created_at: 2026-04-27
updated_at: 2026-04-29
entry_point: scripts/clone.sh
dependencies: ["python>=3.10", "torch>=2.4 (MPS)", "ffmpeg", "uv (for indextts2)"]
backends: ["indextts2 (⭐ Bilibili IndexTTS-2, Apache-2.0, best prosody/breath/emotion)", "f5-tts (MIT, lightweight zero-shot 10s ref)", "voxcpm (openbmb 2B, Apache-2.0, 30 langs)", "gpt-sovits (zh best, few-shot fine-tune)"]
tags: [tts, voice-clone, voice-cloning, zero-shot, mac, apple-silicon, indextts, indextts2, f5-tts, voxcpm, gpt-sovits, prosody, emotion]
---

# mac-voice-clone

Mac 本地**零样本语音克隆**：给一段 6–30s 的参考音频 + 想合成的文字 → 输出"用那个声音朗读这段文字"的音频。

## 与 mac-tts 的区别

| Skill | 输入 | 用途 |
|---|---|---|
| **mac-tts** | 文字 + 预制声音 ID | 日常 TTS，质量稳定 |
| **mac-voice-clone**（本 skill） | 文字 + **参考音频** | 模仿任意人声，做配音/有声书/角色扮演 |

## 后端对比（v1.1：IndexTTS-2 升为默认）

| 后端 | 质量 | Prosody（呼吸/停顿/情绪） | 速度 (M-series) | 中文 | License | 占用 | 何时用 |
|---|---|---|---|---|---|---|---|
| **IndexTTS-2** ⭐ NEW | ★★★★★ | **最佳** — 尊重 `...` `—` `,` `.`，带呼吸停顿，可控情绪 | RTF ~4–9（MPS） | 优 | **Apache-2.0** | ~5 GB 权重 | **默认**：旁白、视频 VO、有声书、播客 |
| **F5-TTS** | ★★★★☆ | 弱 — 架构性忽略标点，节奏偏快 | 实时 ~1x | 良 | MIT | ~1.4 GB | 快速 zero-shot、轻量场景 |
| **VoxCPM2** | ★★★★★ | 中等 | MPS ~0.5x | 优 | Apache-2.0 | ~8 GB 统一内存 | 30 语种、48kHz、多语种 |
| **GPT-SoVITS** | ★★★★★ | 中–好 | 快 (~2x) | **顶级** | MIT | ~4 GB | 中文克隆最强；可做 few-shot 微调 |

> 注：IndexTTS-2 / F5-TTS / VoxCPM 是 **zero-shot**（直接给参考音）。GPT-SoVITS 可 zero-shot，但 5–30 分钟微调后中文质感无对手。

### IndexTTS-2 关键优势

- **自然呼吸 / 停顿 / 句末气口**：F5-TTS 的根因痛点（忽略标点、整段平推）在 IndexTTS-2 被解决——`...` `—` `,` `。` 都被显式建模。
- **情绪可控**：三种方式
  1. 给一段独立的"情绪参考音频"
  2. 文字描述情绪（"sad and slow"），由内置 Qwen 0.6B 转情绪向量
  3. 直接传情绪向量
- **时长控制（roadmap）**：论文里有，v2.0 release **尚未开放**接口。当前用 `interval_silence` + `max_text_tokens_per_segment` 间接调节。
- **License**：Apache-2.0，可商用无歧义。

### IndexTTS-2 代价

- 权重大：首次约 **~5 GB**（Qwen 0.6B 情绪 + s2mel + GPT + bigvgan + MaskGCT semantic codec + campplus + wav2vec2bert）
- 推理慢：M 系列 MPS RTF ~4–9（生成 50s 音频要 ~440s 首跑、~110–225s 后续，得益于 reference cache）
- 装机要求 `uv`（README 明令禁止 pip / conda）

## 何时不要用本 skill

- 只是想读文字 → 用 [`mac-tts`](../mac-tts/) 更轻量
- 要克隆 + 实时低延迟（<200ms）→ 不适合，本地都达不到
- 商用大规模 → 直接用 ElevenLabs / OpenAI Voice API

## 快速开始

```bash
# 一次性安装（默认装 F5-TTS；IndexTTS-2 见下）
bash scripts/install.sh

# 用 IndexTTS-2 克隆（v1.1 推荐默认 — 最自然）
bash scripts/clone.sh \
  --backend indextts2 \
  --ref-audio sample.wav \
  --text "我要合成的新内容，带逗号、停顿——还有省略号……" \
  -o cloned.wav

# 用 F5-TTS 克隆（轻量、快、需要 ref-text）
bash scripts/clone.sh \
  --backend f5 \
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

## 安装 IndexTTS-2（必须用 uv，不要用 pip / conda）

```bash
# 1) 安装 uv（如已装跳过）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) clone 仓库 + 同步依赖
git clone https://github.com/index-tts/index-tts.git ~/working/index-tts
cd ~/working/index-tts
uv sync --all-extras

# 3) 下载权重（~5 GB）
#    国内网络慢可加 HF 镜像：
export HF_ENDPOINT="https://hf-mirror.com"
uv run hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints

# 4) 让本 skill 找得到（在你的 shell rc 里）
export INDEX_TTS_DIR="$HOME/working/index-tts"
```

### 直接用 Python（不走 clone.sh 也可以）

```python
from indextts.infer_v2 import IndexTTS2
import torch
device = "mps" if torch.backends.mps.is_available() else "cpu"
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=False,
    device=device,
)
tts.infer(
    spk_audio_prompt="ref.wav",
    text="要合成的文字，带,。?!……和——。",
    output_path="out.wav",
    verbose=False,
    interval_silence=350,            # ms; ↑ 更多呼吸
    max_text_tokens_per_segment=60,  # ↓ 更多分段 → 更多句间停顿
    length_penalty=-0.5,             # 负值 = 节奏更慢
    temperature=0.75,
    top_p=0.85,
    top_k=30,
    num_beams=3,
    repetition_penalty=10.0,
)
```

## 参考音频要求

| 项 | 要求 |
|---|---|
| 时长 | IndexTTS-2: 6–30s 都行；F5/VoxCPM: 6–15s；GPT-SoVITS: 单条 5–10s（多条更好） |
| 质量 | 16kHz+，单声道，无背景音乐 |
| 内容 | 完整句子，一致情绪 |
| 转写 | F5-TTS 必填；IndexTTS-2 / VoxCPM 可选；GPT-SoVITS 必填 |

不干净的样本会污染克隆效果。先用 ffmpeg 降噪：
```bash
ffmpeg -i raw.wav -af "highpass=f=80,lowpass=f=8000,afftdn=nf=-25" clean.wav
```

## Workflow

### Step 1 · 准备样本
- 录 10s 干净人声（可用 mac-whisper 转写得到 ref-text）
- 必要时切片：`ffmpeg -i src.mp3 -ss 5 -t 12 -ac 1 -ar 24000 sample.wav`

### Step 2 · 选后端
- 默认 / 旁白 / 有声书 / 视频 VO → **IndexTTS-2** ⭐
- 不在乎 prosody、要快 / 要轻 → F5-TTS
- 多语种 / 商用 → VoxCPM
- 中文为主、肯花时间微调 → GPT-SoVITS

### Step 3 · 长文本
长文本（>500 字）自动按句号分段合成再拼接，避免单次推理 OOM。IndexTTS-2 用 `max_text_tokens_per_segment` 自动切；调小可换更多句间气口。

## Lessons Learned（v1.1 — 来自一次 APAC 演示真实生产跑）

> 背景：用 6 段不同口音的旁白参考音 × 6 段中英混排稿件做克隆。先 F5-TTS（v1.0 默认），后切 IndexTTS-2。

1. **F5-TTS 的 prosody 是架构性短板，不是参数问题。**
   - 试过 `--speed 0.9 --nfe_step 48 --cross_fade_duration 0.25`，只买到 ~10–15% 整体减速，**没有句中停顿/呼吸/句末收尾**。
   - `...` `——` `，` `。` 等标点基本被忽略——模型在 token 化阶段就丢了。
   - 不要再花时间调 F5 参数追求自然度。**直接换后端**。

2. **F5-TTS `--remove_silence` 对旁白是 anti-pattern。**
   - 它会把自然呼吸也剥光，听感更机械。旁白/有声书一律 **不要**开。

3. **F5-TTS 在 MPS 上会 mid-batch 段错误。**
   - 实测 `Segmentation fault: 11` 出现在 6 段批跑的第 5 段。
   - 可靠性优先时，把每段克隆放在**独立子进程**里跑；一段挂了不会带走整批。

4. **IndexTTS-2 必须用 `uv` 装，不要用 pip / conda。**
   - 上游 README 明文：非 uv 安装 unsupported，会以"不显眼的方式"挂掉（依赖解析、CUDA/MPS extras、权重路径都可能歪）。
   - 曾尝试 `pip install -e .`，运行时报 protobuf / pynini / wetextprocessing 各种细节问题，全部在 `uv sync --all-extras` 下消失。

5. **IndexTTS-2 首跑要拉 ~5 GB。**
   - 国内 / 公司网络慢就 `export HF_ENDPOINT="https://hf-mirror.com"`，整套时间从小时级降到 10–15 分钟。

6. **IndexTTS-2 v2.0 还没开 explicit duration 接口。**
   - 论文里的"目标时长对齐"在当前 release **没暴露**。如果需要"控制旁白长度"，用：
     - `interval_silence`（句间静音 ms，350 已偏长）
     - `max_text_tokens_per_segment`（调小 → 更多分段 → 更多句间气口）
     - `length_penalty=-0.5`（负值整体放慢一点）
   - 不要去找 `target_duration` 这类参数，没有。

7. **IndexTTS-2 同 speaker reference 有缓存，批跑顺序很重要。**
   - 同一个 `spk_audio_prompt` 路径第一次 ~440s（生成 ~50s 音频），后续每次降到 ~110–225s。
   - 6 段同一个人，**比** 6 段不同人**显著快**。批跑前按 speaker 分组排序。

8. **可调 prosody 的 4 个旋钮（按影响力排序）**
   - `interval_silence`（直接控呼吸停顿）
   - `max_text_tokens_per_segment`（间接控停顿密度）
   - `length_penalty`（< 0 放慢）
   - `temperature` / `top_p` / `num_beams`（稳定性 vs 自然度，默认 `0.75 / 0.85 / 3` 已经稳）

## 与其他 skill 组合

```bash
# 1) 录一段自己声音 → 让 AI 写稿 → 合成"自己读"
bash scripts/clone.sh --backend indextts2 --ref-audio me.wav \
  --text "$(cat new_script.txt)" -o narration.wav

# 2) 配合 mac-whisper：从视频提取人声 + 转写做参考
bash ~/.../mac-whisper/scripts/transcribe.sh interview.mp4 --format txt
# → 得到 ref-text，截前 12s 音频做 ref-audio

# 3) 合成完用 video-frame-extractor 或 remotion 做配视频
```

## License

- This skill: MIT
- IndexTTS-2: **Apache-2.0** (Bilibili / index-tts team)
- F5-TTS: MIT
- VoxCPM: Apache-2.0
- GPT-SoVITS: MIT

## 安全 & 伦理

⚠️ **不要克隆未授权的声音**。本地工具不审查输入，但克隆他人声音用于欺诈/伪造在多数司法管辖区违法。仅克隆：
- 你自己的声音
- 已获授权的音色
- 公有领域 / Creative Commons 音源
