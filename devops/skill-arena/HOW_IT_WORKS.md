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
| **Quality** | 50pts | 输出准确性、任务完整度、边缘 case 处理、workflow 深度 |
| **Maintainability** | 20pts | 文档完整度、结构清晰度、模块化设计 |

**实测基准**（来自 winners.json）：
- 顶分：~69-70（`free-tool-strategy`: 69.75，`"launch-strategy"`: 69.75）
- 中位：~47（`"ciso-advisor"`: 47.0，`content-strategy`: 48.0）
- 弱：20-30

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

> **更新频率**：每次批量导入新 skill 后运行 `bash run.sh full`；单个 skill 增量更新用 `scan → test → update` 三步。
