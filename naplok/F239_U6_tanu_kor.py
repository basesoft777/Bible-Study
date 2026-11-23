# -*- coding: utf-8 -*-
"""F239 U6 (D25) — a Chain Lineage-tanúsorok kora: a CL `century` a szerző születési százada; a kézi érték a HCF-index
évéből (konkordancia/Tanu_atyak_index.tsv: Eusebius of Caesarea 339, Hippolytus of Rome 235). 1) a SPEC kap `kor`
oszlopot; 2) a adat/visszhang_tanuk.tsv érintett sorainak `kor` mezője ugyanerre (a tanu_kinyer.py cl újrafuttatása
ugyanezt adná; hálózati lekérdezés nélkül). Minden más sor bájtra azonos. Futtatás: [--ir]"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOR = {'Eusebius of Caesarea': ('Euszébiosz', '4. sz. (HCF: 339)'), 'Hippolytus': ('Hippolütosz', '3. sz. (HCF: 235)')}
# a HCF-év ellenőrzése a forrásban
hcf = {}
for s in open(os.path.join(GY, 'konkordancia', 'Tanu_atyak_index.tsv'), encoding='utf-8'):
    f = s.rstrip('\r\n').split('\t')
    if len(f) > 4 and f[3] in ('Eusebius of Caesarea', 'Hippolytus of Rome'):
        hcf.setdefault(f[3], set()).add(f[4])
print('HCF-évek:', hcf)
assert hcf == {'Eusebius of Caesarea': {'339'}, 'Hippolytus of Rome': {'235'}}

def cser(ut, fn):
    nyers = open(ut, encoding='utf-8', newline='').read()
    sorok = nyers.split('\n')
    uj = fn(sorok)
    valt = [i for i in range(len(sorok)) if sorok[i] != uj[i]]
    print(os.path.basename(ut), 'változott sor:', len(valt))
    for i in valt:
        print('  -', sorok[i][:160]); print('  +', uj[i][:160])
    if '--ir' in sys.argv:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(uj))
    return len(valt)

def spec(sorok):
    uj = list(sorok)
    fej = sorok[0].rstrip('\r').split('\t'); assert 'kor' not in fej
    uj[0] = sorok[0].rstrip('\r') + '\tkor' + ('\r' if sorok[0].endswith('\r') else '')
    for i in range(1, len(sorok)):
        if not sorok[i].strip(): continue
        cr = '\r' if sorok[i].endswith('\r') else ''
        f = sorok[i].rstrip('\r').split('\t'); d = dict(zip(fej, f))
        uj[i] = sorok[i].rstrip('\r') + '\t' + (KOR[d['szerzo']][1] if d['szerzo'] in KOR else '') + cr
    return uj

def tabla(sorok):
    uj = list(sorok)
    fej = [s for s in sorok if not s.startswith('#')][0].split('\t')
    jk, jt, jf = fej.index('kor'), fej.index('tanu'), fej.index('forras')
    nevek = {v[0]: v[1] for v in KOR.values()}
    for i, s in enumerate(sorok):
        f = s.split('\t')
        if s.startswith('#') or len(f) != len(fej) or f[0] != 'TEREMT-001': continue
        if f[jf] == 'chain_lineage' and f[jt] in nevek:
            f[jk] = nevek[f[jt]]; uj[i] = '\t'.join(f)
    return uj

n1 = cser(os.path.join(GY, 'naplok', 'F239_U1b_cl_spec.tsv'), spec)
n2 = cser(os.path.join(GY, 'adat', 'visszhang_tanuk.tsv'), tabla)
assert n2 == 4, n2
