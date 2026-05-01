#!/usr/bin/env python3
"""extract_ref_text.py — find transcript text overlapping the given clip range."""
import sys, json, re

def parse_clip(s):
    """e.g. '0:00-0:10' or '00:01:30-00:02:00' → (start_sec, end_sec)"""
    a, b = s.split("-")
    def to_sec(t):
        parts = list(map(int, t.split(":")))
        if len(parts) == 2: return parts[0]*60 + parts[1]
        if len(parts) == 3: return parts[0]*3600 + parts[1]*60 + parts[2]
        return float(t)
    return to_sec(a), to_sec(b)

def main():
    seg_json, clip = sys.argv[1], sys.argv[2]
    s, e = parse_clip(clip)
    data = json.load(open(seg_json))
    segs = data.get("segments", data) if isinstance(data, dict) else data
    text = " ".join(seg["text"].strip() for seg in segs if seg["start"] < e and seg["end"] > s)
    print(text)

if __name__ == "__main__":
    main()
