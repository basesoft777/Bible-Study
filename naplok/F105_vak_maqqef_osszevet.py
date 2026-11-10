"""F105 (ELLENOR_F105 3.): a rafe-maqqéf vak minta két kitöltőjének összevetése a kulccsal, Wilson-intervallummal (95%).

Bemenet: `naplok/F105_vak_maqqef_kulcs.tsv` (sorszám, a szabály betűje), `naplok/F105_vak_maqqef_kitolto_1.tsv`,
`naplok/F105_vak_maqqef_kitolto_2.tsv` (sorszám, ítélet: A / B / egyik_sem / nem_donthető, indok).
Futtatás: python naplok/F105_vak_maqqef_osszevet.py
"""
import math
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

NAPLOK = os.path.dirname(os.path.abspath(__file__))


def rd(f):
    with open(os.path.join(NAPLOK, f), encoding='utf-8') as fh:
        sorok = fh.read().splitlines()
    return {r.split('\t')[0]: r.split('\t')[1] for r in sorok[1:] if r.strip()}


def wilson(x, n, z=1.96):
    p = x / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def main():
    k = rd('F105_vak_maqqef_kulcs.tsv')
    a = rd('F105_vak_maqqef_kitolto_1.tsv')
    b = rd('F105_vak_maqqef_kitolto_2.tsv')
    elter = [s for s in k if a.get(s) != b.get(s)]
    print('n', len(k), 'kitöltő-eltérés', elter)
    for nev, f in (('1. kitöltő', a), ('2. kitöltő', b)):
        x = sum(1 for s in k if f.get(s) == k[s])
        print(nev, x, len(k), '%.3f–%.3f' % wilson(x, len(k)))
    egy = [s for s in k if a.get(s) == b.get(s)]
    x = sum(1 for s in egy if a[s] == k[s])
    print('egyező ítélet, a szabályt választja', x, len(egy), '%.3f–%.3f' % wilson(x, len(egy)))
    print('a szabály ellen (egyező ítélet):', [s for s in egy if a[s] != k[s]])
    print('1. kitöltő, nem a kulcs:', {s: a[s] for s in k if a.get(s) != k[s]})
    print('2. kitöltő, nem a kulcs:', {s: b[s] for s in k if b.get(s) != k[s]})


if __name__ == '__main__':
    main()
