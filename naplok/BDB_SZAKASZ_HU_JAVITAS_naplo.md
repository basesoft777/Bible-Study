# BDB magyar szakaszillesztés javítása — napló (F144, FELADATOK #144)

*Brief: `F144_BDB_SZAKASZ_HU_JAVITAS_BRIEF.md` · modell (kért): opus · modell (tényleges): `claude-opus-5-5` · ág: `claude/f144-bdb-szakasz-0e8dfd` · kiinduló HEAD: `9cf0e43a`*

## M0 — újramérés, soronkénti átnézés, javasolt szabály (2026-11-01) ⛔

Az M0 adatot nem ír: a `adat/bdb_szakasz_hu.tsv`, a `adat/forditasok.tsv`, a `adat/bdb_szakaszok.tsv` és a `hu_illeszt.py` változatlan.

proveniencia: `scope=adat/bdb_szakasz_hu.tsv (repó) + a hu_illeszt.py mai bemenetből memóriában generált tábla | forras=naplok/BDB_SZAKASZ_HU_JAVITAS_M0_hatas.py (szabályváltozatok) + ad hoc kivonat (a 20 szócikk soronként, scratchpad) | ts=2026-11-01`

Bemenetek (a futás elején rögzítve; sha256 sorvég-független, `hu_illeszt.sha256_fajl`, első 12 jegy; sha1 bájtra):

| fájl | sha256 (LF) | sha1 |
|---|---|---|
| `adat/forditasok.tsv` | `8d3bc51a3690` | `af1103869e69` |
| `adat/bdb_szakaszok.tsv` | `66bd24b9abb6` | `5a83564dd160` |
| `adat/bdb_szakasz_hu.tsv` | `e2cb5e21e0c0` | `8b80639c86fa` |
| `adat/bdb_vers_jelentes.tsv` | `487607da93b8` | `247805b6fbc3` |
| `eszkozok/bdb_jelolt/hu_illeszt.py` (kód-hash) | `2d8c2a60ab1c` | — |

### 1. Újramérés

**A repóbeli tábla és a mai bemenet.** A repóbeli tábla 674 Strong / 9 664 sor (a 2026-10-18-i generálás; részlegesen frissítve: H4397, H8034, H9004, 2026-10-29, DT423). A jelentés A-feltétele (`illeszkedik`, van `jel`, a `szoveg_hu` legfeljebb a jelölő + 3 karakter) rajta ma is **26 sor, 26 Strong**, a B-kör 79 sor / 70 Strong; a jelentés számai tehát változatlanok.

A mai bemenetből generálva (memóriában, nem írva) a tábla 4 000 Strong / 25 228 sor: ez az N-F131f (a tábla elavult, 3 326 új Strong, 98 változó). A fordítás típusa szerint (`szakasz_bemenet.strong_magyar_sorok`):

| típus | Strong (repó / mai) | A-sor (repó) | A-sor (mai) | B-sor (repó / mai) |
|---|---|---|---|---|
| `teljes` (egy darabban fordított) | 576 / 576 | 15 | 15 | 67 / 67 |
| `szakasz` (szakaszonként fordított) | 98 / 3 424 | 11 | 29 | 13 / 111 |

**A `teljes` típusú 576 Strong repóbeli sorai bájtra azonosak a mai kód kimenetével** (a proveniencia `ts`-e nélkül, mind a 13 adatoszlop): a javítás e Strongokon tisztán mérhető, és a `--strong` részleges frissítés sorkulcs-feltétele teljesül. A repó 98 `szakasz` Strongja a mai kimenettől mind eltér (N-F131f).

**A 20 szócikkből kiesett 5**, mert közben szakaszonkénti fordítást kapott (a régi `teljes` soruk `elavult`, a `sz<n>` sorok élnek): **H3423, H3603, H5324, H7122, H7896** (mind a (b) csoportból). A brief szerint a szakaszonként fordított Strong nincs a hatókörben. Megjegyzés: a mai generálásban ezek A-sora megmarad (H3423 9 `3`, H3603 5 `3`, H5324 15 `3`, H7122 5 `2`, H7896 8 `3`), mert a szakaszos típust ma is a regex-illesztő kezeli; ez az N-F131g (csoporthatár-illesztés) tárgya.

**Marad 15 szócikk**, mind `teljes` típusú.

### 2. Soronkénti ítélet (15 szócikk)

Minden sorra: a forrás angol szövege (`bdb_szakaszok.tsv`), a magyar szöveg a jelölő körül, és a szomszédos sorok. „EN üres” = a forrássor `szoveg`-e (címkék nélkül) legfeljebb 8 karakter.

| Strong | csoport | sor (`jel`) | valódi ok | ítélet | a javított illesztő eredménye |
|---|---|---|---|---|---|
| H0001 | (c) | 3 (`1`), 4 (`2`) | a fejléc „szabeus אב CIS^iv, 1, 37 1. 2 és mások” számtöredékéhez kötött jelölők; az 1. pont a 2. sorba, a fej folytatása is oda került | **hiba** | 2: a fej a „37 1. 2 és mások, etióp …” résszel; 3: „1 az egyén atyja 1Móz 2:24 …”; 4: „2 Istenről mint népe atyjáról …” (R2) |
| H2199 | (c) | 13 (`Hiph`il`), 14 (`1`) | a „hadi szolgálatra hívatik, a Hiph`il 1. szenvedője” említéséhez kötött; a forrásban ez a 12., jelölő nélküli sor eleje, a valódi Hiph`il-szakasz később jön | **hiba** | 13: „Hiph`il imperfectum וַיַּזְעֵק Bír 4:10 …”; 14: „1 hív, kihív, vagy egybehív …” (R4) |
| H5027 | (c) | 3 (`Pi`el`), 4 (`Hiph`il`) | a fej „ige Pi`el, Hiph`il néz (késői héber Pi`el …” felsorolásához kötött | **hiba** | 2: a fej teljes; 3: „Pi`el perfectum consecutivummal וְנִבַּט Ézs 5:30 …”; 4: „Hiph`il perfectum הִבִּיט 4Móz 21:9 …” (R4) |
| H7043 | (c) | 15 (`3`), 16 (`Pu`al`) | a `3` a Pu`al-paradigma nyelvtani személyéhez („Pu`al imperfectum) 3. hímnemű”) kötött, a valódi „3 a dolog tárgyesetével” a kapunak nem jelölő („23 3 a”); a Pu`al ezért `horgonnyal` | **hiba** | 15 (`horgonnyal`): „3 a dolog tárgyesetével 1Móz 8:21 …”; 16 (`illeszkedik`): „Pu`al imperfectum) 3. hímnemű egyes szám …” (R3x) |
| H3381 | (c) | 37 (`Hiph`il`) | a forrásban „(see Hiph`il above)” félkövér törzsneve külön sort nyitott (EN „above)”); a magyar „(l. fent Hiph`il)” | nem illesztőhiba (szakasztábla-műtermék) | változatlan; indokolt kivétel |
| H5060 | (c) | 10 (`Niph`al`) | „see נגף Niph`al”: a félkövér törzsnév külön sort nyitott, EN üres | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel |
| H6499 | (c) | 8 (`b.`) | „— both b. and c. Num 8:12”: a félkövér visszautaló betűk külön sort nyitottak (EN „and”, ill. „Num 8:12”); a magyar „mind b. és c. 4Móz 8:12” ugyanígy | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel |
| H5826 | (b) | 8 (`Qal.`) | a záró „see Qal.” törzsneve külön sor, EN üres; a magyar „l. Qal.” | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel |
| H6299 | (b) | 15 (`Niph`al`) | záró „see Niph`al”, EN üres | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel |
| H7378 | (b) | 11 (`Hiph`il`) | záró „see ארב Hiph`il”, EN üres | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel |
| H7650 | (b) | 15 (`Niph`al`) | záró „1Sam 20:17 see Niph`al”, EN üres | nem illesztőhiba (műtermék) | változatlan; indokolt kivétel (a 11., 12. sor az R4-gyel változik, l. 4.) |
| H3499 | (a) | 3 (`1`) | csoportcím: a forrásban az `1` sora üres, utána „a.”, „b.” | nem hiba (szerkezeti) | változatlan |
| H4519 | (a) | 3 (`1`) | csoportcím, EN üres | nem hiba (szerkezeti) | változatlan |
| H6965 | (a) | 46 (`2`) | csoportcím (Hiph`il 2.), EN üres | nem hiba (szerkezeti) | változatlan |
| H7130 | (a) | 3 (`1`) | csoportcím, EN üres | nem hiba (szerkezeti) | változatlan |

**Összegzés.** A 15-ből **4 valódi illesztőhiba** (H0001, H2199, H5027, H7043). A többi 11 sor forrássora maga is (szinte) üres: a (a) csoport szerkezeti csoportcím, a többi a bontó műterméke (félkövér visszautalás — „see Qal.”, „see Hiph`il above”, „both b. and c.” — külön sort nyit). Ezeknél a magyar oldal pontosan a forrás szerkezetét tükrözi; a hiba, ha az, a szakasztáblában van, amely a brief szerint nem módosítható (`bont.py` kívül esik). **A jelentés (b) típus-magyarázata („a jelölő szövegközi számhoz vagy törzsnévhez kötődött”) a megmaradt négy (b) szócikkre nem áll**: mindegyik üres forrássor.

### 3. Javasolt javítási szabály

Három szűk szabály (a mérőszkript a hatását a `teljes` és a `szakasz` típuson külön méri; „változó sor” = a kategória vagy a `szoveg_hu` változik):

- **R2 — vesszős kötetszámú siglum utáni számsor nem jelölő.** A magyar jelölő előtti 40 karakter végén `\^[ivx]+,(?:\s?\d+[.,]?)+\s$` (pl. „CIS^iv, 1, 37 ”, „CIS^iv, 1, 37 1. ”). A meglévő `SIGLUM_ELOTT` („Kö^ii. 1. 104”) kiterjesztése a vesszős alakra. Szándékosan nem fogja a pontos siglum utáni lapszám + mondatvég esetét („Survey^ii. 305. 2 hely …”, H1008; „Kö^ii. 320. 6 …”, H6440; H0357, H1053), mert ott a jelölő valódi — egy tágabb első változat ezeken ép sort rontott volna. Hatás: `teljes` 3 sor / 1 Strong (H0001), `szakasz` 0.
- **R4 — a törzsnév-jelölő a forrás szerinti előfordulás-indexéhez kötődik.** Ha a forrásban (a sor előtti sorok `jel` + `szoveg` mezőiben, címkék nélkül) *k* azonos törzsnév áll a sor előtt — fej-felsorolás, „Late Hebrew Pi`el”, „see Niph`al 3”, „passive of Hiph`il” —, a magyarban a (*k*+1)-edik előfordulás a jelölő; ha ilyen nincs, vagy a kurzor előtt van, a mai viselkedés marad. Csak törzsnévre (a számok előfordulása a fordításban nem követi a forrást). Hatás: `teljes` 46 sor / 21 Strong, `szakasz` 165 sor / 77 Strong; a kategória-eloszlás mindkét típuson változatlan.
- **R3x — előretekintés a következő törzsnévig.** Nem törzsnév-jelölőt (szám, betű) nem köt az illesztő olyan helyre, amely előtt (a kurzortól) már a következő jelölős sor törzsneve áll — a törzsnév helyét az R4 indexével számolva. Hatás: `teljes` 3 sor / 1 Strong (H7043), `szakasz` 140 sor / 14 Strong (`elakad` 665 → 579).

**Együtt (R2 + R4 + R3x):** `teljes` **52 sor / 23 Strong**, a kategória-eloszlás változatlan (`illeszkedik` 5 218, `horgonnyal` 104, `jelolo_nelkul` 1 988), az A-sor **15 → 11**; `szakasz` 305 sor / 90 Strong, `elakad` 665 → 578, A-sor 29 → 21.

A 23 `teljes` Strong: H0001, H2199, H2803, H2930, H3198, H3427, H3782, H3885, H3920, H5027, H5157, H5647, H5782, H5975, H6381, H6912, H6999, H7043, H7126, H7650, H7665, H8085, H8334.

**Elvetett változatok** (mérve, ugyanazzal a szkripttel):

| változat | `teljes`: változó sor / Strong | miért elvetve |
|---|---|---|
| R1: a törzsnév csak tagolásjel után jelölő (mint a `BETU_J`) | 241 / 68, `elakad` 0 → 64 | a mai mondatközi törzsnév-illesztések többsége **helyes**: a bontó a forrásban is minden félkövér törzsnévnél sort nyit („(Qr Qal participle)”, „+ Qal infinitive absolute”, „l. עבר Hiph`il a vége felé”); a szabály ezeket rontaná |
| R1 + kivétel üres forrássorra | 226 / 64 | ugyanaz |
| R3: általános előretekintés | 526 / 102, `elakad` 0 → 183 | a következő jelölő (szám) szövegközi előfordulása miatt ép sorokat utasít el |
| R3t: előretekintés csak törzsnévig, index nélkül | 15 / 5 | ép sorokat ront (H3559 12, H4390 11, H7843 6 → `elakad`), mert a következő törzsnév korábbi említése („l. Hiph`il”) elé esik a jó találat |

### 4. A változó sorok átnézése (`teljes`, 52 sor)

Mind az 52 sort átnéztem (régi ↔ új `szoveg_hu` eleje ↔ a forrássor angol eleje). **Romló sor nincs.** A változás négy fajtája:

1. **a 4 hibás szócikk javul** (H0001, H2199, H5027, H7043; l. 2.);
2. **fej-felsorolás**: a fej a törzsnév-felsorolással együtt teljes lesz, és az első törzsnév-sor a valódi paradigmával kezdődik (H3198, H5027, H6381, H6999, H8334, H5647);
3. **„l. Niph`al 3”-típusú visszautalás**: a visszautalás az előző szakasz végén marad, ahogy a forrásban (H2803, H2930, H3920, H5157, H5975, H3782 12 → „(l. még Hiph`il …”), a következő törzsnév-szakasz pedig a paradigmával kezdődik (H3427, H3782, H3885, H6912, H7126 21, H7665, H8085);
4. **a szakasz vége igazodik** egy javult szomszédhoz (H3782 5, H3427 11, H7043 14, H5782 13: „Qal l. ott); participium …”, H7650 12: „Niph`al olv. תִּשָּֽׁבְעוּ …”).

**Megmaradó, nem ide tartozó hiba** (a változó sorok között, de a kezdetük a javítás előtt és után is rossz): H5782 9 (`1`), H7650 11 (`1`), H7126 19 (`2`) a ragozási paradigma nyelvtani személyével kezdődik („1. egyes szám …”, „2. hímnemű …”). Ez a DT423 / N-F131g (1) hibaosztálya; a DT423 a célzott személy-szabályt elvetette. A javítás itt csak a sor *végét* igazítja.

**A megmaradó 11 A-sor** mind indokolt kivétel (2. pont): mindegyik forrássora legfeljebb 8 karakter. Javaslat az elfogadási feltétel mérhető alakjára: **A′ = A, és a forrássor `szoveg`-e (címkék nélkül) 8 karakternél hosszabb.** A `teljes` típuson A′ a javítás előtt 4 sor (a 4 hiba), utána 0. A repó teljes tábláján ma A′ = 14: a további 10 a szakaszos típusé (H1129 4, H1980 23, H3423 9, H3603 5, H5324 15, H7122 5, H7200 54, H7725 64, H7896 8, H7971 33), a hatókörön kívül (N-F131f/g).

**`szakasz` típus (nem írandó, csak tájékoztatás).** A 305 változó sorból 23 rekordot szúrópróbával néztem át (minden 13.): mind javulás vagy semleges (pl. H5674 c./d./f./2/d. `elakad` → helyes `illeszkedik`; H3423 10 Niph`al; H2263, H2710, H3722, H5106, H6087, H6958, H7326 a paradigmával kezdődik; H1692 12 a „passive of Hiph`il” forrásvéggel zárul). A típus a #144 hatókörén kívül esik (N-F131g); a kód viszont közös, ezért a szabály a következő teljes generáláskor (N-F131f) ezekre is hat.

### 5. Az M2 menete (javaslat) és a lexikon

- A DT423 szerint a teljes újragenerálás az N-F131g után jön. A `--ts` teljes futás ma 3 326 új Stronggal az N-F131f-et is elvégezné. **Javaslat:** az M2 a `hu_illeszt.py --strong` részleges frissítéssel csak a 23 változó `teljes` Strongot írja (a DT423 H8034-mintája szerint, a fejlécben jelölve). A sorkulcs-feltétel teljesül (1. pont).
- A brief M1 feltétele („a meglévő `teszt_bont.py` is zöld”) ma a main-en sem teljesül: a `HuIlleszt` két tesztje (`test_osszefuzo_a_mai_adaton_valtozatlan`, `test_ellenoriz`) az N-F131f miatt piros. Az M1 csak azt vállalhatja, hogy a #144 nem okoz új piros tesztet.
- **Lexikon:** az M0 adatot nem változtat, ezért nem kell újragenerálni. Az M2 után a 23 Strong `bdb_szakasz_hu.tsv`-sorai változnak; azok lexikonlapjai (és a BDB-nézet) újragenerálást kérnek — ezt a #152-vel kell összehangolni, a #144 nem generál.

### 6. Döntési pont ⛔ (a felhasználóé)

1. A javítási szabály: **R2 + R4 + R3x** (3.) — jóváhagyás, módosítás vagy elvetés. Az R3x a H7043-at javítja, és a nyelvtani személy osztályát egy más úton (előretekintés a következő törzsnévig) érinti; a DT423 („új szabály nem keresendő”) a személy-szabályra vonatkozott, ezért külön jóváhagyást kér.
2. Az M2 hatóköre: részleges frissítés a 23 `teljes` Strongra (javasolt), vagy a teljes újragenerálás (= N-F131f, a DT423 sorrendjével ellentétes).
3. A 11 megmaradó sor indokolt kivétel (üres forrássor), és az elfogadási A-feltétel az A′ alakban mérendő.
4. A bontó műterméke (a félkövér visszautalás külön sort nyit: „see Qal.”, „see Hiph`il above”, „both b. and c.”) a #144-en kívül esik; új N-tétel legyen-e (a `bont.py`-é, a #128 / #131 területe)?

**A döntés (DT-F144a), 2026-11-01.** A felhasználó az orkesztrátor chatjében a 6. pont három részdöntésére egyenként, az orkesztrátor javaslatát idézve felelt: „mehet” (az orkesztrátor `local_2bdbd92d` üzenetében idézve). (1) A szabály R2 + R4 + R3x; az R3x-et külön is jóváhagyta, mert más úton jár, mint a DT423-ban elvetett személy-szabály. (2) Az M2 részleges frissítés, csak a 23 `teljes` Strongra (`--strong`, a DT423 H8034-mintája szerint); a teljes újragenerálás később. (3) A 11 megmaradó sor indokolt kivétel, az elfogadási feltétel az A′ alak. A 4. kérdésről (a `bont.py` N-tétele) nem volt külön döntés, ezért a #144 nem veszi fel. Előzmény: egy korábbi, összevont jóváhagyást („döntsük el kivéve 125”) a felhasználó visszavont („minden visszavonok”), a fenti az újra, egyenként hozott döntés.

## M1 — a szabály a `hu_illeszt.py`-ban, tesztek (2026-11-01)

Kiinduló állapot: a main beolvasztva (`b822386a`; a merge a `adat/forditasok.tsv`-t is hozta: sha256 `7c43b398dfa3`, sha1 `11c1f4e5a1ab`, a #38 12. adagja). A 23 Strong a mai bemenetben is mind `teljes` típusú, és repóbeli sorai (468) bájtra azonosak a régi kód mai kimenetével (`ts=2026-10-18`): a részleges csere sorkulcs-feltétele teljesül.

- `eszkozok/bdb_jelolt/hu_illeszt.py`: (5) `SIGLUM_SOR` (R2) a `magyar_jelolok` szűrőjében; `torzs_index` (a forrás szerinti törzsnév-index); a `strong_illeszt`-ben az R4 és az R3x (a sorok előtti forrásszöveg: `jel` + `szoveg`, címkék nélkül). A `reszleges_szoveg` a korábbi részleges frissítések jelölését megtartja (eddig a H4397, H8034, H9004 jelölése egy újabb `--strong` futáskor elveszett volna), az azonos Strong-halmazé cserélődik.
- **Egyezés az M0-mérővel:** az új `strong_illeszt` mind az 5 696 fordítással bíró Strongon (a táblában lévő 674-en) azonos a `naplok/BDB_SZAKASZ_HU_JAVITAS_M0_hatas.py` R2+R4+R3x változatával (0 eltérés). A régi kódhoz képest változik: `teljes` 23 Strong (pontosan a 6. pont listája), `szakasz` 101 Strong (nem íródik; a mai bemenet több szakaszos Strongot hoz, mint az M0-kori 90).
- `eszkozok/bdb_jelolt/teszt_hu_illeszt.py` (9 teszt, zöld): R2, R4 (indexszel és index nélkül), R3x, a részleges jelölés megtartása; valós adaton H0001 (fejléc-számtöredék), H2199 ((b), törzsnév-említés), H7043 ((c), R3x), H3499 ((a), szerkezeti kivétel). Negatív kontroll: a régi kóddal 7 teszt bukik (az „index nélkül” és a H3499 a régi viselkedést rögzíti, ezek ott is zöldek).
- `teszt_bont.py`: 55 teszt, 4 piros, mind a #144-től független: `HuIlleszt.test_ellenoriz` és `test_osszefuzo_a_mai_adaton_valtozatlan` (N-F131f: a tábla 674 Strongja a mai 5 696-hoz képest elavult; a main-en is piros), `Determinizmus.test_ellenoriz` (`bont.py --ellenoriz`) és `test_javitas_ellenoriz` (`forras_javit.py --ellenoriz`), amelyek a `hu_illeszt.py`-t nem hívják, és a beolvasztott main fájljain futnak. A #144 új piros tesztet nem okoz.

## M2 — részleges frissítés és mérés (2026-11-01)

`python eszkozok/bdb_jelolt/hu_illeszt.py --strong H0001,H2199,H2803,H2930,H3198,H3427,H3782,H3885,H3920,H5027,H5157,H5647,H5782,H5975,H6381,H6912,H6999,H7043,H7126,H7650,H7665,H8085,H8334 --ts 2026-11-01`, majd ugyanez `--ellenoriz`: **azonos**. Az első fejlécsor a két részleges frissítést jelöli (a H4397, H8034, H9004 2026-10-29-i és ez); a `# forras` sor a 2026-10-18-i teljes generálásé marad.

proveniencia: `scope=adat/bdb_szakasz_hu.tsv (674 Strong, 9 664 sor; előtte sha1 8b80639c86fa, utána sha1 b724cba68102 / sha256 36c45a5a363b) | forras=eszkozok/bdb_jelolt/hu_illeszt.py --strong (23 Strong) @ kód 6ed44a36e766 + ad hoc mérés (scratchpad m2_meres.py, m2_bkor.py) | ts=2026-11-01`

Bemenetek az M2-kor: `adat/forditasok.tsv` sha256 `7c43b398dfa3` (a main szerinti), `adat/bdb_szakaszok.tsv` `66bd24b9abb6`, `adat/bdb_vers_jelentes.tsv` `487607da93b8` — mindhárom bájtra azonos a main-nel, a #144 nem írta.

| | előtte | utána |
|---|---|---|
| kategória (sor) | `illeszkedik` 6 395 · `jelolo_nelkul` 2 461 · `elakad` 606 · `horgonnyal` 202 | változatlan |
| A-sor (a jelentés 2. pontja) | 26 (26 Strong) | **22** (22 Strong) |
| A′-sor (A + a forrássor `szoveg`-e > 8 karakter) | 14 | **10** |
| B-kör (`illeszkedik`, jel, `szoveg_hu` < 12, nem A) | 80 sor / 71 Strong | 80 / 71 |

- **Változott sor:** 468 (a 23 Strong minden sora, a proveniencia `ts`-e miatt), ebből **tartalmilag 52** (23 Strong) — azonos az M0 4. pontjában átnézett 52 sorral. Kategória-átmenet: `illeszkedik → illeszkedik` 43, `jelolo_nelkul` (szöveg) 7, `illeszkedik → horgonnyal` 1 és `horgonnyal → illeszkedik` 1 (mindkettő H7043 15/16). Előtte helyes sor nem romlott (az M0 4. pontjának soronkénti átnézése szerint).
- **A 15 szócikk eredménye:** a 4 valódi hiba (H0001, H2199, H5027, H7043) A′-sora megszűnt. A 11 indokolt kivétel (H3381, H5060, H6499, H5826, H6299, H7378, H7650; (a): H3499, H4519, H6965, H7130) A-sor maradt, de forrássoruk legfeljebb 8 karakter, így A′ szerint nem hiba.
- **A megmaradó 10 A′-sor** mind szakaszonként újrafordított Strongé (H1129, H1980, H3423, H3603, H5324, H7122, H7200, H7725, H7896, H7971): a régi `teljes` soruk `elavult`, a szó-lap a szakaszsorokat használja; a #144 hatókörén kívül esnek (N-F131f / N-F131g).
- **B-kör szúrópróba** (minden 3. Strong + a 23 közé esők: 24 Strong, 28 sor): mind helyes — a rövid forrássor hűen fordítva („surely.” → „1 bizony.”, „of man:” → „1 emberről:”, „above” → „Pi`el fent”), a következő sor a saját jelölőjénél kezdődik.

**Lexikon:** a 23 Strong `bdb_szakasz_hu.tsv`-sorai változtak; a lexikonlapjuk és a BDB-nézet újragenerálást kér. A #144 nem generál: a #152-vel összehangolva történik (orkesztrátor, 2026-11-01).

## M3 — zárás ⛔

A felhasználó átnézi a változott sorok mintáját (az M0 4. pontja és a fenti M2-táblázat). Utána a brief `lezarva`.
