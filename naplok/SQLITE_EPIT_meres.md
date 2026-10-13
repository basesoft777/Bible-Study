# SQLITE_EPIT -- mérés (teljes építés) (F79)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py (--mod teljes) | ts=2026-10-13T11:02:35Z`*

<!-- F89-ELOTTE-KEZDET -->
## F89 előtte: a sor-szintű `licenc_*` oszlopokkal (a licenc-váltás előtti mérés)

*Proveniencia: `scope=a jelen fájl korábbi, F79-ös teljes építési mérése (git: a F89.3 előtti állapot) | forras=eszkozok/sqlite_epit.py --mod teljes --ketszer --meret --naplo | ts=2026-10-13T05:53:37Z`*

- fájl: `pardes.db`, **878.9 MB**; építési idő (integritás nélkül): 50.1 s
- a táblák összege 879.1 MB; a `licenc_allapot`, `kereskedelmi`, `licenc_dataset` oszlopok összes részesedése: **259.9 MB (29.6%)**
- a `tisztazatlan` állapotú sorok oka: a `projekt_adat` sor `tisztazatlan` volt (a `Karoli_Strong_*` táblák licencsora hiányzott)
- **utána (F89, a lenti mérés): `pardes.db` 619.0 MB, 65 adattábla + `tabla_licenc` = 66 tábla; a különbség 259.9 MB (29.6%), azaz pontosan a korábbi sor-szintű `licenc_*` oszlopok részesedése.** Proveniencia: `scope=pardes.db teljes építés (--mod teljes --ketszer --meret --naplo) | forras=eszkozok/sqlite_epit.py @ F89.3, adat/licencek.tsv @ F89.2 | ts=2026-10-13`
- G6 (determinizmus): a második, ideiglenes építés táblánkénti hash-e mind azonos (lent).
<!-- F89-ELOTTE-VEGE -->

- fájl: `pardes.db`, **871.2 MB**; építési idő (integritás nélkül): **76.3 s**

## Táblánkénti sorszám és tartalom-hash (G2: két egymás utáni építés)

**AZONOS** -- a második, ideiglenes építés táblánkénti rendezett tartalom-hash-e mind azonos.

| tábla | sor | sha256 (1. építés) | sha256 (2. építés) |
|---|---:|---|---|
| `auditok` | 222 | `ff0b81ca81304142` | `ff0b81ca81304142` |
| `bdb` | 8099 | `2ca2507b37f42492` | `2ca2507b37f42492` |
| `bdb_alias` | 460 | `240ac43c6b7e06e8` | `240ac43c6b7e06e8` |
| `bdb_igehely_javitas` | 93 | `5f885473b14841eb` | `5f885473b14841eb` |
| `bdb_karoli` | 62526 | `cc27eaa08d54fae5` | `cc27eaa08d54fae5` |
| `bsb` | 277817 | `4b24bc5224e67e83` | `4b24bc5224e67e83` |
| `datasetek` | 105 | `1d3885285a09a685` | `1d3885285a09a685` |
| `dontes_hatas` | 10 | `91cd5e7d73cf45c1` | `91cd5e7d73cf45c1` |
| `elofordulasok` | 259 | `44055e771f0ecda1` | `44055e771f0ecda1` |
| `forditasok` | 737 | `e89fa68a4a1f06ae` | `e89fa68a4a1f06ae` |
| `frazis_pozicio` | 941747 | `7dfad52aeb6f9c61` | `7dfad52aeb6f9c61` |
| `fts_motivum` | 624 | `633891ec0abcdcf5` | `633891ec0abcdcf5` |
| `grammatikai_strongok` | 92 | `c506e4015b2c0c91` | `c506e4015b2c0c91` |
| `igehely_tartomany` | 1087 | `520d9f4f840fc6b5` | `520d9f4f840fc6b5` |
| `jeloltek` | 592 | `a2ec01077075640f` | `a2ec01077075640f` |
| `kapcsolatok` | 39 | `d2fafe8c49ccc81f` | `d2fafe8c49ccc81f` |
| `karoli_strong_kivonat` | 383 | `a379213a4e0bc6bb` | `a379213a4e0bc6bb` |
| `karoli_variancia` | 42799 | `5a9ac67d6e6c51d1` | `5a9ac67d6e6c51d1` |
| `kh` | 32407 | `68eb4cbd78ec3508` | `68eb4cbd78ec3508` |
| `kiejtes_heber_jeloltszabalyok` | 20 | `70347451bb064d77` | `70347451bb064d77` |
| `kiejtes_heber_kivetelek` | 1 | `c8d5b893f05d9328` | `c8d5b893f05d9328` |
| `kiejtes_kivetelek` | 5 | `df6dcdea66e3260b` | `df6dcdea66e3260b` |
| `kiejtes_szabalyok` | 24 | `27d3d4eeab3064e7` | `27d3d4eeab3064e7` |
| `kjv` | 348606 | `3f610b1b66a047c2` | `3f610b1b66a047c2` |
| `konyv` | 66 | `7a8105bcd736412f` | `7a8105bcd736412f` |
| `kulcsszavak` | 0 | `e3b0c44298fc1c14` | `e3b0c44298fc1c14` |
| `lexikon_hivatkozasok` | 23 | `01a7bcf42d1941de` | `01a7bcf42d1941de` |
| `licencek` | 49 | `d691fbae40940757` | `d691fbae40940757` |
| `lsj` | 5522 | `69dd9789f79473d3` | `69dd9789f79473d3` |
| `lxx_bridge` | 3301 | `ec2b0ab84f1e82cc` | `ec2b0ab84f1e82cc` |
| `lxx_dontesek` | 90 | `319907495acc63f9` | `319907495acc63f9` |
| `lxx_token` | 616873 | `f2d57f0950e55a0b` | `f2d57f0950e55a0b` |
| `lxx_versszam` | 24232 | `bd70d222a8b64479` | `bd70d222a8b64479` |
| `lxx_versszintu_parok` | 104518 | `e5df63a54e7e715b` | `e5df63a54e7e715b` |
| `mcged` | 5303 | `0ec3cb35b769c931` | `0ec3cb35b769c931` |
| `morf_kulcs_heber` | 124 | `a8a99f9c96eaa270` | `a8a99f9c96eaa270` |
| `morf_nyelv_aramai` | 7549 | `ef2f696a0992e0f5` | `ef2f696a0992e0f5` |
| `motivumok` | 9 | `c4edba7875e2080b` | `c4edba7875e2080b` |
| `nave_basokant` | 85246 | `47af606d9a5ec410` | `47af606d9a5ec410` |
| `nave_vers` | 156214 | `b4ea05b01c9cd4b9` | `b4ea05b01c9cd4b9` |
| `normalizalas_jelentes` | 472 | `06c8b737bd704a99` | `06c8b737bd704a99` |
| `oshl_bdb_igehelyek` | 4053 | `29d7049456d8409a` | `29d7049456d8409a` |
| `oshl_lexikalis_index` | 10221 | `b525fa2474213677` | `b525fa2474213677` |
| `res_forras` | 56 | `e91d76726be3fdb5` | `e91d76726be3fdb5` |
| `sdbh_domenek` | 22280 | `a76d2c6bacb6c8f9` | `a76d2c6bacb6c8f9` |
| `sdgnt_domenek` | 9075 | `51a12b44854aca28` | `51a12b44854aca28` |
| `sece_g` | 5523 | `d62a71806bcd514a` | `d62a71806bcd514a` |
| `sece_h` | 8674 | `7e9eab69417345f0` | `7e9eab69417345f0` |
| `strong_parok` | 571936 | `621af88e29704e69` | `621af88e29704e69` |
| `strong_szotar` | 14347 | `7790c8a17bafb34d` | `7790c8a17bafb34d` |
| `szotar_szerepek` | 26 | `f11558ebc4e66457` | `f11558ebc4e66457` |
| `tabla_licenc` | 71 | `15aa5cb59492398a` | `15aa5cb59492398a` |
| `tbesg` | 11035 | `02081181f1894623` | `02081181f1894623` |
| `tbesh` | 11682 | `79510c68f89bdbb3` | `79510c68f89bdbb3` |
| `terminologia` | 71 | `03ad9354ad077429` | `03ad9354ad077429` |
| `thayer` | 5426 | `03507af618fc151c` | `03507af618fc151c` |
| `tipnr` | 35522 | `7f70556658040c48` | `7f70556658040c48` |
| `token_eredeti` | 611396 | `75a604b8a9278532` | `75a604b8a9278532` |
| `token_karoli` | 981147 | `126d4e3ab7b98734` | `126d4e3ab7b98734` |
| `token_macula` | 475911 | `dc00cf4f469c9273` | `dc00cf4f469c9273` |
| `token_par` | 492380 | `7ee91e0a5b198b74` | `7ee91e0a5b198b74` |
| `token_strong` | 611655 | `69f5cda7c3c2310f` | `69f5cda7c3c2310f` |
| `tsk` | 432949 | `9acf0b780d4f3871` | `9acf0b780d4f3871` |
| `tw_szocikkek` | 598 | `e805af98eac22877` | `e805af98eac22877` |
| `ubs_dbh_jelentesek` | 20182 | `56c21557ad70fe45` | `56c21557ad70fe45` |
| `ubs_dbh_referenciak` | 389212 | `79f34a88a3233d53` | `79f34a88a3233d53` |
| `ubs_dntg_jelentesek` | 9075 | `669391a5962b6fb2` | `669391a5962b6fb2` |
| `ubs_dntg_referenciak` | 130948 | `9afe1e9724d2e732` | `9afe1e9724d2e732` |
| `vers` | 31158 | `0076280f851ecdd6` | `0076280f851ecdd6` |
| `vers_szamozas` | 22931 | `102f5474e027c9d4` | `102f5474e027c9d4` |

## Táblánkénti bájtméret

Mérés: minden tábla (indexeivel) külön adatbázisba másolva, lapszám × lapméret (a Python sqlite3-ból hiányzik a `dbstat`).

- a táblák összege: **871.5 MB** (a fájl: 871.2 MB; a többlet a táblánkénti külön adatbázisok saját fejléc- és séma-lapjaiból adódik)

| tábla | sor | MB (indexszel) |
|---|---:|---:|
| `token_karoli` | 981147 | 128.58 |
| `lxx_token` | 616873 | 104.46 |
| `token_eredeti` | 611396 | 80.96 |
| `token_macula` | 475911 | 78.95 |
| `frazis_pozicio` | 941747 | 68.94 |
| `token_par` | 492380 | 63.04 |
| `token_strong` | 611655 | 35.13 |
| `ubs_dbh_referenciak` | 389212 | 33.79 |
| `kjv` | 348606 | 32.96 |
| `bsb` | 277817 | 30.95 |
| `tsk` | 432949 | 27.53 |
| `strong_parok` | 571936 | 27.19 |
| `lxx_versszintu_parok` | 104518 | 20.46 |
| `nave_vers` | 156214 | 20.23 |
| `bdb_karoli` | 62526 | 12.62 |
| `ubs_dntg_referenciak` | 130948 | 11.09 |
| `lsj` | 5522 | 9.45 |
| `nave_basokant` | 85246 | 8.73 |
| `bdb` | 8099 | 8.43 |
| `vers` | 31158 | 6.06 |
| `karoli_variancia` | 42799 | 5.91 |
| `thayer` | 5426 | 5.77 |
| `tbesg` | 11035 | 5.39 |
| `ubs_dbh_jelentesek` | 20182 | 4.93 |
| `forditasok` | 737 | 4.00 |
| `tbesh` | 11682 | 3.75 |
| `ubs_dntg_jelentesek` | 9075 | 3.42 |
| `tipnr` | 35522 | 3.36 |
| `sece_h` | 8674 | 3.26 |
| `sdbh_domenek` | 22280 | 2.96 |
| `kh` | 32407 | 2.93 |
| `lxx_versszam` | 24232 | 2.43 |
| `sece_g` | 5523 | 1.98 |
| `vers_szamozas` | 22931 | 1.87 |
| `fts_motivum` | 624 | 1.83 |
| `strong_szotar` | 14347 | 1.58 |
| `sdgnt_domenek` | 9075 | 1.44 |
| `tw_szocikkek` | 598 | 1.36 |
| `mcged` | 5303 | 0.98 |
| `oshl_lexikalis_index` | 10221 | 0.86 |
| `morf_nyelv_aramai` | 7549 | 0.28 |
| `jeloltek` | 592 | 0.20 |
| `oshl_bdb_igehelyek` | 4053 | 0.19 |
| `igehely_tartomany` | 1087 | 0.15 |
| `lxx_bridge` | 3301 | 0.14 |
| `licencek` | 49 | 0.12 |
| `elofordulasok` | 259 | 0.09 |
| `karoli_strong_kivonat` | 383 | 0.09 |
| `datasetek` | 105 | 0.07 |
| `lexikon_hivatkozasok` | 23 | 0.07 |
| `bdb_igehely_javitas` | 93 | 0.06 |
| `lxx_dontesek` | 90 | 0.05 |
| `morf_kulcs_heber` | 124 | 0.05 |
| `normalizalas_jelentes` | 472 | 0.05 |
| `bdb_alias` | 460 | 0.04 |
| `auditok` | 222 | 0.04 |
| `grammatikai_strongok` | 92 | 0.02 |
| `tabla_licenc` | 71 | 0.02 |
| `terminologia` | 71 | 0.02 |
| `kapcsolatok` | 39 | 0.02 |
| `meta` | 97 | 0.02 |
| `motivumok` | 9 | 0.02 |
| `res_forras` | 56 | 0.02 |
| `szotar_szerepek` | 26 | 0.02 |
| `konyv` | 66 | 0.01 |
| `dontes_hatas` | 10 | 0.01 |
| `kiejtes_heber_jeloltszabalyok` | 20 | 0.01 |
| `kiejtes_heber_kivetelek` | 1 | 0.01 |
| `kiejtes_kivetelek` | 5 | 0.01 |
| `kiejtes_szabalyok` | 24 | 0.01 |
| `kulcsszavak` | 0 | 0.01 |

## Táblaszintű licenc (`tabla_licenc`, F89 / DT113)

| tábla | licenc_allapot | kereskedelmi | licenc_dataset | cimke |
|---|---|---|---|---|
| `auditok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `bdb` | kozkincs | igen | BDB | közkincs |
| `bdb_alias` | tisztazott | igen | BDB+projekt_adat | közkincs; minden jog fenntartva |
| `bdb_igehely_javitas` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `bdb_karoli` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `bsb` | tisztazott | igen | BSB_Strongs | CC0 1.0 |
| `datasetek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `dontes_hatas` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `elofordulasok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `forditasok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `frazis_pozicio` | tisztazott | igen | Karoli_Strong_parok | minden jog fenntartva |
| `fts_motivum` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `grammatikai_strongok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `igehely_tartomany` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `jeloltek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `kapcsolatok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `karoli_strong_kivonat` | tisztazott | igen | Karoli_Strong_kivonat | minden jog fenntartva |
| `karoli_variancia` | tisztazott | igen | karoli_variancia | minden jog fenntartva |
| `kh` | kozkincs | igen | Karoli_KH | közkincs |
| `kiejtes_heber_jeloltszabalyok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `kiejtes_heber_kivetelek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `kiejtes_kivetelek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `kiejtes_szabalyok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `kjv` | tisztazatlan | tisztazatlan | KJV_Strongs_teljes | tisztázatlan |
| `konyv` | tisztazott | igen | Konyv_nevtablak | CC BY 4.0 |
| `kulcsszavak` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `lexikon_hivatkozasok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `licencek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `lsj` | tisztazott | igen | LSJ | CC BY-SA 4.0 |
| `lxx_bridge` | tisztazott | igen | lxx_bridge | CC BY 4.0 |
| `lxx_dontesek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `lxx_token` | tisztazott | igen | LXX_OS | CC BY 4.0 |
| `lxx_versszam` | tisztazott | igen | LXX_OS+Versifikacios_tablak+Karoli_versmegfeleltetes | CC BY 4.0; minden jog fenntartva |
| `lxx_versszintu_parok` | tisztazott | igen | LXX_versszintu_parok | minden jog fenntartva |
| `mcged` | tisztazott | nem | MCGED | © Mounce 1993 |
| `meta` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `morf_kulcs_heber` | tisztazott | igen | morf_kulcs_heber | CC BY 4.0 |
| `morf_nyelv_aramai` | tisztazott | igen | morf_nyelv_aramai | CC BY 4.0 |
| `motivumok` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `nave_basokant` | kozkincs | igen | Nave_basokant | közkincs |
| `nave_vers` | tisztazott | igen | Nave_basokant+Karoli_versmegfeleltetes+LXX_OS | közkincs; minden jog fenntartva; CC BY 4.0 |
| `normalizalas_jelentes` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `oshl_bdb_igehelyek` | tisztazott | igen | OSHL_BDB | CC BY 4.0 |
| `oshl_lexikalis_index` | tisztazott | igen | OSHL | CC BY 4.0 |
| `res_forras` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `sdbh_domenek` | tisztazott | igen | SDBH | CC BY-SA 4.0 |
| `sdgnt_domenek` | tisztazott | igen | SDGNT | CC BY-SA 4.0 |
| `sece_g` | kozkincs | igen | SECE_G | közkincs |
| `sece_h` | kozkincs | igen | SECE_H | közkincs |
| `strong_parok` | tisztazott | igen | TAHOT+TAGNT+projekt_adat | CC BY 4.0; minden jog fenntartva |
| `strong_szotar` | tisztazott | igen | Strong_szotar | CC BY 4.0 |
| `szotar_szerepek` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `tabla_licenc` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `tbesg` | tisztazott | igen | TBESG | CC BY 4.0 |
| `tbesh` | tisztazott | igen | TBESH | CC BY 4.0 |
| `terminologia` | tisztazott | igen | projekt_adat | minden jog fenntartva |
| `thayer` | kozkincs | igen | Thayer | közkincs |
| `tipnr` | tisztazott | igen | TIPNR | CC BY 4.0 |
| `token_eredeti` | tisztazott | igen | TAHOT+TAGNT | CC BY 4.0 |
| `token_karoli` | tisztazott | igen | Karoli_Strong_szavak | minden jog fenntartva |
| `token_macula` | tisztazott | igen | Macula_heber | CC BY 4.0 |
| `token_par` | tisztazott | igen | Karoli_Strong_parok | minden jog fenntartva |
| `token_strong` | tisztazott | igen | TAHOT+TAGNT | CC BY 4.0 |
| `tsk` | tisztazott | igen | TSK | CC BY 4.0 |
| `tw_szocikkek` | tisztazott | feltetelesen | tW_szocikkek | CC BY-SA 4.0 |
| `ubs_dbh_jelentesek` | tisztazott | igen | UBS_DBH | CC BY-SA 4.0 |
| `ubs_dbh_referenciak` | tisztazott | igen | UBS_DBH | CC BY-SA 4.0 |
| `ubs_dntg_jelentesek` | tisztazott | igen | UBS_DNTG | CC BY-SA 4.0 |
| `ubs_dntg_referenciak` | tisztazott | igen | UBS_DNTG | CC BY-SA 4.0 |
| `vers` | kozkincs | igen | Karoli_1908 | közkincs |
| `vers_szamozas` | tisztazott | igen | Karoli_versmegfeleltetes+BSB_Strongs | minden jog fenntartva; CC0 1.0 |

- `tisztazatlan` állapotú táblák (1): `kjv`
- CC BY-SA 4.0 vagy MCGED (`© Mounce 1993`) címkéjű táblák (9; zárt csomagból kizárandók, DT116): `lsj`, `mcged`, `sdbh_domenek`, `sdgnt_domenek`, `tw_szocikkek`, `ubs_dbh_jelentesek`, `ubs_dbh_referenciak`, `ubs_dntg_jelentesek`, `ubs_dntg_referenciak`
- CC BY-NC címkéjű táblák (0): nincs

## Normalizálási jelentés (G5: nincs néma nem-találat)

| tábla | ok | darab (különböző érték / előfordulás) | példák |
|---|---|---|---|
| TAGNT_kivonat.tsv | nincs ilyen Károli-vers (token_eredeti.van_vers=0) | 3 / 40 | `1Kor 3:23`, `Róm 3:31`, `Róm 8:39` |
| bsb | nincs ilyen Károli-vers | 31 / 349 | `2Móz 36:38`, `4Móz 12:16`, `4Móz 30:17`, `Hós 12:15`, `Hós 13:16`, `Hós 2:23`, `Jób 17:16`, `Jób 37:24` |
| karoli_strong_kivonat | nincs ilyen Károli-vers | 1 / 1 | `Jób 17:16` |
| kh | nincs ilyen Károli-vers (cél-oldal) | 41 / 72 | `1Kir 4:39`, `1Kor 3:23`, `1Móz 2:28`, `1Sám 23:39`, `2Kir 22:23`, `2Kir 7:21`, `2Móz 15:29`, `2Sám 21:23` |
| kh | nincs ilyen Károli-vers (forrás-oldal) | 10 / 24 | `1Kor 3:23`, `Hós 11:12`, `Hós 1:12`, `Ján 1:52`, `Jób 36:34`, `Luk 23:57`, `Péld 11:32`, `Róm 3:31` |
| kjv | nincs ilyen Károli-vers | 146 / 702 | `1Kor 3:23`, `1Sám 23:29`, `2Kor 13:14`, `2Móz 36:38`, `4Móz 12:16`, `4Móz 29:40`, `ApCsel 19:41`, `Hós 11:12` |
| lxx_versszam | a LXX_OS nem ad értéket (vers; üres lxx_igehely, kitöltés nélkül; a térkép értéke legfeljebb a nem kanonikus terkep_ertek oszlopban) | 1 / 383 | `nincs LXX-megfelelő` |
| lxx_versszam | a két forrás LXX-versszáma eltér (vers) | 1 / 1888 | `LXX_OS ≠ versifikációs térkép` |
| lxx_versszam | a térkép kulcsa nem Károli-vers | 178 / 216 | `1Kir 5:32`, `1Sám 23:29`, `2Móz 36:38`, `4Móz 12:16`, `4Móz 29:40`, `Dán 1:22`, `Dán 1:23`, `Dán 1:24` |
| lxx_versszam | a térkép sora nem Károli-kulccsal áll (nem kerül a táblába; sor) | 1 / 39 | `NEM_MEGHATAROZHATO` |
| nave_vers | a forrás-sor nem bomlik versekre (nem kerül a nave_vers-be) | 4 / 9390 | `fejezet_szintu`, `igehely_nelkuli`, `nem_ertelmezheto_hely`, `nincs_karoli_vers_a_tartomanyban` |
| oshl_bdb_igehelyek | Strong-szám nem normalizálható | 1 / 397 | `—` |
| oshl_lexikalis_index | Strong-szám nem normalizálható | 1 / 930 | `—` |
| tipnr | levágott alapszám nincs a token_strong-ban | 1 / 1 | `G6202` |
| tipnr | nem leképezhető | 27 / 30 | `LXX.1Ki.9.20`, `LXX.Deu.20.17`, `LXX.Est.3.1`, `LXX.Est.7.9`, `LXX.Est.9.10`, `LXX.Exo.1.11`, `LXX.Exo.13.5`, `LXX.Exo.18.14` |
| tipnr | nincs ilyen Károli-vers | 17 / 37 | `1Kor 3:23`, `1Sám 23:29`, `2Kor 13:14`, `4Móz 12:16`, `4Móz 29:40`, `Dán 4:37`, `Hós 11:12`, `Hós 13:16` |
| token_macula | kétértelmű vers+Strong illesztés (csoport; feloldás: strong_poz = pozíció-sorrend) | 1 / 30541 | `azonos Strong egy versben többször` |
| token_macula | nincs ilyen Károli-vers | 7 / 132 | `1Móz 50:22;1Móz 50:23`, `1Móz 5:31;1Móz 5:32`, `2Móz 35:15;2Móz 35:16`, `2Móz 37:10;2Móz 37:13`, `5Móz 23:23;5Móz 23:24`, `5Móz 23:24;5Móz 23:25`, `Neh 7:68;Neh 7:69` |

## Megjegyzések

- strong_parok: a teljes TAHOT+TAGNT-ból (31161 vers, grammatikai_strongok és H9001-H9049 nélkül), mód-független
- FTS: 50 fájl, 624 rovat; átmeneti régi tanulmányok `regi_forras=1`; a #11 `migralt: igen` jelzője miatt kiesett: nincs (a jelző még nem létezik)
- Szándékosan nem betöltött konkordancia-táblák: Macula_gorog (a Macula_heber_*, LXX_OS/* és a BDB_strong_alias az F92 óta betöltve), KJV_/ASV_Strongs_{Genesis,Exodus,Proverbs} (a #48 vezeti ki; a KJV_Strongs_teljes betöltve), a BDB_*/aram segédtáblák (a BDB_strong_alias az F92 óta betöltve: bdb_alias), SDBH_SDGNT_domenfa, a versmegfeleltetési segédtáblák; a licencsor hiánya miatt kimaradt táblák száma: 0

