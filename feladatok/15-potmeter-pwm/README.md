# 15 – Potméter és PWM két Arduinóval

## Cél
A küldő Arduino a potméter állását olvassa, és soros vonalon elküldi; a fogadó Arduino a kapott értékkel PWM-mel állítja egy külső LED fényerejét.

## Elvárt működés
- A küldő (jobb oldali) Arduino tizedmásodpercenként elküldi a potméter állását, egy 0 és 1023 közötti számot.
- A potméter tekerésével változik a fogadó (bal oldali) Arduinóra kötött LED fényereje: az egyik végállásban nem világít, a másikban teljes fényerővel világít.
- A fogadó soros monitorán a beállított fényerő (0–255) látszik.

## Magyarázat
- A két Arduino összekötése a 14. feladatéval egyezik: küldő TX (1) → fogadó RX (0). A közös GND-t itt a két próbapanel összekötött − sínje adja. Feltöltés előtt a fogadó 0-s lábán lévő vezetéket ki kell húzni.
- Potméter: a két szélső lába 5 V-ra és GND-re, a középső lába (csúszka) az A0 analóg bemenetre kerül. A csúszkán a tekerés szerint 0 és 5 V közötti feszültség jelenik meg, ezt az `analogRead()` 0–1023 közötti számmá alakítja.
- PWM (impulzusszélesség-moduláció): az `analogWrite()` másodpercenként több százszor ki-be kapcsolja a lábat. A bekapcsolt idő aránya (kitöltés) 0 és 255 között állítható, ennek megfelelően halványabbnak vagy fényesebbnek látszik a LED. Erre csak a `~` jelű lábak (3, 5, 6, 9, 10, 11) képesek.
- `map(ertek, 0, 1023, 0, 255)` a 0–1023 tartományból 0–255 tartományba számolja át az értéket.
- A LED bekötése a 2. feladatéval egyezik (220 Ω-os előtétellenállás), csak a 9-es lábon.
- Wokwi: mindkét programhoz külön Wokwi-projekt tartozik. A küldő projektjében a potméter tekerésekor a küldött érték a soros monitoron látszik; a fogadó projektjében a soros monitorba írt 0 és 1023 közötti számmal lehet kipróbálni.
