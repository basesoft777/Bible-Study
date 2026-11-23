# F239 U5-csomag — a TEREMT-001 lapja és nyitott listája a szerkesztő nézéséhez

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820), az adat a `e9e2a136` fejen. Bemenet: `naplok/F239_atado_U4b.md` („Az U5-csomag”), `naplok/F239_atado_U4.md` (1. pont), `naplok/KIADAS_TEREMT-001_lektor.md`. **A csomag tételt nem dönt el, csak a gazdát mutatja.** Prózát és adatot nem írtam.*

## A lapnézet

- **Fájl (a repón kívül, nem publikálva):** `C:\Users\bases\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_911d4923-53b0-4b46-9fc5-ccdde3608420\F239_U5_TEREMT-001_lapnezet.html` (373 blokkjel, mint a 3/b átolvasásban; a jelek a lenti lista jelei). A megjelenítés az integrátoré.
- **Előállítás:** `python.exe`-lista előtte (nem futott lapgen); a két ideiglenes kerülőút (`adat/motivum_kapcsolatok.tsv`: `DT-F239a` → `DT9991`; `kizart.py`: a 10-szeresnél kisebb arány-mondat kihagyva, N-F239a); `python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <közös jegyzetmappa>/F239_U5_elonezet` (47 mp, 0-s kilépés; a generátor 68 ismétlődő szósort jelez a látható lapon); utána mindkét fájl visszaállítva, a `git status` tiszta. A nézet a `lapnezet.epit()`-jével készült, a `lexikon/TEREMT-001_TUDOMANYOS.md` olvasását egy burkoló az előnézetre irányította (a fejlécben: „előnézet @ e9e2a136”).

## Összegzés

| csoport | gazda | tétel |
|---|---|---:|
| (a) a szerkesztő dönt | a szerkesztő | **29** (lektor 23, 3/b 6) |
| (b) javítandó, gazdával | a próza gazdája (U6) | **2** a listából (lektor 17., 3/b 7.) + 12 forrástétel (F2: 9, F1: 1, független ellenőr: 2), tájékoztatásul |
| (c) generátorhiba | a lapgenerátor (218c, #241, F241.8); két tétel más, már nyitott gazdánál | **112** (3/b) |
| összesen | | **143** |

**Eltérés a 142-től.** A lektor összesítője 23 kérdést mond, a lista szövegében viszont 24 tételnél áll „kérdés” jelölés (6., 8., 9., 10., 11., 12., 15., 17., 18., 20., 21., 22., 23., 24., 25., 27., 28., 29., 30., 36., 37., 38., 41., 44.). A csomag mind a 24-et hozza, így 24 + 119 = 143. A 13., 14. és 43. tétel „rendben”, apró megjegyzéssel; ezek nem kérdések, nincsenek a listán.

**A besorolás szabálya.** (b)-be csak az a listatétel kerül, amely teljes egészében ugyanazt az állítást kifogásolja, mint egy már hamisnak ítélt tétel. Ahol csak részben egyezik, a tétel az (a)-ban marad, és utalás mutat a (b)-re. A 3/b tétele akkor (a), ha a kifogás a prózát vagy a cikkhez írt adatszöveget érinti (az 1/a- és Funkció-mondatok, a tanúsorok, a motívumközi kapcsolatok). Ha a generált blokk összerakását, címkéjét, ismétlését vagy nyers forrásszövegét kifogásolja, a tétel (c).

## (a) A szerkesztő dönt — 29

### A lektor kérdései (23)

| # | hely | olvasói mondat |
|---|---|---|
| L6 | Módszertan (:140) | A mondat szerint a Ráháb, a sárkány és a vízi szörnyek helyein nincs ott a mélység szava, holott a Zsolt 148:7-ben és a Jób 41:32-ben ott áll. A szerkesztő dönti el, szűkül-e a mondat az Ézs 51:9-re, és maradhat-e a „lexikai keresés” kifejezés. |
| L8 | Remez (:81) | A Róm 10:7-nél a tény („hét versben áll együtt…”) és a nyitott kérdés („merít-e Pál”) egy mondatban áll. Kettéválik-e, ahogy a Vitatott pontban? |
| L9 | Peshat (:73) | „A mélység áldásai” az 5Móz 33:13-ra is hivatkozik, de ott a Károli nem áldást, hanem „mélységes vizeket” mond. Marad-e a közös megfogalmazás? (Ugyanaz a vers, mint az F1 79. sora, l. (b).) |
| L10 | Remez (:79) | A „négy hely négy különböző dolgot mond” olvasat, de nincs annak jelölve; a „későbbi könyvek ezeket hozzák vissza” pedig átvételt állít, ahol az adat csak szóismétlést mutat. Jelölést kap-e, és marad-e a mondat? |
| L11 | Vitatott pont (:97) | A „2Móz 15-ben a mélység a tenger része” érv nem szerepel az érvnaplóban, bár az adat alátámasztja. Bekerül az érvnaplóba, vagy kimarad a prózából? |
| L12 | Vitatott pont, Tiámat (:93) | A „nem cselekszik Isten ellen” csak a másik olvasat érveként áll. Az érvnapló szerint ez hiányérv, amely a „demitologizált átvétel” olvasattal is összefér. Kimondja-e ezt a próza? |
| L15 | Vitatott pont (:99) | A „hét versben áll együtt a leszállás vagy a felhozás igéjével” négy versre nem igaz így: ott az ige nem a mélységbe vagy a mélységből való mozgást mondja. Pontosodik-e a mondat? |
| L18 | Kivonat (:11) | A Jel 20:3-ban a Textus Receptus szerint a sárkányt zárják be, nem a mélységet, a Károli „bezárá azt” pedig kétértelmű. Hogyan bánjon a lap a TR olvasatával? (A tétel „Isten megnyit, bezár” része azonos a K36-tal, l. (b); a „zárt hely” része az L38-cal.) |
| L20 | Kivonat (:11) | „A mélység áldásaival, mely alant terül” két hivatkozással áll, de csak az 1Móz 49:25 szövege. Marad-e az 5Móz 33:13 hivatkozás? (Az F1 79. sorával rokon, l. (b).) |
| L21 | Sod (:87) | A „mélység határa mindig kívülről, felülről szabott” mind a 43 helyre szól, határról viszont csak néhány hely beszél, és az „Isten akaratából” következtetés. Szűkül-e? (Rokon: K36.) |
| L22 | Sod zárómondata | „A kulcs egyszer sem a mélységé”, holott a vers szövege „a mélységnek kulcsa”. Átfogalmazódik-e, és megjelenik-e a kikötés, hogy a kulcs és a nyit–zár a Jelenések általános szókincse? |
| L23 | Miért fontos (:59) | A „hullámok” szó csak a 2Móz 15:5-ben áll, a 15:8-ban „mélységes vizek”. Pontosodik-e a mondat? |
| L24 | Drash (:85) és Kivonat (:11) | A Jón 2:6-ban nincs „felhozás” (a 2:7 mondja, más szóval), és az érvnapló ezt a közös jegyet elvetette. Marad-e a Drash mondata? (A Kivonat-rész a K2-vel azonos, l. (b).) |
| L25 | Miért fontos (:47) | A „nagy mélység öt versben” ötödik verse, a Zsolt 78:15 sem a BDB, sem a Károli szerint nem egyértelmű. Négy vers vagy öt? |
| L27 | 2. szakasz, Jel 20:3 (Funkció-mondat) | „Itt bezárják és lepecsételik” a mélységet: ugyanaz a TR-kérdés, mint az L18-ban. |
| L28 | Miért fontos (:45–59) | A „Septuaginta” szó magyarázat nélkül áll, a szöveg máshol „görög Ószövetséget” mond. Azonosítja-e a kettőt a lap? (A tétel másik része, a BDB-helyek válogatás voltának jelzése, azonos a K19-cel és a K20-szal, l. (b).) |
| L29 | Remez (:81) | „A mélységnek királya van, a Vesztő (Jel 9:11)”: a vers szerint a sáskák királya a mélység angyala. Átfogalmazódik-e? |
| L30 | Vitatott pont (:95) | „Mindkét helyen a mélységet zárják be”: az 1Móz 8:2-ben a források záródnak, a Jel 20:3-ban (TR) a sárkány. Pontosodik-e? |
| L36 | Vitatott pont (:95) | A „szóbeli kapcsolat nincs” mondat visszahozza az érvnaplóban elvetett „közös zár-ige hiánya” érvet. Marad-e, és jelzi-e a próza, hogy gyenge az érv? |
| L37 | Kivonat (:11–17) | Az első bekezdés nyolc mondatban huszonegy igehelyet visz végig, a fordulópont a közepén áll. Tagolódik-e? |
| L38 | Kivonat fordulópontja | „Az Ószövetségben a tehóm víz” (a Zsolt 71:20-ban seól), és „az Újszövetségben az abüsszosz zárt hely” (a Róm 10:7, a Luk 8:31, a Jel 11:7 és a 17:8 nem zárásról szól). Mennyire általánosíthat a mondat? |
| L41 | Módszertan (:131) | „Hely nem került ki és be … két hely lett”: a helyek száma bontással nőtt 42-ről 43-ra. Érti-e az olvasó, hogy nem új helyről van szó? |
| L44 | 2. szakasz, Jel 9:11 (Funkció-mondat) | „A mélységnek itt uralkodója van”: a vers szerint a sereg királya a mélység angyala, mint az L29-ben. |

### Az olvasói átolvasás tartalmi tételei (6)

| # | jel | olvasói mondat |
|---|---|---|
| O5 | [fej·4] | A „lexémán kívül” a tágabb kör adatszövegében áll (a motívum határa). A szóhasználatról a szerkesztő dönt; a határ szövege a felhasználó hatásköre (DT938). |
| O8 | [Kivonat·4], [11·2] ↔ [4·100] | A Septuaginta többlete a prózában hol 3, hol 4 vers, és a Jób 41:31 más ok alatt áll. Melyik szám a helyes, és hova tartozik a Jób 41:31? |
| O45 | [2·35] (Zsolt 36:7, 1/a) | A „hasonlat a magasság és a mélység két végpontjával méri” mondat az előzőt ismétli. Marad-e? |
| O87 | [5·4] ↔ [4·100] | A táblázat az 1Móz 49:25-höz a γῆ-t adja („eltérő”), a próza szerint a görögben nem áll a mélység szava. Melyik mondat maradjon, vagy hogyan olvasható a kettő együtt? |
| O98 | [Kivonat·5] ↔ [8·4], [8·5] | A Kivonat két szomszédos motívumot ígér, köztük a tohu va-vohut; a 8. szakaszban az ALVIL-001 és egy döntésre váró ISTENTISZT-001 áll. A próza igazodjon, vagy a motívumközi kapcsolatok adata? |
| O107 | [9·11] | Euszébiosz *De ecclesiastica theologia* című műve „3. sz.” jelöléssel áll, de 4. századi. A tanúsor kora javítandó-e? (Valószínűleg adathiba a visszhang-táblában.) |

## (b) Javítandó, gazdával (U6) — tájékoztatás

*Ezeket a próza gazdája javítja az U6-ban. A szerkesztő a listán látja őket, döntés nem vár rá.*

### A listából (2)

| # | hely | olvasói mondat | forrás |
|---|---|---|---|
| L17 | Peshat (:73) | „Megnyitja és bezárja a forrásait (1Móz 7:11, 8:2)”: mindkét ige szenvedő, cselekvő nélkül. | = K36 |
| O7 | [Kivonat·4], [11·2] ↔ [1·9], [3·2], [3·6] | A próza „95 más versről” beszél, a generált rész „94 versről”, ugyanarról a csoportról. | = K9, K70, a független ellenőr „95”-je |

### A forrástételek (12)

| tétel | hely | olvasói mondat | a listán |
|---|---|---|---|
| F2 K2 | Kivonat (:11) | A Zsolt 33:7-ben nem a mélység a tárház (Isten tárházakba gyűjti); a Jónás nem költői könyv; a Jón 2:6 nem mond felhozást. | L24 (Kivonat-rész) |
| F2 K9 | Kivonat (:15) | A Károli-szavak felsorolásából hiányzik a „mély vizek”, és a „95” a teljes szócsaládra vonatkozik. | O7 |
| F2 K19 | Miért fontos (:47) | A BDB 1. jelentésének helyei teljes listának hatnak, pedig a BDB többet sorol be. | L28 (második rész) |
| F2 K20 | Miért fontos (:47) | Ugyanez a 2. jelentésre (tenger mélye). | L28 (második rész) |
| F2 K36 | Peshat (:73) | „Isten megnyitja és bezárja a forrásait”: az igék szenvedők, és az „ahol” túl általános. | L17; részben L18, L21 |
| F2 K47 | Remez (:81) | A Róm 10:6 nem „szó szerint” idézi a görög 5Móz 30:12-t (a ἡμῖν kimarad). | – |
| F2 K69 | Módszertan (:129) | A felsorolt öt szótári alak 125 versben áll; a 136-hoz további „mély-” alakok kellenek. | – |
| F2 K70 | Módszertan (:129) | A csoportosan kizárt versek száma 96, nem 95. | O7 |
| F2 K99 | 2. szakasz, 1Móz 7:11 (`elofordulasok.tsv`, kapcsolódás) | „A mélység forrásai a héberben csak itt és a 8:2-ben állnak együtt”: a Péld 8:24-ben is együtt áll a két szó. | – |
| F1 79. sor | Remez (`motivumok/TEREMT-001.md:79`) | „A mélység, mely alant terül” sem az 1Móz 49:25, sem az 5Móz 33:13 Károli-szövegével nem egyezik szó szerint; ezért piros az E41. | rokon: L9, L20 |
| független ellenőr | 1Móz 7:11 | „Csak itt és a 8:2-ben”: azonos a K99-cel. | – |
| független ellenőr | Kivonat (:15) | A „95”: azonos a K9-cel és a K70-nel. | O7 |

## (c) Generátorhiba — gazda: a lapgenerátor (218c) — 112

*Mind a 3/b-ből (a jelek a lapnézet jelei). Mechanizmusonként, a `naplok/HIBA_MECHANIZMUSOK.md` szerint: M-CSERE (belső szöveg, kód, munkaszó a látható lapon), M-NYERS (nyers forrásszöveg: angol maradék, feloldatlan rövidítés, más versszámozás), M-RÁRAKÓDÁS (ugyanaz több helyen, egymástól eltérő példányokkal). A naplóban nincs megfelelője két csoportnak; ezek **mechanizmus-jelöltek**, a naplóba nem írtam be őket: J1 (sablon-illesztés: az adatérték mondatba vagy cellába kerül nyelvtani és megjelenítési igazítás nélkül), J2 (rögzített utalás: szakaszszám, pontszám, fájlnév vagy beharangozott pont a tényleges szerkezettől függetlenül). Az N-tétel: N-F239c (`nyitott/uj/nervous-kare-9d2361.md`).*

| mechanizmus | tétel |
|---|---:|
| M-CSERE | 43 |
| M-RÁRAKÓDÁS | 30 |
| M-NYERS | 14 |
| J1 sablon-illesztés (jelölt) | 18 |
| J2 rögzített utalás (jelölt) | 5 |
| más, már nyitott gazdánál | 2 |

### M-CSERE (43)

| # | jel | olvasói mondat |
|---|---|---|
| O1 | [fej·1] | A főcímben a belső azonosító (TEREMT-001) áll, holott a lap szerint a Kolofonba tartozik. |
| O2 | [fej·2], [Kolofon·8] | „Szavas motívum” és „Azonosság típusa: lexikai”: ugyanarra két magyarázatlan belső kódérték. |
| O4 | [fej·3], [1·5], [4·6], [4·84], [9·1]–[9·9] | A „lánc” belső munkaszó, a lap sehol nem határozza meg, és nem derül ki, miért három versből áll a Genezis négy helyéből. |
| O9 | [Jelmagyarázat·4] | A Jelmagyarázat belső dokumentumra („PaRDeS-gyorsreferencia”) utal, a szintek meghatározása pedig a szerzőnek szóló szabály. |
| O11 | [Jelmagyarázat·6] | „Az adatséma szerint szabad szöveg”: adatbázis-szóhasználat az olvasónak. |
| O14 | [Jelmagyarázat·9], 4.2 alcím | A „mélységi szócikk” belső pontnév, és a mélység szócikkében félreérthető. |
| O16 | [Jelmagyarázat·10] és minden szakasz | A lap a készítőknek szóló dőlt technikai mondatokat mutat az olvasónak. |
| O17 | [Jelmagyarázat·11] | A belső munkafolyamat leírása („melyik adattáblából … rejtett megjegyzésként”). |
| O18 | [1·5] | Az „ajánlások” szó sehol nincs megmagyarázva, és a 44 + 136 + 44 → 144 átfedése sem. |
| O19 | [1·7] | „1.2. lépés”, „tartomány-sor”: belső szavak. |
| O23 | [1·9], [3·6], [3·9], [11·2] | „A feldolgozás a könyv nevét elhagyta”, „adathiba:”: a készítés belső hibája az olvasónak (Jób 42:8). |
| O29 | [1·12], [2·2] | A „közepes” megbízhatóság kódérték, magyarázat nélkül. |
| O34 | [2·3], [2·7], [8·3], [4·17] | „(szerkesztői döntés, 2026-10-19)”: dátumos belső döntésjelölés. |
| O37 | [2·4] | „magas · szó-szintű-gépi”, „tartalom-alapú”: belső kódérték a táblázatban. |
| O38 | [2·4] (Jób 38:16, 38:30, 41:32) | A cellában feldolgozási hibaüzenet áll („versszámozás-eltérés, az MT-vers a táblában nincs megadva”). |
| O39 | [2·4], [2·5] | „(nincs hozzárendelés)”, „a szerkesztői jelentésszám nincs leképezve”: belső állapotjelzés, miközben a [4·49] ugyanahhoz jelentést ad. |
| O42 | [2·4], [2·7], [4·8] és tovább | A „szónézet” szó sehol nincs megmagyarázva. |
| O43 | [2·7] | A zárójeles forrásnév a mondatot ismétli, és szétesik a mondat szerkezete. |
| O46 | [3·2], [3·7], [3·8], [3·11] | „A vizsgált helyek forrása (vers): A szavak keresése 98, …”: címkeszerű csonka mondat, háromszor. |
| O54 | [3·12] | „Kereszthivatkozás-napló kutatói minősítése”: belső munkaanyag neve. |
| O56 | [3·12] | A kutatói indoklás nyersen áll: a szót nem nevezi meg, ismeretlen motívumra utal. |
| O57 | [3·12] | Egy cellában háromszor ugyanaz („tematikus, nem lexikai párhuzam”): címke és indoklás egymásra rakva. |
| O58 | „Görög szavak: G0012” alcím; [4·7], [4·30], [4·42] | Kódszám a címben, többes szám egyetlen szóra, kettős zárójel. |
| O60 | [4·6], [4·74] | „Versszintű együtt-előfordulás … nem szavankénti megfeleltetés”: módszertani belső mondat. |
| O64 | [4·18] | „Aeschylus, a Septuaginta (931) 950”: a „Sept.” rövidítés cseréje Aiszkhülosz művét Septuagintává tette (félrevezető). |
| O72 | [4·29], [5·2] | „A szóhíd egy szón át vezet”: érthetetlen belső munkaszó. |
| O83 | [4·75], [4·76] | „(ebből 35 vers görög tartalmi szóval)”, árva „· H8415”, „Forrás: a grammatikai szavak listája”: gépi kifejezések. |
| O85 | „Nyelvfüggetlen szerepek”, „Miért fontos ez a lelet”; [9·2], [Kolofon·7] | „Szerepek”, „lelet”, „nem negatív lelet”: belső munkaszavak címben és szövegben. |
| O86 | [4·93] | „(0 tiltott téma)”, „a tematikus index döntései”: belső szabály és belső tábla neve. |
| O89 | [5·4], [5·5], [5·6] | „(társítás)”, „LXX-minusz=0, …”: belső kategóriák nullás értékkel. |
| O90 | [6·3] | „15 olvasói szavazat”, „MEK 00161”: magyarázatlan; egy helyre többes szám utal. |
| O92 | [6·23], [6·26] | „Kereszthivatkozásból minősített jelölt”: belső kategória (a minta-kapu 1059. sora). |
| O95 | [8·2], [8·5] | Motívumnév helyett azonosító (ALVIL-001), távirati mondatban. |
| O96 | [8·3] | Belső folyamat két egymás utáni zárójelben („beépített motívumközi döntés”). |
| O97 | [8·4] | „Mért: közös vers…”, „Itt \| Ott”: érthetetlen oszlop- és cellaszöveg. |
| O101 | [9·4], [9·9] | „(n/N)”, „40% alatt…”: mérési küszöbök és módszertani kikötések az olvasónak. |
| O103 | [9·10]–[9·12] | „Chain Lineage Browser”, „(együtt-idézés)”, „lekérdezve: 2026-11-23”: eszköznév és lekérdezési dátum. |
| O109 | [10·15], [10·17] | A „Szakirodalom” helyén keresési napló áll („Keresve: OpenAlex, Crossref…”), kétszer. |
| O111 | [12·5] | Kettős zárójelek; a „szótárak” között a Septuaginta és a TSK áll, a Thayer hiányzik. |
| O113 | [12·8], [Kolofon·12] | Belső munkatáblák neve forrásként („Funkciókapcsolók táblája”…), „(közkincs) (közkincs)”. |
| O114 | [Kolofon·8] | Mezőnevek, verziókód („Sablon-megfelelőség \| v14”); a „Státusz” és a „Kiadás” értéke azonos. |
| O116 | [Kolofon·6] | Hays kritériumai magyarázat nélkül, belső fogalmakra képezve („hangerő”, „keltezési réteg”). |
| O117 | [Kolofon·13]–[Kolofon·19] | Angol licencmondatok és belső szavak („`lexica` repó”, „lexikonoldal”) keverve. *(Az angol licencmondat a licencszöveg része lehet; a gazda dönti el, fordul-e.)* |

### M-RÁRAKÓDÁS (30)

| # | jel | olvasói mondat |
|---|---|---|
| O10 | [Jelmagyarázat·4] ↔ [10·2] | A négy PaRDeS-szint kétszer van elmagyarázva, eltérő szavakkal (a generált Jelmagyarázat és a próza). |
| O12 | [Jelmagyarázat·7] ↔ [12·5] | A TBESH/TBESG feloldása kétféle. |
| O20 | [1·7], [1·8], [3·2] | A táblázat számai alatta mondatban, majd a 3. szakaszban újra. |
| O25 | [1·9] ↔ [1·10] | Ugyanaz az ok csoportosan és egyenként is szerepel, magyarázat nélkül. |
| O27 | [1·11] ↔ [2·10]…[2·94] | Mind a 43 Funkció-mondat szó szerint kétszer áll a lapon. |
| O28 | [1·11], [5·4] ↔ [2·4] | A helyek sorrendje a három felsorolásban eltér. |
| O31 | [1·13] ↔ [10·12]…[10·18], [11·6] | A Vitatott pontok és a Nyitott kérdések nyitómondatai szó szerint visszatérnek az 1.5 pontban. |
| O32 | [2·2], [3·2], [4·37] és további 6 blokk | A „Következtetés:” az előtte álló mondatot mondja újra. |
| O36 | [2·5] ↔ [4·49] | Ugyanaz a jelentés-hozzárendelés egyszer igazolt, egyszer kétes. |
| O41 | [2·4] | Ugyanaz a lábjegyzet („2.1”) minden sor két cellájában. |
| O44 | [2·9]…[2·93] | A vers szövege kétszer áll egymás alatt, utána a Funkció harmadszor foglalja össze. |
| O47 | [3·3] ↔ [1·8] | „32 elutasított vagy nyitva maradt” ↔ „Döntés nélkül maradt vers: 0”. |
| O48 | [3·6] ↔ [1·9], [1·10] | Az okok leírása szó szerint ugyanaz; a harmadik kisbetűvel kezdődik. |
| O49 | [3·9] | „A motívumba csak az a hely tartozik…” 29 sor végén szó szerint. |
| O53 | [3·9] (Ézs 44:27) | Az ok a cellán belül kétszer áll, a másik oszlop pedig más okot mond. |
| O55 | [3·12] ↔ [6·26] | „Kereszthivatkozásból minősített jelölt: nincs”, holott a 2Pét 2:4 és a Jel 21:1 éppen onnan került vizsgálatra. |
| O61 | [4·10], [4·11] ↔ [4·45], [4·46] | A két bevezető szinte azonos, és a „bármelyik szón áll a motívum sora” érthetetlen. |
| O69 | [4·23] ↔ [Kolofon·19] | „A szócikkek a szónézetben olvashatók” ↔ „a szócikkek szövegét nem közli”. |
| O70 | [4·27]–[4·28] és további 5 pár | Több pont csak a címszót ismétli vagy máshová utal, saját tartalom nélkül. |
| O71 | [4·29] = [4·72]; nyolc blokk | A bevezető szó szerint kétszer, a „30/35” arány nyolc helyen. |
| O73 | [4·34] = [4·80] | Ugyanaz a technikai jegyzet kétszer. |
| O74 | [4·33] ↔ [3·9] (Jób 36:16) | A רַחַב kiejtése és jelentése két helyen eltér („rachav, szélesség” ↔ „rahab, tág tér”), a tehóm írásképe is más. |
| O91 | [6·21], [6·25] ↔ [6·18], [6·6] | „1 utalás köti össze a motívum két helyét”, holott további utalások is saját helyre mutatnak; ugyanitt „a 5%-a”. |
| O93 | [7·2], [7·3], [7·7]; [7·5] | Háromszor „nincs kapcsolat”, és az „Alátámasztás” nem létező kapcsolatot magyaráz. |
| O94 | [7·2] ↔ [2·16], [2·24], [6·25], [10·6] | „Még nincs ilyen” kapcsolat, miközben a lap máshol összeköti a helyeket (pl. 1Móz 49:25 és 5Móz 33:13). |
| O100 | [9·3] ↔ [5·4], [5·6] | „A láncon kívüli 30 versből 25 (83%)” ↔ az 5. szakasz szerint 32-ből 27. |
| O104 | [9·10], [9·11] | Ugyanaz a tanúsor több helynél szó szerint (Jeromos kétszer, Euszébiosz háromszor…). |
| O112 | [12·8] ↔ [Kolofon·12] | A forráslista licencekkel együtt kétszer áll. |
| O115 | [Kolofon·8] ↔ [fej·2], [fej·4] | A meghatározás és a tágabb kör szó szerint a lap elejéről. |
| O118 | [Kolofon·2] ↔ [Kolofon·3]; [12·2] ↔ [12·3] | A szakasz két egymás utáni bevezetője ugyanazt mondja. |

*A generátor maga 68 ismétlődő szósort jelez a látható lapon (`general.py`, a mai futás); a fenti tételek ennek olvasói oldala.*

### M-NYERS (14)

| # | jel | olvasói mondat |
|---|---|---|
| O13 | [Jelmagyarázat·7]; [2·4]…[6·3] | A lapon használt rövidítések (TAHOT, DBH, DNTG, SECE, MEK 00161…) hiányoznak a feloldásból, vagy angolul maradtak. |
| O40 | [2·4] (Róm 10:7, Jel 9:11) | A görög szóhoz írásjel tapadt („ἄβυσσον;”, „ἀβύσσου·”). |
| O62 | [4·13], [4·14] | Jelentésként nyelvtani megjegyzés áll („a klasszikus görögben melléknév”). |
| O63 | [4·18] | Nyitva maradt zárójel a szótári szövegben. |
| O65 | [4·18] | Angol maradék, feloldatlan „[ET]”, egybetapadt szöveg („Act. Thom.32ὁ τήν”). |
| O66 | [4·11] ↔ [4·18], [4·57] | Nem minden motívumhely kiemelt (5Móz 8:7, Jób 41:32, „42:8”), és a „Zsolt 70:20” jelöletlen görög számozás. |
| O68 | [4·23], [4·24], [4·26], [4·66], [4·69] | Magyar szócikkcímek helyett angol maradék („abyss, bottomless pit (fordításra vár)”, „Regions Below…”). |
| O77 | [4·48], [4·56], [4·61] ↔ [4·98] | A 2. jelentésnek hol nincs, hol van meghatározása (a BDB tagolása nyersen). |
| O78 | [4·52] | Feloldatlan szakirodalmi rövidítések és latin nyelvtani szavak („Albr ZAW xvi…”, „status constructus”). |
| O79 | [4·53], [4·54], [4·59] | „(hivatkozás nélkül)” címke alatt vers áll, és a szöveg vers közepén megszakad („5Móz 33…”, „Pél…”). |
| O80 | [4·57] | Torz héber, „,;”, és magyarázatlan jelek („\|\|”, „J”, „P”). |
| O81 | [4·62] | Kettős számozás, latin megjegyzés, más címszavak utalói a BDB-szövegből. |
| O105 | [9·11] | Műcímek angolul és csupa nagybetűvel, forrásjel a címben, árva csillag, megkettőzött név. |
| O106 | [9·11] | Jelöletlen más versszámozás („Psalm 76”), és nem világos, mit mutat a versfelsorolás. *(A mai előnézetben a „Zsolt 117:24” és a „Zsolt 28:7” már nem áll, F239.30; a „Psalm 76” igen.)* |

### J1 — sablon-illesztés (jelölt, 18)

| # | jel | olvasói mondat |
|---|---|---|
| O3 | [fej·3], [fej·4] | A mondat kisbetűvel indul és pont nélkül ér véget. *(A „gyök” a „szó” helyett a negatív kritérium adatszövege; a határ szövege a felhasználóé, DT938.)* |
| O6 | [fej·5] | „Az azonosító és technikai adatok (azonosító, …)”: az „azonosító” a zárójelben újra áll. |
| O21 | [1·9], [1·10], [3·6], [3·9] | A görög szó ragozva, kiejtés nélkül áll a magyar átírás mellett („ἄβυσσος-t”). |
| O22 | [1·9], [1·10], [3·6] | „Vagy a görög szöveg a héberen túl ismétel”: érthetetlen okszöveg. |
| O24 | [1·9], [1·10] | „Példák” egyetlen versre, és ige nélküli csonka mondat („A kizárt helyek mellékletében is.”). |
| O26 | [1·11] | „8 hely: 8 az Újszövetségben.”: a mondat önmagát mondja. |
| O30 | [1·13] | A „nyitott kérdés” tényállítással ér véget, a kérdés lemaradt (a Vitatott pont nyitómondatai kivágva). |
| O50 | [3·9] | Két oszlop ugyanazt mondja, egy versnél értelmetlenül („1 vers közül az első”). |
| O51 | [3·9] | Bent maradt „a(z)”, és érthetetlen „csoportjának szava”. |
| O52 | [3·9] | A sorrend ábécé szerinti, a sor többi verse nem látszik. |
| O59 | [4·4], [4·5] | Szétesett mondat; a görög szó „LXX-megfelelője” a táblában héber. |
| O75 | [4·37], [4·39]; [4·86] | „Egyikének jelentése sem egyértelmű” ↔ „többségén egyértelmű”, egy bekezdésen belül. |
| O76 | [4·86] ↔ [4·88], [2·4] | A kétértelműség és a hiányzó hozzárendelés egybemosva. |
| O84 | [4·84] ↔ [4·85]; [9·6] | A bevezető rokon nyelvi adatot ígér, a táblázat üres, és a [9·6] is ide küld. |
| O88 | [5·4] | „ἄβυσσος (ἄβυσσος, abüsszosz)”: a szó a zárójelben újra áll. |
| O99 | [9·2] | Nyelvtanilag szétesett mondat, és az 1.2 nem sorol fel szópárokat. |
| O102 | [9·7] | „Az 1 görög szócsaládból 1 esetében”: érthetetlen. |
| O108 | [9·13]; [9·11] | Nem tudni, mi az „ugyanez”; a középkori glossza kor nélkül áll az „Ókori értelmezők” között. |

### J2 — rögzített utalás (jelölt, 5)

| # | jel | olvasói mondat |
|---|---|---|
| O15 | [Jelmagyarázat·9], [4·91] | A beharangozott 4.13 és 4.14 pont nincs a lapon, a 4.11 alatt csak cím áll. |
| O33 | [2·3], [2·4], [2·5], 2.1 alcím | Ugyanaz a szám („2.1”) alcímet és lábjegyzetet is jelöl. |
| O67 | [4·28] ↔ [4·22], [4·26] | „A Louw–Nida-doménsor a 4.4 pontban”, holott a 4.2 alatt áll. |
| O110 | [12·2], [12·4] ↔ [Kolofon·5] | A szakasz idézési formát ígér, csak átutal, a Kolofon pedig megtiltja az idézést. |
| O119 | [Jelmagyarázat·5], [1·6], [1·9], [8·4], [Kolofon·4], [Kolofon·7] | A hivatkozások célja fájlnév (`TEREMT-001_KIZARASOK.md`, `ALVIL-001_TUDOMANYOS.md`…). |

### Más, már nyitott gazdánál (2)

| # | jel | olvasói mondat | gazda |
|---|---|---|---|
| O35 | [2·4], [4·49] ↔ [4·54]… | A táblázat szinte minden helyet a BDB 5. jelentéséhez („örvény”) köt, a szótár és a próza öt jelentésre osztja őket. | #240 (BDB-versjelentés) |
| O82 | [4·75], [5·4] ↔ [4·100] | A „tenger” (πόντος) a táblázatban Pontusz tartomány neveként áll. | N-F240a |
