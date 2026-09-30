#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_kozos.py -- F17 (Macula-import): kozos segedek.

- konyvkodok (USFM <-> STEP <-> magyar), a konkordancia/Konyv_normalizalo_tabla.tsv alapjan
- a Macula (heber: MT-szamozas; gorog: NT) versek -> Karoli-vers kulcs (KK)
- TSV-olvasas: split('\t'); iras: '\t'.join() (CLAUDE.md; a csv modul tilos)
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KONK = os.path.join(REPO, 'konkordancia')

USFM_OSZ = ('GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG '
            'ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL').split()
USFM_USZ = ('MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE '
            '1JN 2JN 3JN JUD REV').split()


def tsv_olvas(ut):
    """(fejlec, sorok); a '#'-sorokat es az ures sorokat kihagyja."""
    sorok = []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if not sor or sor.startswith('#'):
                continue
            sorok.append(sor.split('\t'))
    return sorok[0], sorok[1:]


def tisztit(x):
    return re.sub(r'[\t\r\n]+', ' ', str(x)).strip()


def konyvtablak():
    """(usfm->magyar, usfm->step, magyar->usfm, kanoni magyar lista)."""
    fej, sorok = tsv_olvas(os.path.join(KONK, 'Konyv_normalizalo_tabla.tsv'))
    step = [s[0] for s in sorok]
    mag = [s[1] for s in sorok]
    usfm = USFM_OSZ + USFM_USZ
    if len(step) < len(usfm):
        raise SystemExit('a normalizalo tabla rovidebb a vartnal')
    for i, u in enumerate(usfm):
        if step[i].upper() != u:
            raise SystemExit('konyvkod-elteres: %s <> %s (sor %d)' % (step[i], u, i))
    return ({u: mag[i] for i, u in enumerate(usfm)},
            {u: step[i] for i, u in enumerate(usfm)},
            {mag[i]: u for i, u in enumerate(usfm)},
            mag)


def karoli_versek():
    """{magyar konyv: {(fej, vers)}} a Karoli_1908.tsv-bol (a KK cel-kulcsa)."""
    fej, sorok = tsv_olvas(os.path.join(KONK, 'Karoli_1908.tsv'))
    ki = {}
    for s in sorok:
        m = re.match(r'^(\S+) (\d+):(\d+)$', s[0])
        if m:
            ki.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3))))
    return ki


def vers_tartomany(szoveg, alap_fej):
    """'11:14,23-25' | '3:1' | '9:99-9:9' | '10:1a' -> [(fej, vers), ...]; '--' -> [];
    az ertelmezhetetlen darab None-t ad vissza a listaban (jelzes)."""
    szoveg = szoveg.strip()
    if szoveg in ('', '--'):
        return []
    ki = []
    fej = alap_fej
    for darab in re.split(r'[;,]', szoveg):
        darab = darab.strip()
        if not darab:
            continue
        m = re.fullmatch(r'(?:(\d+):)?(\d+)[a-z]?(?:-(?:(\d+):)?(\d+)[a-z]?)?', darab)
        if not m:
            ki.append(None)
            continue
        if m.group(1):
            fej = int(m.group(1))
        v1 = int(m.group(2))
        if m.group(4):
            fej2 = int(m.group(3)) if m.group(3) else fej
            v2 = int(m.group(4))
            if fej2 == fej:
                ki.extend((fej, v) for v in range(v1, v2 + 1))
            else:
                ki.append((fej, v1))
                ki.append((fej2, v2))
                ki.append(None)  # fejezeten atnyulo tartomany: koztes versek nem ismertek
            fej = fej2
        else:
            ki.append((fej, v1))
    return ki
