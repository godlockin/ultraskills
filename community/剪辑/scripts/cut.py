#!/usr/bin/env python3
"""
cut.py — 解析审查稿，生成 FFmpeg filter.txt 并执行剪辑
用法: python3 scripts/cut.py <video.mp4> <审查稿.md> [--dry-run]
"""
import sys, re, argparse, subprocess
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

def parse_review_draft(draft_path: Path) -> list:
    """解析审查稿中 [x] 勾选的时间段，返回 [(start, end), ...] 删除列表"""
    deletes = []
    pattern = re.compile(r'- \[x\].*?`\((\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\)`')
    for line in draft_path.read_text(encoding='utf-8').splitlines():
        m = pattern.search(line)
        if m:
            deletes.append((float(m.group(1)), float(m.group(2))))
    return sorted(deletes)

def compute_keep_segments(deletes: list, duration: float) -> list:
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
