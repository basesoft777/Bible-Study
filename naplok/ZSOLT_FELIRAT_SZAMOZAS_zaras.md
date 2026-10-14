# Zárójelentés — #91 ZSOLT_FELIRAT_SZAMOZAS

- **Eredmény:** 62 feliratos zsoltár + a Zsolt 13 felmérve (M0, M0b); a `Karoli_versmegfeleltetes.tsv` 63 zsoltáron javítva (1 055 sor, 0 eltérés az LXX_OS-szel, Zsolt 22: 0/32); a javítás a generátorban él (`KAROLI_KK4_tabla_veglegesit.py` + `f91_versmegf_javit.py`, bájtra reprodukálható); a térkép oszlopa `KJV_igehely`, a `sqlite_epit.py` a KJV-kulcson illeszt, a `terkep_ertek` Károli-kulcsos.
- **Közös felirat-halmaz:** `eszkozok/zsolt_felirat_halmaz.py` (67 vers); builder, `f92_db_igazolas.py`, javító és `lxx_os_import.py` ebből dolgozik; a replay (`f91_lxx_os_replay.py`) regressziós ellenőrzés.
- **Döntések:** DT142 (A1/B3/N2), DT143 (KJV_igehely, builder KJV-kulcson), DT144 (Zsolt 13:6 = `13:5`, generátor, N-F91b), DT145 (a). Végleges számot a main-en a `szamkiosztas` ad.
- **Ellenőrzés:** `naplok/ELLENOR_F91.md` (6 eltérés, mind lezárva), `naplok/ELLENOR_F91_2.md` (3 dokumentációs eltérés, javítva).
- **Tesztek:** `teszt_sqlite_epit.py` 64 OK; `ellenoriz.py` SÉRTÉS 0; f92 az ideiglenes DB-n 0 ELTÉRÉS; KK4-generátor bájtra azonos; replay 0/0 (14 könyv, régi és új A-tábla).
- **Merge UTÁN esedékes:** a `pardes.db` és a `naplok/PARDES_DB_OLVASOI_db_igazolas.md` újraépítése a main-en (az ágon nem épült újra; a mérés ideiglenes DB-ken történt). A DB-ben a `lxx_versszam.terkep_ertek` 1 344 soron, a Zsolt 13:1-en a halmaz miatt üresre változik.
- **Jelzés (#60):** a Zsolt 22-n a `terkep_ertek` a 31 nem felirat versen egyezik az LXX_OS-szel, így a #60 kerülőút kivezethető; a pilot kódját az F91 nem módosította.
- **Nyitott:** N-F91a (a térkép és az A-tábla nem zsoltári hiányai: Zsolt 1 `Psa.Psa.151`, Zsolt 37 dupla sor, hiányzó Zsolt 2 és 148–150, 203 átváltás nélküli KJV-kulcs); N-F91b (a Nave-újragenerálás N2: forrás-sha eltérés, ~247 soros drift, NAVE-0130).
- **Egyeztetett eltérés:** a brief M2 egy A- és egy B-oldalra bontva, a közös felirat-halmaz és az `lxx_os_import.py` módosítása a felhasználó döntésére (DT144/d); a Nave újragenerálása elmaradt (N-F91b).
