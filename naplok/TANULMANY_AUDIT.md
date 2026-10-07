# GENERÁLT: eszkozok/ellenorzes/tanulmany_audit.py — kézzel nem szerkesztendő.

# Tanulmány-audit (CI jelentés mód)

*F37 T3 · jelentés mód: minden tanulmányfájl, nem bukik · commit `5dbee41` · 2026-10-07 · proveniencia: `scope=23 tanulmányfájl | forras=eszkozok/ellenorzes/tanulmany_audit.py | ts=2026-10-07T09:46Z`*

A „szint módosításnál” oszlop azt mutatja, mi lenne a találat szintje, ha egy PR az adott sort módosítaná (a kötelező mód csak az új vagy módosított sort bünteti, D8; az E20 fájlszintű: a módosított tanulmányon mindig piros). Javítást ez a jelentés nem végez (DT-F37-5).

## Összesítő szabályonként

| Szabály | Mit néz | Találat | Fájl | Szint módosításnál |
|---|---|---|---|---|
| E20 | kötelező szakasz (a Tanulmány sablonból) | 0 | 0 | — |
| E13 | kiejtés a héber/görög szó mellett (volt E21) | 206 | 22 | HIBA |
| E8 | versformátum (volt E22) | 32 | 13 | HIBA |
| E9 | angol „sense” (volt E23) | 0 | 0 | — |
| E12 | naplójellegű szöveg 【NAPLO】 blokkon kívül (volt E24) | 195 | 23 | FIGYELMEZTETES |
| E2 | „ellenőrizve” jelölés proveniencia nélkül | 0 | 0 | — |
| E15 | SzPA-idézet hossza | 0 | 0 | — |

## Fájlonként

| Tanulmány | E20 | E13 | E8 | E9 | E12 | E2 | E15 |
|---|---|---|---|---|---|---|---|
| `genezis/1Moz_10v1-11v32_bovitett.md` | · | 7 | 1 | · | 7 | · | · |
| `genezis/1Moz_12v1-20_bovitett.md` | · | 12 | 2 | · | 10 | · | · |
| `genezis/1Moz_13v1-18_bovitett.md` | · | 11 | 2 | · | 7 | · | · |
| `genezis/1Moz_14_bovitett.md` | · | 9 | · | · | 6 | · | · |
| `genezis/1Moz_15_bovitett.md` | · | 2 | 1 | · | 5 | · | · |
| `genezis/1Moz_16_bovitett.md` | · | 8 | 1 | · | 3 | · | · |
| `genezis/1Moz_1v1_bovitett.md` | · | 19 | 1 | · | 14 | · | · |
| `genezis/1Moz_1v2-2v3_bovitett.md` | · | 25 | 3 | · | 29 | · | · |
| `genezis/1Moz_2v4-7_bovitett.md` | · | 6 | 1 | · | 7 | · | · |
| `genezis/1Moz_2v8-25_bovitett.md` | · | 14 | 6 | · | 9 | · | · |
| `genezis/1Moz_3v1-6_bovitett.md` | · | 6 | 2 | · | 9 | · | · |
| `genezis/1Moz_3v7-24_bovitett.md` | · | 18 | 9 | · | 19 | · | · |
| `genezis/1Moz_4v1-24_bovitett.md` | · | 4 | 2 | · | 7 | · | · |
| `genezis/1Moz_4v25-5v32_bovitett.md` | · | 7 | 1 | · | 9 | · | · |
| `genezis/1Moz_6v1-8_bovitett.md` | · | 14 | · | · | 7 | · | · |
| `genezis/1Moz_6v9-22_bovitett.md` | · | 9 | · | · | 6 | · | · |
| `genezis/1Moz_7v1-24_bovitett.md` | · | 9 | · | · | 10 | · | · |
| `genezis/1Moz_8v1-22_bovitett.md` | · | 9 | · | · | 6 | · | · |
| `genezis/1Moz_9v1-17_bovitett.md` | · | 5 | · | · | 5 | · | · |
| `genezis/1Moz_9v18-29_bovitett.md` | · | 6 | · | · | 9 | · | · |
| `ujszovetseg/1Thessz_5v23_bovitett.md` | · | · | · | · | 2 | · | · |
| `ujszovetseg/Rom_8v10_bovitett.md` | · | 3 | · | · | 4 | · | · |
| `ujszovetseg/Zsid_4v12_bovitett.md` | · | 3 | · | · | 5 | · | · |

## Találatok

### `genezis/1Moz_10v1-11v32_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: מִגְדָּל/אֲגַדְּלָה -- *v7 — 2026.09.03 (Sod-pont kiegészítve a מִגְדָּל/אֲגַדְּלָה [11:4↔12:2] közös |
| E13 | 5 | HIBA | kiejtes nelkul: גדל -- גדל gyök lelettel — ellentétes visszhang: Bábel önerőből, Ábrám ajándékba |
| E13 | 159 | HIBA | kiejtes nelkul: גדל -- A מִגְדָּל ("torony", 11:4) és az אֲגַדְּלָה ("naggyá teszem", 12:2) azonos גדל gyökből képződik — nem tematikus, hanem  |
| E13 | 224 | HIBA | kiejtes nelkul: שֵׁם -- A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárt két korábban  |
| E13 | 230 | HIBA | kiejtes nelkul: צַיִד גִּבּוֹר -- \| צַיִד גִּבּוֹר (H6679/H6718) \| ✅ \| H6679↔H6718 kölcsönös/denominatív, egy gyökcsalád — triviális \| 18 / 19 \| nincs öná |
| E13 | 232 | HIBA | kiejtes nelkul: שָׂפָה אֶחָת -- \| שָׂפָה אֶחָת (H8193+H259) \| ✅ \| H8193 ← H5595/H8192/H5490 (3 Strong-only javaslat) — BDB egyiket sem erősíti meg, önál |
| E13 | 234 | HIBA | kiejtes nelkul: שָׁמַיִם -- \| שֵׁם / sém (H8034) \| ✅ \| két Strong-only javaslat (← H7760 "elhelyezni"; ← H8064 "ég") — **egyik sem BDB-igazolt** ("√ |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 10:1" -- # 1Mózes 10:1–11:32 — Népek táblázata, Bábel tornya, Sém toledotja |
| E12 | 4 | FIGYELMEZTETES | *v7 — 2026.09.03 (Sod-pont kiegészítve a מִגְדָּל/אֲגַדְּלָה [11:4↔12:2] közös |
| E12 | 9 | FIGYELMEZTETES | *v6 — 2026.08.15 (Alkalmazás pont kiegészítve nevesített tanítói szemszögekkel: Derek Prince — Blessing and Curses [Kánaán-átok, 9:25-27↔10:15-19]; Ke |
| E12 | 116 | FIGYELMEZTETES | Ehhez a mintázathoz egy önálló lexikai szál is társul: a **migdal** ("torony", 11:4) ugyanabból a **גדל** ("naggyá lenni/válni") gyökből képződik, min |
| E12 | 224 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárt két korábban dokumentálatlan O |
| E12 | 237 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv'. |
| E12 | 241 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Belső önellenőrzés |
| E12 | 250 | FIGYELMEZTETES | - ✅ Motívum-napló frissítése **külön lépésként** vár — szólj, ha mehet a 'PaRDeS_motivumok.md' frissítése (v27→v28) |

### `genezis/1Moz_12v1-20_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 7 | HIBA | kiejtes nelkul: גדל -- *v3 — 2026.09.03 (גדול/אגדלה polyptoton hozzáadva a kulcsszótáblához és a Peshat-ponthoz — a "nagy nemzet" [12:2] és a " |
| E13 | 8 | HIBA | kiejtes nelkul: מִזְבֵּחַ -- *v2 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a |
| E13 | 22 | HIBA | kiejtes nelkul: יְהוָה אמר -- Mózesként azonosított szerző/redaktor (hagyomány szerint), aki a Sínai-pusztai Izrael számára rögzíti ősei történetét —  |
| E13 | 73 | HIBA | kiejtes nelkul: גדל -- \| 12:2 \| אֲגַדְּלָה \| *agaddelá* \| H1431 \| "naggyá teszem" [a nevedet] — ugyanaz a גדל gyök, mint az előző sorban (גּוֹי |
| E13 | 88 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- *Megjegyzés: e szakaszban πνεῦμα/ψυχή megkülönböztetés nem releváns — a fejezet nem tartalmazza egyik kulcsfogalmat sem. |
| E13 | 96 | HIBA | kiejtes nelkul: גדל -- YHWH radikális elhívással szólítja meg Ábrámot: három lépésben szakítja el korábbi identitásától — föld, rokonság, atyai |
| E13 | 132 | HIBA | kiejtes nelkul: ἐνευλογηθήσονται -- > *(kulcsszó: **áldás** — héberül *berachá*/*nivrechú*, a Septuaginta ἐνευλογηθήσονται kifejezésén keresztül közvetítve  |
| E13 | 202 | HIBA | kiejtes nelkul: גּוֹי -- A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárt két korábban  |
| E13 | 209 | HIBA | kiejtes nelkul: גּוֹי גָּדוֹל -- \| גּוֹי גָּדוֹל (H1471+H1419) \| ✅ \| H1471 ← H1465 "hátrész/tömeg" — **Strong-only, BDB nem ad gyököt** — elutasítva; H14 |
| E13 | 213 | HIBA | kiejtes nelkul: קָרָא בְשֵׁם יְהוָה -- \| קָרָא בְשֵׁם יְהוָה (H7121+H8034) \| ✅ \| H7121 nincs/bizonytalan (primitív, esetleg H7122); H8034 két Strong-only javas |
| E13 | 215 | HIBA | kiejtes nelkul: נְגָעִים גְּדֹלִים -- \| נְגָעִים גְּדֹלִים (H5061+H1419) \| ✅ \| H5061←H5060 "érinteni" triviális; H1419←H1431 (l. fent) \| 78 / 526 \| nincs önál |
| E13 | 220 | HIBA | kiejtes nelkul: ἔθνη -- - גּוֹי (H1471, "nemzet") ↔ Gal 3:8 ἔθνη (G1484): valódi LXX-fordítási lánc, de nagyon gyakori szó (164 NT-előfordulás), |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 12:1" -- # 1Mózes 12:1-20 — bővített PaRDeS tanulmány |
| E8 | 80 | HIBA | tiltott igehely-format: "Gen.12.7" -- **⚠️ Megjegyzés a מִזְבֵּחַ (mizbéach, "oltár") vershez rendeléséről:** Ábrám ebben a fejezetben **két külön** oltárt épít — Gen.12.7-nél (Sik |
| E12 | 3 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *v4 — 2026.09.03 (Retroaktív „7. Lexikai audit — módszertani napló" |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: szakasz felvéve, a v16 sablon kötelező elemének visszamenőleges |
| E12 | 5 | FIGYELMEZTETES | pótlása — a 2026.09.03-i eredeti audit eredményének formalizálása, új |
| E12 | 7 | FIGYELMEZTETES | *v3 — 2026.09.03 (גדול/אגדלה polyptoton hozzáadva a kulcsszótáblához és a Peshat-ponthoz — a "nagy nemzet" [12:2] és a "naggyá teszem nevedet" [12:2]  |
| E12 | 8 | FIGYELMEZTETES | *v2 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a TAHOT_kivonat.tsv alapján a l |
| E12 | 9 | FIGYELMEZTETES | *v1 — 2026.08.15* |
| E12 | 141 | FIGYELMEZTETES | > 📎 Bővebben, önálló tematikus feldolgozásban: 'Segitsegul_hivni_az_Urat_tematikus.md' (Segítségül hívni az Úr nevét) — ez a study a 12:8-ban dokument |
| E12 | 202 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárt két korábban dokumentálatlan O |
| E12 | 208 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: \| בְּרָכָה / berachá (H1293) \| ✅ \| ← H1288 (*barakh*, "áldani") triviális (a H1288-kérdés önálló, nagyobb téma, l. korrekciós Code-prompt |
| E12 | 217 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv'. |

### `genezis/1Moz_13v1-18_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 5 | HIBA | kiejtes nelkul: שָׂא -- study szövegében kétszer [13:10, 13:14] megjelenő שָׂא...עֵינָיו |
| E13 | 11 | HIBA | kiejtes nelkul: יהוה -- J4-torzítása [יהוה gyakorisága] tisztázva)* |
| E13 | 115 | HIBA | kiejtes nelkul: קָרָא בְשֵׁם יְהוָה -- **Segítségül hívta az Úr nevét (קָרָא בְשֵׁם יְהוָה)** — ⭐ **ez a harmadik előfordulás, elérte az emlékeztető küszöböt.* |
| E13 | 170 | HIBA | kiejtes nelkul: קָרָא, נָשָׂא, עַיִן, רָאָה, אֶרֶץ -- A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. A 2/f (rögzült szópár együttes-előfordulás) már korábba |
| E13 | 174 | HIBA | kiejtes nelkul: קָרָא בְשֵׁם יְהוָה -- \| קָרָא בְשֵׁם יְהוָה (H7121+H3068) \| ✅ \| H7121 nincs (primitív gyök); H3068 ← "lenni" közismert, nem hoz új tartalmat \| |
| E13 | 175 | HIBA | kiejtes nelkul: וַיִּשָּׂא -- \| וַיִּשָּׂא...וַיַּרְא (H5375+H5869+H7200) \| ✅ \| mind primitív gyök/szó, nincs lánc \| 656 / 886 / 1299 \| ✅ 2/f: szópár  |
| E13 | 177 | HIBA | kiejtes nelkul: רָעִים וְחַטָּאִים -- \| רָעִים וְחַטָּאִים (H7451+H2400) \| ✅ \| H7451←H7489 triviális (l. '1Moz_3v1-6'); H2400 ← "vétkezni" triviális \| 662 / 1 |
| E13 | 178 | HIBA | kiejtes nelkul: שָׂא נָא עֵינֶיךָ -- \| שָׂא נָא עֵינֶיךָ (H5375+H5869) \| ✅ \| l. fenti sor \| l. fenti sor \| l. fenti sor (2/f) \| nem releváns \| megerősítve \| |
| E13 | 179 | HIBA | kiejtes nelkul: כַּעֲפַר הָאָרֶץ -- \| כַּעֲפַר הָאָרֶץ (H6083+H776) \| ✅ \| H6083 ← "por" denominatív, fordított irány; H776 ← "szilárdnak lenni" (elveszett g |
| E13 | 180 | HIBA | kiejtes nelkul: וַיִּבֶן -- \| וַיִּבֶן...מִזְבֵּחַ (H1129+H4196) \| ✅ \| H1129 ← "építeni" triviális; H4196 ← "áldozni" triviális \| 376 / 401 \| nincs  |
| E13 | 182 | HIBA | kiejtes nelkul: יהוה -- **J4-torzítás tisztázva:** a kockázat-riport által jelzett magas ("5523 sosem idézett") szám kizárólag a יהוה (H3068) re |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 13:1" -- # 1Mózes 13:1-18 — Ábrám és Lót elválása; az ígéret megújítása |
| E8 | 17 | HIBA | tiltott igehely-format: "1Mózes 12:1" -- A sorozat eddig eljutott 1Mózes 12:1-20-ig: Ábrám elhívása (*lech-lechá*), az első két oltár (Sikem, Bétel-Ai között), a hétrészes áldás-íg |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *v3 — 2026.09.04 (Retroaktív 2/f-audit [protokoll v5] elvégezve: a |
| E12 | 9 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 119 | FIGYELMEZTETES | > 📎 Bővebben, önálló tematikus feldolgozásban: 'Segitsegul_hivni_az_Urat_tematikus.md' (Segítségül hívni az Úr nevét) — a 13:4-ben dokumentált "vissza |
| E12 | 170 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. A 2/f (rögzült szópár együttes-előfordulás) már korábban (2026.09.04) le |
| E12 | 184 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'TAHOT_kivonat.tsv'. |
| E12 | 188 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Önellenőrzés (belső, a végleges válasz előtt lefuttatva) |
| E12 | 200 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Javasolt motívum-napló frissítés *(csak jóváhagyás után kerül be a 'PaRDeS_motivumok.md' fájlba — mondd, hogy "Motívum fájlt", ha szer |

### `genezis/1Moz_14_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: חנך -- nincs új tartalmi lelet; a study saját חנך [chanikáv/chanukká] |
| E13 | 70 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- **πνεῦμα/ψυχή-megjegyzés:** e fejezetben egyik szó sem fordul elő — nem releváns. |
| E13 | 185 | HIBA | kiejtes nelkul: יַיִן, קֹנֵה, יָד -- A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a |
| E13 | 191 | HIBA | kiejtes nelkul: לֶחֶם וָיַיִן -- \| לֶחֶם וָיַיִן (H3899+H3196) \| ✅ \| H3899 ← "harcolni" valódi gyök-egybeesés, BDB nem ad etimológiát, study nem is állít |
| E13 | 192 | HIBA | kiejtes nelkul: אֵל עֶלְיוֹן -- \| אֵל עֶלְיוֹן (H410+H5945) \| ✅ \| H5945 ← עלה "felemelkedni" triviális \| 240 / 53 \| nincs önálló \| nem releváns \| megerő |
| E13 | 193 | HIBA | kiejtes nelkul: קֹנֵה שָׁמַיִם וָאָרֶץ -- \| קֹנֵה שָׁמַיִם וָאָרֶץ (H7069) \| ✅ \| nincs (primitív gyök, "venni/birtokolni" — a study már tárgyalja a "birtokosa/alk |
| E13 | 194 | HIBA | kiejtes nelkul: עֶשֶׂר -- \| מַעֲשֵׂר / maaszér (H4643) \| ✅ \| ← עֶשֶׂר "tíz" triviális \| 32 \| nincs önálló \| nem releváns \| megerősítve \| |
| E13 | 195 | HIBA | kiejtes nelkul: נָשָׂאתִי יָדִי -- \| נָשָׂאתִי יָדִי (H5375+H3027) \| ✅ \| mindkettő primitív, nincs lánc \| 656 / 1619 \| nincs önálló \| nem releváns \| megerő |
| E13 | 197 | HIBA | kiejtes nelkul: βασιλεύς -- **LXX-híd, ellenőrizve, nincs teendő:** Zsid 7:2 ↔ βασιλεύς (G0935) és G4532 — a study 4. pontja már explicit idézi és t |
| E12 | 3 | FIGYELMEZTETES | *v3 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 7 | FIGYELMEZTETES | *v2 — 2026.08.16 (kiegészítve: az Ábrám-Sodoma király esküjéhez [14:22-23] korábban jelzett tanítói gap pótolva — Kenneth Copeland Ministries elsődleg |
| E12 | 124 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Melkizedek_tematikus.md' (Melkizedek — király-pap rendje, kenyér és bor — a motívum teljes kánoni íve: 2 |
| E12 | 126 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Rafaim_tematikus.md' (Rafeusok/óriás-népek — a 14:5-ben dokumentált רְפָאִים/Zuzim/Émim népcsoportot a t |
| E12 | 185 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokumen |
| E12 | 199 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAGNT_kivonat.tsv'. |

### `genezis/1Moz_15_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 166 | HIBA | kiejtes nelkul: אָמַן, חָשַׁב, צְדָקָה, עָנָה -- A 2/a-2/e technikasor lefutott a study mind a 11 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta  |
| E13 | 182 | HIBA | kiejtes nelkul: δικαιοσύνη -- **LXX-híd, ellenőrizve, nincs teendő:** Róm 4:3 ↔ δικαιοσύνη (G1343) és λογίζομαι (G3049) — a study 4. pontja már explic |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 15:1" -- # 1Mózes 15:1-21 — bővített PaRDeS tanulmány |
| E12 | 2 | FIGYELMEZTETES | *v2 — 2026.09.03 (Formázási hiba javítva: két nyers, meg nem jelenített |
| E12 | 166 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 11 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokume |
| E12 | 184 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAGNT_kivonat.tsv'. |
| E12 | 188 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Motívum-napló frissítés |
| E12 | 190 | FIGYELMEZTETES | Ez a tanulmány több új, illetve ismétlődő motívumot azonosított (hit mint betudott igazság — 15:6, első előfordulás; brit bén habetárim / a szövetség  |

### `genezis/1Moz_16_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 5 | HIBA | kiejtes nelkul: יהוה -- J4-torzítása [יהוה gyakorisága] tisztázva)* |
| E13 | 71 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- *Megjegyzés a πνεῦμα/ψυχή megkülönböztetésről:* e szakaszban egyik szó héber megfelelője (*rúach*/*nefes*) sem fordul el |
| E13 | 182 | HIBA | kiejtes nelkul: עָצַר, מַלְאָךְ, בְּאֵר לַחַי רֹאִי -- A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a |
| E13 | 189 | HIBA | kiejtes nelkul: מַלְאַךְ יְהוָה -- \| מַלְאַךְ יְהוָה (H4397+H3068) \| ✅ \| H4397 ← "elküldeni, mint megbízottat" — elveszett gyök; H3068 ← "lenni" közismert  |
| E13 | 190 | HIBA | kiejtes nelkul: שמע -- \| יִשְׁמָעֵאל / Jismáél (H3458) \| ✅ \| ← שמע "hallani" — már kifejtve a 6. pontban \| 48 \| ✅ már beépítve ("Isten meghallj |
| E13 | 191 | HIBA | kiejtes nelkul: אֵל רֳאִי -- \| אֵל רֳאִי (H410+H7210) \| ✅ \| H7210 ← ראה "látni" — már kifejtve a 6. pontban \| 240 / 5 \| ✅ már beépítve ("a látás Iste |
| E13 | 192 | HIBA | kiejtes nelkul: בְּאֵר לַחַי רֹאִי -- \| בְּאֵר לַחַי רֹאִי (H883) \| ✅ \| összetett tulajdonnév: H875 (kút) + H2416 (élő) + H7203 (látó) — a study saját fordítá |
| E13 | 194 | HIBA | kiejtes nelkul: Ἁγάρ -- **LXX-híd, ellenőrizve, nincs teendő:** Gal 4:24-25 ↔ Ἁγάρ (G0028) — a 4. pont már explicit, névvel tárgyalja ezt a kapc |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 16:1" -- # 1Mózes 16:1-16 — Hágár és Ismáel születése |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 182 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokumen |
| E12 | 196 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'TAGNT_kivonat.tsv'. |

### `genezis/1Moz_1v1_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: הַשָּׁמַיִם/הָאָרֶץ -- study szövegében ténylegesen együtt szereplő הַשָּׁמַיִם/הָאָרֶץ merizmus |
| E13 | 9 | HIBA | kiejtes nelkul: בְּרֵאשִׁית -- *v5 — 2026.09.02 (teljes lexikai újraaudit: mind az 5 tartalmi szó [בְּרֵאשִׁית, |
| E13 | 10 | HIBA | kiejtes nelkul: בָּרָא, אֱלֹהִים, הַשָּׁמַיִם, הָאָרֶץ -- בָּרָא, אֱלֹהִים, הַשָּׁמַיִם, הָאָרֶץ] önállóan, a teljes BDB-szócikkből |
| E13 | 12 | HIBA | kiejtes nelkul: בָּרָא -- a jelenlegi értelmezés megerősítve, eltérés nélkül; 1 szónál [בָּרָא] új, |
| E13 | 15 | HIBA | kiejtes nelkul: ἀρχή -- Ján 1:1 és Zsid 1:10 megerősítve [közös szó: ἀρχή, azonos jelentésárnyalat], |
| E13 | 79 | HIBA | kiejtes nelkul: ἐν ἀρχῇ ἐποίησεν ὁ θεὸς -- *📚 Lexikai megerősítés (2026.09.02):* ez nem csak tartalmi, hanem szó szerint lexikai visszhang. A LXX Genezis 1:1 (ἐν ἀ |
| E13 | 112 | HIBA | kiejtes nelkul: ἀρχή -- > János evangélista szó szerint a Genezis nyitószavát idézi, hogy Krisztust — mint megtestesült Igét — állítsa a teremté |
| E13 | 115 | HIBA | kiejtes nelkul: κατ -- > *"...Te Uram kezdetben (κατ' ἀρχάς) alapítottad a földet és a te kezeidnek művei az egek..."* **(kulcsszó: kezdetben — |
| E13 | 130 | HIBA | kiejtes nelkul: ἀρχή -- > ⚠️ **Lexikai figyelmeztetés (2026.09.02):** a Kol 1:16 idézet **helyesen NEM** a ἀρχή-szóegyezésre épül (bár a vers ké |
| E13 | 205 | HIBA | kiejtes nelkul: בְּרֵאשִׁית -- \| בְּרֵאשִׁית (H7225) \| ✅ \| nincs \| 51 \| nincs önálló \| nem releváns \| megerősítve, nincs eltérés \| |
| E13 | 206 | HIBA | kiejtes nelkul: בָּרָא -- \| בָּרָא (H1254) \| ✅ \| nincs \| 55 \| ✅ új érv talált (l. Drash 2.) \| nem releváns \| beépítve \| |
| E13 | 207 | HIBA | kiejtes nelkul: אֱלֹהִים -- \| אֱלֹהִים (H430) \| ✅ \| nincs \| 2603 \| nincs önálló \| nem releváns \| megerősítve, nincs eltérés \| |
| E13 | 208 | HIBA | kiejtes nelkul: הַשָּׁמַיִם -- \| הַשָּׁמַיִם (H8064) \| ✅ \| nincs \| 420 \| ✅ 2/f: הַשָּׁמַיִם/הָאָרֶץ merizmus, 180 közös igehely — túl gyakori, nem rejt |
| E13 | 209 | HIBA | kiejtes nelkul: הָאָרֶץ -- \| הָאָרֶץ (H776) \| ✅ \| nincs \| 2504 \| l. fenti sor (2/f) \| nem releváns \| megerősítve \| |
| E13 | 215 | HIBA | kiejtes nelkul: ἀρχή -- \| Ján 1:1 \| ἀρχή (G0746) \| igen \| igen (1. jelentés mindkét helyen) \| ✅ megerősítve \| |
| E13 | 216 | HIBA | kiejtes nelkul: ἀρχή -- \| Zsid 1:10 \| ἀρχή (G0746) \| igen \| igen \| ✅ megerősítve, ÚJ idézetként felvéve \| |
| E13 | 217 | HIBA | kiejtes nelkul: ἀρχή -- \| Kol 1:16 \| ἀρχή (G0746) \| igen \| **NEM** (3. jelentés ott) \| ⚠️ hamis pozitív, dokumentálva \| |
| E13 | 218 | HIBA | kiejtes nelkul: θεός -- \| Zsid 11:3 \| — \| — \| — \| nincs releváns közös szó (csak generikus θεός) \| |
| E13 | 220 | HIBA | kiejtes nelkul: ἀρχή -- **Amit ez a módszer NEM tett meg** (átláthatóság kedvéért): nem futott le formális "13-as kör" szűrés (ez a tanulmány ne |
| E8 | 1 | HIBA | tiltott igehely-format: "1 Mózes 1:1" -- # 1 Mózes 1:1 — Bővített PaRDeS tanulmány |
| E12 | 3 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *v6 — 2026.09.04 (Retroaktív 2/f-audit [protokoll v5] elvégezve: a |
| E12 | 9 | FIGYELMEZTETES | *v5 — 2026.09.02 (teljes lexikai újraaudit: mind az 5 tartalmi szó [בְּרֵאשִׁית, |
| E12 | 20 | FIGYELMEZTETES | *v4 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a teljes tanulmány egyetlen ver |
| E12 | 21 | FIGYELMEZTETES | *v3 — 2026.07.30 (nevesített tanítói szemszög részletesen kifejtve)* |
| E12 | 26 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: eddig nem készült önálló tanulmány 1Mózesből (a könyv csak keresztutalásként szerepelt — 1Móz 2:7 az 1The |
| E12 | 67 | FIGYELMEZTETES | *📚 Lexikai teljesség-ellenőrzés (2026.09.02):* mind az 5 tartalmi szó teljes BDB-szócikke (nem csak a rövid TBESH-kivonat) átnézve, Origin-lánc követv |
| E12 | 79 | FIGYELMEZTETES | *📚 Lexikai megerősítés (2026.09.02):* ez nem csak tartalmi, hanem szó szerint lexikai visszhang. A LXX Genezis 1:1 (ἐν ἀρχῇ ἐποίησεν ὁ θεὸς...) és Ján |
| E12 | 91 | FIGYELMEZTETES | - **📚 Új lexikai adalék a vitához (2026.09.02, teljes BDB-szócikk alapján):** a *bará* gyök sémi rokonai (arab: "vágással formázni, kifaragni — nádtol |
| E12 | 114 | FIGYELMEZTETES | > 🔗 ⇒ **Zsid 1:10** *(beteljesedés, ÚJ, 2026.09.02)* |
| E12 | 130 | FIGYELMEZTETES | > ⚠️ **Lexikai figyelmeztetés (2026.09.02):** a Kol 1:16 idézet **helyesen NEM** a ἀρχή-szóegyezésre épül (bár a vers később, a "ἀρχαὶ" — "fejedelemsé |
| E12 | 132 | FIGYELMEZTETES | > *Ismétlődő motívum korábbi tanulmányodból: Zsid 4:12 (2026.07.28) — "ige mint megtestesült Logosz", ott Ján 1:1,14 kapcsolódással. Ez a 2. előfordul |
| E12 | 154 | FIGYELMEZTETES | **Bibliai nyelvek** — A בָּרָא (*bará*) ige egyedisége (kizárólag Isten alanyisággal fordul elő) és az אֱלֹהִים (*elohím*) többes alakja egyes számú i |
| E12 | 199 | FIGYELMEZTETES | ## 7. Lexikai audit — módszertani napló (2026.09.02, oszlop-bővítve 2026.09.05, 3/b terv) |
| E12 | 220 | FIGYELMEZTETES | **Amit ez a módszer NEM tett meg** (átláthatóság kedvéért): nem futott le formális "13-as kör" szűrés (ez a tanulmány nem tagja annak a listának); a m |

### `genezis/1Moz_1v2-2v3_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: תֹהוּ וָבֹהוּ -- תֹהוּ וָבֹהוּ [H8414/H0922] szópár teljes körű együttes-előfordulás |
| E13 | 15 | HIBA | kiejtes nelkul: בָּרַךְ -- és nyelvészetileg túlállító volt. A "## 7. Lexikai audit" szakasz בָּרַךְ |
| E13 | 19 | HIBA | kiejtes nelkul: תְהוֹם -- *v4 — 2026.09.02 (teljes lexikai újraaudit a szakasz kulcsszavain: תְהוֹם, |
| E13 | 22 | HIBA | kiejtes nelkul: תְהוֹם/הום -- תְהוֹם/הום-gyök "morajlás" etimológia MEGERŐSÍTVE, helyes forrással |
| E13 | 24 | HIBA | kiejtes nelkul: צֶלֶם -- helyesbítve; (2) צֶלֶם [celem] etimológiai háttere ["kifaragott/kivésett |
| E13 | 28 | HIBA | kiejtes nelkul: φῶς -- estek át: φῶς [Ján 1:5, 2Kor 4:6], εἰκών [Kol 1:15 + Kol 3:10, Ef 4:24, |
| E13 | 29 | HIBA | kiejtes nelkul: θῆλυ -- 2Kor 3:18, 1Kor 11:7 — kibővítve], θῆλυ [Mt 19:4, Mk 10:6 — ÚJ idézet], |
| E13 | 30 | HIBA | kiejtes nelkul: ἕβδομος -- ἕβδομος+καταπαύω [Zsid 4:4 — pontosítás Zsid 4:9-11 mellett].)* |
| E13 | 32 | HIBA | kiejtes nelkul: צֶלֶם -- *v3 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül —  |
| E13 | 89 | HIBA | kiejtes nelkul: הום -- **⚠️ Megjegyzés a תְהוֹם (*tehóm*) gyökeréről (helyesbítve, 2026.09.02):** a szó a הום-gyökből ered — ezt a BDB **nem**  |
| E13 | 95 | HIBA | kiejtes nelkul: πνεῦμα -- **⚠️ Megjegyzés a רוּחַ (*ruach*) fordításáról:** A Károli "Isten Lelke" fordítása itt is elmossa a *ruach* elsődleges j |
| E13 | 250 | HIBA | kiejtes nelkul: ἄρσεν καὶ θῆλυ -- > **Lexikailag igazolt idézet**: Jézus a válás kérdésében szó szerint az 1Móz 1:27 LXX-fordítását idézi ("ἄρσεν καὶ θῆλυ |
| E13 | 260 | HIBA | kiejtes nelkul: φῶς -- > Pál kifejezetten az 1Móz 1:3 teremtő szavát vonatkoztatja az újjászületés belső megvilágosodására — ugyanaz a szó (φῶς |
| E13 | 262 | HIBA | kiejtes nelkul: תֹהוּ וָבֹהוּ -- **Remez** — [a תֹהוּ וָבֹהוּ formátlan/üres kezdőállapot mint a teremtés-előtti negatív minta — ugyanez a ritka szópár a |
| E13 | 288 | HIBA | kiejtes nelkul: צֶלֶם -- > **📚 Kiegészítés (2026.09.02, LXX-alapú lexikai audit):** a LXX 1Móz 1:26 (צֶלֶם → εἰκών) és Kol 1:15 közös szava (εἰκώ |
| E13 | 369 | HIBA | kiejtes nelkul: תְהוֹם -- \| תְהוֹם (H8415) \| ✅ \| igen → H1949 \| 35 \| ✅ helyesbítve, הום-gyök megerősítve \| nem releváns \| helyesbítve \| |
| E13 | 370 | HIBA | kiejtes nelkul: רוּחַ -- \| רוּחַ (H7307) \| ✅ \| nincs \| 377 \| nincs önálló \| nem releváns \| megerősítve \| |
| E13 | 371 | HIBA | kiejtes nelkul: אוֹר -- \| אוֹר (H216) \| ✅ \| nincs \| 120 \| nincs önálló \| ✅ φῶς (G5457), Ján 1:5/2Kor 4:6 \| megerősítve \| |
| E13 | 372 | HIBA | kiejtes nelkul: צֶלֶם -- \| צֶלֶם (H6754) \| ✅ \| nincs \| 17 \| ✅ új érv (l. Drash 2.); + 3. jelentés feltárva (l. Remez) \| ✅ εἰκών (G1504), 5 idézet |
| E13 | 373 | HIBA | kiejtes nelkul: זָכָר/נְקֵבָה -- \| זָכָר/נְקֵבָה (H2145+H5347) \| ✅ \| nincs \| 82 / 22 \| nincs önálló \| ✅ θῆλυ (G2338), Mt 19:4/Mk 10:6 \| megerősítve \| |
| E13 | 374 | HIBA | kiejtes nelkul: שָׁבַת -- \| שָׁבַת (H7673) \| ✅ \| nincs \| 71 \| nincs önálló \| ✅ ἕβδομος+καταπαύω, Zsid 4:4 \| megerősítve \| |
| E13 | 375 | HIBA | kiejtes nelkul: בָּרַךְ -- \| בָּרַךְ (H1288) \| ✅ \| nincs \| 330 \| nincs önálló (apró etimológiai adalék, l. 2. pont) \| nem releváns \| megerősítve \| |
| E13 | 376 | HIBA | kiejtes nelkul: קָדַשׁ -- \| קָדַשׁ (H6942) \| ✅ \| nincs \| 171 \| nincs önálló \| nem releváns \| megerősítve \| |
| E13 | 378 | HIBA | kiejtes nelkul: תֹהוּ וָבֹהוּ -- **2/f — Rögzült szópár együttes-előfordulás ellenőrzése (2026.09.04, protokoll v5):** a תֹהוּ וָבֹהוּ (H8414/H0922) szóp |
| E13 | 380 | HIBA | kiejtes nelkul: תֹהוּ וָבֹהוּ -- **Amit ez a módszer NEM tett meg:** a motívumnapló ('PaRDeS_motivumok.md') érintetlen maradt — sem az εἰκών/*celem*-lele |
| E8 | 1 | HIBA | tiltott igehely-format: "1 Mózes 1:2" -- # 1 Mózes 1:2 – 2:3 — Bővített PaRDeS tanulmány |
| E8 | 39 | HIBA | tiltott igehely-format: "1Mózes 1:1" -- *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: már készült tanulmány 1Mózesből (1Mózes 1:1), ezért ez a pont aktiválódik.* Az előző tanulmány  |
| E8 | 129 | HIBA | tiltott igehely-format: "Gen.1.26" -- **⚠️ Megjegyzés a צֶלֶם (celem) vershez rendeléséről (TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ):** a szó a 'TAHOT_kivonat.tsv' szerint mindkét ver |
| E12 | 3 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *v6 — 2026.09.04 (Retroaktív 2/f-audit [protokoll v5] elvégezve: a |
| E12 | 8 | FIGYELMEZTETES | motívumnapló-felvétel [PaRDeS_motivumok.md] külön, még hátralévő lépés.)* |
| E12 | 10 | FIGYELMEZTETES | *v5 — 2026.09.03 (Csonkítva a וַיְבָרֶךְ/H1288 etimológiai megjegyzés a |
| E12 | 19 | FIGYELMEZTETES | *v4 — 2026.09.02 (teljes lexikai újraaudit a szakasz kulcsszavain: תְהוֹם, |
| E12 | 23 | FIGYELMEZTETES | [H1949, l. 2. pont] — a korábbi, tévesen "nem igazolható" minősítés |
| E12 | 32 | FIGYELMEZTETES | *v3 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a TAHOT_kivonat.tsv alapján mi |
| E12 | 33 | FIGYELMEZTETES | *v2 — 2026.08.15 (kiegészítve: Nevesített tanítói szemszög az Alkalmazás pontban — Capps, Hagin, Copeland, Derek Prince, Wigglesworth)* |
| E12 | 39 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: már készült tanulmány 1Mózesből (1Mózes 1:1), ezért ez a pont aktiválódik.* Az előző tanulmány a "Kezdetb |
| E12 | 89 | FIGYELMEZTETES | **⚠️ Megjegyzés a תְהוֹם (*tehóm*) gyökeréről (helyesbítve, 2026.09.02):** a szó a הום-gyökből ered — ezt a BDB **nem** a תְהוֹם (H8415) szócikke alat |
| E12 | 129 | FIGYELMEZTETES | **⚠️ Megjegyzés a צֶלֶם (celem) vershez rendeléséről (TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ):** a szó a 'TAHOT_kivonat.tsv' szerint mindkét versben elő |
| E12 | 131 | FIGYELMEZTETES | **📚 Lexikai kiegészítés a צֶלֶם (celem) etimológiájáról (ÚJ, 2026.09.02, teljes BDB-szócikk alapján):** a BDB szerint a szó eredeti jelentése *"valami |
| E12 | 134 | FIGYELMEZTETES | visszhang (ÚJ, 2026.09.02, teljes-előfordulás feltárás alapján):** a BDB |
| E12 | 187 | FIGYELMEZTETES | **📚 Lexikai ellenőrzés (2026.09.02):** mindhárom ige teljes BDB-szócikke ellenőrizve — nincs eltérés a jelenlegi értelmezéstől. Egy apró etimológiai a |
| E12 | 208 | FIGYELMEZTETES | pozitív kijelentésének (l. 2. pont lexikai kiegészítése). |
| E12 | 230 | FIGYELMEZTETES | - **📚 Lexikai megerősítés Middleton nézetéhez (ÚJ, 2026.09.02):** a *celem* szó etimológiai háttere (l. 2. pont) — "kifaragott/kivésett kép", túlnyomó |
| E12 | 248 | FIGYELMEZTETES | > 🔗 ⇒ **Mt 19:4 / Mk 10:6** *(beteljesedés, ÚJ, 2026.09.02)* |
| E12 | 258 | FIGYELMEZTETES | > 🔗 ⇒ **Ján 1:5 / 2Kor 4:6** *(beteljesedés, ÚJ, 2026.09.02)* |
| E12 | 264 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: > 🔗 ↔ **Jer 4:23** *(párhuzam, ÚJ, 2026.09.04, retroaktív 2/f-audit)* |
| E12 | 268 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: > 🔗 ↔ **Ézs 34:11** *(párhuzam, ÚJ, 2026.09.04, retroaktív 2/f-audit)* |
| E12 | 272 | FIGYELMEZTETES | > **Ismétlődő motívum:** ez a lelet motívumnapló-jelölt (⭐ küszöb, 3 előfordulás) — a 'PaRDeS_motivumok.md'-be még nem került be, önálló jóváhagyást i |
| E12 | 280 | FIGYELMEZTETES | > **📚 Pontosítás (2026.09.02, LXX-alapú lexikai audit):** a ténylegesen **szó szerinti** idézet nem ez a szakasz, hanem **Zsid 4:4** ("Mert így szólot |
| E12 | 288 | FIGYELMEZTETES | > **📚 Kiegészítés (2026.09.02, LXX-alapú lexikai audit):** a LXX 1Móz 1:26 (צֶלֶם → εἰκών) és Kol 1:15 közös szava (εἰκών, G1504, mindössze 23 újszöve |
| E12 | 294 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Tehom_tematikus.md' (a *tehóm*/ábüσσος — mélység motívuma — az 1:2-ben dokumentált teremtés-előtti mélys |
| E12 | 315 | FIGYELMEZTETES | **Bibliai nyelvek** — A בָּרָא (*bará*, "teremteni") ige kizárólag Istenre alkalmazott, "semmiből" teremtő cselekvést jelöl, szemben a יָצַר (*jacar*, |
| E12 | 326 | FIGYELMEZTETES | **Nevesített tanítói szemszög** *(explicit kérésre, a bővített sablon öt lépéses módszere szerint keresve és ellenőrizve — lásd '2_PaRDeS_bovitett_sab |
| E12 | 363 | FIGYELMEZTETES | ## 7. Lexikai audit — módszertani napló (2026.09.02, oszlop-bővítve 2026.09.05, 3/b terv) |
| E12 | 375 | FIGYELMEZTETES | \| בָּרַךְ (H1288) \| ✅ \| nincs \| 330 \| nincs önálló (apró etimológiai adalék, l. 2. pont) \| nem releváns \| megerősítve \| |
| E12 | 378 | FIGYELMEZTETES | **2/f — Rögzült szópár együttes-előfordulás ellenőrzése (2026.09.04, protokoll v5):** a תֹהוּ וָבֹהוּ (H8414/H0922) szópár teljes körű ellenőrzése ('T |
| E12 | 380 | FIGYELMEZTETES | **Amit ez a módszer NEM tett meg:** a motívumnapló ('PaRDeS_motivumok.md') érintetlen maradt — sem az εἰκών/*celem*-lelet, sem a תֹהוּ וָבֹהוּ-lelet n |

### `genezis/1Moz_2v4-7_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 3 | HIBA | kiejtes nelkul: נֶפֶשׁ -- *v4 — 2026.09.03 (Pontosítás a 7. szakaszban: a נֶפֶשׁ←נָפַשׁ [H5314] |
| E13 | 6 | HIBA | kiejtes nelkul: נֶפֶשׁ -- *v3 — 2026.09.03 (Vitatott pont kiegészítve a נֶפֶשׁ [nefesh] BDB- |
| E13 | 59 | HIBA | kiejtes nelkul: נֶפֶשׁ חַיָּה -- **⚠️ Megjegyzés a héber נֶפֶשׁ (*nefes*) és a görög fordítás kapcsolatáról:** A Septuaginta a נֶפֶשׁ חַיָּה kifejezést ψ |
| E13 | 134 | HIBA | kiejtes nelkul: תוֹלְדוֹת -- **Hermeneutika** — A "toldot" (תוֹלְדוֹת) egy visszatérő szerkesztői formula a Genezisben (összesen tízszer fordul elő), |
| E13 | 164 | HIBA | kiejtes nelkul: יָצַר -- **Elutasított/triviálisnak minősített Origin-lánc-elemek:** תוֹלְדוֹת (H8435) ← H3205 "nemzeni" (triviális); יָצַר (H333 |
| E13 | 166 | HIBA | kiejtes nelkul: ψυχή -- **LXX-híd, ellenőrizve, nincs teendő:** 1Kor 15:45 ↔ G5590 (ψυχή)/G2198 (ζάω) — a Sod blokk már explicit idézi és magyar |
| E8 | 1 | HIBA | tiltott igehely-format: "1 Mózes 2:4" -- # 1 Mózes 2:4-7 — Bővített PaRDeS tanulmány |
| E12 | 3 | FIGYELMEZTETES | *v4 — 2026.09.03 (Pontosítás a 7. szakaszban: a נֶפֶשׁ←נָפַשׁ [H5314] |
| E12 | 6 | FIGYELMEZTETES | *v3 — 2026.09.03 (Vitatott pont kiegészítve a נֶפֶשׁ [nefesh] BDB- |
| E12 | 9 | FIGYELMEZTETES | *v2 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — minden szó egyértelműen 2:4-hez |
| E12 | 10 | FIGYELMEZTETES | *v1 — 2026.07.31* |
| E12 | 16 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: két korábbi tanulmány készült már 1Mózesből — 1Móz 1:1 (a teremtő szó / creatio ex nihilo témában) és 1Mó |
| E12 | 118 | FIGYELMEZTETES | **Ismétlődő motívum korábbi tanulmányodból:** a "lehelet / élet lehelete" motívum már szerepel a 'PaRDeS_motivumok.md' naplóban (1Móz 2:7 ← 1Thessz 5: |
| E12 | 168 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** a fenti adatok a 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv' és 'TAGNT_kivonat.tsv' fájlokból származnak. |

### `genezis/1Moz_2v8-25_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 3 | HIBA | kiejtes nelkul: עֲרוּמִּים -- *v4 — 2026.09.03 (Remez-pont kiegészítve az עֲרוּמִּים [2:25] / עָרוּם [3:1] |
| E13 | 6 | HIBA | kiejtes nelkul: μέσῳ -- kereszthivatkozás kiegészítve a μέσῳ [„közepette"] lexikai párhuzammal |
| E13 | 9 | HIBA | kiejtes nelkul: גַּן -- *v3 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül —  |
| E13 | 103 | HIBA | kiejtes nelkul: צֵלָע -- **⚠️ Megjegyzés a צֵלָע és az אִשָּׁה vershez rendeléséről:** mindkét szó két egymást követő versben is előfordul ebben  |
| E13 | 152 | HIBA | kiejtes nelkul: μυστήριον μέγα -- Az "egy testté" (*bászár echád*) válás nem pusztán családi-szociológiai megállapítás — Pál apostol az Efézusi levélben k |
| E13 | 164 | HIBA | kiejtes nelkul: ἐν -- > Az Éden kertjéből kitiltott **élet fája** a Jelenések könyvében, az új teremtésben tér vissza — a kezdet és a vég össz |
| E13 | 182 | HIBA | kiejtes nelkul: μυστήριον -- > Pál szó szerint idézi 1Móz 2:24-et, és kifejezetten **"nagy titoknak"** (μυστήριον) nevezi — ez a legközvetlenebb, leg |
| E13 | 220 | HIBA | kiejtes nelkul: לֹא, טוֹב, אִשָּׁה, אִישׁ, דָּבַק, אֶחָד -- A 2/a-2/e technikasor lefutott a study mind a 14 kulcsszavára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a k |
| E13 | 226 | HIBA | kiejtes nelkul: עֵץ הַחַיִּים -- \| עֵץ הַחַיִּים (H6086+H2416) \| ✅ \| H6086←H6095 "bezárni" triviális; H2416←H2421 "élni" triviális \| 329 / 498 \| nincs ön |
| E13 | 227 | HIBA | kiejtes nelkul: עֵץ הַדַּעַת טוֹב וָרָע -- \| עֵץ הַדַּעַת טוֹב וָרָע (H6086+H1847) \| ✅ \| H1847←H3045 "tudni" triviális \| 92 \| nincs önálló \| nem releváns \| megerős |
| E13 | 230 | HIBA | kiejtes nelkul: לֹא־טוֹב -- \| לֹא־טוֹב (H3808+H2896) \| ✅ \| H3808 nincs (primitív partikula); H2896←H2895 "kedvesnek lenni" triviális \| 5166 / 538 \|  |
| E13 | 231 | HIBA | kiejtes nelkul: עֵזֶר כְּנֶגְדּוֹ -- \| עֵזֶר כְּנֶגְדּוֹ (H5828+H5048) \| ✅ \| H5828←H5826 "segíteni" triviális; H5048←H5046 "közölni" triviális \| 151 / 151 \|  |
| E13 | 236 | HIBA | kiejtes nelkul: בָּשָׂר אֶחָד -- \| בָּשָׂר אֶחָד (H1320+H259) \| ✅ \| H1320←H1319 "hírt hozni" triviális; H259←H258 (szám-gyök) triviális \| 269 / 969 \| nin |
| E13 | 237 | HIBA | kiejtes nelkul: μέσῳ -- \| עֲרוּמִּים / arummím (H6174) \| ✅ \| ↔ H6175 (3:1) — Strong közös gyököt (H6191) jelez, BDB NEM erősíti meg \| 16 \| ✅ iro |
| E8 | 1 | HIBA | tiltott igehely-format: "1 Mózes 2:8" -- # 1 Mózes 2:8–25 — Bővített PaRDeS tanulmány |
| E8 | 16 | HIBA | tiltott igehely-format: "1Mózes 2:4" -- Az előző tanulmány (1Mózes 2:4-7) az ember porból való megformálását (*jacar*) és az élet leheletét (*nesamá*) tárgyalta — azt a pillanatot, |
| E8 | 59 | HIBA | tiltott igehely-format: "Gen.2.8" -- **⚠️ Megjegyzés a גַּן (gan) vershez rendeléséről:** a szó a 'TAHOT_kivonat.tsv' szerint mindkét versben előfordul — Gen.2.8-ban ("kertet ültet |
| E8 | 87 | HIBA | tiltott igehely-format: "Gen.2.20" -- **⚠️ Megjegyzés az עֵזֶר כְּנֶגְדּוֹ (ézer kenegdó) vershez rendeléséről:** ez a pontos kifejezés szó szerint megismétlődik Gen.2.20-ban is (" |
| E8 | 103 | HIBA | tiltott igehely-format: "Gen.2.21" -- **⚠️ Megjegyzés a צֵלָע és az אִשָּׁה vershez rendeléséről:** mindkét szó két egymást követő versben is előfordul ebben a szakaszban — צֵלָע ( |
| E8 | 184 | HIBA | tiltott igehely-format: "1Mózes 2:8" -- *Összegzés:* Ezek az igehelyek együtt mutatják, hogy 1Mózes 2:8-25 nem elszigetelt előtörténet: a kert és az élet fája az új teremtésben tér |
| E12 | 3 | FIGYELMEZTETES | *v4 — 2026.09.03 (Remez-pont kiegészítve az עֲרוּמִּים [2:25] / עָרוּם [3:1] |
| E12 | 9 | FIGYELMEZTETES | *v3 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a TAHOT_kivonat.tsv alapján a  |
| E12 | 10 | FIGYELMEZTETES | *v2 — 2026.07.31 (javítva: a szó szerinti tükörfordítás pótolva minden kulcsszövegnél)* |
| E12 | 59 | FIGYELMEZTETES | **⚠️ Megjegyzés a גַּן (gan) vershez rendeléséről:** a szó a 'TAHOT_kivonat.tsv' szerint mindkét versben előfordul — Gen.2.8-ban ("kertet ültetett Éde |
| E12 | 78 | FIGYELMEZTETES | **Ismétlődő motívum korábbi tanulmányodból:** az ember méltóságáról és felelősségi köréről szóló motívum ("uralom-megbízás") már szerepel a 'PaRDeS_mo |
| E12 | 87 | FIGYELMEZTETES | **⚠️ Megjegyzés az עֵזֶר כְּנֶגְדּוֹ (ézer kenegdó) vershez rendeléséről:** ez a pontos kifejezés szó szerint megismétlődik Gen.2.20-ban is ("nem talá |
| E12 | 186 | FIGYELMEZTETES | **Új motívum, amit érdemes felvenni a 'PaRDeS_motivumok.md' naplóba:** "munka mint szentélyi szolgálat (avad-sámar)" és "egy test — házasság mint Kris |
| E12 | 220 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 14 kulcsszavára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban a prózába |
| E12 | 239 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv', 'TAGNT_kivonat.tsv', 'LXX_kivonat_Genezis.tsv' |

### `genezis/1Moz_3v1-6_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 3 | HIBA | kiejtes nelkul: נָחָשׁ/נָחַשׁ -- *v6 — 2026.09.03 (Új megjegyzés a נָחָשׁ/נָחַשׁ gyök-kapcsolat helyes |
| E13 | 6 | HIBA | kiejtes nelkul: נָחָשׁ -- *v5 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a |
| E13 | 52 | HIBA | kiejtes nelkul: נָחָשׁ -- **Megjegyzés a נָחָשׁ gyök-kapcsolatáról:** a Strong-szótár a נָחָשׁ ("kígyó") főnevet a נָחַשׁ ("jósolni, varázsolni")  |
| E13 | 160 | HIBA | kiejtes nelkul: עָרוּם, תִגְּעוּ, פֶּן־תְּמֻתוּן, יֹדְעֵ -- A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban d |
| E13 | 167 | HIBA | kiejtes nelkul: פֶּן־תְּמֻתוּן -- \| פֶּן־תְּמֻתוּן (H6435+H4191) \| ✅ \| H6435←H6437 "fordulni" triviális; H4191 nincs (primitív gyök) \| 133 / 840 \| nincs ö |
| E13 | 168 | HIBA | kiejtes nelkul: יֹדְעֵי טוֹב וָרָע -- \| יֹדְעֵי טוֹב וָרָע (H3045+H2896+H7451) \| ✅ \| H3045 nincs (primitív gyök); H2896←H2895 triviális (l. '1Moz_2v8-25'); H7 |
| E8 | 1 | HIBA | tiltott igehely-format: "1 Mózes 3:1" -- # 1 Mózes 3:1-6 — Bővített PaRDeS tanulmány |
| E8 | 50 | HIBA | tiltott igehely-format: "Gen.3.1" -- **⚠️ Megjegyzés a נָחָשׁ (nachás, "kígyó") vershez rendeléséről:** a szó a 'TAHOT_kivonat.tsv' szerint háromszor fordul elő a szakaszban — Gen. |
| E12 | 3 | FIGYELMEZTETES | *v6 — 2026.09.03 (Új megjegyzés a נָחָשׁ/נָחַשׁ gyök-kapcsolat helyes |
| E12 | 6 | FIGYELMEZTETES | *v5 — 2026.08.24 (2. pont táblázata kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — a TAHOT_kivonat.tsv alapján a l |
| E12 | 7 | FIGYELMEZTETES | *v4 — 2026.08.21 (javítva: a "0. Sorozat-kontextus" pontban a kronológiailag helytelen hivatkozás — 1Móz 5 és 1Móz 10-11 mint "korábbi" előzmény — elt |
| E12 | 50 | FIGYELMEZTETES | **⚠️ Megjegyzés a נָחָשׁ (nachás, "kígyó") vershez rendeléséről:** a szó a 'TAHOT_kivonat.tsv' szerint háromszor fordul elő a szakaszban — Gen.3.1-ben |
| E12 | 112 | FIGYELMEZTETES | **Motívum-napló ellenőrzés:** a 'PaRDeS_motivumok.md' fájl jelenlegi kulcsszó-indexében egyik itt azonosított motívum sem szerepelt korábban, tehát mi |
| E12 | 160 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study kulcsszavaira. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokumentálatlan עָ |
| E12 | 164 | FIGYELMEZTETES | \| נָחָשׁ / nachás (H5175) \| ✅ \| ↔ H5172 ("jósolni") — Strong fordított irányt ad, BDB "denominative from נָחָשׁ" a helyes irányt mutatja \| 31 \| ✅ beép |
| E12 | 175 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv', 'TAGNT_kivonat.tsv'. |
| E12 | 179 | FIGYELMEZTETES | *Belső önellenőrzés: kiejtés ✓, ⚠️ + nevesített képviselők ✓, arányok ✓, kereszthivatkozás-formátum, cím, idézett szöveg és kulcsszó-zárójel ✓, Sod fe |

### `genezis/1Moz_3v7-24_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: עֵרֻמִּם -- retroaktívan: mind a 18 kulcsszó BDB-ellenőrizve. A v.7 עֵרֻמִּם |
| E13 | 10 | HIBA | kiejtes nelkul: עֵרֻמִּם -- *v2 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül —  |
| E13 | 112 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- **Megjegyzés πνεῦμα/ψυχή vonatkozásában:** ebben a szakaszban nem fordul elő sem a *pneuma*, sem a *pszükhé* megfelelője |
| E13 | 184 | HIBA | kiejtes nelkul: אָרוּר -- 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gy |
| E13 | 240 | HIBA | kiejtes nelkul: עֵינֵי -- \| עֵינֵי (H5869) \| ✅ \| nincs (valószínűleg primitív) \| 886 \| nincs önálló \| nem releváns \| megerősítve, nincs eltérés \| |
| E13 | 242 | HIBA | kiejtes nelkul: חֲגֹרֹת -- \| חֲגֹרֹת (H2290) \| ✅ \| igen → H2296 (*chágar*, "felövezni") \| 8 \| nincs önálló \| nem releváns \| triviális, megerősítve  |
| E13 | 244 | HIBA | kiejtes nelkul: אֵיבָה -- \| אֵיבָה (H342) \| ✅ \| igen → H340 (*ájav*, "ellenségeskedni") \| 5 \| nincs önálló \| nem releváns \| triviális, megerősítve |
| E13 | 245 | HIBA | kiejtes nelkul: זֶרַע -- \| זֶרַע (H2233) \| ✅ \| igen → H2232 (*zára*, "vetni") \| 229 \| nincs önálló \| nem releváns \| triviális, megerősítve \| |
| E13 | 247 | HIBA | kiejtes nelkul: עָקֵב -- \| עָקֵב (H6119) \| ✅ \| igen → H6117 (*áqáv*, "sarkon fogni, kicselezni" — a Jákób-név gyöke) \| 14 \| dokumentálva, nem tar |
| E13 | 248 | HIBA | kiejtes nelkul: עִצְּבוֹנֵךְ -- \| עִצְּבוֹנֵךְ (H6093) \| ✅ \| igen → H6087 (*ácáv*, "fájni, bánkódni") \| 3 \| nincs önálló \| nem releváns \| triviális, meg |
| E13 | 249 | HIBA | kiejtes nelkul: תְּשׁוּקָתֵךְ -- \| תְּשׁוּקָתֵךְ (H8669) \| ✅ \| nincs \| 3 \| ✅ már dokumentálva a "## 6." szakaszban (1Móz 3:16, 4:7, Én 7:11) \| nem relevá |
| E13 | 251 | HIBA | kiejtes nelkul: עָפָר -- \| עָפָר (H6083) \| ✅ \| igen → H6080 (*áfár*, "porrá lenni") \| 109 \| nincs önálló \| nem releváns \| triviális, megerősítve  |
| E13 | 253 | HIBA | kiejtes nelkul: כָּתְנוֹת -- \| כָּתְנוֹת (H3801) \| ✅ \| nincs (ismeretlen eredetű gyök) \| 29 \| nincs önálló \| nem releváns \| megerősítve, nincs eltéré |
| E13 | 254 | HIBA | kiejtes nelkul: עוֹר -- \| עוֹר (H5785) \| ✅ \| igen → H5783 (*úr*, "meztelennek lenni") \| 98 \| nincs önálló \| nem releváns \| triviális, megerősítv |
| E13 | 255 | HIBA | kiejtes nelkul: כְּרֻבִים -- \| כְּרֻבִים (H3742) \| ✅ \| nincs (bizonytalan eredetű) \| 91 \| nincs önálló \| nem releváns \| megerősítve, nincs eltérés \| |
| E13 | 256 | HIBA | kiejtes nelkul: לַהַט -- \| לַהַט (H3858) \| ✅ \| igen → H3857 (*láhat*, "lángolni") \| 1 \| nincs önálló \| nem releváns \| triviális, megerősítve \| |
| E13 | 257 | HIBA | kiejtes nelkul: הַחֶרֶב -- \| הַחֶרֶב (H2719) \| ✅ \| igen → H2717 (*chárav*, "pusztává lenni") \| 412 \| nincs önálló \| nem releváns \| triviális, meger |
| E13 | 259 | HIBA | kiejtes nelkul: עֵרֻמִּם -- **A v.7 עֵרֻמִּם Strong-szám javítása — indoklás:** a 2026.08.24-i, emberi döntésre váró tétel lezárva. Friss 'TAHOT_kiv |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 3:7" -- # 1Mózes 3:7-24 — bővített PaRDeS-tanulmány |
| E8 | 10 | HIBA | tiltott igehely-format: "Gen.2.25" -- *v2 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — minden szó egyértelműe |
| E8 | 286 | HIBA | tiltott igehely-format: "1Mózes 4:1" -- A logikus folytatás **1Mózes 4:1-16** (Kain és Ábel) lenne — ez közvetlenül folytatja a bűn "gyűrűzésének" ívét (az egyéni bűnből testvérgyi |
| E8 | 292 | HIBA | tiltott igehely-format: "Gen.3.7" -- A korábbi könnyű ellenőrzés ('genezis/Konnyu_ellenorzes_1-16_osszesito.md') eltérést talált a 2. pont táblázatában szereplő H6174 Strong-szám é |
| E8 | 294 | HIBA | tiltott igehely-format: "Gen.2.25" -- - **H6174** (עָרוֹם, *arom*) a tényleges Strong-szám **Gen.2.25**-nél — pontosan azt a szót jelöli, amit az 1Móz 2:8-25 tanulmány 2. pontja is |
| E8 | 295 | HIBA | tiltott igehely-format: "Gen.3.7" -- - **H5903** (עֵירֹם, *erom*) a tényleges Strong-szám **Gen.3.7, 3.10 és 3.11**-nél — ez egy szorosan rokon, de a maszoréta szöveg szerint **kül |
| E8 | 296 | HIBA | tiltott igehely-format: "Gen.3.1" -- - **H6175** (עָרוּם, *arum*, "ravasz") a harmadik, hasonló hangzású, de jelentésben teljesen eltérő szó — ez a kígyó jelzője Gen.3.1-ben (lásd  |
| E8 | 298 | HIBA | tiltott igehely-format: "Gen.2.25" -- A jelen tanulmány v.7-es táblázata a **H6174**-et használja — ez pontosan megegyezik a **Gen.2.25**-nél helyes Strong-számmal, de **nem** a Ge |
| E8 | 300 | HIBA | tiltott igehely-format: "Gen.3.7" -- **Emberi döntést igényel:** a 'Karoli_Strong_kivonat.tsv'-be való felvételkor a Gen.3.7-es sor Strong-száma H5903 legyen-e (a TAHOT tényleges t |
| E12 | 3 | FIGYELMEZTETES | *v3 — 2026.09.04 (Teljes lexikai audit [protokoll 2/a-2/f] elvégezve, |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: retroaktívan: mind a 18 kulcsszó BDB-ellenőrizve. A v.7 עֵרֻמִּם |
| E12 | 5 | FIGYELMEZTETES | Strong-számának 2026.08.24 óta nyitott kérdése LEZÁRVA — a felhasználó |
| E12 | 10 | FIGYELMEZTETES | *v2 — 2026.08.24 (2. pont táblázatai kiegészítve pontos vers-hozzárendeléssel [Vers oszlop], tartalmi változás nélkül — minden szó egyértelműen versre |
| E12 | 11 | FIGYELMEZTETES | *v1 — 2026.07.31* |
| E12 | 51 | FIGYELMEZTETES | \| 3:7 \| עֵרֻמִּם \| erumím \| H5903 (*erom*) \| mezítelenek — javítva 2026.09.04-én, l. "## 7." szakasz \| |
| E12 | 184 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gyűrűzése — átok, föld és romlás |
| E12 | 229 | FIGYELMEZTETES | *Ez a kiegészítés készen áll egy jövőbeli, önálló „pneuma/pszükhé megkülönböztetés" tematikus tanulmány (4_PaRDeS_tematikus_sablon.md szerint) Alkalma |
| E12 | 233 | FIGYELMEZTETES | ## 7. Lexikai audit — módszertani napló (2026.09.04, oszlop-bővítve 2026.09.05, 3/b terv) |
| E12 | 235 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *Ez a szakasz nem PaRDeS-tartalom, hanem a retroaktív 2/a-2/f technikasor átlátható dokumentálása.* |
| E12 | 259 | FIGYELMEZTETES | **A v.7 עֵרֻמִּם Strong-szám javítása — indoklás:** a 2026.08.24-i, emberi döntésre váró tétel lezárva. Friss 'TAHOT_kivonat.tsv'-ellenőrzés megerősít |
| E12 | 261 | FIGYELMEZTETES | **Amit ez a módszer NEM tett meg:** a motívumnapló ('PaRDeS_motivumok.md') érintetlen maradt, ez külön, hátralévő lépés. |
| E12 | 273 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Önellenőrzés |
| E12 | 278 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Kiegészítés (2026.08.01) |
| E12 | 280 | FIGYELMEZTETES | A Hós 6:7-tel kapcsolatos, "szövetség Ádámmal" vitatott kérdés — kiegészítő igehelyekkel (Jób 31:33, Zsolt 82:7, Hós 8:1, Róm 5:12-14) — bekerült a fe |
| E12 | 284 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Következő lépés a sorozatban |
| E12 | 290 | FIGYELMEZTETES | ## ⚠️ Megjegyzés — a v.7 עֵרֻמִּם (arummim) Strong-számának pontosítása (2026.08.24, MEGOLDVA 2026.09.04-én — l. "## 7." szakasz) |
| E12 | 292 | FIGYELMEZTETES | A korábbi könnyű ellenőrzés ('genezis/Konnyu_ellenorzes_1-16_osszesito.md') eltérést talált a 2. pont táblázatában szereplő H6174 Strong-szám és a 'TA |
| E12 | 300 | FIGYELMEZTETES | **Emberi döntést igényel:** a 'Karoli_Strong_kivonat.tsv'-be való felvételkor a Gen.3.7-es sor Strong-száma H5903 legyen-e (a TAHOT tényleges tagje sz |

### `genezis/1Moz_4v1-24_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 65 | HIBA | kiejtes nelkul: נוֹד -- \| 4:12 \| נָע וָנָד \| *ná vánád* \| H5128/H5110 \| „bujdosó és kóborló" — igepár, gyök szerint rokon a „Nód" (נוֹד) helynév |
| E13 | 89 | HIBA | kiejtes nelkul: רֹבֵץ -- - A „bűn az ajtó előtt leselkedik" (רֹבֵץ) kép egy ragadozó állat lapulására utaló szó — ugyanez a mintázat (a fenyegeté |
| E13 | 150 | HIBA | kiejtes nelkul: חַטָּאת -- 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gy |
| E13 | 206 | HIBA | kiejtes nelkul: Ἅβελ -- **LXX-híd, ellenőrizve, nincs teendő:** a jelzett görög szavak (Ἅβελ G0006, Κάϊν G2535, δῶρον G1435, προσφέρω G4374, θυσ |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 4:1" -- # 1Mózes 4:1-24 — bővített PaRDeS tanulmány |
| E8 | 228 | HIBA | tiltott igehely-format: "1Mózes 4:2" -- A 'PaRDeS_motivumok.md' „Feldolgozott igeszakaszok" táblázata szerint a sorozat logikus következő lépése **1Mózes 4:25 – 5:32** (Séth vonala |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 150 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gyűrűzése — átok, föld és romlás |
| E12 | 152 | FIGYELMEZTETES | **A tanulmány után frissítendő 'PaRDeS_motivumok.md' bejegyzések:** lásd a fejezet végén mellékelt, frissített motívum-napló kivonatot. |
| E12 | 210 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** a fenti adatok a 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv' és 'TAGNT_kivonat.tsv' fájlokból származnak. |
| E12 | 214 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Terminológiai és formai önellenőrzés |
| E12 | 226 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Javasolt következő igeszakasz |
| E12 | 228 | FIGYELMEZTETES | A 'PaRDeS_motivumok.md' „Feldolgozott igeszakaszok" táblázata szerint a sorozat logikus következő lépése **1Mózes 4:25 – 5:32** (Séth vonala, a Sétita |

### `genezis/1Moz_4v25-5v32_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 5 | HIBA | kiejtes nelkul: צֶלֶם/דְּמוּת -- ellenőrizve, Origin-lánc követve. Új 2/f-lelet: a צֶלֶם/דְּמוּת szópár |
| E13 | 82 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- **Megjegyzés a πνεῦμα/ψυχή-párhuzamhoz:** ebben a szakaszban a *ruach* (szellem) vagy *nefes* (lélek) szavak nem forduln |
| E13 | 197 | HIBA | kiejtes nelkul: תּוֹלְדֹת -- \| תּוֹלְדֹת (H8435) \| ✅ \| igen → H3205 (*jálad*, "szülni") \| 39 \| nincs önálló \| nem releváns \| triviális, megerősítve \| |
| E13 | 198 | HIBA | kiejtes nelkul: דְּמוּת -- \| דְּמוּת (H1823) \| ✅ \| igen → H1819 (*dámáh*, "hasonlítani") \| 25 \| ✅ 2/f lelet, l. lent \| nem releváns \| triviális, me |
| E13 | 199 | HIBA | kiejtes nelkul: צֶלֶם -- \| צֶלֶם (H6754) \| ✅ \| nincs (bizonytalan eredetű) \| 17 \| ✅ 2/f lelet, l. lent \| nem releváns \| megerősítve \| |
| E13 | 202 | HIBA | kiejtes nelkul: נֹחַ / יְנַחֲמֵנוּ -- \| נֹחַ / יְנַחֲמֵנוּ (H5146+H5162) \| ✅ \| H5146 ← H5118 ("nyugalom") — BDB az 5:29 névmagyarázatot "hagyományos etimológi |
| E13 | 204 | HIBA | kiejtes nelkul: צֶלֶם -- **2/f — Rögzült szópár együttes-előfordulás ellenőrzése:** a צֶלֶם (H6754) és דְּמוּת (H1823) szavak teljes körű ellenőr |
| E8 | 1 | HIBA | tiltott igehely-format: "1Mózes 4:2" -- # 1Mózes 4:25–5:32 — Séth nemzetségtáblája |
| E12 | 3 | FIGYELMEZTETES | *Bővített PaRDeS-tanulmány — v2, 2026.09.04 (Teljes lexikai audit |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: [protokoll 2/a-2/f] elvégezve, retroaktívan: mind a 7 kulcsszó BDB- |
| E12 | 190 | FIGYELMEZTETES | ## 7. Lexikai audit — módszertani napló (2026.09.04, oszlop-bővítve 2026.09.05, 3/b terv) |
| E12 | 192 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *Ez a szakasz nem PaRDeS-tartalom, hanem a retroaktív 2/a-2/f technikasor átlátható dokumentálása.* |
| E12 | 204 | FIGYELMEZTETES | **2/f — Rögzült szópár együttes-előfordulás ellenőrzése:** a צֶלֶם (H6754) és דְּמוּת (H1823) szavak teljes körű ellenőrzése ('TAHOT_kivonat.tsv') meg |
| E12 | 206 | FIGYELMEZTETES | **Amit ez a módszer NEM tett meg:** a motívumnapló ('PaRDeS_motivumok.md') érintetlen maradt — sem a celem/demut, sem a többi jelen study-beli motívum |
| E12 | 210 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés |
| E12 | 223 | FIGYELMEZTETES | *A motívum-napló ('PaRDeS_motivumok.md') frissítése az alábbi új/ismétlődő motívumokkal indokolt — lásd a következő üzenetben a v13 frissítést:* |
| E12 | 234 | FIGYELMEZTETES | **Kapcsolódó tematikus tanulmány:** 📎 Bővebben, önálló tematikus feldolgozásban: 'Segitsegul_hivni_az_Urat_tematikus.md' (Segítségül hívni az Úr nevét |

### `genezis/1Moz_6v1-8_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 5 | HIBA | kiejtes nelkul: עצ״ב -- lexikai kapcsolatokat [jetzer/jacar, עצ״ב-lánc]; a study megfogalmazása |
| E13 | 98 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 112 | HIBA | kiejtes nelkul: יצ״ר -- A יֵצֶר (*jetzer*, "hajlam/formálás") szó ugyanabból a יצ״ר gyökből származik, mint a 2:7-ben használt וַיִּיצֶר (*vajji |
| E13 | 116 | HIBA | kiejtes nelkul: חֵן -- A szöveg tanítása kettős. Egyfelől az emberi szív romlottsága nem elszigetelt eset (mint Kainnál), hanem egyetemes állap |
| E13 | 120 | HIBA | kiejtes nelkul: וַיִּתְעַצֵּב -- A Peshat/Remez rétegekből ténylegesen levezethető mélység: Isten "bánkódása" (וַיִּתְעַצֵּב) ugyanazzal a szógyökkel fej |
| E13 | 139 | HIBA | kiejtes nelkul: יצ״ר -- > 🔗 **1Móz 2:7** — „...és **formálta** (וַיִּיצֶר, *vajjitzer* — kulcsszó: formálás, ugyanaz a יצ״ר gyök, mint a *jetzer |
| E13 | 145 | HIBA | kiejtes nelkul: עצ״ב -- > 🔗 **1Móz 3:17** — „...átkozott legyen a föld te miattad, **fáradságos munkával** (בְּעִצָּבוֹן, *be'itzavon* — kulcssz |
| E13 | 147 | HIBA | kiejtes nelkul: וַיִּתְעַצֵּב -- *Miért kapcsolódik:* Isten "bánkódása" (6:6, וַיִּתְעַצֵּב) szó szerint ugyanazt a gyököt használja, amellyel Ő maga súj |
| E13 | 163 | HIBA | kiejtes nelkul: רַע -- 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gy |
| E13 | 212 | HIBA | kiejtes nelkul: נִחַם, עָצַב, מָחָה -- A 2/a-2/e technikasor lefutott a study mind a 11 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta  |
| E13 | 216 | HIBA | kiejtes nelkul: בְּנֵי־הָאֱלֹהִים -- \| בְּנֵי־הָאֱלֹהִים (H1121+H430) \| ✅ \| H1121←H1129 "építeni" triviális; H430 korábbi studyban (1v1) lezárva \| 4941 / 260 |
| E13 | 217 | HIBA | kiejtes nelkul: בְּנוֹת הָאָדָם -- \| בְּנוֹת הָאָדָם (H1323+H120) \| ✅ \| H1323←H1129 triviális; H120←H119 (adam/adamah, korábban lezárva) \| 588 / 551 \| ninc |
| E13 | 234 | HIBA | kiejtes nelkul: יצ״ר -- - „jetzer — a szív romlott hajlama" — új motívum, rokon a por/formáltatás gyökkel (יצ״ר), de új szemantikai mezőben |
| E13 | 235 | HIBA | kiejtes nelkul: עצ״ב -- - „Isten fájdalma (עצ״ב) — a kimondott átok visszhangja Istenben" — új Sod-motívum, 3:16-17 ↔ 6:6 |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 163 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gyűrűzése — átok, föld és romlás |
| E12 | 165 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Isten_fiai_Nefilim_Gibborim_tematikus.md' ("Isten fiai — Nefilim — Gibborim" motívum-komplexum — a 6:2/6 |
| E12 | 199 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 212 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 11 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a נִחַם, עָצַב, מ |
| E12 | 228 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv'. |
| E12 | 239 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben, vagy ha előbb finomítanál valamit a tanulmányon. |

### `genezis/1Moz_6v9-22_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: מַבּוּל -- nincs új tartalmi lelet; a מַבּוּל-etimológia [יבל] BDB által explicit |
| E13 | 126 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 128 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- A 17. v. נֶפֶשׁ חַיָּה (*nefesh chajjá*, „élő lélek") kifejezés — amelyet a Károli itt „élő lélek"-nek fordít — ugyanaz  |
| E13 | 152 | HIBA | kiejtes nelkul: עֲצֵי־גֹפֶר -- **A "gófer-fa" azonosítása** — az עֲצֵי־גֹפֶר kifejezés a Szentírásban kizárólag itt fordul elő (hapax legomenon), így p |
| E13 | 186 | HIBA | kiejtes nelkul: שָׁחַת -- 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gy |
| E13 | 192 | HIBA | kiejtes nelkul: תָּמִים -- **Rabbinikus hang:** a תָּמִים... בְּדֹרֹתָיו ("feddhetetlen... nemzedékei között") kifejezés klasszikus vitát váltott k |
| E13 | 221 | HIBA | kiejtes nelkul: שָׁחַת, תֵּבָה, עֲצֵי־גֹפֶר -- A 2/a-2/e technikasor lefutott a study mind a 10 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta  |
| E13 | 232 | HIBA | kiejtes nelkul: יבל -- \| מַבּוּל / mabbúl (H3999) \| ✅ \| ← יבל BDB "derivation dubious... but improbable" \| 13 \| nincs önálló \| nem releváns \| e |
| E13 | 233 | HIBA | kiejtes nelkul: נֶפֶשׁ חַיָּה -- \| נֶפֶשׁ חַיָּה (H5315+H2416) \| ✅ \| már részletesen tárgyalva '1Moz_2v4-7' és '1Moz_6v1-8' 7. szakaszában \| 753 / 498 \|  |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 186 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Bun_kovetkezmenyeinek_gyuruzese_tematikus.md' ("A bűn következményeinek gyűrűzése — átok, föld és romlás |
| E12 | 221 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 10 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokume |
| E12 | 236 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv'. |
| E12 | 240 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 257 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben (v15). |

### `genezis/1Moz_7v1-24_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 142 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 186 | HIBA | kiejtes nelkul: רוּחַ -- *Miért kapcsolódik:* a BDB szócikk (H5397) saját maga veti össze a két igehelyet: a 2:7-es *nismat chajjím* ("élet lehel |
| E13 | 204 | HIBA | kiejtes nelkul: שאר -- *Miért kapcsolódik:* Noé — "csak Noé marada meg" (23. v.) — a Szentírás első, névvel jelölt megmaradó maradéka; irányjel |
| E13 | 214 | HIBA | kiejtes nelkul: בְּעֶצֶם הַיּוֹם הַזֶּה -- **Rabbinikus hang:** a Bereseit Rabbá (32-33) klasszikus hagyománya szerint a hét napos haladék (4, 10. v.) Metusélah gy |
| E13 | 249 | HIBA | kiejtes nelkul: אֲרֻבֹּת הַשָּׁמַיִם -- \| אֲרֻבֹּת הַשָּׁמַיִם (H0699+H8064) \| ✅ \| H0699 ← H0693 ("leselkedni") — triviális \| H0699: 9 / H8064: 420 \| nincs önál |
| E13 | 251 | HIBA | kiejtes nelkul: נִשְׁמַת רוּחַ חַיִּים -- \| נִשְׁמַת רוּחַ חַיִּים (H5397+H7307+H2416) \| ✅ \| mind triviális: H5397←H5395 ("zihálni"), H7307←H7306 ("szagolni"), H2 |
| E13 | 252 | HIBA | kiejtes nelkul: וַיִּשָּׁאֶר אַךְ -- \| וַיִּשָּׁאֶר אַךְ (H7604+H0389) \| ✅ \| H0389 ← H0403 ("bizonyára") — triviális \| H7604: 133 / H0389: 161 \| ✅ dokumentál |
| E13 | 267 | HIBA | kiejtes nelkul: λείπω -- - ✅ Sod fegyelem: a maradék-elv (Róm 9:27) kapcsolat gyök-szintű lexikai adatokkal (héber שאר, görög λείπω) alátámasztva |
| E13 | 274 | HIBA | kiejtes nelkul: שאר -- - „maradék-elv (she'erit)" — új motívum, első bibliai előfordulás (7:23 ↔ Róm 9:27), gyök-szintű lexikai alátámasztás: h |
| E12 | 3 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *v3 — 2026.09.03 (Retroaktív „7. Lexikai audit — módszertani napló" |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: szakasz felvéve, a v16 sablon kötelező elemének visszamenőleges |
| E12 | 5 | FIGYELMEZTETES | pótlása — a 2026.09.03-i eredeti audit eredményének formalizálása, új |
| E12 | 7 | FIGYELMEZTETES | *v2 — 2026.09.03 (Róm 9:27 gyök-szintű lexikai alátámasztás hozzáadva; új Remez-pont: nismat chajjím [2:7] ↔ nismat rúach chajjím [7:22] dekreáció-pár |
| E12 | 208 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Tehom_tematikus.md' (a *tehóm*/ábüσσος — mélység motívuma — a 7:11-ben dokumentált dekreációt a teljes g |
| E12 | 243 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 6 kulcsszó-sorára (2. pont táblázatai: táhór, tehóm, arubbot hasámájim, szágár, nismat rúac |
| E12 | 254 | FIGYELMEZTETES | **Elutasított leletek:** a Róm 9:27 kereszthivatkozás Strong-szám-szinten üres metszetet ad (a kockázat-riport ezt piros zászlóként jelezte) — ez NEM  |
| E12 | 256 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** a fenti adatok a 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv', 'TAHOT_kivonat.tsv', 'TAGNT_kivonat.tsv' és 'LXX_k |
| E12 | 260 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 278 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben (v16). |

### `genezis/1Moz_8v1-22_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 3 | HIBA | kiejtes nelkul: נוח -- *v2 — 2026.09.03 (Sod-pont kiegészítve a נוח gyök-hármas lelettel — Noé |
| E13 | 4 | HIBA | kiejtes nelkul: מָנוֹחַ -- neve, a galamb מָנוֹחַ-a és a נִיחֹחַ [kedves illat, 21. v.] mind ugyanabból |
| E13 | 122 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 146 | HIBA | kiejtes nelkul: נוח -- Ez a gyök-mintázat a fejezet zárómondatában is folytatódik: amikor Isten "megérzi a kedves illatot" (רֵיחַ הַנִּיחֹחַ, * |
| E13 | 150 | HIBA | kiejtes nelkul: אֲרָרָט -- **Az Ararát-hegy azonosítása** — a héber „Ararát" (אֲרָרָט) az ókori Urartu királyság térségére utal, amely a mai Örmény |
| E13 | 231 | HIBA | kiejtes nelkul: פָּרוּ וְרָבוּ -- A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a |
| E13 | 237 | HIBA | kiejtes nelkul: עֲלֵה־זַיִת -- \| עֲלֵה־זַיִת (H5929+H2132) \| ✅ \| H5929 ← "felemelkedni" triviális; H2132 ← H2099 nem ad új tartalmat \| 18 / 38 \| nincs  |
| E13 | 238 | HIBA | kiejtes nelkul: פָּרוּ וְרָבוּ -- \| פָּרוּ וְרָבוּ (H6509+H7235) \| ✅ \| mindkettő primitív gyök, nincs lánc \| 29 / 226 \| ✅ visszhangozza az 1:22/1:28 áldás |
| E13 | 240 | HIBA | kiejtes nelkul: רֵיחַ הַנִּיחֹחַ -- \| רֵיחַ הַנִּיחֹחַ (H7381+H5207) \| ✅ \| H5207 ← H5117 (*nuach*, "pihenni") — Noé nevével (נֹחַ) és a study saját *manoach |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Sod-pont kiegészítve a נוח gyök-hármas lelettel — Noé |
| E12 | 196 | FIGYELMEZTETES | 📎 Bővebben, önálló tematikus feldolgozásban: 'Tehom_tematikus.md' (a *tehóm*/ábüσσος — mélység motívuma — a 8:2-ben dokumentált helyreállítást a telje |
| E12 | 231 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokumen |
| E12 | 243 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv'. |
| E12 | 247 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 271 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben (v17). |

### `genezis/1Moz_9v1-17_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 4 | HIBA | kiejtes nelkul: קֶשֶׁת, עוֹלָם -- nincs új tartalmi lelet; két ígéretes etimológia [קֶשֶׁת, עוֹלָם] |
| E13 | 98 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 112 | HIBA | kiejtes nelkul: זָכַרְתִּי -- A קֶשֶׁת (*kesét*) szó a Szentírásban elsődlegesen "hadi íjat" (fegyvert) jelent, nem "szivárványt" — a kép mögött valós |
| E13 | 197 | HIBA | kiejtes nelkul: צֶלֶם -- A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a |
| E13 | 207 | HIBA | kiejtes nelkul: עלם -- \| עוֹלָם / olám (H5769) \| ✅ \| ← עלם "elrejteni" — Strong-only, BDB nem ad explicit gyök-jelölést, elutasítva \| 437 \| nin |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.03 (Új, kötelező 7. szakasz — Lexikai audit — felvéve; |
| E12 | 197 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: A 2/a-2/e technikasor lefutott a study mind a 7 kulcsszó-sorára. 2026.09.05-i retroaktív ellenőrzés (3/b terv) lezárta a korábban dokumen |
| E12 | 209 | FIGYELMEZTETES | **Forrás-hivatkozási fegyelem:** 'Strong_szotar.tsv', 'BDB_teljes_unabridged.tsv'. |
| E12 | 213 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 234 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben (v18). |

### `genezis/1Moz_9v18-29_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 78 | HIBA | kiejtes nelkul: πνεῦμα/ψυχή -- ### Megjegyzés a πνεῦμα/ψυχή-párhuzamról |
| E13 | 92 | HIBA | kiejtes nelkul: יֶפֶת -- Noé "a föld embere" (*is há'adámá*) kifejezés visszautal Ádámra, akit a föld porából (*adámá*) formáltak (2:7) — Noé egy |
| E13 | 108 | HIBA | kiejtes nelkul: עֶרְוַת אָבִיו רָאָה -- **Khám vétkének pontos természete — lexikai alapú kiegészítés (ÚJ, 2026.09.04, retroaktív lexikai audit).** A fenti (5.  |
| E13 | 178 | HIBA | kiejtes nelkul: אִישׁ הָאֲדָמָה -- \| אִישׁ הָאֲדָמָה (H376+H127) \| ✅ \| H127 ← H119 (bizonytalan, vitatott levezetés) \| 1663 / 225 \| nincs önálló \| nem rele |
| E13 | 180 | HIBA | kiejtes nelkul: עֶרְוָה -- \| עֶרְוָה (H6172) \| ✅ \| igen → H6168 (*áráh*, "lemeztelenít") \| 54 \| ✅ új ⚠️ vitatott pont a "## 3." szakaszban \| nem re |
| E13 | 182 | HIBA | kiejtes nelkul: אֱלֹהֵי שֵׁם -- \| אֱלֹהֵי שֵׁם (H430+H8035) \| ✅ \| nincs \| 2603 / 17 \| nincs önálló \| nem releváns \| megerősítve, nincs eltérés \| |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.09.04 (Teljes lexikai audit [protokoll 2/a-2/f] elvégezve, |
| E12 | 4 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: retroaktívan: mind a 6 kulcsszó BDB-ellenőrizve. Új ⚠️ vitatott pont |
| E12 | 108 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: **Khám vétkének pontos természete — lexikai alapú kiegészítés (ÚJ, 2026.09.04, retroaktív lexikai audit).** A fenti (5. pontban idézett)  |
| E12 | 172 | FIGYELMEZTETES | ## 7. Lexikai audit — módszertani napló (2026.09.04, oszlop-bővítve 2026.09.05, 3/b terv) |
| E12 | 174 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: *Ez a szakasz nem PaRDeS-tartalom, hanem a retroaktív 2/a-2/f technikasor átlátható dokumentálása.* |
| E12 | 185 | FIGYELMEZTETES | **Amit ez a módszer NEM tett meg:** a motívumnapló ('PaRDeS_motivumok.md') érintetlen maradt, ez külön, hátralévő lépés. |
| E12 | 189 | FIGYELMEZTETES | naplojellegu szoveg 【NAPLO】 blokkon kivul: ## Formai önellenőrzés (elvégezve) |
| E12 | 208 | FIGYELMEZTETES | Szólj, ha ezeket rögzítsem a 'PaRDeS_motivumok.md'-ben (v19). |
| E12 | 212 | FIGYELMEZTETES | **Lezárt kérdés:** a Derek Prince-integráció (6:1-8-hoz) megtörtént — lásd '1Moz_6v1-8_bovitett.md', Alkalmazás 4. pont. A Noé-*toledot* ezzel a szaka |

### `ujszovetseg/1Thessz_5v23_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E12 | 3 | FIGYELMEZTETES | *v1 — 2026.07.28* |
| E12 | 8 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: ez az első tanulmány 1Thesszalonikából — nincs korábbi tanulmány ugyanabból a könyvből, ezért ez a pont k |

### `ujszovetseg/Rom_8v10_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 48 | HIBA | kiejtes nelkul: ζωή -- **⚠️ Megjegyzés a πνεῦμα (*pneuma*) fordításáról:** A Károli itt "lélek"-nek fordítja a πνεῦμα szót, holott a görög nem  |
| E13 | 63 | HIBA | kiejtes nelkul: πνεῦμα -- ⚠️ **Vitatott pont:** a πνεῦμα (8:10) az ember saját szellemére vagy a bennük lakó Szent Szellemre utal-e? |
| E13 | 65 | HIBA | kiejtes nelkul: πνεῦμα -- - **Gordon Fee** (*God's Empowering Presence*, pünkösdi/Assemblies of God hátterű) erőteljesen a Szent Szellem olvasata  |
| E12 | 3 | FIGYELMEZTETES | *v2 — 2026.07.30 (Alkalmazás pont Derek Prince tanítása alapján)* |
| E12 | 8 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: eddig nem készült önálló tanulmány a Rómaiakhoz írt levélből (csak keresztutalásként szerepelt Róm 8:23 é |
| E12 | 105 | FIGYELMEZTETES | **Ismétlődő motívum korábbi tanulmányodból:** a "test mint a megváltás tárgya" motívum már szerepel a 'PaRDeS_motivumok.md' naplóban (Róm 8:23; 1Kor 1 |
| E12 | 144 | FIGYELMEZTETES | *v2 — 2026.07.30: az Alkalmazás és tanítványság pont kibővítve és forrásolva Derek Prince tanítása alapján.* |

### `ujszovetseg/Zsid_4v12_bovitett.md`

| Szabály | Sor | Szint módosításnál | Részlet |
|---|---|---|---|
| E13 | 20 | HIBA | kiejtes nelkul: κατάπαυσις -- 📖 **Irodalmi kontextus** A 3:7–4:11 szakasz a pusztai nemzedék hitetlenségét állítja példaként a "nyugalomba" (κατάπαυσι |
| E13 | 116 | HIBA | kiejtes nelkul: μερισμός -- A Talmud (Sabbat 88b) egy hagyománya szerint Isten hangja a Sínai-hegyen kimondáskor hetven nyelvre "hasadt szét" — ez a |
| E13 | 130 | HIBA | kiejtes nelkul: ἁρμῶν καὶ μυελῶν -- **Történelmi és kulturális kontextus** *(konkrét, célzott)* — Az "ízületek és velők" (ἁρμῶν καὶ μυελῶν) kifejezés a levi |
| E12 | 3 | FIGYELMEZTETES | *v1 — 2026.07.28* |
| E12 | 8 | FIGYELMEZTETES | *Ellenőrzés a 'PaRDeS_motivumok.md' alapján: ez az első tanulmány a Zsidókhoz írt levélből — nincs korábbi tanulmány ugyanabból a könyvből, ezért ez a |
| E12 | 51 | FIGYELMEZTETES | **Ismétlődő motívum korábbi tanulmányodból:** a *pneuma*/*pszükhé* megkülönböztetés motívuma már szerepel a 'PaRDeS_motivumok.md' naplóban, az 1Thessz |
| E12 | 148 | FIGYELMEZTETES | *v2 — 2026.07.28: kiegészítve Jel 1:16 második Remez-kereszthivatkozással (δίστομος szómegfelelés).* |
| E12 | 149 | FIGYELMEZTETES | *v3 — 2026.07.30: az Alkalmazás és tanítványság pont kibővítve és forrásolva Derek Prince tanítása alapján.* |
