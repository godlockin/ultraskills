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
    stem = video_path.stem
    m = re.match(r'^(\d+)-(.+)$', stem)
    if m:
        return m.group(1), m.group(2)
    return '01', stem

def transcribe_video(video_path: Path, dry_run: bool) -> list:
    """分段转录，返回合并后的 tokens 列表（含字符级时间戳）"""
    if dry_run:
        print(f"[DRY-RUN] FunASR 转录: {video_path} (30s 分段)")
        return []
    from funasr import AutoModel

    model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                      vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                      punc_model="ct-punc-c", punc_model_revision="v2.0.0")
    result = model.generate(input=str(video_path),
                            batch_size_s=SEGMENT_DURATION_S,
                            return_raw_text=True)
    tokens = []
    for char, ts in zip(result[0]['text'], result[0]['timestamp']):
        tokens.append({'char': char, 'start': ts[0]/1000, 'end': ts[1]/1000})
    return tokens

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
        transcript_path = out_dir / f"{seq}-{name}_transcript.json"
        transcript_path.write_text(json.dumps(tokens, ensure_ascii=False, indent=2))
        print(f"✅ 转录: {transcript_path}")

        fillers = find_fillers(tokens)
        silences = find_silences(tokens)
        write_review_draft(seq, name, tokens, fillers, silences, out_dir)

if __name__ == '__main__':
    main()
