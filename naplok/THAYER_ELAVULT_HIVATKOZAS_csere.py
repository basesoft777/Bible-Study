"""F155.4: a 7 `elavult` Thayer-sor megjegyzésében DT-F132c -> DT329 (DT-F155a (a)). Csak split/join, soronkénti összevetéssel."""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/forditasok.tsv'
with open(UT, encoding='utf-8', newline='') as f:
    szoveg = f.read()
sorok = szoveg.split('\n')
fej = sorok[1].split('\t')
i_all, i_megj = fej.index('allapot'), fej.index('megjegyzes')
uj, valt = [], []
for n, s in enumerate(sorok):
    m = s.split('\t')
    if n > 1 and len(m) == len(fej) and m[0] == 'Thayer' and m[i_all] == 'elavult' and 'DT-F132c' in m[i_megj]:
        m[i_megj] = m[i_megj].replace('DT-F132c', 'DT329')
        t = '\t'.join(m)
        # összevetés: egyetlen mező tér el
        a, b = s.split('\t'), t.split('\t')
        if [k for k in range(len(a)) if a[k] != b[k]] != [i_megj] or '\t'.join(a) != s:
            raise SystemExit('eltérés a %d. sornál' % (n + 1))
        valt.append(n + 1)
        s = t
    uj.append(s)
if len(valt) != 7:
    raise SystemExit('várt 7 sor, talált %d: %s' % (len(valt), valt))
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
print('módosított sorok:', valt)
