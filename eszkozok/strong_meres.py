#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/strong_meres.py -- F62: a Strong-értékek SEMA 1.2 szerinti mérése (csak olvas).

Két hatókört mér, külön sorokban:
  (A) STRONG-típusú oszlopok: azok, amelyeknek a fejléce `strong`-ot tartalmaz
      (`strong`, `heber_strong`, `gorog_strong`, `hebrew_strong`, `Strong-szám`, ...),
      az `adat/**/*.tsv` fájlokban és a `konkordancia/Karoli_Strong_kivonat.tsv`-ben.
      Itt minden nem üres cellának SEMA 1.2 alakúnak kell lennie (strong_util.strong_ervenyes).
  (B) forrásalakú értékek: az (A)-n KÍVÜLI oszlopok azon cellái, amelyek teljes egészében
      Strong-kódnak látszanak (`^[HG]\\d+[a-z]?` + `+` lánc), de nem SEMA 1.2 alakúak. Ezek nem a
      STRONG-típusú oszlopban állnak (pl. szótári forrásmezők), nem normalizálandók, de a
      hatókör kimondásához megszámoljuk őket.

A TSV-olvasás `split('\\t')` (a csv modul tilos, CLAUDE.md). Adatot nem ír.

    python eszkozok/strong_meres.py            # összegzés + proveniencia-sor
    python eszkozok/strong_meres.py --reszlet  # oszloponként is
"""

import argparse
import datetime
import glob
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
from strong_util import strong_ervenyes  # noqa: E402

ROOT = os.path.dirname(ITT)
KODSZERU = re.compile(r'^[HG]\d+[a-z]?(\+[HG]\d+[a-z]?)*$')


def fajlok():
    lista = sorted(glob.glob(os.path.join(ROOT, 'adat', '**', '*.tsv'), recursive=True))
    lista.append(os.path.join(ROOT, 'konkordancia', 'Karoli_Strong_kivonat.tsv'))
    return lista


def tsv_sorok(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f]
    return [s for s in sorok if s.strip() and not s.startswith('#')]


def meres():
    """-> (A-oszlopok szama, A-fajlok szama, A-nem-ures, A-eltérés, B-darab, reszletek)"""
    a_oszlop = a_fajl = a_nemures = a_elter = b_db = 0
    resz = []
    for ut in fajlok():
        sorok = tsv_sorok(ut)
        if not sorok:
            continue
        rel = os.path.relpath(ut, ROOT).replace(os.sep, '/')
        fej = sorok[0].split('\t')
        a_idx = [i for i, h in enumerate(fej) if 'strong' in h.lower() and h.lower() != 'strong_vart']
        if a_idx:
            a_fajl += 1
        a_oszlop += len(a_idx)
        for i, h in enumerate(fej):
            nemures = elter = forras = 0
            for s in sorok[1:]:
                p = s.split('\t')
                v = p[i] if i < len(p) else ''
                if not v:
                    continue
                if i in a_idx:
                    nemures += 1
                    if not strong_ervenyes(v):
                        elter += 1
                elif KODSZERU.match(v) and not strong_ervenyes(v):
                    forras += 1
            if i in a_idx:
                a_nemures += nemures
                a_elter += elter
                resz.append('A  %s | %s | nemüres=%d | nem SEMA 1.2=%d' % (rel, h, nemures, elter))
            elif forras:
                b_db += forras
                resz.append('B  %s | %s | forrásalakú, nem SEMA 1.2=%d' % (rel, h, forras))
    return a_oszlop, a_fajl, a_nemures, a_elter, b_db, resz


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--reszlet', action='store_true')
    args = ap.parse_args()
    a_oszlop, a_fajl, a_nemures, a_elter, b_db, resz = meres()
    if args.reszlet:
        for r in resz:
            print(r)
    print('(A) STRONG-típusú oszlop: %d oszlop, %d fájl; nem üres cella: %d; nem SEMA 1.2: %d'
          % (a_oszlop, a_fajl, a_nemures, a_elter))
    print('(B) forrásalakú, nem STRONG-típusú oszlopban álló, nem SEMA 1.2 alakú érték: %d' % b_db)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M') + 'Z'
    print('proveniencia: scope=adat/**/*.tsv+konkordancia/Karoli_Strong_kivonat.tsv | '
          'forras=eszkozok/strong_meres.py | a=%d | b=%d | ts=%s' % (a_elter, b_db, ts))


if __name__ == '__main__':
    main()
