# F21P_meres_v1.md — P4 mérés a v1-adaton (F1, F2, F3, F5, F6; F4 nélkül)

<!-- GENERÁLT: eszkozok/karoli_strong/meres.py | scope=f21p | forras=f21p/valaszok/*.jsonl, f21p/arany_opus.jsonl, f21p/meres_kizaras.tsv, f21p/futasnaplo.tsv | ts=2026-09-30T11:16:32+00:00 | kézzel szerkeszteni tilos; a számok forrása f21p/meres_eredmeny.tsv -->

Kizárólag szkriptkimenet; értelmezés és küszöb-minősítés nincs benne. Cellaforma: érték% (számláló/nevező) [90%-os Wilson-intervallum, linkszintű, optimista]. Az arany 60 vers (R1 20, R2 10, R3 10, R4 20), ezért a rétegenkénti értékek megbízhatósága korlátozott: a nevezőt mindig nézd. `alacsony` arány: egymodelles futásokra n.é. (PD6, G4).

## a) Pontosság és lefedettség az Opus-aranyhoz (csak kapun átment, aranyba eső versek)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A | arany_versek_kapun_atment | 65.0% (13/20) | 60.0% (6/10) | 80.0% (8/10) | 60.0% (12/20) | 65.0% (39/60) |
| A | pontossag | 80.1% (129/161) [74–85] | 92.8% (64/69) [86–96] | 76.0% (190/250) [71–80] | 85.3% (145/170) [80–89] | 81.2% (528/650) [79–84] |
| A | lefedettseg | 75.4% (129/171) [70–80] | 87.7% (64/73) [80–93] | 83.7% (190/227) [79–87] | 81.9% (145/177) [77–86] | 81.5% (528/648) [79–84] |
| B | arany_versek_kapun_atment | 85.0% (17/20) | 100.0% (10/10) | 100.0% (10/10) | 75.0% (15/20) | 86.7% (52/60) |
| B | pontossag | 58.0% (156/269) [53–63] | 72.2% (140/194) [67–77] | 56.9% (244/429) [53–61] | 81.5% (202/248) [77–85] | 65.1% (742/1140) [63–67] |
| B | lefedettseg | 59.8% (156/261) [55–65] | 91.5% (140/153) [87–95] | 91.7% (244/266) [89–94] | 78.6% (202/257) [74–82] | 79.2% (742/937) [77–81] |
| C | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C | pontossag | 94.2% (294/312) [92–96] | 94.2% (146/155) [90–97] | 91.9% (250/272) [89–94] | 92.9% (299/322) [90–95] | 93.2% (989/1061) [92–94] |
| C | lefedettseg | 92.7% (294/317) [90–95] | 95.4% (146/153) [92–98] | 94.0% (250/266) [91–96] | 94.9% (299/315) [92–97] | 94.1% (989/1051) [93–95] |
| A+B magas (A∩B) | arany_versek_kapun_atment | 55.0% (11/20) | 60.0% (6/10) | 80.0% (8/10) | 35.0% (7/20) | 53.3% (32/60) |
| A+B magas (A∩B) | pontossag | 85.2% (52/61) [76–91] | 98.4% (61/62) [93–100] | 91.8% (179/195) [88–94] | 91.7% (77/84) [85–95] | 91.8% (369/402) [89–94] |
| A+B magas (A∩B) | lefedettseg | 35.6% (52/146) [29–42] | 83.6% (61/73) [75–89] | 78.9% (179/227) [74–83] | 64.7% (77/119) [57–72] | 65.3% (369/565) [62–69] |
| A∪B (döntőbíró előtti felső korlát) | arany_versek_kapun_atment | 55.0% (11/20) | 60.0% (6/10) | 80.0% (8/10) | 35.0% (7/20) | 53.3% (32/60) |
| A∪B (döntőbíró előtti felső korlát) | pontossag | 55.6% (120/216) [50–61] | 75.0% (72/96) [67–82] | 53.6% (216/403) [50–58] | 71.1% (101/142) [65–77] | 59.4% (509/857) [57–62] |
| A∪B (döntőbíró előtti felső korlát) | lefedettseg | 82.2% (120/146) [76–87] | 98.6% (72/73) [94–100] | 95.2% (216/227) [92–97] | 84.9% (101/119) [79–90] | 90.1% (509/565) [88–92] |

## b) Régi arany egyezés (kapun átment versek, a 200 verses mintában)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A | hármasok_kapun_atment_versekben | 24 | 0 | 0 | 0 | 24 |
| A | nem_talalhato_karoli_szo | 0.0% (0/24) | — (0/0) | — (0/0) | — (0/0) | 0.0% (0/24) |
| A | egyezes | 62.5% (15/24) [46–77] | — (0/0) | — (0/0) | — (0/0) | 62.5% (15/24) [46–77] |
| B | hármasok_kapun_atment_versekben | 6 | 0 | 0 | 0 | 6 |
| B | nem_talalhato_karoli_szo | 0.0% (0/6) | — (0/0) | — (0/0) | — (0/0) | 0.0% (0/6) |
| B | egyezes | 66.7% (4/6) [35–88] | — (0/0) | — (0/0) | — (0/0) | 66.7% (4/6) [35–88] |
| C | hármasok_kapun_atment_versekben | 32 | 0 | 0 | 0 | 32 |
| C | nem_talalhato_karoli_szo | 0.0% (0/32) | — (0/0) | — (0/0) | — (0/0) | 0.0% (0/32) |
| C | egyezes | 75.0% (24/32) [61–85] | — (0/0) | — (0/0) | — (0/0) | 75.0% (24/32) [61–85] |
| A+B magas (A∩B) | hármasok_kapun_atment_versekben | 5 | 0 | 0 | 0 | 5 |
| A+B magas (A∩B) | nem_talalhato_karoli_szo | 0.0% (0/5) | — (0/0) | — (0/0) | — (0/0) | 0.0% (0/5) |
| A+B magas (A∩B) | egyezes | 60.0% (3/5) [27–86] | — (0/0) | — (0/0) | — (0/0) | 60.0% (3/5) [27–86] |

## c) A–B egyezés (csak ahol A és B is átment a kapun)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A–B | versek_mindketto_atment | 15.0% (15/100) | 68.0% (17/25) | 40.0% (10/25) | 46.0% (23/50) | 32.5% (65/200) |
| A–B | link_egyezes (uniós arány) | 32.5% (93/286) [28–37] | 59.8% (149/249) [55–65] | 48.3% (219/453) [44–52] | 67.5% (287/425) [64–71] | 52.9% (748/1413) [51–55] |
| A–B | azonos_linkhalmazu_versek | 13.3% (2/15) | 0.0% (0/17) | 0.0% (0/10) | 4.3% (1/23) | 4.6% (3/65) |

## d) Kapuhiba-arány (első próbára és végleg)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F1 (A) | kapuhiba_elso_probara | 71.0% (71/100) [63–78] | 76.0% (19/25) [60–87] | 96.0% (24/25) [84–99] | 76.0% (38/50) [65–84] | 76.0% (152/200) [71–81] |
| F1 (A) | kapuhiba_vegleg | 42.0% (42/100) [34–50] | 32.0% (8/25) [19–48] | 40.0% (10/25) [26–56] | 44.0% (22/50) [33–56] | 41.0% (82/200) [35–47] |
| F2 (B) | kapuhiba_elso_probara | 80.0% (80/100) [73–86] | 8.0% (2/25) [3–22] | 52.0% (13/25) [36–67] | 22.0% (11/50) [14–33] | 53.0% (106/200) [47–59] |
| F2 (B) | kapuhiba_vegleg | 68.0% (68/100) [60–75] | 0.0% (0/25) [0–10] | 36.0% (9/25) [22–52] | 10.0% (5/50) [5–19] | 41.0% (82/200) [35–47] |
| F3 (C) | kapuhiba_elso_probara | 17.0% (17/100) [12–24] | 0.0% (0/25) [0–10] | 20.0% (5/25) [10–36] | 16.0% (8/50) [9–26] | 15.0% (30/200) [11–20] |
| F3 (C) | kapuhiba_vegleg | 1.0% (1/100) [0–4] | 0.0% (0/25) [0–10] | 0.0% (0/25) [0–10] | 0.0% (0/50) [0–5] | 0.5% (1/200) [0–2] |
| F5 (A (KJV nélkül)) | kapuhiba_elso_probara | 75.0% (75/100) [67–81] | — | — | — | 75.0% (75/100) [67–81] |
| F5 (A (KJV nélkül)) | kapuhiba_vegleg | 31.0% (31/100) [24–39] | — | — | — | 31.0% (31/100) [24–39] |
| F6 (B (KJV nélkül)) | kapuhiba_elso_probara | 23.0% (23/100) [17–31] | — | — | — | 23.0% (23/100) [17–31] |
| F6 (B (KJV nélkül)) | kapuhiba_vegleg | 13.0% (13/100) [8–20] | — | — | — | 13.0% (13/100) [8–20] |

- keresztellenorzes_elso_probalkozas — F1 (A): 100.0% (152/152); újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: EGYEZIK
- keresztellenorzes_elso_probalkozas — F2 (B): 100.0% (106/106); újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: EGYEZIK
- keresztellenorzes_elso_probalkozas — F3 (C): 100.0% (30/30); újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: EGYEZIK
- keresztellenorzes_elso_probalkozas — F5 (A (KJV nélkül)): 100.0% (75/75); újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: EGYEZIK
- keresztellenorzes_elso_probalkozas — F6 (B (KJV nélkül)): 100.0% (23/23); újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: EGYEZIK

## d2) Kapuhiba-típusok kapupont szerint (hibás versek száma)

| összeállítás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| F1 (A) | kapupont_1-json_elso_probara | 50.0% (100/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F1 (A) | kapupont_1-json_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F1 (A) | kapupont_2_elso_probara | 1.5% (3/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F1 (A) | kapupont_2_vegleg | 6.5% (13/200) | a végleg hibás versek kapuponttal |
| F1 (A) | kapupont_3_elso_probara | 23.5% (47/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F1 (A) | kapupont_3_vegleg | 32.5% (65/200) | a végleg hibás versek kapuponttal |
| F1 (A) | kapupont_4_elso_probara | 7.5% (15/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F1 (A) | kapupont_4_vegleg | 18.5% (37/200) | a végleg hibás versek kapuponttal |
| F2 (B) | kapupont_1-hianyzo_vers_elso_probara | 9.0% (18/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F2 (B) | kapupont_1-hianyzo_vers_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F2 (B) | kapupont_1-json_elso_probara | 20.0% (40/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F2 (B) | kapupont_1-json_vegleg | 20.0% (40/200) | a végleg hibás versek kapuponttal |
| F2 (B) | kapupont_2_elso_probara | 5.0% (10/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F2 (B) | kapupont_2_vegleg | 6.5% (13/200) | a végleg hibás versek kapuponttal |
| F2 (B) | kapupont_3_elso_probara | 11.5% (23/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F2 (B) | kapupont_3_vegleg | 10.0% (20/200) | a végleg hibás versek kapuponttal |
| F2 (B) | kapupont_4_elso_probara | 9.0% (18/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F2 (B) | kapupont_4_vegleg | 6.0% (12/200) | a végleg hibás versek kapuponttal |
| F3 (C) | kapupont_1_elso_probara | 7.5% (15/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F3 (C) | kapupont_1_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F3 (C) | kapupont_1-json_elso_probara | 5.0% (10/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F3 (C) | kapupont_1-json_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F3 (C) | kapupont_2_elso_probara | 0.5% (1/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F3 (C) | kapupont_2_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F3 (C) | kapupont_3_elso_probara | 0.5% (1/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F3 (C) | kapupont_3_vegleg | 0.0% (0/200) | a végleg hibás versek kapuponttal |
| F3 (C) | kapupont_4_elso_probara | 2.5% (5/200) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F3 (C) | kapupont_4_vegleg | 0.5% (1/200) | a végleg hibás versek kapuponttal |
| F5 (A (KJV nélkül)) | kapupont_1_elso_probara | 0.0% (0/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F5 (A (KJV nélkül)) | kapupont_1_vegleg | 2.0% (2/100) | a végleg hibás versek kapuponttal |
| F5 (A (KJV nélkül)) | kapupont_1-json_elso_probara | 30.0% (30/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F5 (A (KJV nélkül)) | kapupont_1-json_vegleg | 0.0% (0/100) | a végleg hibás versek kapuponttal |
| F5 (A (KJV nélkül)) | kapupont_2_elso_probara | 5.0% (5/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F5 (A (KJV nélkül)) | kapupont_2_vegleg | 9.0% (9/100) | a végleg hibás versek kapuponttal |
| F5 (A (KJV nélkül)) | kapupont_3_elso_probara | 38.0% (38/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F5 (A (KJV nélkül)) | kapupont_3_vegleg | 19.0% (19/100) | a végleg hibás versek kapuponttal |
| F5 (A (KJV nélkül)) | kapupont_4_elso_probara | 20.0% (20/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F5 (A (KJV nélkül)) | kapupont_4_vegleg | 16.0% (16/100) | a végleg hibás versek kapuponttal |
| F6 (B (KJV nélkül)) | kapupont_1_elso_probara | 8.0% (8/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F6 (B (KJV nélkül)) | kapupont_1_vegleg | 8.0% (8/100) | a végleg hibás versek kapuponttal |
| F6 (B (KJV nélkül)) | kapupont_3_elso_probara | 7.0% (7/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F6 (B (KJV nélkül)) | kapupont_3_vegleg | 3.0% (3/100) | a végleg hibás versek kapuponttal |
| F6 (B (KJV nélkül)) | kapupont_4_elso_probara | 11.0% (11/100) | hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat) |
| F6 (B (KJV nélkül)) | kapupont_4_vegleg | 2.0% (2/100) | a végleg hibás versek kapuponttal |

## e) Az A+B összeállítás F4 nélkül (döntőbíróhoz menő versek)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A+B | mindketto_atment_azonos_linkekkel | 2.0% (2/100) | 0.0% (0/25) | 0.0% (0/25) | 2.0% (1/50) | 1.5% (3/200) |
| A+B | mindketto_atment_eltero_linkekkel | 13.0% (13/100) | 68.0% (17/25) | 40.0% (10/25) | 44.0% (22/50) | 31.0% (62/200) |
| A+B | csak_A_atment | 43.0% (43/100) | 0.0% (0/25) | 20.0% (5/25) | 10.0% (5/50) | 26.5% (53/200) |
| A+B | csak_B_atment | 17.0% (17/100) | 32.0% (8/25) | 24.0% (6/25) | 44.0% (22/50) | 26.5% (53/200) |
| A+B | egyik_sem_atment | 25.0% (25/100) | 0.0% (0/25) | 16.0% (4/25) | 0.0% (0/50) | 14.5% (29/200) |
| A+B | dontobirohoz_menne (eltero + csak egyik + egyik sem) | 98.0% (98/100) [94–99] | 100.0% (25/25) [90–100] | 100.0% (25/25) [90–100] | 98.0% (49/50) [92–100] | 98.5% (197/200) [96–99] |
| A+B | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| A+B | nem_egyezo_link_arany (1 − A∩B/A∪B) | 67.5% (193/286) | 40.2% (100/249) | 51.7% (234/453) | 32.5% (138/425) | 47.1% (665/1413) |

## f) KJV-hatás az R1-en (F1/F2 R1-részhalmaz az F5/F6-tal szemben)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-val (F1/F2) A | kapuhiba_vegleg | 42.0% (42/100) [34–50] | — | — | — | — |
| KJV-val (F1/F2) A | kapuhiba_elso_probara | 71.0% (71/100) [63–78] | — | — | — | — |
| KJV-val (F1/F2) B | kapuhiba_vegleg | 68.0% (68/100) [60–75] | — | — | — | — |
| KJV-val (F1/F2) B | kapuhiba_elso_probara | 80.0% (80/100) [73–86] | — | — | — | — |
| KJV nélkül (F5/F6) A (KJV nélkül) | kapuhiba_vegleg | 31.0% (31/100) [24–39] | — | — | — | — |
| KJV nélkül (F5/F6) A (KJV nélkül) | kapuhiba_elso_probara | 75.0% (75/100) [67–81] | — | — | — | — |
| KJV nélkül (F5/F6) B (KJV nélkül) | kapuhiba_vegleg | 13.0% (13/100) [8–20] | — | — | — | — |
| KJV nélkül (F5/F6) B (KJV nélkül) | kapuhiba_elso_probara | 23.0% (23/100) [17–31] | — | — | — | — |
| A KJV-val | arany_versek [saját halmaz (kapun átment)] | 65.0% (13/20) | — | — | — | — |
| A KJV-val | pontossag [saját halmaz (kapun átment)] | 80.1% (129/161) [74–85] | — | — | — | — |
| A KJV-val | lefedettseg [saját halmaz (kapun átment)] | 75.4% (129/171) [70–80] | — | — | — | — |
| A KJV-val | arany_versek [közös halmaz (mindkét feltételben átment)] | 55.0% (11/20) | — | — | — | — |
| A KJV-val | pontossag [közös halmaz (mindkét feltételben átment)] | 81.7% (107/131) [76–87] | — | — | — | — |
| A KJV-val | lefedettseg [közös halmaz (mindkét feltételben átment)] | 76.4% (107/140) [70–82] | — | — | — | — |
| A KJV nélkül | arany_versek [saját halmaz (kapun átment)] | 75.0% (15/20) | — | — | — | — |
| A KJV nélkül | pontossag [saját halmaz (kapun átment)] | 78.1% (185/237) [73–82] | — | — | — | — |
| A KJV nélkül | lefedettseg [saját halmaz (kapun átment)] | 86.0% (185/215) [82–89] | — | — | — | — |
| A KJV nélkül | arany_versek [közös halmaz (mindkét feltételben átment)] | 55.0% (11/20) | — | — | — | — |
| A KJV nélkül | pontossag [közös halmaz (mindkét feltételben átment)] | 79.9% (119/149) [74–85] | — | — | — | — |
| A KJV nélkül | lefedettseg [közös halmaz (mindkét feltételben átment)] | 85.0% (119/140) [79–89] | — | — | — | — |
| B KJV-val | arany_versek [saját halmaz (kapun átment)] | 85.0% (17/20) | — | — | — | — |
| B KJV-val | pontossag [saját halmaz (kapun átment)] | 58.0% (156/269) [53–63] | — | — | — | — |
| B KJV-val | lefedettseg [saját halmaz (kapun átment)] | 59.8% (156/261) [55–65] | — | — | — | — |
| B KJV-val | arany_versek [közös halmaz (mindkét feltételben átment)] | 80.0% (16/20) | — | — | — | — |
| B KJV-val | pontossag [közös halmaz (mindkét feltételben átment)] | 59.7% (154/258) [55–65] | — | — | — | — |
| B KJV-val | lefedettseg [közös halmaz (mindkét feltételben átment)] | 62.3% (154/247) [57–67] | — | — | — | — |
| B KJV nélkül | arany_versek [saját halmaz (kapun átment)] | 85.0% (17/20) | — | — | — | — |
| B KJV nélkül | pontossag [saját halmaz (kapun átment)] | 67.7% (172/254) [63–72] | — | — | — | — |
| B KJV nélkül | lefedettseg [saját halmaz (kapun átment)] | 61.9% (172/278) [57–67] | — | — | — | — |
| B KJV nélkül | arany_versek [közös halmaz (mindkét feltételben átment)] | 80.0% (16/20) | — | — | — | — |
| B KJV nélkül | pontossag [közös halmaz (mindkét feltételben átment)] | 66.5% (149/224) [61–71] | — | — | — | — |
| B KJV nélkül | lefedettseg [közös halmaz (mindkét feltételben átment)] | 60.3% (149/247) [55–65] | — | — | — | — |
| KJV-val (F1/F2) | A–B_versek [saját halmaz (A és B átment)] | 15.0% (15/100) | — | — | — | — |
| KJV-val (F1/F2) | A–B_egyezes [saját halmaz (A és B átment)] | 32.5% (93/286) [28–37] | — | — | — | — |
| KJV-val (F1/F2) | A–B_versek [közös halmaz (mind a négy átment)] | 10.0% (10/100) | — | — | — | — |
| KJV-val (F1/F2) | A–B_egyezes [közös halmaz (mind a négy átment)] | 46.1% (77/167) [40–52] | — | — | — | — |
| KJV nélkül (F5/F6) | A–B_versek [saját halmaz (A és B átment)] | 60.0% (60/100) | — | — | — | — |
| KJV nélkül (F5/F6) | A–B_egyezes [saját halmaz (A és B átment)] | 56.3% (651/1157) [54–59] | — | — | — | — |
| KJV nélkül (F5/F6) | A–B_versek [közös halmaz (mind a négy átment)] | 10.0% (10/100) | — | — | — | — |
| KJV nélkül (F5/F6) | A–B_egyezes [közös halmaz (mind a négy átment)] | 50.9% (84/165) [45–57] | — | — | — | — |
| KJV-val (F1/F2) | magas (A∩B) arany_versek [közös halmaz] | 40.0% (8/20) | — | — | — | — |
| KJV-val (F1/F2) | magas (A∩B) pontossag [közös halmaz] | 86.4% (51/59) [78–92] | — | — | — | — |
| KJV-val (F1/F2) | magas (A∩B) lefedettseg [közös halmaz] | 50.5% (51/101) [42–59] | — | — | — | — |
| KJV nélkül (F5/F6) | magas (A∩B) arany_versek [közös halmaz] | 40.0% (8/20) | — | — | — | — |
| KJV nélkül (F5/F6) | magas (A∩B) pontossag [közös halmaz] | 91.8% (56/61) [84–96] | — | — | — | — |
| KJV nélkül (F5/F6) | magas (A∩B) lefedettseg [közös halmaz] | 55.4% (56/101) [47–63] | — | — | — | — |
| KJV-val − KJV nélkül | delta_magas_pontossag_szazalekpont [közös halmaz] | -5.36 | — | — | — | — |
| KJV-val vs KJV nélkül | A–B_eltérés_relativ_csokkenes [közös halmaz (mind a négy átment)] | -9.78 | — | — | — | — |
| KJV-val vs KJV nélkül | A–B_eltérés_relativ_csokkenes [saját halmaz (A és B átment)] | -54.3 | — | — | — | — |

- delta_magas_pontossag_szazalekpont [közös halmaz] — KJV-val − KJV nélkül: -5.36; küszöb-mérőszám 1 (a brief szerint ≥ +1 pp); n: 59 ill. 61 link
- A–B_eltérés_relativ_csokkenes [közös halmaz (mind a négy átment)] — KJV-val vs KJV nélkül: -9.78; küszöb-mérőszám 2 (a brief szerint ≥ 20%); eltérés KJV nélkül 81/165, KJV-val 90/167
- A–B_eltérés_relativ_csokkenes [saját halmaz (A és B átment)] — KJV-val vs KJV nélkül: -54.3; küszöb-mérőszám 2 (a brief szerint ≥ 20%); eltérés KJV nélkül 506/1157, KJV-val 193/286

## g) Költség futásonként (a futásnaplóból)

| összeállítás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| F1 (A) | hivasok_osszes | 40 | próbálkozás=1: 20, próbálkozás=2: 20 |
| F1 (A) | bemeneti_token | 304043 |  |
| F1 (A) | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 50025 |  |
| F1 (A) | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 |  |
| F1 (A) | koltseg_usd (OpenRouter cost mező) | 0.132718 | koltseg_forras: openrouter |
| F1 (A) | gondolkodasi_mod | kikapcsolva |  |
| F2 (B) | hivasok_osszes | 37 | próbálkozás=1: 20, próbálkozás=2: 17 |
| F2 (B) | bemeneti_token | 253328 |  |
| F2 (B) | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 34727 |  |
| F2 (B) | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 |  |
| F2 (B) | koltseg_usd (OpenRouter cost mező) | 0.017725 | koltseg_forras: openrouter |
| F2 (B) | gondolkodasi_mod | kikapcsolva |  |
| F3 (C) | hivasok_osszes | 27 | próbálkozás=1: 20, próbálkozás=2: 7 |
| F3 (C) | bemeneti_token | 196498 |  |
| F3 (C) | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 30770 |  |
| F3 (C) | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 | FIGYELEM: a C-nél a napló 0-t ír; a nyers usage nem maradt meg, a múltbeli érték nem rekonstruálható |
| F3 (C) | koltseg_usd (OpenRouter cost mező) | 0.257251 | koltseg_forras: openrouter |
| F3 (C) | gondolkodasi_mod | kotelezo_effort=minimal |  |
| F5 (A (KJV nélkül)) | hivasok_osszes | 20 | próbálkozás=1: 10, próbálkozás=2: 10 |
| F5 (A (KJV nélkül)) | bemeneti_token | 142979 |  |
| F5 (A (KJV nélkül)) | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 23946 |  |
| F5 (A (KJV nélkül)) | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 |  |
| F5 (A (KJV nélkül)) | koltseg_usd (OpenRouter cost mező) | 0.060663 | koltseg_forras: openrouter |
| F5 (A (KJV nélkül)) | gondolkodasi_mod | kikapcsolva |  |
| F6 (B (KJV nélkül)) | hivasok_osszes | 18 | próbálkozás=1: 10, próbálkozás=2: 8 |
| F6 (B (KJV nélkül)) | bemeneti_token | 120895 |  |
| F6 (B (KJV nélkül)) | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 16819 |  |
| F6 (B (KJV nélkül)) | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 |  |
| F6 (B (KJV nélkül)) | koltseg_usd (OpenRouter cost mező) | 0.009506 | koltseg_forras: openrouter |
| F6 (B (KJV nélkül)) | gondolkodasi_mod | kikapcsolva |  |
| -- összesen | hivasok_osszes | 142 | próbálkozás=1: 80, próbálkozás=2: 62 |
| -- összesen | bemeneti_token | 1017743 |  |
| -- összesen | kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja) | 156287 |  |
| -- összesen | gondolkodasi_token (napló gondolkodas_token oszlopa) | 0 | FIGYELEM: a C-nél a napló 0-t ír; a nyers usage nem maradt meg, a múltbeli érték nem rekonstruálható |
| -- összesen | koltseg_usd (OpenRouter cost mező) | 0.477863 | koltseg_forras: openrouter |
| -- összesen | gondolkodasi_mod | kikapcsolva; kotelezo_effort=minimal |  |

## g2) A cost és a táblaár viszonya

| összeállítás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| google/gemini-3.1-flash-lite | cost / (bemenet·ár + kimenet·ár) | 86.8% (0.193381/0.222712) | táblaár 0.250/1.500 USD/1M (futtat.ARAK); az érték a tényleges/táblaár arány; nem a gondolkodási token mérése |
| deepseek/deepseek-v4-flash | cost / (bemenet·ár + kimenet·ár) | 40.8% (0.027231/0.066824) | táblaár 0.140/0.280 USD/1M (futtat.ARAK); az érték a tényleges/táblaár arány; nem a gondolkodási token mérése |
| google/gemini-3.8-flash | cost / (bemenet·ár + kimenet·ár) | 97.9% (0.257251/0.262761) | táblaár 0.750/3.750 USD/1M (futtat.ARAK); az érték a tényleges/táblaár arány; nem a gondolkodási token mérése |

