"""Hibrid Károli-szótövező, 3. változat (F94.2, FELADATOK #94). A 2. változat: `hibrid_v2.py` (az előmérés
átvétele, F94.1). Saját szabályok + kivételtábla + a Károli saját szóalak-lexikona (`adat/szoto/karoli_lexikon.tsv`)
+ a változattól függően a simplemma (a kód MIT; a nyelvi adat licence függőben: DT-F94c) vagy a saját K tábla
(`adat/szoto/gyakori_alakok.tsv`).
Használat: from hibrid import to, elemez; to('teremté') -> 'teremt'; elemez('teremté') -> dict (szótári alak, mai
alak, alapige, további elfogadható, módszer, szabályforrás, régies jegy).

Változatok (`valtozat(...)`; az alapértelmezés 'A'):
- A: simplemma tartalék-lemmatizáló és igető-jelölt próba (a v2 A-jának megfelelője, a v3 javításaival);
- B: simplemma nélkül, igető-igazolás nélkül (a régies igevégződés-réteg nem vág);
- C: simplemma nélkül; az igető-igazolás a Károli-lexikonból (l. `_ige_jelolt`);
- CK: a C + a K tábla (a leggyakoribb 400 Károli-alak saját, modell-javasolt szótári alakja; DT-F94c).

A v2-höz képest (osztály- és szabályszintű javítások, F94_SZOTOVEZES_BRIEF.md .2; nem egyes alakokra szabva):
1. -é kérdőszócska kötőjellel (láttad-é): a kötőjeles -é leválik, a maradék tövez.
2. Birtokos + rag (igéjéért, házadhoz, barátaiért, kerekségének): a csupasz-tő lépés a -ja/-je/-a/-e mellett a
   -ai/-ei/-jai/-jei, -ad/-ed/-od/-öd és a hosszú magánhangzós -ám/-ém/-ád/-éd birtokos jelet is próbálja, a maradék
   Károli-attesztációjával.
3. Igekötő + ismeretlen ige (meggyarapodnak, feloldja): ha az alak változatlan maradt és igekötővel kezdődik, a
   maradék tövez, és ha igeként igazolt, az igekötő visszakerül; a régies végződés levágása után az igekötő mögött
   legalább 3 betűnek kell maradnia (megkiván ↛ megki). A ^kiván → kíván helyesírási szabály igekötő után is érvényes.
4. Kivételtábla (általános Károli-ismeret, nem a mérés hibáiból): a visszaható névmás (maga …), a névutók és
   határozószók -á/-é végű alakjai (alá, elé, mellé, közé, felé, fölé, mögé, többé, kevéssé — DT130 (9)), a hozzá
   és a reá ragos személyes névmásként (DT130 (3)), a v-tövű igék -vén alakja (tevén, vevén, evén, ivén, hivén,
   vivén, levén, lévén), a jő- alakok (jőtök, jövünk …).
5. Tőváltó: kötel- → kötél, atyj- → atya.
6. Régies -ök → -ük (legelőjök, közülök): a csere a Károli-lexikonban attesztált -ük alakra is megtörténik.
7. Felszólító -j- alakok (éljen, maradjanak): a -j + személyrag leválasztása, igei attesztációval.
8. Szigorított régies ige-felismerés (v1.1): a jelölt igetövet csak igei alak igazolja (főnévi igenév -ni, múlt
   -t/-tt, -ván/-vén, felszólító -jon/-jen/-jön, -ik-es alak); a névszóval közös -nak/-nek/-tok/-tek/-tök végződés
   nem attesztáció, és a simplemma-ismeret önmagában sem (házának ↛ ház mint ige).
9. Régies igei jegy (`regies_jegy`, v1.1): a felismert régies végződés nyelvtani jegye (értékkészlet: SEMA 2.27);
   a jegy a régies alakot írja le, nem a mai megfelelőt (monda: mult.alanyi.E3, mai megfelelője mégis: mondta). Az -ék
   -ik-es igénél `mult.E3` (tartózkodék), egyébként `mult.E1` (láték) — N-F94e, az első befagyasztás után javítva.
A KIADOTT változat a CK (DT-F94e, a felhasználó döntése, 2026-10-13): a szótárialak-tábla (`szotari_alak_epit.py`) simplemma
nélkül készül; az A (simplemmával) csak fejlesztési mérce.
Az ELLENOR_F94 utáni javítás (F94.5, általános szabályok): R1 — névszóképzős tő (-ság/-ség, -mány/-mény, -vány/-vény,
-alom/-elem; -ás/-és, ha előtte igető áll vagy a tő legalább 6 betű) nem régies igető; R2 — a birtokos névszó (a megnyújtott
tő névszói raggal is áll) nem -a/-e, -ának/-ének igealak; a C/C+K-ban az -at/-et/-ot/-öt végű tőnél a névszóval közös
-nak/-nek attesztáció nem elég (kivéve a -hat/-het, -tat/-tet igeképzőt); a csupasz-tő lépés igevizsgálata csak szigorú igei
alakot néz; simplemma nélkül az -ás/-és/-ság/-ség képzős főnév ragos alakja attesztáció nélkül is szótári alakot kap.
10. Szabályforrás (`szabaly_forras`): a helyesírási és tőváltó szabályoknál a szabályellenőrzés
   (`adat/szoto/szabaly_ellenorzes.tsv`, 2026-10-13) alátámasztott szabályai `korpusz_strong`, a cz → c `manual`
   (a felhasználó utasítása, 2026-10-13), a többi és az új szabályok `modell_ellenorizetlen`."""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import simplemma
except ImportError:  # a B, C és CK változat nélküle fut
    simplemma = None

VALTOZATOK = ('A', 'B', 'C', 'CK')
_VALTOZAT = 'A'


def valtozat(v):
    """A mérési változat beállítása: 'A' | 'B' | 'C' | 'CK' (l. a modul leírását)."""
    global _VALTOZAT
    if v not in VALTOZATOK:
        raise ValueError(v)
    if v == 'A' and simplemma is None:
        raise RuntimeError('az A változathoz a simplemma kell')
    _VALTOZAT = v


# 0. Korpusz-lexikon (a sor-formátum: alak, kisbetus, nagy_belul, nagy_kezdo; a #-sorok és a fejléc átugorva)
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LEX = os.path.join(_REPO, 'adat', 'szoto', 'karoli_lexikon.tsv')
_KTAB = os.path.join(_REPO, 'adat', 'szoto', 'gyakori_alakok.tsv')
KIS, NAGY_BELUL = {}, {}
K = {}


def lexikon_betolt(p=_LEX):
    KIS.clear()
    NAGY_BELUL.clear()
    for _l in open(p, encoding='utf-8'):
        # a fejlécsor pontos egyezéssel (az „alak” a Károliban valódi szóalak is, előtag szerint nem szűrhető)
        if _l.startswith('#') or _l.rstrip('\n') == 'alak\tkisbetus\tnagy_belul\tnagy_kezdo':
            continue
        _w, _k, _nb, _nk = _l.rstrip('\n').split('\t')
        if int(_k):
            KIS[_w] = int(_k)
        if int(_nb):
            NAGY_BELUL[_w] = int(_nb)


def k_betolt(p=_KTAB):
    """A K tábla: alak -> (szotari_alak, szotari_alak_mai, alapige, tovabbi_elfogadhato)."""
    K.clear()
    sorok = [s for s in open(p, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        K[r['alak']] = (r['szotari_alak'], r['szotari_alak_mai'], r['alapige'], r['tovabbi_elfogadhato'])


if os.path.exists(_LEX):
    lexikon_betolt()
if os.path.exists(_KTAB):
    k_betolt()

# Nyomkövetés az elemez() számára: a tövezés közben alkalmazott lépések (típus, azonosító, adat)
_NYOM = []

# 1. Károli-helyesírás -> mai helyesírás (szóalakon, a tövezés előtt): (minta, csere, azonosító)
HELYESIRAS = [
    (r'űl$', 'ül', 'űl$ → ül'), (r'űle', 'üle', 'űle → üle'), (r'^szűl', 'szül', '^szűl → szül'),
    (r'körűl', 'körül', 'körűl → körül'), (r'sűly', 'süly', 'sűly → süly'), (r'nyny', 'nny', 'nyny → nny'),
    (r'^setét', 'sötét', '^setét → sötét'), (r'cz', 'c', 'cz → c'),
    (r'^((?:meg|el|ki|be|fel|föl|le|át|vissza|össze)?)kiván', r'\1kíván', '^kiván → kíván'),
]
# a Károli-írásmód visszaállítása a szótári alakon (azonosító -> (minta a mai alakon, csere))
_VISSZA = {'űl$ → ül': (r'ül$', 'űl'), 'űle → üle': (r'ül', 'űl'), '^szűl → szül': (r'^szül', 'szűl'),
           'körűl → körül': (r'körül', 'körűl'), 'sűly → süly': (r'süly', 'sűly'), 'nyny → nny': (r'nny', 'nyny'),
           '^setét → sötét': (r'^sötét', 'setét'), 'cz → c': (r'c(?!s|z)', 'cz'), '^kiván → kíván': (r'kíván', 'kiván')}

# A szabályellenőrzés (adat/szoto/szabaly_ellenorzes.tsv, 2026-10-13) alátámasztott szabályai; a cz → c manual
KORPUSZ_STRONG = {'űle → üle', '^szűl → szül', 'lelk', 'tav', 'magv', 'sátr', 'derek', 'kez', 'nev', 'viz', 'tüz', 'kenyer',
                  'madar', 'ökr', 'szav', 'lov', 'nyar', 'pohar', 'gyöker', 'szeker', 'ajk', 'torny', 'esztendej', 'idej',
                  'mezej', 'tetej', 'fi', 'kegyelm', 'szerelm', 'eg'}
MANUAL = {'cz → c'}


def szabaly_forras(azon):
    if azon in KORPUSZ_STRONG:
        return 'korpusz_strong'
    if azon in MANUAL:
        return 'manual'
    return 'modell_ellenorizetlen'


# 2. Kivételtábla: rendhagyó és tőváltó alakok (kisbetűs alak -> tő), általános Károli-ismeret alapján
KIVETEL = {}
IGEI = set()
JEGY = {}  # a kivételtábla régies igealakjainak jegye


def _k(to, *alakok, ige=False):
    for a in alakok:
        KIVETEL[a] = to
        if ige:
            IGEI.add(a)


def _j(jegy, *alakok):
    for a in alakok:
        JEGY[a] = jegy


_k('mond', 'monda', 'mondá', 'mondék', 'mondának', 'mondotta', 'mondja', ige=True)
_k('van', 'vala', 'valának', 'valék', 'valál', 'valánk', 'valátok', 'volt', 'voltak', 'vagyon', 'vagynak', 'vagyok', 'vagyunk', 'vagytok',
   ige=True)
_k('nincs', 'nincsen', 'nincsenek')
_k('lesz', 'lesz', 'lesznek', 'leszek', 'leszel', 'leszünk', 'lesztek', ige=True)
_k('visz', 'visz', 'viszen', 'visznek', ige=True)
_k('hisz', 'hisz', 'hiszen', 'hisznek', ige=True)
_k('tesz', 'tesz', 'teszen', 'tesznek', ige=True)
_k('vesz', 'vesz', 'veszen', 'vesznek', ige=True)
_k('lesz', 'lőn', 'lőnek', 'lőnének', 'lőne', 'lészen', 'lésznek', 'legyen', 'legyenek', 'lett', 'lettek',
   'lenne', 'lennének', 'lennék', 'lennénk', 'lennétek', 'lennél', 'levén', 'lévén', ige=True)
_k('vesz', 'vevé', 'vevék', 'vevének', 'vőn', 'vőnek', 'vegye', 'vegyed', 'vegyétek', 'vett', 'vette', 'vevén', ige=True)
_k('tesz', 'tevé', 'tevék', 'tevének', 'tőn', 'tőnek', 'tegye', 'tegyed', 'tett', 'tette', 'tevén', ige=True)
_k('megy', 'méne', 'menének', 'menék', 'mene', 'ment', 'mentek', 'menj', 'menjetek', 'menvén', ige=True)
_k('jön', 'jöve', 'jövének', 'jövék', 'jőve', 'jőjön', 'jövel', 'jöjj', 'jő', 'jőnek', 'jőjj', 'jőjjön', 'jőjjenek',
   'jövén', 'jőtök', 'jövök', 'jősz', 'jövünk', 'jőjetek', 'jőjenek', ige=True)
_k('eszik', 'evé', 'evék', 'evének', 'egyél', 'egyetek', 'egyék', 'evett', 'evén', 'egyétek', 'egyed', 'egyem', ige=True)
_k('iszik', 'ivá', 'ivék', 'ivának', 'igyál', 'igyatok', 'igyék', 'ivott', 'ivén', ige=True)
_k('hisz', 'hivé', 'hivének', 'higyj', 'higyjetek', 'hitt', 'hittek', 'hivén', ige=True)
_k('visz', 'vivé', 'vivék', 'vivének', 'vigye', 'vidd', 'vitt', 'vitte', 'vivén', ige=True)
_k('ő', 'néki', 'nékik', 'vele', 'velök', 'velük', 'őnéki', 'őnékik', 'őtet', 'őket', 'őt', 'ővele', 'ő', 'hozzá', 'reá')
_k('én', 'nékem', 'engem', 'engemet', 'velem', 'énnékem')
_k('te', 'néked', 'téged', 'tégedet', 'veled', 'tenéked')
_k('mi', 'nékünk', 'minket', 'minékünk', 'velünk')
_k('ti', 'néktek', 'titeket', 'tinéktek', 'veletek')
_k('maga', 'maga', 'magát', 'magának', 'magával', 'magában', 'magából', 'magára', 'magáról', 'magához', 'magától',
   'magam', 'magad', 'magunk', 'magatok', 'maguk', 'magok', 'magamat', 'magadat', 'magunkat', 'magatokat', 'magukat',
   'magokat', 'magamnak', 'magadnak', 'magunknak', 'magatoknak', 'maguknak', 'magoknak')
_k('fiú', 'fia', 'fiai', 'fiak', 'fiakat', 'fiaid', 'fiaim', 'fiam', 'fiad', 'fiát', 'fiának', 'fiamnak', 'fiadnak', 'fiaitok', 'fiainak', 'fiaiknak', 'fiaival', 'fiaid')
_k('úr', 'ura', 'urak', 'uram', 'urad', 'urát', 'urának', 'uramnak', 'uraknak', 'urunk', 'urunknak', 'uratok', 'urat', 'urakat')
_k('szó', 'szava', 'szavát', 'szavának', 'szavam', 'szavamat', 'szavad', 'szavadat', 'szavai', 'szavait', 'szavak', 'szavakat')
_k('fű', 'füvet', 'fűvet', 'füve', 'füvét')
_k('atyafi', 'atyjafia', 'atyjafiának', 'atyádfia', 'atyádfiának', 'atyámfia', 'atyámfiai', 'atyafiai', 'atyafiait', 'atyafiak', 'atyafiaim', 'atyafiainak')
_k('íme', 'ímé', 'ím', 'ime', 'imé')
for _a in ('azért', 'ezért', 'miért', 'mikor', 'amikor', 'akkor', 'ekkor', 'valamikor', 'semmikor', 'mindenkor',
           'alá', 'elé', 'mellé', 'közé', 'felé', 'fölé', 'mögé', 'belé', 'többé', 'kevéssé'):
    KIVETEL[_a] = _a
_j('mult.alanyi.E3', 'monda', 'vala', 'méne', 'mene', 'jöve', 'jőve')
_j('mult.targyas.E3', 'mondá', 'vevé', 'tevé', 'evé', 'ivá', 'hivé', 'vivé')
_j('mult.T3', 'mondának', 'valának', 'vevének', 'tevének', 'menének', 'jövének', 'evének', 'ivának', 'hivének', 'vivének',
   'lőnének')
_j('mult.E1', 'mondék', 'valék', 'vevék', 'tevék', 'menék', 'jövék', 'vivék')
_j('mult.E3', 'evék', 'ivék')  # N-F94e: az -ik-es eszik/iszik régies múlt E/3-a (1Móz 3:6, 9:21)
# DT-F94f pontosítás (felhasználó, 2026-10-13): a megevék a Károli mind a 4 helyén T/3 tárgyas (2Krón 30:18, Ezsd 6:21,
# Mk 4:4, Luk 8:5); a jegykészletben (SEMA 2.27) nincs rá címke, ezért jegy nélküli kivételtábla-sor (üres), nem az evék öröksége
JEGY['megevék'] = ''
_j('mult.E2', 'valál')
_j('mult.T1', 'valánk')
_j('mult.T2', 'valátok')
_j('hatarozoi_igenev', 'levén', 'lévén', 'vevén', 'tevén', 'menvén', 'jövén', 'evén', 'ivén', 'hivén', 'vivén')

# 2b. Ragos személyes névmások (3. döntés: a tő a személyes névmás): rag-tő × személyrag, a régies -ök alakkal
_SZEM = [('én', 'em', 'am'), ('te', 'ed', 'ad'), ('ő', 'e', 'a'), ('mi', 'ünk', 'unk'), ('ti', 'etek', 'atok'),
         ('ő', 'ük', 'uk'), ('ő', 'ök', 'ok')]
for _rt, _mely in (('benn', True), ('belől', True), ('től', True), ('ról', False), ('rajt', False), ('nál', False),
                   ('érett', True)):
    for _n, _e, _a in _SZEM:
        KIVETEL[_rt + (_e if _mely else _a)] = _n
for _a, _n in (('reám', 'én'), ('reád', 'te'), ('reánk', 'mi'), ('reátok', 'ti'), ('reájok', 'ő'), ('reájuk', 'ő'),
               ('rám', 'én'), ('rád', 'te'), ('ránk', 'mi'), ('rátok', 'ti'), ('rájok', 'ő'), ('rájuk', 'ő'),
               ('belém', 'én'), ('beléd', 'te'), ('belénk', 'mi'), ('belétek', 'ti'), ('beléjök', 'ő'), ('beléjük', 'ő'),
               ('hozzám', 'én'), ('hozzád', 'te'), ('hozzánk', 'mi'), ('hozzátok', 'ti'), ('hozzájok', 'ő'), ('hozzájuk', 'ő')):
    KIVETEL[_a] = _n

# Mai alak (DT130 (2): ugyanazon szó régi és mai alakja) és kétértelmű alak (DT130 (11))
MAI = {'mely': 'amely', 'mostan': 'most', 'leány': 'lány', 'cselekedik': 'cselekszik', 'emlékezik': 'emlékszik',
       'férfiú': 'férfi', 'nevekedik': 'növekedik', 'minekutánna': 'miután', 'miképen': 'miképpen', 'vajjon': 'vajon'}
TOVABBI = {'vagy': 'van', 'ki': 'aki', 'hozzá': 'hozzá', 'reá': 'rá'}

# 3. Tőváltó névszók: a rag/birtokos jel előtti tőváltozat -> szótári alak
TOVALTO = {
    'lelk': 'lélek', 'ur': 'úr', 'tav': 'tó', 'magv': 'mag', 'sátr': 'sátor', 'derek': 'derék', 'kez': 'kéz',
    'nev': 'név', 'viz': 'víz', 'tüz': 'tűz', 'kenyer': 'kenyér', 'level': 'levél', 'madar': 'madár', 'falv': 'falu',
    'ökr': 'ökör', 'bokr': 'bokor', 'szav': 'szó', 'erej': 'erő', 'lov': 'ló', 'köv': 'kő', 'füv': 'fű', 'nyar': 'nyár',
    'pohar': 'pohár', 'gyöker': 'gyökér', 'tehen': 'tehén', 'szeker': 'szekér', 'kebl': 'kebel', 'terh': 'teher',
    'ajk': 'ajak', 'fark': 'farok', 'dolg': 'dolog', 'torny': 'torony', 'esztendej': 'esztendő', 'idej': 'idő',
    'mezej': 'mező', 'tetej': 'tető', 'fi': 'fiú', 'kegyelm': 'kegyelem', 'félelm': 'félelem', 'értelm': 'értelem',
    'szerelm': 'szerelem', 'eg': 'ég', 'kötel': 'kötél', 'atyj': 'atya',
}

# 4. Rag- és birtokosjel-listák a névszói leválasztáshoz
RAG = ['éi', 'é', 'nak', 'nek', 'ban', 'ben', 'ból', 'ből', 'tól', 'től', 'hoz', 'hez', 'höz', 'ról', 'ről', 'nál', 'nél', 'val',
       'vel', 'ért', 'ként', 'ig', 'ba', 'be', 'ra', 're', 'vá', 'vé', 'on', 'en', 'ön', 'at', 'et', 'ot', 'öt', 't', 'n']
BIRT = ['jaink', 'jeink', 'aink', 'eink', 'jaim', 'jeim', 'aim', 'eim', 'jaid', 'jeid', 'aid', 'eid', 'jai', 'jei',
        'ai', 'ei', 'atok', 'etek', 'otok', 'ötök', 'unk', 'ünk', 'juk', 'jük', 'jok', 'jök', 'uk', 'ük', 'ok', 'ök', 'ak', 'ek',
        'am', 'em', 'om', 'öm', 'ad', 'ed', 'od', 'öd', 'ja', 'je', 'a', 'e', 'm', 'd', 'i']
_MGH = set('aáeéiíoóöőuúüű')
_MGH_BIRT = ('a', 'e', 'ok', 'ek', 'ök', 'ak', 'ai', 'ei', 'aim', 'eim', 'aid', 'eid', 'aink', 'eink', 'am', 'em', 'ad', 'ed', 'atok', 'etek')
IGEKOTO = ['vissza', 'össze', 'egybe', 'utána', 'hozzá', 'széjjel', 'szét', 'meg', 'fel', 'föl', 'ki', 'be', 'el', 'le', 'rá',
           'reá', 'át', 'oda', 'ide', 'alá', 'elő', 'ellen', 'végig', 'után']
# régies igevégződés -> a régies alak jegye
IGEVEG = [(r'ván$', 'hatarozoi_igenev'), (r'vén$', 'hatarozoi_igenev'), (r'ának$', 'mult.T3'), (r'ének$', 'mult.T3'),
          (r'ánk$', 'mult.T1'), (r'énk$', 'mult.T1'), (r'átok$', 'mult.T2'), (r'étek$', 'mult.T2'), (r'ék$', 'mult.E1'),
          (r'ál$', 'mult.E2'), (r'él$', 'mult.E2'), (r'á$', 'mult.targyas.E3'), (r'é$', 'mult.targyas.E3'),
          (r'a$', 'mult.alanyi.E3'), (r'e$', 'mult.alanyi.E3')]
# igei attesztáció (v1.1): csak igei alak; a névszóval közös -nak/-nek/-tok/-tek/-tök nem
IGEI_ATTEST = ['ni', 'ani', 'eni', 'ott', 'ett', 'ött', 'tt', 'ván', 'vén', 'jon', 'jen', 'jön']
# a névszóval közös végződés csak akkor igazol, ha a tő a Károliban névszói raggal nem fordul elő (elhamvad-nak: igen;
# ház-nak: nem, mert ház-at, ház-ban is van)
IGEI_ATTEST_FELTETELES = ['nak', 'nek', 'tok', 'tek', 'tök']
_NEMBETU = re.compile(r'[^\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]')


def _ismert(t):
    if _VALTOZAT != 'A':
        return False
    try:
        return simplemma.is_known(t, lang='hu')
    except Exception:
        return False


def _lem(t):
    if _VALTOZAT != 'A':
        return t
    lem = _NEMBETU.sub('', simplemma.lemmatize(t, lang='hu'))
    # kisbetűs alakra nagybetűs (tulajdonnévi) lemma nem fogadható el (véghetetlen ↛ Végh)
    if t[:1].islower() and lem[:1].isupper():
        return t
    return lem


def _helyesiras(w):
    for minta, csere, azon in HELYESIRAS:
        u = re.sub(minta, csere, w)
        if u != w:
            _NYOM.append(('H', azon, None))
        w = u
    return w


def _helyesiras_csendes(w):
    for minta, csere, _ in HELYESIRAS:
        w = re.sub(minta, csere, w)
    return w


def _hosszitas_vissza(t):
    # rag előtti tővégi magánhangzó-nyúlás visszafordítása: Júdá- -> Júda, méhé- -> méhe
    if t.endswith('á'):
        return t[:-1] + 'a'
    if t.endswith('é'):
        return t[:-1] + 'e'
    return t


def _gyak(t):
    return KIS.get(t, 0) + NAGY_BELUL.get(t, 0)


_ONMAGA = ['']  # a tövezett alak maga: önmagát nem igazolhatja (megkíván ↛ megkí + -ván)


def _att(c, v):
    return (c + v) in KIS and (c + v) != _ONMAGA[0]


def _att_igei(c):
    """Szigorú igei attesztáció (önmaga nélkül), a feltételes névszói-közös végződésekkel. Legfeljebb hárombetűs
    tőnél legalább két különböző igei alak kell (ki-ván, fel-ett egyedül nem igazol)."""
    db = sum(1 for v in IGEI_ATTEST if _att(c, v))
    if db >= (2 if len(c) <= 3 else 1):
        return True
    if len(c) <= 3:
        return False
    # a gyenge, névszóval közös -nak/-nek/-tok/-tek/-tök attesztáció csak az A-ban (ott a simplemma igei tudása is dönt);
    # a C/C+K-ban kimarad (ELLENOR_F94: ritka névszónál átengedte a tövet, pl. felekezet-nek, születés-ének)
    if _nevszoi(c) or not any(_att(c, v) for v in IGEI_ATTEST_FELTETELES):
        return False
    if _VALTOZAT == 'A':
        return True
    # C/C+K (ELLENOR_F94): az -at/-et/-ot/-öt végű tőnél (a névszóképző -at/-et osztálya: felekezet, gyülekezet) a
    # névszóval közös végződés nem elég, szigorú igei alak kell (az ilyen igéknek — mutat, szeret — van)
    # (a -hat/-het és a -tat/-tet igeképző kivétel: szólhat, megfelelhet, elemésztet)
    return not re.search(r'(at|et|ot|öt)$', c) or bool(re.search(r'(hat|het|tat|tet)$', c))


def _ik_ige(c):
    """-ik-es ige: c + -ik előfordul, c mássalhangzóra végződik (szolgáik: birtokos többes), a puszta c nem fordul
    elő önállóan (üt, gyűjt: akkor a c+ik tárgyas T/3), és c-nek van szigorú igei alakja (esett, született)."""
    if (c + 'ik') not in KIS or c[-1:] in _MGH or c in KIS or c in IGEKOTO:
        return False
    for ik in IGEKOTO:
        if c.startswith(ik) and c[len(ik):] in KIS:
            return False  # egybegyűjt: a gyűjt önállóan is áll
    return sum(1 for v in IGEI_ATTEST if _att(c, v)) >= (2 if len(c) <= 3 else 1)


def _igei(c):
    """Igei attesztáció: a tő valamely igei alakja (IGEI_ATTEST) vagy -ik-es alakja előfordul a Károliban."""
    return _att_igei(c) or _ik_ige(c)


# a -nak/-nek nincs benne: az igei T/3-mal közös, nem dönt
_NEVSZOI_RAG = ('t', 'ot', 'et', 'at', 'ban', 'ben', 'ra', 're', 'ról', 'ről', 'ba', 'be', 'ból', 'ből',
                'hoz', 'hez', 'val', 'vel', 'ért')


# egyértelmű névszói esetragok (az -at/-et/-t nem: igéből is képez főnevet, kezd-et, áll-at)
_ESETRAG = ('ban', 'ben', 'ra', 're', 'ba', 'be', 'ból', 'ből', 'ról', 'ről', 'hoz', 'hez', 'höz')


def _nevszoi(w):
    """Az alak névszói raggal is előfordul a Károliban (halál: halálra, halált)."""
    return any((w + r) in KIS for r in _NEVSZOI_RAG)


# Képzett igealak (DT130 (10)): a -hat/-het képzős és a szenvedő igealak külön szótári alak, alapigével
_HATHET = re.compile(r'^(.+?)(hat|het)(játok|jétek|ják|jék|juk|jük|ja|je|nánk|nénk|nák|nék|ná|né|na|ne|unk|ünk|tok|tek|tök|'
                     r'nak|nek|ott|ett|om|em|öm|ok|ek|ök|od|ed|ik|sz|i|ja)?$')
_HATHET_ALAP = {'me': 'megy', 'te': 'tesz', 've': 'vesz', 'vi': 'visz', 'hi': 'hisz', 'le': 'lesz', 'jö': 'jön',
                'e': 'eszik', 'i': 'iszik'}
_SZENVEDO = re.compile(r'^(.+?)(tat|tet|at|et)(ik|nak|nek|ott|ett|ék|ának|ének|tak|tek|ván|vén|ni|nék|nának|nének)$')
# Mai igei ragozás (simplemma nélkül, igei attesztációval): a leghosszabb végződés előbb
_MAI_VEG = sorted({'játok', 'jétek', 'ják', 'jék', 'juk', 'jük', 'jatok', 'jetek', 'tátok', 'tétek', 'ottak', 'ettek',
                   'öttek', 'tak', 'tek', 'ottam', 'ettem', 'öttem', 'tam', 'tem', 'ottál', 'ettél', 'öttél', 'tál', 'tél',
                   'ottunk', 'ettünk', 'öttünk', 'tunk', 'tünk', 'ott', 'ett', 'ött', 'unk', 'ünk', 'nak', 'nek', 'tok',
                   'tök', 'ok', 'ek', 'ök', 'om', 'em', 'öm', 'sz', 'ja', 'je', 'ta', 'te', 'i', 'ni', 'ani', 'eni', 'va',
                   've', 'tad', 'ted', 'od', 'ed', 'öd', 'jon', 'jen', 'jön', 'jak', 'jek', 'janak', 'jenek', 'nék', 'nánk', 'nénk', 'nák'},
                  key=len, reverse=True)
_SZEMELYRAG = ('nak', 'nek', 'tok', 'tek', 'tök', 'ok', 'ek', 'ök', 'unk', 'ünk', 'om', 'em', 'öm')
_HASONULT = re.compile(r'^(.*)(ss|zz|cc)(a|e|ák|ék|uk|ük|átok|étek|on|en|ön|anak|enek|unk|ünk|ad|ed|ál|él|ék|ák)$')


def _ige_to(c):
    """A c igető szótári alakja igei attesztációval (-ik-es alak előbb), vagy None."""
    if len(c) < 2:
        return None
    if _ik_ige(c) and c not in KIS and not re.search(r'(tat|tet|ít|szt)$', c):
        return c + 'ik'
    if _att_igei(c):
        # igeként igazolt tő: ha az -ik-es alak is előfordul, és a puszta tő önállóan nem, az -ik-es a szótári alak
        # (megháborod-ott -> megháborodik)
        if (c + 'ik') in KIS and c not in KIS and c[-1:] not in _MGH and not re.search(r'(tat|tet|ít|szt)$', c):
            return c + 'ik'
        if _VALTOZAT == 'A' and _lem(c) == c + 'ik':
            return c + 'ik'
        return c
    return None


def _igekotovel(c, f):
    """f(c), vagy ha c igekötővel kezdődik, igekötő + f(maradék); visszaad (szótári alak, alapige) vagy None."""
    t = f(c)
    if t:
        return t, ''
    for ik in IGEKOTO:
        if c.startswith(ik) and len(c) - len(ik) >= 2:
            t = f(c[len(ik):])
            if t:
                return ik + t, t
    return None


def _kepzett(w2):
    """-hat/-het és szenvedő igealak: (szótári alak, alapige) vagy None."""
    if _VALTOZAT == 'B':
        return None
    m = _HATHET.match(w2)
    if m:
        alap = m.group(1)
        ered = None
        if alap in _HATHET_ALAP:
            ered = (alap + m.group(2), _HATHET_ALAP[alap])
        else:
            r = _igekotovel(alap, _ige_to)
            if r:
                # az alapige az igekötő és a képző nélküli ige (elérheted -> elérhet, alapige: ér)
                ered = (alap + m.group(2), _alapige(r[0]))
        if ered:
            _NYOM.append(('C', 'hat/het', None))
            return ered
    m = _SZENVEDO.match(w2)
    if m:
        lemma = m.group(1) + m.group(2) + 'ik'
        kepzett = m.group(1) + m.group(2)
        # a -tat/-tet/-at/-et előtti rész+képző önálló igeként igazolt: múlt vagy műveltető, nem szenvedő (égettek, megismertetni)
        if lemma in KIS and kepzett not in KIS and not _att_igei(kepzett):
            r = _igekotovel(m.group(1), _ige_to)
            if r:
                _NYOM.append(('C', 'szenvedo', None))
                return lemma, _alapige(r[0])
    return None


def _alapige(t):
    """Az igekötő nélküli ige (megver -> ver), ha a maradék igeként igazolt; különben t."""
    for ik in IGEKOTO:
        if t.startswith(ik) and len(t) - len(ik) >= 2:
            r = _ige_to(t[len(ik):]) or (t[len(ik):] if t[len(ik):].endswith('ik') and t[len(ik):] in KIS else None)
            if r:
                return r
    return t


def _mai_ige(w2):
    """Mai igei ragozás leválasztása igei attesztációval (feloldja, bíznak, megütközzék): (szótári alak, alapige)."""
    if _VALTOZAT == 'B':
        return None
    for v in _MAI_VEG:
        if w2.endswith(v) and len(w2) - len(v) >= 3 and not (
                v[0] == 't' and w2[-len(v) - 1] in _MGH) and not (
                v in _SZEMELYRAG and w2[-len(v) - 1] in 'aáeé'):  # születte-nek ↛  # a -ta/-te/-tam … múlt mássalhangzós tőre jár (nevezete ↛ neveze)
            r = _igekotovel(w2[:-len(v)], _ige_to)
            if r:
                _NYOM.append(('M', v, None))
                return r
    m = _HASONULT.match(w2)
    if m:
        alap = {'ss': ('t', 's', 'sz'), 'zz': ('z', 'sz'), 'cc': ('c',)}[m.group(2)]
        for veg in alap:
            r = _igekotovel(m.group(1) + veg, _ige_to)
            if r:
                _NYOM.append(('M', m.group(2), None))
                return r
    return None


def _nevszo_to(w, nev=False, szigoru=False, laza=False):
    """Rag és birtokos jel leválasztása. A maradék akkor elfogadott, ha tőváltó-táblás, vagy a Károliban önálló
    szóalakként előfordul (névnél nagybetűvel mondat belsejében, köznévnél kisbetűvel, és a simplemma is szótári
    alaknak tartja). Szigorú mód (a simplemma szótári alaknak tartja w-t, pl. istenem, föld, halom): csak birtokos
    jel, és a maradék tőváltó-táblás, vagy legalább 4 betű és a Károliban legalább háromszor olyan gyakori, mint w.
    Laza mód (a simplemma a szót nem ismeri): a simplemmának ismeretlen maradék is elfogadott, ha a Károliban
    legalább kétszer önállóan előfordul. A tőváltó-táblás jelöltet, egyébként a leggyakoribbat adja; ha nincs elfogadott, None."""
    tablas, jeloltek = [], []
    rovid_ok = set()  # a magánhangzós birtokos jellel vagy birtokos jel nélkül kapott jelöltek
    alapok = [(w, 0)]
    if not szigoru:
        alapok += [(w[:-len(r)], len(r)) for r in RAG if w.endswith(r) and len(w) - len(r) >= 2]
        alapok += [(_hosszitas_vissza(a), 0) for a, h in alapok if h and _hosszitas_vissza(a) != a]
    m = None if szigoru else re.match(r'^(.*)(nny|ssz|zzs|ggy|tty|lly|ccs|bb|dd|ff|gg|kk|ll|mm|nn|pp|rr|ss|tt|vv|zz)[áé]$', w)
    if m:
        alapok.append((m.group(1) + {'nny': 'ny', 'ssz': 'sz', 'zzs': 'zs', 'ggy': 'gy', 'tty': 'ty', 'lly': 'ly',
                                     'ccs': 'cs'}.get(m.group(2), m.group(2)[0]), -1))
    for a, rhossz in alapok:
        # az -m/-d birtokos jel kötőhangzó nélkül csak magánhangzó után áll (atyá-m; föld ↛ föl + -d)
        lista = [(a, 0)] + [(a[:-len(b)], len(b)) for b in BIRT if a.endswith(b) and len(a) - len(b) >= 2 and not (
            b in ('m', 'd') and a[:-len(b)][-1:] not in _MGH) and not (b in ('ai', 'ei') and a[:-2].endswith('i'))]
        b_mgh = {a[:-len(b)]: b for b in BIRT if a.endswith(b) and b in _MGH_BIRT}
        for t, bh in lista:
            if a == w and bh == 0:
                continue
            if bh == 0 and rhossz == -1 and (t in NAGY_BELUL if nev else t in KIS):
                jeloltek.append(t)
            for t2 in dict.fromkeys((t, _hosszitas_vissza(t))):  # rendezett (a halmaz bejárása hash-függő volt)
                kulcs = t2.lower()
                if kulcs in TOVALTO:
                    v = TOVALTO[kulcs]
                    tablas.append((v[:1].upper() + v[1:] if nev else v, kulcs))
                elif szigoru:
                    if len(t2) >= 4 and t2 in KIS and _gyak(t2) >= 3 * max(_gyak(w), 1):
                        jeloltek.append(t2)
                elif nev:
                    if t2 in NAGY_BELUL and len(t2) >= 2:
                        jeloltek.append(t2)
                elif (laza and _VALTOZAT != 'A' and bh and len(t2) >= 5 and KIS.get(t2, 0) < 2
                      and re.search(r'(ás|és|ság|ség)$', t2)):
                    # simplemma nélkül: -ás/-és/-ság/-ség képzős főnév birtokos/ragos alakja attesztáció nélkül is
                    # (dicsekvés-ének, születés-e); a csupasz-tő lépés -a/-e szabályának párja
                    jeloltek.append(t2)
                    rovid_ok.add(t2)
                elif t2 in KIS and len(t2) >= 3 and (
                        (_ismert(t2) and _lem(t2) == t2) or (laza and not _ismert(t2) and KIS[t2] >= 2)):
                    jeloltek.append(t2)
                    if bh == 0 or a[len(t):] in _MGH_BIRT or b_mgh.get(t):
                        rovid_ok.add(t2)
    if tablas:
        _NYOM.append(('T', tablas[0][1], None))
        return tablas[0][0]
    if not jeloltek:
        return None
    _NYOM.append(('L', None, None))
    if _VALTOZAT in ('C', 'CK') and not nev and not szigoru:
        # simplemma nélkül a birtokos jel nem szűrődik ki: a rövidebb, legalább kétszer attesztált jelölt nyer
        # (testvérének: testvér, nem testvére)
        jo = [t for t in jeloltek if _gyak(t) >= 2 and t in rovid_ok] or None
        if jo:
            return min(jo, key=lambda t: (len(t), -_gyak(t)))
    return max(jeloltek, key=lambda t: (_gyak(t), len(t)))


_CSUPASZ_BIRT = ('jaink', 'jeink', 'aink', 'eink', 'jaid', 'jeid', 'jaim', 'jeim', 'aid', 'eid', 'aim', 'eim', 'jai', 'jei',
                 'ai', 'ei', 'ánk', 'énk', 'átok', 'étek', 'ám', 'ém', 'ád', 'éd', 'ad', 'ed', 'od', 'öd', 'ja', 'je', 'a', 'e')


def _csupasz(t, nev=False):
    """Ha az eredmény még birtokos alak (szolgája, búsulása, Istene, barátai, háza, atyám), és a csupasz töve a
    Károliban önállóan előfordul, legalább harmadannyiszor, mint t, akkor a csupasz tövet adja. A puszta -a/-e
    birtokos jelnél a tő legalább 4 betű (a v2 feltétele), a többinél legalább 3."""
    lex = NAGY_BELUL if nev else KIS
    if not nev and (any(_att(t, v) for v in IGEI_ATTEST) or any(_att(t, v) for v in ('ja', 'je', 'ják', 'jék', 'ta', 'te', 'ták', 'ték', 'á', 'é'))):
        return t  # igeként igazolt tő (fogad, marad, tagad): nem birtokos alak
    for b in _CSUPASZ_BIRT:
        if t.endswith(b) and len(t) > len(b):
            if b in ('ai', 'ei') and t[:-2].endswith('i'):
                continue  # -i képzős melléknév (babilóniai), nem birtokos többes
            if b[0] in 'áé':
                # hosszú magánhangzós birtokos jel: a tővégi -a/-e nyúlt meg (atyám -> atya)
                c = t[:-len(b)] + ('a' if b[0] == 'á' else 'e')
            else:
                c = _hosszitas_vissza(t[:-len(b)])
            if len(c) >= (4 if nev and b in ('a', 'e') else 3) and c in lex and lex[c] >= (2 if len(c) == 3 else 1) and (
                    b[0] in 'áé' or 3 * lex[c] >= lex.get(t, 0)) and (
                    nev or not _ismert(c) or _lem(c) == c):
                _NYOM.append(('L', None, None))
                return c
            if not nev and b in ('a', 'e') and re.search(r'(ság|ség|ás|és)$', c) and len(c) >= 5:
                # -ság/-ség képzős főnév birtokos -a/-e-vel (kereksége -> kerekség), attesztáció nélkül is
                _NYOM.append(('L', None, None))
                return c
    return t


def _simplemma_ige(c):
    """Az A-ban: a simplemma igeként ismeri c-t — főnévi igeneve vagy múlt idejű alakja c-re (vagy c+ik-re)
    lemmatizál (igei tudás, nem a névszói „ismert szó” próba; házni ↛ ház)."""
    for v in ('ni', 'ani', 'eni', 'ott', 'ett', 'ött', 'tt'):
        if _ismert(c + v) and _lem(c + v) in (c, c + 'ik'):  # csak ismert alak (királyni: ismeretlen, nem igazol)
            return True
    return False


def _ige_jelolt(c):
    """A jelölt tő igeként igazolva (v3, szigorított): igei alakja előfordul a Károliban (`_igei`). Az A-ban a
    simplemma dönti el az -ik-es és a tárgyas olvasat közti választást. Visszaadja a szótári alakot vagy None-t."""
    if _VALTOZAT == 'B' or len(c) < 2 or c in IGEKOTO:
        return None  # az igekötő önmagában nem igető (kié ↛ ki, felének ↛ fel)
    if len(c) == 2:
        # kétbetűs igető (ad-ának, öl-é): csak szigorú igei attesztációval
        if _ik_ige(c):
            return c + 'ik'
        return c if _att_igei(c) else None
    ik = c + 'ik'
    _a_ik = _VALTOZAT == 'A' and _lem(c) == ik
    if _VALTOZAT == 'A':
        # -ik-es ige előbb: a simplemma szótári alaknak tartja, és a Károliban előfordul (az -ik-es alak igei)
        if _ismert(ik) and _lem(ik) == ik and ik in KIS and c[-1:] not in _MGH and c not in KIS and c not in IGEKOTO:
            return ik
        if _ismert(c) and _lem(c) in (c, ik) and (_igei(c) or _simplemma_ige(c)):
            return _lem(c)
    # műveltető/tárgyas képzős tőnél (-tat/-tet/-ít/-szt) az -ik a tárgyas T/3 (helyeztetik), nem -ik-es ige
    if _ik_ige(c) and c not in KIS and not _ismert(ik) and not re.search(r'(tat|tet|ít|szt)$', c):
        return ik
    if _att_igei(c):
        # igeként igazolt tő: ha az -ik-es alak is előfordul, és a puszta tő önállóan nem, az -ik-es a szótári alak
        # (megháborod-ott -> megháborodik)
        if (c + 'ik') in KIS and c not in KIS and c[-1:] not in _MGH and not re.search(r'(tat|tet|ít|szt)$', c):
            return c + 'ik'
        return ik if _a_ik else c
    return None


def _regies_ige(w2):
    if w2.endswith(('felé', 'felől')):
        return None  # irányhatározószó (fölfelé, lefelé, kifelé)
    jeloltek = [(v, j, re.sub(v, '', w2)) for v, j in IGEVEG if re.search(v, w2)]
    # felszólító: -jál/-jél; kettőzött sziszegővel -zzál/-zzél, -sszál/-sszél (régies E/2)
    m = re.match(r'^(.*)j(ál|él)$', w2)
    if m:
        jeloltek.append(('j', 'felszolito.E2', m.group(1)))
    m = re.match(r'^(.*)(zz|ssz|ss|zzs)(ál|él)$', w2)
    if m:
        jeloltek.append(('j', 'felszolito.E2', m.group(1) + {'zz': 'z', 'ssz': 'sz', 'ss': 's', 'zzs': 'zs'}[m.group(2)]))
    # mai felszólító -j + személyrag (éljen, maradjanak): nem régies, jegy nélkül
    m = re.match(r'^(.*[^j])j(on|en|ön|enek|anak|unk|ünk|atok|etek|ak|ek)$', w2)
    if m:
        jeloltek.append(('jm', '', m.group(1)))
    for v, jegy, c in jeloltek:
        # az -a/-e (múlt, alanyi) csak akkor, ha az alak nem ismert névszó (fia, keze, háza)
        if v in (r'a$', r'e$') and _ismert(w2):
            continue
        if re.search(r'(ság|ség|mány|mény|vány|vény|alom|elem)$', c) or (
                re.search(r'(ás|és)$', c) and (len(c) >= 6 or _att_igei(c[:-2]))):
            continue  # R1 (ELLENOR_F94): névszóképzős tő nem igető (születés-e, lakosság-a, teremtés-ének); a rövid ás/vés ige marad
        if v in (r'ának$', r'ének$', r'a$', r'e$') and any(
                (c + ('á' if v in (r'ának$', r'a$') else 'é') + r) in KIS for r in _ESETRAG + ('t', 'vel', 'val')):
            continue  # R2 (ELLENOR_F94): birtokos névszó — a megnyújtott tő névszói raggal is áll (felekezeté-ben)
        if v in (r'ának$', r'ének$', r'a$', r'e$') and any((c + r) in KIS for r in _ESETRAG):
            continue  # a tő egyértelmű névszói esetraggal is előfordul (fej-re, szív-ben): fejének, szívének névszó
        if v in (r'ál$', r'él$', r'ék$') and _nevszoi(w2):
            continue  # a -ál/-él/-ék végű névszó (halál, hajlék, maradék) névszói raggal is előfordul
        if v == r'ék$' and re.search(r't{1,2}ék$', w2) and _att_igei(re.sub(r't{1,2}ék$', '', w2)):
            continue  # -ték/-tték: múlt T/3 tárgyas (megismer-ték), nem régies E/1
        if v in (r'ván$', r'vén$') and len(c) >= 4 and c[-1] not in _MGH and c not in IGEKOTO and _VALTOZAT != 'B' and (
                (_VALTOZAT == 'A' and _ismert(c)) or _igei(c)
                or any(_att(c, x) for x in ('á', 'é', 'ék', 'ának', 'ének', 'nak', 'nek', 'ja', 'je', 'ni'))):
            # a -ván/-vén határozói igenév maga igei: a ritka ige (temetget-vén) más alak nélkül is elfogadott
            t = _ige_jelolt(c) or (c + 'ik' if _VALTOZAT == 'A' and _lem(c) == c + 'ik' else c)
            _NYOM.append(('R', v, jegy))
            return t
        if v == 'jm' and len(c) == 2 and _VALTOZAT != 'B' and _igei(c):
            # kétbetűs igető a -j- előtt (él-jen, ál-ljon nem): csak igei attesztációval
            _NYOM.append(('R', v, jegy))
            return c
        t = _ige_jelolt(c)
        if t:
            _NYOM.append(('R', v, jegy))
            return t
        for ik in IGEKOTO:
            if c.startswith(ik):
                if len(c) - len(ik) < 3:
                    break  # az igekötő mögött legalább 3 betű (megkiván ↛ megki)
                t = _ige_jelolt(c[len(ik):])
                if t:
                    _NYOM.append(('R', v, jegy))
                    _NYOM.append(('A', t, None))
                    return ik + t
    return None


def _kivetel(w):
    if w in KIVETEL:
        _NYOM.append(('X', w, JEGY.get(w, '')))
        return KIVETEL[w]
    for ik in IGEKOTO:
        if w.startswith(ik) and w[len(ik):] in IGEI:
            # az igekötős alak saját jegye (ha van) elsőbb az igekötő nélküli alakénál (megevék, DT-F94f)
            _NYOM.append(('X', w[len(ik):], JEGY.get(w, JEGY.get(w[len(ik):], ''))))
            _NYOM.append(('A', KIVETEL[w[len(ik):]], None))
            return ik + KIVETEL[w[len(ik):]]
    return None


def to(alak):
    """A szóalak szótári alakja (a helyesírási réteg után: mai írásmódú tővel; l. elemez())."""
    del _NYOM[:]
    if re.search(r'..-é$', alak):
        # -é kérdőszócska kötőjellel (láttad-é, értheti-é)
        _NYOM.append(('Q', None, None))
        alak = alak[:-2]
    w = alak.lower()
    if _VALTOZAT == 'CK' and w in K and not (alak[:1].isupper() and NAGY_BELUL.get(alak, 0) > KIS.get(w, 0)):
        _NYOM.append(('K', w, None))
        return K[w][0]
    nev = alak[:1].isupper() and _kivetel(w) is None and NAGY_BELUL.get(alak, 0) > KIS.get(w, 0)
    if nev:
        del _NYOM[:]
        _NYOM.append(('N', None, None))
        return _csupasz(_nevszo_to(alak, nev=True) or alak, nev=True)
    del _NYOM[:]
    t = _to_koznev(w)
    if t in KIVETEL.values() or any(n[0] in ('R', 'M', 'C', 'A', 'X') for n in _NYOM):
        return t  # kivétel vagy igei elemzés: a birtokos jel leválasztása nem alkalmazható (fogad ↛ fog)
    return _csupasz(t)


def _to_koznev(w):
    _ONMAGA[0] = _helyesiras_csendes(w)
    k = _kivetel(w)
    if k:
        return k
    w2 = _helyesiras(w)
    k = _kivetel(w2)
    if k:
        return k
    # névmási/birtokos személyrag, régies -ök -> -ük (közülök, előttök, erejök, legelőjök)
    if w2.endswith('ök') and not _ismert(w2) and (_ismert(w2[:-2] + 'ük') or (w2[:-2] + 'ük') in KIS):
        w2 = w2[:-2] + 'ük'
    r = _kepzett(w2)
    if r:
        if r[1] and r[1] != r[0]:
            _NYOM.append(('A', r[1], None))
        return r[0]
    t = _regies_ige(w2)
    if t:
        return t
    if _VALTOZAT in ('C', 'CK'):
        r = _mai_ige(w2)
        if r:
            ap = r[1] or _alapige(r[0])
            if ap and ap != r[0]:
                _NYOM.append(('A', ap, None))
            return r[0]
    t = _koznev_lem(w2)
    if t == w2 and _VALTOZAT == 'A':
        mentes = list(_NYOM)
        r = _mai_ige(w2)
        if r:
            ap = r[1] or _alapige(r[0])
            if ap and ap != r[0]:
                _NYOM.append(('A', ap, None))
            return r[0]
        _NYOM[:] = mentes
    if t == w2:
        # igekötő + ismeretlen ige (meggyarapodnak, feloldja): a maradék tövezése, ha igeként igazolt
        for ik in IGEKOTO:
            if w2.startswith(ik) and len(w2) - len(ik) >= 4:
                mentes = list(_NYOM)
                r = _to_koznev(w2[len(ik):])
                if r != w2[len(ik):] and (r.endswith('ik') or _igei(r) or (_ismert(r) and _VALTOZAT == 'A' and _igei(r))):
                    _NYOM.append(('A', r, None))
                    return ik + r
                _NYOM[:] = mentes
                break
    return t


def _koznev_lem(w2):
    lem = _lem(w2)
    elotag = lem[:-2] if lem.endswith('ik') else lem
    for kepzo in ('ság', 'ség', 'ás', 'és'):
        maradek = w2[len(elotag + kepzo):]
        if lem != w2 and w2.startswith(elotag + kepzo) and (
                not maradek or maradek[0] in _MGH or any(maradek.startswith(r) for r in RAG)):  # bíráskodik ↛ bírás
            # -ás/-és, -ság/-ség képzős főnév: a főnév a szótári alak, nem az alapszó (kijavítása -> kijavítás,
            # megkeményedés, hamissága -> hamisság)
            _NYOM.append(('S', None, None))
            return elotag + kepzo
    if lem == w2 and _ismert(w2):
        # a simplemma szótári alaknak tartja (föld, mert, istenem): csak szigorú birtokosjel-leválasztás
        return _nevszo_to(w2, szigoru=True) or w2
    if lem == w2 or not _ismert(lem):
        # a simplemma nem ismeri: névszói leválasztás
        return _nevszo_to(w2, laza=True) or lem
    # a simplemma túl rövid tövet adott (gyalázatot -> gyaláz): a névszói leválasztás hosszabb, attesztált töve nyer
    t = _nevszo_to(w2)
    if t and len(t) > len(lem):
        return t
    _NYOM.append(('S', None, None))
    if re.search(r'(a|e|ja|je)$', lem):
        # a simplemma birtokos alakon megállt (háza, igaza): második menet
        lem2 = _lem(lem)
        if lem2 != lem and len(lem2) >= 3 and _ismert(lem2):
            return lem2
    return _nevszo_to(lem, szigoru=True) or lem


_SULY = {'modell_ellenorizetlen': 2, 'manual': 1, 'korpusz_strong': 0}


def elemez(alak):
    """A szóalak teljes elemzése a szótárialak-táblához (SEMA 2.27): szotari_alak (Károli-írásmód), szotari_alak_mai,
    alapige, tovabbi_elfogadhato, modszer (k_tabla | kivetel | nev | szabaly | simplemma | lexikon), szabaly_forras,
    regies_jegy."""
    t = to(alak)
    nyom = list(_NYOM)
    tipusok = {n[0] for n in nyom}
    if 'K' in tipusok:
        global _VALTOZAT
        sz, mai, ap, tov = K[next(n[1] for n in nyom if n[0] == 'K')]
        # a régies jegy a K-sorra is: a szabályág (C) elemzéséből, ha az ugyanarra a szótári alakra jut
        _VALTOZAT = 'C'
        try:
            belso = elemez(alak)
        finally:
            _VALTOZAT = 'CK'
        jegy = belso['regies_jegy'] if {belso['szotari_alak'], belso['szotari_alak_mai']} & {sz, mai} else ''
        return dict(szotari_alak=sz, szotari_alak_mai=mai, alapige=ap, tovabbi_elfogadhato=tov, modszer='k_tabla',
                    szabaly_forras='', regies_jegy=jegy)
    mai = MAI.get(t, t)
    sz = t
    forrasok = []
    for n in nyom:
        if n[0] == 'H':
            forrasok.append(szabaly_forras(n[1]))
            if n[1] in _VISSZA:
                minta, csere = _VISSZA[n[1]]
                sz = re.sub(minta, csere, sz, count=1)
        elif n[0] == 'T':
            forrasok.append(szabaly_forras(n[1]))
        elif n[0] in ('R', 'C', 'M'):
            forrasok.append('modell_ellenorizetlen')
    jegy = ''
    for n in nyom:
        if n[0] == 'R' and n[2]:
            jegy = n[2]
            # N-F94e: az -ik-es igék régies múlt E/3-a is -ék (tartózkodék, uralkodék, esék); a nem -ik-es igéknél az -ék E/1
            # (láték = láttam). A szabályág (R) jegyére; a kivételtábla saját jegyét nem írja felül.
            if jegy == 'mult.E1' and t.endswith('ik'):
                jegy = 'mult.E3'
        elif n[0] == 'X' and n[2]:
            jegy = n[2]
    alapige = next((n[1] for n in nyom if n[0] == 'A'), '')
    if alapige == t:
        alapige = ''
    if 'X' in tipusok:
        modszer = 'kivetel'
    elif 'N' in tipusok:
        modszer = 'nev'
    elif tipusok & {'H', 'T', 'R', 'C', 'M'}:
        modszer = 'szabaly'
    elif 'S' in tipusok:
        modszer = 'simplemma'
    else:
        modszer = 'lexikon'
    return dict(szotari_alak=sz, szotari_alak_mai=mai, alapige=alapige,
                tovabbi_elfogadhato=TOVABBI.get(alak.lower(), ''), modszer=modszer,
                szabaly_forras=max(forrasok, key=lambda f: _SULY[f]) if forrasok else '', regies_jegy=jegy)
