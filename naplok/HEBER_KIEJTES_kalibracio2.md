# Gépi héber kiejtés — 2. kalibráló minta, független (N-F131w, DT430 után)

*Kalibrálás, nem döntés: adat (`adat/`) nem változott, szabály nem módosult, lap nem generálódott. A felhasználó alakonként kiválasztja az elfogadható változato(ka)t és a preferáltat (⛔).*

- **Proveniencia:** `scope=adat/elofordulasok.tsv (ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001; héber Strongok) + konkordancia/TAHOT_kivonat.tsv | forras=naplok/HEBER_KIEJTES_kalibracio.py (seed=20261107) | ts=2026-10-30`; a javasolt és az alternatív változatok: `manual` (a session nyelvtani ítélete, `naplok/HEBER_KIEJTES_kalibracio2_javaslat.tsv`).
- **Minta:** 50 alak; a 8 lexikonlap motívumainak héber verseiből; 2567 szó, 1410 egyedi pontozott alak; a TAHOT-sorokból teljes szóvá összerakva (előtag + tő + toldalék); a motívum Strongján álló szavak előre, a többi a versek többi szavából. Kategóriánként kvóta, seed 20261107. Az 1. minta 50 alakja kizárva (nincs átfedés); a gépi változat a DT430 szabályaival készült; a „vegyes” kategória nehéz jegy nélküli szavakból az átlagos pontossághoz.
- **Változatok:** alakonként három különböző kiejtés, kevert sorrendben (A/B/C, seed 20261108). A forrásuk (gépi / javaslat / alternatíva) a `naplok/HEBER_KIEJTES_kalibracio2_kulcs.json`-ban áll; az az oldalra nem kerül. Géppel olvasható változat: `naplok/HEBER_KIEJTES_kalibracio2.json`.
- **Válasz a chatben:** sorszám + betű, pl. „1A 2C 3B …”; több elfogadható változat is megadható (pl. „3BA”: az első betű, B a preferált, A is elfogadható). A kiértékelés két mértéke: (a) hibás, ha a gépi változat nem elfogadható; (b) konvenció-eltérés, ha elfogadható, de nem a preferált (`python naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --chat "1A 2C 3BA …"`).

## Összesítés a session javaslatához mérve (a felhasználói választás előtt)

A „helyes” itt azt jelenti: a gépi alak (DT430) megegyezik a javasolt alakkal. A javaslat a DT430 konvencióit követi (ס/שׂ = sz, ח = ch, kámec á a kivételekkel, R3, R5, Jahve, jerúsálajim).

| kategória | n | helyes: DT430 | bizonytalan |
|---|---|---|---|
| kámec kátán (gyanú) | 6 | 5 | 2 |
| nem szókezdő sevá | 6 | 6 | 4 |
| furtív patah | 5 | 5 | 1 |
| dáges forte | 5 | 5 | 0 |
| ketiv/qere | 0 | 0 | 0 |
| makkef | 5 | 5 | 0 |
| szókezdő begadkefat dáges nélkül | 5 | 5 | 3 |
| ס és שׂ (sz vagy s) | 5 | 5 | 0 |
| vegyes (nem nehéz) | 13 | 13 | 0 |
| **összesen** | 50 | **49** | 10 |

## A minta

| # | kategória | igehely | Strong | lemma | héber alak | A | B | C | megjegyzés |
|---|---|---|---|---|---|---|---|---|---|
| 1 | kámec kátán (gyanú) | 1Móz 8:2 | H5534 | סָכַר | וַיִּסָּכְרוּ | vajjisszácherú | vajjiszácherú | vajjisszochrú |  |
| 2 | kámec kátán (gyanú) | Ez 28:16 | H7404 | רְכֻלָּה | רְכֻלָּתְךָ | rechulátechá | rechullátechá | rechullátchá | kámec után a sevá kiejtett (rəḵullāṯəḵā); a szövegben nincs meteg |
| 3 | kámec kátán (gyanú) | 1Móz 6:13 | H4390 | מָלֵא | מָלְאָה | molá | máleá | málá |  |
| 4 | kámec kátán (gyanú) | 5Móz 2:20 | H3427 | יָשַׁב | יָשְׁבוּ | jásevú | jásvú | josvú |  |
| 5 | kámec kátán (gyanú) | Zsolt 36:7 | H6666 | צְדָקָה | צִדְקָתְךָ | cidkatechá | cidkátchá | cidkátechá |  |
| 6 | kámec kátán (gyanú) | 1Kir 18:26 | H6672 | צֹ֫הַר | הַצָּהֳרַיִם | haccohorajim | haccáhorajim | hacáhorajim | hátef-kámec előtt a tibériási olvasat o (haccohorajim); a DT430 R2 szerint á |
| 7 | nem szókezdő sevá | Jóel 2:32 | H7121 | קָרָא | יִקְרָא | jikra | jikerá | jikrá |  |
| 8 | nem szókezdő sevá | Jób 14:13 | H7585 | שְׁאוֹל | בִּשְׁאוֹל | biseól | biseol | bisól | a DT430 R3 szerint kiejtett sevá (torokhang előtt); a tibériási olvasatban néma |
| 9 | nem szókezdő sevá | Zsolt 16:10 | H7585 | שְׁאוֹל | לִשְׁאוֹל | liseol | liseól | lisól | a DT430 R3 szerint kiejtett sevá (torokhang előtt); a tibériási olvasatban néma |
| 10 | nem szókezdő sevá | 1Kir 18:24 | H7121 | קָרָא | אֶקְרָא | ekrá | ekra | ekerá |  |
| 11 | nem szókezdő sevá | 1Krón 16:8 | H7121 | קָרָא | קִרְאוּ | kireú | kirú | kireu | a DT430 R3 szerint kiejtett sevá (torokhang előtt); a tibériási olvasatban néma |
| 12 | nem szókezdő sevá | Zsolt 9:18 | H7585 | שְׁאוֹל | לִשְׁאוֹלָה | liseóla | lisólá | liseólá | a DT430 R3 szerint kiejtett sevá (torokhang előtt); a tibériási olvasatban néma |
| 13 | furtív patah | Zsolt 141:7 | H6398 | פָּלַח | פֹלֵחַ | póléach | fóléach | póleach | a DT430 R5 szerint kemény (a tő kezdőbetűje); a pontozás lágyat jelöl |
| 14 | furtív patah | 2Móz 15:8 | H7307 | רוּחַ | וּבְרוּחַ | úvrúach | úberúach | úverúach |  |
| 15 | furtív patah | 1Móz 6:17 | H7307 | רוּחַ | רוּחַ | rúach | ruach | rúcha |  |
| 16 | furtív patah | Zsolt 141:7 | H1234 | בָּקַע | וּבֹקֵעַ | úbókéa | úvókéa | úvókea |  |
| 17 | furtív patah | Ézs 7:11 | H1361 | גָּבַהּ | הַגְבֵּהַּ | hagebéah | hagbéa | hagbéah |  |
| 18 | dáges forte | 1Móz 6:4 | H5303 | נְפִלִים | הַנְּפִלִים | hannefilím | hanefilím | hannefílím |  |
| 19 | dáges forte | 1Kir 18:26 | H7121 | קָרָא | וַיִּקְרְאוּ | vajikreú | vajjikreú | vajjikrú |  |
| 20 | dáges forte | 1Móz 3:16 | H6093 | עִצָּבוֹן | עִצְּבוֹנֵךְ | iccevónéch | iccevónech | icevónéch |  |
| 21 | dáges forte | 1Móz 5:29 | H6093 | עִצָּבוֹן | וּמֵעִצְּבוֹן | úméiccevón | uméiccevón | úméicevón |  |
| 22 | dáges forte | Zsolt 71:20 | H8415 | תְּהוֹם | וּמִתְּהֹמוֹת | umittehómót | úmitehómót | úmittehómót |  |
| 23 | makkef | 1Móz 12:8 | H1129 | בָּנָה | וַיִּבֶן | vajiven | vajjiven | vajjiben |  |
| 24 | makkef | Ézs 28:15 | H5973 | עִם | וְעִם | ve-im | veím | veim |  |
| 25 | makkef | Jób 1:6 | H1571 | גַּם | גַם | gam- | gám | gam |  |
| 26 | makkef | 1Móz 26:25 | H5650 | עֶ֫בֶד | עַבְדֵי | avedé | avdé | abdé |  |
| 27 | makkef | 1Krón 20:8 | H3027 | יָד | בְיַד | vejád | bejad | vejad |  |
| 28 | szókezdő begadkefat dáges nélkül | Ez 26:19 | H3541 | כֹּה | כֹה | kó | chó | kóh | a DT430 R5 szerint kemény (a tő kezdőbetűje); a pontozás lágyat jelöl |
| 29 | szókezdő begadkefat dáges nélkül | Sof 3:9 | H3605 | כֹּל | כֻלָּם | kulám | chullám | kullám | a DT430 R5 szerint kemény (a tő kezdőbetűje); a pontozás lágyat jelöl |
| 30 | szókezdő begadkefat dáges nélkül | Ez 31:16 | H0953 | בּוֹר | בוֹר | bor | bór | vór | a DT430 R5 szerint kemény (a tő kezdőbetűje); a pontozás lágyat jelöl |
| 31 | szókezdő begadkefat dáges nélkül | 1Móz 12:3 | H9031 | Os2m | בְךָ | bechá | vecha | vechá |  |
| 32 | szókezdő begadkefat dáges nélkül | 5Móz 32:22 | H0639 | אַף | בְאַפִּי | veappí | beappí | veapí |  |
| 33 | ס és שׂ (sz vagy s) | 1Móz 42:38 | H0611 | אָסוֹן | אָסוֹן | ászon | ásón | ászón |  |
| 34 | ס és שׂ (sz vagy s) | Ézs 28:18 | H4823 | מִרְמָס | לְמִרְמָס | lemirmász | lemiremász | lemirmás |  |
| 35 | ס és שׂ (sz vagy s) | Zak 6:13 | H5375 | נָשָׂא | יִשָּׂא | jissá | jisszá | jiszá |  |
| 36 | ס és שׂ (sz vagy s) | Jer 17:5 | H5493 | סוּר | יָסוּר | jászúr | jásúr | jaszúr |  |
| 37 | ס és שׂ (sz vagy s) | 1Móz 4:12 | H3254 | יָסַף | תֹסֵף | tósef | tószéf | tószef |  |
| 38 | vegyes (nem nehéz) | 1Kir 2:6 | H7585 | שְׁאוֹל | שְׁאֹל | seól | seol | sól |  |
| 39 | vegyes (nem nehéz) | 1Móz 42:38 | H7585 | שְׁאוֹל | שְׁאוֹלָה | seóla | seolá | seólá |  |
| 40 | vegyes (nem nehéz) | 1Móz 6:5 | H7451 | רָעָה | רָעַת | raat | ráat | ráát |  |
| 41 | vegyes (nem nehéz) | Jer 10:25 | H7121 | קָרָא | קָרָאוּ | karaú | kárú | káráú |  |
| 42 | vegyes (nem nehéz) | 1Krón 11:15 | H7497 | רְפָאִים | רְפָאִים | refáím | rafáím | refaím |  |
| 43 | vegyes (nem nehéz) | 1Móz 4:26 | H8034 | שֵׁם | שְׁמוֹ | semo | semó | smó |  |
| 44 | vegyes (nem nehéz) | Zsolt 116:13 | H8034 | שֵׁם | וּבְשֵׁם | úbesém | úvesém | uvsém |  |
| 45 | vegyes (nem nehéz) | 1Krón 20:6 | H7497 | רָפָה | לְהָרָפָא | leharáfá | leháráfa | leháráfá |  |
| 46 | vegyes (nem nehéz) | Jób 1:6 | H1121 | בֵּן | בְּנֵי | bené | bné | vené |  |
| 47 | vegyes (nem nehéz) | 2Sám 21:16 | H7497 | רָפָה | הָרָפָה | háráfá | hárafá | háráfa |  |
| 48 | vegyes (nem nehéz) | Péld 8:24 | H8415 | תְּהוֹם | תְּהֹמוֹת | tehómót | tehomot | thómót |  |
| 49 | vegyes (nem nehéz) | 1Móz 6:17 | H7843 | שָׁחַת | לְשַׁחֵת | lesahét | lessachét | lesachét |  |
| 50 | vegyes (nem nehéz) | Ézs 7:11 | H7585 | שְׁאוֹל | שְׁאָלָה | sálá | seálá | seála |  |
