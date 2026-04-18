# UltraSkils: The Ultimate AI Skills Library 🚀

## Install a skill in one command

```bash
npx ultraskills install code-review
```

Find and install the best-scored AI skills for Claude Code. 538 skills, arena-ranked.

```
npx ultraskills search "code review"      # find skills
npx ultraskills list --category eng       # browse by category
npx ultraskills install bdi-mental-states # install by id
npx ultraskills update                    # update installed skills
npx ultraskills uninstall bdi-mental-states # remove installed skill
npx ultraskills info bdi-mental-states    # show skill detail
```

---

> **定义 AI 协作的新标准**。
> 本项目不仅仅是一个 Prompt 集合，而是一个**模块化、可复用、可验证**的 AI Skills 工业级标准库。

---

## 🌟 核心设计哲学 (S.C.A.L.E. Model)

我们遵循 **S.C.A.L.E.** 模型来构建每一个 Skill：

- **S**tandardized (标准化): 统一的目录结构与元数据。
- **C**omposable (可组合): 原子化设计，便于跨项目引用。
- **A**utomated/Auditable (可验证): 内置质量检查与评分标准。
- **L**iving (动态演进): 持续迭代的文档与知识库。
- **E**xamples (示例驱动): 强大的 Few-Shot 示例库。

---

## 📂 库结构标准

```text
ultraskils/
├── README.md                   # 库入口与索引
├── CONTRIBUTING.md             # 贡献指南与开发规范
├── index.json                  # 机器可读的技能索引
│
├── engineering/                # [Domain] 工程类 Skills
│   ├── prompt-optimizer/       # [Skill] Prompt 优化器
│   ├── SKILL.md                # 核心技能定义
│   ├── examples/               # 示例库
│   ├── templates/              # 可复用模板
│   └── resources/              # 知识资源
│
└── [skill-name]/               # [Skill] 标准结构
    ├── SKILL.md                # 必须包含 YAML Frontmatter
    ├── examples/               # 必须包含至少 3 个案例
    ├── scripts/                # (可选) 辅助脚本
    └── tests/                  # (可选) 验证清单或测试
```

---

## 🛠 如何在项目中使用

### 方式 1: 全局引用 (推荐)

将本仓库 clone 到您的本地工作区，并在 AI IDE (如 Trae/Cursor) 中添加为 Context 来源。

### 方式 2: 模块化复制

直接复制特定 Skill 文件夹到您的项目 `.agent/skills/` 目录下。

---

## 📚 Skills 索引

| Skill 名称 | 类别 | 描述 | 版本 |
|:----------|:-----|:-----|:----:|
| [**Prompt Optimizer**](./engineering/prompt-optimizer/SKILL.md) | Engineering | 工业级 Prompt 优化框架 | 1.0.0 |
| [**Git Commit Master**](./engineering/git-commit-master/SKILL.md) | Engineering | 生成语义化、规范化的 Git 提交信息 | 1.0.0 |
| [**GitHub Skill Scout**](./engineering/github-skill-scout/SKILL.md) | Engineering | 智能发现与封装 GitHub 工具 | 1.0.0 |
| [**Media Downloader**](./productivity/media-downloader/SKILL.md) | Productivity | 全能视频/音频下载工具 | 1.0.0 |

---

## 🤝 维护与贡献

本项目由 **UltraSkils Team** 维护。欢迎提交 PR 贡献新的 Skill！
请务必阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解 **"S-Tier Skill"** 的验收标准。
