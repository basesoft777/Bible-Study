Bibliai Motívumlexikon — tervezési napló
Rögzítve: 2026.08.30, utolsó frissítés: 2026.09.09. Státusz: KONCEPCIONÁLIS FÁZIS — a végleges architektúra egésze továbbra sem jóváhagyott, implementáció nem indult, de a KAPCSOLATOK réteg Típus-mezőjének öt kategóriás (Előkép/Párhuzam/Beteljesedés/Kontraszt/Variáns) v1 értékkészlete 2026.09.09-én jóváhagyott részdöntés (ld. 6. pont). Ez a fájl a tervezés jelenlegi állását naplózza, a fenti egy ponton kívül nem rögzít végleges döntést.
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

5. **Séma-korlát — versen belüli kontraszt** *(felvetve: 2026.09.09, forrás: `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` NAPLO-jegyzete, 1Kir 18:24 eset)*: a jelenlegi KAPCSOLATOK-formátum (Forrás-igehely | Cél-igehely) két *különböző* igehelyet feltételez. Az 1Kir 18:24 (Illés a Kármelen — YHVH neve vs. a nép istenének neve, ugyanazon a versen belül szembeállítva) ezt nem tudja natívan ábrázolni; jelenleg csak prózai megjegyzésként létezik a study-ban, nem KAPCSOLAT-sorként. Nyitott kérdés: kell-e egy új mező/reláció-típus az intra-verse kontraszthoz, vagy marad prózai kivétel?
6. **A/B/C tipológia — önálló reláció-típus vagy lexikai lábjegyzet?** *(felvetve: 2026.09.09, forrás: `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, 2. pont)*: a קָרָא+שֵׁם szerkezet három szisztematikusan variálódó alany/tárgy-mintázatot mutat — **A** (ember hívja Isten nevét — a fő motívum), **B** (Isten kihirdeti saját nevét, 2Móz 33:19/34:5), **C** (Isten nevez meg egy embert, Ézs 43:1/44:5/45:3, korábban a motívumhoz nem tartozóként elutasítva). Ez lexikai szintű megfigyelés, NEM állítja, hogy A/B/C motívum-szinten összetartozna. ✅ DÖNTÉS: l. alább.

**✅ DÖNTÉS (2026.09.09) — a KAPCSOLATOK Típus-mező öt kategóriája, lezárja az 5. és 6. pontot:**

A felhasználó saját tapasztalata szerint az eredeti előkép/párhuzam/beteljesedés hármas jól működött a tényleges PaRDeS-munkában, a tervezési napló 2. pontjában vázolt elvontabb TEMATIKUS/NARRATÍV-mátrix nem. A Típus-mező induló (v1) értékkészlete ezért öt kategóriából áll, a meglévő három megtartásával és két, a mai konkrét esetekből szükségessé vált új kategóriával:

| Típus | Definíció | Elhatároló teszt |
|---|---|---|
| **Előkép** | korábbi esemény/alak, ami egy későbbi, teljesebb valóság mintája | idői irány kötelező: korábbi → későbbi |
| **Párhuzam** | ismétlődő mintázat, a szereplők szerepe azonos marad | ismétlődik-e ugyanaz a szereposztás? |
| **Beteljesedés** | egy előkép lezárása/valóra válása | mindig egy Előkép-jelöléshez kapcsolódik, önmagában nem áll |
| **Kontraszt** *(ÚJ)* | két fél szándékosan szembeállítva, a lényeg az eltérés | ha a két felet felcserélnéd, a mondanivaló megfordulna-e? (igen → Kontraszt) |
| **Variáns** *(ÚJ)* | ugyanaz a lexikai/formula-mag, de a szereplők szerepe szisztematikusan felcserélődik, nem szembeállítva | ugyanaz a szó/szerkezet, más az alany-tárgy, és ez a csere hordoz jelentést |

Konkrét besorolás a két nyitott esetre: az **1Kir 18:24** (5. pont) a **Kontraszt** kategóriába kerül; az **A/B/C tipológia** (6. pont) a **Variáns** kategóriába. A tervezési napló eredeti TEMATIKUS/NARRATÍV + ISMÉTLÉS/VISSZATÉRÉS/ÖRÖKLÉS-mátrixa (2. pont) ezzel elavulttá vált, tudatosan nem került átvételre. Nyitva marad: a Funkció, Bizonyosság és PaRDeS-szint mezők tartalma, valamint a Motívum-kapcsolatok.tsv tényleges felépítése — ez a döntés csak a Típus-mezőt zárja le.

7. Kapcsolódás a Strong-szótár tervezett BDB-bővítéséhez (2026.08.30,

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

## 15. Döntés: a lexikon-TSV-k lapos, teljes-szöveges struktúrája (2026.09.07)

**Kiegészítés a 6-8. pontokhoz és a `konkordancia/Uj_lexikon_fajlok_2026-09-07.md`-hez.** Rögzítve egy chat-alapú beszélgetés (Claude Sonnet 5, chat-felület) végkövetkeztetéseként, a Motívumlexikon-pilot (ISTENTISZT-001) elemzése nyomán.

**A kérdés, amit ez a jegyzet lezár:** a 7. pont ("reverzibilis tervezés" elve) egy granulált, hármas kulcsú struktúrát javasolt a jövőbeli BDB-bővítéshez:

```
Strong-szám | BDB-entry-id | Sense-szám | Jelentés-szöveg
```

Ezzel szemben a ma (PR #53) ténylegesen elkészült 5 lexikon-TSV (`Thayer_teljes.tsv`, `LSJ_teljes.tsv`, `SECE_H_teljes.tsv`, `SECE_G_teljes.tsv`, `BDB_teljes_unabridged.tsv`) lapos, 3 oszlopos szerkezetű:

```
Strong_padded | Strong_eredeti | Teljes_szocikk
```

A `Teljes_szocikk` egyetlen, tagolatlan szövegblokk — a szótári sense-bontás (pl. BDB a/b/c + 1-9, vagy Thayer 1-5) csak a nyers szövegben van benne, nem külön mezőben.

Ez a jegyzet rögzíti: ez tudatos, végleges formai döntés — nem elmaradt, javítandó granulálás.

**Az indoklás:**

1. **A tényleges munkamód nem mezőnkénti lekérdezés, hanem kereszt-olvasás.** A Motívumlexikon-pilot (`ISTENTISZT-001_TUDOMANYOS.md`, 4. szakasz) konkrét példát adott erre: a G1941 (ἐπικαλέω) szócikknél a BDB, a TBESG (Abbott-Smith) és a Thayer szövege egymás mellé kerülve hozott egy önálló felismerést — a Thayer explicit szétválasztja a "Hebraistically" (5.) sense-t az általános "invokálni" (4.) sense-től, ami három egymástól független forrásból megerősítette a motívum lexikográfiai alapját. Ez a felismerés a teljes, kontextusban hagyott szövegből jött — a "Hebraistically" jelző, a Gesenius-hivatkozás és a zsoltár-párhuzamok együtt adták az értelmezés anyagát. Ha a struktúra eleve granulált, elkülönített sense-mezőkre bontva tárolta volna ezt, pont ez a szövegkörnyezet veszett volna el.
2. **Összhangban a 8. ponttal.** A 8. pont (Basesoft pontosítása, 2026.08.30) már korábban kimondta: a BDB sense-ek nem egymást kizáró választási lehetőségek, hanem rárétegződő jelentés-mélységek, és hogy "melyik sense aktív egy adott versben" interpretív mérlegelés, nem mechanikus előszűrés kérdése. A döntés szerint a BDB-adat referencia-anyag marad, forrásmegjelöléssel idézve — nem strukturált szűrő. A lapos struktúra ennek a döntésnek a közvetlen, következetes folytatása: ha a sense-ek úgyis interpretív mérlegeléssel, forrásidézetként kerülnek egy tanulmányba (mint egy nevesített tanító idézése), egy granulált adatbázis felesleges plusz-réteg lenne.
3. **A módszertani fegyelem, nem a formátum, az elsődleges tényező.** A fenti felismerést nem a lapos formátum önmagában generálta, hanem a már kiforrott study-módszertan (négyforrásos kereszt-ellenőrzés, "lexikai vs. tematikus, sosem keverve" önellenőrzés, nevesített forrás-idézés fegyelme), ami a `Segitsegul_hivni_az_Urat_tematikus.md` és a `PaRDeS_gyorsreferencia.md`-ben rögzült. A lapos formátum szükséges feltétel volt (megőrizte a kontextust), a study-fegyelem másik szükséges feltétel volt (értelmezni tudta azt) — a kettő együtt volt elégséges az eredményhez. Gyakorlati következmény: ha a lexikon-adatstruktúra fejlesztése valaha elszakadna az élő study-munkától (pl. a TSV-k bővülnének tematikus/bővített study nélkül), ez a fajta eredmény valószínűleg nem reprodukálódna — a formátum jósága a módszertantól függ, nem önmagában áll.

**Mikor kellene felülvizsgálni:** ha a jövőben a Motívumlexikon KAPCSOLAT-rétege (11. pont, "Lexikai kulcs" mező) ténylegesen gépi, sense-szintű hivatkozást igényelne (nem csak interpretív idézést egy tanulmány szövegében), a granulálás kérdését újra elő kell venni. Eddig erre nem történt konkrét igény.

Forrás: chat-alapú beszélgetés, 2026.09.07, a Motívumlexikon-pilot (ISTENTISZT-001) és a mai lexikon-TSV-k (PR #53) elemzése alapján.

## 16. Következő lépés
Egyelőre nincs — ez a fájl kizárólag a terv jelenlegi állását rögzíti. A folytatás (melyik nyitott kérdéssel induljunk) Basesoft külön kezdeményezésére történik.

## 17. Károliba épített kereszthivatkozás — megjelenítési ötletelés (2026.09.09, NEM döntés)

**Kiindulás:** a mai beszélgetés során felmerült, hogy a motívum-alapú
kereszthivatkozási réteg (l. "Publikálási terv" nyitott pont,
`NYITOTT_FELADATOK.md` 2. tétel) nem áll meg egy puszta adatrétegnél
("igehely → motívum-ID"), hanem a felhasználó a **teljes lexikon-cikket
és a kapcsolati hálót** akarja elérhetővé tenni minden egyes
előfordulási igehelyről — nem csak egy reprezentatív belépési pontról.

**Ez a szakasz kizárólag a MEGJELENÍTÉS kérdését rögzíti, ötletelés
szinten, döntés nélkül:**

**1. Inline jelölés a versen — három felmerült minta:**
- Egyetlen, semleges jel (pl. 🔗) a vers végén — egyszerű, de nem
  mutatja a típust.
- Típusonként eltérő ikon/szín (l. az 5 kategóriás Típus-mező, ha az
  már rögzítve van a fájlban) — informatívabb, de több kapcsolatnál
  egy versen zsúfolttá válhat.
- Egységes jel + szám (hagyományos referencia-Biblia mintája, pl.
  "¹", "²"), a szám egy lábjegyzet-listára mutat — a legjobban
  skálázódó opció több kapcsolat esetén.

**2. Interakció a jelölésen — három felmerült minta:**
- Popup/tooltip: cél-igehely + típus + rövid címke + link a teljes
  lexikon-cikkhez.
- Oldalsáv (sidebar): az adott vershez tartozó összes kapcsolat
  folyamatosan listázva olvasás közben.
- Kombinált: inline jel → popup gyors infóval → popupban link a
  teljes lexikon-cikkhez.

**3. Technikai alap:** *(2026.09.09-én, később ugyanezen a napon,
korrigálva — l. alább)* a `naszut` projekt **nem** Hugót használ,
hanem sima statikus HTML-t, Netlify drag-and-drop deploy-jal — ez a
korábbi feltételezés téves volt. Egy tényleges Hugo-alapú megoldáshoz
két, valóban használható mintát azonosítottunk: a Kubernetes Docsy
téma `glossary_tooltip`/`glossary_definition` shortcode-párja (popup
+ link + külön adatfájl, majdnem pontosan a szükséges architektúra —
csak a "term" fogalmat kellene "igehelyre" cserélni), és a
SermonIndex.net Hugo-Biblia-oldal automatikus igehely-linkelő
partial-mintája (`linkscripture.html`, 3-menetes regex-technika) —
utóbbi túlbonyolított lenne a mi esetünkre, mivel nálunk a 29
igehely fix, előre ismert lista, nem szabad szövegben felismerendő
hivatkozás.

**Kézzel épített demó** (2026.09.09, Hugo nélkül): egy minimális
HTML-fájl elkészült, ami két részletet mutat be (1Móz 4:20-26 és Róm
10:10-14), inline jelöléssel (kör + szám) és kattintásra nyíló
popup-kártyával, típus szerint színezve. Ez **csak az egyedi
pár-szintű kapcsolatokat** demonstrálja, a gyűjtemény-szintű
motívum-tagságot nem — l. 4. pont alább, ami egy korlátot tárt fel
ebben a megközelítésben.

**4. ÚJ nyitott kérdés (2026.09.09) — gyűjtemény-szintű tagság vs.
egyedi kapcsolat:** a demó-fájl kipróbálása során kiderült, hogy az
inline jelölés+popup mechanizmus **csak a 7. pont (KAPCSOLATOK)
diagramjában szereplő, konkrét, pár-szintű éleket** tudja
megjeleníteni egy adott versnél. Nem tudja megjeleníteni azt a
**gyűjtemény-szintű** tényt, hogy egy adott vers ugyanannak a
lexikai formulának (H7121+H8034/G1941) **29 előfordulása közül az
egyike** — ez az 1. pont (Előfordulások) táblázatából jönne, nem a
diagramból, és minden 29 versen megjelenne, függetlenül attól, van-e
neki konkrét éle máshova (l. a `ISTENTISZT-001_TUDOMANYOS.md` 7.
pontjának 2026.09.09-i módszertani tisztázó bekezdését erről a
különbségről). **Nyitott kérdés:** kell-e egyáltalán jelezni ezt a
"motívum-tagságot" minden előforduláson, függetlenül a konkrét
kapcsolatoktól, és ha igen, hogyan — külön UI-elemként, hogy ne
keveredjen össze a pár-szintű kapcsolat-jelöléssel?

**Nyitva marad — ez a szakasz nem dönt ezekben:**
- Melyik inline jelölési minta legyen az induló választás.
- Melyik interakciós minta (popup/sidebar/kombinált).
- A lexikon-cikkek tényleges megjelenítési formátuma a
  kereszthivatkozás másik végén (nyers markdown vs. Netlify/Hugo-oldal
  — ez összeköti ezt a szálat a "Publikálási terv" nyitott ponttal).
- **ÚJ:** kell-e külön jelezni a gyűjtemény-szintű motívum-tagságot,
  és ha igen, milyen UI-elemmel, a pár-szintű kapcsolat-jelöléstől
  elkülönítve (l. 4. pont).

Forrás: chat-alapú beszélgetés, 2026.09.09.

## 18. KAPCSOLATOK-megjelenítés — DÖNTÉS: egyszerű motívum-link, induló megoldásként (2026.09.09)

**A döntés:** a 17. pontban feltárt probléma (a pár-szintű,
típusonként színezett popup nem tudja megjeleníteni a
gyűjtemény-szintű motívum-tagságot, és a kétféle logika könnyen
összekeveredik) megoldása: **ne próbáljuk a KAPCSOLATOK-diagram
részleteit (Típus-mező, klaszterek) versenként lebontva, a Károli-
oldalon megjeleníteni.** Ehelyett:

- **Inline jelölés:** egyetlen, semleges jel mind a 29 versen —
  nem típusonként színezett, nem kapcsolat-specifikus. A jel azt
  jelzi: "ez a vers ehhez a motívumhoz tartozik", nem azt, hogy
  "itt pontosan ez a kapcsolat van".
- **Interakció:** nincs mini-popup, ami megpróbálná redundálni a
  cikk tartalmát — egyszerű **link a teljes lexikon-cikkre**.
- A KAPCSOLATOK-diagram, a Típus-mező, a klaszterek — mindez
  **megmarad a lexikon-cikken belül**, változatlanul, ahol már
  készen van. Nem kell versenként szétbontani vagy leegyszerűsíteni.

**Mit old ez meg:** mindkét, a 17. pont 4. alpontjában feltárt
problémát egyszerre — nincs többé "melyik kapcsolatot mutassam
ennél a versnél" döntési kérdés (a link mindig ugyanaz: a teljes
cikk), és nincs külön UI-elem-igény a gyűjtemény- vs. pár-szintű
megkülönböztetésre (nincs két külön logika, csak egy: "tartozik
ehhez a motívumhoz → olvasd el a cikket").

**Az ár:** elveszik a gyors, helyszíni előnézet — az olvasó nem látja
a Károli-oldalon maradva, mi a 4 (vagy 5) konkrét kapcsolat, csak
azután, hogy megnyitotta a teljes cikket.

**Ezzel lezárva a 17. pont 1-2. nyitott kérdése** (inline jelölési
minta, interakciós minta) — legalábbis induló megoldásként. A
típusonként színezett, pár-szintű popup **később, ha a build
megvan és az egyszerű verzió kevésnek bizonyul**, bővítésként még
mindig elképzelhető — ez nem zárja ki, csak nem ez az induló
választás.

**Változatlanul nyitva marad:**
- A lexikon-cikkek tényleges megjelenítési formátuma a
  kereszthivatkozás másik végén (nyers markdown vs. Netlify/Hugo-oldal
  — a "Publikálási terv" nyitott ponttal összekötve).
- A technikai build maga (l. 17. pont 3. alpontja — Docsy-minta,
  Hugo-projekt inicializálása) — ez még mindig egy külön munkamenetet
  igénylő lépés.

Forrás: chat-alapú beszélgetés, 2026.09.09.

## 19. Három pilóta-fájl elkészült és felmentve (2026.09.09-10)

A 18. szakasz döntése (egyszerű, típus nélküli link) és a 17. szakasz
technikai kutatása (Docsy, BibleUp, Floating UI) alapján három
kézzel épített HTML-pilóta készült el, mindegyik `motivumlog/
kereszthivatkozas_pilot/` alatt:

- **`01_demo_2_vers.html`** — az első, kézzel épített próba, csak
  1Móz 4:26-ra és Róm 10:14-re, típusonként színezett, szövegbe
  ékelt popup-kártyával, külső könyvtár nélkül.
- **`02_teljes_pilota_29_vers.html`** — a 18. szakasz döntése szerinti
  teljes megvalósítás: mind a 29 igehely, valódi Károli 1908-szöveggel,
  16 könyvön át, egyetlen szögletes UI-címkével ("Névbe vetett
  segítségül hívás" — a study saját, már definiált Rövid UI-címke
  mezőjéből, l. `Motivum_azonosito_sema_javaslat.md` 4. pontja),
  mindegyik ugyanarra a lap-alji, teljes tartalmú lexikon-cikk
  szakaszra mutatva.
- **`03_floating_ui_pilota.html`** — a gazdagabb, típusonként
  színezett popup-verzió próbája, a `@floating-ui/dom` könyvtárral
  (CDN-ről betöltve) pozicionálva — összehasonlításra a 02-es
  egyszerű verzióval, nem helyette.

**Technikai tanulság (hibakeresésből):** a Floating UI CDN-betöltésnél
a `@floating-ui/core` és `@floating-ui/dom` csomagok **egymáshoz nem
illő verziószámai** (pl. core@1.6.8 + dom@1.6.13) törik az exportált
függvénykészletet ("offset is not a function" hiba) — mindig
egyező verziószámmal kell betölteni mindkettőt (pl. mindkettő
1.8.0), a hivatalos dokumentációban szereplő párosítást követve, nem
külön-külön "legújabb" verziót választva mindkettőhöz.

**Státusz:** mindhárom fájl kézzel épített, önálló HTML, build-
folyamat és Hugo-projekt nélkül — a 17. szakasz "külön munkamenetet
igénylő" build-lépése (tényleges Hugo-projekt-inicializálás) továbbra
sem történt meg, ez a három fájl csak a koncepció kipróbálása.

Forrás: chat-alapú beszélgetés, 2026.09.09-10.
