# -*- coding: utf-8 -*-
"""F123 ALVIL-001 új cikk, U3 — az 1/a igehelyenkénti prózája és a lap olvasói adatmezői, nulláról.

Ír (a nem érintett sorok bájtra egyezésének kontrolljával, split('\\t'), CLAUDE.md):
  - adat/elofordulasok.tsv: a 72 ALVIL-001-sor `kapcsolodas` és `funkcio` mezője (kerek mondat;
    „címke — magyarázat”), és két új sor (Mt 16:18, 1Kor 15:55; a jelöltsoruk `beépítve`, DT-F123b);
  - adat/jeloltek.tsv: a három régi `elutasítva` sor indoklása olvasói nyelven (a döntés nem változik);
  - adat/motivumok.tsv: az ALVIL-001 `negativ_kriterium` és `folerendelt_fogalom` mezője olvasói nyelven;
  - adat/szotar_szakasz_cimke.tsv: a BDB H7585 2.a címkéje a szakasz teljes tartalmára (lap-átvilágítás A3);
  - adat/res_forras.tsv: az ALVIL-001 `tanitoi` résének hiány-szövege olvasói nyelven.
Szerző: claude-opus-5-5, egy kézből (F123_MIGRACIO2_BRIEF.md 2a, U3). A régi `kapcsolodas` csak alapanyag.
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = '2026-11-02'

# igehely: (kapcsolodas, funkcio)
P = {
'1Móz 37:35': ('Jákób nem fogad vigasztalást József vélt halála után, és kijelenti: „Sírva megyek fiamhoz a sírba”. A héber szöveg itt a seólt nevezi meg először a Bibliában, a gyászoló apa céljaként, ahová a halott fia után ő is lemegy.',
               '🌱 alap-előfordulás — a szó első megjelenése: a halottak helye, ahová a gyászoló a halott után lemegy'),
'1Móz 42:38': ('Jákób nem engedi Benjámint a testvéreivel Egyiptomba, mert ha baj érné, az ő ősz fejét „búba borítva bocsátanátok le a koporsóba”. A fia elvesztése miatti bánat vinné le az öreg apát a Seolba.',
               '🔁 ismétlődés — a Jákób-történet gyászmondata visszatér: a fiú elvesztése az apát a Seolba vinné'),
'1Móz 44:29': ('Júda Józsefnek idézi fel atyja szavait: ha Benjámint is elviszik, az öreg Jákób ősz fejét „keserűségtől borítva bocsátjátok alá a koporsóba”. A gyászmondat itt már egy könyörgés érve.',
               '🔁 ismétlődés — a gyászmondat Júda szájából, a közbenjárás érveként'),
'1Móz 44:31': ('Júda végigviszi az érvet: ha a gyermek nem tér haza, az apa meghal, és a testvérek lesznek azok, akik ősz fejét „búba borítva bocsátják alá a koporsóba”. Az apa Seolba jutásának felelőssége így a fiakra száll.',
               '🔁 ismétlődés — a gyászmondat utolsó előfordulása: a Seolba jutás felelőssége a testvérekre hárul'),
'4Móz 16:30': ('Mózes kijelenti, hogy ha Kóré és társai „elevenen szállanak alá pokolba”, abból tudja meg a nép, hogy ezek az emberek az Urat gyalázták. A Seolba jutás itt nem a halál rendes útja, hanem az Úr új, mindenki által látható ítélete.',
               '⚡ élve alászállás — a Seol az isteni ítélet eszköze, amely a lázadókat elevenen nyeli el'),
'4Móz 16:33': ('A föld megnyílik, és Kóré lázadói mindenükkel együtt „elevenen a pokolra” szállnak, majd a föld befedi őket. A 16:30-ban meghirdetett jel itt szó szerint teljesedik.',
               '⚡ élve alászállás — a meghirdetett ítélet végrehajtása: a lázadók élve jutnak a Seolba'),
'5Móz 32:22': ('Mózes énekében az Úr haragjának tüze „leég a Seol fenekéig”, megemészti a földet, és a hegyek alapjait is felgyújtja. A Seol itt a világ legalsó pontja, ameddig Isten ítélete leér.',
               '👑 Isten hatalma — Isten haragja a Seol mélyéig ér, a halottak helye sincs kívül az ítéletén'),
'1Sám 2:6': ('Anna hálaénekében az Úr az, aki „öl és elevenít, Sírba visz és visszahoz”. A Seolba vitel és az onnan való visszahozás egyaránt az Úr kezében van.',
             '👑 Isten hatalma — az Úr levisz a Seolba és felhoz onnan: élet és halál egyedül az övé'),
'2Sám 22:6': ('Dávid szabadulási énekében a halál fenyegetését így mondja el: „A pokol kötelei vettek körül, S a halál tőrei estek reám.” A következő versben az Úrhoz kiált, és Isten meghallgatja.',
              '🙏 kiáltás a Seol szorításából — a Seol köti meg az énekest, aki az Úrhoz kiált és megszabadul; párja a Zsolt 18:6'),
'1Kir 2:6': ('Dávid halála előtt arra inti Salamont, hogy Joábot ne engedje, hogy megőszülve „békességgel menjen a koporsóba”. Itt nem az a kérdés, hogy valaki a Seolba jut-e, hanem az, hogy büntetlenül jut-e oda.',
             '⚖️ ítélet a halál módjában — a vétkes ne érje el békében a Seolt'),
'1Kir 2:9': ('Dávid Simeiről is rendelkezik: Salamon ne hagyja büntetlenül, hanem „az ő vénségét vérrel bocsássad a koporsóba”. Ez a 2:6 párja, ugyanazzal az ítélettel.',
             '⚖️ ítélet a halál módjában — a 2:6 párja: a büntetlen öregkori halál helyett erőszakos vég'),
'Jób 7:9': ('Jób a halál véglegességét az eltűnő felhőhöz hasonlítja: „a ki leszáll a sírba, nem jő fel többé”. A Seolból ebben a panaszban nincs visszatérés.',
            '🪦 a halottak helye — a Seol a visszatérés nélküli hely, az emberi élet végpontja'),
'Jób 11:8': ('Cófár Isten bölcsességéről azt mondja, hogy magasabb az égnél, és „Mélyebb az alvilágnál”. A Seol itt a legnagyobb mélység mértéke, amelynél Isten bölcsessége még mélyebb.',
             '👑 Isten hatalma — Isten bölcsessége a Seolnál is mélyebb, ember nem érheti fel'),
'Jób 14:13': ('Jób azt kívánja, hogy Isten rejtse el őt „a holtak országában”, amíg haragja elmúlik, aztán szabjon neki határt, és emlékezzen meg róla. A Seol itt átmeneti rejtekhely, ahonnan Isten visszahívhatja.',
              '🕊️ remény a Seolban — Jób a Seolt rejtekként kéri, ahol Isten megemlékezik róla'),
'Jób 17:12': ('Jób kimondja, hogy reménykedése ellenére „a sír már az én házam”, és a sötétségben vetett ágyat magának. A Seol itt az a lakóhely, amely felé a beteg ember már elindult.',
              '🪦 a halottak helye — Jób a Seolt már a saját házának tekinti'),
'Jób 17:15': ('Jób azt kérdezi, mi lesz a reménységével, és így felel: „Leszáll az majd a sír üregébe”, és vele együtt nyugszik a porban. A Seolba nemcsak ő, a reménysége is vele száll.',
              '🪦 a halottak helye — a Seolba nemcsak az ember, a reménysége is leszáll'),
'Jób 21:13': ('Jób a gonoszok jólétét panaszolja: napjaikat bőségben töltik, és „egy pillanat alatt szállnak alá a sírba”, hosszú szenvedés nélkül. A Seol mindenki közös vége, és a gonosz könnyű halála Jób szemében igazságtalanság.',
              '🪦 a halottak helye — a gonosz is gyötrelem nélkül jut a Seolba, ez Jób panaszának tárgya'),
'Jób 24:19': ('Ahogy a szárazság és a hőség elnyeli a hó vizét, úgy nyeli el „a pokol azokat, a kik vétkeznek”. A mondásban a Seol a bűnösök gyors és nyomtalan eltűnése.',
              '⚖️ a gonoszok sorsa — a Seol elnyeli a vétkezőket, ahogy a hőség a vizet'),
'Jób 26:6': ('Jób Isten nagyságát dicsérve mondja: „Az alvilág mezítelen előtte”, és a pusztulás helye sincs eltakarva. A Seol semmit sem rejt el Isten szeme elől.',
             '👑 Isten hatalma — a Seol nyitva áll Isten előtt'),
'Zsolt 6:6': ('A beteg zsoltáros arra hivatkozik, hogy a halálban nincs emlékezés Istenről, és megkérdezi: „a seolban kicsoda dicsőít téged?” Mivel a Seolban elnémul a dicséret, az életéért könyörög.',
              '🪦 a halottak helye — a Seolban nincs dicséret: ez a szabadításért mondott ima érve'),
'Zsolt 9:18': ('A zsoltár kimondja: „Seolba jutnak a gonoszok”, és vele minden nép, amely elfeledkezik Istenről. A Seol itt az Istent elfelejtők végső sorsa.',
               '⚖️ a gonoszok sorsa — a Seol az Istenről megfeledkező népek célja'),
'Zsolt 16:10': ('Dávid bizalommal mondja Istennek: „nem hagyod lelkemet a Seolban”, és nem engedi, hogy szentje rothadást lásson. Péter pünkösdi beszéde ezt a verset Krisztus feltámadására idézi.',
                '🎯 előkép — a Seolban nem maradó szent ígérete, amely az Újszövetségben Krisztus feltámadásában teljesedik'),
'Zsolt 18:6': ('Ugyanaz a vallomás, mint a 2Sám 22:6-ban: „A Seol kötelei vettek körül”, és a halál tőrei fogták meg a zsoltárost. A következő versben az Úrhoz kiált, és Isten meghallja a hangját.',
               '🙏 kiáltás a Seol szorításából — a 2Sám 22:6 párja a Zsoltárok könyvében'),
'Zsolt 30:4': ('A zsoltáros hálát ad: „Uram, felhoztad a Seolból az én lelkemet”, és felélesztette őt a sírba szállók közül. A Seol itt az a hely, ahonnan Isten már kimentette.',
               '🕊️ szabadulás a Seolból — hálaadás a már megtörtént kimentésért'),
'Zsolt 31:18': ('A szorongatott zsoltáros azt kéri, hogy ő ne szégyenüljön meg, a gonoszok viszont „pusztuljanak a Seolba”. Itt a Seol az ellenség kívánt sorsa, nem a hívőt fenyegető hatalom.',
                '⚖️ a gonoszok sorsa — az imádkozó az ellenségnek kívánja a Seolt'),
'Zsolt 49:15': ('A gazdagságukban bízókról mondja a zsoltár: „Mint juhok, a Seolra vettetnek”, a halál legelteti őket, és alakjukat a Seol emészti el. A vagyon nem menti meg őket a közös végtől.',
                '⚖️ a gonoszok sorsa — a gazdagságban bízók nyájként jutnak a Seolba'),
'Zsolt 49:16': ('A zsoltáros szembeállítja velük a saját reményét: „Csak Isten válthatja ki lelkemet a Seol kezéből”. A Seol hatalmából egyedül Isten válthat ki.',
                '🕊️ szabadulás a Seolból — az igaz reménye, hogy Isten kiváltja őt a Seol hatalmából'),
'Zsolt 55:16': ('Az áruló barát miatt gyötrődő zsoltáros azt kéri, hogy ellenségei „elevenen szálljanak a Seolba”. A kép Kóré lázadóinak élve alászállására emlékeztet.',
                '⚖️ a gonoszok sorsa — ítélet kérése az ellenségre; itt a Seol nem a hívőt szorongatja'),
'Zsolt 86:13': ('A zsoltáros Isten nagy kegyelmét dicséri, mert „kiszabadítottad lelkemet a mélységes pokolból”. A Seol legmélyéről való szabadítás a hála oka.',
                '🕊️ szabadulás a Seolból — hála a legmélyebb Seolból való kimentésért'),
'Zsolt 88:4': ('A súlyos beteg panaszolja, hogy lelke betelt nyomorúsággal, és „életem a Seolig jutott”. Az élő ember itt már a Seol határán áll, és onnan beszél Istenhez.',
               '🪦 a halottak helye — az élő ember a Seol határára jut, és innen panaszolja helyzetét'),
'Zsolt 89:49': ('A zsoltár azt kérdezi, kicsoda olyan erős, hogy ne lásson halált, „s megszabadítsa magát a Seolnak kezéből”. A válasz kimondatlan: senki sem mentheti ki magát a Seolból.',
                '🪦 a halottak helye — a Seol minden embert elér, magát senki nem szabadíthatja meg'),
'Zsolt 116:3': ('A zsoltáros felidézi, hogy körülvették a halál kötelei, és „a pokol szorongattatásai támadtak meg engem”. A következő versben az Úr nevét hívja segítségül, és szabadulást nyer.',
                '🙏 kiáltás a Seol szorításából — a Seol szorongatja a hívőt, aki az Úrhoz kiált; itt ér össze a motívum az Úr nevének segítségül hívásával'),
'Zsolt 139:8': ('A zsoltáros Isten jelenlétéről vallja: ha a mennybe megy fel, ott van, és „ha a Seolba vetek ágyat, ott is jelen vagy”. A Seol sincs kívül Isten jelenlétén.',
                '👑 Isten hatalma — Isten jelen van a Seolban is'),
'Zsolt 141:7': ('A zsoltáros a megöltek sorsát így írja le: ahogy a szántáskor szétszóródik a föld, úgy szóródnak szét a csontjaik „a Seol torkában”. A Seol nyitott torokként fogadja a halottakat.',
                '🕳️ a Seol torka — a Seol mint elnyelő száj képe'),
'Péld 1:12': ('Az erőszakos bűntársak így csábítják a fiatalt: „Nyeljük el azokat, mint a sír elevenen”. A gonoszok a Seol elnyelő hatalmát akarják utánozni áldozataikon.',
              '📜 bölcsességi intés — a Seol elnyelő ereje a gonoszok szavában, intő példaként'),
'Péld 5:5': ('Az idegen asszonyról mondja az intelem: „Az ő lábai a halálra mennek, az ő léptei a sírba törekszenek.” Aki vele jár, a Seol felé halad.',
             '📜 bölcsességi intés — a parázna útja a Seolba vezet'),
'Péld 7:27': ('A csábító asszony házáról mondja a tanító: „Sírba vívő út az ő háza”, amely levisz a halál hajlékába. A ház küszöbe a Seolba vezető út kezdete.',
              '📜 bölcsességi intés — a ház, amely a Seolba vezető út'),
'Péld 9:18': ('A balgaság asszonyának vendégei nem tudják, hogy ott halottak vannak, és hogy meghívottai „a pokol mélyébe esnek”. A lakoma a Seol mélyén végződik.',
              '📜 bölcsességi intés — a balgaság hívása a Seol mélyére vezet'),
'Péld 15:11': ('A mondás szerint „A sír és a pokol az Úr előtt vannak”, mennyivel inkább az emberek szíve. A Seol és a pusztulás helye is nyitva áll az Úr előtt.',
               '👑 Isten hatalma — ha a Seol nyitva áll az Úr előtt, az emberi szív sem rejtőzhet el'),
'Péld 15:24': ('Az értelmes ember útja felfelé visz, „hogy eltávozzék a pokoltól, mely aláfelé van”. A bölcsesség az életre vezet, a Seoltól el.',
               '📜 bölcsességi intés — a bölcs út a Seoltól elvezet'),
'Péld 23:14': ('A tanító azt mondja a fiát fenyítő apának, hogy ha vesszővel megveri, „az ő lelkét a pokolból ragadod ki”. A nevelés itt a Seoltól óvja meg a gyermeket.',
               '🕊️ szabadulás a Seolból — a fegyelmezés a gyermeket a Seoltól menti meg'),
'Péld 27:20': ('„Mint a sír és a pokol meg nem elégednek”, úgy az ember szeme sem elégszik meg soha. A Seol telhetetlensége az emberi kívánság képe.',
               '🕳️ telhetetlenség — a soha meg nem telő Seol az emberi vágy mértéke'),
'Péld 30:16': ('A soha nem elégedő dolgok felsorolásában az első „A sír”, a meddő asszony, a víztől soha nem telő föld és a tűz mellett. A Seol a telhetetlenség példája.',
               '🕳️ telhetetlenség — a Seol a soha nem elégedő dolgok sorának élén'),
'Préd 9:12': ('A Prédikátor arra biztat, hogy amit lehet, most tegyen meg az ember, mert semmi cselekedet és bölcsesség „nincs a Seolban, a hová menendő vagy”. A Seolban a tett és a tudás megszűnik.',
              '🪦 a halottak helye — a Seolban megszűnik a munka és a tudás, ezért most kell cselekedni'),
'Én 8:6': ('A menyasszony a szerelem erejéről beszél: erős a szeretet, mint a halál, és „kemény, mint a sír a buzgó szerelem”. A Seol hajthatatlansága itt a szerelem erejének mértéke.',
           '💞 hasonlat — a Seol hajthatatlansága a szerelem erejét méri'),
'Ézs 5:14': ('Júda dőzsölő vezetőiről mondja a próféta, hogy „a sír kiszélesíti torkát és feltátja száját szertelen”, és leszállnak bele főemberei és zajongó sokasága. A Seol éhes torokként nyeli el a népet.',
             '🕳️ a Seol torka — ítélet: a Seol kitágult torka nyeli el a dőzsölőket'),
'Ézs 7:11': ('Ézsaiás felszólítja Áház királyt, hogy kérjen jelt az Úrtól, „kérj a mélységben vagy fent a magasban!” A héber szöveg itt a Seolt nevezi meg: a jel a legmélyebbtől a legmagasabbig bárhonnan jöhet.',
             '👑 Isten hatalma — a Seol mélye és az ég magassága között minden Isten jelének tere'),
'Ézs 14:9': ('A babiloni király elleni gúnydalban „Alant a sír megindul” az érkező miatt, és felriasztja a halottak árnyait, a föld egykori hatalmasait. A Seol lakói gúnyos fogadtatást készítenek a bukott uralkodónak.',
             '📯 prófétai gúnydal — a Seol felkél, hogy fogadja a bukott királyt'),
'Ézs 14:11': ('A gúnydal így folytatódik: „Kevélységed és lantjaid zengése a sírba szállt”, a király ágya férgek, takarója pondrók. A pompa a Seolban semmivé lesz.',
              '📯 prófétai gúnydal — a kevély uralkodó dicsősége a Seolba hull'),
'Ézs 14:15': ('Az égig törni akaró király ítélete: „Pedig a sírba szállsz alá, sírgödör mélységébe!” A legmagasabbra törőt a Seol legmélye várja.',
              '⬇️ felmagasztalás és megaláztatás — a gőgös a Seol mélyére zuhan; a minta Kapernaum ítéletében tér vissza'),
'Ézs 28:15': ('Jeruzsálem vezetői azzal kérkednek, hogy frigyet kötöttek a halállal, és „a sírral meg szövetséget csináltunk”. Azt hiszik, hogy a Seollal kötött egyezség megvédi őket a csapástól.',
              '⚖️ hamis biztonság — a Seollal kötött szövetség a vezetők önámítása'),
'Ézs 28:18': ('Az Úr válasza az, hogy „a sírral való szövetségtek meg nem áll”, és a halállal kötött frigyük eltöröltetik. A Seol felett az Úr dönt, nem az emberi egyezség.',
              '⚖️ hamis biztonság — a Seollal kötött szövetség érvénytelen'),
'Ézs 38:10': ('Ezékiás király betegségében azt mondja, élete delén kell lemennie „a sír kapuihoz”, megfosztva hátralévő éveitől. A Seol itt a korai halál fenyegetése.',
              '🪦 a halottak helye — a beteg király a Seol kapuja előtt áll'),
'Ézs 38:18': ('Meggyógyulása után Ezékiás azt mondja: „nem a sír dicsőít Téged”, és nem a halál magasztalja Istent. A dicséret az élők dolga, a Seolban elnémul.',
              '🪦 a halottak helye — a Seolban nincs dicséret, ezért a megmentett élet hálát ad'),
'Ézs 57:9': ('A hűtlen nép idegen királyokhoz küldött követeket és ajándékokat, és a próféta szerint „megaláztad magadat a sírig”. A Seol itt a megalázkodás legmélyebb pontja.',
             '⬇️ megaláztatás — a hűtlenség a Seolig alázza a népet'),
'Ez 31:15': ('Az Úr Isten a fáraót a libanoni cédrushoz hasonlítja, és azt mondja, hogy azon a napon, amelyen „sírba aláméne”, gyászba borította miatta a vizeket és a mező fáit. A Seolba szállás itt egy nagyhatalom bukása.',
             '📯 prófétai gúnydal — a cédrus-fáraó Seolba zuhanása gyászba borítja a teremtett világot'),
'Ez 31:16': ('A cédrus zuhanásának hangja megrengeti a nemzeteket, és az Úr így szól róla: „leszállítám őt a sírba” a verembe szállókkal együtt. A bukás a Seolban is visszhangzik, ahol a régebben elbukottak vigasztalódnak.',
             '📯 prófétai gúnydal — a bukás a Seolban is visszhangzik, a már ott lévők vigasztalódnak'),
'Ez 31:17': ('A fáraóval a szövetségesei is „alászállottak vele a sírba”, a fegyverrel megöltekhez. A nagyhatalom kísérete osztozik a sorsában.',
             '📯 prófétai gúnydal — a szövetségesek is a fáraóval együtt jutnak a Seolba'),
'Ez 32:21': ('A hősök hatalmasai „a sír közepéből” szólnak Egyiptomról, amely közéjük, a körülmetéletlenek és a fegyverrel megöltek közé száll le. A Seol itt a bukott népek közössége, ahol a halottak beszélnek.',
             '📯 prófétai gúnydal — a Seol lakói fogadják és megszólítják a bukott Egyiptomot'),
'Ez 32:27': ('A próféta szerint a bukott nép nem fekszik együtt a régi hősökkel, akik „hadiszerszámaikkal szálltak alá a sírba”, fegyverüket a fejük alá téve. A Seolban is különbség van a halottak között.',
             '📯 prófétai gúnydal — a Seolban is rang szerint fekszenek a halottak, a bukott nép a megvetettek közé jut'),
'Hós 13:14': ('Az Úr Efraim felől azt mondja: „Megváltom őket a Seol hatalmából! Megmentem őket a haláltól!”, majd magát a Seolt szólítja meg: „Hol van a te romlásod oh Seol?!” Pál az 1Kor 15:55-ben ezt a felkiáltást idézi a feltámadás diadalénekében.',
              '🎯 előkép — Isten győzelmi kérdése a Seol felett, amelyet az Újszövetség a feltámadásra alkalmaz'),
'Ámós 9:2': ('Az Úr kijelenti, hogy aki elől menekül, ha „a Seolba ássák is be magokat”, keze onnan is kiragadja őket, és ha az égbe hágnak fel, onnan is levonszolja őket. A Seol nem rejtekhely Isten ítélete elől.',
             '👑 Isten hatalma — a Seol sem véd meg Isten ítéletétől'),
'Hab 2:5': ('A kevély, rabló hatalomról mondja a próféta, hogy „tátja száját, mint a Seol”, és telhetetlen, mint a halál, magához ragad minden népet. A Seol telhetetlensége a hódító mohóságának képe.',
            '🕳️ telhetetlenség — a hódító mohósága olyan, mint a soha meg nem telő Seol'),
'Jón 2:3': ('Jónás a hal gyomrából mondja el imáját: „Nyomorúságomban az Úrhoz kiálték és meghallgata engem; a Seol torkából sikolték”. A Seol fenyegetéséből kiáltott az Úrhoz, és Isten meghallotta a szavát.',
            '🙏 kiáltás a Seol szorításából — a Seol torkából kiáltó próféta meghallgatást nyer'),
'ApCsel 2:27': ('Péter pünkösdkor a Zsolt 16:10-et idézi: „nem hagyod az én lelkemet a sírban”, és a zsoltár ígéretét Jézusra alkalmazza. A Károli itt sírnak fordítja azt a görög szót, amely a zsoltár Seoljának felel meg.',
                '🎯 beteljesedés — a Seolban nem maradó szent ígérete Krisztusra alkalmazva'),
'ApCsel 2:31': ('Péter kimondja, hogy Dávid előre látva szólt a Krisztus feltámadásáról: „az ő lelke nem hagyatott a sírban”, és teste sem látott rothadást. A halottak birodalma nem tarthatta fogva a Messiást.',
                '🎯 beteljesedés — a feltámadás mint a halottak birodalma fogságának megtörése'),
'Luk 16:23': ('A gazdag emberről és Lázárról szóló példázatban a gazdag „a pokolban” emeli fel a szemét, kínok között, és messziről látja Ábrahámot és Lázárt. Itt a halottak birodalma a halál utáni, tudatos szenvedés helye.',
              '⚖️ a gonoszok sorsa — a példázatban a halottak birodalma a halál utáni gyötrelem helye'),
'Jel 1:18': ('A feltámadott Krisztus mondja, hogy halott volt, és íme, örökké él, és „nálam vannak a pokolnak és a halálnak kulcsai”. A halottak birodalmának nyitása és zárása az ő hatalmában van.',
             '🗝️ Krisztus hatalma — a halottak birodalmának kulcsai a feltámadott Krisztusnál vannak'),
'Jel 6:8': ('A sárga lovon ülő lovas neve halál, és „a pokol követi vala azt”, hatalmat kapva, hogy a föld negyedrészén öljenek. Itt a halottak birodalma megszemélyesített hatalom, a halál kísérője.',
            '⚔️ megszemélyesítés — a halottak birodalma a halál kísérőjeként az ítélet eszköze'),
'Jel 20:13-14': ('Az utolsó ítéletkor „a halál és a pokol is kiadá a halottakat”, akik náluk voltak, és mindenkit cselekedetei szerint ítélnek meg. Utána a 14. vers szerint a pokol és a halál maga is a tűz tavába vettetik, és ez a második halál.',
                 '🔥 végső megszűnés — a halottak birodalma kiadja halottait, majd maga is megsemmisül'),
'Luk 10:15': ('Jézus Kapernaumnak mondja: „mely mind az égig felmagasztaltattál, a pokolig fogsz lealáztatni”. A gőgös város ítélete ugyanaz a mozgás, mint a babiloni királyé az Ézs 14:15-ben.',
              '⬇️ felmagasztalás és megaláztatás — az égig emelt gőg a halottak birodalmáig zuhan'),
'Mt 11:23': ('Máté evangéliuma ugyanezt az ítéletet hozza: Kapernaum, „a ki az égig felmagasztaltattál, a pokolig fogsz megaláztatni”, mert nem tért meg a csodák láttán. Az indoklásban Sodoma a mérce, amely ilyen csodák láttán megmaradt volna.',
             '⬇️ felmagasztalás és megaláztatás — a Lukács-hely párhuzama, Sodoma példájával kiegészítve'),
'Mt 16:18': ('Jézus Péternek mondja, hogy erre a kősziklára építi egyházát, és „a pokol kapui sem vesznek rajta diadalmat”. A halottak birodalmának kapui itt a halál hatalmát jelentik, amely az egyházat nem győzheti le.',
             '⛪ az egyház és a halál hatalma — más szerep, mint a többi helyen: nem a halottak helye, hanem a halál ereje, amely az egyházon nem győz'),
'1Kor 15:55': ('Pál a feltámadás diadalénekében kiált fel: „Halál! hol a te fullánkod? Pokol! hol a te diadalmad?” A Károli alapszövegében a második felkiáltás a halottak birodalmát szólítja meg; a kritikai szövegkiadások itt mindkét helyen a halált, θάνατε (thanate) olvassák.',
               '🏆 diadal a halál felett — a Hós 13:14 győzelmi kérdése a feltámadás bizonyosságában teljesedik'),
}

UJ_SOROK = {
    'Mt 16:18': dict(pardes_szint='Remez', karoli_szo='a pokol kapui'),
    '1Kor 15:55': dict(pardes_szint='Remez/Drash', karoli_szo='Pokol!'),
}
UJ_PROV = 'scope=manual | forras=F123 ALVIL-001 új cikk (a felhasználó határdöntése, 2026-11-02; jeloltek.tsv beépítve) | ts=' + TS

JELOLT_INDOK = {
    '2Móz 12:29': ('A gépi keresés a halálveszély és a kiáltás szavait egymás közelében találta meg, de a jelenet egyiket sem tartalmazza: '
                   'a „tömlöc” itt börtön, a halál az egyiptomi elsőszülötteké, és a fáraó nem az Úrhoz kiált, hanem Mózest és Áront hívatja. '
                   'A versben a Seol szava sem áll.'),
    'Zsolt 49:10': ('A gépi keresés a „sírgödör” és a „hív” szót találta meg, de a vers a gazdagok sorsáról szól, a „nevöket hangoztatják” '
                    'névadás, nem kiáltás, és a váltságot a zsoltár éppen tagadja. A versben a Seol szava sem áll; a zsoltár Seolt említő '
                    'két verse (49:15, 49:16) a motívum helye.'),
    'Zsolt 107:18': ('A halál kapujához közeledők az Úrhoz kiáltanak, és ő kiszabadítja őket (107:19–20), de a versben a Seol szava nem áll. '
                     'A hely a halálveszélyben elmondott imádság tágabb körébe tartozik, nem a halottak birodalmának motívumába.'),
}

NEGATIV = ('A versben a héber szövegben a שְׁאוֹל (seól), az Újszövetségben a Károli alapszövege (TR) szerint a ᾍδης (hadész) szó áll; ahol a kritikai kiadások ettől eltérnek, a lap jelöli (1Kor 15:55). Ahol a Károli sírt, koporsót, poklot vagy mélységet ír, de az eredetiben más szó áll (a temetkezési sír, a verem, a pusztulás helye, a görög tartarosz), az nem tartozik ide; a תְּהוֹם (tehóm) és az ἄβυσσος (abüsszosz) kozmikus mélysége sem.')  # DT-F123p: a felhasználó jóváhagyásával, 2026-11-02
FOLERENDELT = 'a halál és a túlvilág általában, a halottak birodalmának megnevezése nélkül'
CIMKE_2A = 'a gonoszok sorsa; az igaz félelme és szabadulása'
TANITOI = ('Ehhez a motívumhoz nevesített tanítói egyezést még nem kerestünk; a hiány nincs kitöltve.')


def nyit(ut):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers.split(nl), nl


def ir(ut, sorok, nl):
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


def fej_ix(sorok, kezd):
    i = next(k for k, s in enumerate(sorok) if s.startswith(kezd))
    return i, {n: j for j, n in enumerate(sorok[i].split('\t'))}


def kontroll(regi, uj, erintett):
    a = [s for k, s in enumerate(regi) if k not in erintett]
    b = [s for k, s in enumerate(uj) if k not in erintett]
    if a != b:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')


def elofordulasok():
    ut = os.path.join(GY, 'adat', 'elofordulasok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    uj = list(sorok)
    erintett, latott = set(), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k <= fi or m[0] != 'ALVIL-001':
            continue
        ige = m[ix['igehely']]
        assert ige in P, ige
        m[ix['kapcsolodas']], m[ix['funkcio']] = P[ige]
        uj[k] = '\t'.join(m)
        erintett.add(k)
        latott.add(ige)
        utolso, minta = k, m
    assert len(latott) == 72, len(latott)
    kontroll(sorok, uj, erintett)
    hozza = []
    for ige, d in UJ_SOROK.items():
        assert ige not in latott
        m = [''] * len(ix)
        for mezo in ix:
            m[ix[mezo]] = ''
        m[ix['id']] = 'ALVIL-001'
        m[ix['igehely']] = ige
        m[ix['kapcsolodas']], m[ix['funkcio']] = P[ige]
        m[ix['pardes_szint']] = d['pardes_szint']
        for mezo in ('gerinc_elem', 'strong', 'lexikon_entry_id'):
            m[ix[mezo]] = 'G0086'
        m[ix['lexikon_szotar']] = 'Thayer'
        m[ix['jelentes_szam']] = '2'
        m[ix['karoli_szo']] = d['karoli_szo']
        m[ix['azonositas_modja']] = 'tartalom-alapú'
        m[ix['megbizhatosag']] = 'magas'
        m[ix['proveniencia']] = UJ_PROV
        m[ix['igazolas']] = minta[ix['igazolas']] if minta[ix['strong']] == 'G0086' else 'nincs'
        hozza.append('\t'.join(m))
    uj = uj[:utolso + 1] + hozza + uj[utolso + 1:]
    ir(ut, uj, nl)
    print('elofordulasok.tsv: 72 sor próza, 2 új sor')


def jeloltek():
    ut = os.path.join(GY, 'adat', 'jeloltek.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and m[0] == 'ALVIL-001' and m[ix['igehely']] in JELOLT_INDOK and m[ix['jelolt_tipus']] == 'elofordulas':
            assert m[ix['dontes']] == 'elutasítva'
            m[ix['indoklas']] = JELOLT_INDOK[m[ix['igehely']]]
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == 3, erintett
    kontroll(sorok, uj, erintett)
    ir(ut, uj, nl)
    print('jeloltek.tsv: 3 indoklás')


def motivumok():
    ut = os.path.join(GY, 'adat', 'motivumok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and m[0] == 'ALVIL-001':
            m[ix['negativ_kriterium']] = NEGATIV
            m[ix['folerendelt_fogalom']] = FOLERENDELT
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == 1
    kontroll(sorok, uj, erintett)
    ir(ut, uj, nl)
    print('motivumok.tsv: negatív kritérium, fölérendelt fogalom')


def cimke():
    ut = os.path.join(GY, 'adat', 'szotar_szakasz_cimke.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'szotar\t')
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and m[:3] == ['BDB', 'H7585', '-/2/a']:
            m[ix['cimke_hu']] = CIMKE_2A
            m[ix['proveniencia']] = ('scope=manual | forras=F123 ALVIL-001 új cikk (a BDB 2.a teljes szövege: gonoszok; '
                                     'az igazak rettegnek tőle; a megszabadulás belőle áldás; lap-átvilágítás 2026-11-02, A3) | ts=' + TS)
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == 1
    kontroll(sorok, uj, erintett)
    ir(ut, uj, nl)
    print('szotar_szakasz_cimke.tsv: H7585 2.a')


def res():
    ut = os.path.join(GY, 'adat', 'res_forras.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and m[0] == 'ALVIL-001' and m[ix['res']] == 'tanitoi':
            m[ix['tanulmany']] = TANITOI
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == 1
    kontroll(sorok, uj, erintett)
    ir(ut, uj, nl)
    print('res_forras.tsv: tanitoi')


if __name__ == '__main__':
    elofordulasok()
    jeloltek()
    motivumok()
    cimke()
    res()
