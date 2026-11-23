# F231 — az olvasó egyben: jelentés (2026-11-22)

- **Feladat:** `F231_SZOKARTYA_EGYSEGES_BRIEF.md` (0. szakasz: a hatókör a `naplok/OLVASO_EGYBEN_HIBALISTA.md` 60 sora, a 23. és az 59. sor kivételével).
- **Modell:** a brief `opus`; a végrehajtó session `claude-opus-5-5` (egyezik).
- **Ág:** `claude/olvaso-egyben-3464e1`; a main a F235 (#799) után behozva (`f8a6844f`).
- **Független ellenőrzés: elmarad, DT-F0a gyors sáv** (DT919: a diff a brief fejlécén, ezen a jelentésen és a `naplok/` fájljain túl csak az `eszkozok/olvaso_szerver/` alatti fájlokat érinti).
- **Élő ellenőrzés:** az ágas előnézet (8775, a worktree-ből) a main állapotán („előtte”: 34 mintalap) és a javítás után („utána”). A pillanatkép a F232 normalizálójával készült (`teszt_olvasoi_merce.pillanatkep`; a rejtett fülek tartalmával is). A képek és a szkriptek: a jegyzetmappa `olvaso-egyben-elokeszites/` almappája.

## 1. Döntések

Orkesztrátori döntések (a felhasználó felhatalmazásával, 2026-11-22):

- **DT-F231a: (b).** A lapgen kártyája motívum nélkül, egy Strong-számra API-változás nélkül nem hívható: a teljes bemeneti tárat igényli, a nem hordozó szakaszt első tagmondatra csukja, és több ágon `JeloltHiba`-val megáll. Az olvasó ezért ugyanezt a modellt a saját adatából építi: a jelentések rendje a közös `szotari_glossza`-val, alatta szakaszonként a szöveg egyben, az eredeti szórendben. Az egyezést a HAMART-001 4.2-vel teszt őrzi (`teszt_szokartya_egyseges.EgyezesALexikonlappal`, a gyors tesztek között).
- **#24** (görög glosszák fordítása): kimarad, költségdöntés, a felhasználó hatásköre (N177 marad).
- **#51:** „Biblialex olvasó”, egyetlen kulcsból (`konfig/feliratok.tsv` `olvaso.nev`; DT899).
- **#45/#46:** a jelleg-címkék és a forrássor csukott „Forrás és licenc” lenyílóban, olvasói forrásnévvel; a belső táblanév csak a súgóban.
- **A határ:** ami csak adattal vagy generátorral javítható, az „rád vár” (3. szakasz).

Technikai döntések (DT920, a session dönt):

- **A fordítótábla (DT897):** `eszkozok/olvaso_szerver/konfig/feliratok.tsv` (`kulcs`, `hu`, `en`; üres angolnál a magyar áll), a betöltő a `feliratok.py` (`F(kulcs, **param)`, ismeretlen kulcsnál kimondott hiba; `Fv(kulcs, alap)` a szabad nevű konfigurációs értékekhez). A sablonok is ezt hívják (jinja globális). A kapu: `teszt_szokartya_egyseges.Forditotabla`.
- **Tagolási jelző (#11):** rossz a tagolás, ha egy *számozott* pont vagy alpont meghatározás nélkül alaktani felsorolással nyílik (H3615 Qal 1.a „1. egyes szám …”). Ilyenkor a törzs egyben áll, a pontok jelével. A törzs elején álló, jel nélküli alaktani pont nem hiba: ez a törzs „Alakok” sora (H2398 Qal „perfectum …”). A „status constructus” és a „suffixummal” nem jelző, mert a BDB névszóknál jelentéspontot nyit vele (H0430 4.b).
- **A rövidítőjel szabálya (#8):** R0–R3 (`szokartya_szoveg.geresh_javit`). A szavak sorrendje nem változik, csak a ׳ helye. A Biblia által igazolt sorrend-javítás (`bdb_rovidites.heber_sorrend_javit`) *előtte* fut, mert a forrás alakját keresi (menet közben talált hiba, l. 4. szakasz).
- **A szakasztábla hiányossága (#12):** ahol a tagolt kártya a nyers magyar szócikk 4+ betűs szavainak kevesebb mint 85%-át adja vissza, a „teljes szöveg” nyitva áll, és a kártya ezt kimondja; különben csukva marad, biztosítékként.
- **A motívum jelentése (DT914):** csak biztos besorolású helyről. A kétes pont nem hordozó; ez a lexikonlap 4.2 félkövérjével azonos, az egyezési teszt fogta meg.
- **A két új Thayer-lekérdezés** a meglévő, a tervőrben nyilvántartott függvények paramétere (`thayer_szakasz_sorok(szoveggel=True)`, `thayer_vers_pontok(karoli_vers=None)`). Ugyanaz a tábla, és ugyanaz a hiányzó `strong`-index (F235 2. rész); az `ELFOGADOTT` lista nem nőtt.

## 2. Mérések

| Mérés | Eredmény | Forrás |
|---|---|---|
| Tagolási jelző, BDB (#11) | 8 090 magyar szócikk · 5 129 számozott pontú törzs · **230 törzs (194 szócikk) egyben** · 2 578 jel nélküli alaktani pont „Alakok” sorként | a jegyzetmappa `meres.py`-ja, a `pardes.db`-n |
| Tagolási jelző, Thayer | 2 921 magyar szakasz, ebből 8 alaktani nyitású; a Thayer-kártya ezért nem bont törzsre, a szakaszok egyben állnak | uo. |
| Lefedettség (#12) | 8 088 szócikk; a nyers magyar szövegből a kártyán átlag **91,7%**; 85% alatt 1 073 szócikk (itt a teljes szöveg nyitva). Ok: a szakasztábla egyes szakaszok szövegét nem adja vissza (pl. H1709 második szócikkének alakjai) | uo. |
| BDB hivatkozás-javítás (#19) | **412 / 412** alkalmazva, 0 kihagyva (247 Strong) | `hiv.py` |
| LXX-párok igazolhatósága (#14, integrátori kérés) | a Macula 323 263 H→G párjából **44 225-nél (13,7%)** nem fordul elő a görög Strong az LXX_OS adott versében; 190 Strong egyszer sem. A többség legitim pár más Strong-konvencióval (σου G4675 / LXX_OS G4771: 4 355; μου G3450: 3 507; εἶπεν G2036: 2 235; ισραηλ G2474: 2 284). Az elrejtés vagy a „nem igazolt” jelölés legitim párokat is érintene, ezért **nincs bevezetve**; a valódi hiba (πρωὶ → G5459) az N-F231a | `lxxpar.py` |
| Görög iota-átírás (#34) | **1 471 token** (pl. τῇ „tēa”, ἀρχῇ „archēa”) | `iota.py` |
| Szócsoport tartalék szabálya (#30) | a teljes Ószövetségen a versek **2,77%-ában** tér el a Maculától (a JOHD-mintán 0). A csempe a Macula-azonosítót használja, ahol van; a tartalék csak Macula-sor híján lép be | `teszt_szokartya_egyseges.Szocsoport` |
| A F232 mérce frissítése | 18 fájl, minden megváltozott sor egy hibalista-tételhez rendelve, besorolatlan sor: 0 | `naplok/F231_merce_indoklas.md` |

## 3. A tételek (60 sor)

Kimenet (három kimenet, IRANY.md „Így dolgozunk”; a K a megbízáson kívüli két sor): **J** = javítva · **V** = már javult vagy nem hiba (elvetve, egy sor indokkal) · **R** = rád vár (IRANY.md „Rád vár”; az integrátor vezeti át) · **K** = kimarad a megbízás szerint. Az „előtte” a main (`24e1d2bd`), az „utána” az ág élő lapja.

| # | Kimenet | URL | Előtte (látott) | Utána (látott) |
|---|---|---|---|---|
| 1 | J | /szo/H0430 | „7 hely ⏎ a Krónikák (31-szer) ⏎ Dán 11:37 ⏎ …” (a felsorolás kettévágva, fej nélküli sor) | „… 2Kir 21:22; a Krónikák (31-szer); Dán 11:37; יִשְׂרָאֵל אֱלֹהֵי Izráel Istene …” (egy bekezdés) |
| 2 | J | /szo/H1242 | „a.az éjszaka végéről17 hivatkozás … ⏎ (szemben” (sorfej + hivatkozásmező) | „az éjszaka végéről (ellentétben: לַיְלָה‎) 2Móz 10:13 (J) 3Móz 6:2 (P) Bír 19:25; Ruth 3:13 …” |
| 3 | J | /szo/H1242 | magában álló „l.”, „vö.” sorfej, „—” helyőrző, „&”, „+,” | a szöveg egyben, „&” → „és”, „+” → „és máshol”; a helyőrző „—” helyén a pont első tagmondata (dőlten) |
| 4 | J | /szo/H1242 | „34:25” típusú chip könyvnév nélkül (68/201) | a chipek megszűntek: a hely a mondatban áll, a folytatólagos hivatkozás a BDB idézési rendje szerint, és a link súgója a teljes helyet adja („feloldva: 2Móz 22:9”) |
| 5 | J | /szo/H1242 | „(szemben לַיְלָה-val)”, „(szemben הַיּוֺם ma)”, „‖” | „ellentétben: לֵילוֺת”, „(ellentétben: הַיּוֺם ma)” (a rag nélküli alakot a tételmérce fogta meg), „(párhuzamban: מחר …)”, „(nem párhuzamos hely: Zsolt 18:3)” |
| 6 | J | /szo/H0430 | „Ézs^2 (9-szer)”, „Dl^HWB”, „ᵑ7” | „Ézs² (9-szer)” (felső index), „Dl<sup>HWB</sup>”, „Targum” / „LXX” / „Pesitta” / „Vulgata” (súgóval) |
| 7 | J | /szo/H0430 | „Di 7:13” link és magyarázat nélkül | „(R, l. Di 7:13)”, a „Di” rövidítés súgója „A. Dillmann”, és a jelmagyarázatban is áll; a „7:13” nem könyvnév (a „Di” szerzőjel, nem könyv) |
| 8 | J | /szo/H1242 | „׳לַבּ reggelen …” | „לַבּ׳ Ámós 4:4 7-szer; … לַבּ׳‎ 2Móz 34:2”; a H0430 kártyáján szó eleji ׳: 0 |
| 9 | J | /szo/H0430 | „א׳ אדני אברהם” magyarázat nélkül | „א׳” rövidítés-súgóval („a címszó: אֱלֹהִים (elóhím)”); a szórend a Biblia által igazolt javítással |
| 10 | J | /szo/H1242 | „1reggel131 ⏎ 2holnap, másnap71”, „Apparátus és szövegkritika 2” | „1reggel131 hivatkozás ⏎ 2holnap, másnap71 hivatkozás”; az apparátus-szám megszűnt |
| 11 | J | /szo/H7837, /szo/H3615 | H7837: a teljes szöveg az „Alakok ▸” alatt; H3615: „Qal ⏎ 1—25” | H7837: „A szótár ezt a szócikket nem tagolja … a teljes szöveg áll.” + a szöveg nyitva; H3615: „A szótár itt ragozott alakokat sorol …, ezért a törzs szövege egyben áll.” |
| 12 | J | /szo/H2416 | a tagolt kártyából tagmondatok hiányoztak, csak a csukott teljes szöveg őrizte | a jelentések teljes szövege egyben áll; ahol a szakasztábla hiányos (1 073 szócikk), a teljes szöveg nyitva, kimondva |
| 13 | J | /r/szo/H0747 | nyers „BDB-szócikk (nyers szöveg)” blokk | „Lefordítva · gépi fordítás ⏎ אֲרִיסַי tulajdonnév, hímnemű, Hámán fia …” a kártyában, csukva az „Angol eredeti” |
| 14 | R | /szo/H1242 | „17 hivatkozás” mellett LXX πρωΐ 8 · φωσφόρος 6 · 5; a Görög megfelelő blokkban „φωσφόρος 88” | **Rád vár: adat-PR a #231 után, a kapu-szál előtt (IRANY.md).** A súgó kimondja, hogy a pár versenként számol, ezért az összeg eltérhet (8+6+5 = 19 a 17 hivatkozás mellett: nem számolási hiba). **Mérve: adathiba.** A Macula LXX-párjaiban a „πρωὶ” alak Strong-száma G5459 (φωσφόρος) a G4404 helyett, 88-szor; az LXX_OS-ben a G5459 nem fordul elő; a `lxx_bridge` ezt viszi tovább. Az olvasó kódja jól számol: **N-F231a** (`nyitott/uj/olvaso-egyben-3464e1.md`; célfeladat: rövid adatjavító PR a #231 után, nehéz körrel). A „nem igazolt” jelölés mérve, de nincs bevezetve (2. szakasz) |
| 15 | J | /szo/H1242 | „▸ forrásjel (J) (P) (mindkettő J E) …” leválasztva | a forrásjel a helye mellett, a mondatban: „2Móz 10:13 (J) 3Móz 6:2 (P)”, súgóval |
| 16 | J | /1Moz/1/5?szo=H1242 | „Ebben a versben …” | „A BDB besorolása: 1Móz 1:5 ⏎ A szótár ezt a helyet ebbe a jelentésbe sorolja: 1. e. — ellentétben: עֶרֶב”; kétes, fej, tagolatlan: jelölés nélkül (DT914) |
| 17 | V | /szo/H2403 | „Külön meghatározás nélkül”: a main-en már nem áll (0 találat); a „1.a — 5 hivatkozás” csukott sor | a csukott sorok megszűntek, a szám a tábla feloldott helyeiből (`vj.db`) |
| 18 | R | /szo/H7451 | „172 hivatkozás jelentéspontja … nem azonosítható” | a szöveg olvasói („… a szövegben kattintható, de a jelentéspontja ebben a tagolásban nem azonosítható”). **Rád vár (#237):** a `bdb_tagolas.py` sorbelső feje és a két szócikk azonos címkéje (N144, N145), a régi generátorral közös kód |
| 19 | J | /szo/H0026 | az angol eredetiben „2Sam” | „1Sam 25:18” (a 412 hivatkozás-javítás a kártya angol szövegében is) |
| 20 | J | /szo/H0127 | „4Móz 16:30 ‖ ארץ …”, a pe/mem javítás nem illeszkedett | „פָּֽצְתָה הָא׳ אֶת־פִּיהָ‎ 4Móz 16:30 (P)”; a `bdb_rovidites` változatlan, a betűjavítás az olvasó hívásában a sorrend-csere után, a maqqéf feloldása előtt is fut (`blokkok._heber_sorrend`; a tételmérce fogta meg, l. 4. szakasz) |
| 21 | J | /szo/G0264 | a lap a nyers TBESG-gel kezdődött, nem volt Strong-szótár, Előfordulás, Károli-alakok | blokksor: Strong-szótár, Előfordulás, Károli-alakok, Szótár: Thayer-szócikk, ÚSZ, héber háttér, SDGNT, UBS DNTG, alul csukva a forrásszövegek |
| 22 | J | /szo/G0264 | „Magyar fordítás nincs · az angol eredeti áll.” (az angol egy másik blokkban) | ugyanez a felirat a kártya tetején, alatta a jelentések rendje és szakaszonként az angol szöveg a kártyában, kattintható helyekkel |
| 23 | K | /szo/G0264 | a Thayer magyar fordítása 354/5 426 | kimarad: fizetős fordítás, a felhasználó költségdöntése |
| 24 | R | /szo/G3056 | a görög alapjelentés angol | **Rád vár:** fizetős fordítás (N177), a felhasználó hatásköre |
| 25 | J | /Rom/3/23?szo=G0264 | „Ebben a versben” csak a pont nevével, a szövegben nincs kiemelés | „A Thayer besorolása: Róm 3:23 ⏎ … a — absolutely”; a szövegben a hely kiemelve („Rom 3:23” link, `bdb-itt`) |
| 26 | R | /szo/G0266 | a Thayer-besorolás mért, javítatlan esetei | **Rád vár (#237):** a Thayer-szeletelő és a generált tábla, amelyet a lapgen is használ (N123, N125, N126) |
| 27 | J | /szo/G0264, /szo/H0251 | „000262001001000 ¦ Sin, Wrongdoing …” | „1. to sin; to engage in wrongdoing; sin · Sin, Wrongdoing, Guilt ⏎ … Előfordulások (37): …”; az azonosító csak súgóban; az UBS DBH- és az SDBH-doménkód is |
| 28 | J | /szo/G0264 | „43 előfordulás 37 versben.” + 5 sor | „43 előfordulás 37 versben. ⏎ Az első 5 vers áll a 37 közül. ⏎ Igehely ¦ Károli-szöveg ¦ Jelentés (UBS)” |
| 29 | J/R | /Rom/3/23?szo=G0264 | a görög szó-lapon nem volt vers szerinti blokk | **javítva:** „A Thayer besorolása” a vers szónézetéből; **rád vár:** a görög alaktani elemzés, mert nincs görög alaktani kulcs (`morf_kulcs_heber` csak héber), adatkérdés |
| 30 | J | /1Moz/1/1 | 11 csempe külön, „1 ¦ Kezdetben ¦ בְּ” és „1 ¦ Kezdetben ¦ רֵאשִׁ֖ית” | írott szavanként keret: „בְּרֵאשִׁ֖ית berésít” fölötte, alatta a két csempe; „1 ¦ Kezdetben ¦ בְּ + רֵאשִׁ֖ית ¦ H9003 + H7225” |
| 31 | J | /1Moz/3/6 | „אִישָׁ֛ leísáh” (a ה nélkül) | a keret tetején „לְאִישָׁ֛הּ leísáh”, alatta לְ · אִישָׁ֛ · הּ |
| 32 | J | /1Moz/1/1 | az előtagcsempén nincs kiejtés, a szótőcsempén az egész szóé („berésít”) | a kiejtés az írott szóé, a kereten áll; a csempék nem ismétlik |
| 33 | V | /1Moz/3/6 | „gam” kötőjel nélkül (az F230 óta) | elvetve, mert már javult: az F230 kiejtés-szolgáltatása óta a csempén „גַּם gam” áll, kötőjel nélkül (a tételmérce élőben nézi). |
| 34 | J | /Jan/1/1 | „ἀρχῇ ¦ arkhéa” | „arkhé”; a TAGNT „ēa” átírása az alsó iotás étánál (1 471 token) a kiejtés-szolgáltatásban javítva |
| 35 | J | /Jan/1/1 | „λόγος, ¦ logosz” | „λόγος ¦ logosz” (a központozás nélkül; a tükörfordítás változatlan) |
| 36 | J | /1Moz/1/1 | a csempék adatai 6 nyitott táblázatban | „Táblázatos nézet (a csempék adatai soronként)” csukva (Károli–Strong, TAHOT/TAGNT, Macula ×2, LXX_OS, igealak) |
| 37 | J | /Zsolt/22/2 | „Osztály ¦ KJV-versszám ¦ MT-versszám …” a fül közepén | a Károli-szöveg alatt: „Versszámozás: héber (MT) 22:2 · angol (KJV) 22:1”, „Septuaginta-versszám: Zsolt 21:2” |
| 38 | J | /1Moz/1/5 | „¦ magas” | „¦ 99% (Mózes öt könyve)” (a könyvcsoport mért pontossága, súgóban a 95%-os intervallum és a proveniencia) |
| 39 | R | /1Moz/1/1 | „Ez az adat ebben a kiadásban még nem érhető el” | változatlan, igaz szöveg. **Rád vár (F235 2. rész):** az LXX-többlet táblái nincsenek betöltve (`sqlite_epit` + újraépítés) |
| 40 | J (+N49) | /Zsolt/22/2 | „Nincs adat (üres eredmény, nem negatív lelet).” | „A BSB-forrás ehhez a vershez nem ad szavakat (a forrásból hiányzik).” A forrás pótlása a meglévő **N49**-é (integrátori döntés: a `BSB_Strongs.tsv`-ben nincs Psa.22.1–2), adatmunka |
| 41 | V | /Zsolt/22/2 | „GodH0410GodH0410forsaken…” | nem hiba: a pillanatkép a csempe szavait tapasztja össze; a lapon külön csempék |
| 42 | J | /Zsolt/22/2 | „PROPHECY ¦ . ¦” | „PROPHECY ¦ ¦” (a „.” helyőrző nélkül; a fordítás nélküli téma angolul, a szabály szerint) |
| 43 | J | /1Moz/1/1 | „Összesen 68 hivatkozás; az első 15 látszik …” a táblázat alatt | „68 kereszthivatkozás; az első 15 áll, a szavazatszám szerint.” a táblázat előtt |
| 44 | J | /1Moz/4/7 | „PaRDeS-szint” | „Értelmezési szint” |
| 45 | J | /szo/H1242 | „Strong-szótár forrásadat modell-kimenet” | „Strong-szótár”; a jelleg-címkék a csukott „Forrás és licenc” lenyílóban |
| 46 | J | /szo/H1242 | „Forrás és licenc: Strong_szotar (strong_szotar): CC BY 4.0 · … projekt_adat …” nyitva | csukva: „Forrás és licenc: Strong szotar: CC BY 4.0 · TBESH+TAHOT+a projekt saját adata: …”; a belső nevű sor a súgóban |
| 47 | J | /Jan/1/1 | 16× „Nincs adat (üres eredmény, nem negatív lelet).” | egy sor fülenként: „Ezekben a forrásokban erre nincs adat (üres eredmény, nem negatív lelet): Versszámozás (MT / KJV), LXX-versszám, …” |
| 48 | J | /Zsolt/22/2 | „… ¦ lxx_os_etalon_f91” | az összefoglaló sorban nincs; a forrásazonosító csak súgóban |
| 49 | J | /Zsolt/22/2 | „a Strong-címkék GPL-eredetűek: nyilvános kiadásból kimarad” a blokkcím mellett | a csukott Forrás-lenyílóban |
| 50 | J | /szo/H1242 | „szó-lap önálló címen · előfordulások versenként” | „A szó saját lapja · Minden előfordulás versenként (keresés)” |
| 51 | J | / | „PaRDeS olvasó” | „Biblialex olvasó” (egy kulcs: `olvaso.nev`) |
| 52 | J | / | „Szint nyilvanos regisztralt kutato” | „Szint nyilvános regisztrált kutató” |
| 53 | J | / | a főoldalon nincs Biblia-választó | „Biblia és könyv kiválasztása” (a fejezet-lap navigációja a főoldalon is) |
| 54 | J | /1Moz/1 | az aktív „kis próféták” gomb 4,26:1 | ≈ 5,4:1: az aktív gomb háttere a műfajszín 85%-a feketével keverve (a `g-kis` token a mockupé marad, #a0702a; WCAG AA) |
| 55 | J | / (mobil) | 24–32 px-es érintési célok; tanulmányjel 3,73:1 | érintőképernyőn (`pointer: coarse`) legalább 44 px; a tanulmányjel átlátszóság nélkül 6,65:1 |
| 56 | J | /szo/H1242 | „214 előfordulás, 29 könyvben.” mondatként egy blokkban | a lapfej alatt három számkártya: „214 előfordulás · 29 könyvben · 221 Károli-előfordulás” |
| 57 | J | /szo/H1242 | „A 66 feldolgozott könyv (1Jan, 1Kir, 1Kor, …)” | „Mind a 66 könyv szó szintű párjai alapján.”; arányos sáv (`<meter>`) az alakok mellett |
| 58 | J | /szo/H1242 | „reggel morning” | „reggel” (az angol a súgóban: „angol eredeti: morning”) |
| 59 | K | /motivum/HAMART-001 | 404 | kimarad: F164, új funkció |
| 60 | J | /1Moz/1, /szo/H1242 | lassú (új fejezet 0,8–3 s) | az F235 1. része (#799) a main-en; az ág a main-ről indul (a mintalapok lekérése az előnézeten 0,1–0,4 s) |

## 4. Menet közben talált és javított hibák

- **A Biblia által igazolt héber sorrend-javítás elmaradt** (H0430: „א׳ אברהם אדני” a javított „א׳ אדני אברהם” helyett). Ok: a rövidítőjel áthelyezése a forrás alakját („׳א אברהם אדני”) a sorrend-javítás előtt megváltoztatta. Javítva: a sorrend-javítás fut előbb; regressziós állítás a `teszt_szokartya_egyseges`-ben.
- **Az UBS DNTG magyar fordítása nem jelent meg**, mert a lekérés a Strong-számot adta a bejegyzés-azonosító (lexid) helyett. A teszt fogta meg, javítva.
- **A görög iota-átírás** (#34) nem egyedi eset: 1 471 token, a kiejtés-szolgáltatásban javítva.
- **A 15 jegyű azonosító** nemcsak a DNTG-ben, hanem az UBS DBH- és az SDBH-táblában is látszott (a 2.6-os kapu fogta meg). Javítva: csak súgóban áll.
- **A tételmérce (F231.11) három hibát fogott, amelyet a jelentés javítottnak írt.** (1) #20: a sorrend-javítás előre hozása (F231.7) után a pe/mem betűjavítás a rafe-maqqéf feloldása után futott, ezért a H0127 „אֶתמִּֿיהָ” kulcsa nem illeszkedett, a lapon „אֶת־מִּיהָ” állt. Javítva: `blokkok._heber_sorrend` (sorrend-csere → betűjavítás → a közös `heber_sorrend_javit`). A lexikon-generátor (`lexikon_general.py` 4657. sor) a közös `heber_sorrend_javit`-ot hívja, amelynek belső sorrendje ugyanez (sorrend-csere → maqqéf → betűjavítás), ezért ott a sorrend-javítással érintett pe/mem alak ugyanígy javítatlan maradhat: kimenete: **rád vár: a #809 méri az új generátoron** (integrátori döntés, 2026-11-23: a régi generátort az új, `eszkozok/lapgen/` váltja ki; a #810-ben nincs vele teendő). (2) #5: a „szemben” rag nélküli héber szó előtt („(szemben הַיּוֺם ma)”, H1242 2.) maradt; javítva (`szokartya_szoveg.szemben`, a magyar „vele szemben” érintetlen). (3) #35: a Jn 1:1 csukott „Táblázatos nézet” Károli–Strong sorában „λόγος,” áll: elvetve, mert ez a párosítás forrásadat-sora a forrás tokenjével (a csempe és a TAGNT-sor írásjel nélküli, a tétel tárgya ez volt).
- **A motívum jelentése a kétes pontból is** hordozónak látszott (H7451 10.c). Javítva a DT914 szerint; az egyezési teszt fogta meg.

## 5. Rád vár (az integrátor vezeti át az IRANY.md-be)

- **#14** — a hamis LXX-pár („πρωὶ” → G5459, N-F231a): adat-PR a #231 után, a kapu-szál előtt (IRANY.md).
- **#18** — a `bdb_tagolas.py` sorbelső feje és a két szócikk azonos címkéje (N144, N145): #237 (B0).
- **#24** — a görög rövid jelentések fordítása (pénz): igen vagy elvetve (N177).
- **#26** — a Thayer-besorolás javítatlan esetei (N123, N125, N126): #237 (B0).
- **#29** (a görög alaktani rész) — görög alaktani kulcs kell (adat).
- **#39** — az LXX-többlet táblái: F235 2. rész.
- **Két megvalósítás (DT-F231a feltétele)** — ha a lapgen olvasói felülete elkészül (#237, B0), az olvasó arra áll át, és a saját kártyamodell kivezetendő.

## 6. Tesztek és kapu

- Új: `teszt_szokartya_egyseges.py` (10 teszt): az olvasói szövegátalakítás, a 2.6-os kapu a mérési mintán (‖, ^, 13+ jegyű szám, „szemben X-val”, belső címkék), a fordítótábla-kapu, az egyezési teszt a HAMART-001 4.2-vel, a szócsoport-szabály a Macula ellen.
- A meglévő tesztek a szándékosan megváltozott szerkezethez igazítva (szókártya, Thayer-kártya, Forrás-lenyíló, DT914, a főoldal navigációja, a tervező regisztere: −9 elem, a használati sorok elemei).
- **A tételmérce (F231.11, IRANY.md 1. szál „kész” mércéje):** `teszt_tetelmerce.py`, tételenként egy teszt (`test_t01` … `test_t60`, a 23. és az 59. nélkül: 58). A `J` tétel az élő lapon a javított alakot keresi és a hibásat tiltja (a F232 pillanatképén, a csukott tartalommal vagy anélkül, vagy a nyers HTML-ben; #54/#55 a CSS-ből számolt WCAG-kontraszttal, #60 új fejezet idejével); a `V`/`R` tétel a 3. szakasz sorát nézi (kimenet, legalább egy mondatnyi indok; `R`: „rád vár”); a kimenet-oszlop csak J / V / R lehet (a K a két megbízáson kívüli sor), ezt a `Keszlet` is őrzi, és ahol a lapon is van mit nézni, azt is. Kimenet: `TÉTELMÉRCE: n/58 zöld`. A `Keszlet` osztály őrzi, hogy a mérce a jelentés 60 sorából pontosan az 58-at fedi. Az első futás 51/58 volt: 3 valódi hiba (#5, #20 javítva; #35 elvetve, l. 4. szakasz) és 4 pontatlan minta (#6, #16, #22, #44: rossz lapra vagy blokkra nézett).
- A gyors kör és a push előtti kapu eredménye: l. 7. szakasz.

## 7. Futási eredmények

- `python eszkozok/teszt_futtat.py --gyors`: **zöld** (580 mp, minden fájl; a lassú `teszt_szintek` nélkül).
- `python eszkozok/push_elott.py --reszleges`: az első futás az E5-ön bukott (a mérce-fájlokból törölt `## [blokk]` sorok: a rejtett üres blokkok, #47; a jelölés a commit-üzenet „TÖRLÉS-SZÁNDÉKOS:” sora). A mérce a sorrend-javítás után újra frissült (6 BDB-lap), a besorolás a main-hez mérve újra lefutott (besorolatlan sor: 0). A második futás eredménye a PR első sorában áll.
