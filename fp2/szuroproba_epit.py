#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/szuroproba_epit.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 6. lepes:
8 szocikk (5 kor2 + 3 uj, vegyes hosszal) kiemelese a mar elkeszult
fp2/biralando.md-bol (UGYANAZZAL az A/B/C sorrenddel, nem uj sorsolassal),
ures pontozo- es "melyik a legjobb" oszloppal.

    python fp2/szuroproba_epit.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIRALANDO_UT = os.path.join(REPO, 'fp2', 'biralando.md')
KIMENET_UT = os.path.join(REPO, 'fp2', 'szuroproba.md')

# 5 a kor2-mintabol (vegyes hossz: rovid/kozepes/hosszu/arany) + 3 az ujakbol
KIVALASZTOTT = ['G0004', 'G0813', 'G1941', 'G0086', 'G5590',
                'G2105', 'G3687', 'G0266']


def main():
    text = open(BIRALANDO_UT, encoding='utf-8').read()
    reszek = {}
    for strong in KIVALASZTOTT:
        start = text.index('## %s' % strong)
        vege_jelolo = '\n---\n'
        end = text.find(vege_jelolo, start)
        end = end if end != -1 else len(text)
        reszek[strong] = text[start:end].strip()

    with open(KIMENET_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# FP2 -- vak szúrópróba\n\n')
        fh.write('*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 6. lépés. 8 szócikk '
                  '(5 a kor2-mintából, 3 új), modellnév nélkül, A/B/C címkével -- '
                  'ugyanazzal a besorolással, mint az 5. lépés vak bírálatában. '
                  'Töltsd ki a Pontszám (0-10) és a "melyik a legjobb (A/B/C)" '
                  'oszlopot szócikkenként, majd add vissza. A kulcs csak ezután '
                  'nyílik meg.*\n\n')
        for strong in KIVALASZTOTT:
            fh.write(reszek[strong])
            fh.write('\n\n**Pontszám (A / B / C, 0-10):** ___ / ___ / ___\n\n')
            fh.write('**Melyik a legjobb?** ___\n\n')
            fh.write('**Megjegyzés:**\n\n')
            fh.write('\n---\n\n')

    print('irva: %s (%d szocikk)' % (KIMENET_UT, len(KIVALASZTOTT)))


if __name__ == '__main__':
    main()
