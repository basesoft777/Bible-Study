# F21P_C_diff_F3V2.md — az F3V2 eltérései az arany v2-höz és a (c) esetek összevetése az F3-mal

<!-- GENERÁLT: eszkozok/karoli_strong/c_diff_f3v2.py (c_diff.py --f3v2) | forras=f21p/valaszok/F3.jsonl, f21p/valaszok/F3V2.jsonl, f21p/arany_opus_v2.jsonl (befagyasztva), f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv | kézzel szerkeszteni tilos -->

A megszűnt/maradt/új/örökölt állapot gépi; az F3V2-osztály és a változást magyarázó konvenció (K1–K10) **kézi ítélet (Opus), nem mérés**, és a futás után kerül a f21p/c_diff_f3v2_osszevetes.tsv-be.

| réteg | maradt | megszunt | nem_merheto | uj | oroklott |
|---|---|---|---|---|---|
| R1 | 4 | 0 | 0 | 16 | 17 |
| R2 | 0 | 0 | 0 | 3 | 4 |
| R3 | 5 | 11 | 0 | 7 | 11 |
| R4 | 7 | 10 | 0 | 21 | 6 |
| Összes | 16 | 21 | 0 | 47 | 38 |

## A (c) hibák: F3 (v1 prompt) és F3V2 (prompt v2), az arany v2-höz

A mért értékek (pontosság, lefedettség, küszöb-viszony) a naplok/F21P_meres_v2.md a)–e) pontjában; a küszöb szempontjából csak azok számítanak. Az alábbi osztályok és a korrigált értékek **az Opus besorolása, nem mérés**.

| réteg | F3 (c) | F3V2 (c) | ebből maradt | ebből új | F3 megszűnt (c) | F3V2 (a) | F3V2 (b) |
|---|---|---|---|---|---|---|---|
| R1 | 4 | 13 | 4 | 9 | 0 | 15 | 9 |
| R2 | 0 | 1 | 0 | 1 | 0 | 3 | 3 |
| R3 | 16 | 8 | 5 | 3 | 11 | 12 | 3 |
| R4 | 17 | 17 | 7 | 10 | 10 | 16 | 1 |
| Összes | 37 | 39 | 16 | 23 | 21 | 46 | 16 |

### Korrigált pontosság és lefedettség — az Opus besorolása, nem mérés

Az (a) és (b) eltérést nem-hibának véve (F3: a v1-besorolás öröklődik; F3V2: a fenti kézi besorolás). A küszöb szempontjából csak a mért érték számít.

| réteg | mérőszám | F3 × v2 mért | F3 × v2 korrigált (Opus, nem mérés) | F3V2 × v2 mért | F3V2 × v2 korrigált (Opus, nem mérés) |
|---|---|---|---|---|---|
| R1 | pontosság | 94.6% (295/312) | 99.4% (310/312) | 94.0% (299/318) | 97.5% (310/318) |
| R1 | lefedettség | 93.1% (295/317) | 99.4% (315/317) | 94.3% (299/317) | 98.4% (312/317) |
| R2 | pontosság | 94.2% (146/155) | 100.0% (155/155) | 95.6% (153/160) | 99.4% (159/160) |
| R2 | lefedettség | 95.4% (146/153) | 100.0% (153/153) | 100.0% (153/153) | 100.0% (153/153) |
| R3 | pontosság | 91.9% (250/272) | 97.1% (264/272) | 94.2% (259/275) | 97.8% (269/275) |
| R3 | lefedettség | 94.0% (250/266) | 97.0% (258/266) | 97.4% (259/266) | 99.2% (264/266) |
| R4 | pontosság | 92.9% (299/322) | 96.9% (312/322) | 91.7% (309/337) | 96.1% (324/337) |
| R4 | lefedettség | 94.9% (299/315) | 97.8% (308/315) | 98.1% (309/315) | 98.7% (311/315) |
| Összes | pontosság | 93.3% (990/1061) | 98.1% (1041/1061) | 93.6% (1020/1090) | 97.4% (1062/1090) |
| Összes | lefedettség | 94.2% (990/1051) | 98.4% (1034/1051) | 97.1% (1020/1051) | 99.0% (1040/1051) |

## A változás konvenciónként (kézi besorolás)

segített = a v1 (c) eset megszűnt, és a megnevezett konvenció (prompt-szabály) magyarázza; nem segített = a v1 (c) eset maradt, pedig a konvenció rá vonatkozik; ártott = új (c) eset, amelyet a konvenció szabálya váltott ki; új (a)/(b) = új konvenciókülönbség vagy az arany vitatható döntése. „nincs” = nem konvenció, modell-ingadozás.

| konvenció | segített (v1 (c) megszűnt) | nem segített (v1 (c) maradt) | ártott (új (c)) | új (a) | új (b) |
|---|---|---|---|---|---|
| K1 | 1 | 0 | 0 | 1 | 0 |
| K2 | 2 | 1 | 3 | 8 | 1 |
| K3 | 0 | 0 | 3 | 0 | 0 |
| K4 | 2 | 2 | 2 | 0 | 0 |
| K6 | 1 | 0 | 0 | 1 | 0 |
| K7 | 0 | 0 | 2 | 3 | 0 |
| K9 | 1 | 0 | 0 | 4 | 2 |
| nincs | 14 | 13 | 13 | 0 | 4 |

## Jellemző példák (kézi válogatás)

| vers | irány | magyar szó | eredeti szó | állapot | F3V2-osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|
| Jer 46:21 | hianyzo | 2 zsoldosai | 3 הָ H9024 [its] | megszunt | — | — | K4 | a zsoldosai birtokos ragja most a zsoldosai-n: a prompt D szabálya segített |
| Ez 46:12 | tobblet | 25 ő | 27 וֹ֙ H9023 [his] | megszunt | — | — | K6 | az ő már nem a birtokos raghoz kötött, hanem az igéhez (a prompt F szabálya a névmás–ige viszonyt tette láthatóvá): a (c) eset (a)-vá lett |
| Mt 11:18 | tobblet | 4 a | 5 ἐσθίων G2068 [eating] | uj | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a ki -> az igenév (ἐσθίων): a K2 opciója; konvenciókülönbség (a v1 (c) esetből) |
| Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | maradt | c | — | K4 | a -י a fiam-hoz tartozik; a C továbbra is az engem-hez köti. A prompt D szabálya nem segített |
| 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | uj | c | — | K4 | a -וֹ („az ő [a férfi]”) a szolgálójának birtokos ragja; a C a szemét (-é- birtokjel) szóhoz tette. A prompt D szabálya („ahhoz a magyar szóhoz, amelyik a személyragot viseli”) itt két jelölt közül a rosszat választatta: ártott |
| 2Móz 26:13 | tobblet | 23 is | 26 וּ H9002 [and] | uj | b | 6. szakasz táblázat: 2Móz 26:13 | K9 | a וּ a C-nél az is-hez kötődik: ez a prompt I szabálya („ha a helyén is áll, ahhoz kösd”) szerint következetes; az arany v2 a vav-ot forditatlan-nak, az is-t (6. táblázat) betoldas-nak veszi. Ez a v2-diff nyitott kérdése (az is-hez kötés); a C mindkét is-hez köti |
| Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | uj | c | — | nincs | mint fent |
| Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | uj | c | — | K3 | az azt (azt mondom) Károli betoldása; a C a λέγω-hoz köti. A prompt C szabálya (azt, őt ... a raghoz) általánosítva ártott |
| Mt 27:18 | tobblet | 4 vala | 1 ᾔδει G1492 [He knew] | uj | a | K7 segédige (2. szakasz 7.; prompt G) | K7 | tudja vala: a K7 szerint a vala segédige (betoldas); a prompt G kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet K7-e, és a C ezt alkalmazta: új konvenciókülönbség |
| Zsolt 18:3 | tobblet | 7 és | 4 וּ H9002 [and] | uj | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | K9 | a magyarban egy és van; a C mindkét וּ-t (4, 7) hozzáköti. A prompt I szabálya szerint az első וּ helyén nincs kötőszó (forditatlan): új konvenciókülönbség |
| 1Pét 5:12 | tobblet | 22 a | 21 εἰς G1519 [in] | uj | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a melyben: a C az εἰς-t mindkét tokenhez (a, melyben) köti, a prompt B „mindkét szavát” szabálya szerint; az arany az εἰς-t csak a melyben-hez: új konvenciókülönbség |
| 2Móz 21:6 | hianyzo | 6 ura | 5 ו֙ H9023 [his] | oroklott | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő ura: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jer 51:3 | tobblet | 2 kézívesre | 4 דֹּרֵךְ֙ H1869 [[one] bending] | uj | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | nincs | a kézívesre a Ketiv-olvasat szerint a kettőzött ige / a „hajlító” (דֹּרֵךְ) része; a C a דֹּרֵךְ-ot köti hozzá. A jegyzet 3. szakaszán alapuló vitatható eset (F21.12-es döntés szerint b) |

## Minden új (c) eset

| vers | irány | magyar szó | eredeti szó | állapot | F3V2-osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|
| 2Móz 20:25 | tobblet | 13 a | 18 הָ H9034 [it] | uj | c | — | K2 | az a mint (Károli-betoldás, 6. táblázat) a C-nél a rávetetted tárgyi ragjához (-hā, „rá”) kötődik: nyelvileg téves. A prompt B szabálya („a kettéírt kötőszó mindkét szavát kösd”) kerestetett megfelelőt, és rosszat talált: ártott |
| 2Móz 20:25 | tobblet | 14 mint | 18 הָ H9034 [it] | uj | c | — | K2 | mint fent (a mint token) |
| 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | uj | c | — | K4 | a -וֹ („az ő [a férfi]”) a szolgálójának birtokos ragja; a C a szemét (-é- birtokjel) szóhoz tette. A prompt D szabálya („ahhoz a magyar szóhoz, amelyik a személyragot viseli”) itt két jelölt közül a rosszat választatta: ártott |
| 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | uj | c | — | K4 | mint fent (a rag a szemét-en) |
| 2Móz 26:13 | tobblet | 9 abból | 12 עֹדֵ֔ף H5736 [surplus] | uj | c | — | K2 | az abból a ba- (11) megfelelője; a C a „fölösleges” igenevet (12) is hozzáköti. A prompt B szabályának igenév-ága (a vonatkozó szerkezet az igenévhez) átterjedt a korrelatív abból-ra: ártott |
| Péld 25:24 | hianyzo | 4 tetőnek | 5 גָּ֑ג H1406 [a roof] | uj | c | — | nincs | tetőnek ormán = a tető (גָּג) sarka (פִּנָּה): a C felcserélte (tetőnek -> sarok, ormán -> tető); modell-ingadozás, nem konvenció |
| Péld 25:24 | hianyzo | 5 ormán | 4 פִּנַּת H6438 [[the] corner of] | uj | c | — | nincs | mint fent |
| Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | uj | c | — | nincs | mint fent |
| Péld 25:24 | tobblet | 5 ormán | 5 גָּ֑ג H1406 [a roof] | uj | c | — | nincs | mint fent |
| Zsolt 22:32 | tobblet | 13 ezt | 10 עָשָֽׂה H6213 [he has acted] | uj | c | — | K3 | az ezt Károli betoldása (tárgyi mutató névmás, az eredetiben nincs); a C az igéhez köti. A prompt C szabálya a tárgyi névmásokat (azt, őt ...) sorolja, ez általánosítva ártott |
| Jer 51:3 | hianyzo | 15 ifjainak | 16 אֶל H0413 [<to>] | uj | c | — | nincs | az אֶל (a kímél tárgya) az ifjainak -nak ragja; a C forditatlan-nak veszi |
| Ez 16:57 | tobblet | 7 te | 7 עֵ֚ת H6256 [[the] time of] | uj | c | — | nincs | a te (a 6. táblázat szerint betoldas) a C-nél az עֵת („idő”) szóhoz kötve: nyelvileg nem védhető |
| Ez 33:31 | tobblet | 15 mint | 14 י H9020 [my] | uj | c | — | nincs | a mint (6. táblázat: betoldas) a C-nél a -י („én népem”) raghoz kötve: nem védhető |
| Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | uj | c | — | K3 | az azt (azt mondom) Károli betoldása; a C a λέγω-hoz köti. A prompt C szabálya (azt, őt ... a raghoz) általánosítva ártott |
| Mt 6:31 | tobblet | 4 és | 4 λέγοντες· G3004 [saying;] | uj | c | — | nincs | az és (betoldas) a C-nél a λέγοντες igenévhez kötve |
| Mt 11:18 | tobblet | 11 azt | 9 λέγουσιν· G3004 [they say;] | uj | c | — | K3 | az azt (azt mondják) Károli betoldása; a C a λέγουσιν-hoz köti (a prompt C szabálya általánosítva): ártott |
| Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | uj | c | — | K7 | a jól Károli betoldása; a C az ᾔδει-hez köti (a prompt G kivételének „minden tagja” fordulata húzta magával): ártott |
| Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | uj | c | — | K7 | a hogy (lőn, hogy) Károli betoldása; a C az ἐγένετο-hoz köti (a G kivétel kiterjesztése): ártott |
| Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | uj | c | — | nincs | tudván azt, hogy: az azt (korrelatív) a C-nél a ὅτι-hoz kötve; az arany betoldas [az arany döntése is vitatható; a jegyzetben nem szerepel] (vö. Mt 21:4: azért -> ἵνα kötve) |
| Jak 3:4 | hianyzo | 15 kormánytól | 13 ὑπὸ G5259 [by] | uj | c | — | nincs | az ὑπό a kormánytól -tól ragja; a C a mindazáltal-hoz tette |
| Jak 3:4 | hianyzo | 19 hová | 17 ἂν G0302 [ever] | uj | c | — | nincs | az ἄν a hová-é (ὅπου ἄν); a C most csak az oda-hoz köti |
| Jak 3:4 | tobblet | 12 mindazáltal | 13 ὑπὸ G5259 [by] | uj | c | — | nincs | a mindazáltal (Károli-betoldás) a C-nél az ὑπό-hoz kötve |
| 1Ján 1:10 | tobblet | 2 azt | 3 ὅτι G3754 [that] | uj | c | — | nincs | azt mondjuk, hogy: az azt (korrelatív) a C-nél a ὅτι-hoz kötve; az arany betoldas [az arany döntése is vitatható; a jegyzetben nem szerepel] |

## Minden megszűnt (c) eset (a v1 F3 (c) hibái, amelyek az F3V2-nél nem eltérések)

| vers | irány | magyar szó | eredeti szó | állapot | F3V2-osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|
| Jer 46:21 | hianyzo | 2 zsoldosai | 3 הָ H9024 [its] | megszunt | — | — | K4 | a zsoldosai birtokos ragja most a zsoldosai-n: a prompt D szabálya segített |
| Jer 46:21 | hianyzo | 4 olyanok | 7 כְּ H9004 [[are] like] | megszunt | — | — | nincs | olyanok ... mint: a C most az olyanok-at is a כְּ-hoz köti; konvenció nem szól róla |
| Jer 46:21 | hianyzo | 13 is | 11 גַם H1571 [also] | megszunt | — | — | nincs | ők is = גַם הֵמָּה: most helyes; modell-ingadozás |
| Jer 46:21 | tobblet | 3 is | 3 הָ H9024 [its] | megszunt | — | — | K4 | az is már nem kapja a birtokos ragot (D szabály): segített |
| Jer 51:3 | hianyzo | 8 arra | 8 אֶל H0408 [may not] | megszunt | — | — | nincs | az arra most az אֶל-hez kötve; konvenció nem érinti (Ketiv-olvasat, a jegyzet 3. szakasza) |
| Jer 51:3 | hianyzo | 11 pánczéljába | 10 בְּ H9003 [in] | megszunt | — | — | nincs | a be- most a pánczéljába-n; a v1 2. pontja (elöljáró a ragot viselő szóhoz) a v1-ben is megvolt: modell-ingadozás |
| Jer 51:3 | tobblet | 8 arra | 10 בְּ H9003 [in] | megszunt | — | — | nincs | az arra már nem kapja a be--t; modell-ingadozás |
| Ez 16:57 | hianyzo | 16 valóknak | 13 סְבִיבוֹתֶ֖י H5439 [around] | megszunt | — | — | nincs | a valóknak most kötve (a „való” szerkezetre nincs konvenció; a prompt_v2-ből kikerült a való-betoldásos Mt 1:1-es példa) |
| Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | megszunt | — | — | nincs | olyanok ... mint: most kötve; konvenció nem szól róla |
| Ez 46:12 | tobblet | 25 ő | 27 וֹ֙ H9023 [his] | megszunt | — | — | K6 | az ő már nem a birtokos raghoz kötött, hanem az igéhez (a prompt F szabálya a névmás–ige viszonyt tette láthatóvá): a (c) eset (a)-vá lett |
| Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | megszunt | — | — | K9 | az azután már nem a „kimegy” igéhez kötött, hanem a ve--hez (prompt I): a (c) eset (a)-vá lett |
| Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | megszunt | — | — | nincs | a második ne most a μή-hez kötve; modell-ingadozás |
| Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | megszunt | — | — | K2 | a ki már nem a μήτε-hez kötött, hanem az igenévhez (prompt B / K2 opció): a (c) eset (a)-vá lett |
| Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | megszunt | — | — | K2 | mint fent |
| Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszunt | — | — | nincs | azért ... hogy: az azért most kötve; konvenció nem szól a korrelatívumról |
| Mt 23:31 | hianyzo | 2 hát | 1 ὥστε G5620 [Thus] | megszunt | — | — | nincs | Így hát: a hát most kötve; modell-ingadozás |
| Jak 3:4 | tobblet | 12 mindazáltal | 12 μετάγεται G3329 [are turned about] | megszunt | — | — | nincs | a mindazáltal már nem a μετάγεται-hez kötött — de új hibás link keletkezett (mindazáltal -> ὑπό); modell-ingadozás |
| Jak 3:4 | tobblet | 23 akarja | 19 ὁρμὴ G3730 [impulse] | megszunt | — | — | nincs | az akarja már nem az ὁρμή-hez kötött (a kizárt 22. tokenhez); modell-ingadozás |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 21 ὁ G3588 [<the>] | megszunt | — | — | K1 | a névelő (ὁ) már forditatlan (prompt A): segített; a θεός-link maradt |
| 2Pét 1:7 | hianyzo | 6 való | 6 φιλαδελφίαν, G5360 [brotherly affection,] | megszunt | — | — | nincs | a való most kötve (a „való”-ra nincs konvenció; a való-betoldásos Mt 1:1-es példa kikerült a promptból) |
| 2Pét 1:7 | hianyzo | 10 való | 10 φιλαδελφίᾳ G5360 [brotherly affection] | megszunt | — | — | nincs | mint fent |

## Minden maradt (c) eset

| vers | irány | magyar szó | eredeti szó | állapot | F3V2-osztály | konvenció / jegyzetpont | változás-konvenció | indok (kézi) |
|---|---|---|---|---|---|---|---|---|
| Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | maradt | c | — | K4 | a -י a fiam-hoz tartozik; a C továbbra is az engem-hez köti. A prompt D szabálya nem segített |
| Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | maradt | c | — | K4 | az engem (betoldás) a C-nél a fiam ragjával; a D szabály nem segített |
| Péld 31:8 | hianyzo | 13 dolgában | 6 אֶל H0413 [to] | maradt | c | — | nincs | az אֶל a dolgában ragja; a C továbbra is az és-hez köti; konvenció nem érinti |
| Péld 31:8 | tobblet | 11 és | 6 אֶל H0413 [to] | maradt | c | — | nincs | mint fent |
| Jer 46:21 | hianyzo | 3 is | 1 גַּם H1571 [also] | maradt | c | — | nincs | Még ... is = גַּם (1); a C az első is-t továbbra is a második גַם-hoz köti; modell-ingadozás |
| Jer 46:21 | tobblet | 3 is | 11 גַם H1571 [also] | maradt | c | — | nincs | az első is továbbra is a második גַם-on |
| Jer 51:3 | tobblet | 10 ki | 8 אֶל H0408 [may not] | maradt | c | — | K2 | a ki (vonatkozó) továbbra is az אֶל-hez kötve; a prompt B szabálya (vonatkozó igenév nélkül: betoldas) nem segített |
| Ez 11:3 | tobblet | 9 város | 10 סִּ֔יר H5518 [pot] | maradt | c | — | nincs | a város továbbra is a „fazék”-hoz kötve |
| Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | maradt | c | — | nincs | a pedig továbbra is a הֵמָּה-hoz kötve |
| Mt 21:4 | hianyzo | 8 próféta | 9 διὰ G1223 [through] | maradt | c | — | nincs | a διά továbbra is forditatlan |
| Jak 3:4 | tobblet | 16 oda | 17 ἂν G0302 [ever] | maradt | c | — | nincs | az ἄν továbbra is az oda-n |
| 1Pét 4:11 | hianyzo | 14 erővel | 11 ἐξ G1537 [of] | maradt | c | — | nincs | az ἐκ továbbra is az azzal-on [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | maradt | c | — | nincs | a szólja (Károli-kiegészítés) továbbra is a λαλεῖ-hez kötve [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 12 azzal | 11 ἐξ G1537 [of] | maradt | c | — | nincs | mint fent (az ἐκ) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 15 szolgáljon | 9 διακονεῖ G1247 [serves] | maradt | c | — | nincs | a szolgáljon továbbra is a διακονεῖ-hez kötve [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | maradt | c | — | nincs | a θεός továbbra is a dícsőíttessék-hez kötve (Károli nem fordítja) |

## Minden eltérés (gépi állapot, kézi besorolás)

| vers | irány | magyar szó | eredeti szó | állapot | F3-osztály | F3V2-osztály (kézi) | konvenció / jegyzetpont (kézi) | változás-konvenció (kézi) | indok (kézi) |
|---|---|---|---|---|---|---|---|---|---|
| 2Móz 20:23 | hianyzo | 4 mellém | 5 י H9030 [me] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | a -י rag csak az én-hez kötve, a mellém-hez nem; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 20:25 | tobblet | 13 a | 18 הָ H9034 [it] | uj | — | c | — | K2 | az a mint (Károli-betoldás, 6. táblázat) a C-nél a rávetetted tárgyi ragjához (-hā, „rá”) kötődik: nyelvileg téves. A prompt B szabálya („a kettéírt kötőszó mindkét szavát kösd”) kerestetett megfelelőt, és rosszat talált: ártott |
| 2Móz 20:25 | tobblet | 14 mint | 18 הָ H9034 [it] | uj | — | c | — | K2 | mint fent (a mint token) |
| 2Móz 20:25 | tobblet | 18 megfertőztetted | 19 וַ H9001 [and] | oroklott | a | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a le nem fordított vav-konszekutívum az igéhez kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 21:6 | hianyzo | 6 ura | 5 ו֙ H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő ura: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 21:6 | hianyzo | 20 ura | 22 ו H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | mint fent |
| 2Móz 21:6 | hianyzo | 25 fülét | 25 וֹ֙ H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő fülét: mint fent |
| 2Móz 21:26 | hianyzo | 5 szolgájának | 8 וֹ H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő szolgájának: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | uj | — | c | — | K4 | a -וֹ („az ő [a férfi]”) a szolgálójának birtokos ragja; a C a szemét (-é- birtokjel) szóhoz tette. A prompt D szabálya („ahhoz a magyar szóhoz, amelyik a személyragot viseli”) itt két jelölt közül a rosszat választatta: ártott |
| 2Móz 21:26 | hianyzo | 20 szeméért | 23 וֹ H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő szeméért: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 21:26 | tobblet | 1 Ha | 1 וְ H9002 [and] | oroklott | b | b | 6. szakasz táblázat: 2Móz 21:26 | — | a C a jegyzet alternatíváját választotta (Ha -> 1, 2), mint az F3 |
| 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | uj | — | c | — | K4 | mint fent (a rag a szemét-en) |
| 2Móz 21:26 | tobblet | 10 úgy | 14 וְ H9001 [and] | oroklott | b | b | 6. szakasz táblázat: 2Móz 21:26 | — | úgy ... hogy korrelatív; nem a jegyzet alternatívája, mint az F3-nál |
| 2Móz 25:8 | hianyzo | 8 közöttök | 10 ם H9028 [them] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | a -ām rag csak az ő-höz, a közöttök-höz nem; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 25:40 | hianyzo | 5 formára | 5 בְּ H9003 [in] | oroklott | b | b | 6. szakasz táblázat: 2Móz 25:40 | — | a be- az arra-n (a -ra rag mindkét szón); mint az F3-nál |
| 2Móz 25:40 | tobblet | 1 Vigyázz | 1 וּ H9002 [and] | oroklott | a | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | — | a kezdő vav a Vigyázz-hoz kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 25:40 | tobblet | 3 arra | 5 בְּ H9003 [in] | oroklott | b | b | 6. szakasz táblázat: 2Móz 25:40 | — | mint fent |
| 2Móz 26:13 | tobblet | 9 abból | 12 עֹדֵ֔ף H5736 [surplus] | uj | — | c | — | K2 | az abból a ba- (11) megfelelője; a C a „fölösleges” igenevet (12) is hozzáköti. A prompt B szabályának igenév-ága (a vonatkozó szerkezet az igenévhez) átterjedt a korrelatív abból-ra: ártott |
| 2Móz 26:13 | tobblet | 11 mi | 12 עֹדֵ֔ף H5736 [surplus] | oroklott | a | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a mi az igenévhez kötve (a K2 listájában megnevezett opció); mint az F3 |
| 2Móz 26:13 | tobblet | 23 is | 26 וּ H9002 [and] | uj | — | b | 6. szakasz táblázat: 2Móz 26:13 | K9 | a וּ a C-nél az is-hez kötődik: ez a prompt I szabálya („ha a helyén is áll, ahhoz kösd”) szerint következetes; az arany v2 a vav-ot forditatlan-nak, az is-t (6. táblázat) betoldas-nak veszi. Ez a v2-diff nyitott kérdése (az is-hez kötés); a C mindkét is-hez köti |
| 2Móz 26:13 | tobblet | 25 is | 26 וּ H9002 [and] | uj | — | b | 6. szakasz táblázat: 2Móz 26:13 | K9 | mint fent (a második is) |
| 2Móz 29:4 | hianyzo | 6 fiait | 7 ו֙ H9023 [his] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő fiait: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 2Móz 30:3 | tobblet | 14 is | 15 וְ H9002 [and] | uj | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | K9 | a ve- (15) az arany szerint az és-hez; a C a szarvait is szócskáját is hozzáköti. A prompt I szabálya a kötőszók között az is-t is felsorolja: a konvenció értelmezésének különbsége (új) |
| Péld 23:19 | hianyzo | 3 fiam | 4 י H9020 [my] | maradt | c | c | — | K4 | a -י a fiam-hoz tartozik; a C továbbra is az engem-hez köti. A prompt D szabálya nem segített |
| Péld 23:19 | hianyzo | 5 hogy | 5 וַ H9002 [and] | uj | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | K9 | a וַ az arany szerint a hogy-hoz; a C forditatlan-nak veszi, a hogy-ot betoldas-nak. A prompt I szabályának ellentmond (a hogy a felsorolt kötőszók között): új konvenciókülönbség |
| Péld 23:19 | hianyzo | 11 úton | 9 בַּ H9003 [in the] | oroklott | a | a | K10 összeolvadt névelő + elöljáró (2. szakasz 10.; prompt J) | — | ez úton: a בַּ csak az ez-hez; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Péld 23:19 | tobblet | 4 engem | 4 י H9020 [my] | maradt | c | c | — | K4 | az engem (betoldás) a C-nél a fiam ragjával; a D szabály nem segített |
| Péld 25:24 | hianyzo | 4 tetőnek | 5 גָּ֑ג H1406 [a roof] | uj | — | c | — | nincs | tetőnek ormán = a tető (גָּג) sarka (פִּנָּה): a C felcserélte (tetőnek -> sarok, ormán -> tető); modell-ingadozás, nem konvenció |
| Péld 25:24 | hianyzo | 5 ormán | 4 פִּנַּת H6438 [[the] corner of] | uj | — | c | — | nincs | mint fent |
| Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | uj | — | c | — | nincs | mint fent |
| Péld 25:24 | tobblet | 5 ormán | 5 גָּ֑ג H1406 [a roof] | uj | — | c | — | nincs | mint fent |
| Péld 28:17 | hianyzo | 11 senki | 9 אַל H0408 [may not] | uj | — | b | 6. szakasz táblázat: Péld 28:17 | nincs | az arany: senki -> 9, 10; a C a senki-t csak az igéhez, a ne-t a tagadóhoz köti (nem a jegyzet alternatívája) |
| Péld 28:17 | tobblet | 7 terhel | 3 בְּ H9003 [by] | uj | — | b | 6. szakasz táblázat: Péld 28:17 | nincs | az arany: be- forditatlan; a C a terhel igéhez köti (nem a jegyzet alternatívája, amely: vér -> 3, 4) |
| Péld 30:17 | tobblet | 3 mely | 2 תִּֽלְעַ֣ג H3932 [[which] it mocks] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a mely a melléknévi igenevet fordítja; a C az igenévhez köti — a K2 listájában megnevezett opció (a prompt B szabályának igenév-ága szerint betoldas lenne): új konvenciókülönbség |
| Péld 31:8 | hianyzo | 12 azoknak | 9 בְּנֵ֥י H1121 [[the] sons of] | oroklott | b | b | 6. szakasz táblázat: Péld 31:8 | — | azoknak csak a כָּל-hoz; mint az F3 |
| Péld 31:8 | hianyzo | 13 dolgában | 6 אֶל H0413 [to] | maradt | c | c | — | nincs | az אֶל a dolgában ragja; a C továbbra is az és-hez köti; konvenció nem érinti |
| Péld 31:8 | tobblet | 11 és | 6 אֶל H0413 [to] | maradt | c | c | — | nincs | mint fent |
| Zsolt 16:11 | tobblet | 1 Te | 1 תּֽוֹדִיעֵ H3045 [you will make known to] | oroklott | a | a | K6 külön kitett alanyi névmás (2. szakasz 6.; prompt F) | — | a külön kitett Te az igéhez kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Zsolt 18:1 | tobblet | 11 ez | 16 הַ H9009 [<the>] | oroklott | a | a | K1 névelők (2. szakasz 1.; prompt A) | — | a mutató névmás névelője az ez-hez kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Zsolt 18:1 | tobblet | 14 azon | 18 בְּ H9003 [on] | oroklott | b | b | 6. szakasz táblázat: Zsolt 18:1 | — | azon -> 18 (a jegyzet alternatívája); mint az F3 |
| Zsolt 18:1 | tobblet | 14 azon | 19 י֤וֹם H3117 [[the] day] | oroklott | b | b | 6. szakasz táblázat: Zsolt 18:1 | — | az alternatíva kiterjesztése a יוֹם-ra; mint az F3 |
| Zsolt 18:3 | tobblet | 7 és | 4 וּ H9002 [and] | uj | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | K9 | a magyarban egy és van; a C mindkét וּ-t (4, 7) hozzáköti. A prompt I szabálya szerint az első וּ helyén nincs kötőszó (forditatlan): új konvenciókülönbség |
| Zsolt 22:32 | tobblet | 8 ő | 8 נ֝וֹלָ֗ד H3205 [about to be born] | uj | — | b | 6. szakasz táblázat: Zsolt 22:32 | nincs | az arany: ő (8) betoldas; a C a נוֹלָד-hoz köti (az utánok való mellett); nem a jegyzet alternatívája |
| Zsolt 22:32 | tobblet | 13 ezt | 10 עָשָֽׂה H6213 [he has acted] | uj | — | c | — | K3 | az ezt Károli betoldása (tárgyi mutató névmás, az eredetiben nincs); a C az igéhez köti. A prompt C szabálya a tárgyi névmásokat (azt, őt ...) sorolja, ez általánosítva ártott |
| Jer 46:21 | hianyzo | 2 zsoldosai | 3 הָ H9024 [its] | megszunt | c | — | — | K4 | a zsoldosai birtokos ragja most a zsoldosai-n: a prompt D szabálya segített |
| Jer 46:21 | hianyzo | 3 is | 1 גַּם H1571 [also] | maradt | c | c | — | nincs | Még ... is = גַּם (1); a C az első is-t továbbra is a második גַם-hoz köti; modell-ingadozás |
| Jer 46:21 | hianyzo | 4 olyanok | 7 כְּ H9004 [[are] like] | megszunt | c | — | — | nincs | olyanok ... mint: a C most az olyanok-at is a כְּ-hoz köti; konvenció nem szól róla |
| Jer 46:21 | hianyzo | 6 közöttök | 6 הּ֙ H9024 [its] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | ő közöttök: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jer 46:21 | hianyzo | 13 is | 11 גַם H1571 [also] | megszunt | c | — | — | nincs | ők is = גַם הֵמָּה: most helyes; modell-ingadozás |
| Jer 46:21 | hianyzo | 27 megfenyíttetésök | 27 ם H9028 [their] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő megfenyíttetésök: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jer 46:21 | tobblet | 3 is | 3 הָ H9024 [its] | megszunt | c | — | — | K4 | az is már nem kapja a birtokos ragot (D szabály): segített |
| Jer 46:21 | tobblet | 3 is | 11 גַם H1571 [also] | maradt | c | c | — | nincs | az első is továbbra is a második גַם-on |
| Jer 51:3 | hianyzo | 8 arra | 8 אֶל H0408 [may not] | megszunt | c | — | — | nincs | az arra most az אֶל-hez kötve; konvenció nem érinti (Ketiv-olvasat, a jegyzet 3. szakasza) |
| Jer 51:3 | hianyzo | 11 pánczéljába | 10 בְּ H9003 [in] | megszunt | c | — | — | nincs | a be- most a pánczéljába-n; a v1 2. pontja (elöljáró a ragot viselő szóhoz) a v1-ben is megvolt: modell-ingadozás |
| Jer 51:3 | hianyzo | 15 ifjainak | 16 אֶל H0413 [<to>] | uj | — | c | — | nincs | az אֶל (a kímél tárgya) az ifjainak -nak ragja; a C forditatlan-nak veszi |
| Jer 51:3 | tobblet | 2 kézívesre | 4 דֹּרֵךְ֙ H1869 [[one] bending] | uj | — | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | nincs | a kézívesre a Ketiv-olvasat szerint a kettőzött ige / a „hajlító” (דֹּרֵךְ) része; a C a דֹּרֵךְ-ot köti hozzá. A jegyzet 3. szakaszán alapuló vitatható eset (F21.12-es döntés szerint b) |
| Jer 51:3 | tobblet | 3 kézíves | 3 הַ H9009 [the] | oroklott | a | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelő a kézíves-hez kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jer 51:3 | tobblet | 8 arra | 10 בְּ H9003 [in] | megszunt | c | — | — | nincs | az arra már nem kapja a be--t; modell-ingadozás |
| Jer 51:3 | tobblet | 10 ki | 8 אֶל H0408 [may not] | maradt | c | c | — | K2 | a ki (vonatkozó) továbbra is az אֶל-hez kötve; a prompt B szabálya (vonatkozó igenév nélkül: betoldas) nem segített |
| Ez 11:3 | tobblet | 9 város | 10 סִּ֔יר H5518 [pot] | maradt | c | c | — | nincs | a város továbbra is a „fazék”-hoz kötve |
| Ez 16:57 | hianyzo | 16 valóknak | 13 סְבִיבוֹתֶ֖י H5439 [around] | megszunt | c | — | — | nincs | a valóknak most kötve (a „való” szerkezetre nincs konvenció; a prompt_v2-ből kikerült a való-betoldásos Mt 1:1-es példa) |
| Ez 16:57 | tobblet | 7 te | 7 עֵ֚ת H6256 [[the] time of] | uj | — | c | — | nincs | a te (a 6. táblázat szerint betoldas) a C-nél az עֵת („idő”) szóhoz kötve: nyelvileg nem védhető |
| Ez 22:25 | hianyzo | 4 prófétái | 3 הָ֙ H9024 [its] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő prófétái: a rag csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Ez 22:25 | hianyzo | 6 közepette | 6 הּ H9024 [it] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | ő közepette: mint fent |
| Ez 22:25 | hianyzo | 7 olyanok | 7 כַּ H9004 [like] | megszunt | c | — | — | nincs | olyanok ... mint: most kötve; konvenció nem szól róla |
| Ez 22:25 | tobblet | 12 mely | 10 טֹ֣רֵֽף H2963 [tearing] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a mely a melléknévi igenevet (טֹרֵף) fordítja; a C az igenévhez köti (a K2 opciója): új konvenciókülönbség |
| Ez 33:31 | hianyzo | 18 népem | 14 י H9020 [my] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az én népem: a rag csak az én-hez; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Ez 33:31 | tobblet | 9 szokott | 6 מְבוֹא H3996 [[the] coming of] | oroklott | b | b | 6. szakasz táblázat: Ez 33:31 | — | szokott -> מְבוֹא; mint az F3 |
| Ez 33:31 | tobblet | 15 mint | 14 י H9020 [my] | uj | — | c | — | nincs | a mint (6. táblázat: betoldas) a C-nél a -י („én népem”) raghoz kötve: nem védhető |
| Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | maradt | c | c | — | nincs | a pedig továbbra is a הֵמָּה-hoz kötve |
| Ez 33:31 | tobblet | 33 nyereség | 34 ם H9028 [their] | oroklott | b | b | 6. szakasz táblázat: Ez 33:31 | — | a nyereség ragja kötve; mint az F3 |
| Ez 39:13 | tobblet | 10 ez | 8 הָיָ֥ה H1961 [it will become] | oroklott | a | a | K6 külön kitett alanyi névmás (2. szakasz 6.; prompt F) | — | lészen ez: az ez a הָיָה-hoz kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Ez 39:13 | tobblet | 15 melyen | 13 י֚וֹם H3117 [[the] day of] | oroklott | a | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a melyen a יוֹם-hoz kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Ez 39:13 | tobblet | 16 megdicsőítem | 15 י H9040 [myself] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | a -י a megdicsőítem-hez is; mint az F3 (a K4 kiterjesztése nyitott kérdés) |
| Ez 46:12 | tobblet | 25 ő | 24 עָשָׂ֤ה H6213 [he will offer] | uj | — | a | K6 külön kitett alanyi névmás (2. szakasz 6.; prompt F) | K6 | az ő (a vigye alanya) most az igéhez kötve; a K6 szerint betoldas: konvenciókülönbség (a v1 (c) esetből, l. megszűnt) |
| Ez 46:12 | tobblet | 25 ő | 27 וֹ֙ H9023 [his] | megszunt | c | — | — | K6 | az ő már nem a birtokos raghoz kötött, hanem az igéhez (a prompt F szabálya a névmás–ige viszonyt tette láthatóvá): a (c) eset (a)-vá lett |
| Ez 46:12 | tobblet | 39 azután | 39 וְ H9001 [and] | uj | — | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | K9 | a ve- (39) az arany szerint az és-hez; a C az azután-t is hozzáköti (a prompt I szabályának kiterjesztése): konvenciókülönbség (a v1 (c) esetből) |
| Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | megszunt | c | — | — | K9 | az azután már nem a „kimegy” igéhez kötött, hanem a ve--hez (prompt I): a (c) eset (a)-vá lett |
| Mt 4:4 | tobblet | 16 a | 17 ἐκπορευομένῳ G1607 [coming out] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a mely: a C mindkét tokent (a, mely) az igenévhez köti (a prompt B „mindkét szavát” ága és a K2 opciója): új konvenciókülönbség |
| Mt 4:4 | tobblet | 17 mely | 17 ἐκπορευομένῳ G1607 [coming out] | oroklott | a | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | — | a mely az igenévhez (a K2 opciója); mint az F3 |
| Mt 5:34 | tobblet | 3 azt | 3 λέγω G3004 [say] | uj | — | c | — | K3 | az azt (azt mondom) Károli betoldása; a C a λέγω-hoz köti. A prompt C szabálya (azt, őt ... a raghoz) általánosítva ártott |
| Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | megszunt | c | — | — | nincs | a második ne most a μή-hez kötve; modell-ingadozás |
| Mt 6:31 | tobblet | 4 és | 4 λέγοντες· G3004 [saying;] | uj | — | c | — | nincs | az és (betoldas) a C-nél a λέγοντες igenévhez kötve |
| Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | megszunt | c | — | — | K2 | a ki már nem a μήτε-hez kötött, hanem az igenévhez (prompt B / K2 opció): a (c) eset (a)-vá lett |
| Mt 11:18 | tobblet | 4 a | 5 ἐσθίων G2068 [eating] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a ki -> az igenév (ἐσθίων): a K2 opciója; konvenciókülönbség (a v1 (c) esetből) |
| Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | megszunt | c | — | — | K2 | mint fent |
| Mt 11:18 | tobblet | 5 ki | 5 ἐσθίων G2068 [eating] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | mint fent |
| Mt 11:18 | tobblet | 11 azt | 9 λέγουσιν· G3004 [they say;] | uj | — | c | — | K3 | az azt (azt mondják) Károli betoldása; a C a λέγουσιν-hoz köti (a prompt C szabálya általánosítva): ártott |
| Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | megszunt | c | — | — | nincs | azért ... hogy: az azért most kötve; konvenció nem szól a korrelatívumról |
| Mt 21:4 | hianyzo | 8 próféta | 9 διὰ G1223 [through] | maradt | c | c | — | nincs | a διά továbbra is forditatlan |
| Mt 21:4 | tobblet | 10 a | 12 λέγοντος· G3004 [saying;] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a ki: a C az igenévhez (λέγοντος) köti — a K2 listájában megnevezett opció; új konvenciókülönbség |
| Mt 21:4 | tobblet | 11 ki | 12 λέγοντος· G3004 [saying;] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | mint fent |
| Mt 21:4 | tobblet | 12 így | 12 λέγοντος· G3004 [saying;] | uj | — | b | 6. szakasz táblázat: Mt 21:4 | K2 | az így (6. táblázat: betoldas) a C-nél szintén az igenévhez kötve (a B szabály igenév-ágának kiterjesztése); nem a jegyzet alternatívája |
| Mt 23:31 | hianyzo | 2 hát | 1 ὥστε G5620 [Thus] | megszunt | c | — | — | nincs | Így hát: a hát most kötve; modell-ingadozás |
| Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | uj | — | c | — | K7 | a jól Károli betoldása; a C az ᾔδει-hez köti (a prompt G kivételének „minden tagja” fordulata húzta magával): ártott |
| Mt 27:18 | tobblet | 4 vala | 1 ᾔδει G1492 [He knew] | uj | — | a | K7 segédige (2. szakasz 7.; prompt G) | K7 | tudja vala: a K7 szerint a vala segédige (betoldas); a prompt G kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet K7-e, és a C ezt alkalmazta: új konvenciókülönbség |
| Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | uj | — | c | — | K7 | a hogy (lőn, hogy) Károli betoldása; a C az ἐγένετο-hoz köti (a G kivétel kiterjesztése): ártott |
| Mk 2:23 | tobblet | 9 vala | 7 παραπορεύεσθαι G3899 [passing through] | uj | — | a | K7 segédige (2. szakasz 7.; prompt G) | K7 | megy vala: a vala a C-nél az igéhez (a prompt G kivétele); az arany a K7 szerint betoldas-nak veszi: új konvenciókülönbség |
| Mk 2:23 | tobblet | 19 vala | 15 ἤρξαντο G0757 [began] | uj | — | a | K7 segédige (2. szakasz 7.; prompt G) | K7 | kezdék vala: mint fent |
| Jak 1:18 | hianyzo | 13 teremtményeinek | 13 αὐτοῦ G0846 [of His] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő teremtményeinek: az αὐτοῦ csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jak 1:18 | tobblet | 10 hogy | 7 τὸ G3588 [<the>] | oroklott | a | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelős főnévi igenév névelője a hogy-hoz kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | uj | — | c | — | nincs | tudván azt, hogy: az azt (korrelatív) a C-nél a ὅτι-hoz kötve; az arany betoldas [az arany döntése is vitatható; a jegyzetben nem szerepel] (vö. Mt 21:4: azért -> ἵνα kötve) |
| Jak 3:4 | hianyzo | 15 kormánytól | 13 ὑπὸ G5259 [by] | uj | — | c | — | nincs | az ὑπό a kormánytól -tól ragja; a C a mindazáltal-hoz tette |
| Jak 3:4 | hianyzo | 19 hová | 17 ἂν G0302 [ever] | uj | — | c | — | nincs | az ἄν a hová-é (ὅπου ἄν); a C most csak az oda-hoz köti |
| Jak 3:4 | tobblet | 12 mindazáltal | 12 μετάγεται G3329 [are turned about] | megszunt | c | — | — | nincs | a mindazáltal már nem a μετάγεται-hez kötött — de új hibás link keletkezett (mindazáltal -> ὑπό); modell-ingadozás |
| Jak 3:4 | tobblet | 12 mindazáltal | 13 ὑπὸ G5259 [by] | uj | — | c | — | nincs | a mindazáltal (Károli-betoldás) a C-nél az ὑπό-hoz kötve |
| Jak 3:4 | tobblet | 16 oda | 17 ἂν G0302 [ever] | maradt | c | c | — | nincs | az ἄν továbbra is az oda-n |
| Jak 3:4 | tobblet | 22 szándéka | 18 ἡ G3588 [the] | uj | — | a | K1 névelők (2. szakasz 1.; prompt A) | K1 | a névelő (ἡ) a szándéka-hoz kötve; a prompt A szabálya ellenére: új konvenciókülönbség |
| Jak 3:4 | tobblet | 23 akarja | 19 ὁρμὴ G3730 [impulse] | megszunt | c | — | — | nincs | az akarja már nem az ὁρμή-hez kötött (a kizárt 22. tokenhez); modell-ingadozás |
| 1Pét 4:11 | hianyzo | 14 erővel | 11 ἐξ G1537 [of] | maradt | c | c | — | nincs | az ἐκ továbbra is az azzal-on [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 7 szólja | 3 λαλεῖ G2980 [speaks] | maradt | c | c | — | nincs | a szólja (Károli-kiegészítés) továbbra is a λαλεῖ-hez kötve [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 12 azzal | 11 ἐξ G1537 [of] | maradt | c | c | — | nincs | mint fent (az ἐκ) [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 15 szolgáljon | 9 διακονεῖ G1247 [serves] | maradt | c | c | — | nincs | a szolgáljon továbbra is a διακονεῖ-hez kötve [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 21 ὁ G3588 [<the>] | megszunt | c | — | — | K1 | a névelő (ὁ) már forditatlan (prompt A): segített; a θεός-link maradt |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | maradt | c | c | — | nincs | a θεός továbbra is a dícsőíttessék-hez kötve (Károli nem fordítja) |
| 1Pét 4:11 | tobblet | 32 örökkön | 34 τοὺς G3588 [the] | oroklott | a | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelő (τούς) az örökkön-höz kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 1Pét 4:11 | tobblet | 33 örökké | 36 τῶν G3588 [of the] | oroklott | a | a | K1 névelők (2. szakasz 1.; prompt A) | — | a névelő (τῶν) az örökké-hez kötve; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 1Pét 5:12 | tobblet | 22 a | 21 εἰς G1519 [in] | uj | — | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | K2 | a melyben: a C az εἰς-t mindkét tokenhez (a, melyben) köti, a prompt B „mindkét szavát” szabálya szerint; az arany az εἰς-t csak a melyben-hez: új konvenciókülönbség |
| 2Pét 1:7 | hianyzo | 6 való | 6 φιλαδελφίαν, G5360 [brotherly affection,] | megszunt | c | — | — | nincs | a való most kötve (a „való”-ra nincs konvenció; a való-betoldásos Mt 1:1-es példa kikerült a promptból) |
| 2Pét 1:7 | hianyzo | 10 való | 10 φιλαδελφίᾳ G5360 [brotherly affection] | megszunt | c | — | — | nincs | mint fent |
| 1Ján 1:10 | hianyzo | 13 ígéje | 12 αὐτοῦ G0846 [of Him] | oroklott | a | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | — | az ő ígéje: az αὐτοῦ csak az ő-höz; a konvenció a prompt_v2 ellenére sem érvényesült (az F3-nál is ez az eltérés volt) |
| 1Ján 1:10 | tobblet | 2 azt | 3 ὅτι G3754 [that] | uj | — | c | — | nincs | azt mondjuk, hogy: az azt (korrelatív) a C-nél a ὅτι-hoz kötve; az arany betoldas [az arany döntése is vitatható; a jegyzetben nem szerepel] |

