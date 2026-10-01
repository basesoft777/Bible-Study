# F21P_kjv_meres.md — KJV-mérés: F8V3 (teljes KJV-tábla, minden rétegben) az F3V3-mal szemben

<!-- GENERÁLT: eszkozok/karoli_strong/meres_kjv.py | scope=KJV-mérés (F21.67): F8V3 (C, prompt_v3, 200 vers, KJV-támpont a teljes KJV-táblából) az F3V3-mal szemben (C, prompt_v3, KJV csak az R1-en, régi tábla); ingadozás: F3V2, F3V2B; arany arany_opus_v3.jsonl (60 vers, sha256 acdeb55f969c96fe) | forras=f21p/valaszok/{F3V3,F8V3,F3V2,F3V2B}.jsonl, arany_opus_v3.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, f21p/minta.tsv, konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/KJV_Strongs_teljes.tsv, f21p/futasnaplo.tsv | ts=2026-10-01T07:25:58+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

Kizárólag szkriptkimenet; a jelentés nem von le következtetést, csak a számokat és az olvasási korlátokat adja. Cellaforma: érték (számláló/nevező). A mérés az arany **arany_opus_v3.jsonl** változatára megy (60 vers, hash ellenőrizve). Rétegek: R1–R4; „R2+R3” = a két réteg együtt (ahol a KJV-sor az F3V3-hoz képest tényleg új); „Összes” = R1–R4.

## 0. A két futás beállítása és a KJV-sor jelenléte

- F3V3: google/gemini-3.8-flash | kotelezo_effort=minimal | prompt 84f12ca7aafb; KJV-forrás: regi
- F8V3: google/gemini-3.8-flash | kotelezo_effort=minimal | prompt 84f12ca7aafb; KJV-forrás: teljes

| futás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3 | versek KJV-sorral (a 200-ból) | 100/100 | 0/25 | 0/25 | 0/50 | 0/50 | 100/200 |
| F8V3 | versek KJV-sorral (a 200-ból) | 100/100 | 24/25 | 25/25 | 49/50 | 0/50 | 149/200 |

Keresztellenőrzések a KJV-sorra:
- F8V3: kjv_sorral_versek_jsonl_vs_ujraszamolt jsonl kjv_forras.kjv_sorral_versek (149) = újraszámolt (149): EGYEZIK
- F3V3: kjv_sorral_versek_minta_vs_ujraszamolt minta.tsv kjv_tamapont=van (100) = újraszámolt régi-tábla (100): EGYEZIK
- F8V3: kjv_tabla_sha256_a_jsonlban 5a7891145401aa62dd8aac31d0192eecb112daf780461279a84912fe40826a2e

## a) Pontosság és lefedettség (a kapun átment aranyverseken; „sajat” = a futás saját halmaza)

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V3 | pontossag | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 95.1% (407/428) | 94.4% (306/324) | 95.3% (1009/1059) |
| F3V3 | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.6% (407/417) | 97.5% (306/314) | 96.3% (1009/1048) |
| F8V3 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F8V3 | pontossag | 94.6% (298/315) | 99.3% (151/152) | 95.8% (253/264) | 97.1% (404/416) | 94.4% (303/321) | 95.5% (1005/1052) |
| F8V3 | lefedettseg | 94.0% (298/317) | 99.3% (151/152) | 95.5% (253/265) | 96.9% (404/417) | 96.5% (303/314) | 95.9% (1005/1048) |
| F3V2 | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2 | pontossag | 94.0% (299/318) | 95.0% (152/160) | 93.8% (258/275) | 94.3% (410/435) | 91.4% (308/337) | 93.3% (1017/1090) |
| F3V2 | lefedettseg | 94.3% (299/317) | 100.0% (152/152) | 97.4% (258/265) | 98.3% (410/417) | 98.1% (308/314) | 97.0% (1017/1048) |
| F3V2B | arany_versek_kapun_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2B | pontossag | 93.8% (304/324) | 95.0% (151/159) | 93.6% (262/280) | 94.1% (413/439) | 90.3% (306/339) | 92.8% (1023/1102) |
| F3V2B | lefedettseg | 95.9% (304/317) | 99.3% (151/152) | 98.9% (262/265) | 99.0% (413/417) | 97.5% (306/314) | 97.6% (1023/1048) |

A páros halmaz („kozos”: mindkét összevetett futás átment; ezen megy a Δ):

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3 [pár: F3V3–F8V3] | arany_versek_mindketto_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V3 [pár: F3V3–F8V3] | pontossag | 96.4% (296/307) | 96.2% (152/158) | 94.4% (255/270) | 95.1% (407/428) | 94.4% (306/324) | 95.3% (1009/1059) |
| F3V3 [pár: F3V3–F8V3] | lefedettseg | 93.4% (296/317) | 100.0% (152/152) | 96.2% (255/265) | 97.6% (407/417) | 97.5% (306/314) | 96.3% (1009/1048) |
| F8V3 [pár: F3V3–F8V3] | arany_versek_mindketto_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F8V3 [pár: F3V3–F8V3] | pontossag | 94.6% (298/315) | 99.3% (151/152) | 95.8% (253/264) | 97.1% (404/416) | 94.4% (303/321) | 95.5% (1005/1052) |
| F8V3 [pár: F3V3–F8V3] | lefedettseg | 94.0% (298/317) | 99.3% (151/152) | 95.5% (253/265) | 96.9% (404/417) | 96.5% (303/314) | 95.9% (1005/1048) |
| F3V2 [pár: F3V2–F3V2B] | arany_versek_mindketto_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2 [pár: F3V2–F3V2B] | pontossag | 94.0% (299/318) | 95.0% (152/160) | 93.8% (258/275) | 94.3% (410/435) | 91.4% (308/337) | 93.3% (1017/1090) |
| F3V2 [pár: F3V2–F3V2B] | lefedettseg | 94.3% (299/317) | 100.0% (152/152) | 97.4% (258/265) | 98.3% (410/417) | 98.1% (308/314) | 97.0% (1017/1048) |
| F3V2B [pár: F3V2–F3V2B] | arany_versek_mindketto_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2B [pár: F3V2–F3V2B] | pontossag | 93.8% (304/324) | 95.0% (151/159) | 93.6% (262/280) | 94.1% (413/439) | 90.3% (306/339) | 92.8% (1023/1102) |
| F3V2B [pár: F3V2–F3V2B] | lefedettseg | 95.9% (304/317) | 99.3% (151/152) | 98.9% (262/265) | 99.0% (413/417) | 97.5% (306/314) | 97.6% (1023/1048) |

## b) A különbség: F8V3 − F3V3, páros bootstrap (versek felett, rétegzett, 1 000 újramintavétel, mag 20260930), az ingadozással összevetve

Δ = F8V3 − F3V3 a közös (mindkét futás által átment) aranyversek linkjein (pontosság, lefedettség) és a 200 versen (kapuhiba); a „Δ 90%” a bootstrap 5.–95. percentilise. Ingadozás-becslés: F3V2B − F3V2 (azonos prompt, azonos bemenet), ugyanazokkal a mérőszámokkal és ugyanazzal a bootstrappel, az arany v3-ra mérve. Két leíró jelölés külön: **[0∉]** = a Δ 90%-os intervalluma nem tartalmazza a 0-t; **[>zaj]** = |Δ| > |F3V2B − F3V2|. Nem szignifikanciapróba.

| réteg | mérőszám | F3V3 | F8V3 | Δ | Δ 90% | ingadozás (F3V2B − F3V2) | ingadozás 90% | jelölés | n (arany / 200) |
|---|---|---|---|---|---|---|---|---|---|
| R1 | pontossag | 96.4% | 94.6% | -1.8 pp | [-4.2; +0.8 pp] | -0.2 pp | [-2.4; +1.9 pp] | [>zaj] | 20 / 100 |
| R1 | lefedettseg | 93.4% | 94.0% | +0.6 pp | [-0.7; +2.1 pp] | +1.6 pp | [-1.9; +4.5 pp] | — | 20 / 100 |
| R1 | kapuhiba_elso_probara | 12.0% | 10.0% | -2.0 pp | [-4.0; +0.0 pp] | +9.0 pp | [+3.0; +15.0 pp] | — | 20 / 100 |
| R1 | kapuhiba_vegleg | 0.0% | 0.0% | +0.0 pp | [+0.0; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | — | 20 / 100 |
| R2 | pontossag | 96.2% | 99.3% | +3.1 pp | [+1.1; +5.0 pp] | -0.0 pp | [-2.6; +3.5 pp] | [0∉] [>zaj] | 10 / 25 |
| R2 | lefedettseg | 100.0% | 99.3% | -0.7 pp | [-1.7; +0.0 pp] | -0.7 pp | [-1.8; +0.0 pp] | — | 10 / 25 |
| R2 | kapuhiba_elso_probara | 0.0% | 4.0% | +4.0 pp | [+0.0; +12.0 pp] | +20.0 pp | [+8.0; +32.0 pp] | — | 10 / 25 |
| R2 | kapuhiba_vegleg | 0.0% | 0.0% | +0.0 pp | [+0.0; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | — | 10 / 25 |
| R3 | pontossag | 94.4% | 95.8% | +1.4 pp | [-0.5; +3.4 pp] | -0.2 pp | [-1.8; +1.1 pp] | [>zaj] | 10 / 25 |
| R3 | lefedettseg | 96.2% | 95.5% | -0.8 pp | [-2.5; +1.5 pp] | +1.5 pp | [+0.4; +2.9 pp] | — | 10 / 25 |
| R3 | kapuhiba_elso_probara | 40.0% | 36.0% | -4.0 pp | [-32.0; +28.0 pp] | -4.0 pp | [-12.0; +0.0 pp] | [>zaj] | 10 / 25 |
| R3 | kapuhiba_vegleg | 8.0% | 0.0% | -8.0 pp | [-20.0; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | [>zaj] | 10 / 25 |
| R2+R3 | pontossag | 95.1% | 97.1% | +2.0 pp | [+0.6; +3.5 pp] | -0.2 pp | [-1.6; +1.1 pp] | [0∉] [>zaj] | 20 / 50 |
| R2+R3 | lefedettseg | 97.6% | 96.9% | -0.7 pp | [-1.9; +0.8 pp] | +0.7 pp | [-0.2; +1.6 pp] | [>zaj] | 20 / 50 |
| R2+R3 | kapuhiba_elso_probara | 20.0% | 20.0% | +0.0 pp | [-16.0; +16.0 pp] | +8.0 pp | [+2.0; +16.0 pp] | — | 20 / 50 |
| R2+R3 | kapuhiba_vegleg | 4.0% | 0.0% | -4.0 pp | [-10.0; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | [>zaj] | 20 / 50 |
| R4 | pontossag | 94.4% | 94.4% | -0.1 pp | [-2.2; +1.5 pp] | -1.1 pp | [-3.0; +0.9 pp] | — | 20 / 50 |
| R4 | lefedettseg | 97.5% | 96.5% | -1.0 pp | [-1.7; -0.3 pp] | -0.6 pp | [-1.8; +0.3 pp] | [0∉] [>zaj] | 20 / 50 |
| R4 | kapuhiba_elso_probara | 16.0% | 0.0% | -16.0 pp | [-24.0; -8.0 pp] | -8.0 pp | [-16.0; +0.0 pp] | [0∉] [>zaj] | 20 / 50 |
| R4 | kapuhiba_vegleg | 0.0% | 0.0% | +0.0 pp | [+0.0; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | — | 20 / 50 |
| Összes | pontossag | 95.3% | 95.5% | +0.2 pp | [-0.8; +1.3 pp] | -0.5 pp | [-1.6; +0.6 pp] | — | 60 / 200 |
| Összes | lefedettseg | 96.3% | 95.9% | -0.4 pp | [-1.1; +0.4 pp] | +0.6 pp | [-0.5; +1.6 pp] | — | 60 / 200 |
| Összes | kapuhiba_elso_probara | 15.0% | 10.0% | -5.0 pp | [-9.5; -0.5 pp] | +4.5 pp | [+0.5; +8.5 pp] | [0∉] [>zaj] | 60 / 200 |
| Összes | kapuhiba_vegleg | 1.0% | 0.0% | -1.0 pp | [-2.5; +0.0 pp] | +0.0 pp | [+0.0; +0.0 pp] | [>zaj] | 60 / 200 |

## c) Kapuhiba első próbára és végleg (a 200 versen, rétegenként)

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3 | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 40.0% (10/25) | 20.0% (10/50) | 16.0% (8/50) | 15.0% (30/200) |
| F3V3 | vegleg | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 4.0% (2/50) | 0.0% (0/50) | 1.0% (2/200) |
| F8V3 | elso_probara | 10.0% (10/100) | 4.0% (1/25) | 36.0% (9/25) | 20.0% (10/50) | 0.0% (0/50) | 10.0% (20/200) |
| F8V3 | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/50) | 0.0% (0/200) |
| F3V2 | elso_probara | 12.0% (12/100) | 0.0% (0/25) | 8.0% (2/25) | 4.0% (2/50) | 10.0% (5/50) | 9.5% (19/200) |
| F3V2 | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/50) | 0.0% (0/200) |
| F3V2B | elso_probara | 21.0% (21/100) | 20.0% (5/25) | 4.0% (1/25) | 12.0% (6/50) | 2.0% (1/50) | 14.0% (28/200) |
| F3V2B | vegleg | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/50) | 0.0% (0/200) |

Keresztellenőrzés (újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg):

- F3V3: újraszámolt első-próbás hibás versek (30) = jsonl probalkozas=2 versek (30) = napló kapuhiba_db(probalkozas=1) összeg (30): EGYEZIK
- F8V3: újraszámolt első-próbás hibás versek (20) = jsonl probalkozas=2 versek (20) = napló kapuhiba_db(probalkozas=1) összeg (20): EGYEZIK
- F3V2: újraszámolt első-próbás hibás versek (19) = jsonl probalkozas=2 versek (19) = napló kapuhiba_db(probalkozas=1) összeg (19): EGYEZIK
- F3V2B: újraszámolt első-próbás hibás versek (28) = jsonl probalkozas=2 versek (28) = napló kapuhiba_db(probalkozas=1) összeg (28): EGYEZIK

### Hibatípusok kapupont szerint (hibás versek száma a rétegben a 200-ból; egy vers több ponton is hibázhat)

| összeállítás | mérőszám | Összes | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|
| F3V3 | kapupont_1_elso | 3.5% (7/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 14.0% (7/50) |
| F3V3 | kapupont_1_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_1-json_elso | 10.0% (20/200) | 10.0% (10/100) | 0.0% (0/25) | 40.0% (10/25) | 0.0% (0/50) |
| F3V3 | kapupont_1-json_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_2_elso | 0.5% (1/200) | 1.0% (1/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_2_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_3_elso | 0.5% (1/200) | 1.0% (1/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_3_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F3V3 | kapupont_4_elso | 1.0% (2/200) | 1.0% (1/100) | 0.0% (0/25) | 0.0% (0/25) | 2.0% (1/50) |
| F3V3 | kapupont_4_vegleg | 1.0% (2/200) | 0.0% (0/100) | 0.0% (0/25) | 8.0% (2/25) | 0.0% (0/50) |
| F8V3 | kapupont_1_elso | 4.5% (9/200) | 0.0% (0/100) | 0.0% (0/25) | 36.0% (9/25) | 0.0% (0/50) |
| F8V3 | kapupont_1_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F8V3 | kapupont_1-json_elso | 5.0% (10/200) | 10.0% (10/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F8V3 | kapupont_1-json_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |
| F8V3 | kapupont_3_elso | 0.5% (1/200) | 0.0% (0/100) | 4.0% (1/25) | 0.0% (0/25) | 0.0% (0/50) |
| F8V3 | kapupont_3_vegleg | 0.0% (0/200) | 0.0% (0/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) |

Végleges kapuhibás versek: F3V3: Ézs 48:5 (R3, kapupont 4); F3V3: Jer 16:3 (R3, kapupont 4)

Mentett (allapot=ok) válaszok újraellenőrzése a teljes kapun:

- F3V3: 0 hiba (futtat.mentett_valaszok_ellenoriz: 0 hiba)
- F8V3: 0 hiba (futtat.mentett_valaszok_ellenoriz: 0 hiba)
- F3V2: 0 hiba (futtat.mentett_valaszok_ellenoriz: 0 hiba)
- F3V2B: 0 hiba (futtat.mentett_valaszok_ellenoriz: 0 hiba)

## d) Régi arany egyezés (halmaz-definíció; MÉRT = kizárás nélküli; tájékoztató: 1Móz 6:17 kizárva; a kapun átment versekre)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V3 | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| F3V3 | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |
| F8V3 | regi_arany_kizaras_nelkul | 93.8% (30/32) | — (0/0) | — (0/0) | — (0/0) | 93.8% (30/32) |
| F8V3 | regi_arany_kizarassal_tajekoztato | 96.8% (30/31) | — (0/0) | — (0/0) | — (0/0) | 96.8% (30/31) |

## f) Érintett linkek és szavak (az aranyversek, ahol az F3V3 és az F8V3 is átment)

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes | R2+R3, KJV-sorral az F8V3-ban | R2+R3, KJV-sor nélkül az F8V3-ban |
|---|---|---|---|---|---|---|---|---|---|
| F3V3/F8V3 | aranyversek_mindketto_atment | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (20/20) | 100.0% (60/60) | 100.0% (19/19) | 100.0% (1/1) |
| F3V3/F8V3 | link_hiany_potolva | 4 | 0 | 6 | 6 | 0 | 10 | 6 | 0 |
| F3V3/F8V3 | link_tobblet_megszunt | 6 | 5 | 9 | 14 | 8 | 28 | 13 | 1 |
| F3V3/F8V3 | link_hiany_uj | 2 | 1 | 8 | 9 | 3 | 14 | 9 | 0 |
| F3V3/F8V3 | link_tobblet_uj | 12 | 0 | 5 | 5 | 8 | 25 | 5 | 0 |
| F3V3/F8V3 | link_javitott_osszes (hiany_potolva + tobblet_megszunt) | 10 | 5 | 15 | 20 | 8 | 38 | 19 | 1 |
| F3V3/F8V3 | link_romlott_osszes (hiany_uj + tobblet_uj) | 14 | 1 | 13 | 14 | 11 | 39 | 14 | 0 |
| F3V3/F8V3 | szo_javult | 2.7% (7/261) | 4.2% (5/120) | 3.9% (9/230) | 4.0% (14/350) | 2.4% (7/294) | 3.1% (28/905) | 3.8% (13/339) | 9.1% (1/11) |
| F3V3/F8V3 | szo_romlott | 4.6% (12/261) | 0.0% (0/120) | 4.3% (10/230) | 2.9% (10/350) | 3.4% (10/294) | 3.5% (32/905) | 2.9% (10/339) | 0.0% (0/11) |
| F3V3/F8V3 | szo_valtozott_rossz_marad | 1.1% (3/261) | 0.8% (1/120) | 1.3% (3/230) | 1.1% (4/350) | 0.3% (1/294) | 0.9% (8/905) | 1.2% (4/339) | 0.0% (0/11) |
| F3V3/F8V3 | szo_nem_valtozott_jo | 84.3% (220/261) | 95.0% (114/120) | 87.4% (201/230) | 90.0% (315/350) | 87.8% (258/294) | 87.6% (793/905) | 90.0% (305/339) | 90.9% (10/11) |
| F3V3/F8V3 | szo_nem_valtozott_rossz | 7.3% (19/261) | 0.0% (0/120) | 3.0% (7/230) | 2.0% (7/350) | 6.1% (18/294) | 4.9% (44/905) | 2.1% (7/339) | 0.0% (0/11) |

Link-szint: **hiány pótolva** = arany-link, az F3V3-ban hiányzott, az F8V3-ban megvan; **többlet megszűnt** = az F3V3-ban (aranyban nem szereplő) többlet-link, az F8V3-ban nincs; **hiány új** = arany-link, az F3V3-ban megvolt, az F8V3-ban hiányzik; **többlet új** = az F8V3-ban új, aranyban nem szereplő link. Szó-szint: egy magyar szó linkhalmaza pontosan az arany (javult: F3V3-ban nem, F8V3-ban igen; romlott: fordítva; változott_rossz_marad: mindkettő eltér az aranytól és egymástól is). Az érintett linkek és szavak teljes listája az `erintett_link` és `erintett_szo` szakaszban áll (f21p/kjv_meres_eredmeny.tsv).

### Jellemző példák az R2–R3 versekből (szó-szint; versenként körbejárva, a minta sorrendjében; a kiválasztás szabálya determinisztikus, nem szubjektív)

**Javult (F3V3-ban nem, F8V3-ban pontosan az arany)**

| vers | réteg | leírás |
|---|---|---|
| Jób 33:13 | R2 | magyar: Azért; eredeti – arany: —; F3V3: 5 כִּ֥י (that); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Zsolt 16:11 | R2 | magyar: Te; eredeti – arany: —; F3V3: 1 תּֽוֹדִיעֵ (you will make known to); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Zsolt 18:1 | R2 | magyar: azon; eredeti – arany: —; F3V3: 18 בְּ (on); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Zsolt 22:32 | R2 | magyar: ő; eredeti – arany: —; F3V3: 8 נ֝וֹלָ֗ד (about to be born); F8V3: —; KJV-sor az F8V3-ban: nincs, az F3V3-ban: nincs |
| Jer 46:21 | R3 | magyar: megfenyíttetésök; eredeti – arany: 26 פְּקֻדָּתָֽ (punishment), 27 ם (their); F3V3: 26 פְּקֻדָּתָֽ (punishment); F8V3: 26 פְּקֻדָּתָֽ (punishment), 27 ם (their); KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Jer 51:3 | R3 | magyar: kézíves; eredeti – arany: 4 דֹּרֵךְ֙ ([one] bending); F3V3: 2 יִדְרֹ֤ךְ (he bend), 4 דֹּרֵךְ֙ ([one] bending); F8V3: 4 דֹּרֵךְ֙ ([one] bending); KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Ez 22:25 | R3 | magyar: prófétái; eredeti – arany: 2 נְבִיאֶ֙י (prophets), 3 הָ֙ (its); F3V3: 2 נְבִיאֶ֙י (prophets); F8V3: 2 נְבִיאֶ֙י (prophets), 3 הָ֙ (its); KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Ez 33:31 | R3 | magyar: szokott; eredeti – arany: —; F3V3: 6 מְבוֹא ([the] coming of); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |

**Romlott (F3V3-ban pontosan az arany, F8V3-ban nem)**

| vers | réteg | leírás |
|---|---|---|
| Jer 46:21 | R3 | magyar: olyanok; eredeti – arany: 7 כְּ ([are] like); F3V3: 7 כְּ ([are] like); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Jer 51:3 | R3 | magyar: fel; eredeti – arany: 2 יִדְרֹ֤ךְ (he bend); F3V3: 2 יִדְרֹ֤ךְ (he bend); F8V3: 9 יִתְעַ֖ל (he lift); KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Ez 16:57 | R3 | magyar: valóknak; eredeti – arany: 13 סְבִיבוֹתֶ֖י (around); F3V3: 13 סְבִיבוֹתֶ֖י (around); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Ez 30:5 | R3 | magyar: együtt; eredeti – arany: 17 אִתָּ֖ (with); F3V3: 17 אִתָּ֖ (with); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |
| Ez 33:31 | R3 | magyar: oda; eredeti – arany: 9 יֵשְׁב֤וּ (they may sit); F3V3: 9 יֵשְׁב֤וּ (they may sit); F8V3: —; KJV-sor az F8V3-ban: van, az F3V3-ban: nincs |

## g) Költség és tokenek (a futásnaplóból)

| futás | mérőszám | érték | megjegyzés |
|---|---|---|---|
| F3V3 teljes | hivasok | 26 | próbálkozás=1: 20, próbálkozás=2: 6 |
| F3V3 teljes | bemeneti_token | 226300 |  |
| F3V3 teljes | kimeneti_token | 30719 |  |
| F3V3 teljes | koltseg_usd | 0.260136 | koltseg_forras: openrouter |
| F3V3 teljes | beallitas | google/gemini-3.8-flash | kotelezo_effort=minimal | prompt 84f12ca7aafb |  |
| F8V3 teljes | hivasok | 23 | próbálkozás=1: 20, próbálkozás=2: 3 |
| F8V3 teljes | bemeneti_token | 201000 |  |
| F8V3 teljes | kimeneti_token | 29793 |  |
| F8V3 teljes | koltseg_usd | 0.262474 | koltseg_forras: openrouter |
| F8V3 ebből baleseti kötegek (1+2) | hivasok | 2 | próbálkozás=1: 2, próbálkozás=2: 0 |
| F8V3 ebből baleseti kötegek (1+2) | bemeneti_token | 17717 |  |
| F8V3 ebből baleseti kötegek (1+2) | kimeneti_token | 2652 |  |
| F8V3 ebből baleseti kötegek (1+2) | koltseg_usd | 0.023232 | koltseg_forras: openrouter |
| F8V3 teljes | beallitas | google/gemini-3.8-flash | kotelezo_effort=minimal | prompt 84f12ca7aafb |  |
| F8V3 − F3V3 (teljes) | hivasok | -3 | különbség; nevező: az F3V3 értéke |
| F8V3 − F3V3 (teljes) | bemeneti_token | -25300 | különbség; nevező: az F3V3 értéke |
| F8V3 − F3V3 (teljes) | kimeneti_token | -926 | különbség; nevező: az F3V3 értéke |
| F8V3 − F3V3 (teljes) | koltseg_usd | 0.002338 | különbség (az újrakérések és a kimenet is benne van) |

Az F8V3 első két kötege (1., 2.) helyi baleset eredménye (naplok/F21_baleset_F8V3.md; azonos futtató és konfiguráció); a fenti „teljes” sorok ezeket tartalmazzák, a „baleseti kötegek” sor külön mutatja őket. Köteg-szintű bemenet-összevetés (csak a próbálkozás=1 hívások, mert az újrakérések mérete eltér), a köteg rétegei szerint csoportosítva:

| köteg rétegei | kötegek | bemenet token F3V3 | bemenet token F8V3 | Δ (F8V3 − F3V3) | KJV-sor karakter F3V3 | KJV-sor karakter F8V3 | Δ karakter |
|---|---|---|---|---|---|---|---|
| R1 | 10 | 87477 | 85756 | -1721 (-2.0% (-1721/87477)) | 19616 | 13289 | -6327 |
| R2 | 2 | 13520 | 14492 | 972 (7.2% (972/13520)) | 0 | 1583 | 1583 |
| R2+R3 | 1 | 7952 | 8794 | 842 (10.6% (842/7952)) | 0 | 1343 | 1343 |
| R3 | 2 | 18769 | 20760 | 1991 (10.6% (1991/18769)) | 0 | 3281 | 3281 |
| R4 | 5 | 36690 | 36691 | 1 (0.0% (1/36690)) | 0 | 0 | 0 |

## h) A KJV-sor hossza a bemenetben (a „KJV-TÁMPONT: ” előtaggal és a sortöréssel)

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3 | versek_kjv_sorral | 100.0% (100/100) | 0.0% (0/25) | 0.0% (0/25) | 0.0% (0/50) | 0.0% (0/50) | 50.0% (100/200) |
| F3V3 | kjv_sor_karakter_osszes | 19616 | 0 | 0 | 0 | 0 | 19616 |
| F3V3 | kjv_sor_karakter_atlag_vers | 196 (19616/100) | — (0/0) | — (0/0) | — (0/0) | — (0/0) | 196 (19616/100) |
| F8V3 | versek_kjv_sorral | 100.0% (100/100) | 96.0% (24/25) | 100.0% (25/25) | 98.0% (49/50) | 0.0% (0/50) | 74.5% (149/200) |
| F8V3 | kjv_sor_karakter_osszes | 13289 | 2047 | 4160 | 6207 | 0 | 19496 |
| F8V3 | kjv_sor_karakter_atlag_vers | 133 (13289/100) | 85 (2047/24) | 166 (4160/25) | 127 (6207/49) | — (0/0) | 131 (19496/149) |

Köteg-szinten (karakter/köteg, a köteg rétegei szerint):

| futás | köteg rétegei | kötegek | átlag | min | max |
|---|---|---|---|---|---|
| F3V3 | R1 | 10 | 1962 (19616/10) | 1404 | 2370 |
| F3V3 | R2 | 2 | 0 (0/2) | 0 | 0 |
| F3V3 | R2+R3 | 1 | 0 (0/1) | 0 | 0 |
| F3V3 | R3 | 2 | 0 (0/2) | 0 | 0 |
| F3V3 | R4 | 5 | 0 (0/5) | 0 | 0 |
| F8V3 | R1 | 10 | 1329 (13289/10) | 960 | 1642 |
| F8V3 | R2 | 2 | 792 (1583/2) | 764 | 819 |
| F8V3 | R2+R3 | 1 | 1343 (1343/1) | 1343 | 1343 |
| F8V3 | R3 | 2 | 1640 (3281/2) | 1387 | 1894 |
| F8V3 | R4 | 5 | 0 (0/5) | 0 | 0 |

## i) Verszintű egyezés (hány vers kap azonos linkhalmazt; az F3V2–F3V2B pár az ingadozási alapvonal; az R4-en az F3V3/F8V3 bemenete azonos)

| összeállítás | mérőszám | R1 | R2 | R3 | R2+R3 | R4 | Összes |
|---|---|---|---|---|---|---|---|
| F3V3–F8V3 | versek_mindketto_atment [200 vers] | 100.0% (100/100) | 100.0% (25/25) | 92.0% (23/25) | 96.0% (48/50) | 100.0% (50/50) | 99.0% (198/200) |
| F3V3–F8V3 | azonos_linkhalmazu_versek [200 vers] | 47.0% (47/100) | 44.0% (11/25) | 30.4% (7/23) | 37.5% (18/48) | 58.0% (29/50) | 47.5% (94/198) |
| F3V3–F8V3 | link_egyezes (uniós arány) [200 vers] | 91.8% (1641/1787) | 93.2% (340/365) | 92.1% (523/568) | 92.5% (863/933) | 95.1% (808/850) | 92.8% (3312/3570) |
| F3V3–F8V3 | azonos_linkhalmazu_versek [arany] | 45.0% (9/20) | 50.0% (5/10) | 20.0% (2/10) | 35.0% (7/20) | 55.0% (11/20) | 45.0% (27/60) |
| F3V3–F8V3 | link_egyezes (uniós arány) [arany] | 92.6% (299/323) | 96.2% (152/158) | 90.0% (253/281) | 92.3% (405/439) | 94.3% (313/332) | 93.0% (1017/1094) |
| F3V2–F3V2B (ingadozás) | versek_mindketto_atment [200 vers] | 100.0% (100/100) | 100.0% (25/25) | 100.0% (25/25) | 100.0% (50/50) | 100.0% (50/50) | 100.0% (200/200) |
| F3V2–F3V2B (ingadozás) | azonos_linkhalmazu_versek [200 vers] | 44.0% (44/100) | 56.0% (14/25) | 44.0% (11/25) | 50.0% (25/50) | 38.0% (19/50) | 44.0% (88/200) |
| F3V2–F3V2B (ingadozás) | link_egyezes (uniós arány) [200 vers] | 92.1% (1692/1837) | 94.3% (346/367) | 94.6% (614/649) | 94.5% (960/1016) | 93.1% (810/870) | 93.0% (3462/3723) |
| F3V2–F3V2B (ingadozás) | azonos_linkhalmazu_versek [arany] | 45.0% (9/20) | 60.0% (6/10) | 30.0% (3/10) | 45.0% (9/20) | 30.0% (6/20) | 40.0% (24/60) |
| F3V2–F3V2B (ingadozás) | link_egyezes (uniós arány) [arany] | 89.4% (303/339) | 93.3% (154/165) | 93.4% (268/287) | 93.4% (422/452) | 93.1% (326/350) | 92.1% (1051/1141) |

## j) Olvasási korlátok

1. **A kontroll tisztátalan (R1).** Az R1-en mindkét futásban volt KJV-sor, de a forrás és a forma is más: az F3V3 a régi Genesis/Exodus/Proverbs táblából kapta (frázisok, üres szavú {H0853}-elemek), az F8V3 a konkordancia/KJV_Strongs_teljes.tsv-ből (csak tartalmi szavak + Strong, névelő/kötőszó/írásjel nélkül). Az R1-en tehát a különbség forrás- és formaváltás + futásközi ingadozás, nem tiszta „KJV nélkül/KJV-vel”.
2. **Az R4 hiánya.** Az ÚSZ-ön (R4; 50 vers a mintában, 20 az aranyban) az F8V3 sem kapott KJV-sort (a Károli ↔ KJV megfeleltetési tábla csak az ÓSZ-t fedi: KJV-sorral bíró R4 versek: 0/50). Az R4-en a két futás bemenete azonos, a különbség tiszta futásközi ingadozás.
3. **A KJV-hatás tiszta mérése az R2–R3-on van** (F3V3: nincs KJV-sor, F8V3: van; KJV-sorral az F8V3-ban: R2 24/25, R3 25/25 vers a 200-ból), de ott az aranyba eső versek száma kicsi (R2+R3: 20 aranyvers, ebből mindkét futás átment: 20).
4. **Az ingadozás-becslés egyetlen futáspár** (F3V2 és F3V2B, prompt_v2, arany v3-ra mérve; ugyanazon az aranyversek-halmazon a kapun átment verseken), tehát maga is zajos; a jelölések („0∉”, „>zaj”) leíró jelölések, nem szignifikanciapróbák, és a rétegenkénti cellák kis n-ű mintán (rétegenként 10–20 aranyvers) alapulnak.
5. A pontosság/lefedettség linkszintű, a bootstrap a versek felett, rétegzetten történik; a közös (mindkét futás által átment) halmaz a kapuhibás versek kiesése miatt kisebb lehet a saját halmazoknál (l. a) és f) szakasz).
6. A KJV-sor hossza a bemenetben és a bemeneti többlet token a köteg-szintű táblában áll; a futásnapló költségsorai az újrakéréseket is tartalmazzák, ezért a teljes költség-különbség nem csak a KJV-sor hatása.

