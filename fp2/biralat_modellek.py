#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/biralat_modellek.py -- a kulcs megnyitasa UTAN: a vak biralat (fp2/biralat_adatok.py,
cimke szerint) es az anonim_kulcs.tsv (cimke -> valodi modell) osszefesulese, kulon a
darabolt es a nem darabolt szocikkekre (FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, a
felhasznalo kiegeszito 3. kerdese, 2026.09.28).

    python fp2/biralat_modellek.py
"""
import os
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'fp2'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
from biralat_adatok import sorok_dict  # noqa: E402
import fordit  # noqa: E402

KULCS_UT = os.path.join(REPO, 'fp2', 'anonim_kulcs.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def main():
    kulcs = {(r['strong'], r['cimke']): r['modell'] for r in tsv_dict_sorok(KULCS_UT)}
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)}

    darabszam = {}
    for strong, szoveg in thayer.items():
        darabszam[strong] = len(fordit.darabokra_bont(szoveg))

    sorok = list(sorok_dict())
    for r in sorok:
        r['modell'] = kulcs[(r['strong'], r['cimke'])]
        r['darabolt'] = darabszam.get(r['strong'], 1) > 1

    print('=== modellenkenti osszesito -- TELJES 30 szocikk ===')
    _kiir(sorok)

    print('\n=== modellenkenti osszesito -- CSAK NEM DARABOLT szocikkek (n=%d) ==='
          % sum(1 for r in sorok if not r['darabolt']) // 3 if False else '')
    nem_darabolt = [r for r in sorok if not r['darabolt']]
    print('(%d ertekeles / 3 modell = %d szocikk)' % (len(nem_darabolt), len(nem_darabolt) // 3))
    _kiir(nem_darabolt)

    print('\n=== modellenkenti osszesito -- CSAK DARABOLT szocikkek ===')
    darabolt = [r for r in sorok if r['darabolt']]
    print('(%d ertekeles / 3 modell = %d szocikk)' % (len(darabolt), len(darabolt) // 3))
    _kiir(darabolt)

    print('\n=== kritikus hibak modellenkent (osszes 30 szocikk) ===')
    for modell in sorted(set(r['modell'] for r in sorok)):
        rs = [r for r in sorok if r['modell'] == modell]
        krit = [r for r in rs if 'kritikus' in r['hibak']]
        print('  %-32s kritikus: %d/%d' % (modell, len(krit), len(rs)))
        for r in krit:
            print('      %s (%s, darabolt=%s): %s' % (r['strong'], r['hibak'], r['darabolt'], r['megjegyzes']))


def _kiir(sorok):
    for modell in sorted(set(r['modell'] for r in sorok)):
        rs = [r for r in sorok if r['modell'] == modell]
        if not rs:
            continue
        oszz = [r['osszesen'] for r in rs]
        term = [r['termeszetesseg'] for r in rs]
        krit = sum(1 for r in rs if 'kritikus' in r['hibak'])
        print('  %-32s n=%2d | osszesen atlag=%.2f median=%.1f | termeszetesseg atlag=%.2f | kritikus: %d/%d (%.0f%%)'
              % (modell, len(rs), statistics.mean(oszz), statistics.median(oszz),
                 statistics.mean(term), krit, len(rs), 100.0 * krit / len(rs)))


if __name__ == '__main__':
    main()
