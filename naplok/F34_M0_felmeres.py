#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F34 M0 felmeres (csak olvas): a BDB forrasban a `psi` hibas feloldasa.

Futtatas a repo gyokerebol: python naplok/F34_M0_felmeres.py
Kimenet: naplok/F34_M0_lista.tsv (minden talalat) + osszegzes a stdout-ra.
I/O: split('\t') / '\t'.join (csv modul nelkul).
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

MAX = {'Gen': 50, 'Exod': 40, 'Lev': 27, 'Num': 36, 'Deut': 34, 'Josh': 24, 'Judg': 21, 'Ruth': 4,
       '1Sam': 31, '2Sam': 24, '1Kin': 22, '2Kin': 25, '1Chr': 29, '2Chr': 36, 'Ezra': 10, 'Neh': 13,
       'Esth': 10, 'Job': 42, 'Psa': 150, 'Prov': 31, 'Eccl': 12, 'Song': 8, 'Isa': 66, 'Jer': 52,
       'Lam': 5, 'Ezek': 48, 'Dan': 12, 'Hos': 14, 'Joel': 4, 'Amos': 9, 'Obad': 1, 'Jonah': 4,
       '1Ki': 22, '2Ki': 25, 'Mic': 7, 'Nah': 3, 'Hab': 3, 'Zeph': 3, 'Hag': 2, 'Zech': 14, 'Mal': 4}
HU = {'1Ki': '1Kir', '2Ki': '2Kir', 'Gen': '1Móz', 'Exod': '2Móz', 'Lev': '3Móz', 'Num': '4Móz', 'Deut': '5Móz', 'Josh': 'Józs',
      'Judg': 'Bír', 'Ruth': 'Ruth', '1Sam': '1Sám', '2Sam': '2Sám', '1Kin': '1Kir', '2Kin': '2Kir',
      '1Chr': '1Krón', '2Chr': '2Krón', 'Ezra': 'Ezsd', 'Neh': 'Neh', 'Esth': 'Eszt', 'Job': 'Jób',
      'Psa': 'Zsolt', 'Prov': 'Péld', 'Eccl': 'Préd', 'Song': 'Én', 'Isa': 'Ézs', 'Jer': 'Jer',
      'Lam': 'JSir', 'Ezek': 'Ez', 'Dan': 'Dán', 'Hos': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós',
      'Obad': 'Abd', 'Jonah': 'Jón', 'Mic': 'Mik', 'Nah': 'Náh', 'Hab': 'Hab', 'Zeph': 'Sof',
      'Hag': 'Hag', 'Zech': 'Zak', 'Mal': 'Mal'}
BOOK = '|'.join(sorted(MAX, key=len, reverse=True))
PAT = re.compile(r'(?<![A-Za-z])(' + BOOK + r') (\d{1,3}):(\d+)')
PSWORD = re.compile(r'(Psalms?|Paslm|Psalm)\s*$')
SEP = re.compile(r'^(;|,|\s|\+|\(\w+\)|\d[\d:\-]*)*$')

def main():
    rows = []  # (sor, strong, regi, javitott, osztaly, megj, kontextus)
    forras = open('konkordancia/BDB_teljes_unabridged.tsv', encoding='utf-8').read().split('\n')
    for n, l in enumerate(forras, 1):
        if not l or n == 1:
            continue
        p = l.split('\t')
        strong = p[0]
        ms = list(PAT.finditer(l))
        flagged = {}
        for i, m in enumerate(ms):
            b, c, v = m.group(1), int(m.group(2)), m.group(3)
            if c <= MAX[b]:
                continue
            ps = bool(PSWORD.search(l[max(0, m.start() - 12):m.start()]))
            if b == 'Dan' and c == 22 and v == '14':
                osz, meg = 'KIZART', 'Dán 22:14: forráshiba (Dan 22:14), nem hatókör'
            elif c > 66 or (ps and c > MAX[b]):
                osz, meg = 'A', ('c>66: csak Zsoltár lehet' if c > 66 else 'Psalm-szó áll előtte')
            elif c > 50:
                osz, meg = 'B', 'c 51-66: Zsoltár vagy Ézs; nem eldönthető'
            else:
                osz, meg = 'B', 'c<=50: Zsoltár vagy más könyv (pl. Jób/Kivonulás); nem eldönthető'
            flagged[i] = osz
            rows.append([n, strong, m.start(), m.group(0), 'Psa %d:%s' % (c, v), osz, meg,
                         l[max(0, m.start() - 40):m.end() + 25].replace('\t', ' ')])
        # rejtett: lancban szomszedos, ugyanazzal a konyvnevvel, fejezet <= max
        for i, m in enumerate(ms):
            if i in flagged:
                continue
            b, c, v = m.group(1), int(m.group(2)), m.group(3)
            ps = bool(PSWORD.search(l[max(0, m.start() - 12):m.start()]))
            szomsz = None
            for j in (i - 1, i + 1):
                if j in flagged and ms[j].group(1) == b:
                    a, z = sorted((i, j))
                    kozte = l[ms[a].end():ms[z].start()]
                    if len(kozte) <= 12 and SEP.match(kozte):
                        szomsz = ms[j].group(0)
            if b != 'Psa' and (szomsz or ps):
                meg = ('láncban szomszédos jelölt hellyel: ' + szomsz) if szomsz else 'Psalm-szó áll előtte, de a fejezet létezik'
                rows.append([n, strong, m.start(), m.group(0), '(Psa %d:%s?)' % (c, v), 'R', meg,
                             l[max(0, m.start() - 40):m.end() + 25].replace('\t', ' ')])
    # rejtett eset a brief szerint (a fejezet letezik, a kapu nem jelzi): H7585 `Ezek 16:10`
    for n, l in enumerate(forras, 1):
        if l.startswith('H7585	'):
            i = l.find('Ezek 16:10 (|| ')
            if i >= 0:
                rows.append([n, 'H7585', i, 'Ezek 16:10', '(Psa 16:10?)', 'R',
                             'rejtett (brief): a szovegkornyezet Zsoltar (|| שַׁחַת, a halal/seol-parhuzam)',
                             l[max(0, i - 40):i + 60].replace('	', ' ')])
    with open('naplok/F34_M0_lista.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['forras_sor', 'strong', 'pozicio', 'hibas_alak', 'javitott_alak', 'osztaly', 'megjegyzes', 'kontextus']) + '\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    from collections import Counter
    print(Counter(r[5] for r in rows))
    for o in 'ABRK':
        pass
    print({o: len({r[1] for r in rows if r[5] == o}) for o in ('A', 'B', 'R', 'KIZART')})

main()
