#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_ujranormalizal.py -- F38, DT-F38 (c): a javitoreteg
(eszkozok/normalizal.py) ujrafuttatasa az adat/forditasok.tsv szotari
`teljes` sorain a Konyv_normalizalo_tabla.tsv `Forrás-alakok` oszlopanak
felvetele utan.

Minden Thayer/BDB `teljes` sort megnez: hol valtoztatna a javitoreteg, es a
kapusor (forditas_kapuk.kapuk_futtat) atmegy-e a regi es az uj szovegen.
Irni (--ir) csak az `opus` allapotu, F38-as (megjegyzes: "F38 BDB_FORDITAS")
sorokat irja: a `forditas_hu` mezot az uj szovegre, a `megjegyzes` vegere egy
jelolest. `kezi` sorhoz nem nyul (brief). Minden mas sor bajtra valtozatlan;
ezt iras elott ellenorzi, elteresnel megall.

    python naplok/BDB_FORDITAS_ujranormalizal.py          # csak jelentes
    python naplok/BDB_FORDITAS_ujranormalizal.py --ir
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
import normalizal as N  # noqa: E402

JELOLES = 'F38.13: javítóréteg újra a könyvalak-leképezés bővítése után (DT-F38 c)'
KIVETEL_ELOTAG = 'terminológia-kivétel (bizonytalan_feloldasok): '


def kivetelek(megj):
    for resz in megj.split('; '):
        if resz.startswith(KIVETEL_ELOTAG):
            return tuple(x.strip() for x in resz[len(KIVETEL_ELOTAG):].split(','))
    return ()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    with open(E.FORDITASOK_UT, encoding='utf-8', newline='') as fh:
        eredeti = fh.read()
    sorok = eredeti.split('\n')
    assert sorok[-1] == ''
    sorok = sorok[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fej_i].split('\t')
    assert fejlec == E.FORDITASOK_FEJLEC, fejlec
    ix = {n: i for i, n in enumerate(fejlec)}
    uj_sorok = list(sorok)
    irt = []
    for i in range(fej_i + 1, len(sorok)):
        m = sorok[i].split('\t')
        if m[ix['szotar']] not in ('Thayer', 'BDB') or m[ix['jelentes_szam']] != 'teljes':
            continue
        hu = m[ix['forditas_hu']]
        uj, valt = N.normalizal(hu, m[ix['szotar']])
        if uj == hu:
            continue
        sp, forras = E.forras_szoveg(m[ix['strong']])
        kiv = kivetelek(m[ix['megjegyzes']])
        regi_e = K.kapuk_futtat(m[ix['szotar']], forras, hu, bizonytalan=kiv)
        uj_e = K.kapuk_futtat(m[ix['szotar']], forras, uj, bizonytalan=kiv)
        f38 = m[ix['allapot']] == 'opus' and 'F38 BDB_FORDITAS' in m[ix['megjegyzes']]
        print('%d. sor %s %s (%s): %s; kapu regi %s, uj %s%s' % (
            i + 1, m[ix['strong']], m[ix['allapot']], 'F38' if f38 else 'nem F38',
            ', '.join('%s=%d' % v for v in valt),
            'ATMENT' if K.atment(regi_e) else 'BUKOTT', 'ATMENT' if K.atment(uj_e) else 'BUKOTT',
            '' if f38 else ' -- NEM irja (nem F38-as opus sor)'))
        for n, e, r in uj_e:
            if e not in ('RENDBEN',) and not n.startswith('6'):
                print('    %-22s %-8s %s' % (n, e, r[:300]))
        if f38:
            if not K.atment(uj_e):
                raise SystemExit('az uj szoveg nem megy at a kapukon -- megallok (%s)' % m[ix['strong']])
            m[ix['forditas_hu']] = uj
            m[ix['megjegyzes']] = '; '.join(x for x in (m[ix['megjegyzes']], JELOLES) if x)
            uj_sorok[i] = '\t'.join(m)
            irt.append(i)
    for i, s in enumerate(sorok):
        if i not in irt and uj_sorok[i] != s:
            raise SystemExit('varatlan elteres a %d. sorban -- megallok' % (i + 1))
    print('irando sor: %d' % len(irt))
    if args.ir and irt:
        with open(E.FORDITASOK_UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(uj_sorok) + '\n')
        print('adat/forditasok.tsv: %d sor irva' % len(irt))


if __name__ == '__main__':
    main()
