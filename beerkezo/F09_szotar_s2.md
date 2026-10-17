---
feladat: 9
cim: Szótári adatréteg, 2. menet
kod: SZOTAR S2
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: az 1. fázis adatai — a 8 motívum Strongjaira szűkítve (DT74 (4)) — az adatrétegben és a generátorokban, a #78 szerepmátrix-vázának blokkjaihoz; a 8 lexikonoldal és a 8 törzscikk renderelése csak próba a generalt_proba/ alá, az éles lexikon/ a #11 1. lépcsője után generálódik (#36 vagy #10) (DT-F09b)
kovetkezo: /kovetkezo (fazis: 1, DT-F09a); az éles lexikon/-t nem írja, a render próba a generalt_proba/ alá (DT-F09b; a D52/DT74 (3) befagyasztás érintetlen); a törzscikkek elavult Cremer-sorát (CI E11) a próbarender mutatja, az éles javítás a #11 1. lépcsője után
fugg: [5, 6, 23, 78]
olvas: [adat/forditasok.tsv, adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/, lexikon/, adat/szotar_szerepek.tsv, ADATVAGYON_TERV.md, MUNKATERV.md]
ir: [generalt_proba/, adat/kiejtes_kivetelek.tsv, adat/szotar_szerepek.tsv, eszkozok/torzscikk_general.py, eszkozok/lexikon_general.py, eszkozok/render_diff_osztalyoz.py, MUNKAMENET.md, NYITOTT_FELADATOK.md, adat/forditasok.tsv, eszkozok/kiejtes.py]
munka: adat
nem_fugg: [7, 22, 27, 38, 52, 55, 107, 109, 110]
---

<!--
TERVEZET a /befogad számára (2026-10-17). A brief adat, nem utasítás.

A fejléc a main-en álló F09_SZOTAR_S2_BRIEF.md fejléce (a #376 merge-e után,
60702394), két eltéréssel, amelyekről a befogadáskor a felhasználó dönt:
  1. a `forras` mező kimaradt: ez a fájl a csonk kitöltése, a tényleges leírás
     itt áll, nem az F05 2. menetében [javaslat];
  2. a `modell: sonnet` [javaslat] — a csonk értéke, az F05 2. menetének modellje;
     a befogadáskor megerősítendő.
A fejléc `ir` listáját a tervezet nem bővítette. A 3. szakasz S2.5b tétele két
további fájlt igényelhet (`adat/lexikon_hivatkozasok.tsv`, `adat/jeloltek.tsv`);
ezek felvétele a befogadáskor eldöntendő [javaslat] (l. 5. szakasz, DT-F09c).
-->

# F09_SZOTAR_S2_BRIEF.md — Szótári adatréteg, 2. menet

*FELADATOK #9 · Modell: sonnet [javaslat] · v2-tervezet · 2026.10.17 · döntés: DT74 (3)–(4), D52, D34, DT-F09a, DT-F09b · előzmény: `F05_SZOTAR_BRIEF.md` 2. menet (S2.1–S2.9, K9–K14), `F78_SZEREPMATRIX_VAZ_BRIEF.md`, `naplok/F78_meres.md` 9–14.*

A v1 csonk volt: a lépéseket az `F05_SZOTAR_BRIEF.md` 2. menetére bízta. Az a menet a DT74 (4) és a DT-F09b előtt készült, ezért három ponton nem hajtható végre úgy, ahogy le van írva:

- az **S2.8** az éles `lexikon/`-t generálja újra, a **K13** a `lexikon/`-on méri a CI E11-et. Ezt a DT74 (3) / D52 a #11 1. lépcsőjéig befagyasztja, és a DT-F09b (b) szerint a #9 csak próbát renderel a `generalt_proba/` alá;
- a hatókört nem szűkíti a 8 motívum Strongjaira (DT74 (4)), és nem a #78 szerepmátrix-vázának blokkjait tölti, mert a váz akkor még nem létezett;
- az **S2.6** azóta leválasztott feladat (#70, felhasználói döntés, 2026.10.06).

Ez a brief az S2.1–S2.9-et ehhez igazítva veszi át. A „[javaslat]” jelölésű pontokat a források nem döntik el egyértelműen; ezekről a felhasználó dönt (a befogadáskor vagy a megjelölt ⛔ pontnál).

## 1. Cél

A szerepmátrix (`adat/szotar_szerepek.tsv`) `nincs adatosítva` szerepeit a 8 lexikon-motívum (ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001) Strongjaira adatból töltsük fel, és a generátorok ezt a #78 vázának szerep-blokkjaiban rendereljék. Az adat a meglévő, az 1. menetben (#5) importált és jóváhagyott forrásokból jön: kiejtés-kivételek, TBESH-konszolidált, UBS DBH, Mounce/SECE, tW + TWOT-szám, BDB-etimológia, LXX versszintű párok. A szerep, amelynek nincs forrása, `nincs forrás` (F05 D27); amelynek a forrásában nincs szócikk, ott `a forrás nem tárgyalja` (F05 D11). Hiányt nem pótolunk gyenge anyaggal (CLAUDE.md 3. szabály).

A 8 lexikonoldal és a 8 törzscikk renderelése **csak próba** a `generalt_proba/` alá, diff-osztályozással az éles állapothoz képest. Az éles `lexikon/` nem változik; a #11 1. lépcsője után a #36 vagy a #10 generálja (DT-F09b). A D34 mondata („a törzscikk utoljára itt generálódik”) ezzel a #9 próbarenderére módosul (DT-F09b indoklása).

## 2. Hatókör

**Benne van**

- **Adatréteg:** a 26 jóváhagyott héber lemma-kiejtés rögzítése az `adat/kiejtes_kivetelek.tsv`-be (F05 S2.1); a `szotar_szerepek.tsv` `allapot` és `forras` oszlopa (F05 S2.7); az új glossza- és szócikk-fordítások gyorsítótár-sorai az `adat/forditasok.tsv`-ben (`kezi` vagy `fordításra vár`, l. S2.4–S2.5).
- **Generátorok:** `eszkozok/lexikon_general.py` és `eszkozok/torzscikk_general.py` — a #78 vázának szerep-blokkjait tölti (F05 S2.1–S2.5, S10); a kódbeli `KIEJT` tábla megszűnik (F05 D15); az N-F78a javítása (a `torzscikk_general.py --kimenet` a kimeneti könyvtár lexikonoldalából olvasson); `eszkozok/kiejtes.py` igazítása, ha az S2.1 igényli; `eszkozok/render_diff_osztalyoz.py` új kategóriái (F05 S2.8).
- **Hatókör-szűkítés (DT74 (4)):** a render és az új adatsorok a 8 motívum Strong-tokenjeire. A tokenhalmaz a menet indító commitján mérve (az F05 D28 hatókör-szabálya, a 8 motívumra alkalmazva); a §0 méri.
- **Próbarender:** a 8 `_TUDOMANYOS` és a 8 `_TORZSCIKK` a `generalt_proba/F09_szotar_s2_proba/lexikon/` alá (`general.py … --kimenet`), és a diff-osztályozó jelentése az éles `lexikon/`-hoz képest.
- **Lezárás:** `NYITOTT_FELADATOK.md`, `MUNKAMENET.md`, a saját brief fejléce.

**Nincs benne**

- **az éles `lexikon/` írása** (DT-F09b (b), DT74 (3), D52). Az éles `_TORZSCIKK`-ek Cremer-sora (CI E11, F02 D12) ezért ebben a menetben az éles fájlban megmarad; a próbarender mutatja, hogy a generátor már nem írja;
- **az S2.6** (ISTENTISZT-001 2/b a tanulmányban, F05 S12, K12): leválasztott feladat, **#70** (`munka: ertelmezo`, befagyasztva a #11 1. lépcsőjéig). A `tematikus_lezart/` fájlt a #9 nem írja;
- **a TEREMT-002** (9. motívum) szótári része és lexikonoldala: a #12b. A DT74 (4) a 8 motívumra szűkít; a H8414/H0922 sorsát l. S2.1 és S2.5b [javaslat];
- a fordítási pipeline éles futtatása (#7); a hiányzó fordítások `fordításra vár` jelölést kapnak, gépi fordítás nem fut;
- BDB SQLite-csere, héber gépi kiejtés, Trench, Girdlestone (F05 D18), Cremer (F05 D16);
- az LXX-fordítói döntések a függő igehelyekre (#8);
- a 13–14. szerep (Károli-megfelelők, rejtett/hamis párhuzam) és a 12. (Nave) adatosítása: `javaslat` marad (a 13. a #22-re épül, DT76 (9));
- a `FELADATOK.md` generált blokkja (csak a `main`-re futó Action írja).

## 3. Lépések (⛔ a kötelező megállások)

Első lépés a modell-ellenőrzés (CLAUDE.md): a tényleges modellnév kiírása és összevetése a fejléc `modell` mezőjével; eltérésnél nincs munka.

**Közös szabályok minden lépésre.** TSV olvasása `split('\t')`, írása `'\t'.join()`, `csv` modul nélkül; táblát író lépés előtt a sorok összevetése az eredetivel, eltérésnél megállás (minta: `eszkozok/igazolas_migracio.py`). Héber/görög/magyar szöveget tartalmazó kód csak fájlból fut. Minden lekérdezésből származó számhoz proveniencia-sor (`scope=… | forras=… | ts=…`). Minden `--kimenet` próba a `generalt_proba/F09_szotar_s2_proba/` alá megy (verziózott, nem scratch); a köztes, eldobható futások ideiglenes könyvtárba, a repón kívülre. **Az éles `lexikon/` egyetlen lépésben sem íródik.**

### S0 — kiindulás *(csak olvas)* ⛔

- **S0.1** `main` = `origin/main`; új ág a `main`-ről.
- **S0.2** Mérés, a `naplok/F09_S0_kiindulas.md`-be, proveniencia-sorral:
  1. a 8 motívum Strong-tokenhalmaza az `elofordulasok.tsv`-ből (H és G darabszám, listával); összevetés az F05 §0 0.4 sorával (H 26, G 13, ebből 2 H a TEREMT-002-é, F05 D29). A várt érték H 24, G 13; eltérésnél a D28-szabály a 8 motívumra: új token bekerül, kieső token vagy G-változás → ⛔;
  2. `adat/kiejtes_kivetelek.tsv` sorai (a tervezéskor: az 5 `KIEJT`-sor, `manual`), `grep -c KIEJT eszkozok/torzscikk_general.py`;
  3. `adat/szotar_szerepek.tsv` állapotai (a tervezéskor: 26 sor; `nincs adatosítva`: görög 3, 7, 10; héber 3, 5, 7, 8, 9, 10; `javaslat`: 12–14. mindkét nyelven; `manual`);
  4. a `konkordancia/` 1. menetes importjai megvannak-e és a README-beli SHA egyezik-e: `TBESH_konszolidalt.tsv`, `UBS_DBH_jelentesek.tsv`, `UBS_DBH_referenciak.tsv`, `MCGED_teljes.tsv`, `BDB_etimologia_kezi_hatarok.tsv`, `tW_szocikkek.tsv`, `LXX_versszintu_parok.tsv`; a tW- és az LXX-pár-import elfogadása a `naplok/SZOTAR_S0b_jelentes.md` szerint (F05 S13/S14 feltétele);
  5. `python eszkozok/kiejtes.py --ellenoriz` görög egyezése az aranykészleten (F05 D23: 50 pár, kapu 100%);
  6. N-F78a állapota (`NYITOTT_FELADATOK.md`): nyitott-e;
  7. az éles `lexikon/` mai `_TUDOMANYOS` és `_TORZSCIKK` fájljainak hash-e (a végén ugyanezt kell visszakapni).
- ⛔ **Megállás, ha** a tokenhalmazból token esik ki vagy a G-halmaz változik; egy import hiányzik vagy a SHA eltér; a görög egyezés < 100% (az S2.1 kapuja).

### S2.1 — kiejtés *(F05 S2.1, F05 K9)*

- A görög aranykészlet 100%-os egyezése után: a jóváhagyott héber lemma-kiejtések rögzítése az `adat/kiejtes_kivetelek.tsv`-be (forrás: `naplok/SZOTAR_S1_heber_jeloltek.tsv`, F05 D34–D37; a H2555 kivétele *hámás*, F05 D36). A jelöltlistából csak a jóváhagyott érték kerül át, változtatás nélkül; a táblába írás előtt sor-összevetés.
- **[javaslat] A H8414 és a H0922 (TEREMT-002, F05 D29):** a jóváhagyás mind a 26 lemmára megvan (2026.09.29), a DT74 (4) viszont a 8 motívumra szűkít. Két út: (a) mind a 26 bekerül (a jóváhagyott adat előbb készül, mint a render, F05 D29 indoklása; a render csak a 8 motívumét használja); (b) csak a 8 motívum 24 lemmája, a kettő a #12b-re vár. A brief nem dönt; a §0 ⛔-nél a felhasználó választ.
- Görög kiejtés a generált blokkokban (lemma és alak), a tisztított átírás-lista szerint (F05 S3, D4); héber lemma a kivételtáblából; héber alak STEP-átírás, változatlanul. A kiejtés a #78 vázának 10. szerepe alá kerül (DT81).
- A `torzscikk_general.py` kódbeli `KIEJT` táblája megszűnik (F05 D15).

### S2.2 — TBESH *(F05 S2.2, S4)*

- A héber 1. szerep (Alapjelentés) a `konkordancia/TBESH_konszolidalt.tsv`-ből (unió, a forrás soronként jelölve; F05 D3, D38). A forrásblokk belső szövege a #78 renderének mintáját követi (`_szotar_reszek`).
- A H7121 mutatója a BDB 2.c-re marad (DT-F42a, DT83); a TBESH „részlet” sora nem kerül vissza.
- A H8034 `adatosítva, nincs bekötve` állapotának feloldása: l. S2.5b.

### S2.3 — UBS DBH *(F05 S2.3, S5, S10)*

- A héber 5. szerep (Tömör jelentés, előfordulás) és a 9. (Versenkénti jelentés) a `UBS_DBH_jelentesek.tsv` / `UBS_DBH_referenciak.tsv`-ből, az ÚSZ-oldali UBS DNTG mintájára (F05 S10). A definíció és a glossza magyarul a gyorsítótárból; ha nincs sor, `fordításra vár` (gépi fordítás nem fut, #7).
- A `UBS_DBH_anomaliak.tsv` sorait a render nem használja forrásként [javaslat: a §0 jelenti a 8 motívum tokenjeire eső anomáliákat; ha van ilyen, ⛔].
- A tokenen, amelynek nincs UBS DBH-szócikke: `a forrás nem tárgyalja` (F05 D11, D28).

### S2.4 — Mounce és SECE *(F05 S2.4, S6)*

- A görög 5. szerep kiegészítője a Mounce (`MCGED_teljes.tsv`, GK-szám és tömör glossza; szó szerinti megjelölés kötelező, F05 S6); a 7. szerep (Megfelelők a másik nyelven) mindkét nyelven a SECE megfelelő-listájából. Az L–N mező csak keresztellenőrzés az UBS DNTG ellen (eltérés = JELENTÉS, F05 D7).
- A Mounce angol glosszái magyarul a gyorsítótárból; a hiányzó `fordításra vár`.
- **[javaslat] A 2/b 3 kézi glosszája.** Az F05 S2.4 szerint a 2/b-ben meglévő 3 magyar glossza `kezi` sorként átkerül a gyorsítótárba. Ez a forrásból (ISTENTISZT-001 tanulmány) adatréteg felé mozgó kinyerés: a DT28 szerint csak a `jeloltek.tsv`-n át, `manual` provenienciával, döntéssel mehet, a DT74 (3) pedig a régi forrásréteget befagyasztja. A 2/b átírása a #70-é. A brief nem dönt: (a) a 3 glossza a #9-ben `kezi` sorként átkerül, a 2/b érintetlen; (b) a 3 glossza a #70-re (vagy a #11 szétválasztására) vár, a #9-ben `fordításra vár`.
- A #78 renderében a 7. szerep ma „l. 2/b” hivatkozás (`SZEREP_KEZI_2B`, DT82 3.). **[javaslat]** Ha a SECE-blokk töltődik, a hivatkozás helyére a SECE-adat kerül, a 2/b-re mutató sor megszűnik vagy kiegészítő mutató marad; a felhasználó dönt (a 2/b próza a #70-ig változatlan).

### S2.5 — teológiai szócikk, nyelvi háttér, LXX *(F05 S2.5, S8, S9, S13, S14)*

- **3. szerep:** tW (`tW_szocikkek.tsv`), ha az S0b nyelvenként elfogadta (F05 S14, D20); a héber 3. szerepben a TWOT-szám hivatkozásként (F05 D19, a D17 kivétele). Az angol szöveg mellé a magyar a gyorsítótárból; ha nincs, `fordításra vár`. Ha a tW egy nyelven el lett utasítva: görögül `nincs forrás`, héberül csak a TWOT-szám.
- **Héber 8. szerep:** BDB-etimológia (`BDB_etimologia_kezi_hatarok.tsv` és a gépi határ; csak `gepi` és `jovahagyott`, F05 D41); a `nem_targyalja` tokenen `a forrás nem tárgyalja`.
- **LXX versszintű párok** (`LXX_versszintu_parok.tsv`, ha importálva): a 6. szerep kiegészítőjeként, „versszintű együtt-előfordulás, nem szóillesztés” jelöléssel (F05 S13, D25). A #78 ma a 6. szerepnél a 3. szakaszra hivatkozik; [javaslat] a versszintű párok a hivatkozás mellé, külön sorban kerülnek, nem helyette.

### S2.5b — a #78 által a #9-re hagyott bekötések *(új tétel, a #78 nyomán)* ⛔

A #78 zárása (DT82, DT83; `naplok/F78_meres.md` 12–14.) két bekötést a #9-re hagyott; az F05-ben ezek nem szerepelnek.

- **H8034, héber 1. szerep (ISTENTISZT-001):** a TBESH-sor bekötése a `lexikon_hivatkozasok.tsv`-be. Akadály (F78 mérés 12/2): a `jeloltek.tsv` kulcsa `id` + `igehely`, a szótári szócikknek nincs igehelye, így a jelölt-sor sémasértés nélkül nem írható; a precedens (F6.3) jelölt nélkül, szó szerinti részsztring-ellenőrzéssel kötött be. **[javaslat]** A bekötés útja és a két fájl (`adat/lexikon_hivatkozasok.tsv`, `adat/jeloltek.tsv`) felvétele az `ir`-be a felhasználó döntése (l. 5. szakasz DT-F09c); döntés nélkül a H8034 `adatosítva, nincs bekötve` marad, és a próbarender ezt mutatja.
- **TEREMT-002 héber 1–2. szerep** (`adatosítva, nincs bekötve`, „a #9 köti be”): a DT74 (4) a 8 motívumra szűkít, a TEREMT-002 lexikonoldala a #12b. **[javaslat]** a bekötés a #12b-re kerül, a #78 próbafájl „#9”-mutatója ennek megfelelően a #12b-re javul (a #9 csak a mutató szövegét javítja a generátorban); vagy a #9 köti be, a DT74 (4) alóli kivételként. A felhasználó dönt.
- ⛔ **Megállás e tétel elején**, a döntések nélkül nem ír adatot.

### S2.6 — *(nincs benne: #70)*

Az ISTENTISZT-001 2/b átírása (F05 S12, K12) a #70 feladata. A #9 a tematikus tanulmányt nem írja; a próbarender a tanulmány mai állapotából dolgozik, ezért a `tanulmany` diff-kategória üres is lehet.

### S2.7 — szerepmátrix, lábléc, kolofon *(F05 S2.7, S11)*

- `adat/szotar_szerepek.tsv`: az S2.1–S2.5 szerint töltődő szerepek `allapot`-ja `adatosítva`, a `forras` pontosítva; ahol a forrás nem áll rendelkezésre, `nincs forrás` (F05 D27). A 12–14. szerep `javaslat` marad. Táblát író lépés előtt sor-összevetés; a SEMA 2.13 szövegét a változás nem érinti [javaslat: ha mégis, az `adat/SEMA.md` felvétele az `ir`-be a befogadáskor].
- Lábléc és kolofon az F05 S11 szerint: Mounce (kötelező megjelölés), SECE, UBS DBH (CC BY-SA 4.0, a ©-mondat szó szerint), TWOT (csak a szám, a mű megnevezésével), tW (CC BY-SA 4.0; az unfoldingWord® védjegy a származékos szövegben nem szerepel, a módosítás jelezve, a forrásmegjelölés szó szerint: „The original work by unfoldingWord is available from unfoldingword.org/utw”).

### S2.8 — próbarender és diff-osztályozás *(F05 S2.8, DT-F09b szerint igazítva)* ⛔

- **N-F78a javítása előbb:** a `torzscikk_general.py --kimenet` a kimeneti könyvtár lexikonoldalából olvasson, ha van (különben a próba-törzscikk az éles, befagyasztott oldalra épülne, és a két próbafájl ellentmondana). Igazolás: a próba-törzscikk lefedettségi mátrixa a próba-lexikonoldallal egyezik.
- Próbarender: `general.py --cel lexikon` és `--cel torzscikk`, a 8 motívumra, `--kimenet generalt_proba/F09_szotar_s2_proba` (azonos `PARDES_DATUM`-mal, F05 D30). Az éles `lexikon/` nem íródik; a §0.2/7 hash-ei a végén változatlanok.
- `render_diff_osztalyoz.py`: a próba és az éles `lexikon/` különbsége kategóriákba. Új kategóriák (F05 S2.8): `kiejtes`, `tbesh`, `ubs_dbh`, `mounce_sece`, `teologiai`, `nyelvi_hatter`, `lxx_korpusz`, `licenc`, `szerep` (a meglévő `tanulmany` stb. mellé). [javaslat] Külön kategória a #78-váz miatti eltérésre (az éles oldal még a régi, Strong-sorrendű 2. szakaszt mutatja), pl. `szerep_vaz`; e nélkül a vázváltás minden sora `szerep`-be esne, és elfedné az adatváltozást. Kimenet: `naplok/SZOTAR_S2_diff.tsv`.
- ⛔ **Megállás, ha** a diff-osztályozó ismeretlen kategóriát talál, vagy az éles `lexikon/` bármely fájlja változott.
- A próbarenderben a 8 törzscikk Cremer- és Girdlestone-említése 0 (a CI E11 szabálya a próbán, kézi méréssel; az E11 hatóköre a `lexikon/`, F02 D12, a `generalt_proba/`-t a CI nem nézi [javaslat: a mérés szkripttel, proveniencia-sorral a zárójelentésben]).

### S2.9 — lezárás *(F05 S2.9)*

- `NYITOTT_FELADATOK.md`: a fordítási pipeline (#7); BDB SQLite-csere; héber gépi kiejtés; a Thayer- és (ha van) a tW-szócikkek, a Mounce-glosszák fordítása (`fordításra vár` sorok száma); Trench; javaslat: a CI E11 kiterjesztése a Girdlestone-ra; az N-F78a lezárása; az éles `lexikon/` újragenerálása a #11 1. lépcsője után (#36/#10), az éles törzscikkek Cremer-sorával. Új tétel csak helyőrzővel (`N-F09a`, …).
- `MUNKAMENET.md`: ha a menet a munkamenetben új tanulságot hozott [javaslat: csak akkor írja, egyébként érintetlen].
- A saját brief fejléce (`allapot`, `kovetkezo`, `ag`, `pr`); a `FELADATOK.md` generált blokkját a #9 nem írja.
- Független ellenőr (`fuggetlen-ellenor`, `naplok/ELLENOR_SZOTAR_S2.md`), PR. Merge csak a felhasználótól.

**Commitok, tétel-szintű granularitással** (CLAUDE.md): `S0:`, `S2.1:`, `S2.2:`, … `S2.9:` külön; az üzenet UTF-8 fájlból (`git -c i18n.commitEncoding=UTF-8 commit -F …`).

## 4. Elfogadási feltételek

Az F05 K9–K14-ből, a DT-F09b és a DT74 (4) szerint igazítva.

| # | Feltétel | F05-előzmény |
|---|---|---|
| K9 | Az S2.1 csak 100%-os görög aranykészlet-egyezés után futott; `grep -c KIEJT eszkozok/torzscikk_general.py` = 0; az `adat/kiejtes_kivetelek.tsv` a 8 motívum §0-ban mért összes héber lemmáját tartalmazza (várt: 24) (a H8414/H0922 az S2.1 döntése szerint) | K9 |
| K10 | Diff-osztályozó: ismeretlen kategória 0; a kategóriák darabszáma jelentve (`naplok/SZOTAR_S2_diff.tsv`) | K10 |
| K11 | A lábléc és a kolofon az S11 szerint; a Mounce, az UBS és (ha van) a tW megjelölése szó szerint; az unfoldingWord® védjegy a származékos szövegben nem szerepel — a próbarenderen mérve | K11 |
| K12 | *(a #70-hez tartozik; ebben a menetben nincs)* | K12 |
| K13 | `ellenoriz.py` SÉRTÉS 0, kód 0; a **próbarender** 8 törzscikkében `nincs adatosítva` 0 (a `nincs forrás` és a `javaslat` szerep megengedett), Cremer- és Girdlestone-említés 0 (a CI E11 szabálya a `generalt_proba/F09_szotar_s2_proba/`-n mérve); a CI zöld | K13 (a `lexikon/` helyett a próba) |
| K13b | **Az éles `lexikon/` bájtra változatlan** (a §0.2/7 hash-ei egyeznek; `git diff --stat lexikon/` üres) | új (DT-F09b) |
| K13c | A render a #78 vázának szerep-sorrendjét és üres-blokk jelölését (DT80 B, `ÜRES-NYELV`, `adatosítva, nincs bekötve`) megtartja; `eszkozok/teszt_szerepmatrix.py` zöld | új (DT74 (4)) |
| K13d | Új adatsor és render csak a 8 motívum Strong-tokenjein (DT74 (4)); a §0 tokenlistáján kívüli tokenre írt sor 0 (a S2.1/S2.5b döntése szerinti kivétellel) | új (DT74 (4)) |
| K13e | Az N-F78a javítva: a próba-törzscikk a próba-lexikonoldalból olvas, a két próbafájl lefedettségi mátrixa egyezik | új (N-F78a) |
| K13f | Kitöltetlen szerep sehol nincs gyenge vagy asszociatív anyaggal pótolva; a hiányzó fordítás `fordításra vár`, nem gépi | új (3. szabály) |
| K14 | TSV-kezelés `csv` modul nélkül; commitok tétel-szinten; `git status --porcelain` üres; `python eszkozok/feladatok.py ellenoriz` 0 hiba; független ellenőr jelentése eltérés nélkül | K14 |

## 5. Döntésnapló

- **DT74 (3)–(4), D52** — befagyasztás a #11 1. lépcsőjéig; a #9 hatóköre a 8 motívum Strongjai, a #78 blokkjait tölti — **rögzített**.
- **DT-F09a** — a #9 `fazis: 1` — **rögzített** (2026-10-17).
- **DT-F09b** — a #9 csak adatréteget és generátort ír, a render próba a `generalt_proba/` alá — **rögzített** (2026-10-17).
- **#70 leválasztása** (S2.6, felhasználói döntés, 2026.10.06) — **rögzített**.
- `DT-F09c` *(helyőrző, nyitott)* — a H8034 TBESH-bekötés útja és a TEREMT-002 héber 1–2. szerep helye (S2.5b); vele az `adat/lexikon_hivatkozasok.tsv` / `adat/jeloltek.tsv` felvétele az `ir`-be.
- `DT-F09d` *(helyőrző, nyitott)* — a H8414/H0922 kiejtése a `kiejtes_kivetelek.tsv`-be kerül-e (S2.1).
- `DT-F09e` *(helyőrző, nyitott)* — a 2/b 3 kézi glosszája a #9-ben vagy a #70/#11-ben kerül át (S2.4); a 7. szerep „l. 2/b” mutatójának sorsa.

*A `DT-F09c`–`e` helyőrző (a meglévő `DT-F09a`/`b` folytatása); végleges számot a `szamkiosztas` Action ad merge után.*
