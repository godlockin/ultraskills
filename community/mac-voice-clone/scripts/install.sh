#!/usr/bin/env bash
# mac-voice-clone installer
# Default: F5-TTS. Optional: VoxCPM, GPT-SoVITS.
set -euo pipefail

echo "==> mac-voice-clone install"

# Pick a python>=3.10 via shared discovery (works on any host).
# Override with: ULTRASKILLS_PYTHON=/abs/path/to/python3 bash install.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/_lib/discover_py.sh"
PY="$(discover_py_min_version 3.10)" || {
  echo "ERR: need python>=3.10. install homebrew python (brew install python@3.12) or set ULTRASKILLS_PYTHON"
  exit 1
}
echo "  ✓ python: $PY ($($PY -V))"
PY_BIN_DIR="$(dirname "$PY")"

# HF mirror — let users in restricted networks default to a mirror.
# Append to ~/.zshrc only if user opts in (we don't auto-touch dotfiles).
if [ -z "${HF_ENDPOINT:-}" ]; then
  echo "  ℹ for faster downloads in some regions, consider:"
  echo "      export HF_ENDPOINT=https://hf-mirror.com"
fi

# 1) ffmpeg
if ! command -v ffmpeg >/dev/null; then
  command -v brew >/dev/null && brew install ffmpeg \
    || echo "WARN: brew not found, install ffmpeg manually"
else
  echo "  ✓ ffmpeg present"
fi

# 2) Python check
# (already chosen above as $PY)

# 3) PyTorch with MPS
if ! "$PY" -c "import torch; assert torch.backends.mps.is_available()" 2>/dev/null; then
  echo "Installing torch (MPS)..."
  "$PY" -m pip install --upgrade torch torchaudio torchvision
fi

# 4) F5-TTS (default backend)
if ! "$PY" -c "import f5_tts" 2>/dev/null; then
  echo "Installing F5-TTS..."
  "$PY" -m pip install --upgrade f5-tts
else
  echo "  ✓ f5-tts present"
fi

# 5) VoxCPM (optional)
read -r -p "Install VoxCPM2 (openbmb 2B, ~5GB)? [y/N] " ans || ans="n"
if [[ "${ans:-n}" =~ ^[Yy]$ ]]; then
  "$PY" -m pip install --upgrade voxcpm soundfile
  echo "  ✓ voxcpm installed"
fi

# 6) GPT-SoVITS (optional, larger setup)
read -r -p "Clone GPT-SoVITS (Chinese best, ~3GB)? [y/N] " ans2 || ans2="n"
if [[ "${ans2:-n}" =~ ^[Yy]$ ]]; then
  GPT_SOVITS_DIR="${GPT_SOVITS_DIR:-$HOME/.local/share/GPT-SoVITS}"
  if [ ! -d "$GPT_SOVITS_DIR" ]; then
    git clone --depth 1 https://github.com/RVC-Boss/GPT-SoVITS "$GPT_SOVITS_DIR"
  fi
  ( cd "$GPT_SOVITS_DIR" && "$PY" -m pip install -r requirements.txt || true )
  echo ""
  echo "  ✓ GPT-SoVITS at $GPT_SOVITS_DIR"
  echo "  Add to your shell rc:  export GPT_SOVITS_DIR=\"$GPT_SOVITS_DIR\""
fi

echo ""
echo "Done. Quick test:"
echo "  bash scripts/clone.sh --ref-audio sample.wav --ref-text 'hi' \\"
echo "    --text 'this is a cloned voice' -o /tmp/clone.wav"
echo ""
# PATH guidance: clone.sh auto-discovers, but heads-up if conda not on PATH
if ! command -v f5-tts_infer-cli >/dev/null 2>&1; then
  echo "NOTE: f5-tts_infer-cli not on your shell PATH."
  echo "      clone.sh will auto-find it at: $PY_BIN_DIR"
  echo "      For interactive use, add to ~/.zshrc:"
  echo "        export PATH=\"$PY_BIN_DIR:\$PATH\""
fi
