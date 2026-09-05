---
name: mac-mole
description: 用 Mole (`mo`) CLI 深度清理、卸载、优化和监控 macOS。清理缓存/日志/残留 (clean)、完全卸载应用 (uninstall)、刷新系统服务 (optimize)、磁盘空间分析 (analyze)、系统健康监控 (status)、清除构建产物 (purge)。所有破坏性操作先 --dry-run 预览 + 用户确认。Trigger on 清理 Mac / mac clean / 磁盘空间不足 / 清缓存 / uninstall app / 完全卸载 / 系统优化 / mac optimize / disk usage / 磁盘分析 / mole。
version: 1.0.0
created_at: 2026-09-05
entry_point: scripts/mo.sh
dependencies: ["mole >= 1.53.0 (brew install mole)"]
upstream: https://github.com/tw93/Mole
upstream_license: GPL-3.0 (CLI) — 本 skill 只是 CLI 驱动层，不包含 Mole 源码
tags: [mac, macos, clean, uninstall, optimize, disk-space, system-maintenance, community]
---

# mac-mole

驱动 [Mole](https://github.com/tw93/Mole) (`mo`) CLI 做 macOS 维护。Mole 是 66k stars 的开源
(GPL-3.0) Go 单二进制，定位 = CleanMyMac + AppCleaner + DaisyDisk + iStat Menus。

## When to use

- 磁盘空间不足，要找/清大头
- 卸载应用要清干净（launch agents / preferences / 残留）
- 系统卡顿，刷新 DNS / Spotlight / Finder 缓存
- 查看 CPU/内存/磁盘/网络/电源健康度
- 清除 node_modules / target / dist 等可重建构建产物

## When NOT to use

- Linux/Windows → Mole 仅支持 macOS
- 清理 Homebrew 本身 → `brew cleanup`
- Docker 镜像清理 → `docker system prune`

## 安全契约（必须遵守）

1. **先 dry-run 后执行**：任何删除类命令（clean/uninstall/purge/installer）
   第一步必须 `--dry-run`，把预览结果给用户看。
2. **用户确认才执行**：展示 dry-run 摘要（项数/大小/类别）后，等用户明确同意
   才跑真删。绝不自动真删。
3. **尊重白名单**：`~/.config/mole/whitelist` 里的路径受保护。发现误删风险
   （如 Ollama 模型、Playwright 浏览器、JetBrains 配置），先加白名单再清理。
4. **sudo 边界**：系统缓存需要 sudo。用 `mo touchid enable` 配置 Touch ID
   免密 sudo（需用户同意），否则提示用户手动 `sudo -v`。
5. **操作可追溯**：所有操作记录在 `~/Library/Logs/mole/operations.log`，
   可 `mo history` 回查。删错可从 `mo history` 找回路径。

## Quick Start

```bash
# 安装（如未装）
brew install mole

# 系统健康概览（只读，安全）
mo status                    # 交互式仪表盘
mo status --json | jq '.health_score, .cpu.usage, .memory, .disk'

# 磁盘空间分析（只读）
mo analyze /Users            # 指定目录；Vim 导航，d 移入废纸篓

# 清理（先预览！）
mo clean --dry-run           # 预览将删项数/大小
mo clean                     # 用户确认后真删

# 完全卸载应用
mo uninstall --dry-run       # 预览将删除的 app + 关联文件
mo uninstall                 # 选择 app 执行

# 优化系统服务
mo optimize --dry-run
mo optimize                  # 刷新 DNS/Spotlight/Finder 缓存

# 清构建产物（node_modules 等，可重建）
mo purge --dry-run
mo purge

# 找安装包残留（DMG/PKG/ISO）
mo installer --dry-run
mo installer

# 历史回查
mo history                   # 最近 20 次操作
mo history --json | jq '.sessions[] | select(.size != "0B")'
```

## 命令 × 场景路由

| 用户说 | 命令序列 |
|---|---|
| "磁盘满了" / "空间不足" | `mo status --json` 看磁盘 → `mo analyze <目录>` 定位 → `mo clean --dry-run` |
| "清理缓存" | `mo clean --dry-run` → 确认 → `mo clean` |
| "卸载 XX 应用" | `mo uninstall --dry-run` → 确认 → `mo uninstall` |
| "电脑卡" / "优化系统" | `mo optimize --dry-run` → 确认 → `mo optimize` → `mo status` 复查 |
| "清理 node_modules" | `mo purge --dry-run` → 确认 → `mo purge` |
| "系统状态怎么样" | `mo status --json`（只读，直接执行） |
| "删错了怎么办" | `mo history` → 查 operations.log 找路径 |

## 关键输出解读

### mo status --json（健康监控）

```jsonc
{
  "health_score": 100,          // 0-100，<80 需要关注
  "health_score_msg": "Excellent",
  "uptime": "6d 7h",            // 建议定期重启
  "cpu":  { "usage": 49.0, "load1": 14.9, "core_count": 14 },
  "memory": { ... },            // 压力/swap
  "disk":  { ... }              // 剩余空间
}
```

判断规则：
- `health_score < 80` → 列出异常项，建议 optimize
- `load1 > core_count × 2` → CPU 过载，查 `procs`
- 磁盘剩余 < 10% → 优先 `mo analyze` + `mo clean`

### mo clean --dry-run（清理预览）

- `User app cache · 44 items, 13.72GB dry` → 按类别汇总项数/大小
- 白名单提示 `✓ Whitelist: 19 core patterns active` → 受保护路径数
- `System caches need sudo` → 系统级缓存需 sudo 才计入预览

### mo history --json（操作历史）

```jsonc
{ "sessions": [ { "command": "clean", "items": 2353, "size": "35.89GB",
                  "actions": {"removed": 0, "skipped": 30, ...} } ] }
```

`actions.skipped` 大 = 白名单命中多（正常保护行为）。

## 白名单维护（防误删）

```bash
mo clean --whitelist    # 交互管理清理白名单
mo optimize --whitelist # 交互管理优化白名单
```

建议加白名单的目录（重建代价高）：
- `~/.ollama/models/*` — 本地 LLM 模型（下载代价极高）
- `~/Library/Caches/ms-playwright*` — Playwright 浏览器
- `~/.gradle/caches/*` — Gradle 构建缓存
- `~/Library/Caches/JetBrains*` / `~/Library/Application Support/JetBrains*` — IDE 配置
- `~/Library/Mobile Documents*` — iCloud 文档（绝不能删）

## 依赖安装

```bash
# 方式一：Homebrew
brew install mole

# 方式二：官方脚本
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash

# 验证
mo --version   # >= 1.53.0（--json / --dry-run 语义以实测版本为准）
```

可选配置：
```bash
mo touchid enable   # Touch ID 免密 sudo（系统缓存清理需要 sudo）
mo completion       # shell 补全
```

## 环境边界

- 仅 macOS（实验性 Windows 分支不在此 skill 范围）
- `--json` 已验证支持 `status` / `history`；`clean` 等交互命令以 TUI 输出为准
- 外置卷：`mo clean --external /Volumes/XXX`、`mo analyze /Volumes`

## 参考

- 上游仓库: https://github.com/tw93/Mole
- `references/cli-reference.md` — 完整命令参考
- `scripts/mo.sh` — 安全包装（强制 dry-run 门控）
