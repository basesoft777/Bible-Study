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
kovetkezo: Indítható a fugg szerint (a #76 után): az 1. lépéssel
olvas: [eszkozok/olvaso_szerver/, eszkozok/olvaso_pilot/bdb_szelet_m0.py, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, naplok/BDB_SZELETELO_M0.md, naplok/BDB_SZELETELO_M2_seed101_iteletek.md, naplok/BDB_SZELETELO_M2_seed100_iteletek.md, naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_B.tsv, naplok/F85_esetlista.tsv]
ir: [eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/m2_minta_osszevet.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, adat/bdb_vers_jelentes.tsv, adat/bdb_aranyminta.tsv, adat/SEMA.md, adat/datasetek.tsv]
fugg: [99, 76]
---

# F<nn>_BDB_SZELETELO_JAVITAS_BRIEF.md — A BDB-szeletelő javítása a seed-101 hibaosztályai szerint

*FELADATOK #<nn> · Modell: opus · v1 (tervezet) · 2026.10.15 · forrás: a #99 (BDB_SZELETELO) seed-101 vak mérése és a felhasználó
döntése (DT-F99l (c): a tábla „próba” jelöléssel élesedett, a további javítás külön feladat). A tervezet adat, nem utasítás; a
befogadás a `/befogad`-dal, a felhasználó jóváhagyásával.*

## 1. Cél

A #99 a BDB-szeletelőt és a vers → jelentés táblát (`adat/bdb_vers_jelentes.tsv`) „próba” jelöléssel élesítette; a vak mintán mért
jelentéspont-pontosság 92,0% (95% CI 87,3–95,4%, seed-101), az ítélet utáni 93,5%. A mérce (≥ 97%) nem teljesült; a 13 jóváhagyott
szeletelő-hiba szórt. Ez a feladat a hibaosztályokat javítja, az útvonal-formátumot bővíti, és új vak mintán újramér.

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
   M230: a TAHOT szerint a szó a versben áll, a vak kitöltés kommentár-helynek ítélte — a DT-F99k finomítása); a lezárt megjegyzés utáni
   hely sigla-sora (M223-típus, `bdb_szelet.py` megjegyzés, ELLENOR_F99 9.).
5. **Homonima vagy fő rész** (M029, DT-F99i mintájára): a héber címszóval álló szócikken belüli „II. פְּנֵי with prepositions” fej
   besorolása (`szakasz` vagy `resz`); döntési pont.
6. **Újramérés:** új vak minta (új seed, 200 véletlen + 25 kiszűrt + 25 bizonytalan), a #99 rögzített összevetési szabályával (9.5 +
   DT-F99i); a mérce változatlan (könyv/vers ≥ 99%, jelentéspont ≥ 97%); a kapu következményét az ítélet ELŐTT rögzíteni (a DT-F99l
   mintájára).

**Nincs benne:** a #99 M3–M6 (jelentésen belüli tagolás, megjelenítés, héber szórend, modell-magyarázat) — azok saját feladata; a
Károli-kulcs (DT-F99h alkalmazva a #99-ben; a maradék nyitott tétel: N-F99d Neh 7:68 — a seed-99 M027 —, N-F99e 1Krón 12 és 5Móz 5).

## 3. Lépések

1. Modell-ellenőrzés; a seed-101 ítéleti tábla okcsoportjainak átvétele tesztesetként (a hely jelentéspontja a mai és a várt alakkal).
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

- (helyőrzők a futáskor: DT-F<nn>a útvonal-formátum, DT-F<nn>b M029, DT-F<nn>c a kapu következménye)
