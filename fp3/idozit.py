#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp3/idozit.py -- F27_FP3_BRIEF.md P4: kezdes/befejezes idopont naplozasa szocikkenkent.

    python fp3/idozit.py kezd G0002
    python fp3/idozit.py vege G0002
"""

import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  'fp3', 'forditas', 'opus', 'idonaplo.tsv')


def main():
    esemeny, strong = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.dirname(UT), exist_ok=True)
    uj = not os.path.exists(UT)
    with open(UT, 'a', encoding='utf-8', newline='\n') as fh:
        if uj:
            fh.write('strong\tesemeny\tidopont_utc\n')
        fh.write('%s\t%s\t%s\n' % (strong, esemeny, datetime.now(timezone.utc).isoformat(timespec='seconds')))


if __name__ == '__main__':
    main()
