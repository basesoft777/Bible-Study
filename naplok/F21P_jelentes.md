# F21P_jelentes.md — Károli–Strong mérőpilot: záró jelentés (P6)

<!-- GENERÁLT: eszkozok/karoli_strong/jelentes_f21p.py | forras=f21p/meres_eredmeny.tsv, f21p/meres_v2_eredmeny.tsv, f21p/koltseg_vetites.tsv, f21p/ingadozas.tsv, f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/futasnaplo.tsv | kézzel szerkeszteni tilos -->

A számok kizárólag szkriptkimenetből jönnek (a forrás soronként jelölve). A **korrigált** értékek kizárólag „**Opus-besorolás, nem mérés**” jelöléssel szerepelnek; a küszöb szempontjából csak a mért érték számít (PD10). A jelentés nem ajánl döntést a #22-ről.

## (a) Eredmény

**A Döntési szabály szerint egyik összeállítás sem felel meg.** A rögzített öt feltétel (`magas` pontosság ≥ 98% minden rétegben; lefedettség ≥ 95%; régi arany ≥ 95%; vetített költség 90%-os felső széle ≤ 60 USD; vetített `alacsony` arány ≤ 10%) összeállításonként:

| összeállítás | magas pontosság ≥ 98% | lefedettség ≥ 95% | régi arany ≥ 95% | költség ≤ 60 USD | alacsony ≤ 10% | minősítés |
|---|---|---|---|---|---|---|
| A | n.é. (egymodelles, PD6) | mért: 81.5% (528/648) — nem minősíthető | mért: 83.3% (20/24) | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |
| B | n.é. (egymodelles, PD6) | mért: 79.2% (742/937) — nem minősíthető | mért: 66.7% (4/6) | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |
| C | n.é. (egymodelles, PD6) | mért: F3 94.1% (989/1051) (arany v1), F3V2 97.1% (1020/1051) (arany v2) — nem minősíthető | mért: F3V2 100.0% (30/30) (hibás hármasok nélkül) | vetítve: F3V2 42.0298 USD [37.9494–46.1468] | n.é. (PD6) | nem minősíthető (PD6) |
| A+B | **bukott**: A∩B pontosság R1 85.2% (52/61), R2 98.4% (61/62), R3 91.8% (179/195), R4 91.7% (77/84) | nem mért (F4 nélkül nincs végső linkhalmaz; A∩B lefedettség: 65.3% (369/565)) | mért (A∩B): 60.0% (3/5) | nem vetítve (PD8) | nem mért (F4 nélkül; PD8) | nem felel meg |
| A+B+C | nem mért (az F4 nem futott, PD8) | nem mért | nem mért | nem vetítve | nem mért | nem felel meg (nem mérhető) |

## (b) Mi bukott el

- **Az A+B pontossága:** az A∩B (`magas`) linkek pontossága a 98%-os küszöb alatt: R1 85.2% (52/61), R2 98.4% (61/62), R3 91.8% (179/195), R4 91.7% (77/84) (forrás: meres_eredmeny.tsv, pontossag_lefedettseg).
- **Az A és a B kapuhibája:** végleges kapuhiba A 41.0% (82/200), B 41.0% (82/200); első próbára A 76.0% (152/200), B 53.0% (106/200). A döntőbíróhoz menne (eltérő, csak egyik átment, egyik sem): 98.5% (197/200) (meres_eredmeny.tsv, kapuhiba és ab_osszeallitas).
- **A C:** egymodelles összeállítás, a PD6 szerint nem kaphat megfelelt minősítést (a `magas`/`alacsony` szint egy modellnél nem értelmezhető). A rétegenkénti 98%-hoz mérten a mért összpontosság az arany v2-n F3: R1 94.6% (295/312), R2 94.2% (146/155), R3 91.9% (250/272), R4 92.9% (299/322); F3V2: R1 94.0% (299/318), R2 95.6% (153/160), R3 94.2% (259/275), R4 91.7% (309/337) (rétegenként l. (c)). A korrigált (Opus-besorolás, nem mérés) érték nem számít.
- **Az A+B+C:** az F4 nem futott (PD8), tehát nem mérhető.

## (c) A mért számok

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

### Régi arany egyezés (halmaz-definíció, PD9; a 2 hibás hármas nélkül is)

| összeállítás | kizárás nélkül | hibás hármasok nélkül |
|---|---|---|
| A (arany-független, 200 verses minta) | 83.3% (20/24) | 90.9% (20/22) |
| B (arany-független, 200 verses minta) | 66.7% (4/6) | 66.7% (4/6) |
| C (arany-független, 200 verses minta) | 93.8% (30/32) | 100.0% (30/30) |
| A+B magas (A∩B) (arany-független, 200 verses minta) | 60.0% (3/5) | 60.0% (3/5) |
| C — F3V2 | 93.8% (30/32) | 100.0% (30/30) |

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
| F2 | 0.017725 |
| F3 | 0.257251 |
| F3V2 | 0.256731 |
| F5 | 0.060663 |
| F6 | 0.009506 |
| **a pilot összesen** | **0.734594** (plafon: 3 USD) |

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

## (d) Költségvetítés (P5, csak a C; forrás: koltseg_vetites.tsv)

Módszer: illesztés tokenfajtánként az első próbálkozású hívásokon (bemenet = a + b·x + c·k; kimenet = a + b·x; x = eredeti + Károli-szavak, k = KJV-támpont szavai); a teljes Biblia valódi vershosszai (Karoli_1908, TAHOT/TAGNT); ár a cost mezőből; az újrakérés a pilot mért szorzójával; bootstrap a kötegek felett (1000); ellenőrzés a 200 versen.

| réteg | könyvek | versek |
|---|---|---|
| R1 | 1Móz 2Móz 3Móz 4Móz 5Móz Józs Bír Ruth 1Sám 2Sám 1Kir 2Kir 1Krón 2Krón Ezsd Neh Eszt Péld Préd | 14006 |
| R2 | Jób Zsolt Én | 3712 |
| R3 | Ézs Jer Sir Ez Dán Hós Jóel Ámós Abd Jón Mik Náh Hab Sof Hag Zak Mal | 5486 |
| R4 | Mt Mk Luk Ján ApCsel Róm 1Kor 2Kor Gal Ef Fil Kol 1Thessz 2Thessz 1Tim 2Tim Tit Filem Zsid Jak 1Pét 2Pét 1Ján 2Ján 3Ján Júd Jel | 7954 |

A besorolás szabálya: műfaj és kánonrész, a minta rétegeivel összhangban (R1: Törvény, történeti könyvek, Péld, Préd; R2: Jób, Zsolt, Én; R3: Ézs–Mal a Siralmakkal és Dániellel; R4: az ÚSZ).

| futás | illesztés (bemenet a/b/c; kimenet a/b) | cost/táblaár (1. próba) | újrakérés-szorzó M | 200 vers: vetített / tényleges (eltérés) | leave-one-out eltérés |
|---|---|---|---|---|---|
| F3 | 1898.37 / 12.0799 / 4.6521 ; 135.08 / 3.3741 | 0.999992 | 1.295538 | 0.257253 / 0.257251 USD (0.001%) | -0.149% |
| F3V2 | 2939.52 / 12.0797 / 4.6518 ; 117.52 / 3.4544 | 0.999999 | 1.194298 | 0.256731 / 0.256731 USD (0.0%) | -0.148% |

Az újrakérések cost-ja nem lineáris a tokenben (a megismételt előtag gyorsítótárazott), ezért az újrakérést nem tokenből, hanem a mért M szorzóval vetítjük.

| réteg | F3 (prompt v1) USD [90%] | F3V2 (prompt v2) USD [90%] |
|---|---|---|
| R1 | 20.7157 [18.4867–23.0838] | 20.5079 [18.4766–22.515] |
| R2 | 3.4895 [3.1504–3.8685] | 3.5672 [3.2356–3.9119] |
| R3 | 8.0427 [7.1768–8.9604] | 7.9682 [7.1701–8.7547] |
| R4 | 9.9849 [8.9596–11.1123] | 9.9865 [9.0298–10.9656] |
| Összes | 42.2328 [37.782–47.0314] | 42.0298 [37.9494–46.1468] |

**Kézimunka-vetítés (C):** az aranyon mért eltérés/vers és a (c)-hiba/vers (ez utóbbi Opus-besorolás, nem mérés), rétegenként a teljes Bibliára; a rétegenkénti arany kis mintájú (10–20 vers). `alacsony` arány: n.é. (PD6).

| futás | eltérés/vers (mért, 60 aranyvers) | vetített eltérés a Bibliára | (c)/vers (Opus-besorolás, nem mérés) | vetített (c) a Bibliára (Opus-besorolás, nem mérés) |
|---|---|---|---|---|
| F3 | 2.2 | 69608 | 0.6167 | 18340 |
| F3V2 | 1.6833 | 54649 | 0.65 | 20625 |

## (e) Nyitott tételek a #22 esetleges újraindításához (DT7), átvihető eszközök, megtanult korlátok

### Öt nyitott tétel (nincs v3, nincs újabb futás; DT7)

1. **G / K7:** a prompt_v2 G-szabályának kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet K7-e (*tudja vala*, *megy vala*): melyik az irányadó.
2. **C:** a prompt „azt, őt …” felsorolása a C-nél az *'et* nélküli, betoldott tárgyi névmásokra is általánosult.
3. **„azt … hogy” / „azért … hogy”:** az arany az előbbit betoldásnak veszi, az utóbbit (Mt 21:4) köti.
4. **2Móz 26:13 *is*:** a K9 szerint a *ve-* az *is*-hez köthető volna; az arany v2 forditatlan-nak veszi (az F3V2-nél (b)).
5. **D:** a birtokláncban (*szolgálójának szemét*) nem egyértelmű, melyik szó viseli a ragot.

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
- A prompt-szabályok túlkötést okozhatnak: az F3V2 több linket ad (1090 link az F3 1061-ével szemben, arany v2).

### A #22 opcióinak következményei (tények, ajánlás nélkül)

- **Marad (a jelenlegi céllal):** a Döntési szabály szerint egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8), az A és a B kiesett, a C egyedül a PD6 szerint nem minősíthető. A teljes futás a jelenlegi szabállyal nem indítható.
- **Módosított céllal indul:** a mért adat (C pontossága, lefedettsége, kapuhibája, a vetített költség) rendelkezésre áll; a Döntési szabály vagy a PD6 módosítása felhasználói döntés; az öt nyitott tétel és a prompt túlkötése nyitott.
- **Elhalasztva:** az eszközök, az arany v2 és a mért adat megmarad; a nyitott tételek dokumentálva.

## (f) A korrigált értékek (Opus-besorolás, nem mérés)

A küszöb szempontjából csak a mért érték számít. A (c)-hibák (az arany szerinti valódi C-hibák) darabszáma az Opus besorolása: F3 × arany v1: 37; F3 × arany v2: 37; F3V2 × arany v2: 39 (f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv). A korrigált pontosság és lefedettség: naplok/F21P_C_diff.md és naplok/F21P_C_diff_F3V2.md, ugyanezzel a jelöléssel.

