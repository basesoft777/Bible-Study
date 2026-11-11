"""szotari_glossza.py — a szótári szakasz olvasói meghatározása (glossza), közös szabály (F187, egy szabály, egy hely).

A lexikonlap 4.2-es kétrétegű kártyája (`lexikon_general.bdb_olvasoi_reteg`, `gerinc_szakasz_lista`) és az olvasó-szerver
szó-lapjának Thayer-része (`olvaso_szerver/blokkok.py`, `_r_magyar_gorog`) ugyanezt használja:

- `olvasoi_glossza`: a jóváhagyott címke (`adat/szotar_szakasz_cimke.tsv`), ennek híján a magyar szöveg első tagmondata;
- `thayer_glossza`: ugyanez a görög szó előtt elvágva; `thayer_fej_glossza`: a Thayer-fej meghatározása;
- `thayer_csak_alak`: a meghatározás nélküli Thayer-szakasz kimondott ténye.

Csak standard könyvtár; a lexikon_general.py innen importálja (a nevei ott is elérhetők).
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def _torzs_norm(s):
    return re.sub(r"[\s'`’ʼ]", '', s or '').lower()


def vegyes_cim_nelkul(jel, szoveg):
    """„Hithpa'el — Hithpael — perfectum …”: a szöveg elején a jel törzsnevének másik írásmódja elmarad (egy alak)."""
    torzs = (jel or '').split(' ')[0]
    if not torzs or not torzs[0].isalpha() or len(torzs) < 3:
        return szoveg or ''
    m = re.match(r'\s*([^\s—–,;:]+)[\s—–,;:]*', szoveg or '')
    if m and _torzs_norm(re.sub(r'_\d+$', '', m.group(1))) == _torzs_norm(torzs):
        return (szoveg or '')[m.end():]
    return szoveg or ''


_GLOSSZA_VAG = re.compile(r'[(\[;:=^]|\s[—–]\s|(?:(?<![\w])[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\s+)?\d+:\d+|[֐-׿יִ-ﭏ]|\s(?:l\.|vö\.|ld\.|stb\.)(?:\s|$)|\s(?:J|E|P|D)\b')


def olvasoi_glossza(jel, cimke, szoveg):
    """A jelentés rövid magyar meghatározása az olvasói réteghez: a jóváhagyott címke, ennek híján a magyar szöveg
    első tagmondata az első zárójel, igehely, héber szó, rövidítés vagy hivatkozó szó előtt; None, ha nem marad szó."""
    if cimke:
        return vegyes_cim_nelkul(jel, cimke).strip(' ,;—–-') or None
    s = vegyes_cim_nelkul(jel, jelolo_levag(szoveg or '', jel))
    s = re.sub(r'_\d+', '', re.sub(r'^\s*(?:(?:\d+|[a-z])\.\s*)+', '', s)).lstrip(' =—–-')
    s = _glossza_elotag_nelkul(s)
    m = _GLOSSZA_VAG.search(s)
    if m:
        s = s[:m.start()]
    s = re.sub(r'\s+', ' ', s).strip(' ,.;—–-')
    s = re.sub(r'(?:\s+(?:a|az|és|vagy|mint|egy|is|de|mind|mindkettő))+$', '', s).rstrip(' ,;—–-')
    if len(s) > 70:
        s = s[:70].rsplit(' ', 1)[0].rstrip(' ,;') + '…'
    # az alakjegyzékkel nyíló szakasz („perfectum …”, „participium …”) első szava nyelvtani alak, nem jelentés
    if _ALAKTANI_KEZDET.match(s):
        return None
    return s if re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}', s) else None


# F182 (N139, F29/F34): a szakasz elején álló, meghatározás előtti elem (a forrás-besorolás, a „+ <héber> <nyelvtani>:”
# szerkezet, a héber kifejezés) nem a glossza; utána áll a meghatározás. Csak az elejéről vág; ha utána nem marad szó, a
# szöveg változatlan.
_FORRAS_ELOTAG = re.compile(r'^\s*(?:a|az)\s+(?:[JEPDHR]|JE)(?:\s*\((?:[JEPDHR]|JE)\))?\s+szerint\s+')
_PLUSZ_ELOTAG = re.compile(r'^\s*\+\s*[֐-׿יִ-ﭏ][^:]{0,40}:\s*')
_HEBER_ELOTAG = re.compile(r'^\s*(?:[֐-׿יִ-ﭏ()\u200e\u200f־]+\s*)+')


def _glossza_elotag_nelkul(s):
    for rx in (_FORRAS_ELOTAG, _PLUSZ_ELOTAG):
        m = rx.match(s)
        if m and re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}', s[m.end():]):
            return s[m.end():]
    m = _HEBER_ELOTAG.match(s)
    if m and re.search('[֐-׿יִ-ﭏ]', m.group(0)) and re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}', s[m.end():]):
        # a héber kifejezés utáni magyar meghatározás; a benne álló zárójeles magyarázat elmarad („gonosz (ártalmas) tervet”)
        return re.sub(r'\s*\([^()]*\)', '', s[m.end():], count=1)
    return s


_ALAKTANI_KEZDET = re.compile(r'(?i)(?:perfectum|imperfectum|participium|infinitivus|imperativus|status|suffixum|többes '
                              r'szám|egyes szám|hímnemű|nőnemű|jussivus|cohortativus)\b')


def jelolo_levag(szoveg, jel):
    """A szótári szöveg elejéről a saját tagolási jelét (`3`, `2. a.`, `c.`) levágja, ha az a címke
    `jel`-ének része: a kibontott szakaszon a jel a címkében már áll, az idézetben nem ismétlődik.
    A betűjelet csak ponttal vágja (a névelő `a` így nem jel); más kezdet változatlan marad."""
    jelek = set(t for t in re.split(r'[.\s]+', jel or '') if re.fullmatch(r'\d+|[a-z]', t))
    s = szoveg or ''
    while True:
        m = re.match(r'\s*(\d+)\.?\s+|\s*([a-z])\.\s+', s)
        if not m or (m.group(1) or m.group(2)) not in jelek or not s[m.end():].strip():
            return s
        s = s[m.end():]


_GOROG_BETU_RX = re.compile('[Ͱ-Ͽἀ-῿]')
_KLASSZIKUS = re.compile(r'(?i)\b(?:Plat[óo]n|Xenoph[óo]n|Arisztotel[ée]sz|Aristotle|Aeschylus|Aiszkh[üu]losz|Euripid[ée]sz?|'
                         r'H[ée]rodotosz|Herodotus|Hom[ée]rosz|Plutarkhosz|Plutarch|Pol[üy]bi(?:osz|us)|Josephus|Phil[óo]n?|'
                         r'Thuk[üy]did[ée]sz|Thucydides|Diodorus|Lukianosz|Lucian|Szophokl[ée]sz|Sophocles|Pindarosz|'
                         r'D[ée]mosthen[ée]sz|Isokrat[ée]sz|Aelian|Dionysius|mások)\b')


def _zarojel_nelkul(s):
    """A (beágyazott) zárójeles részek elhagyása."""
    ki, mely = [], 0
    for c in s or '':
        if c == '(':
            mely += 1
        elif c == ')':
            mely = max(0, mely - 1)
        elif not mely:
            ki.append(c)
    return ''.join(ki)


_THAYER_META = re.compile(r'(?i)Septuaginta|használ|\bidő\b|aoriszt|alakban|szenvedő|melléknévi igenév|rokon|óta\b|kezdve|'
                          r'írásokban|\bvö\.|\bl\.\s|nőnemű|hímnemű|semlegesnemű|főnév|ige\b|^\s*csak\b')


def thayer_fej_glossza(hu):
    """A Thayer-szócikk fejének magyar meghatározása: a zárójelek nélküli szöveg „:” és „;” határolta első olyan része, amelyben
    nincs görög vagy héber betű, igehely és nyelvtani/forrásmegjegyzés („átkozott, utálatos, … Isten átka alatt álló”). None,
    ha a fej csak alakot és forrást közöl."""
    for resz in re.split(r'[:;]', _zarojel_nelkul(hu)):
        r = resz.strip(' ,.—–-')
        if (not r or _GOROG_BETU_RX.search(r) or re.search('[֐-׿]', r) or re.search(r'\d+:\d+|\d', r)
                or _THAYER_META.search(r) or _KLASSZIKUS.search(r)):
            continue
        g = olvasoi_glossza('', '', r)
        if g:
            return g
    return None


def thayer_glossza(jel, cimke, hu):
    """A Thayer-szakasz olvasói meghatározása: a jóváhagyott címke, ennek híján a magyar szöveg első tagmondata (mint a
    BDB-nél), a görög szó előtt elvágva."""
    g = olvasoi_glossza(jel, cimke, hu)
    if g and not cimke:
        m = _GOROG_BETU_RX.search(g)
        if m:
            g = g[:m.start()].strip(' ,;:—–-') or None
            g = re.sub(r'(?:\s+(?:a|az|és|vagy|mint|egy|is|de))+$', '', g) if g else None
    return g if g and re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}', g) else None


def thayer_csak_alak(hu):
    """A meghatározás nélküli Thayer-szakasz kimondott ténye (F187, T5): párhuzamot vagy alakot közöl."""
    return 'a szótár csak párhuzamot közöl' if _KLASSZIKUS.search(hu or '') else 'a szótár csak alakot közöl'
