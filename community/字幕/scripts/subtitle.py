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

def load_dict(dict_path: Path) -> list:
    """读取词典.txt，每行一个正确写法"""
    if not dict_path.exists():
        return []
    return [l.strip() for l in dict_path.read_text(encoding='utf-8').splitlines() if l.strip()]

def apply_dict(text: str, words: list) -> str:
    """词典纠错：大小写不敏感替换"""
    for w in words:
        text = re.sub(re.escape(w), w, text, flags=re.IGNORECASE)
    return text

def parse_filename(video_path: Path):
    stem = video_path.stem
    m = re.match(r'^(\d+)-(.+)$', stem)
    return (m.group(1), m.group(2)) if m else ('01', stem)

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
