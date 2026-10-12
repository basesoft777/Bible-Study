# SQLITE_EPIT -- mérés (teljes építés) (F79)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod teljes) | ts=2026-10-12T07:42:51Z`*

- fájl: `pardes.db`, **786.1 MB**; építési idő (integritás nélkül): **42.0 s**

## Táblánkénti sorszám és tartalom-hash

| tábla | sor | sha256 (rendezett tartalom) |
|---|---:|---|
| `auditok` | 222 | `3606a16bb5e31aa1` |
| `bdb` | 8099 | `b03d01e3cec3d659` |
| `bdb_igehely_javitas` | 93 | `a996948f79ea157a` |
| `bsb` | 277817 | `ee19c1705c006067` |
| `datasetek` | 105 | `27cbab944e79a264` |
| `dontes_hatas` | 10 | `ccc44e6d39dda48a` |
| `elofordulasok` | 259 | `0daab833faa0f4bc` |
| `forditasok` | 737 | `0dec518d81982bbe` |
| `frazis_pozicio` | 893397 | `61c6c38327c8ef68` |
| `fts_motivum` | 624 | `02016e85fc18422e` |
| `grammatikai_strongok` | 92 | `5707058f65fb7193` |
| `igehely_tartomany` | 1087 | `e23668936ded33f7` |
| `jeloltek` | 592 | `4fe90261943153b8` |
| `kapcsolatok` | 39 | `33aa058ff673306d` |
| `karoli_variancia` | 42799 | `0f4a32248d4a1a02` |
| `kh` | 32407 | `95e3bca5771391db` |
| `kiejtes_heber_jeloltszabalyok` | 20 | `786b5716cf449569` |
| `kiejtes_heber_kivetelek` | 1 | `7724cfd18d14d2e3` |
| `kiejtes_kivetelek` | 5 | `3c750b8d879d7be9` |
| `kiejtes_szabalyok` | 24 | `3363984813853569` |
| `konyv` | 66 | `119690535bd1f778` |
| `kulcsszavak` | 0 | `e3b0c44298fc1c14` |
| `lexikon_hivatkozasok` | 23 | `b19b90e4323a4618` |
| `licencek` | 46 | `8c0f11b06ba4a1ff` |
| `lsj` | 5522 | `4ed5a849db089aac` |
| `lxx_bridge` | 3301 | `c2395bb7bc429c61` |
| `lxx_dontesek` | 90 | `1978159f0a63f203` |
| `lxx_versszintu_parok` | 104518 | `d02bcff50a3191d6` |
| `mcged` | 5303 | `5af29f685a424bea` |
| `morf_kulcs_heber` | 124 | `206363abdced48a9` |
| `morf_nyelv_aramai` | 7549 | `1af9d37d3c34e9a9` |
| `motivumok` | 9 | `6b7ec84b16cc78eb` |
| `nave_basokant` | 85246 | `62e5001364e4a121` |
| `normalizalas_jelentes` | 2869 | `b35cb9ac89809152` |
| `oshl_bdb_igehelyek` | 4053 | `7183aa23ee59878f` |
| `oshl_lexikalis_index` | 10221 | `88c18fcc8187d1a4` |
| `res_forras` | 56 | `dc612fa972ded461` |
| `sdbh_domenek` | 22280 | `7820f7cc90062424` |
| `sdgnt_domenek` | 9075 | `67edd94815da195d` |
| `sece_g` | 5523 | `e98f405337069580` |
| `sece_h` | 8674 | `6de1a0614762c519` |
| `strong_parok` | 571373 | `0c2b8826f890046c` |
| `strong_szotar` | 14347 | `bb4529cabf938f35` |
| `szotar_szerepek` | 26 | `fa3439efe24b5857` |
| `terminologia` | 71 | `aa2a86cc65f6e4ba` |
| `thayer` | 5426 | `30c9e70e4f70584b` |
| `tipnr` | 35522 | `09bc3fc2a80311c2` |
| `token_eredeti` | 611046 | `2e5cd212165db10f` |
| `token_karoli` | 926179 | `353a6e7d10230822` |
| `token_par` | 466785 | `d1b0a20b21ea1b60` |
| `token_strong` | 611304 | `15f82e2751e3c425` |
| `tsk` | 432949 | `f52ca5dd959490bb` |
| `tw_szocikkek` | 598 | `26ff279266dc5ae9` |
| `ubs_dbh_jelentesek` | 20182 | `86d4d0f6b6361ae6` |
| `ubs_dbh_referenciak` | 389212 | `fcf6ea52341c2efa` |
| `ubs_dntg_jelentesek` | 9075 | `335d4fb7b3a63d76` |
| `ubs_dntg_referenciak` | 130948 | `a34483703b7336a1` |
| `vers` | 31158 | `120ad7544c1f5956` |
| `vers_szamozas` | 22931 | `23e40f6e7d3e9ef4` |

## A `licenc_*` oszlopok helyfoglalása (a #86 N-F86b bemenete)

A három oszlop (`licenc_allapot`, `kereskedelmi`, `licenc_dataset`) minden sorban ismétlődik. Az alábbi bájtszám az oszlopok tartalma (rekord-fejléc és index nélkül, alsó becslés).

- összesen: **212.1 MB** a **786.1 MB**-os fájlból (27.0%)

| tábla | sor | licenc_* bájt | MB |
|---|---:|---:|---:|
| `token_karoli` | 926179 | 50013666 | 47.70 |
| `frazis_pozicio` | 893397 | 48243438 | 46.01 |
| `strong_parok` | 571373 | 27425904 | 26.16 |
| `token_par` | 466785 | 25206390 | 24.04 |
| `token_strong` | 611304 | 15282600 | 14.57 |
| `token_eredeti` | 611046 | 15276150 | 14.57 |
| `ubs_dbh_referenciak` | 389212 | 8173452 | 7.79 |
| `tsk` | 432949 | 7360133 | 7.02 |
| `bsb` | 277817 | 6945425 | 6.62 |
| `lxx_versszintu_parok` | 104518 | 4598792 | 4.39 |
| `ubs_dntg_referenciak` | 130948 | 2880856 | 2.75 |
| `karoli_variancia` | 42799 | 2311146 | 2.20 |

## Normalizálási jelentés (G5: nincs néma nem-találat)

| tábla | ok | darab (különböző érték / előfordulás) | példák |
|---|---|---|---|
| bsb | nincs ilyen Károli-vers | 31 / 349 | `2Móz 36:38`, `4Móz 12:16`, `4Móz 30:17`, `Hós 12:15`, `Hós 13:16`, `Hós 2:23` |
| kh | nincs ilyen Károli-vers (cél-oldal) | 41 / 72 | `1Kir 4:39`, `1Kor 3:23`, `1Móz 2:28`, `1Sám 23:39`, `2Kir 22:23`, `2Kir 7:21` |
| kh | nincs ilyen Károli-vers (forrás-oldal) | 10 / 24 | `1Kor 3:23`, `Hós 11:12`, `Hós 1:12`, `Ján 1:52`, `Jób 36:34`, `Luk 23:57` |
| oshl_bdb_igehelyek | Strong-szám nem normalizálható | 1 / 397 | `—` |
| oshl_lexikalis_index | Strong-szám nem normalizálható | 1 / 930 | `—` |
| tipnr | Strong-szám nem normalizálható | 2741 / 16928 | `G0001G`, `G0007G`, `G0007H`, `G0039G`, `G0039H`, `G0129H` |
| tipnr | nem leképezhető | 27 / 30 | `LXX.1Ki.9.20`, `LXX.Deu.20.17`, `LXX.Est.3.1`, `LXX.Est.7.9`, `LXX.Est.9.10`, `LXX.Exo.1.11` |
| tipnr | nincs ilyen Károli-vers | 17 / 37 | `1Kor 3:23`, `1Sám 23:29`, `2Kor 13:14`, `4Móz 12:16`, `4Móz 29:40`, `Dán 4:37` |

## Megjegyzések

- strong_parok: a teljes TAHOT+TAGNT-ból (31152 vers, grammatikai_strongok és H9001-H9049 nélkül), mód-független
- FTS: 50 fájl, 624 rovat; átmeneti régi tanulmányok `regi_forras=1`; a #11 `migralt: igen` jelzője miatt kiesett: nincs (a jelző még nem létezik)
- Nem betöltött konkordancia-táblák (a DT-F79a és a brief hatóköre nem nevezi őket): Macula_heber_*/Macula_gorog, LXX_OS/*, KJV_Strongs_teljes és KJV_/ASV_Strongs_* (a #48 vezeti ki), TBESG/TBESH, Karoli_Strong_kivonat, a BDB_*/aram/alias segédtáblák, SDBH_SDGNT_domenfa; a licenc-sor hiánya miatt kimaradt táblák száma: 0

