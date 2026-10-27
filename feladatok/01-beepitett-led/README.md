# 01 – A beépített LED villogtatása

## Cél
Az első Arduino-program megírása: a lapra gyárilag szerelt LED villogtatása.

## Elvárt működés
A beépített LED (13-as láb, `LED_BUILTIN`) 1 másodpercig világít, majd 1 másodpercig nem, és ez ismétlődik.

## Magyarázat
- `setup()` egyszer fut le indításkor, a `loop()` utána folyamatosan ismétlődik.
- `pinMode(láb, OUTPUT)` kimenetté teszi a lábat.
- `digitalWrite(láb, HIGH/LOW)` be- vagy kikapcsolja a lábat (5 V / 0 V).
- `delay(ms)` a megadott ezredmásodpercig várakozik.
