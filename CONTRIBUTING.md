# 贡献指南 (Contributing Guide)

本指南帮助你构建符合 **S级标准** 的 AI Skills，添加到 UltraSkills 库中。

---

## 🏗️ Skill 构建标准 (The S-Tier Standard)

### 1. 目录结构规范

每个 Skill 必须是一个独立的文件夹：

```text
my-new-skill/                  # 命名使用短横线 (kebab-case)
├── SKILL.md                   # [必需] 核心定义文件
├── examples/                  # [推荐] 示例库
│   ├── basic-usage.md         # 基础用法示例
│   └── advanced-cases.md      # 复杂场景示例
├── templates/                 # [可选] 可复用的模板/代码片段
└── resources/                 # [可选] 辅助文档、速查表、图片
```

### 2. SKILL.md 规范

必须包含 YAML Frontmatter：

```markdown
---
name: [Skill Name, Human Readable]
description: [One-line description of what this skill does]
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

## 🎯 目标 (Goal)
清晰描述本 Skill 解决什么问题。

## 🧠 核心理念 (Core Concepts)
解释背后的方法论（不仅是 How，还有 Why）。

## 🚀 使用流程 (Workflow)
分步骤说明如何执行。

## ✅ 检查清单 (Checklist)
用于验证结果质量的标准。
```

**外部来源 skill** 额外需要：
```yaml
---
name: ...
github_url: https://github.com/org/repo
github_hash: abc1234   # commit hash at time of import
---
```

### 3. 黄金三法则 (The Golden Rules)

#### 法则一：示例即正义 (Examples are King)

- **必须**：至少 1 个完整的 Before/After 或 Input/Output 示例
- **推荐**：在 `examples/` 目录下提供分类示例

#### 法则二：模块化思维 (Modular Thinking)

Skill 应该是**原子化**的：

- ❌ `Software-Development-Master`（太大）
- ✅ `git-commit-guide`, `react-component-generator`, `sql-optimizer`

#### 法则三：元认知设计 (Meta-Cognitive Design)

引导 AI **思考**，不仅仅是填空：

- 引入思维链 (Chain of Thought)
- 包含自我验证步骤

---

## 🔄 添加工作流

### 自建 Skill

1. **Copy** `_template_skill/` 到目标分类目录（`community/` 或 `engineering/` 等）
2. **Fill** 填充 SKILL.md 内容，遵循上述标准
3. **Validate** 校验结构：
   ```bash
   python3 devops/skill-manager/scripts/scan_and_check.py community/my-new-skill/
   ```
4. **Test** 本地试用：`Skill("my-new-skill")` 或直接 Read SKILL.md
5. **Index** 重建索引（扫描 → 聚类评分 → 写入 index.json）：
   ```bash
   python3 scripts/arena_scan.py && \
   python3 scripts/arena_cluster_score.py && \
   python3 scripts/arena_build_index.py
   ```
6. **Verify** 验证搜索能找到：
   ```bash
   python3 devops/ultraskills-hub/scripts/search.py my new skill
   ```

### 引入外部 GitHub Skills 项目

```bash
# 用 github-to-skills skill 自动转换
Skill("github-to-skills")
# → 输入 GitHub repo URL
# → 自动提取 skills、注入 frontmatter、更新 index.json
```

手动引入（整个 repo）：
```bash
git clone https://github.com/org/skills-repo external/skills-repo
# 然后在 SKILL.md 里注入 github_url/github_hash
# 重建索引
python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py
```

### 追踪外部 Skill 更新

外部来源 skill 的 frontmatter 需包含：
```yaml
github_url: https://github.com/org/repo
github_hash: abc1234def   # import 时的 commit hash，用于检测更新
```

检查并同步上游更新：
```bash
python3 devops/skill-sync-manager/scripts/check_updates.py
python3 devops/skill-sync-manager/scripts/sync_submodules.py
# 同步后重建索引
python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py
```

### Computer-Use (trycua/cua)

涉及原生桌面 GUI 自动化（macOS / Windows / Linux / Android）的 skill 必须配套 cua-mcp：

```bash
# 一次性安装
git submodule update --init --recursive
uv venv --python 3.12 external/cua/.venv
external/cua/.venv/bin/pip install external/cua/libs/python/cua external/cua/libs/python/mcp-server
bash devops/cua-mcp/install-global-mcp.sh

# 验证
python3 devops/cua-mcp/scripts/check_install.py
```

**⚠️ AGPL 警告**：禁止安装 `cua-agent[omni]`（含 ultralytics/AGPL-3.0，会污染整个项目）。仅安装 MIT 核心包：`cua` + `cua-mcp-server` + `cua-computer`。

**平台限制**：`lume`（本地 macOS VM）仅支持 Apple Silicon。非 M 系列 Mac 用户只能使用 `cloud` 模式（需 `CUA_API_KEY`）或 `docker` 模式（Linux-only）。

---

## 🔧 项目自身强化

## ✅ 自查清单

提交前检查：

- [ ] 目录结构符合规范（kebab-case 命名）
- [ ] `SKILL.md` 包含 YAML frontmatter（name, description, version, tags）
- [ ] 外部来源 skill 包含 `github_url` 和 `github_hash`
- [ ] 包含至少一个高质量示例
- [ ] `index.json` 已更新
- [ ] 通过 `skill-security-scan` 安全检查（community/external skills 必需）
- [ ] cua-mcp 注册成功（涉及桌面自动化的 skill 必需）
- [ ] 文档清晰、无错别字

---

## 🔧 项目自身强化

### 改进搜索算法

文件：`devops/ultraskills-hub/scripts/search.py` → `search()` 函数

评分链：id 匹配 → tag 匹配 → 描述词频 → arena bonus。
改进方向：中文分词、fuzzy match、权重调优。

### 添加 Arena 测试套件

目录：`devops/skill-arena/test-suites/<cluster>/`
```bash
# 参考已有 tests.yaml 格式新建
# 运行评测
cd devops/skill-arena && bash run.sh test
```

### 改进评分维度

文件：`scripts/arena_cluster_score.py` → `score_skill()`
扩展新维度后重跑 pipeline。

### 增强 Skill 校验

文件：`devops/skill-manager/scripts/scan_and_check.py`
可增强：脚本引用检查、examples 内容检查、tag 标准化。

### 安全扫描 (SkillSpector)

所有 `community/` 和 `external/` skills 在合并前必须通过 NVIDIA SkillSpector 安全检查。
工具位于 `devops/skill-security-scan/`，底层依赖 `external/skillspector/` 子模块（Apache 2.0）。

```bash
# 一次性安装（需要 Python 3.12+）
git submodule update --init --recursive
pip install -e external/skillspector/

# 扫描单个 skill（CI 安全模式，无需 API key）
python3 devops/skill-security-scan/scripts/run_skillspector.py <skill-path> --no-llm

# 全量健康检查（自动包含 Stage 2.5 安全门）
python3 devops/skill-manager/scripts/scan_and_check.py --health community/
```

判定标准（与 SKILL.md 一致）：

| 等级 | 风险分 | 处理 |
|------|--------|------|
| SAFE | 0-29 | 通过合并 |
| CAUTION | 30-69 | 人工 review，PR 中说明 |
| DO NOT INSTALL | ≥70 或含 critical 模式 | 拒绝合并，要求上游修复 |

64 个检测模式覆盖 16 个类别：prompt 注入、MCP 工具投毒、记忆投毒、数据外泄、供应链 CVE、凭据泄漏等。详细分类见 `devops/skill-security-scan/references/skillspector-patterns.md`。

---

让每一个 Skill 都成为精品！🚀
