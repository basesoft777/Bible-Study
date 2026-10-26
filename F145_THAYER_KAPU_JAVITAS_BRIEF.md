---
feladat: 145
cim: A Thayer-lánc kapujavítása — a 16. kapu műcím-kivétele és ragozás-tűrése, az ellenoriz.py 13. szabályának és a CI E19-nek Thayer-szakasz-ága, a két állapotfüggő teszt (a #142 újraindításának előfeltétele)
kod: THAYER_KAPU_JAVITAS
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: dontesre_var
ag: ccr-4d66ac1d-v5f9un
ad: a 16_sigla kapu a változatlanul átvett műcímben álló siglát nem követeli meg, a magyar alakot ragozva és számjegy mögött (`Homérosztól`, `4Makk`) is elfogadja; az ellenoriz.py 13. szabálya a Thayer szakaszsorok forrásszövegét is ismeri (SÉRTÉS 0); a CI E19 a `teljes` hivatkozást a Strong teljes `sz<n>`-lefedettségével is fedettnek veszi (a #142 PR #482-je zöld); a teszt_lanc.py két állapotfüggő tesztje zöld; a #142 bukott és várakozó 8 Strongja újrafuttatható
kovetkezo: "Te: [elteres_kor 1/2] ELLENOR_F145 1b. tartalmi (DT-F145a: a szerző-típusú siglák átvétel-kivétele); a döntés után /elteres 145 vagy zárás; a PR címe [ELLENŐRZŐ] előtagú"
pr:
lezarva_osszegzes: "A 16_sigla kapu műcím-kivétele, ragozás-tűrése és számjegy-előtagja, az ellenoriz.py 13. szabályának Thayer-ága és a CI E19 szakasz-lefedettsége kész, a két állapotfüggő teszt állapot-független; a #142 fáján ellenoriz.py SÉRTÉS 1→0, E19 HIBA 3→0, a 8 Strong 16. kapuja (kontroll-próba) RENDBEN, az 5 rögzített Strong kapusora változatlan (naplok/F145_zaras.md)."
olvas: [eszkozok/thayer_jelolt/, eszkozok/normalizal.py, eszkozok/ellenoriz.py, eszkozok/teszt_ellenoriz_13.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, adat/thayer_sigla.tsv, adat/thayer_szakaszok.tsv, adat/thayer_forras_javitas.tsv, adat/terminologia.tsv, naplok/F132_THAYER_SZAKASZ_bukottak.tsv, F142_THAYER_M3_BRIEF.md, F132_THAYER_SZAKASZ_BRIEF.md]
ir: [eszkozok/thayer_jelolt/thayer_kapuk.py, eszkozok/thayer_jelolt/teszt_lanc.py, eszkozok/ellenoriz.py, eszkozok/teszt_ellenoriz_13.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, adat/SEMA.md]
fugg: []
nem_fugg: [38, 131, 142]
---

# Fnn_THAYER_KAPU_JAVITAS_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.26 · készítette: a #142 orkesztrátora (`claude-opus-5-5`), a DT-F142a–d
javaslatai szerint, a felhasználó kérésére (chat, 2026-10-26: „igen, írd meg a briefet”); befogadás: `/befogad`, a felhasználó
jóváhagyásával. Befogadáskor a #142 fejlécének `fugg` mezőjébe ennek a feladatnak a száma kerül (a `/befogad` dolga, jóváhagyással).*

## 1. Cél

A #142 (THAYER_M3) futása (F142.4–F142.14, ág `ccr-d5dec8d2-infvx9`) 13 gerinc-Strongból 5-öt lefordított; 5 bukott, 3 vár, és egyik
sem a fordításon múlik, hanem a #132 láncán (a #142 a #132 eszközeit nem módosíthatja). E feladat a láncot javítja, fordítást nem
végez. Az érintett tételek (mind `DONTESEK.md`, javaslatuk szerint):

- **DT-F142b (B):** a `Philo` a G0012, G0282, G4151 forrásában részben német műcímben áll (`Philo's Lehre von der Weltschöpfung`);
  a prompt (5. szabály) a műcímet változatlanul hagyja, a `16_sigla` viszont `Philón`-t követel.
- **DT-F142c:** a `16_sigla` a magyar alakot ragozatlanul, önálló szóként várja (`thayer_kapuk._re`: `(?<![\w])…(?![\w])`), ezért
  (i) a `from Homer down` → `Homérosztól kezdve` (5. kapu, terminológia) és a `Homer` → `Homérosz` (16. kapu) egyszerre nem
  teljesíthető (G1311, G5351, G5590); (ii) a `Macc.` → `Makk` (16. kapu) és a `4Makk` / `2Makk` könyvnév (11. kapu,
  `normalizal.APOKRIF_ALIAS`) kizárja egymást (G1944, G5010, G5590).
- **DT-F142d:** az `ellenoriz.py` 13. szabálya (`_szakasz_szoveg`) csak a `BDB` `sz<n>` sorokhoz keres forrásszöveget; a 19 új
  Thayer-sorra `nincs hozzá forrásszöveg` SÉRTÉS-t ad (a #142 előtt SÉRTÉS 0, utána 1).
- **CI E19 (PR #482, run 40371120583, `f11eaf9d`):** `HIBA adat/lexikon_hivatkozasok.tsv:9 -- Thayer G0086 G86/teljes -- nincs opus,
  sonnet vagy kezi forditas (sem erre a jelentesre, sem teljes szintre)`; ugyanígy a 15. (G2671) és a 19. sor (G5356). Ok: a DT329 (i)
  szerint a régi nem `kezi` `teljes` sor `elavult` lett, az E19 (`szabalyok.py` `e19_szotari_forditas_hiany`) viszont a `teljes`
  hivatkozást csak `teljes` vagy azonos `jelentes_szam`-ú fordítással tekinti fedettnek, a Strong `sz<n>` szakaszsoraival nem.
- **DT-F142a:** a `teszt_lanc.py` két tesztje állapotfüggő: a `test_g1941_reszei` a sigla-jóváhagyás előtti állapotot várja
  (`` `cf.` [besorolatlan …] `` a jóváhagyott `` `cf.` → `vö.` `` helyett); a `test_beir_kezi_marad` feltételezi, hogy a valódi
  `forditasok.tsv`-ben nincs G1941 szakaszsor (az F142.7 óta van).

## 2. Hatókör

**Benne van:**
1. `thayer_kapuk.py` `ellenoriz_sigla` — **(a) műcím / változatlan átvétel:** a forrás egy siglás előfordulása nem követeli meg a
   magyar alakot, ha az előfordulást hordozó, változatlanul átvett szakasz (a sigla és a közvetlen szövegkörnyezete, pl. a sigla és
   az utána álló legalább 3 szó) szó szerint megvan a fordításban. A kapu csak a nem így átvett előfordulásokra követeli meg a magyar
   alakot; ha minden előfordulás átvett, a sor nem ellenőrzött (a kimenetben megnevezve, pl. „1 sigla változatlan átvételben”).
   A pontos szabályt (az ablak mérete, a határ) a végrehajtó rögzíti a docstringben és a naplóban, és a hamis negatív ellen teszttel
   védi (ha a fordításban csak a műcím maradt meg, a folyó szövegbeli `Philo` viszont nem lett `Philón`, a kapu SERTES).
   **(b) ragozás-tűrés:** a cél-oldali (`magyar_alak`) keresés szó elején kezdődik, de toldalékot elfogad (`Homérosztól`,
   `Makk-ban`); a forrás-oldali keresés változatlan. **(c) számjegy-előtag:** a `könyvrövidítés` típusú sor cél-alakja számjegy
   mögött is találat (`4Makk`, `2Makk`). Az egybetűs sigla láncszabálya (F132.20) nem változik.
2. `ellenoriz.py` 13. szabály — **Thayer-ág:** a `szotar = Thayer`, `sz<n>` sor forrásszövege a `thayer_bemenet` szakaszaiból
   (a `forditas.py rogzit` által használt szövegből, ugyanazzal a hash-számítással); a lefedettség-ellenőrzés (egy Strong nem
   `elavult` `sz<n>` sorai a Strong összes szakaszát fedik) a BDB-vel azonos módon. Teszt a `teszt_ellenoriz_13.py`-ban.
2b. `szabalyok.py` E19 — a `jelentes_szam = teljes` hivatkozás fedett, ha a Strongnak (szotár + strong + entry_id) a
   `forditasok.tsv`-ben a szótár összes szakaszát lefedő, nem `elavult` (`opus` / `sonnet` / `kezi`) `sz<n>` sorai vannak (a
   szakaszkészlet a 13. szabály Thayer-, illetve BDB-ágával azonos forrásból); részleges lefedettség nem fed. Teszt a
   `test_szabalyok.py` `E19Teszt` osztályában (teljes lefedettség: nincs találat; hiányzó szakasz: HIBA). A `lexikon_hivatkozasok.tsv`
   nem változik.
3. `teszt_lanc.py` — a `test_g1941_reszei` várakozása a jóváhagyott sigla-állapotra (`` `cf.` → `vö.` ``), vagy a tábla
   fixture-ként (állapot-független; a végrehajtó választ, a naplóba indokolva); a `test_beir_kezi_marad` állapot-független
   (ideiglenes `forditasok.tsv`-másolaton, a valódi tábla állapotától függetlenül). Új tesztek az 1. pont (a)–(c) eseteire,
   pozitív és negatív mintával.
4. A `SEMA.md` 2.37 (a 16. kapu szabályainak leírása) és a `thayer_kapuk.py` docstringje az új szabályokkal.

**Nincs benne:**
- fordítás, a `forditasok.tsv`, a `thayer_sigla.tsv` és a `bukottak.tsv` módosítása (a #142 újrafuttatása a #142 dolga);
- a 11. kapu és a `normalizal.APOKRIF_ALIAS` (a #38 / BDB közös eszköze), a `forditas_kapuk.py` bármely módosítása;
- a `lekerdez.py` „Sir = JSir” aliasa (N-F142a);
- a main-en már fennálló `# forras:` hash-eltérés (`sigla_gyujt.py --ellenoriz`, `teszt_bont.py` 2 hiba,
  `teszt_lanc.py::test_tabla_determinisztikus_es_kezi_vedett`): csak mérés és naplózás; ha az ok egyértelmű és a javítás csak
  fejléc-újragenerálás, külön nyitott tétel (`N-F<nn>`), nem e feladat írása.

## 3. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **M0 — mérés a javítás előtt:** a 8 érintett Strong (G0012, G0282, G4151, G1311, G1944, G5010, G5351, G5590) kapueredménye a
   #142 munkafájljaiból vagy újra előállítva (`forditas.py elokeszit` a scratchpadbe; a bukott vázlatok szövege a `bukottak.tsv`
   okai szerint), a `ellenoriz.py` 13. szabály kimenete, a tesztek állapota — a naplóba, proveniencia-sorral.
2. **A 16. kapu (2. hatókör 1.)**, tesztekkel; commit.
3. **A 13. szabály Thayer-ága (2. hatókör 2.)** és **az E19 szakasz-lefedettsége (2b.)**, tesztekkel; tételenként commit.
4. **A két állapotfüggő teszt (2. hatókör 3.)**; commit.
5. **SEMA és docstring (2. hatókör 4.)**; commit.
6. **Mz — mérés:** ugyanaz a 8 Strong az új kapuval (a fordítás nélküli bukások — Homérosz/Makk/Philo — eltűntek-e; más kapu
   nem lazult); a #142 már rögzített 5 Strongjának kapueredménye változatlan RENDBEN; `python eszkozok/ellenoriz.py` SÉRTÉS 0;
   `python eszkozok/feladatok.py ellenoriz` 0 hiba; `eszkozok/thayer_jelolt/teszt_*.py`, `eszkozok/teszt_forditas_kapuk.py`,
   `eszkozok/teszt_ellenoriz_13.py` zöld (a main-en is fennálló hash-eltérés külön jelölve).

⛔ Megállás, ha (i) a műcím-kivétel csak a hamis negatív kockázatával valósítható meg (a teszt nem tudja elválasztani a változatlan
átvételt a lefordítatlan folyó szövegtől); (ii) a ragozás-tűrés más besorolt sigla esetén hamis pozitívot ad (pl. a cél-alak egy
másik szó eleje), és ezt a mérés kimutatja; (iii) a 13. szabály Thayer-ága a 19 meglévő sor bármelyikén `forras_hash` eltérést
talál (ez adathiba, nem kódhiba): tétel a `DONTESEK.md`-be, helyőrzővel (`DT-F<nn>`).

## 4. Elfogadási feltételek

1. A 16. kapu a 2. hatókör 1. (a)–(c) szerint, mindhárom esetre pozitív és negatív teszttel; a meglévő `teszt_lanc.py` és
   `teszt_forditas_kapuk.py` tesztek változatlanul zöldek (a két állapotfüggő teszt kivételével, amely a 3. pont szerint módosul).
2. `python eszkozok/ellenoriz.py` SÉRTÉS 0 a #142 ágának `forditasok.tsv`-jén is (a 19 Thayer-sor forrásszövege megtalálva, hash egyezik);
   a `python eszkozok/ellenorzes/futtat.py` E19-e a #142 ágának tábláin 0 HIBA.
3. A 8 érintett Strong M0 / Mz kapueredménye a naplóban; a változás oka minden Strongnál megnevezve.
4. Proveniencia minden mérés mellett; a TSV-ket `split('\t')` olvassa (a `csv` modul tilos); `feladatok.py ellenoriz` 0 hiba.

## 5. Döntésnapló

| Pont | Döntés | Forrás |
|---|---|---|
| A javítás külön feladat, nem a #142 része | a #142 a #132 eszközeit nem módosíthatja (F142 brief 3. lépés ⛔) | DT-F142b (B), DT-F142c, DT-F142d javaslata; felhasználó, chat, 2026-10-26 |
| A 11. kapu / `APOKRIF_ALIAS` nem változik | a `Sir.` alakja `Sir` maradt (DT-F142b (A)); a `Makk`-ütközést a 16. kapu számjegy-tűrése oldja | felhasználó, chat, 2026-10-26 („Mindkettő igen”) |
