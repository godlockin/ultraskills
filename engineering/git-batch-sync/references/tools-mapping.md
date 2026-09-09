# Tool Migration Reference

git-batch-sync prefers Rust-based CLI replacements for performance + better UX. Each maps to a POSIX / GNU command.

## Performance map (核心)

| POSIX / GNU | Rust replacement | Speed | 触发场景 |
|---|---|---|---|
| `find` | **fd** | 10-30x | 扫 `.git/` 目录 (本 skill 主用) |
| `grep -r` | **ripgrep** (rg) | 10-100x | 检测 rebase conflict 输出 |
| `cat` | **bat** | — | log / readme 高亮 |
| `ls` | **eza** | — | 目录列表 + git status |
| `diff` | **delta** | — | rebase 冲突 diff 高亮 |
| `du -sh` | **dust** | — | 目录大小可视化 |
| `time` | **hyperfine** | — | benchmark (fd vs find) |
| `wc -l` (代码) | **tokei** | — | 统计 LOC |
| `make` | **just** | — | recipe runner |
| `ps` | **procs** | — | 进程查看 |
| `top` | **btop** | — | 系统监控 |
| `sed` | **sd** | — | 简单替换 |
| `curl` | **xh** | — | HTTP CLI |

## 等价命令对照

```bash
# find → fd
find . -name '*.rs' -not -path '*/target/*'
fd -e rs

# grep -r → rg
grep -rn 'TODO' src/
rg 'TODO' src/

# ls → eza
ls -la
eza -la --git

# du -sh → dust
du -sh ~/code
dust ~/code

# time → hyperfine
hyperfine 'make build'
```

## 降级策略

git-batch-sync 自动检测工具可用性, 缺失时降级:

| 缺失工具 | 降级方案 | 性能影响 |
|---|---|---|
| `fd` | `find` + 6 条 `-not -path` | 10x 慢 |
| `rg` | `grep -qiE` | 100x 慢 (大输出时) |
| `eza` | `ls -la` | 仅 UX 差 |
| `bat` | `cat` | 仅 UX 差 |
| `delta` | 内联 ANSI 颜色 | UX 差 |
| `dust` | 跳过 (summary 不显示) | 无功能影响 |
| `tokei` | 跳过 LOC 统计 | 无功能影响 |
| `hyperfine` | 跳过 benchmark | 无功能影响 |
| `just` | 直接调 bash | 无功能影响 |

## 一键安装

```bash
# 仅核心 (fd + rg)
bash $SKILL_DIR/scripts/install-deps.sh --core-only

# 全部 (含 optional)
bash $SKILL_DIR/scripts/install-deps.sh

# 或 via justfile
just --justfile $SKILL_DIR/scripts/justfile install-deps
```

## 为什么优先 rust 工具

- **性能**: rust 实现 + 多线程 + 内存安全
- **默认友好**: fd 自动跳过 `.gitignore`, rg 自动跳过二进制
- **输出优秀**: bat 语法高亮, delta 侧栏 diff, dust 树形 + 颜色
- **统一哲学**: 一致 flag 风格 (`--type`/`--glob`/`--hidden`)

## 不替换的

| 命令 | 原因 |
|---|---|
| `git` | 没有更快替代 |
| `bash` / `awk` / `sed`(`sd` 仅简单替换) | shell 内置, 替换成本不抵 |
| `ssh` / `scp` | 系统工具 |
| `tar` / `gzip` (ouch) | ouch 更慢, 仅当需要多格式互转时有用 |
