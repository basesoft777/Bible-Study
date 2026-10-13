"""Hibrid Károli-szótövező, 2. változat (F94.1, FELADATOK #94: az előmérés `hibrid.py`-jának átvétele, az A
változatban viselkedésre változatlanul). Saját szabályok + kivételtábla + a Károli saját szóalak-lexikona
(`adat/szoto/karoli_lexikon.tsv`, l. `lexikon_epit.py`) + simplemma (a kód MIT; a nyelvi adat licence: DT-F94c).
Használat: from hibrid import to; to('teremté') -> 'teremt'.

Változatok (`valtozat('A' | 'B' | 'C')`, a DT-F94c méréséhez; az alapértelmezés 'A'):
- A: az előmérés v2-je — a simplemma tartalék-lemmatizáló és igető-igazoló is;
- B: simplemma nélkül — nincs tartalék-lemmatizáló (a lemmatizáló az alakot adja vissza), és nincs igető-igazolás
  (a régies igevégződés-réteg jelöltjét semmi nem igazolja, ezért a réteg nem vág);
- C: simplemma nélkül, a tartalék-lemmatizáló is kimarad, de az igető-igazolást a Károli-lexikon végzi:
  a jelölt c tő elfogadott, ha (1) c önálló kisbetűs alakként előfordul a Károliban (E/3 jelen: teremt, lát), vagy
  (2) c+'ik' előfordul, és c nem -tat/-tet/-ít/-szt végű (születik, emlékezik), vagy (3) c valamely igei ragos
  alakja előfordul (IGE_ATTEST, ugyanaz a lista, mint az A-ban: -ni, -ani, -eni, -ott, -ett, -ött, -tt, -ván, -vén,
  -nak, -nek, -tek, -tok, -tök). Az (1) az A-ban a simplemma szótári-alak próbáját helyettesíti.
A simplemma csak az A változatban kell (importja ott történik).

Az 1. változathoz képest (2026-10-13, fejlesztési halmaz: az első és a független minta):
- nagybetűs alak: tulajdonnév, ha a Károliban mondat belsejében gyakrabban áll nagybetűvel, mint kisbetűvel;
  különben köznévként tövez (Ímé, Istene a mondat elején);
- tulajdonnévről és köznévről a rag/birtokos jel levágása, a maradék korpusz-attesztációjával (Izráelnek, Istenem);
- tőváltó névszók táblája (lelk- → lélek, magv- → mag, tav- → tó …);
- a simplemma birtokos alakon megálló eredményének (háza, igaza) második menete;
- ragos személyes névmások (bennök, reám, belőlük → személyes névmás, 3. döntés);
- régies igealak: igekötő-leválasztás és korpusz-attesztáció (megváltá, kifeszíté, elhamvadának), -jál/-jél felszólító;
- helyesírás: cz → c, kiván- → kíván-, -ök → -ük (névmási személyrag);
- a nincs/nincsen külön tő (nem a van alakja); jő, lenne → jön, lesz;
- az eredményből a nem-betű karakterek törlése (leborul.)."""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import simplemma
except ImportError:  # a B és C változat nélküle fut
    simplemma = None

_VALTOZAT = 'A'


def valtozat(v):
    """A mérési változat beállítása: 'A' (simplemmával), 'B' (nélküle), 'C' (nélküle, Károli-lexikonos igazolással)."""
    global _VALTOZAT
    if v not in ('A', 'B', 'C'):
        raise ValueError(v)
    if v == 'A' and simplemma is None:
        raise RuntimeError('az A változathoz a simplemma kell')
    _VALTOZAT = v


# 0. Korpusz-lexikon (a sor-formátum: alak, kisbetus, nagy_belul, nagy_kezdo; a #-sorok és a fejléc átugorva)
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LEX = os.path.join(_REPO, 'adat', 'szoto', 'karoli_lexikon.tsv')
KIS, NAGY_BELUL = {}, {}


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


if os.path.exists(_LEX):
    lexikon_betolt()

# 1. Károli-helyesírás -> mai helyesírás (szóalakon, a tövezés előtt)
HELYESIRAS = [
    (r'űl$', 'ül'), (r'űle', 'üle'), (r'^szűl', 'szül'), (r'körűl', 'körül'), (r'sűly', 'süly'),
    (r'nyny', 'nny'), (r'^setét', 'sötét'), (r'cz', 'c'), (r'^kiván', 'kíván'),
]

# 2. Kivételtábla: rendhagyó és tőváltó alakok (kisbetűs alak -> tő), általános Károli-ismeret alapján
KIVETEL = {}
IGEI = set()


def _k(to, *alakok, ige=False):
    for a in alakok:
        KIVETEL[a] = to
        if ige:
            IGEI.add(a)


_k('mond', 'monda', 'mondá', 'mondék', 'mondának', 'mondotta', 'mondja', ige=True)
_k('van', 'vala', 'valának', 'valék', 'valál', 'valánk', 'valátok', 'volt', 'voltak', 'vagyon', 'vagynak', 'vagyok', 'vagyunk', 'vagytok',
   ige=True)
_k('nincs', 'nincsen', 'nincsenek')
_k('lesz', 'lőn', 'lőnek', 'lőnének', 'lőne', 'lészen', 'lésznek', 'legyen', 'legyenek', 'lett', 'lettek',
   'lenne', 'lennének', 'lennék', 'lennénk', 'lennétek', 'lennél', ige=True)
_k('vesz', 'vevé', 'vevék', 'vevének', 'vőn', 'vőnek', 'vegye', 'vegyed', 'vegyétek', 'vett', 'vette', ige=True)
_k('tesz', 'tevé', 'tevék', 'tevének', 'tőn', 'tőnek', 'tegye', 'tegyed', 'tett', 'tette', ige=True)
_k('megy', 'méne', 'menének', 'menék', 'mene', 'ment', 'mentek', 'menj', 'menjetek', ige=True)
_k('jön', 'jöve', 'jövének', 'jövék', 'jőve', 'jőjön', 'jövel', 'jöjj', 'jő', 'jőnek', 'jőjj', 'jőjjön', 'jőjjenek',
   'jövén', ige=True)
_k('eszik', 'evé', 'evék', 'evének', 'egyél', 'egyetek', 'egyék', 'evett', ige=True)
_k('iszik', 'ivá', 'ivék', 'ivának', 'igyál', 'igyatok', 'igyék', 'ivott', ige=True)
_k('hisz', 'hivé', 'hivének', 'higyj', 'higyjetek', 'hitt', 'hittek', ige=True)
_k('visz', 'vivé', 'vivék', 'vivének', 'vigye', 'vidd', 'vitt', 'vitte', ige=True)
_k('ő', 'néki', 'nékik', 'vele', 'velök', 'velük', 'őnéki', 'őnékik', 'őtet', 'őket', 'őt', 'ővele', 'ő')
_k('én', 'nékem', 'engem', 'engemet', 'velem', 'énnékem')
_k('te', 'néked', 'téged', 'tégedet', 'veled', 'tenéked')
_k('mi', 'nékünk', 'minket', 'minékünk', 'velünk')
_k('ti', 'néktek', 'titeket', 'tinéktek', 'veletek')
_k('fiú', 'fia', 'fiai', 'fiak', 'fiakat', 'fiaid', 'fiaim', 'fiam', 'fiad', 'fiát', 'fiának', 'fiamnak', 'fiadnak', 'fiaitok', 'fiainak', 'fiaiknak', 'fiaival', 'fiaid')
_k('úr', 'ura', 'urak', 'uram', 'urad', 'urát', 'urának', 'uramnak', 'uraknak', 'urunk', 'urunknak', 'uratok', 'urat', 'urakat')
_k('szó', 'szava', 'szavát', 'szavának', 'szavam', 'szavamat', 'szavad', 'szavadat', 'szavai', 'szavait', 'szavak', 'szavakat')
_k('fű', 'füvet', 'fűvet', 'füve', 'füvét')
_k('atyafi', 'atyjafia', 'atyjafiának', 'atyádfia', 'atyádfiának', 'atyámfia', 'atyámfiai', 'atyafiai', 'atyafiait', 'atyafiak', 'atyafiaim', 'atyafiainak')
_k('íme', 'ímé', 'ím', 'ime', 'imé')
for _a in ('azért', 'ezért', 'miért', 'mikor', 'amikor', 'akkor', 'ekkor', 'valamikor', 'semmikor', 'mindenkor'):
    KIVETEL[_a] = _a

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

# 3. Tőváltó névszók: a rag/birtokos jel előtti tőváltozat -> szótári alak
TOVALTO = {
    'lelk': 'lélek', 'ur': 'úr', 'tav': 'tó', 'magv': 'mag', 'sátr': 'sátor', 'derek': 'derék', 'kez': 'kéz',
    'nev': 'név', 'viz': 'víz', 'tüz': 'tűz', 'kenyer': 'kenyér', 'level': 'levél', 'madar': 'madár', 'falv': 'falu',
    'ökr': 'ökör', 'bokr': 'bokor', 'szav': 'szó', 'erej': 'erő', 'lov': 'ló', 'köv': 'kő', 'füv': 'fű', 'nyar': 'nyár',
    'pohar': 'pohár', 'gyöker': 'gyökér', 'tehen': 'tehén', 'szeker': 'szekér', 'kebl': 'kebel', 'terh': 'teher',
    'ajk': 'ajak', 'fark': 'farok', 'dolg': 'dolog', 'torny': 'torony', 'esztendej': 'esztendő', 'idej': 'idő',
    'mezej': 'mező', 'tetej': 'tető', 'fi': 'fiú', 'kegyelm': 'kegyelem', 'félelm': 'félelem', 'értelm': 'értelem',
    'szerelm': 'szerelem', 'eg': 'ég',
}

# 4. Rag- és birtokosjel-listák a névszói leválasztáshoz
RAG = ['éi', 'é', 'nak', 'nek', 'ban', 'ben', 'ból', 'ből', 'tól', 'től', 'hoz', 'hez', 'höz', 'ról', 'ről', 'nál', 'nél', 'val',
       'vel', 'ért', 'ként', 'ig', 'ba', 'be', 'ra', 're', 'vá', 'vé', 'on', 'en', 'ön', 'at', 'et', 'ot', 'öt', 't', 'n']
BIRT = ['jaink', 'jeink', 'aink', 'eink', 'jaim', 'jeim', 'aim', 'eim', 'jaid', 'jeid', 'aid', 'eid', 'jai', 'jei',
        'ai', 'ei', 'atok', 'etek', 'otok', 'ötök', 'unk', 'ünk', 'juk', 'jük', 'jok', 'jök', 'uk', 'ük', 'ok', 'ök', 'ak', 'ek',
        'am', 'em', 'om', 'öm', 'ad', 'ed', 'od', 'öd', 'ja', 'je', 'a', 'e', 'm', 'd', 'i']
IGEKOTO = ['vissza', 'össze', 'utána', 'hozzá', 'széjjel', 'szét', 'meg', 'fel', 'föl', 'ki', 'be', 'el', 'le', 'rá',
           'reá', 'át', 'oda', 'ide', 'alá', 'elő', 'ellen', 'végig', 'után']
IGEVEG = [r'ván$', r'vén$', r'ának$', r'ének$', r'ánk$', r'énk$', r'átok$', r'étek$', r'ál$', r'él$', r'á$', r'é$', r'a$', r'e$']
IGE_ATTEST = ['ni', 'ani', 'eni', 'ott', 'ett', 'ött', 'tt', 'ván', 'vén', 'nak', 'nek', 'tek', 'tok', 'tök']
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
    return _NEMBETU.sub('', simplemma.lemmatize(t, lang='hu'))


def _helyesiras(w):
    for minta, csere in HELYESIRAS:
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


def _nevszo_to(w, nev=False, szigoru=False, laza=False):
    """Rag és birtokos jel leválasztása. A maradék akkor elfogadott, ha tőváltó-táblás, vagy a Károliban önálló
    szóalakként előfordul (névnél nagybetűvel mondat belsejében, köznévnél kisbetűvel, és a simplemma is szótári
    alaknak tartja). Szigorú mód (a simplemma szótári alaknak tartja w-t, pl. istenem, föld, halom): csak birtokos
    jel, és a maradék tőváltó-táblás, vagy legalább 4 betű és a Károliban legalább háromszor olyan gyakori, mint w.
    Laza mód (a simplemma a szót nem ismeri): a simplemmának ismeretlen maradék is elfogadott, ha a Károliban
    legalább kétszer önállóan előfordul. A tőváltó-táblás jelöltet, egyébként a leggyakoribbat adja; ha nincs elfogadott, None."""
    tablas, jeloltek = [], []
    alapok = [(w, 0)]
    if not szigoru:
        alapok += [(w[:-len(r)], len(r)) for r in RAG if w.endswith(r) and len(w) - len(r) >= 2]
        alapok += [(_hosszitas_vissza(a), 0) for a, h in alapok if h and _hosszitas_vissza(a) != a]
    m = None if szigoru else re.match(r'^(.*)(nny|ssz|zzs|ggy|tty|lly|ccs|bb|dd|ff|gg|kk|ll|mm|nn|pp|rr|ss|tt|vv|zz)[áé]$', w)
    if m:
        alapok.append((m.group(1) + {'nny': 'ny', 'ssz': 'sz', 'zzs': 'zs', 'ggy': 'gy', 'tty': 'ty', 'lly': 'ly',
                                     'ccs': 'cs'}.get(m.group(2), m.group(2)[0]), -1))
    for a, rhossz in alapok:
        lista = [(a, 0)] + [(a[:-len(b)], len(b)) for b in BIRT if a.endswith(b) and len(a) - len(b) >= 2]
        for t, bh in lista:
            if a == w and bh == 0:
                continue
            if bh == 0 and rhossz == -1 and (t in NAGY_BELUL if nev else t in KIS):
                jeloltek.append(t)
            for t2 in {t, _hosszitas_vissza(t)}:
                kulcs = t2.lower()
                if kulcs in TOVALTO:
                    v = TOVALTO[kulcs]
                    tablas.append(v[:1].upper() + v[1:] if nev else v)
                elif szigoru:
                    if len(t2) >= 4 and t2 in KIS and _gyak(t2) >= 3 * max(_gyak(w), 1):
                        jeloltek.append(t2)
                elif nev:
                    if t2 in NAGY_BELUL and len(t2) >= 2:
                        jeloltek.append(t2)
                elif t2 in KIS and len(t2) >= 3 and (
                        (_ismert(t2) and _lem(t2) == t2) or (laza and not _ismert(t2) and KIS[t2] >= 2)):
                    jeloltek.append(t2)
    if tablas:
        return tablas[0]
    if not jeloltek:
        return None
    return max(jeloltek, key=lambda t: (_gyak(t), len(t)))


def _csupasz(t, nev=False):
    """Ha az eredmény még birtokos alak (szolgája, búsulása, Istene), és a csupasz töve legalább 4 betű, a Károliban
    önállóan előfordul, és legalább harmadannyiszor, mint t, akkor a csupasz tövet adja."""
    for b in ('ja', 'je', 'a', 'e'):
        if t.endswith(b):
            c = _hosszitas_vissza(t[:-len(b)])
            lex = NAGY_BELUL if nev else KIS
            if len(c) >= 4 and c in lex and 3 * lex[c] >= lex.get(t, 0) and (nev or not _ismert(c) or _lem(c) == c):
                return c
    return t


def _ige_jelolt(c):
    """A jelölt tő (E/3 jelen, alanyi) igeként igazolva: a simplemma ismeri és önmagára (vagy -ik-es alakjára)
    lemmatizálja, vagy a Károliban igei ragos alakja előfordul. Visszaadja a szótári alakot vagy None-t."""
    if len(c) < 3:
        return None
    if _VALTOZAT == 'B':
        return None
    if _VALTOZAT == 'C':
        if c in KIS:
            return c
        if (c + 'ik') in KIS and not re.search(r'(tat|tet|ít|szt)$', c):
            return c + 'ik'
        if any((c + v) in KIS for v in IGE_ATTEST):
            return c
        return None
    # -ik-es ige előbb: a simplemma szótári alaknak tartja (emlékezik, születik), de nem a tárgyas
    # T/3 alakot (elszélesztik -> elszéleszt)
    if _ismert(c + 'ik') and _lem(c + 'ik') == c + 'ik' and (c + 'ik') in KIS:
        return c + 'ik'
    if _ismert(c) and _lem(c) in (c, c + 'ik'):
        return _lem(c)
    # műveltető/tárgyas képzős tőnél (-tat/-tet/-ít/-szt) az -ik a tárgyas T/3 (helyeztetik), nem -ik-es ige
    if (c + 'ik') in KIS and c not in KIS and not _ismert(c + 'ik') and not re.search(r'(tat|tet|ít|szt)$', c):
        return c + 'ik'
    if any((c + v) in KIS for v in IGE_ATTEST):
        return c
    return None


def _regies_ige(w2):
    jeloltek = [(v, re.sub(v, '', w2)) for v in IGEVEG if re.search(v, w2)]
    # felszólító: -jál/-jél; kettőzött sziszegővel -zzál/-zzél, -sszál/-sszél
    m = re.match(r'^(.*)j(ál|él)$', w2)
    if m:
        jeloltek.append(('j', m.group(1)))
    m = re.match(r'^(.*)(zz|ssz|ss|zzs)(ál|él)$', w2)
    if m:
        jeloltek.append(('j', m.group(1) + {'zz': 'z', 'ssz': 'sz', 'ss': 's', 'zzs': 'zs'}[m.group(2)]))
    for v, c in jeloltek:
        # az -a/-e (múlt, alanyi) csak akkor, ha az alak nem ismert névszó (fia, keze, háza)
        if v in (r'a$', r'e$') and _ismert(w2):
            continue
        t = _ige_jelolt(c)
        if t:
            return t
        for ik in IGEKOTO:
            if c.startswith(ik) and len(c) - len(ik) >= 3:
                t = _ige_jelolt(c[len(ik):])
                if t:
                    return ik + t
    return None


def _kivetel(w):
    if w in KIVETEL:
        return KIVETEL[w]
    for ik in IGEKOTO:
        if w.startswith(ik) and w[len(ik):] in IGEI:
            return ik + KIVETEL[w[len(ik):]]
    return None


def to(alak):
    w = alak.lower()
    nev = alak[:1].isupper() and _kivetel(w) is None and NAGY_BELUL.get(alak, 0) > KIS.get(w, 0)
    if nev:
        return _csupasz(_nevszo_to(alak, nev=True) or alak, nev=True)
    t = _to_koznev(w)
    return t if t in KIVETEL.values() else _csupasz(t)


def _to_koznev(w):
    k = _kivetel(w)
    if k:
        return k
    w2 = _helyesiras(w)
    k = _kivetel(w2)
    if k:
        return k
    # névmási személyrag, régies -ök -> -ük (közülök, előttök, erejök)
    if w2.endswith('ök') and not _ismert(w2) and _ismert(w2[:-2] + 'ük'):
        w2 = w2[:-2] + 'ük'
    t = _regies_ige(w2)
    if t:
        return t
    lem = _lem(w2)
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
    if re.search(r'(a|e|ja|je)$', lem):
        # a simplemma birtokos alakon megállt (háza, igaza): második menet
        lem2 = _lem(lem)
        if lem2 != lem and len(lem2) >= 3 and _ismert(lem2):
            return lem2
    return _nevszo_to(lem, szigoru=True) or lem
