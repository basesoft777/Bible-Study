#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F34 M0: a felmeres-naplo (naplok/F34_M0_felmeres.md) szakaszainak generalasa a lista TSV-bol."""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

rows = [l.split('\t') for l in open('naplok/F34_M0_lista.tsv', encoding='utf-8').read().split('\n')[1:] if l]
def tabla(osz):
    per = {}
    for r in rows:
        if r[5] == osz:
            per.setdefault(r[1], []).append(r)
    out = ['| Strong | forrás-sor | hibás -> javított |', '|---|---|---|']
    for st in sorted(per):
        rs = per[st]
        out.append('| %s | %s | %s |' % (st, rs[0][0], '; '.join('%s -> %s' % (r[3], r[4]) for r in rs)))
    return '\n'.join(out)
print('## A\n' + tabla('A'))
print('## B\n' + tabla('B'))
print('## R\n' + tabla('R'))
