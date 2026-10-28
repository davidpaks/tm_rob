#!/usr/bin/env bash
# Lefordítja és a teszt.yaml alapján szimulálja a megadott feladatokat.
# Két Arduinós feladatnál mindkét programot külön szimulálja (a Wokwi egyszerre csak egy
# Arduinót futtat); a másik Arduino helyett a soros monitor küld vagy fogad.
# Használat: scripts/test.sh feladatok/01-beepitett-led [további feladatok...]
# Paraméter nélkül az összes feladatot futtatja.
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -eq 0 ] && set -- feladatok/*/
for d in "$@"; do
  d=$(realpath "$d")
  echo "== $(basename "$d")"
  scripts/build.sh "$d" >/dev/null
  if [ -f "$d/sketch.ino" ]; then
    wokwi-cli "$d" --scenario "$d/teszt.yaml" --timeout 15000
    continue
  fi
  for t in "$d"/*/teszt.yaml; do
    prog=$(basename "$(dirname "$t")")
    b="$d/build/$prog"
    echo "-- $prog"
    python3 scripts/egy_arduino.py "$d/diagram.json" "$prog" > "$b/diagram.json"
    printf '[wokwi]\nversion = 1\nfirmware = "%s.ino.hex"\nelf = "%s.ino.elf"\n' "$prog" "$prog" > "$b/wokwi.toml"
    wokwi-cli "$b" --scenario "$t" --timeout 15000
  done
done
