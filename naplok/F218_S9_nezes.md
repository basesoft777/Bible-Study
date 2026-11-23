# F218a — S9: a felhasználó nézési csomagja (a második, egyben utolsó kör)

*A brief 6. pontja és az F218.12 szerint egy megállásban: a két renderelt lap, az osztályonkénti eltérés-összesítés, az S2–S9 új sablonmondatai és nevei. A nézés a felhasználóé. Készült: 2026-11-22, a 17. session (`claude-opus-5-5`), az S9a–S9b után; **az S9c változásaival frissítve: 2026-11-23, a 19. session** (`claude-opus-5-5`; a számok, a HN-03 és az N235 sorai, a D. pont, a döntendő N196 és N237); **a szerkesztő három döntése (2026-11-23, DT-F218h) átvezetve, ugyanabban a sessionben.***

## 1. A két renderelt lap

**A szerkesztő szava (2026-11-23):** „hamart az istentisztelettel - átnézésre / jóváhagyás után teremt”. A két lap együtt megy átnézésre, mindkettő előtte–utána eltéréseivel (HAMART-001: 2. pont; ISTENTISZT-001: 2/b pont); a TEREMT-001 a jóváhagyás után, saját briefben.

Mindkét lap az új generátor kimenete, munka módban, `PARDES_DATUM=2026-11-13`, a repón kívül; a session végén a felhasználónak külön is elküldve:
- `HAMART-001_TUDOMANYOS.md` (3288 sor) és `HAMART-001_KIZARASOK.md` (431 sor);
- `ISTENTISZT-001_TUDOMANYOS.md` (1705 sor) és `ISTENTISZT-001_KIZARASOK.md` (307 sor).

**Állapot.** A HAMART-001 teljes lapja a mai jóváhagyott lappal szakaszonként egyezik, csak az alábbi engedélyezett eltérésekkel (engedély nélküli diff-sor 0, a bemenet-hash őrrel). Az ISTENTISZT-001 mércéje a 8.2: a független számlálók (a Döntési út összeadása, az igehelyek halmaza, a KH-darabszám, az ószövetségi versek, a szópár-lánc, az LXX-összesítés) egyeznek, kivétel nélkül (az LXX „egyező versek” száma a lapon és a független számlálással is 13: az 1Kir 18:24 részenként egyező, N196, DT-F218h (2) (b); a regresszió ismert eltérés-listája üres); GK-04 `lxx_egyezes` része, GK-24 (az S9c-től a kézi prózán a csupasz Strong-számra is, DT-F218f: a szótári címke tartós kivétel, 62 név szerinti ismert eltérés tételenkénti darabszám-plafonnal (60 az N-F218i-ig, 2 az F218.13-ig, N235)), GK-25, GK-SZOPAR zöld (a GK-04 `hely_egyseg` része a 218c-é, N234); festékpróba 0 szivárgás; a HN-esetek száma 0. A régi generátor HAMART-kimenete a 218a végén is bájtra azonos a referenciával.

## 2. Eltérés-összesítés osztályonként (HAMART-001)

Összesen **149 diff-sor**, 146 engedélysor (`naplok/F218_elteres_engedely.tsv`), mindegyik `tenyleges_db = elvart_db` (az S9c és a DT-F218h (1) után; az S9b végén 139 / 136).

| Osztály | Szakasz | Diff-sor | Mi változik és miért |
|---|---|---|---|
| Forráslista a valódi olvasásból (8.1 (b), GK-07) | a blokkfejlécek (1., 2., 3., 4., 5., 6., 7., 8., 12., Kolofon) és a rések jelölői | 12 | A generált blokk fejlécének forrás- és licenclistája (megjegyzés, nem látható) a szakasz valódi olvasásaiból jön, nem kódba írt listából. |
| A Kolofon forrástáblája (DT901, DT911, **DT912**) | Kolofon | **55** | A tábla a lap valódi olvasásait mutatja. **28 új / 16 elmaradó / 10 változó sor** (a változók egyike a beszúrás miatt két diff-sorként áll: 11). Valódi új forrás **13**: BDB-szótár forrásjavításai; BDB-szótár rokon nyelvi írásai; Elutasítási okok táblája; Funkciókapcsolók táblája; Grammatikai szavak listája; Károli-kereszthivatkozások javított táblája; LSJ-szótár; Lap teljesség-mérése; Motívumközi kapcsolatok táblája; SDBH és SDGNT elemzetlen bejegyzései; Strong-szótár; Tematikus helyek saját szavai; **Thayer-szótár forrásjavításai** (S9c, GK-N178). Elmaradó forrás **1**: MCGED görög szótár (Mounce). A többi ugyanannak a forrásnak a szakaszlista-átsorolása (15 sor új–elmaradó párként, 10 változóként). *Az S9a után 13 sor szakaszlistájában a „3. Kizárt és vizsgált helyek” is áll; a bontás változatlan.* |
| Kötelező forrásmegjelölés (DT911 (3)) | Kolofon | 1 | A Mounce megjelölése elmarad (nem olvasott forrás); az LSJ-é bekerül (olvasott forrás). Az UBS-megjelölés kettős szóköze az N-F218x (N222) javításával megszűnt. |
| A 12. szakasz forráslistája (DT901) | 12. Irodalom és idézés | 28 | 13 új (az S9c-ben +1: „Thayer-szótár forrásjavításai (közkincs)”), 2 elmaradó, 5 licenc szerint, 8 áthelyezett sor: a lista az olvasási naplóból, a jegyzék `irodalom` oszlopával szűrve. |
| A kritérium egyetlen helye (DT872, DT874) | a lap eleje, 1., 3., Kolofon | 14 | A kritérium a lap elején áll egyszer, máshol hivatkozás: az 1.1 pont (−4 +1 látható, −3 üres), a horgony a lap elején, a 3. szakasz „Negatív kritérium” bekezdése helyett utalás a szakasz elején (−1 +1, üres −1 +1), a Kolofon „Negatív kritérium” sora. |
| A funkció kézi magyarázata (M-CSERE) | 1. Döntési út | 15 | A régi generátor a kézi magyarázat kezdőbetűjét a listaelemben nagyra írta át; az új a kézi szöveget változatlanul adja. |
| A kiejtés utólagos beszúrása (8.1 (j), DT890) | 3., 6., 7. | 3 | A régi lap a kézi indoklásba a kiejtést még egyszer beszúrta („תהו (tóhú)/בהו (tóhú/bóhú)”, „מָלֵא (málé) + חָמָס, málé + chámász”); az új a forrás szövegét adja. |
| A proveniencia eredeti alakja (HN-10, GK-07) | 6., 7., 8. | 3 | A Minősítés, az Alátámasztás és a 8. szakasz proveniencia-sora (megjegyzés) a valódi olvasásokat nevezi (a Károli-KH javított táblájával). |
| A pe/mem betűjavítás a maqqéfos szón (DT-F218h (1)) | 4. Szótári háttér | 1 | A H0127 BDB-szócikkében (4Móz 16:30) a hibás „אֶת־מִּיהָ” helyett „אֶת־פִּיהָ”: a betűjavítás a rafe-maqqéf feloldása előtt fut, a javítótábla rafés kulcsa illeszkedik (S9C-PEMEM). |
| A hamis SECE-mondat (HN-15) | 4. Szótári háttér | 2 | „magyar rövid glossza-tábla a görögre még nincs” helyett a valós állapot (a görög rövid jelentés a fordítástáblában magyarul áll). |
| T9: a jóváhagyás-mondat munka módban (GK-27) | Kolofon | 1 | A szerzőségi mondat a szerző korábbi jóváhagyását mondja, dátummal. |
| A melléklet könyvnevei és forrássorai (GK-17, DT823) | KIZARASOK | 8 | A könyv az adat szerinti rövidítéssel és a Károli-rend helyén (4); a mérés forrássora megjegyzésben, a látható sor a keresés olvasói nevével (4). |
| **HN-03: a mondatközi, zárójeles forrásnév** (8.1 (f), DT925 (2) (a), DT-F218e (1)); S9c | 2., 4., 9. | 6 | A forrásnév a mondat végére vagy „forrás:” alakba kerül (4 új sablonmondat: 3.A 42–45). Minden hely előtte/utána: 3.D. |

## 2/b. Előtte–utána: ISTENTISZT-001

**Előtte:** a jóváhagyott lap, `lexikon/ISTENTISZT-001_TUDOMANYOS.md` — az 1. kiadás (2026.11.04), a régi generátorral, a régi forrásból; a motívum lapja be van fagyasztva, a 2. kiadás az új generátorral készül (DT835, `adat/lap_befagyasztas.tsv`). **Utána:** az új generátor lapja a mai forrásból és adatból (a forrás és az adat a 2. kiadásra kész, 2026-11-12/13). Az eltérés tehát három rétegből áll együtt: (1) az új szakaszrend és a generátor eltérései (ugyanazok az osztályok, mint a HAMART-001-nél: forráslista az olvasásból, a kritérium egyetlen helye, a Kolofon forrástáblája, HN-03, a belső jelölések nélküli sablonmondatok); (2) az adat változása az 1. kiadás óta; (3) a migrált, újraírt kézi forrás (`motivumok/ISTENTISZT-001.md`). A HAMART-nál alkalmazott soronkénti engedély-mérce (8.1) itt nem alkalmazható; a mérce a 8.2 (a független számlálók: mind egyezik, az N196 ismert eltéréssel). A teljes soronkénti diff (2302 sor, 414 KB) a nézéskor külön fájlként megy (a jegyzetmappa `F218_S9_ISTENTISZT_elotte_utana.diff` fájlja).

| Szakasz (régi → új) | Diff-sor (− / +) | A fő változás |
|---|---|---|
| (a lap eleje) | 0 / 8 | Új: „A motívum”, „Mi tartozik ide, és mi nem”, „A tágabb kör” (a kritérium egyetlen helye, DT872, a HAMART mintájára). |
| Kivonat | 2 / 6 | Új kézi Kivonat a HAMART mintájára (DT-F218w): a formula, a 20 hely bontása, a 2Móz 33:19 és 34:5 határesete, a tágabb kör. |
| Tartalomjegyzék, Jelmagyarázat | 31 / 30 | Az új szakaszrend (15 szakasz); „lap” → „szócikk”; a belső hivatkozások (`adat/SEMA.md`, `sablonok/…`, a proveniencia-sor magyarázata) helyett olvasói szöveg; új: a szótári pontok magyarázata. |
| — → 1. Döntési út | új szakasz | A keresés lépései és számai (a HAMART-on már jóváhagyott szakasz). |
| 1. Előfordulások → 2. | 105 / 74 | **22 → 20 hely** (16 ószövetségi, 6 → 4 újszövetségi; az adat 2026-11-12-i állapota); a soronkénti lábjegyzetek közös forrásmegjelölésbe; az igehelyek szövege alatt új kézi mondatok és funkciók; „1/a” → „2.1”. |
| 1/b. Kizárt és vizsgált helyek → 3. | 204 / 122 | 560 → 579 vizsgált vers, 109 → 115 elutasított/nyitott sor; a kizárás mércéje hivatkozás a lap elejére; az okok táblája olvasói címkékkel (N237: a rövid címke névelővel, döntve: DT-F218h (3) (a)). |
| 2. Szótári háttér → 4. | 407 / 416 | A számozott szótári pontok (4.1–4.14) rendje, a „Miért fontos ez a lelet” új kézi szövege; a belső fájl- és szerepmátrix-hivatkozások helyett olvasói forrásnevek. |
| 3. LXX-fordítói döntések → 5. | 22 / 24 | Az összesítés a mai adatból; az 1Kir 18:24 ítélete részenként „egyező” (N196, döntve: DT-F218h (2) (b)); az összesítés 13 egyező / 2 szócsalád, a kiadott lap szerint. |
| 4. Kereszthivatkozások → 6. | 151 / 86 | 22 → 20 hely, 9 → 8 utaló hely, 20 → 19 utalás; „Votes” → „szavazat”; a javított Károli-KH tábla; a Minősítés a mai adatból. |
| 5. Kapcsolatok → 7. | 32 / 27 | 18 → 16 kapcsolat (15 → 13 párhuzam; 14 magas, 3 közepes); az indoklások a mai `kapcsolatok.tsv`-ből. |
| 5/b. → 8. Kapcsolódó motívumok | 5 / 5 | Forráslista és szöveg. |
| — → 9. Hatástörténet | új szakasz | Ókori fordítások (ÓSZ, ÚSZ) és ókori értelmezők (a HAMART-on már jóváhagyott szakasz; GK-SZOPAR: a szópáros lánc). |
| 6. Értelmezés → 10. | 198 / 13 | A régi hosszú értelmezés (PaRDeS-keret, „Új felismerés — a D-minta görög folytatása”) helyett a migrált kézi forrás rövid Értelmezése és „Vitatott pontok” része; a régi szöveg az archívumban (`archivum/ISTENTISZT-001/`). |
| 6/b. Alkalmazás és tanítói egyezés | csak a régin | Kivezetve (az `alkalmazas` rés: DT756; a `tanitoi`: DT643). |
| 7. Módszertan és nyitott kérdések → 11. | 65 / 10 | A régi A/B/C/D tipológia helyett a migrált forrás rövid Módszertana és „Nyitott kérdések” része. |
| 8. Irodalom és idézés → 12. | 52 / 60 | A forráslista az olvasásból (DT901); a hivatkozási adatok a `kiadasi_adat` névtáblából; HN-03 (3 jegyzéksor nem változik). |
| Kolofon | 72 / 75 | A forrástábla a valódi olvasásból (DT912); a szerzőségi mondat a 6/b nélkül; a „Hogyan idézd” a kiadási adatokkal kitöltve (a helyőrzők helyett). |

**Az ISTENTISZT-001-en döntve (2026-11-23):** az N196 és az N237 (4. pont, DT-F218h). A 3. pont sablonmondatai és nevei a két lapra közösek.

## 3. Az S2–S9 új sablonmondatai és nevei

A betűre egyező mai szöveg (`eredet=<a régi generátor szimbóluma>`) nem kér jóváhagyást (brief 6. pont); az S1 után jóváhagyott 8 sablonsor nincs itt. A „vár” jelű sorok a nézésre várnak.

### A. Új sablonmondatok (`eredet=uj`), S2–S9c: 45 sor

| # | Kulcs | Szakasz | Mondat (helyőrzőkkel) | Miért új | Döntés |
|---|---|---|---|---|---|
| 1 | `kz.forrassorok.bevezeto` | melleklet | A Döntési út {szakasz}.{alpont} pontjának versszámai ebből a mérésből jönnek. Keresésenként a megvizsgált versek száma: | — | vár |
| 2 | `kz.forrassorok.kereses` | melleklet | - **{kereses}** ({n} vers) | — | vár |
| 3 | `e2.jel.szocikkel` | 2 | {jel} ({szocikk}) | — | vár |
| 4 | `e2.jel.szocikk_sorszam` | 2 | {szotar\|a} {n}. szócikke | — | vár |
| 5 | `d11.targy` | 1 | A keresés tárgyát a lap eleje határozza meg ([{cim}](#{horgony})). A keresés {elemek\|, \| és } terjedt ki: a szavakat {szakasz\|a}.{forrasok}., a kizárás okait {szakasz\|a}.{kiesett}., a megmaradt helyeket {szakasz\|a}.{maradt}. pont sorolja fel. | DT872: a kritérium ismétlése helyett hivatkozás és számolás | vár |
| 6 | `d11.targy.szavak_nelkul` | 1 | A keresés tárgyát a lap eleje határozza meg ([{cim}](#{horgony})). A kizárás okait {szakasz\|a}.{kiesett}., a megmaradt helyeket {szakasz\|a}.{maradt}. pont sorolja fel. | DT872 | vár |
| 7 | `d11.elem.heber` | 1 | {n} héber szóra | DT872 | vár |
| 8 | `d11.elem.gorog` | 1 | {n} görög szóra | DT872 | vár |
| 9 | `d11.elem.szopar` | 1 | {n} szópárra | DT872 | vár |
| 10 | `d14.hely.magyarazat_nelkul` | 1 | <li><a href="#{horgony}">{hely}</a></li> | — | vár |
| 11 | `s4.felulvizsgalat` | 4 | {szoveg} *(a fordítás felülvizsgálat alatt)* | — | vár |
| 12 | `s4.nyelv.gorog.ures.megjegyzes` | 4 | *A motívumnak nincs görög szava; a görög szavak pontjai itt nem állnak.* | — | vár |
| 13 | `s4.nyelv.heber.ures.megjegyzes` | 4 | *A motívumnak nincs héber szava; a héber szavak pontjai itt nem állnak.* | — | vár |
| 14 | `s4.p3.cim.var` | 4.3 | *{cim}* *(fordításra vár)* | — | vár |
| 15 | `s4.p3.cim.felulvizsgalat` | 4.3 | *{cim}* *(a fordítás felülvizsgálat alatt)* | — | vár |
| 16 | `s4.p4.elemzetlen` | 4.4 | *Figyelem: a szótárban a szóhoz {n} elemzetlen bejegyzés is tartozik.* | — | vár |
| 17 | `s4.p7.labjegyzet` | 4.7 | *A szólista és a sorrend a SECE-é (gyakoriságot nem ad; az ismétlődő szóalak egyszer áll); a Strong-szám a TBESG/TBESH lemmájából vagy a SECE címszavából párosul; a rövid jelentés: héberül {heber}, görögül {gorog}.* | — | vár |
| 18 | `s4.p8.gorog.rokon` | 4.8 | *A klasszikus görög nagyszótár (LSJ) a motívum szavaihoz nem ad adatot; rokon szavaik közül ezekhez ad szócikket: {rokon\|, }.* | — | vár |
| 19 | `s4.p8.gorog.csonk` | 4.8 | {szo} LSJ-szócikke csak az alapigére utal: {alap}. | — | vár |
| 20 | `s4.p8.gorog.csonk.rokon` | 4.8 | Az alapige LSJ-szócikke a rokon szavaknál áll. | — | vár |
| 21 | `s4.p8.gorog.csonk.nincs` | 4.8 | Az alapige LSJ-szócikke a lexikon adatai között nem áll. | — | vár |
| 22 | `s4.p8.gorog.csonkok` | 4.8 | *{csonkok\| } {zaro}* | — | vár |
| 23 | `s4.p8.heber.nincs_fej` | 4.8 | **{szo}** · a BDB-szócikk feje magyarul nem áll rendelkezésre; a szócikk a {szakasz}.{pont} pontban áll. | — | vár |
| 24 | `s4.p2.jel.felulvizsgalat` | 4.2 |  *(a fordítás felülvizsgálat alatt)* | T5, GK-15: az elavult Thayer-fordítás az idézet végén; az 5. ellenőrzés E3 tétele | vár |
| 25 | `s6.ures` | 6 | A két gyűjtemény a motívum egyik helyéről sem ad utalást. | a régi „Nincs TSK/Károli-KH találat ehhez a motívumhoz.” helyett; a két mintalapon nem fut | vár |
| 26 | `s6.min.parok.nincs` | 6 Minősítés | **Külső megerősítés:** nincs olyan TSK-utalás (legalább {kuszob} szavazattal) vagy Károli-utalás, amely a motívum két saját helyét kötné össze. | a régi „**Független megerősítés:** nincs olyan TSK- (Votes ≥ 15) vagy Károli-KH-találat …” helyett; a két mintalapon nem fut | vár |
| 27 | `s9.nincs_targum` | 9 | nincs Targum-forrás (a szabad Targum-szöveg ezt a könyvet nem tartalmazza) | — | vár |
| 28 | `s9.usz.bevezeto.szopar` | 9 | A motívum lexikai újszövetségi helyein a formula görög szavai állnak. A táblázat szócsaládonként azt mutatja, hogy a latin Vulgata ugyanazzal a latin szóval adja-e vissza őket, van-e a formula szavát érintő szövegváltozat, és a formula mely ószövetségi Septuaginta-verseiben áll ugyanez a görög szócsalád. {n\|A} görög szócsaládból {e} esetében a Vulgata a két szövetségben ugyanazt a latin szócsaládot használja. | — | vár |
| 29 | `s9.usz.fejlec.lxx.szopar` | 9 | Ugyanez a szó a formula Septuagintájában | — | vár |
| 30 | `s9.usz.lxx.nincs.szopar` | 9 | nincs a formula ószövetségi verseiben | — | vár |
| 31 | `s9.usz.mit.egyezo.szopar` | 9 | A Vulgata az újszövetségi helyeken és a formula {db} ószövetségi versében is ugyanazt a latin szócsaládot használja ({csal}): a latin olvasó a két szövetség helyeit egy szóval olvassa. | — | vár |
| 32 | `s9.usz.mit.reszben.szopar` | 9 | A Vulgata az újszövetségi helyeken {n}/{nn} versben {csal\|a} szócsaládot használja; a formula azon {db} ószövetségi versében, ahol a görög fordításban ugyanez a görög szócsalád áll, {on} versben: a latin szóválasztás a két szövetség között csak részben egyezik. | — | vár |
| 33 | `s9.usz.lab.szopar` | 9 | *A Vulgata oszlopa a versben álló latin szó és az, hány versben áll a fő latin szócsalád (n/N); a latin megfelelő a Vulgata szövegéből, a forrásszövegen ellenőrizve. Szövegváltozat: az SBL Greek New Testament apparátusa (CC BY 4.0) és a STEPBible TAGNT változatjegyzéke (CC BY 4.0), csak ahol a formula szavát érinti. A formula Septuagintája: ugyanaz a görög szócsalád a formula ellenőrzött ószövetségi Septuaginta-soraiban (az ószövetségi táblázat LXX-oszlopa); ez szóegyezés, nem tipológiai állítás. Vulgata: Clementina (közkincs). {peshitta}* | — | vár |
| 34 | `s9.usz.valt.nincs.szopar` | 9 | nincs a formula szavát érintő változat | — | vár |
| 35 | `kolofon.szerzoseg.kezi` | Kolofon | Az értelmező szakaszok ({resek\|, }) készítőjét a kiadás nem rögzíti modellnévvel | kolofon_szerzoseg: a belső „manual” szó nélkül | vár |
| 36 | `kolofon.jovahagyas.korabbi` | Kolofon | a szerző a lap korábbi változatát hagyta jóvá ({datum}) | T9: a felhasználó döntése, 2026-11-13, „Kiadott lap csak friss jóváhagyással” | a felhasználó, 2026-11-13 (T9) |
| 37 | `kolofon.hogyan.kiadatlan.datum_nelkul` | Kolofon | **Hogyan idézd.** {szerzo}: *{lexikon}*, „{cim}” ({motivum}), kiadás előtti változat, még nem idézhető, {url}/{motivum}. A lap adatai (előfordulások, kizárt helyek) nyílt adatkészletként is elérhetők: https://doi.org/{doi}. | kolofon_kozlemenyek: megadott generálási dátum nélkül a dátum kimarad | vár |
| 38 | `kolofon.ertek.kriterium` | Kolofon | a lap elején áll ([{cim}](#{horgony})) | DT874, 9. tétel: a kritérium egyetlen teljes helye a lap eleje | DT874 (az orkesztrátor, a felhasználó felhatalmazásával, 2026-11-13) |
| 39 | `k3.kriterium` | 3 | *A kizárás mércéje a lap elején álló meghatározás ([{cim}](#{horgony})).* | DT872: a „Negatív kritérium” bekezdés helyett utalás a szakasz elején | vár |
| 40 | `k3.miert.szopar` | 3 | szópár keresése: {szavak\| + } | a régi „gépi szópár-keresés” a Strong-számmal; a szó a Strong-szám helyett | vár |
| 41 | `k3.miert.tematikus` | 3 | Tematikus tanulmány felvetése | a régi „a tematikus tanulmány felvetése (C-minta)”: a minta belső jelölése nem kerül a lapra | vár |
| 42 | `e2.hatokor` | 2 | *… A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja, a „Funkció (a motívumban)” a hely motívumbeli funkcióját (szerkesztői döntés, {datum}). A jelentés forrása: {cimketabla}, {bdb} és {thayer}; a címke forrása a sor lábjegyzetében.* | HN-03 (S9c): a régi „…a szótár tagolásában adja ({cimketabla}, {bdb}, {thayer}; a címke forrása a sor lábjegyzetében), a „Funkció…”” helyett a forrás a mondat után | vár |
| 43 | `s4.p2.app.tartomany` | 4.2 | {vers}: a BDB a helyet nem önállóan idézi, hanem {jel\|a} szakaszban {kezdo\|a}–{veg} verstartomány belsejében (a BDB-ben: „{nyers}{folytatas}”); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely nem BDB-példa | HN-03 (S9c): a zárójelből kimarad a „; a BDB-szótár” (a mondat a BDB-t már megnevezi) | vár |
| 44 | `s4.p8.heber.alap.rovid` | 4.8 | alapjelentés: {jelentes} · forrás: a STEPBible rövid szótára | HN-03 (S9c): a régi „*(a STEPBible rövid szótára szerint)*” helyett „forrás:” alak | vár |
| 45 | `s9.osz.rokon` | 9 | A lánc szavainak rokon nyelvi hátterét a héber szavak {sz}.{p} pontja adja, a BDB-szótár szerint. | HN-03 (S9c): a régi „…hátterét (a BDB-szótár szerint) a héber szavak…” helyett a mondat végén | vár |

### B. Új olvasói nevek (névtábla, `eredet=uj`): 9 sor, és egy új típus

| # | Típus | Kulcs | Olvasói név |
|---|---|---|---|
| 1 | motivumkozi_tipus | `közös_igehely` | közös igehely |
| 2 | irod_adat | `adat/tematikus_sajat_szo.tsv` | Tematikus helyek saját szavai |
| 3 | irod_adat | `adat/bdb_forras_javitas.tsv` | BDB-szótár forrásjavításai |
| 4 | irod_adat | `adat/elutasitasi_okok.tsv` | Elutasítási okok táblája |
| 5 | irod_adat | `konkordancia/SDBH_SDGNT_anomaliak.tsv` | SDBH és SDGNT elemzetlen bejegyzései |
| 6 | irod_adat | `konkordancia/Strong_szotar.tsv` | Strong-szótár |
| 7 | irod_adat | `adat/funkcio_kapcsolok.tsv` | Funkciókapcsolók táblája |
| 8 | irod_adat | `konkordancia/Karoli_KH_javitott.tsv` | Károli-kereszthivatkozások javított táblája |
| 9 | irod_adat | `adat/thayer_forras_javitas.tsv` | Thayer-szótár forrásjavításai (S9c, GK-N178: a 12. szakaszban és a Kolofonban új forrássor) |

**Új típus: `kereses_megszoritas` (S9c, DT926).** A szókeresés-jegyzet megszorítása a bemeneti rétegben kulcs, a látható név ebből a típusból jön; ma 1 sor: `Hif'íl-alakok` → „Hif'íl-alakok” (`eredet`: a B04 keresési forrása, DT926). A lap betűre nem változott; ismeretlen megszorításnál a generálás megáll.

### C. Új névtábla-típus: `ok_leiras_cella` (S9a; DT925 szerint a nézésen)

Az elutasítási ok megjegyzésének táblacella eleji alakja a 3. szakasz okainak táblájában („Mit jelent” oszlop): a névelővel kezdődő megjegyzés nagy kezdőbetűvel (a régi lap szabálya szerint, betűre); a melléklet és a Döntési út a megjegyzést változatlanul közli. 18 sor, a megjegyzéstől csak a kezdőbetűben térhet el (a betöltő ellenőrzi). A sorok: `adat/olvasoi_nevtabla.tsv`, `ok_leiras_cella` típus.

### D. HN-03: a forrásnév a mondat közepén, zárójelben (S9c; DT925 (2) (a), DT-F218e (1))

*Külön tétel, egyenként visszautasítható; a végső szó a szerkesztőé. Az új lapokon 16 hely (HAMART-001 9, ISTENTISZT-001 7). **10 változik** (HAMART-001 6, ISTENTISZT-001 4: a 4 új sablonmondat, 3.A 42–45). **6 nem változik:** a 12. szakasz forrásjegyzékének sor végi „(forrásnév, licenc)” megjegyzése nem mondatközi forrásnév, hanem a jegyzéksor licencrésze; a minta csak a „szótár” szó miatt fogta meg (DT-F218e (1)). Az „előtte” alak a HN-03 előtti négy sablonmondattal generált lap, az „utána” a mostani; mindkettő `PARDES_DATUM=2026-11-13`.*

1. **HAMART-001, 2. Előfordulások** (mondatközi)
   - előtte: … a Károli-szöveggel (2.1) és az UBS-jelentéssel. A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja (a szótári szakaszok címketáblája, a BDB-szótár, a Thayer-szótár; a címke forrása a sor lábjegyzetében), a „Funkció (a motívumban)” a hely motívumbeli funkcióját (szerkesztői döntés, …
   - utána: *A táblázat a motívum 49 igehelyét sorolja fel (forrás: a motívum előfordulás-táblája), kanonikus sorrendben, a Károli-szöveggel (2.1) és az UBS-jelentéssel. A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja, a „Funkció (a motívumban)” a hely motívumbeli funkcióját (szerkesztői döntés, 2026-10-19). A jelenté…
2. **HAMART-001, 4. Szótári háttér** (mondatközi)
   - előtte: *ⓘ Megjegyzés: Sof 1:3: a BDB a helyet nem önállóan idézi, hanem a 4. szakaszban a Sof 1:2–3 verstartomány belsejében (a BDB-ben: „Zeph 1:2-3”; a BDB-szótár); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely …
   - utána: …an a Sof 1:2–3 verstartomány belsejében (a BDB-ben: „Zeph 1:2-3”); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely nem BDB-példa.*
3. **HAMART-001, 4. Szótári háttér** (mondatközi)
   - előtte: **אָבַל (ával)** · alapjelentés: gyászolni *(a STEPBible rövid szótára szerint)*
   - utána: **אָבַל (ával)** · alapjelentés: gyászolni · forrás: a STEPBible rövid szótára
4. **HAMART-001, 4. Szótári háttér** (mondatközi)
   - előtte: **אָלָה (álá)** · alapjelentés: eskü *(a STEPBible rövid szótára szerint)*
   - utána: **אָלָה (álá)** · alapjelentés: eskü · forrás: a STEPBible rövid szótára
5. **HAMART-001, 4. Szótári háttér** (mondatközi)
   - előtte: **חַטָּאת (chattát)** · alapjelentés: bűn *(a STEPBible rövid szótára szerint)*
   - utána: **חַטָּאת (chattát)** · alapjelentés: bűn · forrás: a STEPBible rövid szótára
6. **HAMART-001, 9. Hatástörténet: ókori fordítások és értelmezők** (mondatközi)
   - előtte: A lánc szavainak rokon nyelvi hátterét (a BDB-szótár szerint) a héber szavak 4.8 pontja adja.
   - utána: A lánc szavainak rokon nyelvi hátterét a héber szavak 4.8 pontja adja, a BDB-szótár szerint.
7. **HAMART-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (a BDB-szótár, közkincs)
   - utána: nem változik
8. **HAMART-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) (az LSJ-szótár, CC BY-SA 4.0)
   - utána: nem változik
9. **HAMART-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - SDBH (Semantic Dictionary of Biblical Hebrew) (az SDBH szemantikai szótár, CC BY-SA 4.0)
   - utána: nem változik
10. **ISTENTISZT-001, 2. Előfordulások** (mondatközi)
   - előtte: … a Károli-szöveggel (2.1) és az UBS-jelentéssel. A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja (a szótári szakaszok címketáblája, a BDB-szótár, a Thayer-szótár; a címke forrása a sor lábjegyzetében), a „Funkció (a motívumban)” a hely motívumbeli funkcióját (szerkesztői döntés, …
   - utána: *A táblázat a motívum 20 igehelyét sorolja fel (forrás: a motívum előfordulás-táblája), kanonikus sorrendben, a Károli-szöveggel (2.1) és az UBS-jelentéssel. A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja, a „Funkció (a motívumban)” a hely motívumbeli funkcióját (szerkesztői döntés, 2026-10-19). A jelenté…
11. **ISTENTISZT-001, 4. Szótári háttér** (mondatközi)
   - előtte: …és: 1Kir 18:25: a BDB a helyet nem önállóan idézi, hanem a Qal 2.c szakaszban az 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”; a BDB-szótár); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely …
   - utána: … 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely nem BDB-példa.*
12. **ISTENTISZT-001, 4. Szótári háttér** (mondatközi)
   - előtte: …jegyzés: 1Kir 18:25: a BDB a helyet nem önállóan idézi, hanem a 4. szakaszban az 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”; a BDB-szótár); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely …
   - utána: … 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”); a tartomány nincs kibontva (szerkesztői döntés, 2026-10-28 (A)), ezért a hely nem BDB-példa.*
13. **ISTENTISZT-001, 9. Hatástörténet: ókori fordítások és értelmezők** (mondatközi)
   - előtte: A lánc szavainak rokon nyelvi hátterét (a BDB-szótár szerint) a héber szavak 4.8 pontja adja.
   - utána: A lánc szavainak rokon nyelvi hátterét a héber szavak 4.8 pontja adja, a BDB-szótár szerint.
14. **ISTENTISZT-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (a BDB-szótár, közkincs)
   - utána: nem változik
15. **ISTENTISZT-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) (az LSJ-szótár, CC BY-SA 4.0)
   - utána: nem változik
16. **ISTENTISZT-001, 12. Irodalom és idézés** (sor végi)
   - előtte: - SDBH (Semantic Dictionary of Biblical Hebrew) (az SDBH szemantikai szótár, CC BY-SA 4.0)
   - utána: nem változik

**Adat helyére költözött, szövegében nem új (tájékoztatás):** a névtábla `kiadasi_adat` 5 sora (S8d, DT911: szerző, a lexikon címe — ma „Logosz-lexikon”, a webcím alapja, két DOI; a névcsere az N220); az `ok_cella` 45 és az új `ok_leiras_cella` típus 18 sora (S5, S9a: az elutasítási ok címkéjének és megjegyzésének táblacella eleji alakja, a régi lap nagybetűsítése szerint, betűre).

## 4. A 218a végi lista egyéb tételei (megfigyelések és döntések, röviden)

A részletek a `naplok/F218_folytatas.md` és a `naplok/F218_jelentes.md` megnevezett szakaszaiban.
- **DT872, DT895 kézi szöveg (S2, S8a):** a Kivonat két átvezetése és törölt mondatai, a kritérium tagolása és a kettős szólista, a „Károli alapszövege” a lap elejére, a kizárási lista eltérése.
- **S3:** a H7451 glosszájának látható kihagyásjele („…” vagy „[…]”); a 4.12 bevezetője zárójelben megismétli a tágabb kört; a több lemmás 4.11-sor kétféle kezelése (saját-pár szűrő ⟂ egyforrás-kapu: az 1Kir 18:24 egyező görög szava kiesik); a 4.13–4.14 szótári alakjai kisbetűsítve, idézetként („úr”, „baál”, „ábrám”).
- **S5:** DT884 (az indoklás végleges alakja az adatban); a Minősítés „a {p}%-a” rögzített névelője (1%-nál és 5%-nál „a 5%-a” lenne).
- **S6:** DT888; a `funkcio` adatjavítás (43 + 1 cella); az ISTENTISZT-001 kisbetűs funkció-cellái; az üres funkció- és PaRDeS-cella „—” jele; az ISTENTISZT-001 Alátámasztásának Strong-száma és Markdown-kiemelése.
- **S7:** N214 (a szópáros bevezető ISTENTISZT-specifikus mondata); a tanú korának és a rabbinikus hivatkozásnak a szerkezeti bontása; a szópáros ÚSZ-mondat nevezője (12 a 14 felsorolt vers helyett) és a `kor` mező belső évszáma.
- **S8b:** GK-19 (T6): a Károli-párosítás pontosság-mondata a JOHD-validáció után (N219; döntéssel elhalasztva).
- **N235 — a „blokk-kizárás” munkaszó (HAMART-001, 3. szakasz; döntés: DT-F218e (2) (b)).** Az 1Krón 7:22 és az 1Kir 8:31 csoportsorának indoklása a látható szövegben „a többi előfordulása ezért blokk-kizárás (a H7451 és a H7043 blokkjának mintájára).”: belső munkaszó és két csupasz Strong-szám. A jóváhagyott lapon is így áll; **a jóváhagyás után, az F218.13-ban javul** az új generátoros kiadással együtt, erre az alakra: „a többi előfordulása ezért csoportos kizárás (a רַע (ra) és a קָלַל (kálal) csoportjának mintájára).” Addig a két szám a GK-24 ismert eltérései között áll.
- **S9c (DT-F218f, tájékoztatás):** a GK-24 a kézi prózán a zárójel nélküli Strong-számot is tiltja. A két jóváhagyott lapon 96 ilyen hely állt (a lap ettől nem változik): a „Miért fontos” címsorainak szótári címkéje („H0779 — אָרַר (árar) · BDB”) tartós kivétel; a többi kézi adatban áll (a HAMART TSK-kizárásaiban „de nem a H6093 iccávón-t”, a Károli-csoport 57 blokk-sorában „a G0331 szót fordítja”, az ISTENTISZT egy kapcsolat-indoklásában „azonos H7121+H8034 pár”), és név szerinti, csak fogyó kivétellistán áll a javításig (N-F218i, a 218c adatköre); a két N235-hely is itt áll az F218.13-ig.

**A nézésen döntött tételek (S9c).** A szerkesztő 2026-11-23-án: „mehet a három javaslat” (DT-F218h). Ez a három tételről döntés; a két lap egésze, a 45 új sablonmondat (3.A), a 9 új név (3.B) és a HN-03 helyek (3.D) a szerkesztő külön nézésére várnak.
- **A pe/mem betűjavítás a maqqéfos szón (a #810 lelete, 2026-11-23).** A HAMART-001 4. szakaszában, a H0127 (אֲדָמָה, adámá) BDB-szócikkében egy helyen a hibás „אֶת־מִּיהָ” áll a helyes „אֶת־פִּיהָ” helyett (a 4Móz 16:30 idézetében: „megnyitja a föld a száját”). Ok: a javítótábla (`adat/bdb_forras_javitas.tsv`) a forrás rafés alakjára kulcsol (`אֶתמִּֿיהָ` → `אֶתפִּֿיהָ`), a generátor viszont előbb feloldja a rafe-maqqéfot, és csak utána javít betűt, így a kulcs nem illeszkedik. A jóváhagyott lapon is így áll (a régi generátor ugyanígy hív: `eszkozok/lexikon_general.py` 4657. sor, `bdb_rovidites.heber_sorrend_javit`); az olvasóban a #810 javította. **A javítás helye az új generátorban:** `eszkozok/lapgen/bemenet/kartya.py` `forrasjavitas` (317–318. sor: a `betu_javit` a `maqqef_javit` elé), a HAMART-diffben egy új engedélysorral. A 256 rafés kulcsú betűjavításból a két lapon csak ez az egy hely érintett; az ISTENTISZT-001-en 0. **Döntve: (a)**, javítva a 218a-ban (DT-F218h (1)): a `betu_javit` a `maqqef_javit` előtt fut; a lapon „אֶת־פִּיהָ” áll, a HAMART-diffben egy új engedélysorral (S9C-PEMEM). A kiadott lap és a régi generátor kimenete nem változik.
- **N196 — az 1Kir 18:24 LXX-ítélete (ISTENTISZT-001).** A vers Septuaginta-szövegében a motívum saját görög szava áll (ἐπικαλέσομαι, epikaleszomai); a kiadott lap „egyező”-t ír, az új generátor „ugyanaz a szócsalád”-ot. Az ok: a több lemmás sort („βοάω · ἐπικαλέω”) a saját-pár szűrés egészben hasonlítja, a forrás-kapu részenként. **Döntve: (b)** részenként (DT-F218h (2)): az új lap is „egyező”-t ír (ἐπικαλέσομαι, epikaleszomai), az összesítés 13 egyező / 2 szócsalád, a kiadott lap szerint; a 4.6 két szavankénti mondata és a szóhíd mondata ugyanígy 13 / 2. Az egyforrás-kapu (F182) az egyező sorban a több lemmás társítás egy részét kéri. Az N238 számlálójának ismert eltérése megszűnt.
- **N237 — a rövid okcímke névelője (ISTENTISZT-001, 3. szakasz).** Az okok táblájában a rövid, névelővel kezdődő címke névelővel áll („A hívás igéje a név nélkül”); a régi lap szabálya a rövid táblaelemről a névelőt elhagyta volna („Hívás igéje a név nélkül”). **Döntve: (a)** névelővel, ahogy most (DT-F218h (3)); a kód nem változik.
