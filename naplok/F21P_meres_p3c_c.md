# F21P_meres_p3c_c.md — P4 a regressziós mérésre: a C (F3V3) egyedül, a v2-es C-futásokkal (a Sonnet nélkül)

<!-- GENERÁLT: eszkozok/karoli_strong/meres_p3c.py --csak-c | scope=P4 a regressziós mérésre, a C (F3V3, prompt_v3) EGYEDÜL (a SONNETV3 nem futott: a Sonnet és a Sonnet+C pár nincs adat); a v2-es C-futások (F3V2, F3V2B) és az F3V3 az arany v3-ra és az arany v2-re is; F8V3 (C KJV-támponttal) tájékoztatásul; 200 verses minta; arany v3 (60 vers, sha256 acdeb55f969c96fe) és arany v2 (60 vers, sha256 06a00738f7fd0449) | forras=f21p/valaszok/{F3V3,F3V2,F3V2B,F8V3}.jsonl, arany_opus_v3.jsonl és arany_opus_v2.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, f21p/koltseg_vetites_p3c_c.tsv, konkordancia/KJV_Strongs_teljes.tsv, konkordancia/KJV_Strongs_*.tsv | ts=2026-10-01T07:46:16+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

Kizárólag szkriptkimenet (meres_p3c.py --csak-c). A SONNETV3 még nem futott: a Sonnet egyedül és a Sonnet + C pár sorai **nincs adat (SONNETV3 nem futott)**; a teljes P4 a Sonnet-adat megérkezése után ugyanezzel a szkripttel fut (--csak-c nélkül, az eredeti f21p/meres_p3c_eredmeny.tsv és naplok/F21P_meres_p3c.md néven). A C egymodelles összeállítás: PD6 szerint **nincs minősítése** (nem „megfelelt / nem felel meg”), csak mért számok és a küszöbhöz viszonyítás; az (1) és az (5) feltétel n.é. A futások beállítása: a C `kotelezo_effort=minimal` (gondolkodással), temperature 0; az F3V2/F3V2B a prompt_v2-vel, az F3V3 és az F8V3 a prompt_v3-mal. Cellaforma: érték (számláló/nevező). A mérés az arany **v3** változatára megy (60 vers, sha256 ellenőrizve); a v2-es összevetéshez az arany **v2** is (60 vers, sha256 ellenőrizve).

## a) A C (F3V3) egyedül: az öt rögzített feltétel rétegenként (arany v3)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V3) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V3) | pontossag_osszes (tajekoztato, PD6) | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 94.4% (306/324) | 95.3% (1009/1059) |
| C (F3V3) | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.5% (306/314) | 96.3% (1009/1048) |
| C (F3V3) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V3) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V3) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V3) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |

### Küszöb-viszony (PD6: nem minősítés)

| feltétel | réteg | érték | megjegyzés |
|---|---|---|---|
| f1_magas_pontossag_98 | R1 | n.é. | egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): 96.4% (296/307) |
| f2_lefedettseg_95 | R1 | 93.4% (296/317) | küszöb ≥ 95%: a küszöbön kívül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (MÉRT, kizárás nélkül) | R1 | 93.8% (30/32) | küszöb ≥ 95%: a küszöbön kívül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül) | R1 | 96.8% (30/31) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6); a küszöb szempontjából nem számít (PD12) |
| f5_alacsony_arany_10 | R1 | n.é. | egymodelles (PD6): az alacsony szint nem értelmezhető |
| f1_magas_pontossag_98 | R2 | n.é. | egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): 96.2% (152/158) |
| f2_lefedettseg_95 | R2 | 100.0% (152/152) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (MÉRT, kizárás nélkül) | R2 | n.é. | nincs régi arany hármas a rétegben |
| f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül) | R2 | n.é. | nincs régi arany hármas a rétegben |
| f5_alacsony_arany_10 | R2 | n.é. | egymodelles (PD6): az alacsony szint nem értelmezhető |
| f1_magas_pontossag_98 | R3 | n.é. | egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): 94.4% (255/270) |
| f2_lefedettseg_95 | R3 | 96.2% (255/265) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (MÉRT, kizárás nélkül) | R3 | n.é. | nincs régi arany hármas a rétegben |
| f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül) | R3 | n.é. | nincs régi arany hármas a rétegben |
| f5_alacsony_arany_10 | R3 | n.é. | egymodelles (PD6): az alacsony szint nem értelmezhető |
| f1_magas_pontossag_98 | R4 | n.é. | egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): 94.4% (306/324) |
| f2_lefedettseg_95 | R4 | 97.5% (306/314) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (MÉRT, kizárás nélkül) | R4 | n.é. | nincs régi arany hármas a rétegben |
| f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül) | R4 | n.é. | nincs régi arany hármas a rétegben |
| f5_alacsony_arany_10 | R4 | n.é. | egymodelles (PD6): az alacsony szint nem értelmezhető |
| f1_magas_pontossag_98 | Összes | n.é. | egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): 95.3% (1009/1059) |
| f2_lefedettseg_95 | Összes | 96.3% (1009/1048) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (MÉRT, kizárás nélkül) | Összes | 93.8% (30/32) | küszöb ≥ 95%: a küszöbön kívül (küszöb-viszony, nem minősítés; PD6) |
| f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül) | Összes | 96.8% (30/31) | küszöb ≥ 95%: a küszöbön belül (küszöb-viszony, nem minősítés; PD6); a küszöb szempontjából nem számít (PD12) |
| f5_alacsony_arany_10 | Összes | n.é. | egymodelles (PD6): az alacsony szint nem értelmezhető |
| f4_koltseg_felso90_60 | Összes | 46.62 | vetített teljes költség 42.49 USD [90%: 38.67–46.62]; küszöb: a felső szél ≤ 60 USD: a küszöbön belül (küszöb-viszony, nem minősítés; PD6) |
| minosites | Összes | nincs (egymodelles összeállítás, PD6) | a teljes futásra rétegenként sem mehet; csak mért számok és a küszöbhöz viszonyítás |

## b) A Sonnet egyedül és a Sonnet + C pár

| összeállítás | állapot |
|---|---|
| Sonnet (SONNETV3) | nincs adat (SONNETV3 nem futott) |
| Sonnet+C | nincs adat (SONNETV3 nem futott) |

## c) A C-futások egymás mellett, arany v3 (F3V2, F3V2B: prompt_v2; F3V3: prompt_v3; F8V3: prompt_v3 + KJV-támpont, tájékoztató)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V2) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2) | pontossag_osszes (tajekoztato, PD6) | 94.0% (299/318) | 95.0% (152/160) | 93.8% (258/275) | 91.4% (308/337) | 93.3% (1017/1090) |
| C (F3V2) | lefedettseg | 94.3% (299/317) | 100.0% (152/152) | 97.4% (258/265) | 98.1% (308/314) | 97.0% (1017/1048) |
| C (F3V2) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V2) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V2B) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2B) | pontossag_osszes (tajekoztato, PD6) | 93.8% (304/324) | 95.0% (151/159) | 93.6% (262/280) | 90.3% (306/339) | 92.8% (1023/1102) |
| C (F3V2B) | lefedettseg | 95.9% (304/317) | 99.3% (151/152) | 98.9% (262/265) | 97.5% (306/314) | 97.6% (1023/1048) |
| C (F3V2B) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V2B) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V3) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V3) | pontossag_osszes (tajekoztato, PD6) | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 94.4% (306/324) | 95.3% (1009/1059) |
| C (F3V3) | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.5% (306/314) | 96.3% (1009/1048) |
| C (F3V3) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V3) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C KJV-vel (F8V3, tájékoztató) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C KJV-vel (F8V3, tájékoztató) | pontossag_osszes (tajekoztato, PD6) | 94.6% (298/315) | 99.3% (151/152) | 95.8% (253/264) | 94.4% (303/321) | 95.5% (1005/1052) |
| C KJV-vel (F8V3, tájékoztató) | lefedettseg | 94.0% (298/317) | 99.3% (151/152) | 95.5% (253/265) | 96.5% (303/314) | 95.9% (1005/1048) |
| C KJV-vel (F8V3, tájékoztató) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C KJV-vel (F8V3, tájékoztató) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |

Az F8V3 oszlop tájékoztató (PD17): az **R4 „KJV nélkül, nem mérhető”** (a Károli ↔ KJV megfeleltetés az ÚSZ-t nem fedi, az R4-en a bemenet azonos az F3V3-éval); az R2 a zsoltár-eltolódás miatt gyenge (N-F21); a KJV a promptban: „nem igazolt, a javított táblával újramérhető”. Részletek: naplok/F21P_kjv_meres.md.

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C KJV-vel (F8V3, tájékoztató) | versek_kjv_sorral (teljes tábla) | 100.0% (100/100) | 96.0% (24/25) | 100.0% (25/25) | 0.0% (0/50) | 74.5% (149/200) |
| C KJV-vel (F8V3, tájékoztató) | jeloles | — | gyenge (zsoltár-eltolódás) | — | KJV nélkül, nem mérhető | nem igazolt, a javított táblával újramérhető |
| C (F3V3) | versek_kjv_sorral (régi tábla) | 100.0% (100/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 50.0% (100/200) |

## d) Ugyanez az arany v2-re (a v2-es futások saját aranya; az arany v2 → v3 hatás elválasztásához)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V2) × arany v2 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2) × arany v2 | pontossag_osszes (tajekoztato, PD6) | 94.0% (299/318) | 95.6% (153/160) | 94.2% (259/275) | 91.7% (309/337) | 93.6% (1020/1090) |
| C (F3V2) × arany v2 | lefedettseg | 94.3% (299/317) | 100.0% (153/153) | 97.4% (259/266) | 98.1% (309/315) | 97.1% (1020/1051) |
| C (F3V2B) × arany v2 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2B) × arany v2 | pontossag_osszes (tajekoztato, PD6) | 93.8% (304/324) | 95.6% (152/159) | 93.9% (263/280) | 90.3% (306/339) | 93.0% (1025/1102) |
| C (F3V2B) × arany v2 | lefedettseg | 95.9% (304/317) | 99.3% (152/153) | 98.9% (263/266) | 97.1% (306/315) | 97.5% (1025/1051) |
| C (F3V3) × arany v2 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V3) × arany v2 | pontossag_osszes (tajekoztato, PD6) | 96.4% (296/307) | 96.8% (153/158) | 94.4% (255/270) | 94.4% (306/324) | 95.4% (1010/1059) |
| C (F3V3) × arany v2 | lefedettseg | 93.4% (296/317) | 100.0% (153/153) | 95.9% (255/266) | 97.1% (306/315) | 96.1% (1010/1051) |

### Az arany v2 → v3 hatás azonos futás-kimeneten (determinisztikus)

| futás | réteg | mérőszám | arany v2 | arany v3 | Δ (v3 − v2) | számláló/nevező (v2 \| v3) |
|---|---|---|---|---|---|---|
| C (F3V3) | R1 | pontossag | 96.42% | 96.42% | +0.00 pp | 296/307 \| 296/307 |
| C (F3V3) | R1 | lefedettseg | 93.38% | 93.38% | +0.00 pp | 296/317 \| 296/317 |
| C (F3V3) | R2 | pontossag | 96.84% | 96.20% | -0.63 pp | 153/158 \| 152/158 |
| C (F3V3) | R2 | lefedettseg | 100.00% | 100.00% | +0.00 pp | 153/153 \| 152/152 |
| C (F3V3) | R3 | pontossag | 94.44% | 94.44% | +0.00 pp | 255/270 \| 255/270 |
| C (F3V3) | R3 | lefedettseg | 95.86% | 96.23% | +0.36 pp | 255/266 \| 255/265 |
| C (F3V3) | R4 | pontossag | 94.44% | 94.44% | +0.00 pp | 306/324 \| 306/324 |
| C (F3V3) | R4 | lefedettseg | 97.14% | 97.45% | +0.31 pp | 306/315 \| 306/314 |
| C (F3V3) | Összes | pontossag | 95.37% | 95.28% | -0.09 pp | 1010/1059 \| 1009/1059 |
| C (F3V3) | Összes | lefedettseg | 96.10% | 96.28% | +0.18 pp | 1010/1051 \| 1009/1048 |
| C (F3V2) | R1 | pontossag | 94.03% | 94.03% | +0.00 pp | 299/318 \| 299/318 |
| C (F3V2) | R1 | lefedettseg | 94.32% | 94.32% | +0.00 pp | 299/317 \| 299/317 |
| C (F3V2) | R2 | pontossag | 95.63% | 95.00% | -0.63 pp | 153/160 \| 152/160 |
| C (F3V2) | R2 | lefedettseg | 100.00% | 100.00% | +0.00 pp | 153/153 \| 152/152 |
| C (F3V2) | R3 | pontossag | 94.18% | 93.82% | -0.36 pp | 259/275 \| 258/275 |
| C (F3V2) | R3 | lefedettseg | 97.37% | 97.36% | -0.01 pp | 259/266 \| 258/265 |
| C (F3V2) | R4 | pontossag | 91.69% | 91.39% | -0.30 pp | 309/337 \| 308/337 |
| C (F3V2) | R4 | lefedettseg | 98.10% | 98.09% | -0.01 pp | 309/315 \| 308/314 |
| C (F3V2) | Összes | pontossag | 93.58% | 93.30% | -0.28 pp | 1020/1090 \| 1017/1090 |
| C (F3V2) | Összes | lefedettseg | 97.05% | 97.04% | -0.01 pp | 1020/1051 \| 1017/1048 |
| C (F3V2B) | R1 | pontossag | 93.83% | 93.83% | +0.00 pp | 304/324 \| 304/324 |
| C (F3V2B) | R1 | lefedettseg | 95.90% | 95.90% | +0.00 pp | 304/317 \| 304/317 |
| C (F3V2B) | R2 | pontossag | 95.60% | 94.97% | -0.63 pp | 152/159 \| 151/159 |
| C (F3V2B) | R2 | lefedettseg | 99.35% | 99.34% | -0.00 pp | 152/153 \| 151/152 |
| C (F3V2B) | R3 | pontossag | 93.93% | 93.57% | -0.36 pp | 263/280 \| 262/280 |
| C (F3V2B) | R3 | lefedettseg | 98.87% | 98.87% | -0.00 pp | 263/266 \| 262/265 |
| C (F3V2B) | R4 | pontossag | 90.27% | 90.27% | +0.00 pp | 306/339 \| 306/339 |
| C (F3V2B) | R4 | lefedettseg | 97.14% | 97.45% | +0.31 pp | 306/315 \| 306/314 |
| C (F3V2B) | Összes | pontossag | 93.01% | 92.83% | -0.18 pp | 1025/1102 \| 1023/1102 |
| C (F3V2B) | Összes | lefedettseg | 97.53% | 97.61% | +0.09 pp | 1025/1051 \| 1023/1048 |

A két arany eltérő linkjei: 3 — Jób 33:13 (4, 5) csak v2; Ez 39:13 (18, 16) csak v2; Mt 21:4 (3, 5) csak v2

## e) Kapuhiba első próbára és végleg; hibatípusok kapupont szerint (hibás versek a 200-ból)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V2) | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 8.0% (2/25) | 10.0% (5/50) | 9.5% (19/200) |
| C (F3V2) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V2B) | elso_probara | 21.0% (21/100) | 20.0% (5/25) | 4.0% (1/25) | 2.0% (1/50) | 14.0% (28/200) |
| C (F3V2B) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V3) | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 40.0% (10/25) | 16.0% (8/50) | 15.0% (30/200) |
| C (F3V3) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 0.0% (0/50) | 1.0% (2/200) |
| C KJV-vel (F8V3, tájékoztató) | elso_probara | 10.0% (10/100) | 4.0% (1/25) | 36.0% (9/25) | 0.0% (0/50) | 10.0% (20/200) |
| C KJV-vel (F8V3, tájékoztató) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |

| futás | kapupont | hibás versek (n a 200) |
|---|---|---|
| C (F3V2) | kapupont_1_elso | 5/200 |
| C (F3V2) | kapupont_1_vegleg | 0/200 |
| C (F3V2) | kapupont_1-json_elso | 10/200 |
| C (F3V2) | kapupont_1-json_vegleg | 0/200 |
| C (F3V2) | kapupont_3_elso | 1/200 |
| C (F3V2) | kapupont_3_vegleg | 0/200 |
| C (F3V2) | kapupont_4_elso | 4/200 |
| C (F3V2) | kapupont_4_vegleg | 0/200 |
| C (F3V2B) | kapupont_1_elso | 6/200 |
| C (F3V2B) | kapupont_1_vegleg | 0/200 |
| C (F3V2B) | kapupont_1-json_elso | 20/200 |
| C (F3V2B) | kapupont_1-json_vegleg | 0/200 |
| C (F3V2B) | kapupont_3_elso | 1/200 |
| C (F3V2B) | kapupont_3_vegleg | 0/200 |
| C (F3V2B) | kapupont_4_elso | 1/200 |
| C (F3V2B) | kapupont_4_vegleg | 0/200 |
| C (F3V3) | kapupont_1_elso | 7/200 |
| C (F3V3) | kapupont_1_vegleg | 0/200 |
| C (F3V3) | kapupont_1-json_elso | 20/200 |
| C (F3V3) | kapupont_1-json_vegleg | 0/200 |
| C (F3V3) | kapupont_2_elso | 1/200 |
| C (F3V3) | kapupont_2_vegleg | 0/200 |
| C (F3V3) | kapupont_3_elso | 1/200 |
| C (F3V3) | kapupont_3_vegleg | 0/200 |
| C (F3V3) | kapupont_4_elso | 2/200 |
| C (F3V3) | kapupont_4_vegleg | 2/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_1_elso | 9/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_1_vegleg | 0/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_1-json_elso | 10/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_1-json_vegleg | 0/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_3_elso | 1/200 |
| C KJV-vel (F8V3, tájékoztató) | kapupont_3_vegleg | 0/200 |

| futás | keresztellenőrzés (első próbás hibás versek) |
|---|---|
| C (F3V3) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (30) = napló kapuhiba_db(probalkozas=1) összeg (30): EGYEZIK |
| C (F3V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (19) = napló kapuhiba_db(probalkozas=1) összeg (19): EGYEZIK |
| C (F3V2B) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (28) = napló kapuhiba_db(probalkozas=1) összeg (28): EGYEZIK |
| C KJV-vel (F8V3, tájékoztató) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (20) = napló kapuhiba_db(probalkozas=1) összeg (20): EGYEZIK |

| futás | mentett válaszok újraellenőrzése (hibák) |
|---|---|
| C (F3V3) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C (F3V2) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C (F3V2B) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C KJV-vel (F8V3, tájékoztató) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |

| futás | első próbára kapuhibás versek | véglegesen kapuhibás versek |
|---|---|---|
| C (F3V2) | 19: 1Móz 15:12, 1Móz 24:27, 1Móz 28:8, 1Móz 30:7, 1Móz 31:18, 1Móz 32:19, 1Móz 38:22, 1Móz 41:19, 1Móz 45:24, 1Móz 49:25, 1Móz 50:2, 2Móz 21:26, Ézs 48:5, Ez 46:12, Mk 9:36, Mk 13:21, Mk 14:44, Luk 1:75, Luk 9:27 | 0: — |
| C (F3V2B) | 28: 1Móz 2:2, 1Móz 24:27, 1Móz 28:8, 1Móz 30:7, 1Móz 31:18, 1Móz 32:19, 1Móz 38:22, 1Móz 41:19, 1Móz 45:24, 1Móz 49:25, 1Móz 50:2, 2Móz 32:5, 2Móz 37:12, 2Móz 38:8, 2Móz 38:21, 2Móz 39:23, 2Móz 39:26, 2Móz 39:31, 2Móz 39:33, 2Móz 40:14, 2Móz 40:36, Jób 34:28, Zsolt 16:11, Zsolt 18:1, Zsolt 22:32, Zsolt 59:8, Ézs 48:5, Mk 2:10 | 0: — |
| C (F3V3) | 30: 1Móz 13:14, 1Móz 24:27, 1Móz 28:8, 1Móz 30:7, 1Móz 31:18, 1Móz 32:19, 1Móz 38:22, 1Móz 41:19, 1Móz 45:24, 1Móz 49:25, 1Móz 50:2, 2Móz 26:13, Ézs 38:15, Ézs 48:5, Ézs 55:12, Ézs 63:10, Jer 6:10, Jer 8:19, Jer 9:19, Jer 16:3, Jer 32:27, Jer 44:16, Mt 5:34, Mt 6:31, Mt 11:18, Mt 21:4, Mt 23:31, Mt 27:18, Mk 2:23, Zsid 9:6 | 2: Ézs 48:5 (R3), Jer 16:3 (R3) |
| C KJV-vel (F8V3, tájékoztató) | 20: 1Móz 24:27, 1Móz 28:8, 1Móz 30:7, 1Móz 31:18, 1Móz 32:19, 1Móz 38:22, 1Móz 41:19, 1Móz 45:24, 1Móz 49:25, 1Móz 50:2, Zsolt 18:3, Jer 46:21, Ez 11:3, Ez 16:57, Ez 22:25, Ez 30:5, Ez 33:31, Ez 39:13, Ez 41:2, Ez 46:12 | 0: — |

## f) Költség és beállítás futásonként (a futásnaplóból)

| futás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| C (F3V3) | hivasok | 26 | próbálkozás=1: 20, próbálkozás=2: 6 |
| C (F3V3) | bemeneti_token | 226300 |  |
| C (F3V3) | kimeneti_token | 30719 | a completion_tokens (a gondolkodási token benne van, ha a modell jelenti) |
| C (F3V3) | koltseg_usd | 0.260136 | koltseg_forras: openrouter |
| C (F3V3) | gondolkodas_mod | kotelezo_effort=minimal | a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva |
| C (F3V3) | prompt_sha256_12 | 84f12ca7aafb |  |
| C (F3V2) | hivasok | 26 | próbálkozás=1: 20, próbálkozás=2: 6 |
| C (F3V2) | bemeneti_token | 216985 |  |
| C (F3V2) | kimeneti_token | 29470 | a completion_tokens (a gondolkodási token benne van, ha a modell jelenti) |
| C (F3V2) | koltseg_usd | 0.256731 | koltseg_forras: openrouter |
| C (F3V2) | gondolkodas_mod | kotelezo_effort=minimal | a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva |
| C (F3V2) | prompt_sha256_12 | a9f0f07c67b9 |  |
| C (F3V2B) | hivasok | 26 | próbálkozás=1: 20, próbálkozás=2: 6 |
| C (F3V2B) | bemeneti_token | 212738 |  |
| C (F3V2B) | kimeneti_token | 30888 | a completion_tokens (a gondolkodási token benne van, ha a modell jelenti) |
| C (F3V2B) | koltseg_usd | 0.256110 | koltseg_forras: openrouter |
| C (F3V2B) | gondolkodas_mod | kotelezo_effort=minimal | a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva |
| C (F3V2B) | prompt_sha256_12 | a9f0f07c67b9 |  |
| C KJV-vel (F8V3, tájékoztató) | hivasok | 23 | próbálkozás=1: 20, próbálkozás=2: 3 |
| C KJV-vel (F8V3, tájékoztató) | bemeneti_token | 201000 |  |
| C KJV-vel (F8V3, tájékoztató) | kimeneti_token | 29793 | a completion_tokens (a gondolkodási token benne van, ha a modell jelenti) |
| C KJV-vel (F8V3, tájékoztató) | koltseg_usd | 0.262474 | koltseg_forras: openrouter |
| C KJV-vel (F8V3, tájékoztató) | gondolkodas_mod | kotelezo_effort=minimal | a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva |
| C KJV-vel (F8V3, tájékoztató) | prompt_sha256_12 | 84f12ca7aafb |  |

(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3c_c.tsv; 90%; a bootstrap egysége a köteg):

- C (F3V2): 42.03 USD [37.99–46.07]
- C (F3V2B): 42.03 USD [38.14–46.43]
- C (F3V3): 42.49 USD [38.67–46.62]

## g) A prompt_v2 → v3 hatás (F3V3 a két v2-futás átlagához képest), arany v3, és a futásközi ingadozás

Δ = F3V3 − a v2-futások átlaga, azonos aranyon (tehát az arany változása nincs benne); a 90%-os intervallum a versek bootstrapje (rétegenként rétegzett, 1000 újramintavétel, mag 20260930). Az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|, azonos prompt). „kívül”: |Δ| > az ingadozás ÉS az intervallum nem tartalmazza a 0-t (leíró jelölés, nem próba).

| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | \|F3V2B − F3V2\| | jelölés | n |
|---|---|---|---|---|---|---|---|---|
| R1 | pontossag | 93.93% | 96.42% | +2.49 pp | [-0.10; +4.49] | 0.20 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R1 | lefedettseg | 95.11% | 93.38% | -1.74 pp | [-3.83; +0.51] | 1.58 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R1 | kapuhiba_elso_probara | 16.50% | 12.00% | -4.50 pp | [-8.00; -0.50] | 9.00 pp | az ingadozáson belül / a 0-t tartalmazza | 100 |
| R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 100 |
| R2 | pontossag | 94.98% | 96.20% | +1.22 pp | [-0.75; +2.85] | 0.03 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R2 | lefedettseg | 99.67% | 100.00% | +0.33 pp | [+0.00; +0.94] | 0.66 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R2 | kapuhiba_elso_probara | 10.00% | 0.00% | -10.00 pp | [-16.00; -4.00] | 20.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R3 | pontossag | 93.69% | 94.44% | +0.75 pp | [-1.84; +3.50] | 0.25 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R3 | lefedettseg | 98.11% | 96.23% | -1.89 pp | [-3.71; -0.43] | 1.51 pp | kívül az ingadozáson | 10 |
| R3 | kapuhiba_elso_probara | 6.00% | 40.00% | +34.00 pp | [+18.00; +50.00] | 4.00 pp | kívül az ingadozáson | 25 |
| R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R4 | pontossag | 90.83% | 94.44% | +3.61 pp | [+1.66; +5.71] | 1.13 pp | kívül az ingadozáson | 20 |
| R4 | lefedettseg | 97.77% | 97.45% | -0.32 pp | [-1.58; +0.91] | 0.64 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R4 | kapuhiba_elso_probara | 6.00% | 16.00% | +10.00 pp | [+0.00; +20.00] | 8.00 pp | az ingadozáson belül / a 0-t tartalmazza | 50 |
| R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 50 |
| Összes | pontossag | 93.07% | 95.28% | +2.21 pp | [+1.01; +3.36] | 0.47 pp | kívül az ingadozáson | 60 |
| Összes | lefedettseg | 97.33% | 96.28% | -1.05 pp | [-1.88; -0.11] | 0.57 pp | kívül az ingadozáson | 60 |
| Összes | kapuhiba_elso_probara | 11.75% | 15.00% | +3.25 pp | [-0.50; +7.00] | 4.50 pp | az ingadozáson belül / a 0-t tartalmazza | 200 |
| Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 200 |


## h) A prompt_v2 → v3 hatás (F3V3 a két v2-futás átlagához képest), arany v2, és a futásközi ingadozás

Δ = F3V3 − a v2-futások átlaga, azonos aranyon (tehát az arany változása nincs benne); a 90%-os intervallum a versek bootstrapje (rétegenként rétegzett, 1000 újramintavétel, mag 20260930). Az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|, azonos prompt). „kívül”: |Δ| > az ingadozás ÉS az intervallum nem tartalmazza a 0-t (leíró jelölés, nem próba).

| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | \|F3V2B − F3V2\| | jelölés | n |
|---|---|---|---|---|---|---|---|---|
| R1 | pontossag | 93.93% | 96.42% | +2.49 pp | [-0.10; +4.49] | 0.20 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R1 | lefedettseg | 95.11% | 93.38% | -1.74 pp | [-3.83; +0.51] | 1.58 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R1 | kapuhiba_elso_probara | 16.50% | 12.00% | -4.50 pp | [-8.00; -0.50] | 9.00 pp | az ingadozáson belül / a 0-t tartalmazza | 100 |
| R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 100 |
| R2 | pontossag | 95.61% | 96.84% | +1.22 pp | [-0.76; +2.86] | 0.03 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R2 | lefedettseg | 99.67% | 100.00% | +0.33 pp | [+0.00; +0.93] | 0.65 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R2 | kapuhiba_elso_probara | 10.00% | 0.00% | -10.00 pp | [-16.00; -4.00] | 20.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R3 | pontossag | 94.06% | 94.44% | +0.39 pp | [-1.99; +2.61] | 0.25 pp | az ingadozáson belül / a 0-t tartalmazza | 10 |
| R3 | lefedettseg | 98.12% | 95.86% | -2.26 pp | [-4.11; -0.89] | 1.50 pp | kívül az ingadozáson | 10 |
| R3 | kapuhiba_elso_probara | 6.00% | 40.00% | +34.00 pp | [+18.00; +50.00] | 4.00 pp | kívül az ingadozáson | 25 |
| R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 25 |
| R4 | pontossag | 90.98% | 94.44% | +3.47 pp | [+1.57; +5.53] | 1.43 pp | kívül az ingadozáson | 20 |
| R4 | lefedettseg | 97.62% | 97.14% | -0.48 pp | [-1.77; +0.80] | 0.95 pp | az ingadozáson belül / a 0-t tartalmazza | 20 |
| R4 | kapuhiba_elso_probara | 6.00% | 16.00% | +10.00 pp | [+0.00; +20.00] | 8.00 pp | az ingadozáson belül / a 0-t tartalmazza | 50 |
| R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 50 |
| Összes | pontossag | 93.30% | 95.37% | +2.08 pp | [+0.90; +3.18] | 0.57 pp | kívül az ingadozáson | 60 |
| Összes | lefedettseg | 97.29% | 96.10% | -1.19 pp | [-2.00; -0.26] | 0.48 pp | kívül az ingadozáson | 60 |
| Összes | kapuhiba_elso_probara | 11.75% | 15.00% | +3.25 pp | [-0.50; +7.00] | 4.50 pp | az ingadozáson belül / a 0-t tartalmazza | 200 |
| Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza | 200 |

## i) Páronkénti összevetések (a „[arany v2]” utótag nélkül az arany v3-ra; az F8V3 − F3V3 tájékoztató)

| összevetés | réteg | mérőszám | ref | cél | Δ | Δ 90% | \|Δ\| 95. percentilis | n |
|---|---|---|---|---|---|---|---|---|
| F3V3 − F3V2 | R1 | pontossag | 94.03% | 96.42% | +2.39 pp | [-0.60; +4.84] | 4.84 pp | 20 |
| F3V3 − F3V2 | R1 | lefedettseg | 94.32% | 93.38% | -0.95 pp | [-3.35; +1.40] | 3.37 pp | 20 |
| F3V3 − F3V2 | R1 | kapuhiba_elso_probara | 12.00% | 12.00% | +0.00 pp | [-3.00; +4.00] | 4.00 pp | 100 |
| F3V3 − F3V2 | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − F3V2 | R2 | pontossag | 95.00% | 96.20% | +1.20 pp | [+0.00; +2.30] | 2.30 pp | 10 |
| F3V3 − F3V2 | R2 | lefedettseg | 100.00% | 100.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 10 |
| F3V3 − F3V2 | R2 | kapuhiba_elso_probara | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2 | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2 | R3 | pontossag | 93.82% | 94.44% | +0.63 pp | [-2.57; +3.53] | 3.88 pp | 10 |
| F3V3 − F3V2 | R3 | lefedettseg | 97.36% | 96.23% | -1.13 pp | [-2.67; +0.00] | 2.67 pp | 10 |
| F3V3 − F3V2 | R3 | kapuhiba_elso_probara | 8.00% | 40.00% | +32.00 pp | [+12.00; +48.00] | 48.00 pp | 25 |
| F3V3 − F3V2 | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − F3V2 | R4 | pontossag | 91.39% | 94.44% | +3.05 pp | [+1.09; +5.02] | 5.02 pp | 20 |
| F3V3 − F3V2 | R4 | lefedettseg | 98.09% | 97.45% | -0.64 pp | [-2.04; +0.84] | 2.05 pp | 20 |
| F3V3 − F3V2 | R4 | kapuhiba_elso_probara | 10.00% | 16.00% | +6.00 pp | [-6.00; +18.00] | 18.00 pp | 50 |
| F3V3 − F3V2 | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − F3V2 | Összes | pontossag | 93.30% | 95.28% | +1.98 pp | [+0.63; +3.25] | 3.25 pp | 60 |
| F3V3 − F3V2 | Összes | lefedettseg | 97.04% | 96.28% | -0.76 pp | [-1.67; +0.10] | 1.67 pp | 60 |
| F3V3 − F3V2 | Összes | kapuhiba_elso_probara | 9.50% | 15.00% | +5.50 pp | [+1.50; +9.50] | 9.50 pp | 200 |
| F3V3 − F3V2 | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V3 − F3V2B | R1 | pontossag | 93.83% | 96.42% | +2.59 pp | [+0.13; +4.89] | 4.89 pp | 20 |
| F3V3 − F3V2B | R1 | lefedettseg | 95.90% | 93.38% | -2.52 pp | [-5.52; +0.63] | 5.52 pp | 20 |
| F3V3 − F3V2B | R1 | kapuhiba_elso_probara | 21.00% | 12.00% | -9.00 pp | [-15.00; -3.00] | 15.00 pp | 100 |
| F3V3 − F3V2B | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − F3V2B | R2 | pontossag | 94.97% | 96.20% | +1.23 pp | [-2.31; +3.96] | 4.00 pp | 10 |
| F3V3 − F3V2B | R2 | lefedettseg | 99.34% | 100.00% | +0.66 pp | [+0.00; +1.88] | 1.88 pp | 10 |
| F3V3 − F3V2B | R2 | kapuhiba_elso_probara | 20.00% | 0.00% | -20.00 pp | [-32.00; -8.00] | 32.00 pp | 25 |
| F3V3 − F3V2B | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2B | R3 | pontossag | 93.57% | 94.44% | +0.87 pp | [-1.38; +3.45] | 3.49 pp | 10 |
| F3V3 − F3V2B | R3 | lefedettseg | 98.87% | 96.23% | -2.64 pp | [-4.96; -0.77] | 4.96 pp | 10 |
| F3V3 − F3V2B | R3 | kapuhiba_elso_probara | 4.00% | 40.00% | +36.00 pp | [+20.00; +52.00] | 52.00 pp | 25 |
| F3V3 − F3V2B | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − F3V2B | R4 | pontossag | 90.27% | 94.44% | +4.18 pp | [+1.77; +6.73] | 6.73 pp | 20 |
| F3V3 − F3V2B | R4 | lefedettseg | 97.45% | 97.45% | +0.00 pp | [-1.29; +1.32] | 1.54 pp | 20 |
| F3V3 − F3V2B | R4 | kapuhiba_elso_probara | 2.00% | 16.00% | +14.00 pp | [+6.00; +24.00] | 24.00 pp | 50 |
| F3V3 − F3V2B | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − F3V2B | Összes | pontossag | 92.83% | 95.28% | +2.45 pp | [+1.17; +3.66] | 3.66 pp | 60 |
| F3V3 − F3V2B | Összes | lefedettseg | 97.61% | 96.28% | -1.34 pp | [-2.47; -0.19] | 2.47 pp | 60 |
| F3V3 − F3V2B | Összes | kapuhiba_elso_probara | 14.00% | 15.00% | +1.00 pp | [-3.50; +5.50] | 5.50 pp | 200 |
| F3V3 − F3V2B | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V3 − átlag(F3V2, F3V2B) | R1 | pontossag | 93.93% | 96.42% | +2.49 pp | [-0.10; +4.49] | 4.49 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) | R1 | lefedettseg | 95.11% | 93.38% | -1.74 pp | [-3.83; +0.51] | 3.83 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) | R1 | kapuhiba_elso_probara | 16.50% | 12.00% | -4.50 pp | [-8.00; -0.50] | 8.00 pp | 100 |
| F3V3 − átlag(F3V2, F3V2B) | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − átlag(F3V2, F3V2B) | R2 | pontossag | 94.98% | 96.20% | +1.22 pp | [-0.75; +2.85] | 2.85 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) | R2 | lefedettseg | 99.67% | 100.00% | +0.33 pp | [+0.00; +0.94] | 0.94 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) | R2 | kapuhiba_elso_probara | 10.00% | 0.00% | -10.00 pp | [-16.00; -4.00] | 16.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) | R3 | pontossag | 93.69% | 94.44% | +0.75 pp | [-1.84; +3.50] | 3.57 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) | R3 | lefedettseg | 98.11% | 96.23% | -1.89 pp | [-3.71; -0.43] | 3.71 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) | R3 | kapuhiba_elso_probara | 6.00% | 40.00% | +34.00 pp | [+18.00; +50.00] | 50.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) | R4 | pontossag | 90.83% | 94.44% | +3.61 pp | [+1.66; +5.71] | 5.71 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) | R4 | lefedettseg | 97.77% | 97.45% | -0.32 pp | [-1.58; +0.91] | 1.62 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) | R4 | kapuhiba_elso_probara | 6.00% | 16.00% | +10.00 pp | [+0.00; +20.00] | 20.00 pp | 50 |
| F3V3 − átlag(F3V2, F3V2B) | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − átlag(F3V2, F3V2B) | Összes | pontossag | 93.07% | 95.28% | +2.21 pp | [+1.01; +3.36] | 3.36 pp | 60 |
| F3V3 − átlag(F3V2, F3V2B) | Összes | lefedettseg | 97.33% | 96.28% | -1.05 pp | [-1.88; -0.11] | 1.88 pp | 60 |
| F3V3 − átlag(F3V2, F3V2B) | Összes | kapuhiba_elso_probara | 11.75% | 15.00% | +3.25 pp | [-0.50; +7.00] | 7.00 pp | 200 |
| F3V3 − átlag(F3V2, F3V2B) | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V2B − F3V2 (ingadozás) | R1 | pontossag | 94.03% | 93.83% | -0.20 pp | [-2.46; +1.88] | 2.61 pp | 20 |
| F3V2B − F3V2 (ingadozás) | R1 | lefedettseg | 94.32% | 95.90% | +1.58 pp | [-1.88; +4.59] | 4.65 pp | 20 |
| F3V2B − F3V2 (ingadozás) | R1 | kapuhiba_elso_probara | 12.00% | 21.00% | +9.00 pp | [+3.00; +15.00] | 15.00 pp | 100 |
| F3V2B − F3V2 (ingadozás) | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V2B − F3V2 (ingadozás) | R2 | pontossag | 95.00% | 94.97% | -0.03 pp | [-2.55; +3.56] | 3.60 pp | 10 |
| F3V2B − F3V2 (ingadozás) | R2 | lefedettseg | 100.00% | 99.34% | -0.66 pp | [-1.88; +0.00] | 1.88 pp | 10 |
| F3V2B − F3V2 (ingadozás) | R2 | kapuhiba_elso_probara | 0.00% | 20.00% | +20.00 pp | [+8.00; +32.00] | 32.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) | R3 | pontossag | 93.82% | 93.57% | -0.25 pp | [-1.86; +1.06] | 1.87 pp | 10 |
| F3V2B − F3V2 (ingadozás) | R3 | lefedettseg | 97.36% | 98.87% | +1.51 pp | [+0.34; +2.89] | 2.89 pp | 10 |
| F3V2B − F3V2 (ingadozás) | R3 | kapuhiba_elso_probara | 8.00% | 4.00% | -4.00 pp | [-12.00; +0.00] | 12.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) | R3 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) | R4 | pontossag | 91.39% | 90.27% | -1.13 pp | [-3.02; +0.84] | 3.02 pp | 20 |
| F3V2B − F3V2 (ingadozás) | R4 | lefedettseg | 98.09% | 97.45% | -0.64 pp | [-1.67; +0.32] | 1.67 pp | 20 |
| F3V2B − F3V2 (ingadozás) | R4 | kapuhiba_elso_probara | 10.00% | 2.00% | -8.00 pp | [-16.00; +0.00] | 16.00 pp | 50 |
| F3V2B − F3V2 (ingadozás) | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V2B − F3V2 (ingadozás) | Összes | pontossag | 93.30% | 92.83% | -0.47 pp | [-1.51; +0.60] | 1.52 pp | 60 |
| F3V2B − F3V2 (ingadozás) | Összes | lefedettseg | 97.04% | 97.61% | +0.57 pp | [-0.54; +1.64] | 1.64 pp | 60 |
| F3V2B − F3V2 (ingadozás) | Összes | kapuhiba_elso_probara | 9.50% | 14.00% | +4.50 pp | [+0.50; +8.50] | 8.50 pp | 200 |
| F3V2B − F3V2 (ingadozás) | Összes | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 200 |
| F8V3 − F3V3 (KJV, tájékoztató) | R1 | pontossag | 96.42% | 94.60% | -1.81 pp | [-4.19; +0.90] | 4.19 pp | 20 |
| F8V3 − F3V3 (KJV, tájékoztató) | R1 | lefedettseg | 93.38% | 94.01% | +0.63 pp | [-0.70; +2.20] | 2.20 pp | 20 |
| F8V3 − F3V3 (KJV, tájékoztató) | R1 | kapuhiba_elso_probara | 12.00% | 10.00% | -2.00 pp | [-5.00; +0.00] | 5.00 pp | 100 |
| F8V3 − F3V3 (KJV, tájékoztató) | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F8V3 − F3V3 (KJV, tájékoztató) | R2 | pontossag | 96.20% | 99.34% | +3.14 pp | [+1.24; +5.00] | 5.00 pp | 10 |
| F8V3 − F3V3 (KJV, tájékoztató) | R2 | lefedettseg | 100.00% | 99.34% | -0.66 pp | [-1.61; +0.00] | 1.61 pp | 10 |
| F8V3 − F3V3 (KJV, tájékoztató) | R2 | kapuhiba_elso_probara | 0.00% | 4.00% | +4.00 pp | [+0.00; +12.00] | 12.00 pp | 25 |
| F8V3 − F3V3 (KJV, tájékoztató) | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F8V3 − F3V3 (KJV, tájékoztató) | R3 | pontossag | 94.44% | 95.83% | +1.39 pp | [-0.45; +3.56] | 3.56 pp | 10 |
| F8V3 − F3V3 (KJV, tájékoztató) | R3 | lefedettseg | 96.23% | 95.47% | -0.75 pp | [-2.46; +1.53] | 2.59 pp | 10 |
| F8V3 − F3V3 (KJV, tájékoztató) | R3 | kapuhiba_elso_probara | 40.00% | 36.00% | -4.00 pp | [-32.00; +24.00] | 36.00 pp | 25 |
| F8V3 − F3V3 (KJV, tájékoztató) | R3 | kapuhiba_vegleg | 8.00% | 0.00% | -8.00 pp | [-16.00; +0.00] | 16.00 pp | 25 |
| F8V3 − F3V3 (KJV, tájékoztató) | R4 | pontossag | 94.44% | 94.39% | -0.05 pp | [-2.13; +1.56] | 2.15 pp | 20 |
| F8V3 − F3V3 (KJV, tájékoztató) | R4 | lefedettseg | 97.45% | 96.50% | -0.96 pp | [-1.74; -0.29] | 1.74 pp | 20 |
| F8V3 − F3V3 (KJV, tájékoztató) | R4 | kapuhiba_elso_probara | 16.00% | 0.00% | -16.00 pp | [-24.00; -8.00] | 24.00 pp | 50 |
| F8V3 − F3V3 (KJV, tájékoztató) | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F8V3 − F3V3 (KJV, tájékoztató) | Összes | pontossag | 95.28% | 95.53% | +0.25 pp | [-0.84; +1.31] | 1.34 pp | 60 |
| F8V3 − F3V3 (KJV, tájékoztató) | Összes | lefedettseg | 96.28% | 95.90% | -0.38 pp | [-1.13; +0.40] | 1.13 pp | 60 |
| F8V3 − F3V3 (KJV, tájékoztató) | Összes | kapuhiba_elso_probara | 15.00% | 10.00% | -5.00 pp | [-9.50; -1.00] | 9.50 pp | 200 |
| F8V3 − F3V3 (KJV, tájékoztató) | Összes | kapuhiba_vegleg | 1.00% | 0.00% | -1.00 pp | [-2.00; +0.00] | 2.00 pp | 200 |
| F3V3 − F3V2 [arany v2] | R1 | pontossag | 94.03% | 96.42% | +2.39 pp | [-0.60; +4.84] | 4.84 pp | 20 |
| F3V3 − F3V2 [arany v2] | R1 | lefedettseg | 94.32% | 93.38% | -0.95 pp | [-3.35; +1.40] | 3.37 pp | 20 |
| F3V3 − F3V2 [arany v2] | R1 | kapuhiba_elso_probara | 12.00% | 12.00% | +0.00 pp | [-3.00; +4.00] | 4.00 pp | 100 |
| F3V3 − F3V2 [arany v2] | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − F3V2 [arany v2] | R2 | pontossag | 95.63% | 96.84% | +1.21 pp | [+0.00; +2.31] | 2.31 pp | 10 |
| F3V3 − F3V2 [arany v2] | R2 | lefedettseg | 100.00% | 100.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 10 |
| F3V3 − F3V2 [arany v2] | R2 | kapuhiba_elso_probara | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2 [arany v2] | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2 [arany v2] | R3 | pontossag | 94.18% | 94.44% | +0.26 pp | [-2.86; +2.76] | 3.26 pp | 10 |
| F3V3 − F3V2 [arany v2] | R3 | lefedettseg | 97.37% | 95.86% | -1.50 pp | [-3.08; -0.34] | 3.08 pp | 10 |
| F3V3 − F3V2 [arany v2] | R3 | kapuhiba_elso_probara | 8.00% | 40.00% | +32.00 pp | [+12.00; +48.00] | 48.00 pp | 25 |
| F3V3 − F3V2 [arany v2] | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − F3V2 [arany v2] | R4 | pontossag | 91.69% | 94.44% | +2.75 pp | [+0.75; +4.78] | 4.78 pp | 20 |
| F3V3 − F3V2 [arany v2] | R4 | lefedettseg | 98.10% | 97.14% | -0.95 pp | [-2.38; +0.57] | 2.40 pp | 20 |
| F3V3 − F3V2 [arany v2] | R4 | kapuhiba_elso_probara | 10.00% | 16.00% | +6.00 pp | [-6.00; +18.00] | 18.00 pp | 50 |
| F3V3 − F3V2 [arany v2] | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − F3V2 [arany v2] | Összes | pontossag | 93.58% | 95.37% | +1.80 pp | [+0.46; +3.02] | 3.02 pp | 60 |
| F3V3 − F3V2 [arany v2] | Összes | lefedettseg | 97.05% | 96.10% | -0.95 pp | [-1.82; -0.09] | 1.82 pp | 60 |
| F3V3 − F3V2 [arany v2] | Összes | kapuhiba_elso_probara | 9.50% | 15.00% | +5.50 pp | [+1.50; +9.50] | 9.50 pp | 200 |
| F3V3 − F3V2 [arany v2] | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V3 − F3V2B [arany v2] | R1 | pontossag | 93.83% | 96.42% | +2.59 pp | [+0.13; +4.89] | 4.89 pp | 20 |
| F3V3 − F3V2B [arany v2] | R1 | lefedettseg | 95.90% | 93.38% | -2.52 pp | [-5.52; +0.63] | 5.52 pp | 20 |
| F3V3 − F3V2B [arany v2] | R1 | kapuhiba_elso_probara | 21.00% | 12.00% | -9.00 pp | [-15.00; -3.00] | 15.00 pp | 100 |
| F3V3 − F3V2B [arany v2] | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − F3V2B [arany v2] | R2 | pontossag | 95.60% | 96.84% | +1.24 pp | [-2.34; +3.97] | 4.01 pp | 10 |
| F3V3 − F3V2B [arany v2] | R2 | lefedettseg | 99.35% | 100.00% | +0.65 pp | [+0.00; +1.87] | 1.87 pp | 10 |
| F3V3 − F3V2B [arany v2] | R2 | kapuhiba_elso_probara | 20.00% | 0.00% | -20.00 pp | [-32.00; -8.00] | 32.00 pp | 25 |
| F3V3 − F3V2B [arany v2] | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − F3V2B [arany v2] | R3 | pontossag | 93.93% | 94.44% | +0.52 pp | [-1.44; +2.64] | 2.69 pp | 10 |
| F3V3 − F3V2B [arany v2] | R3 | lefedettseg | 98.87% | 95.86% | -3.01 pp | [-5.24; -1.19] | 5.24 pp | 10 |
| F3V3 − F3V2B [arany v2] | R3 | kapuhiba_elso_probara | 4.00% | 40.00% | +36.00 pp | [+20.00; +52.00] | 52.00 pp | 25 |
| F3V3 − F3V2B [arany v2] | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − F3V2B [arany v2] | R4 | pontossag | 90.27% | 94.44% | +4.18 pp | [+1.77; +6.73] | 6.73 pp | 20 |
| F3V3 − F3V2B [arany v2] | R4 | lefedettseg | 97.14% | 97.14% | +0.00 pp | [-1.29; +1.31] | 1.53 pp | 20 |
| F3V3 − F3V2B [arany v2] | R4 | kapuhiba_elso_probara | 2.00% | 16.00% | +14.00 pp | [+6.00; +24.00] | 24.00 pp | 50 |
| F3V3 − F3V2B [arany v2] | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − F3V2B [arany v2] | Összes | pontossag | 93.01% | 95.37% | +2.36 pp | [+1.12; +3.56] | 3.56 pp | 60 |
| F3V3 − F3V2B [arany v2] | Összes | lefedettseg | 97.53% | 96.10% | -1.43 pp | [-2.56; -0.28] | 2.56 pp | 60 |
| F3V3 − F3V2B [arany v2] | Összes | kapuhiba_elso_probara | 14.00% | 15.00% | +1.00 pp | [-3.50; +5.50] | 5.50 pp | 200 |
| F3V3 − F3V2B [arany v2] | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R1 | pontossag | 93.93% | 96.42% | +2.49 pp | [-0.10; +4.49] | 4.49 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R1 | lefedettseg | 95.11% | 93.38% | -1.74 pp | [-3.83; +0.51] | 3.83 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R1 | kapuhiba_elso_probara | 16.50% | 12.00% | -4.50 pp | [-8.00; -0.50] | 8.00 pp | 100 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R2 | pontossag | 95.61% | 96.84% | +1.22 pp | [-0.76; +2.86] | 2.86 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R2 | lefedettseg | 99.67% | 100.00% | +0.33 pp | [+0.00; +0.93] | 0.93 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R2 | kapuhiba_elso_probara | 10.00% | 0.00% | -10.00 pp | [-16.00; -4.00] | 16.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R3 | pontossag | 94.06% | 94.44% | +0.39 pp | [-1.99; +2.61] | 2.83 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R3 | lefedettseg | 98.12% | 95.86% | -2.26 pp | [-4.11; -0.89] | 4.11 pp | 10 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R3 | kapuhiba_elso_probara | 6.00% | 40.00% | +34.00 pp | [+18.00; +50.00] | 50.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R3 | kapuhiba_vegleg | 0.00% | 8.00% | +8.00 pp | [+0.00; +16.00] | 16.00 pp | 25 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R4 | pontossag | 90.98% | 94.44% | +3.47 pp | [+1.57; +5.53] | 5.53 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R4 | lefedettseg | 97.62% | 97.14% | -0.48 pp | [-1.77; +0.80] | 1.77 pp | 20 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R4 | kapuhiba_elso_probara | 6.00% | 16.00% | +10.00 pp | [+0.00; +20.00] | 20.00 pp | 50 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | Összes | pontossag | 93.30% | 95.37% | +2.08 pp | [+0.90; +3.18] | 3.18 pp | 60 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | Összes | lefedettseg | 97.29% | 96.10% | -1.19 pp | [-2.00; -0.26] | 2.00 pp | 60 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | Összes | kapuhiba_elso_probara | 11.75% | 15.00% | +3.25 pp | [-0.50; +7.00] | 7.00 pp | 200 |
| F3V3 − átlag(F3V2, F3V2B) [arany v2] | Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 2.00 pp | 200 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R1 | pontossag | 94.03% | 93.83% | -0.20 pp | [-2.46; +1.88] | 2.61 pp | 20 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R1 | lefedettseg | 94.32% | 95.90% | +1.58 pp | [-1.88; +4.59] | 4.65 pp | 20 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R1 | kapuhiba_elso_probara | 12.00% | 21.00% | +9.00 pp | [+3.00; +15.00] | 15.00 pp | 100 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R2 | pontossag | 95.63% | 95.60% | -0.03 pp | [-2.56; +3.60] | 3.62 pp | 10 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R2 | lefedettseg | 100.00% | 99.35% | -0.65 pp | [-1.87; +0.00] | 1.87 pp | 10 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R2 | kapuhiba_elso_probara | 0.00% | 20.00% | +20.00 pp | [+8.00; +32.00] | 32.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R3 | pontossag | 94.18% | 93.93% | -0.25 pp | [-1.87; +1.06] | 1.87 pp | 10 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R3 | lefedettseg | 97.37% | 98.87% | +1.50 pp | [+0.34; +2.88] | 2.88 pp | 10 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R3 | kapuhiba_elso_probara | 8.00% | 4.00% | -4.00 pp | [-12.00; +0.00] | 12.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R3 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R4 | pontossag | 91.69% | 90.27% | -1.43 pp | [-3.66; +0.79] | 3.66 pp | 20 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R4 | lefedettseg | 98.10% | 97.14% | -0.95 pp | [-2.14; +0.00] | 2.14 pp | 20 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R4 | kapuhiba_elso_probara | 10.00% | 2.00% | -8.00 pp | [-16.00; +0.00] | 16.00 pp | 50 |
| F3V2B − F3V2 (ingadozás) [arany v2] | R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| F3V2B − F3V2 (ingadozás) [arany v2] | Összes | pontossag | 93.58% | 93.01% | -0.57 pp | [-1.64; +0.53] | 1.64 pp | 60 |
| F3V2B − F3V2 (ingadozás) [arany v2] | Összes | lefedettseg | 97.05% | 97.53% | +0.48 pp | [-0.62; +1.60] | 1.61 pp | 60 |
| F3V2B − F3V2 (ingadozás) [arany v2] | Összes | kapuhiba_elso_probara | 9.50% | 14.00% | +4.50 pp | [+0.50; +8.50] | 8.50 pp | 200 |
| F3V2B − F3V2 (ingadozás) [arany v2] | Összes | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 200 |

Az „F8V3 − F3V3 (KJV, tájékoztató)” sorok R4-e: KJV nélkül, nem mérhető (azonos bemenet, a különbség futásközi ingadozás).

