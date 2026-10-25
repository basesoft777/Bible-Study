---
feladat: 141
cim: A kimeneti literálokban maradt kiosztott helyőrzők (DT-F127b) felmérése, javítása és az ismétlődés megelőzése
kod: LEXIKON_LITERAL_JAVITAS
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: megallt
ag: ccr-6c9c92aa-tnvazz
ad: A kimeneti string-literálokban maradt, már kiosztott helyőrzők (DT-F127b → DT277) felmérve és javítva (a lexikon_general.py:2116 már az F110.29-ben); döntés és megvalósítás az ismétlődés megelőzésére; a 8 érintett lexikonoldal újragenerálása 0-diffet ad.
kovetkezo: "Te: [elteres_kor 0/2] /elteres 141"
lezarva_osszegzes: "E32 CI-szabály (új sorra HIBA, régire JELENTÉS; 15 teszt) és a 4 maradék kimeneti literál javítva (DT-F127b → DT277); a 4. lépés feltétele a DT-F141b szerint a DT277 sor nem-sodródására szűkítve, a 7 elavult lexikonlap újragenerálása a #36/#143 dolga; 70 meglévő literál külön feladat (naplok/F141_zaras.md)."
olvas: [eszkozok/ellenoriz.py, eszkozok/f127_jeloltek_bovit.py, eszkozok/szamkiosztas.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/lexikon_general.py, DONTESEK.md, naplok/SZURO_PILOT_ISTENTISZT_zaras.md, naplok/ELLENOR_F110_4.md]
ir: [eszkozok/ellenoriz.py, eszkozok/f127_jeloltek_bovit.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/szamkiosztas.py]
fugg: [110]
nem_fugg: [121, 131]
---

# Fnn_LEXIKON_UJRAGEN_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

Eredet: az F110 javítókör 1. és 2. köre (ELLENOR_F110 E28; ELLENOR_F110_2 1. és 6.). **Frissítve az F110.29–30 után:** az ISTENTISZT-001 lexikon-sodródása az F110 ágán megoldódott (l. alább), a tervezet a maradékot fedi. Az `olvas` a szűkített hatókört fedi (a maradék literálok fájljai, a `szamkiosztas` és a CI-szabályok); befogadáskor újra ellenőrizni.

## Háttér

Az F110 a `jeloltek.tsv`-ben az ISTENTISZT-001 sorait módosította (21 G1941-sor elutasítva, 2 új `nyitva` H7121+H8034-sor: Ézs 41:25, Ézs 64:6). A `lexikon/ISTENTISZT-001_TUDOMANYOS.md` generált nézet (E28), ezért újra kellett generálni. Az F110 2. körében a fix dátumú (`PARDES_DATUM=2026-10-20`) generátor-diff 2 sor volt: a `kizart` blokk jelöltszáma 91 → 93 (az F110 deltája) és a `kapcsolodo` blokk magyarázó sorában `DT277` → `DT-F127b`.

A második sor main-beli hiba: a `szamkiosztas` Action (57f41f24, `DT-F127b → DT277`) a `.md`/`.tsv` helyőrzőket átszámozta, a `.py` kimeneti string-literálokat nem. A sodródás forrása az `eszkozok/lexikon_general.py:2116` literálja. A **változatlan generátor a DT-F127b helyőrzőt írná vissza a lexikonba a kiosztott DT277 helyére.** Az F110 ágán a lexikon előbb érintetlen maradt (felhasználói döntés, (b) eset), majd a felhasználó kérésére az **F110.29** javította a `lexikon_general.py:2116` literálját (`DT277`), és újragenerálta az ISTENTISZT-001 lapját; a diff pontosan az F110 deltája lett, az E28 megszűnt. Az újragenerált lapon az E11 a G1941 magyar szótárfordításában tiltott Cremer-említést talált; az **F110.30** ezt a felhasználó döntésével törölte az `adat/forditasok.tsv`-ből.

## Felmérés (az F110 2. körében, origin/main-en, `git grep` + AST)

A `DT-F127b` az `eszkozok/*.py`-ban **14 fájlban** szerepel. Ebből:

| fajta | fájl : sor | kimenetbe kerül? |
|---|---|---|
| string-literál | `lexikon_general.py:2115` (a szöveg a 2116. sorban) | **igen**: a lexikon `kapcsolodo` blokkja — **javítva az F110.29-ben** (`DT277`) |
| string-literál | `f127_jeloltek_bovit.py:30` (`UJ_KOMMENT`) | igen, ha újrafuttatják: az `adat/jeloltek.tsv` fejléksora (a main-en most `DT277`) |
| string-literál | `ellenoriz.py:207, 236, 264` | igen: az ellenőrző stdout-üzenetei (cím, hibaüzenet), nem adatfájl |
| docstring | `ellenoriz.py:198`, `f127_jeloltek_bovit.py:1`, `f127_res_eles.py:1`, `karoli_ellenorzes.py:75`, `lexikon_general.py:2122`, `nem_vizsgalt.py:156` | nem (dokumentáció) |
| csak megjegyzés (`#`) | `betolt, ellenoriz, ellenorzes/szabalyok, f127_res_eles, general, jelolt, karoli_ellenorzes, lexikon_general, nem_vizsgalt, sqlite_epit, teszt_general_ellenorzo, teszt_sqlite_epit, torzscikk_general` (összesen 28 megjegyzéssor) | nem |

Tehát 5 kimeneti string-literál volt 3 fájlban; ebből 1 (lexikon_general.py) az F110.29-ben javítva, 4 maradt 2 fájlban (`ellenoriz.py`, `f127_jeloltek_bovit.py`); a többi megjegyzés vagy docstring.

## Lépések (terv)

1. **Felmérés újra** a befogadáskor, a main aktuális állapotán (`git grep -n "DT-F127b" -- 'eszkozok/*.py'`, AST-os szűrés a literálokra); a fenti számok csak az F110 2. körének pillanatképei.
2. ⛔ **Döntés (javaslattal): hogyan akadályozzuk meg az ismétlődést?**
   - (a) **CI-szabály** (javaslat): új E-szabály, amely jelzi, ha egy `eszkozok/*.py` string-literáljában (nem megjegyzésben) olyan `DT-F`/`N-F`/`D-F` helyőrző áll, amelyhez a `DONTESEK.md`/`NYITOTT_FELADATOK.md`/`FELADATOK.md` már végleges számot rendelt. Indok: a `.py` automatikus átírása kódot módosít, a szabály csak jelez, és nem érint megjegyzést/docstringet.
   - (b) a `szamkiosztas.py` kiterjesztése `.py` fájlokra (csak string-literálok, AST alapján). Kockázat: automatikus kódmódosítás a main-en, `.py` fájlok commitja az Action-ből.
   - (c) mindkettő.
3. A 2. lépés döntése szerint megvalósítani; a maradék literálokat (a felmérés 4 sora) a kiosztott számra (DT277) javítani, vagy az ellenőrző szövegét számfüggetlenné tenni.
4. **Elfogadási feltétel:** a 8 érintett lexikonoldal (ALVIL, ANTROP, HAMART, HODIT, KIRALY, ISTENTISZT, MENNY, TEREMT-001; grep `beépített motívumközi jelölt áll, DT` a `lexikon/` alatt) a `main`-en futtatott `python eszkozok/general.py --cel lexikon --id <ID> --ir` (fix `PARDES_DATUM`) után a `ts=` jelölőkön kívül **üres diffet** ad; ha bármelyik lap változik, megállni, és a tartalmi okot döntésre vinni.
5. Az ismétlődés-megelőzés (2. lépés) tesztje: egy szándékosan visszaírt, már kiosztott helyőrző a kimeneti literálban jelzést ad (CI-szabály), illetve átszámozódik (`szamkiosztas`), megjegyzésben és docstringben nem.

Tiltás: a generált fájlt kézzel szerkeszteni tilos (CLAUDE.md, kimenet-réteg).
