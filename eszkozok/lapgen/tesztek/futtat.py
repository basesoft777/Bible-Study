"""A lapgen tesztjeinek futtatója.

    python eszkozok/lapgen/tesztek/futtat.py            # minden teszt_*.py
    python eszkozok/lapgen/tesztek/futtat.py szoveg     # csak a megnevezett fájl(ok): teszt_szoveg.py

Kilépési kód: 0, ha minden teszt zöld (a kihagyott teszt nem hiba; a számukat a futás kiírja).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
sys.path.insert(0, os.path.dirname(os.path.dirname(ITT)))


def main(argv):
    betolto = unittest.TestLoader()
    if argv:
        csomag = unittest.TestSuite(betolto.loadTestsFromName('teszt_%s' % nev) for nev in argv)
    else:
        csomag = betolto.discover(ITT, pattern='teszt_*.py', top_level_dir=ITT)
    eredmeny = unittest.TextTestRunner(verbosity=1).run(csomag)
    print('futott: %d, hiba: %d, bukás: %d, kihagyva: %d' % (
        eredmeny.testsRun, len(eredmeny.errors), len(eredmeny.failures), len(eredmeny.skipped)))
    return 0 if eredmeny.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
