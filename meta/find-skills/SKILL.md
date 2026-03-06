---
name: find-skills
description: 根据任务描述搜索最匹配的 Skills，或在无匹配时自动生成新的 Skill
version: 1.0.0
tags: [skill-discovery, search, skill-generation]
---

# find-skills

> 帮助用户找到最合适的 Skill，或在不存在时自动创建一个新的。

## 🎯 目标

1. **搜索模式**：根据用户描述的任务，从 index.json 中查找最匹配的 Skills
2. **生成模式**：当没有合适的 Skill 时，基于用户需求自动生成一个新的 SKILL.md

## 🔍 搜索模式

当用户描述一个任务（如"我需要处理视频"），find-skills 会：

1. 读取 `index.json` 获取所有 skills 索引
2. 解析用户输入，提取关键词
3. 计算与每个 skill 的相关性得分
4. 返回 top-N 匹配的 skills

### 关键词匹配算法

```python
score = 0
# name 完全匹配 = 10 分
# name 包含 = 5 分
# description 包含 = 3 分
# tags 匹配 = 2 分/个
# 返回得分 > 0 的结果，按得分排序
```

### 使用方式

```
# 直接调用
/find-skills

# 或自然语言触发
"帮我找一个处理视频的 skill"
"我需要一个做 X 的 skill"
```

输入任务描述，脚本会返回匹配的 skills 列表。

## ✨ 生成模式

当搜索结果不理想时，选择"生成新 Skill"：

1. 分析用户任务描述，提取核心需求
2. 基于 `_template_skill` 模板生成新的 SKILL.md
3. 创建基础目录结构 (scripts/, examples/)
4. 提供后续完善指引

### 生成的内容

```
<skill-name>/
├── SKILL.md              # Skill 定义（基于模板）
├── scripts/
│   └── main.py           # 入口脚本占位
└── examples/
    └── basic-usage.md    # 使用示例占位
```

## 📁 依赖

- `index.json` - 现有的 skills 索引
- `_template_skill/SKILL.md` - 生成新 skill 的模板

## 🔧 脚本

- [search.py](./scripts/search.py) - 搜索逻辑
- [generate.py](./scripts/generate.py) - 自动生成逻辑
- [usage.md](./examples/usage.md) - 使用示例