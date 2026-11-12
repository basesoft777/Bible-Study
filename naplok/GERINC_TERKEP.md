# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | bemenet=adat/motivumok.tsv@fed05b71e3,adat/elofordulasok.tsv@486122a095,adat/jeloltek.tsv@3711124e5b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Konyv_normalizalo_tabla.tsv@ca2a6132cd,eszkozok/gerinc_terkep.py@56240fb67a,eszkozok/gerinc_kartya.py@a36f96b341,eszkozok/gerinc_szuro.py@24690476cb,eszkozok/general.py@3d54261253,eszkozok/lekerdez.py@71db13a73a,eszkozok/strong_util.py@46bc09c70a,tanulmanynevek@7214858e10 | ts=2026-11-12T18:45Z

# Prioritási térkép — hol sűrűsödnek a feldolgozatlan gerinc-találatok

Gépi, determinisztikus összesítő (`eszkozok/gerinc_terkep.py`, F124); a következő igeszakasz kiválasztását támogatja. Csak jelölt-sűrűséget mutat, minősítést nem: minden hely a `jeloltek.tsv`-n át, döntéssel kerülhet be. Részletes táblázat: `naplok/GERINC_TERKEP.tsv`.

**Rangsor** (súlyok nélkül, lexikografikusan): különböző motívumok száma, kollokációs találatok, összes szűrt találat; egyezésnél kanonikus sorrend. **Kizárva:** az `elofordulasok.tsv`-ben szereplő, valamint az `elutasítva`/`beépítve` döntésű hely; a #110 szűrője által kiszűrt sor; a már feldolgozott igeszakasz versei. A `nyitva` jelölt külön oszlop (`nyitva_db`), a szűretlen tág gerinc-Strong (`szuretlen_tag_db`) a sűrűségbe nem számít.

## A legjobb 20 fejezet

| # | Fejezet | Különböző motívum | Motívumok | Kollokációs találat | Összes találat | Nyitva | Szűretlen tag |
|---|---|---|---|---|---|---|---|
| 1 | 4Móz 32 | 2 | ISTENTISZT-001,KIRALY-001 | 2 | 3 | 0 | 25 |
| 2 | Ez 17 | 2 | HAMART-001,KIRALY-001 | 0 | 5 | 0 | 4 |
| 3 | 2Krón 6 | 2 | HAMART-001,KIRALY-001 | 0 | 3 | 0 | 19 |
| 4 | Jer 29 | 2 | HAMART-001,KIRALY-001 | 0 | 3 | 0 | 11 |
| 5 | 2Sám 14 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 16 |
| 6 | Péld 29 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 5 |
| 7 | Ézs 19 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 3 |
| 8 | Ézs 66 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 6 |
| 9 | Ámós 9 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 6 |
| 10 | 5Móz 17 | 1 | KIRALY-001 | 1 | 2 | 0 | 18 |
| 11 | Jer 28 | 1 | KIRALY-001 | 1 | 2 | 0 | 9 |
| 12 | Jer 33 | 1 | KIRALY-001 | 1 | 2 | 0 | 5 |
| 13 | 2Móz 35 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 14 | Józs 21 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 22 |
| 15 | Bír 18 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 21 |
| 16 | 1Sám 1 | 1 | KIRALY-001 | 1 | 1 | 0 | 13 |
| 17 | 1Krón 6 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 51 |
| 18 | 2Krón 29 | 1 | KIRALY-001 | 1 | 1 | 0 | 23 |
| 19 | Zsolt 49 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 20 | Zsolt 80 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 7 |

## Motívumonként

A `szuretlen_tag` arány azt mutatja, a motívum új találatainak mekkora hányadára nincs még gépi szűrő (ahol magas, ott kell szűrő-szabály, DT184 (d)).

| Motívum | Szűrt találat | Szűretlen tag | `szuretlen_tag` arány | Nyitva |
|---|---|---|---|---|
| ANTROP-001 | 432 | 1027 | 70% | 0 |
| HAMART-001 | 58 | 1130 | 95% | 0 |
| ISTENTISZT-001 | 10 | 0 | 0% | 0 |
| KIRALY-001 | 225 | 643 | 74% | 0 |
| MENNY-001 | 0 | 5496 | 100% | 0 |

## Lefedettség-mérés

- Fedett vers (tanulmányfájl-nevekből): 401
- Értelmezett tanulmányfájl: 23
- Nem értelmezhető fájlnév: 1

  - `melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md` — a fájlnév nem értelmezhető igeszakasz-tanulmányként
