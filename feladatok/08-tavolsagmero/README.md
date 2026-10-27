# 08 – Távolságmérés ultrahangos szenzorral

## Cél
Egy HC-SR04 ultrahangos távolságmérő bekötése, és a mért távolság kiírása az LCD kijelzőre.

## Elvárt működés
Az LCD első sorában a „Tavolsag:” felirat, a második sorában a mért távolság látható centiméterben, félmásodpercenként frissülve.

## Magyarázat
- A szenzor a TRIG lábra adott 10 µs-os impulzus hatására ultrahangot bocsát ki, majd az ECHO lábon annyi ideig ad HIGH jelet, amennyi idő alatt a hang a tárgyig és vissza ért.
- A `pulseIn(ECHO_PIN, HIGH)` ezt az időt adja meg mikroszekundumban. A hang kb. 0,0343 cm-t tesz meg mikroszekundumonként; mivel oda-vissza utat tesz meg, a távolság: `ido * 0.0343 / 2`.
- A második sor kiírása előtt a sort 16 szóközzel törölni kell, különben egy rövidebb szám mögött ott maradna az előző érték vége.
- A Wokwi-szimulációban a távolság a szenzorra kattintva, csúszkával állítható.
