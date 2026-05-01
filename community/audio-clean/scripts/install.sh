#!/usr/bin/env bash
# audio-clean installer
set -euo pipefail
echo "==> audio-clean install"

# 1) ffmpeg
if ! command -v ffmpeg >/dev/null; then
  command -v brew >/dev/null && brew install ffmpeg || { echo "ERR: install ffmpeg manually"; exit 1; }
fi
echo "  ✓ ffmpeg"

# 2) Pick python>=3.10 via shared discovery (no host-specific paths)
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/_lib/discover_py.sh"
PY="$(discover_py_min_version 3.10)" || { echo "ERR: need python>=3.10 (set ULTRASKILLS_PYTHON=/path/to/python3 to override)"; exit 1; }
echo "  ✓ python: $PY ($($PY -V))"

# 3) demucs (separation)
if ! "$PY" -c "import demucs" 2>/dev/null; then
  echo "Installing demucs..."
  "$PY" -m pip install --upgrade demucs
fi
echo "  ✓ demucs"

# 4) noisereduce (spectral denoise fallback)
if ! "$PY" -c "import noisereduce" 2>/dev/null; then
  "$PY" -m pip install --upgrade noisereduce soundfile
fi
echo "  ✓ noisereduce + soundfile"

# 5) RNNoise model (optional, fetched on first denoise call)
mkdir -p "$HOME/.cache/audio-clean"

echo ""
echo "Done. Test:"
echo "  bash scripts/clean.sh normalize input.mp3 -o out.wav --lufs -16"
