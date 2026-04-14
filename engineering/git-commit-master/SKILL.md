---
name: Git Commit Master
description: 基于Conventional Commits规范，生成语义化、规范化的Git提交信息
version: 1.0.0
tags: [git, engineering, workflow]
---

# Git Commit Master

基于 **Conventional Commits** 规范，将混乱的变更转化为清晰、标准、可自动发布版本的提交信息。

## 🎯 目标 (Goal)

- 消除 "fix bug" 或 "update" 等无意义提交
- 自动化生成符合 Changelog 标准的 commit message
- 确保团队提交风格一致性

## 🧠 核心理念 (Core Concepts)

遵循 `<type>(<scope>): <subject>` 格式：

- **feat**: 新功能
- **fix**: 修补 bug
- **docs**: 文档改变
- **style**: 代码格式改变
- **refactor**: 某个已有功能重构
- **perf**: 性能优化
- **test**: 增加测试
- **build**: 构建工具或外部依赖包变动
- **ci**: CI 配置脚本变化
- **chore**: 杂务

## 🚀 使用流程 (Workflow)

### Step 1: 提供变更 (Input)

提供 `git diff` 或简述做了什么改动。

### Step 2: 语义化映射 (Mapping)

AI 分析改动性质，映射到正确的 type 和 scope。

### Step 3: 格式化输出 (Generation)

生成标题（不超过 50 字符）和正文（解释 Why 和 How）。

## ✅ 检查清单 (Checklist)

- [ ] 是否使用了正确的 Type？
- [ ] 标题是否使用了祈使句（"Add feature" 而非 "Added feature"）？
- [ ] 是否有关联 Issue ID？
- [ ] 是否提及了 BREAKING CHANGE？

## 📚 资源引用

- [示例](./examples/basic-usage.md)
