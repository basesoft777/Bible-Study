#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nyilt_mag_export.py -- a nyílt tudományos mag (CC BY 4.0) generált exportja (F162, FELADATOK #162).

Nem a belső táblák másolata, hanem az adatból generált nézet egy kutató olvasónak (a lap elvével azonosan):
a belső jelek (`gerinc_elem`, `scope=… | forras=… | ts=…`, DT/N/F-hivatkozás, `manual`, belső fájlnév) érthető
oszlopokra, feloldott döntésekre és kódkönyv-mondatokra képződnek le. A kimenet: `nyilt_mag/` (determinisztikus,
rendezett, újrafuttatva bájtazonos).

Leképezés (a F162 brief 2. pontja, a #86 terv 1.5):
    gerinc_elem            -> horgony_tipus + horgony (érthető érték)
    proveniencia-sor       -> lekerdezes_tipusa, forras_megnevezes, forras_dataset, forras_licenc, datum
    manual                 -> „kézi döntés, lekérdezés nélkül”
    DT-hivatkozás          -> nyilvános döntés-azonosító (NYD-nnn) + a `dontesnaplo.tsv` egymondatos szövege
    elutasítási indok      -> szöveges ok (`adat/elutasitasi_okok.tsv`)
    belső fájlnév, zsargon -> elhagyva vagy lefordítva

Licencszűrés (`adat/licencek.tsv`): kizárva a nem kereskedelmi, a GPL-es, a tisztázatlan és a nem szabad
(„minden jog fenntartva”, © Mounce) forrás; a CC BY-SA 4.0 SDBH/SDGNT-domének külön rétegben
(`nyilt_mag/cc_by_sa_reteg/`), attribúcióval.

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (nem `csv`).

Használat:
    python eszkozok/nyilt_mag_export.py [--kimenet nyilt_mag]
"""
import argparse
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEJLEC = ('# GENERÁLT: a PaRDeS nyílt mag exportja (CC BY 4.0), a projekt adataiból generálva — kézzel nem '
          'szerkesztendő; a „#” kezdetű sor megjegyzés.')
KOD_FEJLEC = FEJLEC
FEJLEC_EN = ('# GENERATED: export of the PaRDeS open core (CC BY 4.0), generated from the project data — do not '
             'edit by hand; a line starting with "#" is a comment.')

# --- a licencszűrés
ENGEDETT_CIMKE = {'közkincs', 'CC0 1.0', 'CC BY 4.0'}
SA_CIMKE = 'CC BY-SA 4.0'
SA_RETEG = ('SDBH', 'SDGNT')           # a külön rétegbe kerülő SA-források
SAJAT_SOR = 'projekt_adat'
KIZARAS_OKA = [
    (re.compile(r'GPL', re.I), 'GPL licenc: nem építhető be nyílt (CC BY) csomagba'),
]

KH_JELENTES = 'naplok/KAROLI_KH_EPSEG_jelentes.md'

# a zárt értékkészletű oszlopok (egyetlen helyen; a kapu innen veszi): minden értéküknek van kódkönyv-sora, és az
# export mellettük `<oszlop>_en` oszlopot ad a kódkönyv `cimke_en` mezőjéből (F170.2, DT-F170a). A `;`-vel összetett
# érték részenként címkéződik.
ZART = {
    'motivumok.tsv': ['pardes_szint', 'statusz', 'feldolgozasi_allapot', 'azonossag_tipusa'],
    'elofordulasok.tsv': ['pardes_szint', 'horgony_tipus', 'szotar', 'azonositas_modja', 'megbizhatosag',
                          'igazolas', 'lekerdezes_tipusa', 'forras_megnevezes', 'forras_licenc'],
    'kizarasok.tsv': ['jelolt_tipus', 'kizaras_oka', 'keresesi_mod', 'azonositas_modja', 'megbizhatosag'],
    'beepitesi_dontesek.tsv': ['jelolt_tipus', 'keresesi_mod'],
    'kapcsolatok.tsv': ['tipus', 'bizonyossag', 'pardes_szint', 'lekerdezes_tipusa', 'forras_megnevezes'],
    'motivum_kapcsolatok.tsv': ['tipus', 'bizonyossag', 'pardes_szint', 'lekerdezes_tipusa', 'forras_megnevezes'],
    'forrasok_es_licencek.tsv': ['licenc', 'szerepe_a_csomagban', 'ok'],
    'cc_by_sa_reteg/szemantikai_domenek.tsv': ['szotar'],
}


def ertek_reszek(ertek):
    return [x.strip() for x in (ertek or '').split(';') if x.strip()]


_CIMKE = None


def cimkek():
    """{(tábla, oszlop, érték): cimke_en} a kódkönyvből (`adat/nyilt_kodkonyv.tsv`)."""
    global _CIMKE
    if _CIMKE is None:
        _, kk = tsv('adat/nyilt_kodkonyv.tsv')
        _CIMKE = {(s['tabla'], s['oszlop'], s['ertek']): s.get('cimke_en', '').strip() for s in kk if s['ertek']}
    return _CIMKE


CIMKE_HIANY = []


def cimke_bovit(tabla, fej, sorok):
    """Minden zárt oszlop után a párja (`<oszlop>_en`): a kódkönyv rövid angol címkéje. Hiányzó címke: a hiány a
    `CIMKE_HIANY`-ba kerül (az export a végén megáll), nem üres érték és nem találgatás."""
    zart = ZART.get(tabla, [])
    uj = []
    for o in fej:
        uj.append(o)
        if o in zart:
            uj.append(o + '_en')
    for s in sorok:
        for o in zart:
            if o not in fej:
                continue
            en = []
            for r in ertek_reszek(s.get(o, '')):
                c = cimkek().get((tabla, o, r), '')
                if not c:
                    CIMKE_HIANY.append((tabla, o, r))
                en.append(c)
            s[o + '_en'] = '; '.join(en)
    return uj, sorok


# --- szabad szöveg angol párja (F170.3–4): a gépi fordítás tárolva az `adat/nyilt_angol.tsv`-ben (forrásréteg), az
# export csak kiolvassa. Kulcs: tábla + oszlop + sorkulcs; a fordítás csak akkor kerül a csomagba, ha a tárolt
# forrás-hash a mai magyar cella hash-e (különben a magyar forrás újabb: a fordítás elavult, a kapu bukik).
SZABAD = {
    'motivumok.tsv': ['cim', 'rovid_cimke', 'tema', 'negativ_kriterium', 'folerendelt_fogalom'],
    'elofordulasok.tsv': ['funkcio'],
    'kizarasok.tsv': ['indoklas', 'korabbi_minosites'],
    'beepitesi_dontesek.tsv': ['indoklas', 'korabbi_minosites'],
    'dontesnaplo.tsv': ['kerdes', 'dontes'],
}
SORKULCS = {
    'motivumok.tsv': ['motivum_azonosito'],
    'elofordulasok.tsv': ['motivum_azonosito', 'igehely', 'horgony'],
    'kizarasok.tsv': ['motivum_azonosito', 'igehely', 'cel_motivum', 'cel_igehely'],
    'beepitesi_dontesek.tsv': ['motivum_azonosito', 'igehely', 'cel_motivum', 'cel_igehely'],
    'dontesnaplo.tsv': ['dontes_azonosito'],
}
ANGOL_TABLA = 'adat/nyilt_angol.tsv'
ANGOL_FEJ = ['tabla', 'oszlop', 'sorkulcs', 'forras_hash', 'forras_hu', 'angol', 'modell', 'datum']
FORDITAS_NINCS = 'nincs fordítás'


def szoveg_hash(t):
    return hashlib.sha256((t or '').encode('utf-8')).hexdigest()[:16]


def sorkulcs(tabla, s):
    return ' | '.join(s.get(k, '') for k in SORKULCS[tabla])


_ANGOL = None


def angol_tar():
    """{(tábla, oszlop, sorkulcs): sor} az `adat/nyilt_angol.tsv`-ből (üres, ha a tábla még nincs)."""
    global _ANGOL
    if _ANGOL is None:
        _ANGOL = {}
        if os.path.exists(os.path.join(GYOKER, ANGOL_TABLA)):
            _, sorok = tsv(ANGOL_TABLA)
            for s in sorok:
                _ANGOL[(s['tabla'], s['oszlop'], s['sorkulcs'])] = s
    return _ANGOL


def angol_bovit(tabla, fej, sorok):
    """Minden szabad szöveges oszlop után a párja (`<oszlop>_en`), a sor végén a `forditas_modja`. A fordítás csak
    egyező forrás-hash-sel kerül be; hiányzó vagy elavult fordításnál a cella üres, és a `forditas_modja` kimondja."""
    mezok = [o for o in SZABAD.get(tabla, []) if o in fej]
    uj = []
    for o in fej:
        uj.append(o)
        if o in mezok:
            uj.append(o + '_en')
    uj.append('forditas_modja')
    latott = set()
    for s in sorok:
        k = sorkulcs(tabla, s)
        if k in latott:
            raise SystemExit('angol réteg: a sorkulcs nem egyedi: %s %s' % (tabla, k))
        latott.add(k)
        modellek, hiany, van = set(), 0, 0
        for o in mezok:
            hu = s.get(o, '')
            s[o + '_en'] = ''
            if not hu:
                continue
            van += 1
            t = angol_tar().get((tabla, o, k))
            if t and t['forras_hash'] == szoveg_hash(hu) and t['angol']:
                s[o + '_en'] = t['angol']
                modellek.add(t['modell'])
            else:
                hiany += 1
        if not van:
            s['forditas_modja'] = ''
        elif not modellek:
            s['forditas_modja'] = FORDITAS_NINCS
        else:
            s['forditas_modja'] = ('gépi fordítás (%s)' % ', '.join(sorted(modellek)) +
                                   ('; részben hiányzik' if hiany else ''))
    return uj, sorok


def szabad_cellak(fajlok):
    """[(tábla, oszlop, sorkulcs, magyar szöveg, angol cella)] a generált csomag nem üres szabad szöveges celláiból."""
    ki = []
    for tabla, mezok in sorted(SZABAD.items()):
        _, ds = tsv_szoveg(fajlok[tabla])
        for d in ds:
            for o in mezok:
                if d.get(o):
                    ki.append((tabla, o, sorkulcs(tabla, d), d[o], d.get(o + '_en', '')))
    return ki


# --- angol szófogódzó (F170, a brief 5. pontja): a Strong-szám STEPBible-glosszája (TBESH/TBESG, CC BY 4.0)
GLOSSZA_FORRAS = ('TBESH', 'TBESG')
_GLOSSZA = None


def strong_glossza():
    """{Strong-szám: glossza} a TBESH/TBESG-ből. A Strong-szám (és betűs alváltozatai, pl. H1121a/H1121b) fő
    bejegyzéseinek glosszája (a `H1121A =` és a `H0430G = a Name of` alakú sorok; a „= a Meaning of / Spelling of / Part of” sorok
    kimaradnak), fájlsorrendben, ismétlés nélkül, ` / `-rel fűzve. A csomag Strong-száma betű nélküli, ezért a
    glossza a szám egészére szól, nem jelentés-specifikus (pl. H7497: `Rapha / Rephaim`)."""
    global _GLOSSZA
    if _GLOSSZA is None:
        gy = {}
        for fn in ('konkordancia/TBESH.txt', 'konkordancia/TBESG.txt'):
            with open(os.path.join(GYOKER, fn), encoding='utf-8') as f:
                for s in f:
                    m = s.rstrip('\n').split('\t')
                    if len(m) < 7 or not re.match(r'^[HG]\d{4}[a-z]?$', m[0]):
                        continue
                    if not re.match(r'^[HG]\d{4}[A-Z]? =(?: a Name of)?$', m[1].strip()) or not m[6].strip():
                        continue
                    lista = gy.setdefault(m[0][:5], [])
                    if m[6].strip() not in lista:
                        lista.append(m[6].strip())
        _GLOSSZA = {k: ' / '.join(v) for k, v in gy.items()}
    return _GLOSSZA


def glossza_en(strong):
    """`H7121+H8034` -> `to call: call to + name`; ismeretlen Strong-számnál a rész üres marad (nincs kitöltés)."""
    szamok = [x.strip() for x in (strong or '').split('+') if x.strip()]
    if not szamok:
        return ''
    return ' + '.join(strong_glossza().get(x, '') for x in szamok)

# a nyílt adatmag és a lexikon viszonya (F167.3.8; a felhasználó jóváhagyott sémája, 2026-11-04)
ADATMAG_LEXIKON_HU = ('A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező'
                      ' szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva.')
ADATMAG_LEXIKON_EN = ('The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the '
                      'Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved.')


# ----------------------------------------------------------------------------- olvasás

def tsv(rel):
    """Fejléces TSV: (fejléc, [dict]); a `#` kezdetű és üres sorok kimaradnak; `split('\\t')`."""
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = []
    for s in sorok[1:]:
        m = s.split('\t')
        ki.append(dict(zip(fej, m + [''] * (len(fej) - len(m)))))
    return fej, ki


def olvas(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        return f.read()


# ----------------------------------------------------------------------------- döntések

DT_RX = re.compile(r'DT-?F?\d+[a-z]?')
FAJL_RX = re.compile(r'`?(?:[\w.-]+/)*[\w.-]+\.(?:md|tsv|py|json|txt)`?')


def dontesek_beolvas():
    """DONTESEK.md -> {DT-azonosító: {'kerdes':…, 'dontes':…}}. A sor cellái ` | `-vel válnak; az Állapot-cella
    az első 🟡/🟢/✅ kezdetű cella a 4. indextől, a Döntés a rá következő (egyes soroknál az Opciók cellájában
    ` | ` áll, ezért a helyet az Állapot-cella adja)."""
    ki = {}
    for s in olvas('DONTESEK.md').split('\n'):
        m = re.match(r'\| (DT-?F?\d+[a-z]?) \| ', s)
        if not m:
            continue
        c = [x.strip() for x in s.strip().strip('|').split(' | ')]
        i = next((k for k in range(4, len(c)) if c[k][:1] in ('🟡', '🟢', '✅')), None)
        if i is None or i + 1 >= len(c):
            continue
        ki[m.group(1)] = {'kerdes': c[2], 'dontes': c[i + 1]}
    return ki


class Dontesnaplo:
    """Nyilvános döntés-azonosítók (NYD-nnn). A számozás a DT-szám szerint rendezett, tehát determinisztikus."""

    def __init__(self, forras):
        self.forras = forras
        self.hivatkozott = set()
        self.azon = {}

    def gyujt(self, szoveg):
        for m in DT_RX.finditer(szoveg or ''):
            self.hivatkozott.add(m.group(0))

    def kioszt(self):
        def kulcs(d):
            n = re.search(r'\d+', d)
            return (0 if d[2:3].isdigit() else 1, int(n.group(0)), d)
        ok = [d for d in self.hivatkozott if d in self.forras]
        for i, d in enumerate(sorted(ok, key=kulcs), 1):
            self.azon[d] = 'NYD-%03d' % i

    def feloldott(self, dt):
        return self.azon.get(dt, '')

    def csere(self, szoveg):
        """A szövegbeli DT-hivatkozás (és az utána álló „K4” alpont-jel) a nyilvános azonosítóra cserélődik; a
        feloldatlan hivatkozás egyszerűen elmarad."""
        def f(m):
            return self.azon.get(m.group(1), '')
        szoveg = re.sub(r'(DT-?F?\d+[a-z]?)(?: K\d)?', f, szoveg)
        szoveg = re.sub(r'\(\s*(?:,\s*)*\)', '', szoveg)
        szoveg = re.sub(r'\s*\(\s*([^()]*?)\s*[,;]\s*\)', r' (\1)', szoveg)
        szoveg = re.sub(r'\(\s*[,;]\s*', '(', szoveg)
        return szoveg


# ----------------------------------------------------------------------------- szöveg-tisztítás

CSERE_SZAVAK = [
    (re.compile(r'\baz orkesztrátoron\b'), 'a szerkesztőn'),
    (re.compile(r'\baz orkesztrátor\b'), 'a szerkesztő'),
    (re.compile(r'\b[Oo]rkesztrátor\w*'), 'szerkesztő'),
    (re.compile(r'(?<![\w&/])#\d{2,3}\b'), 'munkatétel'),
    (re.compile(r'(?<![\w/.#-])F\d{1,3}(?:\.\d+)?\b'), 'munkatétel'),
    (re.compile(r'(?<![\w-])N-F\d+[a-z]?\b|(?<![\w-])N\d{1,3}\b'), 'nyitott tétel'),
    (re.compile(r'\bscan\w*', re.I), 'keresés'),
    (re.compile(r'\bstudy\b', re.I), 'tanulmány'),
    (re.compile(r'\bsession\w*', re.I), 'munkamenet'),
    (re.compile(r'\bgerinc-pár', re.I), 'szóbázis-pár'),
    (re.compile(r'\bgerinc', re.I), 'szóbázis'),
    (re.compile(r'\bmanual\b'), 'kézi döntés'),
]


BELSO_KOD_RX = re.compile(r'\b[a-zA-Z]+(?:_[a-zA-Z0-9]+)+(?:=\S+)?')


def fajl_szo(m):
    """A fájlnév olvasói főnévre cserélődik (a név maga belső jel)."""
    s = m.group(0).strip('`')
    if s.endswith('.tsv') or s.endswith('.json'):
        return 'adattábla'
    if s.endswith('.py'):
        return 'szkript'
    return 'dokumentum'


_STEP_HU = None


def step_hu():
    global _STEP_HU
    if _STEP_HU is None:
        _, sorok = tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
        _STEP_HU = {s['STEPBible-rövidítés']: s['Magyar rövidítés'] for s in sorok}
    return _STEP_HU


STEP_REF = re.compile(r'\b([1-3]?[A-Z][a-z]{1,3})\.(\d+)\.(\d+)\b')

# --- OSIS-igehelykulcs (F170.1): magyar rövidítés -> STEPBible-rövidítés (a normalizáló tábla) -> OSIS-könyvkód.
# A STEPBible-rövidítés nem OSIS (Exo/Exod, 1Ki/1Kgs, Ezk/Ezek …), ezért a 66 kanonikus könyv OSIS 2.1.1 kódja
# rögzített tábla. A fejezet- és versszám a Károli-számozás (a magyar `igehely` számai, átkulcsolás nélkül).
STEP_OSIS = {
    'Gen': 'Gen', 'Exo': 'Exod', 'Lev': 'Lev', 'Num': 'Num', 'Deu': 'Deut', 'Jos': 'Josh', 'Jdg': 'Judg',
    'Rut': 'Ruth', '1Sa': '1Sam', '2Sa': '2Sam', '1Ki': '1Kgs', '2Ki': '2Kgs', '1Ch': '1Chr', '2Ch': '2Chr',
    'Ezr': 'Ezra', 'Neh': 'Neh', 'Est': 'Esth', 'Job': 'Job', 'Psa': 'Ps', 'Pro': 'Prov', 'Ecc': 'Eccl',
    'Sng': 'Song', 'Isa': 'Isa', 'Jer': 'Jer', 'Lam': 'Lam', 'Ezk': 'Ezek', 'Dan': 'Dan', 'Hos': 'Hos',
    'Jol': 'Joel', 'Amo': 'Amos', 'Oba': 'Obad', 'Jon': 'Jonah', 'Mic': 'Mic', 'Nam': 'Nah', 'Hab': 'Hab',
    'Zep': 'Zeph', 'Hag': 'Hag', 'Zec': 'Zech', 'Mal': 'Mal',
    'Mat': 'Matt', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John', 'Act': 'Acts', 'Rom': 'Rom', '1Co': '1Cor',
    '2Co': '2Cor', 'Gal': 'Gal', 'Eph': 'Eph', 'Php': 'Phil', 'Col': 'Col', '1Th': '1Thess', '2Th': '2Thess',
    '1Ti': '1Tim', '2Ti': '2Tim', 'Tit': 'Titus', 'Phm': 'Phlm', 'Heb': 'Heb', 'Jas': 'Jas', '1Pe': '1Pet',
    '2Pe': '2Pet', '1Jn': '1John', '2Jn': '2John', '3Jn': '3John', 'Jud': 'Jude', 'Rev': 'Rev'}
OSIS_KONYVEK = frozenset(STEP_OSIS.values())
# a magyar könyvnév forrásbeli változata -> a normalizáló tábla rövidítése. A TAHOT (és a belőle képzett F123
# blokk-listák) a Jeremiás siralmait `Sir`-nek írja; ugyanez az alias: bdb_konyv_javit.TAHOT_KONYV.
KONYV_ALIAS = {'Sir': 'JSir'}
IGEHELY_OSZLOPOK = ('igehely', 'cel_igehely', 'forras_igehely', 'igehely_a', 'igehely_b', 'csoport_sor_igehely')
IGEHELY_RX = re.compile(r'^(\S+) (\d+):(\d+)(?:[-–](\d+))?$')
OSIS_RX = re.compile(r'^[1-3]?[A-Z][A-Za-z]+\.\d+\.\d+(?:-[1-3]?[A-Z][A-Za-z]+\.\d+\.\d+)?$')

_HU_OSIS = None


def hu_osis():
    global _HU_OSIS
    if _HU_OSIS is None:
        _, sorok = tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
        _HU_OSIS = {}
        for s in sorok:
            step = s['STEPBible-rövidítés']
            if step not in STEP_OSIS:
                raise SystemExit('OSIS: a normalizáló tábla %r rövidítésének nincs OSIS-kódja' % step)
            _HU_OSIS[s['Magyar rövidítés']] = STEP_OSIS[step]
    return _HU_OSIS


def igehely_normal(ig):
    """A forrásbeli könyvnév-változat (`Sir`) a csomag egységes magyar rövidítésére (`JSir`)."""
    m = re.match(r'^(\S+)( .*)$', ig or '')
    if m and m.group(1) in KONYV_ALIAS:
        return KONYV_ALIAS[m.group(1)] + m.group(2)
    return ig


def osis(ig):
    """Magyar igehely (`1Kir 13:31`, `1Móz 4:10-11`, `ApCsel 2:27; ApCsel 2:31`) -> OSIS (`1Kgs.13.31`,
    `Gen.4.10-Gen.4.11`, `Acts.2.27 Acts.2.31`). Üres -> üres. Leképezhetetlen könyvnév vagy alak -> megáll
    (nem üres érték, nem találgatás)."""
    if not ig:
        return ''
    ki = []
    for resz in [x.strip() for x in ig.split(';')]:
        m = IGEHELY_RX.match(igehely_normal(resz))
        if not m:
            raise SystemExit('OSIS: nem leképezhető igehely-alak: %r' % ig)
        kod = hu_osis().get(m.group(1))
        if kod is None:
            raise SystemExit('OSIS: leképezhetetlen könyvnév: %r (%r)' % (m.group(1), ig))
        k = '%s.%s.%s' % (kod, m.group(2), m.group(3))
        if m.group(4):
            k += '-%s.%s.%s' % (kod, m.group(2), m.group(4))
        ki.append(k)
    return ' '.join(ki)


def osis_bovit(fej, sorok):
    """Minden igehely-oszlop után a párja (`<oszlop>_osis`); a magyar igehely könyvnevét egységesíti."""
    uj = []
    for o in fej:
        uj.append(o)
        if o in IGEHELY_OSZLOPOK:
            uj.append(o + '_osis')
    for s in sorok:
        for o in fej:
            if o in IGEHELY_OSZLOPOK:
                s[o] = '; '.join(igehely_normal(x.strip()) for x in s.get(o, '').split(';')) if s.get(o) else ''
                s[o + '_osis'] = osis(s[o])
    return uj, sorok


def step_atiras(t):
    def f(m):
        hu = step_hu().get(m.group(1))
        return '%s %s:%s' % (hu, m.group(2), m.group(3)) if hu else m.group(0)
    return STEP_REF.sub(f, t)


def tisztit(szoveg, dn):
    """Belső jelek eltávolítása/lefordítása az olvasói szövegben. A feloldott döntés a nyilvános azonosítóra
    cserélődik; fájlnév és munkazsargon elmarad vagy olvasói szóra cserélődik."""
    if not szoveg:
        return ''
    t = szoveg
    t = dn.csere(t)
    t = t.replace('**', '')
    t = step_atiras(t)
    t = FAJL_RX.sub(fajl_szo, t)
    t = t.replace('`', '')
    t = BELSO_KOD_RX.sub('', t)
    for rx, ujra in CSERE_SZAVAK:
        t = rx.sub(ujra, t)
    t = re.sub(r'\b(adattábla|dokumentum|szkript)\b(?:\s*[,;]?\s*\b\1\b)+', r'\1', t)
    t = re.sub(r'\s+([,.;:)])', r'\1', t)
    t = re.sub(r'\s{2,}', ' ', t).strip()
    return t


def egy_mondat(szoveg, ig=380, min_hossz=90):
    """Az első mondat(ok), legfeljebb `ig` karakter, mondathatáron vágva."""
    t = re.sub(r'\s+', ' ', szoveg or '').strip()
    if len(t) <= ig:
        return t
    vag = t[:ig]
    k = max(vag.rfind('. '), vag.rfind('; '))
    if k >= min_hossz:
        return vag[:k + 1].rstrip(';').rstrip()
    k = vag.rfind(' ')
    return vag[:k].rstrip(',;:') + ' …'


# ----------------------------------------------------------------------------- proveniencia, licenc

PROV_KULCS = re.compile(r'(?:^|\s\|\s)(scope|forras|ts|strong|n|szo)=')


def prov_parse(s):
    """`scope=… | forras=… | ts=…` -> dict. A kulcs-ismétlés (szabad szöveg `|`-ral) nem veszélyes: az első kulcs-
    találat dönt; az értéket a következő ` | kulcs=` jelig vesszük."""
    ki = {}
    poz = [(m.start(), m.group(1), m.end()) for m in PROV_KULCS.finditer(s or '')]
    for i, (_, k, vege) in enumerate(poz):
        kov = poz[i + 1][0] if i + 1 < len(poz) else len(s)
        ki.setdefault(k, s[vege:kov].strip())
    return ki


class Licenc:
    def __init__(self):
        _, sorok = tsv('adat/licencek.tsv')
        self.sor = {s['dataset']: s for s in sorok}
        _, dsor = tsv('adat/datasetek.tsv')
        self.fajl_dataset = {}
        for d in dsor:
            for f in re.split(r'[,;]\s*', d['fajl']):
                b = os.path.basename(f.strip())
                if b:
                    self.fajl_dataset.setdefault(b, d['dataset'])
        # a kézi tábla- és fájlnév-aliasok, ahol a forrásnév nem a datasetek.tsv `fajl` alakja
        for alias, ds in (('TAHOT_kivonat.tsv', 'TAHOT'), ('TAGNT_kivonat.tsv', 'TAGNT'),
                          ('Karoli_1908.tsv', 'Karoli_1908'), ('BSB_Strongs.tsv', 'BSB_Strongs'),
                          ('TSK', 'TSK'), ('LXX_OS', 'LXX_OS')):
            self.fajl_dataset.setdefault(alias, ds)

    def cimke(self, ds):
        return self.sor[ds]['cimke'] if ds in self.sor else 'tisztázatlan'

    def allapot(self, ds):
        """('engedett' | 'sa_reteg' | 'sajat' | 'kizart', ok)"""
        if ds == SAJAT_SOR:
            return 'sajat', 'a projekt saját adata; a nyílt mag licence CC BY 4.0 (a jogtulajdonos döntése)'
        s = self.sor.get(ds)
        if s is None:
            return 'kizart', 'nincs sora a licenc-leltárban (tisztázatlan)'
        for rx, ok in KIZARAS_OKA:
            if rx.search(s['licenc']):
                return 'kizart', ok
        if s['allapot'] == 'tisztazatlan' or s['cimke'] == 'tisztázatlan':
            return 'kizart', 'tisztázatlan licenc'
        if s['cimke'] == 'minden jog fenntartva':
            return 'kizart', 'a projekt zárt (fizetős) származtatott rétege; nem része a nyílt magnak'
        if s['kereskedelmi'] != 'igen':
            return 'kizart', ('a kereskedelmi használat nem szabad (%s: %s)' % (s['kereskedelmi'], s['cimke']))
        if s['cimke'] == SA_CIMKE:
            if ds in SA_RETEG:
                return 'sa_reteg', 'CC BY-SA 4.0: külön rétegben, attribúcióval, nem zárható'
            return 'kizart', 'CC BY-SA 4.0, de a csomag nem használja (nem kerül bele)'
        if s['cimke'] in ENGEDETT_CIMKE:
            return 'engedett', ''
        return 'kizart', 'ismeretlen licenc-címke (%s)' % s['cimke']


FORRAS_OSZTALY = [
    (re.compile(r'_tematikus\.md$'), 'a motívum kézi tematikus tanulmánya'),
    (re.compile(r'_kereszthivatkozas_naplo\.md$|_naplo\.md$'), 'a kézi kereszthivatkozás-napló'),
]


def forras_tokenek(forras):
    """A `forras=` érték tokenjei (`+`, `,` és ` + ` mentén)."""
    return [t.strip() for t in re.split(r'\s*\+\s*|,\s*(?=[\w./]+\.(?:tsv|md|py))', forras or '') if t.strip()]


def forras_fordit(forras, lic):
    """(megnevezés, [dataset], [kizárt dataset]) -- a belső fájlnév helyett olvasói megnevezés."""
    nevek, dsek, kizartak = [], [], []
    for t in forras_tokenek(forras):
        t0 = re.sub(r'\s*\(.*$', '', t).strip()
        b = os.path.basename(t0)
        if b in lic.fajl_dataset or t0 in lic.fajl_dataset:
            ds = lic.fajl_dataset.get(b) or lic.fajl_dataset[t0]
            st, _ = lic.allapot(ds)
            if st == 'kizart':
                kizartak.append(ds)
                nevek.append('kizárt licencű forrás (nem része a csomagnak)')
            else:
                dsek.append(ds)
                nevek.append('%s (%s)' % (ds, lic.cimke(ds)))
            continue
        for rx, nev in FORRAS_OSZTALY:
            if rx.search(b):
                nevek.append(nev)
                break
        else:
            if b.endswith(('.py', '.tsv', '.md')) or 'naplok/' in t0 or 'eszkozok/' in t0:
                nevek.append('a projekt saját mérése és naplója')
            else:
                nevek.append('szerkesztői döntés')
    egyedi = []
    for n in nevek:
        if n not in egyedi:
            egyedi.append(n)
    return '; '.join(egyedi), sorted(set(dsek)), sorted(set(kizartak))


SCOPE_NEV = [
    (re.compile(r'^manual$'), 'kézi döntés, lekérdezés nélkül'),
    (re.compile(r'^OT\+NT-full'), 'teljes ószövetségi és újszövetségi szöveg'),
    (re.compile(r'^OT-full'), 'teljes ószövetségi szöveg'),
    (re.compile(r'^NT-full'), 'teljes újszövetségi szöveg'),
    (re.compile(r'^LXX-39'), 'a LXX 39 könyve'),
    (re.compile(r'^TAHOT-teljes\+TAGNT-teljes'), 'teljes ószövetségi és újszövetségi szöveg (TAHOT + TAGNT)'),
    (re.compile(r'^TAHOT-teljes'), 'teljes ószövetségi szöveg (TAHOT)'),
    (re.compile(r'^TAGNT-teljes'), 'teljes újszövetségi szöveg (TAGNT)'),
    (re.compile(r'^range:'), 'megadott igehely-tartomány'),
]


def scope_ford(scope):
    s = (scope or '').strip()
    if not s:
        return 'kézi döntés, lekérdezés nélkül'
    for rx, nev in SCOPE_NEV:
        if rx.search(s):
            return nev
    return 'lekérdezés a megadott hatókörben'


def kereses_modja(forras_kereses):
    """A jelölt `forras_kereses` mezőjének első (| előtti) része -> a keresés módja olvasói nyelven."""
    t = (forras_kereses or '').split(' | ')[0]
    for rx, nev in KERESES_SZABALY:
        if rx.search(t):
            return nev
    return 'szerkesztői vizsgálat (a keresés módja külön nincs rögzítve)'


KERESES_SZABALY = [
    (re.compile(r'^TSK'), 'TSK-kereszthivatkozás'),
    (re.compile(r'Károli-KH'), 'Károli-kereszthivatkozás'),
    (re.compile(r'TAHOT|TAGNT'), 'szó-szintű visszakeresés a héber/görög szövegben'),
    (re.compile(r'^(scan|lanc)', re.I), 'szóbázis (Strong-szám) szerinti teljes szövegkeresés'),
    (re.compile(r'négyforrásos|pozíció-alapú'), 'többforrásos ellenőrzés'),
    (re.compile(r'kollokaci', re.I), 'kollokáció (két szó egy versben)'),
    (re.compile(r'csalad|rokon', re.I), 'rokon szavak (szócsalád) keresése'),
    (re.compile(r'^motívumközi'), 'motívumközi kapcsolat vizsgálata'),
    (re.compile(r'^BDB'), 'szótári (BDB) szócikk alapján'),
    (re.compile(r'DONTESEK|chat|lap-javit|archivum|^a próza szerzője'), 'kézi döntés'),
    (re.compile(r'^F\d+|teljesség|teljesseg'), 'szerkesztői teljességi felmérés'),
]


# ----------------------------------------------------------------------------- gerinc_elem -> horgony

STRONG_RX = re.compile(r'^[HG]\d{4}(?:\s*\+\s*[HG]\d{4})*$')


EMOJI_ELEJE = re.compile(r'^[^\w(]+')


def funkcio_cimke(f):
    """(címke, kiesett): a `funkcio` mező adatréteg-része (DT-F162c). A „ — ” előtti címke marad, emoji nélkül; a
    „ — ” utáni magyarázat (a lexikon szövege) kimarad. Ha nincs „ — ”, a rövid (≤ 60 karakteres, mondatvég nélküli)
    címke marad, a hosszú próza kimarad (`kiesett`)."""
    f = (f or '').strip()
    if not f:
        return '', False
    if ' — ' in f:
        c = f.split(' — ')[0]
    else:
        c = f
        if len(c) > 60 or re.search(r'[.!?]\s*$|\. ', c):
            return '', True
    return EMOJI_ELEJE.sub('', c).strip(), False


def horgony(gerinc):
    """(horgony_tipus, horgony) -- a belső `gerinc_elem` olvasható alakja."""
    g = (gerinc or '').strip()
    if STRONG_RX.match(g):
        szamok = [x.strip() for x in g.split('+')]
        if len(szamok) == 1:
            return 'szóbázis', szamok[0]
        return 'közös szóbázis', ' + '.join(szamok)
    for elo, tipus in (('tematikus:', 'tematikus kapcsolat'), ('referencia:', 'hivatkozás-kapcsolat'),
                       ('idézet:', 'idézet-kapcsolat'), ('formula:', 'formula-kapcsolat')):
        if g.startswith(elo):
            return tipus, g[len(elo):].strip()
    if g.startswith('LXX:'):
        return 'LXX-híd', g[4:].strip()
    if '+' in g:
        return 'kollokáció (szópár egy versben)', ' + '.join(x.strip() for x in g.split('+'))
    return 'egyéb horgony (a típus külön nincs rögzítve)', g


def strong_szamok(*szovegek):
    ki = set()
    for t in szovegek:
        ki.update(re.findall(r'\b[HG]\d{4}\b', t or ''))
    return ki


# ----------------------------------------------------------------------------- az export

def oszlop_tsv(fej, sorok, tabla=None):
    if any(o in IGEHELY_OSZLOPOK for o in fej):     # előbb: a sorkulcs már az egységesített igehelyből képződik
        fej, sorok = osis_bovit(fej, sorok)
    if tabla in ZART:
        fej, sorok = cimke_bovit(tabla, fej, sorok)
    if tabla in SZABAD:
        fej, sorok = angol_bovit(tabla, fej, sorok)
    ki = [FEJLEC, '\t'.join(fej)]
    for s in sorok:
        ki.append('\t'.join(str(s.get(f, '')).replace('\t', ' ').replace('\n', ' ') for f in fej))
    return '\n'.join(ki) + '\n'


CSOPORT_RX = re.compile(r'Összesítő sor (\d+) versre')
BLOKK_RX = re.compile(r'\b(blokk|osztaly)=([^),\s]+)')  # a kulcs „|”-t is tartalmazhat (HAMART-001: tövis|H0329)
CSOPORT_ELTERES = []


def csoport_tagjai(j, kulon_sorok=frozenset()):
    """Összesítő sor (F123 teljességi felmérés): (versszám, a csoport verseinek listája). A tagok a jelölt
    `forras_kereses` mezője által megnevezett gépi osztályozásból (a motívum `…_blokkok.tsv` munkalistájából) jönnek;
    a lista darabszáma egyezzen az indoklás versszámával, különben az export megáll (nincs kitöltés).

    A jelölés `(blokk=…)` vagy `(osztaly=…)`; a kulcs egyben a blokkfájl oszlopa (az ANTROP-001 osztályozója
    `osztaly` oszlopot ír). A blokk azon verse, amelyet a motívum „külön sor”-ként emelt ki a blokkból (a jelöltsor
    `forras_kereses`-e mondja ki, pl. DT503 külön sora), saját kizárás-sor, nem csoport-tag (`kulon_sorok`)."""
    n = int(CSOPORT_RX.match(j['indoklas']).group(1))
    mb = BLOKK_RX.search(j['forras_kereses'])
    if not mb:      # nincs gépi tag-lista: a versszám marad, a tagok nincsenek kitöltve (CLAUDE.md 3. szabály)
        return str(n), []
    rel = 'naplok/F123_teljesseg_%s_blokkok.tsv' % j['id']
    _, sorok = tsv(rel)
    mh = re.search(r'halo=(\w+)', j['forras_kereses'])
    oszlop, blokk = mb.groups()
    tagok = sorted({igehely_normal(s['igehely']) for s in sorok if s[oszlop] == blokk
                    and (not mh or s.get('halo', mh.group(1)) == mh.group(1))
                    and (j['id'], s['igehely']) not in kulon_sorok})
    if len(tagok) != n:      # a lista nem igazolja a számot: a tagok nem töltődnek ki, az eltérés jelentésbe kerül
        CSOPORT_ELTERES.append((j['id'], j['igehely'], n, len(tagok)))
        return str(n), []
    return str(n), tagok


def elutasitas_ok(indoklas, mid, okok):
    elso = (indoklas or '').split(' | ')[0]
    for o in okok:
        if o['id'] not in ('*', mid):
            continue
        if re.search(o['minta'], elso, re.I):
            return o['cimke']
    return 'a besorolás nincs rögzítve'


def kh_meres():
    """A Károli-KH épségmérés számai a generált jelentésből (nem kézzel beírt számok)."""
    t = olvas(KH_JELENTES)
    def szam(minta):
        m = re.search(r'\| ' + minta + r'[^|]*\| (\d+) \|', t)
        return int(m.group(1)) if m else None
    return {
        'forrasvers': szam(r'forrásvers \(van KH-listája\)'),
        'kh_sor': szam(r'KH-sor összesen'),
        'azonos': szam(r'a listája szó szerint megegyezik'),
        'gyanus': szam(r'\*\*gyanús \(másolt\) forrásvers\*\*'),
        'gyanus_sor': szam(r'… a gyanús listák KH-sorai'),
    }


def ismert_hibak(sz):
    kh = kh_meres()
    szam = lambda k: ('%d' % kh[k]) if kh[k] is not None else 'nincs mérve'
    gy = kh['gyanus']
    ki = ['# Ismert hibák a forrásadatokban', '', FEJLEC, '',
          'A nyílt mag készítői itt mondják ki azokat a forráshibákat, amelyeket a saját méréseik kimutattak, '
          'és azt, hogyan kezeli őket a csomag. A hiányt nem töltjük ki: ahol a forrás hibás vagy hiányos, az '
          'üres eredmény nem negatív lelet.', '',
          '## 1. Károli-kereszthivatkozások: más vers listájának másolata', '',
          'A Károli-Biblia kereszthivatkozás-táblájának (a Károli-kiadás kereszthivatkozásai, KH) egy része '
          'nem a saját versének, hanem egy másik versnek a listáját hordozza (például az ApCsel 2:27 sorai '
          'azonosak az ApCsel 7:14 soraival; Ézs 34:11 = Ézs 40:11; Zsolt 116:13 = Zsolt 140:4).', '',
          '| Mérőszám | Érték |', '|---|---|',
          '| a KH-táblában forrásvers (van kereszthivatkozás-listája) | %s |' % szam('forrasvers'),
          '| KH-sor összesen | %s |' % szam('kh_sor'),
          '| a listája szó szerint megegyezik egy másik forrásversével | %s |' % szam('azonos'),
          '| ebből gyanús (másolt) forrásvers | %s |' % szam('gyanus'),
          '| a gyanús listák KH-sorai | %s |' % szam('gyanus_sor'), '',
          '**Gyanús** az a forrásvers, amelynek a listája szó szerint megegyezik egy másik forrásversével, a '
          'saját listájának egyetlen eleme sem támogatott (sem a TSK ±3 verses környezete, sem a cél '
          'visszautalása nem igazolja), a vele azonos listájú vers listája viszont támogatott.', '',
          '**Kezelés.** A nyílt mag a KH-tábla adatát nem tartalmazza, és egyetlen sora sem épít rá: a '
          'kereszthivatkozás-alapú jelöltek az itteni `kizarasok.tsv`-ben a TSK és a kézi minősítés alapján '
          'szerepelnek, a „Károli-kereszthivatkozás” keresési móddal jelölve. A határ: a mérés a másolat-típusú '
          'hibát fogja meg, az egyedi, nem duplikált hibás listát nem. A hibás listák javítása a projekt '
          'nyitott tétele; a javítás után a mérőszámok megváltoznak.', '',
          '## 2. Szemantikai domének: nem teljes lefedés', '',
          'A külön réteg (`cc_by_sa_reteg/`) az UBS SDBH/SDGNT szemantikai doménjeit tartalmazza a csomag '
          'szóbázisaira. A domén-adat az ószövetségi szókincs kb. 90%-át fedi: a hiányzó bejegyzés **nem '
          'negatív lelet**, és a domén támasz, nem a motívum meghatározásának helyettesítője.', '',
          '## 3. A Károli-szó gépi párosítása', '',
          'Az `elofordulasok.tsv` `azonositas_modja` oszlopának `szó-szintű-gépi` értéke modell-kimenet: '
          'a Károli-szó és a Strong-szám párosítását gép végezte, csak magas bizonyosságú pár igazolhat '
          'sort. A mód azt mondja meg, hogyan azonosítottuk a szót, nem azt, hogy a párosítást ember '
          'ellenőrizte.', '']
    return '\n'.join(ki)


def known_issues_en(sz):
    """KNOWN_ISSUES.md: az `ISMERT_HIBAK.md` angol megfelelője (ugyanazok a mért számok, ugyanaz a tartalom)."""
    kh = kh_meres()
    szam = lambda k: ('%d' % kh[k]) if kh[k] is not None else 'not measured'
    ki = ['# Known Errors in the Source Data', '', FEJLEC_EN, '',
          'The makers of the open core state here the source errors that their own measurements revealed, and how '
          'the package handles them. A gap is not filled: where a source is faulty or incomplete, an empty result '
          'is not a negative finding.', '',
          "## 1. Károli cross-references: a copy of another verse's list", '',
          'Part of the cross-reference table of the Károli Bible (the cross-references of the Károli edition, KH) '
          'carries not the list of its own verse but that of another verse (for example, the rows of Acts 2:27 are '
          'identical to those of Acts 7:14; Isa 34:11 = Isa 40:11; Ps 116:13 = Ps 140:4).', '',
          '| Measure | Value |', '|---|---|',
          '| source verses in the KH table (with a cross-reference list) | %s |' % szam('forrasvers'),
          '| KH rows in total | %s |' % szam('kh_sor'),
          '| list identical word for word to that of another source verse | %s |' % szam('azonos'),
          '| of these, suspect (copied) source verses | %s |' % szam('gyanus'),
          '| KH rows of the suspect lists | %s |' % szam('gyanus_sor'), '',
          'A source verse is **suspect** if its list is identical word for word to that of another source verse, '
          'no element of its own list is supported (neither the TSK context of ±3 verses nor the back-reference of '
          'the target confirms it), while the list of the verse with the identical list is supported.', '',
          '**Handling.** The open core does not contain the KH table data, and none of its rows builds on it: '
          'candidates based on cross-references appear in the `kizarasok.tsv` here on the basis of the TSK and hand-made '
          'assessment, marked with the search mode "Károli cross-reference". The limit: the measurement '
          'catches the copy-type error, not an individual faulty list that is not duplicated. Correcting the faulty '
          'lists is an open task of the project; after the correction the measures will change.', '',
          '## 2. Semantic domains: incomplete coverage', '',
          "The separate layer (`cc_by_sa_reteg/`) contains the UBS SDBH/SDGNT semantic domains for the lexical "
          "bases (Strong's numbers) of the package. The domain data cover about 90% of the Old Testament "
          'vocabulary: a missing entry is **not a negative finding**, and the domain is a support, not a substitute '
          'for the definition of the motif.', '',
          '## 3. Machine alignment of the Károli word', '',
          "The value `szó-szintű-gépi` of the `azonositas_modja` column of `elofordulasok.tsv` is model output: "
          "the alignment of the Károli word with the Strong's number was done by machine, and only a "
          'high-confidence pair may justify a row. The mode states how the word was identified, not that a human '
          'verified the alignment.', '']
    return '\n'.join(ki)


# --- a motívum feldolgozási állapota (F167.3)
ALLAPOT_LEZART = 'lezárt kiadás'
ALLAPOT_REGI = 'régi feldolgozás, frissítés alatt'


def feldolgozasi_allapot():
    """{motívum: állapot} a lezárt motívumokra. Lezárt kiadás az a motívum, amelynek van sora az
    `adat/kiadasok.tsv`-ben, és a kiadott lexikonlapján az olvasói kapu 0 BUKÁS-t ad (az `ellenoriz.py`
    32. szabályának mércéje); minden más motívum régi feldolgozás, frissítés alatt."""
    eszk = os.path.dirname(os.path.abspath(__file__))
    if eszk not in sys.path:
        sys.path.insert(0, eszk)
    import olvasoi_kapu as OK
    _, kiad = tsv('adat/kiadasok.tsv')
    ki = {}
    for mid in sorted({k['id'].strip() for k in kiad if k['id'].strip()}):
        ut = os.path.join(GYOKER, 'lexikon', mid + '_TUDOMANYOS.md')
        if not os.path.exists(ut):
            continue
        with open(ut, encoding='utf-8') as f:
            tal, _ = OK.lap_meres(f.read())
        if not OK.osszesit(tal)[1]:
            ki[mid] = ALLAPOT_LEZART
    return ki


# --- „Hogyan olvasd”: három kidolgozott példa, a generált táblákból számolva (F167.3)
PELDA_MOTIVUM = 'ISTENTISZT-001'
PELDA_KIZART = 'Róm 10:12'


def olvasasi_peldak(fajlok):
    """A „Hogyan olvasd / How to read” szakasz számai a generált csomagfájlokból. A kapu ugyanezzel a
    függvénnyel ellenőrzi, hogy a szakasz a mai adatot mondja. Ha a példa eltűnik az adatból, hibát dob."""
    _, elo = tsv_szoveg(fajlok['elofordulasok.tsv'])
    _, kiz = tsv_szoveg(fajlok['kizarasok.tsv'])
    _, csop = tsv_szoveg(fajlok['kizaras_csoportok.tsv'])
    _, mot = tsv_szoveg(fajlok['motivumok.tsv'])
    m = [x for x in mot if x['motivum_azonosito'] == PELDA_MOTIVUM]
    e = [x for x in elo if x['motivum_azonosito'] == PELDA_MOTIVUM]
    k = [x for x in kiz if x['motivum_azonosito'] == PELDA_MOTIVUM and x['igehely'] == PELDA_KIZART
         and x['jelolt_tipus'] == 'elofordulas']
    if not m or not e or len(k) != 1:
        raise SystemExit('olvasasi_peldak: a példa (%s, %s) nincs meg az adatban; a példát frissíteni kell'
                         % (PELDA_MOTIVUM, PELDA_KIZART))
    horgony = {}
    for x in e:
        horgony[x['horgony']] = horgony.get(x['horgony'], 0) + 1
    egyedi = [x for x in kiz if x['motivum_azonosito'] == PELDA_MOTIVUM and x['jelolt_tipus'] == 'elofordulas'
              and not x['csoport_versszam']]
    csoportok = [x for x in kiz if x['motivum_azonosito'] == PELDA_MOTIVUM and x['csoport_versszam']]
    tagok = [x for x in csop if x['motivum_azonosito'] == PELDA_MOTIVUM]
    ok = lambda x: x['kizaras_oka'].replace(' (összesítő sor)', '')
    return {
        'motivum': PELDA_MOTIVUM, 'cim': m[0]['cim'], 'allapot': m[0]['feldolgozasi_allapot'],
        'elo_db': len(e), 'horgony': sorted(horgony.items(), key=lambda h: (-h[1], h[0])),
        'elso': sorted(e, key=lambda x: x['igehely'])[0],
        'kizart': PELDA_KIZART, 'kizart_ok': k[0]['kizaras_oka'], 'kizart_dontes': k[0]['dontesek'],
        'egyedi_db': len(egyedi),
        'csoport_db': len(csoportok),
        'csoportok': [(x['igehely'], ok(x), int(x['csoport_versszam'])) for x in
                      sorted(csoportok, key=lambda x: (-int(x['csoport_versszam']), x['igehely']))],
        'tag_db': len(tagok),
        'osszes': len(e) + len(egyedi) + len(tagok),
    }


def nevelo(szo):
    """A határozott névelő a szó előtt: magánhangzós kezdetnél „az”."""
    return 'az' if szo[:1].lower() in 'aáeéiíoóöőuúüű' else 'a'


def hogyan_olvasd_hu(p):
    h = ', '.join('`%s` (%d sor)' % hd for hd in p['horgony'])
    cs_ = '; '.join('„%s” (%d vers, első verse: %s)' % (o, n, ig) for ig, o, n in p['csoportok'])
    dontes = ('`%s`' % p['kizart_dontes']) if p['kizart_dontes'] else 'itt üres'
    return ['## Hogyan olvasd', '',
            'Három kérdés lépésről lépésre, %s `%s` motívumon (%s). A válaszok számai ebből a kiadásból '
            'generálódnak.' % (nevelo(p['motivum']), p['motivum'], p['cim']), '',
            '### 1. Mely versek tartoznak %s %s-hez, és melyik szón?' % (nevelo(p['motivum']), p['motivum']), '',
            '1. Nyisd meg az `elofordulasok.tsv`-t, és szűrd a `motivum_azonosito` oszlopot %s `%s` értékre.'
            % (nevelo(p['motivum']), p['motivum']),
            '2. Az eredmény %d sor: minden sor egy vers (`igehely`).' % p['elo_db'],
            '3. A `horgony` oszlop mondja meg, melyik héber vagy görög szón (Strong-számon) áll a vers: %s. '
            'A `karoli_szo` oszlop a Károli-fordítás megfelelő szavát adja (például %s: „%s”).'
            % (h, p['elso']['igehely'], p['elso']['karoli_szo']),
            '4. A motívum feldolgozási állapota a `motivumok.tsv` `feldolgozasi_allapot` oszlopában: „%s”.'
            % p['allapot'], '',
            '### 2. Miért nincs benne a %s?' % p['kizart'], '',
            '1. Nyisd meg a `kizarasok.tsv`-t, és szűrd a `motivum_azonosito` = `%s` és az `igehely` = `%s` '
            'értékre (`jelolt_tipus` = `elofordulas`).' % (p['motivum'], p['kizart']),
            '2. A `kizaras_oka` oszlop: „%s”. Az `indoklas` oszlop teljes mondatban mondja el, miért.'
            % p['kizart_ok'],
            '3. A `dontesek` oszlop (%s) a döntés nyilvános azonosítója; a szövegét a `dontesnaplo.tsv` adja.'
            % dontes, '',
            '### 3. Átnézték-e minden helyet, ahol a szópár előfordul?', '',
            '1. A `kizarasok.tsv`-ben %s `%s` sorai közül azok összesítő sorok, amelyeknek a `csoport_versszam` '
            'oszlopa ki van töltve: %d ilyen sor van. Mindegyik egy azonos okból kizárt versek csoportját '
            'képviseli: %s.' % (nevelo(p['motivum']), p['motivum'], p['csoport_db'], cs_),
            '2. A csoportok összes versét a `kizaras_csoportok.tsv` sorolja fel (szűrés: `motivum_azonosito` = '
            '`%s`): %d vers.' % (p['motivum'], p['tag_db']),
            '3. Együtt: %d előfordulás, %d egyenként kizárt vers és %d csoportban kizárt vers, összesen %d vers, '
            'amelyről döntés van. A még el nem döntött jelöltek nincsenek a csomagban; számukat az „Ami nincs a '
            'csomagban” szakasz adja.'
            % (p['elo_db'], p['egyedi_db'], p['tag_db'], p['osszes']), '']


def hogyan_olvasd_en(p):
    h = ', '.join('`%s` (%d rows)' % hd for hd in p['horgony'])
    cs_ = '; '.join('"%s" (%d verses, first verse: %s)' % (o, n, ig) for ig, o, n in p['csoportok'])
    dontes = ('`%s`' % p['kizart_dontes']) if p['kizart_dontes'] else 'empty here'
    return ['## How to read', '',
            'Three questions, step by step, on the motif `%s`. The numbers in the answers are generated from '
            'this release. The column names and values are Hungarian: next to each closed-vocabulary column the `_en` '
            'column gives the English label, next to each passage column the `_osis` column gives the OSIS reference, '
            'and every column is explained in `KODKONYV.md`.' % p['motivum'], '',
            '### 1. Which verses belong to %s, and on which word?' % p['motivum'], '',
            '1. Open `elofordulasok.tsv` and filter the `motivum_azonosito` column on `%s`.' % p['motivum'],
            '2. The result is %d rows: each row is one verse (`igehely`).' % p['elo_db'],
            "3. The `horgony` column gives the Hebrew or Greek word (Strong's number) the verse rests on: %s. "
            'The `karoli_szo` column gives the corresponding word of the Károli translation (e.g. %s: "%s").'
            % (h, p['elso']['igehely'], p['elso']['karoli_szo']),
            '4. The processing stage of the motif is in the `feldolgozasi_allapot` column of `motivumok.tsv`: '
            '"%s".' % p['allapot'], '',
            '### 2. Why is %s not included?' % p['kizart'], '',
            '1. Open `kizarasok.tsv` and filter on `motivum_azonosito` = `%s` and `igehely` = `%s` '
            '(`jelolt_tipus` = `elofordulas`).' % (p['motivum'], p['kizart']),
            '2. The `kizaras_oka` column: "%s". The `indoklas` column states the reason in full.' % p['kizart_ok'],
            '3. The `dontesek` column (%s) is the public identifier of the decision; its text is in '
            '`dontesnaplo.tsv`.' % dontes, '',
            '### 3. Was every place where the word pair occurs examined?', '',
            '1. Among the `%s` rows of `kizarasok.tsv`, those with a filled `csoport_versszam` column are summary '
            'rows: there are %d. Each stands for a group of verses excluded for one reason: %s.'
            % (p['motivum'], p['csoport_db'], cs_),
            '2. `kizaras_csoportok.tsv` lists every verse of these groups (filter: `motivum_azonosito` = `%s`): '
            '%d verses.' % (p['motivum'], p['tag_db']),
            '3. Together: %d occurrences, %d verses excluded one by one and %d verses excluded in groups, %d verses '
            'with a decision in all. Candidates not yet decided are not in the package; their number is given under '
            '"What is not in the package".'
            % (p['elo_db'], p['egyedi_db'], p['tag_db'], p['osszes']), '']


def export(kimenet):
    global _ANGOL
    _ANGOL = None
    CSOPORT_ELTERES.clear()
    CIMKE_HIANY.clear()
    lic = Licenc()
    okok_fej, okok = tsv('adat/elutasitasi_okok.tsv')
    okok.sort(key=lambda o: int(o['sorrend']))
    _, mot = tsv('adat/motivumok.tsv')
    _, elo = tsv('adat/elofordulasok.tsv')
    _, jel = tsv('adat/jeloltek.tsv')
    _, kap = tsv('adat/kapcsolatok.tsv')
    _, mkap = tsv('adat/motivum_kapcsolatok.tsv')
    dforras = dontesek_beolvas()
    dn = Dontesnaplo(dforras)

    mot.sort(key=lambda m: m['id'])
    elo.sort(key=lambda e: (e['id'], e['igehely'], e['gerinc_elem']))
    dontott = [j for j in jel if j['dontes'] in ('elutasítva', 'beépítve')]
    nyitva_db = sum(1 for j in jel if j['dontes'] == 'nyitva')

    # --- 1. menet: melyik döntés kap nyilvános azonosítót (minden exportált szövegből és a dontes_ref-ből)
    for m in mot:
        dn.gyujt(m['negativ_kriterium'])
        dn.gyujt(m['folerendelt_fogalom'])
    for j in dontott:
        dn.gyujt(j['indoklas'])
        dn.gyujt(j['dontes_ref'])
    for k in mkap:
        dn.gyujt(k['indoklas'])
        dn.gyujt(k['dontes_ref'])
    dn.kioszt()
    feloldatlan_dt = sorted(d for d in dn.hivatkozott if d not in dn.azon)

    fajlok = {}
    stat = {}
    kizart_forrasok = {}

    # --- motivumok.tsv
    lezart = feldolgozasi_allapot()
    fej = ['motivum_azonosito', 'cim', 'rovid_cimke', 'tema', 'pardes_szint', 'statusz', 'statusz_datum',
           'feldolgozasi_allapot', 'azonossag_tipusa', 'negativ_kriterium', 'folerendelt_fogalom']
    sorok = [{'motivum_azonosito': m['id'], 'cim': m['cim'], 'rovid_cimke': m['ui_cimke'], 'tema': m['tema'],
              'pardes_szint': m['pardes_szint'], 'statusz': m['statusz'], 'statusz_datum': m['statusz_datum'],
              'feldolgozasi_allapot': lezart.get(m['id'], ALLAPOT_REGI),
              'azonossag_tipusa': m['azonossag_tipusa'],
              'negativ_kriterium': tisztit(m['negativ_kriterium'], dn),
              'folerendelt_fogalom': tisztit(m['folerendelt_fogalom'], dn)} for m in mot]
    fajlok['motivumok.tsv'] = oszlop_tsv(fej, sorok, 'motivumok.tsv')
    stat['motivumok.tsv'] = len(sorok)

    # --- elofordulasok.tsv
    fej = ['motivum_azonosito', 'igehely', 'funkcio', 'pardes_szint', 'horgony_tipus', 'horgony',
           'strong', 'szotar', 'szotari_szocikk', 'jelentes_szam', 'jelentes_en', 'strong_glossza_en', 'karoli_szo',
           'azonositas_modja',
           'megbizhatosag', 'igazolas', 'lekerdezes_tipusa', 'forras_megnevezes', 'forras_dataset',
           'forras_licenc', 'datum']
    sorok = []
    funkcio_kiesett = []
    strongok = set()
    for e in elo:
        p = prov_parse(e['proveniencia'])
        nev, dsek, kiz = forras_fordit(p.get('forras', ''), lic)
        for k in kiz:
            kizart_forrasok[k] = kizart_forrasok.get(k, 0) + 1
        ht, h = horgony(e['gerinc_elem'])
        cimke, kiesett = funkcio_cimke(e['funkcio'])
        if kiesett:
            funkcio_kiesett.append((e['id'], e['igehely'], len(e['funkcio'])))
        strongok |= strong_szamok(e['strong'], e['gerinc_elem'])
        sorok.append({
            'motivum_azonosito': e['id'], 'igehely': e['igehely'],
            'funkcio': cimke,
            'pardes_szint': e['pardes_szint'], 'horgony_tipus': ht, 'horgony': h, 'strong': e['strong'],
            'szotar': e['lexikon_szotar'], 'szotari_szocikk': e['lexikon_entry_id'],
            'jelentes_szam': e['jelentes_szam'], 'jelentes_en': e['jelentes_en'],
            'strong_glossza_en': glossza_en(e['strong']), 'karoli_szo': e['karoli_szo'],
            'azonositas_modja': e['azonositas_modja'], 'megbizhatosag': e['megbizhatosag'],
            'igazolas': e['igazolas'], 'lekerdezes_tipusa': scope_ford(p.get('scope')),
            'forras_megnevezes': nev, 'forras_dataset': '; '.join(dsek),
            'forras_licenc': '; '.join(sorted({lic.cimke(d) for d in dsek})), 'datum': p.get('ts', '')})
    fajlok['elofordulasok.tsv'] = oszlop_tsv(fej, sorok, 'elofordulasok.tsv')
    stat['elofordulasok.tsv'] = len(sorok)

    # --- kizarasok.tsv (az elutasított jelöltek)
    fej = ['motivum_azonosito', 'igehely', 'jelolt_tipus', 'cel_motivum', 'cel_igehely', 'kizaras_oka', 'indoklas',
           'korabbi_minosites', 'csoport_versszam', 'keresesi_mod', 'karoli_szo', 'azonositas_modja',
           'megbizhatosag', 'dontesek', 'datum']
    sorok = []
    csoport_tagok = []
    kulon_sorok = {(j['id'], j['igehely']) for j in dontott
                   if 'külön sor' in j['forras_kereses'] and not CSOPORT_RX.match(j['indoklas'])}
    for j in dontott:
        if j['dontes'] != 'elutasítva':
            continue
        elso, _, utan = j['indoklas'].partition(' | ')
        csv_db = ''
        mc = CSOPORT_RX.match(elso)
        if mc:
            csv_db, tagok = csoport_tagjai(j, kulon_sorok)
            for ig in tagok:
                csoport_tagok.append({'motivum_azonosito': j['id'], 'csoport_sor_igehely': j['igehely'],
                                      'igehely': ig})
        d_ids = []
        for m in DT_RX.finditer(j['dontes_ref'] + ' ' + j['indoklas']):
            a = dn.feloldott(m.group(0))
            if a and a not in d_ids:
                d_ids.append(a)
        sorok.append({
            'motivum_azonosito': j['id'], 'igehely': j['igehely'], 'jelolt_tipus': j['jelolt_tipus'],
            'cel_motivum': j['cel_id'], 'cel_igehely': j['cel_igehely'],
            'kizaras_oka': elutasitas_ok(j['indoklas'], j['id'], okok),
            'indoklas': tisztit(elso, dn), 'korabbi_minosites': tisztit(utan, dn),
            'csoport_versszam': csv_db,
            'keresesi_mod': kereses_modja(j['forras_kereses']), 'karoli_szo': j['karoli_szo'],
            'azonositas_modja': j['azonositas_modja'], 'megbizhatosag': j['megbizhatosag'],
            'dontesek': '; '.join(sorted(d_ids)), 'datum': j['datum']})
    sorok.sort(key=lambda s: (s['motivum_azonosito'], s['igehely'], s['cel_motivum'], s['cel_igehely']))
    fajlok['kizarasok.tsv'] = oszlop_tsv(fej, sorok, 'kizarasok.tsv')
    stat['kizarasok.tsv'] = len(sorok)
    csoport_tagok.sort(key=lambda s: (s['motivum_azonosito'], s['csoport_sor_igehely'], s['igehely']))
    fajlok['kizaras_csoportok.tsv'] = oszlop_tsv(['motivum_azonosito', 'csoport_sor_igehely', 'igehely'],
                                                  csoport_tagok)
    stat['kizaras_csoportok.tsv'] = len(csoport_tagok)

    # --- beepitesi_dontesek.tsv (a beépített jelöltek indoklása és döntései, az előfordulásokhoz kulcsolva)
    fej = ['motivum_azonosito', 'igehely', 'jelolt_tipus', 'cel_motivum', 'cel_igehely', 'indoklas',
           'korabbi_minosites', 'keresesi_mod', 'dontesek', 'datum']
    sorok = []
    for j in dontott:
        if j['dontes'] != 'beépítve':
            continue
        elso, _, utan = j['indoklas'].partition(' | ')
        d_ids = []
        for m in DT_RX.finditer(j['dontes_ref'] + ' ' + j['indoklas']):
            a = dn.feloldott(m.group(0))
            if a and a not in d_ids:
                d_ids.append(a)
        sorok.append({
            'motivum_azonosito': j['id'], 'igehely': j['igehely'], 'jelolt_tipus': j['jelolt_tipus'],
            'cel_motivum': j['cel_id'], 'cel_igehely': j['cel_igehely'],
            'indoklas': tisztit(elso, dn), 'korabbi_minosites': tisztit(utan, dn),
            'keresesi_mod': kereses_modja(j['forras_kereses']), 'dontesek': '; '.join(sorted(d_ids)),
            'datum': j['datum']})
    sorok.sort(key=lambda s: (s['motivum_azonosito'], s['igehely'], s['cel_motivum'], s['cel_igehely']))
    fajlok['beepitesi_dontesek.tsv'] = oszlop_tsv(fej, sorok, 'beepitesi_dontesek.tsv')
    stat['beepitesi_dontesek.tsv'] = len(sorok)

    # --- kapcsolatok.tsv (igehely-párok)
    fej = ['motivum_azonosito', 'forras_igehely', 'cel_igehely', 'tipus', 'bizonyossag', 'pardes_szint',
           'lekerdezes_tipusa', 'forras_megnevezes', 'datum']
    sorok = []
    for k in kap:
        elso, _, utan = k['indoklas'].partition(' | ')
        p = prov_parse(utan)
        nev = forras_fordit(p.get('forras', ''), lic)[0] if p else ''
        sorok.append({'motivum_azonosito': k['id'], 'forras_igehely': k['forras_igehely'],
                      'cel_igehely': k['cel_igehely'], 'tipus': k['tipus'],
                      'bizonyossag': k['bizonyossag'], 'pardes_szint': k['pardes_szint'],
                      'lekerdezes_tipusa': scope_ford(p.get('scope')) if p else '',
                      'forras_megnevezes': nev, 'datum': (p.get('ts') or '')[:10]})
    sorok.sort(key=lambda s: (s['motivum_azonosito'], s['forras_igehely'], s['cel_igehely']))
    fajlok['kapcsolatok.tsv'] = oszlop_tsv(fej, sorok, 'kapcsolatok.tsv')
    stat['kapcsolatok.tsv'] = len(sorok)

    # --- motivum_kapcsolatok.tsv
    fej = ['motivum_a', 'igehely_a', 'alpont_a', 'motivum_b', 'igehely_b', 'alpont_b', 'tipus',
           'bizonyossag', 'pardes_szint', 'dontesek', 'lekerdezes_tipusa', 'forras_megnevezes', 'datum']
    sorok = []
    for k in mkap:
        p = prov_parse(k['proveniencia'])
        nev, _, _ = forras_fordit(p.get('forras', ''), lic)
        d_ids = sorted({dn.feloldott(m.group(0)) for m in DT_RX.finditer(k['dontes_ref'] + ' ' + k['indoklas'])
                        if dn.feloldott(m.group(0))})
        sorok.append({'motivum_a': k['id_a'], 'igehely_a': k['igehely_a'], 'alpont_a': k['alpont_a'],
                      'motivum_b': k['id_b'], 'igehely_b': k['igehely_b'], 'alpont_b': k['alpont_b'],
                      'tipus': k['tipus'], 'bizonyossag': k['bizonyossag'], 'pardes_szint': k['pardes_szint'],
                      'dontesek': '; '.join(d_ids), 'lekerdezes_tipusa': scope_ford('range:' if p.get('scope') else ''),
                      'forras_megnevezes': nev, 'datum': (p.get('ts') or '')[:10]})
    sorok.sort(key=lambda s: (s['motivum_a'], s['igehely_a'], s['motivum_b'], s['igehely_b']))
    fajlok['motivum_kapcsolatok.tsv'] = oszlop_tsv(fej, sorok, 'motivum_kapcsolatok.tsv')
    stat['motivum_kapcsolatok.tsv'] = len(sorok)

    # --- dontesnaplo.tsv
    fej = ['dontes_azonosito', 'kerdes', 'dontes', 'datum']
    sorok = []
    for dt, nyd in sorted(dn.azon.items(), key=lambda x: x[1]):
        d = dforras[dt]
        datum = re.search(r'\d{4}-\d{2}-\d{2}', d['dontes'])
        sorok.append({'dontes_azonosito': nyd,
                      'kerdes': egy_mondat(tisztit(d['kerdes'], dn), 300),
                      'dontes': egy_mondat(tisztit(d['dontes'], dn), 380),
                      'datum': datum.group(0) if datum else 'nincs rögzítve'})
    fajlok['dontesnaplo.tsv'] = oszlop_tsv(fej, sorok, 'dontesnaplo.tsv')
    stat['dontesnaplo.tsv'] = len(sorok)

    # --- forrasok_es_licencek.tsv
    hasznalt = set()
    for e in elo:
        p = prov_parse(e['proveniencia'])
        hasznalt.update(forras_fordit(p.get('forras', ''), lic)[1])
    for j in dontott:
        for t in re.findall(r'[\w]+_kivonat\.tsv|Karoli_1908\.tsv|BSB_Strongs\.tsv|LXX_OS', j['forras_kereses']):
            if t in lic.fajl_dataset:
                hasznalt.add(lic.fajl_dataset[t])
        if re.search(r'^TSK', j['forras_kereses']) or 'TSK' in j['forras_kereses']:
            hasznalt.add('TSK')
    hasznalt.add(SAJAT_SOR)
    # az angol szófogódzó forrása (strong_glossza_en): a TBESH a héber, a TBESG a görög Strong-számokra
    if any(e['strong'].startswith('H') or '+H' in e['strong'] for e in elo):
        hasznalt.add('TBESH')
    if any(e['strong'].startswith('G') or '+G' in e['strong'] for e in elo):
        hasznalt.add('TBESG')
    fej = ['dataset', 'licenc', 'szerepe_a_csomagban', 'ok']
    sorok = []
    for ds in sorted(lic.sor):
        st, ok = lic.allapot(ds)
        if st == 'kizart':
            szerep = 'kizárva'
        elif st == 'sa_reteg':
            szerep = 'külön réteg (cc_by_sa_reteg/)'
        elif st == 'sajat':
            szerep = 'a csomag saját adata'
        elif ds in GLOSSZA_FORRAS and ds in hasznalt:
            szerep = 'forrás (az angol szófogódzó oszlopé)'
        elif ds in hasznalt:
            szerep = 'forrás (a sorok forrásmegjelölésében szerepel)'
        else:
            szerep = 'engedett, de a csomag nem használja'
        sorok.append({'dataset': ds, 'licenc': lic.cimke(ds), 'szerepe_a_csomagban': szerep, 'ok': ok})
    fajlok['forrasok_es_licencek.tsv'] = oszlop_tsv(fej, sorok, 'forrasok_es_licencek.tsv')
    stat['forrasok_es_licencek.tsv'] = len(sorok)
    kizartak = sorted(s['dataset'] for s in sorok if s['szerepe_a_csomagban'] == 'kizárva')

    # --- CC BY-SA külön réteg: az SDBH/SDGNT-domének a csomag szóbázisaira
    sd_fej = ['strong', 'szotar', 'lemma', 'jelentes_azonosito', 'domen_kod', 'domen_neve', 'glossza']
    sd = []
    for fn in ('SDBH_domenek.tsv', 'SDGNT_domenek.tsv'):
        _, ss = tsv('konkordancia/' + fn)
        for s in ss:
            if s['strong'] in strongok:
                sd.append({'strong': s['strong'], 'szotar': s['szotar'], 'lemma': s['lemma'],
                           'jelentes_azonosito': s['lexid'], 'domen_kod': s['domen_kod'],
                           'domen_neve': s['domen'], 'glossza': s['glossza']})
    sd.sort(key=lambda s: (s['strong'], s['szotar'], s['jelentes_azonosito']))
    sd_fej, sd = cimke_bovit('cc_by_sa_reteg/szemantikai_domenek.tsv', sd_fej, sd)
    sa_fejlec = ('# GENERÁLT: a PaRDeS nyílt mag külön rétege — CC BY-SA 4.0 (UBS SDBH v0.9.2, SDGNT v1.1); '
                 'kézzel nem szerkesztendő; a „#” kezdetű sor megjegyzés.')
    fajlok['cc_by_sa_reteg/szemantikai_domenek.tsv'] = (
        sa_fejlec + '\n' + '\t'.join(sd_fej) + '\n' +
        ''.join('\t'.join(s[f] for f in sd_fej) + '\n' for s in sd))
    stat['cc_by_sa_reteg/szemantikai_domenek.tsv'] = len(sd)
    fajlok['cc_by_sa_reteg/OLVASSEL.md'] = (
        '# CC BY-SA 4.0 réteg — szemantikai domének\n\n' + sa_fejlec + '\n\n'
        'Ez a könyvtár **külön** áll a csomag többi (CC BY 4.0) részétől: tartalma a Creative Commons '
        'Attribution-ShareAlike 4.0 International licenc alatt áll, a belőle származtatott munka is ezen a '
        'licencen adható tovább (nem zárható el).\n\n'
        '**Forrásmegjelölés (szó szerint).** UBS Dictionary of Biblical Hebrew © United Bible Societies, 2023. '
        'Adapted from Semantic Dictionary of Biblical Hebrew © 2000-2023 United Bible Societies. UBS Dictionary '
        'of New Testament Greek, © United Bible Societies, 2023. Adapted from Semantic Dictionary of Biblical '
        'Greek: © United Bible Societies 2018-2023, which is adapted from Greek-English Lexicon of the New '
        'Testament: Based on Semantic Domains, Eds. J P Louw, Eugene Albert Nida © United Bible Societies 1988, '
        '1989. A forrás: ubsicap/ubs-open-license, UBSHebrewDic-v0.9.2-en.JSON és UBSGreekNTDic-v1.1-en.JSON. '
        'Licenc: https://creativecommons.org/licenses/by-sa/4.0/\n\n'
        'A csomag szóbázisaira (Strong-számaira) választott sorok szerepelnek; a domén az ószövetségi '
        'szókincs kb. 90%-át fedi, a hiányzó bejegyzés **nem negatív lelet** (l. `../ISMERT_HIBAK.md`).\n')

    # --- ismert hibák
    fajlok['ISMERT_HIBAK.md'] = ismert_hibak(stat)
    fajlok['KNOWN_ISSUES.md'] = known_issues_en(stat)

    # --- kódkönyv (az adat/nyilt_kodkonyv.tsv-ből: a TSV és az olvasható változat)
    kk_fej, kk = tsv('adat/nyilt_kodkonyv.tsv')
    kk.sort(key=lambda s: (s['tabla'], s['oszlop'], s['ertek']))
    kf = ['tabla', 'oszlop', 'ertek', 'leiras_hu', 'leiras_en', 'cimke_en']
    fajlok['kodkonyv.tsv'] = oszlop_tsv(kf, kk)
    stat['kodkonyv.tsv'] = len(kk)
    md = ['# Kódkönyv / Codebook', '', KOD_FEJLEC, '',
          'Minden oszlop, érték és kód leírása magyarul és angolul. / Description of every column, value and code, '
          'in Hungarian and English.', '',
          '**Adatréteg / data layer.** %s / %s' % (ADATMAG_LEXIKON_HU, ADATMAG_LEXIKON_EN), '']
    akt = None
    for s in kk:
        if (s['tabla']) != akt:
            akt = s['tabla']
            md += ['', '## ' + akt, '']
        if s['ertek']:
            md.append('- `%s` = `%s` (en: `%s`): %s / %s' % (s['oszlop'], s['ertek'], s.get('cimke_en', ''), s['leiras_hu'],
                                                           s['leiras_en']))
        else:
            md += ['', '### `%s`' % s['oszlop'], '', s['leiras_hu'], '', '*' + s['leiras_en'] + '*', '']
    fajlok['KODKONYV.md'] = '\n'.join(md) + '\n'

    # --- OLVASSEL.md
    peldak = olvasasi_peldak(fajlok)
    sorszamok = ''.join('| `%s` | %d |\n' % (k, v) for k, v in sorted(stat.items()))
    ol = ['# PaRDeS nyílt mag — olvass el', '', FEJLEC, '', '*English version: `README.md`.*', '',
          '**Licenc:** CC BY 4.0 (a nyílt mag saját adata és szövege). A `cc_by_sa_reteg/` könyvtár tartalma '
          'külön, CC BY-SA 4.0 licenc alatt áll; l. az ottani `OLVASSEL.md`-t.', '',
          '**Mi ez.** Egy bibliai motívumkutatás (PaRDeS-módszer) nyílt magja: a motívumok meghatározó jegyei, '
          'az előfordulás-lista, a kizárt helyek okkal, az igehely-kapcsolatok és a döntésnapló. A fájlok az '
          'adatból generált, olvasónak szóló nézetek; a munkaközi jelölések feloldva vannak. Az oszlopok '
          'és kódok leírása: `kodkonyv.tsv` / `KODKONYV.md` (magyar és angol).', '',
          '**Feldolgozási állapot.** A motívumok közül %d lezárt kiadás (a lexikonlapja kiadott, és az olvasói '
          'kapun hiba nélkül átment), %d régi feldolgozás, amely a későbbi változatokban frissül; motívumonként a '
          '`motivumok.tsv` `feldolgozasi_allapot` oszlopa mondja meg.' % (len(lezart), len(mot) - len(lezart)), '',
          '**Ismert hibák:** l. `ISMERT_HIBAK.md` (angolul: `KNOWN_ISSUES.md`).', '',
          ] + hogyan_olvasd_hu(peldak) + [
          '## Fájlok és sorszámuk', '', '| Fájl | Sor |', '|---|---|', sorszamok.rstrip('\n'), '',
          '## Licencszűrés', '',
          'A szűrés a projekt licenc-leltára szerint történt. **Kizárt források** (a csomag értéket nem tartalmaz '
          'belőlük): ' + ', '.join('`%s`' % k for k in kizartak) + '. Okuk soronként a `forrasok_es_licencek.tsv` '
          '`ok` oszlopában áll (nem kereskedelmi vagy GPL licenc, tisztázatlan licenc, a projekt zárt '
          'származtatott rétege). Ez a leltár, nem jogi vélemény.', '',
          '## Közzétételi hely', '',
          'A csomag kanonikus közzétételi helye: `<KANONIKUS_FORRAS_URL>` (helyőrző; a közzétételkor töltődik ki). '
          'A változatot a kiadás azonosítója jelöli (`KIADAS.txt`: az adatállapot dátuma és a tartalmi hash), '
          'nem egy fejlesztői tár vagy commit.', '',
          '## Idézés és a mesterséges intelligencia használata', '',
          'A kiadás mellé idézési metaadat (Citation File Format) és a mesterséges intelligencia használatáról '
          'szóló nyilatkozat kerül a közzétételi helyen; a szerző által kitöltendő mezőik a közzétételig '
          'helyőrzők. A nyilatkozat két réteget különít el: a nyílt adatmagot (CC BY 4.0, ez a csomag) és a '
          'lexikont mint önálló művet (minden jog fenntartva).', '',
          '## Angol réteg', '',
          'A csomag oszlopnevei és értékei magyarok; mellettük angol párhuzamos oszlopok állnak. **Igehely:** minden '
          'igehely-oszlop mellett `…_osis` (szabványos OSIS-igehelykulcs, alakja a kódkönyvben); a könyvkód szabványos, a fejezet- és '
          'versszám a Károli-fordítás számozása — ahol ez eltér a KJV- vagy a STEPBible-számozástól, a kulcs a '
          'Károli-verset jelöli. **Zárt értékek:** minden zárt értékkészletű oszlop mellett `…_en`, a kódkönyv '
          'szerkesztett angol címkéjével. **Szabad szöveg** (indoklás, funkció, a motívum meghatározása, a '
          'döntésnapló): `…_en` párhuzamos mező, **gépi fordítás**; a sor `forditas_modja` oszlopa nevezi meg a '
          'modellt, a hiányt kimondja. **Szófogódzó:** az `elofordulasok.tsv` `strong_glossza_en` oszlopa a '
          'Strong-szám STEPBible-glosszája (Data created by www.STEPBible.org based on work at Tyndale House '
          'Cambridge, CC BY 4.0); a `jelentes_en` ettől külön, szótári kivonat.', '',
          '## Csoportos kizárás', '',
          'A `kizarasok.tsv` egyes sorai **összesítő sorok**: egy csoport (azonos ok miatt kizárt versek) első '
          'versét nevezik meg, a `csoport_versszam` oszlop a csoport verseinek számát adja, a csoport összes '
          'versét a `kizaras_csoportok.tsv` sorolja fel. Az összesítő sor indoklása a csoportra érvényes.', '',
          '## Mi van benne, mi nincs (az adatmag és a lexikon)', '',
          ADATMAG_LEXIKON_HU, '',
          '**Benne van (adatréteg):** a motívum azonosítója, címe és kizáró jegye; az előfordulások (igehely, '
          'szóbázis, szótári jelentés, Károli-szó); a kizárások és a beépítési döntések indoklással; a '
          'kapcsolatok; a proveniencia (a forrás megnevezése, licence, a lekérdezés típusa, dátum); a '
          'döntésnapló.', '',
          '**Nincs benne (a lexikon):** az értelmező próza (kivonat, értelmezés, igehelyenkénti '
          'kifejtés), a magyar szótári fordítások, a kötetanyag és a lexikonlapok.', '',
          '## Ami nincs a csomagban', '',
          '- A `nyitva` állapotú (még el nem döntött) jelöltek: %d db.' % nyitva_db,
          '- A lexikon szövege (értelmező próza, magyar szótári fordítások, Strong-számos Károli-szöveg), a '
          'tanulmányok és a lexikonlapok.',
          '- A belső munkajelek: azonosítók, munkafájlok, lekérdezés-nyomok. Ahol egy döntésre hivatkozás áll, a '
          'nyilvános azonosító (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel.', '',
          '## Ellenőrzés', '',
          'A `ELLENORZO_OSSZEG.sha256` fájl minden fájl SHA-256 összegét tartalmazza; az export újrafuttatva '
          'bájtazonos.', '']
    fajlok['OLVASSEL.md'] = '\n'.join(ol)

    # --- README.md (az OLVASSEL.md angol megfelelője: ugyanaz a tartalom)
    re_ = ['# PaRDeS Open Core — Read Me', '', FEJLEC_EN, '',
           '*Magyar változat: `OLVASSEL.md`.*', '',
           "**Licence:** CC BY 4.0 (the open core's own data and text). The contents of the `cc_by_sa_reteg/` "
           'directory are under a separate licence, CC BY-SA 4.0; see the `OLVASSEL.md` there.', '',
           '**What this is.** The open core of a study of biblical motifs (the PaRDeS method): the defining '
           'features of the motifs, the list of occurrences, the excluded passages with reasons, the relations '
           'between passages and the decision log. The files are reader-facing views generated from the data; '
           'working marks are resolved. The columns and codes are described in `kodkonyv.tsv` / `KODKONYV.md` '
           '(Hungarian and English).', '',
           '**Processing stage.** Of the motifs, %d are closed releases (their lexicon page is released and passed '
           'the reader check without error) and %d come from an earlier stage and will be updated in later '
           'versions; the `feldolgozasi_allapot` column of `motivumok.tsv` gives the stage of each motif.'
           % (len(lezart), len(mot) - len(lezart)), '',
           '**Known errors:** see `KNOWN_ISSUES.md`.', '',
           ] + hogyan_olvasd_en(peldak) + [
           '## Files and their row counts', '', '| File | Rows |', '|---|---|', sorszamok.rstrip('\n'), '',
           '## Licence filtering', '',
           "The filtering follows the project's licence inventory. **Excluded sources** (the package contains no "
           'value from them): ' + ', '.join('`%s`' % k for k in kizartak) + '. The reason for each is given in '
           'the `ok` column of `forrasok_es_licencek.tsv` (non-commercial or GPL licence, unclear licence, the '
           "project's closed derived layer). This is an inventory, not a legal opinion.", '',
           '## Place of publication', '',
           'The canonical place of publication of the package: `<KANONIKUS_FORRAS_URL>` (a placeholder, filled in '
           'at publication). A version is identified by the release identifier (`RELEASE.txt`: the date of the '
           'data state and the content hash), not by a development repository or a commit.', '',
           '## Citation and the use of artificial intelligence', '',
           'With the release, citation metadata (Citation File Format) and a statement on the use of artificial '
           'intelligence are provided at the place of publication; their fields to be completed by the author are '
           'placeholders until publication. The statement separates two layers: the open data core (CC BY 4.0, this '
           'package) and the lexicon as a separate work (all rights reserved).', '',
           '## English layer', '',
           'The column names and values of the package are Hungarian; English parallel columns stand next to them. '
           '**Passages:** next to every passage column, `…_osis` (an OSIS reference, e.g. `1Kgs.13.31`); the book '
           'code is standard, chapter and verse follow the versification of the Károli translation — where it '
           'differs from the KJV or STEPBible numbering, the key denotes the Károli verse. **Closed values:** next '
           'to every closed-vocabulary column, `…_en`, with the edited English label of the codebook. **Free '
           'text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, '
           'a **machine translation**; the row’s `forditas_modja` column names the model and states any gap. '
           '**Word cue:** the `strong_glossza_en` column of `elofordulasok.tsv` is the STEPBible gloss of the '
           'Strong number (Data created by www.STEPBible.org based on work at Tyndale House Cambridge, CC BY 4.0); '
           '`jelentes_en` is separate, a dictionary excerpt.', '',
           '## Group exclusion', '',
           'Some rows of `kizarasok.tsv` are **summary rows**: they name the first verse of a group (verses '
           'excluded for the same reason), the `csoport_versszam` column gives the number of verses in the group, '
           'and `kizaras_csoportok.tsv` lists all verses of the group. The rationale of a summary row applies to '
           'the whole group.', '',
           '## What is in it and what is not (the data core and the lexicon)', '',
           ADATMAG_LEXIKON_EN, '',
           '**Included (data layer):** the motif identifier, title and exclusion criterion; the occurrences '
           '(passage, lexical base, dictionary meaning, Károli word); the exclusions and inclusion decisions with '
           'rationale; the relations; provenance (the naming of the source, its licence, the type of query, the '
           'date); the decision log.', '',
           '**Not included (the lexicon):** the interpretive prose (summary, interpretation, passage-by-passage '
           'exposition), the Hungarian dictionary translations, the volume material and the lexicon pages.', '',
           '## What is not in the package', '',
           '- Candidates in the `nyitva` (open, not yet decided) state: %d.' % nyitva_db,
           "- The text of the lexicon (interpretive prose, Hungarian dictionary translations, Károli text with "
           "Strong's numbers), the studies and the lexicon pages.",
           '- Internal working marks: identifiers, working files, query traces. Where a decision is referred to, '
           'the public identifier (`NYD-nnn`) can be resolved in `dontesnaplo.tsv`.', '',
           '## Verification', '',
           'The file `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every file; rerunning the export is '
           'byte-identical.', '']
    fajlok['README.md'] = '\n'.join(re_)

    if CIMKE_HIANY:
        raise SystemExit('a zárt érték angol címkéje (cimke_en) hiányzik a kódkönyvből: %s' % '; '.join(
            '%s/%s = %s' % x for x in sorted(set(CIMKE_HIANY))))

    # --- ellenőrző összeg
    sor = []
    for rel in sorted(fajlok):
        sor.append('%s  %s' % (hashlib.sha256(fajlok[rel].encode('utf-8')).hexdigest(), rel))
    fajlok['ELLENORZO_OSSZEG.sha256'] = '\n'.join(sor) + '\n'
    datumok = []
    for rel in ('elofordulasok.tsv', 'kizarasok.tsv', 'beepitesi_dontesek.tsv'):
        _, ds = tsv_szoveg(fajlok[rel])
        datumok += [d['datum'].replace('.', '-') for d in ds if re.match(r'\d{4}[-.]\d{2}[-.]\d{2}', d['datum'])]
    hash_ = hashlib.sha256(fajlok['ELLENORZO_OSSZEG.sha256'].encode('utf-8')).hexdigest()
    datum = max(datumok) if datumok else 'nincs rögzítve'
    fajlok['KIADAS.txt'] = ('kiadas_azonosito: %s-%s\nadatallapot_datuma: %s\ntartalmi_hash_sha256: %s\n'
                            'kozzeteteli_hely: <KANONIKUS_FORRAS_URL>\n' % (datum, hash_[:16], datum, hash_))
    fajlok['RELEASE.txt'] = ('release_id: %s-%s\ndata_state_date: %s\ncontent_hash_sha256: %s\n'
                             'publication_place: <KANONIKUS_FORRAS_URL>\n' % (datum, hash_[:16], datum, hash_))
    return fajlok, {'stat': stat, 'kizartak': kizartak, 'kizart_forras_sorok': kizart_forrasok,
                    'feloldatlan_dt': feloldatlan_dt, 'nyitva': nyitva_db, 'dontes_db': len(dn.azon),
                    'sd_db': len(sd), 'strong_db': len(strongok),
                    'funkcio_kiesett': funkcio_kiesett, 'csoport_elteres': list(CSOPORT_ELTERES)}


def tsv_szoveg(szoveg):
    """Generált TSV-szöveg (`#` fejléces) -> (fejléc, [dict])."""
    sorok = [s for s in szoveg.split('\n') if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t') + [''] * (len(fej) - len(s.split('\t'))))) for s in sorok[1:]]


def kiir(fajlok, kimenet):
    abs_ki = os.path.join(GYOKER, kimenet) if not os.path.isabs(kimenet) else kimenet
    # a régi generált fájlok eltávolítása (a könyvtár tartalma pontosan a generált készlet)
    if os.path.isdir(abs_ki):
        for gyoker, _, nevek in os.walk(abs_ki):
            for n in nevek:
                rel = os.path.relpath(os.path.join(gyoker, n), abs_ki).replace('\\', '/')
                if rel not in fajlok:
                    os.remove(os.path.join(gyoker, n))
    for rel, tartalom in fajlok.items():
        ut = os.path.join(abs_ki, rel)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)
    return abs_ki


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--kimenet', default='nyilt_mag')
    a = ap.parse_args()
    fajlok, info = export(a.kimenet)
    ut = kiir(fajlok, a.kimenet)
    print('nyílt mag exportálva: %s' % ut)
    for k, v in sorted(info['stat'].items()):
        print('  %-45s %6d sor' % (k, v))
    print('  döntésnapló: %d nyilvános döntés; feloldatlan DT-hivatkozás: %s' % (
        info['dontes_db'], ', '.join(info['feloldatlan_dt']) or 'nincs'))
    print('  kizárt források: %s' % ', '.join(info['kizartak']))
    print('  nyitva (nem exportált): %d' % info['nyitva'])
    for x in info['csoport_elteres']:
        print('  FIGYELEM: összesítő sor versszáma nem egyezik a listával (tagok nincsenek kitöltve): %s %s: %d <> %d' % x)
    return 0


if __name__ == '__main__':
    sys.exit(main())
