# F19 zárójelentés — KJV/ASV-import (eBible)

- **Ág:** `claude/kjv-asv-import`; commitok F19.0–F19.7; ellenőrzés: `naplok/ELLENOR_F19.md` (2 kör).
- **KJV:** `konkordancia/KJV_Strongs_teljes.tsv`, 349 308 sor, 66 könyv, állapot `importált, javaslat`.
- **ASV:** az eBible-ASV **forráshibás** (a nyers USFM-ben hiányzik a H430/H776/H1/G746); a tábla (705 378 sor) a DT19 (b) döntése szerint **nem került a repóba** (F19.7, `git rm`); a bizonyíték a DT19-ben és a `naplok/ELLENOR_F19.md`-ben marad.
- **Hiányok:** `naplok/F19_hianyok.tsv` (versszámozási eltolás / adathiány / kritikai szöveg / gyanús szomszéd).
- **Licenc:** eBible KJV/ASV Public Domain, luvlylavnder CC0; scrollmapper kimaradt. Nem volt ⛔-megállás, meglévő sor nem csökkent.
- **N29:** részben teljesült, nyitva — a Strong-címkés ASV-hez új forrás kell (luvlylavnder ASV-Strongs vagy studybible.info), külön feladat.
- **Döntés:** DT19 ✅ (felhasználói döntés, F19.7).
- **Egyeztetendő:** az `ir` lista bővítése (`eszkozok/f19_ebible_import.py`, `eszkozok/f19_ellenorzes.py`, `adat/szotar_szerepek.tsv`, `adat/datasetek.tsv`) — megtörtént a fejlécben.
- **Frissítve F19.7-ben:** `konkordancia/README.md`, `adat/SEMA.md`; szerepmátrix: a KJV-híd a 9. szerepbe olvasztva (két meglévő sor módosult, dokumentált).
- **Egyeztetett eltérés:** egyfeladatos futás a javasolt csomag helyett (felhasználói döntés: „mehet #19”).
