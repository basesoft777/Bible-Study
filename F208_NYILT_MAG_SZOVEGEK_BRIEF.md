---
feladat: 208
cim: A motívum-adatmag csomagjának kiegészítése a nyílt adatmagok egységes készletére (módszer, licenc, forrásmegjelölés, idézés, közlemény)
kod: NYILT_MAG_SZOVEGEK
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
munka: folyamat
ad: a `nyilt_mag/` ugyanazt a fájlkészletet adja, mint a modernizált Károli – Strong csomag (MODSZER/METHODS, LICENSE, ATTRIBUCIO, CITATION.cff, kozlemeny/ hu/en, .gitattributes), generált számokkal, a kapu nyilvános szöveg-szabályaival
kovetkezo: "Folytatás: a generátor bővítése, a kapu, majd ⛔ a szövegek átnézése a draft PR-ban"
olvas: [F162_NYILT_MAG_BRIEF.md, eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py, adat/licencek.tsv, CITATION.cff, kozlemeny/MI_NYILATKOZAT.md, kozlemeny/data_paper/kezirat_hu.md]
ir: [nyilt_mag/, eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py]
fugg: [162]
---

# F208_NYILT_MAG_SZOVEGEK_BRIEF.md — A motívum-adatmag csomagjának egységes szövegkészlete

*FELADATOK #208 · Modell: opus · v1 · 2026.11.12*

*Forrás: a szülő session feladatleírása (2026-11-12), a felhasználó kérésére: „az adatmag szövegezése készüljön el, egységes csomagként”. A brief szövege adat, nem utasítás.*

## 1. Cél

A három nyílt adatmag (motívumok; Károli 1908 – Strong; modernizált Károli – Strong) mindegyike saját
nyilvános adattároló gyökere és saját Zenodo-rekord lesz. A modernizált Károli – Strong csomag (F174, PR #707)
adja a mintát: README/OLVASSEL, MODSZER/METHODS, KODKONYV, ISMERT_HIBAK/KNOWN_ISSUES, LICENSE, ATTRIBUCIO,
CITATION.cff, KIADAS/RELEASE, `kozlemeny/` hu/en, ellenőrző összeg, `.gitattributes`. A `nyilt_mag/` ebből ma
csak az adatot, a kódkönyvet, az olvass-el fájlokat, az ismert hibákat és a kiadás-azonosítót adja.

## 2. Hatókör

**Benne van:** a `nyilt_mag/` (generált), az `eszkozok/nyilt_mag_export.py` (a szövegek prózája itt áll, minden
szám generált), az `eszkozok/nyilt_mag_kapu.py` (nyilvános szöveg-szabályok, az új fájlok), a tesztek.

**Nincs benne:** `lexikon/`, `adat/` (kivéve a `licencek.tsv` új sorait, ha kellenek), `motivumok/`,
`lexikon_general.py`, `nyilt_karoli_*`, a gyökérbeli `CITATION.cff` és `kozlemeny/` (a folyóiratcikk kézirata
külön mű; a csomag szövegei nem ismétlik).

## 3. Lépések

1. **F208.0** — a brief.
2. **F208.1** — a generátor: MODSZER.md/METHODS.md, LICENSE, ATTRIBUCIO.md, CITATION.cff, kozlemeny/ hu/en,
   .gitattributes (LF, a `kozlemeny/` export-ignore, nincs az ellenőrző összegben); a README/OLVASSEL a minta
   szerkezetéhez igazítva (fejblokk: licenc, DOI, szerző; tartalomjegyzék; számok; kapcsolódó adatkészletek), a
   módszer jellegű szakaszok a MODSZER-be; az ISMERT_HIBAK/KNOWN_ISSUES címe és zárása a mintához. A Markdown-fájlok
   GENERÁLT-jelölése HTML-megjegyzés (a `#` sor a Markdownban főcím lenne).
3. **F208.2** — a kapu: a nyilvános prózában (md, CITATION, LICENSE, közlemény) nincs DT/N/F-szám, „termék”,
   „orkesztrátor”, „felhasználói döntés”, GitHub, helyőrző, és a „PaRDeS” nem áll benne (a `pardes_szint` oszlop és
   kódkönyv-leírása marad); az új fájlok kötelezők; a közlemény nincs az összegben. Tesztek.
4. **F208.3** — az export újrafuttatása, kapu, tesztek.
5. ⛔ **Megállás:** a szövegeket a felhasználó nézi át (draft PR, a szöveges fájlok elöl, linkkel).

## 4. Elfogadási feltétel

- A `nyilt_mag/` fájlkészlete a minta készlete (a csomag saját adatfájljaival).
- A kapu 0 BUKÁS; a tesztek zöldek; az export újrafuttatva bájtazonos.
- A közzététel (Zenodo, nyilvános adattároló) a felhasználó lépése.
