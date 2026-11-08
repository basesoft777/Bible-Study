# F179 záró jegyzet

- A `general.py` `UJSZOVETSEGI_TOKENEK` a `Konyv_normalizalo_tabla.tsv` Mat–Rev soraiból épül (27 könyv); a régi kézi lista 15 újszövetségi könyvet (Mk, Ján, Gal, Ef, ...) nem ismert.
- Teszt: `eszkozok/teszt_general_konyvlista.py`, 5/5 zöld (minden ÚSZ-rövidítés, Gal 3:13 ÚSZ).
- Mérés (repón kívüli generálás, előtte–utána): csak a HAMART-001 érintett: lap-mondat 46/6 → 43/9 (a main-adaton a helyes szám), LXX-tábla 67 → 62 sor (Gal 3:10, 3:13 és Mk 7:21–23 kikerül); a többi 8 lap változatlan.
- N-F09f lezárva (`NYITOTT_FELADATOK.md`).
- ELDÖNTVE (DT-F179a (A), szerkesztői döntés): a main-beli `lexikon/HAMART-001_TUDOMANYOS.md` (és `_TORZSCIKK.md`) nincs és nem is lesz újragenerálva a #179-ben (régi állapotú lap; a generátor kimenete a számokon túl kiejtés-, olvasói mondat- és szócikk-eltéréseket is hoz). A #639 a #179 merge-e után újragenerál, és hozza a helyes számot (42/6 az ő ágán, 43/9 a main-adaton). A (B) gépi blokkcsere és a (C) teljes újragenerálás elvetve.
- NYITOTT: N-F179a: az `n14_hamart_betoltes.py` saját ÚSZ-listája 13 könyvet még nem tartalmaz (köztük Ján); az `ir`-en kívül, nem módosítva (`nyitott/uj/usz-konyvlista.md`).
- A brief „42/6” a #639 állapota; a main-adaton 43/9.
- Az ellenőrzést a `fuggetlen-ellenor` végzi; a saját munkám nem minősített.
