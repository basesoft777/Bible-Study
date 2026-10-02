#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_zaras.py -- F38 zaromenet (DT-F38e): az uj normalizalo-
szabalyok (eszkozok/normalizal.py: elofordulas, nevalakok, konyv_rov, a
F38.261-es tapadt konyvjelzes-leválasztas) es a glossza_visszaallit
visszamenoleges futtatasa a 269 BDB-szocikken, a teljes kapusorral elotte /
utana.

Irni (--ir) csak az `F38 BDB_FORDITAS` megjegyzesu sorokat irja (243); a #28
kezi/opus sorainak (26) szovege nem valtozik, ott a javitas csak listazva van
(`nem_irt` jeloles a kimenetben). Minden sor kapuit a sor sajat terminologia-
kiveteleivel futtatja; ha az uj szoveg nem megy at a gatolo kapukon, megall.
A kimenet: naplok/BDB_FORDITAS_zaras_javitasok.tsv (szocikk, szabaly, regi, uj,
db, iras) es a kapu-osszesites a standard kimeneten.

    python naplok/BDB_FORDITAS_zaras.py            # csak jelentes
    python naplok/BDB_FORDITAS_zaras.py --ir
"""

import argparse
import collections
import difflib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
import normalizal as N  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402

JEL = 'F38 BDB_FORDITAS'
JELOLES = 'F38.267: zárómenet — normalizáló (N t., Izráel, 1Pét, tapadt könyvjelzés), RV/AV-glossza (DT-F38e)'
ELOZO_JELOLES = 'F38.267'
JOVAHAGYAS_REGI = 'jóváhagyásra: DT-F38d'
JOVAHAGYAS_UJ = 'jóváhagyva: DT-F38d (b), 2026.10.02'
KIMENET = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_zaras_javitasok.tsv')


def valtozasok(regi, uj):
    """[(regi_reszlet, uj_reszlet)] szoszintu diffbol, egy szo kornyezettel."""
    a, b = regi.split(' '), uj.split(' ')
    ki = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        ki.append((' '.join(a[i1:i2]), ' '.join(b[j1:j2])))
    return ki


def kapuk_osszesites(eredmenyek):
    """{kapu: Counter(eredmeny)}"""
    ossz = collections.defaultdict(collections.Counter)
    for e in eredmenyek:
        for n, er, _ in e:
            ossz[n][er] += 1
    return ossz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    with open(E.FORDITASOK_UT, encoding='utf-8', newline='') as fh:
        sorok = fh.read().split('\n')
    assert sorok[-1] == ''
    sorok = sorok[:-1]
    ix = {n: i for i, n in enumerate(E.FORDITASOK_FEJLEC)}
    uj_sorok = list(sorok)
    javitasok = []          # (strong, szabaly, regi, uj, f38)
    regi_kapuk, uj_kapuk = [], []
    irt = set()
    szamlalo = collections.Counter()
    for i, s in enumerate(sorok):
        m = s.split('\t')
        if len(m) != 12 or m[0] != 'BDB' or m[3] != 'teljes':
            continue
        szamlalo['BDB teljes'] += 1
        f38 = JEL in m[ix['megjegyzes']]
        sp, forras = E.forras_szoveg(m[1])
        kiv = kivetelek(m[ix['megjegyzes']])
        hu = m[ix['forditas_hu']]
        regi_kapuk.append(K.kapuk_futtat('BDB', forras, hu, bizonytalan=kiv))
        szoveg = hu
        for nev in N.SZABALY_SORREND:
            if 'BDB' not in N.SZABALYOK[nev]:
                continue
            uj, db = N.FUGGVENYEK[nev](szoveg)
            if db:
                for r, u in valtozasok(szoveg, uj):
                    javitasok.append((sp, nev, r, u, f38))
                szoveg = uj
        uj, glossza = N.glossza_visszaallit(forras, szoveg)
        for r, u in glossza:
            javitasok.append((sp, 'glossza_visszaallit', r, u, f38))
        szoveg = uj
        uj_kapuk.append(K.kapuk_futtat('BDB', forras, szoveg, bizonytalan=kiv))
        if f38 and not K.atment(uj_kapuk[-1]):
            raise SystemExit('%s: az uj szoveg nem megy at a gatolo kapukon -- megallok: %s' % (
                sp, [(n, e, r[:200]) for n, e, r in uj_kapuk[-1] if e == 'SERTES']))
        valtozott = szoveg != hu
        megj = m[ix['megjegyzes']]
        if f38:
            if JOVAHAGYAS_REGI in megj:
                megj = megj.replace(JOVAHAGYAS_REGI, JOVAHAGYAS_UJ)
                szamlalo['jovahagyas-jeloles'] += 1
                valtozott = True
            if szoveg != hu and ELOZO_JELOLES not in megj:
                megj = '; '.join(x for x in (megj, JELOLES) if x)
            if valtozott:
                m[ix['forditas_hu']] = szoveg
                m[ix['megjegyzes']] = megj
                uj_sorok[i] = '\t'.join(m)
                irt.add(i)
        szamlalo['valtozott F38' if (f38 and szoveg != hu) else ('valtozna #28' if szoveg != hu else 'valtozatlan')] += 1
    for i, s in enumerate(sorok):
        if i not in irt and uj_sorok[i] != s:
            raise SystemExit('varatlan elteres a %d. sorban -- megallok' % (i + 1))
    # jelentes
    osszes = collections.Counter(r[1] for r in javitasok)
    print('szamlalo:', dict(szamlalo))
    print('javitasok szabalyonkent (db):', dict(collections.Counter(j[1] for j in javitasok)))
    print('javitasok szabalyonkent, F38 / #28:',
          dict(collections.Counter((j[1], 'F38' if j[4] else '#28') for j in javitasok)))
    print('erintett szocikk szabalyonkent:', {k: len({j[0] for j in javitasok if j[1] == k}) for k in
                                              sorted({j[1] for j in javitasok})})
    for nev, cnt in sorted(kapuk_osszesites(regi_kapuk).items()):
        uj_c = kapuk_osszesites(uj_kapuk)[nev]
        print('kapu %-22s elotte %s | utana %s' % (nev, dict(cnt), dict(uj_c)))
    # a 13. kapu (fejezetszam) talalatai: listazas, nem javitas
    print('13. kapu (forrashiba, utana):')
    n13 = 0
    for e, (i, s) in zip(uj_kapuk, [(i, s) for i, s in enumerate(sorok)
                                      if len(s.split('\t')) == 12 and s.split('\t')[0] == 'BDB'
                                      and s.split('\t')[3] == 'teljes']):
        for n, er, r in e:
            if n == '13_fejezetszam' and er == 'JELZES':
                n13 += 1
                print('  %s: %s' % (s.split('\t')[1], r))
    print('13. kapu jelzes: %d szocikk' % n13)
    tsv = ['szocikk\tszabaly\tregi\tuj\tdb\tiras']
    csop = collections.Counter(javitasok)
    for (sp, nev, r, u, f38), db in sorted(csop.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        tsv.append('\t'.join((sp, nev, r, u, str(db), 'igen' if f38 else 'nem (#28 sor)')))
    print('javitas-sor (egyedi): %d' % (len(tsv) - 1))
    print('irando sor: %d' % len(irt))
    if args.ir:
        with open(E.FORDITASOK_UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(uj_sorok) + '\n')
        with open(KIMENET, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(tsv) + '\n')
        print('adat/forditasok.tsv: %d sor irva; %s' % (len(irt), os.path.relpath(KIMENET, REPO)))


if __name__ == '__main__':
    main()
