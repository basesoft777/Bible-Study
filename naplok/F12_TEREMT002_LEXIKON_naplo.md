# F12 — TEREMT-002 lexikonlap (fordított irány): munkanapló

*Brief: `F12_TEREMT002_PROZA_BRIEF.md` · ág: `claude/f12-teremt002-bc1f07` · kiindulás: `origin/main` `b0fbeed9`*

## 0. lépés — modell-ellenőrzés és mérés (2026-11-02)

**Modell.** Kért: `opus` (a brief `modell` mezője). Tényleges: `claude-opus-5-5`. Egyezik.

### 0.1 Előfeltételek a main-en

`scope=eszkozok/*.py + adat/funkcio_kapcsolok.tsv + adat/kiadasok.tsv + git log origin/main | forras=grep, git log | ts=2026-11-02`

| Előfeltétel | Mért | Állapot |
|---|---|---|
| #148: `eszkozok/szakasz_cimke_levezet.py` | megvan | ✅ |
| #148: 18–21. szabály (`ellenoriz.py`) | `szabaly18_gerinc_cimke` … `szabaly21_lap_tisztasag` megvan | ✅ |
| #148: kivétellista | adatban: `adat/funkcio_kapcsolok.tsv`, `SZOTARI_GERINC` (DT437); a generátor `GERINC_KIVETEL_MOTIVUMOK = SZK.kapcsolo_kivetelek('SZOTARI_GERINC')` | ✅, de l. 0.3/E1 |
| ISTENTISZT-001 „teljes” menet | `F152.25`/`F152.26` (v4, 2026.11.02); `adat/kiadasok.tsv`: ISTENTISZT-001 1. kiadás, 2026.11.02 | ✅ |
| a 13–14. szerep-blokk (Károli-megfelelők) | `KAROLI_MEGFELELOK` kapcsoló: ISTENTISZT-001, ALVIL-001 `aktiv`; **TEREMT-002-nek nincs sora** | ✅ a main-en, de l. 0.3/E2 |

### 0.2 A brief 3. szakaszának újramérése

`scope=adat/elofordulasok.tsv (id=TEREMT-002, n=3) + adat/*.tsv + konkordancia/TAHOT_kivonat.tsv + motivumok/TEREMT-002.md | forras=naplok/F12_meres.py (split('\t')) | ts=2026-11-02`

| # | Brief (2026-10-29) | Mért (2026-11-02, `b0fbeed9`) | Eltérés |
|---|---|---|---|
| 3.1 | 3 sor, `tohu+bohu`, `H8414+H0922` | 3 sor: 1Móz 1:2 (Peshat), Jer 4:23 (Remez), Ézs 34:11 (Remez); mind `tohu+bohu` / `H8414+H0922` | — |
| 3.2 | 0/3 szótári mező | 0/3 mind az öt mezőben | — |
| 3.3 | `karoli_szo` 3/3 | „kietlen és puszta” ×2, „pusztaság … semmiségnek” | — |
| 3.4 | H8414 `cim`/`fej`/`-/1/-`/`-/2/-`; H0922 csak `cim`/`fej` | ugyanaz | — |
| 3.5 | H8414 mindhárom vers `-/1`; H0922 `tagolatlan` | ugyanaz | — |
| 3.6 | versenként 1-1 token | 1-1 H8414 és H0922 mindhárom versben | — |
| 3.7 | H8414 `-/1/-`, `-/2/-` `illeszkedik`; H0922 `fej` megvan | ugyanaz (a `cim`/`fej` sorok `jelolo_nelkul`) | — |
| 3.8 | 2 `teljes` sor, `opus` | BDB H8414 és H0922 `teljes`/`forditas_hu`, `allapot=opus`, `modell=claude-opus-5-5` | — |
| 3.9 | 0/0/0/0 | `szotar_szakasz_cimke` 0, `lexikon_hivatkozasok` 0, `res_forras` 0, `lxx_dontesek` 0; továbbá `kiadasok` 0, **`bdb_forras_javitas` 20** (H8414/H0922), **`funkcio_kapcsolok` 1** | l. E1, E3 |
| 3.10 | 68 sor (TEREMT-002 vagy H8414/H0922) | 66 sor `id`/`cel_id` = TEREMT-002 (a mérés a Strong-oszlopot nem nézi; a 2 sor különbség a szűrés módja, nem adatváltozás) | — |
| 3.11 | `feldolgozás alatt`, `v1`, `formulaikus` | ugyanaz; a `negativ_kriterium` és a `folerendelt_fogalom` kitöltött, a `sablon_verzio` és a `forras_study` **üres** | l. E5 |
| 3.12 | 239 sor, RÉS-jelölő nincs | 240 sor (a záró újsor), RÉS-jelölő 0; szakaszrend: Kivonat, 1., 2., 3., 5., 7., Proveniencia-sorok, 3 archív blokk | — |
| 3.13 | „a TEREMT-002 nincs a kivétellistán” | **rajta van**: `SZOTARI_GERINC TEREMT-002 kivetel` („a #12 állítja `aktiv`-ra”, DT437, 2026-11-01) | E1 |
| — | `lexikon/TEREMT-002_TUDOMANYOS.md` | nem létezik | — |
| — | régi 58 `lxx-hid` audit-sor | 60 TEREMT-002 audit-sor LXX-forrásra mutat (`B4`, `LXX_kivonat_*.tsv`, 2026-09-25) | l. E4 |

### 0.3 Eltérések és új leletek

- **E1 — a gerinc-kivétel.** A brief 3.13-at és az 5. szakasz 4. elfogadási feltételét („nincs a kivétellistán, és nem került rá”) a DT437 (2026-11-01) megelőzte: a TEREMT-002 `kivetel` sorral rajta van, a sor szerint a #12 állítja `aktiv`-ra az adatcommitkor. Az `adat/funkcio_kapcsolok.tsv` nincs a brief `ir` mezőjében. → DT-F12f.
- **E2 — a 13–14. szerep.** A `KAROLI_MEGFELELOK` motívumonként bekapcsolandó (`SZK.kapcsolo_motivumok`); TEREMT-002-sor nélkül a lapról a 13–14. szerep hiányzik, a 8.c arany-összevetés pedig ezt a blokkot is kéri. → DT-F12f.
- **E3 — a BDB-forrás héber szórendje (DT-F12b).** A `bdb_forras_javitas.tsv` (generált, `eszkozok/bdb_jelolt/forras_javit.py`, DT445, 2026-11-01) a három motívumvers héber idézetét már **gépileg javította** (`heber_sorrend`, `javitva`): H0922 1Móz 1:2 és Ézs 34:11, H8414 Ézs 34:11. 9 `jelolt_marad` sor maradt a H8414/H0922-n (töredékek, pl. `׳קַותֿֿ`, `ᵐ5 וְתֹהוּ`). A **„49:19”** (H8414, a `-/2/-` szakasz, „worthlessness 49:19 ׳לְת כִלֵּיתִי …”) **nincs javítva**: a héber idézet az Ézs 49:4-é, és ugyanezt a `heber_sorrend` sor („a TAHOT Ézs 49:4 versében áll”) is igazolja. A kézi hivatkozás-javítás útja a DT381 (a) `hivatkozas_kezi` (a `forras_javit.py` `KEZI_HIVATKOZAS` listája, két minta: H8034, H7585) — ez kódbeli lista egy generátorban, nem kézi TSV-sor.
- **E4 — LXX-auditok.** A 60 régi LXX-audit `B4` lépés-kóddal áll (nem `lxx-hid` névvel); a brief „58”-a a szűrés különbsége lehet. A 4. lépés a három versre friss `lekerdez.py lxx-hid` sort ír; a régiek nem törlődnek.
- **E5 — `sablon_verzio` / `forras_study` üres.** Az ISTENTISZT-001 sora `v12`, az ALVIL-001 `v14`. A 9_ sablonra emelés (6. lépés) ezt kitölti; nem döntés, de a `motivumok.tsv` írása a 6. lépés része lesz.
- **E6 — DT438 szűkíti a DT-F12a-t.** A DT438 (a #148, 2026-11-01): a tagolatlan Strong nem lehet `lexikon_entry_id`; ha a sor egyetlen Strongja tagolatlan, `tagolatlan`. Ezzel a DT-F12a (2) (entry = H0922) és (3) (két sorra bontás, H0922 saját `jelentes_szam`-mal) kizárt; az (1) marad, a H0922 `lexikon_hivatkozasok`-értéke `tagolatlan`.

### 0.4 A levezető eszköz próbafutása (írás nélkül)

`scope=TEREMT-002 (n=3) | forras=python eszkozok/szakasz_cimke_levezet.py ellenoriz --id TEREMT-002 | ts=2026-11-02`

`3 sor, levezetve 0, egyezik a kézivel 0, eltér 0, jelzés 3` — mindhárom `[J3] üres mező: lexikon_szotar, lexikon_entry_id, jelentes_szam`. Ez a várt állapot (a mezőket az 1. lépés tölti ki); H8414-eltérés nincs. *(A futás a repóba írta a `naplok/F148_levezetes_TEREMT-002.tsv`-t; a próbafutás „írás nélküli”, ezért a fájlt töröltem, a 2. lépés `--ki` kapcsolóval írja újra.)*

`scope=adat/ (teljes) | forras=python eszkozok/ellenoriz.py --ag-allapot ag | ts=2026-11-02`

`RENDBEN: 18 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 6`. TEREMT-002: 18. szabály kivétellistán (nem fut); 19. szabály JELENTÉS, 3 hiányos sor; 8/c: `fedetlen: BDB (nincs lekérdező) | nincs tematikus_lezart forrás_study | napló nincs`.

### 0.5 Feed (muhely_allapot)

`scope=motivum:TEREMT-002 | forras=python eszkozok/muhely_allapot.py --motivum TEREMT-002 --kimenet <repón kívüli> --nincs-gh | ts=2026-11-02T11:01Z`

**4/8 zöld** („a nyolc ellenőrzési lépésből 4 teljesül”).

| # | Kritérium | Állapot | Érték |
|---|---|---|---|
| 1 | szabály-ellenőrzés (`ellenoriz.py` 1–21) | zöld | 0 HIBA |
| 2 | CI-ellenőrzés (E2–E29) | zöld | 0 HIBA, 43 jelentés |
| 3 | egyforrású, nulla-diff újragenerálás | piros | nincs `lexikon/TEREMT-002_TUDOMANYOS.md` |
| 4 | nincs nyitott jelölt | zöld | 0 |
| 5 | határ: 0 nyitott kérdés | nincs mérő | nincs `naplok/HATAR_TEREMT-002.md` |
| 6 | olvasói blokkok, kiejtés, fordítás | nincs mérő | nincs lexikonlap |
| 7 | nincs nyitott lektori kérdés | nincs mérő | nincs `naplok/LEKTOR_TEREMT-002.tsv` |
| 8 | nincs nyitott DT / ⛔ | zöld | 0 |

**E7 — a 8/8 nem a #12 kezében van.** Az 5. és a 7. kritérium a `hatar-ellenor`, illetve a lektor kimenete, ezeket a felhasználó indítja. A #12 a 3. és a 6. kritériumot tudja zöldre vinni (6/8). A DT-F12e (1) ehhez igazodik: a #12 6/8-ig visz, a 8/8 és a kiadás-sor a lektor-kör után jön.

### ⛔ DT-F12a–f

A kérdések a lexikon ág orkesztrátorához mentek (`local_20eed447-…`; az első küldés tévesen a `local_2bdbd92d-…` címre). A döntés (2026-11-02, a felhasználó felhatalmazásával): a (1), b (1) + (i), c (1), d (1), e (1), f (1); rögzítve: `DONTESEK.md` DT-F12a–f, N-F12a (F12.0, `27d8bf44`).

## 1–6. lépés (2026-11-02)

| Tétel | Commit | Eredmény |
|---|---|---|
| F12.1 | `cb31e347` | a három sor `BDB` / `H8414` / `1` / „formlessness” / „formátlanság” (a -/1/- definíciós feje bájtra; az ISTENTISZT-001 mintája: a jelentés minden során azonos); `lexikon_hivatkozasok.tsv` +2 (H8414 1, H0922 `tagolatlan`); `SZOTARI_GERINC` `aktiv`, új `KAROLI_MEGFELELOK` sor. Napló: `naplok/F12_kitoltes.tsv` |
| F12.2 | `da3ba78c` | `szakasz_cimke_levezet.py --ir`: 3 sor levezetve, jelzés 0; új sor BDB H8414 -/1/- → „formátlanság”. DT187-mutató kivezetve; a `tagolatlan` címke a lapon „(tagolatlan szócikk)” |
| F12.2b | `b4b8c7bf` | 49:19 → 49:4 (`hivatkozas_kezi`); a generátorban a DT-F131z helyőrző DT445-re javítva (l. F1 alább) |
| F12.4 | `b59dc49c` | LD091–LD096; 3 friss B4 audit-sor |
| F12.5 | `407659bc` | tanítói keresés: 18 tanító, 1 találat (Derek Prince, ✅ + ⚠️), 17 gap; a ✅ sor utóellenőrizve |
| F12.6 | `dc307643` | a forrás a 9_ sablon szerint; `res_forras.tsv` 9 sor, E28-sor, `forras_study`; archív: `archivum/TEREMT-002/`; `bdb_vers_jelentes.tsv` újragenerálva (Ézs 49:19 → 49:4, `forras_javitas`) |

**A tesztek.** `teszt_szerepmatrix.py` 3, `teszt_szotari_gerinc.py` 5, `bdb_jelolt/teszt_bont.py` 3 bukás marad; mind a három fájl ugyanezeket a bukásokat adja a main változatán is (a módosított fájlok `origin/main`-változatával futtatva, 2026-11-02): az ISTENTISZT-001 #152 utáni számai (33 → 22 sor, 23 → 16 hely, G0994 rokon szó) és a BDB-tábla mai állapota (`Determinizmus`, `HuIlleszt`). A TEREMT-002-t érintő két teszt és a `test_hivatkozas_kezi` az új állapotra írva, zöld. → N-F12b.

**A 3. lépés sorrendje.** A `glossza_lexikon_forditas.py lista` a `res_forras.tsv` sorai nélkül nem renderel lapot (`KIHAGYVA`), ezért a fordítási kör a 6. lépés után fut.
