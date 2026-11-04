#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
olvasoi_kapu.py -- a gépi olvasói kapu egy generált lexikonlapon (`lexikon/[ID]_TUDOMANYOS.md`).

A lap-átvilágítás (2026-11-02) olvasói hibái átmentek a szerkezeti kapukon (Feed 1–8, ellenoriz.py, CI).
Ez az eszköz az átvilágítás „Mi gépesíthető” táblázatának pontjait méri azon, amit az olvasó lát: a lapon.
Csak olvas; lapot, prózát, adatot nem javít. A Feed 9. kapuja (`muhely_allapot.py`) erre épül (DT-F156k).

Ellenőrzések (azonosító — súlyosság):
    BELSO        belső jelölés az olvasói szövegben (DT/N/F-tétel, #nnn, P1–P7, ELLENOR_, orkesztrátor,
                 gerinc, .tsv, manual, belső fájl; a Strong-szám, ahol mellette ott a héber/görög szó
                 és a kiejtése — a táblázat „Strong” oszlopa kivétel, F123.INDOKLAS)        — BUKÁS
    MOTIVUM_ID   más motívum azonosítója link nélkül                                       — FIGYELMEZTETÉS
    PONT         „N. pont” hivatkozás: nem létező szakaszra vagy rossz névvel BUKÁS, egyébként FIGYELMEZTETÉS
    ANGOL        angol maradék és munkazsargon a szólistából                               — BUKÁS
    ANGOL_SOR    ≥3 angol funkciószó egy sorban                                            — FIGYELMEZTETÉS
    IDEZOJEL     egyenes " a magyar szövegben                                              — BUKÁS
    ATIRAS       ugyanaz a héber/görög szó két kiejtéssel                                  — BUKÁS
    ATIRAS_VALT  a lapon álló kiejtés ékezet-eltérő változata dőlt/zárójeles helyen        — FIGYELMEZTETÉS
    KONYV        könyvrövidítés nem a `Konyv_normalizalo_tabla.tsv` alakjával              — BUKÁS
    BDB_JEL      torzult jel a szövegben (^, ®, °, a BDB átírási betűkészletének ¹ µ £ ¥ ‰ ƒ ‡ ¢ jele, rafe,
                 latin betű héber szóhoz tapadva, ,,)                                         — BUKÁS
    ZAROJEL      nyitva maradt zárójel (a 2. Szótári háttérben BUKÁS, máshol FIGYELMEZTETÉS)
    FUNKCIO_URES az 1. tábla „Funkció” oszlopában üres cella                               — BUKÁS
    IDEZET       az 1/a jegyzet idézete nem a fölötte álló Károli-vers szövege, és nincs „saját fordítás” jelölés — BUKÁS
    KIVONAT_SZAM a Kivonat darabszáma eltér a tábla összesítőjétől                         — FIGYELMEZTETÉS
    KOLOFON      hiányzó Kiadás / Változásjegyzék / Próza modellje, üres törzsadat-mező    — BUKÁS
    HIANYJEL     belső hiányjelzés az olvasói cellában („(nincs …)”)                        — FIGYELMEZTETÉS
    SZINT_ALATT  üres vagy az arany laphoz mérve szint alatti blokk                        — FIGYELMEZTETÉS
    KH_MASOLT    a Károli-KH lista más vers másolata (`karoli_kh_epseg.py`; javítás: N-F156a) — FIGYELMEZTETÉS
    LABJEGYZET   definíció nélküli lábjegyzet (átvett: `ellenoriz.lap_labjegyzet_hianyok`, ha a main-en van) — BUKÁS
    PROZA_1A     az 1/a igehely alatt nincs kerek próza vagy „Funkció:” sor (átvett: `proza_1a.meres`)   — BUKÁS

Az olvasói szöveg: minden látható sor, kivéve a HTML-megjegyzést, a kódblokkot, a technikai dőlt sort (egész
sor `*…*`), a proveniencia-lábjegyzetet (`[^x]: proveniencia:` / `forrás:` / `scope=`), valamint a Tartalomjegyzék,
a Jelmagyarázat és a Kolofon szakaszát (ezek a lap készítőinek szóló, tervezett technikai részek; a Kolofont a
KOLOFON ellenőrzés külön méri). A küszöbök kalibrálása: `naplok/OLVASOI_KAPU_jelentes.md`.

Használat:
    python eszkozok/olvasoi_kapu.py ID [ID ...] [--reszletes] [--json FAJL]
    python eszkozok/olvasoi_kapu.py --osszes
Kilépési kód: 1, ha bármely lapon van BUKÁS; 0 egyébként.
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

BUKAS, FIGY = 'BUKÁS', 'FIGYELMEZTETÉS'
ARANY = 'ISTENTISZT-001'

KIZART_SZAKASZ = ('Tartalomjegyzék', 'Jelmagyarázat', 'Kolofon')
IRODALOM = '8. Irodalom'

# --- BELSO: belső jelölések (az átvilágítás A4, A21, T3, T14, G4, G5, G7)
BELSO = [
    (re.compile(r'(?<![\w-])DT-?F?\d+[a-z]?\b'), 'döntés-azonosító'),
    (re.compile(r'(?<![\w-])N-F\d+[a-z]?\b|(?<![\w-])N\d{1,3}\b'), 'N-tétel'),
    (re.compile(r'(?<![\w/.#-])F\d{1,3}(?:\.\d+)?\b'), 'F-tétel'),
    (re.compile(r'(?<![\w&/])#\d{2,3}\b'), 'feladatszám'),
    (re.compile(r'(?<![\w-])P[1-7]\b'), 'munkalépés-jel'),
    (re.compile(r'ELLENOR_'), 'ellenőri napló'),
    (re.compile(r'orkesztrátor', re.I), 'munkafolyamat-szereplő'),
    (re.compile(r'\bgerinc', re.I), 'belső szó (gerinc)'),
    (re.compile(r'\.tsv\b|\.py\b|[\w/]+\.md\b|NYITOTT_FELADATOK'), 'belső fájl'),
    (re.compile(r'\bmanual\b'), 'proveniencia-érték (manual)'),
    (re.compile(r'\b(?:tanítói|forrás)\s?fájl\w*|\bfájl(?:ban|ból|ja|jában)\b', re.I), 'belső fájl'),
]
MOTIVUM_ID = re.compile(r'(?<![\w\[/#`-])([A-ZÁÉÍÓÖŐÚÜŰ]{3,}-\d{3})\b(?![\]`])')

# --- ANGOL: szólista (A22, T11, G4) és funkciószó-küszöb
ANGOL_SZO = re.compile(r'\bgap\b|\bstudy\b|\bwas called\b|\bhaving been\b|\bscan\w*|LXX_OS|'
                       r'\bpipeline\b|\bworkflow\b|\bbatch\w*|\bverdict\b|(?<![\w.])[1-3]?[A-Z][a-z]{1,3}\.\d+\.\d+\b',
                       re.I)
# az „is” és a „be” magyar szó is, ezért nincs a listában
ANGOL_FUNKCIO = re.compile(r'\b(the|and|of|with|which|from|that|this|are|was|were|by|to|in|for|not|or|as|an|it|'
                           r'its|his|her|their|who|whom|into|upon|unto)\b')
ANGOL_SOR_MIN = 3

# --- BDB_JEL (A12, A23, T8)
BDB_JEL = [
    (re.compile(r'(?<!\[)\^'), 'nyers ^ elválasztó'),
    (re.compile(r'[®°]'), 'torzult jel (® / °)'),
    # F123.GENKOR: a DictBDB.json átírási betűkészletének többi torz jele (N89); a † (Abbott-Smith) és a ± (±1) jogos jel
    (re.compile(r'[¹µ£¥‰ƒ‡¢]'), 'torzult jel (a BDB átírási betűkészlete: ¹ µ £ ¥ ‰ ƒ ‡ ¢)'),
    (re.compile('ֿ'), 'rafe (ֿ) pontjel a héber szóban'),
    (re.compile(r'[א-ת][֑-ׇ]*[A-Za-z]|[A-Za-z][א-ת]'), 'latin betű héber szóhoz tapadva'),
    (re.compile(r'[^\s,],,'), 'dupla vessző'),
]

# számnevek a Kivonat-összevetéshez
SZAMNEV = {'egy': 1, 'két': 2, 'kettő': 2, 'három': 3, 'négy': 4, 'öt': 5, 'hat': 6, 'hét': 7, 'nyolc': 8,
           'kilenc': 9, 'tíz': 10, 'tizenegy': 11, 'tizenkét': 12, 'tizenkettő': 12, 'tizenhárom': 13,
           'tizennégy': 14, 'tizenöt': 15, 'tizenhat': 16, 'tizenhét': 17, 'tizennyolc': 18, 'tizenkilenc': 19,
           'húsz': 20, 'mindkét': 2, 'mindhárom': 3, 'mind a négy': 4, 'mind az öt': 5}
SZAM_FONEV = r'(?:igehely|hely|előfordulás|vers|ószövetségi|újszövetségi)'


# ----------------------------------------------------------------------------- segédek

def tsv(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t') + [''] * (len(fej) - len(s.split('\t'))))) for s in sorok[1:]]


_KONYV = None


def konyvek():
    """(magyar rövidítések halmaza, magyar -> STEPBible, ÚSZ-rövidítések halmaza)."""
    global _KONYV
    if _KONYV is None:
        sorok = tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
        hu = [s['Magyar rövidítés'] for s in sorok]
        step = {s['Magyar rövidítés']: s['STEPBible-rövidítés'] for s in sorok}
        i = next(k for k, s in enumerate(sorok) if s['STEPBible-rövidítés'] == 'Mat')
        _KONYV = (set(hu), step, set(hu[i:]))
    return _KONYV


def ekezet_nelkul(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def normal_szoveg(s):
    """Idézet-összevetéshez: kisbetű, ékezet és írásjel nélkül, egyszeres szóközzel."""
    s = ekezet_nelkul(s.lower())
    s = re.sub(r'[^\w\s]', ' ', s)
    return ' '.join(s.split())


def lathato(s):
    """A sor látható szövege: megjegyzés, horgony, link-cél és lábjegyzet-hivatkozás nélkül."""
    s = re.sub(r'<!--.*?-->', '', s)
    s = re.sub(r'<a id="[^"]*"></a>', '', s)
    s = re.sub(r'\]\([^)]*\)', ']', s)
    s = re.sub(r'\[\^[^\]]+\]', '', s)
    # a cellába vagy sorba ágyazott proveniencia (`scope=… | forras=… | ts=…`, „forrás: `fájl`”) nem olvasói próza
    s = re.sub(r'(?:\\?\|\s*)?scope=.*?ts=[\dT:Z.-]+', '', s)
    s = re.sub(r'forrás:\s*`[^`]*`', '', s)
    return s


def kod_nelkul(s):
    return re.sub(r'`[^`]*`', ' ', s)


class Sor:
    __slots__ = ('n', 'nyers', 'szoveg', 'fajta', 'szakasz', 'alszakasz')

    def __init__(self, n, nyers, szoveg, fajta, szakasz, alszakasz):
        self.n, self.nyers, self.szoveg, self.fajta = n, nyers, szoveg, fajta
        self.szakasz, self.alszakasz = szakasz, alszakasz

    @property
    def olvasoi(self):
        """Olvasói próza-e (az ellenőrzések nagy része csak ezeken fut)."""
        if self.fajta not in ('proza', 'tabla', 'cim', 'labjegyzet'):
            return False
        return not self.szakasz.startswith(KIZART_SZAKASZ)


def tagol(szoveg):
    """A lap soraira bontása fajtával és szakasszal."""
    ki = []
    komment = kod = False
    szakasz = alszakasz = ''
    elozo = ''
    tabla_fej = None
    for n, nyers in enumerate(szoveg.replace('\r', '').split('\n'), 1):
        s = nyers
        if kod:
            if s.strip().startswith('```'):
                kod = False
            ki.append(Sor(n, nyers, '', 'kod', szakasz, alszakasz))
            continue
        if s.strip().startswith('```'):
            kod = True
            ki.append(Sor(n, nyers, '', 'kod', szakasz, alszakasz))
            continue
        if komment:
            if '-->' in s:
                komment = False
                s = s.split('-->', 1)[1]
            else:
                ki.append(Sor(n, nyers, '', 'komment', szakasz, alszakasz))
                continue
        if '<!--' in s and '-->' not in s.split('<!--', 1)[1]:
            komment = True
            s = s.split('<!--', 1)[0]
        lat = lathato(s)
        t = lat.strip()
        m = re.match(r'^(#{1,6})\s+(.*)', t)
        if m:
            if len(m.group(1)) <= 2:
                szakasz, alszakasz = m.group(2).strip(), ''
            else:
                alszakasz = m.group(2).strip()
            fajta = 'cim'
        elif not t:
            fajta = 'ures'
        elif re.match(r'^\[\^[^\]]+\]:', nyers.strip()):
            def_szoveg = nyers.split(':', 1)[1].strip()
            fajta = 'proveniencia' if re.match(r'(proveniencia|forrás)\s*:', def_szoveg) or 'scope=' in def_szoveg \
                else 'labjegyzet'
            lat = def_szoveg
        elif t.startswith('|'):
            fajta = 'tabla'
            cellak = re.split(r'(?<!\\)\|', t.strip('|'))
            if tabla_fej is None:
                tabla_fej = [c.strip() for c in cellak]
            elif len(cellak) == len(tabla_fej):
                # a „Forrás” oszlop proveniencia (fájlnév, dataset-név): nem olvasói próza
                lat = '|' + '|'.join('' if tabla_fej[i] == 'Forrás' else c for i, c in enumerate(cellak)) + '|'
        elif t.startswith('>'):
            fajta = 'idezetblokk'  # a szótár angol eredetijének szó szerinti idézete
        elif re.match(r'^\*[^*].*\*$', t) or t in ('*', '**'):
            fajta = 'karoli' if re.match(r'^\*\*[^*]+\d+:\d+[^*]*\*\*$', elozo.strip()) else 'dolt'
        else:
            fajta = 'proza'
        if fajta != 'tabla':
            tabla_fej = None
        ki.append(Sor(n, nyers, lat, fajta, szakasz, alszakasz))
        if fajta != 'ures':
            elozo = lat
    return ki


def bekezdesek(sorok):
    """Az egymást követő prózasorok bekezdésekké fűzve (a lap kézi sortöréssel tördel): [(első sor, szöveg)].
    Listaelem (`- `, `1. `) új bekezdést kezd."""
    ki, akt = [], None
    for s in sorok:
        if s.fajta == 'proza' and not (akt and re.match(r'^\s*(?:[-*]|\d+\.)\s', s.szoveg)):
            if akt is None:
                akt = [s, [s.szoveg.strip()]]
            else:
                akt[1].append(s.szoveg.strip())
            continue
        if akt:
            ki.append((akt[0], ' '.join(akt[1])))
            akt = None
        if s.fajta == 'proza':
            akt = [s, [s.szoveg.strip()]]
    if akt:
        ki.append((akt[0], ' '.join(akt[1])))
    return ki


def talalat(azon, suly, sor, idezet, uzenet, kulcs=None):
    """Egy találat. A `kulcs` a csoportosítás alapja: az azonos azonosítójú, súlyosságú és kulcsú találatok egy
    szakaszon belül egy tételbe olvadnak (`db`, `sorok`), mert ugyanaz a hiba sokszor ismétlődik (pl. tábla-oszlop)."""
    return {'azonosito': azon, 'sulyossag': suly, 'sor': sor, 'idezet': (idezet or '').strip()[:160],
            'uzenet': uzenet, 'kulcs': kulcs}


def csoportosit(talalatok, sorok):
    szakasz = {s.n: s.szakasz for s in sorok}
    ki, index = [], {}
    for t in sorted(talalatok, key=lambda x: (x['sor'], x['azonosito'])):
        if t['kulcs'] is None:
            t = dict(t, db=1, sorok=[t['sor']])
            t.pop('kulcs')
            ki.append(t)
            continue
        k = (t['azonosito'], t['sulyossag'], t['kulcs'], szakasz.get(t['sor'], ''))
        if k in index:
            index[k]['db'] += 1
            index[k]['sorok'].append(t['sor'])
            continue
        t = dict(t, db=1, sorok=[t['sor']])
        t.pop('kulcs')
        index[k] = t
        ki.append(t)
    return ki


def kornyezet(s, m, szel=50):
    return s[max(0, m.start() - szel):m.end() + szel]


# ----------------------------------------------------------------------------- ellenőrzések

def ell_belso(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        for rx, nev in BELSO:
            if nev == 'belső fájl' and s.szakasz.startswith(IRODALOM):
                continue  # az Irodalom a lapot és a forrásfájlt idézhetőként nevezi meg
            m = rx.search(s.szoveg)
            if m:
                ki.append(talalat('BELSO', BUKAS, s.n, kornyezet(s.szoveg, m), nev + ': ' + m.group(0),
                                  nev + m.group(0)))
        if s.fajta != 'cim':
            for m in MOTIVUM_ID.finditer(s.szoveg):
                ki.append(talalat('MOTIVUM_ID', FIGY, s.n, kornyezet(s.szoveg, m),
                                  'motívum-azonosító link nélkül: ' + m.group(1), m.group(1)))
    ki += ell_belso_strong(sorok)
    return ki


def ell_belso_strong(sorok):
    """BELSO, Strong-szám (F123.INDOKLAS): a Strong-szám az olvasói prózában, ahol mellette ott a héber/görög szó és a
    kiejtése. A mérce az utófeldolgozó `strong_valtozas`-a (amit itt megfog, azt a generátor eltávolítja); kivétel a
    táblázat „Strong” oszlopa, a címsor, az egyedül vagy láncban álló Strong-szám."""
    import olvasoi_utofeldolg as OU
    olvasoi = {s.n for s in sorok if s.olvasoi and s.fajta != 'cim'}
    ki = []
    for n, regi, uj, generalt in OU.strong_valtozas('\n'.join(s.nyers for s in sorok)):
        if n + 1 not in olvasoi:
            continue
        for m in re.finditer(OU._STRONG, regi):
            if m.group(0) not in uj or regi.count(m.group(0)) > uj.count(m.group(0)):
                ki.append(talalat('BELSO', BUKAS, n + 1, kornyezet(regi, m),
                                  'Strong-szám a szó és a kiejtése mellett: ' + m.group(0)
                                  + ('' if generalt else ' (kézi rész: a forrásban javítandó)'), 'strong'))
                break
    return ki


def szakasz_cimek(sorok):
    """{'3': '3. LXX-fordítói döntések', ...} a `## N.` fejlécekből."""
    ki = {}
    for s in sorok:
        if s.fajta == 'cim' and s.szoveg.startswith('## '):
            m = re.match(r'##\s+(\d+)\.\s*(.*)', s.szoveg.strip())
            if m:
                ki.setdefault(m.group(1), m.group(2))
    return ki


def alcimek(sorok):
    """{(`##` szakasz, szám)}: a szakaszon belüli számozott alcímek (`#### 2. Mélységi szócikk`)."""
    ki = set()
    for s in sorok:
        if s.fajta == 'cim' and not s.szoveg.startswith('## '):
            m = re.match(r'#{3,6}\s+(\d+)\.', s.szoveg.strip())
            if m:
                ki.add((s.szakasz, m.group(1)))
    return ki


def ell_pont(sorok):
    cimek = szakasz_cimek(sorok)
    alc = alcimek(sorok)
    ki = []
    rx = re.compile(r'(?<![\d.])(\d+)\.\s*pont\w*\b(?:\s*,\s*[„"]?([A-ZÁÉÍÓÖŐÚÜŰ][\w-]+))?')
    for s in sorok:
        if not s.olvasoi:
            continue
        for m in rx.finditer(s.szoveg):
            szam, nev = m.group(1), m.group(2)
            if (s.szakasz, szam) in alc and not nev:
                continue  # a szakasz saját számozott alpontja (pl. a Szótári háttér „2. pont”-ja)
            if szam not in cimek:
                ki.append(talalat('PONT', BUKAS, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont”: a lapon nincs %s. szakasz' % (szam, szam)))
            elif nev and nev.lower() not in cimek[szam].lower():
                ki.append(talalat('PONT', BUKAS, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont, %s”: a lap %s. szakasza „%s”' % (szam, nev, szam, cimek[szam])))
            else:
                ki.append(talalat('PONT', FIGY, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont”: a lap szakaszait nem pontnak hívja; a forrás saját számozása?' % szam))
    return ki


def ell_angol(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi or s.szakasz.startswith(IRODALOM):
            continue
        t = kod_nelkul(s.szoveg)
        m = ANGOL_SZO.search(t)
        if m:
            ki.append(talalat('ANGOL', BUKAS, s.n, kornyezet(t, m), 'angol maradék / zsargon: ' + m.group(0),
                              m.group(0).lower()))
        fsz = ANGOL_FUNKCIO.findall(t)
        if len(fsz) >= ANGOL_SOR_MIN:
            ki.append(talalat('ANGOL_SOR', FIGY, s.n, t[:140], '%d angol funkciószó (%s)' % (
                len(fsz), ', '.join(sorted(set(fsz))))))
    return ki


def ell_idezojel(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        t = re.sub(r'<[^>]+>', '', kod_nelkul(s.szoveg))
        if '"' in t:
            i = t.index('"')
            ki.append(talalat('IDEZOJEL', BUKAS, s.n, t[max(0, i - 50):i + 60],
                              'egyenes " a magyar szövegben (a „…” helyett)', 'egyenes'))
    return ki


HEBER_SZO = r'[א-תיִ-ﭏ][֑-ׇא-תיִ-ﭏ]*'
GOROG_SZO = r'[Ͱ-Ͽἀ-῿]+'
PAR_RX = re.compile(r'((?:%s|%s)(?:[\s־]+(?:%s|%s))*)\s*\(([^()]{1,80})\)' % (
    HEBER_SZO, GOROG_SZO, HEBER_SZO, GOROG_SZO))


def heber_kulcs(szo):
    if re.search(r'[֐-׿]', szo):
        return re.sub('[֑-ֽ֯׀׃]', '', szo)
    return ekezet_nelkul(szo.lower())


def kiejtes_parok(sorok):
    """[(héber/görög kulcs, kiejtés, sor)] a lapon álló „szó (kiejtés)” párokból."""
    egy, tobb = [], []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures'):
            continue
        for m in PAR_RX.finditer(s.szoveg):
            szavak = [heber_kulcs(w) for w in re.split(r'[\s־]+', m.group(1)) if w]
            belso = re.sub(r'\b[HG]\d{3,5}[a-z]?\b', ' ', m.group(2))
            belso = re.sub(r'[*_;,]', ' ', belso.split(':')[0])
            kiejt = [w.lower().strip("-'’") for w in re.split(r'[\s]+', belso) if w]
            if len(szavak) != len(kiejt) or not all(re.match(r"^[A-Za-zÁ-ž'’ʼ-]+$", w) for w in kiejt):
                continue
            (egy if len(szavak) == 1 else tobb).append((szavak, kiejt, s.n, m.group(0)))
    ki = [(sz[0], k[0], n, idez) for sz, k, n, idez in egy]
    ismert = {(sz[0], k[0]) for sz, k, _, _ in egy}
    for szavak, kiejt, n, idez in tobb:
        # a szótárak angol szövegében a héber szócsoport fordított (vizuális) sorrendben is állhat: azt az
        # irányt fogadjuk el, amelyik több egyszavas párral egyezik
        elore = sum((h, k) in ismert for h, k in zip(szavak, kiejt))
        hatra = sum((h, k) in ismert for h, k in zip(reversed(szavak), kiejt))
        if hatra > elore:
            szavak = list(reversed(szavak))
        ki += [(h, k, n, idez) for h, k in zip(szavak, kiejt)]
    return ki


def ell_atiras(sorok):
    ki = []
    parok = kiejtes_parok(sorok)
    by = {}
    for kulcs, k, n, idez in parok:
        by.setdefault(kulcs, {}).setdefault(k, []).append((n, idez))
    for kulcs, valt in by.items():
        if len(valt) > 1:
            elso = sorted((v[0][0], k, v[0][1]) for k, v in valt.items())
            ki.append(talalat('ATIRAS', BUKAS, elso[1][0], ' · '.join(x[2] for x in elso[:3]),
                              'egy szó %d kiejtéssel: %s' % (len(valt), ', '.join(
                                  '%s (sor %d)' % (k, n) for n, k, _ in elso))))
    # a lapon álló kiejtések ékezet-eltérő változata dőlt vagy zárójeles helyen (pl. hádész / hadész, tohu)
    ismert = {}
    for kulcs, k, n, _ in parok:
        if len(ekezet_nelkul(k)) >= 4 and k != ekezet_nelkul(k):
            ismert.setdefault(ekezet_nelkul(k), set()).add(k)
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'karoli') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue  # a Károli-vers alakja („Seol”) nem a lap kiejtése
        reszek = re.findall(r'(?<!\*)\*([^*]+)\*(?!\*)|\(([^()]*)\)', s.szoveg)
        for dolt, zar in reszek:
            for w in re.findall(r'[A-Za-zÁ-ž]+', dolt or zar):
                wk = w.lower()
                alap = ekezet_nelkul(wk)
                if alap in ismert and wk not in ismert[alap]:
                    ki.append(talalat('ATIRAS_VALT', FIGY, s.n, s.szoveg[:140],
                                      '„%s” — a lapon máshol: %s' % (w, ', '.join(sorted(ismert[alap]))), wk))
    return ki


# a magyar rövidítés pont nélküli; a ponttal álló alak (Lob. Path. Element. 2:6) bibliográfia
KONYV_RX = re.compile(r'(?<![\w./#-])((?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6})\s(\d{1,3})[:,](\d{1,3})')
SZOTAR_ALAK = re.compile(r'(?:BDB|Thayer|szótár)-?(?:ben|ban)?:\s*„$')  # a szótár saját alakját szó szerint idézi


# a normalizáló tábla csak a 66 könyvet tartja; a deuterokanonikus és pszeudepigráf könyvek rövidítése nem hiba
DEUTERO = {'Tób', 'Jud', 'Bölcs', 'Sir', 'Bár', '1Makk', '2Makk', 'Énokh', '1Énokh', 'Jub'}
NEM_KONYV = {'Az', 'A', 'Lásd', 'Vö'}  # mondatkezdő névelő/utalószó egy könyv nélküli fejezet:vers előtt


def ell_konyv(sorok):
    hu = konyvek()[0] | DEUTERO | NEM_KONYV
    ki = []
    for s in sorok:
        if not s.olvasoi and s.fajta != 'dolt':
            continue
        if s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        t = kod_nelkul(s.szoveg)
        for m in KONYV_RX.finditer(t):
            if m.group(1) not in hu and not SZOTAR_ALAK.search(t[max(0, m.start() - 20):m.start()]):
                ki.append(talalat('KONYV', BUKAS, s.n, kornyezet(s.szoveg, m, 30),
                                  'könyvrövidítés nem a normalizáló tábla alakjával: „%s”' % m.group(1), m.group(1)))
    return ki


def ell_bdb(sorok):
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'proveniencia') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        t = kod_nelkul(s.szoveg)
        for rx, nev in BDB_JEL:
            m = rx.search(t)
            if m:
                ki.append(talalat('BDB_JEL', BUKAS, s.n, kornyezet(t, m, 40), nev, nev))
        if s.fajta in ('labjegyzet', 'dolt', 'tabla'):
            for r in (t.split('|') if s.fajta == 'tabla' else [t]):
                if zarojel_nyitva(r):
                    ki.append(zarojel_talalat(s, r))
                    break
    for s, b in bekezdesek(sorok):
        if not s.szakasz.startswith(KIZART_SZAKASZ) and zarojel_nyitva(kod_nelkul(b)):
            ki.append(zarojel_talalat(s, kod_nelkul(b)))
    return ki


def zarojel_nyitva(r):
    return r.count('(') > r.count(')')


def zarojel_talalat(s, r):
    i = r.rfind('(')
    szotar = s.szakasz.startswith('2. Szótári')
    return talalat('ZAROJEL', BUKAS if szotar else FIGY, s.n, r[max(0, i - 60):i + 60], 'nyitva maradt zárójel')


def elso_tabla(sorok, szakasz_kezd):
    """Az adott szakasz első táblája: (fejléc-cellák, [(sor, cellák)])."""
    fej, ki = None, []
    for s in sorok:
        if not s.szakasz.startswith(szakasz_kezd):
            if fej:
                break
            continue
        if s.fajta == 'tabla':
            cellak = [c.strip() for c in s.szoveg.strip().strip('|').split('|')]
            if fej is None:
                fej = cellak
            elif not all(re.match(r'^:?-+:?$', c) for c in cellak if c):
                ki.append((s.n, cellak))
        elif fej is not None and s.fajta != 'ures':
            break
    return fej, ki


def ell_funkcio(sorok):
    fej, tabla = elso_tabla(sorok, '1. Előfordulások')
    if not fej:
        return []
    oszl = next((i for i, c in enumerate(fej) if c.startswith('Funkció')), None)
    if oszl is None:
        return [talalat('FUNKCIO_URES', BUKAS, 0, ' | '.join(fej), 'az 1. táblában nincs „Funkció” oszlop')]
    ki = []
    for n, cellak in tabla:
        if oszl >= len(cellak) or cellak[oszl].strip(' *') in ('', '—', '-', '–'):
            ki.append(talalat('FUNKCIO_URES', BUKAS, n, cellak[0], 'üres „Funkció” cella', 'ures'))
    return ki


IDEZET_RX = re.compile(r'(\(?)\s*(?:„([^”"]+)[”"]|"([^"]+)")')


def blokkok_1a(sorok):
    """[(igehely, sor, Károli-vers, [prózasorok])] az 1/a részből."""
    ki, akt = [], None
    for s in sorok:
        if not s.alszakasz.startswith('1/a') and not s.szakasz.startswith('1/a'):
            if akt:
                ki.append(akt)
                akt = None
            continue
        m = re.match(r'^\*\*([^*]+\d+:\d+[^*]*)\*\*\s*$', s.szoveg.strip())
        if m:
            if akt:
                ki.append(akt)
            akt = [m.group(1).strip(), s.n, '', []]
        elif akt is not None and s.fajta == 'karoli' and not akt[2]:
            akt[2] = s.szoveg.strip().strip('*')
        elif akt is not None and s.fajta == 'proza':
            akt[3].append(s)
    if akt:
        ki.append(akt)
    return ki


IDEZET_SZO_HASONLOSAG = 0.75  # szavanként: a modernizált helyesírás (setétség → sötétség) még egyezik
# darabonként a kihagyott versszavak legfeljebb ennyiszerese az idézett szavaknak (pl. „felfakadának [ezen a napon]
# a nagy mélység [minden] forrásai”); minden idézett szónak sorrendben egyeznie kell, ezért ez nem enged át parafrázist
IDEZET_KIHAGYAS = 1


def szo_egyezik(a, b):
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() >= IDEZET_SZO_HASONLOSAG


def karoli_egyezik(idez, karoli_normal):
    """Az idézet a Károli-vers szövege-e: minden „…”-tal elválasztott darabja a vers szavait sorrendben követi,
    szavanként tűréssel (a Károli régies helyesírása), a darab szószámával arányos kihagyással.
    A más igealak vagy más szó (kihirdetem ↔ kiáltom) saját fordítás."""
    vers = karoli_normal.split()
    for darab in re.split(r'\.\.\.|…|\[[^\]]*\]', idez):
        szavak = normal_szoveg(darab).split()
        if not szavak:
            continue
        keret = IDEZET_KIHAGYAS * len(szavak)
        if not any(illeszt(szavak, vers, 0, k, 0, keret) for k in range(len(vers))):
            return False
    return True


def illeszt(q, v, qi, vi, kihagy, keret):
    """A q[qi:] szavai a v[vi:]-ben sorrendben, összesen legfeljebb `keret` kihagyott versszóval."""
    if qi == len(q):
        return True
    if vi == len(v):
        return False
    if szo_egyezik(q[qi], v[vi]) and illeszt(q, v, qi + 1, vi + 1, kihagy, keret):
        return True
    return qi > 0 and kihagy < keret and illeszt(q, v, qi, vi + 1, kihagy + 1, keret)


def ell_idezet(sorok):
    ki = []
    for ige, _, karoli, proza in blokkok_1a(sorok):
        if not karoli:
            continue
        kn = normal_szoveg(karoli)
        for s in proza:
            if re.match(r'^Funkció\s*:', s.szoveg.strip()):
                continue
            for m in IDEZET_RX.finditer(s.szoveg):
                if m.group(1):  # zárójeles glossza egy héber szó után: nem versidézet
                    continue
                idez = m.group(2) or m.group(3)
                if len(normal_szoveg(idez).split()) < 3:
                    continue
                if karoli_egyezik(idez, kn):
                    continue
                if re.search(r'saját fordítás|sajat forditas|szó szerint:|ford\.\s*:', s.szoveg, re.I):
                    continue
                ki.append(talalat('IDEZET', BUKAS, s.n, '%s: „%s”' % (ige, idez),
                                  'az idézet nem a fölötte álló Károli-vers szövege, és nincs „saját fordítás” jelölés'))
    return ki


def elofordulas_szamok(sorok):
    """Az 1. tábla sorai: (összes, ÓSZ, ÚSZ)."""
    _, tabla = elso_tabla(sorok, '1. Előfordulások')
    _, _, usz = konyvek()
    ossz = len(tabla)
    u = 0
    for _, c in tabla:
        m = re.match(r'\[?((?:[1-5])?[^\s\]]+)\s', c[0])
        if m and m.group(1) in usz:
            u += 1
    return ossz, ossz - u, u


def lxx_osszesites(sorok):
    for s in sorok:
        if s.szakasz.startswith('3. LXX') and 'Összesítés:' in s.szoveg:
            return {k.strip(): int(v) for k, v in re.findall(r'([\wáéíóöőúüű -]+)=(\d+)', s.szoveg)}
    return None


def szam_ertek(szo):
    szo = szo.lower()
    if szo.isdigit():
        return int(szo)
    return SZAMNEV.get(szo)


def ell_kivonat(sorok):
    ossz, osz, usz = elofordulas_szamok(sorok)
    if not ossz:
        return []
    lxx = lxx_osszesites(sorok)
    ki = []
    szam = r'(\d+|%s)' % '|'.join(sorted((re.escape(k) for k in SZAMNEV), key=len, reverse=True))
    for s in sorok:
        if not s.szakasz.startswith('Kivonat') or s.fajta != 'proza' or s.nyers.rstrip().endswith('<!-- olvasói -->'):
            continue
        for mondat in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ„])', s.szoveg):
            lxx_m = re.search(r'Septuaginta|LXX|görög fordítás', mondat)
            for m in re.finditer(r'\b%s\s+(?:\S+\s+){0,2}?[\w-]*?%s' % (szam, SZAM_FONEV), mondat, re.I):
                n = szam_ertek(m.group(1))
                if n is None:
                    continue
                fonev = m.group(0).lower()
                # a testamentum: a darabszó saját jelzője, vagy a mondatban előtte álló utolsó testamentum-szó
                # csak a főnév („az Újszövetségben”); a jelzői „újszövetségi folytatás” nem szűkít
                elotte = re.findall(r'Újszövetség(?!i)|Ószövetség(?!i)', mondat[:m.start()])
                testamentum = 'ú' if 'újszövetségi' in fonev else 'ó' if 'ószövetségi' in fonev else \
                    (elotte[-1][0].lower() if elotte else '')
                if testamentum == 'ú':
                    vart, mi = usz, 'újszövetségi'
                elif testamentum == 'ó':
                    vart, mi = osz, 'ószövetségi'
                else:
                    vart, mi = ossz, 'összes'
                if lxx_m and lxx and n in lxx.values():
                    continue
                if n != vart and (testamentum or n not in (ossz, osz, usz)):
                    ki.append(talalat('KIVONAT_SZAM', FIGY, s.n, mondat[max(0, m.start() - 60):m.end() + 40],
                                      'a Kivonat „%s” darabszáma (%d) ≠ az 1. tábla %s helyeinek száma (%d)' % (
                                          m.group(0), n, mi, vart)))
            if lxx_m and lxx and lxx.get('kutatói azonosítás függőben') and re.search(
                    r'\bmind(?:három|két|en| a \w+)\b', mondat):
                ki.append(talalat('KIVONAT_SZAM', FIGY, s.n, mondat[:160],
                                  'a Kivonat minden LXX-helyről állít, de a 3. szakasz összesítője szerint %d hely '
                                  '„kutatói azonosítás függőben”' % lxx['kutatói azonosítás függőben']))
    return ki


KOLOFON_KOTELEZO = ('Kiadás', 'Próza modellje')
KOLOFON_NEM_URES = ('Státusz', 'Kereszthivatkozás-napló', 'Sablon-megfelelőség', 'Forrás-study')


def ell_kolofon(sorok):
    kol = [s for s in sorok if s.szakasz.startswith('Kolofon')]
    if not kol:
        return [talalat('KOLOFON', BUKAS, 0, '', 'a lapon nincs Kolofon')]
    mezok = {}
    for s in kol:
        if s.fajta == 'tabla':
            c = [x.strip() for x in s.szoveg.strip().strip('|').split('|')]
            if len(c) >= 2:
                mezok.setdefault(c[0], (s.n, c[1]))
    ki = []
    for k in KOLOFON_KOTELEZO:
        if k not in mezok:
            ki.append(talalat('KOLOFON', BUKAS, kol[0].n, '', 'a Kolofonban nincs „%s” sor' % k))
    if not any('Változásjegyzék' in s.szoveg for s in kol):
        ki.append(talalat('KOLOFON', BUKAS, kol[0].n, '', 'a Kolofonban nincs Változásjegyzék'))
    for k in KOLOFON_NEM_URES:
        if k in mezok and mezok[k][1].strip(' `') in ('', '—', '-'):
            ki.append(talalat('KOLOFON', BUKAS, mezok[k][0], '| %s | %s |' % (k, mezok[k][1]),
                              'üres törzsadat-mező: %s' % k))
    return ki


HIANYJEL_RX = re.compile(r'\*\((nincs [^)]*)\)\*|nincs a szakasztáblában')


def ell_hianyjel(sorok):
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'proveniencia') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        for m in HIANYJEL_RX.finditer(s.szoveg):
            ki.append(talalat('HIANYJEL', FIGY, s.n, kornyezet(s.szoveg, m, 30),
                              'belső hiányjelzés az olvasói szövegben: ' + m.group(0), m.group(0)))
            break
    return ki


SZINT_ALATT_RX = re.compile(r'ennél a motívumnál még nincs|nem futott|üres blokk|egyikéhez sincs rögzített indoklás|'
                            r'még nincs (?:ilyen|kapcsolat)', re.I)
SZINT_ARANY = 0.25      # a szakasz szószáma az arany lap azonos szakaszáénak ennyi része alatt: figyelmeztetés
SZINT_MIN_ARANY = 150   # csak az arany lapon legalább ennyi szavas szakaszokat mérjük
# csak az értelmező (kézi) és a kapcsolati szakaszokat: az 1., 1/b., 2–4. hossza az előfordulások számával arányos
SZINT_SZAKASZ = ('5. Kapcsolatok', '5/b.', '6. Értelmezés', '6/b.', '7. Módszertan')


def szakasz_szoszam(sorok):
    ki = {}
    for s in sorok:
        if s.fajta in ('proza', 'tabla', 'dolt', 'karoli', 'labjegyzet') and s.szakasz:
            kulcs = re.sub(r'\s*\*\(.*\)\*\s*$', '', s.szakasz)
            ki[kulcs] = ki.get(kulcs, 0) + len(s.szoveg.split())
    return ki


_ARANY_SZOSZAM = None


def ell_szint(sorok, arany_szoszam=None):
    ki = []
    for s in sorok:
        if s.olvasoi and SZINT_ALATT_RX.search(s.szoveg):
            m = SZINT_ALATT_RX.search(s.szoveg)
            ki.append(talalat('SZINT_ALATT', FIGY, s.n, kornyezet(s.szoveg, m), 'üres vagy hiányt jelző blokk'))
    if arany_szoszam:
        sajat = szakasz_szoszam(sorok)
        elso = {}
        for s in sorok:
            if s.fajta == 'cim' and s.szoveg.startswith('## '):
                elso.setdefault(re.sub(r'\s*\*\(.*\)\*\s*$', '', s.szakasz), s.n)
        for k, a in arany_szoszam.items():
            if a < SZINT_MIN_ARANY or not k.startswith(SZINT_SZAKASZ) or k not in elso:
                continue
            if sajat.get(k, 0) < SZINT_ARANY * a:
                ki.append(talalat('SZINT_ALATT', FIGY, elso[k], k, 'a szakasz %d szó, az arany lapon %d (< %d%%)' % (
                    sajat.get(k, 0), a, int(SZINT_ARANY * 100))))
    return ki


_KH_GYANUS = None


def ell_kh(sorok):
    global _KH_GYANUS
    if _KH_GYANUS is None:
        import karoli_kh_epseg as KH
        _KH_GYANUS = KH.gyanus_forrasok()
    _, step, _ = konyvek()
    ki, jelzett = [], set()
    for s in sorok:
        if not s.szakasz.startswith('4. Kereszthivatkoz') or not s.szoveg.strip().startswith('- Károli-KH'):
            continue
        m = re.match(r'(\S+)\s+(\d+):(\d+)', s.alszakasz)
        if not m or m.group(1) not in step:
            continue
        forras = '%s.%s.%s' % (step[m.group(1)], m.group(2), m.group(3))
        if forras in _KH_GYANUS and forras not in jelzett:
            jelzett.add(forras)
            ki.append(talalat('KH_MASOLT', FIGY, s.n, '%s → %s' % (s.alszakasz, s.szoveg.strip()[2:]),
                              'a Károli-KH lista feltehetően más vers másolata (azonos listájú: %s); javítás: N-F156a'
                              % ', '.join(_KH_GYANUS[forras][:3])))
    return ki


def ell_atvett(szoveg):
    """A párhuzamos szabályok (lábjegyzet: ellenoriz.py 24.; 1/a próza: proza_1a.py) — ha a main-en vannak."""
    ki, megj = [], []
    try:
        import ellenoriz as E
        f = getattr(E, 'lap_labjegyzet_hianyok', None)
    except Exception:  # noqa: BLE001
        f = None
    if f is None:
        megj.append('LABJEGYZET: az ellenoriz.lap_labjegyzet_hianyok még nincs a main-en (PR #595) — nem mérve')
    else:
        for k in f(szoveg):
            ki.append(talalat('LABJEGYZET', BUKAS, 0, '[^%s]' % k, 'definíció nélküli lábjegyzet'))
    try:
        import proza_1a as P
    except ImportError:
        P = None
    if P is None or not hasattr(P, 'meres'):
        megj.append('PROZA_1A: a proza_1a.py még nincs a main-en (PR #593) — nem mérve')
    else:
        for x in P.meres(szoveg):
            if not (x[1] == 'kerek' and x[2] == 'van'):
                ki.append(talalat('PROZA_1A', BUKAS, 0, x[0], '1/a: próza %s, Funkció %s' % (x[1], x[2])))
    return ki, megj


ELLENORZESEK = [ell_belso, ell_pont, ell_angol, ell_idezojel, ell_atiras, ell_konyv, ell_bdb, ell_funkcio,
                ell_idezet, ell_kivonat, ell_kolofon, ell_hianyjel, ell_kh]


def arany_szoszam():
    global _ARANY_SZOSZAM
    if _ARANY_SZOSZAM is None:
        ut = os.path.join(GYOKER, 'lexikon', ARANY + '_TUDOMANYOS.md')
        if os.path.exists(ut):
            with open(ut, encoding='utf-8') as f:
                _ARANY_SZOSZAM = szakasz_szoszam(tagol(f.read()))
        else:
            _ARANY_SZOSZAM = {}
    return _ARANY_SZOSZAM


def lap_meres(szoveg, kh=True, atvett=True, arany=True):
    """Egy lap szövegének mérése: (találatok, megjegyzések)."""
    sorok = tagol(szoveg)
    ki = []
    for f in ELLENORZESEK:
        if f is ell_kh and not kh:
            continue
        ki += f(sorok)
    ki += ell_szint(sorok, arany_szoszam() if arany else None)
    megj = []
    if atvett:
        a, megj = ell_atvett(szoveg)
        ki += a
    return csoportosit(ki, sorok), megj


LEXIKON_KONYVTAR = os.path.join(GYOKER, 'lexikon')


def motivum_meres(mid):
    ut = os.path.join(LEXIKON_KONYVTAR, mid + '_TUDOMANYOS.md')
    if not os.path.exists(ut):
        return None, ['nincs lexikon/%s_TUDOMANYOS.md' % mid]
    with open(ut, encoding='utf-8') as f:
        return lap_meres(f.read())


def osszesit(talalatok):
    """{azonosító: {BUKÁS: n, FIGYELMEZTETÉS: n}} és a két összeg."""
    by = {}
    for t in talalatok:
        by.setdefault(t['azonosito'], {BUKAS: 0, FIGY: 0})[t['sulyossag']] += 1
    return by, sum(1 for t in talalatok if t['sulyossag'] == BUKAS), sum(1 for t in talalatok if t['sulyossag'] == FIGY)


def main():
    ap = argparse.ArgumentParser(description='Gépi olvasói kapu egy lexikonlapon')
    ap.add_argument('id', nargs='*')
    ap.add_argument('--osszes', action='store_true', help='minden lexikon/*_TUDOMANYOS.md')
    ap.add_argument('--reszletes', action='store_true', help='minden találat soronként')
    ap.add_argument('--json', help='a teljes kimenet JSON-fájlba')
    ap.add_argument('--lexikon-konyvtar', help='a lapok könyvtára (alapból lexikon/; pl. egy --kimenet próba lexikon/ mappája)')
    ap.add_argument('--markdown', help='motívumonkénti javítandó lista Markdown-fájlba (generált napló)')
    a = ap.parse_args()
    global LEXIKON_KONYVTAR
    if a.lexikon_konyvtar:
        LEXIKON_KONYVTAR = os.path.abspath(a.lexikon_konyvtar)
    ids = a.id
    if a.osszes:
        ids = sorted(n[:-len('_TUDOMANYOS.md')] for n in os.listdir(LEXIKON_KONYVTAR)
                     if n.endswith('_TUDOMANYOS.md'))
    if not ids:
        ap.error('adj meg motívum-ID-t vagy --osszes')
    ossz, buk_ossz = {}, 0
    for mid in ids:
        tal, megj = motivum_meres(mid)
        if tal is None:
            print('## %s: %s' % (mid, megj[0]))
            continue
        by, b, fi = osszesit(tal)
        buk_ossz += b
        ossz[mid] = {'bukas': b, 'figyelmeztetes': fi, 'kapunkent': by, 'megjegyzes': megj, 'talalatok': tal}
        print('## %s: %d BUKÁS, %d FIGYELMEZTETÉS' % (mid, b, fi))
        for k in sorted(by):
            print('   %-13s BUKÁS %3d · FIGY %3d' % (k, by[k][BUKAS], by[k][FIGY]))
        for x in megj:
            print('   (%s)' % x)
        if a.reszletes:
            for t in tal:
                print('   %5s %-13s %-14s %s — %s' % (t['sor'], t['azonosito'], t['sulyossag'], t['uzenet'], t['idezet']))
        print()
    if a.json:
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(ossz, f, ensure_ascii=False, indent=1)
    if a.markdown:
        with open(a.markdown, 'w', encoding='utf-8', newline='\n') as f:
            f.write(markdown(ossz))
    return 1 if buk_ossz else 0


def cella(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ')


def markdown(ossz):
    """A mérés generált naplója: összesítő és motívumonként a javítandó lista."""
    ki = ['# GENERÁLT: eszkozok/olvasoi_kapu.py --markdown — kézzel szerkeszteni tilos', '',
          '# Olvasói kapu — mérés a lexikonlapokon', '',
          '*scope=lexikon/*_TUDOMANYOS.md | forras=eszkozok/olvasoi_kapu.py | ts=%s*' % os.environ.get(
              'PARDES_DATUM', 'futáskor'), '',
          'Egy tétel = egy hiba egy szakaszban; a `db` az ismétlődések száma (pl. ugyanaz a belső jel egy tábla '
          'több sorában). A sorszám a lap Markdown-sora.', '',
          '| Motívum | BUKÁS | FIGYELMEZTETÉS | Kapunként (B/F) |', '|---|---|---|---|']
    for mid, d in ossz.items():
        ki.append('| %s | %d | %d | %s |' % (mid, d['bukas'], d['figyelmeztetes'], ', '.join(
            '%s %d/%d' % (k, v[BUKAS], v[FIGY]) for k, v in sorted(d['kapunkent'].items()))))
    for mid, d in ossz.items():
        ki += ['', '## %s — %d BUKÁS, %d FIGYELMEZTETÉS' % (mid, d['bukas'], d['figyelmeztetes']), '']
        for m in d['megjegyzes']:
            ki.append('*%s*' % m)
        ki += ['', '| Sor | Ellenőrzés | Súlyosság | db | Mi a hiba | Idézet |', '|---|---|---|---|---|---|']
        for t in sorted(d['talalatok'], key=lambda x: (x['sulyossag'] != BUKAS, x['sor'])):
            ki.append('| %s | %s | %s | %d | %s | %s |' % (t['sor'], t['azonosito'], t['sulyossag'], t['db'],
                                                          cella(t['uzenet']), cella(t['idezet'])))
    return '\n'.join(ki) + '\n'


if __name__ == '__main__':
    sys.exit(main())
