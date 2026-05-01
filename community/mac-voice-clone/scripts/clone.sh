#!/usr/bin/env bash
# mac-voice-clone — voice cloning dispatcher
# Backends: indextts2 (best prosody) | f5-tts (default, lightweight) | voxcpm | gpt-sovits
set -euo pipefail

# Shared python discovery (no host-specific paths). Override via ULTRASKILLS_PYTHON env.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/_lib/discover_py.sh"

usage() {
  cat <<EOF
mac-voice-clone — clone a voice from reference audio

Usage:
  clone.sh --ref-audio <wav> [--ref-text <text>] --text <text|file|-> [options]

Required:
  --ref-audio <path>      reference audio (6-15s, 16kHz+ mono recommended)
  --text <str|file|->     text to synthesize (or file/stdin)

Backend-specific:
  --backend <indextts2|f5|voxcpm|gpt-sovits>   default: f5
  --ref-text <str>        transcript of reference audio (required for f5/gpt-sovits; optional for indextts2/voxcpm)
  --model <id>            override default model id
  --speed <float>         f5: 1.0 default
  --interval-silence <ms> indextts2: ms between segments (default 350; ↑ for more breath)
  --max-tokens <int>      indextts2: max_text_tokens_per_segment (default 60; ↓ for more pauses)
  --length-penalty <f>    indextts2: default -0.5 (negative slows pacing)

Common:
  -o, --output <path>     output wav (default out.wav)
  --device <auto|mps|cpu> default: auto
  -h, --help

Examples:
  clone.sh --backend indextts2 --ref-audio me.wav \\
           --text "带停顿、呼吸——还有省略号……的旁白" -o out.wav

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
INTERVAL_SILENCE="350"
MAX_TOKENS="60"
LENGTH_PENALTY="-0.5"

if [ $# -eq 0 ]; then usage; exit 0; fi

while [ $# -gt 0 ]; do
  case "$1" in
    --backend) BACKEND="$2"; shift 2;;
    --ref-audio) REF_AUDIO="$2"; shift 2;;
    --ref-text) REF_TEXT="$2"; shift 2;;
    --text) TEXT_INPUT="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --speed) SPEED="$2"; shift 2;;
    --interval-silence) INTERVAL_SILENCE="$2"; shift 2;;
    --max-tokens) MAX_TOKENS="$2"; shift 2;;
    --length-penalty) LENGTH_PENALTY="$2"; shift 2;;
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
  # Use whichever python has torch installed (probe miniconda etc.)
  discover_py torch >/dev/null 2>&1 || true
  if python3 -c "import torch; exit(0 if torch.backends.mps.is_available() else 1)" 2>/dev/null; then
    DEVICE="mps"
  else
    DEVICE="cpu"
  fi
fi

run_f5() {
  discover_py f5_tts || { echo "ERR: f5-tts not installed in any known python env. run install.sh"; exit 1; }
  if ! command -v f5-tts_infer-cli >/dev/null; then
    echo "ERR: f5-tts_infer-cli not on PATH (python env found but CLI missing)"; exit 1
  fi
  [ -z "$REF_TEXT" ] && { echo "ERR: --ref-text required for f5-tts"; exit 1; }
  local m="${MODEL:-F5TTS_v1_Base}"

  # Default HF mirror for users in restricted networks (override by exporting your own)
  : "${HF_ENDPOINT:=https://hf-mirror.com}"
  export HF_ENDPOINT

  # Auto-discover local checkpoint to skip HF download.
  # Search order: env F5_CKPT_DIR > ~/models/F5-TTS > ~/.cache/huggingface/.../F5TTS_v1_Base
  local ckpt="" vocab="" extra_args=()
  local search_dirs=(
    "${F5_CKPT_DIR:-}"
    "$HOME/models/F5-TTS"
    "$HOME/models/$m"
    "$HOME/.cache/huggingface/hub/models--SWivid--F5-TTS/snapshots"
  )
  for d in "${search_dirs[@]}"; do
    [ -z "$d" ] || [ ! -d "$d" ] && continue
    local found
    found="$(find "$d" -maxdepth 4 -name "model_*.safetensors" 2>/dev/null | head -1)"
    if [ -n "$found" ]; then
      ckpt="$found"
      vocab="$(dirname "$ckpt")/vocab.txt"
      [ ! -f "$vocab" ] && vocab="$(find "$(dirname "$ckpt")/.." -maxdepth 2 -name vocab.txt 2>/dev/null | head -1)"
      break
    fi
  done

  if [ -n "$ckpt" ]; then
    echo "  → using local ckpt: $ckpt"
    extra_args+=(--ckpt_file "$ckpt")
    [ -n "$vocab" ] && [ -f "$vocab" ] && extra_args+=(--vocab_file "$vocab")
  else
    echo "  → no local ckpt, will download from HF (endpoint=$HF_ENDPOINT)"
  fi

  echo "→ F5-TTS [$m] device=$DEVICE"
  f5-tts_infer-cli \
    --model "$m" \
    "${extra_args[@]}" \
    --ref_audio "$REF_AUDIO" \
    --ref_text "$REF_TEXT" \
    --gen_text "$TEXT" \
    --output_dir "$(dirname "$OUTPUT")" \
    --output_file "$(basename "$OUTPUT")" \
    --speed "$SPEED"
  echo "✓ F5-TTS → $OUTPUT"
}

run_voxcpm() {
  discover_py voxcpm || { echo "ERR: voxcpm not installed in any known python env. run install.sh"; exit 1; }
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

run_indextts2() {
  # IndexTTS-2 — must be installed via uv (NOT pip/conda) per upstream README.
  # Expects $INDEX_TTS_DIR pointing at a `git clone https://github.com/index-tts/index-tts`
  # that has been `uv sync --all-extras`'d and has checkpoints/ downloaded.
  if [ -z "${INDEX_TTS_DIR:-}" ] || [ ! -d "$INDEX_TTS_DIR" ]; then
    echo "ERR: set INDEX_TTS_DIR=/path/to/index-tts (git clone https://github.com/index-tts/index-tts)"
    echo "     then: cd \$INDEX_TTS_DIR && uv sync --all-extras"
    echo "     then: uv run hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints"
    exit 1
  fi
  local cfg="$INDEX_TTS_DIR/checkpoints/config.yaml"
  local mdir="$INDEX_TTS_DIR/checkpoints"
  if [ ! -f "$cfg" ] || [ ! -d "$mdir" ]; then
    echo "ERR: missing checkpoints. run:"
    echo "     cd $INDEX_TTS_DIR && uv run hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints"
    exit 1
  fi
  if ! command -v uv >/dev/null 2>&1; then
    echo "ERR: 'uv' not on PATH. install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
  fi
  : "${HF_ENDPOINT:=https://hf-mirror.com}"
  export HF_ENDPOINT
  echo "→ IndexTTS-2 device=$DEVICE  interval_silence=${INTERVAL_SILENCE}ms  max_tokens=${MAX_TOKENS}  length_penalty=${LENGTH_PENALTY}"

  ( cd "$INDEX_TTS_DIR" && \
    INDEX_REF="$REF_AUDIO" INDEX_TEXT="$TEXT" INDEX_OUT="$OUTPUT" \
    INDEX_CFG="$cfg" INDEX_MDIR="$mdir" INDEX_DEVICE="$DEVICE" \
    INDEX_SIL="$INTERVAL_SILENCE" INDEX_MAXTOK="$MAX_TOKENS" INDEX_LP="$LENGTH_PENALTY" \
    uv run python - <<'PYEOF'
import os, sys
from pathlib import Path
ref   = os.environ["INDEX_REF"]
text  = os.environ["INDEX_TEXT"]
out   = os.environ["INDEX_OUT"]
cfg   = os.environ["INDEX_CFG"]
mdir  = os.environ["INDEX_MDIR"]
dev_in= os.environ.get("INDEX_DEVICE", "auto")
sil   = int(os.environ.get("INDEX_SIL", "350"))
mxtok = int(os.environ.get("INDEX_MAXTOK", "60"))
lp    = float(os.environ.get("INDEX_LP", "-0.5"))

import torch
if dev_in in ("mps","cpu","cuda"):
    device = dev_in
else:
    device = "mps" if (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()) else "cpu"

Path(os.path.dirname(out) or ".").mkdir(parents=True, exist_ok=True)
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path=cfg, model_dir=mdir, use_fp16=False, device=device)
tts.infer(
    spk_audio_prompt=ref,
    text=text,
    output_path=out,
    verbose=False,
    interval_silence=sil,
    max_text_tokens_per_segment=mxtok,
    length_penalty=lp,
    temperature=0.75,
    top_p=0.85,
    top_k=30,
    num_beams=3,
    repetition_penalty=10.0,
)
print(f"  wrote {out}")
PYEOF
  )
  echo "✓ IndexTTS-2 → $OUTPUT"
}

case "$BACKEND" in
  indextts2|indextts|index-tts) run_indextts2;;
  f5|f5-tts) run_f5;;
  voxcpm)    run_voxcpm;;
  gpt-sovits|sovits) run_gpt_sovits;;
  *) echo "ERR: unknown backend $BACKEND"; exit 1;;
esac
