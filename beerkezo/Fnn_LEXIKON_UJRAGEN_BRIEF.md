---
feladat:
cim: Az ISTENTISZT-001 lexikon-nézet újragenerálása a #110 jeloltek-deltája után, a DT-F127b-literál javításával
kod: LEXIKON_LITERAL_JAVITAS
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: nem_indult
ad: A kimeneti string-literálokban maradt, már kiosztott helyőrzők (DT-F127b → DT277) felmérve és javítva; a lexikon/ISTENTISZT-001_TUDOMANYOS.md a generátorból újra előáll, az E28 ismert kivétele megszűnik.
kovetkezo: Te: /befogad — a #110 (F110) merge-e után
olvas: [adat/jeloltek.tsv, adat/motivum_kapcsolatok.tsv, tematikus_lezart/ISTENTISZT-001_tematikus.md, motivumlog/ISTENTISZT-001.md, naplok/SZURO_PILOT_ISTENTISZT_naplo.md, eszkozok/lexikon_general.py, eszkozok/szamkiosztas.py, eszkozok/ellenorzes/szabalyok.py]
ir: [eszkozok/lexikon_general.py, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
fugg: [110]
---

# Fnn_LEXIKON_UJRAGEN_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

Eredet: az F110 javítókör 1. és 2. köre (ELLENOR_F110 E28; ELLENOR_F110_2 1. és 6.). A `tematikus_lezart/` és `motivumlog/` útvonalat a befogadáskor ellenőrizni kell (a motívum tényleges tanulmány- és naplófájlja).

## Háttér

Az F110 a `jeloltek.tsv`-ben az ISTENTISZT-001 sorait módosította (21 G1941-sor elutasítva, 2 új `nyitva` H7121+H8034-sor: Ézs 41:25, Ézs 64:6). A `lexikon/ISTENTISZT-001_TUDOMANYOS.md` generált nézet (E28), ezért újra kellene generálni. A fix dátumú (`PARDES_DATUM=2026-10-20`) generátor-diff 2 sor: a `kizart` blokk jelöltszáma 91 → 93 (az F110 deltája) és a `kapcsolodo` blokk magyarázó sorában `DT277` → `DT-F127b`.

A második sor main-beli hiba: a `szamkiosztas` Action (57f41f24, `DT-F127b → DT277`) a `.md`/`.tsv` helyőrzőket átszámozta, a `.py` kimeneti string-literálokat nem. A sodródás forrása az `eszkozok/lexikon_general.py:2116` literálja. A **változatlan generátor a DT-F127b helyőrzőt írná vissza a lexikonba a kiosztott DT277 helyére.** Ezért az F110 ágán a lexikon érintetlen maradt (felhasználói döntés, (b) eset).

## Felmérés (az F110 2. körében, origin/main-en, `git grep` + AST)

A `DT-F127b` az `eszkozok/*.py`-ban **14 fájlban** szerepel. Ebből:

| fajta | fájl : sor | kimenetbe kerül? |
|---|---|---|
| string-literál | `lexikon_general.py:2115` (a szöveg a 2116. sorban) | **igen**: a lexikon `kapcsolodo` blokkja (ez okozza az E28 sodródást) |
| string-literál | `f127_jeloltek_bovit.py:30` (`UJ_KOMMENT`) | igen, ha újrafuttatják: az `adat/jeloltek.tsv` fejléksora (a main-en most `DT277`) |
| string-literál | `ellenoriz.py:207, 236, 264` | igen: az ellenőrző stdout-üzenetei (cím, hibaüzenet), nem adatfájl |
| docstring | `ellenoriz.py:198`, `f127_jeloltek_bovit.py:1`, `f127_res_eles.py:1`, `karoli_ellenorzes.py:75`, `lexikon_general.py:2122`, `nem_vizsgalt.py:156` | nem (dokumentáció) |
| csak megjegyzés (`#`) | `betolt, ellenoriz, ellenorzes/szabalyok, f127_res_eles, general, jelolt, karoli_ellenorzes, lexikon_general, nem_vizsgalt, sqlite_epit, teszt_general_ellenorzo, teszt_sqlite_epit, torzscikk_general` (összesen 31 megjegyzéssor) | nem |

Tehát 5 kimeneti string-literál van 3 fájlban; a többi megjegyzés vagy docstring.

## Lépések (terv)

1. **Felmérés újra** a befogadáskor, a main aktuális állapotán (`git grep -n "DT-F127b" -- 'eszkozok/*.py'`, AST-os szűrés a literálokra); a fenti számok csak az F110 2. körének pillanatképei.
2. ⛔ **Döntés (javaslattal): hogyan akadályozzuk meg az ismétlődést?**
   - (a) **CI-szabály** (javaslat): új E-szabály, amely jelzi, ha egy `eszkozok/*.py` string-literáljában (nem megjegyzésben) olyan `DT-F`/`N-F`/`D-F` helyőrző áll, amelyhez a `DONTESEK.md`/`NYITOTT_FELADATOK.md`/`FELADATOK.md` már végleges számot rendelt. Indok: a `.py` automatikus átírása kódot módosít, a szabály csak jelez, és nem érint megjegyzést/docstringet.
   - (b) a `szamkiosztas.py` kiterjesztése `.py` fájlokra (csak string-literálok, AST alapján). Kockázat: automatikus kódmódosítás a main-en, `.py` fájlok commitja az Action-ből.
   - (c) mindkettő.
3. A 2. lépés döntése szerint megvalósítani; a literálokat (a felmérés 5 sora) a kiosztott számra (DT277) javítani, vagy a generátor/ellenőrző szövegét számfüggetlenné tenni.
4. **Elfogadási feltétel:** a literál javítása után a `main`-en futtatott `python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --ir` (fix `PARDES_DATUM`) a `ts=` jelölőkön kívül **0 sort változtathat** a sodródáson kívül, vagyis a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` diffje üres. Az F110 deltája (91 → 93) csak az **F110 merge-e után** jelenhet meg.
5. Az F110 merge-e után a lexikon újragenerálása; a diff elvárt tartalma csak a `kizart` blokk száma (91 → 93) és a `ts=` jelölők. Ha más (rés, motívum) is változik, megállni és a tartalmi okot döntésre vinni.
6. Az E28 ismert kivételének (F110) lezárása.

Tiltás: a generált fájlt kézzel szerkeszteni tilos (CLAUDE.md, kimenet-réteg).
