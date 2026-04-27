#!/usr/bin/env bash
# mac-voice-clone installer
# Default: F5-TTS. Optional: VoxCPM, GPT-SoVITS.
set -euo pipefail

echo "==> mac-voice-clone install"

# 1) ffmpeg
if ! command -v ffmpeg >/dev/null; then
  command -v brew >/dev/null && brew install ffmpeg \
    || echo "WARN: brew not found, install ffmpeg manually"
else
  echo "  ✓ ffmpeg present"
fi

# 2) Python check
python3 -c "import sys; assert sys.version_info >= (3,10), 'need py>=3.10'" \
  || { echo "ERR: python>=3.10 required"; exit 1; }

# 3) PyTorch with MPS
if ! python3 -c "import torch; assert torch.backends.mps.is_available()" 2>/dev/null; then
  echo "Installing torch (MPS)..."
  python3 -m pip install --user --upgrade torch torchaudio
fi

# 4) F5-TTS (default backend)
if ! python3 -c "import f5_tts" 2>/dev/null; then
  echo "Installing F5-TTS..."
  python3 -m pip install --user --upgrade f5-tts
else
  echo "  ✓ f5-tts present"
fi

# 5) VoxCPM (optional)
read -r -p "Install VoxCPM2 (openbmb 2B, ~5GB)? [y/N] " ans || ans="n"
if [[ "${ans:-n}" =~ ^[Yy]$ ]]; then
  python3 -m pip install --user --upgrade voxcpm soundfile
  echo "  ✓ voxcpm installed"
fi

# 6) GPT-SoVITS (optional, larger setup)
read -r -p "Clone GPT-SoVITS (Chinese best, ~3GB)? [y/N] " ans2 || ans2="n"
if [[ "${ans2:-n}" =~ ^[Yy]$ ]]; then
  GPT_SOVITS_DIR="${GPT_SOVITS_DIR:-$HOME/.local/share/GPT-SoVITS}"
  if [ ! -d "$GPT_SOVITS_DIR" ]; then
    git clone --depth 1 https://github.com/RVC-Boss/GPT-SoVITS "$GPT_SOVITS_DIR"
  fi
  ( cd "$GPT_SOVITS_DIR" && python3 -m pip install --user -r requirements.txt || true )
  echo ""
  echo "  ✓ GPT-SoVITS at $GPT_SOVITS_DIR"
  echo "  Add to your shell rc:  export GPT_SOVITS_DIR=\"$GPT_SOVITS_DIR\""
fi

echo ""
echo "Done. Quick test:"
echo "  bash scripts/clone.sh --ref-audio sample.wav --ref-text 'hi' \\"
echo "    --text 'this is a cloned voice' -o /tmp/clone.wav"
