#!/usr/bin/env python3
"""srt_to_segments.py — SRT subtitle file → JSON segments."""
import sys, json, re

def parse_ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000.0

def main():
    in_srt, out_json = sys.argv[1], sys.argv[2]
    text = open(in_srt).read()
    blocks = re.split(r"\n\n+", text.strip())
    segs = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3: continue
        ts_line = lines[1]
        m = re.match(r"(\S+)\s*-->\s*(\S+)", ts_line)
        if not m: continue
        start, end = parse_ts(m.group(1)), parse_ts(m.group(2))
        text_lines = "\n".join(lines[2:]).strip()
        segs.append({"start": start, "end": end, "text": text_lines})
    json.dump({"segments": segs}, open(out_json, "w"), ensure_ascii=False, indent=2)
    print(f"✓ {len(segs)} segments → {out_json}")

if __name__ == "__main__":
    main()
