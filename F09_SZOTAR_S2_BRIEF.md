---
feladat: 9
cim: Szótári adatréteg, 2. menet
kod: SZOTAR S2
tipus: feladat
fazis: 2
modell: sonnet
allapot: nem_indult
ad: az 1. fázis adatai — a 8 motívum Strongjaira szűkítve (DT-F52c (4)) — megjelennek a 8 lexikonoldalon a #78 szerepmátrix-vázának blokkjaiban és a 8 törzscikkben; a törzscikk utoljára itt generálódik (D34)
kovetkezo: Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi)
fugg: [5, 6, 23, 78]
olvas: [adat/forditasok.tsv, adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/, lexikon/, adat/szotar_szerepek.tsv, ADATVAGYON_TERV.md, MUNKATERV.md]
ir: [lexikon/, adat/kiejtes_kivetelek.tsv, adat/szotar_szerepek.tsv, eszkozok/torzscikk_general.py, eszkozok/lexikon_general.py, eszkozok/render_diff_osztalyoz.py, MUNKAMENET.md, NYITOTT_FELADATOK.md, adat/forditasok.tsv, eszkozok/kiejtes.py]
munka: adat
forras: F05_SZOTAR_BRIEF.md#2. menet — kimenet-változtató
nem_fugg: [7, 22, 38]
---

# F09_SZOTAR_S2_BRIEF — csonk

*FELADATOK #9 · fejlécet hordozó brief (F20 B3): a tényleges leírás az `F05_SZOTAR_BRIEF.md` 2. menete (`forras`), a végrehajtás az ott leírt lépések szerint történik.*

- **Mit ad, ha kész:** az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben; a törzscikk utoljára itt generálódik (D34)
- **Következő lépés:** Ez javítja a törzscikkek elavult Cremer-sorát is (a CI E11 szabálya jelzi)
- **Forrás:** `F05_SZOTAR_BRIEF.md#2. menet — kimenet-változtató`

A tartalmat az `F05_SZOTAR_BRIEF.md` 2. menete adja; ezt a fájlt a `/kovetkezo` a `forras` mező alapján olvassa.

**Kivétel (2026.10.06, felhasználói döntés):** az S2.6 (ISTENTISZT-001 2/b a tanulmányban, S12) nem ennek a feladatnak a része. A tematikus tanulmány prózáját írja, ezért `munka: ertelmezo` munka, és külön feladatként, a `/befogad`-dal kerül be. E nélkül a #9 `munka: adat`: a `tematikus_lezart/` fájlt nem írja. Az S2.8 újragenerálása a tanulmány akkori állapotából dolgozik; a `tanulmany` diff-kategória ezért üres is lehet. Az F05 K12 elfogadási feltétele a leválasztott feladathoz tartozik.
