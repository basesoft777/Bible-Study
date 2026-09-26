#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P4_vak_epit_kor2.py -- a 2. modellkor (m1-m6, l. FORDITAS_P_jelentes_kor2.md)
vak biralati csomagja. A FORDITAS_P4_vak_epit.py mintajara, DE kulon
kimeneti fajlokba ir, hogy az eredeti (3 modelles, a brief FP4 tetelehez
tartozo) FORDITAS_P4_vak.md/FORDITAS_P4_vak_kulcs.tsv valtozatlan maradjon.

Kimenet:
  naplok/FORDITAS_P4_vak_kor2.md        -- mind a 20 szocikk, akar 6 cimzett
                                            forditassal (A-F), szocikkenkent
                                            veletlen sorrendben, rogzitett
                                            maggal; a modellnev nem szerepel.
  naplok/FORDITAS_P4_vak_kulcs_kor2.tsv -- strong, cimke, modell -- KULON
                                            fajlban.

    python naplok/FORDITAS_P4_vak_epit_kor2.py
"""

import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLOK = os.path.join(REPO, 'naplok')
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import fordit  # noqa: E402

VELETLEN_MAG = 20260926  # ugyanaz a rogzitett mag, mint az 1. korben

VAK_UT = os.path.join(NAPLOK, 'FORDITAS_P4_vak_kor2.md')
KULCS_UT = os.path.join(NAPLOK, 'FORDITAS_P4_vak_kulcs_kor2.tsv')

CIMKEK = ['A', 'B', 'C', 'D', 'E', 'F']


def betolt():
    minta = fordit.minta_betolt()
    thayer = fordit.thayer_betolt()
    kimenet = list(fordit.tsv_dict_sorok(fordit.KIMENET_UT))
    return minta, thayer, kimenet


def szocikk_forditasai(strong, kimenet):
    """strong -> [(modell, forditas), ...] csak a sikeres (nem HIBA:) sorok."""
    talalt = []
    for r in kimenet:
        if r['strong'] != strong:
            continue
        if r['forditas_hu'].startswith('HIBA:'):
            continue
        talalt.append((r['modell'], r['forditas_hu']))
    return talalt


def main():
    minta, thayer, kimenet = betolt()
    rng = random.Random(VELETLEN_MAG)

    kulcs_sorok = []
    minden_szocikk_info = []

    for sor in sorted(minta, key=lambda s: s['strong']):
        strong = sor['strong']
        forditasok = szocikk_forditasai(strong, kimenet)
        rng.shuffle(forditasok)
        if len(forditasok) > len(CIMKEK):
            raise SystemExit('tobb sikeres forditas (%d), mint cimke (%d) -- '
                              'bovitsd a CIMKEK listat' % (len(forditasok), len(CIMKEK)))
        cimzett = list(zip(CIMKEK, forditasok))

        osszes_modell = {r['modell'] for r in kimenet if r['strong'] == strong}
        van_modell = {m for m, _ in forditasok}
        hianyzo = sorted(osszes_modell - van_modell)

        info = []
        for cimke, (modell, forditas) in cimzett:
            info.append((cimke, modell, forditas))
            kulcs_sorok.append({'strong': strong, 'cimke': cimke, 'modell': modell})
        minden_szocikk_info.append((strong, sor['csoport'], info, hianyzo))

    resz = []
    resz.append('# FORDITAS_P4_vak_kor2 -- vak forditas-osszehasonlitas (2. modellkor, 6 modell)\n')
    resz.append('*A modellek neve rejtve (A-F); a cimkezes szocikkenkent veletlen, '
                 'rogzitett maggal (%d). A kulcs KULON fajlban: `FORDITAS_P4_vak_kulcs_kor2.tsv`.*\n'
                 % VELETLEN_MAG)
    for strong, csoport, info, hianyzo in minden_szocikk_info:
        forras = thayer.get(strong, {}).get('Teljes_szocikk', '(nincs forras)')
        resz.append('\n---\n\n## %s (csoport: %s)\n' % (strong, csoport))
        resz.append('**Forrás (Thayer, angol):**\n\n> %s\n' % forras.replace('\n', '\n> '))
        for cimke, modell, forditas in info:
            resz.append('\n**%s fordítása:**\n\n%s\n' % (cimke, forditas))
        if hianyzo:
            resz.append('\n*(%d modell kimarad -- a hívás nem hozott érvényes fordítást, '
                         'l. `FORDITAS_P_jelentes.md`.)*\n' % len(hianyzo))
    with open(VAK_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(''.join(resz))
    print('irva:', VAK_UT)

    fordit.tsv_ir(KULCS_UT, ['strong', 'cimke', 'modell'], kulcs_sorok)
    print('irva:', KULCS_UT, '(%d sor)' % len(kulcs_sorok))


if __name__ == '__main__':
    main()
