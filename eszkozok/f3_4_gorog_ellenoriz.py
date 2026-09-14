# -*- coding: utf-8 -*-
import sys, io, os, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEL = {'1Thessz 5:23', 'Zsid 4:12', '1Kor 15:45', 'Luk 1:46', 'Luk 1:47',
       '1Kor 2:14', '1Kor 2:15', 'Zsid 7:3', 'Zsid 7:17', '2Pét 2:4', '2Pét 2:5'}
with open(os.path.join(ROOT, 'konkordancia', 'TAGNT_kivonat.tsv'), encoding='utf-8') as f:
    r = csv.DictReader(f, delimiter='\t')
    for s in r:
        if s['Igehely'] in CEL:
            print('%-14s %-7s %-22s %-16s %s' % (s['Igehely'], s['Strong-szám'],
                  s['Ragozott alak'], s['Rövid jelentés'], s['Angol tükörfordítás']))
