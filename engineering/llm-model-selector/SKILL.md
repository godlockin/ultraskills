---
name: llm-model-selector
description: 根据任务类型/上下文/成本/延迟/隐私 5 维度推荐 LLM provider + model，输出 top-3 + fallback 链。Triggers: "选个模型", "推荐 LLM", "用 GPT 还是 Claude", "哪个 model 适合 X 任务", "用哪个 model 跑这个 agent", "ultraskills arena 用哪个"
version: 1.0.0
tags: [llm, model-selection, provider, api, ranking, engineering]
argument-hint: "<task description + 1-2 关键约束>"
api_reference: https://models.dev
---

# LLM Model Selector

> 实时数据驱动 (139 providers, 完整 schema)，5 维度评分，避免凭印象选模型。

## 🎯 目标

解决两个场景的"用哪个 model"决策：

1. **ultraskills 内部** — 在本项目做 LLM 相关工作（arena 评估、agent 跑批、文档生成）时挑模型
2. **用户其他项目** — 在任何其他项目里开发时挑模型

不再凭记忆 / 搜博客 / 看 LLM leaderboard（这些数据陈旧）。

## 📊 5 维度评分 (质量+速度优先)

| 维度 | 权重 | 硬性 vs 软性 | 典型选项 |
|---|---|---|---|
| **任务类型** | 35% | 软性 | code / reasoning / creative / vision / audio / long-context / multilingual / embedding / chat |
| **质量** | 25% | 软性 | provider tier (TIER1/2/3) + TOP_TIER 匹配 + 模型新鲜度 |
| **速度** | 20% | 软性 | realtime (<500ms) / interactive / batch (按 mini/flash/nano vs opus/pro/thinking 推断) |
| **上下文** | 10% | **硬性下限** | 8K / 32K / 128K / 1M+ |
| **成本** | 10% | **硬性上限** | free / <$1 / $1-3 / $3-10 / >$10 (per M tokens) |
| **隐私** | 过滤 | **硬性** | any / open_weights / on-prem |

**关键设计**:
- 质量+速度 合计 45% 权重，是价格(10%)的 4.5 倍
- 输出含每维度明细分（不只总分）— 同分模型能看出 trade-off
- 硬性约束不满足 → 直接排除（不管其他维度多强）

## 🚀 工作流

### Step 1: 明确需求
回答 5 维度问题，得到 requirements：
```bash
--task code --context 128k --budget 3 --latency interactive --privacy any
```

### Step 2: 拉取数据 (24h cache)
```bash
python3 <skill-path>/scripts/fetch_models.py
# 首次: 联网拉 models.dev/api.json → 写 .cache/models.json
# 后续: cache < 24h 直接读
```

### Step 3: 跑推荐
```bash
python3 <skill-path>/scripts/recommend.py \
    --task code \
    --context 128k \
    --budget 3 \
    --latency interactive \
    --privacy any \
    --top 3
```

### Step 4: 解读输出
脚本同时输出：
- **JSON ranking** (机器可读)
- **Markdown 表格** (人类可读)

每条推荐含: provider, model, score, cost estimate, capability match, fallback chain。

### Step 5: 决策
- 看 score 排序
- 选 1 个 primary + 2 个 fallback
- fallback 链按 cost ↑ / provider diversity 排序

## 💡 决策框架

```
┌─────────────────────────────────────────────────────────────┐
│  快速选 (10 秒) — 用 capability-matrix.md 速查表            │
│  ✓ 已知道大方向 (GPT-5 / Claude / Gemini)                    │
│  ✓ 脑暴阶段，不需要精确评分                                  │
├─────────────────────────────────────────────────────────────┤
│  精细选 (1 分钟) — 用 recommend.py 评分                      │
│  ✓ 多 provider 候选，需精确排序                              │
│  ✓ 有硬性约束 (成本/上下文/隐私)                              │
│  ✓ 需要 fallback 链                                          │
├─────────────────────────────────────────────────────────────┤
│  兜底 (手查) — https://models.dev 完整数据                    │
│  ✓ 上述都失败 / 数据可疑                                      │
│  ✓ 浏览器直观浏览                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📁 依赖

- **数据源**: `https://models.dev/api.json` (anomalyco/models.dev, 社区维护)
- **本地 cache**: `.cache/models.json` (24h TTL，自动刷新)
- **运行时**: Python 3.8+ stdlib (无第三方依赖)
- **路径无关**: 所有脚本用 `Path(__file__).parent` 定位，可从任何 cwd 调用

## 🔧 脚本

- [fetch_models.py](./scripts/fetch_models.py) — 拉取 + 缓存 models.dev 数据
- [recommend.py](./scripts/recommend.py) — 5 维度评分 → top-N 推荐

## 📚 资源

- [examples/](./examples/) — 4 个真实场景案例
- [references/capability-matrix.md](./references/capability-matrix.md) — Top 30 model 静态速查表
- [https://models.dev](https://models.dev) — 官方网站，可视化浏览

## 💡 最佳实践

**Do**:
- 先明确"5 维度"再调用，不要凭印象跑
- 用 fallback 链 (1 primary + 2 fallbacks) 避免单点
- 数据陈旧时手动 `rm .cache/models.json` 强制刷新

**Don't**:
- 不要只看 cost，要看 capability match (一个 0.3 美元的 model 可能不支持 tool_call)
- 不要忽略 latency 约束 (premium model 可能慢)
- 不要在 production 代码里硬编码推荐结果 (价格变化快)
