---
feladat: 101
cim: Az olvasó adatbázisának automatikus újraépítése — ha az adat (BDB-fordítás, Strong-párok …) előrehalad, a szerver magától friss adatot mutasson
kod: ADATBAZIS_FRISSITES
tipus: feladat
fazis: 1
modell: sonnet
munka: folyamat
allapot: nem_indult
ad: az indító (indit.sh) észleli, ha a pardes.db régebbi a forrás-tábláinál (adat/, konkordancia/), és magától újraépíti (sqlite_epit.py, integritás-ellenőrzéssel), csak siker után cserél; a lábléc kiírja, ha az adatbázis régebbi az adatnál, és ha az újraépítés elbukott, miért; negyedik asztali parancsikon a kézi újraépítéshez
kovetkezo: Halasztva: a #99 (BDB_SZELETELO) lezárásáig — a #99 az eszkozok/sqlite_epit.py-t olvassa, a #101 írja, és a felhasználó döntése szerint a #99 jön előbb; utána /kovetkezo; ⛔ M0 (mérés, DT-F101a–b), ⛔ M2 (a felhasználó kipróbálja)
olvas: [eszkozok/olvaso_szerver/README.md, naplok/SQLITE_EPIT_meres.md, naplok/OLVASO_INDITO_zaras.md, eszkozok/olvaso_szerver/manifest_pardes_db.tsv]
ir: [eszkozok/olvaso_szerver/indit.sh, eszkozok/olvaso_szerver/allapot.py, eszkozok/olvaso_szerver/teszt_indito.py, eszkozok/olvaso_szerver/README.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, naplok/ADATBAZIS_FRISSITES_zaras.md]
fugg: []
nem_fugg: [76]
---

# F101_ADATBAZIS_FRISSITES_BRIEF.md — Az olvasó adatbázisának automatikus újraépítése

*Befogadásra váró brief-tervezet · v1 · 2026.10.15 · forrás: a felhasználó kérdése a chatben (2026-10-15): „ha az adatbázis frissül, pl. halad előre a BDB-fordítás vagy a Strong-ozás, hogyan frissül a szerver adatbázisa?” — és a kérés, hogy ez is automatikus legyen (a #100 OLVASO_INDITO folytatása: „én ezt nem tudom észben tartani, mikor mit kell indítani”).*

**Javasolt fejléc-adatok:** `modell: sonnet` (szkript- és ellenőrzés-bővítés, értelmező munka nincs) · `munka: folyamat` · az `ir` az `eszkozok/olvaso_szerver/` néhány fájlját és az `eszkozok/sqlite_epit.py`-t írja — a #99 és a #76 a szerverkönyvtárat, a #93 és a #99 a `sqlite_epit.py`-t is írja; a sorrendet a `/befogad` függés-számítása adja.

## 1. Háttér

A szerver adatának útja (2026-10-15, a #100 után):

1. **Az adat változik:** a feladatok a `main`-re mergelnek (pl. a #38 BDB-fordítás adagja az `adat/forditasok.tsv`-be, a Károli–Strong párosítás az `adat/karoli_strong/`-ba).
2. **Az adatbázis újraépül:** az `eszkozok/sqlite_epit.py` a TSV-kből építi a `pardes.db`-t (a repó gyökerében, nem commitolt, generált nézet, DT28), integritás-ellenőrzéssel, és beírja a `meta.epites_ts`-t. **Ma ezt kézzel kell futtatni; senki nem indítja.**
3. **A szerver átveszi:** az `indit.sh` (#100) az indításkor összeveti a Windows-oldali és a WSL-beli (`~/pardes/pardes.db`) példány `meta.epites_ts`-ét, és eltérésnél másol; a lábléc figyelmeztet, ha a Windows-oldali példány újabb a futó másolatnál.

Ha a 2. lépés elmarad, a szerver a régi adatot mutatja, és erre semmi nem figyelmeztet: a lábléc csak a két adatbázis-példányt veti össze, a forrás-táblákat nem. Mért építési idő (`naplok/SQLITE_EPIT_meres.md`): 50–84 s integritás-ellenőrzés nélkül.

## 2. Cél

- **Észlelés:** az indító és a lábléc tudja, ha a `pardes.db` régebbi a forrásainál (az `sqlite_epit.py` által olvasott `adat/` és `konkordancia/` fájlok).
- **Automatikus újraépítés:** ha a források újabbak, az indító (parancsikon vagy bejelentkezéskori ütemezett feladat, #100 DT-F100b) újraépít, és csak siker után cseréli az adatbázist; a szerver közben a régi, ép adatbázissal indul vagy fut tovább, nem vár percekig.
- **Hiba esetén:** az integritás-ellenőrzés bukásakor marad a régi adatbázis, a lábléc kiírja, hogy az újraépítés elbukott és hol a napló.
- **Kézi lehetőség:** negyedik asztali parancsikon „PaRDeS adatbázis újraépítése”.

## 3. Hatókör

- **Benne:**
  - a forrás-állapot rögzítése építéskor: az `sqlite_epit.py` a `meta` táblába írja a betöltött forrásfájlok azonosítóját (útvonal + méret + `sha256` vagy legalább módosítási idő; az M0 dönt, DT-F101a), hogy az észlelés ne a fájl mtime-ján múljon;
  - `allapot.py`: „az adatbázis régebbi az adatnál” döntés (a forrásfájlok mostani azonosítója vs. a `meta`-ban rögzített), olcsón (nem olvassa be a 938 MB-ot, és a TSV-ket sem, ha az mtime+méret egyezik);
  - `indit.sh`: ha a források újabbak → háttérben újraépítés (zárral, egyszerre egy), ideiglenes névre, integritással; siker → atomi átnevezés a Windows-oldali `pardes.db` helyére, majd a WSL-másolat frissítése a meglévő (#100) úton; a szerver a régi példánnyal indul, és a lábléc mutatja, hogy építés fut;
  - lábléc: „az adatbázis régebbi az adatnál”, „újraépítés folyamatban (kezdete)”, „az újraépítés elbukott (napló: …)”;
  - negyedik parancsikon (a felhasználó asztalán, a repón kívül; a #100 `-e bash -lc` formájában);
  - tesztek (`teszt_indito.py`, `teszt_sqlite_epit.py`) ideiglenes forrásokkal és adatbázissal.
- **Nincs benne:**
  - az `sqlite_epit.py` tartalmi (tábla-, séma-) változtatása a forrás-azonosítón túl;
  - CI-ben futó építés (a `pardes.db` nem commitolt);
  - a #38 és más adatfeladatok munkamenete (azok nem futtatnak építést).

## 4. Lépések

### M0 — mérés ⛔

1. Az építés ideje integritás-ellenőrzéssel együtt, Windows-on (Python 3.14, a repó gyökerébe) és a WSL-ben (a projekt venv-jével, natív kimenetre, majd másolással) — melyik gyorsabb és megbízhatóbb.
2. A forrás-észlelés: az `sqlite_epit.py` által ténylegesen olvasott fájlok listája (a kód `DATASETEK`-szerű listáiból és az `adat/` táblákból), darab és összméret; a teljes `sha256` ideje vs. mtime+méret.
3. ⛔ **DT-F101a:** a forrás-azonosító módja ((a) mtime+méret, ütközéskor `sha256`; (b) mindig `sha256`; (c) csak mtime). **DT-F101b:** hol fusson az automatikus építés ((a) WSL venv, natív ideiglenes kimenet, utána másolás a Windows-oldalra; (b) Windows Python, közvetlenül a repó gyökerébe; (c) a mérés szerinti gyorsabb), és fusson-e bejelentkezéskor is, vagy csak parancsikonra. Megállás.

### M1 — megvalósítás

1. `sqlite_epit.py`: a forrás-azonosítók a `meta`-ba; teszt.
2. `allapot.py`, `indit.sh`, lábléc; teszt ideiglenes forrásokkal (forrás változik → építés → csere; integritás bukik → régi marad, lábléc hibát mutat; két egyidejű indítás → egy építés).
3. A negyedik parancsikon; README.

### M2 — próba ⛔

1. Gépi próba: egy `adat/` tábla módosítása egy ideiglenes példányon → a lábléc „régebbi az adatnál”, az indító újraépít, a lap az új adatot mutatja.
2. ⛔ A felhasználó kipróbálja: egy valódi adatváltozás (pl. egy BDB-adag merge-e) után az ikon vagy a bejelentkezés frissíti az adatot, és a lábléc mutatja. Megállás; zárónapló.

## 5. Elfogadási feltételek

- Ha egy forrás-tábla változik, a lábléc legfeljebb 3 másodpercen belül jelzi, hogy az adatbázis régebbi az adatnál; ha nem változott, nem jelez.
- Az indító újraépít, ha kell, és a szerver addig a régi, ép adatbázissal válaszol (a lap az építés alatt is betölt); siker után a lap az új adatot mutatja újabb kattintás nélkül vagy egyetlen kattintással (az M0 döntése szerint).
- Integritás-hiba esetén a régi adatbázis érintetlen, a lábléc a hibát és a napló helyét mutatja.
- Két egyidejű indítás egyetlen építést indít (zár).
- A meglévő tesztek zöldek; a regiszter-őr zöld (a lábléc új elemei regisztrálva vagy kizárva).

## 6. Döntésnapló

- **DT-F101a** (M0): a forrás-azonosító módja.
- **DT-F101b** (M0): hol és mikor fusson az automatikus építés.
