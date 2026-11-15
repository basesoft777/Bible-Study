# -*- coding: utf-8 -*-
"""F224.13, C-futás: az F2 ítéletei K-tételenként, Sonnet 1. kör, 2. kör és Opus.

Használat: python naplok/F224_proba/opus_osszevet.py [opus-mappa]
A kimenet: a halmaz-tételek ítéletei körönként, a nem „igazolt” ítéletek
körönkénti halmaza és az eltérések (ingadozás).
"""
import sys, re, pathlib
sys.stdout.reconfigure(encoding='utf-8')

ITT = pathlib.Path(__file__).parent
OPUS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ITT

ITELETEK = ('igazolt', 'hamis', 'vitatott', 'nem eldönthető')

def itelet_tabla(ut):
    """K -> ítélet a fájl táblázatsoraiból (az ítélet-oszlop a fejléc szerint)."""
    ki, it_idx = {}, None
    for sor in ut.read_text(encoding='utf-8').split('\n'):
        if not sor.startswith('|'):
            continue
        cel = [c.strip() for c in sor.strip().strip('|').split('|')]
        if cel and cel[0] == 'K' and 'Ítélet' in cel:
            it_idx = cel.index('Ítélet')
            continue
        m = re.match(r'\**(K\d+)(?!\d)', cel[0] or '')
        if it_idx is None or not m:
            continue
        cel[0] = m.group(1)
        if len(cel) <= it_idx:
            continue
        it = cel[it_idx].lower().replace('*', '').strip()
        for t in ITELETEK:
            if it.startswith(t):
                ki[cel[0]] = t
                break
        else:
            ki[cel[0]] = '?' + it
    return ki

def betolt(nevek):
    d = {}
    for n in nevek:
        d.update(itelet_tabla(n))
    return d

KOROK = {
    'S1': (betolt([ITT / 'F2_HAMART_1.md', ITT / 'F2_HAMART_2.md']), betolt([ITT / 'F2_ISTENTISZT.md'])),
    'S2': (betolt([ITT / 'F2_HAMART_1_2kor.md', ITT / 'F2_HAMART_2_2kor.md']), betolt([ITT / 'F2_ISTENTISZT_2kor.md'])),
}
op = [OPUS / 'F2_HAMART_1_opus.md', OPUS / 'F2_HAMART_2_opus.md', OPUS / 'F2_ISTENTISZT_opus.md']
if all(p.exists() for p in op):
    KOROK['O'] = (betolt(op[:2]), betolt(op[2:]))

# A pontozási kulcs (naplok/F224_proba.md 2.1, 2.2): lektor-tétel -> K-tételek
HAM = {8: ['K5'], 9: ['K104'], 10: ['K104', 'K106'], 11: ['K106'], 12: ['K105'], 13: ['K98'],
       14: ['K98', 'K102'], 21: ['K14'], 22: ['K28'], 28: ['K31'], 29: ['K33', 'K45'], 31: ['K39'],
       33: ['K41'], 34: ['K44'], 35: ['K47'], 36: ['K50'], 38: ['K55'], 42: ['K71']}
IST = {1: ['K50'], 5: ['K27'], 8: ['K52'], 10: ['K25'], 12: ['K13', 'K15'], 13: ['K22'],
       15: ['K4'], 16: ['K5'], 17: ['K7']}

for nev, kulcs, idx in (('HAMART', HAM, 0), ('ISTENTISZT', IST, 1)):
    print(f'== {nev}')
    for t, ks in kulcs.items():
        sor = [f'{t:>2}']
        for kor, (h, i) in KOROK.items():
            d = (h, i)[idx]
            sor.append(f'{kor}: ' + ', '.join(f'{k}={d.get(k, "—")}' for k in ks))
        print(' | '.join(sor))

for kor, (h, i) in KOROK.items():
    for nev, d, n in (('HAM', h, 118), ('IST', i, 58)):
        szam = {t: sum(1 for v in d.values() if v == t) for t in ITELETEK}
        egyeb = [k for k, v in d.items() if v not in ITELETEK]
        print(f'{kor} {nev}: {len(d)}/{n} tétel', szam, 'egyéb:', egyeb)

if 'O' in KOROK:
    for nev, idx in (('HAM', 0), ('IST', 1)):
        s2, o = KOROK['S2'][idx], KOROK['O'][idx]
        s1 = KOROK['S1'][idx]
        nem = lambda d: {k for k, v in d.items() if v != 'igazolt'}
        print(f'-- {nev}: nem igazolt S1 {len(nem(s1))}, S2 {len(nem(s2))}, O {len(nem(o))}')
        print('   O-ban nem igazolt, S1-ben és S2-ben igazolt:', sorted(nem(o) - nem(s1) - nem(s2), key=lambda x: int(x[1:])))
        print('   S2-ben nem igazolt, O-ban igazolt:', sorted(nem(s2) - nem(o), key=lambda x: int(x[1:])))
        elt = sorted((k for k in set(s2) | set(o) if s2.get(k) != o.get(k)), key=lambda x: int(x[1:]))
        print('   S2 ≠ O (ítélet):', len(elt))
