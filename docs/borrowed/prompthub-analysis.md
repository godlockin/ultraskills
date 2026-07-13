# PromptHub 借鉴分析

> 来源: `https://github.com/legeling/PromptHub` @ v0.5.9 (2026-07-10)
> 分析时间: 2026-07-07
> License: AGPL-3.0 (代码不可 fork,仅借鉴方法论)

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### What is PromptHub?

A local-first AI asset workbench for managing prompts, skills, and agent configurations. Ships as Electron desktop + CLI + self-hosted web, all backed by SQLite. Targets developers using multiple AI coding tools who need a single source of truth across platforms.

### Repo at a glance

| Metric | Value |
|--------|-------|
| Stars / Forks | 1.5k / 178 |
| Commits | 561 |
| Last release | v0.5.9 (2026-07-10) |
| Tech | TypeScript 97.6%, Electron, React, Tailwind, SQLite |
| License | AGPL-3.0 (viral — no code fork allowed) |

### What's interesting

1. **Cross-platform distribution** — single skill, install to 15+ AI tools (Claude Code, Cursor, Windsurf, Codex, Cline, Gemini CLI, Kilo Code, Trae). Each platform has its own convention directory, overridable per-user.
2. **Symlink vs Copy dual mode** — symlink shares upstream edits, copy creates independent local copies. User picks at install time.
3. **Version history + diff/rollback** — every prompt/save writes a version row, supports diff view and one-click rollback. (Storage mechanism undisclosed, likely DB-based.)
4. **Custom store sources** — runtime-add GitHub repos, `skills.sh` registries, or local directories as skill sources. No git submodule needed.
5. **Rules management** — scans `.cursor/rules`, `.claude/CLAUDE.md`, `AGENTS.md` and merges project-level config from multiple AI tools.
6. **AI translation + safety scanning** — sidecar translations per `SKILL.md`, AI-driven content review before install.
7. **WebDAV / self-hosted sync** — cross-device state sync without owning a cloud.

### What UltraSkills already does better

| Dimension | PromptHub | UltraSkills |
|-----------|-----------|-------------|
| Skill library depth | ~20 builtin | **945** (arena-scored) |
| Quality signal | Manual stars | Arena score (75 cluster winners) |
| Search | FTS5 + tag + folder | Arena-weighted + tag + cluster |
| Discovery | Manual browse | Hub MCP `search_skills` + auto-load on demand |
| Source | GitHub repos | Git submodules + curated community/ packages |

### Borrowable insights

We adopt **methodology only** (AGPL prevents code fork). Prioritized:

| Priority | Insight | Effort | Value |
|----------|---------|--------|-------|
| **P0** | Cross-platform distribution (15+ AI tools) | 2-3 days | High — unlocks non-Claude-Code users |
| **P0** | Symlink/Copy mode (user picks per install) | 0.5 day | Medium — fork-friendly workflow |
| **P1** | Local snapshot for `~/.claude/skills/` edits | 1 day | Medium — recover lost local changes |
| **P2** | Custom runtime stores (MCP extension) | 1-2 days | Low-Medium — submodule already covers most cases |
| **Skip** | Electron desktop | — | We're a skill library, not a product |
| **Skip** | Self-hosted web | — | Hub MCP is the equivalent |
| **Skip** | AES-256 + master password | — | Skills are public content |
| **Skip** | 7-language UI | — | Developer-facing only |
| **Skip** | AI translation/safety scan | — | Arena score is objective signal |
| **Skip** | Rules manager (.cursor/rules etc.) | — | Project-level config, out of scope |

### Implementation sketch (P0 cross-platform)

```bash
# New dispatch targets in setup.sh:
./setup.sh --platform claude-code    # default (existing)
./setup.sh --platform cursor         # ~/.cursor/skills/ symlinks
./setup.sh --platform windsurf       # ~/.codeium/windsurf/skills/
./setup.sh --platform codex          # ~/.codex/skills/
./setup.sh --platform cline          # ~/.cline/skills/
./setup.sh --platform all            # deploy to every supported platform
./setup.sh --platform list           # print supported platforms

# Implementation: scripts/distribute.py
# - PLATFORMS dict: { name: {skill_dir, hook_dir?, mcp?, config_merge?} }
# - Per-platform: create skill symlinks + register MCP if needed
# - Idempotent: --remove cleans each platform independently
```

### Symlink/Copy mode

```bash
./setup.sh --mode symlink    # default — single source of truth
./setup.sh --mode copy      # one-shot copy, then independent
./setup.sh --mode both      # symlink + copy side-by-side (test/sandbox)
```

Maps to existing flags:

| Current | New equivalent |
|---------|---------------|
| `./setup.sh` | `./setup.sh --mode symlink` |
| `./setup.sh --top` | `./setup.sh --top --mode copy` (independent picks) |
| `./setup.sh --all` | `./setup.sh --all --mode copy` |

### Local snapshot (P1)

```bash
# Auto-snapshot local edits before they get overwritten
./setup.sh                    # detects dirty ~/.claude/skills/, snapshots first
./setup.sh --restore foo      # pick timestamp from list, restore

# Storage: ~/.ultraskills/snapshots/<skill>/<timestamp>.md
# Captures: full SKILL.md content + diff vs upstream HEAD
```

---

<a name="中文"></a>
## 中文

### PromptHub 是什么?

一个本地优先的 AI 资产工作台,管理 prompt、skill、agent 配置。形态是 Electron 桌面 + CLI + 自部署 Web,全部 SQLite 后端。面向使用多个 AI 编程工具、需要统一管理资产的开发者。

### 仓库速览

| 指标 | 值 |
|------|-----|
| Stars / Forks | 1.5k / 178 |
| Commits | 561 |
| 最新版本 | v0.5.9 (2026-07-10) |
| 技术栈 | TypeScript 97.6%, Electron, React, Tailwind, SQLite |
| License | AGPL-3.0 (强传染 — 代码不可 fork) |

### 关键特性

1. **跨平台分发** — 写一次,装到 15+ AI 工具(Claude Code / Cursor / Windsurf / Codex / Cline / Gemini CLI / Kilo Code / Trae)。每个平台有约定目录,可用户级覆写。
2. **Symlink vs Copy 双模式** — symlink 共享上游编辑,copy 独立本地副本。安装时用户选。
3. **版本历史 + diff/rollback** — 每次保存写版本行,支持 diff 和一键回滚。
4. **自定义 store** — 运行时添加 GitHub 仓库、`skills.sh` 注册中心、本地目录为 skill 源。不需要 git submodule。
5. **Rules 管理** — 扫描 `.cursor/rules`、`.claude/CLAUDE.md`、`AGENTS.md` 并合并多 AI 工具的项目级配置。
6. **AI 翻译 + 安全扫描** — 每个 SKILL.md 的旁挂译文,安装前 AI 内容审阅。
7. **WebDAV / 自部署同步** — 跨设备状态同步,不需要自建云。

### UltraSkills 已经更强的地方

| 维度 | PromptHub | UltraSkills |
|------|-----------|-------------|
| Skill 库深度 | ~20 内置 | **945**(arena 评分) |
| 质量信号 | 手动 star | Arena score(75 cluster winners) |
| 检索 | FTS5 + tag + folder | Arena 加权 + tag + cluster |
| 发现方式 | 手动浏览 | Hub MCP `search_skills` + 按需自动加载 |
| 来源 | GitHub repos | Git submodule + curated community/ 包 |

### 可借鉴之处

**仅借鉴方法论**(AGPL 阻止代码 fork)。优先级排序:

| 优先级 | 借鉴点 | 工作量 | 价值 |
|--------|--------|--------|------|
| **P0** | 跨平台分发(15+ AI 工具) | 2-3 天 | 高 — 解锁非 Claude Code 用户 |
| **P0** | Symlink/Copy 模式(用户安装时选) | 0.5 天 | 中 — 利于 fork 工作流 |
| **P1** | `~/.claude/skills/` 本地编辑的 snapshot | 1 天 | 中 — 恢复本地修改丢失 |
| **P2** | 自定义运行时 store(MCP 扩展) | 1-2 天 | 中低 — submodule 已覆盖大部分场景 |
| **不借鉴** | Electron 桌面 | — | 我们的形态是 skill 库,不是产品 |
| **不借鉴** | 自部署 Web | — | Hub MCP 是同等能力 |
| **不借鉴** | AES-256 + 主密码 | — | skill 是公开内容 |
| **不借鉴** | 7 语言 UI | — | 仅开发者使用 |
| **不借鉴** | AI 翻译/安全扫描 | — | Arena score 是客观信号 |
| **不借鉴** | Rules 管理(.cursor/rules 等) | — | 项目级配置,超出 skill 库范畴 |

### P0 跨平台实现草图

```bash
# setup.sh 新增 --platform 分发目标:
./setup.sh --platform claude-code    # 默认(已有)
./setup.sh --platform cursor         # ~/.cursor/skills/ symlinks
./setup.sh --platform windsurf       # ~/.codeium/windsurf/skills/
./setup.sh --platform codex          # ~/.codex/skills/
./setup.sh --platform cline          # ~/.cline/skills/
./setup.sh --platform all            # 部署到所有支持平台
./setup.sh --platform list           # 打印支持的平台

# 实现: scripts/distribute.py
# - PLATFORMS dict: { name: {skill_dir, hook_dir?, mcp?, config_merge?} }
# - 每平台: 建 skill symlinks + 注册 MCP(如需)
# - 幂等: --remove 独立清理每个平台
```

### Symlink/Copy 模式

```bash
./setup.sh --mode symlink    # 默认 — 单一真相源
./setup.sh --mode copy      # 一次性 copy,后续独立
./setup.sh --mode both      # symlink + copy 并存(测试/沙箱)
```

映射现有 flag:

| 现有 | 新等价 |
|------|--------|
| `./setup.sh` | `./setup.sh --mode symlink` |
| `./setup.sh --top` | `./setup.sh --top --mode copy`(独立选取) |
| `./setup.sh --all` | `./setup.sh --all --mode copy` |

### P1 本地 snapshot

```bash
# 安装前自动 snapshot 本地编辑
./setup.sh                    # 检测到 ~/.claude/skills/ 有改动,先 snapshot
./setup.sh --restore foo      # 从列表选时间戳回滚

# 存储: ~/.ultraskills/snapshots/<skill>/<timestamp>.md
# 捕获: 完整 SKILL.md 内容 + 与 upstream HEAD 的 diff
```

### 与既有架构的衔接

| 改动 | 触及文件 | 兼容 |
|------|---------|------|
| `scripts/distribute.py` | 新增 | 与 setup.sh 完全兼容 — Claude Code 是 `--platform claude-code` 默认 |
| `--mode` flag | setup.sh 重构 | 默认值不变,老 flag 不破坏 |
| `--restore` snapshot | 新增 | 与 `setup.sh --remove` 互补 |