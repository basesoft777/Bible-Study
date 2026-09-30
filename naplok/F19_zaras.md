# F19 zárójelentés — KJV/ASV-import (eBible)

- **Ág:** `claude/kjv-asv-import`; commitok F19.0–F19.4; ellenőrzés: `naplok/ELLENOR_F19.md` (2 kör).
- **KJV:** `konkordancia/KJV_Strongs_teljes.tsv`, 349 308 sor, 66 könyv, állapot `importált, javaslat`.
- **ASV:** `konkordancia/ASV_Strongs_teljes.tsv`, 705 378 sor — **forráshibás** (a nyers eBible-USFM-ben is hiányzik a H430/H776/H1/G746), `javaslat`, tartalmi keresésre nem használható.
- **Hiányok:** `naplok/F19_hianyok.tsv` (versszámozási eltolás / adathiány / kritikai szöveg / gyanús szomszéd).
- **Licenc:** eBible KJV/ASV Public Domain, luvlylavnder CC0; scrollmapper kimaradt. Nem volt ⛔-megállás, meglévő sor nem csökkent.
- **N29:** részben teljesült, nyitva — a Strong-címkés ASV-hez új forrás kell (luvlylavnder ASV-Strongs vagy studybible.info), külön feladat.
- **Nyitott döntés:** DT19 (a–h, gépi javaslattal).
- **Egyeztetendő:** az `ir` lista bővítése (`eszkozok/f19_ebible_import.py`, `eszkozok/f19_ellenorzes.py`, `adat/szotar_szerepek.tsv`, `adat/datasetek.tsv`) — megtörtént a fejlécben.
- **Marad:** `konkordancia/README.md`, `adat/SEMA.md` frissítése (DT19 f); szerepmátrix M2-lelet (két meglévő sor módosult, dokumentált).
- **Egyeztetett eltérés:** egyfeladatos futás a javasolt csomag helyett (felhasználói döntés: „mehet #19”).
