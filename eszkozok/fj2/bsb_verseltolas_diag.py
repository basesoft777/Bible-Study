#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_verseltolas_diag.py -- F16: tajekoztato diagnozis a kuszob alatti OSZ-konyvekre.

A TAHOT heber (MT) verszamozast hasznal, a BSB angolt; a bsb_import.py igehely-szintu
egyezese ezert a szamozasi eltolas miatt is elbukhat. Ez a szkript fejezetenkent a
{-1, 0, +1, +2} eltolasok kozul a legjobbat valasztja (BSB v <-> TAHOT v+k), es igy
megmutatja, mennyi a kuszob alatti eredmenybol szamozas-artefaktum. NEM a kuszob alapja,
NEM modositja az import-dontest; a dontes a DONTESEK.md-tetelben a felhasznaloe.

Kimenet: naplok/F16_bsb_verseltolas_diagnozis.tsv (csak a NEM_ERI_EL OSZ-konyvek).
Hasznalat: python eszkozok/fj2/bsb_verseltolas_diag.py --munka <mappa>
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb_import as bi  # noqa: E402

ELTOLASOK = (-1, 0, 1, 2)


def fut(munka, parancs):
    mappa = os.path.join(munka, 'bsb-data-output', 'base', 'display')
    commit = kozos.commit_sha(os.path.join(munka, 'bsb-data-output'))
    tahot = bi.forras_halmazok('H')
    fej, lef = kozos.tsv_olvas(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'))
    ered_i = fej.index('eredmeny')
    alatta = {s[0] for s in lef if s[2] == 'heber' and s[ered_i] == 'NEM_ERI_EL'}
    sorok = []
    for step, mag, nyelv in bi.konyvek()[:39]:
        if mag not in alatta:
            continue
        kod = step.upper()
        bmappa = os.path.join(mappa, kod)
        fejezetek = sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                           for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)
        nevezo = egyezo_alap = egyezo_eltolt = 0
        eltolt_fejezetek = []
        for fej_szam in fejezetek:
            with open(os.path.join(bmappa, '%s%d.json' % (kod, fej_szam)), encoding='utf-8') as f:
                b = bi.vers_strongok(json.load(f), 'H')
            legjobb = None
            for k in ELTOLASOK:
                db = n = 0
                for vs in b:
                    t = tahot.get('%s %d:%d' % (mag, fej_szam, vs + k))
                    if t is None:
                        continue
                    n += 1
                    if t <= b[vs]:
                        db += 1
                if legjobb is None or db > legjobb[1]:
                    legjobb = (k, db, n)
            db0 = n0 = 0
            for vs in b:
                t = tahot.get('%s %d:%d' % (mag, fej_szam, vs))
                if t is None:
                    continue
                n0 += 1
                if t <= b[vs]:
                    db0 += 1
            nevezo += n0
            egyezo_alap += db0
            # az eltolt valtozat nevezoje a nulla-eltolasu nevezo (a tobbi vers tovabbra sem egyezik)
            egyezo_eltolt += max(legjobb[1], db0)
            if legjobb[0] != 0 and legjobb[1] > db0:
                eltolt_fejezetek.append('%d(%+d)' % (fej_szam, legjobb[0]))
        sorok.append((mag, str(nevezo), str(egyezo_alap), '%.2f' % (100.0 * egyezo_alap / nevezo),
                      str(egyezo_eltolt), '%.2f' % (100.0 * egyezo_eltolt / nevezo),
                      ' '.join(eltolt_fejezetek) if eltolt_fejezetek else '-'))
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_verseltolas_diagnozis.tsv'),
                 kozos.fejlec(bi.URL + ' + konkordancia/TAHOT_kivonat.tsv', 'BSB commit ' + commit, parancs)
                 + ['tajekoztato diagnozis, NEM a kuszob alapja; fejezetenkent a legjobb BSB v <-> TAHOT v+k eltolas (k in -1,0,1,2); nevezo = a nulla-eltolasu nevezo',
                    'eltolt_fejezetek: fejezet(eltolas) csak ott, ahol az eltolas javit'],
                 ['konyv', 'nevezo', 'egyezo_eltolas_nelkul', 'szazalek_eltolas_nelkul', 'egyezo_legjobb_eltolassal',
                  'szazalek_legjobb_eltolassal', 'eltolt_fejezetek'], sorok)
    for s in sorok:
        print('\t'.join(s))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--munka', required=True)
    a = ap.parse_args()
    fut(a.munka, 'python eszkozok/fj2/bsb_verseltolas_diag.py --munka <mappa>')


if __name__ == '__main__':
    main()
