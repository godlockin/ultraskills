#!/usr/bin/env bash
# icon-system — search / fetch / batch icons via Iconify
set -euo pipefail

usage() {
  cat <<EOF
icon-system — Iconify-powered icon ops

Commands:
  search <query>                       search 220k icons
  fetch  <prefix:name> [-o file.svg]   fetch one SVG
  batch  <p:n,p:n,...> --out <dir> [--format svg|react-tsx|vue]
  sprite <prefix> --names a,b,c -o sprite.svg

Examples:
  icon.sh search "user heart"
  icon.sh fetch lucide:heart -o heart.svg
  icon.sh batch lucide:user,lucide:bell --out icons/ --format react-tsx
EOF
}

cmd="${1:-}"; shift || true

case "$cmd" in
  search)
    [ -z "${1:-}" ] && { usage; exit 1; }
    Q="$(echo "$@" | sed 's/ /+/g')"
    curl -sS "https://api.iconify.design/search?query=$Q&limit=32" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); [print(i) for i in d.get('icons',[])]"
    ;;
  fetch)
    ID="${1:-}"; shift || true
    OUT=""
    while [ $# -gt 0 ]; do case "$1" in -o) OUT="$2"; shift 2;; *) shift;; esac; done
    [ -z "$ID" ] && { usage; exit 1; }
    PREFIX="${ID%%:*}"; NAME="${ID##*:}"
    URL="https://api.iconify.design/$PREFIX/$NAME.svg"
    if [ -n "$OUT" ]; then curl -sS "$URL" -o "$OUT" && echo "✓ → $OUT"
    else curl -sS "$URL"; fi
    ;;
  batch)
    IDS="${1:-}"; shift || true
    OUTDIR=""; FORMAT="svg"
    while [ $# -gt 0 ]; do case "$1" in
      --out) OUTDIR="$2"; shift 2;;
      --format) FORMAT="$2"; shift 2;;
      *) shift;; esac; done
    [ -z "$IDS" ] || [ -z "$OUTDIR" ] && { usage; exit 1; }
    mkdir -p "$OUTDIR"
    IFS=',' read -ra ARR <<< "$IDS"
    for ID in "${ARR[@]}"; do
      PREFIX="${ID%%:*}"; NAME="${ID##*:}"
      SVG="$(curl -sS "https://api.iconify.design/$PREFIX/$NAME.svg")"
      case "$FORMAT" in
        svg) echo "$SVG" > "$OUTDIR/$NAME.svg";;
        react-tsx)
          cap="$(echo "$NAME" | python3 -c "import sys; n=sys.stdin.read().strip(); print(''.join(p.capitalize() for p in n.split('-')))")"
          inner="$(echo "$SVG" | sed -E 's/<svg[^>]*>//; s|</svg>||')"
          cat > "$OUTDIR/${cap}.tsx" <<TSX
import * as React from "react";
export const ${cap}Icon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
       viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth={1.5} {...props}>
    ${inner}
  </svg>
);
TSX
          ;;
        vue)
          cap="$(echo "$NAME" | python3 -c "import sys; n=sys.stdin.read().strip(); print(''.join(p.capitalize() for p in n.split('-')))")"
          cat > "$OUTDIR/${cap}.vue" <<VUE
<template>$SVG</template>
<script setup lang="ts">
defineOptions({ name: '${cap}Icon' });
</script>
VUE
          ;;
      esac
      echo "  ✓ $ID → $OUTDIR/$NAME"
    done
    ;;
  sprite)
    PREFIX="${1:-}"; shift || true
    NAMES=""; OUT="sprite.svg"
    while [ $# -gt 0 ]; do case "$1" in
      --names) NAMES="$2"; shift 2;;
      -o) OUT="$2"; shift 2;;
      *) shift;; esac; done
    [ -z "$PREFIX" ] || [ -z "$NAMES" ] && { usage; exit 1; }
    {
      echo '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">'
      IFS=',' read -ra ARR <<< "$NAMES"
      for n in "${ARR[@]}"; do
        SVG="$(curl -sS "https://api.iconify.design/$PREFIX/$n.svg")"
        inner="$(echo "$SVG" | sed -E 's/<svg[^>]*>//; s|</svg>||')"
        echo "  <symbol id=\"$n\" viewBox=\"0 0 24 24\">$inner</symbol>"
      done
      echo '</svg>'
    } > "$OUT"
    echo "✓ sprite → $OUT (use: <svg><use href=\"$OUT#name\"/></svg>)"
    ;;
  *) usage; exit 1;;
esac
