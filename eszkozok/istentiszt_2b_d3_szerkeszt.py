#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
istentiszt_2b_d3_szerkeszt.py -- ISTENTISZT_2B_ADATOSITAS.md D3 tetel,
2. resz: a "#### 4. TELJES TBESG (Abbott-Smith) szocikkek" blokk (G1941/
G2564/G0994 TBESG+Thayer idezetei, mar adatban) torlese, es a ket
"#####"-szintu alcim (Kiegeszito adatok..., A heber oldal kiegeszito
adatai...) "####"-re emelese, mivel a szulo #### 4 cim torlodik.

Sor-index alapon dolgozik (nem string-illesztessel), hogy elkerulje a
hebe/gorog kombinalo diakritikus jelek kezi ujragepeleset.

Futtatas a repo gyokerebol:
    python eszkozok/istentiszt_2b_d3_szerkeszt.py
"""

import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLDAL_FAJL = os.path.join(ROOT, 'lexikon', 'ISTENTISZT-001_TUDOMANYOS.md')


def main():
    with io.open(OLDAL_FAJL, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')

    kezdet_cimke = '#### 4. TELJES TBESG (Abbott-Smith) szócikkek — a három görög ige'
    veg_cimke = '##### Kiegészítő adatok: MCGED (Mounce), SECE (Louw-Nida) és LSJ'
    elozo_elvalaszto = '---'

    kezdet_idx = next(i for i, s in enumerate(sorok) if s == kezdet_cimke)
    veg_idx = next(i for i, s in enumerate(sorok) if s == veg_cimke)

    # A blokk elott allo elvalaszto ("---") es az azt megelozo ures sor is torlendo.
    torles_kezdet = kezdet_idx
    if sorok[kezdet_idx - 1] == '' and sorok[kezdet_idx - 2] == elozo_elvalaszto:
        torles_kezdet = kezdet_idx - 2

    uj_sorok = sorok[:torles_kezdet] + ['#### Kiegészítő adatok: MCGED (Mounce), SECE (Louw-Nida) és LSJ'] + sorok[veg_idx + 1:]

    szoveg = '\n'.join(uj_sorok)
    # A masodik ##### alcim (A heber oldal kiegeszito adatai) is #### -re emelkedik.
    regi = '##### A héber oldal kiegészítő adatai (TBESH-konszolidáció + SECE)'
    uj = '#### A héber oldal kiegészítő adatai (TBESH-konszolidáció + SECE)'
    if regi not in szoveg:
        raise ValueError('nincs ilyen alcim: %r' % regi)
    szoveg = szoveg.replace(regi, uj, 1)

    with io.open(OLDAL_FAJL, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)

    print('Törölve: %d -> %d sor közötti blokk (%d sor).' % (torles_kezdet, veg_idx, veg_idx - torles_kezdet + 1))
    print('Kész.')


if __name__ == '__main__':
    main()
