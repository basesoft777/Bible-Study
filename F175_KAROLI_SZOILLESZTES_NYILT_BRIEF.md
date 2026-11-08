---
feladat: 175
cim: A Károli-szóillesztés mint második nyílt adatkészlet — 1. változat (export, kapu, data paper kézirat)
kod: KAROLI_SZOILLESZTES_NYILT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: nem_indult
ad: a Károli–héber/görög szóillesztés a #172-ben mért állapotban, CC BY 4.0 alatt közölhető nyílt adatkészletként (generált export, kétnyelvű kódkönyv, ismert hibák, saját kapu), és a hozzá tartozó második data paper kézirata (hu/en)
kovetkezo: "Te: a #171 (PR #642) és a #172 (PR #643) mergelése; utána /kovetkezo. A Zenodo-feltöltés és a DOI-kérés a felhasználóé"
olvas: [naplok/KAROLI_PONTOSSAG_jelentes.md, f172/, adat/karoli_strong/, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, F162_NYILT_MAG_BRIEF.md, CITATION.cff, DONTESEK.md]
ir: [kozlemeny/adatkozlemenyek/, eszkozok/karoli_szoillesztes_export.py, eszkozok/karoli_szoillesztes_kapu.py, eszkozok/teszt_karoli_szoillesztes.py, nyilt_karoli_szoillesztes/]
fugg: [171, 172]
---

# F175_KAROLI_SZOILLESZTES_NYILT_BRIEF.md — A Károli-szóillesztés mint második nyílt adatkészlet, 1. változat

*FELADATOK #175 · Modell: opus (a kéziratnál effort: high) · v1 · 2026.11.05*

*Befogadva a felhasználó jóváhagyásával („mehet így”, 2026-11-05), az orkesztrátor javaslata alapján. Teljes brief, nem csonk.*

## 1. Cél

A #172 megmérte a gépi Károli–héber/görög szópárosítás (`adat/karoli_strong/`, 598 715 pársor) pontosságát: fő szón a külső forrás szerint 98,72%, minden páron a vak Opus-ellenőrrel 95,06%, a morfémapárokon 90,74%. A DT-F172b szerint a párosítás ezért **nyílt adatként közölhető (CC BY 4.0)**: a nyitás indoka a mért, rétegenként és kapcsolattípusonként dokumentált pontosság, nem küszöb. A megjelenítés (olvasó) fizetős lehet; ez a feladat csak az adatkészletet adja.

Ez a **1. változat**: a #172-ben mért állapot kiadása, változatlanul. A hibák javítása a #173, amelynek eredménye a 2. változat lesz, új méréssel. A feladat a motívum-adatmag (#162) menetét követi második adatkészletre.

## 2. Hatókör

**Benne van:**
- Könyvtár-átrendezés a `kozlemeny/` alatt (3.0).
- Generált export a `nyilt_karoli_szoillesztes/` könyvtárba: könyvenkénti TSV OSIS-kulccsal (Károli-szó, héber/görög szó, Strong, bizonyosság, „javaslat” állapot, kapcsolattípus), kétnyelvű (hu/en) kódkönyv, ISMERT_HIBAK (a #172 hibái és rendszerhibái: N-F172a–c), attribúció (TAHOT/TAGNT, CC BY 4.0), KIADAS.txt, ellenőrző összeg, saját CITATION.cff.
- Saját kapu: teljesség, licenc, zárt forrás kizárása, bájtazonos újrafuttatás.
- A második data paper kézirata (hu/en) a #172 jelentéséből, csatornajavaslattal.

**Nincs benne:**
- A hibák javítása és újramérés (#173).
- A modernizált szövegre vetítés (#174).
- A Zenodo-feltöltés, a DOI-kérés, a folyóirat-beküldés (a felhasználó lépései).
- A `nyilt_mag/` (motívum-adatmag) és a gyökérbeli `CITATION.cff` módosítása: ezek a helyükön maradnak.
- A Bible-Discovery szövegének bármilyen közlése: zárt forrás, az exportba és a kéziratba nem kerül, csak a mért egyezés száma.

## 3. Lépések (⛔ a kötelező megállások)

0. **Könyvtár-átrendezés — első lépés, a #171 (PR #642) merge-e után.** `git mv kozlemeny/data_paper kozlemeny/adatkozlemenyek/motivum_adatmag`; a közös `folyoirat_kovetelmenyek.md` és `folyoirat_lehetosegek.md` a `kozlemeny/adatkozlemenyek/`-be; új mappa: `kozlemeny/adatkozlemenyek/karoli_szoillesztes/`. A projektszintű szövegek (`MI_NYILATKOZAT`, `HAYS_LEKEPEZES`, `PARDES_RECEPCIOS_KERET`, `KOZEL_KELETI_HATAR`, `en/`) a helyükön maradnak. A rá mutató hivatkozások (a `FELADATOK.md`, a `NYITOTT_FELADATOK.md`, a briefek `olvas` mezői, a kéziratok és a `szamok.py` belső útvonalai) **ugyanabban a commitban** frissülnek (CI: E27). Külön commit, mielőtt bármi más készülne.
1. **Export** (`eszkozok/karoli_szoillesztes_export.py`, generált, kézzel szerkeszteni tilos): az `adat/karoli_strong/parok_*.tsv` és `szavak_*.tsv` a `nyilt_karoli_szoillesztes/` könyvtárba, könyvenként; a `bizonyossag` és a „javaslat” állapot megmarad, a Károli-vers kulcsa OSIS. Az exportnak a `nyilt_mag_export.py` mintáját kell követnie (kódkönyv-forrás, ellenőrző összeg, KIADAS.txt). Saját `CITATION.cff` a könyvtárban.
2. **Kapu** (`eszkozok/karoli_szoillesztes_kapu.py`): (a) teljesség: minden forrássor átjön, szám- és kulcs-összevetés; (b) licenc: csak CC BY 4.0-kompatibilis forrás, a TAHOT/TAGNT-attribúció jelen van; (c) zárt forrás kizárva: a Bible-Discovery szövege és a `f172/kulso/` nyers adata nincs az exportban; (d) bájtazonos újrafuttatás (az ellenőrző összeg azonos két futásból); (e) nyilvános szövegben nincs belső jelölés és nincs a „termék” szó. Teszt: `eszkozok/teszt_karoli_szoillesztes.py`. ⛔ a kapu bukása esetén megállás.
3. **Kézirat** (`kozlemeny/adatkozlemenyek/karoli_szoillesztes/kezirat_hu.md`, `kezirat_en.md`, a számok `szamok.py`-ból a #172 jelentéséből): rétegenkénti pontosság, kalibráció, a külső összevetés, hibatípusok, korlátok, a nyitás indoka (mért, dokumentált pontosság, DT-F172b); a 2. kiadás előre rögzített minőségi célja mint tervezett javítás. Csatornajavaslat (JOHD vagy nyelvi erőforrás-hely) a `folyoirat_lehetosegek.md` alapján. A számok nem kerülhetnek kézzel a szövegbe. A próza egy kézben, egy modellel készül.
4. **Rekord-összekötés a kéziratban:** a két rekord (motívum-adatmag és szóillesztés) kölcsönösen hivatkozik egymásra, és közös Zenodo-gyűjteménybe kerül; a DOI-helyek helyőrzők. ⛔ A Zenodo-feltöltés és a DOI-kérés a felhasználó lépése.
5. A `feladatok.py ellenoriz` 0 hiba; döntés és nyitott tétel csak helyőrzővel (`dontesek/uj/`, `nyitott/uj/`).

## 4. Elfogadási feltételek

- [ ] A 3.0 átrendezés külön commitban, a hivatkozások ugyanott frissítve, a CI hivatkozás-ellenőrzés (E27) zöld.
- [ ] `nyilt_karoli_szoillesztes/` generált, kézzel nem szerkesztett; a kapu 0 BUKÁS; az újrafuttatás bájtazonos.
- [ ] Az ISMERT_HIBAK szakasz a #172 minden hibáját és rendszerhibáját (N-F172a–c) tartalmazza; a pontossági számok kapcsolattípusonként és rétegenként, konfidencia-intervallummal szerepelnek.
- [ ] Zárt forrás szövege nincs az exportban és a kéziratban; a „termék” szó nincs nyilvános szövegben.
- [ ] A kézirat hu/en, a számok generáltak, a csatornajavaslat megvan.
- [ ] A `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan.

## 5. Döntésnapló

- A felhasználó, 2026-11-05: „mehet így” — az 1. változat a #172-ben mért állapot kiadása; a javítás a #173 2. változata (orkesztrátor-javaslat alapján).
- DT-F172b (a #172-ből): a párosítás nyílt adat, CC BY 4.0; a megjelenítés fizetős lehet.

*Megjegyzés a fejléchez: az `ir` szándékosan nem sorolja fel a `kozlemeny/data_paper/` forrásútvonalat és a `nyilt_mag_export.py`-t (az átrendezés forrása, illetve a követendő minta), hogy a #171-gyel ne alkosson függési kört; a #171 mergelése a `fugg`-ben előfeltétel.*
