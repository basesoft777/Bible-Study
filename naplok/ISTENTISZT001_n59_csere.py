"""A jeloltek.tsv ISTENTISZT-001 / Zsolt 99:6 sorában a kiosztott N-F126a → N59 (szamkiosztas). Csak az
azonosító; split('\t') / '\t'.join(); írás előtt soronkénti összevetés, pontosan egy sor változhat.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UT = 'adat/jeloltek.tsv'
with open(UT, encoding='utf-8', newline='') as f:
    sorok = f.read().split('\n')
uj = list(sorok)
for i, s in enumerate(sorok):
    m = s.split('\t')
    if len(m) > 2 and m[0] == 'ISTENTISZT-001' and m[1] == 'Zsolt 99:6' and 'N-F126a' in s:
        uj[i] = '\t'.join(x.replace('N-F126a', 'N59') for x in m)
        print(f'{i + 1}. sor: {s.count("N-F126a")} csere')
elter = [i for i in range(len(sorok)) if sorok[i] != uj[i]]
if len(elter) != 1 or 'N-F126a' in '\n'.join(uj):
    raise SystemExit(f'váratlan: {elter}')
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
