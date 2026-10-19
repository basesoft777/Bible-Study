# ELLENOR_F119 — F119_BDB_HEADER_DT_BRIEF.md · 7127e283..b2f46808 (HEAD)

*A `fuggetlen-ellenor` subagent jelentése; fájlíró eszköze nem volt, a szöveget a végrehajtó írta be változtatás nélkül (az összefoglaló táblázat tömörítve), a `Karoli_versmegfeleltetes` hash-lelet a végrehajtó saját ellenőrzésével kiegészítve (lent).*

**Eredmény: ELTÉRÉS: 1 tétel**

| pont | eredmény | indok |
|---|---|---|
| 0 modell | OK | az ellenőr `claude-opus-5-5`, a kért `opus`; a commitok `Co-Authored-By: Claude Sonnet 5.5` egyezik a brief `modell: sonnet` mezőjével |
| Hatókör / `ir` | OK | három fájl: a brief saját fejléce (2/1), `adat/bdb_vers_jelentes.tsv` (1/1), `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` (3/3) |
| G3 generátor | OK | csak a `kiir()` fejléc-literáljának három sora (268–270); a kommentek (5., 48., 55., 60., 64., 206., 233., 240., 251. sor) a briefnek megfelelően helyőrzőt hordoznak |
| G3 leképezés | OK | a `0d7e9dec` szerint a→166, g→172, h→173, i→174, j→175, k→176, n→179; a diff ezzel egyezik, a tábla 2. sorában a DT-szöveg a diff előtt és után azonos |
| G3 tábla | OK | `git diff --numstat`: `1 1 adat/bdb_vers_jelentes.tsv`; csak a 2. sor (`# forras:`), adatsor nem |
| „ad” / brief 2.2 („csak a kód-hash változik”) | **ELTÉRÉS** | a 2. sorban a kód-hash (`98be38af6553`→`93d50844093a`) mellett a `Karoli_versmegfeleltetes.tsv` hash-e is változott (`edd6b4578e7f`→`6890db3cc8bb`); ok: `8f616529` (F117.3) a brief mérése (8965b53f) után újragenerálta a versmegfeleltetést, így a main-en álló tábla fejléce már a base-en is elavult hash-t hordozott; a commit-üzenet ezt nem jelezte |
| G1, G2, G4, G5 | NEM ELLENŐRIZHETŐ az ellenőrnél | a `teszt_futtat.py`, a `--ellenoriz` és a `feladatok.py ellenoriz` nem megengedett ellenőri parancs; a végrehajtó mérése: G1/G2 lent, G4 „bájtra azonos”, G5 0 hiba |
| Megállási pontok (5.) | OK | adatsor nem változott; a #76/#107 nem módosította a két fájlt a mérés óta |
| A1–A6, CI | OK | nincs próza/tanulmány a diffben; `futtat.py`: E12–E15 0 találat; E2–E16, E19, E20, E26, E28, E29 0; E25: 4 (nem a diff), E27: 42 (FELADATOK.md ág-hivatkozások, nem a diff) |
| N-F119a | OK | `NYITOTT_FELADATOK.md:54`; a `bdb_vers_jelentes.py:317` `minta()` kimenete ma is `DT-F99i`-t ír: ez az N-F119a körébe tartozik, nem a #119-ébe |
| Ell. 1–5 | OK | 1 törölt és 1 új fejlécsor, adatsor 0, sorszám-Δ 0 |

## ELTÉRÉS (1)

A `bdb_vers_jelentes.tsv:2`-ben a kód-hash mellett a `Karoli_versmegfeleltetes.tsv` hash-e is változott (F117.3, `8f616529`). Ez ellentmond a brief „ad”-mezőjének és 2.2. pontjának, és a végrehajtó nem jelezte. Az adatsorok változatlanok, így valószínűleg ártalmatlan; hogy a versmegfeleltetés módosulása egyetlen BDB-sort sem érint, az ellenőr G4 nélkül nem tudta igazolni.

**Végrehajtói kiegészítés (a lelet ellenőrzése):** a lelet igaz — `git log 8965b53f..7127e283 -- konkordancia/Karoli_versmegfeleltetes.tsv` = `8f616529`; a diff a 2. sorban a két hash-t mutatja. A G4 a végrehajtónál futott: `--ts 2026-10-16 --ellenoriz` → „bájtra azonos”, és a `git diff --stat adat/bdb_vers_jelentes.tsv` 1 sor ki / 1 be, adatsor nem változott; vagyis a generátor a mai bemenetekből a 3. sortól bájtra ugyanazt állítja elő. A hash-változás tehát a #119-től független bemenet-eltolódás, a brief „csak a kód-hash” feltevése a mérés dátumán (8965b53f) volt igaz.

## Végrehajtó mért tesztek (G1/G2)

`python eszkozok/teszt_futtat.py` (WSL, `~/pardes/pardes.db`, `epites_ts 2026-10-14`) a branch-en és a main-en (`7127e283`):
`teszt_bdb_vers_jelentes`: main FAILED (failures=1) → branch OK (26 teszt); a többi fájl azonos mindkét oldalon (arculat e=2, indito f=3, kereses f=1, olvaso_szerver f=18/e=6, pilot e=16, szintek e=3, tervezo f=1/e=2; ok: régi DB-séma, `no such column: lxx_szo_forras`). A brief G2-ben írt „276 OK, 1 FAIL → 277 OK, 0 FAIL” alap ezen az adatbázison nem reprodukálható.
