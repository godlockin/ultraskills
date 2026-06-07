# LLM Capability Matrix (Top 30)

> 静态速查表 — 脑暴阶段不依赖实时 fetch
> 数据基线: models.dev 2026-06-07
> 实际数据可能漂移，跑 `recommend.py` 取最新

## 🔥 旗舰模型 (Frontier)

| Model | Provider | Context | $in/M | $out/M | Code | Reasoning | Vision | OW |
|-------|----------|---------|-------|--------|------|-----------|--------|-----|
| Claude Opus 4.7 | Anthropic | 1M | 15 | 75 | ✓✓✓ | ✓✓✓ | ✓ | ✗ |
| Claude Sonnet 4.6 | Anthropic | 1M | 3 | 15 | ✓✓✓ | ✓✓ | ✓ | ✗ |
| Claude Haiku 4 | Anthropic | 200K | 0.8 | 4 | ✓✓ | ✓ | ✓ | ✗ |
| GPT-5 | OpenAI | 1M+ | 5 | 15 | ✓✓✓ | ✓✓✓ | ✓ | ✗ |
| GPT-5 mini | OpenAI | 1M | 0.5 | 2 | ✓✓ | ✓ | ✓ | ✗ |
| GPT-4.1 | OpenAI | 1M | 2 | 8 | ✓✓ | ✓✓ | ✓ | ✗ |
| Gemini 2.5 Pro | Google | 2M | 1.25 | 10 | ✓✓ | ✓✓✓ | ✓ | ✗ |
| Gemini 2.5 Flash | Google | 1M | 0.075 | 0.3 | ✓✓ | ✓ | ✓ | ✗ |
| Grok 4 | xAI | 256K | 5 | 15 | ✓✓ | ✓✓ | ✓ | ✗ |

## 🧠 推理专精 (Reasoning)

| Model | Provider | Context | $in/M | $out/M | Note |
|-------|----------|---------|-------|--------|------|
| o3 | OpenAI | 200K | 60 | 240 | 数学/科学最强 |
| o1 | OpenAI | 200K | 15 | 60 | o3 轻量版 |
| DeepSeek R1 | DeepSeek | 64K | 0.55 | 2.19 | 开源推理 SOTA |
| QwQ | Alibaba | 131K | 0.41 | 1.64 | 国产推理 |
| Claude Opus 4.7 (thinking) | Anthropic | 1M | 15 | 75 | 启用 extended thinking |
| Gemini 2.5 Pro (thinking) | Google | 2M | 1.25 | 10 | 内置 thinking |

## 🌐 长上下文 (Long Context > 1M)

| Model | Provider | Context | Note |
|-------|----------|---------|------|
| Qwen Long | Alibaba | **10M** | 上下文之王 |
| Llama 4 Scout | Meta | 10M | 开源 10M |
| Gemini 2.5 Pro | Google | 2M | 商业最佳长上下文 |
| Claude Sonnet 4.6 | Anthropic | 1M | 强 reasoning 长上下文 |
| GPT-4.1 | OpenAI | 1M | OpenAI 长上下文 |
| Grok 4 | xAI | 256K | 256K 实用派 |

## 🛠️ 代码专精 (Code)

| Model | Provider | Context | $in/M | Note |
|-------|----------|---------|-------|------|
| Claude Sonnet 4.6 | Anthropic | 1M | 3 | SWE-bench SOTA |
| GPT-5 | OpenAI | 1M+ | 5 | 综合最强 |
| Qwen2.5-Coder-32B | Alibaba | 128K | self-host | 开源代码 SOTA |
| DeepSeek Coder V2 | DeepSeek | 128K | 0.14 | 性价比 |
| Codestral 25.01 | Mistral | 256K | 0.3 | 补全速度快 |
| Llama 3.3 70B | Meta | 128K | self-host | 通用代码 |

## 🪶 轻量快速 (Fast/Cheap)

| Model | Provider | Context | $in/M | $out/M | 延迟 |
|-------|----------|---------|-------|--------|------|
| Llama 3.1 8B (Groq) | Groq | 128K | 0.05 | 0.08 | <500ms |
| GPT-4o mini | OpenAI | 128K | 0.15 | 0.6 | ~1s |
| Gemini 2.0 Flash | Google | 1M | 0.1 | 0.4 | ~1s |
| Claude Haiku 4 | Anthropic | 200K | 0.8 | 4 | ~1s |
| Mistral Small | Mistral | 128K | 0.2 | 0.6 | ~1s |
| DeepSeek Chat | DeepSeek | 64K | 0.14 | 0.28 | ~1s |

## 🔓 开源可自部署 (Open Weights)

| Model | Size | Context | Hardware | 用途 |
|-------|------|---------|----------|------|
| Llama 3.3 70B | 70B | 128K | 2× A100 80G | 通用 |
| Qwen 2.5 72B | 72B | 128K | 2× A100 80G | 中文强 |
| Mistral Large 2 | 123B | 128K | 2× A100 80G | 欧洲合规 |
| DeepSeek V3 | 67B | 64K | 2× A100 80G | 推理 |
| Qwen Long | 72B+ | 10M | 4× A100 80G | 长上下文 |
| Llama 4 Scout 17B | 17B | 10M | 1× A100 80G | 小模型 10M |
| Gemma 2 27B | 27B | 8K | 1× A100 80G | Google 开源 |

## 🌍 多语言 (Multilingual)

| Model | 中文 | 欧洲 | 阿拉伯 | Note |
|-------|------|------|--------|------|
| Qwen 2.5 | ✓✓✓ | ✓ | ✓ | 中文王者 |
| GPT-5 | ✓✓ | ✓✓ | ✓ | 综合强 |
| Claude Sonnet 4.6 | ✓✓ | ✓✓✓ | ✓ | 欧洲最强 |
| Gemini 2.5 Pro | ✓✓ | ✓✓ | ✓✓ | 阿拉伯语强 |
| Aya Expanse 32B | ✓ | ✓✓ | ✓✓ | 多语言专精 |

## 🎨 多模态 (Multimodal)

### Vision (Image → Text)
- **GPT-5**, **Claude Sonnet 4.6**, **Gemini 2.5 Pro** — 三大商用 vision SOTA
- **Qwen2-VL-72B** — 开源 vision 强
- **Llama 3.2 90B Vision** — Meta 开源 vision
- **Pixtral Large** — Mistral 开源 vision

### Audio (Speech → Text / Text → Speech)
- **GPT-4o Audio** — realtime 对话
- **Gemini 2.0 Flash** — multimodal audio
- **Ultravox v0.4** — 开源 realtime
- **ElevenLabs / Cartesia** — TTS (非 LLM)

### Video
- **Gemini 2.0 Flash** — 视频理解
- **Qwen2-VL** — 视频支持
- **GPT-4o** — 视频帧分析

## 📊 成本对比 (1M input + 500K output)

| Model | 单次成本 | 1K 次/天 月成本 |
|-------|----------|------------------|
| Llama 3.1 8B (Groq) | $0.09 | **$2,700** |
| GPT-4o mini | $0.45 | $13,500 |
| Claude Haiku 4 | $2.80 | $84,000 |
| GPT-5 | $12.50 | $375,000 |
| Claude Opus 4.7 | $52.50 | $1,575,000 |
| o3 | $180.00 | $5,400,000 |

## 🎯 快速决策树

```
需要 1M+ context?  → Gemini 2.5 Pro (2M) / Claude / GPT-4.1
需要 open weights? → Llama 3.3 70B / Qwen 2.5 72B
需要极致便宜?     → Llama 8B (Groq) / DeepSeek
需要最强推理?     → o3 / Claude Opus thinking
需要 vision?      → GPT-5 / Claude Sonnet / Gemini
需要中文?         → Qwen 2.5 / DeepSeek / GPT-5
需要 100% 本地?   → Llama / Qwen / Mistral (自部署)
```

## 📚 资源

- **实时数据**: `python3 ../scripts/fetch_models.py` → `.cache/models.json`
- **精确推荐**: `python3 ../scripts/recommend.py --task <X> --budget <Y>`
- **官方源**: https://models.dev
