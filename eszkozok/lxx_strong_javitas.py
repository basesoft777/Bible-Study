#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lxx_strong_javitas.py — F240 (LXXBDB) L1/L2/L6: a Macula LXX-párok görög Strong-számának javítása és mérése.

A `konkordancia/Macula_heber_*.tsv` `gorog_strong` oszlopa a Macula forrás `greekstrong` attribútuma, változatlanul
(`eszkozok/f17/macula_futtat.py`); az `adat/kulso/lxx_bridge.tsv` (bcv-commons) ugyanennek az összesítése. Néhány
alakon a forrás címkéje más lemmára mutat (pl. „πρωὶ” → G5459 φωσφόρος a G4404 πρωΐ helyett, 88 hely, N-F231a).

Egy kéz: a javítás egyetlen helyen, a kézi `adat/lxx_strong_javitas.tsv` szerint történik, és **minden fogyasztó ezen a
modulon át olvas** (a nyers fájlok változatlanok, licenc és SHA miatt; `CLAUDE.md`, memória: „javítás új fájlként: nyers
marad”):
  * `macula_tokenek(konk)` — a Macula-tokenek javított görög Strong-számmal;
  * `bridge_sorok(adat, konk)` — a `lxx_bridge.tsv` sorai a javított tokenek különbségével (héber Strong szerint −1/+1);
  * `illesztes(...)`, `gyanus_parok(...)` — a Macula–LXX_OS tokenillesztés (ugyanaz a Károli-vers, ugyanaz az
    ékezet nélküli alak) és belőle a kapuk mérőszámai (`eszkozok/ellenoriz.py`, 44–46. szabály).

A `helyes_strong` üres lehet (DT-F240b): ha a helyes lemmának nincs Strong-száma, a pár „megfelelő nélkül” lesz, és
ezt a tábla `indok` mezője kimondja.

Futtatás a repó gyökeréből (mérés, fájlt nem ír, csak `--naplo` esetén a megadott útra):
    python eszkozok/lxx_strong_javitas.py [--naplo naplok/LXXBDB_lxx_jeloltek.tsv]
I/O: split('\\t') / '\\t'.join (csv modul nélkül).
"""
import argparse
import collections
import glob
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVITAS = os.path.join('adat', 'lxx_strong_javitas.tsv')
BRIDGE = os.path.join('adat', 'kulso', 'lxx_bridge.tsv')
JAVITAS_OSZLOPOK = ['alak_norm', 'hibas_strong', 'helyes_strong', 'ok', 'indok', 'proveniencia']


def tsv(ut):
    """(fejléc, [dict]) — '#' kezdetű és üres sorok kihagyva."""
    fej, ki = None, []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fej is None:
                fej = mezok
                continue
            ki.append(dict(zip(fej, mezok + [''] * (len(fej) - len(mezok)))))
    return fej or [], ki


def alak_norm(w):
    """Ékezet, lehelet, írásjel nélkül, kisbetűvel, végső szigma nélkül: „πρωὶ” = „πρωί” = „πρωι”."""
    d = unicodedata.normalize('NFD', w or '')
    return ''.join(c for c in d if unicodedata.category(c).startswith('L')).lower().replace('ς', 'σ')


def strong_g(s):
    """'1722' / 'G1722' / 'G01722' → 'G1722'; üres → ''."""
    s = (s or '').strip()
    if not s:
        return ''
    m = re.match(r'^G?0*(\d+)([a-zA-Z]?)$', s)
    return 'G%04d%s' % (int(m.group(1)), m.group(2)) if m else s


def javitasok(gyoker=GYOKER):
    """{(alak_norm, hibás Strong): (helyes Strong vagy '', indok)}."""
    ut = os.path.join(gyoker, JAVITAS)
    fej, sorok = tsv(ut)
    if fej[:len(JAVITAS_OSZLOPOK)] != JAVITAS_OSZLOPOK:
        raise ValueError('%s: a fejléc nem %s' % (JAVITAS, JAVITAS_OSZLOPOK))
    ki = {}
    for r in sorok:
        k = (r['alak_norm'], strong_g(r['hibas_strong']))
        if k in ki:
            raise ValueError('%s: kettőzött kulcs %s' % (JAVITAS, k))
        ki[k] = (strong_g(r['helyes_strong']), r['indok'])
    return ki


def javit(alak, strong, jt):
    """-> (javított Strong, javítva-e). A `jt` a `javitasok()` kimenete."""
    s = strong_g(strong)
    t = jt.get((alak_norm(alak), s))
    return (t[0], True) if t is not None else (s, False)


def macula_fajlok(konk):
    return sorted(glob.glob(os.path.join(konk, 'Macula_heber_*.tsv')))


def macula_tokenek(konk, jt):
    """Bejárja a Macula-tokeneket: (sor-dict, javított görög Strong, javítva-e). A sor-dict a nyers TSV-sor."""
    for f in macula_fajlok(konk):
        for r in tsv(f)[1]:
            g, jv = javit(r.get('gorog_lxx', ''), r.get('gorog_strong', ''), jt)
            yield r, g, jv


def bridge_sorok(gyoker=GYOKER, konk=None, jt=None):
    """A `lxx_bridge.tsv` sorai (dict: hebrew_strong, greek_strong, count) a javított Macula-tokenek különbségével.
    A forrás a Macula összesítése (count ≥ 3); a különbség csak ott lép be, ahol a hibás pár a forrásban áll, a
    helyes pár pedig hozzáadódik (ha a forrásban nem volt, új sor, a többi sor sorrendje változatlan)."""
    konk = konk or os.path.join(gyoker, 'konkordancia')
    jt = javitasok(gyoker) if jt is None else jt
    fej, sorok = tsv(os.path.join(gyoker, BRIDGE))
    delta = collections.Counter()
    for r, g, jv in macula_tokenek(konk, jt):
        if not jv:
            continue
        h = (r.get('strong') or '').strip()
        if not h:
            continue
        delta[(h, strong_g(r.get('gorog_strong')))] -= 1
        if g:
            delta[(h, g)] += 1
    ki, latott = [], set()
    for r in sorok:
        k = (r['hebrew_strong'], strong_g(r['greek_strong']))
        latott.add(k)
        n = int(r['count']) + delta.get(k, 0)
        if n > 0:
            ki.append({'hebrew_strong': r['hebrew_strong'], 'greek_strong': r['greek_strong'], 'count': str(n)})
    for (h, g), d in sorted(delta.items()):
        if (h, g) not in latott and d > 0:
            ki.append({'hebrew_strong': h, 'greek_strong': g, 'count': str(d)})
    return ki


# -- mérés: Macula–LXX_OS tokenillesztés ------------------------------------------------------------------------

def strong_szotar(konk):
    """{G-szám: szótő} a `Strong_szotar.tsv`-ből."""
    ki = {}
    for r in tsv(os.path.join(konk, 'Strong_szotar.tsv'))[1]:
        s = r.get('Strong-szám', '')
        if s.startswith('G'):
            ki[strong_g(s)] = r.get('Szótő', '')
    return ki


def lxx_os_index(konk):
    """({Károli-vers: {alak_norm: Counter((Strong, lemma))}}, az LXX_OS összes Strongja)."""
    ix = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    osszes = set()
    for f in sorted(glob.glob(os.path.join(konk, 'LXX_OS', '*.tsv'))):
        fej, sorok = tsv(f)
        if 'szoalak' not in fej:
            continue
        for r in sorok:
            ig = r.get('igehely_karoli', '')
            s = strong_g(r.get('strong', ''))
            if s:
                osszes.add(s)
            if ig:
                ix[ig][alak_norm(r.get('szoalak', ''))][(s, r.get('lemma', ''))] += 1
    return ix, osszes


def lxx_os_homograf(konk, sz=None):
    """Az LXX_OS homográf-hibái (N-F240a): Counter{(lemma, hozzárendelt Strong, típus): token}. Az `lxx_os_import.py` a
    lemmát ékezet és kisbetű nélkül keresi, ezért két típusú hiba keletkezik:
      * `masik_strong`: a pontos (ékezethelyes) lemmának saját Strong-száma van, de az LXX_OS mást ad
        (εἷς → G1519 εἰς a G1520 helyett; τίς → G5100 a G5101 helyett; καρπός → G2591 Κάρπος a G2590 helyett);
      * `tulajdonnev`: kisbetűs közszó tulajdonnévi Strong-számmal, amelynek nincs közszói párja
        (πόντος → G4195 Πόντος; τύραννος → G5181 Τύραννος) — a #240 L6.
    Ékezet nélküli lemma (átírt tulajdonnév, pl. Ιερουσαλημ) és a puszta ékezet-írásmód eltérés nem hiba."""
    sz = strong_szotar(konk) if sz is None else sz
    pontos = collections.defaultdict(set)
    for g, szt in sz.items():
        for x in szt.split(','):
            if x.strip():
                pontos[unicodedata.normalize('NFC', x.strip())].add(g)
    ki = collections.Counter()
    for f in sorted(glob.glob(os.path.join(konk, 'LXX_OS', '*.tsv'))):
        fej, sorok = tsv(f)
        if 'szoalak' not in fej:
            continue
        for r in sorok:
            s = strong_g(r.get('strong', ''))
            lem = unicodedata.normalize('NFC', r.get('lemma', '') or '')
            szt = (sz.get(s, '') or '').split(',')[0].strip()
            if not (s and lem and szt):
                continue
            jo = pontos.get(lem, set())
            if jo and s not in jo:
                ki[(lem, s, 'masik_strong')] += 1
            elif not jo and lem[:1].islower() and szt[:1].isupper() and alak_norm(lem) == alak_norm(szt):
                ki[(lem, s, 'tulajdonnev')] += 1
    return ki


def illesztes(konk, jt, ix=None):
    """Counter{(Macula-Strong javítva, LXX_OS-Strong, LXX_OS-lemma): token} az illeszthető tokeneken (a vers azonos
    alakú LXX_OS-tokenjeinek leggyakoribb Strong+lemma párja). Visszaad: (Counter, {kulcs: példa-alak})."""
    if ix is None:
        ix = lxx_os_index(konk)[0]
    db = collections.Counter()
    pelda = {}
    for r, g, _jv in macula_tokenek(konk, jt):
        if not g:
            continue
        c = ix.get(r.get('karoli', ''), {}).get(alak_norm(r.get('gorog_lxx', '')))
        if not c:
            continue
        t, lem = c.most_common(1)[0][0]
        k = (g, t, lem)
        db[k] += 1
        pelda.setdefault(k, r.get('gorog_lxx', ''))
    return db, pelda


JELOLT = os.path.join('naplok', 'LXXBDB_lxx_jeloltek.tsv')
JELOLT_OSZLOPOK = ['macula_strong', 'macula_szoto', 'lxx_os_strong', 'lxx_os_lemma', 'token', 'macula_strong_osszes',
                   'pelda_alak', 'itelet', 'indok']
ITELETEK = ('konvencio', 'macula_hiba', 'lxx_os_hiba', 'illesztesi_zaj', 'nem_eldontheto')


def jeloltek(konk, jt, ix=None, osszes=None, sz=None):
    """A Macula–LXX_OS eltérés-jelöltjei: [(S, T, lemma, token, S összes, példa)]. Jelölt, ha a (javított) Macula-Strong
    az LXX_OS-ben nem fordul elő, és (a) az LXX_OS ugyanazon a tokenen más Strongot ad, vagy (b) nem ad Strongot, és
    az LXX-lemma nem a Macula-Strong szótöve."""
    if ix is None or osszes is None:
        ix, osszes = lxx_os_index(konk)
    sz = strong_szotar(konk) if sz is None else sz
    db, pelda = illesztes(konk, jt, ix)
    ossz = collections.Counter()
    for (s, _t, _l), n in db.items():
        ossz[s] += n
    ki = []
    for (s, t, lem), n in sorted(db.items(), key=lambda kv: (-kv[1], kv[0])):
        if s == t or s in osszes:
            continue
        if not t:
            szt = {alak_norm(x) for x in (sz.get(s, '') or '').split(',') if x.strip()}
            if alak_norm(lem) in szt:
                continue
        ki.append((s, t, lem, n, ossz[s], pelda[(s, t, lem)]))
    return ki


def iteletek(gyoker=GYOKER):
    """{(S, T, lemma): (ítélet, indok)} a jelöltlistából."""
    ut = os.path.join(gyoker, JELOLT)
    if not os.path.exists(ut):
        return {}
    return {(r['macula_strong'], r['lxx_os_strong'], r['lxx_os_lemma']): (r.get('itelet', ''), r.get('indok', ''))
            for r in tsv(ut)[1]}


_GYORSITO = {}


def meres(gyoker=GYOKER):
    """A kapuk közös mérése (egyszer számolva): dict a jelöltekkel, az ítéletekkel, a homográf-számmal."""
    if gyoker in _GYORSITO:
        return _GYORSITO[gyoker]
    konk = os.path.join(gyoker, 'konkordancia')
    jt = javitasok(gyoker)
    ix, osszes = lxx_os_index(konk)
    sz = strong_szotar(konk)
    db, _p = illesztes(konk, jt, ix)
    m = {'jt': jt, 'osszes': osszes, 'sz': sz, 'illesztes': db, 'jeloltek': jeloltek(konk, jt, ix, osszes, sz),
         'iteletek': iteletek(gyoker), 'homograf': lxx_os_homograf(konk, sz)}
    _GYORSITO[gyoker] = m
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ir', action='store_true', help='a jelöltlista (%s) frissítése; a meglévő ítéletek megmaradnak' % JELOLT)
    a = ap.parse_args()
    m = meres()
    it = m['iteletek']
    sorok, uj = [], 0
    for s, t, lem, n, ossz, pel in m['jeloltek']:
        i, ok = it.get((s, t, lem), ('', ''))
        uj += not i
        sorok.append([s, m['sz'].get(s, ''), t, lem, str(n), str(ossz), pel, i, ok])
    print('jelölt pár: %d (token: %d); ítélet nélkül: %d' % (len(sorok), sum(int(x[4]) for x in sorok), uj))
    for k in ITELETEK:
        print('  %-15s %3d pár' % (k, sum(1 for x in sorok if x[7] == k)))
    print('LXX_OS homográf (N-F240a): %d lemma–Strong pár, %d token' % (len(m['homograf']), sum(m['homograf'].values())))
    if a.ir:
        with open(os.path.join(GYOKER, JELOLT), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT jelöltrész + kézi ítélet: eszkozok/lxx_strong_javitas.py --ir (F240 L1); az itelet/indok oszlop kézi, '
                    'újrafuttatáskor megmarad. Ítélet: %s.\n' % ' / '.join(ITELETEK))
            f.write('\t'.join(JELOLT_OSZLOPOK) + '\n')
            for x in sorok:
                f.write('\t'.join(x) + '\n')
        print('kiírva:', JELOLT)


if __name__ == '__main__':
    main()
