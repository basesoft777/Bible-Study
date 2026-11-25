"""F239 U2 — a bírálat (V5) után az Ez 31:15 seól-kapcsolat két olvasói szövege: a mélység itt a kozmikus víz, nem
„a halál mélye” (egyszeri szkript; a kapcsolat maga, DT-F239a, változatlan).

python naplok/F239_U2_biralat_javit.py [--ir]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

CSERE = [
    ('adat/jeloltek.tsv', 'TEREMT-001\tEz 31:15\t',
     'a mélység a halál közelségének képe (vö. Jón 2:6, Zsolt 71:20), a seól a holtak helye.',
     'a mélység a kozmikus víz, a seól a holtak helye.'),
    ('adat/motivum_kapcsolatok.tsv', 'ALVIL-001\tEz 31:15\t\tTEREMT-001\tEz 31:15\t',
     'a cédrus a seólba száll, a mélység gyászba borul: a halál helye és a halál mélye egy versben',
     'a cédrus a seólba száll, Isten miatta gyászba borítja és visszatartja a mélységet: a holtak helye és a kozmikus '
     'víz egy versben'),
]

for ut, elotag, regi, uj in CSERE:
    with open(ut, encoding='utf-8', newline='') as f:
        s = f.read().split('\n')
    idx = [i for i, x in enumerate(s) if x.startswith(elotag) and regi in x]
    if len(idx) != 1:
        sys.exit('HIBA: %s: %d találat (1 kell)' % (ut, len(idx)))
    u = list(s)
    u[idx[0]] = s[idx[0]].replace(regi, uj)
    print('%s: sor %d' % (ut, idx[0] + 1))
    if '--ir' in sys.argv:
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(u))
