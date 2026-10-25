#!/usr/bin/env python
"""A Thayer sigla- és rövidítéstáblájának gépi jelöltgyűjtése (F132, brief 2a/5; M1 mellékterméke).

Bemenet: `adat/thayer_szakaszok.tsv` a javított nézetben (`thayer_bemenet.szakaszok`: a `jel` + `szoveg`, a
`thayer_forras_javitas.tsv` beszúrásaival — vagyis a fordítónak átadott szöveg; DT-F132i (2)). Kimenet:
`adat/thayer_sigla.tsv` (SEMA 2.37). **Félig kézi tábla:** a számoszlopokat (`elofordulas`, `szocikk`,
`gerinc_elofordulas`, `pelda`) és az új jelölt sorokat ez az eszköz írja; a besorolás (`tipus`, `jelentes`, `magyar_alak`,
`allapot` — `javaslat` vagy `besorolt` —, `besorolas_proveniencia`) kézi, és az eszköz **soha nem írja át** (írás előtt összeveti a régi táblával, eltérésnél megáll). Sort nem
töröl: a forrásból eltűnt jelölt `elofordulas = 0`-val marad.

A gyűjtés három szabálya (`gyujtes` oszlop), rögzítve a futás előtt:
  - `minta`: a brief 2a/5 és az M0 7. pontjának megnevezett elemei (kiadás-siglák, grammatikák, antik és modern szerzők,
    `Sept.`, `cf.`, `i. e.` …), szóhatáron;
  - `kiadas_sigla`: az `R G L T Tr WH` siglák, ha legalább kettő sorban áll (`G L T Tr WH`, `R G`), egyenként számolva;
  - `rovidites`: ponttal záruló szóalak (`Xxx.` vagy `xx.`), amely legalább 10-szer fordul elő, és előfordulásainak
    legalább 90%-a ponttal áll (a mondatvégi szó ezért kiesik); a `minta`-elemek nélkül.

  python eszkozok/thayer_jelolt/sigla_gyujt.py [--ts NAP] [--meres] [--ellenoriz]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402

KI_UT = os.path.join(TB.GYOKER, 'adat', 'thayer_sigla.tsv')
FEJLEC = ['forrasalak', 'gyujtes', 'tipus', 'jelentes', 'magyar_alak', 'elofordulas', 'szocikk', 'gerinc_elofordulas', 'pelda',
          'allapot', 'besorolas_proveniencia', 'proveniencia']
KEZI = ('tipus', 'jelentes', 'magyar_alak', 'allapot', 'besorolas_proveniencia')

MINTA = ['Rec.', 'Lachmann', 'Tdf.', 'Tischendorf', 'Griesbach', 'Grsb.', 'Winers Grammar', "Winer's Grammar",
         'Buttmann', 'Sept.', 'Vulg.', 'Apocr.', 'cf.', 'Cf.', 'i. e.', 'q. v.', 'Xenophon', 'Plato', 'Homer', 'Herodotus',
         'Thucydides', 'Josephus', 'Philo', 'Polybius', 'Plutarch', 'Lucian', 'Aristotle', 'Grimm', 'Schmidt', 'Meyer',
         'Lightfoot', 'Trench', 'Gesenius']
SIGLA = ['R', 'G', 'L', 'T', 'Tr', 'WH']
SIGLA_SOR = re.compile(r'(?<![\w.])(?:(?:R|G|L|T|Tr|WH)\s+){1,}(?:R|G|L|T|Tr|WH)(?![\w])')
ROVID = re.compile(r'(?<![\w.\'’])([A-Z][a-z]{0,9}|[a-z]{1,6})\.(?=[\s,;:)\]]|$)')
ROVID_MIN = 10
ROVID_ARANY = 0.9


def _minta_re(a):
    return re.compile(r'(?<![\w])' + re.escape(a) + (r'(?![\w])' if a[-1].isalnum() else ''))


def szovegek(tabla=None):
    """-> [(strong, sorszam, szöveg)] a tábla sorrendjében."""
    ki = []
    for st in TB.tabla_olvas(tabla):
        for x in TB.szakaszok(st, tabla):
            ki.append((st, str(x['sorszam']), x['szoveg']))
    return ki


def gyujt(tabla=None):
    """-> OrderedDict: forrasalak -> {gyujtes, elofordulas, szocikk(set), gerinc, pelda}."""
    sz = szovegek(tabla)
    gerinc = set(szolista.gerinc_strongok())
    ki = collections.OrderedDict()

    def add(alak, gy, st, n, t):
        d = ki.setdefault(alak, {'gyujtes': gy, 'elofordulas': 0, 'szocikk': set(), 'gerinc': 0, 'pelda': ''})
        d['elofordulas'] += t
        d['szocikk'].add(st)
        if st in gerinc:
            d['gerinc'] += t
        if not d['pelda']:
            d['pelda'] = '%s:%s' % (st, n)

    mintak = [(a, _minta_re(a)) for a in MINTA]
    for st, n, t in sz:
        for a, rx in mintak:
            k = len(rx.findall(t))
            if k:
                add(a, 'minta', st, n, k)
        for m in SIGLA_SOR.finditer(t):
            for tok in m.group(0).split():
                add(tok, 'kiadas_sigla', st, n, 1)
    # rövidítések: előbb a számlálás, aztán a küszöb
    pont, csupasz, hol = collections.Counter(), collections.Counter(), collections.defaultdict(list)
    tobbszavas = [_minta_re(a) for a in MINTA if ' ' in a and a.endswith('.')]
    for st, n, t in sz:
        for rx in tobbszavas:          # az `i. e.`, `q. v.` betűi nem önálló rövidítések
            t = rx.sub(' ', t)
        for m in ROVID.finditer(t):
            pont[m.group(1)] += 1
            hol[m.group(1)].append((st, n))
        for w in re.findall(r'(?<![\w.])([A-Za-z]{1,10})(?![\w.])', t):
            csupasz[w] += 1
    kizart = {a.rstrip('.') for a in MINTA if a.endswith('.') and ' ' not in a} | set(SIGLA)
    for w in sorted(pont, key=lambda x: (-pont[x], x)):
        p, b = pont[w], csupasz[w]
        if p < ROVID_MIN or p / float(p + b) < ROVID_ARANY or w in kizart:
            continue
        for st, n in hol[w]:
            add(w + '.', 'rovidites', st, n, 1)
    return ki


def regi_tabla(ut=KI_UT):
    if not os.path.exists(ut):
        return collections.OrderedDict()
    d = collections.OrderedDict()
    for r in szolista.tsv_dict(ut):
        d[r['forrasalak']] = r
    return d


def osszefesul(gy, regi, ts):
    """A régi tábla kézi oszlopai változatlanok; új jelölt a végére; eltűnt jelölt 0-val marad."""
    ki = []
    lattam = set()
    for alak, r in regi.items():
        d = gy.get(alak)
        uj = dict(r)
        uj['elofordulas'] = str(d['elofordulas']) if d else '0'
        uj['szocikk'] = str(len(d['szocikk'])) if d else '0'
        uj['gerinc_elofordulas'] = str(d['gerinc']) if d else '0'
        uj['pelda'] = d['pelda'] if d else ''
        uj['proveniencia'] = 'scope=adat/thayer_szakaszok.tsv | forras=thayer_jelolt/sigla_gyujt.py (fejléc) | ts=%s' % ts
        ki.append(uj)
        lattam.add(alak)
    for alak, d in gy.items():
        if alak in lattam:
            continue
        ki.append({'forrasalak': alak, 'gyujtes': d['gyujtes'], 'tipus': '', 'jelentes': '', 'magyar_alak': '',
                   'elofordulas': str(d['elofordulas']), 'szocikk': str(len(d['szocikk'])),
                   'gerinc_elofordulas': str(d['gerinc']), 'pelda': d['pelda'], 'allapot': 'jelolt', 'besorolas_proveniencia': '',
                   'proveniencia': 'scope=adat/thayer_szakaszok.tsv | forras=thayer_jelolt/sigla_gyujt.py (fejléc) | ts=%s' % ts})
    for r in ki:
        for m in FEJLEC:
            if '\t' in r.get(m, '') or '\n' in r.get(m, ''):
                raise ValueError('tab/sortörés: %s %s' % (r['forrasalak'], m))
    return ki


def fajl_szoveg(sorok, ts):
    fej = ['# FÉLIG KÉZI: a számoszlopokat és az új jelölt sorokat az eszkozok/thayer_jelolt/sigla_gyujt.py --ts %s írja; a tipus, '
           'jelentes, magyar_alak, allapot, besorolas_proveniencia kézi (az eszköz nem írja át). Séma: adat/SEMA.md 2.37.' % ts,
           '# forras: adat/thayer_szakaszok.tsv@%s + adat/thayer_forras_javitas.tsv@%s (nézet) + adat/elofordulasok.tsv@%s (gerinc) '
           '+ kód@%s'
           % (szolista.sha12(TB.TABLA), szolista.sha12(TB.JAV_TABLA), szolista.sha12(szolista.ELOFORDULASOK_UT),
              bont.sha256_fajl(os.path.abspath(__file__))[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(r.get(m, '') for m in FEJLEC) for r in sorok]) + '\n'


def kezi_valtozatlan(regi, uj):
    u = {r['forrasalak']: r for r in uj}
    for alak, r in regi.items():
        for m in KEZI:
            if u[alak].get(m, '') != r.get(m, ''):
                return '%s: a kézi `%s` oszlop változna' % (alak, m)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts')
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    ts = a.ts or (bont.fajl_ts(KI_UT) if a.ellenoriz and os.path.exists(KI_UT) else None) or datetime.date.today().isoformat()
    gy = gyujt()
    c = collections.Counter(d['gyujtes'] for d in gy.values())
    print('jelölt: %d (%s); a gerincszavakban előforduló: %d'
          % (len(gy), dict(c), sum(1 for d in gy.values() if d['gerinc'])))
    if a.meres:
        for alak, d in list(gy.items())[:80]:
            print('  %-18s %-13s %6d %5d %4d' % (alak, d['gyujtes'], d['elofordulas'], len(d['szocikk']), d['gerinc']))
        return 0
    regi = regi_tabla()
    sorok = osszefesul(gy, regi, ts)
    hiba = kezi_valtozatlan(regi, sorok)
    if hiba:
        print('HIBA: %s — megállok' % hiba)
        return 2
    szoveg = fajl_szoveg(sorok, ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            if f.read() != szoveg:
                print('ELTÉR: %s' % KI_UT)
                return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s (%d sor; besorolt: %d)' % (KI_UT, len(sorok), sum(1 for r in sorok if r.get('allapot') == 'besorolt')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
