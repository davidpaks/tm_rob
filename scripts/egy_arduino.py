"""Két Arduinós feladat diagram.json-jából olyan változatot ír ki, amelyben a megadott
Arduino áll elöl. A Wokwi egy szimulációban csak az első Arduinót futtatja.
Használat: python3 scripts/egy_arduino.py feladatok/14-soros-szam/diagram.json kuldo > ki.json"""
import json
import sys

diagram = json.load(open(sys.argv[1], encoding="utf-8"))
board = next(p for p in diagram["parts"] if p["id"] == sys.argv[2])
diagram["parts"] = [board] + [p for p in diagram["parts"] if p is not board]
json.dump(diagram, sys.stdout, ensure_ascii=False, indent=2)
print()
