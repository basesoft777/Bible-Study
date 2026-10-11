# ELLENŐR (3. kör) — F62_STRONG_NORMALIZAL_BRIEF.md · a4a8c3d1..6cdb4937 (F62.6–F62.9)

*A jelentést a `fuggetlen-ellenor` subagent adta (nem volt fájlíró eszköze, a szerepköre a teszt-, `ellenoriz.py`-, `betolt.py`- és `gh`-futtatást nem engedi); a fő session írta ki, tömörítve. A teszteket és az `ellenoriz.py`-t a fő session futtatta az F62.6 után (24/24, 11/11, sértés 0; l. a PR-leírást).*

**Összegzés: ELTÉRÉS: 4 tétel — mind dokumentációs, javítás: F62.10.**

1. **K4:** az `allapot: lezarva` (F62.7) a 3. kör előtt került be, a 2. kör 6 eltéréssel zárt; ez a kör is talált eltérést, tehát a K4 a lezáráskor nem teljesült. (Az 1–4. tétel javítása után sincs 4. kör; a K4 formálisan nem teljesül, a PR-ben jelezve.)
2. A `lezarva_osszegzes` csak az N-F62a-t nevezte nyitottnak (N-F62b, N-F62c hiányzott), a `betolt.py` bájtazonosságot és a „0 eltérés"-t minősítés nélkül mondta.
3. A zárás 14. sora („a brief `allapot: fut` marad") ellentmondott a `lezarva` fejlécnek.
4. A brief `ir` mezője nem sorolta fel a két `naplok/ELLENOR_STRONG_NORMALIZAL*.md` fájlt.

**A 2. kör 6 eltéréséből #2–#6 rendben** (hibaüzenet CLI-szinten: `scan H20447` javaslat nélkül, `scan G020447` → G20447; `domen h779` → H0779; G20447-leltár az N-F62a-ban és a zárásban; `ir`/`kovetkezo`; M0 fájlszám: 9+38+1 = 48 fájl, 11+38+1 = 50 oszlop). N-F62b/c helyőrző-alakú; nincs végleges DT/N szám; adattábla Δ=0; CI-szabályok (`futtat.py`) 0 találat az F62-fájlokon.

**Megjegyzés:** `domen h0032a`/`a0002` kisbetűvel félrevezető hibaüzenetet ad; ez nem regresszió (a main is kisbetűsítés nélkül olvasott).

**NEM ELLENŐRIZHETŐ az ellenőr által:** tesztek és `ellenoriz.py` futtatása; N-F62b „8 study a baseline-on is hibás"; a PR léte (`gh`).
