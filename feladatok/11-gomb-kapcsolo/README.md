# 11 – Nyomógomb kapcsolóként

## Cél
A gomb minden lenyomására váltson a LED állapota: az első lenyomás felkapcsolja, a következő lekapcsolja.

## Elvárt működés
A beépített LED alapból nem világít. Egy gombnyomásra felkapcsol, és felengedés után is világít marad; a következő gombnyomásra lekapcsol.

## Magyarázat
- Nem az számít, hogy a gomb le van-e nyomva, hanem a lenyomás pillanata: amikor a gomb elfogadott állapota HIGH-ról (felengedve) LOW-ra (lenyomva) vált.
- A `ledBe` logikai (`bool`) változó tárolja a LED állapotát; `!ledBe` az ellentéte.
- Pergés: a gomb érintkezője lenyomáskor és felengedéskor néhány ezredmásodpercig többször is összeér és szétválik. Ha a program ezt több lenyomásnak érzékelné, a LED véletlenszerűen váltana.
- Pergésmentesítés `millis()`-szel: a `millis()` az indítás óta eltelt ezredmásodperceket adja. A program megjegyzi, mikor változott utoljára a beolvasott (nyers) érték (`utolsoValtas`), és az új állapotot csak akkor fogadja el (`stabilAllapot`), ha azóta már több mint 50 ms telt el.
- A `delay()`-jel szemben ez nem állítja meg a programot: a `loop()` közben folyamatosan fut, így később egy második gomb vagy egy villogó LED is kezelhető mellette.
- Az időt tároló változók típusa `unsigned long`, mert a `millis()` értéke gyorsan túlnő az `int` határán.
