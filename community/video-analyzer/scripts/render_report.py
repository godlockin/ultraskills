#!/usr/bin/env python3
"""Render REPORT.md from analyzer outputs."""
import argparse, json, os, sys, datetime, subprocess, re

def fmt_ts(s):
    s = float(s)
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"

def video_duration(path):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=10
        )
        return float(r.stdout.strip())
    except Exception:
        return 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--no-chapters", action="store_true")
    args = ap.parse_args()

    out = args.outdir
    name = os.path.basename(args.video)
    dur = video_duration(args.video)

    chapters_path = os.path.join(out, "chapters.json")
    has_chap = (not args.no_chapters) and os.path.isfile(chapters_path)
    chapters = json.load(open(chapters_path)) if has_chap else []

    transcript_txt = ""
    tp = os.path.join(out, "transcript.txt")
    if os.path.isfile(tp):
        transcript_txt = open(tp).read().strip()

    frames_dir = os.path.join(out, "frames")
    n_frames = 0
    if os.path.isdir(frames_dir):
        n_frames = len([f for f in os.listdir(frames_dir)
                        if f.lower().endswith((".jpg",".jpeg",".png",".webp"))])

    print(f"# REPORT — {name}")
    print(f"_generated: {datetime.datetime.now().isoformat(timespec='seconds')}_  ")
    print(f"duration: **{fmt_ts(dur)}** · frames: **{n_frames}** · chapters: **{len(chapters)}**")
    print()
    print(f"- 📝 [transcript.txt](transcript.txt) · [transcript.srt](transcript.srt)")
    print(f"- 🖼  frames/")
    if has_chap:
        print(f"- 📑 [chapters.json](chapters.json)")
    print()

    if has_chap and chapters:
        print("## Chapters")
        print()
        for i, c in enumerate(chapters, 1):
            print(f"### {i}. {c.get('title','(untitled)')} ({fmt_ts(c['start'])}–{fmt_ts(c['end'])})")
            print()
            if c.get("summary"):
                print(c["summary"])
                print()
            for fr in (c.get("frames") or [])[:3]:
                print(f"![](frames/{fr})")
            print()
    else:
        print("## Transcript")
        print()
        # First 80 lines
        print("\n".join(transcript_txt.splitlines()[:80]))
        print()
        if n_frames:
            print("## Sample frames")
            print()
            for f in sorted(os.listdir(frames_dir))[:6]:
                print(f"![](frames/{f})")

if __name__ == "__main__":
    main()
