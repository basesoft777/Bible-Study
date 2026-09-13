# PaRDeS-projekt: STEPBible ↔ SzPA join — adatcsatorna-dokumentáció (felfüggesztett alrendszer)

*Kiszervezve a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 4. szakaszából (F0.7, 2026.09.13) — 40,2 KB, a döntési fájl legnagyobb egyedi szakasza. Az SzPA-integráció a döntési fájl v23-as bejegyzése (2026.08.24) szerint **felfüggesztve, bizonytalan időre** — ez az alrendszer jelenleg nem aktív fejlesztés alatt áll. A tartalom változatlanul megőrizve, arra az esetre, ha az integráció valaha folytatódik.*

---

## 4. Az összekapcsolás: STEPBible ↔ SzPA join Strong-szám alapján

### 4.1 Háromrétegű adatbázis-architektúra

**1. réteg — Forrás-táblák** (nem módosulnak, csak beolvasásra kerülnek):

*Nyilvános (STEPBible-kivonat, publikus repó-rész):*
```
TAHOT_kivonat.tsv / TAGNT_kivonat.tsv
Igehely | Szósorszám | Strong | Ragozott alak | Kiejtés | Szótő | Szótári jelentés | Angol tükörfordítás | Kritikai kiadás*
```
*(a Kritikai kiadás oszlop csak a TAGNT-nál releváns; a héber ÓSZ-nél nincs ilyen elágazás)*

*Privát (SzPA, privát repó-rész) — két külön tábla könyvenként:*
```
[könyv]_versek.tsv:       Igehely | SzPA-szöveg (teljes vers)
[könyv]_labjegyzetek.tsv: Igehely | Lj# | Magyar kifejezés | Eredeti szó | Kiejtés | Jelentés-árnyalatok
```

*Nyilvános (Károli 1908, publikus repó-rész) — új, negyedik forrás:*
```
Karoli_1908.tsv (vagy könyvenkénti bontásban): Igehely | Károli-szöveg (teljes vers)
```
**Eredet:** `scrollmapper/bible_databases` (GitHub, MIT licenc a repóra, a Károli-forrás önmaga **közkincs**) — "HunKar: Revideált Károli Biblia 1908", strukturált JSON/SQL/CSV formátumban, `{"verse": 1, "text": "Kezdetben teremté Isten az eget és a földet."}` séma szerint. Ez a projekt **elsődleges** fordítása — eddig nem volt hozzá strukturált, gépileg kereshető adat, csak az SzPA (másodlagos, összehasonlító forrás) rendelkezett ilyennel.

**A "más Károli-verzió" kérdés:** ez az **1908-as revideált** kiadás (nem az eredeti 1590-es Vizsolyi Biblia) — a leggyakoribb, online is elterjedt "Károli"-szöveg. Ha a projekt korábbi tanulmányai egy eltérő kiadást idéztek, ez visszamenőleg ellenőrizendő (nyitott pont, lásd 8. szakasz).

**2. réteg — Az összekapcsolt (join) tábla** — ez a tényleges, generált végeredmény, ami *minden* STEPBible-sorhoz (tehát minden szóhoz, nem csak a lábjegyzeteshez) hozzárendel egy sort. **Mostantól háromoszlopos a magyar oldal** (Károli bevonásával, nem csak SzPA):
```
[könyv]_osszekapcsolt.tsv:
Igehely | Szósorszám | Strong | Eredeti szó | Kiejtés | Szótári jelentés | Angol tükörfordítás | Kritikai kiadás |
Károli megfelelés | Károli azonosítás módja | SzPA megfelelés | SzPA azonosítás módja | SzPA lábjegyzet-szöveg
```
**Fontos különbség a két magyar oszlop között:** a Károli-oszlopnál **nincs lábjegyzet-forrás** (a Károli maga nem tartalmaz fordítói jegyzeteket) — tehát a Károli-oszlopnál a hármas állapotból (lásd 4.2) csak kettő fordulhat elő: *tartalom-alapú azonosítás* vagy *nincs önálló megfelelés*, sosem *lábjegyzet-alapú*. Az SzPA-oszlopnál mindhárom állapot érvényes, változatlanul.

**Miért éri meg mindkét magyar fordítást egy sorban tartani:** ez teszi lehetővé, hogy egy jövőbeli tanulmány **közvetlenül összevesse**, hol egyezik és hol tér el a Károli és az SzPA fordítói döntése ugyanahhoz az eredeti szóhoz — ez pontosan az a fajta összevetés, amit korábban (a "Károli-hűség" és a szövegkritikai ⚠️ pontok kapcsán) csak esetenként, kézzel végeztünk.

**3. réteg — Fájlszervezés a privát repóban:**
```
Bible-Study-privat/
├── szpa/
│   ├── peldabeszedek_versek.tsv
│   ├── peldabeszedek_labjegyzetek.tsv
│   ├── apcsel_versek.tsv
│   └── apcsel_labjegyzetek.tsv
```
Bible-Study/  (publikus repó-rész)
├── konkordancia/
│   ├── TAGNT_kivonat.tsv
│   ├── TAHOT_kivonat.tsv
│   └── README.md
├── karoli/
│   ├── Karoli_1908.tsv              ← scrollmapper/bible_databases-ből, közkincs
│   └── README.md (forrás, licenc: MIT [repó] / Public Domain [szöveg], generálás dátuma)

Bible-Study-privat/  (privát repó-rész)
├── szpa/
│   ├── peldabeszedek_versek.tsv
│   ├── peldabeszedek_labjegyzetek.tsv
│   ├── apcsel_versek.tsv
│   └── apcsel_labjegyzetek.tsv
├── osszekapcsolt/
│   ├── peldabeszedek_osszekapcsolt.tsv   ← generált, a 2. réteg (Károli + SzPA együtt)
│   ├── apcsel_osszekapcsolt.tsv
│   └── README.md (mikor generálva, milyen STEPBible-verzióból, generálási módszer)
```

**Miért marad a join-tábla mégis privát a Károli bevonása után is:** bár a Károli-oszlop önmagában közkincs, a **teljes sor** (Károli + SzPA együtt egy táblában) a védett SzPA-adatot is tartalmazza — ezért a teljes összekapcsolt tábla továbbra is a privát repóba kerül. *(Elméletileg készíthető lenne egy külön, csak Károli+STEPBible join, ami tisztán publikus lehetne — ez egy jövőbeli, opcionális bővítés, ha valaha SzPA nélküli, csak Károli-alapú konkordanciára is szükség lenne.)*

**Tárolási hely elve:** mivel az összekapcsolt (join) tábla tartalmazza a védett SzPA-szöveget is, **a teljes join-tábla a privát repóba kerül**, még akkor is, ha az egyik forrás-oldal (STEPBible, most már a Károli is) önmagában nyilvános maradhat.

### 4.2 Az "Azonosítás módja" oszlop — hármas állapot (felváltja a korábbi kétállapotú leírást)

A Péld 1:1-4 és ApCsel 1:1-4 minták alapján kiderült, hogy a "van SzPA-lábjegyzet / nincs" kétállapotú megkülönböztetés **pontatlan** volt — a "nincs lábjegyzet" eset valójában **két, egymástól jól elkülönülő alesetre** bomlik:

| Állapot | Jelentése | Példa |
|---|---|---|
| **lábjegyzet-alapú** | SzPA-fordító saját magyarázata köti hozzá — legmagasabb megbízhatóság | Péld 1:2 "bölcsesség" ↔ חָכְמָה |
| **tartalom-alapú azonosítás** | angol gloss segítségével beazonosítva (jelentés szerint, nem pozíció szerint), de nincs SzPA-kommentár hozzá | Péld 1:1 "Salamonnak" ↔ שְׁלֹמֹה |
| **nincs önálló megfelelés** | funkciószó (névelő, nyomatékosító partikula), aminek nincs önálló magyar szava a fordításban | ApCsel 1:1 τὸν (névelő), μέν (nyomatékosító) |

**Miért fontos a megkülönböztetés:** az első két állapot esetében **van** azonosítható magyar szó a join-táblában (csak eltérő megbízhatósággal), a harmadik esetben viszont **nincs is mit azonosítani** — ezt korábban tévesen ugyanabba a "üres mező" kategóriába soroltuk, mint a lábjegyzet-hiányt, pedig ez két, tartalmilag eltérő helyzet.

**A módszer, ami a tartalom-alapú azonosítást lehetővé teszi:** a 8-oszlopos STEPBible-kivonat 7. oszlopa (kontextuális angol tükörfordítás) horgonyként szolgál ahhoz, hogy — akár kézzel, akár nyelvi modell segítségével — a magyar mondatban **jelentés szerint**, pozíciótól függetlenül megtalálható legyen a megfelelő szó. **Ez nem old fel egy tartalmi hiányt** (a fordítói *magyarázat* hiánya továbbra is explicit jelzve marad) — csak azt teszi lehetővé, hogy a magyar szó *azonosítása* (nem a *magyarázata*) megbízható legyen.

*(Elvetett alternatíva a szó-azonosításra: horgonypont-alapú, pozíció-szerinti interpoláció — kísérlettel igazoltan megbízhatatlan héber szövegnél, mert a héber és a magyar szórend rendszeresen eltér, különösen birtokos szerkezeteknél és célhatározói igéknél [lásd Péld 1:1-4 kísérlet]. Görög szövegnél [ApCsel 1:1-4] a szórend-eltérés kisebb, de az egységesség kedvéért a tartalom-alapú módszer mindkét testamentumnál alkalmazandó.)*

### 4.3 További megfigyelések az ApCsel-mintából

**A) A kritikai kiadás-oszlop "nincs eltérés" eredménye is informatív.** Az ApCsel 1:1-4 mind a 19 vizsgált szavánál minden kiadás (NA28-tól Byz-ig) egyezett — nincs szövegkritikai ⚠️ pont ebben a szakaszban. Ez nem "üres" vagy haszontalan eredmény: megerősíti, hogy a Károli/SzPA és a modern kritikai szövegek **teljesen egyeznek** ezen a szakaszon, ami egy jövőbeli tanulmány szövegkritikai ellenőrzési lépésének (lásd a sablon-módosítások között) pozitív, dokumentálandó eredménye.

**B) Egy SzPA-lábjegyzet néha több görög/héber szóra is vonatkozik.** Az ApCsel 1:2-nél a 3. lábjegyzet ("utasításokat adott az apostoloknak") egyszerre két STEPBible-sorhoz kapcsolódik (`ἐντειλάμενος` + `ἀποστόλοις`). A join-tábla generálásakor ezt jelölni kell (pl. mindkét sor "lábjegyzet-alapú" állapotot kap, azonos lábjegyzet-szöveggel, vagy egy "lásd Lj.X" kereszthivatkozással) — a kapcsolat **nem mindig szigorúan 1:1** arányú.

### 4.4 A generálás korlátja

A **lábjegyzet-alapú sorok** gépiesen, megbízhatóan generálhatók (az SzPA lábjegyzet-tábla és a STEPBible Strong-száma egyértelműen összeköthető). A **tartalom-alapú azonosítás** viszont — ahogy mindkét mintánál is történt — **nem tisztán szkriptelhető**, mert szemantikai felismerést igényel; egy teljes könyv generálásakor ez a réteg **kézi átnézést vagy egy nyelvi modell soronkénti közreműködését** igényli, nem egy egyszeri, automatikus script-futtatást.

### 4.5 Miért éri meg mindezt megépíteni

Ez a join gyakorlatilag **egy egyedi, magyar nyelvű, Strong-számmal ellátott konkordanciát** hoz létre — mostantól nemcsak az SzPA-hoz, hanem a **Károlihoz is**. Ilyen, tudomásunk szerint, jelenleg nyilvánosan nem létezik egyetlen magyar bibliafordításhoz sem. Ez túlmutat egy kényelmi eszközön — önálló, projekt-specifikus erőforrás.

### 4.6 Egyéb, a scrollmapper/bible_databases keresésekor azonosított elemek

**Kereszthivatkozás-adatbázis (openbible.info alapú, szavazat-súlyozott)** — a `cross_references` tábla a repóban minden vershez ad lehetséges kereszthivatkozás-jelölteket, relevancia-szavazatszámmal. **Hasznos segédeszköz** a 3/b pont kereszthivatkozás-kereséséhez: nem helyettesíti a tartalmi mérlegelést, de **kiindulási jelöltlistát** ad, amit utána a szokásos módon (lexikai vs. tematikus elhatárolás, STEPBible-ellenőrzés) kell kiértékelni.

**Károli-specifikus kereszthivatkozás-adat (`krisek/HunKar`, GitHub) — új, valószínűleg jobb elsődleges forrás ugyanerre a célra.** Ez egy önálló SWORD-modul repó (Károli 1908, OSIS XML formátum, forrása a `szentiras.hu/KG`), ami **Strong-számot nem tartalmaz**, de **beépített, versenkénti kereszthivatkozásokat** ad, közvetlenül a magyar Károli-hagyományból:
```xml
<verse osisID="Gen.1.1">Kezdetben teremté Isten az eget és a földet.
  <reference osisRef="Gen.2.4-Gen.2.5">1Móz 2,4-5</reference>
  <reference osisRef="Ps.33.6">Zsolt 33,6</reference>
  <reference osisRef="Acts.14.15">Csel 14,15</reference>
  ...
</verse>
```
**Miért lehet jobb, mint a scrollmapper/openbible.info-adat:** ez **magyar, Károli-specifikus, valószínűleg teológiai szerkesztők által összeállított** hivatkozásrendszer (a `szentiras.hu` mögötti szerkesztőségtől), nem angol nyelvű, crowdsourced szavazat-alapú lista. Közvetlenül a projekt elsődleges forrásához (Károli) kötődik, nem egy másik nyelvű köztes fordításhoz.

**A két kereszthivatkozás-forrás egymáshoz való viszonya — nyitva hagyva, nem eldöntve:** mindkettő **kiindulási jelöltlistaként** szolgálhat a 3/b ponthoz, nem helyettesítik a tartalmi mérlegelést. Lehetséges, hogy a kettő **kiegészíti** egymást (a Károli-specifikus szűkebb, de megbízhatóbb; az openbible.info szélesebb, de vegyesebb minőségű) — ez a kérdés egy jövőbeli, tényleges összevetéssel dönthető el, nem itt, elméletben.

**Strong-taggelt Károli — a mélykutatás megtalálta, de zárt licenc alatt.** A `krisek/HunKar` és a scrollmapper-es Károli-forrás mellett végzett mélyebb kutatás **egyetlen, ténylegesen létező, teljes** Strong-tagelt Károlit azonosított: a **Biblia-Felfedező (Bible-Discovery)** program "Károli Gáspár Biblia – Strong számokkal (HUN)" modulja (Zsidó Miklós fejlesztése, mobilbiblia.hu / bible-discovery.com). Ez **valódi, szó szintű** párosítás (nem csak névleges, mint a scrollmapper KJV esetében), a teljes Bibliára (ÓSZ+ÚSZ) elkészült. **Licenc:** zárt — "A Strong párosítás Zsidó Miklós tulajdona. Minden jog fenntartva… Tilos a Művet… forgalmazni… módosítani… szétbontani illetve visszafejteni." A programon kívüli adatkiemeléshez egyedi engedélykérés szükséges (info@mobilbiblia.hu). Egy Bible-software fórumbeszélgetés (biblesupport.com) megerősíti, hogy a Strong-számok kézi hozzáadása egy fordításhoz **általánosan nehéz, homográf-problémákkal terhelt feladat** — ez a Biblia-Felfedező munkájának valódi szakmai értékét is alátámasztja.

**A döntés (lásd 4.7): a Biblia-Felfedező nem lesz elsődleges adatforrás**, mert a zárt licenc pontosan ugyanabba az akadálytípusba ütközik, mint korábban az ESV/Crossway és az Accordance-eset — használható eszköz, de nem exportálható adat.

**KJV/KJVA/RLT "Strong-taggelt" verziói (scrollmapper) — megvizsgálva, jelenleg NEM használható.** A fordítás neve ("with Strongs Numbers and Morphology") a SWORD-modul eredeti elnevezéséből öröklődött, de a scrollmapper könnyen elérhető JSON-konverziója **ténylegesen nem tartalmazza** a Strong-tageket (ellenőrizve: `{"verse": 1, "text": "In the beginning God created..."}`, tag nélkül). A nyers forrás (`sources/en/KJV/`) elvben tartalmazhatja, de **külön feldolgozást** igényelne, és a forrás licence ott **GPL** (nem egyszerű közkincs) — ez nem oldja meg a korábban azonosított "természetes szórendű, Strong-taggelt angol szöveg" hiányt.

**AndBible fejlesztői terv (2026 Q2/Q3, figyelendő, nem kész eszköz).** Az AndBible nyílt forráskódú Biblia-app dokumentált fejlesztési terve szerint egy **AI-alapú Strong-taggelési pipeline-t** építenek, ami egy referencia-Bibliából (KJV/WEB, közkincs) automatikusan hozzárendel Strong-számokat **bármely más fordításhoz** — koncepcionálisan ez pontosan a projekt saját, kézzel végzett "tartalom-alapú azonosítási" módszerét automatizálná. Nem publikált eszköz, csak fejlesztői útiterv — érdemes később visszatérni rá.

### 4.7 Végleges döntés: a Károli-dataset forrása

**A Károli-dataset elsődleges forrása: a közkincs HunKar-szöveg (scrollmapper), Strong-párosítással a projekt már meglévő, tanulmányvezérelt, tartalom-alapú generálási módszerével** (lásd 4.2, 7.1, 7.2) — **nem** a Biblia-Felfedező.

**Indoklás:**
1. **Azonnal elindítható**, nincs engedélykérésre várás (szemben a Biblia-Felfedezővel, ahol egyedi, elbírálás-függő engedély kellene)
2. **Nulla plusz jogi kockázat** — a HunKar bázisszöveg közkincs
3. **A meglévő infrastruktúrába illeszkedik** — a join-tábla, a kumulatív generálás, a kritériumlista mind eleve erre lett kidolgozva
4. **Konzisztens a Károli sajátosságával:** mivel a Károli-szövegnek nincs lábjegyzet-forrása (szemben az SzPA-val), a Károli-oszlop a hármas állapotból (4.2) mindig csak a *tartalom-alapú azonosítás* vagy a *nincs önálló megfelelés* állapotot veheti fel, sosem a *lábjegyzet-alapút* — ez nem hiányosság, hanem a forrás jellegéből következő, várt korlát

**A Biblia-Felfedező szerepe emiatt referencia-eszközzé alakul, nem adatforrássá:** ha egy saját, tartalom-alapú Károli-Strong párosításnál bizonytalanság merül fel, a Biblia-Felfedező programban (ha hozzáférhető) **kézzel visszaellenőrizhető**, hogy a saját azonosítás egyezik-e a professzionális párosítással — anélkül, hogy azok adatát kiemelnénk vagy másolnánk.

**Utólagos felismerés (4.11-es validáció során): a "Károli" név alatt legalább KÉT, szövegszerűen eltérő revízió létezik, más-más jogi státusszal.** A validáció (lásd 4.11) során kiderült, hogy a felhasználó által megadott külső referencia a jelenlegi 1908-as HunKar-szövegnél **modernebb** alakokat használt egyes verseknél (1Móz 1:2: "volt"/"sötétség"/"lebegett" a HunKar "vala"/"setétség"/"lebeg vala" helyett) — ez egy **másik, "Revideált Károli" néven ismert, 2011-es kiadás (Veritas Kiadó)**, ami **© védett, nem közkincs** (szemben a jelenleg használt 1908-as HunKar-ral). A Biblia-Felfedező program feltehetően ezt a 2011-es revíziót futtatja, nem az 1908-ast — ez magyarázza a referencia eltérő alakjait. **A projekt publikus Károli-datasete (`Karoli_1908.tsv`) emiatt is az 1908-as HunKar-on marad** — a Veritas 2011-es revízió licenc-kockázata miatt nem cserélhető rá jogosultság nélkül. Részletek és nyitott döntés: lásd 8. szakasz.

### 4.8 KJV-hidas módszer — validált, ellenőrzött forrással megerősítve

**A módszer:** a tartalom-alapú azonosításnál (4.2) a nyers STEPBible angol tükörfordítás helyett/mellett a **KJV természetes szórendű, teljes mondatszerkezete** szolgál hídként a héber/görög Strong-szám és a Károli/SzPA-szó között. Ez azért segít, mert a KJV **grammatikai szerkezete** (alany-állítmány-tárgy) explicit jelzést ad ott, ahol a nyers szó-glosszok csak egyenrangú jelentés-listát adnak.

**Demó-eredmény (Péld 23:1-4, vak teszt):** a csak STEPBible-glosszra épülő módszer 9/10 (90%) pontosságot ért el; a KJV-hidas módszer **10/10 (100%)** — a kritikus eset (23:2, "mértékletlen" — H1167 "master of" vs. H5315 "appetite") a KJV *"if thou be **a man given to** appetite"* mondatszerkezete alapján oldódott meg helyesen, mert az egyértelműsítette, melyik héber szó az állítmány.

**Forrás — megtalálva és validálva** *(korábbi "még beszerzendő" jelölés lezárva)*: **valódi, ténylegesen beágyazott** Strong-taggelt KJV-szöveg, **öt egymástól független oldalon** megerősítve (nem egyetlen, bizonytalan forrás):
- **`studybible.info/KJV_Strongs/[Könyv]`** — **elsődleges, ajánlott forrás**: könyv-szintű navigációval (mind a 31 fejezet egy oldalon), morfológiai kóddal kiegészítve — ezzel a formátummal készült el ténylegesen a teljes Példabeszédek-dataset (lásd 0. szakasz, 5-6. sor)
- `biblehub.com/kjvs/` (pl. `biblehub.com/kjvs/proverbs/23.htm`) — másodlagos, ugyanúgy validált
- `godrules.net/library/kjvstrongs/`
- `sacrednamebible.com/kjvstrongs/`
- `bibletruthpublishers.com`

**Eredet:** héber Strong-számok — Bible Foundation (bf.org); görög Strong-számok (ÚSZ) — CrossWire KJV2003 projekt. **Licenc:** az Egyesült Királyságban a KJV szövege "Crown copyright" alatt áll, de ez **csak a kereskedelmi nyomtatásra** vonatkozik ott — a világ többi részén, és nem-kereskedelmi/kutatási célra szabadon használható.

**Független megerősítés a saját adat hitelességére:** a fenti forrásokból lekért Strong-számok **számjegyre pontosan egyeztek** a felhasználó saját, korábban bemutatott Károli-Strong adatával (pl. Péld 23:7: számítgatja=8176/8804, magában=5315, egyél=398/8798, igyál=8354/8798, mondja=559/8799, akarattal=3820 — mind egyezik) — ez megerősíti, hogy a felhasználó saját adata **ugyanerre a szabványos, közkincs KJV-Strong konvencióra** épül.

**SzPA-specifikus szabály — kettős következtetés: alapértelmezett javítás, DE explicit kivétel-lista**

**1. Alapszabály:** a KJV-híd **alapértelmezetten bevezetendő** az SzPA tartalom-alapú azonosításánál is — a legtöbb, teológiailag semleges szónál (ahogy a Károli-demó mutatta) ugyanúgy javítja a pontosságot, mert a KJV természetes mondatszerkezete ugyanazt a grammatikai egyértelműsítést adja, függetlenül attól, melyik magyar fordítást (Károli vagy SzPA) kötjük hozzá.

**2. Kivétel-lista — azok a fogalmak, ahol az SzPA tudatosan, dokumentáltan eltér a hagyományos angol (KJV-szerű) fordítási konvenciótól.** Ezeknél a KJV-hidas eredményt **fokozott gyanakvással**, nem automatikusan kell elfogadni, mert éppen itt állhat a KJV a legtávolabb az SzPA szándékos választásától:

| Fogalom | Hagyományos angol (KJV) | SzPA tudatos választása | Miért kockázatos a KJV-híd itt |
|---|---|---|---|
| βαπτίζω (baptizó) | "baptize" | **"alámerít"** | a KJV át nem fordított, transzliterált szava ("baptize") semmilyen tartalmi/grammatikai támpontot nem ad a magyar "alámerít" igéhez |
| πνεῦμα ἅγιον (pneuma hagion) | "Holy Ghost/Spirit" | **"Szent Szellem"** | a "Ghost" szó a mai angolban már nem hordozza a "szellem" jelentésmezőt, félrevezető párhuzamot adhat |
| ἔθνη (ethné) | "Gentiles" | **"nemzetek"** | a "Gentiles" kulturálisan szűkebb (zsidó szempontból "nem-zsidók"), míg a "nemzetek" tágabb, semlegesebb — a KJV itt egy értelmezési döntést is magával hozna |

**3. A kivétel-lista bővítendő, tanulmányvezérelt alapon:** ez a három tétel a beszélgetésben eddig felmerült, dokumentált esetekre épül — **nem kimerítő lista**. Minden jövőbeli tanulmánynál, ahol az SzPA lábjegyzete kifejezetten jelez egy tudatos, hagyománytól eltérő fordítói döntést (ahogy a projekt korábbi terminológiai szabályai is rögzítik, pl. "Szent Szellem" nem "Szentlélek", "spirituális" nem "misztikus"), az adott szó **automatikusan felkerül** erre a listára, mielőtt a KJV-hidas azonosítást rá alkalmaznánk.

**4. Gyakorlati szabály a join-táblában:** minden SzPA-oszlopos sor, ami a kivétel-listán szereplő Strong-számhoz kapcsolódik, kap egy **"⚠️ KJV-híd óvatossággal kezelendő"** jelölést — ez nem zárja ki a KJV-híd használatát, csak jelzi, hogy az eredményt **kézzel is ellenőrizni kell**, mielőtt a "tartalom-alapú azonosítás" állapotot magas bizonyossággal rögzítjük.

### 4.9 Második validáló forrás: ASV (American Standard Version, 1901) — kereszt-ellenőrzés

**A forrás:** ASV, 1901, közkincs alapszöveg; a Strong-taggelés a "Cross Word Project" (Wade Maxfield) munkája — **független** a KJV-Strongs taggelésétől (Bible Foundation/CrossWire), tehát valódi, nem csak formális második forrás. **Elsődleges, ajánlott elérés:** `studybible.info/ASV_Strongs/[Könyv]` — könyv-szintű belépési pont, mind a 31 fejezet linkjével egy oldalon, ugyanazzal a szerkezettel, mint a KJV-nél. *(Fontos: a `biblehub.com/asv/` **nem** Strong-taggelt — csak sima szöveg; a biblehub.com-on nincs külön "ASV+Strong's" útvonal, ellentétben a KJV-vel.)*

**A módszer bővítése:** a join-tábla "Azonosítás módja" oszlopa (4.2) egy negyedik, finomított állapottal egészül ki, amikor KJV-híd alkalmazva van:

| Alállapot | Jelentés | Megbízhatóság |
|---|---|---|
| KJV + ASV egyezik | két független forrás ugyanoda mutat | legmagasabb |
| csak KJV vagy csak ASV elérhető | egy forrás, nincs kereszt-ellenőrzés | közepes |
| **KJV ≠ ASV eltérés** | a két forrás eltérő angol megfogalmazást ad | **explicit ⚠️ jelzés — kézi ellenőrzés kötelező** |

**Demonstrált eset — Péld 23:1, valódi, a mintában ténylegesen előforduló eltérés:**

| Forrás | Megfogalmazás | H0834 ("that which") értelmezése |
|---|---|---|
| KJV | *"consider diligently **what** is before thee"* | tárgyra utal (étel) |
| ASV | *"consider diligently **him** that is before thee"* | személyre utal (uralkodó) |
| Károli | *"...**ki** van előtted"* | **személyre utaló** vonatkozó névmás |

**A Károli "ki" szava egyértelműen az ASV értelmezésével egyezik, nem a KJV-vel.** Ha csak a KJV szolgált volna hídként, ez tévesen sugallhatta volna, hogy a "ki" valamiért mégis egy tárgyra utaló szerkezetet fordít. Az ASV bevonása **azonnal jelezte** az eltérést, és a helyesebb irányba terelt — ez **konkrét, mérhető bizonyíték** a kereszt-ellenőrzés gyakorlati értékére, nem csak elméleti előny. *(A 23:2-4 verseknél az ASV szó szerint megegyezett a KJV-vel — ott a második forrás csak megerősítést adott, nem új információt, ami várható, hiszen az ASV a KJV/ERV hagyomány folytatása.)*

**A teljes lánc, az eredeti szöveg Strong-adatáig visszavezetve — ez magyarázza meg, honnan ered az eltérés:**

| Réteg | Adat |
|---|---|
| Héber szó (Strong) | אֲשֶׁר (H0834A) |
| Kiejtés | *ásér* |
| STEPBible gloss | *"[that] which"* |
| KJV | *"what"* |
| ASV | *"him"* |
| Károli | *"ki"* |

**Kulcsfelismerés:** a héber *ásér* egy **eredendően semleges vonatkozó névmás**, ami egyaránt vonatkozhat személyre és tárgyra (kb. "aki/ami") — a **STEPBible nyers gloss is ezt a semlegességet tükrözi**, nem dönt személy/tárgy között. A KJV és az ASV fordítói **egymástól függetlenül, külön-külön döntöttek** ebben a kérdésben — a kétértelműség tehát **nem fordítási hiba**, hanem **magának az eredeti héber szövegnek a tulajdonsága**.

**Módszertani tanulság — pontosítja a KJV≠ASV jelzés értelmezését:** egy ilyen ⚠️ jelzésnél a kézi ellenőrzésnek **nem mindig az a kérdése, "melyik forrás téved"** — gyakran azt kell megállapítani, hogy **maga az eredeti szöveg enged-e több értelmezést**. Ez utóbbi eset **önmagában is értékes exegetikai megfigyelés**, ami akár egy jövőbeli tanulmány ⚠️ vitatott pontjának alapja is lehet (a saját kritérium 5. pontja szerint: "a szó jelentése önmagában ad okot egy vitatott pontra") — nem csupán technikai zajként kezelendő.

### 4.10 getbible.net API — megvizsgálva, lezárva, nem használjuk

**A kísérlet célja:** kideríteni, van-e egyetlen letöltéssel elérhető, teljes KJV/ASV Strong-taggelt bulk-forrás (a fejezetenkénti scraping helyett), a `getbible.net` API-n keresztül.

**Eredmény:** a `getbible.net` (minden aldomainjével, így `api.getbible.net`-tel együtt) **szervezeti szintű hálózati tiltás alatt áll** a claude.ai munkakörnyezetben — Claude Code-ban végzett teszt sem tudta közvetlenül lekérdezni, a proxy explicit policy denial (403) választ adott.

**Közvetett bizonyíték, GitHub-forrásokból (nem a tiltott API-ból):**
- Az ASV fordítás kulcsa ebben az API-ban ténylegesen `asv` (megerősítve a `getbible/v2` repó gyökérszerkezetéből)
- A `getbible/v2` repóban a `kjv/` mappák **csak metaadatot/SHA-ellenőrzőösszeget** tartalmaznak, a tényleges verstartalmat élőben szolgálja ki a szerver — statikus bulk-fájl **nincs** a repóban magában
- A `getbible/getbiblesword` (az adatfeldolgozó motor) README-je explicit megkülönbözteti a *"rendered text"* (megjelenítésre szánt, feltehetően tag-mentes) és a *"decoded base64 bytes as authoritative"* (nyers, hiteles forrás) fogalmakat — ez arra utal, hogy a publikus JSON `"text"` mezője valószínűleg **tag-mentes**, a Strong-adat csak a mögöttes SWORD-modulban van jelen

**Elsőkézből való megerősítés:** a felhasználó saját gépéről közvetlenül tesztelte a `getbible.net` API-t (a hálózati tiltás miatt itt nem volt lehetséges) — **megerősítve: nincs Strong-szám** a kimenetben. Ez a közvetett GitHub-bizonyítékot véglegesen igazolja.

**Mintázat-felismerés:** ez már **második, egymástól független, ténylegesen ellenőrzött eset** (az első a scrollmapper-KJV volt), ahol egy kényelmes, felhasználóbarát API/JSON-forrás **ígéri** a Strong-taggelést a nevében/metaadatában, de a **tényleges kimenet nem tartalmazza** — a mögöttes, valódi taggelt adat mindkét esetben egy SWORD-modulban van, amit a kényelmi réteg "letisztít" emberi olvasásra. **Ez általános óvatossági elvvé emelhető**: bármely jövőbeli, hasonlóan kényelmes API/JSON-forrást eleve gyanakvással kell kezelni, amíg tételesen nem ellenőrizzük a tényleges kimenetet, a névre/metaadatra hagyatkozás helyett.

**Végleges döntés: nem keresünk tovább bulk API-alternatívát.** A validált, ténylegesen ellenőrzött módszer (`studybible.info/[KJV_Strongs|ASV_Strongs]/[Könyv]`, könyv-szintű navigációval, fejezetenkénti lekérdezéssel) marad az egyetlen működő út — ezzel a módszerrel készült el ténylegesen a teljes Példabeszédek KJV+ASV dataset (lásd 0. szakasz).

### 4.11 Károli-Strong tartalom-alapú párosítás — validálva külső referenciával

**A validáció célja:** a projekt saját, STEPBible-alapú tartalom-alapú Károli-Strong azonosítási módszere (lásd 4.2) eddig kizárólag **belső** ellenőrzéssel (a saját logika önmagával való konzisztenciájával) volt alátámasztva. A felhasználó egy külső, feltehetően Biblia-Felfedezőből vagy hasonló professzionális forrásból származó, Strong-taggelt Károli-referenciát adott meg 1Móz 1:2-4-re, ami **első alkalommal** tette lehetővé egy **független** forrással való összevetést.

**Eredmény: 1Móz 1:3-4-en 13/14 szó pontosan egyezett** — beleértve két, elsőre bonyolultnak tűnő esetet is, amik a módszer megbízhatóságát különösen jól próbára tették:

- **"látá"** — a referencia egyetlen Károli szóra **kettős taggelést** ad: H0853 (tárgyeset-jelölő) + H7200 (látott). Ez pontosan megfelel a `TAHOT_kivonat.tsv` két külön sorának ugyanahhoz a héber szóhoz (H0853 + H7200G) — a projekt saját, morfémánkénti szétbontási logikája (lásd a TAHOT-kivonat módszertana, `konkordancia/TAHOT_TAGNT_README.md`) itt függetlenül igazolódott.
- **"elválasztá" / "a sötétségtől"** — a héber kettős "között...között" szerkezet (H0996 kétszer) helyesen oszlik meg a két Károli kifejezés között, nem csúszik el egy pozícióval — ez pontosan az a fajta eset, ahol a 4.2-ben elvetett, pozíció-alapú interpoláció korábban megbukott, és amit a tartalom-alapú módszer volt hivatva megoldani.

**Az egyetlen eltérés — dokumentálandó, nem hiba:** a "jó" szónál a referencia H2896-ot ad, a `TAHOT_kivonat.tsv` H2895-öt. Ez a טוֹב (tov) gyök **két szomszédos Strong-száma** (H2895 igei alak, "jónak lenni"; H2896 melléknévi alak, "jó") — nyelvtanilag mindkét elemzés védhető erre a mondatra ("hogy jó a világosság"), a kétértelműség **magának a szónak a tulajdonsága** (hasonlóan a 4.9-es ásér/H0834-es esethez), nem fordítási vagy módszertani hiba.

**Jelentősége:** ez az első alkalom, hogy a projekt saját, belső STEPBible-alapú Károli-Strong módszertanát **külső, független forrással** vetettük össze. A 13/14 (93%) egyezés — beleértve a bonyolultabb, kettős-taggelésű eseteket is — megerősíti, hogy a 4.7-es pontban rögzített döntés (saját, tartalom-alapú módszer a közkincs HunKar-ra építve, nem a Biblia-Felfedező) **technikailag életképes és megbízható eredményt ad**, nem csupán jogilag a legtisztább út.

**Mellékfelismerés:** a validáció során derült ki, hogy a felhasznált külső referencia egy **másik, szövegszerűen eltérő Károli-revízióból** származhat, más jogi státusszal — lásd 4.7 és 8. szakasz.

### 4.12 Join-tábla lefedettség — gyors áttekintés

Ez a táblázat minden alkalommal frissítendő, amikor egy tanulmány új sorokat ad a `konkordancia/Karoli_Strong_kivonat.tsv`-hez (lásd `Join_tabla_folyamat_magyarazat.md`). A "Feldolgozott versek száma" a benne szereplő **egyedi** igehelyek száma (nem a szósorok száma), az "Összes vers a könyvben" a `Konyv_normalizalo_tabla.tsv` és a `Karoli_1908.tsv` alapján számolható.

**Jelenlegi állapot (2026.08.24):** a `Karoli_Strong_kivonat.tsv` most jött létre, üres fejléc-fájlként — a korábbi kézi kísérletek (1Móz 1:2-4) ebben a chat-munkamenetben készültek, nem a repóban, ezért egyelőre nem számítanak bele. A táblázat minden könyvnél 0-val indul.

| Könyv | Feldolgozott versek száma | Összes vers a könyvben | Lefedettség |
|---|---|---|---|
| 1Móz | 0 | 1533 | 0% |
| 2Móz | 0 | 1213 | 0% |
| 3Móz | 0 | 859 | 0% |
| 4Móz | 0 | 1288 | 0% |
| 5Móz | 0 | 959 | 0% |
| Józs | 0 | 658 | 0% |
| Bír | 0 | 618 | 0% |
| Ruth | 0 | 85 | 0% |
| 1Sám | 0 | 811 | 0% |
| 2Sám | 0 | 695 | 0% |
| 1Kir | 0 | 817 | 0% |
| 2Kir | 0 | 719 | 0% |
| 1Krón | 0 | 942 | 0% |
| 2Krón | 0 | 822 | 0% |
| Ezsd | 0 | 280 | 0% |
| Neh | 0 | 406 | 0% |
| Eszt | 0 | 167 | 0% |
| Jób | 0 | 1070 | 0% |
| Zsolt | 0 | 2527 | 0% |
| Péld | 0 | 915 | 0% |
| Préd | 0 | 222 | 0% |
| Én | 0 | 117 | 0% |
| Ézs | 0 | 1292 | 0% |
| Jer | 0 | 1364 | 0% |
| Sir | 0 | 154 | 0% |
| Ez | 0 | 1273 | 0% |
| Dán | 0 | 357 | 0% |
| Hós | 0 | 197 | 0% |
| Jóel | 0 | 73 | 0% |
| Ámós | 0 | 146 | 0% |
| Abd | 0 | 21 | 0% |
| Jón | 0 | 48 | 0% |
| Mik | 0 | 105 | 0% |
| Náh | 0 | 47 | 0% |
| Hab | 0 | 56 | 0% |
| Sof | 0 | 53 | 0% |
| Hag | 0 | 38 | 0% |
| Zak | 0 | 211 | 0% |
| Mal | 0 | 55 | 0% |
| Mt | 0 | 1071 | 0% |
| Mk | 0 | 680 | 0% |
| Luk | 0 | 1151 | 0% |
| Ján | 0 | 879 | 0% |
| ApCsel | 0 | 1007 | 0% |
| Róm | 0 | 431 | 0% |
| 1Kor | 0 | 436 | 0% |
| 2Kor | 0 | 256 | 0% |
| Gal | 0 | 149 | 0% |
| Ef | 0 | 155 | 0% |
| Fil | 0 | 104 | 0% |
| Kol | 0 | 95 | 0% |
| 1Thessz | 0 | 89 | 0% |
| 2Thessz | 0 | 47 | 0% |
| 1Tim | 0 | 113 | 0% |
| 2Tim | 0 | 83 | 0% |
| Tit | 0 | 46 | 0% |
| Filem | 0 | 25 | 0% |
| Zsid | 0 | 303 | 0% |
| Jak | 0 | 108 | 0% |
| 1Pét | 0 | 105 | 0% |
| 2Pét | 0 | 61 | 0% |
| 1Ján | 0 | 105 | 0% |
| 2Ján | 0 | 13 | 0% |
| 3Ján | 0 | 15 | 0% |
| Júd | 0 | 25 | 0% |
| Jel | 0 | 405 | 0% |

### 4.13 Önellenőrzési mechanizmus — kereszt-ellenőrzés és megbízhatósági jelölés

**Miért a KJV/ASV a kereszt-ellenőrző forrás, nem közvetlenül a STEPBible:** a Károli-Strong sor ELEVE a STEPBible (TAHOT/TAGNT) Strong-számából és angol glosszából születik, tartalom-alapú azonosítással (lásd 4.2 pont). A STEPBible tehát az ELSŐDLEGES BEMENET ehhez a lépéshez, nem egy második, független forrás — önmagával nem lehet kereszt-ellenőrizni, mert az körkörös lenne (saját magunk munkáját saját magunkkal igazolnánk vissza, új információ nélkül). A KJV és az ASV ezzel szemben VALÓDI, FÜGGETLEN források — nem a STEPBible-ből származnak, külön projektek, külön fordítói döntésekkel (Bible Foundation/CrossWire, illetve a Cross Word Project, lásd 4.8-4.9 pont). Amikor egy Károli-szóhoz generált Strong-számot összevetjük azzal, amit a KJV/ASV ugyanahhoz a Strong-számhoz, ugyanahhoz a vershez rendel, ez valódi, független megerősítés — pontosan úgy, ahogy a Pro.23.1 "ki"/"him"/"what" esetnél is működött (4.9 pont).

Minden új Károli-Strong sor generálásakor, MIELŐTT a `Karoli_Strong_kivonat.tsv`-be kerülne:

1. Ellenőrizd, van-e `KJV_Strongs_[Könyv].tsv` vagy `ASV_Strongs_[Könyv].tsv` adat ugyanarra az igehelyre és Strong-számra.
2. HA VAN és egyezik → "magas" megbízhatóság.
3. HA VAN, de ELTÉR → ÁLLJ MEG, ne generáld automatikusan — ez explicit kézi vizsgálatot igényel (lásd a Gen.1.1 "what"/"him" KJV≠ASV esetet a 4.9 pontban mintaként — lehet, hogy maga az eredeti szöveg enged több értelmezést).
4. HA NINCS KJV/ASV-adat arra a könyvre → "közepes" megbízhatóság.
5. Ha a szó Strong-száma vagy nyelvtani szerepe MAGA is vitatott (két szomszédos, rokon Strong-szám közül bármelyik védhető) → "bizonytalan", a vitát röviden dokumentálva a sor mellett vagy a `Validacios_naplo.md`-ben.

Minden 10. újonnan generált sornál (mintavételesen) érdemes egy független forrással (pl. egy külső, kézzel ellenőrzött referenciával, ha rendelkezésre áll) össze is vetni, és az eredményt a `Validacios_naplo.md`-be rögzíteni — ez korai riasztást ad, ha a módszer valahol szisztematikusan félrecsúszna.

**A `Karoli_Strong_kivonat.tsv` "Megbízhatóság" oszlopának lehetséges értékei, egységesen, csak ezek közül:**
- **"magas"** — egyértelmű, és ha van KJV/ASV-adat arra a versre, az is megerősíti
- **"közepes"** — tartalom-alapú azonosítás, de nincs KJV/ASV kereszt-ellenőrzés (mert arra a könyvre/versre nincs KJV/ASV-Strongs adat a `konkordancia/` mappában)
- **"bizonytalan"** — a szó jelentése/nyelvtani szerepe MAGA is vitatott a forrásokban (pl. mint a Gen.1.4-nél a H2895/H2896 kettős Strong-lehetőség "jó" szóra)
- **"—"** — nincs önálló magyar megfelelés (funkciószó, mint névelő vagy tárgyeset-jel)

### 4.14 A Károli-Strong lefedettség növelésének várható előnyei — nem lineáris haszon

Ahogy a `Karoli_Strong_kivonat.tsv` lefedettsége nő (több könyv, több tanulmányból származó adat), a haszon NEM egyenletesen jelentkezik — érdemes megkülönböztetni a korai és a csak nagy léptéknél jelentkező előnyöket.

**Korai haszon — már kis lefedettségnél is jelentkezik:**

1. **Pontosabb lexikai vs. tematikus megkülönböztetés a 3/b pontnál.** A `Karoli_kereszthivatkozasok.tsv` jelenleg csak azt adja meg, mely versek kapcsolódnak — nem azt, hogy lexikailag vagy csak tematikusan. Ha egyre több kapcsolódó vershez van Károli-Strong adat is, gépileg ellenőrizhető, hogy két kapcsolódó vers ugyanazt a Strong-számot használja-e — ez a lexikai/tematikus elhatárolás egy részét gépi ellenőrzéssel is támogathatóvá teszi.

2. **A tematikus tanulmányok találati listájának gyorsabb feldolgozása.** Egy motívum keresésekor a találati lista Strong-számokat ad; ha az adott könyvben már van Károli-Strong lefedettség, a Károli-szó azonosítása egyszerű grep-pé egyszerűsödik, nem igényel új tartalom-alapú mérlegelést minden egyes találatnál.

3. **A kumulatív modell (7.1-7.2 pont) határköltsége csökken.** Minél több Károli-Strong sor van már meglévő tanulmányokból, annál kevesebb új generálás kell egy jövőbeli tanulmánynál.

**Csak nagyobb lefedettségnél jelentkező haszon:**

4. **Fordított irányú keresés — magyar szó felől.** Elég nagy lefedettségnél ellenőrizhetővé válik, hogy a Károli egy adott magyar szava mindig ugyanazt a héber/görög Strong-számot fedi-e le, vagy több különböző fogalmat mos össze — ez pontosan az a fajta "elmosódás", amit a bővített sablon 2. kiválasztási kritériuma keres, de most objektív, adatalapú jelzést kapna, nem csak egyedi felismerést.

5. **Statisztikai mintázat-felismerés — jövőbeli, nem jelenleg tervezett lehetőség.** Nagy lefedettségnél elméletileg kereshetővé válna, mely Strong-számok fordulnak elő szokatlanul gyakran ugyanazzal a Károli-szóval — objektív jelzést adhatna olyan motívum-jelöltekre, amiket eddig csak kézi, tartalmi munka tárt fel.

### 4.15 A Strong-validáció nem végleges — mikor érdemes újraértékelni

A `Karoli_Strong_kivonat.tsv` "Megbízhatóság" oszlopa (4.13 pont) egy ADOTT IDŐPONTBAN érvényes, dokumentált állapotot rögzít — nem végleges, megkérdőjelezhetetlen tényt. A validáció eredménye időben VÁLTOZHAT, négy fő okból:

1. **KJV/ASV lefedettség bővülése.** Egy sor, ami jelenleg "közepes" megbízhatóságú (mert nincs KJV/ASV-adat arra a könyvre), automatikusan "magas"-ra frissülhet, amint a KJV/ASV-Strongs adat kiterjed az adott könyvre — anélkül, hogy bármi hibás lett volna korábban.

2. **Új tanulmányok új kontextust adhatnak egy korábbi, "bizonytalan" esethez.** Ha egy jövőbeli tanulmány részletesebben foglalkozik ugyanazzal a szógyökkel (pl. a már dokumentált H2895/H2896 vagy H1892/H1893 kettős lehetőségeknél), kideríthet valamit, ami eldönti, melyik Strong-szám a helyesebb az adott kontextusban — ez nem az adat változása, hanem az értelmezés pontosodása.

3. **A STEPBible-Data forrás maga is frissülhet.** Ha a TAHOT/TAGNT-et egy jövőbeli munkamenetben újra letöltjük, és eltér a jelenlegi `konkordancia/TAHOT_kivonat.tsv`-től, egy korábban "megerősített" sor "eltérés"-sé válhat — nem a mi hibánkból, hanem mert a forrás változott.

4. **A visszamenőleges ellenőrzések bővülésével** (mint az 1Móz 1-16 könnyű ellenőrzése) egyre több kontextusból gyűlik össze adat ugyanarra a szóra.

**Gyakorlati szabály:** minden újraértékelést — akár változás történt, akár nem — rögzíteni kell a `konkordancia/Validacios_naplo.md`-ben, dátummal. Egy "nincs változás" eredmény is dokumentálandó, mert ez maga is informatív (megerősíti, hogy az adott sor stabil maradt egy újabb ellenőrzési kör után is).

**Mikor érdemes újraértékelési kört indítani** (nem minden apró változásnál, hanem ezeknél a mérföldköveknél):
- Amikor a KJV/ASV lefedettség egy új könyvre bővül (akkor érdemes újranézni az adott könyv korábban "közepes" jelölésű sorait)
- Amikor egy tematikus vagy mélyelemzés tanulmány érdemben érinti egy korábban "bizonytalan" jelölésű szó szógyökét
- Nagyobb, tudatos STEPBible-forrás-frissítés esetén (nem minden alkalommal, csak ha ténylegesen újra letöltjük a nyers adatot)

