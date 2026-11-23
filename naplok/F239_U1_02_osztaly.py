# -*- coding: utf-8 -*-
"""F239 U1 2. pont: a teljesség-mérés Károli-háló eltéréseinek gépi osztályozása (döntés nélkül) a vers TAHOT/TAGNT-tokenjei alapján.
Bemenet: naplok/F239_U1_TEREMT-001_teljesseg.tsv (eszkozok/teljesseg_meres.py). Kimenet: naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv;
a --jelolt kapcsolóval a nyitva jelölt-blokksorok (naplok/F239_U1_TEREMT-001_jelolt_sorok.tsv). TSV: split/join, csv nélkül."""
import sys, os, re
from collections import OrderedDict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
MID = 'TEREMT-001'
TS = '2026-11-23'
GLOSSZA = re.compile(r'deep|depth|abyss|bottom|whirl|vortex|swirl|bottomless|\bpit\b|sink|sunk|dive', re.I)
CSOPORT = [('mélység', re.compile(r'^mélység', re.I)), ('mély', re.compile(r'^mély(?!ség)', re.I)),
           ('örvény', re.compile(r'^örvény', re.I)), ('fenékig', re.compile(r'^fenékig', re.I))]
tok = {}
for r in L.load_tahot() + L.load_tagnt():
    tok.setdefault(r['Igehely'], []).append(r)
div = []
for s in open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_teljesseg.tsv'), encoding='utf-8'):
    if s.startswith('#'):
        continue
    c = s.rstrip('\n').split('\t')
    if c[0] == 'halo':
        continue
    if c[2] == 'ELTÉRÉS':
        div.append(c)
blokk = OrderedDict()
szo_csop = {}
for halo, ig, allapot, gerinc, reszlet, prov in div:
    if halo == 'karoli':
        szavak = [x.strip() for x in re.split(r'[;,]', reszlet.split(' [')[0])]
        csopok = []
        for sz in szavak:
            for nev, rx in CSOPORT:
                if rx.search(sz) and nev not in csopok:
                    csopok.append(nev)
        if not csopok:
            csopok = ['egyéb']
        talalt = sorted({t['Strong-szám'] for t in tok.get(ig, []) if GLOSSZA.search(t.get('Rövid jelentés', '') + ' ' + t.get('Angol tükörfordítás', ''))})
        for st in talalt:
            blokk.setdefault((halo, st), []).append((ig, gerinc))
        if not talalt:
            for cs in csopok:
                blokk.setdefault((halo, 'osztálytalan:' + cs), []).append((ig, gerinc))
        szo_csop.setdefault(ig, set()).update(csopok)
    else:
        blokk.setdefault((halo, 'szotar'), []).append((ig, gerinc))
for k in blokk:
    seen, out = set(), []
    for v, g in blokk[k]:
        if v not in seen:
            seen.add(v); out.append((v, g))
    blokk[k] = out
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_teljesseg_blokkok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("# GENERÁLT: naplok/F239_U1_02_osztaly.py | scope=naplok/F239_U1_TEREMT-001_teljesseg.tsv ELTÉRÉS-sorai × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (glossza) | forras=split('\t') | ts=%s\n" % TS)
    f.write('halo\tblokk\tigehely\tgerinc_a_versben\n')
    for (h, k), vs in blokk.items():
        for v, g in vs:
            f.write('%s\t%s\t%s\t%s\n' % (h, k, v, g))
print('eltérés-sor:', len(div))
for (h, k), vs in blokk.items():
    print(h, k, len(vs), ', '.join(v for v, _ in vs[:6]))
