# KIADAS TEREMT-001 — lektori kérdéslista és olvasói átolvasás (U4, F239)

*2026-11-23 · a hívó: `claude-opus-5-5` (U4) · a lap: az új generátor előnézete (`python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívül>`, az N-F239a nem commitolt kerülőújtával, a `e1484e2d` fej adatán), mert a repó `lexikon/TEREMT-001_TUDOMANYOS.md` lapja befagyasztott régi lap. **Minden tétel nyitott**, és a lapnézettel együtt kerül az U5-ben a szerkesztő elé; lezárt tétel innen nem megy vissza hozzá. A javítás a próza gazdájáé (U6, `/lap-javit`), illetve a generátoré (a 3/b generált tételei).*

## Összegzés

| rész | forrás | tétel | ebből kérdés |
|---|---|---:|---:|
| 1–2. lefedettség, egyenetlenség | `naplok/KIADAS_TEREMT-001_lista.md` | 2 jelölt blokk | (a lektor listáján: 28., 37. tétel) |
| 3. lektor (Fable) | 44 tételes vak lista (`naplok/F239_U4_lektor_munkafajl.md`: az eredet) | 44 | **23** |
| 3/b (a) minta-kapu | `olvasoi_kapu.py` MINTA-szabálya az előnézeten | 1 találat | 1 |
| 3/b (b) olvasói átolvasás (Fable, teljes lap) | a renderelt lap blokkjelekkel | 119 | **119** |
| 3/b (c) mechanizmusok | `naplok/HIBA_MECHANIZMUSOK.md` | 5 lapot érintő | l. lent |

**A vak minta** (az F2 102 „igazolt” tételéből 11; `random.Random(239)`): a lektor a mintatételek saját állításánál pontossági hibát nem talált (K74: érthetőségi kérdés, 41. tétel; K77-nél és K35-nél a kérdés a szomszédos, más mondatra szól, 6. és 17. tétel). A felfüggesztés szabálya (`/kiadas` 3. lépés) ezért nem lépett életbe; a szomszédos mondatokon talált hibák szivárgásként a `naplok/SZIVARGAS_TEREMT-001.tsv`-ben (S019–S021).

**Az F2 megfogási aránya** (DT881, küszöb 80%): a lektor 17 pontossági kérdéséből (1. vagy 4. típus, vers- vagy adatállítás) az F2 14-et már jelzett (hamis vagy vitatott) — **14/17 = 82%**. Át nem fogott: a 140. sor második mondata (6.), a „hét vers” igéi (15.; F2: K48, K65 igazolt), a Drash Jón 2:6 „felhoz”-a (24.; F2: a Kivonatban K2 hamis, a Drashban K53 igazolt).

## 3. A lektor kérdéslistája (szó szerint)

*A `lektor` subagent válasza változtatás nélkül; csak a címszintek eggyel lejjebb tolva. A tétellista: `naplok/F239_U4_lektor_munkafajl.md` (eredettel).*

**0. Modell-ellenőrzés:** a tényleges modell `claude-fable-5-2`, a kért `fable`: egyezik. A próza modellje a hívó szerint `claude-opus-5-5`, a lektor tehát független.

### Kérdéslista — TEREMT-001 (44 tétel)

Összesen 23 tételnél van kérdés, 21 rendben. A kérdésszámok: 1 = ellentmond az adatnak, 2 = érthetőség, 3 = belső szakszó, 4 = adat nem támasztja alá, 5 = érvnapló. Minden találat kérdés a próza gazdájához.

**1.** (TEREMT-001.md:93; Ézs 51:10, Ámós 7:4, Ézs 51:9) — rendben. Ézs 51:10 „a ki a tengert megszáraztotta, a nagy mélység vizeit”; Ámós 7:4 „megemészté az a nagy mélységet”; Ézs 51:9 „a ki Ráhábot kivágta, és a sárkányt átdöfte” (`Karoli_1908.tsv`; TAHOT Ézs 51:9: H7294 + H8577). Az érvnapló D2.2 szerint áll.

**2.** (TEREMT-001.md:55; 2Móz 15:5, 15:8) — rendben. `LXX_OS/exodus.tsv` 15:5: πόντῳ … εἰς βυθὸν; 15:8: τὰ κύματα. TAHOT 2Móz 15:5: H8415 az első, H4688 (mecólót) a második félversben. Érvnapló A3, D3.1.

**3.** (TEREMT-001.md:47; Zsolt 71:20) — rendben. BDB H8415, 5. pont: „abyss (si vera lectio) … = Shejôl, Psa 71:20” (`BDB_teljes_unabridged.tsv`, H8415).

**4.** (TEREMT-001.md:93; 1Móz 1:2) — rendben. BDB H8415, 3. pont vége: „compare, further, Gunk Schöpfung u. Chaos 21 ff.”. A H8415 szócikkben és a `BDB_rokon_irasok.tsv`-ben nincs Tiámat. A rokonítás recepcióként áll, ahogy az érvnapló V1(a) kéri.

**5.** (elofordulasok.tsv:51; Zsolt 148:7) — rendben. Károli: „Dicsérjétek az Urat a földről: viziszörnyek és mély vizek ti mind!”; TAHOT: H8577 + H8415 többes szám.

**6.** (TEREMT-001.md:140; Ézs 51:9, Zsolt 148:7) — **kérdés (1).** „Ezek saját szavaikkal szerepelnek, a mélység szava nélkül, ezért a lexikai keresés nem hozza őket.”
   - A Zsolt 148:7-ben a szörny-szó és a tehóm ugyanabban a versben áll (TAHOT Zsolt 148:7: H8577 és H8415), és a vers a motívum helye (`elofordulasok.tsv:51`).
   - A Leviatán nyomát mondó Jób 41:32 szintén motívumhely (`elofordulasok.tsv:253`).
   - A „mélység szava nélkül” így a három példából csak az Ézs 51:9-re igaz.
   - Mellékesen (3): a „lexikai keresés” belső szó-e az olvasónak?

**7.** (Péld 8:24, „teremtés előtti állapot”) — rendben. A próza a Péld 8:24-ről ezt mondja: „Itt a mélységnek kezdete van, és Isten határt szab neki” (:75). A „teremtés előtti” kifejezés a résekben nem áll. Érvnapló B1b.

**8.** (Róm 10:7 Vitatott pont, tény és nyitott kérdés külön) — a Vitatott pontban rendben, a Remezben **kérdés (5).**
   - Vitatott pont (:99): „Az tény, hogy…”, „Az is tény, hogy…”, majd külön mondatban „Az egyik olvasat szerint…”. Ez megfelel.
   - Remez (:81): „…hét versben áll együtt a leszállás vagy a felhozás igéjével; hogy Pál ezekből merít-e, a Vitatott pontok egyik nyitott kérdése.” Itt a tény és a nyitott kérdés egy mondatban áll, pontosvesszővel. Az érvnapló V4 döntése és D3.4 a Remezre is külön mondatot ír elő.

**9.** (TEREMT-001.md:73; 1Móz 7:11, 8:2, 49:25, 5Móz 33:13, Péld 8:28, Zsolt 107:26) — **kérdés (1), apró.** „az ég áldásai és a mélység áldásai (1Móz 49:25, 5Móz 33:13)”. Az „áldásai” szó a Károliban csak az 1Móz 49:25-ben áll. Az 5Móz 33:13 szövege: „az égnek kincseivel, a harmattal és az alant elterülő mélységes vizekkel”. A másik három pár rendben (Károli 1Móz 7:11, 8:2; Péld 8:28; Zsolt 107:26).

**10.** (a Remez nem mondja, hogy a Jel 20 „megismétli” az 1Móz 8:2-t) — rendben a tételre: a :79 és a :81 ilyet nem mond, a „keretezi” szó sem áll. Két **kérdés (5)** ugyanerről a helyről:
   - :79: „a négy hely négy különböző dolgot mond a mélységről: a kezdet vizét …, a feltörő és ítélő vizet …, a bezáruló forrásokat … és az áldást”. Az érvnapló V6 szerint a négy funkció neve olvasat, és „a próza így jelöli”; a mondat nem jelöli olvasatnak.
   - :79: „A Biblia későbbi könyvei ezeket a kifejezéseket hozzák vissza.” Ez irányt és átvételt állít. A Remez a lap saját meghatározása szerint „még következtetés nélkül” szól (:71), az érvnapló B-táblája szerint pedig adat csak a szóismétlés.

**11.** (TEREMT-001.md:97) — **kérdés (5).** „a 2Móz 15-ben a mélység a tenger része, nem a világ alatti víz”. Ez az érv az érvnapló V3(b) bizonyítékai között nem szerepel; ott csak az egyetlen közös lexéma és a „forrás”, „nagy” társszó hiánya áll. Az adat egyébként alátámasztja (BDB 1. és 2. jelentés). A mondat többi része rendben: TAHOT 2Móz 15:5 és 15:8-ban nincs H7227 és H4599. A D3.2 szerint törlendő „kommentárirodalom” mondat a V3-ban valóban nem áll.

**12.** (a Kivonat „nem cselekszik Isten ellen” mondata és a Tiámat-pont) — **kérdés (5).**
   - A Kivonatban ez a mondat nem áll. Ott csak ez van: „a versben semmit nem cselekszik” (:11, az 1Móz 1:2-ről). A mondat a Peshatban áll (:73), és a Vitatott pont zárásával (:93) szó szerint egyezik; ellentmondás nincs.
   - A :93 a „nem cselekszik Isten ellen” tényt csak a „másik olvasat” érveként hozza. Az érvnapló V1 mérlegelése szerint ez hiányérv, amely a „demitologizált átvétel” olvasattal is összefér. Ezt a próza nem mondja ki.

**13.** (TEREMT-001.md:13) — rendben. A hivatkozott helyek motívumhelyek (`elofordulasok.tsv:30, 53–55, 47, 65`). Megjegyzés (1), apró: a „helyek csoportjai” felsorolásból hiányzik az adat négy funkciócsoportja: elérhetetlen mélység (Jób 28:14, 38:16, 38:30, 41:32), Isten megjelenése (Zsolt 77:17, Hab 3:10), panasz (Zsolt 42:8), vihar (Zsolt 107:26).

**14.** (Ez 26:19, Ez 31:15, Zsolt 107:26 mint „a halál mélye”) — rendben.
   - Kivonat: „két helyen a halál közelségének képe … (Jón 2:6, Zsolt 71:20)”.
   - A Sod (:87) a három helyet nem említi.
   - Módszertan (:139): az Ez 31:15 „ott sem azonos jelentéssel”.
   - Az adat funkciói: ítélet, érintkezés, vihar (`elofordulasok.tsv:58, 60, 49`).
   - Határeset, a gazda mérlegelésére: a :49 szerint a Zsolt 107:26 „halálos veszedelem”.

**15.** (TEREMT-001.md:99; Zsolt 107:26, Róm 10:7) — az alak és az elöljáró rendben, a hét versnél **kérdés (2/4).**
   - Rendben: LXX Zsolt 106:26 „καταβαίνουσιν ἕως τῶν ἀβύσσων”, Róm 10:7 „εἰς τὴν ἄβυσσον”.
   - A „hét versben áll együtt” csak egy versben való együttállás. Négy versben az ige nem a mélységbe vagy a mélységből való mozgást mondja:
     - Ez 31:15: „κατέβη εἰς ᾅδου, ἐπένθησεν αὐτὸν ἡ ἄβυσσος” (a leszállás a hádészba történik);
     - Jób 38:30: „ἣ καταβαίνει ὥσπερ ὕδωρ ῥέον” (más alany);
     - Jób 36:16: „κατέβη τράπεζά σου” (az asztal);
     - Ez 26:19: „ἀναγαγεῖν με ἐπὶ σὲ τὴν ἄβυσσον” (a mélységet hozza fel).
   - Az olvasó a „leszállás igéjével négyben” fordulatból azt értheti, hogy négy versben a mélységbe szállnak le.

**16.** (névelőhasználat) — rendben. A „névelő” szó a fájlban nem fordul elő (grep: 0 találat). Érvnapló A6: kimarad.

**17.** (TEREMT-001.md:73) — rendben az érvnapló V1 eldöntött állítása szerint. A 35 TAHOT-vers és a 35 Károli-idézet (`elofordulasok.tsv:30–63, 253`) között nincs olyan, ahol a mélység Isten ellen cselekszik. **Kérdés (4)** a következő mondatra: „megnyitja és bezárja a forrásait (1Móz 7:11, 8:2)”. Mindkét ige szenvedő, megnevezett cselekvő nélkül (TAHOT 1Móz 7:11 H1234 „they were split open”, 8:2 H5534 „they were shut up”; Károli „felfakadának”, „bezárulának”). Az érvnapló V2(b) szerint a „megnyit” ige egyik nyelvben sem a mélységé.

**18.** (TEREMT-001.md:11; Luk 8:31, Jel 11:7, 17:8, 9:1-2, 20:1, 20:3) — az idézett helyek rendben (Károli Luk 8:31; Jel 9:1 „a mélység kútjának kulcsa”; 9:2; 20:1; 20:3). Három **kérdés:**
   - (4) „amelyet Isten megnyit, bezár” — ugyanaz, mint a 17. tételnél.
   - (1) „amelyet a Jelenések könyve … egyszer bezár és lepecsétel”. A lap mércéje a Textus Receptus (:15, :133). A TR-ben a zárás tárgya hímnemű névmás: „ἔκλεισεν αὐτὸν” (`TAGNT_kivonat.tsv`, Jel 20:3, G0846, kiadás-oszlop: csak `TR`), az ἄβυσσος pedig nőnemű. A TR szerint tehát a sárkányt zárja be. A Károli „bezárá azt” kétértelmű.
   - (4) a „zárt hely” általánosítása: l. 38. tétel.

**19.** (elofordulasok.tsv:52; Péld 3:20) — rendben. Károli: „Az ő tudománya által fakadtak ki a mélységből a vizek, és a felhők csepegnek harmatot,”.

**20.** (TEREMT-001.md:11; 1Móz 7:11, 8:2, 49:25, 5Móz 33:13, 2Móz 15:5, 8) — rendben, egy **kérdés (1), apró.**
   - Rendben: „a nagy mélység minden forrásai” (1Móz 7:11); „bezárulának a mélység forrásai” (8:2); 2Móz 15:8 „megmerevültek”.
   - A „a mélység áldásaival, mely alant terül” idézet két hivatkozással áll, de csak az 1Móz 49:25 szövege. Az 5Móz 33:13-ban „az alant elterülő mélységes vizekkel” áll.

**21.** (TEREMT-001.md:87) — **kérdés (4).** „A motívum helyein a mélység határa mindig kívülről, felülről szabott.”
   - A „mindig” a 43 helyre szól, határról viszont csak néhány hely beszél (a próza maga négyet-ötöt hoz).
   - Az első példa: „a források Isten akaratából nyílnak meg és zárulnak be (1Móz 7:11, 8:2)”. A két versben cselekvő nincs megnevezve (l. 17. tétel), az „Isten akaratából” következtetés.

**22.** (a Sod zárómondata) — az idézetek rendben, egy **kérdés (2).**
   - Rendben: Jel 9:1 „adaték annak a mélység kútjának kulcsa”; 20:1 „leszállani a mennyből, a kinél vala a mélységnek kulcsa”; 20:3 „míg betelik az ezer esztendő”.
   - „a kulcs egyszer sem a mélységé”: a Károli szövege éppen „a mélységnek kulcsa” (Jel 20:1). A mondat a birtokost tagadja ott, ahol a vers birtokos szerkezettel beszél. Érti-e az olvasó, hogy a kulcs tartójáról van szó?
   - Megjegyzés (5): az érvnapló B9 kikötése, hogy a kulcs és a nyit–zár a Jelenések általános szókincse (Jel 1:18, 3:7), a prózában nem jelenik meg; ellenkező állítás sincs.

**23.** (TEREMT-001.md:59) — **kérdés (1).** „A Tengeri énekben és a Zsolt 33:7-ben »hullámok«”. A Tengeri ének két verse közül csak a 2Móz 15:5-ben áll „hullámok”. A 15:8-ban a Károli szava „mélységes vizek” (`elofordulasok.tsv:35`; Károli: „a mélységes vizek megmerevültek”). A többi szó rendben az adat `karoli_szo` mezőjével és a Károli-versekkel: Hab 3:10 „hullám”, Zsolt 104:6 „Vízáradattal”, 42:8 „Örvény”, Jón 2:6 „mély ár”, Zsolt 107:26 „fenékig”, 5Móz 8:7, Jób 38:30, Zsolt 148:7 „mély vizek”, Jób 41:32 „tenger”.

**24.** (a Drash két tétele, :85) — az első tétel rendben, a másodiknál **kérdés (4/5).**
   - Rendben: Jób 38:16, Zsolt 33:7, 135:6 idézetei (`elofordulasok.tsv:39, 41, 50`).
   - „a mélység a motívum két ószövetségi helyén a halál közelsége, de onnan Isten felhoz. Jónást »mély ár kerített be« (Jón 2:6)”. A Jón 2:6-ban felhozás nem áll. A Károliban a 2:7 mondja: „kiemelted éltemet a mulásból”, más szóval.
   - Az érvnapló B6 ezt rögzíti („a »felhozás« a 2:7-ben (verem)”), a D-tábla „Elutasított 6” sora pedig a „felhoz” közös jegyét elvetette.
   - Ugyanez a Kivonatban (:11): „ahonnan Isten felhoz (Jón 2:6, Zsolt 71:20)”.

**25.** (TEREMT-001.md:47) — **kérdés (1/4).** „A »nagy mélység« kifejezés (tehóm rabbá) öt versben áll: … a Zsolt 78:15-ben …”.
   - A Zsolt 78:15-ben a tehóm többes számú (TAHOT: `te.ho.Mot`), a rabbá egyes számú; a TAHOT glosszája „much”.
   - A Károli határozóként fordítja: „inniok adott bőségesen, akárcsak a mélységes vizekből”.
   - A BDB a רַבָּה תְּהוֹם kifejezésnél négy helyet hoz (1Móz 7:11, Ámós 7:4, Zsolt 36:7, Ézs 51:10); a 78:15-öt külön, „in simile” megjegyzéssel.
   - A próza az érvnapló A7 szerint ír („5 versben”), de az adat az ötödiket nem egyértelműen támasztja alá, és a magyar olvasó a versben nem talál „nagy mélységet”.

**26.** (TEREMT-001.md:13; Zsolt 42:8) — rendben. TAHOT H8415: 36 sor, 35 vers, a Zsolt 42:8 kétszer (`TAHOT_kivonat.tsv:454791, 454793`). 11 könyv: 1Móz, 2Móz, 5Móz, Jób, Zsolt, Péld, Ézs, Ez, Ámós, Hab, Jón. Zsoltárok: 11 vers.

**27.** (elofordulasok.tsv:71; Jel 20:3) — az idézet rendben (szó szerint a Károli Jel 20:3; a megkötözés a 20:2-ben). **Kérdés (1):** „itt bezárják és lepecsételik” a mélységet — a TR „ἔκλεισεν αὐτὸν” olvasata miatt, l. 18. tétel.

**28.** (2. blokk, a `miert_fontos` rés, :45–59) — tömör, de követhető. Két **kérdés (2):**
   - A „Septuaginta” szó a rés címében (:53) magyarázat nélkül áll; a szöveg mindenütt „görög Ószövetség”-et mond, és a kettőt az olvasónak sehol nem azonosítja. A :131 megint „Septuaginta”-t ír.
   - A :47 a BDB első négy jelentésénél nem jelzi, hogy a felsorolt helyek válogatás. Az 1. jelentésből kimarad az Ámós 7:4, a Zsolt 36:7, az Ézs 51:10 és a Zsolt 135:6; a 2.-ból a Hab 3:10, a Jób 38:30 és a Jób 41:32. Az olvasó teljes listának veheti.

**29.** (TEREMT-001.md:81; Jel 9:1, 9:2, 9:11, 11:7, 17:8, 20:1, 20:3) — **kérdés (1).** „a mélységnek királya van, a Vesztő (Jel 9:11)”.
   - A vers szerint a király a sáskáké, és ő a mélység angyala: „Királyukul pedig a mélység angyala vala felettök”; TAGNT Jel 9:11: „ἔχουσιν ἐπ᾽ αὐτῶν βασιλέα τὸν ἄγγελον τῆς ἀβύσσου”.
   - A próza az érvnapló D2.4 megfogalmazását követi, de a vers nem a mélység királyát mondja.
   - A többi rendben (Károli Jel 9:1, 9:2, 20:1; `elofordulasok.tsv:68, 69`). A „bezárja” szóhoz l. 18. tétel.

**30.** (TEREMT-001.md:95; Jel 20:3, 1Móz 8:2, Jel 9:1-2, 1Móz 7:11) — az (a) olvasat az érvnapló V2(a) szerint áll (jelentés-egyezés; „felfakadnak”, nem „megnyílnak”). **Kérdés (1):** „mindkét helyen a mélységet zárják be”.
   - Az 1Móz 8:2-ben a mélység forrásai záródnak (TAHOT: H5534 + H4599 + H8415).
   - A Jel 20:3 TR-szövegében a zárás tárgya a sárkány (l. 18. tétel).
   - A Jel 9:2-ben „a mélységnek kútját” nyitják meg.

**31.** (TEREMT-001.md:47; 1Móz 1:2, Péld 8:27, Zsolt 104:6) — rendben. BDB H8415, 3. pont: „primaeval ocean … Gen 1:2 …, Prov 8:27 …, Psa 104:6”.

**32.** (elofordulasok.tsv:57; Ézs 63:13) — rendben. Károli Ézs 63:13: „Ki járatá őket mélységekben, mint a lovat a síkon, és meg nem botlottanak!”; Zsolt 106:9: „úgy vivé őket a mélységeken, mint egy síkon”. TAHOT: mindkettőben H8415 + H4057.

**33.** (Tiámat: a rokonság nem szótári tény) — rendben. :93: „A vallástörténeti kutatás egy része … rokonítja”, és „A nyelvi rokonságot a szócikk szótárai nem tárgyalják.” Ez megfelel a BDB H8415 szócikknek és az érvnapló V1(a)-nak. A „kommentárirodalomban mindkét álláspont képviselt” mondat a V1-ben a D3.3 szerint marad.

**34.** (Róm 10:7: „ugyanazt a két igét”, „ugyanazok a szavak”) — rendben. Egyik fordulat sem áll a :99-ben. Ami áll: „ugyanazzal az igével, amellyel a Róm 10:7 a felhozást mondja”. Ez egy igére szól, az (a) olvasaton belül, és az adat fedi (LXX Zsolt 70:20 „ἀνήγαγές”, lemma ἀνάγω; érvnapló B8, D3.4).

**35.** (a kulcs és a nyitás–zárás mint motívum-specifikus szerkezet) — rendben. A próza ilyet nem állít. A :95 szerint „a megnyitás és a bezárás a könyv saját mozzanatai”. A B9 megszorítása nincs kimondva (l. 22. tétel megjegyzése).

**36.** (Jel 20 és 1Móz 8:2: „közös zár-ige hiánya”) — **kérdés (5).** „a két hely között szóbeli kapcsolat nincs: a héber 8:2 igéje (szákar) »elzárul«, a Jel 20:3-é a görög »bezár« (κλείω)”.
   - A (b) olvasat a héber igét más magyar szóval („elzárul”) állítja szembe a göröggel. Ugyanez a lap a Kivonatban a Károli „bezárulának” szavát idézi, az (a) olvasat pedig azt mondja, „mindkét helyen … zárják be”.
   - Az érvnapló V2 szerint a héber és a görög ige jelentése egyezik; ez az (a) bizonyítéka. A (b) csak a görög szint hiánya (ἐπικαλύπτω), „gyenge érv, a próza így mondja”.
   - A D-tábla „Elutasított 3” sora a „közös zár-ige hiánya” érvet elvetette. Visszahozza-e ezt a mondat, és jelzi-e a próza az érv gyengeségét?
   - Az adat: TAHOT 1Móz 8:2 H5534 „they were shut up”; LXX 1Móz 8:2 „ἐπεκαλύφθησαν” (ez rendben).

**37.** (Kivonat blokk, :11–17, tömörség) — érthető, a kizárások példái adattal egyeznek:
   - Jón 2:4: H4688, Károli „mélységbe vetettél engem”;
   - Jób 41:31: H4688, Károli „mély vizet”;
   - Ézs 44:27: H6683, Károli „Ki ezt mondja a mélységnek: Száradj ki!”;
   - 2Pét 2:4: Károli „mélységbe taszítván”.

   **Kérdés (2):** az első bekezdés nyolc mondatban huszonegy igehelyet visz végig, és a „fordulópont” állítása a közepén áll. A „zárt hely” és a „felhoz” mondathoz l. 38. és 24. tétel.

**38.** (a Kivonat fordulópontja) — **kérdés (1/4), két ponton.**
   - „Az Ószövetségben a tehóm víz” (és a Peshatban, :73: „Az Ószövetség helyein a tehóm víz”). A lap saját szótári része szerint a Zsolt 71:20 „»föld mélysége« a seól értelmében” áll (:47; BDB 5. pont), a Kivonat szerint pedig ez a hely a halál közelségének képe. Az általános mondat erre az egy helyre nem áll.
   - „az Újszövetség helyein az abüsszosz zárt hely”. A Róm 10:7-ben a halottak helye; zárásról a vers nem szól. A Luk 8:31-ben és a Jel 11:7, 17:8-ban sincs zárás; az utóbbi kettőben a fenevad éppen feljön belőle. Az érvnapló V5 a Róm 10:7-et külön veszi a „börtön”-helyektől. A Remez megfogalmazása („már nem víz, hanem hely”, :81) ezt a gondot nem veti fel.

**39.** (TEREMT-001.md:139; Róm 10:7) — rendben. Thayer G0012: „as the common receptacle of the dead, Rom 10:7, and especially as the abode of demons, Luk 8:31; Rev 9:1 …” (`adat/thayer_szakaszok.tsv`, G0012, 2. sor). Érvnapló V5: csak a Róm 10:7 a halottak helye. Az Ez 31:15 mondata: TAHOT és `elofordulasok.tsv:60`.

**40.** (a 2Móz 15:5 1/a-ja) — rendben. `elofordulasok.tsv:34`: „a versbeli »mélység« viszont más szót, a tenger mélyét jelentő mecólát fordítja, így a magyar »mélység« itt nem a motívum szava”. TAHOT 2Móz 15:5: H8415 (te.ho.Mot) és H4688 (m.tzo.Lot); Károli: „Elborították őket a hullámok, kő módjára merültek a mélységbe.”

**41.** (TEREMT-001.md:131; Jel 20:1-3) — a számok rendben, egy **kérdés (2).**
   - Rendben: `adat/jeloltek.tsv`, a Jel 20:1 és a 20:3 sora: „a Jel 20:1-3 sor kettéválasztása: szerkesztői döntés”, DT-F239d. A Károli Jel 20:2-ben a mélység szava nem áll. Számolás: 35 + 9 = 44 vers; a 20:1-3 három versével 45.
   - „Hely nem került ki és nem került be. Két dolog változott. … egy hely volt … két hely lett”. A helyek száma így 42-ről 43-ra nőtt, miközben az előző mondat szerint hely nem került be. Érti-e az olvasó, hogy bontásról van szó, nem új helyről?

**42.** (TEREMT-001.md:15) — rendben. A kilenc G0012-sor kiadás-oszlopa mind `NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz` (`TAGNT_kivonat.tsv:37558, 90397, 135464, 135470, 135681, 136400, 139129, 140581, 140618`). Ez magára a szóra áll; a Jel 20:3 környező szövegében van TR-eltérés (l. 18. tétel).

**43.** (TEREMT-001.md:85; Zsolt 106:9, Ézs 51:10, 5Móz 33:13) — rendben, egy megjegyzéssel (1), apró.
   - Rendben: Zsolt 106:9 „vivé őket a mélységeken”; 5Móz 33:13 az áldásban. A bekezdés olvasatként jelölt („Az itt képviselt olvasat”).
   - Az Ézs 51:10-ben az út „a tenger feneke”: „a ki a tenger fenekét úttá változtatta”. A nagy mélység vizeit a vers kiszárítja, nem úttá teszi.

**44.** (elofordulasok.tsv:67; Jel 9:11) — az idézet rendben (szó szerint a Károli Jel 9:11). **Kérdés (1):** „A mélységnek itt uralkodója van”. A vers szerint a sereg királya a mélység angyala („Királyukul …”, „ἐπ᾽ αὐτῶν βασιλέα”), nem a mélység uralkodója. L. 29. tétel.

#### A legsúlyosabb kérdések
- **Jel 20:3, a TR olvasata** (18., 27., 30.): a lap saját mércéje szerint a zárás tárgya a sárkány, nem a mélység.
- **„Isten megnyitja és bezárja”** (17., 18., 21.): az 1Móz 7:11 és 8:2 igéi szenvedők, cselekvő nélkül.
- **A „felhoz” a Jón 2:6-nál** (24.): az érvnapló elvetette, a Kivonat és a Drash mégis mondja.
- **A „szóbeli kapcsolat nincs” érv** (36.): az érvnapló elvetett érvét idézi fel.
- **A „nagy mélység” ötödik verse** (25.): a Zsolt 78:15-öt sem a BDB, sem a Károli nem támasztja alá.

`(proveniencia: scope=motivumok/TEREMT-001.md rések: kivonat :11–17, miert_fontos :45–61, ertelmezes :71–101, modszertan :129–142 + adat/elofordulasok.tsv (id=TEREMT-001, 43 sor: 30–71, 253) + adat/jeloltek.tsv (Jel 20:1, 20:3) + adat/visszhang_megfelelok.tsv (TEREMT-001 lxx-sorok) + adat/bdb_vers_jelentes.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv (H8415, G0012) + konkordancia/BDB_teljes_unabridged.tsv (H8415), BDB_rokon_irasok.tsv, TAHOT_kivonat.tsv (H8415: 36 sor; 13 teljes vers), TAGNT_kivonat.tsv (G0012: 9 sor; Jel 9:1, 9:11, 20:3), Karoli_1908.tsv (52 vers), LXX_OS/{exodus,genesis,deuteronomy,ezekiel,job-lxx,psalms-lxx}.tsv (11 vers) + naplok/ERVNAPLO_TEREMT-001.md + a 44 tételes tétellista; nem olvasva: naplok/ALLITAS_*, naplok/F239_U4_lektor_munkafajl.md, az átadók | forras=modell:claude-fable-5-2 | ts=2026-11-23T16:37Z)`

## 3/b. Olvasói átolvasás (DT824; az integrátor döntése, 2026-11-23)

### (a) Minta-kapu a renderelt lapon

`python eszkozok/olvasoi_kapu.py TEREMT-001 --reszletes --lexikon-konyvtar <előnézet>/lexikon`: a MINTA-szabály **1 BUKÁS** (cél: 0): 1059. sor, „szakszó: jelölt — **Kereszthivatkozásból minősített jelölt:** ehhez a motívumhoz nincs.” — generált szöveg. A kapu összesen 7 BUKÁS-t ad, mind generált részben (ZAROJEL 663, MINTA 1059, ANGOL és MUNKASZO 1248 — a Bekken-cím, N-F239b —, MUNKASZO 1290, MI_HANG 1312, LISTA_NEVELO 1324), a prózában 0; 23 FIGYELMEZTETÉS.

### (b) Friss olvasó a teljes lapon (szó szerint)

*Általános ügynök, Fable, brief és döntéslista nélkül; bemenet: a renderelt lap blokkjelekkel (1799 sor, 373 blokkjel). A válasz változtatás nélkül.*

Modell-ellenőrzés: a ténylegesen futott modell `claude-fable-5-2`. A lapot elejétől végéig elolvastam (1799 sor, minden blokk); a HTML-nézetet nem nyitottam meg, a rejtett `<!-- … -->` megjegyzéseket nem tekintettem a lap részének. Fájlt nem írtam és nem módosítottam.

| # | blokkjel | szó szerinti idézet (rövid) | mi a gond |
|---|---|---|---|
| 1 | [fej·1] | „📖 TEREMT-001 — Tehóm…” | idegen: a belső azonosító a főcímben áll, noha a [fej·5] szerint a Kolofonba tartozik. |
| 2 | [fej·2], [Kolofon·8] | „Szavas motívum” / „Azonosság típusa: lexikai” | idegen: ugyanarra két különböző, magyarázat nélküli szakszó. |
| 3 | [fej·3], [fej·4] | „…és mi nem.** az igehelynek a … gyököt kell tartalmaznia” | tört: a mondat kisbetűvel indul, pont nélkül ér véget (a [fej·4] is), és „gyök” áll „szó” helyett. |
| 4 | [fej·3], [1·5], [4·6], [4·84], [9·1]–[9·9] | „az 1Móz 1–8 láncára három versben tartozik”, „lánc-szó”, „a Genezis lánca” | idegen: a „lánc” sehol nincs meghatározva, és nem derül ki, miért három vers, ha a Genezisben négy hely van. |
| 5 | [fej·4], [Kolofon·8] | „lexémán kívül” | idegen: nyelvészeti szakszó magyarázat nélkül. |
| 6 | [fej·5] | „Az azonosító és technikai adatok (azonosító, téma, …” | ismétlődő: az „azonosító” a zárójelben újra áll. |
| 7 | [Kivonat·4], [11·2] ↔ [1·9], [3·2], [3·6] | „95 más versben” ↔ „94 vers” | ellentmondás: ugyanarra a csoportra (a Károli mélység-szava más szót fordít) két szám áll. |
| 8 | [1·9], [1·10], [3·2], [3·6], [Kivonat·4] ↔ [4·100], [11·2], [3·9] (Jób 41:31) | „(3 vers)” ↔ „négy versben ott is abüsszoszt hoz” | ellentmondás: a Septuaginta többlete hol 3, hol 4 vers; a Jób 41:31 más ok alatt áll, bár a sora szerint ott is a görög hozza a szót. |
| 9 | [Jelmagyarázat·4] | „(a PaRDeS-gyorsreferencia)”; „Sod — fegyelmezett, csak szövegből levezethető, gematria/allegorizálás nélkül” | érthetetlen: belső dokumentumra utal, és a Remez/Sod meghatározása szabály, nem magyarázat. |
| 10 | [Jelmagyarázat·4], [10·2] | „Drash — normatív, következtető, alkalmazó” ↔ „a Drash azt, mit tanít” | ismétlődő: a négy szint kétszer van elmagyarázva, eltérő szavakkal. |
| 11 | [Jelmagyarázat·6] | „az adatséma szerint szabad szöveg (nincs zárt értékkészlet)” | idegen: adatbázis-szóhasználat. |
| 12 | [Jelmagyarázat·7] ↔ [12·5] | „Tyndale Bible Encyclopedia — Strong's Hebrew/Greek” ↔ „Tyndale Brief lexicon of Extended Strongs” | ellentmondás: a TBESH/TBESG kétféleképp van feloldva. |
| 13 | [Jelmagyarázat·7]; használva: [2·4], [2·5], [2·7], [4·28], [4·32], [4·78], [6·3] | „TAHOT”, „DBH”, „DNTG”, „SECE”, „Mounce-glossza”, „MEK 00161”, „Strong”, „Masoretic Text”, „TWOT … — csak számhivatkozás” | idegen: a lapon használt rövidítések hiányoznak a feloldásból, vagy angolul maradtak. |
| 14 | [Jelmagyarázat·9], a 4.2 alcímek ([4·10], [4·45] fölött) | „4.2 mélységi szócikk” | érthetetlen: nem derül ki, mit jelent, és a „mélység” szócikkében félreérthető. |
| 15 | [Jelmagyarázat·9], [4·91] ↔ a 4. szakasz vége | „4.13 Károli-megfelelők; 4.14 rejtett / hamis párhuzam” | ellentmondás: a beharangozott 4.13 és 4.14 pont nincs a lapon, a 4.11 alatt pedig csak cím áll. |
| 16 | [Jelmagyarázat·10]; pl. [2·3], [4·11], [4·34], [9·4] | „az alatta álló dőlt, technikai mondat a szócikk készítőinek szól” | idegen: az olvasó készítőknek szóló mondatokat kap, minden szakaszban. |
| 17 | [Jelmagyarázat·11] | „melyik adattáblából vagy lekérdezésből… rejtett megjegyzésként áll” | idegen: belső munkafolyamat leírása. |
| 18 | [1·5] | „A keresések és az ajánlások együtt, a motívum helyeivel” | érthetetlen: „ajánlásokról” sehol nincs szó; a 44 + 136 + 44 → 144 átfedése sincs megmagyarázva. |
| 19 | [1·7] | „1.2. lépés minden találata”; „a tartomány-soroknál több vers egy helyen” | idegen: az 1.2 pont, nem lépés; a „tartomány-sor” belső szó. |
| 20 | [1·7], [1·8], [3·2] | „44 … + 96 … + 4 … = 144” | ismétlődő: a táblázat számai alatta mondatban, majd a 3. szakaszban újra. |
| 21 | [1·9], [1·10], [3·6], [3·9] | „nem a tehómot és nem az ἄβυσσος-t fordítja” | idegen: a görög szó ragozva, kiejtés nélkül áll a magyar átírás mellett, sorról sorra. |
| 22 | [1·9], [1·10], [3·6] | „vagy a görög szöveg a héberen túl ismétel” | érthetetlen. |
| 23 | [1·9], [3·6], [3·9] (Jób 42:8), [11·2] | „a feldolgozás a könyv nevét elhagyta”; „adathiba:” | idegen: a készítés belső hibájának leírása az olvasónak. |
| 24 | [1·9], [1·10] | „Példák (a Károli-szöveggel):” egyetlen versnél; „A kizárt helyek mellékletében is.” | tört: többes szám egy versre, és ige nélküli csonka mondat. |
| 25 | [1·9] ↔ [1·10] | „a Septuaginta többlete, a héberben nincs tehóm — 1 vers” / „— 2 vers” | érthetetlen: ugyanaz az ok „csoportosan” és „egyenként” is szerepel, indok nélkül. |
| 26 | [1·11] | „8 hely: 8 az Újszövetségben.” | ismétlődő: a mondat önmagát mondja. |
| 27 | [1·11] ↔ [2·10], [2·12] … [2·94] (minden „Funkció:” blokk) | „a motívum első helye: a mélység a teremtés kezdetén…” | ismétlődő: mind a 43 mondat szó szerint kétszer áll a lapon. |
| 28 | [1·11], [5·4] ↔ [2·4] | Jób 41:32 a lista végén; Hab 3:10 a Jón 2:6 előtt | ellentmondás: a helyek sorrendje a három felsorolásban eltér. |
| 29 | [1·12], [2·2] | „(nem magas megbízhatóságú azonosítás) … (közepes)” | érthetetlen: nincs megmondva, mitől közepes az az öt hely, ha a szó ott áll. |
| 30 | [1·13] (4–6. tétel) | „A Róm 10:7 cseréjének forrása. Az tény, hogy Pál…” | tört: a „nyitott kérdés” tényállítással ér véget, a kérdés hiányzik. |
| 31 | [1·13] ↔ [10·12], [10·14], [10·16], [10·18], [11·6] | „A vallástörténeti kutatás egy része a tehóm szót…” | ismétlődő: a hat tétel nyitómondatai szó szerint visszatérnek. |
| 32 | [2·2], [3·2], [4·37], [4·73], [4·86], [5·2], [6·2], [6·21], [8·2] | „**Következtetés:** főként ószövetségi; az Újszövetségben 8 hely.” | ismétlődő: a „Következtetés” az előtte álló mondatot mondja újra. |
| 33 | [2·3], [2·4], [2·5], a 2.1 alcím | „a Károli-szöveggel (2.1)”; lábjegyzet „2.1”; „2.1. Az igehelyek szövege” | érthetetlen: ugyanaz a szám alcímet és lábjegyzetet is jelöl. |
| 34 | [2·3], [2·7], [8·3], [4·17] | „(szerkesztői döntés, 2026-10-19)” | idegen: belső döntésre hivatkozó dátumos jelölés. |
| 35 | [2·4], [4·49] ↔ [4·54], [4·57], [4·59], [4·98] | „örvény · 5” (az 1Móz 1:2-nél is) ↔ „A harmadik a kezdet ősóceánja: az 1Móz 1:2” | ellentmondás: a táblázat szinte minden helyet az 5. jelentéshez („örvény”) köt, a szótár és a lap prózája öt külön jelentésre osztja őket. |
| 36 | [2·5] (2.1 jegyzet) ↔ [4·49] | „a BDB az 5. szakaszban maga idézi a helyet” ↔ „a jelentéspont gépi hozzárendelése kétes” | ellentmondás: ugyanaz a hozzárendelés egyszer igazolt, egyszer kétes. |
| 37 | [2·4] | „magas · szó-szintű-gépi”, „tartalom-alapú” | idegen: belső kódérték. |
| 38 | [2·4] (Jób 38:16, 38:30, 41:32) | „— *(ÓSZ; nincs DBH-hivatkozás: versszámozás-eltérés, az MT-vers a táblában nincs megadva)*” | idegen: feldolgozási hibaüzenet a cellában. |
| 39 | [2·4], [2·5] (2.2, 2.3 jegyzet) | „*(nincs hozzárendelés)*”; „a szerkesztői jelentésszám nincs leképezve a szótár tagolására” | idegen: belső állapotjelzés; a [4·49] a Zsolt 106:9-hez mégis ad jelentést. |
| 40 | [2·4] (Róm 10:7, Jel 9:11) | „ἄβυσσον; (abüsszon)”, „ἀβύσσου· (abüsszú)” | tört: a szóhoz írásjel tapadt. |
| 41 | [2·4] | a „2.1” jel soronként kétszer | ismétlődő: ugyanaz a lábjegyzet minden sor két cellájában. |
| 42 | [2·4], [2·7], [4·8], [4·9], [4·19], [4·28] és tovább | „[ⓘ](/szo/H8415)”, „szónézet” | idegen: a „szónézet” sehol nincs megmagyarázva. |
| 43 | [2·7] | „(az UBS Dictionary of Biblical Hebrew, a Károli-vers az MT-számozásra képezve, a Károli-versmegfeleltetés)”; „áll (fordításra vár) jelöléssel” | tört: a zárójel a mondatot ismétli, szerkezete szétesik. |
| 44 | [2·9] … [2·93] | pl. [2·25]: a vers dőlten, majd teljes egészében idézőjelben újra | ismétlődő: a vers szövege kétszer áll egymás alatt, utána a „Funkció” harmadszor foglalja össze. |
| 45 | [2·35] | „A hasonlat a magasság és a mélység két végpontjával méri…” | ismétlődő: az előző mondatot mondja újra. |
| 46 | [3·2], [3·7], [3·8], [3·11] | „A vizsgált helyek forrása (vers): A szavak keresése 98, Szerkesztői felvetés 2.” | tört: címkeszerű csonka mondat, háromszor megismételve. |
| 47 | [3·3] ↔ [1·8] | „32 elutasított vagy nyitva maradt vizsgált sorát” ↔ „Döntés nélkül maradt vers: 0” | ellentmondás: van-e nyitva maradt hely. |
| 48 | [3·6] ↔ [1·9], [1·10] | „A Károli „mély”, „mélység”, „örvény” vagy „fenékig” szava…” | ismétlődő: az okok leírása szó szerint ugyanaz; a harmadik ok ráadásul kisbetűvel kezdődik. |
| 49 | [3·9] | „A motívumba csak az a hely tartozik, ahol a héber szövegben a tehóm, az Újszövetségben az ἄβυσσος áll.” | ismétlődő: 29 sor végén áll szó szerint. |
| 50 | [3·9] | „a csoportosan kizárt 1 vers közül az első” + „A sor 1 verset foglal össze (az igehely az első közülük)” | ismétlődő: két oszlop mondja ugyanazt, egy versnél értelmetlenül. |
| 51 | [3·9] | „főként a(z) βάθος”; „a Károli „mély” csoportjának szava” | tört: bent maradt „a(z)”, és érthetetlen „csoportjának szava”. |
| 52 | [3·9] | 1Kir 4:29, 1Kor 2:10, 1Móz 2:21, 1Sám 17:49 … | érthetetlen: a sorrend ábécé szerinti, és a sor többi verse nem látszik. |
| 53 | [3·9] (Ézs 44:27) | „A Septuaginta többlete…: A sor 1 verset foglal össze…: a Septuaginta többlete: a görög…” | ismétlődő: az ok a cellán belül kétszer áll, a másik oszlop viszont „a Károli magyar szavát” mond oknak. |
| 54 | [3·12] | „Kereszthivatkozás-napló kutatói minősítése” | idegen: belső munkaanyag neve. |
| 55 | [3·12] ↔ [6·26] | ↔ „Kereszthivatkozásból minősített jelölt: ehhez a motívumhoz nincs.” | ellentmondás: a 2Pét 2:4 és a Jel 21:1 éppen onnan került vizsgálatra. |
| 56 | [3·12] | „görög mitológiából kölcsönzött terminus”; „„Isten fiai / gibborim-nefilim” motívumhoz” | érthetetlen: a szó nincs megnevezve, a hivatkozott motívum ismeretlen. |
| 57 | [3·12] | „Csak tematikus párhuzam, lexikai kapcsolat nélkül: nem lexikai rokona … — tematikus, nem lexikai párhuzam” | ismétlődő: egy cellában háromszor ugyanaz. |
| 58 | „Görög szavak: G0012”, „Héber szavak: H8415” alcím; [4·7], [4·30], [4·42] | „A motívumot hordozó görög szavak: ἄβυσσος”; „(ἄβυσσος (abüsszosz))” | idegen: kódszám a címben, többes szám egyetlen szóra, kettős zárójel. |
| 59 | [4·4], [4·5] | „a görög fordítás (Septuaginta) az a szava, amely a héber szó verseiben a legjellemzőbben áll vele együtt” | érthetetlen: szétesett mondat; a görög szó „LXX-megfelelője” a táblában héber. |
| 60 | [4·6], [4·74] | „versszintű együtt-előfordulás … nem szavankénti megfeleltetés” | érthetetlen. |
| 61 | [4·10], [4·11] ↔ [4·45], [4·46] | „bármelyik szón áll a motívum sora” | ismétlődő: a két bevezető szinte azonos, és ez a tagmondat érthetetlen. |
| 62 | [4·13], [4·14] | „→ a szócikk egésze — a klasszikus görögben melléknév” | érthetetlen: jelentésként egy nyelvtani megjegyzés áll. |
| 63 | [4·18] | „melléknév, (ος, (a ὁ βύσσος = βυθός szóból), feneketlen” | tört: nyitva maradt zárójel. |
| 64 | [4·18] | „πλοῦτος ἄβυσσος, Aeschylus, a Septuaginta (931) 950” | érthetetlen (félrevezető): Aiszkhülosz művének helyén „a Septuaginta” áll. |
| 65 | [4·18] | „B. D. American edition under the word”; „[ET]”; „Act. Thom.32ὁ τήν” | idegen: angol maradék, feloldatlan jel, egybetapadt szöveg. |
| 66 | [4·11] ↔ [4·18], [4·57] | „kiemelve áll minden vers, amely a motívum helye” ↔ az 5Móz 8:7, a Jób 41:32, a „42:8” kiemelés nélkül; „Zsolt 70:20” | ellentmondás: nem minden motívumhely kiemelt; a Zsolt 71:20 jelöletlen görög számozással áll. |
| 67 | [4·28] ↔ [4·22], [4·26] | „a Louw–Nida-doménsor a 4.4 pontban” | ellentmondás: a doménsor a 4.2 alatt áll. |
| 68 | [4·23], [4·24], [4·26], [4·66], [4·69] | „magyar szócikkcímei” ↔ „*abyss, bottomless pit* *(fordításra vár)*”; „Regions Below the Surface of the Earth” | idegen: angol maradék ott, ahol a bevezető magyar címeket ígér. |
| 69 | [4·23] ↔ [Kolofon·19] | „a szócikkek a szónézetben olvashatók” ↔ „a szócikkek szövegét nem közli” | ellentmondás. |
| 70 | [4·27]–[4·28], [4·35]–[4·36], [4·40]–[4·41], [4·70]–[4·71], [4·82], [4·89]–[4·90] | „A szó magyaros kiejtése.” → „**ἄβυσσος (abüsszosz)** · G0012” | ismétlődő: több pont csak a címszót ismétli vagy máshová utal, saját tartalom nélkül. |
| 71 | [4·29] = [4·72]; [4·5], [4·30], [4·73], [4·100], [5·2], [5·6] | „szócsalád szerint 30/35 vers” | ismétlődő: a bevezető szó szerint kétszer, a 30/35 arány nyolc helyen áll. |
| 72 | [4·29], [5·2] | „szóhíd egy szón át vezet”; „ezek 35 megállapított versében” | érthetetlen. |
| 73 | [4·34] = [4·80] | „a Strong-szám a TBESG/TBESH lemmájából vagy a SECE címszavából párosul” | ismétlődő: ugyanaz a technikai jegyzet kétszer. |
| 74 | [4·33] ↔ [3·9] (Jób 36:16) | „רַחַב · rachav · szélesség” ↔ „רַחַב (rahab, „tág tér”)” | ellentmondás: a szó kiejtése és jelentése eltér; a tehóm írásképe is más („תְּהֹום”). |
| 75 | [4·37], [4·39]; [4·86] | „egyikének jelentése sem egyértelmű a helyén” ↔ „a motívum helyeinek többségén egyértelmű” | ellentmondás egy bekezdésen belül, mindkét nyelvnél. |
| 76 | [4·86] ↔ [4·88], [2·4] | „nem egyértelmű … (Jób 38:16, 38:30, 41:32)” ↔ „3 helyen nincs hozzárendelés” | ellentmondás: a kétértelműség és a hiányzó adat nem ugyanaz. |
| 77 | [4·48], [4·56], [4·61] ↔ [4·98] | „2. *(külön meghatározás nélkül)*”; csupasz „**2**”, „**5**” ↔ „A második a tenger mélye” | ellentmondás: a 2. jelentésnek hol nincs, hol van meghatározása. |
| 78 | [4·52] | „(Albr ZAW xvi (1896), 62 Kö ii. 2. 167 Ency. Bib. DEEP)”; „status constructus”; „(de l. lent 5)” | idegen: feloldatlan szakirodalmi rövidítések és latin nyelvtani szavak. |
| 79 | [4·53], [4·54], [4·59] | „(hivatkozás nélkül)” ↔ alatta az 1Móz 49:25; „5Móz 33…”, „Pél…” | tört: a címke ellentmond a tartalomnak, a szöveg vers közepén megszakad. |
| 80 | [4·57] | „׳אֶלת־קוֺרַא‎ 42:8 (\|\| גַּלִּים מִשְׁבָּרִים,;” ; „(költemény a J-ben”, „(P;” | tört: torz héber és „,;”; a „\|\|”, a „J” és a „P” jel magyarázat nélkül. |
| 81 | [4·62] | „2. 5. örvény (si vera lectio): … [תַּחְפֻּכָה] l. הפך. תָּו l. תוה. alább…” | tört: kettős számozás, latin megjegyzés, a végén más címszavak utalói. |
| 82 | [4·75], [5·4] ↔ [4·100] | „Πόντος (Pontosz) … Pontusz” ↔ „„tenger” (pontosz, πόντος)” | ellentmondás: a „tenger” szó a táblázatban a Pontusz tartomány neveként áll. |
| 83 | [4·75], [4·76] | „(ebből 35 vers görög tartalmi szóval)”; „ῥήγνυμι · erőszakosan ledobni”; „· H8415”; „Forrás: a grammatikai szavak listája.” | idegen: gépi kifejezések és árva kód; a „forrás” nem forrás. |
| 84 | [4·84] ↔ [4·85]; [9·6] | „rokon nyelvi alakjai … (akkád/asszír, arab, …)” ↔ „BDB-szócikkben nincs rokon nyelvi adat” | ellentmondás: a bevezető adatot ígér, a táblázat üres, és a [9·6] is ide küld. |
| 85 | „Nyelvfüggetlen szerepek”, „Miért fontos ez a lelet” alcím; [9·2], [Kolofon·7] | „szerepek”, „lelet”, „nem negatív lelet” | idegen: belső munkaszavak címben és szövegben. |
| 86 | [4·93] | „(0 tiltott téma)”; „a döntés és a kimaradt témák indoka: a tematikus index döntései” | idegen: belső szabály és belső tábla neve, csonka mondatban. |
| 87 | [5·4] ↔ [4·100] | „1Móz 49:25 … γῆ (gé) · föld: bolygó … eltérő” ↔ „a görög átfogalmaz, és a mélység szava nem áll a versben” | ellentmondás: a táblázat megfelelőt ad ott, ahol a próza szerint nincs. |
| 88 | [5·4] | „ἄβυσσος (ἄβυσσος, abüsszosz)” | ismétlődő: a szó a zárójelben újra áll; kiejtés csak az alak első előfordulásánál van. |
| 89 | [5·4], [5·5], [5·6] | „*(társítás)*”; „LXX-minusz=0, a megfelelő nincs megállapítva=0, versszámozás miatt nem párosítva=0” | idegen: belső kategóriák, nullás értékekkel is kiírva. |
| 90 | [6·3] | „legalább 15 olvasói szavazatot kapott utalásaival”; „(MEK 00161) nem erősíti meg”; „1 hely … ezért ezekre a vizsgálat nem keres” | érthetetlen: nem tudni, kinek a szavazata és mi a MEK-szám; egy helyre többes szám utal. |
| 91 | [6·21], [6·25] ↔ [6·18], [6·6] | „A 36 utalásból 1 a motívum két saját helyét köti össze” ↔ „Jel 20:1 → Károli-KH: Jel 9:1”, „5Móz 33:13 → 1Móz 49:22-26” | ellentmondás: további utalások is a motívum saját helyére mutatnak; ugyanitt „a 5%-a”. |
| 92 | [6·23], [6·26] | „Kereszthivatkozásból minősített jelölt” | idegen. |
| 93 | [7·2], [7·3], [7·7]; [7·5] | „Ehhez a motívumhoz nincs rögzített kapcsolat.”; „miért kapta a fenti kapcsolat…” | ismétlődő: háromszor ugyanaz, és az „Alátámasztás” nem létező kapcsolatot magyaráz. |
| 94 | [7·2] ↔ [2·16], [2·24], [6·25], [10·6] | „még nincs ilyen” | érthetetlen: a lap máshol sorra összeköti a helyeket (pl. 1Móz 49:25 és 5Móz 33:13). |
| 95 | [8·2], [8·5] | „1 kapcsolat 1 másik motívummal (ALVIL-001 1), mind „közös igehely”; további 1 döntésre vár.”; „(ISTENTISZT-001: 1)” | idegen: motívumnév helyett azonosító, távirati mondatban. |
| 96 | [8·3] | „(minden sor mögött beépített motívumközi döntés áll, szerkesztői döntés, 2026-10-19)” | idegen: belső folyamat, két egymás utáni zárójelben. |
| 97 | [8·4] | „Mért: közös vers…; mindkét vers előfordulás a saját motívumában”; „Itt \| Ott” | érthetetlen. |
| 98 | [Kivonat·5] ↔ [8·4], [8·5] | „Két szomszédos motívum érintkezik vele … tohu va-vohu …, amely külön motívum” | ellentmondás: a 8. szakaszban a tohu va-vohu motívuma nem szerepel, helyette egy meg nem nevezett áll. |
| 99 | [9·2] | „A lánc 1 kulcsszava a motívum helyeit összekötő egyes héber szavak, soronként egy (az 1.2 teljes szólistája ennél bővebb: szópárokat … is felsorol)” | tört: nyelvtanilag szétesik, és az 1.2 nem sorol fel szópárokat ([1·4]). |
| 100 | [9·3] ↔ [5·4], [5·6] | „a láncon kívüli 30 versből 25 versben (83%)” | ellentmondás: 35 versből 3 a láncé, tehát 32 marad, és ebből az 5. szakasz szerint 27 egyezik. |
| 101 | [9·4], [9·9] | „(n/N)”; „40% alatt a láncban választott szó (félkövér)”; „ez szóegyezés, nem tipológiai állítás” | idegen: mérési küszöbök és módszertani kikötések az olvasónak. |
| 102 | [9·7] | „A motívum lexikai újszövetségi helyein a lánc görög szavai állnak… Az 1 görög szócsaládból 1 esetében” | érthetetlen. |
| 103 | [9·10], [9·11], [9·12] | „(a Chain Lineage Browser adata)”; „*(együtt-idézés)*”; „lekérdezve: 2026-11-23” | idegen: angol nevű eszköz magyarázat nélkül, lekérdezési dátummal. |
| 104 | [9·10], [9·11] | „A motívum 11 helyén 16 tanú áll.” | ismétlődő: Jeromos sora két helynél szó szerint azonos, Euszébioszé háromszor, Szeverianoszé és a Mekhiltáé kétszer áll. |
| 105 | [9·11] | „Homily 10, on Psalm 76”; „HOMILIES ON GENESIS 1.1”; „[Sefaria] Mekhilta…”; „(Apologia)**”; „Glossa Ordinaria, *Glossa Ordinaria, jegyzet…*” | idegen: műcímek angolul és csupa nagybetűvel, forrásjel a címben, árva csillag, megkettőzött név. |
| 106 | [9·11] | „Zsolt 117:24”, „Zsolt 28:7”, „Psalm 76”; „1Móz 1:2, Péld 8:24, Jel 8:11” | érthetetlen: jelöletlen más számozás (a Károliban nincs Zsolt 117:24), és nem világos, mit mutat a versfelsorolás. |
| 107 | [9·11] | „Euszébiosz, *De ecclesiastica theologia* · görög · 3. sz.” | érthetetlen (félrevezető lehet): Euszébiosz e műve 4. századi. |
| 108 | [9·13]; [9·11] (Luk 8:31) | „ott áll tanúként, ahol jegyzete ugyanezt a kapcsolatot mondja ki” | érthetetlen: nem tudni, mi az „ugyanez”; a középkori glossza kor nélkül áll az „Ókori értelmezők” között. |
| 109 | [10·15], [10·17] | „lektorált forrás a vizsgált adatbázisokban nem került elő. (Keresve: OpenAlex, Crossref, 2026-11-23.)” | idegen: keresési napló a „Szakirodalom” helyén, kétszer. |
| 110 | [12·2], [12·4] ↔ [Kolofon·5] | „Hogyan hivatkozz erre a szócikkre” → „a Kolofon … bekezdésében áll” → „még nem idézhető” | ellentmondás: a szakasz idézési formát ígér, csak átutal, a Kolofon pedig megtiltja az idézést. |
| 111 | [12·5] | „LXX (Septuaginta — lxx-morph + GreekWordList szövegkorpusz) (a Septuaginta szövege, CC BY 4.0)” | érthetetlen: kettős zárójelek; a „szótárak” között a Septuaginta és a TSK is áll, a Thayer hiányzik. |
| 112 | [12·8] ↔ [Kolofon·12] | „Motívum előfordulás-táblája (adatoszlopok: CC BY 4.0…” | ismétlődő: a forráslista licencekkel együtt kétszer áll. |
| 113 | [12·8], [Kolofon·12] | „Funkciókapcsolók táblája”, „Tiltott fordulatok listája”, „Lap teljesség-mérése”, „a nyílt adatmagban”, „Targum (közkincs) (közkincs)” | idegen: belső munkatáblák neve forrásként. |
| 114 | [Kolofon·8] | „Mező \| Érték”, „ID”, „Negatív kritérium”, „Sablon-megfelelőség \| v14”, „Próza modellje \| nincs kiadva — feldolgozás alatt” | idegen: mezőnevek és verziókód; a „Státusz” és a „Kiadás” értéke azonos. |
| 115 | [Kolofon·8] ↔ [fej·2], [fej·4] | „A héber Biblia tehóm szava a föld alatti…” | ismétlődő: a meghatározás és a tágabb kör szó szerint a lap elejéről. |
| 116 | [Kolofon·6] | „a hangerőt (a közös szavak és szópárok)”; „a kizáró feltétel és a tágabb kör”; „keltezési réteg nincs” | érthetetlen: Hays kritériumai magyarázat nélkül, belső fogalmakra képezve. |
| 117 | [Kolofon·13]–[Kolofon·19] | „Data created by www.STEPBible.org based on work…”; „(`lexica` repó)”; „lexikonoldal” | idegen: angol licencmondatok és belső szavak keverve. |
| 118 | [Kolofon·2] ↔ [Kolofon·3]; [12·2] ↔ [12·3] | „A lap technikai adatai…” / „Ez a rész a motívum azonosító adatait…” | ismétlődő: a szakasz két egymás utáni bevezetője ugyanazt mondja. |
| 119 | [Jelmagyarázat·5], [1·6], [1·9], [8·4], [Kolofon·4], [Kolofon·7] | „TEREMT-001_KIZARASOK.md”, „ALVIL-001_TUDOMANYOS.md”, „../kozlemeny/MI_NYILATKOZAT.md” | idegen: a hivatkozások célja fájlnév (ha a nézetben látszik). |

Összesítés: 119 kérdés — idegen 36, ismétlődő 25, érthetetlen 23, ellentmondás 23, tört 12.

`(proveniencia: scope=TEREMT-001 lapja, az új generátor előnézete, teljes lap | forras=modell:claude-fable-5-2 | ts=2026-11-23T15:19Z)`

### (c) A `naplok/HIBA_MECHANIZMUSOK.md` lapot érintő nyitott mechanizmusai

| mechanizmus | a lapon | bizonyíték |
|---|---|---|
| M-CSERE (belső szöveg cserével olvasóivá) | **igen, nyitott** — belső kódérték, mezőnév, cellát ismétlő jegyzet, címke-ismétlés a generált blokkokban | a (b) lista 11., 19., 37.–39., 43., 50., 53., 57., 83., 89., 113.–114. tétele; minta-kapu 1059 |
| M-NYERS (a nyers forrás marad a bemenet) | **igen** — angol szótári maradék (Thayer, BDB, UBS), feloldatlan rövidítések | (b) 62.–65., 68., 78., 80.–81. tétel; olvasói kapu ZAROJEL 663 |
| M-RÁRAKÓDÁS (ugyanaz több helyen) | **igen, nyitott** — a generátor maga 68 ismétlődő szósort jelez a látható lapon (16+ szó); a Funkció-mondatok kétszer, a forráslista kétszer, a Kizárási ok 29 sorban | `general.py` figyelmeztetése (U4 futás); (b) 27., 31., 32., 44., 49., 71., 112., 115., 118. tétel |
| M-ZOLD (a zöld nem minőség) | védve: a „0 BUKÁS” helyett ez a lista megy a szerkesztőhöz; a CI a fejen piros (E41, F217) | `naplok/F239_jelentes.md`, 1. ellenőrzés |
| M-VAKFOLT (ellenőrizetlen réteg) | a nyílt rész („az új generátor olvasói kapuinak mérése a TEREMT-001-en”) ezzel a listával mérve: a kapu 7 BUKÁS-a mellett 119 olvasói kérdés, zömük generált blokkban | ez a szakasz |

A 3/b tételei nem a próza hatáskörei: a generált blokkok hibáinak gazdája az új lapgenerátor (F218a, a 218c-ig); a prózát érintők (pl. 7., 8. tétel: a „95” szám és a Septuaginta-többlet 3/4 verse) a lektorlista és az F2 hamis tételeivel együtt a próza gazdájáé.
