#!/usr/bin/env bash
# Lefordítja egy feladat programját a feladat build/ mappájába.
# Egy Arduinós feladat: sketch.ino -> build/
# Két Arduinós feladat: minden almappa saját programja (pl. kuldo/kuldo.ino) -> build/kuldo/
# Használat: scripts/build.sh feladatok/01-beepitett-led
set -euo pipefail
dir=$(realpath "$1")
if [ -f "$dir/sketch.ino" ]; then
  # Az arduino-cli csak akkor fordít, ha a mappa neve egyezik az .ino nevével.
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  mkdir "$tmp/sketch"
  cp "$dir/sketch.ino" "$tmp/sketch/"
  arduino-cli compile --fqbn arduino:avr:uno --output-dir "$dir/build" "$tmp/sketch"
else
  for prog in "$dir"/*/; do
    name=$(basename "$prog")
    [ -f "$prog/$name.ino" ] || continue
    arduino-cli compile --fqbn arduino:avr:uno --output-dir "$dir/build/$name" "$prog"
  done
fi
