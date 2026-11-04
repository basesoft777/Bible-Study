#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
olvasoi_utofeldolg.py -- a generált lexikonlap olvasói szövegének utófeldolgozása (olvasói kapu, 2026-11-02).

A lap szövege sok forrásból áll össze (kézi rések, adattáblák szövege, szótári fordítások), és mindegyik a maga
írásmódját hozza. A generátor a kész lapon egyszer, determinisztikusan egységesíti az olvasói szöveget; az adat és a
kézi forrás nem változik (DT28), a javítás a kimenet rétegben él, ezért minden újragenerálásnál ugyanaz.

    idezojel   egyenes " -> „…” a magyar szövegben (a kód, a HTML, a hivatkozás-cél és a proveniencia érintetlen)
    konyv      a könyvrövidítés a `konkordancia/Konyv_normalizalo_tabla.tsv` magyar alakjára; a szó szerint idézett,
               angol nyelvű sor (a szótár eredetije) nem változik
    bdb        a BDB-átalakítás maradék jelei: a felső index ^ jele, a dupla vessző, a héber rafe (lásd BDB_CSERE)
    strong     a Strong-szám ott, ahol mellette a héber/görög szó (és a kiejtése) áll, jelölt alakra: a kiejtés hivatkozás a
               szónézetre, a szám halvány felső index (F123.INDOKLAS → F123.GENKOR, DT-F181b; lásd strong_ki);
               a táblázat „Strong” oszlopa, a címsor és az egyedül vagy láncban álló Strong-szám érintetlen; csak a
               generált részen (a kézi részt, mint a kiejtés-szabály, a forrásban kell javítani; DT569)

Az olvasói szöveg határa megegyezik az olvasói kapuéval (`olvasoi_kapu.py`): nem olvasói a HTML-megjegyzés, a kódblokk,
az idézetblokk (`>`, a szótár angol eredetije), a proveniencia-lábjegyzet, valamint a Tartalomjegyzék, a Jelmagyarázat és
a Kolofon szakasz.

TSV-olvasás: split('\\t'), csv modul nélkül (CLAUDE.md).
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NORMALIZALO = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

KIZART_SZAKASZ = ('Tartalomjegyzék', 'Jelmagyarázat', 'Kolofon')

# a sorban védett szakaszok: ezeket a cserék nem látják
VEDETT = re.compile(r'<!--.*?-->|<sup class="strong"[^>]*>[^<]*</sup>|<[^>]+>|`[^`]*`|\]\([^)]*\)|https?://\S+|(?:\\?\|\s*)?scope=.*?ts=[\dT:Z.-]+')

# --- könyvrövidítés ---------------------------------------------------------------------------------------------------
# A normalizáló tábla STEPBible- és forrás-alakjain túl a lapokon mért változatok. A kulcs szóköz nélküli.
EXTRA_KONYV = {
    'Zef': 'Sof', 'Csel': 'ApCsel', 'Ésa': 'Ézs', 'Ezék': 'Ez', 'Mát': 'Mt', 'Máté': 'Mt', 'Matt': 'Mt', 'Márk': 'Mk',
    'Mark': 'Mk', 'Lk': 'Luk', 'Luke': 'Luk', 'Lukács': 'Luk', 'John': 'Ján', 'Jn': 'Ján', '1Jn': '1Ján',
    '2Jn': '2Ján', '3Jn': '3Ján', '1John': '1Ján', 'Ám': 'Ámós', 'Agge': 'Hag', 'Róma': 'Róm', 'Acts': 'ApCsel',
    '1Cor': '1Kor', '2Cor': '2Kor', 'Rom': 'Róm', 'Heb': 'Zsid', '1Pet': '1Pét', '2Pet': '2Pét', '1Thess': '1Thessz',
    '2Thess': '2Thessz', 'Bir': 'Bír', 'Genezis': '1Móz', '1Mózes': '1Móz', 'Jas': 'Jak', 'Eph': 'Ef', 'Col': 'Kol',
    'Rev': 'Jel', 'Jude': 'Júd', 'Mk': 'Mk',
}
KONYV_RX = re.compile(r'(?<![\w./#-])((?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6})(\s)(\d{1,3}[:,]\d{1,3})')
SZOTAR_ALAK = re.compile(r'(?:BDB|Thayer|szótár)-?(?:ben|ban)?:\s*„$')
ANGOL_FUNKCIO = re.compile(r'\b(the|and|of|with|which|from|that|this|are|was|were|by|to|in|for|not|or|as|an|it|its|'
                           r'his|her|their|who|whom|into|upon|unto)\b')

_KONYV_ALIAS = None


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    return [s.split('\t') + [''] * 4 for s in sorok[1:]]


def konyv_alias():
    """{nem magyar alak: magyar rövidítés} és a magyar rövidítések halmaza."""
    global _KONYV_ALIAS
    if _KONYV_ALIAS is None:
        sorok = tsv(NORMALIZALO)
        hu = {s[1] for s in sorok}
        alias = {}
        for s in sorok:
            for a in [s[0]] + [x.strip() for x in s[3].split(',') if x.strip()]:
                alias[a.replace(' ', '')] = s[1]
        alias.update(EXTRA_KONYV)
        for h in hu:      # a magyar alak soha nem cserélődik
            alias.pop(h, None)
        _KONYV_ALIAS = (alias, hu)
    return _KONYV_ALIAS


# --- BDB ---------------------------------------------------------------------------------------------------------------
# A BDB digitális szövegének (DictBDB.json) átalakításából maradt jelek. Eredet: a `konkordancia/_convert_bdb.py` a
# <sup>…</sup> felső indexet `^…`-ra írta (Ges<sup>§ 48d</sup> -> Ges^§ 48d), az OCR a ", " helyére ",,"-t is tett; a
# rafe (U+05BF) a nyomtatott héber pontozás jele, olvasásnál zaj. A nyers forrás és a konverzió nem változik; a
# megjelenítés olvasható alakot ad. NEM javítja a „She®°ôl”-féle torz átírást: ott a helyes alak csak találgatható
# (a hiány nem tölthető ki asszociatív anyaggal), ezért az a kapun maradék.
BDB_CSERE = [
    (re.compile('ֿ'), ''),                          # rafe
    (re.compile(r'(?<=[^\s,]),,'), ','),            # dupla vessző (OCR)
    (re.compile(r' ?(?<!\[)\^ ?'), ' '),             # a felső index jele; a lábjegyzet-jel [^k1] érintetlen
]


def _vedett(sor):
    tarolo = []

    def el(m):
        tarolo.append(m.group(0))
        return '\x00%d\x00' % (len(tarolo) - 1)
    return VEDETT.sub(el, sor), tarolo


def _vissza(sor, tarolo):
    return re.sub(r'\x00(\d+)\x00', lambda m: tarolo[int(m.group(1))], sor)


def idezojel_sor(sor):
    """Az egyenes " cseréje „…”-ra egy sorban. Nyitó, ha a sor elején, szóköz, nyitó zárójel vagy gondolatjel után áll,
    és nem szóköz követi; egyébként záró."""
    v, tarolo = _vedett(sor)
    if '"' not in v:
        return sor
    ki = []
    for i, c in enumerate(v):
        if c != '"':
            ki.append(c)
            continue
        elozo = v[i - 1] if i else ' '
        kovetkezo = v[i + 1] if i + 1 < len(v) else ' '
        nyito = (elozo.isspace() or elozo in '([{—–/|*_„\x00' and not elozo.isalnum()) and not kovetkezo.isspace()
        if elozo == '\x00':     # védett szakasz (kód, hivatkozás) után: a következő karakter dönt
            nyito = not kovetkezo.isspace() and kovetkezo not in '.,;:)]!?'
        ki.append('„' if nyito else '”')
    return _vissza(''.join(ki), tarolo)


def konyv_sor(sor):
    alias, hu = konyv_alias()
    v, tarolo = _vedett(sor)
    if len(ANGOL_FUNKCIO.findall(v)) >= 3:
        return sor      # szó szerint idézett angol szöveg (a szótár eredetije): nem a lap fordítása

    def csere(m):
        nev = m.group(1)
        if nev in hu or SZOTAR_ALAK.search(v[max(0, m.start() - 20):m.start()]):
            return m.group(0)
        uj = alias.get(nev.replace(' ', ''))
        return (uj + m.group(2) + m.group(3)) if uj else m.group(0)
    return _vissza(KONYV_RX.sub(csere, v), tarolo)


def bdb_sor(sor):
    v, tarolo = _vedett(sor)
    for rx, ki in BDB_CSERE:
        v = rx.sub(ki, v)
    return _vissza(v, tarolo)


# --- Strong-szám a szó és a kiejtése mellett (F123.INDOKLAS → F123.GENKOR, DT-F181b) -------------------------------
# A lap olvasói szövegében a csupasz Strong-szám belső azonosító; ahol mellette ott a héber/görög szó (és a kiejtése), a
# generátor jelölt alakra írja: a kiejtés (ennek híján a szó) a szónézetre mutató hivatkozás, a Strong-szám kis, halvány
# felső index, egér alatt a szám és a rövid jelentés (`STRONG_JEL`): „(מִזְבֵּחַ, mizbéah, H4196)” →
# „(מִזְבֵּחַ, [mizbéah](/szo/H4196)<sup class="strong" title="H4196 · oltár">H4196</sup>)”; „(ἐπικαλέω, epikaleó G1941)” →
# „(ἐπικαλέω, [epikaleó](/szo/G1941)<sup …>G1941</sup>)”; „ὄνομα (G3686)” és „H6089 עֶצֶב” → a szó a hivatkozás. A forrásban a
# „(szó, kiejtés, H4196)” alak a generátor bemenete (a kézi résen is: csak a jelölés változik, a szöveg nem). Ahol a Strong-szám
# egyedül áll (a szó nincs mellette, pl. „a H7496/H7497 Strong-szám szerinti megoszlás”, „a kárá (H7121)”), vagy lánc tagja
# („H7121+H8034”, „H0369 + H7121”), az adat része, nem változik. A táblázat „Strong” fejlécű oszlopa és a címsor érintetlen.
# A jelölt alak védett (VEDETT), ezért a művelet idempotens. Az olvasói kapu BELSO-ellenőrzése ugyanezt a függvényt hívja
# (`strong_valtozas`): amit a kapu megfog (a csupasz alak), azt a generátor jelöltre írja; a jelölt alak nem hiba.
SCRIPT = '[֐-׿Ͱ-Ͽἀ-῿]'
_STRONG = r'[HG]\d{4}[a-z]?'
STRONG_TAG = re.compile(r'(?<![\w+/])(?<![+/]\s)' + _STRONG + r'(?![\w+/])(?!\s[+/])')
STRONG_ELEM = re.compile(r'\s*' + _STRONG + r'\s*')
STRONG_UTAN = re.compile(r'^(?P<szo>[^\d,;()]*\S)\s+(?P<strong>' + _STRONG + r')\s*$')   # „epikaleó G1941”
SZKRIPT_SZO = '(?:' + SCRIPT + r'|[֑-ׇ̀-ͯ־]|\w)*' + SCRIPT + r'(?:' + SCRIPT + r'|[֑-ׇ̀-ͯ־]|\w)*'
STRONG_ELOL = re.compile(r'(?<![\w+/])(?<![+/]\s)(?P<strong>' + _STRONG + r')\s+(?P<szo>' + SZKRIPT_SZO + ')')
SZO_ZAROJEL = re.compile(r'(?P<szo>' + SZKRIPT_SZO + r')(?P<jel>[*_]*)\s?\(\s*(?P<strong>' + _STRONG + r')\s*\)')
ZAROJEL = re.compile(r'(\s?)\(([^()]*)\)')
SZKRIPT_VEG = re.compile(SCRIPT + r'[֑-ׇ̀-ͯ]*[\w֑-ׇ̀-ͯ]*[*_]*$')
STRONG_JEL_RX = r'<sup class="strong"[^>]*>[^<]*</sup>'
SZONEZET = '/szo/%s'


def csupasz_strongok(szoveg):
    """A szövegben jelöletlenül (csupaszon) álló Strong-számok: a jelölt alak (hivatkozás + felső index) nélkül."""
    s = re.sub(r'\[[^\]]*\]\(/szo/[^)]*\)', ' ', re.sub(STRONG_JEL_RX, ' ', szoveg))
    return re.findall(_STRONG, s)


def _alap_cim(strong):
    return strong


def strong_jel(strong, cim=None):
    """A Strong-szám jelölt alakja: halvány felső index, a `title` a szám és a rövid jelentés (`cim(strong)`)."""
    t = (cim or _alap_cim)(strong) or strong
    return '<sup class="strong" title="%s">%s</sup>' % (t.replace('&', '&amp;').replace('"', '&quot;'), strong)


def strong_link(szoveg, strong, cim=None):
    """A szó vagy kiejtés hivatkozásként a szónézetre, utána a jelölt Strong-szám. A dőlt jel (`*málé*`) a hivatkozáson belül
    marad."""
    return '[%s](%s)%s' % (szoveg, SZONEZET % strong, strong_jel(strong, cim))


def _kiejtes_elem(elem):
    """Kiejtés-e a zárójel eleme: latin betűs, legfeljebb három szó, szám, idézőjel és héber/görög betű nélkül."""
    e = elem.strip()
    return bool(e) and not re.search(SCRIPT + r'|\d|[„”"\[\]<>]', e) and len(e.split()) <= 3


def _zarojel_strong_jelol(tartalom, cim):
    """A zárójel tartalma jelölt Strong-számmal: a csak Strong-számból álló elem kiesik, a Strong-szám az előtte álló kiejtés
    (ennek híján a héber/görög szó) jelölt alakjába kerül; a „kiejtés Strong” alakú elem jelölt alakra íródik; a zárójel
    elején álló, szó nélküli Strong-szám kiesik. Más elem nem változik."""
    reszek = re.split(r'([,;]\s*)', tartalom)
    elemek = [[reszek[i], reszek[i + 1] if i + 1 < len(reszek) else ''] for i in range(0, len(reszek), 2)]
    ki = []
    for elem, sep in elemek:
        if STRONG_ELEM.fullmatch(elem) and STRONG_TAG.search(elem):
            strong = elem.strip()
            if not ki:
                # „(H7121, שֵׁם nélkül)”: előtte nincs szó, amelyhez kötődne — kiesik, mint az F123.INDOKLAS óta
                continue
            elozo = ki[-1][0]
            kozep = elozo.strip()
            elotte = elozo[:len(elozo) - len(elozo.lstrip())]
            ki[-1][0] = elotte + strong_link(kozep, strong, cim)
            continue
        m = STRONG_UTAN.match(elem)
        if m and STRONG_TAG.search(elem) and len(m.group('szo').split()) <= 3:
            szo = m.group('szo')
            eleje = szo[:len(szo) - len(szo.lstrip())]
            elem = eleje + strong_link(szo.strip(), m.group('strong'), cim)
        ki.append([elem, sep])
    szoveg = ''.join(e + s for e, s in ki)
    return re.sub(r'[,;]\s*$', '', szoveg).strip()


def strong_ki(szoveg, cim=None):
    """Egy olvasói szövegrész (sor vagy cella) a szó mellett álló Strong-szám jelölt alakjával (a védett szakasz, köztük a
    már jelölt alak, érintetlen). A név a korábbi (eltávolító) szabályé; a művelet ma jelölés (DT-F181b)."""
    v, tarolo = _vedett(szoveg)
    if not STRONG_TAG.search(v):
        return szoveg

    def vedd(s):
        tarolo.append(s)
        return '\x00%d\x00' % (len(tarolo) - 1)

    # „ὄνομα (G3686)”: a zárójelben csak a Strong-szám, előtte a szó → a szó a hivatkozás
    # (a szó utáni dőlt-zárójel — „*ὄνομα* (G3686)” — a hivatkozás után marad, a felső index elé)
    v = SZO_ZAROJEL.sub(lambda m: vedd('[%s](%s)%s%s' % (m.group('szo'), SZONEZET % m.group('strong'), m.group('jel'),
                                                         strong_jel(m.group('strong'), cim))), v)

    def zarojel(m):
        tartalom = m.group(2)
        if not STRONG_TAG.search(tartalom):
            return m.group(0)
        elotte = v[:m.start()].rstrip() if not m.group(1) else v[:m.start()]
        if not (re.search(SCRIPT, tartalom) or SZKRIPT_VEG.search(elotte.rstrip())):
            return m.group(0)
        uj = _zarojel_strong_jelol(tartalom, cim)
        if uj == tartalom:
            return m.group(0)
        return '' if not uj else '%s(%s)' % (m.group(1), vedd(uj))
    v = ZAROJEL.sub(zarojel, v)
    v = STRONG_ELOL.sub(lambda m: vedd(strong_link(m.group('szo'), m.group('strong'), cim)), v)
    return _vissza(v, tarolo)


def _cellak(sor):
    return re.split(r'(?<!\\)\|', sor)


def strong_sor(sor, tabla_fej=None, cim=None):
    """A sor a szó mellett álló Strong-szám jelölt alakjával. Táblasorban cellánként; a „Strong” fejlécű oszlop érintetlen."""
    s = sor.strip()
    if re.match(r'^#{1,6}\s', s):
        return sor
    if s.startswith('|'):
        cellak = _cellak(sor)
        if tabla_fej is None or len(cellak) != len(tabla_fej) or re.fullmatch(r'[\s|:-]+', s):
            return sor
        return '|'.join(c if 'Strong' in tabla_fej[i] else strong_ki(c, cim) for i, c in enumerate(cellak))
    return strong_ki(sor, cim)


def generalt_sorok(szoveg):
    """[generált-e] soronként (GENERÁLT-KEZDET…VÉGE, GENERÁLT-RÉS … a rés proveniencia-soráig): a mérce a kiejtés-
    szabályé (`kiejtes_szoveg._sor_reszek`), mert a kézi részt a generátor nem írja (DT569: a kiadott lapon csak a
    generált rész változhat; a kézi részt a forrásban kell javítani)."""
    import kiejtes_szoveg as KSZ
    return [g for g, _forras, _szakasz in KSZ._sor_reszek(szoveg.split('\n'))]


def strong_valtozas(szoveg):
    """[(sorszám (0-tól), régi sor, új sor, generált-e)] az olvasói szöveg azon soraira, amelyekben a `strong_sor`
    változtatna, azaz csupasz (jelöletlen) Strong-szám áll a szó mellett. A generátor a kézi sort is jelöltre írja
    (DT-F181b); a kapu így csak a generátoron kívül írt vagy elavult lapot jelzi."""
    ki = []
    gen = generalt_sorok(szoveg)
    for n, sor, idezet, fej in _sorok_tablafejjel(szoveg):
        if idezet:
            continue
        uj = strong_sor(sor, fej)
        if uj != sor:
            ki.append((n, sor, uj, gen[n]))
    return ki


def _sorok_tablafejjel(szoveg):
    """Az olvasói sorok (`olvasoi_sorok`) a táblázat fejlécével: (sorszám, sor, idézetblokk-e, fejléc-cellák vagy None).
    A táblázat első sora a fejléc (ő maga None-t kap); a táblázat a következő nem `|` sorig tart."""
    fej, elozo = None, -2
    for n, sor, idezet in olvasoi_sorok(szoveg):
        if not sor.strip().startswith('|'):
            fej = None
            yield n, sor, idezet, None
            continue
        if fej is None or n != elozo + 1:
            fej = [c.strip() for c in _cellak(sor)]
            elozo = n
            yield n, sor, idezet, None
            continue
        elozo = n
        yield n, sor, idezet, fej


def olvasoi_sorok(szoveg):
    """(sorszám, sor, idézetblokk-e) az olvasói szöveg soraiból; a többit a hívó változatlanul hagyja. Az idézetblokk a
    szótár szó szerinti idézete: csak a konverzió maradék jelei (bdb) javulnak benne."""
    komment = kod = False
    szakasz = ''
    for n, sor in enumerate(szoveg.split('\n')):
        s = sor.strip()
        if kod:
            if s.startswith('```'):
                kod = False
            continue
        if s.startswith('```'):
            kod = True
            continue
        if komment:
            if '-->' in sor:
                komment = False
            continue
        if '<!--' in sor and '-->' not in sor.split('<!--', 1)[1]:
            komment = True
            continue
        m = re.match(r'^(#{1,2})\s+(.*)', s)
        if m:
            szakasz = m.group(2).strip()
        if szakasz.startswith(KIZART_SZAKASZ):
            continue
        if re.match(r'^\[\^[^\]]+\]:\s*(?:proveniencia|forrás)\s*:', s) or 'scope=' in s and s.startswith('[^'):
            continue
        yield n, sor, s.startswith('>')


def alkalmaz(szoveg, idezojel=True, konyv=True, bdb=True, strong=True, strong_cim=None):
    """`strong_cim(strong)`: a jelölt Strong-szám `title`-je (a szám és a rövid jelentés; alapból a szám). A Strong-jelölés
    a kézi résen is fut (DT-F181b): a forrás „(szó, kiejtés, H4196)” alakja a generátor bemenete, a szöveg nem változik."""
    sorok = szoveg.split('\n')
    for n, sor, idezet, fej in _sorok_tablafejjel(szoveg):
        uj = sor
        if strong and not idezet:
            uj = strong_sor(uj, fej, strong_cim)
        if bdb:
            uj = bdb_sor(uj)
        if konyv and not idezet:
            uj = konyv_sor(uj)
        if idezojel and not idezet:
            uj = idezojel_sor(uj)
        sorok[n] = uj
    return '\n'.join(sorok)
