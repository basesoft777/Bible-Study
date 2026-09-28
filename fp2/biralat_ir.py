#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/biralat_ir.py -- a fp2/biralat_adatok.py-ban rogzitett vak biralatot
irja fp2/biralat.tsv-be, es cimkenkenti (A/B/C, MEG NEM a modellnev szerinti)
osszesitot ad. A kulcs (fp2/anonim_kulcs.tsv) csak a 6. lepes (vak szuroproba)
utan nyilik meg.

    python fp2/biralat_ir.py
"""
import os
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from biralat_adatok import sorok_dict, FEJLEC  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIMENET_UT = os.path.join(REPO, 'fp2', 'biralat.tsv')


def main():
    sorok = list(sorok_dict())
    with open(KIMENET_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(FEJLEC) + '\n')
        for r in sorok:
            fh.write('\t'.join(str(r[m]) for m in FEJLEC) + '\n')
    print('irva: %s (%d sor)' % (KIMENET_UT, len(sorok)))

    cimkenkent = {}
    for r in sorok:
        cimkenkent.setdefault(r['cimke'], []).append(r)

    print('\n=== cimkenkenti osszesito (A/B/C -- a modell meg NEM ismert) ===')
    for cimke in sorted(cimkenkent):
        rs = cimkenkent[cimke]
        osszesenek = [r['osszesen'] for r in rs]
        termek = [r['termeszetesseg'] for r in rs]
        kritikus = sum(1 for r in rs if 'kritikus' in r['hibak'])
        print('  %s: n=%d | osszesen atlag=%.2f median=%.1f | termeszetesseg atlag=%.2f | kritikus hiba: %d/%d (%.0f%%)'
              % (cimke, len(rs), statistics.mean(osszesenek), statistics.median(osszesenek),
                 statistics.mean(termek), kritikus, len(rs), 100.0 * kritikus / len(rs)))


if __name__ == '__main__':
    main()
