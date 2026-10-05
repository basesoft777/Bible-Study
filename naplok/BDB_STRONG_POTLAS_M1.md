# BDB_STRONG_POTLAS M1 — párosítás (F57)

*Generálta: `python eszkozok/bdb_strong_potlas.py --m1` · scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/OSHL_lexikalis_index.tsv + konkordancia/BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py (cimszo-egyezes) | ts=2026-10-05*

## 1. Párosítási szabály (szó szerint, BRIEF §3 M1)

1. Címszó-egyezés: az OSHL-lemma és a BDB-címszó normalizált alakja egyezik; a normalizálás egységesíti a holem-waw írásváltozatokat (U+05BA -> U+05B9), eltávolítja a kantillációs jeleket (U+0591-05AF) és a meteget/rafét; a magánhangzópontok megmaradnak. Címszó: a szófaj-jelölő előtti első `<bdbheb>`; nyelv (héber/arámi) egyezik.
2. Homonímia: ha több jelölt van, az OSHL `def_en` és a BDB glosszái közti szóegyezés dönt; ha nem dönt egyértelműen, `tobb_jelolt`.
3. Kizárás: ha a BDB-szócikknek már van Strong-címkéje, vagy a Strong-számnak már van sora a táblában (vagy `H<n>` kulcsa a BDB.lexicon-ban), nem párosítható.
Gyök-hivatkozás ("√ of following", szófaj nélkül) mindig `nincs_par`.

## 2. Eredmény a címke nélküli szócikkekre

- Sorok: 846; állapotok: {'nincs_par': 843, 'egyertelmu': 3}.
- A `BDB_strong_potlas.tsv` a **címke nélküli** BDB-szócikkeket (BDB-azonosító szerint) sorolja; a Strong-oszlop a pár.

### Egyértelmű párok (mind)

| BDB | Strong | címszó | OSHL-lemma | indok |
|---|---|---|---|---|
| BDB754 | H0747 | אֲרִיסַי | אֲרִיסַי | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: son of Haman / OSHL def_en: Arisai |
| BDB2246 | H4123 | מַהֲתַלּוֺת | מַֽהֲתַלּוֹת | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: deceptions / OSHL def_en: illusions |
| BDB7372 | H4725 | מָקוֺם | מָקוֹם | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: standing-place, place; standing-place / OSHL def_en: standing-place |

### Tobb_jelolt sorok (mind)

Nincs.


### Nincs_par, mássalhangzó-egyezési tipppel (nem párosítás; kézi döntéshez)

| BDB | címszó | tipp |
|---|---|---|
| BDB1362 | בשׂם | H1313 |
| BDB4531 | מהר | H4118 |

## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora

- 529 Strong (a H0136 és a H0341 is ide tartozik), mindegyiknek a szócikke a BDB.lexicon `H<n>` kulcsa alatt **címkével** áll, tehát a 3. kizárási szabály miatt nem párosítható; a szöveg a táblában a testvér-Strong sora alatt megvan (a címszó mássalhangzós alakja a testvér-sor szövegében: 513/529 sorban megtalálható).
- Ez nem a tábla szövegének hiánya, hanem a Strong-kulcs hiánya (a DictBDB.json egy szócikkhez csak egy Strong-kulcsot ad). Lásd a ⛔ döntést (DONTESEK.md).

| Strong | BDB | testvér-Strong a táblában | címszó | címszó a testvér-sorban | OSHL def_en | TAHOT |
|---|---|---|---|---|---|---|
| H0004 | BDB9264 | H0003 |  | NEM | fruit | 3 |
| H0007 | BDB9265 | H0006 | אֲבַד | igen | perish | 7 |
| H0013 | BDB10 | H0012 | אַבְדָ֑ן | igen | destruction | 1 |
| H0021 | BDB24 | H0029 | אֲבִיָּ֫הוּ | igen | Abi | 1 |
| H0038 | BDB24 | H0029 | אֲבִיָּ֫הוּ | igen | Abijam | 5 |
| H0043 | BDB20 | H0023 | אֲבִיאָסָף | igen | Ebiasaph | 3 |
| H0059 | BDB54 | H0058,H0062 | אָבֵל | igen | Abel | 2 |
| H0063 | BDB54 | H0058,H0062 | אָבֵל | igen | Abelshittim | 2 |
| H0064 | BDB54 | H0058,H0062 | אָבֵל | igen | plain of the vineyards | 2 |
| H0065 | BDB54 | H0058,H0062 | אָבֵל | igen | Abel-meholah | 6 |
| H0066 | BDB54 | H0058,H0062 | אָבֵל | igen | Abel-maim | 2 |
| H0067 | BDB54 | H0058,H0062 | אָבֵל | igen | Abel-mizraim | 2 |
| H0069 | BDB9268 | H0068 | אֶ֫בֶן | igen | stone | 8 |
| H0072 | BDB58 | H0068 | אֶ֫בֶן | igen | Ebenezer | 6 |
| H0085 | BDB38 | H0087 | אַבְרָם | igen | Abraham | 175 |
| H0121 | BDB108 | H0120 | אָדָם | igen | Adam | 12 |
| H0128 | BDB109 | H0127 | אֲדָמָה | igen | Adamah | 1 |
| H0136 | BDB125 | H0113 | אָדוֺן | igen | lord | 440 |
| H0144 | BDB9271 | H0143 | אֲדָר | igen | Adar | 1 |
| H0169 | BDB154 | H0168 | אֹ֫הֶל | igen | Ohel | 1 |
| H0206 | BDB223 | H0205,H0204 | אָ֫וֶן | igen | Aven | 2 |
| H0236 | BDB9281 | H0235 | אֲזַל | igen | go | 7 |
| H0277 | BDB290 | H0281 | אֲחִיָּ֫הוּ | igen | Ahi | 2 |
| H0341 | BDB375 | H0340 | אָיַב | igen | be hostile to | 283 |
| H0365 | BDB216 | H0355 | אַיָּלָה | igen | hind | 0 |
| H0372 | BDB35 | H0044 | אֲבִיעֶ֫זֶר | igen | Jeezer | 1 |
| H0373 | BDB36 | H0033 | אֲבִי הָעֶזְרִי | NEM | an Iezrite | 1 |
| H0388 | BDB3847 | H0386 | אֵיתָן | igen | Ethanim | 1 |
| H0399 | BDB9297 | H0398 | אֲכַל | igen | eat | 7 |
| H0449 | BDB431 | H0419 | אֶלְדָּד | igen | Elidad | 1 |
| H0462 | BDB422 | H0454 | אֶלְיוֺעֵינַי | igen | Elienai | 1 |
| H0506 | BDB9305 | H0505 | אֲלַ֑ף | igen | 1,000 | 4 |
| H0521 | BDB9306 | H0520 | אַמָּה | igen | cubit | 4 |
| H0524 | BDB9307 | H0523 | אֻמָּה | igen | nation | 8 |
| H0527 | BDB540 | H0525 | אָמוֺן | igen | artificer | 0 |
| H0532 | BDB515 | H0526 | אָמִי | igen | Ami | 1 |
| H0540 | BDB9308 | H0539 | אֲמַן | igen | trust | 3 |
| H0547 | BDB527 | H0539 | אָמַן | igen | confirm | 1 |
| H0624 | BDB627 | H0622 | אָסַף | igen | store | 3 |
| H0638 | BDB9331 | H0637 | אַף | igen | also | 4 |
| H0706 | BDB7718 | H0702 | אַרְבַּע | igen | four | 1 |
| H0711 | BDB9336 | H0710,H0713 | אַרְגְּוָן | igen | purple | 3 |
| H0723 | BDB733 | H0220 | אֻרְיָה | igen | manger | 3 |
| H0726 | BDB118 | H0130 | אֲדֹמִי | igen | Edomite | 0 |
| H0740 | BDB736 | H0739,H0741 | אֲרִיאֵל | igen | Ariel | 6 |
| H0760 | BDB762 | H0758 | אֲרָם | igen | Aram-zobah | 2 |
| H0763 | BDB762 | H0758 | אֲרָם | igen | Aram-naharaim | 10 |
| H0778 | BDB9349 | H0772 | אֲרַק | igen | earth | 1 |
| H0792 | BDB390 | H0378 | אִישׁבּֿ֫שֶׁת | igen | Eshbaal | 2 |
| H0798 | BDB6692 | H6449 | פִּסְגָּה | NEM | Ashdoth-pisgah | 4 |
| H0799 | BDB793 | H0784 | אֵשׁ | igen | fire | 0 |
| H0808 | BDB848 | H0809 | אֲשִׁישָׁה | igen | raisin-cake | 0 |
| H0868 | BDB9203 | H0866 | אֶתְנָה | igen | hire | 11 |
| H0869 | BDB9203 | H0866 | אֶתְנָה | igen | Ethnan | 1 |
| H0876 | BDB875 | H0875 | בְּאֵר | igen | Beer | 2 |
| H0879 | BDB875 | H0875 | בְּאֵר | igen | Beer-elim | 2 |
| H0887 | BDB9359 | H0888,H7489 | בְּאֵשׁ | igen | have a bad smell | 17 |
| H0895 | BDB9361 | H0894 | בָּבֶל | igen | Babylon | 25 |
| H0951 | BDB1292 | H0941 | בּוֺקֵר | igen | herdsman | 1 |
| H0989 | BDB9368 | H0988 | בְּטֵל | igen | cease | 6 |
| H0997 | BDB9369 | H0996 | בֵּין | igen | between | 2 |
| H0999 | BDB9370 | H0998 | בִּינָה | igen | understanding | 1 |
| H1005 | BDB9372 | H1004 | בַּ֫יִת | igen | house | 44 |
| H1028 | BDB1061 | H1027 | בֵּית הָרָם | igen | Beth-haran | 2 |
| H1037 | BDB4654 | H4407 | מִלּוֺא | igen | house of Millo | 8 |
| H1056 | BDB1096 | H1057 | בָּכָא | igen | Baca | 1 |
| H1070 | BDB1109 | H1072 | בִּכְרָה | igen | young camel | 1 |
| H1073 | BDB1113 | H1063 | בִּכּוּרָה | igen | first ripe fig | 0 |
| H1117 | BDB1158 | H1120 | בָּמוֺת | igen | Bamah. See also | 1 |
| H1123 | BDB9386 | H1247,H1121,H1248 | בַּר | igen | son | 0 |
| H1143 | BDB1037 | H0996 | בַּ֫יִן | igen | interval | 2 |
| H1154 | BDB1204 | H1155 | בֹּ֫סֶר | igen | unripe | 1 |
| H1164 | BDB5866 | H5856 | עִי | igen | ruin | 0 |
| H1170 | BDB1212 | H1167,H1168 | בַּעַל | igen | Baal-berith | 4 |
| H1176 | BDB1212 | H1167,H1168 | בַּעַל | igen | Baal-zebub | 8 |
| H1180 | BDB1212 | H1167,H1168 | בַּעַל | igen | owner | 1 |
| H1181 | BDB1212 | H1167,H1168 | בַּעַל | igen | owner | 0 |
| H1184 | BDB1226 | H1173 | בַּעֲלָה | igen | Baale of Judah | 0 |
| H1194 | BDB1052 | H1010 | בֵּית בַּ֫עַל מְעוֺן | NEM | Beon | 1 |
| H1208 | BDB1274 | H1210 | בָּצִיר | igen | vintage | 0 |
| H1222 | BDB1267 | H1220 | בֶּ֫צֶר | igen | straits | 0 |
| H1273 | BDB1014 | H0978 | בַּחֲרוּמִי | igen | Barchumite | 1 |
| H1286 | BDB428 | H0410,H0416,H0415 | אֵל | igen | Berith | 1 |
| H1289 | BDB9387 | H1288 | בְּרַךְ | igen | kneel | 5 |
| H1329 | BDB1382 | H1328 | בְּתוּאֵל | igen | Bethuel | 1 |
| H1336 | BDB1388 | H1335 | בֶּ֫תֶר | igen | Bether | 1 |
| H1362 | BDB1427 | H1364 | גָּבֹהַּ | igen | high | 0 |
| H1400 | BDB9400 | H1399 | גְּבַר | igen | man | 21 |
| H1418 | BDB1477 | H1417 | גְּדוּד | igen | furrow | 0 |
| H1447 | BDB1520 | H1444 | גָּדֵר | igen | wall | 12 |
| H1467 | BDB9396 | H1344 | גֵּוָה | igen | pride | 1 |
| H1499 | BDB1589 | H1498 | גָּזֵל | igen | robbery | 0 |
| H1531 | BDB1651 | H1543 | גֻּלָּה | igen | basin | 0 |
| H1594 | BDB1704 | H1593 | גַּנָּה | igen | garden | 4 |
| H1596 | BDB9418 | H1595 | גְּנַז | igen | treasure | 3 |
| H1635 | BDB9420 | H1634 | גְּרַם | igen | bone | 1 |
| H1655 | BDB9421 | H1653 | גְּשֵׁם | igen | body | 5 |
| H1678 | BDB9423 | H1677 | דֹּב | igen | bear | 1 |
| H1693 | BDB9427 | H1692 | דְּבֵק | igen | cling | 1 |
| H1701 | BDB9428 | H1700 | דִּבְרָה | igen | cause | 2 |
| H1708 | BDB1833 | H1707 | דַּבֶּ֫שֶׁת | igen | Dabbesheth | 1 |
| H1753 | BDB9431 | H1752 | דּוּר | igen | dwell | 7 |
| H1778 | BDB9441 | H1777 | דִּין | igen | judge | 1 |
| H1815 | BDB9452 | H1814 | דְּלַק | igen | burn | 1 |
| H1821 | BDB9453 | H1819 | דְּמָה | igen | be like | 2 |
| H1855 | BDB9455 | H1751,H1854 | דְּקַק | igen | be shattered | 10 |
| H1859 | BDB9432 | H1755 | דָּר | igen | generation | 4 |
| H1868 | BDB9456 | H1867 | דָּֽרְיָ֫וֶשׁ | igen | Darius | 15 |
| H1922 | BDB9468 | H1921 | הֲדַר | igen | glorify | 3 |
| H1939 | BDB2095 | H1938 | הוֺדַוְיָה | igen | Hodaiah | 0 |
| H1941 | BDB2093 | H1940 | הוֺדִיָּה | igen | Hodijah | 5 |
| H1981 | BDB9473 | H1946 | הֲלַךְ | igen | go | 3 |
| H1996 | BDB1541 | H1463 | גּוֺג | igen | Hamon-gog | 4 |
| H2006 | BDB2204 | H2005,H0518 | הֵן | igen | if | 19 |
| H2017 | BDB2212 | H2016 | הֶ֫פֶךְ | igen | the contrary | 1 |
| H2042 | BDB2240 | H2022 | הַר | igen | mountain | 12 |
| H2088 | BDB6199 | H6258,H2009,H5704,H3588 | עַתָּ֫ה | igen | this | 1180 |
| H2089 | BDB8172 | H7716 | שֶׂה | igen | one of a flock | 0 |
| H2110 | BDB9484 | H2109 | זוּן | igen | feed | 1 |
| H2112 | BDB9486 | H2111 | זוּע | igen | tremble | 2 |
| H2116 | BDB2329 | H2115 | זוּר | igen | press down and out | 1 |
| H2170 | BDB9492 | H2167 | זְמָר | igen | music | 4 |
| H2176 | BDB2388 | H2172 | זִמְרָה | igen | melody | 3 |
| H2178 | BDB9494 | H2177 | זַן | igen | kind | 4 |
| H2189 | BDB2323 | H2113 | זְוָעָה | igen | a trembling | 7 |
| H2200 | BDB9495 | H2199 | זְעִ֑ק | igen | cry | 1 |
| H2211 | BDB9498 | H2210 | זְקַף | igen | raise | 1 |
| H2217 | BDB9499 | H2216 | זְרֻבָּבֶ֫ל | igen | Zerubbabel | 1 |
| H2234 | BDB9500 | H2232,H2233 | זְרַע | igen | seed | 1 |
| H2269 | BDB9504 | H2266 | חֲבַר | igen | fellow | 6 |
| H2298 | BDB9603 | H1768,H1836 | <big>כ</big> | igen | one | 14 |
| H2305 | BDB9507 | H2304 | חֶדְוָה | igen | joy | 1 |
| H2316 | BDB2575 | H2315 | חֶ֫דֶר | igen | Hadar | 0 |
| H2323 | BDB9509 | H2319 | חֲדַ֑ת | igen | new | 1 |
| H2334 | BDB2596 | H2333 | חַוָּה | igen | (Bashan-) Havoth-jair | 8 |
| H2337 | BDB2603 | H2336 | חוֺחַ | igen | brier | 0 |
| H2358 | BDB9515 | H2357 | חִוָּר | igen | white | 1 |
| H2361 | BDB307 | H2438 | חִירָם | igen | Huram. Compare | 13 |
| H2408 | BDB9519 | H2399 | חֲטָי | igen | sin | 1 |
| H2409 | BDB9520 | H2403 | חַטָּיָא | igen | sin-offering | 0 |
| H2417 | BDB9522 | H2416 | חַי | igen | living | 7 |
| H2425 | BDB2715 | H2421 | חָיָה | igen | live | 1 |
| H2429 | BDB9524 | H2428 | חַ֫יִל | igen | power | 7 |
| H2439 | BDB2650 | H2363 | חוּשׁ | igen | haste | 0 |
| H2454 | BDB2736 | H2451 | חָכְמה | igen | wisdom | 0 |
| H2499 | BDB9528 | H2498 | חֲלַף | igen | pass | 4 |
| H2510 | BDB2823 | H2509 | חָלָק | igen | Halak | 2 |
| H2511 | BDB2823 | H2509 | חָלָק | igen | smooth | 1 |
| H2562 | BDB9531 | H2561 | חֲמַר | igen | wine | 6 |
| H2579 | BDB2911 | H2574,H2578 | חֲמָת | igen | Chamath-Rabbah | 2 |
| H2589 | BDB2937 | H2603 | חָנַן | igen | shew favour | 0 |
| H2604 | BDB9534 | H2603 | חֲנַן | igen | shew favour | 2 |
| H2618 | BDB1172 | H1136 | בֶּןחֶֿ֫סֶד | igen | Hesed | 1 |
| H2699 | BDB3047 | H2691 | חָצֵר | igen | Hazerim | 0 |
| H2702 | BDB3052 | H2701 | חֲצַר סוּסָה | NEM | Hazar-susim | 2 |
| H2711 | BDB3072 | H2706 | חֹק | igen | something prescribed | 2 |
| H2718 | BDB9541 | H2717 | חֲרַב | igen | be waste | 1 |
| H2749 | BDB9542 | H2748 | חַרְטֹם | igen | magician | 5 |
| H2753 | BDB3121 | H2752 | חֹרִי | igen | Hori | 4 |
| H2755 | BDB3081 | H2716,H3123 | חֶרֶא | igen | dove’s dung | 0 |
| H2769 | BDB3132 | H2768 | חֶרְמוֺן | igen | the Hermonites | 1 |
| H2783 | BDB9543 | H2761,H2504 | חֲרַךְ | igen | loin | 1 |
| H2794 | BDB3181 | H2790 | חָרַשׁ | igen | cut in | 0 |
| H2798 | BDB3182 | H2796,H1516 | חָרָשׁ | igen | cut in | 1 |
| H2804 | BDB9545 | H2803 | חֲשַׁב | igen | think | 1 |
| H2824 | BDB3221 | H2825 | חֲשֵׁכָה | igen | darkness | 1 |
| H2857 | BDB9552 | H2856 | חֲתַם | igen | seal | 1 |
| H2877 | BDB9555 | H2876 | טַבָּח | igen | guardsman | 1 |
| H2890 | BDB3303 | H2889 | טָהוֺר | igen | clean | 1 |
| H2920 | BDB9559 | H2919 | טַל | igen | dew | 5 |
| H2924 | BDB3339 | H2922,H2923 | טָלֶה | igen | lamb | 2 |
| H2941 | BDB9562 | H2942,H2940 | טְעֵם | igen | taste | 2 |
| H2957 | BDB9564 | H2956 | טְרַד | igen | chase away | 4 |
| H2962 | BDB3379 | H2958 | טֶ֫רֶם | igen | not yet | 56 |
| H3028 | BDB9569 | H3027 | יַד | igen | hand | 17 |
| H3046 | BDB9571 | H3045 | יְדַע | igen | know | 47 |
| H3052 | BDB9573 | H3051 | יְהַב | igen | give | 28 |
| H3057 | BDB3478 | H3064 | יְהוּדִּי | igen | Jehudijah | 1 |
| H3069 | BDB2100 | H3068,H1961,H0430,H0589,H2022,H6635 | יהוה | igen | God | 306 |
| H3070 | BDB7656 | H7200,H7203 | רָאָה | igen | see | 0 |
| H3071 | BDB5242 | H5251 | נֵס | igen | standard | 0 |
| H3072 | BDB6941 | H6664 | צֶ֫דֶק | igen | rightness | 0 |
| H3073 | BDB8734 | H7965 | שָׁלוֺם | igen | completeness | 0 |
| H3074 | BDB8775 | H8033 | שָׁם | igen | there | 0 |
| H3090 | BDB2119 | H3089 | יְהוֺשֶׁ֫בַע | igen | Jehoshabeath | 2 |
| H3099 | BDB2103 | H3059 | יְהוֺאָחָז | igen | Jehoahaz | 4 |
| H3101 | BDB2104 | H3060 | יְהוֺאָשׁ | igen | Joash | 47 |
| H3107 | BDB2105 | H3075 | יְהוֺזָבָד | igen | Josabad | 11 |
| H3110 | BDB2106 | H3076 | יְהוֺחָנָן | igen | Johanan | 22 |
| H3111 | BDB2107 | H3077 | יְהוֺיָדָע | igen | Jehoiada | 5 |
| H3112 | BDB2108 | H3078,H3204 | יְהוֺיָכִין | igen | Jehoiachin | 1 |
| H3113 | BDB2109 | H3079 | יְהוֺיָקִים | igen | Joiakim. Compare | 4 |
| H3114 | BDB2110 | H3080 | יְהוֺיָרִיב | igen | Joiarib | 5 |
| H3122 | BDB2112 | H3082 | יְהוֺנָדָב | igen | Jonadab | 7 |
| H3129 | BDB2113 | H3083 | יְהוֺנָתָן | igen | Jonathan | 43 |
| H3130 | BDB3600 | H3084 | יוֺסֵף | igen | Joseph. Compare | 213 |
| H3137 | BDB2109 | H3079 | יְהוֺיָקִים | igen | Jokim | 1 |
| H3141 | BDB2118 | H3088 | יְהוֺרָם | igen | Joram | 20 |
| H3146 | BDB2122 | H3092 | יְהוֺשָׁפָט | igen | Joshaphat | 2 |
| H3159 | BDB2469 | H3158 | יִזְרְעֵאלִי | igen | a Jezreelitess | 0 |
| H3185 | BDB3034 | H3183 | יַחְצְאֵל | igen | Jahziel. Compare | 1 |
| H3186 | BDB3524 | H0310 | (ו)ייחר | igen | to remain behind | 0 |
| H3197 | BDB3535 | H3027 | יך | igen | a hand | 0 |
| H3212 | BDB2162 | H1980 | הָלַךְ | igen | go | 0 |
| H3221 | BDB9582 | H3220 | יַם | igen | sea | 2 |
| H3231 | BDB3573 | H0541 | יָמַן | igen | go to | 4 |
| H3240 | BDB5049 | H5117,H5118 | נוּחַ | igen | rest | 0 |
| H3249 | BDB5544 | H5493,H5637,H8269 | סוּר | igen | departing | 0 |
| H3255 | BDB9583 | H3254 | יְסַף | igen | add | 1 |
| H3273 | BDB3615 | H3262 | יְעוּאֵל | igen | Jeiel | 14 |
| H3274 | BDB5930 | H3266 | יְעוּשׁ | igen | Jeush (from the margin). Compare | 0 |
| H3292 | BDB6328 | H6130,H0885,H1142 | עֲקָן | igen | Jaakan. Compare | 1 |
| H3340 | BDB3678 | H3339 | יִצְרִי | igen | Jezerites | 1 |
| H3345 | BDB9589 | H3344 | יְקַד | igen | burn | 8 |
| H3347 | BDB3686 | H4169 | מוֺקְדָה | igen | Jokdeam | 1 |
| H3367 | BDB9591 | H3366 | יְקָר | igen | honour | 7 |
| H3393 | BDB9594 | H3391 | יְרַךְ | igen | month | 2 |
| H3443 | BDB9597 | H3442 | יֵשׁוּעַ | igen | Jeshua | 1 |
| H3479 | BDB9596 | H3478 | יִשְׂרָאֵל | igen | Israel | 8 |
| H3482 | BDB8318 | H3481 | יִשְׂרְאֵלִי | igen | Jisreelitess | 0 |
| H3487 | BDB9600 | H0853 | יָת | igen | sign of the object of a verb | 1 |
| H3542 | BDB9605 | H3541 | כָּה | igen | here | 1 |
| H3549 | BDB9607 | H3548 | כָּהֵן | igen | priest | 8 |
| H3567 | BDB9610 | H3566 | כּ֫וֺרֶשׁ | igen | Cyrus | 8 |
| H3571 | BDB3970 | H3569 | כּוּשִׁי | igen | a Cushite woman | 0 |
| H3606 | BDB9612 | H3605,H6903 | כֹּל | igen | the whole | 82 |
| H3613 | BDB688 | H0672 | אֶפְרָ֫תָה | igen | Caleb-ephrathah | 2 |
| H3635 | BDB9611 | H3634 | כְּלַל | igen | complete | 7 |
| H3652 | BDB9613 | H3651 | כֵּן | igen | thus | 8 |
| H3659 | BDB2108 | H3078,H3204 | יְהוֺיָכִין | igen | Coniah | 3 |
| H3661 | BDB4088 | H3657 | כַּנָּה | igen | support | 0 |
| H3696 | BDB4126 | H3694,H8396 | כְּסֻלּוֺת | igen | Chisloth-tabor | 2 |
| H3726 | BDB4164 | H3723 | כָּפָר | igen | village | 1 |
| H3743 | BDB4186 | H3742 | כְּרוּב | igen | Cherub | 2 |
| H3762 | BDB4202 | H3761 | כַּרְמְלִי | igen | the Carmelite | 0 |
| H3769 | BDB9625 | H3603 | כרר | igen | dancing | 2 |
| H3773 | BDB4216 | H3772 | כָּרַת | igen | cut off | 3 |
| H3790 | BDB9628 | H3789 | כְּתַב | igen | write | 8 |
| H3797 | BDB9630 | H3796 | כְּתַל | igen | wall | 2 |
| H3821 | BDB9636 | H3820 | לֵב | igen | heart | 1 |
| H3825 | BDB9635 | H3824 | לְבַב | igen | heart | 7 |
| H3827 | BDB4330 | H3852 | לֶהָבָה | igen | flame | 1 |
| H3831 | BDB9638 | H3830 | לְְבוּשׁ | igen | garment | 2 |
| H3840 | BDB4317 | H3843 | לְבֵנָה | igen | brick | 0 |
| H3848 | BDB9637 | H3847 | לְבֵשׁ | igen | be clothed | 3 |
| H3861 | BDB2188 | H1992,H2004,H3860 | הֵ֫מָּה | igen | except | 7 |
| H3866 | BDB4349 | H3865 | לוּד | igen | Ludim. Lydians | 3 |
| H3879 | BDB9641 | H3878 | לֵוָי | igen | Levite | 4 |
| H3909 | BDB4365 | H3814,H3858 | לָּט | igen | secrecy | 6 |
| H3916 | BDB9645 | H3915 | לֵילָא | igen | night | 5 |
| H3961 | BDB9646 | H3956 | לִשָּׁן | igen | tongue | 7 |
| H3969 | BDB9647 | H3967 | <big>מ</big> | igen | hundred | 8 |
| H3997 | BDB948 | H3996 | מָבוֺא | igen | entrance | 1 |
| H4036 | BDB1575 | H4032 | מָגוֺר | igen | Magormissabib | 2 |
| H4040 | BDB9416 | H4039 | מְגִלָּה | igen | roll | 1 |
| H4059 | BDB4510 | H4058,H4128 | מָדַד | igen | measure | 0 |
| H4078 | BDB4521 | H1767,H4100 | מַדַּי | igen | sufficiency | 0 |
| H4079 | BDB1922 | H4066,H4067,H4060 | מָדוֺן | igen | strife | 10 |
| H4090 | BDB1922 | H4066,H4067,H4060 | מָדוֺן | igen | strife | 2 |
| H4092 | BDB1926 | H4084 | מִדְיָנִי | igen | Midianite | 1 |
| H4101 | BDB9652 | H3964,H4100 | מָה | igen | what? | 13 |
| H4109 | BDB2166 | H4108 | מַהֲלָךְ | igen | walk | 5 |
| H4146 | BDB3595 | H4144 | מוֺסָד | igen | foundation | 5 |
| H4153 | BDB4749 | H4573 | ַמעַדְיָה | igen | Moadiah. Compare | 1 |
| H4154 | BDB4747 | H4571 | מָעַד | igen | slip | 0 |
| H4176 | BDB3725 | H4175 | מוֺרֶה | igen | teacher | 3 |
| H4178 | BDB4813 | H4803 | מָרַט | igen | make smooth | 0 |
| H4193 | BDB9653 | H4191 | מוֺת | igen | death | 1 |
| H4215 | BDB2446 | H2219 | זָרָה | igen | scatter | 1 |
| H4282 | BDB3185 | H4281 | מַחֲרֵשָׁה | igen | ploughshare | 0 |
| H4319 | BDB4618 | H4321 | מִיכָֽיְהוּ | igen | Micaiah (2 Chronicles 18:8) | 0 |
| H4328 | BDB3594 | H4145 | מוּסָדָה | igen | foundation | 0 |
| H4333 | BDB9656 | H4332 | מִישָׁאֵל | igen | Mishael | 1 |
| H4336 | BDB9657 | H4335 | מֵישַׁךְ | igen | Meshak | 14 |
| H4342 | BDB3899 | H3527 | כָּבַר | igen | be much | 1 |
| H4389 | BDB4259 | H4388 | מַכְתֵּשׁ | igen | Maktesh | 1 |
| H4391 | BDB9658 | H4390 | מְלָא | igen | fill | 2 |
| H4415 | BDB9472 | H1965,H1964 | הֵיכַל | igen | eat salt | 1 |
| H4430 | BDB9662 | H4429 | מֶ֫לֶךְ | igen | king | 180 |
| H4444 | BDB4686 | H4428,H7769 | מַלְכִישׁוּעַ | igen | Malchishua | 10 |
| H4504 | BDB9675 | H4503 | מִנְחָה | igen | gift | 2 |
| H4509 | BDB4627 | H4326 | מִיָּמִן | igen | Miniamin. Compare | 3 |
| H4559 | BDB5701 | H4558 | מִסְפָּר | NEM | Mispereth. Compare | 1 |
| H4593 | BDB4813 | H4803 | מָרַט | igen | make smooth | 1 |
| H4610 | BDB6079 | H4608,H0131,H1032,H1483,H2776,H3872,H6731 | מַעֲלֶה | igen | ascent | 4 |
| H4629 | BDB6365 | H4628 | מַעֲרָב | igen | bare | 2 |
| H4632 | BDB6415 | H4631 | מְעָרָה | igen | Mearah | 1 |
| H4663 | BDB6741 | H4662 | מִפְקָד | igen | Miphkad | 0 |
| H4678 | BDB5324 | H4676,H5324 | מַצֵּבָה | igen | pillar | 6 |
| H4704 | BDB7166 | H6810 | צָעִיר | igen | little | 0 |
| H4798 | BDB7839 | H4797 | מַרְזֵחַ | igen | cry | 1 |
| H4804 | BDB9680 | H4803 | מְרַט | igen | pluck | 1 |
| H4827 | BDB8035 | H7489 | רָעַע | igen | be evil | 1 |
| H4873 | BDB9681 | H4872 | מֹשֶׁה | igen | Moses | 1 |
| H4887 | BDB9682 | H4886 | מְשַׁח | igen | oil | 2 |
| H4921 | BDB8748 | H4919 | מְשִׁלֵּמוֺת | igen | Meshillemith. Compare | 1 |
| H4930 | BDB5640 | H4548 | מַסְמֵר | igen | nail | 1 |
| H4961 | BDB9991 | H4960 | מִשְׁתֵּי | igen | feast | 1 |
| H4965 | BDB521 | H0522 | אַמָּה | igen | Metheg-ammah | 2 |
| H4973 | BDB9181 | H4459 | מְתַלְּיוֺת | igen | teeth | 3 |
| H4988 | BDB4901 | H4985 | מָתֹק | igen | become sweet | 0 |
| H5013 | BDB9683 | H5012 | <big>נ</big> | igen | see | 1 |
| H5020 | BDB9686 | H5019 | נְבוּכַדְנֶצַּר | igen | Nebuchadnezzar | 31 |
| H5103 | BDB9696 | H5102 | נְהַר | igen | river | 15 |
| H5111 | BDB9699 | H5075,H5110 | נוּד | igen | flee | 1 |
| H5182 | BDB9704 | H5181 | נְחֵת | igen | descend | 6 |
| H5191 | BDB9705 | H5190 | נְטַל | igen | lift | 2 |
| H5227 | BDB5199 | H5226 | נֹ֫כַח | igen | front | 25 |
| H5229 | BDB5200 | H5228 | נָכֹחַ | igen | straight | 4 |
| H5256 | BDB9710 | H5255 | נְסַח | igen | pull away | 1 |
| H5260 | BDB9711 | H5258 | נְסַךְ | igen | pour out | 1 |
| H5267 | BDB9737 | H5559 | סְלֵק | igen | come up | 1 |
| H5297 | BDB4773 | H4644 | מֹף | igen | Noph | 7 |
| H5304 | BDB5295 | H5300 | נפיסים | igen | Nephusim (from the margin) | 1 |
| H5308 | BDB9713 | H5307 | נְפַל | igen | fall | 11 |
| H5326 | BDB9716 | H5324 | נִצְבָּה | igen | firmness | 1 |
| H5330 | BDB9717 | H5329 | נְצַח | igen | distinguish oneself | 1 |
| H5338 | BDB9718 | H5337 | נְצַל | igen | rescue | 3 |
| H5368 | BDB9720 | H5367 | נְקַשׁ | igen | knock | 1 |
| H5372 | BDB7754 | H7279 | רָגַן | igen | murmur | 0 |
| H5376 | BDB9721 | H5375 | נְשָׂא | igen | lift | 3 |
| H5383 | BDB5401 | H5378 | נָשָׁא | igen | lend | 12 |
| H5396 | BDB9722 | H5395,H5397 | נִשְׁמָה | igen | breath | 1 |
| H5415 | BDB9726 | H5414 | נְתַן | igen | give | 7 |
| H5463 | BDB9733 | H5462 | סְגַר | igen | shut | 1 |
| H5472 | BDB5515 | H5253 | סוּג | igen | move away | 14 |
| H5494 | BDB5544 | H5493,H5637,H8269 | סוּר | igen | turn aside | 2 |
| H5505 | BDB5556 | H5504 | סַ֫חַר | igen | traffic | 0 |
| H5574 | BDB5645 | H5570 | סְנוּאָה | igen | Hasenuah (including the art) | 1 |
| H5598 | BDB5690 | H5593 | סַף | igen | Sippai. Compare | 1 |
| H5626 | BDB886 | H0953 | בּוֺר הַסִּרָה | NEM | Sirah. See also | 1 |
| H5635 | BDB8331 | H8313 | שָׂרַף | igen | burn | 1 |
| H5673 | BDB9748 | H5656 | עֲבִידָה | igen | work | 6 |
| H5722 | BDB5828 | H5719 | עָדִין | igen | Adino | 1 |
| H5735 | BDB6420 | H6177 | עֲרֹעֵר | igen | Adadah | 1 |
| H5745 | BDB5760 | H5658 | עוֺבָל | igen | Obal | 1 |
| H5751 | BDB9754 | H5750 | עוֺד | igen | still | 1 |
| H5758 | BDB9755 | H5753,H5771 | עֲוָיָה | igen | iniquity | 1 |
| H5761 | BDB5872 | H5757 | עַוִּי | igen | Avim | 4 |
| H5776 | BDB9756 | H5774 | עוֺף | igen | fowl | 2 |
| H5831 | BDB9759 | H5830 | עֶזְרָא | igen | Ezra | 3 |
| H5839 | BDB9760 | H5838 | עֲזַרְיָה | igen | Azariah | 1 |
| H5843 | BDB9586 | H2942 | עֵטָא | igen | counsel | 1 |
| H5853 | BDB5999 | H5852,H5854 | עֲטָרוֺת | igen | Ataroth-adar(-addar) | 4 |
| H5855 | BDB5999 | H5852,H5854 | עֲטָרוֺת | igen | Atroth | 2 |
| H5865 | BDB6119 | H5769 | עוֺלָם | igen | long duration | 1 |
| H5870 | BDB9761 | H5869 | עַ֫יִן | igen | eye | 5 |
| H5875 | BDB6016 | H5869,H5871,H5878,H8179 | עַ֫יִן | igen | En-hakhore | 2 |
| H5881 | BDB6030 | H2704,H2703 | עֵינָן | igen | Enan. Compare | 5 |
| H5883 | BDB6016 | H5869,H5871,H5878,H8179 | עַ֫יִן | igen | En-rogel | 8 |
| H5886 | BDB6016 | H5869,H5871,H5878,H8179 | עַ֫יִן | igen | dragon well | 0 |
| H5888 | BDB6033 | H5774 | עִיף | igen | be faint | 5 |
| H5899 | BDB6039 | H3405 | עִיר הַתְּמָרִים | NEM | the city of palmtrees | 8 |
| H5917 | BDB6054 | H5912 | עָכָן | igen | Achar. Compare | 1 |
| H5921 | BDB3996 | H3588,H3651 | כִּי עַל כֵּן | igen | forasmuch as | 5768 |
| H5932 | BDB6086 | H5766 | עַלְוָה | igen | injustice | 1 |
| H5946 | BDB9766 | H5945 | עֶלְיוֺן | igen | Supreme | 4 |
| H5961 | BDB6111 | H4192 | עֲלָמוֺת | igen | young woman | 3 |
| H5972 | BDB9776 | H5971 | עַם | igen | people | 15 |
| H5974 | BDB9777 | H5973 | עִם | igen | with | 22 |
| H5976 | BDB4747 | H4571 | מָעַד | igen | slip | 1 |
| H5978 | BDB6145 | H5973 | עִם | igen | with | 42 |
| H5985 | BDB6151 | H5984 | עַמּוֺנִי | igen | Ammonite | 0 |
| H5993 | BDB6144 | H5971 | עַם | igen | Amminadib | 0 |
| H6032 | BDB9780 | H6030 | עֲנָה | igen | answer | 30 |
| H6038 | BDB6211 | H6037 | עֲנָוָה | igen | humility | 5 |
| H6046 | BDB6019 | H5873 | עֵין גַּנִּים | NEM | Anem | 1 |
| H6062 | BDB6237 | H6061 | עֲנָק | igen | Anakim | 9 |
| H6077 | BDB6252 | H6076 | עֹ֫פֶל | igen | Ophel | 5 |
| H6159 | BDB6367 | H6158 | עֹרֵב | igen | Oreb | 7 |
| H6164 | BDB1082 | H1026 | בֵּית הָֽעֲרָבָה | igen | place of the depression | 2 |
| H6173 | BDB9797 | H6168 | עַרְוָה | igen | dishonour | 1 |
| H6255 | BDB6477 | H6252 | עַשְׁתָּרוֺת | igen | Ashtoreth Karnaim | 2 |
| H6263 | BDB9804 | H6257,H6264 | עֲתִיד | igen | ready | 1 |
| H6268 | BDB9805 | H6267,H6275 | עַתִּיק | igen | advanced | 3 |
| H6358 | BDB6595 | H6362 | פָּטַר | igen | separate | 0 |
| H6359 | BDB6595 | H6362 | פָּטַר | igen | separate | 0 |
| H6366 | BDB6536 | H6310 | פֶּה | igen | mouth | 1 |
| H6374 | BDB6536 | H6310 | פֶּה | igen | mouth | 2 |
| H6386 | BDB9809 | H6385 | פְּלַג | igen | divide | 1 |
| H6407 | BDB1083 | H1046 | בֵּית פָּ֑לֶט | NEM | Paltite | 1 |
| H6422 | BDB6634 | H6423 | פְּלֹנִי | NEM | a certain one | 1 |
| H6433 | BDB9814 | H6310 | פֻּם | NEM | mouth | 6 |
| H6438 | BDB6687 | H6434 | פִּנָּה | NEM | corner | 29 |
| H6450 | BDB675 | H0658 | אֶ֫פֶס דַּמִּים | igen | Pas-dammim. Compare | 2 |
| H6512 | BDB3017 | H2661 | חֲפַרְפָּרָה | NEM | mole | 1 |
| H6546 | BDB6800 | H6545 | פֶּ֫רַע | igen | leader | 2 |
| H6559 | BDB6807 | H6556 | פֶּ֫רֶץ | igen | Perazim | 1 |
| H6560 | BDB6808 | H6557 | פֶ֫רֶץ | igen | Perezuzza | 4 |
| H6565 | BDB6817 | H6331 | פָּרַר | igen | break | 50 |
| H6568 | BDB9824 | H6567 | פְּרַשׁ | igen | make distinct | 1 |
| H6606 | BDB9829 | H6605 | פְּתַח | igen | open | 2 |
| H6702 | BDB7025 | H3341 | צוּת | igen | kindle | 1 |
| H6737 | BDB7058 | H6735,H6736 | צִיר | igen | supply oneself with provisions | 1 |
| H6744 | BDB9842 | H6743 | צְלַח | igen | prosper | 4 |
| H6752 | BDB7079 | H6738 | צֵל | igen | shadow | 4 |
| H6755 | BDB9843 | H6754 | צְלֵם | igen | image | 17 |
| H6799 | BDB6902 | H6630 | צַאֲנָן | igen | Zenan | 1 |
| H6820 | BDB1151 | H1106 | בֶּ֫לַע | igen | Zoar | 10 |
| H6827 | BDB7178 | H6837,H1189 | צִפְיוֺן | igen | Zephon | 1 |
| H6839 | BDB7174 | H6822 | צָפָה | igen | Zophim | 1 |
| H6853 | BDB9844 | H6833 | צִפַּר | igen | bird | 4 |
| H6897 | BDB7281 | H6896 | קֵבָה | igen | stomach | 1 |
| H6902 | BDB9848 | H6901 | קַבֵּל | igen | receive | 3 |
| H6905 | BDB7283 | H6904 | קְבֹל | igen | presence | 1 |
| H6909 | BDB7289 | H3343 | קַבְצְאֵל | igen | Kabzeel. Compare | 3 |
| H6928 | BDB9850 | H6927 | קַדְמָה | igen | former time | 2 |
| H6944 | BDB7327 | H6946,H5880,H8483 | קָדֵשׁ | igen | apartness | 469 |
| H6947 | BDB6023 | H5880 | עֵין מִשְׁפָּטּ | NEM | Kadeshbarnea | 20 |
| H6948 | BDB7325 | H6945 | קָדֵּשׁ | igen | temple-prostitute | 5 |
| H6961 | BDB7346 | H6957 | קַו | igen | cord | 0 |
| H6966 | BDB9856 | H6965 | קוּם | igen | arise | 35 |
| H6978 | BDB7348 | H6979,H6957 | קַוְקָו | igen | might | 4 |
| H6987 | BDB7393 | H6986 | קֶ֫טֶב | igen | destruction | 1 |
| H6990 | BDB7356 | H5354,H6962,H6985 | קוּט | igen | break | 1 |
| H6992 | BDB9859 | H6991 | קְטַל | igen | slay | 7 |
| H7006 | BDB7419 | H6958 | קָיָה | igen | vomit | 1 |
| H7019 | BDB7431 | H6972 | קַ֫יִץ | igen | summer | 20 |
| H7029 | BDB7390 | H6984 | קוּשָׁיָ֫הוּ | igen | Kishi | 1 |
| H7041 | BDB7447 | H7042 | קְלִיטָא | igen | Kelaiah | 1 |
| H7063 | BDB7474 | H7057 | קִמּוֺשׂ | igen | thistles | 1 |
| H7118 | BDB9866 | H7117 | קְצָת | igen | end | 3 |
| H7125 | BDB7557 | H7122 | קְרַאת | igen | encounter | 0 |
| H7127 | BDB9870 | H7126 | קְרֵב | igen | approach | 9 |
| H7162 | BDB9873 | H7161 | קֶ֫רֶן | igen | horn | 14 |
| H7178 | BDB7577 | H7156 | קִרְיָתַ֫יִם | igen | Kartan | 1 |
| H7201 | BDB7655 | H1676 | <big>ר</big> | igen | kite | 1 |
| H7207 | BDB7656 | H7200,H7203 | רָאָה | igen | see | 0 |
| H7226 | BDB7678 | H7218,H4763,H7219,H7220 | רֹאשׁ | igen | place at the head | 1 |
| H7252 | BDB7726 | H7250 | רָבַע | igen | lie stretched out | 1 |
| H7260 | BDB9880 | H7229 | רַב | igen | great | 8 |
| H7262 | BDB7692 | H7227,H7248,H7249,H8248 | רַב | igen | chief | 32 |
| H7265 | BDB9888 | H7264 | רְגַז | igen | enrage | 1 |
| H7294 | BDB7780 | H7293 | רַ֫הַב | igen | Rahab | 4 |
| H7313 | BDB9895 | H7311 | רוּם | igen | rise | 4 |
| H7358 | BDB7862 | H7356 | רֶ֫חֶם | igen | womb | 26 |
| H7361 | BDB7862 | H7356 | רֶ֫חֶם | igen | womb | 0 |
| H7412 | BDB9903 | H7411 | רְמָא | igen | cast | 12 |
| H7421 | BDB763 | H0761 | אֲרַמִּי | igen | Aramæan | 1 |
| H7427 | BDB7817 | H7319 | רוֺמֵמוּת | igen | uprising | 1 |
| H7432 | BDB7813 | H7216,H1568,H7414,H7418,H3406 | רָ(א)מוֺת | igen | Remeth | 1 |
| H7433 | BDB7813 | H7216,H1568,H7414,H7418,H3406 | רָ(א)מוֺת | igen | Ramoth-gilead | 1 |
| H7434 | BDB7181 | H4708 | מִצְפֶּה | NEM | Ramath-mizpeh | 2 |
| H7436 | BDB6995 | H6689 | צוּפִי | igen | Ramathaimzophim | 2 |
| H7437 | BDB7812 | H7418 | רָ(א)מַת | igen | Ramath-lehi | 2 |
| H7444 | BDB7973 | H7442,H7323 | רָנַן | igen | give a ringing cry | 0 |
| H7465 | BDB8036 | H7489,H7462 | רָעַע | igen | break | 1 |
| H7485 | BDB8020 | H7480 | רְעֵלָיָה | igen | Raamiah | 1 |
| H7512 | BDB9909 | H7511 | רְפַס | igen | tread | 2 |
| H7515 | BDB8064 | H7511 | רָפַס | igen | stamp | 3 |
| H7529 | BDB8087 | H7531 | רִצְפָּה | igen | glowing stone | 1 |
| H7535 | BDB8113 | H7534 | רַק | igen | leanness | 109 |
| H7560 | BDB9910 | H7559 | רְשַׁם | igen | inscribe | 7 |
| H7572 | BDB8141 | H7569 | רַתּוֺק | igen | chain | 0 |
| H7593 | BDB9922 | H7592 | <big>שׁ</big> | igen | ask | 6 |
| H7598 | BDB8374 | H7597 | שְׁאַלְתִּיאֵל | igen | Shealtiel | 1 |
| H7606 | BDB9924 | H7605 | שְׁאָר | igen | rest | 12 |
| H7608 | BDB8386 | H7607 | שְׁאֵר | igen | flesh | 1 |
| H7654 | BDB8154 | H7653 | שָׂבְעָה | igen | satiety | 6 |
| H7658 | BDB8428 | H7651 | שִׁבְעָ֫נָה | igen | seven | 1 |
| H7671 | BDB8443 | H7667 | שֶׁ֫בֶר | igen | Shebarim | 1 |
| H7695 | BDB9932 | H7694 | שֵׁגָל | igen | consort | 3 |
| H7715 | BDB9935 | H7714 | שַׁדְרַךְ | igen | Shadrach | 14 |
| H7734 | BDB5515 | H5253 | סוּג | igen | move away | 1 |
| H7735 | BDB5517 | H5473 | סוּג | igen | fence about | 1 |
| H7738 | BDB8501 | H8663 | תְּשֻׁאָה | igen | noise | 0 |
| H7765 | BDB8547 | H7764 | שׁוּנִי | igen | a Shunite | 1 |
| H7773 | BDB8551 | H7769 | שׁוּעַ | igen | cry out | 1 |
| H7780 | BDB8516 | H7731 | שׁוֺבַךְ | igen | Shophach | 2 |
| H7792 | BDB9943 | H7791 | שׁוּר | igen | wall | 3 |
| H7820 | BDB8587 | H7819 | שָׁחַט | igen | slaughter | 5 |
| H7873 | BDB5516 | H5509 | סִיג | igen | a moving back | 1 |
| H7917 | BDB8248 | H7916 | שָׂכִיר | igen | hired | 1 |
| H7929 | BDB8670 | H7926,H7927 | שְׁכֶם | igen | shoulder | 1 |
| H7932 | BDB9951 | H4908,H7931 | שְׁכֵן | igen | dwell | 2 |
| H7953 | BDB8695 | H7951,H7952 | שָׁלָה | igen | draw out | 1 |
| H7960 | BDB9955 | H7955,H7596 | שָׁלוּ | igen | neglect | 4 |
| H7968 | BDB8746 | H7967 | שַׁלּוּן | igen | Shallum | 1 |
| H7972 | BDB9957 | H7971 | שְׁלַח | igen | send | 14 |
| H7981 | BDB9958 | H7980 | שְׁלֵט | igen | have power | 7 |
| H7986 | BDB8721 | H7989 | שַׁלִּיט | igen | having mastery | 1 |
| H8000 | BDB9961 | H7999 | שְׁלֵם | igen | be complete | 3 |
| H8007 | BDB8251 | H8012 | שַׂלְמוֺן | igen | Salma | 4 |
| H8009 | BDB8251 | H8012 | שַׂלְמוֺן | igen | Salmon. Compare | 1 |
| H8023 | BDB8701 | H8024,H7888 | שֵׁלָנִי | igen | Shiloni | 1 |
| H8036 | BDB9963 | H8034 | שֻׁם | igen | name | 12 |
| H8065 | BDB9965 | H8064 | שְׁמַ֫יִן | igen | heavens | 38 |
| H8067 | BDB8817 | H8066 | שְׁמִינִי | igen | eighth | 3 |
| H8073 | BDB8252 | H8014 | שַׂלְמַי | igen | Shalmai (from the margin) | 0 |
| H8086 | BDB9967 | H8085 | שְׁמַע | igen | hear | 9 |
| H8093 | BDB8802 | H8048,H8092,H8096,H8054,H8049 | שַׁמָּה | igen | Shimeah | 3 |
| H8112 | BDB8860 | H8110 | שִׁמְרוֺן | igen | Shimon-meron | 2 |
| H8115 | BDB9968 | H8111 | שָֽׁמְרָ֑יִן | igen | Samaria | 2 |
| H8133 | BDB8881 | H8138,H8132 | שָׁנָה | igen | change | 21 |
| H8153 | BDB3798 | H3462 | יָשֵׁן | igen | sleep | 1 |
| H8157 | BDB8901 | H8156 | שֶׁ֫סַע | igen | cleft | 4 |
| H8183 | BDB8292 | H5591 | שְׂעָרָה | igen | hurricane | 2 |
| H8200 | BDB9978 | H8199 | שְׁפַט | igen | judge | 1 |
| H8214 | BDB9979 | H8213 | שְׁפֵל | igen | be low | 4 |
| H8226 | BDB5683 | H5603 | סָפַן | igen | cover | 1 |
| H8241 | BDB8626 | H7858 | שֶׁ֫טֶף | igen | flood | 1 |
| H8284 | BDB8569 | H7791 | שׁוּר | igen | row | 1 |
| H8293 | BDB9033 | H8281 | שָׁרָה | igen | let loose | 0 |
| H8309 | BDB8482 | H7709 | שְׁדֵמָה | igen | field | 0 |
| H8323 | BDB8190 | H7787,H4883,H5493 | שׂוּר | igen | be prince | 5 |
| H8326 | BDB9050 | H8270 | שֹׁר | igen | navel-string | 1 |
| H8330 | BDB9987 | H8328 | שֹׁ֫רֶשׁ | igen | root | 3 |
| H8338 | BDB8491 | H8341 | שִׁשָּׁה | igen | lead on | 1 |
| H8340 | BDB9064 | H8339 | שִׁשֵּׁא | igen | Sheshbazzar | 2 |
| H8390 | BDB3145 | H8475 | תַּחֲרֵעַ | igen | Tarea. See | 1 |
| H8406 | BDB9994 | H7665 | <big>ת</big> | igen | break | 1 |
| H8421 | BDB9995 | H7725 | תּוּב | igen | return | 8 |
| H8445 | BDB7352 | H8618 | תִּקְוָה | igen | Tikvath (by correction for ) | 0 |
| H8448 | BDB9099 | H8389,H8447 | תֹּ֫אַר | igen | plait | 1 |
| H8450 | BDB9997 | H7794 | תּוֺר | igen | bullock | 7 |
| H8452 | BDB3726 | H8451 | תּוֺרָה | igen | direction | 1 |
| H8459 | BDB9123 | H8430 | תּוֺחַ | igen | Tohu | 1 |
| H8474 | BDB3107 | H2734 | חָרָה | igen | burn | 2 |
| H8479 | BDB9998 | H8460,H8478 | תְּחוֺת | igen | under | 0 |
| H8499 | BDB3954 | H8498,H4349 | תְּכוּנָה | igen | arrangement | 1 |
| H8501 | BDB9151 | H8496 | תֹּךְ | igen | injury | 0 |
| H8517 | BDB9999 | H7950 | תְּלַג | igen | snow | 1 |
| H8543 | BDB9188 | H0865,H8032,H8008 | תְּמוֺל | igen | yesterday | 23 |
| H8550 | BDB9190 | H8537,H0224,H8549 | תֹּם | igen | Thummim | 5 |
| H8625 | BDB9673 | H4484,H4487,H6537 | מְנֵא | igen | weigh | 3 |
| H8627 | BDB10014 | H8626 | תְּקַן | igen | be in order | 1 |
| H8631 | BDB10015 | H8630 | תְּקֵף | igen | grow strong | 5 |
| H8637 | BDB7744 | H7270 | רָגַל | igen | foot it | 1 |
| H8651 | BDB10020 | H8179 | תְּרַע | igen | gate | 2 |
