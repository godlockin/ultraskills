---
name: ai-techbook-translation-review
description: 英文→中文 AI/技术书籍翻译结果 review 工具集 — 核心检查译文是否**正确、完整、可靠**(术语/公式/数据/代码/链接),加分项包括教辅材料、排版美观度、可读性等。生成结构化 report: 必须项 + 加分项 + 综合评分。触发场景: AI/技术书籍翻译验收、Markdown 翻译文档审计、术语一致性核查、公式保留检查、章节覆盖度检查。
version: 1.0.0
tags: [translation, review, audit, ai-techbook, technical-book, markdown, terminology, formula]
---

# AI Techbook Translation Review — AI/技术书籍翻译 Review 工具集

> 沉淀自《The Mathematics, Computer Science, and AI Compendium》中文版翻译 review 全过程 (25 章 + 175 教辅文件 + Pandoc PDF)。

## 🎯 定位 (Positioning)

**核心目标**: 判断译文是否**正确、完整、可靠** — 这是**必须项 (Critical)**。
**次要目标**: 教辅材料、排版美观、可读性 — 这是**加分项 (Bonus)**。

## 📊 Review 报告结构

```
📊 Translation Review Report
├── 1. 必须项 (Critical, 60% 权重)
│   ├── 1.1 术语准确 (Terminology Accuracy)
│   ├── 1.2 公式保留 (Formula Preservation)
│   ├── 1.3 代码完整 (Code Integrity)
│   ├── 1.4 章节覆盖 (Chapter Coverage)
│   ├── 1.5 数据时效 (Data Currency)
│   ├── 1.6 链接可用 (Link Validity)
│   └── 1.7 渲染正确 (Render Correctness)
│
├── 2. 加分项 (Bonus, 40% 权重)
│   ├── 2.1 教辅材料 (Companion Materials)
│   ├── 2.2 排版美观 (Layout Quality)
│   ├── 2.3 内容深度 (Content Depth)
│   ├── 2.4 可读性 (Readability)
│   └── 2.5 时效前沿 (Frontier Coverage)
│
└── 3. 综合评分 (Overall Score)
    ├── 综合得分: X.X / 10
    ├── 通过门槛: 8.0 / 10
    ├── 必须项独立门槛: 9.0 / 10
    └── 修复优先级清单
```

## 🧠 核心理念 (Core Concepts)

### 1. 必须项 vs 加分项

| 类型 | 标准 | 权重 | 不达标后果 |
|------|------|------|------------|
| **必须项** | 0 critical 错误 | 60% | 必须重做 |
| **加分项** | 锦上添花 | 40% | 不影响通过 |

**翻译 review 的本质**: 必须项必须 100% 正确,加分项越多越好。

### 2. 译文正确性的 7 个维度

| 维度 | 检查项 | 自动化工具 |
|------|--------|-----------|
| **术语** | 跨章一致,无混用,无错译 | 术语表对比 |
| **公式** | `$...$` `$$...$$` 内 LaTeX 源码未改 | `audit_translation.py` |
| **代码** | 语法高亮正确,缩进未变 | 字符 diff |
| **章节** | 25 章齐备,小节标题覆盖 | 文件统计 |
| **数据** | 2024+ 数据更新,无过时统计 | 时效审计 |
| **链接** | 内部链接 200,图片 404=0 | 链接检查器 |
| **渲染** | mermaid/KaTeX 正确显示 | `scan_render.py` |

### 3. 多角色独立评审

**4 个独立角色并行 review** (任一角色指出 critical 即修):

| 角色 | 关注 | 触发 |
|------|------|------|
| 术语专家 | 跨章术语一致性 | `--role terminology` |
| 技术专家 | 公式/代码/数据准确性 | `--role technical` |
| 渲染专家 | 文档能否正确显示 | `--role rendering` |
| 完整专家 | 是否漏译/删节 | `--role completeness` |

## 🚀 使用流程 (Workflow)

### Step 1: 准备

```bash
git clone <book-repo>
cd <book-repo>
ls "chapter 01"/   # 英文原版
ls zh/第01章*/     # 中译本
```

### Step 2: 运行自动扫描 (必须项)

```bash
# 1. 翻译对齐度 (章节/公式/图片/链接)
python3 scripts/audit_translation.py --src ./ --target ./zh/

# 2. 渲染检查 (mermaid / KaTeX / math 语法)
python3 scripts/scan_render.py --root ./zh/

# 3. 教辅审计 (加分项)
python3 scripts/audit_companion.py --root ./zh/教辅 --chapters 25
```

### Step 3: 派遣 4 角色 subagent

```bash
# 4 个 reviewer 并行,每个专注 1 个维度
# 详见 templates/review-prompts.md
```

### Step 4: 生成综合 Report

```bash
# 合并 4 角色报告 + 自动扫描结果
python3 scripts/generate_report.py \
  --scan ./scan-results/ \
  --reviews ./reviews/ \
  --output ./translation-review-report.md
```

### Step 5: 输出 report 模板

```markdown
# Translation Review Report

## 📊 综合评分

| 维度 | 权重 | 得分 | 门槛 |
|------|------|------|------|
| 必须项 | 60% | X.X | 9.0 |
| 加分项 | 40% | X.X | 7.0 |
| **综合** | 100% | **X.X** | **8.0** |

**结论**: ✅ 通过 / ❌ 不通过 (必须项 X.X < 9.0)

## 🔴 必须项 (Critical)

### 1.1 术语准确: X.X/10
- ✅ 通过项
- ❌ 问题清单 (严重度排序)

### 1.2 公式保留: X.X/10
...

## 🟢 加分项 (Bonus)

### 2.1 教辅材料: X.X/10
...

## 📋 修复清单 (按优先级)

1. **必修 (Critical)**: X 项
2. **建议修 (Important)**: X 项
3. **可选 (Minor)**: X 项
```

## 📦 工具集

### scripts/

| 文件 | 用途 | 类型 |
|------|------|------|
| `audit_translation.py` | 翻译对齐度审计 | 必须 |
| `scan_render.py` | 渲染报错扫描 | 必须 |
| `audit_companion.py` | 教辅 7 件套审计 | 加分 |
| `generate_report.py` | 合并报告生成 | 必须 |
| `term_check.py` | 术语一致性检查 | 必须 |

### templates/

| 文件 | 用途 |
|------|------|
| `review-prompts.md` | 4 角色评审 prompt 模板 |
| `report-template.md` | 最终 report 模板 |
| `terminology-template.md` | 术语表模板 |

### examples/

| 文件 | 用途 |
|------|------|
| `typical-report.md` | 典型 report 示例 |
| `good-translation.md` | 优秀翻译案例 |
| `common-issues.md` | 翻译常见问题 |

## 🎓 案例研究

**项目**: maths-cs-ai-compendium 中文版 (25 章)

| 阶段 | 必须项 | 加分项 |
|------|--------|--------|
| 初译稿 | 6.5/10 | 8.0/10 |
| 渲染修复 | 9.5/10 | 8.5/10 |
| 前沿更新 | 9.2/10 | 9.0/10 |
| **最终** | **9.2/10** | **9.0/10** |

**关键经验**:
- 必须项 1.0 改进需要 90% 工作量
- 加分项提升到 9.0+ 比从 8.0 提升到 8.5 难 3 倍
- 教辅质量不影响翻译本身的"正确性"
- 公式/术语是翻译 review 的"硬指标"

## 📝 更新日志

**v1.0.0 (2026-07-31)**
- 初版: 翻译 review 工具集
- 7 个必须项 + 5 个加分项
- 4 角色评审框架
- 自动扫描 + 手动评审合并