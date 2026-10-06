# Konkordancia — KJV-Strongs és ASV-Strongs (Példabeszédek, 1Mózes, 2Mózes)

Ez a mappa a PaRDeS-projekt Strong-számmal ellátott angol híd-forrásait tartalmazza,
szavankénti bontásban, a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` döntési fájl
4.8 és 4.9 pontjában rögzített módszertan szerint.

## Fájlok

| Fájl | Tartalom | Sorok (fejléc nélkül) |
|---|---|---|
| `KJV_Strongs_Proverbs.tsv` | KJV (King James Version) + Strong-számok + morfológiai kódok, Példabeszédek 1-31 | 5945 |
| `ASV_Strongs_Proverbs.tsv` | ASV (American Standard Version, 1901) + Strong-számok, Példabeszédek 1-31 | 5872 |
| `KJV_Strongs_Genesis.tsv` | KJV + Strong-számok + morfológiai kódok, 1Mózes 1-50 | 15098 |
| `ASV_Strongs_Genesis.tsv` | ASV + Strong-számok, 1Mózes 1-50 | 14917 |
| `KJV_Strongs_Exodus.tsv` | KJV + Strong-számok + morfológiai kódok, 2Mózes 1-40 | 12253 |
| `ASV_Strongs_Exodus.tsv` | ASV + Strong-számok, 2Mózes 1-40 | 12119 |

## Oszlopok

**KJV_Strongs_*.tsv:**
```
Igehely | Szósorszám | Strong-szám | Angol szó | Morfológiai kód
```

**ASV_Strongs_*.tsv:**
```
Igehely | Szósorszám | Strong-szám | Angol szó
```
(Az ASV-forrás nem tartalmaz morfológiai kódot.)

- **Igehely:** STEPBible-natív formátumban, pl. `Pro.23.7`, `Gen.17.5` — lásd az
  "Igehely-formátum" szakaszt lent, miért ez lett a végleges konvenció mind a négy
  fájlban.
- **Szósorszám:** a szó sorszáma a versen belül (1-től indul)
- **Strong-szám:** héber Strong-szám (H-szám), mert mindkét feldolgozott könyv (Péld,
  1Móz) ószövetségi — **fontos:** ez a forrás (studybible.info) **nem nulla-kitöltött**
  formában adja a Strong-számot (pl. `H85`, nem `H0085`), szemben a TAHOT/TAGNT- és
  TIPNR-kivonattal, ami 4 számjegyre kitölti (`H0085`). Egy jövőbeli összekapcsolásnál
  ezt normalizálni kell (a vezető nullák hozzáadásával/levágásával).
- **Angol szó:** a ragozott angol szóalak, pontosan ahogy a forrás megjeleníti (a szomszédos írásjelek — vessző, kettőspont — a szóhoz tartozó span részeként jelennek meg a forrásban, ezért változatlanul megmaradtak)
- **Morfológiai kód (csak KJV-nél):** a forrásban szögletes zárójelben jelzett igei/névszói alakinformáció (pl. `[H8798]`); ha egy szóhoz több morfológiai jelölés is tartozik (pl. Kethiv/Qere-változat), szóközzel elválasztva, egy cellában szerepelnek (pl. `[H8686] [H8675]`)

## Igehely-formátum — döntés és előzmény

A Példabeszédek-feldolgozás **első körben** a forrás oldal saját angol könyvnév-formátumát
használta (`Proverbs 23:7`). Az 1Mózes-feldolgozás előkészítésekor kiderült, hogy ez
**inkonzisztens** a többi, közben elkészült publikus dataset formátumával
(`Karoli_1908.tsv`: magyar rövidítés; `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv`/
`TIPNR_kivonat.tsv`: STEPBible-natív) — enélkül a `Konyv_normalizalo_tabla.tsv`-n
keresztüli összekapcsolás megbízhatatlan lett volna.

**Végleges döntés (2026-08-24, felhasználói jóváhagyással): STEPBible-natív formátum
(`Gen.1.1`, `Pro.23.7`) mind a négy KJV/ASV-fájlban.** Ez egyezik a TAHOT/TAGNT/TIPNR
konvencióval, és a `Konyv_normalizalo_tabla.tsv` STEPBible-oszlopával közvetlenül,
szöveg-illesztéssel összeköthető. **A már korábban elkészült két Példabeszédek-fájl
(`KJV_Strongs_Proverbs.tsv`, `ASV_Strongs_Proverbs.tsv`) ennek megfelelően visszamenőleg
konvertálva lett** (`Proverbs N:V` → `Pro.N.V`, csak az Igehely-oszlop, minden más adat
változatlan).

## Forrás

- **KJV_Strongs minta-URL:** `https://studybible.info/KJV_Strongs/{Könyv}%20{N}` (pl. `Proverbs%20{N}`, `Genesis%20{N}`)
- **ASV_Strongs minta-URL:** `https://studybible.info/ASV_Strongs/{Könyv}%20{N}`
- **Letöltés dátuma:** 2026-08-24 (Példabeszédek), 2026-08-24 (1Mózes), 2026-08-31 (2Mózes)
- **Letöltő/feldolgozó módszer:** oldalankénti HTML-letöltés (`fetch`), majd szavankénti kinyerés a forrás `<span class="unit">` szerkezetéből (Strong-szám-hivatkozás + angol szórész; a `[H####]` formátumú, zárójeles hivatkozások morfológiai kódként lettek a megelőző szóhoz rendelve, nem önálló szóként számolva). A 2Mózes-feldolgozásnál (80 oldal: 40 fejezet × KJV+ASV) ugyanez a parszolási logika egy erre a célra írt Node.js-szkriptbe került (programozott letöltés + kinyerés a fenti `span.unit` szerkezet szerint), a korábbi két könyvnél alkalmazott, munkamenetenkénti kézi HTML-beolvasás helyett — a kinyerési szabályok (versszám-span vs. szó-span megkülönböztetése, zárójeles morfológiai kódok hozzárendelése) változatlanok maradtak.
- **Ismert parszolási buktató (a Példabeszédek-körben derült ki, az 1Mózes-feldolgozás ugyanezt a javított logikát használta):** a versszám-jelölő span class-neve `"ref english"`, a szó-span-oké `"english"` — ha a parszoló ezt nem különbözteti meg explicit, hanem pozíció alapján (pl. "hagyd ki az első egységet") próbálja kiszűrni a versszámot, minden vers **első valódi szava is kimarad**, mert a versszám-span technikailag sosem illeszkedik a szó-mintára. A helyes megoldás: ne legyen semmilyen "hagyd ki az elsőt" logika — a versszám-span emiatt magától sosem kerül be az eredménybe.

## `KJV_Strongs_teljes.tsv` — teljes KJV, Strong-címkés (F19, FELADATOK #19)

- **Állapot:** `importált, javaslat`. Forrás: eBible `eng-kjv_usfm.zip` (Public Domain), 66 kanonikus könyv, angol versszámozás, 349 308 sor, 31 099 címkés vers; a fejléc (`#` sorok) a proveniencia-sort és a mérést (`manual`, mért dátummal) tartalmazza.
- **Formátum:** mint a `KJV_Strongs_*.tsv` (`Igehely`, `Szósorszám`, `Strong-szám` vezető nulla nélkül, `Angol szó` — gyakran frázis —, `Morfológiai kód` üres). A zsoltárfelirat a 0. versen áll.
- **Hiányok:** `naplok/F19_hianyok.tsv` (3 címke nélküli KJV-vers: Mk 9:43, Lk 6:41, Lk 17:36; nem töltjük ki).
- **ASV:** az `ASV_Strongs_teljes.tsv` **nincs a repóban**, mert az eBible-ASV Strong-címkéi forráshibásak (H430/H776/H1/G746 = 0 előfordulás); l. DONTESEK DT19 és `naplok/ELLENOR_F19.md`.

## Licenc / eredet

- **Alapszöveg (KJV, ASV):** közkincs (public domain). A KJV brit "Crown copyright"-szabálya kizárólag a kereskedelmi nyomtatásra vonatkozik az Egyesült Királyságban; nem-kereskedelmi/kutatási felhasználásra és a világ többi részén szabadon felhasználható.
- **Héber Strong-számok (KJV-Strongs):** Bible Foundation (bf.org).
- **Görög Strong-számok (KJV-Strongs, ÚSZ-hez, itt nem releváns):** CrossWire KJV2003 projekt.
- **ASV Strong-taggelés:** a "Cross Word Project" (Wade Maxfield) munkája — a KJV-Strongs taggelésétől független forrás, ami valódi kereszt-ellenőrzést tesz lehetővé.

A pontos hivatkozásokért és a módszertani indoklásért lásd a döntési fájl
[PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md](../PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md)
4.8 (KJV-hidas módszer) és 4.9 (ASV kereszt-ellenőrzés) pontját.

## Validáció

**Példabeszédek — Pro.23.7** egyezést mutat a döntési fájl 4.8-as pontjában rögzített,
korábban kézzel ellenőrzött referenciával:

```
számítgatja = H8176 [H8804]
magában     = H5315
egyél       = H398  [H8798]
igyál       = H8354 [H8798]
mondja      = H559  [H8799]
akarattal   = H3820
```

Mind a hat szó (Strong-szám és morfológiai kód) számjegyre pontosan egyezik.

**1Mózes — Gen.17.5** (az Ábrám→Ábrahám névváltás verse) egyezést mutat a
`TIPNR_kivonat.tsv`-vel: a KJV/ASV Gen.17.5 sorai között megjelenik `H87` (Abram) és
`H85` (Abraham) — ugyanaz a két név, mint a TIPNR `H0087`/`H0085` bejegyzése ugyanerre a
versre (a nulla-kitöltés különbsége dokumentált fent, az "Igehely-formátum" szakasz
utáni bekezdésben).

Mindhárom könyvnél minden fejezet (Péld 1-31, 1Móz 1-50, 2Móz 1-40) sikeresen letöltve és
feldolgozva, 0 hibás formátumú Strong-szám és 0 üres kötelező mező egyik fájlban sem.

**2Mózes — Exo.3.14** ("ÉN VAGYOK AKI VAGYOK" / "I AM THAT I AM" — vö. a döntési fájl 4.9
pontjában dokumentált módszertan) egyezést mutat mindkét irányban: a KJV és ASV
Strong-sorozata szó szerint megegyezik egymással (`H430, H559, H4872, H1961, H1961, H559,
H559, H1121, H3478, H7971`), és minden előforduló Strong-szám megjelenik a
`TAHOT_kivonat.tsv` "2Móz 3:14" sorai között is (a TAHOT ott néhány további funkciószót és
egy harmadik `H1961`-előfordulást is tartalmaz, amit a KJV/ASV forrás egy szomszédos szóval
összevonva jelenít meg — ez a forrás szegmentálásának sajátossága, nem hiba).

**2Mózes — Exo.20.1, Exo.20.13, Exo.20.17** (Tízparancsolat, mintavételes ellenőrzés)
mindhárom versnél a KJV és ASV Strong-sorozata szó szerint megegyezik egymással, és minden
tartalmi (nem-funkciószó) Strong-szám megjelenik a `TAHOT_kivonat.tsv` megfelelő "2Móz 20:x"
soraiban.

**Egyik ellenőrzött 2Mózes-versnél sem merült fel KJV≠ASV eltérés** — nincs ⚠️ jelzésre váró
tétel ebből a validációs körből.

---

## Cremer nyers fájlok (archive.org, `cu31924098819406`) — CREMER_OCR_BRIEF.md O0.1

**Tétel:** Hermann Cremer, *Biblico-Theological Lexicon of New Testament Greek*, 3. angol
kiadás, Supplementtel. Archívum-azonosító: `cu31924098819406` (archive.org). A nyers fájlok
a `konkordancia/_nyers/cremer/` alatt vannak, **nem verziózva** (`.gitignore`) — kb. 1,85 GB.
A `CREMER_OCR_BRIEF.md` csak öt fájlt használ fel közülük (a többi az archive.org-letöltés
mellékterméke: epub, pdf, djvu, cubook.zip stb., ezeket a pipeline nem olvassa).

| Fájl | SHA-256 | Méret (bájt) |
|---|---|---|
| `cu31924098819406_hocr.html` | `9dbaf624795988e5116a210dcfaf774bf00b88daa183b5388a5ca232bdfe16af` | 75913833 |
| `cu31924098819406_page_numbers.json` | `e555123787eb7fa76c1320d6ba46992029a57d2abf016c1526eec9120c16d172` | 185706 |
| `cu31924098819406_jp2.zip` | `84b654268b1fa3f5ee7fcaae140289e72eeb9f69cb9160904d40866a0bcb6545` | 777703228 |
| `cu31924098819406_meta.xml` | `d1a13ac7506377373e4bccd6991ca272b1e10b61c37c90be6759497fb4c98e7e` | 2360 |
| `cu31924098819406_scandata.xml` | `12f48c6f2b38071d0c6dd6993701b2c722dacbc8c7a3cacbd94c0c41f3cfb953` | 329775 |

**Levél/oldal-indexelés (O0 ismételt mérés, 2026-09-24 — a CREMER_OCR_BRIEF.md §0-jával
mindenben egyezik):**

- 967 számozott levél (`cu31924098819406_page_numbers.json` `pages` tömbje, `leafNum` 1-967);
  a hOCR emellett tartalmaz egy `page_000000` elemet is (968 `ocr_page` összesen) — ez a
  page_numbers.json-ban nem szerepel (feltehetően a borító), a pipeline nem használja.
- A hOCR lapindexe (`page_NNNNNN`, 6 jegyű) és a jp2-zip fájlneve (`..._NNNN.jp2`, 4 jegyű)
  egyaránt közvetlenül a levélszám — nincs eltolás.
- 561 048 hOCR-szó, ebből 107 802 `x_wconf < 60`; görög karakter a szavakban: 0 — mindhárom
  szám pontosan egyezik a brief §0.4-ével.
- Levél↔oldal formula (§0.3) ellenőrizve a teljes `page_numbers.json`-on: 0 valódi eltérés;
  a 949 számozott oldalból 3 (oldal 590-592) **két** levélhez is tartozik (`+15` és `+18` ág
  egyaránt talál rá) — ez a nyomtatott kötet egy duplán számozott oldaltartománya, nem hiba,
  és pontosan ezért ad meg a brief két, egymást fedő oldaltartományt.
- Az ismert szócikkek (§0.5) és a két mutató kezdőlevele (§0.6) mind pontosan egyeznek a
  `page_numbers.json` `pageNumber` mezőjével.

## Cremer nyers fájlok (archive.org, `biblicotheologic00cremuoft`) — CREMER_OCR_BRIEF.md O0.6.1

**Tétel:** Hermann Cremer, *Biblico-Theological Lexicon of New Testament Greek*, 4. angol
kiadás, Supplementtel. Archívum-azonosító: `biblicotheologic00cremuoft` (archive.org,
Torontói Egyetem/Robarts könyvtár, 1895). A nyers fájlok a `konkordancia/_nyers/cremuoft/`
alatt vannak, **nem verziózva** (`.gitignore`). A `_meta.xml` szerint az OCR-motor
`tesseract 5.0.0-1-g862e`, `-l grc+eng` paraméterrel — ez a tétel a `cu31924098819406`-tal
ellentétben **görög nyelvi modellel** lett OCR-ezve.

Nincs önálló `_scandata.xml` fájl ennél a tételnél (csak a tömörített `scandata.zip`,
48 279 147 bájt) — az `_scandata.xml`-t a `scandata.zip` helyettesíti a lenti táblában.

| Fájl | SHA-256 | Méret (bájt) |
|---|---|---|
| `biblicotheologic00cremuoft_djvu.txt` | `f4736481b00a8af03273f7993c0292bfa546e4f2877a6db87261755561d7f3d1` | 3937823 |
| `biblicotheologic00cremuoft_djvu.xml` | `014a3beae0f95be68ef9412875ae46233c0d2c9fc259fe5c39f9fb0e03ceb6e7` | 43716007 |
| `biblicotheologic00cremuoft_chocr.html.gz` | `cb76779e7fd4fdf3dd88e537b0399e2b4b88fd39700700ffb7e407340e57df29` | 44516082 |
| `biblicotheologic00cremuoft_hocr.html` | `9fb53d0ddac63a78c0e1b6b8d171c1cc9c1ab984e9914047db77dc6e53615589` | 84419665 |
| `biblicotheologic00cremuoft_jp2.zip` | `bb5df74605d50b7ebc48f411cd9262991c4632028dd279f6a5d9963922dd7706` | 452094546 |
| `biblicotheologic00cremuoft_page_numbers.json` | `7c4118f2f52f93925192a807549860506f27a7e009170b2c43d64a7e2a79cc3e` | 164169 |
| `biblicotheologic00cremuoft_meta.xml` | `7db5579bf1c2bc25a9ee3572d00cf08e78ebcfe38e07e1fa2a9b0130e26061bc` | 2877 |
| `biblicotheologic00cremuoft_scandata.zip` (helyettesíti a `_scandata.xml`-t) | `0be5f7d9941ce4a7209e814da93ad6452f062cccbb21b75c80361c5b4ca20ecb` | 48279147 |

**Rétegazonosítás (O0.6.1c, mag: 20260925):** mind a négy réteg (`_djvu.txt`, `_djvu.xml`,
`_hocr.html`, `_chocr.html.gz`) pontosan ugyanannyi görög karaktert tartalmaz (634 103,
U+0370–03FF és U+1F00–1FFF). 100 véletlen görög token összevetésében a `_djvu.xml` és a
`_hocr.html` 100/100-ban egyezik a `_djvu.txt`-vel (karakterre azonos alak, NFC-normalizálva);
a `_chocr.html.gz` karakterenkénti (nem szóalapú) jelölése miatt a naiv címke-eltávolítás után
csak 4/100 — ez a fájl szerkezetéből adódik, nem valódi eltérés. **Választott koordinátás
réteg: `_hocr.html`** (szó-szintű bbox, azonos formátum, mint amit a `cremer_ocr_javit.py` a
`cu31924098819406`-nál használ).

**Levél↔oldal leképezés (O0.6.2a, `_page_numbers.json` alapján):**

| Levéltartomány | Oldaltartomány | Eltolás (level − oldal) |
|---|---|---|
| 14–890 | 2–878 | +12 |
| 891–957 | 876–942 | +15 |

A két szegmens határán (level 890→891) az oldalszám 878-ról 876-ra esik vissza — ez nem
hiba a leképezésben (mindkét szegmensen belül az eltolás szigorúan egyenletes), hanem a
nyomtatott kötet főszöveg/Supplement-átmenetének mellékelt, számozatlan lapjai miatti
+3 eltolás-ugrás. A görög szómutató a 929. levéltől (oldal 914), a héber mutató
(„V. HEBREW WORDS REFERRED TO") a 949. levéltől (oldal 934) kezdődik — mindkettő a
`+15` szegmensbe esik, és a lapon szereplő nyomtatott oldalszámmal (929→„INDEX … 915" a
930. levélen, illetve 949→„INDEX, 934") pontosan egyezik.

**Ismert szócikkek (§0.5) egyezése cross-edition ellenőrzésben (O0.6.2b) — ÁLLJ:** a hat
oldalszám közül négy egyezik (ἄβυσσος: oldal 2 → level 14; ἐπικατάρατος: oldal 109 →
level 121; ᾅδης első előfordulása: oldal 67 → level 79; ἐπικαλέω első előfordulása: oldal
335 → level 347), de **kettő nem** — ᾅδης második (`cu31924`-ben Supplement-beli)
előfordulása az oldal 610-nek megfelelő level 622-n nem `ᾅδης`-t, hanem a Συνάγω/Ἀγών
szócikkeket tartalmazza; ugyanígy ἐπικαλέω második előfordulása az oldal 742-nek megfelelő
level 754-n az Ἀναστατόω/Διχοστασία szócikkeknél jár. A `±1` szomszédos levélen sem
található egyik címszó sem. Magyarázat: a `cu31924098819406` kiadásban a Supplement kb. a
590. oldaltól kezdődik (a brief §0.3 offset-váltása), míg a `cremuoft`-ban a főszöveg
folyamatosan az 876. oldalig tart — a két kiadás Supplementje eltérő ponton kezdődik és
eltérő terjedelmű, ezért a Supplement-beli (második) címszó-előfordulások oldalszáma a két
kiadás közt nem transzferálható közvetlenül. A főszövegen belüli (első) előfordulások és a
mutatók kezdőlevele viszont pontosan egyeznek — a levél↔oldal leképezés önmagában
helyesnek igazolt a `+12` és a `+15` szegmensen belül is.

## `LXX_kivonat_*.tsv` — kivezetve (F42, DT-F33b, DT-F42f)

A 39 `LXX_kivonat_*.tsv` és a `LXX_kivonat_README.md` **kikerült a repóból** (`git rm`, F42.M5; a git-történetben az F42 előtti commitokban megmarad). Ok: a licence `tisztazatlan` volt (studybible.info, explicit licencnyilatkozat nincs), és a `LXX_OS` (lxx-morph + GreekWordList, CC BY 4.0) átveszi a helyét. Olvasói átálltak: `eszkozok/lekerdez.py` (`lxx-hid`), `eszkozok/lxx_bridge_egyezes.py`, `eszkozok/lexikon_general.py`, `eszkozok/kockazat_szures_18_tanulmany.py`; az `adat/datasetek.tsv` négy sora `LXX_OS`-re mutat. A régi↔új teljes eltéréslista: `naplok/FORRASKIVEZETES_M5_eltereslista.tsv` (`eszkozok/lxx_osszevetes.py`), a részletek a `naplok/FORRASKIVEZETES_zaras.md`-ben. Az `LXX_OS` szövegváltozat-választását és az Ezsd/Neh/Eszt besorolást a `LXX_OS/README.md` rögzíti. Új munka a régi kivonatra nem építhet.

## `LXX_versszintu_parok.tsv` — versszintű együtt-előfordulás (F05_SZOTAR_BRIEF.md S13)

**Generált** (`eszkozok/lxx_versszintu_import.py`, kézzel nem szerkesztendő).
A D28 hatókörébe tartozó 26 héber gerinc-token mindegyikének TAHOT-igehelyeit
veti össze a `LXX_OS/*.tsv`-vel: minden versben az ott előforduló, a
`adat/grammatikai_strongok.tsv` 31 G-sorával **grammatikailag szűrt**, egyedi
görög Strong-kódokkal — **versszintű együtt-előfordulás, nem szóillesztés**
(D14/D25 — a `LXX_OS` nem szóillesztett korpusz). Fejléc: `heber_strong
igehely lxx_igehely gorog_strong proveniencia`. Egy héber token egy verséhez
több sor tartozhat (egy-egy társ-görög Strong-kódonként); ha a szűrés után
egy versben nem marad tartalmi görög kód, egy sor kerül be üres
`gorog_strong` mezővel (a vers lefedettsége így is nyomon követhető).

Mért értékek (2026.09.28-i futtatás): 99 356 sor, 26 héber token, 729
TAHOT-igehely nem található meg a `LXX_OS`-ben (kihagyva — a `LXX_OS` nem
fedi le a teljes ÓSZ-t, l. `naplok/FORRAS_jelentes.md`). A módszertani
megerősítés (H7121 × G1941/G2564, a szűrés zajcsökkentő hatása) a
`naplok/SZOTAR_S0b_jelentes.md` 5. szakaszában.

**Licenc:** CC BY 4.0 (öröklődik a `LXX_OS`-től).

**Bemenet-azonosítás (K7, F05b, pontosítva a `fuggetlen-ellenor` 3.
köre után):** a tábla generálásához a szkript
(`eszkozok/lxx_versszintu_import.py`) három fájlt olvas be futásidőben:
`konkordancia/LXX_OS/*.tsv` (a versszintű MT–LXX-párosítás, SHA a
`konkordancia/LXX_OS/README.md`-ben, `verse_pairs.jsonl` alapján),
`konkordancia/TAHOT_kivonat.tsv` és `adat/grammatikai_strongok.tsv`. A
26 héber gerinc-token listája **nem** az `adat/elofordulasok.tsv`-ből
jön futásidőben — a szkript egy kódba égetett `HEBER_TOKENEK` konstans
(az S1.4-es futtatáskor `adat/elofordulasok.tsv`-ből lekérdezve, l. a
szkript fejcommentjét), amit a forrás nem olvas újra. Egyetlen,
egyértelmű "a bemenet" fájl nincs — a `LXX_OS` a tartalmilag
meghatározó forrás (ennek SHA-ja már dokumentált a saját README-jében),
a másik két tábla saját SEMA-bejegyzéssel (2.4, 2.15) rendelkezik,
külön SHA nélkül (nem verziózott külső letöltés, hanem a repó saját
adata).

## SZOTAR S1.4 importok — index (F05_SZOTAR_BRIEF.md, S1.6)

A szótári adatréteg 1. menetében (SZOTAR S1.4) importált 7 tábla mindegyike
saját, dedikált README-ben dokumentált (forrás-URL, SHA, licenc, sor- és
oszlopleírás) — ez a szakasz csak index, hogy melyik tábla melyik
dokumentumban van:

| Tábla | Dokumentáció | Import-szkript |
|---|---|---|
| `_nyers/tbesh/TBESH_konszolidalt.tsv` (gitignore-olt, helyben generált; F42) | `TBESH_TBESG_README.md` | `eszkozok/tbesh_konszolidalt_import.py` |
| `UBS_DBH_jelentesek.tsv`, `UBS_DBH_referenciak.tsv`, `UBS_DBH_anomaliak.tsv` | `SDBH_SDGNT_README.md` | `eszkozok/ubs_dbh_import.py` |
| `MCGED_teljes.tsv` | `lexikonok_nyers/README.md` | `eszkozok/mcged_import.py` |
| `BDB_etimologia_kezi_hatarok.tsv` | `BDB_teljes_unabridged_README.md` | `eszkozok/bdb_etim_hatarok_import.py` |
| `tW_szocikkek.tsv` | `tW_README.md` | `eszkozok/tw_import.py` |
| `LXX_versszintu_parok.tsv` | l. feljebb, ebben a fájlban | `eszkozok/lxx_versszintu_import.py` |

A generátor (`lexikon_general.py`/`torzscikk_general.py`) ezeket a
táblákat még nem olvassa — ez a SZOTAR S2 (2. menet) tétele.
`naplok/SZOTAR_S1_4_jelentes.md`: a teljes S1.4-jelentés, a mért sorszámok
és a döntésnapló-hivatkozások (D33).

## CC BY-SA 4.0 licencű datasetek — SDBH, SDGNT

A `SDBH_domenek.tsv`, a `SDGNT_domenek.tsv`, a `SDBH_SDGNT_domenfa.tsv` és a
`SDBH_SDGNT_anomaliak.tsv` a United Bible Societies nyílt szótáraiból származik,
**CC BY-SA 4.0** licenc alatt. A forrásmegjelölés kötelező, és a belőlük származó
adat — beleértve a motívumlexikon domén-hivatkozásait — **ugyanilyen licenc alá
esik**. Ez eltér a mappa többi, közkincs vagy CC BY 4.0 licencű forrásától.
Forrás-commit, ellenőrző összegek és a pontos forrásmegjelölés:
`SDBH_SDGNT_README.md`.


## `BSB_Strongs.tsv` — Berean Standard Bible, Strong-számozott angol híd (F16, FELADATOK #16)

- **Forrás:** https://github.com/BSB-publishing/bsb-data-output, `base/display/` (commit `a4a2c0558c26e0281ba4e3f0e5479398459e2183`, letöltve 2026.09.30).
- **Licenc:** CC0 1.0 (a repo README-je és ATTRIBUTION.md szerint a `base/display/`). A CC BY 4.0 `index-cc-by/` nem importált.
- **Tartalom:** 278 166 adatsor, 36 ÓSZ-könyv (1Móz–Ruth, 1Sám, 1Kir, 2Kir, 1Krón, 2Krón, Neh, Eszt, Jób, Zsolt, Péld, Préd, Én, Ézs, Jer, Sir, Ez, Hós, Jóel, Ámós, Abd, Jón, Mik, Náh, Hab, Sof, Hag, Zak, Mal). A küszöb alatt maradt 3 ÓSZ-könyv (2Sám 94,96%, Ezsd 94,64%, Dán 89,64%) **véglegesen nincs benne** (DONTESEK DT6 (a), (d) elutasítva 2026-10-06: a 95%-os küszöb nem változik): e könyvekre a `BSB_Strongs.tsv` **explicit üres eredmény**, nem hiányzó adat; a Strong-réteget a `TAHOT_kivonat.tsv` adja. Az újramérés: F41, `naplok/F41_nem_egyezo_versek.tsv` (az okuk nem a számozás; `okkategoria` szerint 2Sám: 3 `cimkezes`, 32 `egyeb`; Ezsd: 7 `arami`, 1 `cimkezes`, 7 `egyeb`; Dán: 25 `cimkezes`, 10 `arami`, 2 `egyeb`).
- **Formátum:** mint a `KJV_Strongs_*.tsv`: `Igehely` (STEP-alak, `Gen.1.1`), `Szósorszám` (a Strong-címkés szavaké), `Strong-szám`, `Angol szó`, `Morfológiai kód` (mindig üres), **`Angol szó állapota`** (F41, DT6 (e)), **`Számozás`** (F41). Strong-címke nélküli BSB-szavak nincsenek benne. **`Angol szó állapota`:** `forditva` (247 211 sor: az „Angol szó” nem üres) / `elhagyva` (30 955 sor, ebből 747 a Zsolt-sor: az „Angol szó” üres, mert a forrás-span `elided` jelzőt hordoz: a BSB angol szövegében nem megjelenő, de címkézett héber szó, pl. `H853`, `H996`) / `ures_jelzo_nelkul` (0 sor: üres „Angol szó” `elided` jelző nélkül); az „Angol szó” mezőbe helyőrző szöveg nem kerül; a `Szósorszám` az `elhagyva` sorokat is lépteti. A `bsb_import.py` az írás végén visszaolvassa a fájlt, és ellenőrzi az állapot-darabszámokat (a naplófejléc „szűrt sorok” számlálói mind a 66 könyvre vonatkoznak: szűrt = importált + nem importált). **`Számozás`** (DT-F41f, szigorítva F41.12 / DT-F41g; **versszintű WLC-összevetésből**, `eszkozok/fj2/wlc_versek.py` `vers_igazolt`): `mt` (260 284 sor, 20 184 vers: a WLC-vel versszinten egyértelműen megfeleltetett — a WLC azonos számú versének Strong-halmaza > 0,5 átfedéssel az Igehely-versben van, ez szigorúan jobb a WLC- és a BSB-környezet bármely másik versénél, nem hibrid részvers, és a szomszéd vers is illeszkedik; Strong-halmaz-egyezés, nem tartalmi egyezés) / `ellenorizetlen` (17 659 sor, 1 477 vers, 271 fejezet: a WLC-vel egyértelműen nem igazolt — többnyire formulás/ismétlődő vers döntetlenje, részvers vagy üres WLC-halmaz, nem „TAHOT-hibrid számozás”; **nem állítja, hogy a szám hibás**; fejezetenként `naplok/F41_wlc_versszam_ellenorzes.tsv`) / `kjv` (223 sor, 34 vers: a Jób 41, BSB-szám 41:1–34 = MT 40:25–41:26, a BSB/KJV-szám marad). A TAHOT-szám nem MT-forrás, a referencia a WLC; fejezetenként: `naplok/F41_wlc_versszam_ellenorzes.tsv`.
- **Lefedettség:** a küszöb (95%, igehely-szintű, TAHOT ⊆ BSB) és a könyvenkénti mérés: `naplok/F16_bsb_lefedettseg.tsv`; a szkript: `eszkozok/fj2/bsb_import.py`.
- **Versszámozás (F16.8, F16.11):** a BSB angol (KJV-) számozású; a `Zsolt` sorai kivétel: ezek **MT-számozásúak** (a TAHOT, a Károli-kulcs és a Macula számozása), mert az MT a zsoltárfeliratot saját versszámon számozza (63 zsoltárnál áll a felirat saját MT-versszámon: 58-nál +1, 4-nél (Zsolt 51, 52, 54, 60) +2 vers, plusz a Zsolt 13; a többi feliratos zsoltárnál, 53-nál, a felirat az MT 1. versének része). A BSB-vers → MT-vers megfeleltetés fejezetenként k = (a Károli-kulcs `igehely_mt` oszlopából az MT-fejezet utolsó versszáma) − (a BSB fejezet versszáma); a `Psa.3.3` tehát a BSB 3:2 verse (= Károli 3:3), nem a BSB 3:3. **Belső versosztás-eltérés:** ha a fejezetenként állandó k egy BSB-versnél nem igazolható (a BSB-vers a szomszédos MT-verssel egyezik, vagy az MT-vers két BSB-vers uniója), a fejezet **illesztetlen**, kimarad a mérésből és az importból. Jelenleg nincs ilyen fejezet: a **Zsolt 13** (BSB 2–4 = MT 3–5, BSB 5–6 = MT 6) **kézi kivétellel** szerepel (F71, DT-F41a; `KEZI_KIVETEL` a `bsb_import.py`-ban, `manual` proveniencia, `ok = kezi_kivetel_DT-F41a_manual` a `naplok/F41_bsb_megfeleltetes.tsv`-ben; az `illesztetlen` állapot `kezi`; a felirat → MT 1 és a BSB 13:1 → MT 2 a döntés szerinti megfeleltetés, de a display-JSON-ban nincs szövegük, ezért a `BSB_Strongs.tsv`-ben csak az MT 3–6 áll, 41 sor, `Számozás` = `mt`; a BSB 5 és 6 az MT 6-on egy mérési egység, a `Szósorszám` folytatódik; a nulladiff: `naplok/F71_nulladiff.txt`). Zsoltáronkénti táblázat és az illesztetlen lista: `naplok/F16_bsb_zsolt_megfeleltetes.tsv`. **Versszintű megfeleltetés (F41):** az import a Zsoltáron túl a többi könyvre is a BSB-vers → MT-vers megfeleltetést alkalmazza (Strong-illeszkedés, monoton igazítás, fejezetenkénti igazolás: `naplok/F41_bsb_megfeleltetes.tsv`; oszlopai `konyv, bsb_vers, mt_vers, modell, ok, tahot_vers, szamozas`), így átszámozott: 4Móz 29/30; 1Sám 23/24; 1Kir 22 (a BSB 22:43 két MT-versre osztva: 22:43 + 22:44); Ézs 9; Hós 11/12; Jón 1/2 (a Zsolt-sorok korábban). **A célszámozás az MT (WLC; a `Macula_heber_*.tsv` `ref`-je) — DT-F41b.** A megfeleltetés alapja a `TAHOT_kivonat.tsv` versszámozása, amely 25 ószövetségi könyvben nem azonos a WLC-vel (több helyen KJV-, máshol Károli-szerű); ezért az `Igehely` **nem mindenütt igazolt WLC-számozás**: a versszintű összevetés `naplok/F41_wlc_versszam_ellenorzes.tsv` (a 7. oszlop `Számozás` értékei `mt` / `kjv` / `ellenorizetlen`; kategóriák fejezetenként: `mt` 610, `reszben_mt` 243, `nem_igazolt` 29, `nincs_bsb_sor` 48; a szkript: `eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py`: konzisztencia-ellenőrzés (NEM független: ugyanaz a `vers_igazolt` a fájlból, a 7. oszlop minden versére) és külön, saját Macula-olvasású, Jaccard-alapú független ellenőrzés az `mt` versekre), a fejezet-max vizsgálat `naplok/F41_wlc_hatar_ellenorzes.tsv`. **A BSB/KJV-szám marad (nincs átszámozás):** a 4Móz 12/13, a Préd 11/12 és az Ézs 2/3 (itt a WLC szerint KJV = MT, a `TAHOT_kivonat` Károli-szerű: az átszámozás visszavonva, DT-F41f) és a Jób 38–41 (a `kjv` címke csak a tényleges KJV ≠ MT Jób 41-et jelöli: 223 sor, BSB 41:1–34 = MT 40:25–41:26; a Jób 40:1/3/6, 17 sor, `ellenorizetlen`; MT-re számozásuk külön N-tétel). **A `Számozás` darabszámai: `mt` 260 284 sor (20 184 vers), `kjv` 223 sor (34 vers), `ellenorizetlen` 17 659 sor (1 477 vers, 271 fejezet): az `ellenorizetlen` a WLC-vel egyértelműen nem igazolt (nagy része formulás döntetlen KJV = MT fejezetekben), nem „hibrid TAHOT-számozás”, és nem állítja, hogy a szám hibás; a kritérium paraméter-érzékenysége: `naplok/F41_parameter_erzekenyseg.md`.** A nulla-diff a main-nel: `naplok/F41_nulladiff.txt` (`eszkozok/fj2/bsb_nulladiff.py`).
- **Ismert hiány:** a forrás `base/display/` JSON-ja **117 fejezet 1. versének érdemi szövegét nem tartalmazza**: a 116 feliratos zsoltárét (pl. az MT 3:2 „Uram! mennyire megsokasodtak ellenségeim!…” a BSB 3:1; MT 18:2, 23:1, 51:3, 60:3) és a Zak 12:1-ét. A `base/text-only/` (CC0) állományban a versek megvannak. A felirat maga nem hiányzik: a BSB `d` szintű headingként adja (`headings.jsonl`: `before_v: 2`; a display-JSON `structure`-jében a „2” kulcson), csak a fejezet 1. versének szövege esik ki. Ezért a `BSB_Strongs.tsv`-ben ezek a versek nincsenek (MT-kulcsban a Zsoltár 183 hiányzó versszáma; a Zsolt 13 MT 1–2 verse (felirat, BSB 13:1) a kézi kivétel után is hiányzik, F71). Ez **nem az import hibája és nem a BSB szövegének hiánya**, hanem a display-JSON építéséé. A pótlás (DT6 (c)) nyitott: N-F71b — előbb a `base/hebrew-tsv/` licencének ellenőrzése.
- **ÚSZ:** a BSB-import az **Ószövetség miatt** készült; az újszövetségi görög réteg forrása a **Macula** (#87). A 27 ÚSZ-könyv **szándékosan maradt ki**, nem „küszöb alatti hiba”: a `bsb_import.py` az ÚSZ-könyvekre csak tájékoztató mérést végez (`eredmeny=USZ_KIHAGYVA`), és ÚSZ-sort nem írhat (a fájlban 0 `G`-sor van).
