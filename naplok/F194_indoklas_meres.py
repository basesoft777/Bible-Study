"""F194 (K47, K48, K04): az ISTENTISZT-001 jelöltjeinek `indoklas`-mezője az olvasói kapu indoklás-szabályaival mérve.

A generált lap helyett közvetlenül az adatot méri (`adat/jeloltek.tsv`), az `eszkozok/olvasoi_kapu.py` mintáival:
INDOKLAS (írás kiejtés nélkül, más sorra hivatkozás, munkajavaslat), NEVELO („a” magánhangzó előtt), BELSO-jellegű
belső jelek (DT/N/F-azonosító, fájlnév, „tanulmány”, „napló”, „study”, „D-minta”, „gerinc”, „felhasználó”).
Csak olvas. Futtatás: python naplok/F194_indoklas_meres.py [--id ISTENTISZT-001] [--reszletes]
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok'))
import olvasoi_kapu as ok  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BELSO_RX = (
    (re.compile(r'\bDT-?F?\d+[a-z]?\b|\bN-?F?\d+[a-z]?\b|\bF\d{2,3}\b|#\d+'), 'belső azonosító'),
    (re.compile(r'\w+\.(?:tsv|md|py)\b'), 'fájlnév'),
    (re.compile(r'[Tt]anulmány|\bstudy\b|[Nn]apló|\bQ\d\b'), 'tanulmányra/naplóra hivatkozik'),
    (re.compile(r'\b[A-D]-mint[aá]'), 'belső tipológia-címke'),
    (re.compile(r'[Gg]erinc|[Ff]elhasználó|orkesztrátor|\bscan\b|\btoken'), 'munkaszó'),
    (re.compile(r'\b[HG]\d{4}\b'), 'Strong-szám'),
)


def olvas(ut):
    fej, ki = None, []
    for n, s in enumerate(open(ut, encoding='utf-8').read().split('\n'), 1):
        if not s or s.startswith('#'):
            continue
        m = s.split('\t')
        if fej is None:
            fej = m
            continue
        ki.append((n, dict(zip(fej, m))))
    return ki


def merj(ind):
    hibak = []
    for f in ok.iras_kiejtes_nelkul(ind):
        hibak.append(('írás kiejtés nélkül', f))
    for rx, nev in ok.INDOKLAS_TILOS + BELSO_RX:
        for m in rx.finditer(ind):
            hibak.append((nev, m.group(0)))
    for m in ok.NEVELO_RX.finditer(ind):
        hibak.append(('névelő', ind[m.start():m.start() + 12]))
    return hibak


def main():
    mid = 'ISTENTISZT-001'
    if '--id' in sys.argv:
        mid = sys.argv[sys.argv.index('--id') + 1]
    sorok = [(n, r) for n, r in olvas(os.path.join(GYOKER, 'adat', 'jeloltek.tsv')) if r['id'] == mid]
    hibas = 0
    osztaly = {}
    for n, r in sorok:
        h = merj(r['indoklas'])
        if h:
            hibas += 1
            for nev, _ in h:
                osztaly[nev] = osztaly.get(nev, 0) + 1
            if '--reszletes' in sys.argv:
                print('%d\t%s\t%s\t%s' % (n, r['igehely'], r['dontes'], '; '.join('%s: %s' % x for x in h)))
    print('%s: %d sor, ebből hibás indoklás: %d' % (mid, len(sorok), hibas))
    for k, v in sorted(osztaly.items(), key=lambda x: -x[1]):
        print('  %s: %d' % (k, v))


if __name__ == '__main__':
    main()
