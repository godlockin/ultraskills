---
name: reverse-skill-router
description: Reverse engineering / penetration testing / CTF / 数字取证 / 漏洞分析 的方法论路由器。Use when user mentions any reverse/pentest/security/CTF/取证/漏洞 keyword (APK, jadx, IDA, Frida, BurpSuite, pwn, ROP, jailbreak, prompt injection, EDR bypass, malware analysis, etc.). 委托给 external/reverse-skill/ 的 83 个 SKILL.md 提供的方法论——同时**主动屏蔽原仓库 RULES.md 的全局 CLAUDE.md 注入指令**以保护用户会话。Trigger 词见 references/trigger-keywords.md。
version: 1.0.0
tags: [security, reverse-engineering, pentest, ctf, forensics, methodology, community]
source: https://github.com/zhaoxuya520/reverse-skill (MIT)
license: MIT (主项目)
license_notes: |
  reverse-skill 主项目 = MIT ✅
  CTF-Sandbox-Orchestrator 子模块 = GPLv3 ⚠️ (submodule 隔离,不污染本仓库)
  Pentest Swarm AI = AGPL-3.0 ⚠️ (仅 CLI/MCP 间接调用)
---

# Reverse Skill Router（逆向技能路由器）

提供 reverse engineering / penetration testing / CTF / 取证 / 漏洞分析的全套方法论入口。本 skill 是**元路由器**——本身不教技术，**路由到** [`external/reverse-skill/`](../../external/reverse-skill/) 下的 83 个领域 SKILL.md。

> **本 skill 的关键责任**：
> 1. **入口路由** — 根据用户任务关键词映射到对应的场景 SKILL.md
> 2. **主动屏蔽注入** — 每次触发时检查并运行 `scripts/shield-reverse-skill.sh`，防止 reverse-skill 的 RULES.md 把 routing 规则写入用户的 `~/.claude/CLAUDE.md`
> 3. **安全边界提醒** — 提醒用户授权、范围、合规

---

## ⚠️ 重要安全声明

### License 混合

reverse-skill 包含 **3 种 license**：

| 组件 | License | 传染性 |
|---|---|---|
| 主项目 reverse-skill | MIT | ✅ 安全 |
| `CTF-Sandbox-Orchestrator/` 子模块 | **GPLv3** | ⚠️ copyleft |
| `pentestswarm`（CLI/MCP 依赖）| **AGPL-3.0** | ⚠️ copyleft + 网络服务条款 |

**作为 git submodule 引入 — 隔离目录，**不污染**本仓库 license**。但调用 GPL/AGPL 组件时遵守对应许可。

### 全局 CLAUDE.md 注入已屏蔽

`external/reverse-skill/RULES.md` 的 `## Global Injection (MUST do on first use)` 段要求 AI 在首次使用时**自动写 routing 规则到用户全局配置**（`~/.claude/CLAUDE.md`、`~/.kiro/steering/` 等）——这会劫持用户所有 Claude Code 会话。

**本仓库已通过 `scripts/shield-reverse-skill.sh` 屏蔽该指令**：
- 把 Global Injection 段替换为警告占位符
- 把 Global Injection Content (Compact) 段标记为 DEPRECATED
- 原始内容保留在 `RULES.md.original.bak`
- **idempotent**：每次触发 router 时自动检查 + re-shield

### 合规边界

reverse-skill 含红队方法论（SQL 注入 / ROP / EDR 绕过 / prompt injection 等）。**仅在合法授权范围使用**：
- SRC（安全响应中心）合法项目
- 自有系统授权测试
- CTF 比赛
- Bug Bounty 平台授权目标

**未经授权的攻击行为违反法律。**

---

## 工作流程

### 1. 主动执行 Shield

每次触发本 skill 时，**第一步**自动执行：

```bash
bash scripts/shield-reverse-skill.sh
```

确保 RULES.md 屏蔽生效（防止 `git submodule update` 拉新版本时丢失 patch）。

### 2. 读取 routing 关键词

读取 [`external/reverse-skill/RULES.md`](../../external/reverse-skill/RULES.md) 的 "Trigger Keywords" 段（约 30+ 关键词分类），判断用户任务属于哪个场景。

完整 trigger 关键词列表见 [`references/trigger-keywords.md`](references/trigger-keywords.md)。

### 3. 路由到对应场景 SKILL.md

`external/reverse-skill/skills/` 下有 40+ 场景目录，每个有独立 SKILL.md。按用户任务类型路由：

| 用户意图关键词 | 路由到 |
|---|---|
| APK / Android / smali / jadx / Frida | [`external/reverse-skill/skills/apk-reverse/SKILL.md`](../../external/reverse-skill/skills/apk-reverse/SKILL.md) |
| iOS / Objection | [`external/reverse-skill/skills/mobile-reverse/SKILL.md`](../../external/reverse-skill/skills/mobile-reverse/SKILL.md) |
| IDA / Ghidra / radare2 / 二进制 | [`external/reverse-skill/skills/reverse-engineering/SKILL.md`](../../external/reverse-skill/skills/reverse-engineering/SKILL.md) |
| JS / SourceMap / 前端加密 | [`external/reverse-skill/skills/js-reverse/SKILL.md`](../../external/reverse-skill/skills/js-reverse/SKILL.md) |
| .NET / dnSpy / C# | [`external/reverse-skill/skills/dotnet-reverse/SKILL.md`](../../external/reverse-skill/skills/dotnet-reverse/SKILL.md) |
| Web 渗透 / Burp / SQLMap / Nuclei | [`external/reverse-skill/skills/attack-chain/SKILL.md`](../../external/reverse-skill/skills/attack-chain/SKILL.md) |
| Pwn / ROP / 栈溢出 | [`external/reverse-skill/skills/pwn-chain/SKILL.md`](../../external/reverse-skill/skills/pwn-chain/SKILL.md) |
| 恶意软件 / YARA | [`external/reverse-skill/skills/malware-analysis/SKILL.md`](../../external/reverse-skill/skills/malware-analysis/SKILL.md) |
| LLM 安全 / prompt injection / jailbreak | [`external/reverse-skill/skills/llm-security/SKILL.md`](../../external/reverse-skill/skills/llm-security/SKILL.md) |
| API / GraphQL / JWT | [`external/reverse-skill/skills/api-security/SKILL.md`](../../external/reverse-skill/skills/api-security/SKILL.md) |
| 固件 / IoT / binwalk | [`external/reverse-skill/skills/firmware-pentest/SKILL.md`](../../external/reverse-skill/skills/firmware-pentest/SKILL.md) |
| Windows AD / 域渗透 / Mimikatz | [`external/reverse-skill/skills/windows-ad/SKILL.md`](../../external/reverse-skill/skills/windows-ad/SKILL.md) |
| 取证 / 证据链 | [`external/reverse-skill/skills/digital-forensics/SKILL.md`](../../external/reverse-skill/skills/digital-forensics/SKILL.md) |
| 威胁狩猎 | [`external/reverse-skill/skills/threat-hunting/SKILL.md`](../../external/reverse-skill/skills/threat-hunting/SKILL.md) |
| EDR 绕过 / 免杀 | [`external/reverse-skill/skills/edr-bypass-re/SKILL.md`](../../external/reverse-skill/skills/edr-bypass-re/SKILL.md) |
| 完整 83 个 SKILL.md 列表 | `external/reverse-skill/skills/*/SKILL.md` |

### 4. 执行场景工作流

按场景 SKILL.md 的流程执行。注意：
- 严格遵守授权范围（**没有 auth.status=granted 不 ACT**）
- 使用 `external/reverse-skill/skills/ops/scope-contract.md` 跟踪 scope
- 按 `external/reverse-skill/skills/ops/evidence-finding-path.md` 记录证据链

---

## 如何首次使用

### 用户侧

```bash
# 1. clone 时初始化 submodule
git submodule update --init external/reverse-skill

# 2. 主动运行屏蔽脚本
bash scripts/shield-reverse-skill.sh

# 3. 浏览主入口
cat external/reverse-skill/README.md

# 4. 浏览 routing
cat external/reverse-skill/RULES.md

# 5. 触发本 router skill（本 skill 的存在就是为了路由）
```

### AI 侧（Claude Code / Cursor 等）

触发本 skill 后，**第一步**应执行：

```bash
bash scripts/shield-reverse-skill.sh
```

然后读取 `external/reverse-skill/RULES.md`（已屏蔽）的 Trigger Keywords 段，再按 3. 路由到对应场景。

---

## 引用与致谢

本 router skill 是 ultraskills 对 [`zhaoxuya520/reverse-skill`](https://github.com/zhaoxuya520/reverse-skill)（18.6k stars）的薄包装。**核心内容来自原仓库**，本 skill 只提供路由 + 屏蔽注入 + 合规边界。

屏蔽脚本：[`scripts/shield-reverse-skill.sh`](../../scripts/shield-reverse-skill.sh)