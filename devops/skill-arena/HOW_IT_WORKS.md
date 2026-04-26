# Skill Arena — How It Works

Skill Arena 是 UltraSkills 库的质量排名系统。从 562 个 skill 中，按类别选出最优 champion，并将评分写回 `index.json`，驱动 hub 搜索排序。

---

## 1. 输出文件

| 文件 | 内容 |
|------|------|
| `clusters.json` | 562 个 skill 分组到 39 个语义 cluster，含 skill 元数据 |
| `winners.json` | 每个 cluster 的冠军 skill + 被击败列表 + 评分明细 |
| `index.json` | 主索引，每个 skill 写入 `arena` 字段（score、is_winner、rank、category） |

---

## 2. 评分公式

```
总分 = Speed(30%) + Quality(50%) + Maintainability(20%) = max 100pts
```

| 维度 | 权重 | 评分依据 |
|------|------|----------|
| **Speed** | 30pts | 指令清晰度、token 效率、Claude 执行速度 |
| **Quality** | 50pts | 见下方子维度拆解 |
| **Maintainability** | 20pts | 文档完整度、结构清晰度、模块化设计 |

### Quality (50%) 子维度拆解

| 子维度 | 权重 | 说明 |
|--------|------|------|
| **accuracy**（准确性） | 20% | 输出是否正确回答了任务目标；结论是否无误、无幻觉 |
| **executability**（可执行性） | 20% | 给出的建议/步骤是否可操作；避免空洞的"最佳实践"泛言 |
| **boundary_coverage**（边界覆盖） | 10% | 是否处理了边缘场景、异常路径、corner case |

> **当前状态**：`index.json` / `winners.json` 中的 `quality` 字段为合并分值（满分 50），子维度尚未单独存储。未来可将 `scores.quality` 扩展为 `{accuracy, executability, boundary_coverage}` 对象以支持更细粒度分析（见第 9 节 ELO 扩展说明）。

**实测基准**（来自 winners.json）：
- 顶分：~69-70（`free-tool-strategy`: 69.75，`"launch-strategy"`: 69.75）
- 中位：~47（`"ciso-advisor"`: 47.0，`content-strategy`: 48.0）
- 弱：20-30

---

## 2.2 长度惩罚规则（Length Penalty）

借鉴 AlpacaEval 的 length-controlled win-rate 思路，防止 verbose skill 通过堆砌输出虚高得分。

**规则**：若 skill 输出 token 数超过"参考长度"的 **1.5 倍**，Quality 分自动降低 **10%**。

```
参考长度 = 该 cluster 内所有 skills 输出的中位数长度（token 数）

if output_tokens > reference_length * 1.5:
    quality_score *= 0.90
```

**参考长度定义**：每次 `test` 阶段记录每个 skill 的输出 token 数，取 cluster 内所有 skills 的中位数作为 `reference_length`，存入 `clusters.json` 的 `median_output_tokens` 字段。

**目的**：消除长度偏见（length bias）。LLM judge 倾向于将更长的输出评为更高质量，该惩罚机制抵消此偏差，确保 Quality 分真正反映信息密度而非信息量。

---

## 3. Cluster 结构（39个类别）

| Cluster ID | 名称 | Skill 数 |
|-----------|------|---------|
| cluster-001 | eng-code-quality | 30 |
| cluster-002 | eng-testing | 24 |
| cluster-003 | eng-architecture | 43 |
| cluster-004 | eng-devops | 44 |
| cluster-005 | eng-security | 25 |
| cluster-006 | seo-technical | 2 |
| cluster-007 | seo-content | 10 |
| cluster-008 | cro-landing | 8 |
| cluster-009 | cro-form | 11 |
| cluster-010 | cro-funnel | 8 |
| cluster-011 | cro-ab-testing | 6 |
| cluster-012 | content-copywriting | 5 |
| cluster-013 | content-strategy | 3 |
| cluster-014 | content-social | 8 |
| cluster-015 | content-email | 7 |
| cluster-016 | marketing-analytics | 5 |
| cluster-017 | marketing-paid | 5 |
| cluster-018 | marketing-growth | 10 |
| cluster-019 | product-strategy | 2 |
| cluster-020 | product-discovery | 83 |
| cluster-021 | product-ux | 19 |
| cluster-022 | agent-context | 8 |
| cluster-023 | agent-workflow | 5 |
| cluster-024 | agent-tool | 7 |
| cluster-025 | agent-bdi | 1 |
| cluster-026 | devops-mcp | 8 |
| cluster-027 | data-analysis | 18 |
| cluster-028 | data-docs | 5 |
| cluster-029 | video-editing | 18 |
| cluster-030 | video-media | 9 |
| cluster-031 | sales-outreach | 2 |
| cluster-032 | sales-enablement | 3 |
| cluster-033 | business-strategy | 6 |
| cluster-034 | business-finance | 5 |
| cluster-035 | compliance-ra | 42 |
| cluster-036 | compliance-qm | 12 |
| cluster-037 | compliance-security | 2 |
| cluster-038 | creative-visual | 5 |
| cluster-039 | other | 204 |

每个 cluster 描述格式：`{名称} - {领域描述}`，例如 `eng-code-quality - code analysis, bug detection, best practices`。

---

## 4. PK 机制（Challenger 挑战赛）

新 skill 进入流程：

```
新 skill 加入库
    ↓
scan → 自动分配到最匹配的 cluster
    ↓
test → LLM judge 对该 skill 打分（Speed/Quality/Maintainability）
    ↓
compare → 与当前 cluster winner 比分
    ↓
新分 > 当前冠军分  → 新 skill 成为 winner，旧冠军进入 defeated 列表
新分 ≤ 当前冠军分  → 当前 winner 保持，新 skill 记入 defeated 列表
```

`winners.json` 结构示例：
```json
{
  "category": "marketing-growth",
  "skill_id": "free-tool-strategy",
  "score": 69.75,
  "scores": {
    "speed": 30.0,
    "quality": 23.75,
    "maintainability": 16.0,
    "total": 69.75
  },
  "defeated": [
    "x-twitter-growth",
    "referral-program",
    "community-marketing",
    "cmo-advisor",
    ...
  ]
}
```

---

## 5. 运行命令

```bash
# 环境准备（自动加载 auth/.env 或 .env）
cd devops/skill-arena
bash run.sh <subcommand>
```

| 子命令 | 作用 |
|--------|------|
| `scan` | 扫描所有 skill，执行语义聚类，更新 clusters.json |
| `test` | 对各 cluster 内 skill 跑 PK 测试（调用 LLM judge） |
| `report` | 生成 benchmark 报告到 `reports/` |
| `update` | 将 arena 评分写入 index.json |
| `full` | 全流程：scan → test → report → update |
| `backtrack` | 用新 test case 重跑所有 skill（重新评分） |

**新增 skill 后的增量更新流程：**

```bash
# 1. 将新 skill 加入库（复制目录、更新 index.json）
# 2. 重新聚类（新 skill 分配 cluster）
bash run.sh scan

# 3. 只跑新 skill 的 PK 测试
bash run.sh test

# 4. 写回评分到 index.json
bash run.sh update
```

脚本依赖文件：
- `scripts/skill-arena.py` — 主入口，解析子命令
- `scripts/cluster_skills.py` — 语义聚类逻辑
- `scripts/run_benchmarks.py` — LLM 调用 + PK 评测
- `scripts/score_results.py` — 分数计算与排名
- `scripts/llm_judge.py` — LLM judge wrapper
- `scripts/update_index.py` — 写回 index.json
- `scripts/generate_report.py` — 报告生成

---

## 6. 评分影响 Hub 搜索排序

`search.py` 中，arena 评分通过以下方式影响搜索结果排序：

```python
# 关键词命中 > 0 时，叠加 arena bonus
if is_winner and keyword_score >= 10:
    score += 15          # winner 大奖励（仅对相关查询有效）
elif is_winner:
    score += 5           # winner 小奖励（关键词弱匹配）

score += arena_score * 0.10          # arena总分贡献（max +10pts）
score += quality_score * 0.15        # quality维度贡献（max +7.5pts）
score += maintainability_score * 0.10  # 可维护性贡献（max +2pts）

# browse 模式（无关键词）：纯 arena 驱动排序
score = arena_score * 0.10 + is_winner * 15 + quality * 0.15
```

**设计原则**：winner bonus 仅在关键词匹配 ≥ 10pts 时触发，防止无关 winner 排名超过高度相关的 non-winner。

---

## 7. 文件结构

```
devops/skill-arena/
├── HOW_IT_WORKS.md          # 本文档
├── IMPLEMENTATION_SUMMARY.md # 实现细节摘要
├── README.md                 # 对外说明
├── SKILL.md                  # Arena 本身作为 skill 的定义
├── run.sh                    # 启动脚本（加载 env → 调用 skill-arena.py）
├── requirements.txt          # Python 依赖
├── clusters.json             # 562 skills × 39 clusters（auto-generated）
├── winners.json              # 39 cluster winners（auto-generated）
├── .no-skill                 # 标记此目录非普通 skill
├── scripts/
│   ├── skill-arena.py        # 主入口
│   ├── cluster_skills.py     # 语义聚类
│   ├── run_benchmarks.py     # LLM PK 测试
│   ├── score_results.py      # 评分计算
│   ├── llm_judge.py          # LLM judge 封装
│   ├── llm_invoker.py        # LLM API 调用层
│   ├── expert_panels.py      # 专家评审面板
│   ├── expert_collaboration.py # 多专家协作
│   ├── update_index.py       # 写回 index.json
│   ├── generate_report.py    # 报告生成
│   └── design_tests.py       # 测试用例设计
├── reports/                  # 历次 benchmark 报告
├── test-suites/              # 测试用例集
├── examples/                 # 使用示例
└── templates/                # 模板
```

---

## 8. 实战示例：`free-tool-strategy` 夺冠 marketing-growth

**背景**：`marketing-growth` cluster 共 10 个 skill，包括 `referral-program`、`community-marketing`、`x-twitter-growth` 等。

**Skill 描述**：`free-tool-strategy` — 免费工具增长策略，指导如何通过构建免费工具获取有机流量和用户。

**评分过程**：
- Speed: **30.0** — 指令直接，Claude 可立即执行，无歧义
- Quality: **23.75** — 策略完整，覆盖工具选型、SEO 价值、转化路径等关键维度，边缘 case 处理良好
- Maintainability: **16.0** — 文档结构清晰，有示例，模块化

**总分：69.75**（全库最高分之一）

**PK 结果**：
- 击败 `referral-program`、`community-marketing`、`cmo-advisor`、`x-twitter-growth` 等 9 个 challenger
- 成为 `marketing-growth` cluster champion
- `is_winner: true` 写入 index.json

**Hub 搜索影响**：
- 搜索 "growth strategy" → keyword 命中 ≥ 10pts → winner bonus +15 触发
- 总 match_score 显著领先同类 skill，排名第一

---

---

## 9. 增量更新：ELO 机制

### 设计动机

全量重测（`bash run.sh full`）代价高，需为所有 562 个 skill 调用 LLM judge。ELO 机制将新 skill 的入场成本压缩到**1次 pairwise 对战**。

### ELO 更新公式

```
new_rating = old_rating + K × (actual - expected)
```

| 参数 | 值 | 说明 |
|------|----|------|
| `K` | 32 | 标准国际象棋 K 因子，变化幅度适中 |
| `actual` | 1（胜）/ 0.5（平）/ 0（负） | 本次对战结果 |
| `expected` | `1 / (1 + 10^((R_opponent - R_self) / 400))` | 基于当前 rating 的胜率预期 |

### 触发时机

```
新 skill 加入 cluster
    ↓
仅 vs 当前 cluster champion（1次 pairwise）
    ↓
胜负判定：arena 总分（Speed+Quality+Maintainability）高者胜
    ↓
双方 ELO 同步更新（零和：winner +K×(1-expected)，loser -K×expected）
    ↓
新 skill 总分 > champion → 夺冠 + ELO 更新
新 skill 总分 ≤ champion → 保持现状 + ELO 更新
```

### clusters.json 扩展字段（未来 schema）

当前 `clusters.json` 每个 skill entry 包含基础元数据。未来可添加 `elo_rating` 字段：

```json
{
  "cluster_id": "cluster-018",
  "cluster_name": "marketing-growth",
  "skills": [
    {
      "skill_id": "free-tool-strategy",
      "arena_score": 69.75,
      "elo_rating": 1523,        // 新增：ELO rating（初始值 1500）
      "elo_matches": 9,          // 新增：参与过的 ELO 对战次数
      "is_champion": true
    }
  ]
}
```

> **当前状态**：`clusters.json` 尚未存储 `elo_rating`，此为设计预留字段。实现时在 `score_results.py` 中增加 ELO 计算逻辑即可，无需改动其他脚本。

### 好处

- **边际成本极低**：新增1个 skill 只需1次 LLM 调用（vs champion），而非562次
- **历史评分不失效**：旧 skill 的 ELO 通过对战自然收敛，无需重测
- **连续排名**：ELO 提供比"winner/defeated"二值更细粒度的相对强度信息

---

> **更新频率**：每次批量导入新 skill 后运行 `bash run.sh full`；单个 skill 增量更新用 `scan → test → update` 三步；未来启用 ELO 后，增量更新仅需1次 vs champion 对战。

---

## 10. 评分可重复性

LLM judge 存在非确定性，同一 skill 多次评分结果可能浮动。以下规范确保评分稳定可信。

### 推荐策略

**方案 A：固定 seed（快速，单次）**
- 调用 LLM 时传入 `seed=42`（支持该参数的模型，如 OpenAI）
- 相同 seed + 相同输入 → 结果确定性最高

**方案 B：多次采样取中位数（稳健，推荐）**
- 对每个 skill 独立评分 **N=3** 次
- 取三次得分的**中位数**作为最终分数
- 可同时记录最大值/最小值，供稳定性分析

```python
scores = [judge(skill) for _ in range(3)]
final_score = sorted(scores)[1]  # 中位数
```

### 稳定性判定标准

使用**变异系数（CV，Coefficient of Variation）**衡量评分稳定性：

```
CV = 标准差 / 均值 × 100%
```

| CV 值 | 判定 | 处置 |
|-------|------|------|
| < 10% | ✅ 稳定，评分可信 | 正常写入 index.json |
| 10%–20% | ⚠️ 轻微抖动 | 增加采样至 N=5，取中位数 |
| > 20% | ❌ 不稳定 | 检查 prompt / judge 设计，不写入 |

### 示例

```
skill: free-tool-strategy
采样 3 次: [69.0, 69.75, 70.5]
均值: 69.75  标准差: 0.61  CV: 0.87% → ✅ 稳定
```
