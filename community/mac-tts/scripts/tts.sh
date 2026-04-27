#!/usr/bin/env bash
# mac-tts — local Mac TTS dispatcher
# Backends: edge-tts (default, free MS neural) > kokoro-tts (offline) > say (fallback)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<EOF
mac-tts — text-to-speech dispatcher

Usage:
  tts.sh <text|file|-> [options]

Options:
  --backend <edge|kokoro|say>   default: edge
  --voice <id>                  voice id (backend-specific)
  --rate <±N%>                  edge-tts only, e.g. +20%
  --pitch <±NHz>                edge-tts only, e.g. +50Hz
  --volume <±N%>                edge-tts only
  --lang <zh|en|ja|ko|...>      hint to auto-pick default voice
  -o, --output <path>           output file (.mp3/.wav/.aiff). default: out.mp3
  --list-voices                 list edge-tts voices and exit
  -h, --help                    show this help

Examples:
  tts.sh "你好世界" -o hello.mp3
  tts.sh article.txt --voice zh-CN-YunxiNeural -o art.mp3
  cat note.md | tts.sh - --backend kokoro -o note.wav
  tts.sh "fallback test" --backend say -o out.aiff
EOF
}

BACKEND="edge"
VOICE=""
RATE=""
PITCH=""
VOLUME=""
LANG_HINT=""
OUTPUT="out.mp3"
INPUT=""

if [ $# -eq 0 ]; then usage; exit 0; fi

# First positional: text / file / -
case "${1:-}" in
  -h|--help) usage; exit 0;;
  --list-voices)
    command -v edge-tts >/dev/null || { echo "edge-tts not installed. run install.sh"; exit 1; }
    edge-tts --list-voices
    exit 0;;
  --*) ;;
  *) INPUT="$1"; shift;;
esac

while [ $# -gt 0 ]; do
  case "$1" in
    --backend) BACKEND="$2"; shift 2;;
    --voice) VOICE="$2"; shift 2;;
    --rate) RATE="$2"; shift 2;;
    --pitch) PITCH="$2"; shift 2;;
    --volume) VOLUME="$2"; shift 2;;
    --lang) LANG_HINT="$2"; shift 2;;
    -o|--output) OUTPUT="$2"; shift 2;;
    --list-voices)
      edge-tts --list-voices; exit 0;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

# Resolve input → TEXT
if [ -z "$INPUT" ]; then
  echo "ERR: no input text"; exit 1
fi
if [ "$INPUT" = "-" ]; then
  TEXT="$(cat)"
elif [ -f "$INPUT" ]; then
  TEXT="$(cat "$INPUT")"
else
  TEXT="$INPUT"
fi

if [ -z "${TEXT// /}" ]; then
  echo "ERR: empty text"; exit 1
fi

# Auto-detect language for default voice
detect_lang() {
  if [[ "$TEXT" =~ [一-龥] ]]; then echo "zh"
  elif [[ "$TEXT" =~ [ぁ-んァ-ヶ] ]]; then echo "ja"
  elif [[ "$TEXT" =~ [가-힣] ]]; then echo "ko"
  else echo "en"; fi
}
[ -z "$LANG_HINT" ] && LANG_HINT="$(detect_lang)"

# Output suffix → format
EXT="${OUTPUT##*.}"
EXT="$(echo "$EXT" | tr '[:upper:]' '[:lower:]')"

need_ffmpeg() { command -v ffmpeg >/dev/null || { echo "ERR: ffmpeg required for format conversion"; exit 1; }; }

# ── edge-tts ────────────────────────────────────────────────────────────────
run_edge() {
  command -v edge-tts >/dev/null || { echo "ERR: edge-tts not installed. run install.sh"; exit 1; }
  if [ -z "$VOICE" ]; then
    case "$LANG_HINT" in
      zh) VOICE="zh-CN-XiaoxiaoNeural";;
      en) VOICE="en-US-AriaNeural";;
      ja) VOICE="ja-JP-NanamiNeural";;
      ko) VOICE="ko-KR-SunHiNeural";;
      *)  VOICE="en-US-AriaNeural";;
    esac
  fi
  local args=(--voice "$VOICE" --text "$TEXT")
  [ -n "$RATE" ]   && args+=(--rate "$RATE")
  [ -n "$PITCH" ]  && args+=(--pitch "$PITCH")
  [ -n "$VOLUME" ] && args+=(--volume "$VOLUME")

  local tmp_mp3
  tmp_mp3="$(mktemp -t edge-tts.XXXXXX).mp3"
  edge-tts "${args[@]}" --write-media "$tmp_mp3"

  if [ "$EXT" = "mp3" ]; then
    mv "$tmp_mp3" "$OUTPUT"
  else
    need_ffmpeg
    ffmpeg -y -loglevel error -i "$tmp_mp3" "$OUTPUT"
    rm -f "$tmp_mp3"
  fi
  echo "✓ edge-tts → $OUTPUT (voice=$VOICE)"
}

# ── kokoro-tts (offline) ────────────────────────────────────────────────────
run_kokoro() {
  if ! command -v kokoro-tts >/dev/null && ! python3 -c "import kokoro" 2>/dev/null; then
    echo "ERR: kokoro not installed. run install.sh"; exit 1
  fi
  [ -z "$VOICE" ] && VOICE="af_heart"  # kokoro default voice
  local tmp_wav
  tmp_wav="$(mktemp -t kokoro.XXXXXX).wav"

  python3 - "$VOICE" "$tmp_wav" <<PYEOF
import sys, soundfile as sf
voice, out = sys.argv[1], sys.argv[2]
text = """$TEXT"""
try:
    from kokoro import KPipeline
    pipe = KPipeline(lang_code='a')  # auto
    audio_chunks = []
    for _, _, audio in pipe(text, voice=voice):
        audio_chunks.append(audio)
    import numpy as np
    data = np.concatenate(audio_chunks) if audio_chunks else np.array([])
    sf.write(out, data, 24000)
except Exception as e:
    print(f"kokoro failed: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF

  if [ "$EXT" = "wav" ]; then
    mv "$tmp_wav" "$OUTPUT"
  else
    need_ffmpeg
    ffmpeg -y -loglevel error -i "$tmp_wav" "$OUTPUT"
    rm -f "$tmp_wav"
  fi
  echo "✓ kokoro → $OUTPUT (voice=$VOICE)"
}

# ── macOS say (fallback) ────────────────────────────────────────────────────
run_say() {
  command -v say >/dev/null || { echo "ERR: 'say' not found (macOS only)"; exit 1; }
  [ -z "$VOICE" ] && case "$LANG_HINT" in
    zh) VOICE="Tingting";;
    ja) VOICE="Kyoko";;
    ko) VOICE="Yuna";;
    *)  VOICE="Samantha";;
  esac
  local tmp_aiff
  tmp_aiff="$(mktemp -t say.XXXXXX).aiff"
  say -v "$VOICE" -o "$tmp_aiff" "$TEXT"

  if [ "$EXT" = "aiff" ]; then
    mv "$tmp_aiff" "$OUTPUT"
  else
    need_ffmpeg
    ffmpeg -y -loglevel error -i "$tmp_aiff" "$OUTPUT"
    rm -f "$tmp_aiff"
  fi
  echo "✓ say → $OUTPUT (voice=$VOICE)"
}

case "$BACKEND" in
  edge|edge-tts) run_edge;;
  kokoro|kokoro-tts) run_kokoro;;
  say|macos) run_say;;
  *) echo "ERR: unknown backend $BACKEND"; exit 1;;
esac
