# F54 — a `LXX_versszintu_parok.tsv` újragenerálásának különbség-kimutatása (DT-F54b)

*2026.10.11 · modell: sonnet · `scope=konkordancia/LXX_versszintu_parok.tsv (commitolt, ts=2026-09-28) vs eszkozok/lxx_versszintu_import.py újrafuttatása | forras=manual (összevetés) | ts=2026-10-11`*

Összevetés a (heber_strong, igehely, lxx_igehely, gorog_strong) négyes szerint, a `proveniencia` (ts) oszlop nélkül.

| | sor | (heber, igehely) pár |
|---|---|---|
| commitolt fájl | 99 356 | |
| újragenerált | 104 518 | |
| **hozzájött** | **5 529** | 647 teljesen új pár |
| **eltűnt** | **367** | 34 teljesen eltűnt pár |
| változott (ugyanaz a pár, más sorhalmaz) | | 2 (a Zsolt 13:3 és 13:4) |

## Az eltűnt sorok oka — két külön hatás

Az újragenerálást három lépésben szétválasztottam (a) a commitolt fájl, (b) az M1 előtti `LXX_OS` + a mai `TAHOT_kivonat.tsv`, (c) a mai `LXX_OS` + mai TAHOT között:

| Hatás | eltűnt | hozzájött | magyarázat |
|---|---|---|---|
| (a)→(b): a `TAHOT_kivonat.tsv` F85.6-os átkulcsolása (a fájl 2026-09-28-i, az F85 előtti kulcsokból készült) | 352 sor | 4 597 | a TAHOT `Igehely` kulcsa Károli-verssé vált (Préd 2/9/10, Hós 12, Ézs 9, 4Móz 30: korábban eltolt kulcs); ez nem az F54 hatása |
| (b)→(c): az F54 M1 (438 új kulcs + Zsolt 13 javítás) | **15** (mind Zsolt 13) | 932 | az eltűnt 15 sor a Zsolt 13:3 (8) és Zsolt 13:4 (7) hibás, eltolt LXX-verse (12:4, 12:5); helyette a helyes versek kerülnek be |

Az F54 hatásában tehát a Zsolt 13-on kívül **sor nem tűnik el**, csak hozzá jön. A teljes újragenerálás viszont a Zsolt 13-on kívül is töröl sorokat (352 sor, 34 pár: 4Móz 3, Hós 3, Préd 23, Ézs 5 pár), ezért a DT-F54b 2. feltétele szerint megálltam (DT-F54c); a DT-F54c 🟢 (1. opció) után a teljes újragenerálás két külön commitban megtörtént (F54.7: F85-örökség, F54.8: F54-hatás) — l. az alábbi „Végrehajtás” szakaszt.

Eltűnt párok (heber, igehely), könyvenként: Préd 23 (pl. H0430 Préd 2:24, 9:1, 9:7; H1121 Préd 2:3, 2:7, 9:3, 9:12, 10:17; H2416 Préd 2:17, 2:3, 9:3, 9:4, 9:9; H7451 Préd 2:17, 2:21, 9:12, 10:5, 10:13; H5315 Préd 2:24; H7043 Préd 10:10), Ézs 5 (H1121 / H7121 Ézs 9:5; H3678 / H4467 Ézs 9:6), Hós 3 (H0430 Hós 12:4, 12:7, 12:10), 4Móz 3 (H1121 4Móz 30:2; H5315 4Móz 30:3, 30:14).

## Végrehajtás (DT-F54c, 1. opció) — két külön commit

| Commit | Tartalom | eltűnt | hozzájött |
|---|---|---|---|
| F54.7 | az F85 TAHOT-átkulcsolás öröksége (a mai TAHOT + az M1 előtti `LXX_OS`, 6d1360b6); DT92 | 352 sor (34 pár) | 4 597 sor |
| F54.8 | az F54 kulcsai (438 + 6 extra + Zsolt 13 javítás) | 15 sor (mind Zsolt 13) | 932 sor |

Az F54.8-ban a Zsolt 13-on kívül sor nem tűnt el. A két lépés összege: 367 eltűnt, 5 529 hozzájött sor (a fenti táblával egyezően).

## A 34 eltűnt (heber_strong, igehely) pár — tételesen

Mindegyiknél a mai `TAHOT_kivonat.tsv`-ben a (Strong, igehely) pár **0 sorral** szerepel (ellenőrizve: a `Strong-szám` oszlop a megadott Strongot az adott `Igehely`-en nem tartalmazza). A „szomszéd” oszlop azt mutatja, mely közeli versben (±2) van meg a Strong a mai TAHOT-ban, vagyis hová csúszott a pár az F85 átkulcsolásával.

| Strong | Igehely | LXX-vers (a régi sorban) | régi sor | szomszéd a mai TAHOT-ban |
|---|---|---|---|---|
| H0430 | Hós 12:4 | Hosea 12:5 | 9 | 12:3, 12:5, 12:6 |
| H0430 | Hós 12:7 | Hosea 12:8 | 6 | 12:5, 12:6, 12:9 |
| H0430 | Hós 12:10 | Hosea 12:11 | 6 | 12:9 |
| H0430 | Préd 2:24 | Ecclesiastes 2:23 | 9 | 2:25, 2:26 |
| H0430 | Préd 9:1 | Ecclesiastes 8:16 | 14 | 9:2, 9:3 |
| H0430 | Préd 9:7 | Ecclesiastes 9:5 | 10 | 9:9 |
| H1121 | 4Móz 30:2 | Numbers 30:3 | 15 | 30:1 |
| H1121 | Préd 2:3 | Ecclesiastes 2:2 | 5 | 2:4 |
| H1121 | Préd 2:7 | Ecclesiastes 2:6 | 5 | 2:8, 2:9 |
| H1121 | Préd 9:3 | Ecclesiastes 9:1 | 15 | 9:5 |
| H1121 | Préd 9:12 | Ecclesiastes 9:10 | 16 | 9:14 |
| H1121 | Préd 10:17 | Ecclesiastes 10:20 | 13 | — |
| H1121 | Ézs 9:5 | Isaiah 9:4 | 9 | 9:6 |
| H2416 | Préd 2:3 | Ecclesiastes 2:2 | 5 | 2:4 |
| H2416 | Préd 2:17 | Ecclesiastes 2:16 | 13 | 2:18 |
| H2416 | Préd 9:3 | Ecclesiastes 9:1 | 15 | 9:5 |
| H2416 | Préd 9:4 | Ecclesiastes 9:2 | 11 | 9:5, 9:6 |
| H2416 | Préd 9:9 | Ecclesiastes 9:7 | 12 | 9:7, 9:11 |
| H3678 | Ézs 9:6 | Isaiah 9:5 | 15 | 9:7 |
| H4467 | Ézs 9:6 | Isaiah 9:5 | 15 | 9:7 |
| H5315 | 4Móz 30:3 | Numbers 30:4 | 8 | 30:2, 30:4, 30:5 |
| H5315 | 4Móz 30:14 | Numbers 30:15 | 6 | 30:12, 30:13 |
| H5315 | Préd 2:24 | Ecclesiastes 2:23 | 9 | 2:25 |
| H7043 | Préd 10:10 | Ecclesiastes 10:13 | 6 | — |
| H7121 | Ézs 9:5 | Isaiah 9:4 | 9 | 9:6 |
| H7451 | Préd 2:17 | Ecclesiastes 2:16 | 13 | 2:18 |
| H7451 | Préd 2:21 | Ecclesiastes 2:20 | 6 | 2:22 |
| H7451 | Préd 9:2 | Ecclesiastes 8:17 | 16 | 9:4 |
| H7451 | Préd 9:3 | Ecclesiastes 9:1 | 15 | 9:4, 9:5 |
| H7451 | Préd 9:12 | Ecclesiastes 9:10 | 16 | 9:14 |
| H7451 | Préd 10:5 | Ecclesiastes 10:8 | 7 | — |
| H7451 | Préd 10:13 | Ecclesiastes 10:16 | 7 | — |
| H7585 | Préd 9:10 | Ecclesiastes 9:8 | 8 | 9:12 |
| H8034 | Ézs 9:5 | Isaiah 9:4 | 9 | 9:6 |

**A független ellenőrnek mintázandó három pár** (a mai TAHOT-kulcson nem áll elő a pár; a mintázás azt igazolja, hogy a pár tényleg az F85 előtti, eltolt kulcsra épült, nem hiba az újragenerálásban):
1. **H7043 Préd 10:10** — nincs közeli vers a mai TAHOT-ban (a legerősebb eset: a Strong ±2 versben sincs meg);
2. **H0430 Hós 12:4** — a Strong a 12:3, 12:5, 12:6-ban van meg (a Hós 12 eltolás-régió, F85);
3. **H5315 4Móz 30:3** — a Strong a 30:2, 30:4, 30:5-ben van meg (4Móz 30 eltolás-régió, F85).
