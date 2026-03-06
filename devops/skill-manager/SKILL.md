---
name: skill-manager
description: Skills 生命周期管理器。用于批量扫描 Skills 目录、检查 GitHub 更新、执行升级引导。触发词：/skill-manager check, list, delete
version: 1.0.0
tags: [devops, automation, lifecycle, management]
---

# Skill Lifecycle Manager

> 自动化管理 GitHub 封装的 Skills，检测更新并辅助升级。

## 🎯 目标 (Goal)

- **审计 (Audit)**: 扫描本地 skills 目录，识别带有 `github_url` 元数据的 skills
- **检查 (Check)**: 对比本地 `github_hash` 与远程最新 commit
- **报告 (Report)**: 生成状态报告，标识 "Stale" 或 "Current"
- **更新 (Update)**: 引导 Agent 执行升级流程
- **清理 (Clean)**: 列出并删除不需要的 skills

## 🧠 核心理念 (Core Concepts)

### 依赖元数据标准

本管理器依赖 `github-to-skills` 创建的扩展元数据：

- `github_url`: 真理来源 (Source of Truth)
- `github_hash`: 状态来源 (State of Truth)

只有包含这两个字段的 skills 才会被识别为"可管理"的 GitHub 技能。

## 🚀 使用流程 (Workflow)

### 触发方式

```text
/skill-manager check    # 扫描并检查更新
/skill-manager list     # 列出所有 skills
/skill-manager delete <name>   # 删除指定 skill
```

或自然语言：

- "扫描一下我的 skills 有没有更新"
- "列出所有安装的 skills"
- "删除 xxx skill"

---

### Workflow 1: 检查更新

#### Step 1: 运行扫描器

```bash
python scripts/scan_and_check.py ~/.claude/skills/
```

#### Step 2: 查看报告

脚本输出 JSON 格式的状态报告：

```json
[
  {
    "name": "yt-dlp",
    "status": "outdated",
    "message": "New commits available",
    "local_hash": "abc123",
    "remote_hash": "def456"
  },
  {
    "name": "ffmpeg-tool",
    "status": "current",
    "message": "Up to date"
  }
]
```

Agent 向用户呈现：
> "发现 3 个过时的 skills: `yt-dlp` (落后 50 commits), `ffmpeg-tool` (落后 2 commits)..."

---

### Workflow 2: 更新 Skill

**触发**: "更新 [Skill Name]" (在检查之后)

#### Step 1: 备份

```bash
python scripts/update_helper.py ~/.claude/skills/yt-dlp/
```

#### Step 2: 获取新上下文

Agent 从远程仓库获取最新 README。

#### Step 3: 差异分析

- 对比新 README 与旧 `SKILL.md`
- 识别新功能、废弃参数、使用变化

#### Step 4: 重构

- 重写 `SKILL.md` 反映新能力
- 更新 frontmatter 中的 `github_hash`
- 可选：更新 `wrapper.py` 如果 CLI 参数变化

#### Step 5: 对齐经验

运行 `skill-evolution-manager` 的 `smart_stitch.py` 重新缝合用户经验。

---

### Workflow 3: 列出 Skills

```bash
python scripts/list_skills.py ~/.claude/skills/
```

输出表格：

```
Skill Name           | Type         | Description                              | Ver     
---------------------------------------------------------------------------------------
yt-dlp               | GitHub       | Video downloader wrapped from GitHub     | 0.1.0   
my-custom-skill      | Standard     | A locally created skill                  | 1.0.0   
```

---

### Workflow 4: 删除 Skill

```bash
python scripts/delete_skill.py yt-dlp ~/.claude/skills/
```

## 💡 最佳实践 (Best Practices)

- **Do**: 更新前先备份
- **Do**: 更新后运行 `skill-evolution-manager` 对齐经验
- **Don't**: 不要手动修改 `github_hash`，让系统自动管理

## 📚 资源引用

- [示例：检查更新](./examples/check-updates.md)
- [scan_and_check.py](./scripts/scan_and_check.py) - 扫描与检查
- [list_skills.py](./scripts/list_skills.py) - 列出 skills
- [delete_skill.py](./scripts/delete_skill.py) - 删除 skill
- [update_helper.py](./scripts/update_helper.py) - 更新辅助
