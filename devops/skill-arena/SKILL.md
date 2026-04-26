---
name: skill-arena
description: 自动扫描项目 skills，通过 LLM 自主聚类分组，设计测试用例并执行 PK 测试，基于速度 + 质量 + 可维护性加权打分选出胜者，持续迭代测试用例并更新 index.json 添加优先级和适用场景标签
version: 1.0.0
tags: [devops, automation, testing, benchmark, skill-management]
---

# Skill Arena - AI Skills 竞技测试框架

> 自动发现、聚类、测试和评级项目中的所有 AI skills，通过持续迭代的测试用例和打擂台机制，选出每个类别的最佳技能。

## 🎯 目标 (Goal)

- **自动发现 (Auto-Discovery)**: 扫描项目，识别所有可用的 skills
- **智能聚类 (Smart Clustering)**: 使用 LLM 分析技能语义，自动分组相似 skills
- **PK 测试 (PK Testing)**: 为每组技能设计测试用例，执行对比测试
- **综合评分 (Weighted Scoring)**: 基于速度 (30%) + 质量 (50%) + 可维护性 (20%) 加权打分
- **胜者榜单 (Winner's List)**: 选出每组最佳技能，标记到 index.json
- **持续迭代 (Continuous Iteration)**: 每次新技能加入时重新测试，测试用例持续优化
- **回溯机制 (Backtracking)**: 测试用例升级后，重新评估所有历史 skills

---

## 🧠 核心理念 (Core Concepts)

### 专家小组召唤 (Expert Panel Summoning)

每个类别的技能都由对应的领域专家小组共同设计测试用例：

```
┌────────────────────────────────────────────────────────────────┐
│                    Expert Panel Structure                       │
├────────────────────────────────────────────────────────────────┤
│  Category    │  Panel Name              │  Expert Count       │
│  ─────────   │  ──────────              │  ────────────       │
│  cro         │  CRO Expert Panel        │  4 专家             │
│  seo         │  SEO Expert Panel        │  4 专家             │
│  engineering │  Engineering Expert Panel│  4 专家             │
│  product     │  Product Expert Panel    │  4 专家             │
│  marketing   │  Marketing Expert Panel  │  4 专家             │
│  ...         │  ...                     │  ...                │
└────────────────────────────────────────────────────────────────┘
```

**专家协作流程：**
1. **召唤专家** - 根据类别召唤对应专家团队
2. **圆桌讨论** - 每位专家从专业视角提出测试建议
3. **交叉评审** - 专家互相评审和完善测试用例
4. **共识建立** - 形成最终测试套件

### 评分维度

```
┌─────────────────────────────────────────────────────────────┐
│                    Skill Performance                        │
├─────────────────────────────────────────────────────────────┤
│  速度 (30%)           质量 (50%)          可维护性 (20%)    │
│  ─────────            ────────            ────────────      │
│  • 响应时间           • 输出准确性         • 代码复杂度       │
│  • Token 效率          • 任务完成度         • 文档完整性       │
│  • 并发能力           • 边界条件处理       • 测试覆盖率       │
│  • 缓存命中率         • 错误处理质量       • 模块耦合度       │
└─────────────────────────────────────────────────────────────┘

总分 = (速度分 × 0.30) + (质量分 × 0.50) + (可维护性分 × 0.20)

> ⚠️ **长度惩罚**：若 skill 输出 token 数超过 cluster 内中位数长度的 **1.5 倍**，Quality 分自动降 **10%**（防止 verbose skill 虚高得分，消除 length bias）。详见 HOW_IT_WORKS.md §2.1。
```

### 聚类维度

技能按以下维度进行语义聚类：

1. **功能域**: engineering, marketing, product, design, devops, etc.
2. **任务类型**: analysis, creation, review, optimization, debugging
3. **输入类型**: code, text, image, data, config
4. **输出类型**: report, code, design, recommendation, transformation
5. **复杂度级别**: beginner, intermediate, advanced, expert

### 打擂台机制

```
新 Skill 加入
    │
    ▼
┌───────────────────┐
│ 1. 语义分析       │ → 确定所属类别
└───────────────────┘
    │
    ▼
┌───────────────────┐
│ 2. 查找当前胜者   │ → 从 winners.json 获取
└──────────┬────────┘
           │
    ┌──────┴──────┐
    │  有胜者？    │
    ├──────┬──────┤
       是        否
    │           │
    ▼           ▼
┌─────────┐ ┌──────────┐
│ PK 测试  │ │ 直接当选 │
└────┬────┘ └────┬─────┘
     │           │
     ▼           ▼
┌──────────────────┐
│ 3. 更新胜者榜单   │
└──────────────────┘
```

---

## 🚀 使用流程 (Workflow)

### 触发方式

```text
/skill-arena scan         # 扫描所有 skills 并聚类
/skill-arena test         # 执行 PK 测试
/skill-arena report       # 生成测试报告
/skill-arena update       # 更新 index.json 添加评级
/skill-arena full         # 完整流程：扫描→聚类→测试→报告→更新
/skill-arena backtrack    # 用新测试用例重新测试所有 skills
```

---

### 完整工作流程

#### Phase 1: 扫描与聚类

**Step 1.1: 扫描项目**
```bash
python scripts/skill-arena.py scan --project ./
```

扫描范围:
- `index.json` 中注册的所有 skills
- `community/`, `engineering/`, `external/*/` 等目录
- 所有包含 `SKILL.md` 或 `skill.md` 的目录

**Step 1.2: 语义分析**
```bash
python scripts/skill-arena.py analyze
```

对每个 skill 分析:
- 提取 SKILL.md 中的 name, description, tags
- 使用 LLM 生成功能嵌入向量
- 分析代码结构（如有）

**Step 1.3: 自动聚类**
```bash
python scripts/skill-arena.py cluster
```

聚类算法:
1. 计算技能间的语义相似度
2. 使用层次聚类或 DBSCAN
3. LLM 审核聚类结果，调整边界案例
4. 输出聚类报告

**Step 1.4: 输出聚类结果**
```
clusters/
├── cluster-001-cro/
│   ├── skills: [page-cro, signup-flow-cro, popup-cro, ...]
│   └── description: "Conversion Rate Optimization skills"
├── cluster-002-seo/
│   ├── skills: [seo-audit, ai-seo, schema-markup, ...]
│   └── description: "SEO optimization and audit skills"
└── ...
```

---

#### Phase 2: 设计测试用例

**Step 2.1: 为每个聚类设计测试**
```bash
python scripts/skill-arena.py design-tests --cluster cluster-001-cro
```

测试用例设计原则:
- **代表性**: 覆盖该类别 80% 以上的使用场景
- **可比性**: 所有技能都能执行相同的测试任务
- **渐进性**: 从简单到复杂，分层评估
- **可量化**: 每个测试都有明确的评分标准

**Step 2.2: 测试用例结构**
```yaml
# clusters/cluster-001-cro/tests.yaml
cluster: cluster-001-cro
name: "CRO Skills Benchmark"
version: 1.0.0

test_cases:
  - id: tc-001
    name: "首页转化率分析"
    description: "分析给定 landing page 并提供 CRO 建议"
    input:
      type: url
      value: "https://example.com/landing"
    expected_outputs:
      - "识别至少 3 个转化障碍"
      - "提供具体的优化建议"
      - "包含优先级排序"
    scoring:
      speed:
        - "响应时间 < 5s: 10 分"
        - "5-10s: 7 分"
        - "> 10s: 4 分"
      quality:
        - "建议可执行性: 1-10 分"
        - "问题识别准确性: 1-10 分"
      maintainability:
        - "输出结构清晰度: 1-10 分"

  - id: tc-002
    name: "A/B 测试方案设计"
    description: "为给定的转化问题设计 A/B 测试"
    # ...
```

---

#### Phase 3: 执行 PK 测试

**Step 3.1: 批量执行测试**
```bash
python scripts/skill-arena.py run --cluster cluster-001-cro --parallel
```

执行过程:
1. 为每个技能分配相同的测试任务
2. 并行执行测试（可配置并发数）
3. 收集执行结果和指标
4. 记录详细日志

**Step 3.2: 评分与排名**
```bash
python scripts/skill-arena.py score --cluster cluster-001-cro
```

评分流程:
1. **自动评分**: 执行预定义的评分规则
2. **LLM 评估**: 使用独立 LLM 评估输出质量
3. **加权计算**: 按 30/50/20 权重计算总分
4. **排名生成**: 生成排行榜

---

#### Phase 4: 生成报告与更新

**Step 4.1: 生成测试报告**
```bash
python scripts/skill-arena.py report --output reports/skill-arena-report.md
```

报告结构:
```markdown
# Skill Arena Benchmark Report

## Executive Summary
- 测试日期：2026-03-09
- 参测 Skills: 292
- 聚类组数：45
- 测试用例总数：180

## Winners by Category

### 🏆 CRO Skills
| Rank | Skill | Speed | Quality | Maintainability | Total |
|------|-------|-------|---------|-----------------|-------|
| 1    | page-cro | 28/30 | 47/50 | 18/20 | 93/100 |
| 2    | signup-flow-cro | 25/30 | 44/50 | 17/20 | 86/100 |

### 🏆 SEO Skills
...

## Detailed Results
...

## Test Case Coverage
...
```

**Step 4.2: 更新 index.json**
```bash
python scripts/skill-arena.py update-index
```

更新内容:
```json
{
  "skills": [
    {
      "id": "page-cro",
      "name": "Page Conversion Rate Optimization",
      "path": "./community/page-cro/SKILL.md",
      "description": "...",
      "tags": ["cro", "marketing", "optimization"],
      "arena": {
        "rank": 1,
        "category": "cro",
        "score": 93,
        "scores": {
          "speed": 28,
          "quality": 47,
          "maintainability": 18
        },
        "is_winner": true,
        "test_date": "2026-03-09",
        "test_version": "1.0.0"
      },
      "recommended_for": ["landing-page-review", "conversion-audit", "cro-consultation"]
    }
  ]
}
```

---

## 📊 数据结构

### 聚类结果 (clusters.json)
```json
{
  "version": "1.0.0",
  "updated_at": "2026-03-09",
  "clusters": [
    {
      "id": "cluster-001",
      "name": "cro",
      "description": "Conversion Rate Optimization skills",
      "skills": ["page-cro", "signup-flow-cro", "popup-cro"],
      "winner": "page-cro",
      "test_count": 5
    }
  ]
}
```

### 胜者榜单 (winners.json)
```json
{
  "version": "1.0.0",
  "updated_at": "2026-03-09",
  "winners": [
    {
      "category": "cro",
      "skill_id": "page-cro",
      "score": 93,
      "challenged_at": "2026-03-09",
      "defeated": ["signup-flow-cro", "popup-cro"]
    }
  ]
}
```

### 测试用例库 (test-suites/)
```
test-suites/
├── cro/
│   ├── tests.yaml
│   ├── expected-outputs/
│   └── scoring-rules.yaml
├── seo/
│   └── ...
└── ...
```

---

## 📜 脚本

- `scripts/skill-arena.py` - 主程序入口
- `scripts/cluster_skills.py` - 技能聚类
- `scripts/design_tests.py` - 测试用例设计
- `scripts/run_benchmarks.py` - 执行基准测试
- `scripts/score_results.py` - 评分与排名
- `scripts/update_index.py` - 更新 index.json

---

## 💡 最佳实践 (Best Practices)

- **Do**: 每次新 skill 加入时自动触发 PK 测试
- **Do**: 定期（如每月）回溯测试，确保胜者仍是最佳
- **Do**: 测试用例版本化，记录每次变更
- **Don't**: 不要手动修改测试结果，保持客观
- **Don't**: 测试用例应覆盖边界场景，不仅是正常流程

---

## 🔄 持续迭代机制

### 测试用例升级流程

1. **收集反馈**: 记录每次测试的不足和边缘案例
2. **分析缺口**: 识别未被覆盖的场景
3. **设计新用例**: 添加补充测试
4. **版本升级**: `test_version += 1`
5. **回溯测试**: 重新测试所有历史 skills
6. **更新榜单**: 如胜者变更，记录变更日志

### 变更日志示例
```json
{
  "test_versions": [
    {
      "version": "1.1.0",
      "date": "2026-03-15",
      "changes": ["添加边界条件测试 tc-006", "优化质量评分权重"],
      "winner_changes": [
        {"category": "cro", "old": "page-cro", "new": "signup-flow-cro"}
      ]
    }
  ]
}
```

---

## 📚 资源引用

- [示例：测试报告模板](./templates/benchmark-report.md)
- [示例：测试用例设计](./examples/cro-tests.yaml)
- [聚类算法实现](./scripts/cluster_skills.py)
