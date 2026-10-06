#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/bdb_adatblokk.py -- F56 (BDB_ADATBLOKK): szocikkenkent elore szamolt
adatblokk a BDB-fordito promptba (kozvetlen TSV-valtozat, DT-F38i (a) 2b), es
a BDB-hivatkozasok fejezetszam-javitotablaja (DT-F38i (c)).

Az adatblokk nem ertelmez es nem egeszit ki emlekezetbol (CLAUDE.md 3.
szabaly): minden szam es idezet egy forrassorra visszakereshetu, minden
szakasz vegen proveniencia-sor all, ures forrasnal kifejezett jelzes.

    python eszkozok/bdb_adatblokk.py H2617                 # a blokk stdout-ra
    python eszkozok/bdb_adatblokk.py H2617 --ki blokk.md
    python eszkozok/bdb_adatblokk.py --minta H2617 H3548   # tobb blokk
    python eszkozok/bdb_adatblokk.py --javitas-epit        # adat/bdb_igehely_javitas.tsv
    python eszkozok/bdb_adatblokk.py --javitas-atvezet     # M5: az 1-5. adag forditasai

A Strong-szam alakja H2617 / H02617 / 2617 / h2617 mind elfogadott; belsoleg
`H` + 4 jegyu kitoltott szam (+ homograf-betu). Az adat- es kutatasi oldali
tablak olvasasa split('\\t'), irasa '\\t'.join() (CLAUDE.md, TSV-olvasas;
a csv modul tilos).
"""

import argparse
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

KONK = os.path.join(REPO, 'konkordancia')
ADAT = os.path.join(REPO, 'adat')

BDB_UT = os.path.join(KONK, 'BDB_teljes_unabridged.tsv')
TAHOT_UT = os.path.join(KONK, 'TAHOT_kivonat.tsv')
KAROLI_UT = os.path.join(KONK, 'Karoli_1908.tsv')
SZOTAR_UT = os.path.join(KONK, 'Strong_szotar.tsv')
OSHL_UT = os.path.join(KONK, 'OSHL_lexikalis_index.tsv')
LXX_UT = os.path.join(ADAT, 'kulso', 'lxx_bridge.tsv')
PAROK_MAPPA = os.path.join(ADAT, 'karoli_strong')
LEXHIV_UT = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
GRAMM_UT = os.path.join(ADAT, 'grammatikai_strongok.tsv')
FORDITASOK_UT = os.path.join(ADAT, 'forditasok.tsv')
JAVITAS_UT = os.path.join(ADAT, 'bdb_igehely_javitas.tsv')
SORREND_UT = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_sorrend.tsv')

JAVITAS_FEJLEC = ['strong', 'forras_hivatkozas', 'javitott_hivatkozas', 'allapot', 'indok', 'proveniencia']

# A blokk merete (karakter); a levagas szabalya a blokk fejlecebe kerul.
BLOKK_MAX = 2500
PELDA_MAX = 3            # szoalakonkent legfeljebb ennyi pelda-vers
PELDA_ABLAK = 45         # a kiemelt szo korul ennyi karakter a versbol
LXX_MAX = 3
ROKON_MAX = 5
MAGYAR_MAX = 300         # a meglevo magyar szocikk-reszlet hossza


# ---------------------------------------------------------------------------
# TSV, Strong-normalizalas
# ---------------------------------------------------------------------------

def tsv_sorok(ut):
    """A `#`-sorokat es az ures sorokat atugrik; split('\\t')."""
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor and not sor.startswith('#'):
                yield sor.split('\t')


_STRONG = re.compile(r'^\s*[Hh]?0*(\d{1,4})([a-z]?)\s*$')


def strong_norm(s):
    """H2617 / H02617 / 2617 / h2617 -> 'H2617'; homograf-betu megmarad
    (H0090a -> 'H90a'). Hibas alakra None. A belso kulcs a szam (betu nelkul)
    -- l. strong_szam --, a kijelzesre a H + szam szolgal."""
    m = _STRONG.match(s or '')
    if not m:
        return None
    return 'H%d%s' % (int(m.group(1)), m.group(2))


def strong_szam(s):
    """'H2617' / 'H0090a' -> 2617 (a homograf-betu nelkul): a TAHOT, a parok
    es a lxx_bridge csak szamot hasznal."""
    n = strong_norm(s)
    return int(re.match(r'H(\d+)', n).group(1)) if n else None


def strong_padded(s):
    n = strong_norm(s)
    m = re.match(r'H(\d+)([a-z]?)', n)
    return 'H%04d%s' % (int(m.group(1)), m.group(2))


def ts_most():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def prov(scope, forras, ts):
    return '*proveniencia: scope=%s | forras=%s | ts=%s*' % (scope, forras, ts)


# ---------------------------------------------------------------------------
# Betoltok (lusta, egyszer)
# ---------------------------------------------------------------------------

_CACHE = {}


def _cache(kulcs, fv):
    if kulcs not in _CACHE:
        _CACHE[kulcs] = fv()
    return _CACHE[kulcs]


def bdb_szocikkek():
    """{Strong_padded: szoveg}"""
    def be():
        d = {}
        for m in tsv_sorok(BDB_UT):
            if m[0] == 'Strong_padded':
                continue
            d[m[0]] = m[2] if len(m) > 2 else ''
        return d
    return _cache('bdb', be)


def tahot_versek():
    """{strong_szam: {igehely: darab}} -- a TAHOT_kivonat.tsv-bol."""
    def be():
        d = {}
        elso = True
        for m in tsv_sorok(TAHOT_UT):
            if elso:
                elso = False
                continue
            mm = re.match(r'^H(\d+)', m[1])
            if not mm:
                continue
            ig = d.setdefault(int(mm.group(1)), {})
            ig[m[0]] = ig.get(m[0], 0) + 1
        return d
    return _cache('tahot', be)


def parok_konyvek():
    """[(konyv, ut)] a parok_<konyv>.tsv fajlokbol, a fajlnev szerint rendezve
    a kanonikus sorrendben (1Moz..Jozs)."""
    sorrend = ['1Moz', '2Moz', '3Moz', '4Moz', '5Moz', 'Jozs']
    ki = []
    for fn in sorted(os.listdir(PAROK_MAPPA)):
        m = re.match(r'^parok_(.+)\.tsv$', fn)
        if m:
            ki.append((m.group(1), os.path.join(PAROK_MAPPA, fn)))
    ki.sort(key=lambda x: (sorrend.index(x[0]) if x[0] in sorrend else 99, x[0]))
    return ki


def parok():
    """{strong_szam: [(vers, hu_sorszam, hu_szo, bizonyossag)]}, kanonikus
    konyv-sorrendben, fajlon belul a fajl sorrendjeben. Csak H-strong."""
    def be():
        d = {}
        for _kv, ut in parok_konyvek():
            elso = True
            for m in tsv_sorok(ut):
                if elso:                      # fejlec
                    elso = False
                    continue
                mm = re.match(r'^H(\d+)$', m[5])
                if not mm:
                    continue
                d.setdefault(int(mm.group(1)), []).append((m[0], int(m[1]), m[2], m[6]))
        return d
    return _cache('parok', be)


def lefedett_konyvek():
    """A Karoli-Strong parositas kesz konyvei, magyar rovidites szerint."""
    def be():
        ki = []
        for kv, ut in parok_konyvek():
            for m in tsv_sorok(ut):
                if m[0] == 'vers':
                    continue
                ki.append(m[0].rsplit(' ', 1)[0])
                break
        return ki
    return _cache('lefedett', be)


def karoli_vers():
    def be():
        d = {}
        elso = True
        for m in tsv_sorok(KAROLI_UT):
            if elso:
                elso = False
                continue
            d[m[0]] = m[1]
        return d
    return _cache('karoli', be)


def szotar():
    """{Strong_padded: (szoto, jelentes)} -- Strong_szotar.tsv."""
    def be():
        d = {}
        elso = True
        for m in tsv_sorok(SZOTAR_UT):
            if elso:
                elso = False
                continue
            d[m[0]] = (m[1], m[5] if len(m) > 5 else '')
        return d
    return _cache('szotar', be)


def lxx_hid():
    """{heber_strong_szam: [(greek_padded, db)]}"""
    def be():
        d = {}
        elso = True
        for m in tsv_sorok(LXX_UT):
            if elso:
                elso = False
                continue
            mm = re.match(r'^H(\d+)$', m[0])
            if not mm:
                continue
            d.setdefault(int(mm.group(1)), []).append((m[1], int(m[2])))
        return d
    return _cache('lxx', be)


def grammatikai():
    """A nyelvtani (stopword) Strong-szamok halmaza: {'H0413', 'G3588', ...}
    (4 jegyre kitoltve) -- adat/grammatikai_strongok.tsv, F56 M3b."""
    def be():
        d = set()
        elso = True
        for m in tsv_sorok(GRAMM_UT):
            if elso:
                elso = False
                continue
            mm = re.match(r'^([HG])0*(\d{1,4})$', m[0])
            if mm:
                d.add('%s%04d' % (mm.group(1), int(mm.group(2))))
        return d
    return _cache('gramm', be)


def twot_szam(t):
    m = re.match(r'^(\d+)', t or '')
    return m.group(1) if m else None


def oshl():
    """({strong_szam: set(twot-szam)}, {twot-szam: set(strong_szam)})"""
    def be():
        s2t, t2s = {}, {}
        elso = True
        for m in tsv_sorok(OSHL_UT):
            if elso:
                elso = False
                continue
            mm = re.match(r'^H(\d+)$', m[0])
            tw = twot_szam(m[2])
            if not mm or not tw:
                continue
            sz = int(mm.group(1))
            s2t.setdefault(sz, set()).add(tw)
            t2s.setdefault(tw, set()).add(sz)
        return s2t, t2s
    return _cache('oshl', be)


# ---------------------------------------------------------------------------
# Fejezetszam-javitotabla (M2, DT-F38i (c))
# ---------------------------------------------------------------------------

def _kapuk():
    import forditas_kapuk as K
    return K


def konyv_minta():
    """A BDB-szoveg `Konyv fej:vers` hivatkozasait megfogo minta (a 11. kapu
    forras-oldali konyv-lekepezesevel): (kompilalt minta, {forras-alak: Karoli-rovidites})."""
    def be():
        K = _kapuk()
        lek = K._konyv_mintak()[0]
        kulcsok = sorted(set(lek), key=len, reverse=True)
        minta = re.compile(r'(?<![A-Za-zÀ-ɏ0-9])(%s)\.?\s+(\d{1,3}):(\d{1,3})'
                           % '|'.join(re.escape(x) for x in kulcsok))
        return minta, lek
    return _cache('konyvminta', be)


def fejezet_jeloltek(rossz, max_fej):
    """A hibas fejezetszamtol (str) egy szamjegy elhagyasaval, betoldasaval vagy
    cserejevel eloallo, 1..max_fej koze eso fejezetszamok (a hibas maga nelkul)."""
    jel = set()
    n = len(rossz)
    for i in range(n):                                # elhagyas
        jel.add(rossz[:i] + rossz[i + 1:])
    for i in range(n + 1):                            # betoldas
        for d in '0123456789':
            jel.add(rossz[:i] + d + rossz[i:])
    for i in range(n):                                # csere
        for d in '0123456789':
            if d != rossz[i]:
                jel.add(rossz[:i] + d + rossz[i + 1:])
    ki = set()
    for j in jel:
        if not j or j[0] == '0' or not j.isdigit():
            continue
        if 1 <= int(j) <= max_fej and j != rossz:
            ki.add(int(j))
    return sorted(ki)


def forras_hibas_hivatkozasok(szoveg):
    """[(forras_hivatkozas, karoli_konyv, fejezet, vers)] a szocikkbol: a
    konyv fejezetszamanal nagyobb fejezetu, konyvnevvel jelolt hivatkozasok,
    elso elofordulasi sorrendben, ismetles nelkul."""
    K = _kapuk()
    minta, lek = konyv_minta()
    ki, lattam = [], set()
    for m in minta.finditer(szoveg):
        kv = lek[m.group(1)]
        if kv not in K.FEJEZETSZAM:
            continue
        fej = int(m.group(2))
        if fej <= K.FEJEZETSZAM[kv]:
            continue
        forras = '%s %s:%s' % (m.group(1), m.group(2), m.group(3))
        if forras in lattam:
            continue
        lattam.add(forras)
        ki.append((forras, kv, m.group(2), int(m.group(3))))
    return ki


def javitas_sorok(strong_padded_kulcs, szoveg, ts):
    """Egy szocikk javitotabla-sorai (dict-ek). Az algoritmus (brief M2):
    1. a Strong-szam elofordulasai az adott konyvben (TAHOT_kivonat.tsv, plusz a
       parok_<konyv>.tsv; a TAHOT ismert hianyai miatt mindkettő);
    2. jeloltek: a hibas fejezetszambol egy szamjegy elhagyasaval, betoldasaval
       vagy cserejevel elo, a konyvben letezo fejezet, amelynek ugyanazon a
       versszamu versen a Strong-szam elofordul;
    3. pontosan egy jelolt -> javitva; nulla vagy tobb -> jelolt_marad (a
       jeloltek felsorolasaval). Talalgatas nincs."""
    K = _kapuk()
    sz = int(re.match(r'H(\d+)', strong_padded_kulcs).group(1))
    versek = set(tahot_versek().get(sz, {}))
    versek.update(v for v, _a, _b, _c in parok().get(sz, []))
    sorok = []
    for forras, kv, fej, vers in forras_hibas_hivatkozasok(szoveg):
        jelolt = [f for f in fejezet_jeloltek(fej, K.FEJEZETSZAM[kv])
                  if '%s %d:%d' % (kv, f, vers) in versek]
        # Tajekoztato figyelmeztetes (nem dont): a hibas `fejezet:vers` valid fejezet
        # MASIK konyvben, es ott a Strong-szam elofordul -- a hiba lehet konyv-
        # felodasi hiba (pl. psi -> masik konyv) is, nem fejezetszam-elgepeles.
        masik = sorted(v for v in versek
                       if v.rsplit(' ', 1)[0] != kv and v.rsplit(' ', 1)[1] == '%s:%d' % (fej, vers))
        scope = '%s' % strong_norm(strong_padded_kulcs)
        forras_jel = ('konkordancia/BDB_teljes_unabridged.tsv x konkordancia/TAHOT_kivonat.tsv'
                      ' x adat/karoli_strong/parok_*.tsv')
        pv = 'scope=%s | forras=%s; eszkozok/bdb_adatblokk.py --javitas-epit | ts=%s' % (
            scope, forras_jel, ts)
        figy = (' FIGYELEM: a %s:%d azonos fejezet:vers masik konyvben is tartalmazza a %s-t (%s) -- a hiba konyvfelodasi '
                'hiba is lehet.' % (fej, vers, strong_norm(strong_padded_kulcs), ', '.join(masik[:4]))) if masik else ''
        if len(jelolt) == 1 and not masik:
            sorok.append({
                'strong': strong_padded_kulcs,
                'forras_hivatkozas': forras,
                'javitott_hivatkozas': '%s %d:%d' % (kv, jelolt[0], vers),
                'allapot': 'javitva',
                'indok': ('a %s fejezetszam a konyvben nem letezik (max. %d); egy szamjegy elhagyasaval/'
                          'betoldasaval/cserejevel pontosan egy jelolt van, ahol a %s a TAHOT/parok szerint'
                          ' elofordul: %s %d:%d.%s'
                          % (fej, K.FEJEZETSZAM[kv], strong_norm(strong_padded_kulcs), kv, jelolt[0], vers, figy)),
                'proveniencia': pv,
            })
        else:
            if jelolt and masik and len(jelolt) == 1:
                ind = ('a %s fejezetszam a konyvben nem letezik (max. %d); egy jelolt van (%s %d:%d), de javitas nincs: '
                       'konyvnev-hiba gyanu (szabaly: ha a hibas hivatkozas masik konyvben is letezik es ott a '
                       'Strong-szam szerepel, jelolt_marad).%s'
                       % (fej, K.FEJEZETSZAM[kv], kv, jelolt[0], vers, figy))
            elif jelolt:
                ind = ('a %s fejezetszam a konyvben nem letezik (max. %d); %d jelolt, javitas nincs: %s.%s'
                       % (fej, K.FEJEZETSZAM[kv], len(jelolt),
                          ', '.join('%s %d:%d' % (kv, f, vers) for f in jelolt), figy))
            else:
                ind = ('a %s fejezetszam a konyvben nem letezik (max. %d); nincs jelolt (egy szamjegy '
                       'elhagyasaval/betoldasaval/cserejevel sem talalhato olyan vers, ahol a %s elofordul), '
                       'javitas nincs.%s' % (fej, K.FEJEZETSZAM[kv], strong_norm(strong_padded_kulcs), figy))
            sorok.append({
                'strong': strong_padded_kulcs,
                'forras_hivatkozas': forras,
                'javitott_hivatkozas': '',
                'allapot': 'jelolt_marad',
                'indok': ind,
                'proveniencia': pv,
            })
    return sorok


def javitotabla_epit(ts):
    sorok = []
    for sp, szoveg in sorted(bdb_szocikkek().items()):
        sorok.extend(javitas_sorok(sp, szoveg, ts))
    return sorok


def javitotabla_ir(sorok, ut=JAVITAS_UT):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# Fejezetszam-javitotabla a BDB-hivatkozasokhoz (F56 M2, DT-F38i (c)). Sema: adat/SEMA.md 2.23. '
                 'Generalja: python eszkozok/bdb_adatblokk.py --javitas-epit; kezzel nem szerkesztendo.\n')
        fh.write('\t'.join(JAVITAS_FEJLEC) + '\n')
        for s in sorok:
            fh.write('\t'.join(s[m] for m in JAVITAS_FEJLEC) + '\n')


def javitotabla_olvas(ut=JAVITAS_UT):
    """{strong_padded: [sor-dict]}; ures dict, ha a tabla nem letezik."""
    d = {}
    if not os.path.exists(ut):
        return d
    elso = True
    for m in tsv_sorok(ut):
        if elso:
            elso = False
            continue
        s = dict(zip(JAVITAS_FEJLEC, m + [''] * (len(JAVITAS_FEJLEC) - len(m))))
        d.setdefault(s['strong'], []).append(s)
    return d


# ---------------------------------------------------------------------------
# Az adatblokk szakaszai
# ---------------------------------------------------------------------------

def _kisbetu(s):
    return s.lower()


def karoli_alakok(szam):
    """{kisbetus_alak: {'magas': n, 'egyeb': n, 'peldak': [(vers, sorszam, szo, biz)]}} --
    a peldak a parok kanonikus sorrendjeben."""
    ki = {}
    for vers, sorszam, szo, biz in parok().get(szam, []):
        a = ki.setdefault(_kisbetu(szo), {'magas': 0, 'egyeb': 0, 'peldak': []})
        a['magas' if biz == 'magas' else 'egyeb'] += 1
        a['peldak'].append((vers, sorszam, szo, biz))
    return ki


def _tokenek():
    import importlib.util
    ut = os.path.join(REPO, 'eszkozok', 'karoli_strong', 'tokenek.py')
    spec = importlib.util.spec_from_file_location('karoli_tokenek', ut)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def vers_kiemelve(vers, sorszam):
    """A Karoli-vers a sorszam-adik tokennel kiemelve (**szo**), a szo korul
    PELDA_ABLAK karakternyi ablakkal. Visszaadott ertek: szoveg vagy None, ha a
    vers hianyzik vagy a sorszam nem illik a tokenekre."""
    szoveg = karoli_vers().get(vers)
    if szoveg is None:
        return None
    T = _cache('tokenmodul', _tokenek)
    toks = list(T._TOKEN.finditer(szoveg))
    if not 1 <= sorszam <= len(toks):
        return None
    m = toks[sorszam - 1]
    a, b = m.start(), m.end()
    elo = max(0, a - PELDA_ABLAK)
    if elo > 0:                       # szohatarra igazit
        sp = szoveg.find(' ', elo, a)
        elo = sp + 1 if sp != -1 else elo
    utan = min(len(szoveg), b + PELDA_ABLAK)
    if utan < len(szoveg):
        sp = szoveg.rfind(' ', b, utan)
        utan = sp if sp != -1 else utan
    kiv = szoveg[elo:a] + '**' + szoveg[a:b] + '**' + szoveg[b:utan]
    return ('...' if elo > 0 else '') + kiv + ('...' if utan < len(szoveg) else '')


def szakasz_karoli(strong, ts, pelda_per_alak=PELDA_MAX, alak_max=8, pelda_alak_max=None):
    sz = strong_szam(strong)
    lef = lefedett_konyvek()
    alakok = karoli_alakok(sz)
    sorok = []
    lef_szoveg = ', '.join(lef) if lef else 'nincs'
    f1 = ['**1. Károli-szóalakok** (a Károli–Strong párosítás kész könyvei: %s; az arányok csak ezekre érvényesek; a szóalakok kisbetűsítve, egyesítve számolva)'
          % lef_szoveg]
    # TAHOT-elofordulas a lefedett konyvekben vs. a parok darabszama (nem nema nem-talalat)
    tah = tahot_versek().get(sz, {})
    lef_tah = sum(db for v, db in tah.items() if v.rsplit(' ', 1)[0] in lef)
    par_db = len(parok().get(sz, []))
    if not alakok:
        f1.append('[NINCS KÁROLI-ALAK] (a lefedett könyvekben a TAHOT-ban %d előfordulás, Károli-pár %d)'
                  % (lef_tah, par_db))
    else:
        rendez = sorted(alakok.items(), key=lambda kv: (-(kv[1]['magas'] + kv[1]['egyeb']), kv[0]))
        magas = sorted(((a, v['magas']) for a, v in alakok.items() if v['magas']),
                       key=lambda x: (-x[1], x[0]))
        egyeb = sorted(((a, v['egyeb']) for a, v in alakok.items() if v['egyeb']),
                       key=lambda x: (-x[1], x[0]))

        def lista(l):
            if not l:
                return '—'
            r = ', '.join('%s ×%d' % (a, n) for a, n in l[:alak_max])
            if len(l) > alak_max:
                r += ' (+%d további alak)' % (len(l) - alak_max)
            return r
        f1.append('- magas bizonyosságú pár: %s' % lista(magas))
        f1.append('- alacsonyabb bizonyosságú pár (`alacsony`): %s' % lista(egyeb))
        f1.append('- a lefedett könyvekben a TAHOT-ban %d előfordulás, ebből %d kapott Károli-párt' % (lef_tah, par_db))
    f1.append(prov(strong_norm(strong), 'adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv', ts))
    # peldak
    f2 = ['**2. Példaversek** (szabály: a leggyakoribb szóalakok, alakonként a kanonikus sorrend első %d verse, a szó **kiemelve**)' % pelda_per_alak]
    if not alakok:
        f2.append('—')
    else:
        rendez = sorted(alakok.items(), key=lambda kv: (-(kv[1]['magas'] + kv[1]['egyeb']), kv[0]))
        if pelda_alak_max is not None:
            rendez_p = rendez[:pelda_alak_max]
        else:
            rendez_p = rendez
        for alak, v in rendez_p:
            lattam, db = set(), []
            for vers, sorsz, szo, biz in v['peldak']:
                if vers in lattam:
                    continue
                lattam.add(vers)
                idez = vers_kiemelve(vers, sorsz)
                if idez is None:
                    db.append('%s „[nincs Károli-szöveg a Karoli_1908.tsv-ben]”' % vers)
                else:
                    db.append('%s „%s”' % (vers, idez))
                if len(db) >= pelda_per_alak:
                    break
            f2.append('- **%s**: %s' % (alak, ' · '.join(db) if db else '—'))
        if pelda_alak_max is not None and len(rendez) > pelda_alak_max:
            f2.append('[LEVÁGVA: a további %d szóalak példái kimaradtak]' % (len(rendez) - pelda_alak_max))
    f2.append(prov(strong_norm(strong), 'adat/karoli_strong/parok_*.tsv + konkordancia/Karoli_1908.tsv', ts))
    return f1, f2


def szakasz_lxx(strong, ts):
    """LXX-megfelelo (legfeljebb LXX_MAX). F56 M3b: ha a HEBER szo nem nyelvtani
    (adat/grammatikai_strongok.tsv), a nyelvtani gorog talalatok (nevelo, eloljaro,
    kotoszo: G3588, G1519, ...) kimaradnak a legfeljebb 3 koze; ha a heber szo maga is
    nyelvtani, a gorog nyelvtani talalatok maradnak. A kihagyas jelolve van."""
    sz = strong_szam(strong)
    mind = sorted(lxx_hid().get(sz, []), key=lambda x: (-x[1], x[0]))
    gr = grammatikai()
    heber_nyelvtani = ('H%04d' % sz) in gr
    kihagyva = []
    if heber_nyelvtani:
        sor = mind[:LXX_MAX]
    else:
        sor = []
        for g, db in mind:
            if g in gr:
                kihagyva.append((g, db))
            elif len(sor) < LXX_MAX:
                sor.append((g, db))
    f = ['**3. LXX-megfelelő**']
    if not sor:
        f.append('—')
    else:
        r = []
        for g, db in sor:
            lemma = szotar().get(g, ('[nincs lemma a Strong_szotar.tsv-ben]', ''))[0]
            r.append('%s %s ×%d' % (g[:1] + str(int(g[1:])), lemma, db))
        f.append(', '.join(r) + ' (a legfeljebb %d leggyakoribb)' % LXX_MAX)
    if kihagyva:
        f.append('[kihagyva, nyelvtani görög szó: %s]' % ', '.join(
            '%s %s ×%d' % (g[:1] + str(int(g[1:])), szotar().get(g, ('?', ''))[0], db)
            for g, db in kihagyva[:3]) + (' (+%d további)' % (len(kihagyva) - 3) if len(kihagyva) > 3 else ''))
    f.append(prov(strong_norm(strong),
                  'adat/kulso/lxx_bridge.tsv + konkordancia/Strong_szotar.tsv + adat/grammatikai_strongok.tsv', ts))
    return f


def szakasz_rokon(strong, ts):
    sz = strong_szam(strong)
    s2t, t2s = oshl()
    f = ['**4. Rokon szavak** (azonos TWOT-szám, legfeljebb %d, a Strong-szám szerint növekvő)' % ROKON_MAX]
    tw = sorted(s2t.get(sz, set()), key=int)
    rokon = sorted({r for t in tw for r in t2s[t] if r != sz})
    if not rokon:
        f.append('—' + ('' if tw else ' (a Strong-számhoz nincs TWOT-szám az OSHL-indexben)'))
    else:
        r = []
        for x in rokon[:ROKON_MAX]:
            sp = 'H%04d' % x
            szoto, jel = szotar().get(sp, ('[nincs lemma]', ''))
            r.append('H%d %s%s' % (x, szoto, ' („%s”)' % jel if jel else ''))
        f.append('TWOT %s: ' % ', '.join(tw) + '; '.join(r)
                 + (' (+%d további)' % (len(rokon) - ROKON_MAX) if len(rokon) > ROKON_MAX else ''))
    f.append(prov(strong_norm(strong),
                  'konkordancia/OSHL_lexikalis_index.tsv + konkordancia/Strong_szotar.tsv', ts))
    return f


def szakasz_magyar(strong, ts, magyar_max=MAGYAR_MAX):
    """A lexikon_hivatkozasok.tsv sorai -> a forditasok.tsv magyar szovege (a
    sajat `teljes` BDB-sor nem szamit: az a most forditando szocikk)."""
    sp = strong_padded(strong)
    szam = strong_szam(strong)
    f = ['**5. Meglévő magyar szócikk**']
    forditasok = {}
    elso = True
    for m in tsv_sorok(FORDITASOK_UT):
        if elso:
            elso = False
            continue
        forditasok[(m[0], m[1], m[2], m[3], m[4])] = m[6]
    r = []
    elso = True
    for m in tsv_sorok(LEXHIV_UT):
        if elso:
            elso = False
            continue
        mm = re.match(r'^H(\d+)', m[0])
        if not mm or int(mm.group(1)) != szam:
            continue
        if m[3] == 'teljes':
            continue
        hu = forditasok.get((m[1], m[0], m[2], m[3], 'forditas_hu'))
        if hu:
            r.append('%s %s: %s' % (m[1], m[3], hu if len(hu) <= magyar_max else hu[:magyar_max] + ' [LEVÁGVA]'))
    f.append(' · '.join(r) if r else '—')
    f.append(prov(strong_norm(strong), 'adat/lexikon_hivatkozasok.tsv + adat/forditasok.tsv', ts))
    return f


def szakasz_javitas(strong, ts):
    sp = strong_padded(strong)
    f = ['**6. Javított forrás-hivatkozások** (adat/bdb_igehely_javitas.tsv)']
    sorok = javitotabla_olvas().get(sp, [])
    if not sorok:
        f.append('—')
    for s in sorok:
        if s['allapot'] == 'javitva':
            f.append('- a forrásban `%s` → helyesen `%s`' % (s['forras_hivatkozas'], s['javitott_hivatkozas']))
        else:
            ind = s['indok']
            mj = re.search(r'egy jelolt van \(([^)]+)\)', ind)
            if mj and 'konyvnev-hiba gyanu' in ind:
                ok = 'könyvnév-hiba gyanú, a hibás fejezet:vers másik könyvben is tartalmazza a Strong-számot; egy jelölt: %s' % mj.group(1)
            elif 'nincs jelolt' in ind:
                ok = 'nincs jelölt'
            else:
                ok = ind.split('; ', 1)[-1].split(' FIGYELEM')[0].rstrip('.')
            f.append('- a forrásban `%s` nem létező fejezet; javítás nincs (%s)' % (s['forras_hivatkozas'], ok))
    f.append(prov(strong_norm(strong), 'adat/bdb_igehely_javitas.tsv', ts))
    return f


def blokk_epit(strong, ts=None, max_kar=BLOKK_MAX):
    """Az adatblokk Markdown-szovege. Meretkorlat: max_kar karakter; ha a blokk
    hosszabb, a levagas sorrendje: (1) a peldak szoalakonkenti szama 3 -> 2 -> 1,
    (2) a peldaval ellatott szoalakok szamanak csokkentese, (3) a szoalak-lista
    rovidítese. Minden levagas `[LEVÁGVA ...]` jelolest kap."""
    n = strong_norm(strong)
    if n is None:
        raise ValueError('hibas Strong-szam: %r' % strong)
    ts = ts or ts_most()
    fejlec = ('### ADATBLOKK %s (gépi, a projekt adataiból; nem értelmezés; max. %d karakter; levágás: '
              'példák/alak 3→2→1, kevesebb példás alak, rövidebb alaklista, rövidebb magyar szöveg; jelzés: [LEVÁGVA])' % (n, max_kar))
    vegso = None
    lepesek = [dict(pelda_per_alak=3, alak_max=6, pelda_alak_max=3),
               dict(pelda_per_alak=3, alak_max=6, pelda_alak_max=2),
               dict(pelda_per_alak=2, alak_max=6, pelda_alak_max=2),
               dict(pelda_per_alak=2, alak_max=5, pelda_alak_max=1),
               dict(pelda_per_alak=1, alak_max=4, pelda_alak_max=1),
               dict(pelda_per_alak=1, alak_max=3, pelda_alak_max=1),
               dict(pelda_per_alak=1, alak_max=3, pelda_alak_max=1, magyar_max=120)]
    for lp in lepesek:
        f1, f2 = szakasz_karoli(strong, ts, **{k: v for k, v in lp.items() if k != 'magyar_max'})
        szakaszok = [f1, f2, szakasz_lxx(strong, ts), szakasz_rokon(strong, ts),
                     szakasz_magyar(strong, ts, lp.get('magyar_max', MAGYAR_MAX)), szakasz_javitas(strong, ts)]
        szoveg = fejlec + '\n\n' + '\n\n'.join('\n'.join(s) for s in szakaszok) + '\n'
        vegso = szoveg
        if len(szoveg) <= max_kar:
            return szoveg
    # utolso eset: vagas a szoveg vegen, jelezve (a proveniencia-sorok elvesznek --
    # ez csak a hibakezeles; a mintaban nem fordulhat elo, a tesztek figyelik)
    jel = '\n[LEVÁGVA: a blokk a méretkorlát miatt csonka]\n'
    return vegso[:max_kar - len(jel)] + jel


# ---------------------------------------------------------------------------
# M5: visszamenoleges atvezetes (a forditasok.tsv `javitva` hivatkozasai)
# ---------------------------------------------------------------------------

def atvezet_szoveg(forditas, javitva_sorok):
    """A forditas-szoveg `X` hivatkozasait `Y [BDB: X]`-re cserelve a `javitva`
    sorok alapjan. A forras-hivatkozas (angol alak) magyar megfeleloje a
    fordításban: <Karoli-konyv> <fej>:<vers>. Visszaad: (uj_szoveg, [(regi, uj, db)])."""
    K = _kapuk()
    lek = konyv_minta()[1]
    csere = []
    uj = forditas
    for s in javitva_sorok:
        m = re.match(r'^(.+?)\.?\s+(\d{1,3}):(\d{1,3})$', s['forras_hivatkozas'])
        kv = lek[m.group(1)]
        regi = '%s %s:%s' % (kv, m.group(2), m.group(3))
        jav = s['javitott_hivatkozas']
        minta = re.compile(r'(?<![A-Za-zÀ-ɏ0-9])%s(?![0-9])(?!\])' % re.escape(regi))
        db = len(minta.findall(uj))
        if db:
            uj = minta.sub(lambda mm, jav=jav, regi=regi: '%s [BDB: %s]' % (jav, regi), uj)
            csere.append((regi, jav, db))
    return uj, csere


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('strong', nargs='?', help='pl. H2617')
    ap.add_argument('--ki', help='kimeneti fajl (alapertelmezes: stdout)')
    ap.add_argument('--ts', help='a proveniencia-sor ts-e (alapertelmezes: most, UTC)')
    ap.add_argument('--minta', nargs='+', metavar='STRONG', help='tobb blokk egymas utan')
    ap.add_argument('--javitas-epit', action='store_true', help='adat/bdb_igehely_javitas.tsv ujraepitese')
    args = ap.parse_args(argv)
    ts = args.ts or ts_most()
    if args.javitas_epit:
        sorok = javitotabla_epit(ts)
        javitotabla_ir(sorok)
        jav = sum(1 for s in sorok if s['allapot'] == 'javitva')
        print('irva: %s (%d sor; javitva %d, jelolt_marad %d)' % (JAVITAS_UT, len(sorok), jav, len(sorok) - jav))
        return 0
    strongok = args.minta or ([args.strong] if args.strong else [])
    if not strongok:
        ap.error('adj meg egy Strong-szamot, vagy --minta / --javitas-epit')
    kimenet = '\n'.join(blokk_epit(s, ts) for s in strongok)
    if args.ki:
        with open(args.ki, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(kimenet)
        print('irva: %s (%d karakter)' % (args.ki, len(kimenet)))
    else:
        print(kimenet)
    return 0


if __name__ == '__main__':
    sys.exit(main())
