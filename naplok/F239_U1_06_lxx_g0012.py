# -*- coding: utf-8 -*-
"""F239 U1 6. pont (LXX-híd, a G0012 oldal): az LXX minden ἄβυσσος-verse (G0012), és hogy a héber versben áll-e H8415; az ÚSZ G0012-helyei.
Csak olvas. Kimenet: naplok/F239_U1_TEREMT-001_lxx_g0012.tsv. TSV: split/join, csv nélkül."""
import sys, os
from collections import OrderedDict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
d = os.path.join(GY, 'konkordancia', 'LXX_OS')
vers = OrderedDict()
kulcs_nelkul = []
for f in sorted(os.listdir(d)):
    if not f.endswith('.tsv'):
        continue
    fej = None
    for s in open(os.path.join(d, f), encoding='utf-8'):
        if s.startswith('#') or not s.strip():
            continue
        c = s.rstrip('\n').split('\t')
        if fej is None:
            fej = c; continue
        r = dict(zip(fej, c))
        if (r.get('strong') or '').isdigit() and int(r['strong']) == 12:
            if not r['igehely_karoli']:
                kulcs_nelkul.append((f, r.get('igehely_lxx', '')))
                continue
            vers.setdefault(r['igehely_karoli'], []).append(r.get('szoalak', ''))
h8415 = set()
for r in L.load_tahot():
    if r['Strong-szám'] == 'H8415':
        h8415.add(r['Igehely'])
usz = sorted({r['Igehely'] for r in L.load_tagnt() if r['Strong-szám'] == 'G0012'}, key=L.parse_igehely)
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_lxx_g0012.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("# GENERÁLT: naplok/F239_U1_06_lxx_g0012.py | scope=LXX_OS-teljes (G0012) × TAHOT_kivonat.tsv (H8415) + TAGNT_kivonat.tsv (G0012) | forras=konkordancia/LXX_OS/*.tsv, TAHOT_kivonat.tsv, TAGNT_kivonat.tsv | ts=2026-11-23 | gerinc_elem: G0012 / H8415\n")
    f.write('gerinc_elem\tigehely\thely_tipusa\tlxx_alak\th8415_a_heber_versben\n')
    for ig, al in vers.items():
        f.write('G0012\t%s\tLXX-vers (ἄβυσσος)\t%s\t%s\n' % (ig, ' | '.join(al), 'igen' if ig in h8415 else 'NEM (az LXX többlete vagy más héber szó)'))
    for ig in usz:
        f.write('G0012\t%s\tÚSZ-hely (nem LXX-vers)\t\t-\n' % ig)
lx_nem = [v for v in vers if v not in h8415]
print('LXX G0012 versek:', len(vers), '| ebből H8415 a héber versben:', len(vers) - len(lx_nem), '| nem:', len(lx_nem))
print('H8415 versek, amelyekben az LXX-ben nincs G0012:', len([v for v in h8415 if v not in vers]), '| H8415 versek összesen:', len(h8415))
print('LXX-ban G0012, héberben nem H8415:', ', '.join(lx_nem))
print('ÚSZ G0012 versek:', len(usz))
print('G0012 token Károli-kulcs nélkül (kihagyva):', len(kulcs_nelkul), kulcs_nelkul[:5])
