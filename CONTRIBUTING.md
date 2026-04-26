# 贡献指南 (Contributing Guide)

本指南帮助你构建符合 **S级标准** 的 AI Skills，添加到 UltraSkills 库中。

---

## 🏗️ Skill 构建标准 (The S-Tier Standard)

### 1. 目录结构规范

每个 Skill 必须是一个独立的文件夹：

```text
my-new-skill/                  # 命名使用短横线 (kebab-case)
├── SKILL.md                   # [必需] 核心定义文件
├── examples/                  # [推荐] 示例库
│   ├── basic-usage.md         # 基础用法示例
│   └── advanced-cases.md      # 复杂场景示例
├── templates/                 # [可选] 可复用的模板/代码片段
└── resources/                 # [可选] 辅助文档、速查表、图片
```

### 2. SKILL.md 规范

必须包含 YAML Frontmatter：

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

**外部来源 skill** 额外需要：
```yaml
---
name: ...
github_url: https://github.com/org/repo
github_hash: abc1234   # commit hash at time of import
---
```

### 3. 黄金三法则 (The Golden Rules)

#### 法则一：示例即正义 (Examples are King)

- **必须**：至少 1 个完整的 Before/After 或 Input/Output 示例
- **推荐**：在 `examples/` 目录下提供分类示例

#### 法则二：模块化思维 (Modular Thinking)

Skill 应该是**原子化**的：

- ❌ `Software-Development-Master`（太大）
- ✅ `git-commit-guide`, `react-component-generator`, `sql-optimizer`

#### 法则三：元认知设计 (Meta-Cognitive Design)

引导 AI **思考**，不仅仅是填空：

- 引入思维链 (Chain of Thought)
- 包含自我验证步骤

---

## 🔄 添加工作流

### 自建 Skill

1. **Copy** `_template_skill/` 到目标分类目录（`community/` 或 `engineering/` 等）
2. **Fill** 填充 SKILL.md 内容，遵循上述标准
3. **Test** 本地试用：`Skill("my-new-skill")` 或直接 Read SKILL.md
4. **Index** 更新 `index.json`，或让 Claude 自动更新

### 引入外部 GitHub Skills 项目

```bash
# 用 github-to-skills skill 自动转换
Skill("github-to-skills")
# → 输入 GitHub repo URL
# → 自动提取 skills、注入 frontmatter、更新 index.json
```

手动引入（整个 repo）：
```bash
git clone https://github.com/org/skills-repo external/skills-repo
# 然后在 SKILL.md 里注入 github_url/github_hash
# 更新 index.json
```

### 追踪外部 Skill 更新

外部来源 skill 的 frontmatter 需包含：
```yaml
github_url: https://github.com/org/repo
github_hash: abc1234def   # import 时的 commit hash，用于检测更新
```

检查上游更新：`Skill("skill-manager")` → check

---

## ✅ 自查清单

提交前检查：

- [ ] 目录结构符合规范（kebab-case 命名）
- [ ] `SKILL.md` 包含 YAML frontmatter（name, description, version, tags）
- [ ] 外部来源 skill 包含 `github_url` 和 `github_hash`
- [ ] 包含至少一个高质量示例
- [ ] `index.json` 已更新
- [ ] 文档清晰、无错别字

让每一个 Skill 都成为精品！🚀
