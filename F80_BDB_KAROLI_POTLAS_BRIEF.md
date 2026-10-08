---
feladat: 80
cim: A Károli-támasz nélkül fordított BDB-szócikkek adatblokkjának pótlása a teljes Károli–Strong után (újrafordítás nélkül)
kod: BDB_KAROLI_POTLAS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: brief_kell
ad: a #22 lezárása után a [NINCS KÁROLI-ALAK] jelölésű (vagy a párosított könyvek szűkössége miatt hiányos) BDB-szócikkek adatblokkja — Károli-alakok, példaversek — pótolva; a fordítás szövege nem változik
kovetkezo: brief írása a #22 lezárása után; a tárolás helye (a forditasok.tsv mezője vagy külön tábla, SEMA-bővítéssel) a brief ⛔ M0-jának kérdése
olvas: [adat/karoli_strong/, adat/forditasok.tsv, eszkozok/bdb_adatblokk.py, F38_BDB_FORDITAS_BRIEF.md, naplok/BDB_FORDITAS_naplo.md]
ir: [adat/forditasok.tsv]
fugg: [22]
---

# F80_BDB_KAROLI_POTLAS_BRIEF — csonk

*FELADATOK #80 · csonk-brief: nem végrehajtható · döntés: DT-F52f (15) · forrás: `ADATVAGYON_TERV.md` 19. (teendő: „BDB javító menet a teljes Károli–Strong után”), 21. (1. lépcső); DT54 („a hiányt a javító menet pótolja”), DT56*

- **Mit ad, ha kész:** a #38 adagjaiban a Károli-támasz nélkül fordított szócikkek is megkapják a Károli-alakokat és a példaverseket mint adatot.
- **Határ:** újrafordítás nincs — a DT56 az utólagos visszaellenőrzést (újrafordítást) elvetette; ez a feladat csak az adatot pótolja, így a DT54 „javító menet” mondatát pontosítja (DT-F52f (15)).
- **Függés:** #22 (teljes Károli–Strong).
- **`ir`:** a legszűkebb ismert halmaz (`adat/forditasok.tsv`); ha az M0 külön táblát választ, a brief `ir`-je tételként bővül (SEMA-bővítéssel).

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
