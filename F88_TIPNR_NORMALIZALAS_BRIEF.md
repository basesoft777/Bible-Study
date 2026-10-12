---
feladat: 88
cim: TIPNR Strong-normalizálás — alapszám a strong oszlopban, utótag külön (DT-F79c)
kod: TIPNR_NORMALIZALAS
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: brief_kell
ad: a pardes.db tipnr.strong oszlopa az alapszámot hordozza (a nagy- és kisbetűs utótag levágva, a TIPNR-betöltő kifejezett szabályaként), új utotag oszlop, a strong_nyers marad; SEMA 1.2 bővítve; a G6202 a normalizálási jelentésben; teszt és újraépítés, a NULL-arány mérve
kovetkezo: brief írása a DT-F79c szerint (a #302 merge-e után)
olvas: [DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, eszkozok/strong_util.py, eszkozok/sqlite_epit.py, konkordancia/TIPNR_kivonat.tsv, naplok/SQLITE_EPIT_meres.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, adat/SEMA.md]
fugg: [79]
---

# F88_TIPNR_NORMALIZALAS_BRIEF — csonk

*FELADATOK #88 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza; a brief csak chatben van.*

- **Mit ad, ha kész:** a pardes.db tipnr.strong oszlopa az alapszámot hordozza (a nagy- és kisbetűs utótag levágva, a TIPNR-betöltő kifejezett szabályaként), új utotag oszlop, a strong_nyers marad; SEMA 1.2 bővítve; a G6202 a normalizálási jelentésben; teszt és újraépítés, a NULL-arány mérve
- **Következő lépés:** brief írása a DT-F79c szerint (a #302 merge-e után)

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
