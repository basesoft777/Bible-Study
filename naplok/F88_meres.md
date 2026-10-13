# F88 — a TIPNR Strong-normalizálás mérése (DT111)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod teljes --ketszer --meret --naplo), a kész pardes.db lekérdezése | ts=2026-10-13`. A hash-egyezés a `--ketszer`, a táblaméret a `--meret` futásból. Független újramérés (F88.9): `naplok/ELLENOR_F88_2.md` — a számok egyeznek. Külön napló: az `sqlite_epit.py --naplo` futása nem írja felül. A teljes építés generált mérése: `naplok/SQLITE_EPIT_meres.md`.*

| mutató | F79 (előtte) | F88 (utána) |
|---|---:|---:|
| `tipnr` sorok | 35 522 | 35 522 |
| `strong IS NULL` | 16 928 (47,7%) | **0 (0,0%)** |
| utótagos sor (`utotag` nem üres) | – | 16 928 |
| utótag nélküli sor, `strong` = `strong_nyers` | 18 594 | 18 594 |
| `tipnr` mérete (indexszel) | 3,91 MB | 4,12 MB |
| `strong`-ja a `token_strong`-ban szerepel | – | 35 433 / 35 522 |

A `token_strong`-ban nem szereplő 89 sor (újramérve a kész `pardes.db`-n, 2026-10-13):

- 1 sor utótagos: `G6202` (`Millo Akra`, `G6202G`) — a levágott alapszám a normalizálási jelentésben jelölve (jelölés, nem javítás);
- 88 sor utótag nélküli, 62 különböző alapszám (pl. `G0300`, `G0962`) — már az F79 óta sem szerepelnek; nem az F88 hatóköre, a jelentés nem jelöli.

Összeg: 35 433 + 88 + 1 = 35 522. (A korábbi változat „63 alapszám, 89 sor” utótag nélkülire hibás volt.)

- Megmaradt NULL sor nincs; a „Strong-szám nem normalizálható” ok a `tipnr`-nél nem fordul elő.
- Két építés, táblánkénti hash azonos (G2); a `tipnr` hash-e `d4a93c34d0e36db8`.
- A többi tábla hash-eltérése az F79-es mérés óta a main-be került más változásokból ered (pl. `bdb_karoli`, `token_*`), nem az F88-ból.
- A jelentés `nyers` mezőjébe az alapszám (`G6202`) kerül, nem a nyers `G6202G`.
