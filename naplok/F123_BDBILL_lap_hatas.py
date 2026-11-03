#!/usr/bin/env python
"""F123.BDBILL: mit kap a lap BDB-gerince (`lexikon_general.bdb_gerinc_szakaszok`) egy Strongra a régi (HEAD) és az új
`bdb_szakasz_hu.tsv`-ből. Szakaszonként: magyar szöveg van / nincs (a lapon: angol + „fordításra vár”) / `elakad`. Fájlt nem ír.

Futtatás: python naplok/F123_BDBILL_lap_hatas.py <régi tábla útvonala> H1875 H8415 …
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
os.chdir(GYOKER)
import lexikon_general as LG  # noqa: E402


def gerinc(tabla, strong):
    LG._gerinc_adat_cache = None
    regi = LG.BDB_SZAKASZ_HU_FAJL
    LG.BDB_SZAKASZ_HU_FAJL = tabla
    try:
        return LG.bdb_gerinc_szakaszok(LG.gerinc_adat(), strong)
    finally:
        LG.BDB_SZAKASZ_HU_FAJL = regi
        LG._gerinc_adat_cache = None


def main():
    regi_tabla, strongok = sys.argv[1], sys.argv[2:]
    for st in strongok:
        a, b = gerinc(regi_tabla, st), gerinc('adat/bdb_szakasz_hu.tsv', st)
        nincs_a = sum(1 for x in a if not x[2])
        nincs_b = sum(1 for x in b if not x[2])
        print('%s: útvonal %d; magyar szöveg nélkül (a lapon angol + „fordításra vár”): régi %d → új %d'
              % (st, len(b), nincs_a, nincs_b))
        for x, y in zip(a, b):
            if (x[2] or '') != (y[2] or ''):
                print('   %-10s régi: %s' % (x[0], (x[2] or '—')[:70]))
                print('   %-10s új:   %s' % ('', (y[2] or '—')[:70]))


if __name__ == '__main__':
    main()
