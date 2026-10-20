#!/usr/bin/env bash
# Checks the tools mahan-skills needs and prints only problems.
#   preflight.sh          Hook mode. Required problems only. Always exits 0.
#   preflight.sh --full   Also prints optional-tool notes. Exits 1 if a required tool is missing.
# Written for bash 3.2 (macOS default).
set -u

full=0
[ "${1:-}" = "--full" ] && full=1

required_problems=""
optional_notes=""

add_required() { required_problems="${required_problems}mahan-skills: $1
"; }
add_optional() { optional_notes="${optional_notes}mahan-skills (optional): $1
"; }

if command -v quarto >/dev/null 2>&1; then
  version="$(quarto --version 2>/dev/null | head -n 1)"
  major="${version%%.*}"
  rest="${version#*.}"
  minor="${rest%%.*}"
  case "${major}${minor}" in
    ''|*[!0-9]*) add_required "cannot read the Quarto version (got '${version}'). spec-creator and quarto-authoring need Quarto 1.7 or later." ;;
    *)
      if [ "$major" -lt 1 ] || { [ "$major" -eq 1 ] && [ "$minor" -lt 7 ]; }; then
        add_required "Quarto ${version} is too old. spec-creator and quarto-authoring need 1.7 or later: https://quarto.org/docs/get-started/"
      fi
      ;;
  esac
else
  add_required "Quarto not found. spec-creator and quarto-authoring need Quarto 1.7 or later: https://quarto.org/docs/get-started/"
fi

command -v git >/dev/null 2>&1 || add_required "git not found. spec-creator tags the draft with git."
command -v python3 >/dev/null 2>&1 || add_required "python3 not found. handoff and its session-start hook need Python 3.9 or later."

if [ "$full" -eq 1 ]; then
  command -v uv >/dev/null 2>&1 || add_optional "uv not found. Needed only to init a Python project at the commit step."
  if [ ! -d "/Applications/Google Chrome.app" ] && ! command -v google-chrome >/dev/null 2>&1 && ! command -v chromium >/dev/null 2>&1; then
    add_optional "no Chrome or Chromium found. The figure check will be skipped."
  fi
fi

[ -n "$required_problems" ] && printf '%s' "$required_problems"
[ "$full" -eq 1 ] && [ -n "$optional_notes" ] && printf '%s' "$optional_notes"

if [ "$full" -eq 1 ] && [ -n "$required_problems" ]; then
  exit 1
fi
exit 0
