"""szokartya_szoveg.py — a szótári szöveg (BDB, Thayer) olvasói alakja a szókártyán (F231, olvasó egyben, 2026-11-22).

A szókártya a szótár szakaszszövegét egybefüggően, az eredeti szórendben mutatja (a lexikonlap 4.2 „Mélységi szócikk”
mintájára; a felhasználó: „az md lapon jobb a szeletelő”). A szöveget nem írjuk át: csak a digitalizálás és a fordítás
jelöléseit oldjuk fel olvasói alakra, mindig ugyanazzal a szabállyal (a lista sorszámai: `naplok/OLVASO_EGYBEN_HIBALISTA.md`):

- `geresh_javit` (8.): a héber rövidítőjel (׳) a digitalizálásban a rövidített szó elé került („׳הַבּ” → „הַבּ׳”, „א ׳אדני”
  → „א׳ אדני”); a jel a helyére kerül, a szavak sorrendje nem változik;
- `parhuzam` (5.): a BDB „||” / „‖” jele: igehely előtt „párhuzamos hely:”, héber szó előtt „párhuzamban:”;
- `szemben` (5.): a „szemben X-val” fordulat (héber szóra ragasztott magyar rag) → „ellentétben: X”;
- `nemi_tanu` (6.): a „főnév^1Móz 10:13” típusú tanú-jel (a szófaj után álló igehely) → szóköz;
- `takarit_hu` (3.): a magyar szövegben maradt „&” → „és”; az igehely után álló „+” (a BDB „és máshol” jele) → „és máshol”;
- `tudosjel_html` (6.): a kész HTML szövegrészeiben a `Szerző^Mű`, `Ézs^2`, `ᵐ5^L` felső indexe `<sup>`-ként (a BDB
  nyomtatott alakja), a nyers „^” nem marad.

A feliratok (a „párhuzamos hely”, „ellentétben” stb.) a fordítótáblából jönnek (DT897, `feliratok.py`).
Csak standard könyvtár és a közös `bdb_rovidites`; SQL nincs benne.
"""
import re
import sys

from feliratok import F

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BETU = 'א-תיִ-ﭏ'           # héber alapbetű (a prezentációs alakok is)
JEL = '֑-ֽֿׁׂׄ-ׇ'   # pontozás és kantilláció (a maqqef U+05BE és a geres nélkül)
GERES = '׳'
RAFE = 'ֿ'
MAQQEF = '־'
TOKEN = '[%s][%s%s]*' % (BETU, BETU, JEL)
_TOKEN_RE = re.compile(TOKEN)


def _betuszam(t):
    return len(re.findall('[%s]' % BETU, t))


# --- 8. a héber rövidítőjel helye ---------------------------------------------------------------------------------------
# R0: „עַדבּֿ ׳בָּעֶרֶב” — a rafe a maqqef helyén áll a rövidített betű után, a geres a következő szó elé került: „עַד־בּ׳ בָּעֶרֶב”
_R0 = re.compile('(%s)([%s][%s]*)%s(\\s+)%s(?=[%s])' % ('[%s][%s%s]*?' % (BETU, BETU, JEL), BETU, JEL.replace(RAFE, ''), RAFE,
                                                         GERES, BETU))
# R1: magában álló rövid (1–2 betűs) szó, utána szóköz (vessző) és a következő szó elején a geres: a geres a rövid szóé
_R1 = re.compile('(?<![%s%s%s])((?:[%s][%s]*){1,2})(\\s*,?\\s+)%s(?=[%s])' % (BETU, JEL, GERES, BETU, JEL, GERES, BETU))
# R2: a szó elején álló geres egy legfeljebb háromjegyű szón: a szó végére („׳הַבּ” → „הַבּ׳”)
_R2 = re.compile('(?<![%s%s%s])%s((?:[%s][%s]*){1,3})(?![%s%s%s])' % (BETU, JEL, GERES, GERES, BETU, JEL, BETU, JEL, GERES))
# R3: hosszú szó elején álló geres egy héber futamban, amelyben magában álló egybetűs szó van geres nélkül: a geres azé
_FUTAM = re.compile('%s?%s%s?(?:[ %s]+%s?%s%s?)+' % (GERES, TOKEN, GERES, MAQQEF, GERES, TOKEN, GERES))


def _r3(m):
    s = m.group(0)
    reszek = re.split('([ %s]+)' % MAQQEF, s)
    szavak = reszek[0::2]
    for i, w in enumerate(szavak):
        if not (w.startswith(GERES) and _betuszam(w) >= 4):
            continue
        jeloltek = [j for j, v in enumerate(szavak) if _betuszam(v) == 1 and GERES not in v and _TOKEN_RE.fullmatch(v)]
        if not jeloltek:
            continue
        j = min(jeloltek, key=lambda x: (abs(x - i), x > i))     # a legközelebbi, egyenlő távolságnál a megelőző
        szavak[i] = w[1:]
        szavak[j] = szavak[j] + GERES
    reszek[0::2] = szavak
    return ''.join(reszek)


def geresh_javit(s):
    """A rövidítőjel a helyén (R0–R3); a szavak és a betűk sorrendje nem változik. Idempotens."""
    if not s or GERES not in s:
        return s
    s = _R0.sub(lambda m: m.group(1) + MAQQEF + m.group(2) + GERES + m.group(3), s)
    s = _R1.sub(lambda m: m.group(1) + GERES + m.group(2), s)
    s = _R2.sub(lambda m: m.group(1) + GERES, s)
    return _FUTAM.sub(_r3, s)


# --- 5. párhuzam és ellentét --------------------------------------------------------------------------------------------
_KONYV = r'(?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\.?\s+\d+:\d+'
_PARHUZAM_RE = re.compile(r'(?:\|\||‖)\s*(?=(%s)|(\d+:\d+)|([%s%s(]))?' % (_KONYV, BETU, GERES))


def parhuzam(s):
    """„||” / „‖” → „párhuzamos hely:” igehely előtt, „párhuzamban:” héber szó előtt; egyéb helyzetben „párhuzamban:”."""
    if not s or ('||' not in s and '‖' not in s):
        return s

    def csere(m):
        kulcs = 'szk.parhuzamos_hely' if (m.group(1) or m.group(2)) else 'szk.parhuzamban'
        return F(kulcs) + ' '
    return _PARHUZAM_RE.sub(csere, s)


_SZEMBEN_RE = re.compile(r'szemben\s+(%s?[%s][%s%s%s\s]*?)-?[vV]?[ae]l\b' % (GERES, BETU, BETU, JEL, GERES + MAQQEF))
_SZEMBEN_RAG_NELKUL_RE = re.compile(r'(?<!\w)szemben\s+(?=%s?[%s])' % (GERES, BETU))


def szemben(s):
    """„szemben X-val/-vel” (X héber) → „ellentétben: X” (a héber szón magyar rag nélkül)."""
    if not s or 'szemben' not in s:
        return s
    s = _SZEMBEN_RE.sub(lambda m: F('szk.ellentetben', szo=m.group(1).strip()), s)
    # F231 (#5): rag nélkül is („(szemben הַיּוֺם ma)”, H1242 2.); csak közvetlenül héber szó előtt (a magyar „vele szemben” marad)
    return _SZEMBEN_RAG_NELKUL_RE.sub(lambda m: F('szk.ellentetben', szo='').rstrip() + ' ', s) if 'szemben' in s else s


# --- 6. tanú-jel, tudósjel ----------------------------------------------------------------------------------------------
# a könyvnév betűje bármely (akár felbontott, kombináló ékezetes) betű lehet
_NEMI_RE = re.compile(r'(?<=\S)\s?\^(?=(?:[1-5]\s?)?[^\W\d_][^\W\d_]{0,7}\.?\s+\d+:\d+)')     # a jel előtt szóköz is állhat


def nemi_tanu(s):
    """A szófaj (nem) tanújának jele: „főnév^1Móz 10:13” → „főnév 1Móz 10:13” (az igehely kattintható marad)."""
    return _NEMI_RE.sub(' ', s) if s and '^' in s else s


_PLUSZ_RE = re.compile(r'(?<=\d)\s*\+(?:\s*stb\.)?(?=\s*[,;.)]|\s*$)')


def takarit_hu(s):
    """A magyar szövegben: „&” → „és”; az igehely utáni magában álló „+” (a BDB „és máshol” jele) → „és máshol”."""
    if not s:
        return s
    s = re.sub(r'\s*&(?:amp;)?\s*', ' %s ' % F('szk.es'), s)
    return _PLUSZ_RE.sub(' ' + F('szk.es_mashol'), s)


# a kész HTML szövegrészében: a „^” utáni felső index (a BDB nyomtatott alakja); a jel előtt nem-szóköz (vagy záró címke) áll
_CIMKE_RE = re.compile(r'(<[^>]*>)')
_FELSO_RE = re.compile(r'\^\s?([^\s<^;,()\[\]]+)')


def tudosjel_html(html):
    """A címkén kívüli szövegrészekben „X^Y” → „X<sup>Y</sup>”. A szöveg már escape-elt: a csere nem visz be
    nyers adatot címkébe (a felső index tartalma a szövegrész maga)."""
    ki = []
    for i, r in enumerate(_CIMKE_RE.split(str(html))):
        ki.append(r if i % 2 or '^' not in r else _FELSO_RE.sub(r'<sup>\1</sup>', r))
    return ''.join(ki)


# --- 11. a tagolási jelző és a meghatározás nélküli pont címe ------------------------------------------------------------
_HEBER_RE = re.compile('[%s%s%s%s]+' % (BETU, JEL, GERES, MAQQEF))
_PARADIGMA_RE = re.compile(
    r'^(?:perfectum|imperfectum|participium|infinitivus|imperativus|jussivus|cohortativus|consecutiv\w*|(?:\d\.?\s*)?(?:hímnemű\s+|nőnemű\s+|közös\s+)?(?:egyes|többes|kettes)\s+szám|'
    r'\d\.?\s+(?:hímnemű|nőnemű|közös)|perfect|imperfect|participle|infinitive|imperative|jussive|cohortative|'
    r'\d\s+(?:masculine|feminine|common|singular|plural))\b', re.I)


def paradigma(s):
    """A pont szövege alaktani felsorolással nyílik (a héber alakok nélkül: „perfectum כ׳ 1Kir 6:38”, „3. nőnemű egyes szám”):
    ilyenkor a pont nem jelentés, hanem a ragozás egy sora (a tagolási jelző rossz tagolást mutat). A „status constructus” és a
    „suffixummal” nem jelző: a BDB névszóknál jelentéspontot nyit vele (H0430 4.b „status constructus … személyekkel”)."""
    t = _HEBER_RE.sub(' ', s or '')
    t = re.sub(r'^[\s,;:.‎‏()\-—–]+', '', t)
    return bool(_PARADIGMA_RE.match(t))


def elso_tagmondat(s, hatar=70):
    """A meghatározás nélküli pont címe: a szöveg első tagmondata (az első „;” vagy „:” előtt), szóhatáron rövidítve „…” jellel."""
    t = _HEBER_RE.sub(' ', s or '')
    t = re.sub(r'(?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\.?\s+\d+(?::\d+)?(?:[-–]\d+)?', ' ', t)    # igehely
    t = re.sub(r'\s+', ' ', t).strip(' ,.=‎‏()')
    t = re.split(r'[;:]|\s—\s', t, maxsplit=1)[0].strip(' ,.=()')
    if len(t) > hatar:
        t = t[:hatar].rsplit(' ', 1)[0].rstrip(' ,;') + '…'
    return t


def olvasoi(s, magyar=True, elotte=None):
    """A szakaszszöveg olvasói alakja (a linkelés és az escape előtt): rövidítőjel, párhuzam, ellentét, tanú-jel, takarítás.
    `elotte`: a Biblia által igazolt héber javítás (`bdb_rovidites.heber_sorrend_javit` a Strongra kötve), amely a forrás alakját
    keresi, ezért a rövidítőjel áthelyezése ELŐTT kell lefutnia (különben a „׳א אברהם אדני” forrásalak nem ismerhető fel)."""
    s = elotte(s or '') if elotte else (s or '')
    s = re.sub(r'^\s*_\d+\s*', '', s)    # a pont elején álló BDB-gyakoriság („_140”): a törzs fejében már áll
    s = geresh_javit(s)
    s = nemi_tanu(s)
    if magyar:
        s = parhuzam(s)
        s = szemben(s)
        s = takarit_hu(s)
    return s
