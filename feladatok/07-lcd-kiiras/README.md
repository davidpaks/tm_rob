# 07 – Szöveg kiírása LCD kijelzőre

## Cél
Egy I2C-s 16x2-es LCD kijelző bekötése és szöveg kiírása rá.

## Elvárt működés
Az első sorban a „Hello, Robotika!” felirat látható, a második sorban az indítás óta eltelt másodpercek száma, másodpercenként frissülve.

## Magyarázat
- Az I2C-s kijelzőnek csak négy lába van: GND, VCC (5 V), SDA (adat) és SCL (órajel). Az Arduino Unón az SDA az A4, az SCL az A5 láb.
- A tápot a próbapanel alsó sínjei osztják el: a + sín az Arduino 5V, a − sín a GND lábára csatlakozik.
- A program a `LiquidCrystal I2C` könyvtárat használja (Arduino IDE: Eszközök → Könyvtárak kezelése). A kijelző I2C-címe általában `0x27`.
- `lcd.setCursor(oszlop, sor)` a kurzort helyezi el (a számozás 0-tól indul), `lcd.print()` a kurzortól kezdve ír.
- A kijelző nem tud ékezetes betűket megjeleníteni, ezért a szövegek ékezet nélküliek.
