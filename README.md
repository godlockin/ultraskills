# UltraSkills: 556 AI Skills for Claude Code 🚀

> **定义 AI 协作的新标准** — 模块化、可复用、竞技场排名的 AI Skills 工业级标准库

---

## ⚡ Quick Start (3 commands)

```bash
git clone https://github.com/godlockin/ultraskills.git
cd ultraskills
./setup.sh          # installs ultraskills-hub into ~/.claude/skills/
```

Done. Restart Claude Code — Claude can now search all 556 skills on demand.

---

## 🔍 How It Works: Hub Search

安装后，Claude Code 拥有一个 **ultraskills-hub** skill。每次需要技能时，Claude 先搜索库：

```
You: "help me optimize this prompt"
Claude: [searches hub] → finds prompt-optimizer → invokes it
```

Hub 内部使用 `devops/ultraskills-hub/scripts/search.py` 对 `index.json` 做关键词搜索，返回匹配的 SKILL.md 路径。按需加载，context 零负担。

### 安装选项

```bash
./setup.sh           # 推荐：仅安装 hub（1 个 skill 在 system prompt）
./setup.sh --top     # hub + 33 个精选高分 skills
./setup.sh --all     # 全部 556 个（不推荐，context 很大）
./setup.sh --remove  # 卸载
```

---

## 🏆 Arena 竞技场排名

每个 skill 按 **质量 / 速度 / 可维护性** 评分。556 个 skills 中产生 **37 个 Arena Winners**（跨 39 个类别）。

在 `SKILLS_INDEX.md` 中，Arena 冠军用 🏆 标记。`index.json` 包含每个 skill 的 arena score。

---

## 📂 仓库结构

```text
ultraskills/
├── setup.sh                    # 安装脚本
├── index.json                  # 机器可读索引（556 skills，含 arena 分数）
├── SKILLS_INDEX.md             # 人类可读索引（556 × 39 类别，冠军标记）
├── CONTRIBUTING.md             # S-Tier skill 标准
├── _template_skill/            # 新 skill 模板
│
├── devops/
│   └── ultraskills-hub/        # ⭐ Hub 入口 skill
│       └── scripts/search.py  # 关键词搜索引擎
│
├── engineering/                # 工程类 skills（git, code review, prompt 等）
├── productivity/               # 效率工具（media downloader, task analysis 等）
├── devops/                     # 技能管理工具
├── creative/                   # 创意设计（视频, 图像, 艺术生成等）
├── community/                  # 社区贡献
└── external/                   # 外部来源 skills
```

每个 skill 目录结构：
```text
[skill-name]/
├── SKILL.md          # 必需：YAML frontmatter + 指令
├── examples/         # 推荐：使用示例
└── resources/        # 可选：辅助文档
```

---

## 🧠 S.C.A.L.E. 设计哲学

| 字母 | 含义 | 说明 |
|------|------|------|
| **S** | Standardized 标准化 | 统一目录结构与 YAML 元数据 |
| **C** | Composable 可组合 | 原子化设计，跨项目引用 |
| **A** | Automated/Auditable 可验证 | 内置质量检查与评分 |
| **L** | Living 动态演进 | Evolution 系统持续迭代 |
| **E** | Examples 示例驱动 | Few-Shot 示例库 |

---

## ➕ 引入新 Skills / Skills 项目

发现一个有用的 skill 或 GitHub 上的 skills 项目？三种引入方式：

### 方式一：引入单个 skill（手动）

```bash
# 1. 在合适的分类下创建目录
mkdir -p community/my-new-skill

# 2. 写 SKILL.md（参考 _template_skill/）
# 必须包含 YAML frontmatter: name, description, version, tags

# 3. 更新索引
python3 devops/skill-manager/scripts/scan_and_check.py  # 验证结构
# 然后手动在 index.json 添加条目，或让 Claude 做

# 4. 可选：注册到 ~/.claude/skills/
ln -sf $(pwd)/community/my-new-skill ~/.claude/skills/my-new-skill
```

### 方式二：引入 GitHub skills 项目（github-to-skills）

```bash
# 用 github-to-skills skill 自动转换整个 GitHub 仓库
# 触发: Skill("github-to-skills")

# 示例：引入 mattpocock/skills
# Claude 会：
# 1. 分析 GitHub repo 结构
# 2. 提取每个 skill 的内容
# 3. 创建标准 SKILL.md（注入 github_url/github_hash frontmatter）
# 4. 放入 external/ 或 community/ 目录
# 5. 更新 index.json
```

手动方式（git submodule）：
```bash
# 整个项目作为 submodule 引入 external/
git submodule add https://github.com/org/skills-repo external/skills-repo

# 或直接 clone 到 external/
git clone https://github.com/org/skills-repo external/skills-repo
```

### 方式三：用 skill-manager 追踪外部更新

引入外部 skill 后，在 SKILL.md frontmatter 加上来源信息：
```yaml
github_url: https://github.com/org/repo
github_hash: abc1234def   # import 时的 commit hash
```

之后可以用 `Skill("skill-manager")` 检查哪些 skills 有上游更新。

---

## 🖥️ 加载到本地 Claude Code

### 新机器完整安装

```bash
# 1. Clone
git clone https://github.com/godlockin/ultraskills.git ~/skills/ultraskills
cd ~/skills/ultraskills

# 2. 安装 hub（核心入口）
./setup.sh

# 3. 可选：安装 lessons 检索
ln -sf $(pwd)/devops/skill-evolution-manager/scripts/lessons-lookup.py \
  ~/.claude/lessons-lookup.py

# 4. 可选：在全局 CLAUDE.md 里加上 lessons 查询指引
# ~/.claude/CLAUDE.md 末尾加：
# python3 ~/.claude/lessons-lookup.py <keyword>  # 遇到问题先查经验库
```

### 细粒度控制：选择性加载

```bash
# 只加载特定 skill（绕过 hub，直接注册）
ln -sf $(pwd)/community/karpathy-guidelines ~/.claude/skills/karpathy-guidelines

# 加载整个类别
for d in engineering/*/; do
  id=$(basename "$d")
  ln -sf "$(pwd)/$d" ~/.claude/skills/"$id"
done

# 卸载所有 ultraskills symlinks
./setup.sh --remove
```

### 验证安装

```bash
ls ~/.claude/skills/ultraskills-hub   # 应该是 symlink
python3 devops/ultraskills-hub/scripts/search.py git commit  # 应该返回结果
```

---

## 🔄 Evolution System（经验演进）

Skills 通过 Stop hook 自动积累使用经验：

```
session结束 → pending-evolutions.jsonl → evolution.json → ~/.claude/lessons/
```

可选：安装 lessons 检索工具
```bash
ln -sf $(pwd)/devops/skill-evolution-manager/scripts/lessons-lookup.py ~/.claude/lessons-lookup.py
python3 ~/.claude/lessons-lookup.py "prompt optimization"  # 搜索历史经验
```

---

## 📋 Skills 总览

556 个 skills，39 个类别。完整列表见 [SKILLS_INDEX.md](./SKILLS_INDEX.md)。

部分精选：

| Skill | 类别 | 描述 |
|:------|:-----|:-----|
| [ultraskills-hub](./devops/ultraskills-hub/SKILL.md) | DevOps | 🏆 技能搜索入口 |
| [prompt-optimizer](./engineering/prompt-optimizer/SKILL.md) | Engineering | 工业级 Prompt 优化框架 |
| [git-commit-master](./engineering/git-commit-master/SKILL.md) | Engineering | 语义化 Git 提交信息 |
| [media-downloader](./productivity/media-downloader/SKILL.md) | Productivity | 全能视频/音频下载 |
| [skill-arena](./devops/skill-arena/SKILL.md) | DevOps | Skill 质量竞技场评分 |

完整 37 个 Arena Winners 见 SKILLS_INDEX.md 🏆 标记。
