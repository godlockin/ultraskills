#!/usr/bin/env bash
# video-analyzer — chain whisper + frame-extractor + LLM into a Markdown report
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COMMUNITY_DIR="$(cd "$SKILL_DIR/.." && pwd)"

WHISPER_SH="$COMMUNITY_DIR/mac-whisper/scripts/transcribe.sh"
FRAMES_SH="$COMMUNITY_DIR/video-frame-extractor/scripts/extract.sh"

usage() {
  cat <<EOF
video-analyzer — turn a video into transcript + key frames + chaptered report

Usage:
  analyze.sh <video> [options]

Options:
  -o, --output <dir>          default: <video>_report/
  --lang <code>               whisper language (zh/en/...)
  --whisper-model <id>        default: mlx-community/whisper-large-v3-turbo
  --frame-mode <m>            scene|fps|keyframes|timestamps   (default: scene)
  --fps <n>                   for fps mode (default 1)
  --scene-threshold <f>       0-1 (default 0.3)
  --max-frames <n>            cap frames (default 100)
  --llm <provider>            claude-cli|openai|ollama|none (default claude-cli)
  --llm-model <id>            provider-specific model id
  --no-chapters               skip LLM chapterization
  --keep-audio                keep intermediate audio
  -h, --help
EOF
}

VIDEO=""
OUTDIR=""
LANG=""
WHISPER_MODEL="mlx-community/whisper-large-v3-turbo"
FRAME_MODE="scene"
FPS="1"
SCENE_THRESH="0.3"
MAX_FRAMES="100"
LLM="claude-cli"
LLM_MODEL=""
NO_CHAPTERS=0
KEEP_AUDIO=0

if [ $# -eq 0 ]; then usage; exit 0; fi

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0;;
    -o|--output) OUTDIR="$2"; shift 2;;
    --lang) LANG="$2"; shift 2;;
    --whisper-model) WHISPER_MODEL="$2"; shift 2;;
    --frame-mode) FRAME_MODE="$2"; shift 2;;
    --fps) FPS="$2"; shift 2;;
    --scene-threshold) SCENE_THRESH="$2"; shift 2;;
    --max-frames) MAX_FRAMES="$2"; shift 2;;
    --llm) LLM="$2"; shift 2;;
    --llm-model) LLM_MODEL="$2"; shift 2;;
    --no-chapters) NO_CHAPTERS=1; shift;;
    --keep-audio) KEEP_AUDIO=1; shift;;
    --) shift; break;;
    -*) echo "Unknown opt: $1"; usage; exit 1;;
    *) VIDEO="$1"; shift;;
  esac
done

[ -z "$VIDEO" ] && { echo "ERR: video required"; exit 1; }
[ ! -f "$VIDEO" ] && { echo "ERR: video not found: $VIDEO"; exit 1; }

VIDEO_BASE="$(basename "${VIDEO%.*}")"
[ -z "$OUTDIR" ] && OUTDIR="${VIDEO_BASE}_report"
mkdir -p "$OUTDIR/frames"

echo "==> video-analyzer"
echo "  input : $VIDEO"
echo "  output: $OUTDIR"

# ── 1) Extract audio ────────────────────────────────────────────────────────
AUDIO="$OUTDIR/_audio.wav"
echo ""
echo "[1/4] Extracting audio → $AUDIO"
ffmpeg -y -loglevel error -i "$VIDEO" -ac 1 -ar 16000 -vn "$AUDIO"

# ── 2) Whisper transcription ────────────────────────────────────────────────
echo ""
echo "[2/4] Transcribing (whisper)..."
if [ ! -x "$WHISPER_SH" ]; then
  echo "  WARN: $WHISPER_SH not found/executable. Falling back to direct mlx_whisper."
  python3 -m mlx_whisper "$AUDIO" --model "$WHISPER_MODEL" \
    ${LANG:+--language "$LANG"} \
    --output-dir "$OUTDIR" --output-format all >/dev/null
else
  bash "$WHISPER_SH" "$AUDIO" \
    --model "$WHISPER_MODEL" \
    ${LANG:+--lang "$LANG"} \
    --format all \
    --out "$OUTDIR"
fi

# Normalize output names
[ -f "$OUTDIR/_audio.txt" ] && mv "$OUTDIR/_audio.txt" "$OUTDIR/transcript.txt"
[ -f "$OUTDIR/_audio.srt" ] && mv "$OUTDIR/_audio.srt" "$OUTDIR/transcript.srt"
[ -f "$OUTDIR/_audio.json" ] && mv "$OUTDIR/_audio.json" "$OUTDIR/transcript.json"
[ -f "$OUTDIR/_audio.vtt" ] && mv "$OUTDIR/_audio.vtt" "$OUTDIR/transcript.vtt"

# ── 3) Frame extraction ─────────────────────────────────────────────────────
echo ""
echo "[3/4] Extracting frames (mode=$FRAME_MODE)..."
FRAMES_DIR="$OUTDIR/frames"
if [ -x "$FRAMES_SH" ]; then
  case "$FRAME_MODE" in
    scene)
      bash "$FRAMES_SH" "$VIDEO" --mode scene --threshold "$SCENE_THRESH" \
        --max "$MAX_FRAMES" -o "$FRAMES_DIR" || true;;
    fps)
      bash "$FRAMES_SH" "$VIDEO" --mode fps --fps "$FPS" \
        --max "$MAX_FRAMES" -o "$FRAMES_DIR" || true;;
    keyframes)
      bash "$FRAMES_SH" "$VIDEO" --mode keyframes --max "$MAX_FRAMES" -o "$FRAMES_DIR" || true;;
    *) echo "  WARN: frame mode $FRAME_MODE not auto-handled, skipping";;
  esac
else
  # Fallback: ffmpeg scene-detect direct
  ffmpeg -y -loglevel error -i "$VIDEO" \
    -vf "select='gt(scene,${SCENE_THRESH})',showinfo" \
    -vsync vfr -frames:v "$MAX_FRAMES" \
    "$FRAMES_DIR/frame_%04d.jpg"
fi

FRAME_COUNT=$(/bin/ls "$FRAMES_DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "  ✓ $FRAME_COUNT frames"

# ── 4) Chapterize via LLM ──────────────────────────────────────────────────
if [ "$NO_CHAPTERS" = "1" ]; then
  echo ""
  echo "[4/4] Skipping LLM chapterization (--no-chapters)"
else
  echo ""
  echo "[4/4] LLM chapterization ($LLM)..."
  python3 "$SCRIPT_DIR/chapterize.py" \
    --transcript "$OUTDIR/transcript.json" \
    --frames-dir "$FRAMES_DIR" \
    --output "$OUTDIR/chapters.json" \
    --llm "$LLM" \
    ${LLM_MODEL:+--llm-model "$LLM_MODEL"} \
    || { echo "  WARN: chapterize failed, skipping"; NO_CHAPTERS=1; }
fi

# ── Render REPORT.md ───────────────────────────────────────────────────────
echo ""
echo "Rendering REPORT.md..."
python3 "$SCRIPT_DIR/render_report.py" \
  --video "$VIDEO" \
  --outdir "$OUTDIR" \
  ${NO_CHAPTERS:+--no-chapters} \
  > "$OUTDIR/REPORT.md"

# Cleanup
[ "$KEEP_AUDIO" = "0" ] && rm -f "$AUDIO"

echo ""
echo "✓ Done. Report at: $OUTDIR/REPORT.md"
