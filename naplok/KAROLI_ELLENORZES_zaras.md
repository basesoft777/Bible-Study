# KAROLI_ELLENORZES zárás (F65, 2026-10-11)

proveniencia: scope=manual | forras=adat/karoli_strong/parok_*.tsv, adat/elofordulasok.tsv | ts=manual (nem lekérdezés; a gépi párosítás modell-kimenet)

- Ellenőrzött sor (`elofordulasok.tsv`): 205 → **egyezik 153** (`magas` párokon 23, `alacsony` párokon 130), **elter 3**, **nincs_par 49**; +16 TEREMT-002 `jeloltek`-sor `nincs_strong` ítélettel (nincs `elofordulasok`-párja, Strong híján nem ellenőrizhető).
- Átállítva `szó-szintű-gépi`-re: **23 sor az `elofordulasok.tsv`-ben, 23 a `jeloltek.tsv`-ben** (csak az `azonositas_modja`; 1Móz 20, 2Móz 3). Egyezés jellege (névelő/`és` kiszűrve): 15 teljes, 8 részleges. Második `--frissit --ir`: 0 sor.
- Nem változott, kézi ítéletre vár: `elter` 3 (KIRALY-001 2Móz 19:6; TEREMT-001 2Móz 15:5; ALVIL-001 Jób 17:13), `nincs_par` 49, `egyezik`+`alacsony` 130 (a #22 kétmodelles futása után újrafuttatható).
- **Versszám-javítás:** Préd 9:10, Jób 17:13, Jób 17:16 régi igehelye nem Károli-kulcs (KJV/MT-számozás); Károli-kulcs: Préd 9:12, Jób 17:12, Jób 17:15. A Jób 17:13 `elter` és a másik kettő `nincs_par` eltolásból ered, nem szóeltérésből (jelölve az eltéréslistán; az ítélet és az adatsor nem változott).
- **Bontási napló, `adat/karoli_variancia.tsv`** (42 797 adatsor): `strong_szoalak` 1Móz 12 040, 2Móz 9 347; `szoalak_strong` 1Móz 12 040, 2Móz 9 347; `megerosites` 23 (1Móz 20, 2Móz 3). A `konyv` oszlop az igehely rövidítése (`1Móz`). A `--ts` alapértéke a futás UTC időbélyege.
- **Fenntartások.** (1) A „segítségül” → H9003 összerendelés a #22 gépi párosításának modell-értelmezése (a `qárá bešém` szerkezet), nem szó szerinti megfelelés. (2) Az „a 23 soron nincs valódi hézag (`nincs_gepi_par`)” állítás a `parok_*.tsv` modell-kimenetén múlik (proveniencia), nem áll önállóan.
- **Egyeztetett eltérés a briefhez (DT-F65a):** az M3 mintája az ISTENTISZT-001 az ANTROP-001 helyett (az ANTROP-001-nek 1 sora van az 1Móz/2Móz-ben).
- Nem érintett: tanulmány-, motívum-, lexikonfájl, `Karoli_Strong_kivonat.tsv` (N-F65a); a `lexikon/` generált nézete még `tartalom-alapú`-t mutat (N-F65b).
- Hátra: `lezarva` fejléc (megtörtént a F65.6-ban), a PR-t az orkesztrátor nyitja.
