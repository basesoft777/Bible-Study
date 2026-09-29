#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
futtat.py -- F06_FORRASFELMERES_BRIEF.md: a mero-szkriptek kozos indito.

    python eszkozok/fj2/futtat.py --lepes meres            # nave, kjv_asv, bsb, macula
    python eszkozok/fj2/futtat.py --lepes licenc           # MiniMax-elemzes (OPENROUTER_API_KEY kell)
    python eszkozok/fj2/futtat.py --lepes nave|kjv_asv|bsb|macula
    python eszkozok/fj2/futtat.py --szaraz                 # letoltes es API-hivas nelkul, csak a szerkezet

Kapu (nem --szaraz futasnal): a mereshez a brief 2. lepesenek valasza kell -- az
eszkozok/fj2/kuszob.txt (BSB-kuszob) es a naplok/F06_felmeres.md-ben a '## ⛔ Valasz'
szakasz. Ezek nelkul a szkript nem indul.
"""

import argparse
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402


def kapu_ellenoriz():
    hiany = []
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kuszob.txt')):
        hiany.append('eszkozok/fj2/kuszob.txt')
    felmeres = os.path.join(kozos.NAPLOK, 'F06_felmeres.md')
    if not os.path.exists(felmeres) or not re.search(r'^## ⛔ Válasz', open(felmeres, encoding='utf-8').read(), re.M):
        hiany.append("naplok/F06_felmeres.md '## ⛔ Válasz' szakasz")
    if hiany:
        raise SystemExit('HIBA: a brief 2. lepesenek (⛔) valasza hianyzik: ' + ', '.join(hiany))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lepes', default='meres', choices=['meres', 'licenc', 'nave', 'kjv_asv', 'bsb', 'macula'])
    ap.add_argument('--szaraz', action='store_true')
    ap.add_argument('--munka', default=None, help='munkakonyvtar a nyers klonoknak (nem commitba)')
    a = ap.parse_args()
    kozos.SZARAZ = a.szaraz
    parancs = 'python eszkozok/fj2/futtat.py --lepes %s' % a.lepes
    if not a.szaraz:
        kapu_ellenoriz()
    munka = a.munka or tempfile.mkdtemp(prefix='f06_')
    import nave, kjv_asv, bsb, macula, licenc
    if a.lepes in ('meres', 'nave'):
        nave.fut(munka, parancs)
    if a.lepes in ('meres', 'kjv_asv'):
        kjv_asv.fut(munka, parancs)
    if a.lepes in ('meres', 'bsb'):
        bsb.fut(munka, parancs)
    if a.lepes in ('meres', 'macula'):
        macula.fut(munka, parancs)
    if a.lepes != 'licenc':
        kozos.licenc_index_ir(parancs)
    if a.lepes == 'licenc':
        licenc.fut(parancs)
    if a.munka is None:
        shutil.rmtree(munka, ignore_errors=True)


if __name__ == '__main__':
    main()
