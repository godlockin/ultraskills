# UltraSkills Evaluation System

> **Arena Version**: 1.0.0
> **Last Updated**: 2026-05-08

---

## Overview

UltraSkills Arena 采用多维度评估体系，对每个 skill 进行量化打分，确保库内技能质量可衡量、可比较、可持续优化。

## 评分维度

每个技能从三个维度评估，权重相等（各 33.3%）：

### 1. 文档质量 (Documentation Quality)

**评分范围**: 0-10 分

**评估标准**:

| 分数 | 标准 |
|------|------|
| 10 | SKILL.md frontmatter 完整（name/description/version/tags），包含 examples/、references/、scripts/ 至少2个，描述清晰具体 |
| 8-9 | Frontmatter 完整，包含 examples/ 或 references/，描述清晰 |
| 6-7 | Frontmatter 基本完整，缺少 version 或 tags，描述简略 |
| 4-5 | Frontmatter 不完整，缺少多个必需字段，无示例 |
| 0-3 | 仅有 SKILL.md，无 frontmatter 或格式错误 |

**检查项**:
- [ ] YAML frontmatter 存在且格式正确
- [ ] `name` 字段清晰（kebab-case）
- [ ] `description` 字段具体（非泛泛而谈）
- [ ] `version` 字段存在（语义化版本号）
- [ ] `tags` 字段存在且相关（至少2个）
- [ ] `examples/` 目录存在且有实质内容
- [ ] `references/` 或 `scripts/` 至少一个存在

### 2. 功能明确性 (Functional Clarity)

**评分范围**: 0-10 分

**评估标准**:

| 分数 | 标准 |
|------|------|
| 10 | 明确的触发条件，具体的使用场景（3+），清晰的输出预期，差异化价值明显 |
| 8-9 | 触发条件清晰，使用场景具体（2+），输出预期明确 |
| 6-7 | 触发条件模糊，使用场景泛泛，输出预期不明确 |
| 4-5 | 功能描述抽象，与其他 skills 高度重复 |
| 0-3 | 功能不明确，纯通用提示词 |

**检查项**:
- [ ] 明确说明「何时使用此 skill」
- [ ] 提供具体使用场景（非「帮助用户」等泛泛描述）
- [ ] 说明预期输出（报告/代码/设计/建议等）
- [ ] 与同类 skills 有明显差异化
- [ ] 避免万能 skill（"通用助手"类）

### 3. 可维护性 (Maintainability)

**评分范围**: 0-10 分

**评估标准**:

| 分数 | 标准 |
|------|------|
| 10 | 代码结构清晰（如有），版本控制规范，tags 组织良好，依赖明确 |
| 8-9 | 结构清晰，版本控制存在，tags 基本合理 |
| 6-7 | 结构松散，版本号缺失，tags 随意 |
| 4-5 | 无结构，无版本控制，tags 混乱 |
| 0-3 | 单文件堆砌，无组织 |

**检查项**:
- [ ] 脚本代码有注释和模块划分（如适用）
- [ ] 版本号遵循语义化版本（SemVer）
- [ ] Tags 使用标准词汇（参考 CONTRIBUTING.md）
- [ ] 依赖项明确列出（Python/Node.js/外部工具）
- [ ] 文件结构符合模板标准

## 最终得分计算

```
final_score = (doc_quality + func_clarity + maintainability) / 3
```

**示例**:
- 文档质量: 10/10（完整 frontmatter + examples + references）
- 功能明确性: 9/10（清晰触发条件 + 3个具体场景 + 明确输出）
- 可维护性: 9/10（版本控制 + 标准 tags + 依赖明确）
- **最终得分**: (10 + 9 + 9) / 3 = **9.3/10**

## 聚类逻辑

Skills 按功能语义自动聚类为 54 个类别：

| 类别 | Skills 数量 |
|------|-------------|
| 其他未分类 | 49 |
| 工程·代码质量 | 30 |
| 工程·全栈工程师 | 25 |
| 内容·社交媒体 | 24 |
| Skills·管理 | 23 |
| 商业·高管顾问 | 22 |
| 内容·视频 | 21 |
| 工程·DevOps | 21 |
| 营销·策略 | 21 |
| 内容·写作 | 19 |
| 工程·架构 | 19 |
| Agent·AgentHub协作 | 18 |
| 内容·图像设计 | 18 |
| 教育·学习研究 | 16 |
| 工程·安全 | 15 |
| 人物·视角模拟 | 15 |
| 数据·分析 | 14 |
| 营销·转化率优化 | 13 |
| 内容·文档生成 | 12 |
| Skills·浏览器 | 12 |

*...and 34 more clusters*

**聚类规则**:
- 基于 description、tags、recommended_for 语义相似度
- 使用层次聚类算法（距离阈值自适应）
- LLM 辅助审核边界案例
- 每个聚类选出得分最高者为 Winner

## 分级标准

| 等级 | 分数范围 | 说明 |
|------|----------|------|
| S-Tier | 9.0-10.0 | 完美或卓越，推荐优先使用 |
| A-Tier | 8.0-8.9 | 优秀，质量可靠 |
| B-Tier | 7.0-7.9 | 良好，基本可用 |
| C-Tier | 6.0-6.9 | 及格，需改进 |
| D-Tier | 4.0-5.9 | 不及格，建议重构 |
| F-Tier | 0-3.9 | 淘汰候选 |

**淘汰机制**:
- 连续 3 轮评测 < 4.0 分 → 进入淘汰候选名单
- 手动审核确认后，从库中移除
- 淘汰记录存档到 `skill-arena/eliminated.json`

## 评测流程

```bash
# Step 1: 扫描所有 SKILL.md
python3 scripts/arena_scan.py
# Output: skill-arena/skills_inventory.json

# Step 2: 聚类 + 评分
python3 scripts/arena_cluster_score.py
# Output: skill-arena/{clusters, scores, winners}.json

# Step 3: 重建主索引
python3 scripts/arena_build_index.py
# Output: index.json
```

## 持续改进

- **每周**: 自动扫描新增 skills
- **每月**: 重新评测所有 skills（规则可能更新）
- **按需**: 用户反馈触发重评

---

*评分标准持续演进，详见 [CONTRIBUTING.md](../CONTRIBUTING.md)*
