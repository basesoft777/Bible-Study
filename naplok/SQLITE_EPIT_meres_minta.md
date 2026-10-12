# SQLITE_EPIT -- mérés (kis minta) (F79)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod minta) | ts=2026-10-12T07:33:17Z`*

- fájl: `pardes_minta.db`, **121.3 MB**; építési idő (integritás nélkül): **29.0 s**

- minta: 2110 Károli-vers (1Móz + a motívumok hivatkozott versei)

## Táblánkénti sorszám és tartalom-hash

| tábla | sor | sha256 (rendezett tartalom) |
|---|---:|---|
| `auditok` | 222 | `3606a16bb5e31aa1` |
| `bdb` | 8099 | `b03d01e3cec3d659` |
| `bdb_igehely_javitas` | 93 | `a996948f79ea157a` |
| `bsb` | 24788 | `75886fd853befadf` |
| `datasetek` | 105 | `27cbab944e79a264` |
| `dontes_hatas` | 10 | `ccc44e6d39dda48a` |
| `elofordulasok` | 259 | `0daab833faa0f4bc` |
| `forditasok` | 737 | `0dec518d81982bbe` |
| `frazis_pozicio` | 75019 | `8f3f118cdb8aec57` |
| `fts_motivum` | 624 | `02016e85fc18422e` |
| `grammatikai_strongok` | 92 | `5707058f65fb7193` |
| `igehely_tartomany` | 1087 | `e23668936ded33f7` |
| `jeloltek` | 592 | `4fe90261943153b8` |
| `kapcsolatok` | 39 | `33aa058ff673306d` |
| `kh` | 1176 | `f5494d6eafc63f25` |
| `kiejtes_heber_jeloltszabalyok` | 20 | `786b5716cf449569` |
| `kiejtes_heber_kivetelek` | 1 | `7724cfd18d14d2e3` |
| `kiejtes_kivetelek` | 5 | `3c750b8d879d7be9` |
| `kiejtes_szabalyok` | 24 | `3363984813853569` |
| `konyv` | 66 | `119690535bd1f778` |
| `kulcsszavak` | 0 | `e3b0c44298fc1c14` |
| `lexikon_hivatkozasok` | 23 | `b19b90e4323a4618` |
| `licencek` | 46 | `8c0f11b06ba4a1ff` |
| `lxx_bridge` | 3301 | `c2395bb7bc429c61` |
| `lxx_dontesek` | 90 | `1978159f0a63f203` |
| `lxx_versszintu_parok` | 12940 | `7f9e7260c6dc0ac0` |
| `morf_kulcs_heber` | 124 | `206363abdced48a9` |
| `morf_nyelv_aramai` | 7549 | `1af9d37d3c34e9a9` |
| `motivumok` | 9 | `6b7ec84b16cc78eb` |
| `normalizalas_jelentes` | 411 | `1d32a4fdb8f7094a` |
| `res_forras` | 56 | `dc612fa972ded461` |
| `strong_parok` | 571373 | `0c2b8826f890046c` |
| `strong_szotar` | 14347 | `bb4529cabf938f35` |
| `szotar_szerepek` | 26 | `fa3439efe24b5857` |
| `terminologia` | 71 | `aa2a86cc65f6e4ba` |
| `tipnr` | 2984 | `31845094edffc6a9` |
| `token_eredeti` | 42996 | `3d21a071ea1673e8` |
| `token_karoli` | 76786 | `1c5b9d567e3fa73a` |
| `token_par` | 39112 | `ea723cc19d5665ec` |
| `token_strong` | 42997 | `89525e3432ef98d2` |
| `tsk` | 26837 | `3e279247c0bd84a0` |
| `vers` | 2110 | `9d9d0ff6b8df2842` |
| `vers_szamozas` | 1917 | `c7efb7bd7a8e978e` |

## Normalizálási jelentés (G5: nincs néma nem-találat)

| tábla | ok | darab (különböző érték / előfordulás) | példák |
|---|---|---|---|
| bsb | nincs ilyen Károli-vers | 31 / 349 | `2Móz 36:38`, `4Móz 12:16`, `4Móz 30:17`, `Hós 12:15`, `Hós 13:16`, `Hós 2:23` |
| kh | nincs ilyen Károli-vers (cél-oldal) | 41 / 72 | `1Kir 4:39`, `1Kor 3:23`, `1Móz 2:28`, `1Sám 23:39`, `2Kir 22:23`, `2Kir 7:21` |
| kh | nincs ilyen Károli-vers (forrás-oldal) | 10 / 24 | `1Kor 3:23`, `Hós 11:12`, `Hós 1:12`, `Ján 1:52`, `Jób 36:34`, `Luk 23:57` |
| tipnr | Strong-szám nem normalizálható | 285 / 1397 | `G1228G`, `G2424G`, `G2455N`, `G2976G`, `G3017J`, `G3137G` |
| tipnr | nem leképezhető | 27 / 30 | `LXX.1Ki.9.20`, `LXX.Deu.20.17`, `LXX.Est.3.1`, `LXX.Est.7.9`, `LXX.Est.9.10`, `LXX.Exo.1.11` |
| tipnr | nincs ilyen Károli-vers | 17 / 37 | `1Kor 3:23`, `1Sám 23:29`, `2Kor 13:14`, `4Móz 12:16`, `4Móz 29:40`, `Dán 4:37` |

## Megjegyzések

- strong_parok: a teljes TAHOT+TAGNT-ból (31152 vers, grammatikai_strongok és H9001-H9049 nélkül), mód-független
- FTS: 50 fájl, 624 rovat; átmeneti régi tanulmányok `regi_forras=1`; a #11 `migralt: igen` jelzője miatt kiesett: nincs (a jelző még nem létezik)

## Lekérdezés-próba (M3: ADATVAGYON 4. pont, 1–6., 13–15.)

### 1. pont -- H0922 -> összes vers: **MEGEGYEZIK**

- SQL: `SELECT DISTINCT igehely FROM token_strong WHERE strong='H0922' ORDER BY igehely`
- eredmény: `['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']`
- várt: ['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']
- forrás: adat/elofordulasok.tsv TEREMT-002 (H8414+H0922, 3 sor), ADATVAGYON 4. pont mintaképe

### 2. pont -- „mélység” -> Strong-lista: **MEGEGYEZIK**

- SQL: `SELECT strong, COUNT(*) FROM token_par WHERE hu_szo='mélység' GROUP BY strong ORDER BY COUNT(*) DESC`
- eredmény: `[('H8415', 9), ('H8482', 1)]`
- várt: ['H8415 szerepel']
- forrás: adat/elofordulasok.tsv TEREMT-001 1Móz 1:2 (karoli_szo=mélység, strong=H8415)

### 3. pont -- H3548 -> Károli-szóalakok: **MEGEGYEZIK**

- SQL: `SELECT hu_szo, COUNT(*) FROM token_par WHERE strong='H3548' GROUP BY hu_szo ORDER BY COUNT(*) DESC`
- eredmény: `[('papjának', 5), ('papok', 3), ('pap', 3), ('papja', 2), ('papoknak', 1), ('papnak', 1), ('főtanácsos', 1), ('fők', 1), ('fő', 1), ('embere', 1), ('Pap', 1)]`
- várt: ['papja szerepel']
- forrás: adat/elofordulasok.tsv KIRALY-001 1Móz 14:18-20 (karoli_szo=papja, strong=H3548)

### 4. pont -- H8414 + H0922 egy versben: **MEGEGYEZIK**

- SQL: `SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely WHERE a.strong='H8414' AND b.strong='H0922' ORDER BY a.igehely`
- eredmény: `['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']`
- várt: ['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']
- forrás: adat/elofordulasok.tsv TEREMT-002 (1Móz 1:2, Jer 4:23, Ézs 34:11)

### 5. pont -- frázis: H7121 és H8034 (±6 token): **MEGEGYEZIK**

- SQL: `SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely AND b.sorszam<>a.sorszam AND ABS(b.sorszam-a.sorszam)<=6 WHERE a.strong='H7121' AND b.strong='H8034' ORDER BY a.igehely`
- eredmény: `['1Kir 18:24', '1Kir 18:25', '1Kir 18:26', '1Krón 16:8', '1Móz 11:9', '1Móz 12:8', '1Móz 13:4', '1Móz 16:11', '1Móz 16:13', '1Móz 16:15', '1Móz 17:15', '1Móz 17:19', '1Móz 17:5', '1Móz 19:22', '1Móz 19:37', '1Móz 19:38', '1Móz 21:3', '1Móz 21:33', '1Móz 22:14', '1Móz 25:25', '1Móz 25:26', '1Móz 25:30', '1Móz 26:18', '1Móz 26:20', '1Móz 26:21', '1Móz 26:22', '1Móz 26:25', '1Móz 26:33', '1Móz 27:36', '1Móz 28:19', '1Móz 29:32', '1Móz 29:33', '1Móz 29:34', '1Móz 29:35', '1Móz 2:20', '1Móz 30:11', '1Móz 30:13', '1Móz 30:18', '1Móz 30:20', '1Móz 30:21', '1Móz 30:24', '1Móz 30:6', '1Móz 30:8', '1Móz`
- várt: 22 elofordulasok-sor mindegyike szerepel (ISTENTISZT-001, gerinc H7121+H8034)
- forrás: adat/elofordulasok.tsv ISTENTISZT-001 (gerinc_elem=H7121+H8034)
- megjegyzés: hiányzó sor: - | az elvárt listán kívüli találat: 61 vers (a puszta Strong-pár a névadó „hívta a nevét” fordulatot is fogja; ez keresési találat, nem study-sor: CLAUDE.md 2. szabály) 1Móz 11:9, 1Móz 16:11, 1Móz 16:13, 1Móz 16:15, 1Móz 17:15, 1Móz 17:19, 1Móz 17:5, 1Móz 19:22, 1Móz 19:37, 1Móz 19:38, 1Móz 21:3, 1Móz 22:14

### 6. pont -- gyök (H0922, H8414): **MEGEGYEZIK**

- SQL: `SELECT strong, gyok_szarmaztatas FROM strong_szotar WHERE strong IN ('H0922','H8414')`
- eredmény: `[('H0922', 'from an unused root (meaning to be empty)'), ('H8414', 'from an unused root meaning to lie waste')]`
- várt: ['unused root mindkettőnél']
- forrás: konkordancia/Strong_szotar.tsv (Gyök/Származtatás)

### 13. pont -- BDB H7121: jelentés-sorok és a motívum tartománya: **MEGEGYEZIK**

- SQL: `SELECT l.strong, l.szotar, l.jelentes_szam, length(b.teljes_szocikk), (SELECT COUNT(*) FROM elofordulasok e WHERE e.jelentes_szam=l.jelentes_szam AND e.strong LIKE '%'\|\|l.strong\|\|'%' AND e.id='ISTENTISZT-001') FROM lexikon_hivatkozasok l JOIN bdb b ON b.strong=l.strong WHERE l.strong='H7121' AND l.szotar='BDB' ORDER BY l.jelentes_szam`
- eredmény: `[('H7121', 'BDB', '2.c', 10780, 17), ('H7121', 'BDB', '3', 10780, 2)]`
- várt: jelentes_szam: 2.c, 3; a 2.c-hez ISTENTISZT-001 sorok
- forrás: adat/lexikon_hivatkozasok.tsv, adat/elofordulasok.tsv (jelentes_szam=2.c)

### 14. pont -- LXX-híd H8415 -> G0012 -> ÚSZ: **MEGEGYEZIK**

- SQL: `SELECT greek_strong, count FROM lxx_bridge WHERE hebrew_strong='H8415' ORDER BY CAST(count AS INTEGER) DESC ; SELECT DISTINCT igehely FROM token_strong WHERE strong='G0012' ORDER BY igehely`
- eredmény: `{'hid': [('G0012', '24')], 'usz': ['Jel 11:7', 'Jel 17:8', 'Jel 20:1', 'Jel 20:3', 'Jel 9:1', 'Jel 9:11', 'Jel 9:2', 'Luk 8:31', 'Róm 10:7']}`
- várt: híd: [('G0012', '24')]; az ÚSZ-találat lefedi mind a 7 elofordulasok-sort
- forrás: adat/kulso/lxx_bridge.tsv; adat/elofordulasok.tsv TEREMT-001 (G0012)
- megjegyzés: nem lefedett elofordulasok-sor: - (a tartomány-sorok, pl. Jel 20:1-3, egy versen kapnak találatot)

### 15. pont -- kiejtés (H8415, 1Móz 1:2): **MEGEGYEZIK**

- SQL: `SELECT DISTINCT kiejtes FROM token_eredeti WHERE igehely='1Móz 1:2' AND strong_lanc='H8415'`
- eredmény: `['te.Hom']`
- várt: ['te.Hom']
- forrás: konkordancia/Strong_szotar.tsv H8415 Kiejtés

