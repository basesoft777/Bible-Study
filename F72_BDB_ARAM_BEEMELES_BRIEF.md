---
feladat: 72
cim: Az arámi pótlás beemelése a BDB fő táblába (164 alias-sor + 6 szöveges pótlás)
kod: BDB_ARAM_BEEMELES
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: lezarva
ag: claude/bdb-aram-beemeles
pr: 236
lezarva_osszegzes: PR #236; 164 arámi alias-sor + 6 szövegsor a BDB fő táblába (a régi sorok bájtra azonosak), a #38 sorrendje újragenerálva (+9 sor, a 7. adag első sora H4725), jelölt H0004, H3769, H5013; N-F72a helyőrző; ellenőr 2 kör
ad: a konkordancia/BDB_strong_alias.tsv a 164 duplikált arámi Strong-számmal bővül (a héber testvérsorra mutatva), a BDB_teljes_unabridged.tsv végére a 6 valódi hiány kerül szövegsorként; a meglévő sorok bájtra azonosak; a #38 sorrendje újragenerálva
kovetkezo: "lezárva; a #38 befogadáskori fugg-bővítése és a 7. adag (sorrend 649–, az első sor most H4725); a DT-F67a 9. adag kapuját az adagok eltolódása érintheti"
olvas: [konkordancia/BDB_aram_potlas.tsv, konkordancia/BDB_aram_potlas_README.md, naplok/BDB_ARAM_POTLAS_duplikacio.md, naplok/BDB_ARAM_POTLAS_zaras.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_strong_alias.tsv, konkordancia/BDB_strong_alias_elvetett.tsv, konkordancia/BDB_teljes_unabridged_README.md, eszkozok/bdb_strong_potlas.py, eszkozok/bdb_aram_potlas.py, F38_BDB_FORDITAS_BRIEF.md, adat/SEMA.md]
ir: [eszkozok/bdb_sorrend_ujragen.py, naplok/BDB_FORDITAS_sorrend.tsv, naplok/ELLENOR_F72.md, NYITOTT_FELADATOK.md, naplok/BDB_ARAM_BEEMELES_szarazfutas.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_strong_alias.tsv, konkordancia/BDB_teljes_unabridged_README.md, eszkozok/bdb_aram_beemeles.py, eszkozok/teszt_bdb_aram_beemeles.py, naplok/BDB_ARAM_BEEMELES_zaras.md]
fugg: [66]
---

# F72_BDB_ARAM_BEEMELES_BRIEF.md — Az arámi pótlás beemelése a BDB fő táblába

*FELADATOK #72 · Modell: sonnet · v1 · 2026.10.06 · forrás: N51 (NYITOTT_FELADATOK.md), felhasználói döntés 2026-10-06 (chat)*

## 1. Cél

Az F66 (#66) a `konkordancia/BDB_aram_potlas.tsv` táblában 170 elfogadott arámi sort állított elő (169 `egyertelmu` + 1 `kezi_elfogadott`: H2298 → BDB9285), a fő tábla változatlan hagyása mellett. A duplikáció-mérés (`naplok/BDB_ARAM_POTLAS_duplikacio.md`) szerint 164 sor szövege (mérőszám ≥ 0,8) már a fő táblában van, a héber testvérsor végén; 5 részleges (0,5–0,8), 1 nincs (H6433).

A felhasználó döntése (N51, 2026-10-06, chat): a 164 duplikált sort **nem** emeljük be új szövegsorként; a 164 Strong-szám **alias-sorként** kerül be, a héber testvérsorra mutatva; szöveges pótlásként csak a **6 valódi hiány** megy a fő tábla végére. A cél, hogy a #38 (BDB fordítás) minden arámi Strong-számot elérjen, szöveg-duplikáció nélkül.

## 2. Hatókör

**Benne van:**

- 164 alias-sor a `konkordancia/BDB_strong_alias.tsv`-be, a meglévő minta szerint: `masodlagos_strong` (az arámi Strong), `tabla_strong` (a héber testvérsor kulcsa a fő táblában, a duplikáció-napló „főtáblasor” oszlopából), `bdb_id`, `nyelv` (`aram`), `cimszo`, `szoveg_hasonlosag` (az ujjlenyomat-mérőszám), `proveniencia` (a mérés soráról: `scope=… | forras=eszkozok/bdb_aram_potlas.py --duplikacio | ts=…`).
- 6 szöveges pótlás a `konkordancia/BDB_teljes_unabridged.tsv` végére (az 5 részleges és a H6433), az `eszkozok/bdb_strong_potlas.py --m2` mintájára; a meglévő sorok bájtra azonosak maradnak.
- Új szkript és teszt (`eszkozok/bdb_aram_beemeles.py`, `eszkozok/teszt_bdb_aram_beemeles.py`): a beemelés reprodukálható, a bájtazonosság és a sorszámok tesztelve.
- A `BDB_teljes_unabridged_README.md` frissítése (új sorok, alias-bővülés).
- A #38 sorrendjének újragenerálása (l. 3. lépés: ⛔).

**Nincs benne:**

- A 164 duplikált sor szövegének új szövegsorként való beemelése (a döntés kizárja).
- H0004 (`cimke_reszleges`), H3769, H5013 (`csonk`): jelölt marad, nem kerül be.
- A #38 fordítási munkája (az arámi szócikkek fordítása a #38 dolga).
- A `BDB_strong_alias_elvetett.tsv` módosítása, hacsak a döntés egyértelműen nem követeli (l. nyitott kérdések).

## 3. Lépések (⛔ a kötelező megállások)

1. **M0, szárazfutás.** A szkript a 170 sorból kiszámolja a 164 alias-jelöltet (mérőszám ≥ 0,8, testvérsor azonosítva) és a 6 szöveges pótlást, a repón kívülre írva; összesítő: darabszámok, ütköző kulcs nincs, a testvérsor kulcsa minden alias-sornál létezik a fő táblában.
2. ⛔ **Jóváhagyás: a 6 szöveges pótlás és a 164 alias-sor.** A felhasználó a szárazfutás kivonatát (a 6 pótlás szövege, az alias-sorok mintája és számai) látja; jóváhagyás nélkül a fő tábla és az alias-tábla nem íródik.
3. **Írás.** Az alias-sorok az alias-tábla végére; a 6 pótlás a fő tábla végére; a meglévő sorok bájtra azonosak (teszt: a régi tartalom prefixként megegyezik). TSV-olvasás/írás `split('\t')` / `'\t'.join()`, nem `csv`.
4. ⛔ **A #38 sorrendjének újragenerálása.** A beemelés a #38 7. adagja ELŐTT fusson; utána a #38 sorrendjét újra kell generálni (a #38 saját briefje szerint). A #38 7. adaga ettől a feladattól függjön (a #38 fejlécébe `fugg` bővítés; a befogadáskor).
5. **Zárás.** `naplok/BDB_ARAM_BEEMELES_zaras.md` (≤20 sor): végszámok (alias: 164, szöveges: 6, jelölt: 3), SHA-256 előtte/utána; N51 lezárása helyőrzővel.

## 4. Elfogadási feltételek

- Az alias-tábla pontosan 164 új sorral nő; minden sor `tabla_strong` kulcsa létezik a fő táblában.
- A fő tábla pontosan 6 új sorral nő, a végén; a korábbi sorok bájtra azonosak.
- H0004, H3769, H5013 nem szerepel sem az alias-táblában, sem a fő táblában.
- Minden új sorban proveniencia (nem üres, nem „ellenőrizve”).
- A teszt zöld; a #38 sorrendje újragenerálva, a #38 7. adaga függ ettől a feladattól.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-06 | A 164 duplikált sor alias-sorként, a 6 valódi hiány szövegsorként; a beemelés a #38 7. adaga előtt; külön feladat. | felhasználó, chat (N51) |
| v2 | 2026-10-07 | A ⛔ 2. pont jóváhagyása: 6 pótlás + 162 alias; a H2298 (kezi_elfogadott) és a H5839 (feltételezett téves testvér) kizárva, jelölt: 5. | felhasználó, chat |
| v3 | 2026-10-07 | A két kizárás visszavonva (téves alapon álltak: a szöveg mindkét esetben a testvérsor végén van; a `kezi_elfogadott` döntés a szócikk-azonosításról szólt, nem a táblasorról). H5839 → H5838 (BDB9760): indokolt felülírás a szkriptben (`TABLA_FELULIR`); H2298 → H0259 (BDB9285): automatikus egyezés (0,947) a `KIZAR` kiürítése óta, felülírás nélkül. Eredmény: **164 alias + 6 pótlás, jelölt 3** (H0004, H3769, H5013). A H3606 → H3605 kézi ellenőrzése: elfogadva. A #38 sorrendjének újragenerálása jóváhagyva (a végleges alias-táblából, külön commit). | felhasználó, chat; ELLENOR_F72 |

**Nyitott kérdések (a befogadáskor):**

- `DT-F66b`/`N-F66c` (helyőrző): a 164 alias-sorból 162 a #57 elvetett táblájának `testver_strong` oszlopában is szerepel; az elvetett tábla soraira kell-e jelölés (pl. „beemelve”), vagy marad változatlan? Javaslat: marad változatlan, az alias-tábla a tény.
- A 2 alias-sor, amelynek testvére nem szerepel az elvetett táblában (164 − 162: H2298 → H0259 és H3606 → H3605): a `tabla_strong` kézi ellenőrzése kell-e? Javaslat: igen, a szárazfutás külön listázza. (Elvégezve, F72: mindkettő elfogadva.)
- Az 5 részleges sor szöveges pótlása a teljes arámi szócikk szövege, vagy csak a hiányzó rész? Javaslat: a teljes szócikk (a `--m2` minta szerint), a héber testvérsor érintetlen marad.
- A #38 jelenlegi adag-számozása (7. adag) a befogadáskor ellenőrizendő.
