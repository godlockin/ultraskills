#!/usr/bin/env bash
# setup_skillspector.sh — Create Python venv and install NVIDIA SkillSpector
#
# Called by:
#   - setup.sh (project init)
#   - Manually: ./devops/skill-security-scan/scripts/setup_skillspector.sh [--force]
#
# Mirrors scripts/setup_cua.sh. SkillSpector requires Python 3.12+.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SPECT_DIR="$REPO_ROOT/external/skillspector"
VENV_DIR="$SPECT_DIR/.venv"
FORCE=0

[[ "${1:-}" == "--force" ]] && FORCE=1

detect_python() {
  for ver in 3.14 3.13 3.12; do
    if command -v "python$ver" >/dev/null 2>&1; then
      echo "python$ver"
      return 0
    fi
  done
  return 1
}

uv_or_pip() {
  if command -v uv >/dev/null 2>&1; then
    echo "uv"
  elif python3 -m pip --version >/dev/null 2>&1; then
    echo "pip"
  else
    return 1
  fi
}

install_with() {
  local installer="$1"
  local py_bin="$2"
  shift 2
  case "$installer" in
    uv) uv pip install --python "$VENV_DIR/bin/python" "$@" ;;
    pip) "$VENV_DIR/bin/pip" install "$@" ;;
  esac
}

main() {
  if [[ ! -d "$SPECT_DIR/src/skillspector" ]]; then
    echo "✗ external/skillspector/ submodule not initialized"
    echo "  Run: git submodule update --init --recursive"
    return 1
  fi

  if [[ -x "$VENV_DIR/bin/skillspector" && $FORCE -eq 0 ]]; then
    echo "✓ skillspector already installed: $VENV_DIR"
    "$VENV_DIR/bin/skillspector" --version 2>&1 | head -1 || true
    return 0
  fi

  local py_bin
  py_bin=$(detect_python) || { echo "✗ Python 3.12+ not found"; return 1; }
  echo "→ Using Python: $py_bin"

  local installer
  installer=$(uv_or_pip) || { echo "✗ Need uv or pip"; return 1; }
  echo "→ Installer: $installer"

  echo "→ Creating venv at $VENV_DIR"
  if [[ "$installer" == "uv" ]]; then
    uv venv --python "$py_bin" "$VENV_DIR"
  else
    "$py_bin" -m venv "$VENV_DIR"
  fi

  echo "→ Upgrading pip"
  install_with "$installer" "$py_bin" --upgrade pip wheel setuptools 2>/dev/null || true

  echo "→ Installing skillspector (editable)"
  install_with "$installer" "$py_bin" -e "$SPECT_DIR" || {
    echo "✗ pip install failed"
    return 1
  }

  if [[ ! -x "$VENV_DIR/bin/skillspector" ]]; then
    echo "✗ skillspector binary not in venv after install"
    return 1
  fi

  echo ""
  echo "✓ Installed: $VENV_DIR/bin/skillspector"
  echo ""
  echo "Test:"
  echo "  python3 devops/skill-security-scan/scripts/health_gate.py community/remotion"
}

main "$@"
