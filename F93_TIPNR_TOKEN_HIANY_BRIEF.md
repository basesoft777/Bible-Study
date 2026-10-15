---
feladat: 93
cim: A TIPNR 62 token nélküli görög alapszáma — szövegváltozat vagy hiány (88 sor)
kod: TIPNR_TOKEN_HIANY
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: fut
ag: claude/f93-tipnr-token-hiany
ad: a 62 alapszám (88 TIPNR-sor) mindegyike osztályozva (szövegváltozat / számozási eltérés / adathiány / nem eldönthető), forrásmegjelöléssel naplózva; az eredmény jelölés, nem javítás
kovetkezo: M0 felmérés (csak olvas); ⛔ a jelölés helyéről (DT-F93a) a felhasználó dönt
fugg: [88]
olvas: [naplok/F88_meres.md, naplok/ELLENOR_F88_2.md, adat/SEMA.md, konkordancia/TIPNR_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_TIPNR_Normalizalo_README.md, eszkozok/sqlite_epit.py, F90_TAGNT_ZAROJELES_BRIEF.md]
ir: [naplok/F93_jelentes.md, naplok/F93_alapszamok.tsv, eszkozok/f93_tipnr_token_hiany.py, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, adat/SEMA.md, NYITOTT_FELADATOK.md, DONTESEK.md]
---

# F93_TIPNR_TOKEN_HIANY_BRIEF.md — a TIPNR token nélküli görög alapszámai

*FELADATOK #93 · Modell: sonnet · v1 · 2026.10.13 · a csonk-briefet váltja fel · a commitok sorszáma a befogadás `F93.0`–`F93.2`-je után folytatódik · forrás: az F88 mérése (`naplok/F88_meres.md`, `naplok/ELLENOR_F88_2.md`)*

## 1. Cél

A `pardes.db` `tipnr` táblájának 35 522 sorából 89 olyan `strong`-ot hordoz, amely a
`token_strong`-ban nem szerepel. Ebből 1 a #88 levágott utótagja (`G6202`, a normalizálási
jelentésben jelölve); **88 sor, 62 különböző görög alapszám utótag nélküli**, és már az F79 óta
nem illeszkedik (pl. `G0300`, `G0962`). Ezekre a TIPNR-névrekordból nincs út az igehelyhez:
a lekérdezés **néma nem-találatot** ad (`lekerdez.py scan G0300` → `n=0`).

**Feltevés (nem ellenőrzött):** a többség szövegváltozat. A TAGNT-kivonat a kritikai szöveg
olvasatait hordozza, a TIPNR viszont más kiadás olvasatának Strong-számát is felsorolja, és ezt a
`Névváltozat` oszlopban jelöli. Példa: `Amon =NIV,KJV,TR` → `G0300`, Mt 1:10; a
`TAGNT_kivonat.tsv` Mt 1:10-nél csak a `G0301`-et (Ámósz) adja, `Kritikai kiadás` =
`NA28+NA27+Tyn+SBL+WH+Treg` (TR nélkül).

A cél: mind a 62 alapszámról **adatból** eldönteni, mi az oka, és ezt jelölni. **Nem javítás:**
sem a TIPNR, sem a TAGNT nem módosul, és token sem keletkezik.

## 2. Hatókör

**Benne van**

- A 62 alapszám (88 sor) listája a kész `pardes.db`-ből vagy közvetlenül a két kivonatból,
  determinisztikus szkripttel (`eszkozok/f93_tipnr_token_hiany.py`).
- Osztályozás alapszámonként, kizárólag a repó adatából:
  - **szövegváltozat** — a TIPNR-sor `Névváltozat` mezője kiadás-jelölést hordoz (`=KJV`, `=TR`,
    `=NIV` …), és a TAGNT-kivonat ugyanazon a versen más Strong-számot ad, amelynek `Kritikai
    kiadás` mezője az adott kiadást nem tartalmazza;
  - **számozási eltérés** — a TIPNR igehelye (STEPBible-alak, normalizálva a
    `Konyv_normalizalo_tabla.tsv`-vel) és a TAGNT Károli-kulcsa versszámozás miatt tér el (l. #90,
    `[..]`/`{..}` csoportok); a szó a szomszédos versben megvan;
  - **adathiány** — a TAGNT a versen ugyanazt a nevet más Strong-szám nélkül sem hordozza, és
    kiadás-jelölés sincs;
  - **nem eldönthető** — a repó adatából nem dönthető el; **explicit jelölendő, nem kitöltendő**
    (CLAUDE.md 3. szabály).
- Alapszámonként egy sor a `naplok/F93_alapszamok.tsv`-ben: `strong`, `nev`, `nevvaltozat`,
  `igehely` (a TIPNR-sor(ok)), `osztaly`, `tagnt_strong_a_versen`, `tagnt_kiadas`, `indoklas`,
  `proveniencia` (`scope=… | forras=… | ts=…`). TSV-írás `'\t'.join()`-nal, nem `csv`-vel.
- Összesítő a `naplok/F93_jelentes.md`-ben: osztályonkénti darabszám, a nem eldönthetők listája.
- A jelölés a DT-F93a döntése szerint (3. pont, ⛔).

**Nincs benne**

- a `konkordancia/TIPNR_kivonat.tsv` és a `TAGNT_kivonat.tsv` módosítása (forrás);
- a nyers STEPBible TAGNT letöltése vagy olvasása (ha a repó adata nem elég, a sor `nem
  eldönthető`; a nyers adat bevonása új tétel `N-F93a` helyőrzővel);
- a TR/KJV-olvasatok tokenként való felvétele a `pardes.db`-be;
- a `lekerdez.py` viselkedése (ha a mérés szerint a néma nem-találatot ott kellene jelezni,
  új tétel `N-F93b` helyőrzővel);
- a nem létező Károli-versre mutató TIPNR-sorok (N-F79b, DT114).

## 3. Lépések

- **M0 — felmérés (csak olvas; a fejléc-commit `F93.<n>:`).** A 62 alapszám és 88 sor újramérése
  (egyezik-e az F88 számával; ha nem, ⛔); a `Névváltozat` kiadás-jelöléseinek eloszlása a 88
  soron; próbaosztályozás. **⛔ megállás:** a felhasználó dönt a DT-F93a-ról, az osztályok
  darabszámával a kezében.
- **M1 — a szkript és a lista** (külön commit): `eszkozok/f93_tipnr_token_hiany.py` (UTF-8 őr az
  importok után, TSV `split('\t')`), a `naplok/F93_alapszamok.tsv` megírása; két futás
  bájtazonos.
- **M2 — a jelölés** (külön commit) a DT-F93a szerint:
  - (a) csak a lista és a jelentés — nincs kódváltozás, az `ir`-ből a `sqlite_epit.py`,
    `teszt_sqlite_epit.py` és `adat/SEMA.md` kimarad;
  - (b) új ok a `pardes.db` `normalizalas_jelentes`-ében (`token nélküli alapszám: <osztály>`),
    tesztekkel és a SEMA bekezdésével; teljes újraépítés, két építés hash-e azonos.
- **M3 — jelentés** (külön commit): `naplok/F93_jelentes.md`.
- **Zárás.** `fuggetlen-ellenor`; `python eszkozok/feladatok.py ellenoriz` 0; fejléc `lezarva`,
  `lezarva_osszegzes`; draft PR.

## 4. Elfogadási feltételek

- **G1** A diff nem érint `konkordancia/`, `motivumok/`, `lexikon/` fájlt és `adat/*.tsv`-t; a
  `pardes.db` nincs a repóban.
- **G2** A 62 alapszám mindegyike pontosan egy osztályt kap; a lista sorainak száma 62, a mögöttük
  álló TIPNR-sorok száma 88 (ha a mérés eltér, ⛔ az M0-ban).
- **G3** Minden `szövegváltozat` sor megnevezi a TAGNT-oldali Strong-számot és annak `Kritikai
  kiadás` mezőjét; minden sor proveniencia-sort hordoz. Asszociatív vagy emlékezetből vett
  indoklás nincs; ahol a repó adata nem dönt, `nem eldönthető`.
- **G4** A szkript determinisztikus: két futás kimenete bájtazonos.
- **G5** (b) esetén: a meglévő 43 teszt és az új tesztek zöldek; két építés táblánkénti hash-e
  azonos; a `tipnr` tábla tartalma nem változik (hash `d4a93c34d0e36db8`), csak a
  `normalizalas_jelentes`.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| DT-F93a | Hol áll a jelölés: (a) csak `naplok/F93_alapszamok.tsv` + jelentés, vagy (b) a `pardes.db` `normalizalas_jelentes`-ében is? | (a), ha a `nem eldönthető` osztály üres vagy kicsi; (b), ha az olvasói felületnek (#92) kell a lekérdezéskor | nyitott — ⛔ az M0 után, a felhasználó dönt |
