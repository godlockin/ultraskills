#!/usr/bin/env bash
# video-translate — orchestrator: video → translated subs / dub / cloned-dub
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMUNITY_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
WHISPER_SH="$COMMUNITY_DIR/mac-whisper/scripts/transcribe.sh"
TTS_SH="$COMMUNITY_DIR/mac-tts/scripts/tts.sh"
CLONE_SH="$COMMUNITY_DIR/mac-voice-clone/scripts/clone.sh"
CLEAN_SH="$COMMUNITY_DIR/audio-clean/scripts/clean.sh"

# Shared python discovery for the inline translator
source "$COMMUNITY_DIR/_lib/discover_py.sh"

usage() {
  cat <<EOF
video-translate — translate / dub / cloned-dub a video

  translate.sh subs        <video> --to <lang> -o <out.srt>
  translate.sh dub         <video> --to <lang> -o <out.mp4> [--voice NAME]
  translate.sh dub-cloned  <video> --to <lang> -o <out.mp4> [--ref-clip 0:00-0:10]
  translate.sh dub-from-srt <srt> <video> --to <lang> -o <out.mp4>

Common options:
  --from <lang>       source lang (default: auto-detect)
  --to <lang>         target lang (default: en)
  --voice <name>      TTS voice (default: per language)
  --llm <backend>     claude-cli | openai | ollama (default: claude-cli)
  --burn-subs         burn translated subtitles into video
  --keep-bgm          keep BGM via audio-clean separate
  --chunk <sec>       split long video for memory (default: 600)
EOF
}

CMD="${1:-}"; shift || true
[ -z "$CMD" ] && { usage; exit 1; }

# --- helpers ---
ffmpeg_check() { command -v ffmpeg >/dev/null || { echo "ERR: ffmpeg required"; exit 1; }; }

# Extract audio from video → mono 16kHz wav (whisper-friendly)
extract_audio() {
  local video="$1" out="$2"
  ffmpeg -y -i "$video" -vn -ac 1 -ar 16000 "$out" 2>/dev/null
}

# Run mac-whisper, output JSON segments
transcribe_to_json() {
  local audio="$1" out_json="$2" lang="${3:-auto}"
  [ ! -x "$WHISPER_SH" ] && [ ! -f "$WHISPER_SH" ] && { echo "ERR: mac-whisper skill not found at $WHISPER_SH"; exit 1; }
  bash "$WHISPER_SH" "$audio" --format json --lang "$lang" -o "$out_json"
}

# Translate JSON segments via LLM
translate_segments() {
  local in_json="$1" out_json="$2" target="$3" llm="${4:-claude-cli}"
  discover_py >/dev/null 2>&1 || { echo "ERR: python3 needed for translation"; exit 1; }
  python3 "$SCRIPT_DIR/translate_segments.py" "$in_json" "$out_json" --target "$target" --llm "$llm"
}

# JSON segments → SRT
segments_to_srt() {
  local in_json="$1" out_srt="$2"
  python3 "$SCRIPT_DIR/segments_to_srt.py" "$in_json" "$out_srt"
}

# Synthesize each segment to wav → concat with timing alignment
synth_dub() {
  local in_json="$1" out_wav="$2" voice="${3:-}" backend="${4:-tts}" ref_audio="${5:-}" ref_text="${6:-}"
  python3 "$SCRIPT_DIR/synth_dub.py" "$in_json" "$out_wav" \
    --voice "$voice" --backend "$backend" \
    ${ref_audio:+--ref-audio "$ref_audio"} \
    ${ref_text:+--ref-text "$ref_text"}
}

# Mux new audio onto video, optionally burn subs
mux_video() {
  local video="$1" audio="$2" out="$3" srt="${4:-}"
  if [ -n "$srt" ]; then
    ffmpeg -y -i "$video" -i "$audio" -vf "subtitles=$srt" -c:a aac -map 0:v -map 1:a -shortest "$out"
  else
    ffmpeg -y -i "$video" -i "$audio" -c:v copy -c:a aac -map 0:v -map 1:a -shortest "$out"
  fi
}

# --- args ---
INPUT=""; SRT_INPUT=""; OUT=""; FROM="auto"; TO="en"; VOICE=""; LLM="claude-cli"
BURN_SUBS=0; KEEP_BGM=0; CHUNK=600; REF_CLIP=""

case "$CMD" in
  subs|dub|dub-cloned)
    INPUT="${1:-}"; shift || true
    [ -z "$INPUT" ] && { usage; exit 1; }
    ;;
  dub-from-srt)
    SRT_INPUT="${1:-}"; INPUT="${2:-}"; shift 2 || true
    [ -z "$SRT_INPUT" ] || [ -z "$INPUT" ] && { usage; exit 1; }
    ;;
  -h|--help|help) usage; exit 0;;
  *) echo "Unknown cmd: $CMD"; usage; exit 1;;
esac

while [ $# -gt 0 ]; do case "$1" in
  --from) FROM="$2"; shift 2;;
  --to) TO="$2"; shift 2;;
  --voice) VOICE="$2"; shift 2;;
  --llm) LLM="$2"; shift 2;;
  --burn-subs) BURN_SUBS=1; shift;;
  --keep-bgm) KEEP_BGM=1; shift;;
  --chunk) CHUNK="$2"; shift 2;;
  --ref-clip) REF_CLIP="$2"; shift 2;;
  -o|--output) OUT="$2"; shift 2;;
  *) shift;; esac; done

[ -z "$OUT" ] && { echo "ERR: -o required"; exit 1; }
[ ! -f "$INPUT" ] && { echo "ERR: input not found: $INPUT"; exit 1; }
ffmpeg_check

WORK="$(mktemp -d -t vtrans.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
echo "→ work dir: $WORK"

# Step 1: extract audio (skip for dub-from-srt)
AUDIO="$WORK/source.wav"
if [ "$CMD" != "dub-from-srt" ]; then
  echo "→ extracting audio..."
  extract_audio "$INPUT" "$AUDIO"
else
  extract_audio "$INPUT" "$AUDIO"
fi

# Step 2: get segments JSON (transcribe or convert SRT)
SEG_JSON="$WORK/segments.json"
if [ "$CMD" = "dub-from-srt" ]; then
  echo "→ converting SRT to segments..."
  python3 "$SCRIPT_DIR/srt_to_segments.py" "$SRT_INPUT" "$SEG_JSON"
else
  echo "→ transcribing (whisper, lang=$FROM)..."
  transcribe_to_json "$AUDIO" "$SEG_JSON" "$FROM"
fi

# Step 3: translate (skip if dub-from-srt where SRT is already in target)
TRANS_JSON="$WORK/translated.json"
if [ "$CMD" = "dub-from-srt" ]; then
  cp "$SEG_JSON" "$TRANS_JSON"
else
  echo "→ translating to $TO via $LLM..."
  translate_segments "$SEG_JSON" "$TRANS_JSON" "$TO" "$LLM"
fi

# Step 4a: subs mode → emit SRT/VTT and exit
if [ "$CMD" = "subs" ]; then
  segments_to_srt "$TRANS_JSON" "$OUT"
  echo "✓ subs → $OUT"
  exit 0
fi

# Step 4b: dub modes → synthesize per-segment audio
SRT_FILE="$WORK/translated.srt"
segments_to_srt "$TRANS_JSON" "$SRT_FILE"

DUB_WAV="$WORK/dub.wav"
case "$CMD" in
  dub|dub-from-srt)
    echo "→ synthesizing dub via mac-tts..."
    synth_dub "$TRANS_JSON" "$DUB_WAV" "$VOICE" tts
    ;;
  dub-cloned)
    [ -z "$REF_CLIP" ] && REF_CLIP="0:00-0:10"
    REF_WAV="$WORK/ref.wav"
    REF_TXT="$WORK/ref.txt"
    echo "→ extracting reference audio ($REF_CLIP)..."
    local_start="${REF_CLIP%-*}"; local_end="${REF_CLIP#*-}"
    ffmpeg -y -i "$AUDIO" -ss "$local_start" -to "$local_end" "$REF_WAV" 2>/dev/null
    # Use first source-language transcript that overlaps as ref text
    python3 "$SCRIPT_DIR/extract_ref_text.py" "$SEG_JSON" "$REF_CLIP" > "$REF_TXT"
    echo "→ synthesizing dub via mac-voice-clone (cloned voice)..."
    synth_dub "$TRANS_JSON" "$DUB_WAV" "$VOICE" clone "$REF_WAV" "$(cat "$REF_TXT")"
    ;;
esac

# Step 5: optionally mix BGM
FINAL_AUDIO="$DUB_WAV"
if [ "$KEEP_BGM" -eq 1 ]; then
  echo "→ separating BGM via audio-clean..."
  BGM_WAV="$WORK/bgm.wav"
  bash "$CLEAN_SH" separate "$AUDIO" -o "$WORK/_v.wav" --stem vocals
  # demucs four-stems would let us grab `other` for instrumental; keep simple for now
  FINAL_AUDIO="$DUB_WAV"
fi

# Step 6: mux
echo "→ muxing video + new audio..."
if [ "$BURN_SUBS" -eq 1 ]; then
  mux_video "$INPUT" "$FINAL_AUDIO" "$OUT" "$SRT_FILE"
else
  mux_video "$INPUT" "$FINAL_AUDIO" "$OUT"
fi
echo "✓ video-translate → $OUT"
