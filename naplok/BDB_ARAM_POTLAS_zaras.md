# BDB_ARAM_POTLAS zárás (F66)

*A `konkordancia/BDB_aram_potlas.tsv` végszámai (173 sor) · scope=konkordancia/BDB_aram_potlas.tsv | forras=eszkozok/bdb_aram_potlas.py --m1 | ts=2026-10-06*

- `egyertelmu`: 169 (a felhasználó a 20 soros szúrópróba után elfogadta)
- `kezi_elfogadott`: 1 (H2298 → BDB9285, חַד; új állapotérték, DT-F66a, proveniencia `manual`)
- `csonk`: 2 (H3769, H5013; jelölt marad)
- `cimke_reszleges`: 1 (H0004, a BDB9264 bevezető jegyzet; jelölt marad)
- `tobb_jelolt`: 0, `nincs_szoveg`: 0
- Elfogadott sor összesen: 170; jelölt: 3.
- A `BDB_teljes_unabridged.tsv` (SHA-256 `40d96e57…f3cf6`), a `BDB_strong_alias.tsv` és a `BDB_strong_alias_elvetett.tsv` bájtra azonos a main-nel (a teszt `git diff origin/main`-nal ellenőrzi).
- A 187 reprodukálva (14 alias + 173 elvetett); a 198 nem reprodukálható (`naplok/BDB_ARAM_POTLAS_M0.md`).
- Átfedés a fő táblával (mérés, `naplok/BDB_ARAM_POTLAS_duplikacio.md`): a 170 elfogadott sorból 164 szövege már a héber testvérsor végén van; a beemelés duplikációt okozhat, külön felhasználói döntés (N-F66b).
- Döntés: DT-F66a (az új állapotok). Új nyitott tétel: **N-F66b** (a 170 elfogadott sor beemelése a fő táblába a #38 aktuális adagja után, felhasználói döntéssel; a #38 sorrendjének újragenerálása). Lezárt: N-F66a (a szúrópróba-kivonat két hibája).
- Teszt: `python eszkozok/teszt_bdb_aram_potlas.py` zöld. A független ellenőrzést a felhasználó futtatja az ágon.
