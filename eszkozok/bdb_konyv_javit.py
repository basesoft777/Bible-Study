#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bdb_konyv_javit.py — F46 (BDB_KONYVFELOLDAS): a BDB-forras rosszul feloldott
konyvneveinek felmerese (es a jovahagyas utan javitasa).

Bemenet:
  konkordancia/BDB_teljes_unabridged.tsv   (a javitando forras)
  konkordancia/OSHL_BDB_igehelyek.tsv      (fuggetlen forras: OpenScriptures BDB-XML
                                            strukturalt igehelyei, l. --kivonat)
  konkordancia/TAHOT_kivonat.tsv           (Strong-proba, +-1 vers)
  konkordancia/Macula_heber_*.tsv          (MT-versszamozas: vers-letezes, MT->Karoli
                                            versmegfeleltetes a TAHOT-probahoz)
  naplok/F34_M2_maradek.tsv                (az N-F34 maradeka: a ψ-tipus jelolese)

Modok (a repo gyokerebol):
  python eszkozok/bdb_konyv_javit.py --kivonat <BrownDriverBriggs.xml> <LexicalIndex.xml>
        -> konkordancia/OSHL_BDB_igehelyek.tsv (strong, bdb_id, sorszam, konyv, fejezet, vers)
  python eszkozok/bdb_konyv_javit.py            (felmeres, szarazon)
        -> naplok/BDB_KONYVFELOLDAS_csere.tsv, naplok/BDB_KONYVFELOLDAS_kezi.tsv,
           osszesites a kimeneten (proveniencia-sorral)
  python eszkozok/bdb_konyv_javit.py --ir --szintek magas[,kozepes]
        -> (CSAK a 3.5 jovahagyasa utan) mezokulcsos, poziciohoz kotott csere a
           forrasban es az adat/forditasok.tsv BDB-soraiban

Az igehely egysege a forrasban a KONYVJELOLT TOKEN (`Hab 41:47`): a konyv nelkuli,
lancolt igehelyek (`; 42:3`) az elozo konyvjelolest oroklik, tehat a token javitasa
a lancot is javitja. A token kulcsa: (strong, pozicio = karakter-offset a
Teljes_szocikk mezoben, forras_alak).

I/O: split('\\t') / '\\t'.join (csv modul nelkul); iras elott sor-osszevetes.
"""
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import normalizal as N  # noqa: E402
from forditas_kapuk import FEJEZETSZAM  # noqa: E402

FORRAS = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
OSHL_REF = os.path.join(REPO, 'konkordancia', 'OSHL_BDB_igehelyek.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
FORD = os.path.join(REPO, 'adat', 'forditasok.tsv')
F34_MARADEK = os.path.join(REPO, 'naplok', 'F34_M2_maradek.tsv')
CSERE = os.path.join(REPO, 'naplok', 'BDB_KONYVFELOLDAS_csere.tsv')
KEZI = os.path.join(REPO, 'naplok', 'BDB_KONYVFELOLDAS_kezi.tsv')
OSHL_COMMIT = '21c9add13bc727d3a951361778e97e3ff7afd1ce'

OSZ = ['1Móz', '2Móz', '3Móz', '4Móz', '5Móz', 'Józs', 'Bír', 'Ruth', '1Sám', '2Sám', '1Kir',
       '2Kir', '1Krón', '2Krón', 'Ezsd', 'Neh', 'Eszt', 'Jób', 'Zsolt', 'Péld', 'Préd', 'Én',
       'Ézs', 'Jer', 'JSir', 'Ez', 'Dán', 'Hós', 'Jóel', 'Ámós', 'Abd', 'Jón', 'Mik', 'Náh',
       'Hab', 'Sof', 'Hag', 'Zak', 'Mal']
OSZ_SET = set(OSZ)

# Macula konyvkod -> Karoli-rovidites (a Macula_heber_* fajlok ref-oszlopa)
MACULA_KOD = {
    'GEN': '1Móz', 'EXO': '2Móz', 'LEV': '3Móz', 'NUM': '4Móz', 'DEU': '5Móz', 'JOS': 'Józs',
    'JDG': 'Bír', 'RUT': 'Ruth', '1SA': '1Sám', '2SA': '2Sám', '1KI': '1Kir', '2KI': '2Kir',
    '1CH': '1Krón', '2CH': '2Krón', 'EZR': 'Ezsd', 'NEH': 'Neh', 'EST': 'Eszt', 'JOB': 'Jób',
    'PSA': 'Zsolt', 'PRO': 'Péld', 'ECC': 'Préd', 'SNG': 'Én', 'ISA': 'Ézs', 'JER': 'Jer',
    'LAM': 'JSir', 'EZK': 'Ez', 'DAN': 'Dán', 'HOS': 'Hós', 'JOL': 'Jóel', 'AMO': 'Ámós',
    'OBA': 'Abd', 'JON': 'Jón', 'MIC': 'Mik', 'NAM': 'Náh', 'HAB': 'Hab', 'ZEP': 'Sof',
    'HAG': 'Hag', 'ZEC': 'Zak', 'MAL': 'Mal'}
# a TAHOT a Lam-ot 'Sir'-nek irja (bdb_psi_javit.py, HU vs HU_FORD)
TAHOT_KONYV = {'Sir': 'JSir'}

# OSIS (a BDB-XML r= attributuma) -> Karoli. A forrasbeli elirasok (Hosea, Is, iKgs,
# Jugd, Jos, Zp, Zec, Ho) a kivonatban Karoli-alakra kepzodnek, es a kivonat
# fejlece rogziti oket.
OSIS = {
    'Gen': '1Móz', 'Exod': '2Móz', 'Lev': '3Móz', 'Num': '4Móz', 'Deut': '5Móz', 'Josh': 'Józs',
    'Judg': 'Bír', 'Ruth': 'Ruth', '1Sam': '1Sám', '2Sam': '2Sám', '1Kgs': '1Kir', '2Kgs': '2Kir',
    '1Chr': '1Krón', '2Chr': '2Krón', 'Ezra': 'Ezsd', 'Neh': 'Neh', 'Esth': 'Eszt', 'Job': 'Jób',
    'Ps': 'Zsolt', 'Prov': 'Péld', 'Eccl': 'Préd', 'Song': 'Én', 'Isa': 'Ézs', 'Jer': 'Jer',
    'Lam': 'JSir', 'Ezek': 'Ez', 'Dan': 'Dán', 'Hos': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós',
    'Obad': 'Abd', 'Jonah': 'Jón', 'Mic': 'Mik', 'Nah': 'Náh', 'Hab': 'Hab', 'Zeph': 'Sof',
    'Hag': 'Hag', 'Zech': 'Zak', 'Mal': 'Mal', 'Matt': 'Mt', 'Luke': 'Luk'}
OSIS_ELIRAS = {'Hosea': 'Hós', 'Is': 'Ézs', 'iKgs': '1Kir', 'Jugd': 'Bír', 'Jos': 'Józs',
               'Zp': 'Sof', 'Zec': 'Zak', 'Ho': 'Hós'}

# A forras nem lekepezett vagy tobbertelmu konyvalakjai (F38.13, a brief 2. pontja):
# alak -> a lehetseges konyvek. A valasztast a fuggetlen forras / Strong-proba adja,
# nem ez a tabla.
TOBBERTELMU = {
    'Kings': ('1Kir', '2Kir'), 'Ki': ('1Kir', '2Kir'), 'Sam': ('1Sám', '2Sám'),
    'Samuel': ('1Sám', '2Sám'), 'Chron': ('1Krón', '2Krón'), 'Chronicles': ('1Krón', '2Krón'),
    'Ze': ('Zak', 'Sof'), 'Jes': ('Ézs',), 'Esc': ('Préd',), 'De': tuple(OSZ), 'En': tuple(OSZ),
    'Ear': ('Ezsd',),
}
# ezek a forrasban nem bibliai sziglak (kommentator, Talmud, Korán, apokrif) -- a lancot
# megszakitjak, de nem csere-jeloltek
LANCTORO = {'Qor', 'Qoran', 'Gi', 'Ginsb', 'Di', 'Klo', 'Baer', 'Co', 'Aboth', 'Ab', 'Yoma',
            'Sota', 'Iliad', 'Odyssey', 'Sanh', 'Kil', 'Ter', 'Pes', 'Taan', 'Yeb', 'Ber', 'Git',
            'Ohaloth', 'Keth', 'Tariff', 'Str', 'Stu', 'Dr', 'Ryle', 'Ges', 'Che', 'Hd', 'Mez',
            'Comm', 'Gr', 'Zf', 'Gf', 'Aq', 'Or', 'Ball', 'Element'}

_BETU_NAGY = 'A-ZÀ-ÖØ-Þ'


def tsv(path):
    sorok = open(path, encoding='utf-8', newline='').read().split('\n')
    return [l.split('\t') for l in sorok if l and not l.startswith('#')]


def strong_szam(s):
    """'H0090a' / 'H90' / '0871a' -> 90 / 90 / 871 (az egesz resz)."""
    m = re.search(r'(\d+)', s or '')
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# konyvalakok
# ---------------------------------------------------------------------------

def konyv_lekepezes():
    """{forras-alak: Karoli-rovidites} -- a 11. kapu lekepezese (normalizal.py),
    csak OSZ- es UJSZ-konyvekre (apokrif nelkul)."""
    lek = {}
    for step, (rov, _) in N.KAROLI.items():
        lek[step] = rov
    for alias, step in N.FORRAS_ALIAS.items():
        if step in N.KAROLI:
            lek.setdefault(alias, N.KAROLI[step][0])
    return lek


LEK = konyv_lekepezes()
_ALAKOK = sorted(set(LEK) | set(TOBBERTELMU) | LANCTORO | set(N.APOKRIF_ALIAS), key=len, reverse=True)
# a 11. kapu forrasoldali mintaja (tapadt=True): kisbetus szohoz tapadt jelzes is talalat
TOKEN = re.compile(r'(?<![%s0-9])(%s)\.?\s+(\d{1,3}):(\d{1,3})(\d*)'
                   % (_BETU_NAGY, '|'.join(re.escape(x) for x in _ALAKOK)))
# szamjegyhez tapadt szamozott konyv (`22Chr 35:9` = 2. jelentes + 2Chr): osszeolvadt alak
TAPADT_SZAM = re.compile(r'(?<=\d)([123])(Chr|Chron|Chronicles|Kin|Ki|Sam|Kgs) (\d{1,3}):(\d{1,3})')
# ket azonos konyvu token kozott a csoportot nem szakitja meg: irasjel, szam, lancolt
# igehely es a BDB osszekoto szavai (`; compare`, `and`, `also`, `see`, `so`)
CSOPORT_KOZ = re.compile(r'(?:[\s;,.()\d:\-–+f]|compare|and|also|see|so)*')
CSUPASZ = re.compile(r'(?<![\w:.^])(\d{1,3}):(\d{1,3})(?![\d:])')


# ---------------------------------------------------------------------------
# versszamozas es Strong-index
# ---------------------------------------------------------------------------

def macula_betolt():
    """-> (versek {konyv: {fejezet: set(vers)}} MT, strongok {(konyv,c,v): set(int)} MT,
           mt2karoli {(konyv,c,v): set((konyv,c,v))})"""
    versek, strongok, mt2k = {}, {}, {}
    kdir = os.path.join(REPO, 'konkordancia')
    for fn in sorted(os.listdir(kdir)):
        if not (fn.startswith('Macula_heber_') and fn.endswith('.tsv')):
            continue
        fej = None
        for p in tsv(os.path.join(kdir, fn)):
            if fej is None:
                fej = {k: i for i, k in enumerate(p)}
                continue
            m = re.match(r'(\w+) (\d+):(\d+)', p[fej['ref']])
            if not m or m.group(1) not in MACULA_KOD:
                continue
            k, c, v = MACULA_KOD[m.group(1)], int(m.group(2)), int(m.group(3))
            versek.setdefault(k, {}).setdefault(c, set()).add(v)
            s = strong_szam(p[fej['strong_x']]) or strong_szam(p[fej['strong']])
            if s is not None:
                strongok.setdefault((k, c, v), set()).add(s)
            for kr in (p[fej['karoli']] or '').split(';'):
                mk = re.match(r'\s*(\S+) (\d+):(\d+)', kr)
                if mk:
                    mt2k.setdefault((k, c, v), set()).add((mk.group(1), int(mk.group(2)), int(mk.group(3))))
    return versek, strongok, mt2k


def tahot_betolt():
    """-> (strongok {(konyv,c,v): set(int)}, versek {konyv: {c: set(v)}})"""
    idx, versek = {}, {}
    for p in tsv(TAHOT)[1:]:
        if len(p) < 2:
            continue
        m = re.match(r'(.+) (\d+):(\d+)$', p[0])
        if not m:
            continue
        k = TAHOT_KONYV.get(m.group(1), m.group(1))
        c, v = int(m.group(2)), int(m.group(3))
        versek.setdefault(k, {}).setdefault(c, set()).add(v)
        s = strong_szam(p[1])
        if s is not None:
            idx.setdefault((k, c, v), set()).add(s)
    return idx, versek


class Bizonyitek:
    def __init__(self):
        self.mac_versek, self.mac_strong, self.mt2k = macula_betolt()
        self.tahot, self.tahot_versek = tahot_betolt()
        self._gyak = None

    def letezik(self, k, c, v):
        if k not in OSZ_SET:
            return None   # UJSZ: nem merjuk
        if c < 1 or c > FEJEZETSZAM[k] or v < 1:
            return False
        return v in self.mac_versek.get(k, {}).get(c, ()) or v in self.tahot_versek.get(k, {}).get(c, ())

    def fejezet_letezik(self, k, c):
        return k in OSZ_SET and 1 <= c <= FEJEZETSZAM[k]

    def tahot_talal(self, s, k, c, v):
        """Strong-proba (a brief 3.4): a TAHOT-ban a k c:v +-1 helyen; a hely MT-szamozasu,
        ezert a Macula MT->Karoli megfeleltetes szerinti helyen is (+-1)."""
        helyek = {(k, c, v)} | self.mt2k.get((k, c, v), set())
        for (kk, cc, vv) in helyek:
            for d in (-1, 0, 1):
                if s in self.tahot.get((kk, cc, vv + d), ()):
                    return True
        return False

    def macula_talal(self, s, k, c, v):
        for d in (-1, 0, 1):
            if s in self.mac_strong.get((k, c, v + d), ()):
                return True
        return False

    def talal(self, s, k, c, v):
        return self.tahot_talal(s, k, c, v) or self.macula_talal(s, k, c, v)

    def tahot_lefed(self, k, c, v):
        """a TAHOT-kivonat lefedi-e a helyet (fejezet-szinten; ismert rések: 1Móz 32,
        Zsolt 88/89/140/142, Jóel 3 -- CLAUDE.md)"""
        helyek = {(k, c, v)} | self.mt2k.get((k, c, v), set())
        return any(cc in self.tahot_versek.get(kk, {}) for (kk, cc, vv) in helyek)

    def proba(self, s, k, c, v):
        """A brief 3.4 Strong-probaja: TAHOT +-1 vers; ahol a TAHOT a fejezetet nem
        fedi le (ismert res), a Macula (MT) all helyette."""
        if self.tahot_lefed(k, c, v):
            return self.tahot_talal(s, k, c, v)
        return self.macula_talal(s, k, c, v)

    def esely(self, s):
        """annak eselye, hogy a Strong-szam egy veletlen 3 verses ablakban all (Macula, MT)"""
        if self._gyak is None:
            # a Macula es a TAHOT gyakorisaga kozul a nagyobbik (a TAHOT elotag-kodjai,
            # pl. H9003-H9009, a Maculaban nem allnak)
            self._gyak = []
            for idx in (self.mac_strong, self.tahot):
                g = collections.Counter()
                for st in idx.values():
                    for x in st:
                        g[x] += 1
                self._gyak.append((g, len(idx)))
        return min(1.0, max(3.0 * g.get(s, 0) / n for g, n in self._gyak))


# ---------------------------------------------------------------------------
# fuggetlen forras (OSHL BDB-XML) -- kivonat es betoltes
# ---------------------------------------------------------------------------

def kivonat(bdb_xml, lex_xml):
    import xml.etree.ElementTree as ET
    ns = '{http://openscriptures.github.com/morphhb/namespace}'
    # LexicalIndex: bdb-id -> Strong(ok)
    bdb2strong = {}
    for e in ET.parse(lex_xml).getroot().iter(ns + 'entry'):
        x = e.find(ns + 'xref')
        if x is None:
            continue
        st, bdb = x.get('strong'), x.get('bdb')
        if bdb and st and st.isdigit():
            bdb2strong.setdefault(bdb, set()).add('H%04d' % int(st))
    sorok, ismeretlen, osszes = [], collections.Counter(), 0
    for e in ET.parse(bdb_xml).getroot().iter(ns + 'entry'):
        eid = e.get('id')
        n = 0
        for r in e.iter(ns + 'ref'):
            osszes += 1
            # F46.9 (ELLENOR_F46 2.): a commitolt kivonat (4053 sor) ezzel a mintaval keszult;
            # a versresz-utotagos alak (`Gen.30.20!a`, 9 ref) kimarad, a felmeres erre epult.
            # Az utotag elfogadasa (`(?:![a-z])?`) +9 refet adna (4062 sor) -- csak uj felmeressel.
            m = re.match(r'([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)$', r.get('r') or '')
            if not m:
                ismeretlen[r.get('r')] += 1
                continue
            k = OSIS.get(m.group(1)) or OSIS_ELIRAS.get(m.group(1))
            if not k:
                ismeretlen[m.group(1)] += 1
                continue
            n += 1
            for st in sorted(bdb2strong.get(eid, {'—'})):
                sorok.append((st, eid, n, k, int(m.group(2)), int(m.group(3))))
    sorok.sort(key=lambda x: (x[0], x[1], x[2]))
    sha = hashlib.sha256(open(bdb_xml, 'rb').read()).hexdigest()
    with open(OSHL_REF, 'w', encoding='utf-8', newline='') as f:
        f.write('# GENERÁLT: eszkozok/bdb_konyv_javit.py --kivonat — kézzel nem szerkesztendő.\n')
        f.write('# forras: openscriptures/HebrewLexicon @ %s | BrownDriverBriggs.xml sha256=%s | '
                'LexicalIndex.xml (bdb-id -> Strong)\n' % (OSHL_COMMIT, sha))
        f.write('# licenc: CC BY 4.0 — Open Scriptures Hebrew Bible Project; l. adat/licencek.tsv OSHL_BDB\n')
        f.write('# konyv: a <ref r="OSIS.c.v"> attributum konyve Karoli-rovidítesre kepezve; a forrasbeli '
                'OSIS-elirasok (%s) is. sorszam: a ref sorszama a BDB-XML szocikkben (1-tol). '
                'strong=— : a bdb-id-hez nincs Strong a LexicalIndex-ben.\n'
                % ', '.join('%s->%s' % kv for kv in sorted(OSIS_ELIRAS.items())))
        f.write('\t'.join(['strong', 'bdb_id', 'sorszam', 'konyv', 'fejezet', 'vers']) + '\n')
        for s in sorok:
            f.write('\t'.join(str(x) for x in s) + '\n')
    print('BDB-XML ref:', osszes, '| kivonatolt sor:', len(sorok), '| ismeretlen r=:', dict(ismeretlen))
    print('scope=BDB-XML <ref r> igehelyek, Strong-leképezéssel | forras=openscriptures/HebrewLexicon@%s '
          'BrownDriverBriggs.xml + LexicalIndex.xml | ts=%s' % (OSHL_COMMIT, datetime.date.today().isoformat()))


def oshl_betolt():
    """-> {strong: [(bdb_id, sorszam, konyv, c, v), ...]}"""
    idx = {}
    for p in tsv(OSHL_REF)[1:]:
        idx.setdefault(p[0], []).append((p[1], int(p[2]), p[3], int(p[4]), int(p[5])))
    return idx


# ---------------------------------------------------------------------------
# forras-elemzes
# ---------------------------------------------------------------------------

class Token:
    __slots__ = ('strong', 'poz', 'alak', 'forma', 'konyvek', 'c', 'v', 'farok', 'szoveg',
                 'lanc', 'tipus_jel', 'csoport', 'lanc_poz')

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def tokenek(strong, szoveg):
    """A szocikk konyvjelolt tokenjei, a lancolt (konyv nelkuli) igehelyekkel."""
    ki = []
    spanok = []
    for m in TAPADT_SZAM.finditer(szoveg):
        forma = m.group(1) + m.group(2)
        k = LEK.get(forma) or {'1Chron': '1Krón', '2Chron': '2Krón', '1Chronicles': '1Krón',
                               '2Chronicles': '2Krón'}.get(forma)
        ki.append(Token(strong=strong, poz=m.start(), alak=m.group(0), forma=forma,
                        konyvek=(k,) if k else (), c=int(m.group(3)), v=int(m.group(4)), farok='',
                        szoveg=szoveg, lanc=[], lanc_poz=[], tipus_jel='osszeolvadt_szam'))
        spanok.append(m.span())
    for m in TOKEN.finditer(szoveg):
        if any(a <= m.start() < b for a, b in spanok):
            continue
        forma = m.group(1)
        elotte = szoveg[max(0, m.start() - 6):m.start()]
        if forma in LANCTORO or forma in N.APOKRIF_ALIAS or elotte.endswith('^') or elotte.endswith('Comm. '):
            # bibliografiai hivatkozas (`De^Job 2:598` = Delitzsch Job-kommentarja, 2. kotet
            # 598. o.; `Che^Comm. Isaiah 2:148`): nem igehely
            k = ()
            jel = 'lanctoro'
        elif forma in LEK:
            k = (LEK[forma],)
            jel = ''
        else:
            k = TOBBERTELMU[forma]
            jel = 'nem_lekepezett'
        ki.append(Token(strong=strong, poz=m.start(), alak=m.group(0), forma=forma, konyvek=k,
                        c=int(m.group(2)), v=int(m.group(3)), farok=m.group(4), szoveg=szoveg,
                        lanc=[], lanc_poz=[], tipus_jel=jel))
        spanok.append(m.span())
    ki.sort(key=lambda t: t.poz)
    # lancolt igehelyek: a kovetkezo tokenig
    for i, t in enumerate(ki):
        vege = ki[i + 1].poz if i + 1 < len(ki) else len(szoveg)
        kezd = t.poz + len(t.alak)
        for m in CSUPASZ.finditer(szoveg, kezd, vege):
            t.lanc.append((int(m.group(1)), int(m.group(2))))
            t.lanc_poz.append((m.start(), m.group(0)))
    # csoport: az egymast kozvetlenul koveto, azonos konyvre feloldott tokenek (csak
    # irasjel, szam es lancolt igehely kozottuk: `1 Samuel 3:22; 1 Samuel 5:26; 1Sam 15:22`)
    # -- a konvertalo a nyomtatott lanc minden tagjat kulon tokenne bontotta
    csoportok = []
    for i, t in enumerate(ki):
        if (i and csoportok and ki[i - 1].konyvek == t.konyvek and t.tipus_jel != 'lanctoro'
                and re.fullmatch(CSOPORT_KOZ, szoveg[ki[i - 1].poz + len(ki[i - 1].alak):t.poz])):
            csoportok[-1].append(t)
        else:
            csoportok.append([t])
    for cs in csoportok:
        for t in cs:
            t.csoport = (list(t.lanc) + [(u.c, u.v) for u in cs if u is not t]
                         + [x for u in cs if u is not t for x in u.lanc])
    return [t for t in ki if t.tipus_jel != 'lanctoro']


def kornyezet(szoveg, poz, alak, n=60):
    a = max(0, poz - n)
    b = min(len(szoveg), poz + len(alak) + n)
    return ('…' if a else '') + szoveg[a:poz] + '⟦' + alak + '⟧' + szoveg[poz + len(alak):b] + ('…' if b < len(szoveg) else '')


def karoli_alak(k, c, v):
    return '%s %d:%d' % (k, c, v)


def forras_alak_uj(t, k_uj, c_uj, v_uj):
    """A javasolt forrasbeli (angol, BDB-stilusu) alak: a 11. kapu lekepezesenek
    BDB-alakja (Gen, Exod, 1Sam, Psa ...)."""
    return '%s %d:%d' % (BDB_ALAK[k_uj], c_uj, v_uj)


# a forras uralkodo alakja konyvenkent (a csere-tabla forrasoldali uj alakja)
BDB_ALAK = {'1Móz': 'Gen', '2Móz': 'Exod', '3Móz': 'Lev', '4Móz': 'Num', '5Móz': 'Deut',
            'Józs': 'Josh', 'Bír': 'Judg', 'Ruth': 'Ruth', '1Sám': '1Sam', '2Sám': '2Sam',
            '1Kir': '1Kin', '2Kir': '2Kin', '1Krón': '1Chr', '2Krón': '2Chr', 'Ezsd': 'Ezra',
            'Neh': 'Neh', 'Eszt': 'Est', 'Jób': 'Job', 'Zsolt': 'Psa', 'Péld': 'Prov',
            'Préd': 'Eccl', 'Én': 'Song', 'Ézs': 'Isa', 'Jer': 'Jer', 'JSir': 'Lam', 'Ez': 'Ezek',
            'Dán': 'Dan', 'Hós': 'Hosea', 'Jóel': 'Joel', 'Ámós': 'Amos', 'Abd': 'Obad',
            'Jón': 'Jonah', 'Mik': 'Micah', 'Náh': 'Nahum', 'Hab': 'Hab', 'Sof': 'Zeph',
            'Hag': 'Hag', 'Zak': 'Zech', 'Mal': 'Mal'}


def f34_maradek():
    ki = set()
    if os.path.exists(F34_MARADEK):
        for p in tsv(F34_MARADEK)[1:]:
            ki.add((p[0], p[1]))
    return ki


# az arameus szakaszok (MT): itt a heber szocikk Strong-szama a TAHOT-ban nem all
# (a BDB a heber szocikkben targyalja az arameus alakot is), a proba nem szelektiv
ARAMEUS = [('Dán', (2, 4), (7, 28)), ('Ezsd', (4, 8), (6, 18)), ('Ezsd', (7, 12), (7, 26)),
           ('Jer', (10, 11), (10, 11)), ('1Móz', (31, 47), (31, 47))]
# a Strong-proba szelektivitasa: a veletlen talalat varhato szama a jelolt helyek
# kozott, E = (jelolt helyek szama) * p^(1 + lanc-talalatok), ahol p annak eselye, hogy
# a szo egy veletlen 3 verses ablakban all. A gyakori szo (H0834, H6213, H0001 ...)
# probaja onmagaban semmit nem bizonyit; a lancolt/csoportbeli helyek egyuttes talalata
# igen. Kuszob: lehetetlen helynel (a hiba biztos, csak a javitas kerdeses) 0.25; letezo
# helynel (a forrasbeli hely is lehet jo) 0.05, es lanc/csoport-tamasz is kell.
SZELEKTIV_E_LEHETETLEN = 0.25
SZELEKTIV_E_LETEZO = 0.05
# a szocikk Strong-probajanak megbizhatosaga: a forrasbeli konyvjelolesek ennyi
# reszet kell a proba igazolja, hogy a proba hianya hibajel lehessen
MEGBIZHATO = 0.5
# konyvnev, amely torzs- vagy szemelynevkent is all: angol eloljaro utan a token
# lehet `assigned to Dan [Josh] 19:41` (a konyvjeloles kiesett), ilyenkor nem cserelheto
NEVKENT_IS = {'Dan', 'Daniel', 'Ruth', 'Job', 'Joel', 'Amos', 'Jonah', 'Micah', 'Nahum', 'Ezra',
              'Esther', 'Est', 'Samuel', 'Hosea', 'Obadiah', 'Haggai', 'Malachi', 'Zechariah',
              'Nehemiah', 'Jeremiah', 'Isaiah', 'Joshua', 'Mal', 'Hag', 'Neh', 'Jer', 'Isa', 'Zech'}
HATAROZATLAN = {'De', 'En'}   # nem konyv (kommentator / ismeretlen szigla): mindig kezi


def arameus(k, c, v):
    return any(k == kk and a <= (c, v) <= b for kk, a, b in ARAMEUS)


def ertekel(t, B, oshl, megb):
    """Egy token ertekelese.
    -> None (rendben), 'igazolatlan' (a hely letezik, a proba nem igazolja, de
       hibajel sincs -- nem jelolt), vagy dict a csere-tabla mezoivel."""
    s = strong_szam(t.strong)
    xml = [r for r in oshl.get(t.strong[:5], []) if (r[3], r[4]) == (t.c, t.v)]
    xml_konyvek = sorted({r[2] for r in xml})
    egy = len(t.konyvek) == 1
    k0 = t.konyvek[0] if egy else None
    p_s = B.esely(s)

    # 1) a forrasbeli konyv igazolt-e (engedekeny: TAHOT vagy Macula vagy fuggetlen forras)
    if egy and t.tipus_jel == '' and not t.farok:
        if k0 not in OSZ_SET:
            return None   # UJSZ-hely
        if B.letezik(k0, t.c, t.v) and (B.talal(s, k0, t.c, t.v) or k0 in xml_konyvek):
            return None
    # 2) hibatipus a forrasbeli konyv szerint
    if t.tipus_jel == 'osszeolvadt_szam' or t.farok or t.v > 176:   # a leghosszabb fejezet (Zsolt 119) 176 vers
        tipus = 'osszeolvadt_alak'
    elif t.tipus_jel == 'nem_lekepezett':
        tipus = 'nem_lekepezett_alak'
    elif not B.fejezet_letezik(k0, t.c):
        tipus = 'fejezet_tullepes'
    elif not B.letezik(k0, t.c, t.v):
        tipus = 'vers_tullepes'
    else:
        tipus = 'mas_konyv_ervenyes_fejezettel'
    xml_ellentmond = bool(xml_konyvek) and k0 not in xml_konyvek
    ok = []
    if t.tipus_jel == 'osszeolvadt_szam':
        return {'tipus': tipus, 'javaslat': None, 'biz': 'kezi', 'xml': ','.join(xml_konyvek) or '—',
                'ok': 'jelentesszam tapadt a szamozott konyvhoz (%s); a konyv nem hibas, a javitas '
                      'szokoz-beszuras lenne -- konyvneven tuli OCR, nem e feladat hataskore' % t.alak}

    # 3) jeloltek
    jeloltek = []   # (k, c, v, xml, tahot, macula, lanc_t, tail)

    def jelolt(k, c, v, tail=''):
        x = (c, v) == (t.c, t.v) and any((r[2], r[3], r[4]) == (k, c, v) for r in xml)
        # ugyanabban a konyvben (szamjegy-javitas) a lanc nem tamasz: a lanc a konyvet
        # igazolja, nem a verset
        lanc_t = 0 if (egy and k == k0) else sum(
            1 for (c2, v2) in t.csoport if B.letezik(k, c2, v2) and B.talal(s, k, c2, v2))
        jeloltek.append((k, c, v, x, B.proba(s, k, c, v), B.macula_talal(s, k, c, v), lanc_t, tail))

    if tipus == 'osszeolvadt_alak':
        teljes = str(t.v) + t.farok
        for i in range(1, len(teljes)):
            v2 = int(teljes[:i])
            if B.letezik(k0, t.c, v2):
                jelolt(k0, t.c, v2, ' ' + teljes[i:])
    else:
        for k in (t.konyvek if tipus == 'nem_lekepezett_alak' else OSZ):
            if egy and k == k0:
                continue
            if B.letezik(k, t.c, t.v):
                jelolt(k, t.c, t.v)
        if tipus == 'vers_tullepes':
            # egyjegyu elteres a versben vagy a fejezetben (21:83 -> 21:33; 12:28 -> 13:28)
            for v2 in egyjegyu_valtozatok(t.v):
                if B.letezik(k0, t.c, v2):
                    jelolt(k0, t.c, v2)
            for c2 in egyjegyu_valtozatok(t.c):
                if B.letezik(k0, c2, t.v):
                    jelolt(k0, c2, t.v)
    lanc_B = (sum(1 for (c2, v2) in t.csoport if B.letezik(k0, c2, v2) and B.talal(s, k0, c2, v2))
              if egy and k0 in OSZ_SET else 0)

    n_jelolt = max(1, len(jeloltek))
    letezo = tipus == 'mas_konyv_ervenyes_fejezettel'

    def varhato(j):
        return n_jelolt * p_s ** (1 + j[6])

    def gyenge(j):
        """a talalat nem veletlen-szeru (E <= a lehetetlen helyek kuszobe)"""
        return bool(j[3] or ((j[4] or j[5]) and varhato(j) <= SZELEKTIV_E_LEHETETLEN))

    def szelektiv(j):
        if j[3]:
            return True
        if not gyenge(j):
            return False
        if letezo:
            return j[6] > lanc_B and varhato(j) <= SZELEKTIV_E_LETEZO
        return True

    def pont(j):
        return (j[3], szelektiv(j), j[4] or j[5], j[6], j[4])

    jo = sorted([j for j in jeloltek if j[3] or j[4] or j[5]], key=pont, reverse=True)

    # 4) a letezo, igazolatlan hely csak hibajellel jelolt
    if tipus == 'mas_konyv_ervenyes_fejezettel' and not xml_ellentmond:
        if arameus(k0, t.c, t.v) or megb < MEGBIZHATO:
            return 'igazolatlan'
        # jelolt: legalabb nem veletlen-szeru talalat mas konyvben; a szigoru
        # szelektivitas (lanc/csoport-tamasz) hianyaban kezi
        jo = [j for j in jo if gyenge(j)]
        if not jo:
            return 'igazolatlan'

    javaslat = None
    if jo:
        legjobb = [j for j in jo if pont(j) == pont(jo[0])]
        if len(legjobb) == 1:
            javaslat = legjobb[0]
        else:
            ok.append('tobb egyenrangu jelolt: ' + ', '.join(karoli_alak(*j[:3]) for j in legjobb[:8]))
    else:
        ok.append('nincs olyan konyv/vers, ahol a hely letezik es a Strong-proba vagy a fuggetlen forras igazolna')

    # 5) bizonyossag (a brief 3.4): fuggetlen forras egyezik + a vers letezik + Strong-proba
    if javaslat:
        n = sum([bool(javaslat[3]), True, bool(javaslat[4])])
        biz = 'magas' if n == 3 else ('kozepes' if n == 2 else 'kezi')
        if not javaslat[4] and javaslat[5]:
            ok.append('a TAHOT-proba nem sikeres, a Macula (MT) igazolja')
        if javaslat[6]:
            ok.append('a lancolt/csoportbeli helyek kozul %d/%d is ebben a konyvben igazolt (a forrasbeli konyvben %d)'
                      % (javaslat[6], len(t.csoport), lanc_B))
        if biz != 'kezi' and not gyenge(javaslat):
            ok.append('a Strong-proba nem szelektiv (a szo egy veletlen 3 verses ablakban %.0f%% esellyel all; '
                      'a veletlen talalat varhato szama %d jelolt hely kozott %.2f), fuggetlen forras nincs'
                      % (100 * p_s, n_jelolt, varhato(javaslat)))
            biz = 'kezi'
    else:
        biz = 'kezi'
    if javaslat and biz != 'kezi' and letezo and not szelektiv(javaslat):
        # a forrasbeli hely letezo hely: a mas konyvbeli talalat onmagaban nem cafolja
        # (emendacio, eltero Strong-cimke, versszamozas) -- lanc/csoport-tamasz kell
        ok.append('a forrasbeli hely is letezik; a mas konyvbeli talalat mellett nincs eleg '
                  'lanc/csoport-tamasz (E=%.2f, lanc %d, a forrasbeli konyvben %d) es fuggetlen forras'
                  % (varhato(javaslat), javaslat[6], lanc_B))
        biz = 'kezi'
    if xml_konyvek and javaslat and javaslat[0] not in xml_konyvek:
        ok.append('a fuggetlen forras mas konyvet mond: ' + ','.join(xml_konyvek))
        biz = 'kezi'
    elotte = t.szoveg[max(0, t.poz - 12):t.poz]
    if (javaslat and biz != 'kezi' and t.forma in NEVKENT_IS and javaslat[0] != k0
            and re.search(r'\b(to|of|in|by|from|with|and|as|for|son|sons|tribe|city|cities)\s+$', elotte)):
        ok.append('a(z) %r itt torzs- vagy szemelynev is lehet (elotte: %r): a csere a nevet torolne'
                  % (t.forma, elotte.strip()))
        biz = 'kezi'
    if t.forma in HATAROZATLAN:
        ok.append('a(z) %r alak valoszinuleg nem konyvnev (szigla), kezi dontes' % t.forma)
        biz = 'kezi'
    if egy and k0 in OSZ_SET and arameus(k0, t.c, t.v):
        ok.append('arameus szakasz: a heber Strong-proba itt nem szelektiv')
    return {'tipus': tipus, 'javaslat': javaslat, 'biz': biz, 'ok': '; '.join(ok),
            'xml': ','.join(xml_konyvek) or '—'}


def egyjegyu_valtozatok(v):
    s = str(v)
    ki = set()
    for i in range(len(s)):
        for d in '0123456789':
            if d != s[i]:
                ki.add(s[:i] + d + s[i + 1:])
        ki.add(s[:i] + s[i + 1:])
        if i + 1 < len(s):
            ki.add(s[:i] + s[i + 1] + s[i] + s[i + 2:])   # felcserelt szomszedos jegyek (82 -> 28)
    return sorted({int(x) for x in ki if x and not x.startswith('0')} - {v})


def megbizhatosag(B, tok):
    """{strong: a Strong-proba megbizhatosaga a szocikkben} -- azon (egyertelmu OSZ)
    konyvjelolesek aranya, amelyek c:v helyen a Strong-szam BARMELY konyvben megtalalhato.
    Ha a szocikk Strong-szama a TAHOT/Macula cimkezeseben altalaban nem all a hivatkozott
    helyeken (eltero Strong-hozzarendeles), a proba hianya nem hibajel. (A forrasbeli konyv
    hibaja itt nem rontja az aranyt, mert a helyes konyvben a talalat szamit.)"""
    ki = {}
    for st, ts in tok.items():
        s = strong_szam(st)
        n = jo = 0
        for t in ts:
            if len(t.konyvek) == 1 and t.konyvek[0] in OSZ_SET and not t.tipus_jel and not t.farok:
                n += 1
                if B.letezik(t.konyvek[0], t.c, t.v) and B.talal(s, t.konyvek[0], t.c, t.v):
                    jo += 1
                elif any(B.letezik(k, t.c, t.v) and B.talal(s, k, t.c, t.v) for k in OSZ):
                    jo += 1
        ki[st] = jo / n if n else 0.0
    return ki


# ---------------------------------------------------------------------------
# nevhiba (a brief 2. pontja): konyvnev helyen allo nevhiba, kulon listan, csak
# jovahagyassal. A nyomtatott BDB `Ph.` roviditese a fáraot (Pharaoh) es a fönicait
# (Phoenician) is jelolheti; a konvertalo mindenhol Phoenicianre oldotta. Itt csak
# az a hely jelolt, ahol a szo igei/eloljarosi szerkezetben szemelyre utal.
# ---------------------------------------------------------------------------

# a szo utan heber szoveg, nevelo (`a crash`) vagy igehely all (`with Ph. Ex 8:8`)
NEVHIBA = [(re.compile(r'\b(to|with|unto|before|name of) (Phoenician)'
                       r'(?= (?:[֐-׿]|a |(?:%s) \d))' % '|'.join(map(re.escape, BDB_ALAK.values()))),
            'Pharaoh')]
NYERS_XML = os.path.join(REPO, 'konkordancia', '_nyers', 'oshl', 'BrownDriverBriggs.xml')


def nevhiba_xml_ok(xml, st, uj):
    """A fuggetlen forras allasa egy nevhiba-jeloltrol: a SZOCIKK BDB-XML-bejegyzesei
    (Strong -> bdb-id a konkordancia/OSHL_lexikalis_index.tsv-bol) tartalmazzak-e a javitott
    szot. (F46.9, ELLENOR_F46 5.: a korabbi valtozat az egesz XML-ben kereste, es a
    `Pharaoh` a parʿoh-szocikkben all, ezert tevesen „elofordul”-t irt.)"""
    if xml is None:
        return 'a fuggetlen forras (BDB-XML) nincs a gepen, nem ellenorizheto'
    ids = []
    for l in open(os.path.join(REPO, 'konkordancia', 'OSHL_lexikalis_index.tsv'), encoding='utf-8').read().split('\n'):
        if l and not l.startswith('#'):
            p = l.split('\t')
            if p[0] == st:
                ids.append(p[3])
    if not ids:
        return ('a fuggetlen forras nem igazolja: a szocikknek nincs BDB-XML-bejegyzese (a LexicalIndex-ben '
                'nincs bdb-id); a %r szo a BDB-XML-ben csak mas szocikkekben all' % uj)
    allapot = []
    for b in ids:
        m = re.search(r'<entry id="%s"[^>]*>(.*?)</entry>' % re.escape(b), xml, re.S)
        t = m.group(1) if m else ''
        if uj in t:
            return 'a szocikk BDB-XML-bejegyzeseben (%s) a %r szo all: kezi osszevetes kell' % (b, uj)
        s_ = re.search(r'<status[^>]*>(\w+)', t)
        allapot.append('%s: %s' % (b, s_.group(1) if s_ else 'nincs'))
    return ('a fuggetlen forras nem igazolja: a szocikk BDB-XML-bejegyzeseiben (%s) a %r szo nem all '
            '(a bejegyzes kidolgozatlan vazlat); a szo a BDB-XML-ben csak mas szocikkekben fordul elo'
            % ('; '.join(allapot), uj))


def nevhibak(sorok):
    xml = open(NYERS_XML, encoding='utf-8-sig').read() if os.path.exists(NYERS_XML) else None
    ki = []
    for st, szoveg in sorok:
        for minta, uj in NEVHIBA:
            for m in minta.finditer(szoveg):
                ok = nevhiba_xml_ok(xml, st, uj)
                ki.append({
                    'strong': st, 'pozicio': str(m.start(2)), 'forras_alak': m.group(2),
                    'fuggetlen_alak': '—', 'javasolt_forras_alak': uj, 'javasolt_karoli_alak': 'fáraó',
                    'hibatipus': 'nevhiba', 'bizonyossag': 'kezi', 'lanc': '—', 'ok': ok,
                    'kornyezet': kornyezet(szoveg, m.start(2), m.group(2)),
                })
    return ki


# ---------------------------------------------------------------------------
# forditasok (adat/forditasok.tsv): a forrasbeli token Karoli-alakja a forditasban
# ---------------------------------------------------------------------------

def ford_betolt():
    """-> (sorok, fejlec, {strong: sorindex}) a BDB `teljes` forditas_hu sorokra"""
    fs = open(FORD, encoding='utf-8', newline='').read().split('\n')
    fej = fs[1].split('\t')
    ix = {}
    for i, l in enumerate(fs):
        if i < 2 or not l:
            continue
        p = dict(zip(fej, l.split('\t')))
        if p['szotar'] == 'BDB' and p['jelentes_szam'] == 'teljes' and p['mezo'] == 'forditas_hu':
            ix[p['strong']] = i
    return fs, fej, ix


def hu_regi(t):
    """a token Karoli-alakja, ahogy a forditas (hiven) atvette; None, ha a forras
    alakja nem egyertelmu konyv"""
    if t.tipus_jel == 'nem_lekepezett':
        return '%s %d:%d' % (t.forma, t.c, t.v)   # a fordito a nem lekepezett alakot betuhiven vitte at
    if len(t.konyvek) != 1 or t.tipus_jel:
        return None
    return '%s %d:%d%s' % (t.konyvek[0], t.c, t.v, t.farok)


def hu_minta(alak):
    return re.compile(r'(?<![\wÀ-ɏ])' + re.escape(alak) + r'(?![\d])')


def ford_illesztes(tok_szocikk, t, hu_szoveg):
    """-> (allapot, j): a token hanyadik elofordulasa a forditasban cserelendo.
    A forrasban azonos Karoli-alaku tokenek sorrendje = a forditasbeli elofordulasok
    sorrendje, ha a darabszam egyezik."""
    regi = hu_regi(t)
    if regi is None:
        return 'nem_egyertelmu_forrasalak', None
    azonos = [u for u in tok_szocikk if hu_regi(u) == regi]
    j = [u.poz for u in azonos].index(t.poz)
    n_ford = len(hu_minta(regi).findall(hu_szoveg))
    if n_ford != len(azonos):
        return 'nem_illesztheto (forras %d, forditas %d)' % (len(azonos), n_ford), None
    return 'illesztheto (%d/%d)' % (j + 1, len(azonos)), j


def felmeres():
    B = Bizonyitek()
    oshl = oshl_betolt()
    psi = f34_maradek()
    sorok = tsv(FORRAS)[1:]
    tok = {p[0]: tokenek(p[0], p[2]) for p in sorok}
    szov = {p[0]: p[2] for p in sorok}
    megb = megbizhatosag(B, tok)
    fs, fej, fix = ford_betolt()
    fhu = {st: dict(zip(fej, fs[i].split('\t')))['forditas_hu'] for st, i in fix.items()}
    csere, kezi = [], []
    javasolt_konyv = {}
    stat = collections.Counter()
    for st in (p[0] for p in sorok):
        szoveg = szov[st]
        for t in tok[st]:
            stat['token'] += 1
            e = ertekel(t, B, oshl, megb[st])
            if e is None:
                stat['rendben'] += 1
                continue
            if e == 'igazolatlan':
                stat['igazolatlan'] += 1
                continue
            tipus = e['tipus']
            norm = re.sub(r'\.?\s+', ' ', t.alak)
            j = e['javaslat']
            if (st, norm) in psi:
                # az N-F34 maradek sora: psi_maradek, ha a javaslat Zsolt vagy nincs javaslat;
                # kulonben a valodi tipus marad (az F34 B/R listaja nem csak psi-hibat tartalmazott)
                if not j or j[0] == 'Zsolt':
                    tipus = 'psi_maradek'
                e['ok'] = ('N-F34 maradek sora; ' + e['ok']).rstrip('; ')
            if j:
                uj_forras = '%s %d:%d%s' % (BDB_ALAK[j[0]], j[1], j[2], j[7])
                uj_karoli = karoli_alak(j[0], j[1], j[2]) + j[7]
            else:
                uj_forras = uj_karoli = '—'
            if st in fhu:
                fall, _ = ford_illesztes(tok[st], t, fhu[st])
            else:
                fall = '—'
            sor = {
                'strong': st, 'pozicio': str(t.poz), 'forras_alak': t.alak,
                'fuggetlen_alak': e['xml'], 'javasolt_forras_alak': uj_forras,
                'javasolt_karoli_alak': uj_karoli, 'hibatipus': tipus, 'bizonyossag': e['biz'],
                'lanc': ';'.join('%d:%d' % x for x in t.csoport) or '—', 'forditas': fall,
                'ok': e['ok'] or '—',
            }
            if e['biz'] == 'kezi':
                sor['kornyezet'] = kornyezet(szoveg, t.poz, t.alak)
                kezi.append(sor)
            csere.append(sor)
            if j:
                javasolt_konyv[(st, t.poz)] = j[0]
        # lancolt (konyv nelkuli) igehely, amely az orokolt konyvben nem letezik
        for t in tok[st]:
            if len(t.konyvek) != 1 or t.konyvek[0] not in OSZ_SET:
                continue
            k0 = t.konyvek[0]
            for (c, v), (lp, la) in zip(t.lanc, t.lanc_poz):
                if B.letezik(k0, c, v):
                    continue
                stat['lanc_lehetetlen'] += 1
                jk = javasolt_konyv.get((st, t.poz))
                if jk and B.letezik(jk, c, v):
                    stat['lanc_lehetetlen_tokennel_rendezodik'] += 1
                    continue
                sor = {
                    'strong': st, 'pozicio': str(lp), 'forras_alak': la, 'fuggetlen_alak': '—',
                    'javasolt_forras_alak': '—', 'javasolt_karoli_alak': '—',
                    'hibatipus': 'lanc_lehetetlen', 'bizonyossag': 'kezi', 'lanc': '—',
                    'forditas': '—' if st not in fhu else 'van forditas',
                    'ok': 'konyv nelkuli, lancolt igehely: az orokolt konyvben (%s, a %r token utan) %s nem letezik%s; '
                          'a gepi csere csak konyvjelolt tokent cserel' % (
                              k0, t.alak, 'a fejezet' if not B.fejezet_letezik(k0, c) else 'a vers',
                              ('; a token javaslata (%s) sem oldja meg' % jk) if jk else ''),
                    'kornyezet': kornyezet(szoveg, lp, la),
                }
                csere.append(sor)
                kezi.append(sor)
    for sor in nevhibak([(p[0], p[2]) for p in sorok]):
        sor['forditas'] = '—' if sor['strong'] not in fhu else (
            'van forditas (%d Fáraó/fáraó a szovegben)' % len(re.findall(r'[Ff]áraó', fhu[sor['strong']])))
        csere.append(sor)
        kezi.append(sor)
    lefedett = {(s['strong'], re.sub(r'\.?\s+', ' ', s['forras_alak'])) for s in csere}
    stat['psi_maradek_lista'] = len(psi)
    stat['psi_maradek_hianyzik'] = len([x for x in psi if x not in lefedett])
    stat['psi_maradek_lefedve'] = len(psi) - stat['psi_maradek_hianyzik']
    return csere, kezi, stat


CSERE_FEJ = ['strong', 'pozicio', 'forras_alak', 'fuggetlen_alak', 'javasolt_forras_alak',
             'javasolt_karoli_alak', 'hibatipus', 'bizonyossag', 'lanc', 'forditas', 'ok']
KEZI_FEJ = CSERE_FEJ + ['kornyezet']


def ir_tabla(path, fej, sorok, proveniencia):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write('# ' + proveniencia + '\n')
        f.write('\t'.join(fej) + '\n')
        for s in sorok:
            f.write('\t'.join(s[k].replace('\t', ' ').replace('\n', ' ') for k in fej) + '\n')


# ---------------------------------------------------------------------------
# 13. kapu a forrason (a naplok/BDB_FORDITAS_M0.py merese szerint: a konyvjelolt
# igehely fejezete nagyobb a konyv fejezetszamanal)
# ---------------------------------------------------------------------------

def fejezet_jelzes(szoveg):
    rossz = set()
    for m in TOKEN.finditer(szoveg):
        k = LEK.get(m.group(1))
        if k in FEJEZETSZAM and int(m.group(2)) > FEJEZETSZAM[k]:
            rossz.add('%s %s' % (k, m.group(2)))
    return rossz


# ---------------------------------------------------------------------------
# gepi csere (3.6) -- csak a csere-tabla jovahagyasa utan
# ---------------------------------------------------------------------------

def csere_tabla_beolvas(szintek, kulcsok=(), dontes=None):
    """a jovahagyott sorok: bizonyossag a szintek kozt, vagy a sor kulcsa
    (strong:pozicio) a kulon jovahagyott kulcsok kozt; dontes=<oszlop> eseten azok a
    sorok, amelyeknel a dontes-oszlop erteke `csere`; javaslat nelkuli sor soha"""
    sor = [l for l in open(CSERE, encoding='utf-8').read().split('\n') if l and not l.startswith('#')]
    fej = sor[0].split('\t')
    ki = []
    for l in sor[1:]:
        r = dict(zip(fej, l.split('\t')))
        if r['javasolt_forras_alak'] == '—':
            continue
        if dontes:
            if r.get(dontes) == 'csere':
                ki.append(r)
        elif r['bizonyossag'] in szintek or '%s:%s' % (r['strong'], r['pozicio']) in kulcsok:
            ki.append(r)
    return ki


# ---------------------------------------------------------------------------
# DT-F46 (felhasznalo, 2026-10-03): (1) b -- magas + a lehetetlen tipusu kozepes;
# feltetelek: a 6 MT-szamozasu javasolt Karoli-alak (H2742, H7105, H8492, H5997, H0215,
# H6778) a Macula MT->Karoli atvaltassal javitva, kulonben kezi; a gepi kapu minden
# javasolt Karoli-alak letezeset ellenorzi; a TAHOT szerint 500-nal tobbszor elofordulo
# Strong-szamok sorai kezi listara; (3) a: a harom nevhiba cserelheto (a H3117 nem).
# ---------------------------------------------------------------------------

DT_F46_MT_STRONG = {'H2742', 'H7105', 'H8492', 'H5997', 'H0215', 'H6778'}
DT_F46_NEVHIBA = {'H5973', 'H7588', 'H9005'}
DT_F46_GYAKORI = 500
LEHETETLEN_TIPUS = {'fejezet_tullepes', 'vers_tullepes', 'nem_lekepezett_alak'}
# a nevhiba a forditasban: a forditott alak (betuhiven, pontosan egyszer) -> a javitott
NEVHIBA_FORDITAS = {'H9005': ('a föníciaihoz', 'a fáraóhoz'),
                    'H5973': ('föníciai mellől', 'a fáraó mellől')}
KAROLI_VERSEK = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')


def karoli_versek():
    return {l.split('\t')[0] for l in open(KAROLI_VERSEK, encoding='utf-8').read().split('\n')[1:] if l}


def karoli_hely(alak):
    """'Jóel 3:14' / 'Hab 41:47 16' -> 'Jóel 3:14' (a konyv es az elso c:v)"""
    m = re.match(r'(\S+ \d+:\d+)', alak)
    return m.group(1) if m else None


# DT-F46 kiegeszites (2) (felhasznalo, 2026-10-03): a Karoli-letezes kapu a Strong-szam
# jelenletet is ellenorzi a javasolt Karoli-versben: TAHOT_kivonat (a Karoli_versmegfeleltetes
# `igehely_kjv` oszlopa szerinti helyen is) vagy Karoli_Strong_kivonat (STEP-alak a
# Konyv_normalizalo_tabla szerint). Ablak: 0 = pontosan a Karoli-vers (alapertek).
KAROLI_VERSMEGF = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
KAROLI_STRONG = os.path.join(REPO, 'konkordancia', 'Karoli_Strong_kivonat.tsv')
KAROLI_UT_TABLA = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
_KS = None


def _karoli_strong_index():
    global _KS
    if _KS is None:
        tah, _ = tahot_betolt()
        k2t = {}
        for p in tsv(KAROLI_VERSMEGF)[1:]:
            if len(p) > 1:
                k2t[p[0]] = p[1]
        step2hu = {p[0]: p[1] for p in tsv(KAROLI_UT_TABLA)[1:] if len(p) > 1}
        ksk = collections.defaultdict(set)
        for p in tsv(KAROLI_STRONG)[1:]:
            m = re.match(r'(\w+)\.(\d+)\.(\d+)', p[0]) if len(p) > 1 else None
            if m and m.group(1) in step2hu:
                ksk[(step2hu[m.group(1)], int(m.group(2)), int(m.group(3)))].add(strong_szam(p[1]))
        _KS = (tah, k2t, ksk)
    return _KS


def karoli_strong_van(strong, karoli_alak, ablak=0):
    """True, ha a Strong-szam a javasolt Karoli-versben (+-ablak) all; None, ha nem igehely."""
    m = re.match(r'(\S+) (\d+):(\d+)', karoli_alak or '')
    if not m:
        return None
    tah, k2t, ksk = _karoli_strong_index()
    k, c, v = m.group(1), int(m.group(2)), int(m.group(3))
    s = strong_szam(strong)
    helyek = {(k, c, v)}
    mm = re.match(r'(\d+):(\d+)$', k2t.get('%s %d:%d' % (k, c, v), ''))
    if mm:
        helyek.add((k, int(mm.group(1)), int(mm.group(2))))
    return any(s in tah.get((a, b, e + d), ()) or s in ksk.get((a, b, e + d), ())
               for (a, b, e) in helyek for d in range(-ablak, ablak + 1))


def karoli_strong_kapu_jelentes(ablak=0):
    """--karoli-strong-kapu: a teljes csere-tabla (javaslattal biro igehely-sorok) ellen; nem ir."""
    sor = [l for l in open(CSERE, encoding='utf-8').read().split('\n') if l and not l.startswith('#')]
    fej = sor[0].split('\t')
    c = collections.Counter()
    bukik = []
    for l in sor[1:]:
        r = dict(zip(fej, l.split('\t')))
        if r['javasolt_forras_alak'] == '—' or r['hibatipus'] == 'nevhiba':
            continue
        v = karoli_strong_van(r['strong'], r['javasolt_karoli_alak'], ablak)
        d = (r.get('dt_f46') or '—').split(' ')[0]
        c[(d, v)] += 1
        if not v:
            bukik.append((r['strong'], r['forras_alak'], r['javasolt_karoli_alak'], d))
    print('ablak=%d | %s' % (ablak, dict(c)))
    for b in bukik:
        print('  BUKIK:', b)
    return bukik


# DT-F46 kiegeszites 2 (felhasznalo, 2026-10-03; F46.14): a Karoli-vers Strong-kapun (ablak 0)
# nem igazolt 16 csere visszaallitva; e sorok javasolt_karoli_alak-ja azota a TAHOT szerinti
# szomszedos vers (csak javaslat, nem gepi csere-jelolt) -- ezert a kapu ujrafuttatva atengedne
# oket. Kulcs: (strong, pozicio a 3.6 elotti forrasban, forras_alak).
DT_F46_KIEG2 = {
    ('H0056', '370', '1 Samuel 3:26'), ('H0215', '1505', 'Job 42:24'), ('H2406', '823', '1 Chronicles 20:21'),
    ('H2574', '1418', 'Ezekiel 47:48'), ('H2851', '716', 'Ezekiel 26:26'), ('H4803', '982', 'Ezra 9:20'),
    ('H4908', '154', 'Ex 46:6'), ('H5019', '924', 'Ezekiel 29:30'), ('H5456', '61', 'Isaiah 44:46'),
    ('H5532', '324', 'Eccl 22:22'), ('H6622', '50', 'Genesis 40:41'), ('H6778', '171', '2 Samuel 12:40'),
    ('H7092', '474', 'Deuteronomy 15:80'), ('H7676', '3040', 'Lev 28:8'), ('H7927', '370', 'Genesis 33:47'),
    ('H8193', '1896', 'Psalm 16:14')}
DT_F46_KIEG2_OK = 'kezi (DT-F46 kiegeszites 2: a Strong a javasolt Karoli-versben nem all; visszaallitva F46.14)'


def kieg2(r):
    return any(st == r['strong'] and fa == r['forras_alak'] and (poz is None or poz == r['pozicio'])
               for st, poz, fa in DT_F46_KIEG2)


def dt_f46_szures(ir=True):
    """A csere-tabla (cserenaplo) `dt_f46` oszlopa: csere / kezi (ok) / —; a 6 Strong
    javasolt Karoli-alakja MT->Karoli atvaltva. A DT-F46 miatt kezi sorok a kezi listara.
    Idempotens (F46.17): ujrafuttatva a commitolt allapotot adja; ir=False: szarazon,
    a jelenlegi dt_f46 oszloppal veti ossze, nem ir."""
    B = Bizonyitek()
    tah = collections.Counter()
    for p in tsv(TAHOT)[1:]:
        if len(p) > 1:
            tah[strong_szam(p[1])] += 1
    kv = karoli_versek()
    nyers = open(CSERE, encoding='utf-8').read().split('\n')
    fejsor = [l for l in nyers if l.startswith('#')]
    adat = [l for l in nyers if l and not l.startswith('#')]
    fej = adat[0].split('\t')
    sorok = [dict(zip(fej, l.split('\t'))) for l in adat[1:]]
    uj_kezi = []
    stat = collections.Counter()
    elozo = {(r['strong'], r['pozicio']): r.get('dt_f46', '—') for r in sorok}
    for r in sorok:
        r['dt_f46'] = '—'
        if kieg2(r):
            r['dt_f46'] = DT_F46_KIEG2_OK
            uj_kezi.append(r)
            stat['kezi_kieg2'] += 1
            continue
        valasztott = (r['javasolt_forras_alak'] != '—' and (
            r['bizonyossag'] == 'magas'
            or (r['bizonyossag'] == 'kozepes' and r['hibatipus'] in LEHETETLEN_TIPUS)))
        if r['hibatipus'] == 'nevhiba':
            r['dt_f46'] = 'csere' if r['strong'] in DT_F46_NEVHIBA else 'kezi (DT-F46 (3): elvetve, nyelvi hasznalat)'
            stat[r['dt_f46'].split(' ')[0] + '_nevhiba'] += 1
            continue
        if r['bizonyossag'] == 'kozepes' and r['hibatipus'] == 'mas_konyv_ervenyes_fejezettel':
            r['dt_f46'] = 'kezi (DT-F46 (1) b: a letezo hely kozepes sora kezi listara)'
            uj_kezi.append(r)
            stat['kezi_mas_konyv'] += 1
            continue
        if not valasztott:
            continue
        n = tah[strong_szam(r['strong'])]
        if n > DT_F46_GYAKORI:
            r['dt_f46'] = 'kezi (DT-F46 (1): a Strong-szam a TAHOT-ban %d-szor all, > %d)' % (n, DT_F46_GYAKORI)
            uj_kezi.append(r)
            stat['kezi_gyakori'] += 1
            continue
        if r['strong'] in DT_F46_MT_STRONG and 'DT-F46: MT->Karoli' not in r['ok']:
            m = re.match(r'(\S+) (\d+):(\d+)(.*)$', r['javasolt_karoli_alak'])
            k, c, v, farok = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            kk = B.mt2k.get((k, c, v))
            if not kk or len(kk) != 1:
                r['dt_f46'] = 'kezi (DT-F46 (1): az MT->Karoli atvaltas nem egyertelmu: %s)' % (sorted(kk or []),)
                uj_kezi.append(r)
                stat['kezi_mt_atvaltas'] += 1
                continue
            (k2, c2, v2), = kk
            uj = '%s %d:%d%s' % (k2, c2, v2, farok)
            if uj != r['javasolt_karoli_alak']:
                r['ok'] = ('DT-F46: MT->Karoli %s -> %s; ' % (r['javasolt_karoli_alak'], uj) + r['ok']).rstrip('; —')
                r['javasolt_karoli_alak'] = uj
                stat['mt_atvaltva'] += 1
        if karoli_hely(r['javasolt_karoli_alak']) not in kv:
            r['dt_f46'] = 'kezi (DT-F46 (4): a javasolt Karoli-alak a Karoli-szovegben nem letezik)'
            uj_kezi.append(r)
            stat['kezi_karoli_nem_letezik'] += 1
            continue
        # a Strong-kapu bukasat a F46.6 kapu utan ervenyesitjuk (a F46.6 kapu a korabbi; ahol
        # mindketto bukik, a F46.6 indoka marad -- a commitolt allapot szerint)
        r['_strong_bukik'] = not karoli_strong_van(r['strong'], r['javasolt_karoli_alak'])
        r['dt_f46'] = 'csere'
        stat['csere'] += 1
    # kapu (F46.6, a gepi csere elotti ellenorzesbol): ugyanabban a szocikkben KULONBOZO
    # forrasalakok ugyanarra a celra (H5656: `2 Chronicles 31:33/31:39/31:43` -> 2Krón 31:3)
    # -- a szamjegy-javitas itt nem lehet helyes, kezi listara
    cel = collections.defaultdict(set)
    for r in sorok:
        if r['dt_f46'] == 'csere' and r['hibatipus'] != 'nevhiba':
            cel[(r['strong'], r['javasolt_karoli_alak'])].add(r['forras_alak'])
    for r in sorok:
        if (r['dt_f46'] == 'csere' and r['hibatipus'] != 'nevhiba'
                and len(cel[(r['strong'], r['javasolt_karoli_alak'])]) > 1):
            r['dt_f46'] = ('kezi (F46.6 kapu: a szocikkben kulonbozo forrasalakok ugyanarra a celra: %s)'
                           % ', '.join(sorted(cel[(r['strong'], r['javasolt_karoli_alak'])])))
            uj_kezi.append(r)
            stat['csere'] -= 1
            stat['kezi_azonos_cel'] += 1
    for r in sorok:
        if r['dt_f46'] == 'csere' and r.get('_strong_bukik'):
            r['dt_f46'] = 'kezi (DT-F46 kiegeszites (2): a Strong-szam a javasolt Karoli-versben nem all)'
            uj_kezi.append(r)
            stat['csere'] -= 1
            stat['kezi_karoli_strong'] += 1
        r.pop('_strong_bukik', None)
    valt = [(k, elozo[k], r['dt_f46']) for r in sorok for k in [(r['strong'], r['pozicio'])]
            if elozo[k] != r['dt_f46']]
    if not ir:
        print('DT-F46 szures (SZARAZ, nem ir):', dict(stat), '| csere-sor:',
              sum(1 for r in sorok if r['dt_f46'] == 'csere'), '| elteres a commitolt dt_f46-tol:', len(valt))
        for v in valt[:20]:
            print('  ', v)
        return stat
    fej2 = fej + ['dt_f46'] if 'dt_f46' not in fej else fej
    megj = '# cserenaplo (DT-F46): a pozicio a 3.6 elotti forrasra vonatkozik; dt_f46 = a felhasznaloi dontes alkalmazasa'
    with open(CSERE, 'w', encoding='utf-8', newline='') as f:
        for l in fejsor:
            f.write(l + '\n')
        if megj not in fejsor:
            f.write(megj + '\n')
        f.write('\t'.join(fej2) + '\n')
        for r in sorok:
            f.write('\t'.join(r.get(k, '—') for k in fej2) + '\n')
    # kezi lista: a DT-F46 miatt kezi sorok hozzafuzese (szovegkornyezettel)
    szov = {p[0]: p[2] for p in tsv(FORRAS)[1:]}
    kn = open(KEZI, encoding='utf-8').read().split('\n')
    kfej = [l for l in kn if l and not l.startswith('#')][0].split('\t')
    # a kezi lista pozicioi a 3.6 utani forrasra vonatkoznak, ezert a kulcs nem a pozicio:
    # (strong, forras_alak, javasolt_forras_alak) darabszama -- csak a hianyzot fuzzuk hozza
    meglevo = collections.Counter()
    for l in kn:
        if l and not l.startswith('#') and not l.startswith('strong\t'):
            q = dict(zip(kfej, l.split('\t')))
            meglevo[(q['strong'], q['forras_alak'], q['javasolt_forras_alak'])] += 1
    with open(KEZI, 'a', encoding='utf-8', newline='') as f:
        for r in uj_kezi:
            k = (r['strong'], r['forras_alak'], r['javasolt_forras_alak'])
            if meglevo[k] > 0:
                meglevo[k] -= 1
                continue
            r2 = dict(r)
            r2['ok'] = (r['dt_f46'] + '; ' + r['ok']).rstrip('; —')
            r2['kornyezet'] = kornyezet(szov[r['strong']], int(r['pozicio']), r['forras_alak'])
            f.write('\t'.join(r2.get(k, '—').replace('\t', ' ') for k in kfej) + '\n')
            stat['kezi_listara'] += 1
    print('DT-F46 szures:', dict(stat))
    return stat


def alkalmaz(sorok_csere, ir):
    """Mezokulcsos, poziciohoz kotott csere a forrasban es a forditasban.
    -> statisztika; ir=False eseten semmit nem ir (vetites)."""
    sorok = open(FORRAS, encoding='utf-8', newline='').read().split('\n')
    eredeti = list(sorok)
    idx = {l.split('\t')[0]: i for i, l in enumerate(sorok) if i and l}
    regi_szov = {st: sorok[i].split('\t')[2] for st, i in idx.items()}
    tok_regi = {st: tokenek(st, regi_szov[st]) for st in {r['strong'] for r in sorok_csere}}
    per = collections.defaultdict(list)
    for r in sorok_csere:
        per[r['strong']].append(r)
    stat = collections.Counter()
    # kapu (DT-F46 (4)): minden javasolt Karoli-alak letezik a Karoli-szovegben
    kv = karoli_versek()
    nem_letezo = [(r['strong'], r['javasolt_karoli_alak']) for r in sorok_csere
                  if r['hibatipus'] != 'nevhiba' and karoli_hely(r['javasolt_karoli_alak']) not in kv]
    if nem_letezo:
        print('KAROLI-KAPU BUKIK: a javasolt Karoli-alak nem letezik:', nem_letezo)
        sys.exit(7)
    strong_hiany = [(r['strong'], r['javasolt_karoli_alak']) for r in sorok_csere
                    if r['hibatipus'] != 'nevhiba' and not karoli_strong_van(r['strong'], r['javasolt_karoli_alak'])]
    if strong_hiany:
        print('KAROLI-STRONG-KAPU BUKIK: a Strong-szam a javasolt Karoli-versben nem all:', strong_hiany)
        sys.exit(7)
    stat['karoli_kapu_ellenorzott'] = len(sorok_csere)
    for st, rs in per.items():
        p = sorok[idx[st]].split('\t')
        szoveg = p[2]
        for r in sorted(rs, key=lambda r: -int(r['pozicio'])):
            i = int(r['pozicio'])
            if szoveg[i:i + len(r['forras_alak'])] != r['forras_alak']:
                print('ELTERES a poziciotol: %s %s %r' % (st, i, r['forras_alak']))
                sys.exit(2)
            szoveg = szoveg[:i] + r['javasolt_forras_alak'] + szoveg[i + len(r['forras_alak']):]
            stat['forras_csere'] += 1
        # kapu: a szoveg csak a cserelt tokenekben valtozhat
        a, b, poz = regi_szov[st], szoveg, sorted(rs, key=lambda r: int(r['pozicio']))
        maradek_a, maradek_b, eltol = [], [], 0
        e = 0
        for r in poz:
            i = int(r['pozicio'])
            maradek_a.append(a[e:i])
            maradek_b.append(b[e + eltol:i + eltol])
            eltol += len(r['javasolt_forras_alak']) - len(r['forras_alak'])
            e = i + len(r['forras_alak'])
        maradek_a.append(a[e:])
        maradek_b.append(b[e + eltol:])
        if maradek_a != maradek_b:
            print('KAPU BUKIK (nem csak az igehely-token valtozott):', st)
            sys.exit(3)
        p[2] = szoveg
        sorok[idx[st]] = '\t'.join(p)
    assert len(sorok) == len(eredeti)
    uj_szov = {st: sorok[i].split('\t')[2] for st, i in idx.items()}

    # forditasok
    fs, fej, fix = ford_betolt()
    ki_ford = list(fs)
    nem_ill = []
    for st, rs in per.items():
        if st not in fix:
            continue
        p = fs[fix[st]].split('\t')
        sor = dict(zip(fej, p))
        hu = sor['forditas_hu']
        if hashlib.sha1(regi_szov[st].encode('utf-8')).hexdigest() != sor['forras_hash']:
            print('A TAROLT forras_hash MAR ELTER a regi forrastol:', st)
            sys.exit(4)
        cserek = []
        for r in rs:
            if r['hibatipus'] == 'nevhiba':
                regi_hu, uj_hu = NEVHIBA_FORDITAS.get(st, (None, None))
                if regi_hu is None or hu.count(regi_hu) != 1:
                    nem_ill.append((st, r['forras_alak'], 'nevhiba: a forditott alak nem egyertelmu'))
                    continue
                a_ = hu.index(regi_hu)
                cserek.append((a_, a_ + len(regi_hu), uj_hu))
                continue
            t = next(u for u in tok_regi[st] if u.poz == int(r['pozicio']))
            allapot, j = ford_illesztes(tok_regi[st], t, hu)
            if j is None:
                nem_ill.append((st, r['forras_alak'], allapot))
                continue
            regi = hu_regi(t)
            m = list(hu_minta(regi).finditer(hu))[j]
            cserek.append((m.start(), m.end(), r['javasolt_karoli_alak']))
        for a_, b_, uj in sorted(cserek, reverse=True):
            hu = hu[:a_] + uj + hu[b_:]
            stat['forditas_csere'] += 1
        p[fej.index('forditas_hu')] = hu
        p[fej.index('forras_hash')] = hashlib.sha1(uj_szov[st].encode('utf-8')).hexdigest()
        ki_ford[fix[st]] = '\t'.join(p)
        stat['forditas_sor'] += 1
    stat['forditas_nem_illesztheto'] = len(nem_ill)
    stat['13_kapu_forras_elotte'] = sum(1 for st in regi_szov if fejezet_jelzes(regi_szov[st]))
    stat['13_kapu_forras_utana'] = sum(1 for st in uj_szov if fejezet_jelzes(uj_szov[st]))
    stat['erintett_szocikk_forras'] = len(per)
    for x in nem_ill:
        print('nem illesztheto a forditasban:', x)
    if ir:
        open(FORRAS, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
        open(FORD, 'w', encoding='utf-8', newline='').write('\n'.join(ki_ford))
        print('IRVA; forras sha256:', hashlib.sha256(open(FORRAS, 'rb').read()).hexdigest())
        stat['kezi_pozicio_eltolva'] = kezi_eltolas(per, uj_szov)
    return stat


def kezi_eltolas(per, uj_szov):
    """A kezi lista (nyitott tetel) pozicioi az uj forrasra: a szocikkben elotte
    vegrehajtott cserek hosszkulonbsegevel tolva; utana a pozicion a forras_alak all."""
    nyers = open(KEZI, encoding='utf-8').read().split('\n')
    fej = [l for l in nyers if l and not l.startswith('#')][0].split('\t')
    n = 0
    for i, l in enumerate(nyers):
        if not l or l.startswith('#') or l.startswith('strong\t'):
            continue
        r = dict(zip(fej, l.split('\t')))
        if r['strong'] not in per:
            continue
        if any(c['pozicio'] == r['pozicio'] and c['forras_alak'] == r['forras_alak'] for c in per[r['strong']]):
            nyers[i] = None   # jovahagyassal cserelodott (DT-F46 (3) nevhiba): lekerul a kezi listarol
            continue
        poz = int(r['pozicio'])
        d = sum(len(c['javasolt_forras_alak']) - len(c['forras_alak'])
                for c in per[r['strong']] if int(c['pozicio']) < poz)
        if d:
            r['pozicio'] = str(poz + d)
            n += 1
        if uj_szov[r['strong']][int(r['pozicio']):int(r['pozicio']) + len(r['forras_alak'])] != r['forras_alak']:
            print('KEZI-ELTOLAS HIBA:', r['strong'], poz, r['forras_alak'])
            sys.exit(8)
        nyers[i] = '\t'.join(r[k] for k in fej)
    open(KEZI, 'w', encoding='utf-8', newline='').write('\n'.join(x for x in nyers if x is not None))
    return n


def main():
    if '--kivonat' in sys.argv:
        i = sys.argv.index('--kivonat')
        kivonat(sys.argv[i + 1], sys.argv[i + 2])
        return
    ismert = {'--kivonat', '--ir', '--vetit', '--dt-f46', '--dt-f46-szures', '--jovahagyva', '--szintek',
              '--kulcsok', '--kezi-eltolas-dt-f46', '--karoli-strong-kapu', '--ablak', '--szaraz'}
    ismeretlen = [a for a in sys.argv[1:] if a.startswith('--') and a not in ismert]
    if ismeretlen:
        # ne fusson le helyette a felmeres: az felulirna a cserenaplot es a kezi listat
        print('ismeretlen kapcsolo:', ismeretlen)
        sys.exit(2)
    if '--karoli-strong-kapu' in sys.argv:
        i = sys.argv.index('--ablak') if '--ablak' in sys.argv else None
        karoli_strong_kapu_jelentes(int(sys.argv[i + 1]) if i else 0)
        return
    if '--kezi-eltolas-dt-f46' in sys.argv:
        # a 3.6 utolso lepese kulon is futtathato (az uj forrason)
        per = collections.defaultdict(list)
        for r in csere_tabla_beolvas(set(), (), 'dt_f46'):
            per[r['strong']].append(r)
        uj_szov = {p[0]: p[2] for p in tsv(FORRAS)[1:]}
        print('kezi lista: eltolt pozicio:', kezi_eltolas(per, uj_szov))
        return
    if '--dt-f46-szures' in sys.argv:
        dt_f46_szures(ir='--szaraz' not in sys.argv)
        return
    if '--ir' in sys.argv or '--vetit' in sys.argv:
        i = sys.argv.index('--szintek') if '--szintek' in sys.argv else None
        szintek = set(sys.argv[i + 1].split(',')) if i else {'magas'}
        k = sys.argv.index('--kulcsok') if '--kulcsok' in sys.argv else None
        kulcsok = set(open(sys.argv[k + 1], encoding='utf-8').read().split()) if k else set()
        ir = '--ir' in sys.argv
        if ir and '--jovahagyva' not in sys.argv:
            print('A gepi csere (3.6) csak a csere-tabla jovahagyasa utan futhat (--jovahagyva <DT-tetel>).')
            sys.exit(9)
        dontes = 'dt_f46' if '--dt-f46' in sys.argv else None
        stat = alkalmaz(csere_tabla_beolvas(szintek, kulcsok, dontes), ir)
        print('szintek:', sorted(szintek), '| kulon kulcs:', len(kulcsok), '|', dict(stat))
        return
    csere, kezi, stat = felmeres()
    n = stat['token']
    prov = ('scope=BDB_teljes_unabridged.tsv minden könyvjelölt igehely-tokene (%d) | forras=%s + %s + '
            'TAHOT_kivonat.tsv (+-1 vers) + Macula_heber_*.tsv (MT) | ts=%s'
            % (n, 'konkordancia/BDB_teljes_unabridged.tsv', 'konkordancia/OSHL_BDB_igehelyek.tsv',
               datetime.date.today().isoformat()))
    ir_tabla(CSERE, CSERE_FEJ, csere, prov)
    ir_tabla(KEZI, KEZI_FEJ, kezi, prov)
    c = collections.Counter((s['hibatipus'], s['bizonyossag']) for s in csere)
    print('tokenek:', n, '| csere-tabla sor:', len(csere), '| kezi:', len(kezi))
    for k in sorted(c):
        print('  %-32s %-8s %d' % (k[0], k[1], c[k]))
    print('erintett szocikk:', len({s['strong'] for s in csere}))
    fc = collections.Counter((s['bizonyossag'], s['forditas'].split(' ')[0]) for s in csere if s['forditas'] != '—')
    print('forditasban:', dict(fc), '| erintett forditott szocikk:',
          len({s['strong'] for s in csere if s['forditas'] != '—'}))
    print('statisztika:', dict(stat))
    print(prov)


if __name__ == '__main__':
    main()
