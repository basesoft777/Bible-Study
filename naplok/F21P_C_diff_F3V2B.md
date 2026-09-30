# F21P_C_diff_F3V2B.md — a C második futása (F3V2B) az F3V2-vel összevetve; az A+B+C gépi diffje

<!-- GENERÁLT: eszkozok/karoli_strong/c_diff_f3v2b.py | scope=F3V2 és F3V2B a 60 aranyversen (arany v2); A+B+C (F1V2, F2V2, F4V2, G4) | forras=f21p/valaszok/{F3V2,F3V2B,F1V2,F2V2,F4V2}.jsonl, f21p/arany_opus_v2.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv | ts=2026-09-30T14:30:59+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

A közös eltérések (mindkét futásban ugyanaz a link hiányzik vagy többlet) az F3V2 kézi besorolását öröklik; az F3V2B új eltéréseit (csak_f3v2b) az Opus sorolta be. **Az osztályok az Opus besorolása, nem mérés.** Azonos prompt mellett a két futás eltérése a futásközi ingadozás becslése.

## 1. Eltérések rétegenként

| réteg | F3V2 eltérés | F3V2B eltérés | közös | csak F3V2B | csak F3V2 |
|---|---|---|---|---|---|
| R1 | 37 | 33 | 17 | 16 | 20 |
| R2 | 7 | 8 | 2 | 6 | 5 |
| R3 | 23 | 20 | 12 | 8 | 11 |
| R4 | 34 | 42 | 26 | 16 | 8 |
| Összes | 101 | 103 | 57 | 46 | 44 |

## 2. A (c) esetek (az Opus besorolása, nem mérés)

| réteg | F3V2 (c) | F3V2B (c) | azonos (c) | új (c) az F3V2B-nél | megszűnt (c) (az F3V2-nél volt) |
|---|---|---|---|---|---|
| R1 | 13 | 6 | 4 | 2 | 9 |
| R2 | 1 | 0 | 0 | 0 | 1 |
| R3 | 8 | 9 | 5 | 4 | 3 |
| R4 | 17 | 21 | 11 | 10 | 6 |
| Összes | 39 | 36 | 20 | 16 | 19 |

## 3. Az F3V2B új eltérései (kézi besorolás)

| vers | irány | magyar szó | eredeti szó | osztály | konvenció / jegyzetpont | indok |
|---|---|---|---|---|---|---|
| 2Móz 20:25 | tobblet | 13 a | 13 כִּ֧י H3588 [for] | b | 6. szakasz táblázat: 2Móz 20:25 | a mint -> כִּי: a jegyzet alternatívája (a az a tokenen) |
| 2Móz 20:25 | tobblet | 14 mint | 13 כִּ֧י H3588 [for] | b | 6. szakasz táblázat: 2Móz 20:25 | a mint -> כִּי: a jegyzet alternatívája |
| 2Móz 21:26 | tobblet | 10 úgy | 1 וְ H9002 [and] | b | 6. szakasz táblázat: 2Móz 21:26 | az úgy a kezdő ve--hez kötve; nem a jegyzet alternatívája (az: Ha -> 1, 2) |
| 2Móz 25:40 | hianyzo | 3 arra | 7 ם H9028 [their] | b | 6. szakasz táblázat: 2Móz 25:40 | a -ām a formára-n (mint az F3-nál); nem a jegyzet alternatívája |
| 2Móz 25:40 | tobblet | 5 formára | 7 ם H9028 [their] | b | 6. szakasz táblázat: 2Móz 25:40 | mint fent |
| 2Móz 26:13 | tobblet | 10 a | 12 עֹדֵ֔ף H5736 [surplus] | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | a mi: az a is az igenévhez kötve (a K2 opciója, „mindkét szavát”) |
| Péld 28:17 | tobblet | 6 vér | 3 בְּ H9003 [by] | b | 6. szakasz táblázat: Péld 28:17 | vér -> 3, 4: a jegyzet alternatívája |
| Péld 30:17 | hianyzo | 6 vagy | 5 וְ H9002 [so] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a ve- (5) a vagy helyett az igéhez kötve (a prompt I szabálya ellenére) |
| Péld 30:17 | hianyzo | 13 kivágják | 11 הָ H9034 [it] | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | a tárgyi rag az igén nincs kötve (az F3-mal azonos besorolás; a tárgyrag nyitott kérdés, DT20 a) |
| Péld 30:17 | hianyzo | 17 vagy | 14 וְֽ H9002 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a ve- (14) a vagy helyett az igéhez kötve |
| Péld 30:17 | hianyzo | 18 megeszik | 16 הָ H9034 [it] | a | K4 birtokos és névmási ragok (2. szakasz 4.; prompt D) | mint a 13. szónál |
| Péld 30:17 | tobblet | 7 megútálja | 5 וְ H9002 [so] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a ve- az igén (l. fent) |
| Péld 30:17 | tobblet | 18 megeszik | 14 וְֽ H9002 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a ve- az igén (l. fent) |
| Péld 31:5 | hianyzo | 11 ne | 1 פֶּן H6435 [lest] | c | — | a második ne a פֶּן-é; a C a ve--hez (6) köti |
| Péld 31:5 | tobblet | 6 felejtkezzék | 3 וְ H9002 [and] | b | 6. szakasz táblázat: Péld 31:5 | a ve- (3) az igén (mint az F3-nál); nem a jegyzet alternatívája |
| Péld 31:5 | tobblet | 11 ne | 6 וִֽ֝ H9002 [and] | c | — | a ne nem a ve- (6) |
| Zsolt 18:1 | tobblet | 12 ének | 14 הַ H9009 [the] | a | K1 névelők (2. szakasz 1.; prompt A) | a névelő (הַ) az ének-en |
| Zsolt 18:1 | tobblet | 13 szavait | 12 אֶת H0853 [<obj.>] | a | K3 tárgyjelölő névmási raggal (2. szakasz 3.; prompt C) | az 'et a szavait-hoz kötve; a K3 szerint forditatlan |
| Zsolt 18:1 | tobblet | 23 őt | 22 אוֹת֥ H0853 [<obj.>] | a | K3 tárgyjelölő névmási raggal (2. szakasz 3.; prompt C) | őt: az 'et is a névmáshoz kötve |
| Zsolt 18:3 | tobblet | 6 váram | 4 וּ H9002 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a וּ (4) a magyarban kötőszó nélkül; a C a váram-hoz köti |
| Zsolt 18:3 | tobblet | 21 idvességem | 19 וְ H9002 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | a וְ (19) kötőszó nélkül; a C az idvességem-hez köti |
| Zsolt 22:32 | hianyzo | 9 utánok | 8 נ֝וֹלָ֗ד H3205 [about to be born] | b | 6. szakasz táblázat: Zsolt 22:32 | az utánok betoldas-ként: a jegyzet alternatívája (utánok való betoldas) |
| Jer 51:3 | tobblet | 2 kézívesre | 2 יִדְרֹ֤ךְ H1869 [he bend] | b | 3. szakasz (Jer 51:3, Ketiv) — a 6. táblázatba nem kerül be | a kézívesre a Ketiv kettőzött igéjével (F21.12: b) |
| Jer 51:3 | tobblet | 2 kézívesre | 3 הַ H9009 [the] | a | K1 névelők (2. szakasz 1.; prompt A) | a névelő (הַ) a kézívesre-n |
| Jer 51:3 | tobblet | 9 a | 8 אֶל H0408 [may not] | c | — | az a (a ki) nem az אֶל (az F3 ki -> 8 (c) esetének párja) |
| Ez 16:57 | tobblet | 6 miképen | 7 עֵ֚ת H6256 [[the] time of] | c | — | a miképen nem az עֵת („idő”) |
| Ez 33:31 | tobblet | 15 mint | 5 כִּ H9004 [like] | b | 6. szakasz táblázat: Ez 33:31 | a mint -> כְּ (mint az F3-nál); védhető |
| Ez 33:31 | tobblet | 32 pedig | 20 וְ H9002 [and] | c | — | a pedig nem a 20. ve- (az a de-é) |
| Ez 41:2 | tobblet | 22 is | 20 וַ H9001 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | az is a ve--hez (20) is kötve; az arany a ve--t a megméré-hez köti (az I szabály az is-t is felsorolja) |
| Ez 46:12 | tobblet | 39 azután | 40 יָצָ֛א H3318 [he will go out] | c | — | az azután Károli betoldása; a „kimegy” igéhez kötve (az F3 (c) esete) |
| Mt 6:31 | hianyzo | 5 ne | 1 μὴ G3361 [Not] | c | — | a második ne a μή-é; a C a λέγοντες-hez köti [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Mt 6:31 | tobblet | 5 ne | 4 λέγοντες· G3004 [saying;] | c | — | a ne nem a λέγοντες |
| Mt 11:18 | tobblet | 4 a | 4 μήτε G3383 [neither] | c | — | az a (a ki) nem a μήτε (az F3 (c) esete) |
| Mt 11:18 | tobblet | 5 ki | 4 μήτε G3383 [neither] | c | — | a ki nem a μήτε (az F3 (c) esete) |
| Mt 21:4 | hianyzo | 3 azért | 5 ἵνα G2443 [that] | c | — | azért ... hogy: az azért a ἵνα-é [az arany döntése is vitatható; a jegyzetben nem szerepel] |
| Mt 21:4 | tobblet | 3 azért | 4 γέγονεν G1096 [has come to pass] | c | — | az azért nem a γέγονεν |
| Mt 21:4 | tobblet | 9 mondása | 7 τὸ G3588 [that] | a | K1 névelők (2. szakasz 1.; prompt A) | a névelő (τό) a mondása-n |
| Mt 21:4 | tobblet | 13 szólott | 9 διὰ G1223 [through] | c | — | a διά („által”) nem a szólott |
| Mk 3:18 | hianyzo | 6 és | 7 καὶ G2532 [and] | a | K9 le nem fordított ve-/kai (2. szakasz 9.; prompt I) | az és a καί helyén áll, a C betoldas-nak veszi (az I szabály ellenére) |
| Jak 1:18 | hianyzo | 2 ő | 1 βουληθεὶς G1014 [Having willed [it]] | c | — | az ő akarata -> βουληθείς (6. táblázat); a C az ő-t az αὐτοῦ-hoz (13) köti, ami az ő teremtményeinek-é: nem védhető |
| Jak 1:18 | tobblet | 2 ő | 13 αὐτοῦ G0846 [of His] | c | — | mint fent |
| Jak 3:4 | tobblet | 18 a | 17 ἂν G0302 [ever] | a | K2 kettéírt Károli-kötőszók / vonatkozó (2. szakasz 2.; prompt B) | a hová: az a is az ἄν-hez kötve („mindkét szavát”) |
| Jak 3:8 | tobblet | 10 meg | 6 δύναται G1410 [is able] | a | K5 különírt igekötő (2. szakasz 5.; prompt E) | az igekötő (meg) az ige mindkét eredetijéhez (δαμάσαι, δύναται) kötve |
| 1Pét 4:2 | tobblet | 1 Hogy | 2 τὸ G3588 [<the>] | a | K1 névelők (2. szakasz 1.; prompt A) | a névelős főnévi igenév névelője (τό) a Hogy-on |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 27 ἐστιν G1510 [be] | c | — | az ἐστιν nem a dícsőíttessék |
| 1Pét 5:12 | tobblet | 9 atyátokfia | 3 ὑμῖν G4771 [to you] | b | 6. szakasz táblázat: 1Pét 5:12 | ὑμῖν az atyátokfia -tok ragjához (mint az F3-nál); nem a jegyzet alternatívája |

## 4. Az F3V2 eltérései, amelyek az F3V2B-nél nincsenek (osztály az F3V2 besorolásából)

| vers | irány | magyar szó | eredeti szó | F3V2-osztály |
|---|---|---|---|---|
| 2Móz 20:25 | tobblet | 13 a | 18 הָ H9034 [it] | c |
| 2Móz 20:25 | tobblet | 14 mint | 18 הָ H9034 [it] | c |
| 2Móz 21:6 | hianyzo | 6 ura | 5 ו֙ H9023 [his] | a |
| 2Móz 21:6 | hianyzo | 20 ura | 22 ו H9023 [his] | a |
| 2Móz 21:6 | hianyzo | 25 fülét | 25 וֹ֙ H9023 [his] | a |
| 2Móz 21:26 | hianyzo | 5 szolgájának | 8 וֹ H9023 [his] | a |
| 2Móz 21:26 | hianyzo | 8 szolgálójának | 13 וֹ H9023 [his] | c |
| 2Móz 21:26 | hianyzo | 20 szeméért | 23 וֹ H9023 [his] | a |
| 2Móz 21:26 | tobblet | 1 Ha | 1 וְ H9002 [and] | b |
| 2Móz 21:26 | tobblet | 9 szemét | 13 וֹ H9023 [his] | c |
| 2Móz 21:26 | tobblet | 10 úgy | 14 וְ H9001 [and] | b |
| 2Móz 25:8 | hianyzo | 8 közöttök | 10 ם H9028 [them] | a |
| 2Móz 26:13 | tobblet | 9 abból | 12 עֹדֵ֔ף H5736 [surplus] | c |
| 2Móz 29:4 | hianyzo | 6 fiait | 7 ו֙ H9023 [his] | a |
| Péld 25:24 | hianyzo | 4 tetőnek | 5 גָּ֑ג H1406 [a roof] | c |
| Péld 25:24 | hianyzo | 5 ormán | 4 פִּנַּת H6438 [[the] corner of] | c |
| Péld 25:24 | tobblet | 4 tetőnek | 4 פִּנַּת H6438 [[the] corner of] | c |
| Péld 25:24 | tobblet | 5 ormán | 5 גָּ֑ג H1406 [a roof] | c |
| Péld 28:17 | hianyzo | 11 senki | 9 אַל H0408 [may not] | b |
| Péld 28:17 | tobblet | 7 terhel | 3 בְּ H9003 [by] | b |
| Zsolt 16:11 | tobblet | 1 Te | 1 תּֽוֹדִיעֵ H3045 [you will make known to] | a |
| Zsolt 18:1 | tobblet | 14 azon | 19 י֤וֹם H3117 [[the] day] | b |
| Zsolt 18:3 | tobblet | 7 és | 4 וּ H9002 [and] | a |
| Zsolt 22:32 | tobblet | 8 ő | 8 נ֝וֹלָ֗ד H3205 [about to be born] | b |
| Zsolt 22:32 | tobblet | 13 ezt | 10 עָשָֽׂה H6213 [he has acted] | c |
| Jer 46:21 | hianyzo | 27 megfenyíttetésök | 27 ם H9028 [their] | a |
| Jer 51:3 | tobblet | 3 kézíves | 3 הַ H9009 [the] | a |
| Ez 16:57 | tobblet | 7 te | 7 עֵ֚ת H6256 [[the] time of] | c |
| Ez 22:25 | hianyzo | 4 prófétái | 3 הָ֙ H9024 [its] | a |
| Ez 22:25 | hianyzo | 6 közepette | 6 הּ H9024 [it] | a |
| Ez 33:31 | hianyzo | 18 népem | 14 י H9020 [my] | a |
| Ez 33:31 | tobblet | 15 mint | 14 י H9020 [my] | c |
| Ez 33:31 | tobblet | 32 pedig | 30 הֵ֣מָּה H1992 [they] | c |
| Ez 33:31 | tobblet | 33 nyereség | 34 ם H9028 [their] | b |
| Ez 46:12 | tobblet | 25 ő | 24 עָשָׂ֤ה H6213 [he will offer] | a |
| Ez 46:12 | tobblet | 39 azután | 39 וְ H9001 [and] | a |
| Mt 27:18 | tobblet | 2 jól | 1 ᾔδει G1492 [He knew] | c |
| Mt 27:18 | tobblet | 4 vala | 1 ᾔδει G1492 [He knew] | a |
| Mk 2:23 | tobblet | 3 hogy | 2 ἐγένετο G1096 [it came to pass] | c |
| Jak 3:1 | tobblet | 7 azt | 8 ὅτι G3754 [that] | c |
| Jak 3:4 | hianyzo | 19 hová | 17 ἂν G0302 [ever] | c |
| Jak 3:4 | tobblet | 22 szándéka | 18 ἡ G3588 [the] | a |
| 1Pét 4:11 | tobblet | 22 dícsőíttessék | 22 θεὸς G2316 [God] | c |
| 1Ján 1:10 | tobblet | 2 azt | 3 ὅτι G3754 [that] | c |

## 5. Az A+B+C (G4) gépi diffje az arany v2-höz (kézi besorolás nélkül)

| réteg | hiányzó | többlet (magas) | többlet (kozepes) | többlet (alacsony) | aranyvers |
|---|---|---|---|---|---|
| R1 | 34 | 4 | 5 | 10 | 20 |
| R2 | 2 | 7 | 4 | 1 | 10 |
| R3 | 10 | 6 | 3 | 12 | 10 |
| R4 | 16 | 3 | 8 | 12 | 20 |
| Összes | 62 | 20 | 20 | 35 | 60 |

