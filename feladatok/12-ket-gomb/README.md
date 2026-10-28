# 12 – Két nyomógomb

## Cél
Gyakorló feladat: két gombbal vezérelni a beépített LED-et; az egyik felkapcsolja, a másik lekapcsolja.

## Elvárt működés
- A zöld gomb (2-es láb) lenyomására a LED felkapcsol, és felengedés után is világít marad.
- A piros gomb (3-as láb) lenyomására a LED lekapcsol.
- Ugyanazt a gombot többször megnyomva a LED állapota nem változik.

## Magyarázat
- Mindkét gomb az előző feladatok szerint, INPUT_PULLUP módban van bekötve; a GND oldaluk a próbapanel alsó − sínjére kerül.
- Itt nincs szükség az előző állapot figyelésére és pergésmentesítésre: a „be” gomb akárhányszor kapcsolja be a LED-et, az eredmény ugyanaz.
