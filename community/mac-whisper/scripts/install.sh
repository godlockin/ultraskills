#!/usr/bin/env bash
# mac-whisper :: install.sh
# Installs mlx-whisper (preferred) and optionally whisper.cpp (fallback).
set -euo pipefail

echo "=== mac-whisper installer ==="

# 1. mlx-whisper (preferred)
if command -v mlx_whisper >/dev/null 2>&1; then
  echo "✔ mlx-whisper already installed"
else
  echo "→ Installing mlx-whisper via pip..."
  if command -v pip3 >/dev/null 2>&1; then
    pip3 install -U mlx-whisper
  else
    pip install -U mlx-whisper
  fi
fi

# 2. ffmpeg (required for non-wav input)
if command -v ffmpeg >/dev/null 2>&1; then
  echo "✔ ffmpeg present"
else
  echo "→ Installing ffmpeg via Homebrew..."
  brew install ffmpeg
fi

# 3. whisper.cpp (optional fallback)
read -r -p "Also install whisper.cpp as fallback? (y/N) " ans
if [[ "${ans:-N}" =~ ^[Yy]$ ]]; then
  if command -v whisper-cli >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1; then
    echo "✔ whisper.cpp already installed"
  else
    brew install whisper-cpp
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

echo
echo "✅ Done. Test:"
echo "    bash $(dirname "$0")/transcribe.sh path/to/audio.mp3 --lang zh --format srt"
