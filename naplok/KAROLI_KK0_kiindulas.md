# KAROLI_KK0_kiindulas.md — kiindulás újramérése a `main`-en

*KK0 — KAROLI_KULCS_BRIEF.md §3 szerint, 2026.09.25. Ág:
`claude/karoli-kulcs-35158`, `main`-ről indítva (`a6783e4`). Szkriptek:
`naplok/KAROLI_KK0_kiindulas_general.py`, `naplok/KAROLI_KK0_versszam_ellenoriz.py`.*

## §0 számainak újramérése

| # | Mérés | Brief-érték | Újramért érték | Egyezik? |
|---|---|---|---|---|
| 0.1 | `karoli_ok` szósor-szinten | ures 441 718 · nincs_karoli_konyv 133 229 · szamozas_elteres 20 346 · zsolt_felirat_eltolas 14 065 · kezi_eltolas_tabla 5 025 · nincs_mt_parositas 2 490 | ugyanaz | igen |
| 0.2 | `szamozas_elteres` versszinten | 1 015 vers, 112 fejezet, 16 fájl, `psalms-lxx.tsv` 63 fejezet | ugyanaz | igen |
| 0.3 | A lexikon 15 sora | l. brief lista | ugyanaz (a FORRASJELOLTEK FJ2-menetéből) | igen |
| 0.4 | `job-lxx.tsv`, `joshua-vaticanus-b.tsv` fejezetei | 42/42, 24/24 | ugyanaz | igen |
| 0.5 | `KEZI_ELTOLASOK['Job']` | `(38,1..38)`→`None`; `(38,39)`→`(39,1)` | ugyanaz, `eszkozok/lxx_kivonat_fetch_v2.py:369` | igen |
| 0.6 | `job-lxx.tsv` `szamozas_elteres` fejezetenként | 38: 431 · 37: 289 · 17: 176 | ugyanaz | igen |
| 0.7 | Károli–KJV versszám mintafejezetek | Jób 17: 15/16 · 37: 23/24 · 38: 38/41 · Jón 2: 11/10 · Hós 13: 15/16 · Ézs 64: 11/12 | ugyanaz | igen |
| 0.8 | Tartalmi kontroll | Károli Jón 2:3 = LXX 2:3 = KJV 2:2; Károli Jób 17:10 = KJV 17:11 | ugyanaz — közvetlenül ellenőrizve a `Karoli_1908.tsv`-n és a nyers `jonah.json`-on: **Károli Jón 2:3 szó szerint egyezik a nyers (nem eltolt) LXX Jonah 2:3-mal** ("És mondá... Nyomorúságomban... kiálték" = "καὶ εἶπεν... ἐβόησα ἐν θλίψει μου") | igen |
| 0.9 | `eszkozok/ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 | ugyanaz | igen |

Eltérés nincs a §0-hoz képest — a brief méréseit a `main` teljes egészében
megerősíti.

## Első következtetés a 0.8 alapján (előretekintés a KK1-re)

A 0.8 közvetlen ellenőrzése **cáfolja a korábbi FORRASJELOLTEK-menet (FJ2)
Jón 2:3-ra vonatkozó javaslatát** (LXX 2:3→2:4 eltolás): a Károli szövege
szó szerint egyezik a **nem eltolt**, raw LXX Jonah 2:3-mal, nem a
verse_pairs.jsonl TVTMS-térkép szerinti (MT 2:3 → grk 2:4) céllal. Ez a H2
munkahipotézist (Károli MT-számozást követ Jónásban) erősíti, nem a
KJV/TVTMS-alapú eltolást — a KK1-ben részletesen dokumentálva.
