# KAROLI_KK7_2_ok_es_javitas.md — az ok igazolása és a javítás

*KK7.2 — KAROLI_KULCS_KK7_BRIEF.md §3.*

## A 0.6 négy példája — az ok igazolása (a javítás ELŐTT, a KK6-os kimeneten)

| LXX-vers | KK6-kimenet (hibás) | Helyes | Ág, amelyik a hibát adta |
|---|---|---|---|
| Isaiah 63:1 | Ézs 63:2 | Ézs 63:1 | `resolve_karoli` H2-ág: `d = karoli_max(19) − kjv_max(18) = 1`; `uj_vers = kjv_v(1) + 1 = 2` — **egyenletes** eltolás a fejezet MINDEN versére |
| Isaiah 63:12 | Ézs 63:13 | Ézs 63:12 | ugyanaz a H2-ág, ugyanaz a `d=1` |
| 4Móz (Numbers) 6:4 | 4Móz 6:5 | 4Móz 6:4 | ugyanaz a H2-ág |
| 1 Samuel 20:8 | 1Sám 20:9 | 1Sám 20:8 | ugyanaz a H2-ág |

**Igazolva** — mind a négy eset a `resolve_karoli` H2 (MT-szamozás-követés) ágán
ment át, amely a fejezet **teljes hosszkülönbségéből** (`d`) számol egyetlen,
egyenletes eltolást, és ezt a fejezet MINDEN versére alkalmazza. Ez csak
akkor helyes, ha a többletvers a fejezet **elején** van (mint a Zsoltárok
címsora, amire az ág eredetileg épült) — Ézsaiás 63, 4Móz 6 és 1Sám 20
esetében a többlet **máshol** van a fejezetben, ezért az egyenletes eltolás
minden verset elcsúsztat. **A hipotézis megerősítve.**

## A javítás (G2 — adatvezérelt)

A `resolve_karoli` mindkét "újonnan töltő" ágát (a H1 KEZI-identitás-tartalék
és a H2 MT-szamozás-ág) kiegészítettük egy `load_fejezet_dontes()` hívással,
amely a `naplok/KAROLI_KK7_fejezet_dontes.tsv` (KK7.1) tábláját olvassa:

- ha a fejezet döntése **`ures`** → a sor `szamozas_elteres` marad (G1: üres
  jobb, mint hibás) — a régi, egyenletes eltolás **nem** fut le;
- ha a fejezet döntése **`elfogad`**, az `elfogadott_eltolas` oszlop értékét
  **hozzáadjuk** a korábban (KK6-ban) számolt célvershez — ez korrigálja az
  egyenletes eltolást a tartalmi próba által mért, helyes értékre;
- ha a fejezetre nincs bejegyzés a táblában (a fejezetben nem volt újonnan
  kitöltött kulcs, tehát a KK7.1 nem is vizsgálta), a viselkedés **változatlan**
  marad a KK6-hoz képest — ez biztosítja a K1 nem-regressziót minden, korábban
  már helyesen kitöltött sorra.

**Fontos:** ez NEM egy heurisztikus új ág (a brief G2 kifejezetten tiltja),
hanem a MEGLÉVŐ H1/H2 ágak kimenetének egy tábla-vezérelt utókorrekciója —
a döntés (elfogad/üres) és a korrekció mértéke kizárólag a KK7.1 mért
korrelációiból származik, kézzel beírt szám vagy könyv-specifikus feltétel
nélkül.

## Ellenőrzés a javítás után (nyers kimenet)

| LXX-vers | Javított kimenet | Ellenőrizve |
|---|---|---|
| Isaiah 63:1 | **Ézs 63:1** | ✓ közvetlenül a regenerált `isaiah.tsv`-ben |
| Isaiah 63:12 | **Ézs 63:12** | ✓ közvetlenül a regenerált `isaiah.tsv`-ben |
| Numbers 6:4 | **4Móz 6:4** | ✓ közvetlenül a regenerált `numbers.tsv`-ben |
| 1 Samuel 20:8 | **1Sám 20:8** | ✓ közvetlenül a regenerált `1-samuel.tsv`-ben |
| Jonah 2:3 | **Jón 2:3** | ✓ változatlan (a fejezet döntése `elfogad, 0` — már korábban is helyes volt) |

Mind a négy példa (és a próbakő, Ézs 63:13, l. KK7.4) most már helyes célt ad.
