---
feladat: 79
cim: SQLite-építő — a pardes.db a SEMA szerint, integritási tesztekkel (az olvasói konkordancia adatbázisa)
kod: SQLITE_EPIT
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: brief_kell
ad: eszkozok/sqlite_epit.py: SEMA-típusok, IGEHELY-normalizálás a Konyv_normalizalo_tabla-n át, KK-alapú vers-kulcs, szamozas (BSB-értékkészlet + N46), licenc_allapot és kereskedelmi minden táblán, strong_parok és frázis-pozíció előszámolva, FTS a motivumok/ fölött; a SEMA 3. szakasz integritási szabályai tesztként, sértésnél megáll; a pardes.db helyben, .gitignore-ban
kovetkezo: brief írása a MUNKATERV 4. szakasz SQLITE_EPIT sora és az ADATVAGYON_TERV 21. (3. lépcső), 22.4 szerint; kis minta: 8 lexikonoldalas motívum + 1Mózes
olvas: [adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, adat/karoli_strong/, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/BSB_Strongs.tsv, MUNKATERV.md, ADATVAGYON_TERV.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, .gitignore]
fugg: [62]
nem_fugg: [38, 52]
---

# F79_SQLITE_EPIT_BRIEF — csonk

*FELADATOK #79 · csonk-brief: nem végrehajtható · döntés: DT-F52f (12), DT-M1 · forrás: `MUNKATERV.md` 4. szakasz (SQLITE_EPIT), `ADATVAGYON_TERV.md` 19., 21. (3. lépcső), 22.4*

- **Mit ad, ha kész:** a `pardes.db` (generált, nem commit), `naplok/SQLITE_EPIT_integritas.md`; a 26 pontból az 1–6, 13–15 lekérdezése visszaadja a tanulmányok ismert tényeit.
- **Fázis:** `1`, mert a #76 (#25a) erre vár, és a DT-F52d (6) elve szerint az 1. fázisú feladatot visszatartó feladat nem lehet `folyamat` (a döntési lista 12. tétele „folyamat”-ot írt; az eltérést a felhasználó jóváhagyta, DT-F52d (6)).
- **Függés:** #62 (egységes `strong_normalizal()`); a #76 függ tőle.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
