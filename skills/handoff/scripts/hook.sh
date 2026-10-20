#!/usr/bin/env bash
# SessionStart hook: runs `handoff.py hook` with the hook's stdin.
# Exits 0 silently when python3 is missing, or is the macOS /usr/bin stub, which
# opens an install dialog until the Command Line Tools are installed.
# Written for bash 3.2 (macOS default).
py="$(command -v python3)" || exit 0
if [ "$py" = /usr/bin/python3 ] && ! xcode-select -p >/dev/null 2>&1; then
  exit 0
fi
exec python3 "$(dirname "$0")/handoff.py" hook
