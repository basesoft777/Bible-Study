# F101 — jelentés (ADATBAZIS_FRISSITES)

## M0 — mérés (2026-11-21, Windows, Python 3.14, `origin/main` 8d3eca35)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py --mod teljes (--gyoker a worktree, ideiglenes kimenet a repón kívül), ideiglenes mérőszkript | ts=2026-11-21`*

1. **Építési idő, Windows:** az építés (`Epito.epit`) 146,1 s, 1125,3 MB, 120 tábla; a táblánkénti hash-számítással és a meta-íréssel együtt a teljes futás 221,7 s. Az `integritas()` ellenőrzés ebben benne van, külön nem mértem.
2. **WSL (`pardes` disztribúció, 2026-11-22, javítva: az első bejegyzés téves disztribúcióra utalt):** a `pardes` disztribúció venvjével (`~/pardes/eszkozok/olvaso_szerver/.venv`, Python 3.12.3), a friss `HEAD` kivonatán (`git archive`, a WSL natív `/tmp`-jén) az építés 96,0 s, a teljes futás 141 s; kimenet 1125,3 MB, 120 tábla, a bájtméret azonos a Windows-építésével (1 179 987 968 B). A WSL tehát kb. 1,5-szer gyorsabb, mint a Windows (146 s / 221,7 s). A `~/pardes` checkout maga régi (`f6f6f50`, F76.7), módosított, és az integritás-ellenőrzésen elbukik (rc=1, 56 + 714 sértés), ezért azon nem épül adatbázis: az automatikus építésnek friss forrásból kell dolgoznia. A WSL→Windows másolás idejét nem mértem.
3. **Forrásfájlok:** az `adat/` és a `konkordancia/` összesen 452 fájl, 1020 MB; a `stat` (mtime+méret) az egészre 0,25 s. A teljes `sha256` a 718 MB-nyi `.tsv`-re 30,2 s, tehát indításkor nem használható, csak mtime-eltéréskor.
4. **Az építő által ténylegesen olvasott fájlok listája hiányos:** az `open()`-t figyelő mérés csak 25 fájlt (100,6 MB) látott, mert a többit más úton olvassa az építő (a `KONKORDANCIA_ALTALANOS` lista és az `adat/` táblák). M1-ben a listát a kódból kell kinyerni, nem a futásból.
5. **Nem mért:** a `git checkout`/`pull` mtime-hatása (az mtime módosul akkor is, ha a tartalom nem), ezért a javaslat mtime+méret, eltéréskor `sha256`.

## ⛔ M0 megállás — döntések: DT-F101a, DT-F101b (`dontesek/uj/adatbazis-frissites.md`)
