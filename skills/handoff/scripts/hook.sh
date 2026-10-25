#!/usr/bin/env bash
# SessionStart hook: runs `handoff.py hook` with the hook's stdin.
# Exits 0 silently when python3 is missing, is older than 3.9, or is the macOS /usr/bin
# stub, which opens an install dialog until the Command Line Tools are installed.
# Written for bash 3.2 (macOS default).
py="$(command -v python3)" || exit 0
if [ "$py" = /usr/bin/python3 ] && ! xcode-select -p >/dev/null 2>&1; then
  exit 0
fi
"$py" -c 'import sys; sys.exit(sys.version_info < (3, 9))' || exit 0
exec "$py" "$(dirname "$0")/handoff.py" hook
