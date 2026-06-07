# Example: 成本敏感场景

## 场景
个人项目 / 副业 / 大规模批量标注：
- 每次调用都计费，必须省
- 任务可分解 (不需要最强推理)
- 大量调用 (1K+ 次/天)
- 质量"够用即可" (80 分)

## 推荐命令

```bash
python3 <skill-path>/scripts/recommend.py \
    --task code \
    --context 32k \
    --budget low \
    --latency interactive \
    --top 10
```

## 实际输出 (示例)

| Rank | Score | Provider | Model | Context | $in/M | $out/M | Note |
|------|-------|----------|-------|---------|-------|--------|------|
| 1 | ~92 | groq | llama-3.1-8b-instant | 128k | 0.05 | 0.08 | 超快 inference |
| 2 | ~90 | openai | gpt-4o-mini | 128k | 0.15 | 0.60 | 质量稳 |
| 3 | ~88 | google | gemini-2.0-flash | 1M | 0.10 | 0.40 | 1M context |
| 4 | ~85 | mistral | mistral-small | 128k | 0.20 | 0.60 | 欧洲合规 |
| 5 | ~82 | deepseek | deepseek-chat | 64k | 0.14 | 0.28 | 中文友好 |

## 决策说明

**Primary: Llama 3.1 8B (Groq 路由)**
- $0.05/M input = 同质量下最便宜
- Groq LPU 推理 ~500 tokens/s
- 128k context 足够 80% 任务

**Fallback 链**:
- `gpt-4o-mini` (质量稳, OpenAI 生态)
- `gemini-2.0-flash` (1M context 备不时之需)
- `deepseek-chat` (中文任务首选)

## 成本对比 (1M 调用, 平均 1K input + 500 output)

| 模型 | 月成本 |
|------|--------|
| Llama 3.1 8B (Groq) | **$90** |
| GPT-4o mini | $300 |
| GPT-5 | $5,000+ |
| Claude Opus | $15,000+ |

→ 选 mini 模型 vs Opus 差 **170 倍**

## 实战代码示例

```python
# 成本优化配置
COST_OPTIMIZED = {
    "primary": "groq/llama-3.1-8b-instant",  # $0.05/M
    "quality_threshold": 0.8,  # 自动 fallback 触发
    "fallback_chain": [
        "openai/gpt-4o-mini",  # 质量升级
        "anthropic/claude-haiku-4",  # 复杂任务
    ],
}

# 使用模式: 80% 流量用 primary, 20% 升级到 fallback
def route(prompt_complexity: int) -> str:
    if prompt_complexity < 30:
        return COST_OPTIMIZED["primary"]
    return COST_OPTIMIZED["fallback_chain"][0]
```

## 关键陷阱

- **不要**用 mini 模型做关键决策 (法律/医疗/金融) — 幻觉率高
- **batch 场景**才用 mini — 实时用户对话用 mini 体验差
- **质量阈值**自动 fallback: primary 输出 confidence < 0.8 时升级
