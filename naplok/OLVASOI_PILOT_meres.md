<!-- GENERÁLT: eszkozok/olvaso_pilot/meres.py — kézzel nem szerkesztendő. -->
# Olvasói pilot — mérés (F60.2, bővítve: F60.5)

*Gép által generált (`eszkozok/olvaso_pilot/meres.py`), kézzel nem szerkesztendő; a #60 M2 lépése. Mért adatállapot: repó-commit `94f68d91` (az `ág: claude/olvasoi-pilot` feje a mérés előtt), a szakasz-adatok `ts` ideje: 1Móz 1–25 2026-10-12T15:11Z, Zsolt 22 2026-10-12T15:12Z.*

A pilot az aktuális adatállapotot méri (a #7, #9, #22, #38, #54, #56, #57 lezárása után újrafuttatható). A számok a pilot-oldalra kerülő adatot jellemzik, nem a repó egészét.

## 1. A Károli-szavak kötése héber szóhoz

- `scope=1Móz 1–25 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| Károli-szó (írásjelekkel együtt, szótoken) | 12961 | 407 |
| kötött tartalmas héber szóhoz (kattintható, szó-lappal) | 7617 (58.8%) | 243 (59.7%) |
| — ebből „magas” bizonyosság | 7502 (98.5% a kötöttekből) | 0 (0.0% a kötöttekből) |
| — ebből nem „magas” (alacsony) | 115 (1.5% a kötöttekből) | 243 (100.0% a kötöttekből) |
| csak nyelvtani elemhez kötött (nincs szó-lap) | 3215 (24.8%) | 92 (22.6%) |
| párosítás nélkül | 2129 (16.4%) | 72 (17.7%) |

## 2. Héber szó-lapok: BDB-szócikk

- `scope=1Móz 1–25 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| héber szó-lap (nem nyelvtani Strong-szám) | 1075 | 159 |
| van magyar BDB-szócikk | 439 (40.8%) | 112 (70.4%) |
| csak angol BDB-szócikk | 624 (58.0%) | 47 (29.6%) |
| egyik sincs (csak a Strong-szótár rövid jelentése) | 12 (1.1%) | 0 (0.0%) |

- 1Móz 1–25: BDB-szócikk nélküli szó-lapok: H0553, H1746, H3231, H3252, H4138, H4176, H5503, H5668, H5745, H6820, H7742, H8646
- 1Móz 1–25: a saját szócikk nélküli, de a BDB_strong_alias.tsv szerint másik Strong-szám alatt álló szó-lapok (az alias-szócikk a lapon jelezve; a fenti számokban a magyar/angol sorban szerepelnek): H0085, H0121, H0136, H0341, H0763, H2962, H3069, H3866, H5227, H5978, H6255, H6565, H7019, H7358, H7535
- Zsolt 22: a saját szócikk nélküli, de a BDB_strong_alias.tsv szerint másik Strong-szám alatt álló szó-lapok (az alias-szócikk a lapon jelezve; a fenti számokban a magyar/angol sorban szerepelnek): H0136, H7358

## 3. BDB-bontás (gépi szeletelés)

- `scope=1Móz 1–25 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| legalább 2 jelentésre bomlik | 531 (49.4%) | 123 (77.4%) |
| egyben marad (1 számozott jelentés) | 34 (3.2%) | 2 (1.3%) |
| nincs számozott jelentés a szeletelésben (0) | 510 (47.4%) | 34 (21.4%) |

- 1Móz 1–25, egyben maradó szócikkek (34): H0213 אוּץ, H0567 אֱמֹרִי, H1323 בַּת, H1581 גָּמָל, H2009 הִנֵּה, H2416 חַי, H2506 חֵ֫לֶק, H2820 חָשַׂךְ, H2962 טֶ֫רֶם, H3458 יִשְׁמָעֵאל, H3533 כָּבַשׁ, H3644 כְּמוֹ, H3682 כְּסוּת, H3967 מֵאָה, H4116 מָהַר, H4376 מָכַר, H4705 מִצְעָר, H4714 מִצְרַ֫יִם, H5002 נְאֻם, H5030 נָבִיא, H5310 נָפַץ, H6113 עָצַר, H6153 עֶ֫רֶב, H6926 קִדְמָה, H7287 רָדָה, H7390 רַךְ, H7535 רַק, H7969 שָׁלֹשׁ, H8083 שְׁמֹנֶה, H8159 שָׁעָה, H8337 שֵׁשׁ, H8415 תְּהוֹם, H8449 תֹּר, H8672 תֵּ֫שַׁע
- 1Móz 1–25, számozott jelentés nélkül (510): H0014 אָבָה, H0028 אֲבִידָע, H0039 אֲבִימָאֵל, H0040 אֲבִימֶ֫לֶךְ, H0061 אֲבָל, H0085 אַבְרָהָם, H0087 אַבְרָם, H0108 אֵד, H0110 אַדְבְּאֵל, H0122 אֱדֹם, H0123 אֱדוֹם, H0126 אַדְמָה, H0132 אַדְמוֹנִי, H0167 אָהַל, H0182 אוֹדָה, H0187 אוּזָל, H0218 אוּר, H0226 אוֹת, H0251 אָח, H0272 אֲחֻזָּה, H0312 אַחֵר, H0322 אֲחֹרַנִּית, H0339 אִי, H0341 אֹיֵב, H0342 אֵיבָה, H0346 אַיֵּה, H0352 אַ֫יִל, H0364 אֵיל פָּארָן, H0367 אֵימָה, H0368 אֵימִים, H0376 אִישׁ, H0390 אַכַּד, H0400 אֹ֫כֶל, H0402 אׇכְלָה, H0408 אַל, H0411 אֵל, H0420 אֶלְדָּעָה, H0428 אֵ֫לֶּה, H0436 אֵלוֹן, H0461 אֱלִיעֶ֫זֶר, H0473 אֱלִישָׁה, H0486 אַלְמוֹדָד, H0495 אֶלָּסָר, H0505 אֶ֫לֶף, H0523 אֻמָּה, H0546 אׇמְנָה, H0552 אֻמְנָם, H0553 אָמֵץ, H0565 אִמְרָה, H0569 אַמְרָפֶל, H0570 אֶ֫מֶשׁ, H0575 אָן, H0583 אֱנוֹשׁ, H0587 אֲנַ֫חְנוּ, H0589 אֲנִי, אָֽנֹכִ֫י, H0595 אָֽנֹכִ֫י, H0644 אָפָה, H0665 אֵ֫פֶר, H0699 אֲרֻבָּה, H0721 אַרְוָדִי, H0746 אַרְיוֹךְ, H0751 אֶ֫רֶךְ, H0753 אֹ֫רֶךְ, H0761 אֲרַמִּי, H0775 אַרְפַּכְשַׁד, H0779 אָרַר, H0780 אֲרָרַט, H0805 אַשּׁוּרִם, H0812 אֶשְׁכֹּל, H0813 אַשְׁכְּנַז, H0815 אֵ֫שֶׁל, H0859 אַתָּ֫ה, H0860 אָתוֹן, H0883 בְּאֵר לַחַי רֹאִי, H0884 בְּאֵר שֶׁ֫בַע, H0894 בָּבֶ֫ל, בָּבֶל, H0916 בְּדֹ֫לַח, H0922 בֹּהוּ, H0938 בּוּז, H1062 בְּכֹרָה, H1067 בְּכִירָה, H1086 בָּלָה, H1106 בֶּ֫לַע, H1107 בִּלְעֲדֵי, H1151 בֶּן־עַמִּי, H1219 בָּצַר, H1235 בֶּ֫קַע, H1298 בֶּ֫רַע, H1306 בִּרְשַׁע, H1328 בְּתוּאֵל, H1330 בְּתוּלָה, H1334 בָּתַר, H1404 גְּבֶ֫רֶת, H1419 גַּל, H1469 גּוֹזָל, H1478 גָּוַע, H1497 גָּזַל, H1506 גֶּ֫זֶר, H1512 גָּחוֹן, H1514 גַּ֫חַם, H1558 גָּלָל, H1572 גָּמָא, H1586 גֹּ֫מֶר, H1588 גַּן, H1613 גֹּ֫פֶר, H1614 גׇּפְרִית, H1622 גִּרְגָּשִׁי, H1642 גְּרָר, H1644 גָּרַשׁ, H1653 גֶּ֫שֶׁם, H1666 גֶּ֫תֶר, H1696 דָבַר, H1709 דָּג, H1710 דָּגָה, H1721 רוֹדָנִים, H1746 דּוּמָה, H1834 דַּמֶּ֫שֶׂק, H1853 דִּקְלָה, H1863 דַּרְדַּר, H1876 דָּשָׁא, H1877 דֶּ֫שֶׁא, H1893 הֶ֫בֶל, H1904 הָגָר, H1913 הֲדוֹרָם, H1973 הָֽ֫לְאָה, H1976 הַלָּזֶה, H1984 הָלַל, H1988 הֲלֹם, H1990 הָ֑ם, H2007 הֵנָּה, H2008 הֵ֫נָּה, H2018 הֲפֵכָה, H2030 הָרָה, H2032 הֵרָיוֹן, H2056 וָלָד, H2091 זָהָב, H2104 זוּזִים, H2145 זָכָר, H2175 זִמְרָן, H2188 זֵעָה, H2204 זָקֵן, H2208 זְקֻנִים, H2209 זִקְנָה, H2250 חַבּוּרָה, H2290 חֲגוֹרָה, H2301 חֲדַד, H2313 חִדֶּ֫קֶל, H2327 חוֹבָה, H2332 חַוָּה, H2343 חוּל, H2344 חוֹל, H2375 חֲזוֹ, H2400 חַטָּא, H2436 חֵיק, H2461 חָלָב, H2472 חֲלוֹם, H2474 חַלּוֹן, H2486 חָלִ֫ילָה, H2490 חָלַל, H2527 חֹם, H2529 חֶמְאָה, H2530 חָמַד, H2551 חֶמְלָה, H2555 חָמָס, H2564 חֵמָר, H2573 חֵ֫מֶת, H2577 חֲמָתִי, H2585 חֲנוֹךְ, H2593 חָנִיךְ, H2688 חַצֲצֹן תָּמָר, H2700 חֲצַרְמָ֫וֶת, H2724 חָֽרָבָה, H2771 חָרָן, H2779 חֹ֫רֶף, H2825 חֲשֵׁכָה, H2844 חַת, H2845 חֵת, H2875 טֶ֫בַח, H2909 טָחָה, H2965 טָרָף, H2983 יְבוּסִי, H2989 יָבָל, H3004 יַבָּשָׁה, H3044 יִדְלָ֑ף, H3106 יוּבָ֑ל, H3120 יָוָן, H3123 יוֹנָה, H3196 יַ֫יִן, H3206 יֶ֫לֶד, H3211 יָלִיד, H3220 יָם, H3231 יָמַן, H3243 יָנַק, H3252 יִסְכָּה, H3303 יָפֶה, H3315 יֶ֫פֶת, H3327 יִצְחָק, H3351 יְקוּם, H3355 יׇקְטָן, H3364 יָקַץ, H3370 יׇקְשָׁן, H3373 יָרֵא, H3382 יֶ֫רֶד, H3383 יַרְדֵּן, H3392 יֶ֫רַח, H3418 יֶ֫רֶק, H3435 יִשְׁבָּק, H3462 יָשֵׁן, H3535 כִּבְשָׂה, H3536 כִּבְשָׁן, H3537 כַּד, H3540 כְּדׇרְלָעֹמֶר, H3556 כּוֹכָב, H3568 כּוּשׁ, H3625 כֶּ֫לַח, H3641 כַּלְנֵ֑ה, H3658 כִּנּוֹר, H3695 כַּסְלֻחִים, H3701 כֶּ֫סֶף, H3732 כַּפְתֹּרִי, H3754 כֶּרֶם, H3777 כֶּ֫שֶׂד, H3778 כַּשְׂדִּים, H3794 כִּתִּי, H3801 כֻּתֹּ֫נֶת, H3811 לָאָה, H3816 לְאֹם, H3817 לְאֻמִּ֑ים, H3837 לָבָן, H3853 לְהָבִים, H3858 לַ֫הַט, H3865 לוּד, H3866 לוּדִי, H3876 לוֹט, H3885 לוּן, H3888 לוּשׁ, H3912 לְטוּשִׁם, H3938 לָעַט, H3940 לַפִּיד, H3962 לֶ֫שַׁע, H3972 מְא֫וּמָה, H3974 מָאוֹר, H3978 מַאֲכָל, H3979 מַאֲכֶ֫לֶת, H3999 מַבּוּל, H4005 מִבְחָר, H4017 מִבְשָׂם, H4030 מִגְדָּנָה, H4031 מָגוֹג, H4033 מָגוֹר, H4042 מָגַן, H4043 מָגֵן, H4080 מִדְיָן, H4091 מְדָן, H4102 מָהַהּ, H4135 מוּל, H4138 מוֹלֶ֫דֶת, H4176 מוֹרֶה, H4179 מֹרִיָּה, H4232 מְחוּיָאֵל, H4236 מַחֲזֶה, H4283 מׇחֳרָת, H4305 מָטַר, H4310 מִי, H4327 מִין, H4375 מַכְפֵּלָה, H4392 מָלֵא, H4417 מֶ֫לַח, H4421 מִלְחָמָה, H4442 מַלְכִּי־צֶ֫דֶק, H4448 מָלַל, H4554 מִסְפּוֹא, H4599 מַעְיָן, H4601 מַעֲכָה, H4631 מְעָרָה, H4682 מַצָּה, H4723 מִקְוֶה, H4735 מִקְנֶה, H4808 מְרִיבָה, H4851 מַשׁ, H4852 מֵשָׁא, H4854 מַשָּׂא, H4902 מֶ֫שֶׁךְ, H4943 מֶ֫שֶׁק, H4948 מִשְׁקָל, H4967 מְתוּשָׁאֵל, H4968 מְתוּשֶׁ֫לַח, H4979 מַתָּנָה, H5032 נְבָיוֹת, H5066 נָגַשׁ, H5113 נוֹד, H5138 נָזִיד, H5146 נֹחַ, H5148 נָחָה, H5207 נִיחֹחַ, H5209 נִין, H5210 נִינְוֵה, H5220 נֶ֫כֶד, H5236 נֵכָר, H5271 נְעוּרִים, H5275 נַ֫עַל, H5279 נַעֲמָה, H5288 נַ֫עַר, H5301 נָפַח, H5303 נְפִלִים, H5305 נָפִישׁ, H5320 נַפְתֻּחִים, H5375 נָשָׂא, H5377 נָשָׁא, H5380 נָשַׁב, H5429 סְאָה, H5434 סְבָא, H5442 סְבַךְ, H5454 סַבְתָּה, H5455 סַבְתְּכָא, H5467 סְדֹם, H5503 סָחַר, H5513 סִינִי, H5534 סָכַר, H5560 סֹ֫לֶת, H5575 סַנְוֵרִים, H5594 סָפַד, H5611 סְפָר, H5668 עָבוּר, H5692 עֻגָה, H5697 עֶגְלָה, H5711 עָדָה, H5713 עֵדָה, H5730 עֶדְנָה, H5731 עֵ֫דֶן, H5742 עֲדָשָׁה, H5745 עוֹבָל, H5748 עוּגָב, H5780 עוּץ, H5804 עַזָּה, H5861 עַ֫יִט, H5880 עֵין מִשְׁפָּט, H5889 עָיֵף, H5891 עֵיפָה, H5893 עִיר, H5897 עִירָד, H5929 עָלֶה, H5930 עֹלָה, H5939 עֲלָטָה, H5945 עֶלְיוֹן, H5959 עַלְמָה, H5983 עַמּוֹן, H6003 עֲמָלֵקִי, H6010 עֵ֫מֶק, H6017 עֲמֹרָה, H6031 עָנָה, H6047 עֲנָמִים, H6049 עָנַן, H6063 עָנֵר, H6086 עֵץ, H6087 עָצַב, H6093 עִצָּבוֹן, H6119 עָקֵב, H6123 עָקַד, H6135 עָקָר, H6158 עֹרֵב, H6174 עָרוֹם, H6185 עֲרִירִי, H6189 עָרֵל, H6190 עׇרְלָה, H6208 עַרְקִי, H6212 עֵ֫שֶׂב, H6215 עֵשָׂו, H6238 עָשַׁר, H6255 עַשְׁתְּרֹת קַרְנַיִם, H6279 עָתַר, H6290 פָּארָן, H6307 פַּדָּן, H6316 פּוּט, H6369 פִּיכֹל, H6376 פִּישׁוֹן, H6385 פָּלַג, H6389 פֶּ֫לֶג, H6394 פִּלְדָּשׁ, H6412 פָּלִיט, H6430 פְּלִשְׁתִּי, H6482 פֶּ֫צַע, H6484 פָּצַר, H6501 פֶּ֫רֶא, H6522 פְּרִזִּי, H6547 פַּרְעֹה, H6565 פָּרַר, H6578 פְּרָת, H6595 פַּת, H6607 פֶּ֫תַח, H6625 פַּתְרֻסִים, H6636 צְבֹיִים, H6654 צַד, H6672 צֹ֫הַר, H6680 צָוָה, H6712 צְחֹק, H6714 צֹ֫חַר, H6721 צִידוֹן, H6741 צִלָּה, H6781 צָמִיד …(+110)
- 1Móz 1–25, bomló szócikkek (531), jelentésszám szerint csökkenően: H6965 קוּם (32), H5927 עָלָה (23), H7725 שׁוּב (22), H3947 לָקַח (20), H2388 חָזַק (19), H6942 קָדַשׁ (17), H1980 הָלַךְ (16), H5307 נָפַל (16), H2142 זָכַר (15), H3772 כָּרַת (15), H0398 אָכַל (14), H4196 מִזְבֵּחַ (14), H5975 עָמַד (13), H7971 שָׁלַח (13), H2398 חָטָא (12), H6213 עָשָׂה (12), H0216 אוֹר (11), H1288 בָּרַךְ (11), H2505 חָלַק (11), H2803 חָשַׁב (11), H3045 יָדַע (11), H3513 כָּבֵד (11), H4191 מוּת (11), H4672 מָצָא (11), H5221 נָכָה (11) …
- Zsolt 22, egyben maradó szócikkek (2): H1518 גִּיחַ, H3119 יוֹמָם
- Zsolt 22, számozott jelentés nélkül (34): H0251 אָח, H0355 אַיָּלָה, H0360 אֱיָלוּת, H0376 אִישׁ, H0408 אַל, H0595 אָֽנֹכִ֫י, H0657 אֶ֫פֶס, H0738 אַרְיֵה, H0859 אַתָּ֫ה, H1316 בָּשָׁן, H1556 גָּלַל, H1732 דָּוִד, H1747 דּוּמִיָּה, H1749 דּוֹנַג, H1879 דָּשֵׁן, H1984 הָלַל, H2963 טָרַף, H3373 יָרֵא, H3611 כֶּ֫לֶב, H3803 כָּתַר, H3830 לְבוּשׁ, H3932 לָעַג, H4210 מִזְמוֹר, H4410 מְלוּכָה, H4455 מַלְקוֹחַ, H5362 נָקַף, H5826 עָזַר, H6039 עֱנוּת, H6869 צָרָה, H7214 רְאֵם, H7227 רַב, H7768 שָׁוַע, H7837 שַׁ֫חַר, H8432 תָּ֫וֶךְ
- Zsolt 22, bomló szócikkek (123), jelentésszám szerint csökkenően: H7725 שׁוּב (22), H5307 נָפַל (16), H2142 זָכַר (15), H0398 אָכַל (14), H6213 עָשָׂה (12), H2505 חָלַק (11), H3513 כָּבֵד (11), H5437 סָבַב (11), H5647 עָבַד (11), H7999 שָׁלֵם (11), H3820 לֵב (10), H3824 לֵבָב (10), H4422 מָלַט (10), H5315 נֶ֫פֶשׁ (10), H7200 רָאָה (10), H0001 אָב (9), H1697 דָּבָר (8), H3381 יָרַד (8), H3427 יָשַׁב (8), H5337 נָצַל (8), H5608 סָפַר (8), H6440 פָּנֶה (8), H7121 קָרָא (8), H0410 אֵל (7), H1961 הָיָה (7) …

## 4. Görög szó-lapok

- `scope=1Móz 1–25 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire, és minden görög szó, amelyre egy héber szó-lap a lxx_bridge-ből hivatkozik | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire, és minden görög szó, amelyre egy héber szó-lap a lxx_bridge-ből hivatkozik | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| görög szó-lap | 1230 | 305 |
| van magyar jelentés (adat/forditasok.tsv: Thayer / UBS_DNTG) | 8 (0.7%) | 3 (1.0%) |
| van újszövetségi előfordulás (TAGNT) | 1174 (95.4%) | 287 (94.1%) |
| van héber háttér (lxx_bridge) | 999 (81.2%) | 287 (94.1%) |
| van TBESG szótári szöveg (angol) | 1230 (100.0%) | 305 (100.0%) |

## 5. A görög szóalak forrása

- `scope=1Móz 1–25 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| héber szó (TAHOT-sor, a nyelvtani elemekkel együtt) | 14142 | 389 |
| nincs Macula-párja (a görög megfelelő nem is képezhető) | 49 (0.3%) | 1 (0.3%) |
| Macula-párral rendelkező szó | 14093 | 388 |
| — van görög megfelelője | 11307 (80.2%) | 324 (83.5%) |
| — a szóalak az LXX_OS-ből (egyezés Strong-szám + alak szerint) | 8967 (79.3% a görögből) | 222 (68.5% a görögből) |
| — a szóalak a Maculából marad (nincs LXX_OS-egyezés) | 1136 (10.0% a görögből) | 60 (18.5% a görögből) |
| — ebből χ vagy ξ van a Macula-alakban (a Macula-oszlop χ/ξ-hibás) | 26 | 2 |
| — nincs görög megfelelő (a Macula `gorog_lxx` üres) | 2786 | 64 |
| Macula-alak ≠ LXX_OS-alak (ékezet és hehezet nélkül) | 354 | 14 |
| — ebből a χ/ξ felcserélése magyarázza | 302 | 11 |

## 6. UBS-jelentés lefedettsége, versszámozás

- `scope=1Móz 1–25 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| nem nyelvtani héber szó-előfordulás | 7616 | 218 |
| — van UBS-jelentés-besorolás (előfordulásonként) | 6866 (90.2%) | 200 (91.7%) |
| különböző héber szó-lap | 1075 | 159 |
| — legalább egy előfordulásához van UBS-jelentés | 1049 (97.6%) | 153 (96.2%) |
| vers a szakaszban | 693 | 32 |
| — a versmegfeleltető tábla szerint nincs KJV-megfelelő | 0 | 1 |
| — nincs LXX-szó a versre (LXX_OS) | 0 | 0 |
| — a tábla KJV- vagy MT-száma eltér a Károli-számtól | 0 | 0 |
| — a versmegfeleltető tábla és az LXX_OS saját KJV-oszlopa ellentmond | 0 | 31 |

- Zsolt 22, nincs KJV-megfelelő: Zsolt 22:32
- Zsolt 22, a két tábla KJV-száma ellentmond: Zsolt 22:2, Zsolt 22:3, Zsolt 22:4, Zsolt 22:5, Zsolt 22:6, Zsolt 22:7, Zsolt 22:8, Zsolt 22:9, Zsolt 22:10, Zsolt 22:11, Zsolt 22:12, Zsolt 22:13, Zsolt 22:14, Zsolt 22:15, Zsolt 22:16, Zsolt 22:17, Zsolt 22:18, Zsolt 22:19, Zsolt 22:20, Zsolt 22:21, Zsolt 22:22, Zsolt 22:23, Zsolt 22:24, Zsolt 22:25, Zsolt 22:26, Zsolt 22:27, Zsolt 22:28, Zsolt 22:29, Zsolt 22:30, Zsolt 22:31, Zsolt 22:32

## 7. A bővítés (F60.5, v2): a meglévő adatok megjelenítésének mérése

A bővítés új adatot nem állít elő: minden érték egy meglévő tábla sora; a gépi feldolgozás (kulcs-illesztés, tartomány bontása, morf-kód feloldása) jelölt. A teljes adatkészlet-felmérés: `naplok/OLVASOI_PILOT_adatfelmeres.md`.

### 7.1 Szó-lapok (Strong-kulcs)

- `scope=1Móz 1–25 | forras=konkordancia/{SDBH_domenek,SDGNT_domenek,SECE_H_teljes,SECE_G_teljes,OSHL_lexikalis_index,LSJ_teljes,MCGED_teljes,UBS_DNTG_jelentesek,tW_szocikkek}.tsv + TBESH.txt; szó-lapok: adat.py → bovites.py | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=konkordancia/{SDBH_domenek,SDGNT_domenek,SECE_H_teljes,SECE_G_teljes,OSHL_lexikalis_index,LSJ_teljes,MCGED_teljes,UBS_DNTG_jelentesek,tW_szocikkek}.tsv + TBESH.txt; szó-lapok: adat.py → bovites.py | ts=2026-10-12T15:11Z`

| Mérőszám (a szakasz szó-lapjai közül) | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| héber: SDBH-domén | 1054/1075 (98.0%) | 154/159 (96.9%) |
| héber: SECE_H-szócikk | 1075/1075 (100.0%) | 159/159 (100.0%) |
| héber: OSHL (TWOT, BDB-azonosító) | 1074/1075 (99.9%) | 159/159 (100.0%) |
| héber: TBESH-szócikk | 1075/1075 (100.0%) | 159/159 (100.0%) |
| héber: tW-szócikk | 491/1075 (45.7%) | 124/159 (78.0%) |
| görög: SDGNT-domén | 1173/1230 (95.4%) | 283/305 (92.8%) |
| görög: UBS_DNTG angol jelentések | 1173/1230 (95.4%) | 283/305 (92.8%) |
| görög: LSJ-szócikk | 1229/1230 (99.9%) | 305/305 (100.0%) |
| görög: MCGED (Mounce) | 1200/1230 (97.6%) | 295/305 (96.7%) |
| görög: SECE_G-szócikk | 1230/1230 (100.0%) | 305/305 (100.0%) |
| görög: tW-szócikk | 488/1230 (39.7%) | 141/305 (46.2%) |
| görög: ÚSZ-hely UBS_DNTG-besorolása (a lapon listázott helyek) | 4665/4853 (96.1%) | 1218/1304 (93.4%) |

### 7.2 Vers-lapok (vers-kulcs)

- `scope=1Móz 1–25 | forras=konkordancia/{BSB_Strongs,KJV_Strongs_teljes,Nave_basokant,TIPNR_kivonat,LXX_versszintu_parok,LXX_tobblet_szakaszok,Verzifikacios_elteres_tabla}.tsv + adat/{elofordulasok,kapcsolatok,lxx_dontesek,motivumok}.tsv; vers-kulcs: eszkozok/olvaso_pilot/bovites.py (gépi illesztés) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=konkordancia/{BSB_Strongs,KJV_Strongs_teljes,Nave_basokant,TIPNR_kivonat,LXX_versszintu_parok,LXX_tobblet_szakaszok,Verzifikacios_elteres_tabla}.tsv + adat/{elofordulasok,kapcsolatok,lxx_dontesek,motivumok}.tsv; vers-kulcs: eszkozok/olvaso_pilot/bovites.py (gépi illesztés) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| vers, amelyhez van BSB-sor (MT-kulcs) | 693/693 (100.0%) | 30/32 (93.8%) |
| BSB-szó összesen (ebből „elhagyva” állapotú) | 8996 (1225) | 232 (4) |
| BSB „Számozás” oszlop értékei a pilot-versekre | ellenorizetlen, mt | mt |
| vers, amelyhez van KJV-sor (KJV-kulcs) | 693/693 (100.0%) | 32/32 (100.0%) |
| KJV-szó összesen | 6758 | 196 |
| a KJV-kulcs forrása | LXX_OS KJV-oszlop: 693 | LXX_OS KJV-oszlop: 31; a fejezet eltolása (nincs LXX-szó a versre): 1 |
| a versmegfeleltető tábla KJV-száma eltér a KJV-kulcstól (vers) | 0 | 31 |
| vers, amelyhez van Nave-sor (vers- és tartományhivatkozás) | 683/693 (98.6%) | 31/32 (96.9%) |
| Nave-sor a versekre összesen (ebből tartományból bontva); fejezet-szintű sor | 4461 (2769); 54 | 130 (64); 8 |
| TIPNR: vers névvel; a szakasz TIPNR-sorai közül illesztve | 444 vers; 1060/1064 (99.6%) | 7 vers; 9/9 (100.0%) |
| adat/elofordulasok.tsv: sor a szakasz verseire | 41 | 0 |
| adat/kapcsolatok.tsv: sor a szakasz verseire | 20 | 0 |
| adat/lxx_dontesek.tsv: sor a szakasz verseire | 27 | 0 |
| LXX versszintű együttelőfordulás: vers; pár | 337/693 (48.6%); 4866 | 4/32 (12.5%); 31 |
| LXX_tobblet_szakaszok / Verzifikacios_elteres_tabla: sor | 0 / 0 | 0 / 0 |

### 7.3 Morfológia és méret

- `scope=1Móz 1–25 | forras=adat/morf_kulcs_heber.tsv + adat/morf_nyelv_aramai.tsv; Macula-kód: konkordancia/Macula_heber_*.tsv; feldolgozás: eszkozok/olvaso_pilot/bovites.py (gépi feldolgozás) | ts=2026-10-12T15:11Z`
- `scope=Zsolt 22 | forras=adat/morf_kulcs_heber.tsv + adat/morf_nyelv_aramai.tsv; Macula-kód: konkordancia/Macula_heber_*.tsv; feldolgozás: eszkozok/olvaso_pilot/bovites.py (gépi feldolgozás) | ts=2026-10-12T15:11Z`

| Mérőszám | 1Móz 1–25 | Zsolt 22 |
|---|---|---|
| Macula-szó morfológiai kóddal, ebből magyarul feloldva (a nyers kód mellett marad) | 14093/14093 (100.0%) | 388/388 (100.0%) |
| ismeretlen jelű kód (a jelkulcs nem oldja fel) | 0 | 0 |
| arámi szó a szakaszban (adat/morf_nyelv_aramai.tsv) | 0 | 0 |
| olvaso_pilot.json mérete (bájt) | 33 712 997 | 6 403 526 |
| karoli_konkordancia_proba.html mérete (bájt; egyetlen fájl, minden adat beágyazva) | 10 204 234 | 2 538 866 |

A legnagyobb HTML 10 204 234 bájt, vagyis átlépte a 8 MB-ot: lusta betöltésre vagy külön JSON-ra kell áttérni.

