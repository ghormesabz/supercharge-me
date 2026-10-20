#!/usr/bin/env bash
# Renders the worked example spec in a scratch folder and lists the output.
#   render-example.sh [OUT_DIR]
# Doubles as the smoke test for the house format, figures.css and render.sh.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
assets="$root/skills/spec-creator/assets"
out="${1:-$(mktemp -d)}"
mkdir -p "$out"

cp "$assets/example/spec.qmd" "$out/spec.qmd"
cp "$assets/figures.css" "$assets/tokens.css" "$assets/render.sh" "$out/"
bash "$root/skills/quarto-authoring/scripts/install-house.sh" "$out"
bash "$out/render.sh"

echo "rendered in: $out"
ls -1 "$out"/*.html
