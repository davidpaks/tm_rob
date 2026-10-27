# 04 – Közlekedési lámpa

## Cél
Három LED vezérlése egy közlekedési lámpa fázisai szerint.

## Alkatrészek
- Arduino Uno
- 3 db LED (piros, sárga, zöld)
- 3 db 220 Ω-os ellenállás

## Bekötés
- 10-es láb → 220 Ω → piros LED anódja; katód → GND
- 9-es láb → 220 Ω → sárga LED anódja; katód → GND
- 8-as láb → 220 Ω → zöld LED anódja; katód → GND

## Elvárt működés
| Fázis | Piros | Sárga | Zöld | Időtartam |
|---|---|---|---|---|
| 1 | ● | | | 3 s |
| 2 | ● | ● | | 1 s |
| 3 | | | ● | 3 s |
| 4 | | ● | | 1 s |

A 4. fázis után a ciklus újraindul.
