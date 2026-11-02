#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KH_ELREJTES_hatas.py -- mérés (olvasói kapu, N-F156a): ha a generátor a másolat-gyanús Károli-KH listákat nem
jelenítené meg, laponként hány sor tűnne el a 4. Kereszthivatkozások szakaszból (Károli-KH sor, üressé váló
igehely-fejléc) és a Minősítés „Független megerősítés” párjai közül. Csak olvas: a mai lapokat méri, nem generál.

Használat: python naplok/KH_ELREJTES_hatas.py
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


def main():
    gyanus = KH.gyanus_forrasok()
    _, step, _ = K.konyvek()
    print('| Motívum | Károli-KH sor (4.) | ebből eltűnne | üressé váló igehely-fejléc | KH-pár a Minősítésben | ebből eltűnne |')
    print('|---|---|---|---|---|---|')
    ossz = [0] * 5
    for nev in sorted(os.listdir(os.path.join(GYOKER, 'lexikon'))):
        if not nev.endswith('_TUDOMANYOS.md'):
            continue
        with open(os.path.join(GYOKER, 'lexikon', nev), encoding='utf-8') as f:
            sorok = K.tagol(f.read())
        kh = tunik = ures = 0
        fejlec = {}
        for s in sorok:
            if not s.szakasz.startswith('4. Kereszthivatkoz') or not s.alszakasz:
                continue
            m = re.match(r'(\S+)\s+(\d+):(\d+)$', s.alszakasz.strip())
            if not m or m.group(1) not in step:
                continue
            forras = '%s.%s.%s' % (step[m.group(1)], m.group(2), m.group(3))
            f = fejlec.setdefault(s.alszakasz, [0, 0])
            if s.szoveg.strip().startswith('- TSK'):
                f[0] += 1
            elif s.szoveg.strip().startswith('- Károli-KH'):
                kh += 1
                if forras in gyanus:
                    tunik += 1
                else:
                    f[0] += 1
        ures = sum(1 for f in fejlec.values() if f[0] == 0)
        par = par_tunik = 0
        for s in sorok:
            m = re.match(r'^- (\S+ \d+:\d+) → .* — Károli-KH$', s.szoveg.strip())
            if m:
                par += 1
                a = re.match(r'(\S+)\s+(\d+):(\d+)', m.group(1))
                if a and a.group(1) in step and '%s.%s.%s' % (step[a.group(1)], a.group(2), a.group(3)) in gyanus:
                    par_tunik += 1
        for i, v in enumerate((kh, tunik, ures, par, par_tunik)):
            ossz[i] += v
        print('| %s | %d | %d | %d | %d | %d |' % (nev[:-len('_TUDOMANYOS.md')], kh, tunik, ures, par, par_tunik))
    print('| **összesen** | %d | %d | %d | %d | %d |' % tuple(ossz))


if __name__ == '__main__':
    main()
