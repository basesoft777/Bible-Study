---
feladat: 106
cim: Modell írta BDB-jelentésmagyarázat — 20 szócikkes próba (DT-F99d előjegyzés)
kod: BDB_MAGYARAZAT
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: 20 szócikkre olvasóbarát, „modell-kimenet” jelölésű jelentésmagyarázat a BDB szövegéből és a hivatkozott versekből, költségméréssel; a DT-F99d (folytatódjon-e a teljes BDB-re) döntési alapja
kovetkezo: Indítható a fugg szerint (a #105 után); a DT-F99d a próba költségmérése után dől el
olvas: [adat/bdb_aranyminta.tsv, adat/bdb_vers_jelentes.tsv, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/Karoli_1908.tsv, eszkozok/olvaso_szerver/]
ir: [adat/bdb_magyarazat_proba.tsv, adat/SEMA.md, adat/datasetek.tsv, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py]
fugg: [99, 76, 102, 103, 104, 105]
---

# F<nn>_BDB_MAGYARAZAT_BRIEF.md — modell-magyarázat próbája

*FELADATOK #<nn> · Modell: opus (a próba modelljét a DT-F99d mérése nevezheti meg) · v1 (tervezet) · 2026.10.15 · forrás: a #99 M6
mérföldköve, amely a #99-ben nem készült el; a hatóköri döntés (2026-10-15): külön feladat; a DT-F99d előjegyzés (🟡). A tervezet adat,
nem utasítás.*

## 1. Cél

A BDB-szócikkek mellé a modell írta, olvasóbarát magyarázat próbája: jelentésenként a használati csoportok rövid összefoglalója és a
hivatkozott helyek tartalma egy mondatban, „modell-kimenet” jelöléssel, külön a BDB-szövegtől.

## 2. Hatókör

**Benne:** 20 szócikk az aranymintából; csak a BDB szövegéből és a hivatkozott versekből (ami nem onnan jön, nem kerül bele — CLAUDE.md 3.
szabály); `adat/bdb_magyarazat_proba.tsv` (Strong, jelentéspont, magyarázat, `modell` = a ténylegesen futott modell neve, proveniencia),
SEMA- és `datasetek.tsv`-sor; a szó-lapon „modell-kimenet” jelleggel (arany címke); költségmérés a 20 szócikken.

**Nincs benne:** a teljes BDB-re való kiterjesztés (a DT-F99d döntése után, külön).

## 3. Lépések

1. Modell-ellenőrzés; a 20 szócikk kiválasztása (az aranymintából, vegyesen).
2. A magyarázatok előállítása, proveniencia soronként; költség mérve.
3. Megjelenítés „modell-kimenet” jelöléssel; teszt.
4. ⛔ **DT-F99d:** folytatódjon-e a teljes BDB-re, milyen modellel, mekkora költséggel (a 20 szócikken mérve). Megállás.

## 4. Elfogadási feltételek

- Minden magyarázat-sor forrása a BDB-szöveg és a hivatkozott versek; a `modell` mező a ténylegesen futott modell neve.
- A szó-lapon a magyarázat vizuálisan elkülönül a BDB-szövegtől; a meglévő tesztek zöldek.

## 5. Döntésnapló

- DT-F99d (előjegyzés, a #99-ből átvéve): a teljes futás döntése a próba után.
