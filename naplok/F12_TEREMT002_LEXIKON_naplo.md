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

## 3. lépés — fordítás a lap előtt (F12.3, F12.7c)

A lista (`glossza_lexikon_forditas.py lista`, a forrás bekötése után) 10 egységet adott: 6 TBESG `rovid` (a H8414 SECE-megfelelői), 2 UBS_DBH `glosszak_hu`, 2 BDB (H8414 `1`, H0922 `tagolatlan`). A nyolc rövid glosszát a `vegrehajto-sonnet` (`claude-sonnet-5-5`) fordította tervezetbe, kapukkal (`naplok/F12_forditas_tervezet.tsv`, `naplok/F12_forditas_naplo.md`). **Egy eltérés a tervezettől:** a H8414 „waste; desolation; chaos” 2. tagja „elpusztítottság” helyett „kietlenség” — a rangsor szerint (szójegyzék > Károli > BDB > szótár) a Károli „kietlen” szava a *tohu* megfelelője (1Móz 1:2; Jer 4:23), és a nyelvközi egység elve szerint a fogalomnak egy magyar szava van; az orkesztrátor elfogadta. A két BDB-egység a gerincen a `bdb_szakasz_hu.tsv`-ből (a 2026.10.01-i Opus-teljesfordítás szakaszai) magyarul áll; az E19 a H0922 `tagolatlan` sort fordítássorral kérte, ezért az a meglévő teljes fordítás `fej`-szakaszából került át (F12.7c), új fordítás nélkül. A #64 5.3 lelete (a BDB-fordítást ugyanaz a modell írta, mint a prózát) a forrás 7. pontjában módszertani mondat. Fizetős API-hívás nem volt.

## 7. lépés — generálás (F12.7a–d, F12.8)

- A próbalap repón kívül (`--kimenet`), mérés: `naplok/F12_proba_meres.py`. ⛔ a próbalap után: DT-F12g, DT-F12h; az orkesztrátor jóváhagyta az éles írást.
- DT-F12g: `szerep_karoli.py` `KOTOSZO = {'és'}`. Nulla-diff: A/B generálás mind a kilenc lapra (régi és új kód, `PARDES_DATUM=2026-11-02`): nyolc lap bájtra azonos; az ISTENTISZT-001 és az ALVIL-001 a saját `PARDES_DATUM`-ával (2026-10-29) 0 eltérő sor a commitolt lappal.
- Éles: `general.py --cel lexikon --id TEREMT-002 --ir`; a második futás „változatlan”. `naplo`, `nyitott` `--ir`, majd `--ellenoriz`: zöld.
- F12.7d: a „Görög szavak” ÜRES-NYELV blokkjának nem volt olvasói bevezetője (az első motívum görög Strong-token nélkül), a Feed 6. kapuja 46/47-et mért; a generátor új `nyelv_ures` sablont kapott (ÜRES-NYELV blokk csak ezen a lapon áll).
- F12.8: a friss main (`cccd17a8`) beolvasztva; a lap utána „változatlan”, a `naplo`/`nyitott` zöld.

## 8. lépés — ellenőrzés az arany lap mércéje szerint

**(a) Gépi.** `ellenoriz.py`: RENDBEN 18 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 6; a 18–21. szabály a TEREMT-002-n RENDBEN. `ellenorzes/futtat.py` (`--valtozott`, `[ELLENŐRZŐ]` PR-cím): HIBA csak az E5 (négy törölt címsor), a commit-üzenet `TÖRLÉS-SZÁNDÉKOS:` sora oldja fel (F12.9). `kuszob.py`: 3 fő előfordulás, kitöltött. `gate.py`: egy átfedés, 1Móz 1:2 a TEREMT-001-gyel — a forrás 3. pontjának „Elhatárolás”-a kezeli (más mondatrész, más funkció). Kiejtés: kézi hiány 0, generált 3 (a jelmagyarázat; az arany lapon ugyanez).

**Feed (`muhely_allapot.py`, 2026-11-02): 6/8.** Zöld: 1, 2, 3 (nulla-diff), 4, 6 (47/47 blokk, kiejtés-hiány 0, fordításra vár 0), 8. Mérő nélkül: 5 (határ: `naplok/HATAR_TEREMT-002.md`), 7 (lektor: `naplok/LEKTOR_TEREMT-002.tsv`) — a felhasználó indítja (DT-F12e (1)).

**(b) Sablon-kapu** (6_ L1–L7, DT2, a 9_ sablon 8. pontja):

| Kapu | Állapot | Mivel |
|---|---|---|
| L1 szerkezeti teljesség | ✅ | a 9_ sablon 4. pontjának minden aktív `kezi_forras` szakasza; inaktív: 0., 1.L, 2/b (`INAKTÍV`, indokkal); `adat` szakaszok `ADAT-NÉZET`-tel |
| L2 napló-jelölés | ✅ | dátum-, eredet-, döntés- és folyamatmondat `【NAPLO】`-ban; a megbízhatóságot érintő módszertani mondat (a BDB-fordítás nem független; a szótári besorolás gépi) a 7. pontban, apparátusként |
| L3 lexikai vs. tematikus | ✅ | Ézs 45:18, Ézs 24:10, a mérőkötél: „tematikus, nem lexikai” |
| L4 kereszt-motívum | ✅ | TEREMT-001: elhatárolás a 3. pontban; a TEREMT-001 sorai változatlanok |
| L5 nevesített tanító | ✅ | hivatkozás a 7. lépés fájljára (5. pont), a lapon „Tanítói egyezés” rés |
| L6 a)–f), L7 PaRDeS-rétegfegyelem | ✅ | a #64-ben mérve, a próza érvelése nem változott; új bekezdés: „A két olvasat képviselői” (3.V, olvasói) |
| DT2/1 rések | ✅ | kilenc rés: hat kézi (kivonat, miert_fontos, ertelmezes, alkalmazas, tanitoi, modszertan), három generált (2b, minosites, alatamasztas) |
| DT2/2 adat-forrás jelölés | ✅ | `ADAT-NÉZET` minden adatból generált helyen; `ADAT-HIV` öt sorra (kinyerés: 0 hiba) |
| Kivonat határ-elemek (9_ v0.4) | ✅ | a negatív kritérium szó szerint (két szó egy versben; a *tohu* egyedül nem; a „kietlen” magyar szó sem dönt, Zsolt 107:40); kivétel nincs, a két kapcsolt hely megnevezve; a fölérendelt fogalom mondata belső szó és forrásnév nélkül |

**(c) Arany-összevetés, blokkonként** (`naplok/F12_proba_meres.py`):

| Blokk | ISTENTISZT-001 | TEREMT-002 | Megjegyzés |
|---|---|---|---|
| szótári gerinc (DT272) | 3 | 2 | a TEREMT-002-nek két héber szava van, görög nincs |
| „Jelentés (a szó)” / „Funkció (a motívumban)” | 2 / 2 | 2 / 2 | — |
| ⓘ-lábjegyzet | 66 | 12 | a helyek száma (22 / 3) szerint |
| „Mit mutat ez a rész?” | 51 | 39 | a görög szerepek nélkül; az ÜRES-NYELV blokk bevezetővel (F12.7d) |
| LXX-fordítói döntések | ✅ | ✅ | a Jer 4:23 „függőben” (DT-F12h, N-F12c) |
| 12. / 13. / 14. szerep | ✅ | ✅ | a 12. az arany lapon kitöltött, itt `javaslat` állapotú explicit üres blokk (`ÜRES-BLOKK`, 1); a 13–14. az „és” nélkül |
| Kolofon, Irodalom és idézés | ✅ | ✅ | a kiadás-sor nélkül (DT-F12e) |
| Rések (kivonat … modszertan) | ✅ | ✅ | — |
| Rokon szavak | ✅ | — | **a lapon explicit hiányjelölés nincs**: a generátor a szakaszt rokon szó nélkül elhagyja; a TEREMT-002-nek nincs a lapon hivatkozott rokon szava |
| Új felismerés | ✅ | — | tartalmi: a TEREMT-002-n nincs ilyen |
| „fordításra vár” | 1 | 1 | a jelmagyarázat |

**(d) A fordított irány mérése: ahol kézi javítás kellett.** A #13 új motívumainak folyamathibái; a #148/#125-nek szóló tétel mellettük.

| # | Hol | Mi kellett kézzel | Tétel |
|---|---|---|---|
| 1 | a brief 3.13 és 5.4 | a DT437 (2026-11-01) a TEREMT-002-t a gerinc-kivétellistára tette, a brief még „nincs rajta”-t mért; a `KAROLI_MEGFELELOK` motívumonként kapcsolandó, a brief nem említette | DT-F12f |
| 2 | `bdb_jelolt/forras_javit.py` | a kódban a DT-F131z helyőrző maradt, az adat DT445-öt írt; enélkül az újragenerálás 36 253 sort írt vissza | N-F12d |
| 3 | BDB „49:19” | kézi hivatkozás-javítás, utána a `bdb_vers_jelentes.tsv` újragenerálása; a lánc nincs leírva | DT-F12b (1) |
| 4 | a 3. lépés sorrendje és eszköze | a fordítási lista a `res_forras.tsv` nélkül nem renderel; téves `nincs_forras` a gerincen fordított BDB-szakaszra és a TBESG `rovid`-ra; a repóba ír | N-F12e |
| 5 | a lap címe | a `motivumok.tsv` `cim`-változása meglévő lapra nem kerül át | N-F12f |
| 6 | H0922 gerinc-ⓘ | tagolatlan szócikk: technikai ⓘ-szöveg a példahelyeknél | N-F12g |
| 7 | kiejtés | a forrásban 9 kézi kiejtés-hiány; a `motivumok.tsv` címe és negatív kritériuma kiejtés nélkül | javítva (F12.6) |
| 8 | 13–14. szerep | az „és” kötőszó kulcsszóként | javítva (F12.7b, DT-F12g) |
| 9 | ÜRES-NYELV blokk | olvasói bevezető nélkül | javítva (F12.7d) |
| 10 | E19 | a tagolatlan sor fordítássort kér, bár a gerinc a szakasz magyarját mutatja | javítva (F12.7c) |
| 11 | tesztek | három tesztfájl a main-en is bukik | N-F12b |
| 12 | E16 / E5 | a PR-cím `[ELLENŐRZŐ]` előtagja (e28-sor); a commit-üzenet `TÖRLÉS-SZÁNDÉKOS:` sora (a forrás átszerkesztése) | folyamat |

**Ami nem kellett kézzel:** a szakaszcímke (gépi, 0 jelzés), a szótári mezők (gépi, a BDB saját példahelyeiből), a gerinc, a fordítások (subagent + kapuk), a lap generálása és fixpontja.

## 10. Javítókör a független ellenőr után (F12.9–F12.10)

A `fuggetlen-ellenor` (`claude-opus-5-5`, `cccd17a8..f58f38e8`) 15 ELTÉRÉS-t talált; a jelentés a subagent helyett a session mentésével: `naplok/ELLENOR_F12_TEREMT002_LEXIKON.md`.

| # | Eltérés | Sorsa |
|---|---|---|
| 1 | E5: négy törölt címsor, a hivatkozott F12.9 nem létezett | javítva: az F12.9 commit-üzenetének `TÖRLÉS-SZÁNDÉKOS:` sora; `futtat.py --commit-uzenet-fajl`: 0 HIBA |
| 2 | LXX: a H0922 sora a H8414-ét ismétli | javítva (F12.10): tokenenkénti verdikt a saját döntéssorból; a H0922: eltérő 1 · függőben 2. Az összesítés „LXX-minusz=0” helyes: a két `lxx_minusz` sor `valoszinu`, a DT23 szerint „függőben” jelenik meg (N-F12c) |
| 3 | A1: „a BDB-határ a motívumhatár” | javítva (F12.10): a szótári tagolás a mező két ágát választja szét, a motívumhatárt a pár húzza meg |
| 4 | sablonos LXX- és SECE-következtetés görög szó nélkül | javítva (F12.10), új ág a `olvasoi_kovetkeztetes`-ben; A/B: a kiadott lapok bájtra azonosak, a HODIT-001 és a MENNY-001 újragenerálásnál ugyanezt a javított mondatot kapná (a commitolt lapjuk nem változik) |
| 5 | ⛔ 4.7: nincs nyoma, hogy a felhasználó látta a próbalapot | a próbalap a közös jegyzetmappában állt (`F12_TEREMT-002_TUDOMANYOS_proba.md`), az éles írást az orkesztrátor hagyta jóvá a felhasználó 2026-11-02-i felhatalmazásával; a felhasználó a lapot a PR-ben és a lektor-körben látja |
| 6 | a tesztek nem zöldek | a három bukó fájl a main-en is bukik (N-F12b) |
| 7 | Rokon szavak / Új felismerés jelölés nélkül | Rokon szavak: N-F12h (a generátor-változás a kiadott lapokat is érintené); Új felismerés: tartalmi, nem mérce-blokk |
| 8 | 49:19 a `bdb_szakasz_hu.tsv`-ben | a lapon nem jelenik meg; N-F12a-hoz jegyezve |
| 9 | L2: első személyű folyamatmondatok a lapon (a tanítói rés) | javítva (F12.10): harmadik személy, a folyamat-nyom NAPLO-ban |
| 10 | a kiejtés nem egységes | javítva (F12.10): a Kivonat „tóhú vávóhú”, az Ézs 34:11 `kapcsolodas`-a kiejtéssel. A token-kiejtés (vábóhú) a generátor `kiejtes_ehhez`-éé, a jóváhagyott kiejtési szabály kimenete; a forrás nem írja |
| 11 | a kolofon „Sablon-megfelelőség” cellája üres | N-F12i (a natív motívum `sablon_verzio`-ja döntés) |
| 12 | a brief fejléce elavult | javítva (F12.11) |
| 13 | N-F12d hatóköre hiányos | javítva: hét fájl |
| 14 | a UBS H8414 `modell`-mezője | javítva: „claude-sonnet-5-5; claude-opus-5-5 (2. tag)” |
| 15 | az F12.7c nem kapott külön commitot | elismerve: a H0922 `tagolatlan` fordítássor az F12.7 (`5d2505bc`) része; a történet nem íródik át |

A javítókör után: `ellenoriz.py` SÉRTÉS 0; a `naplo`/`nyitott` zöld; a lap fixpontja megvan; kézi kiejtés-hiány 0.

## 9. Zárás

Draft PR; a brief fejléce `megallt`: a lap 6/8-on, a határ- és a lektori kör a felhasználóé, utána a 8/8, a kiadás-sor és a verzió-emelés külön tételben (DT-F12e (1)). ⛔ A merge a felhasználóé. Független ellenőrzés: `naplok/ELLENOR_F12_TEREMT002_LEXIKON.md`.
