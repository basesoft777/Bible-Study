# `adat/` — séma

**Verzió:** v1 — 2026.09.13
**Forrás:** `ATALAKITASI_TERV.md.md` 1.A pont (tábla-lista), 4.2 (proveniencia), 4.5 (gerinc-elem), 4.6 (gate-mezők), 4.7 (Károli-join)
**Fázis:** F1.2

Ez a réteg a **kanonikus igazságforrás**. A `tematikus_lezart/`, `genezis/`, `motivumlog/`
és `lexikon/` kimenetei ebből generálódnak vagy ehhez igazodnak. Ha egy tény itt és egy
markdown-fájlban ellentmond, **ez a tábla az irányadó**. Az adat egy irányba mozog (3/9,
DT28): a kézi forrásból ide kinyerés van (`jeloltek.tsv`), innen a kimenetbe generálás;
forrásba visszaírás nincs.

A kilenc tábla (és a modell-kimenetű `karoli_strong/` táblapár, 2.20) és a hozzájuk tartozó kulcs:

| Fájl | Kulcs | Ki írja |
|---|---|---|
| `motivumok.tsv` | `id` | `betolt.py` / kézzel, validálva |
| `elofordulasok.tsv` | `id` + `igehely` | `betolt.py`, jelöltből előléptetve |
| `kapcsolatok.tsv` | `forras_igehely` + `cel_igehely` + `id` | `betolt.py` / kézzel |
| `jeloltek.tsv` | `id` + `igehely` | `lekerdez.py` írja, ember minősíti |
| `lexikon_hivatkozasok.tsv` | `strong` + `entry_id` + `jelentes_szam` | `betolt.py` |
| `datasetek.tsv` | `study_tipus` + `dataset` | kézzel (policy-tábla) |
| `grammatikai_strongok.tsv` | `strong` | **generált** — `eszkozok/grammatikai_strongok_general.py` |
| `auditok.tsv` | nincs (l. 2.9) | a `lekerdez.py` proveniencia-sora, kézzel rögzítve |
| `licencek.tsv` | `dataset` | kézzel (leltár, F24) |
| `dontes_hatas.tsv` | `dontes_forras` + `erintett_fajl` + `tilos_minta` | kézzel (F51, 2.21) |
| `karoli_strong/parok_<könyv>.tsv`, `karoli_strong/szavak_<könyv>.tsv` | `vers` + `hu_sorszam` + `er_sorszam` / `vers` + `oldal` + `sorszam` | **generált** (modell-kimenet, javaslat) — `eszkozok/karoli_strong/egyesit.py` (2.20, F22) |

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

Zárt: `tartalom-alapú` | `szó-szintű-tagged` | `interlineáris-gloss` | `kikövetkeztetett`.
*Mért kiindulás:* ma mind a 227 join-sor `tartalom-alapú` — a projektnek nincs szó-szintű
Strong-taggelt Károlija, és a döntési fájl 8. szakasza szerint nem is lesz (zárt licenc).

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

> **Ismert névütközés, nem oldódott meg** — a `motivumlog/lexikon_pilot/Motivum_kapcsolatok_PILOT.tsv`
> „Típus" oszlopa egy **másik tengely** (`LEXIKAI`/`NARRATÍV`/`STRUKTURÁLIS`/`TEMATIKUS`),
> mint az itteni `tipus`. A pilot-TSV-ben nincs önálló oszlop a PaRDeS Típus-mezőre.
> A betöltésnél (F3) a két tengelyt szét kell választani; ez a tábla a PaRDeS-tengelyt viszi.

### 2.4 `jeloltek.tsv` — a kereszthivatkozás-napló gépi alakja

Kulcs: `id` + `igehely`. **Ez a tábla a rendszer legfontosabb szerkezeti javítása.**

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | motívum-id | ✔ | |
| `igehely` | `IGEHELY` | ✔ | |
| `forras_kereses` | szabad szöveg | ✔ | Melyik lekérdezés hozta elő (`scan H7497`, `TSK 1Móz 6:4`, `Károli-KH`). |
| `dontes` | zárt | ✔ | `beépítve` \| `elutasítva` \| `nyitva`. |
| `indoklas` | szabad szöveg | ✔ | `elutasítva` esetén **kötelezően érdemi**. Egészséges jel, ha sok az *„elutasítva, mert csak a fölérendelt fogalmon keresztül tartozna ide"* tétel. |
| `karoli_szo` | szabad szöveg | | L. 2.4.1. |
| `azonositas_modja` | `AZONOSITAS_MODJA` | | |
| `megbizhatosag` | `MEGBIZHATOSAG` | | |
| `datum` | `DATUM` | ✔ | |

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
| `lepes` | zárt: `A5` \| `B2` \| `B3` \| `B4` | ✔ | A `MUNKAMENET.md` lépés-kódja, amely a lekérdezést futtatta. A `B3` a mező-hipotézis támasztó lekérdezése (`lekerdez.py domen`) — maga a hipotézis kézi, sort nem kap (TEREMT002_KUTATAS_BRIEF.md, D2, 2026.09.25). |
| `proveniencia` | `PROVENIENCIA` | ✔ | A `lekerdez.py` utolsó sora **szó szerint**, a `proveniencia: ` előtag nélkül — l. 1.5. |
| `datum` | `DATUM` | ✔ | |

Minden A5/B2/B3/B4-lekérdezés sort kap, **0 találatnál is** — a nyom a
lekérdezéshez tartozik, nem a találathoz. A lefedett dataset a `proveniencia`
`forras` kulcsából **származtatott**: a `+` mentén bontott fájlnevek, a
`datasetek.tsv` `fajl` mezőjének alapnevével pontos egyezéssel (nem
részsztring — l. 3.8 indoklása). A `lexikai-scan` subagent a proveniencia-sort
amúgy is szó szerint adja vissza; a rögzítés a fő szál feladata, nem a
subagenté.

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

Kulcs: `id` + `res`. A lexikonoldal (`_TUDOMANYOS.md`) hét kézi rése
(`kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`,
`modszertan`) motívumonkénti és résenkénti forrása — a render-elv szerint a
rés törzse nem a lexikonoldalon él, hanem a tanulmányban (RENDER_BRIEF.md G1).

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `id` | szabad szöveg | ✔ | Motívum-ID (`motivumok.tsv` kulcsa). |
| `res` | zárt | ✔ | `kivonat` \| `2b` \| `miert_fontos` \| `minosites` \| `alatamasztas` \| `ertelmezes` \| `modszertan`. |
| `fejlec` | szabad szöveg | ✔ | A rés fejlécsora a lexikonoldalon, szó szerint (RENDER_BRIEF.md G2/G4 — a `VAZ_SABLON` induló fejléce; a nulla-diff ezt bájtra megőrzi). |
| `forras` | zárt | ✔ | `lap` (a lexikonoldal mai, kézzel írt rése, változatlanul — átmeneti, RENDER_BRIEF.md G12) \| `tanulmany` (a `tanulmany` mezőben megadott fájl `<!-- RÉS-KEZDET: [res] -->…<!-- RÉS-VÉGE: [res] -->` jelölői közötti törzse) \| `adat` (a generátor adatból írja, pl. 0 kapcsolatnál az `alatamasztas`, RENDER_BRIEF.md G16). |
| `tanulmany` | szabad szöveg | `forras=tanulmany`-nál ✔, egyébként üres | A forrásfájl relatív útvonala — a motívum tematikus tanulmánya (`tematikus_lezart/*.md`) vagy — a `minosites` résnél — a kereszthivatkozás-napló (`tematikus_lezart/naplok/*.md`), RENDER_BRIEF.md G14. |

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
| `jelentes_szam` | union (l. 2.2.2) | ✔ | `szotar=UBS_DNTG` esetén a Louw–Nida `entry_kod` (pl. `33.176`, a régi `forditas_ubs.entry_kod`); egyébként azonos a 2.5 `jelentes_szam` értelmezésével. |
| `mezo` | zárt | ✔ | Melyik forrásmezőt fordítja ez a sor: `forditas_hu` (a 2.5 `szoveg_en`-jét), `definicio_hu` vagy `glosszak_hu` (a régi `forditas_ubs.tsv` két oszlopa). |
| `forras_hash` | szabad szöveg | ✔ | A forrásszöveg (az eredeti nyelvű, EN) SHA-1 hexdigestje (`hashlib.sha1(szoveg).hexdigest()`), UTF-8 kódolásból. Eltérés a forrás-hash és az újraszámolt hash között `ellenoriz.py`-sértés (S1.5, 13. szabály). A forrásszöveg a `lexikon_hivatkozasok.tsv` `szoveg_en`-je (UBS-nél a `UBS_DNTG_jelentesek.tsv`); ha ott nincs sor, és a sor `szotar ∈ {Thayer, BDB}`, `jelentes_szam=teljes`, `mezo=forditas_hu`, akkor a `konkordancia/Thayer_teljes.tsv` / `BDB_teljes_unabridged.tsv` `Teljes_szocikk` mezője (kulcs: `strong` → `Strong_padded`, az `entry_id`-nek a `Strong_eredeti`-vel kell egyeznie; F28 DT24 (b)). |
| `forditas_hu` | szabad szöveg | ✔ | A fordítás szövege — ugyanaz a tartalmi szabály, mint a 2.5-ben leírt `forditas_hu`-nál. |
| `allapot` | zárt | ✔ | `kezi` (a migrált, ember által korábban jóváhagyott sorok; az F28-ban a felhasználó által jóváhagyott Opus-fordítás) \| `opus` (a teljes Thayer-/BDB-szócikk Opus-fordítása, kapukon átment, emberi jóváhagyás nélkül, l. `F28_EMELES_BRIEF.md` E4) \| `sonnet` (a teljes Thayer-/BDB-szócikk Sonnet-fordítása, kapukon átment, emberi jóváhagyás nélkül; F38, DT-F38e) \| `pilot` (az `eszkozok/fordit.py` próba-kimenete, l. `F03_FORDITAS_PILOT_BRIEF.md`) \| `elavult` (a `forras_hash` már nem egyezik, `ellenoriz.py` javaslata). |
| `modell` | szabad szöveg | | A fordító LLM modell-azonosítója (pl. `anthropic/claude-haiku-4.5`); üres, ha `allapot=kezi` és nem model-fordítás. Az F28 jóváhagyott (`kezi`) Opus-fordításainál kitöltve marad (`claude-opus-5-5`); az F38 `sonnet` soraiban a Sonnet modell-azonosítója (`claude-sonnet-5-5`). Az `emeles.py rogzit --modell` kötelező (nincs alapérték): a címke a ténylegesen fordító modellt jelöli (F38.265) — a jóváhagyás az állapotot változtatja, a provenienciát nem. |
| `datum` | `DATUM` | ✔ | A migrált soroknál a forrás utolsó tartalmi módosításának git-dátuma (a `lexikon_hivatkozasok.tsv` soraira) vagy a korábbi `forditas_ubs.proveniencia` jóváhagyási dátuma (az UBS-soroknál); új soroknál a fordítás dátuma. |
| `terminologia_verzio` | szabad szöveg | | A 2.15 `terminologia.tsv` verziója, amellyel a fordítás készült; üres a migrált (a terminológia-tábla előtti) soroknál. |
| `megjegyzes` | szabad szöveg | | A megszűnt `forditas_ubs.tsv` `megjegyzes` oszlopának öröksége — lábjegyzet-hivatkozás vagy a fordítói döntés indoklása. A render nem olvassa (csak emberi/archív jegyzet); üres a legtöbb sornál. |

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
| `cimke` | zárt (F42 / DT-F42g): a generált nézetekben megjelenő rövid licenc-címke; **kötelező minden sorra**. Értékek: `közkincs` \| `CC0 1.0` \| `CC BY 4.0` \| `CC BY-SA 4.0` \| `© Mounce 1993` \| `projekt-adat` \| `tisztázatlan`. Szabály: `allapot=tisztazatlan` sor címkéje `tisztázatlan` (kivétel: a `projekt_adat` sor, címkéje `projekt-adat`); `tisztazott` és `kozkincs` sor címkéje a `licenc` oszlop szerinti rövid név. Új típusú licencnél a címke-értékkészlet bővítése SEMA-változtatás. A tábla **utolsó** oszlopa. |

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
3. A `projekt_adat` sor a repó saját adatáé; a repónak nincs LICENSE-fájlja, tehát a
   kimeneti réteg licence nyitott kérdés (DT-F24).

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
összevetés). Az első hat könyvből két modellel az 1Móz (`parok_1Moz.tsv`, `szavak_1Moz.tsv`), a 2Móz (`parok_2Moz.tsv`, `szavak_2Moz.tsv`; a 2Móz 35:36–36:37 versei a versbeosztás-detektor megfeleltetésével, a `2Móz_javito` javító menetből, l. `naplok/F22_2Moz_jelentes.md` 5.1, 5.5). Az `er` sorok `vers` oszlopa a **Károli-kulcs**: a megfeleltetett eredeti vers tokenjei (pl. a `2Móz 35:36` `er` sorai az F22 idején a TAHOT 36:1 szavai voltak; az F85.6 óta ezek a `TAHOT_kivonat.tsv` `2Móz 35:36` kulcsán állnak); a megfeleltetés nélküli eredeti vers a saját kulcsán, ha az foglalt, `+1000`-es verssorszámú azonosítón szerepel (nem igehely; a jelenlegi 2Móz–4Móz listában ilyen nincs: a 4Móz 30:1 a kézi 1:2 beolvasztásba kerül), `kezi` állapotban. **Az F85.6 (a `TAHOT_kivonat.tsv` versszintű átkulcsolása) és az F85.8 óta** a TAHOT-kulcs maga Károli-kulcs, az `f22/versmegfeleltetes.tsv` ÓSZ-sora és a kézi tábla adatsora kivezetve (az alábbi felsorolás az F22-beli előállítás állapotát írja le; `naplok/F85_jelentes.md`). A megfeleltetés a `f22/versmegfeleltetes.tsv` jóváhagyott könyveire érvényes volt (`tokenek.VERSBEOSZTAS_JOVAHAGYOTT`: 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón, Ezsd, Ez, Péld, Bír, Jób, Eszt, 2Sám, 1Sám; a 3Mózesnek, az 5Mózesnek, a Józsuénak, a Zsoltároknak, a Jeremiásnak, az 1Krónikának, a 2Krónikának, az Ezsdrásnak, az Ezékielnek, a Bíráknak, az Eszternek, a 2Sámuelnek és az 1Sámuelnek a listában nincs sora; a 4Mózesnél csak a 30. fejezet sorai; az Ézsaiásnál a detektor 9. és 64. fejezeti hibáját a `f22/versmegfeleltetes_kezi.tsv` kézi megfeleltetése javítja, a Példabeszédeknél ugyanez a 12. fejezet eltolását (Károli 12:n → TAHOT 12:(n+1)), a Jóbnál a 17. és a 37. fejezetét (Károli n → TAHOT n+1) és a 40. fejezetét (Károli 40:n → TAHOT 40:(n+5), #83); a kézi táblát a detektor regenerálása nem írja felül, jóváhagyás: `naplok/F22_versbeosztas_jovahagyas.md`). **Kézi 1:2 beolvasztás** (`f22/versosszevonas.tsv`; az F85.10 óta a beolvasztott vers tokenjei a közös Károli-kulcson állnak, a fájl `er_tol`–`er_ig` oszlopa jelöli a helyüket): a Károli-vers egy szakasza és az eredeti vers tokenjei `kezi` (nincs link, nem `betoldas`); az eredeti vers `er` sorai a Károli-vers saját eredeti szavai után folytatott sorszámmal szerepelnek (4Móz 29:39 hu 25–38, er 31–43 = TAHOT 4Móz 30:1; 2:1 irányban ugyanígy: Ézs 9:20 hu 15–34 = TAHOT Ézs 9:20, Ézs 64:1 hu 12–31 = TAHOT Ézs 64:2, Péld 11:31 hu 15–30 = TAHOT Péld 12:1, Jób 16:22 hu 14–21 = TAHOT Jób 17:1, Jób 36:33 hu 13–21 = TAHOT Jób 37:1). **Csak-Sonnet könyv** (3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón, Ezsd, Ez, Péld, Bír, Jób, Eszt, 2Sám és 1Sám, `parok_3Moz.tsv`, `szavak_3Moz.tsv`, `parok_4Moz.tsv`, `szavak_4Moz.tsv`, `parok_5Moz.tsv`, `szavak_5Moz.tsv`, `parok_Jozs.tsv`, `szavak_Jozs.tsv`, `parok_Zsolt.tsv`, `szavak_Zsolt.tsv`, `parok_Ezs.tsv`, `szavak_Ezs.tsv`, `parok_Jer.tsv`, `szavak_Jer.tsv`, `parok_1Kron.tsv`, `szavak_1Kron.tsv`, `parok_2Kron.tsv`, `szavak_2Kron.tsv`, `parok_Ezsd.tsv`, `szavak_Ezsd.tsv`, `parok_Ez.tsv`, `szavak_Ez.tsv`, `parok_Peld.tsv`, `szavak_Peld.tsv`, `parok_Bir.tsv`, `szavak_Bir.tsv`, `parok_Job.tsv`, `szavak_Job.tsv`, `parok_Eszt.tsv`, `szavak_Eszt.tsv`, `parok_2Sam.tsv`, `szavak_2Sam.tsv`, `parok_1Sam.tsv`, `szavak_1Sam.tsv`, l. `naplok/F22_5Moz_jelentes.md`, `naplok/F22_Jozs_jelentes.md`, `naplok/F22_Zsolt_jelentes.md`, `naplok/F22_Ezs_jelentes.md`, `naplok/F22_Jer_jelentes.md`, `naplok/F22_1Kron_jelentes.md`, `naplok/F22_2Kron_jelentes.md`, `naplok/F22_Ezsd_jelentes.md`, `naplok/F22_Ez_jelentes.md`, `naplok/F22_Peld_jelentes.md`, `naplok/F22_Bir_jelentes.md`, `naplok/F22_Job_jelentes.md`, `naplok/F22_Eszt_jelentes.md`, `naplok/F22_2Sam_jelentes.md`, `naplok/F22_1Sam_jelentes.md`; az Ézs, a Jer, az 1Krón, a 2Krón, az Ezsd, az Ez, a Péld, a Bír, a Jób, az Eszt, a 2Sám és az 1Sám a Message Batches API-n, DT73 (a); DT-F22c: a C kimarad): nincs C-fájl, ezért minden link és szó `alacsony`, `forras: S` (a végleges kapuhibás és a kézi beolvasztott versek szavai `kezi`, pl. 1Krón 19:2, 2Sám 23:16, Ézs 9:20, 64:1, Péld 11:31, Jób 16:22, 36:33; egy modell, nincs egyezés; a `magas` jelölés nincs), a proveniencia-sor `ts=manual` (nincs C futásnapló), az `f22_elemzes.py` „gyanús fejezetek” sora minden fejezetet jelez (nem eltolódás-jel); a többi könyv ugyanezzel a
sémával, a könyv-paraméter cseréjével. A fájlnév a magyar könyvrövidítés ékezet nélküli alakja.

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
együtt a #12 pilotja véglegesíti. A `javaslat` jelölésű pontokról a `DONTESEK.md`
DT84 tétele dönt. A D35 szabálya (generált fájlba kézzel nem írunk) a 3/9-ben áll; ez
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
`belso` mindent. Nyilvános nézet csak `olvasoi` vagy `apparatus` mélységű lehet.

#### 3.10.2 A jelölés blokkszintű, gépileg olvasható

- **Alapszint:** minden szakasz alapszintje a forrássablon 4. pontjának táblázatában áll;
  a forrásban ehhez jelölő nem kell. Ismeretlen (a táblázatban nem szereplő) szakasz
  szintje `belso` (zárt alapérték, l. 3.10.4).
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

*[javaslat: DT84 (1) — a jelölőpár alakja. A #64 ideiglenes alakja (`<!-- SZINT: x -->` a
következő jelölőig) írás közben kezelhető volt, de a hatóköre nem volt kimondva
(`naplok/TEREMT002_PROZA_PROBA_meres.md` 3. szakasz, 2. tanulság); a pár ezt zárja le.]*

#### 3.10.3 A `【NAPLO】` mindig `belso`

A `【NAPLO: …】` blokk szintje mindig `belso`, attól függetlenül, milyen szintű szakaszban
vagy jelölőpárban áll; külön jelölő nem kell hozzá (DT66 (a) 1. kivétel: kézi, de nem az
érvelés része). Kinyerés belőle nincs (az `adat` alternatíva elvetve, DT66 (a) 1.).

#### 3.10.4 Engedélyezőlista és build-kihagyás (D36)

- **Engedélyezőlista:** a nyilvános nézet csak azt veszi fel, ami a forrássablon
  szakaszlistáján szerepel, aktív (forrássablon 3. pont), és szintje legfeljebb a nézet
  mélysége. Ami nincs a listán (ismeretlen szakasz, ismeretlen jelölő), az kimarad —
  zárt alapérték, nem nyitott.
- **Build-kihagyás, nem elrejtés:** a `belso` blokk a nyilvános nézet felépítésekor **nem
  kerül a kimenetbe**. Nem HTML-megjegyzésbe, nem `<details>` alá, nem CSS-sel rejtve: a
  nyilvános fájlban a szövege nem létezik. Ugyanígy kimarad minden csak-forrásbeli jelölő
  (`SZINT-*`, `INAKTÍV`, `JELÖLT`, `ADAT-HIV`, `ADAT-ÉRTÉK`, `FORRÁSRÉTEG`).
- Gépi ellenőrzés: CI E29 (`naplok/MOTIVUM_FORRAS_ci_terv.md`).

#### 3.10.5 Kinyerés jelölőnként — (b) → (a)

A 3/9 egyirányúsági szabályára épül: a kinyerés a forrásból **csak jelölt-sort** ír a
`jeloltek.tsv`-be, `manual` provenienciával; a jelölt-sorról ember dönt (3/2), és **a
generátor a forrásba nem ír**. Más táblába a kinyerés közvetlenül nem ír.

| Jelölő (forrássablon 6. pont) | Tábla | Kulcs | Mit ír | Proveniencia | Ütközés (a kulcs már létezik) |
|---|---|---|---|---|---|
| `<!-- JELÖLT: [igehely] \| gerinc: [gerinc_elem] \| [indoklás] -->` | `jeloltek.tsv` (2.4) | `id` + `igehely` | `dontes=nyitva`, `indoklas` = a jelölő indoklása, `datum` = a kinyerés napja | a `forras_kereses` mezőben: `scope=manual \| forras=motivumok/[ID].md#[szakasz] \| ts=[DATUM]` (1.5) | nem ír; a kinyerési jelentés jelzi, hogy a jelölt már minősítve van |
| proveniencia-lábjegyzet (bármely `scope`) | — (hivatkozás) | — | semmit: a lábjegyzet a próza állításának forrás-hivatkozása; az audit-sort a 2.9 szerint a lekérdezést futtató fő szál rögzíti, nem a kinyerés | — | — |
| `ADAT-HIV`, `ADAT-ÉRTÉK` | — (ellenőrző) | a jelölőben megadott | semmit; hiány vagy eltérés a kinyerési jelentésbe | — | — |
| szerkezeti jelölők (`FORRÁSRÉTEG`, `SZINT-*`, `【NAPLO】`, `INAKTÍV`, `RÉS-*`, `ADAT-NÉZET`) | — | — | semmit | — | — |

- **Előléptetés:** a jelölt-sorból az `elofordulasok.tsv` sora csak döntéssel
  (`dontes=beépítve`) lesz (3/2); a sor `proveniencia` mezője a jelölt `forras_kereses`
  proveniencia-sora (`scope=manual`), az `igazolas` mezője az 1.8 szerint. A `manual`
  sor a generált kimenetben értelmezésként jelölendő (3/3).
- **Audit-út a lábjegyzetből:** *[javaslat: DT84 (2) — a `scope≠manual` lábjegyzetből
  közvetlenül, döntés nélkül írt `auditok.tsv`-sor ütközne a 3/9-cel (kinyerés csak a
  `jeloltek.tsv`-n át, `manual` provenienciával, döntéssel). Opciók: (a) nincs
  audit-kinyerés, a lábjegyzet csak hivatkozás (ez a fenti normatív szöveg); (b) a
  `jeloltek.tsv`-n át, döntéssel; (c) a 3/9 módosítása külön döntéssel. Ha a (b) vagy
  a (c) nyer, a `lepes` mezőt a lábjegyzet kulcsának előtagja vagy egy zárójeles címke
  hordozza, mert a proveniencia-sor szó szerinti, abba új kulcs nem írható.]*
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

#### 3.10.7 Nyitott séma-kérdések (DT66 (a) megjegyzése; *javaslat*, DT84 (3), (8))

A DT66 (a) a Minősítés, az Alátámasztás és a 7. Módszertan `adat`-besorolását fogadta el,
azzal a megjegyzéssel, hogy új oszlopot kérhet. A mai sémával:

1. **Alátámasztás → `kapcsolatok.tsv`:** a soronkénti funkció-/bizonyosság-indoklásnak
   nincs oszlopa (2.3: `funkcio` van, indoklás nincs). Új `indoklas` oszlop kell, vagy az
   Alátámasztás `kezi_forras` marad.
2. **Minősítés → `jeloltek.tsv`:** az „új találat” és a „nem releváns” a `dontes`
   (`beépítve` / `nyitva` / `elutasítva`) és az `indoklas` mezőbe képezhető, a
   kereszthivatkozás forrás-verse a `forras_kereses` mezőbe (`TSK [igehely]`). A
   „független megerősítés” viszont egy már beépített igehelyre szól; a kulcs (`id` +
   `igehely`) miatt második sor nem írható. Új érték vagy oszlop kell, vagy a megerősítés
   a minősítés-nézetben generált (a TSK-találat és a beépített sor metszete).
3. **Módszertan-tábla és kapu-eredmény → `auditok.tsv`:** a `lepes` értékkészlete
   (`A5` | `B2` | `B3` | `B4`) a retroaktív ellenőrzési rétegeket és a Q-kapu eredményét
   nem fedi, és ezek többségéhez nincs `lekerdez.py`-proveniencia. Lehetőség: új `lepes`
   érték, új tábla, vagy a régi rétegtáblák archívumba (a nézet a meglévő audit-sorokból
   generálódik).
4. **Nem igehely-kulcsú adat a prózában** (szótári idézet, LXX-megfelelő): a
   `jeloltek.tsv` kulcsa igehely, ezért jelölt-sor nem írható (`naplok/F78_meres.md`
   12. szakasz 2. pont); a tervezet az `ADAT-HIV` ellenőrző utat adja (3.10.5).

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
