# F21P_meres_v2.md — F3 (prompt v1) és F3V2 (prompt v2) az arany v1/v2-höz

<!-- GENERÁLT: eszkozok/karoli_strong/meres_v2.py (meres.py --v2) | scope=f21p F3, F3V2 | forras=f21p/valaszok/F3.jsonl, f21p/valaszok/F3V2.jsonl, f21p/arany_opus.jsonl, f21p/arany_opus_v2.jsonl (befagyasztva, sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, f21p/futasnaplo.tsv | kézzel szerkeszteni tilos -->

Kizárólag szkriptkimenet, a meres.py definícióival. **Egymodelles összeállítás (a C egyedül) nem kaphat „megfelelt” minősítést (PD6):** a táblák a mért számot és a rögzített küszöbhöz való viszonyát adják, minősítést nem. A `magas` pontosság (≥ 98%) egymodelles összeállításra nem értelmezhető; az összpontosság a 98% mellett csak tájékoztató. A korrigált (Opus-besorolásos) érték nem része ennek a jelentésnek (l. naplok/F21P_C_diff.md; az „az Opus besorolása, nem mérés”).

## a) Pontosság és lefedettség (kapun átment aranyversek)

| réteg | mérőszám | F3 × arany v1 | F3 × arany v2 | F3V2 × arany v2 |
|---|---|---|---|---|
| R1 | aranyversek kapun átment | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) |
| R1 | pontosság (tájékoztató a 98% mellett, PD6) | 94.2% (294/312) [92–96] | 94.6% (295/312) [92–96] | 94.0% (299/318) [91–96] |
| R1 | lefedettség | 92.7% (294/317) [90–95] | 93.1% (295/317) [90–95] | 94.3% (299/317) [92–96] |
| R1 | lefedettség vs küszöb 95% | küszöb alatt (< 95%) | küszöb alatt (< 95%) | küszöb alatt (< 95%) |
| R2 | aranyversek kapun átment | 100.0% (10/10) | 100.0% (10/10) | 100.0% (10/10) |
| R2 | pontosság (tájékoztató a 98% mellett, PD6) | 94.2% (146/155) [90–97] | 94.2% (146/155) [90–97] | 95.6% (153/160) [92–98] |
| R2 | lefedettség | 95.4% (146/153) [92–98] | 95.4% (146/153) [92–98] | 100.0% (153/153) [98–100] |
| R2 | lefedettség vs küszöb 95% | elérve (≥ 95%) | elérve (≥ 95%) | elérve (≥ 95%) |
| R3 | aranyversek kapun átment | 100.0% (10/10) | 100.0% (10/10) | 100.0% (10/10) |
| R3 | pontosság (tájékoztató a 98% mellett, PD6) | 91.9% (250/272) [89–94] | 91.9% (250/272) [89–94] | 94.2% (259/275) [91–96] |
| R3 | lefedettség | 94.0% (250/266) [91–96] | 94.0% (250/266) [91–96] | 97.4% (259/266) [95–99] |
| R3 | lefedettség vs küszöb 95% | küszöb alatt (< 95%) | küszöb alatt (< 95%) | elérve (≥ 95%) |
| R4 | aranyversek kapun átment | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) |
| R4 | pontosság (tájékoztató a 98% mellett, PD6) | 92.9% (299/322) [90–95] | 92.9% (299/322) [90–95] | 91.7% (309/337) [89–94] |
| R4 | lefedettség | 94.9% (299/315) [92–97] | 94.9% (299/315) [92–97] | 98.1% (309/315) [96–99] |
| R4 | lefedettség vs küszöb 95% | küszöb alatt (< 95%) | küszöb alatt (< 95%) | elérve (≥ 95%) |
| Összes | aranyversek kapun átment | 100.0% (60/60) | 100.0% (60/60) | 100.0% (60/60) |
| Összes | pontosság (tájékoztató a 98% mellett, PD6) | 93.2% (989/1061) [92–94] | 93.3% (990/1061) [92–94] | 93.6% (1020/1090) [92–95] |
| Összes | lefedettség | 94.1% (989/1051) [93–95] | 94.2% (990/1051) [93–95] | 97.1% (1020/1051) [96–98] |
| Összes | lefedettség vs küszöb 95% | küszöb alatt (< 95%) | küszöb alatt (< 95%) | elérve (≥ 95%) |

## b) Régi arany egyezés (halmaz-definíció; kapun átment versek, 200 verses minta)

| réteg | mérőszám | F3 (prompt v1) | F3V2 (prompt v2) |
|---|---|---|---|
| R1 | egyezés, kizárás nélkül | 93.8% (30/32) [83–98] | 93.8% (30/32) [83–98] |
| R1 | egyezés, a hibás hármasok nélkül | 100.0% (30/30) [92–100] | 100.0% (30/30) [92–100] |
| R1 | (hibás nélkül) vs küszöb 95% | elérve (≥ 95%) | elérve (≥ 95%) |
| R2 | egyezés, kizárás nélkül | — (0/0) | — (0/0) |
| R2 | egyezés, a hibás hármasok nélkül | — (0/0) | — (0/0) |
| R2 | (hibás nélkül) vs küszöb 95% | n.é. | n.é. |
| R3 | egyezés, kizárás nélkül | — (0/0) | — (0/0) |
| R3 | egyezés, a hibás hármasok nélkül | — (0/0) | — (0/0) |
| R3 | (hibás nélkül) vs küszöb 95% | n.é. | n.é. |
| R4 | egyezés, kizárás nélkül | — (0/0) | — (0/0) |
| R4 | egyezés, a hibás hármasok nélkül | — (0/0) | — (0/0) |
| R4 | (hibás nélkül) vs küszöb 95% | n.é. | n.é. |
| Összes | egyezés, kizárás nélkül | 93.8% (30/32) [83–98] | 93.8% (30/32) [83–98] |
| Összes | egyezés, a hibás hármasok nélkül | 100.0% (30/30) [92–100] | 100.0% (30/30) [92–100] |
| Összes | (hibás nélkül) vs küszöb 95% | elérve (≥ 95%) | elérve (≥ 95%) |

## c) Kapuhiba-arány

| réteg | mérőszám | F3 (prompt v1) | F3V2 (prompt v2) |
|---|---|---|---|
| R1 | első próbára | 17.0% (17/100) | 12.0% (12/100) |
| R1 | végleg | 1.0% (1/100) | 0.0% (0/100) |
| R2 | első próbára | 0.0% (0/25) | 0.0% (0/25) |
| R2 | végleg | 0.0% (0/25) | 0.0% (0/25) |
| R3 | első próbára | 20.0% (5/25) | 8.0% (2/25) |
| R3 | végleg | 0.0% (0/25) | 0.0% (0/25) |
| R4 | első próbára | 16.0% (8/50) | 10.0% (5/50) |
| R4 | végleg | 0.0% (0/50) | 0.0% (0/50) |
| Összes | első próbára | 15.0% (30/200) | 9.5% (19/200) |
| Összes | végleg | 0.5% (1/200) | 0.0% (0/200) |

## d) Költség (futásnapló; a gondolkodási token külön oszlop)

| futás | hívás (ebből újrakérés) | bemeneti token | kimeneti token | gondolkodási token (napló) | gondolkodási token (jsonl nyers usage) | cost USD | cost-forrás | gondolkodási mód | prompt sha256[:12] |
|---|---|---|---|---|---|---|---|---|---|
| F3 (prompt v1) | 27 (7) | 196498 | 30770 | 0 | n.é. (a futás nem tárolta a nyers usage-ot) | 0.257251 | openrouter | kotelezo_effort=minimal | 053993cdccbf |
| F3V2 (prompt v2) | 26 (6) | 216985 | 29470 | 0 | 0 | 0.256731 | openrouter | kotelezo_effort=minimal | a9f0f07c67b9 |

## e) Hibatípusok kapupont szerint (hibás versek száma)

| kapupont | F3 (prompt v1) első próbára | F3 (prompt v1) végleg | F3V2 (prompt v2) első próbára | F3V2 (prompt v2) végleg |
|---|---|---|---|---|
| 1 | 7.5% (15/200) | 0.0% (0/200) | 2.5% (5/200) | 0.0% (0/200) |
| 1-json | 5.0% (10/200) | 0.0% (0/200) | 5.0% (10/200) | 0.0% (0/200) |
| 2 | 0.5% (1/200) | 0.0% (0/200) | 0.0% (0/200) | 0.0% (0/200) |
| 3 | 0.5% (1/200) | 0.0% (0/200) | 0.5% (1/200) | 0.0% (0/200) |
| 4 | 2.5% (5/200) | 0.5% (1/200) | 2.0% (4/200) | 0.0% (0/200) |

