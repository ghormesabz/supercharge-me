#!/usr/bin/env bash
# Renders spec.qmd beside this script.
#   spec-draft: true   -> design-review.html  (Part A and Part B, draft banner)
#   spec-draft: false  -> design-sheet.html   (Part A only)
#                         build-spec.html     (Part A and Part B)
# Fails loud: any missing tool or render error stops the script.
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v quarto >/dev/null 2>&1; then
  echo "quarto not found. Install Quarto 1.7 or later: https://quarto.org/docs/get-started/" >&2
  exit 1
fi

if [ ! -f spec.qmd ]; then
  echo "spec.qmd not found in $(pwd)" >&2
  exit 1
fi

if grep -q -E '^spec-draft:[[:space:]]*true' spec.qmd; then
  quarto render spec.qmd -M builder:true --output design-review.html
else
  quarto render spec.qmd --output design-sheet.html
  quarto render spec.qmd -M builder:true --output build-spec.html
  rm -f design-review.html
fi
