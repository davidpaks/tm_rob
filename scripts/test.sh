#!/usr/bin/env bash
# Lefordítja és a teszt.yaml alapján szimulálja a megadott feladatokat.
# Használat: scripts/test.sh feladatok/01-beepitett-led [további feladatok...]
# Paraméter nélkül az összes feladatot futtatja.
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -eq 0 ] && set -- feladatok/*/
for d in "$@"; do
  d=$(realpath "$d")
  echo "== $(basename "$d")"
  scripts/build.sh "$d" >/dev/null
  wokwi-cli "$d" --scenario "$d/teszt.yaml" --timeout 15000
done
