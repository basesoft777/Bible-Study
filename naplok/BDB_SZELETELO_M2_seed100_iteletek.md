# F99 M2 — a seed-100 újramérés eltéréseinek soronkénti ítélete

*Kézi ítélet a forrásszöveg alapján (`konkordancia/BDB_teljes_unabridged.tsv`, a Strong sora, a szeletelő „lapított” alakjában; a `poz` a
hivatkozás helye). A felhasználó utasítása (2026-10-15): javítás előtt minden eltérés besorolása forrásidézettel — **szeletelő-hiba**,
**kitöltő-hiba** (csak a forrással bizonyítva), **kulcs-ellentmondás**; az ítéleteket a felhasználó hagyja jóvá. Az ítélet a **mért**
állapothoz kötődik: a kulcs `naplok/BDB_SZELETELO_M2_minta_seed100_kulcs.tsv` (a F99.19-es tábla), a kitöltések
`naplok/BDB_SZELETELO_M2_seed100_kitoltott_A.tsv` (M001–M125) és `_B.tsv` (M126–M250), az összevetés
`naplok/BDB_SZELETELO_M2_seed100_osszevetes.txt` (F99.20). A szűrő-lista F99.21-es bővítése ezt nem írja felül. Proveniencia:
`scope=seed-100 vak minta | forras=BDB_teljes_unabridged.tsv + TAHOT_kivonat.tsv (ellenőrzés) | ts=2026-10-15`; az ítélet értelmezés
(manual), nem gépi eredmény.*

## 1. Összesítő

| kategória | jelentéspont (18) | könyv/vers (2) | szűrés (a kulcs szerint téves, 4) | forrás (3) |
|---|---:|---:|---:|---:|
| szeletelő-hiba | **15** | 1 (M013) | 3 (M001, M075 a szövegtanú-szabály szerint; M158 vitás, l. lent) | — |
| kitöltő-hiba (forrással bizonyítva) | 0 | 1 (M134, rövidítés — nem hiba) | 1 (M121) | — |
| kulcs-ellentmondás | **3** | — | — | — |
| `forras_hiba` (a BDB szövegének hibája) | — | — | — | 3 (M006, M064, M079) |

**Kapu (a felhasználó 3. pontja):** a jelentéspontban 15 szeletelő-hiba marad (M076-ot forrásbeli OCR-ként külön is lehet sorolni: akkor
14) — **több mint 6**, tehát a mérce a seed-100-on **nem teljesült**: javítás, újragenerálás, újramérés seed 101-gyel, változatlan
mércével és szabályokkal (a jóváhagyás után). A három kulcs-ellentmondásból kettő a két római szint esete (DT-F99i), egy a szócikk végi
„— Note.” helye.

## 2. Jelentéspont — 18 eltérés

| azon | Strong | kulcs | kitöltés | forrásidézet (a hely környezete) | ítélet | ok |
|---|---|---|---|---|---|---|
| M019 | H5704 עַד | `I -/3` | `III I/3` | „H5704. ad III. עַד … I. preposition 1. of space … 3 Of degree, … Exod 9:7 עַדאֶֿחָד” | **kulcs-ellentmondás** | két római szint: a címszó homonima-száma (III.) és a szócikk fő tagolása (I. preposition); a mai kulcs egy szakasz-mezőt ismer (DT-F99i). A kulcs `I -/3`-a és a kitöltés is helyes a maga szintjén |
| M037 | H8438 תּוֺלָע | `I -/2` | `-/2` (a második címszó alatt) | „… token of luxury Lam 4:5. תּוֺלַ֫עַת תּוֺלֵעָה,_40 noun feminine worm; — … 2 elsewhere (P) specif + שָׁנִי … Lev 14:4, 6, 49, 51” | **szeletelő-hiba** | jelöletlen második címszó két alakkal és vesszővel („תּוֺלַ֫עַת תּוֺלֵעָה,_40 noun”) — a `JELOLETLEN` nem ismeri fel |
| M052 | H7832 שָׂחַק | `fej` | `Qal/1/a` | „— QalPerfect3masculine singular … — 1. a. laugh at … Hab 1:10; Job 5:22” | **szeletelő-hiba** | OCR-ben tapadt törzsnév („QalPerfect”): a Qal nem törzsfejléc, a jelentések a fejbe esnek |
| M065 | H7704 שָׂדֶה | `-/4/f` | `-/1/f` | „… Psa 98:7). שָׂדֶה_318 noun masculine^Lev 27:24 id. … — 1 open field, country: a. … f. open country … Lev 25:31” | **szeletelő-hiba** | a második címszó héber prezentációs alakkal (U+FB2B „שׂ”) áll; a `JELOLETLEN`/`CIM` karakterosztálya ezt nem fedi, a שָׂדַי szakasz 4. pontja alá kerül |
| M076 | H2022 הַר | `-/1/k` | `-/1/m` | „k. as scene of massacre … 1 as places of illicit worship … masculine in various combinations … Deut 32:22” | **szeletelő-hiba** (forrásbeli OCR) | az „l.” „1”-ként, az „m.” „masculine”-ként áll a forrásban; a kitöltő a nyomtatott betűrendet adja. Forrás-OCR-ként is sorolható |
| M078 | H6213 עָשָׂה | `II Qal/2` | `I Qal/2` | „asah I. עָשָׂה … II. 1. make … 2 produce, yield … hippop. producing fat Job 15:27” | **kulcs-ellentmondás** | két római szint: címszó I., fő tagolás II.; a kulcs a tagolást, a kitöltés a címszót írta (DT-F99i) |
| M098 | H9005 לְ | `-/6` | `-/5/g/(c)` | „… 29:5 a. 6 b; compare Ezra 6:7 (Aramaic), 7:28. f. … g. marking the aim … (c) more distinctly on behalf of … Judg 1:1; 20:18” | **szeletelő-hiba** | hamis jelölő: a „29:5 a. 6 b” versrész-hivatkozás „6”-ja jelentés-sorszámnak számít |
| M100 | H9003 בְּ | `-/2` | `I I/2` | „I. בְּ, preposition in … I. In: 1 strictly … 2 of presence in the midst … Deut 7:14; 15:4, 7; 18:10 … II. Denoting proximity … III. 1. With” | **szeletelő-hiba** | a fejléc nem bontódik (a címszó és a homonima-szám hiányzik), és az I.–V. fő tagolás nem ismert fel |
| M105 | H0905 בַּד | `III -/1/b` | `II -/1/b` | „H905. bad II, III. בַּד see below I, II. בדד. II. בָּ֑ד בַּד, noun masculine separation … b. with suffix … Isa 44:24” | **szeletelő-hiba** | a fejléc az utaló csonk („III. בַּד see below”) számát veszi; a valódi címszó a „II. בָּ֑ד בַּד, noun” (két héber alak, a `CIM` nem ismeri fel) |
| M114 | H5973 עִם | `-/5/a` | `-/a` (מֵעִם) | „… compare Lam 4:7). מֵעִם_72 from with or beside …: hence a. after verbs of departing … Deut 18:19; 23:22” | **szeletelő-hiba** | szófaj nélküli jelöletlen alcímszó („מֵעִם_72 from with”) — nem válik külön szakasszá, az 5. pont alá kerül |
| M129 | H0389 אַךְ | `-/2/b` | `-/1` | „אַךְ_159 adverb … 1 surely. 2 with a restrictive force …: a. … b. … only 1 asseverative, … Isa 34:14-15 … 2 restrictive: a.” | **szeletelő-hiba** | a fejléc számozott összefoglalója („1 surely. 2 …”) gondolatjel nélkül; a valódi szerkezet az „1 asseverative”-nél indul |
| M149 | H4911 מָשַׁל | `I Qal/-` | `II Qal` | „II. מָשַׁל verb denominative use a proverb … — Qal … Imperative מְשֹׁל 17:2” | **szeletelő-hiba** | a II. címszó héber prezentációs alakkal (U+FB2A „שׁ”) áll; a `CIM` nem ismeri fel |
| M161 | H6086 עֵץ | `-/1/c` | `-/2/a` | „see ׳אַלְגּ above 2 (approximately 175 times; approximately 120 times plural …) a. wood, as material … Num 31:20, compare 35:18” | **szeletelő-hiba** | a „2 (approximately 175 times …)” jelölő a gyakoriság-zárójel miatt kimarad (csak a „c. N t.”/„kb.” alak engedett) |
| M174 | H5973 עִם | `-/5/a` | `-/a` (מֵעִם) | „מֵעִם_72 from with … a. after verbs of departing … of heart turning י ׳מעם Deut 29:17; 1Kin 11:9” | **szeletelő-hiba** | mint M114 |
| M195 | H6331 פּוּר | `fej` | `Hiph`il/1/b` | „[מָּרַר] verb Hiph`il break, frustrate … — 1 break, violate …: a. … b. of men violating covenant … Deut 31:16” | **szeletelő-hiba** | a fejlécben álló egyetlen törzs („verb Hiph`il break”) nem törzsfejléc; a később álló Hoph`al miatt a Hiph`il jelentései a fejbe esnek |
| M210 | H0758 אֲרָם | `-/2/a` | `-/a` | „— 1 5th son of Shem … 2 grandson of Nahor … 3 1Chr 2:23. 4 a descendant … — Elsewhere only of AramÊan people … a. people … Ezek 16:57; 27:16” | **szeletelő-hiba** | a „3 1Chr 2:23” jelölő (számmal kezdődő könyvnév követi) kimarad, a sor a 2-nél megáll; az „a.” a 2. alá kerül. A kitöltés (`-/a`, a 4. utáni számozatlan rész) a forrás szerint védhető |
| M230 | H6258 עַתָּה | `-/2/g` | `-/2` | „… (b) after a protasis, surely then Gen 31:42 + (see כִּי 1d b, p. 472). — Note. Read עַתָּ כְּמוֺ … for עֵת כְּמוֺ Ezek 16:57” | **kulcs-ellentmondás** | a szócikk végi „— Note.” helye: a kulcs a szövegrend szerint a 2/g-hez köti, a kitöltő a 2-höz; a szabály nem rendezi (egyik sem bizonyítottan hibás) |
| M240 | H1138 בֻּנִּי | `-/-/a` | `-/1/a` | „Bunni בּוּנִּי proper name, masculine see בנה. בֻּנִּי proper name, masculine 1. Levites, a. Neh 9:4” | **szeletelő-hiba** | a második címszó („proper name”) nem ismert fel, és az „1. Levites” (nagybetűs szó követi) jelölő kimarad |

**Okcsoportok (a javítókörhöz):** jelöletlen második címszó/alcímszó (M037, M065, M114, M174, M240); héber prezentációs alak a címszóban
(M065, M149); fejléc (M100, M105, M129, M195); hamis vagy kimaradt számjelölő (M098, M161, M210, M240); OCR (M052, M076); fő tagolás
(M100).

## 3. Könyv/vers — 2 eltérés

| azon | forrásidézet | ítélet |
|---|---|---|
| M013 H6666 | „צ ׳שֶׁמֶשׁ Malachi 3:20 sun of righteousness … his people 5:9; 31:2; 71:2; 89:17; 119:40; 143:1” | **szeletelő-hiba**: a Malakiásnak nincs 143. fejezete; a könyv nem öröklődhet. Javítva (F99.21): `orokles_hibas`, könyv és vers nélkül (bizonytalan) |
| M134 H0594 | „7:7” → kulcs `Ámós 7:7`, kitöltés `Ám 7:7` | nem hiba (könyvrövidítés), mint a seed-99 M012 |

## 4. Szűrés — a kulcs szerint téves sorok (a felhasználó 5. pontja)

| azon | forrásidézet (mi tapad a `^` elé) | ítélet |
|---|---|---|
| M001 H0883 | „compared with לחי, γνάφος, see ᵐ5^Judg 15:9 We^Prol. 344” | **szeletelő-hiba** (a szövegtanú-szabály szerint): a `^` előtt a LXX (`ᵐ5`) szövegtanú-jele áll, nem szerzői sigla. Megjegyzés: a TAHOT a H0883-at a Bír 15:9-ben nem hordozza (a LXX a לְחִי-t fordítja) |
| M075 H8079 | „a kind of lizard (so ᵑ7 ᵑ9 ᵐ5^Lev 11:30 compare Str^Pr” | **szeletelő-hiba** (szövegtanú `ᵐ5^`); a TAHOT a H8079-et a 3Móz 11:30-ban nem hordozza |
| M158 H1988 | „compare Che Hup^Now. Gen 16:13 = here; but here also text is dubious” | **a szabály szerint a szűrés helyes** (a `Hup^Now.` szerzői sigla, F99.17 közvetlen-sigla szabály), **de ellenjelzés**: a TAHOT a H1988 הֲלֹם-ot a 1Móz 16:13-ban hordozza, a forrás a szó saját bibliai helyét idézi („= here”). Döntés kell: a közvetlen-sigla szabály a szó saját helyét is kiszűri |
| M121 H8410 | „compare Di, … — √dubious; Ges 41:19 Thes derives from דהר” | a `nem_bibliai` helyes (Gesenius, Thesaurus); a kitöltés „bizonytalan”-ja nem cáfolja |

## 5. Forráshiba (a felhasználó 6. pontja): `forras_hiba`

A tábla a forrás szövegét rögzíti (könyv, vers, jelentéspont változatlan), az okkód `forras_hiba`; nem szeletelő-hiba, a kapunál nem
számít. A TAHOT ellenőrzés a kitöltő megjegyzését igazolja.

| azon | forrásidézet | a helyes hely (TAHOT) |
|---|---|---|
| M006 H5591 | „see also סוּפָה בְּיוֺם בְּסַעַר Amos 1:14 and Joel 1:4, 12” | Jón 1:4 (H5591 ott áll; a Jóel 1:4-ben nincs) |
| M064 H7913 | „construct א ׳שְׁכֵחֵי Psa 9:8 all nations forgetful of God” | Zsolt 9:18 (H7913 ott áll) |
| M079 H3051 | „Pe`il … 3 masculine singular יְהִיב Ezra 7:4, 6” | Dán 7:4, 6 (H3052 a Dán 7:6-ban; az Ezsd 7:6 héber) |
