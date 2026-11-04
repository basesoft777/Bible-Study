#!/usr/bin/env python
"""B3: az `atiras` hibaosztály hatásának mérése a BDB-fordításokon és a lexikonlapokon.

1. A `adat/bdb_forras_javitas.tsv` `atiras` sorai Strongonként (javitva / jelolt_marad).
2. Az `adat/forditasok.tsv` BDB-sorai, amelyek `forditas_hu` mezője „®”-t hordoz: a megjelenítési csere
   (`bdb_rovidites.atiras_javit`) után marad-e torz jel. Ahol marad, ott a csere nem elég (új fordítás vagy
   forrásdöntés kell); ahol nem marad, újrafordítás nem kell.
3. A `lexikon/*.md` lapok „®”-előfordulásai (a generált lapokon).

Használat: python naplok/B3_ATIRAS_meres.py  (csak olvas; a kimenet a konzolra)
TSV: split('\\t'), csv modul nélkül.
"""
import collections
import glob
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import bdb_rovidites as BR  # noqa: E402


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def main():
    jav = [d for d in tsv(os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')) if d['hiba'] == 'atiras']
    st = collections.defaultdict(collections.Counter)
    for d in jav:
        st[d['strong']][d['allapot']] += 1
    print('## 1. atiras sorok: %d sor, %d Strong' % (len(jav), len(st)))
    for allapot in ('javitva', 'jelolt_marad'):
        s = sorted(k for k, v in st.items() if v[allapot])
        print('- %s: %d sor, %d Strong: %s' % (allapot, sum(v[allapot] for v in st.values()), len(s), ', '.join(s)))

    print('\n## 2. BDB-fordítások „®”-vel (forditas_hu)')
    print('| Strong | jelentes_szam | allapot | torz előtte | torz utána | teendő |')
    print('|---|---|---|---|---|---|')
    marad = []
    for d in tsv(os.path.join(GYOKER, 'adat', 'forditasok.tsv')):
        if d['szotar'] != 'BDB' or '®' not in d['forditas_hu']:
            continue
        ut = BR.atiras_javit(d['forditas_hu'], d['strong'])
        elotte, utana = d['forditas_hu'].count('®'), ut.count('®')
        if d['allapot'] == 'elavult':
            teendo = 'nincs (elavult sor, nem renderel)'
        elif utana:
            teendo = 'a forrás `jelolt_marad`: előbb forrásdöntés, utána esetleg új fordítás'
            marad.append(d['strong'])
        else:
            teendo = 'nincs: a megjelenítés javítja'
        print('| %s | %s | %s | %d | %d | %s |' % (d['strong'], d['jelentes_szam'], d['allapot'], elotte, utana, teendo))
    print('\nÚj fordítást vagy forrásdöntést kívánó Strong: %s' % (', '.join(sorted(set(marad))) or 'nincs'))

    print('\n## 3. Lexikonlapok „®”-vel')
    for ut in sorted(glob.glob(os.path.join(GYOKER, 'lexikon', '*.md'))):
        with open(ut, encoding='utf-8') as f:
            n = f.read().count('®')
        if n:
            print('- %s: %d' % (os.path.basename(ut), n))
    print('(vége)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
