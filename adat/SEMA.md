# `adat/` — séma

**Verzió:** v1 — 2026.09.13
**Forrás:** `ATALAKITASI_TERV.md.md` 1.A pont (tábla-lista), 4.2 (proveniencia), 4.5 (gerinc-elem), 4.6 (gate-mezők), 4.7 (Károli-join)
**Fázis:** F1.2

Ez a réteg a **kanonikus igazságforrás**. A `tematikus_lezart/`, `genezis/`, `motivumlog/`
és `lexikon/` kimenetei ebből generálódnak vagy ehhez igazodnak. Ha egy tény itt és egy
markdown-fájlban ellentmond, **ez a tábla az irányadó**.

A hét tábla és a hozzájuk tartozó kulcs:

| Fájl | Kulcs | Ki írja |
|---|---|---|
| `motivumok.tsv` | `id` | `betolt.py` / kézzel, validálva |
| `elofordulasok.tsv` | `id` + `igehely` | `betolt.py`, jelöltből előléptetve |
| `kapcsolatok.tsv` | `forras_igehely` + `cel_igehely` + `id` | `betolt.py` / kézzel |
| `jeloltek.tsv` | `id` + `igehely` | `lekerdez.py` írja, ember minősíti |
| `lexikon_hivatkozasok.tsv` | `strong` + `entry_id` + `jelentes_szam` | `betolt.py` |
| `datasetek.tsv` | `study_tipus` + `dataset` | kézzel (policy-tábla) |
| `grammatikai_strongok.tsv` | `strong` | **generált** — `eszkozok/grammatikai_strongok_general.py` |

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
| `bdb_entry_id` | szabad szöveg | | A BDB-szócikk azonosítója. |
| `jelentes_szam` | **union** | | L. 2.2.2 — ez a mező a 3.8-as nyitott tétel lezárása. |
| `jelentes_en` | szabad szöveg | | A szótári jelentés eredetiben. |
| `jelentes_hu` | szabad szöveg | | Magyar fordítása. |
| `karoli_szo` | szabad szöveg | | A Károli-szóalak ezen a helyen. **Öröklődik a `jeloltek.tsv` azonos kulcsú sorából.** |
| `azonositas_modja` | `AZONOSITAS_MODJA` | | Kötelező, ha `karoli_szo` ki van töltve. |
| `megbizhatosag` | `MEGBIZHATOSAG` | | Kötelező, ha `karoli_szo` ki van töltve. |
| `proveniencia` | `PROVENIENCIA` | ✔ | L. 1.5. |

#### 2.2.1 A `gerinc_elem` mező — miért kötelező

Nem azért, mert enélkül hígulna a motívum, hanem mert **enélkül nem látszik, hogy nem
hígult.** A projekt megfigyelt hibái eddig határproblémák voltak (Rafaim ↔ Nefilim), nem
hígulás — de ez az információ eddig a munkamenet fejében élt, a fájlban csak az eredmény
maradt. A 49 soros HAMART-001 táblából nem állapítható meg, melyik horgonyon lóg a 38.

Ingyen van: a `lekerdez.py` tudja, melyik parancs melyik sort hozta.

*Kalibráció:* az opus-ág 49 sora ~8 gerinc-elemen állt, azaz ~6 sor elemenként. Húsz sor
egyetlen elemre **vizsgálandó — jelzés, nem tiltás.**

#### 2.2.2 A `jelentes_szam` mező — a 3.8-as tétel lezárása

**A mező típusa union: numerikus jelentés-szám VAGY binyan-címke.**

| Alak | Mikor | Példa |
|---|---|---|
| numerikus | a BDB számozott sense-ekre tagolja a szócikket (főnevek, melléknevek túlnyomó része) | `1`, `2`, `3a` |
| binyan-címke | **a BDB az igegyököket binyan szerint tagolja, nem számozott sense-ekkel** | `Nif'ál`, `Pi'él`, `Hif'íl` |
| binyan + igealak | ha a megkülönböztetés igealakon múlik | `Qal pass. ptc.`, `Qal impf.` |
| alternatíva | ha a hely két binyan között eldöntetlen | `Nif'ál / Hif'íl` |

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

Kulcs: `strong` + `entry_id` + `jelentes_szam`.

| Mező | Típus | Kötelező | Leírás |
|---|---|---|---|
| `strong` | `STRONG` | ✔ | |
| `szotar` | zárt | ✔ | `BDB` \| `Thayer` \| `LSJ` \| `Strong` \| `SDBH` \| `SDGNT` \| `SECE_G` \| `SECE_H` |
| `entry_id` | szabad szöveg | ✔ | |
| `jelentes_szam` | union (l. 2.2.2) | ✔ | |
| `szoveg_en` | szabad szöveg | ✔ | **Rövid kivonat, nem teljes szócikk** — a BDB-sorok egyenként több kilobájtosak. |
| `forditas_hu` | szabad szöveg | | |
| `forrasfajl` | fájlút | ✔ | Pl. `konkordancia/BDB_teljes_unabridged.tsv`. |

### 2.6 `datasetek.tsv`

Kulcs: `study_tipus` + `dataset`. A terv 4.3 mátrixa, négy study-típusra kifejtve
(`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`), 17 dataset × 4 = 68 sor.

| Mező | Értékkészlet |
|---|---|
| `study_tipus` | `bovitett` \| `tematikus` \| `melyelemzes` \| `lexikon_oldal` |
| `dataset` | a dataset rövid neve (17 érték) |
| `fajl` | a dataset útvonala; glob is lehet (`konkordancia/LXX_kivonat_*.tsv`), üres, ha `allapot=hianyzik` |
| `kotelezoseg` | `mindig` \| `felteteles` \| `ajanlott` \| `oroklott` |
| `feltetel` | mikor válik kötelezővé a `felteteles` sor; `—`, ha nem feltételes |
| `allapot` | `elerheto` \| `korlatos` \| `hianyzik` \| `generalt_nezet` |
| `megjegyzes` | a datasetre jellemző korlát vagy tudnivaló (study-típustól független) |

**Két `allapot` érték követel figyelmet:**

- `hianyzik` — az **SDBH és az SDGNT importja nem történt meg**. A terv 4.3 pontja ezeket
  új datasetként javasolja (UBS, CC BY-SA 4.0, a `ubsicap/ubs-open-license` repóból), és az
  F2 `domen` parancsa **ezekre épül**. Amíg az import nincs meg, a `domen` parancs nem
  implementálható, és az F2 harmadik elfogadási tesztje (az `arar`/`kalal` közös „Curse"
  doménje) nem futtatható.
- `korlatos` — a `KJV_ASV_Strongs` **csak Genezis, Exodus és Példabeszédek** könyvekre áll
  rendelkezésre. Bármely más könyvre hivatkozó „ellenőrizve" állítás ezen a dataseten hamis.

*Licenc-következmény, amit a `konkordancia/README.md`-nek rögzítenie kell:* a CC BY-SA 4.0
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

---

## 3. Integritási szabályok

Ezeket az `ellenoriz.py` (F4/commit-hook) kényszeríti ki. Amíg az nem készül el, kézi
ellenőrzés tárgyai.

1. **Hivatkozási épség.** `elofordulasok.id`, `kapcsolatok.id`, `jeloltek.id` → létező
   `motivumok.id`.
2. **Nincs közvetlen út.** Minden `elofordulasok` sorhoz tartozik `jeloltek` sor azonos
   kulccsal, `dontes=beépítve` értékkel.
3. **Proveniencia-kényszer.** `elofordulasok.proveniencia` nem lehet üres. Ha `manual`,
   a sor értelmezésként jelölendő a generált kimenetben.
4. **Horgony-kényszer.** `elofordulasok.gerinc_elem` nem lehet üres.
5. **Károli-triplet.** Ha `karoli_szo` ki van töltve, `azonositas_modja` és
   `megbizhatosag` is kötelező.
6. **Gate-kényszer** (4.6): `azonossag_tipusa`, `negativ_kriterium`, `folerendelt_fogalom`
   egyike sem lehet üres egy `publikálható` vagy `véglegesített` motívumnál.
7. **Ütközés- és részhalmaz-jelentés** (`gate.py`): mely motívumpárok osztoznak igehelyen;
   ha `B` igehely-halmaza ⊆ `A`, akkor **B nem önálló ID, hanem ↳ alpont**.
8. **Dataset-lefedettség.** Minden `mindig` és teljesült feltételű `felteteles` datasethez
   tartozzon legalább egy proveniencia-nyom a motívum sorai közt.

---

## 4. Amit ez a séma nem old meg

- **A `TAHOT_kivonat.tsv` lefedettségi rése.** A `TAHOT_TAGNT_README.md` „39 könyv, teljes
  ÓSZ"-t állít, de hiányzik legalább 1Móz 32 teljes fejezete, Zsolt 88/89/140/142 (150-ből
  88 zsoltárfejezet van jelen) és Jóel 3. Ez **minden** „teljes körű scan" állítás
  megbízhatóságát érinti, tehát a `PROVENIENCIA` `scope=OT-full` értékét is. Az F2 első
  lépése a tételes felmérés; addig a `scope=OT-full` **a kivonat teljességét jelenti, nem
  a kánonét**.
- **A `kapcsolatok.tipus` és a pilot-TSV „Típus" oszlopának névütközése** (l. 2.3).
- **Az SDBH/SDGNT hiánya** (l. 2.6) — az F2 `domen` parancsának előfeltétele.
- **A `keretszo` lista teljessége.** 34 tétel, gyakoriság alapján válogatva. Nem állítjuk,
  hogy teljes; bővítése az F3 betöltés tapasztalatai alapján várható.
