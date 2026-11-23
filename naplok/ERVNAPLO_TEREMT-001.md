# ERVNAPLO_TEREMT-001 — érvvázlat és érvnapló (C-ev)

*Kézi, belső (`sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pont, „Az érvnapló”). Író: `claude-opus-5-5`, 2026-11-23, F239 U2, a bizonyítéklap (`naplok/BIZONYITEK_TEREMT-001.md`) után, a próza előtt. A határ: `naplok/F239_hatar.md`. Állításonként: állítás · érvtípus (szövegtanú / hiány / recepció) · bizonyíték · döntés (eldöntve / nyitva / kimarad). A „nyitva” pontok a lap Vitatott pontjai; a lap többi mondata ezeket nem dönti el. „Lekérdezendő” sor nem maradt: a próza előtt mind lefutott.*

*Az U2 lekérdezéseinek proveniencia-sorai: a kollokációk a `naplok/F239_lekerdezesek.tsv` B3-sorai (`scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H8415+… | ts=2026-11-23T12:23–12:33Z`); a vers-szintű görög és héber szavak: `scope=range:Jel 9:1+9:2+20:1+20:3+Róm 10:7+Luk 8:31+Ézs 51:9+51:10 | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | ts=2026-11-23`; a Septuaginta szavai: `scope=range:1Móz 7:11+8:2+5Móz 30:13+Zsolt 71:20+107:26+Jón 2:6 | forras=konkordancia/LXX_OS/{genesis,deuteronomy,psalms-lxx,jonah}.tsv | ts=2026-11-23`; a névelő-számlálás: `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv (a H8415 tokent közvetlenül megelőző H9009) | strong=H8415 | n=36 | ts=2026-11-23`.*

## A. A lexikai alap (eldöntve; a próza ezekből indul)

| # | állítás | érvtípus | bizonyíték | döntés |
|---|---|---|---|---|
| A1 | A héber Bibliában a tehóm 35 versben, 36-szor áll (a Zsolt 42:8-ban kétszer); egyes és többes számban. | szövegtanú | `lekerdez.py scan H8415`: 35 igehely, 36 előfordulás (U1 3. pont); bizonyítéklap, alapvonal: 35 / 23 204 vers | eldöntve |
| A2 | Az Újszövetségben az ἄβυσσος 9 versben áll: Luk 8:31, Róm 10:7 és hétszer a Jelenésekben. | szövegtanú | `scan G0012`: 9 igehely (U1 3. pont) | eldöntve |
| A3 | A görög fordítás (Septuaginta) a 35 tehóm-versből 30-ban ἄβυσσος-szal adja vissza; ez köti össze a két nyelvet. Öt versben más szót hoz vagy átfogalmaz (2Móz 15:5 βυθός; 2Móz 15:8; 1Móz 49:25; Péld 8:27, 28). | szövegtanú | `naplok/F239_U1_TEREMT-001_lxx_hid.tsv`, `…_lxx_g0012.tsv` | eldöntve |
| A4 | A görög ἄβυσσος tágabb a tehómnál: négy versben más héber szót vagy semmit nem fordít (Ézs 44:27 cúlá, Jób 41:31 mecólá, Jób 36:16 rahab, Zsolt 71:21 ismétlés). Az ÚSZ ezt a tágabb görög szót örökli. | szövegtanú | ugyanott; a héber szavak: TAHOT; `F239_hatar.md` K2 | eldöntve |
| A5 | A magyar „mélység” nem jele a tehómnak: a Károli a motívum verseiben „tenger”, „víz”, „örvény”, „fenékig” szóval is fordítja (Jób 41:32 „a tenger megőszült”), és mélység-szavai 95 más versben más héber vagy görög szót fordítanak. | szövegtanú | teljesség-mérés, Károli-szó háló (U1 2. pont); `F239_hatar.md` K1 | eldöntve |
| A6 | A tehóm sohasem áll kiírt névelővel. | szövegtanú | 36 előfordulásból 0-ban áll közvetlenül előtte a névelő (H9009) a TAHOT-ban; *korlát:* az elöljárószóba olvadt névelőt ez a számlálás nem látja, ezért a próza csak a kiírt névelőről beszél | eldöntve |
| A7 | A leggyakoribb társszavak: víz (14 vers), „nagy/sok” (8: a „nagy mélység”), ég (7), tenger (7), föld (6). | szövegtanú | kollokáció (U1 4. pont) | eldöntve |

## B. A láncbeli szerep (DT878: a lap a hely szerepét e döntés szerint mondja)

A motívum láncának csomópontjai, szerepükkel. A szakaszbeli szerep (az igehely saját funkciója) az igehely-prózában áll; itt csak a láncbeli.

| # | hely | láncbeli szerep | bizonyíték | döntés |
|---|---|---|---|---|
| B1 | 1Móz 1:2 | **kezdőpont**: a teremtés előtti víztömeg, sötétséggel a színén, a Lélek fölötte; nem ellenfél, hanem a formálás anyaga | a vers szavai (sötétség + tehóm: kollokáció n=1); a tehóm a versben semmit nem cselekszik | eldöntve |
| B2 | 1Móz 7:11 → 8:2 | **megnyitás és bezárás**: ugyanaz a kifejezés („a nagy mélység forrásai”, a 8:2-ben „a mélység forrásai”) ellentétes igével; az özönvíz a teremtési határ felfüggesztése és visszaállítása | kollokáció H8415+H4599 (forrás): 1Móz 7:11, 8:2, Péld 8:24 (n=3); 7:11: „felfakadának”, 8:2: „bezárulának” | eldöntve |
| B3 | 1Móz 49:25 = 5Móz 33:13 | **áldásforrás**: „a mélység, amely alant nyugszik” — ugyanaz a kifejezés Jákob és Mózes áldásában, József törzsére | kollokáció H8415+H7257 (nyugszik/hever): pontosan ez a két vers (n=2); ég + mélység párban mindkettőben | eldöntve |
| B4 | 2Móz 15:5, 15:8 | **szabadítás és ítélet eszköze**: a mélységek ellepik az egyiptomiakat, megsűrűsödnek a tenger közepén; a többes szám első helye | a vers szavai; a 15:5-ben a tehóm a מְצוֹלָה (mecólá) párja (kollokáció n=1) | eldöntve |
| B5 | Ézs 51:10 (és 63:13, Zsolt 106:9) | **kötés**: a teremtés és a kivonulás egy versben — aki kiszárította „a nagy mélység vizeit”, és utat csinált a megváltottaknak; az előző vers (51:9) a Ráhábot és a sárkányt nevezi | TAHOT: Ézs 51:9 Ráháb (H7294) + tannín (H8577), 51:10 tehóm + „nagy” + tenger + megváltottak | eldöntve (a Ráháb a 51:9-ben áll, nem a tehóm-versben: a próza kontextusként, nem előfordulásként említi) |
| B6 | Jón 2:6, Zsolt 71:20, Zsolt 107:26, Ez 26:19, Ez 31:15 | **a halál mélye**: a mélység mint a halál közelsége, ahonnan Isten felhoz | a versek szavai; az Ez 31:15-ben a seól is (kollokáció H8415+H7585 n=1); a Jón 2:3-ban a seól, a 2:6-ban a tehóm | eldöntve (a szerep; a seól-motívummal való viszony: V5) |
| B7 | Jób 38:16, 38:30, 28:14; Zsolt 33:7, 135:6 | **Isten tudásának és uralmának mértéke**: a mélység, ahová ember nem jut el, és amelyet Isten raktárba gyűjt | a versek szavai | eldöntve |
| B8 | Róm 10:7 | **az ÚSZ halál-mélysége**: „ki száll le a mélységbe? (tudniillik Krisztust a halálból felhozni)” | TAGNT: καταβαίνω + ἄβυσσος + ἐκ νεκρῶν + ἀνάγω; az 5Móz 30:13 görögje itt „a tenger túlsó partja” (πέραν τῆς θαλάσσης), Pál ezt cseréli ἄβυσσος-ra | eldöntve (a csere ténye); a csere forrása: V4 |
| B9 | Luk 8:31; Jel 9:1–2, 11:7, 17:8, 20:1–3 | **a bezárt mélység**: a démonok, a fenevad, a sárkány helye; a Jelenésekben kulccsal megnyitják (9:1–2) és kulccsal bezárják, lepecsételik (20:1–3) | TAGNT: κλείς (kulcs) a 9:1-ben és a 20:1-ben; ἀνοίγω (megnyit) a 9:2-ben, κλείω (bezár) + σφραγίζω (lepecsétel) a 20:3-ban | eldöntve (a Jelenéseken belüli pár); a Genezishez való viszony: V2 |

## C. A vitatott pontok

### V1 — A tehóm és Tiámat: rokon-e, és ha igen, polémia-e az 1Móz 1:2?
- *Állítás (a) — a régi tanulmány kiinduló felvetése:* a tehóm nyelvileg rokon az akkád Tiámattal, és az 1Móz 1:2 a babiloni teremtésmítosz polemikus átvétele (Gunkel, *Schöpfung und Chaos*). · **recepció** (szakirodalom, a szintje: vallástörténeti hipotézis) · bizonyíték: a szöveg részéről csak az A6 (névelő nélküli, tulajdonnévszerű használat) és a költői megszemélyesítés (Hab 3:10 „a mélység hangot ad, felemeli kezeit”; Zsolt 77:17 „megrendültek”) támogatja; a nyelvi rokonság szótári tény, a polémia nem a szövegből, hanem a mítosz ismeretéből következik.
- *Állítás (b):* a tehóm a bibliai szövegben sehol nem cselekvő, Istennel szembenálló lény, hanem anyagi elem; a megszemélyesítés költői, és a mélység Istent dicséri (Zsolt 148:7) (Wenham, Cassuto). · **szövegtanú** + **recepció** · bizonyíték: a 35 vers egyikében sem alanya a tehóm Isten elleni cselekvésnek (bizonyítéklap, versenként); a Zsolt 148:7 dicséretre hívja; az 1Móz 1:2-ben a tehóm semmit nem tesz.
- *Döntés:* **nyitva** a rokonság és a polémia kérdésében (a lap mindkettőt bemutatja, a forrásukkal); **eldöntve** a (b) szöveg-szintű része: a lap kimondja, hogy a szövegben a mélység nem ellenfél. A két réteg nem ellentmondás: a vallástörténeti háttér kérdése nyitva marad, a bibliai szöveg viselkedése nem.

### V2 — A Jelenések bezárása (20:1–3) visszhangozza-e az 1Móz 8:2 bezárását?
- *Állítás (a) — a régi tanulmány:* a Jel 20:1–3 „bezárás”-a szerkezetileg megismétli az 1Móz 8:2-t; az özönvíz az eszkatológiai mintázat előképe (nyitás 7:11 ↔ Jel 9:1–2, zárás 8:2 ↔ Jel 20:3). · **recepció** (tipológiai olvasat) · bizonyíték: a mozzanatok sorrendje (megnyitás → pusztítás → bezárás) mindkét helyen; a görög 1Móz 7:11 ugyanazt a „megnyit” igét (ἀνοίγω) használja, mint a Jel 9:2 — de az ég csatornáira, nem a mélységre.
- *Állítás (b):* a kapcsolat kép-szintű, nem szó szerinti: a görög 1Móz 8:2 igéje ἐπικαλύπτω („befed”), a Jel 20:3-é κλείω („bezár”); a Jelenések saját párja (kulcs: 9:1 és 20:1) a könyvön belül zárul. · **szövegtanú** (+ **hiány**: a közös zár-ige hiánya) · bizonyíték: LXX 1Móz 8:2 ἐπεκαλύφθησαν; TAGNT Jel 20:3 ἔκλεισεν; LXX 1Móz 7:11 ἠνεῴχθησαν az ég csatornáira.
- *Döntés:* **nyitva**. A lap a Jelenéseken belüli kulcs-párt eldöntöttként mondja (B9), a Genezishez való viszonyt a Vitatott pontok között, mindkét olvasattal; a Remez nem mondja, hogy a Jel 20 „megismétli” a 8:2-t.

### V3 — A Tengeri ének (2Móz 15:5, 8) tudatosan visszautal-e a genezisi özönvízre?
- *Állítás (a):* igen, a mélységek ugyanazt a szerepet töltik be (az ítélet eszköze), mint az özönvíz tehómja (Cassuto, Sarna, Levenson; a régi tanulmány szerint). · **recepció** · bizonyíték: a közös lexéma; a funkció hasonlósága (víz mint ítélet).
- *Állítás (b):* a teremtés-káosz séma általánosabb felidézése, nem egy szöveghelyre utalás (Childs). · **recepció** + **hiány** · bizonyíték: a 2Móz 15-ben a „forrás” (H4599) és a „nagy” társszó nem áll; többes szám, nem a genezisi egyes szám; a közös szó egyetlen lexéma, kifejezés nem.
- *Döntés:* **nyitva**. A szerkezeti állítás (a lexéma közös; a funkció ítélet és szabadítás) eldöntve (B4); a szándékos visszautalás kérdése a Vitatott pontok között. *A szerzők nevei a régi tanulmányból valók; az U1b/U3 forrásellenőrzése nélkül a próza nem tulajdonít nekik konkrét mondatot (a hivatkozás szintje: „a kommentárirodalomban mindkét álláspont képviselt”, vagy az ellenőrzött hely).*

### V4 — A Róm 10:7 cseréjének forrása
- *Állítás (a):* Pál a görög Zsolt 107:26 szópárját veszi át: „felmennek az egekig, leszállnak a mélységekig” (ἀναβαίνω οὐρανός / καταβαίνω ἄβυσσος) — a Róm 10:6–7 ugyanezt a két igét és a két helyet hozza, az 5Móz 30:12–13 „tengerentúl”-ja helyett. · **szövegtanú** (a görög Zsoltár szövege) + **recepció** (a függés feltevése) · bizonyíték: LXX Zsolt 106(107):26 ἀναβαίνουσιν … οὐρανῶν, καταβαίνουσιν ἕως τῶν ἀβύσσων; TAGNT Róm 10:7 καταβήσεται εἰς τὴν ἄβυσσον; az ἀνάγω („felhoz”) a görög Zsolt 70(71):20-ban is ἄβυσσος-szal áll („a föld mélységeiből ismét felhoztál”), és a Róm 10:7-ben is.
- *Állítás (b):* a csere Pál saját krisztológiai értelmezése (a „halottak közül” glossza), irodalmi forrás nélkül. · **recepció** · bizonyíték: a glossza („Krisztust a halálból felhozni”) a cserét maga értelmezi.
- *Döntés:* **eldöntve** a szókincs-egyezés ténye (a próza kimondja: a Róm 10:7 szavai a görög Zsolt 107:26 és 71:20 szavai); **nyitva**, hogy Pál tudatosan ezekből merít-e. A lapon a ténynél a „nem tudni, szándékos-e” megjegyzés áll, a Vitatott pontok között egy mondat.

### V5 — A halál mélye: a tehóm és a seól viszonya
- *Állítás:* a tehóm több helyen (Jón 2:6, Zsolt 71:20, 107:26, Ez 26:19, 31:15) a halál közelségének képe, a seól mellett, de nem azonos vele; a holtak lakóhelye az ÓSZ-ben a seól, nem a tehóm. Az ÚSZ ἄβυσσος-a (Róm 10:7) közeledik a hádészhez. · **szövegtanú** · bizonyíték: Ez 31:15 tehóm + seól egy versben (kollokáció n=1); Jón 2:3 seól, 2:6 tehóm; a 35 tehóm-vers egyikében sem „lakik” halott a tehómban; Róm 10:7 ἐκ νεκρῶν.
- *Döntés:* **eldöntve** (a határ 3. kérdése: két motívum, érintkezéssel). A lap a seól-motívumot kapcsolódó motívumként nevezi; az Ez 31:15 a két motívum adatbeli kapcsolata (`közös_igehely`; DT-F239a, szerkesztői döntés, 2026-11-23); a tohu va-vohuval az 1Móz 1:2 csak a prózában áll.

### V6 — A Genezis négy helye szándékos ív-e (teremtés → ítélet → helyreállítás → áldás)?
- *Állítás:* a szerkesztett Genezis szándékosan viszi végig a szót négy regiszteren (a régi tanulmány Remeze). · **recepció** + **hiány** · bizonyíték: a négy hely és a négy funkció szöveg-szintű (B1–B3); a szándékra a szöveg nem tanú.
- *Döntés:* **kimarad** a „szándékos” állítás; a négy hely és a négy funkció sorrendje eldöntve (a próza leírja, ítélet nélkül a szerkesztői szándékról).

## D. A bírálatra adott válaszok

*(a bíráló, `naplok/BIRALAT_TEREMT-001.md`, után kitöltve)*
