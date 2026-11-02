"""F149 — tanulmány-regiszter és vers → tanulmány-szakasz index (generált kimenet).

A kész tanulmányok (genezis/, ujszovetseg/, melyelemzesek/) tartományát a fájl
első címsorából nyeri ki, és a fájlnévvel veti össze (DT-F149a (c)): ha a kettő
nem egyezik, a tanulmány NEM kerül a regiszterbe, a kimenet megnevezi
(üres eredmény jobb, mint hibás horgony). A szakaszonkénti igehely-hivatkozások
két fokozatot kapnak (DT-F149b): `nev` (egyedi vers) és `tartomany` (a szakasz
egy tartományt említ). A tanulmány forrása nem változik, semmi nem íródik vissza
(DT28); a kimenet a `pardes.db`-be épül (`sqlite_epit.py`), nem az `adat/`-ba.

A `tartomany_cimsorbol` és a `kinyer` a #124 számára is hívható (közös döntés,
DT-F149a).

Használat: python eszkozok/tanulmany_regiszter.py   (összegzés és figyelmeztetések)
"""
import glob
import os
import re
import sys
import unicodedata
from collections import namedtuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (könyvtár, minta, típus, azonosító-végződés)
FORRASOK = (
    ('genezis', '*_bovitett.md', 'bovitett', '_bovitett'),
    ('ujszovetseg', '*_bovitett.md', 'bovitett', '_bovitett'),
    ('melyelemzesek', '*_melyelemzes.md', 'melyelemzes', '_melyelemzes'),
)

# A könyvtár-alapú összevetés tipikus hosszú könyvnevei (a normalizáló táblán kívül).
HOSSZU_ALIAS = {
    '1mozes': '1Móz', '2mozes': '2Móz', '3mozes': '3Móz', '4mozes': '4Móz', '5mozes': '5Móz',
    'zsoltarok': 'Zsolt', 'zsidok': 'Zsid', 'roma': 'Róm', 'romaiak': 'Róm', 'rom': 'Róm',
    'moz': None,
}

Tanulmany = namedtuple('Tanulmany', 'tanulmany_id fajl tipus cim tartomany_szoveg sorrend')
Tartomany = namedtuple('Tartomany', 'tanulmany_id resz kezdo veg kezdo_sorrend veg_sorrend')
Hivatkozas = namedtuple('Hivatkozas', 'tanulmany_id szakasz_horgony szakasz_cim igehely fokozat hivatkozas tartomanyban')
Eredmeny = namedtuple('Eredmeny', 'tanulmanyok tartomanyok hivatkozasok figyelmeztetesek kihagyott szovegek')


def strip(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def olvas_tsv(p):
    with open(p, encoding='utf-8') as f:
        return [l.rstrip('\r\n').split('\t') for l in f]


class Karoli(object):
    """Károli-versek sorrendje és a könyvnév-normalizálás."""

    def __init__(self, kulcsok, gyoker=GYOKER, tabla_sorok=None):
        """`tabla_sorok`: a Konyv_normalizalo_tabla sorai (STEP-kód, magyar rövidítés, teljes név, forrás-alakok); hiányában a fájl."""
        self.lista = list(kulcsok)
        self.poz = {}
        self.konyv_versei = {}
        for i, k in enumerate(self.lista):
            m = re.match(r'^(\S+) (\d+):(\d+)$', k)
            if not m:
                raise ValueError('nem egy Károli-vers: %r' % k)
            kk, f, v = m.group(1), int(m.group(2)), int(m.group(3))
            self.poz[(kk, f, v)] = i
            self.konyv_versei.setdefault(kk, []).append((f, v, i))
        self.alias = {}
        if tabla_sorok is None:
            tabla_sorok = olvas_tsv(os.path.join(gyoker, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'))[1:]
        for r in tabla_sorok:
            if len(r) >= 2 and r[1]:
                self.alias[strip(r[1])] = r[1]
                if len(r) >= 4:
                    for a in r[3].split(','):
                        if a.strip():
                            self.alias[strip(a.strip())] = r[1]
        for a, k in HOSSZU_ALIAS.items():
            if k:
                self.alias[a] = k
        # a tábla első oszlopa a STEP-rövidítés; a magyar a másodiké — a fenti ciklus az elsőt is felveszi,
        # ezért a magyar rövidítéseket a Károli-kulcsok könyvneveiből egészítjük ki
        for kk in self.konyv_versei:
            self.alias[strip(kk)] = kk
        for r in tabla_sorok:
            if len(r) >= 3 and r[2]:                 # teljes magyar könyvnév: „Zsidókhoz írt levél”
                self.alias[strip(r[2])] = r[1]

    def konyv(self, nev):
        n = strip(nev.rstrip('.'))
        k = self.alias.get(n) or self.alias.get(n.replace(' ', ''))
        return k if k in self.konyv_versei else None

    def vers_kulcs(self, konyv, f, v):
        i = self.poz.get((konyv, f, v))
        return None if i is None else self.lista[i]

    def fejezet_vegek(self, konyv, f):
        vs = [x for x in self.konyv_versei.get(konyv, []) if x[0] == f]
        if not vs:
            return None
        return vs[0], vs[-1]


# --------------------------------------------------------------------------
# tartomány a címsorból és a fájlnévből
# --------------------------------------------------------------------------

SZEGMENS_RE = re.compile(
    r'^(?P<k>\d?\s?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+(?:\s[a-záéíóöőúüű]+)*)\s+(?P<f1>\d+)(?::(?P<v1>\d+))?'
    r'(?:\s?[–-]\s?(?:(?P<f2>\d+):)?(?P<v2>\d+))?\s*$')


def tartomany_cimsorbol(cimsor, kar):
    """'# 1Mózes 14:18-20 / Zsoltárok 110:4 / Zsidók 5-7 — Mélyelemzés' ->
    [(konyv, (f1, v1), (f2, v2)), ...] vagy None, ha nem értelmezhető.
    A vég (f2, v2) a Károli szerinti tényleges utolsó vers (egész fejezetnél is)."""
    t = cimsor.lstrip('#').strip()
    t = re.split(r'\s[—–]\s(?=\D)', t, maxsplit=1)[0]
    ki = []
    for seg in t.split(' / '):
        m = SZEGMENS_RE.match(seg.strip())
        if not m:
            return None
        konyv = kar.konyv(m.group('k'))
        if not konyv:
            return None
        f1 = int(m.group('f1'))
        if m.group('v1') is None:                    # egész fejezet(ek): '5-7' vagy '14'
            f_utolso = int(m.group('v2')) if m.group('v2') else f1
            a = kar.fejezet_vegek(konyv, f1)
            b = kar.fejezet_vegek(konyv, f_utolso)
            if not a or not b:
                return None
            ki.append((konyv, (f1, a[0][1]), (f_utolso, b[1][1])))
            continue
        v1 = int(m.group('v1'))
        if m.group('v2') is None:
            ki.append((konyv, (f1, v1), (f1, v1)))
        else:
            f2 = int(m.group('f2')) if m.group('f2') else f1
            ki.append((konyv, (f1, v1), (f2, int(m.group('v2')))))
    for konyv, kez, veg in ki:
        if (konyv, kez[0], kez[1]) not in kar.poz or (konyv, veg[0], veg[1]) not in kar.poz:
            return None
        if kar.poz[(konyv, kez[0], kez[1])] > kar.poz[(konyv, veg[0], veg[1])]:
            return None
    return ki


def fajlnev_jegyei(stem, kar):
    """A fájlnév (azonosító) könyvei és számai a címsorral való összevetéshez:
    ([könyv, ...], [szám, ...]); a könyvszám-előtag (1Móz) a könyvhöz tartozik."""
    konyvek, szamok = [], []
    for m in re.finditer(r'(\d?)([A-Za-z]{3,})(?=[_\d]|$)', stem):
        k = kar.konyv(m.group(1) + m.group(2))
        if k:
            konyvek.append(k)
    maradek = re.sub(r'\d?[A-Za-z]{3,}', ' ', stem)
    for m in re.finditer(r'\d+', maradek):
        szamok.append(int(m.group()))
    return konyvek, szamok


def tartomany_fajlnevbol(tid, kar):
    """Bővített fájlnév-minta (`1Moz_4v25-5v32`, `1Moz_14`, `Rom_8v10`) -> [(könyv, kezdő, vég)] vagy None."""
    m = re.match(r'^(\d?[A-Za-z]+)_(\d+)(?:v(\d+))?(?:-(?:(\d+)v)?(\d+))?$', tid)
    if not m:
        return None
    konyv = kar.konyv(m.group(1))
    if not konyv:
        return None
    f1 = int(m.group(2))
    if m.group(3) is None:
        a = kar.fejezet_vegek(konyv, f1)
        return [(konyv, (f1, a[0][1]), (f1, a[1][1]))] if a else None
    v1 = int(m.group(3))
    if m.group(5) is None:
        return [(konyv, (f1, v1), (f1, v1))]
    f2 = int(m.group(4)) if m.group(4) else f1
    return [(konyv, (f1, v1), (f2, int(m.group(5))))]


def cimsor_jegyei(cimsor, kar):
    t = re.split(r'\s[—–]\s(?=\D)', cimsor.lstrip('#').strip(), maxsplit=1)[0]
    konyvek, szamok = [], []
    for seg in t.split(' / '):
        m = re.match(r'^(\d?)\s?([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+)\s+(.*)$', seg.strip())
        if not m:
            return None
        k = kar.konyv(m.group(1) + m.group(2))
        if not k:
            return None
        konyvek.append(k)
        szamok += [int(x) for x in re.findall(r'\d+', m.group(3))]
    return konyvek, szamok


# --------------------------------------------------------------------------
# igehely-hivatkozások a szövegből
# --------------------------------------------------------------------------

KONYV_RE = r'(?:[123]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+\.?'
REF_RE = re.compile(
    r'(?:(?P<k>' + KONYV_RE + r')\s+)?(?<![\d:])(?P<f>\d{1,3}):(?P<v>\d{1,3})(?![\d:])'
    r'(?:\s?[–-]\s?(?:(?P<f2>\d{1,3}):)?(?P<v2>\d{1,3})(?![\d:]))?'
    r'(?P<lista>(?:\s?,\s?\d{1,3}(?![\d:])(?:\s?[–-]\s?\d{1,3}(?![\d:]))?)*)')
VERS_RE = re.compile(
    r'(?<![\d:])(?P<l>\d{1,3}(?:\s?[–-]\s?\d{1,3})?(?:\s?[,;]\s?\d{1,3}(?:\s?[–-]\s?\d{1,3})?)*)\.\s?v\.')
SZAM_TARTOMANY_RE = re.compile(r'(\d{1,3})(?:\s?[–-]\s?(\d{1,3}))?')


def _vers_eleme(kar, konyv, f, v1, v2):
    """(kulcsok, tartomany_e)"""
    a = kar.poz.get((konyv, f, v1))
    b = kar.poz.get((konyv, f, v2))
    if a is None or b is None or b < a or b - a > 200:
        return []
    return kar.lista[a:b + 1]


def _fokozat(lo, hi):
    return 'nev' if lo == hi else 'tartomany'


def talalatok(bek, alap_konyv, egy_fejezet, kar):
    """Egy bekezdés (vagy szövegrész) igehely-hivatkozásai pozícióval: [(kezdet, vég, [(kulcs, fokozat)], hivatkozas_szoveg)].
    A könyv a bekezdés elején alaphelyzetbe áll; a „3. v.” és a táblázat első cellája csak egyfejezetes tanulmányban (`egy_fejezet`)
    oldható fel. Az index (`hivatkozasok_szovegbol`) és a tanulmány-oldal hivatkozásai ugyanezt a függvényt használják."""
    ki = []
    akt = alap_konyv
    for m in REF_RE.finditer(bek):
        if m.group('k'):
            k = kar.konyv(m.group('k'))
            if k:
                akt = k
            elif re.match(r'^[A-ZÁÉÍÓÖŐÚÜŰ]', m.group('k')):
                pass            # ismeretlen szó (pl. mondatkezdő) a szám előtt: a jelenlegi könyvön értjük
            else:
                continue
        f, v = int(m.group('f')), int(m.group('v'))
        ref = m.group(0).strip()
        kulcsok = []
        if m.group('v2'):
            f2 = int(m.group('f2')) if m.group('f2') else f
            a = kar.poz.get((akt, f, v))
            b = kar.poz.get((akt, f2, int(m.group('v2'))))
            if a is not None and b is not None and a <= b <= a + 200:
                kulcsok = [(kk, 'tartomany') for kk in kar.lista[a:b + 1]]
        else:
            kk = kar.vers_kulcs(akt, f, v)
            if kk:
                kulcsok.append((kk, 'nev'))
            for x in SZAM_TARTOMANY_RE.finditer(m.group('lista') or ''):
                lo = int(x.group(1))
                hi = int(x.group(2)) if x.group(2) else lo
                kulcsok += [(kk2, _fokozat(lo, hi)) for kk2 in _vers_eleme(kar, akt, f, lo, hi)]
        if kulcsok:
            ki.append((m.start(), m.end(), kulcsok, ref))
    if egy_fejezet:
        konyv, f = egy_fejezet
        for m in VERS_RE.finditer(bek):
            kulcsok = []
            for x in SZAM_TARTOMANY_RE.finditer(m.group('l')):
                lo = int(x.group(1))
                hi = int(x.group(2)) if x.group(2) else lo
                kulcsok += [(kk, _fokozat(lo, hi)) for kk in _vers_eleme(kar, konyv, f, lo, hi)]
            if kulcsok:
                ki.append((m.start(), m.end(), kulcsok, m.group(0).strip()))
        for m in re.finditer(r'^\|\s*\**(\d{1,3})(?:\s?[–-]\s?(\d{1,3}))?\**\s*\|', bek, re.M):
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            kulcsok = [(kk, _fokozat(lo, hi)) for kk in _vers_eleme(kar, konyv, f, lo, hi)]
            if kulcsok:
                ki.append((m.start(), m.end(), kulcsok, m.group(0).strip('| ').strip()))
    ki.sort(key=lambda x: x[0])
    return ki


def hivatkozasok_szovegbol(szoveg, alap_konyv, egy_fejezet, kar):
    """[(kulcs, fokozat, hivatkozas_szoveg)] — bekezdésenként (üres sorral elválasztva) a könyv alaphelyzetbe áll."""
    ki = []
    for bek in re.split(r'\n\s*\n', szoveg):
        for _, _, kulcsok, ref in talalatok(bek, alap_konyv, egy_fejezet, kar):
            ki += [(kk, fok, ref) for kk, fok in kulcsok]
    return ki


# --------------------------------------------------------------------------
# szakaszok és horgonyok
# --------------------------------------------------------------------------

def slug(cim):
    s = strip(re.sub(r'[*_`]', '', cim))
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:48] or 'szakasz'


def szakaszok(szoveg):
    """[(horgony, cim, szoveg)] — a `##`/`###` címsorok szerint; a bevezető rész horgonya `eleje`.
    A horgony egyedi a fájlon belül (ismétlődő címnél -2, -3 …); a /tanulmany/<id> oldal ugyanezt használja."""
    ki, cim, buf, hasznalt = [], None, [], {}

    def zar():
        if cim is None:
            if ''.join(buf).strip():
                ki.append(('eleje', 'A tanulmány eleje', '\n'.join(buf)))
            return
        s = slug(cim)
        hasznalt[s] = hasznalt.get(s, 0) + 1
        h = s if hasznalt[s] == 1 else '%s-%d' % (s, hasznalt[s])
        ki.append((h, cim, '\n'.join(buf)))
    for sor in szoveg.split('\n'):
        m = re.match(r'^(#{2,3}) (.*)$', sor)
        if m:
            zar()
            cim, buf = m.group(2).strip(), []
        else:
            buf.append(sor)
    zar()
    return ki


def elso_cimsor(szoveg):
    for sor in szoveg.split('\n'):
        if sor.startswith('# '):
            return sor.strip()
    return None


# --------------------------------------------------------------------------
# a kinyerő
# --------------------------------------------------------------------------

def kinyer(gyoker, karoli_kulcsok):
    """-> Eredmeny. A kihagyott: [(fajl, ok)] — nem kerül a regiszterbe (DT-F149a)."""
    kar = Karoli(karoli_kulcsok, gyoker)
    tanulmanyok, tartomanyok, hivatkozasok, fig, kihagyott, szovegek = [], [], [], [], [], []
    nyers = []
    for konyvtar, minta, tipus, vegzodes in FORRASOK:
        for p in sorted(glob.glob(os.path.join(gyoker, konyvtar, minta))):
            rel = konyvtar + '/' + os.path.basename(p)
            tid = os.path.basename(p)[:-3]
            if tid.endswith(vegzodes):
                tid = tid[:-len(vegzodes)]
            with open(p, encoding='utf-8') as f:
                szoveg = f.read()
            cs = elso_cimsor(szoveg)
            if not cs:
                kihagyott.append((rel, 'nincs első címsor'))
                continue
            tart = tartomany_cimsorbol(cs, kar)
            if not tart:
                kihagyott.append((rel, 'a címsor tartománya nem értelmezhető: %s' % cs))
                continue
            ft = tartomany_fajlnevbol(tid, kar)
            if ft is not None:
                egyezik = (ft == tart)
            else:                                      # több tartományos név: a könyvek és a számok sora
                fk, fsz = fajlnev_jegyei(tid, kar)
                ck = cimsor_jegyei(cs, kar)
                egyezik = ck is not None and fk == ck[0] and fsz == ck[1]
            if not egyezik:
                kihagyott.append((rel, 'a fájlnév (%s) és a címsor (%s) tartománya nem egyezik' % (tid, cs)))
                continue
            nyers.append((rel, tid, tipus, cs, tart, szoveg))

    def kez_sorrend(x):
        k, a, _ = x[4][0]
        return kar.poz[(k, a[0], a[1])]
    nyers.sort(key=kez_sorrend)
    for sorrend, (rel, tid, tipus, cs, tart, szoveg) in enumerate(nyers):
        cim = re.split(r'\s[—–]\s(?=\D)', cs.lstrip('#').strip(), maxsplit=1)
        cim = cim[1].strip() if len(cim) > 1 else cs.lstrip('#').strip()
        szoveg_t = ' / '.join(_tart_szoveg(t) for t in tart)
        tanulmanyok.append(Tanulmany(tid, rel, tipus, cim, szoveg_t, sorrend))
        szovegek.append((tid, szoveg))
        halmaz = set()
        for i, (k, kez, veg) in enumerate(tart):
            a, b = kar.poz[(k, kez[0], kez[1])], kar.poz[(k, veg[0], veg[1])]
            tartomanyok.append(Tartomany(tid, i + 1, kar.lista[a], kar.lista[b], a, b))
            halmaz.update(range(a, b + 1))
        fejezetek = {(k, f) for (k, kez, veg) in tart for f in range(kez[0], veg[0] + 1)}
        egy = next(iter(fejezetek)) if len(fejezetek) == 1 else None
        alap = tart[0][0]
        for horgony, szcim, sz in szakaszok(szoveg):
            if horgony == 'eleje' or re.match(r'^0\.', szcim):
                continue        # fejléc-blokk és sorozat-kontextus: a sorozat navigációja, nem a vers tárgyalása
            talalt = {}
            lista = hivatkozasok_szovegbol(sz, alap, egy, kar)
            ref_versei = {}
            for kk, fokozat, ref in lista:
                if fokozat == 'tartomany':
                    ref_versei.setdefault(ref, set()).add(kar.poz[_kulcs_hely(kk)])
            for kk, fokozat, ref in lista:
                if fokozat == 'tartomany':
                    if ref_versei[ref] == halmaz:
                        continue    # a tanulmány a saját teljes tartományát nevezi meg: nem új információ
                    if kar.poz[_kulcs_hely(kk)] not in halmaz:
                        continue    # tartomány-említés a tartományon kívül nem „tárgyalás” (DT-F149b)
                elozo = talalt.get(kk)
                if elozo is None or (elozo[0] == 'tartomany' and fokozat == 'nev'):
                    talalt[kk] = (fokozat, ref)
            for kk in sorted(talalt, key=lambda x: kar.poz[_kulcs_hely(x)]):
                fokozat, ref = talalt[kk]
                hivatkozasok.append(Hivatkozas(tid, horgony, szcim, kk, fokozat, ref,
                                               1 if kar.poz[_kulcs_hely(kk)] in halmaz else 0))
    fig += sorozat_ellenorzes(tanulmanyok, tartomanyok, kar)
    return Eredmeny(tanulmanyok, tartomanyok, hivatkozasok, fig, kihagyott, szovegek)


def _kulcs_hely(kulcs):
    m = re.match(r'^(\S+) (\d+):(\d+)$', kulcs)
    return (m.group(1), int(m.group(2)), int(m.group(3)))


def _tart_szoveg(t):
    k, kez, veg = t
    if kez == veg:
        return '%s %d:%d' % (k, kez[0], kez[1])
    if kez[0] == veg[0]:
        return '%s %d:%d–%d' % (k, kez[0], kez[1], veg[1])
    return '%s %d:%d–%d:%d' % (k, kez[0], kez[1], veg[0], veg[1])


def sorozat_ellenorzes(tanulmanyok, tartomanyok, kar):
    """Könyvenként a bővített sorozat hézagai és átfedései — figyelmeztetés, nem hiba."""
    fig = []
    tip = {t.tanulmany_id: t for t in tanulmanyok}
    per_konyv = {}
    for r in tartomanyok:
        if tip[r.tanulmany_id].tipus != 'bovitett':
            continue
        konyv = r.kezdo.split(' ')[0]
        per_konyv.setdefault(konyv, []).append(r)
    for konyv, rs in sorted(per_konyv.items()):
        rs.sort(key=lambda r: r.kezdo_sorrend)
        for a, b in zip(rs, rs[1:]):
            if b.kezdo_sorrend <= a.veg_sorrend:
                fig.append('átfedés (%s): %s ↔ %s' % (konyv, a.tanulmany_id, b.tanulmany_id))
            elif b.kezdo_sorrend > a.veg_sorrend + 1:
                n = b.kezdo_sorrend - a.veg_sorrend - 1
                fig.append('hézag (%s): %s – %s (%d vers) a %s és a %s között' % (
                    konyv, kar.lista[a.veg_sorrend + 1], kar.lista[b.kezdo_sorrend - 1], n,
                    a.tanulmany_id, b.tanulmany_id))
    return fig


def tablak(e):
    """A `pardes.db` három táblája: [(név, [(oszlop, típus)], sorok, [index])]. A `sqlite_epit.py` és a
    manifest-készítő ugyanezt használja (egy forrás a sémának)."""
    return [
        ('tanulmany',
         [('tanulmany_id', 'TEXT'), ('fajl', 'TEXT'), ('tipus', 'TEXT'), ('cim', 'TEXT'),
          ('tartomany', 'TEXT'), ('sorrend', 'INTEGER')],
         [tuple(t) for t in e.tanulmanyok], ['tanulmany_id']),
        ('tanulmany_tartomany',
         [('tanulmany_id', 'TEXT'), ('resz', 'INTEGER'), ('kezdo', 'TEXT'), ('veg', 'TEXT'),
          ('kezdo_sorrend', 'INTEGER'), ('veg_sorrend', 'INTEGER')],
         [tuple(t) for t in e.tartomanyok], ['kezdo_sorrend, veg_sorrend', 'tanulmany_id']),
        ('tanulmany_hivatkozas',
         [('tanulmany_id', 'TEXT'), ('szakasz_horgony', 'TEXT'), ('szakasz_cim', 'TEXT'), ('igehely', 'TEXT'),
          ('fokozat', 'TEXT'), ('hivatkozas', 'TEXT'), ('tartomanyban', 'INTEGER')],
         [tuple(t) for t in e.hivatkozasok], ['igehely', 'tanulmany_id, szakasz_horgony']),
        # a /tanulmany/<id> oldal forrása: a szerver csak a pardes.db-t látja; a szöveg a kézi forrás változatlan másolata (nézet, nem szerkeszthető)
        ('tanulmany_szoveg', [('tanulmany_id', 'TEXT'), ('szoveg', 'TEXT')], [tuple(t) for t in e.szovegek], ['tanulmany_id']),
    ]


def karoli_kulcsok(gyoker=GYOKER):
    return [r[0] for r in olvas_tsv(os.path.join(gyoker, 'konkordancia', 'Karoli_1908.tsv'))[1:] if r and r[0]]


def main():
    e = kinyer(GYOKER, karoli_kulcsok())
    print('tanulmány: %d, tartomány-sor: %d, hivatkozás-sor: %d' % (
        len(e.tanulmanyok), len(e.tartomanyok), len(e.hivatkozasok)))
    for t in e.tanulmanyok:
        print('  %-22s %-12s %s' % (t.tanulmany_id, t.tipus, t.tartomany_szoveg))
    for f, ok in e.kihagyott:
        print('KIHAGYVA: %s — %s' % (f, ok))
    for f in e.figyelmeztetesek:
        print('FIGYELMEZTETÉS: %s' % f)
    nev = sum(1 for h in e.hivatkozasok if h.fokozat == 'nev')
    print('fokozatok: nev=%d, tartomany=%d; tartományon belül: %d' % (
        nev, len(e.hivatkozasok) - nev, sum(h.tartomanyban for h in e.hivatkozasok)))


if __name__ == '__main__':
    main()
