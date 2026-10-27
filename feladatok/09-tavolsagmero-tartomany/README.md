# 09 – Távolságmérő a mérési tartomány figyelésével

## Cél
Az előző feladat továbbfejlesztése önálló feladatként: csak a szenzor mérési tartományába eső értékek kiírása, a mértékegység a távolságtól függően.

## Elvárt működés
- A HC-SR04 kb. 2 cm és 4 m között mér megbízhatóan. Ha a mért érték ezen kívül esik, a második sorban a „Kivul: 2cm-4m” felirat jelenik meg.
- 1 m alatt a távolság centiméterben látható (pl. „57 cm”).
- 1 m felett méterben, két tizedesjeggyel (pl. „2.51 m”).

## Magyarázat
- A tartomány határait érdemes konstansként megadni (`MIN_CM`, `MAX_CM`), így később egy helyen módosíthatók.
- Ha nem érkezik visszhang, a `pulseIn()` a megadott idő (itt 30 ms) után 0-t ad vissza; ilyenkor a távolság 0, ami szintén a tartományon kívül esik.
- `lcd.print(ertek, 2)` két tizedesjeggyel írja ki a számot.
- A szimulált szenzor néhány tized százalékkal többet mér, ezért pontosan 4 m-nél már a tartományon kívüli üzenet jelenhet meg; a valódi szenzor pontossága is hasonló.
