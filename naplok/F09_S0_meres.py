"""F09 S0 mérés: a 8 motívum Strong-tokenhalmaza, hash-ek, importok. Csak olvas."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import hashlib, os, glob
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
M8 = ['ALVIL-001','ANTROP-001','HAMART-001','HODIT-001','ISTENTISZT-001','KIRALY-001','MENNY-001','TEREMT-001']

def rd(p):
    with open(os.path.join(R, p), encoding='utf-8') as f:
        return [l.rstrip('\n').split('\t') for l in f if not l.startswith('#') and l.strip()]

rows = rd('adat/elofordulasok.tsv')
h = rows[0]; ix = {k: i for i, k in enumerate(h)}
ids = {}
for r in rows[1:]:
    ids.setdefault(r[ix['id']], 0); ids[r[ix['id']]] += 1
print('azonositok es sorok:', ids)
import re
tok = {}
for r in rows[1:]:
    if r[ix['id']] in M8:
        for t in re.split(r'[;,+ ]+', r[ix['strong']].strip()):
            if re.match(r'^[HG]\d+', t):
                tok.setdefault(r[ix['id']], set()).add(t)
allH = set(); allG = set()
for k, v in sorted(tok.items()):
    print(k, sorted(v))
    for t in v:
        (allH if t[0] == 'H' else allG).add(t)
print('H', len(allH), sorted(allH))
print('G', len(allG), sorted(allG))
print('---- elo 9. motivum:')
for k in ids:
    if k not in M8:
        s = set()
        for r in rows[1:]:
            if r[ix['id']] == k:
                s.update(t for t in re.split(r'[;,+ ]+', r[ix['strong']].strip()) if re.match(r'^[HG]\d+', t))
        print(k, sorted(s))
print('---- hash')
for f in sorted(glob.glob(os.path.join(R, 'lexikon', '*_TUDOMANYOS.md')) + glob.glob(os.path.join(R, 'lexikon', '*_TORZSCIKK.md'))):
    print(hashlib.sha256(open(f, 'rb').read()).hexdigest(), os.path.basename(f))

print('---- S0.2/3 UBS DBH jelentesek/anomaliak a 24 H-tokenre')
HT = sorted(allH)
mid = {}
for r in rd('konkordancia/UBS_DBH_jelentesek.tsv')[1:]:
    if r[0] in allH:
        mid.setdefault(r[0], set()).add(r[3])
for t in HT:
    print(t, 'jelentes-sor-szocikk:', len(mid.get(t, [])))
mids = set().union(*mid.values()) if mid else set()
an = [r for r in rd('konkordancia/UBS_DBH_anomaliak.tsv')[1:] if r[0] in mids]
print('anomalia a tokenek szocikkein:', len(an))
for r in an[:20]: print(r)
