"""F239 U3 — a TEREMT-001 1/a prózája (adat/elofordulasok.tsv `kapcsolodas`, `funkcio`) és meghatározása
(adat/motivumok.tsv `meghatarozas`), nulláról, egy kézből (claude-opus-5-5), a 10-es prompt és a 9-es sablon
„Az 1/a igehelyenkénti prózája” szerint: kerek mondat, az idézet a Károli-vers szó szerinti része, a funkció
„címke — magyarázat”. A régi mondatok archívumban: archivum/TEREMT-001/TEREMT-001_1a_proza_regi.tsv.

Írás előtt: minden „…” idézet a sor Károli-verseinek (a tartomány minden versének) szövegében áll
(konkordancia/Karoli_1908.tsv); mind a 43 sor megvan; csak a sorok `kapcsolodas`, `funkcio` és `proveniencia` mezője,
illetve a motívum `meghatarozas` mezője változik (összevetés). A `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F239_U3_proza_1a.py [--ir]"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

MOT = 'TEREMT-001'
PROV = ('scope=manual | forras=F239 TEREMT-001 új cikk, U3 (claude-opus-5-5; a Károli-vers: konkordancia/Karoli_1908.tsv; '
        'a héber és a görög szó: TAHOT_kivonat.tsv, TAGNT_kivonat.tsv; a láncbeli helyzet: naplok/ERVNAPLO_TEREMT-001.md) '
        '| ts=2026-11-23')

MEGHATAROZAS = (
    'A héber Biblia tehóm szava a föld alatti és a tenger mélyén lévő vizet, a mélységet nevezi meg; görög utóda, az '
    'abüsszosz, az Újszövetségben zárt hellyé lesz, ahová a démonokat és a sárkányt küldik. A motívum azokat a '
    'helyeket foglalja magában, amelyekben ez a két szó áll, a teremtés kezdetének vizétől az özönvíz forrásain, az '
    'áldásokon és a kivonulás tengerén át a Jelenések bezárt mélységéig.')

P = {
    '1Móz 1:2': (
        'A teremtés első állapotának leírásában a mélység az a víztömeg, amelyen sötétség van: „setétség vala a '
        'mélység színén, és az Isten Lelke lebeg vala a vizek felett”. A motívum helyei közül ez az első; a mélység a '
        'versben semmit nem cselekszik, a föld állapotát pedig ugyanez a vers egy másik szópárral, a tohu va-vohuval '
        'mondja („kietlen és puszta”).',
        '🌱 kezdet — a motívum első helye: a mélység a teremtés kezdetén, sötétséggel a színén, cselekvés nélkül'),
    '1Móz 7:11': (
        'Az özönvíz kezdetén két irányból tör elő a víz: „felfakadának ezen a napon a nagy mélység minden forrásai, és '
        'az ég csatornái megnyilatkozának”. A mélység forrásai a héberben csak itt és a 8:2-ben állnak együtt; az '
        'alulról feltörő víz itt az ítélet eszköze.',
        '🌊 özönvíz — a mélység forrásai megnyílnak: a lent lévő víz az ítélet eszköze'),
    '1Móz 8:2': (
        'Az özönvíz végén ugyanazok a források záródnak be: „bezárulának a mélység forrásai s az ég csatornái”. A héber '
        'ige (szákar) elzárást jelent; a 7:11-ben megnyílt két vízforrás itt egy mondatban zárul le, és az eső is '
        'megszűnik.',
        '🌊 özönvíz — a megnyitás párja: a mélység forrásai bezárulnak, az ítélet véget ér'),
    '1Móz 49:25': (
        'Jákob Józsefre mondott áldásában a mélység az áldás forrása: „az ég áldásaival, onnan felülről, a mélység '
        'áldásaival, mely alant terül”. Az ég és a mélység itt is együtt áll, mint az 1Móz 7:11-ben, de mindkettő '
        'áldást hoz.',
        '💧 áldás — az ég és a mélység együtt, áldásként; a kifejezés Mózes áldásában visszatér (5Móz 33:13)'),
    '5Móz 33:13': (
        'Mózes Józsefre mondott áldása ugyanazt a képet hozza: „Áldott az Úrtól az ő földe az égnek kincseivel, a '
        'harmattal és az alant elterülő mélységes vizekkel”. Az „alant elterülő” mélység a héberben ugyanaz a '
        'kifejezés, mint Jákob áldásában (1Móz 49:25); a mélység mellett ez az ige csak ebben a két versben áll.',
        '💧 áldás — Jákob áldásának kifejezése Mózes áldásában, ugyanarra a törzsre'),
    '2Móz 15:5': (
        'A Tengeri ének az egyiptomiak pusztulását mondja el: „Elborították őket a hullámok, kő módjára merültek a '
        'mélységbe.” A héberben a „hullámok” szava a tehóm többes száma; a versbeli „mélység” viszont más szót, a '
        'tenger mélyét jelentő mecólát fordítja, így a magyar „mélység” itt nem a motívum szava.',
        '🌊 kivonulás — a mélységek az üldözők fölött: a víz itt a szabadítás és az ítélet eszköze'),
    '2Móz 15:8': (
        'Az ének Isten leheletének tulajdonítja a tenger kettéválását: „Orrod lehelletétől feltorlódtak a vizek”, és '
        '„a mélységes vizek megmerevültek a tenger szívében”. A mélység itt nem önálló erő: Isten leheletére áll meg, '
        'hogy a nép átmehessen.',
        '🌊 kivonulás — a mélység Isten leheletére megmerevedik a tenger közepén'),
    '5Móz 8:7': (
        'Mózes az ígéret földjét írja le: „bővizű patakoknak, forrásoknak és mély vizeknek földére, a melyek a '
        'völgyekben és a hegyeken fakadnak”. A „mély vizek” a tehóm többes száma; a mélység itt a földet öntöző, '
        'feltörő víz, a jó föld egyik ajándéka.',
        '💧 vízforrás — az ígéret földjének feltörő vizei: a mélység mint bőség'),
    'Jób 28:14': (
        'A bölcsesség helyét kereső vers a mélységet és a tengert szólaltatja meg: „A mélység azt mondja: Nincsen az '
        'bennem; a tenger azt mondja: én nálam sincsen.” A legmélyebb hely sem rejti a bölcsességet; a vers ezzel a '
        'teremtett világ határát mutatja meg.',
        '❓ elérhetetlen mélység — a mélység sem rejti a bölcsességet'),
    'Jób 38:16': (
        'Isten a forgószélből kérdezi Jóbot: „Eljutottál-é a tenger forrásáig, bejártad-é a mélységnek fenekét?” A '
        'mélység itt az a hely, ahová ember nem jut el; a kérdés Isten tudásának mértékét állítja az ember elé.',
        '❓ elérhetetlen mélység — Isten kérdése: a mélység feneke az ember előtt rejtve van'),
    'Jób 38:30': (
        'Ugyanebben a beszédben a fagy képe áll: „Miként rejtőznek el a vizek mintegy kő alá, és mint zárul be a mély '
        'vizek színe?” A „mély vizek színe” a héberben a mélység színe (pené tehóm), ugyanaz a kifejezés, mint az 1Móz '
        '1:2-ben; itt a felszín jéggé zárul.',
        '❓ elérhetetlen mélység — a mélység színe befagy: Isten műve, amelyet ember nem ért'),
    'Zsolt 33:7': (
        'A teremtő Istent dicsérő zsoltár szerint Isten „Összegyűjti a tenger vizeit, mintegy tömlőbe; tárházakba '
        'rakja a hullámokat.” A „hullámok” a héberben a tehóm többes száma: a mélység itt Isten raktárában van, '
        'rendezett és megőrzött készletként.',
        '👑 Isten uralma — a mélységet Isten tárházakba gyűjti'),
    'Zsolt 36:7': (
        'A zsoltár Isten igazságát a hegyekhez, ítéleteit a mélységhez méri: „Igazságod, mint Isten hegyei; '
        'ítéleteid, mint a nagy mélységek”. A hasonlat a magasság és a mélység két végpontjával méri Isten '
        'igazságát és ítéleteit.',
        '👑 Isten uralma — hasonlat: Isten ítéletei olyanok, mint a nagy mélység'),
    'Zsolt 42:8': (
        'A panaszkodó zsoltáros a rázúduló vizek képével beszél: „Örvény örvényt hív elő zuhatagjaid hangjára; minden '
        'vízáradásod és hullámod összecsap fölöttem!” A héberben a tehóm itt kétszer áll, a Károli „örvény”-nek '
        'fordítja; a vizek Istenéi, és a szenvedőt borítják el.',
        '🙏 panasz — a mélység mint az imádkozót elborító víz; a szó kétszer áll a versben'),
    'Zsolt 71:20': (
        'Az idős zsoltáros így szól Istenhez: „A ki sok bajt és nyomorúságot éreztettél velünk, de ismét '
        'megelevenítesz, és a föld mélységéből ismét felhozol minket.” A „föld mélységéből” szavakban a tehóm többes száma áll a föld '
        'szavával; a megelevenítés mellett a mélység itt a halál közelségének képe, ahonnan Isten felhoz.',
        '🕳️ halál közelsége — a föld mélysége, ahonnan Isten felhoz'),
    'Zsolt 77:17': (
        'A zsoltár Isten megjelenését a vizek félelmével írja le: „Láttak téged a vizek, oh Isten, láttak téged a vizek '
        'és megfélemlének; a mélységek is megrázkódának.” A mélység itt Isten előtt remegő teremtmény; a zsoltár '
        'ugyanebben a szakaszban Isten tengeren át vezető útjáról beszél.',
        '📯 Isten megjelenése — a mélységek megrázkódnak Isten láttán'),
    'Zsolt 78:15': (
        'A pusztai vándorlásra visszatekintő zsoltár szerint Isten „Sziklákat hasított meg a pusztában, és inniok adott '
        'bőségesen, akárcsak a mélységes vizekből.” A mélység itt hasonlat: a sziklából fakadó víz bőségét a mélység '
        'vizéhez méri.',
        '💧 vízforrás — hasonlat: a sziklából fakadó víz bősége, mint a mélységé'),
    'Zsolt 104:6': (
        'A teremtést éneklő zsoltár a föld első állapotát írja le: „Vízáradattal, mint egy ruhával borítottad be azt, a '
        'hegyek felett is vizek állottak vala.” A „vízáradat” a tehóm fordítása; a mélység itt ruhaként borítja a '
        'földet, és a következő versben (Zsolt 104:7) Isten kiáltására eloszlik.',
        '🌱 kezdet — a mélység mint a földet borító ruha, amelyet Isten szava rendbe szab'),
    'Zsolt 106:9': (
        'A nép történetét elmondó zsoltár a Veres-tengeri átkelést idézi: „Rákiálta a veres tengerre és kiszáradt, s '
        'úgy vivé őket a mélységeken, mint egy síkon.” A mélység itt az az út, amelyen Isten a népet átvezeti.',
        '🌊 kivonulás — a mélység mint út, amelyen Isten a népet átvezeti'),
    'Zsolt 107:26': (
        'A tengeren járók viharát leíró szakaszban a hajósok „Az égig emelkedének, a fenékig sülyedének; lelkök '
        'elolvada az inségben.” A „fenék” a tehóm fordítása: a mélység itt a viharhullámok völgye, halálos veszedelem, '
        'amelyből a hajósok az Úrhoz kiáltanak (Zsolt 107:28).',
        '🌊 vihar — a mélység mint a hajósokat elnyelni készülő tenger'),
    'Zsolt 135:6': (
        'A dicséret Isten hatalmát a világ minden rétegére kiterjeszti: „Mind megteszi az Úr, a mit akar: az egekben és '
        'a földön, a vizekben és minden mélységben.” A mélység a felsorolás utolsó, legalsó tagja; ott is Isten akarata '
        'teljesül.',
        '👑 Isten uralma — a mélység a világ legalsó rétege, ahol Isten akarata is teljesül'),
    'Zsolt 148:7': (
        'A teremtett világot dicséretre hívó zsoltár a földről szólítja meg a tenger teremtményeit: „Dicsérjétek az '
        'Urat a földről: viziszörnyek és mély vizek ti mind!” A „mély vizek” a tehóm többes száma: a mélység a vízi '
        'szörnyekkel együtt Isten dicséretére hívott teremtmény.',
        '👑 Isten uralma — a mélységet is Isten dicséretére hívják'),
    'Péld 3:20': (
        'A bölcsességet dicsérő szakasz szerint a teremtő Isten „tudománya által fakadtak ki a mélységből a vizek, és a '
        'felhők csepegnek harmatot”. A mélység itt Isten bölcsessége által megnyitott vízforrás, a felhők harmatával '
        'párban.',
        '💧 vízforrás — a mélység vize Isten tudása által fakad'),
    'Péld 8:24': (
        'A megszemélyesített Bölcsesség a saját eredetét a mélységek elé teszi: „Még mikor semmi mélységek nem voltak, '
        'születtem vala”. A vers szerint a mélységeknek kezdetük van: nem mindig voltak, hanem Isten teremtésének '
        'részei.',
        '🏛️ kezdet és határ — a mélységek is teremtettek: a Bölcsesség előttük született'),
    'Péld 8:27': (
        'A Bölcsesség azt mondja magáról, hogy ott volt, amikor Isten az eget készítette, és „mikor felveté a mélységek '
        'színén a kerekséget”. A mélység színe (pené tehóm) az 1Móz 1:2-ben is áll; itt Isten kört, határvonalat húz rá.',
        '🏛️ kezdet és határ — Isten kört szab a mélység színére'),
    'Péld 8:28': (
        'A következő mondat a fent és a lent vizeit állítja párba: Isten „megerősíté a felhőket ott fenn”, és „erősekké '
        'lőnek a mélységeknek forrásai”. A mélység forrásai itt Isten teremtő rendjében erősödnek meg.',
        '🏛️ kezdet és határ — a mélység forrásai Isten rendjében megerősödnek'),
    'Ézs 51:10': (
        'A próféta az Úr karjához szól, és a kivonulást idézi: „Nem te vagy-é, a ki a tengert megszáraztotta, a nagy '
        'mélység vizeit; a ki a tenger fenekét úttá változtatta, hogy átmenjenek a megváltottak?!” A „nagy mélység” az '
        'özönvíz mondatából ismert kifejezés (1Móz 7:11); az előző vers (Ézs 51:9) a Ráhábot és a sárkányt nevezi meg, '
        'más szavakkal.',
        '🌊 kivonulás — a nagy mélység kiszárítva, út a megváltottaknak'),
    'Ézs 63:13': (
        'A próféta Isten régi tetteire emlékezik, arra, „Ki járatá őket mélységekben, mint a lovat a síkon, és meg nem '
        'botlottanak!” A kép a Zsolt 106:9-ével rokon: mindkettőben a mélység sík út, amelyen a nép biztosan halad.',
        '🌊 kivonulás — a mélység sík útként a nép lába alatt'),
    'Ez 26:19': (
        'Tírus ellen szóló ítéletében Isten azt mondja: „mikor a mélység árját felhozom reád, hogy beborítsanak a sok '
        'vizek”. A mélység itt a várost elborító tenger, az ítélet eszköze; a következő vers (Ez 26:20) más szóval, a '
        'sírgödörbe szállók képével folytatja.',
        '⚖️ ítélet — a mélység Tírust elborító víz; a következő vers a sírgödröt nevezi'),
    'Ez 31:4': (
        'A fáraóhoz intézett példázatban egy nagy cédrus áll, és a fa nagyságának oka a víz: „Víz nevelte nagygyá, a '
        'mélység vizei tették magassá”. A mélység itt a fát tápláló, folyókon át öntöző víz.',
        '💧 vízforrás — a mélység vize táplálja a cédrust'),
    'Ez 31:15': (
        'Ugyanebben a példázatban a cédrus bukásakor Isten azt mondja: „Azon a napon, a melyen sírba aláméne, gyászba '
        'öltöztetém miatta a mélység vizeit, és megtartóztatám folyóikat”. A „sír” a héberben a seól; a mélység és a '
        'seól csak ebben a versben áll együtt, és itt sem azonos: a fa a seólba száll, a mélység vize gyászol, és Isten '
        'visszatartja.',
        '🔗 érintkezés — a mélység és a seól egy versben: a gyászoló víz és a holtak helye'),
    'Ámós 7:4': (
        'Ámós látomásában Isten tüzet hív elő ítéletre, és az „megemészté az a nagy mélységet, és megemészté az '
        'országot”. A nagy mélység itt az ítélet tárgya: a tűz előbb a nagy mélységet, azután az országot emészti, és a '
        'következő versben a próféta könyörög a népért.',
        '⚖️ ítélet — az ítélet tüze a nagy mélységet is megemészti'),
    'Hab 3:10': (
        'Habakuk imájában Isten megjelenésekor „megrendülnek a hegyek, gátat tör a víz-ár, harsog a hullám, és magasra '
        'emeli karjait”. A „hullám” a héberben a tehóm, és szó szerint ezt mondja: a mélység hangot ad; a mélység itt '
        'Isten előtt felkiáltó teremtmény.',
        '📯 Isten megjelenése — a mélység hangot ad Isten láttán'),
    'Jón 2:6': (
        'Jónás a hal gyomrából mondott imájában így írja le a vízbe merülését: „Körülvettek engem a vizek lelkemig, mély '
        'ár kerített be engem, hinár szövődött fejemre.” A „mély ár” a tehóm fordítása; ugyanebben az imában a 2:3 a '
        'Seol torkából kiáltásról szól, más szóval, így a mélység itt a halál közelségének képe.',
        '🕳️ halál közelsége — a mélység körülveszi az imádkozót'),
    'Luk 8:31': (
        'A Gaderénusok tartományában a megszállott emberből kiűzendő ördögök arra kérik Jézust, „hogy ne parancsolja '
        'nékik, hogy a mélységbe menjenek.” A mélység (abüsszosz) itt a gonosz lelkek kényszerű helye, amelytől félnek, '
        'és ahová Jézus parancsa küldheti őket.',
        '⛓️ bezárt mélység — a démonok kényszerű helye, amelytől félnek'),
    'Róm 10:7': (
        'Pál a hitből való igazságot Mózes szavaival mondja el, de a kérdést megváltoztatja: „Kicsoda száll le a '
        'mélységbe? (azaz, hogy Krisztust a halálból felhozza.)” Az 5Móz 30:13 a tengeren való átkelésről kérdez; Pál '
        'a mélységről, és a halottak közüli felhozásra érti, így a mélység itt a halottak helye.',
        '✝️ Krisztus — a mélység mint a halottak helye; Pál a Mózes-idézet tengerét cseréli rá'),
    'Jel 9:1-2': (
        'Az ötödik trombitaszó után egy lehullott csillag megkapja a kulcsot („adaték annak a mélység kútjának kulcsa”), '
        'és „Megnyitá azért a mélységnek kútját: és füst jöve fel a kútból”. A mélység itt zárt hely, amelyet kulccsal '
        'nyitnak meg; a megnyitott kútból füst, a füstből a következő versben sáskák jönnek elő.',
        '⛓️ bezárt mélység — kulccsal megnyitják, füst és sötétség jön fel belőle'),
    'Jel 9:11': (
        'A mélységből feljött sereg fölött király áll: „Királyukul pedig a mélység angyala vala felettök; annak a neve '
        'zsidóul Abaddon, görögül pedig Apollion, azaz Vesztő a neve.” A mélységnek itt uralkodója van, akinek a neve a '
        'pusztítást mondja.',
        '⛓️ bezárt mélység — a mélységnek királya van, a Vesztő'),
    'Jel 11:7': (
        'A két tanú bizonyságtételének végén „a mélységből feljövő fenevad hadakozik ellenök, és legyőzi őket, és megöli '
        'őket.” A mélység itt az a hely, ahonnan Isten tanúinak ellensége feljön.',
        '⛓️ bezárt mélység — a fenevad onnan jön fel a tanúk ellen'),
    'Jel 17:8': (
        'Az angyal magyarázata szerint a fenevad „volt és nincs; és a mélységből jő fel és megy a veszedelemre.” A '
        'mélységből való feljövetel itt nem győzelem: a fenevad útja a veszedelembe vezet.',
        '⛓️ bezárt mélység — a fenevad feljövetele, amelynek vége a veszedelem'),
    'Jel 20:1': (
        'A látomásban egy angyal száll le a mennyből, „a kinél vala a mélységnek kulcsa, és egy nagy láncz a '
        'kezében.” A kulcs ugyanaz a görög szó, mint a Jel 9:1-ben; ott egy lehullott csillag kapja meg, itt egy '
        'mennyből leszálló angyalnál van.',
        '⛓️ bezárt mélység — a mélység kulcsa egy mennyei angyalnál'),
    'Jel 20:3': (
        'Az angyal a sárkányt, akit az előző versben megkötözött, a mélységbe veti: „És veté őt a mélységbe, és bezárá '
        'azt és bepecsételé ő felette, hogy többé el ne hitesse a népeket, míg betelik az ezer esztendő”. A Jelenések '
        'könyvében a mélységet a 9:2-ben megnyitják, itt bezárják és lepecsételik; a lezárás időre szól.',
        '⛓️ bezárt mélység — bezárják és lepecsételik, ezer esztendőre'),
    'Jób 41:32': (
        'A Leviatánról szóló leírás szerint a szörny „Maga után világos ösvényt hagy, azt hinné valaki, a tenger '
        'megőszült.” A „tenger” itt a tehóm fordítása: a héber szöveg szerint a mélység látszik ősznek a Leviatán '
        'habzó nyomától; a magyar szövegben a mélység szava nem látszik, a hely a héber szó miatt tartozik a motívumhoz.',
        '❓ elérhetetlen mélység — a mélység a Leviatán nyomától fehér; a Károli „tenger”-nek fordítja'),
}


def versek(ih):
    k, h = ih.rsplit(' ', 1)
    f, v = h.split(':')
    if '-' in v:
        a, b = v.split('-')
        return ['%s %s:%d' % (k, f, i) for i in range(int(a), int(b) + 1)]
    return [ih]


def main(ir):
    karoli = {}
    for s in open('konkordancia/Karoli_1908.tsv', encoding='utf-8'):
        m = s.rstrip('\r\n').split('\t')
        if len(m) == 2:
            karoli[m[0]] = m[1]
    hiba = []
    for ih, (kap, funk) in P.items():
        szoveg = ' '.join(karoli[v] for v in versek(ih))
        for idezet in re.findall(r'„([^”]*)”', kap):
            if idezet not in szoveg and not re.fullmatch(r'[a-záéíóöőúüű -]+', idezet):
                hiba.append('%s: nem Károli-szöveg: „%s”' % (ih, idezet))
        if ' — ' not in funk:
            hiba.append('%s: a funkció nem „címke — magyarázat”' % ih)
        if not kap.endswith('.'):
            hiba.append('%s: a próza nem ponttal zárul' % ih)
    # egyszavas idézet (a szó megnevezése) csak akkor, ha a versben áll
    for ih, (kap, _f) in P.items():
        szoveg = ' '.join(karoli[v] for v in versek(ih)).lower()
        for idezet in re.findall(r'„([^”]*)”', kap):
            if re.fullmatch(r'[a-záéíóöőúüű -]+', idezet) and idezet.lower() not in szoveg:
                hiba.append('%s: a megnevezett szó nem áll a versben: „%s”' % (ih, idezet))
    nyers = open('adat/elofordulasok.tsv', encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(nl)
    fi = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    ix = {k: i for i, k in enumerate(sorok[fi].split('\t'))}
    kesz = set()
    for i in range(fi + 1, len(sorok)):
        m = sorok[i].split('\t')
        if len(m) < 2 or m[0] != MOT:
            continue
        if m[1] not in P:
            hiba.append('%s: nincs próza' % m[1])
            continue
        regi = list(m)
        m[ix['kapcsolodas']], m[ix['funkcio']] = P[m[1]]
        m[ix['proveniencia']] = PROV
        for k, j in ix.items():
            if k not in ('kapcsolodas', 'funkcio', 'proveniencia') and m[j] != regi[j]:
                hiba.append('%s: más mező változna: %s' % (m[1], k))
        sorok[i] = '\t'.join(m)
        kesz.add(m[1])
    if set(P) - kesz:
        hiba.append('az adatban nincs: %s' % sorted(set(P) - kesz))
    if hiba:
        print('\n'.join(hiba))
        sys.exit(1)
    print('elofordulasok.tsv: %d sor (kapcsolodas, funkcio, proveniencia)' % len(kesz))
    # meghatározás
    mn = open('adat/motivumok.tsv', encoding='utf-8', newline='').read()
    mnl = '\r\n' if '\r\n' in mn else '\n'
    ms = mn.split(mnl)
    mfi = next(i for i, l in enumerate(ms) if l and not l.startswith('#'))
    mix = {k: i for i, k in enumerate(ms[mfi].split('\t'))}
    for i, l in enumerate(ms):
        m = l.split('\t')
        if m[0] == MOT:
            m[mix['meghatarozas']] = MEGHATAROZAS
            ms[i] = '\t'.join(m)
    if ir:
        open('adat/elofordulasok.tsv', 'w', encoding='utf-8', newline='').write(nl.join(sorok))
        open('adat/motivumok.tsv', 'w', encoding='utf-8', newline='').write(mnl.join(ms))
    print('motivumok.tsv: meghatarozas')
    print('ÍRVA' if ir else '(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
