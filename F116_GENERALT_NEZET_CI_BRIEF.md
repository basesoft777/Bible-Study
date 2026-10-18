---
feladat: 116
cim: CI-szabályok a generált nézetre: újragenerálás-egyezés (E28) és a kiadható kimenet tisztasága (E29)
kod: GENERALT_NEZET_CI
tipus: feladat
fazis: 1
munka: folyamat
modell: sonnet
allapot: nem_indult
ad: E28 (a generált nézet bájtra egyezik a commit adat- és forrásrétegéből újragenerálttal) és E29 (a kiadható kimenetben nulla `belso` jelölés és nulla `【NAPLO`) a CI-ban, pozitív és negatív tesztekkel, a migrált nézetek engedélyezőlistájával (kezdetben üres); a mai main-en 0 HIBA, méréssel igazolva
kovetkezo: a brief végrehajtása a `/kovetkezo`-val; a #11 M2 lépése előtt le kell zárulnia (D6, `F11_MIGRACIO_BRIEF.md` M2)
olvas: [naplok/MOTIVUM_FORRAS_ci_terv.md, naplok/MOTIVUM_FORRAS_pilot_terv.md, adat/SEMA.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, F11_MIGRACIO_BRIEF.md, eszkozok/ellenorzes/, .github/workflows/ellenorzes.yml, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/nulladiff.sh, Lezart_tematikus_tanulmanyok_index.md, lexikon/]
ir: [eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, eszkozok/ellenorzes/tesztek/, .github/workflows/ellenorzes.yml, motivumlog/PaRDeS_motivumok.md, naplok/GENERALT_NEZET_CI_meres.md, naplok/ELLENOR_F116.md]
fugg: []
nem_fugg: [11, 114]
---
# F116_GENERALT_NEZET_CI_BRIEF.md — CI-szabályok a generált nézetre (E28, E29)

*FELADATOK #116 · Modell: sonnet · v1 · 2026.10.18 · döntések: D34, D35, D36, DT28, DT74 (3), DT84 (10)*

## 1. Cél

A #23 CI-terve (`naplok/MOTIVUM_FORRAS_ci_terv.md`, DT84 átvezetve) két szabály szerződését
rögzítette, implementáció nélkül; az implementáció külön ágon megy, a #11 M2 lépése előtt (D6,
`F11_MIGRACIO_BRIEF.md` 38. és 53. sor). Ez a feladat ezt az implementációt végzi el:

- **E28:** a generált nézet bájtra egyezik azzal, amit a generátor a commit (a) adat- és
  (b) forrásrétegéből előállít. Kézi szerkesztést és újragenerálás nélküli adatváltozást fog
  meg (CLAUDE.md „Rétegek”, SEMA 3/9).
- **E29:** a kiadható kimenetben nulla `belso` jelölés és nulla `【NAPLO` (SEMA 3.10.4, D36:
  build-kihagyás, nem elrejtés).

A szerződés a CI-terv 1. és 2. szakasza; ez a brief azt nem ismétli, csak a végrehajtási
döntéseket és az eltéréseket rögzíti. Ahol a brief és a CI-terv ellentmond, **állj meg**, és
jelezd (⛔).

## 2. Hatókör

**Benne van:**

- az E28 és az E29 a `szabalyok.py`-ban, a `futtat.py`-ba és a workflow-ba bekötve;
- a migrált nézetek engedélyezőlistája: `eszkozok/ellenorzes/e28_migralt_nezetek.tsv` (D2, D3);
- a meglévő generált marker-blokkok (`general.py --cel naplo`, `index`, `nyitott`) E28-as
  ellenőrzése, a ma eltérő két blokk újragenerálásával (D4);
- tesztek a `tesztek/test_szabalyok.py` mintájára (`_IdeiglenesGyoker`), mindkét szabályhoz
  pozitív és negatív eset (4. G3);
- mérési napló: `naplok/GENERALT_NEZET_CI_meres.md`.

**Nincs benne:**

- a törzscikk (`lexikon/*_TORZSCIKK.md`; a #11-ben megszűnik, N-F78a) és a `generalt_proba/`
  (verziózott próbakimenet) — CI-terv 1. szakasz;
- a nem migrált motívumok éles `lexikon/` lapja (befagyasztva, DT74 (3)): rájuk egyik szabály
  sem fut;
- **szint-szűrő** (N-F23b): az E29 nem szűr, nem olvas forrást és nem hívja a generátort, csak a
  kész kimenetben keres (D5). A közös build-idejű szűrő gazdája nyitott, nem ez a feladat;
- a #11 briefje (a visszahivatkozást a felhasználó vezeti át, l. 5. D7), a forrásra futó
  szakasz-szabály (CI-terv 3. szakasz), az arany-készlet CI-része (DT78 (22));
- generátor-módosítás. Ha az E28 csak generátor-javítással lehetne zöld, **állj meg** (⛔).

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a kért modell `sonnet`; eltérésnél állj meg.

**1. M0 — kiinduló mérés a friss main-en** (naplóba, proveniencia-sorral):

- a számok szabadok-e még: `E28`, `E29` a `szabalyok.py`-ban, a workflow-ban és az összes
  távoli ág md/py/yml fájljában (az `E30` a #112-é). Ha foglalt, a következő szabad szám, és a
  CI-terv 0. szakasza hivatkozással frissül (a CI-terv 0. szakaszának szabálya);
- `python eszkozok/general.py --cel <naplo|index|nyitott> --ellenoriz` mindhárom célra: blokkonként
  zöld/eltér, és az eltérő blokkok sor-szintű diffje (a generált blokk `--kimenet`-tel, a repón
  kívüli ideiglenes könyvtárba). Az eltérés okát blokkonként nevezd meg: adatváltozás
  újragenerálás nélkül / kézi szerkesztés / generátor-változás;
- a generátorok futnak-e friss checkouton a gitignore-olt `konkordancia/_nyers/` nélkül (a CI
  ezt látja); futási idő célonként;
- sorvég: ugyanaz a generátor-kimenet keletkezik-e Windowson és Linuxon, és mi a commitolt
  blob sorvége (`core.autocrlf=true`, `.gitattributes`). Az összevetés alapja a commitolt blob
  (`git show <fej>:<út>`), nem a munkafa-fájl (CI-terv 1. szakasz 3. pont).

*A brief írásakor mért állapot* (`scope=general.py --ellenoriz, cél: naplo, index, nyitott |
forras=manual (CLI-futtatás, blokk-diff scratch-szkripttel) | ts=2026-10-18`, `origin/main`
1d0189e6): `index` zöld; `naplo#attekintes`, `#kuszob`, `#kulcsszo_index` zöld; **`naplo#konyv_index`
eltér** (4 diff-sor: a Jób 17:13/17:16 → 17:12/17:15 és a Préd 9:10 → 9:12 ALVIL-001-sor, azaz az
`elofordulasok.tsv` versszám-javítása újragenerálás nélkül); **`nyitott` eltér** (79 diff-sor:
a blokk 17 nyitott jelöltet mutat 3 motívumról, a tábla ma 50-et 7-ről, többek közt az F108
újrascan sorait, azaz `jeloltek.tsv`-változás újragenerálás nélkül). Ha az M0 ettől eltér, a
mért érték számít, és a különbség a naplóba kerül.

**2. ⛔ Ha az M0 bármelyik pontja eltér a brief feltevésétől** (a generátor CI-ban nem fut; a
sorvég platformfüggő; egy blokk eltérésének oka kézi szerkesztés vagy generátor-változás, nem
újragenerálás nélküli adatváltozás): megállás, `DT-F116a` tétel a `DONTESEK.md`-be, `allapot:
dontesre_var`.

**3. A két eltérő blokk újragenerálása** külön commitban (`F116.3:`), ha az M0 szerint mindkét
eltérés oka újragenerálás nélküli adatváltozás: `general.py --cel naplo --ir` és `--cel nyitott
--ir`. A commit csak a `GENERÁLT-KEZDET`/`GENERÁLT-VÉGE` közti törzseket és a markersorok `ts=`
értékét változtatja (git diff-fel igazolva, a naplóban); a kézi szakaszok bájtra változatlanok.
Utána a három cél `--ellenoriz`-e zöld.
**⛔ Commit előtt** (a felhasználó kikötése, 2026-10-18, a befogadáskor): a két blokk
újragenerálásának diffjét meg kell mutatni a felhasználónak, blokkonként a diff-sorok számával és
azzal, hogy melyik adatváltozás (commit, tábla, sor) okozza. Ha a diff nem csak a hiányzó
újragenerálásból adódik (bármely sor nem vezethető vissza commitolt adatváltozásra): megállás,
`DT-F116a`, `allapot: dontesre_var`. Commit csak a felhasználó jóváhagyása után.

**4. Az engedélyezőlista** `eszkozok/ellenorzes/e28_migralt_nezetek.tsv`, fejléccel, sor nélkül
(D2, D3). Oszlopok: `id`, `fajl` (a generált nézet repó-relatív útja), `cel` (a `general.py`
célja, amely előállítja), `melyseg` (`apparatus` | `olvasoi`, az E29 mintakészletéhez),
`feladat`, `datum`. Olvasás `split('\t')`, a `csv` modul tilos (CLAUDE.md „TSV-olvasás”).

**5. Az E28 megvalósítása** a CI-terv 1. szakasza szerint, két ágon:

- *marker-blokkok:* a három cél blokkjainak törzs-összevetése a `general.py` meglévő
  `--ellenoriz` útján (alfolyamatként vagy a függvényei importjával; a logika nem duplikálódik);
- *migrált nézetek:* a lista minden sorára a fájl újragenerálása a repón kívüli ideiglenes
  könyvtárba, `PARDES_DATUM` = a commitolt fájl első `GENERÁLT` jelölőjének `ts=` dátuma, majd
  bájt-összevetés a commitolt blobbal. Üres listánál ez az ág nem csinál semmit, és ezt a jelentés
  kiírja („E28: 0 migrált nézet”).

Mikor fut: PR-en, ha a változott fájlok között van `adat/*.tsv`, `motivumok/*.md`,
`eszkozok/*general*.py`, `sablonok/9_*.md`, a lista, vagy a hatókör generált fájlja; `--teljes`
módban mindig. Szint: **HIBA**, `FAJLSZINTU_SZABALYOK` közé (a D8 diff-leminősítés nem
alkalmazandó). A jelentés: a fájl, az első eltérő sor száma, mindkét oldal sora, marker-blokknál
a cél-kulcs, és a javító parancs (pl. `python eszkozok/general.py --cel nyitott --ir`).

**6. Az E29 megvalósítása** a CI-terv 2. szakasza szerint: a lista minden `fajl`-ján szöveges
keresés a minta-konstansra (kódkerítésen belül is), a `melyseg` szerinti kiegészítő mintákkal
(`olvasoi`: `GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`, `RÉS-KEZDET`, `RÉS-VÉGE`, `proveniencia:`). A
minta-konstans mellett megjegyzés: forrása a SEMA 3.10.4 jelölő-listája, a SEMA bővülésekor
együtt bővül. Szint: **HIBA**, `FAJLSZINTU_SZABALYOK` közé (D6); a jelentés soronként: fájl, sor,
minta. Minden PR-en és `--teljes` módban fut (a lista kicsi, a keresés olcsó).

**7. Tesztek** a `test_szabalyok.py`-ban (`E28Teszt`, `E29Teszt`), a CI-terv tesztlistája szerint
(4. G3). Az E28 tesztje a generátort nem az éles repón futtatja: a fixture ideiglenes gyökérben
áll, a generátor-hívás a tesztben helyettesíthető (a meglévő `_IdeiglenesGyoker` mintájára).

**8. Mérés a kész kóddal**, a naplóba:

- `python eszkozok/ellenorzes/futtat.py --teljes` a munkaágon (= main + a 3. lépés
  újragenerálása): E28 0 HIBA, E29 0 HIBA; a három marker-cél zöld; a lista üres;
- egy próba-futás egy ideiglenes listával, amelyben a mai `lexikon/ISTENTISZT-001_TUDOMANYOS.md`
  áll (`melyseg=apparatus`), **commit nélkül**: az E29-nek a mért 14 `【NAPLO` sort kell
  jeleznie (CI-terv 2. szakasz „Mért kiindulás”), az E28-nak pedig a #78 óta eltérő
  2. szakaszt. Ez igazolja, hogy a szabály a migrált lapon élesen fog: a lista ezért üres
  addig, amíg a #11 a migrált lappal együtt fel nem veszi a sort;
- a szabály-tesztek és a `python eszkozok/feladatok.py ellenoriz` zöld.

**9. ⛔ Független ellenőrzés** (`fuggetlen-ellenor`): `naplok/ELLENOR_F116.md`, a teljes
base..head diffen.

**10. Zárás** a `/kovetkezo` szerint. **A PR címe `[ELLENŐRZŐ]` előtaggal kezdődik** (E16: a PR
az `eszkozok/ellenorzes/`-t és a `.github/`-ot érinti); e nélkül a saját CI-je piros.

## 4. Elfogadási feltételek

- **G1.** Az E28 és az E29 a CI-terv szerződését valósítja meg; ahol eltér, az eltérés a 5.
  döntésnaplóban áll, indokkal.
- **G2.** A `futtat.py --teljes` a munkaágon E28/E29 0 HIBA (8. lépés), a mért kimenet a naplóban.
- **G3.** Tesztek, mind zöld: *E28* — pozitív: változatlan forrásból generált, commitolt nézet és
  marker-blokk zöld; negatív: (a) a nézetbe kézzel írt egy szó piros, (b) egy `adat/*.tsv` mező
  változik, a nézet nem: piros, (c) a forrás egy `olvasoi` bekezdése változik, a nézet nem: piros,
  (d) marker-blokk törzsének kézi átírása piros, (e) a listán nem szereplő (befagyasztott) lap: nem
  fut; *E29* — pozitív: `apparatus` nézet `【NAPLO` nélkül zöld; negatív: (a) `【NAPLO` a lapon
  piros, (b) `<!-- SZINT-KEZDET: belso -->` piros, (c) `INAKTÍV:` piros, (d) `olvasoi` mélységű
  sorban `proveniencia:` piros, `apparatus` mélységűben nem, (e) ugyanez a `motivumok/*.md`
  forrásban: nem fut.
- **G4.** Az E29 kódja nem importál generátort és nem olvas `motivumok/` forrást (grep-pel
  igazolva a naplóban, D5).
- **G5.** A 3. lépés commitja csak marker-blokk törzset és marker `ts=`-t változtat, és a felhasználó a diffet a commit előtt jóváhagyta (3. lépés ⛔).
- **G6.** A TSV-t a kód `split('\t')`-tel olvassa; a `csv` modult nem használja.
- **G7.** A szkriptek a CLAUDE.md „Shell” szakasza szerinti stdout/stderr-wrappert viselik.

## 5. Döntésnapló

- **D1.** A számok: **E28** és **E29** (a CI-terv 0. szakasza foglalta, 2026-10-08); az E30 a
  #112-é (`F112_COMMIT_EKEZET_BRIEF.md` D1). Az M0 újraméri (1. lépés).
- **D2.** Az engedélyezőlista **kezdetben üres** (csak fejléc). Indok: a #11 M1 leképezési táblája
  jóváhagyva (`claude/f11-migracio`, 2ab6389d), de az M2 (generátor-képességek: forrás olvasása
  szintszűréssel) még nem készült el, ezért az ISTENTISZT-001 ma nem renderel a forrásból; a
  `motivumok/ISTENTISZT-001.md` a régi F4-forrásréteg, az éles lapja a befagyasztott régi lap
  14 `【NAPLO`-val. Ha a lista ma az ISTENTISZT-001-et tartalmazná, az E29 14 HIBÁ-t adna, az E28
  pedig olyan generátor-utat hívna, amely még nincs: a main piros lenne. A sort a #11 veszi fel,
  ugyanabban a commitban, amelyben a migrált lap először a forrásból generálódik (M4/M5), és az
  E28/E29 attól fogva élesen fut rá (pilot-terv 7.3 5. pont).
- **D3.** A lista helye `eszkozok/ellenorzes/` (nem `adat/`). Indok: a lista a CI hatókörét
  szabja meg; egy sor törlése gyengíti az ellenőrzést, ezért az E16 önmódosítás-védelme alá kell
  esnie. Következmény: a #11 PR-je, amely a sort felveszi, `[ELLENŐRZŐ]` előtagot kap.
- **D4.** A marker-blokkok hatókörben vannak (CI-terv 1. szakasz), ezért a ma eltérő két blokk
  (`naplo#konyv_index`, `nyitott`) a szabály élesítése előtt újragenerálódik (3. lépés), nem
  kerül kivétellistára: az E28 nem ismer elfogadott eltérést (CI-terv „Elfogadott eltérés
  nincs”). Következmény a többi feladatra: az `adat/jeloltek.tsv`-t, `motivumok.tsv`-t vagy
  `elofordulasok.tsv`-t író PR-nek ugyanabban a PR-ben újra kell generálnia az érintett
  marker-blokkot (a hibaüzenet megadja a parancsot).
- **D5.** Az E29 **csak a kimenetet ellenőrzi** (N-F23b): nem szint-szűrő, nem dönti el, mi
  kerüljön a kimenetbe, és nem implementálja a D36 build-kihagyást. Így nem jön létre második
  szűrő a #86 leendő feed-építője mellett; a közös szűrő gazdája továbbra is nyitott.
- **D6.** Eltérés a CI-tervtől: az E29 szintje HIBA, de **fájlszintű** (`FAJLSZINTU_SZABALYOK`),
  nem a D8 szerint diff-leminősített soronkénti találat. Indok: a hatókör generált fájl, amelyet a
  PR egészében újraír; a „régi, a PR által nem érintett sor” kategóriája rá nem értelmezhető. A
  jelentés soronkénti marad.
- **D7.** A #11 briefjét ez a feladat nem írja. **Javaslat a felhasználónak** (a #11 fejlécén
  átvezetendő): `fugg: [9, 23, 116]` (a sorrend gépileg is látsszon), és az `ir` mező bővítése az
  `eszkozok/ellenorzes/e28_migralt_nezetek.tsv`-vel (a D2 szerinti sorfelvételhez).
- **D8.** Modell: `sonnet`. Indok: a szerződés (mit, mire, milyen szinten, mi a bukás) a CI-tervben
  rögzítve van, a minta (`szabalyok.py` E5/E27, `test_szabalyok.py`) adott, értelmező próza és
  tartalmi döntés nincs; a kockázatos pontok (generátor CI-futása, sorvég, a blokk-eltérés oka)
  mérési kérdések, amelyeken a brief ⛔-nel megáll (2. lépés). Opus akkor indokolt, ha az M0 után a
  feladat generátor-módosítást kívánna, ez viszont a hatókörön kívül van.
