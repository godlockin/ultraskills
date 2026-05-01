#!/usr/bin/env bash
# discover_py.sh — shared python discovery helper for ultraskills audio/video skills.
#
# Usage:
#   source "$(dirname "$0")/../../_lib/discover_py.sh"
#   discover_py PKG               # ensures PATH has a python3 with `import PKG` succeeding
#   discover_py_min_version 3.10  # ensures any python3>=3.10 is on PATH (no package check)
#
# Strategy (in order):
#   1. Honor explicit env: ULTRASKILLS_PYTHON=/abs/path/to/python3
#   2. Try `command -v python3` from current PATH — if it has the package, done
#   3. Probe common conda/homebrew/system locations as FALLBACK only
#
# Never assumes conda is installed. Works on any Mac / Linux user.

discover_py() {
  local pkg="${1:-}"
  # 1. Explicit override
  if [ -n "${ULTRASKILLS_PYTHON:-}" ] && [ -x "$ULTRASKILLS_PYTHON" ]; then
    if [ -z "$pkg" ] || "$ULTRASKILLS_PYTHON" -c "import $pkg" 2>/dev/null; then
      export PATH="$(dirname "$ULTRASKILLS_PYTHON"):$PATH"
      return 0
    fi
  fi
  # 2. Current PATH first
  if command -v python3 >/dev/null 2>&1; then
    if [ -z "$pkg" ] || python3 -c "import $pkg" 2>/dev/null; then
      return 0
    fi
  fi
  # 3. Fallback locations (alphabetical preference: official > conda > brew)
  local candidates=(
    "/opt/homebrew/bin/python3.13"
    "/opt/homebrew/bin/python3.12"
    "/opt/homebrew/bin/python3.11"
    "/opt/homebrew/bin/python3"
    "/usr/local/bin/python3"
    "$HOME/miniconda3/bin/python3"
    "$HOME/miniforge3/bin/python3"
    "$HOME/anaconda3/bin/python3"
    "$HOME/mambaforge/bin/python3"
    "/usr/bin/python3"
  )
  local d py
  for py in "${candidates[@]}"; do
    [ ! -x "$py" ] && continue
    if [ -z "$pkg" ] || "$py" -c "import $pkg" 2>/dev/null; then
      d="$(dirname "$py")"
      export PATH="$d:$PATH"
      [ -n "${VERBOSE:-}" ] && echo "  → using python: $py" >&2
      return 0
    fi
  done
  return 1
}

discover_py_min_version() {
  local min="${1:-3.10}"
  local maj="${min%.*}" minor="${min#*.}"
  # Same probe order, but check sys.version_info instead of importing pkg
  if [ -n "${ULTRASKILLS_PYTHON:-}" ] && [ -x "$ULTRASKILLS_PYTHON" ]; then
    if "$ULTRASKILLS_PYTHON" -c "import sys; assert sys.version_info >= ($maj,$minor)" 2>/dev/null; then
      export PATH="$(dirname "$ULTRASKILLS_PYTHON"):$PATH"
      echo "$ULTRASKILLS_PYTHON"; return 0
    fi
  fi
  if command -v python3 >/dev/null 2>&1 && \
     python3 -c "import sys; assert sys.version_info >= ($maj,$minor)" 2>/dev/null; then
    command -v python3; return 0
  fi
  for py in \
    "/opt/homebrew/bin/python3.13" "/opt/homebrew/bin/python3.12" "/opt/homebrew/bin/python3.11" \
    "/opt/homebrew/bin/python3" "/usr/local/bin/python3" \
    "$HOME/miniconda3/bin/python3" "$HOME/miniforge3/bin/python3" "$HOME/anaconda3/bin/python3" \
    "$HOME/mambaforge/bin/python3" "/usr/bin/python3"; do
    [ -x "$py" ] || continue
    if "$py" -c "import sys; assert sys.version_info >= ($maj,$minor)" 2>/dev/null; then
      export PATH="$(dirname "$py"):$PATH"
      echo "$py"; return 0
    fi
  done
  return 1
}
