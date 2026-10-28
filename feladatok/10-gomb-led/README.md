# 10 – Nyomógomb és LED

## Cél
Egy nyomógomb bekötése és beolvasása: a beépített LED addig világít, amíg a gomb le van nyomva.

## Elvárt működés
Lenyomott gombnál a beépített LED világít, felengedett gombnál nem.

## Magyarázat
- A gomb a 2-es láb és a GND közé van kötve, a próbapanel középső árka fölött. Lenyomáskor a két oldala összeér.
- `pinMode(GOMB_PIN, INPUT_PULLUP)` bemenetté teszi a lábat, és bekapcsolja az Arduino belső felhúzó ellenállását. Így a láb felengedett gombnál HIGH, lenyomott gombnál LOW (fordított logika), külső ellenállás nélkül.
- `digitalRead(láb)` a láb állapotát adja vissza (HIGH vagy LOW).
