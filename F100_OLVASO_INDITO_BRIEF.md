---
feladat: 100
cim: Az olvasó-szerver automatikus indítása — friss kód, friss adatbázis, egy kattintás; tesztek natív fájlokból
kod: OLVASO_INDITO
tipus: feladat
fazis: 1
modell: sonnet
munka: folyamat
allapot: nem_indult
ad: egy közös indító-szkript, amelyet a három asztali parancsikon hív: leállítja a régi példányt, a WSL-beli pardes.db-t a Windows-oldalihoz igazítja (csak eltérésnél másol), és kódváltozáskor magától újrainduló szervert indít; a lap láblécében ág, kódverzió és adatbázis, figyelmeztetéssel, ha valami nem friss; a tesztek egyetlen belépési pontról, natív fájlokból futnak
kovetkezo: /kovetkezo; ⛔ M0 (a felmérés és a DT-F100a–b), ⛔ M2 (a felhasználó kipróbálja a parancsikonokat)
olvas: [eszkozok/olvaso_szerver/README.md, eszkozok/olvaso_szerver/frissesseg.py, eszkozok/olvaso_szerver/manifest_pardes_db.tsv, eszkozok/olvaso_szerver/pyproject.toml]
ir: [eszkozok/olvaso_szerver/indit.sh, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/teszt_indito.py, eszkozok/olvaso_szerver/README.md, eszkozok/teszt_futtat.py, CLAUDE.md, naplok/OLVASO_INDITO_zaras.md]
fugg: []
nem_fugg: [76]
---

# F100_OLVASO_INDITO_BRIEF.md — Az olvasó-szerver automatikus indítása

*Befogadásra váró brief-tervezet · v1 · 2026.10.15 · forrás: a felhasználó kérése a chatben (2026-10-15): „automatikus legyen, én ezt nem tudom észben tartani, mikor mit kell indítani”; a három asztali parancsikon maradjon.*

**Javasolt fejléc-adatok:** `modell: sonnet` (szkript és kis szerver-módosítás, értelmező munka nincs) · `munka: folyamat` · `ir`: az `eszkozok/olvaso_szerver/` néhány fájlja — a #76 és a #99 ugyanezt a könyvtárat írja, a sorrendet a `/befogad` függés-számítása adja.

## 1. Háttér

A felhasználó az olvasó-szervert három asztali parancsikonnal indítja (`PaRDeS olvaso - belso (tervezo).bat` → 8765, `nyilvanos` → 8766, `kereskedelmi` → 8768). Mindhárom a WSL `pardes` disztribúcióban, a projekt venv-jével (Python 3.12) futtatja az `alkalmazas.py`-t, a kódot a Windows-checkoutból (`/mnt/c/…`), az adatbázist a WSL saját példányából (`PARDES_DB=$HOME/pardes/pardes.db`) olvasva. 2026-10-15-én (a #98 lezárása után) az indítók már leállítják az azon a porton futó régi példányt (`fuser -k -TERM <port>/tcp`), mielőtt újat indítanak — ez a változtatás a repón kívül, a felhasználó asztalán történt; az eredeti fájlok mentve a session scratch-könyvtárában.

Ami még nincs megoldva (2026-10-14/15-ei esetek):

1. **Kódváltozáskor nincs újraindulás.** Egy commit után a futó szerver a régi Python-kóddal fut, de a sablonokat és a CSS-t frissen olvassa: a 2026-10-14-i „szétesett” lap (`/arculat.css` 404, mert a régi kódban még nem volt meg az útvonal), és a BDB-blokk kétszer álló szövege (régi HTML, új CSS).
2. **Az adatbázis-másolat elavulhat.** A `~/pardes/pardes.db` kézzel másolt példány; a Windows-oldali `pardes.db` újraépítése után semmi nem jelzi, hogy a szerver régi adatot mutat.
3. **A szerver annak az ágnak a kódját futtatja, amelyiken a Windows-checkout áll** — egy session ágváltása csendben megváltoztatja az alkalmazást.
4. **Tesztek:** a projekt venv-je a WSL-ben van; a WSL a `/mnt/c` fájlrendszert nagyon lassan olvassa. A `teszt_olvaso_szerver.py` a `PARDES_DB` nélkül a `/mnt/c/…/pardes.db`-t nyitja (45+ perc a natív 2 perc helyett; a `TestD2PilotEgyezes` a `konkordancia/`-t is a `/mnt/c`-ről olvassa).

## 2. Cél

- **Egy kattintás = friss szerver**, amire nem kell gondolni: a parancsikon után mindig a checkout aktuális kódja és a legfrissebb adatbázis fut.
- **Futás közben is friss:** kódváltozáskor a szerver magától újraindul.
- **Látható állapot:** a lap láblécében ág, commit, adatbázis-építési idő; figyelmeztetés, ha a checkout nem a `main`-en áll, vagy az adatbázis-másolat régebbi a Windows-oldalinál.
- **Tesztek:** egyetlen belépési pont, amely magától a gyors (natív fájlokat olvasó) környezetet választja; a CLAUDE.md egy sora rögzíti, hogy a sessionök ezt használják.

## 3. Hatókör

- **Benne:**
  - `eszkozok/olvaso_szerver/indit.sh <kiadás> <port>`: (1) a porton futó régi példány leállítása; (2) adatbázis-szinkron: a WSL-beli és a Windows-oldali `pardes.db` `meta.epites_ts`-ének összevetése (kis olvasás, a 938 MB beolvasása nélkül), eltérésnél másolás ideiglenes névre, majd atomi átnevezés; (3) a szerver indítása újratöltővel.
  - `alkalmazas.py`: `--ujratolt` kapcsoló (Werkzeug-újratöltő **`stat` módban**: a `/mnt/c`-n az inotify nem működik); a figyelt fájlok: a szerver `.py` fájljai, a `sablonok/`, a `konfig/`, a pilot `bdb_szelet.py`-ja.
  - Lábléc (`sablonok/alap.html`): ág, rövid commit-hash, a `pardes.db` `epites_ts`-e, kiadás; figyelmeztető sor, ha az ág nem `main`, vagy a WSL-másolat régebbi.
  - A három asztali parancsikon átírása: egy-egy sor, amely az `indit.sh`-t hívja (a felhasználó asztalán, a repón kívül).
  - `eszkozok/teszt_futtat.py`: a tesztek belépési pontja; a környezetet magától választja (DT-F100a), a `PARDES_DB`-t a natív példányra állítja; a CLAUDE.md „Shell” szakaszába egy sor.
  - `teszt_indito.py`: az `indit.sh` szinkron-döntésének és a lábléc-figyelmeztetésnek a tesztje (ideiglenes adatbázisokkal).
- **Nincs benne:**
  - az éles (gunicorn) üzemeltetés és a hosting;
  - a `pardes.db` újraépítése (az a `sqlite_epit.py` dolga);
  - automatikus indítás bejelentkezéskor (DT-F100b dönt róla).

## 4. Lépések

### M0 — felmérés ⛔

1. A három parancsikon mai tartalma, a `~/pardes` állapota (git-klón, venv, `pardes.db`, hiányzó `konkordancia/`), a Windows-oldali `pardes.db` `epites_ts`-e; mérés: a `meta` tábla olvasásának ideje a `/mnt/c`-n.
2. A Werkzeug `stat`-újratöltő mérése a `/mnt/c`-n (hány fájlt figyel, mennyi CPU-t visz el üresjáratban).
3. ⛔ **DT-F100a:** a tesztkörnyezet: (a) Windows-os Python 3.12 venv (`uv`-vel; telepítés a felhasználó jóváhagyásával), a tesztek teljesen natívan; (b) a WSL venv-je, `PARDES_DB` a natív példányra, a `konkordancia/` a `~/pardes`-be szinkronizálva; (c) a WSL venv-je, `PARDES_DB` a natív példányra, a `konkordancia/`-t olvasó tesztek a `/mnt/c`-ről (lassú, de nincs másolat). **DT-F100b:** induljon-e a 8765-ös (belső) szerver magától bejelentkezéskor (Windows ütemezett feladat; tartós beállítás, a felhasználó jóváhagyásával). Megállás.

### M1 — indító, újratöltés, lábléc

1. `indit.sh`, `--ujratolt`, lábléc; `teszt_indito.py`.
2. A parancsikonok átírása az `indit.sh`-ra.
3. `teszt_futtat.py` a DT-F100a szerint; a CLAUDE.md sora; README.

### M2 — próba ⛔

1. Gépi próba: indítás → kódfájl módosítása (`touch`) → az újraindulás a naplóban; a Windows-oldali `pardes.db` `epites_ts`-ének eltérése → másolás az indításkor; ágváltás → a lábléc figyelmeztet.
2. ⛔ A felhasználó kipróbálja a három parancsikont. Megállás; zárónapló.

## 5. Elfogadási feltételek

- A parancsikon kétszeri egymás utáni kattintása után pontosan egy szerverpéldány fut az adott porton, és a lap 200-zal válaszol.
- Egy `.py` vagy sablonfájl módosítása után a futó szerver legfeljebb 5 másodpercen belül az új kóddal válaszol (a lábléc commit-hashe vagy a módosított fájl hatása mutatja).
- Ha a Windows-oldali `pardes.db` újabb, az indításkor a másolat frissül; ha azonos, nincs másolás (a napló kiírja, melyik történt). A másolás közben a régi példány ép marad (ideiglenes név + átnevezés).
- A lábléc mindhárom kiadásban mutatja az ágat, a commitot és az adatbázis építési idejét; nem `main` ágon és régi adatbázisnál figyelmeztet.
- `teszt_futtat.py`-vel a `teszt_olvaso_szerver.py` a választott környezetben 5 percen belül lefut; a teszt induláskor kiírja, melyik adatbázist nyitotta meg, és figyelmeztet, ha az a `/mnt/c` alatt van.
- A meglévő tesztek zöldek; a #98 regiszter-őre zöld (a lábléc új elemei regisztrálva vagy indokolva kizárva).

## 6. Döntésnapló

- **DT-F100a** (M0): a tesztkörnyezet — (a) Windows-os 3.12 venv `uv`-vel / (b) WSL venv + `konkordancia/` szinkron / (c) WSL venv, `konkordancia/` a `/mnt/c`-ről.
- **DT-F100b** (M0): automatikus indítás bejelentkezéskor (ütemezett feladat) — igen / nem.
