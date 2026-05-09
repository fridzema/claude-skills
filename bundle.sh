#!/usr/bin/env bash
# Bundle skill source dirs into distributable .skill (zip) files.
# Usage: ./bundle.sh [skill-name ...]   (no args = all skills)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"
mkdir -p "$DIST"

bundle_one() {
  local name="$1"
  local src="$ROOT/$name"
  [[ -f "$src/SKILL.md" ]] || { echo "skip: $name (no SKILL.md)"; return; }
  local out="$DIST/$name.skill"
  rm -f "$out"
  (cd "$ROOT" && zip -qr "$out" "$name" -x "*.DS_Store")
  echo "built: $out"
}

if [[ $# -gt 0 ]]; then
  for n in "$@"; do bundle_one "$n"; done
else
  for d in "$ROOT"/*/; do
    name="$(basename "$d")"
    [[ "$name" == "dist" ]] && continue
    bundle_one "$name"
  done
fi
