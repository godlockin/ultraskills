#!/usr/bin/env python3
"""segments_to_srt.py — JSON segments → SRT subtitle file."""
import sys, json

def fmt_ts(s):
    h = int(s // 3600); s -= h*3600
    m = int(s // 60); s -= m*60
    sec = int(s); ms = int((s - sec) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def main():
    in_json, out_srt = sys.argv[1], sys.argv[2]
    data = json.load(open(in_json))
    segs = data.get("segments", data) if isinstance(data, dict) else data
    with open(out_srt, "w") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{fmt_ts(s['start'])} --> {fmt_ts(s['end'])}\n{s['text'].strip()}\n\n")
    print(f"✓ srt → {out_srt} ({len(segs)} cues)")

if __name__ == "__main__":
    main()
