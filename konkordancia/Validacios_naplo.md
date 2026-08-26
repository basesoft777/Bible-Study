# Validációs napló — Károli-Strong join-tábla

*Ennek a naplónak a célja, hogy minden jövőbeli validációs esemény (akár mintavételes,
akár teljes körű) ide kerüljön, ne szórtan a különböző README-kbe. Lásd
`Join_tabla_folyamat_magyarazat.md` a join-tábla építésének folyamatáról és a döntési
fájl 4.13 pontját az önellenőrzési mechanizmusról (KJV/ASV kereszt-ellenőrzés,
megbízhatósági jelölés).*

---

| Dátum | Igehely(ek) | Módszer | Eredmény | Megjegyzés |
|---|---|---|---|---|
| 2026.08.23-24 körül | Pro.23.1-9 | Felhasználói külső referenciával összevetve | 43/44 egyezés | 1 tudatos eltérés (23:2, Károli szabad fordítása) |
| 2026.08.23-24 körül | Act.1.1-4 | KJV/ASV kereszt-ellenőrzés | 19/19 szó, kritikai kiadás is egyezik | nincs szövegkritikai eltérés ezen a szakaszon |
| 2026.08.23-24 körül | Gen.1.2-4 | Felhasználói "régi Strong" referenciával összevetve | 12/14, majd 13/14 egyezés | 1 dokumentált kettős Strong-lehetőség (H2895/H2896) |
| 2026.08.24 | Gen.1-16 (a `Konnyu_ellenorzes_1-16_osszesito_v2.md` megerősített szavai) | Betöltés a `Karoli_Strong_kivonat.tsv` join-táblába: tartalom-alapú azonosítás + KJV/ASV kereszt-ellenőrzés (4.13 szabály), majd minden Károli-szó szigorú, teljes szóhatáros egyezés-ellenőrzése a `Karoli_1908.tsv` tényleges vers-szövegével szemben | 178 sor ténylegesen betöltve (Reliability: magas=177, közepes=1) | KJV/ASV kereszt-ellenőrzés: 177 sor "magas" (talált egyező KJV vagy ASV Strong-adat ugyanarra a versre/Strong-számra), 1 sor "közepes" (Gen.12.1 H1980 "Eredj" — nincs KJV/ASV Strong-adat erre a vers/Strong-párra); ebben a körben ÚJ KJV/ASV ELTÉRÉS nem került elő (a meglévő párosítás minden fellelt esetben egyezett). 7 sor kihagyva "TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ" jelöléssel (צֶלֶם, גַּן, עֵזֶר כְּנֶגְדּוֹ, צֵלָע, אִשָּׁה, נָחָשׁ, מִזְבֵּחַ), 2 sor kihagyva nyitott ELTÉRÉS miatt (1Móz 3:7-24 עֵרֻמִּם/H6174, 1Móz 4:1-24 הֶבֶל/H1892) — egyik kihagyott tétel sem került be a join-táblába, emberi döntésre várnak |
| 2026.08.26 | Teljes verzifikációs vizsgálat lezárása: 2094 ÓSZ + 4 ÚSZ zárójeles kettős hivatkozású verspár (A + B feladat) | A feladat: `TAHOT_kivonat.tsv` Károli-natív kulcsra állítása + minden zárójeles kettős hivatkozású ÓSZ-eset egyenkénti eldöntése. B feladat: `TAGNT_kivonat.tsv` Károli-natív kulcsra állítása a 4 ÚSZ-esetre + Károli-oldali adatminőségi gyorsaudit. C feladat: retroaktív ellenőrzés a motívumnaplóban + jelen lezáró bejegyzés. | Lásd részletesen lent | **Lezárva.** Nincs eldöntetlen (`NYITOTT`) eset. Az egyetlen nyitott kategória `ADATMINOSEGI_GYANU` (Károli-oldali, nem versifikációs okú). |

---

## 2026.08.26 — A teljes verzifikációs vizsgálat lezárása (A + B + C feladat)

Ezzel a bejegyzéssel lezárul a TAHOT/TAGNT-kivonatok Károli-natív kulcsra állítása és
a zárójeles kettős hivatkozású verspárok (2094 ÓSZ + 4 ÚSZ = 2098 eset) egyenkénti
eldöntése. Terjedelem: teljes ÓSZ (39 könyv) + a TAGNT-ban azonosított 4 ÚSZ-eset.

### A feladat eredménye (ÓSZ, TAHOT)

- `TAHOT_kivonat.tsv`: **435 724 → 468 233 sor** (Károli-natív `Igehely` kulcs, pl.
  `1Móz 1:1`, a korábbi STEPBible `Gen.1.1` formátum helyett).
- Minden zárójeles kettős hivatkozású ÓSZ-eset egyenként eldöntve és lezárva — **nincs
  eldöntetlen (`NYITOTT`) eset.**
- Az egyetlen továbbra is nyitva maradó kategória: **`ADATMINOSEGI_GYANU`**, kizárólag
  Ezékiel 20/21 vonatkozásában (`TAHOT_kivonat_nyitott_esetek.tsv`, 1069 sor) — ennek
  oka egy Károli-oldali gyanús összeolvadt vers, **nem** versifikációs eltérés a
  STEPBible és Károli könyv-/fejezet-/versbeosztása között.

### B feladat eredménye (ÚSZ, TAGNT + Károli-adatminőségi audit)

- `TAGNT_kivonat.tsv`: mind a 4 ÚSZ-eset Károli-natív kulcsra állítva és lezárva
  (`Verzifikacios_elteres_tabla.tsv`: Róm 3:26, ApCsel 13:39, Mk 12:14, ApCsel 19:40 —
  mindegyik `IGAZOLVA`).
- Károli-oldali adatminőségi gyorsaudit (`Karoli_adatminosegi_anomaliak.tsv`):
  **7 talált anomália**, mind `ELLENORZESRE_VAR` státusszal: Ez 20:44, Jób 41:25,
  Préd 9:18, 2Móz 35:35, Dán 3:30, Én 5:16, Hós 14:9. Ezek a Károli-szöveg oldalán
  feltételezett összeolvadt/áthelyeződött versek, nem a STEPBible-adat hibái —
  emberi ellenőrzésre várnak, önálló feladat tárgyát képezik.

### C feladat — Retroaktív ellenőrzés a `PaRDeS_motivumok_v43.md` motívumnaplóban

A motívumnaplóban rögzített, korábban (a hiányos kivonat idején) külső forrásból
igazolt három állítás ellenőrzése az immár javított, Károli-natív kulcsú
`TAHOT_kivonat.tsv` alapján:

| Igehely | Napló állítása | Ellenőrzés eredménye |
|---|---|---|
| **Zsolt 140:12** | H6679 (cúd, "vadászni") gyök jelenléte | **EGYEZIK.** `H6679 / יְצוּדֶ֗ / ye.tzu.De. / צוּד / to hunt / let it hunt` sorban pontosan megtalálható. |
| **Zsolt 88:11** | רְפָאִים szó jelenléte (a "Rafeusok/óriás-népek" lezárt tematikus tanulmány alapja) | **EGYEZIK.** `H7496 / רְ֝פָאִ֗ים / re.fa.'Im / רְפָאִים / shade / [the] shades` sorban pontosan megtalálható. **A lezárt tematikus tanulmány nem igényel újranyitást** — az alap, amire épült, stabil marad az immár teljes kivonatban is. |
| **1Sám 24:11** | H6679 (cúd) gyök jelenléte, "Károli eltérő szót választ" megjegyzéssel | **ELTÉR.** 1Sám 24:11 sorai között nincs H6679 vagy צוד gyökű szó. A szemantikailag legközelebbi szó ("lying in wait" / "ambush") a **következő** versben, **1Sám 24:12**-ben található, **H6658** (`צָדָה`) Strong-számmal — ez a H6679 (`צוּד`) rokon, de **különböző** Strong-bejegyzésű gyöke. A napló pontos állítása (H6679, 24:11) tehát két ponton sem igazolható szó szerint: (a) a szó a következő versben van, (b) a Strong-szám egy rokon, de eltérő gyöké. A motívum lényege (egy "vadászni/leselkedni" jelentésű gyök jelenléte, amit Károli más szóval — "leselkedel" — ad vissza) fennáll, de a napló-bejegyzés pontosítást igényel: helyes hivatkozás **1Sám 24:12, H6658**. **A motívumnapló módosítása nem történt meg** (ez a feladat kizárólag ellenőrzés, nem javítás) — a pontosítást a napló kezelője végezze el, ha szükségesnek ítéli. |

### Nyitott, alacsony prioritású tétel: LXX (Septuaginta) bevonása — fázisolt terv

A jelenlegi héber/Károli-illesztés (A+B+C) lezárása után, **jövőbeli, önálló
feladatként** érdemes megvizsgálni a Septuaginta bevonását. Fázisolt terv:

- **0. fázis (elvégezve ebben a körben — dokumentálás, nem adatintegráció):** lásd
  `TAHOT_TAGNT_README.md` "LXX (Septuaginta) — jelenlegi lefedettség és jövőbeli
  bevonás" szakaszát. Röviden: (a) a TAHOT már most tartalmaz korlátozott
  LXX-apparátust a STEPBible dokumentációja szerint ("LXX additions included as
  Hebrew from BHS/BHK apparatus"); (b) a már letöltött `TFLSJ` és `TBESG` lexikonok
  eleve LXX-kompatibilisek (NT+LXX+Apokrif közös Strong-rendszer), tehát a szótári
  háttér egy jövőbeli integrációhoz már rendelkezésre áll.
- **1. fázis (jövőbeli):** forrás-figyelés. A STEPBible saját `TAGOT` (Translators
  Amalgamated Greek OT) adatkészlete illeszkedne legjobban a meglévő
  TAHOT/TAGNT-infrastruktúrához, de a STEPBible dokumentációja szerint még készül
  és/vagy ellenőrzés alatt áll, és jelenleg nem található fájlként a repóban —
  időnként érdemes ellenőrizni, elérhetővé vált-e. Alternatíva: CATSS morfológiailag
  taggelt Rahlfs-LXX (LXXM), szabadon elérhető akadémiai szabvány, STEPBible-től
  függetlenül.
- **2. fázis (jövőbeli):** LXX-specifikus versifikációs feltérképezés — az LXX saját
  könyv-/fejezetbeosztást használ (pl. Zsoltárok eltolódása a 9-10. zsoltártól,
  Jeremiás eltérő szerkezete/sorrendje). A `Versification/TVTMS...` fájl neve
  explicit tartalmazza a görögöt is ("Eng+Heb+Lat+Grk+Others") — ezt érdemes lesz
  elsőként megnézni, mennyire fedi már le az LXX-eltéréseket.
- **3. fázis (jövőbeli):** bekötés korlátozott hatókörrel — mivel Károli
  maszoréta-alapú fordítás, az LXX nem váltaná ki a TAHOT-ot mint elsődleges kulcsot,
  hanem kiegészítő rétegként kapcsolódna, elsősorban az ismert ÓSZ→ÚSZ idézetek
  helyén (a "3/b Kereszthivatkozási réteg" Remez-munkájához) — jóval szűkebb
  hatókör, mint a teljes ÓSZ 2094 esete.

Csak a 0. fázis készült el ebben a körben; az 1-3. fázis csak jövőbeli, önálló
feladatként jelölve, a jelen A+B+C lezárás után.

---

## 2026.08.26 (kiegészítés) — LXX-fázisolt terv frissítése: forrás azonosítva

A korábban rögzített LXX-fázisolt terv "1. fázisa" (forrás-figyelés, STEPBible TAGOT-ra
várva) elavulttá vált: a studybible.info (már használt forrás KJV_Strongs/ASV_Strongs
lekérésére) közvetlenül kínál Strong-taggelt LXX-szöveget könyvenkénti oldalakon
(`LXX_WH` és `ABP_GRK` verziók). Ellenőrizve, hogy a formátum megfelelő granularitású
(szavankénti Strong-szám + morfológiai kód). A 3. fázis (tényleges LXX-integráció)
ezért nem függ többé a TAGOT megjelenésétől — a 2. fázis (TVTMS-alapú versificaiós
térképezés) lezárása után közvetlenül indítható ezzel a forrással.

A fázisolt terv többi eleme (2. fázis: versificaiós térképezés a TVTMS alapján; 3.
fázis: korlátozott hatókörű bekötés, elsősorban az ismert ÓSZ→ÚSZ idézetek helyén)
változatlan.

---

## 2026.08.26 (kiegészítés) — LXX-fázis 2 lezárása: TVTMS-alapú versificaiós térkép

Elvégezve a `Feladat D` (LXX-fázis 2), önálló `lxx-fazis2-versificacios-terkep`
branch-en, main-ből ágazva (nincs merge-elve, nincs push-olva). Előfeltétel-ellenőrzés
(A+B+C lezárva, `TAHOT_kivonat.tsv` Károli-natív kulcsú, 468 233 sor) sikeres volt.

**Forrás:** a STEPBible-Data repo `Versification/TVTMS - Translators Versification
Traditions...` fájlja (letöltve a munkakönyvtárba, `master` branch, ~5,6 MB — a nyers
fájl **nem** került be a repóba, a projekt gyakorlatának megfelelően).

**Módszertani pontosítás a validáció során (felhasználói döntéssel lezárva):** az
eredeti terv a `SourceType` mezőre szűrt volna (Greek/Greek2/GreekUndivided). A
validációs próba (Gen.32:1) kimutatta, hogy ez a szűrés hibás eredményt adna — a
tényleges "Renumber verse" akció gyakran **Hebrew** `SourceType` alatt szerepel (a
görög/latin nézőpontból ugyanez a jelenség "Keep verse", mert onnan nézve nincs
változás). A végleges logika ehelyett az **Ancient Versions annotációra** szűr (van-e
`Greek=` érték a sorban, függetlenül a `SourceType`-tól), a sorokat a Hebrew/Latin/Greek
hármas (könyv + hármas) alapján csoportosítja, és csoportonként a legspecifikusabb
Action-t veszi (Concatenation/MergedNext/MergedPrev > Renumber verse > egyéb — az
utóbbi csoportok, pl. csak "Keep verse", kimaradnak a térképből, mert nem jeleznek
valódi eltérést). Ezzel a logikával mindhárom validációs eset (Gen.32:1, Gen.3:1,
Gen.6:1) pontosan a várt eredményt adta, beleértve a `Karoli_egyezik_hol` mező
"Latin,Gorog" értékét Gen.32:1-re.

**1-2. típus (Renumber, Concatenation/Merge) — `LXX_versificacios_terkep.tsv`:**
5426 sor (a teljes 39 könyves TAHOT-hatókör vizsgálva; ebből 34 könyvben található
tényleges eltérés — Ruth, Ezsdrás, Siralmak, Abdiás és Habakuk 0 sorral szerepel,
mert nincs bennük TVTMS-dokumentált görög versificaiós eltérés). Ebből:
- 5091 Renumber, 335 Concatenation/Merge.
- `Karoli_egyezik_hol` eloszlás: 1503 Heber, 1211 Heber+Latin, 426 Latin+Gorog, 361
  Latin, 216 Heber+Gorog, 165 Heber+Latin+Gorog, 7 Gorog — összesen **3889 sor**
  automatikusan, validáltan Károli-illesztve (nem feltételezve — a `TAHOT_kivonat.tsv`
  tényleges kulcsai ellen ellenőrizve).
- **1233 sor `EGYIK_SEM`** — a Károli-vers egyik oszloppal sem egyezik pontosan (pl.
  a legtöbb Zsoltár-eset, ahol Károli saját, negyedik számozási hagyományt követ a
  felirat-versek miatt; és Dán 4 egyes versei). Ezek nem hibák, hanem Károli önálló
  hagyományának dokumentált nyomai — jövőbeli vizsgálat tárgyai.
- **304 sor `ELLENORZESRE_VAR`** — a becsült Károli-kulcs nem található meg a
  `TAHOT_kivonat.tsv`-ben. Szúrópróba alapján ez nagyrészt egybevág a már ismert
  esetekkel: Ez 20/21 (a korábban dokumentált `ADATMINOSEGI_GYANU` Károli-oldali
  gyanú), 1Sám 23:29/24:1 (a korábban dokumentált vadász-gyök motívum kontextusa),
  valamint apokrif/LXX-only betoldások (Eszt 13, Dán 3 "Három ifjú éneke"), amelyeknek
  Károliban (protestáns kánon) nincs megfelelőjük.

**3-4. típus (LongVerse, LongVerseDuplicated) — `LXX_tobblet_szakaszok.tsv`:**
**Fontos eltérés a tervezetthez képest:** a LongVerse/LongVerseDuplicated jelenségek
a TVTMS fájl **Condensed szakaszában** találhatók (`#DataStart(Condensed)` —
`#DataEnd(Condensed)`), **nem** az Expanded szakaszban, ahol az Expanded szakasz 0
ilyen sort tartalmaz. A Condensed szakasz eltérő oszlopszerkezetű ($Szakasz + English
KJV/Hebrew/Latin/Greek/egyéb oszlopok, szakaszonkénti fejléccel), ezért külön
feldolgozó logikát igényelt. Eredmény: **106 sor**, mind "kutatási jelölt" státusszal
(`LongVerseDuplicated`: 36, `LongVerseElsewhere`: 32, `LongVerse/LVExtra`: 15,
`LongVerseElsewhereJoin`: 13, `LongVerse/LVElsewhere`: 7, `LongVerse/LVDuplicated`: 3).
Túlnyomó többségük (83/106) a 2Móz 25-40 (sátor/templom-berendezés, LXX-Vulgata eltérő
sorrend) és 1Kir 2-7 (LXX duplikált betoldások) szakaszokból. Nem lettek lezárva —
jövőbeli, önálló szövegkritikai/teológiai vizsgálat kiindulópontjai.

**Ez a térkép még nem tartalmaz tényleges LXX-lexikai adatot** — csak
versifikációs (verscím/verszám) megfeleltetést. A tényleges LXX-szó/Strong-adat
bekötése (3. fázis) a `studybible.info/LXX_WH` vagy `.../ABP_GRK` forrás alapján
lesz elvégezhető (lásd a 2026.08.26-i korábbi kiegészítést a forrás azonosításáról),
és közvetlenül erre a versificaiós térképre épülhet.

**Fájlok (a `lxx-fazis2-versificacios-terkep` branch-en, nincs commitolva még):**
`konkordancia/LXX_versificacios_terkep.tsv` (5426 sor + fejléc),
`konkordancia/LXX_tobblet_szakaszok.tsv` (106 sor + fejléc).
