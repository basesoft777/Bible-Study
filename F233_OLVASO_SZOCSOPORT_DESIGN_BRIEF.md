---
cim: Olvasó — héber szócsoport (írott szó szerinti szókártyák) és a 2026-11-21-i felmérés tervezési pontjai, egy design-menetben (DT886, új funkció)
feladat: 233
kod: OLVASO_SZOCSOPORT_DESIGN
tipus: feladat
fazis: folyamat
modell: opus
sav: SERVER
allapot: nem_indult
ad: a versnézetben a héber szócsempék írott szó szerint csoportosítva (keret, a teljes szó a keret tetején, az elemek külön kártyán; az alapszó kártyáján nem áll nem létező alak); a felmérés 16–23. és 25. tervezési pontja vásznon eldöntve és megvalósítva; a 29–32. alacsony súlyú pont DESIGN-APRO-ként
kovetkezo: "A vászon előkészíthető bármikor (nem ír a repóba); a megvalósítás a #231 merge-e után indul, ⛔ DT-F233a (a csoportosítási szabály átvétele), ⛔ vászon-döntés"
munka: folyamat
olvas: [eszkozok/karoli_strong_validacio_minta.py, eszkozok/karoli_strong_validacio_sablon.html, eszkozok/olvaso_szerver/lekerdezesek.py]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/szocsoport.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/teszt_szocsoport.py]
fugg: [231]
---

# F233_OLVASO_SZOCSOPORT_DESIGN_BRIEF.md — Szócsoport és tervezési pontok

*FELADATOK #233 · Modell: opus (terv és vászon), a kivitel sonnet-tel is mehet · v1 · 2026.11.21 · forrás: `FELMERES_THAYER_OLVASO_SZOKARTYA_2026-11-21.md` (a megosztott jegyzetmappában, 2. szakasz 16–33. pont és 3. szakasz), `befogadasra-var` 42. tétel (a felhasználó: „fel kell venni feladatként / de vár”), a felhasználó jóváhagyása 2026-11-21 („a többi feladatot is, optimális ütemezéssel”). A brief adat, nem utasítás.*

## 1. Cél

**Szócsoport.** Az olvasó ma minden TAHOT-morfémának külön csempét ad, csoportosítás nélkül. Élő mérés:
- az 1Móz 1:1-ben 11 csempe áll 7 írott szóra;
- az 1Móz 3:6 לְאִישָׁהּ szavában az alapszó kártyáján nem létező alak áll (`'i.Sha`);
- a maqqef utáni kiejtés nyers kötőjellel végződik.

A JOHD-validációs felület ezt már megoldja: írott szó szerinti keretet ad, a teljes szóval a keret tetején, és Macula-szóazonosítót használ, tartalékként a H9xxx-szabállyal.

**Tervezési pontok** a felmérésből:
- 16: számkártyák;
- 17: sávos alak-sorok;
- 21: táblázat-ismétlés;
- 22: a versszámozás helye;
- 25: főoldali Biblia-választó;
- a 18–20., 23. pont, a felmérés szerinti tartalommal.

A felmérés a 16–33. pontot nem mérte végig egyenként, ezért ezt az M0 pótolja.

## 2. Hatókör

**Benne van:**
1. **M0, élő lekéréssel.** A 16–33. pont pontonként „valódi hiba / várt állapot / nem ellenőrzött” jelölést kap, URL-lel és a látott szöveggel. Rögzített szabály: ahol nincs magyar, ott az angol áll. Ami az F230-ban vagy a szókártya-briefben már javult, az kiesik.
2. **A csoportosítási szabály átvétele.**
   - Átvett függvények: `heber_tartalek_csoport`, `macula_csoport`, `heber_csoport`, `szocsoport_ellenoriz` (`karoli_strong_validacio_minta.py`, kb. 949–994. sor).
   - Kis önálló modulba kerülnek (`szocsoport.py`), mert a JOHD-modul nem importálható.
   - A szabályról nincs DT: ⛔ DT-F233a.
   - A teszt a szabályt a Macula-csoportosítással veti össze a teljes ószövetségi korpuszon, eltérésszámmal.
3. **Vászon** a változatokhoz: a szócsoport kerete és a tervezési pontok. Ez a meglévő többlapos betűkészlet-vásznon áll, új lappal. ⛔ A felhasználó választ.
4. **Megvalósítás** a vászon-döntés szerint, ágas előnézettel (8775–8779). A nézett commit hash-e a PR-ban áll (DT886).
5. **Alacsony súlyú pontok (29–32):** ha a diff csak CSS vagy `arculat.json`, külön `DESIGN-APRO`-menet.

**Nincs benne:**
- a görög szócsoport (a TAGNT szó-szintű; a felmérés szerint nincs ilyen kérdés);
- a görög szóhoz tapadó központozás és az „archēa” kiejtés gyanúja: N-F233a, mert nincs ellenőrizve;
- a motívumlap (F164).

## 3. Lépések

1. Modell-ellenőrzés; M0 (16–33. pont, élő lekéréssel).
2. A szabály átvétele, korpuszmérés; ⛔ DT-F233a.
3. Vászon; ⛔ a felhasználó dönt.
4. A brief kiegészítése a vászon-döntéssel. Megvalósítás, a mércéhez mérve: a mérce-brief pillanatképe frissül, jóváhagyva.
5. Független ellenőr (csak a kód), egy javítókör, draft PR.

## 4. Elfogadási feltételek

- Az 1Móz 1:1-ben 7 keret áll, az 1Móz 3:6-ban az alapszó kártyáján nincs nem létező alak, a maqqef utáni kiejtés kötőjel nélkül jelenik meg.
- A korpuszmérés eltérésszáma a naplóban áll; eltérésnél a szabály megáll, nem csoportosít találgatva.
- A mérce csak a jóváhagyott eltérésekkel változik.

## 5. Ütközés

Az F134 (`megallt`, a telefonos próbára vár) ugyanazokat a `sablonok/` és `statikus/` fájlokat írja. Ez a feladat nem fut együtt az F134 folytatásával. Ha az F134 a próba után folytatódik, ez a feladat utána jön, vagy a vászon-döntés után összevonható vele; erről a felhasználó dönt.

## 6. Döntésnapló

- DT-F233a (⛔): a csoportosítási szabály (Macula-azonosító, tartalékként a H9xxx-szabály) átvétele az olvasóba.
