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

## CC BY-SA 4.0 licencű datasetek — SDBH, SDGNT

A `SDBH_domenek.tsv`, a `SDGNT_domenek.tsv`, a `SDBH_SDGNT_domenfa.tsv` és a
`SDBH_SDGNT_anomaliak.tsv` a United Bible Societies nyílt szótáraiból származik,
**CC BY-SA 4.0** licenc alatt. A forrásmegjelölés kötelező, és a belőlük származó
adat — beleértve a motívumlexikon domén-hivatkozásait — **ugyanilyen licenc alá
esik**. Ez eltér a mappa többi, közkincs vagy CC BY 4.0 licencű forrásától.
Forrás-commit, ellenőrző összegek és a pontos forrásmegjelölés:
`SDBH_SDGNT_README.md`.
