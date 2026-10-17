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
forras: F05_SZOTAR_BRIEF.md#2. menet — kimenet-változtató
nem_fugg: [7, 22, 27, 38, 52, 55, 107, 109, 110]
---

# F09_SZOTAR_S2_BRIEF — csonk

*FELADATOK #9 · fejlécet hordozó brief (F20 B3): a tényleges leírás az `F05_SZOTAR_BRIEF.md` 2. menete (`forras`), a végrehajtás az ott leírt lépések szerint történik.*

- **Mit ad, ha kész:** az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben; a törzscikk utoljára itt generálódik (D34)
- **Következő lépés:** Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi)
- **Forrás:** `F05_SZOTAR_BRIEF.md#2. menet — kimenet-változtató`

A tartalmat az `F05_SZOTAR_BRIEF.md` 2. menete adja; ezt a fájlt a `/kovetkezo` a `forras` mező alapján olvassa.

**Kivétel (2026.10.06, felhasználói döntés):** az S2.6 (ISTENTISZT-001 2/b a tanulmányban, S12) nem ennek a feladatnak a része. A tematikus tanulmány prózáját írja, ezért `munka: ertelmezo` munka, és külön feladatként, a `/befogad`-dal kerül be. E nélkül a #9 `munka: adat`: a `tematikus_lezart/` fájlt nem írja. Az S2.8 újragenerálása a tanulmány akkori állapotából dolgozik; a `tanulmany` diff-kategória ezért üres is lehet. Az F05 K12 elfogadási feltétele a leválasztott feladathoz tartozik.
