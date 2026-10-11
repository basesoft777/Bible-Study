# KAROLI_ELLENORZES zárás (F65, 2026-10-11)

proveniencia: scope=manual | forras=adat/karoli_strong/parok_*.tsv, adat/elofordulasok.tsv | ts=manual (nem lekérdezés)

- Ellenőrzött sor (`elofordulasok.tsv`, tartalom-alapú vagy már átállított): 205.
- **egyezik 153** (ebből `magas` párokon 23, `alacsony` párokon 130), **elter 3**, **nincs_par 49**.
- Frissítve `szó-szintű-gépi`-re: **23 sor az `elofordulasok.tsv`-ben, 23 a `jeloltek.tsv`-ben** (csak az `azonositas_modja`; 1Móz 20, 2Móz 3 sor; motívumok: KIRALY-001, ISTENTISZT-001, TEREMT-001, TEREMT-002, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001).
- Egyezés jellege (névelő/`és` kiszűrve): 15 teljes, 8 részleges.
- Nem változott (kézi ítéletre vár): 3 `elter` (KIRALY-001 2Móz 19:6; TEREMT-001 2Móz 15:5; Jób-sor), 49 `nincs_par` (NT, még nem párosított ÓSZ-könyv, Jób 17:16, Préd 9:10), 130 `egyezik`+`alacsony` (a #22 kétmodelles futása után újrafuttatható).
- Idempotencia: a második `--frissit --ir` 0 sort írt; a variancia újragenerálása bájtazonos.
- Nem érintett: tanulmány-, motívum-, lexikonfájl; `Karoli_Strong_kivonat.tsv` (N-F65a).
- Hátra: `fuggetlen-ellenor` (`naplok/ELLENOR_KAROLI_ELLENORZES.md`), `lezarva`, draft PR.
