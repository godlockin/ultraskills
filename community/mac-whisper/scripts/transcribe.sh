#!/usr/bin/env bash
# mac-whisper :: transcribe.sh
# Usage: transcribe.sh <audio_or_video> [options]
#   --lang LANG              Force language (zh, en, ja, ...). Default: auto-detect.
#   --format FMT             txt | srt | vtt | json | all. Default: txt.
#   --model REPO             HF repo id. mlx default: mlx-community/whisper-large-v3-turbo
#                            faster-whisper default: Systran/faster-whisper-large-v3
#   --out DIR                Output directory. Default: same dir as input.
#   --prompt TEXT            Initial prompt (punctuation/style/jargon).
#   --backend NAME           Force backend: mlx | faster | cpp. Default: auto-detect.
#   --compute-type TYPE      faster-whisper only: int8 | int8_float16 | float16 | float32.
#                            int8 = best speed/quality on CPU (default).
#                            float16 = GPU/MPS.
#   -h, --help               Show this message.
set -euo pipefail

INPUT=""
LANG=""
FORMAT="txt"
MODEL=""
OUTDIR=""
PROMPT=""
BACKEND_FORCE=""
COMPUTE_TYPE=""

usage() {
  cat <<EOF
Usage: $(basename "$0") <audio_or_video> [options]

Options:
  --lang LANG         Force language (zh, en, ja, ...). Default: auto-detect.
  --format FMT        txt | srt | vtt | json | all. Default: txt.
  --model REPO        HF repo id. Default depends on backend:
                        mlx   → mlx-community/whisper-large-v3-turbo
                        faster→ Systran/faster-whisper-large-v3
  --backend NAME      mlx | faster | cpp. Default: auto (mlx → faster → cpp).
  --compute-type TYPE faster-whisper only: int8 (CPU) | float16 (GPU/MPS) | float32.
                      Default: int8.
  --out DIR           Output directory. Default: same dir as input.
  --prompt TEXT       Initial prompt (punctuation/style/jargon).
  -h, --help          Show this message.

Examples:
  # Auto-detect everything (typical use)
  $(basename "$0") audio.mp3

  # Force faster-whisper on Apple Silicon GPU with float16
  $(basename "$0") audio.mp3 --backend faster --compute-type float16

  # Use a smaller model for quick drafts
  $(basename "$0") audio.mp3 --model Systran/faster-whisper-small

  # Force whisper.cpp (low-RAM / offline)
  $(basename "$0") audio.mp3 --backend cpp --lang zh --format srt
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)          LANG="$2"; shift 2 ;;
    --format)        FORMAT="$2"; shift 2 ;;
    --model)         MODEL="$2"; shift 2 ;;
    --backend)       BACKEND_FORCE="$2"; shift 2 ;;
    --compute-type)  COMPUTE_TYPE="$2"; shift 2 ;;
    --out)           OUTDIR="$2"; shift 2 ;;
    --prompt)        PROMPT="$2"; shift 2 ;;
    -h|--help)       usage; exit 0 ;;
    -*)              echo "Unknown flag: $1" >&2; usage; exit 2 ;;
    *)               INPUT="$1"; shift ;;
  esac
done

[[ -z "$INPUT" ]] && { usage; exit 2; }
[[ ! -f "$INPUT" ]] && { echo "❌ File not found: $INPUT" >&2; exit 1; }

# Detect Apple Silicon
if [[ "$(uname -s)" != "Darwin" ]] || [[ "$(uname -m)" != "arm64" ]]; then
  echo "⚠️  This skill is optimized for Apple Silicon. Detected: $(uname -sm)" >&2
fi

# Pick backend — auto-fallback chain: mlx → faster-whisper → whisper.cpp
ARCH="$(uname -m)"
PY_ARCH="$(python3 -c 'import platform; print(platform.machine())' 2>/dev/null || echo "$ARCH")"

pick_backend() {
  # mlx-whisper requires native arm64 Python (NOT Rosetta x86_64)
  if [[ "$ARCH" == "arm64" && "$PY_ARCH" == "arm64" ]] && command -v mlx_whisper >/dev/null 2>&1; then
    echo "mlx"; return
  fi
  if python3 -c "import faster_whisper" 2>/dev/null; then
    echo "faster"; return
  fi
  if command -v whisper-cli >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1; then
    echo "cpp"; return
  fi
  echo ""
}

BACKEND=""
if [[ -n "$BACKEND_FORCE" ]]; then
  # Validate that the forced backend is actually usable
  case "$BACKEND_FORCE" in
    mlx)
      if [[ "$ARCH" != "arm64" || "$PY_ARCH" != "arm64" ]]; then
        echo "❌ --backend mlx requires native arm64 Python (you have: $PY_ARCH)." >&2
        exit 1
      fi
      if ! command -v mlx_whisper >/dev/null 2>&1; then
        echo "❌ --backend mlx requested but mlx_whisper not installed. Run install.sh." >&2
        exit 1
      fi
      BACKEND="mlx"
      ;;
    faster)
      if ! python3 -c "import faster_whisper" 2>/dev/null; then
        echo "❌ --backend faster requested but faster_whisper not installed. Run install.sh." >&2
        exit 1
      fi
      BACKEND="faster"
      ;;
    cpp)
      if ! command -v whisper-cli >/dev/null 2>&1 && ! command -v whisper-cpp >/dev/null 2>&1; then
        echo "❌ --backend cpp requested but whisper-cli/whisper-cpp not installed." >&2
        exit 1
      fi
      BACKEND="cpp"
      ;;
    *)
      echo "❌ Unknown backend: $BACKEND_FORCE (expected: mlx | faster | cpp)" >&2
      exit 2
      ;;
  esac
else
  BACKEND="$(pick_backend)"
  if [[ -z "$BACKEND" ]]; then
    echo "❌ No whisper backend installed."
    echo "   Run: bash $(dirname "$0")/install.sh"
    exit 1
  fi
  if [[ "$BACKEND" != "mlx" && ( "$ARCH" == "arm64" || "$PY_ARCH" == "arm64" ) ]]; then
    echo "ℹ️  mlx-whisper not available (needs native arm64 Python + pip install mlx-whisper)."
    echo "   Falling back to: $BACKEND"
  fi
fi

# Default model per backend
if [[ -z "$MODEL" ]]; then
  case "$BACKEND" in
    mlx)    MODEL="mlx-community/whisper-large-v3-turbo" ;;
    faster) MODEL="Systran/faster-whisper-large-v3"     ;;
    cpp)    MODEL="" ;;  # cpp uses ggml file path, not HF repo
  esac
fi

# Resolve output dir
if [[ -z "$OUTDIR" ]]; then
  OUTDIR="$(dirname "$INPUT")"
fi
mkdir -p "$OUTDIR"

BASENAME="$(basename "${INPUT%.*}")"

echo "🎙  Backend : $BACKEND"
echo "📦 Model   : $MODEL"
echo "🌐 Lang    : ${LANG:-auto}"
echo "💾 Out dir : $OUTDIR"
echo "📝 Format  : $FORMAT"
echo

if [[ "$BACKEND" == "mlx" ]]; then
  ARGS=(--model "$MODEL" --output-dir "$OUTDIR")

  # mlx_whisper output format mapping
  case "$FORMAT" in
    txt|srt|vtt|json) ARGS+=(--output-format "$FORMAT") ;;
    all)              ARGS+=(--output-format all) ;;
    *) echo "❌ Unsupported format: $FORMAT" >&2; exit 2 ;;
  esac

  [[ -n "$LANG"   ]] && ARGS+=(--language "$LANG")
  [[ -n "$PROMPT" ]] && ARGS+=(--initial-prompt "$PROMPT")

  ARGS+=("$INPUT")
  echo "→ mlx_whisper ${ARGS[*]}"
  exec mlx_whisper "${ARGS[@]}"
fi

# faster-whisper fallback (works on x86_64 / arm64 / Linux / macOS)
if [[ "$BACKEND" == "faster" ]]; then
  # Use --model / --compute-type from CLI; env vars FW_MODEL/FW_COMPUTE still work as override
  FW_MODEL="${FW_MODEL:-$MODEL}"
  FW_COMPUTE="${COMPUTE_TYPE:-${FW_COMPUTE:-int8}}"
  case "$FORMAT" in
    txt)  FW_OUT="txt"  ;;
    srt)  FW_OUT="srt"  ;;
    vtt)  FW_OUT="vtt"  ;;
    json) FW_OUT="json" ;;
    all)  FW_OUT="all"  ;;
    *) echo "❌ Unsupported format: $FORMAT" >&2; exit 2 ;;
  esac

  # Pass lang/prompt via env so the heredoc Python can read them safely
  export FW_LANG="$LANG"
  export FW_PROMPT="$PROMPT"

  # OMP duplicate lib workaround (common on conda + faster-whisper)
  export KMP_DUPLICATE_LIB_OK="${KMP_DUPLICATE_LIB_OK:-TRUE}"

  python3 - "$INPUT" "$OUTDIR" "$FW_MODEL" "$FW_COMPUTE" "$FW_OUT" <<'PYEOF'
import os, sys
from faster_whisper import WhisperModel
audio, out_dir, model_id, compute_type, fmt = sys.argv[1:6]
m = WhisperModel(model_id, device="auto", compute_type=compute_type)
kwargs = dict(beam_size=5, vad_filter=True,
              vad_parameters={"min_silence_duration_ms": 500},
              condition_on_previous_text=True)
if os.environ.get("FW_LANG"):
    kwargs["language"] = os.environ["FW_LANG"]
if os.environ.get("FW_PROMPT"):
    kwargs["initial_prompt"] = os.environ["FW_PROMPT"]
segs, info = m.transcribe(audio, **kwargs)
segs = list(segs)
print(f"🌐 Detected: {info.language} (prob={info.language_probability:.2f})", file=sys.stderr)
print(f"⏱  Duration: {info.duration:.1f}s  |  segments: {len(segs)}", file=sys.stderr)

def srt_ts(t):
    h, rem = divmod(int(t), 3600); m, s = divmod(rem, 60); ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

stem = os.path.splitext(os.path.basename(audio))[0]
def want(ext): return fmt in (ext, "all")

if want("txt"):
    p = os.path.join(out_dir, f"{stem}.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"# {stem}\n# language: {info.language} (prob={info.language_probability:.2f})\n# duration: {info.duration:.1f}s\n\n")
        for s in segs:
            f.write(f"[{s.start:07.2f} → {s.end:07.2f}] {s.text.strip()}\n")
    print(f"✅ {p}")
if want("srt"):
    p = os.path.join(out_dir, f"{stem}.srt")
    with open(p, "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{srt_ts(s.start)} --> {srt_ts(s.end)}\n{s.text.strip()}\n\n")
    print(f"✅ {p}")
if want("vtt"):
    p = os.path.join(out_dir, f"{stem}.vtt")
    with open(p, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{srt_ts(s.start).replace(',','.')} --> {srt_ts(s.end).replace(',','.')}\n{s.text.strip()}\n\n")
    print(f"✅ {p}")
if want("json"):
    import json
    p = os.path.join(out_dir, f"{stem}.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump({
            "language": info.language, "language_probability": info.language_probability,
            "duration": info.duration,
            "segments": [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs],
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ {p}")
PYEOF
  exit $?
fi

# whisper.cpp fallback
if [[ "$BACKEND" == "cpp" ]]; then
  CMD="whisper-cli"
  command -v whisper-cli >/dev/null 2>&1 || CMD="whisper-cpp"

  # whisper.cpp wants ggml model file path; user must download separately.
  GGML_MODEL="${WHISPER_CPP_MODEL:-$HOME/.cache/whisper.cpp/ggml-large-v3-turbo-q5_0.bin}"
  if [[ ! -f "$GGML_MODEL" ]]; then
    echo "❌ whisper.cpp ggml model not found at: $GGML_MODEL"
    echo "   Set WHISPER_CPP_MODEL=/path/to/ggml-*.bin or run install.sh"
    exit 1
  fi

  # whisper.cpp needs WAV 16k mono input
  TMP_WAV="$(mktemp -t whisper-XXXXXX).wav"
  trap 'rm -f "$TMP_WAV"' EXIT
  echo "→ ffmpeg -> 16kHz mono WAV"
  ffmpeg -y -loglevel error -i "$INPUT" -ar 16000 -ac 1 -c:a pcm_s16le "$TMP_WAV"

  CARGS=(-m "$GGML_MODEL" -f "$TMP_WAV" -of "$OUTDIR/$BASENAME")
  [[ -n "$LANG"   ]] && CARGS+=(-l "$LANG")
  [[ -n "$PROMPT" ]] && CARGS+=(--prompt "$PROMPT")
  case "$FORMAT" in
    txt)  CARGS+=(-otxt) ;;
    srt)  CARGS+=(-osrt) ;;
    vtt)  CARGS+=(-ovtt) ;;
    json) CARGS+=(-oj)   ;;
    all)  CARGS+=(-otxt -osrt -ovtt -oj) ;;
  esac
  echo "→ $CMD ${CARGS[*]}"
  exec "$CMD" "${CARGS[@]}"
fi
