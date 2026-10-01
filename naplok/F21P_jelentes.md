# F21P_jelentes.md — Károli–Strong mérőpilot: záró jelentés (P6)

<!-- GENERÁLT: eszkozok/karoli_strong/jelentes_f21p.py | scope=F21 mérőpilot, P6 záró jelentés (A, B, C, A+B, A+B+C; R1–R4) | forras=f21p/meres_eredmeny.tsv, f21p/meres_v2_eredmeny.tsv, f21p/koltseg_vetites.tsv, f21p/ingadozas.tsv, f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/futasnaplo.tsv, f21p/minta.tsv, f21p/sorrend_eltero_versek.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/meres_p3b_eredmeny.tsv, f21p/koltseg_vetites_p3b.tsv, f21p/c_diff_f3v2b_besorolas.tsv, f21p/meres_p3c_eredmeny.tsv, f21p/koltseg_vetites_p3c.tsv, f21p/c_diff_p3c_besorolas.tsv, f21p/kjv_meres_eredmeny.tsv, f21p/elopar_kjv_eredmeny.tsv, f21p/meres_p3c_c_eredmeny.tsv | ts=2026-10-01T09:39:05+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

A számok kizárólag szkriptkimenetből jönnek (a forrás soronként jelölve). A **korrigált** értékek kizárólag „**Opus-besorolás, nem mérés**” jelöléssel szerepelnek; a küszöb szempontjából csak a mért érték számít (PD10). A jelentés nem ajánl döntést a #22-ről.

## A regressziós mérés (P3c, prompt_v3) — összefoglaló és végleges eredmény (F21.82)

Források: f21p/meres_p3c_eredmeny.tsv, f21p/koltseg_vetites_p3c.tsv, f21p/c_diff_p3c_besorolas.tsv, f21p/kjv_meres_eredmeny.tsv, f21p/elopar_kjv_eredmeny.tsv, f21p/meres_p3c_c_eredmeny.tsv; a régi P3/P3b-adat: f21p/meres_p3b_eredmeny.tsv, f21p/koltseg_vetites_p3b.tsv; a költség: f21p/futasnaplo.tsv. A P3c az arany **v3**-ra mér, a P3b az arany **v2**-re (a két arany 3 linkben tér el; l. naplok/F21P_meres_p3c_c.md). A korrigált értékek kizárólag „Opus-besorolás, nem mérés” jelöléssel; a küszöb szempontjából csak a mért érték számít.

### Végleges eredmény a Döntési szabály szerint: egyik összeállítás sem felel meg

- **A+B (P3b, prompt_v2, arany v2): nem felel meg** — bukott feltétel: 1, 2, 3, 5; nem mért: — (tájékoztató, 1Móz 6:17 nélkül: nem felel meg — bukott feltétel: 1, 2, 3_tajekoztato, 5; nem mért: —).
- **A+B+C (P3b, prompt_v2, arany v2): nem felel meg** — bukott feltétel: 1, 2, 3, 4, 5; nem mért: — (tájékoztató, 1Móz 6:17 nélkül: nem felel meg — bukott feltétel: 1, 2, 3_tajekoztato, 4, 5; nem mért: —).
- **Sonnet + C pár (P3c: A = SONNETV3, B = F3V3, prompt_v3, arany v3; döntőbíró nélkül): nem felel meg** — bukott feltétel: 3, 4, 5; nem mért: —; nem mérhető: 1 (tájékoztató, 1Móz 6:17 nélkül: nem felel meg — bukott feltétel: 4, 5; nem mért: —; nem mérhető: 1).
- A Sonnet + C pár (1) feltétele: **nem mérhető** (0/0 magas link: R3 (PD19 (1))): a Sonnet R3-aranyversei a 15. köteg length-lezárása miatt végleg kapuhibásak; a próféták előtt pótolandó, pótló futás most nincs (PD19 (1)).
- Az egymodelles összeállítások (A, B, C — F3V2, F3V2B, F3V3 —, Sonnet) a PD6 szerint nem minősíthetők; csak mért számaik vannak.

### (a) Az öt feltétel összeállításonként (Összes; az (1) rétegenként)

Feltételek: (1) `magas` pontosság ≥ 98% rétegenként; (2) lefedettség ≥ 95%; (3) régi arany ≥ 95% (mért = kizárás nélkül; tájékoztató = 1Móz 6:17 nélkül); (4) a vetített teljes költség 90%-os felső széle ≤ 60 USD; (5) `alacsony` arány ≤ 10% (a 200 versen mért link-arány; a Sonnet + C-nél a teljes Bibliára vetített is). Egymodelles összeállításnál az (1) helyén az összpontosság (tájékoztató, PD6), az (5) n.é.

| összeállítás | (1) magas pontosság R1 / R2 / R3 / R4 | (2) lefedettség | (3) régi arany: mért / tájékoztató | (4) költség USD [90%] | (5) alacsony | minősítés |
|---|---|---|---|---|---|---|
| A+B (P3b) | 95.4% (83/87) / 93.4% (99/106) / 90.6% (58/64) / 97.0% (98/101) | 64.5% (678/1051) | 56.2% (18/32) / 58.1% (18/31) | 27.9563 [26.7382–29.1534] | 69.7% (2617/3754) | nem felel meg (bukott feltétel: 1, 2, 3, 5; nem mért: —) |
| A+B+C (P3b) | 95.4% (83/87) / 93.4% (99/106) / 90.6% (58/64) / 97.0% (98/101) | 94.1% (989/1051) | 87.5% (28/32) / 90.3% (28/31) | 85.9074 [79.5981–92.6267] | 59.7% (2086/3493) | nem felel meg (bukott feltétel: 1, 2, 3, 4, 5; nem mért: —) |
| Sonnet + C (P3c) | 98.3% (291/296) / 99.3% (149/150) / — (0/0) / 98.7% (294/298) | 98.6% (1033/1048) | 93.8% (30/32) / 96.8% (30/31) | 416.4304 [379.8793–460.9697] | 19.1% (700/3673); vetítve 21.4% | nem felel meg (bukott feltétel: 3, 4, 5; nem mért: —; nem mérhető: 1) |
| A (F1V2, P3b) | n.é. (PD6); összpontosság 82.3% (400/486) | 79.7% (400/502) | 71.4% (10/14) / 76.9% (10/13) | 22.8359 [22.0403–23.6158] | n.é. (PD6) | nem minősíthető (PD6) |
| B (F2V2, P3b) | n.é. (PD6); összpontosság 60.9% (616/1011) | 93.2% (616/661) | 84.2% (16/19) / 88.9% (16/18) | 5.1204 [4.2687–6.0138] | n.é. (PD6) | nem minősíthető (PD6) |
| C (F3V2, P3b) | n.é. (PD6); összpontosság 93.6% (1020/1090) | 97.1% (1020/1051) | 93.8% (30/32) / 96.8% (30/31) | 42.0329 [38.1616–46.2746] | n.é. (PD6) | nem minősíthető (PD6) |
| C (F3V2B, P3b) | n.é. (PD6); összpontosság 93.0% (1025/1102) | 97.5% (1025/1051) | 93.8% (30/32) / 96.8% (30/31) | 42.0348 [38.057–46.494] | n.é. (PD6) | nem minősíthető (PD6) |
| C (F3V3, P3c) | n.é. (PD6); összpontosság 95.3% (1009/1059) | 96.3% (1009/1048) | 93.8% (30/32) / 96.8% (30/31) | 42.4899 [38.5542–46.5194] | n.é. (PD6) | nem minősíthető (PD6) |
| Sonnet (SONNETV3, P3c) | n.é. (PD6); összpontosság 97.3% (758/779) | 96.8% (758/783) | 93.8% (30/32) / 96.8% (30/31) | 373.9405 [337.9675–418.6543] | n.é. (PD6) | nem minősíthető (PD6) |

Egymodelles összeállításnál a lefedettség és a régi arany a kapun átment versekre vonatkozik (n a cellában); a Sonnet kapun átment aranyversei: 83.3% (50/60).

### (b) A C (F3V3) a v2-es C-futásokkal egymás mellett, arany v3 (meres_p3c_eredmeny.tsv)

| futás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| C (F3V2) | pontossag_osszes | 94.0% (299/318) | 95.0% (152/160) | 93.8% (258/275) | 91.4% (308/337) | 93.3% (1017/1090) |
| C (F3V2) | lefedettseg | 94.3% (299/317) | 100.0% (152/152) | 97.4% (258/265) | 98.1% (308/314) | 97.0% (1017/1048) |
| C (F3V2) | kapuhiba elso_probara | 12.0% (12/100) | 0.0% (0/25) | 8.0% (2/25) | 10.0% (5/50) | 9.5% (19/200) |
| C (F3V2) | kapuhiba vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V2B) | pontossag_osszes | 93.8% (304/324) | 95.0% (151/159) | 93.6% (262/280) | 90.3% (306/339) | 92.8% (1023/1102) |
| C (F3V2B) | lefedettseg | 95.9% (304/317) | 99.3% (151/152) | 98.9% (262/265) | 97.5% (306/314) | 97.6% (1023/1048) |
| C (F3V2B) | kapuhiba elso_probara | 21.0% (21/100) | 20.0% (5/25) | 4.0% (1/25) | 2.0% (1/50) | 14.0% (28/200) |
| C (F3V2B) | kapuhiba vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/200) |
| C (F3V3) | pontossag_osszes | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 94.4% (306/324) | 95.3% (1009/1059) |
| C (F3V3) | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.5% (306/314) | 96.3% (1009/1048) |
| C (F3V3) | kapuhiba elso_probara | 12.0% (12/100) | 0.0% (0/25) | 40.0% (10/25) | 16.0% (8/50) | 15.0% (30/200) |
| C (F3V3) | kapuhiba vegleg | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 0.0% (0/50) | 1.0% (2/200) |

A prompt_v2 → v3 hatás: Δ = F3V3 − a két v2-futás átlaga (azonos aranyon), 90%-os bootstrap a versek felett; az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|, azonos prompt); „kívül”: |Δ| > ingadozás ÉS az intervallum nem tartalmazza a 0-t (leíró jelölés, nem próba).

| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | ingadozás | jelölés |
|---|---|---|---|---|---|---|---|
| R1 | pontossag | 93.93% | 96.42% | +2.49 pp | [-0.10; +4.49] | 0.20 pp | az ingadozáson belül / a 0-t tartalmazza |
| R1 | lefedettseg | 95.11% | 93.38% | -1.74 pp | [-3.83; +0.51] | 1.58 pp | az ingadozáson belül / a 0-t tartalmazza |
| R2 | pontossag | 94.98% | 96.20% | +1.22 pp | [-0.75; +2.85] | 0.03 pp | az ingadozáson belül / a 0-t tartalmazza |
| R2 | lefedettseg | 99.67% | 100.00% | +0.33 pp | [+0.00; +0.94] | 0.66 pp | az ingadozáson belül / a 0-t tartalmazza |
| R3 | pontossag | 93.69% | 94.44% | +0.75 pp | [-1.84; +3.50] | 0.25 pp | az ingadozáson belül / a 0-t tartalmazza |
| R3 | lefedettseg | 98.11% | 96.23% | -1.89 pp | [-3.71; -0.43] | 1.51 pp | kívül az ingadozáson |
| R4 | pontossag | 90.83% | 94.44% | +3.61 pp | [+1.66; +5.71] | 1.13 pp | kívül az ingadozáson |
| R4 | lefedettseg | 97.77% | 97.45% | -0.32 pp | [-1.58; +0.91] | 0.64 pp | az ingadozáson belül / a 0-t tartalmazza |
| Összes | pontossag | 93.07% | 95.28% | +2.21 pp | [+1.01; +3.36] | 0.47 pp | kívül az ingadozáson |
| Összes | lefedettseg | 97.33% | 96.28% | -1.05 pp | [-1.88; -0.11] | 0.57 pp | kívül az ingadozáson |
| Összes | kapuhiba_elso_probara | 11.75% | 15.00% | +3.25 pp | [-0.50; +7.00] | 4.50 pp | az ingadozáson belül / a 0-t tartalmazza |
| Összes | kapuhiba_vegleg | 0.00% | 1.00% | +1.00 pp | [+0.00; +2.00] | 0.00 pp | az ingadozáson belül / a 0-t tartalmazza |

### (c) A Sonnet-futás (meres_p3c_eredmeny.tsv: koltseg, gondolkodas, vegleges_kapuhiba, jeloles)

- Költség: 2.197554 USD (22 hívás; próbálkozás=1: 20, próbálkozás=2: 2); bemenet 231707, kimenet 173414 token.
- A gondolkodási keret be nem tartása: 142077 gondolkodási token a 173414 kimeneti tokenből; hívásonként a legnagyobb 11144 (min 0, medián 6642, 22 hívás); a keret (reasoning.max_tokens = 1024) fölötti hívás 21 a 22-ből (a legnagyobb a keret 10.9-szerese). A gondolkodási token a kimeneti táblaáron 1.420770 USD a mért 2.197554 USD-ből.
- Length-lezárás: 2 a 22 hívásból — finish_reason=length: köteg 15 / próba 1, köteg 15 / próba 2; költségük 0.291850 USD; kimenet 12000+12000 token, ebből gondolkodás 11144+10364.
- A 10 végleges kapuhibás vers (köteg 15, végső kapupont 1-json): Jer 46:21 (R3, aranyvers), Jer 51:3 (R3, aranyvers), Ez 11:3 (R3, aranyvers), Ez 16:57 (R3, aranyvers), Ez 22:25 (R3, aranyvers), Ez 30:5 (R3, aranyvers), Ez 33:31 (R3, aranyvers), Ez 39:13 (R3, aranyvers), Ez 41:2 (R3, aranyvers), Ez 46:12 (R3, aranyvers).
- a Sonnet-kérés temperature nélkül ment, gondolkodással: a futás nem determinisztikus (egyetlen futás, ingadozás-becslés nincs)

### (d) A beállítás-eltérések jelölése

- F21 pilot: az A és a B gondolkodás nélkül; a C kötelező minimális gondolkodással (kotelezo_effort=minimal); a Sonnet minimális gondolkodási kerettel (reasoning.max_tokens=1024), amelyet a modell nem tartott be (l. gondolkodas).
- A gondolkodási mód futásonként (futásnapló): Sonnet (SONNETV3): reasoning_max_tokens=1024; C (F3V3): kotelezo_effort=minimal; C (F3V2): kotelezo_effort=minimal; C (F3V2B): kotelezo_effort=minimal.

### (e) P5: a teljes Biblia költsége összeállításonként (F22 műfaji öt réteg, köteg-bootstrap, 90%)

Az A, B, C (F3V2), A+B, A+B+C a P3b-vetítés (koltseg_vetites_p3b.tsv, prompt_v2); a C (F3V3), a Sonnet és a Sonnet + C a P3c-vetítés (koltseg_vetites_p3c.tsv, prompt_v3; a pár = a két futás vetítésének összege, döntőbíró nélkül). Az újrakérési szorzó (M) minden futásnál a saját mért adatból.

| összeállítás | ÓSZ-próza | költészet | próféta | evangélium+ApCsel | levél+Jel | Összes |
|---|---|---|---|---|---|---|
| A (F1V2) | 10.5772 [10.1633–10.9407] | 2.584 [2.4804–2.6958] | 4.285 [4.1149–4.4344] | 3.2495 [3.1405–3.3612] | 2.1403 [2.0691–2.214] | 22.8359 [22.0403–23.6158] |
| B (F2V2) | 2.2947 [1.9029–2.7044] | 0.6623 [0.5586–0.7829] | 0.9279 [0.7696–1.0945] | 0.7444 [0.6232–0.8733] | 0.4911 [0.4115–0.5759] | 5.1204 [4.2687–6.0138] |
| C (F3V2) | 19.2778 [17.4733–21.2438] | 4.9671 [4.536–5.4531] | 7.8015 [7.0728–8.6014] | 6.0195 [5.4711–6.6193] | 3.967 [3.6058–4.3622] | 42.0329 [38.1616–46.2746] |
| A+B | 12.8718 [12.2818–13.4151] | 3.2463 [3.0919–3.4163] | 5.2128 [4.9741–5.4321] | 3.9939 [3.8194–4.1659] | 2.6315 [2.5168–2.7445] | 27.9563 [26.7382–29.1534] |
| A+B+C | 39.2741 [36.4125–42.2582] | 10.1116 [9.3219–11.1173] | 16.2654 [15.0646–17.5362] | 11.9354 [10.7866–13.1005] | 8.3209 [7.7147–8.9708] | 85.9074 [79.5981–92.6267] |
| C (F3V3) | 19.4119 [17.5993–21.2688] | 5.0931 [4.6433–5.5672] | 7.8611 [7.122–8.6071] | 6.1018 [5.5418–6.6776] | 4.0219 [3.6528–4.4016] | 42.4899 [38.5542–46.5194] |
| Sonnet (SONNETV3) | 173.3934 [154.8944–194.3728] | 41.2015 [35.9178–46.7355] | 70.938 [63.3828–79.5027] | 53.3063 [48.1794–59.6705] | 35.1014 [31.7197–39.2959] | 373.9405 [337.9675–418.6543] |
| Sonnet+C | 192.8053 [174.3403–213.9392] | 46.2946 [40.7127–51.9994] | 78.7991 [71.2282–87.5053] | 59.4081 [54.1866–65.8666] | 39.1233 [35.6917–43.3607] | 416.4304 [379.8793–460.9697] |

Ellenőrzés a 200 versre (a konzervatívabb számít, DT21 g): Sonnet (SONNETV3) -0.446%; C (F3V3) -0.087%; Sonnet+C -0.408%.

### (f) A KJV-támpont

- A mérés (kjv_meres_eredmeny.tsv, F8V3 − F3V3, Összes): a pontosság Δ = +0.25 pp [90%: -0.84; +1.32], az ingadozás-becslés (F3V2B − F3V2) -0.47 pp: a mérés szerint nincs kimutatható hatás (az ingadozáson belül); a pilot döntése: „nem igazolt, a javított táblával újramérhető” (PD17 (3)).
- Az R4: „KJV nélkül, nem mérhető” (meres_p3c_c_eredmeny.tsv); a Károli ↔ KJV versmegfeleltetés zsoltár-eltolódása: N-F21 (NYITOTT_FELADATOK.md).
- Az előpárosítás KJV-szabálya („nincs KJV-tag → forditatlan-jelölt”; elopar_kjv_eredmeny.tsv, A) önállóan, Összes): pontosság 14.8% (22/149).

### (g) A (c) hibák újrabesorolása (Opus-besorolás, nem mérés; c_diff_p3c_besorolas.tsv, naplok/F21P_C_diff_p3c.md)

- C (F3V3), arany v3: a / b / c = 41 / 22 / 26; Sonnet (50 kapun átment aranyvers): 22 / 17 / 7; közös (c) eset: 1.
- A konvenciók hatása (a v2-es C-futások (c) eseteihez képest, DT21 a–e): l. (h).
- Olvasási korlátok: a besorolás az Opus kézi döntése, nem mérés; a Sonnet R3-a nincs benne (kapuhiba); az egyetlen v2-futásban (c) eset megszűnése a futásközi ingadozással is összefér; a korrigált értékek a küszöb szempontjából nem számítanak.

### (h) Nyitott és lezárt tételek

- A DT21 a–e a regressziós mérésben lezárva (segített = a v2 (c) eset megszűnt vagy átsorolódott; nem segített = maradt; ártott = új (c)): a) 2 / 0 / 0; b) 4 / 0 / 0; c) 4 / 0 / 0; d) 0 / 0 / 0; e) 3 / 0 / 0.
- „Arany-felülvizsgálatra jelölt” sor: 8 (C: 7, Sonnet: 1): 1Pét 4:11, Ez 22:25, Mt 21:4, Mt 23:31, Mt 6:31; a számokban (c), a 6. táblázat zárt (PD10).
- Az (1) feltétel R3-ja nem mérhető (a Sonnet R3-pótlása a próféták előtt; pótló futás most nincs).
- N-F21: a Károli ↔ KJV versmegfeleltetés zsoltár-eltolódása (most nem javítjuk; PD17 (1)).

### (i) A teljes pilot költsége (futásnapló, futásonként)

| szakasz | futás | hívás | költség USD | megjegyzés |
|---|---|---|---|---|
| P3 | F1 | 40 | 0.132718 |  |
| P3 | F2 | 37 | 0.017725 |  |
| P3 | F3 | 27 | 0.257251 |  |
| P3 | F5 | 20 | 0.060663 |  |
| P3 | F6 | 18 | 0.009506 |  |
| P3 | F3V2 | 26 | 0.256731 |  |
| **P3 összesen** | | | **0.734594** | |
| P3b | F1V2 | 40 | 0.137698 |  |
| P3b | F2V2 | 38 | 0.032072 |  |
| P3b | F5V2 | 20 | 0.072390 |  |
| P3b | F6V2 | 19 | 0.012887 |  |
| P3b | F3V2B | 26 | 0.256110 |  |
| P3b | F4V2 | 34 | 0.359316 |  |
| **P3b összesen** | | | **0.870473** | |
| P3c | F3V3 | 26 | 0.260136 |  |
| P3c | F8V3 | 23 | 0.262474 | ebből a véletlen helyi futás két kötege (1., 2.; naplok/F21_baleset_F8V3.md): 2 hívás, 0.023232 USD |
| P3c | SONNETV3 | 22 | 2.197554 |  |
| **P3c összesen** | | | **2.720164** | |
| **a pilot összesen** | | 416 | **4.325231** | a napló utolsó futó összege 4.325231: EGYEZIK |

A plafonok és a megállási küszöbök (felhasználói döntések): 3 USD (P3/P3b; 2 USD-s küszöb) → 4,00 USD, küszöb 3,90 (PD14 (2)) → 5,00 USD, küszöb 4,90 (PD18 (1)). A futó összeg legnagyobb értéke a naplóban 4.325231 USD: a 4,90-es küszöb és az 5,00-es plafon alatt.

*A lenti szakaszok a P3b- és a P3-adatot őrzik változatlanul (prompt_v2 / v1, arany v2 / v1).*

## P3b-eredmény (prompt_v2): minden összeállítás az arany v2-höz (forrás: meres_p3b_eredmeny.tsv, koltseg_vetites_p3b.tsv)

Futások: A = F1V2, B = F2V2, C = F3V2 és F3V2B (két futás), A+B+C döntőbíró = F4V2, KJV nélkül F5V2/F6V2 — mind prompt_v2. A G4 bizonyossági szabály szó szerint (F22 brief 22.6): magas = A∩B (a KJV-ellentmondás feltétele gépileg nem értelmezhető, n.é.); kozepes = a döntőbíró linkje A vagy B egyikében; alacsony = hármas eltérés, vagy a vers kapuhibás maradt (A vagy B végleg kapuhibás: a C válasza, minden link alacsony). Az A+B döntőbíró nélkül: A∩B magas, minden más link alacsony (a jelentés értelmezése). Egymodelles összeállítás (A, B, C) a PD6 szerint nem minősíthető, csak mért számokat kap.

### Összefoglaló (P3b)

- **A+B: nem felel meg** (bukott feltétel: 1, 2, 3, 5; nem mért: —; mért, a kizárás nélküli régi arannyal — DT21 i). Tájékoztató (az 1Móz 6:17 kizárásával, nem minősít): nem felel meg (bukott feltétel: 1, 2, 3_tajekoztato, 5; nem mért: —).
- **A+B+C: nem felel meg** (bukott feltétel: 1, 2, 3, 4, 5; nem mért: —; mért, a kizárás nélküli régi arannyal — DT21 i). Tájékoztató (az 1Móz 6:17 kizárásával, nem minősít): nem felel meg (bukott feltétel: 1, 2, 3_tajekoztato, 4, 5; nem mért: —).
- Az A, a B és a C egymodelles összeállítás: a PD6 szerint nem minősíthető.
- A Döntési szabály „Javaslat” pontjához (tények): rétegenként sem az A+B, sem az A+B+C nem teljesíti a rétegfeltételeket (l. lent), tehát a szabály szerinti eset: „egyik sem” — a bukott feltételek a táblákban.

### Az öt feltétel összeállításonként és rétegenként

Feltételek: (1) `magas` pontosság ≥ 98% rétegenként; (2) lefedettség ≥ 95%; (3) régi arany ≥ 95% (halmaz-definíció; a MÉRT érték a kizárás nélküli, a küszöb ehhez viszonyít — DT21 i; mellette TÁJÉKOZTATÓKÉNT az 1Móz 6:17 nélküli érték); (4) vetített költség 90%-os felső széle ≤ 60 USD (teljes Biblia; az „Összes” sor az F22 műfaji öt réteg szerinti vetítés, DT21 h; az R1–R4 sorokban a réteg része a korábbi pilot-4-réteges besorolás szerint, tájékoztató); (5) vetített `alacsony` arány ≤ 10% (link-arány a végső kimenetben; a 200 versen / az aranyon). Egymodelles összeállításnál az (1) és az (5) n.é. (PD6); az (1) helyén az összpontosság tájékoztatásul áll.

| összeállítás | réteg | (1) magas pontosság | (2) lefedettség | (3) régi arany: mért (kizárás nélkül) / tájékoztató (1Móz 6:17 nélkül) | (4) költség USD [90%] (Összes: F22; R1–R4: pilot-4, tájékoztató) | (5) alacsony: 200 vers / arany |
|---|---|---|---|---|---|---|
| A (F1V2) | R1 | n.é. (PD6); összpontosság: 85.5% (118/138) | 73.8% (118/160) | 71.4% (10/14) / 76.9% (10/13) | 11.2206 [10.7962–11.6113] | n.é. (PD6) |
| A (F1V2) | R2 | n.é. (PD6); összpontosság: 81.7% (103/126) | 81.7% (103/126) | — (0/0) / — (0/0) | 1.851 [1.7736–1.9335] | n.é. (PD6) |
| A (F1V2) | R3 | n.é. (PD6); összpontosság: 79.5% (58/73) | 87.9% (58/66) | — (0/0) / — (0/0) | 4.3735 [4.2019–4.5258] | n.é. (PD6) |
| A (F1V2) | R4 | n.é. (PD6); összpontosság: 81.2% (121/149) | 80.7% (121/150) | — (0/0) / — (0/0) | 5.3898 [5.2096–5.5752] | n.é. (PD6) |
| A (F1V2) | Összes | n.é. (PD6); összpontosság: 82.3% (400/486) | 79.7% (400/502) | 71.4% (10/14) / 76.9% (10/13) | 22.8359 [22.0403–23.6158] | n.é. (PD6) |
| B (F2V2) | R1 | n.é. (PD6); összpontosság: 61.3% (111/181) | 87.4% (111/127) | 84.2% (16/19) / 88.9% (16/18) | 2.4564 [2.0425–2.8923] | n.é. (PD6) |
| B (F2V2) | R2 | n.é. (PD6); összpontosság: 79.1% (121/153) | 96.0% (121/126) | — (0/0) / — (0/0) | 0.4786 [0.4031–0.5668] | n.é. (PD6) |
| B (F2V2) | R3 | n.é. (PD6); összpontosság: 50.0% (255/510) | 95.9% (255/266) | — (0/0) / — (0/0) | 0.9492 [0.7875–1.1194] | n.é. (PD6) |
| B (F2V2) | R4 | n.é. (PD6); összpontosság: 77.2% (129/167) | 90.8% (129/142) | — (0/0) / — (0/0) | 1.2355 [1.0347–1.4489] | n.é. (PD6) |
| B (F2V2) | Összes | n.é. (PD6); összpontosság: 60.9% (616/1011) | 93.2% (616/661) | 84.2% (16/19) / 88.9% (16/18) | 5.1204 [4.2687–6.0138] | n.é. (PD6) |
| C (F3V2) | R1 | n.é. (PD6); összpontosság: 94.0% (299/318) | 94.3% (299/317) | 93.8% (30/32) / 96.8% (30/31) | 20.5079 [18.6004–22.5908] | n.é. (PD6) |
| C (F3V2) | R2 | n.é. (PD6); összpontosság: 95.6% (153/160) | 100.0% (153/153) | — (0/0) / — (0/0) | 3.5672 [3.2585–3.9147] | n.é. (PD6) |
| C (F3V2) | R3 | n.é. (PD6); összpontosság: 94.2% (259/275) | 97.4% (259/266) | — (0/0) / — (0/0) | 7.9682 [7.2246–8.7845] | n.é. (PD6) |
| C (F3V2) | R4 | n.é. (PD6); összpontosság: 91.7% (309/337) | 98.1% (309/315) | — (0/0) / — (0/0) | 9.9865 [9.0769–10.9815] | n.é. (PD6) |
| C (F3V2) | Összes | n.é. (PD6); összpontosság: 93.6% (1020/1090) | 97.1% (1020/1051) | 93.8% (30/32) / 96.8% (30/31) | 42.0329 [38.1616–46.2746] | n.é. (PD6) |
| C (F3V2B) | R1 | n.é. (PD6); összpontosság: 93.8% (304/324) | 95.9% (304/317) | 93.8% (30/32) / 96.8% (30/31) | 20.544 [18.5624–22.8045] | n.é. (PD6) |
| C (F3V2B) | R2 | n.é. (PD6); összpontosság: 95.6% (152/159) | 99.3% (152/153) | — (0/0) / — (0/0) | 3.5309 [3.2443–3.8467] | n.é. (PD6) |
| C (F3V2B) | R3 | n.é. (PD6); összpontosság: 93.9% (263/280) | 98.9% (263/266) | — (0/0) / — (0/0) | 7.986 [7.2059–8.87] | n.é. (PD6) |
| C (F3V2B) | R4 | n.é. (PD6); összpontosság: 90.3% (306/339) | 97.1% (306/315) | — (0/0) / — (0/0) | 9.971 [9.054–11.0073] | n.é. (PD6) |
| C (F3V2B) | Összes | n.é. (PD6); összpontosság: 93.0% (1025/1102) | 97.5% (1025/1051) | 93.8% (30/32) / 96.8% (30/31) | 42.0348 [38.057–46.494] | n.é. (PD6) |
| A+B | R1 | 95.4% (83/87) | 46.1% (146/317) | 56.2% (18/32) / 58.1% (18/31) | 13.6769 [13.0599–14.2572] | 68.9% (1255/1822) / 62.5% (145/232) |
| A+B | R2 | 93.4% (99/106) | 81.7% (125/153) | — (0/0) / — (0/0) | 2.3295 [2.2175–2.4531] | 55.0% (230/418) / 38.7% (67/173) |
| A+B | R3 | 90.6% (58/64) | 95.9% (255/266) | — (0/0) / — (0/0) | 5.3227 [5.0794–5.5464] | 84.0% (701/835) / 87.7% (455/519) |
| A+B | R4 | 97.0% (98/101) | 48.3% (152/315) | — (0/0) / — (0/0) | 6.6253 [6.3372–6.9104] | 63.5% (431/679) / 53.0% (114/215) |
| A+B | Összes | 94.4% (338/358) | 64.5% (678/1051) | 56.2% (18/32) / 58.1% (18/31) | 27.9563 [26.7382–29.1534] | 69.7% (2617/3754) / 68.6% (781/1139) |
| A+B+C | R1 | 95.4% (83/87) | 89.3% (283/317) | 87.5% (28/32) / 90.3% (28/31) | 41.1791 [38.2149–44.3132] | 57.4% (963/1677) / 62.3% (188/302) |
| A+B+C | R2 | 93.4% (99/106) | 98.7% (151/153) | — (0/0) / — (0/0) | 7.5782 [7.0117–8.3013] | 34.0% (124/365) / 17.2% (28/163) |
| A+B+C | R3 | 90.6% (58/64) | 96.2% (256/266) | — (0/0) / — (0/0) | 16.6169 [15.3948–17.9057] | 75.3% (469/623) / 74.0% (205/277) |
| A+B+C | R4 | 97.0% (98/101) | 94.9% (299/315) | — (0/0) / — (0/0) | 20.3713 [18.7513–22.1013] | 64.0% (530/828) / 60.6% (195/322) |
| A+B+C | Összes | 94.4% (338/358) | 94.1% (989/1051) | 87.5% (28/32) / 90.3% (28/31) | 85.9074 [79.5981–92.6267] | 59.7% (2086/3493) / 57.9% (616/1064) |

Egymodelles összeállításnál a lefedettség és a régi arany a kapun átment versekre vonatkozik (n a cellában); az A+B és az A+B+C mind a 60 aranyversre és mind a 200 versre.

### Minősítés (csak A+B és A+B+C)

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

| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5; a (4) összesen) | bukott |
|---|---|---|---|
| A+B | R1 | nem teljesül | bukott: 1, 2, 3, 5; (3) mért |
| A+B | R2 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B | R3 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B | R4 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R1 | nem teljesül | bukott: 1, 2, 3, 5; (3) mért |
| A+B+C | R2 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R3 | nem teljesül | bukott: 1, 5; (3) n.é. (nincs régi arany a rétegben) |
| A+B+C | R4 | nem teljesül | bukott: 1, 2, 5; (3) n.é. (nincs régi arany a rétegben) |

### Bizonyossági szintek (A+B+C, G4)

| réteg | magas pontosság | kozepes pontosság | alacsony pontosság | eloszlás magas / kozepes / alacsony (200 vers) |
|---|---|---|---|---|
| R1 | 95.4% (83/87) | 81.5% (22/27) | 94.7% (178/188) | 33.8% (567/1677) / 8.8% (147/1677) / 57.4% (963/1677) |
| R2 | 93.4% (99/106) | 86.2% (25/29) | 96.4% (27/28) | 51.5% (188/365) / 14.5% (53/365) / 34.0% (124/365) |
| R3 | 90.6% (58/64) | 62.5% (5/8) | 94.1% (193/205) | 21.5% (134/623) / 3.2% (20/623) / 75.3% (469/623) |
| R4 | 97.0% (98/101) | 69.2% (18/26) | 93.8% (183/195) | 30.0% (248/828) / 6.0% (50/828) / 64.0% (530/828) |
| Összes | 94.4% (338/358) | 77.8% (70/90) | 94.3% (581/616) | 32.6% (1137/3493) / 7.7% (270/3493) / 59.7% (2086/3493) |

Érzékenység (a G4 „kapuhibás maradt” ágának másik olvasata: a kapuhibás versben a C túlélő modellel egyező linkje kozepes): alacsony arány a 200 versen 27.9% (976/3493), az aranyon 33.5% (356/1064) (A+B+C (alt)); a minősítés ezen nem változna, mert az (5) ezzel az olvasattal sem teljesül.

### KJV-támpont a v2-adaton (F1V2/F2V2 vs F5V2/F6V2, R1)

- `magas` (A∩B) pontosság a közös halmazon (mind a négy futás átment: 7/20 R1-aranyvers): KJV-val 93.7% (59/63), KJV nélkül 78.0% (71/91); különbség 15.63 százalékpont (küszöb: ≥ +1).
- Az A–B eltérés relatív csökkenése: közös halmazon -65.56%, saját halmazokon -37.87% (küszöb: ≥ 20%; küszöb-mérőszám 2 (a brief szerint ≥ 20%); eltérés KJV nélkül 163/463, KJV-val 394/676; küszöb-mérőszám 2 (a brief szerint ≥ 20%); eltérés KJV nélkül 299/788, KJV-val 622/1189).
- A közös halmaz 7 aranyvers: a kiválasztás torzít (csak azok a versek, ahol mind a négy futás kapun átment; a KJV-val futó A és B más verseken bukik, mint a KJV nélküli). Az 1. küszöb-mérőszám formálisan teljesül, a 2. nem; a kis n miatt nem végleges.

### A C két futása (F3V2 vs F3V2B, azonos prompt): futásközi ingadozás

| réteg | mérőszám | F3V2 | F3V2B | Δ | Δ 90% | |Δ| 95. percentilis |
|---|---|---|---|---|---|---|
| R1 | pontossag | 94.03% | 93.83% | -0.20 pp | [-2.46; +1.88] | 2.61 pp |
| R1 | lefedettseg | 94.32% | 95.90% | +1.58 pp | [-1.88; +4.59] | 4.65 pp |
| R1 | kapuhiba_elso_probara | 12.00% | 21.00% | +9.00 pp | [+3.00; +15.00] | 15.00 pp |
| R1 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp |
| R2 | pontossag | 95.63% | 95.60% | -0.03 pp | [-2.56; +3.60] | 3.62 pp |
| R2 | lefedettseg | 100.00% | 99.35% | -0.65 pp | [-1.87; +0.00] | 1.87 pp |
| R2 | kapuhiba_elso_probara | 0.00% | 20.00% | +20.00 pp | [+8.00; +32.00] | 32.00 pp |
| R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp |
| R3 | pontossag | 94.18% | 93.93% | -0.25 pp | [-1.87; +1.06] | 1.87 pp |
| R3 | lefedettseg | 97.37% | 98.87% | +1.50 pp | [+0.34; +2.88] | 2.88 pp |
| R3 | kapuhiba_elso_probara | 8.00% | 4.00% | -4.00 pp | [-12.00; +0.00] | 12.00 pp |
| R3 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp |
| R4 | pontossag | 91.69% | 90.27% | -1.43 pp | [-3.66; +0.79] | 3.66 pp |
| R4 | lefedettseg | 98.10% | 97.14% | -0.95 pp | [-2.14; +0.00] | 2.14 pp |
| R4 | kapuhiba_elso_probara | 10.00% | 2.00% | -8.00 pp | [-16.00; +0.00] | 16.00 pp |
| R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp |
| Összes | pontossag | 93.58% | 93.01% | -0.57 pp | [-1.64; +0.53] | 1.64 pp |
| Összes | lefedettseg | 97.05% | 97.53% | +0.48 pp | [-0.62; +1.60] | 1.61 pp |
| Összes | kapuhiba_elso_probara | 9.50% | 14.00% | +4.50 pp | [+0.50; +8.50] | 8.50 pp |
| Összes | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] | 0.00 pp |

A (c)-esetek (az Opus besorolása, nem mérés; naplok/F21P_C_diff_F3V2B.md): F3V2 39, F3V2B 36; azonos 20, új az F3V2B-nél 16, az F3V2-nél volt, az F3V2B-nél nincs 19. Eltérés az aranyhoz: F3V2 101, F3V2B 103, ebből közös 57.

Azonos linkhalmazú vers: 40.0% (24/60) az aranyon, 44.0% (88/200) a mintán; linkegyezés Σ|∩|/Σ|∪| 92.1% (1051/1141) (arany), 93.0% (3462/3723) (minta). Azonos prompt és konfiguráció mellett ez a futásközi ingadozás becslése (egy futáspárból); a (c)-hibák egy része futásról futásra cserélődik.

### Kapuhiba v1 és v2 (első próbára / végleg; érvénytelen JSON első próbára)

| futás | első próbára | végleg | JSON-hiba (1. kapupont) első próbára | végleg |
|---|---|---|---|---|
| A v1 (F1) | 76.0% (152/200) | 41.0% (82/200) | 50.0% (100/200) | 0.0% (0/200) |
| A v2 (F1V2) | 80.0% (160/200) | 42.0% (84/200) | 45.0% (90/200) | 0.0% (0/200) |
| B v1 (F2) | 53.0% (106/200) | 41.0% (82/200) | 20.0% (40/200) | 20.0% (40/200) |
| B v2 (F2V2) | 70.5% (141/200) | 27.5% (55/200) | 55.0% (110/200) | 5.0% (10/200) |
| C v1 (F3) | 15.0% (30/200) | 0.5% (1/200) | 5.0% (10/200) | 0.0% (0/200) |
| C v2 (F3V2) | 9.5% (19/200) | 0.0% (0/200) | 5.0% (10/200) | 0.0% (0/200) |
| C (2. futás) v2 (F3V2B) | 14.0% (28/200) | 0.0% (0/200) | 10.0% (20/200) | 0.0% (0/200) |
| A KJV nélkül v1 (F5) | 75.0% (75/100) | 31.0% (31/100) | 30.0% (30/100) | 0.0% (0/100) |
| A KJV nélkül v2 (F5V2) | 72.0% (72/100) | 48.0% (48/100) | 50.0% (50/100) | 0.0% (0/100) |
| B KJV nélkül v1 (F6) | 23.0% (23/100) | 13.0% (13/100) | nincs ilyen hiba | nincs ilyen hiba |
| B KJV nélkül v2 (F6V2) | 57.0% (57/100) | 24.0% (24/100) | 50.0% (50/100) | 0.0% (0/100) |
| C döntőbíró v2 (F4V2) | 21.2% (41/193) | 0.0% (0/193) | 10.4% (20/193) | 0.0% (0/193) |

A döntőbíró (F4V2) versei: az F1V2/F2V2 eltérő vagy kapuhibás versei, 193. Az első próbás kapuhibát a teljes kapun számoljuk (ötpontos kapu + 6. pont: az A–B rögzítés, futtat.biro_kenyszer, ahogy a futtató a futáskor ellenőrizte): első próbára 21.2% (41/193), végleg 0.0% (0/193). Kapupontonként első próbára: 1. pont 2.1% (4/193), 1-json 10.4% (20/193), 3. pont 1.0% (2/193), 4. pont 0.5% (1/193), 6. pont (rögzítés-sértés) 7.3% (14/193).
**Megfigyelés (nem feltétel):** legalább 14 versben a C első válasza megsértette az A–B rögzítést; a 6. pontos kényszer és az egy újrakérés mindet javította (végleg 0/193).
Keresztellenőrzés (az újraszámolt első próbás hibás versek = a jsonl probalkozas=2 versei = a futásnapló kapuhiba_db összege az első próbálkozásokon): A v1 (F1) 152 = 152: EGYEZIK; A v2 (F1V2) 160 = 160: EGYEZIK; B v1 (F2) 106 = 106: EGYEZIK; B v2 (F2V2) 141 = 141: EGYEZIK; C v1 (F3) 30 = 30: EGYEZIK; C v2 (F3V2) 19 = 19: EGYEZIK; C (2. futás) v2 (F3V2B) 28 = 28: EGYEZIK; A KJV nélkül v1 (F5) 75 = 75: EGYEZIK; A KJV nélkül v2 (F5V2) 72 = 72: EGYEZIK; B KJV nélkül v1 (F6) 23 = 23: EGYEZIK; B KJV nélkül v2 (F6V2) 57 = 57: EGYEZIK; C döntőbíró v2 (F4V2) 41 = 41: EGYEZIK.
A mentett (kapun átment) válaszok újraellenőrzése a teljes kapun (futtat.mentett_valaszok_ellenoriz): F1V2: 0 hiba; F2V2: 0 hiba; F3V2: 0 hiba; F3V2B: 0 hiba; F4V2: 0 hiba; F5V2: 0 hiba; F6V2: 0 hiba.

### P5 minden összeállításra (teljes Biblia, 90%-os intervallum)

**Eltérés a brieftől:** a bootstrap egysége a köteg, nem a vers — DT21 f): **elfogadva (felhasználói döntés)**. Az ár a modell táblaára × a futás mért cost/táblaár aránya (az A-nál és a B-nél a cost nem egyenlő a táblaárral).

**Rétegbesorolás (DT21 h, felhasználói döntés):** a teljes Biblia vetítése az F22 brief 22.2 **műfaji** (nem kánon szerinti) öt rétege szerint készül: ÓSZ-próza (1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Bír, Ruth, 1Sám, 2Sám, 1Kir, 2Kir, 1Krón, 2Krón, Ezsd, Neh, Eszt); költészet (Jób, Zsolt, Péld, Préd, Én, Sir); próféta (Ézs, Jer, Ez, Dán, Hós, Jóel, Ámós, Abd, Jón, Mik, Náh, Hab, Sof, Hag, Zak, Mal); evangélium+ApCsel (Mt, Mk, Luk, Ján, ApCsel); levél+Jel (Róm, 1Kor, 2Kor, Gal, Ef, Fil, Kol, 1Thessz, 2Thessz, 1Tim, 2Tim, Tit, Filem, Zsid, Jak, 1Pét, 2Pét, 1Ján, 2Ján, 3Ján, Júd, Jel). A 22.2 szövegén túli könyveket a felhasználó sorolta be: Préd → költészet, Sir → költészet, Dán → próféta, Ruth → ÓSZ-próza, Eszt → ÓSZ-próza. A pilot mérési rétegei (R1–R4, minta.tsv, arany v2) nem változnak; a minta versei a döntőbírói arányhoz és a kézimunkához könyv szerint képeződnek le az F22-rétegekre (Péld az R1-ből a költészethez; az R4 evangéliumai az evangélium+ApCsel, levelei a levél+Jel réteghez). A korábbi pilot-4-réteges besorolás alább tájékoztatóként áll.

**A leképezés még nyitott része (nem egyértelmű):** az ApCsel és a Jel nincs a pilotmintában, ezért a mintában nincs az F22 szerinti evangélium+ApCsel és levél+Jel réteg-pontos mérése: e két réteg döntőbírói aránya és kézimunka-rátája csak az evangéliumok, illetve a levelek mintaverseiből jön, és a vetítés az ApCsel/Jel verseire is ezt alkalmazza (a token-illesztés rétegfüggetlen, azt nem érinti). Az öt F22-réteg a pilot négy mérési rétegével szemben: a mérési táblák R1–R4-ek maradnak, az öt réteg csak a vetítésben él.

| összeállítás | ÓSZ-próza | költészet | próféta | evangélium+ApCsel | levél+Jel | Összes (F22) |
|---|---|---|---|---|---|---|
| A (F1V2) | 10.5772 [10.1633–10.9407] | 2.584 [2.4804–2.6958] | 4.285 [4.1149–4.4344] | 3.2495 [3.1405–3.3612] | 2.1403 [2.0691–2.214] | 22.8359 [22.0403–23.6158] |
| B (F2V2) | 2.2947 [1.9029–2.7044] | 0.6623 [0.5586–0.7829] | 0.9279 [0.7696–1.0945] | 0.7444 [0.6232–0.8733] | 0.4911 [0.4115–0.5759] | 5.1204 [4.2687–6.0138] |
| C (F3V2) | 19.2778 [17.4733–21.2438] | 4.9671 [4.536–5.4531] | 7.8015 [7.0728–8.6014] | 6.0195 [5.4711–6.6193] | 3.967 [3.6058–4.3622] | 42.0329 [38.1616–46.2746] |
| C (F3V2B) | 19.3234 [17.4457–21.4833] | 4.9202 [4.52–5.3712] | 7.8202 [7.0559–8.6867] | 6.0105 [5.457–6.636] | 3.9605 [3.5968–4.3713] | 42.0348 [38.057–46.494] |
| A+B | 12.8718 [12.2818–13.4151] | 3.2463 [3.0919–3.4163] | 5.2128 [4.9741–5.4321] | 3.9939 [3.8194–4.1659] | 2.6315 [2.5168–2.7445] | 27.9563 [26.7382–29.1534] |
| A+B+C | 39.2741 [36.4125–42.2582] | 10.1116 [9.3219–11.1173] | 16.2654 [15.0646–17.5362] | 11.9354 [10.7866–13.1005] | 8.3209 [7.7147–8.9708] | 85.9074 [79.5981–92.6267] |
| C döntőbíró rész | 26.4022 [23.6316–29.4579] | 6.8653 [6.1057–7.8284] | 11.0525 [9.8629–12.2769] | 7.9416 [6.7883–9.073] | 5.6895 [5.1116–6.3191] | 57.9511 [51.9552–64.4589] |

Tájékoztató: a korábbi pilot-4-réteges besorolás szerint (ugyanazzal a bootstrap-mintával):

| összeállítás | R1 | R2 | R3 | R4 | Összes (pilot-4) |
|---|---|---|---|---|---|
| A (F1V2) | 11.2206 [10.7962–11.6113] | 1.851 [1.7736–1.9335] | 4.3735 [4.2019–4.5258] | 5.3898 [5.2096–5.5752] | 22.8348 [22.0394–23.6148] |
| B (F2V2) | 2.4564 [2.0425–2.8923] | 0.4786 [0.4031–0.5668] | 0.9492 [0.7875–1.1194] | 1.2355 [1.0347–1.4489] | 5.1197 [4.2679–6.0131] |
| C (F3V2) | 20.5079 [18.6004–22.5908] | 3.5672 [3.2585–3.9147] | 7.9682 [7.2246–8.7845] | 9.9865 [9.0769–10.9815] | 42.0298 [38.1586–46.2713] |
| C (F3V2B) | 20.544 [18.5624–22.8045] | 3.5309 [3.2443–3.8467] | 7.986 [7.2059–8.87] | 9.971 [9.054–11.0073] | 42.0319 [38.0541–46.491] |
| A+B | 13.6769 [13.0599–14.2572] | 2.3295 [2.2175–2.4531] | 5.3227 [5.0794–5.5464] | 6.6253 [6.3372–6.9104] | 27.9545 [26.7362–29.1517] |
| A+B+C | 41.1791 [38.2149–44.3132] | 7.5782 [7.0117–8.3013] | 16.6169 [15.3948–17.9057] | 20.3713 [18.7513–22.1013] | 85.7455 [79.6322–92.3303] |
| C döntőbíró rész | 27.5022 [24.6275–30.6357] | 5.2487 [4.6821–5.9345] | 11.2942 [10.0794–12.5528] | 13.7459 [12.1933–15.4553] | 57.791 [51.8778–64.2355] |

A két besorolás költségkülönbsége (tájékoztató; F22 műfaji 5 réteg − korábbi pilot-4 réteg, pont-becslés):

| összeállítás | F22 USD | pilot-4 USD | különbség USD | különbség % |
|---|---|---|---|---|
| A (F1V2) | 22.8359 | 22.8348 | 0.001071 | 0.0047% |
| B (F2V2) | 5.1204 | 5.1197 | 0.000709 | 0.0138% |
| C (F3V2) | 42.0329 | 42.0298 | 0.003159 | 0.0075% |
| C (F3V2B) | 42.0348 | 42.0319 | 0.002892 | 0.0069% |
| A+B | 27.9563 | 27.9545 | 0.00178 | 0.0064% |
| A+B+C | 85.9074 | 85.7455 | 0.161913 | 0.1888% |
| C döntőbíró rész | 57.9511 | 57.791 | 0.160133 | 0.2771% |

Az egymodelles összeállításoknál a különbség csak a rétegenkénti ceil(N/10) kötegszám kerekítéséből jön (az illesztés rétegfüggetlen); az A+B+C-nél a döntőbírói versarány rétegenkénti súlyozása is változik.

| futás | cost/táblaár (s) | újrakérés-szorzó M | ellenőrzés mintán belül | leave-one-out | **számító (DT21 g: a konzervatívabb)** |
|---|---|---|---|---|---|
| F1V2 | 1.000013 | 1.744426 | 0.0% | -0.111% | -0.111% (leave-one-out; küszöb ≤ 10%: teljesül) |
| F2V2 | 0.65627 | 1.800281 | 0.0% | -0.276% | -0.276% (leave-one-out; küszöb ≤ 10%: teljesül) |
| F3V2 | 0.999999 | 1.194298 | 0.0% | -0.148% | -0.148% (leave-one-out; küszöb ≤ 10%: teljesül) |
| F3V2B | 0.99999 | 1.181673 | 0.0% | -0.077% | -0.077% (leave-one-out; küszöb ≤ 10%: teljesül) |
| F4V2 | 1.000001 | 1.366257 | 0.0% | 0.321% | 0.321% (leave-one-out; küszöb ≤ 10%: teljesül) |

DT21 g) (felhasználói döntés): a mintán belüli és a leave-one-out ellenőrzés közül a konzervatívabb — a nagyobb abszolút eltérésű — számít a ≤ 10%-os küszöbhöz; ez minden futásnál a leave-one-out (a mintán belüli illesztés a saját hívásait közel 0 eltéréssel adja vissza). Az A+B+C összesített ellenőrzése (0.0%) csak mintán belüli; a futásonkénti leave-one-out a fenti táblában.

A pilot tényleges költsége (futásnapló, minden futás, P3 és P3b): 1.605067 USD. A C (F3V2) vetítés intervalluma itt kissé eltér a P3-as koltseg_vetites.tsv-étől, mert a két szkript bootstrapja más véletlenszám-sorrendet használ (azonos mag mellett).

Döntőbírói versarány F22-rétegenként (F4V2; a minta versei könyv szerint leképezve): ÓSZ-próza 68/70 vers, költészet 52/55 vers, próféta 25/25 vers, evangélium+ApCsel 23/25 vers, levél+Jel 25/25 vers. Tájékoztató, pilot-rétegenként: R1 95/100 vers, R2 25/25 vers, R3 25/25 vers, R4 48/50 vers. Kézimunka-vetítés (A+B+C, G4; F22-rétegenként): vetített `alacsony` link a Bibliára 359569 (alt olvasat: 165461); vetített eltérés az aranyhoz mérten 73372; a (c)-hiba/vers az A+B+C-re n.é. (nincs besorolva). Tájékoztató, a pilot-4-réteges besorolással: `alacsony` 340519 (alt: 152119), eltérés 74830.

*A lenti szakaszok a P3 (a P3b előtti) adatát őrzik változatlanul (v1-A/B, F3/F3V2); a P3b-eredmény a fenti.*

## Összefoglaló — P3 (korábbi, a P3b előtt: v1-A/B, F3/F3V2)

- **Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).**
- Az A+B két mért feltételen bukott: az A∩B (`magas`) pontosság R1-ben, R3-ban és R4-ben a 98% alatt van, a régi arany egyezése 60.0% (3/5) (a 95% alatt).
- A C egymodelles összeállítás, a PD6 szerint nem minősíthető. A C régi arany egyezése: **mért (kizárás nélkül) 93.8% (30/32) — a 95% alatt**; az 1Móz 6:17 kizárásával 96.8% (30/31) (tájékoztató, nem minősít — a küszöb szempontjából a mért, kizárás nélküli érték számít (DT21 i); a hibásnak jelölt hármas csak az 1Móz 6:17, az 1Móz 13:4 korábbi hibás-jelölése a felhasználó döntése szerint visszavonva).

## (a) Eredmény — P3 (korábbi, a P3b előtt)

**Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).** A rögzített öt feltétel (`magas` pontosság ≥ 98% minden rétegben; lefedettség ≥ 95%; régi arany ≥ 95%; vetített költség 90%-os felső széle ≤ 60 USD; vetített `alacsony` arány ≤ 10%) összeállításonként:

| összeállítás | magas pontosság ≥ 98% | lefedettség ≥ 95% | régi arany ≥ 95% | költség ≤ 60 USD | alacsony ≤ 10% | minősítés |
|---|---|---|---|---|---|---|
| A | n.é. (egymodelles, PD6) | mért: 81.5% (528/648) — nem minősíthető | mért: 83.3% (20/24) | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |
| B | n.é. (egymodelles, PD6) | mért: 79.2% (742/937) — nem minősíthető | mért: 66.7% (4/6) | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |
| C | n.é. (egymodelles, PD6) | mért: F3 94.1% (989/1051) (arany v1), F3V2 97.1% (1020/1051) (arany v2) — nem minősíthető | mért (kizárás nélkül): F3 93.8% (30/32), F3V2 93.8% (30/32) — a 95% alatt; az 1Móz 6:17 kizárásával F3V2 96.8% (30/31) (tájékoztató, nem minősít — a küszöb szempontjából a mért, kizárás nélküli érték számít (DT21 i); a hibásnak jelölt hármas csak az 1Móz 6:17, az 1Móz 13:4 korábbi hibás-jelölése a felhasználó döntése szerint visszavonva) | vetítve (F22 műfaji 5 réteg): F3 42.2353 USD [37.7848–47.034], F3V2 42.033 USD [37.9527–46.1502] (90%) | n.é. (PD6) | nem minősíthető (PD6) |
| A+B | **bukott**: A∩B pontosság R1 85.2% (52/61), R2 98.4% (61/62), R3 91.8% (179/195), R4 91.7% (77/84) | nem mért (F4 nélkül nincs végső linkhalmaz; A∩B lefedettség tájékoztatásul: 65.3% (369/565)) | **bukott** (A∩B): 60.0% (3/5); a korábbi, összetett Strong nélküli definícióval is 60.0% (3/5) | nem vetítve (PD8) | nem mért (F4 nélkül; PD8) | nem felel meg |
| A+B+C | nem mért (az F4 nem futott, PD8) | nem mért | nem mért | nem vetítve | nem mért | nem mért (PD8) |

## (b) Mi bukott el — P3 (korábbi; csak a rögzített öt feltétel)

- **A+B, `magas` pontosság ≥ 98% minden rétegben — bukott:** az A∩B linkek pontossága R1 85.2% (52/61), R2 98.4% (61/62), R3 91.8% (179/195), R4 91.7% (77/84) (forrás: meres_eredmeny.tsv, pontossag_lefedettseg).
- **A+B, régi arany ≥ 95% — bukott:** az A∩B egyezése a halmaz-definícióval 60.0% (3/5), a korábbi (összetett Strong nélküli) definícióval 60.0% (3/5) (meres_eredmeny.tsv, regi_arany).
- **A+B, lefedettség, költség, `alacsony` arány:** nem mért (F4 nélkül nincs végső linkhalmaz és bizonyossági szint; PD8).
- **A, B, C (egymodelles):** a PD6 szerint nem minősíthető; a `magas`/`alacsony` szint egy modellnél nem értelmezhető. A C mért összpontossága a rétegenkénti 98%-hoz mérten az arany v2-n F3: R1 94.6% (295/312), R2 94.2% (146/155), R3 91.9% (250/272), R4 92.9% (299/322); F3V2: R1 94.0% (299/318), R2 95.6% (153/160), R3 94.2% (259/275), R4 91.7% (309/337). A korrigált (Opus-besorolás, nem mérés) érték nem számít.
- **A+B+C:** nem mért (PD8, az F4 nem futott).

**Megfigyelés (nem feltétel):** a kapuhiba nem tartozik a rögzített öt feltétel közé. Végleges kapuhiba A 41.0% (82/200), B 41.0% (82/200); első próbára A 76.0% (152/200), B 53.0% (106/200). A döntőbíróhoz menne (eltérő, csak egyik átment, egyik sem): 98.5% (197/200) (meres_eredmeny.tsv, kapuhiba és ab_osszeallitas). Emiatt az A+B összeállításban a döntőbíró (F4) nélkül az `alacsony`-arány feltétel nem mért.

## (b2) Mérőszámok összeállításonként és rétegenként — P3 (P-K4; forrás: meres_eredmeny.tsv, arany v1)

Bizonyossági szintek (G4): a `magas` az A∩B (az A+B egyező linkjei); a `kozepes` és az `alacsony` a döntőbíró (F4) döntésén alapul, F4 nélkül nem mért (PD8); egymodelles összeállításra egyik szint sem értelmezett (PD6).

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| A | arany_versek_kapun_atment | 65.0% (13/20) | 60.0% (6/10) | 80.0% (8/10) | 60.0% (12/20) | 65.0% (39/60) |
| A | pontossag | 80.1% (129/161) | 92.8% (64/69) | 76.0% (190/250) | 85.3% (145/170) | 81.2% (528/650) |
| A | lefedettseg | 75.4% (129/171) | 87.7% (64/73) | 83.7% (190/227) | 81.9% (145/177) | 81.5% (528/648) |
| B | arany_versek_kapun_atment | 85.0% (17/20) | 100.0% (10/10) | 100.0% (10/10) | 75.0% (15/20) | 86.7% (52/60) |
| B | pontossag | 58.0% (156/269) | 72.2% (140/194) | 56.9% (244/429) | 81.5% (202/248) | 65.1% (742/1140) |
| B | lefedettseg | 59.8% (156/261) | 91.5% (140/153) | 91.7% (244/266) | 78.6% (202/257) | 79.2% (742/937) |
| C | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| C | pontossag | 94.2% (294/312) | 94.2% (146/155) | 91.9% (250/272) | 92.9% (299/322) | 93.2% (989/1061) |
| C | lefedettseg | 92.7% (294/317) | 95.4% (146/153) | 94.0% (250/266) | 94.9% (299/315) | 94.1% (989/1051) |
| A+B magas (A∩B) | arany_versek_kapun_atment | 55.0% (11/20) | 60.0% (6/10) | 80.0% (8/10) | 35.0% (7/20) | 53.3% (32/60) |
| A+B magas (A∩B) | pontossag | 85.2% (52/61) | 98.4% (61/62) | 91.8% (179/195) | 91.7% (77/84) | 91.8% (369/402) |
| A+B magas (A∩B) | lefedettseg | 35.6% (52/146) | 83.6% (61/73) | 78.9% (179/227) | 64.7% (77/119) | 65.3% (369/565) |
| A∪B (döntőbíró előtti felső korlát) | arany_versek_kapun_atment | 55.0% (11/20) | 60.0% (6/10) | 80.0% (8/10) | 35.0% (7/20) | 53.3% (32/60) |
| A∪B (döntőbíró előtti felső korlát) | pontossag | 55.6% (120/216) | 75.0% (72/96) | 53.6% (216/403) | 71.1% (101/142) | 59.4% (509/857) |
| A∪B (döntőbíró előtti felső korlát) | lefedettseg | 82.2% (120/146) | 98.6% (72/73) | 95.2% (216/227) | 84.9% (101/119) | 90.1% (509/565) |
| A–B | versek_mindketto_atment | 15.0% (15/100) | 68.0% (17/25) | 40.0% (10/25) | 46.0% (23/50) | 32.5% (65/200) |
| A–B | link_egyezes (uniós arány) | 32.5% (93/286) | 59.8% (149/249) | 48.3% (219/453) | 67.5% (287/425) | 52.9% (748/1413) |
| A–B | azonos_linkhalmazu_versek | 13.3% (2/15) | 0.0% (0/17) | 0.0% (0/10) | 4.3% (1/23) | 4.6% (3/65) |
| A | régi arany: egyezes | 83.3% (20/24) | — (0/0) | — (0/0) | — (0/0) | 83.3% (20/24) |
| A | régi arany: egyezes_hibas_kizarva_tajekoztato | 87.0% (20/23) | — (0/0) | — (0/0) | — (0/0) | 87.0% (20/23) |
| B | régi arany: egyezes | 66.7% (4/6) | — (0/0) | — (0/0) | — (0/0) | 66.7% (4/6) |
| B | régi arany: egyezes_hibas_kizarva_tajekoztato | 66.7% (4/6) | — (0/0) | — (0/0) | — (0/0) | 66.7% (4/6) |
| C | régi arany: egyezes | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| C | régi arany: egyezes_hibas_kizarva_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| A+B magas (A∩B) | régi arany: egyezes | 60.0% (3/5) | — (0/0) | — (0/0) | — (0/0) | 60.0% (3/5) |
| A+B magas (A∩B) | régi arany: egyezes_hibas_kizarva_tajekoztato | 60.0% (3/5) | — (0/0) | — (0/0) | — (0/0) | 60.0% (3/5) |
| F1 (A) | kapuhiba_elso_probara | 71.0% (71/100) | 76.0% (19/25) | 96.0% (24/25) | 76.0% (38/50) | 76.0% (152/200) |
| F1 (A) | kapuhiba_vegleg | 42.0% (42/100) | 32.0% (8/25) | 40.0% (10/25) | 44.0% (22/50) | 41.0% (82/200) |
| F2 (B) | kapuhiba_elso_probara | 80.0% (80/100) | 8.0% (2/25) | 52.0% (13/25) | 22.0% (11/50) | 53.0% (106/200) |
| F2 (B) | kapuhiba_vegleg | 68.0% (68/100) | 0.0% (0/25) | 36.0% (9/25) | 10.0% (5/50) | 41.0% (82/200) |
| F3 (C) | kapuhiba_elso_probara | 17.0% (17/100) | 0.0% (0/25) | 20.0% (5/25) | 16.0% (8/50) | 15.0% (30/200) |
| F3 (C) | kapuhiba_vegleg | 1.0% (1/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.5% (1/200) |
| F5 (A (KJV nélkül)) | kapuhiba_elso_probara | 75.0% (75/100) | — | — | — | 75.0% (75/100) |
| F5 (A (KJV nélkül)) | kapuhiba_vegleg | 31.0% (31/100) | — | — | — | 31.0% (31/100) |
| F6 (B (KJV nélkül)) | kapuhiba_elso_probara | 23.0% (23/100) | — | — | — | 23.0% (23/100) |
| F6 (B (KJV nélkül)) | kapuhiba_vegleg | 13.0% (13/100) | — | — | — | 13.0% (13/100) |
| A+B | mindketto_atment_azonos_linkekkel | 2.0% (2/100) | 0.0% (0/25) | 0.0% (0/25) | 2.0% (1/50) | 1.5% (3/200) |
| A+B | mindketto_atment_eltero_linkekkel | 13.0% (13/100) | 68.0% (17/25) | 40.0% (10/25) | 44.0% (22/50) | 31.0% (62/200) |
| A+B | csak_A_atment | 43.0% (43/100) | 0.0% (0/25) | 20.0% (5/25) | 10.0% (5/50) | 26.5% (53/200) |
| A+B | csak_B_atment | 17.0% (17/100) | 32.0% (8/25) | 24.0% (6/25) | 44.0% (22/50) | 26.5% (53/200) |
| A+B | egyik_sem_atment | 25.0% (25/100) | 0.0% (0/25) | 16.0% (4/25) | 0.0% (0/50) | 14.5% (29/200) |
| A+B | dontobirohoz_menne (eltero + csak egyik + egyik sem) | 98.0% (98/100) | 100.0% (25/25) | 100.0% (25/25) | 98.0% (49/50) | 98.5% (197/200) |
| A+B | nem_egyezo_link_arany (1 − A∩B/A∪B) | 67.5% (193/286) | 40.2% (100/249) | 51.7% (234/453) | 32.5% (138/425) | 47.1% (665/1413) |
| A+B | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |

## (c) A mért számok — P3 (C: F3/F3V2; v1-A/B)

### Pontosság és lefedettség (C; forrás: meres_v2_eredmeny.tsv)

| réteg | mérőszám | F3 × arany v1 | F3 × arany v2 | F3V2 × arany v2 |
|---|---|---|---|---|
| R1 | pontossag | 94.2% (294/312) | 94.6% (295/312) | 94.0% (299/318) |
| R1 | lefedettseg | 92.7% (294/317) | 93.1% (295/317) | 94.3% (299/317) |
| R2 | pontossag | 94.2% (146/155) | 94.2% (146/155) | 95.6% (153/160) |
| R2 | lefedettseg | 95.4% (146/153) | 95.4% (146/153) | 100.0% (153/153) |
| R3 | pontossag | 91.9% (250/272) | 91.9% (250/272) | 94.2% (259/275) |
| R3 | lefedettseg | 94.0% (250/266) | 94.0% (250/266) | 97.4% (259/266) |
| R4 | pontossag | 92.9% (299/322) | 92.9% (299/322) | 91.7% (309/337) |
| R4 | lefedettseg | 94.9% (299/315) | 94.9% (299/315) | 98.1% (309/315) |
| Összes | pontossag | 93.2% (989/1061) | 93.3% (990/1061) | 93.6% (1020/1090) |
| Összes | lefedettseg | 94.1% (989/1051) | 94.2% (990/1051) | 97.1% (1020/1051) |

Az A és a B (arany v1, kapun átment versek; meres_eredmeny.tsv): A pontosság 81.2% (528/650), lefedettség 81.5% (528/648); B pontosság 65.1% (742/1140), lefedettség 79.2% (742/937).

### Régi arany egyezés (halmaz-definíció; mért = kizárás nélkül, DT21 i)

| összeállítás | kizárás nélkül (MÉRT) | az 1Móz 6:17 nélkül (TÁJÉKOZTATÓ) |
|---|---|---|
| A (arany-független, 200 verses minta) | 83.3% (20/24) | 87.0% (20/23) |
| B (arany-független, 200 verses minta) | 66.7% (4/6) | 66.7% (4/6) |
| C (arany-független, 200 verses minta) | 93.8% (30/32) | 96.8% (30/31) |
| A+B magas (A∩B) (arany-független, 200 verses minta) | 60.0% (3/5) | 60.0% (3/5) |
| C — F3V2 | 93.8% (30/32) | 96.8% (30/31) |

### Kapuhiba-arány (első próbára / végleg)

| futás | első próbára | végleg |
|---|---|---|
| A | 76.0% (152/200) | 41.0% (82/200) |
| B | 53.0% (106/200) | 41.0% (82/200) |
| C (F3) | 15.0% (30/200) | 0.5% (1/200) |
| C (F3V2) | 9.5% (19/200) | 0.0% (0/200) |

### Költség (futásnapló)

| futás | cost USD |
|---|---|
| F1 | 0.132718 |
| F1V2 | 0.137698 |
| F2 | 0.017725 |
| F2V2 | 0.032072 |
| F3 | 0.257251 |
| F3V2 | 0.256731 |
| F3V2B | 0.256110 |
| F4V2 | 0.359316 |
| F5 | 0.060663 |
| F5V2 | 0.072390 |
| F6 | 0.009506 |
| F6V2 | 0.012887 |
| P3 összesen (a P3b előtt: F1–F3, F5, F6, F3V2) | 0.734594 |
| **a pilot összesen (P3 + P3b)** | **1.605067** (plafon: 3 USD) |

A C gondolkodási tokenje a futásnaplóban 0 (F3 és F3V2), és az F3V2 nyers usage-ában is 0 (koltseg_vetites.tsv, illesztes/gondolkodasi_token).

### KJV-támpont (N29)

A v1-adaton nem teljesül, n=8, nem végleges. A közös halmazon (mind a négy futás átment, 8/20 R1-aranyvers): a `magas` pontosság különbsége (KJV-val − KJV nélkül) -5.36 százalékpont (küszöb: ≥ +1); az A–B eltérés relatív csökkenése -9.78% (küszöb: ≥ 20%) — meres_eredmeny.tsv, kjv_hatas. Az A és a B kiesett (PD8), a KJV-hatás a C-re nem mért.

### Futásközi eltérés (F3 vs F3V2, arany v2; forrás: ingadozas.tsv)

A két C-futás promptja is különbözik: az eltérés = prompthatás + futásközi ingadozás, a kettő egy-egy futásból **nem választható szét**. A bootstrap (a versek felett, rétegzett, 1000) a versminta bizonytalanságát fedi, a futás megismétlésének szórását nem. A |Δ| a két futás közti eltérés (prompt és ingadozás együtt) felső becslése, nem az ingadozásé.

| réteg | mérőszám | F3 | F3V2 | Δ | Δ 90%-os intervallum | |Δ| felső becslés (95. percentilis) | n |
|---|---|---|---|---|---|---|---|
| R1 | pontossag | 94.55% | 94.03% | -0.53 pp | [-2.73; +1.56] pp | 2.75 pp | 20 |
| R1 | lefedettseg | 93.06% | 94.32% | +1.26 pp | [-1.01; +3.68] pp | 3.68 pp | 20 |
| R1 | kapuhiba_elso_probara | 17.00% | 12.00% | -5.00 pp | [-10.00; +0.00] pp | 10.00 pp | 100 |
| R1 | kapuhiba_vegleg | 1.00% | 0.00% | -1.00 pp | [-3.00; +0.00] pp | 3.00 pp | 100 |
| R2 | pontossag | 94.19% | 95.63% | +1.43 pp | [-3.03; +4.76] pp | 4.83 pp | 10 |
| R2 | lefedettseg | 95.42% | 100.00% | +4.58 pp | [+0.65; +8.79] pp | 8.79 pp | 10 |
| R2 | kapuhiba_elso_probara | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] pp | 0.00 pp | 25 |
| R2 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] pp | 0.00 pp | 25 |
| R3 | pontossag | 91.91% | 94.18% | +2.27 pp | [+0.71; +4.02] pp | 4.02 pp | 10 |
| R3 | lefedettseg | 93.98% | 97.37% | +3.38 pp | [+1.82; +5.13] pp | 5.13 pp | 10 |
| R3 | kapuhiba_elso_probara | 20.00% | 8.00% | -12.00 pp | [-28.00; +0.00] pp | 28.00 pp | 25 |
| R3 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] pp | 0.00 pp | 25 |
| R4 | pontossag | 92.86% | 91.69% | -1.17 pp | [-4.22; +1.53] pp | 4.22 pp | 20 |
| R4 | lefedettseg | 94.92% | 98.10% | +3.17 pp | [+1.63; +4.92] pp | 4.92 pp | 20 |
| R4 | kapuhiba_elso_probara | 16.00% | 10.00% | -6.00 pp | [-12.00; -2.00] pp | 12.00 pp | 50 |
| R4 | kapuhiba_vegleg | 0.00% | 0.00% | +0.00 pp | [+0.00; +0.00] pp | 0.00 pp | 50 |
| Összes | pontossag | 93.31% | 93.58% | +0.27 pp | [-1.03; +1.61] pp | 1.66 pp | 60 |
| Összes | lefedettseg | 94.20% | 97.05% | +2.85 pp | [+1.69; +4.03] pp | 4.03 pp | 60 |
| Összes | kapuhiba_elso_probara | 15.00% | 9.50% | -5.50 pp | [-9.00; -2.00] pp | 9.00 pp | 200 |
| Összes | kapuhiba_vegleg | 0.50% | 0.00% | -0.50 pp | [-1.50; +0.00] pp | 1.50 pp | 200 |

Verszintű linkhalmaz-egyezés: azonos linkhalmazú vers 20/60 az aranyon, 69/199 a mintán (mindkét futás átment); a linkek egyezése Σ|∩|/Σ|∪| = 89.8% (3321/3698) a mintán.
A lefedettség 94.20% → 97.05% különbsége (+2.85 pp) 90%-os intervalluma [+1.69; +4.03] pp: a versminta bizonytalansága ezt a különbséget nem magyarázza (az intervallum nem tartalmazza a 0-t); hogy mekkora része prompthatás és mekkora futásközi ingadozás, egy-egy futásból nem mondható meg.

## (d) Költségvetítés — P3 (P5, csak a C; forrás: koltseg_vetites.tsv; a P3b-vetítés a fenti P3b-szakaszban)

**Eltérés a brieftől:** a bootstrap egysége a 10 verses köteg, nem a vers (a brief P5.6 a verseken kéri; a token hívásonként, 10 versre ismert, versenként nem mérhető). DT21 f): **elfogadva (felhasználói döntés)**.

Módszer: illesztés tokenfajtánként az első próbálkozású hívásokon (bemenet = a + b·x + c·k; kimenet = a + b·x; x = eredeti + Károli-szavak, k = KJV-támpont szavai); a teljes Biblia valódi vershosszai (Karoli_1908, TAHOT/TAGNT); ár a cost mezőből; az újrakérés a pilot mért szorzójával; bootstrap a kötegek felett (1000); ellenőrzés a 200 versen.

Rétegbesorolás (DT21 h): az F22 brief 22.2 műfaji (nem kánon szerinti) öt rétege; a korábbi pilot-4-réteges besorolás tájékoztatóként alább.

| réteg (F22) | könyvek | versek |
|---|---|---|
| ÓSZ-próza | 1Móz 2Móz 3Móz 4Móz 5Móz Józs Bír Ruth 1Sám 2Sám 1Kir 2Kir 1Krón 2Krón Ezsd Neh Eszt | 12871 |
| költészet | Jób Zsolt Péld Préd Én Sir | 5001 |
| próféta | Ézs Jer Ez Dán Hós Jóel Ámós Abd Jón Mik Náh Hab Sof Hag Zak Mal | 5332 |
| evangélium+ApCsel | Mt Mk Luk Ján ApCsel | 4785 |
| levél+Jel | Róm 1Kor 2Kor Gal Ef Fil Kol 1Thessz 2Thessz 1Tim 2Tim Tit Filem Zsid Jak 1Pét 2Pét 1Ján 2Ján 3Ján Júd Jel | 3169 |

| réteg (pilot-4, tájékoztató) | könyvek | versek |
|---|---|---|
| R1 | 1Móz 2Móz 3Móz 4Móz 5Móz Józs Bír Ruth 1Sám 2Sám 1Kir 2Kir 1Krón 2Krón Ezsd Neh Eszt Péld Préd | 14006 |
| R2 | Jób Zsolt Én | 3712 |
| R3 | Ézs Jer Sir Ez Dán Hós Jóel Ámós Abd Jón Mik Náh Hab Sof Hag Zak Mal | 5486 |
| R4 | Mt Mk Luk Ján ApCsel Róm 1Kor 2Kor Gal Ef Fil Kol 1Thessz 2Thessz 1Tim 2Tim Tit Filem Zsid Jak 1Pét 2Pét 1Ján 2Ján 3Ján Júd Jel | 7954 |

| futás | illesztés (bemenet a/b/c; kimenet a/b) | cost/táblaár (1. próba) | újrakérés-szorzó M | 200 vers: vetített / tényleges (eltérés) | leave-one-out eltérés | **számító (DT21 g)** |
|---|---|---|---|---|---|---|
| F3 | 1898.37 / 12.0799 / 4.6521 ; 135.08 / 3.3741 | 0.999992 | 1.295538 | 0.257253 / 0.257251 USD (0.001%) | -0.149% | -0.149% (leave-one-out; küszöb ≤ 10%: teljesül) |
| F3V2 | 2939.52 / 12.0797 / 4.6518 ; 117.52 / 3.4544 | 0.999999 | 1.194298 | 0.256731 / 0.256731 USD (0.0%) | -0.148% | -0.148% (leave-one-out; küszöb ≤ 10%: teljesül) |

Az újrakérések cost-ja nem lineáris a tokenben (a megismételt előtag gyorsítótárazott), ezért az újrakérést nem tokenből, hanem a mért M szorzóval vetítjük.

| réteg (F22) | F3 (prompt v1) USD [90%] | F3V2 (prompt v2) USD [90%] |
|---|---|---|
| ÓSZ-próza | 19.498 [17.3915–21.7333] | 19.2778 [17.3559–21.171] |
| költészet | 4.8749 [4.3993–5.4167] | 4.9671 [4.5063–5.4401] |
| próféta | 7.8775 [7.0293–8.7774] | 7.8015 [7.0186–8.571] |
| evangélium+ApCsel | 6.0193 [5.4011–6.6994] | 6.0195 [5.4425–6.6098] |
| levél+Jel | 3.9656 [3.5585–4.4128] | 3.967 [3.5873–4.3558] |
| Összes | 42.2353 [37.7848–47.034] | 42.033 [37.9527–46.1502] |

| réteg (pilot-4, tájékoztató) | F3 USD [90%] | F3V2 USD [90%] |
|---|---|---|
| R1 | 20.7157 [18.4867–23.0838] | 20.5079 [18.4766–22.515] |
| R2 | 3.4895 [3.1504–3.8685] | 3.5672 [3.2356–3.9119] |
| R3 | 8.0427 [7.1768–8.9604] | 7.9682 [7.1701–8.7547] |
| R4 | 9.9849 [8.9596–11.1123] | 9.9865 [9.0298–10.9656] |
| Összes | 42.2328 [37.782–47.0314] | 42.0298 [37.9494–46.1468] |

A két besorolás különbsége (tájékoztató, F22 − pilot-4): F3 0.002501 USD (0.0059%), F3V2 0.003159 USD (0.0075%).

**Kézimunka-vetítés (C):** az aranyon mért eltérés/vers és a (c)-hiba/vers (ez utóbbi Opus-besorolás, nem mérés), F22-rétegenként a teljes Bibliára (a minta aranyversei könyv szerint leképezve); a rétegenkénti arany kis mintájú (10–20 vers). `alacsony` arány: n.é. (PD6).

| futás | eltérés/vers (mért, 60 aranyvers) | vetített eltérés a Bibliára (F22) | (c)/vers (Opus-besorolás, nem mérés) | vetített (c) a Bibliára (F22; Opus-besorolás, nem mérés) | tájékoztató, pilot-4: eltérés / (c) |
|---|---|---|---|---|---|
| F3 | 2.2 | 73363 | 0.6167 | 15888 | 69608 / 18340 |
| F3V2 | 1.6833 | 60478 | 0.65 | 19308 | 54649 / 20625 |

## (e) A DT21 tételei, átvihető eszközök, megtanult korlátok

**A #22:** a döntés elhalasztva a regressziós futás utánra; brief-diff nem készül, teljes futás nem indul; marad `dontesre_var`.

### Az a–e tétel: regressziós mérésre átvéve (DT21 döntés: a–e a jegyzet v2-be, prompt_v3, F3V3)

1. **G / K7:** a prompt_v2 G-szabályának kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet K7-e (*tudja vala*, *megy vala*): melyik az irányadó.
2. **C:** a prompt „azt, őt …” felsorolása a C-nél az *'et* nélküli, betoldott tárgyi névmásokra is általánosult.
3. **„azt … hogy” / „azért … hogy”:** az arany az előbbit betoldásnak veszi, az utóbbit (Mt 21:4) köti.
4. **2Móz 26:13 *is*:** a K9 szerint a *ve-* az *is*-hez köthető volna; az arany v2 forditatlan-nak veszi (az F3V2-nél (b)).
5. **D:** a birtokláncban (*szolgálójának szemét*) nem egyértelmű, melyik szó viseli a ragot.

### Lezárt tételek (f–k; felhasználói döntés, DT21)

- **f)** a P5 bootstrap-egysége a köteg: elfogadva (felhasználói döntés).
- **g)** költség-ellenőrzés: a mintán belüli és a leave-one-out közül a konzervatívabb (nagyobb abszolút eltérésű) számít; ez minden futásnál a leave-one-out (P5-táblák, „számító” oszlop).
- **h)** a teljes Biblia rétegbesorolása: az F22 brief 22.2 műfaji öt rétege (Préd, Sir → költészet, Dán → próféta, Ruth, Eszt → ÓSZ-próza a felhasználó döntése szerint); a korábbi pilot-4-réteges besorolás tájékoztató; a pilot mérési rétegei (R1–R4) változatlanok. Nyitott marad: az ApCsel és a Jel nincs a mintában.
- **i)** régi arany: a mért érték a kizárás nélküli (C, F3V2: 93.8% (30/32) — a 95% alatt); a kizárásos érték csak tájékoztató (az 1Móz 6:17 nélkül: 96.8% (30/31)); az 1Móz 13:4 hibás-jelölése visszavonva.
- **j)** a gondolkodási mód eltérése a pilot idején elfogadva.
- **k)** az A+B+C-nél a szó szerinti olvasat számít (59.7% (2086/3493)), az A+B definíciója elfogadva.

### Az F22-re átvihető eszközök

- prompt: f21p/prompt_v1.md, f21p/prompt_v2.md (a tíz konvenció szabályként);
- kapu: eszkozok/karoli_strong/kapu.py (ötpontos, újrakéréssel);
- arany v2: f21p/arany_opus_v2.jsonl (befagyasztva, sha256: f21p/arany_opus_v2.sha256), a jegyzettel;
- eszkozok/karoli_strong/tokenek.py (tokenizálás, TR-jelölés, kizárás), futtat.py (futtató, plafon, --szaraz, --onteszt), meres.py és meres_v2.py (mérés), c_diff.py és c_diff_f3v2.py (diff és besorolás-váz), koltseg_vetit.py, ingadozas.py.

### Megtanult korlátok

- TAHOT-sorrend: 57 vers kivonatbeli sorrendje nem a szórend (f21p/sorrend_eltero_versek.tsv), ezek a mintából kimaradtak.
- X / Q(K) változatsorok: a Ketiv / Qere és az üres helyőrzők a kivonatban nem mind látszanak (l. f21p/arany_opus_jegyzetek.md 3. szakasz).
- `[nem TR]`: a „TR»N / TR«N” jelölés javítva (PD7); a 200 verses mintában most 20 `[nem TR]` token, az „eltérő alak” tokenek kizárva.
- Összetett Strong a régi aranyban: 68 hármas „+”-os Stronggal; halmaz-definícióval mérve (PD9).
- Az A és a B JSON-hibái: első próbára érvénytelen JSON A 50.0% (100/200), B 20.0% (40/200) (meres_eredmeny.tsv, kapuhiba_tipus).
- A C gondolkodási tokenje a naplóban és a nyers usage-ban 0 (minimal effort); a nyers usage tárolása az F3V2-től.
- Gondolkodási mód (eltérés a brief Keretek pontjától, amely mindhárom modellnél azonos beállítást kért; DT21 j: a pilot idején elfogadva): az A és a B kikapcsolva, a C-nél a gondolkodás kötelező, `minimal` szinten. Az F1–F6 napló `gondolkodas_token` = 0 értéke nem mérés (a token olvasása csak az F21.10-től él); a nyers usage az F3V2-től tárolt, abban is 0. A költség ettől helyes, mert a `cost` mezőből jön.
- A prompt-szabályok túlkötést okozhatnak: az F3V2 több linket ad (1090 link az F3 1061-ével szemben, arany v2).

### A #22 opcióinak következményei (tények, ajánlás nélkül)

- **Marad (a jelenlegi céllal):** a P3b-adaton az A+B és az A+B+C mért, és a Döntési szabály szerint egyik sem felel meg (a bukott feltételek a P3b-szakaszban); az A, a B és a C egymodelles, a PD6 szerint nem minősíthető. A teljes futás a jelenlegi szabállyal nem indítható.
- **Módosított céllal indul:** minden összeállítás mért adata (pontosság, lefedettség, régi arany, kapuhiba, bizonyossági szintek, vetített költség) rendelkezésre áll; a Döntési szabály, a PD6 vagy a G4 módosítása felhasználói döntés; az a–e tétel és a prompt túlkötése regressziós mérésre átvéve (jegyzet v2, prompt_v3, F3V3).
- **Elhalasztva:** az eszközök, az arany v2 és a mért adat megmarad; az a–e tétel regressziós mérésre átvéve, a lezárt f–k tétel dokumentálva.

## (f) A korrigált értékek (Opus-besorolás, nem mérés)

A küszöb szempontjából csak a mért érték számít. A (c)-hibák (az arany szerinti valódi C-hibák) darabszáma az Opus besorolása: F3 × arany v1: 37; F3 × arany v2: 37; F3V2 × arany v2: 39 (f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv). A korrigált pontosság és lefedettség: naplok/F21P_C_diff.md és naplok/F21P_C_diff_F3V2.md, ugyanezzel a jelöléssel.


## Javaslat — a #22 választott iránya (a felhasználó döntése, javaslatként rögzítve; a #22 briefje ezzel nem változik, brief-diff nem készül, teljes futás nem indul)

A felhasználó szó szerinti iránya (PD19 (3), DT32):

> „Sonnet a Code-ban + C az Actionsben, könyvenként, a Genezissel kezdve; `magas` = egyezés, eltérésnél a Sonnet változata `alacsony` jelöléssel; a próféták kötegmérete 5 vers; az 1Móz 1–5 után `/usage`-jelentés, és megállás, ha a teljes Genezisre vetítve a heti keret 50%-a fölött van.”

Az irány elemei és a mért adatok, amelyekre a döntés épül (rögzítés, ajánlás nélkül; a számok forrása f21p/koltseg_vetites_p3c.tsv és f21p/meres_p3c_eredmeny.tsv):

- **Futtatási környezet.** A Sonnet a Claude Code-ban fut, az előfizetési (heti) kereten belül; a C (F3V3 beállítás, prompt_v3) a GitHub Actionsben, OpenRouter-költségen. A mért adatok szerint a Sonnet teljes Bibliára vetített OpenRouter-költsége 373.9405 [337.9675–418.6543] USD, a C-é 42.4899 [38.5542–46.5194] USD, a páré 416.4304 [379.8793–460.9697] USD (90%-os intervallum; a (4) küszöb 60 USD): ezért fut a Sonnet a Code-ban. A Code-ban futó Sonnet a heti keretet terheli; erre a pilotnak nincs mért adata.
- **Könyvenként, a Genezissel kezdve.** Az 1Móz 1533 vers, ebből az 1Móz 1–5 138 vers (Károli-kivonat).
- **`magas` = egyezés.** Ez a pár mérésének logikája (A∩B, döntőbíró nélkül): a két modell egyező linkje `magas`. A mért `magas`-pontosság rétegenként: R1 98.3% (291/296), R2 99.3% (149/150), R3 — (0/0), R4 98.7% (294/298); az R3 nem mérhető (0/0).
- **Eltérésnél a Sonnet változata `alacsony` jelöléssel** kerül be (nem a C-é). A pár mérésében az `alacsony` arány 19.1% (700/3673) (200 vers, mért), 21.4% (a teljes Bibliára vetítve), az R3-ban 55.9% (347/621); ez a mérés a két modell nem egyező linkjeit együtt (és a kapuhibás oldal mellett a túlélő oldal linkjeit) számolja, ezért a csak Sonnet-változatot tartalmazó kimenet `alacsony` aránya ettől eltérhet (nem mért).
- **A próféták kötegmérete 5 vers.** Ok: a Sonnet R3-kötege (15.) mindkét próbán length-lezárással végződött (finish_reason=length: köteg 15 / próba 1, köteg 15 / próba 2; költségük 0.291850 USD; kimenet 12000+12000 token, ebből gondolkodás 11144+10364), és a köteg tíz R3-aranyverse végleg kapuhibás; a pótlás a próféták előtt (kis köteg a hosszú gondolkodás miatt). A próféta réteg (F22) 5332 vers: 10 verses kötegben 534, 5 versesben 1067 köteg.
- **A `/usage`-jelentés és az 50%-os megállási feltétel.** A heti keret felhasználását a Claude Code `/usage` parancsa mutatja; a leolvasást a felhasználó végzi (vagy a `/usage` kimenetét adja át), az 1Móz 1–5 előtt és után. A mérték: a teljes Genezisre vetített felhasználás = (az 1Móz 1–5 alatt felhasznált heti keret) × (az 1Móz versszáma / az 1Móz 1–5 versszáma) = × 1533/138 (≈ × 11.11); megállás, ha ez a heti keret 50%-a fölött van. A Sonnet tokenigényéről a pilot mért adata (OpenRouter, 200 vers): 142077 gondolkodási token a 173414 kimeneti tokenből; hívásonként legfeljebb 11144.
- **Kapcsolódó állapotok.** A #22 fejléce `dontesre_var` (a briefje nem változik). Az F31-brief (F31_F21R_BRIEF.md, `nem_indult`) a regressziós mérést írja le, amely ezen az ágon, a pilot PD13–PD19 döntései szerint lefutott: az átfedés kezelése a felhasználó döntése.

