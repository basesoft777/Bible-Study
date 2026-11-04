# F123.BDBGER — a BDB-gerinc szócikk-összevonása (az N98 második fele)

*scope=adat/bdb_szakaszok.tsv (2.30) + adat/bdb_vers_jelentes.tsv (2.29) + adat/bdb_szakasz_hu.tsv (2.32) + konkordancia/BDB_teljes_unabridged.tsv + adat/elofordulasok.tsv + lexikon/*_TUDOMANYOS.md (9 lap; az ANTROP-001 a PR #608 ágán, ab54fbf5) | forras=naplok/F123_BDBGER_meres.py (kimenet: naplok/F123_BDBGER_meres_kimenet.txt) + eszkozok/general.py --cel lexikon --id <ID> --kimenet <repón kívül> előtte/utána + diff | ts=2026-11-03*

Modell: `claude-opus-5-5`.

## 1. Az ok

A `lexikon_general.py` `bdb_gerinc_szakaszok`-ja a 2.30 sorait csak az útvonal (`utvonal`) szerint vonta össze, és a
gerinc többi része (`teljes_ut`, a hordozó-halmaz, a kiemelési célok, a `szotar_szakasz_cimke.tsv` kulcsa) is csak
útvonal-kulcsú volt. Egy Strongnak viszont több BDB-szócikke lehet (`bdb_id`: I., II., arámi), és az útvonal
(`-/1/-`) csak a szócikken belül egyedi. Ezért a több szócikkű Strong különböző szócikkeinek azonos útvonalú
szakaszai egy szakaszba folytak össze, és a szócikkek feje is egy fejbe. Igazolt eset (PR #608 ágán, a javítás
előtt): a H2416 kibontott `1` szakasza a BDB2718 („állat, mint élő, tevékeny lény:”), a BDB2721 („1 élet: testi …”)
és a BDB9522 (arámi) szövegét fűzte egybe; a rövid fejsor „rokon nyelvi adat: arab”-ja a BDB2717 (rokonság)
fejéből szivárgott át.

A DT589 (1) (a) próbája csak az összevonást kulcsolta át, ezért bukott (a hordozó-halmaz és a kiemelés
útvonal-kulcsú maradt: mindhárom `1` kibontva, az arámi szöveg kétszer). Ebből a tanulság: a kulcsot **mindenütt**
cserélni kell, és a 2.29 példahelyének is szócikket kell kapnia — a 2.29 `bdb_id` oszlopa ugyanis nem a 2.30
azonosítója (az OSHL-azonosítók listája, pl. `h.cd.ab,…`).

## 2. Számok

| Mérés | Érték |
|---|---|
| Strong a 2.30-ban | 8 090 |
| több BDB-szócikkű Strong | 1 583 |
| ebből a régi generátor összevonta a fejüket | 1 583 (mind) |
| ebből a fejen kívüli útvonalat is több szócikkből vont össze | 133 |
| szócikken belül nem szomszédos ismétlődő útvonal (nem e tétel tárgya, N-F123gc) | 231 |
| 2.29-sor a több szócikkű Strongokban (szurt≠1, Károli-verssel) | 58 476 |
| — szócikk az útvonalból (egy szócikkben áll) | 42 018 |
| — szócikk a helyből (`poz`; útvonal több szócikkben vagy fej) | 14 375 |
| — nem azonosítható (a lapon explicit ⓘ, választás nélkül) | 2 083 |
| a hely ellenőrzése az útvonalból egyértelmű 41 050 soron: egyezik / ellentmond | 40 462 / 588 (579 egyértelműen) |
| Strong, amelyben a hely ezért nem dönt (N-F123gb) | 102 |
| 2.32 szócikkhatáron át elnyelt (jelölő nélküli, magyar szöveg nélküli) sor (N-F123ga) | 192 Strong, 264 sor |

A feladatleírás felső becslése (427 Strong, ebből 24 lapon, pl. H3068, H3605, H4672, H6213) nem ugyanez a mérés:
a H3068, H4672, H6213 ismétlődése szócikken belüli (a 231-es osztály), a H3068 nem is szerepel az
`elofordulasok.tsv`-ben. A 2.30 szerint az `elofordulasok.tsv` H-tokenjei közül 10 több szócikkű, ebből 2-ben
(H2416, H7451) a fejen kívüli útvonal is ütközött.

A hely szerinti azonosítás: a 2.30 sorainak szövegét a teljes angol szócikk `lapit`-alakjában (a 2.29 `poz`-ának
koordinátáiban) sorban megkeresem; a `poz` szócikk-jelöltjei az előtte kezdődő utolsó megtalált sor és a következő
megtalált sorig a nem megtalált sorok szócikkei. A hely csak akkor dönt, ha a Strongban az útvonalból egyértelmű
minden soron egyezik az útvonallal (önellenőrzés); a 102 eltérő Strongban (főleg H0834, H3162, H5973, H0227) nem.

## 3. A kilenc lap — hol fűzött össze a régi generátor

| Lap | Gerinc | Több szócikkű Strong | Régi összevonás | 2.32 elnyelés |
|---|---|---|---|---|
| ALVIL-001 | aktív | H7585 (BDB8371, BDB8375) | fej | BDB8375 fej → BDB8371 fej |
| ANTROP-001 | a main-en nem; a #608 ágán aktív | H2416 (7 szócikk) | `-/1/-`, `-/1/a`, `-/1/b`, `-/1/c`, `-/2/-`, `-/3/-`, fej | — (szakaszos fordítás) |
| HAMART-001 | nem | H2403 (2), H7451 (3) | H2403 fej; H7451 `-/1/-`, `-/2/-`, `-/3/-`, fej | H2403: BDB9520 fej → BDB2699 `5`; H7451: BDB8033 fej → BDB8032 `10.d`, BDB8034 fej → BDB8033 `3` |
| HODIT-001 | nem | H7496 (2) | fej | BDB8060 fej → BDB8044 fej |
| ISTENTISZT-001 | aktív | H8034 (BDB8776, BDB9963 arámi) | fej (az arámi szócikk el is tűnt a lapról) | BDB9963 fej → BDB8776 `5` |
| KIRALY-001 | nem | H3548, H3678, H4467 (2–2) | fej | mindháromban a második szócikk feje az elsőben |
| MENNY-001 | nem | H1121 (2) | fej | BDB1169 fej → BDB1160 `9.b` |
| TEREMT-001 | nem | — | — | — |
| TEREMT-002 | aktív | — | — | — |

A nem gerinces lapokon a régi összevonás nem látszott (a gerinc nem renderelődik), de a gerinc bekapcsolásakor
megjelent volna (a #123 migrációja ezeket sorra bekapcsolja). A 2.29 nem azonosítható sorai a lapokon: H2416 25
(Dán/Ezsd: a 2.29 szeletelője az arámi részt a חיים `3`-ához sorolja, a hely szerint a BDB9522/9523-ban áll — a két
forrás ellentmond, nem választ), H7451 22, H1121 29 (itt a hely nem megbízható); a H7585, H8034, H2403, H7496,
H3548, H3678, H4467 mind azonosítható.

## 4. A javítás

- `eszkozok/lexikon_general.py`: a szakasz kulcsa (`bdb_id`, útvonal) — `bdb_gerinc_szocikkek` (szócikkenként, a
  2.30 sorrendjében; az elnyelt sorok `elnyelt` térképe), `bdb_vers_szocikk` (a 2.29 sorának szócikke),
  `kutatoi_szakasz` → (bdb_id, szakasz), `jelentes_cimke_token`, `bdb_tartomanyban`, `gerinc_blokk`,
  `gerinc_szakasz_lista`; a több szócikkű Strong a lapon szócikkenként, saját fejcímmel
  (`**BDB2718 · I. חַיָּה** *(a H2416 3. BDB-szócikke a 7-ből)*`; az arámi a BDB9264-től `· arámi`,
  `konkordancia/BDB_aram_potlas_README.md`); a jel csak akkor kap szócikk-előtagot (`BDB2721 1`), ha az útvonal a
  Strong több szócikkében is áll; az elnyelt szakasz/fej a lapon kimondja, hol áll a szövege, a kiemelés oda mutat.
  A rövid fejsor (8. szerep) az első szócikk feje.
- `adat/szotar_szakasz_cimke.tsv` (SEMA 2.40): új `bdb_id` oszlop a `strong` után; a régi → új kulcs leképezése
  `naplok/F123_BDBGER_cimke_lekepezes.tsv` (19 sor, ebből 14 BDB, mind egyértelmű: H7121 → BDB7550, H8034 →
  BDB8776, H7585 → BDB8375, H8414 → BDB9112); író: `naplok/F123_BDBGER_cimke_migracio.py` (írás előtt és után
  összevet; a #608 ágán is egyértelmű: 28 sor, 15 BDB, a H5315 → egy szócikk).
- `eszkozok/ellenoriz.py` 17. szabály: a kulcs (szotar, strong, bdb_id, szakasz); BDB-sorban a `bdb_id` kötelező, és
  a szakasz ennek a szócikknek az útvonala; 18. szabály: a generátor kulcsával. Új **27. szabály** (DT-F123gb).
- `eszkozok/ellenorzes/szabalyok.py` E19: a kutatói leképezés szakaszai a szócikk soraira szűkítve.
- `eszkozok/szakasz_cimke_levezet.py`: a gépi levezetés szócikk-tudatos (a több szócikkben álló számozás J2, „több
  szócikk”, nem választ); a tábla írója az új oszloppal.

## 5. Laponkénti diff (előtte ↔ utána, mindkettő repón kívül, nulláról generálva)

`general.py --cel lexikon --id <ID> --kimenet <scratch>`, a javítás előtt (HEAD b9b38bff) és után; az előtte-változat a
gerinces lapokon (ALVIL-001, ISTENTISZT-001, TEREMT-002) bájtra egyezik a commitolttal (sorvég nélkül).

| Lap | Diff (sor) | Mi változik |
|---|---|---|
| ALVIL-001 (kiadott) | 10 | H7585: két szócikkfej (`BDB8371 · שְׁאָ֫לָה`, `BDB8375 · שְׁאֹל`); a BDB8371 fején a teljes magyar fej (a 2.32 szerint ott áll), a BDB8375 fején a jelzés, hogy a szövege ott áll; a gerinc ⓘ-je az elnyelés forrását nevezi meg. A kiemelések és a többi ⓘ-tétel bájtra azonos. |
| ISTENTISZT-001 (kiadott) | 10 | H8034: két szócikkfej (`BDB8776 · I. שֵׁם`, `BDB9963 · שֻׁם · arámi` — az arámi szócikk eddig nem látszott); az összecsukott `5` jelzi, hogy az arámi fej szövegét is tartalmazza; a gerinc ⓘ-je bővül. A kiemelések és a többi ⓘ-tétel bájtra azonos. |
| TEREMT-002 | 0 | (H0922, H8414 egy szócikkűek) |
| ANTROP-001 (main) | 0 | (a main-en a gerinc nem aktív) |
| ANTROP-001 (PR #608 ága, ab54fbf5) | 60 | H2416: hét szócikk saját fejjel; a kibontott `1` a BDB2721 („élet: testi …”) egyedül, az `1.d` a BDB2716-é; a BDB2718 `1`–`4` összecsukva a saját szócikkében; a rövid fejsorból kiesik a „rokon nyelvi adat: arab” (a BDB2717 fejéből szivárgott át); egy ⓘ-mondatban az `1., 1.d` → `1.d, BDB2721 1` |
| HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 | 0 | (a gerinc nem aktív) |

Kézi próza egyik lapon sem változik: minden eltérés a 2. szerep szótári gerincében, a gerinc ⓘ-jében, egy
proveniencia-lábjegyzetben és a 8. szerep generált rövid fejsorában áll. A diffek: a jegyzetmappa
`BDB_GERINC_lapdiff/` könyvtára.

## 6. Kapuk és tesztek (a munkafában, a két kiadott lap újragenerált változatával)

| Kapu | Eredmény |
|---|---|
| `ellenoriz.py` | SÉRTÉS 0 (17., 18., 26. RENDBEN; 27. JELENTÉS 2: a H7585 és a H8034 elnyelése). A régi lapokkal: 27. SÉRTÉS 2 (ALVIL-001 H7585, ISTENTISZT-001 H8034). |
| olvasói kapu (`olvasoi_kapu.py`) | ALVIL-001 0 BUKÁS / 13 FIGY., ISTENTISZT-001 24 / 7, TEREMT-002 17 / 28 — bájtra azonos a HEAD-del; ANTROP-001 (#608) 0 / 15, előtte is |
| helyi CI (`ellenorzes/futtat.py` a változott fájlokra) | E16: a PR címe `[ELLENŐRZŐ]` előtagot kér (a PR-nél); E28: a commitolt lap eltér az újragenerálttól — a lapok commitjával szűnik meg (⛔) |
| `ellenorzes/tesztek/test_szabalyok.py` | 209/209 OK |
| `feladatok.py ellenoriz` | 181 brief, 0 hiba |
| `teszt_feladatok.py`, `teszt_olvasoi_kapu.py` | OK |
| `teszt_szotari_gerinc.py` | 68 teszt, 5 bukik — ugyanaz az 5, mint a HEAD-en (N-F123gd); az új `SzocikkKulcs` és `Szabaly27` (6 teszt) zöld |
| `teszt_szakasz_cimke_levezet.py` | 21 teszt, 2 bukik — ugyanaz a 2, mint a HEAD-en (N-F123gd); az új `test_tobb_szocikk` zöld |
| `teszt_ellenoriz_vedokorlat.py` | 1 bukik (`test_20_21_a_repon`) — a HEAD-en is |

## 7. Ami nem e tételé

N-F123ga (a `hu_illeszt.py` elnyelése), N-F123gb (a 2.29 saját `bdb_id`-je), N-F123gc (szócikken belüli ismétlés),
N-F123gd (a main-en is bukó tesztek). A PR #608 rebase-ekor a `szotar_szakasz_cimke.tsv` új sorait a
`naplok/F123_BDBGER_cimke_migracio.py` szerint kell átkulcsolni (a H5315 sora egy szócikkű, egyértelmű), és az
ANTROP-001 lapot újragenerálni.

## 8. Átnézés (DT569 mintája, DT-F123ga)

- ALVIL-001: az átnézés érvényes marad, a változott lapra (lap-commit cfb10b07) új sor az `adat/lap_atnezesek.tsv`-ben, a `naplok/F123_atnezes_ALVIL-001.md` mondatával.
- ISTENTISZT-001: az átnézés érvényes marad (csak a generált szótári gerinc változott: H8034 két szócikkfej, az arámi BDB9963 láthatóvá vált; próza és az olvasói kapu bájtra azonos); a lapnak az `adat/lap_atnezesek.tsv`-ben nincs sora, új kiadásszám nem kell.
