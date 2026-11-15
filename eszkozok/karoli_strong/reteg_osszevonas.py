#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175 — a #172 két Mózes-rétegének összevonása egy rétegbe (Mózes öt könyve), ugyanabból a mérésből.

A #172 mintavétele a Mózes öt könyvét két rétegben húzta (`OSZ_mozes_magas`: az 1–2Móz két modell egyezésével
párosított párjai; `OSZ_mozes`: a Mózes-könyvek minden más párja), rétegenként 200 párral. A nyilvános közlés a
rétegeket könyvcsoportként nevezi (a felhasználó döntése, 2026-11-14: a két modell egyezése nem minősítés), ezért a
két réteg egy rétegként jelenik meg. Új mérés nincs: a két réteg mért aránya a pársúlyával (`f172/keret.tsv`
`parsor`) súlyozva összegződik, a varianciában ugyanazzal a rétegzett képlettel, mint a #172 súlyozott sorai
(`pontossag_meres.retegzett`: normál közelítésű 95%, véges sokasági korrekció nélkül). A hibatípus-sorok darabszámai
összeadódnak.

Bemenet: f172/meres_eredmeny.tsv, f172/keret.tsv
Kimenet: f172/reteg_osszevont.tsv (proveniencia-sorral; a `karoli_strong_export.py` olvassa)

Használat: python eszkozok/karoli_strong/reteg_osszevonas.py [--ellenoriz]
(--ellenoriz: nem ír, csak összeveti a lemezen állóval; eltérésnél 1-es kóddal lép ki)
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pontossag_meres as pm  # noqa: E402  (a #172 rétegzett becslése)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = pm.GYOKER
MERES = 'f172/meres_eredmeny.tsv'
KERET = 'f172/keret.tsv'
KIMENET = 'f172/reteg_osszevont.tsv'
FORRAS_RETEGEK = ('OSZ_mozes_magas', 'OSZ_mozes')
UJ_CIMKE = 'OSZ_mozes_osszevont'
FEJ = ['szakasz', 'cimke', 'n', 'x', 'p', 'also95', 'felso95', 'megjegyzes']


def tabla(rel):
    """TSV-olvasás `split('\\t')`-tel; a `#` sorok megjegyzések."""
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def git_hash(*rel):
    r = subprocess.run(['git', 'log', '-1', '--format=%h', '--'] + list(rel), cwd=GYOKER, capture_output=True,
                       text=True, encoding='utf-8')
    h = r.stdout.strip()
    if not h:
        raise SystemExit('összevonás: a bemenet nincs a git-történetben: %s' % (rel,))
    return h


def osszevon():
    meres = tabla(MERES)
    keret = {s['reteg']: int(s['parsor']) for s in tabla(KERET)}
    adat = {}
    for s in meres:
        if s['szakasz'] == 'reteg' and s['cimke'] in FORRAS_RETEGEK:
            adat[s['cimke']] = (int(s['x']), int(s['n']))
    if set(adat) != set(FORRAS_RETEGEK):
        raise SystemExit('összevonás: hiányzó Mózes-réteg a mérőtáblában: %s' % sorted(set(FORRAS_RETEGEK) - set(adat)))
    p, lo, hi, n = pm.retegzett(adat, keret)
    x = sum(v[0] for v in adat.values())
    sulyok = ' + '.join('%s %d' % (r, keret[r]) for r in FORRAS_RETEGEK)
    ki = [['reteg', UJ_CIMKE, str(n), str(x), '%.4f' % p, '%.4f' % lo, '%.4f' % hi,
           'rétegzett becslés a két Mózes-réteg pársúlyával (%s), normál 95%%' % sulyok]]
    for ht in pm.HIBATIPUSOK:
        nn = kk = 0
        for r in FORRAS_RETEGEK:
            s = [m for m in meres if m['szakasz'] == 'hibatipus' and m['cimke'] == '%s · %s' % (r, ht)]
            if len(s) != 1:
                raise SystemExit('összevonás: hiányzó hibatípus-sor: %s · %s' % (r, ht))
            nn += int(s[0]['n'])
            kk += int(s[0]['x'])
        ki.append(['hibatipus', '%s · %s' % (UJ_CIMKE, ht), str(nn), str(kk), '', '', '',
                   'a nem helyes párok közül (a két Mózes-réteg összege)'])
    return ki


def szoveg(sorok):
    h = git_hash(MERES, KERET)
    prov = ('# MANUAL: scope=F175 rétegösszevonás (a #172 két Mózes-rétege egy rétegben; új mérés nincs) | forras=%s, '
            '%s @ git:%s | ts=git:%s | manual (determinisztikus; előállítás: '
            'eszkozok/karoli_strong/reteg_osszevonas.py)' % (MERES, KERET, h, h))
    return '\n'.join([prov, '\t'.join(FEJ)] + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    uj = szoveg(osszevon())
    ut = os.path.join(GYOKER, KIMENET)
    if a.ellenoriz:
        with open(ut, encoding='utf-8') as f:
            regi = f.read()
        if regi != uj:
            print('ELTÉR: %s nem a mérőtáblákból számolt' % KIMENET)
            return 1
        print('OK: %s a mérőtáblákból számolt' % KIMENET)
        return 0
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(uj)
    print(uj)
    return 0


if __name__ == '__main__':
    sys.exit(main())
