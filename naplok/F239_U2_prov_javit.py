"""F239 U2 — a Jel 20:1 és 20:3 új előfordulás-sorának proveniencia-mezőjéből a nem kulcs=érték alakú toldalék
kivéve (ellenoriz.py 3. szabály); a döntés nyoma a jelölt-sor `dontes_ref`-jében és a lépésnaplóban áll.

python naplok/F239_U2_prov_javit.py [--ir]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/elofordulasok.tsv'
TOLD = ' | a Jel 20:1-3 sor kettéválasztása: szerkesztői döntés (a felhasználó, 2026-11-23)'

with open(UT, encoding='utf-8', newline='') as f:
    s = f.read().split('\n')
idx = [i for i, x in enumerate(s) if x.startswith(('TEREMT-001\tJel 20:1\t', 'TEREMT-001\tJel 20:3\t')) and TOLD in x]
if len(idx) != 2:
    sys.exit('HIBA: %d sor (2 kell)' % len(idx))
u = list(s)
for i in idx:
    u[i] = s[i].replace(TOLD, '')
print('módosul: %s' % [i + 1 for i in idx])
if '--ir' in sys.argv:
    with open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(u))
    print('írva')
