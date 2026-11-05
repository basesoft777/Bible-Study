---
feladat: 170
cim: A nyílt mag angol rétege — OSIS-kulcs, angol címkék és párhuzamos mezők, angol motívum-meghatározás
kod: NYILT_MAG_ANGOL
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ad: a nyílt adatmag minden sora OSIS-igehelykulccsal, a zárt értékkészletek angol címkével, a szabad szöveges indoklás és funkció-címke jelölt gépi angol párhuzamos mezővel, a motívumok angol meghatározásával; kódkönyv (hu/en) és kapu bővítve, E35 zöld — a data paper beküldésének előfeltétele
kovetkezo: F170.1–F170.5 kész (jelentés: naplok/NYILT_MAG_ANGOL_jelentes.md); független ellenőr, draft PR, merge a felhasználóé
munka: folyamat
olvas: [konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/TBESH.txt, konkordancia/TBESG.txt, konkordancia/TBESH_TBESG_README.md, adat/motivumok.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/elutasitasi_okok.tsv, adat/licencek.tsv, adat/datasetek.tsv, adat/SEMA.md]
ir: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py, eszkozok/nyilt_mag_angol.py, adat/nyilt_kodkonyv.tsv, adat/nyilt_angol.tsv, adat/SEMA.md, nyilt_mag/, kozlemeny/MI_NYILATKOZAT.md, kozlemeny/en/]
fugg: []
nem_fugg: [38, 123, 163]
---

# F170_NYILT_MAG_ANGOL_BRIEF.md — A nyílt mag angol rétege

*FELADATOK #170 · Modell: opus (a fordítási lépés: sonnet) · v1 · 2026.11.05*

*Befogadva a felhasználó jóváhagyásával („Igen, vedd fel”, 2026-11-05). Előzmény: #162 NYILT_MAG (az export, a kódkönyv és a kapu), F169.2 (az angol olvasói fájlok: `README.md`, `KNOWN_ISSUES.md`, `RELEASE.txt`), F169.3 (E35), #163 (MI-nyilatkozat), a #86 terv 1.6b szakasza (angol réteg).*

## 1. Cél

A nyílt adatmag (`nyilt_mag/`, CC BY 4.0) ma magyar oszlopértékekkel és magyar szabad szöveggel áll; az angol olvasó csak a kódkönyvön és az angol olvasói fájlokon át éri el. A data paper (`kozlemeny/data_paper/kezirat_en.md`) nemzetközi folyóiratnak megy, ezért az adatkészletnek **soronként** használhatónak kell lennie angolul, és a versek szabványos igehelykulccsal kell hogy összekapcsolhatók legyenek más korpuszokkal. A feladat ezt az angol réteget **generátor-szinten** építi be: a `nyilt_mag/` generált kimenet, kézzel nem szerkeszthető.

## 2. Hatókör

**Benne van:**

1. **OSIS-igehelykulcs** minden igehelyet hordozó sorhoz (új oszlop, pl. `igehely_osis`: `1Kgs.13.31`), a `konkordancia/Konyv_normalizalo_tabla.tsv` leképezésével. A magyar `igehely` oszlop marad. Leképezhetetlen könyvnév → a generátor megáll (nem üres érték, nem találgatás).
2. **Angol címke a zárt értékkészletekre** — legalább: kizárás oka, funkciótípus (`pardes_szint`, `horgony_tipus` és ami a kódkönyvben zárt), azonosítás módja, megbízhatóság. Helye: párhuzamos `_en` oszlop az exportban **vagy** a kódkönyv-hivatkozás; a választás a 3. lépés ⛔-je. A címke-szótár a `adat/nyilt_kodkonyv.tsv` `leiras_en` mezőjére épül (egy forrás, nem kettő).
3. **Angol párhuzamos mező a szabad szövegre**: a kizárási/felvételi indoklás és a funkció-címke (`funkcio`). **Gépi fordítás Sonnettel**, soronként jelölve (pl. `*_en` + `forditas_modja` = `gépi (claude-sonnet-…)` a ténylegesen futott modellnévvel, CLAUDE.md „Modell-ellenőrzés”), a fordítás tárolva egy forrásrétegbeli táblában (javaslat: `adat/nyilt_angol.tsv`, kulcs + magyar forrásszöveg-hash + angol szöveg + modell + dátum), hogy az export determinisztikus legyen és a forrás változása kimutatható (hash-eltérés → újrafordítandó, a kapu bukik).
4. **A motívumok angol meghatározása**: cím, negatív kritérium, fölérendelt fogalom (`nyilt_mag/motivumok.tsv` `_en` mezők). Ugyanaz a fordítási út és jelölés, mint a 3. pontban.
5. **Angol szófogódzó**: ahol az exportnak angol szójelentés kell, a forrás a STEPBible-glossza (`TBESH`/`TBESG`, CC BY 4.0, attribúcióval). Ha a meglévő `jelentes_en` oszlop más forrásból jön, a 1. lépés ezt megméri és jelenti.
6. **Kódkönyv** (`adat/nyilt_kodkonyv.tsv` és a generált `KODKONYV.md`): minden új oszlop és érték leírva magyarul és angolul.
7. **Kapu** (`eszkozok/nyilt_mag_kapu.py`, teszttel): (a) minden sornak van érvényes OSIS-kulcsa; (b) minden zárt érték angol címkéje megvan; (c) minden szabad szövegű mezőnek van angol párja vagy kimondott hiány-jelölése; (d) a gépi fordítás jelölése minden fordított mezőn ott van; (e) a forrás-hash egyezik; (f) a csomagban nincs KJV-Strong (GPL) eredetű érték — a meglévő licencszűrés kiterjesztése az új oszlopokra.
8. **MI-nyilatkozat**: egy mondat a `kozlemeny/MI_NYILATKOZAT.md`-ben (és az angol párjában, `kozlemeny/en/`) arról, hogy az angol párhuzamos mezők gépi fordítások, melyik modellel, jelölve. A DT605/DT606 helyőrzőihez nem nyúl.
9. Újragenerálás: `python eszkozok/nyilt_mag_export.py`, a commitolt `nyilt_mag/` naprakész (E35 zöld), a hash-fájl (`ELLENORZO_OSSZEG.sha256`) újra.

**Nincs benne:** a lexikongenerátor fordítás-paraméterezése; a BSB-alapú angol próbalap; a kéziratok (`kozlemeny/data_paper/kezirat_*.md`) átírása (a „Hungarian column names and values” korlát-mondat frissítése nyitott tétel, N-F170a); a KJV-Strong bármilyen formában; a lexikon (`lexikon/`) bármely fájlja; a magyar szöveg bármilyen javítása (ha a fordítás forráshibát mutat, az tétel, nem javítás).

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md): a session `opus`; a fordítási subagent `sonnet` (a saját modellnevét a kimenetbe írja). Olvasd: `F162_NYILT_MAG_BRIEF.md`, `adat/SEMA.md` nyílt mag szakasza, `nyilt_mag/KODKONYV.md`, `kozlemeny/MI_NYILATKOZAT.md`.
1. **Felmérés** (`naplok/NYILT_MAG_ANGOL_felmeres.md`): oszloponként a zárt/szabad besorolás, a fordítandó egyedi szövegek száma és karakterszáma (költségbecslés), a leképezendő könyvnevek száma és a leképezhetetlenek listája, a `jelentes_en` mai forrása.
2. OSIS-kulcs a generátorban, kapu (a) + teszt. Commit (`F170.1`).
3. ⛔ **Zárt címkék helye**: párhuzamos `_en` oszlop vagy csak kódkönyv-hivatkozás — javaslat az 1. lépés számaival, tétel `dontesek/uj/<ágnév>.md`-be (helyőrző `DT626`), megállás.
4. Zárt címkék a választás szerint, kódkönyv, kapu (b). Commit (`F170.2`).
5. ⛔ **Fordítás indítása**: a becsült költség (subscription-subagent vagy API-keret, `forditas_api_keretbol` gyakorlat) és a fordítási prompt (terminológia: a projekt angol olvasói fájljainak szóhasználata, a „lexicon” / „open data core” pár, „termék / product” szó nincs) bemutatva; a felhasználó „mehet”-je nélkül nem indul.
6. Fordítás Sonnettel (`eszkozok/nyilt_mag_angol.py`: kötegelés, hash, tárolás `adat/nyilt_angol.tsv`-be — **TSV-írás `'\t'.join()`**, CLAUDE.md), majd az export beköti; kapu (c)–(e). Szúrópróba: 30 véletlen sor (rögzített mag) angol–magyar összevetése az Opus-sessionben, eltérés a naplóba. Commit (`F170.3`).
7. Motívum-meghatározások angolul, ugyanígy. Commit (`F170.4`).
8. Licenc: kapu (f), MI-nyilatkozat mondata (hu/en). Commit (`F170.5`).
9. Újragenerálás, `python eszkozok/nyilt_mag_kapu.py` 0 BUKÁS, `python eszkozok/teszt_nyilt_mag.py` zöld, E35 zöld; jelentés `naplok/NYILT_MAG_ANGOL_jelentes.md` (számok a futás kimenetéből). Független ellenőr (`fuggetlen-ellenor`). Draft PR; a merge a felhasználóé.

## 4. Elfogadási feltételek

- Az export minden igehelyes sorában érvényes OSIS-kulcs áll; 0 leképezhetetlen (vagy a leképezhetetlenek listája a jelentésben, és a generátor ezekre megáll).
- Minden zárt értéknek van angol címkéje; minden szabad szövegű mezőnek angol párja és gépi-fordítás jelölése (modellnév a futásból), vagy kimondott hiány.
- A forrás-hash minden fordított mezőn egyezik; a kapu bukik, ha a magyar forrás változott és a fordítás nem.
- A csomagban 0 KJV-Strong-eredetű érték (kapu mér); az angol szójelentés forrása STEPBible-glossza, attribúcióval.
- `nyilt_mag_kapu.py` 0 BUKÁS, `teszt_nyilt_mag.py` zöld, a CI-ben E35 zöld.
- Kódkönyv: minden új oszlop és érték hu/en; az MI-nyilatkozat egy mondata a gépi fordításról (hu/en).
- A 30 soros szúrópróba eredménye a jelentésben (hány sor jó, hány javítandó, javítás csak a fordításon).

## 5. Döntésnapló

- `nem_fugg: [38, 123, 163]` (befogadás, 2026-11-05): a #38 és a #123 csak olvasott táblát (normalizáló tábla, `motivumok.tsv`) ír; az export mindig a mai állapotból generál, és az E35 minden adatváltozásnál újragenerálást kér. A #163 (`dontesre_var`) az MI-nyilatkozat DT605/DT606 helyőrzőin vár; ez a feladat csak egy mondatot ad hozzá, a helyőrzőket nem érinti (a kettő a `kizar` miatt nem fut egyszerre).
- Ütközés a #171-gyel (`eszkozok/nyilt_mag_export.py`, `nyilt_mag/`): a két feladat nem fut egyszerre; a sorrend szám szerint #170 → #171, vagy a #171 kézirat-része előre (a generátor-rész a #170 merge-e után).
- N-F170a (nyitott, `NYITOTT_FELADATOK.md`): a `kezirat_en.md` „Hungarian column names and values” korlát-mondata a #170 után frissítendő.
