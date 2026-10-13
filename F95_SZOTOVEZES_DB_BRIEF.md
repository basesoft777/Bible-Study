---
feladat: 95
cim: A szótári alak oszlopai a pardes.db-ben — a #94 kimenetének betöltése, index, frissességi teszt
kod: SZOTOVEZES_DB
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: brief_kell
ad: a Károli-tokenekhez szótári alak, mai szótári alak, alapige és további elfogadható alak a pardes.db-ben, indexelve a szótári alak szerinti kereséshez (#76)
kovetkezo: brief kell a #94 lezárása után; a #92 merge-e után futhat
olvas: [adat/szoto/, adat/SEMA.md, adat/licencek.tsv]
ir: [eszkozok/sqlite_epit.py]
fugg: [92, 94]
---

# F95_SZOTOVEZES_DB_BRIEF — csonk

*FELADATOK #95 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza; v1; a tartalom forrása: `F94_SZOTOVEZES_BRIEF.md` 3. pont („A `pardes.db`-oszlop — külön feladat”), a felhasználó döntése (chat, 2026-10-13): a #94 .4 lépése külön feladat, hogy a #94 .0–.3 a #92 előtt indulhasson.*

- **Mit ad, ha kész:** a Károli-tokenekhez szótári alak, mai szótári alak, alapige és további elfogadható alak a pardes.db-ben, indexelve a szótári alak szerinti kereséshez (#76)
- **Következő lépés:** brief kell a #94 lezárása után; a #92 merge-e után futhat (sorrend: #88 → #89 → #92 → #95 → #76, mind a `sqlite_epit.py`-t írja)

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
