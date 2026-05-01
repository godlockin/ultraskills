#!/usr/bin/env python3
"""translate_segments.py — translate whisper JSON segments via LLM."""
import sys, json, argparse, subprocess, re, os

def claude_translate(segments, target):
    text = "\n".join(f"[{i+1}] {s['text']}" for i, s in enumerate(segments))
    prompt = (
        f"Translate the following segments to {target}. "
        "Return STRICT JSON array: [{\"id\":1,\"text\":\"...\"}, ...]. "
        "Preserve numbering. Keep each translation roughly the same speaking duration. "
        "No markdown, no commentary.\n\n" + text
    )
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=120, check=True)
        out = r.stdout
    except FileNotFoundError:
        sys.exit("ERR: `claude` CLI not found. Install Claude CLI or use --llm openai/ollama.")
    return parse_json_array(out)

def openai_translate(segments, target):
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("ERR: pip install openai")
    client = OpenAI()
    text = "\n".join(f"[{i+1}] {s['text']}" for i, s in enumerate(segments))
    r = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You translate subtitle segments. Return strict JSON array only."},
            {"role": "user", "content":
                f"Translate to {target}. Return [{{\"id\":1,\"text\":\"...\"}}, ...]. Keep numbering.\n\n{text}"},
        ],
        temperature=0.2,
    )
    return parse_json_array(r.choices[0].message.content)

def ollama_translate(segments, target):
    text = "\n".join(f"[{i+1}] {s['text']}" for i, s in enumerate(segments))
    prompt = (f"Translate to {target}. Return JSON array [{{\"id\":1,\"text\":\"...\"}}]. "
              f"No commentary.\n\n{text}")
    r = subprocess.run(
        ["ollama", "run", os.environ.get("OLLAMA_MODEL", "qwen2.5:7b"), prompt],
        capture_output=True, text=True, check=True
    )
    return parse_json_array(r.stdout)

def parse_json_array(s):
    # Find first [...] block
    m = re.search(r"\[\s*\{.*?\}\s*\]", s, re.S)
    if not m:
        sys.exit("ERR: LLM returned non-JSON output:\n" + s[:500])
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        sys.exit(f"ERR: invalid JSON: {e}\n{m.group(0)[:500]}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--target", required=True)
    ap.add_argument("--llm", default="claude-cli")
    args = ap.parse_args()

    data = json.load(open(args.input))
    # mac-whisper JSON format: {"segments": [{"start","end","text"}, ...]} OR list
    segments = data.get("segments", data) if isinstance(data, dict) else data

    fn = {"claude-cli": claude_translate, "openai": openai_translate, "ollama": ollama_translate}.get(args.llm)
    if not fn: sys.exit(f"unknown llm: {args.llm}")

    # Chunk if too many segments to fit in one prompt
    CHUNK = 50
    translated = []
    for i in range(0, len(segments), CHUNK):
        batch = segments[i:i+CHUNK]
        out = fn(batch, args.target)
        # Map by id back to start/end
        by_id = {x["id"]: x["text"] for x in out}
        for j, seg in enumerate(batch):
            text_t = by_id.get(j+1, seg["text"])
            translated.append({"start": seg["start"], "end": seg["end"], "text": text_t})

    json.dump({"segments": translated}, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(f"✓ translated {len(translated)} segments → {args.output}")

if __name__ == "__main__":
    main()
