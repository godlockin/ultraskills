#!/usr/bin/env bash
# video-analyzer install — chains mac-whisper + video-frame-extractor installers.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMUNITY_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "==> video-analyzer install (chaining sub-skills)"

# ffmpeg
if ! command -v ffmpeg >/dev/null; then
  command -v brew >/dev/null && brew install ffmpeg \
    || { echo "ERR: install ffmpeg manually"; exit 1; }
fi
echo "  ✓ ffmpeg"

# Sub-skill installers (best-effort)
WHISPER_INSTALL="$COMMUNITY_DIR/mac-whisper/scripts/install.sh"
FRAMES_INSTALL="$COMMUNITY_DIR/video-frame-extractor/scripts/install.sh"

if [ -x "$WHISPER_INSTALL" ]; then
  echo ""
  echo "→ mac-whisper install..."
  bash "$WHISPER_INSTALL" || echo "  WARN: mac-whisper install had issues"
else
  echo "  WARN: $WHISPER_INSTALL not found"
fi

if [ -x "$FRAMES_INSTALL" ]; then
  echo ""
  echo "→ video-frame-extractor install..."
  bash "$FRAMES_INSTALL" || echo "  WARN: frame-extractor install had issues"
fi

echo ""
echo "Done. Test:"
echo "  bash $SCRIPT_DIR/analyze.sh sample.mp4 -o /tmp/report"
