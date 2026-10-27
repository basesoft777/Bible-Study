# `adat/` — séma

**Verzió:** v1 — 2026.09.13
**Forrás:** `ATALAKITASI_TERV.md.md` 1.A pont (tábla-lista), 4.2 (proveniencia), 4.5 (gerinc-elem), 4.6 (gate-mezők), 4.7 (Károli-join)
**Fázis:** F1.2

Ez a réteg a **kanonikus igazságforrás**. A `tematikus_lezart/`, `genezis/`, `motivumlog/`
és `lexikon/` kimenetei ebből generálódnak vagy ehhez igazodnak. Ha egy tény itt és egy
markdown-fájlban ellentmond, **ez a tábla az irányadó**. Az adat egy irányba mozog (3/9,
DT28): a kézi forrásból ide kinyerés van (`jeloltek.tsv`), innen a kimenetbe generálás;
forrásba visszaírás nincs.

A kilenc tábla (és a modell-kimenetű `karoli_strong/` táblapár, 2.20, valamint a belőle származtatott `karoli_variancia.tsv`, 2.24) és a hozzájuk tartozó kulcs:

| Fájl | Kulcs | Ki írja |
|---|---|---|
| `motivumok.tsv` | `id` | `betolt.py` / kézzel, validálva |
| `elofordulasok.tsv` | `id` + `igehely` | `betolt.py`, jelöltből előléptetve |
| `kapcsolatok.tsv` | `forras_igehely` + `cel_igehely` + `id` | `betolt.py` / kézzel |
| `jeloltek.tsv` | `id` + `igehely` | `lekerdez.py` írja, ember minősíti |
| `lexikon_hivatkozasok.tsv` | `strong` + `entry_id` + `jelentes_szam` | `betolt.py` |
| `datasetek.tsv` | `study_tipus` + `dataset` | kézzel (policy-tábla) |
| `grammatikai_strongok.tsv` | `strong` | **generált** — `eszkozok/grammatikai_strongok_general.py` |
| `auditok.tsv` | nincs (l. 2.9) | a `lekerdez.py` proveniencia-sora; `--naplo ID --lepes KÓD` esetén maga a lekérdező fűzi hozzá (l. 2.9) |
| `licencek.tsv` | `dataset` | kézzel (leltár, F24) |
| `dontes_hatas.tsv` | `dontes_forras` + `erintett_fajl` + `tilos_minta` | kézzel (F51, 2.21) |
| `karoli_strong/parok_<könyv>.tsv`, `karoli_strong/szavak_<könyv>.tsv` | `vers` + `hu_sorszam` + `er_sorszam` / `vers` + `oldal` + `sorszam` | **generált** (modell-kimenet, javaslat) — `eszkozok/karoli_strong/egyesit.py` (2.20, F22) |
| `karoli_variancia.tsv` | `tipus` + `konyv` + `kulcs` + `ertek` + `bizonyossag` (+ `id` + `igehely` a `megerosites` sornál) | **generált** — `eszkozok/karoli_ellenorzes.py --variancia` (2.24, F65) |
| `karoli_strong/nem_tr_parositott.tsv` | `vers` + `er_sorszam` | **generált** — `eszkozok/karoli_strong/nem_tr_lista.py` (2.20, F22 D45) |

---

## 1. Közös típusok

Ezek minden táblára érvényesek. Egy mező típusa a 2. szakaszban erre hivatkozik.

### 1.1 `IGEHELY` — a legfontosabb közös típus

**Kanonikus alak: magyar rövidítés + szóköz + fejezet + kettőspont + vers.**

```
1Móz 3:16      Mt 24:38      Zsolt 110:4      1Krón 4:40
```

Ez **döntés, nem megfigyelés** — a repóban ma két formátum él egymás mellett:

| Alak | Hol | Példa |
|---|---|---|
| **magyar kanonikus** (ez a séma alakja) | `TAHOT_kivonat.tsv`, `TAGNT_kivonat.tsv`, `TSK_kereszthivatkozasok.tsv`, `Karoli_1908.tsv`, `LXX_OS/*.tsv` (`igehely_karoli` oszlop) | `1Móz 1:1` |
| STEPBible-pontozott | `Karoli_kereszthivatkozasok.tsv`, `Karoli_Strong_kivonat.tsv`, `TIPNR_kivonat.tsv` | `Gen.1.1` |

Az `adat/` réteg **kizárólag a magyar kanonikus alakot** használja. Indok: a `lekerdez.py`
öt determinisztikus lépése (gerinc, scan, kollokáció, igealak, LXX-híd) mind olyan
datasetet olvas, amely már ebben az alakban áll, és a tanulmányok szövege is ezt írja.
A másik három dataset felé a `konkordancia/Konyv_normalizalo_tabla.tsv` (66 könyv,
STEPBible-rövidítés ↔ magyar rövidítés ↔ teljes név) oda-vissza konvertál.

*Következmény, amit az F2-nek kezelnie kell:* a `karoli` és a `tsk` parancs bemenete és
kimenete között normalizálási lépés áll. Ez nem opcionális kényelmi funkció — normalizálás
nélkül a `Karoli_kereszthivatkozasok.tsv` és a `TAHOT_kivonat.tsv` **néma nem-találatot** ad
ugyanarra a versre.

**Vers-tartomány** kötőjellel, a második tagon könyvnév nélkül, ha azonos: `1Móz 6:1-8`.
Fejezeten átnyúló tartomány mindkét tagot kiírja: `1Móz 4:25-5:32`.

### 1.2 `STRONG`

`H` vagy `G` + **négy számjegy, balról nullázva**: `H0779`, `H8415`, `G0086`.
A nullázás kötelező — `H779` nem érvényes érték, mert a datasetek rendezése így rendezi.
Több Strong-szám egy cellában: `+` jellel, sorrendben (`G0934+G2406`).
G-kiegészítő kód: `G` + öt számjegy, nem nullával kezdődik (TAGNT, pl. `G20447`).

**A TIPNR betűutótagja (F88, DT111).** A `TIPNR_kivonat.tsv` a Strong-számhoz egyértelműsítő
betűt fűz: a **nagybetű** (`G2424G` Jézus, `G2424H` Barabbás, `H3063G` Júda, `H3063N` Júdea)
személyt/entitást különböztet meg egy lexémán belül, nem jelentésváltozatot; a **kisbetű**
(`H5838z`) ugyanígy utótag. Ez nem SEMA 1.2 alak, a `strong_util.strong_normalizal()` hibaként
elutasítja (alapérték: `utotag='tilt'`). A `pardes.db` TIPNR-betöltője kifejezett szabállyal
(`sqlite_epit.tipnr_strong_szetvalaszt`) levágja: a `tipnr.strong` az **alapszámot** (SEMA 1.2
alak) hordozza, így a `token_strong` kulcsán illeszkedik; az utótag a `tipnr.utotag`
oszlopba kerül (utótag nélküli soron üres); a teljes eredeti érték a `tipnr.strong_nyers`-ben
marad. Amit a levágás után sem lehet normalizálni, a `normalizalas_jelentes`-be kerül.

### 1.3 `DATUM`

`ÉÉÉÉ.HH.NN` (`2026.09.13`). Relatív dátum (*„tegnap", „a múlt héten"*) nem írható be.

### 1.4 `PARDES_SZINT`

Zárt értékkészlet: `Pshat` | `Remez` | `Drash` | `Sod`.
Több szint egy cellában `/` jellel (`Remez/Drash`). Üres, ha a sor nem PaRDeS-besorolt.

### 1.5 `PROVENIENCIA` — a terv 4.2 pontja

A `lekerdez.py` minden futása kiírja a saját provenienciáját, és **az a sor kerül a mezőbe,
szó szerint**, szerkesztés nélkül:

```
scope=OT-full | forras=TAHOT_kivonat.tsv | strong=H6093 | n=3 | ts=2026-09-11T14:22Z
```

Kötelező kulcsok: `scope`, `forras`, `ts`. A `scope` megengedett értékei:
`OT-full` | `NT-full` | `OT+NT-full` | `LXX-39` | `range:<igehely-tartomány>` | `manual`.

**A `manual` érték jelentése:** az állítás nem lekérdezésből származik. Ez nem tiltott, de
**greppelhető**, és a Minőségi kapu értelmezésként, nem ténymegállapításként kezeli.
Üres proveniencia-mező ugyanezt jelenti, csak jelöletlenül — ezért a `manual` a helyes
kitöltés, nem az üresen hagyás.

*Miért ez a terv legfontosabb egyetlen eleme:* két dokumentált incidens ugyanabból a
hibaosztályból származott — egy „🔍 STEPBible-ellenőrizve" sor lekérdezés nélkül, és egy
Gen 1-11-re szűkített scan „teljes"-nek címkézve. Fegyelmi szabály ezt nem oldja meg;
az a mező igen, amelyet nem az ember tölt ki.

### 1.6 `MEGBIZHATOSAG`

Zárt: `magas` | `közepes` | `alacsony`.
*Mért kiindulás (2026.09.13):* a `Karoli_Strong_kivonat.tsv` 227 sorából 222 `magas`, 5 `közepes`.

### 1.7 `AZONOSITAS_MODJA`

Zárt: `tartalom-alapú` | `szó-szintű-gépi` | `szó-szintű-tagged` | `interlineáris-gloss` | `kikövetkeztetett`.

- `tartalom-alapú` — a tanulmány írója a Károli-szöveget olvasva rendelte a szót a Strong-számhoz.
- `szó-szintű-gépi` (DT-M2, F65) — a #22 gépi Károli–Strong párosításából (`adat/karoli_strong/parok_<könyv>.tsv`) megerősített sor. **Csak `magas` bizonyosságú pár igazolhatja**, és csak ha a sor minden Strongja szerepel a `karoli_szo` szavainak gépi párjai között ugyanazon a versen; a sor saját proveniencia-sora az `adat/karoli_variancia.tsv` `megerosites` sorában áll (2.24). A gépi párosítás modell-kimenet: a mód a *azonosítás módját* mondja, nem „ellenőrizve” minősítést.
- `szó-szintű-tagged` — esetleges kiadói, kézzel taggelt Károli-szövegnek fenntartva; ma nincs ilyen forrás.

*Mért kiindulás:* a 2026.09.13-i 227 join-sor mind `tartalom-alapú` volt. A #22 szó-szintű, gépi párosítást ad könyvenként, ezért az a korábbi mondat, hogy a projektnek nincs és nem is lesz szó-szintű Strong-taggelt Károlija, **elavult** (zárt licenc: kiadói tagged szöveg tényleg nincs; gépi párosítás van). Az átállítás szabálya (F65, DT104): csak az `azonositas_modja` vált; a `karoli_szo`, a `megbizhatosag` és a `proveniencia` marad.

---

### 1.8 `IGAZOLAS` — a D25 szerinti szétválasztás

Zárt értékkészlet: `TAHOT-igazolt` | `TAHOT-hatokoron-kivul` | `nincs`.

**Miért külön mező, és nem a provenienciában:** a proveniencia arra válaszol, *honnan
származik az állítás*; az igazolás arra, hogy *megerősítette-e valami*. A kettő
független. Egy retroaktívan betöltött study-sor provenienciája jogosan `manual` (az
állítás a kézzel írt tanulmányból jön), miközben a Strong-hozzárendelését a
TAHOT-visszakeresés tételesen igazolta — ez nem teszi a sort lekérdezés-eredménnyé,
de nem is puszta értelmezés.

Az F3 betöltői ezt eleinte a proveniencia-stringbe írták (`talalat=IGAZOLVA`,
`strong_vart=…`), ami két hibát okozott: nem szabványos kulcsokat vitt egy olyan
mezőbe, amelyet az 1.5 szerint a `lekerdez.py` ír szó szerint, és a 3.3 kényszert
értelmezhetetlenné tette (a sor egyszerre lett volna értelmezés és igazolt tény).
A szétválasztást az `eszkozok/igazolas_migracio.py` végezte el; a `strong_vart`
eldobásra került, mert mind a 138 soron azonos volt a `strong` oszloppal.

**A 3.3 kényszer ettől nem gyengül:** `manual` proveniencia esetén a sor továbbra is
értelmezésként jelölendő a generált kimenetben. Az `igazolas` mező ehhez *hozzátesz*
egy külön állítást, nem vonja vissza.

---

## 2. Táblák

### 2.1 `motivumok.tsv` — motívum-törzstábla

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | `TÉMAKÓD-NNN` | ✔ | A `motivumlog/Motivum_azonosito_sema_javaslat.md` v3 szerint. Témakódok: `TEREMT`, `ALVIL`, `ISTENTISZT`, `HODIT`, `ANTROP`, `MENNY`, `KIRALY`, `HAMART`, `SZOVETS` — **nyitott lista**, új kód felvehető. |
| `cim` | szabad szöveg | ✔ | Teljes név, pl. *Isten képmása (celem/eikón) motívum*. |
| `ui_cimke` | szabad szöveg, ≤ 24 karakter | ✔ | Rövid megjelenítési címke. |
| `tema` | szabad szöveg | | Szisztematikus locus, **opcionális** és **többértékű** (`Antropológia + Krisztológia`). A v3 séma szándékosan választotta el az `id`-tól: 3 motívumnál a dogmatikai besorolás nem egyértelmű vagy nem releváns. |
| `pardes_szint` | `PARDES_SZINT` | | A motívum súlypontja. |
| `statusz` | zárt | ✔ | `feldolgozás alatt` \| `publikálható` \| `véglegesített` — l. 2.1.1. |
| `statusz_verzio` | `v<N>` | ✔ | Pl. `v3`. |
| `statusz_datum` | `DATUM` | ✔ | A státusz felvételének napja. |
| `azonossag_tipusa` | zárt | ✔ | `lexikai` \| `formulaikus` \| `referenciális` \| `fogalmi` \| `strukturális` — a 4.6 gate 1. kérdése. |
| `negativ_kriterium` | szabad szöveg | ✔ | *Mi az a minimális jegy, amely nélkül egy igehely NEM tartozik ide?* A 4.6 gate 2. kérdése. Üresen hagyni nem szabad: **a határt a kizárások rajzolják meg, nem a meghatározás.** |
| `folerendelt_fogalom` | szabad szöveg | ✔ | Az a tágabb kategória, amely felé a motívum hígulni fog (HAMART-001: *a bűn / hamartológia általában*). Minden új sornál egyetlen kérdés: *csak ezen keresztül tartozik ide?* Ha igen, kizárandó. |
| `sablon_verzio` | `v<N>` vagy `v<N> részleges (érintett: …)` | | A megfelelőségi kör eredménye — l. az F5.2 szabályt. Teljes `v<N>` csak akkor írható, ha az ellenőrzés **minden** szakaszra lefutott. |
| `forras_study` | fájlút | | Pl. `tematikus_lezart/Rafaim_tematikus.md`. Több érték `;` jellel. |

#### 2.1.1 A háromértékű státusz

| Érték | Mit jelent |
|---|---|
| `feldolgozás alatt` | A motívum nyitott; jelöltjei minősítetlenek lehetnek. |
| `publikálható` | A tanulmány megírva és kapuzva, de **új lexikai bizonyíték vagy szerkesztői szándék egyaránt újranyithatja**. |
| `véglegesített` | **Csak új lexikai bizonyíték nyithatja újra, szerkesztői szándék nem.** |

*Miért váltja ez a mai „LEZÁRVA" címkét:* tizenhat motívum van ma így jelölve, közben a
Melkizedek a 08.22-i „lezárás" után 09.08-09-én bővült, a Segítségül hívni kétszer is.
A címke tehát nem jelentett semmit. A hármas skála mellett mérhetővé válik, **hányszor
nyílt újra egy tanulmány** — ami a küszöb-kritérium minőségének mérőszáma.

### 2.2 `elofordulasok.tsv` — a motívum igehelyei

Kulcs: `id` + `igehely`. **Ide csak a `jeloltek.tsv`-ből, `dontes=beépítve` értékkel
előléptetett sor kerülhet** (adatáramlási szabály 2: nincs közvetlen út a keresésből a
study táblázatába).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | motívum-id | ✔ | Idegen kulcs a `motivumok.tsv`-re. |
| `igehely` | `IGEHELY` | ✔ | |
| `kapcsolodas` | szabad szöveg | ✔ | Mi köti ide ezt a verset. |
| `pardes_szint` | `PARDES_SZINT` | | |
| `funkcio` | szabad szöveg | | A vers szerepe a motívum ívében. A 4.6 gate 3. kérdésének adata: ha egy igehely két motívumhoz tartozik, **a funkciónak különböznie kell**. |
| `gerinc_elem` | szabad szöveg | ✔ | **Melyik gerinc-elemen lóg ez a sor** — Strong-szám, kollokáció-pár vagy LXX-híd megnevezve (`H8415`, `málé+chámász`, `LXX:ᾅδης←H7585`). Ha egy sor nem tudja megnevezni a horgonyát, **a `jeloltek.tsv`-ben marad**. L. 2.2.1. |
| `strong` | `STRONG` | | Üres, ha a sor nem lexikai horgonyon áll (strukturális motívumnál ez normális). |
| `lexikon_szotar` | zárt: a 2.5 `szotar` értékkészlete | | Melyik szótár jelentésére hivatkozik a sor. Kötelező, ha `lexikon_entry_id` ki van töltve. |
| `lexikon_entry_id` | szabad szöveg | | A szócikk azonosítója az adott szótár kulcsa szerint (l. 2.5). |
| `jelentes_szam` | **union** | | L. 2.2.2 — ez a mező a 3.8-as nyitott tétel lezárása. A `lexikon_szotar` + `lexikon_entry_id` + `jelentes_szam` hármas a `lexikon_hivatkozasok.tsv` kulcsára mutat (2.5). |
| `jelentes_en` | szabad szöveg | | A szótári jelentés eredetiben. |
| `jelentes_hu` | szabad szöveg | | Magyar fordítása. |
| `karoli_szo` | szabad szöveg | | A Károli-szóalak ezen a helyen. **Öröklődik a `jeloltek.tsv` azonos kulcsú sorából.** |
| `azonositas_modja` | `AZONOSITAS_MODJA` | | Kötelező, ha `karoli_szo` ki van töltve. |
| `megbizhatosag` | `MEGBIZHATOSAG` | | Kötelező, ha `karoli_szo` ki van töltve. |
| `proveniencia` | `PROVENIENCIA` | ✔ | L. 1.5. |
| `igazolas` | `IGAZOLAS` | ✔ | Megerősítette-e lekérdezés ezt a sort. L. 1.8. |
| `fo_elofordulas` | szabad szöveg — **csoportkulcs, nem igen/nem** | | A naplóban (`PaRDeS_motivumok.md`) megnevezett "fő előfordulás" saját szövege, szó szerint (pl. `2Móz 15:5,8`, `1Móz 6:1-4`). Üres, ha a sor nem tartozik fő előforduláshoz. L. 2.2.3. |
| `felmerult_tanulmany` | szabad szöveg | | A study 1. pontja "PaRDeS-szint, ahol felmerült" oszlopának a szint utáni része, szó szerint. Üres, ha a study táblázata nem tartalmaz ilyen oszlopot, vagy a sor csak a szintet ismétli. |
| `forras_tanulmany` | repó-relatív fájlút | | A tanulmányfájl, amelyben a sor lelete felmerült (pl. `genezis/1Moz_3v7-24_bovitett.md`): a generált visszamutató link forrása (DT66 (a) 5., DT250). Az utolsó oszlop (a DT183 mintájára, #11 S2). Csak létező, repón belüli fájlra mutathat, előtag (`./`) és visszalépés (`..`) nélkül, `/` elválasztóval (CI: E31, HIBA; a fejlécet az `ellenoriz.py` 16. szabálya nézi). Üres érték: nincs rögzített forrástanulmány, **nem negatív lelet**; üres sor nem tölthető ki asszociatív alapon. A `felmerult_tanulmany` szabad szöveg marad, mellette változatlan. |

#### 2.2.1 A `gerinc_elem` mező — miért kötelező

Nem azért, mert enélkül hígulna a motívum, hanem mert **enélkül nem látszik, hogy nem
hígult.** A projekt megfigyelt hibái eddig határproblémák voltak (Rafaim ↔ Nefilim), nem
hígulás — de ez az információ eddig a munkamenet fejében élt, a fájlban csak az eredmény
maradt. A 49 soros HAMART-001 táblából nem állapítható meg, melyik horgonyon lóg a 38.

Ingyen van: a `lekerdez.py` tudja, melyik parancs melyik sort hozta.

*Kalibráció:* az opus-ág 49 sora ~8 gerinc-elemen állt, azaz ~6 sor elemenként. Húsz sor
egyetlen elemre **vizsgálandó — jelzés, nem tiltás.**

#### 2.2.3 A `fo_elofordulas` mező — miért csoportkulcs, nem logikai érték

**Eredeti terv (D10, F4_GENERATOR_BRIEF.md): `igen`/`nem`.** A G0/d kitöltés közben
kiderült, hogy ez elveszít egy tényt: a napló többször **egyetlen "fő
előfordulásként" nevez meg egy verközt vagy verspárt** (pl. `2Móz 15:5,8`,
`1Móz 6:1-4`, `Luk 1:46-47`, `1Kor 2:14-15`), miközben ez a tábla verssoronként
tárol. Egy logikai mező ilyenkor vagy két sorra bontaná a "fő előfordulást"
(a generált szám elszakadna a napló számától), vagy csak az egyik sort jelölné
(a másik verssor indoklás nélkül tűnne el a küszöbszámlálásból).

**A döntés (2026.09.15, chat-menet):** a mező típusa szöveg — a napló saját
megnevezése a csoportról, szó szerint. A ⭐ küszöb-generátor ezután
`COUNT(DISTINCT fo_elofordulas)`-t számol ID-nként, nem sorszámlálást. Egyik
verssor sem vész el, a generált szám egyezik a napló prózájának számával, és a
mező grepelhető vissza a napló szövegére — az összevetés bármikor
megismételhető. Ez a D10 módosítása, nem visszavonása.

*Önellenőrzési szabály a generátornak:* ID-nként a `COUNT(DISTINCT
fo_elofordulas)` egyezzen a napló ⭐-szakaszában kimondott számmal; eltérésnél a
szkript álljon meg (l. a G0/d 2026.09.15-i futásának ALVIL-001-esetét, ahol ez a
szabály egy második, addig dokumentálatlan hibát is felszínre hozott — a
`Lezart_tematikus_tanulmanyok_index.md` #2 sorából hiányzott a Jel 1:18).

#### 2.2.2 A `jelentes_szam` mező — a 3.8-as tétel lezárása

**A mező típusa union: numerikus jelentés-szám VAGY binyan-címke.**

| Alak | Mikor | Példa |
|---|---|---|
| numerikus | a BDB számozott jelentésekre tagolja a szócikket (főnevek, melléknevek túlnyomó része) | `1`, `2`, `3a` |
| binyan-címke | **a BDB az igegyököket binyan szerint tagolja, nem számozott jelentésekkel** | `Nif'ál`, `Pi'él`, `Hif'íl` |
| binyan + igealak | ha a megkülönböztetés igealakon múlik | `Qal pass. ptc.`, `Qal impf.` |
| alternatíva | ha a hely két binyan között eldöntetlen | `Nif'ál / Hif'íl` |
| `teljes` | **a forrásfájl nem bont számozott jelentésekre — a teljes szócikk egy sorban áll** (LEXV2_2_BRIEF.md V2.3, jelenleg: Thayer) | `teljes` |
| `részlet` | **a szótári szócikk egy kiemelt része** (szócikkfej, etimológia vagy reprezentatív kivonat), amikor a forrás nem jelentés-szám szerint van tagolva, vagy a teljes szócikk terjedelme miatt csak részlet szerepel (ISTENTISZT_2B_ADATOSITAS.md D0) | `részlet` |

**A `teljes` és a `részlet` érték három korlátja — azonos:**
1. Csak olyan szótárnál használható, amelynek forrásfájlja ténylegesen nem bont
   számozott jelentésekre (`teljes`: jelenleg egyedül a `Thayer_teljes.tsv` —
   egy sor = egy teljes szócikk, `Teljes_szocikk` mezővel), illetve amelynek
   idézete a fenti okból csak részlet (`részlet`).
2. Csak a `lexikon_hivatkozasok.tsv`-ben szerepelhet. Az `elofordulasok.tsv`
   `jelentes_szam` mezője **soha** nem mutathat `teljes` vagy `részlet`
   értékre — egy előfordulás mindig egy konkrét jelentésre hivatkozik, nem a
   teljes szócikkre vagy annak részletére.
3. Egy `szotar` + `strong` + `entry_id` hármashoz **legfeljebb egy** `teljes`
   jelentes_szam-ú **és** legfeljebb egy `részlet` jelentes_szam-ú sor
   tartozhat (a kulcs egyébként `szotar`+`strong`+`entry_id`+`jelentes_szam`,
   tehát enélkül a korlát nélkül duplázható lenne).

*A ma használatban lévő teljes értékkészlet* (mért, `tematikus_lezart/` + `genezis/`):
`Qal pass. ptc.` (6), `Pi'él` (2), `Qal impf.` (1), `Nif'ál` (1), `Hif'íl` (1),
`Nif'ál / Hif'íl` (1).

**Az indoklás, amely eddig hiányzott:** a `4_PaRDeS_tematikus_sablon.md` literál példája
(`1`) numerikus értéket sugall, és a nem-numerikus értékek eddig **indoklás nélkül**
álltak a táblázatokban — ez volt az átadási dokumentum 3.8-as kifogása. Az adaptáció
ésszerű, mert a BDB szerkezetét követi; ami hiányzott, az a rögzítése. Ez a szakasz
rögzíti. **A sablonba nem kell külön módszertani jegyzet** — a sablon erre a szakaszra
hivatkozzon.

*Validációs szabály:* ha a `strong` mező igét jelöl (a `Strong_szotar.tsv` szófaj-mezője
`ige`), a numerikus érték **gyanús** — az `ellenoriz.py` jelezze, de ne utasítsa el.

### 2.3 `kapcsolatok.tsv` — igehely-párok

Kulcs: `forras_igehely` + `cel_igehely` + `id`.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `forras_igehely` | `IGEHELY` | ✔ | |
| `cel_igehely` | `IGEHELY` | ✔ | |
| `id` | motívum-id | ✔ | |
| `tipus` | zárt | ✔ | `Előkép` \| `Párhuzam` \| `Beteljesedés` \| `Kontraszt` \| `Variáns` — a **KAPCSOLATOK Típus-mező v1**, 2026.09.09-én lezárva. |
| `funkcio` | szabad szöveg | | |
| `bizonyossag` | zárt | ✔ | `magas` \| `közepes` \| `alacsony`. Küszöb alatti sor a `jeloltek.tsv`-ben marad. |
| `pardes_szint` | `PARDES_SZINT` | | |
| `indoklas` | szabad szöveg | | A sor funkció- és bizonyosság-indoklása: a lexikonoldal Alátámasztás-résének soronkénti adata (3.10.7 1., DT84 (8) a). Az utolsó oszlop; a meglévő sorokon üres (#11 S1, DT183). Üres érték: nincs rögzített indoklás, nem negatív lelet. |

> **Ismert névütközés, nem oldódott meg** — a `motivumlog/lexikon_pilot/Motivum_kapcsolatok_PILOT.tsv`
> „Típus" oszlopa egy **másik tengely** (`LEXIKAI`/`NARRATÍV`/`STRUKTURÁLIS`/`TEMATIKUS`),
> mint az itteni `tipus`. A pilot-TSV-ben nincs önálló oszlop a PaRDeS Típus-mezőre.
> A betöltésnél (F3) a két tengelyt szét kell választani; ez a tábla a PaRDeS-tengelyt viszi.

### 2.4 `jeloltek.tsv` — a kereszthivatkozás-napló gépi alakja

Kulcs: `id` + `igehely` + `jelolt_tipus` + `cel_id` (DT277 (i), #127; előtte `id` + `igehely`).
**Ez a tábla a rendszer legfontosabb szerkezeti javítása.**

A tábla két jelöltfajtát hordoz, és ez az egyetlen kapu mindkettőhöz (2. szabály):
**előfordulás-jelölt** (`jelolt_tipus=elofordulas`: a motívum lehetséges előfordulása) és
**motívumközi jelölt** (`jelolt_tipus=motivumkozi`: az `id` motívum `igehely`-e és a `cel_id`
motívum `cel_igehely`-e közötti lehetséges kapcsolat; a döntés után a `motivum_kapcsolatok.tsv`
sora lesz belőle, 2.33). **Minden előfordulás-jelöltet olvasó eszköz csak az `elofordulas`
sorokat olvassa** (`general.elofordulas_jeloltek`; DT279 (1): `general.py`,
`lexikon_general.py`, `ellenoriz.py`, `jelolt.py`, `nem_vizsgalt.py`, `betolt.py`,
`karoli_ellenorzes.py`, `ellenorzes/szabalyok.py`, `sqlite_epit.py`) — a motívumközi jelölt
nem kizárt hely, nem a motívum vizsgált verse, és nem igazol előfordulást.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | motívum-id | ✔ | |
| `igehely` | `IGEHELY` | ✔ | Motívumközi jelöltnél az `id` motívum oldali igehely. |
| `forras_kereses` | szabad szöveg | ✔ | Melyik lekérdezés hozta elő (`scan H7497`, `TSK 1Móz 6:4`, `Károli-KH`). |
| `dontes` | zárt | ✔ | `beépítve` \| `elutasítva` \| `nyitva`. |
| `indoklas` | szabad szöveg | ✔ | `elutasítva` esetén **kötelezően érdemi**. Egészséges jel, ha sok az *„elutasítva, mert csak a fölérendelt fogalmon keresztül tartozna ide"* tétel. |
| `karoli_szo` | szabad szöveg | | L. 2.4.1. |
| `azonositas_modja` | `AZONOSITAS_MODJA` | | |
| `megbizhatosag` | `MEGBIZHATOSAG` | | |
| `datum` | `DATUM` | ✔ | |
| `jelolt_tipus` | zárt | ✔ | `elofordulas` \| `motivumkozi` (DT277). A #127 előtti 627 sor `elofordulas`. |
| `cel_id` | motívum-id | `motivumkozi`-nál ✔, egyébként üres | A kapcsolat másik motívuma; létező, a sajáttól eltérő ID. |
| `cel_igehely` | `IGEHELY`-lista (`; `-vel elválasztva) | `motivumkozi`-nál ✔, egyébként üres | A másik motívum oldali igehely(ek); nem kulcs (DT279). |
| `cel_alpont` | szabad szöveg (a célalpont neve) | | DT277 (C): a kapcsolat célja a másik motívum egy ↳ alpontja. Amíg az alpontnak nincs adatbeli azonosítója, a jelölt `nyitva` marad (az `ellenoriz.py` 2/b. szabálya a `beépítve` + `cel_alpont` párt elutasítja), kapcsolat-sor nem keletkezik belőle. Nem kulcs (DT279). |

#### 2.4.1 Miért itt van a `karoli_szo`, és nem máshol

**Ma a napló külön megírandó fájl, tehát el lehet felejteni — 2026.09.10-én négy valódi
keresésnél el is felejtődött.** Ugyanaz a kimaradt lépés okozta a négy hiányzó
kereszthivatkozás-naplót **és** azt, hogy a nap négy teljes körű scanje egyetlen új
join-sort sem termelt (a Rafaim H7497 három új igehelye, a Tehóm H8415 három új verse, a
Hádész-scan Hós 13:14-es lelete — egyik sem került be). Egy ok, két nyom.

A Károli-hozzárendelés nem a *szükség*, hanem a **jelöltek tételes minősítése** mentén
keletkezik: aki minden találatot végigvisz, az menet közben a Károli-szöveget is megnézi,
mert a tartalmi ítélethez kell.

Ezért a `karoli_szo` **fizikailag ugyanaz a sor**, mint a minősítés. Nem lehet elfelejteni
azt, ami annak a sornak a mezője, ahol az igehely amúgy is szerepel.

*Megerősítő jel a mérésből:* a naplóval rendelkező tanulmányok sűrűbben járulnak hozzá a
join-táblához (Tehóm 24 sor, Segítségül hívni 8), a napló nélküliek ritkábban (Rafaim 6,
Hádész 4).

### 2.5 `lexikon_hivatkozasok.tsv`

Kulcs: `szotar` + `strong` + `entry_id` + `jelentes_szam`.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `strong` | `STRONG` | ✔ | |
| `szotar` | zárt | ✔ | `BDB` \| `TBESH` \| `TBESG` \| `Thayer` \| `LSJ` \| `Strong` \| `SDBH` \| `SDGNT` \| `SECE_G` \| `SECE_H` \| `MCGED` |
| `entry_id` | szabad szöveg | ✔ | Szótáranként: BDB, LSJ, SECE → a konkordancia-fájl `Strong_padded` kulcsa; **Thayer** → a `Thayer_teljes.tsv` `Strong_eredeti` mezője (nullázatlan, pl. `G12`, nem `G0012` — LEXV2_2_BRIEF.md V2.3 döntés, eltér a többi szótár konvenciójától); MCGED → a `lexikonok_nyers/MCGED.lexicon` `G####` Strong-kulcsa (a `gkG5####` GK-kulcs nem használható, l. `lexikonok_nyers/README.md`); TBESH/TBESG → a fájl első oszlopa; SDBH/SDGNT → `entry_id` (`MainId`), a `jelentes_szam` pedig a `lexid`. |
| `jelentes_szam` | union (l. 2.2.2) | ✔ | |
| `szoveg_en` | szabad szöveg | ✔ | **Rövid kivonat, nem teljes szócikk** — a forrásfájl sorának szó szerinti részlete; a generált lexikon innen idéz. |
| `forrasfajl` | fájlút | ✔ | Pl. `konkordancia/BDB_teljes_unabridged.tsv`. |

A szótárankénti tényleges licenc a `konkordancia/lexikonok_nyers/README.md`-ben van
rögzítve (Thayer, LSJ, SECE, MCGED); a generált lexikon-oldal minden szótárból idézhet,
a forrás saját licencének jelölésével — az MCGED-nél kötelező szó szerinti
forrásmegjelöléssel (F6 D16).

**A `forditas_hu` oszlop 2026.09.28-tól (SZOTAR S1.1) megszűnt** — a jelentés
magyar fordítása az `adat/forditasok.tsv`-be költözött (l. 2.14), kulcsban
`mezo=forditas_hu`-val azonosítva; a lookupot a `lexikon_general.py`
`forditas_ehhez()` függvénye végzi renderidőben. A fordítás tartalmi
szabálya (rövidítés-feloldás, Károli-rövidítés, változatlan idegen idézet
stb.) változatlanul érvényes, csak a tárolás helye más.

### 2.6 `datasetek.tsv`

Kulcs: `study_tipus` + `dataset`. A terv 4.3 mátrixa, négy study-típusra kifejtve
(`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`), 21 dataset × 4 = 84 sor.

| Mező | Értékkészlet |
|---|---|
| `study_tipus` | `bovitett` \| `tematikus` \| `melyelemzes` \| `lexikon_oldal` |
| `dataset` | a dataset rövid neve (21 érték) |
| `fajl` | a dataset útvonala; glob is lehet (`konkordancia/LXX_OS/*.tsv`), üres, ha `allapot=hianyzik` |
| `kotelezoseg` | `mindig` \| `felteteles` \| `ajanlott` \| `oroklott` |
| `feltetel` | mikor válik kötelezővé a `felteteles` sor; `—`, ha nem feltételes |
| `allapot` | `elerheto` \| `korlatos` \| `hianyzik` \| `generalt_nezet` |
| `megjegyzes` | a datasetre jellemző korlát vagy tudnivaló (study-típustól független) |

**Két `allapot` érték követel figyelmet:**

- `hianyzik` — jelenleg egyetlen sor sem viseli. Az SDBH és az SDGNT volt ilyen; importjuk
  2026.09-ben megtörtént (`konkordancia/SDBH_SDGNT_README.md`). Az érték az értékkészletben
  marad a még nem importált datasetek számára.
- `korlatos` — a `KJV_ASV_Strongs` **csak Genezis, Exodus és Példabeszédek** könyvekre áll
  rendelkezésre. Bármely más könyvre hivatkozó „ellenőrizve" állítás ezen a dataseten hamis.
  A `KJV_Strongs_teljes.tsv` (F19) külön, `importált, javaslat` állapotú dataset, a `KJV_ASV_Strongs` sor `fajl`-mintája nem tartalmazza; az `ASV_Strongs_teljes.tsv` forráshibás és nincs a repóban (DT19, `naplok/ELLENOR_F19.md`).
  **A `KJV_teljes_szoveg.tsv` (F118, #118) a dataset leírása; a DT226 dataset-README szerepét ez a bekezdés tölti be** (a szabály még nincs a main-en, és a brief `ir` listájában nincs README; `naplok/KJV_SZOVEG_meres.md`).
  - **Mi ez:** a teljes KJV-szöveg versenként, a Károli melletti párhuzamos megjelenítéshez; `ajanlott`, nem lexikai forrás. Generált (`eszkozok/kjv_szoveg_import.py`, `# GENERÁLT:` fejléc), kézzel nem szerkeszthető. 66 kanonikus könyv, 31 218 sor: 31 102 vers és 116 zsoltárfelirat 0. versként. Állapot: `importált, elfogadva` (felhasználó, 2026-10-18).
  - **Oszlopok:** `Igehely` (STEP-alak, `Gen.1.1`, KJV-számozás, a felirat verse `0`; a magyar alakra a `Konyv_normalizalo_tabla.tsv` konvertál) · `Szöveg` (olvasószöveg: jelölő, lábjegyzet és `¶` nélkül) · `Szöveg_jelolt` (a dőlt betoldás `[…]`, Jézus szavai `‹…›` versenként zárva, a `¶` megmarad) · `Elotte` (a vers előtti `\s1` címsor: a Zsolt 119 22 akrosztichon-fejléce, pl. `א ALEPH.`) · `Utoirat` (a könyv utolsó verse utáni `\s1`: 14 páli utóirat, Róm 16:27 … Zsid 13:25). Az `Elotte`/`Utoirat` olvasószöveg-alakú (DT213).
  - **A két KJV-tábla viszonya:** ugyanabból a forrásból (az eBible-csomag; az F19-generátor az új csomagból bájtra a `KJV_Strongs_teljes.tsv`-t adja, `naplok/KJV_SZOVEG_M0.md`) és ugyanazzal a kulccsal. A `KJV_Strongs_teljes.tsv` szavanként a Strong-címkés szavakat hordozza (licenc: DT124/DT126), ez a tábla versenként a teljes szöveget, Strong-címke nélkül (DT210: `kozkincs`). A `KJV_Strongs_teljes` versei ⊆ e tábla versei; a különbség a 3 címke nélküli vers (Mk 9:43, Lk 6:41, Lk 17:36). Minden Strong-címkés szó megtalálható a `Szöveg`-ben; 76 összetett szó (where+in = wherein) és 8 szótöredék-címke (afrai|…+d) a `naplok/KJV_SZOVEG_szoegyezes_hiany.tsv`-ben.
  - **Különlegesség:** az 1Jn 2:23 forrásbeli „[but]” szögletes zárójele a forrás szerint marad, ezért a `Szöveg_jelolt`-ban egymásba ágyazott: „[[but] … also]” (DT213 (3)). A 66 kanonikus könyvben ez az egyetlen szó szerinti szögletes zárójel.
  - **Nyers forrás (DT212 (d), DT226 (1)):** https://ebible.org/Scriptures/eng-kjv_usfm.zip, sha256 `00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447`, 2 766 294 bájt, a bejegyzések 2026-10-17-esek. A zip nincs a repóban (a Strong-címkeréteget hordozza, DT124/DT126). Elsődleges hely: `C:\Users\bases\Desktop\kjv_munka\kjv.zip`. **Második példány: megadandó** (a felhasználó adja meg; addig üres). Újrafuttatás: `python eszkozok/kjv_szoveg_import.py --munka <mappa>`; a nyersből bájtra a tábla adódik (mérve, `naplok/KJV_SZOVEG_meres.md`). A DT126 döntése után a zip helye újranézendő.
  - **Veszteséges konverzió (DT226 (2)):** a tábla `# veszteség:` fejlécsora darabszámmal: kimarad a Strong-címke (349 308), a lábjegyzet (6 959), a `\p`/`\q1`/`\b` tagolás (4 635 / 2 461 / 209), a könyvfejléc (398 sor), a `\nd` (6 892) és a `\tl` (22) jelölése; a `Szöveg`-ből a `\wj` (2 038), az `\add` (21 510; az utóiratokban 7 jelölése teljesen elvész) és a `¶` (2 970), amelyeket a `Szöveg_jelolt` megőriz. A darabszámok a nyers forrás független számolásával egyeznek (`naplok/KJV_SZOVEG_meres.md`).
  Ugyanígy `korlatos` a `BSB_Strongs` (F16): csak a 95%-os küszöböt elérő 36 ÓSZ-könyv (nincs: 2Sám, Ezsd, Dán), ÚSZ szándékosan nincs (a görög réteg forrása a Macula, #87);
  a Zak 12:1 és a 116 feliratos zsoltár 1. versének érdemi szövege a display-forrásból hiányzik (a text-only megvan);
  az `Igehely` célszámozása az MT (WLC); a 7. oszlop (`Számozás`) versszintű WLC-összevetésből: `mt` (260 243 sor, 20 180 vers: a WLC-vel versszinten egyértelműen megfeleltetett — a WLC azonos számú versének Strong-halmaza > 0,5 átfedéssel az Igehely-versben van, ez szigorúan jobb a WLC- és a BSB-környezet bármely másik versénél, nem hibrid részvers, és a szomszéd vers is illeszkedik; Strong-halmaz-egyezés, nem tartalmi egyezés) / `ellenorizetlen` (17 659 sor, 1 477 vers, 271 fejezet: a WLC-vel egyértelműen nem igazolt — nagy része formulás/ismétlődő, azonos Strong-halmazú szomszéd versek döntetlenje KJV = MT fejezetekben; a többi hibrid részvers, izolált egyezés, vagy üres WLC-halmaz; a Jób 40:1/3/6 is; **nem állítja, hogy a szám hibás**; fejezetenként `naplok/F41_wlc_versszam_ellenorzes.tsv`) / `kjv` (223 sor, 34 vers: a ténylegesen KJV ≠ MT Jób 41, a BSB/KJV-szám marad; paraméter-érzékenység: `naplok/F41_parameter_erzekenyseg.md`); a Zsolt 13 kézi kivétellel importálva (DT-F41a, F71: csak MT 3–6; az MT 1–2 hiányzik). A 6. oszlop (`Angol szó állapota`): `forditva` / `elhagyva` / `ures_jelzo_nelkul`.

*Licenc-következmény, rögzítve a `konkordancia/README.md` licenc-szakaszában és a
`konkordancia/SDBH_SDGNT_README.md`-ben:* a CC BY-SA 4.0
forrásmegjelölést követel, **és a származékos adat is ugyanilyen licenc alá esik** — ez
érinti a lexikon publikálási formáját.

### 2.7 `grammatikai_strongok.tsv` — **generált**

Kulcs: `strong`. Előállítja: `eszkozok/grammatikai_strongok_general.py`.
**Kézzel nem szerkesztendő** — a két tételes lista (`HEBER_KEZI`, `GOROG_KEZI`), a
`TILTOLISTA` és a `HATARESET` a szkript forrásában él, ott módosítandó.

A terv 4.1 pontja szerint a gerinc-metszet e fájl nélkül használhatatlan.

| Mező | Leírás |
|---|---|
| `strong` | `STRONG` (l. 1.2) |
| `rovid_jelentes` | a szó rövid magyar jelentése; héber oldalon a TAHOT-kivonat glossza |
| `kategoria` | `affixum` \| `targyrag` \| `vonatkozo_nevmas` \| `tagadoszo` \| `nevelo` \| `kotoszo` \| `eloljaro` \| `nevmas` \| `partikula` |
| `kizaras_oka` | **miért** nem hordoz motívum-tartalmat ez a Strong-szám |

*Megjegyzés az oszlopnevekről:* a specifikáció ezeket `Strong | rövid jelentés |
kategória | kizárás oka` alakban adta meg; a fájl a többi `adat/` táblával egyező
ASCII snake_case alakot használja, azonos jelentéssel.

#### 2.7.1 A besorolás kritériuma

**Egy Strong-szám akkor grammatikai, ha a szó önmagában nem hordoz tartalmi jegyet —
függetlenül attól, hogy prefixként vagy szabadon áll. A `H9xxx` tartomány kényelmes
kiindulás, de nem definíció.**

Ez a szakasz legfontosabb mondata, és a tábla szerkezete ebből következik, nem fordítva.
A `H9xxx` tartomány **ortográfiai határ, nem szemantikai**: a héberben a névelő, a
kötőszó és a gyakori elöljárók prefixumként tapadnak a szóhoz, ezért kaptak külön
grammatikai kódot — de egy elöljáró nem attól lesz tartalmas, hogy külön szóként írják.

A kritérium **ellenőrizhető**, nem csak kimondott: a `Strong_szotar.tsv` szófaj-mezője
független jelet ad. A kézi listára felvett tíz héber tétel mindegyike `elöljárószó`,
`kötőszó`, `partikula` vagy `névmás`; a szándékosan kihagyottak `főnév`, illetve `ige`.

#### 2.7.2 A tábla három forrása

| Forrás | Sor | Hogyan keletkezik |
|---|---|---|
| **héber gépi alap** — a TAHOT `H9xxx` tartománya | **44** | a szkript automatikusan olvassa ki, provenienciával; kézi karbantartást nem igényel |
| **héber kézi kiegészítés** | **10** | tételes, soronként indokolt |
| **görög tételes lista** | **31** | tételes, soronként indokolt |
| **összesen** | **85** | |

A `H9xxx` tartomány a héber névelőt, kötőszót, a prefixált elöljárókat és a névmási
szuffixumokat fedi le: **44 kód, 169 598 előfordulás** a TAHOT-kivonatban — a kivonat
468 968 sorának 36%-a. Ez a fájl legnagyobb hozadéka, és teljes egészében gépi.

A **tíz kézi héber tétel** azért kell, mert a 2.7.1 kritériuma szerint grammatikai, de
nincs a `H9xxx`-ben:

| Strong | Szó | Kategória | db | Miért |
|---|---|---|---|---|
| `H0853` | אֵת | tárgyrag | 11 050 | nem hordoz jelentést, csak a határozott tárgyat jelöli |
| `H0834` | אֲשֶׁר | vonatkozó névmás | 5 502 | alárendelt tagmondatot vezet be; a tagmondat tartalmáról semmit nem mond |
| `H3808` | לֹא | tagadószó | 5 166 | a tagadás formális jelölője; a tartalmat a tagadott fogalom hordozza |
| `H5921` | עַל | elöljáró | 5 768 | szabadon álló; görög párja a `G1909` (ἐπί) |
| `H0413` | אֶל | elöljáró | 5 515 | szabadon álló; görög párja a `G1519` (εἰς) |
| `H3588` | כִּי | kötőszó | 4 482 | alárendelő; görög párja a `G3754` (ὅτι) |
| `H1931` | הוּא | névmás | 1 876 | személyes/mutató; görög párja a `G0846` (αὐτός) |
| `H5704` | עַד | elöljáró | 1 261 | időbeli/térbeli határ, tartalmi jegy nélkül |
| `H4480` | מִן־ | elöljáró | 1 189 | szabadon álló — l. alább |
| `H2088` | זֶה | névmás | 1 180 | mutató; görög párja a `G3778` (οὗτος) |

**A `H4480` a legárulkodóbb eset, mert önmagában bizonyítja a kritériumot.** Ugyanaz a
héber elöljáró (*min*, „-ból, -től") két Strong-számon ül, aszerint, hogy hogyan írják:

| | Strong | Előfordulás | Hol volt |
|---|---|---|---|
| prefixált (מִ) | `H9006` | **6 383** | a gépi `H9xxx` alapban, kezdettől |
| szabadon álló (מִן־) | `H4480` | **1 189** | sehol, amíg kézzel fel nem vettük |

Azonos szó, azonos jelentés, azonos funkció — a listát pusztán az írásmód vágta ketté.

#### 2.7.3 A görög oldalnak nincs gépi alapja

**A héber `H9xxx`-nek nincs görög megfelelője.** A TAGNT `G9xxx` tartománya
**nem grammatikai**: mindössze hét ritka *lexikai* szó (συναλλάσσω „sürgetni",
ὑπόλειμμα „maradék", ταπεινοφροσύνη, οἰκουργός stb.), egyenként **egy** előfordulással —
kiegészítő Strong-számok olyan szavakhoz, amelyek az eredeti Strong-számozásban nem
szerepelnek.

Ennek oka ugyanaz az ortográfiai tény, amit a 2.7.1 mond ki, csak a másik irányból: a
héberben ezek prefixumok, a görögben **önálló szavak**, tehát rendes Strong-számon ülnek
(`G3588` ὁ, `G2532` καί, `G1722` ἐν). A görög oldal ezért **eleve** az, amivé a héber
oldal a tíz kézi tétellel vált: tételes lista.

31 kód, 65 646 előfordulás a TAGNT-kivonatban: névelő (1), kötőszók (7), elöljárók (12),
névmások (8), tagadószók (3), partikulák (3).

*Egy lemmatizálási sajátosság dokumentálva:* a TAGNT a **többes számú személyes
névmásokat is az egyes számú kód alá** sorolja (`ἡμῶν` a `G3165` alatt, a többes számú
„ti"-alakok a `G4771` alatt), ezért a `G2249` (ἡμεῖς) és a `G5210` (ὑμεῖς) **nem kap
sort** — a kivonatban nulla előfordulásúak.

#### 2.7.4 `TILTOLISTA` — amit soha nem szabad kiszűrni

Hat Strong-szám **gépi tiltás** alatt áll. Ha egy későbbi bővítés — például
gyakoriság-alapú — bármelyiket felvenné, a **szkript hibával leáll**, nem csak
figyelmeztet:

| Strong | Szó | db | Miért nem szűrhető |
|---|---|---|---|
| `H3068` | יהוה | 6 528 | az istennév maga motívum-hordozó |
| `H1961` | הָיָה | 3 562 | „lenni" — **tartalmi ige**; a teremtés-motívumoknál gerinc-elem lehet |
| `H6213` | עָשָׂה | 2 628 | „tenni, csinálni" — tartalmi ige, ugyanazon okból |
| `H0559` | אָמַר | 5 309 | „mondani" — elbeszélői keretszó, **de tartalmi ige**; kizárása leletet törölne |
| `G2316` | θεός | 1 343 | a `H3068`/`H0430` görög párja, ugyanazon okból |
| `G3004` | λέγω | 1 357 | a `H0559` görög párja, ugyanazon okból |

**Miért gépi tiltás, és nem megjegyzés:** e szavak nagy gyakoriságúak — pontosan azok,
amelyeket egy „szűrjük ki a leggyakoribbakat" típusú bővítés **elsőként söpörne be**.
A tiltás azt a hibát zárja ki, amit a szándék nem tud: a szűrő így nem zajt távolítana
el, hanem leletet.

**Határeset, szándékosan nyitva hagyva:** a `H3605` (כֹּל, *kol*, „minden", 5 412
előfordulás) gyakori és kvantor-szerű, **de tartalmi jegyet is hordozhat** — a teljesség,
a kivétel nélküliség motívumszinten releváns lehet. Ezért **sem a táblán, sem a
tiltólistán nincs**: a szkript `HATARESET` szótárában dokumentált, de inaktív. Ha valaha
felvesszük, külön kategóriával és külön indoklással.

#### 2.7.5 Hatókör — ez stopword-lista, nem globális kizárás

**Ez a tábla a `lekerdez.py gerinc` parancs stopword-listája.** Nem jelenti azt, hogy a
felsorolt szavak a projektben bárhol érdektelenek.

Ha egy elöljáró **motívumszinten** számít — mint az עַל־פְּנֵי (*al-pené*, „színe fölött",
1Móz 1:2) szerkezet —, azt a **`kollokacio` parancs** találja meg, amely szópárt keres
egy versen belül, nem a **`gerinc` parancs**, amely szakaszok közös Strong-halmazát
metszi. **A kettő nem ütközik:** más a bemenetük, más a kérdésük.

A megkülönböztetés gyakorlati következménye: ha egy sor egy elöljárós szerkezeten lóg,
a `gerinc_elem` mezőbe a **kollokáció-pár** kerül (`al+pané`), nem a puszta Strong-szám.

#### 2.7.6 Kalibráció a HAMART-001 esetre

A terv 4.1 pontja szerint a HAMART-001 gerinc-metszete 23 közös Strong-számot adott,
amelyből egyetlen tartalmi szó maradt: אֲדָמָה (*adamá*, H0127). A metszetet gépileg
újraszámoltam (1Móz 3 ∩ 4 ∩ 6:1-8 ∩ 6:9-22) — **pontosan 23**, egyezik a tervvel.

A szűrőn átengedve:

| | |
|---|---|
| metszet | **23** |
| kiszűrve — 7 `H9xxx` affixum + `H0853`, `H0834`, `H0413`, `H5921`, `H3588` | **12** |
| **marad — gerinc-jelölt** | **11** (52% zajszűrés) |

**A lényeges eredmény nem a szám, hanem az összetétel: a megmaradó tizenegyből egy sem
funkciószó.** Mind főnév vagy ige — `H0127` *adamá*, `H0430` *Elohim*, `H0559` *amar*,
`H0802` *issá*, `H1121` *bén*, `H1961` *hájá*, `H3205` *jalad*, `H3605` *kol*,
`H3947` *lakach*, `H6213` *aszá*, `H6440` *pané*. A grammatikai osztály ezen a
teszteseten **lezárult**; ami bent maradt, az emberi ítéletet kíván, nem listabővítést.

*A lista fejlődése ugyanezen az eseten:* 23 → 3 (első, keretszavas változat) → 23 → 14
(szűkített, háromtételes kézi lista) → **23 → 11** (a kritérium következetes
alkalmazása). A középső lépés hagyta bent a `H0413`/`H5921`/`H3588` hármast — nem elvi
okból, hanem mert a lista még esetenként épült, nem szabály szerint.

**Ez a fájl elfogadási tesztje; a szkript módosítása után újra kell futtatni.**

### 2.8 `kulcsszavak.tsv` — átmeneti tábla, study→adat átjáró (F8_BRIEF.md G2a)

Kulcs: `tanulmany` + `igehely` + `strong`. **Átmeneti tábla:** a Tanulmány sablon 2.
pontjának kulcsszó-táblázatát viszi géppel olvasható alakba, mielőtt a betöltés
motívum-ID-t rendelne hozzá. Az `id` mező szándékosan **nincs** ezen a táblán — az
csak az A4 lépésben, a `jeloltek.tsv`-ben születik meg (l. 2.4 és `F8_BRIEF.md` §1 L4). A `betolt.py`
(A3 irány, G2a) írja; kézzel nem bővítendő.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `tanulmany` | fájlút | ✔ | A forrás tanulmány (igeszakasz-tanulmány) útvonala. |
| `igehely` | `IGEHELY` | ✔ | |
| `szo` | szabad szöveg | ✔ | A kulcsszó-táblázat magyar/héber/görög szava, ahogy a study-ban áll. |
| `strong` | `STRONG` | ✔ | |
| `datum` | `DATUM` | ✔ | |

### 2.9 `auditok.tsv` — lekérdezés-napló, motívumszintű dataset-nyom (N12)

Kulcs **nincs** — egy ID-hez több azonos sor is lehet (egy motívumnál a `scan`
parancs több Strong-számra is fut, mindegyik saját sort kap). Ez a tábla adja
a 8. szabály (3.8) nyomát: a 8. szabály **motívumszintű**, nem igehely-szintű
— egy 0 találatos lekérdezés is dataset-lefedettséget bizonyít, de nincs
hozzá `elofordulasok` sor, amelyben a proveniencia elférne.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | motívum-id | ✔ | Idegen kulcs a `motivumok.tsv`-re. |
| `lepes` | zárt: `A5` \| `B2` \| `B3` \| `B4` \| `adhoc` | ✔ | A `MUNKAMENET.md` lépés-kódja, amely a lekérdezést futtatta; az `adhoc` a kutatási lépésen kívüli lekérdezés (felmérés, pilot; DT-M3). A `B3` a mező-hipotézis támasztó lekérdezése (`lekerdez.py domen`) — maga a hipotézis kézi, sort nem kap (TEREMT002_KUTATAS_BRIEF.md, D2, 2026.09.25). |
| `proveniencia` | `PROVENIENCIA` | ✔ | A `lekerdez.py` utolsó sora **szó szerint**, a `proveniencia: ` előtag nélkül — l. 1.5. |
| `datum` | `DATUM` | ✔ | |

Minden A5/B2/B3/B4-lekérdezés sort kap, **0 találatnál is** — a nyom a
lekérdezéshez tartozik, nem a találathoz. A lefedett dataset a `proveniencia`
`forras` kulcsából **származtatott**: a `+` mentén bontott fájlnevek, a
`datasetek.tsv` `fajl` mezőjének alapnevével pontos egyezéssel (nem
részsztring — l. 3.8 indoklása). A `lexikai-scan` subagent a proveniencia-sort
amúgy is szó szerint adja vissza; a rögzítés a fő szál feladata, nem a
subagenté.

**Önnaplózás (F61, DT102).** A `lekerdez.py --naplo ID --lepes KÓD <alparancs> …`
(a két kapcsoló az alparancs előtt és után is állhat) az alparancs kimenete után
maga hozzáfűzi a sort; a `--lepes` ilyenkor kötelező, zárt értékkészlete
`A5 | B2 | B3 | B4 | adhoc`. A `--naplo` ID három ágon dönt:

| `--naplo` ID | Célfájl |
|---|---|
| létező motívum a `motivumok.tsv`-ben | `adat/auditok.tsv` (ez a tábla) |
| feladatkód (`^F\d+$`) | `naplok/<KÓD>_lekerdezesek.tsv`, azonos oszlopokkal (`id lepes proveniencia datum`) — a motívumszintű 1. és 8. szabály így nem érinti |
| minden más | hiba, `exit 1`, semmi nem íródik |

Csak hozzáfűzés; az azonos (`id` + `lepes` + `proveniencia`) sort nem veszi fel
kétszer; írás előtt az utolsó sor sorvégét és oszlopszámát ellenőrzi; hibás
lekérdezésnél (nincs proveniencia-sor) nem ír. `--naplo` esetén a kiírt
proveniencia-sor végére a `csatorna=cli` kulcs kerül (a futtatás csatornája),
és a naplósor ezt szó szerint tartalmazza; kapcsoló nélkül a kimenet változatlan.
A `csatorna` az `ellenoriz.py` megengedett további proveniencia-kulcsai között van
(`strong`, `n`, `csatorna`). A `# napló: …` állapotsor a stderr-re megy, így a stdout utolsó
sora `--naplo` esetén is a proveniencia-sor. A `naplok/*_lekerdezesek.tsv` formai ellenőrzése külön tétel.

**Commitolási szabály (DT103).** Az `ellenoriz.py` 8. szabálya nem nézi a `lepes` mezőt: egy
motívum-ID első `auditok.tsv`-sora — bármely lépésé, nem csak az `adhoc`-é — SÉRTÉST ad, amíg a
motívum „mindig”-datasetjeinek teljes lefedése nincs meg. Egy motívum auditsorai ezért csak a
teljes lefedés után commitolandók; a motívum lekérdezései nem vándorolnak feladatnaplóba.

### 2.10 `forditas_ubs.tsv` — **megszűnt (SZOTAR S1.1, 2026.09.28)**

Ez a tábla 2026.09.28-tól nem létezik — a tartalma (UBS DNTG/Louw–Nida
jelentések magyar fordítása) az `adat/forditasok.tsv`-be költözött (l.
2.14), `szotar=UBS_DNTG`, `entry_id`=a régi `lexid`, `jelentes_szam`=a régi
`entry_kod`, `mezo`=`definicio_hu` vagy `glosszak_hu`. A lookupot a
`lexikon_general.py` `ubs_jelentes_cella()` végzi a `forditas_ehhez()`
függvényen keresztül. Az alábbi (törölt) séma csak történeti hivatkozásul
marad:

Kulcs (volt): `strong` + `entry_kod`.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `strong` | `STRONG` | ✔ | |
| `entry_kod` | szabad szöveg | ✔ | Louw–Nida domén.alszám (pl. `33.176`) — ma az `adat/forditasok.tsv` `jelentes_szam` mezője. |
| `lexid` | szabad szöveg | ✔ | A `UBS_DNTG_jelentesek.tsv` `lexid` mezője — ma az `adat/forditasok.tsv` `entry_id` mezője. |
| `definicio_hu` | szabad szöveg | ✔ | A `definicio_rovid` hű magyar fordítása. |
| `glosszak_hu` | szabad szöveg | ✔ | A `glosszak` hű magyar fordítása, pontosvesszővel elválasztva. |
| `megjegyzes` | szabad szöveg | | Csak akkor töltött, ha a forrás UBS-definíció `{N:0..}` lábjegyzet-hivatkozást tartalmaz — ilyenkor `forrásban {N:001} lábjegyzet` (a lábjegyzet szövege nem kerül be a táblába, csak a generált oldal jelöli a hiányt). **Az `adat/forditasok.tsv` is felvette ezt a mezőt (l. 2.14) — a 4 érintett sor (G1311/88.266, G1944/33.475, G5351/88.266, G5590/9.20) jegyzete átkerült** (`NYITOTT_FELADATOK.md` N34, lezárva). |
| `proveniencia` | `PROVENIENCIA` | ✔ | `forras=UBS_DNTG_jelentesek.tsv \| forditas=chat-jovahagyas <dátum>` — ma az `adat/forditasok.tsv` `datum` mezőjeként őrződik meg (a `forditas=chat-jovahagyas ` előtag nélkül). |

Üres UBS-fordítás a generált lexikon-oldalon mindig `fordítás függőben`
jelölést kap, sosem üres cellát.

### 2.11 `lxx_dontesek.tsv` — kutatói LXX-fordítói döntések (LEXV2_2_BRIEF.md V2.2, G5)

Kulcs: `id`. Kézzel bővítendő tábla, csak azokra a versekre, ahol a motívum
saját G-tokenje **nem** fordul elő a `konkordancia/LXX_OS` adott versében
(„eltérő" eset) — a héber→görög megfelelőt ilyenkor gépi tippelés helyett ez
a tábla adja. Automatikus héber→görög tippelés nincs (l. 0. Kiindulás:
`HebrewStrong.xml` 0/8674 szócikke tartalmaz görög Strong-számot).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | szabad szöveg | ✔ | Sorazonosító (nem motívum-ID). |
| `igehely` | `IGEHELY` | ✔ | Károli-igehely. |
| `lxx_igehely` | szabad szöveg | ✔ | Az `LXX_OS` szerinti igehely (pl. `Genesis 4:26`). |
| `heber_strong` | `STRONG` | ✔ (tematikus sornál üres) | A motívum héber Strong-tokenje, amelyre a döntés vonatkozik (az `elofordulasok.tsv` motívum-sorának `strong` mezője; ha a versben álló szó saját Strong-ja eltér, a `megjegyzes` jelzi). `nincs_heber_kulcsszo`-nál üres, ha az előfordulás-sor tematikus (nincs Strong). |
| `gorog_lemma` | szabad szöveg | `eltero_forditas`-nál ✔, `lxx_minusz`-nál, `nincs_heber_kulcsszo`-nál és `nyitott` sornál üres | A kutatói azonosítású görög megfelelő lemmája (ékezetes szóalak); `lxx_minusz`-nál nincs mit megadni (nincs görög megfelelő). `nyitott` sornál a jelölt csak a `megjegyzes`-ben áll. |
| `gorog_strong` | `STRONG` | | A görög Strong-szám, ha van. |
| `lxx_pozicio` | egész szám | | Az `LXX_OS` adott sorának `pozicio` mezője, ha a szóalak egyértelműen egy adott előfordulásra mutat. |
| `tipus` | zárt | ✔ (`nyitott` sornál üres) | `eltero_forditas` (a LXX más görög szóval fordítja, mint amit a motívum ÚSZ-i G-tokenje várna) \| `lxx_minusz` (a héber tagmondatnak/szónak nincs görög megfelelője a LXX-ben — LXX-minusz) \| `nincs_heber_kulcsszo` (F08: az ige-tartományú előfordulás-sor e versében nem áll a motívum héber kulcsszava, vagy a sor tematikus; LXX-döntés tárgytalan). A generált lexikon-oldal 3. szakasza `lxx_minusz`-nál „nincs megfelelő a görögben (LXX-minusz)" szöveget ír a Görög megfelelő cellába (LEXV2_2_BRIEF.md V2.6a G6). |
| `megjegyzes` | szabad szöveg | | Indoklás/forrás a döntéshez. |
| `bizonyossag` | zárt | | F08 (F08_LXX_DONTESEK_BRIEF.md 3. lépés): `biztos` (két független forrás egyezik: a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű versében ugyanaz a lemma a héber szó helyén) \| `valoszinu` (egy forrás, ellentmondás nélkül, vagy ellentmondásos források, felhasználói döntéssel feloldva (`feloldas=` kötelező)) \| `nyitott` (nincs forrás, vagy a források ellentmondanak — a munkalap-szóra vonatkozóan is, ha a Macula a verset csak részben illeszti; `tipus` és `gorog_lemma` üres) \| `nem_alkalmazhato` (csak és kizárólag `nincs_heber_kulcsszo` típusnál: a skála nem értelmezhető, mert nincs LXX-megfelelő, amit forrás igazolna). Üres: az F08 előtti kutatói döntés (LD001–LD004), a skála nélkül. |
| `proveniencia` | `PROVENIENCIA` | ✔ | F08: felhasználói döntéssel kitöltött sornál `dontes=<DT-tétel>(<pont>)`; ellentmondásos forrásoknál `feloldas=<DT-tétel>` (l. alább). |

**Ellentmondó források (F08, DT23; az `ellenoriz.py` 10. szabálya):** egy sor
forrásai akkor ellentmondók, ha a `bizonyossag` `valoszinu`, és a
proveniencia `forras=` mezője a két független forrást — `Macula_heber` **és**
`LXX_OS` — egyaránt felsorolja. (Két egyező forrás `biztos` lenne; ha mindkettő
szerepel, de a sor csak `valoszinu`, a források a munkalap-szóra nem egyeztek.)
Ilyen sornál a `feloldas=` mező kötelező, és a `megjegyzes`-nek ki kell mondania
az ellentmondást („ellentmondott”). **Nem ellentmondás**, ha a Macula az adott
szót nem illeszti (’’): ez hiányzó forrás, nem ellenkező állítás — az ilyen sor
`forras=` mezőjében a két független forrás közül csak az `LXX_OS` áll (pl.
LD021, LD048; LD050: `LXX_OS` + `Karoli_versmegfeleltetes`).

Ebben a körben (V2.2) a tábla csak fejlécet tartalmaz — a tartalmi feltöltés
a 2. kör (V2.8, ISTENTISZT-001 LXX-döntések) tárgya.

**F08 (FELADATOK #8):** a 87 függő igehely (`naplok/F17_87_hely.tsv`) 86 sort
kapott (LD005–LD090; a 4Móz 13:34 a HODIT-001 és a MENNY-001 közös sora); a
bemenet `naplok/F08_bemenet.txt`, a szkript `eszkozok/f08/f08_dontesek.py`.
A generátor (`eszkozok/lexikon_general.py`, `lxx_dontesek_index`) csak az üres
vagy `biztos` bizonyosságú, `eltero_forditas`/`lxx_minusz` típusú sorokat
jeleníti meg; a `valoszinu`/`nyitott`/`nem_alkalmazhato` sorok „kutatói
azonosítás függőben” jelöléssel jelennek meg (DT23; a `nincs_heber_kulcsszo`
sorok saját címkéje: N-F08b).
A szűrő a 3. (LXX) blokkon túl a „Rokon szavak” blokkot is érinti
(`rokon_szavak_strongok` a megjelenő sorok `gorog_strong`-jait olvassa).

---

### 2.12 `res_forras.tsv` — rés-forrás megfeleltetés (RENDER_BRIEF.md R1.1)

Kulcs: `id` + `res`. A lexikonoldal (`_TUDOMANYOS.md`) kilenc rése
(`kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`,
`alkalmazas`, `tanitoi`, `modszertan`) motívumonkénti és résenkénti forrása — a
render-elv szerint a rés törzse nem a lexikonoldalon él, hanem a tanulmányban
(RENDER_BRIEF.md G1).

Az `alkalmazas` és a `tanitoi` rés a DT276 (#127) óta él: a lap „6/b. Alkalmazás
és tanítói egyezés” szakaszában állnak, a 6. Értelmezés után (a szakaszszámozás
nem tolódik). Az `alkalmazas` forrása a motívum kézi forrásának „5. Alkalmazás és
tanítványság” pontja, a `tanitoi` forrása a 7. lépés saját fájljának
(`motivumok/naplok/[ID]_tanitoi_kereses.md`) „Összegzés” szakasza — mindkettő a
meglévő jelölő-mechanizmussal, saját sorral. A még nem migrált motívumoknál
`forras=adat`, rögzített átmeneti mondattal; a jelölőket a #123 ciklusai teszik a
forrásba. A törzscikkben (`_TORZSCIKK.md`) a két rés nem jelenik meg (D34).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | szabad szöveg | ✔ | Motívum-ID (`motivumok.tsv` kulcsa). |
| `res` | zárt | ✔ | `kivonat` \| `2b` \| `miert_fontos` \| `minosites` \| `alatamasztas` \| `ertelmezes` \| `alkalmazas` \| `tanitoi` \| `modszertan` (az utolsó előtti kettő: DT276). |
| `fejlec` | szabad szöveg | ✔ | A rés fejlécsora a lexikonoldalon, szó szerint (RENDER_BRIEF.md G2/G4 — a `VAZ_SABLON` induló fejléce; a nulla-diff ezt bájtra megőrzi). |
| `forras` | zárt | ✔ | `lap` (a lexikonoldal mai, kézzel írt rése, változatlanul — átmeneti, RENDER_BRIEF.md G12) \| `tanulmany` (a `tanulmany` mezőben megadott fájl `<!-- RÉS-KEZDET: [res] -->…<!-- RÉS-VÉGE: [res] -->` jelölői közötti törzse) \| `adat` (a generátor adatból írja, pl. 0 kapcsolatnál az `alatamasztas`, RENDER_BRIEF.md G16). |
| `tanulmany` | szabad szöveg | `forras=tanulmany`-nál ✔, egyébként üres | A forrásfájl relatív útvonala — a motívum tematikus tanulmánya (`tematikus_lezart/*.md`) vagy — a `minosites` résnél — a kereszthivatkozás-napló (`tematikus_lezart/naplok/*.md`), RENDER_BRIEF.md G14; a migrált motívumnál (#11, D34) a motívum kézi forrása (`motivumok/[ID].md`), a `tanitoi` résnél pedig a 7. lépés saját fájlja (`motivumok/naplok/[ID]_tanitoi_kereses.md`, DT276). `forras=adat`-nál: ha nem üres, a rés törzse maga ez a rögzített mondat (G16); ha üres, a generátor az adattáblából rendereli (F11 R, DT216): `alatamasztas` ← `kapcsolatok.tsv` `indoklas` (2.3), `2b` ← a `lexikon_hivatkozasok.tsv` szerephez nem rendelt (`SECE_G`, `SECE_H`, `MCGED`) sorai a motívum Strong-tokenjeire (2.5; ezeket a szerepmátrix nem rendereli), `minosites` ← `jeloltek.tsv` (a TSK / Károli-KH `forras_kereses`-ű sorok) + a független megerősítés (TSK Votes ≥ 15 / Károli-KH ∩ a motívum előfordulás-igehelyei, 3.10.7 2.). Üres adatnál kimondott hiánymondat; más rés üres mezővel hiba. Az így generált rés törzse elöl `<!-- GENERÁLT-RÉS: [rés] \| general.py --cel lexikon \| forrás: … -->` jelölőt, a végén proveniencia-sort (`scope=id:[ID] \| forras=… \| ts=…`) kap, a `fejlec` pedig `*(generált)*` végű (a határkeresés a régi `*(kézi)*` alakot tartalékként elfogadja). |

A tábla `forras=lap` sorainál a `tanulmany` mező üres: az 1. menetben a 7
helyőrzős lexikonoldal mind a 49 rése `lap` forrású (RENDER_BRIEF.md G12); a
2. menet végére minden sor `tanulmany`-ra vált (a `lap` érték eltűnik).

---

### 2.13 `szotar_szerepek.tsv` — szótári szerepmátrix (RENDER_BRIEF.md R1.5, G6)

Kulcs: `nyelv` + `sorrend`. 13 szerep × 2 nyelv = 26 sor, statikus tábla (nem
motívumonkénti): melyik szótári forrás felel meg egy adott „kérdéstípusnak"
(pl. „Alapjelentés", „Mélységi szócikk") mindkét nyelven, és a forrás ma
adatosítva van-e a projektben.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `nyelv` | zárt | ✔ | `gorog` \| `heber`. |
| `sorrend` | egész szám | ✔ | 1–10, 12, 13 és 14, a szerep-lista rögzített sorrendje (azonos mindkét nyelven); a 11-es érték nincs kiosztva. A 12. a „Tematikus index” (Nave, F18, DT29 (j)); a 13. a „Károli-megfelelők (+ SZPA)”, a 14. a „Rejtett / hamis párhuzam” (F78, DT-M4 = DT76 (9); mindkettő nyelvfüggetlen, a 12. mintájára két sor, `javaslat` állapottal, amíg a #22 nem teljes; a 14. a 13.-ból származtatott lekérdezés, a render külön blokkja); az első 10 az eredeti szerepkészlet. |
| `szerep` | szabad szöveg | ✔ | A szerep megnevezése (pl. „Alapjelentés", „LXX-híd"). |
| `forras` | szabad szöveg | ✔ | A szerepet ma (vagy célként) kitöltő forrás megnevezése. |
| `allapot` | zárt | ✔ | `adatosítva` \| `nincs adatosítva` \| `nincs forrás` \| `javaslat` (F05_SZOTAR_BRIEF.md D27, S1.6; `javaslat`: F18.12, DT29) — a RENDER_BRIEF.md G6 záró bekezdése szerint: adatosítva a TBESG, TBESH, Thayer, BDB, UBS DNTG (a meglévő import), SDBH domének, LSJ és az LXX-híd (mindkét irány); a többi (Girdlestone, UBS DBH glossza+referencia, Mounce-kiegészítő önmagában, SECE, BDB-etimológia, kiejtés) a `F05_SZOTAR_BRIEF.md` tárgya. **`nincs forrás`** (D27): a szerepnek az adott nyelven nincs a D17 forrásszabálynak megfelelő forrása — VÉGLEGES állapot, nem pótlandó hiány (szemben a `nincs adatosítva`-val, amely ígéretet sugallna); pl. a görög 3. szerep, ha a Translation Words elutasításra kerül (S0b.2 küszöbe alatt). **`javaslat`** (F18.12): az adat a repóban van, de teljessége/helyessége független igazolással nincs megerősítve (a 12. „Tematikus index” szerep, a Nave-import, l. `naplok/F18_import_naplo.md`; a 13. és 14. szerep, F78 / DT-M4: az adat még nincs meg, a #22 Károli–Strong párosítás nem teljes — a sor a mátrix metaadata, nem adatosítás); a generátorok ezt nem adatosítottnak kezelik (csak az `adatosítva` érték számít adatosítottnak). |

A törzscikk (`_TORZSCIKK.md`) 5. szakaszának szerep-mátrixa ebből a táblából
épül; a lefedettségi mátrix (szavanként) a belső adatmodellből (G5).

### 2.14 `forditasok.tsv` — fordítási gyorsítótár (F05_SZOTAR_BRIEF.md S1, S1.1)

Kulcs: `szotar` + `strong` + `entry_id` + `jelentes_szam` + `mezo`. Minden
magyar szótári fordítás egyetlen helye — a `lexikon_hivatkozasok.tsv`
`forditas_hu` oszlopát (l. 2.5) és a megszűnt `forditas_ubs.tsv`-t (l.
2.10) váltja fel, egységes sémában, amely megegyezik az `eszkozok/fordit.py`
`KIMENET_FEJLEC` kimenet-oszlopaival — a jövőbeli gépi fordítás (FELADATOK
#7) ugyanide ír majd.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `szotar` | szabad szöveg | ✔ | A 2.5 `szotar` zárt listája (BDB, TBESH, TBESG, Thayer, LSJ, …), **plusz** `UBS_DNTG` a megszűnt `forditas_ubs.tsv` soraihoz. |
| `strong` | `STRONG` | ✔ | |
| `entry_id` | szabad szöveg | ✔ | `szotar=UBS_DNTG` esetén a `UBS_DNTG_jelentesek.tsv` `lexid` mezője (a régi `forditas_ubs.lexid`); egyébként azonos a 2.5 `entry_id` értelmezésével. |
| `jelentes_szam` | union (l. 2.2.2) | ✔ | `szotar=UBS_DNTG` esetén a Louw–Nida `entry_kod` (pl. `33.176`, a régi `forditas_ubs.entry_kod`); egyébként azonos a 2.5 `jelentes_szam` értelmezésével. **Szakaszonkénti BDB-sor (F128, DT285 (a)):** `sz<sorszam>`, a `adat/bdb_szakaszok.tsv` (2.30) `sorszam`-a (pl. `sz12`); egy szakasz egy sor, a Strong teljes magyar szövege nézet (l. lent). |
| `mezo` | zárt | ✔ | Melyik forrásmezőt fordítja ez a sor: `forditas_hu` (a 2.5 `szoveg_en`-jét), `definicio_hu` vagy `glosszak_hu` (a régi `forditas_ubs.tsv` két oszlopa). |
| `forras_hash` | szabad szöveg | ✔ | A forrásszöveg (az eredeti nyelvű, EN) SHA-1 hexdigestje (`hashlib.sha1(szoveg).hexdigest()`), UTF-8 kódolásból. Eltérés a forrás-hash és az újraszámolt hash között `ellenoriz.py`-sértés (S1.5, 13. szabály). A forrásszöveg a `lexikon_hivatkozasok.tsv` `szoveg_en`-je (UBS-nél a `UBS_DNTG_jelentesek.tsv`); ha ott nincs sor, és a sor `szotar ∈ {Thayer, BDB}`, `jelentes_szam=teljes`, `mezo=forditas_hu`, akkor a `konkordancia/Thayer_teljes.tsv` / `BDB_teljes_unabridged.tsv` `Teljes_szocikk` mezője (kulcs: `strong` → `Strong_padded`, az `entry_id`-nek a `Strong_eredeti`-vel kell egyeznie; F28 DT24 (b)). **Az `sz<n>` sor (F128, DT286 (1)):** a fordítónak átadott szakaszszöveg SHA-1-e: a 2.30 sor `jel` + `szoveg`-e egy szóközzel, a 2.31 `hivatkozas` / `javitva` javításaival, pe/mem csere és határtoken nélkül (`eszkozok/bdb_jelolt/szakasz_bemenet.py`, `szakaszok()[i].hash`). A 674 régi `teljes` BDB-sor a TSV-alapon marad (674/674 egyezik, F128 M0); a két alap a `jelentes_szam`-ból válik el, a TSV-cseréig (DT231 (d), DT269 (1)). |
| `forditas_hu` | szabad szöveg | ✔ | A fordítás szövege — ugyanaz a tartalmi szabály, mint a 2.5-ben leírt `forditas_hu`-nál. |
| `allapot` | zárt | ✔ | `kezi` (a migrált, ember által korábban jóváhagyott sorok; az F28-ban a felhasználó által jóváhagyott Opus-fordítás) \| `opus` (a teljes Thayer-/BDB-szócikk Opus-fordítása, kapukon átment, emberi jóváhagyás nélkül, l. `F28_EMELES_BRIEF.md` E4) \| `sonnet` (a teljes Thayer-/BDB-szócikk Sonnet-fordítása, kapukon átment, emberi jóváhagyás nélkül; F38, DT-F38e) \| `pilot` (az `eszkozok/fordit.py` próba-kimenete, l. `F03_FORDITAS_PILOT_BRIEF.md`) \| `elavult` (a `forras_hash` már nem egyezik, `ellenoriz.py` javaslata). **F128 (DT289):** a szakaszonként újrafordított Strong régi `teljes` sora nem törlődik, hanem `elavult` lesz, a `megjegyzes` a felváltást jelöli (`emeles.py szakasz_beir --regi-elavult`); `kezi` régi sor csak `--kezi-felulir`-ral (a H8415-ről a DT290 dönt). |
| `modell` | szabad szöveg | | A fordító LLM modell-azonosítója (pl. `anthropic/claude-haiku-4.5`); üres, ha `allapot=kezi` és nem model-fordítás. Az F28 jóváhagyott (`kezi`) Opus-fordításainál kitöltve marad (`claude-opus-5-5`); az F38 `sonnet` soraiban a Sonnet modell-azonosítója (`claude-sonnet-5-5`). Az `emeles.py rogzit --modell` kötelező (nincs alapérték): a címke a ténylegesen fordító modellt jelöli (F38.265) — a jóváhagyás az állapotot változtatja, a provenienciát nem. |
| `datum` | `DATUM` | ✔ | A migrált soroknál a forrás utolsó tartalmi módosításának git-dátuma (a `lexikon_hivatkozasok.tsv` soraira) vagy a korábbi `forditas_ubs.proveniencia` jóváhagyási dátuma (az UBS-soroknál); új soroknál a fordítás dátuma. |
| `terminologia_verzio` | szabad szöveg | | A 2.15 `terminologia.tsv` verziója, amellyel a fordítás készült; üres a migrált (a terminológia-tábla előtti) soroknál. |
| `megjegyzes` | szabad szöveg | | A megszűnt `forditas_ubs.tsv` `megjegyzes` oszlopának öröksége — lábjegyzet-hivatkozás vagy a fordítói döntés indoklása. A render nem olvassa (csak emberi/archív jegyzet); üres a legtöbb sornál. |

**Szakaszonkénti BDB-sorok (F128; DT181 (b), DT269 (1), DT285–g).** A #38 a 7. adag előtti újrafordító adagtól
(DT289: a 98 N-F107b Strong) szakaszonként fordít: a bemenet a `szakasz_bemenet.py` tokenes szövege (minden szakasz előtt
`⟪<sorszam>⟫`), a prompt `forditas/prompt_v5.md`, a rögzítés `emeles.py szakasz_rogzit` → `szakasz_beir`. Egy Strong nem
`elavult` `sz<n>` sorai együtt a Strong összes szakaszát lefedik (a `szakasz_beir` és a 13. szabály ellenőrzi). **A Strong
magyar szövege nézet:** a közös összefűző (`szakasz_bemenet.strong_magyar` / `strong_magyar_sorok`) a nem `elavult` `sz<n>`
sorokat sorszám szerint, egy szóközzel fűzi össze; ha ilyen nincs, a `teljes` sort adja (a nem `elavult` elsőbbséggel). **A
jóváhagyott sor elsőbbsége (DT290 (3)):** ha a Strongnak nem `elavult`, `kezi` `teljes` sora van (H8415), az az érvényes,
amíg a szakaszsorok nem mind `kezi`-k; a nem `kezi` szakaszsorok mellé `szakasz_beir --kezi-marad` (a régi sor érintetlen), a
jóváhagyott (`--allapot kezi`) szakaszsorokhoz `--regi-elavult --kezi-felulir` (ekkor lesz a régi `elavult`). **Az olvasók
(DT291 (a), F128.10–.14) ezt az összefűzőt használják:** az olvasó szerver `bdb_magyar` / `bdb_magyar_meta`
(`olvaso_szerver/lekerdezesek.py`; a meta a felhasznált sorok modelljei és legkésőbbi dátuma), a `hu_illeszt.py` (2.32), a
`bdb_adatblokk.py --karoli-epit` kész halmaza (`teljes` vagy `sz<n>` sor); a 13. szabály (`ellenoriz.py`, CI E1) az `sz<n>`
sor forrásszövegét a szakasztáblából veszi (a `forras_hash` fenti alapja). A #60 pilot (`olvaso_pilot/adat.py`) nincs
átállítva (csak újragenerálásnál számít; DT291 (a)). A 9 táblán kívüli Strong (H0747, H1753, H3367, H3848, H4123, H4725, H6433, H7560, H8065) és a Thayer a régi
`teljes` úton (prompt v4) fordul (DT288 (2)); a `reszleges` / `sikertelen` / `csonk` illesztésű Strong is szakaszonként.

**Thayer `sz<n>` sorok (F132, F145; DT353).** A Thayer a #132 óta szakaszonként is fordul (`eszkozok/thayer_jelolt/forditas.py`, prompt
`forditas/prompt_v5_1.md`); az `sz<n>` sor `forras_hash`-e a `thayer_bemenet.szakaszok()[i].hash`: a 2.34 sor `jel` + `szoveg`-e egy szóközzel, a 2.38 `javitva`
beszúrásaival. A 13. szabály (`ellenoriz.py`) a `szotar = Thayer`, `sz<n>` sor forrásszövegét ebből veszi (az `entry_id` a Strong eredeti alakja, `G86`), és a
nem `elavult` `sz<n>` sorok lefedettségét a BDB-vel azonos módon ellenőrzi. A CI **E19** (`szabalyok.py`) a `lexikon_hivatkozasok.tsv` `jelentes_szam = teljes`
sorát fedettnek veszi, ha a Strongnak (szótár + strong + entry_id) a szótár összes szakaszát lefedő, nem `elavult` (`opus` / `sonnet` / `kezi`) `sz<n>` sorai vannak
(a szakaszkészlet a 13. szabályéval azonos forrásból, a 2.30 / 2.34 táblából); részleges lefedettség nem fed.
A hívás egysége (DT287 (2)): 20 000 karakterig a Strong egészben, fölötte ≤ ~10 000 karakteres szakaszcsoportok
tokenhatáron. A kapuk: a 14. szakasz-kapu (`forditas_kapuk.ellenoriz_szakasz`), a 9. tagolás szakaszonként, a többi a token
nélküli szövegen (`kapuk_futtat_szakaszos`).

**Migráció (S1.1, 51 sor):** 11 sor a `lexikon_hivatkozasok.tsv` akkor
töltött `forditas_hu` celláiból (`mezo=forditas_hu`), 40 sor a megszűnt
`forditas_ubs.tsv`-ből (20×`definicio_hu` + 20×`glosszak_hu`). A megszűnt
`forditas_ubs.tsv` `megjegyzes` oszlopa (4 sor: G1311/88.266, G1944/33.475,
G5351/88.266, G5590/9.20) a `megjegyzes` mezőben őrződik meg, mindkét
származó soron (`definicio_hu` és `glosszak_hu`) — l. `NYITOTT_FELADATOK.md`
N34 (lezárva).

### 2.15 `terminologia.tsv` — fordítási terminológia (F05_SZOTAR_BRIEF.md S2, D26)

Kulcs: `angol` + `verzio`. Kézzel bővítendő tábla: angol szakkifejezések és
rövidítés-feloldások rögzített magyar megfelelője, amelyet az
`eszkozok/fordit.py` (és a jövőbeli élesített gépi fordítás, FELADATOK #7)
a fordítói promptba fűz be, hogy a fordítás konzisztens maradjon szótárak
és futások között.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `angol` | szabad szöveg | ✔ | Az angol szakkifejezés vagy rövidítés, ahogy a forrásszótárban áll (pl. `cf.`, `spirit`). |
| `magyar` | szabad szöveg | ✔ | A rögzített magyar megfelelő. |
| `megjegyzes` | szabad szöveg | | A feloldás indoklása vagy eredete (pl. melyik próbafuttatásból igazolódott). |
| `verzio` | `v<N>` | ✔ | A terminológia-tábla verziója; a `forditasok.tsv` `terminologia_verzio` mezője erre mutat. |
| `kapu` | `igen` / `nem` | | DT27: ellenőrzi-e a fordítási kapu (`eszkozok/forditas_kapuk.py`, 5. terminológia) a sort. `nem`: a sor a fordítói promptba bekerül, de a kapu nem követeli meg a magyar alakot — azoknál a soroknál, amelyek forrásbeli angol alakja nem egyértelmű kulcs (szórend, minta, többjelentésű szó). Hiányzó vagy üres érték: `igen`. A `forditasok.tsv` 14. szabálya (`ellenoriz.py`, verzió-elmaradás) ettől független. |

A pontos kulcsolásban (l. a v3 bekezdést) csak a `kapu=igen` hosszabb kulcs vonja el
a rövidebb kulcs előfordulásait; a `kapu=nem` hosszabb kulcs (pl. `which see`)
belsejében álló rövidebb előfordulás (`see`) a rövidebb, `kapu=igen` soré marad, így
egy `kapu=nem` sor nem vehet ki a kapu alól ellenőrzött sort (ELLENOR_DT27, F28.46). Az oszlop bevezetése (DT27) nem emelte a `verzio`-t:
a sorok tartalma nem változott, csak az ellenőrzésük módja.

**Induló tartalom (D26):** a `naplok/FORDITAS_P_terminologia.tsv` 13 sora,
változatlanul, `v1` verzióval.

**v3 (F28, DT26):** az emelés jóváhagyott szakkifejezései (alaktan, rövidítés-feloldások,
szerzőnevek, könyvnevek). Ha egy kulcs egy hosszabb kulcs része (`compare` ⊂ `מִן compare`),
a fordítási kapu (`eszkozok/forditas_kapuk.py`) a forrás hosszabb kulcson belüli
előfordulásait a hosszabbik sorhoz rendeli: a kulcs maga a forrásbeli alak, a
megkülönböztetés a kulcsban van, nem a kapu lazításában.

### 2.16 `kiejtes_szabalyok.tsv` — görög átírási szabálytábla (F05_SZOTAR_BRIEF.md S3)

Kulcs: `sorszam`. **Generált célra szolgáló, de kézzel karbantartott** tábla:
az `eszkozok/kiejtes.py` (S1.3) ebből olvassa a görög SBL-stílusú (Unicode
makronos) akadémiai átirat → magyaros kiejtés szekvenciális, literális
(nem regex) cseréinek rendezett listáját. A bemenet a `TAGNT_kivonat.tsv`/
`TBESG.txt` „Kiejtés” oszlopa.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `sorszam` | egész szám | ✔ | Az alkalmazás sorrendje — **kötelező betartani**, mert egyes szabályok csak egy másik szabály előtt/után helyesek (pl. a `z`→`dz` a `s`→`sz` előtt, az `ou`→`ú` a `u`→`ü` előtt). |
| `minta` | szabad szöveg | ✔ | A cserélendő literális Latin (SBL-átiratos) részstring. |
| `csere` | szabad szöveg | ✔ | A magyaros megfelelő. |
| `megjegyzes` | szabad szöveg | | A szabály indoklása, jellemző görög betű/eset, és — ha van — egy igazoló példa a `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` aranykészletéből. |

**Két eset NEM szerepel a táblában, kódszinten (`eszkozok/kiejtes.py`
`atir()`) van maszkolva, mert egy egyszerű szekvenciális csereként
tévesen viselkedne:** a σσ (dupla szigma) → `ssz` (a magyar geminációs
helyesírás miatt — a `s`→`sz` szabály a maszkolás nélkül a `ssz`-ben
bennmaradó két bare `s`-t újra feldolgozná), és az αυ/ευ diftongusok
`u`-ja (nem álló upsilon, nem válhat `ü`-vé — l. `καύχημα` → `kauchēma`
→ `kaukhéma`, nem `kaükhéma`).

**Állapot (S1.3, validálva):** a 24 sor az `eszkozok/kiejtes.py
--ellenoriz` szerint mind a 26 tesztelhető „arany” görög párt (a 30
egyedi párból 4 kontextus-függő kimaradt) hibátlanul adja vissza —
`naplok/SZOTAR_S1_kiejtes_jelentes.md`. **D32:** az S1.2-es első
változat tévesen `y`-t használt az upsilonra (ellenőrzés nélküli
feltételezésből); a tényleges forrás (`TBESG.txt`/`TAGNT_kivonat.tsv`)
sima `u`-t ad — javítva. A 100%-os egyezés önmagában nem elfogadási
érv — l. a jelentés lefedettségi és kihagyásos (leave-one-out) részét.

### 2.17 `kiejtes_kivetelek.tsv` — kiejtés-kivételek (F05_SZOTAR_BRIEF.md S3, D15)

Kulcs: `nyelv` + `alak`. Kézzel bővítendő/jóváhagyandó tábla, kettős
szereppel: **görögül** felülírja/kiegészíti a `kiejtes_szabalyok.tsv`
szabálytábla-alapú átirat egy-egy ismert, kivételes esetét; **héberül** ez
az EGYETLEN forrás — a render héber lemma-kiejtést sosem generál (S3).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `nyelv` | zárt | ✔ | `gorog` \| `heber`. |
| `alak` | szabad szöveg | ✔ | A forrás (SBL-átiratos vagy OSHL-átiratos) lemma vagy szó szerinti alak, amelyre a kivétel vonatkozik. |
| `kiejtes` | szabad szöveg | ✔ | A jóváhagyott magyaros kiejtés. |
| `megjegyzes` | szabad szöveg | | Eredet/indoklás (pl. `KIEJT-migracio`, vagy — héber jelölteknél, S1.7/S2.1 után — az OSHL-jelöltlista hivatkozása és a jóváhagyás dátuma). |

**Induló tartalom (S1.2):** az `eszkozok/torzscikk_general.py` kódbeli
`KIEJT` szótárának 5 sora (3 görög: `epikaleō`, `kaleō`, `boaō`; 2 héber:
`qa.ra`, `shem`) — a kódbeli `KIEJT` tábla ezzel párhuzamosan, változatlanul
megmarad (nulla-diff, D30/D31); a kódbeli tábla kivezetése az S2.1 tétele.
**A 26 héber lemma-kiejtés-jelölt (D28) az S1.7-ben készül, de csak az
ÁLLJ-jóváhagyás után, az S2.1-ben kerül ide.**

### 2.18 `kiejtes_heber_jeloltszabalyok.tsv` és `kiejtes_heber_kivetelek.tsv` — héber kiejtés-jelölt gépezet (F05_SZOTAR_BRIEF.md S1.7, D34–D37)

Két tábla, amelyek EGYÜTT állítják elő a `naplok/SZOTAR_S1_heber_jeloltek.tsv`
JELÖLT-listát (`eszkozok/heber_kiejtes_jeloltek.py`) — egyik sem a végleges,
render által olvasott `kiejtes_kivetelek.tsv` (2.17); abba csak kézi
jóváhagyás után, az S2.1-ben kerülnek be a jóváhagyott jelöltek.

**`kiejtes_heber_jeloltszabalyok.tsv`** — kulcs: `sorszam`. Szekvenciális,
literális (nem regex) csereszabályok az OSHL `atiras` mezőn (SBL Academic
stílus), a görög `kiejtes_szabalyok.tsv` (2.16) mintájára, de külön táblában
(eltérő ábécé, eltérő szabályhalmaz — aleph/ajin elhagyás, š/ṣ/ṭ/ḥ/q/y
átirata, hosszú/redukált magánhangzók).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `sorszam` | egész szám | ✔ | Az alkalmazás sorrendje — kötelező betartani. |
| `minta` | szabad szöveg | ✔ | A cserélendő literális OSHL-átiratos részstring — sosem üres (ez maga a keresett minta). |
| `csere` | szabad szöveg | | A magyaros megfelelő; üres, ha a `minta` egyszerűen törlődik (l. az aleph/ajin-szabályt). |
| `megjegyzes` | szabad szöveg | | A szabály indoklása, jellemző héber betű, igazoló példa. |

**A begadkefat-spirantizáció (ב/כ/פ → v/ch/f, D34) NEM ebben a táblában
van** — pozíciófüggő (dagesh/szókezdő helyzet), az OSHL `atiras` maga nem
jelöli, ezért a pontozott `oshl_lemma` mezőt elemző `spirantize()` lépés
(`eszkozok/heber_kiejtes_jeloltek.py`) végzi, a szabálytábla ELŐTT.

**`kiejtes_heber_kivetelek.tsv`** — kulcs: `strong`. Kézi felülbírálás,
amit a generátor a szabályfutás UTÁN alkalmaz (pl. H2555 → „hámás”, D36,
a `ḥ→ch` szabály gépies eredménye helyett).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `strong` | `STRONG` | ✔ | A felülbírált Strong-szám. |
| `ertek` | szabad szöveg | ✔ | A jóváhagyott magyaros kiejtés-jelölt. |
| `indok` | szabad szöveg | ✔ | Miért tér el a szabályszerű eredménytől. |
| `datum` | `DATUM` | ✔ | A döntés dátuma. |

**Ki írja, ki olvassa:** mindkét táblát kézzel bővíti a felhasználó (chat
jóváhagyással); egyedül az `eszkozok/heber_kiejtes_jeloltek.py` olvassa
őket. A render (`lexikon_general.py`/`torzscikk_general.py`) egyiket sem
olvassa — az S1.7 jelölt-lépés, nem az S2 render-lépés tartozéka.

### 2.19 `licencek.tsv` — licenc-leltár (F24, FELADATOK #24, D41)

Adatkészletenként **egy** sor; a licenc **adatkészlet-szinten** él, a sorszintű adat a
dataset-azonosítón át örökli (a sorszintű proveniencia nem változik). Ez a **leltár, nem jogi
vélemény**: kereskedelmi vagy nyilvános kiadás előtt jogásznak kell átnéznie.

**Ez a licenc egyetlen forrása.** Minden generált nézetnek (render, törzscikk, lexikonoldal,
nyilvános kiadás) ebből kell olvasnia; a licenc-besorolás másutt (kódkonstans, README-mondat)
legfeljebb tükör, és ha ellentmond, **ez a tábla az irányadó**. (A `lexikon_general.py` a licenc-állapotot és a rövid címkét innen olvassa; a `LICENC`-konstans és a
`TISZTAZATLAN_SZOTARAK` megszűnt: F42 / DT-F42g, N9 lezárva, l. lent.)

Kulcs: `dataset`. Fejlécsorok `#`-tel; olvasás `split('\t')`.

| Mező | Értékkészlet |
|---|---|
| `dataset` | a `datasetek.tsv` azonosítója, ha van ilyen; egyébként a konkordancia/ tábla- vagy forrásneve (`TBESH`, `LXX_OS`, `UBS_DBH`, `MCGED`, `tW_szocikkek`, ...); a szerepmátrix forrásai közül a nem importáltak is (`Girdlestone`); a projekt saját táblái a `projekt_adat` soron |
| `licenc` | a forrásdokumentum szerinti licenc, nevével és verziójával; `tisztázatlan` vagy a README állítása zárójeles jelöléssel, ha a forrásból nem igazolt |
| `verzio_vagy_commit` | rögzített commit, tag, sha256 vagy letöltési dátum; „commit nincs rögzítve”, ha tényleg nincs |
| `forras_hely` | a licenc pontos helye: a forrás fájlja/sora, vagy a repó README-jének sora, amely a forrás szövegét idézi. `tisztazott` sornál kötelező |
| `kereskedelmi` | `igen` \| `nem` \| `feltetelesen` \| `tisztazatlan` |
| `share_alike` | `igen` \| `nem` \| `tisztazatlan` |
| `kotelezo_megjeloles` | a kötelező forrásmegjelölés **szó szerint**, ha a forrás megad ilyet; egyébként üres |
| `allapot` | `tisztazott` (a licenc a forrás saját dokumentumából, megadott helyen igazolt) \| `kozkincs` (F33 / DT-F33d; feltételei a 2. szabályban) \| `tisztazatlan` |
| `megjegyzes` | tudnivaló; `javaslat:` kezdetű mondat = eltérés vagy javasolt teendő (nem döntés) |
| `cimke` | zárt (F42 / DT-F42g): a generált nézetekben megjelenő rövid licenc-címke; **kötelező minden sorra**. Értékek: `közkincs` \| `CC0 1.0` \| `CC BY 4.0` \| `CC BY-SA 4.0` \| `© Mounce 1993` \| `minden jog fenntartva` \| `tisztázatlan`. Szabály: `allapot=tisztazatlan` sor címkéje `tisztázatlan`; `tisztazott` és `kozkincs` sor címkéje a `licenc` oszlop szerinti rövid név. A `minden jog fenntartva` a projekt saját adatáé és prózáé (F89 / DT131, DT116): a `projekt_adat` soré, valamint azoké a származtatott soroké, amelyeknek a saját része ez (`Karoli_Strong_parok`, `Karoli_Strong_szavak`, `karoli_variancia`, `Karoli_Strong_kivonat`, `LXX_versszintu_parok`, `Karoli_versmegfeleltetes`); a harmadik fél komponenseire a `licenc` oszlop és a komponens-sorok vonatkoznak. A korábbi `projekt-adat` címke megszűnt. Új típusú licencnél a címke-értékkészlet bővítése SEMA-változtatás. A tábla **utolsó** oszlopa. |

**Két bővítés a briefhez képest.** A `kereskedelmi` és a `share_alike` oszlop a
`tisztazatlan` értéket is felveszi: egy ismeretlen licencű forrásnál sem `igen`, sem `nem`
nem állítható (CLAUDE.md 3. szabály, a hiányt nem töltjük ki). A `feltetelesen` a
licenc-szövegen túli feltételt jelöl (pl. védjegy-szabály, UK Crown-jog).

**Szabályok.**

1. A `share_alike = igen` sorok (CC BY-SA: SDBH, SDGNT, UBS_DBH, UBS_DNTG,
   SDBH_SDGNT_segedtablak, tW_szocikkek, LSJ; hét sor, mind `tisztazott`; az LSJ: Perseus saját nyilatkozata, CC BY-SA 4.0, 2026.10.04) megjegyzése rögzíti: a belőlük
   származó réteg nem zárható el, a kiadásban külön jelölendő. A kereskedelmi használat
   itt `igen` (a CC BY-SA megengedi), de a ShareAlike a származékos munkára is kiterjed.
2. `tisztazott` csak akkor, ha a `forras_hely` a licenc szövegére vagy a forrás saját
   állítását szó szerint idéző repó-fájlra mutat. A szerző forrásoldalából (másodkézből)
   átvett állítás `tisztazatlan`, a README-állítással a `licenc` oszlopban.
   **F33 / DT-F33c pontosítás (felhasználói döntés, 2026.10.02):** a forrásrepó README-je akkor fogadható el,
   ha a JOGTULAJDONOS szó szerinti licencnyilatkozata a saját adatára, és megnevezi vagy egyértelműen
   lefedi az adott fájlt. Harmadik fél licencének továbbadása vagy összefoglalása nem bizonyíték.
   A `tisztazott` sor megjegyzése nem mondhat ellent az állapotnak.
   **`kozkincs` (F33 / DT-F33d, felhasználói döntés, 2026.10.02; ékezet nélkül):** csak akkor, ha (a) a mű kora miatt
   közkincs, (b) a használt digitális kiadás azonosítva van (forrás + commit/URL/sha256), és (c) a kiadásnak nincs saját
   licencigénye, vagy a kiadás készítője maga nyilvánítja közkincsnek (szó szerint idézve a `forras_hely`-ben). Ha (c)
   nem igazolt: `tisztazatlan`. A `kozkincs` sor `kereskedelmi`/`share_alike` értéke a megszokott értékkészletből való
   (a kor miatti közkincs mellett lehet külön feltétel, pl. UK Crown-jog: `feltetelesen`).
   **DT-F33e (felhasználói döntés, 2026.10.04), a (c) szűkítő kivétele:** a **Károli 1908-as szövegére** (`Karoli_1908`,
   `Karoli_KH`) a (c) feltétel nem követelmény: a szöveg a mű kora miatt közkincs, a magyar jogban evidens, kiadói
   nyilatkozat nincs, és nem is kérendő. A kivétel erre a műre szól, más sorra nem általánosítható.
   **DT-F33f (felhasználói döntés, 2026.10.04), második kivétel:** a **TBESH** sorra (a `Meaning` oszlop Online Bible-eredetű
   tartalmát is beleértve) a `tisztazott` állapothoz nem kell a jogtulajdonos (Larry Pierce / Online Bible) saját nyilatkozata:
   a "Please do not redistribute it yourself." és a "Permission should be gained from Online Bible" mondat kérés, nem
   licencfeltétel; a hatályos forrás az upstream README (CC BY 4.0). Más sorra nem általánosítható.
   **DT-F33g (felhasználói döntés, 2026.10.04), harmadik kivétel:** a **BDB** (1906), a **Thayer** (1886, 1889) és a
   **Nave_basokant** (Nave, 1897) sorra a `kozkincs` állapothoz a (c) feltétel nem követelmény: a mű kora miatt közkincs,
   kiadói nyilatkozat nélkül is. A kivétel a művekre szól, a digitális réteg külön feltételeit (formázás, lekaparás)
   nem igazolja; azokat a sorok megjegyzése `javaslat:` jelöléssel tartja nyilván. Más sorra nem általánosítható.
3. A `projekt_adat` sor a repó saját adatáé és prózáé. **F89 / DT131 (felhasználói döntés, 2026.10.13; DT116):** a jogok forrása a jogtulajdonos döntése, a repó gyökerében lévő `LICENSE`-ban rögzítve (ez a sor `forras_hely`-e);
   minden jog fenntartva, `kereskedelmi=igen` (a jogtulajdonos maga használhatja; harmadik félnek a `LICENSE` nem ad jogot), `share_alike=nem`, `allapot=tisztazott`.
   A harmadik fél adatára a `LICENSE` nem terjed ki, az a saját sora szerint érvényes; a CC BY-SA és az MCGED eredetű rész nem kerülhet zárt csomagba. (A DT-F24 halasztása lezárva, a DT112 felülírva.)

**N9 (a licenc-besorolás kettős forrása): lezárva (F42 / DT-F42g, 2026-10-05).** A generátor (`eszkozok/lexikon_general.py`) a licenc-állapotot (`allapot`) és a megjelenő rövid címkét (`cimke`) ebből a táblából olvassa; a kódban nincs licenc-konstans, és nincs alapértelmezett érték.

- A generátor szótár- és adatkulcsai a `dataset` azonosítók (pl. `BDB`, `TBESG`, `Karoli_KH`, `LXX_OS`, `UBS_DNTG`, `projekt_adat`). **Ha egy kulcsnak nincs sora a táblában, vagy a sor `cimke` mezője üres, a generátor hibával áll meg** (`SystemExit`, a kulcs és a fájl megnevezésével).
- Leképezés: `tisztazott` és `kozkincs` állapotú sor: nincs tisztázatlan-jelölés; `tisztazatlan` állapotú sor: van jelölés (a generátor motívumonkénti összegző sora, `tisztázatlan licencű forrás érintett-e`, a `szocikkek` blokk szótárkulcsaira).
- A `cimke` csak a nézetek rövid címkéje; a kötelező forrásmegjelölések szó szerinti szövege a `kotelezo_megjeloles` mezőben áll (a Mounce- és LSJ-megjelölést a generátor ma is saját mondatként írja, az LSJ-mondat licencneve a táblából jön).
- A mai kód és tábla eltérései, amelyek a bevezetéskor megszűntek: az `UBS` kulcs (a táblában `UBS_DBH` és `UBS_DNTG`), a `projekt-adat` / `projekt_adat` névkülönbség, az LSJ címkéje (CC BY-SA 3.0 → 4.0, Perseus nyilatkozata szerint).
- A tábla és a generátor együttes helyességét a `python eszkozok/general.py --cel lexikon --ellenoriz` futása mutatja (hiányzó sor = hiba).

### 2.20 `adat/karoli_strong/parok_<könyv>.tsv` és `szavak_<könyv>.tsv` — Károli–Strong párosítás könyvenként

**Állapot: javaslat (modell-kimenet), nem lekérdezés-eredmény.** Két modell (Sonnet a Code-ban, Gemini az
Actionsben) független párosítása ugyanazzal a prompttal (`f21p/prompt_v3.md`, befagyasztva); az
`eszkozok/karoli_strong/egyesit.py` determinisztikusan (API nélkül) állítja elő. A modell Strong-számot
nem ír: a `strong` a TAHOT-ból jön, a linkelt eredeti szó sorszáma alapján. Mivel nem `lekerdez.py`
eredmény, a két tábla **első sora egy `#`-kezdetű proveniencia-sor** (a `licencek.tsv` mintájára; az olvasók átugorják),
`scope=manual | forras=… | ts=…` alakban (1.5); a `ts` a C futásnapló utolsó időbélyege, tehát a bemenetekből származik, és az
újraépítés bájtra azonos marad. A tábla modell-kimenet, javaslat (CLAUDE.md 1. szabály: a `bizonyossag` nem „ellenőrizve”). A zárt licencű Károli–Strong
forrás adata nem része a tábláknak (l. `eszkozok/karoli_strong/zart_osszevet.py`: csak helyi, összesített
összevetés). Az első hat könyvből két modellel az 1Móz (`parok_1Moz.tsv`, `szavak_1Moz.tsv`), a 2Móz (`parok_2Moz.tsv`, `szavak_2Moz.tsv`; a 2Móz 35:36–36:37 versei a versbeosztás-detektor megfeleltetésével, a `2Móz_javito` javító menetből, l. `naplok/F22_2Moz_jelentes.md` 5.1, 5.5). Az `er` sorok `vers` oszlopa a **Károli-kulcs**: a megfeleltetett eredeti vers tokenjei (pl. a `2Móz 35:36` `er` sorai az F22 idején a TAHOT 36:1 szavai voltak; az F85.6 óta ezek a `TAHOT_kivonat.tsv` `2Móz 35:36` kulcsán állnak); a megfeleltetés nélküli eredeti vers a saját kulcsán, ha az foglalt, `+1000`-es verssorszámú azonosítón szerepel (nem igehely; a jelenlegi 2Móz–4Móz listában ilyen nincs: a 4Móz 30:1 a kézi 1:2 beolvasztásba kerül), `kezi` állapotban. **Az F85.6 (a `TAHOT_kivonat.tsv` versszintű átkulcsolása) és az F85.8 óta** a TAHOT-kulcs maga Károli-kulcs, az `f22/versmegfeleltetes.tsv` ÓSZ-sora és a kézi tábla adatsora kivezetve (az alábbi felsorolás az F22-beli előállítás állapotát írja le; `naplok/F85_jelentes.md`). A megfeleltetés a `f22/versmegfeleltetes.tsv` jóváhagyott könyveire érvényes volt (`tokenek.VERSBEOSZTAS_JOVAHAGYOTT`: 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón, Ezsd, Ez, Péld, Bír, Jób, Eszt, 2Sám, 1Sám, 1Kir, Neh, 2Kir, Dán, Ruth, Jón, Náh, Préd, Abd, Zak, Hós, Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir; a 3Mózesnek, az 5Mózesnek, a Józsuénak, a Zsoltároknak, a Jeremiásnak, az 1Krónikának, a 2Krónikának, az Ezsdrásnak, az Ezékielnek, a Bíráknak, az Eszternek, a 2Sámuelnek, az 1Sámuelnek, az 1Királyoknak, a Nehémiásnak, a 2Királyoknak, a Dánielnek, a Ruthnak, a Jónásnak, a Náhumnak, a Prédikátornak (a Préd 2:26 jóváhagyott beolvasztása az `f22/versosszevonas.tsv`-ben áll), az Abdiásnak, a Zakariásnak, a Hóseásnak (a Hós 1:11 és 11:11 jóváhagyott beolvasztása az `f22/versosszevonas.tsv`-ben áll) és a Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én és Sir könyvnek (a felhasználó közvetlen ellenőrzése, 2026.10.11) a listában nincs sora; a 4Mózesnél csak a 30. fejezet sorai; az Ézsaiásnál a detektor 9. és 64. fejezeti hibáját a `f22/versmegfeleltetes_kezi.tsv` kézi megfeleltetése javítja, a Példabeszédeknél ugyanez a 12. fejezet eltolását (Károli 12:n → TAHOT 12:(n+1)), a Jóbnál a 17. és a 37. fejezetét (Károli n → TAHOT n+1) és a 40. fejezetét (Károli 40:n → TAHOT 40:(n+5), #83); a kézi táblát a detektor regenerálása nem írja felül, jóváhagyás: `naplok/F22_versbeosztas_jovahagyas.md`). **Kézi 1:2 beolvasztás** (`f22/versosszevonas.tsv`; az F85.10 óta a beolvasztott vers tokenjei a közös Károli-kulcson állnak, a fájl `er_tol`–`er_ig` oszlopa jelöli a helyüket): a Károli-vers egy szakasza és az eredeti vers tokenjei `kezi` (nincs link, nem `betoldas`); az eredeti vers `er` sorai a Károli-vers saját eredeti szavai után folytatott sorszámmal szerepelnek (4Móz 29:39 hu 25–38, er 31–43 = TAHOT 4Móz 30:1; 2:1 irányban ugyanígy: Ézs 9:20 hu 15–34 = TAHOT Ézs 9:20, Ézs 64:1 hu 12–31 = TAHOT Ézs 64:2, Péld 11:31 hu 15–30 = TAHOT Péld 12:1, Jób 16:22 hu 14–21 = TAHOT Jób 17:1, Jób 36:33 hu 13–21 = TAHOT Jób 37:1). **Csak-Sonnet könyv** (3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón, Ezsd, Ez, Péld, Bír, Jób, Eszt, 2Sám, 1Sám, 1Kir, Neh, 2Kir, Dán, Ruth, Jón, Náh, Préd, Abd, Zak, Hós, Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én és Sir, `parok_3Moz.tsv`, `szavak_3Moz.tsv`, `parok_4Moz.tsv`, `szavak_4Moz.tsv`, `parok_5Moz.tsv`, `szavak_5Moz.tsv`, `parok_Jozs.tsv`, `szavak_Jozs.tsv`, `parok_Zsolt.tsv`, `szavak_Zsolt.tsv`, `parok_Ezs.tsv`, `szavak_Ezs.tsv`, `parok_Jer.tsv`, `szavak_Jer.tsv`, `parok_1Kron.tsv`, `szavak_1Kron.tsv`, `parok_2Kron.tsv`, `szavak_2Kron.tsv`, `parok_Ezsd.tsv`, `szavak_Ezsd.tsv`, `parok_Ez.tsv`, `szavak_Ez.tsv`, `parok_Peld.tsv`, `szavak_Peld.tsv`, `parok_Bir.tsv`, `szavak_Bir.tsv`, `parok_Job.tsv`, `szavak_Job.tsv`, `parok_Eszt.tsv`, `szavak_Eszt.tsv`, `parok_2Sam.tsv`, `szavak_2Sam.tsv`, `parok_1Sam.tsv`, `szavak_1Sam.tsv`, `parok_1Kir.tsv`, `szavak_1Kir.tsv`, `parok_Neh.tsv`, `szavak_Neh.tsv`, `parok_2Kir.tsv`, `szavak_2Kir.tsv`, `parok_Dan.tsv`, `szavak_Dan.tsv`, `parok_Ruth.tsv`, `szavak_Ruth.tsv`, `parok_Jon.tsv`, `szavak_Jon.tsv`, `parok_Nah.tsv`, `szavak_Nah.tsv`, `parok_Pred.tsv`, `szavak_Pred.tsv`, `parok_Abd.tsv`, `szavak_Abd.tsv`, `parok_Zak.tsv`, `szavak_Zak.tsv`, `parok_Hos.tsv`, `szavak_Hos.tsv`, `parok_Mal.tsv`, `szavak_Mal.tsv`, `parok_Hag.tsv`, `szavak_Hag.tsv`, `parok_Sof.tsv`, `szavak_Sof.tsv`, `parok_Hab.tsv`, `szavak_Hab.tsv`, `parok_Mik.tsv`, `szavak_Mik.tsv`, `parok_Amos.tsv`, `szavak_Amos.tsv`, `parok_Joel.tsv`, `szavak_Joel.tsv`, `parok_En.tsv`, `szavak_En.tsv`, `parok_Sir.tsv`, `szavak_Sir.tsv`, l. `naplok/F22_5Moz_jelentes.md`, `naplok/F22_Jozs_jelentes.md`, `naplok/F22_Zsolt_jelentes.md`, `naplok/F22_Ezs_jelentes.md`, `naplok/F22_Jer_jelentes.md`, `naplok/F22_1Kron_jelentes.md`, `naplok/F22_2Kron_jelentes.md`, `naplok/F22_Ezsd_jelentes.md`, `naplok/F22_Ez_jelentes.md`, `naplok/F22_Peld_jelentes.md`, `naplok/F22_Bir_jelentes.md`, `naplok/F22_Job_jelentes.md`, `naplok/F22_Eszt_jelentes.md`, `naplok/F22_2Sam_jelentes.md`, `naplok/F22_1Sam_jelentes.md`, `naplok/F22_1Kir_jelentes.md`, `naplok/F22_Neh_jelentes.md`, `naplok/F22_2Kir_jelentes.md`, `naplok/F22_Dan_jelentes.md`, `naplok/F22_Ruth_jelentes.md`, `naplok/F22_Jon_jelentes.md`, `naplok/F22_Nah_jelentes.md`, `naplok/F22_Pred_jelentes.md`, `naplok/F22_Abd_jelentes.md`, `naplok/F22_Zak_jelentes.md`, `naplok/F22_Hos_jelentes.md`, `naplok/F22_Mal_jelentes.md`, `naplok/F22_Hag_jelentes.md`, `naplok/F22_Sof_jelentes.md`, `naplok/F22_Hab_jelentes.md`, `naplok/F22_Mik_jelentes.md`, `naplok/F22_Amos_jelentes.md`, `naplok/F22_Joel_jelentes.md`, `naplok/F22_En_jelentes.md`, `naplok/F22_Sir_jelentes.md`, `naplok/F22_Filem_jelentes.md`, `naplok/F22_2Jan_jelentes.md`, `naplok/F22_3Jan_jelentes.md`, `naplok/F22_Jud_jelentes.md`, `naplok/F22_USZ_proba_jelentes.md`, `naplok/F22_Tit_jelentes.md`, `naplok/F22_2Thessz_jelentes.md`, `naplok/F22_2Pet_jelentes.md`, `naplok/F22_2Tim_jelentes.md`, `naplok/F22_1Thessz_jelentes.md`, `naplok/F22_Kol_jelentes.md`, `naplok/F22_Fil_jelentes.md`, `naplok/F22_1Pet_jelentes.md`, `naplok/F22_1Jan_jelentes.md`, `naplok/F22_Jak_jelentes.md`, `naplok/F22_1Tim_jelentes.md`, `naplok/F22_USZ_A_jelentes.md`, `naplok/F22_Gal_jelentes.md`, `naplok/F22_Ef_jelentes.md`, `naplok/F22_Zsid_jelentes.md`, `naplok/F22_USZ_B_jelentes.md`; az Ézs, a Jer, az 1Krón, a 2Krón, az Ezsd, az Ez, a Péld, a Bír, a Jób, az Eszt, a 2Sám, az 1Sám, az 1Kir, a Neh, a 2Kir, a Dán, a Ruth, a Jón, a Náh, a Préd, az Abd, a Zak, a Hós, a Mal, a Hag, a Sof, a Hab, a Mik, az Ámós, a Jóel, az Én és a Sir a Message Batches API-n, DT73 (a); DT-F22c: a C kimarad): nincs C-fájl, ezért minden link és szó `alacsony`, `forras: S` (a végleges kapuhibás és a kézi beolvasztott versek szavai `kezi`, pl. 1Krón 19:2, 2Sám 23:16, Ézs 9:20, 64:1, Péld 11:31, Jób 16:22, 36:33; egy modell, nincs egyezés; a `magas` jelölés nincs), a proveniencia-sor `ts=manual` (nincs C futásnapló), az `f22_elemzes.py` „gyanús fejezetek” sora minden fejezetet jelez (nem eltolódás-jel); a többi könyv ugyanezzel a
sémával, a könyv-paraméter cseréjével. A fájlnév a magyar könyvrövidítés ékezet nélküli alakja.

**ÚSZ-könyvek (F22 22.8, 2026.10.12: Filem, 2Ján, 3Ján, Júd; 22.9 A csomag: Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 22.9 B csomag: Gal, Ef, Zsid).** Ugyanez a séma; az `er` oldal forrása a `TAGNT_kivonat.tsv` (a `TAHOT` helyett mindenütt, ahol az alábbi táblázatok a TAHOT-ot nevezik: `er_szo`, `strong`, G-számok), a proveniencia-sor a TAGNT-t nevezi meg. A TR-ben nem szereplő eredeti szó (`Kritikai kiadás` mezőjében nincs `TR`, `TR»N`, `TR«N`) a bemenetben `[nem TR]` jelölést kap, és a `prompt_v3` K szabálya szerint `forditatlan`; ahol azonban a TR más alakot olvas, és annak nincs sora a kivonatban, a modell a `[nem TR]` sorhoz köti a Károli szavát (`parositva`, a `strong` a kritikai szöveg alakjáé; az A csomagban 27/375, l. `naplok/F22_USZ_A_jelentes.md` 4.). Ezeket a tokeneket a link megtartásával (D45, (a) változat) az **adatszintű jelölőtábla** sorolja fel: `adat/karoli_strong/nem_tr_parositott.tsv` (generált, `eszkozok/karoli_strong/nem_tr_lista.py`; oszlopok: `vers`, `er_sorszam`, `er_szo`, `strong`, `kritikai_kiadas` (a TAGNT mezője), `allapot`, `hu_sorszam` (a partnerek, vesszővel), `hu_szo`; kulcs: `vers` + `er_sorszam`). A tábla minden ÚSZ-könyv egyesítése után újraépül (`--ellenoriz`: egyezik-e). Aki a `strong` oszlopot TR-hű adatként használja, ezeket a sorokat kizárja vagy külön kezeli. Eredeti vers nélküli Károli-vers (3Ján 1:15, Fil 1:16, Fil 1:17; N-F22c; a Fil 1:16–17 külön: N-F22d), valamint a `f22/kezi_versek_<könyv>.tsv`-ben felsorolt vers (a nyers TAGNT `[..]`/`{..}` sorai a kivonatból kimaradtak, a görög szöveg részleges lehet; N-F22c): minden Károli-tokenje `fuggoben`, link nélkül, és az átnézési sorba kerül.

Olvasás/írás: `split('	')` / `'	'.join()` (a `csv` modul tilos, l. CLAUDE.md). Az igehely kanonikus magyar alak.

**`parok_<könyv>.tsv`** — linkenként egy sor (a Károli-token és az eredeti token párja):

| Mező | Tartalom |
|---|---|
| `vers` | `IGEHELY` (1.1), pl. `1Móz 1:1` |
| `hu_sorszam`, `hu_szo` | a Károli-token sorszáma (1-től) és szövege (`tokenek.tokenizal`, a `Karoli_1908.tsv` versszövegéből) |
| `er_sorszam`, `er_szo` | az eredeti token sorszáma és ragozott alakja a `TAHOT_kivonat.tsv`-ből (soronkénti sorrend a versen belül) |
| `strong` | a TAHOT `Strong-szám` mezője (pl. `H7225`; `H9001`–`H9049` a TAHOT morféma-kódjai) — a szkript veszi, modell nem írja |
| `bizonyossag` | `magas` (mindkét modell ugyanazt a linket adta) \| `alacsony` (a két modell eltér, vagy csak az egyik ment át a kapun; a Sonnet változata kerül a táblába) \| `kezi` (mindkét modell kapuhibás; ilyen versnek nincs sora ebben a táblában, a vers az átnézési sorba kerül) |
| `forras` | `S+C` (egyezés) \| `S` (csak Sonnet) \| `C` (csak C) |

**`szavak_<könyv>.tsv`** — tokenenként egy sor; minden Károli-token és minden eredeti token **pontosan egyszer**:

| Mező | Tartalom |
|---|---|
| `vers`, `oldal`, `sorszam`, `szo` | az igehely; `hu` (Károli) vagy `er` (eredeti); a token sorszáma és szövege |
| `allapot` | `parositva` \| `betoldas` (Károli-token, amelynek nincs eredeti párja) \| `forditatlan` (eredeti token, amelyet Károli nem fordított) \| `fuggoben` (csak `kezi` versnél) |
| `partner_sorszam` | a párok sorszámai vesszővel (`hu` sorban az eredeti, `er` sorban a Károli sorszámok) |
| `strong` | `er`: a token TAHOT-Strongja; `hu`: a partnerek TAHOT-Strongjai `+`-szal fűzve (üres, ha nincs partner) |
| `bizonyossag`, `forras` | mint a `parok` táblában; token-szinten `magas`, ha a két modell ugyanazt a partnerhalmazt (vagy ugyanazt a betoldás/fordítatlan döntést) adta |

**Gépi ellenőrzés** (`egyesit.py --ellenoriz`): minden token pontosan egyszer szerepel a `szavak` táblában; a
`strong` minden értéke a TAHOT-ból levezethető; a `parok` és `szavak` szó-alakjai a forrásból. **Átnézési sor:**
`naplok/F22_<könyv>_atnezes.tsv` (a `kezi` versek, linkek nélkül). A tábla `egyesit.py`-val újraépíthető, a két
modell nyers válaszaiból (`f22/valaszok/sonnet/`, `f22/valaszok/c/`), API-hívás nélkül, bájtra azonosan.

### 2.21 `dontes_hatas.tsv` — döntések átvezetésének nyilvántartása (F51, FELADATOK #51, DT-F51-5)

Egy sor = egy döntés egy érintett fájlban: az a mintapár, amely a fájlban a **döntés előtti** állapotot
jelzi. A tábla a CI E25 szabályának (l. `eszkozok/ellenorzes/szabalyok.py`) egyetlen bemenete; csak azt
fogja meg, amit előre leírtunk. A táblában nem szereplő, fogalmi ellentmondásokat a `/konzisztencia`
ügynök (`.claude/commands/konzisztencia.md`) keresi.

Kulcs: `dontes_forras` + `erintett_fajl` + `tilos_minta`. **A fájl a kulcs része**, mert a D-számok
fájlonként újraindulnak, és ütköznek (pl. D34: `F26_EGYFORRAS_NAPLO_BRIEF.md` kontra
`F05_SZOTAR_BRIEF.md`, l. `naplok/KONZISZTENCIA_naplo.md`). Fejlécsorok `#`-tel; olvasás
`split('\t')`, írás `'\t'.join()` (a `csv` modul tilos, l. CLAUDE.md).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `dontes_forras` | `fájl#azonosító` | ✔ | a döntést rögzítő repó-relatív fájl és azonosító, pl. `F26_EGYFORRAS_NAPLO_BRIEF.md#D34`. A fájlnak léteznie kell, és az azonosítónak szó szerint (`\bD34\b`) szerepelnie kell benne |
| `datum` | `ÉÉÉÉ-HH-NN` | ✔ | a döntés napja; a 14 napos állás-határ (E25 (b)) ettől számít |
| `erintett_fajl` | repó-relatív út | ✔ | az a fájl, amelynek a döntést tükröznie kell; léteznie kell |
| `tilos_minta` | regex (Python `re`) | ✔ | a döntés előtti állapot; sorokra illesztve (`re.search`), tabot nem tartalmazhat |
| `atmeneti_jeloles` | regex | | ha a fájlban bárhol megvan, a `tilos_minta` találat csak `JELENTES` (jogos átmeneti állapot), nem `FIGYELMEZTETES` |
| `tovabbvivo_feladat` | egész szám | | a `FELADATOK.md` száma, amely a döntést átvezeti; üres, ha nincs. Az állapotát az `F<nn>_*_BRIEF.md` fejlécének `feladat:`/`allapot:` mezője adja |
| `megjegyzes` | szabad szöveg | | indok, a sor származása |

**E25 (CI, `szabalyok.py`):** (a) `tilos_minta` találat az `erintett_fajl`-ban `atmeneti_jeloles` nélkül →
FIGYELMEZTETES (jelöléssel: JELENTES); (b) a `tovabbvivo_feladat` állapota `nem_indult` / `brief_kell`, és a
`datum` óta több mint 14 nap telt el → FIGYELMEZTETES; (c) a `dontes_forras` fájlja vagy azonosítója, az
`erintett_fajl` vagy egy `tilos_minta` / `atmeneti_jeloles` regex hibás vagy nem létezik → **HIBA** (a tábla
nem avulhat el csendben). Csak az (c) HIBA (DT-F51-4).

**Felvételi szabály:** csak olyan döntésre kerül sor, amelynek a régi állapota **regexszel egyértelműen**
felismerhető. Ami nem az, azt az ügynök jelenti (nem a tábla dolga). Egy sor kézzel kerül be, a döntés
rögzítésével egy menetben; a szabály nem javít, nem ír vissza.

---

### 2.22 `morf_kulcs_heber.tsv` és `morf_nyelv_aramai.tsv` — héber morfológiai jelkulcs (F58, FELADATOK #58, DT35)

A `konkordancia/Macula_heber_*.tsv` `morf` oszlopának kódjait (OSHB-kódolás, nyelvjelölő nélkül) oldja fel magyarra.
**Forrás és licenc:** `adat/kulso/oshb_HebrewMorphologyCodes.html` (openscriptures/morphhb@3d15126fb1ef74867fc1434be1942e837932691f,
`parsing/HebrewMorphologyCodes.html`), **CC BY 4.0**; a szó szerinti nyilatkozat és a kötelező megjelölés:
`adat/kulso/morf_kulcs_LICENC.txt` és `adat/licencek.tsv` (`morf_kulcs_heber`, `morf_nyelv_aramai` sor). Az ETCBC `Morphology.lexicon` (CC BY-NC) nem forrás.
Mindkét tábla **generált** (`eszkozok/morf_kulcs_import.py`, `eszkozok/morf_nyelv_kivonat.py`), kézzel nem szerkeszthető. Olvasás `split('\t')`; fejlécsorok `#`-tel.

**`morf_kulcs_heber.tsv`** — kulcs: (`pozicio`, `nyelv`, `kod`).

| Mező | Tartalom |
|---|---|
| `pozicio` | `szofaj` · `szerkezet` (a szófaj pozícióinak sorrendje, a forrás szófaj-táblázatából: `jelentes_forras` = pl. `type > gender > number > state`) · `igetorzs` · `igetipus` · `tipus_A/N/P/R/S/T` (a szófaj típusa) · `szemely` · `nem` · `szam` · `allapot` · `nyelv_jel` (a forrás `H`/`A` jele) · `helykitolto` (az `x`) |
| `nyelv` | `H` (csak héber), `A` (csak arámi), `*` (mindkettő). Csak az `igetorzs` nyelvfüggő: a törzsbetűk jelentése héberben és arámiban más |
| `kod` | a jel (egy karakter; a `szerkezet` sorban a szófaj betűje) |
| `jelentes_forras` | a forrás saját megnevezése, szó szerint (angol) |
| `jelentes_hu` | a `jelentes_forras` fordítása a projekt szóhasználatával; **magyarázat nincs benne** |
| `forras` | a forrás pontos azonosítója (repó@commit, fájl, licenc) |
| `proveniencia` | `scope=… | forras=… | ts=…` (CLAUDE.md 1. szabály) |

Szabályok: (1) a feloldó (`eszkozok/morf_feloldas.py`) kizárólag ebből a táblából dolgozik; (2) a Macula-kód nyelvjelölőt **nem** hordoz, ezért
a szó nyelvét a `morf_nyelv_aramai.tsv` adja; nyelv nélkül az `igetorzs` kétértelmű vagy nyelvfüggő, és a kimenet ezt jelzi; (3) az `allapot` (feloldás eredménye) értékei: `teljes` · `helykitoltovel` · `ketertelmu` (nyelv nélkül több olvasat; a `ketertelmu` jelző mező is megmarad; arámi nyelv-kivonattal hívva egyértelmű, tehát `teljes`) · `reszleges` · `ismeretlen`; sorrend: hiányzó jel → `reszleges`, helykitöltő → `helykitoltovel`, kétértelmű jelző → `ketertelmu`, egyébként `teljes` (DT36); (3b) az `x` a forrás
szerinti helykitöltő („ismeretlen vagy szükségtelen érték”), a feloldás állapota ilyenkor `helykitoltovel`, nem `teljes`; (4) a forrás a nemet
`common (verb)` / `both (noun)` megnevezéssel adja, a magyar oszlop ezt szó szerint tükrözi akkor is, ha a névmásnál zavaró (`Pdxcp`).

**`morf_nyelv_aramai.tsv`** — kulcs: `xml_id` (a Macula-szó azonosítója, `Macula_heber_*.tsv` `xml_id`). Oszlopok: `xml_id`, `ref`, `morf`, `nyelv` (mindig `A`).
Csak az arámi szavak szerepelnek (7 549 morféma, a `w@lang="A"` a Macula lowfat XML-ben); ami nincs a táblában, az a Macula szerint héber (`lang="H"`, 468 362 szó).
Forrás: Macula Hebrew @47db250b, CC BY 4.0 (Biblica, Inc). A `morf` oszlop minden sorban egyezik a `Macula_heber_*.tsv` értékével (0 eltérés).

### 2.23 `bdb_igehely_javitas.tsv` — a BDB-hivatkozások fejezetszám-javítótáblája (F56, FELADATOK #56, DT-F38i (c))

A `konkordancia/BDB_teljes_unabridged.tsv` néhány hivatkozásának fejezetszáma az adott könyvben nem létezik (pl. `Eccl 17:10`, a Prédikátor 12 fejezetes).
A forrásfájl **nem módosul**; a javítás ebben a táblában él, és az adatblokk (`eszkozok/bdb_adatblokk.py`, 6. szakasz) meg a fordítás (`Y [BDB: X]`) olvassa.
**Generált** (`python eszkozok/bdb_adatblokk.py --javitas-epit`), kézzel nem szerkeszthető; olvasás `split('\t')`, fejlécsor előtt `#`-sor. A tábla **javaslat-szintű**
(gépi, a TAHOT/Károli–Strong adatából levezetett), a felhasználó az F56 M3 megállásán a fenti szabályt jóváhagyta.

| Mező | Tartalom |
|---|---|
| `strong` | a BDB-szócikk `Strong_padded` kulcsa (pl. `H7223`, homográfnál `H0090a`) |
| `forras_hivatkozas` | a hivatkozás a forrásban, betűre (a forrás könyvrövidítésével), pl. `Eccl 17:10` |
| `javitott_hivatkozas` | a javított igehely Károli-rövidítéssel (`Préd 7:10`); üres, ha `allapot=jelolt_marad` |
| `allapot` | `javitva` (pontosan egy jelölt, és nincs könyvnév-hiba gyanú) · `jelolt_marad` (nulla vagy több jelölt, vagy könyvnév-hiba gyanú; a forrás alakja marad) |
| `indok` | az algoritmus eredménye szavakkal: a jelölt(ek), illetve hogy nincs jelölt; ha ugyanaz a `fejezet:vers` másik könyvben is tartalmazza a Strong-számot, `FIGYELEM:` megjegyzés (a hiba könyvfeloldási hiba is lehet) |
| `proveniencia` | `scope=… | forras=… | ts=…` (1.5; CLAUDE.md 1. szabály) |

**Algoritmus** (brief M2): minden olyan `Könyv fej:vers` hivatkozásra a szócikkben, amelynek fejezetszáma a könyvben nem létezik (`forditas_kapuk.FEJEZETSZAM`, az ÓSZ-ben a Károli- és az MT-szám nagyobbika),
(1) a szócikk Strong-számának előfordulásai az adott könyvben (`TAHOT_kivonat.tsv` ∪ `adat/karoli_strong/parok_*.tsv`; a TAHOT ismert hiányai miatt mindkettő; a homográf-betű nem számít; az önálló és a nyelvtani előtag-alak egy szónak számít, pl. H4480 `min` = H9006 `mi-`, a pár forrása az `adat/grammatikai_strongok.tsv` `PREFIXÁLT változata (H9xxx` megjegyzése);
(2) jelöltek: a hibás fejezetszámból **egy számjegy elhagyásával, betoldásával vagy cseréjével** előálló, a könyvben létező fejezetszám, amelynek **ugyanazon a versszámú versén** a Strong-szám előfordul;
(3) **pontosan egy jelölt** → `javitva`; nulla vagy több → `jelolt_marad`. Találgatás nincs.
**Könyvnév-hiba gyanú (DT46, felhasználói döntés 2026-10-06):** ha a hibás `fejezet:vers` *más könyvben is létezik, és ott a Strong-szám szerepel*, a sor `jelolt_marad` akkor is, ha egyetlen jelölt van (a hiba könyvfeloldási hiba is lehet; a javítás fordítási szöveget érintene), az `indok` `FIGYELEM:` jelzést kap. Ezért `javitva` sor soha nem FIGYELEM-es. **Nyelvtani és gyakori Strong (DT48):** az egyetlen jelölt sem `javitva`, ha a Strong-szám az `adat/grammatikai_strongok.tsv`-ben szerepel (pl. H4480, H9009; felhasználói döntés 2026-10-06), vagy (a végrehajtó kiegészítése, a felhasználó 2026-10-06-án jóváhagyta, DT48: biztonsági háló, nem kalibrált határ; ha valaha egy sort érint, a sor kézi átnézésre kerül; ma egy sort sem érint) 1000-nél több különböző versben fordul elő (a nyelvtani előtag-párral együtt számolva; a talált egy jelölt ekkor nem bizonyít; a megmaradt `javitva` sorok legnagyobbika 358 vers). Ilyenkor az `indok` ezt nevezi. Állapot: 93 sor, 7 `javitva`, 86 `jelolt_marad` (ebből 61 FIGYELEM-es; a H4480 `1Ki 32:47` sora az előtag-pár révén lett az, mert az 5Móz 32:47 a H9006-tal szerepel). Csak a könyvnévvel jelölt hivatkozások vizsgáltak (a lánc második tagja, `Isa 40:1; 41:2`, könyvnév nélkül nem).
Kulcs: `strong` + `forras_hivatkozas`. Teszteset: `H7223`, `Eccl 17:10` → `Préd 7:10`.
**Átvezetés a fordításba (M5, `eszkozok/bdb_atvezet_m5.py`):** a `javitva` hivatkozás a `forditasok.tsv` BDB-sorainak `forditas_hu` mezőjében `Y [BDB: X]` alakot kap (Y a helyes, X a forrásbeli hivatkozás, Károli-rövidítéssel); más mező nem változik (a `forras_hash` a forrásé, ezért érintetlen). A kapuk ezt kezelik: a 13. (fejezetszám) az `[BDB: …]` tartalmát nem jelzi, a többi a `Y [BDB: X]` → `X` visszaállított szöveget látja (`forditas_kapuk.bdb_jeloles_vissza`). Az 1–5. adag fordításaiban 4 a 7 `javitva` sorból fordul elő (H5002, H5046, H4427, H7223); H0479, H2597 és H5377 a 9–11. adagba esik, ott az adatblokk 6. szakasza viszi át a #38 menetében. A H4480 és a H9009 sora a DT48 miatt `jelolt_marad`, a két fordításmező a `bdb_atvezet_m5.py --visszaallit` móddal `Y [BDB: X]` → `X` alakra állt vissza.

### 2.24 `karoli_variancia.tsv` — Károli-variancia és soronkénti megerősítés (F65, FELADATOK #65, DT-M2, DT104)

**Generált** (`python eszkozok/karoli_ellenorzes.py --variancia adat/karoli_variancia.tsv`), kézzel nem szerkeszthető; olvasás `split('\t')`, a `csv` modul tilos. A fájl első sora `# proveniencia: …` (fájlszintű); a `megerosites` sorok és az aggregátum-sorok saját `proveniencia` oszlopot is hordoznak.

Forrás a `parok_<könyv>.tsv`, tehát **modell-kimenet, javaslat** (a `bizonyossag` nem „ellenőrizve”). Hatókör: azok a könyvek, amelyekben van `magas` pár (ma 1Móz, 2Móz; az `alacsony` pár is szerepel, a `bizonyossag` oszlopban jelölve — a csak-`alacsony` könyvek varianciája ~190 ezer sor lenne, ezért nem kerül be, a `variancia()` függvény `konyvek=` paraméterével előállítható).

| Oszlop | Jelentés |
|---|---|
| `tipus` | `strong_szoalak` (Strong → Károli-szóalakok) \| `szoalak_strong` (szóalak → Strongok) \| `megerosites` (egy régi sor megerősítése) |
| `konyv` | a `parok_<könyv>` könyve (az igehely rövidítése) |
| `kulcs` | az aggregátumnál a Strong (vagy a szóalak); a `megerosites` sornál a régi sor Strongja(i) |
| `ertek` | az aggregátumnál a szóalak (vagy a Strong); a `megerosites` sornál a `karoli_szo` szavaihoz tartozó gépi Strongok |
| `darab` | előfordulások száma (csak aggregátum) |
| `bizonyossag` | `magas` \| `alacsony` (a pár; a `megerosites` sor csak `magas` lehet) |
| `id`, `igehely`, `karoli_szo` | csak `megerosites`: az `elofordulasok.tsv` sor kulcsa és a régi `karoli_szo` |
| `reszleges` | csak `megerosites`: `igen`, ha a `karoli_szo` több szavas és a névelőn (`a`, `az`) és az `és`-en kívül nem minden szava illeszkedett a sor Strongjaihoz (laza illesztés, DT104 (1); a szűrés csak lista-szűrés, az ítéletet nem érinti, DT105 (2)); egyébként `nem` |
| `nincs_gepi_par` | csak `megerosites`: a `karoli_szo` azon szavai, amelyeknek a versben nincs gépi párja (valódi hézag), vesszővel; a névelő (`a`, `az`) és az `és` ki van szűrve |
| `mas_strong` | csak `megerosites`: a `karoli_szo` azon szavai, amelyek a versben más Stronghoz illeszkednek, `szó:Strong` alakban (több Strong `+`-szal), vesszővel; a névelő és az `és` ki van szűrve |
| `proveniencia` | `scope=… \| forras=… \| ts=…` (kötelező, nem üres) |

A `megerosites` sor a `szó-szintű-gépi` állítás (1.7) saját bizonyítéka: megléte a feltétele annak, hogy az `elofordulasok.tsv`/`jeloltek.tsv` sor `azonositas_modja`-ja `szó-szintű-gépi` lehet. A sor akkor is újraáll, ha a mód már átállt (a generálás idempotens).

### 2.25 `bdb_karoli.tsv` — a kész BDB-szócikkek Károli-adata (F80, FELADATOK #80, DT117)

A #38 BDB-fordítása a Károli–Strong párosítás hiányos állapotában készült (a fordítót tápláló adatblokk Károli-szakasza csak az 1–5Móz és a Józs párjaiból élt, a többinél `[NINCS KÁROLI-ALAK]` állt vagy adatblokk még nem volt). A fordítás szövege nem változik (DT56); ez a tábla az **adatot** pótolja: minden kész (`forditasok.tsv`: `szotar=BDB`, `jelentes_szam=teljes`, `mezo=forditas_hu`) szócikkhez a **teljes ÓSZ** párosításból (`adat/karoli_strong/parok_*.tsv`, 2.20) a Károli-szóalakokat előfordulás-számmal és bizonyossággal, valamint példaverseket. A `forditasok.tsv` bájtra változatlan marad (a pótlás külön tábla; a #38 és az `emeles.py` írását nem érinti).

**Generált** (`python eszkozok/bdb_adatblokk.py --karoli-epit [--ts …]`), kézzel nem szerkeszthető; a kész szócikkek halmaza a `forditasok.tsv`-ből, az adat a `parok_*.tsv` és a `TAHOT_kivonat.tsv`-ből jön, ugyanaz a logika, mint az adatblokk 1. és 2. szakaszáé (`karoli_alakok`). A fájl első sora `# GENERÁLT: …` fájlszintű proveniencia (az olvasók átugorják), második a fejléc. Olvasás `split('\t')`, írás `'\t'.join()` (a `csv` modul tilos, CLAUDE.md). Újrafuttatható (a #38 új szócikkeire, a #22-javítások után); azonos `--ts`-sel bájtra azonos. A tábla **javaslat-szintű** (a `parok` modell-kimenet, 2.20; a `bizonyossag` nem „ellenőrizve”).

| Oszlop | Jelentés |
|---|---|
| `strong` | a BDB-szócikk kulcsa, a `forditasok.tsv` `strong` mezőjével azonos alak: `H` + 4 jegyű kitöltött szám (`H0001`, `H2617`); az adatot a szám alapján (`strong_szam`, homográf-betű nélkül) keresi a `parok`/`TAHOT` táblákban. Ma egyik kulcsnak sincs homográf-betűje. |
| `tipus` | `szocikk` (szócikkenként egy sor: összesítés + proveniencia) \| `alak` (Károli-szóalakonként egy sor) |
| `karoli_alak` | `alak` sorban a kisbetűsített Károli-szóalak (`parok.hu_szo`); `szocikk` sorban üres, **vagy** a `[NINCS KÁROLI-ALAK]` jelzés, ha a szócikk Strongjának a `parok`-ban nincs párja (üres forrás: kifejezett jelzés, nem kitöltés; CLAUDE.md 3. szabály; a mostani 674-ből egyiknél sem fordul elő) |
| `magas` | az alak (`szocikk` sorban az összes alak) `magas` bizonyosságú párjainak száma |
| `alacsony` | ugyanez az `alacsony` bizonyosságú pároké (a `parok` `magas` kivételével minden értéke; ma csak `alacsony` van) |
| `pelda_versek` | csak `alak` sor: legfeljebb 3 különböző vers `;`-vel, a `parok` kanonikus könyvsorrendjében (a `konkordancia/Konyv_normalizalo_tabla.tsv` sorrendje: 1Móz … Mal; a `bdb_adatblokk.parok_konyvek()` ebből rendez, és hibával áll meg, ha egy `parok_*.tsv` könyve a táblában nincs; egyetlen alias: a `parok_Sir.tsv` Siralmai a táblában `JSir`), könyvön belül a fájl sorrendjében (`IGEHELY`, 1.1). **Hivatkozás, nem szöveg:** a versszöveg nem másolódik. A példa kulcsa a **vers + a szócikk Strongja + a Károli-alak** (nem fájlbeli sorszám, mert a párosítás még változhat: #22-javítások, N46); a tárolt alak ellenőrző: a hármas a `parok_*.tsv`-ben egy sorra visszakereshető (`bdb_adatblokk.karoli_pelda_forras`), különben a hivatkozás elavult. |
| `tahot_elofordulas` | csak `szocikk` sor: a Strong előfordulásai a `TAHOT_kivonat.tsv`-ben a párosítás kész könyveiben |
| `par_db` | csak `szocikk` sor: a Strong `parok`-sorainak (Károli–Strong linkjeinek) száma az **egész ÓSZ-párosításban**; **link-darab, nem a `tahot_elofordulas` részhalmaza** (egy előfordulásra több link is eshet, és a `tahot_elofordulas` csak a kész könyvek előfordulásait számolja: pl. H3722: 178 pár 102 előfordulásra, H4191: 1087 / 840); a kettő viszonya lefedettség-jelzés (nem néma nem-találat), de nem hányados |
| `proveniencia` | **minden sorban kötelező, nem üres:** `scope=<Strong> \| forras=… \| ts=…` (1.5). Az `alak` sor proveniencia-ja a szócikk `szocikk` sorának proveniencia-jával **szó szerint azonos** (ugyanaz a lekérdezés adta; a sorszintű ismétlés ~+5 MB, elfogadott: így minden sor önállóan szűrhető/idézhető, csoportszintű hivatkozás nélkül) |

Kulcs: `strong` + `tipus` + `karoli_alak` (az `alak` sor egyedi a szócikkön belül). Rendezés: `strong` növekvően; szócikkenként a `szocikk` sor, majd az alakok az előfordulás-szám csökkenő, azonos számnál a kisbetűs szóalak kódpont-sorrendjében (Unicode, nem magyar ábécé: a magyar ékezetes betűk a latin alapbetűk után, az `a`–`z` blokk végén állnak). A szócikk-adat és a `forditasok.tsv` sora a `strong` mezőn kapcsolható (join). Ellenőrzés: `python eszkozok/teszt_bdb_adatblokk.py` (`KaroliTabla`: minden kész szócikk megvan, és minden sorban (`szocikk` és `alak`) nem üres a proveniencia, az `alak` soré a szócikk soréval azonos; a példaversek a `Konyv_normalizalo_tabla.tsv` könyvsorrendjében állnak; ismert Strongokon — H2617, H5785, H8057 — a példák forrássorra visszakereshetők; a `forditasok.tsv` hash-e a tábla-építés előtt és után azonos).

### 2.26 A `pardes.db` olvasói táblái — `token_macula`, `lxx_token`, `lxx_versszam`, `bdb_alias`, `nave_vers` (F92, FELADATOK #92, DT-F92a)

Generált nézet (`eszkozok/sqlite_epit.py`; DT28): az adatbázis nem commitolt, kézzel nem írható. A táblák az olvasói lapok eddig csak TSV-ből előálló blokkjait adják; mindegyik `meta`-sorral (sorszám és hash: `hash:<tábla>`) és táblaszintű licenccel (`tabla_licenc`, DT113) épül. Kulcs, ahol van: a **Károli-igehely**.

| tábla | forrás | licenc-kulcsok | tartalom |
|---|---|---|---|
| `token_macula` | `konkordancia/Macula_heber_*.tsv` | `Macula_heber` | héber token: `xml_id`, `igehely`, `sorszam` (Macula-szósorszám), `kk_mod`, `allapot`, `szo`, `lemma`, `strong` (SEMA 1.2) + `strong_nyers`, `strong_poz`/`strong_n`, `morf`, `szofaj`, `gloss`, `lxx_szo` (a **javított** görög alak, F115), `lxx_strong`, `lxx_szo_forras` (az upstream `greek` változatlanul), `lxx_szo_rahlfs` (minőségjelölés) |
| `lxx_token` | `konkordancia/LXX_OS/*.tsv` (a `szoalak` oszlopos könyvfájlok) | `LXX_OS` | LXX-szó: `lxx_igehely`, `kjv_vers`, `karoli_igehely` (üres: nincs Károli-megfelelő), `karoli_ok`, `pozicio`, `szoalak`, `lemma`, `morf`, `strong` (G + 4 számjegy), `strong_ok`, **`szovegforma`** (a forrásfájl neve: `genesis`, `daniel`, `daniel-theodotion`, …) |
| `lxx_versszam` | `LXX_OS` verskulcsa + `LXX_versificacios_terkep.tsv` (csak a nem kanonikus `terkep_ertek` oszlop; a térkép kulcsa `KJV_igehely`, a builder a KJV-kulcson illeszt, F91/DT143) | `LXX_OS`, `Versifikacios_tablak`, `Karoli_versmegfeleltetes` | minden ÓSZ Károli-versre legalább egy sor: `karoli_igehely`, `lxx_igehely`, `kjv_vers`, `forras` (csak `LXX_OS` / `nincs`), `megjegyzes`, **`szovegforma`** (az `LXX_OS`-sorokon a forrásfájl neve, egyébként üres), **`terkep_ertek`** (nem kanonikus: a `LXX_versificacios_terkep.tsv` értéke, ha a Károli-vers KJV-kulcsára (`LXX_OS` `igehely_kjv` vagy a `Karoli_versmegfeleltetes.tsv` `igehely_kjv`-je) van; Károli-kulcsos marad; **nem forrás**, hiányt nem tölt ki) |
| `bdb_alias` | `konkordancia/BDB_strong_alias.tsv` | `BDB`, `projekt_adat` (a `meta`-ban: `bdb_alias:licenc_osszetevok`) | másodlagos Strong → a BDB-szócikket hordozó Strong, `bdb_id`, `nyelv`, `cimszo`, `szoveg_hasonlosag` |
| `nave_vers` | `konkordancia/Nave_basokant.tsv` + a KJV→Károli megfeleltetés | `Nave_basokant`, `Karoli_versmegfeleltetes`, `LXX_OS` | Nave-téma × Károli-vers: `forras_sor`, `tema_id`, `tema`, `cimke`, `kapcsolat`, `nave_hely` (az eredeti KJV-hivatkozás), `igehely`, `tartomanyos` |

**Szabályok.**
- **`lxx_versszam`:** az egyetlen forrás az `LXX_OS` (`forras=LXX_OS`); ahol a Károli-versre nincs `LXX_OS`-sor, a sor `forras=nincs`, **üres `lxx_igehely`-vel, kitöltés nélkül** (CLAUDE.md 3. szabály). A versifikációs térkép **nem forrás** (DT-F92b: a közös versek 799 / 4906-án eltér az `LXX_OS`-től (F91 után, KJV-kulcson illesztve; előtte 1888 / 4889), más versbeosztásra utal); az értéke legfeljebb a nem kanonikus `terkep_ertek` oszlopban áll. Az eltérés-számok a `meta` `lxx_versszam:*` kulcsaiban és a `normalizalas_jelentes`-ben.
- **Párhuzamos LXX-szövegformák (ellenőri ÚJ-1).** A Dániel, a Bírák és a Józsué két-két LXX-szövegformában áll a `LXX_OS`-ben (`daniel` / `daniel-theodotion`, `judges` / `judges-vaticanus-b`, `joshua` / `joshua-vaticanus-b`; hasonlóan Bel és a Sárkány, Zsuzsanna, Tóbiás), és ugyanarra a Károli-versre esnek. Az `lxx_token` és az `lxx_versszam` ezért `szovegforma` oszlopot hordoz, és soha nem fésüli össze a formákat: egy Károli-versre formánként külön sor áll; az olvasónak formánként csoportosítania kell (`ORDER BY szovegforma, pozicio`), vagy egy formát kell választania. A `lxx_versszam:*` összegző számok sor-, nem vers-alapúak.
- **A térkép `NEM_MEGHATAROZHATO` sorai** (a `LXX_versificacios_terkep.tsv` első oszlopában, a `KJV_igehely`-ben KJV-kulcs helyett ez áll) a térkép nem forrás volta miatt tárgytalanok;  a számuk a `meta` `lxx_versszam:terkep_nem_meghatarozhato_sor` kulcsában és a `normalizalas_jelentes`-ben áll. A többi térkép-kulcs (KJV-kulcs) bontása: `lxx_versszam:terkep_kjv_kulcs` (különböző KJV-kulcs), `terkep_kjv_kulcs_karoli_nelkul` (nem váltható át Károli-versre), `terkep_karoli_kulcs` (a Károli-vers, amelyhez térkép-érték kerül), `terkep_ot_vers`, `terkep_nem_ot_vers`.
- **`nave_vers`:** a bontás szabálya az `eszkozok/nave_bontas.py`-ban él (KJV-szám szerint, a Károli-vers KJV-kulcsa: `LXX_OS` `igehely_kjv` → fejezet-eltolás → `Karoli_versmegfeleltetes` → Károli-szám). **Fejezet-szintű és igehely nélküli sor nem kerül bele** (a fejezet-nézet a `nave_basokant`-ból jön); a kihagyott sorok száma okonként a `meta` `nave_vers:kihagyott:<ok>` kulcsaiban és a `normalizalas_jelentes`-ben. Invariáns: `nave_vers:nave_basokant_sor` = `nave_vers:bontott_forras_sor` + `nave_vers:kihagyott_osszes` (semmi nem tűnik el némán).
- **`token_macula`:** a Macula–TAHOT illesztés vers+Strong alapon történik. Ahol ugyanaz a Strong egy versben többször áll, az illesztés **kétértelmű**; a `strong_n` a vers+Strong előfordulásainak száma, a `strong_poz` a fájlsorrend szerinti pozíció (a feloldás pozíció-sorrend). A kétértelmű csoportok száma: `meta` `token_macula:ketertelmu_vers_strong_csoport`. A „0 eltérés” ilyenkor nem jelent helyes illesztést. **`lxx_szo` / `lxx_szo_forras` / `lxx_szo_rahlfs` (F115, DT203):** a Macula héber `greek` attribútumában a χ és a ξ fel van cserélve (forrásoldali hiba); az import minden χ/ξ-t tartalmazó értékben felcseréli a két betűt (`χ↔ξ`, `Χ↔Ξ`). Az `lxx_szo` a javított alak, az `lxx_szo_forras` az upstream érték változatlanul (minden sorban), az `lxx_szo_rahlfs` üres a χ/ξ-mentes sorban, különben `rahlfs_igazolt` (a javított szó betűre és Strongra megvan a Károli-vers Rahlfs-LXX tokenjei között) vagy `nem_igazolt:<ok>` (`strong_elteres`, `csak_kisbetu`, `csak_ekezet`, `nincs_egyezes`, `nincs_karoli`, `nincs_lxx_vers`). A minőségjelölés **jelölés, nem feltétel**: a javítás minden érintett sorban megtörténik. Darabszámok: `meta` `token_macula:lxx_szo_rahlfs:<érték>`. A forrás: `naplok/MACULA_CHI_XI_felmeres.md`.
- **`szo_kis` / `hu_szo_kis`** (a `token_karoli`-ban, illetve a `token_par`-ban): a magyar szó kisbetűs, nem-betű/szám karakterektől mentes alakja (`sqlite_epit.szo_kis`); a keresés ezen indexel (`token_karoli`: `szo_kis, igehely, oldal, sorszam`). A kereső oldalon ugyanez a normalizálás alkalmazandó.

**A szótári alak táblái (F95, FELADATOK #95, DT141; forrás: `adat/szoto/karoli_szotari_alak.tsv`, SEMA 2.27; licenc: `szoto_tablak`, táblaszintű; az építő `_szotari_alak` metódusa a `token_karoli` után fut, minta módban is a teljes táblákkal):**

- **`szotari_alak`** — a TSV nyolc oszlopa változatlanul (`alak`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `modszer`, `szabaly_forras`, `regies_jegy`), 66 824 sor (a TSV adatsorai, a fejléc és a `#`-sorok nélkül; az első nem-`#` sor a fejléc, ezért a Károli valódi *alak* szava nem vész el). Kulcs: `alak` (`UNIQUE`, kis-/nagybetű-érzékeny), index még a `szotari_alak`-on. `modszer=simplemma` sor nem fordulhat elő. `meta`: `szotari_alak:forras_sor`, `hash:szotari_alak`.
- **`szotari_kereso`** (`keresoalak`, `alak`, `mezok`) — egy sor egy (NFC + kisbetűs `keresoalak`, `alak`) párra, 72 720 sor; `mezok` a találat forrása vesszővel: `szotari`, `mai`, `alapige`, `tovabbi` (a `tovabbi_elfogadhato` `|`-listájának elemei külön sor). Index `(keresoalak, alak)`. A keresett szót ugyanígy (NFC, kisbetű) kell normalizálni; **nem** `szo_kis` (a kötőjelet megtartja).
- **`szotari_token_kotojeles`** (`igehely`, `sorszam`, `alak`, `pontos_talalat`) — a `token_karoli` a kötőjeles alakot szétvágja (*Béth-Semes* → *Béth*, *Semes*); a tábla azokat a `hu` tokeneket köti a kötőjeles `alak`-hoz, amelyek 2–3 szomszédos tokenként, `-`-lel összefűzve egy `szotari_alak.alak`-ot adnak: 4 750 token (a teljes építésben), ebből `pontos_talalat=1` 3 684 (a darab önmagában is létező alak, ezért a pontos kulcs a darab saját szótári alakját adja), `0` 1 066 (a pontos kulcs nem talál, ez köti). **6 token nem oldható fel** (felfüggesztett kötőjel: *mogyoró-*, *fige-*, *faolaj-*, *-nek*, *méreg-*, *jog-*): dokumentált hiány. `meta`: `szotari_token:*`.
- **Kapcsolási kulcs:** `token_karoli.szo` = `szotari_alak.alak`, pontos (a `szo_kis` nem). Index: `token_karoli (szo, igehely, sorszam) WHERE oldal='hu'` (részleges; a lekérdezésnek tartalmaznia kell az `oldal='hu'` feltételt). Az ÚSZ 9 párosítatlan könyvére (Mt, Mk, Luk, Ján, ApCsel, Róm, 1–2Kor, Jel) a szótári alak megvan, token-kapcsolás nincs.
- **(c) keresési mód** (szótári alak VAGY Strong; a mért pontosság erre érvényes, l. 2.27): a lemma tokenjei ∪ azok a `hu` tokenek, amelyek `token_par.strong`-ja a lemma tokenjeinek nem nyelvtani Strong-jai közé tartozik (`grammatikai_strongok` szűrés). Mintalekérdezés és mérés: `eszkozok/olvaso_pilot/db_meres.py --szoto`. A gyakori lemmákon 173–874 ms (tízezres találathalmaz; egy tartalmas lemmán kb. 120 ms): a #76 felületen lapozás/`COUNT` kell; a 100 ms-os küszöb az (a) módra és a kereső táblára érvényes.

### 2.27 `adat/szoto/` — magyar szótövezés: minták, korpusz-lexikon, szabályellenőrzés, szótári alak (F94, FELADATOK #94, DT130)

A Károli szóalakjainak **szótári alakja** (lemma; nem nyelvtani szótő, DT130 (6)). Olvasás `split('\t')`, írás `'\t'.join()` (a `csv` modul tilos). Minden fájl első sora `# proveniencia: …` (vagy generált táblánál `# GENERÁLT: …`), utána további `#`-sorok állhatnak; az első nem-`#` sor a fejléc. A Strong-szám formátuma 1.2; több Strong `+`-szal.

**Minták** — `szoto_minta_1_fejlesztes.tsv` (213 alak, 1Móz 1–25), `szoto_minta_2_fejlesztes.tsv` (180 alak, Zsolt 1–41 + Ézs 40–55; a terv szerinti Gal/Ef/Zsid rész üres), `szoto_minta_3_ellenorzott.tsv` (113 alak, Jer/Jób/Luk/Jak); a negyedik (F94.3) `szoto_minta_4_fuggetlen.tsv` néven. Az 1–3. a repón kívüli előmérés átvétele (`eszkozok/szoto/minta_atvetel.py`, F94.0), a fejlécben a forrásfájl neve + sha256. **Kézi forrás** (a szótári alak modell- vagy felhasználói állítás), a javítás soronként, a `ellenorzes` frissítésével. Kulcs: `alak` (a mintán belül egyedi, kis-/nagybetű-érzékeny).

| Oszlop | Jelentés |
|---|---|
| `alak` | a Károli-szóalak, ahogy a szövegben áll (nagybetűvel is, ha úgy fordul elő) |
| `gyakorisag` | előfordulás a minta hatókörén belül (a proveniencia-sor mondja meg a hatókört); az M1 súlya |
| `kategoria` | réteg: `gyakori` \| `ragos_nevszo` \| `regies_ige` \| `regies_helyesiras` \| `ige_mai_alak` \| `tulajdonnev` (a mintavétel rétege, nem a helyes elemzés: pl. a 3. mintában a *Mutassa* `tulajdonnev` rétegből jött) |
| `szotari_alak` | a szótári alak Károli-helyesírással (DT130 (1)–(9)); névnél a Károli-átírás (5) |
| `szotari_alak_mai` | ugyanez mai helyesírással (*mely* → *amely*, *orca* → *arc*); a kereső mindkettőre talál (DT130 (1)) |
| `alapige` | igénél az igekötő és a képző nélküli ige (DT130 (4), (10)); üres, ha nem ige, vagy azonos a szótári alakkal (mind a négy mintában; az 1. és 2. mintát a DT135 E-7/E-8 erre a konvencióra igazította: a 2. minta igekötős igéi alapigét kaptak, az 1. minta azonos értékű alapigéi kiürültek — `naplok/SZOTOVEZES_meres.md` 5.1). |
| `tovabbi_elfogadhato` | a mérésben szintén helyes további alakok `\|`-vel (kétértelmű alak másik olvasata, DT130 (11); képzett igénél az alapige, (10)); üres, ha nincs |
| `ellenorzes` | **kötelező, nem üres:** `felhasznalo` (a felhasználó a sort ellenőrizte vagy eldöntötte) \| `modell_ellenorizetlen` (a felhasználó „mehet”-tel engedte, a sort nem nézte). **Nem „ellenőrizve”.** A mérés (`meres.py`) a negyedik mintán csak a `felhasznalo` sorokat veszi. Az `ellenorzes` oszlopot a felhasználó tölti, a modell soha (F94.3). |
| `indoklas` | a szótári alak indoklása (modell, manual); a 3. mintában a soronkénti, nem általános felhasználói döntés szó szerint, `[döntés: …]` alakban a végén |
| `pelda_igehely` | egy előfordulás (`IGEHELY`, 1.1) |
| `strong` | a példa-előfordulás Strong-párja(i) a repó Károli–Strong párosításából (`adat/karoli_strong/szavak_<könyv>.tsv`, SEMA 2.20; modell-kimenet, javaslat; `eszkozok/szoto/minta_strong.py`, F94.1b, illetve `minta4_ir.py`); üres, ha a token betoldás, vagy a könyv nincs párosítva (a 3. minta: a forrás nem hordozta; a 4. mintában az Mk, Ján, Róm, Jel) |

**Generált táblák (F94.1–.3; kézzel nem szerkeszthetők, a javítás a kivételtáblában vagy a szabályban történik):**

- `karoli_lexikon.tsv` — a hibrid korpusz-lexikona a `konkordancia/Karoli_1908.tsv`-ből (`eszkozok/szoto/lexikon_epit.py`; nem a `pardes.db`-ből, DT28): `alak`, `kisbetus` (kisbetűs előfordulás), `nagy_belul` (nagybetűs, mondat belsejében), `nagy_kezdo` (nagybetűs, mondatkezdő helyzetben: a vers első szava, vagy `. ! ? :` után).
- `szabaly_ellenorzes.tsv` — a hibrid helyesírási és tőváltó szabályainak Strong-támasza (`eszkozok/szoto/szabaly_ellenorzes.py`, az `adat/karoli_strong/`-ból): `tipus`, `szabaly`, `regi_alak`, `regi_token`, `par`, `par_token`, `tamasz`, `konyv`, `minosites` (`alátámasztva` \| `gyenge` \| `ellentmond` \| `nincs adat`), `pelda`.
- `karoli_szotari_alak.tsv` — a teljes Károli szótárialak-táblája (F94.3; `eszkozok/szoto/szotari_alak_epit.py`; a korpusz-lexikon minden írásmódjára egy sor, 66 824): `alak`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `modszer` (`kivetel` \| `szabaly` \| `lexikon` \| `nev` \| `k_tabla`; a `simplemma` érték a kiadott táblában nem fordulhat elő), `szabaly_forras` (`korpusz_strong`: a szabályellenőrzés alátámasztotta \| `manual`: általános helyesírás-történeti tudás, a *cz → c* \| `modell_ellenorizetlen` \| üres, ha nem szabály adta), `regies_jegy`. **A kiadott hibrid a C+K, simplemma nélkül (DT139)**: az előállító a simplemma importját letiltja. A fejlécben `# GENERÁLT: …` proveniencia-sor (a hibrid v3 sha256-ja, a K tábla és a lexikon hash-e), `# allapot:` sor a keresési mód figyelmeztetésével (a mért pontosság a (c) módra — szótári alak VAGY Strong — érvényes, a tisztán szótári alakos keresés gyengébb) és `# megjegyzes:` sor. Determinisztikus (hash-magtól és Python-verziótól független); kézzel nem szerkeszthető.
- **`regies_jegy` értékkészlete** (a régies alakot írja le, nem a mai megfelelőt): `mult.alanyi.E3` (-a/-e: *monda*), `mult.targyas.E3` (-á/-é: *teremté*), `mult.E1` (-ék nem -ik-es igén: *láték*; magas hangrendű igénél a T/3 tárgyassal azonos alakú, l. napló 16.), `mult.E3` (-ék -ik-es igén: *tartózkodék*, N-F94e), `mult.E2` (-ál/-él: *adál*), `mult.T1` (-ánk/-énk), `mult.T2` (-átok/-étek), `mult.T3` (-ának/-ének: *mondának*), `felszolito.E2` (-jál/-jél, -zzál …: *cselekedjél*), `hatarozoi_igenev` (-ván/-vén: *mondván*); üres: nem igei alak, mai igealak (*éljen*), és a kivételtábla jegy nélküli sora.

- `regies_jegy_minta.tsv` — a `regies_jegy` hibaarányának becslése (F94.7, DT140, N-F94h; `eszkozok/szoto/jegy_minta.py`): a szótárialak-tábla jegyes soraiból 100 elemű, rögzített magú (20261013) egyszerű véletlen minta. Oszlopok: `alak`, `szotari_alak`, `regies_jegy`, `modszer` (a táblából), `pelda_igehely` (az első Károli-vers, amelyben az alak pontosan így áll), `igei`, `jegy_helyes` (`igen` \| `nem` \| `ketes`; kézi besorolás a példavers alapján, modell-állítás), `ellenorzes` (`modell_ellenorizetlen`), `indoklas`. Kézi forrás (a besorolás a `jegy_minta.py` `BESOROLAS` szótárában); a hibaarány és a Wilson-intervallum a naplóban. Azért itt, nem a naplóban: soronkénti, újraellenőrizhető adat, amelyet a modernizálás (DT128) aranymintája bővíthet.

**K tábla** — `gyakori_alakok.tsv` (F94.2, DT137; a C+K mérési változat): a Károli 1908 leggyakoribb 400 alakja (kisbetűs + mondatkezdő előfordulás, kisbetűsítve; a sorhalmazt a `eszkozok/szoto/k_tabla_epit.py` gépileg választja), a szótári alak modell-javaslat a DT130 szerint (nem a simplemma kimenetéből). Oszlopok: `rang`, `alak` (kisbetűs), `gyakorisag`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato` (mint a mintáknál), `ellenorzes` (`modell_ellenorizetlen` \| `felhasznalo`; a felhasználó tölti, a modell soha; az újraépítés megtartja, ha a sor szótári alakja nem változott), `indoklas`. A szótári alak kézi forrása a `k_tabla_epit.py` `JAVASLAT` szótára (javítás ott).

### 2.28 `bdb_aranyminta.tsv` — a BDB-szeletelő aranymintája (F99, FELADATOK #99, M0)

A BDB-szócikkek **várt szerkezete** kézzel, a szeletelő (`eszkozok/olvaso_pilot/bdb_szelet.py`) mérésére: szakaszok (homonima-sor, jelöletlen al- és arámi címszó, fő rész), törzsek, jelentések, alpontok, használati csoportok, a jelentéscím és a csomópont szövegkezdete angolul és (ahol a `forditasok.tsv`-ben van) magyarul. **Kézi forrás**, nem generált: a minta a szócikk szövegének olvasásából készül, a szeletelő kimenete nem forrása (a projekt szabálya: előbb a minta, utána a mérés). Az első két sor `# proveniencia: …` és `# ellenorzes: …`, a harmadik a fejléc. Olvasás `split('\t')`, írás `'\t'.join()`. Az összevetés: `python eszkozok/olvaso_pilot/bdb_szelet_m0.py --arany` (a címekhez a szerver `blokkok` modulja kell, ezért a WSL venv-ben fut; nélküle a címek kimaradnak, és ezt kiírja).

| Oszlop | Jelentés |
|---|---|
| `strong` | a BDB-sor kulcsa (`H` + 4 jegy, mint a `BDB_teljes_unabridged.tsv` `Strong_padded` mezője) |
| `szakasz` | üres: a fő (a Strong-lemmához tartozó) szakasz; római szám (`II`, `III`): a római számmal jelölt homonima; héber szó: a jelöletlen al- vagy arámi címszó (az összevetés a mássalhangzó-vázon illeszt) |
| `resz` | DT174 (felhasználó, 2026-10-15): a szócikk római számos fő tagolása (`I`, `II` … — „I. preposition … II. conjunction”), külön a homonima-számtól; üres, ha nincs (a mai 658 sorban mind üres). Az összevetés kulcsa a `szakasz` és a `resz` együtt |
| `utvonal` | `<törzs>/<jelentés>/<alpont>/+<n>`; a hiányzó szint `-` (`-/1`: törzs nélküli 1. jelentés; `-/a`: jelentés nélküli alpont); a számozatlan, de önálló jelentés `-1`, `-2` (`Hiph'il/-2`, `okkod=szamozatlan_jelentes`); a törzs neve a szeletelő alakjában (`Pi'el`, `Hithpa'el`) |
| `szint` | `szocikk` (szócikkenként egy: a `kezdet_en` a címszó héber alakja, a `jel` a homonima-szám) \| `szakasz` \| `torzs` \| `jelentes` \| `alpont` \| `csoport` (használati csoport: a mondatkezdő bevezető, pl. `absolute`, `followed by`, `with`, vagy a zárójeles harmadik szint `(1)`, `(a)`, `(β)` — mindenhol csoport, az OCR-torzult alak (`-1`, `-2`, `3as`) is jelölő; a bevezető-lista a DT167) \| `utalo` (utaló címszó saját tartalom nélkül, pl. „I. עַלְוָה transposed from עַוְלָה”; nem szakasz, az összevetés nem csomópontként kezeli) \| `kihagy` (az útvonal alatti csomópontokat az összevetés nem nézi: a forrás hiányos, vagy a szint nincs rögzítve; a `megjegyzes` mondja meg, miért) |
| `jel` | a jelölő (`1`, `a`, `Qal`, `II`, a csoport bevezetőjének kulcsa) |
| `okkod` | üres, vagy gépi okkód: `utalo_cimszo` (az `utalo` sor), `szamozatlan_jelentes` (a számozatlan önálló jelentés) |
| `kezdet_en`, `kezdet_hu` | a csomópont saját szövegének eleje (a jelölő után), az összevetés horgonya; üres: nem vizsgált (a magyarnál: nincs fordítás, vagy a horgony nem ellenőrzött) |
| `cim` | a várt jelentéscím (a szócikk saját szavai, a zárójeles részek nélkül, az első igehelyig, pontosvesszőig vagy kettőspontig); üres: nem vizsgált. Az összevetés a héber betűk és az írásjelek nélkül hasonlít |
| `megjegyzes` | miért ez a szerkezet (ál-jelölők, forráshibák, hivatkozásként álló törzsnevek) |
| `ellenorzes` | `modell_ellenorizetlen` (a modell készítette vagy javította, átnézés nélkül) \| `fuggetlen_ellenor` (a független ellenőr átnézte, `naplok/ELLENOR_F99_minta.md`, az eltéréseket a felhasználó eldöntötte) \| `felhasznalo` (a felhasználó ellenőrizte); a modell `felhasznalo`-t soha nem ír |
| `proveniencia` | `manual` (nem lekérdezés; 1.5) |

Kulcs: `strong` + `szakasz` + `resz` + `utvonal` + `szint`. Állapot (F99.6, 2026-10-15, a független ellenőr jelentése és a felhasználó döntései után): 32 szócikk (14 magyar fordítással), 658 sor (184 csoport, 1 utaló); 607 sor `fuggetlen_ellenor`, 51 `modell_ellenorizetlen` (az új vagy javított sorok; a H6440, H7307, H0430 a F99.7-től, a felhasználó elfogadása után, `fuggetlen_ellenor`).


### 2.29 `bdb_vers_jelentes.tsv` — a BDB igehely-hivatkozásai jelentésponthoz kötve (F99, FELADATOK #99, M2)

**Generált** (`python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts <nap>`; kézzel nem szerkeszthető; azonos bemenettel és `--ts`-sel
bájtra azonos, a `--ellenoriz` és a `teszt_bdb_vers_jelentes.py` ellenőrzi). Az angol BDB (`konkordancia/BDB_teljes_unabridged.tsv`)
minden szócikkének minden igehely-hivatkozására egy sor, a szócikkön belüli sorrendben. **Lexikai index, nem study-adat:** keresési
találatból nem lehet közvetlenül study-sor (CLAUDE.md 2. szabály); bármely felhasználása a `jeloltek.tsv`-n megy át. A szabályok a DT166
döntése szerint (felhasználó, 2026-10-15). Az első két sor `# GENERÁLT: …` és `# forras: …` (a bemenetek hash-e és a kód hash-e), a harmadik a
fejléc. Olvasás `split('\t')`. A pardes.db-be az `adat/` tábláival együtt kerül (`sqlite_epit.py`, licenc: BDB + Macula_heber + projekt_adat).

| Oszlop | Jelentés |
|---|---|
| `strong` | a BDB-sor kulcsa (`Strong_padded`) |
| `bdb_id` | a Strong OSHL BDB-azonosító(i) (`OSHL_lexikalis_index.tsv`), vesszővel; üres, ha nincs |
| `sorszam` | a hivatkozás sorszáma a szócikkben (1-től) |
| `poz` | a hivatkozás kezdete a szeletelő szövegében (`bdb_szelet.lapit`: sortörés szóközre, „1.a” → „1. a.”), karakterben |
| `nyers` | a hivatkozás a forrásban (`Gen 44:19`, `17:4`, a vers-folytatásnál `, 25`) |
| `konyv_feloldas` | `kiirt` (könyvvel) \| `orokolt` (könyv nélküli fejezet:vers, a megelőző könyv a szócikk elejéig visszafelé) \| `folytatas` (vesszős vers-folytatás: „Gen 18:18, 25” → 18:25) \| `feloldhatatlan` (nincs megelőző könyv, vagy az örökölt könyvben nincs ilyen fejezet: `orokles_hibas`) |
| `mt_vers` | a feloldott MT-vers (Károli-könyvrövidítéssel; a BDB az MT számozását követi); üres a kiszűrt és a könyv nélküli sorban |
| `karoli_vers` | a Károli-vers a `Karoli_1908.tsv` kulcsa szerint (a Siralmak `Sir`); **üres, ha nincs** (kiszűrt sor, nem létező vers, Károli-megfelelő nélkül): kitöltés nélkül |
| `vers_feloldas` | `azonos` \| `atkulcsolt` (a Macula `karoli` oszlopa szerint más Károli-vers) \| `azonos_f85` (az F85-ben elvetett Macula-régió: azonos kulcs) \| `atkulcsolt_f85` (DT173 (b): az F85 esetlistája — `naplok/F85_esetlista.tsv`, WLC (MT) → Károli, J ≥ 0,5 — szerinti Károli-vers) \| `atkulcsolt_karoli_szoveg` (DT179, felhasználó, 2026-10-16: az Ézs 3 — MT 2:22 → K 3:1, MT 3:n → K 3:(n+1) —, forrása a Károli-szöveg (`Karoli_1908.tsv`: a Károli Ézs 3:1 az MT 2:22 szövege) és a TAHOT megerősítése, nem az F85 esetlista) \| `azonos_tahot` (a Károli-megfelelő nélküli sor az azonos számú Károli-versre került, mert a TAHOT ott hordozza a szót; okkód `karoli_tahot`) \| `atkulcsolt_bizonytalan` (a Károli-versmegfeleltetés MT-osztályú sora mást mond) \| `nem_letezo_vers` (az MT-ben nincs ilyen vers) \| `nincs_karoli` \| `usz` (újszövetségi hely, nem kulcsolva) \| üres (kiszűrt vagy könyv nélküli sor) |
| `szakasz` | a jelentéspont szakasza: a fő címszó **saját római száma** (a forrás „I. יֶ֫תֶר noun …” fejénél `I`; ha nincs, üres), egy további homonima-címszó római száma, a szócikk **római számos fő tagolása** (`I`, `II` … — pl. „I. of man … II. of God …”; igénél a törzsön belüli, a rákövetkező törzs már a fő címszóé), vagy a jelöletlen második címszó `h:<mássalhangzó-váz>`-a. A római szakasz a jelentéspont része (F99 M2, felhasználó, 2026-10-15; az összevetés szabálya: `naplok/BDB_SZELETELO_M0.md` 9.5) |
| `resz` | DT174 (felhasználó, 2026-10-15): a szócikk **római számos fő tagolása** (`I`, `II` …), külön a homonima-számtól: „H5704. ad III. עַד … I. preposition … 3 …” → `szakasz` `III`, `resz` `I`, `utvonal` `-/3`; igénél a tagolás a törzsön belüli, a rákövetkező törzs (Niph`al …) már a címszóé (`resz` üres). Üres, ha a helynek nincs fő része |
| `utvonal` | a jelentéspont: `<törzs>/<jelentés>/<alpont>` (hiányzó szint `-`, mint az aranymintában); `fej` (a csomópontokon kívül: címsor, nyelvi háttér, alaktan); `tagolatlan` (a hivatkozás **szakaszában** nincs törzs, számozott jelentés vagy alpont: a hivatkozás az egész szakaszhoz tartozik; a `fej` és a `tagolatlan` a szakasz szerint dől el). A használati csoport (M3) még nem része |
| `okkod` | vesszővel: `nem_bibliai`, `sigla_tapadt`, `sigla_lista` (a megnevezett kommentár-siglák listája: Schrader COT, Driver, Mésa-felirat, Targum, Fleischer/Delitzsch; DT175) (kiszűrve), `sigla_kozel`, `tobbertelmu`, `ismeretlen_alak`, `nincs_elozmeny`, `orokles_hibas` (az örökölt könyvben nincs ilyen fejezet: a könyv nem öröklődik, könyv és vers nélkül; F99, seed-100 M013) (bizonytalan, a táblában marad), `sigla_igazolt` (DT176: sigla melletti hivatkozás, amelynek versében a TAHOT hordozza a szócikk Strong-számát — bibliai, nem szűrt), `nem_letezo_vers`, `nincs_karoli`, `tobb_karoli_vers` (a Macula több Károli-verset ad; az első áll), `usz`, `karoli_tahot` (DT173 kiegészítés: az azonos számú Károli-vers a TAHOT szerint), `forras_hiba` (a BDB forrásszövegének hibás igehelye, kézi döntéssel azonosítva; a sor a forrást rögzíti, nem szűrt; F99, felhasználó, 2026-10-15); üres: feloldott bibliai hivatkozás |
| `szurt` | `1`: álhivatkozás, kiszűrve: `nem_bibliai` (DT166 (1)), és a sigla melletti hivatkozás (`sigla_tapadt`, `sigla_kozel`, `sigla_lista`), ha a TAHOT szerint a vers NEM tartalmazza a szócikk Strong-számát (DT176, felhasználó, 2026-10-15); `0`: nem |
| `proveniencia` | **minden sorban:** `scope=<Strong> \| forras=bdb_vers_jelentes.py (fejléc) \| ts=<nap>` (gépi; `manual` nem lehet). A kód-hash (a `bdb_szelet.py`, a `bdb_vers_jelentes.py`, a `bdb_konyv_javit.py` és a `normalizal.py` LF-re normalizált tartalmáé) és minden bemenet hash-e (BDB, Macula_heber_*, Károli-versmegfeleltetés, Karoli_1908, F85_macula_elvetve, F85_esetlista, OSHL-index, Strong_szotar, TAHOT; ELLENOR_F99 3–4.) **csak a fájl `# forras:` fejlécsorában** áll (DT172, felhasználó, 2026-10-15; eltér a brief soronkénti `bdb_szelet@<commit>` alakjától: így egy szeletelő-javítás nem írja újra az összes sort) |

Kulcs: `strong` + `sorszam`. A jelentéspont a gépi szeletelés szerint áll (a szeletelő ismert hibái, `naplok/BDB_SZELETELO_M0.md` 2.3, öröklődnek); a pontosságát az M2 ⛔ 200-as mintája méri.


### 2.30 `bdb_szakaszok.tsv` — a BDB jelölt szövegrétege, szakaszonként (F107, FELADATOK #107, DT225, DT227)

**Generált** (`python eszkozok/bdb_jelolt/bont.py --ts <nap>`; kézzel nem szerkeszthető; azonos bemenettel és `--ts`-sel bájtra
azonos, a `--ellenoriz` és az `eszkozok/bdb_jelolt/teszt_bont.py` ellenőrzi). A BDB-szócikkek tagolása (cím, fej, jelentéspont,
alpont, alcímszó, `section`/`remarks`) **adatként**, a nyers forrás jelölőiből, nem a sima szövegből visszafejtve. Forrás (DT225 (c),
felhasználó, 2026-10-18): **a szöveg és a bekezdés-tagolás** a `konkordancia/lexikonok_nyers/DictBDB.json`-ból (közkincs, DT225 (i));
**a `bdb_id`, a szócikkhatár és a `section`/`remarks` osztály** a `konkordancia/lexikonok_nyers/BDB.lexicon`-ból, illesztéssel — a lexikon
licence tisztázatlan, ezért **csak azonosítót és szerkezeti metaadatot ad, szöveget nem**. Egy sor = a JSON Strong-elemének egy bekezdése
(`<p>`, `<p style="sub1">`, vagy bekezdésen kívüli szövegdarab), a forrás sorrendjében. Az első két sor `# GENERÁLT: …` és `# forras: …`
(a két nyers fájl és a kód hash-e), a harmadik a fejléc. Olvasás `split('\t')`. **Lexikai forrásréteg, nem study-adat:** keresési
találatból nem lehet közvetlenül study-sor (CLAUDE.md 2. szabály).

| Oszlop | Jelentés |
|---|---|
| `strong` | a JSON-kulcs `H` + 4 jegyre kitöltve (mint a `BDB_teljes_unabridged.tsv` `Strong_padded`-je). A JSON mind a 8 090 Strongja; a TSV 9 JSON-kulcs nélküli sora (F57: H0747, H4123, H4725; F72: H1753, H3367, H3848, H6433, H7560, H8065) **nincs** a táblában (a szövegük a lexikonból jött, amely szöveget nem ad; explicit hiány) |
| `bdb_id` | az illesztett BDB-szócikk (`BDB<n>`, a `BDB.lexicon` kulcsa); **üres**, ha a Strong illesztése `reszleges` / `sikertelen` / `csonk` (DT227 (a): explicit hiány, nem kitöltés) |
| `sorszam` | a bekezdés sorszáma a Strong-elemben (1-től; az 1. a cím) |
| `alszocikk` | a szócikken belüli jelöletlen alcímszó (`<p style="sub1">`, amely nem új BDB-szócikk) sorszáma; `0`: a fő címszó |
| `szakasz` | a homonima-szakasz római száma (`I`, `II` …; aranyminta 2.28 `szakasz`): a szócikk-eleji római fej, és ha a szócikk első római feje `I.`, és előtte nem volt szám-, betű- vagy törzsfej, a további római fejek is (DT229 (a) (2), H6440); üres, ha nincs |
| `resz` | a római számos fő tagolás (`I`, `II` …; aranyminta 2.28 `resz`, DT174): a szócikkön belüli római fej, ha nem homonima-szakasz (l. `szakasz`; pl. H3068, H8478) |
| `utvonal` | `<törzs>[.<nagybetű>]/<szám>/<betű>[/<zárójeles>]`, a hiányzó szint `-` (pl. `-/1/-`, `Qal/2/a`, `Hiph'il.A/1/a`); a törzsnév a szeletelő alakjában (`Pi'el`); különleges érték: `cim`, `fej` (a szócikk első bekezdése, és a fej utáni, jelölő nélküli bekezdés). Az alap a 2.28–2.29 formátuma, a #102 két bővítésével (nagybetűs csoport, zárójeles/görög szint). **Nincs kanonikus kulcsként befagyasztva** (DT190 🟡) |
| `jelolo` | `cim` \| `fej` \| `point` (félkövér szerkezeti fejjel nyíló bekezdés) \| `bekezdes` (fej nélküli bekezdés a szócikk belsejében: az útvonal az előzőé) \| `alcimszo` \| `section` / `remarks` (a lexikon osztálya; elsőbbséget kap a `point` előtt, az útvonal és a `jel` ilyenkor is a fejet írja le) |
| `jel` | a bekezdés elején álló félkövér fej a forrás alakjában (`1`, `2. a.`, `Hiph`il A.`, `II.`); üres, ha nincs |
| `gyakorisag` | a bekezdés `<sub>` számai vesszővel, a forrás sorrendjében (a gyakoriságszám; a `_convert_bdb.py` ezt `_N` alakban a szövegbe írta) |
| `szoveg` | a bekezdés sima szövege a `jel` után, a `_convert_bdb.py` tisztításával, egy eltéréssel: a `<sub>` kimarad. **A nyers JSON szövege, javítás nélkül** (a `bdb_forras_javitas.tsv` javításai NEM alkalmazódnak; l. lent) |
| `illesztes` | a Strong illesztési kategóriája (a `bont.py` docstringje): `egyezik` (az első bekezdés szócikk-kezdet, és minden szegmens szólefedése mindkét irányban ≥ 0,90) \| `szocikk_resze` (a JSON-szegmens ≥ 0,90-re a szócikkben, de a szócikk más Strongok részét is hordozza; `bdb_id` kitöltve) \| `reszleges` \| `sikertelen` \| `csonk` (a JSON-elem csak a cím folytatása) |
| `forras` | `DictBDB.json:<JSON-kulcs>#<blokkindex>`; a blokk a bontó blokkja: a bekezdésen belüli (és a bekezdés végi) valódi félkövér fej új blokkot nyit (DT229 (a) (3)), ezért egy JSON-bekezdés több blokk is lehet |
| `forras_hash` | a bekezdés nyers HTML-jének SHA-256-ja, 16 jegy (az elavulás jele) |
| `proveniencia` | `scope=<Strong> \| forras=bdb_jelolt/bont.py (fejléc) \| ts=<nap>`; a bemenetek és a kód hash-e a `# forras:` fejlécsorban (a 2.29 mintája) |

Kulcs: `strong` + `sorszam` (egyedi; a `strong` + `bdb_id` + `utvonal` a jelöletlen bekezdések miatt nem egyedi — a DT190 kulcsához ez döntendő).
Állapot (F107.29, 2026-10-18): 36 621 sor; illesztés: `egyezik` 7 916, `szocikk_resze` 30, `reszleges` 94, `sikertelen` 15, `csonk` 35 Strong. A fej-felismerés szabályai (DT229 (a)): a fejet közvetlenül „)”, „,”, „;”, „]” követi → hivatkozás, nem fej; a homonima-szakasz (`szakasz`); a bekezdésen belüli fej (előtte „.”, „—”, „:”, „;” vagy „,”, utána nem „)”, „,”, „;”, „.”, „]”, törzsnév után nem szám; a bekezdés végén csak ha a következő blokk fejjel nyit); a szóköz nélküli kombinált fej („1.a.”) két token A negyedik szabály (DT230 (a), F107.29): a JSON blokk eleji feje hivatkozás, ha a `BDB.lexicon` ugyanazon szócikkében ugyanez a fej a szövegen belül, hivatkozó szó után áll; a fejsorbeli törzsnév („verb Pa`el”) a törzsállapot. Mérés (F107.29): aranyminta 411 / 425 (96,7%), a `forras_hiba` nélkül 411 / 416 (98,8%, elfogadva: DT233; a maradék: N-F107c), seed-101 9 / 13 (9 / 10), korpusz 85,4% (`naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 2.3, 4.5, 4.8).

**A `szoveg` és a javítótábla viszonya (DT231 (d), felhasználó, 2026-10-18):** a tábla a nyers szöveget hordozza, a javítás külön
táblában áll (`bdb_forras_javitas.tsv`, 2.31), a `strong` + `sorszam` (+ `szo_sorszam` / `elofordulas`) kulccsal; a javított szöveg **nézet**
(`eszkozok/bdb_jelolt/nezet_general.py`: a tábla + a `javitva` sorok), a táblát a javítás nem írja át. A `BDB_teljes_unabridged.tsv` változatlan;
a cseréje a nézetre és az olvasók átállása külön, `/befogad`-dal felvett feladat.


### 2.31 `bdb_forras_javitas.tsv` — a BDB forráshibáinak javítótáblája (F107, FELADATOK #107, DT228)

**Generált** (`python eszkozok/bdb_jelolt/forras_javit.py --ts <nap>`; kézzel nem szerkeszthető; `--ellenoriz`; teszt:
`teszt_bont.py`). A nyers forrásban (`DictBDB.json`) is hibás helyek javítása **a nyers fájl és a szakasztábla érintése nélkül** (a
`bdb_igehely_javitas.tsv`, 2.23 mintájára). Négy hibaosztály (`hiba`): **`pe_mem`** — a `DictBDB.json` a dagesses pét dagesses memként írja
(0 dagesses pe; `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 2.2); a 2.30 `szoveg` mezőjének minden dagesses memje egy sor, a javított alak
**szabályból** jön (a mem → pe csere), a `BDB.lexicon` csak igazol (DT225 (i)); **`hivatkozas`** — a TSV F34/F46 hivatkozás-javításai
(DT231 (d)); **`jelolo_hianyzik`** és **`hamis_jelolo`** — kézi sorok a mindkét nyers forrásban igazolt szerkezeti forráshibákról (DT229 (b)). Első két sor `# GENERÁLT` / `# forras`, a harmadik a fejléc;
a héber alakok NFD-ben. Olvasás `split('\t')`.

| Oszlop | Jelentés |
|---|---|
| `strong`, `sorszam`, `bdb_id` | a 2.30 sora (kulcs) és illesztett szócikke |
| `hiba` | a hibaosztály: `pe_mem` (generált) \| `hivatkozas` (generált; DT231 (d): a `BDB_teljes_unabridged.tsv` utólagos F34/F46 hivatkozás-javítása, amely a nyers JSON-ban nincs — a TSV és a JSON (`_convert_bdb.py` szerint) szóköz szerinti tokenjeinek eltérő szakasza) \| `jelolo_hianyzik` (a szerkezeti jelölő a nyers forrásban hiányzik: pl. a „Qal” sima szöveg) \| `hamis_jelolo` (a nyers forrás fejében téves elem áll: pl. „Niph`al 6.”, „2. g.”) |
| `szo_sorszam` | `pe_mem`: a héber szó sorszáma a `szoveg` mezőben (1-től, NFD után a `[\u0590-\u05ff]+` szavak között); kézi sorban üres |
| `elofordulas` | `pe_mem`: a dagesses mem sorszáma a szón belül (1-től); `hivatkozas`: a `forras_alak` hányadik egész-token előfordulása a Strong nézet-szövegében (a sorok `jel` + `szoveg`-e egy szóközzel; a `sorszam` az a táblasor, amelyben áll); kézi sorban üres |
| `forras_alak` | `pe_mem`: a szó a JSON-ban (NFD); `hivatkozas`: a JSON-szakasz (pl. `Gen`, `Numbers 34:43;`); kézi sorban a nyers JSON rövid részlete |
| `javitott_alak` | `pe_mem`: a javított szó (NFD), csak `javitva` sorban; `hivatkozas`: a TSV-szakasz (pl. `Psa`, `Num 33:43;`); kézi sorban a várt szerkezet (útvonal, pl. `Qal/1`) |
| `allapot` | `javitva` (a pe-s alak — egy vagy a szó minden dagesses memjét cserélve — az illesztett szócikk héber szavai között áll, a mem-es nem) \| `valodi_mem` (a mem-es alak áll a szócikkben: nem hiba) \| `jelolt_marad` (egyik sem igazolt, vagy a sornak nincs `bdb_id`-je: nincs javítás) \| `kezi` (DT229 (b): kézi sor egy szerkezeti forráshibáról, amely a `DictBDB.json`-ban ÉS a `BDB.lexicon`-ban is igazolt; a sor a forrás-hibát rögzíti, a táblát nem írja át) |
| `indok` | a döntés oka, magyarul |
| `proveniencia` | generált sor: `scope=<Strong> \| forras=bdb_jelolt/forras_javit.py (fejléc)[…] \| ts=<nap>` (a `hivatkozas` sorban a forrásjavítás is: F34 / F46 / F46.6); kézi sor: `manual` (a forrás és az indok az `indok` mezőben; a kézi tételek a `forras_javit.py` `KEZI` listájában, a `sorszam` horgony szerint keresve) |

Összevetés: NFD, kantilláció (U+0591–U+05AF), meteg, paszek, szof pászuk és U+200E nélkül, U+05BA = U+05B9. Állapot (F107.49, 2026-10-18):
7 202 sor: `pe_mem` 6 781 (`javitva` 3 823 (1 428 Strong), `valodi_mem` 2 402, `jelolt_marad` 556, ebből 112 `bdb_id` nélküli sorban) + `kezi` 9 (H0559 2, H0539 2, H3318, H4900, H1242, H6440 2) + `hivatkozas` 412 (mind `javitva`; forrás: F34 159 — `naplok/F34_M2_csere.tsv` JAVIT —, F46 250 — `naplok/BDB_KONYVFELOLDAS_csere.tsv` / `_kezi.tsv` —, F46.6 3 — git `6400b5a7`, „Phoenician” → „Pharaoh”, a csere-naplóban nem szerepel). A kész fordítások érintettsége: N-F107a. A sima szöveges nézetet a `eszkozok/bdb_jelolt/nezet_general.py` állítja elő (`--pe-mem` a pe/mem javítással is); a kimenet nem a repóba és nem a `BDB_teljes_unabridged.tsv`-be íródik (DT231 (d)).



### 2.32 `bdb_szakasz_hu.tsv` — a kész magyar BDB-fordítás illesztése a szakaszokhoz (F107, FELADATOK #107, 7. lépés)

**Generált** (`python eszkozok/bdb_jelolt/hu_illeszt.py --ts <nap>`; kézzel nem szerkeszthető; `--ellenoriz`; teszt: `teszt_bont.py`). A kész
magyar BDB-fordítás (`adat/forditasok.tsv` BDB-sorai Strongonként a közös összefűzőn át, 2.14 — F128 előtt: az utolsó nem üres `forditas_hu`, a mai adaton azonos eredménnyel; **a fájl nem íródik**, az a #38-é)
szakaszhatárai a szakasztábla (2.30) soraihoz illesztve, a #38 szakaszonkénti fordításának (DT181 (b)) előkészítéseként. Soronként a
szakasztábla egy sora (csak a lefordított Strongok). Első két sor `# GENERÁLT` / `# forras` (a bemenetek és a kód hash-e), a harmadik a
fejléc. Olvasás `split('\t')`.

| Oszlop | Jelentés |
|---|---|
| `strong`, `sorszam`, `bdb_id`, `szakasz`, `resz`, `utvonal`, `jel` | a 2.30 sora (kulcs: `strong` + `sorszam`) |
| `kategoria` | `illeszkedik` (a sor összes fej-jelölője — szám, betű, római, zárójeles, törzsnév — sorrendben megvan a magyarban) \| `horgonnyal` (a jelölő nem illeszkedett, de a sor szövegének első fejezet:verse a magyarban az előző és a következő illesztett szakasz között megvan; a szakasz a sor saját jelölőjének ott álló utolsó előfordulásától, ennek híján a megelőző mondathatártól indul) \| `elakad` (egyik sem: a sor magyar szövege az előző szakaszban van) \| `jelolo_nelkul` (a sornak nincs fej-jelölője: cím, fej, fej nélküli bekezdés, alcímszó — az előző szakaszban halad; a fej a magyar szöveg elejét kapja) |
| `horgony` | `illeszkedik`: a jelölők (pl. `2 a`, `T:Qal`); `horgonnyal`: a fejezet:vers; különben üres |
| `hu_kezdet`, `hu_hossz` | a szakasz kezdete és hossza a `forditas_hu`-ban (karakter); üres, ha a sornak nincs saját szakasza |
| `szoveg_hu` | a magyar szakasz (a sor horgonyától a következő horgonyig, a széleken szóköz nélkül); üres, ha nincs saját szakasza |
| `forditas_forras_hash` | a fordítássor `forras_hash`-e (a TSV `Teljes_szocikk` SHA-1-e a fordításkor): az elavulás jele (DT231 (d): addig a változatlan TSV-hez kötött). **Szakaszonként fordított Strongnál** (F128, DT291 (a): a magyar szöveg a közös összefűzőből, 2.14): a token nélküli forrásnézet (`szakasz_bemenet.nezet`, a szakaszok javított szövege egy szóközzel) SHA-1-e |
| `proveniencia` | `scope=<Strong> \| forras=bdb_jelolt/hu_illeszt.py (fejléc) \| ts=<nap>` |

Állapot (F107.38, 2026-10-18; DT232 (d): a magyar jelölő-felismerés bővítése az illesztőben — törzsnév mindkét oldalon a bontó törzslistájából, a forrás alakjában, a magyaros alakokkal és a raggal, kulcs a kanonikus név (`Hithpa'el`, `Pe'al`); betű j-től csak tagolásjel után, a szám utáni „k.” nem; a kérdőjel utáni szám): 674 Strong, 9 664 sor; soronként `illeszkedik` 6 395, `horgonnyal` 202, `elakad` 606, `jelolo_nelkul` 2 461 (F107.34: 6 210 / 271 / 618 / 2 565). Strong-szinten a kapu szigorú illesztőjével (a kapu regexei, mint a kiinduló mérés) változatlanul `illeszkedik` 380, `tagolatlan` 94, `elakad` 200 (kiinduló: 355 / 89 / 230); horgonnyal kiegészítve `illeszkedik` 409, `horgonnyal` 85, `elakad` 98, `tagolatlan` 82 (F107.34: 385 / 105 / 101 / 83). A maradék `elakad` Strongok a #38 következő adagjában szakaszonként újrafordítandók (DT232 (c); lista: N-F107b, `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 7.1); kézi illesztés nincs.
---

### 2.33 `motivum_kapcsolatok.tsv` — motívum–motívum kapcsolatok (F127, FELADATOK #127, DT277)

Kulcs: `id_a` + `igehely_a` + `id_b` + `igehely_b`, **rendezett párként** (`id_a` < `id_b`
betűrendben). Szimmetrikus: a sor mindkét motívum lapján megjelenik (generált „5/b.
Kapcsolódó motívumok” blokk, DT277 (α)). Más tengely, mint a `kapcsolatok.tsv` (2.3, a
motívumon belüli igehely-párok); a 4. szakasz névütközése ugyanezt mutatja. **Minden sor
mögött `beépítve` motívumközi jelölt áll** a `jeloltek.tsv`-ben (2. szabály; `ellenoriz.py`
2/b.): a `dontes_ref` arra a sorra mutat, és a pár egyik oldala a jelölt `id`/`igehely`-e, a
másik a `cel_id`/`cel_igehely` egyik eleme.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id_a` | motívum-id | ✔ | |
| `igehely_a` | `IGEHELY` | ✔ | |
| `alpont_a` | alpont-azonosító | | DT277 (C): csak létező alpont-azonosító (ma egy sincs: az alpont adatosítása a #123 ALVIL-001-ciklusáé vagy külön séma-tételé); üres = a motívum egésze. |
| `id_b` | motívum-id | ✔ | |
| `igehely_b` | `IGEHELY` | ✔ | |
| `alpont_b` | alpont-azonosító | | Mint az `alpont_a`. |
| `tipus` | zárt | ✔ | `szomszédos` (ugyanabban a fejezetben vagy beszédben áll) \| `közös_igehely`. A `tematikus` a DT277 szerint most nem része a készletnek. |
| `funkcio` | szabad szöveg | | |
| `bizonyossag` | zárt | ✔ | `magas` \| `közepes` \| `alacsony`. |
| `pardes_szint` | `PARDES_SZINT` | | |
| `indoklas` | szabad szöveg | | A mért szomszédság; a közös fejezet vagy szókészlet önmagában nem bizonyít szándékos utalást. |
| `dontes_ref` | szöveg | ✔ | `jeloltek.tsv;<id>;<igehely>;motivumkozi;<cel_id>` — a döntést hordozó jelölt-sor kulcsa. |
| `proveniencia` | `PROVENIENCIA` | ✔ | |

### 2.34 `thayer_szakaszok.tsv` — a Thayer jelölt szövegrétege, szakaszonként (F132, FELADATOK #132, DT327–b)

**Generált** (`python eszkozok/thayer_jelolt/bont.py --ts <nap>`; kézzel nem szerkeszthető; azonos bemenettel és `--ts`-sel bájtra
azonos, a `--ellenoriz` és az `eszkozok/thayer_jelolt/teszt_bont.py` ellenőrzi). Forrás (DT327 (b), felhasználó, 2026-10-25):
**a szerkezet** (bekezdéshatár, fej, útvonal) a `konkordancia/lexikonok_nyers/Thayer.lexicon`-ból (`Lexicon(Topic, Definition)`, HTML;
a formázási réteg licence nem tisztázott, ezért innen csak szerkezet és azonosító jön, szöveg nem); **a szöveg** a
`konkordancia/Thayer_teljes.tsv` `Teljes_szocikk`-jéből, illesztéssel (a szakasz szövege a TSV-szöveg szelete). Egy sor = a szócikk egy
bekezdése: a `<p>`, `</p>`, `<div>`, `</div>` jelölők közötti, címkék nélkül nem üres HTML-darab, a forrás sorrendjében (a forrásban
helyenként egymásba ágyazott vagy lezáratlan `<p>` áll, ezért a határ a jelölő). Az első két sor `# GENERÁLT: …` és `# forras: …` (a két
bemenet és a kód hash-e), a harmadik a fejléc. Olvasás `split('\t')`. **Lexikai forrásréteg, nem study-adat:** keresési találatból nem
lehet közvetlenül study-sor (CLAUDE.md 2. szabály).

| Oszlop | Jelentés |
|---|---|
| `strong` | `Strong_padded` (`G0012`); a lexikon `Topic`-ja (`G12`) az `eszkozok/thayer_jelolt/kulcs.py` `strong_pad` függvényével normalizálva (DT328 (4): egyetlen függvény) |
| `sorszam` | a bekezdés sorszáma a szócikkben (1-től; az 1. a cím) |
| `utvonal` | `<felső>/<szám>/<betű>`, a hiányzó szint `-` (pl. `-/1/-`, `II/1/a`, `A.I/2/-`); a felső szint a nagybetűs fej (`A.`, sima szöveg, csak a sorban következő betű) és a római fej (`<span class="lexheading">I.</span>`) ponttal; különleges: `cim` (a `<b>G… — …</b>` címsor; újabb címsor a fejállapotot törli), `fej` (a cím után, az első fej előtti bekezdés). Fej nélküli bekezdés az előző útvonalát örökli |
| `jel` | a bekezdés elején álló fej a forrás alakjában (`1.`, `a.`, `I.`, `A.`); üres, ha nincs. A forrásban bekezdésen belüli fej nem fordul elő (F132 M1 felmérés) |
| `szoveg` | a bekezdés szövege a `jel` után, a `Thayer_teljes.tsv` szövegéből (a szóközök összevonva, tab nélkül); `sikertelen` illesztésnél üres (explicit hiány). **Nyers:** a `thayer_forras_javitas.tsv` (2.38) beszúrásai nem kerülnek bele; a javított szöveg nézet (`thayer_bemenet.szakaszok`) |
| `illesztes` | a Strong illesztési kategóriája: `egyezik` (a bekezdések szóközök nélküli szövege sorban, hézag és maradék nélkül kiadja a TSV szövegét) \| `javitassal` (így van, de csak a 2.38 `javitva` sorainak beszúrásával: a határok pontosak, a `szoveg` nyers; DT333 (2)) \| `reszleges` (nem így: a határok a difflib egyező blokkjain át vetülnek a TSV-szövegre; a szöveg közelítő) \| `sikertelen` (a TSV-ben nincs ilyen Strong) |
| `forras` | `Thayer.lexicon:<Topic>#<sorszam>` (a szerkezet helye) |
| `forras_hash` | a bekezdés nyers HTML-jének SHA-256-ja, 16 jegy (az elavulás jele) |
| `proveniencia` | `scope=<Strong> \| forras=thayer_jelolt/bont.py (fejléc) \| ts=<nap>`; a bemenetek és a kód hash-e a `# forras:` fejlécsorban (a 2.29 mintája) |

Kulcs: `strong` + `sorszam`. Állapot (F132.11, 2026-10-25): 5 426 Strong, 17 093 sor; illesztés: `egyezik` 5 411, `javitassal` 15,
`reszleges` 0, `sikertelen` 0; fejes szócikk 1 687. A 15 `javitassal` Strong mindegyikében a `Thayer_teljes.tsv` egy összefüggő
szövegrészt elveszít (összesen 2 715 karakter szóközök nélkül, a G4151-ben 18), jellemzően egy `πρωι` / `νοι` / `Νινευι` alak után (a
TSV-konverzió hibája); a javítótábla nélkül ezek `reszleges`-ek (F132 M1). A kezelés: DT333 (2), 2.38. A `# forras:` fejlécsor a
javítótábla hash-ét is hordozza (a bontó csak a határokhoz olvassa).


### 2.35 `thayer_vers_jelentes.tsv` — a Thayer igehely-hivatkozásai jelentésponthoz kötve (F132, FELADATOK #132, DT328 (2))

**Generált** (`python eszkozok/thayer_jelolt/vers_jelentes.py --ts <nap>`; kézzel nem szerkeszthető; azonos bemenettel és `--ts`-sel
bájtra azonos, a `--ellenoriz` és az `eszkozok/thayer_jelolt/teszt_vers_jelentes.py` ellenőrzi). A `Thayer.lexicon` minden
`<ref onclick="bcv(k,f,v)">` hivatkozására egy sor, a szócikkön belüli sorrendben. A forrásban az igehely gépi attribútum, tehát —
a BDB-vel (2.29) szemben — nincs szövegből visszafejtés, öröklött könyv és okkód. A forrásban jelöletlen folytatás („Act 9:14,21;
22:16”: csak a 9:14 `bcv`) **nincs** a táblában (explicit hiány). **Lexikai index, nem study-adat** (CLAUDE.md 2. szabály). Az első két
sor `# GENERÁLT: …` és `# forras: …`, a harmadik a fejléc. Olvasás `split('\t')`.

| Oszlop | Jelentés |
|---|---|
| `strong` | `Strong_padded` (a `thayer_jelolt/kulcs.py` szerint) |
| `sorszam` | a hivatkozás sorszáma a szócikkben (1-től; a 2.29 `sorszam`-ja) |
| `szakasz` | a hivatkozást tartalmazó bekezdés `sorszam`-a a `thayer_szakaszok.tsv`-ben (2.34; a `strong` + `szakasz` oda mutat) |
| `konyv` | a `bcv` könyvszáma (1–66) a `Konyv_normalizalo_tabla.tsv` k-adik adatsorának `Magyar rövidítés`-e (`1Móz`, `Mt`, `JSir`) |
| `fejezet`, `vers` | a `bcv` fejezet- és versszáma, változatlanul |
| `karoli_vers` | a Károli-vers a `Karoli_1908.tsv` `Igehely` kulcsa szerint (a Siralmak ott `Sir`); **üres, ha nincs ilyen kulcs** (kitöltés és átkulcsolás nélkül). ÚSZ-helyen a számozás egyezik; az ÓSZ-hivatkozás (LXX-utalás, pl. `Zsolt 103:30`) LXX-számozása csak akkor látszik, ha a vers a Károliban nem létezik — a létező, de eltolt vers nem jelölt |
| `utvonal` | a `szakasz` útvonala (2.34) |
| `proveniencia` | `scope=<Strong> \| forras=thayer_jelolt/vers_jelentes.py (fejléc) \| ts=<nap>`; a bemenetek és a kód hash-e a `# forras:` fejlécsorban |

Kulcs: `strong` + `sorszam`. Állapot (F132 M2, 2026-10-25): 63 953 sor (ÚSZ 58 266, ÓSZ 5 687); `karoli_vers` üres: ÚSZ 28, ÓSZ 12.


### 2.36 `tiltott_fordulatok.tsv` — tiltott magyar fordulatok (F132, DT331; elv: DT241, F121 2a/2)

**Kézi tábla** (kézzel szerkeszthető; új tételt a fordítási javítások hoznak, a felhasználó döntésével). Szótárfüggetlen: a
BDB- és a Thayer-lánc közös kapuja, a `forditas_kapuk.py` **15. kapuja** (`15_tiltott`, gátoló; a `kapuk_futtat` és a
`kapuk_futtat_szakaszos` is futtatja). Olyan magyar szerkezetek, amelyek a fordítás kimenetében hibának számítanak
(tükörfordítás, hamis barát); a tétel **értelemhez kötött minta**, nem puszta szó (DT241: a „melléknév” nyelvtani értelemben
helyes). Találatnál a sor nem rögzül automatikusan, kézi ítéletre áll meg. Az első sor `#` megjegyzés, a második a fejléc.
Olvasás `split('\t')`.

| Oszlop | Jelentés |
|---|---|
| `magyar_alak` | a tiltott fordulat olvasható alakja (`melléknéven nevezni`) |
| `minta` | Python regex, kis/nagybetű-független (`re.IGNORECASE`), a fordítás nyers szövegén; csak az igei / értelemhez kötött szerkezetet fogja |
| `ertelem` | melyik értelemben tiltott (pl. „ige: nevet adni, más néven is nevezni”) |
| `helyette` | a javasolt alak (a terminológiai szójegyzékkel összhangban) |
| `indoklas` | miért hiba |
| `verzio` | a tétel verziója (`v1` …) |
| `proveniencia` | `manual (döntés: …; tétel: …)` — a felvételt elrendelő döntés és forrás |

Kulcs: `magyar_alak` + `verzio`. Állapot (F132, 2026-10-25): 2 tétel (a DT241 / F121 2a/2 első elemei: „melléknéven nevezni”,
„melléknevet adni”); a `forditasok.tsv`-ben a kapu 4 helyen talál, mind a G1941 két sorában (Thayer `teljes`, TBESG `1`; F121 2b/4),
a 98 nyelvtani „melléknév” sor nem találat. A tartalmat a #121 bővíti.


### 2.37 `thayer_sigla.tsv` — a Thayer sigla- és rövidítéstáblája (F132, brief 2a/5)

**Félig kézi tábla.** A számoszlopokat és az új jelölt sorokat az `eszkozok/thayer_jelolt/sigla_gyujt.py --ts <nap>` írja a
`thayer_szakaszok.tsv` javított nézetéből (`thayer_bemenet.szakaszok`, a 2.38 beszúrásaival: a fordítónak átadott szöveg); a **besorolás kézi** (`tipus`, `jelentes`, `magyar_alak`,
`allapot`, `besorolas_proveniencia`), és az eszköz ezeket soha nem írja át (írás előtt összeveti, eltérésnél megáll); sort nem töröl (az eltűnt jelölt
`elofordulas = 0`). A `--ellenoriz` bájtra összevet. A besorolt sorokat a `thayer_jelolt/thayer_kapuk.py` **16. kapuja**
(`16_sigla`, gátoló) ellenőrzi a Thayer-fordításon; a besorolatlan sor nem gátol (JELZES). A tábla a #129 (BDB-kiadás)
rövidítésjegyzékének is mintája.

**A 16. kapu szabályai (F145, DT351/c; pontos leírás: `thayer_kapuk.py` docstringje).** A kapu a besorolt sor minden forrásbeli
előfordulására (a forrás-oldali keresés: önálló szó; az egybetűs sigla láncszabálya, F132.20, változatlan) megköveteli a cél-alakot
(`magyar_alak`; `változatlan` esetén a `forrasalak`) a fordításban, három tűréssel. **(a) Változatlan átvétel (egyedi kivétel, DT355 (b)):** nincs általános átvétel-kivétel semmilyen sigla-típusra (`rövidítés`, `antik szerző`, `modern szerző`, …): a fordítatlan `cf. Winers Grammar`, `Xenophon, Cyril 3, 3`, G0282 `by Philo in de temul.` és G4151 `in Philo's use of` SERTES. Az egyetlen kivétel a `thayer_kapuk.py` `ATVETEL_KIVETEL` állandójának soronkénti eleme (Strong, sigla, a változatlanul átvett ablak = a sigla szava + 3 szó): G0012, `Philo`, `Philo's Lehre von der` (J. G. Müller, *Philo's Lehre von der Weltschöpfung*, műcím; a prompt 5. szabálya: a műcím változatlan). Az az előfordulás mentesül, amelynek ablaka szerepel a kivételek között és szó szerint, szóhatáron kezdődően megvan a fordításban; a kapu hívása a Strongot nem adja át, ezért a (sigla, ablak) egyezés azonosít. Ha minden előfordulás mentesül, a sor nem ellenőrzött, és a kapu részletében „N sigla változatlan átvételben, nem ellenőrzött” áll; a többi előfordulás magyar alakját a kapu megköveteli. Új kivétel csak döntéssel vehető fel. **(b) Ragozás-tűrés:** a
legalább 4 betűs, nem `könyvrövidítés` típusú cél-alak szó elején kezdődik, de toldalékot elfogad (`Homérosztól`, `Platónnál`); a rövidebb
cél-alaknál (`Tr`, `WH`) és a `könyvrövidítés`nél a szóvég-határ marad. **(c) Számjegy-előtag:** a `könyvrövidítés` típusú sor cél-alakja számjegy
mögött is találat (`4Makk`, `2Makk`, a 11. kapu `normalizal.APOKRIF_ALIAS` alakja). Az első két sor `#` megjegyzés (a második: a bemenetek és a kód hash-e), a harmadik a fejléc.

| Oszlop | Jelentés |
|---|---|
| `forrasalak` | a sigla / rövidítés a forrás alakjában (`Rec.`, `WH`, `Winers Grammar`, `cf.`, `Macc.`) |
| `gyujtes` | a gépi gyűjtés szabálya: `minta` (a brief 2a/5 és az M0 7. pontjának megnevezett elemei) \| `kiadas_sigla` (az `R G L T Tr WH` sigla, ha legalább kettő sorban áll) \| `rovidites` (ponttal záruló szóalak, ≥ 10 előfordulás, ≥ 90%-ban ponttal) |
| `tipus` | **kézi:** pl. `kiadás-sigla`, `grammatika`, `antik szerző`, `modern szerző`, `rövidítés`, `könyvrövidítés`, `nem sigla`; üres: besorolatlan |
| `jelentes` | **kézi:** mi ez (pl. „Westcott–Hort kiadás”) |
| `magyar_alak` | **kézi:** a magyar kiadás egységes alakja; `változatlan`: a forrásalak marad; `nincs_egyseges`: nincs egységes magyar alak (több szerep, a szövegkörnyezet dönt; a 16. kapu nem ellenőrzi, az adatblokk így jelzi). `javaslat` és `besorolt` sorban **nem üres** (ELLENOR_F132 4. tétel, F132.21; teszt: `teszt_lanc.py` `test_tabla_sema`); `jelolt` sorban üres |
| `elofordulas`, `szocikk` | gépi: előfordulás és érintett szócikk a teljes Thayerben |
| `gerinc_elofordulas` | gépi: előfordulás a motívumok aktuális görög gerincszavaiban (`szolista.gerinc_strongok`) |
| `pelda` | gépi: az első előfordulás `<strong>:<sorszam>` (a 2.34 kulcsa) |
| `allapot` | `jelolt` (gépi, besorolatlan) \| `javaslat` (DT335 (3): modell-javaslat a `tipus`, `jelentes`, `magyar_alak` mezőben, **jóváhagyásra vár**; a kapu és az adatblokk besorolatlannak veszi) \| `besorolt` (kézi, a felhasználó jóváhagyásával; csak ilyen sort ellenőriz a 16. kapu; `nincs_egyseges`: a kapu nem ellenőrzi; üres `magyar_alak`: kitöltetlen besorolás, a kapu JELZES-ként jelenti, nem gátol) |
| `besorolas_proveniencia` | **kézi:** a besorolás (javaslat vagy jóváhagyás) proveniencia-sora; modell-javaslatnál `scope=adat/thayer_sigla.tsv (tipus, jelentes, magyar_alak) \| forras=manual — modell-javaslat (<tényleges modellnév>), nem lekérdezés: … \| ts=<nap>` (CLAUDE.md 1. szabály: nem lekérdezés, tehát `manual`); üres: besorolatlan |
| `proveniencia` | `scope=adat/thayer_szakaszok.tsv \| forras=thayer_jelolt/sigla_gyujt.py (fejléc) \| ts=<nap>`: a gépi oszlopoké (az eszköz minden futáskor írja) |

Kulcs: `forrasalak`. Állapot (F132.11, 2026-10-25; a javított nézeten): 255 jelölt (`minta` 31, `kiadas_sigla` 6, `rovidites` 218),
ebből 91 fordul elő a gerincszavakban; besorolt: 0 (az F132.9-es, nyers szövegen mért állapot: 254 / 90). F132.13 (DT335 (3)):
a 91 gerinc-jelölt mindegyike `javaslat` (`claude-opus-5-5`; magyar alak 22, `változatlan` 62, `nincs_egyseges` 7 — az F132.21 előtt üres —; a
terminológiai kulcsú sorok alakja a szójegyzéké); a jóváhagyás (`besorolt`) a felhasználóé, az M3 előfeltétele. A lista:
`naplok/F132_THAYER_SZAKASZ_naplo.md` F132.13. A terminológiai szójegyzék (2.15) 10 jelöltre már ad magyar alakot (`cf.` → `vö.`, `Sept.` →
`Septuaginta`, `i. e.` → `azaz`, `Plato` → `Platón` …), az elsőbbséget kap (az adatblokk jelzi). F132.19 (DT337 (a), a
KIRALY-001 G0813 → G0540): a gerincszavakban előforduló jelölt 90 (az `educ.` gerinc-előfordulása 0, `javaslat` marad).


### 2.38 `thayer_forras_javitas.tsv` — a `Thayer_teljes.tsv` szövegvesztésének javítótáblája (F132, DT333 (2); a 2.31 mintája)

**Generált** (`python eszkozok/thayer_jelolt/forras_javit.py --ts <nap>`; kézzel nem szerkeszthető; `--ellenoriz`; teszt:
`eszkozok/thayer_jelolt/teszt_bont.py`, `Javitas`). A DT327 (b) szerint a Thayer-szakasz szövege a `Thayer_teljes.tsv`-ből jön; ahol a
TSV a `Thayer.lexicon`-hoz képest egy összefüggő szövegrészt elveszít (a TSV-konverzió hibája), a hiányzó szöveg ebben a táblában áll,
**a nyers fájlok és a szakasztábla (2.34) `szoveg` mezőjének érintése nélkül**. A bontó a táblát csak a szakaszhatárokhoz olvassa (az
illesztés `javitassal`); a javított szöveg **nézet**: `eszkozok/thayer_jelolt/thayer_bemenet.szakaszok` (a fordítás bemenete, a
`forras_hash` alapja, a sigla-gyűjtés szövege). A hiányzó szöveg forrása a lexikon bekezdésének címkék nélküli szövege (`bont.sima`):
sima szöveg, szerkezeti jelölés nélkül. Első két sor `# GENERÁLT` / `# forras` (a két bemenet és a kód hash-e), a harmadik a fejléc.
Olvasás `split('\t')`. Egy sor = egy lyuk.

| Oszlop | Jelentés |
|---|---|
| `strong`, `sorszam` | a 2.34 sora (kulcs), amelybe a beszúrás esik; `jelolt_marad` sorban a `sorszam` üres |
| `hiba` | `tsv_szovegvesztes` (az egyetlen osztály) |
| `tsv_poz` | a beszúrás helye a `Thayer_teljes.tsv` `Teljes_szocikk` mezőjében (karakterindex: a lyuk előtti utolsó nem-szóköz karakter után) |
| `sor_poz` | a beszúrás helye a 2.34 sorának `szoveg` mezőjében (karakterindex) — a nézet ezt használja |
| `elotte`, `utana` | a sor `szoveg`-ének legfeljebb 20 karaktere a beszúrás előtt és után (igazolás: a nézet eltérésnél ValueError-ral megáll) |
| `javitott_alak` | a beszúrt szöveg: a lexikonbekezdés sima szövege a lyuk előtti utolsó nem-szóköz karakter utántól a lyuk utolsó karakteréig |
| `hossz` | a beszúrt szöveg hossza szóközök nélkül |
| `allapot` | `javitva` (mindhárom gépi feltétel teljesül: a lexikon és a TSV eltérése egyetlen törlés egyetlen bekezdés belsejében; a beszúrással a Strong illesztése `egyezik`; a javított sor szóközök nélkül = a lexikonbekezdés szövege) \| `jelolt_marad` (nem teljesül: nincs javítás, a bontó `reszleges`-t ír) |
| `indok` | a döntés oka, magyarul |
| `proveniencia` | `scope=<Strong> \| forras=thayer_jelolt/forras_javit.py (fejléc) \| ts=<nap>` |

Kulcs: `strong` + `sorszam`. Állapot (F132.11, 2026-10-25): 15 sor, mind `javitva` (G0260, G0575, G0846, G1100, G1909, G2675, G3536,
G3563, G4151, G4404, G4405, G4406, G4407, G5132, G5567), 2 715 karakter szóközök nélkül; `jelolt_marad` 0. A `Thayer_teljes.tsv`
változatlan.

---

### 2.34 `adat/karoli_modern/` — a modernizált Károli-szövegréteg (F96, FELADATOK #96, DT128, DT305, DT314)

A Károli 1908 modernizált rétege: helyesírás és igealak, a szókincs, a szórend, az írásjel és a betoldás-jelölés változatlan (DT128). **Generált, kézzel nem szerkeszthető**; a javítás a szabályban (`eszkozok/karoli_modern/helyesiras.py`, `igealak.py`, `igeragozas.py`) vagy a kivételtáblában (`KEZI`, `GYANU_KEZI`, `KIVETEL_LEMMA`) történik. Az 1908-as szöveg mellett áll, nem helyette. Olvasás `split('\t')`, írás `'\t'.join()` (a `csv` modul tilos). Az első sor `# GENERÁLT: …` (a bemenetek teljes sha256-ja, a mérés hivatkozása), az első nem-`#` sor a fejléc. A tokenizálás az `eszkozok/karoli_strong/tokenek.py` `tokenizal` függvénye: a `sorszam` ugyanaz, amelyen a #22 párosítás (`adat/karoli_strong/szavak_*.tsv`, 2.20) `sorszam`-a áll. **A réteg Strongot nem tárol és nem ellenőriz** (DT305); a Strong token-kulcson (`igehely` + `sorszam`) illeszthető, és a modernizálástól nem változik (DT314, K3b: a generátor igazolja, hogy a #22 minden Strongos magyar tokenjének kulcsa itt áll, azonos 1908-as alakkal). Mérés: `naplok/KAROLI_MODERN_meres.md` 4. (.1) és 5. (.2).

**Kiadott táblák (F96.3, `eszkozok/karoli_modern/karoli_modern.py`):**

`karoli_modern.tsv` — token-soronként a teljes Károli 1908 (599 367 token). Kulcs: `igehely` + `sorszam`.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `igehely` | `IGEHELY` | ✔ | a `konkordancia/Karoli_1908.tsv` vers-kulcsa |
| `sorszam` | egész | ✔ | a token sorszáma a versben (`tokenizal`, 1-től); a #22 `sorszam`-a |
| `alak_1908` | szöveg | ✔ | az 1908-as token, ahogy a szövegben áll |
| `alak_modern` | szöveg | | a modern alak; **üres, ha a token kiesik** |
| `kieso` | zárt | | `osszevonva` (a különírt vonatkozó névmás „a”-ja: *a kik → akik*) \| `segedige` (a segédigei *vala*: *lebeg vala → lebegett*) \| üres |
| `kieso_gazda` | egész | | a kieső tokennél a gazdaszó `sorszam`-a (az összevont „a”-é a következő, a segédigei *vala*-é az előző token); a kereső ide köti a kieső token Strongját (DT314, #137) |
| `szabaly` | szöveg | | a cserét adó szabály(ok) `+`-szal (`karakter`, `neki`, `szoto_94`, `rea`, `jok`, `nevmas:…`, `ami:…`, `igealak:<jegy>`, `gyanu_kezi`, `kotohang_mult`, `mult_E1_targyas`, `ok_birtokos`, `kivetel`, `token_kivetel`, `igealak_kezi`, `gyanu_kezi`, `tobbseg:<források>`, `kor3:szabaly+opus`, `kor3:opus` (a 3. kör, DT316), `kor4:szabaly+opus`, `kor4:opus` (a 4. kör, DT317), `kor3:opus_tanusitott`, `kor4:opus_tanusitott`, `tobbseg:opus_tanusitott`, `tobbseg:alanyi_targyas` (a jelölt-kör, DT318), `kor5:token_opus+meglevo` (az 5. kör, DT320), `vala_letige`, `vala_segedige_…` (a `vala_segedige_kor3`, `_kor4` is), `vala_letige_kor4`, `jelen_mult_vala`, `lon`, `vagyon` …); a változatlan tokennél üres vagy a nem cserélő döntés (`mi_birtokos_marad`, `vagyon_fonev_marad`) |
| `bizonytalan` | szöveg | | a heurisztikus döntés jele (`targyas_heur`, `ek_E1_T3`, `mult_korpuszban_nincs`, `nevelo_utan` (a névelő után álló jelölt főnévnek véve, nem cserél: *a* + mássalhangzós, *az* + magánhangzós szó, *egy*; a mássalhangzós szó előtti *az* névmás, ott nincs kizárás; napló 15.2), `vala_segedige`, `kor3_csak_opus`, `kor4_csak_opus` (a szabály-jelölt nélküli, csak az opus döntötte csere, DT316/r), `szabaly_nem_tanusitott` (a korpuszban nem álló szabály-jelölt helyett a tanúsított opus-alak, DT318), `token_opus` (a tokenszintű opus-válasz egy meglévő jelölttel egyezve, DT320), `mi_birtokos_vagy_vonatkozo` …): a csere megtörtént vagy szándékosan elmaradt, de felhasználói ellenőrzés nélküli |

`karoli_modern_versek.tsv` — versenként a modern szöveg (31 158 vers): `igehely`, `szoveg_modern` (a nem kieső tokenek modern alakja az 1908-as írásjel-vázban; a kieső token és az egy szóköze elmarad), `valtozott` (`igen` \| `nem`). A K2: a `szoveg_modern` újratokenizálva pontosan a vers nem kieső `alak_modern`-jeit adja, sorrendben.

**Mérő- és melléktáblák (generált, nem a kiadott réteg):** `fedettseg_alakok.tsv` (F96.0, alakosztályok), `token_minta.tsv` + `token_minta_hivasok.jsonl` (F96.0/3, API-mérés), `helyesiras_alakok.tsv`, `helyesiras_tokenek.tsv`, `helyesiras_hunspell.tsv` (DT301: csak mérce), `helyesiras_ami_proba.tsv`, `helyesiras_ami_ellenorzes.tsv`, `helyesiras_minta.tsv` (.1), `igealak_alakok.tsv`, `igealak_tokenek.tsv`, `igealak_llm.tsv` + `igealak_llm_hivasok.jsonl` (sonnet), `igealak_llm_opus.tsv` + `igealak_llm_opus_hivasok.jsonl` (opus), `igealak_minta.tsv` (.2), `regies_szken.tsv` (`eszkozok/karoli_modern/regies_szken.py`, a 3. ellenőri kör előtti réteg pillanatképe: a modern szövegben változatlanul maradt régies-igealak-jelöltek; `id`, `tipus` = `alak` \| `vala`, `kerdes`, `gyakorisag`, `szabaly_jelolt` — szövegkörnyezetfüggőnél `E1=…\|T3=…` vagy `alanyi=…\|targyas=…` —, `elso_igehely`, `versreszlet`), `igealak_llm_kor3.tsv` + `igealak_llm_kor3_hivasok.jsonl` (opus, DT316: `id`, `tipus`, `kerdes`, `szabaly_jelolt`, `opus_alak`; a *vala*-páron `-` = létige), `regies_szken_kor4.tsv` + `igealak_llm_kor4.tsv` + `igealak_llm_kor4_hivasok.jsonl` (a 4. kör, DT317: mint a 3. köré, `S%04d`; a `tipus` `jelolt` is: a DT311 opus-szavazata), `regies_szken_kor5.tsv` + `igealak_llm_kor5.tsv` + `igealak_llm_kor5_hivasok.jsonl` (az 5. kör, DT320: tokenenként, `T%04d`; `igehely`, `sorszam`, `alak`, `meglevo_jeloltek`, a kérdéstáblában `vers` — a modern vers, a token [zárójelben] —, a választáblában `opus_alak`), `igealak_minta2.tsv` (N-F96g: a lefedettséget is mérő minta, `H%03d`; `ellenorzes` = `jó` \| `hibás` \| `kihagyás`, a `megjegyzes` `csere=<n> hiba=<n> kihagyas=<n>`-nel kezdődik). Az LLM-táblák modell-kimenetek (`modell_ellenorizetlen`); a minták `ellenorzes`/`megjegyzes` oszlopa a felhasználói (vagy a felhasználó által elfogadott modell-) ellenőrzés, újragenerálásnál megmarad. **Proveniencia (napló 15.4):** az `igealak.py` és a `regies_szken.py` minden táblájának `# GENERÁLT:` fejléce `forras=… | scope=… | ts=…` hármast hordoz; a szken-tábla fejléce a saját körét és döntését nevezi meg (3. kör: N-F96d/e, DT316; 4. kör: DT317; 5. kör: DT320). A szken-táblák pillanatképek: az újrageneráláshoz a bemenetet a pillanatkép commitjából kell visszaállítani (3. kör `8b858b3`, 4. kör `9fd137f`, 5. kör `0dda8b3`). A meglévő válaszfájlokból újraírt LLM-tábla fejlécében a `futas_ts` az LLM-futás eredeti ideje, a `ts` az újraírásé.

### 2.39 `glosszak_heber_hu.tsv` — a TBESH-glosszák magyar fordítása (F140, FELADATOK #140, DT-F140a, DT346)

Kulcs: `entry_id`. Minden héber Strong (8 718; a H9015–H9019 előtag-elemek nincsenek benne) minden
TBESH-sora egy sor (11 677 sor, DT346 K1 (B)). A szó-lap kiemelt jelentés-sorának forrása (a
forrás-sorrendet és a megjelenítést a #139 adja). A `forditasok.tsv`-től (2.14) külön tábla, mert azt a
#38 folyamatosan írja. Írja: `eszkozok/glossza_forditas.py` (`--fix`, `--rogzit`); a session fordít
kötegenként (K7 (a)), a szkript nem hív modellt. Ellenőrzi: `glossza_forditas.py --ellenoriz`. A sorok
entry_id szerint rendezve állnak; a szkript írás előtt összeveti a meglévő sorokat (változás esetén megáll).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `strong` | `STRONG` | ✔ | A TBESH `eStrong#` oszlopa (az első öt karakter). TBESH-sajátosság: a H7178 alatt áll a `H7156H` entry_id (Kartan). |
| `entry_id` | szabad szöveg | ✔ | A TBESH `dStrong` oszlopának első szava (`H0430G`, `H2763A`); a tábla kulcsa, globálisan egyedi. |
| `kapcsolat` | szabad szöveg | | A TBESH kapcsolata (`a Name of`, `a Meaning of`, `in Aramaic of`, …); üres, ha nincs. |
| `fo` | zárt | | `igen`, ha a sor a Strong kiemelt jelöltje; Strongonként pontosan egy. Szabály (K2): az a sor, amelynek glosszája (a kettőspont előtti rész, kisbetűsítve, `_` helyett szóköz) egyezik a `TAHOT_kivonat.tsv` „Rövid jelentés” oszlopának Strongonkénti többségi értékével; a 11 istenneves Strongnál a K5-lista (`K5_FO`) dönt; ahol a TAHOT nem illeszthető, a 2.2 heurisztika (`fo_heurisztika`). A TAHOT-oszlop csak a kiválasztásban számít, szöveg nem kerül át belőle. |
| `glossza_en` | szabad szöveg | ✔ | A TBESH 7. oszlopa (`Gloss`) szó szerint. |
| `forras_hash` | szabad szöveg | ✔ | A `glossza_en` SHA-1 hexdigestje, UTF-8 kódolásból; eltérés az újraszámolttól sértés (`--ellenoriz`). |
| `glossza_hu` | szabad szöveg | ✔ | A magyar jelentés: legfeljebb 50 karakter és 6 szó; szófaj nélkül; ige főnévi igenévvel (K4), főnév alanyesetben; a „szó: árnyalat” kettőspontja megmarad (K3, kapu); nincs héber/görög betű, idézőjel, kérdőjel és angol szó (forrás-alapú közelítés + kivétel-lista, K9). Istennevek: a K5-lista (`ISTENNEV_FIX`), az „az ÚR” projekt-konvenció, nem Károli-alak. **Kivétel (ELLENOR_F140_4 3. tétel):** ha a TBESH szerint az ige csak melléknévi/igenévi alakban fordul elő (pl. H7465 „összetört, romlott”, Péld 25:19; H7806 „sodrott, sodorva készült”, 2Móz 26:1), vagy a szó Hithpael/Hophal/Pual alakú, a magyar jelentés ezt az alakot követheti, ha a Károli-hely igazolja. |
| `allapot` | zárt | ✔ | `sonnet` (a modell fordította, kapukon átment, emberi jóváhagyás nélkül) \| `kezi` (a sort a naplózott `--javit` mód írta át: a felhasználó átnézési javítása, vagy a felhasználó által jóváhagyott átnéző-javaslat [DT347]; a `modell` mező ilyenkor is a fordítót rögzíti; a szöveg nem mindig változik, l. `?`). |
| `modell` | szabad szöveg | ✔ | A ténylegesen futó modell neve (a session saját környezetéből; briefből másolni tilos). |
| `datum` | `DATUM` | ✔ | A fordítás napja. |
| `megjegyzes` | zárt | | Üres vagy `?`: a fordító (vagy az átnéző) bizonytalan: magyaros átírás (K6), vagy a TBESH-glossza és a definíció eltér (pl. H6808); a `--javit` `=?` értéke a szöveget nem változtatja, a `?`-t beállítja (`kezi`; napló: `? beallitva`, korábbi `?` visszaállításakor `? visszaallitva`). A több értelmet a vessző (szinonimák) vagy a pontosvessző (különböző értelmek) választja el, a két alak együtt él (DT348). Az M2 zárójelentése külön felsorolja. |

**Gyorsítótár (K7):** azonos (`glossza_en`, szófaj) párra egyszer fordul a modell; az eredmény a pár minden sorába kerül. **Elakadók:** a kapun kétszer elbukó sor nem kerül a táblába, hanem a `naplok/GLOSSZA_FORDITAS_elakad.tsv`-be. **Licenc:** a TBESH CC BY 4.0, a fordítás származtatott mű, a `fo` kiválasztása a TAHOT-ot is használja; az `sqlite_epit.py` `ADAT_LICENC`-bejegyzése (`glosszak_heber_hu: ['TBESH', 'TAHOT', 'projekt_adat']`) bekerült (DT346 K8, F140.138), így a tábla a TBESH (CC BY 4.0) forrásjelölésével töltődik a `pardes.db`-be.


### 2.40 `szotar_szakasz_cimke.tsv` — szótári szakaszcímkék és a kutatói jelentésszám leképezése (F131, FELADATOK #131, DT-F131b–d)

**Kézi** (`manual` proveniencia; író: `naplok/F131_cimke_ir.py`, amely írás előtt összeveti a meglévő sorokat, és
eltérésnél megáll). A motívumlap szótári gerincének (DT272, F131) adatai: (1) a szótári szakasz rövid magyar
**címkéje**, amelyet a lexikonoldal előfordulás-táblájának „Jelentés (a szó)” oszlopa és a gerinc vázlata mutat;
(2) a kutatói `jelentes_szam` (`elofordulasok.tsv`, 2.2) **leképezése** a szótár saját tagolására (DT-F131b 2.: a
leképezés itt áll, a `lexikon_hivatkozasok.tsv` sémája nem változik; ha a DT190 (a) nyer, a sor átvihető oda);
(3) a Thayer magyar `teljes` sorának **kézi szakaszhatárai**, átmenetként a szakaszonkénti Thayer-fordításig
(#142; DT-F131c 2.). **A tábla saját tagolást nem tart:** minden sor létező szakaszra mutat. A címke a szóról
szól: motívumra, invokációra vagy tagadásra utaló minősítés nem állhat benne (DT272 (d)). Csak az arany lap
(ISTENTISZT-001) Strongjai. Olvasás `split('\t')`.

| Oszlop | Jelentés |
|---|---|
| `szotar` | `BDB` \| `Thayer` \| `TBESG` |
| `strong` | a Strong-szám a forrástábla alakjában (`H7121`, `G1941`) |
| `szakasz` | `BDB`: a `bdb_szakaszok.tsv` (2.30) `utvonal`-a (`Qal/2/c`, `-/3/-`); `Thayer`: a `thayer_szakaszok.tsv` (2.34) `utvonal`-a (`cim`, `fej`, `-/5/-`); `TBESG`: a `lexikon_hivatkozasok.tsv` `jelentes_szam`-a (`2`) |
| `lexikon_jelentes_szam` | üres, vagy a kutatói `jelentes_szam` (minősítő nélkül, `2.c`), amely erre a szakaszra képeződik; a `lexikon_hivatkozasok.tsv` (`szotar`, `strong`, `jelentes_szam`) kulcsa. Egy kulcs legfeljebb egy szakaszra |
| `cimke_hu` | üres, vagy a szakasz rövid magyar címkéje (a magyar szakasz vezérszavaiból, a végrehajtó javaslata; jóváhagyás: DT-F131f) |
| `hu_kezdet`, `hu_hossz` | csak `Thayer`: a szakasz kezdete és hossza (karakter) a `forditasok.tsv` `Thayer <strong> teljes forditas_hu` sorában; a szakaszok sorrendben, csak szóközzel elválasztva fedik a szöveget |
| `forditas_hash` | csak `Thayer`: a határok alapjául szolgáló `forditas_hu` SHA-1-e; eltérés a mai sorétól: a határok elavultak |
| `proveniencia` | `scope=… \| forras=… \| ts=…` |
| `megjegyzes` | szabad szöveg |

Kulcs: `szotar` + `strong` + `szakasz`. **Ellenőrzés** (`ellenoriz.py` 17. szabály, SÉRTÉS): a kulcs egyedi; minden
`BDB`-szakasz létezik a 2.30-ban (a záró `/-` levágásával összevetve, mert a 2.29 `-/3`, a 2.30 `-/3/-` alakot
ír), minden `Thayer`-szakasz a 2.34-ben, minden `TBESG`-szakasz a `lexikon_hivatkozasok.tsv`-ben; minden nem üres
`lexikon_jelentes_szam` létező `lexikon_hivatkozasok.tsv`-kulcs, és egy kulcs legfeljebb egy szakaszra mutat; egy
Strong `Thayer`-sorai együtt a Strong minden 2.34-szakaszát fedik, a szeletek sorban, csak szóközzel elválasztva
bájtra kiadják a mai magyar sort, és a `forditas_hash` egyezik (különben: elavult); a `cimke_hu` nem tartalmaz
tiltott minősítést (`motívum`, `invokál`, `invokáci`, önálló `nem`). Állapot (F131.1, 2026-10-26): 13 sor (BDB 5,
TBESG 1, Thayer 7 — G1941, kézi határral; címkés 8).


---

## 3. Integritási szabályok

Ezeket az `ellenoriz.py` (F4/commit-hook) kényszeríti ki. Amíg az nem készül el, kézi
ellenőrzés tárgyai.

1. **Hivatkozási épség.** `elofordulasok.id`, `kapcsolatok.id`, `jeloltek.id`, `auditok.id`
   → létező `motivumok.id`.
2. **Nincs közvetlen út.** Minden `elofordulasok` sorhoz tartozik `jeloltek` sor azonos
   kulccsal, `dontes=beépítve` értékkel.
3. **Proveniencia-kényszer.** `elofordulasok.proveniencia` nem lehet üres. Kötelező kulcsai
   `scope`, `forras`, `ts`; a `lekerdez.py` által írt további kulcsok (`strong`, `n`)
   megengedettek; az igazolás-jellegű kulcsok (`talalat`, `strong_vart`, l. 1.8) tiltottak
   (`F8_BRIEF.md` G9). Ha `manual`, a sor értelmezésként jelölendő a generált kimenetben.
   Ugyanez a szabály vonatkozik az `auditok.proveniencia` mezőre (N12).
4. **Horgony-kényszer.** `elofordulasok.gerinc_elem` nem lehet üres.
5. **Károli-triplet.** Ha `karoli_szo` ki van töltve, `azonositas_modja` és
   `megbizhatosag` is kötelező.
6. **Gate-kényszer** (4.6): `azonossag_tipusa`, `negativ_kriterium`, `folerendelt_fogalom`
   egyike sem lehet üres egy `publikálható` vagy `véglegesített` motívumnál.
7. **Ütközés- és részhalmaz-jelentés** (`gate.py`): mely motívumpárok osztoznak igehelyen;
   ha `B` igehely-halmaza ⊆ `A`, akkor **B nem önálló ID, hanem ↳ alpont**.
8. **Dataset-lefedettség** (motívumszintű, N12). Egy motívum nyomai: az `auditok` sorai és
   az `elofordulasok` proveniencia-mezői; a nyomot a `forras` `+` mentén bontott fájlnevei
   adják, pontos egyezéssel. Minden `mindig` datasethez tartozzon nyom. Kivételek, KÉZI
   jelentéssel: (a) a lekérdező nélküli datasetek (`ellenoriz.LEKERDEZO_NELKULI`, ma: BDB);
   (b) a 8 retroaktív, F3/N14-betöltésű motívum hiányzó datasetjei (`ellenoriz.RETROAKTIV_IDK`,
   zárt lista). A `felteteles` datasetek a 8/b alatt KÉZI.
9. **Egyirányúság** (DT28, 2026.10.05). Három réteg, minden fájl pontosan egyben:
   (a) kanonikus adat (`adat/*.tsv`); (b) kézi próza-forrás markerekkel
   (`motivumok/[ID].md`, a tanulmányok), amelyből a generátor kinyer; (c) generált kimenet
   (`lexikon/`), kézzel nem írható. A mozgás csak (b)→(a) kinyerés (a `jeloltek.tsv`-n át,
   `manual` provenienciával, döntéssel: 2. szabály) és (a)→(c) generálás. (a)→(b) visszaírás
   tilos. A régi, adatot prózában hordozó tanulmány migrációja szétválasztás: az adatrész
   (a)-ba, az értelmező rész (b)-be, a maradék (c) vagy archívum. Kézi ellenőrzés tárgya,
   amíg a #37 auditja és a #23 forrássablonja el nem készül.

### 3.10 Szintjelölés és kinyerés a kézi forrásból (#23 M1, D36, DT28)

*F23 M1/2, 2026.10.08. Tervezet: a forrássablonnal (`sablonok/9_PaRDeS_motivum_forras_sablon.md`)
együtt a #12 pilotja véglegesíti. A v0 `javaslat` jelölésű pontjairól a `DONTESEK.md`
DT84 tétele döntött (🟢, felhasználó, 2026-10-12; átvezetve 2026.10.17). A D35 szabálya (generált fájlba kézzel nem írunk) a 3/9-ben áll; ez
az alfejezet nem ismétli, hanem a (b)→(a) kinyeréssel egészíti ki.*

Ez az alfejezet a (b) réteg (`motivumok/[ID].md`) két gépi tulajdonságát írja le: a
**mélységi szintet**, amely szerint a nézetek válogatnak, és a **kinyerést**, amellyel a
forrás jelölőiből adat lesz. A dokumentum szerkezetét nem írja le: az a forrássablon
dolga, és ott is szakaszsorrend és jelölő, nem mezőhatár (F32 KONTEXTUS K1/2).

#### 3.10.1 Három szint

Zárt értékkészlet: `olvasoi` | `apparatus` | `belso` (D36).

| Szint | Mi tartozik ide | Melyik nézet mutatja |
|---|---|---|
| `olvasoi` | az összefüggő érvelés olvasónak szóló része (Kivonat, PaRDeS-rétegek, Alkalmazás) | mind |
| `apparatus` | tudományos apparátus: táblák, szótári háttér, minősítés, alátámasztás, nyitott kérdések | `apparatus` és `belso` mélységű nézet (a motívumcikk és a lexikonoldal ilyen) |
| `belso` | folyamat-nyom: `【NAPLO】`, P1–P7 levezetés, módszertani réteg-tábla, kapu-eredmény, proveniencia-sorok, archív blokk | csak a `belso` (szerkesztői) nézet |

A nézet mélysége kumulatív: az `apparatus` nézet az `olvasoi` blokkokat is mutatja, a
`belso` mindent. Kiadható nézet csak `olvasoi` vagy `apparatus` mélységű lehet; a
motívumcikk és a lexikonoldal **kiadható `apparatus` nézet (a DT-F86a szerint prémium)**,
a `belso` réteg belőlük is kimarad (DT84 (10)). A licenc szerinti szűrés nyitott: a #86
DT-F86c pontja (BY-SA-eredetű blokk zárt rétegben ne álljon) ma *javaslat*, nem döntés;
ez az alfejezet nem épít rá. A közös build-idejű szűrő: N-F23b.

#### 3.10.2 A jelölés blokkszintű, gépileg olvasható

- **Alapszint:** minden szakasz alapszintje a forrássablon 4. pontjának táblázatában áll;
  a forrásban ehhez jelölő nem kell. Ismeretlen (a táblázatban nem szereplő) szakasz
  szintje `belso` (zárt alapérték, l. 3.10.4).
- **Szakasz-felismerés** (DT202 (a), 2026-10-18): a szakasz a `##` címsor, és a címsor
  eleje azonosítja (`Kivonat`, `0.`–`7.`, `Proveniencia-sorok`); a `###` alcím a szakasz
  szintjét örökli, kivéve az 1. szakasz „P1–P7” alcímét (1.P, `belso`); az első `##`
  előtti rész `belso`. A részletes szabály és a P-lépés-figyelmeztetés: forrássablon 4. pont.
- **Eltérés:** jelölőpár, a meglévő `RÉS-KEZDET` / `GENERÁLT-KEZDET` mintájára, saját sorban:

  ```
  <!-- SZINT-KEZDET: belso -->
  …
  <!-- SZINT-VÉGE: belso -->
  ```

  Gépi alak: `^<!-- SZINT-(KEZDET|VÉGE): (olvasoi|apparatus|belso) -->$`.
- **Szabályok:** a pár kezdő és záró értéke azonos; a pár nem nyúlhat át `##` címsoron;
  egymásba ágyazni csak mélyebb szint felé lehet (`olvasoi` szakaszon belül `apparatus`
  vagy `belso`, `apparatus`-on belül `belso`); sekélyebb szintre váltani nem lehet
  (egy `belso` szakaszból nem emelhető ki `olvasoi` blokk). Párosítatlan vagy ellentmondó
  jelölő generátor-hiba, nem csendes kihagyás.
- Az `ADAT-NÉZET` jelölő a saját `SZINT:` mezőjében adja a generált blokk szintjét
  (a #64 mintája, `motivumok/TEREMT-002.md`).

A jelölőpár alakja és a hatókör-szabály eldöntve (DT84 (1)): a hatókör így gépileg
ellenőrizhető. A #64 ideiglenes alakja (`<!-- SZINT: x -->` a következő jelölőig) írás
közben kezelhető volt, de a hatóköre nem volt kimondva
(`naplok/TEREMT002_PROZA_PROBA_meres.md` 3. szakasz, 2. tanulság); nem használható.

#### 3.10.3 A `【NAPLO】` mindig `belso`

A `【NAPLO: …】` blokk szintje mindig `belso`, attól függetlenül, milyen szintű szakaszban
vagy jelölőpárban áll; külön jelölő nem kell hozzá (DT66 (a) 1. kivétel: kézi, de nem az
érvelés része). Kinyerés belőle nincs (az `adat` alternatíva elvetve, DT66 (a) 1.).

Mivel mindig `belso`, a `【NAPLO】` csak folyamat-nyomot hordozhat (dátum, ki/mikor, forrás
elérhetősége). Az állítás megbízhatóságát érintő módszertani figyelmeztetés nem
`【NAPLO】`, hanem apparátus-szöveg (Minősítés, Módszertan vagy Nyitott kérdések). Az
örökölt lapok `【NAPLO】`-jait a #11 szétválasztása egyenként ítéli meg, és az
apparátusba emelt figyelmeztetés a leképezési táblában külön, indokolt sort kap
(DT84 (10) (ii); `naplok/MOTIVUM_FORRAS_pilot_terv.md` 8. szakasz).

#### 3.10.4 Engedélyezőlista és build-kihagyás (D36)

- **Engedélyezőlista:** a kiadható nézet csak azt veszi fel, ami a forrássablon
  szakaszlistáján szerepel, aktív (forrássablon 3. pont), és szintje legfeljebb a nézet
  mélysége. Ami nincs a listán (ismeretlen szakasz, ismeretlen jelölő), az kimarad —
  zárt alapérték, nem nyitott.
- **Build-kihagyás, nem elrejtés:** a `belso` blokk a kiadható nézet felépítésekor **nem
  kerül a kimenetbe**. Nem HTML-megjegyzésbe, nem `<details>` alá, nem CSS-sel rejtve: a
  kiadható fájlban a szövege nem létezik. Ugyanígy kimarad minden csak-forrásbeli jelölő
  (`SZINT-*`, `INAKTÍV`, `JELÖLT`, `ADAT-HIV`, `ADAT-ÉRTÉK`, `FORRÁSRÉTEG`).
- Gépi ellenőrzés: CI E29 (`naplok/MOTIVUM_FORRAS_ci_terv.md`).

#### 3.10.5 Kinyerés jelölőnként — (b) → (a)

A 3/9 egyirányúsági szabályára épül: a kinyerés a forrásból **csak jelölt-sort** ír a
`jeloltek.tsv`-be, `manual` provenienciával; a jelölt-sorról ember dönt (3/2), és **a
generátor a forrásba nem ír**. Más táblába a kinyerés közvetlenül nem ír.

| Jelölő (forrássablon 6. pont) | Tábla | Kulcs | Mit ír | Proveniencia | Ütközés (a kulcs már létezik) |
|---|---|---|---|---|---|
| `<!-- JELÖLT: [igehely] \| gerinc: [gerinc_elem] \| [indoklás] -->` | `jeloltek.tsv` (2.4) | `id` + `igehely` | `dontes=nyitva`, `indoklas` = `gerinc: [gerinc_elem] — [a jelölő indoklása]` (DT202 (d): a gerinc séma-bővítés nélkül megmarad az előléptetéshez), `datum` = a kinyerés napja | a `forras_kereses` mezőben: `scope=manual \| forras=motivumok/[ID].md#[szakasz] \| ts=[DATUM]` (1.5); a `[szakasz]` a `##` címsor szövege | nem ír; a kinyerési jelentés jelzi, hogy a jelölt már minősítve van |
| proveniencia-lábjegyzet (bármely `scope`) | — (hivatkozás) | — | semmit: a lábjegyzet a próza állításának forrás-hivatkozása; az audit-sort a 2.9 szerint a lekérdezést futtató fő szál rögzíti, nem a kinyerés | — | — |
| `ADAT-HIV`, `ADAT-ÉRTÉK` | — (ellenőrző) | a jelölőben megadott: `ADAT-HIV` — `mező=érték; …` a tábla teljes kulcsával (a 2. szakasz „Kulcs:” sorai), pontosan egy egyező sor; `ADAT-ÉRTÉK` — zárt készlet: `count([szűrő])`, `count_distinct([mező]; [szűrő])`, a szűrő ugyanilyen `mező=érték; …` alakú, az érték egész szám, karakterre egyezik (DT202 (b), (c); forrássablon 6. pont) | semmit; hiány vagy eltérés a kinyerési jelentésbe, a futás megáll | — | — |
| szerkezeti jelölők (`FORRÁSRÉTEG`, `SZINT-*`, `【NAPLO】`, `INAKTÍV`, `RÉS-*`, `ADAT-NÉZET`) | — | — | semmit | — | — |

- **Előléptetés:** a jelölt-sorból az `elofordulasok.tsv` sora csak döntéssel
  (`dontes=beépítve`) lesz (3/2); a sor `proveniencia` mezője a jelölt `forras_kereses`
  proveniencia-sora (`scope=manual`), az `igazolas` mezője az 1.8 szerint. A `manual`
  sor a generált kimenetben értelmezésként jelölendő (3/3).
- **Audit-út a lábjegyzetből nincs** (DT84 (2)): a `scope≠manual` lábjegyzet csak
  hivatkozás; a lekérdezés nyomát a futtató fő szál már rögzítette (2.9), a lábjegyzet
  ennek másolata, nem új adat. A 3/9 és a 2.9 változatlan.
- **Kinyerési jelentés:** a kinyerés futásának kimenete (generált, (c) réteg): a felvett
  jelölt-sorok, az ütközések, az `ADAT-HIV` hiányai és az `ADAT-ÉRTÉK`
  eltérései. Táblát nem ír felül; eltérésnél a futás megáll (minta:
  `eszkozok/igazolas_migracio.py`, `CLAUDE.md` „TSV-olvasás”).

#### 3.10.6 Ami nincs

- **(a) → (b) út nincs.** A generátor a forrásba nem ír; az adatból semmi nem kerül
  vissza a prózába. Generált jelölő (`GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`, `GENERÁLT:`,
  `ÜRES-BLOKK`, `ÜRES-NYELV`) a forrásban tilos; ha megjelenik, visszaírás-gyanú.
- **Közvetlen út nincs.** Kinyerő jelölő soha nem ír közvetlenül `elofordulasok.tsv`,
  `kapcsolatok.tsv`, `lexikon_hivatkozasok.tsv` vagy `lxx_dontesek.tsv` sort.

#### 3.10.7 Séma-kérdések — eldöntve (DT66 (a) megjegyzése; DT84 (3), (8))

A DT66 (a) a Minősítés, az Alátámasztás és a 7. Módszertan `adat`-besorolását fogadta el,
azzal a megjegyzéssel, hogy új oszlopot kérhet. A DT84 döntése:

1. **Alátámasztás → `kapcsolatok.tsv`, új `indoklas` oszlop** (DT84 (8) a). A mai sémában
   a soronkénti funkció-/bizonyosság-indoklásnak nincs oszlopa (2.3: `funkcio` van,
   indoklás nincs). Az oszlop felvétele (a 2.3 bővítése és a tábla) nem ennek a tervnek
   a része (a #23 adattáblát nem ír); hogy melyik lépés és mikor végzi, arról a
   `DONTESEK.md` DT183 tétele dönt. *Átvezetve (#11 S1, DT183 a):* a 2.3 `indoklas`
   mezője és a tábla fejléce felvéve, a meglévő sorokon üres értékkel.
2. **Minősítés → `jeloltek.tsv`, a „független megerősítés” generált** (DT84 (8) a): az
   „új találat” és a „nem releváns” a `dontes` (`beépítve` / `nyitva` / `elutasítva`) és
   az `indoklas` mezőbe képezhető, a kereszthivatkozás forrás-verse a `forras_kereses`
   mezőbe (`TSK [igehely]`). A már beépített igehelyre szóló megerősítés a
   minősítés-nézetben generálódik (a TSK-találat és a beépített sor metszete);
   séma-bővítés nincs.
3. **Módszertan-tábla és kapu-eredmény → archívum** (DT84 (8) a): a `lepes` értékkészlete
   (`A5` | `B2` | `B3` | `B4`) változatlan; a régi retroaktív rétegtáblák és a Q-kapu
   kézi eredménye a #11-ben archívumba kerül, a nézet a meglévő audit-sorokból
   generálódik. Új `lepes` érték és új tábla nincs.
4. **Nem igehely-kulcsú adat a prózában** (szótári idézet, LXX-megfelelő; DT84 (3) a): a
   `jeloltek.tsv` kulcsa igehely, ezért jelölt-sor nem írható (`naplok/F78_meres.md`
   12. szakasz 2. pont). Az út az `ADAT-HIV` ellenőrző jelölő és a kinyerési jelentés
   (3.10.5); a hiányzó sort döntéssel, `forras=manual` provenienciával a meglévő adatút
   írja. Új jelölt-tábla nincs; a kérdés a #9 adatosítás tapasztalata után nyitható újra.
   *Viszony a 3/9-hez:* ez az út nem kinyerés a 3/9 értelmében, ezért nem kivétel alóla.
   Az `ADAT-HIV` ellenőrző jelölő (3.10.5 táblázat): a generátor belőle semmit nem ír, csak
   a sor hiányát jelenti. A hiányzó sort nem a forrásból kinyert szöveg tölti, hanem a
   meglévő adatút a saját döntésével. A 3/9 „csak a `jeloltek.tsv`-n át” szabálya a
   forrásból kinyert sorra szól; ilyen sor itt nem keletkezik.

---

## 4. Amit ez a séma nem old meg

- **A `TAHOT_kivonat.tsv` lefedettsége és kulcsolása — mért állapot (F85, 2026.10.09).**
  A korábban itt és a `NYITOTT_FELADATOK.md`-ben rögzített hiány-tételek (1Móz 32, Zsolt 88/89/140/142, Jóel 3; később a Jób 40:1–5 és a Jób 41)
  **megszűntek / elavultak**: az F2 tételes felmérése (`eszkozok/tahot_lefedettseg_ellenoriz.py`) a hat fejezetet teljesnek találta; a Jób 40:1–5 nem hiányzott
  (TAHOT-kulcsa 39:34–38), a Jób 41-et az F84 (332 sor) pótolta. Az F85.6 óta az `Igehely` kulcs versszinten a **Károli-vers**, amelynek a héber szövegét a sor hordozza
  (337 vers, 6 330 sor átkulcsolva; a fejezethatár- és fejezeten belüli eltolások megszűntek): minden TAHOT-kulcs létező Károli-vers, és minden ÓSZ-Károli-versnek van
  TAHOT-sora (teljes ÓSZ-os versszintű kulcs-összevetés: `naplok/F85_kulcsosszevetes.md`; továbbá `naplok/F85_jelentes.md`, `naplok/F85_igazolas.md`). Fennmarad: ahol a Károli két TAHOT-verset egy versbe vont (9 hely), mindkét vers a közös
  Károli-kulcson áll (a vershatár az `f22/versosszevonas.tsv`-ben), és a fájlsorrend nem Károli-sorrend. **A `scope` proveniencia-értéke ettől függetlenül `TAHOT-teljes` marad,
  nem `OT-full`** — ez a kivonat egészére vonatkozó, nem a kánon teljességét állító címke, és az `eszkozok/lekerdez.py` minden parancsa ezt írja ki;
  az `OT-full` címke kiadása a DT90 döntése (az F85 mérése ezt érdemben eldönthetővé teszi, de nem dönti el).
- **A `kapcsolatok.tipus` és a pilot-TSV „Típus" oszlopának névütközése** (l. 2.3).
- **Az SDBH lefedettsége** (l. 2.6) — kb. 90%; gyakori szavak is hiányoznak (pl. H1961, H5414, H6440), ezért a `domen` üres eredménye nem negatív lelet.
- **A `keretszo` lista teljessége.** 34 tétel, gyakoriság alapján válogatva. Nem állítjuk,
  hogy teljes; bővítése az F3 betöltés tapasztalatai alapján várható.
