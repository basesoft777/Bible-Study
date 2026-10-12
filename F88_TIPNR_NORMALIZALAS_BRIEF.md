---
feladat: 88
cim: TIPNR Strong-normalizálás — alapszám a strong oszlopban, utótag külön (DT111)
kod: TIPNR_NORMALIZALAS
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: nem_indult
ad: a pardes.db tipnr.strong oszlopa az alapszámot hordozza (a nagy- és kisbetűs utótag levágva, a TIPNR-betöltő kifejezett szabályaként), új utotag oszlop, a strong_nyers marad; SEMA 1.2 bővítve; a G6202 a normalizálási jelentésben; teszt és újraépítés, a NULL-arány mérve
kovetkezo: "M0 felmérés (csak olvas); ⛔, ha a mérés eltér a DT111 feltevésétől"
olvas: [DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, eszkozok/strong_util.py, eszkozok/sqlite_epit.py, konkordancia/TIPNR_kivonat.tsv, naplok/SQLITE_EPIT_meres.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, adat/SEMA.md, naplok/SQLITE_EPIT_meres.md, NYITOTT_FELADATOK.md]
fugg: [79]
---

# F88_TIPNR_NORMALIZALAS_BRIEF.md — TIPNR Strong-normalizálás a pardes.db-ben

*FELADATOK #88 · Modell: sonnet · v1 · 2026.10.12 · a csonk-briefet váltja fel · döntés: DT111 · forrás: `NYITOTT_FELADATOK.md` N-F79c, `naplok/SQLITE_EPIT_meres.md` (Normalizálási jelentés), `naplok/ELLENOR_F79.md` 6. pont*

## 1. Cél

A `pardes.db` `tipnr` táblájában ma 16 928 sor (47,7%) `strong` mezője NULL, mert a TIPNR a
Strong-számhoz egyértelműsítő utótagot fűz, a `strong_normalizal()` pedig ezt (helyesen)
elutasítja. A nagybetűs utótag a STEPBible-ben **személyt/entitást** különböztet meg egy
lexémán belül (`G2424G` Jézus, `G2424H` Barabbás, `H3063G` Júda, `H3063N` Júdea), nem
jelentésváltozatot. A cél: a `strong` oszlop az **alapszámot** hordozza, így a TIPNR a
`token_strong` kulcsán illeszkedik a lexikai lekérdezéshez, az entitás pedig nem vész el
(DT111).

## 2. Hatókör

**Benne van**

- `eszkozok/sqlite_epit.py`, a TIPNR-betöltő (ma a `# -- TSK, Karoli-KH, TIPNR` szakasz, `TIPNR_kivonat.tsv`):
  - a `Strong-szám` mezőből az alapszám (`H`/`G` + szám, SEMA 1.2 szerint nullázva) a `strong`
    oszlopba; a levágott utótag (nagy- és kisbetűs egyaránt) az **új `utotag` oszlopba**; a
    `strong_nyers` változatlan;
  - a levágás **a TIPNR-betöltő kifejezett, megnevezett szabálya** (egy függvény, docstringgel és
    DT111-hivatkozással); a `strong_util.strong_normalizal()` és annak `utotag='tilt'`
    alapértéke **nem változik** (máshol az utótag hibát jelezhet);
  - ami a levágás után sem normalizálható, továbbra is a `normalizalas_jelentes`-be kerül (G5);
  - új jelentés-ok: a levágott alapszám, amely a `token_strong`-ban nem szerepel (a mai mérés
    szerint egy: `G6202`) — nem javítás, csak jelölés.
- `adat/SEMA.md` 1.2: egy bekezdés a TIPNR-utótagról (mi a nagy- és a kisbetűs utótag, a
  `pardes.db` betöltője levágja, a teljes érték a `strong_nyers`-ben, az utótag az `utotag`-ban).
- `eszkozok/teszt_sqlite_epit.py`: tesztek (4. pont, G3).
- Teljes újraépítés és mérés a `naplok/SQLITE_EPIT_meres.md`-ben (a `tipnr` sorai, a NULL-arány
  előtte/utána, a táblaméret).

**Nincs benne**

- a licenc-rendezés és a táblaszintű licenc (#89, DT112, DT113);
- a nem létező Károli-versre mutató TIPNR-sorok (N-F79b, DT114: jelölve maradnak);
- a `konkordancia/TIPNR_kivonat.tsv` módosítása (forrás, nem ír bele);
- a `lekerdez.py` és más eszközök TIPNR-kezelése (ha a mérés eltérést mutat, nyitott tétel
  `N-F88a` helyőrzővel).

## 3. Lépések

- **M0 — felmérés (csak olvas).** A TIPNR `Strong-szám` mezőjének alakjai (utótag-típusok
  darabszámmal; van-e `+`-os vagy más rendhagyó érték); a levágott alapszámok illeszkedése a
  `token_strong`-hoz; ki olvas még TIPNR-Strongot a repóban (`grep`). Ha a mérés a DT111
  feltevésétől eltér (pl. a nagybetű nem entitás, vagy a levágás után ütközik valami), ⛔ megállás,
  és a felhasználó dönt. Egyébként folytatódik.
- **M1 — a szabály az építőben** (`F88.1:`), kis mintán futtatva.
- **M2 — tesztek** (`F88.2:`).
- **M3 — SEMA 1.2** (`F88.3:`).
- **M4 — teljes újraépítés és mérés** (`F88.4:`): két építés, táblánkénti hash azonos; a `tipnr`
  NULL-aránya; a jelentés új sora.
- **Zárás.** `fuggetlen-ellenor`; `python eszkozok/feladatok.py ellenoriz` 0; a
  `NYITOTT_FELADATOK.md` N-F79c lezárása a DT111-re hivatkozva; fejléc `lezarva`,
  `lezarva_osszegzes`; draft PR.

## 4. Elfogadási feltételek

- **G1** A diff nem érint `adat/*.tsv`, `konkordancia/`, `motivumok/`, `lexikon/` fájlt; a
  `pardes.db` nincs a repóban.
- **G2** A `strong_util.py` diffje üres; a levágás az építőben, egy megnevezett függvényben van.
- **G3** Tesztek: (a) `G2424G` → `strong='G2424'`, `utotag='G'`, `strong_nyers='G2424G'`;
  (b) egy kisbetűs utótagos sor ugyanígy; (c) utótag nélküli sor változatlan, `utotag` üres/NULL;
  (d) nem értelmezhető érték a jelentésbe kerül, nem némán NULL; (e) a `strong_util`
  `utotag='tilt'` továbbra is elutasítja a `G2424G`-t.
- **G4** A teljes építés után a `tipnr.strong` NULL-aránya mérve; minden megmaradt NULL sor név
  szerint a `normalizalas_jelentes`-ben (G5 az F79-ből).
- **G5** A `token_strong`-ban nem szereplő alapszámok listája a jelentésben (a mai mérés szerint
  `G6202`).
- **G6** Az építés determinisztikus (két futás táblánkénti hash-e azonos); a 37 + új teszt zöld.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| DT111 | A TIPNR utótag kezelése | alapszám a `strong`-ban, `utotag` oszlop, `strong_nyers` marad; a szabály a betöltőben, a `strong_util` alapértéke változatlan; SEMA 1.2; `G6202` a jelentésbe | eldöntve (felhasználó, 2026.10.12) |
