---
name: github-to-skills
description: 将 GitHub 仓库自动转换为标准化 AI Skills 的工厂工具。当用户提供 GitHub URL 并希望将其"打包"、"封装"或"创建 Skill"时触发。
version: 1.0.0
tags: [devops, automation, github, skill-creation]
---

# GitHub to Skills Factory

> 自动化将 GitHub 仓库转换为可管理的 AI Skills。

## 🎯 目标 (Goal)

- 自动获取仓库元数据（描述、README、最新 Commit Hash）
- 创建标准化的 Skill 目录结构
- 生成带扩展元数据的 `SKILL.md`，支持后续生命周期管理

## 🧠 核心理念 (Core Concepts)

### 扩展元数据 Schema

每个由本工具创建的 Skill **必须**包含以下 YAML frontmatter，这是 `skill-manager` 后续管理的基础：

```yaml
---
name: <kebab-case-repo-name>
description: <简洁描述，用于 AI 触发识别>
# 扩展元数据 (必需)
github_url: <原始仓库 URL>
github_hash: <创建时的最新 commit hash>
version: <tag 或 0.1.0>
created_at: <ISO-8601 日期>
entry_point: scripts/wrapper.py
dependencies: ["dep1", "dep2"]  # 主要依赖
---
```

### 为什么需要 Hash？

- **唯一标识**：`github_hash` 作为 Skill 的版本快照
- **自动更新检测**：`skill-manager` 通过对比本地与远程 hash 判断是否需要更新
- **经验保留**：更新时不会丢失 `evolution.json` 中积累的用户经验

## 🚀 使用流程 (Workflow)

### 触发方式

```text
/github-to-skills <github_url>
```

或自然语言：

- "帮我把这个仓库封装成 Skill: <https://github.com/>..."
- "Package this repo into a skill"

### Step 1: 获取信息 (Fetch)

运行 `scripts/fetch_github_info.py` 获取仓库数据：

```bash
python scripts/fetch_github_info.py https://github.com/yt-dlp/yt-dlp
```

输出 JSON:

```json
{
  "name": "yt-dlp",
  "url": "https://github.com/yt-dlp/yt-dlp",
  "latest_hash": "abc123...",
  "readme": "# yt-dlp..."
}
```

### Step 2: 分析规划 (Plan)

Agent 分析 README，理解：

- 工具的安装方式
- CLI 参数和使用模式
- 主要功能点

### Step 3: 生成 Skill (Generate)

运行 `scripts/create_github_skill.py` 创建目录结构：

```bash
python scripts/create_github_skill.py /tmp/repo_info.json ~/.claude/skills/
```

生成结构：

```
yt-dlp/
├── SKILL.md           # 带扩展元数据
├── scripts/
│   └── wrapper.py     # 调用逻辑
├── references/        # 参考文档
└── assets/            # 资源文件
```

### Step 4: 验证 (Verify)

检查 `github_hash` 是否正确捕获。

## 💡 最佳实践 (Best Practices)

- **Do**: 只包含必要的 wrapper 代码，引用原仓库获取详细信息
- **Do**: 明确声明依赖，使用 venv 或 uv 隔离环境
- **Don't**: 不要把整个仓库内容都塞进 Skill

## 📚 资源引用

- [示例：转换 yt-dlp](./examples/convert-ytdlp.md)
- [fetch_github_info.py](./scripts/fetch_github_info.py) - 仓库信息获取
- [create_github_skill.py](./scripts/create_github_skill.py) - Skill 脚手架生成
