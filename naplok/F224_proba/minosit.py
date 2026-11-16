# -*- coding: utf-8 -*-
"""F224.13 vak minta minősítése: K57 (1 074) és K64 (573) a forrás állapotán."""
import sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eszkozok')
import proza_allitas as P

LANC14 = 'G1311 G1944 G2671 G5351 G5356 H0127 H0779 H2403 H2555 H6093 H6975 H7043 H7451 H7843'.split()
HEB_TOBBI = [s for s in LANC14 if s.startswith('H') and s not in ('H7451', 'H7043')]

# K64: TAHOT
versei = {}
for d in P.tsv_dict(P.T_TAHOT):
    s = P.strong_norm(d.get('Strong-szám', ''))
    if s in LANC14:
        versei.setdefault(s, set()).add(d['Igehely'])
tobbi = set().union(*[versei.get(s, set()) for s in HEB_TOBBI])
ra, qa = versei.get('H7451', set()), versei.get('H7043', set())
print('H7451 vers:', len(ra), '| tobbi lanc nelkul:', len(ra - tobbi), '| tobbi es qalal nelkul:', len(ra - tobbi - qa))
print('H7043 vers:', len(qa), '| tobbi lanc nelkul:', len(qa - tobbi), '| tobbi es ra nelkul:', len(qa - tobbi - ra))
print('ra vagy qa, tobbi nelkul:', len((ra | qa) - tobbi))

# K57: a bdb/thayer karoli_vers a f6da955e-n
def karoli_versek(tartalom, strong_mezo='strong'):
    sorok = [s for s in tartalom.split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = set()
    for s in sorok[1:]:
        d = dict(zip(fej, s.split('\t')))
        if P.strong_norm(d.get(strong_mezo, '')) in LANC14 and d.get('karoli_vers'):
            ki.add(d['karoli_vers'])
    return ki
for commit in ('f6da955e', 'HEAD'):
    b = subprocess.run(['git', 'show', commit + ':adat/bdb_vers_jelentes.tsv'], capture_output=True).stdout.decode('utf-8')
    t = subprocess.run(['git', 'show', commit + ':adat/thayer_vers_jelentes.tsv'], capture_output=True).stdout.decode('utf-8')
    fb = b.split('\n', 3)
    bv, tv = karoli_versek(b), karoli_versek(t)
    print(commit, 'BDB', len(bv), 'Thayer', len(tv), 'unio', len(bv | tv))
