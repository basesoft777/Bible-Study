# Olvasói pilot (nem éles)

Az olvasói nézet első, belső próbája (2026-10-05): egy szakasz folyamatos Károli-szövege, kattintható szavakkal, jobb oldalon a héber és görög szó-lapokkal és a versrészletekkel. Hatóköre: **1Móz 1–25** (693 vers) és **Zsolt 22** (32 vers); az 1Móz 1:1–2:3 a regressziós alap (a prototípus szakasza). A továbbfejlesztés és az értékelés a **#60 OLVASOI_PILOT** feladat (`F60_OLVASOI_PILOT_BRIEF.md`; a v2 bővítés: a repó minden használható, már meglévő adata a lapon, és a pilot datasetjének felmérése).

## Futtatás

```bash
python eszkozok/olvaso_pilot/adat.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/epit.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/adat.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/epit.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/adat.py --szakasz "1Móz 1-25"        # a #60 v2 hatókör (~30 s)
python eszkozok/olvaso_pilot/epit.py --szakasz "1Móz 1-25"
python eszkozok/olvaso_pilot/adat.py --szakasz "Zsolt 22" --kiadas nyilvanos   # a KJV-Strong blokk (GPL) nélkül
python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py               # 100 teszt, ~100 s (az 1Móz 1–25 futás és a prototípus-regresszió is benne)
python eszkozok/olvaso_pilot/db_meres.py                         # a pardes.db mérése (csak olvas; D1–D5)
python eszkozok/olvaso_pilot/meres.py        # naplok/OLVASOI_PILOT_meres.md (újrafuttatja az adat.py-t és az epit.py-t)
python eszkozok/olvaso_pilot/felmeres.py     # naplok/OLVASOI_PILOT_adatfelmeres.md (az adat.py-t újrafuttatja)
```

A `--szakasz` vers-tartomány (`"1Móz 1:1-2:3"`), fejezet-tartomány (`"1Móz 1-25"`, a #60 v2 hatóköre) vagy egész fejezet (`"Zsolt 22"`); a versek a `Karoli_1908.tsv`-ből jönnek, a könyvfájlok a `szakasz.py` `KONYVFAJLOK` táblájából (ma: 1Móz, Zsolt; más könyvre a pilot hibával áll meg). Az `adat.py` és az `epit.py` a `--kimenet KÖNYVTÁR` könyvtárba ír, alapból a repón kívüli `<temp>/olvaso_pilot/<szakasz-azonosító>/` könyvtárba. A `--kiadas {belso,nyilvanos,kereskedelmi}` (csak az `adat.py`-n; alap: `belso`) a kiadás típusa szerint kiveszi a licenc miatt kimaradó blokkokat (l. „Kiadás-kapcsoló” alább). A kimenet (`olvaso_pilot.json`, `karoli_konkordancia_proba.html`) nem kerül a repóba. A `ts=` mező a futás UTC ideje. Böngészős próba: `python -m http.server <szabad port>` a kimeneti könyvtárból, a végén a folyamat leállítandó.

Az oldal egyetlen önálló HTML (minden adat beágyazva, gzip+base64 alakban: az 1Móz 1–25 oldala 11,2 MB, a Zsolt 22 3,1 MB, a 16 MB-os határ alatt, ezért nincs lusta betöltés; a nyers beágyazás az 1Móz 1–25-re 35,8 MB lenne, MB = 10^6 bájt; a határ átlépésekor a nagy szövegeket — SECE, LSJ, tW, TBESH, BDB teljes szöveg — külön JSON-ba kellene tenni). A görög lapon a TBESG- és a Thayer-szöveg vágás nélkül, gördíthető blokkban áll.

| Fájl | Szerep |
|---|---|
| `szakasz.py` | a `--szakasz` feloldása (versek, könyvfájlok, szakaszcím) |
| `adat.py` | adatkinyerés a repó tábláiból (csak olvas), JSON-kimenet; a fő szó, a görög szóalak, a BDB-alias szabálya |
| `bovites.py` | a v2 bővítés: szó-lap és vers-lap blokkok további táblákból; a vers-kulcsok (MT, KJV); a Macula igealak-kód feloldása (`MorfKulcs`) |
| `bdb_szelet.py` | a BDB-szócikk gépi bontása apparátusokra (címszó, alapjelentés, nyelvi háttér, alakok, törzsek, jelentésszerkezet, jelek) |
| `epit.py` | a JSON beágyazása a sablonba |
| `sablon.html` | az oldal (HTML, CSS, JS); a tartalmat a beágyazott JSON-ból rajzolja |
| `meres.py` | a pilot-oldalra kerülő adat mérése → `naplok/OLVASOI_PILOT_meres.md` |
| `felmeres.py` | az adatkészletek felmérése → `naplok/OLVASOI_PILOT_adatfelmeres.md` |
| `db_meres.py` | a `pardes.db` mérése (M2b, D1–D5): csak olvas (`mode=ro`), nem épít újra |
| `teszt_olvaso_pilot.py` | tesztek: szakasz, fő szó, görög szóalak, BDB-bontás, bővítés, proveniencia, „csak adat” ellenőrzés, a Szó / Vers részletei fülváltás (statikus: a `[hidden]` CSS-szabály megvan), az értékazonos prototípus-regresszió (`ce4ef98f`, engedélyezett-eltérés lista), az 1Móz 1–25 (693 vers), a teljes angol szöveg, a `--kiadas` kapcsoló, a `db_meres.py` |

## Alapszabály: csak adat, és a jellege jelölve

A lapon minden tartalom a repó egy táblájából jön; magyarázó szöveg nincs rajta (felhasználói döntés, 2026-10-05). Új adatot a pilot nem állít elő (v2: 2026-10-07): csak meglévő táblát jelenít meg vagy mér. Minden blokk címe mellett a jellege áll:

| Jelleg | Jelentése | Példa |
|---|---|---|
| **forrásadat** | változtatás nélkül egy adatkészletből | Károli-szöveg, TAHOT, LXX_OS, TSK, BDB angolul, UBS DBH, lxx_bridge, SDBH/SDGNT, SECE, OSHL, TBESH, LSJ, MCGED, tW, BSB, KJV, Nave, TIPNR, az adatréteg sorai |
| **gépi feldolgozás** | determinisztikus szabály rendezi vagy párosítja a forrásadatot | BDB-bontás, a fő héber szó választása, a görög szóalak párosítása, rövid jelentés kivágása, vers-kulcsok (MT, KJV), a Nave-tartomány bontása versekre, a TIPNR-illesztés, az igealak-kód feloldása, a BDB-alias |
| **modell-kimenet** | nyelvi modell állította elő; javaslat-értékű | Károli–Strong párosítás (#22), BDB magyarul (#38), Thayer/UBS magyarul (#28) |

A „?” jel a blokk adatkészletét, fájlját és licencét mutatja (`adat/licencek.tsv`); a licenc mellett a `tisztázatlan`, a `nem kereskedelmi` és a `share-alike` jelzés is megjelenik, ahol a licenc-tábla ezt rögzíti. A teszt ellenőrzi, hogy a sablon minden blokk-címe kap jelleg-címkét és adatforrást, és hogy a lapon nincs feladatszám.

## A bővítés blokkjai (v2)

| Hol | Blokk | Tábla (kulcs) |
|---|---|---|
| szó-lap (héber) | Szemantikai domén (SDBH), SECE-szócikk (héber), TWOT- és BDB-azonosító (OSHL), Bővített Strong-szócikk (TBESH), translationWords (tW) | `SDBH_domenek` + `SDBH_SDGNT_domenfa`, `SECE_H_teljes`, `OSHL_lexikalis_index`, `TBESH.txt`, `tW_szocikkek` (Strong) |
| szó-lap (görög) | Szemantikai domén (SDGNT), UBS DNTG jelentések (angol), LSJ-szócikk, Mounce-szótár (MCGED), SECE-szócikk (görög), translationWords; az ÚSZ-helyek mellett a UBS DNTG besorolása | `SDGNT_domenek`, `UBS_DNTG_jelentesek` + `_referenciak`, `LSJ_teljes`, `MCGED_teljes`, `SECE_G_teljes`, `tW_szocikkek` (Strong) |
| vers-lap | Angol szó szavanként (BSB, KJV), Témák (Nave), Tulajdonnevek (TIPNR), Motívumadat / Igehely-kapcsolatok / LXX-fordítói döntések (adatréteg, soronként a saját proveniencia-mezővel), LXX versszintű együttelőfordulás, LXX többlet és számozási eltérés | `BSB_Strongs`, `KJV_Strongs_teljes`, `Nave_basokant`, `TIPNR_kivonat`, `adat/elofordulasok` + `motivumok`, `adat/kapcsolatok`, `adat/lxx_dontesek`, `LXX_versszintu_parok`, `LXX_tobblet_szakaszok`, `Verzifikacios_elteres_tabla` (vers) |
| héber szó, igealak | az igealak-kód magyar feloldása a nyers kód mellett | `adat/morf_kulcs_heber.tsv`, `adat/morf_nyelv_aramai.tsv` |
| héber szó-lap | BDB-szócikk másik Strong-szám alatt (alias, jelezve) | `BDB_strong_alias.tsv` |

**Versszám-kulcsok.** A Károli-számozás az MT-t követi (a feliratos zsoltár felirata a 22:1). A BSB MT-számozású (a `Számozás` oszlop értéke a blokkban látszik). A KJV-kulcs és a Nave (KJV-számozású) kulcsa az `LXX_OS` KJV-oszlopából jön, ahol a vers kapott LXX-szót; egyébként a fejezet eltolásával (Zsolt 22:1 → KJV 22:0, a felirat). A `Karoli_versmegfeleltetes.tsv` a Zsolt 22-re Károli = KJV azonosságot ad, ami a KJV-szöveggel ellentmond; a vers-lap jelzi az ellentmondást, a pilot a táblát nem javítja. A TIPNR-sor számozását a vers Strong-számai igazolják (KJV-szám, majd MT-szám).

## A gépi szabályok röviden

- **Fő héber szó**, ha egy Károli-szó több héber szót ad vissza: előbb a `magas` bizonyosságú pár, azon belül a tartalmas szófajú (a `Strong_szotar.tsv` szófaja szerint nem elöljárószó, kötőszó, partikula, névmás, indulatszó). A többi pár a szó-lapon látható.
- **Görög szóalak**: a héber–görög párosítás a Maculából jön, a szóalak az `LXX_OS`-ből (azonos Strong-szám, és a szóalak ékezet nélkül azonos vagy legfeljebb 1 betűben tér el). Ok: a Macula `gorog_lxx` oszlopában a χ és a ξ fel van cserélve (`NYITOTT_FELADATOK.md`).
- **BDB-bontás**: a szócikk saját jelölői (gondolatjel, sorrendhelyes „1, 2 …” és „a, b …”, törzsnevek). Hibás határ előfordulhat; a szöveg nem változik.
- **BDB-alias**: ha egy Strong-számnak sem magyar, sem angol BDB-szócikke nincs, a `BDB_strong_alias.tsv` szerinti másik Strong-szám szócikke áll, a lapon jelezve (Zsolt 22: H0136, H7358).
- **Igealak**: a Macula nyers kódja marad; mellette a magyar feloldás a `morf_kulcs_heber.tsv` pozíció-szabályaival (szófaj, törzs, típus, személy, nem, szám, állapot; az `x` helykitöltő kimarad; a nyelvet a `morf_nyelv_aramai.tsv` adja, hiányzó sor = héber). Ismeretlen jel a kimenetben `[?]`, a mérés számolja (ma 0).
- **Nave**: a hivatkozás-tartomány (pl. `1Móz 1:26-28`) minden olyan versre érvényes, amelynek KJV-kulcsa a tartományba esik; a fejezet-szintű hivatkozás külön, lenyitható sor.

## Ismert korlátok (2026-10-12)

A számok forrása: `naplok/OLVASOI_PILOT_meres.md` (újramérve 2026-10-12, a HEAD állapotán).

- A héber szó-lapok magyar BDB-szócikkel: 1Móz 1–25: 1 075-ből 439 (40,8%), Zsolt 22: 159-ből 112 (70,4%); a többinek az angol eredeti áll, 12 lapnak (1Móz 1–25) egyik BDB-szócikke sincs (a #38 gyakorisági sorrendben halad).
- A Károli–Strong párosítás (`adat/karoli_strong/parok_*.tsv`, 57 könyvfájl) modell-kimenet (#22); a Zsolt 22-ben a párok mind „alacsony” bizonyosságúak (egy modell).
- A görög szó-lapokon magyar jelentés csak a #28 lexikon-szócikkeiből van (1Móz 1–25: 1 230-ból 8, Zsolt 22: 305-ből 3); a többinél az angol TBESG/Thayer áll.
- A BSB-tábla a Zsolt 22:1–2-re nem ad sort (a pilot nem pótolja). A TAHOT-kivonat fejezet-szinten teljes (`eszkozok/tahot_lefedettseg_ellenoriz.py`: nincs hiányzó fejezet).
- A `Karoli_versmegfeleltetes.tsv`, a `LXX_versificacios_terkep.tsv` és a Nave `karoli_allapot` oszlopa a Zsolt 22-re Károli = KJV számozást feltételez (lásd az adatfelmérés 5. pontját; a kerülőút: DT-F60b, `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md`).
- Licenc (`adat/licencek.tsv` szerint): a **TBESH** `tisztazott`, CC BY 4.0 (DT-F33f; az Online Bible-eredetű „Meaning” oszlop fejléc-kérése nem licencfeltétel, a „© Larry Pierce” jelölés megtartandó); az **MCGED** nem kereskedelmi (© Mounce); a **KJV-Strong-címkék** GPL-eredetűek, a `licencek.tsv` sora `tisztazatlan` (DT-F60a, DT-F60c); az `LXX_versszintu_parok` és a `Karoli_versmegfeleltetes` licence tisztázatlan; a tW és az UBS/SDBH CC BY-SA (share-alike). Nyilvános közzététel előtt a `--kiadas` kapcsoló és a DT-M6 szerinti jogi átnézés kell.
- Regressziós alap: a `TestRegresszioProto` a prototípus (`ce4ef98f`) `adat.py`-ját és `bdb_szelet.py`-ját együtt, repón kívüli ideiglenes könyvtárba írja a gitből, onnan lefuttatja (a prototípus saját szeletelőjével), és az 1Móz 1:1–2:3 kimenet minden kulcsának értékét összeveti (a `ts=` és a tesztben indokolt, darabszámmal rögzített engedélyezett-eltérés lista kivételével: `morf_hu` 746, teljes TBESG 38 / Thayer 64, a BDB-szeletelő változása 40 szó-lapon, ebből 8-nál a `szeletel(…, lemma)` argumentum is, a TAHOT-megjegyzés 1). Külön környezeti változó nem kell.

## Kiadás-kapcsoló (DT-F60a, F60.45)

Az `adat.py --kiadas {belso,nyilvanos,kereskedelmi}` (alap: `belso`; a kiadott oldalak a `belso` szerintiek maradnak): `belso` — minden blokk; `nyilvanos` — a KJV-Strong blokk (GPL) kimarad; `kereskedelmi` — a KJV-Strong és az MCGED blokk is kimarad. A kivett blokk adata, statisztikája és proveniencia-sora is kikerül a JSON-ból, a sablon pedig a hiányzó blokkot nem rajzolja. A JSON `kiadas` mezője rögzíti a kiadás típusát. Teszt: `TestKiadas`.

## Beágyazás, db_meres (F60.27–F60.30, #60 v3.2)

- Az `epit.py` alapból **gzip + base64** alakban ágyazza be a JSON-t (`data-kodolas="gzip-base64"`, a sablon `adatBetolt` függvénye bontja ki `DecompressionStream`-mel): az 1Móz 1–25 JSON-ja 35,7 MB, a nyers HTML 35,8 MB (16 MB fölött), a tömörített 11,2 MB (MB = 10^6 bájt). `--nyers`: a tömörítetlen változat (hibakereséshez; ugyanabba a fájlnévbe ír, ezért külön `--kimenet` kell).
- `db_meres.py` (M2b, D1–D5): a `pardes.db`-t méri, csak olvas (`mode=ro`), nem épít újra. A `pardes.db` a `.gitignore`-ban van; külön `git worktree`-ben az alapértelmezett hely a fő munkamásolat `pardes.db`-je. Nincs adatbázis: „nem mérhető”. A D2 a TBESG/Thayer teljes szövegét veti össze (a régi, vágott JSON-t előtag-egyezéssel is kezeli), az alias-mögötti BDB-szócikkeket külön okkal jelzi. A D4 mérete MB = 10^6 bájt (a `SQLITE_EPIT_meres.md` MiB-értékeit átszámolja).
