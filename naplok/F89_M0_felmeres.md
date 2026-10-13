# F89 M0 felmérés — licenc-rendezés (csak olvasás)

*#89 · modell: claude-sonnet-5-5 · 2026.10.13 · brief: `F89_LICENC_RENDEZES_BRIEF.md` v2 · proveniencia: `scope=repó (F89 worktree) | forras=adat/licencek.tsv, eszkozok/*.py, lexikon/, .github/workflows/ (grep, split('\t')) | ts=2026-10-13`. Ez leltár, nem jogi vélemény. Nem írtam sem LICENSE-t, sem `licencek.tsv`-t, sem kódot.*

## 1. A `licencek.tsv` és a `projekt_adat`

A tábla 46 adatsor (fejléc a 6. sorban; 10 oszlop, a `cimke` az utolsó), ebből 12 `tisztazatlan`. A `projekt_adat` a 49. sor: `licenc` = „a repó saját licence nincs rögzítve”, `kereskedelmi`/`share_alike`/`allapot` = `tisztazatlan`, `cimke` = `projekt-adat` (a SEMA 2.19 kivétele). A repónak nincs `LICENSE`-fájlja.

**A) A `projekt_adat`-on múló `tisztazatlan` sorok (a brief újraértékelési köre)**

| sor | dataset | mi tart tisztázatlanban | DT116 után |
|---|---|---|---|
| 11 | `Karoli_Strong_kivonat` | komponensek: `projekt_adat` (tisztazatlan), Károli (közkincs), Strong_szotar (CC BY 4.0, tisztazott) | `tisztazott` lehet, ha a `projekt_adat` az. Kötelező megjelölés a Strong_szotar szerint (Szófaj, Gyök/Származtatás oszlop); a `kotelezo_megjeloles` ma üres |
| 33 | `LXX_versszintu_parok` | LXX_OS (tisztazott) + TAHOT (tisztazott) + `projekt_adat` | `tisztazott` lehet; a `kotelezo_megjeloles` már áll (lxx-morph, Kushniryk). A megjegyzés szerint „saját licencidézetet nem kapott”: a `forras_hely` ellenőrzendő, hogy a SEMA 2.19 2. szabálya teljesül-e |
| 34 | `Karoli_versmegfeleltetes` | verse_pairs (LXX_OS, CC BY 4.0, TVTMS-származék), Károli, TAHOT, `projekt_adat` (KEZI_ELTOLASOK) | `tisztazott` lehet, ugyanazzal a fenntartással |

**B) Csak hivatkozás, a sor állapota nem múlik rajta** (`tisztazott`/`kozkincs` marad; a megjegyzés „a projekt_adat sorban tisztazatlan” mondata elavul): 7 `BDB` (BDB_etimologia_kezi_hatarok.tsv), 32 `LXX_OS` (karoli_*.tsv a könyvtárban), 41 `Versifikacios_tablak` (Károli_igehely, KEZI_ELTOLASOK stb.), 42 `Konyv_nevtablak` (magyar nevek). A brief G1 szerint csak a megnevezett sorok változnak, ezért ezekhez nem nyúlnék (kérdés: K1).

**C) Hiányzó sorok:** `Karoli_Strong_parok`, `Karoli_Strong_szavak` (a `datasetek.tsv` 89–99. során minden study-típusnál szerepel, a `licencek.tsv`-ben nincs sor), `karoli_variancia` (a `datasetek.tsv`-ben sincs sor; a SEMA 2.24 írja le). Az N-F79a ezekről szól.

**D) Nem a `projekt_adat`-on múló `tisztazatlan` sorok (kívül esnek):** `KJV_ASV_Strongs`, `LXX_kivonat`, `KJV_Strongs_teljes`, `lexikonok_nyers`, `LXX_lexicon`, `Heber_ETCBC_modulok`, `Cremer_nyers`, `Girdlestone`.

**Komponens-állapotok a legszigorúbb-érték szabályhoz:** `Karoli_1908` közkincs/igen; `TAHOT`, `TAGNT` tisztazott/igen/share_alike nem; `projekt_adat` ma tisztazatlan. A DT116 és D3 = `igen` után a `token_par`, `token_karoli`, `frazis_pozicio`, `karoli_variancia`, `strong_parok`, `igehely_tartomany`, `normalizalas_jelentes`, `meta`, `fts_motivum` tábla `tisztazott`/`igen`-re javul (a `SZIGOR_ALLAPOT` sorrendje M3-ban ellenőrzendő). D3 = `nem` esetén mind `nem` lenne.

## 2. Kódhelyek

**A `projekt_adat` kulcs, a `cimke` és a `licenc_*` oszlopok olvasói:**

- `eszkozok/lexikon_general.py`: `licencek()` (69. sor), `LC(dataset)` (95–106): a `cimke`-t a táblából olvassa; a kódban nincs licenc-konstans és nincs zárt-készlet ellenőrzés a címkére (csak a nem üres feltétel, 99. sor). `LC('projekt_adat')` hívások: 338, 370, 560, 563, 567, 619–620, 994–995, 1206, 1209, 1316–1317, 1345–1346, 1434, 1495 (tartalom, jelmagyarázat, elofordulasok, kapcsolatok, idézés, lxx_dontesek, szerepmátrix, kolofon blokkok). A címkeváltáshoz kódmódosítás nem kell; a blokkok `licenc:` mezője és a kolofon licenclistája változik.
- `eszkozok/sqlite_epit.py`: `RESERVALT_OSZLOP` (85), `SZARMAZTATOTT_LICENC` (89–106; a `token_par`, `token_karoli`, `frazis_pozicio`, `karoli_variancia`, `strong_parok`, `igehely_tartomany`, `normalizalas_jelentes`, `meta`, `fts_motivum` hordozza a `projekt_adat`-ot), `ADAT_LICENC` (134; a többi `adat/` tábla alapértéke `['projekt_adat']`, 822), `licenc_feloldas` / `licenc_ellenorzes` (325, 370), `tabla()` (344–352: a három `licenc_*` oszlop minden táblához), az FTS `UNINDEXED` oszlopok (855–856), a `meta` hash-sorok `('projekt_adat','tisztazatlan','projekt_adat')` értéke (1269). A DT113 tárolásváltás ezeket érinti.
- `eszkozok/teszt_sqlite_epit.py`: 306–307 (üres licenc-oszlop teszt), 395–398 (`motivumok` → `('projekt_adat',)`): `tabla_licenc`-re írandó át.
- `eszkozok/teszt_szerepmatrix.py` 238: `LG.LC('projekt_adat')` pár; a címkeváltástól független.
- `eszkozok/olvaso_pilot/adat.py` 560 és `felmeres.py` 290: `licencek.tsv` oszlopindex szerint (`r[9]` = cimke, `r[7]` allapot, `r[4]`, `r[5]`, `r[6]`); a `cimke` a JSON `licenc`-térképébe kerül. `sablon.html` 999–1055: `projekt_adat` kulcs és felirat („projekt adatréteg (adat/)”). Az olvasói pilot kimenete újragenerálódhat (nem a #89 hatóköre, jelzem).
- `eszkozok/olvaso_pilot/db_meres.py` 303, 383: a `licencek` tábla beolvasása a mérésbe.
- `eszkozok/feladatok.py` 72: a `licencek.tsv` a figyelt fájlok között (a tartalmát nem olvassa).
- **Nem érinti:** a `lekerdez.py`, az `ellenoriz.py` és a `general.py` közvetlenül nem hivatkozik a `projekt_adat`/`cimke`/`licenc_*` kulcsra; a `.github/workflows/*.yml` egyike sem olvassa a `licencek.tsv`-t (az `f06_forrasfelmeres.yml` „licenc” job-ja a külső forrásfelmérésé, más tárgy).

**A címkeváltás hatása a generált fájlokra (D2):** a `lexikon/` 8 fájlja hordozza a `licenc: projekt-adat` jelölést (összesen 146 előfordulás, GENERÁLT-KEZDET sorok és kolofon): `ALVIL-001`, `ANTROP-001`, `HAMART-001`, `HODIT-001`, `ISTENTISZT-001`, `KIRALY-001`, `MENNY-001`, `TEREMT-001` `_TUDOMANYOS.md`. A `_TORZSCIKK.md` fájlokban nincs találat. Frissítésük: `python eszkozok/general.py --cel lexikon` (kézzel tilos). A `generalt_proba/` (9 fájl, köztük `F78_szerepmatrix_proba`, `TEREMT-002_szotari_proba`) verziózott próbakimenet, törölni tilos; a régi címkét tartja (K2). Ha a `Karoli_Strong_kivonat` `tisztazott` lesz, a `cimke` is változik (`tisztázatlan` → a licenc szerinti rövid név), ami a kivonatot használó blokkok címkéit is érinti.

## 3. A `LICENSE` tervezete (D1 javaslat; a név helyőrző, nem jogi szöveg)

```
Copyright (c) <ÉV> <JOGTULAJDONOS NEVE>. Minden jog fenntartva.
All rights reserved.

1. Saját adat. A repó saját adatrétege minden jog fenntartva: az adat/*.tsv fájlok,
   az adat/karoli_strong/* és az adat/karoli_variancia.tsv, valamint a belőlük épített
   pardes.db saját táblái. A Károli–Strong párosítás a jogtulajdonos irányításával és
   ellenőrzésével készült.

2. Próza. A tanulmányok (tematikus_lezart/, genezis/, ujszovetseg/, melyelemzesek/,
   motivumlog/), a lexikon/ és a motivumok/ alatti motívumcikkek minden jog fenntartva.

3. Harmadik fél adata. A konkordancia/ alatti és a repóba átvett harmadik féltől
   származó adatra ez a nyilatkozat NEM terjed ki. Ezek licencét, a kötelező
   megjelöléseket és az állapotukat az adat/licencek.tsv rögzíti (köztük CC BY 4.0,
   CC BY-SA 4.0, közkincs és korlátozott felhasználású források); azok feltételei
   érvényesek. A saját adat harmadik fél adatából származtatott részére a forrás
   megjelölési és ShareAlike-feltételei továbbra is vonatkoznak.

4. Engedély nélkül a fentiek másolása, terjesztése, módosítása és felhasználása nem
   megengedett. Engedély: <KAPCSOLAT>.

Ez a nyilatkozat leltár, nem jogi vélemény.
```

## 4. Javaslat és nyitott kérdések (DT131, helyőrző; a DONTESEK.md-be nem írtam, mert a brief D1–D3-at már nevesíti)

- **D1 (felhasználó):** a `LICENSE` szövege (a fenti tervezet jó-e, fájlkörönként bontva) és a **jogtulajdonos neve + éve + kapcsolat**. Név nélkül nem írom meg a fájlt.
- **D2 (felhasználó):** új zárt `cimke`-érték `minden jog fenntartva`, a `projekt-adat` kivétel megszűnik (javaslat). Alternatíva: a `projekt-adat` címke marad, csak a licenc-szöveg változik (kisebb diff, de a címke nem mondja ki a jogállást). Hatás: a 8 lexikonfájl újragenerálása.
- **D3 (felhasználó):** `projekt_adat.kereskedelmi` = `igen` (javaslat: a jogtulajdonos maga kereskedelmileg felhasználhatja; harmadiknak a LICENSE nem ad jogot). `nem` esetén a legszigorúbb-érték szabály minden saját származtatott táblát `nem`-re vinne, és a #86 csomagja nem épülhetne rájuk.
- **K1:** az 1/B pont négy sorában (BDB, LXX_OS, Versifikacios_tablak, Konyv_nevtablak) az elavuló „a projekt_adat sorban tisztazatlan” mondatokhoz nyúlhatok-e (G1 szerint csak a megnevezett sorok változnak)?
- **K2:** a `generalt_proba/` régi címkéi maradjanak (javaslat), vagy kérsz új próbát?
- **K3:** a három újraértékelt sor (11, 33, 34) `tisztazott`-ra váltásának feltétele, hogy a `forras_hely` a SEMA 2.19 2. szabálya szerint a licenc szövegére mutasson; a lxx-morph/TVTMS-idézet a sorokban csak részben áll. Ha nem elég, a sor marad `tisztazatlan`, a megjegyzés megnevezi, min múlik (a brief szerint).
- **Jogász (DT116 listája):** a modell által előállított, a felhasználó által irányított Károli–Strong párosítás szerzői jogi védelme; a LICENSE tervezete a kereskedelmi kiadás előtt jogászi átnézést kap.

## 5. M1–M4 végrehajtás: igazolások és eltérések (F89.2–F89.5)

*Proveniencia: `scope=repó (F89 worktree) | forras=adat/licencek.tsv (split('\t')), eszkozok/general.py --cel lexikon, eszkozok/sqlite_epit.py --mod teljes | ts=2026-10-13`. A D1–D3 döntés: DT131 (felhasználó, 2026-10-13).*

**G1 (soronkénti összevetés, `licencek.tsv`).** Az írás előtt a szkript minden sort összevetett az eredetivel (`split('\t')`/`'\t'.join()`, `csv` nélkül, 10 mező ellenőrizve). Változott pontosan 4 sor: `projekt_adat`, `Karoli_Strong_kivonat`, `LXX_versszintu_parok`, `Karoli_versmegfeleltetes`; hozzáadva 3 sor: `Karoli_Strong_parok`, `Karoli_Strong_szavak`, `karoli_variancia`. A többi sor és a fejlécsorok bájtra azonosak.

**G2.** A `projekt_adat`: `tisztazott`, `kereskedelmi=igen`, `share_alike=nem`, `cimke=minden jog fenntartva`, `forras_hely` = a `LICENSE` 1. sora + DT131. A három új sor minden mezője kitöltött, a `kotelezo_megjeloles` szó szerint a TAHOT/TAGNT sor megjelölése ("Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)").

**K3 (újraértékelt sorok).** A `Karoli_Strong_kivonat`, `LXX_versszintu_parok`, `Karoli_versmegfeleltetes` mindhárom `tisztazott` lett: a projekt_adat sor `tisztazott`, a komponensek sorai (Karoli_1908 közkincs, Strong_szotar/LXX_OS/TAHOT `tisztazott`; a verse_pairs a LXX_OS sor szerint, a TVTMS-rész a Versifikacios_tablak sor szerint) szó szerinti idézetet hordoznak, és a `forras_hely` ezekre mutat. A `cimke` mindháromnál `minden jog fenntartva` (a saját rész jogállása; a harmadik fél komponensek a `licenc` oszlopban és a komponens-sorokban); ez a SEMA 2.19 `cimke`-szabályába beírva. Ha az orkesztrátor a vegyes sorokra CC BY 4.0 címkét szán, az a három sor `cimke` mezőjének átírása és a lexikon újragenerálása.

**K1.** Nem módosítottam a négy hivatkozó sor megjegyzését. Az elavult „a projekt_adat sorban tisztazatlan” mondat áll: `BDB` (7), `LXX_OS` (32), `Versifikacios_tablak` (41), `Konyv_nevtablak` (42).

**M2 (lexikon) — ELTÉRÉS A BRIEFTŐL, NEM COMMITOLTAM.** A brief szerint a `python eszkozok/general.py --cel lexikon` diffje csak a címkesorokat érinti. Ez nem teljesül: az éles `lexikon/*_TUDOMANYOS.md` (8 fájl) a generátorhoz és az adathoz képest már a #89 előtt elmaradt (a `--ellenoriz` a baseline-on, a régi `licencek.tsv`-vel is „frissítve lenne” üzenetet ad mind a 8 motívumra; kilépési kód 0). Az éles írás (`--ir`) 1476 beszúrt / 514 törölt sort adott, a címkesorokon kívül tartalmi blokkokat is (pl. KIRALY-001 `kizart`: 0 helyett 14 jelölt; `szocikkek`: szerepmátrixos átrendezés; `elofordulasok` sorok). A kézi szerkesztés tilos, a tartalmi újragenerálás nem a #89 hatóköre, ezért az éles `lexikon/` változatlan, és az újragenerálást az orkesztrátor döntésére hagytam (l. a jelentést). A `generalt_proba/` érintetlen (a próba-alapértelmezett futás egyik fájlját visszaállítottam, `git checkout`).
G3 igazolása a generátor próbafutásából (`--kimenet` ideiglenes könyvtár a repón kívül, a repó nem változott): a címkék a `licencek.tsv`-ből jönnek, `projekt-adat` egyik fájlban sincs. KIRALY-001 blokkok `licenc:` mezője: `tartalom`, `jelmagyarazat`, `kizart`, `kapcsolatok`, `idezes` (prózai és saját adatblokk) = `minden jog fenntartva`; `elofordulasok` = `minden jog fenntartva, közkincs, CC BY-SA 4.0` (saját adat + harmadik fél komponens); `szocikkek` (harmadik fél: BDB, Strong, UBS) = `CC BY 4.0, CC BY-SA 4.0, közkincs, minden jog fenntartva`; `lxx` = `CC BY 4.0, minden jog fenntartva`; `kereszthivatkozasok` = `CC BY 4.0, közkincs`. Sem a saját adat, sem a próza nem kapott szabad licenc-jelölést.

**M3–M4 (sqlite_epit.py, `pardes.db`).** A `teszt_sqlite_epit.py` 47 teszt zöld. Teljes építés: `pardes.db` 619.0 MB (előtte 878.9 MB: −259.9 MB, azaz a sor-szintű licenc-oszlopok teljes, korábban mért 259.9 MB-ja), 66 tábla = 66 `tabla_licenc`-sor (egyenként pontosan egy), egyik adattáblában sincs `licenc_allapot`/`kereskedelmi`/`licenc_dataset` oszlop. Két építés táblánkénti hash-e azonos (G6). `tisztazatlan` tábla: `kjv` (KJV_Strongs_teljes; nem a projekt_adat-on múlik). CC BY-SA 4.0 vagy MCGED címkéjű táblák (9): `lsj`, `mcged`, `sdbh_domenek`, `sdgnt_domenek`, `tw_szocikkek`, `ubs_dbh_jelentesek`, `ubs_dbh_referenciak`, `ubs_dntg_jelentesek`, `ubs_dntg_referenciak`; CC BY-NC tábla nincs a `pardes.db`-ben. A saját táblák címkéje `minden jog fenntartva` (a vegyes származtatottaké több címke `; `-vel, pl. `CC BY 4.0; minden jog fenntartva`).
