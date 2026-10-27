#!/usr/bin/env bash
# Lefordítja egy feladat sketch.ino-ját a feladat build/ mappájába.
# Használat: scripts/build.sh feladatok/01-beepitett-led
set -euo pipefail
dir=$(realpath "$1")
# Az arduino-cli csak akkor fordít, ha a mappa neve egyezik az .ino nevével.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/sketch"
cp "$dir/sketch.ino" "$tmp/sketch/"
arduino-cli compile --fqbn arduino:avr:uno --output-dir "$dir/build" "$tmp/sketch"
