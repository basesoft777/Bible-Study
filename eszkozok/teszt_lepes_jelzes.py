#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_lepes_jelzes.py -- F0.33: az `eszkozok/lepes_jelzes.py` (több lépéses PR és álló draft jelzése) tesztje.

Fut: python eszkozok/teszt_lepes_jelzes.py (a CI-ben is). Kilépési kód: 0 = zöld. Hálózatot nem használ.
"""

import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lepes_jelzes as L

HIBAK = []


def ellenoriz(feltetel, nev):
    if feltetel:
        print('RENDBEN  ' + nev)
    else:
        print('BUKOTT   ' + nev)
        HIBAK.append(nev)


def main():
    # egy lépés több commitja, a .0 befogadás és a betűs utótag: nincs jelzés
    ellenoriz(L.tobb_lepes(['F241.0: a brief befogadása', 'F241.1: első', 'F241.1: első, javítva']) == {}, 'egy lépés + .0: nincs jelzés')
    ellenoriz(L.tobb_lepes(['F241.5: a lépés', 'F241.5b: ugyanaz a lépés javítva']) == {}, '5 és 5b egy lépés')
    # több lépés ugyanabból a feladatból
    ellenoriz(L.tobb_lepes(['F241.4: licenckapu', 'F241.5: fordítás']) == {'F241': ['4', '5']}, 'F241.4 + F241.5')
    ellenoriz(L.tobb_lepes(['F240.L1: a', 'F240.L7 — b']) == {'F240': ['L1', 'L7']}, 'F240.L1 + F240.L7 (betűs lépés)')
    ellenoriz(L.tobb_lepes(['F241.0: a', 'F241.1: b', 'F241.2: c']) == {'F241': ['1', '2']}, 'a .0 nem számít lépésnek')
    # különböző feladatok külön számolnak
    ellenoriz(L.tobb_lepes(['F241.1: a', 'F242.1: b']) == {}, 'két feladat egy-egy lépéssel: nincs jelzés')
    ellenoriz(L.tobb_lepes(['F241.1: a', 'F241.2: b', 'F242.1: c']) == {'F241': ['1', '2']}, 'csak az érintett feladat jelez')
    ellenoriz(L.tobb_lepes(['F218a.S8c: a', 'F218a.S9: b', 'F218.1: c']) == {'F218a': ['S8c', 'S9']}, 'a feladat betűs utótagja külön feladat')
    # kimaradók
    kimarad = ['F0.31: gépi', 'F0.32: gépi', 'FELADATOK.md frissítés (gép)', 'szamkiosztas: DT1', 'Merge pull request #1',
               'OLVASO-GYORS: valami', 'DESIGN-APRO: valami', 'F241 lépés pont nélkül', '']
    ellenoriz(L.tetelek(kimarad) == {}, 'F0.<n>, gépi és előtag nélküli tárgyak nem számítanak')
    # sorrend: első előfordulás
    ellenoriz(L.tetelek(['F5.3: a', 'F5.1: b', 'F5.3: c'])['F5'] == ['3', '1'], 'első előfordulás sorrendje, ismétlés nélkül')
    # a szöveg
    sz = L.lepes_szoveg({'F241': ['4', '5']})
    ellenoriz(L.MARKER_LEPES in sz and 'F241' in sz and '`.4`' in sz, 'a jelzés szövege: marker, feladat, lépések')
    ellenoriz('nem bukás' in sz, 'a jelzés kimondja, hogy nem bukás')
    ellenoriz(L.MARKER_ALLO in L.allo_szoveg(3) and '3 napja' in L.allo_szoveg(3), 'az álló draft jelzés szövege')
    # a CLI helyi módja egy ideiglenes fájlból, hálózat és token nélkül
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, 'targyak.txt')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write('F9.1: a\nF9.2: b\n')
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lepes_jelzes.py'), 'pr', '--uzenetek', f],
                           capture_output=True, text=True, encoding='utf-8', env={k: v for k, v in os.environ.items() if k not in ('GITHUB_TOKEN', 'PR_SZAM')})
        ellenoriz(r.returncode == 0 and 'F9' in r.stdout, 'CLI: jelez, de nem bukik (kilépési kód 0, token nélkül sem ír kommentet)')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write('F9.1: a\nF0.2: gépi\n')
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lepes_jelzes.py'), 'pr', '--uzenetek', f],
                           capture_output=True, text=True, encoding='utf-8')
        ellenoriz(r.returncode == 0 and 'nincs jelzés' in r.stdout, 'CLI: egy lépés, nincs jelzés')
    # a feladat-main keresés: ismert feladat (F239.1 a main-ben van?) nem hálózat, csak git; ismeretlen feladat nincs
    try:
        ellenoriz(L.feladat_a_mainben('F99999') is False, 'ismeretlen feladat nincs a main-ben')
        ellenoriz(L.feladat_a_mainben('F231') is True, 'az F231 lépései a main-ben vannak')
    except RuntimeError as e:
        print('KIHAGYVA  a feladat_a_mainben git-ellenőrzése (nincs origin/main: %s)' % str(e)[:80])

    print('\n%s' % ('MINDEN ZÖLD' if not HIBAK else 'BUKOTT: %d' % len(HIBAK)))
    return 0 if not HIBAK else 1


if __name__ == '__main__':
    sys.exit(main())
