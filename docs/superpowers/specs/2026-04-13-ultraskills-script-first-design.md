# UltraSkills：脚本优先升级 + 一键部署脚本 — 设计文档

**日期**：2026-04-13  
**状态**：待实现  
**范围**：ultraskills 仓库

---

## 背景

当前 ultraskills 的 skills 大多是「对话式」——所有命令在 SKILL.md 里描述，由 Agent 每次临时拼接执行。这导致：

- 复杂命令（FunASR 30s 分段、FFmpeg filter_complex）每次手拼，参数不一致、易出错
- 没有 `--dry-run`，Agent 执行前无法预览
- 新机器重建环境需要手动逐个创建 symlink

目标：借鉴 cdh_skills 的「脚本优先原则」，对高频/高复杂度 skill 添加 `scripts/` 封装；同时提供一键部署脚本统一管理 `~/.claude/skills/` 目录。

---

## 方案：分层改造（方案 B）

### Layer 1 — Skills 升级

#### 升级范围

| 优先级 | Skill | 封装脚本 | 理由 |
|--------|-------|---------|------|
| P0 | `community/剪口播` | `scripts/transcribe.py` | FunASR 分段参数复杂，每次易漂移 |
| P0 | `community/剪辑` | `scripts/cut.py` | FFmpeg filter_complex 手拼极易出错 |
| P0 | `community/字幕` | `scripts/subtitle.py` | Whisper + FFmpeg 两步，参数多 |
| P1 | `productivity/media-downloader` | `scripts/download.py` | yt-dlp 最优参数组合需固化 |
| P2 | `community/git-commit-master` | `scripts/commit.sh` | Conventional Commits 格式校验 |

community 里其他纯对话式 skill（brainstorming、context-* 等）**不改造**，YAGNI。

#### 改造后目录结构

```
剪口播/
├── scripts/
│   └── transcribe.py      ← 核心命令封装
├── tips/
│   ├── 转录最佳实践.md
│   └── 口误识别方法论.md
├── README.md
└── SKILL.md               ← 加「脚本优先」段落

字幕/
├── scripts/
│   └── subtitle.py
├── 词典.txt
├── README.md
└── SKILL.md

剪辑/
├── scripts/
│   └── cut.py
├── README.md
└── SKILL.md

media-downloader/
├── scripts/
│   └── download.py
├── examples/
└── SKILL.md

git-commit-master/
├── scripts/
│   └── commit.sh
└── SKILL.md
```

#### SKILL.md 改造模式

在每个升级的 skill 的 SKILL.md `## 流程` 之前，插入「脚本优先」段落：

```markdown
## ⭐ 脚本优先原则

**必须**优先使用 `scripts/` 目录下的脚本，而非手动拼命令。

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 转录视频 | `python3 scripts/transcribe.py <video>` | 手动拼 funasr 参数 |
| 识别口误 | 同上（脚本内置） | 逐句临时分析 |
```

#### 各脚本接口设计

**`剪口播/scripts/transcribe.py`**

```
用法：python3 scripts/transcribe.py <video.mp4> [--dry-run]

功能：
  - 自动 30s 分段（避免 FunASR 时间戳漂移）
  - 内置口误/语气词/静音识别（从 tips/ 读方法论）
  - 检查依赖：funasr, modelscope

输出：
  01-{name}_transcript.json   # 转录结果（含字符级时间戳）
  01-{name}_审查稿.md          # 口误审查稿，展示给用户确认
```

**`剪辑/scripts/cut.py`**

```
用法：python3 scripts/cut.py <video.mp4> <审查稿.md> [--dry-run]

功能：
  - 解析审查稿中勾选的 (start-end) 时间段
  - 生成 FFmpeg filter.txt（trim+concat）
  - --dry-run：只打印 FFmpeg 命令，不执行
  - 检查依赖：ffmpeg

输出：
  01-{name}-v{N}.mp4          # 版本号自动递增
  01-{name}-v{N}_transcript.json  # 重新转录（验证用）
```

**`字幕/scripts/subtitle.py`**

```
用法：
  python3 scripts/subtitle.py <video.mp4>               # 阶段1：生成字幕稿
  python3 scripts/subtitle.py <video.mp4> <字幕稿.txt>  # 阶段2：烧录

阶段1功能：
  - Whisper 转录（medium 模型，zh）
  - 词典纠错（读取 词典.txt）
  - 输出字幕稿.txt（≤15字/行，等用户审核）

阶段2功能：
  - 匹配时间戳 → 生成 SRT
  - FFmpeg 烧录（白字黑边，底部居中）
  - 检查依赖：whisper, ffmpeg

输出：
  01-{name}_字幕稿.txt
  01-{name}.srt
  01-{name}-字幕.mp4
```

**`media-downloader/scripts/download.py`**

```
用法：python3 scripts/download.py <url> [--audio-only] [--quality 720]

功能：
  - 自动识别平台（YouTube / Bilibili / 通用）
  - 选最优格式（bv+ba/b）
  - Bilibili 1080p 自动提示 cookie 配置
  - 检查依赖：yt-dlp, ffmpeg

输出：
  {title}.mp4 / {title}.mp3（--audio-only）
```

**`git-commit-master/scripts/commit.sh`**

```
用法：bash scripts/commit.sh [--dry-run]

功能：
  - 检查 git staged 是否有内容
  - 按 Conventional Commits 格式生成 message
  - --dry-run：只打印 message，不执行 git commit
```

#### 通用脚本约定

所有脚本遵循：

1. **`check_deps()`**：顶部检查依赖，缺失时给出安装命令，不崩溃
2. **`--dry-run`**：打印将执行的命令，不实际执行
3. **错误友好**：失败时输出人类可读的修复建议，而非 traceback
4. **输出命名规范**：`{序号}-{name}-v{N}.{ext}`，版本号自动递增

---

### Layer 2 — 部署脚本

#### 文件位置

```
ultraskills/
└── scripts/
    ├── bootstrap.sh           ← 新增
    ├── init_project_skills.sh ← 保留不动
    └── sync_skills.py         ← 保留不动
```

`bootstrap.sh` 和 `init_project_skills.sh` 职责不重叠：
- `bootstrap.sh`：管理 `~/.claude/skills/`（全局）
- `init_project_skills.sh`：把 skills 注入某个项目（项目级）

#### 三个模式

**`--self`（默认）：个人快速重建**

```bash
bash scripts/bootstrap.sh
```

行为：
1. 自动检测 ultraskills 仓库路径（处理 OneDrive 软链接）
2. 遍历 `community/ engineering/ creative/ devops/ productivity/`
3. 跳过 `external/`（子模块，按需手动安装）
4. 为每个 skill 在 `~/.claude/skills/` 创建 symlink
5. 输出报告：新建 N / 已存在 N / 失败 N

**`--guided`：交互式（给他人用）**

```bash
bash scripts/bootstrap.sh --guided
```

行为（复用 `init_project_skills.sh` 的 `interactive_select()` 等函数）：
1. 按分类展示 skills（含描述，从 SKILL.md frontmatter 读取）
2. 用户输入数字/范围勾选（如 `1,3,5-8` 或 `all`）
3. 支持 `--target` 指定安装目录（默认 `~/.claude/skills/`）
4. 确认后建 symlink

**`--upgrade`：更新**

```bash
bash scripts/bootstrap.sh --upgrade
```

行为：
1. `git pull`（更新 ultraskills 仓库）
2. `git submodule update --remote`（更新 external/ 子模块）
3. 扫描 `~/.claude/skills/` 下所有 symlink
4. 修复断链（目标已不存在的 symlink）
5. 报告：更新了哪些 / 修复了哪些断链

#### 脚本参数完整列表

```
bash scripts/bootstrap.sh [OPTIONS]

选项：
  (无)          --self 模式，快速全量安装
  --guided      交互式选择
  --upgrade     更新仓库 + 修复断链
  --dry-run     只打印操作，不实际执行
  --target DIR  指定安装目录（默认 ~/.claude/skills）
  --help        显示帮助
```

---

## 实现顺序

```
Phase 1（高价值，先做）：
  1. bootstrap.sh — 部署脚本
  2. 剪口播/scripts/transcribe.py + SKILL.md 更新
  3. 剪辑/scripts/cut.py + SKILL.md 更新

Phase 2：
  4. 字幕/scripts/subtitle.py + SKILL.md 更新
  5. media-downloader/scripts/download.py + SKILL.md 更新

Phase 3（可选）：
  6. git-commit-master/scripts/commit.sh + SKILL.md 更新
```

---

## 不做的事（YAGNI）

- ❌ pre-commit hook 校验（个人库，不需要）
- ❌ marketplace.json 分组（没有多团队分发需求）
- ❌ 双仓库同步 CI/CD（个人库）
- ❌ 改造对话式 skill（brainstorming 等无脚本化价值）
