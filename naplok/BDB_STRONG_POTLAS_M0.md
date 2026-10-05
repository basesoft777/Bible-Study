# BDB_STRONG_POTLAS M0 — felmérés (F57)

*Generálta: `python eszkozok/bdb_strong_potlas.py --m0` · proveniencia: scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/BDB_teljes_unabridged.tsv + konkordancia/OSHL_lexikalis_index.tsv + konkordancia/TAHOT_kivonat.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=2026-10-05*

## 1. A BDB.lexicon szerkezete

- SQLite, egyetlen `Lexicon` tábla (`Topic`, `Definition`); `Topic` háromféle: `BDB####` (10022 szócikk), `H<n>` (8619 Strong-kulcs), `info` (1).
- A szócikk fejlécében (`<h1>`) a Strong-címke `<entry onclick="lex('H…')">` alakban áll; egy szócikknek 0, 1 vagy több címkéje lehet. A `H<n>` kulcs a szócikket a *saját* címkéi alatt adja vissza.
- Nyelv: a navigációs sorban `BIBLICAL HEBREW` / `BIBLICAL ARAMAIC` (9263 / 759).

## 2. Címke nélküli BDB-szócikkek

- BDB-azonosítós szócikk: 10022; ebből címkével: 9176; **címke nélkül: 846** (heber 831, arámi 15).
- Ebből szófaj nélküli gyök-hivatkozás ("√ of following"): 615.

| BDB-azonosító | nyelv | homonímaszám | címszó | szófaj | első glossza | gyök-hivatkozás |
|---|---|---|---|---|---|---|
| BDB2 | heber | — | אבב | — | fresh, bright |  |
| BDB16 | heber | II | אבה | — | abû | igen |
| BDB47 | heber | — | אבח | — | abâµu |  |
| BDB53 | heber | II | אבל | — | grow green | igen |
| BDB56 | heber | III | אבל | — | able to manage camels |  |
| BDB64 | heber | — | אבץ | — | — |  |
| BDB67 | heber | — | אבק | — | run away |  |
| BDB71 | heber | — | אבר | — | abâru |  |
| BDB78 | heber | — | אגא | ** | flee |  |
| BDB82 | heber | — | אגד | ** | bind |  |
| BDB85 | heber | — | אגל | — | restrict |  |
| BDB88 | heber | — | אגם | ** | troubled, sad |  |
| BDB92 | heber | — | אגן | — | circular, round |  |
| BDB94 | heber | — | אגף | — | agappu, wing |  |
| BDB97 | heber | II | אגר | — | pay, hire |  |
| BDB103 | heber | — | אדד | — | strength |  |
| BDB107 | heber | I | אדם | — | adâmu |  |
| BDB112 | heber | II | אדם | — | tawny |  |
| BDB123 | heber | — | אדן | — | adannu |  |
| BDB147 | heber | — | אהד | — | — |  |
| BDB153 | heber | I | אהל | ** | settle down |  |
| BDB165 | heber | — | אוב | — | return |  |
| BDB168 | heber | — | אוד | — | be curved, bent |  |
| BDB173 | heber | I | אוה | 1. | betake oneself |  |
| BDB187 | heber | III | אוה | — | to cry |  |
| BDB192 | heber | I | אול | — | be foolish |  |
| BDB196 | heber | II | אול | ** | be in front of, precede, lead |  |
| BDB222 | heber | I | און | ** | be fatigued, tired |  |
| BDB225 | heber | II | און | — | be at rest, at ease, enjoy life of plenty |  |
| BDB232 | heber | — | אוניות | — | — |  |
| BDB255 | heber | — | מֵאָז | — | from that time: |  |
| BDB262 | heber | I | אזן | — | pointed, sharp |  |
| BDB284 | heber | — | אחה | — | surround, protect |  |
| BDB323 | heber | I | אחח | — | cry, howl |  |
| BDB325 | heber | II | אחח | — | — |  |
| BDB330 | heber | — | אחל | — | — |  |
| BDB338 | heber | — | אָדָם אַחֲרַי | — | afterwards |  |
| BDB350 | heber | — | אטד | — | make firm, strong |  |
| BDB352 | heber | — | אטט | — | to emit a moaning |  |
| BDB353 | heber | — | אִטִּי | noun masculine | mutterer, plural |  |
| BDB380 | heber | — | אָים | — | terrify |  |
| BDB388 | heber | — | אישׁ | — | inš | igen |
| BDB410 | heber | — | אכר | — | dig, till |  |
| BDB412 | heber | I | אַל | — | algebra, Alhambra, alkali, alcohol, alcove |  |
| BDB427 | heber | I | אלה | 1. a. | god, God |  |
| BDB482 | heber | I | אלל | — | to be weak |  |
| BDB485 | heber | II | אלל | — | — | igen |
| BDB512 | heber | — | אמה | — | — | igen |
| BDB519 | heber | I | אמם | — | be wide, roomy |  |
| BDB547 | heber | II | אָמַן | — | — |  |
| BDB574 | heber | — | אנב | — | spring, leap |  |
| BDB580 | heber | II | אנה | — | ânu, unûtu | igen |
| BDB585 | heber | — | תֹּאֲנָה | noun feminine | opportunity |  |
| BDB608 | heber | II | אנשׁ | — | be inclined to |  |
| BDB611 | heber | III | אנשׁ | — | soft, delicate |  |
| BDB613 | heber | — | אנת | — | anta |  |
| BDB619 | heber | I | אסה | — | heal |  |
| BDB621 | heber | II | אסה | — | — |  |
| BDB623 | heber | — | אסם | — | gather, store |  |
| BDB631 | heber | — | אָסֹף | noun [masculine] | what is gathered, store |  |
| BDB637 | heber | — | אֵסוּר | noun masculine | band, bond |  |
| BDB643 | heber | — | מוֺסֵר | noun masculine | band, bond |  |
| BDB650 | heber | — | אַף כִּי | 1. | furthermore |  |
| BDB651 | heber | — | אפד | — | gird on | igen |
| BDB661 | heber | — | אפל | — | disappear, depart, set |  |
| BDB668 | heber | — | אפן | — | turn |  |
| BDB682 | heber | I | אפר | — | leap |  |
| BDB684 | heber | II | אפר | — | enclose, envelope | igen |
| BDB690 | heber | — | אפת | ** | calamity |  |
| BDB693 | heber | — | אצל | — | to join |  |
| BDB702 | heber | — | אצם | — | be angry |  |
| BDB739 | heber | II | ארה | — | burn |  |
| BDB754 | heber | — | אֲרִיסַי | proper name, masculine | son of Haman |  |
| BDB765 | heber | — | ארם | — | — | igen |
| BDB768 | heber | I | ארן | — | alacer, laetus fuit | igen |
| BDB776 | heber | II | ארן | — | êrû | igen |
| BDB786 | heber | — | ארשׁ | — | to desire, request |  |
| BDB800 | heber | — | אשׁד | — | išdu | igen |
| BDB806 | heber | — | אשׁה | — | support | igen |
| BDB808 | heber | — | אָשְׁיָה | noun feminine | wall, bulwark |  |
| BDB819 | heber | — | אשׁל | — | be firm, firmly rooted |  |
| BDB825 | heber | — | אשׁן | — | be hard, firm | igen |
| BDB828 | heber | — | אשׁף | — | — | igen |
| BDB862 | heber | — | אתן | — | take short steps |  |
| BDB868 | heber | — | אתת | — | — | igen |
| BDB873 | heber | II | בְּ | proper name | — |  |
| BDB915 | heber | II | בדד | — | id quod |  |
| BDB925 | heber | — | בדק | — | penetrate, split |  |
| BDB928 | heber | — | בָּדַק | verb denominative | mend fissures |  |
| BDB930 | heber | — | בהה | — | be empty |  |
| BDB935 | heber | — | בהם | — | shut |  |
| BDB938 | heber | — | בהן | — | shut, cover |  |
| BDB941 | heber | — | בהק | — | shine |  |
| BDB943 | heber | — | בהר | — | be bright, shine |  |
| BDB969 | heber | — | בוע | — | efferbuit et commotus fuit | igen |
| BDB971 | heber | — | בוץ | — | surpass in whiteness |  |
| BDB974 | heber | — | בוק | — | — |  |
| BDB992 | heber | — | בזק | — | scatter |  |
| BDB1024 | heber | II | בטח | — | — | igen |
| BDB1027 | heber | I | בטן | — | — | igen |
| BDB1030 | heber | II | בטן | — | — | igen |
| BDB1064 | heber | — | בֵּית חָנָן | proper name, of a location | Beit „anûn |  |
| BDB1095 | heber | — | בֵּית | preposition | between |  |
| BDB1135 | heber | II | בִּלהָה | proper name, of a location | a city of Simeon |  |
| BDB1145 | heber | — | בלס | — | fig |  |
| BDB1198 | heber | — | בנט | — | — | igen |
| BDB1203 | heber | — | בסר | — | be too early |  |
| BDB1205 | heber | — | בעד | — | be remote, distant |  |
| BDB1208 | heber | — | בעז | — | quick ? |  |
| BDB1252 | heber | — | בצל | — | strip, strip off |  |
| BDB1277 | heber | — | בקה | — | test, prove |  |
| BDB1306 | heber | — | ברד | — | be |  |
| BDB1314 | heber | II | ברה | — | barû |  |
| BDB1316 | heber | — | ברז | — | bore, pierce |  |
| BDB1338 | heber | — | ברם | — | twist a rope of two strands |  |
| BDB1358 | heber | — | ברשׁ | — | — | igen |
| BDB1362 | heber | — | בשׂם | — | have a sweet odour |  |
| BDB1375 | heber | — | בשׁן | — | smooth, soft | igen |
| BDB1383 | heber | — | בתל | — | sever, separate |  |
| BDB1390 | heber | — | בתת | — | cut off, sever |  |
| BDB1394 | heber | — | <big>ג</big> | — | — |  |
| BDB1406 | heber | — | גְּאוּלַי | noun abstract | redemption |  |
| BDB1415 | heber | — | גבא | — | restrain |  |
| BDB1417 | heber | — | גבב | — | be curved, convex, elevated |  |
| BDB1422 | heber | — | גבה | — | collect |  |
| BDB1432 | heber | — | גבח | — | giant |  |
| BDB1436 | heber | — | גבל | — | twist, wind |  |
| BDB1445 | heber | — | גבן | — | be curved, contracted, coagulated |  |
| BDB1449 | heber | — | גבע | — | convex, projecting, high |  |
| BDB1471 | heber | — | גבשׁ | — | be firm, massive |  |
| BDB1489 | heber | — | גדה | — | cut, cut |  |
| BDB1500 | heber | — | הַגְּדוֺלִים | proper name, masculine | father of Zabdiel |  |
| BDB1529 | heber | I | גדשׁ | — | heap up |  |
| BDB1531 | heber | II | גּדשׁ | — | — |  |
| BDB1545 | heber | — | גוה | — | project, be convex |  |
| BDB1556 | heber | — | גּון | — | tinge |  |
| BDB1578 | heber | — | גושׁ | — | be hard |  |
| BDB1591 | heber | II | גזל | — | crassa vox, vox columbi | igen |
| BDB1593 | heber | — | גזם | — | cut off |  |
| BDB1596 | heber | — | גזע | — | cut off | igen |
| BDB1605 | heber | — | גחל | — | kindle, burn |  |
| BDB1607 | heber | — | גחם | — | kindle |  |
| BDB1609 | heber | — | גחן | — | curve, bend |  |
| BDB1611 | heber | — | גחר | — | retire, retreat |  |
| BDB1615 | heber | — | גיד | — | gâdu, bind, fetter | igen |
| BDB1626 | heber | — | גיר | — | boil, boil up |  |
| BDB1631 | heber | — | גלב | — | shear, shave |  |
| BDB1634 | heber | — | גלד | — | obducere, inducere | igen |
| BDB1644 | heber | I | גלל | — | be great in rank |  |
| BDB1675 | heber | — | גמד | — | congeal, become solid; be hard, stern | igen |
| BDB1685 | heber | — | גָּמָל | noun masculine | camel |  |
| BDB1687 | heber | — | גמם | — | become much |  |
| BDB1690 | heber | — | גמץ | — | dig | igen |
| BDB1699 | heber | — | גנז | — | cover up, hide |  |
| BDB1722 | heber | — | גפן | — | — | igen |
| BDB1724 | heber | — | גפף | — | curved, convex | igen |
| BDB1729 | heber | — | גרב | — | have the scab | igen |
| BDB1741 | heber | — | גרטל | — | — | igen |
| BDB1743 | heber | — | גרל | — | stones |  |
| BDB1750 | heber | — | גרן | — | become accustomed, worn smooth | igen |
| BDB1764 | heber | — | גרשׂ | — | bray, pound, grind, coarse |  |
| BDB1774 | heber | — | גשׁם | — | be bulky, massive | igen |
| BDB1782 | heber | — | גשׁר | — | gašâru | igen |
| BDB1789 | heber | — | <big>ד</big> | — | — |  |
| BDB1801 | heber | — | דבא | — | — | igen |
| BDB1807 | heber | — | דבל | — | collect |  |
| BDB1831 | heber | — | דבשׁ | — | become black | igen |
| BDB1845 | heber | — | דגן | — | heap up | igen |
| BDB1860 | heber | — | דוד | — | swing, rock, dandle, fondle, love | igen |
| BDB1880 | heber | — | דום | — | spread slander |  |
| BDB1888 | heber | — | דוק | — | — | igen |
| BDB1905 | heber | — | דחן | — | smoke arose | igen |
| BDB1935 | heber | — | דכך | — | — | igen |
| BDB1970 | heber | — | דמן | — | prepare, improve, manure land | igen |
| BDB1982 | heber | — | דנג | — | — | igen |
| BDB1987 | heber | — | דפה | — | blemish, fault | igen |
| BDB1991 | heber | — | דקל | — | palm | igen |
| BDB1999 | heber | — | דרא | — | repel | igen |
| BDB2001 | heber | — | דרב | — | become accustomed, trained | igen |
| BDB2004 | heber | — | דרג | — | go on foot, step by step, walk | igen |
| BDB2013 | heber | — | דרע | — | arm |  |
| BDB2016 | heber | — | דרק | — | walk rapidly, hasten | igen |
| BDB2018 | heber | — | דרר | 1. | stream, flow abundantly |  |
| BDB2047 | heber | — | הגג | — | murmur |  |
| BDB2055 | heber | — | הגן | — | be suitable, fit, worthy: |  |
| BDB2057 | heber | — | הגר | — | forsake, retire | igen |
| BDB2060 | heber | — | הדד | — | make a loud noise |  |
| BDB2072 | heber | — | הדם | — | overthrow, overturn, cast down | igen |
| BDB2089 | heber | — | הוד | — | crash, roar, resonance | igen |
| BDB2193 | heber | — | המל | — | shed tears | igen |
| BDB2197 | heber | — | הָמַן | verb | rage, be trubulent |  |
| BDB2199 | heber | — | המס | — | — | igen |
| BDB2201 | heber | — | המר | — | pour, pour out | igen |
| BDB2239 | heber | — | הרר | — | — | igen |
| BDB2246 | heber | — | מַהֲתַלּוֺת | noun feminine plural | deceptions |  |
| BDB2253 | heber | — | וזר | — | bear a burden | igen |
| BDB2260 | heber | — | <big>ז</big> | — | — |  |
| BDB2261 | heber | — | זאב | — | id quod | igen |
| BDB2265 | heber | — | זבב | — | go hither and thither | igen |
| BDB2287 | heber | — | זוג | — | be clear, bright transparent | igen |
| BDB2293 | heber | — | זהב | — | — | igen |
| BDB2303 | heber | — | זוה | — | put aside | igen |
| BDB2306 | heber | I | זוז | — | move |  |
| BDB2313 | heber | II | זוז | — | be abundant | igen |
| BDB2317 | heber | I | זול | — | remove, depart | igen |
| BDB2366 | heber | — | זלא | — | — | igen |
| BDB2368 | heber | — | זלג | — | glide, slip |  |
| BDB2375 | heber | — | זלעף | — | — | igen |
| BDB2378 | heber | — | זִלְפָּה | proper name, feminine | Leah's maid |  |
| BDB2396 | heber | III | זמר | ** | thing to be protected, thing sacred, inviolable |  |
| BDB2404 | heber | — | זנב | — | — | igen |
| BDB2424 | heber | — | זער | — | be scanty |  |
| BDB2431 | heber | — | זקן | — | — | igen |
| BDB2471 | heber | II | זרע | — | stretch out, extend |  |
| BDB2484 | heber | — | <big>ח</big> | — | — |  |
| BDB2531 | heber | — | חבת | — | be obscure | igen |
| BDB2534 | heber | — | חגּב | — | prevent, intervene, hide | igen |
| BDB2546 | heber | — | חגה | — | conceal | igen |
| BDB2548 | heber | — | חגל | — | hobble, hop | igen |
| BDB2571 | heber | — | חדק | — | press | igen |
| BDB2589 | heber | I | חוד | — | decline, turn aside, avoid | igen |
| BDB2595 | heber | II | חוה | — | collect, gather | igen |
| BDB2602 | heber | — | חוח | — | — | igen |
| BDB2605 | heber | — | חוט | — | sew | igen |
| BDB2624 | heber | — | חום | — | be warm | igen |
| BDB2629 | heber | I | חוץ | — | — | igen |
| BDB2632 | heber | II | חוץ | — | sew together | igen |
| BDB2634 | heber | — | חוק | — | —î ‡u | igen |
| BDB2643 | heber | III | חוּר | — | — |  |
| BDB2647 | heber | II | חור | — | bend, turn, incline | igen |
| BDB2675 | heber | II | חזה | — | be opposite | igen |
| BDB2678 | heber | — | חזז | — | cut | igen |
| BDB2690 | heber | — | חזר | — | the eye was | igen |
| BDB2701 | heber | II | חטב | — | turbid, dusky, mixed with yellowish red | igen |
| BDB2704 | heber | — | חטט | — | make lines, marks | igen |
| BDB2706 | heber | — | חטל | — | be flabby | igen |
| BDB2711 | heber | — | חטר | — | lash with the tail, move spear up and down, shake, | igen |
| BDB2713 | heber | — | חטשׁ | — | — | igen |
| BDB2729 | heber | — | חכל | — | be confused, vague | igen |
| BDB2741 | heber | II | חלא | — | she sinned and defiled herself | igen |
| BDB2744 | heber | — | חלב | — | — | igen |
| BDB2746 | heber | II | חלב | — | —alâbu | igen |
| BDB2753 | heber | I | חלד | — | abide, continue | igen |
| BDB2755 | heber | II | חלד | — | dig | igen |
| BDB2767 | heber | III | חלה | — | adorn |  |
| BDB2775 | heber | — | חלך | — | be black | igen |
| BDB2794 | heber | — | חלמשׁ | — | — | igen |
| BDB2809 | heber | — | חֵ֫לֶץ | proper name, masculine | — |  |
| BDB2835 | heber | — | חמא | — | be hard | igen |
| BDB2846 | heber | I | חמה | — | protect, guard | igen |
| BDB2854 | heber | — | חמט | — | —amâ ‰u | igen |
| BDB2890 | heber | III | חמר | — | heap up | igen |
| BDB2899 | heber | I | חמשׁ | — | — | igen |
| BDB2905 | heber | III | חמשׁ | — | — | igen |
| BDB2907 | heber | IV | חמשׁ | — | army | igen |
| BDB2909 | heber | — | חמת | — | grow rancid, putrid | igen |
| BDB2927 | heber | I | חנך | — | — | igen |
| BDB2997 | heber | — | חפן | — | take with both hands | igen |
| BDB3005 | heber | II | חפף | — | rub, cleanse |  |
| BDB3038 | heber | — | חצן | — | carry in the arms | igen |
| BDB3046 | heber | I | חצר | — | encompass, surround | igen |
| BDB3048 | heber | II | חצר | — | be present, settle | igen |
| BDB3064 | heber | III | חצר | — | be green | igen |
| BDB3066 | heber | IV | חצר | — | — | igen |
| BDB3080 | heber | — | חרא | — | — | igen |
| BDB3099 | heber | — | חרגל | — | run right and left, run swiftly | igen |
| BDB3111 | heber | — | חרז | — | string together | igen |
| BDB3115 | heber | I | חרט | — | cut, scratch, tear | igen |
| BDB3118 | heber | II | חרט | — | — | igen |
| BDB3123 | heber | II | חרך | — | — | igen |
| BDB3125 | heber | — | חרל | — | — | igen |
| BDB3141 | heber | — | חרס | — | — | igen |
| BDB3144 | heber | — | חרע | — | be clever | igen |
| BDB3148 | heber | II | חרף | — | gather fruit, pluck | igen |
| BDB3158 | heber | III | חָרוּץ | noun [masculine] | trench, moat |  |
| BDB3162 | heber | II | חרץ | — | be yellow | igen |
| BDB3164 | heber | — | חרצב | — | bind | igen |
| BDB3171 | heber | II | חרר | — | be | igen |
| BDB3173 | heber | III | חרר | — | —arâru | igen |
| BDB3177 | heber | — | חרשׂ | — | scratch, lacerate | igen |
| BDB3189 | heber | III | חרשׁ | — | — | igen |
| BDB3191 | heber | IV | חרשׁ | — | — | igen |
| BDB3229 | heber | — | חשׁן | — | be excellent, beautiful | igen |
| BDB3236 | heber | — | חשׁר | — | ašâru | igen |
| BDB3239 | heber | — | חשׁשׁ | — | hasten, hurry | igen |
| BDB3256 | heber | I | חתן | — | circumcise | igen |
| BDB3274 | heber | — | <big>ט</big> | — | — |  |
| BDB3289 | heber | II | טבל | — | wind about, wrap up | igen |
| BDB3294 | heber | — | טבר | — | — | igen |
| BDB3317 | heber | — | טוט | — | — | igen |
| BDB3321 | heber | — | טוּר | — | go | igen |
| BDB3331 | heber | — | טחר | — | eject | igen |
| BDB3333 | heber | — | טטף | — | ‰a‰âpu | igen |
| BDB3338 | heber | — | טלה | — | tie a lamb | igen |
| BDB3340 | heber | I | טלל | — | rained fine rain | igen |
| BDB3343 | heber | — | טלם | — | oppress, injure | igen |
| BDB3353 | heber | — | טנא | — | set up, erect | igen |
| BDB3375 | heber | — | טרה | — | be fresh, juicy, moist | igen |
| BDB3384 | heber | — | <big>י</big> | — | — |  |
| BDB3406 | heber | — | יבם | — | — | igen |
| BDB3421 | heber | — | יגן | — | beat | igen |
| BDB3440 | heber | II | ידד | — | love | igen |
| BDB3485 | heber | — | יהץ | — | break, split; valide calcavit | igen |
| BDB3487 | heber | — | יהר | — | shew oneself haughty | igen |
| BDB3496 | heber | I | יון | — | — | igen |
| BDB3498 | heber | II | יון | — | wanâ | igen |
| BDB3503 | heber | — | יזה | — | congregatus, conglomeratus fuit. | igen |
| BDB3506 | heber | — | יזע | — | fluxit | igen |
| BDB3522 | heber | — | יחף | — | discalceatus fuit | igen |
| BDB3525 | heber | — | יחשׂ | — | — | igen |
| BDB3533 | heber | — | יין | — | wine | igen |
| BDB3559 | heber | — | ילף | — | conjunctus fuit | igen |
| BDB3561 | heber | — | ילק | — | lick | igen |
| BDB3566 | heber | — | ימם | — | — | igen |
| BDB3620 | heber | II | יעל | — | eminuit, prominuit | igen |
| BDB3627 | heber | — | יען | — | avidus, cupidus | igen |
| BDB3634 | heber | II | יעף | — | ascend | igen |
| BDB3639 | heber | I | יער | — | be rugged | igen |
| BDB3641 | heber | II | יער | — | — | igen |
| BDB3681 | heber | — | יקב | — | be sunk, depressed | igen |
| BDB3687 | heber | — | יָקְדְעָם | proper name, of a location | a city of Judah |  |
| BDB3688 | heber | — | יקה | — | preserve | igen |
| BDB3691 | heber | — | יקהּ | — | be obedient | igen |
| BDB3693 | heber | — | יָקוֺט | — | — |  |
| BDB3733 | heber | — | ירח | — | wanderer | igen |
| BDB3741 | heber | — | ירך | — | — | igen |
| BDB3750 | heber | I | ירק | — | grow green | igen |
| BDB3785 | heber | — | ישׁה | — | assist, support: | igen |
| BDB3789 | heber | — | ישׁח | — | — | igen |
| BDB3808 | heber | II | שׁוֺעַ | — | — |  |
| BDB3809 | heber | III | שׁוֺעַ | proper name, of a people | — |  |
| BDB3834 | heber | — | ישׁשׁ | — | weak | igen |
| BDB3838 | heber | — | יתד | — | drive in peg, be firm | igen |
| BDB3840 | heber | — | יְתוּר | — | — |  |
| BDB3841 | heber | — | יתח | — | beat with a club, chastise | igen |
| BDB3843 | heber | — | יתם | — | be alone, bereaved | igen |
| BDB3846 | heber | — | יתן | — | be perpetual, never-failing | igen |
| BDB3880 | heber | — | כבב | — | roll threads into a ball | igen |
| BDB3892 | heber | — | כבל | — | bind | igen |
| BDB3894 | heber | — | כבן | — | wrap round, wrap up | igen |
| BDB3904 | heber | II | כבר | — | to intertwine, net | igen |
| BDB3916 | heber | — | כדד | — | toil severely | igen |
| BDB3920 | heber | — | כדר | — | shoot | igen |
| BDB3930 | heber | — | כהן | — | divine | igen |
| BDB3942 | heber | — | כום | — | heap up, accumulate | igen |
| BDB3958 | heber | I | כור | ** | be |  |
| BDB3982 | heber | — | כזר | — | be cruel | igen |
| BDB3989 | heber | — | כחח | — | — | igen |
| BDB3999 | heber | — | כיד | — | labour, take pains, strive | igen |
| BDB4012 | heber | — | כלב | — | — | igen |
| BDB4029 | heber | II | כלה | — | — | igen |
| BDB4031 | heber | — | כלח | — | contract the face, look hard, stern | igen |
| BDB4042 | heber | II | כלל | — | kallâtu | igen |
| BDB4057 | heber | — | כמז | — | bunch, heap | igen |
| BDB4060 | heber | — | כמן | — | be hidden | igen |
| BDB4066 | heber | II | כמר | — | black, dark | igen |
| BDB4068 | heber | III | כמר | — | kamâru | igen |
| BDB4074 | heber | — | כמת | — | — | igen |
| BDB4081 | heber | I | כנן | — | be firm, substantial | igen |
| BDB4086 | heber | II | כנן | — | — | igen |
| BDB4098 | heber | — | כנף | — | fence in, enclose | igen |
| BDB4101 | heber | — | כנר | — | — | igen |
| BDB4113 | heber | II | כסה | Pi`el | bind |  |
| BDB4148 | heber | — | כפס | — | bind, fasten | igen |
| BDB4153 | heber | I | כפר | ** | cover |  |
| BDB4158 | heber | II | כפר | — | — | igen |
| BDB4161 | heber | III | כפר | — | — | igen |
| BDB4167 | heber | — | כְּפִירִים | — | villages |  |
| BDB4168 | heber | IV | כפר | — | dig | igen |
| BDB4175 | heber | I | כַּר | — | basket-saddle |  |
| BDB4177 | heber | III | כַּר | — | lamb |  |
| BDB4189 | heber | — | כרך | — | enwrap, surround | igen |
| BDB4191 | heber | — | כרכב | quadril. | furnish with a rim, enclose, set |  |
| BDB4208 | heber | — | כָּרַר | verb | use circumlocution |  |
| BDB4212 | heber | — | כרשׂ | — | be wrinkled | igen |
| BDB4229 | heber | I | כשׁף | — | cut off, cut up | igen |
| BDB4233 | heber | II | כשׁף | — | — | igen |
| BDB4244 | heber | — | כתל | — | make into firm lumps | igen |
| BDB4248 | heber | II | כתם | — | — | igen |
| BDB4251 | heber | — | כתן | — | clothe | igen |
| BDB4253 | heber | — | כתף | — | — | igen |
| BDB4271 | heber | — | לאב | — | be thirsty | igen |
| BDB4279 | heber | — | לאך | — | send | igen |
| BDB4285 | heber | — | לאם | — | bind up | igen |
| BDB4288 | heber | — | לבא | — | lioness | igen |
| BDB4293 | heber | — | לבב | 1. | lab'bu, in unruhiger Bewegung sein; |  |
| BDB4301 | heber | — | לְבַד | — | alone |  |
| BDB4302 | heber | — | לַבָּה | — | — |  |
| BDB4328 | heber | — | להב | — | thirsty | igen |
| BDB4334 | heber | — | להג | — | be devoted, attached | igen |
| BDB4338 | heber | — | לִהְלֵהַּ | verb quadriliteral | amaze, startle |  |
| BDB4353 | heber | III | לוה | — | turn, twist, wind | igen |
| BDB4361 | heber | — | לוח | — | shine, gleam, flash | igen |
| BDB4372 | heber | — | לולו | — | turn, twist, wind | igen |
| BDB4384 | heber | — | לחה | — | smoothness | igen |
| BDB4387 | heber | — | לחח | — | moisten, cool | igen |
| BDB4405 | heber | — | לטא | — | — | igen |
| BDB4414 | heber | — | לישׁ | — | be strong | igen |
| BDB4443 | heber | — | לפד | — | — | igen |
| BDB4462 | heber | — | לקשׁ | — | be late | igen |
| BDB4466 | heber | — | לשׁד | — | suck, lick | igen |
| BDB4468 | heber | — | לשׁך | — | — | igen |
| BDB4472 | heber | — | לשׁן | — | lick | igen |
| BDB4477 | heber | — | לתח | — | spread out | igen |
| BDB4479 | heber | — | לתך | — | — | igen |
| BDB4481 | heber | — | <big>מ</big> | — | — |  |
| BDB4482 | heber | — | מאד | — | ma'âdu | igen |
| BDB4486 | heber | — | מאם | — | black | igen |
| BDB4488 | heber | — | מוּם | noun masculine | id. |  |
| BDB4497 | heber | — | מאץ | (compare | white |  |
| BDB4503 | heber | — | מגד | — | be glorious, excel in glory | igen |
| BDB4516 | heber | — | מדה | — | — | igen |
| BDB4531 | heber | II | מהר | ( | mâru |  |
| BDB4534 | heber | I | מו | — | what |  |
| BDB4539 | heber | I | מוד | — | stretch, extend | igen |
| BDB4550 | heber | — | מוץ | — | — | igen |
| BDB4564 | heber | — | (לְ)מוֺתָם | 1. | — |  |
| BDB4566 | heber | — | מזג | — | mix, prepare by mixing. | igen |
| BDB4568 | heber | — | מזה | — | suck out | igen |
| BDB4574 | heber | I | מזר | — | be bad | igen |
| BDB4576 | heber | II | מזר | — | spread out | igen |
| BDB4586 | heber | — | מחח | — | be fat | igen |
| BDB4602 | heber | — | מחר | — | be in front of meet | igen |
| BDB4607 | heber | — | מטל | — | strike, beat, extend by beating, shape iron into a | igen |
| BDB4628 | heber | — | מין | — | i | igen |
| BDB4631 | heber | — | מיץ | — | press, squeeze | igen |
| BDB4659 | heber | II | מלח | — | — | igen |
| BDB4668 | heber | I | מלך | — | possess, own exclusively | igen |
| BDB4721 | heber | — | מנח | — | lend, give a gift | igen |
| BDB4725 | heber | — | מנן | — | praecidit | igen |
| BDB4751 | heber | — | מעה | — | — | igen |
| BDB4755 | heber | — | מעז | — | — | igen |
| BDB4779 | heber | — | מצח | — | — | igen |
| BDB4784 | heber | — | מצר | — | — | igen |
| BDB4795 | heber | II | מרא | — | be fat | igen |
| BDB4828 | heber | II | מרק | — | fill a pot with rich broth | igen |
| BDB4847 | heber | II | מרר | — | pass by, go | igen |
| BDB4882 | heber | — | משׁע | — | misû |  |
| BDB4885 | heber | — | משׁקֹ | — | — | igen |
| BDB4893 | heber | — | מתג | — | — | igen |
| BDB4898 | heber | — | מתן | — | be stout, firm, enduring | igen |
| BDB4908 | heber | — | <big>נ</big> | — | — |  |
| BDB4914 | heber | — | נאם | — | groan, sigh | igen |
| BDB4927 | heber | — | נבא | ** | utter a low voice, or sound |  |
| BDB4947 | heber | I | נבל | — | — | igen |
| BDB4960 | heber | — | נגב | — | be dry, parched | igen |
| BDB4971 | heber | — | נגל | — | strike, split, pierce | igen |
| BDB4996 | heber | II | נדד | — | high hill, hill rising high into the sky | igen |
| BDB4999 | heber | II | נדה | — | be moist, moistened | igen |
| BDB5015 | heber | — | הִי | noun [masculine] | wailing |  |
| BDB5040 | heber | — | נוהּ | — | be high, eminent | igen |
| BDB5043 | heber | II | נוה | — | aim at, propose to oneself as aim | igen |
| BDB5082 | heber | II | נוף | — | overtop | igen |
| BDB5087 | heber | — | נור | — | flame, fire | igen |
| BDB5098 | heber | — | נזם | — | — | igen |
| BDB5107 | heber | I | נחל | — | give for one's own, bestow | igen |
| BDB5111 | heber | II | נָחַל | — | — | igen |
| BDB5129 | heber | — | נחר | — | na—îru | igen |
| BDB5135 | heber | I | נחשׁ | ** | hiss |  |
| BDB5141 | heber | III | נחשׁ | — | — | igen |
| BDB5147 | heber | IV | נחשׁ | — | goad, prick | igen |
| BDB5184 | heber | II | ניר | — | heddles | igen |
| BDB5190 | heber | — | נכד | — | gens, stirps | igen |
| BDB5195 | heber | I | נָכוֺן | noun [masculine] | blow |  |
| BDB5198 | heber | — | נכח | — | be in front of | igen |
| BDB5208 | heber | II | נכר | ** | foreign, strange |  |
| BDB5219 | heber | — | נמל | — | — | igen |
| BDB5221 | heber | — | נמר | — | namâru | igen |
| BDB5246 | heber | II | נסע | — | throw | igen |
| BDB5268 | heber | II | נעם | — | speak in a low, gentle voice | igen |
| BDB5270 | heber | — | נעץ | — | prick, stick | igen |
| BDB5276 | heber | III | נער | — | — | igen |
| BDB5309 | heber | — | נפשׁ | — | soul, life, person, living being, blood, desire | igen |
| BDB5333 | heber | II | נצח | — | sprinkle | igen |
| BDB5344 | heber | II | נצץ | — | isle (coast) of hawks | igen |
| BDB5348 | heber | II | נצר | — | be fresh, bright, grow green | igen |
| BDB5357 | heber | I | נקד | — | point, furnish with points | igen |
| BDB5361 | heber | II | נקד | — | a kind of small sheep | igen |
| BDB5377 | heber | — | נקק | — | rima, fissura | igen |
| BDB5399 | heber | — | נשׂר | — | saw | igen |
| BDB5434 | heber | — | נתב | — | swell forth, become prominent, protuberant | igen |
| BDB5465 | heber | — | <big>ס</big> | — | — |  |
| BDB5495 | heber | — | סגל | — | acquire property | igen |
| BDB5507 | heber | — | סדר | — | sadâru | igen |
| BDB5511 | heber | — | סהר | proper name, of a location | be round |  |
| BDB5518 | heber | — | סוד | Niph`al | converse |  |
| BDB5521 | heber | — | סוה | — | curtain, veil ? | igen |
| BDB5618 | heber | II | סלל | ** | plait, curl |  |
| BDB5621 | heber | — | סלע | — | cleave, split | igen |
| BDB5635 | heber | — | סמם | — | smell | igen |
| BDB5656 | heber | — | סעף | — | cleave, divide | igen |
| BDB5666 | heber | — | ספא | — | give to eat | igen |
| BDB5672 | heber | II | ספח | — | pour out | igen |
| BDB5676 | heber | III | ספח | — | — | igen |
| BDB5686 | heber | — | ספף | — | — | igen |
| BDB5709 | heber | — | סרד | — | be frightened | igen |
| BDB5731 | heber | — | <big>ע</big> | — | — |  |
| BDB5732 | heber | — | עבב | — | — | igen |
| BDB5755 | heber | — | עבט | — | ubbu‰u° | igen |
| BDB5759 | heber | — | עבל | — | be bulky, stout | igen |
| BDB5763 | heber | — | עבץ | — | — | igen |
| BDB5779 | heber | — | מַעְבָּרָה | noun feminine | ford, pass, passage |  |
| BDB5788 | heber | — | עגל | — | berounded | igen |
| BDB5800 | heber | — | עגר | — | — | igen |
| BDB5802 | heber | — | עדד | — | count, reckon | igen |
| BDB5816 | heber | I | עדל | — | act equitably | igen |
| BDB5818 | heber | II | עדל | — | turn aside | igen |
| BDB5821 | heber | I | עדן | — | mollities, lanquor | igen |
| BDB5832 | heber | II | עדן | — | edinu | igen |
| BDB5846 | heber | — | עוב | — | be absent, hidden | igen |
| BDB5849 | heber | — | עוג | — | id. draw a circle | igen |
| BDB5868 | heber | II | עוה | — | err from the way | igen |
| BDB5879 | heber | II | עול | — | feed, nourish | igen |
| BDB5881 | heber | III | עול | — | deviate from | igen |
| BDB5902 | heber | — | תְּעֻפָה | noun feminine | — |  |
| BDB5927 | heber | III | עור | — | — | igen |
| BDB5982 | heber | II | עזר | — | temple-court | igen |
| BDB5989 | heber | — | עטן | — | put | igen |
| BDB6000 | heber | — | עטשׁ | — | sneeze | igen |
| BDB6041 | heber | — | עיר | — | go away, go hither and thither, escape through spr | igen |
| BDB6053 | heber | — | עכן | — | — | igen |
| BDB6056 | heber | — | עכס | — | reverse, tie backward | igen |
| BDB6066 | heber | — | עלג | — | — | igen |
| BDB6101 | heber | II | עלל | — | capricious, mischievous | igen |
| BDB6114 | heber | II | עלם | — | be mature | igen |
| BDB6118 | heber | III | עלם | — | world, age | igen |
| BDB6126 | heber | — | עלק | — | hang, be suspended, cleave, adhere | igen |
| BDB6134 | heber | — | עמה | — | emû, be united, associated; emûtu, family, family  | igen |
| BDB6143 | heber | I | עָמַם | verb | be comprehensive, include |  |
| BDB6171 | heber | I | עמר | — | be abundant | igen |
| BDB6178 | heber | III | עמר | — | live, live long | igen |
| BDB6185 | heber | — | ענב | — | id. | igen |
| BDB6219 | heber | — | ענז | — | turn aside | igen |
| BDB6225 | heber | I | ענן | — | cover | igen |
| BDB6233 | heber | — | ענף | — | — | igen |
| BDB6236 | heber | — | ענק | — | neck | igen |
| BDB6241 | heber | — | ענשׁ | — | be fined | igen |
| BDB6256 | heber | I | עפר | — | dust | igen |
| BDB6259 | heber | II | עפר | — | young of mountain-goat | igen |
| BDB6277 | heber | — | עצד | — | lop trees with a | igen |
| BDB6280 | heber | II | עצה | — | wood | igen |
| BDB6283 | heber | III | עצה | — | eƒên-ƒêri,eƒên | igen |
| BDB6285 | heber | IV | עצה | — | a land abounding with the trees called | igen |
| BDB6308 | heber | — | עקב | — | be protuberant | igen |
| BDB6321 | heber | II | עקד | — | striped with bands | igen |
| BDB6323 | heber | — | עקה | — | hinder | igen |
| BDB6329 | heber | — | עקר | — | root | igen |
| BDB6345 | heber | I | ערב | — | mix | igen |
| BDB6356 | heber | IV | ערב | — | be arid | igen |
| BDB6362 | heber | V | ערב | — | erêbu | igen |
| BDB6366 | heber | VI | ערב | — | be black | igen |
| BDB6387 | heber | — | ערל | — | foreskin | igen |
| BDB6393 | heber | II | ערם | — | strip | igen |
| BDB6399 | heber | — | ערס | — | — | igen |
| BDB6401 | heber | I | ערף | — | mane | igen |
| BDB6414 | heber | I | ערר | — | sepulchre | igen |
| BDB6422 | heber | — | ערשׂ | — | booth, shed, throne | igen |
| BDB6424 | heber | — | ערשׁ | — | — | igen |
| BDB6426 | heber | — | עשׂב | — | ešêbu | igen |
| BDB6440 | heber | — | עשׂר | — | gather, unite | igen |
| BDB6450 | heber | — | עשׁן | — | ascend | igen |
| BDB6484 | heber | — | עתל | — | atâlu | igen |
| BDB6499 | heber | III | עתר | — | — | igen |
| BDB6501 | heber | — | <big>פ</big> | — | — |  |
| BDB6507 | heber | II | פאר | — | — | igen |
| BDB6513 | heber | — | פגג | — | unripe fig | igen |
| BDB6515 | heber | — | פגל | — | be thick and soft, flaccid | igen |
| BDB6564 | heber | I | פור | — | foam | igen |
| BDB6583 | heber | — | פחח | — | — | igen |
| BDB6587 | heber | — | פחם | — | be black | igen |
| BDB6589 | heber | — | פחת | — | cut off | igen |
| BDB6601 | heber | — | פיד | — | die | igen |
| BDB6604 | heber | — | פים | — | fill | igen |
| BDB6610 | heber | — | פכך | — | flask | igen |
| BDB6614 | heber | — | פלא | — | separate | igen |
| BDB6640 | heber | I | פַּלְטִי | adjective, of a people | — |  |
| BDB6652 | heber | — | פלך | — | be round | igen |
| BDB6664 | heber | — | פלס | — | be even, balance | igen |
| BDB6686 | heber | — | פנן | — | — | igen |
| BDB6703 | heber | I | פסס | — | spread | igen |
| BDB6748 | heber | — | פקע | — | split, spring off | igen |
| BDB6752 | heber | II | פרא | — | run | igen |
| BDB6758 | heber | II | פרד | — | flee, flee away | igen |
| BDB6768 | heber | — | פרז | — | remove, separate | igen |
| BDB6782 | heber | I | פרך | — | rub, chafe, crumble | igen |
| BDB6784 | heber | II | פרך | — | parâku | igen |
| BDB6794 | heber | I | פרע | — | overtop | igen |
| BDB6799 | heber | II | פרע | — | sprout | igen |
| BDB6811 | heber | II | פרץ | — | notch, make mark by notching | igen |
| BDB6819 | heber | III | פרר | — | young | igen |
| BDB6829 | heber | III | פרשׁ | — | cause to break | igen |
| BDB6832 | heber | IV | פרשׁ | — | horse | igen |
| BDB6885 | heber | — | פתן | — | patânu | igen |
| BDB6898 | heber | — | <big>צ</big> | — | — |  |
| BDB6900 | heber | — | צאן | — | ƒênu | igen |
| BDB6905 | heber | I | צבב | — | ƒumbu | igen |
| BDB6907 | heber | II | צבב | — | cleave to ground | igen |
| BDB6912 | heber | II | צבה | — | lean, incline | igen |
| BDB6914 | heber | III | צבה | — | ƒabîtu | igen |
| BDB6921 | heber | I | צבע | — | dye | igen |
| BDB6924 | heber | II | צבע | — | point | igen |
| BDB6926 | heber | III | צבע | — | limp | igen |
| BDB6931 | heber | — | צבת | — | bind, unite | igen |
| BDB6933 | heber | — | צדד | — | turn away | igen |
| BDB6940 | heber | — | צדק | — | speak the truth | igen |
| BDB6952 | heber | — | צהר | ( | appear, mount |  |
| BDB6959 | heber | — | צוא | — | be foul | igen |
| BDB6974 | heber | II | צוד | — | sîdîtu | igen |
| BDB6984 | heber | — | צול | — | miƒwal | igen |
| BDB6990 | heber | — | צוע | — | form, fashion | igen |
| BDB7009 | heber | I | צור | — | cause to incline, learn | igen |
| BDB7019 | heber | V | צור | — | rock | igen |
| BDB7026 | heber | — | צחה | — | be cloudless | igen |
| BDB7033 | heber | — | צחן | — | stinking fluid | igen |
| BDB7038 | heber | — | צחר | — | dry up, become yellow | igen |
| BDB7048 | heber | — | ציה | — | be parched | igen |
| BDB7057 | heber | I | ציר | — | become, attain to go | igen |
| BDB7059 | heber | II | ציר | ** | turn, revolve |  |
| BDB7066 | heber | III | צלח | — | flat dish | igen |
| BDB7085 | heber | IV | צלל | — | unleavened bread | igen |
| BDB7087 | heber | — | צלם | — | cut off | igen |
| BDB7093 | heber | I | צלע | — | decline, deviate | igen |
| BDB7113 | heber | — | צמם | Jer | draw together |  |
| BDB7118 | heber | — | צמר | — | — | igen |
| BDB7129 | heber | I | צנן | — | — | igen |
| BDB7133 | heber | II | צנן | — | be cold | igen |
| BDB7135 | heber | III | צנן | — | preserve,keep | igen |
| BDB7139 | heber | — | צָנוּעַ | adjective | modest |  |
| BDB7144 | heber | — | צנק | — | shut up | igen |
| BDB7146 | heber | — | צנר | — | hinge-socket | igen |
| BDB7153 | heber | II | צעד | — | — | igen |
| BDB7160 | heber | — | צעף | — | make double | igen |
| BDB7187 | heber | — | צפח | — | make wide, broad | igen |
| BDB7200 | heber | I | צפע | I. | hiss |  |
| BDB7203 | heber | II | צפע | — | cacavit | igen |
| BDB7205 | heber | III | צפע | — | — | igen |
| BDB7210 | heber | II | צפר | — | peep, twitter whistle | igen |
| BDB7214 | heber | III | צפר | — | plait, braid | igen |
| BDB7216 | heber | IV | צפר | — | ƒupru | igen |
| BDB7218 | heber | V | צפר | — | leap | igen |
| BDB7233 | heber | — | צרה | — | run blood, bleed | igen |
| BDB7238 | heber | II | צרח | — | dig | igen |
| BDB7240 | heber | — | צרך | — | have need of | igen |
| BDB7242 | heber | — | צרע | — | throw down, prostrate | igen |
| BDB7265 | heber | III | צרר | — | be sharp | igen |
| BDB7274 | heber | — | <big>ק</big> | — | — |  |
| BDB7276 | heber | I | קבב | — | arch, dome | igen |
| BDB7280 | heber | — | קבה | — | echinus | igen |
| BDB7296 | heber | II | קדד | — | ‡a‡‡adu | igen |
| BDB7302 | heber | — | קדם | 1 a | be before, in front |  |
| BDB7321 | heber | — | קדשׁ | — | separation, withdrawal | igen |
| BDB7331 | heber | — | קהל | — | assembly, congregation | igen |
| BDB7358 | heber | — | קול | — | kâlu | igen |
| BDB7372 | heber | — | מָקוֺם | noun masculine | standing-place, place |  |
| BDB7381 | heber | II | קוץ | — | cut off | igen |
| BDB7387 | heber | II | קור | — | turn, twist | igen |
| BDB7392 | heber | — | קטב | — | cut off | igen |
| BDB7402 | heber | I | קטר | — | ‡utru | igen |
| BDB7420 | heber | — | קין | — | fit together, fabricate (make artificially), forge | igen |
| BDB7430 | heber | II | קיץ | — | vehement heat of summer, late summer | igen |
| BDB7444 | heber | I | קלט | — | take up, in, harbour, so ᵑ7 קְלַט ; Ba Es:36 compa | igen |
| BDB7467 | heber | — | קמח | — | ‡amû | igen |
| BDB7473 | heber | — | קמשׂ | — | — | igen |
| BDB7475 | heber | — | קנא | — | become intensely red (or black) | igen |
| BDB7485 | heber | II | קנה | — | ‡anû | igen |
| BDB7491 | heber | — | קנן | — | nest | igen |
| BDB7494 | heber | — | קנץ | — | catch, capture, ensnare | igen |
| BDB7497 | heber | — | קסם | — | divide, assign | igen |
| BDB7503 | heber | — | קעקע | — | pull, tear | igen |
| BDB7505 | heber | — | קער | — | be deep | igen |
| BDB7513 | heber | — | קפז | — | leap, spring | igen |
| BDB7524 | heber | II | קצה | — | decide judicially, decree | igen |
| BDB7526 | heber | — | קצח | — | seeds used for seasoning | igen |
| BDB7532 | heber | II | קצע | — | cut off | igen |
| BDB7537 | heber | II | קצף | — | break, snap off | igen |
| BDB7565 | heber | II | קרב | — | kirbu | igen |
| BDB7593 | heber | II | קרח | — | — | igen |
| BDB7596 | heber | — | קרן | — | ‡arnu | igen |
| BDB7619 | heber | — | קרשׁ | — | be | igen |
| BDB7621 | heber | — | קשׂה | — | basket of palm-leaves | igen |
| BDB7624 | heber | — | קשׂט | — | — | igen |
| BDB7626 | heber | — | קשׂשׂ | — | scale | igen |
| BDB7628 | heber | — | קשׁא | Jer | cucumber |  |
| BDB7639 | heber | II | קשׁה | — | decorticavit | igen |
| BDB7644 | heber | — | קשׁט | — | succeed | igen |
| BDB7649 | heber | I | קשׁשׁ | — | be old | igen |
| BDB7697 | heber | — | רָבַב | Pu`al denominative | Participle |  |
| BDB7703 | heber | I | רבד | — | confine, tie | igen |
| BDB7717 | heber | I | רבע | — | — | igen |
| BDB7731 | heber | — | רבק | — | tie fast | igen |
| BDB7734 | heber | — | רגב | — | — | igen |
| BDB7745 | heber | — | רִגֵל | c. | treader, fuller |  |
| BDB7782 | heber | — | רהג | — | raise | igen |
| BDB7785 | heber | I | רהט | — | collect, gather | igen |
| BDB7787 | heber | II | רהט | — | run, flow | igen |
| BDB7796 | heber | — | רוח | — | breathe, blow | igen |
| BDB7826 | heber | — | רוף | — | — | igen |
| BDB7838 | heber | — | רזח | — | cry out |  |
| BDB7855 | heber | — | רחה | — | handmill | igen |
| BDB7858 | heber | — | רחל | — | ewe | igen |
| BDB7861 | heber | I | רחם | — | be soft | igen |
| BDB7873 | heber | II | רחם | — | vulture | igen |
| BDB7876 | heber | — | רחן | — | — | igen |
| BDB7893 | heber | — | רטט | — | tremble |  |
| BDB7909 | heber | — | ריף | — | — | igen |
| BDB7924 | heber | — | רֵכָבִי | adjective, of a people | — |  |
| BDB7950 | heber | III | רמה | — | ramû grow loose | igen |
| BDB7962 | heber | — | רמל | — | adorn |  |
| BDB7980 | heber | — | רסן | — | — | igen |
| BDB7985 | heber | II | רסס | — | break, crush | igen |
| BDB8012 | heber | III | רעה | 2 b | take pleasure |  |
| BDB8021 | heber | — | רעם | — | move violently | igen |
| BDB8028 | heber | — | רָעַן | verb | be or grow luxuriant, fresh, green |  |
| BDB8030 | heber | I | רעע | — | — | igen |
| BDB8043 | heber | II | רָפָא | — | — |  |
| BDB8069 | heber | — | רפשׁ | — | talk | igen |
| BDB8086 | heber | II | רצף | — | glow | igen |
| BDB8112 | heber | I | רקק | — | be thin | igen |
| BDB8120 | heber | — | רשׁה | — | permit | igen |
| BDB8123 | heber | — | רשׁע | — | be loose | igen |
| BDB8129 | heber | — | רשׁף | — | irritavit, incendit | igen |
| BDB8143 | heber | — | רתת | — | tremble | igen |
| BDB8145 | heber | — | <big>שׂ</big> | — | — |  |
| BDB8146 | heber | — | שׂאר | — | leaven | igen |
| BDB8148 | heber | — | שׂבךְ | — | interweave | igen |
| BDB8169 | heber | — | שׂדה | — | šadû | igen |
| BDB8174 | heber | — | שׂהר | — | new moon | igen |
| BDB8180 | heber | II | שׂוך | — | branch |  |
| BDB8188 | heber | II | שׂום | — | be inauspicious | igen |
| BDB8206 | heber | — | שׂטן | — | — | igen |
| BDB8214 | heber | — | שׂיד | — | lime | igen |
| BDB8217 | heber | I | שׂיח | — | speak | igen |
| BDB8222 | heber | II | שׂיח | — | šâ—u | igen |
| BDB8224 | heber | — | שׂכה | — | look out | igen |
| BDB8261 | heber | — | שׂמל | — | enclose, envelope | igen |
| BDB8268 | heber | — | שׂמר | — | — | igen |
| BDB8274 | heber | — | שׂעף | — | divide | igen |
| BDB8277 | heber | I | שׂער | — | be hairy | igen |
| BDB8294 | heber | IV | שׂער | — | — | igen |
| BDB8297 | heber | — | שׂפה | — | šaptu | igen |
| BDB8303 | heber | — | שׂקק | — | — | igen |
| BDB8313 | heber | II | שׂרד | — | plait, braid? | igen |
| BDB8320 | heber | II | שׂרה | — | rule ? | igen |
| BDB8338 | heber | I | שׂרק | — | comb, card |  |
| BDB8340 | heber | II | שׂרק | — | light red |  |
| BDB8347 | heber | — | שׂרר | — | šarâru | igen |
| BDB8355 | heber | — | <big>שׁ</big> | — | — |  |
| BDB8385 | heber | II | שׁאר | — | šêru | igen |
| BDB8391 | heber | I | שׁבב | — | hew |  |
| BDB8393 | heber | II | שׁבב | — | šabâbu |  |
| BDB8409 | heber | — | שׁבט | — | šabâ‰u | igen |
| BDB8413 | heber | — | שׁבל | — | cause to hang down | igen |
| BDB8419 | heber | — | שׁבן | — | — | igen |
| BDB8422 | heber | — | שׁבס | — | — | igen |
| BDB8439 | heber | — | שׁבק | — | let go leave | igen |
| BDB8470 | heber | — | שׁגר | J | cast, throw |  |
| BDB8475 | heber | — | שׁדה | — | moisten | igen |
| BDB8481 | heber | — | שׁדם | — | — | igen |
| BDB8487 | heber | — | שׁדשׁ | — | six | igen |
| BDB8495 | heber | I | שׁוא | — | be evil, foul, unseemly | igen |
| BDB8497 | heber | II | שׁוא | — | — | igen |
| BDB8517 | heber | — | שׁוג | — | — | igen |
| BDB8543 | heber | — | שׁוּל | — | hang down loose | igen |
| BDB8556 | heber | I | שׁוּק | — | drive | igen |
| BDB8560 | heber | III | שׁוק | — | attract, impel | igen |
| BDB8567 | heber | III | שׁור | — | become raised, excited, leap, spring | igen |
| BDB8590 | heber | — | שׁחל | — | ša—âlu | igen |
| BDB8593 | heber | — | שׁחן | — | be hot | igen |
| BDB8595 | heber | — | שׁחף | — | is pare, peel off | igen |
| BDB8598 | heber | — | שׁחץ | — | act proudly | igen |
| BDB8609 | heber | II | שׁחר | — | šêru | igen |
| BDB8627 | heber | — | שׁטר | — | ša‰âru | igen |
| BDB8639 | heber | — | שׁין | — | šînu | igen |
| BDB8642 | heber | — | שׁיר | — | — | igen |
| BDB8669 | heber | — | שׁכם | — | carry on the shoulder | igen |
| BDB8685 | heber | II | שׁכר | — | — | igen |
| BDB8692 | heber | — | שׁלג | — | his snow | igen |
| BDB8718 | heber | II | שׁלח | — | strip off hide | igen |
| BDB8723 | heber | II | שׁלט | — | šal‰u | igen |
| BDB8761 | heber | — | שׁלשׁ | — | — | igen |
| BDB8783 | heber | — | שׁמא | — | — | igen |
| BDB8791 | heber | — | שׁמה | — | be high, lofty | igen |
| BDB8815 | heber | II | שׁמן | — | — | igen |
| BDB8845 | heber | — | שׁמץ | — | accusation (or suspicion) | igen |
| BDB8867 | heber | II | שׁמר | — | be tawny, dark | igen |
| BDB8869 | heber | III | שׁמר | — | diamond | igen |
| BDB8873 | heber | — | שׁמשׁ | — | šamšu | igen |
| BDB8879 | heber | — | שׁנב | — | — | igen |
| BDB8883 | heber | II | שׁנה | — | shine | igen |
| BDB8904 | heber | — | שׁעט | — | pound to pieces | igen |
| BDB8907 | heber | I | שׁעל | — | deep, depth | igen |
| BDB8910 | heber | II | שׁעל | — | — | igen |
| BDB8913 | heber | III | שׁוּעָל | proper name, masculine | in Asher |  |
| BDB8917 | heber | — | שׁעם | — | — | igen |
| BDB8928 | heber | I | שׁער | — | break, break off, through | igen |
| BDB8935 | heber | III | שׁער | — | — | igen |
| BDB8946 | heber | II | שׁפה | — | stone |  |
| BDB8952 | heber | — | שׁפח | — | pour | igen |
| BDB8975 | heber | — | שׁפן | — | — | igen |
| BDB8977 | heber | II | שָׁפָן | proper name, masculine | — |  |
| BDB8979 | heber | — | שׁפע | — | flow abundantly, be abundant | igen |
| BDB8983 | heber | — | שׁפף | — | — | igen |
| BDB9017 | heber | II | שׁקף | — | strike | igen |
| BDB9021 | heber | — | שׁקץ | — | šikƒu | igen |
| BDB9027 | heber | — | שׁקר | — | deceive | igen |
| BDB9030 | heber | — | שׁרב | — | parch | igen |
| BDB9034 | heber | II | שׁרה | — | be moist | igen |
| BDB9036 | heber | III | שׁרה | — | short dart | igen |
| BDB9038 | heber | IV | שׁרה | — | siriyâm | igen |
| BDB9049 | heber | — | שׁרר | — | be firm sound | igen |
| BDB9057 | heber | — | שׁרשׁ | — | nerve, muscle | igen |
| BDB9076 | heber | II | שׁתה | — | set, sit | igen |
| BDB9078 | heber | III | שׁתה | — | weave | igen |
| BDB9086 | heber | — | <big>ת</big> | — | — |  |
| BDB9093 | heber | — | תאם | — | agree | igen |
| BDB9111 | heber | — | תהה | — | rage, roar | igen |
| BDB9114 | heber | — | תהם | — | tiâmtu | igen |
| BDB9118 | heber | I | תוה | — | — | igen |
| BDB9127 | heber | — | תוף | — | spit | igen |
| BDB9150 | heber | — | תכך | — | overcome | igen |
| BDB9164 | heber | I | תלל | J | heap |  |
| BDB9172 | heber | — | תלם | — | break edge of, make a breach, gap | igen |
| BDB9175 | heber | — | תלע | — | gnaw | igen |
| BDB9195 | heber | — | תמר | — | be erect, stiff | igen |
| BDB9206 | heber | — | תנך | — | — | igen |
| BDB9209 | heber | I | תנן | — | lament | igen |
| BDB9212 | heber | II | תנן | — | — | igen |
| BDB9214 | heber | — | תעב | — | — | igen |
| BDB9224 | heber | I | תפל | — | unsalted | igen |
| BDB9227 | heber | II | תפל | — | — | igen |
| BDB9230 | heber | — | תפף | — | timbrel | igen |
| BDB9266 | arameus | — | אבה | — | — | igen |
| BDB9275 | arameus | — | אוה | — | — | igen |
| BDB9277 | arameus | — | אול | — | — | igen |
| BDB9341 | arameus | — | אַרְיוֺךְ | proper name, masculine | id. |  |
| BDB9358 | arameus | — | <big>ב</big> | — | — |  |
| BDB9366 | arameus | — | בול | — | — | igen |
| BDB9451 | arameus | — | דָּכְרָן | noun [masculine] | — |  |
| BDB9463 | arameus | — | <big>ה</big> | — | — |  |
| BDB9478 | arameus | — | הרהר | — | reflect, brood impurely | igen |
| BDB9480 | arameus | — | <big>ו</big> | — | — |  |
| BDB9510 | arameus | — | חוד | — | riddle | igen |
| BDB9631 | arameus | — | <big>ל</big> | — | — |  |
| BDB9835 | arameus | II | צבע | — | — | igen |
| BDB9846 | arameus | — | <big>ק</big> | — | — |  |
| BDB9925 | arameus | — | שׁבב | — | — | igen |

## 3. A táblából hiányzó Strong-számok (OSHL-index szerint)

- A tábla sorai: 8090; OSHL-index Strong-számai (különböző, `—` nélkül): 8673; **a táblából hiányzik: 590** (heber 396, arámi 194).
- OSHL-sor Strong nélkül (`—`): nem listázható (nincs Strong-kulcs).
- Osztályok: {'masodlagos_cimke': 529, 'nincs_H_kulcs': 61}.
  - `masodlagos_cimke`: a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong **más Strong mellett** áll (pl. H0136 a BDB125-ben, [H113 H136]); a szöveg a táblában a testvér-Strong alatt már megvan.
  - `nincs_H_kulcs`: a BDB.lexicon-ban a Strongnak nincs `H<n>` kulcsa: ide a címke nélküli szócikkekből lehet párosítani (M1).
- Az ismert "396" az előfelmérés számítási módjától függ; ez a lista a teljes OSHL-indexen (heber + arámi, minden Strong, ha a táblában nincs sora) készült.

| Strong | lemma | OSHL bdb_id | def_en | nyelv | osztály | TAHOT-előfordulás |
|---|---|---|---|---|---|---|
| H0004 | אֵב | xa.aa.ac | fruit | arameus | masodlagos_cimke | 3 |
| H0007 | אֲבַד | xa.ab.aa | perish | arameus | masodlagos_cimke | 7 |
| H0013 | אׇבְדַן | a.ac.ae | destruction | heber | masodlagos_cimke | 1 |
| H0021 | אֲבִי | a.ae.ai | Abi | heber | masodlagos_cimke | 1 |
| H0025 | אֲבִי גִבְעוֹן | c.al.aj | father of Gibeon | heber | nincs_H_kulcs | 0 |
| H0038 | אֲבִיָּם | a.ae.ai | Abijam | heber | masodlagos_cimke | 5 |
| H0043 | אֶבְיָסָף | a.ae.ae | Ebiasaph | heber | masodlagos_cimke | 3 |
| H0059 | אָבֵל | a.aj.ab | Abel | heber | masodlagos_cimke | 2 |
| H0063 | אָבֵל הַשִּׁטִּים | a.aj.ab | Abelshittim | heber | masodlagos_cimke | 2 |
| H0064 | אָבֵל כְּרָמִים | a.aj.ab | plain of the vineyards | heber | masodlagos_cimke | 2 |
| H0065 | אָבֵל מְחוֹלָה | a.aj.ab | Abel-meholah | heber | masodlagos_cimke | 6 |
| H0066 | אַבֵל מַיִם | a.aj.ab | Abel-maim | heber | masodlagos_cimke | 2 |
| H0067 | אָבֵל מִצְרַיִם | a.aj.ab | Abel-mizraim | heber | masodlagos_cimke | 2 |
| H0069 | אֶ֫בֶן | xa.ac.ac | stone | arameus | masodlagos_cimke | 8 |
| H0072 | אֶבֶן הָעֵזֶר | a.am.aa | Ebenezer | heber | masodlagos_cimke | 6 |
| H0085 | אַבְרָהָם | a.ae.aw | Abraham | heber | masodlagos_cimke | 175 |
| H0121 | אָדָם | a.bc.ab | Adam | heber | masodlagos_cimke | 12 |
| H0128 | אֲדָמָה | a.bc.ac | Adamah | heber | masodlagos_cimke | 1 |
| H0136 | אֲדֹנָי | a.be.ac | lord | heber | masodlagos_cimke | 440 |
| H0144 | אֲדָר | xa.ac.af | Adar | arameus | masodlagos_cimke | 1 |
| H0169 | אֹ֫הֶל | a.bl.ab | Ohel | heber | masodlagos_cimke | 1 |
| H0206 | אָ֫וֶן | a.ca.ab | Aven | heber | masodlagos_cimke | 2 |
| H0236 | אֲזַל | xa.ag.aa | go | arameus | masodlagos_cimke | 7 |
| H0277 | אֲחִי | a.ck.ah | Ahi | heber | masodlagos_cimke | 2 |
| H0341 | אָיַב | a.cx.aa | be hostile to | heber | masodlagos_cimke | 283 |
| H0365 | אַיֶּלֶת | a.bx.au | hind | heber | masodlagos_cimke | 0 |
| H0372 | אִיעֶזֶר | a.ae.at | Jeezer | heber | masodlagos_cimke | 1 |
| H0373 | אִיעֶזְרִי | a.ae.au | an Iezrite | heber | masodlagos_cimke | 1 |
| H0388 | אֵיתָנִים | j.ee.ab | Ethanim | heber | masodlagos_cimke | 1 |
| H0399 | אֲכַל | xa.al.aa | eat | arameus | masodlagos_cimke | 7 |
| H0449 | אֱלִידָד | a.dl.al | Elidad | heber | masodlagos_cimke | 1 |
| H0462 | אֶלְיוֹעֵינַי | a.di.ac | Elienai | heber | masodlagos_cimke | 1 |
| H0506 | אֲלַ֑ף | xa.ar.ab | 1,000 | arameus | masodlagos_cimke | 4 |
| H0521 | אַמָּה | xa.ar.ac | cubit | arameus | masodlagos_cimke | 4 |
| H0524 | אֻמָּה | xa.ar.ad | nation | arameus | masodlagos_cimke | 8 |
| H0527 | אָמוֹן | a.dy.an | artificer | heber | masodlagos_cimke | 0 |
| H0532 | אָמִי | a.dv.ad | Ami | heber | masodlagos_cimke | 1 |
| H0540 | אֲמַן | xa.as.aa | trust | arameus | masodlagos_cimke | 3 |
| H0547 | אֹמְנָה | a.dy.aa | confirm | heber | masodlagos_cimke | 1 |
| H0553 | אָמֵץ | a.dz.aa | be stout | heber | nincs_H_kulcs | 41 |
| H0624 | אָסֹף | a.ev.ae | store | heber | masodlagos_cimke | 3 |
| H0638 | אַף | xa.be.aa | also | arameus | masodlagos_cimke | 4 |
| H0706 | אַרְבַּעְתַּיִם | t.al.ab | four | heber | masodlagos_cimke | 1 |
| H0711 | אַרְגְּוָן | xa.be.ah | purple | arameus | masodlagos_cimke | 3 |
| H0723 | אֻרְיָה | a.fo.ac | manger | heber | masodlagos_cimke | 3 |
| H0726 | אֲרוֹמִי | a.bd.ag | Edomite | heber | masodlagos_cimke | 0 |
| H0740 | אֲרִיאֵל | a.fo.af | Ariel | heber | masodlagos_cimke | 6 |
| H0747 | אֲרִיסַי | a.fr.ah | Arisai | heber | nincs_H_kulcs | 1 |
| H0760 | אֲרַם צוֹבָה | a.ft.aa | Aram-zobah | heber | masodlagos_cimke | 2 |
| H0763 | אֲרַם נַהֲרַיִם | a.ft.aa | Aram-naharaim | heber | masodlagos_cimke | 10 |
| H0778 | אֲרַק | xa.bi.ag | earth | arameus | masodlagos_cimke | 1 |
| H0791 | אַשְׁבֵּעַ | a.gb.ah | Ashbea | heber | nincs_H_kulcs | 1 |
| H0792 | אֶשְׁבַּעַל | a.gb.ai | Eshbaal | heber | masodlagos_cimke | 2 |
| H0798 | אַשְׁדּוֹת הַפִּסְגָּה | q.bx.ab | Ashdoth-pisgah | heber | masodlagos_cimke | 4 |
| H0799 | אֶשְׁדָּת | a.gb.aa | fire | heber | masodlagos_cimke | 0 |
| H0808 | אָשִׁישׁ | a.gl.ab | raisin-cake | heber | masodlagos_cimke | 0 |
| H0868 | אֶתְנַן | w.bf.ab | hire | heber | masodlagos_cimke | 11 |
| H0869 | אֶתְנַן | w.bf.ac | Ethnan | heber | masodlagos_cimke | 1 |
| H0876 | בְּאֵר | b.ac.ab | Beer | heber | masodlagos_cimke | 2 |
| H0879 | בְּאֵר אֵלִים | b.ac.ab | Beer-elim | heber | masodlagos_cimke | 2 |
| H0887 | בָּאַשׁ | b.ad.aa | have a bad smell | heber | masodlagos_cimke | 17 |
| H0895 | בָּבֶל | xb.ab.ad | Babylon | arameus | masodlagos_cimke | 25 |
| H0951 | בּוֹקֵר | b.cu.ac | herdsman | heber | masodlagos_cimke | 1 |
| H0989 | בְּטֵל | xb.af.aa | cease | arameus | masodlagos_cimke | 6 |
| H0997 | בֵּין | xb.af.ab | between | arameus | masodlagos_cimke | 2 |
| H0999 | בִּינָה | xb.af.ac | understanding | arameus | masodlagos_cimke | 1 |
| H1005 | בַּ֫יִת | xb.ag.aa | house | arameus | masodlagos_cimke | 44 |
| H1028 | בֵּית הָרָן | b.bp.aq | Beth-haran | heber | masodlagos_cimke | 2 |
| H1037 | בֵּית מִלּוֹא | m.bz.ag | house of Millo | heber | masodlagos_cimke | 8 |
| H1056 | בָּכָא | b.bp.cc | Baca | heber | masodlagos_cimke | 1 |
| H1070 | בֶּכֶר | b.br.ag | young camel | heber | masodlagos_cimke | 1 |
| H1073 | בִּכּוּרָה | b.br.ak | first ripe fig | heber | masodlagos_cimke | 0 |
| H1117 | בָּמָה | b.bz.af | Bamah. See also | heber | masodlagos_cimke | 1 |
| H1123 | בֵּן | xb.al.ab | son | arameus | masodlagos_cimke | 0 |
| H1143 | בֵּנַיִם | b.bo.ac | interval | heber | masodlagos_cimke | 2 |
| H1154 | בֶּסֶר | b.cd.ab | unripe | heber | masodlagos_cimke | 1 |
| H1164 | בְּעִי | p.bd.ad | ruin | heber | masodlagos_cimke | 0 |
| H1170 | בַּעַל בְּרִית | b.ci.ab | Baal-berith | heber | masodlagos_cimke | 4 |
| H1176 | בַּעַל זְבוּב | b.ci.ab | Baal-zebub | heber | masodlagos_cimke | 8 |
| H1180 | בַּעֲלִי | b.ci.ab | owner | heber | masodlagos_cimke | 1 |
| H1181 | בַּעֲלֵי בָּמוֹת | b.ci.ab | owner | heber | masodlagos_cimke | 0 |
| H1184 | בַּעֲלֵי יְהוּדָה | b.ci.ap | Baale of Judah | heber | masodlagos_cimke | 0 |
| H1194 | בְּעֹן | b.bp.ah | Beon | heber | masodlagos_cimke | 1 |
| H1208 | בָּצוֹר | b.cp.ai | vintage | heber | masodlagos_cimke | 0 |
| H1222 | בְּצַר | r.dz.ac | straits | heber | masodlagos_cimke | 0 |
| H1273 | בַּרְחֻמִי | b.dc.af | Barchumite | heber | masodlagos_cimke | 1 |
| H1286 | אֵל בְּרִית | a.dl.ab | Berith | heber | masodlagos_cimke | 1 |
| H1289 | בְּרַךְ | xb.am.aa | kneel | arameus | masodlagos_cimke | 5 |
| H1313 | בֹּ֫שֶׂם | b.di.ac | spice | heber | nincs_H_kulcs | 1 |
| H1329 | בְּתוּל | b.dm.af | Bethuel | heber | masodlagos_cimke | 1 |
| H1336 | בֶּ֫תֶר | b.dp.ab | Bether | heber | masodlagos_cimke | 1 |
| H1362 | גָּבֹהַּ | c.ah.ab | high | heber | masodlagos_cimke | 0 |
| H1400 | גְּבַר | xc.ab.ab | man | arameus | masodlagos_cimke | 21 |
| H1408 | גַּד | c.ao.ae | that troop | heber | nincs_H_kulcs | 1 |
| H1418 | גְּדוּדָה | c.ao.ac | furrow | heber | masodlagos_cimke | 0 |
| H1447 | גָּדֵר | c.at.ab | wall | heber | masodlagos_cimke | 12 |
| H1467 | גֵּוָה | xc.aa.ab | pride | arameus | masodlagos_cimke | 1 |
| H1499 | גֵּזֶל | c.bl.ab | robbery | heber | masodlagos_cimke | 0 |
| H1519 | גִּיחַ | xc.ad.ac | burst forth | arameus | nincs_H_kulcs | 1 |
| H1531 | גֻּלָּה | c.cd.ag | basin | heber | masodlagos_cimke | 0 |
| H1594 | גִּנָּה | c.cp.ac | garden | heber | masodlagos_cimke | 4 |
| H1596 | גְּנַז | xc.ah.ab | treasure | arameus | masodlagos_cimke | 3 |
| H1635 | גְּרַם | xc.ah.ad | bone | arameus | masodlagos_cimke | 1 |
| H1655 | גְּשֵׁם | xc.ah.ae | body | arameus | masodlagos_cimke | 5 |
| H1678 | דֹּב | xd.aa.ab | bear | arameus | masodlagos_cimke | 1 |
| H1693 | דְּבֵק | xd.ac.aa | cling | arameus | masodlagos_cimke | 1 |
| H1701 | דִּבְרָה | xd.ac.ab | cause | arameus | masodlagos_cimke | 2 |
| H1708 | דַּבֶּ֫שֶׁת | d.aj.ac | Dabbesheth | heber | masodlagos_cimke | 1 |
| H1746 | דּוּמָה | d.aw.ac | Dumah | heber | nincs_H_kulcs | 3 |
| H1753 | דּוּר | xd.ad.aa | dwell | arameus | masodlagos_cimke | 7 |
| H1778 | דִּין | xd.ah.aa | judge | arameus | masodlagos_cimke | 1 |
| H1815 | דְּלַק | xd.ak.aa | burn | arameus | masodlagos_cimke | 1 |
| H1821 | דְּמָה | xd.al.aa | be like | arameus | masodlagos_cimke | 2 |
| H1855 | דְּקַק | xd.an.aa | be shattered | arameus | masodlagos_cimke | 10 |
| H1859 | דָּר | xd.ad.ab | generation | arameus | masodlagos_cimke | 4 |
| H1868 | דָּֽרְיָ֫וֶשׁ | xd.an.ac | Darius | arameus | masodlagos_cimke | 15 |
| H1922 | הֲדַר | xe.ad.aa | glorify | arameus | masodlagos_cimke | 3 |
| H1939 | הוֹדַיְוָהוּ | j.at.ab | Hodaiah | heber | masodlagos_cimke | 0 |
| H1941 | הוֹדִיָּה | e.ay.ae | Hodijah | heber | masodlagos_cimke | 5 |
| H1981 | הֲלַךְ | xe.ag.aa | go | arameus | masodlagos_cimke | 3 |
| H1996 | הֲמוֹן גּוֹג | e.bt.ab | Hamon-gog | heber | masodlagos_cimke | 4 |
| H2006 | הֵן | xe.ai.aa | if | arameus | masodlagos_cimke | 19 |
| H2017 | הֹפֶךְ | e.cb.ab | the contrary | heber | masodlagos_cimke | 1 |
| H2042 | הָרָר | e.cf.ab | mountain | heber | masodlagos_cimke | 12 |
| H2088 | זֶה | g.ah.aa | this | heber | masodlagos_cimke | 1180 |
| H2089 | זֶה | u.ak.af | one of a flock | heber | masodlagos_cimke | 0 |
| H2110 | זוּן | xg.ad.aa | feed | arameus | masodlagos_cimke | 1 |
| H2112 | זוּעַ | xg.ae.aa | tremble | arameus | masodlagos_cimke | 2 |
| H2116 | זוּרֶה | g.ba.aa | press down and out | heber | masodlagos_cimke | 1 |
| H2170 | זְמָר | xg.ag.aa | music | arameus | masodlagos_cimke | 4 |
| H2176 | זִמְרָת | g.bq.ab | melody | heber | masodlagos_cimke | 3 |
| H2178 | זַן | xg.ag.ac | kind | arameus | masodlagos_cimke | 4 |
| H2185 | זֹנוֹת | g.bu.aa | commit fornication | heber | nincs_H_kulcs | 0 |
| H2189 | זַעֲוָה | g.ax.ab | a trembling | heber | masodlagos_cimke | 7 |
| H2200 | זְעִ֑ק | xg.ag.ad | cry | arameus | masodlagos_cimke | 1 |
| H2211 | זְקַף | xg.ai.aa | raise | arameus | masodlagos_cimke | 1 |
| H2214 | זָרָא | g.az.ab | loathsome thing | heber | nincs_H_kulcs | 1 |
| H2217 | זְרֻבָּבֶ֫ל | xg.ai.ab | Zerubbabel | arameus | masodlagos_cimke | 1 |
| H2234 | זְרַע | xg.ai.ac | seed | arameus | masodlagos_cimke | 1 |
| H2269 | חֲבַר | xh.ab.aa | fellow | arameus | masodlagos_cimke | 6 |
| H2298 | חַד | xa.ai.ab | one | arameus | masodlagos_cimke | 14 |
| H2305 | חֶדְוָה | xh.ab.ae | joy | arameus | masodlagos_cimke | 1 |
| H2316 | חֲדַר | h.aq.ae | Hadar | heber | masodlagos_cimke | 0 |
| H2323 | חֲדַ֑ת | xh.ab.ag | new | arameus | masodlagos_cimke | 1 |
| H2334 | חַוּוֹת יָעִיר | h.bb.ab | (Bashan-) Havoth-jair | heber | masodlagos_cimke | 8 |
| H2337 | חָוָח | h.bd.ab | brier | heber | masodlagos_cimke | 0 |
| H2358 | חִוָּר | xh.ae.ab | white | arameus | masodlagos_cimke | 1 |
| H2361 | חוּרָם | a.ck.ay | Huram. Compare | heber | masodlagos_cimke | 13 |
| H2408 | חֲטָי | xh.ag.aa | sin | arameus | masodlagos_cimke | 1 |
| H2409 | חַטָּיָא | xh.ag.ab | sin-offering | arameus | masodlagos_cimke | 0 |
| H2417 | חַי | xh.ah.ab | living | arameus | masodlagos_cimke | 7 |
| H2425 | חָיַי | h.cd.aa | live | heber | masodlagos_cimke | 1 |
| H2429 | חַ֫יִל | xh.ah.ad | power | arameus | masodlagos_cimke | 7 |
| H2439 | חִישׁ | h.bn.aa | haste | heber | masodlagos_cimke | 0 |
| H2454 | חׇכְמוֹת | h.cg.ac | wisdom | heber | masodlagos_cimke | 0 |
| H2499 | חֲלַף | xh.aj.aa | pass | arameus | masodlagos_cimke | 4 |
| H2510 | חָלָק | h.db.ac | Halak | heber | masodlagos_cimke | 2 |
| H2511 | חַלָּק | h.db.ac | smooth | heber | masodlagos_cimke | 1 |
| H2562 | חֲמַר | xh.aj.ae | wine | arameus | masodlagos_cimke | 6 |
| H2579 | חֲמַת רַבָּה | h.du.ac | Chamath-Rabbah | heber | masodlagos_cimke | 2 |
| H2589 | חַנּוֹת | h.dz.aa | shew favour | heber | masodlagos_cimke | 0 |
| H2604 | חֲנַן | xh.ak.aa | shew favour | arameus | masodlagos_cimke | 2 |
| H2618 | חֶסֶד | b.ca.am | Hesed | heber | masodlagos_cimke | 1 |
| H2699 | חֲצֵרִים | h.fb.ab | Hazerim | heber | masodlagos_cimke | 0 |
| H2702 | חֲצַר סוּסָה | h.fb.ae | Hazar-susim | heber | masodlagos_cimke | 2 |
| H2711 | חֵקֶק | h.ff.ab | something prescribed | heber | masodlagos_cimke | 2 |
| H2718 | חֲרַב | xh.an.aa | be waste | arameus | masodlagos_cimke | 1 |
| H2749 | חַרְטֹם | xh.an.ab | magician | arameus | masodlagos_cimke | 5 |
| H2753 | חֹרִי | h.gi.ad | Hori | heber | masodlagos_cimke | 4 |
| H2755 | חֲרֵי־יוֹנִים | d.af.ad | dove’s dung | heber | masodlagos_cimke | 0 |
| H2769 | חֶרְמוֹנִים | h.fv.af | the Hermonites | heber | masodlagos_cimke | 1 |
| H2783 | חֲרַץ | xh.ao.ab | loin | arameus | masodlagos_cimke | 1 |
| H2794 | חֹרֵשׁ | h.gk.aa | cut in | heber | masodlagos_cimke | 0 |
| H2798 | חֲרָשִׁים | h.gk.aa | cut in | heber | masodlagos_cimke | 1 |
| H2804 | חֲשַׁב | xh.ap.aa | think | arameus | masodlagos_cimke | 1 |
| H2824 | חֶשְׁכָה | h.gt.ad | darkness | heber | masodlagos_cimke | 1 |
| H2857 | חֲתַם | xh.at.aa | seal | arameus | masodlagos_cimke | 1 |
| H2877 | טַבָּח | xi.aa.ac | guardsman | arameus | masodlagos_cimke | 1 |
| H2890 | טְהוֹר | i.ah.ae | clean | heber | masodlagos_cimke | 1 |
| H2920 | טַל | xi.aa.ag | dew | arameus | masodlagos_cimke | 5 |
| H2924 | טָלֶה | i.au.ab | lamb | heber | masodlagos_cimke | 2 |
| H2929 | טַלְמוֹן | i.ax.ac | Talmon | heber | nincs_H_kulcs | 5 |
| H2941 | טְעֵם | xi.ab.ab | taste | arameus | masodlagos_cimke | 2 |
| H2957 | טְרַד | xi.ac.aa | chase away | arameus | masodlagos_cimke | 4 |
| H2962 | טֶ֫רֶם | i.bn.aa | not yet | heber | masodlagos_cimke | 56 |
| H3028 | יַד | xj.aa.ad | hand | arameus | masodlagos_cimke | 17 |
| H3046 | יְדַע | xj.ac.aa | know | arameus | masodlagos_cimke | 47 |
| H3052 | יְהַב | xj.ad.aa | give | arameus | masodlagos_cimke | 28 |
| H3057 | יְהֻדִיָּה | j.av.aj | Jehudijah | heber | masodlagos_cimke | 1 |
| H3069 | יְהֹוִה | e.az.ae | God | heber | masodlagos_cimke | 306 |
| H3070 | יְהֹוָה יִרְאֶה | t.ab.aa | see | heber | masodlagos_cimke | 0 |
| H3071 | יְהֹוָה נִסִּי | n.dy.ab | standard | heber | masodlagos_cimke | 0 |
| H3072 | יְהֹוָה צִדְקֵנוּ | r.ar.ab | rightness | heber | masodlagos_cimke | 0 |
| H3073 | יְהֹוָה שָׁלוֹם | v.ds.ab | completeness | heber | masodlagos_cimke | 0 |
| H3074 | יְהֹוָה שָׁמָּה | v.dv.aa | there | heber | masodlagos_cimke | 0 |
| H3090 | יְהוֹשַׁבְעַת | e.az.ax | Jehoshabeath | heber | masodlagos_cimke | 2 |
| H3099 | יוֹאָחָז | e.az.ah | Jehoahaz | heber | masodlagos_cimke | 4 |
| H3101 | יוֹאָשׁ | e.az.ai | Joash | heber | masodlagos_cimke | 47 |
| H3107 | יוֹזָבָד | e.az.aj | Josabad | heber | masodlagos_cimke | 11 |
| H3110 | יוֹחָנָן | e.az.ak | Johanan | heber | masodlagos_cimke | 22 |
| H3111 | יוֹיָדָע | e.az.al | Jehoiada | heber | masodlagos_cimke | 5 |
| H3112 | יוֹיָכִין | e.az.am | Jehoiachin | heber | masodlagos_cimke | 1 |
| H3113 | יוֹיָקִים | e.az.an | Joiakim. Compare | heber | masodlagos_cimke | 4 |
| H3114 | יוֹיָרִיב | e.az.ao | Joiarib | heber | masodlagos_cimke | 5 |
| H3122 | יוֹנָדָב | e.az.aq | Jonadab | heber | masodlagos_cimke | 7 |
| H3129 | יוֹנָתָן | e.az.ar | Jonathan | heber | masodlagos_cimke | 43 |
| H3130 | יוֹסֵף | j.bz.ab | Joseph. Compare | heber | masodlagos_cimke | 213 |
| H3137 | יוֹקִים | e.az.an | Jokim | heber | masodlagos_cimke | 1 |
| H3141 | יוֹרָם | e.az.aw | Joram | heber | masodlagos_cimke | 20 |
| H3146 | יוֹשָׁפָט | e.az.bb | Joshaphat | heber | masodlagos_cimke | 2 |
| H3159 | יִזְרְעֵאלִית | g.cl.ag | a Jezreelitess | heber | masodlagos_cimke | 0 |
| H3185 | יַחְצִיאֵל | h.ex.af | Jahziel. Compare | heber | masodlagos_cimke | 1 |
| H3186 | יָחַר | a.cp.aa | to remain behind | heber | masodlagos_cimke | 0 |
| H3197 | יך | j.bk.ac | a hand | heber | masodlagos_cimke | 0 |
| H3212 | יָלַךְ | e.bn.aa | go | heber | masodlagos_cimke | 0 |
| H3221 | יַם | xj.ag.ab | sea | arameus | masodlagos_cimke | 2 |
| H3231 | יָמַן | j.bs.ae | go to | heber | masodlagos_cimke | 4 |
| H3240 | יָנַח | n.by.aa | rest | heber | masodlagos_cimke | 0 |
| H3249 | יסור | o.au.af | departing | heber | masodlagos_cimke | 0 |
| H3252 | יִסְכָּה | j.by.ab | Iscah | heber | nincs_H_kulcs | 1 |
| H3255 | יְסַף | xj.ah.aa | add | arameus | masodlagos_cimke | 1 |
| H3273 | יְעִיאֵל | j.cc.ac | Jeiel | heber | masodlagos_cimke | 14 |
| H3274 | יְעִישׁ | p.bs.ab | Jeush (from the margin). Compare | heber | masodlagos_cimke | 0 |
| H3292 | יַעֲקָן | p.ey.ad | Jaakan. Compare | heber | masodlagos_cimke | 1 |
| H3301 | יִפְדְּיָה | j.cm.ai | Iphedeiah | heber | nincs_H_kulcs | 1 |
| H3340 | יִצְרִי | j.cv.ad | Jezerites | heber | masodlagos_cimke | 1 |
| H3345 | יְקַד | xj.ak.aa | burn | arameus | masodlagos_cimke | 8 |
| H3347 | יׇקְדְעָם | j.cy.ae | Jokdeam | heber | masodlagos_cimke | 1 |
| H3367 | יְקָר | xj.ak.ac | honour | arameus | masodlagos_cimke | 7 |
| H3393 | יְרַח | xj.ak.af | month | arameus | masodlagos_cimke | 2 |
| H3421 | יׇרְקְעָ֑ם | j.do.ah | Jorkeam | heber | nincs_H_kulcs | 1 |
| H3443 | יֵשׁוּעַ | xj.ak.ai | Jeshua | arameus | masodlagos_cimke | 1 |
| H3479 | יִשְׂרָאֵל | xj.ak.ah | Israel | arameus | masodlagos_cimke | 8 |
| H3482 | יִשְׂרְאֵלִית | u.ce.ac | Jisreelitess | heber | masodlagos_cimke | 0 |
| H3487 | יָת | xj.am.aa | sign of the object of a verb | arameus | masodlagos_cimke | 1 |
| H3542 | כָּה | xk.ab.aa | here | arameus | masodlagos_cimke | 1 |
| H3549 | כָּהֵן | xk.ac.ab | priest | arameus | masodlagos_cimke | 8 |
| H3567 | כּ֫וֹרֶשׁ | xk.ac.ae | Cyrus | arameus | masodlagos_cimke | 8 |
| H3571 | כּוּשִׁית | k.az.ac | a Cushite woman | heber | masodlagos_cimke | 0 |
| H3606 | כֹּל | xk.ad.ab | the whole | arameus | masodlagos_cimke | 82 |
| H3613 | כָּלֵב אֶפְרָתָה | a.fh.ag | Caleb-ephrathah | heber | masodlagos_cimke | 2 |
| H3635 | כְּלַל | xk.ad.aa | complete | arameus | masodlagos_cimke | 7 |
| H3652 | כֵּן | xk.ad.ac | thus | arameus | masodlagos_cimke | 8 |
| H3659 | כׇּנְיָהוּ | e.az.am | Coniah | heber | masodlagos_cimke | 3 |
| H3661 | כָּנַן | k.cb.ac | support | heber | masodlagos_cimke | 0 |
| H3696 | כִּסְלֹת תָּבֹר | k.cj.aj | Chisloth-tabor | heber | masodlagos_cimke | 2 |
| H3726 | כְּפַר הָעַמּוֹנִי | k.cv.ad | village | heber | masodlagos_cimke | 1 |
| H3743 | כְּרוּב | k.da.ac | Cherub | heber | masodlagos_cimke | 2 |
| H3762 | כַּרְמְלִית | k.dd.ag | the Carmelite | heber | masodlagos_cimke | 0 |
| H3769 | כָּרַר | k.df.aa | dancing | heber | masodlagos_cimke | 2 |
| H3773 | כָּרֻתָה | k.dh.aa | cut off | heber | masodlagos_cimke | 3 |
| H3790 | כְּתַב | xk.aj.aa | write | arameus | masodlagos_cimke | 8 |
| H3797 | כְּתַל | xk.aj.ac | wall | arameus | masodlagos_cimke | 2 |
| H3821 | לֵב | xl.ad.ab | heart | arameus | masodlagos_cimke | 1 |
| H3825 | לְבַב | xl.ad.aa | heart | arameus | masodlagos_cimke | 7 |
| H3827 | לַבָּה | l.am.ac | flame | heber | masodlagos_cimke | 1 |
| H3831 | לְבוּשׁ | xl.ae.ab | garment | arameus | masodlagos_cimke | 2 |
| H3840 | לְבֵנָה | l.ak.an | brick | heber | masodlagos_cimke | 0 |
| H3848 | לְבֵשׁ | xl.ae.aa | be clothed | arameus | masodlagos_cimke | 3 |
| H3861 | לָהֵן | xl.ag.aa | except | arameus | masodlagos_cimke | 7 |
| H3866 | לוּדִי | l.ar.ae | Ludim. Lydians | heber | masodlagos_cimke | 3 |
| H3879 | לֵוָי | xl.ag.ab | Levite | arameus | masodlagos_cimke | 4 |
| H3909 | לָט | l.ax.ab | secrecy | heber | masodlagos_cimke | 6 |
| H3916 | לֵילָא | xl.ag.af | night | arameus | masodlagos_cimke | 5 |
| H3945 | לָצַץ | l.bn.aa | scorn | heber | nincs_H_kulcs | 0 |
| H3961 | לִשָּׁן | xl.ag.ag | tongue | arameus | masodlagos_cimke | 7 |
| H3969 | מְאָה | xm.aa.ab | hundred | arameus | masodlagos_cimke | 8 |
| H3997 | מְבוֹאָה | b.ap.ac | entrance | heber | masodlagos_cimke | 1 |
| H4036 | מָגוֹר מִסָּבִיב | o.ad.ac | Magormissabib | heber | masodlagos_cimke | 2 |
| H4040 | מְגִלָּה | xc.ag.ad | roll | arameus | masodlagos_cimke | 1 |
| H4059 | מָדַד | m.al.aa | measure | heber | masodlagos_cimke | 0 |
| H4078 | מַדַּי | d.bg.aa | sufficiency | heber | masodlagos_cimke | 0 |
| H4079 | מָדוֹן | d.bh.ah | strife | heber | masodlagos_cimke | 10 |
| H4090 | מְדָן | d.bh.ah | strife | heber | masodlagos_cimke | 2 |
| H4092 | מִדְיָנִי | d.bh.al | Midianite | heber | masodlagos_cimke | 1 |
| H4101 | מָה | xm.ab.aa | what? | arameus | masodlagos_cimke | 13 |
| H4109 | מַהֲלָךְ | e.bn.ae | walk | heber | masodlagos_cimke | 5 |
| H4118 | מַהֵר | m.aq.ab | hastening | heber | nincs_H_kulcs | 14 |
| H4123 | מַֽהֲתַלּוֹת | w.au.ab | illusions | heber | nincs_H_kulcs | 1 |
| H4138 | מוֹלֶ֫דֶת | j.bn.ai | kindred | heber | nincs_H_kulcs | 22 |
| H4142 | מוּסַבָּה | o.ad.aa | turn about | heber | nincs_H_kulcs | 0 |
| H4146 | מוֹסָדָה | j.bx.ag | foundation | heber | masodlagos_cimke | 5 |
| H4153 | מוֹעַדְיָה | m.cu.ac | Moadiah. Compare | heber | masodlagos_cimke | 1 |
| H4154 | מוּעֶדֶת | m.cu.aa | slip | heber | masodlagos_cimke | 0 |
| H4176 | מוֹרֶה | j.di.ae | teacher | heber | masodlagos_cimke | 3 |
| H4178 | מוֹרָט | m.dm.aa | make smooth | heber | masodlagos_cimke | 0 |
| H4193 | מוֹת | xm.ab.ab | death | arameus | masodlagos_cimke | 1 |
| H4195 | מוֹתָר | j.ef.ao | abundance | heber | nincs_H_kulcs | 3 |
| H4215 | מְזָרֶה | g.ci.aa | scatter | heber | masodlagos_cimke | 1 |
| H4282 | מַחֲרֶ֫שֶׁת | h.gk.ae | ploughshare | heber | masodlagos_cimke | 0 |
| H4319 | מִיכָהוּ | m.bu.ad | Micaiah (2 Chronicles 18:8) | heber | masodlagos_cimke | 0 |
| H4328 | מְיֻסָּדָה | j.bx.af | foundation | heber | masodlagos_cimke | 0 |
| H4333 | מִישָׁאֵל | xm.ad.ab | Mishael | arameus | masodlagos_cimke | 1 |
| H4336 | מֵישַׁךְ | xm.ad.ac | Meshak | arameus | masodlagos_cimke | 14 |
| H4342 | מַכְבִּיר | k.ak.aa | be much | heber | masodlagos_cimke | 1 |
| H4389 | מַכְתֵּשׁ | k.du.ab | Maktesh | heber | masodlagos_cimke | 1 |
| H4391 | מְלָא | xm.ae.aa | fill | arameus | masodlagos_cimke | 2 |
| H4415 | מְלַח | xm.af.ab | eat salt | arameus | masodlagos_cimke | 1 |
| H4430 | מֶ֫לֶךְ | xm.ag.ab | king | arameus | masodlagos_cimke | 180 |
| H4444 | מַלְכִּישׁוּעַ | m.cd.as | Malchishua | heber | masodlagos_cimke | 10 |
| H4504 | מִנְחָה | xm.al.ad | gift | arameus | masodlagos_cimke | 2 |
| H4509 | מִנְיָמִין | m.bu.as | Miniamin. Compare | heber | masodlagos_cimke | 3 |
| H4559 | מִסְפֶּרֶת | o.ck.ai | Mispereth. Compare | heber | masodlagos_cimke | 1 |
| H4593 | מָעֹט | m.dm.aa | make smooth | heber | masodlagos_cimke | 1 |
| H4610 | מַעֲלֵה עַקְרַבִּים | p.cs.al | ascent | heber | masodlagos_cimke | 4 |
| H4629 | מַעֲרֶה | p.fi.ae | bare | heber | masodlagos_cimke | 2 |
| H4632 | מְעָרָה | p.ft.ab | Mearah | heber | masodlagos_cimke | 1 |
| H4648 | מְפִיבֹשֶׁת | t.cm.al | Mephibosheth | heber | nincs_H_kulcs | 18 |
| H4663 | מִפְקָד | q.co.ah | Miphkad | heber | masodlagos_cimke | 0 |
| H4678 | מַצֶּבֶת | n.ep.ai | pillar | heber | masodlagos_cimke | 6 |
| H4704 | מִצְּעִירָה | r.dd.ac | little | heber | masodlagos_cimke | 0 |
| H4725 | מָקוֹם | s.av.am | standing-place | heber | nincs_H_kulcs | 401 |
| H4756 | מָרֵא | xm.al.aj | lord | arameus | nincs_H_kulcs | 4 |
| H4798 | מַרְזֵחַ | t.bt.ab | cry | heber | masodlagos_cimke | 1 |
| H4804 | מְרַט | xm.am.aa | pluck | arameus | masodlagos_cimke | 1 |
| H4810 | מְרִי בַעַל | t.cm.al | Meri-baal. Compare | heber | nincs_H_kulcs | 2 |
| H4827 | מֵרַע | t.dq.af | be evil | heber | masodlagos_cimke | 1 |
| H4873 | מֹשֶׁה | xm.am.ab | Moses | arameus | masodlagos_cimke | 1 |
| H4887 | מְשַׁח | xm.am.ac | oil | arameus | masodlagos_cimke | 2 |
| H4921 | מְשִׁלֵּמִית | v.ds.ap | Meshillemith. Compare | heber | masodlagos_cimke | 1 |
| H4930 | מַשְׂמְרָה | o.bw.ac | nail | heber | masodlagos_cimke | 1 |
| H4961 | מִשְׁתֶּה | xv.bh.ab | feast | arameus | masodlagos_cimke | 1 |
| H4965 | מֶתֶג הָאַמָּה | m.eb.ab | Metheg-ammah | heber | masodlagos_cimke | 2 |
| H4972 | מַתְּלָאָה | l.ad.ab | weariness | heber | nincs_H_kulcs | 0 |
| H4973 | מְתַלְּעוֹת | w.aw.ag | teeth | heber | masodlagos_cimke | 3 |
| H4988 | מָתֹק | m.ef.aa | become sweet | heber | masodlagos_cimke | 0 |
| H5013 | נבא | xn.aa.aa | see | arameus | masodlagos_cimke | 1 |
| H5020 | נְבוּכַדְנֶצַּר | xn.aa.ad | Nebuchadnezzar | arameus | masodlagos_cimke | 31 |
| H5103 | נְהַר | xn.ad.ac | river | arameus | masodlagos_cimke | 15 |
| H5111 | נוּד | xn.ae.aa | flee | arameus | masodlagos_cimke | 1 |
| H5182 | נְחֵת | xn.ag.aa | descend | arameus | masodlagos_cimke | 6 |
| H5191 | נְטַל | xn.ah.aa | lift | arameus | masodlagos_cimke | 2 |
| H5211 | נִיס | n.cc.aa | flee | heber | nincs_H_kulcs | 0 |
| H5227 | נֹ֫כַח | n.dl.ab | front | heber | masodlagos_cimke | 25 |
| H5229 | נְכֹחָה | n.dl.ac | straight | heber | masodlagos_cimke | 4 |
| H5256 | נְסַח | xn.aj.aa | pull away | arameus | masodlagos_cimke | 1 |
| H5260 | נְסַךְ | xn.ak.aa | pour out | arameus | masodlagos_cimke | 1 |
| H5267 | נְסַק | xo.ae.aa | come up | arameus | masodlagos_cimke | 1 |
| H5297 | נֹף | m.da.av | Noph | heber | masodlagos_cimke | 7 |
| H5304 | נְפוּסִים | n.ej.ah | Nephusim (from the margin) | heber | masodlagos_cimke | 1 |
| H5308 | נְפַל | xn.al.aa | fall | arameus | masodlagos_cimke | 11 |
| H5326 | נִצְבָּה | xn.am.ac | firmness | arameus | masodlagos_cimke | 1 |
| H5330 | נְצַח | xn.an.aa | distinguish oneself | arameus | masodlagos_cimke | 1 |
| H5338 | נְצַל | xn.ao.aa | rescue | arameus | masodlagos_cimke | 3 |
| H5368 | נְקַשׁ | xn.ap.aa | knock | arameus | masodlagos_cimke | 1 |
| H5372 | נִרְגָּן | t.at.aa | murmur | heber | masodlagos_cimke | 0 |
| H5376 | נְשָׂא | xn.aq.aa | lift | arameus | masodlagos_cimke | 3 |
| H5383 | נָשָׁה | n.ft.aa | lend | heber | masodlagos_cimke | 12 |
| H5396 | נִשְׁמָא | xn.aq.ac | breath | arameus | masodlagos_cimke | 1 |
| H5415 | נְתַן | xn.ar.aa | give | arameus | masodlagos_cimke | 7 |
| H5463 | סְגַר | xo.ac.ad | shut | arameus | masodlagos_cimke | 1 |
| H5472 | סוּג | o.am.aa | move away | heber | masodlagos_cimke | 14 |
| H5494 | סוּר | o.au.aa | turn aside | heber | masodlagos_cimke | 2 |
| H5503 | סָחַר | o.az.aa | go around | heber | nincs_H_kulcs | 21 |
| H5505 | סָ֫חַר | o.az.ab | traffic | heber | masodlagos_cimke | 0 |
| H5574 | סְנוּאָה | o.bw.ah | Hasenuah (including the art) | heber | masodlagos_cimke | 1 |
| H5598 | סִפַּי | o.ci.ae | Sippai. Compare | heber | masodlagos_cimke | 1 |
| H5626 | בּוֹר הַסִּרָה | b.ac.an | Sirah. See also | heber | masodlagos_cimke | 1 |
| H5635 | סָרַף | u.cj.aa | burn | heber | masodlagos_cimke | 1 |
| H5668 | עָבוּר | p.ah.am | for the sake of | heber | nincs_H_kulcs | 49 |
| H5673 | עֲבִידָה | xp.aa.ad | work | arameus | masodlagos_cimke | 6 |
| H5686 | עָבַת | p.aj.aa | wind | heber | nincs_H_kulcs | 1 |
| H5687 | עָבוֹת | p.aj.ab | interwoven | heber | nincs_H_kulcs | 4 |
| H5722 | עֲדִינוֹ | p.au.ah | Adino | heber | masodlagos_cimke | 1 |
| H5735 | עֲדְעָדָה | p.fu.ae | Adadah | heber | masodlagos_cimke | 1 |
| H5745 | עוֹבָל | p.af.ab | Obal | heber | masodlagos_cimke | 1 |
| H5751 | עוֹד | xp.ad.aa | still | arameus | masodlagos_cimke | 1 |
| H5758 | עֲוָיָה | xp.ad.ab | iniquity | arameus | masodlagos_cimke | 1 |
| H5761 | עַוִּים | p.bf.ad | Avim | heber | masodlagos_cimke | 4 |
| H5776 | עוֹף | xp.ad.ac | fowl | arameus | masodlagos_cimke | 2 |
| H5815 | עֲזִיאֵל | p.bx.ap | Aziel. Compare | heber | nincs_H_kulcs | 1 |
| H5831 | עֶזְרָא | xp.ad.ag | Ezra | arameus | masodlagos_cimke | 3 |
| H5839 | עֲזַרְיָה | xp.ad.ah | Azariah | arameus | masodlagos_cimke | 1 |
| H5843 | עֵטָא | xj.ai.ac | counsel | arameus | masodlagos_cimke | 1 |
| H5853 | עַטְרוֹת אַדָּר | p.ch.ae | Ataroth-adar(-addar) | heber | masodlagos_cimke | 4 |
| H5855 | עַטְרוֹת שׁוֹפָן | p.ch.ae | Atroth | heber | masodlagos_cimke | 2 |
| H5858 | עֵיבָל | p.af.ab | Ebal | heber | nincs_H_kulcs | 8 |
| H5863 | עִיֵּי הָעֲבָרִים | p.cj.ae | Ije-abarim | heber | nincs_H_kulcs | 4 |
| H5865 | עֵילוֹם | p.cz.ab | long duration | heber | masodlagos_cimke | 1 |
| H5870 | עַ֫יִן | xp.ad.aj | eye | arameus | masodlagos_cimke | 5 |
| H5875 | עֵין הַקּוֹרֵא | p.ck.ac | En-hakhore | heber | masodlagos_cimke | 2 |
| H5881 | עֵינָן | p.ck.aq | Enan. Compare | heber | masodlagos_cimke | 5 |
| H5883 | עֵין רֹגֵל | p.ck.ac | En-rogel | heber | masodlagos_cimke | 8 |
| H5886 | עֵין תַּנִּים | p.ck.ac | dragon well | heber | masodlagos_cimke | 0 |
| H5888 | עִיף | p.cm.aa | be faint | heber | masodlagos_cimke | 5 |
| H5899 | עִיר הַתְּמָרִים | p.cm.ai | the city of palmtrees | heber | masodlagos_cimke | 8 |
| H5917 | עָכָר | p.co.ab | Achar. Compare | heber | masodlagos_cimke | 1 |
| H5921 | כִּי עַל כֵּן | k.bg.ac | forasmuch as | heber | masodlagos_cimke | 5768 |
| H5932 | עַלְוָה | p.bi.ad | injustice | heber | masodlagos_cimke | 1 |
| H5946 | עֶלְיוֹן | xp.ae.ad | Supreme | arameus | masodlagos_cimke | 4 |
| H5961 | עֲלָמוֹת | p.cy.ac | young woman | heber | masodlagos_cimke | 3 |
| H5972 | עַם | xp.ag.ag | people | arameus | masodlagos_cimke | 15 |
| H5974 | עִם | xp.ah.aa | with | arameus | masodlagos_cimke | 22 |
| H5976 | עָמַד | m.cu.aa | slip | heber | masodlagos_cimke | 1 |
| H5978 | עִמָּד | p.dj.aa | with | heber | masodlagos_cimke | 42 |
| H5985 | עַמּוֹנִית | p.dj.ah | Ammonite | heber | masodlagos_cimke | 0 |
| H5993 | עַמִּי נָדִיב | p.di.ab | Amminadib | heber | masodlagos_cimke | 0 |
| H6032 | עֲנָה | xp.ai.aa | answer | arameus | masodlagos_cimke | 30 |
| H6038 | עֲנָוָה | p.dv.ac | humility | heber | masodlagos_cimke | 5 |
| H6046 | עָנֵם | p.ck.af | Anem | heber | masodlagos_cimke | 1 |
| H6062 | עֲנָקִי | p.eb.ab | Anakim | heber | masodlagos_cimke | 9 |
| H6077 | עֹ֫פֶל | p.ee.ab | Ophel | heber | masodlagos_cimke | 5 |
| H6112 | עֵצֶן | p.au.ah | voluptuous | heber | nincs_H_kulcs | 1 |
| H6159 | עֹרֵב | p.fg.ac | Oreb | heber | masodlagos_cimke | 7 |
| H6164 | עַרְבָתִי | b.bp.bo | place of the depression | heber | masodlagos_cimke | 2 |
| H6165 | עָרַג | p.fh.aa | long for | heber | nincs_H_kulcs | 3 |
| H6173 | עַרְוָה | xp.ao.ac | dishonour | arameus | masodlagos_cimke | 1 |
| H6255 | עַשְׁתְּרֹת קַרְנַיִם | p.gh.ah | Ashtoreth Karnaim | heber | masodlagos_cimke | 2 |
| H6263 | עֲתִיד | xp.aq.ae | ready | arameus | masodlagos_cimke | 1 |
| H6268 | עַתִּיק | xp.aq.af | advanced | arameus | masodlagos_cimke | 3 |
| H6358 | פָּטוּר | q.bg.aa | separate | heber | masodlagos_cimke | 0 |
| H6359 | פָּטִיר | q.bg.aa | separate | heber | masodlagos_cimke | 0 |
| H6366 | פֵּיָה | q.al.aa | mouth | heber | masodlagos_cimke | 1 |
| H6374 | פִּיפִיָּה | q.al.aa | mouth | heber | masodlagos_cimke | 2 |
| H6386 | פְּלַג | xq.ab.aa | divide | arameus | masodlagos_cimke | 1 |
| H6407 | פַּלְטִי | b.bp.bp | Paltite | heber | masodlagos_cimke | 1 |
| H6422 | פַּלְמוֹנִי | q.bm.ab | a certain one | heber | masodlagos_cimke | 1 |
| H6433 | פֻּם | xq.ac.ac | mouth | arameus | masodlagos_cimke | 6 |
| H6438 | פִּנָּה | q.bv.ab | corner | heber | masodlagos_cimke | 29 |
| H6450 | פַּס דַּמִּים | a.fd.ad | Pas-dammim. Compare | heber | masodlagos_cimke | 2 |
| H6512 | פֵּרָה | h.es.af | mole | heber | masodlagos_cimke | 1 |
| H6546 | פֶּ֫רַע | q.df.ab | leader | heber | masodlagos_cimke | 2 |
| H6559 | פְּרָצִים | q.di.ac | Perazim | heber | masodlagos_cimke | 1 |
| H6560 | פֶּרֶץ עֻזָּא | q.di.ac | Perezuzza | heber | masodlagos_cimke | 4 |
| H6565 | פָּרַר | q.dl.aa | break | heber | masodlagos_cimke | 50 |
| H6568 | פְּרַשׁ | xq.ag.aa | make distinct | arameus | masodlagos_cimke | 1 |
| H6606 | פְּתַח | xq.ai.aa | open | arameus | masodlagos_cimke | 2 |
| H6702 | צוּת | j.cw.aa | kindle | heber | masodlagos_cimke | 1 |
| H6708 | צְחִיחִי | r.bp.ac | shining | heber | nincs_H_kulcs | 0 |
| H6737 | צָיַר | r.ay.ad | supply oneself with provisions | heber | masodlagos_cimke | 1 |
| H6744 | צְלַח | xr.ae.aa | prosper | arameus | masodlagos_cimke | 4 |
| H6752 | צֵלֶל | r.cc.ab | shadow | heber | masodlagos_cimke | 4 |
| H6755 | צְלֵם | xr.ae.ab | image | arameus | masodlagos_cimke | 17 |
| H6799 | צְנָן | r.ab.ac | Zenan | heber | masodlagos_cimke | 1 |
| H6820 | צֹ֫עַר | r.dd.ab | Zoar | heber | masodlagos_cimke | 10 |
| H6827 | צְפוֹן | r.df.ae | Zephon | heber | masodlagos_cimke | 1 |
| H6839 | צֹפִים | r.df.aa | Zophim | heber | masodlagos_cimke | 1 |
| H6853 | צְפַר | xr.ae.ac | bird | arameus | masodlagos_cimke | 4 |
| H6897 | קֹבָה | s.ad.ab | stomach | heber | masodlagos_cimke | 1 |
| H6902 | קַבֵּל | xs.aa.ac | receive | arameus | masodlagos_cimke | 3 |
| H6905 | קָבָל | s.ae.ab | presence | heber | masodlagos_cimke | 1 |
| H6909 | קַבְצְאֵל | s.ag.ad | Kabzeel. Compare | heber | masodlagos_cimke | 3 |
| H6919 | קָדַח | s.ak.aa | be kindled | heber | nincs_H_kulcs | 5 |
| H6928 | קַדְמָה | xs.aa.ae | former time | arameus | masodlagos_cimke | 2 |
| H6944 | קֹ֫דֶשׁ | s.an.ab | apartness | heber | masodlagos_cimke | 469 |
| H6947 | קָדֵשׁ בַּרְנֵעַ | s.an.ag | Kadeshbarnea | heber | masodlagos_cimke | 20 |
| H6948 | קְדֵשָׁה | s.an.ae | temple-prostitute | heber | masodlagos_cimke | 5 |
| H6961 | קוה | s.aq.ac | cord | heber | masodlagos_cimke | 0 |
| H6966 | קוּם | xs.ad.aa | arise | arameus | masodlagos_cimke | 35 |
| H6978 | קַוְקָו | s.aq.ad | might | heber | masodlagos_cimke | 4 |
| H6987 | קֹטֶב | s.bc.ab | destruction | heber | masodlagos_cimke | 1 |
| H6990 | קוֹט | s.at.aa | break | heber | masodlagos_cimke | 1 |
| H6992 | קְטַל | xs.ae.aa | slay | arameus | masodlagos_cimke | 7 |
| H7006 | קָיָה | s.bj.aa | vomit | heber | masodlagos_cimke | 1 |
| H7019 | קַ֫יִץ | s.bm.ab | summer | heber | masodlagos_cimke | 20 |
| H7029 | קִישִׁי | s.bb.ab | Kishi | heber | masodlagos_cimke | 1 |
| H7041 | קֵלָיָה | s.au.ac | Kelaiah | heber | masodlagos_cimke | 1 |
| H7063 | קִמָּשׂוֹן | s.bz.ab | thistles | heber | masodlagos_cimke | 1 |
| H7083 | קֶ֫סֶת | s.dn.ac | pot | heber | nincs_H_kulcs | 3 |
| H7113 | קְצַץ | xs.ah.aa | cut off | arameus | nincs_H_kulcs | 1 |
| H7118 | קְצָת | xs.ah.ab | end | arameus | masodlagos_cimke | 3 |
| H7119 | קַר | s.dk.ab | cool | heber | nincs_H_kulcs | 2 |
| H7125 | קִרְאָה | s.cz.aa | encounter | heber | masodlagos_cimke | 0 |
| H7127 | קְרֵב | xs.ak.aa | approach | arameus | masodlagos_cimke | 9 |
| H7162 | קֶ֫רֶן | xs.ak.ad | horn | arameus | masodlagos_cimke | 14 |
| H7178 | קַרְתָּן | s.dc.aj | Kartan | heber | masodlagos_cimke | 1 |
| H7201 | רָאָה | d.ad.ab | kite | heber | masodlagos_cimke | 1 |
| H7207 | רַאֲוָה | t.ab.aa | see | heber | masodlagos_cimke | 0 |
| H7226 | רַאֲשֹׁת | t.ad.ai | place at the head | heber | masodlagos_cimke | 1 |
| H7252 | רֶבַע | t.am.aa | lie stretched out | heber | masodlagos_cimke | 1 |
| H7260 | רַבְרַב | xt.ab.ab | great | arameus | masodlagos_cimke | 8 |
| H7262 | רַבְשָׁקֵה | t.ae.ac | chief | heber | masodlagos_cimke | 32 |
| H7265 | רְגַז | xt.ae.aa | enrage | arameus | masodlagos_cimke | 1 |
| H7294 | רַ֫הַב | t.bd.ad | Rahab | heber | masodlagos_cimke | 4 |
| H7313 | רוּם | xt.ah.aa | rise | arameus | masodlagos_cimke | 4 |
| H7358 | רֶ֫חֶם | t.bz.ab | womb | heber | masodlagos_cimke | 26 |
| H7361 | רַחֲמָה | t.bz.ab | womb | heber | masodlagos_cimke | 0 |
| H7412 | רְמָא | xt.ak.aa | cast | arameus | masodlagos_cimke | 12 |
| H7421 | רַמִּי | a.ft.ab | Aramæan | heber | masodlagos_cimke | 1 |
| H7427 | רוֹמֵמוּת | t.bm.ao | uprising | heber | masodlagos_cimke | 1 |
| H7432 | רֶמֶת | t.bm.ak | Remeth | heber | masodlagos_cimke | 1 |
| H7433 | רָמֹת גִּלעָד | t.bm.ak | Ramoth-gilead | heber | masodlagos_cimke | 1 |
| H7434 | רָמַת הַמִּצְפֶּה | t.bm.aj | Ramath-mizpeh | heber | masodlagos_cimke | 2 |
| H7436 | רָמָתַיִם צוֹפִים | r.be.ad | Ramathaimzophim | heber | masodlagos_cimke | 2 |
| H7437 | רָמַת לֶחִי | t.bm.aj | Ramath-lehi | heber | masodlagos_cimke | 2 |
| H7444 | רַנֵּן | t.de.aa | give a ringing cry | heber | masodlagos_cimke | 0 |
| H7465 | רֹעָה | t.dr.aa | break | heber | masodlagos_cimke | 1 |
| H7485 | רַעַמְיָה | t.dn.af | Raamiah | heber | masodlagos_cimke | 1 |
| H7512 | רְפַס | xt.an.aa | tread | arameus | masodlagos_cimke | 2 |
| H7515 | רָפַשׂ | t.dy.aa | stamp | heber | masodlagos_cimke | 3 |
| H7529 | רֶצֶף | t.ei.ab | glowing stone | heber | masodlagos_cimke | 1 |
| H7535 | רַק | t.ep.ab | leanness | heber | masodlagos_cimke | 109 |
| H7560 | רְשַׁם | xt.ao.aa | inscribe | arameus | masodlagos_cimke | 7 |
| H7572 | רַתִּיקָה | t.ey.ac | chain | heber | masodlagos_cimke | 0 |
| H7593 | שְׁאֵל | xv.aa.aa | ask | arameus | masodlagos_cimke | 6 |
| H7598 | שְׁאַלְתִּיאֵל | xv.aa.ac | Shealtiel | arameus | masodlagos_cimke | 1 |
| H7606 | שְׁאָר | xv.aa.ad | rest | arameus | masodlagos_cimke | 12 |
| H7608 | שַׁאֲרָה | v.al.ab | flesh | heber | masodlagos_cimke | 1 |
| H7638 | שָׂבָךְ | u.ac.ac | lattice-work | heber | nincs_H_kulcs | 0 |
| H7654 | שׇׂבְעָה | u.ad.ac | satiety | heber | masodlagos_cimke | 6 |
| H7658 | שִׁבְעָ֫נָה | v.av.ae | seven | heber | masodlagos_cimke | 1 |
| H7671 | שְׁבָרִים | v.ay.ab | Shebarim | heber | masodlagos_cimke | 1 |
| H7695 | שֵׁגָל | xv.af.ab | consort | arameus | masodlagos_cimke | 3 |
| H7715 | שַׁדְרַךְ | xv.ag.ac | Shadrach | arameus | masodlagos_cimke | 14 |
| H7721 | שׂוֹא | n.fm.aa | lift | heber | nincs_H_kulcs | 0 |
| H7734 | שׂוּג | o.am.aa | move away | heber | masodlagos_cimke | 1 |
| H7735 | שׂוּג | o.an.aa | fence about | heber | masodlagos_cimke | 1 |
| H7736 | שׁוּד | v.bg.aa | deal violently with | heber | nincs_H_kulcs | 1 |
| H7738 | שָׁוָה | v.bm.ae | noise | heber | masodlagos_cimke | 0 |
| H7742 | שׂוּחַ | v.bs.aa | go about | heber | nincs_H_kulcs | 1 |
| H7765 | שׁוּנִי | v.bu.ag | a Shunite | heber | masodlagos_cimke | 1 |
| H7773 | שֶׁוַע | v.bv.aa | cry out | heber | masodlagos_cimke | 1 |
| H7780 | שׁוֹפָךְ | v.bn.ap | Shophach | heber | masodlagos_cimke | 2 |
| H7792 | שׁוּר | xv.ak.ac | wall | arameus | masodlagos_cimke | 3 |
| H7798 | שַׁוְשָׁא | u.ce.ad | Shavsha | heber | nincs_H_kulcs | 1 |
| H7820 | שָׁחַט | v.ci.aa | slaughter | heber | masodlagos_cimke | 5 |
| H7824 | שָׁחִיף | u.au.ab | panelled | heber | nincs_H_kulcs | 1 |
| H7864 | שְׁיָא | v.bk.ai | Sheva (from the margin) | heber | nincs_H_kulcs | 0 |
| H7873 | שִׂיג | o.am.ac | a moving back | heber | masodlagos_cimke | 1 |
| H7917 | שְׂכִירָה | u.bk.ae | hired | heber | masodlagos_cimke | 1 |
| H7929 | שִׁכְמָה | v.dd.ab | shoulder | heber | masodlagos_cimke | 1 |
| H7930 | שִׁכְמִי | v.dd.af | Shikmite | heber | nincs_H_kulcs | 1 |
| H7932 | שְׁכֵן | xv.ap.aa | dwell | arameus | masodlagos_cimke | 2 |
| H7953 | שָׁלָה | v.dk.aa | draw out | heber | masodlagos_cimke | 1 |
| H7960 | שָׁלוּ | xv.aq.ac | neglect | arameus | masodlagos_cimke | 4 |
| H7968 | שַׁלּוּן | v.ds.an | Shallum | heber | masodlagos_cimke | 1 |
| H7972 | שְׁלַח | xv.ar.aa | send | arameus | masodlagos_cimke | 14 |
| H7981 | שְׁלֵט | xv.as.aa | have power | arameus | masodlagos_cimke | 7 |
| H7984 | שִׁלְטוֹן | xv.as.ab | ruler | arameus | nincs_H_kulcs | 2 |
| H7986 | שַׁלֶּטֶת | v.dn.ab | having mastery | heber | masodlagos_cimke | 1 |
| H8000 | שְׁלֵם | xv.at.aa | be complete | arameus | masodlagos_cimke | 3 |
| H8007 | שַׂלְמָא | u.bk.ak | Salma | heber | masodlagos_cimke | 4 |
| H8009 | שַׂלְמָה | u.bk.ak | Salmon. Compare | heber | masodlagos_cimke | 1 |
| H8023 | שִׁלֹנִי | v.dk.ad | Shiloni | heber | masodlagos_cimke | 1 |
| H8036 | שֻׁם | xv.at.ac | name | arameus | masodlagos_cimke | 12 |
| H8065 | שָׁמַ֫יִן | xv.au.ab | heavens | arameus | masodlagos_cimke | 38 |
| H8067 | שְׁמִינִית | v.ec.ac | eighth | heber | masodlagos_cimke | 3 |
| H8073 | שַׁמְלַי | u.bk.al | Shalmai (from the margin) | heber | masodlagos_cimke | 0 |
| H8086 | שְׁמַע | xv.aw.aa | hear | arameus | masodlagos_cimke | 9 |
| H8093 | שִׁמְעָה | v.ed.ah | Shimeah | heber | masodlagos_cimke | 3 |
| H8112 | שִׁמְרוֹן מְראוֹן | v.ef.am | Shimon-meron | heber | masodlagos_cimke | 2 |
| H8115 | שׇֽׁמְרָ֑יִן | xv.aw.ab | Samaria | arameus | masodlagos_cimke | 2 |
| H8133 | שְׁנָא | xv.az.aa | change | arameus | masodlagos_cimke | 21 |
| H8153 | שְׁנָת | j.dx.af | sleep | heber | masodlagos_cimke | 1 |
| H8157 | שֶׁ֫סַע | v.er.ab | cleft | heber | masodlagos_cimke | 4 |
| H8180 | שַׁ֫עַר | v.fb.ab | measure | heber | nincs_H_kulcs | 1 |
| H8183 | שְׂעָרָה | u.bt.ac | hurricane | heber | masodlagos_cimke | 2 |
| H8200 | שְׁפַט | xv.bb.aa | judge | arameus | masodlagos_cimke | 1 |
| H8214 | שְׁפֵל | xv.bc.aa | be low | arameus | masodlagos_cimke | 4 |
| H8226 | שָׂפַן | o.ch.aa | cover | heber | masodlagos_cimke | 1 |
| H8241 | שֶׁצֶף | v.cs.ab | flood | heber | masodlagos_cimke | 1 |
| H8249 | שִׁקֻּו | v.fo.ab | drink | heber | nincs_H_kulcs | 1 |
| H8284 | שָׁרָה | v.cc.ae | row | heber | masodlagos_cimke | 1 |
| H8293 | שֵׁרוּת | v.fy.aa | let loose | heber | masodlagos_cimke | 0 |
| H8309 | שְׁרֵמָה | v.bi.ab | field | heber | masodlagos_cimke | 0 |
| H8323 | שָׂרַר | u.cm.ac | be prince | heber | masodlagos_cimke | 5 |
| H8326 | שֹׁרֶר | v.ge.ab | navel-string | heber | masodlagos_cimke | 1 |
| H8330 | שֹׁ֫רֶשׁ | xv.bg.aa | root | arameus | masodlagos_cimke | 3 |
| H8338 | שִׁשֵּׁא | v.gh.aa | lead on | heber | masodlagos_cimke | 1 |
| H8340 | שֵׁשְׁבַּצַּר | xv.bg.ac | Sheshbazzar | arameus | masodlagos_cimke | 2 |
| H8351 | שֵׁת | v.ae.ae | din | heber | nincs_H_kulcs | 0 |
| H8386 | תַּאֲנִיָּה | a.ec.ab | mourning | heber | nincs_H_kulcs | 2 |
| H8390 | תַּאֲרֵעַ | h.fy.ab | Tarea. See | heber | masodlagos_cimke | 1 |
| H8404 | תַּבְעֵרָה | b.cj.ac | Taberah | heber | nincs_H_kulcs | 2 |
| H8406 | תְּבַר | xw.aa.aa | break | arameus | masodlagos_cimke | 1 |
| H8408 | תַּגְמוּל | c.cj.ae | benefit | heber | nincs_H_kulcs | 1 |
| H8419 | תַּהְפֻּכָה | e.cb.ag | perversity | heber | nincs_H_kulcs | 10 |
| H8421 | תּוּב | xw.ab.aa | return | arameus | masodlagos_cimke | 8 |
| H8445 | תּוֹקַהַת | s.aq.ah | Tikvath (by correction for ) | heber | masodlagos_cimke | 0 |
| H8448 | תּוֹר | w.al.ab | plait | heber | masodlagos_cimke | 1 |
| H8450 | תּוֹר | xw.ac.ab | bullock | arameus | masodlagos_cimke | 7 |
| H8452 | תּוֹרָה | j.di.af | direction | heber | masodlagos_cimke | 1 |
| H8459 | תֹּחוּ | w.aj.ab | Tohu | heber | masodlagos_cimke | 1 |
| H8474 | תַּחָרָה | h.fo.aa | burn | heber | masodlagos_cimke | 2 |
| H8479 | תַּחַת | xw.ac.ac | under | arameus | masodlagos_cimke | 0 |
| H8490 | תִּימָרָה | w.ba.af | column | heber | nincs_H_kulcs | 2 |
| H8499 | תְּכוּנָה | k.aw.ak | arrangement | heber | masodlagos_cimke | 1 |
| H8501 | תָּכָךְ | w.ap.ab | injury | heber | masodlagos_cimke | 0 |
| H8517 | תְּלַג | xw.ac.ad | snow | arameus | masodlagos_cimke | 1 |
| H8543 | תְּמוֹל | w.ay.ab | yesterday | heber | masodlagos_cimke | 23 |
| H8550 | תֻּמִּים | w.az.ab | Thummim | heber | masodlagos_cimke | 5 |
| H8567 | תָּנָה | w.bc.aa | recount | heber | nincs_H_kulcs | 2 |
| H8568 | תַּנָּה | w.be.ab | jackal | heber | nincs_H_kulcs | 0 |
| H8616 | תִּקְוָה | s.aq.ah | Tikvah | heber | nincs_H_kulcs | 3 |
| H8625 | תְּקַל | xw.ag.aa | weigh | arameus | masodlagos_cimke | 3 |
| H8627 | תְּקַן | xw.ah.aa | be in order | arameus | masodlagos_cimke | 1 |
| H8631 | תְּקֵף | xw.ai.aa | grow strong | arameus | masodlagos_cimke | 5 |
| H8637 | תִּרְגַּל | t.ar.ab | foot it | heber | masodlagos_cimke | 1 |
| H8646 | תֶּ֫רַח | w.bq.ao | Tarah | heber | nincs_H_kulcs | 13 |
| H8651 | תְּרַע | xw.ah.af | gate | arameus | masodlagos_cimke | 2 |

## 4. BDB.lexicon H-kulcsok, amelyek a táblából hiányoznak

- A `H<n>` kulcsok száma: 8619; a táblában nincs sora: **530**; ebből testvér-Strong a táblában van: 529, nincs: 1.
- Ez a másodlagos-címke osztály; a szócikk szövege a testvér-sor alatt a táblában benne van, ezért nem szövegpótlás, hanem Strong→sor megfeleltetés kérdése (⛔ döntés).

## 5. Ellenőrzés a DictBDB.json-ban

- A `DictBDB.json` nincs a repóban (a `_convert_bdb.py` a `Temp` könyvtárból olvasta); újraletöltése nem történt (lemezkeret, letöltési engedély). A konverter **minden** nem üres bejegyzést kiír, a tábla tehát a JSON kulcskészletének képe (kulcsok: 8090, ebből betűutótagos: 0, a fejlécsor nélkül).
- Következtetés: a hiányzó Strong-szám a JSON-ban sem szerepel más kulcs alatt (a betűutótagos kulcsok száma fent; a tábla kulcsai és a hiányzók listája diszjunkt). A közvetlen JSON-ellenőrzés a konverter forrásának újraletöltését igényelné; ezt a ⛔ nem blokkolja.
