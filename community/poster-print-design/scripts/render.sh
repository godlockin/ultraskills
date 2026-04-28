#!/usr/bin/env bash
# poster-print-design — render HTML to PNG/PDF via Playwright
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES="$SCRIPT_DIR/../templates"

usage() { cat <<EOF
poster render — html → png / pdf

  render.sh og     --title T [--subtitle S] [--author A] -o out.png
  render.sh quote  --quote Q [--author A] -o out.png
  render.sh custom <file.html> [--width N --height N | --size A4|A3] [--pdf] -o out.png
  render.sh batch  <template.html> --data data.json --out dir/

Options:
  --width / --height   default per template
  --size A4|A3         shorthand (96dpi sizes)
  --pdf                output PDF instead of PNG
EOF
}

CMD="${1:-}"; shift || true
[ -z "$CMD" ] && { usage; exit 1; }

# Defaults
W=1200; H=630; OUT="out.png"; PDF=0; HTML=""

resolve_size() {
  case "${1:-}" in
    A4) W=794; H=1123;;
    A3) W=1123; H=1587;;
    A4-print) W=2480; H=3508;;
    A3-print) W=3508; H=4961;;
  esac
}

render_html_to_file() {
  local html_file="$1" out="$2"
  node - <<JS
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: $W, height: $H }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto('file://' + require('path').resolve("$html_file"));
  await page.waitForLoadState('networkidle');
  ${PDF}
    ? await page.pdf({ path: "$out", width: '${W}px', height: '${H}px', printBackground: true })
    : await page.screenshot({ path: "$out", fullPage: false, omitBackground: false });
  await browser.close();
})();
JS
  echo "✓ → $out"
}

case "$CMD" in
  og)
    TITLE=""; SUB=""; AUTHOR=""; OUT="og.png"
    while [ $# -gt 0 ]; do case "$1" in
      --title) TITLE="$2"; shift 2;;
      --subtitle) SUB="$2"; shift 2;;
      --author) AUTHOR="$2"; shift 2;;
      -o) OUT="$2"; shift 2;;
      *) shift;; esac; done
    TMP="$(mktemp -t og.XXXXXX).html"
    sed -e "s|{{TITLE}}|${TITLE//|/\\|}|g" \
        -e "s|{{SUBTITLE}}|${SUB//|/\\|}|g" \
        -e "s|{{AUTHOR}}|${AUTHOR//|/\\|}|g" \
        "$TEMPLATES/og.html" > "$TMP"
    W=1200; H=630
    render_html_to_file "$TMP" "$OUT"
    rm -f "$TMP";;
  quote)
    QUOTE=""; AUTHOR=""; OUT="quote.png"
    while [ $# -gt 0 ]; do case "$1" in
      --quote) QUOTE="$2"; shift 2;;
      --author) AUTHOR="$2"; shift 2;;
      -o) OUT="$2"; shift 2;;
      *) shift;; esac; done
    TMP="$(mktemp -t quote.XXXXXX).html"
    sed -e "s|{{QUOTE}}|${QUOTE//|/\\|}|g" \
        -e "s|{{AUTHOR}}|${AUTHOR//|/\\|}|g" \
        "$TEMPLATES/quote.html" > "$TMP"
    W=1080; H=1080
    render_html_to_file "$TMP" "$OUT"
    rm -f "$TMP";;
  custom)
    HTML="${1:-}"; shift || true
    [ -z "$HTML" ] && { usage; exit 1; }
    while [ $# -gt 0 ]; do case "$1" in
      --width) W="$2"; shift 2;;
      --height) H="$2"; shift 2;;
      --size) resolve_size "$2"; shift 2;;
      --pdf) PDF=1; OUT="${OUT%.png}.pdf"; shift;;
      -o) OUT="$2"; shift 2;;
      *) shift;; esac; done
    render_html_to_file "$HTML" "$OUT";;
  batch)
    TPL="${1:-}"; shift || true
    DATA=""; OUTDIR="."
    while [ $# -gt 0 ]; do case "$1" in
      --data) DATA="$2"; shift 2;;
      --out) OUTDIR="$2"; shift 2;;
      *) shift;; esac; done
    [ -z "$TPL" ] || [ -z "$DATA" ] && { usage; exit 1; }
    mkdir -p "$OUTDIR"
    python3 - "$TPL" "$DATA" "$OUTDIR" <<'PY'
import sys, json, re, subprocess, os, tempfile
tpl, data_file, outdir = sys.argv[1:]
tpl_str = open(tpl).read()
items = json.load(open(data_file))
for i, item in enumerate(items):
    out = os.path.join(outdir, f"{item.get('slug', i)}.png")
    s = tpl_str
    for k,v in item.items():
        s = s.replace(f"{{{{{k.upper()}}}}}", str(v))
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
    tmp.write(s.encode()); tmp.close()
    subprocess.run(["bash", os.path.join(os.path.dirname(__file__), "render.sh"),
                    "custom", tmp.name, "-o", out], check=True)
    os.unlink(tmp.name)
PY
    ;;
  *) usage; exit 1;;
esac
