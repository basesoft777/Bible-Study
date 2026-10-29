# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | bemenet=adat/motivumok.tsv@5dd32d70ce,adat/elofordulasok.tsv@8bf0bc5cd1,adat/jeloltek.tsv@b361efb4a9,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Konyv_normalizalo_tabla.tsv@ca2a6132cd,eszkozok/gerinc_terkep.py@56240fb67a,eszkozok/gerinc_kartya.py@a36f96b341,eszkozok/gerinc_szuro.py@24690476cb,eszkozok/general.py@a7f6298c93,eszkozok/lekerdez.py@b9dd893f71,eszkozok/strong_util.py@46bc09c70a,tanulmanynevek@7214858e10 | ts=2026-10-29T11:09Z

# Prioritási térkép — hol sűrűsödnek a feldolgozatlan gerinc-találatok

Gépi, determinisztikus összesítő (`eszkozok/gerinc_terkep.py`, F124); a következő igeszakasz kiválasztását támogatja. Csak jelölt-sűrűséget mutat, minősítést nem: minden hely a `jeloltek.tsv`-n át, döntéssel kerülhet be. Részletes táblázat: `naplok/GERINC_TERKEP.tsv`.

**Rangsor** (súlyok nélkül, lexikografikusan): különböző motívumok száma, kollokációs találatok, összes szűrt találat; egyezésnél kanonikus sorrend. **Kizárva:** az `elofordulasok.tsv`-ben szereplő, valamint az `elutasítva`/`beépítve` döntésű hely; a #110 szűrője által kiszűrt sor; a már feldolgozott igeszakasz versei. A `nyitva` jelölt külön oszlop (`nyitva_db`), a szűretlen tág gerinc-Strong (`szuretlen_tag_db`) a sűrűségbe nem számít.

## A legjobb 20 fejezet

| # | Fejezet | Különböző motívum | Motívumok | Kollokációs találat | Összes találat | Nyitva | Szűretlen tag |
|---|---|---|---|---|---|---|---|
| 1 | 4Móz 32 | 2 | ISTENTISZT-001,KIRALY-001 | 2 | 3 | 0 | 25 |
| 2 | 5Móz 17 | 1 | KIRALY-001 | 1 | 2 | 0 | 18 |
| 3 | Jer 28 | 1 | KIRALY-001 | 1 | 2 | 0 | 9 |
| 4 | Jer 33 | 1 | KIRALY-001 | 1 | 2 | 0 | 5 |
| 5 | 2Móz 31 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 10 |
| 6 | 2Móz 35 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 7 | Józs 21 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 22 |
| 8 | Bír 18 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 21 |
| 9 | 1Sám 1 | 1 | KIRALY-001 | 1 | 1 | 0 | 13 |
| 10 | 1Krón 6 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 51 |
| 11 | 2Krón 29 | 1 | KIRALY-001 | 1 | 1 | 0 | 23 |
| 12 | Zsolt 49 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 13 | Zsolt 80 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 7 |
| 14 | Ézs 40 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 8 |
| 15 | Ézs 45 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 16 | Jer 13 | 1 | KIRALY-001 | 1 | 1 | 0 | 10 |
| 17 | Róm 8 | 1 | ANTROP-001 | 0 | 14 | 0 | 0 |
| 18 | 1Kir 1 | 1 | KIRALY-001 | 0 | 11 | 0 | 37 |
| 19 | ApCsel 2 | 1 | ANTROP-001 | 0 | 9 | 0 | 0 |
| 20 | 1Kor 12 | 1 | ANTROP-001 | 0 | 8 | 0 | 0 |

## Motívumonként

A `szuretlen_tag` arány azt mutatja, a motívum új találatainak mekkora hányadára nincs még gépi szűrő (ahol magas, ott kell szűrő-szabály, DT184 (d)).

| Motívum | Szűrt találat | Szűretlen tag | `szuretlen_tag` arány | Nyitva |
|---|---|---|---|---|
| ANTROP-001 | 431 | 1033 | 71% | 3 |
| HAMART-001 | 8 | 1234 | 99% | 4 |
| ISTENTISZT-001 | 11 | 0 | 0% | 1 |
| KIRALY-001 | 225 | 643 | 74% | 0 |
| MENNY-001 | 0 | 5496 | 100% | 0 |

## Lefedettség-mérés

- Fedett vers (tanulmányfájl-nevekből): 401
- Értelmezett tanulmányfájl: 23
- Nem értelmezhető fájlnév: 1

  - `melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md` — a fájlnév nem értelmezhető igeszakasz-tanulmányként
