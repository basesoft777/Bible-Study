import sys, json
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Users\bases\Desktop\Bible-Study\adat'
ID = 'ISTENTISZT-001'

def olvas(nev):
    fej, sorok = None, []
    with open(f'{ROOT}\\{nev}', encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s or s.startswith('#'):
                continue
            m = s.split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    return sorok

mot = [r for r in olvas('motivumok.tsv') if r['id'] == ID][0]
elo = [r for r in olvas('elofordulasok.tsv') if r['id'] == ID]
jel = [r for r in olvas('jeloltek.tsv') if r['id'] == ID]
kap = [r for r in olvas('kapcsolatok.tsv') if r['id'] == ID]
out = {'mot': mot, 'elo': elo, 'jel': jel, 'kap': kap}
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
print(len(elo), len(jel), len(kap))
print(Counter(r['dontes'] for r in jel))
print(Counter(r['megbizhatosag'] for r in jel))
print(Counter(r['tipus'] for r in kap), Counter(r['funkcio'][:30] for r in kap).most_common(5))
print(mot.keys())
for r in jel:
    if r['dontes'] != 'beépítve':
        print(r['igehely'], '|', r['dontes'], '|', r['indoklas'][:120])
print(kap[0])
