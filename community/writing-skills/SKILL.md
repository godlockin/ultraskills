---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
version: 2.0.0
tags: [community]
---

# Writing Skills

> **Writing skills IS Test-Driven Development applied to process documentation.**
>
> 主体只保留:触发条件 + 核心铁律 + 高层索引。所有"如何做"的细节 → references/。

## 📌 何时该用本 skill

| 触发 | 例句 |
|---|---|
| **创建新 skill** | "写个新 skill / 创造 skill / 新增 skill 到项目" |
| **修改现有 skill** | "改这个 skill / 修一下 skill / 优化 SKILL.md" |
| **验证 skill** | "这个 skill 能用吗 / 测一下 skill 是否生效" |
| **批量生产** | "批量蒸馏 5 个人的思维框架" / "扫外部 repo 拿 best-of" |

## 🎯 核心铁律 (Iron Law)

> **「先写测试,再写 skill。」** — 与 [test-driven-development](../test-driven-development/) 同一 RED-GREEN-REFACTOR 循环。
>
> **If you didn't watch an agent fail WITHOUT the skill, you don't know if the skill teaches the right thing.**

**3 个强制阶段**:

```
RED    → 写失败测试 (3+ combined pressure scenarios + baseline 行为记录)
GREEN  → 写最小 skill (description + overview + 必要 code example)
REFACTOR → 关 loophole (rationalizations table + red flags list)
```

**Deploying untested skills = deploying untested code. 违反质量底线。**

---

## 🧩 Skill 3 大类型(决定写多深)

| 类型 | 内容 | 适用 |
|---|---|---|
| **Technique** | how-to 步骤、code examples | 写命令、写流程 |
| **Pattern** | 思维框架 + 何时用 + 如何用 | 决策框架、思维模型 |
| **Reference** | API/格式文档、索引 | 静态知识 |

→ 详细内容 + 各类型模板: [`references/skill-types-and-templates.md`](references/skill-types-and-templates.md)

---

## 🏗️ 目录结构标准

```
skill-name/
├── SKILL.md              # 主体 < 500 行
├── examples/             # 至少 1-3 个 case
├── scripts/              # 可选:自动化
├── references/           # 按需加载(详细内容)
└── templates/            # 可选:模板
```

→ 完整目录模板 + 各场景(自包含 / 带工具 / 重 reference): [`references/directory-structure.md`](references/directory-structure.md)

---

## 🔍 Claude Search Optimization (CSO) · 4 大要素

> **CSO 是 skill 被 Claude 正确触发的关键。** description 必须既说"做什么"又说"何时用"。

| # | 要素 | 失败信号 |
|---|---|---|
| 1 | **Rich Description Field** | "I don't know when to use it" → description 缺触发词 |
| 2 | **Keyword Coverage** | 描述里没包含用户会说的具体错误信息、工具名、症状 |
| 3 | **Descriptive Naming** | `helper1` / `step3` / `pattern4` 这种泛名 |
| 4 | **Token Efficiency** | SKILL.md 主体 > 500 行,核心找不回 |

→ 完整 CSO 规则 + bad/good 对照 + 字数限制: [`references/cso-rules.md`](references/cso-rules.md)

---

## 🧪 TDD 流程 · Skill 测试模板

> **Testing All Skill Types** — 不同类型 skill 的测试重点不同。

### 4 类 skill 测试侧重点

| Skill 类型 | 测试核心 | 失败模式 |
|---|---|---|
| **Discipline-Enforcing** | 是否绕过/找理由 | "spirit vs letter" / "这次特殊情况" |
| **Technique** | 是否正确执行步骤 | 跳过步骤 / 自创替代 |
| **Pattern** | 是否识别正确场景 | 强行套用到不适配场景 |
| **Reference** | 是否找到正确信息 | 索引不完整 / 找不到 |

→ 完整 TDD 流程 + Bulletproofing Against Rationalization + Anti-Patterns: [`references/tdd-process.md`](references/tdd-process.md)

---

## 🚨 Anti-Patterns · 红线

| ❌ 反模式 | 为什么坏 |
|---|---|
| Narrative Example | 太具体,不可复用("2025-10-03 那个 case") |
| Multi-Language Dilution | 多语言示例 → 质量平庸 + 维护负担 |
| Code in Flowcharts | 流程图里写代码 → 不可复制 |
| Generic Labels | helper1/step3/pattern4 → 标签无语义 |
| Batching Without Testing | 批量写多个 skill 不单独测 → 违反 TDD |
| Skip Because "效率高" | "批量更高效" → 单测丢失的红旗会延后到生产 |

→ 完整反模式库 + 错误示例: [`references/anti-patterns.md`](references/anti-patterns.md)

---

## 📚 资源引用

| references | 内容 |
|---|---|
| [`skill-types-and-templates.md`](references/skill-types-and-templates.md) | 3 大类型详解 + SKILL.md 结构模板 |
| [`directory-structure.md`](references/directory-structure.md) | 目录模板 + 3 种典型场景 |
| [`cso-rules.md`](references/cso-rules.md) | CSO 4 大要素 + 触发词优化 + 字数限制 |
| [`tdd-process.md`](references/tdd-process.md) | TDD 4 阶段 + Bulletproofing + Red Flags |
| [`anti-patterns.md`](references/anti-patterns.md) | 反模式库 + Good/Bad 对照 |
| [`code-examples.md`](references/code-examples.md) | Flowchart + 代码块使用规范 |
| [`cross-referencing.md`](references/cross-referencing.md) | skill 间引用 vs 复制 |
| [`anthropic-best-practices.md`](references/anthropic-best-practices.md) | Anthropic 官方最佳实践补充 |
| [`testing-skills-with-subagents.md`](references/testing-skills-with-subagents.md) | 用 subagent 测 skill 的实操 |
| [`persuasion-principles.md`](references/persuasion-principles.md) | 描述措辞心理学参考 |
| [`graphviz-conventions.dot`](references/graphviz-conventions.dot) | Flowchart 规范 dot 文件 |

---

## 🛠 主体自检 Checklist(每个新 skill 完成前)

- [ ] 写了 3+ combined pressure scenarios?
- [ ] 跑了 RED(baseline agent behavior)?
- [ ] 写了 GREEN(最小 SKILL.md)?
- [ ] 跑了 REFACTOR(关 loophole)?
- [ ] Description 包含"Use when"开头 + 具体触发词?
- [ ] Description < 1024 字?
- [ ] Token Efficiency:SKILL.md < 500 行?
- [ ] references/ 按需加载(非全展开在主体)?
- [ ] Anti-Patterns 检查全过?
- [ ] 部署前跑了 [test-driven-development] 流程?

**主公记住**:**主体短 + references 厚 = 好 skill**。把所有"如何做"的细节放到 references/,主体只留骨架(触发 / 铁律 / 索引)。