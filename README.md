# Robotika – bevezető feladatok

Arduino Uno feladatok tanegységenként, mintamegoldással és bekötési ábrával. Az áramkörök a [Wokwi](https://wokwi.com) online szimulátorban is kipróbálhatók.

**A tananyag böngészőben: https://davidpaks.github.io/tm_rob/**

## Mi található az oldalon?

Minden feladatnál:

- a feladat leírása és az elvárt működés,
- az alkatrészlista,
- a bekötési ábra próbapanellel, az alkatrészek elhelyezése a próbapanelen és a vezetékek listája,
- a mintamegoldás színezett kóddal (másolás gombbal), valamint a **Wokwi-projekt** (.zip: `sketch.ino` + `diagram.json`; két Arduinós feladatnál Arduinónként külön projekt, mert a Wokwi egyszerre csak egy Arduinót szimulál).

Az oldal világos és sötét módban is olvasható; a jobb felső gombbal kézzel is váltható.

## Javasolt menet egy feladathoz

1. A feladat leírásának és a bekötésnek az áttekintése.
2. Az áramkör összeállítása (Wokwi-ban vagy valódi eszközökkel) és a program megírása.
3. Összevetés a mintamegoldással.

## Tanegységek

| Tanegység | Téma | Feladatok |
|---|---|---|
| 1. | LED-ek vezérlése | [Beépített LED](feladatok/01-beepitett-led/), [Külső LED](feladatok/02-kulso-led/), [Két LED felváltva](feladatok/03-ket-led-felvaltva/), [Közlekedési lámpa](feladatok/04-kozlekedesi-lampa/) |
| 2. | 7 szegmenses kijelző | [Szám kiírása](feladatok/05-hetszegmens-szam/), [Számlálás 0-tól 9-ig](feladatok/06-hetszegmens-szamlalo/) |
| 3. | I2C-s LCD kijelző és ultrahangos távolságmérő | [Szöveg kiírása LCD-re](feladatok/07-lcd-kiiras/), [Távolságmérés](feladatok/08-tavolsagmero/), [Mérési tartomány figyelése](feladatok/09-tavolsagmero-tartomany/) (önálló feladat) |
| 4. | Nyomógombok | [Gomb és LED](feladatok/10-gomb-led/), [Gomb kapcsolóként](feladatok/11-gomb-kapcsolo/), [Két gomb](feladatok/12-ket-gomb/), [Fel-le számláló](feladatok/13-fel-le-szamlalo/) (gyakorló feladatok) |
| 5. | Soros kommunikáció (UART) két Arduino között | [Szám küldése soros vonalon](feladatok/14-soros-szam/), [Potméter és PWM két Arduinóval](feladatok/15-potmeter-pwm/) |

## A repository felépítése

Minden feladat a [`feladatok`](feladatok) mappában, saját almappában van:

- `README.md` – a feladat leírása,
- `sketch.ino` – mintamegoldás (két Arduinós feladatnál Arduinónként külön almappában, pl. `kuldo/kuldo.ino` és `fogado/fogado.ino`),
- `diagram.json` – az áramkör (Wokwi-formátum),
- `teszt.yaml` – automatikus teszt a Wokwi-szimulátorhoz (két Arduinós feladatnál a programok mellett),
- `wokwi.toml` – Wokwi projektbeállítás,
- `referencia/` – (ha van) a kijelző várt képe a teszthez.

A tanegységek sorrendjét a [`tananyag.json`](tananyag.json) adja meg; ebből és a feladatmappákból a `.github/scripts/build_site.py` állítja össze a weboldalt minden `main`-re pusholáskor.
