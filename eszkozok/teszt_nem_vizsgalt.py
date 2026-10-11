#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tesztek az eszkozok/nem_vizsgalt.py-hoz (F63). A hozzafuzes ideiglenes
tablamasolaton fut; az igazi adat/jeloltek.tsv-t nem erinti.
Futtatas: python eszkozok/teszt_nem_vizsgalt.py"""

import argparse
import os
import shutil
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nem_vizsgalt as N  # noqa: E402


def teszt_kibont():
    assert N.kibont('Zsid 7:1-28') == {'Zsid 7:%d' % i for i in range(1, 29)}
    assert N.kibont('1Móz 3:16') == {'1Móz 3:16'}
    assert N.kibont('Zsid 2:5-3:6') == {'Zsid 2:5', 'Zsid 3:6'}  # fejezethatar: a két vég


def teszt_lista_munkalappal():
    e0 = N.elemez('ALVIL-001', False)
    e1 = N.elemez('ALVIL-001', True)
    n0 = sum(len(v) for v in e0['nem_vizsgalt'].values())
    n1 = sum(len(v) for v in e1['nem_vizsgalt'].values())
    assert e1['kezelt'] >= e0['kezelt']
    assert n1 <= n0
    # a scan-halmaz futaskor, az elofordulasok.strong-bol vezetodik le
    s, _ = N.scan_halmaz('ALVIL-001')
    assert set(s) == {'H7585', 'G0086'}, s
    # kollokacio-tagok nem kulon scan
    s, k = N.scan_halmaz('ISTENTISZT-001')
    assert 'H7121' not in s and 'H8034' not in s and k and 'G1941' in s
    # csoportos kizaras kulon kategoria
    e = N.elemez('HAMART-001', False)
    assert 'H2403' in e['csoportos'] and 'H2403' not in e['nem_vizsgalt']


def teszt_hozzafuz():
    tmp = tempfile.mkdtemp()
    try:
        adat = os.path.join(tmp, 'adat')
        nap = os.path.join(tmp, 'naplok')
        os.makedirs(adat)
        os.makedirs(nap)
        shutil.copy(os.path.join(N.ADAT, 'jeloltek.tsv'), adat)
        shutil.copy(os.path.join(N.NAPLOK, 'JELOLTEK_RETRO_HODIT-001_sorok.tsv'), nap)
        regi_adat, regi_nap = N.ADAT, N.NAPLOK
        N.ADAT, N.NAPLOK = adat, nap
        try:
            p = os.path.join(adat, 'jeloltek.tsv')
            elotte = open(p, 'rb').read()
            # szaraz futas: nem ir
            N.cmd_hozzafuz(argparse.Namespace(id=['HODIT-001'], ir=False))
            assert open(p, 'rb').read() == elotte
            # iras: a regi bajtok valtozatlanok, +1 sor
            N.cmd_hozzafuz(argparse.Namespace(id=['HODIT-001'], ir=True))
            utana = open(p, 'rb').read()
            assert utana[:len(elotte)] == elotte and len(utana) > len(elotte)
            assert utana[len(elotte):].count(b'\n') == 1
            # masodik futas: mar letezo kulcs -> megallas
            try:
                N.cmd_hozzafuz(argparse.Namespace(id=['HODIT-001'], ir=True))
                raise AssertionError('nem allt meg')
            except SystemExit as ex:
                assert 'létező kulcs' in str(ex)
            assert open(p, 'rb').read() == utana
            # ervenytelen dontes -> megallas
            m = os.path.join(nap, 'JELOLTEK_RETRO_HODIT-001_sorok.tsv')
            szoveg = open(m, encoding='utf-8', newline='').read().replace('elutasítva', 'talan')
            open(m, 'w', encoding='utf-8', newline='').write(szoveg)
            try:
                N.munkalap_sorok('HODIT-001')
                raise AssertionError('nem allt meg')
            except SystemExit as ex:
                assert 'Érvénytelen dontes' in str(ex)
        finally:
            N.ADAT, N.NAPLOK = regi_adat, regi_nap
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    for f in (teszt_kibont, teszt_lista_munkalappal, teszt_hozzafuz):
        f()
        print('OK', f.__name__)
    print('Minden teszt rendben.')


if __name__ == '__main__':
    main()
