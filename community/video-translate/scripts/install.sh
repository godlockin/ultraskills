#!/usr/bin/env bash
# video-translate installer — verifies dependent skills + ffmpeg
set -euo pipefail
echo "==> video-translate install (verifying dependencies)"

COMMUNITY="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# 1) ffmpeg
command -v ffmpeg >/dev/null || {
  echo "→ installing ffmpeg via brew..."
  command -v brew >/dev/null && brew install ffmpeg || { echo "ERR: install ffmpeg"; exit 1; }
}
echo "  ✓ ffmpeg"

# 2) check sibling skills
for s in mac-whisper mac-tts; do
  d="$COMMUNITY/$s"
  if [ -d "$d" ]; then
    echo "  ✓ $s present"
  else
    echo "  ! $s NOT installed in community/. Find it: bash $COMMUNITY/../setup.sh --top"
  fi
done

# 3) optional skills
for s in mac-voice-clone audio-clean; do
  d="$COMMUNITY/$s"
  [ -d "$d" ] && echo "  ✓ $s present (optional)" || echo "  · $s missing (only needed for cloned-dub / --keep-bgm)"
done

# 4) python3 (for translate_segments.py + helpers)
source "$COMMUNITY/_lib/discover_py.sh"
PY="$(discover_py_min_version 3.9)" || { echo "ERR: need python3>=3.9"; exit 1; }
echo "  ✓ python: $PY"

# 5) LLM backend hint
if command -v claude >/dev/null; then
  echo "  ✓ claude CLI (default --llm)"
elif "$PY" -c "import openai" 2>/dev/null; then
  echo "  ✓ openai SDK (use --llm openai, set OPENAI_API_KEY)"
elif command -v ollama >/dev/null; then
  echo "  ✓ ollama (use --llm ollama)"
else
  echo "  ! no LLM backend found. install one of:"
  echo "      claude CLI   |   pip install openai   |   brew install ollama"
fi

echo ""
echo "Done. Try:"
echo "  bash scripts/translate.sh subs my.mp4 --to en -o en.srt"
