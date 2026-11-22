# F218a — S9: a felhasználó nézési csomagja (a második, egyben utolsó kör)

*A brief 6. pontja és az F218.12 szerint egy megállásban: a két renderelt lap, az osztályonkénti eltérés-összesítés, az S2–S9 új sablonmondatai és nevei. A nézés a felhasználóé. Készült: 2026-11-22, a 17. session (`claude-opus-5-5`), az S9a–S9b után.*

## 1. A két renderelt lap

Mindkét lap az új generátor kimenete, munka módban, `PARDES_DATUM=2026-11-13`, a repón kívül; a session végén a felhasználónak külön is elküldve:
- `HAMART-001_TUDOMANYOS.md` (3286 sor) és `HAMART-001_KIZARASOK.md` (431 sor);
- `ISTENTISZT-001_TUDOMANYOS.md` (1703 sor) és `ISTENTISZT-001_KIZARASOK.md` (307 sor).

**Állapot.** A HAMART-001 teljes lapja a mai jóváhagyott lappal szakaszonként egyezik, csak az alábbi engedélyezett eltérésekkel (engedély nélküli diff-sor 0, a bemenet-hash őrrel). Az ISTENTISZT-001 mércéje a 8.2: a független számlálók (a Döntési út összeadása, az igehelyek halmaza, a KH-darabszám, az ószövetségi versek, a szópár-lánc) mind egyeznek; GK-04, GK-24, GK-25, GK-SZOPAR zöld; festékpróba 0 szivárgás; a HN-esetek száma 0. A régi generátor HAMART-kimenete a 218a végén is bájtra azonos a referenciával.

## 2. Eltérés-összesítés osztályonként (HAMART-001)

Összesen **140 diff-sor**, 137 engedélysor (`naplok/F218_elteres_engedely.tsv`), mindegyik `tenyleges_db = elvart_db`.

| Osztály | Szakasz | Diff-sor | Mi változik és miért |
|---|---|---|---|
| Forráslista a valódi olvasásból (8.1 (b), GK-07) | a blokkfejlécek (1., 2., 3., 4., 5., 6., 7., 8., 12., Kolofon) és a rések jelölői | 12 | A generált blokk fejlécének forrás- és licenclistája (megjegyzés, nem látható) a szakasz valódi olvasásaiból jön, nem kódba írt listából. |
| A Kolofon forrástáblája (DT901, DT911, **DT912**) | Kolofon | **53** | A tábla a lap valódi olvasásait mutatja. **27 új / 16 elmaradó / 10 változó sor.** Valódi új forrás **12**: BDB-szótár forrásjavításai; BDB-szótár rokon nyelvi írásai; Elutasítási okok táblája; Funkciókapcsolók táblája; Grammatikai szavak listája; Károli-kereszthivatkozások javított táblája; LSJ-szótár; Lap teljesség-mérése; Motívumközi kapcsolatok táblája; SDBH és SDGNT elemzetlen bejegyzései; Strong-szótár; Tematikus helyek saját szavai. Elmaradó forrás **1**: MCGED görög szótár (Mounce). A többi ugyanannak a forrásnak a szakaszlista-átsorolása (15 sor új–elmaradó párként, 10 változóként). *Az S9a után 13 sor szakaszlistájában a „3. Kizárt és vizsgált helyek” is áll; a bontás változatlan.* |
| Kötelező forrásmegjelölés (DT911 (3)) | Kolofon | 2 | A Mounce megjelölése elmarad (nem olvasott forrás), az LSJ-é bekerül (olvasott forrás). |
| A 12. szakasz forráslistája (DT901) | 12. Irodalom és idézés | 27 | 12 új, 2 elmaradó, 5 licenc szerint, 8 áthelyezett sor: a lista az olvasási naplóból, a jegyzék `irodalom` oszlopával szűrve. |
| A kritérium egyetlen helye (DT872, DT874) | a lap eleje, 1., 3., Kolofon | 14 | A kritérium a lap elején áll egyszer, máshol hivatkozás: az 1.1 pont (−4 +1 látható, −3 üres), a horgony a lap elején, a 3. szakasz „Negatív kritérium” bekezdése helyett utalás a szakasz elején (−1 +1, üres −1 +1), a Kolofon „Negatív kritérium” sora. |
| A funkció kézi magyarázata (M-CSERE) | 1. Döntési út | 15 | A régi generátor a kézi magyarázat kezdőbetűjét a listaelemben nagyra írta át; az új a kézi szöveget változatlanul adja. |
| A kiejtés utólagos beszúrása (8.1 (j), DT890) | 3., 6., 7. | 3 | A régi lap a kézi indoklásba a kiejtést még egyszer beszúrta („תהו (tóhú)/בהו (tóhú/bóhú)”, „מָלֵא (málé) + חָמָס, málé + chámász”); az új a forrás szövegét adja. |
| A proveniencia eredeti alakja (HN-10, GK-07) | 6., 7., 8. | 3 | A Minősítés, az Alátámasztás és a 8. szakasz proveniencia-sora (megjegyzés) a valódi olvasásokat nevezi (a Károli-KH javított táblájával). |
| A hamis SECE-mondat (HN-15) | 4. Szótári háttér | 2 | „magyar rövid glossza-tábla a görögre még nincs” helyett a valós állapot (a görög rövid jelentés a fordítástáblában magyarul áll). |
| T9: a jóváhagyás-mondat munka módban (GK-27) | Kolofon | 1 | A szerzőségi mondat a szerző korábbi jóváhagyását mondja, dátummal. |
| A melléklet könyvnevei és forrássorai (GK-17, DT823) | KIZARASOK | 8 | A könyv az adat szerinti rövidítéssel és a Károli-rend helyén (4); a mérés forrássora megjegyzésben, a látható sor a keresés olvasói nevével (4). |

## 3. Az S2–S9 új sablonmondatai és nevei

A betűre egyező mai szöveg (`eredet=<a régi generátor szimbóluma>`) nem kér jóváhagyást (brief 6. pont); az S1 után jóváhagyott 8 sablonsor nincs itt. A „vár” jelű sorok a nézésre várnak.

### A. Új sablonmondatok (`eredet=uj`), S2–S9: 41 sor

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

### B. Új olvasói nevek (névtábla, `eredet=uj`): 8 sor

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

**Adat helyére költözött, szövegében nem új (tájékoztatás):** a névtábla `kiadasi_adat` 5 sora (S8d, DT911: szerző, a lexikon címe — ma „Logosz-lexikon”, a webcím alapja, két DOI; a névcsere az N220); az `ok_cella` 45 és az új `ok_leiras_cella` típus 18 sora (S5, S9a: az elutasítási ok címkéjének és megjegyzésének táblacella eleji alakja, a régi lap nagybetűsítése szerint, betűre).

## 4. A 218a végi lista egyéb tételei (megfigyelések és döntések, röviden)

A részletek a `naplok/F218_folytatas.md` és a `naplok/F218_jelentes.md` megnevezett szakaszaiban.
- **DT872, DT895 kézi szöveg (S2, S8a):** a Kivonat két átvezetése és törölt mondatai, a kritérium tagolása és a kettős szólista, a „Károli alapszövege” a lap elejére, a kizárási lista eltérése.
- **S3:** a H7451 glosszájának látható kihagyásjele („…” vagy „[…]”); a 4.12 bevezetője zárójelben megismétli a tágabb kört; a több lemmás 4.11-sor kétféle kezelése (saját-pár szűrő ⟂ egyforrás-kapu: az 1Kir 18:24 egyező görög szava kiesik); a 4.13–4.14 szótári alakjai kisbetűsítve, idézetként („úr”, „baál”, „ábrám”).
- **S5:** DT884 (az indoklás végleges alakja az adatban); a Minősítés „a {p}%-a” rögzített névelője (1%-nál és 5%-nál „a 5%-a” lenne).
- **S6:** DT888; a `funkcio` adatjavítás (43 + 1 cella); az ISTENTISZT-001 kisbetűs funkció-cellái; az üres funkció- és PaRDeS-cella „—” jele; az ISTENTISZT-001 Alátámasztásának Strong-száma és Markdown-kiemelése.
- **S7:** N214 (a szópáros bevezető ISTENTISZT-specifikus mondata); a tanú korának és a rabbinikus hivatkozásnak a szerkezeti bontása; a szópáros ÚSZ-mondat nevezője (12 a 14 felsorolt vers helyett) és a `kor` mező belső évszáma.
- **S8b:** GK-19 (T6): a Károli-párosítás pontosság-mondata a JOHD-validáció után (N219; döntéssel elhalasztva).
- **S9a (új):** a HAMART-001 1Krón 7:22 csoportos indoklása a látható szövegben „blokk-kizárás (a H7451 és a H7043 blokkjának mintájára)” fordulatot hoz (munkaszó és csupasz Strong-szám a döntésnapló kézi szövegében; a mai lapon is így áll, nem javítottam).
