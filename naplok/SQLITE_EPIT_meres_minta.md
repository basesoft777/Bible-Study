# SQLITE_EPIT -- mérés (kis minta) (F79)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod minta) | ts=2026-10-12T07:39:49Z`*

- fájl: `t.db`, **121.3 MB**; építési idő (integritás nélkül): **29.4 s**

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

## A `licenc_*` oszlopok helyfoglalása (a #86 N-F86b bemenete)

A három oszlop (`licenc_allapot`, `kereskedelmi`, `licenc_dataset`) minden sorban ismétlődik. Az alábbi bájtszám az oszlopok tartalma (rekord-fejléc és index nélkül, alsó becslés).

- összesen: **40.8 MB** a **121.3 MB**-os fájlból (33.6%)

| tábla | sor | licenc_* bájt | MB |
|---|---:|---:|---:|
| `strong_parok` | 571373 | 27425904 | 26.16 |
| `token_karoli` | 76786 | 4146444 | 3.95 |
| `frazis_pozicio` | 75019 | 4051026 | 3.86 |
| `token_par` | 39112 | 2112048 | 2.01 |
| `token_strong` | 42997 | 1074925 | 1.03 |
| `token_eredeti` | 42996 | 1074900 | 1.03 |
| `bsb` | 24788 | 619700 | 0.59 |
| `lxx_versszintu_parok` | 12940 | 569360 | 0.54 |
| `tsk` | 26837 | 456229 | 0.44 |
| `strong_szotar` | 14347 | 387369 | 0.37 |
| `morf_nyelv_aramai` | 7549 | 271764 | 0.26 |
| `bdb` | 8099 | 121485 | 0.12 |

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

