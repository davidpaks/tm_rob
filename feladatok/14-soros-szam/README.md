# 14 – Szám küldése soros vonalon

## Cél
Két Arduino összekötése soros (UART) kommunikációval: a küldő Arduino számokat küld, a fogadó Arduino fogadja és kiírja őket a soros monitorra.

## Elvárt működés
- A küldő (jobb oldali) Arduino másodpercenként elküld egy számot: 0, 1, 2, …
- A fogadó (bal oldali) Arduino minden kapott számra kiír egy sort a saját soros monitorára, például: `Kapott szám: 5`.

## Magyarázat
- Bekötés: a küldő TX (1-es) lába a fogadó RX (0-s) lábára, a küldő GND-je a fogadó GND-jére kerül. A közös GND nélkül a két panel jelszintjének nincs közös viszonyítási pontja.
- Két program tartozik a feladathoz: `kuldo/kuldo.ino` a küldőre, `fogado/fogado.ino` a fogadóra kerül.
- Program feltöltése előtt a fogadó 0-s lábán lévő vezetéket ki kell húzni, mert az RX láb egyben az USB-kapcsolat fogadó vonala is. Feltöltés után vissza lehet dugni.
- `Serial.begin(9600)` elindítja a soros portot 9600 bit/s sebességgel. A két oldalon ugyanakkora sebességet kell beállítani.
- `Serial.println(szam)` a számot szövegként, számjegyenként egy-egy karakterrel küldi el, a végén sorvége jellel. Ebből tudja a fogadó, hol ér véget egy szám.
- `Serial.available()` megadja, hány beolvasásra váró karakter érkezett; ha 0, még nem jött adat. `Serial.readStringUntil('\n')` a sor végéig olvas, a `toInt()` pedig a kapott szöveget számmá alakítja.
- A fogadó a saját TX lábán, az USB-n át ír a soros monitorra; a küldő felé nem megy vissza adat, mert a fogadó TX lába nincs bekötve. Az elküldött számok a küldő soros monitorán is látszanak, mert a küldő TX lába az USB felé is továbbít.
- Wokwi: a szimulátor egyszerre csak egy Arduinót futtat, ezért mindkét programhoz külön Wokwi-projekt tartozik. A küldő projektjében az elküldött számok a soros monitoron jelennek meg; a fogadó projektjében a küldő helyett a soros monitor beviteli mezőjébe lehet számot írni.
