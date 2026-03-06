# 贡献指南 (Contributing Guide)

感谢你有兴趣为 **UltraSkils** 贡献力量！本指南旨在帮助你构建符合**S级标准**的 AI Skills。

---

## 🏗️ Skill 构建标准 (The S-Tier Standard)

所有提交的 Skill 必须符合以下规范。这是我们将此仓库打造为"全网最佳实践"的基石。

### 1. 目录结构规范

每个 Skill 必须是一个独立的文件夹，结构如下：

```text
my-new-skill/                  # 命名使用各类短横线 (kebab-case)
├── SKILL.md                   # [必需] 核心定义文件
├── examples/                  # [必需] 示例库
│   ├── basic-usage.md         # 基础用法示例
│   └── advanced-cases.md      # 复杂场景示例
├── templates/                 # [可选] 可复用的模板/代码片段
└── resources/                 # [可选] 辅助文档、速查表、图片
```

### 2. SKILL.md 规范

这是 AI 读取的入口文件。必须包含 YAML Frontmatter。

```markdown
---
name: [Skill Name, Human Readable]
description: [One-line description of what this skill does]
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

## 🎯 目标 (Goal)
清晰描述本 Skill 解决什么问题。

## 🧠 核心理念 (Core Concepts)
解释背后的方法论（不仅是 How，还有 Why）。

## 🚀 使用流程 (Workflow)
分步骤说明如何执行。

## ✅ 检查清单 (Checklist)
用于验证结果质量的标准。
```

### 3. 黄金三法则 (The Golden Rules)

#### 法则一：示例即正义 (Examples are King)

不要只解释"怎么做"，要展示"做好的样子"。

- **必须**：至少提供 1 个完整的前后对比 (Before/After) 或 Input/Output 示例。
- **推荐**：在 `examples/` 目录下提供分类示例。

#### 法则二：模块化思维 (Modular Thinking)

Skill 应该是**原子化**的。

- ❌ 错误：`Software-Development-Master` (太大了)
- ✅ 正确：`git-commit-guide`, `react-component-generator`, `sql-optimizer`

#### 法则三：元认知设计 (Meta-Cognitive Design)

所有的 Skill 都应该指导用户或 AI 进行**思考**，而不仅仅是填空。

- 引入思维链 (Chain of Thought)
- 包含自我验证步骤

---

## 🔄 提交工作流 (Submission Workflow)

1. **Fork** 本仓库
2. **Copy** `_template_skill/` (即将创建) 到新目录
3. **Fill** 填充内容，遵循上述标准
4. **Test** 自己试用，确保 AI 能理解并执行
5. **PR** 提交 Pull Request，在描述中说明 Skill 的价值

---

## ✅ PR 验收清单 (Code Review Rubric)

在提交 PR 前，请自我检查：

- [ ] 目录结构是否符合规范？
- [ ] `SKILL.md` 是否有 YAML 头信息？
- [ ] 是否包含至少一个高质量示例？
- [ ] 是否在 `README.md` 的索引表中添加了你的 Skill？
- [ ] 文档是否清晰、无错别字？

让每一个 Skill 都成为精品！🚀
