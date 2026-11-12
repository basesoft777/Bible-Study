---
feladat: 174
cim: A modernizált Károli Strong-vetítése — harmadik nyílt mag (nyilt_karoli_modern/), módszertani leírással
kod: KAROLI_MODERN_STRONG
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: lezarva
pr: 707
lezarva_osszegzes: "PR #707 (F174.1–9): nyilt_karoli_modern/ (598 715 pár, 488 659 Strongos token, kapu 0 BUKÁS, bájtazonos), MODSZER/METHODS, közlemény hu/en; a szövegek szerkesztői jóváhagyással (2026-11-12); a 3 E/1 → T/3 hiba a forrásnál javítva (F174.8); jelentés: naplok/F174_jelentes.md"
ad: a modernizált Károli (#96) és a hozzá vetített Strong-párok CC BY 4.0 alatt közölhető nyílt magja (nyilt_karoli_modern/), MODSZER.md-vel, saját kapuval, és a modernizálás módszerének közlemény-szövege (hu/en)
kovetkezo: "lezárva; a Zenodo-feltöltés (DOI 10.5281/zenodo.24141950) a felhasználó lépése; előtte a `licencek.tsv` N-F174a sora"
olvas: [adat/karoli_modern/, adat/karoli_strong/, naplok/KAROLI_MODERN_zaras.md, naplok/KAROLI_MODERN_meres.md, naplok/ELLENOR_F96.md, naplok/ELLENOR_F96_2.md, naplok/ELLENOR_F96_3.md, naplok/KAROLI_PONTOSSAG_jelentes.md, eszkozok/karoli_modern/, adat/SEMA.md, adat/licencek.tsv, F96_KAROLI_MODERN_BRIEF.md, F137_KAROLI_MODERN_DB_BRIEF.md, F162_NYILT_MAG_BRIEF.md, DONTESEK.md, NYITOTT_FELADATOK.md]
ir: [nyilt_karoli_modern/, eszkozok/karoli_modern_export.py, eszkozok/karoli_modern_kapu.py, eszkozok/teszt_karoli_modern_export.py, eszkozok/karoli_modern/igealak.py, eszkozok/karoli_modern/karoli_modern.py, adat/karoli_modern/]
fugg: [96, 172]
---

# F174_KAROLI_MODERN_STRONG_BRIEF.md — A modernizált Károli Strong-vetítése, harmadik nyílt mag

*FELADATOK #174 · Modell: opus (a szövegnél effort: high) · v2 (a csonk teljes briefre váltva) · 2026.11.08*

*Felhasználói jóváhagyás (2026-11-05): „a modernizált károli strongozását vegyük fel jövőbeni feladatnak”; (2026-11-08): „igen mehet / a közleményeknél szépen fogalmazzuk le, hogyan történt a strongozás vagy a modernizálás … a modernizált Károli a projekt munkája”.*

## 1. Cél

A #96 a Károli 1908 szövegét modernizálta (helyesírás és igealak; 599 367 token, 31 158 vers). A #22 a Károli-szavakat a héber/görög szavakhoz és Strong-számokhoz párosította (javaslat-állapot). A feladat a kettő **kulcs szerinti összekapcsolása**, és az eredmény kiadása önálló, harmadik nyílt magként (`nyilt_karoli_modern/`, CC BY 4.0). A modernizált szöveg a projekt saját munkája; a Strong-párok a #172-ben mért pontosságú gépi párosítás; a TAHOT/TAGNT-attribúció kötelező.

Az összekapcsolás nem származtat új Strong-állítást: a vetítés determinisztikus, modell nélküli kulcs-illesztés (DT305: a modern réteg nem tárol Strongot, a join éri el; ez az export származtatott nézet).

## 2. Hatókör

**Benne van:**
- A vetítés: az `adat/karoli_strong/parok_*.tsv` és az `adat/karoli_modern/karoli_modern.tsv` az (igehely, sorszám) kulcson. A kieső tokenek (`kieso`, `kieso_gazda`) a gazdaszóhoz kötődnek (DT314), jelölve, nem vesznek el; összevonásnál mindkét régi pár Strongja megmarad.
- Az export: `nyilt_karoli_modern/` — a mappa tartalma 1:1-ben a nyilvános adatrepó gyökere: könyvenkénti TSV (OSIS-kulcs, 1908-as alak, modern alak, Strong, bizonyosság, kapcsolattípus, „javaslat” állapot, kieső-jelölés), kétnyelvű kódkönyv, `ISMERT_HIBAK` (köztük az N-F96h), `MODSZER.md`, attribúció, `KIADAS.txt`, ellenőrző összeg, saját `CITATION.cff`, `OLVASSEL`/`README`.
- Saját kapu.
- `MODSZER.md` (3. lépés) és a modernizálás közlemény-szövege (3. lépés).

**Nincs benne:**
- Az N-F96h javítása: dokumentálva megy ki (felhasználói jóváhagyás, 2026-11-08), nem javítva.
- A betöltés a `pardes.db`-be és a keresés (#137); a brief rögzíti: a #174 a #137 előfeltétele a Strong-kötéshez (DT314), a #137 nem része ennek.
- Az export-kód a nyilvános mappába: csak a `MODSZER.md` kerül.
- Harmadik fél adata: a Bible-Discovery, a `f172/kulso/`, a TAHOT/TAGNT nyers szövege nem kerül az exportba.
- A hibák javítása a párosításban (#173).

## 3. Lépések (⛔ a kötelező megállások)

1. **Vetítés és export** (`eszkozok/karoli_modern_export.py`, generált, kézzel szerkeszteni tilos). Mintája a `nyilt_mag_export.py` (kódkönyv-forrás, ellenőrző összeg, KIADAS.txt). Kimenet a `nyilt_karoli_modern/` könyvtárba.
2. **Kapu** (`eszkozok/karoli_modern_kapu.py`, teszt: `teszt_karoli_modern_export.py`):
   - (a) **teljesség:** minden régi pár átvetítve, egy sem vész el, új nem keletkezik; mind a 418 633 Strongos token kulcsa megvan (`naplok/KAROLI_MODERN_zaras.md`);
   - (b) licenc: csak CC BY 4.0-kompatibilis; a TAHOT/TAGNT-attribúció jelen van;
   - (c) harmadik fél adata és export-kód nincs a mappában;
   - (d) bájtazonos újrafuttatás;
   - (e) nyilvános szövegben nincs belső jelölés, „orkesztrátor”, „felhasználói döntés”, „termék”; a „PaRDeS” nem központi keretezés.
   ⛔ a kapu bukása esetén megállás.
3. **Szövegek** (a próza egy kézben, egy modellel, effort: high; a számok generáltak, kézzel nem kerülnek a szövegbe):
   - **`MODSZER.md`** (hu/en) — a #96 **tényleges** eljárását írja le, nem a brief tervét (forrás: `naplok/KAROLI_MODERN_zaras.md`, `_meres.md`, `ELLENOR_F96*.md`): szabályok és a #94 szótár-tábla (a Hunspell csak mérce, DT301); öt LLM-kör (Sonnet kb. 1,4 M, Opus kb. 1,5 M token, Claude Code előfizetésből); kézi kivételek; a menet közbeni határdöntések (DT304, DT306, DT308–DT310, DT315, DT320); tokenösszevonás és -kiesés; négy ellenőri kör és két javítókör. Mért eredmény: a cserék 0 hibásak a mintákon; az igealak-lefedettség 94,8% (92 csere, 5 kihagyás); az N-F96h ismert hibaként.
   - **Közlemény-szöveg** (`nyilt_karoli_modern/kozlemeny/`, hu/en): „szépen megfogalmazva”, magas szinten, hogyan történt a modernizálás és a Strong-vetítés. Szerepel benne a „szerkesztői döntés” (nem „felhasználói”); az „orkesztrátor” szó és a belső jelölések nem; a „PaRDeS” nem központi keretezés. A `kozlemeny/` almappát a release a megjelenésig kihagyja (a kapu ellenőrzi).
4. ⛔ A szövegek átnézése a felhasználóval; a Zenodo-feltöltés és a DOI-kérés a felhasználó lépése; a rekordok kölcsönösen hivatkoznak egymásra, közös gyűjtemény.
5. A `feladatok.py ellenoriz` 0 hiba; döntés és nyitott tétel csak helyőrzővel.

## 4. Elfogadási feltételek

- [ ] A kapu 0 BUKÁS; az újrafuttatás bájtazonos; a teljességi ellenőrzés a 418 633 Strongos tokenre teljesül.
- [ ] `nyilt_karoli_modern/` generált, kézzel nem szerkesztett; a mappa a nyilvános repó gyökere (nincs benne export-kód, nincs harmadik fél adata).
- [ ] A `MODSZER.md` a tényleges eljárást írja le a fenti pontokkal, a számok forrásfájlra vezethetők vissza.
- [ ] Az N-F96h az `ISMERT_HIBAK`-ban dokumentált; a #137 viszonya (előfeltétel) rögzítve.
- [ ] A közlemény-szöveg hu/en, nyilvános szövegszabályokkal (2. lépés (e)).
- [ ] A `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan.

## 5. Döntésnapló

- 2026-11-08 (felhasználó): az N-F96h dokumentálva megy ki, nem javítva; a modernizált Károli a projekt munkája; a nyílt magok saját gyökérszintű mappát kapnak, harmadik fél adata nem megy be, elég egy `MODSZER.md`.
- DT305/DT314 (a #96-ból): a Strong a #22 párosításból jön, a modern réteg nem tárolja; a kieső token a gazdaszón át érhető el.
- 2026-11-12 (végrehajtás, `claude-opus-5-5`): a vetítés és a kapu lefutott (0 BUKÁS, UJRA bájtazonos). A teljességi pont a mai 66 könyvön mér: 598 715 pár, 488 659 Strongos token; a brief 418 633-as száma a #96 zárásakori 61 könyvé (a Mt, Mk, Luk, Ján, ApCsel párosítása később készült), és a kapu ezt a 61 könyvön külön is igazolja (418 633 / 418 633). A modern réteg az 5 új könyvön is illeszkedik (0 alakeltérés). Formátum: páronként egy sor, a pár nélküli token egy sorban; `kapcsolat` = `morfema` a H9001–H9049 Strongon, egyébként `szo`. A `kozlemeny/` generált, az ellenőrző összegen kívül, `.gitattributes` export-ignore-ral. A #137 viszonya: a #137 a kieső token Strongját a csomag `gazda_token` oszlopa szerint köti (DT314); a #174 a Strong-kötés előfeltétele. Nyitott: N-F174a (licencek.tsv), N-F174b (CI).
- 2026-11-12 (szerkesztői döntés, az orkesztrátoron át): a három E/1 → T/3 személyhiba ebben a kiadásban javítva, az `igealak.py` `TOKEN_KIVETEL` táblájában (1Móz 39:15 kezdtem, Dán 7:16 kértem, Ez 22:30 kerestem); az `ir` ezért bővült az `eszkozok/karoli_modern/igealak.py`-val és az `adat/karoli_modern/`-val. Az N-F96h ezen része így lezárult; a `NYITOTT_FELADATOK.md` N-F96h-szövegének frissítése nem ennek az ágnak a fájlja.
