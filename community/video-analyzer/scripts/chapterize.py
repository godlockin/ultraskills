#!/usr/bin/env python3
"""
chapterize.py — turn whisper segments into chapters via LLM.

Inputs:
  --transcript <whisper.json>   whisper output with "segments" [{start, end, text}]
  --frames-dir <dir>            dir of frames named like 00_01_23_456.jpg
  --output <chapters.json>      output
  --llm <claude-cli|openai|ollama|none>
  --llm-model <id>              optional override

Output schema:
[
  {"start": 0.0, "end": 201.3, "title": "Intro", "summary": "...", "frames": ["00_00_05_000.jpg"]},
  ...
]
"""
import argparse, json, os, subprocess, sys, re

def load_segments(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict) and "segments" in data:
        return data["segments"]
    if isinstance(data, list):
        return data
    return []

def parse_frame_ts(name):
    # e.g. 00_01_23_456.jpg → 83.456
    m = re.match(r"(\d+)_(\d+)_(\d+)_(\d+)", name)
    if not m: return None
    h, mi, s, ms = map(int, m.groups())
    return h*3600 + mi*60 + s + ms/1000.0

def list_frames(frames_dir):
    out = []
    if not os.path.isdir(frames_dir): return out
    for f in sorted(os.listdir(frames_dir)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        ts = parse_frame_ts(f)
        out.append({"file": f, "ts": ts if ts is not None else 0.0})
    return out

def build_prompt(segments, frames):
    lines = [
        "You split a transcript into 4-12 logical chapters. Output ONLY valid JSON.",
        "Schema: [{\"start\": float_seconds, \"end\": float_seconds, \"title\": str, \"summary\": str (1-3 sentences)}]",
        "",
        "TRANSCRIPT (start_sec | text):",
    ]
    for s in segments:
        t = s.get("text", "").strip().replace("\n", " ")
        lines.append(f"{s.get('start', 0):.1f} | {t}")
    lines.append("")
    lines.append(f"Frame timestamps available: {[round(f['ts'],1) for f in frames[:30]]}{'...' if len(frames)>30 else ''}")
    lines.append("")
    lines.append("Return JSON array only, no markdown, no commentary.")
    return "\n".join(lines)

def run_claude_cli(prompt, model=None):
    cmd = ["claude", "-p", prompt]
    if model: cmd += ["--model", model]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"claude cli: {r.stderr}")
    return r.stdout

def run_openai(prompt, model=None):
    import openai
    client = openai.OpenAI()
    resp = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content

def run_ollama(prompt, model=None):
    cmd = ["ollama", "run", model or "qwen2.5:14b"]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=600)
    if r.returncode != 0: raise RuntimeError(f"ollama: {r.stderr}")
    return r.stdout

def extract_json(text):
    # find first '[' .. last ']'
    s = text.find("[")
    e = text.rfind("]")
    if s < 0 or e < 0: raise ValueError("no JSON array in LLM output")
    return json.loads(text[s:e+1])

def assign_frames(chapters, frames):
    for c in chapters:
        c["frames"] = [f["file"] for f in frames if c["start"] <= f["ts"] <= c["end"]]
    return chapters

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--frames-dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--llm", default="claude-cli")
    ap.add_argument("--llm-model", default=None)
    args = ap.parse_args()

    segments = load_segments(args.transcript)
    frames = list_frames(args.frames_dir)
    if not segments:
        print("WARN: no segments, writing empty chapters", file=sys.stderr)
        json.dump([], open(args.output, "w"))
        return

    if args.llm == "none":
        # Heuristic fallback: 1 chapter per ~5 minutes
        chapters = []
        chunk = 300.0
        cur_start = segments[0]["start"]
        cur_text = []
        for s in segments:
            cur_text.append(s["text"])
            if s["end"] - cur_start >= chunk:
                chapters.append({"start": cur_start, "end": s["end"],
                                 "title": f"Chapter {len(chapters)+1}",
                                 "summary": " ".join(cur_text)[:200]})
                cur_start = s["end"]; cur_text = []
        if cur_text:
            chapters.append({"start": cur_start, "end": segments[-1]["end"],
                             "title": f"Chapter {len(chapters)+1}",
                             "summary": " ".join(cur_text)[:200]})
        chapters = assign_frames(chapters, frames)
        json.dump(chapters, open(args.output, "w"), ensure_ascii=False, indent=2)
        return

    prompt = build_prompt(segments, frames)
    runners = {"claude-cli": run_claude_cli, "openai": run_openai, "ollama": run_ollama}
    runner = runners.get(args.llm)
    if not runner:
        print(f"ERR: unknown --llm {args.llm}", file=sys.stderr); sys.exit(1)

    out = runner(prompt, args.llm_model)
    chapters = extract_json(out)
    chapters = assign_frames(chapters, frames)
    json.dump(chapters, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(f"  ✓ {len(chapters)} chapters → {args.output}")

if __name__ == "__main__":
    main()
