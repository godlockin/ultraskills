# Mole CLI 参考（基于 v1.53.0 实测）

上游: https://github.com/tw93/Mole · Go 单二进制 · GPL-3.0 · macOS only

## 全局选项

| 选项 | 说明 |
|---|---|
| `--debug` | 详细操作日志 |
| `--dry-run` / `-n` | 预览不执行（clean/optimize/uninstall/purge/installer/remove/touchid/completion 均支持） |

## 命令详解

### `mo` — 主菜单
交互式 TUI 入口，列出全部功能。

### `mo clean` — 清理磁盘
| 选项 | 说明 |
|---|---|
| `--dry-run, -n` | 预览 |
| `--external PATH` | 清外置卷 OS 元数据 |
| `--whitelist` | 管理受保护路径 |

类别（dry-run 输出按此分组）：
- User essentials（用户应用缓存/日志）
- Developer（Xcode DerivedData / npm / pip 等）
- System（需 sudo：系统日志 / 系统缓存）

### `mo uninstall` — 完全卸载应用
App 本体 + launch agents/daemons + preferences + 隐藏残留。

### `mo optimize` — 系统优化
刷新 DNS 缓存、Spotlight 索引、Finder 缓存、系统服务。

### `mo analyze [PATH]` — 磁盘分析
终端磁盘浏览器：Vim 导航（j/k/回车进入）、过滤、`d` 移入废纸篓。
默认扫全盘；`mo analyze /Volumes` 只看外置卷。

### `mo status` — 系统监控（只读）
`--json` 输出字段：`health_score`(0-100)、`uptime`、`procs`、`cpu`(usage/per_core/load)、
`memory`、`disk`、`network`、`power`、`hardware`。

### `mo purge` — 清构建产物
删可重建产物（node_modules/target/dist/build 等）。
`--paths` 配置扫描目录。

### `mo installer` — 安装包残留
找已装完的 DMG/PKG/ISO 文件。

### `mo history` — 操作历史
`--json` 输出 `sessions[]`：command/started_at/items/size/actions{removed,trashed,skipped,failed}。
日志文件：`~/Library/Logs/mole/operations.log`、`deletions.log`。

### `mo touchid enable` — Touch ID 免密 sudo
系统级清理需要 sudo 时用。

### `mo update` / `mo remove`
`--force` 强制重装稳定版；`--nightly` 装 main 分支构建；`mo remove` 卸载 Mole 自身。

## 文件位置

| 路径 | 用途 |
|---|---|
| `~/.config/mole/whitelist` | 白名单规则 |
| `~/Library/Logs/mole/operations.log` | 操作日志 |
| `~/Library/Logs/mole/deletions.log` | 删除明细 |
