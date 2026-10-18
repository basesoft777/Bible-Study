"""F117.3: a DT-F117b osztály-szabálya (KJV, ha a KJV-szám = Károli-szám; különben KEZI) és a mai tábla konvenciója
(kitöltött `igehely_mt` csak MT osztályú sorban; KJV/KEZI sorban üres) közötti ütközés számlálása a 346 javított soron.
Bemenet: naplok/F117_mt_levezetes.tsv; a mai konvenció mérése: konkordancia/Karoli_versmegfeleltetes.tsv (csak olvas)."""
import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n')
            if s and not s.startswith('#'):
                yield s.split('\t')


konv = Counter()
for p in sorok(os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')):
    if p[0] == 'igehely_karoli':
        continue
    konv[(p[3], 'mt_kitoltve' if p[2] else 'mt_ures', 'mt=karoli' if p[2] and p[2] == p[0].rsplit(' ', 1)[1] else '-')] += 1
print('mai tábla (osztály, mt, mt=Károli-szám):', dict(konv))

kat = Counter()
pelda = {}
for p in sorok(os.path.join(ROOT, 'naplok', 'F117_mt_levezetes.tsv')):
    if p[0] == 'igehely_karoli':
        continue
    kar = p[0].rsplit(' ', 1)[1]
    kjv, mt = p[2], p[3]
    osz_b = 'KJV' if kjv == kar else 'KEZI'
    if mt == kar and kjv == kar:
        k = 'K=KJV=MT (KJV, mt üresen hagyható: ütközés nincs)'
    elif mt == kar and kjv != kar:
        k = 'K=MT≠KJV (a konvenció szerint MT osztály; DT-F117b: KEZI)'
    elif mt != kar and kjv == kar:
        k = 'K=KJV≠MT (DT-F117b: KJV; kitöltött mt-vel: nincs ilyen sor a mai táblában)'
    else:
        k = 'K≠KJV, K≠MT (DT-F117b: KEZI; kitöltött mt-vel: nincs ilyen sor a mai táblában)'
    kat[k] += 1
    pelda.setdefault(k, []).append('%s→KJV %s/MT %s' % (p[0], kjv, mt))
for k, n in kat.items():
    print('%3d  %s' % (n, k))
    print('      pl.: %s%s' % (', '.join(pelda[k][:6]), ' …' if len(pelda[k]) > 6 else ''))

# tételes lista: naplok/F117_osztaly_utkozes.tsv (soronként a kategória; a 174-es csoportban az MT = KJV-e)
ki = ['# F117.3: osztály-ütközés (DT-F117b ↔ a mai tábla konvenciója) a 346 javított soron',
      '# proveniencia: scope=A–D′ (346) | forras=naplok/F117_mt_levezetes.tsv + konkordancia/Karoli_versmegfeleltetes.tsv (konvenció) | eszkoz=naplok/F117_osztaly_utkozes.py | n=346 | ts=2026-10-18',
      'igehely_karoli\tkjv\tmt\tosztaly_dt_f117b\tosztaly_konvencio\tkategoria\tmt_eq_kjv']
mt_eq = Counter()
for p in sorok(os.path.join(ROOT, 'naplok', 'F117_mt_levezetes.tsv')):
    if p[0] == 'igehely_karoli':
        continue
    kar = p[0].rsplit(' ', 1)[1]
    kjv, mt = p[2], p[3]
    ob = 'KJV' if kjv == kar else 'KEZI'
    if mt == kar and kjv == kar:
        k, ok_ = 'K=KJV=MT', 'KJV (mt üres)'
    elif mt == kar:
        k, ok_ = 'K=MT≠KJV', 'MT (mt = Károli-szám)'
    elif kjv == kar:
        k, ok_ = 'K=KJV≠MT', 'nincs mintája'
    else:
        k, ok_ = 'K≠KJV,K≠MT', 'nincs mintája (KEZI: mt üres)'
    e = 'igen' if mt == kjv else 'nem'
    if k == 'K≠KJV,K≠MT':
        mt_eq[e] += 1
    ki.append('\t'.join([p[0], kjv, mt, ob, ok_, k, e]))
with open(os.path.join(ROOT, 'naplok', 'F117_osztaly_utkozes.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(ki) + '\n')
print('a K≠KJV,K≠MT csoportban MT = KJV:', dict(mt_eq))
