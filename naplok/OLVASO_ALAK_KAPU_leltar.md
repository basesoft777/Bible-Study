<!-- GENERÁLT: eszkozok/olvaso_szerver/teszt_olvaso_alak_kapu.py --leltar; kézzel ne szerkeszd -->
# Az olvasó alak-kapujának leltára

A hátralék és a bekötési leltár: minden belső alak, amely ma az olvasó lapjain látszik, mintánként és kódhelyenként. A darabszám a találatok (előfordulások) száma a bejárt lapokon; a kapu (`alak_kapu_hatralek.tsv`) a (minta, kódhely) osztályokat tartja, és új osztályra bukik.

- Szerverek: **main** = `http://localhost:8765` (main @ `0052c1f5`), **pr810** = `http://localhost:8775` (claude/olvaso-egyben-3464e1 @ `e0328691`)
- Bejárt lapok: 77 (egyéb 6, fejezet 3, kereső 6, szó 25, szókártya 3, vers 32, vers-töredék 2); a `merce/` 18 lapja, a vers fülei és rétege, szókártya, kereső, egyéb lapok, és rögzített magú (20261123) véletlen minta: 12 vers, 12 szó.
- A kódhely ennek a checkoutnak a kódjából áll (a sorszám a `main`-é); a blokk-azonosító (`data-blokk`) mindkét ágon azonos.
- Nem 200-as lapok: main: /szo/H9999=404; pr810: /szo/H9999=404

## Összesítés

| minta | main (db) | pr810 (db) | main (osztály) | pr810 (osztály) |
|---|---:|---:|---:|---:|
| `tablanev` — adatbázis-táblanév (pl. `token_par`, `lxx_bridge`; zárójelben aláhúzás nélkül is, pl. `(bdb)`) | 1406 | 1183 | 48 | 46 |
| `dataset_kod` — dataset- vagy provenienciakód aláhúzással (pl. `projekt_adat`, `Karoli_Strong_parok`) | 997 | 826 | 44 | 42 |
| `alahuzas_azonosito` — egyéb aláhúzásos belső azonosító (pl. `tW_szocikkek`) | 12 | 12 | 4 | 4 |
| `proveniencia_sor` — nyers proveniencia-mező (`scope=`, `forras=`, `ts=`) | 66 | 1065 | 2 | 3 |
| `rc_link` — nyers `rc://` hivatkozás (translationWords) | 0 | 0 | 0 | 0 |
| `tw_kategoria` — translationWords kategóriakód (pl. `(kt, kt/angel)`, `other/wrong`) | 40 | 40 | 2 | 2 |
| `md_felkover` — nyers Markdown félkövér (`**…**`) | 0 | 0 | 0 | 0 |
| `md_link` — nyers Markdown hivatkozás (`[…](…)`) | 0 | 0 | 0 | 0 |
| `md_cimsor` — nyers Markdown címsor (sor eleji `#`) | 0 | 0 | 0 | 0 |
| `angol_cimke_tw` — angol szótárcímke, translationWords (pl. `Definition:`) | 180 | 180 | 2 | 2 |
| `angol_cimke_lexikon` — angol szótárcímke, lexikon (pl. `Derivation:`, `See:`, `KJV:`) | 159 | 163 | 3 | 4 |
| `hosszu_szamazonosito` — hosszú számazonosító (12+ jegy, pl. a 15 jegyű UBS-azonosító) | 555 | 372 | 4 | 5 |
| `kalap_index` — nyers `^` index | 147 | 4 | 3 | 3 |
| `licenc_ellentmondas` — ellentmondó licencmondat (`CC BY` és „minden jog fenntartva” egy mondatban) | 80 | 158 | 7 | 7 |
| `gepi_datum` — nyers dátumos gépi jelölés (pl. „Lefordítva · gépi fordítás, 2026.10.01”) | 16 | 16 | 1 | 1 |
| `fajlnev` — belső fájlnév (`.db`, `.tsv`, `.py`, `.md`, `.json`, `.toml`) | 81 | 81 | 2 | 2 |
| **összesen** | **3739** | **4100** | **122** | **121** |

## Eltérés a szerverek között (hibaosztály: minta · kódhely)

- csak **main**: `dataset_kod` · `blokk:szo.magyar_gorog`, `dataset_kod` · `forrássor:vers.kapcsolat`, `dataset_kod` · `forrássor:vers.motivum`, `proveniencia_sor` · `blokk:szo.magyar_gorog`, `tablanev` · `forrássor:vers.kapcsolat`, `tablanev` · `forrássor:vers.motivum`
- csak **pr810**: `angol_cimke_lexikon` · `blokk:vers.lxx_versszam`, `dataset_kod` · `lapváz:p.ures`, `hosszu_szamazonosito` · `blokk:szo.usz`, `proveniencia_sor` · `blokk:szo.ebben`, `proveniencia_sor` · `blokk:vers.par`

## `tablanev` — adatbázis-táblanév (pl. `token_par`, `lxx_bridge`; zárójelben aláhúzás nélkül is, pl. `(bdb)`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `forrássor:szo.bdb_apparatus` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 160 | 160 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: BDB (bdb): közkincs · BDB+projekt_adat (bdb_alia |
| `forrássor:szo.ebben` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 24 | 24 | szó, szókártya | `/szo/H0216?vers=1Moz/1/3` `/r/szo/H0216?ig=1Moz/1/3` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 · TAHOT+TAGNT (token_eredet |
| `forrássor:szo.elofordulas` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 27 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: TAHOT+TAGNT (token_strong): CC BY 4.0 |
| `forrássor:szo.heber_hatter` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 18 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: lxx_bridge (lxx_bridge): CC BY 4.0 |
| `forrássor:szo.karoli_alakok` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 27 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 |
| `forrássor:szo.lsj` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 22 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: LSJ (lsj): CC BY-SA 4.0 [share-alike] · projekt_ |
| `forrássor:szo.lxx_bridge` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 20 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: lxx_bridge (lxx_bridge): CC BY 4.0 |
| `forrássor:szo.magyar_gorog` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.mcged` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: MCGED (mcged): © Mounce 1993 [nem kereskedelmi] |
| `forrássor:szo.oshl` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 32 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: OSHL (oshl_lexikalis_index): CC BY 4.0 · OSHL_BDB (oshl_bdb_igehel |
| `forrássor:szo.oshl_csalad` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: OSHL (oshl_lexikalis_index): CC BY 4.0 |
| `forrássor:szo.sdbh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 32 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: SDBH (sdbh_domenek): CC BY-SA 4.0 [share-alike] · projekt_ |
| `forrássor:szo.sdgnt` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 22 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: SDGNT (sdgnt_domenek): CC BY-SA 4.0 [share-alike] · projekt_ |
| `forrássor:szo.sece_g` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: SECE_G (sece_g): közkincs |
| `forrássor:szo.sece_h` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: SECE_H (sece_h): közkincs |
| `forrássor:szo.szotar` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 54 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: Strong_szotar (strong_szotar): CC BY 4.0 · TBESH+TAHOT+projekt_adat  |
| `forrássor:szo.tbesg` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 22 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: TBESG (tbesg): CC BY 4.0 · projekt_adat (forditasok) |
| `forrássor:szo.tbesh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 48 | 42 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: TBESH (tbesh): CC BY 4.0 · TBESH+TAHOT+projekt_adat  |
| `forrássor:szo.thayer` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: Thayer (thayer): közkincs |
| `forrássor:szo.tw_g` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 16 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: tW_szocikkek (tw_szocikkek): CC BY-SA 4.0 [feltételesen kereskedel |
| `forrássor:szo.tw_h` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 12 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: tW_szocikkek (tw_szocikkek): CC BY-SA 4.0 [feltételesen kereskedel |
| `forrássor:szo.ubs_dbh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 30 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: UBS_DBH (ubs_dbh_jelentesek): CC BY-SA 4.0 [share-alike] · projekt_ |
| `forrássor:szo.ubs_dntg` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: UBS_DNTG (ubs_dntg_jelentesek): CC BY-SA 4.0 [share-alike] |
| `forrássor:szo.usz` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 33 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: TAHOT+TAGNT (token_strong): CC BY 4.0 · Karoli_1908 (vers): közki |
| `forrássor:vers.bsb` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: BSB_Strongs (bsb): CC0 1.0 |
| `forrássor:vers.eredeti` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: TAHOT+TAGNT (token_eredeti): CC BY 4.0 |
| `forrássor:vers.heber_csempe` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 182 | 119 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: TAHOT+TAGNT (token_eredeti): CC BY 4.0 · Macula_heber (token_macul |
| `forrássor:vers.kapcsolat` | blokkok.py:2348 'forras_sor' | 2 | 0 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (kapcsolatok): minden jog fenntartva |
| `forrássor:vers.karoli` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Karoli_1908 (vers): közkincs |
| `forrássor:vers.kh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 1 | vers | `/1Moz/1/1?ful=kh` `/Jan/1/1?ful=kh` | li_KH+Karoli_KH_MEK+Karoli_KH_javitott (kh): közkincs; CC BY 4.0 |
| `forrássor:vers.kjv` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: KJV_Strongs_teljes (kjv): tisztázatlan [tisztázatlan] |
| `forrássor:vers.lxx_csempe` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_OS (lxx_token): CC BY 4.0 |
| `forrássor:vers.lxx_dontes` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 1 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: projekt_adat (lxx_dontesek): minden jog fenntartva |
| `forrássor:vers.lxx_par` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 9 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_versszintu_parok (lxx_versszintu_parok): minden jog fenntartva |
| `forrássor:vers.lxx_szavak` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_OS (lxx_token): CC BY 4.0 |
| `forrássor:vers.lxx_versszam` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | kacios_tablak+Karoli_versmegfeleltetes (lxx_versszam): CC BY 4.0; minden jog fenntartva |
| `forrássor:vers.macula_gorog` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 16 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Macula_heber (token_macula): CC BY 4.0 |
| `forrássor:vers.macula_morf` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 16 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Macula_heber (token_macula): CC BY 4.0 |
| `forrássor:vers.morf_hu` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 130 | 80 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: morf_kulcs_heber (morf_kulcs_heber): CC BY 4.0 · Macula_ |
| `forrássor:vers.motivum` | blokkok.py:2348 'forras_sor' | 4 | 0 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (elofordulasok): minden jog fenntartva · Karoli_1908 ( |
| `forrássor:vers.nave` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 6 | 6 | vers | `/1Moz/1/1?ful=temak` `/Jan/1/1?ful=temak` | sokant+Karoli_versmegfeleltetes+LXX_OS (nave_vers): közkincs; minden jog fenntartva; CC B |
| `forrássor:vers.par` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 |
| `forrássor:vers.tanulmany` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 2 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (tanulmany): minden jog fenntartva |
| `forrássor:vers.tipnr` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 1 | vers | `/1Moz/1/1?ful=temak` `/Jan/1/1?ful=temak` | Forrás és licenc: TIPNR (tipnr): CC BY 4.0 |
| `forrássor:vers.tsk` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 2 | vers | `/1Moz/1/1?ful=kh` `/Jan/1/1?ful=kh` | Forrás és licenc: TSK (tsk): CC BY 4.0 |
| `forrássor:vers.ubs` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: UBS_DBH (ubs_dbh_referenciak): CC BY-SA 4.0 [share-alike] |
| `forrássor:vers.versszamozas` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | : Karoli_versmegfeleltetes+BSB_Strongs (vers_szamozas): minden jog fenntartva; CC0 1.0 |
| `lapváz:div.szoveg-jegy` | sablonok/fejezet.html:76 | 35 | 35 | egyéb, fejezet, kereső, vers | `/1Moz/1` `/Zsolt/22` | Forrás és licenc: Karoli_1908 (vers): közkincs |

## `dataset_kod` — dataset- vagy provenienciakód aláhúzással (pl. `projekt_adat`, `Karoli_Strong_parok`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.magyar_gorog` | blokkok.py:2108 '_r_magyar_gorog' | 12 | 0 | szó | `/szo/G1311` `/szo/G2671` | UBS_DNTG, 20.40. jelentés · definíció |
| `blokk:vers.lxx_dontes` | blokkok.py:530 '_r_lxx_dontes' | 1 | 1 | vers | `/1Moz/4/7` | οὐκ ἐὰν ὀρθῶς προσενέγκῃς …); Macula és LXX_OS egyezik. |
| `blokk:vers.lxx_szavak` | blokkok.py:288 '_r_lxx_szavak' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Görög szóalak és LXX-vers szavai (LXX_OS) forrásadat |
| `blokk:vers.lxx_versszam` (attr:title, szöveg) | blokkok.py:305 '_r_lxx_versszam' | 17 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | LXX_OS |
| `forrássor:szo.bdb_apparatus` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 80 | 80 | szó, szókártya | `/szo/H1242` `/szo/H7451` | ás és licenc: BDB (bdb): közkincs · BDB+projekt_adat (bdb_alias): közkincs; minden jog fennt |
| `forrássor:szo.ebben` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 14 | 14 | szó, szókártya | `/szo/H0216?vers=1Moz/1/3` `/r/szo/H0216?ig=1Moz/1/3` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 · TAHOT+TAGNT (t |
| `forrássor:szo.karoli_alakok` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 27 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 |
| `forrássor:szo.lsj` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | LSJ (lsj): CC BY-SA 4.0 [share-alike] · projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.magyar_gorog` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.oshl` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | SHL (oshl_lexikalis_index): CC BY 4.0 · OSHL_BDB (oshl_bdb_igehelyek): CC BY 4.0 |
| `forrássor:szo.sdbh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | _domenek): CC BY-SA 4.0 [share-alike] · projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.sdgnt` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | _domenek): CC BY-SA 4.0 [share-alike] · projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.sece_g` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: SECE_G (sece_g): közkincs |
| `forrássor:szo.sece_h` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: SECE_H (sece_h): közkincs |
| `forrássor:szo.szotar` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 54 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: Strong_szotar (strong_szotar): CC BY 4.0 · TBESH+TAHO |
| `forrássor:szo.tbesg` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | s és licenc: TBESG (tbesg): CC BY 4.0 · projekt_adat (forditasok): minden jog fenntartva |
| `forrássor:szo.tbesh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 28 | szó, szókártya | `/szo/H1242` `/szo/H7451` |  TBESH (tbesh): CC BY 4.0 · TBESH+TAHOT+projekt_adat (glosszak_heber_hu): CC BY 4.0; minden  |
| `forrássor:szo.tw_g` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 22 | 16 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: tW_szocikkek (tw_szocikkek): CC BY-SA 4.0 [feltétele |
| `forrássor:szo.tw_h` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 12 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: tW_szocikkek (tw_szocikkek): CC BY-SA 4.0 [feltétele |
| `forrássor:szo.ubs_dbh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 32 | 30 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Forrás és licenc: UBS_DBH (ubs_dbh_jelentesek): CC BY-SA 4.0 [sha |
| `forrássor:szo.ubs_dntg` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 11 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Forrás és licenc: UBS_DNTG (ubs_dntg_jelentesek): CC BY-SA 4.0 [sh |
| `forrássor:szo.usz` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 11 | 22 | szó, szókártya | `/szo/G0264` `/szo/G3056` | TAHOT+TAGNT (token_strong): CC BY 4.0 · Karoli_1908 (vers): közkincs |
| `forrássor:vers.bsb` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: BSB_Strongs (bsb): CC0 1.0 |
| `forrássor:vers.heber_csempe` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 52 | 34 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | AHOT+TAGNT (token_eredeti): CC BY 4.0 · Macula_heber (token_macula): CC BY 4.0 · LXX_OS (lxx |
| `forrássor:vers.kapcsolat` | blokkok.py:2348 'forras_sor' | 2 | 0 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (kapcsolatok): minden jog fenntartva |
| `forrássor:vers.karoli` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Karoli_1908 (vers): közkincs |
| `forrássor:vers.kh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 6 | 3 | vers | `/1Moz/1/1?ful=kh` `/Jan/1/1?ful=kh` | Forrás és licenc: Karoli_KH+Karoli_KH_MEK+Karoli_KH_javitott (kh):  |
| `forrássor:vers.kjv` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: KJV_Strongs_teljes (kjv): tisztázatlan [tisztázatlan] |
| `forrássor:vers.lxx_csempe` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_OS (lxx_token): CC BY 4.0 |
| `forrássor:vers.lxx_dontes` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 1 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: projekt_adat (lxx_dontesek): minden jog fenntartva |
| `forrássor:vers.lxx_par` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 9 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_versszintu_parok (lxx_versszintu_parok): minden jog fenn |
| `forrássor:vers.lxx_szavak` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_OS (lxx_token): CC BY 4.0 |
| `forrássor:vers.lxx_versszam` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 78 | 51 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: LXX_OS+Versifikacios_tablak+Karoli_versmegfele |
| `forrássor:vers.macula_gorog` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 16 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Macula_heber (token_macula): CC BY 4.0 |
| `forrássor:vers.macula_morf` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 16 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Macula_heber (token_macula): CC BY 4.0 |
| `forrássor:vers.morf_hu` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 16 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | s_heber (morf_kulcs_heber): CC BY 4.0 · Macula_heber (token_macula): CC BY 4.0 · morf_nyelv_ |
| `forrássor:vers.motivum` | blokkok.py:2348 'forras_sor' | 4 | 0 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (elofordulasok): minden jog fenntartva  |
| `forrássor:vers.nave` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 10 | 10 | vers | `/1Moz/1/1?ful=temak` `/Jan/1/1?ful=temak` | Forrás és licenc: Nave_basokant+Karoli_versmegfeleltetes+LXX_OS (nave_v |
| `forrássor:vers.par` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 26 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Karoli_Strong_parok (token_par): CC BY 4.0 |
| `forrássor:vers.tanulmany` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 2 | vers | `/1Moz/1/1?ful=motivum` `/Jan/1/1?ful=motivum` | Forrás és licenc: projekt_adat (tanulmany): minden jog fenntartva |
| `forrássor:vers.ubs` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 17 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: UBS_DBH (ubs_dbh_referenciak): CC BY-SA 4.0 [sh |
| `forrássor:vers.versszamozas` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 52 | 34 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | Forrás és licenc: Karoli_versmegfeleltetes+BSB_Strongs (vers_szamozas): minden jog |
| `lapváz:div.szoveg-jegy` | sablonok/fejezet.html:76 | 36 | 36 | egyéb, fejezet, kereső, vers | `/1Moz/1` `/Zsolt/22` | Forrás és licenc: Karoli_1908 (vers): közkincs |
| `lapváz:div.tan-szoveg` | sablonok/tanulmany.html:10 | 2 | 2 | egyéb | `/tanulmany/1Moz_10v1-11v32` `/tanulmany/1Moz_12v1-20` | Forrás-hivatkozási fegyelem: Strong_szotar.tsv, BDB_teljes_unabridged.tsv, TAHOT_k |
| `lapváz:p.ures` | sablonok/_vers_panel.html:12 | 0 | 9 | vers, vers-töredék | `/Jan/1/1` `/Jan/1/1?ful=szo` | ula), Görög szóalak és LXX-vers szavai (LXX_OS), Az igealak magyar feloldása, LXX-ford |

## `alahuzas_azonosito` — egyéb aláhúzásos belső azonosító (pl. `tW_szocikkek`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:vers.lxx_dontes` | blokkok.py:530 '_r_lxx_dontes' | 1 | 1 | vers | `/1Moz/4/7` | eltero_forditas |
| `blokk:vers.macula_gorog` (attr:title) | blokkok.py:263 '_r_macula_gorog' | 2 | 2 | vers | `/Zsolt/126/4` | nem_igazolt:strong_elteres; forrásalak (upstream):  |
| `blokk:vers.versszamozas` (attr:title, szöveg) | blokkok.py:315 '_r_versszamozas' | 2 | 2 | vers | `/Zsolt/22/2` `/En/5/11` | lxx_os_etalon_f91 |
| `lapváz:div.tan-szoveg` | sablonok/tanulmany.html:10 | 7 | 7 | egyéb | `/tanulmany/1Moz_10v1-11v32` `/tanulmany/1Moz_12v1-20` | ivatkozási fegyelem: Strong_szotar.tsv, BDB_teljes_unabridged.tsv, TAHOT_kivonat.tsv. |

## `proveniencia_sor` — nyers proveniencia-mező (`scope=`, `forras=`, `ts=`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.ebben` (attr:title) | blokkok.py:715 '_r_ebben' | 0 | 6 | szó, szókártya | `/szo/H0216?vers=1Moz/1/3` `/r/szo/H0216?ig=1Moz/1/3` |  intervallum: 96,4–99,7%; proveniencia: scope=F172 pontosságmérés, rétegek \| forras=f17 |
| `blokk:szo.karoli_alakok` (attr:title) | blokkok.py:830 '_r_karoli_alakok' | 48 | 81 | szó, szókártya | `/szo/H1242` `/szo/H7451` | tervallum: 93,81–96,32%); proveniencia: scope=F172 pontosságmérés, OSSZES (súlyozott) \| |
| `blokk:szo.magyar_gorog` (attr:title) | blokkok.py:2108 '_r_magyar_gorog' | 18 | 0 | szó, szókártya | `/szo/G3056` `/szo/G1311` | proveniencia: scope=seed-204, véletlen 200 ÚSZ-hivatkozás (16 |
| `blokk:vers.par` (attr:title) | blokkok.py:227 '_r_par' | 0 | 978 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` |  intervallum: 96,4–99,7%; proveniencia: scope=F172 pontosságmérés, rétegek \| forras=f17 |

## `tw_kategoria` — translationWords kategóriakód (pl. `(kt, kt/angel)`, `other/wrong`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.tw_g` | blokkok.py:2013 '_r_tw' | 16 | 16 | szó, szókártya | `/szo/G0264` `/szo/G3056` | , vétkezés sin, sinful, sinner, sinning (kt, kt/sin) |
| `blokk:szo.tw_h` | blokkok.py:2013 '_r_tw' | 24 | 24 | szó | `/szo/H7451` `/szo/H3615` | llem demon, evil spirit, unclean spirit (kt, kt/demon) |

## `angol_cimke_tw` — angol szótárcímke, translationWords (pl. `Definition:`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.tw_g` | blokkok.py:2013 '_r_tw' | 75 | 75 | szó, szókártya | `/szo/G0264` `/szo/G3056` | Definition: |
| `blokk:szo.tw_h` | blokkok.py:2013 '_r_tw' | 105 | 105 | szó | `/szo/H7451` `/szo/H3615` | Definition: |

## `angol_cimke_lexikon` — angol szótárcímke, lexikon (pl. `Derivation:`, `See:`, `KJV:`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.sece_g` | blokkok.py:1887 '_r_szoveg' | 81 | 81 | szó, szókártya | `/szo/G0264` `/szo/G3056` | m-ar-tan'-o｜verb｜to sin) [Grk] ἁμαρτάνω LN: 88.289 GK: G279 Hebrew: אָשַׁם, חָטָא, מ |
| `blokk:szo.sece_h` | blokkok.py:1887 '_r_szoveg' | 77 | 77 | szó, szókártya | `/szo/H1242` `/szo/H7451` | (subs｜morning) OSHL: b.cu.ad TWOT: 274c GK: H1331, H1332 Greek: ἡμέρα, ὄρθρος, πρωΐ |
| `blokk:szo.tw_h` | blokkok.py:2013 '_r_tw' | 1 | 1 | szó | `/szo/H7451` | lated in a local or national language. (See: How to Translate Unknowns) |
| `blokk:vers.lxx_versszam` (attr:title) | blokkok.py:305 '_r_lxx_versszam' | 0 | 4 | vers | `/Zsolt/22/2` `/Zsolt/126/4` | LXX_OS: Psalms (LXX) 21:2; KJV: Psa.21:1-2 \| Psa.21:2 |

## `hosszu_szamazonosito` — hosszú számazonosító (12+ jegy, pl. a 15 jegyű UBS-azonosító)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.sdbh` (attr:title, szöveg) | blokkok.py:1868 '_r_sdbh' | 64 | 64 | szó, szókártya | `/szo/H1242` `/szo/H7451` | 002002002010 |
| `blokk:szo.ubs_dbh` (attr:title, szöveg) | blokkok.py:2184 '_r_ubs_dbh' | 67 | 67 | szó, szókártya | `/szo/H1242` `/szo/H7451` | 001148001001000 |
| `blokk:szo.ubs_dntg` (attr:title, szöveg) | blokkok.py:2243 '_r_ubs_dntg' | 285 | 53 | szó, szókártya | `/szo/G0264` `/szo/G3056` | 000262001001000 |
| `blokk:szo.usz` (attr:title) | blokkok.py:2194 '_r_usz' | 0 | 49 | szó, szókártya | `/szo/G0264` `/szo/G3056` | UBS DNTG jelentés-azonosító: 000262001001000 |
| `blokk:vers.ubs` | blokkok.py:763 '_r_ubs' | 139 | 139 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | 000396001003000 |

## `kalap_index` — nyers `^` index

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.bdb_apparatus` (attr:title, szöveg) | blokkok.py:1753 '_r_bdb_apparatus' | 145 | 2 | szó, szókártya | `/szo/H1242` `/szo/H7451` | ínűleg = 2300 fél nap Ew Hi Meinh Bev Dr^Intr. 464, vö. 8:26 & 3 2-Jan idők (évek |
| `blokk:vers.heber_csempe` | blokkok.py:648 '_r_heber_csempe' | 1 | 1 | vers | `/1Moz/4/7` | אִם֙veimifH0518kötőszó "{..^δὲ}" |
| `blokk:vers.macula_gorog` | blokkok.py:263 '_r_macula_gorog' | 1 | 1 | vers | `/1Moz/4/7` | "{..^δὲ}" |

## `licenc_ellentmondas` — ellentmondó licencmondat (`CC BY` és „minden jog fenntartva” egy mondatban)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `forrássor:szo.bdb_apparatus` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 32 | szó, szókártya | `/szo/H1242` `/szo/H7451` | ekt_adat (bdb_vers_jelentes): közkincs; CC BY 4.0; minden jog fenntartva · TAHOT+TAGNT (token_eredeti): CC BY… |
| `forrássor:szo.ebben` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 4 | szó, szókártya | `/szo/H0216?vers=1Moz/1/3` `/r/szo/H0216?ig=1Moz/1/3` | TAHOT+projekt_adat (glosszak_heber_hu): CC BY 4.0; minden jog fenntartva · Strong_szotar (strong_szotar): CC … |
| `forrássor:szo.szotar` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 54 | szó, szókártya | `/szo/H1242` `/szo/H7451` | TAHOT+projekt_adat (glosszak_heber_hu): CC BY 4.0; minden jog fenntartva |
| `forrássor:szo.tbesh` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 16 | 28 | szó, szókártya | `/szo/H1242` `/szo/H7451` | TAHOT+projekt_adat (glosszak_heber_hu): CC BY 4.0; minden jog fenntartva · projekt_adat (forditasok): minden … |
| `forrássor:vers.lxx_versszam` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 26 | 34 | vers, vers-töredék | `/1Moz/1/1` `/1Moz/1/5` | aroli_versmegfeleltetes (lxx_versszam): CC BY 4.0; minden jog fenntartva |
| `forrássor:vers.nave` (attr:title, szöveg) | blokkok.py:2348 'forras_sor' | 2 | 4 | vers | `/1Moz/1/1?ful=temak` `/Jan/1/1?ful=temak` | eleltetes+LXX_OS (nave_vers): közkincs; minden jog fenntartva; CC BY 4.0 · Nave_basokant (nave_basokant): kö |
| `lapváz:div.szoveg-jegy` | sablonok/fejezet.html:76 | 2 | 2 | kereső | `/kereses?q=vil%C3%A1goss%C3%A1g` `/kereses?q=xyzqq` | trong_szavak (szotari_token_kotojeles): minden jog fenntartva; CC BY 4.0 · Karoli_Strong_parok (token_par):  |

## `gepi_datum` — nyers dátumos gépi jelölés (pl. „Lefordítva · gépi fordítás, 2026.10.01”)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `blokk:szo.bdb_apparatus` | blokkok.py:1753 '_r_bdb_apparatus' | 16 | 16 | szó, szókártya | `/szo/H1242` `/szo/H7451` | Lefordítva · gépi fordítás, 2026.10.25 |

## `fajlnev` — belső fájlnév (`.db`, `.tsv`, `.py`, `.md`, `.json`, `.toml`)

| kódhely | forráshely | main | pr810 | oldaltípus | példa URL | példa |
|---|---|---:|---:|---|---|---|
| `lapváz:div.tan-szoveg` | sablonok/tanulmany.html:10 | 9 | 9 | egyéb | `/tanulmany/1Moz_10v1-11v32` `/tanulmany/1Moz_12v1-20` | Forrás-hivatkozási fegyelem: Strong_szotar.tsv, BDB_teljes_unabridged.tsv, TAHOT_kivon |
| `lapváz:footer.labjegyzet` | sablonok/alap.html:29 | 72 | 72 | egyéb, fejezet, kereső, szó, vers | `/szo/H1242` `/szo/H7451` | datok a repó TSV-táblázataiból generált pardes.db-ből jönnek; a blokkok és a szövegoszlop |
