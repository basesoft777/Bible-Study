# Olvasói pilot (nem éles)

Az olvasói nézet első, belső próbája (2026-10-05): egy szakasz folyamatos Károli-szövege, kattintható szavakkal, jobb oldalon a héber és görög szó-lapokkal és a versrészletekkel. Ma két szakaszon fut: 1Mózes 1:1–2:3 és Zsoltárok 22. A továbbfejlesztés és az értékelés a **#60 OLVASOI_PILOT** feladat (`F60_OLVASOI_PILOT_BRIEF.md`; a v2 bővítés: a repó minden használható, már meglévő adata a lapon, és a pilot datasetjének felmérése).

## Futtatás

```bash
python eszkozok/olvaso_pilot/adat.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/epit.py --szakasz "1Móz 1:1-2:3"
python eszkozok/olvaso_pilot/adat.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/epit.py --szakasz "Zsolt 22"
python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py
python eszkozok/olvaso_pilot/meres.py        # naplok/OLVASOI_PILOT_meres.md (újrafuttatja az adat.py-t és az epit.py-t)
python eszkozok/olvaso_pilot/felmeres.py     # naplok/OLVASOI_PILOT_adatfelmeres.md (az adat.py-t újrafuttatja)
```

A `--szakasz` vers-tartomány (`"1Móz 1:1-2:3"`) vagy egész fejezet (`"Zsolt 22"`); a versek a `Karoli_1908.tsv`-ből jönnek, a könyvfájlok a `szakasz.py` `KONYVFAJLOK` táblájából (ma: 1Móz, Zsolt; más könyvre a pilot hibával áll meg). Az `adat.py` és az `epit.py` a `--kimenet KÖNYVTÁR` könyvtárba ír, alapból a repón kívüli `<temp>/olvaso_pilot/<szakasz-azonosító>/` könyvtárba. A kimenet (`olvaso_pilot.json`, `karoli_konkordancia_proba.html`) nem kerül a repóba. A `ts=` mező a futás UTC ideje. Böngészős próba: `python -m http.server <szabad port>` a kimeneti könyvtárból, a végén a folyamat leállítandó.

Az oldal egyetlen önálló HTML (minden adat beágyazva; ma 3,7 és 4,8 MB, a 8 MB-os határ alatt, ezért nincs lusta betöltés; a határ átlépésekor a nagy szövegeket — SECE, LSJ, tW, TBESH, BDB teljes szöveg — külön JSON-ba kellene tenni).

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
| `teszt_olvaso_pilot.py` | tesztek: szakasz, fő szó, görög szóalak, BDB-bontás, bővítés, proveniencia, „csak adat” ellenőrzés, a Szó / Vers részletei fülváltás (statikus: a `[hidden]` CSS-szabály megvan), maszkolt regresszió |

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

## Ismert korlátok (2026-10-07, a `naplok/OLVASOI_PILOT_meres.md` szerint)

- A héber szó-lapok magyar BDB-szócikkel: 1Móz 98-ból 61 (62,2%), Zsolt 159-ből 112 (70,4%); a többinek az angol eredeti áll (a #38 gyakorisági sorrendben halad).
- A Károli–Strong párosítás csak 1–5Móz, Józsué és Zsoltárok könyvére kész; az Újszövetségre nincs. A Zsoltárokban a párok mind „alacsony” bizonyosságúak (egy modell, #22).
- A görög szó-lapokon magyar jelentés csak a #28 lexikon-szócikkeiből van (1Móz 202-ből 4, Zsolt 304-ből 3; a görög szó-lapok köre a lxx_bridge-ből hivatkozott szavakkal bővült, F60.15).
- A BSB-tábla a Zsolt 22:1–2-re nem ad sort (a pilot nem pótolja); a TAHOT-kivonat nem teljes (a két szakaszt nem érinti).
- A `Karoli_versmegfeleltetes.tsv`, a `LXX_versificacios_terkep.tsv` és a Nave `karoli_allapot` oszlopa a Zsolt 22-re Károli = KJV számozást feltételez (lásd az adatfelmérés 5. pontját).
- A TBESH jelentés-listája Online Bible-eredetű (a fejléc szerint külön engedély kell); az MCGED nem kereskedelmi; a KJV-Strong-címkék, az LXX_versszintu_parok és a Karoli_versmegfeleltetes licence tisztázatlan; a tW és az UBS/SDBH CC BY-SA (share-alike). Nyilvános közzététel előtt jogi átnézés kell (DT-M6).
- Regressziós alap a bővítés előtti állapothoz: `git worktree add <könyvtár> 98b5098`, ott `adat.py --szakasz "1Móz 1:1-2:3" --kimenet <ideiglenes>`, majd `OLVASO_PROTOTIP_JSON=<az olvaso_pilot.json útvonala>` a tesztfuttatáskor; a bővítés csak új mezőket adhat, a `morf_hu` kivételével (a feloldás korábban üres volt).
