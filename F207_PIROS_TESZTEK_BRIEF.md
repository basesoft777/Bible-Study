---
feladat: 207
cim: A gyors tesztsor piros tesztjei — gyökérok szerint (elavult teszt, kódhiba, elavult adatbázis)
kod: PIROS_TESZTEK
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/lucid-tesla-29681d
ad: a `python eszkozok/teszt_futtat.py --gyors` újra zöld; minden bukás besorolva (a/b/c), a tiltott fájlokba nem nyúltunk
kovetkezo: "Te: a draft PR áttekintése; merge-et az orkesztrátor végzi"
munka: folyamat
olvas: [eszkozok/teszt_futtat.py, eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_pilot/db_meres.py, eszkozok/teszt_szotari_gerinc.py]
ir: [eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_pilot/db_meres.py, eszkozok/teszt_szotari_gerinc.py, nyitott/uj/lucid-tesla-29681d.md]
fugg: []
nem_fugg: []
---

# F207_PIROS_TESZTEK_BRIEF.md — A gyors tesztsor piros tesztjei

*FELADATOK #207 · Modell: claude-sonnet-5-5 · v1 · 2026.11.12*

**Hatókör.** A gyors tesztsor (`teszt_futtat.py --gyors`) bukásai és a #182 által jelzett `teszt_szotari_gerinc.py`. A `lexikon_general.py`, az olvasói kapu, `bdb_jelolt/*`, `thayer_jelolt/*`, `adat/*`, `lexikon/*`, `sablonok/*` érintetlen.

## Futtatási környezet
A `~/pardes/pardes.db` (WSL-natív) 2026-11-02-i, 1048 MB — **elavult** az `adat/`-hoz képest (a `bdb_szakasz_hu`-ban 674 Strong, a repóban több; a `forditasok` 2026-11-02-ig). Ezért a régi DB-vel két további teszt is piros volt (`test_kattinthato_helyek`, `test_bdb_jelentesszerkezet_jeloloi_a_szocikkbol`): **(c)**, a friss DB-vel zöldek. A mérés a friss DB-vel készült: `python eszkozok/sqlite_epit.py --mod teljes --kimenet /home/basesoft/f207_proba.db` (746 mp), `PARDES_DB=/home/basesoft/f207_proba.db`. A közös DB cseréje (`indit.sh` szinkron a Desktop-példányról, amely szintén 2026-11-02-i) a felhasználó/orkesztrátor dolga: N-F207e.

## A bukások és az okuk (friss DB-vel)
| Teszt | Ok | Besorolás | Javítás |
|---|---|---|---|
| `teszt_olvaso_szerver` `TestD2PilotEgyezes.test_1moz_1_25`, `test_zsolt_22` | az F187.2 (`9861d9cf`, N-F186g) az `adat.py`-ban és a `lekerdezesek.magyar_gorog`-ban csak az érvényes (nem `elavult`, nem `~`) Thayer/UBS-sort számolja; a `db_meres.db_gorog` még mindet | **(b)** a mérőeszköz | `db_meres.py`: ugyanaz a szűrés |
| `teszt_pilot_aranymintaval` F76g | az F182.10 (`09c74179`) óta a bontás a szakasztáblából épül (`bdb_tagolas`), nem a pilot szeletelőjéből; a pilot aranya mind a 256 lapnál eltér (`fej.cimke`, `irodalom`, `krit`, …) | **(a)** a teszt | a tartalom-egyezés helyett szerkezet-invariáns; a tartalmat a `teszt_bdb_tagolas.py` fedi; a hu/meta/alias egyezés megmarad |
| ugyanott, **H4725** | a szakasztáblában (`adat/bdb_szakaszok.tsv`) nincs sora, noha van BDB-szócikke és magyar fordítása | **adathiány** (tiltott terület) | önlejáró kivétel a tesztben (`BDB_TAGOLAS_HIANYZIK`), N-F207a |
| `teszt_pilot_aranymintaval` F76f | ugyanaz az ok (az `alap` a szakasztáblából jön); ráadásul a H0559 alapjelentése hivatkozást hordozott („… mondani Gen 3:17”) | **(a)** + **(b)** | a teszt az invariánst nézi (közös `alap_jelentes`, nincs `\d+:\d+`); új `blokkok._alap_jelentes`: a sor végi hivatkozás levágva a közös `bdb_szelet.alap_jelentes` előtt (a `bdb_szelet.py` kód-hash-e a generált `adat/bdb_vers_jelentes.tsv` fejében áll: a módosítása a `teszt_bdb_vers_jelentes.test_bajtra_azonos`-t buktatta, ezért ott nem módosítunk) |
| `teszt_szotari_gerinc.test_kapcsolo` | a HAMART-001 migrált (`51949f07`), a kivétellistán nincs | **(a)** | a teszt `aktiv`-ot vár |

## Nem javított (határ vagy tartalom) — helyőrzős nyitott tételek
- **N-F207a** H4725 hiányzó szakasztábla-sor (`adat/*`).
- **N-F207b** `teszt_szotari_gerinc`: öt bukás (`test_33_sor`, `test_sz_sorok_es_tiltott`, `test_13`, `test_14`, `test_13_es_14_mondat`) — az ISTENTISZT-001 33 → 22 sorra (F152.14, `4dd8bba6`, DT-F152b/c): **(a)**, de a számok (22 hely, 13 szó, 91%, 37% …) az ISTENTISZT új cikkével még változhatnak.
- **N-F207c** `teszt_szotari_gerinc`: két F187-kártyateszt (`test_c_apparatusban_olvashato_forras_hivatkozas`, `test_c_szocikk_neve_sorszam_es_azonosito_nelkul`) — a gyökérok a generátorban/kártyában (`lexikon_general.py`, #699 alatt).
- **N-F207d** `bdb_szelet.alap_jelentes`: a szakasztáblából jövő `alap` néhol nem jelentést ad (H1875 „Ezsd”, H4723 „-ben l”, H5608/H6030 csonka) — a gyökérok a szakasztábla fejének bontásában.
- **N-F207e** a közös `pardes.db` újraépítése/szinkronja (**(c)**).

## Kész
`python eszkozok/teszt_futtat.py --gyors` a friss DB-vel: l. a PR leírása.
