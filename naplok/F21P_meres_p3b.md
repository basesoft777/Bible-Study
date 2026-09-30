# F21P_meres_p3b.md — P4 a P3b-adaton (prompt_v2), minden összeállítás, arany v2

<!-- GENERÁLT: eszkozok/karoli_strong/meres_p3b.py | scope=P3b (prompt_v2): A=F1V2, B=F2V2, C=F3V2 és F3V2B, A+B, A+B+C (F4V2), KJV nélkül F5V2/F6V2; arany v2 (60 vers), 200 verses minta | forras=f21p/valaszok/{F1V2,F2V2,F3V2,F3V2B,F4V2,F5V2,F6V2}.jsonl, f21p/valaszok/{F1,F2,F3,F5,F6}.jsonl (v1-kapuhiba), f21p/arany_opus_v2.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, f21p/koltseg_vetites_p3b.tsv | ts=2026-09-30T15:21:36+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

Kizárólag szkriptkimenet. A G4 szabály szó szerint (F22 brief 22.6): magas = A∩B (a KJV-ellentmondás feltétele gépileg n.é.); kozepes = a C döntőbíró linkje A vagy B egyikében; alacsony = hármas eltérés, vagy a vers kapuhibás maradt (A vagy B végleg kapuhibás: a C válasza, minden link alacsony). Az A+B (döntőbíró nélkül): A∩B magas, minden más link alacsony — a jelentés értelmezése. Egymodelles összeállítás (A, B, C) nem minősíthető (PD6). Cellaforma: érték (számláló/nevező).

## a) Az öt feltétel összeállításonként és rétegenként

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A (F1V2) | arany_versek_kapun_atment | 60.0% (12/20) | 90.0% (9/10) | 30.0% (3/10) | 55.0% (11/20) | 58.3% (35/60) |
| A (F1V2) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| A (F1V2) | pontossag_osszes (tajekoztato, PD6) | 85.5% (118/138) | 81.7% (103/126) | 79.5% (58/73) | 81.2% (121/149) | 82.3% (400/486) |
| A (F1V2) | lefedettseg | 73.8% (118/160) | 81.7% (103/126) | 87.9% (58/66) | 80.7% (121/150) | 79.7% (400/502) |
| A (F1V2) | regi_arany_kizaras_nelkul | 71.4% (10/14) | — (0/0) | — (0/0) | — (0/0) | 71.4% (10/14) |
| A (F1V2) | regi_arany_kizarassal_tajekoztato | 76.9% (10/13) | — (0/0) | — (0/0) | — (0/0) | 76.9% (10/13) |
| A (F1V2) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| B (F2V2) | arany_versek_kapun_atment | 50.0% (10/20) | 90.0% (9/10) | 100.0% (10/10) | 50.0% (10/20) | 65.0% (39/60) |
| B (F2V2) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| B (F2V2) | pontossag_osszes (tajekoztato, PD6) | 61.3% (111/181) | 79.1% (121/153) | 50.0% (255/510) | 77.2% (129/167) | 60.9% (616/1011) |
| B (F2V2) | lefedettseg | 87.4% (111/127) | 96.0% (121/126) | 95.9% (255/266) | 90.8% (129/142) | 93.2% (616/661) |
| B (F2V2) | regi_arany_kizaras_nelkul | 84.2% (16/19) | — (0/0) | — (0/0) | — (0/0) | 84.2% (16/19) |
| B (F2V2) | regi_arany_kizarassal_tajekoztato | 88.9% (16/18) | — (0/0) | — (0/0) | — (0/0) | 88.9% (16/18) |
| B (F2V2) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V2) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V2) | pontossag_osszes (tajekoztato, PD6) | 94.0% (299/318) | 95.6% (153/160) | 94.2% (259/275) | 91.7% (309/337) | 93.6% (1020/1090) |
| C (F3V2) | lefedettseg | 94.3% (299/317) | 100.0% (153/153) | 97.4% (259/266) | 98.1% (309/315) | 97.1% (1020/1051) |
| C (F3V2) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V2) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V2) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V2B) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V2B) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V2B) | pontossag_osszes (tajekoztato, PD6) | 93.8% (304/324) | 95.6% (152/159) | 93.9% (263/280) | 90.3% (306/339) | 93.0% (1025/1102) |
| C (F3V2B) | lefedettseg | 95.9% (304/317) | 99.3% (152/153) | 98.9% (263/266) | 97.1% (306/315) | 97.5% (1025/1051) |
| C (F3V2B) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V2B) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V2B) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| A+B | arany_versek | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| A+B | magas_pontossag | 95.4% (83/87) | 93.4% (99/106) | 90.6% (58/64) | 97.0% (98/101) | 94.4% (338/358) |
| A+B | pontossag_osszes (tajekoztato) | 62.9% (146/232) | 72.3% (125/173) | 49.1% (255/519) | 70.7% (152/215) | 59.5% (678/1139) |
| A+B | lefedettseg | 46.1% (146/317) | 81.7% (125/153) | 95.9% (255/266) | 48.3% (152/315) | 64.5% (678/1051) |
| A+B | regi_arany_kizaras_nelkul | 56.2% (18/32) | — (0/0) | — (0/0) | — (0/0) | 56.2% (18/32) |
| A+B | regi_arany_kizarassal_tajekoztato | 58.1% (18/31) | — (0/0) | — (0/0) | — (0/0) | 58.1% (18/31) |
| A+B | alacsony_arany [200 vers] | 68.9% (1255/1822) | 55.0% (230/418) | 84.0% (701/835) | 63.5% (431/679) | 69.7% (2617/3754) |
| A+B | alacsony_arany [arany] | 62.5% (145/232) | 38.7% (67/173) | 87.7% (455/519) | 53.0% (114/215) | 68.6% (781/1139) |
| A+B+C | arany_versek | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| A+B+C | magas_pontossag | 95.4% (83/87) | 93.4% (99/106) | 90.6% (58/64) | 97.0% (98/101) | 94.4% (338/358) |
| A+B+C | pontossag_osszes (tajekoztato) | 93.7% (283/302) | 92.6% (151/163) | 92.4% (256/277) | 92.9% (299/322) | 93.0% (989/1064) |
| A+B+C | lefedettseg | 89.3% (283/317) | 98.7% (151/153) | 96.2% (256/266) | 94.9% (299/315) | 94.1% (989/1051) |
| A+B+C | regi_arany_kizaras_nelkul | 87.5% (28/32) | — (0/0) | — (0/0) | — (0/0) | 87.5% (28/32) |
| A+B+C | regi_arany_kizarassal_tajekoztato | 90.3% (28/31) | — (0/0) | — (0/0) | — (0/0) | 90.3% (28/31) |
| A+B+C | alacsony_arany [200 vers] | 57.4% (963/1677) | 34.0% (124/365) | 75.3% (469/623) | 64.0% (530/828) | 59.7% (2086/3493) |
| A+B+C | alacsony_arany [arany] | 62.3% (188/302) | 17.2% (28/163) | 74.0% (205/277) | 60.6% (195/322) | 57.9% (616/1064) |

(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3b.tsv, 90%; a bootstrap egysége a köteg — DT21 f: elfogadva, felhasználói döntés):

- A (F1V2): 22.84 USD [22.04–23.62]
- B (F2V2): 5.12 USD [4.27–6.01]
- C (F3V2): 42.03 USD [38.16–46.27]
- C (F3V2B): 42.03 USD [38.06–46.49]
- A+B: 27.96 USD [26.74–29.15]
- A+B+C: 85.91 USD [79.60–92.63]

## b) Minősítés (csak A+B és A+B+C; a többi PD6 szerint nem minősíthető)

| összeállítás | feltétel | eredmény | megjegyzés |
|---|---|---|---|
| A+B | feltetel_1 | nem teljesül |  |
| A+B | feltetel_2 | nem teljesül |  |
| A+B | feltetel_3 | nem teljesül |  |
| A+B | feltetel_3_tajekoztato | nem teljesül |  |
| A+B | feltetel_4 | teljesül |  |
| A+B | feltetel_5 | nem teljesül |  |
| A+B | minosites (kizárás nélküli régi arannyal) | nem felel meg | bukott feltétel: 1, 2, 3, 5; nem mért: — |
| A+B | minosites (tájékoztató: 1Móz 6:17 kizárva) | nem felel meg | bukott feltétel: 1, 2, 3_tajekoztato, 5; nem mért: — |
| A+B+C | feltetel_1 | nem teljesül |  |
| A+B+C | feltetel_2 | nem teljesül |  |
| A+B+C | feltetel_3 | nem teljesül |  |
| A+B+C | feltetel_3_tajekoztato | nem teljesül |  |
| A+B+C | feltetel_4 | nem teljesül |  |
| A+B+C | feltetel_5 | nem teljesül |  |
| A+B+C | minosites (kizárás nélküli régi arannyal) | nem felel meg | bukott feltétel: 1, 2, 3, 4, 5; nem mért: — |
| A+B+C | minosites (tájékoztató: 1Móz 6:17 kizárva) | nem felel meg | bukott feltétel: 1, 2, 3_tajekoztato, 4, 5; nem mért: — |

| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5) | megjegyzés |
|---|---|---|---|
| A+B | R1 | nem teljesül | bukott: 1, 2, 3, 5; (3) mért |
| A+B | R2 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B | R3 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B | R4 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R1 | nem teljesül | bukott: 1, 2, 3, 5; (3) mért |
| A+B+C | R2 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R3 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R4 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |

## c) Bizonyossági szintek (A+B, A+B+C)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A+B | kozepes_pontossag | — (0/0) | — (0/0) | — (0/0) | — (0/0) | — (0/0) |
| A+B | alacsony_pontossag | 43.4% (63/145) | 38.8% (26/67) | 43.3% (197/455) | 47.4% (54/114) | 43.5% (340/781) |
| A+B | eloszlas_magas [200 vers] | 31.1% (567/1822) | 45.0% (188/418) | 16.0% (134/835) | 36.5% (248/679) | 30.3% (1137/3754) |
| A+B | eloszlas_kozepes [200 vers] | 0.0% (0/1822) | 0.0% (0/418) | 0.0% (0/835) | 0.0% (0/679) | 0.0% (0/3754) |
| A+B | eloszlas_alacsony [200 vers] | 68.9% (1255/1822) | 55.0% (230/418) | 84.0% (701/835) | 63.5% (431/679) | 69.7% (2617/3754) |
| A+B | eloszlas_magas [arany] | 37.5% (87/232) | 61.3% (106/173) | 12.3% (64/519) | 47.0% (101/215) | 31.4% (358/1139) |
| A+B | eloszlas_kozepes [arany] | 0.0% (0/232) | 0.0% (0/173) | 0.0% (0/519) | 0.0% (0/215) | 0.0% (0/1139) |
| A+B | eloszlas_alacsony [arany] | 62.5% (145/232) | 38.7% (67/173) | 87.7% (455/519) | 53.0% (114/215) | 68.6% (781/1139) |
| A+B | kimenet_nelkuli_versek [200 vers] | 20.0% (20/100) | 4.0% (1/25) | 20.0% (5/25) | 22.0% (11/50) | 18.5% (37/200) |
| A+B | kimenet_nelkuli_versek [arany] | 40.0% (8/20) | 10.0% (1/10) | 0.0% (0/10) | 40.0% (8/20) | 28.3% (17/60) |
| A+B+C | kozepes_pontossag | 81.5% (22/27) | 86.2% (25/29) | 62.5% (5/8) | 69.2% (18/26) | 77.8% (70/90) |
| A+B+C | alacsony_pontossag | 94.7% (178/188) | 96.4% (27/28) | 94.1% (193/205) | 93.8% (183/195) | 94.3% (581/616) |
| A+B+C | eloszlas_magas [200 vers] | 33.8% (567/1677) | 51.5% (188/365) | 21.5% (134/623) | 30.0% (248/828) | 32.6% (1137/3493) |
| A+B+C | eloszlas_kozepes [200 vers] | 8.8% (147/1677) | 14.5% (53/365) | 3.2% (20/623) | 6.0% (50/828) | 7.7% (270/3493) |
| A+B+C | eloszlas_alacsony [200 vers] | 57.4% (963/1677) | 34.0% (124/365) | 75.3% (469/623) | 64.0% (530/828) | 59.7% (2086/3493) |
| A+B+C | eloszlas_magas [arany] | 28.8% (87/302) | 65.0% (106/163) | 23.1% (64/277) | 31.4% (101/322) | 33.6% (358/1064) |
| A+B+C | eloszlas_kozepes [arany] | 8.9% (27/302) | 17.8% (29/163) | 2.9% (8/277) | 8.1% (26/322) | 8.5% (90/1064) |
| A+B+C | eloszlas_alacsony [arany] | 62.3% (188/302) | 17.2% (28/163) | 74.0% (205/277) | 60.6% (195/322) | 57.9% (616/1064) |
| A+B+C | kimenet_nelkuli_versek [200 vers] | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| A+B+C | kimenet_nelkuli_versek [arany] | 0.0% (0/20) | 0.0% (0/10) | 0.0% (0/10) | 0.0% (0/20) | 0.0% (0/60) |

## d) A meres.py P4-mérőszámai a v2-adaton (A=F1V2, B=F2V2, C=F3V2, arany v2)

### pontosság és lefedettség

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A | arany_versek_kapun_atment | 60.0% (12/20) | 90.0% (9/10) | 30.0% (3/10) | 55.0% (11/20) | 58.3% (35/60) |
| A | pontossag | 85.5% (118/138) | 81.7% (103/126) | 79.5% (58/73) | 81.2% (121/149) | 82.3% (400/486) |
| A | lefedettseg | 73.8% (118/160) | 81.7% (103/126) | 87.9% (58/66) | 80.7% (121/150) | 79.7% (400/502) |
| B | arany_versek_kapun_atment | 50.0% (10/20) | 90.0% (9/10) | 100.0% (10/10) | 50.0% (10/20) | 65.0% (39/60) |
| B | pontossag | 61.3% (111/181) | 79.1% (121/153) | 50.0% (255/510) | 77.2% (129/167) | 60.9% (616/1011) |
| B | lefedettseg | 87.4% (111/127) | 96.0% (121/126) | 95.9% (255/266) | 90.8% (129/142) | 93.2% (616/661) |
| C | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C | pontossag | 94.0% (299/318) | 95.6% (153/160) | 94.2% (259/275) | 91.7% (309/337) | 93.6% (1020/1090) |
| C | lefedettseg | 94.3% (299/317) | 100.0% (153/153) | 97.4% (259/266) | 98.1% (309/315) | 97.1% (1020/1051) |
| A+B magas (A∩B) | arany_versek_kapun_atment | 50.0% (10/20) | 90.0% (9/10) | 30.0% (3/10) | 45.0% (9/20) | 51.7% (31/60) |
| A+B magas (A∩B) | pontossag | 95.4% (83/87) | 93.4% (99/106) | 90.6% (58/64) | 97.0% (98/101) | 94.4% (338/358) |
| A+B magas (A∩B) | lefedettseg | 65.4% (83/127) | 78.6% (99/126) | 87.9% (58/66) | 77.2% (98/127) | 75.8% (338/446) |
| A∪B (döntőbíró előtti felső korlát) | arany_versek_kapun_atment | 50.0% (10/20) | 90.0% (9/10) | 30.0% (3/10) | 45.0% (9/20) | 51.7% (31/60) |
| A∪B (döntőbíró előtti felső korlát) | pontossag | 58.5% (117/200) | 72.3% (125/173) | 56.5% (65/115) | 67.8% (118/174) | 64.2% (425/662) |
| A∪B (döntőbíró előtti felső korlát) | lefedettseg | 92.1% (117/127) | 99.2% (125/126) | 98.5% (65/66) | 92.9% (118/127) | 95.3% (425/446) |

### A–B egyezés

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A–B | versek_mindketto_atment | 52.0% (52/100) | 72.0% (18/25) | 28.0% (7/25) | 42.0% (21/50) | 49.0% (98/200) |
| A–B | link_egyezes (uniós arány) | 47.7% (567/1189) | 58.4% (188/322) | 63.8% (134/210) | 65.4% (248/379) | 54.1% (1137/2100) |
| A–B | azonos_linkhalmazu_versek | 9.6% (5/52) | 0.0% (0/18) | 0.0% (0/7) | 9.5% (2/21) | 7.1% (7/98) |

### A+B összeállítás, döntőbíróhoz menő versek

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A+B | mindketto_atment_azonos_linkekkel | 5.0% (5/100) | 0.0% (0/25) | 0.0% (0/25) | 4.0% (2/50) | 3.5% (7/200) |
| A+B | mindketto_atment_eltero_linkekkel | 47.0% (47/100) | 72.0% (18/25) | 28.0% (7/25) | 38.0% (19/50) | 45.5% (91/200) |
| A+B | csak_A_atment | 3.0% (3/100) | 0.0% (0/25) | 0.0% (0/25) | 30.0% (15/50) | 9.0% (18/200) |
| A+B | csak_B_atment | 25.0% (25/100) | 24.0% (6/25) | 52.0% (13/25) | 6.0% (3/50) | 23.5% (47/200) |
| A+B | egyik_sem_atment | 20.0% (20/100) | 4.0% (1/25) | 20.0% (5/25) | 22.0% (11/50) | 18.5% (37/200) |
| A+B | dontobirohoz_menne (eltero + csak egyik + egyik sem) | 95.0% (95/100) | 100.0% (25/25) | 100.0% (25/25) | 96.0% (48/50) | 96.5% (193/200) |
| A+B | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| A+B | nem_egyezo_link_arany (1 − A∩B/A∪B) | 52.3% (622/1189) | 41.6% (134/322) | 36.2% (76/210) | 34.6% (131/379) | 45.9% (963/2100) |

### KJV-hatás (F1V2/F2V2 vs F5V2/F6V2, R1)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-val (F1V2/F2V2) A | kapuhiba_vegleg | 45.0% (45/100) | — | — | — | — |
| KJV-val (F1V2/F2V2) A | kapuhiba_elso_probara | 80.0% (80/100) | — | — | — | — |
| KJV-val (F1V2/F2V2) B | kapuhiba_vegleg | 23.0% (23/100) | — | — | — | — |
| KJV-val (F1V2/F2V2) B | kapuhiba_elso_probara | 61.0% (61/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) A (KJV nélkül) | kapuhiba_vegleg | 48.0% (48/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) A (KJV nélkül) | kapuhiba_elso_probara | 72.0% (72/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) B (KJV nélkül) | kapuhiba_vegleg | 24.0% (24/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) B (KJV nélkül) | kapuhiba_elso_probara | 57.0% (57/100) | — | — | — | — |
| A KJV-val | arany_versek [saját halmaz (kapun átment)] | 60.0% (12/20) | — | — | — | — |
| A KJV-val | pontossag [saját halmaz (kapun átment)] | 85.5% (118/138) | — | — | — | — |
| A KJV-val | lefedettseg [saját halmaz (kapun átment)] | 73.8% (118/160) | — | — | — | — |
| A KJV-val | arany_versek [közös halmaz (mindkét feltételben átment)] | 40.0% (8/20) | — | — | — | — |
| A KJV-val | pontossag [közös halmaz (mindkét feltételben átment)] | 81.8% (72/88) | — | — | — | — |
| A KJV-val | lefedettseg [közös halmaz (mindkét feltételben átment)] | 69.2% (72/104) | — | — | — | — |
| A KJV nélkül | arany_versek [saját halmaz (kapun átment)] | 55.0% (11/20) | — | — | — | — |
| A KJV nélkül | pontossag [saját halmaz (kapun átment)] | 76.8% (129/168) | — | — | — | — |
| A KJV nélkül | lefedettseg [saját halmaz (kapun átment)] | 86.6% (129/149) | — | — | — | — |
| A KJV nélkül | arany_versek [közös halmaz (mindkét feltételben átment)] | 40.0% (8/20) | — | — | — | — |
| A KJV nélkül | pontossag [közös halmaz (mindkét feltételben átment)] | 73.1% (87/119) | — | — | — | — |
| A KJV nélkül | lefedettseg [közös halmaz (mindkét feltételben átment)] | 83.7% (87/104) | — | — | — | — |
| B KJV-val | arany_versek [saját halmaz (kapun átment)] | 50.0% (10/20) | — | — | — | — |
| B KJV-val | pontossag [saját halmaz (kapun átment)] | 61.3% (111/181) | — | — | — | — |
| B KJV-val | lefedettseg [saját halmaz (kapun átment)] | 87.4% (111/127) | — | — | — | — |
| B KJV-val | arany_versek [közös halmaz (mindkét feltételben átment)] | 50.0% (10/20) | — | — | — | — |
| B KJV-val | pontossag [közös halmaz (mindkét feltételben átment)] | 61.3% (111/181) | — | — | — | — |
| B KJV-val | lefedettseg [közös halmaz (mindkét feltételben átment)] | 87.4% (111/127) | — | — | — | — |
| B KJV nélkül | arany_versek [saját halmaz (kapun átment)] | 100.0% (20/20) | — | — | — | — |
| B KJV nélkül | pontossag [saját halmaz (kapun átment)] | 70.8% (276/390) | — | — | — | — |
| B KJV nélkül | lefedettseg [saját halmaz (kapun átment)] | 87.1% (276/317) | — | — | — | — |
| B KJV nélkül | arany_versek [közös halmaz (mindkét feltételben átment)] | 50.0% (10/20) | — | — | — | — |
| B KJV nélkül | pontossag [közös halmaz (mindkét feltételben átment)] | 63.7% (109/171) | — | — | — | — |
| B KJV nélkül | lefedettseg [közös halmaz (mindkét feltételben átment)] | 85.8% (109/127) | — | — | — | — |
| KJV-val (F1V2/F2V2) | A–B_versek [saját halmaz (A és B átment)] | 52.0% (52/100) | — | — | — | — |
| KJV-val (F1V2/F2V2) | A–B_egyezes [saját halmaz (A és B átment)] | 47.7% (567/1189) | — | — | — | — |
| KJV-val (F1V2/F2V2) | A–B_versek [közös halmaz (mind a négy átment)] | 27.0% (27/100) | — | — | — | — |
| KJV-val (F1V2/F2V2) | A–B_egyezes [közös halmaz (mind a négy átment)] | 41.7% (282/676) | — | — | — | — |
| KJV-val (F1V2/F2V2) | magas (A∩B) arany_versek [közös halmaz] | 35.0% (7/20) | — | — | — | — |
| KJV-val (F1V2/F2V2) | magas (A∩B) pontossag [közös halmaz] | 93.7% (59/63) | — | — | — | — |
| KJV-val (F1V2/F2V2) | magas (A∩B) lefedettseg [közös halmaz] | 64.1% (59/92) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | A–B_versek [saját halmaz (A és B átment)] | 41.0% (41/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | A–B_egyezes [saját halmaz (A és B átment)] | 62.1% (489/788) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | A–B_versek [közös halmaz (mind a négy átment)] | 27.0% (27/100) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | A–B_egyezes [közös halmaz (mind a négy átment)] | 64.8% (300/463) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | magas (A∩B) arany_versek [közös halmaz] | 35.0% (7/20) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | magas (A∩B) pontossag [közös halmaz] | 78.0% (71/91) | — | — | — | — |
| KJV nélkül (F5V2/F6V2) | magas (A∩B) lefedettseg [közös halmaz] | 77.2% (71/92) | — | — | — | — |
| KJV-val − KJV nélkül | delta_magas_pontossag_szazalekpont [közös halmaz] | 15.63 | — | — | — | — |
| KJV-val vs KJV nélkül | A–B_eltérés_relativ_csokkenes [közös halmaz (mind a négy átment)] | -65.56 | — | — | — | — |
| KJV-val vs KJV nélkül | A–B_eltérés_relativ_csokkenes [saját halmaz (A és B átment)] | -37.87 | — | — | — | — |

## e) A C két futása (F3V2 vs F3V2B, azonos prompt): futásközi ingadozás

A két futás konfigurációja azonos (prompt_v2, C, 200 vers), ezért a különbség a futásközi ingadozás becslése (egyetlen futáspárból; a bootstrap a versminta bizonytalanságát adja hozzá, a futás többszöri megismétlésének eloszlását nem helyettesíti).

| réteg | mérőszám | F3V2 | F3V2B | Δ | Δ 90% | |Δ| 95. percentilis | n |
|---|---|---|---|---|---|---|---|
| R1 | pontossag | 94.03% | 93.83% | -0.20 pp | [-2.46; +1.88] | 2.61 pp | 20 |
| R1 | lefedettseg | 94.32% | 95.90% | +1.58 pp | [-1.88; +4.59] | 4.65 pp | 20 |
| R1 | kapuhiba_elso_probara | 12.00% | 21.00% | +9.00 pp | [+3.00; +15.00] | 15.00 pp | 100 |
| R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 100 |
| R2 | pontossag | 95.63% | 95.60% | -0.03 pp | [-2.56; +3.60] | 3.62 pp | 10 |
| R2 | lefedettseg | 100.00% | 99.35% | -0.65 pp | [-1.87; +0.00] | 1.87 pp | 10 |
| R2 | kapuhiba_elso_probara | 0.00% | 20.00% | +20.00 pp | [+8.00; +32.00] | 32.00 pp | 25 |
| R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| R3 | pontossag | 94.18% | 93.93% | -0.25 pp | [-1.87; +1.06] | 1.87 pp | 10 |
| R3 | lefedettseg | 97.37% | 98.87% | +1.50 pp | [+0.34; +2.88] | 2.88 pp | 10 |
| R3 | kapuhiba_elso_probara | 8.00% | 4.00% | -4.00 pp | [-12.00; +0.00] | 12.00 pp | 25 |
| R3 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 25 |
| R4 | pontossag | 91.69% | 90.27% | -1.43 pp | [-3.66; +0.79] | 3.66 pp | 20 |
| R4 | lefedettseg | 98.10% | 97.14% | -0.95 pp | [-2.14; +0.00] | 2.14 pp | 20 |
| R4 | kapuhiba_elso_probara | 10.00% | 2.00% | -8.00 pp | [-16.00; +0.00] | 16.00 pp | 50 |
| R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 50 |
| Összes | pontossag | 93.58% | 93.01% | -0.57 pp | [-1.64; +0.53] | 1.64 pp | 60 |
| Összes | lefedettseg | 97.05% | 97.53% | +0.48 pp | [-0.62; +1.60] | 1.61 pp | 60 |
| Összes | kapuhiba_elso_probara | 9.50% | 14.00% | +4.50 pp | [+0.50; +8.50] | 8.50 pp | 200 |
| Összes | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp | 200 |

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V2 vs F3V2B | azonos_linkhalmazu_versek [arany] | 45.0% (9/20) | 60.0% (6/10) | 30.0% (3/10) | 30.0% (6/20) | 40.0% (24/60) |
| F3V2 vs F3V2B | link_egyezes [arany] | 89.4% (303/339) | 93.3% (154/165) | 93.4% (268/287) | 93.1% (326/350) | 92.1% (1051/1141) |
| F3V2 vs F3V2B | azonos_linkhalmazu_versek [minta] | 44.0% (44/100) | 56.0% (14/25) | 44.0% (11/25) | 38.0% (19/50) | 44.0% (88/200) |
| F3V2 vs F3V2B | link_egyezes [minta] | 92.1% (1692/1837) | 94.3% (346/367) | 94.6% (614/649) | 93.1% (810/870) | 93.0% (3462/3723) |

## f) Kapuhiba: v1 és v2 egymás mellett, hibatípusok kapupont szerint

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A v1 (F1) | elso_probara | 71.0% (71/100) | 76.0% (19/25) | 96.0% (24/25) | 76.0% (38/50) | 76.0% (152/200) |
| A v1 (F1) | vegleg | 42.0% (42/100) | 32.0% (8/25) | 40.0% (10/25) | 44.0% (22/50) | 41.0% (82/200) |
| A v2 (F1V2) | elso_probara | 80.0% (80/100) | 88.0% (22/25) | 92.0% (23/25) | 70.0% (35/50) | 80.0% (160/200) |
| A v2 (F1V2) | vegleg | 45.0% (45/100) | 28.0% (7/25) | 72.0% (18/25) | 28.0% (14/50) | 42.0% (84/200) |
| B v1 (F2) | elso_probara | 80.0% (80/100) | 8.0% (2/25) | 52.0% (13/25) | 22.0% (11/50) | 53.0% (106/200) |
| B v1 (F2) | vegleg | 68.0% (68/100) | 0.0% (0/25) | 36.0% (9/25) | 10.0% (5/50) | 41.0% (82/200) |
| B v2 (F2V2) | elso_probara | 61.0% (61/100) | 60.0% (15/25) | 96.0% (24/25) | 82.0% (41/50) | 70.5% (141/200) |
| B v2 (F2V2) | vegleg | 23.0% (23/100) | 4.0% (1/25) | 20.0% (5/25) | 52.0% (26/50) | 27.5% (55/200) |
| C v1 (F3) | elso_probara | 17.0% (17/100) | 0.0% (0/25) | 20.0% (5/25) | 16.0% (8/50) | 15.0% (30/200) |
| C v1 (F3) | vegleg | 1.0% (1/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.5% (1/200) |
| C v2 (F3V2) | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 8.0% (2/25) | 10.0% (5/50) | 9.5% (19/200) |
| C v2 (F3V2) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | elso_probara | 21.0% (21/100) | 20.0% (5/25) | 4.0% (1/25) | 2.0% (1/50) | 14.0% (28/200) |
| C (2. futás) v2 (F3V2B) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| A KJV nélkül v1 (F5) | elso_probara | 75.0% (75/100) | — | — | — | 75.0% (75/100) |
| A KJV nélkül v1 (F5) | vegleg | 31.0% (31/100) | — | — | — | 31.0% (31/100) |
| A KJV nélkül v2 (F5V2) | elso_probara | 72.0% (72/100) | — | — | — | 72.0% (72/100) |
| A KJV nélkül v2 (F5V2) | vegleg | 48.0% (48/100) | — | — | — | 48.0% (48/100) |
| B KJV nélkül v1 (F6) | elso_probara | 23.0% (23/100) | — | — | — | 23.0% (23/100) |
| B KJV nélkül v1 (F6) | vegleg | 13.0% (13/100) | — | — | — | 13.0% (13/100) |
| B KJV nélkül v2 (F6V2) | elso_probara | 57.0% (57/100) | — | — | — | 57.0% (57/100) |
| B KJV nélkül v2 (F6V2) | vegleg | 24.0% (24/100) | — | — | — | 24.0% (24/100) |
| C döntőbíró v2 (F4V2) | elso_probara | 25.3% (24/95) | 48.0% (12/25) | 4.0% (1/25) | 8.3% (4/48) | 21.2% (41/193) |
| C döntőbíró v2 (F4V2) | vegleg | 0.0% (0/95) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/48) | 0.0% (0/193) |

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A v1 (F1) | kapupont_1-json_elso | — | — | — | — | 50.0% (100/200) |
| A v1 (F1) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/200) |
| A v1 (F1) | kapupont_2_elso | — | — | — | — | 1.5% (3/200) |
| A v1 (F1) | kapupont_2_vegleg | — | — | — | — | 6.5% (13/200) |
| A v1 (F1) | kapupont_3_elso | — | — | — | — | 23.5% (47/200) |
| A v1 (F1) | kapupont_3_vegleg | — | — | — | — | 32.5% (65/200) |
| A v1 (F1) | kapupont_4_elso | — | — | — | — | 7.5% (15/200) |
| A v1 (F1) | kapupont_4_vegleg | — | — | — | — | 18.5% (37/200) |
| A v2 (F1V2) | kapupont_1-json_elso | — | — | — | — | 45.0% (90/200) |
| A v2 (F1V2) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/200) |
| A v2 (F1V2) | kapupont_2_elso | — | — | — | — | 3.0% (6/200) |
| A v2 (F1V2) | kapupont_2_vegleg | — | — | — | — | 3.0% (6/200) |
| A v2 (F1V2) | kapupont_3_elso | — | — | — | — | 29.5% (59/200) |
| A v2 (F1V2) | kapupont_3_vegleg | — | — | — | — | 28.5% (57/200) |
| A v2 (F1V2) | kapupont_4_elso | — | — | — | — | 16.0% (32/200) |
| A v2 (F1V2) | kapupont_4_vegleg | — | — | — | — | 21.0% (42/200) |
| A v2 (F1V2) | kapupont_1_elso | — | — | — | — | 0.0% (0/200) |
| A v2 (F1V2) | kapupont_1_vegleg | — | — | — | — | 4.5% (9/200) |
| B v1 (F2) | kapupont_1-json_elso | — | — | — | — | 20.0% (40/200) |
| B v1 (F2) | kapupont_1-json_vegleg | — | — | — | — | 20.0% (40/200) |
| B v1 (F2) | kapupont_2_elso | — | — | — | — | 5.0% (10/200) |
| B v1 (F2) | kapupont_2_vegleg | — | — | — | — | 6.5% (13/200) |
| B v1 (F2) | kapupont_3_elso | — | — | — | — | 11.5% (23/200) |
| B v1 (F2) | kapupont_3_vegleg | — | — | — | — | 10.0% (20/200) |
| B v1 (F2) | kapupont_4_elso | — | — | — | — | 9.0% (18/200) |
| B v1 (F2) | kapupont_4_vegleg | — | — | — | — | 6.0% (12/200) |
| B v1 (F2) | kapupont_1-hianyzo_vers_elso | — | — | — | — | 9.0% (18/200) |
| B v1 (F2) | kapupont_1-hianyzo_vers_vegleg | — | — | — | — | 0.0% (0/200) |
| B v2 (F2V2) | kapupont_1-json_elso | — | — | — | — | 55.0% (110/200) |
| B v2 (F2V2) | kapupont_1-json_vegleg | — | — | — | — | 5.0% (10/200) |
| B v2 (F2V2) | kapupont_2_elso | — | — | — | — | 1.5% (3/200) |
| B v2 (F2V2) | kapupont_2_vegleg | — | — | — | — | 1.0% (2/200) |
| B v2 (F2V2) | kapupont_3_elso | — | — | — | — | 5.5% (11/200) |
| B v2 (F2V2) | kapupont_3_vegleg | — | — | — | — | 6.5% (13/200) |
| B v2 (F2V2) | kapupont_4_elso | — | — | — | — | 4.5% (9/200) |
| B v2 (F2V2) | kapupont_4_vegleg | — | — | — | — | 6.5% (13/200) |
| B v2 (F2V2) | kapupont_1-hianyzo_vers_elso | — | — | — | — | 4.5% (9/200) |
| B v2 (F2V2) | kapupont_1-hianyzo_vers_vegleg | — | — | — | — | 10.0% (20/200) |
| C v1 (F3) | kapupont_1-json_elso | — | — | — | — | 5.0% (10/200) |
| C v1 (F3) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/200) |
| C v1 (F3) | kapupont_2_elso | — | — | — | — | 0.5% (1/200) |
| C v1 (F3) | kapupont_2_vegleg | — | — | — | — | 0.0% (0/200) |
| C v1 (F3) | kapupont_3_elso | — | — | — | — | 0.5% (1/200) |
| C v1 (F3) | kapupont_3_vegleg | — | — | — | — | 0.0% (0/200) |
| C v1 (F3) | kapupont_4_elso | — | — | — | — | 2.5% (5/200) |
| C v1 (F3) | kapupont_4_vegleg | — | — | — | — | 0.5% (1/200) |
| C v1 (F3) | kapupont_1_elso | — | — | — | — | 7.5% (15/200) |
| C v1 (F3) | kapupont_1_vegleg | — | — | — | — | 0.0% (0/200) |
| C v2 (F3V2) | kapupont_1-json_elso | — | — | — | — | 5.0% (10/200) |
| C v2 (F3V2) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/200) |
| C v2 (F3V2) | kapupont_3_elso | — | — | — | — | 0.5% (1/200) |
| C v2 (F3V2) | kapupont_3_vegleg | — | — | — | — | 0.0% (0/200) |
| C v2 (F3V2) | kapupont_4_elso | — | — | — | — | 2.0% (4/200) |
| C v2 (F3V2) | kapupont_4_vegleg | — | — | — | — | 0.0% (0/200) |
| C v2 (F3V2) | kapupont_1_elso | — | — | — | — | 2.5% (5/200) |
| C v2 (F3V2) | kapupont_1_vegleg | — | — | — | — | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | kapupont_1-json_elso | — | — | — | — | 10.0% (20/200) |
| C (2. futás) v2 (F3V2B) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | kapupont_3_elso | — | — | — | — | 0.5% (1/200) |
| C (2. futás) v2 (F3V2B) | kapupont_3_vegleg | — | — | — | — | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | kapupont_4_elso | — | — | — | — | 0.5% (1/200) |
| C (2. futás) v2 (F3V2B) | kapupont_4_vegleg | — | — | — | — | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | kapupont_1_elso | — | — | — | — | 3.0% (6/200) |
| C (2. futás) v2 (F3V2B) | kapupont_1_vegleg | — | — | — | — | 0.0% (0/200) |
| A KJV nélkül v1 (F5) | kapupont_1-json_elso | — | — | — | — | 30.0% (30/100) |
| A KJV nélkül v1 (F5) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/100) |
| A KJV nélkül v1 (F5) | kapupont_2_elso | — | — | — | — | 5.0% (5/100) |
| A KJV nélkül v1 (F5) | kapupont_2_vegleg | — | — | — | — | 9.0% (9/100) |
| A KJV nélkül v1 (F5) | kapupont_3_elso | — | — | — | — | 38.0% (38/100) |
| A KJV nélkül v1 (F5) | kapupont_3_vegleg | — | — | — | — | 19.0% (19/100) |
| A KJV nélkül v1 (F5) | kapupont_4_elso | — | — | — | — | 20.0% (20/100) |
| A KJV nélkül v1 (F5) | kapupont_4_vegleg | — | — | — | — | 16.0% (16/100) |
| A KJV nélkül v1 (F5) | kapupont_1_elso | — | — | — | — | 0.0% (0/100) |
| A KJV nélkül v1 (F5) | kapupont_1_vegleg | — | — | — | — | 2.0% (2/100) |
| A KJV nélkül v2 (F5V2) | kapupont_1-json_elso | — | — | — | — | 50.0% (50/100) |
| A KJV nélkül v2 (F5V2) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/100) |
| A KJV nélkül v2 (F5V2) | kapupont_2_elso | — | — | — | — | 3.0% (3/100) |
| A KJV nélkül v2 (F5V2) | kapupont_2_vegleg | — | — | — | — | 4.0% (4/100) |
| A KJV nélkül v2 (F5V2) | kapupont_3_elso | — | — | — | — | 18.0% (18/100) |
| A KJV nélkül v2 (F5V2) | kapupont_3_vegleg | — | — | — | — | 42.0% (42/100) |
| A KJV nélkül v2 (F5V2) | kapupont_4_elso | — | — | — | — | 8.0% (8/100) |
| A KJV nélkül v2 (F5V2) | kapupont_4_vegleg | — | — | — | — | 20.0% (20/100) |
| B KJV nélkül v1 (F6) | kapupont_3_elso | — | — | — | — | 7.0% (7/100) |
| B KJV nélkül v1 (F6) | kapupont_3_vegleg | — | — | — | — | 3.0% (3/100) |
| B KJV nélkül v1 (F6) | kapupont_4_elso | — | — | — | — | 11.0% (11/100) |
| B KJV nélkül v1 (F6) | kapupont_4_vegleg | — | — | — | — | 2.0% (2/100) |
| B KJV nélkül v1 (F6) | kapupont_1_elso | — | — | — | — | 8.0% (8/100) |
| B KJV nélkül v1 (F6) | kapupont_1_vegleg | — | — | — | — | 8.0% (8/100) |
| B KJV nélkül v2 (F6V2) | kapupont_1-json_elso | — | — | — | — | 50.0% (50/100) |
| B KJV nélkül v2 (F6V2) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/100) |
| B KJV nélkül v2 (F6V2) | kapupont_4_elso | — | — | — | — | 7.0% (7/100) |
| B KJV nélkül v2 (F6V2) | kapupont_4_vegleg | — | — | — | — | 4.0% (4/100) |
| B KJV nélkül v2 (F6V2) | kapupont_1-hianyzo_vers_elso | — | — | — | — | 0.0% (0/100) |
| B KJV nélkül v2 (F6V2) | kapupont_1-hianyzo_vers_vegleg | — | — | — | — | 20.0% (20/100) |
| C döntőbíró v2 (F4V2) | kapupont_1-json_elso | — | — | — | — | 10.4% (20/193) |
| C döntőbíró v2 (F4V2) | kapupont_1-json_vegleg | — | — | — | — | 0.0% (0/193) |
| C döntőbíró v2 (F4V2) | kapupont_3_elso | — | — | — | — | 1.0% (2/193) |
| C döntőbíró v2 (F4V2) | kapupont_3_vegleg | — | — | — | — | 0.0% (0/193) |
| C döntőbíró v2 (F4V2) | kapupont_4_elso | — | — | — | — | 0.5% (1/193) |
| C döntőbíró v2 (F4V2) | kapupont_4_vegleg | — | — | — | — | 0.0% (0/193) |
| C döntőbíró v2 (F4V2) | kapupont_1_elso | — | — | — | — | 2.1% (4/193) |
| C döntőbíró v2 (F4V2) | kapupont_1_vegleg | — | — | — | — | 0.0% (0/193) |
| C döntőbíró v2 (F4V2) | kapupont_6_elso | — | — | — | — | 7.3% (14/193) |
| C döntőbíró v2 (F4V2) | kapupont_6_vegleg | — | — | — | — | 0.0% (0/193) |

A döntőbírói futás (F4V2) első próbás kapuhibája a teljes kapun számolva: ötpontos kapu + 6. pont (az A–B rögzítés, futtat.biro_kenyszer), ahogy a futtató a futáskor ellenőrizte.

| futás | keresztellenőrzés (első próbás hibás versek) |
|---|---|
| A v1 (F1) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (152) = napló kapuhiba_db(probalkozas=1) összeg (152): EGYEZIK |
| A v2 (F1V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (160) = napló kapuhiba_db(probalkozas=1) összeg (160): EGYEZIK |
| B v1 (F2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (106) = napló kapuhiba_db(probalkozas=1) összeg (106): EGYEZIK |
| B v2 (F2V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (141) = napló kapuhiba_db(probalkozas=1) összeg (141): EGYEZIK |
| C v1 (F3) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (30) = napló kapuhiba_db(probalkozas=1) összeg (30): EGYEZIK |
| C v2 (F3V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (19) = napló kapuhiba_db(probalkozas=1) összeg (19): EGYEZIK |
| C (2. futás) v2 (F3V2B) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (28) = napló kapuhiba_db(probalkozas=1) összeg (28): EGYEZIK |
| A KJV nélkül v1 (F5) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (75) = napló kapuhiba_db(probalkozas=1) összeg (75): EGYEZIK |
| A KJV nélkül v2 (F5V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (72) = napló kapuhiba_db(probalkozas=1) összeg (72): EGYEZIK |
| B KJV nélkül v1 (F6) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (23) = napló kapuhiba_db(probalkozas=1) összeg (23): EGYEZIK |
| B KJV nélkül v2 (F6V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (57) = napló kapuhiba_db(probalkozas=1) összeg (57): EGYEZIK |
| C döntőbíró v2 (F4V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (41) = napló kapuhiba_db(probalkozas=1) összeg (41): EGYEZIK |

| futás | mentett válaszok újraellenőrzése (hibák) |
|---|---|
| F1V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F2V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F3V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F3V2B | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F4V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F5V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| F6V2 | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |

