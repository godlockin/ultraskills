#!/usr/bin/env bash
# mac-voice-clone — voice cloning dispatcher
# Backends: f5-tts (default) | voxcpm | gpt-sovits
set -euo pipefail

usage() {
  cat <<EOF
mac-voice-clone — clone a voice from reference audio

Usage:
  clone.sh --ref-audio <wav> [--ref-text <text>] --text <text|file|-> [options]

Required:
  --ref-audio <path>      reference audio (6-15s, 16kHz+ mono recommended)
  --text <str|file|->     text to synthesize (or file/stdin)

Backend-specific:
  --backend <f5|voxcpm|gpt-sovits>   default: f5
  --ref-text <str>        transcript of reference audio (required for f5/gpt-sovits)
  --model <id>            override default model id
  --speed <float>         f5: 1.0 default

Common:
  -o, --output <path>     output wav (default out.wav)
  --device <auto|mps|cpu> default: auto
  -h, --help

Examples:
  clone.sh --ref-audio me.wav --ref-text "Hello world" \\
           --text "Synthesize this in my voice" -o out.wav

  clone.sh --backend voxcpm --ref-audio me.wav --text "Multi-lang text" -o out.wav

  clone.sh --backend gpt-sovits --ref-audio zh.wav --ref-text "你好" \\
           --text "今天天气真好" -o zh.wav
EOF
}

BACKEND="f5"
REF_AUDIO=""
REF_TEXT=""
TEXT_INPUT=""
OUTPUT="out.wav"
MODEL=""
SPEED="1.0"
DEVICE="auto"

if [ $# -eq 0 ]; then usage; exit 0; fi

while [ $# -gt 0 ]; do
  case "$1" in
    --backend) BACKEND="$2"; shift 2;;
    --ref-audio) REF_AUDIO="$2"; shift 2;;
    --ref-text) REF_TEXT="$2"; shift 2;;
    --text) TEXT_INPUT="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --speed) SPEED="$2"; shift 2;;
    --device) DEVICE="$2"; shift 2;;
    -o|--output) OUTPUT="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

[ -z "$REF_AUDIO" ] && { echo "ERR: --ref-audio required"; exit 1; }
[ ! -f "$REF_AUDIO" ] && { echo "ERR: ref audio not found: $REF_AUDIO"; exit 1; }
[ -z "$TEXT_INPUT" ] && { echo "ERR: --text required"; exit 1; }

# Resolve TEXT
if [ "$TEXT_INPUT" = "-" ]; then
  TEXT="$(cat)"
elif [ -f "$TEXT_INPUT" ]; then
  TEXT="$(cat "$TEXT_INPUT")"
else
  TEXT="$TEXT_INPUT"
fi
[ -z "${TEXT// /}" ] && { echo "ERR: empty text"; exit 1; }

# Auto-detect device for python backends
if [ "$DEVICE" = "auto" ]; then
  if python3 -c "import torch; exit(0 if torch.backends.mps.is_available() else 1)" 2>/dev/null; then
    DEVICE="mps"
  else
    DEVICE="cpu"
  fi
fi

run_f5() {
  if ! python3 -c "import f5_tts" 2>/dev/null; then
    echo "ERR: f5-tts not installed. run install.sh"; exit 1
  fi
  [ -z "$REF_TEXT" ] && { echo "ERR: --ref-text required for f5-tts"; exit 1; }
  local m="${MODEL:-F5TTS_v1_Base}"
  echo "→ F5-TTS [$m] device=$DEVICE"
  f5-tts_infer-cli \
    --model "$m" \
    --ref_audio "$REF_AUDIO" \
    --ref_text "$REF_TEXT" \
    --gen_text "$TEXT" \
    --output_dir "$(dirname "$OUTPUT")" \
    --output_file "$(basename "$OUTPUT")" \
    --speed "$SPEED"
  echo "✓ F5-TTS → $OUTPUT"
}

run_voxcpm() {
  if ! python3 -c "import voxcpm" 2>/dev/null; then
    echo "ERR: voxcpm not installed. run install.sh"; exit 1
  fi
  local m="${MODEL:-openbmb/VoxCPM2}"
  echo "→ VoxCPM [$m] device=$DEVICE"
  python3 - "$REF_AUDIO" "$REF_TEXT" "$TEXT" "$OUTPUT" "$m" "$DEVICE" <<'PYEOF'
import sys, soundfile as sf
ref_audio, ref_text, text, out, model_id, device = sys.argv[1:7]
from voxcpm import VoxCPM
import torch
dev = device if device in ("mps","cpu","cuda") else ("mps" if torch.backends.mps.is_available() else "cpu")
model = VoxCPM.from_pretrained(model_id)
try:
    model = model.to(dev)
except Exception:
    pass
kwargs = {"text": text, "prompt_audio": ref_audio}
if ref_text:
    kwargs["prompt_text"] = ref_text
wav = model.generate(**kwargs)
sr = getattr(model, "sample_rate", 48000)
sf.write(out, wav, sr)
print(f"  wrote {out} @ {sr}Hz")
PYEOF
  echo "✓ VoxCPM → $OUTPUT"
}

run_gpt_sovits() {
  if [ -z "${GPT_SOVITS_DIR:-}" ] || [ ! -d "$GPT_SOVITS_DIR" ]; then
    echo "ERR: set GPT_SOVITS_DIR=/path/to/GPT-SoVITS (clone from RVC-Boss/GPT-SoVITS)"
    echo "     run install.sh first to clone & set up"
    exit 1
  fi
  [ -z "$REF_TEXT" ] && { echo "ERR: --ref-text required for gpt-sovits"; exit 1; }
  echo "→ GPT-SoVITS device=$DEVICE"
  ( cd "$GPT_SOVITS_DIR" && python3 inference_cli.py \
      --ref_audio "$REF_AUDIO" \
      --ref_text  "$REF_TEXT" \
      --target_text "$TEXT" \
      --output "$OUTPUT" )
  echo "✓ GPT-SoVITS → $OUTPUT"
}

case "$BACKEND" in
  f5|f5-tts) run_f5;;
  voxcpm)    run_voxcpm;;
  gpt-sovits|sovits) run_gpt_sovits;;
  *) echo "ERR: unknown backend $BACKEND"; exit 1;;
esac
