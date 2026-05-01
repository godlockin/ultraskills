#!/usr/bin/env bash
# audio-clean — separate / denoise / normalize / pipeline
set -euo pipefail

# Load shared python discovery helper (no host-specific paths)
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/_lib/discover_py.sh"

usage() {
  cat <<EOF
audio-clean — separate / denoise / normalize / pipeline

  clean.sh separate  <in> -o <out> [--model htdemucs|mdx_extra] [--stem vocals|all]
  clean.sh denoise   <in> -o <out> [--method rnnoise|spectral] [--strength 0-1]
  clean.sh normalize <in> -o <out> [--lufs -23|-16|-14] [--tp -1.0] [--lra 11]
  clean.sh pipeline  <in> -o <out> [--steps separate,denoise,normalize] [--lufs -16]
EOF
}

CMD="${1:-}"; shift || true
[ -z "$CMD" ] && { usage; exit 1; }

run_separate() {
  local in="$1" out="$2" model="${3:-htdemucs}" stem="${4:-vocals}"
  discover_py demucs || { echo "ERR: demucs not installed. run install.sh"; exit 1; }
  command -v ffmpeg >/dev/null || { echo "ERR: ffmpeg required"; exit 1; }
  local tmpdir; tmpdir="$(mktemp -d -t demucs.XXXXXX)"
  echo "→ demucs [$model] separating..."
  if [ "$stem" = "all" ]; then
    python3 -m demucs --name "$model" -o "$tmpdir" "$in"
    local base; base="$(basename "${in%.*}")"
    local src="$tmpdir/$model/$base/$stem.wav"
    [ ! -f "$src" ] && src="$(find "$tmpdir/$model/$base" -name "${stem}.wav" | head -1)"
    cp "$src" "$out"
    echo "✓ $stem → $out"
  fi
  rm -rf "$tmpdir"
}

run_denoise() {
  local in="$1" out="$2" method="${3:-rnnoise}" strength="${4:-0.7}"
  command -v ffmpeg >/dev/null || { echo "ERR: ffmpeg required"; exit 1; }
  case "$method" in
    rnnoise)
      # Try ffmpeg arnndn with bundled model first; fallback to spectral
      local model="${HOME}/.cache/audio-clean/rnnoise.rnnn"
      if [ ! -f "$model" ]; then
        mkdir -p "$(dirname "$model")"
        echo "  → fetching rnnoise model..."
        curl -fsSL -o "$model" "https://github.com/GregorR/rnnoise-models/raw/master/somnolent-hogwash-2018-09-01/sh.rnnn" \
          || { echo "  ! rnnoise model fetch failed, falling back to spectral"; method="spectral"; }
      fi
      if [ "$method" = "rnnoise" ]; then
        echo "→ ffmpeg arnndn (rnnoise, mix=$strength)"
        ffmpeg -y -i "$in" -af "arnndn=m=$model:mix=$strength" "$out"
      fi
      ;;
  esac
  if [ "$method" = "spectral" ]; then
    discover_py noisereduce || { echo "ERR: noisereduce not installed. pip install noisereduce soundfile"; exit 1; }
    echo "→ noisereduce (spectral, prop=$strength)"
    python3 - "$in" "$out" "$strength" <<'PY'
import sys, soundfile as sf, noisereduce as nr
inp, outp, strength = sys.argv[1], sys.argv[2], float(sys.argv[3])
data, sr = sf.read(inp)
reduced = nr.reduce_noise(y=data, sr=sr, prop_decrease=strength, stationary=False)
sf.write(outp, reduced, sr)
PY
  fi
  echo "✓ denoised → $out"
}

run_normalize() {
  local in="$1" out="$2" lufs="${3:--16}" tp="${4:--1.0}" lra="${5:-11}"
  command -v ffmpeg >/dev/null || { echo "ERR: ffmpeg required"; exit 1; }
  echo "→ loudnorm I=$lufs TP=$tp LRA=$lra (two-pass EBU R128)"
  # Two-pass: first measure, then apply
  local stats
  stats=$(ffmpeg -hide_banner -i "$in" -af "loudnorm=I=$lufs:TP=$tp:LRA=$lra:print_format=json" -f null - 2>&1 \
    | awk '/^\{/,/^\}/' | tr -d '\n')
  local mi tp_in lra_in thr off
  mi=$(echo "$stats" | sed -n 's/.*"input_i"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  tp_in=$(echo "$stats" | sed -n 's/.*"input_tp"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  lra_in=$(echo "$stats" | sed -n 's/.*"input_lra"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  thr=$(echo "$stats" | sed -n 's/.*"input_thresh"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  off=$(echo "$stats" | sed -n 's/.*"target_offset"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  if [ -z "$mi" ]; then
    echo "  ! pass-1 measure failed, falling back to single-pass"
    ffmpeg -y -i "$in" -af "loudnorm=I=$lufs:TP=$tp:LRA=$lra" "$out"
  else
    echo "  pass-1: I=$mi TP=$tp_in LRA=$lra_in"
    ffmpeg -y -i "$in" -af "loudnorm=I=$lufs:TP=$tp:LRA=$lra:measured_I=$mi:measured_TP=$tp_in:measured_LRA=$lra_in:measured_thresh=$thr:offset=$off:linear=true:print_format=summary" "$out"
  fi
  echo "✓ normalized → $out"
}

run_pipeline() {
  local in="$1" out="$2" steps="${3:-separate,denoise,normalize}" lufs="${4:--16}"
  local cur="$in"
  local tmp1="" tmp2=""
  IFS=',' read -ra arr <<< "$steps"
  for i in "${!arr[@]}"; do
    local step="${arr[$i]}"
    local nxt
    if [ "$i" -eq "$((${#arr[@]}-1))" ]; then nxt="$out"; else nxt="$(mktemp -t aclean.XXXXXX).wav"; fi
    case "$step" in
      separate) run_separate "$cur" "$nxt" htdemucs vocals;;
      denoise)  run_denoise  "$cur" "$nxt" rnnoise 0.7;;
      normalize) run_normalize "$cur" "$nxt" "$lufs" -1.0 11;;
      *) echo "ERR: unknown step: $step"; exit 1;;
    esac
    [ "$cur" != "$in" ] && rm -f "$cur"
    cur="$nxt"
  done
}

# Parse common args
IN=""; OUT=""; MODEL="htdemucs"; STEM="vocals"; METHOD="rnnoise"; STRENGTH="0.7"
LUFS="-16"; TP="-1.0"; LRA="11"; STEPS="separate,denoise,normalize"

case "$CMD" in
  separate|denoise|normalize|pipeline)
    IN="${1:-}"; shift || true
    [ -z "$IN" ] && { usage; exit 1; }
    while [ $# -gt 0 ]; do case "$1" in
      -o|--output) OUT="$2"; shift 2;;
      --model) MODEL="$2"; shift 2;;
      --stem) STEM="$2"; shift 2;;
      --method) METHOD="$2"; shift 2;;
      --strength) STRENGTH="$2"; shift 2;;
      --lufs) LUFS="$2"; shift 2;;
      --tp) TP="$2"; shift 2;;
      --lra) LRA="$2"; shift 2;;
      --steps) STEPS="$2"; shift 2;;
      *) echo "Unknown: $1"; shift;;
    esac; done
    [ -z "$OUT" ] && { echo "ERR: -o required"; exit 1; }
    [ ! -f "$IN" ] && { echo "ERR: input not found: $IN"; exit 1; }
    case "$CMD" in
      separate)  run_separate  "$IN" "$OUT" "$MODEL" "$STEM";;
      denoise)   run_denoise   "$IN" "$OUT" "$METHOD" "$STRENGTH";;
      normalize) run_normalize "$IN" "$OUT" "$LUFS" "$TP" "$LRA";;
      pipeline)  run_pipeline  "$IN" "$OUT" "$STEPS" "$LUFS";;
    esac
    ;;
  -h|--help|help) usage;;
  *) echo "Unknown cmd: $CMD"; usage; exit 1;;
esac
