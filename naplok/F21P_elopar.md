# F21P_elopar.md — szkriptes előpárosítás (kísérlet), mérés az arany v3-on

<!-- GENERÁLT: eszkozok/karoli_strong/elopar.py | scope=f21p, előpárosítás (kísérlet) az arany v3 60 versén (rétegek: f21p/minta.tsv), szótár 140 forrásversből (F3V2 ∩ F3V2B), C-összevetés: F3V2, F3V2B, F3V3 | forras=f21p/szotar_elopar.tsv, f21p/arany_opus_v3.jsonl (sha256 acdeb55f969c96feaa256f5384867c44320c7ad11e1b44b5db529d7543d8d458), f21p/meres_kizaras.tsv, f21p/minta.tsv, f21p/valaszok/F3V2.jsonl, F3V2B.jsonl, F3V3.jsonl, konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, TAGNT_kivonat.tsv | ts=2026-10-01T06:44:44+00:00 | nem minősítés; kézzel szerkeszteni tilos -->

**Ez kísérlet, nem minősítés:** a számok a szkript kimenetei (f21p/elopar_eredmeny.tsv), döntési szabályhoz (küszöbhöz) nem viszonyítanak. Cellaforma: érték% (számláló/nevező) [90%-os Wilson-intervallum, linkszintű, a versen belüli összefüggést nem kezeli, tehát optimista]. Az arany 60 vers (R1 20, R2 10, R3 10, R4 20): a rétegenkénti nevező kicsi, a K8-nál és a K9-linknél nagyon kicsi (n < 30 esetén az intervallum széles; nézd a nevezőt).

## Algoritmus (összefoglalás; a teljes leírás az elopar.py docstringjében)

- **Szótár:** F3V2 ∩ F3V2B egyező linkjei (ugyanaz a (magyar, eredeti) sorszámpár mindkét futásban, ugyanabban a versben), csak a mindkét futásban kapun átment versekből, az arany 60 verse nélkül. Kulcs: a Károli-token kisbetűsítve (ékezettel, egyéb normalizálás nélkül); érték: a TAHOT/TAGNT Strong-mező. Kizárva: a H9xxx / G3588 / G2532 összetevőjű Strong és az a/az/és/s szóalak (K-szabályok hatásköre). Felvétel: db >= 3 és a szóalaknak nincs versengő Strongja.
- **Szótári döntés:** versenként Strongonként csak 1 magyar igénylő : 1 (TR-es) eredeti jelölt esetén; az ismételt szóalak vagy az azonos Strongra mutató két szóalak „modellre vár” (tobb_magyar).
- **K1:** a/az → betoldas, ha a következő szó nem vonatkozó névmás/kötőszó, nem névutó, nem a/az/is, és az alak illik (a + mássalhangzó, az + magánhangzó); H9009/G3588 → forditatlan, ha a tükörfordítás puszta névelő (the, of the, <the>, [is] the ...) és a versben nincs e/ez/ezen/eme/emez/ama (J szabály). Minden más névelő-eset: modellre vár.
- **K8:** H9012, H9013 → forditatlan.
- **K9:** ve- (H9001, H9002) / καί (G2532): ha a magyar versben nincs és/s/pedig/is/de/hogy és nincs mind/se/sem/sőt → forditatlan; ha pontosan egy ve-/καί és pontosan egy kötőszó-szó van, és az az és/s (bővítő szó és τε nélkül) → link; minden más eset modellre vár.
- A [nem TR] eredeti szót egyik szabály sem dönti el. Nem használ KJV-t és modellválaszt.

## Szótár

| mérőszám | érték |
|---|---|
| forrasversek | 140 |
| egyezo_linkek | 2411 |
| kizart_link_strong_miatt | 621 |
| kizart_link_szoalak_miatt | 41 |
| szotarjelolt_parok | 1388 |
| szotarjelolt_szoalakok | 1119 |
| kiesett_versenges | 198 |
| kiesett_versenges_de_volt_3_feletti_par | 35 |
| kiesett_keves | 901 |
| szotar_meret | 20 |
| szotar_lefedett_linkek | 69 |
| szotar_bejegyzes_3_alatti_token_elofordulassal | 0 |

Gépi ellenőrzés: a szótár forrásversei (140) és az arany versei (60) metszete: **0**.

A 15 leggyakoribb szótárbejegyzés: *napon* → H3117 (5), *felől* → H5921 (4), *fiai* → H1121 (4), *köröskörül* → H5439 (4), *legyen* → H1961 (4), *noé* → H5146 (4), *ábrám* → H0087 (4), *áron* → H0175 (4), *alkotott* → H6213 (3), *csinála* → H6213 (3), *istentelen* → H7563 (3), *keletre* → H6924 (3), *mózes* → H4872 (3), *nevét* → H8034 (3), *oltárt* → H4196 (3)

## Lefedettség (az arany egységeiből a szkript által helyesen eldöntött)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| szkript | link_lefedettseg (összes szkript-link ∩ arany / arany link) | 1.3% (4/317) [1–3] | 2.0% (3/152) [1–5] | 1.9% (5/265) [1–4] | 0.0% (0/314) [0–1] | 1.1% (12/1048) [1–2] |
| szkript | link_lefedettseg [szótár] | 0.6% (2/317) [0–2] | 0.7% (1/152) [0–3] | 1.1% (3/265) [0–3] | 0.0% (0/314) [0–1] | 0.6% (6/1048) [0–1] |
| szkript | link_lefedettseg [K9] | 0.6% (2/317) [0–2] | 1.3% (2/152) [0–4] | 0.8% (2/265) [0–2] | 0.0% (0/314) [0–1] | 0.6% (6/1048) [0–1] |
| szkript | betoldas_lefedettseg [K1] | 58.2% (32/55) [47–68] | 56.7% (17/30) [42–70] | 56.8% (25/44) [44–68] | 52.7% (29/55) [42–63] | 56.0% (103/184) [50–62] |
| szkript | forditatlan_lefedettseg [K1+K8+K9] | 30.8% (8/26) [18–47] | 30.0% (3/10) [13–56] | 37.5% (9/24) [23–54] | 72.1% (31/43) [60–82] | 49.5% (51/103) [42–58] |
| szkript | egyseg_lefedettseg (link + betoldas + forditatlan) | 11.1% (44/398) [9–14] | 12.0% (23/192) [9–16] | 11.7% (39/333) [9–15] | 14.6% (60/412) [12–18] | 12.4% (166/1335) [11–14] |
| szkript | egyseg_dontott_arany (szkript-döntés / arany egység) | 11.6% (46/398) | 12.0% (23/192) | 11.7% (39/333) | 15.0% (62/412) | 12.7% (170/1335) |

## Pontosság a szkript saját döntésein

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| szkript | link_pontossag [összes link] | 100.0% (4/4) [60–100] | 100.0% (3/3) [53–100] | 100.0% (5/5) [65–100] | — (0/0) | 100.0% (12/12) [82–100] |
| szkript | link_pontossag [szótár] | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — (0/0) | 100.0% (6/6) [69–100] |
| szkript | link_pontossag [K9] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — (0/0) | 100.0% (6/6) [69–100] |
| szkript | betoldas_pontossag [K1] | 100.0% (32/32) [92–100] | 100.0% (17/17) [86–100] | 100.0% (25/25) [90–100] | 100.0% (29/29) [91–100] | 100.0% (103/103) [97–100] |
| szkript | forditatlan_pontossag [K1] | 100.0% (7/7) [72–100] | — (0/0) | 100.0% (9/9) [77–100] | 93.9% (31/33) [83–98] | 95.9% (47/49) [88–99] |
| szkript | forditatlan_pontossag [K8] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — (0/0) | — (0/0) | 100.0% (4/4) [60–100] |
| szkript | forditatlan_pontossag [K9] | 0.0% (0/2) [0–57] | — (0/0) | — (0/0) | — (0/0) | 0.0% (0/2) [0–57] |
| szkript | egyseg_pontossag [szótár] | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — (0/0) | 100.0% (6/6) [69–100] |
| szkript | egyseg_pontossag [K1] | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 100.0% (34/34) [93–100] | 96.8% (60/62) [91–99] | 98.7% (150/152) [96–100] |
| szkript | egyseg_pontossag [K8] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — (0/0) | — (0/0) | 100.0% (4/4) [60–100] |
| szkript | egyseg_pontossag [K9] | 50.0% (2/4) [18–82] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — (0/0) | 75.0% (6/8) [46–91] |
| szkript | egyseg_pontossag [K1+K8+K9] | 95.5% (42/44) [87–98] | 100.0% (22/22) [89–100] | 100.0% (36/36) [93–100] | 96.8% (60/62) [91–99] | 97.6% (160/164) [95–99] |
| szkript | egyseg_pontossag [összes] | 95.7% (44/46) [88–99] | 100.0% (23/23) [89–100] | 100.0% (39/39) [94–100] | 96.8% (60/62) [91–99] | 97.6% (166/170) [95–99] |

## „Modellre vár” aránya és okai

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| szkript | magyar_token_modellre_var | 88.3% (271/307) | 86.2% (125/145) | 88.7% (236/266) | 91.4% (310/339) | 89.1% (942/1057) |
| szkript | magyar_ok: nincs_szotarban | 80.8% (248/307) | 82.8% (120/145) | 79.7% (212/266) | 83.8% (284/339) | 81.7% (864/1057) |
| szkript | magyar_ok: tobb_magyar | 0.7% (2/307) | 0.0% (0/145) | 0.0% (0/266) | 0.0% (0/339) | 0.2% (2/1057) |
| szkript | magyar_ok: nincs_jelolt | 0.0% (0/307) | 0.0% (0/145) | 0.0% (0/266) | 0.3% (1/339) | 0.1% (1/1057) |
| szkript | magyar_ok: tobb_jelolt | 0.0% (0/307) | 0.0% (0/145) | 0.4% (1/266) | 0.0% (0/339) | 0.1% (1/1057) |
| szkript | magyar_ok: K1_kivetel | 2.6% (8/307) | 1.4% (2/145) | 1.5% (4/266) | 3.8% (13/339) | 2.6% (27/1057) |
| szkript | magyar_ok: K9_nem_gepies | 4.2% (13/307) | 2.1% (3/145) | 7.1% (19/266) | 3.5% (12/339) | 4.4% (47/1057) |
| szkript | magyar_ok: egyeb | 0.0% (0/307) | 0.0% (0/145) | 0.0% (0/266) | 0.0% (0/339) | 0.0% (0/1057) |
| szkript | eredeti_szo_modellre_var | 95.5% (295/309) | 95.9% (141/147) | 94.6% (247/261) | 89.6% (285/318) | 93.5% (968/1035) |
| szkript | eredeti_ok: nincs_szabaly | 85.8% (265/309) | 91.2% (134/147) | 82.8% (216/261) | 81.8% (260/318) | 84.5% (875/1035) |
| szkript | eredeti_ok: K1_kivetel_nevmasi | 0.0% (0/309) | 0.0% (0/147) | 0.8% (2/261) | 1.3% (4/318) | 0.6% (6/1035) |
| szkript | eredeti_ok: K1_kivetel_J | 0.0% (0/309) | 1.4% (2/147) | 1.5% (4/261) | 1.3% (4/318) | 1.0% (10/1035) |
| szkript | eredeti_ok: K9_nem_gepies | 9.7% (30/309) | 3.4% (5/147) | 9.6% (25/261) | 5.0% (16/318) | 7.3% (76/1035) |
| szkript | eredeti_ok: nem_tr | 0.0% (0/309) | 0.0% (0/147) | 0.0% (0/261) | 0.3% (1/318) | 0.1% (1/1035) |

## Alapadat

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| szkript | arany_versek | 20 | 10 | 10 | 20 | 60 |

## C-összevetés ugyanazokon az egységeken (tájékoztató)

Egységenkénti igen/nem kérdés: a szkript minden döntése „igen” az adott egységre (link, betoldas, forditatlan). A C ugyanerre igent mond, ha az egység benne van a C kimenetében. A C-pontosság: a C igen/nem válasza egyezik az arannyal. Eltérésnél pontosan az egyik egyezik. Csak a C-ben kapun átment aranyversek.

### F3V2

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V2 [szótár] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V2 [szótár] | szkript_pontossag (ugyanezeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2 [szótár] | C_pontossag (ugyanazokon az egységeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2 [szótár] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2 [szótár] | elteres (C nem mondja ugyanezt) | 0.0% (0/2) | 0.0% (0/1) | 0.0% (0/3) | — | 0.0% (0/6) |
| F3V2 [szótár] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V2 [szótár] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V2 [K1] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2 [K1] | szkript_pontossag (ugyanezeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 100.0% (34/34) [93–100] | 96.8% (60/62) [91–99] | 98.7% (150/152) [96–100] |
| F3V2 [K1] | C_pontossag (ugyanazokon az egységeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 93.5% (58/62) [86–97] | 96.7% (147/152) [93–98] |
| F3V2 [K1] | C_fedi_a_helyes_szkript_dontest | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 93.3% (56/60) [86–97] | 96.7% (145/150) [93–98] |
| F3V2 [K1] | elteres (C nem mondja ugyanezt) | 0.0% (0/39) | 0.0% (0/17) | 2.9% (1/34) | 9.7% (6/62) | 4.6% (7/152) |
| F3V2 [K1] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | 100.0% (1/1) | 66.7% (4/6) | 71.4% (5/7) |
| F3V2 [K1] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | 0.0% (0/1) | 33.3% (2/6) | 28.6% (2/7) |
| F3V2 [K8] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | — | — | 100.0% (60/60) |
| F3V2 [K8] | szkript_pontossag (ugyanezeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2 [K8] | C_pontossag (ugyanazokon az egységeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2 [K8] | C_fedi_a_helyes_szkript_dontest | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2 [K8] | elteres (C nem mondja ugyanezt) | 0.0% (0/1) | 0.0% (0/3) | — | — | 0.0% (0/4) |
| F3V2 [K8] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V2 [K8] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V2 [K9] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V2 [K9] | szkript_pontossag (ugyanezeken) | 50.0% (2/4) [18–82] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 75.0% (6/8) [46–91] |
| F3V2 [K9] | C_pontossag (ugyanazokon az egységeken) | 100.0% (4/4) [60–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (8/8) [75–100] |
| F3V2 [K9] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (6/6) [69–100] |
| F3V2 [K9] | elteres (C nem mondja ugyanezt) | 50.0% (2/4) | 0.0% (0/2) | 0.0% (0/2) | — | 25.0% (2/8) |
| F3V2 [K9] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | — (0/0) | — | 0.0% (0/2) |
| F3V2 [K9] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | — (0/0) | — | 100.0% (2/2) |
| F3V2 [összes] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2 [összes] | szkript_pontossag (ugyanezeken) | 95.7% (44/46) [88–99] | 100.0% (23/23) [89–100] | 100.0% (39/39) [94–100] | 96.8% (60/62) [91–99] | 97.6% (166/170) [95–99] |
| F3V2 [összes] | C_pontossag (ugyanazokon az egységeken) | 100.0% (46/46) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 93.5% (58/62) [86–97] | 97.1% (165/170) [94–99] |
| F3V2 [összes] | C_fedi_a_helyes_szkript_dontest | 100.0% (44/44) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 93.3% (56/60) [86–97] | 97.0% (161/166) [94–99] |
| F3V2 [összes] | elteres (C nem mondja ugyanezt) | 4.3% (2/46) | 0.0% (0/23) | 2.6% (1/39) | 9.7% (6/62) | 5.3% (9/170) |
| F3V2 [összes] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | 100.0% (1/1) | 66.7% (4/6) | 55.6% (5/9) |
| F3V2 [összes] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | 0.0% (0/1) | 33.3% (2/6) | 44.4% (4/9) |

### F3V2B

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V2B [szótár] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V2B [szótár] | szkript_pontossag (ugyanezeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2B [szótár] | C_pontossag (ugyanazokon az egységeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2B [szótár] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V2B [szótár] | elteres (C nem mondja ugyanezt) | 0.0% (0/2) | 0.0% (0/1) | 0.0% (0/3) | — | 0.0% (0/6) |
| F3V2B [szótár] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V2B [szótár] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V2B [K1] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2B [K1] | szkript_pontossag (ugyanezeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 100.0% (34/34) [93–100] | 96.8% (60/62) [91–99] | 98.7% (150/152) [96–100] |
| F3V2B [K1] | C_pontossag (ugyanazokon az egységeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 93.5% (58/62) [86–97] | 96.7% (147/152) [93–98] |
| F3V2B [K1] | C_fedi_a_helyes_szkript_dontest | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 93.3% (56/60) [86–97] | 96.7% (145/150) [93–98] |
| F3V2B [K1] | elteres (C nem mondja ugyanezt) | 0.0% (0/39) | 0.0% (0/17) | 2.9% (1/34) | 9.7% (6/62) | 4.6% (7/152) |
| F3V2B [K1] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | 100.0% (1/1) | 66.7% (4/6) | 71.4% (5/7) |
| F3V2B [K1] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | 0.0% (0/1) | 33.3% (2/6) | 28.6% (2/7) |
| F3V2B [K8] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | — | — | 100.0% (60/60) |
| F3V2B [K8] | szkript_pontossag (ugyanezeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2B [K8] | C_pontossag (ugyanazokon az egységeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2B [K8] | C_fedi_a_helyes_szkript_dontest | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V2B [K8] | elteres (C nem mondja ugyanezt) | 0.0% (0/1) | 0.0% (0/3) | — | — | 0.0% (0/4) |
| F3V2B [K8] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V2B [K8] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V2B [K9] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V2B [K9] | szkript_pontossag (ugyanezeken) | 50.0% (2/4) [18–82] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 75.0% (6/8) [46–91] |
| F3V2B [K9] | C_pontossag (ugyanazokon az egységeken) | 100.0% (4/4) [60–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (8/8) [75–100] |
| F3V2B [K9] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (6/6) [69–100] |
| F3V2B [K9] | elteres (C nem mondja ugyanezt) | 50.0% (2/4) | 0.0% (0/2) | 0.0% (0/2) | — | 25.0% (2/8) |
| F3V2B [K9] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | — (0/0) | — | 0.0% (0/2) |
| F3V2B [K9] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | — (0/0) | — | 100.0% (2/2) |
| F3V2B [összes] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2B [összes] | szkript_pontossag (ugyanezeken) | 95.7% (44/46) [88–99] | 100.0% (23/23) [89–100] | 100.0% (39/39) [94–100] | 96.8% (60/62) [91–99] | 97.6% (166/170) [95–99] |
| F3V2B [összes] | C_pontossag (ugyanazokon az egységeken) | 100.0% (46/46) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 93.5% (58/62) [86–97] | 97.1% (165/170) [94–99] |
| F3V2B [összes] | C_fedi_a_helyes_szkript_dontest | 100.0% (44/44) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 93.3% (56/60) [86–97] | 97.0% (161/166) [94–99] |
| F3V2B [összes] | elteres (C nem mondja ugyanezt) | 4.3% (2/46) | 0.0% (0/23) | 2.6% (1/39) | 9.7% (6/62) | 5.3% (9/170) |
| F3V2B [összes] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | 100.0% (1/1) | 66.7% (4/6) | 55.6% (5/9) |
| F3V2B [összes] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | 0.0% (0/1) | 33.3% (2/6) | 44.4% (4/9) |

### F3V3

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V3 [szótár] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V3 [szótár] | szkript_pontossag (ugyanezeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V3 [szótár] | C_pontossag (ugyanazokon az egységeken) | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V3 [szótár] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | 100.0% (6/6) [69–100] |
| F3V3 [szótár] | elteres (C nem mondja ugyanezt) | 0.0% (0/2) | 0.0% (0/1) | 0.0% (0/3) | — | 0.0% (0/6) |
| F3V3 [szótár] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V3 [szótár] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — (0/0) | — | — (0/0) |
| F3V3 [K1] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V3 [K1] | szkript_pontossag (ugyanezeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 100.0% (34/34) [93–100] | 96.8% (60/62) [91–99] | 98.7% (150/152) [96–100] |
| F3V3 [K1] | C_pontossag (ugyanazokon az egységeken) | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 96.8% (60/62) [91–99] | 98.0% (149/152) [95–99] |
| F3V3 [K1] | C_fedi_a_helyes_szkript_dontest | 100.0% (39/39) [94–100] | 100.0% (17/17) [86–100] | 97.1% (33/34) [88–99] | 96.7% (58/60) [90–99] | 98.0% (147/150) [95–99] |
| F3V3 [K1] | elteres (C nem mondja ugyanezt) | 0.0% (0/39) | 0.0% (0/17) | 2.9% (1/34) | 6.5% (4/62) | 3.3% (5/152) |
| F3V3 [K1] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | 100.0% (1/1) | 50.0% (2/4) | 60.0% (3/5) |
| F3V3 [K1] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | 0.0% (0/1) | 50.0% (2/4) | 40.0% (2/5) |
| F3V3 [K8] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | — | — | 100.0% (60/60) |
| F3V3 [K8] | szkript_pontossag (ugyanezeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V3 [K8] | C_pontossag (ugyanazokon az egységeken) | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V3 [K8] | C_fedi_a_helyes_szkript_dontest | 100.0% (1/1) [27–100] | 100.0% (3/3) [53–100] | — | — | 100.0% (4/4) [60–100] |
| F3V3 [K8] | elteres (C nem mondja ugyanezt) | 0.0% (0/1) | 0.0% (0/3) | — | — | 0.0% (0/4) |
| F3V3 [K8] | elteresbol_szkript_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V3 [K8] | elteresbol_C_egyezik_arannyal | — (0/0) | — (0/0) | — | — | — (0/0) |
| F3V3 [K9] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | — | 100.0% (60/60) |
| F3V3 [K9] | szkript_pontossag (ugyanezeken) | 50.0% (2/4) [18–82] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 75.0% (6/8) [46–91] |
| F3V3 [K9] | C_pontossag (ugyanazokon az egységeken) | 100.0% (4/4) [60–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (8/8) [75–100] |
| F3V3 [K9] | C_fedi_a_helyes_szkript_dontest | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | 100.0% (2/2) [42–100] | — | 100.0% (6/6) [69–100] |
| F3V3 [K9] | elteres (C nem mondja ugyanezt) | 50.0% (2/4) | 0.0% (0/2) | 0.0% (0/2) | — | 25.0% (2/8) |
| F3V3 [K9] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | — (0/0) | — | 0.0% (0/2) |
| F3V3 [K9] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | — (0/0) | — | 100.0% (2/2) |
| F3V3 [összes] | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V3 [összes] | szkript_pontossag (ugyanezeken) | 95.7% (44/46) [88–99] | 100.0% (23/23) [89–100] | 100.0% (39/39) [94–100] | 96.8% (60/62) [91–99] | 97.6% (166/170) [95–99] |
| F3V3 [összes] | C_pontossag (ugyanazokon az egységeken) | 100.0% (46/46) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 96.8% (60/62) [91–99] | 98.2% (167/170) [96–99] |
| F3V3 [összes] | C_fedi_a_helyes_szkript_dontest | 100.0% (44/44) [94–100] | 100.0% (23/23) [89–100] | 97.4% (38/39) [89–99] | 96.7% (58/60) [90–99] | 98.2% (163/166) [96–99] |
| F3V3 [összes] | elteres (C nem mondja ugyanezt) | 4.3% (2/46) | 0.0% (0/23) | 2.6% (1/39) | 6.5% (4/62) | 4.1% (7/170) |
| F3V3 [összes] | elteresbol_szkript_egyezik_arannyal | 0.0% (0/2) | — (0/0) | 100.0% (1/1) | 50.0% (2/4) | 42.9% (3/7) |
| F3V3 [összes] | elteresbol_C_egyezik_arannyal | 100.0% (2/2) | — (0/0) | 0.0% (0/1) | 50.0% (2/4) | 57.1% (4/7) |

## Hibás szkript-döntések

Összesen 4 hibás szkript-egység (a kizárások után): K1: 2, K9: 2.

| csoport | hibatípus (az arany szerint) | db |
|---|---|---|
| K1 | az eredeti szó az aranyban párosítva | 2 |
| K9 | az eredeti szó az aranyban párosítva | 2 |

### Hibás szótári döntések szótárbejegyzésenként

| szóalak | Strong | db (szótár) | vers_db | hibás döntés | helyes döntés |
|---|---|---|---|---|---|
| (nincs hibás szótári döntés) | | | | 0 | 6 |

A helyes szótári döntések bejegyzésenként: *fiai* (1), *napon* (3), *oltárt* (1), *tiszta* (1).

### Példák (az első 15 hibás döntés versrendben; legfeljebb 10 szótári, a többi K-szabály)

| vers | csoport | magyar szó | szkript-döntés | az arany szerint | típus |
|---|---|---|---|---|---|
| Péld 30:17 | K9 | — | forditatlan: #14 וְֽ H9002 [and] | 17 vagy | az eredeti szó az aranyban párosítva |
| Péld 30:17 | K9 | — | forditatlan: #5 וְ H9002 [so] | 6 vagy | az eredeti szó az aranyban párosítva |
| Mt 4:4 | K1 | — | forditatlan: #1 Ὁ G3588 [<the>] | 1 Ő | az eredeti szó az aranyban párosítva |
| 1Pét 5:12 | K1 | — | forditatlan: #4 τοῦ G3588 [the] | 3 a, 4 ki | az eredeti szó az aranyban párosítva |

## Nyitott kérdések (a kísérlet korlátai, nem döntés)

- A szótár szóalak-szintű és nyers (csak kisbetű): a toldalékos alakok külön kulcsok, ezért a lefedettség a gyakori, kötött alakokra korlátozódik; tövesítés nem készült.
- A szótár forrása két modellfutás egyezése, nem arany: a C következetes tévedései bekerülhetnek.
- A K1 névelő-vizsgálata (a/az + következő szó) és a tükörfordítás-alapú névmási szűrés gépies közelítés; a K9 csak az „egy ve-/καί : egy és/s” és a „nincs kötőszó” esetet dönti el.
- A mérés 60 versen fut; a C-összevetés csak a szkript által eldöntött egységeken értelmezett, nem a C teljes pontossága.
- A szótár `db` mezője link-szintű (egy magyar token több azonos Strongú eredetihez kötve többször számít); a `szotar_bejegyzes_3_alatti_token_elofordulassal` sor mutatja, hány bejegyzés esne ki, ha a feltétel token-előfordulásra szólna.
- A fenti hibapéldák a szabályok lehetséges finomítására utalnak (pl. a K9 kötőszó-listája, a névelő + δέ, a magyar „a ki” és a görög névelő összekapcsolása). Ezek az arany ismeretében fogalmazódnának meg, tehát az ugyanezen a 60 versen mért javulás nem volna független mérés; a szkript ezért nem tartalmazza őket.

