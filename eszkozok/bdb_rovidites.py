"""bdb_rovidites.py — a BDB-szöveg egybetűs rövidítéseinek jelölése (N-F131x).

A lexikon-generátor (`lexikon_general.bdb_rovidites_jelol`) és az olvasó-szerver szó-lapja
(`olvaso_szerver/blokkok.py`) ugyanezt a függvényt hívja.

A felhasználó kérése (2026-10-29): „nem lehetne jelölni a szövegben /pl más szinű háttér , hogy a
szó rövidités?”, majd: „ezt a felismerést rakljuk el az olvasó felület számára is”.

A forrás (DictBDB.json) a rövidítő jelet (geres, ׳) a betű ELÉ írja (׳י); a helyes alak a betű utáni
(י׳). Csak az önálló, egybetűs alakot javítja és jelöli (<abbr>, címmel); a több szavas, felcserélt
sorrendű héber kifejezésekhez nem nyúl (forrás-konverziós hiba, külön tétel).

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

HEB_BETU = 'א-תיִ-ﭏ'  # a prezentációs alakok (pl. U+FB2A שׁ) is
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


def jelol(szoveg, cimszo='', kezdo='', cim_esc=None, attr=''):
    """A szöveg egybetűs rövidítései: „׳י” → `<abbr class="rovidites" title="…">י׳</abbr>`.

    A jelölő csak héber betűt és geres jelet fog meg, a többi karakterhez nem nyúl: a `szoveg` lehet nyers
    (a lexikon Markdown-kimenete) vagy már escape-elt HTML-szöveg (az olvasó; címkén kívüli szövegrész).
    `cim_esc`: a cím escape-elője HTML-kimenethez (a címszó adatból jön); `attr`: további attribútumok
    (az olvasón `tabindex="0"`, hogy érintésre/fókuszra is megjelenjen a feloldás)."""
    esc = cim_esc or (lambda s: s)
    return ROVIDITES_RE.sub(
        lambda m: '<abbr class="rovidites" title="%s"%s>%s׳</abbr>' % (esc(feloldas(m.group(1), cimszo, kezdo)), attr,
                                                                       m.group(1)), szoveg or '')
