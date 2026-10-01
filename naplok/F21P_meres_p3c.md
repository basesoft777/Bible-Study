# F21P_meres_p3c.md — P4 a regressziós mérésre (P3c): Sonnet, Sonnet+C, C (F3V3) a v2-es C-futásokkal

<!-- GENERÁLT: eszkozok/karoli_strong/meres_p3c.py | scope=P3c (prompt_v3): Sonnet egyedül (SONNETV3), C (F3V3) a v2-es két C-futással (F3V2, F3V2B), Sonnet+C pár (A=SONNETV3, B=F3V3, döntőbíró nélkül), a Sonnet gondolkodási kerete, length-lezárásai, végleges kapuhibái és a kapupont-bontás (F21.80), 200 verses minta, arany v3 (60 vers, sha256 acdeb55f969c96fe) | forras=f21p/valaszok/{SONNETV3,F3V3,F3V2,F3V2B}.jsonl, arany_opus_v3.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, f21p/koltseg_vetites_p3c.tsv | ts=2026-10-01T09:33:35+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

Kizárólag szkriptkimenet. Az összeállítások: Sonnet egyedül (SONNETV3), C egyedül (F3V3), Sonnet+C pár (A = Sonnet, B = C F3V3-futása, mindkettő prompt_v3; A∩B = magas, döntőbíró nélkül; az egyik oldal kapuhibája: a vers minden linkje alacsony és beleszámít az alacsony arányba). Egymodelles összeállítás (Sonnet, C) nem minősíthető (PD6): az alacsony arány n.é. Az A/B/C/Sonnet beállítása eltérő (PD15: a C minimal, kötelező; a Sonnet minimális gondolkodási kerettel, temperature nélkül, nem determinisztikus; az A és a B kikapcsolva). Cellaforma: érték (számláló/nevező). A mérés az arany **v3** változatára megy (60 vers).

## a) Az öt feltétel összeállításonként és rétegenként

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| Sonnet (SONNETV3) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 0.0% (0/10) | 100.0% (20/20) | 83.3% (50/60) |
| Sonnet (SONNETV3) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| Sonnet (SONNETV3) | pontossag_osszes (tajekoztato, PD6) | 96.9% (308/318) | 99.3% (149/150) | — (0/0) | 96.8% (301/311) | 97.3% (758/779) |
| Sonnet (SONNETV3) | lefedettseg | 97.2% (308/317) | 98.0% (149/152) | — (0/0) | 95.9% (301/314) | 96.8% (758/783) |
| Sonnet (SONNETV3) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| Sonnet (SONNETV3) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| Sonnet (SONNETV3) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V3) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C (F3V3) | magas_pontossag | n.é. | n.é. | n.é. | n.é. | n.é. |
| C (F3V3) | pontossag_osszes (tajekoztato, PD6) | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 94.4% (306/324) | 95.3% (1009/1059) |
| C (F3V3) | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.5% (306/314) | 96.3% (1009/1048) |
| C (F3V3) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C (F3V3) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| C (F3V3) | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |
| Sonnet+C | arany_versek | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| Sonnet+C | magas_pontossag | 98.3% (291/296) | 99.3% (149/150) | — (0/0) | 98.7% (294/298) | 98.7% (734/744) |
| Sonnet+C | pontossag_osszes (tajekoztato) | 95.1% (313/329) | 96.2% (152/158) | 94.4% (255/270) | 92.9% (313/337) | 94.4% (1033/1094) |
| Sonnet+C | lefedettseg | 98.7% (313/317) | 100.0% (152/152) | 96.2% (255/265) | 99.7% (313/314) | 98.6% (1033/1048) |
| Sonnet+C | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| Sonnet+C | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| Sonnet+C | alacsony_arany [200 vers] | 12.0% (219/1822) | 11.2% (42/374) | 55.9% (347/621) | 10.7% (92/856) | 19.1% (700/3673) |
| Sonnet+C | alacsony_arany [arany] | 10.0% (33/329) | 5.1% (8/158) | 100.0% (270/270) | 11.6% (39/337) | 32.0% (350/1094) |

(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3c.tsv, 90%; a bootstrap egysége a köteg):

- Sonnet (SONNETV3): 373.94 USD [337.97–418.65]
- C (F3V3): 42.49 USD [38.55–46.52]
- Sonnet+C: 416.43 USD [379.88–460.97]

## b) Minősítés (csak a Sonnet+C pár; az egymodelles összeállítás PD6 szerint nem minősíthető)

| összeállítás | feltétel | eredmény | megjegyzés |
|---|---|---|---|
| Sonnet+C | feltetel_1 | nem mérhető | 0/0 magas link: R3 (PD19 (1)) |
| Sonnet+C | feltetel_2 | teljesül |  |
| Sonnet+C | feltetel_3 | nem teljesül |  |
| Sonnet+C | feltetel_3_tajekoztato | teljesül |  |
| Sonnet+C | feltetel_4 | nem teljesül |  |
| Sonnet+C | feltetel_5 | nem teljesül |  |
| Sonnet+C | minosites (kizárás nélküli régi arannyal) | nem felel meg | bukott feltétel: 3, 4, 5; nem mért: —; nem mérhető: 1 |
| Sonnet+C | minosites (tájékoztató: 1Móz 6:17 kizárva) | nem felel meg | bukott feltétel: 4, 5; nem mért: —; nem mérhető: 1 |

| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5) | megjegyzés |
|---|---|---|---|
| Sonnet+C | R1 | nem teljesül | bukott: 3, 5; (3) mért |
| Sonnet+C | R2 | nem teljesül | bukott: 5; (3) n.é. (nincs régi arany a rétegben) |
| Sonnet+C | R3 | nem teljesül | bukott: 5; (3) n.é. (nincs régi arany a rétegben); (1) nem mérhető (0/0 magas link, PD19 (1)) |
| Sonnet+C | R4 | nem teljesül | bukott: 5; (3) n.é. (nincs régi arany a rétegben) |

## c) A Sonnet+C pár bizonyossági szintjei és versosztályai

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| Sonnet+C | kozepes_pontossag | — (0/0) | — (0/0) | — (0/0) | — (0/0) | — (0/0) |
| Sonnet+C | alacsony_pontossag | 66.7% (22/33) | 37.5% (3/8) | 94.4% (255/270) | 48.7% (19/39) | 85.4% (299/350) |
| Sonnet+C | eloszlas_magas [200 vers] | 88.0% (1603/1822) | 88.8% (332/374) | 44.1% (274/621) | 89.3% (764/856) | 80.9% (2973/3673) |
| Sonnet+C | eloszlas_kozepes [200 vers] | 0.0% (0/1822) | 0.0% (0/374) | 0.0% (0/621) | 0.0% (0/856) | 0.0% (0/3673) |
| Sonnet+C | eloszlas_alacsony [200 vers] | 12.0% (219/1822) | 11.2% (42/374) | 55.9% (347/621) | 10.7% (92/856) | 19.1% (700/3673) |
| Sonnet+C | eloszlas_magas [arany] | 90.0% (296/329) | 94.9% (150/158) | 0.0% (0/270) | 88.4% (298/337) | 68.0% (744/1094) |
| Sonnet+C | eloszlas_kozepes [arany] | 0.0% (0/329) | 0.0% (0/158) | 0.0% (0/270) | 0.0% (0/337) | 0.0% (0/1094) |
| Sonnet+C | eloszlas_alacsony [arany] | 10.0% (33/329) | 5.1% (8/158) | 100.0% (270/270) | 11.6% (39/337) | 32.0% (350/1094) |
| Sonnet+C | kimenet_nelkuli_versek [200 vers] | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| Sonnet+C | kimenet_nelkuli_versek [arany] | 0.0% (0/20) | 0.0% (0/10) | 0.0% (0/10) | 0.0% (0/20) | 0.0% (0/60) |

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| Sonnet+C | mindketto_atment_azonos_linkekkel | 31.0% (31/100) | 36.0% (9/25) | 20.0% (5/25) | 30.0% (15/50) | 30.0% (60/200) |
| Sonnet+C | mindketto_atment_eltero_linkekkel | 69.0% (69/100) | 64.0% (16/25) | 32.0% (8/25) | 70.0% (35/50) | 64.0% (128/200) |
| Sonnet+C | csak_Sonnet_atment | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 0.0% (0/50) | 1.0% (2/200) |
| Sonnet+C | csak_C_atment | 0.0% (0/100) | 0.0% (0/25) | 40.0% (10/25) | 0.0% (0/50) | 5.0% (10/200) |
| Sonnet+C | egyik_sem_atment | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| Sonnet+C | versek_mindketto_atment | 100.0% (100/100) | 100.0% (25/25) | 52.0% (13/25) | 100.0% (50/50) | 94.0% (188/200) |
| Sonnet+C | link_egyezes (uniós arány) | 88.0% (1603/1822) | 88.8% (332/374) | 93.5% (274/293) | 89.3% (764/856) | 88.9% (2973/3345) |
| Sonnet+C | azonos_linkhalmazu_versek | 31.0% (31/100) | 36.0% (9/25) | 38.5% (5/13) | 30.0% (15/50) | 31.9% (60/188) |

## d) A C három futása egymás mellett (F3V2, F3V2B: prompt_v2; F3V3: prompt_v3) és a Sonnet

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
| Sonnet (SONNETV3) | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 0.0% (0/10) | 100.0% (20/20) | 83.3% (50/60) |
| Sonnet (SONNETV3) | pontossag_osszes (tajekoztato, PD6) | 96.9% (308/318) | 99.3% (149/150) | — (0/0) | 96.8% (301/311) | 97.3% (758/779) |
| Sonnet (SONNETV3) | lefedettseg | 97.2% (308/317) | 98.0% (149/152) | — (0/0) | 95.9% (301/314) | 96.8% (758/783) |
| Sonnet (SONNETV3) | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| Sonnet (SONNETV3) | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |

### Kapuhiba első próbára és végleg; hibatípusok kapupont szerint (hibás versek száma a 200-ból)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V2) | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 8.0% (2/25) | 10.0% (5/50) | 9.5% (19/200) |
| C (F3V2) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V2B) | elso_probara | 21.0% (21/100) | 20.0% (5/25) | 4.0% (1/25) | 2.0% (1/50) | 14.0% (28/200) |
| C (F3V2B) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V3) | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 40.0% (10/25) | 16.0% (8/50) | 15.0% (30/200) |
| C (F3V3) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 0.0% (0/50) | 1.0% (2/200) |
| Sonnet (SONNETV3) | elso_probara | 3.0% (3/100) | 0.0% (0/25) | 40.0% (10/25) | 0.0% (0/50) | 6.5% (13/200) |
| Sonnet (SONNETV3) | vegleg | 0.0% (0/100) | 0.0% (0/25) | 40.0% (10/25) | 0.0% (0/50) | 5.0% (10/200) |

| futás | kapupont | hibás versek (n a 200) |
|---|---|---|
| C (F3V2) | kapupont_1-json_elso | 10/200 |
| C (F3V2) | kapupont_1-json_vegleg | 0/200 |
| C (F3V2) | kapupont_3_elso | 1/200 |
| C (F3V2) | kapupont_3_vegleg | 0/200 |
| C (F3V2) | kapupont_4_elso | 4/200 |
| C (F3V2) | kapupont_4_vegleg | 0/200 |
| C (F3V2) | kapupont_1_elso | 5/200 |
| C (F3V2) | kapupont_1_vegleg | 0/200 |
| C (F3V2B) | kapupont_1-json_elso | 20/200 |
| C (F3V2B) | kapupont_1-json_vegleg | 0/200 |
| C (F3V2B) | kapupont_3_elso | 1/200 |
| C (F3V2B) | kapupont_3_vegleg | 0/200 |
| C (F3V2B) | kapupont_4_elso | 1/200 |
| C (F3V2B) | kapupont_4_vegleg | 0/200 |
| C (F3V2B) | kapupont_1_elso | 6/200 |
| C (F3V2B) | kapupont_1_vegleg | 0/200 |
| C (F3V3) | kapupont_1-json_elso | 20/200 |
| C (F3V3) | kapupont_1-json_vegleg | 0/200 |
| C (F3V3) | kapupont_3_elso | 1/200 |
| C (F3V3) | kapupont_3_vegleg | 0/200 |
| C (F3V3) | kapupont_4_elso | 2/200 |
| C (F3V3) | kapupont_4_vegleg | 2/200 |
| C (F3V3) | kapupont_1_elso | 7/200 |
| C (F3V3) | kapupont_1_vegleg | 0/200 |
| C (F3V3) | kapupont_2_elso | 1/200 |
| C (F3V3) | kapupont_2_vegleg | 0/200 |
| Sonnet (SONNETV3) | kapupont_1-json_elso | 10/200 |
| Sonnet (SONNETV3) | kapupont_1-json_vegleg | 10/200 |
| Sonnet (SONNETV3) | kapupont_3_elso | 1/200 |
| Sonnet (SONNETV3) | kapupont_3_vegleg | 0/200 |
| Sonnet (SONNETV3) | kapupont_4_elso | 2/200 |
| Sonnet (SONNETV3) | kapupont_4_vegleg | 0/200 |

| futás | keresztellenőrzés (első próbás hibás versek) |
|---|---|
| Sonnet (SONNETV3) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (13) = napló kapuhiba_db(probalkozas=1) összeg (13): EGYEZIK |
| C (F3V3) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (30) = napló kapuhiba_db(probalkozas=1) összeg (30): EGYEZIK |
| C (F3V2) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (19) = napló kapuhiba_db(probalkozas=1) összeg (19): EGYEZIK |
| C (F3V2B) | újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (28) = napló kapuhiba_db(probalkozas=1) összeg (28): EGYEZIK |

| futás | mentett válaszok újraellenőrzése (hibák) |
|---|---|
| Sonnet (SONNETV3) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C (F3V3) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C (F3V2) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |
| C (F3V2B) | 0 — futtat.mentett_valaszok_ellenoriz: 0 hiba |

### Költség és beállítás futásonként (a futásnaplóból)

| futás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| Sonnet (SONNETV3) | hivasok | 22 | próbálkozás=1: 20, próbálkozás=2: 2 |
| Sonnet (SONNETV3) | bemeneti_token | 231707 |  |
| Sonnet (SONNETV3) | kimeneti_token | 173414 | a completion_tokens (a gondolkodási token benne van, ha a modell jelenti) |
| Sonnet (SONNETV3) | koltseg_usd | 2.197554 | koltseg_forras: openrouter |
| Sonnet (SONNETV3) | gondolkodas_mod | reasoning_max_tokens=1024 | a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva |
| Sonnet (SONNETV3) | prompt_sha256_12 | 84f12ca7aafb |  |
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

## e) A prompt_v2 → v3 hatás (F3V3 a két v2-futáshoz képest) és a futásközi ingadozás

Δ = F3V3 − a v2-futás(ok) átlaga; a 90%-os intervallum a versek bootstrapje (rétegenként rétegzett, 1000 újramintavétel). Az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|). „kívül”: |Δ| > az ingadozás ÉS az intervallum nem tartalmazza a 0-t (leíró jelölés, nem próba).

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

### Páronkénti összevetések

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

## f) A Sonnet futása: a gondolkodási keret, a length-lezárások, a végleges kapuhibák (F21.80)

### (i) A gondolkodási keret: a modell nem tartotta be

- A konfigurált keret: reasoning.max_tokens = 1024 (gondolkodas_mod: reasoning_max_tokens=1024).
- Mért gondolkodási token összesen: 142077 a 173414 kimeneti tokenből (81.9%); hívásonként a legnagyobb 11144 (min 0, medián 6642, 22 hívás).
- A keret fölötti hívások: 21 a 22-ből; a legnagyobb a keret 10.9-szerese.
- A költségre: a gondolkodási token a kimeneti táblaáron 1.420770 USD (10.00 USD/1M; anthropic/claude-sonnet-5.5) a mért összköltséghez (64.7%).
- A length-lezárások: 2 a 22 hívásból (finish_reason=length: köteg 15 / próba 1, köteg 15 / próba 2; költségük 0.291850 USD; kimenet 12000+12000 token, ebből gondolkodás 11144+10364): a kimenet elérte a max_tokens-t, és nagyobb részét a gondolkodási token adta; a köteg versei véglegesen kapuhibásak maradtak (alább).

| köteg / próba | gondolkodási token / kimeneti token | megjegyzés |
|---|---|---|
| köteg 01 / próba 1 | 5109 / 6581 | keret 1024 (×5.0); finish_reason=stop; költség 0.087068 USD; versek 10, kapuhiba_db 0 |
| köteg 02 / próba 1 | 7408 / 9046 | keret 1024 (×7.2); finish_reason=stop; költség 0.113354 USD; versek 10, kapuhiba_db 0 |
| köteg 03 / próba 1 | 6471 / 8159 | keret 1024 (×6.3); finish_reason=stop; költség 0.104944 USD; versek 10, kapuhiba_db 0 |
| köteg 04 / próba 1 | 9085 / 10881 | keret 1024 (×8.9); finish_reason=stop; költség 0.133302 USD; versek 10, kapuhiba_db 0 |
| köteg 05 / próba 1 | 9207 / 11011 | keret 1024 (×9.0); finish_reason=stop; költség 0.134836 USD; versek 10, kapuhiba_db 0 |
| köteg 06 / próba 1 | 6193 / 7798 | keret 1024 (×6.0); finish_reason=stop; költség 0.100114 USD; versek 10, kapuhiba_db 0 |
| köteg 07 / próba 1 | 0 / 1514 | keret 1024 (×0.0); finish_reason=stop; költség 0.037494 USD; versek 10, kapuhiba_db 3 |
| köteg 07 / próba 2 | 2040 / 2539 | keret 1024 (×2.0); finish_reason=stop; költség 0.051352 USD; versek 3, kapuhiba_db 0 |
| köteg 08 / próba 1 | 5503 / 6603 | keret 1024 (×5.4); finish_reason=stop; költség 0.083426 USD; versek 10, kapuhiba_db 0 |
| köteg 09 / próba 1 | 4291 / 5477 | keret 1024 (×4.2); finish_reason=stop; költség 0.073012 USD; versek 10, kapuhiba_db 0 |
| köteg 10 / próba 1 | 4601 / 5780 | keret 1024 (×4.5); finish_reason=stop; költség 0.076060 USD; versek 10, kapuhiba_db 0 |
| köteg 11 / próba 1 | 4227 / 5387 | keret 1024 (×4.1); finish_reason=stop; költség 0.070132 USD; versek 10, kapuhiba_db 0 |
| köteg 12 / próba 1 | 3564 / 4894 | keret 1024 (×3.5); finish_reason=stop; költség 0.067222 USD; versek 10, kapuhiba_db 0 |
| köteg 13 / próba 1 | 9260 / 10868 | keret 1024 (×9.0); finish_reason=stop; költség 0.128712 USD; versek 10, kapuhiba_db 0 |
| köteg 14 / próba 1 | 9624 / 11458 | keret 1024 (×9.4); finish_reason=stop; költség 0.136624 USD; versek 10, kapuhiba_db 0 |
| köteg 15 / próba 1 | 11144 / 12000 | keret 1024 (×10.9); finish_reason=length; költség 0.144404 USD; versek 10, kapuhiba_db 10 |
| köteg 15 / próba 2 | 10364 / 12000 | keret 1024 (×10.1); finish_reason=length; költség 0.147446 USD; versek 10, kapuhiba_db 10 |
| köteg 16 / próba 1 | 7002 / 8376 | keret 1024 (×6.8); finish_reason=stop; költség 0.101588 USD; versek 10, kapuhiba_db 0 |
| köteg 17 / próba 1 | 6642 / 8050 | keret 1024 (×6.5); finish_reason=stop; költség 0.098924 USD; versek 10, kapuhiba_db 0 |
| köteg 18 / próba 1 | 7067 / 8703 | keret 1024 (×6.9); finish_reason=stop; költség 0.107100 USD; versek 10, kapuhiba_db 0 |
| köteg 19 / próba 1 | 5581 / 7020 | keret 1024 (×5.5); finish_reason=stop; költség 0.088348 USD; versek 10, kapuhiba_db 0 |
| köteg 20 / próba 1 | 7694 / 9269 | keret 1024 (×7.5); finish_reason=stop; költség 0.112092 USD; versek 10, kapuhiba_db 0 |

| futás | mérőszám | érték | nevező | megjegyzés |
|---|---|---|---|---|
| Sonnet (SONNETV3) | gondolkodasi_token | 142077 | 173414 | a kimeneti tokenből (completion_tokens) a modell által jelentett gondolkodási token (futásnapló) |
| Sonnet (SONNETV3) | gondolkodasi_token_hivasonkent_max | 11144 |  | min 0, medián 6642, 22 hívás |
| Sonnet (SONNETV3) | finish_reason | length: 2, stop: 20 |  |  |
| Sonnet (SONNETV3) | gondolkodasi_token_koltsege_usd | 1.420770 | 2.197554 | a gondolkodási token × a kimeneti táblaár (10.00 USD/1M; anthropic/claude-sonnet-5.5) a mért összköltséghez (64.7%) |
| Sonnet (SONNETV3) | keret_feletti_hivasok | 21 | 22 | a konfigurált keret (reasoning.max_tokens=1024) fölötti mért gondolkodási token hívásonként; a legnagyobb a keret 10.9-szerese |
| Sonnet (SONNETV3) | length_hivasok | 2 | 22 | finish_reason=length: köteg 15 / próba 1, köteg 15 / próba 2; költségük 0.291850 USD; kimenet 12000+12000 token, ebből gondolkodás 11144+10364 |
| C (F3V3) | gondolkodasi_token | 0 | 30719 | a kimeneti tokenből (completion_tokens) a modell által jelentett gondolkodási token (futásnapló) |
| C (F3V3) | gondolkodasi_token_hivasonkent_max | 0 |  | min 0, medián 0, 26 hívás |
| C (F3V3) | finish_reason | stop: 26 |  |  |
| C (F3V3) | gondolkodasi_token_koltsege_usd | 0.000000 | 0.260136 | a gondolkodási token × a kimeneti táblaár (3.75 USD/1M; google/gemini-3.8-flash) a mért összköltséghez (0.0%) |
| C (F3V2) | gondolkodasi_token | 0 | 29470 | a kimeneti tokenből (completion_tokens) a modell által jelentett gondolkodási token (futásnapló) |
| C (F3V2) | gondolkodasi_token_hivasonkent_max | 0 |  | min 0, medián 0, 26 hívás |
| C (F3V2) | finish_reason | stop: 26 |  |  |
| C (F3V2) | gondolkodasi_token_koltsege_usd | 0.000000 | 0.256731 | a gondolkodási token × a kimeneti táblaár (3.75 USD/1M; google/gemini-3.8-flash) a mért összköltséghez (0.0%) |
| C (F3V2B) | gondolkodasi_token | 0 | 30888 | a kimeneti tokenből (completion_tokens) a modell által jelentett gondolkodási token (futásnapló) |
| C (F3V2B) | gondolkodasi_token_hivasonkent_max | 0 |  | min 0, medián 0, 26 hívás |
| C (F3V2B) | finish_reason | stop: 26 |  |  |
| C (F3V2B) | gondolkodasi_token_koltsege_usd | 0.000000 | 0.256110 | a gondolkodási token × a kimeneti táblaár (3.75 USD/1M; google/gemini-3.8-flash) a mért összköltséghez (0.0%) |

### (ii) Beállítás-eltérés és determinizmus

- Sonnet (SONNETV3): a Sonnet-kérés temperature nélkül ment, gondolkodással: a futás nem determinisztikus (egyetlen futás, ingadozás-becslés nincs).
- F21 pilot: az A és a B gondolkodás nélkül; a C kötelező minimális gondolkodással (kotelezo_effort=minimal); a Sonnet minimális gondolkodási kerettel (reasoning.max_tokens=1024), amelyet a modell nem tartott be (l. gondolkodas).

### A Sonnet véglegesen kapuhibás versei (10)

| réteg | vers | végső kapupont | köteg | hívások \| végső hiba |
|---|---|---|---|---|
| R3 | Jer 46:21 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Jer 51:3 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 11:3 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 16:57 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 22:25 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 30:5 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 33:31 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 39:13 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 41:2 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |
| R3 | Ez 46:12 | 1-json | köteg 15 | hívások: próba 1: finish_reason=length, kimenet 12000 (gondolkodás 11144); próba 2: finish_reason=length, kimenet 12000 (gondolkodás 10364) \| végső hiba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 2252 (char 2251) \| aranyvers |

## g) A minősítés részletezése (az (1) 0/0 rétege „nem mérhető”, PD19 (1); a küszöb szempontjából csak a mért érték számít)

| feltétel | réteg | érték | megjegyzés |
|---|---|---|---|
| feltetel_1_magas_pontossag | R1 | 98.3% (291/296) | ≥ 98%: teljesül |
| feltetel_1_magas_pontossag | R2 | 99.3% (149/150) | ≥ 98%: teljesül |
| feltetel_1_magas_pontossag | R3 | — (0/0) | nincs magas link a rétegben (0/0): nem mérhető (PD19 (1); a Sonnet R3-aranyversei a 15. köteg length-lezárása miatt végleg kapuhibásak; a próféták előtt pótolandó, pótló futás most nincs) |
| feltetel_1_magas_pontossag | R4 | 98.7% (294/298) | ≥ 98%: teljesül |
| feltetel_5_alacsony_arany_mert_200_vers | Összes | 19.1% (700/3673) | ≤ 10%: nem teljesül; a minősítés ezt használja (meres_p3b.minosit) |
| feltetel_5_alacsony_arany_vetitett | Összes | 21.4% | F22-rétegenként vetítve a teljes Bibliára (koltseg_vetites_p3c.tsv: 129049 / 602188 link); ≤ 10%: nem teljesül |
| feltetel_4_koltseg_felso90 | Összes | 460.97 | vetített 416.43 USD [90%: 379.88–460.97]; ≤ 60 USD: nem teljesül |

## h) Az első próbás kapuhiba kapupontonként és rétegenként: Sonnet és C (F3V3)

Módszer: a köteg nyers[0] válaszának újraellenőrzése a teljes kapun (meres._tipusok); keresztellenőrzés a rétegenkénti első-próbás számokkal, a jsonl probalkozas=2 verseivel és a napló kapuhiba_db(probalkozas=1) összegével.

| réteg | kapupont | Sonnet (SONNETV3) | C (F3V3) |
|---|---|---|---|
| R1 | hibas_versek_elso | 3/100 | 12/100 |
| R1 | kapupont_1_elso | 0/100 | 0/100 |
| R1 | kapupont_1-json_elso | 0/100 | 10/100 |
| R1 | kapupont_2_elso | 0/100 | 1/100 |
| R1 | kapupont_3_elso | 1/100 | 1/100 |
| R1 | kapupont_4_elso | 2/100 | 1/100 |
| R1 | tobb_kapupontos_versek_elso | 0/100 | 1/100 |
| R2 | hibas_versek_elso | 0/25 | 0/25 |
| R2 | kapupont_1_elso | 0/25 | 0/25 |
| R2 | kapupont_1-json_elso | 0/25 | 0/25 |
| R2 | kapupont_2_elso | 0/25 | 0/25 |
| R2 | kapupont_3_elso | 0/25 | 0/25 |
| R2 | kapupont_4_elso | 0/25 | 0/25 |
| R2 | tobb_kapupontos_versek_elso | 0/25 | 0/25 |
| R3 | hibas_versek_elso | 10/25 | 10/25 |
| R3 | kapupont_1_elso | 0/25 | 0/25 |
| R3 | kapupont_1-json_elso | 10/25 | 10/25 |
| R3 | kapupont_2_elso | 0/25 | 0/25 |
| R3 | kapupont_3_elso | 0/25 | 0/25 |
| R3 | kapupont_4_elso | 0/25 | 0/25 |
| R3 | tobb_kapupontos_versek_elso | 0/25 | 0/25 |
| R4 | hibas_versek_elso | 0/50 | 8/50 |
| R4 | kapupont_1_elso | 0/50 | 7/50 |
| R4 | kapupont_1-json_elso | 0/50 | 0/50 |
| R4 | kapupont_2_elso | 0/50 | 0/50 |
| R4 | kapupont_3_elso | 0/50 | 0/50 |
| R4 | kapupont_4_elso | 0/50 | 1/50 |
| R4 | tobb_kapupontos_versek_elso | 0/50 | 0/50 |
| Összes | hibas_versek_elso | 13/200 | 30/200 |
| Összes | kapupont_1_elso | 0/200 | 7/200 |
| Összes | kapupont_1-json_elso | 10/200 | 20/200 |
| Összes | kapupont_2_elso | 0/200 | 1/200 |
| Összes | kapupont_3_elso | 1/200 | 1/200 |
| Összes | kapupont_4_elso | 2/200 | 2/200 |
| Összes | tobb_kapupontos_versek_elso | 0/200 | 1/200 |

| futás | keresztellenőrzés (kapupont-bontás) |
|---|---|
| Sonnet (SONNETV3) | a kapupont-bontás hibás versei (13) = a kapuhiba-szakasz rétegenkénti első-próbás számai (R1: 3, R2: 0, R3: 10, R4: 0, Összes: 13) = jsonl probalkozas=2 versek (13) = napló kapuhiba_db(probalkozas=1) összeg (13): EGYEZIK |
| C (F3V3) | a kapupont-bontás hibás versei (30) = a kapuhiba-szakasz rétegenkénti első-próbás számai (R1: 12, R2: 0, R3: 10, R4: 8, Összes: 30) = jsonl probalkozas=2 versek (30) = napló kapuhiba_db(probalkozas=1) összeg (30): EGYEZIK |

| futás | réteg | vers | kapupont | köteg | első próba: hibaüzenet (röviden) \| végleg |
|---|---|---|---|---|---|
| Sonnet (SONNETV3) | R1 | 2Móz 38:8 | 4 | köteg 7 | első próba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: [20] \| végleg: átment (2. próba) |
| Sonnet (SONNETV3) | R1 | 2Móz 39:23 | 3 | köteg 7 | első próba: 3. ezek a magyar szavak többször szerepelnek (a "parok" bal oldalán vagy a "betoldas"-ban): [19] \| végleg: átment (2. próba) |
| Sonnet (SONNETV3) | R1 | 2Móz 39:26 | 4 | köteg 7 | első próba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: [7] \| végleg: átment (2. próba) |
| Sonnet (SONNETV3) | R3 | Jer 46:21 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Jer 51:3 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 11:3 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 16:57 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 22:25 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 30:5 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 33:31 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 39:13 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 41:2 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |
| Sonnet (SONNETV3) | R3 | Ez 46:12 | 1-json | köteg 15 | első próba: 1. a válasz nem érvényes JSON: Expecting ',' delimiter: line 1 column 1170 (char 1169) \| végleg: kapuhibás (kapupont 1-json) \| aranyvers |

