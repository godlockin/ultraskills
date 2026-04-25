#!/usr/bin/env bash
# mac-whisper :: transcribe.sh
# Usage: transcribe.sh <audio_or_video> [--lang LANG] [--format txt|srt|vtt|json|all]
#                                       [--model HF_REPO] [--out DIR] [--prompt TEXT]
set -euo pipefail

INPUT=""
LANG=""
FORMAT="txt"
MODEL="mlx-community/whisper-large-v3-turbo"
OUTDIR=""
PROMPT=""

usage() {
  cat <<EOF
Usage: $(basename "$0") <audio_or_video> [options]

Options:
  --lang LANG       Force language (zh, en, ja, ...). Default: auto-detect.
  --format FMT      txt | srt | vtt | json | all. Default: txt.
  --model REPO      HF repo id. Default: $MODEL
  --out DIR         Output directory. Default: same dir as input.
  --prompt TEXT     Initial prompt (helpful for punctuation/style/jargon).
  -h, --help        Show this message.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)   LANG="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --model)  MODEL="$2"; shift 2 ;;
    --out)    OUTDIR="$2"; shift 2 ;;
    --prompt) PROMPT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*)       echo "Unknown flag: $1" >&2; usage; exit 2 ;;
    *)        INPUT="$1"; shift ;;
  esac
done

[[ -z "$INPUT" ]] && { usage; exit 2; }
[[ ! -f "$INPUT" ]] && { echo "❌ File not found: $INPUT" >&2; exit 1; }

# Detect Apple Silicon
if [[ "$(uname -s)" != "Darwin" ]] || [[ "$(uname -m)" != "arm64" ]]; then
  echo "⚠️  This skill is optimized for Apple Silicon. Detected: $(uname -sm)" >&2
fi

# Pick backend
BACKEND=""
if command -v mlx_whisper >/dev/null 2>&1; then
  BACKEND="mlx"
elif command -v whisper-cli >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1; then
  BACKEND="cpp"
else
  echo "❌ Neither mlx-whisper nor whisper.cpp installed."
  echo "   Run: bash $(dirname "$0")/install.sh"
  exit 1
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
