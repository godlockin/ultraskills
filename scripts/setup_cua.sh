#!/usr/bin/env bash
# setup_cua.sh — Create Python venv and install trycua/cua packages
#
# Called by:
#   - setup.sh (project init)
#   - Manually: ./scripts/setup_cua.sh [--force]
#
# Behavior:
#   1. Detect Python 3.12 or 3.13 (cua requires >=3.12,<3.14)
#   2. Create external/cua/.venv with that Python
#   3. Install cua + cua-mcp-server (MIT only — NO [omni] extra!)
#   4. Verify cua-mcp-server is importable
#
# Failure handling: any step fails → exit 1, leaves no half-state

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CUA_DIR="$REPO_ROOT/external/cua"
VENV_DIR="$CUA_DIR/.venv"
FORCE=0

[[ "${1:-}" == "--force" ]] && FORCE=1

# ── Helpers ───────────────────────────────────────────────────────────────────
detect_python() {
  # cua requires >=3.12,<3.14. Prefer 3.13, fall back to 3.12.
  for ver in 3.13 3.12; do
    if command -v "python$ver" >/dev/null 2>&1; then
      echo "python$ver"
      return 0
    fi
  done
  return 1
}

uv_or_pip() {
  # Prefer `uv` (fast, handles resolution); fall back to `python -m pip`
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
    uv)
      # --python pins the venv's interpreter; --no-managed-python uses system Python
      uv pip install --python "$VENV_DIR/bin/python" "$@"
      ;;
    pip)
      "$VENV_DIR/bin/pip" install "$@"
      ;;
  esac
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
  # 1. Submodule must be cloned
  if [[ ! -d "$CUA_DIR/libs/python/cua" ]]; then
    echo "✗ external/cua/ submodule not initialized"
    echo "  Run: git submodule update --init --recursive"
    return 1
  fi

  # 2. Already installed?
  if [[ -x "$VENV_DIR/bin/cua-mcp-server" && $FORCE -eq 0 ]]; then
    echo "✓ cua already installed: $VENV_DIR"
    "$VENV_DIR/bin/cua-mcp-server" --help 2>&1 | head -3 || true
    return 0
  fi

  # 3. Detect Python
  local py_bin
  if ! py_bin=$(detect_python); then
    echo "✗ Python 3.12 or 3.13 not found in PATH"
    echo "  Install: brew install python@3.12   # or python@3.13"
    return 1
  fi
  echo "→ Using Python: $py_bin"

  # 4. Detect installer
  local installer
  if ! installer=$(uv_or_pip); then
    echo "✗ Neither 'uv' nor 'pip' available"
    echo "  Install: brew install uv  # recommended"
    return 1
  fi
  echo "→ Installer: $installer"

  # 5. Create venv
  echo "→ Creating venv at $VENV_DIR"
  if [[ "$installer" == "uv" ]]; then
    uv venv --python "$py_bin" "$VENV_DIR"
  else
    "$py_bin" -m venv "$VENV_DIR"
  fi

  # 6. Upgrade pip / uv-managed installer
  echo "→ Upgrading pip"
  install_with "$installer" "$py_bin" --upgrade pip wheel setuptools 2>/dev/null || true

  # 7. Install cua packages (MIT only — NO [omni] extra!)
  echo "→ Installing cua + cua-mcp-server (MIT core, no AGPL [omni] extra)"
  install_with "$installer" "$py_bin" \
    "$CUA_DIR/libs/python/cua" \
    "$CUA_DIR/libs/python/mcp-server" || {
      echo "✗ pip install failed"
      echo "  cua pyproject requires Python <3.14. If using 3.14, downgrade to 3.12 or 3.13."
      return 1
    }

  # 8. Verify
  if [[ ! -x "$VENV_DIR/bin/cua-mcp-server" ]]; then
    echo "✗ cua-mcp-server not found in venv after install"
    return 1
  fi

  echo ""
  echo "✓ Installed: $VENV_DIR/bin/cua-mcp-server"
  echo ""
  echo "=== Next steps ==="
  echo "  1. Register MCP server:"
  echo "       bash devops/cua-mcp/install-global-mcp.sh"
  echo "  2. Restart Claude Code"
  echo "  3. Verify: python3 devops/cua-mcp/scripts/check_install.py"
  echo ""
  echo "=== AGPL warning ==="
  echo "  Do NOT run: pip install cua-agent[omni]"
  echo "  This pulls in ultralytics/AGPL-3.0 and contaminates the project."
}

main "$@"
