# F111_zaras.md — az `/elteres` parancs zárójelentése

Modell: claude-sonnet-5-5 (a brief `sonnet` mezőjével egyezik). Ág: `claude/f111-elteres`. Push, PR, merge nem történt.
- Elkészült: `.claude/commands/elteres.md` (a 3.1 mind a hét lépése, SOHA-lista, `teves` csak saját lekérdezéssel, `munka: ertelmezo` → csak a brief modelljének végrehajtója, korlát 2 kör, a korlátnál megállás); `kovetkezo.md` 9. lépése egyetlen új mondat (G5).
- Korábbi javítókörök átnézése (F23.D8–Z5, F93.12–F93.23, F99.32–F99.46, F108.6–7): minden valódi tétel besorolható; ⛔ (`DT-F111a`) nem kellett. Egy határeset: az F108 „commit-granularitás” tétele (már megtörtént, utólag nem javítható): az `elteres.md` 2. lépése `tartalmi`-nak sorolja (döntés az elfogadásról), ezt a szöveg kimondja.
- Megállapított gyakorlat, amit a parancs egységesít: körszám korlát nélkül (F23: 5, F93: 3 újraellenőrzés), `_ujra` név (F99), külön vagy összevont jelentés-rögzítés, hatókörön kívüli lelet csak az F99-nél ment a `beerkezo/`-ba.
- G7: `python eszkozok/feladatok.py ellenoriz` → 138 brief, 0 hiba.

## Egyeztetett eltérés
- E1: a száraz próba célpontja a brief 3.2/4 pontjában szereplő `naplok/ELLENOR_F9.md` helyett `naplok/ELLENOR_F115.md` (az F9 jelentés nem létezik, a `claude/f09-szotar-s2` PR-ja, #381, már mergelt). A brief 2. pont „Nincs benne” f09-szotar-s2 sora ezért elavult. A próba írás nélkül, az F115-höz tartozó fájlt/ágat nem módosítottam; a G6 ennek megfelelően értendő.
- E2: D2 (korlát 2 kör) eldöntve a felhasználó 2026-10-18-i jóváhagyásával; a korlát elérésekor a megmaradt tételek tételesen (jelentés + tételszám + egy szavas kategória) kerülnek a brief `kovetkezo` mezőjébe (`elteres.md` 6. lépés).

## Száraz próba: az `ELLENOR_F115.md` (ELTÉRÉS: 7 tétel) besorolási javaslata (kör: 1 / 2, javaslat, javítás nem történt)
| # | tétel | kategória | indok |
|---|---|---|---|
| 1 | G7: `teszt_bdb_vers_jelentes.test_bajtra_azonos` bukik | tartalmi | a hash-eltérés okai részben nem e tétel (DT-F99n/DT179); döntés: külön tétel vagy ir-bővítés |
| 2 | G8: nincs olvasó-teszt a jelölőre | mechanikus | a teszt megírható; a kézi böngészős ellenőrzés a felhasználóé (jelezni) |
| 3 | CI E27: ágnévre hivatkozás (`NYITOTT_FELADATOK.md:144`) | mechanikus | hivatkozás/push-sorrend javítása, nincs értelmezés |
| 4 | N57 félrevezető címke | mechanikus | a rés a Macula `karoli` oszlopában van (mért); a címke pontosítása |
| 5 | `strong_elteres` 714/1029 üres LXX_OS-Strong | tartalmi | a jelentés szerint a felhasználó dönt (címke vagy osztály) |
| 6 | Teszt (1) megengedő `assertIn` | mechanikus | a mért érték (`rahlfs_igazolt`) a DB-ből adott |
| 7 | `Macula_gorog.tsv` csak `ts` változott | mechanikus | a fájl visszaállítása; teves nem (a diff a jelentés szerint igazolt) |
Összesen: 5 mechanikus, 2 tartalmi, 0 hatókörön kívüli, 0 téves (téves lekérdezés nélkül nem javasolható).
