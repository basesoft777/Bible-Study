# -*- coding: utf-8 -*-
"""F123 HAMART-001 új cikk, U3 — a lap olvasói adatmezői nulláról, a szótári gerinc és a határmezők.

Ír (a nem érintett sorok egyezésének kontrolljával, split('\\t'), CLAUDE.md):
  - adat/elofordulasok.tsv: a HAMART-001 52 sorának `kapcsolodas`, `funkcio`, `karoli_szo` mezője (kerek mondat;
    „címke — magyarázat”), a szótári gerinc mezői (`lexikon_szotar`, `lexikon_entry_id`, `jelentes_szam`), a DT593
    következménye (1Móz 6:5 → tematikus, 1Móz 8:21 → H0127), és 8 új sor (DT-F123ha);
  - adat/motivumok.tsv: `negativ_kriterium`, `folerendelt_fogalom` olvasói nyelven, `forras_study`;
  - adat/szotar_szakasz_cimke.tsv, adat/lexikon_hivatkozasok.tsv: a gerinc szakaszcímkéi és kulcssorai;
  - adat/res_forras.tsv: a rések a `motivumok/HAMART-001.md`-re mutatnak;
  - adat/funkcio_kapcsolok.tsv: SZOTARI_GERINC HAMART-001 `kivetel` → `aktiv` (X.K).
Szerző: claude-opus-5-5, egy kézből (F123_MIGRACIO2_BRIEF.md 2a, U3). A régi `kapcsolodas` csak alapanyag
(archívumban: archivum/HAMART-001/HAMART-001_1a_proza_regi.tsv). Döntés: DT-F123ha, DT593.
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = 'HAMART-001'
TS = '2026-11-05'
FORRAS = 'F123 HAMART-001 új cikk, U3 (claude-opus-5-5; a jeloltek.tsv beépített sora, DT-F123ha)'
PROV = 'scope=manual | forras=' + FORRAS + ' | ts=' + TS

B, T = 'BDB', 'Thayer'


def p(k, f, karoli, strong, szotar, entry, jsz, gerinc=None, pardes=None):
    return dict(k=k, f=f, karoli=karoli, strong=strong, szotar=szotar, entry=entry, jsz=jsz, gerinc=gerinc,
                pardes=pardes)


P = {
'1Móz 3:14': p('Az Úr Isten a kígyónak mondja ki az első átkot: „átkozott légy minden barom és minden mezei vad között”. '
               'A Biblia itt használja először az átok igéjét (árar), és a sor a kígyóval kezdődik, mielőtt a földre '
               'és az emberre lépne.',
               '🌱 első kimondás — az átok első kimondása, a kígyóra; a lánc minden későbbi tagja erre a szóra épül',
               'átkozott', 'H0779', B, 'H0779', 'Qal'),
'1Móz 3:16': p('Az asszonynak szóló ítéletben áll először a fájdalom szava (itzávón): „Felette igen megsokasítom '
               'viselősséged fájdalmait”. A szó az egész Ószövetségben csak háromszor fordul elő, mindháromszor ebben a '
               'láncban (1Móz 3:16, 3:17, 5:29).',
               '🔗 láncszem — a fájdalom szava az asszonyra; a szó mindhárom előfordulása a láncban áll',
               'fájdalmait', 'H6093', B, 'H6093', 'tagolatlan'),
'1Móz 3:17': p('Az ember bűne miatt az átok nem az emberre, hanem a földre száll: „Átkozott legyen a föld te miattad, '
               'fáradságos munkával élj belőle”. Ebben a versben áll együtt először az átok (árar), a föld (adámá) és a '
               'fáradság (itzávón) szava; a következmény itt lép ki az elkövetőből a környezetébe.',
               '🔑 kulcsvers — az átok a földre lép; az átok, a föld és a fáradság szava először áll együtt',
               'föld', 'H0127', B, 'H0127', '1'),
'1Móz 3:18': p('Az átkozott föld terméke a tövis és a bogáncs: „Töviset és bogácskórót teremjen tenéked”. A héber '
               'szópár (kóc vedardar) az Ószövetségben csak még egyszer áll együtt (Hós 10:8), a görög fordítás szavait '
               'pedig a Zsid 6:8 veszi át.',
               '🔗 láncszem — az átok látható jele a föld termésén; a szópár később szó szerint visszatér',
               'Töviset', 'H6975', B, 'H6975', '1'),
'1Móz 3:19': p('Az ember a földből vétetett, és oda tér vissza: „míglen visszatérsz a földbe, mert abból vétettél”. A föld '
               'itt az anyag, amelyből az ember lett, ezért a halála is a földhöz köti; az átok a földön át az ember '
               'életének végét is érinti.',
               '🔗 láncszem — a föld mint az ember anyaga és sírja; az átok a halálig ér',
               'földbe', 'H0127', B, 'H0127', '3'),
'1Móz 3:23': p('Isten kiküldi az embert az Éden kertjéből, „hogy mívelje a földet, a melyből vétetett vala”. Az ember ettől '
               'kezdve azt a földet műveli, amely miatta átkozott; a kiűzetés így ahhoz a földhöz köti, amelyből vétetett.',
               '🔗 láncszem — a kiűzetés az átkozott földhöz köti az embert',
               'földet', 'H0127', B, 'H0127', '1'),
'1Móz 4:2-3': p('Kain „földmívelő” lesz, és „a föld gyümölcséből” visz ajándékot az Úrnak. Az átkozott föld itt a következő '
                'nemzedék munkájának terepe, és ugyanez a föld lesz a testvérgyilkosság színtere.',
                '🔗 láncszem — az átkozott föld a következő nemzedéken; a testvéri viszály színtere',
                'föld', 'H0127', B, 'H0127', '1'),
'1Móz 4:7': p('Isten Kaint figyelmezteti: „a bűn az ajtó előtt leselkedik, és reád van vágyódása; de te uralkodjál rajta.” '
              'Itt áll a Bibliában először a bűn szava (chattát), leselkedő hatalomként, amely még a küszöbön áll, és '
              'amelyen az ember még uralkodhat.',
              '🚪 küszöb — a bűn szavának első előfordulása, még az ajtó előtt; a lánc itt még megállítható',
              'bűn', 'H2403', B, 'H2403', '1'),
'1Móz 4:10-11': p('Ábel vére „kiált én hozzám a földről”, és Isten kimondja Kainra: „átkozott légy e földön”. Az átok most '
                  'már nem a földre, hanem a személyre száll, a föld felől; ugyanaz a két szó, az átok és a föld áll itt, '
                  'mint az 1Móz 3:17-ben, felcserélt szerepben.',
                  '🔥 fokozás — az átok a személyre száll, a föld felől; a 3:17 két szava felcserélt szerepben',
                  'átkozott', 'H0779', B, 'H0779', 'Qal'),
'1Móz 4:12': p('A föld megtagadja Kaintól a termést: „Mikor a földet míveled, ne adja az többé néked az ő termő erejét”. Ami '
               'az 1Móz 3:17-ben fáradság volt, az itt teljes meddőség, és a földművesből „bujdosó és vándorló” lesz.',
               '🔗 láncszem — a föld megtagadja termését; a büntetés a 3:17-19-nél súlyosabb',
               'földet', 'H0127', B, 'H0127', '1'),
'1Móz 4:14': p('Kain panaszában a büntetés kiűzetés: „Ímé elűzöl engem ma e földnek színéről”. A föld színéről való elűzés '
               'itt még egy emberre szól; az 1Móz 6:7-ben ugyanez a fordulat az egész emberiségre kimondott ítélet lesz.',
               '🔗 láncszem — kiűzetés a föld színéről; a fordulat az özönvíz ítéletében tér vissza',
               'földnek színéről', 'H0127', B, 'H0127', '4'),
'1Móz 5:29': p('Lámek fia születésekor egy mondatban idézi vissza a lánc három szavát: Noé megvigasztal „kezünk terhes '
               'fáradozásában e földön, melyet megátkozott az Úr.” A fáradság (itzávón), a föld (adámá) és az átok (árar) '
               'itt együtt áll, mint az 1Móz 3:17-ben, és Lámek a terhet vigasztalásra váró állapotként nevezi meg.',
               '🔄 forgópont — a lánc három szava egy mondatban; az átok állapot, amelyből vigasztalást várnak',
               'fáradozásában', 'H6093', B, 'H6093', 'tagolatlan'),
'1Móz 6:5': p('Az Úr látja, „hogy megsokasult az ember gonoszsága a földön, és hogy szíve gondolatának minden alkotása '
              'szüntelen csak gonosz.” A bűn itt már nem a küszöbön leselkedő hatalom (1Móz 4:7), hanem az ember belső, '
              'állandó állapota; a vers a lánc szavai nélkül áll a motívumban, mint a diagnózis, amelyre az özönvíz '
              'ítélete felel.',
              '🔍 tematikus, nem lexikai — a bűn belső, egyetemes állapottá válik; erre felel a 6:7 és a 6:13 ítélete',
              'gonosz', 'H7451', B, 'H7451', '10.c', gerinc='tematikus:1Móz 6:5'),
'1Móz 6:7': p('Isten kimondja: „Eltörlöm az embert, a kit teremtettem, a földnek színéről”. A föld színéről való eltörlés, '
              'amely Kainnál egy ember elűzése volt (1Móz 4:14), itt az egész élővilágra szól: az emberre, a barmokra, a '
              'csúszó-mászókra és az ég madaraira.',
              '🌍 egyetemes ítélet — a föld színéről való eltörlés kimondása; az özönvíz-elbeszélés ezt hajtja végre',
              'földnek színéről', 'H0127', B, 'H0127', '4'),
'1Móz 6:11': p('A romlás most már a földé: „A föld pedig romlott vala Isten előtt és megtelék a föld erőszakoskodással.” '
               'Itt áll először együtt a romlás igéje (sáchat) és az erőszak (chámász), a megtelés igéjével; a lánc ettől '
               'a mondattól a romlás és az erőszak szavain halad tovább.',
               '🔗 láncszem — a föld megromlik és megtelik erőszakkal; a romlás és az erőszak szavának első együttállása',
               'romlott', 'H7843', B, 'H7843', "Nif'ál"),
'1Móz 6:12': p('Isten a földre tekint, „és ímé meg vala romolva, mert minden test megrontotta vala az ő útát a földön.” '
               'Ugyanaz az ige kétszer áll: a föld megromlott, mert minden test megrontotta az útját; a romlás így az '
               'egész emberiség tette.',
               '🌍 egyetemes romlás — minden test megrontotta útját; a Zsoltárok ezt az igealakot veszik át',
               'megrontotta', 'H7843', B, 'H7843', "Hif'íl 2"),
'1Móz 6:13': p('Isten Noénak mondja: „a föld erőszakoskodással telt meg általok: és ímé elvesztem őket a földdel egybe.” '
               'Az ítélet igéje ugyanaz, mint a romlásé az előző versben: amit az ember a földdel tett, azt teszi Isten '
               'az emberrel, és a büntetés a bűn formáját követi.',
               '⚖️ tükörítélet — Isten ugyanazzal az igével felel, amellyel az ember a földet megrontotta',
               'erőszakoskodással', 'H2555', B, 'H2555', 'tagolatlan'),
'1Móz 6:17': p('Isten bejelenti az özönvizet, „hogy elveszessek minden testet, a melyben élő lélek van az ég alatt”. Az '
               'elvesztés igéje ugyanaz a romlás-ige (sáchat), amely a 6:11-12-ben az ember tettét nevezte meg; az '
               'özönvíz célja a megromlott föld elvesztése.',
               '🌊 özönvíz — az ítélet célja ugyanazzal az igével, mint az ember romlása',
               'elveszessek', 'H7843', B, 'H7843', "Pi'él 1"),
'1Móz 7:4': p('Isten hét nappal az özönvíz előtt megismétli a 6:7 szavát: „eltörlök a föld színéről minden állatot, melyet '
              'teremtettem.” A föld színéről való eltörlés itt már nem szándék, hanem napra kitűzött ítélet.',
              '🌊 özönvíz — a 6:7 kimondásának bejelentése, ugyanazzal az igével és fordulattal',
              'föld színéről', 'H0127', B, 'H0127', '4', pardes='Peshat'),
'1Móz 7:23': p('Az elbeszélés rögzíti a végrehajtást: „eltörle az Isten minden állatot, a mely a föld színén vala, az '
               'embertől a baromig”. A 6:7 felsorolása tér itt vissza, és a vers végén megnevezi, aki megmarad: „csak Noé '
               'marada meg”.',
               '🌊 özönvíz — a 6:7 ítéletének végrehajtása; egyedül Noé marad meg',
               'föld színén', 'H0127', B, 'H0127', '4', pardes='Peshat'),
'1Móz 8:21': p('Az özönvíz után az Úr megígéri: „Nem átkozom meg többé a földet az emberért”. A héberben itt nem az átok '
               'igéje (árar), hanem egy másik ige (qalal) áll, és az indoklás ugyanaz, mint a 6:5-ben: az ember szívének '
               'gondolata gonosz. Az ígéret a földet védi, az ember szívét nem változtatja meg, és Lámek vigasztalás-várását '
               '(1Móz 5:29) így csak részben teljesíti.',
               '⏸️ megállás — az ígéret a föld további átkát zárja ki, más igével; a szív állapota változatlan',
               'földet', 'H0127', B, 'H0127', '1', gerinc='H0127'),
'1Móz 9:11': p('Isten szövetséget köt: „soha sem lesz többé özönvíz a földnek elvesztésére.” Az elvesztés igéje (sáchat) itt '
               'tagadva áll: a szövetség éppen azt zárja ki, amit a 6:17 bejelentett.',
               '🤝 szövetség — a romlás-ige tagadva; a szövetség kizárja a föld újabb elvesztését',
               'elvesztésére', 'H7843', B, 'H7843', "Pi'él 1"),
'1Móz 9:15': p('A szivárvány-szövetség jeleként Isten megemlékezik, és „nem lesz többé a víz özönné minden testnek '
               'elvesztésére.” A tagadott elvesztés itt minden testre szól, ugyanarra a körre, amely a 6:12 szerint '
               'megrontotta az útját.',
               '🤝 szövetség — a tagadás minden testre szól, a 6:12 körére',
               'elvesztésére', 'H7843', B, 'H7843', "Pi'él 1"),
'1Móz 9:25': p('Az özönvíz után az átok szava újra elhangzik, most Noé szájából: „Átkozott Kanaán!” A lánc nem szakad meg a '
               'szövetséggel: az ígéret a föld átkát zárta ki, az ember szavában az átok tovább él. A motívum a verset '
               'csak e szó miatt veszi fel, a Khám vétkének értelmezése nélkül.',
               '🔁 újraindulás — az átok szava az özönvíz után újra elhangzik',
               'Átkozott', 'H0779', B, 'H0779', 'Qal'),
'1Móz 12:3': p('Ábrám elhívásában a lánc megfordul: „a ki téged átkoz, megátkozom azt: és megáldatnak te benned a föld '
               'minden nemzetségei.” Az átok szava itt az áldás keretében áll, és a föld (adámá) nemzetségei, amelyek az '
               'átok terhét hordozták, áldást kapnak.',
               '🔄 megfordítás — az átok az áldás keretébe kerül; a föld nemzetségei áldást kapnak',
               'megátkozom', 'H0779', B, 'H0779', 'Qal'),
'5Móz 27:15-26': p('A léviták tizenkétszer mondják ki a nép előtt: „Átkozott”, és a nép mindegyikre ámennel felel. A Genezis '
                   'átok-kimondása itt törvényi, liturgikus formulává lesz, amely a szövetség megszegőjét sújtja.',
                   '📜 törvényi formula — tizenkét átok-kimondás a szövetség megszegőjére; a Gal 3:10 innen idéz',
                   'Átkozott', 'H0779', B, 'H0779', 'Qal'),
'5Móz 28:16-19': p('A szövetség átkai négyszer mondják ki: „Átkozott”, a városban és a mezőn, a kosáron és a teknőn, a méh '
                   'gyümölcsén és a föld termésén. A négy átok az áldások négy mondatának (5Móz 28:3-6) tükörképe, és a föld '
                   'termését is eléri.',
                   '📜 törvényi formula — négy átok az áldások tükörképeként; a föld termése is alá esik',
                   'Átkozott', 'H0779', B, 'H0779', 'Qal'),
'Jer 17:5': p('Az Úr kimondja: „Átkozott az a férfi, a ki emberben bízik és testbe helyezi erejét”. Az átok-formula itt '
              'egyéni döntésre szól: arra, aki az Úr helyett emberre támaszkodik.',
              '📜 formula egyénre — az átok a bizalom rossz irányára szól',
              'Átkozott', 'H0779', B, 'H0779', 'Qal'),
'Zsolt 14:1': p('A zsoltár a balgatag ember tagadásáról szól, és ítéletet mond: „Megromlottak, útálatosságot cselekedtek; '
                'nincs, a ki jót cselekedjék.” A „Megromlottak” ugyanaz a héber igealak, mint az 1Móz 6:12-ben, és a '
                'folytatásban az Úr, mint ott, letekint az emberekre: a zsoltár a Genezis egyetemes romlás-mondatát '
                'ismétli.',
                '🌍 egyetemes romlás — az 1Móz 6:12 igealakja a zsoltárban; senki sincs kivétel',
                'Megromlottak', 'H7843', B, 'H7843', "Hif'íl 2"),
'Zsolt 53:2': p('A 14. zsoltár párja ugyanezt mondja: „Megromlottak és útálatos hamisságot cselekedtek, nincs a ki jót '
                'cselekedjék.” A kettős előfordulás a romlás-mondatot a Zsoltárok könyvében kétszer is rögzíti.',
                '🌍 egyetemes romlás — a 14. zsoltár párja, ugyanazzal az igealakkal',
                'Megromlottak', 'H7843', B, 'H7843', "Hif'íl 2"),
'Ez 7:23': p('Ezékiel láncot készíttet, „mert a föld tele van véres ítélettel, és a város tele van erőszakossággal.” A '
             'megtelés és az erőszak szókapcsolata (málé chámász) az 1Móz 6:11 és 6:13 mondatát viszi át Jeruzsálemre, '
             'és a következmény itt is ítélet.',
             '⚖️ visszhang — a föld megtelése erőszakkal Jeruzsálemre alkalmazva',
             'erőszakossággal', 'H2555', B, 'H2555', 'tagolatlan'),
'Ez 8:17': p('Az Úr megmutatja a prófétának, hogy Júda háza a bálványimádáson túl „még a földet is betöltik '
             'erőszakossággal”. A mondat a földet és az erőszakot ugyanúgy köti össze, mint az 1Móz 6:11.',
             '⚖️ visszhang — Júda háza megtölti a földet erőszakkal, mint az özönvíz előtti nemzedék',
             'erőszakossággal', 'H2555', B, 'H2555', 'tagolatlan'),
'Ez 12:19': p('Ezékiel Izrael földjéről mondja, „hogy pusztaságra vetkőzzék földje bőségéből minden lakói álnoksága '
              'miatt.” A héberben az erőszak (chámász), a föld (adámá) és a teljesség (melóá, a megtelés igéjének '
              'tövéből) szava áll együtt: a föld a lakói erőszaka miatt üresedik ki, ahogy az 1Móz 6:11-13-ban a '
              'megtelt földet éri az ítélet.',
              '⚖️ visszhang — az erőszakkal megtelt föld kiürül; az 1Móz 6:11-13 szerkezete Izraelre',
              'álnoksága', 'H2555', B, 'H2555', 'tagolatlan', pardes='Remez'),
'Ez 28:16': p('Tírusz fejedelméről mondja az Úr: „Kereskedésed bősége miatt belsőd erőszakossággal telt meg és vétkezél”. '
              'A megtelés és az erőszak szókapcsolata itt egy uralkodóra szól, mellette áll a vétek, és az ítélet a '
              'bukás.',
              '⚖️ visszhang — egy uralkodó belseje telik meg erőszakkal; a vétek és a bukás együtt',
              'erőszakossággal', 'H2555', B, 'H2555', 'tagolatlan'),
'Zsolt 74:20': p('A zsoltáros Istent a szövetségre emlékezteti, „mert telve vannak e földnek rejtekhelyei zsaroló '
                 'tanyákkal.” A héberben itt is az erőszak (chámász) és a megtelés igéje áll: a megtelt föld a panasz '
                 'tárgya, és a zsoltáros a szövetségre hivatkozva kér változást.',
                 '🙏 panasz — a megtelt föld a szövetségre hivatkozó ima tárgya',
                 'zsaroló', 'H2555', B, 'H2555', 'tagolatlan'),
'Mik 6:12': p('Mikeás Jeruzsálem gazdagjairól mondja: „a gazdagok megtöltöztek köztök ragadománynyal”. A „ragadomány” a '
              'héberben az erőszak szava (chámász), mellette a megtelés igéje áll, és a következő vers a csapást mondja ki.',
              '⚖️ visszhang — a gazdagok telnek meg erőszakkal; a csapás a következő versben',
              'ragadománynyal', 'H2555', B, 'H2555', 'tagolatlan'),
'Sof 1:2-3': p('Sofóniás könyve az özönvíz ítéletének szavaival kezdődik: „mindent elvesztek e föld színéről”, „Elvesztek '
               'embert és barmot; elvesztem az ég madarait”. A próféta az 1Móz 6:7 felsorolását és a föld színéről való '
               'eltörlés fordulatát egyetemes ítéletként mondja ki, és a 3. vers végén megismétli: „az embert is kiirtom a '
               'föld színéről”.',
               '🌍 egyetemes ítélet — az 1Móz 6:7 felsorolása és fordulata a próféta ítéletében',
               'föld színéről', 'H0127', B, 'H0127', '4', pardes='Remez'),
'Sof 1:9': p('Az Úr megfenyíti azokat, „a kik erőszakkal és csalárdsággal töltik meg az ő uroknak házát.” A megtelés és az '
             'erőszak szókapcsolata itt egy ház megtöltésére szól, abban a fejezetben, amely a föld színéről való '
             'eltörlést hirdeti (Sof 1:2-3).',
             '⚖️ visszhang — a ház megtöltése erőszakkal, a föld színéről szóló ítélet közelében',
             'erőszakkal', 'H2555', B, 'H2555', 'tagolatlan'),
'Hab 2:8': p('Habakuk a fosztogató hatalomnak mondja: „kifosztanak téged mind a többi népek az emberek véréért, és az '
             'országok, városok és minden bennök lakozók ellen való erőszaktételért.” Az erőszak itt visszatér arra, aki '
             'elkövette: a fosztogatót kifosztják.',
             '🔁 visszatérés — az erőszak az elkövetőre száll vissza',
             'erőszaktételért', 'H2555', B, 'H2555', 'tagolatlan'),
'Hab 2:17': p('A jövendölés folytatódik: „a libanoni erőszakoskodás gyászba borít téged”. Az erőszak, amelyet a hatalom a '
              'Libanonon és az országon elkövetett, most őt borítja be; a megtorlás ugyanabban a formában érkezik, mint a '
              'bűn.',
              '🔁 visszatérés — az elkövetett erőszak borítja be az elkövetőt',
              'erőszakoskodás', 'H2555', B, 'H2555', 'tagolatlan'),
'Jón 3:8': p('Ninive királya elrendeli: „térjen meg kiki az ő gonosz útáról és az erőszakosságból, a mely az ő kezökben '
             'van!” Ez az egyetlen hely a láncban, ahol egy nép az erőszakból megtérve elkerüli a kimondott pusztulást: '
             'a fejezet vége szerint Isten nem bocsátja rájuk a veszedelmet.',
             '🔄 megtérés — az egyetlen hely, ahol az erőszakból megtérő nép elkerüli az ítéletet',
             'erőszakosságból', 'H2555', B, 'H2555', 'tagolatlan'),
'Ézs 60:18': p('Ézsaiás a megváltott városnak ígéri: „Nem hallatik többé erőszaktétel földeden, pusztítás és romlás '
               'határaidban”. A hallás és az erőszak szókapcsolata (sámá chámász) itt tagadva áll: ami Jeremiásnál a '
               'város bűnének hangja volt, az a megváltott városban többé nem hallatszik.',
               '🔄 megfordítás — az erőszak hangja megszűnik; a lánc végidei visszavonása',
               'erőszaktétel', 'H2555', B, 'H2555', 'tagolatlan'),
'Jer 6:7': p('Jeruzsálemről mondja a próféta: „erőszakosság és önkény hallatszik benne”. A város úgy őrzi gonoszságát, mint '
             'a kút a vizét, és az erőszak hangja Isten előtt szüntelen; az ítélet ennek a hangnak felel.',
             '⚖️ visszhang — az erőszak hangja hallatszik a városban',
             'erőszakosság', 'H2555', B, 'H2555', 'tagolatlan'),
'Jer 51:25': p('Az Úr Babilon ellen fordul, a „romlásnak hegye” ellen, „a ki az egész földet megrontottad”. A romlás igéje '
               '(sáchat) és az egész föld együtt az 1Móz 6:11-13 mondata, és ugyanez a vád tér vissza a Jel 19:2-ben, ahol '
               'a nagy parázna „a földet megrontotta az ő paráznaságával”.',
               '🌍 egyetemes romlás — Babilon az egész földet rontja meg; a Jel 19:2 előképe',
               'megrontottad', 'H7843', B, 'H7843', "Hif'íl 1", pardes='Remez'),
'Jer 51:46': p('Babilon bukása előtt hír hallatszik, „hogy erőszakosság van a földön, uralkodó tör uralkodóra!” A föld és az '
               'erőszak szava itt a hallás igéjével áll együtt, és a hír a birodalom összeomlását vetíti előre.',
               '⚖️ visszhang — az erőszak híre Babilon bukásának előjele',
               'erőszakosság', 'H2555', B, 'H2555', 'tagolatlan'),
'Hab 1:2': p('Habakuk panasza így kezdődik: „Kiáltozom hozzád az erőszak miatt, és nem szabadítasz meg!” Itt a próféta kiált '
             'az erőszak miatt, és úgy érzi, Isten nem hallja; a szókapcsolat a panasz oldaláról mutatja a láncot.',
             '🙏 panasz — a próféta kiált az erőszak miatt',
             'erőszak', 'H2555', B, 'H2555', 'tagolatlan'),
'Hós 10:8': p('Hóseás Izrael bálványos magaslatairól mondja: „Tövis és bogácskóró növi be oltáraikat”, és ugyanez a vers „az '
              'Izráel vétke” szavakkal a bűnt is megnevezi. Az 1Móz 3:18 szópárja (kóc vedardar) az Ószövetségben csak itt '
              'tér vissza, és itt is a bűn következménye a föld termésén.',
              '🔗 visszatérő szópár — a genezisi tövis és bogáncs a bűn helyén nő',
              'Tövis', 'H6975', B, 'H6975', '1', pardes='Remez'),
'Mal 3:11': p('Malakiás könyvében a 3:9 átka után az Úr megígéri, hogy megdorgálja a kártevőt, „és nem veszti el földetek '
              'gyümölcsét”. A héberben itt a romlás igéje (sáchat) és a föld (adámá) áll, vagyis a föld termésének ígérete '
              'az 1Móz 3:17-18 és 4:12 átkának megfordítása.',
              '🔄 megfordítás — a föld termését többé nem rontja meg a kártevő',
              'veszti el', 'H7843', B, 'H7843', "Hif'íl 1", pardes='Remez'),
'Ézs 24:5-6': p('Ézsaiás a földről mondja: „A föld megfertőztetett lakosai alatt”, és „Ezért átok emészti meg a földet”. A '
                'föld, az átok és a lakók hármasa az 1Móz 3:17 szerkezete, de a héberben itt az átok más szava (álá) áll; a '
                'hely ezért tematikus, nem lexikai kapcsolatként tartozik ide.',
                '🔍 tematikus, nem lexikai — a föld, az átok és a lakók hármasa más átok-szóval',
                'átok', 'H0423', B, 'H0423', '3'),
'Hós 4:1-3': p('Hóseás az Úr perét hirdeti a föld lakóival, felsorolja bűneiket, és kimondja: „Azért búsul a föld és '
               'elerőtlenül minden, a mi azon lakik”. A lakók bűne a föld sorvadását hozza, ahogy a Genezisben, de a lánc '
               'szavai nélkül; a hely tematikus, nem lexikai kapcsolatként tartozik ide.',
               '🔍 tematikus, nem lexikai — a lakók bűne miatt búsul a föld',
               'búsul', 'H0056', B, 'H0056', 'Qal'),
'Róm 8:20-22': p('Pál szerint „a teremtett világ hiábavalóság alá vettetett”, de azzal a reménységgel, „hogy maga a teremtett '
                 'világ is megszabadul a rothadandóság rabságától”. A rothadandóság (φθορά, fthora) a görög Ószövetség '
                 'romlás-szócsaládjából való, és a mondat azt mondja ki, hogy a föld átka mint állapot nem szűnt meg: az '
                 'egész teremtett világ együtt nyög.',
                 '⏳ állapot — a teremtett világ még a romlás rabságában, de szabadulásra vár',
                 'rothadandóság', 'G5356', T, 'G5356', '1'),
'Gal 3:10': p('Pál az 5Móz 27:26-ot idézi: „Átkozott minden, a ki meg nem marad mindazokban, a mik megirattak a törvény '
              'könyvében”. A görög szó (ἐπικατάρατος, epikataratosz) ugyanaz, amellyel a görög Ószövetség az 1Móz 3:17 '
              'átkát fordítja; a törvény átka így a genezisi átok nyelvén szól.',
              '📜 törvényi formula — az 5Móz 27:26 átka a Genezis görög szavával',
              'Átkozott', 'G1944', T, 'G1944', 'fej'),
'Gal 3:13': p('Pál kimondja: „Krisztus váltott meg minket a törvény átkától, átokká levén érettünk”. Az 5Móz 21:23 '
              'idézetében a görög Ószövetség szavát a Genezis átok-szavára (ἐπικατάρατος) cseréli: „Átkozott minden, a ki '
              'fán függ”, így Krisztus ugyanazt az átkot veszi magára, amely a 3:17 óta a földön és az emberen van.',
              '🔄 megváltás — Krisztus magára veszi az átkot; az idézet a Genezis szavára hangolva',
              'Átkozott', 'G1944', T, 'G1944', 'fej'),
'Zsid 6:7-8': p('A levél példázata szerint a föld, amely „töviseket és bojtorjánokat terem, megvetett és közel van az '
                'átokhoz”. A föld, a tövis, a bojtorján és az átok együtt az 1Móz 3:17-18 görög szövegének szavai: a '
                'genezisi átok itt erkölcsi példázattá lesz.',
                '🔗 példázat — a 3:17-18 szavai a föld termésének erkölcsi képében',
                'átokhoz', 'G2671', T, 'G2671', 'fej'),
'Jel 11:18': p('A vének hálaadása szerint eljött az idő, hogy Isten „elpusztítsd azokat, a kik a földet pusztítják.” A '
               'görögben ugyanaz az ige (διαφθείρω, diaftheiró) áll mindkét oldalon, ahogy az 1Móz 6:12-13-ban: Isten '
               'azzal az igével ítél, amellyel a föld megrontói vétkeztek.',
               '⚖️ tükörítélet — ugyanaz az ige a vétekre és az ítéletre, mint az 1Móz 6:12-13-ban',
               'pusztítják', 'G1311', T, 'G1311', '1'),
'Jel 19:2': p('A mennyei sokaság Isten ítéletét dicséri a nagy parázna felett, „a mely a földet megrontotta az ő '
              'paráznaságával”. A romlás igéje (φθείρω, ftheiró) a földdel együtt az Újszövetségben csak itt és a Jel '
              '11:18-ban áll, és a vád Babilon ellen ugyanaz, mint a Jer 51:25-ben.',
              '⚖️ ítélet — a föld megrontójának elítélése; a Jer 51:25 vádja',
              'megrontotta', 'G5351', T, 'G5351', 'fej'),
'Jel 22:3': p('Az új Jeruzsálem leírásában áll: „semmi elátkozott nem lesz többé”. A görög szó (κατάθεμα, katathema) '
              'nem a Genezis átok-szava, de az élet fája mellett (Jel 22:2) a kánon záró képe az 1Móz 3 átkának '
              'megszűnése; a hely ezért tematikus, nem lexikai kapcsolatként tartozik ide.',
              '🔍 tematikus, nem lexikai — a kánon zárása: az átok megszűnik',
              'elátkozott', 'G2652', T, 'G2652', 'fej', gerinc='tematikus:1Móz 3:17', pardes='Sod'),
'Mt 15:19': p('Jézus tanítása szerint „a szívből származnak a gonosz gondolatok, gyilkosságok, házasságtörések”. A szív '
              'gondolatainak gonoszsága az 1Móz 6:5 diagnózisa; a hely a lánc szavai nélkül, tematikus, nem lexikai '
              'kapcsolatként tartozik ide.',
              '🔍 tematikus, nem lexikai — a 6:5 szív-diagnózisa Jézus tanításában',
              'gonosz gondolatok', 'G1261', T, 'G1261', '1'),
'Mk 7:21-23': p('Márk hosszabb felsorolással adja ugyanezt: „az emberek szívéből származnak a gonosz gondolatok”, és '
                'hozzáteszi: „Mind ezek a gonoszságok belőlről jőnek ki, és megfertőztetik az embert.” A tisztátalanság '
                'forrása a szív, mint az 1Móz 6:5-ben; a hely tematikus, nem lexikai kapcsolatként tartozik ide.',
                '🔍 tematikus, nem lexikai — a szív gonosz gondolatai fertőzik meg az embert',
                'gonosz gondolatok', 'G1261', T, 'G1261', '1'),
'2Pét 3:6-7': p('Péter szerint az akkori világ „vízzel elboríttatván elveszett”, a mostani ég és föld pedig „tűznek tartatván '
                'fenn, az ítéletnek és az istentelen emberek romlásának napjára.” Az özönvíz ítélete itt a végső ítélet '
                'előképe; a hely a lánc szavai nélkül, tematikus, nem lexikai kapcsolatként tartozik ide.',
                '🔍 tematikus, nem lexikai — az özönvíz ítélete a végső ítélet előképe',
                'elboríttatván', 'G2626', T, 'G2626', 'fej'),
}

UJ = ('1Móz 7:4', '1Móz 7:23', 'Ez 12:19', 'Sof 1:2-3', 'Jer 51:25', 'Hós 10:8', 'Mal 3:11', 'Jel 22:3')
UJ_GERINC = {'1Móz 7:4': 'H0127', '1Móz 7:23': 'H0127', 'Ez 12:19': 'H2555', 'Sof 1:2-3': 'H0127',
             'Jer 51:25': 'H7843', 'Hós 10:8': 'H6975+H1863', 'Mal 3:11': 'H7843'}
# kanonikus sorrend: az új sor a megnevezett meglévő sor után áll
UTANA = {'1Móz 7:4': '1Móz 6:17', '1Móz 7:23': '1Móz 7:4', 'Ez 12:19': 'Ez 8:17', 'Sof 1:2-3': 'Mik 6:12',
         'Jer 51:25': 'Jer 6:7', 'Hós 10:8': 'Hab 1:2', 'Mal 3:11': 'Hós 10:8', 'Jel 22:3': 'Jel 19:2'}

NEGATIV = ('A versben a genezisi lánc egyik szava áll — héberül az átok (árar), a föld (adámá), a fájdalom és fáradság '
           '(itzávón), a bűn (chattát), az erőszak (chámász) vagy a romlás igéje (sáchat); görögül az átkozott '
           '(ἐπικατάρατος, epikataratosz), az átok (κατάρα, katara) vagy a romlás szócsaládja (φθείρω, ftheiró) —, vagy '
           'a lánc szópárja (tövis és bogáncs; megtelt erőszakkal; hallatszik az erőszak), és a hely ezen a szón át az '
           '1Móz 3–9 láncára utal vissza: az átkot a földön, a föld romlását, az erőszakkal megtelt földet vagy a föld '
           'színéről való eltörlést mondja ki, ismétli vagy fordítja meg. Nem tartozik ide a hely, amelyben a szó '
           'általános használatban áll (bűnáldozat, föld mint ország vagy talaj, katonai pusztítás, rituális vagy '
           'emberi átkozódás, romlandó test), és az sem, amely a föld elvesztését csak a szövetségi rendben mondja ki. '
           'A szavak nélkül a hely csak „tematikus, nem lexikai” jelöléssel, név szerint tartozik ide. Az újszövetségi '
           'helyeknél a Textus Receptus a mérce.')
FOLERENDELT = 'a bűn és következményei általában, a genezisi lánc szavai és szerkezete nélkül'

# (szotar, strong, bdb_id, szakasz, jelentes_szam, cimke_hu)
CIMKE = [
    (B, 'H0127', 'BDB109', '-/1/-', '1', 'a megművelt föld, amely táplál'),
    (B, 'H0127', 'BDB109', '-/3/-', '3', 'a föld mint anyag, amelyből az ember lett'),
    (B, 'H0127', 'BDB109', '-/4/-', '4', 'a föld látható felszíne, a föld színe'),
    (B, 'H0779', 'BDB782', 'Qal/-/-', 'Qal', 'átkoz, átkozott'),
    (B, 'H6975', 'BDB7382', '-/1/-', '1', 'tövisbokor, a bogánccsal együtt'),
    (B, 'H2403', 'BDB2699', '-/1/-', '1', 'bűn'),
    (B, 'H7843', 'BDB8615', "Niph'al/-/-", "Nif'ál", 'megromlik, tönkremegy'),
    (B, 'H7843', 'BDB8615', "Pi'el/1/-", "Pi'él 1", 'elront, elpusztít'),
    (B, 'H7843', 'BDB8615', "Hiph'il/1/-", "Hif'íl 1", 'elront, tönkretesz (termést, földet)'),
    (B, 'H7843', 'BDB8615', "Hiph'il/2/-", "Hif'íl 2", 'erkölcsileg megront, romlottan cselekszik'),
    (B, 'H7451', 'BDB8032', '-/10/c', '10.c', 'gonosz (a szív gondolatairól)'),
    (B, 'H0423', 'BDB472', '-/3/-', '3', 'átok, Istentől'),
    (B, 'H0056', 'BDB50', 'Qal/-/-', 'Qal', 'gyászol, búsul'),
    (T, 'G5356', '', '-/1/-', '1', 'romlás, enyészet, pusztulás'),
    (T, 'G1944', '', 'fej', 'fej', 'átkozott, Isten átka alatt álló'),
    (T, 'G2671', '', 'fej', 'fej', 'átok, átkozódás'),
    (T, 'G1311', '', '-/1/-', '1', 'megront, rosszabbá tesz'),
    (T, 'G5351', '', 'fej', 'fej', 'megront, elpusztít'),
    (T, 'G2652', '', 'fej', 'fej', 'elátkozott dolog'),
    (T, 'G1261', '', '-/1/-', '1', 'gondolat, belső okoskodás'),
    (T, 'G2626', '', 'fej', 'fej', 'elönt, vízzel elborít'),
]
CIMKE_PROV = 'scope=manual | forras=' + FORRAS + ' (a szakasz szövege: adat/thayer_szakaszok.tsv, adat/bdb_szakaszok.tsv) | ts=' + TS

RES_TANULMANY = ('kivonat', 'miert_fontos', 'ertelmezes', 'alkalmazas', 'modszertan')
RES_ADAT = {'2b': '### 2/b. Kiegészítő szótári adatok', 'minosites': '### Minősítés',
            'alatamasztas': '### Alátámasztás'}
TANITOI = 'Ehhez a motívumhoz nevesített tanítói egyezés még nem került a lapra; a hiány nincs kitöltve.'


def nyit(ut):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers.split(nl), nl


def ir(ut, sorok, nl):
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


def fej_ix(sorok, kezd):
    i = next(k for k, s in enumerate(sorok) if s.startswith(kezd))
    return i, {n: j for j, n in enumerate(sorok[i].split('\t'))}


def karoli_versek():
    d = {}
    for l in io.open(os.path.join(GY, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8'):
        r = l.rstrip('\n').split('\t')
        if len(r) >= 2:
            d[r[0]] = r[1]
    return d


def tartomany_szoveg(kar, ige):
    k, h = ige.rsplit(' ', 1)
    f, v = h.split(':')
    a, b = (v.split('-') + [v])[:2]
    return ' '.join(kar.get('%s %s:%d' % (k, f, i), '') for i in range(int(a), int(b) + 1))


def ellenoriz_karoli():
    """Minden `karoli_szo` és minden „…” idézet a Károli-vers (vagy a megnevezett vers) szó szerinti része."""
    import re
    kar = karoli_versek()
    hiba = []
    for ige, d in P.items():
        sz = tartomany_szoveg(kar, ige)
        if d['karoli'] not in sz:
            hiba.append('%s karoli_szo: %s' % (ige, d['karoli']))
        for idezet in re.findall(r'„([^”]+)”', d['k']):
            if idezet.rstrip('.!?') not in sz and not any(idezet.rstrip('.!?') in kar.get(x, '') for x in
                                                         ('Jel 19:2', '1Móz 3:17', 'Jón 3:10')):
                hiba.append('%s idézet: %s' % (ige, idezet))
    if hiba:
        sys.exit('KÁROLI-ELTÉRÉS:\n' + '\n'.join(hiba))
    print('Károli-idézetek: rendben (%d hely)' % len(P))


def elofordulasok():
    ut = os.path.join(GY, 'adat', 'elofordulasok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    regi_ix = [k for k, s in enumerate(sorok) if k > fi and s.split('\t')[0] == ID]
    assert regi_ix == list(range(regi_ix[0], regi_ix[-1] + 1)), 'a motívum sorai nem egy blokkban'
    regi = [sorok[k].split('\t') for k in regi_ix]
    latott = [m[ix['igehely']] for m in regi]
    assert set(latott) == set(P) - set(UJ), set(latott) ^ (set(P) - set(UJ))
    archiv = []
    blokk = []
    for m in regi:
        ige = m[ix['igehely']]
        archiv.append('\t'.join([ige, m[ix['kapcsolodas']], m[ix['funkcio']], m[ix['karoli_szo']]]))
        blokk.append(m)
    for ige in UJ:
        m = [''] * len(ix)
        m[ix['id']], m[ix['igehely']] = ID, ige
        m[ix['pardes_szint']] = P[ige]['pardes']
        m[ix['gerinc_elem']] = UJ_GERINC.get(ige, P[ige]['gerinc'])
        m[ix['igazolas']] = 'TAHOT-igazolt' if ige != 'Jel 22:3' else 'TAHOT-hatokoron-kivul'
        hova = next(i for i, x in enumerate(blokk) if x[ix['igehely']] == UTANA[ige])
        blokk.insert(hova + 1, m)
    for m in blokk:
        d = P[m[ix['igehely']]]
        m[ix['kapcsolodas']], m[ix['funkcio']], m[ix['karoli_szo']] = d['k'], d['f'], d['karoli']
        m[ix['strong']] = d['strong'] if not (d['gerinc'] or '').startswith('tematikus') or m[ix['igehely']] in (
            '1Móz 6:5',) else ''
        if d['gerinc']:
            m[ix['gerinc_elem']] = d['gerinc']
        m[ix['lexikon_szotar']], m[ix['lexikon_entry_id']], m[ix['jelentes_szam']] = d['szotar'], d['entry'], d['jsz']
        tem = (m[ix['gerinc_elem']] or '').startswith('tematikus')
        m[ix['azonositas_modja']] = 'tartalom-alapú'
        m[ix['megbizhatosag']] = 'közepes' if tem else 'magas'
        m[ix['proveniencia']] = PROV
    uj = sorok[:regi_ix[0]] + ['\t'.join(m) for m in blokk] + sorok[regi_ix[-1] + 1:]
    a = sorok[:regi_ix[0]] + sorok[regi_ix[-1] + 1:]
    b = uj[:regi_ix[0]] + uj[regi_ix[0] + len(blokk):]
    if a != b:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
    ir(ut, uj, nl)
    os.makedirs(os.path.join(GY, 'archivum', ID), exist_ok=True)
    ir(os.path.join(GY, 'archivum', ID, ID + '_1a_proza_regi.tsv'),
       ['# ARCHÍV: adat/elofordulasok.tsv HAMART-001 kapcsolodas/funkcio/karoli_szo a F123 HAMART-001 új cikke előtt '
        '(2026-11-05) · nem forrás, nem szerkesztendő', 'igehely\tkapcsolodas\tfunkcio\tkaroli_szo'] + archiv + [''],
       '\n')
    print('elofordulasok.tsv: %d sor (%d új)' % (len(blokk), len(UJ)))


def egy_sor(fajl, kezd, feltetel, modosit, varhato=1):
    ut = os.path.join(GY, 'adat', fajl)
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, kezd)
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and feltetel(m, ix):
            modosit(m, ix)
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == varhato, (fajl, len(erintett))
    ir(ut, uj, nl)
    print('%s: %d sor' % (fajl, len(erintett)))


def motivumok():
    def mod(m, ix):
        m[ix['negativ_kriterium']], m[ix['folerendelt_fogalom']] = NEGATIV, FOLERENDELT
        m[ix['forras_study']] = 'motivumok/HAMART-001.md'
    egy_sor('motivumok.tsv', 'id\t', lambda m, ix: m[0] == ID, mod)


def res():
    def mod(m, ix):
        r = m[ix['res']]
        if r in RES_TANULMANY:
            m[ix['forras']], m[ix['tanulmany']] = 'tanulmany', 'motivumok/HAMART-001.md'
        elif r in RES_ADAT:
            m[ix['forras']] = 'adat'
            if r != 'alatamasztas':
                m[ix['tanulmany']] = ''
        elif r == 'tanitoi':
            m[ix['forras']], m[ix['tanulmany']] = 'adat', TANITOI
    egy_sor('res_forras.tsv', 'id\t', lambda m, ix: m[0] == ID, mod, varhato=9)


def kapcsolo():
    def mod(m, ix):
        m[ix['allapot']] = 'aktiv'
        m[ix['indok']] = 'a szótári gerinc a motívumon kész (F123 HAMART-001 új cikk: a szakaszcímkék és a sorok szótári mezői)'
        m[ix['proveniencia']] = PROV
    egy_sor('funkcio_kapcsolok.tsv', 'kapcsolo\t', lambda m, ix: m[0] == 'SZOTARI_GERINC' and m[1] == ID, mod)


def cimke():
    ut = os.path.join(GY, 'adat', 'szotar_szakasz_cimke.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'szotar\t')
    meglevo = {tuple(s.split('\t')[:4]) for s in sorok[fi + 1:] if s.strip()}
    hozza = []
    for sz, st, bid, utv, jsz, hu in CIMKE:
        if (sz, st, bid, utv) in meglevo:
            continue
        hozza.append('\t'.join([sz, st, bid, utv, jsz, hu, CIMKE_PROV, '']))
    utolso = max(k for k, s in enumerate(sorok) if s.strip())
    ir(ut, sorok[:utolso + 1] + hozza + sorok[utolso + 1:], nl)
    print('szotar_szakasz_cimke.tsv: +%d sor' % len(hozza))


def hivatkozas():
    """A szakaszcímkék kutatói kulcsa létező lexikon_hivatkozasok-kulcs legyen (17. szabály)."""
    def szakaszok(fajl, bdb):
        sorok, _ = nyit(os.path.join(GY, 'adat', fajl))
        fi, ix = fej_ix(sorok, 'strong\t')
        d = {}
        for s in sorok[fi + 1:]:
            m = s.split('\t')
            if len(m) < len(ix):
                continue
            k = (m[ix['strong']], m[ix['bdb_id']] if bdb else '', m[ix['utvonal']])
            jel = m[ix['jel']].strip()
            d.setdefault(k, ((jel + ' ') if jel else '') + m[ix['szoveg']])
        return d
    th = szakaszok('thayer_szakaszok.tsv', False)
    bdb = szakaszok('bdb_szakaszok.tsv', True)
    ut = os.path.join(GY, 'adat', 'lexikon_hivatkozasok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'strong\t')
    meglevo = {tuple(s.split('\t')[:4]) for s in sorok[fi + 1:] if s.strip()}
    hozza = []
    for sz, st, bid, utv, jsz, _hu in CIMKE:
        k = (st, sz, st, jsz)
        if k in meglevo:
            continue
        szoveg = (th if sz == T else bdb)[(st, bid, utv)]
        forras = 'adat/thayer_szakaszok.tsv' if sz == T else 'adat/bdb_szakaszok.tsv'
        hozza.append('\t'.join([st, sz, st, jsz, szoveg, forras]))
    utolso = max(k for k, s in enumerate(sorok) if s.strip())
    ir(ut, sorok[:utolso + 1] + hozza + sorok[utolso + 1:], nl)
    print('lexikon_hivatkozasok.tsv: +%d sor' % len(hozza))


if __name__ == '__main__':
    ellenoriz_karoli()
    if '--csak-ellenoriz' in sys.argv:
        sys.exit(0)
    elofordulasok()
    motivumok()
    res()
    kapcsolo()
    cimke()
    hivatkozas()
