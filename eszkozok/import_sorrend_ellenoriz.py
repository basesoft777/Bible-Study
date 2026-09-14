#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modulszintű név-kötési sorrend ellenőrzése — MELLÉKHATÁS NÉLKÜL.

Azt a hibaosztályt fogja meg, amit a 28ae8d4-ben a stdout-őr okozott: a modul
törzse használ egy nevet (pl. `sys`), amelyet csak később importál, tehát a
szkript NameError-rel bukik, még mielőtt bármit csinálna.

Miért nem `python szkript.py --help`: az eszkozok/*.py huszonnégyből tizenkilenc
NEM használ argparse-t, tehát a --help nem súgót ír, hanem lefuttatja a teljes
szkriptet — a betöltők pedig ilyenkor felülírják az adat/*.tsv-t. A futtatásos
füstteszt ezen a repón adatvesztést okoz, nem diagnózist.

Miért nem grep: az `import csv, sys, os, io, re` alakot a soralapú minta nem
fogja meg (három fájl ilyen), és téves riasztást ad.

Futtatás a repó gyökeréből:
    python eszkozok/import_sorrend_ellenoriz.py
Kilépési kód 1, ha van hibás fájl.
"""

import ast
import builtins
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESZKOZOK = os.path.join(ROOT, 'eszkozok')


# A modul betöltésekor a Python maga köti ezeket, import nélkül.
DUNDER = {'__file__', '__name__', '__doc__', '__package__', '__spec__',
          '__loader__', '__builtins__', '__debug__'}


def kotesek(fa):
    """Modulszintű névkötések: név -> a legkorábbi sor, ahol kötve lesz."""
    ki = {}
    for csomo in ast.walk(fa):
        nevek = []
        if isinstance(csomo, (ast.Import, ast.ImportFrom)):
            for a in csomo.names:
                nevek.append((a.asname or a.name).split('.')[0])
        elif isinstance(csomo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nevek.append(csomo.name)
        elif isinstance(csomo, ast.Name) and isinstance(csomo.ctx, ast.Store):
            nevek.append(csomo.id)
        elif isinstance(csomo, ast.ExceptHandler) and csomo.name:
            nevek.append(csomo.name)
        elif isinstance(csomo, ast.arg):
            nevek.append(csomo.arg)
        for n in nevek:
            if n not in ki or csomo.lineno < ki[n]:
                ki[n] = csomo.lineno
    return ki


def modulszintu_hasznalat(fa):
    """(név, sor) párok, amelyek a modul TÖRZSÉBEN olvasnak egy nevet —
    függvény- és osztálytörzsek kihagyva, azok csak hívásukkor futnak."""
    ki = []

    def bejar(csomo):
        for gyerek in ast.iter_child_nodes(csomo):
            if isinstance(gyerek, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            # A listaértelmezések saját hatókört kapnak; a ciklusváltozójuk
            # nem modulszintű név, ezért az egész csomópontot kihagyjuk.
            if isinstance(gyerek, (ast.ListComp, ast.SetComp, ast.DictComp,
                                   ast.GeneratorExp, ast.Lambda)):
                continue
            if isinstance(gyerek, ast.Name) and isinstance(gyerek.ctx, ast.Load):
                ki.append((gyerek.id, gyerek.lineno))
            bejar(gyerek)

    bejar(fa)
    return ki


def main():
    hibas = []
    fajlok = sorted(f for f in os.listdir(ESZKOZOK) if f.endswith('.py'))
    for fn in fajlok:
        ut = os.path.join(ESZKOZOK, fn)
        with open(ut, encoding='utf-8') as f:
            forras = f.read()
        try:
            fa = ast.parse(forras, filename=fn)
        except SyntaxError as e:
            hibas.append((fn, 'SyntaxError', e.lineno, '-'))
            continue
        kot = kotesek(fa)
        beepitett = set(dir(builtins)) | DUNDER
        for nev, sor in modulszintu_hasznalat(fa):
            if nev in beepitett:
                continue
            if nev not in kot:
                hibas.append((fn, nev, sor, 'nincs kötve'))
            elif sor < kot[nev]:
                hibas.append((fn, nev, sor, kot[nev]))

    if not hibas:
        print('OK — mind a %d eszkozok/*.py modulszintű névhasználata a kötés után áll.'
              % len(fajlok))
        return 0

    print('HIBÁS FÁJLOK (%d):' % len({h[0] for h in hibas}))
    for fn, nev, sor, kotes in hibas:
        print('  %-40s `%s` használva a %s. sorban, kötve a %s. sorban'
              % (fn, nev, sor, kotes))
    return 1


if __name__ == '__main__':
    sys.exit(main())
