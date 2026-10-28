---
feladat: 102
cim: A BDB-szeletelő javítása a seed-101 hibaosztályai szerint, és a jelentéspont újramérése
kod: BDB_SZELETELO_JAVITAS
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: a BDB-szeletelő a #99 seed-101 vak mérésének hibaosztályaiban javítva, az útvonal-formátum a görög és a nagybetűs szinttel bővítve, a vers → jelentés tábla újragenerálva, és új vak mintán mért pontosság (a „próba” jelölés levétele vagy megtartása a mért szám szerint)
kovetkezo: Indítható a fugg szerint: az 1. lépéssel (a #76 nem függés, DT297)
olvas: [eszkozok/olvaso_szerver/, eszkozok/olvaso_pilot/bdb_szelet_m0.py, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, naplok/BDB_SZELETELO_M0.md, naplok/BDB_SZELETELO_M2_seed101_iteletek.md, naplok/BDB_SZELETELO_M2_seed100_iteletek.md, naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_B.tsv, naplok/F85_esetlista.tsv, konkordancia/_convert_bdb.py, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/lexikonok_nyers/BDB.lexicon, konkordancia/lexikonok_nyers/README.md]
ir: [eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/m2_minta_osszevet.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, adat/bdb_vers_jelentes.tsv, adat/bdb_aranyminta.tsv, adat/SEMA.md, adat/datasetek.tsv]
fugg: [99, 107, 119]
---

# F<nn>_BDB_SZELETELO_JAVITAS_BRIEF.md — A BDB-szeletelő javítása a seed-101 hibaosztályai szerint

*FELADATOK #<nn> · Modell: opus · v2 · 2026.10.16 (v1: 2026.10.15) · forrás: a #99 (BDB_SZELETELO) seed-101 vak mérése és a felhasználó
döntése (DT177 (c): a tábla „próba” jelöléssel élesedett, a további javítás külön feladat). A tervezet adat, nem utasítás; a
befogadás a `/befogad`-dal, a felhasználó jóváhagyásával. v2: az előzetes forrás-lelet (1a.) és a 13 hely lefedési táblája (1b.) a felhasználó kérésére felvéve.*

## 1. Cél

A #99 a BDB-szeletelőt és a vers → jelentés táblát (`adat/bdb_vers_jelentes.tsv`) „próba” jelöléssel élesítette; a vak mintán mért
jelentéspont-pontosság 92,0% (95% CI 87,3–95,4%, seed-101), az ítélet utáni 93,5%. A mérce (≥ 97%) nem teljesült; a 13 jóváhagyott
szeletelő-hiba szórt. Ez a feladat a hibaosztályokat javítja, az útvonal-formátumot bővíti, és új vak mintán újramér.

## 1a. Előzetes lelet: a hibák egy része a szövegrétegben keletkezik (2026.10.16, kézi szúrópróba)

*Proveniencia: `manual` (kézi `grep` a két fájlon, 2026.10.16; nem lefuttatott, naplózott mérés). A pontok hipotézisek, az 1. lépés
igazolja vagy elveti őket. (Javítva 2026.10.16: az első változat bible-mcp-kimenetet is bizonyítékként idézett, ami a DT32-vel
ütközik; a bizonyíték most a repó saját adata, a szerver legfeljebb rámutatás.)*

A szeletelő a `BDB_teljes_unabridged.tsv` sima szövegét olvassa. Ez a `DictBDB.json` (Eliran Wong, Tim Morton átirata)
HTML-jének `konkordancia/_convert_bdb.py`-val lecsupaszított alakja. Ugyanennek a digitalizálás-családnak egy másik formázása,
a `konkordancia/lexikonok_nyers/BDB.lexicon` (biblematedata, SQLite) a jelentéstagolást **jelölőkkel** őrzi:
`class="point"` 20 515, `class="section"` 913, `class="remarks"` 512 előfordulás (nyers számlálás a fájlon).

| Hely (seed-101) | A TSV-ben | A `BDB.lexicon`-ban | Következtetés |
|---|---|---|---|
| M102 (H0559) | `263.1Say` | `263</sup></lookup>.</p><div class="section"><p>1. <highlight>Say` | nem a BDB hibája; a szakaszhatár és a szóköz a `DictBDB.json`-ban vagy a konverzióban veszett el |
| M117 (H0539) | `Deut 28:59. 1.carried` | `Deut 28:59</ref>. 1. <highlight>carried` | ugyanaz |
| M140 (H7626) | `2 145:tribe` | `<div class="point"><b>2.</b> 145:tribe` | **valódi forráshiba**: a „145:” mindkét formázásban áll (`forras_hiba`) |
| M043-típus (H8057) | `2_46 (especially Psalms …` | `<div class="point"><b>2.</b><sub>46</sub> (especially …` | a `_46` a konverzió terméke (`_convert_bdb.py` 12. sor: `<sub>` → `_`); a nyersben a jelentéspont (`<b>`) és a gyakoriságszám (`<sub>`) egyértelműen elválik |

Nyitott: a `_convert_bdb.py` az ismeretlen tagot szóközre cseréli (15. sor), ezért az M102/M117 összeolvadása valószínűleg már a
`DictBDB.json`-ban megvan. Ezt csak a `DictBDB.json` maga dönti el; a repóban nincs meg, az URL a README-ben áll.

**A H7626 „145:” forráshiba-voltát a repó saját adata igazolja:** a `BDB_teljes_unabridged.tsv` H7626-sorának összefoglaló feje
„1 rod, staff, club, sceptre. 2 tribe” — a 2. jelentés a „tribe”, a „145:” tehát a szövegbe került idegen elem. (A bible-mcp
csak ráirányította a figyelmet erre a fejre; kimenete a DT32 szerint nem bizonyíték.) A TSV homográf-toldalékait a
`BDB_teljes_unabridged_README.md` írja le (`H90a` → `H0090a`); a 2026.10.15-i szóbeli feltevés, hogy a TSV egy sorba olvasztott több
homonimát (M130, M029), nincs mérve — az 1. lépés dönti el.

**Javaslat (döntésre, nem hatókör):** az OCR-okcsoport és a gyakoriságszámos jelölő javítása ne a szövegben folyjon. Két út:
(a) a TSV újragenerálása a jelölők megőrzésével (pl. `<sub>` → külön jel, nem `_`; a `point`/`section` határ sorjelként);
(b) a szeletelő tagolás-kontrollja a `BDB.lexicon` jelölőiből. Mindkettő új szövegréteg, ezért aranymintát és teljes
újramérést igényel. A `BDB.lexicon` licence ugyanúgy „tisztázatlan”, mint a TSV-é (`BDB_teljes_unabridged_README.md`).

### 1b. A seed-101 13 szeletelő-hibájának lefedése a `BDB.lexicon` jelölésével (2026.10.16)

*Proveniencia: `manual` (két egyszeri, csak olvasó SQLite-szkript a `Lexicon(Topic, Definition)` táblán, a repón kívül,
2026.10.16, és kézi `grep`; nem naplózott mérés). A `BDB.lexicon` 18 642 sorának egy része BDB-azonosítós (`BDB5049`), egy része
Strong-kulcsú (`H5117`); a Strong-kulcsú sor a hozzá tartozó BDB-szócikk(ek) másolata, egy Strong alatt több szócikkel.*

| Hely | Strong | Okcsoport | Nyers jelölés (rövidítve) | Lefedi? |
|---|---|---|---|---|
| M028 | H7379 | gyakoriságszám | `<div class="point"><b>3.</b><sub>39</sub> especially dispute` | **igen** |
| M043 | H8057 | gyakoriságszám | `<div class="point"><b>2.</b><sub>46</sub> (especially Psalms` | **igen** |
| M102 | H0559 | „OCR” | `263</sup></lookup>.</p><div class="section"><p>1. Say` | **igen** |
| M117 | H0539 | „OCR” | `Deut 28:59</ref>. 1. carried` | **igen** (a szóköz megvan; `point`-határ nincs) |
| M140 | H7626 | „OCR” / forráshiba | `<div class="point"><b>2.</b> 145:tribe` | **igen** (a jelölő `<b>`-ben; a „145:” szöveg marad) |
| M146 | H7227 | zárójeles jelölő | `<div class="point"><b>1.</b> (often opposed to …) <b>a.</b> (1)much` | **igen** |
| M243 | H1129 | zárójeles jelölő | `<div class="point"><b>1.</b> (literal) <b>a.</b> with accusative` | **igen** |
| M236 | H5437 | laza jelölő | `De and others </div><div class="point"><b>2. a.</b> march, or walk` | **igen** |
| M203 | H3068 | fő tagolás | `<div class="section"><p><b>I.</b> …` · `<div class="point"><b>II. 1.</b> …` | **igen** |
| M238 | H5608 | jelöletlen alcímszó | külön szócikk: `<h1>BDB5696 [H5608]</h1> … סֹפֵר, סוֺפֵר <b>noun masculine</b>` | **igen** (szócikkhatár) |
| M031 | H5117 | törzsfejléc | `<b>Hiph`il A.</b> Perfect 3 masculine singular` · `<b>B.</b> Perfect` | **részben**: a fejléc egy `<b>`-elem, de nem `section`/`point` |
| M162 | H3318 | törzs nélküli első törzs | `— <div class="point"><b>1.</b> go or come out or forth: <b>a.</b>` | **részben**: a jelentéspont és a betű egyértelmű, a „Qal” név itt is hiányzik (kikövetkeztetendő) |
| M130 | H8478 | magányos II. | `Ezek 47:1</ref>b <b>II.</b> as <b>preposition</b>` (nem `div`-ben, I. nincs) | **nem**: csak a `<b>` különíti el; szabály kell |

**Összesítve:** 10 igen, 2 részben, 1 nem. Ha a jelölés a 10 helyet javítja, 3 hiba marad (98,5%), a két részlegessel 1 (99,5%) —
**a seed-101 mintán**. Ez nem a kapu mérése: (1) a seed-101-re hangolt javítás erre a mintára optimista; (2) az új forrásréteg új
hibákat hozhat, amelyeket a seed-101 nem mutat; (3) a kapu az új vak mintán (2. pont 6.) dől el. Két mellékmegfigyelés: a TSV
„Perfect3masculine” alakja a nyersben „Perfect 3 masculine” (szóközvesztés a TSV-láncban, mint M102/M117); az M162-nél a
„Qal” név mindkét formázásból hiányzik, tehát az nem konverziós hiba.

## 1c. Átadás a #107-ből (2026.10.18)

*A #107 (BDB_JELOLT_SZOVEG) 8. lépése; a felhasználó döntése szerint (2026-10-18) egyeztetett eltérésként a #107 írja ezt a szakaszt —
csak a törzset, a fejlécet nem. Forrás: `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 4.8, 6.1; mérés: `eszkozok/bdb_jelolt/szerkezet_osszevet.py`
(F107.29, `5aba58c9`).*

**Elérhető (a #107 ágán, merge után a main-en):**
- `adat/bdb_szakaszok.tsv` (SEMA 2.30) — a BDB minden szócikke (a `DictBDB.json` 8 090 Strongja) szakaszokra bontva a nyers forrás
  jelölőiből (DT225 (c) hibrid: a szöveg és a tagolás a JSON-ból, a `bdb_id`, a szócikkhatár és a `section`/`remarks` a `BDB.lexicon`-ból,
  csak metaadatként); oszlopok: `strong`, `bdb_id`, `sorszam`, `alszocikk`, `szakasz`, `resz`, `utvonal`, `jelolo`, `jel`, `gyakorisag`,
  `szoveg`, `illesztes`, …; kulcs `strong` + `sorszam`.
- `adat/bdb_forras_javitas.tsv` (SEMA 2.31) — a forráshibák javítótáblája: `pe_mem` (a JSON dagesses pe → mem hibája, 3 823 `javitva`),
  `hivatkozas` (a TSV F34/F46 hivatkozás-javításai, 412), `kezi` (7 szerkezeti forráshiba, mindkét nyers forrásban igazolva).
- Eszközök: `eszkozok/bdb_jelolt/bont.py` (bontó), `nezet_general.py` (sima szöveges nézet a táblából + javítótáblából),
  `szerkezet_osszevet.py` (aranyminta / seed-101 / korpusz összevetés), `teszt_bont.py`.
- **Az útvonal-formátum nincs kanonikus kulcsként befagyasztva** (DT190 🟡): `<törzs>[.<nagybetű>]/<szám>/<betű>[/<zárójeles>]`, a 2.28/2.29
  formátumához igazítva, a #102 két bővítésével (nagybetűs csoport, zárójeles szint); a homonima-szakasz külön `szakasz`, a római fő tagolás
  külön `resz` oszlop.

**Mért számok a táblán (teljes / a `forras_hiba` csomópontok és helyek nélkül):**

| mérce | teljes | `forras_hiba` nélkül |
|---|---|---|
| aranyminta (`adat/bdb_aranyminta.tsv`, 425 törzs / jelentés / alpont) | 411 / 425 (96,7%) | 411 / 416 (98,8%) |
| seed-101 (a #99 13 szeletelő-hibájának helye) | 9 / 13 | 9 / 10 |
| korpusz: a tábla útvonala ↔ a mai szeletelő (`adat/bdb_vers_jelentes.tsv`, 159 804 nem szűrt hivatkozás) | 136 538 (85,4%) | — |

Seed-101 helyenként: egyezik M028, M031, M043, M140, M146, M203, M236, M238, M243; `forras_hiba` (a nyers forrásban igazolva, kézi sor a
javítótáblában) M102 (H0559: a „Qal” és az „1” jelöletlen), M117 (H0539: a „Niph`al” és az „1.” jelöletlen), M162 (H3318: a „Qal” név
hiányzik); nem egyezik M130 (H8478: a magányos „II.” `resz`-ként megvan, de az „1” a forrásban nem félkövér, és a seed várt helye a forrásból
nem azonosítható egyértelműen). A korpusz-eltérés (14,6%) soronként nincs osztályozva (`szerkezet_osszevet.py --korpusz --lista N`).

**JAVASLAT a hatókör szűkítésére (a #107 brief 8. lépése szerint; a felhasználó a `/befogad`-dal hagyja jóvá, addig a fenti 2. Hatókör
érvényes):**
- *A tábla által megszűnő (a táblán mérve kezelt) hibaosztályok:* a zárójeles és a gyakoriságszámos jelölő (M028, M043, M146, M243 — a
  `<sub>` a `gyakorisag` oszlopban); a törzsfejléc „Hiph`il A./B.” (M031); a fő tagolás „II.” (M203); a jelöletlen alcímszó (M238, szócikkhatár);
  a laza „2. a.” jelölő (M236); a fej-összefoglaló és a „1.a.” fej (M140); az útvonal-formátum (nagybetűs és zárójeles szint a táblában).
- *Forrásban hibás, a javítótáblában kézi sorral (nem a szeletelő dolga):* az OCR-tapadás „263.1Say” (M102) és „1.carried” (M117), a hiányzó
  „Qal” név (M162).
- *Ami marad a #102-nek:* az igehely → szakasz hozzárendelés a táblán (a szeletelő átállása); az öröklés (az egyfejezetes könyv után); a
  sigla-szűrés; az M130 (magányos „II.”); a korpusz-eltérések (14,6%) osztályozása; új vak mérés a táblán.

## 1d. A #131-ben elkészült két tétel (2026-10-28)

A DT-F131k és a DT-F131l eredetileg a #102-nek átadott tétel volt. A felhasználó döntése szerint (2026-10-28: „meggondoltam. rövid úton legyen kész,
de hibátlan a 131”) mindkettő a #131-ben (SZOTARI_GERINC) elkészült, a #102 `ir`-fájljaiban is. A #102 ezeket nem ismétli, a mérését a
javított kinyerőre építi.

- **DT-F131k (a):** a 2.31 (`adat/bdb_forras_javitas.tsv`) új hibaosztálya a `hivatkozas_kezi` (kézi sor, `manual`): H8034 „26:35” → 26:25.
  A 2.29 kinyerője olvassa (okkód `forras_javitas`) (F131.3.20–F131.3.21).
- **DT-F131l (A):** a `bdb_szelet.py` `hivatkozasok()` a verstartomány után is keresi a vers-folytatást („1Kin 18:24-25, 26” → 18:26), kibontás
  nélkül. Az `adat/bdb_vers_jelentes.tsv` `--ts 2026-10-28`-cal újragenerálva: +1 438 sor, 603 Strong, 35 012 `sorszam`-eltolódás
  (F131.3.21; `naplok/F131_SZOTARI_GERINC_naplo.md` 5.5). **Nem készült el (a #102 dönt róla):** a tartományok kibontása (DT-F131l (B)).
  A tartomány utáni ágon a folytatás nem indulhat egy kiírt hivatkozás kezdetén („16:8-9, 1 Samuel 21:16”: az „1” könyvnév). A
  tartomány nélküli ágon ez az ellenőrzés nincs: a teljes táblában 1 ilyen sor van, a javítás előtt is (H1004, „2Chr 10:19, 2 Chronicles
  10…” → hamis 2Krón 10:2 folytatás). A #131 ezt nem javította, ez a #102-é. *(proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes |
  forras=eseti szkript (F131_tartomany_nelkuli_ag_meres.py, a session közös jegyzetmappájában; `bdb_szelet.hivatkozasok`, a teljes BDB) | ts=2026-10-28)*

## 2. Hatókör

**Benne (mérési alap: `naplok/BDB_SZELETELO_M2_seed101_iteletek.md`, a seed-100 ítéletei mellett):**

1. **Öt okcsoport a seed-101 13 szeletelő-hibájából:**
   - zárójellel vagy gyakoriságszámmal folytatódó jelölő: „3_39”, „2_46” (M028, M043), „1 (often opposed …)”, „1 (literal)” (M146, M243);
   - OCR: „263.1Say” (M102), „1.carried” (M117), „2 145:tribe” és fejléc-glossza (M140);
   - törzsfejléc: „Hiph`il A. Perfect” (M031), a „Qal” fej nélküli első törzs (M162);
   - fő tagolás: a magányos „II.” I. nélkül (M130), a H3068 angol tagolása (M203);
   - laza jelölő és jelöletlen alcímszó: „others 2. a.” (M236), „סוֺפֵר סֹפֵר, noun” (M238).
2. **Útvonal-formátum bővítése:** a görög betűs negyedik szint (δ; M008) és a nagybetűs csoportszint (A./B.; M011) — az aranymintában
   (`adat/bdb_aranyminta.tsv`, SEMA 2.28), a szeletelőben, a táblában (SEMA 2.29) és az összevetőben (`m2_minta_osszevet.py`).
3. **Öröklés:** az egyfejezetes könyv (pl. „Obadiah 19”) után a könyv nélküli hely a megelőző könyvet folytatja (seed-101 M092:
   „2Chr 17:2; compare 34:6; … Obadiah 19; … 31:1” → 2Krón 31:1; ma `orokles_hibas`).
4. **Szűrés (seed-101, napló 9.14):** a nem bibliai jelölőről öröklődő könyv a bibliai helyre (igazolt hamis pozitív: H2623
   „116:15” — és a Zsolt 149:1, 5, 9, 4 sor —, H4912 „1:1”); a hét `sigla_igazolt` eltérés elbírálása (M054, M065, M147, M149, M191, M198,
   M230: a TAHOT szerint a szó a versben áll, a vak kitöltés kommentár-helynek ítélte — a DT176 finomítása); a lezárt megjegyzés utáni
   hely sigla-sora (M223-típus, `bdb_szelet.py` megjegyzés, ELLENOR_F99 9.).
5. **Homonima vagy fő rész** (M029, DT174 mintájára): a héber címszóval álló szócikken belüli „II. פְּנֵי with prepositions” fej
   besorolása (`szakasz` vagy `resz`); döntési pont.
6. **Újramérés:** új vak minta (új seed, 200 véletlen + 25 kiszűrt + 25 bizonytalan), a #99 rögzített összevetési szabályával (9.5 +
   DT174); a mérce változatlan (könyv/vers ≥ 99%, jelentéspont ≥ 97%); a kapu következményét az ítélet ELŐTT rögzíteni (a DT177
   mintájára).

**Nincs benne:** a #99 M3–M6 (jelentésen belüli tagolás, megjelenítés, héber szórend, modell-magyarázat) — azok saját feladata; a
Károli-kulcs (DT173 alkalmazva a #99-ben; a maradék nyitott tétel: N-F99d Neh 7:68 — a seed-99 M027 —, N-F99e 1Krón 12 és 5Móz 5).

## 3. Lépések

1. Modell-ellenőrzés; a seed-101 ítéleti tábla okcsoportjainak átvétele tesztesetként (a hely jelentéspontja a mai és a várt alakkal).
   Az 1a. lelet igazolása: a `DictBDB.json` ugyanezen helyei (hibás-e már ott az M102/M117), és a 13 hiba besorolása
   `szoveg_konverzio` / `forras_hiba` / `szeleto` szerint. ⛔ Ha a hibák számottevő része a szövegrétegben keletkezik: az 1a. (a)/(b)
   út javaslatként a `DONTESEK.md`-be (`DT-F<nn>d`), megállás a 2. lépés előtt.
2. Javítás okcsoportonként, minden csoport után: a tábla újragenerálása (kilépési kód + mtime-őr), aranyminta (`bdb_szelet_m0.py
   --arany`), a korpusz-szintű szerkezetváltozás szúrópróbája, tesztek (`teszt_bdb_vers_jelentes`, `teszt_futtat --gyors`, pilot).
3. ⛔ Az útvonal-formátum bővítése (2. pont) és az M029 (4. pont): javaslat a `DONTESEK.md`-be, megállás.
4. Az öröklési szabály (3. pont) a teljes táblán mért hatással.
5. ⛔ Az újramérés előtt: a kapu következménye rögzítve; vak munkalap + kulcs (új seed); a vak kitöltést az orkesztrátor indítja.
6. ⛔ Ítéleti tábla forrásidézettel (szeletelő-hiba / kitöltő-hiba / kulcs-ellentmondás / `forras_hiba`), jóváhagyás.
7. A szó-lap mért pontosságának frissítése (`blokkok.py` `BDB_MERT_PONTOSSAG`) a jóváhagyott nyers számra; a „próba” jelölés sorsa a
   kapu szerint.

## 4. Elfogadási feltételek

- A seed-101 13 szeletelő-hibájának helyén a tábla a jóváhagyott ítélet szerinti jelentéspontot adja (teszttel).
- Az aranyminta nem romlik (hibás szócikk, szerkezeti eltérés, jó cím: legalább a #99 záró számai: EN 7/32, HU 4/14; 71/72).
- Az új vak minta eredménye a rögzített mércével és a kapu előre rögzített következményével értékelve; a szó-lapon a mért szám áll.

## 5. Döntésnapló

- (helyőrzők a futáskor: DT-F<nn>a útvonal-formátum, DT-F<nn>b M029, DT-F<nn>c a kapu következménye, DT-F<nn>d a szövegréteg útja az 1a. szerint)
