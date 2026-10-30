# Gépi héber kiejtés — kalibráló minta (N-F131w)

*Kalibrálás, nem döntés: adat (`adat/`) nem változott, szabály nem módosult, lap nem generálódott. A felhasználó alakonként kiválasztja az elfogadható változato(ka)t és a preferáltat (⛔).*

- **Proveniencia:** `scope=adat/elofordulasok.tsv (ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001; héber Strongok) + konkordancia/TAHOT_kivonat.tsv | forras=naplok/HEBER_KIEJTES_kalibracio.py (seed=20261030) | ts=2026-10-30`; a javasolt és az alternatív változatok: `manual` (a session nyelvtani ítélete, `naplok/HEBER_KIEJTES_kalibracio_javaslat.tsv`).
- **Minta:** 50 alak; a 8 lexikonlap motívumainak héber verseiből; 2567 szó, 1460 egyedi pontozott alak; a TAHOT-sorokból teljes szóvá összerakva (előtag + tő + toldalék); a motívum Strongján álló szavak előre, a többi a versek többi szavából. Kategóriánként kvóta, seed 20261030.
- **Változatok:** alakonként három különböző kiejtés, kevert sorrendben (A/B/C, seed 20261031). A forrásuk (gépi / javaslat / alternatíva) a `naplok/HEBER_KIEJTES_kalibracio_kulcs.json`-ban áll; az az oldalra nem kerül. Géppel olvasható változat: `naplok/HEBER_KIEJTES_kalibracio.json`.
- **Válasz a chatben:** sorszám + betű, pl. „1A 2C 3B …”; több elfogadható változat is megadható (pl. „3BA”: az első betű, B a preferált, A is elfogadható). A kiértékelés két mértéke: (a) hibás, ha a gépi változat nem elfogadható; (b) konvenció-eltérés, ha elfogadható, de nem a preferált (`python naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --chat "1A 2C 3BA …"`).

## Összesítés a session javaslatához mérve (a felhasználói választás előtt)

A „helyes” itt azt jelenti: a gépi alak megegyezik a javasolt alakkal. A javaslat konvenciója: ס és שׂ = sz, a szókezdő begadkefatról a pontozás dönt. Az sz/s és a kemény/lágy kérdés miatt a gépi alakot négy konvenció-kombinációval is összevetettem.

| kategória | n | helyes: mai szabály (ס = s, שׂ = sz; szókezdő begadkefat kemény) | helyes: ס és שׂ = sz | helyes: begadkefat a pontozás szerint | helyes: mindkettő | bizonytalan |
|---|---|---|---|---|---|---|
| kámec kátán (gyanú) | 7 | 3 | 3 | 3 | 3 | 2 |
| nem szókezdő sevá | 6 | 4 | 4 | 6 | 6 | 0 |
| furtív patah | 6 | 6 | 6 | 6 | 6 | 0 |
| dáges forte | 6 | 6 | 6 | 6 | 6 | 0 |
| ketiv/qere | 5 | 3 | 3 | 3 | 3 | 3 |
| makkef | 6 | 2 | 3 | 4 | 5 | 2 |
| szókezdő begadkefat dáges nélkül | 7 | 0 | 0 | 7 | 7 | 0 |
| ס és שׂ (sz vagy s) | 7 | 0 | 6 | 0 | 6 | 4 |
| **összesen** | 50 | **24** | **31** | **35** | **42** | 11 |

## A minta

| # | kategória | igehely | Strong | lemma | héber alak | A | B | C | megjegyzés |
|---|---|---|---|---|---|---|---|---|---|
| 1 | kámec kátán (gyanú) | 1Krón 20:4 | H7497 | רְפָאִים | הָרְפָאִים | hárfáím | horfáím | hárefáím |  |
| 2 | kámec kátán (gyanú) | Józs 17:15 | H7497 | רְפָאִים | וְהָרְפָאִים | vehárefáím | vehárfáím | vehorfáím |  |
| 3 | kámec kátán (gyanú) | Jón 3:8 | H2394 | חׇזְקָה | בְּחָזְקָה | becházeká | becházká | bechozká |  |
| 4 | kámec kátán (gyanú) | 1Móz 1:2 | H1961 | הָיָה | הָיְתָה | hájetá | hájtá | hojtá |  |
| 5 | kámec kátán (gyanú) | Ézs 17:5 | H7641 | שִׁבֹּ֫לֶת | שִׁבֳּלִים | sibolím | sibbolím | sibbólím |  |
| 6 | kámec kátán (gyanú) | 1Móz 12:8 | H0168 | אֹ֫הֶל | אָהְָלוֹ | oholó | áháló | áholó | a hé alatt sevá és kámec együtt áll (a hátef-kámec szokatlan kódolása); az ohŏlô olvasat a valószínű |
| 7 | kámec kátán (gyanú) | Ézs 28:15 | H5641 | סָתַר | נִסְתָּרְנוּ | nisztárnú | nisztárenú | nistárenú | pauzális alak: a hangsúlyos zárt szótag után a sevát némának tartom, a STEP kiejtettnek írja |
| 8 | nem szókezdő sevá | Ámós 9:2 | H7585 | שְׁאוֹל | בִשְׁאוֹל | viseól | bisól | visól |  |
| 9 | nem szókezdő sevá | Ézs 64:6 | H8034 | שֵׁם | בְשִׁמְךָ | vesimchá | vesimechá | besimchá |  |
| 10 | nem szókezdő sevá | 1Kir 18:25 | H7121 | קָרָא | וְקִרְאוּ | vekirú | vekireú | vekiru |  |
| 11 | nem szókezdő sevá | 1Móz 6:12 | H7843 | שָׁחַת | נִשְׁחָתָה | nishátá | nisechátá | nischátá |  |
| 12 | nem szókezdő sevá | Zsolt 78:15 | H8415 | תְּהוֹם | כִּתְהֹמוֹת | kithómót | kitehómót | kit-hómót |  |
| 13 | nem szókezdő sevá | 4Móz 13:34 | H5303 | נְפִלִים | הַנְּפִילִים | hanefílím | hannefílím | hannefilím |  |
| 14 | furtív patah | Józs 17:15 | H3091 | יְהוֹשׁוּעַ | יְהוֹשֻׁעַ | jehósúa | jehósuá | jehósua |  |
| 15 | furtív patah | 1Kir 18:26 | H4196 | מִזְבֵּחַ | הַמִּזְבֵּחַ | hammizbécha | hammizbéach | hamizbéach |  |
| 16 | furtív patah | 1Móz 3:18 | H6779 | צָמַח | תַּצְמִיחַ | tacmíach | tacmícha | tacemíach |  |
| 17 | furtív patah | 1Móz 12:8 | H4196 | מִזְבֵּחַ | מִזְבֵּחַ | mizbéach | mizebéach | mizbécha |  |
| 18 | furtív patah | Péld 21:16 | H5117 | נוּחַ | יָנוּחַ | jánúach | janúach | jánúcha |  |
| 19 | furtív patah | 1Móz 8:21 | H7381 | רֵיחַ | רֵיחַ | réach | réjach | récha |  |
| 20 | dáges forte | 5Móz 33:13 | H8415 | תְּהוֹם | וּמִתְּהוֹם | úmittehóm | umittehóm | úmitehóm |  |
| 21 | dáges forte | 1Móz 2:7 | H2416 | חַיִּים | חַיִּים | hajjím | chajjím | chajím |  |
| 22 | dáges forte | 1Móz 12:8 | H7121 | קָרָא | וַיִּקְרָא | vajjikrá | vajikrá | vajjikerá |  |
| 23 | dáges forte | 1Móz 2:7 | H2416 | חַי | חַיָּה | chajá | hajjá | chajjá |  |
| 24 | dáges forte | Jób 11:8 | H7585 | שְׁאוֹל | מִשְּׁאוֹל | missól | misseól | miseól |  |
| 25 | dáges forte | 1Móz 4:7 | H2403 | חַטָּאת | חַטָּאת | chattát | hattát | chatát |  |
| 26 | ketiv/qere | Jóel 2:32 | H3389 | יְרוּשָׁלִַ֫ם, יְרוּשְׁלֵם | וּבִירוּשָׁלִַם | úvírúsálajim | úvírúsálém | úvírúsálim | ketiv/qere: a mássalhangzós szöveg (ketiv) „Jerúsálém”-et, a pontozás (qere) „Jerúsálajim”-ot ad |
| 27 | ketiv/qere | Józs 15:8 | H3389 | יְרוּשָׁלִַ֫ם, יְרוּשְׁלֵם | יְרוּשָׁלִָם | jerúsálajim | jerúsálim | jerúsálém | ketiv/qere: l. az előző sort |
| 28 | ketiv/qere | Ez 26:19 | H3069 | יְהֹוִה | יְהוִה | Elóhím | Jahve | JHVH | az „Adonáj JHVH” kapcsolatban a pontozás (qere) Elóhímot olvastat; a lapon a JHVH-konvenció áll |
| 29 | ketiv/qere | 1Móz 3:14 | H3068 | יהוה | יְהֹוָה | Adonáj | JHVH | Jahve |  |
| 30 | ketiv/qere | 1Kir 18:24 | H3068 | יהוה | יְהוָה | Adonáj | Jahve | JHVH |  |
| 31 | makkef | 1Móz 6:2 | H1121 | בֵּן | בְנֵי | vené | bené | bné |  |
| 32 | makkef | 1Kir 18:24 | H8034 | שֵׁם | בְשֵׁם | vesém | vesem | besém |  |
| 33 | makkef | Hab 2:17 | H2555 | חָמָס | וַחֲמַס | vahamasz | vachamasz | vachamas | a H2555 lemmája kézi kivétel („hámás”, D36: ח → h); kérdés, hogy ez a ragozott alakokra is vonatkozik-e |
| 34 | makkef | Ézs 51:10 | H0859 | אַתְּ | אַתְּ | atte | att | at | a szóvégi תְּ dágessel: a hagyományos olvasat „at”, a régebbi kiejtés „atte” |
| 35 | makkef | 5Móz 2:11 | H0637 | אַף | אַף | áf | ap | af |  |
| 36 | makkef | Jer 51:46 | H6435 | פֶּן־ | וּפֶן | úpen | úfen | ufen |  |
| 37 | szókezdő begadkefat dáges nélkül | Én 8:6 | H7585 | שְׁאוֹל | כִשְׁאוֹל | chiseól | chisól | kisól |  |
| 38 | szókezdő begadkefat dáges nélkül | Zak 6:13 | H3548 | כֹּהֵן | כֹהֵן | kohén | kóhén | chóhén |  |
| 39 | szókezdő begadkefat dáges nélkül | Zak 13:9 | H8034 | שֵׁם | בִשְׁמִי | vismí | bismí | visemí |  |
| 40 | szókezdő begadkefat dáges nélkül | 1Krón 16:8 | H8034 | שֵׁם | בִשְׁמוֹ | visemó | bismó | vismó |  |
| 41 | szókezdő begadkefat dáges nélkül | Zsolt 76:3 | H8004 | שָׁלֵם | בְשָׁלֵם | vesalém | vesálém | besálém |  |
| 42 | szókezdő begadkefat dáges nélkül | Ez 31:17 | H6738 | צֵל | בְצִלּוֹ | vecilló | veciló | becilló |  |
| 43 | szókezdő begadkefat dáges nélkül | Ézs 28:15 | H1285 | בְּרִית | בְרִית | verít | berít | brít |  |
| 44 | ס és שׂ (sz vagy s) | Jer 51:46 | H2555 | חָמָס | וְחָמָס | vechámász | vehámász | vechámás | a H2555 kézi kivétele („hámás”, D36) a ragozott alakra is vonatkozhat |
| 45 | ס és שׂ (sz vagy s) | Jón 3:8 | H2555 | חָמָס | הֶחָמָס | hehámász | hechámás | hechámász | l. a 44. sort |
| 46 | ס és שׂ (sz vagy s) | 1Móz 6:13 | H2555 | חָמָס | חָמָס | hámász | chámás | hámás | a jóváhagyott lemma-kiejtés „hámás” (D36); az sz-változat a ס-konvenciótól függ |
| 47 | ס és שׂ (sz vagy s) | Zak 6:13 | H3678 | כִּסֵּא | כִּסְאוֹ | kisó | kiszó | kiszeó |  |
| 48 | ס és שׂ (sz vagy s) | Hab 2:17 | H2555 | חָמָס | חֲמַס | chamas | chamasz | hamasz | l. a 44. sort |
| 49 | ס és שׂ (sz vagy s) | Zsolt 86:13 | H2617 | חֶ֫סֶד | חַסְדְּךָ | haszdechá | chaszdechá | chasdechá |  |
| 50 | ס és שׂ (sz vagy s) | Zak 13:9 | H3701 | כֶּ֫סֶף | הַכֶּסֶף | hakeszef | hakkeszef | hakkesef |  |
