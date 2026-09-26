# KAROLI_KK75_jelentes.md — újramérés és jelentés ⛔

*KK7.5.3 — KAROLI_KULCS_KK75_BRIEF.md §3. Ág: `claude/karoli-kulcs-35158`.*

## §1 mércék

| Mérce | Eredmény |
|---|---|
| A §0 négy verse a "Helyesen" oszlop szerint áll | **igen** — `1 Samuel 20:41→1Sám 20:41`, `20:42→1Sám 20:42`, `21:1→1Sám 20:43`, `21:2→1Sám 21:1`, mind közvetlenül ellenőrizve a regenerált `1-samuel.tsv`-ben |
| Korpuszszintű keresés — nyitott találat | a KK7.5.1 keresése 1 valódi hibát talált (1Sám 20:42/21:1), ez a KK7.5.2-ben javítva; a `naplok/KAROLI_KK75_hatarkereses2_general.py` **strukturális** detektor (a `verse_pairs.jsonl` mintázatát nézi, nem a végső kimenetet) ezt a mintázatot továbbra is jelzi — ez várható, mert a felülbírálási tábla a `resolve_karoli` elején, a mintázat felett avatkozik be; a **tényleges kimenet** mind a 4 versre helyes (l. fent) |
| Nem-regresszió | 460 808 korábban kitöltött szósor **változatlan**, **0 eltűnt** |
| Próbakő: Ézs 63:13 | **egyező** (változatlan a KK7.4 óta) |
| Lexikon-fixpont, 8 motívum | mind a 8-ra `general.py --cel lexikon --id X --ellenoriz` → **0 eltérés** |

## A lexikon "Egyezés"-bontása — KK7 után → KK7.5 után

| Kategória | KK7 után | KK7.5 után |
|---|---|---|
| egyező | 126 | 126 |
| kutatói azonosítás függőben | 87 | 87 |
| szamozas_elteres | 12 | 12 |
| eltérő | 3 | 3 |
| nincs LXX_OS-könyv | 5 | 5 |
| LXX-minusz | 1 | 1 |

**Nincs változás** — a brief maga is jelezte: "Motívum-igehelyet nem érint"
(az 1Sám 20/21 határ egyik lezárt motívum ÓSZ-előfordulási listáján sem
szerepel). A javítás a nyers `LXX_OS`-adatot pontosította, a 8 vizsgált
motívum lexikonoldalát nem.

## K1–K6

| # | Feltétel | Állapot |
|---|---|---|
| K1 | a KK előtti 460 808 kulcs változatlan; 0 eltűnt sor | **RENDBEN** |
| K2 | a §0 négy verse helyes; a §1 keresése után 0 nyitott (a)/(b)/(c) találat | **RENDBEN** — az egyetlen valódi találat javítva, a többi (a)/(b)/(c) hit dokumentáltan szándékos vagy valódi LXX-minusz (l. `KAROLI_KK75_hatarkereses_jelentes.md`) |
| K3 | az importer nem olvas a `naplok/` alól (grep) | **RENDBEN** — `grep -n '"naplok"' eszkozok/lxx_os_import.py` nulla találat; a döntéstábla és a felülbírálási tábla mindkettő `konkordancia/LXX_OS/` alatt |
| K4 | az Ézs 63:13 "egyező"; a lexikon-fixpont 8/8 motívumon 0 eltérés | **RENDBEN** |
| K5 | `ellenoriz.py`: RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 | **RENDBEN** — pontosan ez az érték |
| K6 | nincs `csv` modul; héber/görög szöveg csak fájlba írt szkriptből | **RENDBEN** |

**Minden feltétel RENDBEN.**
