# BDB_HEADER_DT — zárójelentés (#119, F119)

*2026.10.19 · modell: claude-sonnet-5-5 · ág: claude/f119-bdb-header-dt*

- **Ok:** a `szamkiosztas` Action csak `*.md`/`*.tsv` fájlokban cseréli a DT-helyőrzőket, a `bdb_vers_jelentes.py` fejléc-literáljában `DT-F99*` maradt, így a tábla 2. sora nem volt reprodukálható és a `test_bajtra_azonos` bukott.
- **Javítás:** `bdb_vers_jelentes.py` `kiir()` (268–270. sor): `DT-F99a/g/h/i/j/k/n` → `DT166/172/173/174/175/176/179` (0d7e9dec szerint). A kommentek változatlanok (helyőrző marad).
- **Tábla:** `adat/bdb_vers_jelentes.tsv` újragenerálva `--ts 2026-10-16`-tal; a diff 1 sor ki / 1 be, csak a 2. sor, adatsor nem változott.
- **G4:** `--ts 2026-10-16 --ellenoriz` → „bájtra azonos”. **G5:** `feladatok.py ellenoriz` 0 hiba.
- **G1/G2:** `teszt_futtat.py` (WSL, `epites_ts 2026-10-14`): `teszt_bdb_vers_jelentes` main-en FAILED (1) → ágon OK (26 teszt, benne `test_bajtra_azonos`). A többi tesztfájl azonos mindkét oldalon (arculat e=2, indito f=3, kereses f=1, olvaso_szerver f=18/e=6, pilot e=16, szintek e=3, tervezo f=1/e=2), régi DB-séma miatt (`no such column: lxx_szo_forras`). A brief 276 OK/1 FAIL alapja ezen az adatbázison nem reprodukálható.
- **ELTÉRÉS (ELLENOR_F119, a felhasználó elfogadta, 2026-10-19):** a 2. sorban a kód-hash mellett a `Karoli_versmegfeleltetes.tsv` hash-e is változott (`edd6b4578e7f`→`6890db3cc8bb`), mert az F117.3 (`8f616529`) a brief mérése után újragenerálta a bemenetet; a main-en álló tábla fejléce már elavult volt. Adatsor nem érintett.
- **N-F119a (nyitott, nem e feladat):** a `szamkiosztas` nem nyúl `.py`-hoz; a `minta()` kimenete (`bdb_vers_jelentes.py:317`) ma is `DT-F99i`-t ír. Gyógymód tartalmi döntés.
- **Ellenőrizetlen:** a teljes zöld futás (277 OK/0 FAIL) a régi WSL-adatbázis miatt nem érhető el; az adatbázis újraépítése nem e feladat.
