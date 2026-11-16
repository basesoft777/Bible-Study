#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szamkiosztas_ujragen.py -- F201, F217: vékony hívás.

F201 óta a számkiosztás után ez generálta újra a számtól függő nézeteket (marker-blokkok, a migrált lapok,
a nyílt mag), hogy az E28/E35 a main-en ne pirosodjon be (DT-F201a). F217 óta a main-en minden push után
a generált nézetek jegyzéke (`adat/generalt_nezetek.tsv`) szerint az `eszkozok/generalt_nezetek.py --ir`
generál újra (a feladatok.yml 2. lépése, kiosztástól függetlenül); ez a szkript csak továbbhív, hogy a régi
parancs ugyanazt tegye.

CLI:
    python eszkozok/szamkiosztas_ujragen.py            # = generalt_nezetek.py --ir
    python eszkozok/szamkiosztas_ujragen.py --lista    # = generalt_nezetek.py --lista
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generalt_nezetek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    sys.argv = [sys.argv[0], '--lista' if '--lista' in sys.argv[1:] else '--ir']
    return generalt_nezetek.main()


if __name__ == '__main__':
    sys.exit(main())
