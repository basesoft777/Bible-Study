#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F34 M0: a forras-talalatok vetitese az adat/forditasok.tsv soraira (csak olvas).
Futtatas: python naplok/F34_M0_felmeres.py ; python naplok/F34_M0_forditasok.py
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, 'naplok')
HU = {'1Ki': '1Kir', '2Ki': '2Kir', 'Gen': '1Móz', 'Exod': '2Móz', 'Lev': '3Móz', 'Num': '4Móz', 'Deut': '5Móz', 'Josh': 'Józs',
      'Judg': 'Bír', 'Ruth': 'Ruth', '1Sam': '1Sám', '2Sam': '2Sám', '1Kin': '1Kir', '2Kin': '2Kir',
      '1Chr': '1Krón', '2Chr': '2Krón', 'Ezra': 'Ezsd', 'Neh': 'Neh', 'Esth': 'Eszt', 'Job': 'Jób',
      'Psa': 'Zsolt', 'Prov': 'Péld', 'Eccl': 'Préd', 'Song': 'Én', 'Isa': 'Ézs', 'Jer': 'Jer',
      'Lam': 'JSir', 'Ezek': 'Ez', 'Dan': 'Dán', 'Hos': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós',
      'Obad': 'Abd', 'Jonah': 'Jón', 'Mic': 'Mik', 'Nah': 'Náh', 'Hab': 'Hab', 'Zeph': 'Sof',
      'Hag': 'Hag', 'Zech': 'Zak', 'Mal': 'Mal'}

lista = [l.split('\t') for l in open('naplok/F34_M0_lista.tsv', encoding='utf-8').read().split('\n')[1:] if l]
per_strong = {}
for r in lista:
    per_strong.setdefault(r[1], []).append(r)

sorok = open('adat/forditasok.tsv', encoding='utf-8').read().split('\n')
fej = sorok[1].split('\t')
ix = {k: i for i, k in enumerate(fej)}
print('sor\tszotar\tstrong\tjelentes\tallapot\tforras_hit\thu_hit_A\thu_hit_B\thu_hit_R')
osszes = 0
for n, l in enumerate(sorok, 1):
    if n <= 2 or not l:
        continue
    p = l.split('\t')
    if p[ix['szotar']] != 'BDB':
        continue
    st = p[ix['strong']]
    if st not in per_strong:
        continue
    hu = p[ix['forditas_hu']]
    cnt = {'A': [], 'B': [], 'R': []}
    for r in per_strong[st]:
        if r[5] not in cnt:
            continue
        m = re.match(r'(\S+) (\d+):(\d+)', r[3])
        k = '%s %s:%s' % (HU[m.group(1)], m.group(2), m.group(3))
        if re.search(r'(?<![\wÀ-ɏ])' + re.escape(k) + r'(?!\d)', hu):
            cnt[r[5]].append(k)
    print('%d\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s' % (n, p[0], st, p[ix['jelentes_szam']], p[ix['allapot']],
          len(per_strong[st]), ','.join(cnt['A']) or '-', ','.join(cnt['B']) or '-', ','.join(cnt['R']) or '-'))
