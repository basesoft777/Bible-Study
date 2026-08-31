Bibliai Motívumlexikon — tervezési napló
Rögzítve: 2026.08.30. Státusz: KONCEPCIONÁLIS FÁZIS, folytatásra vár — nincs jóváhagyott végleges architektúra, nincs megkezdett implementáció. Ez a fájl a tervezés jelenlegi állását naplózza, nem döntést rögzít.
1. Előzmény

* 2026.08.30 korábban: a chat-felület (Claude Sonnet 5) javaslatot tett egy szűk, azonnal megvalósítható motívum-azonosító sémára (ld. `Motivum_azonosito_sema_javaslat.md` és a `Claude_Code_prompt_motivum_azonosito_sema_bevezetese.md`), ami a `PaRDeS_motivumok.md` `###` bejegyzéseit látja el stabil, kategórián belüli sorszámmal (pl. `HAMART-009`).
* Ugyanazon a napon Basesoft feltöltötte a `Bibliai_Motivumlexikon_reszletes_tervezesi_javaslat.md` dokumentumot — egy jelentősen tágabb, réteges rendszer-architektúra víziót, amibe a fenti azonosító-séma csak egy építőelem.

2. Basesoft koncepciójának összefoglalása (a feltöltött dokumentum alapján)
Alapelv: a rendszer központi egysége nem a Strong-szám és nem a lexéma önmagában, hanem a motívumhoz kapcsolt igehely/igeszakasz.
Rétegzett modell:

```
SZÖVEG → KONKORDANCIA → LEXIKON → MOTÍVUM → KAPCSOLAT → TANULMÁNY (→ PaRDeS)

```

Fő elemek:

* IGEHELY szint: lexikai adatok (szóalak, lemma, gyök, morfológia, Strong) + a hozzá kapcsolódó motívum-előfordulások + konkordancia (további előfordulások).
* MOTÍVUM szint: egy motívumhoz több előfordulás tartozhat; egy vershez több motívum is kapcsolódhat; a motívumnak lehet formula-mezője (rögzített eredeti nyelvi kifejezés, pl. `קָרָא בְשֵׁם יְהוָה`).
* KAPCSOLAT szint: KÉT KONKRÉT ELŐFORDULÁS közötti, típusos reláció, 4 dimenzióval: Típus (pl. TEMATIKUS/NARRATÍV), Funkció (pl. ISMÉTLÉS/VISSZATÉRÉS, ÖRÖKLÉS/MINTAÁTVÉTEL), Bizonyosság, PaRDeS (melyik rétegben értelmezhető a kapcsolat).
* Kapcsolódó fogalmak, egyelőre vázlatosan: "használva volt", előkép és beteljesedés, párhuzam, újrahasználás, öröklés, motívum életciklusa, kánoni ív (pl. Jóel → ApCsel → Róma).
* TANULMÁNY szint: tanítói hangok, forráskritika, jegyzetek — ez a meglévő PaRDeS-módszertan illesztési pontja.
* Felhasználói felület vízió: navigáció 📖 Igeszakaszok / 🔤 Lexikon / 🔎 Konkordancia / 🧩 Motívumok / 🔗 Kapcsolatok / 📚 Tanulmányok / ✡ PaRDeS / 📝 Saját jegyzetek; igeszakasz-lap és motívum-lap konkrét vázlata.
* Javasolt fejlesztési sorrend (a dokumentum 31. pontja): szövegalap → konkordancia → lexikai réteg → motívumréteg → kapcsolati réteg → tanulmányi réteg → PaRDeS.

Konkrét példa a dokumentumban: a már lezárt "Segítségül hívni az Úr nevét" tematikus tanulmány (1Móz 4:26, 12:8, 13:4, 21:33, 26:25), a kapcsolatok és a kánoni ív bemutatására.
A dokumentum jelenlegi állapota: a 32 szakaszból kb. 15 még csak egyetlen betűs vázlat (3., 4., 5., 6., 8-14., 16-22., 27., 29. pont) — tehát ez egy induló koncepció-váz, nem kész terv.
3. A chat-felület összevetése — hol egyezik, hol tér el
Egyezés: a motívum mint önálló, azonosítható entitás gondolata közös. A korábban javasolt `HAMART-009`-szerű azonosító-séma természetes módon szolgálhatna a "MOTÍVUM" csomópont elsődleges kulcsaként ebben a tágabb modellben — nincs elvi ütközés, az azonosító-séma belefér a nagyobb architektúrába, mint annak egy rétege.
Amiben a Basesoft-koncepció bővebb, mint a korábbi (szűkebb) javaslat:

1. Típusos KAPCSOLATOK réteg — két konkrét előfordulás közötti reláció, 4 dimenzióval. Ez explicit strukturált adatot igényel, nem csak szabad szöveges "Lásd még" hivatkozást (ami a jelenlegi motívumnaplóban van).
2. Formula-mező — önálló mezőként rögzített eredeti nyelvi kifejezés, elkülönítve a Strong-számoktól.
3. Motívum életciklus, öröklés, előkép/beteljesedés, kánoni ív — a KAPCSOLAT-réteg finomításai, egyelőre kidolgozatlan tartalommal.
4. UI/navigációs vízió — ez korábban egyáltalán nem szerepelt.

4. Nyitott kérdések, mielőtt a tervezés folytatódik

1. A ~15 vázlatos szakasz tartalommal töltése — melyiket töltsük ki először, van-e köztük olyan, ami blokkolja a többit?
2. Formátum/eszköztár kérdés: a KAPCSOLATOK réteg (két-igehelyes, típusos reláció) nem fér el egy szabad szöveges markdown-naplóban — gyakorlatilag egy önálló, relációs adatfájlt igényelne (pl. `Motivum_kapcsolatok.tsv`, kb. `Forrás-igehely | Cél-igehely | Motívum-ID | Típus | Funkció | Bizonyosság | PaRDeS-szint` oszlopokkal). Ez már közelebb áll egy kis adatbázishoz, mint a jelenlegi markdown+TSV+git-alapú struktúrához — tudatos döntést igényel, hogy ez a lépték szándékos-e.
3. Pilot-javaslat (a chat-felülettől, egyelőre csak feljegyezve, NEM elindítva): mielőtt a teljes réteges modellt megterveznénk, érdemes lehet a KAPCSOLATOK-réteget egyetlen, már lezárt motívumon kipróbálni — pont a dokumentum saját példáján, a "Segítségül hívni az Úr nevét" tanulmányon, aminek van 5 rögzített előfordulása és a kapcsolatok jó része már szöveges formában megvan a `Segitsegul_hivni_az_Urat_tematikus.md`-ben.
4. Viszony a korábban elfogadott, szűkebb motívum-azonosító sémához: az a séma változtatás nélkül beépíthető-e ebbe a nagyobb modellbe, vagy a nagyobb terv fényében érdemes újragondolni, mielőtt az 1Móz 17-es teszt-kör elindulna?

5. Kapcsolódás a Strong-szótár tervezett BDB-bővítéséhez (2026.08.30,

```
utólagos kiegészítés)

```

A Motívumlexikon-modell megemeli a `Strong_szotar.tsv` tervezett BDB jelentéstartomány-bővítésének (ld. `Motivum_azonosito_sema_javaslat.md` 5.b szakasza) tétjét — ez nem csak önmagában hasznos gazdagítás, hanem a nagyobb architektúra egyik rétegének előfeltétele lesz:

1. A "LEXIKON" a modellben önálló réteg (4. szakasz "A Strong szerepe" alpontja), ami az IGEHELY szinthez (lexikai adatok) ÉS a MOTÍVUM szinthez (formula/lexikai alap) is kapcsolódik — vagyis a `Strong_szotar.tsv` + a tervezett BDB-bővítés gyakorlatilag ez a réteg lesz, nem mellékes kiegészítő adat.
2. A MOTÍVUM-formula pontossága a jelentés-ág szintjén dőlhet el. Ha egy motívum lexikai alapja nem csak "ez a Strong-szám", hanem "ez a Strong-szám, ebben a konkrét jelentés-ágban", akkor a KAPCSOLAT-réteg Típus-mezője (lexikai vs. tematikus kapcsolat) is ettől függhet — ez pontosan az a distinkció, amit a projekt már most is következetesen megkövetel ("lexikai vs. tematikus, sosem keverve"), a BDB sense-szint ennek egy finomabb, géppel is ellenőrizhető alapja lenne.
3. A korábban javasolt "Lexikai kulcs" mező (`H0001.8` formátum) a motívum-séma javaslatban eddig csak "opcionális, jövőbeli bővítés" volt — a Motívumlexikon-terv fényében ez load-bearing elemmé válhat, ha a KAPCSOLAT-réteget valaha megépítjük.

Megerősítő észrevétel: a Motívumlexikon-doksi tudatosan szétválasztja a KONKORDANCIA ("hol van a szövegben") és a LEXIKON ("mi a nyelvi egység") kérdését — a projekt jelenlegi fájlfelosztása (`TAHOT_kivonat.tsv` = előfordulás-szintű konkordancia, `Strong_szotar.tsv` = szó-szintű lexikon) már most pontosan ezt a felosztást követi. Ez jelzi, hogy az eddigi adatarchitektúra jó irányba állt, nem szükséges újratervezni.
Gyakorlati következmény: a jövőbeli BDB-munka (`Strong_szotar_BDB_ jelentestartomanyok.tsv` oszlop-terve) érdemes eleve úgy kialakítani, hogy egy jövőbeli motívum-formula vagy motívum-előfordulás tisztán tudjon rá hivatkozni (Strong-szám + BDB-entry-id + Sense-szám hármas kulcsként) — ez nem változtatja meg a korábban vázolt tervet, csak megerősíti az irányt.
6. Kockázat-elemzés: a BDB-bővítés időzítése a Motívumlexikon-tervezéshez

```
képest (2026.08.30, Basesoft felvetése alapján)

```

A kérdés: milyen későbbi problémával járhat, ha a Strong-szótár BDB jelentéstartomány-bővítése megtörténik, MIELŐTT a Motívumlexikon lexikai adatstruktúrája ténylegesen meg lenne tervezve?
Kockázatok, ha a BDB-munka most, korán indul:

1. Kulcs-formátum korai lezárása, migrációt igényelhet. Ha most eldől, hogy a jelentés-ág hivatkozás formátuma `H0001.8` (Strong + sense-szám), de a Motívumlexikon KAPCSOLAT-rétege kiderül, hogy másra van szüksége (pl. globálisan egyedi sense-azonosító, más particionálás), akkor utólag át kell dolgozni minden már felvett hivatkozást.
2. Kétszintű hierarchia (BDB-bejegyzés a/b/c + sense-szám 1-9) elveszhet, ha csak az egyik szintet rögzítjük. Egy Strong-számhoz több BDB-bejegyzés (homonima) is tartozhat; ha a mostani munka csak a sense-számra fókuszál és nem kezeli explicit az a/b/c szintet is, egy homonima-eset hibásan összemosódhat — ez pontosan az a fajta hiba, amit a projekt eddig következetesen elkerült (lexikai/tematikus fegyelmi elv).
3. Terjedelem: ~8700 héber Strong-szám, soronként átlag 3-9 sense — könnyire 20-30 ezer sornyi adat. Ha ez korai, ad hoc struktúrában készül el, és a Motívumlexikon-tervezés később máshogy particionálná/ indexelné (normalizált vs. denormalizált forma), jelentős újramunkálást jelenthet.

Fordított kockázat, ha megvárjuk a teljes Motívumlexikon-tervet: a Motívumlexikon-doksi jelenleg 15+ üres szakasszal áll (ld. 2. szakasz) — ha megvárnánk, amíg teljesen kész, az akár évekig húzódhat, miközben a BDB-bővítés önmagában is hasznos lenne (gazdagabb "Lexikai adatok" a jelenlegi PaRDeS-tanulmányokban), függetlenül attól, hogy a Motívumlexikon valaha megépül-e.
Javasolt kiegyensúlyozás — "reversibilis tervezés" (a projekt saját "kis minta, explicit megállási szabály" elve szerint): ha mégis belevágunk a BDB-munkába a nagy architektúra előtt, a kulcs-struktúrát eleve úgy alakítsuk ki, hogy semmi ne vesszen el visszamenőleg — már a mintavételi körben is mindhárom szintet külön oszlopban rögzítjük (`Strong-szám | BDB-entry-id | Sense-szám | Jelentés-szöveg`), még akkor is, ha a motívum-séma egyelőre csak a Strong-szint hivatkozást használja. A nyers adat így gazdag marad, a Motívumlexikon bármikor eldöntheti később, hogyan particionálja/indexelje — nem kell újra letölteni/ feldolgozni, csak átalakítani.
Döntés: egyelőre nem született — ez a szakasz a kockázat-elemzést rögzíti, a folytatás (BDB-munka most, "reversibilis" struktúrával, vagy várjon a Motívumlexikon-architektúra érésére) Basesoft külön kezdeményezésére dől el.
8. Pontosítás és konkrét javaslat: a BDB jelentéstartomány szerepe (2026.08.30, Basesoft pontosítása alapján)
Basesoft pontosítása: a BDB jelentés-ágak (sense n="1".."9") nem alternatív fordítási lehetőségek egy adott előfordulásra, amik közül választani kellene — hanem egy szó jelentés-mélységének/konnotációjának leírása, ami tipikusan rárétegeződik, nem kizárja egymást. Ez élesebbé teszi (és részben átírja) a 6-7. szakaszban vázolt kockázat-elemzést: a probléma nem csak technikai adathiány (nincs sense-cimkézett korpusz), hanem hogy a "melyik sense aktív egy adott versben" kérdésnek gyakran nincs egyetlen helyes válasza — ez interpretív mérlegelés, ami a Peshat/Remez/ Drash rétegekbe való, nem egy mechanikus előszűrőbe.
Konkrét javaslat (4 pont):

1. A bővített sablon 6. kritériuma (objektív ritkaság, `2_PaRDeS_bovitett_sablon.md` 71. sor) maradjon változatlanul, tisztán Strong-szám szintű. A BDB-adat ide NE épüljön be, sem közvetlenül, sem közvetve — ez a mechanikus előszűrés pontosan azért működik jól, mert nem igényel értelmezést.
2. A BDB jelentéstartomány helye: a már kiválasztott szó Peshat/Drash kifejtésében, forrásmegjelöléssel — gazdagító anyagként, nem szűrőként. Ugyanolyan fegyelemmel idézve, mint egy nevesített tanító (explicit forrásmegjelöléssel, nem összemosva az "objektív adat" réteggel).
3. A `Motivum_azonosito_sema_javaslat.md` 3.3 pontjában korábban felvetett sense-szintű "Lexikai kulcs" formátum (`H0001.8`) felülvizsgálandó. Ha egy motívum lexikai alapja egy szó jelentés-mélysége (nem egy elkülönült, kiválasztható jelentés), egyetlen sense-számra mutatás hamisan sugallná, hogy a motívum csak arra az egy ágra korlátozódik. A "Lexikai kulcs" mező maradjon Strong-szám szinten, a sense-szintű finomítás csak szabad szöveges kiegészítésként jelenjen meg a motívum leírásában, ha releváns.
4. Gyakorlati következmény a jövőbeli BDB-munkára: a `Strong_szotar_BDB_jelentestartomanyok.tsv` tisztán referencia-adatként kezelendő — forrás, amit a tanulmányírás közben idézünk, nem struktúra, amibe automatikusan besorolunk egy-egy előfordulást. Ez lényegesen egyszerűbb cél, mint a korábban feltételezett "melyik sense aktív itt" egyértelműsítési probléma megoldása — és jól illeszkedik a projekt már bevált mintájához (lexikonok/tanítók idézése forrásjelöléssel).

Döntés: a 4 pont Basesoft jóváhagyásával rögzítve (2026.08.30) — ez már konkrét irányadó elv a jövőbeli BDB-munkához és a motívum-séma esetleges módosításához, de maga a BDB-implementáció továbbra sem indult el.
9. Fordítási elv: BDB jelentéstartomány magyarra fordítása (2026.08.30,

```
Basesoft felvetése alapján)

```

A kérdés: a BDB jelentéstartomány-leírások angolul vannak — a tanulmányokban/naplóban magyarul szükségesek. Előre lefordítsuk-e a teljes adatbázist, és egy magyar változatot tároljunk?
Javaslat: NE fordítsuk le előre. Indoklás:

1. Ugyanaz a hiba lenne, amitől a `Karoli_Strong_kivonat.tsv` gyakorlata már óv — az a fájl (178→213 sor) tudatosan tanulmány-vezérelt, fokozatos építésű, nem előre, a teljes Bibliára legenerált. A BDB ~8700 tétele (soronként átlag 3-9 sense, azaz 20-30 ezer egység) előre lefordítva pont az ellenkező elvet valósítaná meg.
2. A fordítás minősége kontextustól függ. Egy tömör angol sense-definíció pontos magyar megfogalmazása exegetikai döntés is lehet, nem tisztán gépi fordítási feladat — kontextus nélkül előre fordítva vagy túl általános lenne, vagy csendben bevinne egy nem minden felhasználásra illő értelmezési irányt.
3. Összhangban van a 8. szakasz döntésével: a BDB-adat referencia- anyagként, forrásmegjelöléssel idézve szerepel a tanulmányokban, nem strukturált, automatikusan beépülő mezőként — a fordítás a study-írás pillanatában, a konkrét igehely kontextusában készül, ez pont ezt az elvet valósítja meg.

Konkrét mechanizmus — fokozatos, gyorsítótárazott fordítás:

* Amikor egy tanulmány ténylegesen idéz egy BDB sense-t, a fordítás ott, a study szövegében készül el, forrásmegjelöléssel.
* Emellett egy kumulatívan bővülő fájl (javasolt: `konkordancia/Strong_szotar_BDB_forditasi_gyorsitotar.tsv`, oszlopok: `Strong-szám | BDB-entry-id | Sense-szám | Angol eredeti | Magyar fordítás | Első felhasznált tanulmány`) visszakapja minden lefordított sense-t — egy későbbi tanulmány, ami ugyanazt a sense-t idézi, nem fordít újra, hanem a meglévő, konzisztens magyar megfogalmazást használja (kivéve, ha a kontextus indokolt finomítást kíván — ez explicit döntés marad, nem automatikus).
* Ez a `Join_tabla_folyamat_magyarazat.md`-ben már leírt "kumulatív alapelv" mintáját követi ("minden generált sor visszakerül a privát join-táblába, így egy következő tanulmány... már nem generál újra semmit"), fordításra alkalmazva.

Döntés: Basesoft jóváhagyta (2026.08.30) — ez irányadó elv a jövőbeli BDB-munkához, de maga az implementáció továbbra sem indult el.
11. Navigációs ív: igehely-központú belépés a motívumhoz és a lexikai

```
adatlaphoz (2026.08.30, Basesoft kiegészítése alapján)

```

Basesoft kiegészítése: a végleges rendszerben a felhasználó a Károli- szöveget olvassa (igehely-központú belépés), és onnan indul kifelé — a motívum csak egy rövid, azonnal látható "címke" a vers mellett, amiről tovább lehet lépni a teljes motívum-tanulmányra. Ez ugyanaz a mintázat, amit a jelenlegi `PaRDeS_motivumok.md` már részben megvalósít, csak fordított irányban (motívum → igehely, a "Könyv szerinti index" szakaszban) — a végleges rendszernek igehely → motívum irányban is működnie kell, ugyanabból az adatból, más elsődleges kulccsal.
Teljes navigációs ív: Igehely (Károli-szöveg) → rövid motívum-címke a vers mellett → motívum-oldal (teljes leírás) → a motívum lexikai alapjának Strong/BDB-szótárszerű adatlapja, a motívum-oldalon megjelenítve.
Új mező-igény, amit ez felvet: a motívum-azonosító séma eddig két szintet definiált (ID, pl. `HAMART-009`; teljes leíró cím). Egy vershez csatolva a teljes cím túl hosszú lenne egy UI-címkéhez — szükség lehet egy harmadik, nagyon rövid mezőre (kb. 2-4 szó, pl. csak "Kánaán-átok" a teljes indoklás nélkül). Javasolt: `Rövid UI-címke` mező hozzáadása a sémához, amit már az új motívumok felvételekor érdemes kitölteni, hogy ne kelljen később visszamenőleg mind a 33+ motívumot újranézni.
A "Lexikai kulcs" mező funkcionális igazolása: a korábban (3.3 pont, `Motivum_azonosito_sema_javaslat.md`) megtervezett, Strong-szám szintű "Lexikai kulcs" mező eddig elsősorban belső rendteremtésnek tűnt — most világos, hogy ez lesz a tényleges kapcsolókulcs, ami a motívum-oldalon megjeleníti a hozzá tartozó szótári bejegyzést. A `Strong_szotar.tsv` + a tervezett BDB-bővítés így kettős szerepet kap: (a) igehely-szinten, a "LEXIKAI ADATOK" ágban (szóalak, lemma, gyök, morfológia, Strong) — minden előfordulásra vonatkozó, konkordancia-szintű adat; (b) motívum-szinten, a motívum lexikai alapjának egyetlen, reprezentatív BDB-bejegyzéseként — nem minden előfordulás adata, hanem a motívum "törzsszavának" teljes szótári bejegyzése. A két megjelenés más adatból táplálkozik (előbbi a `TAHOT_kivonat.tsv`-ből versenként, utóbbi a `Strong_szotar.tsv`+BDB-ből motívumonként), de ugyanarra a forrásra mutat — nincs duplikáció, csak két belépési pont ugyanahhoz az adathoz.
12. Minőségi megkötés: a motívumnapló önmagában is értelmezhető marad,

```
nyomtatható formában is (2026.08.30, Basesoft kiegészítése alapján)

```

Basesoft megkötése: bármilyen adatbázis-/relációs struktúra is épül fel a Motívumlexikonból, a motívumnaplónak önmagában is, kattintás/ adatbázis-lekérdezés nélkül, mint egy hagyományos bibliai fogalomtár olvashatónak kell maradnia — akár nyomtatható változatban is.
Konkrét következmények:

1. A motívum-oldal nem támaszkodhat kizárólag hivatkozásokra (pl. "ld. Igehely X lexikai adatai") — a szöveges leírásnak önmagában is elegendőnek kell lennie a megértéshez, a lexikai adatlap és az igehely-kapcsolat csak kiegészítés. Ez már most is így működik a `PaRDeS_motivumok.md` "Kulcsszavak részletesen" szakaszában — nem új teher, hanem egy bevált gyakorlat megerősítése és rögzítése tervezési elvként, mielőtt bármilyen adatbázis-formára váltanánk.
2. "Nyomtatható változat" — explicit exportálhatósági követelmény: a végső rendszernek tudnia kell egy tiszta, formázott, lapozható dokumentumot (mint egy hagyományos konkordancia/fogalomtár) visszaállítani, akkor is, ha az alapadat relációs struktúrában (KAPCSOLATOK-tábla, motívum-adatbázis) tárolódik. A projekt már rendelkezik docx/pdf- generálási képességgel, tehát technikailag nem akadály, de tervezéskor figyelembe veendő: a mezők úgy alakuljanak ki, hogy egy tiszta, nyomtatható lista (ábécé- vagy kategória-rendezett) mechanikusan előállítható legyen belőlük.
3. A meglévő kétszintű felépítés (tömör Kulcsszó-index + bővebb Kulcsszavak részletesen szakasz) pontosan illeszkedik ehhez az elvhez — ez most explicit tervezési szabállyá válik, nem csak véletlenül kialakult formátum marad.

Döntés: mindkét szakasz (11-12.) Basesoft jóváhagyásával rögzítve (2026.08.30) — irányadó elvek a jövőbeli Motívumlexikon-architektúrához, implementáció még nem indult el.
## 14. Prompt Caching / import-architektúra dokumentum feldolgozása
    (2026.08.31, Basesoft által megosztott anyag alapján)

**A megosztott dokumentum tartalma:** gyakorlati javaslat a Strong–BDB–TWOT
import AI-alapú feldolgozásának költséghatékony megszervezésére —
Anthropic API prompt-caching technika (állandó szabály/séma/példa-blokk
cache-elve, csak a szófüggő rész megy "élesben" minden híváskor), valamint
egy architektúra-javaslat: nyers XML → Python-parser (ElementTree/lxml) →
SQLite/JSONL tartós tárolás → AI csak a ténylegesen értelmezést igénylő
részekre (fordítás, OCR-javítás, teológiai magyarázat ellenőrzése).

**A chat-felület (Claude Sonnet 5) értékelése:**

1. **Egyetértés a réteg-szétválasztással**: a Strong↔BDB↔TWOT-szám
   összerendelés determinisztikus adatkapcsolás, nem AI-feladat — ez
   illeszkedik ahhoz, amit korábban (SQLite-demonstráció) is megmutattunk.
2. **Ütközés jelezve, de NEM eldöntve**: a dokumentum a BDB-fordítást
   tömeges, előre elvégzett kampányként veszi alapul (H1-H8674, cache-
   optimalizálva) — ez szemben áll a 9. szakaszban rögzített döntéssel
   (fordítás tanulmány-vezérelt, fokozatos, nem előre tömeges). Javasolt
   feloldás (MÉG NEM ELDÖNTÖTT): a strukturális import (angol nyersadat
   SQLite-ba, AI nélkül, tisztán parserrel) elválasztható a fordítás
   ütemezésétől — az import mehetne tömegesen, a fordítás maradna a 9.
   szakasz szerinti fokozatos módban, a cache-technikát csak az egyedi,
   on-demand fordítási hívásokon alkalmazva (közös szabályblokk cache-elve,
   akkor is, ha nem tömeges kampányban történik).
3. **TWOT-forrás — licenc-kérdés jelezve, Basesoft pontosítása alapján
   RÉSZBEN FELOLDVA**: a dokumentum egy "TWOT OCR-forrásra" hivatkozik,
   ami — ha a teljes TWOT-szöveget jelentené — védett, 1980-as kiadású mű,
   nem közkincs, mint a BDB. **Basesoft pontosítása**: a tervezett
   felhasználás **kizárólag a TWOT-hivatkozási SZÁM** megjelenítése a
   lexikonban (pl. "4a"), NEM a TWOT-szöveg maga. A TWOT-szám már most is
   elérhető, jogtiszta forrásból — az `openscriptures/HebrewLexicon`
   `LexicalIndex.xml`-je tartalmazza, saját dokumentációja szerint
   *"TWOT numbers are included for reference purposes only... in no way
   directly transcribing the Theological Wordbook"*. Emiatt a TWOT-szám
   megjelenítése **nem igényel új forrás/licenc-ellenőrzést** — a
   TWOT-szöveg (OCR-forrás) bevonása viszont továbbra is tisztázandó
   kérdés marad, ha valaha felmerülne.

**Döntés:** egyelőre semmi nincs eldöntve — ez a szakasz a dokumentum
tartalmát, az értékelést és a TWOT-szám/TWOT-szöveg megkülönböztetést
rögzíti, a korábbi szakaszokhoz hasonlóan tervezési feljegyzésként.

## 15. Következő lépés
Egyelőre nincs — ez a fájl kizárólag a terv jelenlegi állását rögzíti. A folytatás (melyik nyitott kérdéssel induljunk) Basesoft külön kezdeményezésére történik.
