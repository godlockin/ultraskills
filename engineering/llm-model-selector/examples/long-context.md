# Example: 1M+ Context RAG

## 场景
RAG pipeline 要处理整个 codebase / 长 PDF / 多文档综述：
- 上下文 ≥ 1M tokens
- 强 reasoning (跨文档综合)
- 成本敏感 (每次调用 tokens 大)
- 允许慢 (batch 处理)

## 推荐命令

```bash
python3 <skill-path>/scripts/recommend.py \
    --task long-context \
    --context 1m \
    --budget medium \
    --latency batch \
    --top 5
```

## 实际输出 (示例)

| Rank | Score | Provider | Model | Context | Capabilities |
|------|-------|----------|-------|---------|--------------|
| 1 | ~95 | gemini-* | gemini-2.5-pro | 2,000,000 | reasoning, attachment |
| 2 | ~92 | openai | gpt-4.1 | 1,000,000 | tool_call, structured_output |
| 3 | ~90 | claude | claude-sonnet-4-6 | 1,000,000 | reasoning, attachment |
| 4 | ~88 | qwen | qwen-long | 10,000,000 | open_weights, on-prem |

## 决策说明

**Primary: Gemini 2.5 Pro** (2M context, batch 友好)
- 2M context = 一次吃下整本技术书
- batch 延迟无所谓，省钱
- cost 约 $1.25/M input (业界最便宜的大 context)

**Fallback 链**:
- `gpt-4.1` (1M, OpenAI 生态稳定)
- `claude-sonnet-4-6` (1M, 强 reasoning)
- `qwen-long` (10M!, open_weights, **完全本地**部署)

## 实战代码示例

```python
# RAG config
RAG_CONFIG = {
    "primary": {
        "provider": "google",
        "model": "gemini-2.5-pro",
        "context_window": 2_000_000,
    },
    "fallback_chain": [
        {"provider": "openai", "model": "gpt-4.1"},
        {"provider": "anthropic", "model": "claude-sonnet-4-6"},
    ],
    "local_emergency": {  # 断网/API 挂了
        "model": "qwen-long",
        "deployment": "on-prem",
    },
}
```

## 关键陷阱

- **不要用** `flash` 类模型做 long-context 任务 — context 大但 quality drop
- **Gemini 2.5 Pro** 的 long-context 实测比 Sonnet 在跨文档推理上更强
- **qwen-long 10M** 是核武器，但需自部署 GPU，成本换隐私
