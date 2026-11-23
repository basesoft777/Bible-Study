# Bírálat: TEREMT-001 érvnaplója (`naplok/ERVNAPLO_TEREMT-001.md`)

*C-bi (`MUNKAMENET.md`), a `biralo` subagent kimenete, a hívó (#239 U2, `claude-opus-5-5`) mentette változatlanul, 2026-11-23. A bírált állapot: az ág 508aa565 commitja. A válaszok: az érvnapló D szakasza.*

Modell-ellenőrzés: a tényleges modellem `claude-sonnet-5-5` (Sonnet 5.5), a kért `sonnet`. Egyezik, a bírálat lefutott.

A bemenetben csak az érvnapló, a bizonyítéklap és a határ volt. Igeszakasz-tanulmány-blokk és lapmondat (Kivonat, Remez, Sod, Módszertan) nem érkezett. Ezért a 5. kérdés (a lap két helyének ellentmondása) mindenhol **lekérdezendő a próza után**.

A „TAHOT/TAGNT-sor" és a „BDB" jelölés a `konkordancia/` datasetjeire utal.

## V1. A tehóm és Tiámat

**Súlyos**

- **A6 és V1(a), 2. és 3. kérdés.**
  - **Gyengeség.** Az A6 „sohasem áll kiírt névelővel" így nem tartható, és V1(a) támasznak használja.
  - **Fedezet a kijelentés alatt.** A számlálás csak a különálló H9009 tokent látja. Két versben az olvadt névelő meg van jelölve az adatban:
    - Zsolt 106:9: TAHOT `H9003 בַּ ba. „in the"` + H8415.
    - Ézs 63:13: ugyanez.
    - BDB, H8415: „׳בַּתּ Isa 63:13 + Psa 106:9 (only here with article)".
  - **Nem megkülönböztető.** A névelőtlenség a közszavaknál is gyakori. A Zsolt/Jób/Péld könyvekben a névelőt viselő előfordulások:
    - H8415: 1 a 20-ból.
    - H4325 (víz): 8 a 92-ből (kb. 9%).
    - H3220 (tenger): 19 az 53-ból.
    - H8064 (ég): 41 a 103-ból.
    - H7585 (seól): 0 a 33-ból. A seól éppen a nem-tulajdonnév, mégsem kap névelőt.
  - **Kezelés.** A „korlát" megjegyzés elfedi, hogy a hiány nem az „istenségnév-szerűséget" jelzi, és a próza által kiírt „kiírt névelő" kifejezés félrevezető. A számlálás durva (a „the" glosszát keresi), a kérdés szempontjából elég.
  - **Bizonyíték.** Lekérdezések: 1, 2, 3.

**Közepes**

- **1. és 6. kérdés.** A V1(b) szövegtanúja hiányérv („35 versben sehol nem alanya Isten elleni cselekvésnek"), és nem megkülönböztető: a „demitologizált átvétel" olvasattal is összefér, mert az is a konfliktus hiányát jósolja. Az érv a másik olvasatot nem cáfolja, csak a „nyers mítosz-ellenfél" változatot. Ellenpélda ugyanabból a halmazból: Zsolt 148:7 (a tehóm és a tannín egy versben, kollokáció H8415+H8577 n=1; a tehóm dicsér); Jón 2:6 (a tehóm körülveszi az embert); Zsolt 42:8 (a tehóm hívja a tehómot). A „nem ellenfél" szűkebb állítás: Isten ellen nem cselekszik. Bizonyíték: bizonyítéklap versenként; 6. lekérdezés.
- **6. kérdés.** A „nyelvi rokonság szótári tény" állítás nincs a repó adatában. A BDB H8415 szócikkében nincs Tiámat vagy szemita rokon szó; a „Tiamat" a BDB-ben csak a Livyathan szócikkben áll. A `BDB_rokon_irasok.tsv` nem tartalmaz H8415-sort. A BDB a Gunkel-művet (*Schöpfung u. Chaos* 21 ff.) a tehóm-kozmogóniánál idézi, ez a Gunkel-hivatkozás egyetlen adatbeli alátámasztása. A rokonság „szótári tény" jelölése lekérdezendő külső forrásnál. Bizonyíték: 4., 5. lekérdezés.
- **6. kérdés.** Wenham és Cassuto a V1(b)-ben a régi tanulmányból valók; a V3-nál lévő óvatosság (a próza ne tulajdonítson konkrét mondatot) a V1-nél hiányzik. Ugyanaz a szabály kell.

**Enyhe**

- **4. kérdés.** A V1(b) „szövegtanú + recepció" egy tételben áll. Szét kell választani: a szövegtanú a Zsolt 148:7 és a 35 vers, a recepció Wenham és Cassuto.
- **Eldöntött rész.** „A szövegben a mélység nem ellenfél" a fenti szűkítéssel (nem Isten elleni cselekvő) áll meg.

**Elutasított tételek:** A6 mint „sohasem áll névelővel"; A6 mint a tulajdonnévszerűség támasza; „szótári tény" a rokonságra, repó-forrás nélkül.

## V2. Jel 20:1–3 és az 1Móz 8:2

**Közepes**

- **3. és 4. kérdés.** A V2(b) „közös zár-ige hiánya" érv csak a Septuaginta szintjén áll. TAHOT 1Móz 8:2: `H5534 יִּסָּֽכְרוּ „they were shut up"`; Károli: „bezárulának". Az érvnapló B2-je maga „bezárás"-t mond, a V2(b) viszont a görög ἐπεκαλύφθησαν („befed") miatt tagadja az azonos igét. A V2(b) „szövegtanú" valójában Septuaginta-recepció, nem az 1Móz 8:2 szövegéé. Bizonyíték: 7., 10. lekérdezés.
- **2. kérdés.** A B9 „kulccsal megnyitják és kulccsal bezárják" és a V2(b) „a kulcs-pár a könyvön belül zárul" a Jelenések általános szóhasználata, nem tehóm-specifikus: ἀνοίγω és κλείω egy versben a Jel 3:7-ben is; κλείς 6 versben (Jel 1:18, 3:7, 9:1, 20:1, Mt 16:19, Luk 11:52); κλείς és ἄβυσσος együtt 2 versben (Jel 9:1, 20:1); ἄβυσσος és κλείω együtt 1 versben (Jel 20:3). A kulcs-pár tény marad, de a nyit–zár ige a könyv általános szókincse.
- **3. kérdés.** A V2(a) kiegészítése pontos: az LXX-ben a mélység forrásaihoz ἐρράγησαν áll, az égcsatornákhoz ἠνεῴχθησαν. A TAHOT szerint a héberben is a mélység forrásaihoz „hasadás" (H1234 נִבְקְעוּ), az éghez H6605 „megnyit" áll. A „megnyit" ige a tehómhoz egyik nyelvben sem kapcsolódik. Bizonyíték: 8., 10. lekérdezés.

**Enyhe**

- **7. kérdés.** A V2(a) „nyitás 7:11 ↔ Jel 9:1–2, zárás 8:2 ↔ Jel 20:3" láncon átívelő keretet ad: értelmezés, az érvnapló helyesen recepcióként jelöli. A „keret" szó a lapon nem kerülhet [adat] jelzés alá.

**Elutasított:** „a közös zár-ige hiánya" mint ellenérv (a héber és a Károli ugyanazt az igét hozza); „a Jelenések saját kulcs-párja" mint a Genezis-kapcsolat ellenérve.

## V3. A Tengeri ének és az özönvíz

**Közepes**

- **3. kérdés.** A „forrás+mélység" a H4599-cel három versen áll (1Móz 7:11, 8:2, Péld 8:24), de a „forrás" más tőből is áll a tehóm mellett: H8415+H5869 (עַיִן) 5Móz 8:7 és Péld 8:28 (n=2). A Péld 8:24-ben nem „a mélység forrásai" áll, hanem „víztől teljes források" a mélységek mellett, tehát az „ugyanaz a kifejezés" csak az 1Móz 7:11-re és 8:2-re mondható. A V3(b) érve változatlan, a B2 bizonyítéka viszont túlszámlálja a kifejezést. Bizonyíték: 15., 16. lekérdezés.
- **6. kérdés.** A Cassuto/Sarna/Levenson/Childs a régi tanulmányból való, ellenőrzés nélkül (a V3 jelzi, a V1 nem).

**Enyhe**

- **1. kérdés.** A „többes szám, nem egyes szám" nem megkülönböztető: az 5Móz 8:7 és a Zsolt 106:9 is többes, és nem Genezis-visszautalások. Ez a gyengébb érv.

## V4. Róm 10:7 csere

**Közepes**

- **2. kérdés.** Az ἀναβαίνω a Róm 10:6-ban az 5Móz 30:12-ből származik (LXX 5Móz 30:12: τίς ἀναβήσεται … εἰς τὸν οὐρανόν; Róm 10:6 ugyanez), tehát nem a Zsoltár mellett szól. LXX 5Móz 30:13: τίς διαπεράσει … εἰς τὸ πέραν τῆς θαλάσσης; Róm 10:7: τίς καταβήσεται εἰς τὴν ἄβυσσον. Csak a καταβαίνω + ἄβυσσος párosítás új. Bizonyíték: 17., 18., 21. lekérdezés.
- **4. kérdés.** Az „eldöntve: a Róm 10:7 szavai a görög Zsolt 107:26 és 71:20 szavai" nem pontos: a Zsoltárban ἕως τῶν ἀβύσσων (többes, ἕως), a Róm-ban εἰς τὴν ἄβυσσον (egyes, εἰς). Pontos tény: Zsolt 71:20 LXX ἐκ τῶν ἀβύσσων … ἀνήγαγές és Róm 10:7 ἀναγαγεῖν: azonos tő (ἀνάγω); Zsolt 107:26 LXX καταβαίνουσιν ἕως τῶν ἀβύσσων és Róm 10:7 καταβήσεται εἰς τὴν ἄβυσσον: azonos tövek, eltérő alak és elöljáró. A V4(a)-ban a szövegtanú és a függés feltevése egy tételben áll. Bizonyíték: 19., 20. lekérdezés.
- **3. kérdés.** A Zsolt 107:26 környezete a tengeri vihar („az égig emelkedének, a fenékig sülyedének"); ez a tengeri kép az 5Móz 30:13 „tengeren túl"-jával rokon, de az érvnapló nem használja. Lekérdezendő, hogy ez a környezeti egyezés magyarázza-e a cserét.

**Enyhe**

- **5. kérdés.** Az „eldöntve" szókincs-egyezés és a „nem tudni, szándékos-e" egy mondatban hangzik el; a lap Kivonat- és Remez-mondata ezt nem keverheti. Lekérdezendő a próza után.

**Elutasított:** „ugyanazt a két igét" mint a függés érve; „a Róm 10:7 szavai a Zsolt 107:26 szavai" ebben az alakban.

## V5. A halál mélye, a tehóm és a seól

**Közepes**

- **2. kérdés.** A B6 és a V5 „a halál mélye" csoportja (Jón 2:6, Zsolt 71:20, 107:26, Ez 26:19, 31:15) túlterhelt. A BDB a helyeket más jelentéssel olvassa: Ez 26:19 „(deep) sea, overwhelming Tyre"; Ez 31:4 és 31:15 „deep, of river (Nile)"; Zsolt 107:26 „poetic of hollows of great waves"; Zsolt 71:20 „abyss (si vera lectio) … = Shejôl"; Zsolt 42:8 „possibly here of Jordan". A tehómhoz mavet, mut, shachat vagy bór együtt-előfordulás egy versben nincs (H8415+H4194, H4191, H7845, H0953: mind n=0). A seól csak az Ez 31:15-ben áll a tehóm mellett. A „felhoz" a Jón 2:7-ben áll (verem), nem a tehóm-versben. Csak a Jón 2:6 és a Zsolt 71:20 áll igazoltan a halál oldalán; a B6 „ahonnan Isten felhoz" az Ez 26:19-re és 31:15-re nem illik. A V5 negatív következtetése (a tehóm nem a holtak lakóhelye) áll; a „több helyen a halál képe" öt helyre kiterjesztve nem. Bizonyíték: 4., 22–27. lekérdezés.
- **Belső következetlenség.** A határ (`F239_hatar.md`, 3. szakasz, (e) csoport) a Zsolt 42:8-at is a halál mélyéhez sorolja, a B6 nem.

**Enyhe**

- **4. kérdés.** „Az ÚSZ ἄβυσσος-a közeledik a hádészhez" a Róm 10:7-re épül; a Luk 8:31 és a Jelenések ἄβυσσος-a börtön (B9), nem a halottak helye. Az állítás egy versre szól, nem az ÚSZ-re általában.

**Elutasított:** „Ez 26:19 és Ez 31:15 a halál mélye" mint láncbeli szerep (B6); a B6 „ahonnan Isten felhoz" mint a csoport közös jegye.

## V6. A Genezis négy helye

**Közepes**

- **3. kérdés.** A B1 és a hipotézis (a) csoportja a Péld 8:24-et is a „teremtés előtti állapot és a formálás anyaga" alá sorolja, pedig a Péld 8:24 szerint („Még mikor semmi mélységek nem voltak, születtem vala") a tehóm *még nem létezik*. A „teremtés előtti állapot" és a „megteremtett mélység" két külön regiszter. A B1 „formálás anyaga" is értelmezés (az 1Móz 1:2 nem mondja, hogy a tehómból formál).
- **1. kérdés.** A „szándékos" kihagyása helyes. A négy funkció (teremtés, ítélet, helyreállítás, áldás) értelmezői besorolás, nem szöveg-adat; a B2 (megnyitás és bezárás) és a B3 (áldásforrás) szövegtanú.

## Általános tételek

**Enyhe**

- **A7 / hipotézis, 2. kérdés.** A „nagy/sok" társszó 8 verse nem mind a „nagy mélység": a H7227 csak az 1Móz 7:11, Zsolt 36:7, 78:15, Ámós 7:4, Ézs 51:10 versekben jelzi a tehómot; a Zsolt 71:20, Ez 26:19, Ez 31:15 versekben nem. A „nagy mélység" frázis 5 versre szól.
- **7. kérdés.** B2, B5, B9 „kötés", „keret", „megnyitás és bezárás" értelmezés. Csak a szóismétlés [adat]: H8415+H4599 (1Móz 7:11, 8:2, Péld 8:24), H8415+H7257 (1Móz 49:25, 5Móz 33:13), G0012+G2807 (Jel 9:1, 20:1).
- **5. kérdés (összefoglaló).** A próza után lekérdezendő: (a) V1: a Kivonat „a szövegben a mélység nem ellenfél" mondata és a Vitatott pont „nyitva" egyezik-e; (b) V2: a Remez nem mondja-e, hogy a Jel 20 „megismétli" a 8:2-t; (c) V5: a Sod és a Módszertan nem mond-e „a halál mélye"-t az Ez 31:15-re.
- **6. kérdés (összefoglaló).** A V1 és V3 szerzőnevei a régi tanulmányból valók; az egyetlen, a repó adatával alátámasztott név a Gunkel (BDB, *Schöpfung u. Chaos* 21 ff.).

## Elutasított tételek összegzése (a lektornak és a felhasználónak)

1. A6: „a tehóm sohasem áll névelővel" (a Zsolt 106:9 és az Ézs 63:13 határozott, BDB és TAHOT szerint) és mint a tulajdonnévszerűség támasza.
2. V1(a): „a nyelvi rokonság szótári tény" (a repóban nincs ilyen szócikk-adat).
3. V2(b): a „közös zár-ige hiánya" mint ellenérv (a héber 8:2 „bezár", a Károli is).
4. B9 / V2(b): a kulcs-pár mint motívum-specifikus (a κλείς és az ἀνοίγω/κλείω a Jelenések általános szókincse).
5. V4(a): „ugyanazt a két igét" (az ἀναβαίνω az 5Móz 30:12-ből való) és „ugyanazok a szavak" (alak és elöljáró eltér).
6. B6 / V5: az Ez 26:19, 31:15 és a Zsolt 107:26 mint „a halál mélye" szerep; a „felhoz" közös jegye.
7. Hipotézis (a) / B1: a Péld 8:24 „teremtés előtti állapot"-ként (a vers szerint a mélységek még nem voltak).

## Lekérdezési napló (összefoglalva)

30 lekérdezés (`lekerdez.py` scan / kollokacio / lxx-hid, a TAHOT/TAGNT/BDB célzott olvasása `split('\t')`-tel), pontonként legfeljebb 10: V1 7, V2 8, V3 2, V4 5, V5 7. A főbb eredmények a fenti tételeknél, a számokkal. **Lekérdezendő (nem futott, nem tényként):** az A3 „30 a 35-ből" független ellenőrzése; a V1 és V3 szerzőinek mondatai a repón kívül; hogy a Targum vagy más forrás magyarázza-e a Róm 10:7 cseréjét.

*(proveniencia: scope=TEREMT-001 érvnapló V1–V6, A–D szakasz; bizonyíték: `naplok/BIZONYITEK_TEREMT-001.md`, `naplok/F239_hatar.md`; konkordancia: TAHOT_kivonat.tsv, TAGNT_kivonat.tsv, BDB_teljes_unabridged.tsv, LXX_OS | forras=modell:claude-sonnet-5-5 (biralo) | ts=2026-11-23T13:10Z)*
