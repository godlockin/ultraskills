#!/usr/bin/env python3
"""synth_dub.py — synthesize per-segment audio and concat with timing alignment.

Strategy: render each segment via mac-tts or mac-voice-clone, then align by
inserting silence to match the original timing window. If the synthesized clip
is longer than the window, apply ffmpeg atempo (pitch-preserving speedup).
"""
import sys, json, argparse, subprocess, os, tempfile, shutil, wave, math

COMMUNITY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TTS_SH = os.path.join(COMMUNITY, "mac-tts", "scripts", "tts.sh")
CLONE_SH = os.path.join(COMMUNITY, "mac-voice-clone", "scripts", "clone.sh")

def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / float(w.getframerate())

def render_segment_tts(text, out, voice=""):
    args = ["bash", TTS_SH, text, "-o", out]
    if voice:
        args += ["--voice", voice]
    subprocess.run(args, check=True, capture_output=True)

def render_segment_clone(text, out, ref_audio, ref_text):
    args = ["bash", CLONE_SH, "--ref-audio", ref_audio, "--ref-text", ref_text,
            "--text", text, "-o", out, "--device", "auto"]
    subprocess.run(args, check=True, capture_output=True)

def fit_to_window(in_wav, out_wav, target_dur):
    """Speed up if longer than target. Pad with silence at end if shorter."""
    cur = wav_duration(in_wav)
    if abs(cur - target_dur) / max(target_dur, 0.001) < 0.05:
        shutil.copy(in_wav, out_wav); return
    if cur > target_dur:
        # speed up. atempo accepts 0.5..2.0; chain if needed.
        ratio = cur / target_dur
        ratio = min(ratio, 2.0)  # don't exceed 2x to avoid chipmunk
        subprocess.run(["ffmpeg", "-y", "-i", in_wav, "-filter:a",
                        f"atempo={ratio:.3f}", out_wav],
                       check=True, capture_output=True)
    else:
        # pad
        pad = target_dur - cur
        subprocess.run(["ffmpeg", "-y", "-i", in_wav, "-af",
                        f"apad=pad_dur={pad:.3f}", out_wav],
                       check=True, capture_output=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--voice", default="")
    ap.add_argument("--backend", choices=["tts", "clone"], default="tts")
    ap.add_argument("--ref-audio", default="")
    ap.add_argument("--ref-text", default="")
    args = ap.parse_args()

    data = json.load(open(args.input))
    segs = data.get("segments", data) if isinstance(data, dict) else data
    if not segs: sys.exit("no segments")

    workdir = tempfile.mkdtemp(prefix="vdub.")
    concat_list = os.path.join(workdir, "list.txt")

    total_end = segs[-1]["end"]
    rendered = []
    prev_end = 0.0
    for i, s in enumerate(segs):
        start, end, text = s["start"], s["end"], s["text"].strip()
        if not text: continue
        target = end - start
        # leading silence to fill gap from prev segment
        gap = max(start - prev_end, 0)
        raw = os.path.join(workdir, f"seg_{i:04d}_raw.wav")
        fit = os.path.join(workdir, f"seg_{i:04d}_fit.wav")
        try:
            if args.backend == "tts":
                render_segment_tts(text, raw, args.voice)
            else:
                render_segment_clone(text, raw, args.ref_audio, args.ref_text)
            fit_to_window(raw, fit, target)
        except subprocess.CalledProcessError as e:
            print(f"  ! seg {i} render failed, inserting silence: {e}", file=sys.stderr)
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                            f"anullsrc=r=24000:cl=mono", "-t", str(target), fit],
                           check=True, capture_output=True)
        if gap > 0.05:
            sil = os.path.join(workdir, f"seg_{i:04d}_gap.wav")
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                            f"anullsrc=r=24000:cl=mono", "-t", str(gap), sil],
                           check=True, capture_output=True)
            rendered.append(sil)
        rendered.append(fit)
        prev_end = end

    # concat — re-encode to ensure uniform format
    with open(concat_list, "w") as f:
        for r in rendered:
            f.write(f"file '{r}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", concat_list, "-ar", "24000", "-ac", "1", args.output],
                   check=True, capture_output=True)
    print(f"✓ dub → {args.output} ({len(rendered)} clips, {total_end:.1f}s target)")

if __name__ == "__main__":
    main()
