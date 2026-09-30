#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_bont.py -- F17.9: a konkordancia/Macula_heber.tsv egyszeri, konyvenkenti bontasa.

EGYSZERI, ARCHIV ESZKOZ: a regi konkordancia/Macula_heber.tsv az F17.11-ben torolve lett, a bontas
mar megtortent. A bemenet a regi egyetlen fajl (--be, KOTELEZO): git show f15fc91:konkordancia/Macula_heber.tsv > <ideiglenes_fajl>;
a kimenet
konkordancia/Macula_heber_<Konyv>.tsv (39 fajl), mindegyik sajat fejleccel (a licenc-attribucios
fejlecsorokkal egyutt) + egy konyv-sorral. A futtato (macula_futtat.py) ugyanezt a kiirast hasznalja,
igy ujrafuttatas ugyanezt a kimenetet adja. A bontas nem ir at adatot: a torzs (fejlec nelkul)
sorrendben osszefuzve bajtra azonos a regi fajl torzsevel (ezt --ellenoriz igazolja).

Hasznalat: python eszkozok/f17/macula_bont.py --be <regi_fajl> [--ellenoriz <regi_fajl>]
A konyvfajlok sorrendje a Macula-kanon (HEBER_KONYV_FAJL, macula_import.py).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import macula_kozos as K  # noqa: E402
import macula_import as M  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def beolvas(ut):
    fejlec, oszlop, sorok = [], None, []
    with open(ut, encoding='utf-8', newline='') as f:
        for l in f:
            l = l.rstrip('\n')
            if oszlop is None:
                if l.startswith('# '):
                    fejlec.append(l[2:])
                else:
                    oszlop = l.split('\t')
                continue
            sorok.append(l.split('\t'))
    return fejlec, oszlop, sorok


def torzs_bajt(ut):
    """A fajl adatsorai (a # sorok es az oszlopfejlec nelkul), nyers bajtokban."""
    ki = []
    with open(ut, 'rb') as f:
        elso = False
        for l in f:
            if not elso:
                if l.startswith(b'#'):
                    continue
                elso = True   # az oszlopfejlec
                continue
            ki.append(l)
    return b''.join(ki)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True, help='a regi Macula_heber.tsv (git show f15fc91:konkordancia/Macula_heber.tsv)')
    ap.add_argument('--ellenoriz', help='a regi fajl, amellyel a torzs bajtazonossagat vetjuk ossze')
    a = ap.parse_args()
    fejlec, oszlop, sorok = beolvas(a.be)
    ki = M.tsv_ir_konyvenkent(K.KONK, fejlec, oszlop, sorok)
    ossz = sum(db for _, db in ki)
    print('fajlok: %d, sorok osszesen: %d (bemenet: %d)' % (len(ki), ossz, len(sorok)))
    if ossz != len(sorok):
        sys.exit('SORSZAM-ELTERES')
    regi = torzs_bajt(a.ellenoriz or a.be)
    uj = b''.join(torzs_bajt(os.path.join(K.KONK, n)) for n, _ in ki)
    print('torzs bajtra azonos: %s (%d bajt)' % (regi == uj, len(uj)))
    if regi != uj:
        sys.exit('BAJT-ELTERES')
    for n, db in ki:
        print('%s\t%d\t%d' % (n, db, os.path.getsize(os.path.join(K.KONK, n))))


if __name__ == '__main__':
    main()
