# 13 – Fel-le számláló

## Cél
Gyakorló feladat: két nyomógombbal változtatni a 7 szegmenses kijelzőn látható számot; az egyik gomb növeli, a másik csökkenti.

## Elvárt működés
- Induláskor a kijelző 0-t mutat.
- A zöld gomb (2-es láb) minden lenyomására a szám eggyel nő, a piros gomb (3-as láb) minden lenyomására eggyel csökken.
- A 9 után ismét 0 következik, a 0 előtt pedig 9 (körbe-körbe számol).
- Egy lenyomás pontosan egy lépés, akkor is, ha a gombot hosszan nyomva tartják.

## Magyarázat
- A kijelző bekötése és a `display()` függvény megegyezik a 6. feladatéval; a két gomb a 4. tanegység szerint, INPUT_PULLUP módban van bekötve.
- A 12. feladat egyszerű megoldása itt nem elég: ha a program csak azt nézné, hogy a gomb le van-e nyomva, a szám a nyomva tartás alatt folyamatosan pörögne. A lenyomás pillanatát kell érzékelni, a pergést pedig ki kell szűrni, ahogy a 11. feladatban.
- Mivel két gombra kell ugyanaz a pergésmentesítés, a gombonkénti adatok (`stabilAllapot`, `elozoNyers`, `utolsoValtas`) kételemű tömbökben vannak, és a `lenyomtak()` függvény a gomb sorszámát kapja meg. A függvény `bool` értéket ad vissza: `true`-t, ha a gombot éppen most nyomták le.
- Az alkatrészek szűkös hely miatt kisebb, 6×6 mm-es nyomógombok, és a piros gomb jele egy átkötéssel a 29. oszlopba kerül, így a vezetékek nem keresztezik egymást.
