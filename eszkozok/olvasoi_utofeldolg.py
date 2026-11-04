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
    strong     a Strong-szám ott, ahol mellette a héber/görög szó (és a kiejtése) áll (F123.INDOKLAS; lásd strong_ki);
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
VEDETT = re.compile(r'<!--.*?-->|<[^>]+>|`[^`]*`|\]\([^)]*\)|https?://\S+|(?:\\?\|\s*)?scope=.*?ts=[\dT:Z.-]+')

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


# --- Strong-szám a szó és a kiejtése mellett (F123.INDOKLAS) -----------------------------------------------------------
# A lap olvasói szövegében a Strong-szám belső azonosító; ahol mellette ott a héber/görög szó (és a kiejtése), ismétlés,
# és kikerül: „ὄνομα (G3686) nélkül” -> „ὄνομα nélkül”, „(ἐπικαλέω, epikaleó G1941)” -> „(ἐπικαλέω, epikaleó)”, „H6089 עֶצֶב” -> „עֶצֶב”. Ahol a Strong-szám egyedül áll (a szó nincs mellette, pl. „a H7496/H7497 Strong-szám
# szerinti megoszlás”), vagy lánc tagja („H7121+H8034”, „H0369 + H7121”), az adat része, nem változik. A táblázat
# „Strong” fejlécű oszlopa és a címsor érintetlen. Az olvasói kapu BELSO-ellenőrzése ugyanezt a függvényt hívja
# (`strong_valtozas`): amit a kapu megfog, azt a generátor eltávolítja.
SCRIPT = '[֐-׿Ͱ-Ͽἀ-῿]'
_STRONG = r'[HG]\d{4}[a-z]?'
STRONG_TAG = re.compile(r'(?<![\w+/])(?<![+/]\s)' + _STRONG + r'(?![\w+/])(?!\s[+/])')
STRONG_ELEM = re.compile(r'\s*' + _STRONG + r'\s*')
STRONG_UTAN = re.compile(r'^(?P<szo>[^\d,;()]*\S)\s+' + _STRONG + r'\s*$')   # „epikaleó G1941”
STRONG_ELOL = re.compile(r'(?<![\w+/])(?<![+/]\s)' + _STRONG + r'\s+(?=' + SCRIPT + ')')
ZAROJEL = re.compile(r'(\s?)\(([^()]*)\)')
SZKRIPT_VEG = re.compile(SCRIPT + r'[֑-ׇ̀-ͯ]*[\w֑-ׇ̀-ͯ]*[*_]*$')


def _zarojel_strong_ki(tartalom):
    """A zárójel tartalma a Strong-tag nélkül: a vesszővel/pontosvesszővel elválasztott elemek közül az, amely csak a
    Strong-szám, kiesik; a „szó Strong” alakú elemből a Strong-szám esik ki. Más elem nem változik."""
    reszek = re.split(r'([,;]\s*)', tartalom)
    elemek = [(reszek[i], reszek[i + 1] if i + 1 < len(reszek) else '') for i in range(0, len(reszek), 2)]
    ki = []
    for elem, sep in elemek:
        if STRONG_ELEM.fullmatch(elem) and STRONG_TAG.search(elem):
            continue
        m = STRONG_UTAN.match(elem)
        if m and STRONG_TAG.search(elem) and len(m.group('szo').split()) <= 3:
            elem = m.group('szo')
        ki.append((elem, sep))
    szoveg = ''.join(e + s for e, s in ki)
    return re.sub(r'[,;]\s*$', '', szoveg).strip()


def strong_ki(szoveg):
    """Egy olvasói szövegrész (sor vagy cella) a szó mellett álló Strong-szám nélkül (a védett szakasz érintetlen)."""
    v, tarolo = _vedett(szoveg)
    if not STRONG_TAG.search(v):
        return szoveg

    def zarojel(m):
        tartalom = m.group(2)
        if not STRONG_TAG.search(tartalom):
            return m.group(0)
        elotte = v[:m.start()].rstrip() if not m.group(1) else v[:m.start()]
        if not (re.search(SCRIPT, tartalom) or SZKRIPT_VEG.search(elotte.rstrip())):
            return m.group(0)
        uj = _zarojel_strong_ki(tartalom)
        if uj == tartalom:
            return m.group(0)
        return '' if not uj else '%s(%s)' % (m.group(1), uj)
    v = ZAROJEL.sub(zarojel, v)
    v = STRONG_ELOL.sub('', v)
    return _vissza(v, tarolo)


def _cellak(sor):
    return re.split(r'(?<!\\)\|', sor)


def strong_sor(sor, tabla_fej=None):
    """A sor a szó mellett álló Strong-szám nélkül. Táblasorban cellánként; a „Strong” fejlécű oszlop érintetlen."""
    s = sor.strip()
    if re.match(r'^#{1,6}\s', s):
        return sor
    if s.startswith('|'):
        cellak = _cellak(sor)
        if tabla_fej is None or len(cellak) != len(tabla_fej) or re.fullmatch(r'[\s|:-]+', s):
            return sor
        return '|'.join(c if 'Strong' in tabla_fej[i] else strong_ki(c) for i, c in enumerate(cellak))
    return strong_ki(sor)


def generalt_sorok(szoveg):
    """[generált-e] soronként (GENERÁLT-KEZDET…VÉGE, GENERÁLT-RÉS … a rés proveniencia-soráig): a mérce a kiejtés-
    szabályé (`kiejtes_szoveg._sor_reszek`), mert a kézi részt a generátor nem írja (DT569: a kiadott lapon csak a
    generált rész változhat; a kézi részt a forrásban kell javítani)."""
    import kiejtes_szoveg as KSZ
    return [g for g, _forras, _szakasz in KSZ._sor_reszek(szoveg.split('\n'))]


def strong_valtozas(szoveg):
    """[(sorszám (0-tól), régi sor, új sor, generált-e)] az olvasói szöveg azon soraira, amelyekben a `strong_sor`
    változtatna. A generátor csak a generált sort írja át; a kapu a kézi sort is jelzi (a forrásban javítandó)."""
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


def alkalmaz(szoveg, idezojel=True, konyv=True, bdb=True, strong=True):
    sorok = szoveg.split('\n')
    gen = generalt_sorok(szoveg) if strong else None
    for n, sor, idezet, fej in _sorok_tablafejjel(szoveg):
        uj = sor
        if strong and not idezet and gen[n]:
            uj = strong_sor(uj, fej)
        if bdb:
            uj = bdb_sor(uj)
        if konyv and not idezet:
            uj = konyv_sor(uj)
        if idezojel and not idezet:
            uj = idezojel_sor(uj)
        sorok[n] = uj
    return '\n'.join(sorok)
