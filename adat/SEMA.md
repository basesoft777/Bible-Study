# `adat/` — séma

**Verzió:** v1 — 2026.09.13
**Forrás:** `ATALAKITASI_TERV.md.md` 1.A pont (tábla-lista), 4.2 (proveniencia), 4.5 (gerinc-elem), 4.6 (gate-mezők), 4.7 (Károli-join)
**Fázis:** F1.2

Ez a réteg a **kanonikus igazságforrás**. A `tematikus_lezart/`, `genezis/`, `motivumlog/`
és `lexikon/` kimenetei ebből generálódnak vagy ehhez igazodnak. Ha egy tény itt és egy
markdown-fájlban ellentmond, **ez a tábla az irányadó**.

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
| **magyar kanonikus** (ez a séma alakja) | `TAHOT_kivonat.tsv`, `TAGNT_kivonat.tsv`, `TSK_kereszthivatkozasok.tsv`, `Karoli_1908.tsv`, `LXX_kivonat_*.tsv` | `1Móz 1:1` |
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
| `fajl` | a dataset útvonala; glob is lehet (`konkordancia/LXX_kivonat_*.tsv`), üres, ha `allapot=hianyzik` |
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
  Ugyanígy `korlatos` a `BSB_Strongs` (F16): csak a 95%-os küszöböt elérő 31 ÓSZ-könyv, ÚSZ szándékosan nincs (a görög réteg forrása a Macula, #87);
  a Zak 12:1 és a 116 feliratos zsoltár 1. versének érdemi szövege a display-forrásból hiányzik (a text-only megvan);
  a Zsolt-sorok MT-számozásúak (a Zsolt 13 illesztetlen, kimarad), a többi könyv BSB/angol számozású.

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

Kulcs: `tanulmany` + `igehely` + `strong`. **Átmeneti tábla:** a bővített sablon 2.
pontjának kulcsszó-táblázatát viszi géppel olvasható alakba, mielőtt a betöltés
motívum-ID-t rendelne hozzá. Az `id` mező szándékosan **nincs** ezen a táblán — az
csak az A4 lépésben, a `jeloltek.tsv`-ben születik meg (l. 2.4 és `F8_BRIEF.md` §1 L4). A `betolt.py`
(A3 irány, G2a) írja; kézzel nem bővítendő.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `tanulmany` | fájlút | ✔ | A forrás bővített tanulmány útvonala. |
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

Kulcs: `nyelv` + `sorrend`. 11 szerep × 2 nyelv = 22 sor, statikus tábla (nem
motívumonkénti): melyik szótári forrás felel meg egy adott „kérdéstípusnak"
(pl. „Alapjelentés", „Mélységi szócikk") mindkét nyelven, és a forrás ma
adatosítva van-e a projektben.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `nyelv` | zárt | ✔ | `gorog` \| `heber`. |
| `sorrend` | egész szám | ✔ | 1–10 és 12, a szerep-lista rögzített sorrendje (azonos mindkét nyelven); a 11-es érték nincs kiosztva. A 12. a „Tematikus index” (Nave, F18, DT18 (j)); az első 10 az eredeti szerepkészlet. |
| `szerep` | szabad szöveg | ✔ | A szerep megnevezése (pl. „Alapjelentés", „LXX-híd"). |
| `forras` | szabad szöveg | ✔ | A szerepet ma (vagy célként) kitöltő forrás megnevezése. |
| `allapot` | zárt | ✔ | `adatosítva` \| `nincs adatosítva` \| `nincs forrás` \| `javaslat` (F05_SZOTAR_BRIEF.md D27, S1.6; `javaslat`: F18.12, DT18) — a RENDER_BRIEF.md G6 záró bekezdése szerint: adatosítva a TBESG, TBESH, Thayer, BDB, UBS DNTG (a meglévő import), SDBH domének, LSJ és az LXX-híd (mindkét irány); a többi (Girdlestone, UBS DBH glossza+referencia, Mounce-kiegészítő önmagában, SECE, BDB-etimológia, kiejtés) a `F05_SZOTAR_BRIEF.md` tárgya. **`nincs forrás`** (D27): a szerepnek az adott nyelven nincs a D17 forrásszabálynak megfelelő forrása — VÉGLEGES állapot, nem pótlandó hiány (szemben a `nincs adatosítva`-val, amely ígéretet sugallna); pl. a görög 3. szerep, ha a Translation Words elutasításra kerül (S0b.2 küszöbe alatt). **`javaslat`** (F18.12): az adat a repóban van, de teljessége/helyessége független igazolással nincs megerősítve (ma: a 12. „Tematikus index” szerep, a Nave-import, l. `naplok/F18_import_naplo.md`); a generátorok ezt nem adatosítottnak kezelik (csak az `adatosítva` érték számít adatosítottnak). |

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
| `allapot` | zárt | ✔ | `kezi` (a migrált, ember által korábban jóváhagyott sorok; az F28-ban a felhasználó által jóváhagyott Opus-fordítás) \| `opus` (a teljes Thayer-/BDB-szócikk Opus-fordítása, kapukon átment, emberi jóváhagyás nélkül, l. `F28_EMELES_BRIEF.md` E4) \| `pilot` (az `eszkozok/fordit.py` próba-kimenete, l. `F03_FORDITAS_PILOT_BRIEF.md`) \| `elavult` (a `forras_hash` már nem egyezik, `ellenoriz.py` javaslata). |
| `modell` | szabad szöveg | | A fordító LLM modell-azonosítója (pl. `anthropic/claude-haiku-4.5`); üres, ha `allapot=kezi` és nem model-fordítás. Az F28 jóváhagyott (`kezi`) Opus-fordításainál kitöltve marad (`claude-opus-5-5`) — a jóváhagyás az állapotot változtatja, a provenienciát nem. |
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
legfeljebb tükör, és ha ellentmond, **ez a tábla az irányadó**. (A `lexikon_general.py`
`LICENC`-konstansához és a `TISZTAZATLAN_SZOTARAK`-hoz az F24 nem nyúlt; az átállás az N9
lezárása, l. lent.)

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

**Két bővítés a briefhez képest.** A `kereskedelmi` és a `share_alike` oszlop a
`tisztazatlan` értéket is felveszi: egy ismeretlen licencű forrásnál sem `igen`, sem `nem`
nem állítható (CLAUDE.md 3. szabály, a hiányt nem töltjük ki). A `feltetelesen` a
licenc-szövegen túli feltételt jelöl (pl. védjegy-szabály, UK Crown-jog).

**Szabályok.**

1. A `share_alike = igen` sorok (CC BY-SA: SDBH, SDGNT, UBS_DBH, UBS_DNTG,
   SDBH_SDGNT_segedtablak, tW_szocikkek; hat sor, mind `tisztazott`; az LSJ állítólag CC BY-SA 3.0, de `tisztazatlan`, ezért `share_alike=tisztazatlan`) megjegyzése rögzíti: a belőlük
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
3. A `projekt_adat` sor a repó saját adatáé; a repónak nincs LICENSE-fájlja, tehát a
   kimeneti réteg licence nyitott kérdés (DT-F24).

**N9 (a licenc-besorolás kettős forrása) lezárásának javaslata.** A `NYITOTT_FELADATOK.md`
N9 tétele szerint a besorolás a `lexikon_general.py` `LICENC`-konstansában és a
`TISZTAZATLAN_SZOTARAK` halmazban él. A `licencek.tsv` után a lezárás: (1) a generátor
`LICENC` dict-je a `licencek.tsv` `dataset` → `licenc` leképezéséből töltődik (a lexikon
szótárkulcsai megegyeznek a `dataset` azonosítókkal, kivéve `UBS` és `projekt-adat`:
ezekre kis megfeleltetés kell); (2) `TISZTAZATLAN_SZOTARAK = {d for d in licencek if allapot == 'tisztazatlan'}`,
vagyis a halmaz a tábla `allapot` oszlopából származik, nem kézzel áll; (3) a konstans és a
tábla összevetése CI-ellenőrzés (E-szabály) legyen. A mai konstans és a tábla eltérései:
`Thayer`, `LSJ`, `SECE_G`, `SECE_H`, `MCGED`, `TSK`, `BDB`, `LXX_OS` és a `projekt-adat` kulcs (a táblában `projekt_adat`) a konstansban besorolt, a táblában
`tisztazatlan` — ezek (2) után a halmazba kerülnének, és a generátor tisztázatlan-jelölést
adna rájuk. Ez az F24 hatókörén kívüli kód- és render-változás, ezért külön tétel.

### 2.20 `adat/karoli_strong/parok_<könyv>.tsv` és `szavak_<könyv>.tsv` — Károli–Strong párosítás könyvenként

**Állapot: javaslat (modell-kimenet), nem lekérdezés-eredmény.** Két modell (Sonnet a Code-ban, Gemini az
Actionsben) független párosítása ugyanazzal a prompttal (`f21p/prompt_v3.md`, befagyasztva); az
`eszkozok/karoli_strong/egyesit.py` determinisztikusan (API nélkül) állítja elő. A modell Strong-számot
nem ír: a `strong` a TAHOT-ból jön, a linkelt eredeti szó sorszáma alapján. Mivel nem `lekerdez.py`
eredmény, a két tábla **első sora egy `#`-kezdetű proveniencia-sor** (a `licencek.tsv` mintájára; az olvasók átugorják),
`scope=manual | forras=… | ts=…` alakban (1.5); a `ts` a C futásnapló utolsó időbélyege, tehát a bemenetekből származik, és az
újraépítés bájtra azonos marad. A tábla modell-kimenet, javaslat (CLAUDE.md 1. szabály: a `bizonyossag` nem „ellenőrizve”). A zárt licencű Károli–Strong
forrás adata nem része a tábláknak (l. `eszkozok/karoli_strong/zart_osszevet.py`: csak helyi, összesített
összevetés). Az első négy könyv az 1Móz (`parok_1Moz.tsv`, `szavak_1Moz.tsv`), a 2Móz (`parok_2Moz.tsv`, `szavak_2Moz.tsv`; a 2Móz 35:36–36:37 versei a versbeosztás-detektor megfeleltetésével, a `2Móz_javito` javító menetből, l. `naplok/F22_2Moz_jelentes.md` 5.1, 5.5). Az `er` sorok `vers` oszlopa a **Károli-kulcs**: a megfeleltetett eredeti vers tokenjei (pl. a `2Móz 35:36` `er` sorai a TAHOT 36:1 szavai); a megfeleltetés nélküli eredeti vers a saját kulcsán, ha az foglalt, `+1000`-es verssorszámú azonosítón szerepel (nem igehely; a jelenlegi 2Móz–4Móz listában ilyen nincs: a 4Móz 30:1 a kézi 1:2 beolvasztásba kerül), `kezi` állapotban. A megfeleltetés a `f22/versmegfeleltetes.tsv` jóváhagyott könyveire érvényes (`tokenek.VERSBEOSZTAS_JOVAHAGYOTT`: 2Móz, 3Móz, 4Móz, 5Móz; a 3Mózesnek és az 5Mózesnek a listában nincs sora; a 4Mózesnél csak a 30. fejezet sorai, jóváhagyás: `naplok/F22_versbeosztas_jovahagyas.md`). **Kézi 1:2 beolvasztás** (`f22/versosszevonas.tsv`): a Károli-vers egy szakasza és az eredeti vers tokenjei `kezi` (nincs link, nem `betoldas`); az eredeti vers `er` sorai a Károli-vers saját eredeti szavai után folytatott sorszámmal szerepelnek (4Móz 29:39 hu 25–38, er 31–43 = TAHOT 4Móz 30:1). **Csak-Sonnet könyv** (3Móz és 4Móz, `parok_3Moz.tsv`, `szavak_3Moz.tsv`, `parok_4Moz.tsv`, `szavak_4Moz.tsv`; DT-F22c: a C kimarad): nincs C-fájl, ezért minden link és szó `alacsony`, `forras: S` (egy modell, nincs egyezés; a `magas` jelölés nincs), a proveniencia-sor `ts=manual` (nincs C futásnapló), az `f22_elemzes.py` „gyanús fejezetek” sora minden fejezetet jelez (nem eltolódás-jel); a többi könyv ugyanezzel a
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

---

## 4. Amit ez a séma nem old meg

- **A `TAHOT_kivonat.tsv` lefedettségi rése — F2-ben tételesen felmérve (2026.09.14).**
  A korábban itt és a `NYITOTT_FELADATOK.md`-ben rögzített tétel (1Móz 32, Zsolt
  88/89/140/142, Jóel 3 hiánya) **elavultnak bizonyult**: mind a hat fejezet teljes
  egészében jelen van — ezt a `TAHOT_TAGNT_README.md` már korábban dokumentálta pótlásként,
  csak ez a két fájl nem lett frissítve utána. A tételes, mind a 39 könyvre kiterjedő
  fejezet- és versszintű ellenőrzés (`eszkozok/tahot_lefedettseg_ellenoriz.py`) helyette egy
  **korábban nem dokumentált** hiányt talált: **Jób 40:1-5 és a teljes Jób 41. fejezet
  hiányzik** — valószínűleg a Jób könyvének 40-41. fejezeteinél ismert héber/angol
  versszámozási eltolódás miatt, ez a forrás STEPBible-fájlból tételesen még
  ellenőrizendő (l. `TAHOT_TAGNT_README.md`). **A `scope` proveniencia-értéke ettől
  függetlenül `TAHOT-teljes` marad, nem `OT-full`** — ez a kivonat egészére vonatkozó,
  nem a kánon teljességét állító címke, és az `eszkozok/lekerdez.py` minden parancsa
  ezt írja ki.
- **A `kapcsolatok.tipus` és a pilot-TSV „Típus" oszlopának névütközése** (l. 2.3).
- **Az SDBH lefedettsége** (l. 2.6) — kb. 90%; gyakori szavak is hiányoznak (pl. H1961, H5414, H6440), ezért a `domen` üres eredménye nem negatív lelet.
- **A `keretszo` lista teljessége.** 34 tétel, gyakoriság alapján válogatva. Nem állítjuk,
  hogy teljes; bővítése az F3 betöltés tapasztalatai alapján várható.
