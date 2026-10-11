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

Az F54 hatásában tehát a Zsolt 13-on kívül **sor nem tűnik el**, csak hozzá jön. A teljes újragenerálás viszont a Zsolt 13-on kívül is töröl sorokat (352 sor, 34 pár: 4Móz 3, Hós 3, Préd 23, Ézs 5 pár), ezért — a DT-F54b 2. feltétele szerint — megálltam, és a fájlt **nem** commitoltam újragenerálva (a commitolt állapot változatlan).

Eltűnt párok (heber, igehely), könyvenként: Préd 23 (pl. H0430 Préd 2:24, 9:1, 9:7; H1121 Préd 2:3, 2:7, 9:3, 9:12, 10:17; H2416 Préd 2:17, 2:3, 9:3, 9:4, 9:9; H7451 Préd 2:17, 2:21, 9:12, 10:5, 10:13; H5315 Préd 2:24; H7043 Préd 10:10), Ézs 5 (H1121 / H7121 Ézs 9:5; H3678 / H4467 Ézs 9:6), Hós 3 (H0430 Hós 12:4, 12:7, 12:10), 4Móz 3 (H1121 4Móz 30:2; H5315 4Móz 30:3, 30:14).
