#!/usr/bin/env bash
# mac-whisper :: install.sh
# Auto-detects the best available backend and installs it.
# Order: mlx-whisper (arm64 mac only) → faster-whisper (any platform) → whisper.cpp
set -uo pipefail  # not -e: we want to try fallbacks even if one fails

echo "=== mac-whisper installer ==="

ARCH="$(uname -m)"
PY_ARCH="$(python3 -c 'import platform; print(platform.machine())' 2>/dev/null || echo "$ARCH")"
echo "🖥  Arch: $ARCH  |  Python arch: $PY_ARCH"

# 1. ffmpeg (required for non-wav input)
if command -v ffmpeg >/dev/null 2>&1; then
  echo "✔ ffmpeg present"
else
  echo "→ Installing ffmpeg via Homebrew..."
  brew install ffmpeg || echo "⚠️  ffmpeg install failed; install manually: brew install ffmpeg"
fi

# 2. Try mlx-whisper ONLY on native arm64 macOS
if [[ "$ARCH" == "arm64" && "$PY_ARCH" == "arm64" ]]; then
  if command -v mlx_whisper >/dev/null 2>&1; then
    echo "✔ mlx-whisper already installed"
  else
    echo "→ Installing mlx-whisper..."
    if command -v pip3 >/dev/null 2>&1; then
      pip3 install -U mlx-whisper && echo "✔ mlx-whisper installed"
    else
      pip install -U mlx-whisper && echo "✔ mlx-whisper installed"
    fi || echo "⚠️  mlx-whisper install failed; will try faster-whisper"
  fi
else
  echo "ℹ️  Skipping mlx-whisper (requires native arm64 macOS; you have: $PY_ARCH)"
fi

# 3. Always try faster-whisper as cross-platform fallback
if python3 -c "import faster_whisper" 2>/dev/null; then
  echo "✔ faster-whisper already installed"
else
  echo "→ Installing faster-whisper..."
  if command -v pip3 >/dev/null 2>&1; then
    pip3 install -U faster-whisper && echo "✔ faster-whisper installed"
  else
    pip install -U faster-whisper && echo "✔ faster-whisper installed"
  fi || echo "⚠️  faster-whisper install failed"
fi

# 4. Optional: whisper.cpp (smaller binary, good for low-RAM systems)
read -r -p "Also install whisper.cpp as offline fallback? (y/N) " ans
if [[ "${ans:-N}" =~ ^[Yy]$ ]]; then
  if command -v whisper-cli >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1; then
    echo "✔ whisper.cpp already installed"
  else
    brew install whisper-cpp || echo "⚠️  whisper.cpp install failed"
  fi

  MODEL_DIR="$HOME/.cache/whisper.cpp"
  MODEL_FILE="$MODEL_DIR/ggml-large-v3-turbo-q5_0.bin"
  if [[ ! -f "$MODEL_FILE" ]]; then
    mkdir -p "$MODEL_DIR"
    echo "→ Downloading ggml-large-v3-turbo-q5_0 (~570MB)..."
    curl -L -o "$MODEL_FILE" \
      https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
  fi
  echo "✔ whisper.cpp model: $MODEL_FILE"
fi

# 5. Final summary — what's actually usable?
echo
echo "=== Backend summary ==="
HAS_ANY=0
if [[ "$ARCH" == "arm64" && "$PY_ARCH" == "arm64" ]] && command -v mlx_whisper >/dev/null 2>&1; then
  echo "  ✅ mlx-whisper    (preferred, arm64 only)"; HAS_ANY=1
fi
if python3 -c "import faster_whisper" 2>/dev/null; then
  echo "  ✅ faster-whisper (cross-platform fallback)"; HAS_ANY=1
fi
if command -v whisper-cli >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1; then
  echo "  ✅ whisper.cpp    (offline, low-RAM)"; HAS_ANY=1
fi
[[ $HAS_ANY -eq 0 ]] && echo "  ❌ No backend installed. Run this script again or install manually."

echo
echo "✅ Done. Test:"
echo "    bash $(dirname "$0")/transcribe.sh path/to/audio.mp3 --lang zh --format srt"
