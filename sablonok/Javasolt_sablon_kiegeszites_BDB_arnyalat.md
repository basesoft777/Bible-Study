# Javasolt sablon-kiegészítés — BDB-árnyalat integrálása a PaRDeS-tanulmányokba

*v5 — 2026.09.03 (Új 2/f lépés a technikasorban: rögzült szópár
együttes-előfordulás ellenőrzése — amikor a study szövege két szót
rendszeresen együtt említ [pl. תהו/בהו], külön kereséssel meg kell
állapítani, hányszor fordul elő a PÁR együtt a teljes Szentírásban,
nem csak külön-külön a két szó; konkrét precedens: 1Móz 1:2 תהו/בהו
párja mindössze 3 igehelyen fordul elő együtt [1Móz 1:2, Jer 4:23,
Ézs 34:11], ez korábban nem került elő, mert a 2/c lépés csak egyetlen
szó önálló előfordulását nézi, nem szópárokét)*
*v4 — 2026.09.03 (A "13-as kör" gating-mechanizmus ELVETVE: a 2/a-2/e
technikasor mostantól minden, a bővített sablon saját triázsán átment
kulcsszóra lefut, külön motívum-lista alapú szűrés nélkül — a 8. pont
történeti feljegyzésként megmarad, de többé nem éles protokoll-elem; az
1. pont 2. lépése és a 11. pont 1. tétele ennek megfelelően frissítve)*
*v3 — 2026.09.03 (A 2/e LXX-híd lépés kiegészítve explicit hatókör-
záradékkal: a `LXX_kivonat_Genezis.tsv` jelenleg KIZÁRÓLAG a Genezis
könyvet fedi le [1-50. fejezet] — Genezisen kívüli tanulmányoknál a 2/e
lépés görög oldala nem futtatható le a jelenlegi forrásokkal, csak a
héber gyök-ellenőrzés; ezt korábban csak a 3. pont forrás-hierarchia
táblázata jelezte, a technikasor lépésénél nem)*
*v2 — 2026.09.03. Teljes szerkezeti átdolgozás: a 2/a-2/e technikasor
egységes lánccá szervezve (a 2026.09.03-i két study-audit
[1Moz_7v1-24, 1Moz_12v1-20] gyakorlatából kodifikálva), a
forrás-hivatkozási fegyelem általános szabállyá emelve, a 7. szakasz
("Lexikai audit — módszertani napló") kötelező sablon-elemmé téve
minden jövőbeli auditált tanulmányhoz, a ritkaság-küszöb egységesítve.
Az előző verzió (v1, rekonstruált 2026.09.02) tartalma megőrizve,
kiegészítve.*

---

## 0. Cél

Ez a dokumentum írja le, **hogyan** kerüljön be BDB/TBESH-alapú lexikai
árnyalat-adat egy PaRDeS-tanulmányba (alap vagy bővített sablon szerint),
két alkalmazási szinten:
1. **Per-study sense-választás** — egy adott vers egy adott szavának melyik
   BDB-jelentésárnyalata releváns az adott kontextusban
2. **Motívum-lexikon "Lexikai adatlap"** — a motívum-lexikon architektúra
   része (l. a mock-up-kör eredményei)

---

## 1. Determinisztikus protokoll v2 (MINDEN MÁS ELŐFELTÉTELE)

```
BDB/TBESH-ELLENŐRZÉSI PROTOKOLL v2 — minden triázson átment szónál,
KIVÉTEL NÉLKÜL, ebben a sorrendben:

1. `grep "^H####" konkordancia/TBESH.txt` (héber) vagy
   `grep "^G####" konkordancia/TBESG.txt` (görög) — MINDIG lefut,
   MINDEN triázson átment szónál.

2. A teljes 2/a-2/e technikasor MINDEN, a bővített sablon saját
   triázsán (`2_PaRDeS_bovitett_sablon.md`, 2. pont, 6 kritérium) átment
   kulcsszóra kötelezően lefut — nincs további szűrés vagy
   kör-tagság-vizsgálat. (2026.09.03-ig egy külön "13-as kör" lista
   szűkítette volna ezt a kört, de a gyakorlat — l. 1Moz_7v1-24 és
   1Moz_12v1-20 auditja — azt mutatta, hogy a triázson átment szavak
   száma önmagában elég szűk halmaz ahhoz, hogy külön kör-lista nélkül
   is kezelhető legyen; a "13-as kör" koncepció emiatt elvetve, l. 8.
   pont.) Ebben a sorrendben:

   2/a — SZÓ-SZINTŰ BDB-ELLENŐRZÉS
   `grep "^H####" konkordancia/BDB_teljes_unabridged.tsv`
   (elsődleges teljes forrás — l. 3. pont, forrás-hierarchia).
   HA a BDB_teljes_unabridged.tsv-ben SEM ad tartalmilag érdemi
   találatot (rendkívül ritka eset, mivel ez a forrás 8090/8090
   bejegyzésnél tartalmaz szöveget) → EXPLICIT gap-jelzés a
   ⚡-jegyzetben: "Determinisztikus forrásból etimológiai/
   jelentésárnyalati adat nem elérhető." NEM pótolható web_search-csel
   vagy Claude általános tudásából.

   2/b — ORIGIN-LÁNC KÖVETÉSE
   Nézd meg a fejszó Strong-számának sorát a `Strong_szotar.tsv`
   "Gyök/Származtatás" oszlopában (NEM a BDB-szócikkben — a BDB
   szabadszöveges bejegyzései NEM tartalmaznak strukturált "Origin:"
   jelölést). Ha a mező "from H####", "corresponding to H####",
   "variation of H####" vagy hasonló, másik Strong-számra mutató
   mintát tartalmaz, ELLENŐRIZD a hivatkozott Strong-szám szócikkét is
   a TBESH.txt / BDB_teljes_unabridged.tsv-ben, mielőtt a fejszó
   szócikkét "teljesnek" tekintenéd. Ha a hivatkozott Strong-szám
   szócikke maga is további hivatkozást tartalmaz, a láncot addig
   KÖVESD, amíg tartalmilag érdemi adatot nem talál, vagy a lánc nem
   zárul (pl. "primitive root", "unused root"). Minden lánc-lépésnél
   MEGNEVEZVE, honnan jön az adat (l. 2. pont, forrás-hivatkozási
   fegyelem) — konkrét precedens (2026.09.02-03): a תְּהוֹם/H8415
   esetén a `Strong_szotar.tsv` "from H1949" bejegyzése a הום-gyök
   szócikkére mutat; a hivatkozás forrása a Strong-szótár, NEM a BDB
   saját szövege.

   2/c — TELJES-ELŐFORDULÁS FELTÁRÁS (ÚJ, 2026.09.03)
   `grep "Strong-szám" konkordancia/TAHOT_kivonat.tsv` (héber) vagy
   `konkordancia/TAGNT_kivonat.tsv` (görög) — a szó ÖSSZES ó- vagy
   újszövetségi előfordulásának kigyűjtése. NEM kell minden
   előfordulást tárgyalni a study-ban, de a keresést MINDIG le kell
   futtatni, hogy legyen alapja eldönteni, van-e kiaknázatlan, a study
   szempontjából releváns párhuzam. Konkrét precedens (2026.09.03,
   1Moz_7v1-24): a נִשְׁמַת רוּחַ חַיִּים (7:22) ↔ נִשְׁמַת חַיִּים (2:7)
   dekreáció-párhuzam pontosan ebből a lépésből derült ki — a BDB
   H5397-szócikk saját maga veti össze a két igehelyet.

   2/d — KERESZTHIVATKOZÁS/MOTÍVUM-AZONOSSÁG-ELLENŐRZÉS
   L. részletesen a 6-7. pontban (a TBESH/TBESG pontos rendeltetése és
   a kétfunkciós triázs szétválasztása) — annak eldöntése, hogy egy már
   meglévő kapcsolat mögött azonos BDB-jelentésárnyalat áll-e, vagy
   csak felszíni szóazonosság.

   2/e — LXX-HÍD (ÚJ, 2026.09.03, a Róm 9:27-eset alapján)
   Amikor egy újszövetségi kereszthivatkozásnál a Strong-szám-szintű
   metszet üres a genezisi/ószövetségi vers és az idézett újszövetségi
   vers görög szókészlete között, EZ ÖNMAGÁBAN NEM ELÉG a kapcsolat
   "tematikusnak" (nem lexikainak) minősítéséhez. KÖTELEZŐ külön
   ellenőrizni:
     (a) a héber gyök-szintű kapcsolatot (a study saját nyelvi verse és
         az idézett ÓSZ-hely azonos triliterális gyöke, akkor is, ha
         eltérő szófajban/alakban jelenik meg);
     (b) a görög gyök-szintű kapcsolatot (LXX-fordítás a genezisi/ÓSZ
         versben vs. az ÚSZ-idézet szava, akkor is, ha eltérő
         igekötővel/összetétellel).
   Csak ha SEM a héber, SEM a görög gyök-szinten nincs kapcsolat,
   minősíthető a kapcsolat "tematikus, nem lexikai"-nak. Konkrét
   precedens (2026.09.03, 1Moz_7v1-24): a Róm 9:27 piros zászló
   (üres Strong-szám-szintű metszet) ellenére VALÓDI gyök-szintű
   kapcsolatot mutatott mindkét nyelvi rétegben (héber שאר, görög
   λείπω-család) — a "tematikus" minősítés pontatlan lett volna.

   **Hatókör-korlátozás (2026.09.03):** a görög oldali ellenőrzéshez
   használt `LXX_kivonat_Genezis.tsv` JELENLEG KIZÁRÓLAG a Genezis
   könyvet fedi le (1-50. fejezet). Genezisen kívüli tanulmányoknál
   (pl. 2Mózes és utána) a 2/e lépés görög fele NEM futtatható le a
   jelenlegi forrásokkal — ilyenkor csak a héber gyök-ellenőrzés
   (Strong_szotar.tsv/BDB alapján) végezhető el, és ezt a korlátozást
   a study saját ⚡-jegyzetében vagy kereszthivatkozás-naplójában
   EXPLICIT jelezni kell ("LXX-híd görög oldala nem ellenőrizhető,
   mivel a jelenlegi LXX-forrás csak Genezisre terjed ki"), nem szabad
   hallgatólagosan kihagyni.

   2/f — RÖGZÜLT SZÓPÁR EGYÜTTES-ELŐFORDULÁS ELLENŐRZÉSE (ÚJ, 2026.09.03)
   Amikor a study szövege egy RÖGZÜLT, hendiadysz-szerű szópárt
   azonosít (két szó, amelyek a study saját passzusában együtt,
   egymás mellett jelennek meg, pl. תהו/בהו "tohu vabohu" 1Móz 1:2-ben),
   külön keresést kell futtatni: mindkét szó ÖSSZES előfordulását
   lekérdezni a TAHOT_kivonat.tsv-ből (vagy TAGNT_kivonat.tsv-ből görög
   esetén), majd a két előfordulás-listát metszeni — mely versekben
   szerepel MINDKETTŐ EGYÜTT. Ez különbözik a 2/c lépéstől (ami egy-egy
   szó önálló előfordulását nézi elszigetelten) — itt kifejezetten a PÁR
   együttes előfordulása a keresés tárgya. Ha a metszet szűk (kevés
   igehely), ez önmagában erős, konkordancia-alapú lexikai kapocs a
   study saját passzusa és a metszetben található más igehelyek között
   — akkor is, ha ezt korábban semmilyen kommentár vagy más forrás nem
   jelezte. Aktiválási feltétel: ez a lépés csak akkor fut, ha a study
   szövege (vagy egy korábbi 2/a-2/e lépés) MAGA már azonosít egy ilyen
   rögzült szópárt — nem kell minden lehetséges szópár-kombinációra
   lefuttatni, ami kombinatorikusan kezelhetetlen volna. Konkrét
   precedens: 1Móz 1:2 תהו/בהו párja mindössze 3 igehelyen fordul elő
   együtt a teljes Szentírásban (1Móz 1:2, Jer 4:23, Ézs 34:11) — mindhárom
   ítélet/dekreáció-kontextusban.

3. Minden ⚡-jegyzet FELTÜNTETI, melyik lépés(ek) futottak le, és melyik
   fájlból (TBESH.txt / BDB_teljes_unabridged.tsv / Strong_szotar.tsv /
   TAHOT_kivonat.tsv / TAGNT_kivonat.tsv / LXX_kivonat_Genezis.tsv).

4. TILOS korábbi, más kontextusban/munkamenetben talált adatot
   "visszamásolni" ellenőrzés nélkül — minden ⚡-jegyzet a SAJÁT, ebben
   a körben lefuttatott 1–2/e lépésből származik.
```

---

## 2. Forrás-hivatkozási fegyelem (ÁLTALÁNOS SZABÁLY, 2026.09.03)

Minden forrás-eredetű állításnál **kötelező** külön nevezni:
- **(a)** mi jött **közvetlenül** a saját repó adott fájljából (pl.
  `BDB_teljes_unabridged.tsv`, `Strong_szotar.tsv`, `TAHOT_kivonat.tsv`,
  `TAGNT_kivonat.tsv`, `LXX_kivonat_Genezis.tsv`);
- **(b)** mi jött egy **külső** forrásból, amit csak **tartalmilag**
  kereszt-ellenőriztünk a saját repónkkal (pl. StudyLight.org, más
  weboldal, korábbi munkamenetben talált anyag).

**(a) és (b) összemosása tilos**, még akkor is, ha a tartalom helyesnek
bizonyul.

**Precedens (2026.09.03):** a תְּהוֹם (H8415) "from H1949" hivatkozás
forrása valójában a `Strong_szotar.tsv` "Gyök/Származtatás" oszlopa —
korábban tévesen lett a BDB saját szövegének attribuálva
(`BDB_teljes_unabridged_README.md` és e dokumentum korábbi verziója).
A tartalmi ellenőrzés (H1949 = "morajlás") helyesnek bizonyult, csak a
forrás-megnevezés volt pontatlan — ez éppen ezért nehezen észrevehető
hiba: a hibás forrás-attribúció önmagában nem befolyásolja a végkövetkeztetés
helyességét, csak a nyomon-követhetőséget és a jövőbeli automatizálhatóságot
veszélyezteti.

---

## 3. Forrás-hierarchia

| Forrás | Szerep | Megbízhatóság | Megjegyzés |
|---|---|---|---|
| `TBESH.txt` / `TBESG.txt` (repóban) | 1. lépés, mindig fut | Csak sense-hierarchia, gyök-etimológia nélkül | STEPBible CC BY 4.0 |
| `BDB_teljes_unabridged.tsv` (bevezetve) | **Elsődleges teljes forrás**, 2/a lépés | 8090/8090 bejegyzés, 0 üres | Közkincs (Tim Morton/Eliran Wong) |
| `Strong_szotar.tsv` (repóban) | **Origin-lánc forrása** — minden szónál ellenőrzendő a 2/b lépésben | openscriptures, CC BY 4.0 | A "Gyök/Származtatás" oszlop tartalmazza a más Strong-számra mutató hivatkozásokat (pl. "from H1949") — ez a Strong's Concise Dictionary tartalma, NEM a BDB-é; a BDB-fájlok maguk nem tartalmaznak strukturált gyök-hivatkozást |
| `TAHOT_kivonat.tsv` / `TAGNT_kivonat.tsv` (repóban) | **Teljes-előfordulás forrása**, 2/c lépés | 468 232 / teljes ÚSZ sor | STEPBible CC BY 4.0 |
| `LXX_kivonat_Genezis.tsv` (repóban) | **LXX-híd forrása**, 2/e lépés | Csak Genezis-pilot hatókör | STEPBible CC BY 4.0 |
| openscriptures `BrownDriverBriggs.xml`+`LexicalIndex.xml` | Másodlagos/tartalék, csak ha az elsődleges forrás hiányzik a repóból | 2595 gyökből 453 (17,5%) üres | CC BY 4.0, de kevésbé teljes |
| archive.org OCR-szkennelt teljes szövegek (BDB, Gesenius) | **NEM használandó automatikus protokollban** | Tartalmilag teljes, de OCR-zajos, nem grep-elhető megbízhatóan | Csak kivételes, explicit jelzett manuális ellenőrzésre, ha egyáltalán szükséges |
| web_search | **TILOS** a determinisztikus protokoll részeként | — | Csak akkor, ha Basesoft kifejezetten kéri egy adott, nyitott kérdés kutatását — ilyenkor NEM kerül be ⚡-jegyzetként, hanem külön, "nem determinisztikus kiegészítés" jelzéssel |

---

## 4. Ritkaság-küszöb (egységesítve, 2026.09.03)

A ritkaság-küszöb **kontextusfüggő**, mert két különböző dolgot mér:

- **`<50`** — **szó-szintű kombinált keresésnél** (két vagy több
  Strong-szám együttes előfordulása egyetlen versen belül). Ez a
  kombinált co-occurrence-keresések ritkaság-szűrője.
- **`<200`** — **vers-pár-szintű összevetésnél** (pl. a 2/e LXX-híd
  lépésben egy teljes igehely-pár görög szókészletének metszete).
  Ez tágabb küszöb, mert egy teljes vers szókészlete természeténél
  fogva több gyakori szót (nyelvtani elem, kötőszó) is tartalmaz — a
  kockázat-szűrő szkript saját, >800 globális előfordulású
  "ragasztószó"-kizárása (l. `Kockazat_szures_riport_2026-09-03.md`)
  ennek a küszöbnek egy durvább, automatizált közelítése.

Mindkét küszöb megtartandó, alkalmazási kontextus szerint választva —
**explicit jóváhagyva, 2026.09.03.**

---

## 5. A TBESH/TBESG pontos rendeltetése — mit csinál, és mit NEM

**Alapvető megkülönböztetés, amit a triázs minden alkalmazásának
tiszteletben kell tartania:**

- **A vers-szintű rendszer (TSK, Károli-KH) — FELFEDEZŐ, BŐVÍTŐ funkció.**
  Új igehelyeket keres: "melyik másik vers kapcsolódhat ehhez a vershez?"
  — bemenete egy vers, kimenete egy lista korábban nem ismert,
  potenciálisan releváns jelöltekről. Ez a funkció bővíti a kapcsolatok
  halmazát.

- **A TBESH/TBESG — NEM ezt csinálja.** A TBESH/TBESG **nem talál új
  igehelyeket**. A munkája: megvizsgálja, hogy egy **már meglévő**
  kapcsolat (amit a vers-szintű rendszer már kiválasztott és beépített
  a tanulmányba, vagy amit a motívumnapló már rögzített) mögött **valódi,
  azonos motívum-szál** áll-e (azonos BDB-jelentésárnyalat), vagy csak
  **felszíni, véletlen szóazonosság** (más jelentésárnyalat, hamis
  pozitív).

  **Tehát: a TBESH/TBESG nem kereszthivatkozást keres, hanem
  motívum-azonosságot igazol vagy cáfol egy már meglévő kapcsolaton
  belül.**

Ez a projekt már meglévő "motif scope discipline" elvének (Strong-based
search for completeness + genuine content evaluation distinguishing true
matches, false positives, and related-but-structurally-different
occurrences) **finomítása, nem új tengely**: eddig a "tartalmi értékelés"
lépés szubjektív volt (valaki elolvasta a verset, és eldöntötte, hasonló-e
— l. korábbi elv: "Strong-number identity does NOT prove motif identity").
A TBESH/TBESG ezt teszi objektívebbé, forrás-hivatkozottá: nem "szerintem
hasonló", hanem "ugyanaz a BDB jelentésárnyalat, vagy más".

### Ebből következő, szűkített hatókör

A TBESH/TBESG-ellenőrzés **nem minden szónál releváns**, hanem
kifejezetten ott, ahol **egy motívum-igazolás (⭐-küszöb, "Lásd még"
hivatkozás, vagy egy már kiválasztott kereszthivatkozás) a Strong-szám
puszta egyezésén alapul**, és ezt meg szeretnék erősíteni vagy
megkérdőjelezni. Ez szűkebb, pontosabb hatókör, mint egy általános
"teológiailag súlyos szavak" kritérium.

Emellett igaz marad a korábbi megállapítás: a triázs nem a study saját,
adott 3/b pontban idézett kereszthivatkozásait nézi kizárólagosan, hanem
**a motívum teljes, más fájlokban (tematikus tanulmány, motívum-lexikon
cikk) is dokumentált ismert lexikai hálóját** — akkor is, ha az adott
bővített tanulmány saját 3/b pontja nem idézi az adott kapcsolatot.

---

## 6. Kétfunkciós triázs szétválasztása

Az 5. pontban tisztázott rendeltetésből (motívum-azonosság igazolása egy
MÁR MEGLÉVŐ kapcsolaton belül) közvetlenül következik ez a szétválasztás:

- **Motívum-azonosság ellenőrzés** (ez az 5. pontban tisztázott elsődleges
  funkció, napló-tápláló): 2+ előfordulás közötti BDB-árnyalat-egyezés/
  eltérés vizsgálata egy már meglévő kapcsolaton belül. Ez a
  `PaRDeS_motivumok.md` frissítését táplálja.
- **Exegetikai védettség-ellenőrzés** (study-belüli QA, más eredetű
  funkció): egyetlen előfordulás Drash-állításának védettsége a szótár
  alternatív árnyalataival szemben (pl. a כָּבַשׁ-eset, ahol a "gondoskodó
  uralom" tanítás nem zárta ki explicit a szótár keményebb olvasatait).
  NEM tartozik a napló-tápláló folyamathoz, külön kezelendő, és NEM
  íródik be a motívumnaplóba — marad a bővített sablon saját,
  study-belüli lépéseként.

**Gyakorlati következtetés:** amikor a kettő közül el kell dönteni, melyik
szolgálja "a lexikai folyamatot" (a naplót tápláló mechanizmust), a
**motívum-azonossági definíció a helyes, szűkebb hatókör**.

---

## 7. Szint-korlátozás

1. szint (a study saját szava → elsődleges jelentésárnyalat) **mindig lefut**.
2–3. szint (a kereszthivatkozásban idézett TOVÁBBI szó — pl. ἀρχή Kol
1:16-nál, σαββατισμός Zsid 4:9-nél) **csak explicit, névvel jelzett
kérésre nyílik meg**, nem automatikusan ugyanabban a körben.

---

## 8. "13-as kör" — ELVETVE (2026.09.03), történeti feljegyzésként megőrizve

**Döntés (2026.09.03):** a "13-as kör" mint külön jóváhagyandó
szűrő-lista elvetve — a 2/a-2/e technikasor mostantól minden, a
bővített sablon saját triázsán átment kulcsszóra lefut (l. 1. pont, 2.
lépés). A lista sosem lett véglegesítve (l. alább az eltérő
számítások), és a gyakorlati tapasztalat (két teljes study-audit) azt
mutatta, hogy külön kör-lista nélkül is kezelhető a technikasor
terjedelme. Az alábbi, korábban javasolt lista TÖRTÉNETI
FELJEGYZÉSKÉNT megmarad, de többé NEM éles protokoll-elem:

A korábbi munkamenet "13 motívum (8 ✅ önálló tanulmánnyal + 5 ⭐ küszöbön
túli)" számot említett, amely a teljes BDB-kiegészítést kapná (2/a lépés).
A `PaRDeS_motivumok_v43.md` fájl alapján végzett ellenőrzés ettől eltérő
számot ad (5–6 ✅ lezárt fájl/mélyelemzés + 6 ⭐ aktív küszöbön túli =
11–12, a Melkizedek-mélyelemzés és a Tehóm-komplexum kettős számítása
szerint változóan). **Ezt a listát Basesoft-nak explicit meg kell
erősítenie**, mielőtt ez a szakasz éles protokollként funkcionálna.
Javasolt jelölők a végleges listához, ha elkészül:

```
[ ] tehóm — a mélység motívuma
[ ] tehóm-abüsszosz-hádész-tartarosz (kibővített komplexum)
[ ] hádész (seól)
[ ] segítségül hívni az Úr nevét
[ ] Rafeusok/óriás-népek
[ ] Melkizedek — király-pap rendje (mélyelemzés — számít-e ide?)
[ ] pneuma/pszükhé megkülönböztetés ⭐
[ ] bűn következményeinek gyűrűzése ⭐
[ ] uralom-megbízás/emberi méltóság ⭐
[ ] Isten képmása (celem/eikón) ⭐
[ ] brít ⭐
[ ] oltárépítés — Ábrám vándorlásának jelölői ⭐
```

**Ez a záró mondat is elavult a fenti döntés fényében** — a gating
mostantól nem motívum-szinten, hanem study-szintű triázson átment
kulcsszavanként dől el (l. 1. pont, 2. lépés), nem a motívumnapló
motívumainak egy előre kijelölt alcsoportjaként.

---

## 9. Lezárási szabály

```
BDB-ellenőrzés: v2, [dátum] — triázs-szinten lezárva (2/a-2/e technikasor
szerint, max. 2 ⚡-jegyzet/PaRDeS-réteg), N nyitott kérdés dokumentálva.
Újranyitás csak explicit Basesoft-kérésre.
```

Motívum-szinten fut (nem study-szinten) tematikus tanulmányoknál, mert egy
motívum sosem "véglegesen lezárt" — új előfordulás esetén csak az ÚJ
előfordulás kap ellenőrzést, a korábbiak nem nyílnak újra automatikusan.

---

## 10. Napló-egyesítés és a 7. szakasz kötelezővé tétele (2026.09.03)

A jövőbeli BDB/TBESH-találatok **ugyanabba a kereszthivatkozás-napló-
formátumba** kerüljenek, mint amit a `1Moz_1v1_kereszthivatkozas_naplo.md`
és `1Moz_1v2-2v3_kereszthivatkozas_naplo.md` már bevált formában használ
(Hivatalossá téve-dátum, ✅/🔶/❌ minősítés, "javasolt, de még nem
végrehajtott" zárósor) — ne külön, párhuzamos napló-rendszer legyen.

**Kötelező sablon-elem (2026.09.03-tól):** minden ezután, ezzel a
protokollal auditált bővített tanulmány kapjon egy rögzített
**"7. szakasz — Lexikai audit, módszertani napló"** részt, amely
dokumentálja:
- mely kulcsszavakon futott le a 2/a-2/e technikasor;
- mi lett beépítve a study-ba, és mi lett explicit elutasítva, megnevezett
  indokkal (pl. gyenge/ellenőrizetlen forrás-attribúció miatt — l. 2. pont
  precedense);
- a forrás-hivatkozási fegyelem (2. pont) betartva dokumentálva minden
  egyes lelethez.

Ez a szakasz a bővített sablon (`2_PaRDeS_bovitett_sablon.md`) saját
struktúrájába nem íródik vissza automatikusan ezzel a dokumentummal — a
sablon-fájl saját, külön jóváhagyást igénylő frissítése továbbra is
nyitott feladat (l. 11. pont).

---

## 11. Nyitott végrehajtási kérdések

1. ~~A 8. pont "13-as kör" listájának végleges megerősítése~~ —
   TÁRGYTALANNÁ VÁLT (2026.09.03): a koncepció elvetve, l. 8. pont.
2. A bővített sablon (`2_PaRDeS_bovitett_sablon.md`) saját frissítése a
   kötelező 7. szakasszal (l. 10. pont) — ez a dokumentum eddig csak a
   *szabályt* rögzíti, a sablon-fájl saját szerkezeti frissítése még
   hátravan, külön jóváhagyással
3. Retroaktív vs. előremenő BDB-rollout a 20 meglévő bővített
   tanulmányra (korábbi, még döntetlen kérdés) — ide tartozik: a már
   auditált 2 study (1Moz_7v1-24, 1Moz_12v1-20) kapjon-e utólag formális
   7. szakaszt is, vagy a jelenlegi (Remez/Sod-blokkba illesztett)
   megoldás elegendő
