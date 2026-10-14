# #76 M2b — a szerver és a #60 pilot blokkonkénti összevetése

*Végrehajtói mérés (`claude-sonnet-5-5`), nem független ellenőri. Ág: `claude/olvasoi-konkordancia-m2b`. Az összevetés csak olvas és mér; a pótlás állapotát a 7. szakasz rögzíti.*

`scope=pilot: 1Móz 1:1–2:3 (34 vers; H6440 szó-lap az 1:2-re, G2316 görög lap az 1:1-re, vers-lapok 1:1 és 1:2) és Zsolt 22 (22:2 vers, H0410 szó-lap); szerver: ugyanazok a lapok (/1Moz/1, /1Moz/1/1, /1Moz/1/2, /szo/H6440, /r/szo/H6440, /r/szo/G2316, /r/vers/…, /Zsolt/22/2, /szo/H0410), mindhárom nézetben a vers+szó kontextus | forras=pilot: eszkozok/olvaso_pilot/adat.py + epit.py (kimenet a repón kívül, ideiglenes könyvtár), a lap böngészőben kirajzolva (a beágyazott JS-sablon DOM-szövege), szerver: eszkozok/olvaso_szerver (a branch kódja = origin/main a #343 után), Flask test_client a pardes WSL-disztribúción (Python 3.12.3), a pardes.db epites_ts=2026-10-14T09:35:00Z | ts=2026-10-14`

A pilot a böngészőben rajzolja ki a blokkokat (a kimenete egy beágyazott JSON), ezért az összevetés a kirajzolt DOM-ot (címek, szövegek) és a szerver HTML-jét veti össze, nem csak a JSON-t. A pilot „teljes blokk-készlete” a **kirajzolt** blokkok (a `sablon.html` `rajzolVersBelso`, `rajzolSzoBelso`, `rajzolGorog` függvényei és a `SUGO`-lista), nem a `db_meres.py` `BLOKKOK` listája: az M0 3.4 „39 blokkja” a *mért adatblokkok* listája, és ebből hiányzik több kirajzolt blokk (l. 3. szakasz).

## 1. Az 1–4. pont mérése (a felhasználó észrevételei)

| # | Állítás | Mérés | Ítélet |
|---|---|---|---|
| 1a | A szerveren hiányoznak a Károli-szöveg írásjelei | A `/1Moz/1` Olvasópult/Interlineáris/Munkaasztal szövege a `token_karoli.szo` szavaiból áll, ezek írásjel nélküliek (`Kezdetben teremté Isten az eget és a földet`; a pilotban `… földet.`, `monda Isten: Legyen világosság: és lőn világosság.`). A vers-lap „Károli-szöveg” blokkja a `vers.karoli_szoveg`-ből jön, ott az írásjelek megvannak. | **igazolva** (a fejezet-szöveg; a vers-lap blokk nem érintett) |
| 1b | A pilot folyó szöveg versszámmal, a szerver versenként új sor | Pilot: egy folyamatos szövegtömb, a kis versszámok a szövegben; szerver: minden vers külön `<p class="vers">`. A brief Olvasópult-leírása is „folyamatos Károli-szöveg (a #60 pilot elrendezése)”. | **igazolva**; elrendezési döntés (DT148) |
| 2a | Angol Strong-glossza („face”) a magyar „Alapjelentés: arc, arcok is” helyett | A szerver szó-lap fejléce: `pe.Nei · face` és a Strong-szótár tábla; „Alapjelentés” blokk nincs. A pilot alapjelentése a magyar BDB-szócikk gépi bontásának első sora („arc, arcok is”), ennek híján a Strong-rövid jelentés. | **igazolva** |
| 2b | A BDB angol nyers tömb a pilot magyar, apparátusokra bontott szócikke helyett | **Részben cáfolva:** a szerver *mindkettőt* adja: „BDB-szócikk (angol)” és „BDB-szócikk (magyar fordítás)” (a `forditasok` #38 táblából, modell-kimenet), de a magyar is **egy nyers, bontatlan szövegtömb**; hiányzik a címszó / alapjelentés és szófaj / alakok / jelentésszerkezet bontás és a „Lefordítva · claude-sonnet-5-5, 2026.10.01” sor (a `forditasok.modell`, `.datum` megvan a DB-ben). | **részben igazolva** |
| 2c | Hiányzik az „Ebben a versben” blokk (alak, magyar morfológia, UBS-jelentés, „Károli itt”) | A szerver szó-lapja nem kap vers-kontextust (a `/1Moz/1/2?szo=H6440` lap szó-panelje azonos a `/szo/H6440`-nel); a megfelelő adatok a vers-lap táblázataiban vannak (Macula, magyar feloldás, UBS), de nem a szóhoz kötve, és a „Károli itt: „színén”” nincs. | **igazolva** |
| 3a | A vers részleteiben a héber szöveg szócsempékből áll (héber, átírás, jelentés, Strong, magyar alaktan, alatta LXX görög szó; kattintható) | Szerveren: a TAHOT, Macula, magyar feloldás, héber–görög párosítás **négy külön táblázat**; csempe nincs; az LXX-megfelelő nincs a héber szó alatt. A Strong-számok linkek. | **igazolva** (az adat megvan, a szavankénti egység hiányzik) |
| 3b | A Septuaginta-blokk görög szócsempe Strong-gal (kattintásra görög szó-lap) | Szerveren: „Görög szóalak és LXX-vers szavai (LXX_OS)” táblázat (szóalak, lemma, Strong, morf); a G-Strong linkel a `/szo/G…`-re; csempe nincs. | **részben igazolva** (a link megvan, a forma tábla) |
| 3c | Hiányzik „LXX versszintű együttelőfordulás” | Nincs ilyen blokk a regiszterben; a `lxx_versszintu_parok` tábla a DB-ben megvan (104 518 sor). | **igazolva**; mechanikus pótlás |
| 3d | Hiányzik „LXX többlet és számozási eltérés” | Nincs blokk, és a két forrástábla (`LXX_tobblet_szakaszok`, `Verzifikacios_elteres_tabla`) **nincs a pardes.db-ben** (a `sqlite_epit.py` és a 73 táblás séma nem tartalmazza). | **igazolva**; DB-bővítés kell (DT151) |
| 3e | „Motívumadat” és „Igehely-kapcsolatok” blokk lehet, hogy hiányzik | Nem hiányzik: egyetlen összevont blokk, „LXX-döntés, kapcsolat, motívum (adatréteg)” h4 alcímekkel (Motívum-előfordulások, Igehely-kapcsolatok); az LXX-döntések az összevont blokkban vannak. A pilotban három önálló blokk, saját címmel, jelleg- és forrássorral. | **részben cáfolva** (megvan, összevonva) |
| 4a | Hiányzik a „Hogyan olvasd” útmutató | A kezdőlapon és a fejezet-lapon nincs; a pilotban lenyitható `<details>`. | **igazolva** |
| 4b | Hiányoznak a számláló címkék (pl. „BDB magyarul: 61/98”) | A pilot fejlécében: `34 vers`, `98 héber + 202 görög szó-lap`, `BDB magyarul: 61/98` (arany, ha nem teljes), `Károli–Strong: 57 könyv`; a szerver fejezet-lapján nincs. | **igazolva** |

## 2. Összevetés blokkonként

Jelölés: **megvan** = tartalom és forma azonos; **forma** = a tartalom megvan, a megjelenítés más; **tartalom** = a tartalom eltér vagy részben hiányzik; **hiányzik**. Hacsak nem jelzem külön, a két szakaszon (A: 1Móz 1:1–2:3, B: Zsolt 22) azonos az eredmény. A „pilot” oszlopban a `sablon.html` függvénye áll. A *Mech.* oszlop: a pótlás tartalmi döntés nélkül elvégezhető-e (**i**) vagy döntés kell (**D**).

### 2.1 Oldal- és fejléc-szint

| P | Pilot-elem | Szerver | Állapot | Mech. |
|---|---|---|---|---|
| P1 | Számláló címkék (`cimkek`) | nincs | hiányzik | i |
| P2 | „Hogyan olvasd ezt az oldalt?” (`utmutato`) | nincs | hiányzik | i |
| P3 | Folyó Károli-szöveg, írásjelekkel, kis versszámokkal | versenként külön sor, írásjel nélkül | tartalom (írásjel) + forma (folyó) | írásjel: i; folyó/soronként: D |
| P4 | „Kapcsolt szavak jelölése” kapcsoló (aláhúzás ki/be) | nincs kapcsoló, az aláhúzás mindig látszik | forma | D (kicsi; az UI része) |
| P5 | Téma-váltó (Rendszer / Világos / Sötét) | nincs | hiányzik | D (kicsi; UI) |
| P6 | Szó-/vers-fül a jobb panelben, kattintásra helyben nyílik | linkre kattintás, oldalbetöltés (`?szo=`, `?ful=`) és `/r/…` töredék | forma (a szerveroldali elv) | — (a brief szerinti szerveroldali lap) |
| P7 | Kereszthivatkozás-gomb, Bezárás gomb | nincs | forma | — |

### 2.2 Vers-panel („Vers részletei”)

| # | Pilot-blokk | Szerver-blokk | Állapot | Mech. |
|---|---|---|---|---|
| V1 | Versszámozás (Károli, héber MT, LXX, KJV, KJV-kulcs + „a számozás egyezik”) | „Versszámozás (MT / KJV)” + „LXX-versszám” két táblázat | forma | — |
| V2 | Károli-szöveg (forrásadat + modell-kimenet) | „Károli-szöveg” + „Károli–Strong párosítás” táblázat | megvan (tartalom azonos; a pilot egy blokkban, két jelleg-címkével) | — |
| V3 | **Héber szöveg**: szócsempék jobbról balra: héber, átírás, angol tükör, Strong, magyar alaktan, alatta az LXX-görög szó („LXX: —” ha nincs); szaggatott keret a nyelvtani elemre | „Eredeti szavak (TAHOT/TAGNT)”, „Igealak-kód és szófaj (Macula)”, „Héber–görög párosítás szavanként”, „Az igealak magyar feloldása”: négy táblázat | forma (a tartalom megvan, de nem szavankénti egység; nem kattintható csempe) | i (csak megjelenítés) |
| V4 | **Septuaginta (LXX, Rahlfs)**: görög szócsempék, alattuk Strong; keretes+aláhúzott = szó-lappal, arany = nincs ÚSZ-Strong | „Görög szóalak és LXX-vers szavai” táblázat (lemma, morf is), G-Strong link | forma | i |
| V5 | Kereszthivatkozások (TSK, 68 db; a legtöbb szavazatot kapott 6) | „Kereszthivatkozások (TSK)”: az első 15 + szavazat, „Összesen 68” | tartalom (a szerver 15-öt és szavazatot ad, a pilot 6-ot, vessző-formában „Ján 1,1”; a szerver a CLAUDE.md formáját `Ján 1:1` használja) | — (a szerver a bővebb; nem pótlás) |
| V6 | Károli-kereszthivatkozások | „Károli-kereszthivatkozások” | megvan (formátum: pilot „Zsid 11,3”, `Csel 14,15`; szerver `ApCsel 14:15`) | — |
| V7 | Angol szó szavanként (BSB): csempék, Strong, kattintható | táblázat (#, angol szó, Strong, morf) | forma | i |
| V8 | Angol szó szavanként (KJV) | táblázat; kiadási kizárás | forma | i |
| V9 | Témák (Nave) + „Fejezet-szintű hivatkozások (2)” lenyitva | „Témák (Nave, versekre bontva)”; a **fejezet-szintű hivatkozások nincsenek** | tartalom (a `nave_basokant` `hely_tipus='fejezet'` sorai, 2 212 a DB-ben, a szerver nem olvassa) | i |
| V10 | Tulajdonnevek (TIPNR) | „Tulajdonnevek (TIPNR)” | megvan | — |
| V11 | Motívumadat (adatréteg) – „Nincs sor erre a vershez: …” | az összevont „LXX-döntés, kapcsolat, motívum” blokk üres szöveggel | forma (összevonva; a három saját cím és jelleg-/forrássor egy blokkba került) | i (szétválasztás) |
| V12 | Igehely-kapcsolatok (adatréteg) | ugyanaz az összevont blokk, h4 alcím | forma | i |
| V13 | LXX-fordítói döntések (adatréteg) | ugyanaz az összevont blokk | forma | i |
| V14 | **LXX versszintű együttelőfordulás** („1 héber szó, 5 pár”) | nincs | hiányzik | i (`lxx_versszintu_parok` megvan) |
| V15 | **LXX többlet és számozási eltérés** (+ „A Verzifikacios_elteres_tabla nem ad sort”) | nincs | hiányzik | **D** (a két forrástábla nincs a DB-ben) |
| V16 | (a pilotban nincs) | „UBS-jelentés az előfordulásra”, „Igealak-kód és szófaj”, „Az igealak magyar feloldása” | a szerveren az „Ebben a versben” adatai itt állnak, szóhoz nem kötve | — |

Szakaszkülönbség (B): a BSB-tábla a Zsolt 22:1–2-re nem ad sort (mindkét oldalon üres; a pilot ezt jelzi, a szerver „Nincs adat”-ot). A V1 sor a Zsolt 22:1-et feliratként kezeli mindkét oldalon (a pilot külön jelzi az ellentmondás-esetet; a Zsolt 22-n a `tabla_ellentmond` hamis, mindkettő azonos).

### 2.3 Héber szó-lap (A: H6440, B: H0410)

| # | Pilot-blokk | Szerver-blokk | Állapot | Mech. |
|---|---|---|---|---|
| H1 | **Szó adatai (héber)**: szótő, átírás · szófaj, **Alapjelentés** (magyar: „arc, arcok is”, „isten”), 3 számláló (2127 előfordulás, 38 könyv, 2177 Károli-pár (267 magas)) | „Strong-szótár” táblázat (szótő, kiejtés, szófaj, **angol** rövid jelentés „face”, gyök) + „Előfordulás, könyvek száma” (2127, 38) + „Károli-alakok” (2177, 267) | tartalom: a számok **azonosak**; a magyar **alapjelentés hiányzik**, helyette az angol Strong-glossza | **D** (az alapjelentés a magyar BDB-bontásból jön) |
| H2 | **Ebben a versben (1Móz 1:2)**: „Károli itt: „színén””, alak + átírás + szófaj + Macula-kód magyarul, UBS-jelentés vagy „nem ad besorolást”, „Görögül ebben a versben (LXX): ὁ · G3588” | nincs (a szó-lap nem kap vers-kontextust) | hiányzik | i |
| H3 | Így fordítja Károli (előtt 549, elé 107 …; „57 feldolgozott könyv” felsorolás) | „Károli-alakok és bizonyosság” (azonos lista és darabszám); az „57 feldolgozott könyv” jelzés nincs | megvan (a könyvlista-jelzés hiányzik; kicsi) | i (jelzés) |
| H4 | **BDB-szócikk apparátusokra bontva (magyarul)**: „Lefordítva · claude-sonnet-5-5, 2026.10.01”, gépi szeletelés jelzése, Címszó / Alapjelentés és szófaj / (Nyelvi háttér) / Alakok / Jelentésszerkezet (lenyitható, „49 hely”) / Irodalmi és szövegkritikai jelek | „BDB-szócikk (angol)” nyersen + „BDB-szócikk (magyar fordítás)” nyersen, egy tömbben, a fordítás-jelölés nélkül | tartalom + forma (a szöveg megvan, bontás és fordítás-jelölés nincs) | **D** (N-F76d (1): a bontás átvétele, és a #38 adat vs a pilot gépi bontása) |
| H5 | Görög megfelelő a Septuagintában (πρόσωπον G4383 923×…) | „Görög megfelelő (lxx_bridge)” táblázat (azonos számok) | megvan (forma: tábla) | — |
| H6 | Szemantikai domén (SDBH): „nem ad domént” | „Szemantikai domén (SDBH)”: üres | megvan | — |
| H7 | SECE-szócikk (héber) | „SECE-szócikk (héber)” | megvan | — |
| H8 | TWOT- és BDB-azonosító (OSHL) | „OSHL: TWOT- és BDB-azonosító, BDB-helyek” | megvan | — |
| H9 | Bővített Strong-szócikk (TBESH) | „Bővített Strong-szócikk (TBESH)” | megvan | — |
| H10 | translationWords (tW), lenyitható cikkek | „translationWords” h4 cikkcímekkel | megvan | — |
| H11 | (a pilotban nincs) | „Nyelvtani Strong-számok szűrése” | a szerveren többlet | — |

### 2.4 Görög szó-lap (A: G2316)

| # | Pilot-blokk | Szerver-blokk | Állapot | Mech. |
|---|---|---|---|---|
| G1 | **Szó adatai (görög)**: lemma, átírás · szófaj, Alapjelentés „God”, 3 számláló (1346 előfordulás az ÚSZ-ben, 1173 versben, 5 héber szó mögötte) | fejléc `theos · God`; a számok az „ÚSZ-előfordulás és versek” (1346, 1173) és a „Héber háttér” táblában | tartalom megvan, forma szétszórt; a szófaj és a „5 héber szó” számláló nincs | i |
| G2 | Jelentés: „Magyar fordítás nincs · az angol eredeti áll”, Rövid jelentés | „Magyar jelentés (Thayer, UBS DNTG)”: „Nincs adat (üres eredmény, nem negatív lelet)” | megvan (üres) | — |
| G3 | Héber háttér (5 szó: אֱלֹהִים 2153× …) | „Héber háttér (lxx_bridge)” (10 sor; a pilot az első 5-öt mutatja) | megvan | — |
| G4 | Az Újszövetségben (Károli; az első 5 a 1173 versből): vers + Károli-szöveg + UBS DNTG-besorolás soronként + a Károli–Strong párosítású könyvek jelzése | „ÚSZ-előfordulás és versek”: 5 vers + Károli-szöveg; az UBS DNTG-besorolás külön, „UBS DNTG jelentés / Előfordulások (az első 40)” alatt | forma (a soronkénti UBS-besorolás külön blokkban) | — |
| G5 | Szótári szöveg (angol): TBESG + Thayer (lenyitva) | „TBESG” + „Thayer (angol)” | megvan | — |
| G6 | Szemantikai domén (SDGNT) | „Szemantikai domén (SDGNT)”: a blokkcím mellett fixen „üres eredmény nem negatív lelet” megjegyzés akkor is, ha a blokk tartalmas | tartalom megvan; a jelleg-megjegyzés félrevezető | i (kicsi) |
| G7 | UBS DNTG jelentések (angol) | „UBS DNTG jelentés” | megvan | — |
| G8 | LSJ | „LSJ” | megvan | — |
| G9 | Mounce (MCGED) | „MCGED (Mounce)” | megvan | — |
| G10 | SECE-szócikk (görög) | „SECE-szócikk (görög)” | megvan | — |
| G11 | translationWords | „translationWords” | megvan | — |

## 3. A „39 blokk” és a kirajzolt blokkok eltérése (ok)

Az M0 3.4 táblázata a `db_meres.py` `BLOKKOK` listájából készült (adatblokkok: táblák és D2-összehasonlítók). A pilot **kirajzolt** blokkjai között olyanok vannak, amelyeknek ott nincs külön sora, vagy amelyeket a regiszter eltérően csoportosít:

| Kirajzolt pilot-blokk | M0 3.4 / regiszter |
|---|---|
| Héber szöveg (szócsempék), Septuaginta (szócsempék) | az adatuk a 3–6. blokk (táblázat-nézet); a csempe-összeállítás nincs |
| Ebben a versben | nincs sor (a 4., 5., 12., 16. blokk adata, de szóhoz kötve nem) |
| Szó adatai: Alapjelentés | nincs sor (a 17. blokk angol rövid jelentése áll helyette) |
| BDB apparátusokra bontva | nincs sor (a 21. blokk nyers magyar szövege) |
| LXX versszintű együttelőfordulás | nincs sor |
| LXX többlet és számozási eltérés | nincs sor |
| Motívumadat / Igehely-kapcsolatok / LXX-fordítói döntések | a 13. blokkban összevonva |
| Fejezet-szintű Nave | a 10. blokk csak `nave_vers`-t olvas |

A brief „a #60 pilot teljes blokk-készlete (39 blokk)” szöveg tehát a *mért adatblokkokra* teljesült (a D2-egyezés, a jelleg- és forrássor), a *kirajzolt készletre* nem.

## 4. Összegzés

| Állapot | Sor |
|---|---|
| megvan (azonos tartalom, azonos vagy nem lényegesen eltérő forma) | V2, V6, V10, H3, H5–H10, G2, G3, G5, G7–G11 |
| forma eltér (tartalom megvan) | V1, V3, V4, V7, V8, V11–V13, G4, P6, P7 |
| tartalom eltér vagy részben hiányzik | V5 (a szerver bővebb), V9 (fejezet-szintű Nave), H1 (magyar alapjelentés), H4 (BDB-bontás), G1, G6, P3 (írásjel) |
| hiányzik | V14, V15, H2, P1, P2, P4, P5 |

## 5. Mi mechanikus és mi igényel döntést

- **Mechanikus (pótolható döntés nélkül):** írásjelek a fejezet-szövegben (P3, a `vers.karoli_szoveg`-ből); „Hogyan olvasd” és számláló címkék (P1, P2); héber szócsempe-blokk és Septuaginta-csempe blokk (V3, V4); BSB/KJV csempék (V7, V8); „Ebben a versben” a szó-lapon (H2); LXX versszintű együttelőfordulás (V14); fejezet-szintű Nave (V9); Motívum/Kapcsolat/LXX-döntés szétválasztása három blokkra (V11–V13); „57 feldolgozott könyv” jelzés (H3); SDGNT jelleg-megjegyzés (G6); görög szó-lap számlálói (G1).
- **Tartalmi döntés (DT148…):** folyó szöveg vs soronkénti elrendezés (P3, DT148); a magyar alapjelentés és az angol Strong-glossza sorsa, a magyar BDB-szócikk bontása és forrása (H1, H4; DT149, DT150; N-F76d (1)); az LXX többlet és számozási eltérés blokk (V15: a két forrástábla a DB-be, vagy a blokk kimarad; DT151); a pilot UI-elemei (P4, P5: aláhúzás-kapcsoló, téma-váltó; DT152).

## 6. Mérési korlátok

- A pilot oldala a böngészőben, a beágyazott JS-sablon kirajzolt DOM-szövegéből lett összevetve; a H6440 / H0410 / G2316 lap és a vers-lapok a példák, nem az összes lap. A H6440 és H0410 lapokra a blokkok jelenléte és a számok ellenőrzöttek; a pilot és a szerver D2-egyezése (21 991 és 3 022 összevetés) az M2 naplójában áll, ez a dokumentum a *kirajzolt* készletet méri.
- A szerver a `pardes.db`-t kizárólag olvasta; nincs adatírás, nincs új adat.

## 7. A pótlás állapota

**Pótolva (F76.25–F76.26, döntés nélküli tételek), a pilot aranymintájával szemben tesztelve:**

| Sor | Mi készült | Hol |
|---|---|---|
| P3 (írásjel) | a fejezet-szöveg a `token_karoli` szavaiból és a `vers.karoli_szoveg` írásjeleiből (`szovegbe_igazit`; a kötőjeles összetétel szóköz nélkül) mindhárom nézetben | `lekerdezesek.py`, `oldalak.py`, `fejezet.html` |
| P1, P2 | fejléc-számlálók (n vers, x héber + y görög szó-lap, BDB magyarul a/x arannyal, Károli–Strong k könyv) és a „Hogyan olvasd” útmutató | `oldalak.szamlalok`, `fejezet.html` |
| V3, V4 | „Héber szöveg” szócsempe-blokk (héber, átírás, angol tükör, Strong, magyar alaktan, alatta az LXX-megfelelő; nyelvtani elem szaggatott kerettel) és „Septuaginta” csempe-blokk (görög szó + Strong, kattintható), a vers mellett nyíló szó-lappal | `blokkok.py` (`_heber_csempek` a pilot párosításával) |
| V7, V8 | BSB és KJV szavankénti csempék | `blokkok._r_angol` |
| V9 | fejezet-szintű Nave (a `nave_basokant` `hely_tipus='fejezet'` soraiból) | `q.nave_fejezet` |
| V11–V13 | a motívum, kapcsolat és LXX-döntés blokk három önálló blokk, saját címmel, jelleg- és forrássorral | `blokkok.py` |
| V14 | LXX versszintű együttelőfordulás | `q.lxx_versszintu` |
| H2 | „Ebben a versben” a héber szó-lapon (Károli itt, alak és magyar alaktan, LXX-párja, UBS-besorolás), csak vers-kontextussal | `szo.ebben` (`vers_kell`) |
| H3 | a „57 feldolgozott könyv” jelzés a Károli-alakok blokkban | `blokkok._r_karoli_alakok` |

Blokkszám: 46 azonosító (az M2 40-e + 6). A szócsempe-blokkok mellett a táblázatos blokkok megmaradtak (a tartalom azonos, a táblázat részletesebb); eltávolításuk elrendezési döntés lehetne.

**(Az F76.25 idején még nem pótolva; a döntések után az F76.30 pótolta, l. lent) Döntésre várt, a teszt `expectedFailure` volt:** P3 folyó szöveg (DT148), H1 magyar alapjelentés (DT149), H4 bontott magyar BDB (DT150), V15 LXX többlet és számozási eltérés (DT151), P4/P5 aláhúzás-kapcsoló és témaváltó (DT152). **Nem pótolva, nem döntésköteles, kis tétel:** G1 (a görög szó-lap „szó adatai” számlálói: szófaj, „5 héber szó mögötte”), V5/V6 (TSK-szám és formátum), G6 (SDGNT megjegyzés): N-F76h.

**Tesztfutás, végrehajtói futás, nem független ellenőri:** `scope=eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py (19 teszt: 14 zöld, 5 expectedFailure) és teszt_olvaso_szerver.py (62 teszt, ezek között a pilot D2-egyezése mindkét szakaszon, az egyetlen dokumentált eltérés a DT147 „+” Strong-lánc) | forras=unittest, Python 3.12.3, pardes WSL-disztribúció, parancs: wsl -d pardes -- env PARDES_DB=/home/basesoft/pardes/pardes.db PARDES_PILOT_JSON=<pilot JSON-ok: 1moz_1_1_2_3, zsolt_22, 1moz_1_25> <venv>/bin/python -W error::ResourceWarning <fájl> (a Windows-munkafán, /mnt/c), a pardes.db epites_ts=2026-10-14T09:35:00Z | ts=2026-10-14`. Eredmény: **OK** mindkét fájlra (65,8 s és 4,7 s).

*Megjegyzés a futó szerverhez:* a felhasználó 8765-ös portján futó szerver az M2 kódjával indult (a Flask fejlesztői szerver nem tölti újra a kódot, és a lapokat gyorsítótárazza); az M2b változásai újraindítás után látszanak.

**A döntések kódja (F76.30–F76.31; DT148–i, felhasználó, 2026-10-14):**

| Döntés | Mi készült | Teszt |
|---|---|---|
| e (c) | az Olvasópult egyetlen folyó bekezdés kis versszámokkal; az Interlineáris és a Munkaasztal versenként | `test_DT_F76e_…` |
| f (a) | a szó-lap fejlécében magyar „Alapjelentés” (`bdb_szelet.alap_jelentes`), híján az angol Strong-glossza; az angol glossza a Strong-szótár blokkban marad | `test_DT_F76f_…` (minden pilot-lapra) |
| g (b) | `szo.bdb_apparatus` blokk: a szerver a pilot `bdb_szelet.py`-ját hívja (importlib, kódmásolás nélkül, a pilot könyvtára nem kerül a `sys.path`-ra), jelleg: forrásadat + modell-kimenet + gépi feldolgozás, „hibás határ előfordulhat” jelzés, „Lefordítva · modell, dátum” (`forditasok`), minden szöveg escape-elve | `test_DT_F76g_…` (bontás szócikkenként egyezik a pilot `appar`-jával, 1Móz 1:1–2:3 és Zsolt 22 összes héber lapján) |
| h (c) | `vers.lxx_tobblet` blokk „Az adat még nincs a DB-ben” jelzéssel (N-F76j); a forrássor a két TSV-t nevezi | `test_DT_F76h_…` |
| i (a) | „Kapcsolt szavak jelölése” kapcsoló és Rendszer/Világos/Sötét témaváltó (localStorage, süti nélkül; CSP-barát) | `test_DT_F76i_…` |
| 3. pont | az Interlineáris nézet szavai csempék: magyar szó, alatta az eredeti, átírás, angol tükörfordítás, Strong (a pilot héber-csempe tartalma, a `token_eredeti`-ból az `er_sorszam` szerint); kattintásra a szó-lap; nyelvtani elem link nélkül | `test_interlinearis_csempek_…` |
| 4. pont | az ETag és a gyorsítótár kulcsa tartalmazza a kód/sablon/statikus/konfig és a pilot `bdb_szelet.py` hash-ét (`oldalak.kod_verzio`, induláskor; `/statusz` is mutatja) | `test_etag_es_gyorsitotar_kulcsa_…`, `test_kod_verzio_valtozik_…` |

Az Interlineáris csempe tartalmánál az „angol tükörfordítás” (a pilot csempéjének `gl` mezője) áll a „rövid jelentés” helyett: a pilot mintáját követtem; ha a TAHOT rövid jelentése kell, egyetlen mező cseréje.

**Tesztfutás, végrehajtói futás, nem független ellenőri (F76.30):** `scope=eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py (22 teszt, mind zöld, expectedFailure már nincs) és teszt_olvaso_szerver.py (65 teszt, köztük a D2-egyezés, az egyetlen eltérés a DT147) | forras=unittest, Python 3.12.3, pardes WSL-disztribúció, ugyanaz a parancs mint fent, a pardes.db epites_ts=2026-10-14T09:35:00Z | ts=2026-10-14`. Eredmény: **OK** mindkét fájlra (72 s és 9 s). A regiszter 48 azonosítós.
