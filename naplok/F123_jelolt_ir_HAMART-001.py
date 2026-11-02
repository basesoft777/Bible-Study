#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F123_jelolt_ir_HAMART-001.py — DT-F123t (a) végrehajtása: a HAMART-001 negatív kritériumának mérhető kitételeiből
származó új helyek `nyitva` jelöltként az `adat/jeloltek.tsv`-be (F123.HAMART.A12).

Bemenet (az `allapot` = `ÚJ` sorok):
  - `naplok/F123_adat_HAMART-001_kollokacio.tsv` — a H6975+H1863 pár (Hós 10:8);
  - `naplok/F123_adat_HAMART-001_csalad.tsv` — a φθείρω-család `pozitív` tagjai (a `privatív` a munkafájlban marad);
  - `naplok/F123_adat_HAMART-001_lanc_ablak1.tsv` — a lánc-együttállás; az egymást követő versek (azonos fejezet)
    egy helynek számítanak (`5Móz 9:26-27`).
Döntés (beépítés/elutasítás) nincs: `dontes=nyitva`. Az indoklás-típus a DT-F123t szerint; a `forras_kereses` a mérés
proveniencia-sora.

TSV: split('\\t') / '\\t'.join() (a csv modul tilos, CLAUDE.md). Írás előtt a meglévő sorok változatlanságát
ellenőrzi; eltérésnél megáll. Futtatás: python naplok/F123_jelolt_ir_HAMART-001.py [--ir]
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
JEL = ROOT / 'adat' / 'jeloltek.tsv'
N = ROOT / 'naplok'
MID = 'HAMART-001'
DATUM = '2026.11.02'
VEG = '; F123 X.A (DT-F123t), elbírálatlan'
ALVIL = {'ApCsel 2:27', 'ApCsel 2:31', 'ApCsel 13:34', 'ApCsel 13:35', 'ApCsel 13:36', 'ApCsel 13:37'}


def olvas(nev):
    sorok = [s for s in (N / nev).read_text(encoding='utf-8').split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def sor(igehely, forras, ind):
    return [MID, igehely, forras, 'nyitva', ind, '', '', '', DATUM, 'elofordulas', '', '', '']


def hely_bontas(ig):
    konyv, cv = ig.rsplit(' ', 1)
    c, v = cv.split(':')
    return konyv, int(c), int(v)


def main():
    uj = []
    for r in olvas('F123_adat_HAMART-001_kollokacio.tsv'):
        if r['allapot'] == 'ÚJ':
            uj.append(sor(r['igehely'], 'kollokacio %s | %s' % (r['par'], r['proveniencia']),
                          'kollokáció (1Móz 3:18 gerinc-pár): %s egy versben%s' % (r['par'], VEG)))
    for r in olvas('F123_adat_HAMART-001_csalad.tsv'):
        if r['allapot'] == 'ÚJ' and r['tipus'] == 'pozitív':
            ind = 'φθείρω-család — a kritérium lexémája: %s %s' % (r['strong'], r['szoto'])
            if r['igehely'] in ALVIL:
                ind += ('; ALVIL-001-közelség: a Zsolt 16:10 (Seol) idézetének közege, az ApCsel 2:27 és 2:31 '
                        'ALVIL-001-előfordulás — motívumközi kérdés lehet')
            uj.append(sor(r['igehely'], 'csalad %s | %s' % (r['strong'], r['proveniencia']), ind + VEG))
    # lánc: az egymást követő versek egy hely
    csop = []
    for r in olvas('F123_adat_HAMART-001_lanc_ablak1.tsv'):
        if r['allapot'] != 'ÚJ':
            continue
        k, c, v = hely_bontas(r['igehely'])
        if csop and csop[-1]['k'] == (k, c) and csop[-1]['v'][-1] == v - 1:
            csop[-1]['v'].append(v)
            csop[-1]['lex'].update(r['lexema_az_ablakban'].split('+'))
        else:
            csop.append({'k': (k, c), 'v': [v], 'lex': set(r['lexema_az_ablakban'].split('+')), 'prov': r['proveniencia']})
    for g in csop:
        k, c = g['k']
        ig = '%s %d:%d' % (k, c, g['v'][0]) + ('-%d' % g['v'][-1] if len(g['v']) > 1 else '')
        uj.append(sor(ig, 'lanc ±1 | ' + g['prov'],
                      'lánc-együttállás — gyenge, strukturális közelítés; az értelmező menet dönt: %s%s'
                      % ('+'.join(sorted(g['lex'])), VEG)))

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
    if len({u[1] for u in uj}) != len(uj):
        sys.exit('ismétlődő igehely az új sorok közt')
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
