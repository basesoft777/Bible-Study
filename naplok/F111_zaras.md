# F111_zaras.md — az `/elteres` parancs zárójelentése

Modell: claude-sonnet-5-5 (a brief `sonnet` mezőjével egyezik). Ág: `claude/f111-elteres`. Push, PR, merge nem történt.
- Elkészült: `.claude/commands/elteres.md` (a 3.1 mind a hét lépése, SOHA-lista, `teves` csak saját lekérdezéssel, `munka: ertelmezo` → csak a brief modelljének végrehajtója, korlát 2 kör, a korlátnál megállás); `kovetkezo.md` 9. lépése egyetlen új mondat (G5).
- Korábbi javítókörök átnézése (F23.D8–Z5, F93.12–F93.23, F99.32–F99.46, F108.6–7): minden valódi tétel besorolható; ⛔ (`DT-F111a`) nem kellett. Határeset: az F108 „commit-granularitás” tétele (már megtörtént, utólag nem javítható): az `elteres.md` 2. lépése `tartalmi`-nak sorolja.
- Megállapított gyakorlat, amit a parancs egységesít: körszám korlát nélkül (F23: 5, F93: 3 újraellenőrzés), `_ujra` név (F99), külön vagy összevont jelentés-rögzítés, hatókörön kívüli lelet csak az F99-nél ment a `beerkezo/`-ba.
- G7: `python eszkozok/feladatok.py ellenoriz` → 0 hiba (a javítókör végén újra mérve).
- Lezárás: az `allapot: lezarva`, a `pr` és a `lezarva_osszegzes` csak a független újraellenőrzés `TISZTA` jelentése után kerül a fejlécbe (ELLENOR_F111_2 után); addig a brief `megallt`/`fut`.

## Egyeztetett eltérés
- E1: a száraz próba célpontja a brief 3.2/4 pontjában szereplő `naplok/ELLENOR_F9.md` helyett `naplok/ELLENOR_F115.md` (az F9 jelentés nem létezik, a `claude/f09-szotar-s2` PR-ja, #381, mergelt). A brief 2. pont „Nincs benne” f09-szotar-s2 sora elavult. A próba írás nélkül futott; az F115 fájljait/ágát nem módosítottam.
- E2: D2 (korlát 2 kör) a felhasználó 2026-10-18-i jóváhagyásával; a korlátnál a maradék tételesen a `kovetkezo` mezőbe kerül (`elteres.md` 6. lépés).
- E3 (ELLENOR_F111 5.): a brief törzse is változott a fejlécen túl: a D2 sor átírva (E2 kiegészítéssel) és új E1 sor a döntésnaplóban. Mindkettő a felhasználó 2026-10-18-i döntésének rögzítése; az `ir`-en kívüli (brief-törzs) írás ezért egyeztetett eltérés.

## Száraz próba: az `/elteres` 1. lépése az `ELLENOR_F115.md`-re (a próba eredménye)
Eredmény: **a parancs jelez és megáll, nem sorol be.** Az F115 ág PR-ja mergelt: `gh pr list --head claude/f115-macula-chi-xi --state all` → #402, `MERGED` (2026-10-18T13:58Z); `git log origin/main --grep='#402'` → `19b9841b Merge pull request #402`. Az 1. lépés szerint új ág kell a main-ből. Az F115-ön ráadásul már lezajlott javítókör is (F115.8, F115.9: a 6., 7., és az 1. tételt kezelte). A korábbi 7 tételes besorolás ezért **nem a parancs kimenete**; a próba egyszerre azt is igazolja, hogy a mergelt-PR szabály működik.

Szemléltető, nem a parancs kimenete: ha az ág nem volna mergelt, a 2. lépés javaslata (kör: 1 / 2)
| # | tétel | kategória | indok |
|---|---|---|---|
| 1 | G7: `teszt_bdb_vers_jelentes.test_bajtra_azonos` bukik | tartalmi | a hash-eltérés okai részben nem e tétel (DT-F99n/DT179) |
| 2 | G8: nincs olvasó-teszt a jelölőre | hatokoron_kivul | az `eszkozok/olvaso_szerver/teszt_*` nincs az F115 `ir`-jében |
| 3 | CI E27: ágnévre hivatkozás (`NYITOTT_FELADATOK.md:144`) | mechanikus | a `NYITOTT_FELADATOK.md` közös koordinációs fájl (`BRIEF_SABLON.md` kivétele), az `ir`-be nem kell; a hivatkozás javítása egyértelmű |
| 4 | N57 félrevezető címke | mechanikus | a rés a Macula `karoli` oszlopában van (mért) |
| 5 | `strong_elteres` 714/1029 üres LXX_OS-Strong | tartalmi | a jelentés szerint a felhasználó dönt |
| 6 | Teszt (1) megengedő `assertIn` | mechanikus | a mért érték a DB-ből adott |
| 7 | `Macula_gorog.tsv` csak `ts` változott | mechanikus | a fájl visszaállítása |
Összesen: 4 mechanikus, 2 tartalmi, 1 hatókörön kívüli, 0 téves.

## Körszámláló száraz próbája (írás nélkül; `kovetkezo` mező `[elteres_kor k/2]` jelölője, ELLENOR_F111 3.)
A jelölő a `Te:` / `Folytatás:` után áll (`feladatok.py` `startswith` vizsgálat); új fejlécmező nincs (az `elteres_kor` mező `ellenoriz`-en „ismeretlen kulcs” hibát adna, ezért a felhasználó a `kovetkezo`-szöveges megoldást választotta, `feladatok.py` érintetlen).
- (a) `kovetkezo: "Te: [elteres_kor 2/2] ELLENOR_F111_2 …"` + utolsó jelentés `ELTÉRÉS`: 1. lépés: PR nem mergelt → jelentés ELTÉRÉS → `k = 2` = korlát → új kör nélkül megáll, nem sorol, nem egyeztet; 6. lépés szerinti tételes maradék.
- (b) `kovetkezo: "Folytatás: [elteres_kor 1/2] …"` + `ELTÉRÉS`: `k = 1 < 2` → mostani kör 2 → 2. lépés (besorolás), 3. lépés fejléce `kör: 2 / 2`.
- (c) jelölő nélkül: `k = 0` → 1. kör, `kör: 1 / 2`.
