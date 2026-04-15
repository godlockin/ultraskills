#!/usr/bin/env python3
"""
download.py — 视频/音频下载（yt-dlp 最优参数封装）
用法: python3 scripts/download.py <url> [--audio-only] [--quality 720] [--dry-run]
"""
import sys, subprocess, argparse, shutil

def check_deps():
    missing = []
    if shutil.which('yt-dlp') is None:
        missing.append("yt-dlp  # pip install yt-dlp")
    if shutil.which('ffmpeg') is None:
        missing.append("ffmpeg  # brew install ffmpeg")
    if missing:
        print("❌ 缺少依赖："); [print(f"   {m}") for m in missing]; sys.exit(1)

def detect_platform(url: str) -> str:
    if 'bilibili.com' in url or 'b23.tv' in url: return 'bilibili'
    if 'youtube.com' in url or 'youtu.be' in url: return 'youtube'
    return 'generic'

def build_cmd(url: str, audio_only: bool, quality: int) -> list:
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

    cmd = build_cmd(args.url, args.audio_only, args.quality)

    if args.dry_run:
        print(f"[DRY-RUN] {' '.join(cmd)}"); return

    check_deps()
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()
