---
feladat: 18
cim: Nave-import, basokant (N27)
kod: F18
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: "Nave-témák és igehely-hivatkozások a basokant/nave nyers szövegéből (5 322 entry, DT5: a theonize nincs importálva); az eredet-ellenőrzés a 4980 témán nem futott"
kovetkezo: "DT18 tételei a felhasználó döntésére várnak"
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv]
ir: [konkordancia/Nave_basokant.tsv, konkordancia/Nave_basokant_README.md, eszkozok/nave_import.py, adat/szotar_szerepek.tsv, naplok/F18_licenc.md, naplok/F18_import_naplo.md, NYITOTT_FELADATOK.md, DONTESEK.md]
fugg: [6]
ag: claude/nave-import
pr: 86
lezarva_osszegzes: "basokant/nave saját parszolóval importálva (85 116 sor, 5 322 téma, javaslat-állapot; DT5: a theonize GPLv3 miatt kimaradt); licenc- és import-napló `naplok/F18_licenc.md`, `naplok/F18_import_naplo.md`, ellenőrzés `naplok/ELLENOR_F18.md`; eredet-ellenőrzés a 4980 témán és a Gemini-lépés nem futott; nyitott tételek DT18"
---
# F18 — Nave-import (theonize), teljes eredet-ellenőrzéssel

*FELADATOK #18 · N27 · v1 · 2026.09.29*
*Modell: `sonnet`. Külső modell: Gemini 3.1 Flash Lite, csak a 3.2 lépésben.*
*Ág: `claude/nave-import` · Függ: #6 · Párhuzamosan fut: #16, #17, #19*

## Cél

A theonize Nave-adatának importja, és a Nave-eredet igazolása mind a 4980 témán.

## Lépések

1. **Licenc:** vesd össze a theonize GPLv3-at a repó licencével. ⛔ ütközés esetén. A basokant licencét is rögzítsd. Az elcafe7-et nem importáljuk.

2. **Import:** a theonize teljes importja (32 253 sor, 4980 téma, 92 609 reláció).

3. **Eredet-ellenőrzés mind a 4980 témán, a basokant ellen, két lépésben:**
   1. Szkript: normalizált témanév és az igehely-halmazok átfedése.
   2. Gemini 3.1 Flash Lite: csak a szkripttel nem illeszthető témapárok. Ítélet: igen / nem / bizonytalan, egysoros indoklással. Az FP-ben készült modellhívó eszközökkel futtasd (gyorsítótár, naplózott költség).
      - Előtte becsüld meg a költséget a maradék méretéből.
      - ⛔ ha a tényleges költség eléri a 2 USD-t.

4. **Küszöb:** ha az összesített egyezés 90% alatt van, az import `javaslat` státuszú, és kerüljön be egy tétel a `DONTESEK.md`-be.

## Munkaszabályok (a négy importfeladatban azonosak: #16–#19)

1. **Teljes feldolgozás:** teljes Biblia, teljes állomány, ne minta.
2. **Párhuzamos futás:** ez a feladat a #16–#19 másik hárommal egy időben fut, az orkesztrátor csomagjában, saját worktree-ben és saját ágon.
   - Csak a saját fájljaidat hozd létre vagy módosítsd: a saját `adat/` fájlokat, a saját naplót és a `FELADATOK.md` saját sorát.
   - Közös fájl a `adat/szotar_szerepek.tsv` és a `NYITOTT_FELADATOK.md`. Ezekben csak a saját soraidat írd.
   - A PR előtt futtass `git rebase origin/main`-t. Ütközés esetén mindkét oldal sorait tartsd meg.
   - Az importdöntések döntésnapló-sorait (D14–D19) a chat már rögzítette. Új D-sort ne írj.
3. **⛔ azonnali megállás csak ebben a két esetben:**
   - licencütközés;
   - a meglévő `adat/` vagy `konkordancia/` sorainak nem szándékolt csökkenése vagy törlése.
4. **A többi döntés a menet végére gyűlik.** Menet közben ne állj meg. Az érintett adatsor `javaslat` jelölést kap. A zárás előtt nyiss egyetlen összesített tételt a `DONTESEK.md`-ben, gépi javaslattal.
5. **A számokat a PR #75 mérési fájljaiból olvasd**, ne ebből a briefből. Eltérés esetén a fájl az irányadó, az eltérést naplózd.
6. **Minden importnál naplózd:** forrás, licenc, verzió vagy commit, sorszám. A szerepmátrixba (`adat/szotar_szerepek.tsv`) is kerüljön bejegyzés.
7. **Zárás a `/kovetkezo` 9–10. lépése szerint:** `fuggetlen-ellenor`, zárójelentés, a saját sor frissítése, draft PR. A `NYITOTT_FELADATOK.md`-ben zárd le a saját N-tételedet.
