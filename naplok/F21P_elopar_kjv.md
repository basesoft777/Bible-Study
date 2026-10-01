# F21P_elopar_kjv.md — a KJV-szabály mérése a szkriptes előpárosításban (kísérlet)

<!-- GENERÁLT: eszkozok/karoli_strong/elopar_kjv.py | scope=f21p, a KJV-szabály ("nincs KJV-tag → forditatlan-jelölt") mérése (kísérlet) az arany v3 60 versén, rétegenként (f21p/minta.tsv); A) önállóan, B) az előpárosítással együtt; R1-kontroll a régi táblával; C-összevetés: F3V2, F3V2B, F3V3 | forras=konkordancia/KJV_Strongs_teljes.tsv (sha256 5a7891145401aa62dd8aac31d0192eecb112daf780461279a84912fe40826a2e), konkordancia/KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, f21p/arany_opus_v3.jsonl (sha256 acdeb55f969c96feaa256f5384867c44320c7ad11e1b44b5db529d7543d8d458; csak mérce), f21p/meres_kizaras.tsv, f21p/minta.tsv, f21p/szotar_elopar.tsv (csak B), f21p/valaszok/F3V2.jsonl, F3V2B.jsonl, F3V3.jsonl (csak C-összevetés), konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, TAGNT_kivonat.tsv | ts=2026-10-01T07:21:27+00:00 | kísérlet, nem minősítés a döntési szabály szerint; kézzel szerkeszteni tilos -->

**Kísérlet, nem minősítés a döntési szabály szerint.** A számok a szkript kimenetei (f21p/elopar_kjv_eredmeny.tsv); küszöbhöz nem viszonyítanak, ajánlást nem tartalmaznak. Cellaforma: érték% (számláló/nevező) [90%-os Wilson-intervallum, szószintű, a versen belüli összefüggést nem kezeli, tehát optimista]. A 60 vers rétegenként kicsi (R1 20, R2 10, R3 10, R4 20): nézd a nevezőt.

## A KJV-szabály algoritmusa

1. **KJV-sor:** `tokenek.kjv_tamapont_forras(igehely, "teljes")` — a `konkordancia/KJV_Strongs_teljes.tsv` (F19) sora a `Karoli_versmegfeleltetes.tsv` KJV-oszlopa szerinti versre. A vers KJV-Strong-halmaza a sor összes `{...}` címkéje. Ha nincs KJV-sor, a vers minden szava **„nincs KJV-sor”** (nem „nincs KJV-tag”): a szabály ott nem alkalmazható.
2. **Normalizálás:** minden Strong `^([HG])0*(\d+)[a-zA-Z]?$` → betű + négyjegyű szám (H430 = H0430 = H0430a).
3. **Összetett Strong:** a `+` mentén összetevőkre bontva; a **lexikális összetevők** = az összetevők a kizárási lista nélkül (pl. G2532+G1473 κἀγώ → G1473).
4. **Kizárási lista** (a K1/K8/K9 hatásköre; a KJV-ben eleve nincs rájuk Strong): **minden H9xxx** (STEPBible héber elő-/utórag: H9001/H9002 ve-, H9003–H9008 elöljárók, H9009 névelő, H9010–H9013), **G3588** (görög névelő), **G2532** (καί). Lexikális összetevő nélküli szó: „kizárt (nyelvtani)”, a szabály nem dönt. Más funkciószó (H0853, H0834, G1161 …) nincs kizárva: a lista a K-szabályok duplázását zárja ki, nem a KJV-címkézés hiányait — ezek hatását a hibaok-elemzés méri.
5. **[nem TR]** eredeti szó: nem dönt (mint az elopar.py).
6. Különben **„van KJV-tag”**, ha legalább egy lexikális összetevő a KJV-halmazban van; **„nincs KJV-tag”** (forditatlan-jelölt), ha egyik sincs.

**Döntés.** *A) önállóan:* minden „nincs KJV-tag” szó → `forditatlan`. *B) az előpárosítással együtt:* csak ha az `elopar.parosit()` arra a szóra nem döntött (sem K1/K8/K9-forditatlan, sem szótári / K9-link). A K-szabályok csak kizárási listás Strongokra döntenek, ezért a B) az A)-tól csak a szótári/K9-linkkel ütköző szavakban tér el. A KJV-szabály szótárt, modellválaszt és aranyat nem használ; az arany csak a mérce.

## Alapadat és a szavak állapota

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-szabály | arany_versek | 20 | 10 | 10 | 20 | 60 |
| KJV-szabály | versek_kjv_sorral (teljes tábla) | 100.0% (20/20) | 90.0% (9/10) | 100.0% (10/10) | 0.0% (0/20) | 65.0% (39/60) |
| KJV-szabály | versek_nincs_kjv_sor | 0.0% (0/20) | 10.0% (1/10) | 0.0% (0/10) | 100.0% (20/20) | 35.0% (21/60) |
| KJV-szabály | eredeti_szo (kizárások nélkül) | 309 | 147 | 261 | 318 | 1035 |
| KJV-szabály | eredeti_szo a KJV-soros versekben | 100.0% (309/309) | 93.2% (137/147) | 100.0% (261/261) | 0.0% (0/318) | 68.3% (707/1035) |

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-szabály | állapot: nincs_kjv_sor | 0.0% (0/309) | 6.8% (10/147) | 0.0% (0/261) | 100.0% (318/318) | 31.7% (328/1035) |
| KJV-szabály | állapot: nem_tr | 0.0% (0/309) | 0.0% (0/147) | 0.0% (0/261) | 0.0% (0/318) | 0.0% (0/1035) |
| KJV-szabály | állapot: kizart_nyelvtani | 35.9% (111/309) | 32.7% (48/147) | 36.4% (95/261) | 0.0% (0/318) | 24.5% (254/1035) |
| KJV-szabály | állapot: van_kjv_tag | 48.5% (150/309) | 18.4% (27/147) | 48.7% (127/261) | 0.0% (0/318) | 29.4% (304/1035) |
| KJV-szabály | állapot: nincs_kjv_tag | 15.5% (48/309) | 42.2% (62/147) | 14.9% (39/261) | 0.0% (0/318) | 14.4% (149/1035) |
| KJV-szabály | jelolt_arany_szerint_forditatlan | 22.9% (11/48) [15–34] | 4.8% (3/62) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.8% (22/149) [11–20] |

### A KJV-sor nélküli aranyversek

| vers | réteg | ok |
|---|---|---|
| Zsolt 22:32 | R2 | nincs KJV-megfeleltetés (versszámozás) |
| Mt 4:4 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 5:34 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 6:31 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 11:18 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 21:4 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 23:31 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mt 27:18 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mk 2:10 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mk 2:23 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Mk 3:18 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Jak 1:15 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Jak 1:18 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Jak 3:1 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Jak 3:4 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| Jak 3:8 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| 1Pét 4:2 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| 1Pét 4:11 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| 1Pét 5:12 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| 2Pét 1:7 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |
| 1Ján 1:10 | R4 | ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi) |

A F19 KJV-oldali adathiány-versei (Mk 9:43, Lk 6:41, Lk 17:36) közül az aranyban: egy sincs.

### Versszámozás-gyanús versek (KJV-sor van, de valószínűleg nem a megfelelő vers)

Arany nélküli vizsgálat: a vers *jól címkézett* Strongjai (a korpuszban a KJV legalább 50%-ban címkézi, n >= 5) közül kevesebb mint fele van a megfeleltetett KJV-vers címkéi között. Az oszlopok a megfeleltetett KJV-vers (0) és a fejezeten belüli szomszédai (-1, +1) illeszkedését mutatják (talált/összes jól címkézett Strong). A KJV-szám a `Karoli_versmegfeleltetes.tsv` igehely_kjv oszlopa.

| vers | réteg | megfeleltetett KJV-vers | -1 | 0 | +1 | „nincs KJV-tag” jelölt |
|---|---|---|---|---|---|---|
| Zsolt 6:5 | R2 | 6:5 | 6:4: 6/6 | 6:5: 0/6 | 6:6: 0/6 | 7 |
| Zsolt 13:2 | R2 | 13:2 | 13:1: 5/5 | 13:2: 0/5 | 13:3: 1/5 | 11 |
| Zsolt 18:1 | R2 | 18:1 | 18:0: 12/12 | 18:1: 1/12 | 18:2: 1/12 | 17 |
| Zsolt 18:3 | R2 | 18:3 | 18:2: 11/11 | 18:3: 1/11 | 18:4: 0/11 | 10 |
| Zsolt 59:8 | R2 | 59:8 | 59:7: 5/5 | 59:8: 0/5 | 59:9: 0/5 | 8 |

Ugyanez a vizsgálat a teljes ÓSZ-en (tájékoztató, arany nélkül): 22730 KJV-soros ÓSZ-versből 1162 versszámozás-gyanús; ebből 1039-nál egy fejezeten belüli szomszédos KJV-vers (-1/+1) illeszkedik (>= 50%). Könyvenként: Zsolt 915, Ézs 42, Préd 24, 1Sám 20, Hós 13, Jón 9, 4Móz 8, 1Kir 6, Dán 2. A megfeleltetési tábla osztálya (osztaly) ezeknél: MT 984, KJV 29, KEZI 26.

## Döntések, pontosság, fedés (A és B)

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-szabály A) önállóan | forditatlan_dontes | 48 | 62 | 39 | 0 | 149 |
| KJV-szabály A) önállóan | pontossag (döntés ∩ arany forditatlan / döntés) | 22.9% (11/48) [15–34] | 4.8% (3/62) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.8% (22/149) [11–20] |
| KJV-szabály A) önállóan | hibás döntés, az aranyban kötött (link) | 100.0% (37/37) | 100.0% (59/59) | 100.0% (31/31) | — (0/0) | 100.0% (127/127) |
| KJV-szabály A) önállóan | fedes (az arany összes forditatlan-szavából) | 42.3% (11/26) [28–58] | 30.0% (3/10) [13–56] | 33.3% (8/24) [20–50] | 0.0% (0/43) [0–6] | 21.4% (22/103) [15–29] |
| KJV-szabály A) önállóan | fedes a KJV-soros versekben | 42.3% (11/26) [28–58] | 30.0% (3/10) [13–56] | 33.3% (8/24) [20–50] | — (0/0) | 36.7% (22/60) [27–47] |
| KJV-szabály A) önállóan | fedes a KJV-soros versek lexikális szavain | 100.0% (11/11) [80–100] | 100.0% (3/3) [53–100] | 100.0% (8/8) [75–100] | — (0/0) | 100.0% (22/22) [89–100] |
| KJV-szabály B) az előpárosítással együtt | forditatlan_dontes | 48 | 61 | 39 | 0 | 148 |
| KJV-szabály B) az előpárosítással együtt | pontossag (döntés ∩ arany forditatlan / döntés) | 22.9% (11/48) [15–34] | 4.9% (3/61) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.9% (22/148) [11–20] |
| KJV-szabály B) az előpárosítással együtt | hibás döntés, az aranyban kötött (link) | 100.0% (37/37) | 100.0% (58/58) | 100.0% (31/31) | — (0/0) | 100.0% (126/126) |
| KJV-szabály B) az előpárosítással együtt | fedes (az arany összes forditatlan-szavából) | 42.3% (11/26) [28–58] | 30.0% (3/10) [13–56] | 33.3% (8/24) [20–50] | 0.0% (0/43) [0–6] | 21.4% (22/103) [15–29] |
| KJV-szabály B) az előpárosítással együtt | fedes a KJV-soros versekben | 42.3% (11/26) [28–58] | 30.0% (3/10) [13–56] | 33.3% (8/24) [20–50] | — (0/0) | 36.7% (22/60) [27–47] |
| KJV-szabály B) az előpárosítással együtt | fedes a KJV-soros versek lexikális szavain | 100.0% (11/11) [80–100] | 100.0% (3/3) [53–100] | 100.0% (8/8) [75–100] | — (0/0) | 100.0% (22/22) [89–100] |
| érzékenység: A) a versszámozás-gyanús versek nélkül | versek_kjv_sorral_gyanu_nelkul | 100.0% (20/20) | 44.4% (4/9) | 100.0% (10/10) | — (0/0) | 87.2% (34/39) |
| érzékenység: A) a versszámozás-gyanús versek nélkül | forditatlan_dontes | 48 | 9 | 39 | 0 | 96 |
| érzékenység: A) a versszámozás-gyanús versek nélkül | pontossag (döntés ∩ arany forditatlan / döntés) | 22.9% (11/48) [15–34] | 0.0% (0/9) [0–23] | 20.5% (8/39) [12–33] | — (0/0) | 19.8% (19/96) [14–27] |
| érzékenység: A) a versszámozás-gyanús versek nélkül | fedes (az arany összes forditatlan-szavából) | 42.3% (11/26) [28–58] | 0.0% (0/10) [0–21] | 33.3% (8/24) [20–50] | 0.0% (0/43) [0–6] | 18.4% (19/103) [13–26] |
| érzékenység: A) a versszámozás-gyanús versek nélkül | fedes a nem gyanús KJV-soros versekben | 42.3% (11/26) [28–58] | — (0/0) | 33.3% (8/24) [20–50] | — (0/0) | 38.0% (19/50) [28–50] |

## Ütközés az előpárosítással

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| KJV-szabály | A-döntés, amelyet az előpárosítás linkként döntött el | 0.0% (0/48) | 1.6% (1/62) | 0.0% (0/39) | — (0/0) | 0.7% (1/149) |
| KJV-szabály | ebből a link az aranyban | — (0/0) | 100.0% (1/1) | — (0/0) | — (0/0) | 100.0% (1/1) |
| KJV-szabály | ebből forditatlan az aranyban | — (0/0) | 0.0% (0/1) | — (0/0) | — (0/0) | 0.0% (0/1) |
| KJV-szabály | A-döntés, amelyet a K1/K8/K9 forditatlannak döntött | 0.0% (0/48) | 0.0% (0/62) | 0.0% (0/39) | — (0/0) | 0.0% (0/149) |

## Kombinált előpárosítás (az F21.60 előpárosítás + a B) döntései)

Az előpárosítás sorai az F21P_elopar.md számait ismétlik (166/1335 egység; 1,1% link-fedés); a KJV-szabály csak forditatlan-döntést ad, a link-fedést nem változtatja.

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| előpárosítás (F21.60) | egyseg_lefedettseg | 11.1% (44/398) [9–14] | 12.0% (23/192) [9–16] | 11.7% (39/333) [9–15] | 14.6% (60/412) [12–18] | 12.4% (166/1335) [11–14] |
| előpárosítás (F21.60) | egyseg_pontossag | 95.7% (44/46) [88–99] | 100.0% (23/23) [89–100] | 100.0% (39/39) [94–100] | 96.8% (60/62) [91–99] | 97.6% (166/170) [95–99] |
| előpárosítás (F21.60) | forditatlan_lefedettseg | 30.8% (8/26) [18–47] | 30.0% (3/10) [13–56] | 37.5% (9/24) [23–54] | 72.1% (31/43) [60–82] | 49.5% (51/103) [42–58] |
| előpárosítás (F21.60) | forditatlan_pontossag | 80.0% (8/10) [54–93] | 100.0% (3/3) [53–100] | 100.0% (9/9) [77–100] | 93.9% (31/33) [83–98] | 92.7% (51/55) [85–97] |
| előpárosítás + KJV-szabály B) | egyseg_lefedettseg | 13.8% (55/398) [11–17] | 13.5% (26/192) [10–18] | 14.1% (47/333) [11–18] | 14.6% (60/412) [12–18] | 14.1% (188/1335) [13–16] |
| előpárosítás + KJV-szabály B) | egyseg_pontossag | 58.5% (55/94) [50–67] | 31.0% (26/84) [23–40] | 60.3% (47/78) [51–69] | 96.8% (60/62) [91–99] | 59.1% (188/318) [55–64] |
| előpárosítás + KJV-szabály B) | egyseg_dontott_arany | 23.6% (94/398) | 43.8% (84/192) | 23.4% (78/333) | 15.0% (62/412) | 23.8% (318/1335) |
| előpárosítás + KJV-szabály B) | forditatlan_lefedettseg | 73.1% (19/26) [57–85] | 60.0% (6/10) [35–81] | 70.8% (17/24) [54–83] | 72.1% (31/43) [60–82] | 70.9% (73/103) [63–78] |
| előpárosítás + KJV-szabály B) | forditatlan_pontossag | 32.8% (19/58) [24–43] | 9.4% (6/64) [5–17] | 35.4% (17/48) [25–47] | 93.9% (31/33) [83–98] | 36.0% (73/203) [31–42] |

## R1-kontroll: régi (Genesis/Exodus/Proverbs) és teljes tábla

A régi tábla frázisokat és üres szavú {H0853}-elemeket is tartalmaz, a teljes (eBible) szó-szintű és a H0853-at szinte sosem címkézi; a két forrás „nincs KJV-tag” jelöltjeinek különbsége a forma hatása.

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| R1-kontroll: régi tábla (Gen/Exo/Pro) | "nincs KJV-tag" jelölt (A-döntés) | 47 | — | — | — | 47 |
| R1-kontroll: régi tábla (Gen/Exo/Pro) | pontossag | 23.4% (11/47) [15–35] | — | — | — | 23.4% (11/47) [15–35] |
| R1-kontroll: régi tábla (Gen/Exo/Pro) | fedes | 42.3% (11/26) [28–58] | — | — | — | 42.3% (11/26) [28–58] |
| R1-kontroll: teljes tábla (F19) | "nincs KJV-tag" jelölt (A-döntés) | 48 | — | — | — | 48 |
| R1-kontroll: teljes tábla (F19) | pontossag | 22.9% (11/48) [15–34] | — | — | — | 22.9% (11/48) [15–34] |
| R1-kontroll: teljes tábla (F19) | fedes | 42.3% (11/26) [28–58] | — | — | — | 42.3% (11/26) [28–58] |
| R1-kontroll: mindkét tábla szerint jelölt | "nincs KJV-tag" jelölt (A-döntés) | 47 | — | — | — | 47 |
| R1-kontroll: mindkét tábla szerint jelölt | pontossag | 23.4% (11/47) [15–35] | — | — | — | 23.4% (11/47) [15–35] |
| R1-kontroll: mindkét tábla szerint jelölt | fedes | 42.3% (11/26) [28–58] | — | — | — | 42.3% (11/26) [28–58] |
| R1-kontroll: csak a régi szerint | "nincs KJV-tag" jelölt (A-döntés) | 0 | — | — | — | 0 |
| R1-kontroll: csak a régi szerint | pontossag | — (0/0) | — | — | — | — (0/0) |
| R1-kontroll: csak a régi szerint | fedes | 0.0% (0/26) [0–9] | — | — | — | 0.0% (0/26) [0–9] |
| R1-kontroll: csak a teljes szerint | "nincs KJV-tag" jelölt (A-döntés) | 1 | — | — | — | 1 |
| R1-kontroll: csak a teljes szerint | pontossag | 0.0% (0/1) [0–73] | — | — | — | 0.0% (0/1) [0–73] |
| R1-kontroll: csak a teljes szerint | fedes | 0.0% (0/26) [0–9] | — | — | — | 0.0% (0/26) [0–9] |

A különbség Strongonként: csak a régi szerint jelölt: —; csak a teljes szerint jelölt: H6040 (1).

## C-összevetés ugyanezeken a döntéseken (tájékoztató)

Az A) döntéseken: a C igent mond, ha a szó a C `forditatlan`-listájában van (csak a C-ben kapun átment aranyversek). A C pontossága: a C igen/nem válasza egyezik az arannyal.

| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |
|---|---|---|---|---|---|---|
| F3V2 (az A-döntéseken) | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2 (az A-döntéseken) | KJV-szabály pontossága (ugyanezeken) | 22.9% (11/48) [15–34] | 4.8% (3/62) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.8% (22/149) [11–20] |
| F3V2 (az A-döntéseken) | C pontossága (igen/nem egyezik az arannyal) | 100.0% (48/48) [95–100] | 100.0% (62/62) [96–100] | 94.9% (37/39) [86–98] | — (0/0) | 98.7% (147/149) [96–100] |
| F3V2 (az A-döntéseken) | C forditatlan-igen pontossága | 100.0% (11/11) [80–100] | 100.0% (3/3) [53–100] | 87.5% (7/8) [59–97] | — (0/0) | 95.5% (21/22) [82–99] |
| F3V2B (az A-döntéseken) | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V2B (az A-döntéseken) | KJV-szabály pontossága (ugyanezeken) | 22.9% (11/48) [15–34] | 4.8% (3/62) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.8% (22/149) [11–20] |
| F3V2B (az A-döntéseken) | C pontossága (igen/nem egyezik az arannyal) | 100.0% (48/48) [95–100] | 96.8% (60/62) [91–99] | 97.4% (38/39) [89–99] | — (0/0) | 98.0% (146/149) [95–99] |
| F3V2B (az A-döntéseken) | C forditatlan-igen pontossága | 100.0% (11/11) [80–100] | 100.0% (1/1) [27–100] | 88.9% (8/9) [62–97] | — (0/0) | 95.2% (20/21) [81–99] |
| F3V3 (az A-döntéseken) | versek_C_ok | 100.0% (20/20) | 100.0% (10/10) | 100.0% (10/10) | 100.0% (20/20) | 100.0% (60/60) |
| F3V3 (az A-döntéseken) | KJV-szabály pontossága (ugyanezeken) | 22.9% (11/48) [15–34] | 4.8% (3/62) [2–12] | 20.5% (8/39) [12–33] | — (0/0) | 14.8% (22/149) [11–20] |
| F3V3 (az A-döntéseken) | C pontossága (igen/nem egyezik az arannyal) | 100.0% (48/48) [95–100] | 100.0% (62/62) [96–100] | 94.9% (37/39) [86–98] | — (0/0) | 98.7% (147/149) [96–100] |
| F3V3 (az A-döntéseken) | C forditatlan-igen pontossága | 100.0% (11/11) [80–100] | 100.0% (3/3) [53–100] | 80.0% (8/10) [54–93] | — (0/0) | 91.7% (22/24) [78–97] |

## Hibás KJV-döntések (A, összes réteg): forditatlan a szabály szerint, de az aranyban nem

Összesen 127. Gépi okbesorolás (első illő; a definíció a szkript docstringjében):

| ok | R1 | R2 | R3 | R4 | összes |
|---|---|---|---|---|---|
| ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) | 35 | 9 | 30 | 0 | 74 |
| versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) | 0 | 50 | 0 | 0 | 50 |
| más Strong a KJV-sorban (a vers eredetijében nem szereplő KJV-címke) | 1 | 0 | 1 | 0 | 2 |
| egyéb (kihagyott címke / többszavas kifejezés) | 1 | 0 | 0 | 0 | 1 |

A helyes A-döntések Strongonként: H0853 21 (R1 11, R2 3, R3 7), H1992 1 (R3 1).

Leggyakoribb Strongok a hibákban: H0413 (8), H3588 (8), H3605 (8), H3808 (7), H5921 (7), H0408 (6), H0854 (4), H1961 (4), H0176 (3), H0834 (3), H5704 (3), H0518 (2), H0575 (2), H0859 (2), H1571 (2).

### Példák (versrendben, okonként legfeljebb 5, összesen legfeljebb 15)

| vers | eredeti szó | az aranyban (magyar) | KJV-címkézési arány (korpusz) | a KJV-sor a versben nem illeszkedő címkéi | ok |
|---|---|---|---|---|---|
| 2Móz 20:23 | #1 לֹ֥א H3808 [not] | 1 Ne | H3808 68/3894 | — | ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) |
| 2Móz 20:23 | #4 אִתִּ֑ H0854 [with] | 4 mellém | H0854 16/808 | — | ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) |
| 2Móz 20:23 | #11 לֹ֥א H3808 [not] | 10 se | H3808 68/3894 | — | ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) |
| 2Móz 20:25 | #2 אִם H0518 [if] | 1 Ha | H0518 39/917 | — | ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) |
| 2Móz 20:25 | #8 לֹֽא H3808 [not] | 7 ne | H3808 68/3894 | — | ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi) |
| Péld 25:24 | #11 חָֽבֶר H2269 [association] | 11 közös | H2269 3/6 | H2267 | más Strong a KJV-sorban (a vers eredetijében nem szereplő KJV-címke) |
| Péld 31:5 | #11 עֹֽנִי H6040 [affliction] | 14 nyomorultnak | H6040 31/36 | — | egyéb (kihagyott címke / többszavas kifejezés) |
| Zsolt 6:5 | #1 שׁוּבָ֣ H7725 [return] | 1 Térj, 2 vissza | H7725 889/930 | H2143 H3034 H4194 H7585 | versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) |
| Zsolt 6:5 | #3 יְ֭הוָה H3068 [O Yahweh] | 3 Uram | H3068 5288/5452 | H2143 H3034 H4194 H7585 | versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) |
| Zsolt 6:5 | #4 חַלְּצָ֣ H2502 [rescue] | 4 mentsd, 5 ki | H2502 36/44 | H2143 H3034 H4194 H7585 | versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) |
| Zsolt 6:5 | #6 נַפְשִׁ֑ H5315 [life] | 6 lelkemet | H5315 605/672 | H2143 H3034 H4194 H7585 | versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) |
| Zsolt 6:5 | #8 ה֝וֹשִׁיעֵ֗ H3467 [save] | 7 segíts, 8 meg | H3467 162/192 | H2143 H3034 H4194 H7585 | versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban) |
| Ez 30:5 | #9 עֶ֣רֶב H6154 [foreigner] | 12 gyülevész | H6154 11/15 | H6153 | más Strong a KJV-sorban (a vers eredetijében nem szereplő KJV-címke) |

## Nyitott kérdések (a kísérlet korlátai, nem döntés)

- A versszámozás-gyanús versek (fent) a KJV-sor forrását érintik, nem a szabályt: ahol a megfeleltetett KJV-vers helyett a szomszédos illeszkedik, ott a `Karoli_versmegfeleltetes.tsv` igehely_kjv oszlopa (és így a `tokenek.kjv_tamapont_teljes`) más verset ad. Ugyanez a KJV-sor megy a C-nek a KJV-támponttal futó változatokban; a javítás nem e mérés hatásköre (a tábla és a tokenek.py nem része a feladatnak).
- Az R4-ben (és a Zsolt 22:32-ben) nincs KJV-sor: a teljes táblában van ÚSZ-adat, de a Károli → KJV versmegfeleltetés csak az ÓSZ-t fedi; ott a szabály nem alkalmazható, és a hiányt a szkript nem tölti ki.
- A kizárási lista csak a K-szabályok Strongjait zárja ki. Hogy a KJV által jellemzően nem címkézett funkciószavak (a „ritkán címkézett Strong” hibaok) kizárása mit adna, az a fenti hibaok-táblából látszik, de egy erre szabott lista ugyanezen a 60 versen mérve nem volna független mérés; a szkript nem tartalmazza.
- A korpusz-szintű címkézési arány verstalálaton alapul (a Strong szerepel-e a vers KJV-címkéi között), nem szószintű illesztésen; a versen belül ismétlődő Strongot nem különbözteti meg.
- A szabály versszintű halmazokkal dolgozik: ha egy Strong a versben kétszer áll, és a KJV csak egyszer címkézi, mindkét előfordulás „van KJV-tag” (a fordítatlan második nem jelölt).
- A mérés 60 versen fut; a C-összevetés csak a KJV-szabály döntésein értelmezett, nem a C teljes pontossága.

