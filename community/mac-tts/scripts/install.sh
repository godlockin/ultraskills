#!/usr/bin/env bash
# mac-tts installer — installs edge-tts (default), optional kokoro, ffmpeg.
set -euo pipefail

echo "==> mac-tts install"

# 1) ffmpeg (recommended for format conversion)
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then
    echo "Installing ffmpeg via brew..."
    brew install ffmpeg
  else
    echo "WARN: ffmpeg not found and brew unavailable. Format conversion (mp3↔wav) disabled."
  fi
else
  echo "  ✓ ffmpeg present"
fi

# 2) Python check
if ! command -v python3 >/dev/null; then
  echo "ERR: python3 required (>=3.9)"; exit 1
fi

# 3) edge-tts (default backend)
if ! command -v edge-tts >/dev/null; then
  echo "Installing edge-tts..."
  python3 -m pip install --user --upgrade edge-tts
else
  echo "  ✓ edge-tts present"
fi

# 4) kokoro (optional, offline)
read -r -p "Install kokoro-tts (offline, ~400MB)? [y/N] " ans || ans="n"
if [[ "${ans:-n}" =~ ^[Yy]$ ]]; then
  python3 -m pip install --user --upgrade kokoro soundfile numpy
  echo "  ✓ kokoro installed"
else
  echo "  skipped kokoro"
fi

echo ""
echo "Done. Test:"
echo "  bash $(dirname "$0")/tts.sh \"你好世界\" -o /tmp/hello.mp3 && open /tmp/hello.mp3"
