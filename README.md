# UltraSkills: 581 AI Skills for Claude Code 🚀

> **定义 AI 协作的新标准** — 模块化、可复用、竞技场排名的 AI Skills 工业级标准库

---

## ⚡ Quick Start (3 commands)

```bash
git clone https://github.com/godlockin/ultraskills.git
cd ultraskills
./setup.sh          # auto-inits submodules + installs ultraskills-hub
```

Done. Restart Claude Code — Claude can now search all 581 skills on demand.

> **Submodules**: `setup.sh` automatically runs `git submodule update --init --recursive` on first run.
> Pass `--no-submodules` to skip (some external skills will be unavailable).

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
./setup.sh                # 推荐：hub-only（1 个 skill 在 system prompt）
./setup.sh --top          # hub + 33 个精选高分 skills
./setup.sh --all          # 全部 581 个（不推荐，context 很大）
./setup.sh --no-submodules  # 跳过 submodule 初始化（部分 external skills 不可用）
./setup.sh --remove       # 卸载
```

### Submodule 说明

本库包含多个 git submodule（第三方 skill 集合，位于 `external/` 和部分 `community/` 下）：

| 路径 | 来源 |
|------|------|
| `external/marketingskills` | coreyhaines31/marketingskills |
| `external/claude-skills` | alirezarezvani/claude-skills |
| `external/anthropic-skills` | anthropics/skills |
| `external/superpowers` | obra/superpowers |
| `community/gstack` | garrytan/gstack |
| `community/planning-with-files` | OthmanAdi/planning-with-files |
| … | （共 17 个，见 `.gitmodules`） |

**初始化方式**（`setup.sh` 自动执行，无需手动）：

```bash
# 全部初始化（推荐）
git submodule update --init --recursive

# 仅初始化特定 submodule
git submodule update --init external/marketingskills

# 检查 submodule 状态
git submodule status
```

> 未初始化的 submodule 目录存在但为空。`validate_skills.py` 会将此类缺失路径标记为
> **warning**（而非 error），不影响 CI 通过，但对应 skills 无法使用。



## 🏆 Arena 竞技场排名

每个 skill 按 **质量 / 速度 / 可维护性** 评分。在 `SKILLS_INDEX.md` 中，Arena 冠军用 🏆 标记。`index.json` 包含每个 skill 的 arena score。

### Arena Pipeline

```bash
# 一键执行全量扫描→评分→索引重建
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py
```

**数据流：**
```
SKILL.md (各目录)
    ↓ scripts/arena_scan.py
skill-arena/skills_inventory.json
    ↓ scripts/arena_cluster_score.py
skill-arena/{clusters, scores, winners}.json
    ↓ scripts/arena_build_index.py
index.json (主索引，供 hub/CLI 检索)
```

**脚本说明：**

| 脚本 | 作用 | 输出 |
|------|------|------|
| `scripts/arena_scan.py` | 扫描全库 SKILL.md，提取元数据 | `skill-arena/skills_inventory.json` |
| `scripts/arena_cluster_score.py` | 规则聚类 + 多维度评分 | `skill-arena/{clusters,scores,winners}.json` |
| `scripts/arena_build_index.py` | 合并 inventory + scores | `index.json` (覆盖) |
| `scripts/deploy_skills.py` | scan + 软链接部署到 ~/.claude/skills | symlinks |
| `scripts/sync_skills.py` | 从外部目录/GitHub 同步 skills | index.json 更新 |
| `scripts/pipeline_lock.py` | 共用文件锁，防止 pipeline 并发冲突 | `.pipeline.lock` |

> ⚠️ **Post-process 强制规则**：任何 skill 内容变更（新增、修改、删除、外部同步）后，**必须**执行 arena pipeline 全量重建。索引未更新 = hub 搜索不到 = 等于没改。

### 搜索功能

```bash
# 关键词搜索（支持中英文、fuzzy match）
python3 devops/ultraskills-hub/scripts/search.py 语音克隆
python3 devops/ultraskills-hub/scripts/search.py review

# 健康巡检（检查脚本引用、examples 非空、tags 标准化）
python3 devops/skill-manager/scripts/scan_and_check.py --health community/
```

---

## 📂 仓库结构

```text
ultraskills/
├── setup.sh                         # 安装脚本
├── index.json                       # 主索引（全量 skills + arena 分数）
├── SKILLS_INDEX.md                  # 人类可读索引
├── CONTRIBUTING.md                  # S-Tier skill 标准
├── _template_skill/                 # 新 skill 模板
│
├── bin/ultraskills.js               # Node.js CLI 入口
├── lib/                             # CLI 核心模块 (search/list/install/update)
│
├── scripts/                         # ⭐ Arena + 索引主流程 (Python)
│   ├── arena_scan.py                # Step 1: 扫描 SKILL.md → skills_inventory.json
│   ├── arena_cluster_score.py       # Step 2: 聚类+打分 → clusters/scores/winners.json
│   ├── arena_build_index.py         # Step 3: 合并 → index.json
│   ├── deploy_skills.py             # 部署 skills 到 ~/.claude/skills
│   ├── sync_skills.py               # 从外部目录/GitHub 同步 skills
│   └── pipeline_lock.py             # 共用文件锁 (防并发冲突)
│
├── skill-arena/                     # Arena 数据 (JSON，被 scripts/ 读写)
│   ├── skills_inventory.json        # 全量 skill 清单
│   ├── clusters.json / scores.json / winners.json
│
├── community/                       # 社区 skills (~130+)
├── engineering/                     # 工程 skills
├── productivity/                    # 生产力 skills
├── creative/                        # 创意/设计 skills
├── external/                        # 外部开源 skills (git submodule)
│
└── devops/                          # 运维管理工具
    ├── ultraskills-hub/             # ⭐ Hub 搜索 skill
    │   └── scripts/search.py
    ├── skill-arena/                 # Arena 完整测试框架
    │   ├── run.sh                   # 启动器
    │   └── scripts/                 # 12 个脚本 (run_benchmarks, score_results 等)
    ├── skill-manager/               # 技能生命周期管理
    │   └── scripts/scan_and_check.py, list_skills.py, delete_skill.py
    ├── skill-evolution-manager/     # Skill 迭代进化
    ├── skill-loader/                # MCP 动态加载器
    ├── skill-sync-manager/          # 子模块同步
    └── github-to-skills/            # GitHub repo → skill 转换
```

每个 skill 目录结构：
```text
[skill-name]/
├── SKILL.md          # 必需：YAML frontmatter + 指令
├── examples/         # 推荐：使用示例
├── scripts/          # 可选：自动化脚本
├── references/       # 可选：知识库
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

# 3. 验证结构 + 健康检查
python3 devops/skill-manager/scripts/scan_and_check.py community/my-new-skill/
python3 devops/skill-manager/scripts/scan_and_check.py --health community/my-new-skill/

# 4. [必须] 重建索引（任何 skill 变更后必跑）
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py

# 5. 验证搜索能找到
python3 devops/ultraskills-hub/scripts/search.py my-new-skill
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

### 方式三：用 skill-sync-manager 同步外部更新

```bash
# 检查外部 skills 是否有上游更新
python3 devops/skill-sync-manager/scripts/check_updates.py

# 同步更新
python3 devops/skill-sync-manager/scripts/sync_submodules.py
```

引入外部 skill 后，在 SKILL.md frontmatter 加上来源信息：
```yaml
github_url: https://github.com/org/repo
github_hash: abc1234def   # import 时的 commit hash
```

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
ls ~/.claude/skills/ultraskills-hub       # 应该是 symlink
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
