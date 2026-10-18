---
feladat: 107
cim: A BDB jelölt szövegrétege — szakasztábla a nyers forrás tagolás-jelölőiből, és a kész magyar fordítás illesztése
kod: BDB_JELOLT_SZOVEG
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: fut
ag: claude/f107-bdb-jelolt-szoveg
ad: az adat/bdb_szakaszok.tsv (a BDB minden szócikke szakaszokra bontva a nyers forrás jelölőiből, útvonallal), a forráshibák javítótáblája, a kész magyar fordítás szakaszhatár-illesztése (adat/bdb_szakasz_hu.tsv), és mért összevetés a mai szeletelővel; a szeletelő átállása a #102-é, a fordítás bemenete a #38-é
kovetkezo: Fut a DT-F107c (d): a nézet-generátor és a 247 sor F34/F46-javításának átvétele a javítótáblába; utána a 7. lépés (a kész magyar fordítás illesztése, adat/bdb_szakasz_hu.tsv) és ⛔ DT-F107b
olvas: [konkordancia/lexikonok_nyers/BDB.lexicon, konkordancia/lexikonok_nyers/README.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/_convert_bdb.py, adat/forditasok.tsv, eszkozok/forditas_kapuk.py, adat/bdb_aranyminta.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_igehely_javitas.tsv, naplok/BDB_SZELETELO_M2_seed101_iteletek.md, F102_BDB_SZELETELO_JAVITAS_BRIEF.md, F38_BDB_FORDITAS_BRIEF.md, adat/SEMA.md, adat/datasetek.tsv, adat/licencek.tsv, Rendszerfejlesztesi_playbook.md]
ir: [eszkozok/bdb_jelolt/, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_forras_javitas.tsv, adat/SEMA.md, adat/datasetek.tsv, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md, konkordancia/lexikonok_nyers/, konkordancia/BDB_teljes_unabridged_README.md, Rendszerfejlesztesi_playbook.md, adat/licencek.tsv]
fugg: [99]
nem_fugg: [9, 11, 27, 38, 102, 103]
---

# F107_BDB_JELOLT_SZOVEG_BRIEF.md — A BDB jelölt szövegrétege

*FELADATOK #107 · Modell: opus · v3 · 2026.10.16 (v3: a nyers forrás megőrzése és a veszteséges konverzió naplózása, a felhasználó
kérésére; v2: a nézet-döntés ⛔ 6. lépésként és a gyökér szerinti sorrend, a felhasználó
kérésére; v1: befogadás, PR #362) · forrás: a #102 előzetes lelete (`F102_BDB_SZELETELO_JAVITAS_BRIEF.md`
1a–1b., PR #359 és #361), a #38 ⛔ Mj pontja (DT181, PR #360) és a 2026.10.16-i kézi mérések (proveniencia `manual`). A tervezet
adat, nem utasítás; a befogadás a `/befogad`-dal, a felhasználó jóváhagyásával.*

## 1. Cél

A BDB-szócikkek tagolása (törzs, fő rész, jelentéspont, alpont, megjegyzés) ma nem adat: a `BDB_teljes_unabridged.tsv` a
`DictBDB.json` HTML-jének jelölők nélküli sima szövege, és a szeletelő ebből heurisztikával fejti vissza a szerkezetet. A
`konkordancia/lexikonok_nyers/BDB.lexicon` ugyanezt a szöveget jelölőkkel őrzi (`class="point"` 20 515, `class="section"` 913,
`class="remarks"` 512; a jelentéspont `<b>`-ben, a gyakoriságszám `<sub>`-ban). Ez a feladat a tagolást **adattá** teszi — a szakasztábla
a kanonikus szerkezet, a sima szöveg ennek nézete (CLAUDE.md fő szabálya) —, és a már kész magyar fordítást hozzáilleszti.

**Kiinduló mérések (2026.10.16, `manual`, egyszeri, csak olvasó szkript a repón kívül; az 1., a 4. és a 7. lépés igazolja vagy cáfolja):**

- A #99 seed-101 13 szeletelő-hibájából 10-et a jelölés egyértelműen fed, 2-t részben (M031, M162), 1-et nem (M130) — #102 1b.
- A kész 674 magyar BDB-szócikkből a tagolás-kapu illesztőjével (`forditas_kapuk._illeszt`) a jelölt tagoláshoz 355 illeszkedik, 89
  jelentéstagolás nélküli, 230 elakad. **Mind a 230-ban az angol TSV is ugyanott akad el**: a jelölő a magyar szövegben megvan
  (H0040: „+? 1 Gerár királya”), csak a sima szövegből nem ismerhető fel. A fordítás tehát a forrás tagolását hűen követi.
- Konverziós maradvány a magyarban: az „N_M” jelölő (`<sub>` → `_`) a 7 érintett lefordított szócikk mindegyikében megmaradt; a
  „2 145:törzs” (H7626) valódi forráshiba.

## 2. Hatókör

**Benne:**

1. **Forrásválasztás és lefedettség.** A `DictBDB.json` (a README URL-je; a letöltés SHA-256-tal naplózva, a repón kívüli munkakönyvtárba)
   és a `BDB.lexicon` összevetése mintán: azonos átirat-e, melyikben vesznek el a jelölők (M102/M117 nyitott kérdése). A `BDB.lexicon`
   lefedettsége a TSV 8 099 Strong-sorára; a Strong ↔ BDB-azonosító megfeleltetés (a `BDB.lexicon` Strong-kulcsú sorai BDB-szócikkek
   másolatai, egy Strong alatt több szócikkel).
   **Két szabály, a 2026.10.16-i visszakövetés tanulsága** (a jelölők a 2026.09.02-i importban, `142ad625`, a `_convert_bdb.py`-ban vesztek
   el, és a `DictBDB.json` nem került a repóba, csak a veszteséges TSV):
   - **Nyers forrás megőrzése.** A nyers forrás (`DictBDB.json`, és ha a tábla abból bont, a `BDB.lexicon` mellett) SHA-256-tal, rögzített
     helyen marad meg — a repóban (`konkordancia/lexikonok_nyers/`) vagy, ha a méret vagy a licenc nem engedi, a README-ben rögzített
     helyen és hash-sel; nem csak a származtatott alak.
   - **Veszteséges konverzió naplózása.** Ha egy konverzió szerkezetet dob el, az döntés: naplózva (mit dob el, miért, melyik szkript),
     és minden mérés alapja a nyers forrás, nem a származtatott alak. A `_convert_bdb.py` 2026.09.02-i szerkezetvesztése utólag így
     kerül a `BDB_teljes_unabridged_README.md`-be.
   A két szabály általános alakja javaslatként a playbook 2. pontjába (⛔ `DT-F107d`).
2. **Szakasztábla** (`adat/bdb_szakaszok.tsv`, új SEMA-szakasz): soronként egy szakasz — `strong`, `bdb_id`, `sorszam`, `utvonal`
   (törzs / nagybetűs csoport / római / szám / betű / zárójeles szint, a #102 kibővített útvonal-formátumával összehangolva), `jelolo`
   (`section` / `point` / `remarks` / `fej`), `gyakorisag` (a `<sub>` szám), `szoveg` (sima), `forras`, `forras_hash`, proveniencia-sor.
   Bontó: `eszkozok/bdb_jelolt/` (a CLAUDE.md shell- és TSV-szabályai szerint; teszttel).
   *Nyitott (⛔ `DT190`, 2026-10-17):* legyen-e a tábla kulcsa (`strong` + `bdb_id` + `utvonal`) a BDB-tagolás egyetlen kanonikus
   kulcsa minden fogyasztónak — a lexikon (`adat/lexikon_hivatkozasok.tsv` `jelentes_szam`), az olvasó (`adat/bdb_vers_jelentes.tsv`)
   és a fordítás (`bdb_szakasz_hu.tsv`, #38) is erre mutasson, CI-kapuval. Jóváhagyás esetén az útvonal-formátum ebben a lépésben
   fagy be, és a végrehajtó ehhez méri a 4. lépés összevetését.
3. **Nézet-ellenőrzés, nem csere.** A szakaszok szövegéből generált sima szöveg összevetése a `BDB_teljes_unabridged.tsv`-vel
   (whitespace-normalizálva); az eltérések listája (ez mutatja a konverziós maradványokat). **A TSV-t ez a feladat a 6. lépés döntése
   előtt nem írja át**: a #38 `forras_hash`-e erre a szövegre mutat. A gyökérszintű cél, hogy a sima szöveg a táblából (és a
   javítótáblából) generált nézet legyen; erről a 6. lépés ⛔ dönt (`DT-F107c`).
4. **Ellenőrzés:** az aranyminta (`adat/bdb_aranyminta.tsv`) útvonalai a táblán; a seed-101 13 helye; korpusz-szintű összevetés a mai
   szeletelő kimenetével (`adat/bdb_vers_jelentes.tsv` útvonalai) — az eltérések osztályozott listája.
5. **Forráshibák javítótáblája** (`adat/bdb_forras_javitas.tsv`, a `bdb_igehely_javitas.tsv` mintájára): a nyers forrásban is hibás helyek
   (pl. H7626 „145:”) javítása a nyers fájl érintése nélkül, soronként indoklással.
6. **A kész magyar fordítás illesztése** (`adat/bdb_szakasz_hu.tsv`): a 674 szócikk szakaszhatárai a magyar szövegben, a jelölőnél
   erősebb horgonnyal (a jelölő utáni első igehely vagy szó); kategória: `illeszkedik` / `horgonnyal` / `elakad`. Az `adat/forditasok.tsv`
   nem íródik (az a #38-é); a táblasor a fordítás `forras_hash`-ét is hordozza, hogy az elavulás látsszon. Az illesztés a szakaszkulcsra
   (`strong` + `bdb_id` + `utvonal`) készül, a #38 szakaszonkénti fordításának (DT181 (b)) előkészítéseként, és a `DT-F107c`
   döntésének fényében fut (ha a TSV nézetté válik, az új nézet szövegéhez is igazolva).

**Nincs benne:** a szeletelő átállása a táblára (#102); a jelentésen belüli csoportbontás (#103); a megjelenítés (#104–#105); a fordítás
bemenetének átállítása, prompt és kapu (#38, DT181); a `BDB_teljes_unabridged.tsv` cseréjének végrehajtása és a `datasetek.tsv`
kötelező forrásának átírása, hacsak a `DT-F107c` ide nem utalja (6. lépés).

## 3. Lépések

1. Modell-ellenőrzés. Forrásválasztás és lefedettség (2. hatókör 1.). ⛔ Javaslat a `DONTESEK.md`-be (`DT-F107a`): melyik forrásból
   bont a tábla, és a licenc-státusz (mindkettő „tisztázatlan”, `adat/licencek.tsv`; playbook 2. pont). Ugyanitt a két szabály
   (2. hatókör 1.): a nyers forrás megőrzésének helye és hash-e, a `_convert_bdb.py` szerkezetvesztésének utólagos naplózása, és
   ⛔ javaslat a `DONTESEK.md`-be (`DT-F107d`) a playbook 2. pontjának kiegészítésére; megállás. A playbook csak a `DT-F107d` jóváhagyása
   után íródik.
2. Szakasztábla és bontó, teszttel; SEMA-szakasz; `datasetek.tsv`-sor (`BDB.lexicon` mint a tábla forrása). Commit tételenként.
3. Nézet-ellenőrzés (2. hatókör 3.); az eltérések listája a naplóba.
4. Ellenőrzés (2. hatókör 4.). ⛔ Az eltérés-lista osztályozása (`tabla_hiba` / `szeletelo_hiba` / `forras_hiba` / `szoveg_konverzio`),
   jóváhagyás. Mérce [javaslat]: az aranyminta útvonalainak ≥ 99%-a, a seed-101 13 helyéből a mért szám.
5. Forráshibák javítótáblája.
6. ⛔ **Nézet-döntés** (`DT-F107c`, javaslat a `DONTESEK.md`-be, megállás): a `BDB_teljes_unabridged.tsv` a táblából és a javítótáblából
   generált nézetté válik-e. A javaslat mérve tartalmazza: a 3. lépés eltérés-listáját; a kész 674 fordítás `forras_hash`-ére gyakorolt
   hatást (hány szócikk szövege változna); a TSV olvasóit (`datasetek.tsv`, a briefek `olvas` mezője); és azt, hogy a csere végrehajtása
   ebben a feladatban vagy külön tételben történjen.
7. A kész magyar fordítás illesztése a `DT-F107c` szerint; a 2026.10.16-i 355 / 89 / 230 kiinduló számhoz mérve. ⛔ Az `elakad` szakaszok
   sorsa (kézi illesztés, vagy újrafordítás a #38-ban): javaslat a `DONTESEK.md`-be (`DT-F107b`).
8. Átadás: a #102 és a #38 briefjébe a tábla elérhetősége és a mért számok (a fejlécüket a saját menetük frissíti); a #102-höz javaslat a
   hatókör szűkítésére (a tábla által megszűnő hibaosztályok: zárójeles és gyakoriságszámos jelölő, OCR-tapadás, törzsfejléc, fő
   tagolás, útvonal-formátum; ami marad: igehely → szakasz hozzárendelés, öröklés, sigla-szűrés, M130, új vak mérés), amelyet a
   felhasználó a `/befogad`-dal hagy jóvá.

## 4. Elfogadási feltételek

- A tábla minden TSV-Strongot lefed, vagy a hiány listázva van (üres eredmény explicit jelölve, nem kitöltve).
- A tábla szövegéből generált nézet és a TSV eltérése osztályozott; ismeretlen okú eltérés nincs.
- Az aranyminta és a seed-101 eredménye a táblán mért számmal a naplóban.
- A 674 kész szócikk mindegyike kategóriát kapott; az `adat/forditasok.tsv` változatlan.

## 5. Összehangolás (a felhasználó döntése, 2026-10-16: a gyökérnél)

1. `#107` 1. lépés: forrás és licenc (⛔ `DT-F107a`) — a legmélyebb függés.
2. `#107` 2–5. lépés: szakasztábla, nézet-ellenőrzés, ellenőrzés, javítótábla.
3. `#107` 6. lépés: nézet-döntés (⛔ `DT-F107c`).
4. `#107` 7. lépés és `#38`: a kész fordítás illesztése; a #38 következő adagja csak a `DT-F107c` után, várhatóan szakaszonkénti kulccsal
   (DT181 (b)).
5. `#102` (a #76 és a #107 után), szűkített hatókörrel (8. lépés javaslata).
6. `#103` → `#104` → `#105` → `#106`, a szakaszok szövegén.

## 6. Döntésnapló

- (helyőrzők a futáskor: DT-F107a forrás és licenc, DT-F107b az elakadó magyar szakaszok, DT-F107c a sima szöveg nézetté válása, DT-F107d a nyers forrás megőrzése és a
  veszteséges konverzió naplózása mint a playbook 2. pontjának általános szabálya)
- `DT190` (a #9 ágán nyitva, 2026-10-17, 🟡): a szakasztábla mint a BDB-tagolás egyetlen kanonikus forrása minden fogyasztónak
  (lexikon, olvasó, fordítás), közös kulccsal és CI-kapuval; a lexikon 4 BDB-sorának átkulcsolása jóváhagyás esetén a #107 után
  külön tétel (`DONTESEK.md`).
