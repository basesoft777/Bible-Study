#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F123_jelolt_ir_ANTROP-001.py — DT-F123q (a) végrehajtása: az ANTROP-001 rokon alakos és versablakos
mérésének 9 új helye `nyitva` jelöltként az `adat/jeloltek.tsv`-be (F123.ANTROP.A7).

Bemenet: `naplok/F123_adat_ANTROP-001_rokon_ablak1.tsv` (az `allapot` = `ÚJ` sorok). Döntés (beépítés/elutasítás)
nincs: `dontes=nyitva`. Az indoklás a DT-F123q szerint: „azonos vers”, illetve „szomszédos vers — a mondathatár az
értelmező menetben ellenőrizendő”. A `forras_kereses` a mérés proveniencia-sora.

TSV: split('\\t') / '\\t'.join() (a csv modul tilos, CLAUDE.md). Írás előtt a meglévő sorok változatlanságát
ellenőrzi; eltérésnél megáll. Futtatás: python naplok/F123_jelolt_ir_ANTROP-001.py [--ir]
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
JEL = ROOT / 'adat' / 'jeloltek.tsv'
MERES = ROOT / 'naplok' / 'F123_adat_ANTROP-001_rokon_ablak1.tsv'
MID = 'ANTROP-001'
DATUM = '2026.11.02'


def igehely(mezo):
    """'Luk 9:55 – Luk 9:56' → 'Luk 9:55-56'; egy vers változatlan."""
    if ' – ' not in mezo:
        return mezo
    a, b = mezo.split(' – ')
    ka, va = a.rsplit(':', 1)
    kb, vb = b.rsplit(':', 1)
    if ka != kb:
        sys.exit('fejezethatáron átnyúló pár: %s' % mezo)
    return '%s:%s-%s' % (ka, va, vb)


def main():
    nyers = MERES.read_text(encoding='utf-8').split('\n')
    sorok = [s for s in nyers if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    uj = []
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        if r['allapot'] != 'ÚJ':
            continue
        if r['alap'] == 'azonos vers':
            ind = 'azonos vers'
        else:
            ind = 'szomszédos vers — a mondathatár az értelmező menetben ellenőrizendő'
        ind += ('; gerinc: G4151+G5590 (a versben: %s + %s, %s); F123 X.A rokon alakos és ±1 verses mérés (DT-F123q), '
                'elbírálatlan' % (r['a_csoport_a_versben'], r['b_csoport_a_versben'], r['alak']))
        forras = 'rokon (G4151|G4152) × (G5590|G5591) ±1 vers | ' + r['proveniencia']
        uj.append([MID, igehely(r['igehely']), forras, 'nyitva', ind, '', '', '', DATUM, 'elofordulas', '', '', ''])

    szoveg = JEL.read_text(encoding='utf-8')
    eredeti = szoveg.split('\n')
    fejlec = [s for s in eredeti if s and not s.startswith('#')][0].split('\t')
    if len(fejlec) != 13 or fejlec[:2] != ['id', 'igehely']:
        sys.exit('váratlan fejléc: %r' % fejlec)
    meglevo = {(s.split('\t')[0], s.split('\t')[1], s.split('\t')[9], s.split('\t')[10])
               for s in eredeti if s and not s.startswith('#') and s.split('\t')[0] != 'id'}
    for u in uj:
        if (u[0], u[1], u[9], u[10]) in meglevo:
            sys.exit('a kulcs már létezik: %s %s' % (u[0], u[1]))
    utolso = max(i for i, s in enumerate(eredeti) if s.split('\t')[0] == MID)
    ki = eredeti[:utolso + 1] + ['\t'.join(u) for u in uj] + eredeti[utolso + 1:]
    # ellenőrzés: a régi sorok változatlanok és sorrendjük megmarad
    if [s for s in ki if s not in {'\t'.join(u) for u in uj}] != eredeti:
        sys.exit('a meglévő sorok változnának — megállok')
    for u in uj:
        print('\t'.join(u[:2] + [u[4]]))
    print('új sor: %d' % len(uj))
    if '--ir' in sys.argv:
        JEL.write_text('\n'.join(ki), encoding='utf-8', newline='')
        print('írva: %s' % JEL.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
