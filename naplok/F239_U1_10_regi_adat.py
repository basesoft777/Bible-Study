# -*- coding: utf-8 -*-
"""F239 U1 10. pont: a régi adat alakja az új generátorhoz (csak lista). Kimenet: naplok/F239_U1_TEREMT-001_regi_adat.tsv. TSV: split/join, csv nélkül."""
import sys, os, re
from collections import Counter, OrderedDict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MID = 'TEREMT-001'
def tsv(p):
    return [l.rstrip('\n').split('\t') for l in open(os.path.join(GY, p), encoding='utf-8') if l.strip() and not l.startswith('#')]
out = []
# a) jeloltek.tsv forras_kereses alakjai (az F239 U1 által ma felvett nyitva sorok nélkül)
c = OrderedDict()
for r in tsv('adat/jeloltek.tsv')[1:]:
    if r[0] == MID and not r[2].startswith('F239 U1 teljesség-mérés'):
        alak = r[2].split(' | ')[0]
        alak = re.sub(r'§.*', '§…', alak)
        k = (alak, r[3])
        c.setdefault(k, []).append(r[1])
for (alak, d), vs in c.items():
    out.append(['jeloltek_forras_kereses', alak, d, str(len(vs)), ', '.join(vs[:4]) + (' …' if len(vs) > 4 else ''),
                ('EZ A RÉGI `scan H…` ALAK (a TEREMT-002-n B04-et adott): az U3 technikai része javítsa; a lapgen nem futott, a hatás nem mért'
                 if alak.startswith('scan H') else 'nem `scan H…` alak (visszakeresés-felirat / napló-hivatkozás); a lapgen nem futott, a hatás nem mért')])
# b) res_forras.tsv sorai, amelyek nem a kézi forrásra mutatnak
for r in tsv('adat/res_forras.tsv')[1:]:
    if r[0] == MID:
        kezi = r[4] == 'motivumok/%s.md' % MID
        out.append(['res_forras', r[1], r[3], '1', r[4][:140], 'kézi forrásra mutat' if kezi else 'NEM a kézi forrásra mutat (motivumok/TEREMT-001.md)'])
# c) N58
t = open(os.path.join(GY, 'tematikus_lezart', 'Tehom_tematikus.md'), encoding='utf-8').read()
out.append(['N58', 'tematikus_lezart/Tehom_tematikus.md 51. sor', '', '1', '„35-ször” áll' if '**35-ször**' in t else 'más szám', 'a ma mért scan: 36 szó-előfordulás, 35 igehely; nyitva (a régi réteg, K1)'])
out.append(['N58', 'tematikus_lezart/Tehom_tematikus.md 84. sor', '', '1', '„egyedi versek száma emiatt 34” áll' if 'egyedi versek száma emiatt 34' in t else 'más szám', 'ugyanez'])
out.append(['N58', 'Jób 41:32 említése a régi tanulmányban', '', '1', 'van' if '41:32' in t else 'nincs', 'az adatban E-sor + beépített jelölt van (lekerdez scan H8415: igen)'])
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_regi_adat.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("# GENERÁLT: naplok/F239_U1_10_regi_adat.py | scope=adat/jeloltek.tsv + adat/res_forras.tsv TEREMT-001 sorai + tematikus_lezart/Tehom_tematikus.md | forras=split('\t') | ts=2026-11-23 | csak lista\n")
    f.write('mit\ttartalom\tdontes_vagy_forras\tdb\tpelda\tmegjegyzes\n')
    for o in out:
        f.write('\t'.join(x.replace('\t', ' ') for x in o) + '\n')
for o in out:
    print('\t'.join(o)[:260])
