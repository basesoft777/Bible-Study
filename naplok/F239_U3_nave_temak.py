"""F239 U3 — a TEREMT-001 kiválasztott Nave-témáinak és altételeinek angol neve (a magyar név tervezetéhez)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'eszkozok'))
import szerep_nave as N
sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sorok = []
for s in open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8'):
    pass
fej = None
for s in open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8'):
    s = s.rstrip('\r\n')
    if not s or s.startswith('#'):
        continue
    m = s.split('\t')
    if fej is None:
        fej = m; continue
    r = dict(zip(fej, m))
    if r['id'] == 'TEREMT-001':
        sorok.append(r)
for t in N.nave_temak(sorok):
    print('%s\t\t%s\t%s' % (t['tema_id'], t['tema'], N.sha1(t['tema'])), ' | ', ', '.join(t['motivumversek']))
    for c, vs in t['cimkek'].items():
        if c:
            print('%s\t%s\t%s\t%s' % (t['tema_id'], c, c, N.sha1(c)), ' | ', ', '.join(vs))
