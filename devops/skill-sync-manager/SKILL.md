---
name: skill-sync-manager
description: 全量更新 Skills。用于批量更新所有 submodules，检查更新，并同步到社区 skills。触发词：/skill-sync, 同步 skills, 更新所有 skills
version: 1.0.0
tags: [devops, automation, sync, submodule, update]
---

# Skill Sync Manager

> 批量管理 external sources 的 submodules，定期同步最新代码到本地 skills 库。

## 🎯 目标 (Goal)

- **同步 (Sync)**: 批量更新所有 external submodules 到最新版本
- **检查 (Check)**: 检查哪些 submodule 有更新
- **报告 (Report)**: 生成更新报告
- **自动化 (Automate)**: 通过 GitHub Action 定时执行

## 🧠 核心理念 (Core Concepts)

### Submodule 结构

```
external/                          # Git Submodules 源
├── claude-code/                  # Anthropic 官方 Claude Code skills
├── anthropic-skills/              # Anthropic skills
├── anthropic-quickstarts/         # Anthropic Quickstarts
├── context-engineering-skills/    # Context Engineering skills
├── khazix-skills/                 # Khazix 自定义 skills
├── superpowers/                   # Superpowers 技能库
├── videocut-skills/              # Video 剪辑技能
└── marketingskills/              # Marketing skills (CRO, copywriting, SEO, etc.)
```

### 目录映射

| Submodule | 本地 Skills 目录 |
|-----------|-----------------|
| claude-code | community/ (部分) |
| anthropic-skills | community/ (部分) |
| superpowers | community/superpowers/* |
| videocut-skills | community/剪口播, 剪辑, 字幕 |
| marketingskills | external/marketingskills/skills/* (32 个 marketing skills) |

## 🚀 使用流程 (Workflow)

### 触发方式

```text
/skill-sync          # 同步所有 submodules
/skill-sync check    # 只检查更新，不实际更新
/skill-sync report   # 生成更新报告
```

---

### Workflow 1: 同步所有 Submodules

#### Step 1: 进入项目目录

```bash
cd /path/to/ultraskils
```

#### Step 2: 执行同步脚本

```bash
python scripts/sync_submodules.py
```

或使用 git 命令直接更新：

```bash
git submodule update --remote --merge
```

#### Step 3: 检查变更

```bash
git status
git diff --submodule
```

#### Step 4: 提交更新

```bash
git add external/
git commit -m "chore: 更新 skills submodules"
git push
```

---

### Workflow 2: 检查更新

```bash
git submodule status
```

输出示例：
```
+4b2549e8093a6dee1c394bdd8fcf83cb914a271a external/anthropic-quickstarts (v1.2.0)
+7029232b9212482c0476da354b83364bd28fab2f external/anthropic-skills (v2.0.0)
```

`+` 表示有可用更新。

---

### Workflow 3: 手动更新单个 Submodule

```bash
git submodule update --remote external/claude-code
```

---

## 📜 脚本

- `scripts/sync_submodules.py` - 批量同步 submodules
- `scripts/check_updates.py` - 检查更新并生成报告

---

## 🔄 GitHub Action 自动同步

创建 `.github/workflows/sync-skills.yml`：

```yaml
name: Sync Skills

on:
  schedule:
    - cron: '0 0 * * *'  # 每天午夜执行
  workflow_dispatch:     # 支持手动触发

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true

      - name: Update submodules
        run: |
          git submodule update --remote --merge

      - name: Check for changes
        id: changes
        run: |
          if git diff --submodule --quiet; then
            echo "changes=false" >> $GITHUB_OUTPUT
          else
            echo "changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit and push
        if: steps.changes.outputs.changes == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add external/
          git commit -m "chore: 自动更新 skills submodules"
          git push
```

---

## 💡 最佳实践 (Best Practices)

- **Do**: 定期运行同步，保持 skills 最新
- **Do**: 同步后检查变更，确保没有破坏性更新
- **Don't**: 不要在未检查的情况下直接推送
- **Don't**: 避免频繁提交，可以使用累积更新

## 📚 资源引用

- [Git Submodules 文档](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [示例：同步脚本](./scripts/sync_submodules.py)
- [GitHub Action 配置](./.github/workflows/sync-skills.yml)