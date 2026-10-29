"""A kiejtés-szabály egyszeri mérése egy lexikonlapon (DT-F131w; ISTENTISZT-001 arany lap, 2026-10-29). Csak olvas.

A szabály és az elemzés az `eszkozok/kiejtes_szoveg.py`-ban (ugyanazt használja a generátor pótlása): szakaszonként az
első előfordulás, minden cím és táblázatfej; forrásidézetben nem kell. A kimenet: a hiányzó kiejtések száma generált /
kézi részre bontva, szavanként, és a héber alakok közül azok, amelyeknek nincs jóváhagyott kiejtése (a felhasználó dönt).
A végleges ellenőrző-szabály a #125-é.

  python naplok/KIEJTES_elso_elofordulas_meres.py lexikon/ISTENTISZT-001_TUDOMANYOS.md [--reszletes]
"""
import argparse
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok'))
import kiejtes_szoveg as KSZ  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lap')
    ap.add_argument('--reszletes', action='store_true')
    a = ap.parse_args()
    with open(a.lap, encoding='utf-8') as f:
        h = KSZ.elemez(f.read())
    c = collections.Counter(x[2] for x in h)
    jova = [x for x in h if not x[5]]
    print('hiányzó kiejtés: %d (generált %d, kézi %d); ebből jóváhagyott kiejtés nélküli héber alak: %d'
          % (len(h), c['generált'], c['kézi'], len(jova)))
    for resz in ('generált', 'kézi'):
        szavak = collections.Counter((x[3], x[5] or '— (nincs jóváhagyott alak)') for x in h if x[2] == resz)
        print('\n== %s: %d különböző szó ==' % (resz, len(szavak)))
        for (szo, jav), n in szavak.most_common():
            print('  %s ×%d  → %s' % (szo, n, jav))
    if a.reszletes:
        print('\n== soronként ==')
        for i, sz, resz, szo, mi, jav in h:
            print('%5d  %-8s  %-16s  %-30s  %-20s  %s' % (i, resz, mi, szo, jav or '—', sz[:50]))


if __name__ == '__main__':
    main()
