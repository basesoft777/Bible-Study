#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KH_ELREJTES_igazolas.py -- az olvasói kapu (N-F156a) igazoló listája: a 9 lexikonlap 4. szakaszából eltűnő
Károli-KH sorok egyenként, a forrásverssel, a másolt lista vélt eredeti gazdájával (az azonos listájú, támogatott
verssel) és a három vers Károli-szövegével, hogy a kézi ítélet (másolat-e) a szöveg alapján ellenőrizhető legyen.
Csak olvas. Kimenet: Markdown a stdout-ra.

Használat: python naplok/KH_ELREJTES_igazolas.py > <fájl>
"""
import os
import re
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import karoli_kh_epseg as KH  # noqa: E402
import olvasoi_kapu as K  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def karoli():
    ki = {}
    with open(os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
        next(f)
        for s in f:
            m = s.rstrip('\n').split('\t')
            if len(m) >= 2:
                ki[m[0]] = m[1]
    return ki


def main():
    kh, tsk = KH.betolt()
    gyanus = KH.gyanus_forrasok(kh, tsk)
    _, step, _ = K.konyvek()
    hu = {v: k for k, v in step.items()}
    szoveg = karoli()

    def hu_ref(s):
        r = KH.step_ref(s.split('-')[0])
        return '%s %d:%d' % (hu.get(r[0], r[0]), r[1], r[2]) if r else s

    def rovid(ref, n=110):
        t = szoveg.get(ref, '—')
        return (t[:n] + '…') if len(t) > n else t

    print('| Lap | Forrásvers | Eltűnő KH-sorok | A lista vélt gazdája (azonos lista, támogatott) | Forrásvers (Károli) | '
          'Első cél (Károli) | A gazda (Károli) |')
    print('|---|---|---|---|---|---|---|')
    db = 0
    for nev in sorted(os.listdir(os.path.join(GYOKER, 'lexikon'))):
        if not nev.endswith('_TUDOMANYOS.md'):
            continue
        with open(os.path.join(GYOKER, 'lexikon', nev), encoding='utf-8') as f:
            sorok = K.tagol(f.read())
        latott = set()
        for s in sorok:
            if not s.szakasz.startswith('4. Kereszthivatkoz') or not s.szoveg.strip().startswith('- Károli-KH'):
                continue
            m = re.match(r'(\S+)\s+(\d+):(\d+)$', s.alszakasz.strip())
            if not m or m.group(1) not in step:
                continue
            forras = '%s.%s.%s' % (step[m.group(1)], m.group(2), m.group(3))
            if forras not in gyanus or forras in latott:
                continue
            latott.add(forras)
            n = sum(1 for x in sorok if x.alszakasz == s.alszakasz and x.szoveg.strip().startswith('- Károli-KH'))
            db += n
            gazda = gyanus[forras][0]
            print('| %s | %s | %d: %s | %s | %s | %s | %s |' % (
                nev[:-len('_TUDOMANYOS.md')], s.alszakasz, n, ', '.join(hu_ref(c) for c in kh[forras]),
                ', '.join(hu_ref(g) for g in gyanus[forras]), rovid(s.alszakasz), rovid(hu_ref(kh[forras][0])),
                rovid(hu_ref(gazda))))
    print('\n*Összesen %d eltűnő Károli-KH sor.*' % db)


if __name__ == '__main__':
    main()
