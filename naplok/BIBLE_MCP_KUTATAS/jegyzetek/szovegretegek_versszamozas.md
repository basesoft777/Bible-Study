# A bible-mcp szöveg- és szóadat-rétegei, összevetve a PaRDeS-repó meglévő adatkészleteivel

*Kutatási jegyzet, 2026-10-16. A repót csak olvastam. A mért tények mellett mindig ott áll a lefuttatott hívás (MCP-eszköz + argumentum) vagy a repófájl. A „Következtetések” alpontok értelmezést tartalmaznak, nem mérést. Az MCP-hívások forrásjelölése: `MCP:<eszköz>('<argumentum>')`; ezek a bible-mcp szerver élő válaszai 2026-10-16-án, URL nélkül.*

## 1. kérdés: melyik réteg mit ad (mezők, kulcs, Strong-alak, licencszint, ismert korlátok)?

### Takeaway (összegzés)
Az MCP hat bibliai réteget kínál: BSB, WEB, LXX-Brenton (angol), LXX-GRC (Swete, csak felszíni alak), MACULA-GRC (N1904) és MACULA-HEB (WLC). A szóadat lemmát, kiterjesztett Strong-számot (betűs utótaggal), morfológiát és kontextuális angol glosszát ad. A corpus_info szerint SDBH- és Louw–Nida-domén is van benne, de a kipróbált eszközök (`get_interlinear`, `word_study`) egyiket sem mutatták meg. Az MCP CC BY 4.0-nak címkézi őket, pedig a MACULA licence szerint a UBS-mezők „Used with permission” alapon állnak.

### Cited Findings
- **Rétegek és darabszámok** (`MCP:corpus_info()`): BSB, Public Domain (tier A), 31 086 szakasz, 66 könyv. WEB (Ecumenical), PD, 38 029 szakasz, 83 könyv, teljes apokrif/deuterokanonikus résszel. LXX (Brenton, 1851), PD, 28 548 szakasz. LXX-GRC (Swete), **CC BY-SA 4.0 (tier B)**, 28 122 szakasz. MACULA-GRC (Nestle1904), CC BY 4.0, „Word-level: lemma, Strong's, morphology, glosses, Louw-Nida domains”. MACULA-HEB (WLC), CC BY 4.0, „Word-level: lemma, Strong's, morphology, glosses, SDBH domains”. Szósorok: 137 779 görög és 475 911 héber/arámi. További rétegek: BDB (OpenScriptures-markup, CC BY 4.0), StrongsHebrew, AbbottSmith, Easton, 344 799 kereszthivatkozás, 4 814 entitás, 5 673 fogalom. — `MCP:corpus_info()`
- **A Brenton-LXX és az LXX-GRC versszámozása:** a zsoltárokat angol (KJV) számozásra képezték le. A Jer, a görög Dán, a 2Móz, a Jób, a görög Eszt és a Bár viszont megtartja az LXX saját fejezet- és versszerkezetét, „which diverges from BSB/WEB in these books (reordering and/or length, not just numbering) — full alignment deferred, see ROADMAP.md”. Az LXX-GRC-ből nincs feldolgozva a Prédikátor, az Ódák és a Salamon zsoltárai; a Dánielnél csak a Theodotion-szöveg van benne. — `MCP:corpus_info()`
- **Az LXX-GRC eredete:** a nathans/lxx-swete repó, amely a First1KGreek (OGL) átirata; a szöveg és az annotációk CC BY-SA 4.0, a build-kód MIT. — [nathans/lxx-swete](https://github.com/nathans/lxx-swete)
- **A héber szósor formája** (`MCP:get_interlinear('Joel 3:1')`): felszíni alak (pontozott, kantillált), átírás, `lemma=`, Strong négyjegyű, nullával feltöltött, betűs utótaggal (`H0871a`, `H1886a`, `H2050b`, `H3807a`, `H1931a`), kontextuális angol glossza (`'I.will.turn.back'`) és OSHB-stílusú morfológiai kód (`Vhi1cs`, `Ncfsc`). A névelő vagy prepozíció önálló morfémasor, üres felszíni alakkal (`(–) lemma=הַ H1886a`).
- **A görög szósor formája** (`MCP:get_interlinear('John 3:16')`): felszíni alak, `lemma=`, Strong feltöltés nélkül (`G25`, `G3588`), angol glossza és Robinson-stílusú morfológia (`V-AAI-3S`, `T-NSM`).
- **A doméneket az eszközök nem adják vissza:** sem a `get_interlinear('John 3:16')`, `('Joel 3:1')`, `('Psalm 51:1')` kimenetében, sem a `word_study('G26')` és `('H7622')` kimenetében nincs SDBH- vagy Louw–Nida-mező. A `word_study` a következőket adja: előfordulásszám, lemmaváltozatok betűs Strong szerint (`H7622` 26x, `H7622a` 3x+2x), glosszatartomány, könyvenkénti eloszlás, BDB/Strong/Abbott-Smith-szócikk (kb. 700 karakterre vágva) és mintaversek. — `MCP:word_study('H7622')`, `MCP:word_study('G26')`
- **A MACULA licencei:** a Hebrew LICENSE szerint „MACULA Hebrew Linguistic Datasets © 2022-2024 by Biblica, Inc is licensed under CC BY 4.0”. Az SDBH-ra külön sor vonatkozik: „©2000-2021 United Bible Societies. Used with permission.” — [macula-hebrew LICENSE.md](https://github.com/Clear-Bible/macula-hebrew/blob/main/LICENSE.md). A Greek LICENSE szerint a „Word sense data from the United Bible Societies (`@ln`, `@domain`) Used with permission.” — [macula-greek LICENSE.md](https://github.com/Clear-Bible/macula-greek/blob/main/LICENSE.md)
- **A repó ugyanezt mérte (F17):** a macula-hebrew LICENSE.md 21. sora és a macula-greek LICENSE.md 3. pontja szerint a héber `sdbh`, `lexdomain`, `coredomain`, `contextualdomain`, `sensenumber` és a görög `domain`, `ln` mező „nem CC BY”. Ezért ezek „nem kerültek be”. — [naplok/F17_import_naplo.md](file:///C:/Users/bases/Desktop/Bible-Study/naplok/F17_import_naplo.md) (24–29. sor)
- **A Swete-átirat hibái** (mért, `get_interlinear`): `Mal 4:1` [LXX] mezőjében „ὁὡς κλίβανος”, „Γαντοκράτωρ”, „όίζα” áll. A `Joel 2:28` mezőben „νεαυίσκοι”. A fejezetjelölő bekerült a szövegbe: a `Genesis 31:55` LXX-szövege „… Καὶ Ἰακὼβ ἀπῆλθεν XXXII”-re végződik, a `Genesis 32:1` pedig „XXXIIεἰς τὴν ἑαυτοῦ ὁδόν”-nal kezdődik. — `MCP:get_interlinear('Malachi 4:1')`, `('Genesis 31:55')`, `('Genesis 32:1')`

### Következtetések
- A 475 911-es héber sorszám pontosan egyezik a repó `Macula_heber_*.tsv` morfémasoraival (l. 3. kérdés). Valószínű, hogy ugyanaz a MACULA lowfat `<w>`-szintű forrás, más kiadásból.
- A 137 779-es görög sorszám a csak N1904-es kiadás méretének felel meg. A repó `Macula_gorog.tsv` 275 520 sora két kiadást tartalmaz (N1904 és SBLGNT), tehát a fele nagyjából ennyi. Ez arányszámítás, nem sorszintű egyezés.
- Az MCP „tier A / CC BY 4.0” címkéje a domén-mezőkre (ha a szerver egyáltalán tárolja őket) licencszempontból pontatlan. A projektnek nem szabad átvennie: ha az MCP-ből SDBH- vagy Louw–Nida-értéket idéznénk, a projekt az F17-ben tudatosan kizárt, „Used with permission” státuszú adatot vinne be.
- A Swete-szöveg OCR-hibái miatt az LXX-GRC idézet-azonosság eldöntésére (mélyelemzés, LXX-híd) nem alkalmas forrás. Erre a repó Rahlfs-alapú `LXX_OS`-e szolgál.

### Gaps
- Az MCP-forrás (ROADMAP.md, MACULA-commit) nem nyilvános: nem tudtam ellenőrizni, melyik MACULA-commitból töltöttek, és tárolják-e ténylegesen a domén-mezőket.
- A `concepts_in_passage` és a `get_concept` eszközt nem próbáltam ki (más kutató hatóköre). Lehet, hogy azok mutatnak doménszerű adatot.

## 2. kérdés: hogyan számozza a szerver a versszámozás-érzékeny helyeket, és ad-e megfeleltetést?

### Takeaway (összegzés)
A héber szóréteg belül MT-kulcsú, a lekérdezés viszont angol (BSB/KJV) számozással megy. A szerver MT→angol leképezést végez. Az MT-alakú hivatkozás csak ott működik, ahol nem ütközik angol kulccsal (pl. `Mal 3:19`, `Joel 4:1`, `Job 40:25`), ütközéskor az angol számozás nyer. Külön megfeleltetési eszköz nincs; a leképezés csak a `word_study` mintaverseinek „[MT = angol]” címkéjében látszik. Az LXX-oldal az eltérő könyvekben nincs igazítva (Jer, Jób), és a Neh 7:68-nál a héber réteg hamis duplikátumot ad.

### Cited Findings (mind mért, a hívás zárójelben)
- **Jóel (MT 3 = angol 2:28–32, MT 4 = angol 3):** a `get_interlinear('Joel 2:28')` angol 2:28-szöveget ad, mellette az MT 3:1 héber szavaival („וְהָיָה אַחֲרֵי כֵן אֶשְׁפּוֹךְ אֶת רוּחִי”) és helyes LXX-szöveggel. A `get_interlinear('Joel 3:1')` és a `('Joel 4:1')` ugyanazt a 20 héber szót adja („כִּי הִנֵּה בַּיָּמִים הָהֵמָּה”); az első angol szöveggel és LXX-szel, a `Joel 4:1` szöveg és LXX nélkül. A `get_interlinear('Joel 3:5')` az angol 3:5-öt adja („Because you have taken my silver…”), az MT 4:5 szavaival: az MT 3:5 („aki segítségül hívja…”) a `Joel 3:5` kulccsal **nem érhető el**, csak a `Joel 2:32`-vel.
- **Malakiás (MT 3:19–24 = angol 4:1–6):** a `get_interlinear('Malachi 3:19')` és a `('Malachi 4:1')` ugyanazt a héber szósort adja (`כִּי הִנֵּה הַיּוֹם בָּא בֹּעֵר כַּתַּנּוּר`). A `Mal 3:19` angol szöveg és LXX nélkül, a `Mal 4:1` WEB-szöveggel és Swete-LXX-szel jön. A `Malachi 3:24` az MT 3:24 szavait adja (`וְהֵשִׁיב לֵב אָבוֹת`).
- **Zsolt 51 (MT-ben a felirat 2 vers):** a `get_interlinear('Psalm 51:1')` egyetlen tételben adja az MT 51:1–3 héber szavait (felirat és „חָנֵּנִי אֱלֹהִים”), a WEB 51:1 szövegével (felirattal együtt) és a feliratot is tartalmazó LXX-szel. A `('Psalm 51:3')` az angol 51:3-at (MT 51:5, „כִּי פְשָׁעַי אֲנִי אֵדָע”) adja. A `('Psalm 51:21')` válasza: „No word-level data for Psalm 51:21”. Az MT-kulcsú utolsó vers tehát az MT-alakú hivatkozással nem érhető el.
- **Jób (MT 40:25–32 = angol 41:1–8):** a `get_interlinear('Job 41:1')` és a `('Job 40:25')` ugyanazt a héber verset adja („תִּמְשֹׁךְ לִוְיָתָן בְּחַכָּה”). Az LXX-mező viszont eltér, és egyik sem a Leviatán-vers: a `Job 41:1`-nél „οὐδὲ ἐπὶ τοῖς λεγομένοις τεθαύμακας…”, a `Job 40:25`-nél „ἐνσιτοῦνται δὲ ἐν αὐτῷ ἔθνη…”. Az LXX tehát saját kulcson áll, igazítás nélkül, ahogy a corpus_info is jelzi.
- **Jeremiás:** a `get_interlinear('Jeremiah 25:15')` az MT/angol 25:15 héber szavait adja (a harag borának pohara), mellette az LXX-mezőben „Τάδε λέγει Κύριος Συνετρίβη τὸ τόξον Αἰλάμ” áll. Ez az LXX Jer 25:15, vagyis tartalmilag az MT Jer 49:35, ami **téves párosítás**.
- **Neh 7:68 (az MT-ben nincs meg a lovas vers):** a `get_interlinear('Nehemiah 7:68')` a WEB 7:68 „Their horses were seven hundred thirty-six…” szövegét adja, mellette viszont az MT 7:67 héber szavait (szolgák 7337, énekesek 245), LXX nélkül. A `('Nehemiah 7:67')` ugyanezt a héber szósort adja, LXX-szel. A `('Nehemiah 7:69')` angol „435 camels” szövege mellett az MT 7:68 („גְּמַלִּים אַרְבַּע מֵאוֹת”) áll, ami helyes. Az angol többletversnél tehát a héber réteg **hamis duplikátumot** ad. A `compare_versions('Nehemiah 7:68-69')` a BSB-ben és a WEB-ben is mindkét verset tartalmazza.
- **Dán 3:31–33 / 4:1–3 és 1Móz 31:55 / 32:1:** a `get_interlinear('Daniel 4:1')` az MT 3:31 arámi szavait adja („נְבוּכַדְנֶצַּר מַלְכָּא לְכָל עַמְמַיָּא”). A `('Genesis 31:55')` az MT 32:1, a `('Genesis 32:1')` az MT 32:2 szavait adja; az angol kulcs helyesen van leképezve.
- **Megfeleltetés csak a `word_study`-ban látszik:** a mintaversek címkéje kiírja a párt: „[Joel.4.1 = Joel.3.1]”, „[Ps.53.7 = Ps.53.6]”, „[Ps.85.2 = Ps.85.1]”. Eszerint a szósorok MT-kulcsúak, a megjelenítés angol számozású. Önálló versszámozási vagy megfeleltetési eszköz nincs a felületen. — `MCP:word_study('H7622')`
- **A `compare_versions` csak BSB-t és WEB-et vet össze,** az angol számozás szerint (`compare_versions('Joel 2:28')`). LXX-et és eredeti nyelvet nem ad. — `MCP:compare_versions('Joel 2:28')`

### Következtetések
- A szerver forrásmegfeleltetése MT↔angol (BSB/KJV) típusú, valószínűleg STEPBible TVTMS- vagy BSB-alapú. A Neh 7:68-as duplikátum arra utal, hogy a többletversre a leképezés az előző MT-verset ismétli, nem üres eredményt ad. Ez a „hiányt ne tölts ki” szabály (CLAUDE.md, 3. szabály) szempontjából veszélyes: egy verskulcsú számlálás a Neh 7:67 szavait kétszer számolná.
- Az LXX-oldal csak a zsoltároknál igazított. A Jer, a Jób (és a corpus_info szerint a 2Móz, az Eszt, a Dán, a Bár) héber↔görög párosításai az `get_interlinear` kimenetében tartalmilag tévesek lehetnek, ezért az LXX-hídhoz nem használhatók.

### Gaps
- Nem tudtam megállapítani, hogy a `word_study` darabszámaiba (pl. `H7622` = 32) bekerülnek-e a duplikált többletversek. A `H7622` eloszlása (32 = könyvenkénti összeg) nem érinti a Neh 7-et, ezért ebből nem dönthető el.
- A 2Móz 35–40, az Eszt és a Bár LXX-viselkedését nem mértem.

## 3. kérdés: mi duplikál, mi új és mi ütközik a repó adatkészleteihez képest?

### Takeaway (összegzés)
A MACULA-HEB és a MACULA-GRC szóadata **teljes duplikátum**: a repó az F17-ben (2026-10-02) már importálta mindkettőt rögzített commitból, Károli-oszloppal. A TAHOT, a TAGNT, a KJV_Strongs_teljes, az LXX_OS (Rahlfs + morfológia + Strong) és a jelentés-szintű SDBH/SDGNT szintén lefedi az MCP szóadatait, és többet ad. Az MCP-ben valóban új szöveg a **WEB** (deuterokanonikus könyvekkel), a **Brenton-LXX** (angol) és a **Swete-LXX** felszíni szövege (Theodotion Dán). Az új szövegek közül egyiknek sincs lemmája vagy Strong-száma, és egyik sem Károli-kulcsú.

### Cited Findings
- **Macula_heber (repó):** `Clear-Bible macula-hebrew@47db250b, CC BY 4.0; 475 911 morféma-sor, 39 könyvfájl`, MT-számozás, a Károli-vers a `karoli` oszlopban; „az UBS-engedélyes domén-mezők (sdbh, lexdomain…) NEM importáltak”. Oszlopok: `xml_id ref karoli kk_mod allapot szo lemma strong strong_x strong_illesztes morf szofaj gloss gorog_lxx gorog_strong`. Példa: `JOL 1:1!1 | Jóel 1:1 | … | H1697 | Ncmsc | the.word | λόγος | G3056`. — [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv) (81. sor), [konkordancia/Macula_heber_Joel.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Macula_heber_Joel.tsv) (fejléc)
- **Macula_gorog (repó):** `macula-greek@8423afe4, CC BY 4.0; 275 520 sor (két kiadás)`, N1904 és SBLGNT; „az UBS-engedélyes domain/ln mezők NEM importáltak”. Oszlopok: `kiadas xml_id ref karoli kk_mod allapot szo lemma strong strong_x strong_illesztes morf szofaj gloss english`. — [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv) (85. sor), [konkordancia/Macula_gorog.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Macula_gorog.tsv)
- **Az F17-ben nem importált MACULA-mezők** (mérethatár vagy szükségtelenség miatt): héber `mandarin`, `transliteration`, `english`, `frame`, `participantref`, `subjref`, `after`, továbbá a nyelvtani jegyek külön mezőben; görög `mandarin`, `after`, `normalized`, `frame`, `subjref`, `referent`, `role`. — [naplok/F17_import_naplo.md](file:///C:/Users/bases/Desktop/Bible-Study/naplok/F17_import_naplo.md) (39–41. sor)
- **TAHOT_kivonat.tsv:** 469 301 sor (fejléccel). Oszlopok: `Igehely` (magyar alak, `1Móz 1:1`, az F85 óta Károli-kulcsú), `Strong-szám` (`H9003` típusú előtagkódok), `Ragozott alak`, `Kiejtés`, `Szótő`, `Rövid jelentés`, `Angol tükörfordítás`. **TAGNT_kivonat.tsv:** 142 097 sor; oszlopai ugyanezek, plusz `Kritikai kiadás` (`NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz`). — [konkordancia/TAHOT_kivonat.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/TAHOT_kivonat.tsv), [konkordancia/TAGNT_kivonat.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/TAGNT_kivonat.tsv)
- **LXX_OS:** 59 könyv, Rahlfs, lxx-morph + GreekWordList, CC BY 4.0. Oszlopok: `igehely_lxx igehely_kjv igehely_karoli karoli_ok pozicio szoalak normalizalt lemma morf strong strong_ok proveniencia`. Ebben **van** lemma, morfológia és Strong; a Swete-rétegben nincs. — [konkordancia/LXX_OS/joel.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/LXX_OS/joel.tsv), [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv)
- **SDBH/SDGNT (repó):** az ubsicap/ubs-open-license forrásból, **CC BY-SA 4.0**, jelentésszintű domén (`lexid`, `domen_kod`, `domen`, `glossza`, `hivatkozas_n`). Az SDGNT Louw–Nida-alapú (`entry_kod` = pl. `61.7`). Az SECE_G Louw–Nida-doménjei is megvannak (5 406/5 523). — [konkordancia/SDBH_domenek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/SDBH_domenek.tsv), [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv)
- **KJV_Strongs_teljes.tsv:** eBible, PD, 66 könyv, angol számozás, 349 308 sor, STEP-alakú kulcs (`Gen.1.1`). **BSB_Strongs.tsv:** CC0, 36 ÓSZ-könyv, MT-célszámozás, ÚSZ nincs. **Karoli_1908.tsv:** 31 159 sor, versszöveg. — [konkordancia/README.md](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/README.md) (77., 305–313. sor), [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv)
- **BDB és Strong:** a repóban megvan a `BDB_teljes_unabridged.tsv`, az `OSHL_BDB_igehelyek.tsv` és az `OSHL_lexikalis_index.tsv` (OpenScriptures, CC BY 4.0), valamint a `Strong_szotar.tsv`. Ugyanezek az MCP BDB/StrongsHebrew rétegei (OpenScriptures LexicalIndex-híd). — [adat/datasetek.tsv](file:///C:/Users/bases/Desktop/Bible-Study/adat/datasetek.tsv), `MCP:corpus_info()`

### Következtetések: duplikált, új és ütköző elemek
**Duplikált (a repó adata egyenértékű vagy jobb):**
1. MACULA-HEB szóadat: a repóban ugyanannyi sor van (475 911), Károli-oszloppal, rögzített commitból, és benne van a szószintű LXX-megfelelő (`gorog_lxx`) is.
2. MACULA-GRC szóadat: a repóban az N1904 mellett az SBLGNT is megvan.
3. Lemma, Strong és morfológia: a TAHOT, a TAGNT és az LXX_OS lefedi.
4. BDB, Strong-szótár, Abbott-Smith-szerű görög lexikonok: a repóban megvan a BDB, a Thayer, az LSJ, a TBESG és az MCGED.
5. Domének: a repó SDBH/SDGNT-je jelentésszintű és licencelt (CC BY-SA). Az MCP domén-állítása nem látható, és licencszempontból bizonytalan.
6. A BSB nagy része: a repóban megvan a BSB_Strongs (36 ÓSZ-könyv, Strong-címkével). A BSB folyószöveg mint olvasószöveg nincs benne (a repó angol szövegre a KJV-t használja).

**Új (a repóban nincs):**
1. WEB-szöveg, az apokrifokkal (83 könyv): angol szöveg a deuterokanonikus könyvekhez.
2. Brenton-LXX angol fordítása: az LXX angol olvasata, a görög híd ellenőrzésének emberi segédlete.
3. Swete-LXX felszíni szöveg: a repó LXX_OS-e Rahlfs-alapú. A Swete második szövegtanú lehet (főleg Theodotion Dán), de lemma és Strong nélkül, OCR-hibákkal, CC BY-SA 4.0 (share-alike) licenccel.
4. A BSB folyószövege és a WEB kényelmes versszintű összevetése (`compare_versions`).
5. A MACULA el nem hozott mezői (`frame`, `subjref`, `participantref`, `referent`, `role`): ezeket az MCP **sem** adja vissza a vizsgált eszközökben, tehát az MCP-n át ez sem új.

**Ütköző:**
1. A versszámozási modell: az MCP angol (BSB/KJV) számozással kérdez, a repó Károli-kulccsal. A Károli vegyes rendszer (a mérés a 4. kérdésben). Az MCP kimenete ezért nem írható közvetlenül a repó igehely-mezőibe.
2. Licenc: az MCP a MACULA-doméneket CC BY 4.0 / tier A címkével közli, a forrás szerint „Used with permission”. Az F17 döntése (a domének kizárása) ezzel ütközik, ha az MCP-ből domént vennénk át.
3. A Neh 7:68 duplikátum és az LXX téves párosításai (Jer 25:15, Jób 41:1) ellentmondanak a repó F85- és LXX_OS-megfeleltetéseinek.

### Gaps
- Az MCP BSB-szövege és a repó BSB_Strongs-a közti esetleges verzióeltérést nem mértem.

## 4. kérdés: elérhető-e a MACULA ömlesztett nyílt adatként?

### Takeaway (összegzés)
Igen. A github.com/Clear-Bible/macula-hebrew és a macula-greek nyilvános repó, CC BY 4.0 (Biblica), csomópontos (nodes), lowfat XML és TSV formátumban. **A repó ezt már megtette:** az F17 rögzített commitból importálta (hebrew@47db250b, greek@8423afe4). A MCP-n keresztüli betöltésnek nincs előnye.

### Cited Findings
- A macula-hebrew formátumai: `WLC/nodes` (beágyazott Node-fa), `WLC/lowfat` és `WLC/tsv` (szószintű tábla, fa nélkül). Forrásai: WLC-szöveg, Open Scriptures morfológia, Groves Center szintaxis, UBS MARBLE szójelentések, Cherith-glosszák, szemantikus szerepek, szereplőhivatkozások (participant referents). Tagolt kiadás (release) nincs, a `main` ágon 444 commit látható. — [Clear-Bible/macula-hebrew](https://github.com/Clear-Bible/macula-hebrew)
- Licenc: CC BY 4.0 © Biblica. Kötelező forrásmegjelölés: „MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/”. A UBS-eredetű mezők külön „Used with permission” státuszúak. — [macula-hebrew LICENSE.md](https://github.com/Clear-Bible/macula-hebrew/blob/main/LICENSE.md), [macula-greek LICENSE.md](https://github.com/Clear-Bible/macula-greek/blob/main/LICENSE.md)
- A repó importja: `forras=https://github.com/Clear-Bible/macula-hebrew@commit 47db250bd55d0d8577f2a94fba114ef16c35b23c | licenc=CC BY 4.0 (Biblica, Inc) | ts=2026-10-02`, futtatás: `python eszkozok/f17/macula_futtat.py --heber <klon> --gorog <klon>`. — [konkordancia/Macula_heber_Joel.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Macula_heber_Joel.tsv) (fejléc)

### Következtetések
- Ha a projektnek szintaktikai vagy szereplőadat kellene (`frame`, `subjref`, `participantref`; görögben `referent`, `role`), annak útja a meglévő F17-importáló kiterjesztése ugyanarról a klónról, nem az MCP. Az F17-napló ezt kifejezetten „később külön, ha kell” javaslatként rögzítette. A strukturális azonosság-hordozójú motívumokhoz (pl. alany- vagy szereplőazonosság) ezek a mezők valódi új jelet adnának; ez feltevés, nem mért eredmény.

### Gaps
- A macula-hebrew TSV pontos oszloplistáját a README nem sorolja fel; a `doc/` mappát nem nyitottam meg.

## 5. kérdés: segít-e az MCP a Károli↔MT versszámozás kérdésében?

### Takeaway (összegzés)
Érdemben nem. A Károli vegyes rendszer: a Jóel, a Malakiás, a Nehémiás, a Jób és az 1Móz 31–32 a KJV-számozást követi, a Zsoltárok és a Dániel az MT-t. Az MCP csak MT↔angol leképezést ismer, Károli-kulcsot nem. A repó F85-ös versszintű kulcsa (23 204 kulcs, 0 árva) és a `Karoli_versmegfeleltetes.tsv` mindazt lefedi, amit az MCP adna. Az MCP legfeljebb független harmadik tanúként használható a KJV-típusú könyvekben, ott is a Neh 7:68 hibával együtt.

### Cited Findings (mért: `kar.py`, a `Karoli_1908.tsv` és a `Karoli_versmegfeleltetes.tsv` beolvasása `split('\t')`-vel)
- **A Károli a KJV-számozást követi ezeken a helyeken:** a `Jóel 2:28` szövege „És lészen azután, hogy kiöntöm lelkemet…”, a `Jóel 3:1` „Mert ímé, azokon a napokon…”, `Jóel 4:1` nincs. A `Mal 4:1` „Mert ímé, eljön a nap…”, `Mal 3:19` nincs. A `Neh 7:68` „Lovaik hétszázharminczhat…” (a vers megvan). A `Jób 41:1` „Kihúzhatod-é a leviáthánt horoggal…”, `Jób 40:25` nincs. Az `1Móz 31:55` Lábán reggele, az `1Móz 32:1` Jákób útja. A versmegfeleltetésben ezek mind `osztaly=KJV`, `forras=szamlalas`. — [konkordancia/Karoli_1908.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Karoli_1908.tsv), [konkordancia/Karoli_versmegfeleltetes.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Karoli_versmegfeleltetes.tsv)
- **A Károli az MT-számozást követi ezeken a helyeken:** a `Zsolt 51:1` szövege „Az éneklőmesternek; Dávid zsoltára;”, a `Zsolt 51:2` „Mikor ő hozzá ment Nátán…”, a `Zsolt 51:3` „Könyörülj rajtam…”, és van `Zsolt 51:21`. A versmegfeleltetés: `Zsolt 51:3 → kjv 51:1, mt 51:3, MT, lxx_os_etalon_f91`; `Zsolt 51:1–2 → felirat 2 vers`. A `Dán 3:31` szövege „Nabukodonozor király minden népnek…”, a `Dán 4:1` „Én Nabukodonozor békében valék…” (`→ kjv 4:4, KEZI`). — ugyanott
- **Az ütközés következménye:** az MCP `Psalm 51:3` hívása az MT 51:5-öt adja, ami Károli 51:5; a `Psalm 51:21` hívásra nincs adat, holott a Károli 51:21 létezik; a `Daniel 4:1` hívás az MT 3:31-et adja, ami Károli 3:31. — `MCP:get_interlinear('Psalm 51:3')`, `('Psalm 51:21')`, `('Daniel 4:1')`, összevetve a fenti Károli-sorokkal
- **A repó megfeleltetése:** az F85 tartalmi párosítása Needleman–Wunsch-igazítással készült, a TAHOT-versfolyamot a Macula (MT/WLC) versfolyamához igazítva (Jaccard − 0,30, ±80 vers). „A 22 827 azonos kulcsú vers WLC-vel igazolt”. A Macula `karoli` oszlopa (KK/TVTMS-alapú) „megbízhatatlannak bizonyult” eltolt régiókban (Ézs 3, Ézs 9, Én 6, Hós 2 és 12), ezért csak támasznak számít. — [naplok/F85_jelentes.md](file:///C:/Users/bases/Desktop/Bible-Study/naplok/F85_jelentes.md) (43–46. sor)
- **A Karoli_versmegfeleltetes forrása:** az lxx-morph `verse_pairs.jsonl` (TVTMS-alapú MT–KJV kulcs, CC BY 4.0), a Karoli_1908, a TAHOT és kézi eltolások; F91-es javítás a feliratos zsoltárokra. — [konkordancia/Karoli_versmegfeleltetes.tsv](file:///C:/Users/bases/Desktop/Bible-Study/konkordancia/Karoli_versmegfeleltetes.tsv) (fejléc)

### Következtetések
- Az MCP-hez Károli-igehelyet csak a repó `Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopán át lehet küldeni (Károli → KJV/angol hivatkozás). A KJV-típusú könyvekben ez azonosság, a Zsoltárokban és a Dánielben eltolás. A feliratversekre (`igehely_kjv` üres) az MCP-ben nincs külön kulcs: a Zsolt 51:1 hívás az MT 1–3 egyesített szavait adja.
- Az MCP leképezése lényegében ugyanannak a TVTMS/KJV-hagyománynak egy másik példánya, amelyre a repó már épít. Új, független jelet a Károli-oldalra nem ad. A projektnek nincs szüksége rá a versszámozáshoz; ha mégis használja, csak tanúként, `jeloltek.tsv`-n át, provenienciával.
- A Neh 7:68 esete negatív tanulság: a Károli 7:68-nak (és a KJV 7:68-nak) nincs MT-megfelelője, az MCP mégis héber szavakat ad hozzá. Az üres eredmény itt helyes kimenet lenne.

### Gaps
- Nem vizsgáltam az összes ismert eltérést (Ézs 9, Hós 12, Én 6, Préd 12, 4Móz 13, 2Móz 36, Jób 39) az MCP-ben. A mért minta 10 hely.
- Nem tudom, hogy az MCP leképezése TVTMS-ből vagy a BSB saját adatából származik; a ROADMAP.md nem elérhető.
