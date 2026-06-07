# Example: Code Agent / IDE 补全

## 场景
构建一个代码 agent，需要：
- 强 tool_call (调用 grep/edit/test)
- 长上下文 (读整个 repo)
- 中等预算 (production 跑批)
- 响应延迟可接受 (非实时)

## 推荐命令

```bash
python3 <skill-path>/scripts/recommend.py \
    --task code \
    --context 128k \
    --budget medium \
    --latency interactive \
    --privacy any \
    --top 5
```

## 实际输出

| Rank | Score | Task | Qual | Speed | Ctx | Cost | Provider | Model |
|------|-------|------|------|-------|-----|------|----------|-------|
| 1 | 91.5 | 90 | 100 | 75 | 100 | 100 | snowflake-cortex | claude-sonnet-4-6 |
| 2 | 91.5 | 90 | 100 | 75 | 100 | 100 | snowflake-cortex | openai-gpt-5.4 |
| 3 | 91.5 | 90 | 100 | 95 | 60 | 100 | snowflake-cortex | openai-gpt-5-mini |
| 4 | 91.5 | 90 | 100 | 95 | 60 | 100 | snowflake-cortex | openai-gpt-5-nano |
| 5 | 91.42 | 90 | 100 | 95 | 60 | 99 | openai | gpt-5-nano |

**解读 breakdown**:
- Task=90: 都进 TOP_TIER (claude-sonnet-4 / gpt-5)
- Quality=100: 顶级实验室 + TOP_TIER 家族 + 新鲜 (近 6 月)
- Speed=75 vs 95: gpt-5-mini/nano 因 "mini/nano" 标识快 20 点
- Ctx=100 vs 60: gpt-5-mini 仅 272K context, 比 1M+ 弱
- Cost=100: snowflake-cortex 路由免费

→ 速度优势被 context 劣势抵消, 4 个并列 91.5。**挑 1 个时考虑**: 1M context 选 #1/#2, 速度优先选 #3/#4。

## 决策说明

**Primary: claude-sonnet-4-6** (snowflake-cortex 路由)
- 1M context 完整吃下整个 repo
- 强 tool_call + reasoning (适合多步 debug)
- attachment 支持 (传图片/screenshot)
- cost 优势 (通过 snowflake-cortex 路由)

**Fallback 链**:
- `openai-gpt-5.4` (snowflake-cortex) — 不同 family，避免单供应商锁定
- `claude-opus-4-7` — 更强但更慢/batch 任务
- 本地直连: `anthropic/claude-sonnet-4-6` (anyapi) — 当 snowflake-cortex 不可用

## 实战代码示例

```python
# 选 primary + 2 fallbacks
PRIMARY = "snowflake-cortex/claude-sonnet-4-6"
FALLBACK_1 = "openai-gpt-5.4"  # 不同 family
FALLBACK_2 = "anthropic/claude-opus-4-7"  # 强推理
```

## 注意

- 真实 $0 是 snowflake-cortex 路由的免费 tier (用量配额)
- production 跑批需监控配额，超限自动降级到 fallback
- 如果数据敏感，替换 `--privacy any` 为 `--privacy on-prem` → 排除 snowflake-cortex，转 Llama/Qwen 本地模型
