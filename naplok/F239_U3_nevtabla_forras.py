"""F239 U3 — két forrás olvasói neve az olvasói névtáblában (adat/olvasoi_nevtabla.tsv, `forras` típus): a TEREMT-001
kézi forrásának proveniencia-sorai a BDB teljes szövegét (B22) és a Thayer szakaszait (B20) nevezik, és a lapgenerátor
a forrássor bemenetét olvasói névvel írja ki. Csak hiányzó sort ír. Futtatás: python naplok/F239_U3_nevtabla_forras.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
UT = 'adat/olvasoi_nevtabla.tsv'
UJ = [('B22', 'a BDB-szótár teljes szövege'), ('B20', 'a Thayer-szótár szakaszai')]
nyers = open(UT, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
s = nyers.split(nl)
eredet = next(l.split('\t')[3] for l in s if l.startswith('forras\tB03\t'))
meglevo = {tuple(l.split('\t')[:2]) for l in s if '\t' in l}
while s and s[-1] == '':
    s.pop()
uj = ['\t'.join(['forras', k, n, eredet]) for k, n in UJ if ('forras', k) not in meglevo]
open(UT, 'w', encoding='utf-8', newline='').write(nl.join(s + uj + ['']))
print('+%d sor' % len(uj))
