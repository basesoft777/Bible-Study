---
feladat: 62
cim: Egységes Strong-normalizáló függvény — egyetlen strong_normalizal() a lekérdezőben és a betöltőben
kod: STRONG_NORMALIZAL
tipus: feladat
fazis: folyamat
modell: sonnet
munka: folyamat
allapot: nem_indult
ad: egyetlen, tesztelt strong_normalizal() függvény (eszkozok/strong_util.py) a SEMA 1.2 alakra (H/G + négy számjegy, balról nullázva, + láncok), amelyet a lekerdez.py és a betolt.py használ; a többi saját normalizáló leltárba kerül, és az adattáblákon gépi ellenőrzés igazolja, hogy nincs SEMA 1.2-nek nem megfelelő Strong-érték
kovetkezo: /kovetkezo; ⛔ az M0 után (a leltár és a bemeneti alakok elfogadása)
olvas: [adat/SEMA.md, eszkozok/lekerdez.py, eszkozok/betolt.py, eszkozok/ellenoriz.py, eszkozok/lxx_osszevetes.py, eszkozok/merge_karoli_szofaj.py, eszkozok/tw_import.py, eszkozok/tbesh_konszolidalt_import.py, eszkozok/teszt_lekerdez_sir.py, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/lexikon_hivatkozasok.tsv, adat/grammatikai_strongok.tsv, konkordancia/Karoli_Strong_kivonat.tsv, NYITOTT_FELADATOK.md]
ir: [eszkozok/strong_util.py, eszkozok/teszt_strong_util.py, eszkozok/lekerdez.py, eszkozok/betolt.py]
fugg: []
nem_fugg: [54, 61, 63, 65]
---

# F62_STRONG_NORMALIZAL_BRIEF.md — Egységes Strong-normalizáló függvény

*FELADATOK #62 · Modell: sonnet · v1 · 2026.10.05 · forrás: `MUNKATERV.md` 4. szakasz (STRONG_NORMALIZAL, 1. hullám), `NYITOTT_FELADATOK.md` N37 és N21, `ADATVAGYON_TERV.md` 1. szakasz 5. pont*

## 1. Cél

A SEMA 1.2 szerint a Strong-szám `H` vagy `G` + négy számjegy, balról nullázva (`H0779`), több szám egy cellában `+` jellel. A projektben ma nincs egyetlen függvény, amely ezt az alakot előállítja: az N37 legalább hét önálló implementációt számolt össze (pl. `lxx_osszevetes.py`, `merge_karoli_szofaj.py`, `tw_import.py`, `tbesh_konszolidalt_import.py`), és ugyanez a hibaosztály okozta az N21-et (`H922` a `H0922` helyett) és a `tw_import.py` első verziójának `G00120` → `G0120` hibáját.

A feladat egy közös függvényt ad, és a két központi eszközbe (lekérdező, betöltő) beköti. A munkaterv szerint ez minden későbbi betöltés, köztük az SQLITE_EPIT előfeltétele.

**Állapot a befogadáskor (2026.10.05):** az N21 adatjavítása már megtörtént (KB3, `4ecb612`: a `Karoli_Strong_kivonat.tsv` 26 sora). Az `adat/*.tsv` és a `Karoli_Strong_kivonat.tsv` Strong-oszlopaiban a befogadáskori mérés nem talált SEMA 1.2-nek nem megfelelő értéket; nullázatlan kód csak a szótári forrásszöveg szabad szövegében áll (pl. „from H215”), az nem normalizálandó. A munkaterv „N21 nullázatlan értékek javítása” része ezért várhatóan tárgytalan; az M0 ezt igazolja.

## 2. Hatókör

**Benne van:**
- `eszkozok/strong_util.py`: `strong_normalizal(s)` (egy kód vagy `+` lánc → SEMA 1.2 alak), és egy érvényességet vizsgáló párja (`strong_ervenyes(s)`);
- a bemeneti alakok, amelyeket az M0 leltára talál a projekt forrásaiban (pl. nullázatlan `H922`, öt számjegyű `G00120`, kisbetű, szóköz, `+` lánc), mindegyik teszttel;
- a `lekerdez.py` és a `betolt.py` saját Strong-kezelésének cseréje erre a függvényre, viselkedésváltozás nélkül;
- gépi ellenőrzés az M0-ban: minden `adat/*.tsv` Strong-oszlop és a `Karoli_Strong_kivonat.tsv` Strong-oszlopa SEMA 1.2 szerint;
- `eszkozok/teszt_strong_util.py`.

**Nincs benne:**
- a többi meglévő normalizáló (az N37 listája és amit az M0 még talál) cseréje: ezek leltárba kerülnek, a csere külön tétel (`/befogad`), mert egyszeri import-szkriptek, és a cseréjük a régi kimenetek újragenerálását is felvetné;
- adattábla írása: ha az M0 mégis talál nem megfelelő értéket, ⛔, és a javítás külön döntés;
- új CI-szabály (ha az M0 javasolja, külön tétel; a CI-szabályfájlt a #30, #37, #40, #51 is írja);
- szabad szövegű mezők (szótári forrásszöveg, `kapcsolodas`, `indoklas`) Strong-hivatkozásai.

## 3. Lépések

### M0 — Leltár, mérés és ⛔

Jelentés: `naplok/STRONG_NORMALIZAL_M0.md`.
1. Az összes Strong-normalizáló implementáció az `eszkozok/` alatt, kereséssel (`grep`; az `olvas` lista csak a ma ismert fájlokat nevezi meg, hogy ne kössön függést minden eszközt író feladatra) (függvénynév, fájl, milyen bemenetet fogad, mit ad, eltér-e a SEMA 1.2-től).
2. A bemeneti alakok leltára: milyen Strong-alakok jönnek a datasetekből és a kézi forrásokból (a munkaterv „20 ismert eltérő alak” kis mintája ennek a listának a része; ha az M0 más számot talál, a mért szám érvényes).
3. Mérés: minden `adat/*.tsv` Strong-oszlop (az `olvas` lista a befogadáskor Strong-oszlopot hordozó táblákat nevezi meg; ha az M0 többet talál, a jelentés felsorolja) és a `konkordancia/Karoli_Strong_kivonat.tsv` Strong-oszlopa a SEMA 1.2 ellen (a TSV-olvasás `split('\t')`, a `csv` modul tilos, CLAUDE.md). Az eredmény akkor is a jelentésbe kerül, ha 0.
4. A `lekerdez.py` és a `betolt.py` mai Strong-kezelése: hol normalizál, hol hasonlít össze, milyen kimenetet ad.

**⛔ Megállás:** a felhasználó elfogadja (a) a bemeneti alakok listáját és a függvény elvárt kimenetét alakonként, (b) a 3. pont eredményét. Ha a 3. pont nem 0, a javítás módjáról ő dönt (külön tétel vagy e feladat bővítése).

### M1 — A függvény és a tesztek

- `strong_normalizal()`: minden M0-beli alakra a SEMA 1.2 alak; érvénytelen bemenetnél kivétel, nem csendes csonkolás (a `G00120` esete: öt számjegynél a vezető nulla elhagyható, nem nulla vezető számjegy hiba).
- `teszt_strong_util.py`: alakonként egy teszt, plusz a `+` lánc sorrendjének megőrzése és az idempotencia (`f(f(x)) == f(x)`).
- A modul a CLAUDE.md szerinti kódolási őrt viseli (az importok után).

### M2 — Bekötés

- A `lekerdez.py` és a `betolt.py` a közös függvényt hívja. **Viselkedésváltozás nincs:** a `teszt_lekerdez_sir.py` és a meglévő tesztek változatlanul zöldek; a `betolt.py` szárazfutása (ha van ilyen mód, egyébként ideiglenes könyvtárba, a repón kívülre) bájtra azonos kimenetet ad.

### M3 — Zárás

`naplok/STRONG_NORMALIZAL_zaras.md` (≤20 sor: a leltár összegzése, a csere-javaslat a többi implementációra), `fuggetlen-ellenor` (`naplok/ELLENOR_STRONG_NORMALIZAL.md`), a brief fejléce `lezarva`, push, draft PR. A zárás javaslatot tesz az N21 lezárására a `NYITOTT_FELADATOK.md`-ben, ha az M0 3. pontja 0.

## 4. Elfogadási feltételek

- **K1.** Egy függvény, minden M0-beli bemeneti alakra teszttel; az idempotencia-teszt zöld.
- **K2.** A `lekerdez.py` és a `betolt.py` csak ezt a függvényt használja Strong-normalizálásra; kimenetük változatlan.
- **K3.** Az adattáblák mérése dokumentált (0 találat is); adattábla nem változott.
- **K4.** Az `ellenoriz.py` és a CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A munkaterv „N21 nullázatlan értékek javítása” része a KB3 (`4ecb612`) óta várhatóan tárgytalan; a feladat adattáblát nem ír, az M0 mér. | befogadás, mérés 2026-10-05 |
| v1 | 2026-10-05 | A többi normalizáló cseréje nem e feladat része; leltár és javaslat. | befogadás |
