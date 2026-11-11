# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | bemenet=adat/motivumok.tsv@e1d84722b1,adat/elofordulasok.tsv@f271baeb6f,adat/jeloltek.tsv@874b626869,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Konyv_normalizalo_tabla.tsv@ca2a6132cd,eszkozok/gerinc_terkep.py@56240fb67a,eszkozok/gerinc_kartya.py@a36f96b341,eszkozok/gerinc_szuro.py@24690476cb,eszkozok/general.py@da14f8309f,eszkozok/lekerdez.py@71db13a73a,eszkozok/strong_util.py@46bc09c70a,tanulmanynevek@7214858e10 | ts=2026-11-11T10:55Z

# Prioritási térkép — hol sűrűsödnek a feldolgozatlan gerinc-találatok

Gépi, determinisztikus összesítő (`eszkozok/gerinc_terkep.py`, F124); a következő igeszakasz kiválasztását támogatja. Csak jelölt-sűrűséget mutat, minősítést nem: minden hely a `jeloltek.tsv`-n át, döntéssel kerülhet be. Részletes táblázat: `naplok/GERINC_TERKEP.tsv`.

**Rangsor** (súlyok nélkül, lexikografikusan): különböző motívumok száma, kollokációs találatok, összes szűrt találat; egyezésnél kanonikus sorrend. **Kizárva:** az `elofordulasok.tsv`-ben szereplő, valamint az `elutasítva`/`beépítve` döntésű hely; a #110 szűrője által kiszűrt sor; a már feldolgozott igeszakasz versei. A `nyitva` jelölt külön oszlop (`nyitva_db`), a szűretlen tág gerinc-Strong (`szuretlen_tag_db`) a sűrűségbe nem számít.

## A legjobb 20 fejezet

| # | Fejezet | Különböző motívum | Motívumok | Kollokációs találat | Összes találat | Nyitva | Szűretlen tag |
|---|---|---|---|---|---|---|---|
| 1 | 4Móz 32 | 2 | ISTENTISZT-001,KIRALY-001 | 2 | 3 | 0 | 25 |
| 2 | Ez 17 | 2 | HAMART-001,KIRALY-001 | 0 | 5 | 0 | 4 |
| 3 | 1Kir 8 | 2 | HAMART-001,KIRALY-001 | 0 | 3 | 0 | 26 |
| 4 | 2Krón 6 | 2 | HAMART-001,KIRALY-001 | 0 | 3 | 0 | 19 |
| 5 | Jer 29 | 2 | HAMART-001,KIRALY-001 | 0 | 3 | 0 | 11 |
| 6 | 2Sám 14 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 16 |
| 7 | Péld 29 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 5 |
| 8 | Ézs 19 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 3 |
| 9 | Ézs 66 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 6 |
| 10 | Jer 14 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 7 |
| 11 | Sir 2 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 7 |
| 12 | Ámós 9 | 2 | HAMART-001,KIRALY-001 | 0 | 2 | 0 | 6 |
| 13 | 5Móz 17 | 1 | KIRALY-001 | 1 | 2 | 0 | 18 |
| 14 | Jer 28 | 1 | KIRALY-001 | 1 | 2 | 0 | 9 |
| 15 | Jer 33 | 1 | KIRALY-001 | 1 | 2 | 0 | 5 |
| 16 | 2Móz 35 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 17 | Józs 21 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 22 |
| 18 | Bír 18 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 21 |
| 19 | 1Sám 1 | 1 | KIRALY-001 | 1 | 1 | 0 | 13 |
| 20 | 1Krón 6 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 51 |

## Motívumonként

A `szuretlen_tag` arány azt mutatja, a motívum új találatainak mekkora hányadára nincs még gépi szűrő (ahol magas, ott kell szűrő-szabály, DT184 (d)).

| Motívum | Szűrt találat | Szűretlen tag | `szuretlen_tag` arány | Nyitva |
|---|---|---|---|---|
| ANTROP-001 | 432 | 1027 | 70% | 0 |
| HAMART-001 | 68 | 1134 | 94% | 0 |
| ISTENTISZT-001 | 10 | 0 | 0% | 0 |
| KIRALY-001 | 225 | 643 | 74% | 0 |
| MENNY-001 | 0 | 5496 | 100% | 0 |

## Lefedettség-mérés

- Fedett vers (tanulmányfájl-nevekből): 401
- Értelmezett tanulmányfájl: 23
- Nem értelmezhető fájlnév: 1

  - `melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md` — a fájlnév nem értelmezhető igeszakasz-tanulmányként
