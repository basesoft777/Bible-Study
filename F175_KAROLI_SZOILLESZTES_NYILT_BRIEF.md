---
feladat: 175
cim: A Károli–Strong szóillesztés mint második nyílt mag — 1. változat (nyilt_karoli_strong/, repó-átrendezés, kézirat)
kod: KAROLI_SZOILLESZTES_NYILT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: fut
ad: a Károli–héber/görög szóillesztés a #172-ben mért állapotban, CC BY 4.0 alatt közölhető nyílt magként (nyilt_karoli_strong/: generált export, kétnyelvű kódkönyv, ismert hibák, MODSZER.md, saját kapu), a közlemények magonkénti mappába rendezése, és a hozzá tartozó második data paper kézirata (hu/en)
kovetkezo: "fut: (1) export, kapu, MODSZER, közlemény (claude/peaceful-leavitt-ccb923); a (3) repó-átrendezés a #710 (F208) merge-e után, ⛔ döntéssel; a Zenodo-feltöltés a felhasználóé"
olvas: [naplok/KAROLI_PONTOSSAG_jelentes.md, f172/, adat/karoli_strong/, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, F162_NYILT_MAG_BRIEF.md, F174_KAROLI_MODERN_STRONG_BRIEF.md, CITATION.cff, DONTESEK.md]
ir: [nyilt_karoli_strong/, nyilt_mag/kozlemeny/, eszkozok/karoli_strong_export.py, eszkozok/karoli_strong_szovegek.py, eszkozok/karoli_strong_kapu.py, eszkozok/teszt_karoli_strong_export.py]
fugg: [171, 172, 174]
---

# F175_KAROLI_SZOILLESZTES_NYILT_BRIEF.md — A Károli–Strong szóillesztés mint második nyílt mag, 1. változat

*FELADATOK #175 · Modell: opus (a kéziratnál effort: high) · v2 (átírva az új repó-szerkezetre) · 2026.11.08*

*Felhasználói jóváhagyás: „mehet így” (2026-11-05); az új szerkezetre: „igen mehet … az itteni repó szerkezete is igazodjon. Az elkészült közlemény mappa a nyílt mag mappa alá kerülne” (2026-11-08).*

## 1. Cél

A #172 megmérte a gépi Károli–héber/görög szópárosítás (`adat/karoli_strong/`, 598 715 pársor) pontosságát: fő szón a külső forrás szerint 98,72%, minden páron a vak Opus-ellenőrrel 95,06%, a morfémapárokon 90,74%. A DT-F172b szerint a párosítás ezért **nyílt adatként közölhető (CC BY 4.0)**: a nyitás indoka a mért, rétegenként és kapcsolattípusonként dokumentált pontosság, nem küszöb. A megjelenítés (olvasó) fizetős lehet; ez a feladat csak az adatot adja.

**1. változat:** a #172-ben mért állapot, változatlanul. A hibák javítása a #173, amelynek eredménye a 2. változat lesz, új méréssel.

**Repó-szerkezet (új elv, 2026-11-08):** minden nyílt mag saját gyökérszintű mappát kap, amelynek tartalma 1:1-ben a nyilvános adatrepó gyökere; mindegyik magnak külön repója lesz, csak a saját, itt generált fájlokkal. A magok: `nyilt_mag/` (motívum-adatmag, #162), `nyilt_karoli_strong/` (ez a feladat), `nyilt_karoli_modern/` (#174). A közlemény a mag mappája alá kerül (`<mag>/kozlemeny/`).

## 2. Hatókör

**Benne van:**
- Generált export a `nyilt_karoli_strong/` könyvtárba: könyvenkénti TSV OSIS-kulccsal (Károli-szó, héber/görög szó, Strong, bizonyosság, kapcsolattípus, „javaslat” állapot), kétnyelvű kódkönyv, `ISMERT_HIBAK` (a #172 hibái és rendszerhibái: N-F172a–c), attribúció (TAHOT/TAGNT, CC BY 4.0), `MODSZER.md`, `KIADAS.txt`, ellenőrző összeg, saját `CITATION.cff`.
- Saját kapu.
- A második data paper kézirata (hu/en), benne a Strong-párosítás menetének „szépen megfogalmazott”, magas szintű leírása.
- A repó-átrendezés (3. lépés).

**Nincs benne:**
- A hibák javítása és újramérés (#173); a modernizált réteg (#174).
- A Zenodo-feltöltés, a DOI-kérés, a folyóirat-beküldés (a felhasználó lépései).
- A `nyilt_mag/` adatfájljainak és a gyökérbeli `CITATION.cff`-nek a módosítása (a `nyilt_mag/kozlemeny/` a közlemény költözése).
- Harmadik fél adata: a Bible-Discovery szövege és a `f172/kulso/` nyers adata, a TAHOT/TAGNT nyers szövege semmiképp. Csak a mért egyezés száma szerepel.
- Export-kód a nyilvános mappába: csak a `MODSZER.md` kerül.

## 3. Lépések (⛔ a kötelező megállások)

1. **Export** (`eszkozok/karoli_strong_export.py`, generált, kézzel szerkeszteni tilos): az `adat/karoli_strong/parok_*.tsv` és `szavak_*.tsv` a `nyilt_karoli_strong/` könyvtárba, könyvenként; a `bizonyossag` és a „javaslat” állapot megmarad, a vers kulcsa OSIS. Mintája a `nyilt_mag_export.py`. `MODSZER.md` (hu/en): a #22 párosításának tényleges menete (modellek, kapu, javaslat-állapot, a #172 mérése), a #174 `MODSZER.md` mintájára. **Kapu** (`eszkozok/karoli_strong_kapu.py`, teszt: `teszt_karoli_strong_export.py`): (a) teljesség: minden forrássor átjön, szám- és kulcs-összevetés; (b) licenc: CC BY 4.0-kompatibilis, TAHOT/TAGNT-attribúció jelen van; (c) harmadik fél adata és export-kód nincs a mappában; (d) bájtazonos újrafuttatás; (e) nyilvános szövegben nincs belső jelölés, „orkesztrátor”, „felhasználói döntés”, „termék”; a „PaRDeS” nem központi keretezés. ⛔ a kapu bukása esetén megállás.
2. **Kézirat** (`nyilt_karoli_strong/kozlemeny/kezirat_hu.md`, `kezirat_en.md`, a számok generáltak, a #172 jelentéséből): rétegenkénti pontosság, kalibráció, a külső összevetés, hibatípusok, korlátok, a nyitás indoka (mért, dokumentált pontosság, DT-F172b), a 2. kiadás előre rögzített minőségi célja mint tervezett javítás; a Strong-párosítás és (hivatkozással a #174 közleményére) a modernizálás menete. Csatornajavaslat (JOHD vagy nyelvi erőforrás-hely) a `nyilt_mag/kozlemeny/folyoirat_lehetosegek.md` alapján. „Szerkesztői döntés”, nem „felhasználói”; az „orkesztrátor” szó nem szerepel. A próza egy kézben, egy modellel. A `kozlemeny/` almappát a release a megjelenésig kihagyja.
3. **Repó-átrendezés** (külön commit, a #174 után): `git mv kozlemeny/data_paper nyilt_mag/kozlemeny`; a keretdokumentumok (`kozlemeny/PARDES_RECEPCIOS_KERET.md`, `HAYS_LEKEPEZES.md`, `KOZEL_KELETI_HATAR.md`, `MI_NYILATKOZAT.md`, `kozlemeny/en/`) a `kozlemeny/`-ben maradnak, mert a lapok linkelnek rájuk. **A rá mutató hivatkozások ugyanabban a commitban frissülnek** (E27): `FELADATOK.md`, `NYITOTT_FELADATOK.md`, a briefek `olvas`/`ir` mezői (F170, F171 stb.), a kéziratok és a `szamok.py` belső útvonalai, `naplok/NYILT_MAG_ANGOL_jelentes.md`. A `nyilt_mag` release-kapuja a `nyilt_mag/kozlemeny/` almappát a megjelenésig kihagyja (útvonal-frissítés; a #162 kapujának módosítása csak ennyi). Végén `feladatok.py ellenoriz` és `ellenorzes/futtat.py` a változott fájlokkal 0 hiba.
4. ⛔ A kézirat és az átrendezés átnézése a felhasználóval. A Zenodo-feltöltés a felhasználó lépése; a rekordok kölcsönösen hivatkoznak egymásra, közös gyűjteménybe kerülnek.
5. Döntés és nyitott tétel csak helyőrzővel (`dontesek/uj/`, `nyitott/uj/`).

## 4. Elfogadási feltételek

- [ ] `nyilt_karoli_strong/` generált, kézzel nem szerkesztett; a kapu 0 BUKÁS; az újrafuttatás bájtazonos; nincs benne harmadik fél adata és export-kód.
- [ ] Az `ISMERT_HIBAK` a #172 minden hibáját és rendszerhibáját (N-F172a–c) tartalmazza; a pontosság kapcsolattípusonként és rétegenként, konfidencia-intervallummal szerepel.
- [ ] A `MODSZER.md` és a kézirat (hu/en) kész, a számok generáltak, a nyilvános szövegszabályok teljesülnek.
- [ ] Az átrendezés külön commitban, a hivatkozások ugyanott frissítve, az E27 zöld.
- [ ] A `nyilt_mag/` adatfájljai és a gyökérbeli `CITATION.cff` változatlan.

## 5. Döntésnapló

- 2026-11-05 (felhasználó): „mehet így” — az 1. változat a #172-ben mért állapot kiadása; a javítás a #173 2. változata.
- 2026-11-08 (felhasználó): a magok saját gyökérszintű mappát kapnak (a mappa 1:1-ben a nyilvános repó gyökere, magonként külön repó); a közlemény a mag mappája alá kerül; harmadik fél adata nem megy be; elég egy `MODSZER.md`; a mappanév `nyilt_karoli_strong/` (a korábbi `nyilt_karoli_szoillesztes/` helyett).
- DT-F172b (a #172-ből): a párosítás nyílt adat, CC BY 4.0; a megjelenítés fizetős lehet.
