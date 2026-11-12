---
feladat: 215
cim: Az olvasó angol Thayer- és BDB-szövege a javított adatból
kod: ANGOL_BDB_THAYER
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/f215-angol-bdb-thayer-357f75
ad: az olvasó angol Thayer-blokkja a thayer_forras_javitas mind a 15 beszúrását tartalmazza; az angol BDB hivatkozás-javításáról mérés igazolja, hogy a DB szövege már a javított; a fogyasztók listája a nyers táblák olvasóiról
kovetkezo: "Te: a draft PR átnézése; merge az orkesztrátoré"
munka: adat
olvas: [CLAUDE.md, NYITOTT_FELADATOK.md, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/thayer_jelolt/thayer_bemenet.py, eszkozok/bdb_jelolt/szakasz_bemenet.py, adat/thayer_forras_javitas.tsv, adat/bdb_forras_javitas.tsv]
ir: [eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_angol_javitott.py, eszkozok/olvaso_szerver/README.md, naplok/F215_jelentes.md, F215_ANGOL_BDB_THAYER_BRIEF.md]
lezarva_osszegzes: "angol Thayer: a 15 beszúrás a lekérdezésben (thayer_forras_javitas a DB-ből), 15 Strong változott; angol BDB: a hivatkozás-javítás a DB szövegében már benne van, 0 Strong változott, teszt őrzi"
fugg: []
---

# F215_ANGOL_BDB_THAYER_BRIEF.md — az olvasó angol Thayer- és BDB-szövege a javított adatból

*FELADATOK #215 · Modell: sonnet · v1 · 2026.11.12*

## 1. Cél

A bekötési audit (2026-11-12, `FELMERES_BDB_THAYER_KJV_2026-11-12.md` 1. rész) szerint az olvasó angol Thayer-szövege nyers (a `thayer_forras_javitas` 15 beszúrása nem látszik), és az angol BDB-re a `hivatkozas` javítások (412 sor, 247 Strong) nem futnak. A szabály: javított adat → minden fogyasztó a javítottat olvassa.

## 2. Hatókör

**Benne van.** `eszkozok/olvaso_szerver/lekerdezesek.py` (`thayer`, `bdb_angol`), új teszt, README-sor, jelentés; a nyers `thayer`/`bdb` táblát olvasó fogyasztók listája.

**Nincs benne.** A `lexikon_general.py` (az F212 írja); `sqlite_epit.py` (nem kellett); a pe/mem-ütközések finomítása a BDB-ben (külön tétel).

## 3. Lépések

1. A Thayer-javítás helye: lekérdezés vs db-építés (a választás indoka: `naplok/F215_jelentes.md`).
2. A BDB-hivatkozás: a javítótábla alkalmazhatóságának mérése az angol `bdb.teljes_szocikk`-re. ⛔ Ha a mérés a felmérés feltevését cáfolja, nem alkalmazunk javítást: jelentés.
3. Teszt, mérés, fogyasztó-lista, draft PR.

## 4. Elfogadási feltételek

A `szo.thayer` blokk szövege mind a 15 beszúrást tartalmazza; a BDB-hivatkozás javított alakja áll (H0026); a mérés számai és a fogyasztó-lista a jelentésben; draft PR zöld CI-vel.

## 5. Döntésnapló

Az 1. lépés választása és a 2. lépés ⛔ pontja a jelentésben (nem tartalmi döntés: a mérés eldönti).
