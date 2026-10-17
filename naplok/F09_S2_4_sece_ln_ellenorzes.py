"""F09 S2.4: a SECE `LN:` mezo keresztellenorzese az UBS DNTG entry_kod-jai ellen (F05 S6, D7).

A SECE Louw-Nida kodjai csak keresztellenorzes: eltereskor JELENTES (a render nem hasznalja).
A 13 gorog token (a 8 motivum Strong-tokenjei). Kimenet: naplok/F09_S2_4_sece_ln_ellenorzes.tsv.
Proveniencia: scope=konkordancia/SECE_G_teljes.tsv + konkordancia/UBS_DNTG_jelentesek.tsv |
forras=naplok/F09_S2_4_sece_ln_ellenorzes.py (split('\\t'), csv nelkul) | ts=2026-10-17
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import general as G
import lexikon_general as LG

TOKENEK = []
_, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
M8 = ['ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001', 'ISTENTISZT-001', 'KIRALY-001', 'MENNY-001', 'TEREMT-001']
for r in elo:
    if r['id'] in M8:
        for t in LG.motivum_strong_tokenek([r]):
            if t.startswith('G') and t not in TOKENEK:
                TOKENEK.append(t)
TOKENEK.sort()

sece = {}
with open(os.path.join(ROOT, 'konkordancia', 'SECE_G_teljes.tsv'), encoding='utf-8') as f:
    for sor in f.read().split('\n'):
        m = sor.split('\t')
        if len(m) == 3 and m[0].startswith('G'):
            sece[m[0]] = m[2]

jelentesek, _darab = LG.ubs_dntg_adatok()
sorok = ['strong\tsece_ln\tubs_dntg_entry_kod\tegyezes\tmegjegyzes']
elter = 0
for t in TOKENEK:
    szoveg = sece.get(t, '')
    m = re.search(r'\sLN:\s(.*?)\sGK:', szoveg)
    sece_ln = sorted(set(x.strip() for x in m.group(1).split(',') if x.strip())) if m else []
    ubs = sorted(set(r['entry_kod'] for r in jelentesek.get(t, {}).values()))
    if sece_ln == ubs:
        egy, megj = 'egyezik', ''
    else:
        elter += 1
        egy = 'ELTER'
        megj = 'csak SECE: %s; csak UBS DNTG: %s' % (
            ','.join(sorted(set(sece_ln) - set(ubs))) or '-', ','.join(sorted(set(ubs) - set(sece_ln))) or '-')
    sorok.append('\t'.join([t, ','.join(sece_ln), ','.join(ubs), egy, megj]))
ut = os.path.join(ROOT, 'naplok', 'F09_S2_4_sece_ln_ellenorzes.tsv')
with open(ut, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(sorok) + '\n')
print('tokenek: %d, egyezik: %d, eltér (JELENTÉS): %d' % (len(TOKENEK), len(TOKENEK) - elter, elter))
for s in sorok[1:]:
    print(s)
