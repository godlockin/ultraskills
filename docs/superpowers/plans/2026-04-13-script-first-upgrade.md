# UltraSkills 脚本优先升级 + 一键部署 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为视频处理类和工具类 skills 添加 `scripts/` 封装，并提供 `bootstrap.sh` 一键管理 `~/.claude/skills/` 全局目录。

**Architecture:** 分两层并行推进——Layer 1 在各 skill 目录内新增 `scripts/` Python/bash 脚本并更新 SKILL.md；Layer 2 新增 `scripts/bootstrap.sh`，复用 `init_project_skills.sh` 的已有函数，支持 `--self / --guided / --upgrade` 三模式。

**Tech Stack:** Python 3.x（FunASR, modelscope, openai-whisper, yt-dlp）、FFmpeg、bash/zsh、git

---

## 文件清单

| 操作 | 路径 |
|------|------|
| 新建 | `community/剪口播/scripts/transcribe.py` |
| 修改 | `community/剪口播/SKILL.md` |
| 新建 | `community/剪辑/scripts/cut.py` |
| 修改 | `community/剪辑/SKILL.md` |
| 新建 | `community/字幕/scripts/subtitle.py` |
| 修改 | `community/字幕/SKILL.md` |
| 新建 | `productivity/media-downloader/scripts/download.py` |
| 修改 | `productivity/media-downloader/SKILL.md` |
| 新建 | `community/git-commit-master/scripts/commit.sh` |
| 修改 | `community/git-commit-master/SKILL.md` |
| 新建 | `scripts/bootstrap.sh` |

---

## Task 1: bootstrap.sh — `--self` 模式

**Files:**
- Create: `scripts/bootstrap.sh`

> 先做部署脚本，因为它独立、无外部依赖，完成后立刻可用。

- [ ] **Step 1: 创建脚本骨架，解析参数**

```bash
# scripts/bootstrap.sh
#!/usr/bin/env bash
set -euo pipefail

UPGRADE=false
GUIDED=false
DRY_RUN=false
TARGET_DIR="$HOME/.claude/skills"

for arg in "$@"; do
  case $arg in
    --upgrade)  UPGRADE=true ;;
    --guided)   GUIDED=true ;;
    --dry-run)  DRY_RUN=true ;;
    --target=*) TARGET_DIR="${arg#*=}" ;;
    --help)
      echo "Usage: bash scripts/bootstrap.sh [--upgrade] [--guided] [--dry-run] [--target=DIR]"
      exit 0 ;;
  esac
done

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'; BOLD='\033[1m'
ok()   { echo -e "${GREEN}✓ $1${NC}"; }
info() { echo -e "${CYAN}  $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
err()  { echo -e "${RED}✗ $1${NC}"; }
step() { echo -e "\n${BOLD}${YELLOW}→ $1${NC}"; }
```

- [ ] **Step 2: 实现仓库路径自动检测**

在骨架后追加（检测 OneDrive 软链接）：

```bash
# 自动检测 ultraskills 仓库根目录（支持 OneDrive 软链接）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
info "仓库路径: $REPO_ROOT"
```

- [ ] **Step 3: 实现 `--self` 核心逻辑（遍历分类，创建 symlink）**

```bash
SKILL_CATEGORIES=("community" "engineering" "creative" "devops" "productivity")
NEW=0; EXISTS=0; FAIL=0

do_symlink() {
  local src="$1" name="$2"
  local dst="$TARGET_DIR/$name"
  if [ -L "$dst" ] && [ -e "$dst" ]; then
    info "已存在: $name"
    EXISTS=$((EXISTS + 1))
  elif $DRY_RUN; then
    info "[DRY-RUN] ln -s $src $dst"
    NEW=$((NEW + 1))
  else
    mkdir -p "$TARGET_DIR"
    ln -sf "$src" "$dst" && ok "链接: $name" && NEW=$((NEW + 1)) \
      || { err "失败: $name"; FAIL=$((FAIL + 1)); }
  fi
}

if ! $GUIDED && ! $UPGRADE; then
  step "安装所有 skills → $TARGET_DIR"
  for cat in "${SKILL_CATEGORIES[@]}"; do
    cat_dir="$REPO_ROOT/$cat"
    [ -d "$cat_dir" ] || continue
    for skill_dir in "$cat_dir"/*/; do
      [ -d "$skill_dir" ] || continue
      skill_name="$(basename "$skill_dir")"
      do_symlink "$skill_dir" "$skill_name"
    done
  done
  echo ""
  echo -e "${BOLD}完成: 新建 ${GREEN}$NEW${NC} / 已存在 ${CYAN}$EXISTS${NC} / 失败 ${RED}$FAIL${NC}"
fi
```

- [ ] **Step 4: 手动验证 `--self` 模式**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills
bash scripts/bootstrap.sh --dry-run
# 预期：打印所有 skill 的 [DRY-RUN] ln -s 行，无报错
```

- [ ] **Step 5: 提交**

```bash
git add scripts/bootstrap.sh
git commit -m "feat(bootstrap): add --self mode for global skill symlink setup"
```

---

## Task 2: bootstrap.sh — `--upgrade` 模式

**Files:**
- Modify: `scripts/bootstrap.sh`

- [ ] **Step 1: 追加 `--upgrade` 逻辑**

```bash
if $UPGRADE; then
  step "更新仓库..."
  $DRY_RUN && info "[DRY-RUN] git pull" || git -C "$REPO_ROOT" pull
  $DRY_RUN && info "[DRY-RUN] git submodule update --remote" \
    || git -C "$REPO_ROOT" submodule update --remote --quiet

  step "修复断链..."
  FIXED=0
  for link in "$TARGET_DIR"/*/; do
    link="${link%/}"
    [ -L "$link" ] || continue
    if [ ! -e "$link" ]; then
      warn "断链: $(basename "$link")"
      $DRY_RUN && info "[DRY-RUN] rm $link" || { rm "$link"; FIXED=$((FIXED + 1)); }
    fi
  done
  ok "修复断链: $FIXED 个"
  exit 0
fi
```

- [ ] **Step 2: 验证 `--upgrade --dry-run`**

```bash
bash scripts/bootstrap.sh --upgrade --dry-run
# 预期：打印 git pull / git submodule update，扫描 ~/.claude/skills/ 断链，无实际操作
```

- [ ] **Step 3: 提交**

```bash
git add scripts/bootstrap.sh
git commit -m "feat(bootstrap): add --upgrade mode with broken symlink repair"
```

---

## Task 3: bootstrap.sh — `--guided` 模式

**Files:**
- Modify: `scripts/bootstrap.sh`

> `--guided` 复用 `init_project_skills.sh` 中已有的函数，采用 source 方式，不复制代码。

- [ ] **Step 1: 确认 `init_project_skills.sh` source 后 main() 不自动执行（必须先于 Step 2）**

```bash
grep -n "^main" ~/Desktop/working/sourcecode/tools/ultraskills/scripts/init_project_skills.sh
# 若末尾有 main "$@"，则修改为守卫写法，防止 source 时自动执行：
```

如末尾是 `main "$@"` 则改为：
```bash
[ "${BASH_SOURCE[0]}" = "$0" ] && main "$@"
```

同时确认函数名存在：
```bash
grep -n "^collect_available_skills\|^interactive_select\|^SKILL_NAMES\|^SKILL_PATHS\|^SKILL_SELECTED" \
  ~/Desktop/working/sourcecode/tools/ultraskills/scripts/init_project_skills.sh
# 预期：找到 collect_available_skills() 和 interactive_select() 定义
# 若函数名不同，在 Step 2 中使用实际函数名
```

- [ ] **Step 2: 追加 `--guided` 逻辑（使用 Step 1 确认的实际函数名）**

```bash
if $GUIDED; then
  # source 复用 init_project_skills.sh 的交互函数（已确认 main() 有守卫）
  source "$SCRIPT_DIR/init_project_skills.sh" || {
    err "无法加载 init_project_skills.sh"; exit 1
  }

  step "收集可用 skills..."
  collect_available_skills  # 填充 SKILL_NAMES / SKILL_PATHS 全局数组

  step "选择要安装的 skills"
  interactive_select        # 填充 SKILL_SELECTED 全局数组

  step "安装选中 skills → $TARGET_DIR"
  for i in "${!SKILL_SELECTED[@]}"; do
    [ "${SKILL_SELECTED[$i]}" = "true" ] || continue
    do_symlink "${SKILL_PATHS[$i]}" "${SKILL_NAMES[$i]}"
  done
  echo ""
  echo -e "${BOLD}完成: 新建 ${GREEN}$NEW${NC} / 已存在 ${CYAN}$EXISTS${NC} / 失败 ${RED}$FAIL${NC}"
  exit 0
fi
```

- [ ] **Step 3: 验证 `--guided` 交互流程**

```bash
bash scripts/bootstrap.sh --guided --dry-run
# 预期：显示 skill 列表，允许输入数字选择，打印 [DRY-RUN] 安装行
```

- [ ] **Step 4: 提交**

```bash
git add scripts/bootstrap.sh scripts/init_project_skills.sh
git commit -m "feat(bootstrap): add --guided interactive mode"
```

---

## Task 4: transcribe.py（剪口播）

**Files:**
- Create: `community/剪口播/scripts/transcribe.py`
- Modify: `community/剪口播/SKILL.md`

- [ ] **Step 1: 创建脚本，写依赖检查和常量**

```python
#!/usr/bin/env python3
"""
transcribe.py — 视频转录 + 口误识别
用法: python3 scripts/transcribe.py <video.mp4> [--dry-run]
"""
import sys, re, json, argparse
from pathlib import Path

FILLER_WORDS = ["嗯", "哎", "诶", "啊"]
SILENCE_THRESHOLD_S = 1.0
SEGMENT_DURATION_S = 30

def check_deps(dry_run: bool = False):
    missing = []
    try: import funasr
    except ImportError: missing.append("funasr  # pip install funasr")
    try: import modelscope
    except ImportError: missing.append("modelscope  # pip install modelscope")
    if missing:
        if dry_run:
            print("⚠️  以下依赖未安装（dry-run 模式下可继续）：")
            for m in missing: print(f"   pip install {m.split('#')[0].strip()}")
        else:
            print("❌ 缺少依赖，请先安装：")
            for m in missing: print(f"   pip install {m.split('#')[0].strip()}")
            sys.exit(1)

def parse_filename(video_path: Path):
    """从文件名解析序号和名称: 01-demo.mp4 → ('01', 'demo')"""
    stem = video_path.stem  # '01-demo'
    m = re.match(r'^(\d+)-(.+)$', stem)
    if m:
        return m.group(1), m.group(2)
    return '01', stem
```

- [ ] **Step 2: 实现 30s 分段转录逻辑**

```python
def transcribe_video(video_path: Path, dry_run: bool) -> list:
    """分段转录，返回合并后的 tokens 列表（含字符级时间戳）"""
    from funasr import AutoModel
    if dry_run:
        print(f"[DRY-RUN] FunASR 转录: {video_path} (30s 分段)")
        return []

    model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                      vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                      punc_model="ct-punc-c", punc_model_revision="v2.0.0")
    result = model.generate(input=str(video_path),
                            batch_size_s=SEGMENT_DURATION_S,
                            return_raw_text=True)
    # result[0]['timestamp'] 是字符级时间戳列表 [[start_ms, end_ms], ...]
    tokens = []
    for char, ts in zip(result[0]['text'], result[0]['timestamp']):
        tokens.append({'char': char, 'start': ts[0]/1000, 'end': ts[1]/1000})
    return tokens
```

- [ ] **Step 3: 实现口误/语气词/静音识别，生成审查稿**

```python
def find_fillers(tokens: list) -> list:
    """识别语气词，返回删除项列表"""
    items = []
    for i, t in enumerate(tokens):
        if t['char'] in FILLER_WORDS:
            prev_end = tokens[i-1]['end'] if i > 0 else t['start']
            next_start = tokens[i+1]['start'] if i < len(tokens)-1 else t['end']
            items.append({'type': '语气词', 'text': t['char'],
                          'start': prev_end, 'end': next_start})
    return items

def find_silences(tokens: list) -> list:
    """识别静音段（相邻 token 间隔 >= SILENCE_THRESHOLD_S）"""
    items = []
    for i in range(1, len(tokens)):
        gap = tokens[i]['start'] - tokens[i-1]['end']
        if gap >= SILENCE_THRESHOLD_S:
            items.append({'type': '静音', 'text': f'静音{gap:.1f}s',
                          'start': tokens[i-1]['end'], 'end': tokens[i]['start']})
    return items

def write_review_draft(seq: str, name: str, tokens: list,
                       fillers: list, silences: list, out_dir: Path):
    """生成审查稿 Markdown"""
    lines = [f"# {seq}-{name} 审查稿\n"]
    lines.append(f"## 语气词（{len(fillers)}处）\n")
    for i, f in enumerate(fillers, 1):
        lines.append(f"- [ ] {i}. `({f['start']:.3f}-{f['end']:.3f})` 删\"{f['text']}\"\n")
    lines.append(f"\n## 静音（{len(silences)}处）\n")
    for i, s in enumerate(silences, 1):
        lines.append(f"- [ ] {i}. `({s['start']:.3f}-{s['end']:.3f})` {s['text']}\n")
    draft_path = out_dir / f"{seq}-{name}_审查稿.md"
    draft_path.write_text(''.join(lines), encoding='utf-8')
    print(f"✅ 审查稿: {draft_path}")
    return draft_path
```

- [ ] **Step 4: 实现 main 入口**

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    check_deps(dry_run=args.dry_run)
    seq, name = parse_filename(args.video)
    out_dir = args.video.parent

    tokens = transcribe_video(args.video, args.dry_run)

    if not args.dry_run:
        # 保存 transcript JSON
        transcript_path = out_dir / f"{seq}-{name}_transcript.json"
        transcript_path.write_text(json.dumps(tokens, ensure_ascii=False, indent=2))
        print(f"✅ 转录: {transcript_path}")

        fillers = find_fillers(tokens)
        silences = find_silences(tokens)
        write_review_draft(seq, name, tokens, fillers, silences, out_dir)

if __name__ == '__main__':
    main()
```

- [ ] **Step 5: 验证 `--dry-run`（无需 GPU/模型）**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills/community/剪口播
python3 scripts/transcribe.py some_video.mp4 --dry-run
# 预期: [DRY-RUN] FunASR 转录: some_video.mp4 (30s 分段)
# 缺少 funasr 时: ❌ 缺少依赖，请先安装...
```

- [ ] **Step 6: 更新 SKILL.md，加「脚本优先」段落**

在 `community/剪口播/SKILL.md` 的 `## 流程` 前插入：

```markdown
## ⭐ 脚本优先原则

**必须**优先使用 `scripts/` 目录下的脚本，而非手动拼命令。

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 转录视频 + 识别口误 | `python3 scripts/transcribe.py <video.mp4>` | 手动拼 funasr 参数 |
| 预览模式（无需模型） | `python3 scripts/transcribe.py <video.mp4> --dry-run` | 直接调用 AutoModel |
```

- [ ] **Step 7: 提交**

```bash
git add community/剪口播/scripts/transcribe.py community/剪口播/SKILL.md
git commit -m "feat(剪口播): add transcribe.py with script-first principle"
```

---

## Task 5: cut.py（剪辑）

**Files:**
- Create: `community/剪辑/scripts/cut.py`
- Modify: `community/剪辑/SKILL.md`

- [ ] **Step 1: 创建脚本，实现审查稿解析**

```python
#!/usr/bin/env python3
"""
cut.py — 解析审查稿，生成 FFmpeg filter.txt 并执行剪辑
用法: python3 scripts/cut.py <video.mp4> <审查稿.md> [--dry-run]
"""
import sys, re, json, argparse, subprocess
from pathlib import Path

def check_deps():
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
    if result.returncode != 0:
        print("❌ 缺少 ffmpeg，请安装: brew install ffmpeg")
        sys.exit(1)

def parse_filename(video_path: Path):
    stem = video_path.stem
    # 匹配 01-name-v1 格式
    m = re.match(r'^(\d+)-(.+?)(?:-v(\d+))?$', stem)
    if m:
        return m.group(1), m.group(2), int(m.group(3) or 1)
    return '01', stem, 1

def parse_review_draft(draft_path: Path) -> list[tuple[float, float]]:
    """解析审查稿中 [x] 勾选的时间段，返回 [(start, end), ...] 删除列表"""
    deletes = []
    pattern = re.compile(r'- \[x\].*?`\((\d+\.\d+)-(\d+\.\d+)\)`')
    for line in draft_path.read_text(encoding='utf-8').splitlines():
        m = pattern.search(line)
        if m:
            deletes.append((float(m.group(1)), float(m.group(2))))
    return sorted(deletes)
```

- [ ] **Step 2: 实现保留区间计算和 filter.txt 生成**

```python
def compute_keep_segments(deletes: list, duration: float) -> list[tuple[float, float]]:
    """删除区间的补集 = 保留区间"""
    keep = []
    prev = 0.0
    for start, end in deletes:
        if start > prev:
            keep.append((prev, start))
        prev = end
    if prev < duration:
        keep.append((prev, duration))
    return keep

def get_video_duration(video_path: Path) -> float:
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)],
        capture_output=True, text=True)
    return float(result.stdout.strip())

def write_filter(keep: list, n_segments: int) -> str:
    """生成 FFmpeg filter_complex 字符串"""
    lines = []
    for i, (s, e) in enumerate(keep):
        lines.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{i}];")
        lines.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{i}];")
    concat_v = ''.join(f'[v{i}]' for i in range(n_segments))
    concat_a = ''.join(f'[a{i}]' for i in range(n_segments))
    lines.append(f"{concat_v}{concat_a}concat=n={n_segments}:v=1:a=1[outv][outa]")
    return '\n'.join(lines)
```

- [ ] **Step 3: 实现 main，执行 FFmpeg**

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('draft', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    check_deps()
    seq, name, version = parse_filename(args.video)
    out_version = version + 1
    out_video = args.video.parent / f"{seq}-{name}-v{out_version}.mp4"
    filter_file = args.video.parent / f"filter_{seq}-{name}-v{out_version}.txt"

    deletes = parse_review_draft(args.draft)
    if not deletes:
        print("⚠️  审查稿中无勾选项，无需剪辑")
        return

    if args.dry_run:
        # dry-run 时跳过 ffprobe（视频文件可能不存在），用占位时长演示
        keep = compute_keep_segments(deletes, 999.0)
        filter_str = write_filter(keep, len(keep))
        print(f"[DRY-RUN] filter.txt 内容:\n{filter_str}")
        print(f"[DRY-RUN] ffmpeg -y -i {args.video} -filter_complex_script {filter_file} "
              f"-map '[outv]' -map '[outa]' -c:v libx264 -crf 18 -c:a aac {out_video}")
        return

    duration = get_video_duration(args.video)
    keep = compute_keep_segments(deletes, duration)
    filter_str = write_filter(keep, len(keep))

    filter_file.write_text(filter_str)
    cmd = ['ffmpeg', '-y', '-i', str(args.video),
           '-filter_complex_script', str(filter_file),
           '-map', '[outv]', '-map', '[outa]',
           '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', str(out_video)]
    subprocess.run(cmd, check=True)
    print(f"✅ 输出: {out_video}")

if __name__ == '__main__':
    main()
```

- [ ] **Step 4: 验证 `--dry-run`**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills/community/剪辑
# 准备一个包含 [x] 勾选行的测试审查稿
echo "- [x] 1. \`(1.000-2.500)\` 删\"嗯\"" > test_审查稿.md
python3 scripts/cut.py test_video.mp4 test_审查稿.md --dry-run
# 预期：打印 filter.txt 内容（含 trim/concat）和 FFmpeg 命令
rm test_审查稿.md
```

- [ ] **Step 5: 更新 SKILL.md**

在 `community/剪辑/SKILL.md` 的 `## 流程` 前插入：

```markdown
## ⭐ 脚本优先原则

**必须**优先使用 `scripts/` 目录下的脚本。

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 执行剪辑 | `python3 scripts/cut.py <video.mp4> <审查稿.md>` | 手动拼 FFmpeg filter_complex |
| 预览 FFmpeg 命令 | 加 `--dry-run` 参数 | 直接执行 ffmpeg |
```

- [ ] **Step 6: 提交**

```bash
git add community/剪辑/scripts/cut.py community/剪辑/SKILL.md
git commit -m "feat(剪辑): add cut.py with filter_complex generation"
```

---

## Task 6: subtitle.py（字幕）

**Files:**
- Create: `community/字幕/scripts/subtitle.py`
- Modify: `community/字幕/SKILL.md`

- [ ] **Step 1: 创建脚本骨架，依赖检查，词典加载**

```python
#!/usr/bin/env python3
"""
subtitle.py — 字幕生成与烧录（两阶段）
阶段1: python3 scripts/subtitle.py <video.mp4>
阶段2: python3 scripts/subtitle.py <video.mp4> <字幕稿.txt>
"""
import sys, re, json, argparse, subprocess
from pathlib import Path

def check_deps(dry_run: bool = False):
    missing = []
    try: import whisper
    except ImportError: missing.append("openai-whisper  # pip install openai-whisper")
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
    if result.returncode != 0:
        missing.append("ffmpeg  # brew install ffmpeg")
    if missing:
        if dry_run:
            print("⚠️  以下依赖未安装（dry-run 模式下可继续）：")
            [print(f"   {m}") for m in missing]
        else:
            print("❌ 缺少依赖："); [print(f"   {m}") for m in missing]; sys.exit(1)

def load_dict(dict_path: Path) -> list[str]:
    """读取词典.txt，每行一个正确写法"""
    if not dict_path.exists():
        return []
    return [l.strip() for l in dict_path.read_text(encoding='utf-8').splitlines() if l.strip()]

def apply_dict(text: str, words: list[str]) -> str:
    """词典纠错：大小写不敏感替换"""
    for w in words:
        text = re.sub(re.escape(w), w, text, flags=re.IGNORECASE)
    return text

def parse_filename(video_path: Path):
    stem = video_path.stem
    m = re.match(r'^(\d+)-(.+)$', stem)
    return (m.group(1), m.group(2)) if m else ('01', stem)
```

- [ ] **Step 2: 实现阶段 1（转录 → 字幕稿）**

```python
def stage1_transcribe(video: Path, seq: str, name: str, dry_run: bool):
    dict_path = Path(__file__).parent.parent / '词典.txt'
    words = load_dict(dict_path)

    if dry_run:
        print(f"[DRY-RUN] whisper {video} --model medium --language zh --output_format json")
        return

    import whisper
    model = whisper.load_model("medium")
    result = model.transcribe(str(video), language='zh', word_timestamps=True)

    # 保存含词级时间戳的 JSON
    ts_path = video.parent / f"{seq}-{name}_whisper.json"
    ts_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))

    # 生成字幕稿（≤15字/行）
    MAX_CHARS = 15
    lines = []
    buf = ''
    for seg in result['segments']:
        for word in seg.get('words', []):
            w = apply_dict(word['word'].strip(), words)
            if len(buf) + len(w) > MAX_CHARS:
                if buf: lines.append(buf)
                buf = w
            else:
                buf += w
    if buf: lines.append(buf)

    draft_path = video.parent / f"{seq}-{name}_字幕稿.txt"
    draft_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✅ 字幕稿（{len(lines)}行）: {draft_path}")
    print("📝 请审核后，再运行阶段2：")
    print(f"   python3 scripts/subtitle.py {video} {draft_path}")
```

- [ ] **Step 3: 实现阶段 2（字幕稿 → SRT → 烧录）**

```python
def stage2_burn(video: Path, draft: Path, seq: str, name: str, dry_run: bool):
    """对齐时间戳：字幕稿每行 → whisper JSON 等长片段首词start/末词end"""
    ts_path = video.parent / f"{seq}-{name}_whisper.json"
    srt_path = video.parent / f"{seq}-{name}.srt"
    out_path = video.parent / f"{seq}-{name}-字幕.mp4"

    cmd = ['ffmpeg', '-y', '-i', str(video),
           '-vf', f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&HFFFFFF,"
                  "OutlineColour=&H000000,Outline=2,Alignment=2'",
           '-c:a', 'copy', str(out_path)]

    if dry_run:
        print(f"[DRY-RUN] 生成 SRT: {srt_path}")
        print(f"[DRY-RUN] FFmpeg: {' '.join(cmd)}")
        return

    if not ts_path.exists():
        print(f"❌ 找不到时间戳文件: {ts_path}，请先运行阶段1"); sys.exit(1)

    result = json.loads(ts_path.read_text())
    lines = [l for l in draft.read_text(encoding='utf-8').splitlines() if l.strip()]

    # 展平所有词级时间戳
    all_words = [w for seg in result['segments'] for w in seg.get('words', [])]

    def fmt_ts(s: float) -> str:
        h, r = divmod(int(s), 3600); m, sec = divmod(r, 60)
        ms = int((s - int(s)) * 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

    srt_lines, word_idx = [], 0
    for i, line in enumerate(lines, 1):
        # 按行长度消耗 all_words，取首词 start 和末词 end
        consumed, chars = [], 0
        while word_idx < len(all_words) and chars < len(line):
            consumed.append(all_words[word_idx])
            chars += len(all_words[word_idx]['word'].strip())
            word_idx += 1
        if not consumed: continue
        start = consumed[0]['start']; end = consumed[-1]['end']
        srt_lines += [str(i), f"{fmt_ts(start)} --> {fmt_ts(end)}", line, '']

    srt_path.write_text('\n'.join(srt_lines), encoding='utf-8')

    subprocess.run(cmd, check=True)
    print(f"✅ 字幕视频: {out_path}")
```

- [ ] **Step 4: 实现 main**

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('draft', type=Path, nargs='?', default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    check_deps(dry_run=args.dry_run)
    seq, name = parse_filename(args.video)
    if args.draft is None:
        stage1_transcribe(args.video, seq, name, args.dry_run)
    else:
        stage2_burn(args.video, args.draft, seq, name, args.dry_run)

if __name__ == '__main__':
    main()
```

- [ ] **Step 5: 验证 `--dry-run`**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills/community/字幕
python3 scripts/subtitle.py 01-test.mp4 --dry-run
# 预期: [DRY-RUN] whisper 01-test.mp4 --model medium --language zh --output_format json
python3 scripts/subtitle.py 01-test.mp4 01-test_字幕稿.txt --dry-run
# 预期: [DRY-RUN] 生成 SRT / FFmpeg 命令
```

- [ ] **Step 6: 更新 SKILL.md**

在 `community/字幕/SKILL.md` 的 `## 流程` 前插入：

```markdown
## ⭐ 脚本优先原则

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 阶段1：转录+生成字幕稿 | `python3 scripts/subtitle.py <video.mp4>` | 手动调用 whisper 命令 |
| 阶段2：匹配时间戳+烧录 | `python3 scripts/subtitle.py <video.mp4> <字幕稿.txt>` | 手动拼 FFmpeg subtitles filter |

⚠️ 约束：阶段2 用户只能修改字幕稿的文字内容，不能调整行顺序，否则时间戳对齐失效。
```

- [ ] **Step 7: 提交**

```bash
git add community/字幕/scripts/subtitle.py community/字幕/SKILL.md
git commit -m "feat(字幕): add subtitle.py two-stage whisper+ffmpeg pipeline"
```

---

## Task 7: download.py（media-downloader）

**Files:**
- Create: `productivity/media-downloader/scripts/download.py`
- Modify: `productivity/media-downloader/SKILL.md`

- [ ] **Step 1: 创建脚本**

```python
#!/usr/bin/env python3
"""
download.py — 视频/音频下载（yt-dlp 最优参数封装）
用法: python3 scripts/download.py <url> [--audio-only] [--quality 720] [--dry-run]
"""
import sys, re, subprocess, argparse

def check_deps():
    missing = []
    if subprocess.run(['yt-dlp', '--version'], capture_output=True).returncode != 0:
        missing.append("yt-dlp  # pip install yt-dlp")
    if subprocess.run(['ffmpeg', '-version'], capture_output=True).returncode != 0:
        missing.append("ffmpeg  # brew install ffmpeg")
    if missing:
        print("❌ 缺少依赖："); [print(f"   {m}") for m in missing]; sys.exit(1)

def detect_platform(url: str) -> str:
    if 'bilibili.com' in url or 'b23.tv' in url: return 'bilibili'
    if 'youtube.com' in url or 'youtu.be' in url: return 'youtube'
    return 'generic'

def build_cmd(url: str, audio_only: bool, quality: int) -> list[str]:
    platform = detect_platform(url)
    cmd = ['yt-dlp']

    if audio_only:
        cmd += ['-f', 'bestaudio/best', '-x', '--audio-format', 'mp3']
    else:
        fmt = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        cmd += ['-f', fmt, '--merge-output-format', 'mp4']

    if platform == 'bilibili':
        cmd += ['--cookies-from-browser', 'chrome']
        if not audio_only and quality >= 1080:
            print("ℹ️  Bilibili 1080p 需要登录 cookie，确保 Chrome 已登录 Bilibili")

    cmd += ['-o', '%(title)s.%(ext)s', url]
    return cmd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--audio-only', action='store_true')
    parser.add_argument('--quality', type=int, default=1080)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    check_deps()
    cmd = build_cmd(args.url, args.audio_only, args.quality)

    if args.dry_run:
        print(f"[DRY-RUN] {' '.join(cmd)}"); return

    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 验证 `--dry-run`**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills/productivity/media-downloader
python3 scripts/download.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --dry-run
# 预期: [DRY-RUN] yt-dlp -f bestvideo[height<=1080]+bestaudio/best ... 
python3 scripts/download.py https://www.bilibili.com/video/BV1xx411c7mD --audio-only --dry-run
# 预期: [DRY-RUN] yt-dlp -f bestaudio/best -x --audio-format mp3 --cookies-from-browser chrome ...
```

- [ ] **Step 3: 更新 SKILL.md**

在 `productivity/media-downloader/SKILL.md` 的 `## 🚀 使用流程` 前插入：

```markdown
## ⭐ 脚本优先原则

| 场景 | 使用脚本 | 禁止行为 |
|------|---------|---------|
| 下载视频 | `python3 scripts/download.py <url>` | 手动拼 yt-dlp 参数 |
| 仅下载音频 | `python3 scripts/download.py <url> --audio-only` | — |
| 指定分辨率 | `python3 scripts/download.py <url> --quality 720` | — |
```

- [ ] **Step 4: 提交**

```bash
git add productivity/media-downloader/scripts/download.py productivity/media-downloader/SKILL.md
git commit -m "feat(media-downloader): add download.py with platform detection"
```

---

## Task 8: commit.sh（git-commit-master，P2 可选）

**Files:**
- Create: `community/git-commit-master/scripts/commit.sh`
- Modify: `community/git-commit-master/SKILL.md`

- [ ] **Step 1: 创建脚本**

```bash
#!/usr/bin/env bash
# commit.sh — Conventional Commits 格式校验 + 执行
# 用法: MESSAGE="feat: add feature" bash scripts/commit.sh [--dry-run]
set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# 1. 检查有无 staged 内容
if ! git diff --cached --name-only | grep -q .; then
  echo "❌ 没有 staged 的内容，请先 git add"; exit 1
fi

# 2. 获取 MESSAGE（环境变量或 stdin）
if [ -z "${MESSAGE:-}" ]; then
  echo "请输入 commit message (Ctrl+D 结束):"
  MESSAGE=$(cat)
fi

# 3. 校验 Conventional Commits 格式
# 格式: type(scope): description  或  type: description
CC_PATTERN='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .+'
if ! echo "$MESSAGE" | grep -qE "$CC_PATTERN"; then
  echo "❌ 不符合 Conventional Commits 格式"
  echo "   期望: type(scope): description"
  echo "   类型: feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert"
  echo "   收到: $MESSAGE"
  exit 1
fi

# 4. 执行（或 dry-run）
if $DRY_RUN; then
  echo "[DRY-RUN] git commit -m \"$MESSAGE\""
else
  git commit -m "$MESSAGE"
  echo "✅ 已提交: $MESSAGE"
fi
```

- [ ] **Step 2: 验证**

```bash
cd ~/Desktop/working/sourcecode/tools/ultraskills
# 测试格式校验
MESSAGE="不符合格式" bash community/git-commit-master/scripts/commit.sh --dry-run
# 预期: ❌ 不符合 Conventional Commits 格式

MESSAGE="feat: add something" bash community/git-commit-master/scripts/commit.sh --dry-run
# 预期: [DRY-RUN] git commit -m "feat: add something"
```

- [ ] **Step 3: 更新 SKILL.md 并提交**

在 `community/git-commit-master/SKILL.md` 的 `## 🚀 使用流程` 前插入：

~~~markdown
## ⭐ 脚本优先原则

Agent 生成 message，脚本负责格式校验和执行：

```bash
MESSAGE="feat(auth): add login flow" bash scripts/commit.sh
# --dry-run 预览不执行：
MESSAGE="feat: test" bash scripts/commit.sh --dry-run
```
~~~

```bash
git add community/git-commit-master/scripts/commit.sh community/git-commit-master/SKILL.md
git commit -m "feat(git-commit-master): add commit.sh with CC format validation"
```

---

## 验证清单（全部完成后执行）

- [ ] `bash scripts/bootstrap.sh --dry-run` — 无报错，打印所有 skill symlink 操作
- [ ] `bash scripts/bootstrap.sh --upgrade --dry-run` — 无报错，打印 git pull + 断链扫描
- [ ] `python3 community/剪口播/scripts/transcribe.py dummy.mp4 --dry-run` — 正确打印
- [ ] `python3 community/剪辑/scripts/cut.py dummy.mp4 dummy_审查稿.md --dry-run` — 正确打印 filter
- [ ] `python3 community/字幕/scripts/subtitle.py dummy.mp4 --dry-run` — 正确打印
- [ ] `python3 productivity/media-downloader/scripts/download.py https://youtu.be/xxx --dry-run` — 正确打印
- [ ] 所有改动 SKILL.md 均包含「脚本优先原则」段落
