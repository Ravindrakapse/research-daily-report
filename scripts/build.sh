#!/bin/bash
# Build a daily report PDF from Markdown.
# Usage: build.sh <input.md> "<Title>" "<Subtitle>" "<Author>" "<Date>" [extra-tight]
set -e
IN="$1"; TITLE="$2"; SUB="$3"; AUTHOR="$4"; DATE="$5"; TIGHT="$6"
DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="${IN%.md}"
python3 "$DIR/md2tex.py" "$IN" "$BASE.tex" "$TITLE" "$SUB" "$AUTHOR" "$DATE"
if [ -n "$TIGHT" ]; then
  sed -i.bak 's/top=0.6in,bottom=0.6in/top=0.5in,bottom=0.5in/; s/linespread{0.97}/linespread{0.96}/' "$BASE.tex" && rm -f "$BASE.tex.bak"
fi
tectonic "$BASE.tex" >/dev/null 2>&1
pdfinfo "$BASE.pdf" | grep Pages
