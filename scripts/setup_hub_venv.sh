#!/usr/bin/env bash
# setup_hub_venv.sh — Create Python venv and install mcp SDK for ultraskills-hub
#
# Called by:
#   - setup.sh (project init, after hub install)
#   - Manually: ./scripts/setup_hub_venv.sh [--force]
#
# Mirrors scripts/setup_cua.sh pattern.
# Required by devops/ultraskills-hub/mcp_server.py (imports mcp.server).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HUB_DIR="$REPO_ROOT/devops/ultraskills-hub"
VENV_DIR="$HUB_DIR/.venv"
FORCE=0

[[ "${1:-}" == "--force" ]] && FORCE=1

detect_python() {
  for ver in 3.13 3.12 3.11; do
    if command -v "python$ver" >/dev/null 2>&1; then
      echo "python$ver"
      return 0
    fi
  done
  # Fallback to default python3
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi
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
  if [ ! -f "$HUB_DIR/mcp_server.py" ]; then
    echo "✗ devops/ultraskills-hub/mcp_server.py not found"
    return 1
  fi

  # Already installed?
  if [ -x "$VENV_DIR/bin/python" ] && [[ "$VENV_DIR/bin/python" -nt "$HUB_DIR/mcp_server.py" ]] && [ $FORCE -eq 0 ]; then
    if "$VENV_DIR/bin/python" -c "import mcp" 2>/dev/null; then
      echo "✓ hub venv already installed: $VENV_DIR"
      return 0
    fi
  fi

  local py_bin
  if ! py_bin=$(detect_python); then
    echo "✗ Python 3.11+ not found in PATH"
    return 1
  fi
  echo "→ Using Python: $py_bin"

  local installer
  if ! installer=$(uv_or_pip); then
    echo "✗ Neither 'uv' nor 'pip' available"
    return 1
  fi
  echo "→ Installer: $installer"

  echo "→ Creating venv at $VENV_DIR"
  if [[ "$installer" == "uv" ]]; then
    uv venv --python "$py_bin" "$VENV_DIR"
  else
    "$py_bin" -m venv "$VENV_DIR"
  fi

  echo "→ Upgrading pip"
  install_with "$installer" "$py_bin" --upgrade pip wheel setuptools 2>/dev/null || true

  echo "→ Installing mcp SDK"
  install_with "$installer" "$py_bin" -r "$HUB_DIR/requirements.txt" || {
    echo "✗ pip install failed"
    return 1
  }

  if ! "$VENV_DIR/bin/python" -c "import mcp" 2>/dev/null; then
    echo "✗ mcp not importable after install"
    return 1
  fi

  echo ""
  echo "✓ Installed: $VENV_DIR/bin/python (with mcp)"
  echo ""
  echo "=== Next steps ==="
  echo "  Run ./setup.sh to re-register the MCP server with the venv python."
}

main "$@"