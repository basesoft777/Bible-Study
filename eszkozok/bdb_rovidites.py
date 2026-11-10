"""bdb_rovidites.py — a BDB-szöveg egybetűs rövidítéseinek jelölése (N-F131x).

A lexikon-generátor (`lexikon_general.bdb_rovidites_jelol`) és az olvasó-szerver szó-lapja
(`olvaso_szerver/blokkok.py`) ugyanezt a függvényt hívja.

A felhasználó kérése (2026-10-29): „nem lehetne jelölni a szövegben /pl más szinű háttér , hogy a
szó rövidités?”, majd: „ezt a felismerést rakljuk el az olvasó felület számára is”.

A forrás (DictBDB.json) a rövidítő jelet (geres, ׳) a betű ELÉ írja (׳י); a helyes alak a betű utáni
(י׳). A `jelol` az önálló, egybetűs alakot jelöli (<abbr>, címmel), a forrás és a javított alakban is.

A megjelenítés sorrendje (DT-F131z; a lexikon-generátor és az olvasó ugyanígy): `atiras_javit` (a latin betűs
átírások betűkészlet-hibája, `adat/bdb_forras_javitas.tsv` `atiras` / `javitva`, B3) → `heber_sorrend_javit` (a több
szavas kifejezések Biblia által igazolt sorrend-javítása, `heber_sorrend` / `javitva`) → `izolal` (LRM a héber futam után,
ha szám következik) → `jelol`.

A cím: a י Jahve (ha a címszó is י-vel kezdődik, mindkét feloldás); a címszó kezdőbetűje a címszó;
más betű általános jelölés (a feloldást nem találjuk ki).
"""
import importlib.util
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HEB_BETU = 'א-ת\ufb1d-\ufb4f'  # a prezentációs alakok (pl. U+FB2A) is; escape-pel, mert a korábbi „יִ” literál két karakter volt (U+05D9 U+05B4), és az osztály U+05B4–U+FB4F-et fogta (az LRM-et, a gondolatjelet is)
HEB_JEL = 'ְ-ׇ'
ROVIDITES_RE = re.compile(r'(?<![%s%s])׳([%s][%s]*)(?![%s%s])' % (HEB_BETU, HEB_JEL, HEB_BETU, HEB_JEL,
                                                                     HEB_BETU, HEB_JEL))
JAHVE_CIM = 'יְהוָה (JHVH), az Úr'
ALTALANOS = 'a BDB rövidítése; a feloldás a szócikk szövegéből derül ki'


def alapbetu(szo):
    """A szó első héber alapbetűje (a pontozás és a prezentációs alak nélkül), vagy ''."""
    return next((c for c in unicodedata.normalize('NFD', szo or '') if 'א' <= c <= 'ת'), '')


def cimszo_alak(lemma, kiejtes):
    """„lemma (kiejtés)”, vagy „lemma”, ha a kiejtés üres (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29)."""
    return '%s (%s)' % (lemma, kiejtes) if kiejtes else (lemma or '')


_HEBER_KIEJTES = None


def heber_kiejtes(lemma, atiras):
    """A jóváhagyott héber lemma-kiejtés (`adat/kiejtes_kivetelek.tsv`, a `kiejtes.py` betöltőjével; kulcs: a lemma NFC
    alakja, majd a STEP-átírás, mint a `lexikon_general.heber_lemma_kiejtes`), vagy ''. Gépi héber kiejtés nincs
    (kiejtés-szabály). Az olvasó-szerver hívja; a kiejtes.py fájlútvonalról töltődik, a `sys.path` nem változik."""
    global _HEBER_KIEJTES
    if _HEBER_KIEJTES is None:
        try:
            spec = importlib.util.spec_from_file_location(
                'bdb_rovidites_kiejtes', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kiejtes.py'))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            _HEBER_KIEJTES = m.kivetelek_betolt(nyelv='heber')
        except OSError:                 # a tábla nélkül: kiejtés nélkül (a lemma marad), nem generálunk
            _HEBER_KIEJTES = {}
    return _HEBER_KIEJTES.get(unicodedata.normalize('NFC', lemma or '')) or _HEBER_KIEJTES.get(atiras or '') or ''


def feloldas(betu, cimszo='', kezdo=''):
    """A rövidítés címe. `cimszo`: „lemma (kiejtés)”; `kezdo`: a címszó alapbetűje."""
    b = alapbetu(betu)
    if b == 'י':
        return JAHVE_CIM + ('; vagy a címszó: %s' % cimszo if kezdo == 'י' and cimszo else '')
    if b and b == kezdo and cimszo:
        return 'a címszó: %s' % cimszo
    return ALTALANOS


# A javított (helyes) alak: a geres a betű UTÁN (N-F131y, DT-F131z: a `heber_sorrend` javítás után „ק׳ בְּשֵׁם”).
ROVIDITES_UTAN_RE = re.compile(r'(?<![%s%s׳])([%s][%s]*)׳(?![%s%s])' % (HEB_BETU, HEB_JEL, HEB_BETU, HEB_JEL,
                                                                       HEB_BETU, HEB_JEL))
_EGYUTT_RE = re.compile('%s|%s' % (ROVIDITES_RE.pattern, ROVIDITES_UTAN_RE.pattern))


def jelol(szoveg, cimszo='', kezdo='', cim_esc=None, attr=''):
    """A szöveg egybetűs rövidítései: „׳י” (a forrás alakja) és „י׳” (a javított alak) →
    `<abbr class="rovidites" title="…">י׳</abbr>`.

    A jelölő csak héber betűt és geres jelet fog meg, a többi karakterhez nem nyúl: a `szoveg` lehet nyers
    (a lexikon Markdown-kimenete) vagy már escape-elt HTML-szöveg (az olvasó; címkén kívüli szövegrész).
    `cim_esc`: a cím escape-elője HTML-kimenethez (a címszó adatból jön); `attr`: további attribútumok
    (az olvasón `tabindex="0"`, hogy érintésre/fókuszra is megjelenjen a feloldás)."""
    esc = cim_esc or (lambda s: s)

    def csere(m):
        betu = m.group(1) or m.group(2)
        return '<abbr class="rovidites" title="%s"%s>%s׳</abbr>' % (esc(feloldas(betu, cimszo, kezdo)), attr, betu)
    return _EGYUTT_RE.sub(csere, szoveg or '')


# ---------------------------------------------------------------- héber sorrend (N-F131y, DT-F131z)
# A `adat/bdb_forras_javitas.tsv` `heber_sorrend` / `javitva` sorai (a Biblia által igazolt, tiszta tételek): a forrás alakja
# → a javított alak, Strongonként, betű szerint (a forrás alakja az angol szövegben és a magyar fordításban is szó szerint
# áll; újrafordítás nincs). A `valodi_sorrend` és a `jelolt_marad` sorokhoz a megjelenítés nem nyúl.
JAVITAS_UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'adat', 'bdb_forras_javitas.tsv')
_SORREND = None
_ATIRAS = None


def _strong_kulcs(strong):
    m = re.match(r'^H(\d+)(.*)$', strong or '')
    return 'H%04d%s' % (int(m.group(1)), m.group(2)) if m else (strong or '')


def _javitasok(hiba, ut=None):
    """A `hiba` osztály `javitva` sorai: Strong → [(forrás alak, javított alak)], hosszabb elöl; egy alak, amelynek a
    Strongon belül több javított alakja is van, kimarad (nem egyértelmű)."""
    tab = {}
    try:
        with open(ut or JAVITAS_UT, encoding='utf-8') as f:
            sorok = [s.rstrip('\n').split('\t') for s in f if not s.startswith('#')]
    except OSError:            # a tábla nélkül: nincs csere
        sorok = []
    fej = sorok[0] if sorok else []
    for s in sorok[1:]:
        d = dict(zip(fej, s))
        if d.get('hiba') == hiba and d.get('allapot') == 'javitva' and d.get('javitott_alak'):
            tab.setdefault(d['strong'], {}).setdefault(d['forras_alak'], set()).add(d['javitott_alak'])
    return {st: sorted(((a, next(iter(b))) for a, b in t.items() if len(b) == 1), key=lambda p: -len(p[0]))
            for st, t in tab.items()}


def sorrend_javitasok(ut=None):
    """A `heber_sorrend` / `javitva` sorok (l. `_javitasok`)."""
    global _SORREND
    if ut:
        return _javitasok('heber_sorrend', ut)
    if _SORREND is None:
        _SORREND = _javitasok('heber_sorrend')
    return _SORREND


def atiras_javitasok(ut=None):
    """Az `atiras` / `javitva` sorok (l. `_javitasok`)."""
    global _ATIRAS
    if ut:
        return _javitasok('atiras', ut)
    if _ATIRAS is None:
        _ATIRAS = _javitasok('atiras')
    return _ATIRAS


# A javított átírás magyar szövegbeli alakja (DT-F164a, felhasználó, 2026-11-03: „Seól álljon”): az angol forrásszövegben a
# helyreállított átírás marad, a magyar fordításban a tár alakja áll. Kulcs: a javítótábla `javitott_alak`-ja.
ATIRAS_MAGYAR = {'Sheʾôl': 'Seól', 'sheʾôl': 'seól', 'Qorʾân': 'Korán', 'Leḥi': 'Lehi'}
_ZAROJEL = None


def zarojel_javitasok(ut=None):
    """A `zarojel` / `javitva` kézi sorok (F123.GENKOR, l. `_javitasok`): a digitalizálásban elveszett zárójel, az angol
    forrásszöveg és a magyar fordítás alakja külön sorban."""
    global _ZAROJEL
    if ut:
        return _javitasok('zarojel', ut)
    if _ZAROJEL is None:
        _ZAROJEL = _javitasok('zarojel')
    return _ZAROJEL


def zarojel_javit(szoveg, strong, javitasok=None):
    """A Strong `zarojel` javításainak cseréje a szövegben, részszöveg szerint (az angol és a magyar alak külön sor, ezért a
    nyelvet nem kell tudni). A szöveg rövidítése (a gerinc vázlatsora) ELŐTT fut, hogy a vágás a javított szövegen történjen."""
    parok = (javitasok if javitasok is not None else zarojel_javitasok()).get(_strong_kulcs(strong))
    if not parok or not szoveg:
        return szoveg
    for regi, uj in parok:
        szoveg = szoveg.replace(regi, uj)
    return szoveg


def atiras_javit(szoveg, strong, javitasok=None, magyar=False):
    """A Strong `javitva` átírásainak cseréje a szövegben, részszöveg szerint (a torz alak az angol szövegben és a magyar
    fordításban is szó szerint áll, a fordításban toldalékkal). `magyar`: a szöveg a magyar fordítás, ott a javított alak
    magyar alakja áll (`ATIRAS_MAGYAR`): „Sh®°ôlban” → „Seólban”; angolul „Sh®°ôl” → „Sheʾôl” (B3)."""
    parok = (javitasok if javitasok is not None else atiras_javitasok()).get(_strong_kulcs(strong))
    if not parok or not szoveg:
        return szoveg
    for regi, uj in parok:
        szoveg = szoveg.replace(regi, ATIRAS_MAGYAR.get(uj, uj) if magyar else uj)
    return szoveg


def _heber_jel(c):
    return 'א' <= c <= 'ת' or '\ufb1d' <= c <= '\ufb4f' or '֑' <= c <= 'ׇ' or c in '׳״'


# ---------------------------------------------------------------- rafe-maqqéf (F105, DT-F105a)
# A forrás a maqqéf (U+05BE) helyén a két szót egybeírja, és rafét (U+05BF) tesz a szóhatár melletti betűre: hol a második
# szó első betűjére (`מִןהָֿאָרֶץ`, `יֿוֺם`: a magánhangzót gyakran a következő mater-betű hordozza), ritkán az első szó
# utolsó betűjére (`עִםֿ הַחֲמוֺר`, `בַּתֿ צִיּוֺן`). Szabály: végbetű-alak, vagy a token utolsó betűje (utána nem héber betű
# vagy geres áll) → a szóhatár utána; minden más betű → előtte (a második szó eleje). „Előtte”: maqqéf a betű elé, az előző betű végbetű-alakra (ha nem rövidítés); csak ha a szóban van
# előző betű. „Utána”: maqqéf a betű jelei után, ha ott héber betű áll, vagy a közvetlen szóköz helyére, ha utána héber
# betű jön. Ahol egyik sem áll, a rafe marad (nem találgatunk). Kivétel (`_szotag_zaro`, ELLENOR_F105 3.): pont nélküli
# rafés betű nyitott szótag után → utána (`אֶתֿכֹּל` → `אֶת־כֹּל`), ha pedig mater-betű (ו / י) követi, szón belüli rafe → marad.
# Mérés (a magánhangzó-pont szerinti változat elvetve):
# `naplok/F105_naplo.md`, `naplok/F105_maqqef_meres.py`.
RAFE = 'ֿ'
MAQQEF = '־'
_VEGBETU = dict(zip('כמנפצ', 'ךםןףץ'))


def _betu(c):
    return 'א' <= c <= 'ת'


def _jel(c):
    return '֑' <= c <= 'ׇ' and c != MAQQEF


_PONT = set('ְֱֲֳִֵֶַָׇֹֺֻ')   # magánhangzó-pontok (a sva is)


def _szotag_zaro(s, b, e):
    """A rafét hordozó (b) betű nyitott szótag után áll: neki nincs magánhangzó-pontja, az előtte álló betűnek van (a sva nem
    számít), és az nem mater-betű (ו / י: `לוֺ`, `עֲלֵי` után a következő betű a második szó eleje). Ilyenkor a betű az első
    szó szótagját zárja (`אֶתֿכֹּל` → 'utana'), kivéve ha utána mater-betű (ו / י) jön: az a szón belüli rafe (`חֲטֻבֿוֺת`,
    `מִמֵּנֿוּ`), nem maqqéf → 'marad'; a pont nélküli (néma) álef is szón belüli (`בָּאֿזִקִּים`, ELLENOR_F105) → 'marad'.
    Más esetben None (az általános szabály dönt)."""
    sajat = any(c in _PONT for c in s[b + 1:e])
    p = b - 1
    while p >= 0 and _jel(s[p]):
        p -= 1
    if p < 0 or not _betu(s[p]) or s[p] in 'וי':
        return None
    if not any(c in _PONT and c != 'ְ' for c in s[p + 1:b]):
        return None
    if sajat:
        return None
    return 'marad' if (e < len(s) and s[e] in 'וי') or s[b] == 'א' else 'utana'


def maqqef_javit(szoveg):
    """A rafe-maqqéf feloldása (l. fent); idempotens, a rafe nélküli szöveget nem változtatja."""
    if not szoveg or RAFE not in szoveg:
        return szoveg
    s = list(szoveg)
    i = 0
    while i < len(s):
        if s[i] != RAFE:
            i += 1
            continue
        b = i - 1                                   # a rafét hordozó betű
        while b >= 0 and _jel(s[b]):
            b -= 1
        if b < 0 or not _betu(s[b]):
            i += 1
            continue
        e = b + 1                                   # a betű jeleinek vége
        while e < len(s) and _jel(s[e]):
            e += 1
        kov = s[e] if e < len(s) else ''
        zaro = _szotag_zaro(s, b, e)
        if zaro == 'marad':
            i += 1
            continue
        elotte = s[b] not in 'ךםןףץ' and (_betu(kov) or kov == '׳') and zaro != 'utana'
        if elotte:
            p = b - 1                               # az előző betű (a jelei és a geres átugrásával)
            while p >= 0 and (_jel(s[p]) or s[p] == '׳'):
                p -= 1
            if p < 0 or not _betu(s[p]):
                i += 1
                continue
            rov = any(x == '׳' for x in s[p + 1:b])
            if not rov and s[p] in _VEGBETU:
                s[p] = _VEGBETU[s[p]]
            del s[i]
            s.insert(b, MAQQEF)
            i += 1
        else:
            if kov and _betu(kov):
                del s[i]
                s.insert(e - 1, MAQQEF)
            elif kov == ' ' and e + 1 < len(s) and _betu(s[e + 1]):
                del s[i]
                s[e - 1] = MAQQEF
            else:
                i += 1
    return ''.join(s)


def heber_sorrend_javit(szoveg, strong, javitasok=None):
    """A Strong `javitva` héber kifejezéseinek cseréje a szövegben (betű szerint, héber betűvel nem határos előfordulás;
    a hosszabb kifejezés elsőbbséggel, átfedés nélkül), utána a rafe-maqqéf feloldása (`maqqef_javit`, F105): a
    megjelenítés egyetlen héber szórend-lépése, az olvasó (`blokkok._rovidites`) és a lexikon-generátor is ezt hívja."""
    return maqqef_javit(_sorrend_csere(szoveg, strong, javitasok))


def _sorrend_csere(szoveg, strong, javitasok=None):
    parok = (javitasok if javitasok is not None else sorrend_javitasok()).get(_strong_kulcs(strong))
    if not parok or not szoveg:
        return szoveg
    foglalt, cserek = [], []
    for regi, uj in parok:
        i = szoveg.find(regi)
        while i >= 0:
            e = i + len(regi)
            if not (i and _heber_jel(szoveg[i - 1])) and not (e < len(szoveg) and _heber_jel(szoveg[e])) \
                    and not any(a < e and i < b for a, b in foglalt):
                foglalt.append((i, e))
                cserek.append((i, e, uj))
            i = szoveg.find(regi, i + 1)
    for i, e, uj in sorted(cserek, reverse=True):
        szoveg = szoveg[:i] + uj + szoveg[e:]
    return szoveg


# ---------------------------------------------------------------- izolálás (a jelentés 9. szakasza)
# A forrás minden héber futam után LRM-et (U+200E) tesz; a tisztítás (bont.py sima()) kiveszi. Bidi-megjelenítésben a futam
# utáni szám (igehely: „יִקְרָא 1Móz 2:19”) és a köztük álló semleges jelek a jobbról balra futamhoz tapadnak („1 יִקְרָאMóz”).
# A megjelenítés ezért a héber futam után — ha utána (semleges jelek és címkék után) szám áll — LRM-et tesz vissza.
LRM = '‎'
_IZOLAL_RE = re.compile(r'(?<=[%s%s׳״])(?=(?:[\s,;:()\[\].*_=–—-]|<[^>]*>)*\d)' % (HEB_BETU, HEB_JEL))


def izolal(szoveg):
    """LRM a héber futam után, ha utána szám következik (idempotens: a már ott álló LRM után nem tesz újat)."""
    return _IZOLAL_RE.sub(LRM, szoveg or '')
