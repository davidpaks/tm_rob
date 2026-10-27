# 05 – Szám kiírása 7 szegmenses kijelzőre

## Cél
Egy függvény megírása, amely a paraméterként kapott számjegyet (0–9) megjeleníti a 7 szegmenses kijelzőn.

## Elvárt működés
A kijelzőn a programban megadott számjegy látható (a mintamegoldásban az 5). Másik szám a `display()` hívásában adható meg.

## Magyarázat
- A kijelző hét LED-szegmensből áll, ezek neve A-tól G-ig: A felül, majd az óramutató járása szerint B, C, D, E, F, középen G.
- Közös katódos kijelzőnél a szegmensek katódja közös lábon (COM) van, ez a GND-re kerül; egy szegmens akkor világít, ha a lábára HIGH jut.
- Minden szegmens saját 220 Ω-os előtétellenálláson keresztül kapcsolódik az Arduinóhoz, így mind egyformán világít.
- A `numArray` tömb 10 sora a 10 számjegy, 7 oszlopa a 7 szegmens állapota. A `display(szam)` a `szam`-adik sort írja ki a lábakra.
