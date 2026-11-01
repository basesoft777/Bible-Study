"""bdb_rovidites.py — a BDB-szöveg egybetűs rövidítéseinek jelölése (N-F131x).

A lexikon-generátor (`lexikon_general.bdb_rovidites_jelol`) és az olvasó-szerver szó-lapja
(`olvaso_szerver/blokkok.py`) ugyanezt a függvényt hívja.

A felhasználó kérése (2026-10-29): „nem lehetne jelölni a szövegben /pl más szinű háttér , hogy a
szó rövidités?”, majd: „ezt a felismerést rakljuk el az olvasó felület számára is”.

A forrás (DictBDB.json) a rövidítő jelet (geres, ׳) a betű ELÉ írja (׳י); a helyes alak a betű utáni
(י׳). A `jelol` az önálló, egybetűs alakot jelöli (<abbr>, címmel), a forrás és a javított alakban is.

A megjelenítés sorrendje (DT-F131y; a lexikon-generátor és az olvasó ugyanígy): `heber_sorrend_javit` (a több
szavas kifejezések Biblia által igazolt sorrend-javítása, `adat/bdb_forras_javitas.tsv` `heber_sorrend` /
`javitva`) → `izolal` (LRM a héber futam után, ha szám következik) → `jelol`.

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
JAHVE_CIM = 'יְהוָה (Jahve), az Úr'
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


# A javított (helyes) alak: a geres a betű UTÁN (N-F131y, DT-F131y: a `heber_sorrend` javítás után „ק׳ בְּשֵׁם”).
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


# ---------------------------------------------------------------- héber sorrend (N-F131y, DT-F131y)
# A `adat/bdb_forras_javitas.tsv` `heber_sorrend` / `javitva` sorai (a Biblia által igazolt, tiszta tételek): a forrás alakja
# → a javított alak, Strongonként, betű szerint (a forrás alakja az angol szövegben és a magyar fordításban is szó szerint
# áll; újrafordítás nincs). A `valodi_sorrend` és a `jelolt_marad` sorokhoz a megjelenítés nem nyúl.
JAVITAS_UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'adat', 'bdb_forras_javitas.tsv')
_SORREND = None


def _strong_kulcs(strong):
    m = re.match(r'^H(\d+)(.*)$', strong or '')
    return 'H%04d%s' % (int(m.group(1)), m.group(2)) if m else (strong or '')


def sorrend_javitasok(ut=None):
    """Strong → [(forrás alak, javított alak)], hosszabb elöl; egy alak, amelynek a Strongon belül több javított alakja is
    van, kimarad (nem egyértelmű)."""
    global _SORREND
    if _SORREND is None or ut:
        tab = {}
        try:
            with open(ut or JAVITAS_UT, encoding='utf-8') as f:
                sorok = [s.rstrip('\n').split('\t') for s in f if not s.startswith('#')]
        except OSError:            # a tábla nélkül: nincs csere
            sorok = []
        fej = sorok[0] if sorok else []
        for s in sorok[1:]:
            d = dict(zip(fej, s))
            if d.get('hiba') == 'heber_sorrend' and d.get('allapot') == 'javitva' and d.get('javitott_alak'):
                tab.setdefault(d['strong'], {}).setdefault(d['forras_alak'], set()).add(d['javitott_alak'])
        ki = {st: sorted(((a, next(iter(b))) for a, b in t.items() if len(b) == 1), key=lambda p: -len(p[0]))
              for st, t in tab.items()}
        if ut:
            return ki
        _SORREND = ki
    return _SORREND


def _heber_jel(c):
    return 'א' <= c <= 'ת' or '\ufb1d' <= c <= '\ufb4f' or '֑' <= c <= 'ׇ' or c in '׳״'


def heber_sorrend_javit(szoveg, strong, javitasok=None):
    """A Strong `javitva` héber kifejezéseinek cseréje a szövegben (betű szerint, héber betűvel nem határos előfordulás;
    a hosszabb kifejezés elsőbbséggel, átfedés nélkül)."""
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
