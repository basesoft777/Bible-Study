# GENERÁLT: eszkozok/olvaso_szerver/bekotesi_leltar.py — kézzel szerkeszteni tilos; a forrás (adat, regiszter, kód) javul, és újragenerálódik

# Az olvasó bekötési leltára

A leltár azt mutatja meg, milyen adatunk van, és ebből mi nincs még a versnézeten vagy a szónézeten. Nem azonos az alak-kapu hibalistájával: az a meglévő blokkok hibáit méri, ez a még be nem kötött adatot. A blokk-jegyzék (`konfig/blokk_jegyzek.tsv`) első feltöltéséhez ad választási alapot; azt ez a leltár nem írja.

- Adatbázis: `pardes.db` (építés: 2026-11-22T17:57:40Z, mód: teljes; a DB útvonala a(z) a fő checkout szerint)
- Lefedettség nevezője: 31 158 vers (a `vers` tábla), 14 347 Strong-szám (a `strong_szotar`: H 8 718, G 5 629)
- Kiadás és szint, amelyre a „látszik” értendő: `belso`, `kutato`

## Összefoglaló

- Adatkészlet: **61** (a `projekt_adat` saját táblái nélkül); ebből **50** áll a `pardes.db`-ben, **46** van legalább egy blokkban vagy a fejezetlapon, **46** látszik legalább egy táblájával.
- Nincs DB-táblája (a `sqlite_epit.py` nem építi be): `Chain_Lineage_Browser`, `Glossa_Ordinaria`, `KJV_ASV_Strongs`, `Macula_gorog`, `openbible_crossrefs`, `SBLGNT_apparatus`, `TAGNT_valtozatok`, `Tanu_atyak_index`, `Tanu_rabbinikus_index`, `Targum_PD`, `Vulgata_Clementina`.
- DB-tábla: **121**, ebből versre vagy Strong-számra szóló: **75**; ebből kötött (blokk, fejezetlap vagy keresés): **56**, látszik: **54**, **be nem kötött: 18**.
- Blokk a regiszterben (a keresési módokkal és a szövegoszloppal együtt): **56**, ebből látszik: **56**.

## Hogyan olvasd, és mit nem tud

- **Kulcs** (az oszlopnevekből, gépileg): `igehely`-jellegű oszlop (vagy `konyv`+`fejezet`+`vers`) → versnézet; `strong`-jellegű oszlop → szónézet; mindkettő → mindkettő; különben egyik sem. Egy kivétel van, a `KULCS_KIVETEL` a szkriptben (`strong_parok`).
- **Bekötött**: a tábla szerepel egy blokk `tablak` mezőjében, vagy a blokk adatlekérője/megjelenítője (a `lekerdezesek.py` hívásain át) olvassa, vagy a fejezetlap közvetlen hívása (`oldalak.py`: `fejezet_lap`, `_biblia_fejezet_lap`; `bibliak.py`) olvassa, vagy keresési blokk. Ha csak a kód olvassa máshol (fejléc, számlálók, ellenőrzések), az a „máshol” jelzés; ez nem kötés.
- **Látszik**: a konfigurált kiadásban (`konfig/szerver.toml`) és az alapszinten (`konfig/hozzaferes.toml`) a blokk látszik-e. A „feltételhez kötve” azt jelenti, hogy a blokk csak bizonyos feltétellel áll a lapon (vers-kontextus, üres eredménynél rejtve, a régebbi DB-ből hiányozhat, másik blokkot követ). A **csukva** állapotot a regiszter nem rögzíti (a lenyílók a blokkok belsejében vannak), ezért ez a leltár nem mutatja.
- **Olvasói név**: az `adat/olvasoi_nevtabla.tsv` `forras` sorai a lapgenerátor bemenet-jegyzékén (`adat/lapgen_bemenetek.tsv`) át, tábla- (a fájlnév azonos a táblanévvel) vagy adatkészlet-szinten. A blokkcímek (4. szakasz) az olvasón látható magyar címek: a regiszter szöveg-literálja, vagy az `F("kulcs")` hívás a `konfig/feliratok.tsv`-ből; a tábla olvasói neve (3. szakasz) nem a feliratokból jön.
- **Magyar fordítás**: a `forditasok` tábla mezői (szótár szerint), a magyar glosszák/Nave/BDB-bontás táblái, és a blokk, amely a táblát a fordítással együtt olvassa. A `—` azt jelenti, hogy a táblában nincs szöveges oszlop. A `nincs` szöveges táblára gépileg nem talált fordítást.
- **Licenc**: a `tabla_licenc` (cimke, jelzések) és a `licencek` (share-alike).
- **Lefedettség**: hány versre vagy Strong-számra van legalább egy sor. Verseknél a Károli-igehellyel egyező kulcsok, Strong-számnál a `strong_szotar`-ral egyezők.
- A leltár nem ítél arról, mi *kötendő*: egy támaszadat (például egy szóalak-tábla) lehet, hogy sosem lesz önálló blokk.

## 1. Be nem kötött, de versre vagy szóra szóló adat (lefedettség szerint csökkenő)

Ebből választ a szerkesztő; a választás lesz a blokk-jegyzék (`konfig/blokk_jegyzek.tsv`) első feltöltése. Ide az a tábla kerül, amelyet sem blokk (a regiszter `tablak` mezője vagy az adatlekérő kódja), sem a fejezetlap közvetlen hívása, sem a keresés nem olvas, és amelynek a kulcsa versre vagy Strong-számra szól. A tábla utolsó oszlopa jelzi, ha a szerver kódja máshol mégis olvassa (akkor a tábla támaszadat, nem feltétlenül kötendő blokk).

### 1/a. Külső adatkészlet adata (6 tábla)

| # | Tábla | Adatkészlet | Kulcs | Sor | Lefedettség | Olvasói név | Magyar fordítás | Licenc | A kód máshol |
|--:|---|---|---|--:|---|---|---|---|---|
| 1 | `frazis_pozicio` | Karoli_Strong_parok | mindkettő | 1 144 551 | 31 125 vers (99,9%) · H 8 553 · G 5 333 szó (96,8%) | — | magyar eredetű (Károli) | CC BY 4.0 |  |
| 2 | `strong_parok` | TAHOT+TAGNT+projekt_adat | szó | 571 936 | H 7 888 · G 5 053 szó (90,2%) | — | — | CC BY 4.0; minden jog fenntartva |  |
| 3 | `bdb_jp_sefaria` | BDB_rokon_irasok+projekt_adat | mindkettő | 161 244 | 22 622 vers (72,6%) · H 8 026 · G 0 szó (55,9%) | — | — | közkincs; minden jog fenntartva |  |
| 4 | `karoli_strong_kivonat` | Karoli_Strong_kivonat | mindkettő | 383 | 308 vers (1,0%) · H 119 · G 12 szó (0,9%) | — | magyar eredetű (Károli) | minden jog fenntartva |  |
| 5 | `bdb_aranyminta` | BDB+projekt_adat | szó | 658 | H 32 · G 0 szó (0,2%) | a BDB-szótár (adatkészlet-szinten) | magyar oszlop a táblában (kezdet_hu) | közkincs; minden jog fenntartva |  |
| 6 | `karoli_variancia` | karoli_variancia | mindkettő | 42 799 | 23 vers (0,1%) · H 0 · G 0 szó (0,0%), figyelem: a kulcsok csak 0/9 egyezik a Strong-szótárral | — | magyar eredetű (Károli) | minden jog fenntartva |  |

### 1/b. Saját (projekt) adat és munkatáblák (12 tábla)

| # | Tábla | Adatkészlet | Kulcs | Sor | Lefedettség | Olvasói név | Magyar fordítás | Licenc | A kód máshol |
|--:|---|---|---|--:|---|---|---|---|---|
| 1 | `bdb_forras_javitas` | projekt_adat | szó | 43 828 | H 6 124 · G 0 szó (42,7%) | — | — | minden jog fenntartva |  |
| 2 | `bdb_karoli` | projekt_adat | szó | 62 526 | H 674 · G 0 szó (4,7%) | — | — | minden jog fenntartva |  |
| 3 | `thayer_aranyminta` | projekt_adat | mindkettő | 800 | 753 vers (2,4%) · H 0 · G 517 szó (3,6%) | — | nincs | minden jog fenntartva |  |
| 4 | `igehely_tartomany` | projekt_adat | vers | 1 408 | 872 vers (2,8%) | — | — | minden jog fenntartva |  |
| 5 | `jeloltek` | projekt_adat | vers | 929 | 767 vers (2,5%) | — | — | minden jog fenntartva |  |
| 6 | `bdb_igehely_javitas` | projekt_adat | szó | 93 | H 63 · G 0 szó (0,4%) | — | — | minden jog fenntartva |  |
| 7 | `lexikon_hivatkozasok` | projekt_adat | szó | 67 | H 15 · G 20 szó (0,2%) | — | nincs | minden jog fenntartva |  |
| 8 | `visszhang_megfelelok` | projekt_adat | mindkettő | 196 | 48 vers (0,2%) · H 10 · G 6 szó (0,1%) | — | nincs | minden jog fenntartva |  |
| 9 | `visszhang_tanuk` | projekt_adat | vers | 12 | 5 vers (0,0%) | — | — | minden jog fenntartva |  |
| 10 | `motivum_kapcsolatok` | projekt_adat | vers | 3 | 3 vers (0,0%) | — | — | minden jog fenntartva |  |
| 11 | `kiejtes_heber_kivetelek` | projekt_adat | szó | 1 | H 1 · G 0 szó (0,0%) | — | — | minden jog fenntartva |  |
| 12 | `tematikus_sajat_szo` | projekt_adat | mindkettő | 1 | 1 vers (0,0%) · H 0 · G 1 szó (0,0%) | — | — | minden jog fenntartva |  |

### 1/c. Mindkét nézetre szóló adat, amely csak az egyik nézeten kötött (11 tábla)

A kulcsa versre is és szóra is szól (például a vers és a Strong-szám együtt), de az egyik nézeten nincs blokkja. Nem minden ilyen adat kötendő mindkét helyre; a szerkesztő dönt.

| # | Tábla | Adatkészlet | Hiány | Kötött helyen | Lefedettség | Olvasói név | Licenc |
|--:|---|---|---|---|---|---|---|
| 1 | `token_karoli` | Karoli_Strong_szavak | a szónézeten nincs | `szoveg.par`, `kereses.szo`, `kereses.frazis`, `kereses.heber`, … (+1) | 31 158 vers (100%) · H 8 557 · G 5 443 szó (97,6%), figyelem: a kulcsok csak 14 000/38 034 egyezik a Strong-szótárral | — | CC BY 4.0 |
| 2 | `token_strong` | TAHOT+TAGNT | a versnézeten nincs | `szo.elofordulas`, `szo.usz`, `kereses.strong` | 31 158 vers (100%) · H 8 557 · G 5 420 szó (97,4%) | — | CC BY 4.0 |
| 3 | `kjv` | KJV_Strongs_teljes | a szónézeten nincs | `vers.kjv`, fejezetlap-hívás | 31 075 vers (99,7%) · H 8 573 · G 5 473 szó (97,9%) | — | tisztázatlan |
| 4 | `bdb_vers_jelentes` | BDB+Macula_heber+OSHL+TAHOT+projekt_adat | a versnézeten nincs | `szo.bdb_apparatus` | 22 707 vers (72,9%) · H 8 027 · G 0 szó (55,9%) | a BDB-szótár | közkincs; CC BY 4.0; minden jog fenntartva |
| 5 | `bsb` | BSB_Strongs | a szónézeten nincs | `vers.bsb`, fejezetlap-hívás | 21 424 vers (68,8%) · H 7 642 · G 0 szó (53,3%) | — | CC0 1.0 |
| 6 | `tipnr` | TIPNR | a szónézeten nincs | `vers.tipnr` | 15 005 vers (48,2%) · H 2 826 · G 634 szó (24,1%) | — | CC BY 4.0 |
| 7 | `thayer_vers_jelentes` | projekt_adat | a versnézeten nincs | `szo.magyar_gorog` | 12 466 vers (40,0%), becslés: a kulcs nem Károli-igehely · H 0 · G 5 357 szó (37,3%) | a Thayer-szótár | minden jog fenntartva |
| 8 | `ubs_dntg_referenciak` | UBS_DNTG | a versnézeten nincs | `szo.usz`, `szo.ubs_dntg` | 7 938 vers (25,5%) · H 0 · G 5 312 szó (37,0%) | — | CC BY-SA 4.0 [share-alike] |
| 9 | `lxx_versszintu_parok` | LXX_versszintu_parok | a szónézeten nincs | `vers.lxx_par` | 8 764 vers (28,1%) · H 26 · G 0 szó (0,2%) | — | minden jog fenntartva |
| 10 | `oshl_bdb_igehelyek` | OSHL_BDB | a versnézeten nincs | `szo.oshl` | 3 047 vers (9,8%), becslés: a kulcs nem Károli-igehely · H 2 814 · G 0 szó (19,6%) | — | CC BY 4.0 |
| 11 | `lxx_dontesek` | projekt_adat | a szónézeten nincs | `vers.lxx_dontes` | 93 vers (0,3%) · H 20 · G 0 szó (0,1%) | — | minden jog fenntartva |

## 2. Adatkészletek (`adat/datasetek.tsv` + a licenc-leltár adatkészlet-nevei)

Az adatkészlet a `datasetek.tsv` sora (a `fajl` mezővel), illetve a `tabla_licenc` adatkészlet-neve. A DB-táblák a licenc-adatkészlet neve szerint kapcsolódnak (egy tábla több adatkészletből is épülhet, `+` jellel). Ahol az adatkészletnek nincs táblája, a `sqlite_epit.py` nem építi be a `pardes.db`-be.

| Adatkészlet | `datasetek.tsv` (kötelezőség · állapot) | DB-táblák | Blokkban | Látszik | Licenc | Magyar fordítás |
|---|---|---|--:|--:|---|---|
| BDB | mindig · elerheto | `bdb`, `bdb_alias`, `bdb_aranyminta`, `bdb_vers_jelentes` | 3/4 | 3/4 | közkincs; közkincs; CC BY 4.0; minden jog fenntartva … | van fordítás; magyar oszlop a táblában |
| BDB_rokon_irasok | ajanlott · elerheto | `bdb_jp_sefaria` | 0/1 | 0/1 | közkincs; minden jog fenntartva | — |
| BDB_szakaszok | ajanlott · korlatos | `bdb_szakaszok` | 1/1 | 1/1 | minden jog fenntartva | — |
| BDB_vers_jelentes | ajanlott · korlatos | `bdb_vers_jelentes` | 1/1 | 1/1 | közkincs; CC BY 4.0; minden jog fenntartva | — |
| BSB_Strongs | felteteles · korlatos | `bsb`, `vers_szamozas` | 2/2 | 2/2 | CC0 1.0; minden jog fenntartva; CC0 1.0 | — |
| Chain_Lineage_Browser | ajanlott · korlatos | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| Glossa_Ordinaria | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| Karoli_1908 | mindig · elerheto | `szoveg_modern`, `token_modern`, `vers` | 3/3 | 3/3 | CC BY 4.0; közkincs; közkincs | magyar eredetű |
| Karoli_KH | mindig · elerheto | `kh` | 1/1 | 1/1 | közkincs; CC BY 4.0 | — |
| Karoli_KH_javitott | ajanlott · elerheto | `kh` | 1/1 | 1/1 | közkincs; CC BY 4.0 | — |
| Karoli_KH_MEK | ajanlott · elerheto | `kh` | 1/1 | 1/1 | közkincs; CC BY 4.0 | — |
| karoli_modern | — | `szoveg_modern`, `token_modern` | 2/2 | 2/2 | CC BY 4.0; közkincs | magyar eredetű |
| Karoli_Strong_kivonat | oroklott · generalt_nezet | `karoli_strong_kivonat` | 0/1 | 0/1 | minden jog fenntartva | magyar eredetű |
| Karoli_Strong_parok | ajanlott · korlatos | `frazis_pozicio`, `token_par` | 1/2 | 1/2 | CC BY 4.0 | magyar eredetű |
| Karoli_Strong_szavak | ajanlott · korlatos | `szotari_token_kotojeles`, `token_karoli` | 2/2 | 2/2 | CC BY 4.0; minden jog fenntartva; CC BY 4.0 | magyar eredetű |
| karoli_variancia | — | `karoli_variancia` | 0/1 | 0/1 | minden jog fenntartva | magyar eredetű |
| Karoli_versmegfeleltetes | — | `lxx_versszam`, `nave_vers`, `vers_szamozas` | 3/3 | 3/3 | CC BY 4.0; minden jog fenntartva; közkincs; minden jog fenntartva; CC BY 4.0 … | a blokk magyar fordítással együtt mutatja |
| KJV_ASV_Strongs | felteteles · korlatos | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| KJV_Strongs_teljes | — | `kjv` | 1/1 | 1/1 | tisztázatlan | — |
| KJV_teljes_szoveg | ajanlott · elerheto | `szoveg_kjv` | 1/1 | 1/1 | közkincs | — |
| Konyv_nevtablak | — | `konyv` | 0/1 | 0/1 | CC BY 4.0 | — |
| LSJ | felteteles · elerheto | `lsj` | 1/1 | 1/1 | CC BY-SA 4.0 | igen |
| lxx_bridge | — | `lxx_bridge` | 1/1 | 1/1 | CC BY 4.0 | — |
| LXX_OS | felteteles · elerheto / mindig · elerheto / oroklott · elerheto | `lxx_token`, `lxx_versszam`, `nave_vers` | 3/3 | 3/3 | CC BY 4.0; CC BY 4.0; minden jog fenntartva … | a blokk magyar fordítással együtt mutatja |
| LXX_versszintu_parok | — | `lxx_versszintu_parok` | 1/1 | 1/1 | minden jog fenntartva | — |
| Macula_gorog | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| Macula_heber | ajanlott · elerheto | `bdb_vers_jelentes`, `token_macula` | 2/2 | 2/2 | CC BY 4.0; közkincs; CC BY 4.0; minden jog fenntartva | — |
| MCGED | — | `mcged` | 1/1 | 1/1 | © Mounce 1993 | — |
| morf_kulcs_heber | ajanlott · elerheto | `morf_kulcs_heber` | 1/1 | 1/1 | CC BY 4.0 | magyar oszlop a táblában |
| morf_nyelv_aramai | — | `morf_nyelv_aramai` | 1/1 | 1/1 | CC BY 4.0 | — |
| Nave_basokant | ajanlott · korlatos | `nave_basokant`, `nave_vers` | 2/2 | 2/2 | közkincs; közkincs; minden jog fenntartva; CC BY 4.0 | a blokk magyar fordítással együtt mutatja |
| openbible_crossrefs | ajanlott · hianyzik | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| OSHL | — | `bdb_vers_jelentes`, `oshl_lexikalis_index` | 2/2 | 2/2 | CC BY 4.0; közkincs; CC BY 4.0; minden jog fenntartva | — |
| OSHL_BDB | — | `oshl_bdb_igehelyek` | 1/1 | 1/1 | CC BY 4.0 | — |
| OSHL_BDB_igehelyek | ajanlott · korlatos | `oshl_bdb_igehelyek` | 1/1 | 1/1 | CC BY 4.0 | — |
| OSHL_lexikalis_index | ajanlott · elerheto | `oshl_lexikalis_index` | 1/1 | 1/1 | CC BY 4.0 | — |
| SBLGNT_apparatus | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| SDBH | ajanlott · elerheto | `sdbh_domenek` | 1/1 | 1/1 | CC BY-SA 4.0 | igen |
| SDGNT | ajanlott · elerheto | `sdgnt_domenek` | 1/1 | 1/1 | CC BY-SA 4.0 | igen |
| SECE_G | ajanlott · elerheto / felteteles · elerheto / oroklott · elerheto | `sece_g` | 1/1 | 1/1 | közkincs | — |
| SECE_H | felteteles · elerheto | `sece_h` | 1/1 | 1/1 | közkincs | — |
| Strong_szotar | felteteles · elerheto | `strong_szotar` | 1/1 | 1/1 | CC BY 4.0 | a blokk magyar fordítással együtt mutatja |
| szoto_tablak | — | `szotari_alak`, `szotari_kereso`, `szotari_token_kotojeles` | 3/3 | 3/3 | minden jog fenntartva; minden jog fenntartva; CC BY 4.0 | — |
| TAGNT | felteteles · elerheto / mindig · elerheto / oroklott · elerheto | `strong_parok`, `token_eredeti`, `token_strong` | 2/3 | 2/3 | CC BY 4.0; CC BY 4.0; minden jog fenntartva | — |
| TAGNT_valtozatok | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| TAHOT | mindig · elerheto | `bdb_vers_jelentes`, `glosszak_heber_hu`, `strong_parok`, `token_eredeti`, `token_strong` | 4/5 | 4/5 | CC BY 4.0; CC BY 4.0; minden jog fenntartva … | maga a fordítás-tábla |
| Tanu_atyak_index | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| Tanu_rabbinikus_index | ajanlott · korlatos | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| Targum_PD | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| TBESG | — | `tbesg` | 1/1 | 1/1 | CC BY 4.0 | igen |
| TBESH | — | `glosszak_heber_hu`, `tbesh` | 2/2 | 2/2 | CC BY 4.0; CC BY 4.0; minden jog fenntartva | maga a fordítás-tábla; igen |
| Thayer | felteteles · elerheto | `thayer` | 1/1 | 1/1 | közkincs | van fordítás |
| Thayer_szakaszok | ajanlott · korlatos | `thayer_szakaszok` | 1/1 | 1/1 | minden jog fenntartva | a blokk magyar fordítással együtt mutatja |
| Thayer_vers_jelentes | ajanlott · korlatos | `thayer_vers_jelentes` | 1/1 | 1/1 | minden jog fenntartva | — |
| TIPNR | felteteles · elerheto | `tipnr` | 1/1 | 1/1 | CC BY 4.0 | — |
| TSK | mindig · elerheto | `tsk` | 1/1 | 1/1 | CC BY 4.0 | — |
| tW_szocikkek | — | `tw_szocikkek` | 1/1 | 1/1 | CC BY-SA 4.0 | igen |
| UBS_DBH | — | `ubs_dbh_jelentesek`, `ubs_dbh_referenciak` | 2/2 | 2/2 | CC BY-SA 4.0 | igen |
| UBS_DNTG | — | `ubs_dntg_jelentesek`, `ubs_dntg_referenciak` | 2/2 | 2/2 | CC BY-SA 4.0 | van fordítás |
| Versifikacios_tablak | — | `lxx_versszam` | 1/1 | 1/1 | CC BY 4.0; minden jog fenntartva | — |
| Vulgata_Clementina | ajanlott · elerheto | **nincs DB-tábla** | 0/0 | 0/0 | — | — |
| projekt_adat | — | `auditok`, `bdb_alias`, `bdb_aranyminta`, `bdb_forras_javitas`, `bdb_igehely_javitas`, `bdb_jp_sefaria` … (+67) | 19/73 | 17/73 | CC BY 4.0; minden jog fenntartva; közkincs; CC BY 4.0; minden jog fenntartva … | magyar oszlop a táblában; maga a fordítás-tábla |

## 3. Minden DB-tábla (121)

Blokk-oszlop: a regiszter `tablak` mezőjében szereplő blokk-azonosító; csillag (`*`): a blokk adatlekérője olvassa a táblát, de a `tablak` mező nem sorolja fel (így a blokk forrás- és licencsora sem mutatja). A „Látszik” a konfigurált kiadásra (`belso`) és az alapszintre (`kutato`) értendő.

| Tábla | Adatkészlet | Kulcs | Sor | Blokk (vers · szó · fejezetlap · keresés) | Látszik | Olvasói név | Licenc | Magyar fordítás | Lefedettség |
|---|---|---|--:|---|---|---|---|---|---|
| `auditok` | projekt_adat | egyik sem | 431 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `bdb` | BDB | Strong → szónézet | 8 099 | `szo.bdb_apparatus`, `szo.bdb_angol` | látszik | a BDB-szótár (adatkészlet-szinten) | közkincs | van fordítás (30 000 mező), de ez a blokk nem mutatja | H 8 098 · G 0 szó (56,4%) |
| `bdb_alias` | BDB+projekt_adat | Strong → szónézet | 460 | `szo.bdb_apparatus`, `szo.bdb_angol` | látszik | a BDB-szótár (adatkészlet-szinten) | közkincs; minden jog fenntartva | nincs | H 460 · G 0 szó (3,2%) |
| `bdb_aranyminta` | BDB+projekt_adat | Strong → szónézet | 658 | — | nincs blokk | a BDB-szótár (adatkészlet-szinten) | közkincs; minden jog fenntartva | magyar oszlop a táblában (kezdet_hu) | H 32 · G 0 szó (0,2%) |
| `bdb_forras_javitas` | projekt_adat | Strong → szónézet | 43 828 | — | nincs blokk | — | minden jog fenntartva | — | H 6 124 · G 0 szó (42,7%) |
| `bdb_igehely_javitas` | projekt_adat | Strong → szónézet | 93 | — | nincs blokk | — | minden jog fenntartva | — | H 63 · G 0 szó (0,4%) |
| `bdb_jp_sefaria` | BDB_rokon_irasok+projekt_adat | vers + Strong → mindkettő | 161 244 | — | nincs blokk | — | közkincs; minden jog fenntartva | — | 22 622 vers (72,6%) · H 8 026 · G 0 szó (55,9%) |
| `bdb_karoli` | projekt_adat | Strong → szónézet | 62 526 | — | nincs blokk | — | minden jog fenntartva | — | H 674 · G 0 szó (4,7%) |
| `bdb_szakasz_hu` | projekt_adat | Strong → szónézet | 36 621 | `szo.bdb_apparatus`* | látszik | — | minden jog fenntartva | maga a fordítás-tábla (36 621 sor) | H 8 089 · G 0 szó (56,4%) |
| `bdb_szakaszok` | projekt_adat | Strong → szónézet | 36 621 | `szo.bdb_apparatus`* | látszik | — | minden jog fenntartva | nincs | H 8 089 · G 0 szó (56,4%) |
| `bdb_vers_jelentes` | BDB+Macula_heber+OSHL+TAHOT+projekt_adat | vers + Strong → mindkettő | 162 053 | `szo.bdb_apparatus` | látszik | a BDB-szótár | közkincs; CC BY 4.0; minden jog fenntartva | — | 22 707 vers (72,9%) · H 8 027 · G 0 szó (55,9%) |
| `bsb` | BSB_Strongs | vers + Strong → mindkettő | 275 042 | `vers.bsb`, fejezetlap-hívás | látszik | — | CC0 1.0 | nincs | 21 424 vers (68,8%) · H 7 642 · G 0 szó (53,3%) |
| `datasetek` | projekt_adat | egyik sem | 136 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `dontes_hatas` | projekt_adat | egyik sem | 10 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `elofordulasok` | projekt_adat | vers + Strong → mindkettő | 250 | `vers.motivum`, `szo.bdb_apparatus` | látszik | a motívum előfordulás-táblája | minden jog fenntartva | magyar oszlop a táblában (jelentes_hu) | 232 vers (0,7%) · H 17 · G 12 szó (0,2%) |
| `elutasitasi_okok` | projekt_adat | egyik sem | 63 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `forditasok` | projekt_adat | Strong → szónézet | 33 623 | `szo.szotar`*, `szo.ebben`, `szo.bdb_apparatus`, `szo.bdb_angol`*, `szo.ubs_dbh`, `szo.sdbh`, … (+8) | látszik | a lexikon fordítástáblája | minden jog fenntartva | maga a fordítás-tábla (33 623 sor) | H 8 098 · G 539 szó (60,2%) |
| `frazis_pozicio` | Karoli_Strong_parok | vers + Strong → mindkettő | 1 144 551 | — | nincs blokk | — | CC BY 4.0 | magyar eredetű (Károli) | 31 125 vers (99,9%) · H 8 553 · G 5 333 szó (96,8%) |
| `fts_motivum` | projekt_adat | egyik sem | 580 | — | nincs blokk | — | minden jog fenntartva | nincs | — |
| `funkcio_kapcsolok` | projekt_adat | egyik sem | 14 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `generalt_nezetek` | projekt_adat | egyik sem | 11 | — | nincs blokk | — | minden jog fenntartva | nincs | — |
| `glosszak_heber_hu` | TBESH+TAHOT+projekt_adat | Strong → szónézet | 11 677 | `szo.szotar`, `szo.ebben`, `szo.tbesh` | látszik | — | CC BY 4.0; minden jog fenntartva | maga a fordítás-tábla (11 677 sor) | H 8 718 · G 0 szó (60,8%) |
| `grammatikai_strongok` | projekt_adat | Strong → szónézet | 92 | `szo.nyelvtani` | feltételhez kötve — üres eredménynél rejtve | — | minden jog fenntartva | nincs | H 61 · G 31 szó (0,6%) |
| `heti_keret` | projekt_adat | egyik sem | 0 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `heti_keret_meres` | projekt_adat | egyik sem | 2 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `heti_terv` | projekt_adat | egyik sem | 18 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `igehely_tartomany` | projekt_adat | vers → versnézet | 1 408 | — | nincs blokk | — | minden jog fenntartva | — | 872 vers (2,8%) |
| `jeloltek` | projekt_adat | vers → versnézet | 929 | — | nincs blokk | — | minden jog fenntartva | — | 767 vers (2,5%) |
| `kapcsolatok` | projekt_adat | vers → versnézet | 86 | `vers.kapcsolat` | látszik | — | minden jog fenntartva | — | 35 vers (0,1%) |
| `karoli_strong_kivonat` | Karoli_Strong_kivonat | vers + Strong → mindkettő | 383 | — | nincs blokk | — | minden jog fenntartva | magyar eredetű (Károli) | 308 vers (1,0%) · H 119 · G 12 szó (0,9%) |
| `karoli_variancia` | karoli_variancia | vers + Strong → mindkettő | 42 799 | — | nincs blokk | — | minden jog fenntartva | magyar eredetű (Károli) | 23 vers (0,1%) · H 0 · G 0 szó (0,0%), figyelem: a kulcsok csak 0/9 egyezik a Strong-szótárral |
| `keret_munkamappa` | projekt_adat | egyik sem | 1 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `keret_sulyok` | projekt_adat | egyik sem | 15 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kh` | Karoli_KH+Karoli_KH_MEK+Karoli_KH_javitott | vers → versnézet | 23 979 | `vers.kh` | látszik | — | közkincs; CC BY 4.0 | — | 13 125 vers (42,1%) |
| `kiadasok` | projekt_adat | egyik sem | 7 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kiejtes_heber_jeloltszabalyok` | projekt_adat | egyik sem | 20 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kiejtes_heber_kivetelek` | projekt_adat | Strong → szónézet | 1 | — | nincs blokk | — | minden jog fenntartva | — | H 1 · G 0 szó (0,0%) |
| `kiejtes_kivetelek` | projekt_adat | egyik sem | 32 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kiejtes_szabalyok` | projekt_adat | egyik sem | 24 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kjv` | KJV_Strongs_teljes | vers + Strong → mindkettő | 348 705 | `vers.kjv`, fejezetlap-hívás | látszik — kizárva a(z) kereskedelmi és nyilvános kiadásból | — | tisztázatlan | nincs | 31 075 vers (99,7%) · H 8 573 · G 5 473 szó (97,9%) |
| `konyv` | Konyv_nevtablak | egyik sem | 66 | — | nincs blokk | — | CC BY 4.0 | — | — |
| `kozel_keleti_hatar` | projekt_adat | egyik sem | 3 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `kulcsszavak` | projekt_adat | vers + Strong → mindkettő | 0 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lap_atnezesek` | projekt_adat | egyik sem | 8 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lap_befagyasztas` | projekt_adat | egyik sem | 8 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lap_javitasok` | projekt_adat | egyik sem | 82 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lapgen_bemenetek` | projekt_adat | egyik sem | 69 | — | nincs blokk | — | minden jog fenntartva | nincs | — |
| `lapgen_sablonok` | projekt_adat | egyik sem | 961 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lexikon_hivatkozasok` | projekt_adat | Strong → szónézet | 67 | — | nincs blokk | — | minden jog fenntartva | nincs | H 15 · G 20 szó (0,2%) |
| `licencek` | projekt_adat | egyik sem | 65 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `lsj` | LSJ | Strong → szónézet | 5 522 | `szo.lsj` | látszik | — | CC BY-SA 4.0 [share-alike] | igen: 2 fordított mező (forditasok) | H 0 · G 5 522 szó (38,5%) |
| `lxx_bridge` | lxx_bridge | Strong → szónézet | 3 301 | `szo.lxx_bridge`, `szo.heber_hatter` | látszik | — | CC BY 4.0 | — | H 1 862 · G 0 szó (13,0%) |
| `lxx_dontesek` | projekt_adat | vers + Strong → mindkettő | 96 | `vers.lxx_dontes` | látszik | — | minden jog fenntartva | — | 93 vers (0,3%) · H 20 · G 0 szó (0,1%) |
| `lxx_token` | LXX_OS | vers + Strong → mindkettő | 616 873 | `vers.heber_csempe`, `vers.lxx_csempe`, `vers.lxx_szavak`, `szo.ebben`, fejezetlap-hívás | látszik | — | CC BY 4.0 | nincs | 22 821 vers (73,2%) · H 0 · G 3 885 szó (27,1%) |
| `lxx_versszam` | LXX_OS+Versifikacios_tablak+Karoli_versmegfeleltetes | vers → versnézet | 24 232 | `vers.lxx_versszam` | látszik | a Károli-versmegfeleltetés (adatkészlet-szinten) | CC BY 4.0; minden jog fenntartva | nincs | 23 204 vers (74,5%) |
| `lxx_versszintu_parok` | LXX_versszintu_parok | vers + Strong → mindkettő | 104 518 | `vers.lxx_par` | látszik | — | minden jog fenntartva | — | 8 764 vers (28,1%) · H 26 · G 0 szó (0,2%) |
| `mcged` | MCGED | Strong → szónézet | 5 303 | `szo.mcged` | látszik — kizárva a(z) kereskedelmi kiadásból | — | © Mounce 1993 [nem kereskedelmi] | nincs | H 0 · G 5 302 szó (37,0%) |
| `meta` | projekt_adat | egyik sem | 761 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `morf_kulcs_heber` | morf_kulcs_heber | egyik sem | 124 | `vers.heber_csempe`, `vers.morf_hu`, `szo.ebben`, `szo.bdb_apparatus` | látszik | — | CC BY 4.0 | magyar oszlop a táblában (jelentes_hu) | — |
| `morf_nyelv_aramai` | morf_nyelv_aramai | egyik sem | 7 549 | `vers.heber_csempe`, `vers.morf_hu`, `szo.ebben`, `szo.bdb_apparatus` | látszik | — | CC BY 4.0 | — | — |
| `motivum_kapcsolatok` | projekt_adat | vers → versnézet | 3 | — | nincs blokk | — | minden jog fenntartva | — | 3 vers (0,0%) |
| `motivumok` | projekt_adat | egyik sem | 9 | `vers.motivum` | látszik | — | minden jog fenntartva | nincs | — |
| `nave_basokant` | Nave_basokant | vers → versnézet | 85 246 | `vers.nave` | látszik | Nave tárgymutatója (1897) | közkincs | a blokk magyar fordítással együtt mutatja (nave_tema_hu) | 22 944 vers (73,6%) |
| `nave_tema_hu` | projekt_adat | egyik sem | 69 | `vers.nave` | látszik | a Nave-témák magyar nevei | minden jog fenntartva | maga a fordítás-tábla (69 sor) | — |
| `nave_vers` | Nave_basokant+Karoli_versmegfeleltetes+LXX_OS | vers → versnézet | 156 214 | `vers.nave` | látszik | Nave tárgymutatója (1897) (adatkészlet-szinten) | közkincs; minden jog fenntartva; CC BY 4.0 | a blokk magyar fordítással együtt mutatja (nave_tema_hu) | 30 145 vers (96,7%) |
| `normalizalas_jelentes` | projekt_adat | egyik sem | 781 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `nyilt_angol` | projekt_adat | egyik sem | 1 207 | — | nincs blokk | — | minden jog fenntartva | magyar oszlop a táblában (forras_hu) | — |
| `nyilt_kodkonyv` | projekt_adat | egyik sem | 441 | — | nincs blokk | — | minden jog fenntartva | magyar oszlop a táblában (leiras_hu) | — |
| `olvasoi_nevtabla` | projekt_adat | egyik sem | 227 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `oshl_bdb_igehelyek` | OSHL_BDB | vers + Strong → mindkettő | 4 053 | `szo.oshl` | látszik | — | CC BY 4.0 | — | 3 047 vers (9,8%), becslés: a kulcs nem Károli-igehely · H 2 814 · G 0 szó (19,6%) |
| `oshl_lexikalis_index` | OSHL | Strong → szónézet | 10 221 | `szo.oshl`, `szo.oshl_csalad` | látszik | — | CC BY 4.0 | — | H 8 673 · G 0 szó (60,5%) |
| `otlettar` | projekt_adat | egyik sem | 32 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `res_forras` | projekt_adat | egyik sem | 77 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `sdbh_domenek` | SDBH | Strong → szónézet | 22 280 | `szo.sdbh` | látszik | — | CC BY-SA 4.0 [share-alike] | igen: 31 fordított mező (forditasok) | H 8 557 · G 0 szó (59,6%) |
| `sdgnt_domenek` | SDGNT | Strong → szónézet | 9 075 | `szo.sdgnt` | látszik | — | CC BY-SA 4.0 [share-alike] | igen: 11 fordított mező (forditasok) | H 0 · G 5 312 szó (37,0%) |
| `sece_g` | SECE_G | Strong → szónézet | 5 523 | `szo.sece_g` | látszik | — | közkincs | nincs | H 0 · G 5 523 szó (38,5%) |
| `sece_h` | SECE_H | Strong → szónézet | 8 674 | `szo.sece_h` | látszik | — | közkincs | nincs | H 8 674 · G 0 szó (60,5%) |
| `strong_parok` | TAHOT+TAGNT+projekt_adat | Strong → szónézet | 571 936 | — | nincs blokk | — | CC BY 4.0; minden jog fenntartva | — | H 7 888 · G 5 053 szó (90,2%) |
| `strong_szotar` | Strong_szotar | Strong → szónézet | 14 347 | `szo.szotar`, `szo.ebben`, fejezetlap-hívás | látszik | — | CC BY 4.0 | a blokk magyar fordítással együtt mutatja (glosszak_heber_hu) | H 8 718 · G 5 629 szó (100%) |
| `szotar_szakasz_cimke` | projekt_adat | Strong → szónézet | 49 | `szo.bdb_apparatus`, `szo.magyar_gorog`* | látszik | a szótári szakaszok címketáblája | minden jog fenntartva | magyar oszlop a táblában (cimke_hu) | H 13 · G 14 szó (0,2%) |
| `szotar_szerepek` | projekt_adat | egyik sem | 26 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `szotari_alak` | szoto_tablak | egyik sem | 66 824 | `kereses.szo` | látszik | — | minden jog fenntartva | — | — |
| `szotari_kereso` | szoto_tablak | egyik sem | 72 766 | `kereses.szo` | látszik | — | minden jog fenntartva | — | — |
| `szotari_token_kotojeles` | szoto_tablak+Karoli_Strong_szavak | vers → versnézet | 5 580 | `kereses.szo` | látszik | — | minden jog fenntartva; CC BY 4.0 | — | 2 299 vers (7,4%) |
| `szoveg_kjv` | KJV_teljes_szoveg | vers → versnézet | 31 085 | fejezetlap-hívás | látszik (csak a fejezetlapon) | — | közkincs [feltételesen kereskedelmi] | nincs | 31 078 vers (99,7%) |
| `szoveg_modern` | karoli_modern+Karoli_1908 | vers → versnézet | 31 158 | fejezetlap-hívás | látszik (csak a fejezetlapon) | — | CC BY 4.0; közkincs | magyar eredetű (Károli) | 31 158 vers (100%) |
| `tabla_licenc` | projekt_adat | egyik sem | 121 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `tanulmany` | projekt_adat | egyik sem | 24 | `vers.motivum`*, `vers.tanulmany`, fejezetlap-hívás | látszik | — | minden jog fenntartva | — | — |
| `tanulmany_hivatkozas` | projekt_adat | vers → versnézet | 1 660 | `vers.tanulmany` | feltételhez kötve — a régebbi adatbázisból hiányozhat | — | minden jog fenntartva | — | 552 vers (1,8%) |
| `tanulmany_szoveg` | projekt_adat | egyik sem | 24 | — | nincs blokk | — | minden jog fenntartva | nincs | — |
| `tanulmany_tartomany` | projekt_adat | vers → versnézet | 26 | `vers.tanulmany`, fejezetlap-hívás | látszik | — | minden jog fenntartva | — | 464 vers (1,5%) (tartományok lefedése) |
| `tbesg` | TBESG | Strong → szónézet | 11 035 | `szo.szotar`*, `szo.ebben`*, `szo.tbesg` | látszik | — | CC BY 4.0 | igen: 275 fordított mező (forditasok) | H 0 · G 5 603 szó (39,1%) |
| `tbesh` | TBESH | Strong → szónézet | 11 682 | `szo.szotar`*, `szo.ebben`*, `szo.bdb_apparatus`*, `szo.bdb_angol`*, `szo.tbesh` | látszik | — | CC BY 4.0 | igen: 1 fordított mező (forditasok, glosszak_heber_hu) | H 8 176 · G 0 szó (57,0%) |
| `tematikus_sajat_szo` | projekt_adat | vers + Strong → mindkettő | 1 | — | nincs blokk | — | minden jog fenntartva | — | 1 vers (0,0%) · H 0 · G 1 szó (0,0%) |
| `tematikus_temak` | projekt_adat | egyik sem | 105 | — | nincs blokk | a tematikus index döntései | minden jog fenntartva | nincs | — |
| `terminologia` | projekt_adat | egyik sem | 114 | — | nincs blokk | — | minden jog fenntartva | magyar oszlop a táblában (magyar) | — |
| `thayer` | Thayer | Strong → szónézet | 5 426 | `szo.thayer` | látszik | a Thayer-szótár (adatkészlet-szinten) | közkincs | van fordítás (2 935 mező), de ez a blokk nem mutatja | H 0 · G 5 426 szó (37,8%) |
| `thayer_aranyminta` | projekt_adat | vers + Strong → mindkettő | 800 | — | nincs blokk | — | minden jog fenntartva | nincs | 753 vers (2,4%) · H 0 · G 517 szó (3,6%) |
| `thayer_forras_javitas` | projekt_adat | Strong → szónézet | 15 | `szo.thayer`* | látszik | — | minden jog fenntartva | — | H 0 · G 15 szó (0,1%) |
| `thayer_sigla` | projekt_adat | egyik sem | 255 | — | nincs blokk | — | minden jog fenntartva | nincs | — |
| `thayer_szakaszok` | projekt_adat | Strong → szónézet | 17 220 | `szo.magyar_gorog` | látszik | — | minden jog fenntartva | a blokk magyar fordítással együtt mutatja (forditasok) | H 0 · G 5 426 szó (37,8%) |
| `thayer_vers_jelentes` | projekt_adat | vers + Strong → mindkettő | 64 431 | `szo.magyar_gorog` | látszik | a Thayer-szótár | minden jog fenntartva | — | 12 466 vers (40,0%), becslés: a kulcs nem Károli-igehely · H 0 · G 5 357 szó (37,3%) |
| `tiltott_fordulatok` | projekt_adat | egyik sem | 3 | — | nincs blokk | — | minden jog fenntartva | — | — |
| `tipnr` | TIPNR | vers + Strong → mindkettő | 35 522 | `vers.tipnr` | látszik | — | CC BY 4.0 | — | 15 005 vers (48,2%) · H 2 826 · G 634 szó (24,1%) |
| `token_eredeti` | TAHOT+TAGNT | vers + Strong → mindkettő | 611 396 | `vers.heber_csempe`, `vers.eredeti`, `vers.ubs`*, `szo.ebben`, `szo.bdb_apparatus`, `szo.usz`*, … (+1) | látszik | — | CC BY 4.0 | nincs | 31 158 vers (100%) · H 8 557 · G 5 443 szó (97,6%) |
| `token_karoli` | Karoli_Strong_szavak | vers + Strong → mindkettő | 1 210 763 | `szoveg.par`, `kereses.szo`, `kereses.frazis`, `kereses.heber`, fejezetlap-hívás | látszik | — | CC BY 4.0 | magyar eredetű (Károli) | 31 158 vers (100%) · H 8 557 · G 5 443 szó (97,6%), figyelem: a kulcsok csak 14 000/38 034 egyezik a Strong-szótárral |
| `token_macula` | Macula_heber | vers + Strong → mindkettő | 475 911 | `vers.heber_csempe`, `vers.macula_morf`, `vers.macula_gorog`, `vers.morf_hu`, `szo.ebben`, `szo.bdb_apparatus` | látszik | — | CC BY 4.0 | nincs | 23 023 vers (73,9%) · H 8 193 · G 0 szó (57,1%) |
| `token_modern` | karoli_modern+Karoli_1908 | vers → versnézet | 585 621 | fejezetlap-hívás | látszik (csak a fejezetlapon) | — | CC BY 4.0; közkincs | magyar eredetű (Károli) | 31 158 vers (100%) |
| `token_par` | Karoli_Strong_parok | vers + Strong → mindkettő | 598 715 | `vers.par`, `szo.ebben`, `szo.karoli_alakok`, `szoveg.par`, `kereses.strong`, `kereses.szo`, … (+2) | látszik | — | CC BY 4.0 | magyar eredetű (Károli) | 31 125 vers (99,9%) · H 8 553 · G 5 333 szó (96,8%) |
| `token_strong` | TAHOT+TAGNT | vers + Strong → mindkettő | 611 655 | `szo.elofordulas`, `szo.usz`, `kereses.strong` | látszik | — | CC BY 4.0 | — | 31 158 vers (100%) · H 8 557 · G 5 420 szó (97,4%) |
| `tsk` | TSK | vers → versnézet | 432 442 | `vers.tsk` | látszik | — | CC BY 4.0 | — | 29 340 vers (94,2%) |
| `tw_szocikkek` | tW_szocikkek | Strong → szónézet | 598 | `szo.tw_h`, `szo.tw_g` | látszik | — | CC BY-SA 4.0 [feltételesen kereskedelmi, share-alike] | igen: 29 fordított mező (forditasok) | H 21 · G 21 szó (0,3%), figyelem: a kulcsok csak 42/580 egyezik a Strong-szótárral |
| `ubs_dbh_jelentesek` | UBS_DBH | Strong → szónézet | 20 182 | `vers.ubs`, `szo.ebben`, `szo.ubs_dbh` | látszik | az UBS Dictionary of Biblical Hebrew | CC BY-SA 4.0 [share-alike] | igen: 237 fordított mező (forditasok) | H 7 924 · G 0 szó (55,2%) |
| `ubs_dbh_referenciak` | UBS_DBH | vers + Strong → mindkettő | 389 212 | `vers.ubs`, `szo.ebben` | látszik | az UBS Dictionary of Biblical Hebrew | CC BY-SA 4.0 [share-alike] | — | 23 057 vers (74,0%) · H 7 924 · G 0 szó (55,2%) |
| `ubs_dntg_jelentesek` | UBS_DNTG | Strong → szónézet | 9 075 | `szo.usz`, `szo.ubs_dntg` | látszik | — | CC BY-SA 4.0 [share-alike] | van fordítás (102 mező), de ez a blokk nem mutatja | H 0 · G 5 312 szó (37,0%) |
| `ubs_dntg_referenciak` | UBS_DNTG | vers + Strong → mindkettő | 130 948 | `szo.usz`, `szo.ubs_dntg` | látszik | — | CC BY-SA 4.0 [share-alike] | — | 7 938 vers (25,5%) · H 0 · G 5 312 szó (37,0%) |
| `vers` | Karoli_1908 | vers → versnézet | 31 158 | `vers.karoli`, `vers.nave`*, `vers.motivum`, `vers.tanulmany`*, `szo.usz`, `szoveg.karoli`, … (+5) | látszik | — | közkincs | magyar eredetű (Károli) | 31 158 vers (100%) |
| `vers_szamozas` | Karoli_versmegfeleltetes+BSB_Strongs | vers → versnézet | 23 195 | `vers.versszamozas`, `vers.nave`* | látszik | a Károli-versmegfeleltetés (adatkészlet-szinten) | minden jog fenntartva; CC0 1.0 | — | 23 195 vers (74,4%) |
| `visszhang_megfelelok` | projekt_adat | vers + Strong → mindkettő | 196 | — | nincs blokk | — | minden jog fenntartva | nincs | 48 vers (0,2%) · H 10 · G 6 szó (0,1%) |
| `visszhang_tanuk` | projekt_adat | vers → versnézet | 12 | — | nincs blokk | — | minden jog fenntartva | — | 5 vers (0,0%) |
| `vitatott_forrasok` | projekt_adat | egyik sem | 3 | — | nincs blokk | — | minden jog fenntartva | — | — |

## 4. A blokk-regiszter (a blokk-jegyzék kiindulása)

Minden blokk egy sor: azonosító, nézet, hely, látszik-e, a `tablak` mező és a kódban ténylegesen olvasott többlet-táblák.

| Blokk | Cím | Nézet | Hely | Látszik | `tablak` | Kódban olvasott többlet | Jelzések |
|---|---|---|---|---|---|---|---|
| `vers.karoli` | Károli-szöveg | vers | Vers fül | igen | vers | — | — |
| `vers.versszamozas` | Versszámozás (MT / KJV) | vers | Vers fül | igen | vers_szamozas | — | — |
| `vers.lxx_versszam` | LXX-versszám | vers | Vers fül | igen | lxx_versszam | — | — |
| `vers.heber_csempe` | Héber szöveg | vers | Vers fül | igen | token_eredeti, token_macula, lxx_token, morf_kulcs_heber, morf_nyelv_aramai | — | — |
| `vers.lxx_csempe` | Septuaginta (LXX, Rahlfs) | vers | Vers fül | igen | lxx_token | — | — |
| `vers.par` | Károli–Strong párosítás | vers | Vers fül | igen | token_par | — | — |
| `vers.eredeti` | Eredeti szavak (TAHOT / TAGNT) | vers | Vers fül | igen | token_eredeti | — | — |
| `vers.macula_morf` | Igealak-kód és szófaj (Macula) | vers | Vers fül | igen | token_macula | — | — |
| `vers.macula_gorog` | Héber–görög párosítás szavanként (Macula) | vers | Vers fül | igen | token_macula | — | — |
| `vers.lxx_szavak` | Görög szóalak és LXX-vers szavai (LXX_OS) | vers | Vers fül | igen | lxx_token | — | — |
| `vers.bsb` | Angol szavak szavanként (BSB) | vers | Vers fül | igen | bsb | — | — |
| `vers.kjv` | Angol szavak szavanként (KJV + Strong) | vers | Vers fül | igen | kjv | — | kizárva a(z) kereskedelmi és nyilvános kiadásból |
| `vers.nave` | Témák (Nave, versekre bontva) | vers | Témák fül | igen | nave_vers, nave_basokant, nave_tema_hu | vers, vers_szamozas | — |
| `vers.tipnr` | Tulajdonnevek (TIPNR) | vers | Témák fül | igen | tipnr | — | — |
| `vers.morf_hu` | Az igealak magyar feloldása | vers | Vers fül | igen | morf_kulcs_heber, token_macula, morf_nyelv_aramai | — | — |
| `vers.motivum` | Motívumadat (adatréteg) | vers | Motívum fül | igen | elofordulasok, motivumok, vers | tanulmany | — |
| `vers.tanulmany` | Tanulmányok erről a versről | vers | Motívum fül | igen | tanulmany, tanulmany_tartomany, tanulmany_hivatkozas | vers | a régebbi adatbázisból hiányozhat |
| `vers.kapcsolat` | Igehely-kapcsolatok (adatréteg) | vers | Motívum fül | igen | kapcsolatok | — | — |
| `vers.lxx_dontes` | LXX-fordítói döntések (adatréteg) | vers | Vers fül | igen | lxx_dontesek | — | — |
| `vers.lxx_par` | LXX versszintű együttelőfordulás | vers | Vers fül | igen | lxx_versszintu_parok | — | — |
| `vers.lxx_tobblet` | LXX többlet és számozási eltérés | vers | Vers fül | igen | — | — | — |
| `vers.tsk` | Kereszthivatkozások (TSK) | vers | Kereszthiv. fül | igen | tsk | — | — |
| `vers.kh` | Károli-kereszthivatkozások | vers | Kereszthiv. fül | igen | kh | — | — |
| `vers.ubs` | UBS-jelentés az előfordulásra | vers | Vers fül | igen | ubs_dbh_referenciak, ubs_dbh_jelentesek | token_eredeti | — |
| `szo.szotar` | Strong-szótár | szó | szó-panel | igen | strong_szotar, glosszak_heber_hu | forditasok, tbesg, tbesh | — |
| `szo.elofordulas` | Előfordulás, könyvek száma | szó | szó-panel | igen | token_strong | — | — |
| `szo.ebben` | Ebben a versben | szó | szó-panel | igen | token_par, token_eredeti, token_macula, lxx_token, ubs_dbh_referenciak, ubs_dbh_jelentesek, morf_kulcs_heber, morf_nyelv_aramai, glosszak_heber_hu, strong_szotar, forditasok | tbesg, tbesh | csak vers-kontextussal; követi: vers.ubs, vers.heber_csempe, vers.par |
| `szo.karoli_alakok` | Károli-alakok és pontosság | szó | szó-panel | igen | token_par | — | — |
| `szo.bdb_apparatus` | Szótár: BDB-szócikk (Brown–Driver–Briggs) | szó | szó-panel | igen | bdb, bdb_alias, forditasok, bdb_vers_jelentes, token_eredeti, token_macula, morf_kulcs_heber, morf_nyelv_aramai, szotar_szakasz_cimke, elofordulasok | bdb_szakasz_hu, bdb_szakaszok, tbesh | — |
| `szo.bdb_angol` | BDB-szócikk (nyers szöveg) | szó | szó-panel | igen | bdb, bdb_alias | forditasok, tbesh | üres eredménynél rejtve |
| `szo.lxx_bridge` | Görög megfelelő (Septuaginta) | szó | szó-panel | igen | lxx_bridge | — | — |
| `szo.ubs_dbh` | UBS DBH jelentések (a teljes szócikk, magyar fordítással) | szó | szó-panel | igen | ubs_dbh_jelentesek, forditasok | — | — |
| `szo.sdbh` | Szemantikai domén (SDBH) | szó | szó-panel | igen | sdbh_domenek, forditasok | — | — |
| `szo.sece_h` | SECE-szócikk (héber) | szó | szó-panel | igen | sece_h | — | — |
| `szo.oshl` | OSHL: TWOT- és BDB-azonosító, BDB-helyek | szó | szó-panel | igen | oshl_lexikalis_index, oshl_bdb_igehelyek | — | — |
| `szo.oshl_csalad` | Rokon szavak (OSHL-gyökcsalád) | szó | szó-panel | igen | oshl_lexikalis_index | — | — |
| `szo.tbesh` | Bővített Strong-szócikk (TBESH) | szó | szó-panel | igen | tbesh, glosszak_heber_hu, forditasok | — | — |
| `szo.tw_h` | translationWords | szó | szó-panel | igen | tw_szocikkek, forditasok | — | — |
| `szo.nyelvtani` | Nyelvtani Strong-számok szűrése | szó | szó-panel | igen | grammatikai_strongok | — | üres eredménynél rejtve |
| `szo.magyar_gorog` | Szótár: Thayer-szócikk | szó | szó-panel | igen | forditasok, thayer_szakaszok, thayer_vers_jelentes | szotar_szakasz_cimke | — |
| `szo.usz` | ÚSZ-előfordulás és versek | szó | szó-panel | igen | token_strong, vers, ubs_dntg_jelentesek, ubs_dntg_referenciak | token_eredeti | — |
| `szo.heber_hatter` | Héber háttér (Septuaginta) | szó | szó-panel | igen | lxx_bridge | — | — |
| `szo.sdgnt` | Szemantikai domén (SDGNT) | szó | szó-panel | igen | sdgnt_domenek, forditasok | — | — |
| `szo.ubs_dntg` | UBS DNTG jelentés | szó | szó-panel | igen | ubs_dntg_jelentesek, ubs_dntg_referenciak | forditasok | — |
| `szo.tbesg` | TBESG (forrásszöveg) | szó | szó-panel | igen | tbesg, forditasok | — | — |
| `szo.thayer` | Thayer, angol (forrásszöveg) | szó | szó-panel | igen | thayer | thayer_forras_javitas | — |
| `szo.lsj` | LSJ | szó | szó-panel | igen | lsj, forditasok | — | — |
| `szo.mcged` | MCGED (Mounce) | szó | szó-panel | igen | mcged | — | kizárva a(z) kereskedelmi kiadásból |
| `szo.sece_g` | SECE-szócikk (görög) | szó | szó-panel | igen | sece_g | — | — |
| `szo.tw_g` | translationWords | szó | szó-panel | igen | tw_szocikkek, forditasok | — | — |
| `szoveg.karoli` | szövegoszlop | fejezetlap | fejezetlap szövegoszlopa | igen | vers | — | — |
| `szoveg.par` | szövegoszlop | fejezetlap | fejezetlap szövegoszlopa | igen | token_par, token_karoli | — | — |
| `kereses.strong` | Strong-szám | keresés | keresőlap | igen | token_strong, vers, token_par | — | — |
| `kereses.szo` | magyar szó | keresés | keresőlap | igen | token_karoli, vers, szotari_kereso, szotari_alak, szotari_token_kotojeles, token_par | — | — |
| `kereses.frazis` | magyar frázis | keresés | keresőlap | igen | token_karoli, vers | — | — |
| `kereses.heber` | héber frázis | keresés | keresőlap | igen | token_karoli, vers, token_par | — | — |

