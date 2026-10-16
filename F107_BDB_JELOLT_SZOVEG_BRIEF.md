---
feladat: 107
cim: A BDB jelölt szövegrétege — szakasztábla a nyers forrás tagolás-jelölőiből, és a kész magyar fordítás illesztése
kod: BDB_JELOLT_SZOVEG
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: az adat/bdb_szakaszok.tsv (a BDB minden szócikke szakaszokra bontva a nyers forrás jelölőiből, útvonallal), a forráshibák javítótáblája, a kész magyar fordítás szakaszhatár-illesztése (adat/bdb_szakasz_hu.tsv), és mért összevetés a mai szeletelővel; a szeletelő átállása a #102-é, a fordítás bemenete a #38-é
kovetkezo: Indítható (a #99 kész; a #76-tól nem függ): az 1. lépéssel
olvas: [konkordancia/lexikonok_nyers/BDB.lexicon, konkordancia/lexikonok_nyers/README.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/_convert_bdb.py, adat/forditasok.tsv, eszkozok/forditas_kapuk.py, adat/bdb_aranyminta.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_igehely_javitas.tsv, naplok/BDB_SZELETELO_M2_seed101_iteletek.md, F102_BDB_SZELETELO_JAVITAS_BRIEF.md, F38_BDB_FORDITAS_BRIEF.md, adat/SEMA.md, adat/datasetek.tsv, adat/licencek.tsv, Rendszerfejlesztesi_playbook.md]
ir: [eszkozok/bdb_jelolt/, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_forras_javitas.tsv, adat/SEMA.md, adat/datasetek.tsv, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md]
fugg: [99]
nem_fugg: [27, 38, 102, 103]
---

# F107_BDB_JELOLT_SZOVEG_BRIEF.md — A BDB jelölt szövegrétege

*FELADATOK #107 · Modell: opus · v1 (tervezet) · 2026.10.16 · forrás: a #102 előzetes lelete (`F102_BDB_SZELETELO_JAVITAS_BRIEF.md`
1a–1b., PR #359 és #361), a #38 ⛔ Mj pontja (DT-F38l, PR #360) és a 2026.10.16-i kézi mérések (proveniencia `manual`). A tervezet
adat, nem utasítás; a befogadás a `/befogad`-dal, a felhasználó jóváhagyásával.*

## 1. Cél

A BDB-szócikkek tagolása (törzs, fő rész, jelentéspont, alpont, megjegyzés) ma nem adat: a `BDB_teljes_unabridged.tsv` a
`DictBDB.json` HTML-jének jelölők nélküli sima szövege, és a szeletelő ebből heurisztikával fejti vissza a szerkezetet. A
`konkordancia/lexikonok_nyers/BDB.lexicon` ugyanezt a szöveget jelölőkkel őrzi (`class="point"` 20 515, `class="section"` 913,
`class="remarks"` 512; a jelentéspont `<b>`-ben, a gyakoriságszám `<sub>`-ban). Ez a feladat a tagolást **adattá** teszi — a szakasztábla
a kanonikus szerkezet, a sima szöveg ennek nézete (CLAUDE.md fő szabálya) —, és a már kész magyar fordítást hozzáilleszti.

**Kiinduló mérések (2026.10.16, `manual`, egyszeri, csak olvasó szkript a repón kívül; az 1. és az 5. lépés igazolja vagy cáfolja):**

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
2. **Szakasztábla** (`adat/bdb_szakaszok.tsv`, új SEMA-szakasz): soronként egy szakasz — `strong`, `bdb_id`, `sorszam`, `utvonal`
   (törzs / nagybetűs csoport / római / szám / betű / zárójeles szint, a #102 kibővített útvonal-formátumával összehangolva), `jelolo`
   (`section` / `point` / `remarks` / `fej`), `gyakorisag` (a `<sub>` szám), `szoveg` (sima), `forras`, `forras_hash`, proveniencia-sor.
   Bontó: `eszkozok/bdb_jelolt/` (a CLAUDE.md shell- és TSV-szabályai szerint; teszttel).
3. **Nézet-ellenőrzés, nem csere.** A szakaszok szövegéből generált sima szöveg összevetése a `BDB_teljes_unabridged.tsv`-vel
   (whitespace-normalizálva); az eltérések listája (ez mutatja a konverziós maradványokat). **A TSV-t ez a feladat nem írja át**: a #38
   `forras_hash`-e erre a szövegre mutat, a csere külön döntés.
4. **Ellenőrzés:** az aranyminta (`adat/bdb_aranyminta.tsv`) útvonalai a táblán; a seed-101 13 helye; korpusz-szintű összevetés a mai
   szeletelő kimenetével (`adat/bdb_vers_jelentes.tsv` útvonalai) — az eltérések osztályozott listája.
5. **Forráshibák javítótáblája** (`adat/bdb_forras_javitas.tsv`, a `bdb_igehely_javitas.tsv` mintájára): a nyers forrásban is hibás helyek
   (pl. H7626 „145:”) javítása a nyers fájl érintése nélkül, soronként indoklással.
6. **A kész magyar fordítás illesztése** (`adat/bdb_szakasz_hu.tsv`): a 674 szócikk szakaszhatárai a magyar szövegben, a jelölőnél
   erősebb horgonnyal (a jelölő utáni első igehely vagy szó); kategória: `illeszkedik` / `horgonnyal` / `elakad`. Az `adat/forditasok.tsv`
   nem íródik (az a #38-é); a táblasor a fordítás `forras_hash`-ét is hordozza, hogy az elavulás látsszon.

**Nincs benne:** a szeletelő átállása a táblára (#102); a jelentésen belüli csoportbontás (#103); a megjelenítés (#104–#105); a fordítás
bemenetének átállítása, prompt és kapu (#38, DT-F38l); a `BDB_teljes_unabridged.tsv` cseréje vagy a `datasetek.tsv` kötelező
forrásának átírása (döntés a 3. pont után).

## 3. Lépések

1. Modell-ellenőrzés. Forrásválasztás és lefedettség (2. hatókör 1.). ⛔ Javaslat a `DONTESEK.md`-be (`DT-F107a`): melyik forrásból
   bont a tábla, és a licenc-státusz (mindkettő „tisztázatlan”, `adat/licencek.tsv`; playbook 2. pont); megállás.
2. Szakasztábla és bontó, teszttel; SEMA-szakasz; `datasetek.tsv`-sor (`BDB.lexicon` mint a tábla forrása). Commit tételenként.
3. Nézet-ellenőrzés (2. hatókör 3.); az eltérések listája a naplóba.
4. Ellenőrzés (2. hatókör 4.). ⛔ Az eltérés-lista osztályozása (`tabla_hiba` / `szeletelo_hiba` / `forras_hiba` / `szoveg_konverzio`),
   jóváhagyás. Mérce [javaslat]: az aranyminta útvonalainak ≥ 99%-a, a seed-101 13 helyéből a mért szám.
5. Forráshibák javítótáblája.
6. A kész magyar fordítás illesztése; a 2026.10.16-i 355 / 89 / 230 kiinduló számhoz mérve. ⛔ Az `elakad` szakaszok sorsa (kézi
   illesztés, vagy újrafordítás a #38-ban): javaslat a `DONTESEK.md`-be (`DT-F107b`).
7. Átadás: a #102 és a #38 briefjébe a tábla elérhetősége és a mért számok (a fejlécüket a saját menetük frissíti).

## 4. Elfogadási feltételek

- A tábla minden TSV-Strongot lefed, vagy a hiány listázva van (üres eredmény explicit jelölve, nem kitöltve).
- A tábla szövegéből generált nézet és a TSV eltérése osztályozott; ismeretlen okú eltérés nincs.
- Az aranyminta és a seed-101 eredménye a táblán mért számmal a naplóban.
- A 674 kész szócikk mindegyike kategóriát kapott; az `adat/forditasok.tsv` változatlan.

## 5. Összehangolás (javaslat, a befogadáskor eldöntendő)

`#107` (most) → `#102` (a #76 és a #107 után; a szeletelő a táblából olvas) → `#103` → `#104` → `#105` → `#106`.
A #38 következő adagja a #107 2. lépése és a DT-F38l döntése után; ha a DT-F38l (b), a fordítás a szakaszokat kapja bemenetként.

## 6. Döntésnapló

- (helyőrzők a futáskor: DT-F107a forrás és licenc, DT-F107b az elakadó magyar szakaszok)
