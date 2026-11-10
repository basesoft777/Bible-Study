# F105 — a BDB héber idézeteinek szórendje: mérés, gépi egyezés, 50-es minta (FELADATOK #105)

*2026-11-10. Modell: `claude-opus-5-5`. Ág: `claude/f105-bdb-szorend`. Az 1–5. szakasz mérés és minta (akkor az adat és
a megjelenítés még nem változott); a 6. szakasz a megvalósítás (a javítótábla és a megjelenítés változott); a 7. a vak minta
eredménye. A forrás (`BDB_teljes_unabridged.tsv`) és a `lexikon/` egyik szakaszban sem változott. Mérőszkript: `naplok/F105_meres.py` (kb. 10 mp), minta: `naplok/F105_minta.py`.*

*proveniencia: scope=BDB_teljes_unabridged.tsv minden szócikkének többszavas héber futama (29 469) | forras=naplok/F105_meres.py@49a9f39bea4a;
konkordancia/BDB_teljes_unabridged.tsv@d4b15b2faea6, konkordancia/TAHOT_kivonat.tsv@4c876f570aad, adat/bdb_vers_jelentes.tsv@17a27594fd5e,
adat/bdb_forras_javitas.tsv@834be5c1ee6e, eszkozok/bdb_rovidites.py@64c639fe67b0, eszkozok/olvaso_szerver/bdb_szelet.py@180ed181fb02 | ts=2026-11-10*

## 1. Kiinduló lelet: a brief tárgyának nagy része a DT445 óta él

A brief (v1, 2026-10-15) óta a szórend-javítás elkészült és élesben van: a DT445 (N-F131y, 2026-11-01;
`naplok/BDB_HEBER_SORREND_meres.md`) a javítótáblán (`adat/bdb_forras_javitas.tsv`, `heber_sorrend`: `javitva` 14 976,
`valodi_sorrend` 224, `jelolt_marad` 21 052) és a megjelenítésben (`eszkozok/bdb_rovidites.heber_sorrend_javit`, amelyet az
olvasó `blokkok._rovidites` és a lexikon-generátor is hív). A gépi ellenőrzés ott **bármely** TAHOT-versen futott; a brief
módszere, a **hivatkozott** vers (`adat/bdb_vers_jelentes.tsv`), új. Nincs megoldva: a `jelolt_marad` tételek, és a
rafe mint maqqéf-pótló (U+05BF; az N-F131y szerint „külön mérendő”).

## 2. Mérés (a brief 1. lépése)

**Módszer.** Futam: a szeletelő `lapit` alakjában legalább két, szóközzel tagolt héber token. A futamot akkor tekintem
TAHOT-tal ellenőrizhetőnek, ha közvetlenül (legfeljebb írásjel, zárójel, „&c.” után) hivatkozás követi, amelynek a
vers → jelentés táblában Károli-verse van, és nincs kiszűrve. Próba a vers TAHOT-vázfolyamán (mássalhangzók, végbetű
alapbetűre, pe/mem egybevéve; teljes szó = betűi, rövidítés = betűi + legfeljebb 8 betű rés, ellipszis legfeljebb 60).
Három alakot vetek össze: **F** a forrás, **M** a mai megjelenítés (DT445 csere), **R** a lexikon nélküli R_hib (geres
nélkül a tokenek megfordítása, geresnél a DT445 `r_str`-je, `eszkozok/bdb_jelolt/heber_sorrend.py`).

| Mi | Szám |
|---|---:|
| többszavas héber futam | **29 469** |
| — geres nélkül / geresszel | 19 242 / 10 227 |
| — rafe-maqqéffel egybeírt tokennel | 2 891 |
| DT445 szerint: `javitva` / `valodi_sorrend` / `jelolt_marad` / részleges / nincs sora | 14 744 / 216 / 11 437 / 139 / 2 933 |
| **TAHOT-tal ellenőrizhető** (hivatkozott, nem kiszűrt vers követi) | **17 953 (60,9%)** |
| — kevés anyag (nincs egy teljes szó és még egy egység) | 135 |
| — a vers nem dönt (sem F, sem R nem illeszkedik: nem szó szerinti idézet, plene/defektív írás, osztott rövidítés) | 5 510 |
| — **eldönthető** | **12 308** |

## 3. Gépi egyezés a hivatkozott versen (a brief 2. lépésének mérése)

| Ítélet (az eldönthető 12 308-on) | Szám | Állapot a DT445 szerint |
|---|---:|---|
| M illeszkedik (a mai megjelenítés egyezik a verssel) | **10 483 (85,2%)** | ebből `javitva` 8 369, a többi változatlanul is jó |
| M nem illeszkedik, R igen (**javítható**) | **1 825 (14,8%)** | `jelolt_marad` 1 748, nincs sora 69, részleges 6, `valodi_sorrend` 2 |

- **A DT445 `javitva` cseréit a hivatkozott vers sehol nem cáfolja:** ahol dönt, 8 369 / 8 369 egyezik.
- **A szabály (R) pontossága a forrással szemben**, ahol a vers csak az egyiket illeszti: R helyes 10 194, F helyes 89
  (**99,1%**). A 89-ből 44 a DT445 `valodi_sorrend` sora (ott a forrás marad), 45 `jelolt_marad` / nincs sora / részleges.
  Hivatkozott-vers-vétóval (csak ahol a vers R-t igazolja, F-et nem) ez a 89 nem romlik el.
- **Ütközés** (DT445 `valodi_sorrend`, de a hivatkozott vers R-t igazolja): 2 sor, `naplok/F105_utkozes.tsv`.
- Ha az 1 823 jelöltet (a nem javított `jelolt_marad` / nincs sora / részleges, `F0_M0_R1`) a megjelenítés javítaná, az
  eldönthető futamokon a megjelenítés és a vers egyezése 85,2%-ról 99,98%-ra nőne (a maradék a 2 ütközés). *(Ez a szám a
  jelölt halmaz definíciójából következik; a valódi próbája az 50-es kézi minta, 4. szakasz.)*

**Maqqéf.** A rafe-maqqéf (`מִןהָֿאָרֶץ` = מִן־הָאָרֶץ) a megjelenítésben ma sehol sincs feloldva (a `bdb_rovidites.py`-ban
és a `blokkok.py`-ban nincs rá szabály). 2 891 többszavas futamot érint (az egytokenes alakokkal együtt a DT445 mérése
szerint 5 589 kifejezést). A minta helyreállított alakja a feloldást is mutatja (a rafét hordozó, nem első betű elé U+05BE, a
rafe ki, az előző betű végbetűre).

## 4. Megállás: hatóköri döntés (DT-F105a) és ⛔ 50-es minta

A brief 2. lépése egy új, az olvasóba kötött szabálymodult (`eszkozok/olvaso_szerver/bdb_szoerend.py`) ír elő. A DT445 óta
a szórend szabálya és a csere egy helyen él (javítótábla + `bdb_rovidites`, a lexikonlap és az olvasó közös útja); egy
második, csak az olvasóban futó szabály ugyanazt a futamot kétszer fordíthatná meg, és a lexikonlap eltérne az olvasótól.
Ezért a megvalósítás előtt megálltam: **DT-F105a** (`dontesek/uj/f105-bdb-szorend.md`). A `blokkok.py`, a
`teszt_olvaso_szerver.py` és a `bdb_szoerend.py` nem változott, a `KETRETEGU_BDB_KARTYA` kapcsolóhoz nem nyúltam.

A ⛔ 50-es minta (5. szakasz) a fenti 1 823 jelöltből készült. Bármelyik változat ezeket javítaná újonnan, így a minta
jóváhagyása a döntéstől független.

## 5. ⛔ Az 50-es kézi minta

Seed 105, véletlen 50 az 1 823 jelöltből, Strong és pozíció szerint. „nyers forrás”: a `BDB_teljes_unabridged.tsv` futama;
„helyreállított alak”: a lexikon nélküli R_hib, utána a rafe-maqqéf feloldása (csak itt: a megjelenítés nem változott);
„vers”: a hivatkozás Károli-kulcsa; „a vers héber szövege”: a Macula szavai a Károli-versen (csak olvasásra, a maqqéf nélkül;
a gépi ellenőrzés a TAHOT-on fut). A „kézi ítélet” (helyes / rossz / nem tudom) a független ellenőré vagy a felhasználóé.
Újragenerálás: `python naplok/F105_meres.py --ki <kvt>`, majd `python naplok/F105_minta.py --be <kvt> --ki-md <fájl> --ki-utkozes naplok/F105_utkozes.tsv`.

| # | Strong | DT445 | nyers forrás | helyreállított alak | vers | a vers héber szövege (Macula) | kézi ítélet |
|---|---|---|---|---|---|---|---|
| 1 | H0068 | jelolt_marad | א ׳חָרָשֵׁי | חָרָשֵׁי א׳ | 2Sám 5:11 | וַ֠יִּשְׁלַח חִירָ֨ם מֶֽלֶךְ צֹ֥ר מַלְאָכִים֮ אֶל דָּוִד֒ וַעֲצֵ֣י אֲרָזִ֔ים וְחָרָשֵׁ֣י עֵ֔ץ וְחָֽרָשֵׁ֖י אֶ֣בֶן קִ֑יר וַיִּבְנֽוּ בַ֖יִת לְדָוִֽד |  |
| 2 | H0854 | jelolt_marad | אִתּוֺ אֲשֶׁר הָעָם | הָעָם אֲשֶׁר אִתּוֺ | Bír 4:13 | וַיַּזְעֵ֨ק סִֽיסְרָ֜א אֶת כָּל רִכְבּ֗וֹ תְּשַׁ֤ע מֵאוֹת֙ רֶ֣כֶב בַּרְזֶ֔ל וְאֶת כָּל הָעָ֖ם אֲשֶׁ֣ר אִתּ֑וֹ מֵחֲרֹ֥שֶׁת הַגּוֹיִ֖ם אֶל נַ֥חַל קִישֽׁוֹן |  |
| 3 | H1245 | jelolt_marad | י ׳דבר | דבר י׳ | Ámós 8:12 | וְנָעוּ֙ מִיָּ֣ם עַד יָ֔ם וּמִצָּפ֖וֹן וְעַד מִזְרָ֑ח יְשֽׁוֹטְט֛וּ לְבַקֵּ֥שׁ אֶת דְּבַר יְהוָ֖ה וְלֹ֥א יִמְצָֽאוּ |  |
| 4 | H1323 | jelolt_marad | ב ׳צֿ׳בְּתוּלַת | בְּתוּלַת ב׳־צ׳ | 2Kir 19:21 | זֶ֣ה הַדָּבָ֔ר אֲשֶׁר דִּבֶּ֥ר יְהוָ֖ה עָלָ֑יו בָּזָ֨ה לְךָ֜ לָעֲגָ֣ה לְךָ֗ בְּתוּלַת֙ בַּת צִיּ֔וֹן אַחֲרֶ֨יךָ֙ רֹ֣אשׁ הֵנִ֔יעָה בַּ֖ת יְרוּשָׁלִָֽם |  |
| 5 | H1568 | jelolt_marad | הַגּ ׳הַר | הַר הַגּ׳ | 1Móz 31:21 | וַיִּבְרַ֥ח הוּא֙ וְכָל אֲשֶׁר ל֔וֹ וַיָּ֖קָם וַיַּעֲבֹ֣ר אֶת הַנָּהָ֑ר וַיָּ֥שֶׂם אֶת פָּנָ֖יו הַ֥ר הַגִּלְעָֽד |  |
| 6 | H1961 | jelolt_marad | נ ׳לֹא | לֹא נ׳ | Zak 8:10 | כִּ֗י לִפְנֵי֙ הַיָּמִ֣ים הָהֵ֔ם שְׂכַ֤ר הָֽאָדָם֙ לֹ֣א נִֽהְיָ֔ה וּשְׂכַ֥ר הַבְּהֵמָ֖ה אֵינֶ֑נָּה וְלַיּוֹצֵ֨א  וְלַבָּ֤א  אֵין שָׁלוֹם֙ מִן הַצָּ֔ר וַאֲשַׁלַּ֥ח אֶת כָּל הָאָדָ֖ם אִ֥ישׁ בְּרֵעֵֽהוּ |  |
| 7 | H2063 | jelolt_marad | זֹאת עַל | עַל זֹאת | Ámós 8:8 | הַ֤עַל זֹאת֙ לֹֽא תִרְגַּ֣ז הָאָ֔רֶץ וְאָבַ֖ל כָּל יוֹשֵׁ֣ב בָּ֑הּ וְעָלְתָ֤ה כָאֹר֙  כֻּלָּ֔הּ וְנִגְרְשָׁ֥ה וְנִשְׁקְעָ֖ה כִּיא֥וֹר מִצְרָֽיִם |  |
| 8 | H2077 | jelolt_marad | זָבַ֑ח בֵּית | בֵּית זָבַ֑ח | 2Krón 7:12 | וַיֵּרָ֧א יְהוָ֛ה אֶל שְׁלֹמֹ֖ה בַּלָּ֑יְלָה  וַיֹּ֣אמֶר ל֗וֹ שָׁמַ֨עְתִּי֙ אֶת תְּפִלָּתֶ֔ךָ וּבָחַ֜רְתִּי בַּמָּק֥וֹם  הַזֶּ֛ה לִ֖י לְבֵ֥ית זָֽבַח |  |
| 9 | H2174 | jelolt_marad | ז ׳מַלְכֵי | מַלְכֵי ז׳ | Jer 25:25 | וְאֵ֣ת כָּל מַלְכֵ֣י זִמְרִ֗י וְאֵת֙ כָּל מַלְכֵ֣י עֵילָ֔ם וְאֵ֖ת כָּל מַלְכֵ֥י מָדָֽי |  |
| 10 | H2416 | jelolt_marad | חַי אֵל | אֵל חַי | Józs 3:10 | וַיֹּ֣אמֶר יְהוֹשֻׁ֔עַ בְּזֹאת֙ תֵּֽדְע֔וּן כִּ֛י אֵ֥ל חַ֖י בְּקִרְבְּכֶ֑ם וְהוֹרֵ֣שׁ יוֹרִ֣ישׁ מִ֠פְּנֵיכֶם אֶת הַכְּנַעֲנִ֨י וְאֶת הַחִתִּ֜י וְאֶת הַחִוִּ֗י וְאֶת הַפְּרִזִּי֙ וְאֶת הַגִּרְגָּשִׁ֔י וְהָאֱמֹרִ֖י וְהַיְבוּסִֽי |  |
| 11 | H2896 | jelolt_marad | טוב יבוא | יבוא טוב | Jer 17:6 | וְהָיָה֙ כְּעַרְעָ֣ר בָּֽעֲרָבָ֔ה  וְלֹ֥א יִרְאֶ֖ה כִּי יָב֣וֹא ט֑וֹב וְשָׁכַ֤ן חֲרֵרִים֙ בַּמִּדְבָּ֔ר  אֶ֥רֶץ מְלֵחָ֖ה וְלֹ֥א תֵשֵֽׁב |  |
| 12 | H3220 | jelolt_marad | מְּלִשְׁתִּים יָם | יָם מְּלִשְׁתִּים | 2Móz 23:31 | וְשַׁתִּ֣י אֶת גְּבֻלְךָ֗ מִיַּם סוּף֙ וְעַד יָ֣ם פְּלִשְׁתִּ֔ים וּמִמִּדְבָּ֖ר עַד הַנָּהָ֑ר כִּ֣י אֶתֵּ֣ן בְּיֶדְכֶ֗ם אֵ֚ת יֹשְׁבֵ֣י הָאָ֔רֶץ וְגֵרַשְׁתָּ֖מוֹ מִפָּנֶֽיךָ |  |
| 13 | H3584 | jelolt_marad | כ ׳לְמַעַן | לְמַעַן כ׳ | Zak 13:4 | וְהָיָ֣ה בַּיּ֣וֹם  הַה֗וּא יֵבֹ֧שׁוּ הַנְּבִיאִ֛ים אִ֥ישׁ מֵחֶזְיֹנ֖וֹ בְּהִנָּֽבְאֹת֑וֹ וְלֹ֧א יִלְבְּשׁ֛וּ אַדֶּ֥רֶת שֵׂעָ֖ר לְמַ֥עַן כַּחֵֽשׁ |  |
| 14 | H3671 | jelolt_marad | כ ׳בַּעַל | בַּעַל כ׳ | Péld 1:17 | כִּֽי חִ֭נָּם מְזֹרָ֣ה הָרָ֑שֶׁת בְּ֝עֵינֵ֗י כָל בַּ֥עַל כָּנָֽף |  |
| 15 | H3680 | nincs_sor | כִסִּתִי אֵלֶיךָ | אֵלֶיךָ כִסִּתִי | Zsolt 143:9 | הַצִּילֵ֖נִי מֵאֹיְבַ֥י יְהוָ֗ה אֵלֶ֥יךָ כִסִּֽתִי |  |
| 16 | H3820 | jelolt_marad | אין לב | לב אין | Péld 17:16 | לָמָּה זֶּ֣ה מְחִ֣יר בְּיַד כְּסִ֑יל לִקְנ֖וֹת חָכְמָ֣ה וְלֶב אָֽיִן |  |
| 17 | H3844 | jelolt_marad | ל ׳יֵין | יֵין ל׳ | Hós 14:8 | יָשֻׁ֙בוּ֙ יֹשְׁבֵ֣י בְ צִלּ֔ וֹ יְחַיּ֥וּ דָגָ֖ן וְ יִפְרְח֣וּ כַ גָּ֑פֶן זִכְר֖ וֹ כְּ יֵ֥ין לְבָנֽוֹן (TAHOT*) |  |
| 18 | H3956 | jelolt_marad | ל ׳שׁוֺט | שׁוֺט ל׳ | Jób 5:21 | בְּשׁ֣וֹט לָ֭שׁוֹן תֵּחָבֵ֑א וְֽלֹא תִירָ֥א מִ֝שֹּׁ֗ד כִּ֣י יָבֽוֹא |  |
| 19 | H3956 | jelolt_marad | הַלּ ׳בַּעַל | בַּעַל הַלּ׳ | Préd 10:8 | אִם יִשֹּׁ֥ךְ הַנָּחָ֖שׁ בְּלוֹא לָ֑חַשׁ וְאֵ֣ין יִתְר֔וֹן לְבַ֖עַל הַלָּשֽׁוֹן |  |
| 20 | H3967 | jelolt_marad | מ ׳חֲמֵשׁ בַּשֶּׁקֶל | חֲמֵשׁ מ׳ בַּשֶּׁקֶל | 2Móz 30:24 | וְקִדָּ֕ה חֲמֵ֥שׁ מֵא֖וֹת בְּשֶׁ֣קֶל הַקֹּ֑דֶשׁ וְשֶׁ֥מֶן זַ֖יִת הִֽין |  |
| 21 | H4033 | jelolt_marad | מ ׳בֵּית | בֵּית מ׳ | Zsolt 119:54 | זְ֭מִרוֹת הָֽיוּ לִ֥י חֻקֶּ֗יךָ בְּבֵ֣ית מְגוּרָֽי |  |
| 22 | H4347 | jelolt_marad | מ ׳מַחַץ | מַחַץ מ׳ | Ézs 30:26 | וְהָיָ֤ה אֽוֹר הַלְּבָנָה֙ כְּא֣וֹר הַֽחַמָּ֔ה וְא֤וֹר הַֽחַמָּה֙ יִהְיֶ֣ה שִׁבְעָתַ֔יִם כְּא֖וֹר שִׁבְעַ֣ת הַיָּמִ֑ים בְּי֗וֹם חֲבֹ֤שׁ יְהוָה֙ אֶת שֶׁ֣בֶר עַמּ֔וֹ וּמַ֥חַץ מַכָּת֖וֹ יִרְפָּֽא |  |
| 23 | H4421 | jelolt_marad | מ ׳אִישׁ | אִישׁ מ׳ | Ézs 3:3 | גִּבּ֖וֹר וְ אִ֣ישׁ מִלְחָמָ֑ה שׁוֹפֵ֥ט וְ נָבִ֖יא וְ קֹסֵ֥ם וְ זָקֵֽן (TAHOT*) |  |
| 24 | H4659 | jelolt_marad | י ׳מִפְעֲלוֺת | מִפְעֲלוֺת י׳ | Zsolt 46:9 | לְֽכוּ חֲ֭זוּ מִפְעֲל֣וֹת יְהוָ֑ה אֲשֶׁר שָׂ֖ם שַׁמּ֣וֹת בָּאָֽרֶץ  |  |
| 25 | H4725 | nincs_sor | הַקֹּדֶשׁ ׳מְ | מְ הַקֹּדֶשׁ׳ | 3Móz 10:17 | מַדּ֗וּעַ לֹֽא אֲכַלְתֶּ֤ם אֶת הַֽחַטָּאת֙ בִּמְק֣וֹם הַקֹּ֔דֶשׁ כִּ֛י קֹ֥דֶשׁ קָֽדָשִׁ֖ים הִ֑וא וְאֹתָ֣הּ נָתַ֣ן לָכֶ֗ם לָשֵׂאת֙ אֶת עֲוֺ֣ן הָעֵדָ֔ה לְכַפֵּ֥ר עֲלֵיהֶ֖ם לִפְנֵ֥י יְהוָֽה |  |
| 26 | H4931 | jelolt_marad | מ ׳עֲלֵיהֶם | עֲלֵיהֶם מ׳ | 1Krón 9:27 | וּסְבִיב֥וֹת בֵּית הָאֱלֹהִ֖ים יָלִ֑ינוּ כִּֽי עֲלֵיהֶ֣ם מִשְׁמֶ֔רֶת וְהֵ֥ם עַל הַמַּפְתֵּ֖חַ וְלַבֹּ֥קֶר  לַבֹּֽקֶר  |  |
| 27 | H5212 | jelolt_marad | נ ׳חֹדֶשׁ | חֹדֶשׁ נ׳ | Neh 2:1 | וַיְהִ֣י בְּחֹ֣דֶשׁ נִיסָ֗ן שְׁנַ֥ת עֶשְׂרִ֛ים לְאַרְתַּחְשַׁ֥סְתְּא הַמֶּ֖לֶךְ יַ֣יִן לְפָנָ֑יו וָאֶשָּׂ֤א אֶת הַיַּ֨יִן֙ וָאֶתְּנָ֣ה לַמֶּ֔לֶךְ  וְלֹא הָיִ֥יתִי רַ֖ע לְפָנָֽיו |  |
| 28 | H5419 | jelolt_marad | ת ׳לְשׁוֺן | לְשׁוֺן ת׳ | Péld 10:31 | פִּֽי צַ֭דִּיק יָנ֣וּב חָכְמָ֑ה וּלְשׁ֥וֹן תַּ֝הְפֻּכ֗וֹת תִּכָּרֵֽת |  |
| 29 | H5428 | jelolt_marad | נ ׳עָרִים | עָרִים נ׳ | Zsolt 9:7 | הָֽאוֹיֵ֨ב תַּ֥מּוּ חֳרָב֗וֹת לָ֫נֶ֥צַח וְעָרִ֥ים נָתַ֑שְׁתָּ אָבַ֖ד זִכְרָ֣ם הֵֽמָּה |  |
| 30 | H5889 | jelolt_marad | ע ׳נֶפֶשׁ | נֶפֶשׁ ע׳ | Péld 25:25 | מַ֣יִם קָ֭רִים עַל נֶ֣פֶשׁ עֲיֵפָ֑ה וּשְׁמוּעָ֥ה ט֝וֹבָ֗ה מֵאֶ֥רֶץ מֶרְחָֽק |  |
| 31 | H5927 | jelolt_marad | שׁבע באר | באר שׁבע | 1Móz 26:23 | וַיַּ֥עַל מִשָּׁ֖ם בְּאֵ֥ר שָֽׁבַע |  |
| 32 | H5999 | jelolt_marad | ע ׳יֹצֵר | יֹצֵר ע׳ | Zsolt 94:20 | הַֽ֭יְחָבְרְךָ כִּסֵּ֣א הַוּ֑וֹת יֹצֵ֖ר עָמָ֣ל עֲלֵי חֹֽק |  |
| 33 | H6310 | jelolt_marad | פ ׳אִמְרֵי | אִמְרֵי פ׳ | 5Móz 32:1 | הַאֲזִ֥ינוּ הַשָּׁמַ֖יִם וַאֲדַבֵּ֑רָה וְתִשְׁמַ֥ע הָאָ֖רֶץ אִמְרֵי פִֽי |  |
| 34 | H6341 | jelolt_marad | פ ׳יַעֲלֶה | יַעֲלֶה פ׳ | Ámós 3:5 | הֲתִפֹּ֤ל צִפּוֹר֙ עַל פַּ֣ח הָאָ֔רֶץ וּמוֹקֵ֖שׁ אֵ֣ין לָ֑הּ הֲיַֽעֲלֶה פַּח֙ מִן הָ֣אֲדָמָ֔ה וְלָכ֖וֹד לֹ֥א יִלְכּֽוֹד |  |
| 35 | H6437 | jelolt_marad | י ׳מֵעִם | מֵעִם י׳ | 5Móz 29:18 | פֶּן יֵ֣שׁ בָּ֠כֶם אִ֣ישׁ אוֹ אִשָּׁ֞ה א֧וֹ מִשְׁפָּחָ֣ה אוֹ שֵׁ֗בֶט אֲשֶׁר֩ לְבָב֨וֹ פֹנֶ֤ה הַיּוֹם֙ מֵעִם֙ יְהוָ֣ה אֱלֹהֵ֔ינוּ לָלֶ֣כֶת לַעֲבֹ֔ד אֶת אֱלֹהֵ֖י הַגּוֹיִ֣ם הָהֵ֑ם פֶּן יֵ֣שׁ בָּכֶ֗ם שֹׁ֛רֶשׁ פֹּרֶ֥ה רֹ֖אשׁ וְלַעֲנָֽה |  |
| 36 | H6884 | jelolt_marad | מ ׳כְּאֵשׁ | כְּאֵשׁ מ׳ | Mal 3:2 | וּמִ֤י מְכַלְכֵּל֙ אֶת י֣וֹם בּוֹא֔וֹ וּמִ֥י הָעֹמֵ֖ד בְּהֵרָֽאוֹת֑וֹ כִּֽי הוּא֙ כְּאֵ֣שׁ מְצָרֵ֔ף וּכְבֹרִ֖ית מְכַבְּסִֽים |  |
| 37 | H7068 | jelolt_marad | ק ׳מנחת | מנחת ק׳ | 4Móz 5:15 | וְהֵבִ֨יא הָאִ֣ישׁ אֶת אִשְׁתּוֹ֮ אֶל הַכֹּהֵן֒ וְהֵבִ֤יא אֶת קָרְבָּנָהּ֙ עָלֶ֔יהָ עֲשִׂירִ֥ת הָאֵיפָ֖ה קֶ֣מַח שְׂעֹרִ֑ים לֹֽא יִצֹ֨ק עָלָ֜יו שֶׁ֗מֶן וְלֹֽא יִתֵּ֤ן עָלָיו֙ לְבֹנָ֔ה כִּֽי מִנְחַ֤ת קְנָאֹת֙ ה֔וּא מִנְחַ֥ת זִכָּר֖וֹן מַזְכֶּ֥רֶת עָוֺֽן |  |
| 38 | H7393 | jelolt_marad | אֵשׁ רֶכֶב | רֶכֶב אֵשׁ | 2Kir 2:11 | וַיְהִ֗י הֵ֣מָּה הֹלְכִ֤ים הָלוֹךְ֙ וְדַבֵּ֔ר וְהִנֵּ֤ה רֶֽכֶב אֵשׁ֙ וְס֣וּסֵי אֵ֔שׁ וַיַּפְרִ֖דוּ בֵּ֣ין שְׁנֵיהֶ֑ם וַיַּ֨עַל֙ אֵ֣לִיָּ֔הוּ בַּֽסְעָרָ֖ה  הַשָּׁמָֽיִם |  |
| 39 | H7723 | jelolt_marad | שׁ ׳נָפַת | נָפַת שׁ׳ | Ézs 30:28 | וְרוּח֞וֹ כְּנַ֤חַל שׁוֹטֵף֙ עַד צַוָּ֣אר יֶֽחֱצֶ֔ה לַהֲנָפָ֥ה גוֹיִ֖ם בְּנָ֣פַת שָׁ֑וְא וְרֶ֣סֶן מַתְעֶ֔ה עַ֖ל לְחָיֵ֥י עַמִּֽים |  |
| 40 | H7938 | jelolt_marad | שׂ ׳עשֵֹׁי | עשֵֹׁי שׂ׳ | Ézs 19:10 | וְהָי֥וּ שָׁתֹתֶ֖יהָ מְדֻכָּאִ֑ים כָּל עֹ֥שֵׂי שֶׂ֖כֶר אַגְמֵי נָֽפֶשׁ |  |
| 41 | H8064 | jelolt_marad | שׁ ׳דְָּגַן | דְָּגַן שׁ׳ | Zsolt 78:24 | וַיַּמְטֵ֬ר עֲלֵיהֶ֣ם מָ֣ן לֶאֱכֹ֑ל וּדְגַן שָׁ֝מַ֗יִם נָ֣תַן לָֽמוֹ |  |
| 42 | H8189 | jelolt_marad | שׁ ׳דֶּרֶךְ | דֶּרֶךְ שׁ׳ | 1Sám 17:52 | וַיָּקֻ֣מוּ אַנְשֵׁי֩ יִשְׂרָאֵ֨ל וִיהוּדָ֜ה וַיָּרִ֗עוּ וַֽיִּרְדְּפוּ֙ אֶת הַפְּלִשְׁתִּ֔ים עַד בּוֹאֲךָ֣ גַ֔יְא וְעַ֖ד שַׁעֲרֵ֣י עֶקְר֑וֹן וַֽיִּפְּל֞וּ חַֽלְלֵ֤י פְלִשְׁתִּים֙ בְּדֶ֣רֶךְ שַׁעֲרַ֔יִם וְעַד גַּ֖ת וְעַד עֶקְרֽוֹן |  |
| 43 | H8193 | jelolt_marad | שׂ ׳דְּבַר | דְּבַר שׂ׳ | Zsolt 17:4 | לִפְעֻלּ֣וֹת אָ֭דָם בִּדְבַ֣ר שְׂפָתֶ֑יךָ אֲנִ֥י שָׁ֝מַ֗רְתִּי אָרְח֥וֹת פָּרִֽיץ |  |
| 44 | H8239 | jelolt_marad | הַסִּיר שְׁפֹת | שְׁפֹת הַסִּיר | 2Kir 4:38 | וֶאֱלִישָׁ֞ע שָׁ֤ב הַגִּלְגָּ֨לָה֙ וְהָרָעָ֣ב בָּאָ֔רֶץ  וּבְנֵי֙ הַנְּבִיאִ֔ים יֹשְׁבִ֖ים לְפָנָ֑יו וַיֹּ֣אמֶר לְנַעֲר֗וֹ שְׁפֹת֙ הַסִּ֣יר הַגְּדוֹלָ֔ה וּבַשֵּׁ֥ל נָזִ֖יד לִבְנֵ֥י הַנְּבִיאִֽים |  |
| 45 | H8269 | jelolt_marad | יְהוּדָה שָׂרֵי | שָׂרֵי יְהוּדָה | Neh 12:31 | וָאַעֲלֶה֙ אֶת שָׂרֵ֣י יְהוּדָ֔ה מֵעַ֖ל לַחוֹמָ֑ה  וָאַעֲמִ֡ידָה שְׁתֵּ֣י תוֹדֹת֩ גְּדוֹלֹ֨ת וְתַהֲלֻכֹ֤ת לַיָּמִין֙  מֵעַ֣ל לַחוֹמָ֔ה  לְשַׁ֖עַר הָאַשְׁפֹּֽת |  |
| 46 | H8441 | jelolt_marad | ת ׳גִּלּוּלֵי | גִּלּוּלֵי ת׳ | Ez 16:36 | כֹּֽה אָמַ֞ר אֲדֹנָ֣י יְהֹוִ֗ה יַ֣עַן הִשָּׁפֵ֤ךְ נְחֻשְׁתֵּךְ֙ וַתִּגָּלֶ֣ה עֶרְוָתֵ֔ךְ בְּתַזְנוּתַ֖יִךְ עַל מְאַהֲבָ֑יִךְ וְעַל֙ כָּל גִּלּוּלֵ֣י תוֹעֲבוֹתַ֔יִךְ וְכִדְמֵ֣י בָנַ֔יִךְ אֲשֶׁ֥ר נָתַ֖תְּ לָהֶֽם |  |
| 47 | H8476 | nincs_sor | תְּחָשִׁים עֹרֹת | עֹרֹת תְּחָשִׁים | 2Móz 25:5 | וְעֹרֹ֨ת אֵילִ֧ם מְאָדָּמִ֛ים וְעֹרֹ֥ת תְּחָשִׁ֖ים וַעֲצֵ֥י שִׁטִּֽים |  |
| 48 | H8672 | jelolt_marad | מֵאוֺת תְשַׁע | תְשַׁע מֵאוֺת | Bír 4:3 | וַיִּצְעֲק֥וּ בְנֵֽי יִשְׂרָאֵ֖ל אֶל יְהוָ֑ה כִּ֠י תְּשַׁ֨ע מֵא֤וֹת רֶֽכֶב בַּרְזֶל֙ ל֔וֹ וְ֠הוּא לָחַ֞ץ אֶת בְּנֵ֧י יִשְׂרָאֵ֛ל בְּחָזְקָ֖ה עֶשְׂרִ֥ים שָׁנָֽה |  |
| 49 | H9005 | jelolt_marad | לְ עמד | עמד לְ | Ézs 11:10 | וְהָיָה֙ בַּיּ֣וֹם  הַה֔וּא שֹׁ֣רֶשׁ יִשַׁ֗י אֲשֶׁ֤ר עֹמֵד֙ לְנֵ֣ס עַמִּ֔ים אֵלָ֖יו גּוֹיִ֣ם יִדְרֹ֑שׁוּ וְהָיְתָ֥ה מְנֻחָת֖וֹ כָּבֽוֹד |  |
| 50 | H9005 | jelolt_marad | לְ מִקֶּדֶם | מִקֶּדֶם לְ | 1Móz 3:24 | וַיְגָ֖רֶשׁ אֶת הָֽאָדָ֑ם וַיַּשְׁכֵּן֩ מִקֶּ֨דֶם לְגַן עֵ֜דֶן אֶת הַכְּרֻבִ֗ים וְאֵ֨ת לַ֤הַט הַחֶ֨רֶב֙ הַמִּתְהַפֶּ֔כֶת לִשְׁמֹ֕ר אֶת דֶּ֖רֶךְ עֵ֥ץ הַֽחַיִּֽים |  |

*A 4. sor (H1323) helyreállított alakjában a maqqéf a rafe feloldásából jön; a futamszámlálás (2. szakasz) ezt a tokent nem számolta rafe-maqqéfesnek, mert ott a rafe a token első betűjén áll a geres után.*

*A 17. (Hós 14:8) és a 23. sor (Ézs 3:3) versszövege a TAHOT-ból (Károli-kulcs, morfémák szóközzel; ELLENOR_F105 5.): a Macula `karoli` oszlopa a Hós 14-ben üres, az Ézs 3-ban pedig azonosságot ad, holott ott az F85 eltolást mért (DT179), ezért az eredeti táblában a 17. sor üres volt, a 23. az MT 3:3-at adta. A vak minta (7. szakasz) már a TAHOT-ot használta.*

## 6. Megvalósítás (DT-F105a (a), orkesztrátori döntés a felhasználó felhatalmazásával, 2026-11-10)

*A megvalósítás (F105.7–F105.9) a vak minta eredménye előtt készült; a minta eredménye a 7. szakaszban áll (két kitöltő,
50/50). A lexikonlapok ebben a szakaszban nem generálódtak újra.*

**6.1 A javítótábla** (`eszkozok/bdb_jelolt/forras_javit.py` + `heber_sorrend.py`; újragenerálás:
`naplok/F105_tabla_osszevet.py`, írás előtti összevetéssel; a generátor `--ellenoriz` módja bájtra azonosnak méri).

| Változás | Sor |
|---|---:|
| sorok száma | 43 504 → 43 572 |
| meglévő `javitva` sor sérült (bármely osztály) | **0** |
| `heber_sorrend` `jelolt_marad` → `javitva` (hivatkozott-vers-próba) | 1 778 |
| `heber_sorrend` `valodi_sorrend` → `javitva` (kézi, `manual`: H2638 Péld 17:18, H3801 3Móz 16:4) | 2 |
| új `heber_sorrend` `javitva` sor (több `<heb>` elemre bontott futam, hivatkozott-vers-próba) | 68 |
| `heber_sorrend` utána: `javitva` / `valodi_sorrend` / `jelolt_marad` | 16 824 / 222 / 19 274 |

A próba: a szakasztábla sorának előfordulását a környezete (30-30 karakter) illeszti a szócikk teljes `lapit`-szövegébe
(a feltáró mérés szerint a `jelolt_marad` sorok 99,4%-a egyértelműen illeszthető: 20 929 / 21 052; 119 nem, 4 többször);
a hivatkozott vers a `bdb_vers_jelentes.tsv`-ből (Károli-vers, nem kiszűrt, a futam és a hivatkozás között csak írásjel,
zárójel, szóköz, „&c.”); a TAHOT-minta (`Biblia.minta_vers`) a rafét hordozó betű előtt szóra bont, így a rövidítés rése a
saját részéé (`ח׳לֵֿב`: „ח” + rés, „לב”). A DT445 `minta`-ja változatlan. A két kézi sorban a DT445 bármely-vers-próbája a
forrás alakját véletlenül egy idegen versben találta (Sir 4:7, 3Móz 23:8) a rövidítés 8 betűs résével.

*Körkörös hivatkozás:* a `bdb_vers_jelentes.tsv` fejléce a javítótábla hash-ét hordozza (a `hivatkozas_kezi` sorok miatt),
a javítótábla most az övét. A javítótábla fejlécében ezért a `bdb_vers_jelentes.tsv` hash-e csak az adatsorokra vonatkozik;
a `bdb_vers_jelentes.tsv` csak a fejlécében változott (újragenerálva, `--ts 2026-11-09`).

**6.2 A megjelenítés: rafe-maqqéf** (`eszkozok/bdb_rovidites.maqqef_javit`; a `heber_sorrend_javit` a sorrend-csere után
hívja, így az olvasó és a lexikon-generátor is). Szabály: a maqqéf a rafét hordozó betű elé kerül, kivéve ha az végbetű-alak
vagy a token utolsó betűje (akkor utána: a következő betű elé, vagy a közvetlen szóköz helyére); az előző betű
végbetű-alakra; ahol nincs szomszédos betű, a rafe marad. Mérés (`naplok/F105_maqqef_meres.py`: a szón belüli bontás két része
a Macula szókészletében):

| Változat | jó | rossz | nem dönt |
|---|---:|---:|---:|
| 1. (magánhangzó-pont szerint előtte/utána; elvetve) | 2 189 | 483 (a „mögötte” ágon 399, ott 33 jó) | 1 849 |
| **végleges** (előtte, kivéve végbetű / token vége) | **2 555** | **113** | 1 584 |

A 113 „rossz” felső becslés: benne a pe/mem-forráshiba (`אֶת־מִּיהָ` = פִּיהָ) és a ritka / csonka szó (`אֶל־הַחָם`) zaja;
valódi hiba a nem maqqéf-jelölő rafe (`אַרְכָֿה`, `לאֿהרן`) és a szón belüli szóvégi rafe (`אֶתֿכֹּל` → `אֶ־תכֹּל`). A token
végi rafe (`בַּתֿ צִיּוֺן` → `בַּת־צִיּוֺן`) a szomszéd szóval kapcsolódik; ezt a szómérés nem látja (a „változatlan” 1 631-ben).

**6.3 Gépi egyezés a hivatkozott versen, előtte / utána** (`naplok/F105_meres.py@a7c99e9b58d1`; a maqqéf a mérésben is szóhatár; az „előtte” oszlop az F105.1-es futásé, akkor még nem volt maqqéf; proveniencia: scope=a 29 469 futam | forras=naplok/F105_meres.py, adat/bdb_forras_javitas.tsv (F105.7) | ts=2026-11-10)

| | előtte (F105.1) | utána |
|---|---:|---:|
| ellenőrizhető / eldönthető futam | 17 953 / 12 308 | 17 953 / 12 308 |
| a megjelenítés egyezik a verssel | 10 483 (**85,2%**) | 12 287 (**99,8%**) |
| javítható, de nem javított (M nem, R igen) | 1 825 | 20 (12 `jelolt_marad`: nem egyértelmű illesztés; 8 a H4725 sor nélküli, ismétlődő futama) |
| a forrás jó, a megjelenítés nem (F igen, M nem) | 0 | 1 (H7121, Siral 3:55; l. lent) |
| a futamok állapota (`javitva` / `jelolt_marad` / sor nélkül) | 14 744 / 11 437 / 2 933 | 16 581 / 9 671 / 2 870 |

*A H7121-es eset nem visszaesés:* a megjelenítés a Strongon belül alak szerint cserél (DT445), ezért az új `javitva` sor
(sorszám 39, Jer 44:26) a `י ׳שֵׁם` másik, eldönthetetlen előfordulását (Siral 3:55) is `שֵׁם י׳`-re javítja; a mérés ott a
vers `שִׁמְךָ` toldaléka miatt téved. Ugyanez a hatás 42 alakra áll (új `javitva` sor mellett ugyanazon alak `jelolt_marad`
előfordulása a Strongban); `valodi_sorrend` előfordulással egy új sor sem ütközik (0).

**6.4 Renderelt minta (repón kívül):** `C:\Users\bases\AppData\Local\Temp\F105_kartya_minta\F105_kartya_minta.html` — az
olvasó BDB-kártyájának szövegrétege (a `blokkok._rovidites` lánca) előtte (a `b2317a2e` kódja és táblája) / utána, H1323
(12 változó szakaszsor), H2638 (1), H0413 (12).

## 7. ⛔ Az 50-es minta: két független vak kitöltő (orkesztrátori eljárás, 2026-11-10)

A felhasználó a mintát nem tölti ki. Az eljárás: két független, vak Opus-kitöltő dolgozott subagentként, a végrehajtón kívül. Az elv: aki javít, az nem ítél.

**Mit kaptak a kitöltők:** a hivatkozott vers Károli-kulcsát, a vers héber szövegét a TAHOT-ból, és a futam két sorrendjét „A” és „B” címkével. A címkék tételenként rögzített seeddel, véletlenszerűen kerültek a két sorrendre: 26 tételben az A, 24-ben a B a helyreállított alak. A gépi döntést, a DT445-állapotot és a Strong-számot nem kapták meg.

**Vakság:** a geres mindkét alakból kikerült (`naplok/F105_vak.py`, F105.4–F105.6). Ennek az oka, hogy a geres a betű előtt csak a forrásalakban állt, és ez 34 tételben árulkodott. A két alak 49 tételben ugyanannak a tokenhalmaznak a permutációja. Az 50. tétel, a 4. kivétel: a rafe-maqqéf csak az egyik alakban bontott két szóra.

**Kérdés:** melyik sorrend áll a versben (`A` / `B` / `egyik_sem` / `nem_donthető`).

**Eredmény** (`python naplok/F105_vak_osszevet.py`):

| | helyes / n | 95% Wilson |
|---|---|---|
| 1. kitöltő | 50 / 50 | 0,929–1,000 |
| 2. kitöltő | 50 / 50 | 0,929–1,000 |
| a két kitöltő egyezik, és a helyreállított alakot választja | 50 / 50 | 0,929–1,000 |
| ugyanez a 4. tétel nélkül | 49 / 49 | 0,927–1,000 |

- A két kitöltő egyetlen tételben sem tért el egymástól, ezért nincs orkesztrátori döntésre váró tétel.
- Egyik kitöltő sem adott `egyik_sem` vagy `nem_donthető` ítéletet.
- A mért szám: a hivatkozott vers a helyreállított sorrendet igazolja az 1 823 jelöltből vett 50-es mintán (seed 105), 95%-os alsó korláttal 92,9%.
- A minta az 1 823 jelöltből vett véletlen minta, nem a teljes `javitva` halmazból. A DT445 meglévő cseréit a 3. szakasz gépi mérése fedi.

**Fájlok:**
- `naplok/F105_vak_minta.md`: a kitöltők bemenete.
- `naplok/F105_vak_kulcs.tsv`: a kulcs, a kitöltés alatt a repón kívül volt.
- `naplok/F105_vak_kitolto_1.tsv`, `naplok/F105_vak_kitolto_2.tsv`: a két kitöltés, indokkal.
- `naplok/F105_vak_osszevet.py`: az összevetés szkriptje.

Az 5. szakasz táblájának „kézi ítélet” oszlopa üres marad: az ítéletet a két kitöltő-fájl hordozza.

*proveniencia: scope=F105 50-es minta (seed 105, az 1 823 jelöltből) | forras=naplok/F105_vak_osszevet.py | ts=2026-11-10*
