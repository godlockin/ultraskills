---
name: skill-evolution-manager
description: Skills 进化管理器。在对话结束时根据用户反馈持续优化 Skills。触发词：/evolve, "复盘一下", "把这个经验保存到 Skill"
version: 1.0.0
tags: [devops, automation, evolution, feedback, learning]
---

# Skill Evolution Manager

> AI 技能系统的"进化中枢"，让 Skills 能够自我进化和持续优化。

## 🎯 目标 (Goal)

- **复盘诊断 (Session Review)**: 在对话结束时分析被调用 Skills 的表现
- **经验提取 (Experience Extraction)**: 将用户反馈转化为结构化 JSON 数据
- **智能缝合 (Smart Stitching)**: 自动将经验写入 `SKILL.md`，确保持久化

## 🧠 核心理念 (Core Concepts)

### 双文件系统

```
skill-folder/
├── SKILL.md          # 核心功能文档 (可能被版本更新覆盖)
└── evolution.json    # 用户经验存档 (永远不会丢失)
```

- **SKILL.md**: 来自 GitHub 的核心功能，会被 `skill-manager` 更新覆盖
- **evolution.json**: 本地积累的使用经验，类似"游戏存档"，永不丢失

### evolution.json 数据结构

```json
{
  "last_updated": "2024-01-15T10:30:00",
  "preferences": [
    "用户希望下载默认静音",
    "优先 1080p 画质"
  ],
  "fixes": [
    "Windows 下 ffmpeg 路径需要转义",
    "代理需要使用 socks5 而非 http"
  ],
  "custom_prompts": "在执行前总是先打印预估耗时和文件大小"
}
```

## 🚀 使用流程 (Workflow)

### 触发方式

```text
/evolve
```

或自然语言：

- "复盘一下刚才的对话"
- "我觉得刚才那个工具不太好用，记录一下"
- "把这个经验保存到 Skill 里"

---

### Workflow 1: 经验复盘 (Review & Extract)

#### Step 1: 扫描上下文

Agent 分析对话内容，识别：

- 用户不满意的点（报错、风格不对、参数错误）
- 用户满意的点（特定 Prompt 效果好）

#### Step 2: 定位 Skill

确定是哪个 Skill 需要进化（例如 `yt-dlp` 或 `ffmpeg-tool`）

#### Step 3: 生成 JSON

Agent 在内存中构建经验数据：

```json
{
  "preferences": ["用户希望下载默认静音"],
  "fixes": ["Windows 下 ffmpeg 路径需转义"],
  "custom_prompts": "在执行前总是先打印预估耗时"
}
```

---

### Workflow 2: 经验持久化 (Persist)

```bash
python scripts/merge_evolution.py <skill_path> '<json_string>'
```

示例：

```bash
python scripts/merge_evolution.py ~/.claude/skills/yt-dlp/ '{"preferences": ["默认静音"]}'
```

此脚本会：

- 读取现有 `evolution.json`（如果存在）
- 增量合并新数据，自动去重
- 保存更新后的 JSON

---

### Workflow 3: 文档缝合 (Stitch)

```bash
python scripts/smart_stitch.py <skill_path>
```

此脚本会：

- 读取 `evolution.json`
- 在 `SKILL.md` 末尾生成或更新 `## User-Learned Best Practices & Constraints` 章节
- 使用正则替换确保不重复

---

### Workflow 4: 跨版本对齐 (Align)

当 `skill-manager` 更新了 Skill 后，运行：

```bash
python scripts/align_all.py ~/.claude/skills/
```

此脚本会遍历所有 skills，将存在的 `evolution.json` 经验重新缝合回对应的 `SKILL.md`。

## 💡 最佳实践 (Best Practices)

- **Do**: 所有经验修正通过 `evolution.json` 通道进行
- **Do**: 更新 Skill 后立即运行 `align_all.py`
- **Don't**: 不要直接修改 SKILL.md 的正文（除非是拼写错误）
- **Don't**: 不要手动编辑 `evolution.json`，让 Agent 通过脚本操作

## 🗂 Lessons DB（跨instance经验共享）

经验不写回SKILL.md（浪费上下文），而是存入全局lessons库：

```
~/.claude/lessons/
  index.json              ← 可搜索索引 (id / keywords / updated)
  by-skill/{id}.md        ← 每个skill的提炼经验 (markdown)
```

**查询方式**（新instance启动时遇到问题先查）：

```bash
python3 ~/.claude/lessons-lookup.py <keyword>           # 关键词搜索
python3 ~/.claude/lessons-lookup.py --skill <skill-id>  # 查具体skill
python3 ~/.claude/lessons-lookup.py --list              # 列出所有
```

**自动流程**：
```
turn结束 → auto-evolve.sh flush → evolution.json (raw)
  → 阈值触发 or 每日09:00+21:00 cron
  → consolidate-evolutions.sh
  → existing lessons + new evolution → claude -p merge
  → ~/.claude/lessons/by-skill/{id}.md (updated)
  → evolution.json cleared
```

## 📚 资源引用

- [示例：进化 Skill](./examples/evolve-skill.md)
- [merge_evolution.py](./scripts/merge_evolution.py) - 增量合并工具
- [lessons-lookup.py](./scripts/lessons-lookup.py) - 经验检索工具
- [consolidate-evolutions.sh](./hooks/consolidate-evolutions.sh) - LLM提炼+写入lessons DB
- [auto-evolve.sh](./hooks/auto-evolve.sh) - Stop hook，每turn flush
