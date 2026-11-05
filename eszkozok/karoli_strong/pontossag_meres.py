#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a Károli–Strong párosítás pontosságának mérése a vak Opus-ellenőrzésből.

Bemenet: f172/minta.tsv (a rétegzett minta), f172/keret.tsv (rétegsúlyok),
f172/ellenor/celok.tsv, f172/ellenor/valasz/koteg_*.json (a vak ellenőr
jelölései), a régi arany (tokenek.regi_arany), f21p/regi_arany_hibas.tsv, és
csak olvasva az adat/karoli_strong/parok_*.tsv (a gépi pár teljes
partnerhalmaza a hiányzó-pár leíró számhoz és a gépi pár arany-egyezéséhez).

A pár HELYES, ha a gépi pár eredeti tokenje benne van az ellenőr által az adott
Károli-szóhoz jelölt halmazban. Hibatípus (csak a nem helyes párra, ebben a
sorrendben): `fölös pár` (az ellenőr szerint a Károli-szó betoldás) ·
`azonos lexéma, más előfordulás` (az ellenőr halmazában van ugyanilyen
Strong-számú más token) · `szomszédos token` (az ellenőr halmazának szomszédos
tokenje; csak helyzeti címke: többszavas egység vagy morféma-fürt hibás bontását
jelezheti, de valódi felcserélést is takarhat) · `rossz szó a versben`.
A `hiányzó pár` leíró szám: az ellenőr-jelölt token, amely a gépi partnerhalmazban
nincs (a lefedettség nem cél, F172 2.).

Kimenet:
  f172/itelet_par.tsv     — páronként az ellenőr halmaza, ítélet, hibatípus
  f172/meres_eredmeny.tsv — rétegenként n, helyes, pontosság, Wilson 95%;
                            súlyozott ÓSZ / ÚSZ / összes (rétegzett becslés,
                            normál közelítésű 95% CI); morféma/tartalmi bontás;
                            hibatípusok; kalibráció (az ellenőr és a gépi pár
                            egyezése a régi arannyal)

Használat: python eszkozok/karoli_strong/pontossag_meres.py [--reszleges]
(--reszleges: a még hiányzó kötegek céljait kihagyja, és jelzi)
"""

import argparse
import glob
import json
import math
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pontossag_minta as pm  # noqa: E402

GYOKER = pm.GYOKER
F172 = os.path.join(GYOKER, 'f172')
VALASZ = os.path.join(F172, 'ellenor', 'valasz')
Z95 = 1.959963984540054
HIBATIPUSOK = ['fölös pár', 'azonos lexéma, más előfordulás', 'szomszédos token', 'rossz szó a versben']
OSZ = [r for r in pm.RETEGEK if r.startswith('OSZ')]
USZ = [r for r in pm.RETEGEK if r.startswith('USZ')]


def wilson(x, n, z=Z95):
    if n == 0:
        return (float('nan'), float('nan'))
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def retegzett(adat, sulyok):
    """adat: {reteg: (x, n)}, sulyok: {reteg: N_h}. -> (p, also, felso, n).

    Rétegzett becslés a rétegek saját súlyával (N_h / ΣN_h), a varianciában
    véges sokasági korrekció nélkül (a minta a keret < 0,5%-a)."""
    ret = [r for r in adat if adat[r][1] > 0]
    N = sum(sulyok[r] for r in ret)
    if N == 0:
        return (float('nan'),) * 3 + (0,)
    p = sum(sulyok[r] / N * adat[r][0] / adat[r][1] for r in ret)
    var = sum((sulyok[r] / N) ** 2 * (adat[r][0] / adat[r][1]) * (1 - adat[r][0] / adat[r][1]) / adat[r][1]
              for r in ret)
    h = Z95 * math.sqrt(var)
    return (p, max(0.0, p - h), min(1.0, p + h), sum(adat[r][1] for r in ret))


def hibatipus(er, er_strong, opus, strong_of):
    """A nem helyes pár hibatípusa. opus: az ellenőr halmaza (eredeti sorszámok)."""
    if not opus:
        return HIBATIPUSOK[0]
    if any(strong_of(s) == er_strong for s in opus):
        return HIBATIPUSOK[1]
    if any(abs(s - er) == 1 for s in opus):
        return HIBATIPUSOK[2]
    return HIBATIPUSOK[3]


def valaszok():
    """{(vers, hu_sorszam): set(er)} + {koteg: modell}."""
    j, modell = {}, {}
    for ut in sorted(glob.glob(os.path.join(VALASZ, 'koteg_*.json'))):
        with open(ut, encoding='utf-8') as f:
            d = json.load(f)
        modell[d['koteg']] = d['modell']
        for x in d['versek']:
            for h, es in x['jeloles']:
                j[(x['vers'], h)] = set(es)
    return j, modell


def gepi_partnerek(versek):
    """{(vers, hu): set(er)} és {(vers, er): strong} a parok-táblákból, csak a kért versekre."""
    konyvek = set()
    for k in pm.konyvek():
        konyvek.add(k)
    part, strong = {}, {}
    for k in sorted(konyvek):
        _, sorok = pm._tabla(os.path.join(pm.ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            if r['vers'] not in versek:
                continue
            part.setdefault((r['vers'], int(r['hu_sorszam'])), set()).add(int(r['er_sorszam']))
            strong[(r['vers'], int(r['er_sorszam']))] = r['strong']
    return part, strong


def _strong_norm(s):
    s = s.strip()
    return s[0] + str(int(s[1:])) if len(s) > 1 and s[1:].isdigit() else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reszleges', action='store_true')
    a = ap.parse_args()

    import bemenet  # noqa: E402  (lassú betöltés: csak itt)
    import tokenek  # noqa: E402
    _, ered = bemenet._adatok()

    _, minta = pm._tabla(os.path.join(F172, 'minta.tsv'))
    _, keret = pm._tabla(os.path.join(F172, 'keret.tsv'))
    sulyok = {r['reteg']: int(r['parsor']) for r in keret if r['reteg'] in pm.RETEGEK}
    _, celok = pm._tabla(os.path.join(F172, 'ellenor', 'celok.tsv'))
    jel, modell = valaszok()
    for k, m in modell.items():
        ml = m.lower()
        if 'opus' not in ml or 'sonnet' in ml or 'gemini' in ml:
            raise SystemExit('a %s. köteg modellje nem Opus: %r' % (k, m))
    hianyzo_koteg = sorted({int(c['koteg']) for c in celok if c['koteg'] != '-'} - set(modell))
    if hianyzo_koteg and not a.reszleges:
        raise SystemExit('hiányzó kötegek: %s (--reszleges a részméréshez)' % hianyzo_koteg)

    versek = {r['vers'] for r in minta} | {c['vers'] for c in celok}
    gpart, _ = gepi_partnerek(versek)

    def strong_of(v):
        return lambda e: ered[v][e - 1]['strong']

    # --- páronkénti ítélet
    itelet = []
    for r in minta:
        kulcs = (r['vers'], int(r['hu_sorszam']))
        if kulcs not in jel:
            continue
        S = jel[kulcs]
        er = int(r['er_sorszam'])
        ok = er in S
        ht = '' if ok else hibatipus(er, r['strong'], S, strong_of(r['vers']))
        hiany = sorted(S - gpart.get(kulcs, set()))
        itelet.append(dict(r, opus=','.join(map(str, sorted(S))) or '-', helyes='1' if ok else '0',
                           hibatipus=ht, hianyzo=','.join(map(str, hiany))))

    head = pm.git_head()
    fej = ['minta_id', 'reteg', 'vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong',
           'morfema', 'nem_tr', 'opus', 'helyes', 'hibatipus', 'hianyzo']
    with open(os.path.join(F172, 'itelet_par.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 páronkénti ítélet (a gépi pár vs a vak Opus-ellenőr) | forras=f172/minta.tsv, '
                'f172/ellenor/valasz/koteg_*.json (%s) | ts=git:%s | manual (determinisztikus összevetés; az '
                'ellenőr modell-kimenet, nem arany)\n' % (', '.join(sorted(set(modell.values()))), head))
        f.write('\t'.join(fej) + '\n')
        for r in itelet:
            f.write('\t'.join(r[k] for k in fej) + '\n')

    # --- rétegenként
    sorok = []

    def sor(szakasz, cimke, x, n, p=None, lo=None, hi=None, megj=''):
        if p is None:
            p = x / n if n else float('nan')
            lo, hi = wilson(x, n)
        sorok.append([szakasz, cimke, str(n), str(x), '%.4f' % p, '%.4f' % lo, '%.4f' % hi, megj])

    adat = {}
    adat_t, adat_m = {}, {}
    for rt in pm.RETEGEK:
        rr = [r for r in itelet if r['reteg'] == rt]
        x, n = sum(r['helyes'] == '1' for r in rr), len(rr)
        adat[rt] = (x, n)
        sor('reteg', rt, x, n, megj='Wilson 95%')
        t = [r for r in rr if r['morfema'] == '0']
        m = [r for r in rr if r['morfema'] == '1']
        adat_t[rt] = (sum(r['helyes'] == '1' for r in t), len(t))
        adat_m[rt] = (sum(r['helyes'] == '1' for r in m), len(m))
    for cimke, ret in [('OSZ (súlyozott)', OSZ), ('USZ (súlyozott)', USZ), ('OSSZES (súlyozott)', pm.RETEGEK)]:
        p, lo, hi, n = retegzett({r: adat[r] for r in ret}, sulyok)
        x = sum(adat[r][0] for r in ret)
        sor('sulyozott', cimke, x, n, p, lo, hi, 'rétegzett becslés, normál 95%')
    for cimke, d in [('tartalmi szó', adat_t), ('morféma (H9001–H9049)', adat_m)]:
        for nev, ret in [('OSZ', OSZ), ('OSSZES', pm.RETEGEK)]:
            p, lo, hi, n = retegzett({r: d[r] for r in ret}, sulyok)
            if n:
                sor('bontas', '%s · %s' % (nev, cimke), sum(d[r][0] for r in ret), n, p, lo, hi,
                    'rétegzett (a réteg teljes súlyával), leíró')
    # hibatípusok
    for rt in pm.RETEGEK + ['OSSZES']:
        rr = [r for r in itelet if r['helyes'] == '0' and (rt == 'OSSZES' or r['reteg'] == rt)]
        for ht in HIBATIPUSOK:
            k = sum(r['hibatipus'] == ht for r in rr)
            sorok.append(['hibatipus', '%s · %s' % (rt, ht), str(len(rr)), str(k), '', '', '', 'a nem helyes párok közül'])
    for mf, cimke in [('0', 'tartalmi'), ('1', 'morféma')]:
        rr = [r for r in itelet if r['helyes'] == '0' and r['morfema'] == mf]
        for ht in HIBATIPUSOK:
            sorok.append(['hibatipus', 'OSSZES · %s · %s' % (cimke, ht), str(len(rr)),
                          str(sum(r['hibatipus'] == ht for r in rr)), '', '', '', 'a nem helyes párok közül'])
    hp = sum(1 for r in itelet if r['hianyzo'])
    sorok.append(['leiro', 'cél Károli-szó, amelyhez az ellenőr a gépinél több eredeti tokent jelölt', str(len(itelet)),
                  str(hp), '', '', '', 'hiányzó pár (lefedettség), nem a pontosság része'])

    # --- kalibráció a régi arannyal
    hibas = set()
    hut = os.path.join(GYOKER, 'f21p', 'regi_arany_hibas.tsv')
    _, hs = pm._tabla(hut)
    for r in hs:
        hibas.add((r['igehely'], r['karoli_szo'], r['strong']))
    karoli, _ = bemenet._adatok()
    kal = {'ellenor': [0, 0], 'gepi': [0, 0], 'ellenor_kiz': [0, 0], 'gepi_kiz': [0, 0]}
    kimaradt = 0
    for ig, szo, strong in tokenek.regi_arany():
        if ig not in karoli or ig not in ered:
            kimaradt += 1
            continue
        tl = [t.casefold() for t in tokenek.tokenizal(karoli[ig])]
        kif = [t.casefold() for t in tokenek.tokenizal(szo)]
        helyek = [i for i in range(len(tl) - len(kif) + 1) if kif and tl[i:i + len(kif)] == kif]
        if not helyek:
            kimaradt += 1
            continue
        osszetevok = {_strong_norm(s) for s in strong.split('+')}
        if any((ig, p + j + 1) not in jel for p in helyek for j in range(len(kif))):
            continue  # a köteg még nincs kész (--reszleges)

        def egyezik(halmaz_of):
            for p in helyek:
                u = set()
                for j in range(len(kif)):
                    u |= {_strong_norm(ered[ig][e - 1]['strong']) for e in halmaz_of((ig, p + j + 1))}
                if osszetevok <= u:
                    return True
            return False
        e1 = egyezik(lambda k: jel.get(k, set()))
        e2 = egyezik(lambda k: gpart.get(k, set()))
        for nev, e in [('ellenor', e1), ('gepi', e2)]:
            kal[nev][1] += 1
            kal[nev][0] += int(e)
            if (ig, szo, strong) not in hibas:
                kal[nev + '_kiz'][1] += 1
                kal[nev + '_kiz'][0] += int(e)
    sor('kalibracio', 'vak Opus-ellenőr = régi arany', *kal['ellenor'], megj='halmaz-definíció (F21), Wilson 95%')
    sor('kalibracio', 'gépi pár (#22) = régi arany', *kal['gepi'], megj='ugyanazokon a hármasokon')
    sor('kalibracio', 'vak Opus-ellenőr = régi arany (a hibás hármasok nélkül)', *kal['ellenor_kiz'],
        megj='tájékoztató: f21p/regi_arany_hibas.tsv kizárva')
    sor('kalibracio', 'gépi pár (#22) = régi arany (a hibás hármasok nélkül)', *kal['gepi_kiz'], megj='tájékoztató')
    sorok.append(['kalibracio', 'kimaradt arany-hármas (nincs vers / a kifejezés nincs a versben)', '', str(kimaradt),
                  '', '', '', ''])

    with open(os.path.join(F172, 'meres_eredmeny.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 pontosságmérés | forras=f172/itelet_par.tsv, f172/keret.tsv, '
                'konkordancia/Karoli_Strong_kivonat.tsv, adat/karoli_strong/parok_*.tsv @ git:%s | ts=git:%s | '
                'manual (determinisztikus; az ellenőr: %s; kötegek: %d%s)\n'
                % (head, head, ', '.join(sorted(set(modell.values()))), len(modell),
                   '; RÉSZLEGES, hiányzik: %s' % hianyzo_koteg if hianyzo_koteg else ''))
        f.write('\t'.join(['szakasz', 'cimke', 'n', 'x', 'p', 'also95', 'felso95', 'megjegyzes']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    for s in sorok:
        if s[0] in ('reteg', 'sulyozott', 'bontas', 'kalibracio'):
            print('%-11s %-62s n=%-5s x=%-5s p=%s [%s, %s]' % tuple(s[:7]))
    if hianyzo_koteg:
        print('RÉSZLEGES: hiányzó kötegek: %d' % len(hianyzo_koteg))


if __name__ == '__main__':
    main()
