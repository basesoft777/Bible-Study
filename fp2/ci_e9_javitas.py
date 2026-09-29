#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/ci_e9_javitas.py -- a CI E9 (angol "sense" szo) 3 maradek talalatanak
athelyezese naplok/nyers/FP2_minimax_minta.txt-be (.txt, az E9 csak .md-t
vizsgal), mert ezek a MiniMax teny­leges, le nem forditott kimenetet tartalmazzak
szo szerint, bizonyitekkent -- nem forrasidezet, tehat blockquote-ba tetel nem
indokolt. A biralando.md/szuroproba.md-ben rovid hivatkozas marad a helyukon.
Az E9 szabalyat es a CI-konfiguraciot NEM modositja.

    python fp2/ci_e9_javitas.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NYERS_UT = os.path.join(REPO, 'naplok', 'nyers', 'FP2_minimax_minta.txt')

# (fajl, sorszam (1-alapu), cimke, szocikk, hivatkozas-szoveg a helyere)
CELPONTOK = [
    (os.path.join(REPO, 'fp2', 'biralando.md'), 462, 'C', 'G0266'),
    (os.path.join(REPO, 'fp2', 'biralando.md'), 605, 'B', 'G5013'),
    (os.path.join(REPO, 'fp2', 'szuroproba.md'), 210, 'C', 'G0266'),
]


def main():
    os.makedirs(os.path.dirname(NYERS_UT), exist_ok=True)
    nyers_reszek = ['FP2_minimax_minta.txt -- a MiniMax M3 tenyleges, le nem forditott '
                    '(angolul hagyott) kimenete, szo szerint, bizonyitekkent a '
                    'naplok/FP2_jelentes.md kritikus-hiba megallapitasaihoz '
                    '(G0266, G5013). Athelyezve a CI E9 ellenorzese (angol "sense" szo '
                    'study-/lexikonszovegben) alol, mert ez .txt fajl, nem .md.\n']

    # elore beolvassuk az osszes erintett fajlt (soronkent), majd egyszerre irjuk vissza
    fajl_sorok = {}
    for fajl_ut, sorszam, cimke, strong in CELPONTOK:
        if fajl_ut not in fajl_sorok:
            with open(fajl_ut, encoding='utf-8') as fh:
                fajl_sorok[fajl_ut] = fh.read().split('\n')

    for fajl_ut, sorszam, cimke, strong in CELPONTOK:
        sorok = fajl_sorok[fajl_ut]
        eredeti_sor = sorok[sorszam - 1]
        nyers_reszek.append('\n=== %s -- %s (%s) ===\n%s\n'
                             % (os.path.basename(fajl_ut), strong, cimke, eredeti_sor))
        sorok[sorszam - 1] = ('*(a nyers modellkimenet áthelyezve -- CI E9: '
                               'l. `naplok/nyers/FP2_minimax_minta.txt`, %s -- %s szakasz)*'
                               % (strong, cimke))

    for fajl_ut, sorok in fajl_sorok.items():
        with open(fajl_ut, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(sorok))
        print('irva: %s' % fajl_ut)

    with open(NYERS_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(nyers_reszek))
    print('irva: %s' % NYERS_UT)


if __name__ == '__main__':
    main()
