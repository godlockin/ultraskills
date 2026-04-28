#!/usr/bin/env bash
# figma-to-code — REST API helper (also setup hint for MCP)
set -euo pipefail

usage() {
  cat <<EOF
figma-to-code — fetch Figma nodes / images / variables via REST

Env: FIGMA_ACCESS_TOKEN (Personal Access Token)

Usage:
  fetch.sh --file <FILE_KEY> --node <id>            # node JSON
  fetch.sh --file <FILE_KEY> --node <id> --format png|svg|pdf  # render
  fetch.sh --file <FILE_KEY> --variables             # design tokens
  fetch.sh --file <FILE_KEY> --components            # all components
  fetch.sh --url <figma_url>                         # auto-extract file+node

Options:
  -o, --output <path>   default stdout
  --scale <1|2|3|4>     image scale (default 2)
EOF
}

FILE_KEY=""
NODE_ID=""
URL=""
FORMAT=""
OUTPUT=""
SCALE="2"
MODE="node"

while [ $# -gt 0 ]; do
  case "$1" in
    --file) FILE_KEY="$2"; shift 2;;
    --node) NODE_ID="$2"; shift 2;;
    --url) URL="$2"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    --variables) MODE="variables"; shift;;
    --components) MODE="components"; shift;;
    --scale) SCALE="$2"; shift 2;;
    -o|--output) OUTPUT="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown: $1"; usage; exit 1;;
  esac
done

if [ -n "$URL" ]; then
  FILE_KEY="$(echo "$URL" | sed -nE 's|.*figma\.com/(design\|file)/([^/?]+).*|\2|p')"
  NODE_ID="$(echo "$URL" | sed -nE 's|.*[?&]node-id=([0-9]+-[0-9]+).*|\1|p' | tr '-' ':')"
fi

[ -z "${FIGMA_ACCESS_TOKEN:-}" ] && { echo "ERR: FIGMA_ACCESS_TOKEN not set"; exit 1; }
[ -z "$FILE_KEY" ] && { echo "ERR: --file or --url required"; exit 1; }

H=(-H "X-Figma-Token: $FIGMA_ACCESS_TOKEN")

run() {
  if [ -n "$OUTPUT" ]; then
    curl -sS "${H[@]}" "$@" -o "$OUTPUT"
    echo "✓ → $OUTPUT"
  else
    curl -sS "${H[@]}" "$@"
  fi
}

case "$MODE" in
  variables)
    run "https://api.figma.com/v1/files/$FILE_KEY/variables/local";;
  components)
    run "https://api.figma.com/v1/files/$FILE_KEY/components";;
  node)
    if [ -n "$FORMAT" ]; then
      [ -z "$NODE_ID" ] && { echo "ERR: --node required for image"; exit 1; }
      RESP="$(curl -sS "${H[@]}" "https://api.figma.com/v1/images/$FILE_KEY?ids=$NODE_ID&format=$FORMAT&scale=$SCALE")"
      IMG_URL="$(echo "$RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(list(d['images'].values())[0])")"
      [ -n "$OUTPUT" ] && curl -sSL "$IMG_URL" -o "$OUTPUT" && echo "✓ → $OUTPUT" \
        || echo "$IMG_URL"
    elif [ -n "$NODE_ID" ]; then
      run "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE_ID"
    else
      run "https://api.figma.com/v1/files/$FILE_KEY"
    fi
    ;;
esac
