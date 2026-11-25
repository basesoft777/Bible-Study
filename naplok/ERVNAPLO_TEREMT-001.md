# ERVNAPLO_TEREMT-001 — érvvázlat és érvnapló (C-ev)

*Kézi, belső (`sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pont, „Az érvnapló”). Író: `claude-opus-5-5`, 2026-11-23, F239 U2, a bizonyítéklap (`naplok/BIZONYITEK_TEREMT-001.md`) után, a próza előtt. A határ: `naplok/F239_hatar.md` (a szerkesztő döntésével, DT-F239a–d). Állításonként: állítás · érvtípus (szövegtanú / hiány / recepció) · bizonyíték · döntés (eldöntve / nyitva / kimarad). A „nyitva” pontok a lap Vitatott pontjai; a lap többi mondata ezeket nem dönti el. „Lekérdezendő” sor nem maradt: ami nem futott le, az „kimarad” vagy „nyitva”. **v2:** a bírálat (`naplok/BIRALAT_TEREMT-001.md`) után átírva; a változások tételenként a D szakaszban.*

*Az U2 lekérdezéseinek proveniencia-sorai: a kollokációk a `naplok/F239_lekerdezesek.tsv` B3-sorai (`scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H8415+… | ts=2026-11-23T12:23–12:33Z`); a vers-szintű görög és héber szavak: `scope=range:Jel 9:1+9:2+20:1+20:3+Róm 10:7+Luk 8:31+Ézs 51:9+51:10 | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | ts=2026-11-23`; a Septuaginta szavai: `scope=range:1Móz 7:11+8:2+5Móz 30:13+Zsolt 71:20+107:26+Jón 2:6 | forras=konkordancia/LXX_OS/{genesis,deuteronomy,psalms-lxx,jonah}.tsv | ts=2026-11-23`. A bíráló 30 lekérdezése: a bírálat lekérdezési naplója (`ts=2026-11-23T13:10Z`, `claude-sonnet-5-5`).*

## A. A lexikai alap (eldöntve; a próza ezekből indul)

| # | állítás | érvtípus | bizonyíték | döntés |
|---|---|---|---|---|
| A1 | A héber Bibliában a tehóm 35 versben, 36-szor áll (a Zsolt 42:8-ban kétszer); egyes és többes számban. | szövegtanú | `lekerdez.py scan H8415`: 35 igehely, 36 előfordulás (U1 3. pont); bizonyítéklap, alapvonal: 35 / 23 204 vers | eldöntve |
| A2 | Az Újszövetségben az ἄβυσσος 9 versben áll: Luk 8:31, Róm 10:7 és hétszer a Jelenésekben. | szövegtanú | `scan G0012`: 9 igehely (U1 3. pont) | eldöntve |
| A3 | A görög fordítás (Septuaginta) a 35 tehóm-versből 30-ban ἄβυσσος-szal adja vissza; ez köti össze a két nyelvet. Öt versben más szót hoz vagy átfogalmaz (2Móz 15:5 πόντος — a vers βυθός-a a mecólá fordítása, U1b, javítva az U3b-ben; 2Móz 15:8 κύματα; 1Móz 49:25; Péld 8:27, 28). | szövegtanú | `naplok/F239_U1_TEREMT-001_lxx_hid.tsv`, `…_lxx_g0012.tsv` (a 35 vers LXX-szavai versenként; a bíráló független ellenőrzést kért, ez a versenkénti tábla) | eldöntve |
| A4 | A görög ἄβυσσος tágabb a tehómnál: négy versben más héber szót vagy semmit nem fordít (Ézs 44:27 cúlá, Jób 41:31 mecólá, Jób 36:16 rahab, Zsolt 71:21 ismétlés). Az ÚSZ ezt a tágabb görög szót örökli. | szövegtanú | ugyanott; a héber szavak: TAHOT; `F239_hatar.md` K2 | eldöntve |
| A5 | A magyar „mélység” nem jele a tehómnak: a Károli a motívum verseiben „tenger”, „víz”, „örvény”, „fenékig” szóval is fordítja (Jób 41:32 „a tenger megőszült”), és mélység-szavai 95 más versben más héber vagy görög szót fordítanak. | szövegtanú | teljesség-mérés, Károli-szó háló (U1 2. pont); `F239_hatar.md` K1 | eldöntve |
| A6 | ~~A tehóm sohasem áll kiírt névelővel.~~ | — | a bírálat: a Zsolt 106:9 és az Ézs 63:13 elöljáróba olvadt névelővel áll (BDB: „only here with article”); a névelőtlenség a költői könyvekben közszavaknál is gyakori (a seól 0/33) | **kimarad** (a próza nem mondja, és Tiámat-érvként sem használja) |
| A7 | A leggyakoribb társszavak: víz (14 vers), ég (7), tenger (7), föld (6). A „nagy mélység” (tehóm rabbá) 5 versben áll: 1Móz 7:11, Zsolt 36:7, 78:15, Ámós 7:4, Ézs 51:10. | szövegtanú | kollokáció (U1 4. pont); a H7227 8 verséből 3-ban (Zsolt 71:20, Ez 26:19, 31:15) a „sok” nem a tehóm jelzője (bírálat) | eldöntve |

## B. A láncbeli szerep (DT878: a lap a hely szerepét e döntés szerint mondja)

A szerep megnevezése (kezdőpont, áldásforrás …) **értelmezés**; adat csak a szóismétlés, a helyekkel (bírálat, 7. kérdés). A szakaszbeli szerep (az igehely saját funkciója) az igehely-prózában áll; itt csak a láncbeli.

| # | hely | láncbeli szerep | bizonyíték (az adat) | döntés |
|---|---|---|---|---|
| B1 | 1Móz 1:2 | **kezdőpont**: a teremtés előtti állapot, a víztömeg sötétséggel a színén, a Lélek fölötte; a tehóm a versben semmit nem cselekszik | a vers szavai (sötétség + tehóm: kollokáció n=1); hogy a tehóm a „formálás anyaga”, a vers nem mondja | eldöntve (a „formálás anyaga” kimarad) |
| B1b | Péld 8:24, 8:27, 8:28; Péld 3:20; Zsolt 104:6 | **a megteremtett mélység**: a Bölcsesség a mélységek előtt született („Még mikor semmi mélységek nem voltak”), Isten határt szab nekik, a tudása hasítja meg őket | a versek szavai; a Péld 8:24 szerint a mélységek még nem voltak, tehát ez más regiszter, mint az 1Móz 1:2 | eldöntve (két regiszter: a teremtés előtti állapot és a teremtett mélység) |
| B2 | 1Móz 7:11 → 8:2 | **megnyitás és bezárás**: „a nagy mélység forrásai” felfakadnak (7:11), „a mélység forrásai” bezárulnak (8:2); a héber 8:2 igéje סָכַר („bezárul”), a Károli „bezárulának” | kollokáció H8415+H4599 („forrás”): 1Móz 7:11, 8:2, Péld 8:24; **a kifejezés („a mélység forrásai”) csak a 7:11-ben és a 8:2-ben**, a Péld 8:24-ben „víztől teljes források” a mélységek mellett; a „forrás” más szóval (עַיִן) az 5Móz 8:7-ben és a Péld 8:28-ban | eldöntve |
| B3 | 1Móz 49:25 = 5Móz 33:13 | **áldásforrás**: „a mélység, amely alant nyugszik” — ugyanaz a kifejezés Jákob és Mózes áldásában, József törzsére | kollokáció H8415+H7257 (nyugszik/hever): pontosan ez a két vers (n=2); ég + mélység párban mindkettőben | eldöntve |
| B4 | 2Móz 15:5, 15:8 | **szabadítás és ítélet eszköze**: a mélységek ellepik az egyiptomiakat, megsűrűsödnek a tenger közepén; a többes szám első helye | a vers szavai; a 15:5-ben a tehóm a מְצוֹלָה (mecólá) párja (kollokáció n=1) | eldöntve |
| B5 | Ézs 51:10 (és 63:13, Zsolt 106:9) | **teremtés és kivonulás egy helyen**: aki kiszárította „a nagy mélység vizeit”, és utat csinált a megváltottaknak; az előző vers (51:9) a Ráhábot és a sárkányt nevezi | TAHOT: Ézs 51:9 Ráháb (H7294) + tannín (H8577), 51:10 tehóm + „nagy” + tenger + megváltottak | eldöntve (a Ráháb a 51:9-ben áll, nem a tehóm-versben: a próza kontextusként, nem előfordulásként említi) |
| B6 | Jón 2:6, Zsolt 71:20 | **a halál mélye**: a mélység mint a halál közelsége (Jón 2:6: „körülvett engem a mélység”; Zsolt 71:20: „a föld mélységéből ismét felhozol”) | a versek szavai; BDB a Zsolt 71:20-hoz: a seól értelmében; a Jón 2:3-ban a seól, a 2:6-ban a tehóm, a „felhozás” a 2:7-ben (verem); egy versben a tehóm mellett halál-szó (mávet, sahat, bór) sehol nem áll (n=0), a seól csak az Ez 31:15-ben | eldöntve (két hely; a többi korábbi tagot l. B6b) |
| B6b | Ez 26:19; Ez 31:4, 31:15; Zsolt 107:26; Zsolt 42:8 | **nem a halál mélye**: Ez 26:19 a Tíruszt elborító tenger (ítélet); Ez 31:4, 15 a Nílus vize (a cédrust táplálja, majd Isten gyászban visszatartja; a 31:15-ben a seól mellett); Zsolt 107:26 a viharhullámok mélye; Zsolt 42:8 a zuhatag (BDB: talán a Jordán) | BDB H8415 versenkénti jelentései (bírálat, V5) | eldöntve (az Ez 31:15 a seól-motívummal közös vers: DT-F239a; szerepe: a kozmikus víz a holtak helye mellett, nem a halál mélye) |
| B7 | Jób 38:16, 38:30, 28:14; Zsolt 33:7, 135:6 | **Isten tudásának és uralmának mértéke**: a mélység, ahová ember nem jut el, és amelyet Isten raktárba gyűjt | a versek szavai | eldöntve |
| B8 | Róm 10:7 | **az ÚSZ halál-mélysége**: „ki száll le a mélységbe? (tudniillik Krisztust a halálból felhozni)” | TAGNT: καταβαίνω + ἄβυσσος + ἐκ νεκρῶν + ἀνάγω; az 5Móz 30:13 görögje itt „a tenger túlsó partja” (πέραν τῆς θαλάσσης), Pál ezt cseréli ἄβυσσος-ra | eldöntve (a csere ténye); a csere forrása: V4 |
| B9 | Luk 8:31; Jel 9:1–2, 11:7, 17:8, 20:1, 20:3 | **a bezárt mélység**: a démonok, a fenevad, a sárkány helye; a Jelenésekben a mélység kulcsa két helyen áll (9:1, 20:1), a 9:2-ben megnyitják, a 20:3-ban bezárják és lepecsételik | TAGNT: κλείς + ἄβυσσος 2 versben (Jel 9:1, 20:1); ἀνοίγω a 9:2-ben, κλείω + σφραγίζω a 20:3-ban; *a nyit–zár ige és a kulcs a Jelenések általános szókincse (Jel 3:7, 1:18): a pár tény, de nem a mélységre szabott szerkezet* | eldöntve (a tény); a Genezishez való viszony: V2 |

## C. A vitatott pontok

### V1 — A tehóm és Tiámat: rokon-e, és ha igen, polémia-e az 1Móz 1:2?
- *Állítás (a):* a tehóm nyelvileg rokon az akkád Tiámattal, és az 1Móz 1:2 a babiloni teremtésmítosz polemikus, demitologizált átvétele. · **recepció** (vallástörténeti hipotézis; a repó adatában egyetlen hely: a BDB a tehóm szócikkében Gunkel *Schöpfung und Chaos* művét idézi) · bizonyíték: a nyelvi rokonság a repó szótáraiban **nem** szerepel (a BDB H8415 szócikkében nincs Tiámat; a `BDB_rokon_irasok.tsv`-ben nincs sor), ezért a próza nem mondja „szótári ténynek”, hanem a vallástörténeti irodalom felvetéseként.
- *Állítás (b), szövegtanú:* a tehóm a 35 versben sehol nem cselekszik Isten ellen; a megszemélyesítés költői (Hab 3:10 „hangot ad”; Zsolt 77:17 „megrendültek”; Zsolt 42:8 „mélység mélységet hív”; Jón 2:6 „körülvett”), és a Zsolt 148:7 a mélységet a tengeri szörnyekkel (tannín) együtt Isten dicséretére hívja. · bizonyíték: bizonyítéklap versenként; kollokáció H8415+H8577: Zsolt 148:7 (n=1).
- *Állítás (b), recepció:* ebből a kommentárirodalom egy része (a régi tanulmány Wenhamet és Cassutót nevezi) arra következtet, hogy a tehóm puszta anyagi elem. · **recepció**, a szerzők mondatai a repóban nem ellenőrzöttek.
- *Mérlegelés (a bírálat):* a (b) szövegtanúja hiányérv, és az (a) „demitologizált átvétel” változatával is összefér: az is a konfliktus hiányát jósolja. A szöveg a „nyers mítosz-ellenfél” olvasatot cáfolja, a vallástörténeti hátteret nem.
- *Döntés:* **eldöntve** a szűk szöveg-szintű állítás: a lap kimondja, hogy a bibliai szövegben a mélység **nem cselekszik Isten ellen**, és Isten dicséretére hívható. **Nyitva** a rokonság és a polémia: a lap a Vitatott pontok között mindkettőt bemutatja; név csak a Gunkelé áll (a BDB idézi), a többieknél „a kommentárirodalomban mindkét álláspont képviselt”.

### V2 — A Jelenések bezárása (20:3) visszhangozza-e az 1Móz 8:2 bezárását?
- *Állítás (a):* a Jel 20:3 bezárása az 1Móz 8:2 bezárását ismétli; az özönvíz az eszkatológiai mintázat előképe (a régi tanulmány). · **recepció** (tipológiai olvasat; a „keret” értelmezés, nem adat) · bizonyíték: a jelentés-szintű egyezés: a héber 8:2 igéje סָכַר („bezárul”, Károli: „bezárulának”), a Jel 20:3-é κλείω („bezár”); mindkettő a mélységre vonatkozik.
- *Állítás (b):* a kapcsolat a görög szöveg szintjén nem igazolható: a Septuaginta a 8:2-ben ἐπικαλύπτω („befed”) igét hoz, a Jelenések nem idéz; a megnyitásnál egyik nyelvben sem a mélységé a „megnyit” ige (a héber és a görög 7:11-ben a mélység forrásai „hasadnak”, az ég csatornái „nyílnak”). · **recepció** (a Septuaginta mint a görög olvasó szövege) + **hiány** (a közös görög szó hiánya; gyenge érv, a próza így mondja).
- *Döntés:* **nyitva**. A lap a jelentés-egyezést (bezárás mindkét helyen) és a görög szöveg hiányát egyaránt kimondja; a Remez nem mondja, hogy a Jel 20 „megismétli” vagy „keretezi” a 8:2-t. A Jelenéseken belüli kulcs-pár (B9) tény, de nem érv a Genezis-kapcsolat mellett vagy ellen.

### V3 — A Tengeri ének (2Móz 15:5, 8) tudatosan visszautal-e a genezisi özönvízre?
- *Állítás (a):* igen, a mélységek ugyanazt a szerepet töltik be (az ítélet eszköze), mint az özönvíz tehómja. · **recepció** (a régi tanulmány Cassutót, Sarnát, Levensont nevezi; a mondataik a repóban nem ellenőrzöttek) · bizonyíték: a közös lexéma; a funkció hasonlósága (víz mint ítélet).
- *Állítás (b):* a teremtés-káosz séma általánosabb felidézése, nem egy szöveghelyre utalás (a régi tanulmány Childsot nevezi). · **recepció** + **hiány** · bizonyíték: a 2Móz 15-ben a „forrás” és a „nagy” társszó nem áll; a közös szó egyetlen lexéma, kifejezés nem. (A „többes szám” érv kimarad: az 5Móz 8:7 és a Zsolt 106:9 is többes, és nem Genezis-utalás.)
- *Döntés:* **nyitva**. A szerkezeti állítás (közös lexéma; a funkció ítélet és szabadítás) eldöntve (B4); a szándékos visszautalás a Vitatott pontok között, nevek nélkül („a kommentárirodalomban mindkét álláspont képviselt”).

### V4 — A Róm 10:7 cseréjének forrása
- *Tény (szövegtanú):* a Róm 10:6 az 5Móz 30:12-t idézi (τίς ἀναβήσεται εἰς τὸν οὐρανόν), a Róm 10:7 az 5Móz 30:13 „ki megy át a tenger túlsó partjára” kérdését „ki száll le a mélységbe” (τίς καταβήσεται εἰς τὴν ἄβυσσον) kérdésre cseréli, és „Krisztust a halottak közül felhozni” (ἀναγαγεῖν) magyarázattal látja el.
- *Állítás (a):* Pál a görög Zsoltárok szókincséből merít: a καταβαίνω + ἄβυσσος a görög Zsolt 107:26-ban („leszállnak a mélységekig”), az ἀνάγω + ἄβυσσος a görög Zsolt 71:20-ban („a föld mélységeiből ismét felhoztál”) áll; a Zsolt 107:26 környezete tengeri vihar, ez a „tengeren túl” képével rokon. · **szövegtanú** (az azonos szótövek; az alak és az elöljáró eltér: ἕως τῶν ἀβύσσων ↔ εἰς τὴν ἄβυσσον) + **recepció** (a függés feltevése)
- *Állítás (b):* a csere Pál saját krisztológiai értelmezése, irodalmi forrás nélkül. · **recepció** · bizonyíték: a magyarázó mondat a cserét maga értelmezi.
- *Döntés:* **eldöntve** a tény (a csere és a két zsoltár azonos szótövei); **nyitva**, hogy Pál tudatosan ezekből merít-e. A lap a ténynél nem mondja, hogy „ugyanazok a szavak” vagy „ugyanaz a két ige”; a Kivonat és a Remez a tényt és a nyitott kérdést külön mondatban mondja.

### V5 — A halál mélye: a tehóm és a seól viszonya
- *Állítás:* a tehóm két helyen a halál közelségének képe (Jón 2:6, Zsolt 71:20), de nem a holtak lakóhelye; a holtak helye az ÓSZ-ben a seól. A két szó egy versben csak az Ez 31:15-ben áll, ott a tehóm a Nílus kozmikus vize, amelyet Isten a fáraó bukásakor gyászba borít, a seól a hely, ahová a cédrus leszáll. Az ÚSZ-ben a Róm 10:7 ἄβυσσος-a a halottak helye; a Luk 8:31 és a Jelenések ἄβυσσος-a börtön. · **szövegtanú** · bizonyíték: B6, B6b; kollokáció H8415+H7585 (Ez 31:15, n=1); H8415 + halál-szavak n=0; Róm 10:7 ἐκ νεκρῶν.
- *Döntés:* **eldöntve** (a határ 3. kérdése: két motívum, érintkezéssel). A lap a seól-motívumot kapcsolódó motívumként nevezi; az Ez 31:15 a két motívum adatbeli kapcsolata (`közös_igehely`; DT-F239a, szerkesztői döntés, 2026-11-23); a tohu va-vohuval az 1Móz 1:2 csak a prózában áll. A lap az Ez 31:15-re, az Ez 26:19-re és a Zsolt 107:26-ra nem mondja, hogy „a halál mélye”, és az ÚSZ-ről általában sem, hogy az ἄβυσσος a halottak helye (csak a Róm 10:7-ről).

### V6 — A Genezis négy helye szándékos ív-e (teremtés → ítélet → helyreállítás → áldás)?
- *Állítás:* a szerkesztett Genezis szándékosan viszi végig a szót négy regiszteren (a régi tanulmány Remeze). · **recepció** + **hiány** · bizonyíték: a négy hely szöveg-szintű (B1–B3), a négy funkció megnevezése értelmezői besorolás; a szándékra a szöveg nem tanú.
- *Döntés:* **kimarad** a „szándékos” állítás. A lap a négy helyet a könyv sorrendjében, a szavaikkal mondja el; a 7:11 és 8:2 (megnyitás, bezárás) és a 49:25 (= 5Móz 33:13, áldás) szövegtanú; a négy funkció neve olvasat, a próza így jelöli.

## D. A bírálatra adott válaszok

*A bírálat: `naplok/BIRALAT_TEREMT-001.md` (2026-11-23, `claude-sonnet-5-5`). Minden tételre egy sor.*

| bírálati tétel | válasz | mi változott |
|---|---|---|
| Elutasított 1 — A6 „sohasem áll névelővel”, és mint a tulajdonnévszerűség támasza | **elfogadva** | az A6 kimarad; a V1-ben nem érv |
| Elutasított 2 — V1(a) „a nyelvi rokonság szótári tény” | **elfogadva** | V1(a): recepció, a BDB Gunkel-idézetével; a próza nem mondja szótári ténynek |
| V1 — a (b) szövegtanúja hiányérv, a „demitologizált átvétellel” is összefér; ellenpéldák (Zsolt 148:7, Jón 2:6, Zsolt 42:8) | **elfogadva** | az eldöntött rész szűkítve: „nem cselekszik Isten ellen”; a Zsolt 148:7 bizonyítékként; mérlegelés-sor |
| V1 — Wenham/Cassuto ellenőrzés nélkül; a szövegtanú és a recepció egy tételben | **elfogadva** | szétválasztva; nevek a prózában nem (csak Gunkel) |
| Elutasított 3 — V2(b) „a közös zár-ige hiánya” (a héber 8:2 is „bezár”) | **elfogadva** | V2(a) bizonyítéka a jelentés-egyezés; V2(b) a görög szint hiánya, recepcióként; a B2-ben a héber ige |
| Elutasított 4 — a kulcs-pár mint motívum-specifikus szerkezet | **elfogadva** | B9: tény, a Jelenések általános szókincsének jelzésével; nem érv a V2-ben |
| V2 — a „megnyit” egyik nyelvben sem a mélységé | **elfogadva** | V2(b)-be felvéve |
| V2 — a „keret” értelmezés, nem adat | **elfogadva** | a B-tábla bevezetője: a szerep-nevek értelmezések, adat csak a szóismétlés |
| V3 — a B2 túlszámlálja a „forrás” kifejezést; a „forrás” más szóval is (5Móz 8:7, Péld 8:28) | **elfogadva** | B2: a kifejezés csak a 7:11-ben és a 8:2-ben; a Péld 8:24 és az עַיִן-helyek külön |
| V3 — a „többes szám” érv nem megkülönböztető | **elfogadva** | kimarad a V3(b)-ből |
| V3 — szerzőnevek ellenőrzés nélkül | **elfogadva** | nevek nélkül a prózában |
| Elutasított 5 — V4(a) „ugyanazt a két igét”, „ugyanazok a szavak” | **elfogadva** | V4: az ἀναβαίνω az 5Móz 30:12-ből; azonos szótövek, eltérő alak és elöljáró |
| V4 — a Zsolt 107:26 tengeri környezete | **elfogadva** | V4(a)-ba felvéve, a nyitott kérdés része |
| V4 — a tény és a nyitott kérdés ne keveredjen a lapon | **elfogadva** | V4 döntés: külön mondatban; a próza utáni ellenőrzés (U4) |
| Elutasított 6 — az Ez 26:19, 31:15 és a Zsolt 107:26 mint „a halál mélye”; a „felhoz” közös jegye | **elfogadva** | B6 két helyre szűkítve (Jón 2:6, Zsolt 71:20); B6b az új szerepekkel; V5 átírva; a határ-fájl (e) csoportja igazítva |
| V5 — a Zsolt 42:8 a határban a halál mélye, a B6-ban nem | **elfogadva** | a Zsolt 42:8 a B6b-ben (zuhatag), a határ-fájl (e) csoportjából kivéve |
| V5 — „az ÚSZ ἄβυσσος-a közeledik a hádészhez” egy versre szól | **elfogadva** | V5: csak a Róm 10:7-ről; a Luk 8:31 és a Jelenések: börtön |
| Elutasított 7 — a Péld 8:24 mint „teremtés előtti állapot” | **elfogadva** | B1b: a megteremtett mélység külön regiszter; a B1 „formálás anyaga” kimarad |
| V6 — a négy funkció értelmezői besorolás | **elfogadva** | V6 döntés: a négy funkció neve olvasat, a próza így jelöli |
| A7 — a „nagy mélység” 5 versre szól, nem 8-ra | **elfogadva** | A7 átírva |
| 5. kérdés (a lap két helye) — a próza után ellenőrizendő: V1 Kivonat ↔ Vitatott pont; V2 Remez; V5 Sod és Módszertan az Ez 31:15-ről | **elfogadva, az U3/U4-re** | az U2 átadójában az U3 kötelező elemei és az U4 ellenőrzési listája közé felvéve |
| Lekérdezendő: az A3 független ellenőrzése | **elutasítva** | az A3 bizonyítéka a versenkénti LXX-tábla (`…_lxx_g0012.tsv`: a 34 Károli-kulcsos G0012-vers, mind a 35 tehóm-vers megjelölve); ez maga a független számlálás |
| Lekérdezendő: a szerzők mondatai; a Targum a Róm 10:7-hez | **elfogadva, kimarad** | repón kívüli forrás; a próza nem tulajdonít mondatot, és a Targumot nem említi; a visszhang-réteg (U1b) Targum-sorai ezt később pótolhatják |

## D2. A második bírálat többlete

*A második bírálat: `naplok/BIRALAT_TEREMT-001_masodik.md` (`claude-sonnet-5-5`, 2026-11-23T13:25Z, a v1-en; az U3 futtatta). Ami a D-ben már válaszolt (A6, A7, V1 szerzőnevek és rokonság, B1 / Péld 8:24, V2 „pár”, V4 az 5Móz 30:12, a Zsolt 107:26 a halál-csoportban, a „hádész” mondat), itt nem ismétlődik; csak a többlet. Író: `claude-opus-5-5` (F239 U3). Ellenőrző lekérdezések: a görög Ószövetség ἄβυσσος-versei a καταβαίνω / ἀνάγω / ἀναβαίνω igével (`scope=LXX_OS-teljes | forras=konkordancia/LXX_OS/*.tsv (lemma) | n=7 | ts=2026-11-23`); a tehóm előtti előtag-tokenek (`scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H8415 | ts=2026-11-23`: a Zsolt 106:9 és az Ézs 63:13 `בַּ`).*

| # | a második bírálat tétele | válasz | mi változik |
|---|---|---|---|
| D2.1 | V4: a leszállás és a felhozás igéje az ἄβυσσος mellett nem csak a két zsoltárban áll (G2597: Ez 31:15, Jób 36:16, Jób 38:30, Zsolt 107:26; G0321: Ez 26:19, Zsolt 71:20, 71:21) | **elfogadva** | A V4 ténye bővül: a lap nem mondja, hogy a szópár csak a két zsoltárban áll; a nyitott kérdés (honnan merít Pál) a hét verset említi, a két zsoltárt mint a legközelebbit (a 107:26-ban mindkét irány, fel és le, egy versben; a 71:20-ban a „felhoz”). |
| D2.2 | V1: a tehóm több helyen Isten cselekvésének tárgya (Ézs 51:10 kiszárítja, Ámós 7:4 tűz emészti), a Zsolt 104:6–7 a vizek szétriadását mondja | **elfogadva** | A V1 Vitatott pontja ezt is kimondja, a vallástörténeti olvasat mellett szóló adatként: Isten a mélységgel cselekszik (kiszárítja, megemészti, tárházba gyűjti), az Ézs 51:9 Ráhábja és sárkánya a szomszéd versben. Az eldöntött szűk állítás („nem cselekszik Isten ellen”) változatlan. |
| D2.3 | B3: a vízforrás és áldás szerepe több helyen áll (5Móz 8:7, Péld 3:20, Zsolt 78:15, Ez 31:4) | **elfogadva** | **B11 — vízforrás és táplálás** (olvasat; adat a versek szava): 5Móz 8:7 („mély vizeknek földére … fakadnak”), Péld 3:20 („fakadtak ki a mélységből a vizek”), Zsolt 78:15 (inni ad), Ez 31:4 (a cédrust nagygyá neveli). A B3 kifejezés-szintű állítása (1Móz 49:25 = 5Móz 33:13) változatlan. |
| D2.4 | A B-táblából kimaradt helyek (Zsolt 36:7, 42:8, 77:17, 148:7, Hab 3:10, Ámós 7:4, Jób 41:32, Jel 9:11) | **elfogadva** | **B12 — Isten uralma és a mélység válasza** (olvasat): Zsolt 33:7, 135:6 (Isten tárháza, Isten akarata a mélységben), Zsolt 77:17 és Hab 3:10 (a mélység megrázkódik, „harsog” Isten láttán), Zsolt 148:7 (dicséretre hívják), Zsolt 36:7 (Isten ítéletei olyanok, mint a nagy mélység), Ámós 7:4 (az ítélet tüze megemészti). A Jób 41:32 a Leviatán nyomát mondja a mélységen (B7 mellé). A Jel 9:11: a mélységnek királya, angyala van (B9 mellé). A Zsolt 42:8 a B6b szerint. |
| D2.5 | Ez 26:20: a tehóm-verset a sírgödörbe szállók és „a mélységek országa” követi, más szóval | **elfogadva** | Az Ez 26:19 helye a B6b szerint áll (a Tíruszt elborító víz); az 1/a-mondata kimondja, hogy a következő vers más szóval a sírgödörbe szállást nevezi. „A halál mélye” erre a helyre nem áll. |
| D2.6 | A Hab 3:10 adatsorának Károli-szava („a víz-ár”) | **saját lelet, javítva** | A Hab 3:10-ben a „víz-ár” a zerem majim fordítása; a tehómot a Károli „a hullám”-mal adja („harsog a hullám”). Az `adat/elofordulasok.tsv` sorának `karoli_szo` mezője „a hullám”-ra javul (az 1/a-próza menetében, `manual` provenienciával). |

## D3. Az U3b igazításai (a kész 9. Hatástörténethez)

*2026-11-23, `claude-opus-5-5` (F239 U3b). A próza az U1b előtt készült; ez a szakasz azt rögzíti, mi változott az érvekben, miután a 9. blokk és a vitatott pontok szakirodalma (`adat/vitatott_forrasok.tsv`) elkészült. A lépések indoka: `naplok/F239_naplo.md`, „U3b”.*

| # | tétel | mi változik |
|---|---|---|
| D3.1 | A3: a 2Móz 15:5 görög szava | A tehóm megfelelője a πόντος („tenger”), a vers βυθός-a a mecólá fordítása (U1b, két kéz); a 2Móz 15:8-é κύματα. Az A3 sora és a Miért fontos „A Septuaginta hídja” rése javítva. |
| D3.2 | V3: „a kommentárirodalomban mindkét álláspont képviselt” | Kimarad a prózából. A mondat alapja a régi tanulmány ellenőrizetlen névsora volt; a vitatott pont szakirodalom-sora szerint a kérdésről lektorált forrás nem került elő (OpenAlex, Crossref, 2026-11-23), így a próza többet állítana az adatnál. A két olvasat és a döntés („a szócikk a kérdést nem dönti el”) változatlan. |
| D3.3 | V1: ugyanez a mondat | Marad: a szakirodalom-sor (Tsumura, JAOS 2021) pontosan erről a kérdésről két álláspontot mutat be. |
| D3.4 | V4: a D2.1 alkalmazása | A tény bővül a hét versre (καταβαίνω: Ez 31:15, Jób 36:16, Jób 38:30, Zsolt 107:26; ἀνάγω: Ez 26:19, Zsolt 71:20, 71:21; ellenőrizve: `naplok/F239_U3b_rom107_hatter.py`, n=7), a két zsoltár mint a legközelebbi a nyitott kérdés (a) olvasatában. Az elöljáró-eltérés csak a Zsolt 107:26-ra áll (ἕως τῶν ἀβύσσων ↔ εἰς τὴν ἄβυσσον); a Zsolt 71:20 ἐκ … ἀνήγαγες alakja a Róm 10:7 ἐκ νεκρῶν ἀναγαγεῖν szerkezetével nem ütközik, ezért a (b) olvasat érve a 107:26-ra szűkül. A Remez a hét verset tényként, a merítést nyitott kérdésként mondja, külön mondatban. |
| D3.5 | Az atyai tanúk (Jeromos ×4, Órigenész ×1) | A próza hallgat róluk (a 9. blokk a saját szavas mondatokat kimondja). A próza szöveg-szintű állításai („a szöveg nem mondja ki, hogy a mélység maga gonosz”; „a mélység nem cselekszik Isten ellen”) a szövegről szólnak, nem a recepcióról; Jeromos „rossz értelmű” mélysége (Hab 3:10-kommentár) és az 1Móz 1:2 ↔ Luk 8:31 azonosítása recepció, nem ellentmondás. |

## D4. Az U6 igazításai (a szerkesztő U5-döntései szerint)

*2026-11-23, `claude-opus-5-5` (F239 U6). A döntések szövege: `naplok/F239_dontesek.md` D2–D25; a lekérdezések: `naplok/F239_U6_lekerdezesek.py`.*

| # | tétel | mi változik |
|---|---|---|
| D4.1 | V3 (b): új bizonyíték (D16) | *A 2Móz 15-ben a mélység a tenger része, nem a világ alatti víz.* · **szövegtanú** · bizonyíték: a 2Móz 15:8-ban a mélységek „a tenger szívében” (בְּלֶב־יָם, H3820 + H3220) merevednek meg; a szomszédos 15:4 és 15:10 a tengerről (H3220) beszél, a 15:5 a fáraó tisztjeinek a tengerbe süllyedését folytatja. A próza mondata változatlan, a V3 (b) bizonyítéka ezzel kiegészül. |
| D4.2 | V2: a bezárás tárgya (D4, D18) | A Jel 20:3 bezárásának tárgya a Textus Receptusban a sárkány (αὐτόν, csak TR), a kritikai kiadásokban az ige tárgy nélkül áll; a pecsét (ἐπάνω αὐτοῦ) minden kiadásban a sárkány fölött. Az (a) olvasat bizonyítéka a jelentés-egyezés marad (szákar ↔ κλείω), de a próza kimondja, hogy a bezárás tárgya a két helyen más (források ↔ sárkány). A „szóbeli kapcsolat nincs” mondat kimarad (az elvetett „közös zár-ige hiánya” érv, D „Elutasított 3”); a (b) olvasat a görög szint hiányára szűkül (ἐπικαλύπτω). |
| D4.3 | V4: a hét vers (D15) | A hét versből háromban mondja a görög szöveg a mélységbe való leszállást vagy a mélységből való felhozást (Zsolt 107:26 καταβαίνουσιν ἕως τῶν ἀβύσσων; Zsolt 71:20 és 71:21 ἐκ τῶν ἀβύσσων … ἀνήγαγες); a többi négyben az ige a mélység szava mellett más mozgást mond (Ez 26:19 a mélységet hozza fel Tíruszra; Ez 31:15 a fa a hádészba száll; Jób 36:16 az asztal száll le; Jób 38:30 a víz száll le). A tény erre a háromra szűkül, a négy külön mondatban áll. A (b) olvasat „nem csak a két zsoltárban” érve ezzel elesik (a három vers a két zsoltáré); a (b) érve a 107:26 alakjára és elöljárójára, valamint a magyarázó mondatra szűkül. |
| D4.4 | B6, Drash (D7) | A Jón 2:6 a mélység körülzárásáról szól; a felhozás nem közös jegy (D „Elutasított 6”): a Jón 2:7 a szabadítást más szóval mondja (H5927 + H7845). A Drash második tétele a halál közelségére szűkül, a felhozás csak a Zsolt 71:20-é. |
| D4.5 | V1 (D17) | A próza kimondja, hogy a „nem cselekszik Isten ellen” hiányérv, és a demitologizált átvétellel is összefér (a D „V1” sor szerint); egyik olvasatnak sem döntő érve. |
