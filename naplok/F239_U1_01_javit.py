# -*- coding: utf-8 -*-
"""A _lxx_hid.tsv-ben a Jób 41:32 kétszer állt (a H8415-scan már tartalmazza); a második sor törlése."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
p = 'naplok/F239_U1_TEREMT-001_lxx_hid.tsv'
sorok = open(p, encoding='utf-8', newline='').read().split('\n')
ki, lattam = [], set()
for s in sorok:
    k = s.split('\t')[:2]
    if len(k) == 2 and not s.startswith('#') and k[0] != 'gerinc_elem':
        if tuple(k) in lattam:
            continue
        lattam.add(tuple(k))
    ki.append(s)
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(ki))
print(len(sorok), '->', len(ki))
