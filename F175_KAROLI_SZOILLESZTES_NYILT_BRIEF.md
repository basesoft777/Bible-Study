---
feladat: 175
cim: A Károli–Strong szóillesztés mint második nyílt mag — 1. változat (nyilt_karoli_strong/, repó-átrendezés, kézirat)
kod: KAROLI_SZOILLESZTES_NYILT
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: lezarva
pr: 712
lezarva_osszegzes: "PR #712 (F175.1–7): nyilt_karoli_strong/ (598 715 pár, 1 210 763 szó, 31 158 vers, meres.tsv; kapu 0 BUKÁS, bájtazonos), MODSZER/METHODS, ISMERT_HIBAK, rövid közlemény hu/en; a második data paper kézirata a kozlemeny/data_paper/ alatt (DT809); a szövegek szerkesztői átnézéssel (11.12), névelő-szabály kapuval; N-F175a–c nyitva"
ad: a Károli–héber/görög szóillesztés a #172-ben mért állapotban, CC BY 4.0 alatt közölhető nyílt magként (nyilt_karoli_strong/: generált export, kétnyelvű kódkönyv, ismert hibák, MODSZER.md, saját kapu, saját kozlemeny/ mappa), és a hozzá tartozó második data paper kézirata (hu/en) a gyökérbeli kozlemeny/data_paper/ alatt
kovetkezo: "lezárva; a merge az orkesztrátoré, a Zenodo-feltöltés (DOI 10.5281/zenodo.24141884) a felhasználóé; nyitva: N-F175a (CI), N-F175b (névelő-szabály a modernizált csomagban), N-F175c (a motívum-csomag címe a #710 után)"
olvas: [naplok/KAROLI_PONTOSSAG_jelentes.md, f172/, adat/karoli_strong/, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, F162_NYILT_MAG_BRIEF.md, F174_KAROLI_MODERN_STRONG_BRIEF.md, CITATION.cff, DONTESEK.md, kozlemeny/data_paper/folyoirat_lehetosegek.md]
ir: [nyilt_karoli_strong/, kozlemeny/data_paper/karoli_strong_kezirat_hu.md, kozlemeny/data_paper/karoli_strong_kezirat_en.md, eszkozok/karoli_strong_export.py, eszkozok/karoli_strong_szovegek.py, eszkozok/karoli_strong_kapu.py, eszkozok/teszt_karoli_strong_export.py]
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
- A közlemény helye (3. lépés, DT809 szerint szűkítve).

**Nincs benne:**
- A hibák javítása és újramérés (#173); a modernizált réteg (#174).
- A Zenodo-feltöltés, a DOI-kérés, a folyóirat-beküldés (a felhasználó lépései).
- A `nyilt_mag/` bármely fájlja és a gyökérbeli `CITATION.cff` (DT809: a `kozlemeny/data_paper/` nem költözik a `nyilt_mag/kozlemeny/`-be).
- Harmadik fél adata: a Bible-Discovery szövege és a `f172/kulso/` nyers adata, a TAHOT/TAGNT nyers szövege semmiképp. Csak a mért egyezés száma szerepel.
- Export-kód a nyilvános mappába: csak a `MODSZER.md` kerül.

## 3. Lépések (⛔ a kötelező megállások)

1. **Export** (`eszkozok/karoli_strong_export.py`, generált, kézzel szerkeszteni tilos): az `adat/karoli_strong/parok_*.tsv` és `szavak_*.tsv` a `nyilt_karoli_strong/` könyvtárba, könyvenként; a `bizonyossag` és a „javaslat” állapot megmarad, a vers kulcsa OSIS. Mintája a `nyilt_mag_export.py`. `MODSZER.md` (hu/en): a #22 párosításának tényleges menete (modellek, kapu, javaslat-állapot, a #172 mérése), a #174 `MODSZER.md` mintájára. **Kapu** (`eszkozok/karoli_strong_kapu.py`, teszt: `teszt_karoli_strong_export.py`): (a) teljesség: minden forrássor átjön, szám- és kulcs-összevetés; (b) licenc: CC BY 4.0-kompatibilis, TAHOT/TAGNT-attribúció jelen van; (c) harmadik fél adata és export-kód nincs a mappában; (d) bájtazonos újrafuttatás; (e) nyilvános szövegben nincs belső jelölés, „orkesztrátor”, „felhasználói döntés”, „termék”; a „PaRDeS” nem központi keretezés. ⛔ a kapu bukása esetén megállás.
2. **Kézirat** (DT809 óta: `kozlemeny/data_paper/karoli_strong_kezirat_hu.md`, `_en.md`, a repó gyökerében, a csomagon kívül; a csomag `kozlemeny/` mappájában a #174-mintájú rövid közlemény áll; a számok generáltak, a #172 jelentéséből): rétegenkénti pontosság, kalibráció, a külső összevetés, hibatípusok, korlátok, a nyitás indoka (mért, dokumentált pontosság, DT-F172b), a 2. kiadás előre rögzített minőségi célja mint tervezett javítás; a Strong-párosítás és (hivatkozással a #174 közleményére) a modernizálás menete. Csatornajavaslat (JOHD vagy nyelvi erőforrás-hely) a `kozlemeny/data_paper/folyoirat_lehetosegek.md` alapján. „Szerkesztői döntés”, nem „felhasználói”; az „orkesztrátor” szó nem szerepel. A próza egy kézben, egy modellel. A `kozlemeny/` almappát a release a megjelenésig kihagyja.
3. **A közlemény helye** (DT809, 2026-11-12, szűkítve): a `nyilt_karoli_strong/` saját `kozlemeny/` mappája (hu/en) a csomagon belül, export-ignore; a második data paper kézirata a gyökérbeli `kozlemeny/data_paper/` alatt, külön fájlként, a generátor írja; a `kozlemeny/data_paper/` a helyén marad, a `nyilt_mag/`-hoz a feladat nem nyúl. *Az eredeti, elvetett változat (archív):* ~~Repó-átrendezés (külön commit, a #174 után): `git mv kozlemeny/data_paper nyilt_mag/kozlemeny`; a keretdokumentumok (`kozlemeny/PARDES_RECEPCIOS_KERET.md`, `HAYS_LEKEPEZES.md`, `KOZEL_KELETI_HATAR.md`, `MI_NYILATKOZAT.md`, `kozlemeny/en/`) a `kozlemeny/`-ben maradnak, mert a lapok linkelnek rájuk. **A rá mutató hivatkozások ugyanabban a commitban frissülnek** (E27): `FELADATOK.md`, `NYITOTT_FELADATOK.md`, a briefek `olvas`/`ir` mezői (F170, F171 stb.), a kéziratok és a `szamok.py` belső útvonalai, `naplok/NYILT_MAG_ANGOL_jelentes.md`. A `nyilt_mag` release-kapuja a `nyilt_mag/kozlemeny/` almappát a megjelenésig kihagyja (útvonal-frissítés; a #162 kapujának módosítása csak ennyi). Végén `feladatok.py ellenoriz` és `ellenorzes/futtat.py` a változott fájlokkal 0 hiba.~~
4. ⛔ A szövegek és a kézirat átnézése a felhasználóval. A Zenodo-feltöltés a felhasználó lépése; a rekordok kölcsönösen hivatkoznak egymásra, közös gyűjteménybe kerülnek.
5. Döntés és nyitott tétel csak helyőrzővel (`dontesek/uj/`, `nyitott/uj/`).

## 4. Elfogadási feltételek

- [ ] `nyilt_karoli_strong/` generált, kézzel nem szerkesztett; a kapu 0 BUKÁS; az újrafuttatás bájtazonos; nincs benne harmadik fél adata és export-kód.
- [ ] Az `ISMERT_HIBAK` a #172 minden hibáját és rendszerhibáját (N-F172a–c) tartalmazza; a pontosság kapcsolattípusonként és rétegenként, konfidencia-intervallummal szerepel.
- [ ] A `MODSZER.md` és a kézirat (hu/en) kész, a számok generáltak, a nyilvános szövegszabályok teljesülnek.
- [ ] A kézirat a `kozlemeny/data_paper/` alatt, a csomagon kívül (DT809); a csomag `kozlemeny/` mappája a rövid közleményt tartalmazza.
- [ ] A `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan.

## 5. Döntésnapló

- 2026-11-05 (felhasználó): „mehet így” — az 1. változat a #172-ben mért állapot kiadása; a javítás a #173 2. változata.
- 2026-11-08 (felhasználó): a magok saját gyökérszintű mappát kapnak (a mappa 1:1-ben a nyilvános repó gyökere, magonként külön repó); a közlemény a mag mappája alá kerül; harmadik fél adata nem megy be; elég egy `MODSZER.md`; a mappanév `nyilt_karoli_strong/` (a korábbi `nyilt_karoli_szoillesztes/` helyett).
- DT-F172b (a #172-ből): a párosítás nyílt adat, CC BY 4.0; a megjelenítés fizetős lehet.
- 2026-11-12 (végrehajtás): DT808 — a csomag héber/görög szóalak nélkül, a #174 fájlkészletével (`parok/`, `szavak/`, `versek.tsv`, `meres.tsv`); 🟡, átnézés a 4. lépésben.
- 2026-11-12 (felhasználó, a szövegek átnézése, az orkesztrátoron át): öt jóváhagyott javítás — névelő a számok előtt a kiejtés szerint (generátor + kapu), ISMERT_HIBAK 1. „négy helyen”, MODSZER 6. „nem is ekként közöljük”, OLVASSEL/README „A csomag minden fájlja a kiadás része.”, a közlemény első mondata; a többi szöveg rendben.
- 2026-11-12 (orkesztrátori döntés, a generált csomagmappa védelme): DT809 — a `kozlemeny/data_paper/` nem költözik a `nyilt_mag/kozlemeny/`-be (az a #710 óta a csomag generált rövid közleménye); a 3. lépés a csomag saját `kozlemeny/` mappájára és a brief mezőire szűkül; a második data paper kézirata a gyökérbeli `kozlemeny/data_paper/` alá kerül.
