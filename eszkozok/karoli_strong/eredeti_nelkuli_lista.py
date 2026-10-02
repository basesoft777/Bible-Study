#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a Károli-kulcs szerint: melyik Károli-versnek nincs eredeti (TAHOT/TAGNT) verse, és fordítva.

Kimenet: naplok/F22_nincs_parja_versek.tsv — soronként egy vers (`irany`: karoli_eredeti_nelkul |
eredeti_karoli_nelkul), a könyvenkénti darabszámokkal a végén (# összesítő sorok), API nélkül,
determinisztikusan. A Károli-oldali lista az, amelyet a modellminta (`sonnet_koteg.minta_epit`)
eleve kihagy, és az egyesítő `kezi` állapotban visz tovább; az eredeti-oldali verseket az egyesítő
szintén `kezi` állapotban viszi (a Károli-oldalon nincs token, az eredeti tokenek `fuggoben`).

Használat:
    python eszkozok/karoli_strong/eredeti_nelkuli_lista.py [--kimenet naplok/F22_nincs_parja_versek.tsv]
"""
import argparse
import os
import sys

import tokenek
import sonnet_koteg

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

IRANYOK = ('karoli_eredeti_nelkul', 'eredeti_karoli_nelkul')


def lista(karoli=None, ered=None):
    """[(irany, konyv, igehely, token_db)] a Károli-sorrendben, majd az eredeti-oldal a TAHOT/TAGNT sorrendjében."""
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti(versmegf=False)   # a nyers Károli-kulcs
    ki = []
    for ig, szoveg in karoli.items():
        if not ered.get(ig):
            b = tokenek.igehely_bont(ig)
            ki.append((IRANYOK[0], b[0] if b else '?', ig, len(tokenek.tokenizal(szoveg))))
    for ig, szavak in ered.items():
        if ig not in karoli:
            b = tokenek.igehely_bont(ig)
            ki.append((IRANYOK[1], b[0] if b else '?', ig, len(szavak)))
    return ki


def szoveg(sorok):
    be = ['# GENERÁLT: eszkozok/karoli_strong/eredeti_nelkuli_lista.py | scope=Károli_1908.tsv+TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (Károli-kulcs) | forras=determinisztikus kulcs-összevetés | ts=%s' % tokenek.generalas_ts(),
          'irany\tkonyv\tigehely\ttoken_db']
    be += ['\t'.join(str(x) for x in s) for s in sorok]
    be.append('# ÖSSZESÍTŐ könyvenként (irany, konyv: vers_db, token_db)')
    ossz = {}
    for irany, k, ig, n in sorok:
        a = ossz.setdefault((irany, k), [0, 0])
        a[0] += 1
        a[1] += n
    for (irany, k), (v, n) in sorted(ossz.items(), key=lambda x: (IRANYOK.index(x[0][0]), x[0][1])):
        be.append('# %s\t%s\t%d vers\t%d token' % (irany, k, v, n))
    for irany in IRANYOK:
        v = sum(a[0] for (i, _), a in ossz.items() if i == irany)
        n = sum(a[1] for (i, _), a in ossz.items() if i == irany)
        be.append('# ÖSSZESEN\t%s\t%d vers\t%d token' % (irany, v, n))
    return '\n'.join(be) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kimenet', default=os.path.join('naplok', 'F22_nincs_parja_versek.tsv'))
    a = ap.parse_args(argv)
    sorok = lista()
    os.makedirs(os.path.dirname(a.kimenet) or '.', exist_ok=True)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg(sorok))
    print('írva: %s (%d sor)' % (a.kimenet, len(sorok)))
    for irany in IRANYOK:
        print('%s: %d vers' % (irany, sum(1 for s in sorok if s[0] == irany)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
