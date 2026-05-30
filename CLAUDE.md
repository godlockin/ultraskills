# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Default Skills

**caveman mode is ALWAYS ON** — talk like caveman by default. Cut filler words. Keep technical accuracy. Use `/caveman lite|full|ultra` to adjust intensity or "normal mode" to disable.

## Project Overview

**UltraSkills** is a 581-skill library for Claude Code. Modular, arena-ranked AI prompt patterns following the S.C.A.L.E. model. Primarily a documentation/prompt library.

---

## Repository Structure

```
ultraskills/
├── setup.sh                         # Install: hub-only / --top / --all / --remove
├── index.json                       # Master index (all skills + arena scores)
├── SKILLS_INDEX.md                  # Human-readable index by category
├── CONTRIBUTING.md                  # S-Tier skill standards
├── CLAUDE.md                        # This file
├── TODOS.md                         # Project TODO list
├── package.json                     # Node.js CLI package config
│
├── bin/
│   └── ultraskills.js               # CLI entry point (search/list/install/update)
│
├── lib/                             # CLI core modules (Node.js)
│   ├── search.js                    # Keyword search engine
│   ├── list.js                      # List skills
│   ├── install.js / uninstall.js    # Install/remove skills to ~/.claude/skills
│   ├── update.js                    # Update installed skills
│   ├── cache.js                     # Cache management
│   └── info.js                      # Skill detail display
│
├── scripts/                         # ⭐ Arena + 索引主流程脚本 (Python)
│   ├── arena_scan.py                # Step 1: 扫描所有 SKILL.md → skills_inventory.json
│   ├── arena_cluster_score.py       # Step 2: 聚类 + 打分 → clusters/scores/winners.json
│   ├── arena_build_index.py         # Step 3: 合并 inventory+scores → index.json
│   ├── deploy_skills.py             # 部署: scan + deploy 到 ~/.claude/skills
│   ├── sync_skills.py               # 同步: 从外部目录/GitHub 导入 skills
│   └── pipeline_lock.py             # 共用文件锁 (防并发冲突)
│   ├── bootstrap.sh                 # 初始化项目环境
│   └── init_project_skills.sh       # 初始化项目级 skills
│
├── skill-arena/                     # Arena 数据目录 (JSON，被 scripts/ 读写)
│   ├── skills_inventory.json        # arena_scan.py 输出: 全量 skill 清单
│   ├── clusters.json                # arena_cluster_score.py 输出: 聚类结果
│   ├── scores.json                  # arena_cluster_score.py 输出: 评分
│   └── winners.json                 # arena_cluster_score.py 输出: 各 cluster 获胜者
│
├── _template_skill/                 # 新 skill 模板 (拷贝创建用)
│
├── community/                       # 社区 skills (~130+)
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── examples/
│       ├── scripts/                 # Optional
│       └── references/              # Optional
│
├── engineering/                     # 工程 skills
├── productivity/                    # 生产力 skills
├── creative/                        # 创意/设计 skills
├── external/                        # 外部开源 skills (git submodule)
│
├── devops/                          # 运维管理工具 skills
│   ├── ultraskills-hub/             # ⭐ Hub 搜索 skill (Claude Code 入口)
│   │   └── scripts/search.py
│   ├── skill-arena/                 # Arena 完整测试框架 (独立于 scripts/arena_*)
│   │   ├── run.sh                   # 启动器 (加载 .env → 调用 skill-arena.py)
│   │   ├── scripts/
│   │   │   ├── skill-arena.py       # Arena 主入口
│   │   │   ├── run_benchmarks.py    # 基准测试执行
│   │   │   ├── score_results.py     # 测试结果评分
│   │   │   ├── validate_skills.py   # 技能验证
│   │   │   ├── cluster_skills.py    # 技能聚类
│   │   │   ├── design_tests.py      # 测试用例设计
│   │   │   ├── expert_panels.py     # 专家评审面板
│   │   │   ├── expert_collaboration.py
│   │   │   ├── generate_report.py   # 生成评测报告
│   │   │   ├── llm_judge.py         # LLM 评分裁判
│   │   │   ├── llm_invoker.py       # LLM 调用封装
│   │   │   └── update_index.py      # 用 winners/rankings 更新 index.json
│   │   ├── test-suites/             # 40+ 测试套件 (每类一个 tests.yaml)
│   │   └── reports/                 # 评测报告输出
│   ├── skill-manager/               # 技能生命周期管理
│   │   └── scripts/
│   │       ├── scan_and_check.py    # 结构合规校验
│   │       ├── list_skills.py       # 列出所有 skills
│   │       ├── delete_skill.py      # 删除 skill
│   │       └── update_helper.py     # 更新辅助
│   ├── skill-evolution-manager/     # Skill 迭代进化
│   │   └── scripts/
│   │       ├── merge_evolution.py
│   │       ├── smart_stitch.py
│   │       ├── align_all.py
│   │       └── lessons-lookup.py
│   ├── skill-loader/                # MCP 动态加载器
│   │   ├── mcp_server.py
│   │   ├── skill_router.py
│   │   └── cli.py
│   ├── skill-sync-manager/          # 子模块同步
│   │   └── scripts/
│   │       ├── check_updates.py
│   │       └── sync_submodules.py
│   ├── github-to-skills/            # GitHub repo → skill 转换
│   │   └── scripts/
│   │       ├── create_github_skill.py
│   │       └── fetch_github_info.py
│   ├── bfg-repo-cleaner/            # Git 仓库清理
│   └── pua/ pua-en/ pua-ja/         # PUA 系列 skills
│
├── meta/                            # Meta-skills (find-skills 等)
├── test/                            # Node.js 单元测试
├── docs/                            # 文档
└── .github/                         # GitHub Actions
```

---

## Skill Structure Standard

Every skill follows this pattern:

```
[skill-name]/
├── SKILL.md              # Required: Core definition with YAML Frontmatter
├── examples/             # Required: At least 1-3 case studies
├── scripts/              # Optional: Automation tools
├── references/           # Optional: Knowledge bases
├── templates/            # Optional: Reusable code snippets
└── resources/            # Optional: Documentation, images
```

**SKILL.md must include YAML frontmatter:**
```yaml
---
name: [Skill Name]
description: [One-line description]
version: 1.0.0
tags: [tag1, tag2]
---
```

---

## Skill Categories

| Category | Description |
|----------|-------------|
| `engineering/` | Prompt optimization, git workflows, code patterns |
| `productivity/` | Media downloading, task analysis |
| `devops/` | Skill management, GitHub automation |
| `creative/` | Design, video, art generation skills |
| `community/` | Community-contributed skills (~130+) |
| `external/` | Externally-sourced skills (git submodule) |

---

## Arena Pipeline (skill 扫描→评分→索引)

完整竞技场流程分三步，由 `scripts/` 下脚本驱动:

```bash
# Step 1: 扫描全库 SKILL.md，提取元数据 → skill-arena/skills_inventory.json
python3 scripts/arena_scan.py

# Step 2: 基于 inventory 做聚类 + 打分 → skill-arena/{clusters,scores,winners}.json
python3 scripts/arena_cluster_score.py

# Step 3: 合并 inventory + scores → index.json (全量重建)
python3 scripts/arena_build_index.py
```

**一键执行全部流程:**
```bash
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py
```

**数据流向:**
```
SKILL.md (各目录)
    ↓ arena_scan.py
skill-arena/skills_inventory.json
    ↓ arena_cluster_score.py
skill-arena/{clusters, scores, winners}.json
    ↓ arena_build_index.py
index.json (主索引，供 hub/CLI 检索)
```

---

## Development Commands

### 新增 Skill
```bash
# 1. 拷贝模板
cp -r _template_skill/ community/my-new-skill/

# 2. 编辑 SKILL.md (填写 frontmatter + 内容)

# 3. 校验结构 + 健康检查
python3 devops/skill-manager/scripts/scan_and_check.py community/my-new-skill/
python3 devops/skill-manager/scripts/scan_and_check.py --health community/my-new-skill/

# 4. [必须] 重建索引 + 竞技场 (任何 skill 新增/修改/删除后必跑)
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py

# 5. 验证搜索能找到
python3 devops/ultraskills-hub/scripts/search.py my-new-skill
```

> ⚠️ **Post-process 强制规则**：任何 skill 内容变更（新增、修改、删除、外部同步）后，
> **必须**执行 Step 4 的 arena pipeline 全量重建。索引未更新 = hub 搜索不到 = 等于没改。

### Skill 管理
```bash
# 列出所有 skills
python3 devops/skill-manager/scripts/list_skills.py

# 校验 skill 结构
python3 devops/skill-manager/scripts/scan_and_check.py community/

# 删除 skill
python3 devops/skill-manager/scripts/delete_skill.py <skill-name>

# 部署 skills 到 ~/.claude/skills
python3 scripts/deploy_skills.py deploy

# 从外部目录/GitHub 同步 skills
python3 scripts/sync_skills.py
```

### Hub 搜索
```bash
python3 devops/ultraskills-hub/scripts/search.py <keyword>
```

### 竞技场独立测试 (devops/skill-arena/)
```bash
# 加载环境变量 + 运行完整 arena 测试框架
cd devops/skill-arena && bash run.sh [args]
```

### Node.js CLI
```bash
node bin/ultraskills.js search <keyword>
node bin/ultraskills.js list
node bin/ultraskills.js install <skill>
```

---

## Working with Skills

1. **Finding skills**: Use `ultraskills-hub` skill → `search.py` over index.json

2. **Creating new skills**: Copy `_template_skill/` → fill SKILL.md → `scan_and_check.py` → rebuild index

3. **Updating skills**: Edit SKILL.md → rebuild index

4. **Skill invocation**: Invoke by name via the `Skill` tool

---

## Key Files

| File | Purpose |
|------|---------|
| `index.json` | Master index (all skills + arena scores) — 唯一数据源 |
| `skill-arena/skills_inventory.json` | arena_scan.py 输出: 全量 skill 清单 |
| `skill-arena/{clusters,scores,winners}.json` | arena_cluster_score.py 输出: 聚类/评分/获胜者 |
| `SKILLS_INDEX.md` | 人工可读索引 |
| `CONTRIBUTING.md` | S-Tier skill 标准 |
| `setup.sh` | 安装 skills 到 ~/.claude/skills/ |
| `scripts/arena_scan.py` | 竞技场 Step1: 扫描 |
| `scripts/arena_cluster_score.py` | 竞技场 Step2: 聚类+评分 |
| `scripts/arena_build_index.py` | 竞技场 Step3: 重建 index.json |
| `devops/ultraskills-hub/scripts/search.py` | Hub 搜索引擎 |
| `devops/skill-manager/scripts/scan_and_check.py` | 结构合规校验 |
| `devops/skill-arena/run.sh` | Arena 测试框架启动器 |

---

## Project Self-Improvement (项目自身强化)

### 改进搜索算法

搜索逻辑在 `devops/ultraskills-hub/scripts/search.py` 的 `search()` 函数。
评分维度：id 匹配(+20/+5) → tag 匹配(+6) → recommended_for(+5) → 描述关键词(×2) → arena bonus。
改进方向：
- 增加中文分词支持（当前按空格切词，中文描述匹配弱）
- 增加 fuzzy match（拼写容错）
- 调整权重（如 tag 权重应该高于描述词频）

### 添加 Arena 测试套件

测试套件在 `devops/skill-arena/test-suites/`，每类一个目录：
```
test-suites/<cluster-name>/
├── tests.yaml              # 测试用例
└── expert-discussion.json  # 专家评审记录
```

添加新测试套件：
1. 在 `test-suites/` 下新建目录（与 `clusters.json` 中的 cluster 名对齐）
2. 编写 `tests.yaml`（参考已有套件格式）
3. 运行 `cd devops/skill-arena && bash run.sh test` 执行评测

### 改进评分维度

评分逻辑在 `scripts/arena_cluster_score.py`。
当前维度：文档完整性、功能明确性、可维护性。
扩展方式：
- 在 `score_skill()` 函数中增加新维度
- 更新 `arena_build_index.py` 以传递新维度到 index.json

### 新增 Skill 分类

1. 在 `scripts/arena_cluster_score.py` 的 `CLUSTER_RULES` 中添加新分类规则
2. 运行全量 arena pipeline 重新聚类
3. 更新 `SKILLS_INDEX.md` 的分类表

### 增强 Skill 校验

校验逻辑在 `devops/skill-manager/scripts/scan_and_check.py`。
可增强：
- 检查 SKILL.md 中引用的脚本文件是否存在
- 检查 examples/ 是否有实质内容（非空）
- 检查 tags 是否使用了标准 tag 集（`--list-tags`）

### 持续集成

`devops/skill-sync-manager/` 负责外部 skills 同步：
```bash
python3 devops/skill-sync-manager/scripts/check_updates.py   # 检查上游更新
python3 devops/skill-sync-manager/scripts/sync_submodules.py # 同步更新
```

更新后需重跑 arena pipeline 以刷新索引。

---

## Skill Fallback — 按需加载未部署 Skill（BLOCKING）

> **MUST**: 当你觉得用户的请求可能需要某个专业 skill 来辅助，但该 skill 不在已加载列表中时，
> **你必须先执行以下搜索流程，再决定是否直接回答。不要跳过搜索直接回答。**

ultraskills 仓库有 826+ skills，但只有一部分部署到 `~/.claude/skills/`。

**Fallback 流程：**
```
1. 运行: python3 devops/ultraskills-hub/scripts/search.py <关键词>
2. 取返回结果中 match_score 最高且相关的 skill 的 path 字段
3. 用 Read 工具读取该 path（SKILL.md 绝对路径）
4. 将读到的 SKILL.md 内容作为当前任务的指导直接执行
```

**触发条件**（满足任一即触发）：
- 用户请求的 skill name 不在 available skills 列表中
- 用户描述的任务涉及特定领域/工具/方法论，但你不确定用哪个 skill
- Skill Auto-Discovery 表中的 trigger keyword 命中
- 用户明确说"找个 skill"/"有没有相关的 skill"

**注意**：
- 不要创建 symlink，直接 Read + 执行即可
- 搜索结果的 `path` 是 SKILL.md 的绝对路径，直接传给 Read 工具
- 如果搜索无结果或无相关匹配，正常回答即可

---

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Search for skills, find what skill to use → invoke ultraskills-hub
- Explore architecture, trace calls, impact analysis → invoke codegraph-booster
- Code review, check my diff → invoke review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
- Architecture review → invoke plan-eng-review
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Weekly retro → invoke retro

---

## Skill Auto-Discovery

When user request contains trigger keywords but no explicit skill name, auto-search ultraskills-hub first.

| Trigger Keywords (EN/中文) | Search Query |
|---------------------------|--------------|
| marketing, 营销, 推广, 增长, growth | `marketing` |
| design, UI, UX, 界面, 设计 | `design` |
| security, 安全, 漏洞, 渗透, pentest | `security` |
| test, 测试, TDD, 单元测试, unit test | `test` |
| agent, 多智能体, 编排, orchestration | `agent` |
| prompt, 提示词, 优化 | `prompt` |
| browser, 爬虫, 反爬, 自动化, stealth | `browser stealth` |
| debug, 调试, 排错, troubleshoot | `debug` |
| review, 审查, 代码审查, code review | `review` |
| deploy, 部署, 发布, CI/CD | `deploy` |
| api, 接口, REST, GraphQL | `api` |
| database, 数据库, SQL, 查询优化 | `database` |

**Workflow:**
1. Detect trigger keyword in user request
2. Invoke `ultraskills-hub` with mapped search query
3. If relevant skill found → invoke that skill
4. If no match → proceed with direct answer
