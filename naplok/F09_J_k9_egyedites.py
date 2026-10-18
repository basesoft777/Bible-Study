#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_k9_egyedites.py -- DT-F09j: a görög kiejtés-aranykészlet darabszámai (K9, F05 D23).

Méri: (1) az F05 D23 aranykészlete nyersen hány görög sor (naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv,
nyelv=gorog, besorolas=arany); (2) egyedítve hány pár; (3) melyik a 4 kontextusfüggő pár, amely nincs a
gépileg tesztelhető 26-ban (naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv); (4) mennyi a maradék.
TSV-olvasás kizárólag split('\\t') (CLAUDE.md).

    python naplok/F09_J_k9_egyedites.py
"""

import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESZT = os.path.join(ROOT, 'naplok', 'SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv')
ARANY26 = os.path.join(ROOT, 'naplok', 'SZOTAR_S1_kiejtes_arany_sbl.tsv')


def sorok(ut):
    """(fejléc, [dict]) -- a '#' kezdetű sorok kihagyva."""
    fej, ki = None, []
    with io.open(ut, encoding='utf-8', newline='') as f:
        for sor in f.read().replace('\r\n', '\n').split('\n'):
            if not sor.strip() or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(dict(zip(fej, m)))
    return fej, ki


def main():
    _, t = sorok(TESZT)
    nyers = [r for r in t if r['nyelv'] == 'gorog' and r['besorolas'] == 'arany']
    print('1. nyers görög arany sor: %d' % len(nyers))
    # egyedítés: a szó és a kiejtés-mező G-kód nélküli alakja (az "epikaleó" és "epikaleó, G1941" ugyanaz a pár)
    def kiej(r):
        return r['kiejtes'].split(',')[0].strip()
    egyedi = {}
    for r in nyers:
        egyedi.setdefault((r['szo'], kiej(r)), []).append(r)
    print('2. egyedi (szó, kiejtés G-kód nélkül) pár: %d; csak szó szerint egyedi: %d; (szó, teljes kiejtés-mező) egyedi: %d'
          % (len(egyedi), len(set(r['szo'] for r in nyers)), len(set((r['szo'], r['kiejtes']) for r in nyers))))
    _, a = sorok(ARANY26)
    szavak26 = set(r['szo_gorog'] for r in a)
    print('3. a gépileg tesztelhető sorok (SZOTAR_S1_kiejtes_arany_sbl.tsv): %d' % len(a))
    # a csonkolt "szo" (a gold szó eleje hiányzik) miatt a megfeleltetés a 26 szó végződésére is megy
    def megvan(szo):
        return szo in szavak26 or any(sz.endswith(szo) for sz in szavak26)
    kontext = [(szo, k) for (szo, k) in egyedi if not megvan(szo)]
    print('4. a 26-ban nincs meg (kontextusfüggő pár): %d' % len(kontext))
    for szo, k in sorted(kontext):
        print('   - %s | %s | %s' % (szo, k, egyedi[(szo, k)][0]['hely']))
    print('5. maradék (egyedi - kontextusfüggő): %d' % (len(egyedi) - len(kontext)))
    # a K9 / DT-F09j mért számai: 50 nyers -> 30 egyedi -> 4 kontextusfüggő -> 26 marad
    assert len(nyers) == 50, len(nyers)
    assert len(egyedi) == 30, len(egyedi)
    assert len(a) == 26, len(a)
    assert len(kontext) == 4, len(kontext)
    assert len(egyedi) - len(kontext) == 26
    print('assert OK: 50 / 30 / 4 / 26')
    print('proveniencia: scope=naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv (nyelv=gorog, besorolas=arany) + '
          'naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv | forras=naplok/F09_J_k9_egyedites.py | ts=2026-10-17')


if __name__ == '__main__':
    main()
