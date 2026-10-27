# 02 – Külső LED rákötése

## Cél
Egy külső LED bekötése előtétellenállással, és villogtatása a 8-as lábról.

## Alkatrészek
- Arduino Uno
- 1 db LED (piros)
- 1 db 220 Ω-os ellenállás

## Bekötés
- 8-as láb → 220 Ω-os ellenállás → LED anódja (hosszabb láb)
- LED katódja (rövidebb láb) → GND

## Elvárt működés
A LED 1 másodpercig világít, majd 1 másodpercig nem, és ez ismétlődik.

## Magyarázat
- Az ellenállás korlátozza az áramot, nélküle a LED vagy az Arduino lába tönkremehet.
- A LED-nek polaritása van: fordítva bekötve nem világít.
