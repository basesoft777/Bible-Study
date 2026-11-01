"""F120 (3.5, DT-F120a (a)): a régi (F71.2) és az újragenerált BSB_Strongs.tsv összevetése (csak olvas).

Mér: sorszám, Számozás-eloszlás, fejezetenkénti sor-különbség (a változott fejezetek listája), a csak az egyikben meglévő
fejezetek, a Zsoltárok bájtazonossága (E5) és a Zsolt 13 sorai, a kulcsváltások (a régiben X kulcson álló BSB-szó az újban
Y kulcson) fejezetenként.
Használat: python naplok/F120_bsb_osszevetes.py <regi_BSB_Strongs.tsv> [uj_BSB_Strongs.tsv]
(a régi: git show <alap>:konkordancia/BSB_Strongs.tsv)
"""
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)([a-z]?)$')


def olvas(path):
    with open(path, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    return [s for s in sorok[1:] if s]


def fejezet(sor):
    m = STEP.match(sor.split('\t', 1)[0])
    return (m.group(1), int(m.group(2))) if m else ('?', 0)


def main():
    regi = olvas(sys.argv[1])
    uj = olvas(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'konkordancia', 'BSB_Strongs.tsv'))
    print('sorok: régi %d, új %d, különbség %+d' % (len(regi), len(uj), len(uj) - len(regi)))
    for nev, t in (('régi', regi), ('új', uj)):
        print('Számozás, %s: %s' % (nev, dict(sorted(Counter(s.split('\t')[6] for s in t).items()))))
    fr, fu = defaultdict(list), defaultdict(list)
    for s in regi:
        fr[fejezet(s)].append(s)
    for s in uj:
        fu[fejezet(s)].append(s)
    valtozott = sorted(f for f in set(fr) | set(fu) if fr.get(f) != fu.get(f))
    print('változott fejezet: %d (azonos: %d)' % (len(valtozott), len(set(fr) | set(fu)) - len(valtozott)))
    for f in valtozott:
        r, u = fr.get(f, []), fu.get(f, [])
        # a kulcsváltás: az első 5 oszlop (kulcs nélkül) azonos sorrendben -> csak a kulcs/Számozás változott
        rk = [s.split('\t', 1)[1].rsplit('\t', 1)[0] for s in r]
        uk = [s.split('\t', 1)[1].rsplit('\t', 1)[0] for s in u]
        if not r:
            tipus = 'csak az újban'
        elif not u:
            tipus = 'csak a régiben (kimaradt)'
        elif rk == uk:
            kul = Counter((a.split('\t', 1)[0], b.split('\t', 1)[0]) for a, b in zip(r, u) if a.split('\t', 1)[0] != b.split('\t', 1)[0])
            szam = Counter((a.rsplit('\t', 1)[1], b.rsplit('\t', 1)[1]) for a, b in zip(r, u) if a.rsplit('\t', 1)[1] != b.rsplit('\t', 1)[1])
            tipus = 'azonos szavak; kulcsváltás %d sor, Számozás-váltás %s' % (sum(kul.values()), dict(szam))
        else:
            tipus = 'más tartalom'
        print('  %s %d\trégi %d sor\túj %d sor\t%s' % (f[0], f[1], len(r), len(u), tipus))
    zr = [s for s in regi if s.startswith('Psa.')]
    zu = [s for s in uj if s.startswith('Psa.')]
    print('Zsoltárok (E5): %s (%d / %d sor)' % ('BÁJTRA AZONOS' if zr == zu else 'ELTÉR', len(zr), len(zu)))
    z13 = [s for s in uj if s.startswith('Psa.13.')]
    print('Zsolt 13 (F71 kézi kivétel): %s' % ('azonos' if z13 == [s for s in regi if s.startswith('Psa.13.')] else 'ELTÉR'))
    print('proveniencia: scope=BSB_Strongs.tsv régi/új | eszkoz=naplok/F120_bsb_osszevetes.py | ts=2026-11-01')


if __name__ == '__main__':
    main()
