#!/usr/bin/env bash
# Screenshots every .fig in a rendered spec, one PNG per figure, in page order.
#   figure-shots.sh HTML_FILE [OUT_DIR]
# Prints the folder holding fig1.png, fig2.png, ... Exits 1 with a message when
# no browser is found or a screenshot fails.
# Headless Chrome ignores scroll position, so each figure is shifted to the top
# of a scratch copy of the page before the screenshot.
set -euo pipefail

html="${1:-}"
if [ -z "$html" ] || [ ! -f "$html" ]; then
  echo "usage: figure-shots.sh HTML_FILE [OUT_DIR]" >&2
  exit 2
fi

out="${2:-$(mktemp -d)}"
mkdir -p "$out"

chrome=""
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif command -v google-chrome >/dev/null 2>&1; then
  chrome="google-chrome"
elif command -v chromium >/dev/null 2>&1; then
  chrome="chromium"
fi

if [ -z "$chrome" ]; then
  echo "no Chrome or Chromium found. Skip the figure check and say so in the report." >&2
  exit 1
fi

n_figs="$(grep -o 'class="fig[ "]' "$html" | wc -l | tr -d ' ')"
if [ "$n_figs" -eq 0 ]; then
  echo "no figures found in $html" >&2
  exit 1
fi

n=1
while [ "$n" -le "$n_figs" ]; do
  idx=$((n - 1))
  sed "s|</body>|<script>addEventListener('load',()=>{const f=document.querySelectorAll('.fig')[$idx];document.body.style.marginTop=(20-f.getBoundingClientRect().top-scrollY)+'px'})</script></body>|" "$html" > "$out/fig$n.html"
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1400 \
    --screenshot="$out/fig$n.png" "file://$out/fig$n.html" >/dev/null 2>&1 || true
  if [ ! -f "$out/fig$n.png" ]; then
    echo "screenshot $n failed" >&2
    exit 1
  fi
  rm -f "$out/fig$n.html"
  n=$((n + 1))
done

echo "$out"
