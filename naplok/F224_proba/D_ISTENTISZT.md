<!-- F224.13 — a bíráló (D) nyers kimenete, változtatás nélkül. Ügynök: general-purpose, model=sonnet, a szerepfájl (.claude/agents/biralo.md) törzsével mint utasítással. Bemenet: naplok/F224_proba/bemenet/dist/ (+ bemenet/ist/ist_forras.md). Tokenek: 144 504, eszközhívás: 14, idő: 319 s. Mentette: claude-opus-5-5, 2026-11-15. A ügynök a `L<n>` jelölést HTML-entitással írta (`L&lt;n&gt;`); ez is változatlan. -->

# Bírálat a próza előtt: ISTENTISZT-001, régi (javítás előtti) állapot

Modell-ellenőrzés: a tényleges modellem `claude-sonnet-5-5`, a kért `sonnet`, tehát egyezik. A `--naplo` kapcsolót nem használtam, mert az a repóba írna. A lekérdezéseket közvetlenül a `konkordancia/` táblákon futtattam. A segédszkriptek a `…/scratchpad/proba/munka_dist/q1.py`–`q5.py` fájlokban vannak, `split('\t')` olvasással.

Jelölések: `V:` az érvvázlat sora (`ist_ervvazlat.md`). `F:` a forrás sora (`ist_forras.md`). `B:` a bizonyítéklap. `L&lt;n&gt;` a lekérdezési napló sorszáma a végén.

---

## 1. vitatott pont: 2Móz 33:19 és 34:5, kiáltás vagy segítségül hívás

### 1. Kérdéslista az írónak

**Súlyos**

- **S1.1 (kérdés 5, a lap két helyének ellentmondása).** A vitatott pont szerint „a lap a kérdést nem dönti el”. A lap azonban négy helyen kimondja a „kiáltás” (az Úr kiáltja ki a nevét) olvasatot.
  - F:11, Kivonat: „kettő Mózes második könyvében, ahol a formula szerkezete az **Úr saját mondatában** szól (2Móz 33:19, 34:5)”.
  - F:25, a helyek rendje: „az a két hely, ahol a formula szerkezete az Úr saját mondatában áll, Mózes előtt”.
  - F:95, Sod: „a 2Móz 34:5-ben **megtörténik**, amit a 33:19 ígér”, és az ebből levont következtetés: „az a név, amelyet az ember segítségül hív, ugyanaz, amelyet az Úr maga kiált ki Mózes előtt”.
  - F:61, a görög fordítás szakasza: „ott tér el tőle, ahol a héber szerkezet az Úr saját mondatában áll”.
  - A 34:5 elbeszélő mondat, nem az Úr „mondata”. Ha a 34:5 alanya Mózes (a második olvasat), a Sod állítása elveszíti a másik lábát: marad a 33:19 ígérete, esemény nélkül. A vázlat ezért az egyik olvasatot adatként használja, a másikat „vitatott”-ként tartja.
- **S1.2 (kérdés 2 és 3, az érv valódi ereje, hiányzó érv).** A vázlat szerint a második olvasat mellett szól, hogy „a héber mondat a kiáltót külön nem nevezi meg”. A héber szöveg viszont megnevezi a legközelebbi alanyt.
  - A 34:5 három egymás utáni wayyiqtol igéből áll: `וַיֵּרֶד יְהוָה` (az Úr leszállt), `וַיִּתְיַצֵּב עִמּוֹ` (megállt vele), `וַיִּקְרָא` (kiáltott/hívott) (L1, B:41–43). Az alany az első igénél az Úr. A mondat mellékszereplője az `עִמּוֹ` utótagjában szereplő „ő” (Mózes). Alanyváltásra a szövegben nincs jel.
  - A második olvasat tehát alanyváltást igényel az `עִמּוֹ` után. A Vulgata ezt úgy éri el, hogy a „stetit Dominus cum eo” helyett „stetit **Moyses** cum eo”-t ír (L5). Ez fordítói beavatkozás, nem a héber szöveg többértelműsége.
  - A vázlat ezt nem mondja ki. A „külön nem nevezi meg” érv így a hallgatásból vett (hiány-típusú) érv, és a **második** olvasat felé gyengébb, mint ahogy áll.
- **S1.3 (kérdés 1, 2 és 7, a „szerkezet ugyanaz” érv).** Az érv így szól: „a szerkezet ugyanaz, mint az emberi segítségül hívás helyein”. Ez nem megkülönböztető érv.
  - A `קָרָא` + `בְּ` + `שֵׁם` szerkezet a TAHOT-ban 29 versben áll (L2). Ezek között olyanok is vannak, ahol a szerkezet **megnevezést** jelent, nem segítségül hívást. Például 2Móz 31:2 és 35:30 (`קָרָאתִי בְשֵׁם בְּצַלְאֵל`, „név szerint hívtam Becalélt”), Ézs 43:1, 45:3. A BDB maga külön sorolja: Qal 4 „summon by name” (BDB, L6).
  - Ugyanaz a szerkezet tehát legalább három szerepet visz: segítségül hívás, kihirdetés, név szerinti megszólítás. A „szerkezet” mindkét olvasattal összefér.
  - A határkérdést (a 31:2 miért nem tartozik ide) nem én ítélem meg. Azt jelzem, hogy az érvelés a határ alakja szerint a motívumon belülre rajzolt szerkezetre épül, és erre a szerkezet nem elegendő bizonyíték.

**Közepes**

- **K1.1 (kérdés 4, szintkeverés).** A pont érveit a vázlat egyenrangúan sorolja fel, de három típus keveredik.
  - Szövegtanú: a 33:19 beszélője; a 34:6 „az Úr … kiálta”; a 34:5 alanya.
  - Recepció: BDB (Qal 3.b, 1906), LXX, Targum, Vulgata.
  - A recepciós tanúk (LXX, Targum) mind az első olvasat mellett állnak. A Vulgata a második mellett, de annak a 34:5-ben a 34:6-ot is vokatívusszá alakítja: „Quo transeunte coram eo, ait: Dominator Domine Deus” (L5). Ott a Vulgata szerint Mózes beszél, mert az „Úr, Úr” megszólítás.
  - A 34:6 „az Úr kiálta: Az Úr, az Úr” ezért önmagában kérdéses érv: a 34:6 ugyanabban az alanyi kérdésben áll, amelyet bizonyítana. A vázlat szövegtanúként használja az első olvasat mellett. Nem független az 1.1–1.2 érvtől. A 34:6 ige- és vokatívusz-olvasatának rabbinikus tárgyalásáról a repó nem ad adatot: lekérdezendő.
- **K1.2 (kérdés 2, a fordítási tanúk ereje).** A vázlat a görög és a Targum tanúságát egymás melletti „egy olvasatot támogató” érvként adja. Mérésem szerint ezek eltérők.
  - LXX 33:19: `καὶ καλέσω ἐπὶ τῷ ὀνόματί μου κύριος ἐναντίον σου` (L4). Ez „az **én nevemre**” (`μου`), ἐπί elöljáróval, és a `κύριος` a név tartalma lehet. A héber szöveg nem ezt mondja (a héberben `בְשֵׁם יְהוָה`, „az Úr nevében”).
  - LXX 34:5: `ἐκάλεσεν τῷ ὀνόματι κυρίου`, tisztán datívusz, elöljáró nélkül. A formula többi LXX-helyén az ἐπικαλέω + accusativus áll. A kiáltó a LXX-ben `κύριος`, nincs alanyváltás.
  - Az „előtag nélküli καλέω” tehát csak az egyik jel. A szerkezet (ἐπὶ τῷ ὀνόματί μου / datívusz) más szerkezet, nem csak más ige. A vázlat ezt az eltérést nem említi.
  - Targum (Onkelos): 33:19 `וְאֶקְרֵי בִשְׁמָא דַיְיָ`, 34:5 `וּקְרָא בִשְׁמָא דַיְיָ` (L3). Az Onkelos 34:5-ben az alany az `יְיָ` (`וְאִתְגְלִי יְיָ … וְאִתְעַתַּד עִמֵהּ … וּקְרָא`). A Targum tehát az **Úrnak** tulajdonítja a kiáltást: ez támogatja az első olvasatot, és megkülönböztető is, mert az emberi segítségül hívást másutt `צלי`-vel adja (1Móz 12:8, 13:4, 21:33, 26:25, L3).
  - A vázlat ezt az érvet a 34:5 alanyáról nem használja, csak a „hívás igéjét” említi. Ez a legerősebb recepciós tanú, kihasználatlanul.
- **K1.3 (kérdés 1, az egyensúly).** A 33:19-re a második olvasat nem alkalmazható.
  - A 33:19-ben az alany első személyű (`קָרָאתִי`, az Úr beszél), és a címzett Mózes (`לְפָנֶיךָ`, L1). A „Mózes hívja segítségül” olvasat csak a 34:5-re lehet érvényes.
  - A vitatott pont címe és záró mondata („mindkét hely”) a két verset egy kérdésbe vonja. Valójában két kérdés van: a 33:19-ben nincs alanyvita, csak a „kihirdetés vs. segítségül hívás” (BDB 3.b vs 2.c). A 34:5-ben alanyvita is van. A kettő különböző súlyú.

**Enyhe**

- **E1.1 (kérdés 6, szakirodalom-hatókör).** A „BDB … a név kihirdetéséhez sorolja”: a BDB Qal 3.b valóban „Exod 33:19; 34:5 (JE)” (L6). A BDB egy 1906-os szótár, forráskritikai megjelöléssel. Az állítás pontos, de hatóköre egyetlen szótár. A kommentárirodalomról és a rabbinikus olvasatokról (pl. a 34:6 kiáltó alanya) a bemenet nem tartalmaz adatot: lekérdezendő.
- **E1.2 (kérdés 7, a szerkezet jelölése).** A „khiazmus/keret” nem szerepel a pontban. A „fordított sorrendű ismétlés” a bizonyítéklapon: nincs (B:32, B:47). Itt tehát nincs gyengeség.

### 2. Elutasított tételek

- „A 34:5 szerkezete miatt az Úr saját mondata” (F:11, F:25, F:61, F:95). Ez eldönti a vitát, így nem tartható, amíg a vitatott pont „nem dönti el”-t mond.
- „A 34:5-ben megtörténik, amit a 33:19 ígér” (F:95) mint adat. A második olvasat szerint nem történik meg, mert Mózes hívja segítségül.
- „A szerkezet ugyanaz, mint az emberi segítségül hívás helyein” mint megkülönböztető érv a második olvasat mellett (S1.3): ugyanez a szerkezet a megnevezés helyein is áll.
- „A héber mondat a kiáltót külön nem nevezi meg” ebben a formában (S1.2): a legközelebbi megnevezett alany az Úr.

---

## 2. vitatott pont: 1Móz 4:26, kezdet vagy hanyatlás

### 1. Kérdéslista az írónak

**Súlyos**

- **S2.1 (kérdés 3, hiányzó szövegbeli érv).** A vitatott pont „A héber mondat azt mondja, hogy … »kezdték«” mondattal kezd. A héber szövegben ez nem ilyen egyértelmű, és a vázlat a három olvasat közös gyökerét nem mondja ki.
  - A héber ige `הוּחַל` (hofal, H2490 `חָלַל`). A TAHOT glosszája: „to profane; begin” (L7, B:55–60). A forma a TAHOT-ban csak egyszer fordul elő, hapax (L8). A BDB „then it was begun (= men began)” értelmet ad a hofal alaknak (L9).
  - A vázlat azt írja, hogy a Targum „megfordítja” (`חָלוּ … מִלְּצַלָּאָה`, „felhagytak az imádkozással”, L3, Onkelos). A LXX `ἤλπισεν` („remélte”) más gyököt olvas (`יחל`), ahogy a vázlat is jelzi.
  - A három „olvasat” (kezdték / felhagytak / remélte) ugyanannak a szónak a három lehetséges gyök- vagy értelmezése. A bizonyítéklap glosszája is mutatja (H2490 egy szó alatt a „profane” és a „begin”). A vázlat ezt nem teszi explicit érvvé, pedig ez a kérdés egyetlen szövegi magva, és a hapax-státusz miatt nincs belső összehasonlítási tanú.
  - A mondat „A héber mondat azt mondja … kezdték” enyhén túlállít: a héber hofal egyes számú, személytelen („kezdetett”), a „kezdték” (többes szám, cselekvő) már értelmezés.
- **S2.2 (kérdés 5, a lap két helyének ellentmondása).** A pont szerint „a lap a kérdést nem dönti el”, a lap viszont dönt.
  - F:9, Kivonat: „A formula Énós nemzedékében **kezdődik**” (idézőjel nélkül, ténymondatként), és az 1Móz 4:26 a motívum első helye.
  - F:25: „a kezdet Énós nemzedékében”.
  - F:53 (H8034, BDB): „ahol a szótár magyarázata szerint a nevet az istentiszteletben használják”.
  - F:57 (Thayer): az 1Móz 4:26 a „héber formula görög mása” példájaként áll.
  - F:93 (Drash): „A pátriárkák helyein egy ember vagy egy nemzedék hívja segítségül” (a 4:26 egy nemzedék).
  - A vázlat „a motívum a vers héber szövegét és a Károli fordítását követi, amely a kezdetet mondja ki” mondata magyarázat arra, miért dönt a lap. A „követi” azonban döntés (a Károli-olvasat mint mérce), és a lap többi része a kezdetre épít (F:9, F:25), nem csak a kérdés megnevezésére.

**Közepes**

- **K2.1 (kérdés 6, szakirodalom-hatókör).** „Az ókori fordítások közül a Targum a mondatot megfordítja.” A repóban a Targum_PD.tsv Mózes öt könyvében kizárólag Onkelos található (5846 vers, L11). A Targum Neofiti és a Pszeudo-Jonatán nem áll rendelkezésre. A „Targum” tehát egy targum, nem az arámi fordítási hagyomány. A lap az „ókori fordítások” kifejezést használja, a hatókör: egy Targum.
  - Ráadásul az Onkelos ugyanazt a `צלי` igét használja a 4:26-ban („felhagytak az imádkozással az Úr nevében”), mint az emberi segítségül hívás többi helyén, és ott szolgálja a formulát. A lap a Peshat-ban a Targumot adatként használja az öt helyről (F:85). A 4:26 a „hét helyből öt” között szerepel, tehát ugyanaz a Targum, amely a formula emberi cselekvésére a `צלי`-t adja, a 4:26-ban a cselekvés **megszűnését** állítja. Az F:85-ben ez a megkülönböztetés nem látszik.
- **K2.2 (kérdés 1, 2, az egyensúly).** A pontban három olvasat áll, de az érvek típusa kevert.
  - Kezdet: Károli (recepció), a héber szöveg (a bizonyítéklap szerint hofal, mint fent), továbbá a Vulgata, amely a vázlatban nem szerepel: „iste cœpit invocare nomen Domini” (L5), ez is a kezdetet adja.
  - Hanyatlás: Onkelos (recepció).
  - Remény: LXX (recepció).
  - A pont három recepciós olvasatot állít szembe, szövegtanú nélkül. A hallgatásból vett érv itt nincs, de a „héber szöveg” sem szövegtanúként szerepel: csak mint a „kezdetet mondó” szöveg.

**Enyhe**

- **E2.1 (kérdés 4).** Az „Énós remélte” görög olvasat szerkezeti (gyökérváltásos), a Targum értelmezői. A vázlat mindkettőt „olvasat”-ként nevezi: a megnevezés nem különbözteti meg, hogy a LXX igeolvasatot, a Targum értelmezői magyarázatot ad.

### 2. Elutasított tételek

- „A héber mondat azt mondja, hogy … »kezdték«” szó szerinti szövegtanúként: a héber személytelen hofal, hapax, kettős gyökkel (L7–L9).
- „A Targum” általánosan az ókori fordítások képviselőjeként: csak Onkelos áll rendelkezésre (L11).
- „A formula Énós nemzedékében kezdődik” (F:9) mint a vitatott pont melletti tény: a pont maga szerint nem eldöntött.

---

## 3. vitatott pont: Róm 10:13 „Ura”, az Úr Jóel könyvében vagy Jézus

### 1. Kérdéslista az írónak

**Súlyos**

- **S3.1 (kérdés 3, hiányzó szövegbeli érv).** A pont a második olvasat (Jézus) mellett a Róm 10:9-et és az 1Kor 1:2-t hozza. Közelebbi, a Róm 10-en belüli adat a vázlatban nem szerepel.
  - Róm 10:11: `πᾶς ὁ πιστεύων ἐπ᾽ αὐτῷ` („aki hisz **őbenne**”, L12).
  - Róm 10:12: `ὁ γὰρ αὐτὸς κύριος πάντων πλουτῶν εἰς πάντας τοὺς ἐπικαλουμένους αὐτόν` („**ugyanaz** az Úr mindenkié, gazdag mindazokhoz, akik hívják **őt**”, L12). A lap maga idézi a 10:12-t (F:93), a vázlat mégsem.
  - Róm 10:14: `Πῶς οὖν ἐπικαλέσωνται εἰς ὃν οὐκ ἐπίστευσαν;` („hogyan hívják segítségül azt, akiben nem hittek?”, L12): a segítségül hívott és a hitnek tárgya ugyanaz.
  - A 10:9 `κύριον Ἰησοῦν` és a 10:12 `ὁ αὐτὸς κύριος` szoros szövegi lánc. Ez a legközelebbi szövegtanú a második olvasat mellett, és erősebb, mint az 1Kor 1:2, amely másik levél. A vázlat a távolabbi bizonyítékot említi, a közelebbit nem. Az 1Kor 1:2 ugyanazon szerző másik levele, nem a Róm 10:13 szövegtanúja.
- **S3.2 (kérdés 1, az érvek egyensúlya).** Az első olvasat („ugyanaz, mint Jóelnél”) mellett a vitatott pont egyetlen érvet sem hoz: csak azt állítja, hogy „Pál a próféta mondatát a maga értelmében idézi”. A második olvasat mellett három érv áll (10:9, 1Kor 1:2, Thayer).
  - Az első olvasat szövegi alapja: a LXX Jóel 2:32 `ὃς ἂν ἐπικαλέσηται τὸ ὄνομα κυρίου` (L13), és a Jóel 2:32 héber szövegében `בְּשֵׁם יְהוָה` (L14). A Róm 10:13 és az ApCsel 2:21 szó szerint a LXX-ból idéz (L12), a `κυρίου` változatlan.
  - Ez a vázlatban nem érvként jelenik meg. A pont azt az állapotot mutatja, mintha az egyik olvasat érv nélkül állna a másik mellett.
- **S3.3 (kérdés 5, a lap két helyének ellentmondása).** A „lap nem dönti el” mondat mellett a lap két ellentétes irányba húz.
  - Jóel-irányba: F:9, Kivonat, „A fordulópont Jóel mondata … Az Újszövetség Jóel mondatát idézi (ApCsel 2:21, Róm 10:13)”; F:89, Remez, „Az első Jóel ígéretétől vezet az Újszövetségig: az ApCsel 2:21 és a Róm 10:13 … szó szerint ugyanazt a mondatot hozza”, mint magas erősségű kapcsolat.
  - Jézus-irányba: F:93, Drash, „A harmadik: az Újszövetségben a név után álló szó Jézus Krisztus”, és a példa az 1Kor 1:2; F:9, Kivonat, „az 1Kor 1:2-ben pedig a név után Jézus Krisztus neve áll”.
  - A Drash általánosít („az Újszövetségben”), pedig az „a név után Jézus Krisztus áll” kifejezetten csak az 1Kor 1:2-re igaz (L12). Az ApCsel 2:21 és a Róm 10:13 `τὸ ὄνομα κυρίου` alakja Jézust névvel nem nevezi (L12). A Róm 10:13-ra vonatkozó vita pontosan az, hogy a `κυρίου` kire vonatkozik. A Drash-állítás előre dönt a vitában, amelyet a vitatott pont nyitva hagy.

**Közepes**

- **K3.1 (kérdés 4, szintkeverés).** A pont érveinek típusai:
  - szövegtanú: Róm 10:9, 10:11–14 (ugyanabban a levélben), Jóel 2:32 héber és LXX szöveg;
  - kereszthivatkozás/szómagyarázat: 1Kor 1:2 (másik levél);
  - recepció: Thayer szótár 5. jelentése („A Thayer-szótár … a második olvasatot adja”).
  - A vázlat a Thayer-t érvként, ugyanazon a szinten sorolja a szövegi adatokkal. A Thayer egy 19. századi szótár értelmezése, nem a vers szövegtanúja. Hogy a szótár tényleg ezt a jelentést adja a Róm 10:13-hoz, az `adat/thayer_vers_jelentes.tsv`-ben van, amit nem nyithattam meg: lekérdezendő.
- **K3.2 (kérdés 2, az érv valódi ereje, a Jézus-olvasat).** Az ApCsel 2-ben, ahol ugyanaz a Jóel-idézet áll, a szövegkörnyezet ezt a kérdést megválaszolja: 2:36 `κύριον … Ἰησοῦν`, 2:38 `ἐν τῷ ὀνόματι Ἰησοῦ` (L16). Ez a közvetlen, a vázlatban nem szereplő párhuzam, és a Jóel-idézet Péter-féle alkalmazása az adat. A vázlat csak a Róm-ot és az 1Kor-t használja. Hogy az ApCsel 2:36 érve a Róm 10:13 értelmezésére mennyit nyom, az nem az én kérdésem. Az viszont igen, hogy a hasonló használat másutt (a lap saját anyagában, F:9) benne van, a vázlatban nem.

**Enyhe**

- **E3.1 (kérdés 6, ismétlődés).** A vázlat szerint „Pál a Jóel 2:32-t idézi” és „a görög fordítás ezt κύριος szóval adja vissza”. Mindkettő igaz (L13, L14). A mondat „négy verssel korábban” a Róm 10:9-ről pontos.
- **E3.2 (a Remez-mondat pontossága, F:89).** „az ApCsel 2:21 és a Róm 10:13 görögül szó szerint ugyanazt a mondatot hozza, mint a Jóel 2:32 görög fordítása.” Az ApCsel 2:21 az `καὶ ἔσται πᾶς ὃς ἂν ἐπικαλέσηται τὸ ὄνομα κυρίου σωθήσεται` szó szerint a LXX Jóel-mondat. A Róm 10:13 `πᾶς γὰρ ὃς ἂν ἐπικαλέσηται τὸ ὄνομα κυρίου σωθήσεται`: a `καὶ ἔσται` helyén `γάρ` áll (L12, L13). A „szó szerint ugyanaz” a Róm-ra csak a `πᾶς ὃς ἂν … σωθήσεται` magra igaz.

### 2. Elutasított tételek

- „Az Újszövetségben a név után álló szó Jézus Krisztus” (F:93, Drash) általánosításként: csak az 1Kor 1:2 tartalmazza (L12).
- „A Thayer a második olvasatot adja” mint a lap érve, szövegtanúi szinten: a szótári besorolás recepció, és a forrása nem ellenőrizhető a megengedett körben.
- A Róm 10:13 „szó szerint ugyanaz” a Jóel-mondattal (F:89), kiegészítés nélkül: a nyitó szavak eltérnek (E3.2).

---

## Lekérdezési napló

A pontonkénti keret legfeljebb 10 lekérdezés. A közös lekérdezéseket egyszer számoltam, ahol a pontokra használtam, ott a sorszám megegyezik.

| Sorszám | Parancs (közvetlen szkript) | Találat |
|---|---|---|
| L1 | `q1.py`: `TAHOT_kivonat.tsv`, 2Móz 33:19, 34:5, 34:6, 1Móz 4:26 szavai | 4 vers, teljes szószint |
| L2 | `q2.py`: `TAHOT_kivonat.tsv`, `H7121` + `H9003` + `H8034` szerkezet (3 szón belül) | 29 vers (köztük 2Móz 31:2, 35:30, Ézs 43:1, 45:3) |
| L3 | `q3.py`: `Targum_PD.tsv`, 1Móz 4:26, 12:8, 13:4, 21:33, 26:25, 2Móz 33:19, 34:5, 34:6 | 8 vers (Onkelos) |
| L4 | `q3.py`: `LXX_OS/exodus.tsv`, `genesis.tsv`, `joel.tsv` | 2Móz 33:19, 34:5, 34:6, 1Móz 4:26, Jóel 2:32 |
| L5 | `q3.py`: `Vulgata_Clementina.tsv` | 1Móz 4:26, 2Móz 33:19, 34:5, 34:6, Róm 10:9, 10:12, 10:13, Jóel 2:32 |
| L6 | `q4.py`: `BDB_teljes_unabridged.tsv`, H7121, a 33:19 / 34:5 / 4:26 hivatkozások | Qal 2.c (4:26), Qal 3.b (33:19; 34:5), Qal 4 (név szerint) |
| L7 | `q1.py`: 1Móz 4:26 `H2490` glossza | `הוּחַל`, „to profane; begin” |
| L8 | `q4.py`: `TAHOT_kivonat.tsv`, `H2490` hofal-alakok (`^ה[וֻ]`) | 1 találat (1Móz 4:26), minta szerint; teljes alaktani ellenőrzés: lekérdezendő |
| L9 | `q4.py`: BDB `H2490`, 4:26 | Hoph`al: „then it was begun (= men began)” |
| L10 | `q4.py`: TAHOT Jóel 2:32 | `יִקְרָא בְּשֵׁם יְהוָה`, 3 × `H3068` a versben |
| L11 | `q5.py`: `Targum_PD.tsv`, Mózes öt könyve, verziók | csak Onkelos, 5846 vers |
| L12 | `q3.py`: `TAGNT_kivonat.tsv`, Róm 10:9, 10:11–14, ApCsel 2:21, 1Kor 1:2 | 7 vers |
| L13 | `q3.py`: `LXX_OS/joel.tsv`, Jóel 2:32 | 1 vers |
| L14 | `q4.py`: `TAGNT_kivonat.tsv`, ApCsel 2:36, 2:38 | `κύριον … Ἰησοῦν`, `ἐν τῷ ὀνόματι Ἰησοῦ` |

### Lekérdezendő (nem kérdeztem le, nem állítom tényként)

- A 2Móz 34:6 `יְהוָה יְהוָה` megszólítás vagy tartalom-e: rabbinikus és kommentár-hagyomány (1. pont).
- Targum Neofiti és Pszeudo-Jonatán 1Móz 4:26 olvasata (2. pont): nincs a repóban.
- A hofal `הוּחַל` alaktani teljes körű ellenőrzése: a TAHOT minta alapján egy találat. A teljes Bibliára kiterjedő hofal-keresést nem futtattam (2. pont).
- A Thayer 5. jelentése valóban a Róm 10:13-hoz sorolja-e a „Jézus” olvasatot (3. pont): a forrás (`adat/thayer_vers_jelentes.tsv`) a vak szabály alá esik.

(proveniencia: scope=ist_ervvazlat.md mind a 3 vitatott pontja, ist_bizonyitek.md, ist_forras.md (teljes), konkordancia/TAHOT_kivonat.tsv, TAGNT_kivonat.tsv, Targum_PD.tsv, Vulgata_Clementina.tsv, LXX_OS/{exodus,genesis,joel}.tsv, BDB_teljes_unabridged.tsv | forras=modell:claude-sonnet-5-5 | ts=2026-11-15)
