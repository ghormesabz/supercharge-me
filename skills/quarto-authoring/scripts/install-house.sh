#!/usr/bin/env bash
# Installs the house format into a folder: <target>/_extensions/house/
#   install-house.sh <target-dir> [--force]
# Fails loud. It never replaces a different existing copy without --force.
set -euo pipefail

target="${1:-}"
force=0
[ "${2:-}" = "--force" ] && force=1

if [ -z "$target" ]; then
  echo "usage: install-house.sh <target-dir> [--force]" >&2
  exit 2
fi

src="$(cd "$(dirname "$0")/.." && pwd)/assets/_extensions/house"
dest="$target/_extensions/house"

if [ ! -d "$src" ]; then
  echo "house format missing at $src" >&2
  exit 1
fi

if [ -e "$dest" ] && [ "$force" -ne 1 ]; then
  if diff -rq "$src" "$dest" >/dev/null 2>&1; then
    echo "already installed and identical: $dest"
    exit 0
  fi
  echo "refusing to replace a different $dest (pass --force to replace)" >&2
  exit 1
fi

mkdir -p "$target/_extensions"
rm -rf "$dest"
cp -R "$src" "$dest"
echo "installed: $dest"
