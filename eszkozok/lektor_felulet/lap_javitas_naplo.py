#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lap_javitas_naplo.py -- F165 (LAPJAVIT_ARTIFACT): biztonságos hozzáfűzés az `adat/lap_javitasok.tsv`-hez (SEMA 2.49),
a `/lap-javit` 4. pontjához.

A session a jóváhagyott helyek sorait egy repón kívüli TSV-be írja (fejléc a sémáé, a fejléc-sor el is hagyható), és:

    python eszkozok/lektor_felulet/lap_javitas_naplo.py <tmp>/naplo_uj.tsv

A szkript a sorokat a napló végére fűzi, és megáll (kilépési kód 2, írás nélkül), ha:
- a napló fejléce eltér a sémától, vagy egy új sor mezőszáma rossz;
- egy új sor az `ellenoriz.py` 30. szabálya szerint hibás (`lap_javitas_hibak`: zárt `tipus`/`gond`, dátum,
  létező motívum, a `jovahagyta` nem modellnév, érvényes proveniencia, nincs üres mező);
- a kulcs (`id` + `hely` + `datum`) már szerepel;
- a meglévő sorok bármelyike változna.
Olvasás `split('\\t')`, írás `'\\t'.join()` (CLAUDE.md).
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HELY))
sys.path.insert(0, os.path.dirname(HELY))
import ellenoriz as E  # noqa: E402

NAPLO = os.path.join(ROOT, 'adat', 'lap_javitasok.tsv')
FEJLEC = E.LAP_JAVITASOK_FEJLEC


def _beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    return sorok


def motivumok(root=ROOT):
    return {s.split('\t')[0] for s in _beolvas(os.path.join(root, 'adat', 'motivumok.tsv')) if s and not s.startswith('#')}


def hozzafuz(uj_ut, naplo=NAPLO, motivum_id_halmaz=None):
    """Az új sorok hozzáfűzése; a hozzáfűzött sorok száma. Hibánál ValueError, írás nélkül."""
    regi = _beolvas(naplo)
    adat_regi = [s for s in regi if s and not s.startswith('#')]
    if not adat_regi or adat_regi[0].split('\t') != FEJLEC:
        raise ValueError('a napló fejléce eltér a sémától')
    ujak = [s for s in _beolvas(uj_ut) if s.strip() and not s.startswith('#')]
    if ujak and ujak[0].split('\t') == FEJLEC:
        ujak = ujak[1:]
    if not ujak:
        raise ValueError('nincs hozzáfűzendő sor')
    rek = []
    for s in ujak:
        m = s.split('\t')
        if len(m) != len(FEJLEC):
            raise ValueError('%d mező a várt %d helyett: %s' % (len(m), len(FEJLEC), s[:80]))
        rek.append(dict(zip(FEJLEC, m)))
    hibak = E.lap_javitas_hibak(FEJLEC, rek, motivumok() if motivum_id_halmaz is None else motivum_id_halmaz)
    if hibak:
        raise ValueError('a 30. szabály szerint hibás sor(ok):\n  ' + '\n  '.join(hibak))
    kulcsok = {tuple(s.split('\t')[i] for i in (0, 1, 8)) for s in adat_regi[1:]}
    for r in rek:
        k = (r['id'], r['hely'], r['datum'])
        if k in kulcsok:
            raise ValueError('kulcs-ütközés: %s / %s / %s' % k)
        kulcsok.add(k)
    uj_szoveg = '\n'.join(regi + ['\t'.join(r[k] for k in FEJLEC) for r in rek]) + '\n'
    if not uj_szoveg.startswith('\n'.join(regi)):
        raise ValueError('a meglévő sorok változnának: megállok')
    with open(naplo, 'w', encoding='utf-8', newline='\n') as f:
        f.write(uj_szoveg)
    return len(rek)


def main():
    if len(sys.argv) != 2:
        raise ValueError('használat: lap_javitas_naplo.py <új sorok TSV>')
    print('  %d sor hozzáfűzve: %s' % (hozzafuz(sys.argv[1]), NAPLO))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
