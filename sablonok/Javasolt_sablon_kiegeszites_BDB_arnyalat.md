# Javasolt sablon-kiegészítés — BDB-árnyalat integrálása a PaRDeS-tanulmányokba

*v1 (rekonstruált) — 2026.09.02. Az eredeti fájl elveszett egy korábbi
kontextusablak-váltás során; ez a verzió a 2026.09.01–02-i munkamenetek
következtetéseiből újraépítve készült, kiegészítve a determinisztikus
protokollal, ami az eredetiből még hiányzott.*

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

## 1. Determinisztikus protokoll v1 (MINDEN MÁS ELŐFELTÉTELE)

```
BDB/TBESH-ELLENŐRZÉSI PROTOKOLL v1 — minden triázson átment szónál,
KIVÉTEL NÉLKÜL, ebben a sorrendben:

1. `grep "^H####" konkordancia/TBESH.txt` (héber) vagy
   `grep "^G####" konkordancia/TBESG.txt` (görög) — MINDIG lefut,
   MINDEN triázson átment szónál.

2. HA a szó a "13-as kör" tagja (l. 6. pont — a pontos lista Basesoft
   jóváhagyására vár) → KÖTELEZŐEN kiegészítve teljes BDB-kereséssel is:
   `grep "^H####" konkordancia/BDB_teljes_unabridged.tsv`
   (elsődleges teljes forrás — l. 2. pont a forrás-hierarchiában).

   2/b. HA a szó a BDB_teljes_unabridged.tsv-ben SEM ad tartalmilag
        érdemi találatot (rendkívül ritka eset, mivel ez a forrás
        8090/8090 bejegyzésnél tartalmaz szöveget) → EXPLICIT gap-jelzés
        a ⚡-jegyzetben: "Determinisztikus forrásból etimológiai/
        jelentésárnyalati adat nem elérhető." NEM pótolható web_search-csel
        vagy Claude általános tudásából.

   2/c. Ha a fejszó BDB-szócikke "Origin: from H####" vagy hasonló
        gyök-hivatkozást tartalmaz, ELLENŐRIZD a hivatkozott Strong-szám
        szócikkét is ugyanazon forrásban (TBESH.txt / BDB_teljes_unabridged.tsv),
        mielőtt a fejszó szócikkét "teljesnek" tekintenéd. A gyök-etimológia
        gyakran külön Strong-szám alatt szerepel, nem a származék szó
        szócikkében.

3. Minden ⚡-jegyzet FELTÜNTETI, melyik lépés(ek) futottak le, és melyik
   fájlból (TBESH.txt / BDB_teljes_unabridged.tsv).

4. TILOS korábbi, más kontextusban/munkamenetben talált adatot
   "visszamásolni" ellenőrzés nélkül — minden ⚡-jegyzet a SAJÁT, ebben
   a körben lefuttatott 1–2. lépésből származik.

5. Ha egy szó szócikke egy másik Strong-számra hivatkozik gyök-eredetként
   ("Origin: from H####" vagy "√" jelölés a BDB-szövegben), a protokoll
   KÖVESSE VÉGIG ezt a hivatkozást, és ellenőrizze a hivatkozott
   Strong-szám szócikkét is, mielőtt gap-et jelezne. Konkrét precedens
   (2026.09.02): a תְּהוֹם/H8415 "Origin: from H1949" hivatkozása a
   הום-gyök szócikkére mutat, ami tartalmazza a "morajlás" etimológiát —
   ez csak a hivatkozási lánc végigkövetésével derült ki, a H8415 önálló
   ellenőrzése tévesen "nem igazolható" eredményt adott.
```

---

## 2. Forrás-hierarchia (frissítve, 2026.09.02)

| Forrás | Szerep | Megbízhatóság | Megjegyzés |
|---|---|---|---|
| `TBESH.txt` / `TBESG.txt` (repóban) | 1. lépés, mindig fut | Csak sense-hierarchia, gyök-etimológia nélkül | STEPBible CC BY 4.0 |
| `BDB_teljes_unabridged.tsv` (bevezetendő) | **Elsődleges teljes forrás**, 2. lépés | 8090/8090 bejegyzés, 0 üres | Közkincs (Tim Morton/Eliran Wong), l. `Code_prompt_teljes_BDB_bevezetese.md` |
| openscriptures `BrownDriverBriggs.xml`+`LexicalIndex.xml` | Másodlagos/tartalék, csak ha az elsődleges forrás hiányzik a repóból | 2595 gyökből 453 (17,5%) üres | CC BY 4.0, de kevésbé teljes |
| archive.org OCR-szkennelt teljes szövegek (BDB, Gesenius) | **NEM használandó automatikus protokollban** | Tartalmilag teljes, de OCR-zajos, nem grep-elhető megbízhatóan | Csak kivételes, explicit jelzett manuális ellenőrzésre, ha egyáltalán szükséges |
| web_search | **TILOS** a determinisztikus protokoll részeként | — | Csak akkor, ha Basesoft kifejezetten kéri egy adott, nyitott kérdés kutatását — ilyenkor NEM kerül be ⚡-jegyzetként, hanem külön, "nem determinisztikus kiegészítés" jelzéssel |

---

## 3. A TBESH/TBESG pontos rendeltetése — mit csinál, és mit NEM

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

## 4. Kétfunkciós triázs szétválasztása

A 3. pontban tisztázott rendeltetésből (motívum-azonosság igazolása egy
MÁR MEGLÉVŐ kapcsolaton belül) közvetlenül következik ez a szétválasztás:

- **Motívum-azonosság ellenőrzés** (ez a 3. pontban tisztázott elsődleges
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

## 5. Szint-korlátozás

1. szint (a study saját szava → elsődleges jelentésárnyalat) **mindig lefut**.
2–3. szint (a kereszthivatkozásban idézett TOVÁBBI szó — pl. ἀρχή Kol
1:16-nál, σαββατισμός Zsid 4:9-nél) **csak explicit, névvel jelzett
kérésre nyílik meg**, nem automatikusan ugyanabban a körben.

---

## 6. "13-as kör" — NYITOTT, Basesoft jóváhagyására vár

A korábbi munkamenet "13 motívum (8 ✅ önálló tanulmánnyal + 5 ⭐ küszöbön
túli)" számot említett, amely a teljes BDB-kiegészítést kapná (2. lépés).
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

A többi, ~62 motívum csak az 1. lépést (TBESH/TBESG-grep) kapja.

---

## 7. Lezárási szabály

```
BDB-ellenőrzés: v1, [dátum] — triázs-szinten lezárva (5 kritérium
szerint, max. 2 ⚡-jegyzet/PaRDeS-réteg), N nyitott kérdés dokumentálva.
Újranyitás csak explicit Basesoft-kérésre.
```

Motívum-szinten fut (nem study-szinten) tematikus tanulmányoknál, mert egy
motívum sosem "véglegesen lezárt" — új előfordulás esetén csak az ÚJ
előfordulás kap ellenőrzést, a korábbiak nem nyílnak újra automatikusan.

---

## 8. Napló-egyesítés

A jövőbeli BDB/TBESH-találatok **ugyanabba a kereszthivatkozás-napló-
formátumba** kerüljenek, mint amit a `1Moz_1v1_kereszthivatkozas_naplo.md`
és `1Moz_1v2-2v3_kereszthivatkozas_naplo.md` már bevált formában használ
(Hivatalossá téve-dátum, ✅/🔶/❌ minősítés, "javasolt, de még nem
végrehajtott" zárósor) — ne külön, párhuzamos napló-rendszer legyen.

---

## 9. Nyitott végrehajtási kérdések

1. A 6. pont "13-as kör" listájának végleges megerősítése
2. A `Code_prompt_teljes_BDB_bevezetese.md` tényleges kiadása Claude
   Code-nak (l. külön fájl)
3. Retroaktív vs. előremenő BDB-rollout a 20 meglévő bővített
   tanulmányra (korábbi, még döntetlen kérdés)
4. ~~A `TBESH_pilot_riport_1Moz_1v2-2v3.md` és `Ujrageneralt_1Moz_1v2-2v3_TELJES.md`
   felülvizsgálata a הום-gyök állítás miatt~~ — **LEZÁRVA (2026.09.03,
   keresés nélkül):** a két fájl továbbra sem található, de a felülvizsgálat
   célja okafogyottá vált — a הום-gyök állítás időközben három hiteles
   helyen javítva lett (`BDB_teljes_unabridged_README.md`,
   `1Moz_1v2-2v3_bovitett.md` v4, a kereszthivatkozás-napló 6. szakasza).
   A két elveszett fájl elvesztése emiatt nem blokkoló, további keresés nem
   szükséges.
