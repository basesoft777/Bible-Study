"""N-F65b mérése egy motívumon: az élő lexikonoldal azonosítás/megbízhatóság-címkéi
egyeznek-e az `adat/elofordulasok.tsv` soraival.

Használat: python naplok/NF65b_ISTENTISZT_meres.py [MOTIVUM-ID]   (alapértelmezés: ISTENTISZT-001)
Csak olvas; a TSV-t split('\\t')-tel bontja (CLAUDE.md, TSV-olvasás).
"""
import os
import re
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MID = sys.argv[1] if len(sys.argv) > 1 else 'ISTENTISZT-001'
CIMKE = re.compile(r'(magas|közepes|alacsony) · (tartalom-alapú|szó-szintű-gépi|[^\s|\[]+)')


def main():
    sorok = [l.rstrip('\n').split('\t')
             for l in open(os.path.join(REPO, 'adat', 'elofordulasok.tsv'), encoding='utf-8')
             if not l.startswith('#')]
    fej = sorok[0]
    ix = {k: i for i, k in enumerate(fej)}
    adat = {}
    for r in sorok[1:]:
        if len(r) < len(fej) or r[ix['id']] != MID:
            continue
        adat[r[ix['igehely']]] = (r[ix['megbizhatosag']], r[ix['azonositas_modja']])

    lap = open(os.path.join(REPO, 'lexikon', MID + '_TUDOMANYOS.md'), encoding='utf-8').read()
    lapon = {}
    for sor in lap.splitlines():
        m = re.match(r'\| \[([^\]]+)\]\(#ige-', sor)
        g = CIMKE.search(sor) if m else None
        if m and g and m.group(1) in adat:
            lapon[m.group(1)] = (g.group(1), g.group(2))

    print('motívum:', MID)
    print('adat:', dict(Counter(adat.values())))
    print('lap :', dict(Counter(lapon.values())))
    hiany = sorted(set(adat) - set(lapon))
    elteres = [(ig, adat[ig], lapon[ig]) for ig in sorted(lapon) if adat[ig] != lapon[ig]]
    print('a lapon címke nélkül:', len(hiany), hiany)
    print('eltérő címke:', len(elteres))
    for e in elteres:
        print('  ', e)
    return 1 if (hiany or elteres) else 0


if __name__ == '__main__':
    sys.exit(main())
