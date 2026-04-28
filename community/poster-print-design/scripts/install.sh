#!/usr/bin/env bash
set -euo pipefail
echo "==> poster-print-design install"
command -v node >/dev/null || { command -v brew && brew install node || { echo "install node first"; exit 1; }; }
npm i --no-save playwright >/dev/null 2>&1 || npm i playwright
npx playwright install chromium
echo "✓ done"
