---
feladat: 93
cim: A TIPNR 62 token nélküli görög alapszáma — szövegváltozat vagy hiány (88 sor)
kod: TIPNR_TOKEN_HIANY
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: brief_kell
ad: a 62 alapszám (88 TIPNR-sor) mindegyikéről eldöntve és naplózva, hogy szövegváltozat, számozási eltérés vagy adathiány; az eredmény jelölés, nem javítás
kovetkezo: brief kell (a jelölés helye — normalizalas_jelentes vagy külön lista — a brief döntése)
fugg: [88]
olvas: [naplok/F88_meres.md, naplok/ELLENOR_F88_2.md, adat/SEMA.md, konkordancia/TIPNR_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, eszkozok/sqlite_epit.py, F90_TAGNT_ZAROJELES_BRIEF.md]
ir: [naplok/F93_jelentes.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, NYITOTT_FELADATOK.md]
---

# F93_TIPNR_TOKEN_HIANY_BRIEF — csonk

*FELADATOK #93 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza; v1 · 2026.10.13 · forrás: az F88 mérése (`naplok/F88_meres.md`, `naplok/ELLENOR_F88_2.md`).*

- **Lelet:** a `pardes.db` `tipnr` táblájának 88 utótag nélküli sora 62 különböző görög alapszámon (pl. `G0300`, `G0962`) olyan Strong-számot hordoz, amely a `token_strong`-ban nem szerepel — az F79 óta, a #88 normalizálásától függetlenül. A TIPNR-névrekordból ezekre nincs út az igehelyhez (néma nem-találat).
- **Feltevés (nem ellenőrzött):** szövegváltozat — a TAGNT a kritikai szöveget követi, a TIPNR más olvasat Strong-számát is felsorolja (pl. Mt 1:10 Ámon/Ámósz, Jn 1:28 Bethabara/Betánia). A 62 szám végignézése dönti el.
- **Mit ad, ha kész:** a 62 alapszám mindegyikéről eldöntve és naplózva, hogy szövegváltozat, számozási eltérés vagy adathiány; az eredmény jelölés, nem javítás.
- **Következő lépés:** brief kell; a jelölés helye (`normalizalas_jelentes` vagy külön lista) a brief döntése — ha külön lista, az `ir`-ből a `sqlite_epit.py` kikerül, és a #89/#92-vel való ütközés megszűnik.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
