#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P4_vak_epit.py -- FORDITAS_PILOT_BRIEF.md v1, FP4: a vak biralati
csomag es a felhasznaloi minta elokeszitese.

Kimenet:
  naplok/FORDITAS_P4_vak.md            -- mind a 20 szocikk: forras + a
                                           sikeresen leforditott modellek
                                           valasza X/Y/Z cimkevel, cimkezes
                                           szocikkenkent veletlen (rogzitett
                                           maggal); a nev nem szerepel.
  naplok/FORDITAS_P4_vak_kulcs.tsv     -- strong, cimke, modell -- KULON
                                           fajlban, az FP5 alatt nem
                                           nyitando meg (l. a brief FP5 tetele).
  naplok/FORDITAS_P4_minta_felhasznalo.md -- 5, veletlenul (rogzitett maggal)
                                           kivalasztott szocikk vakon,
                                           kitoltendo pontozotablaval (SS1).

    python naplok/FORDITAS_P4_vak_epit.py
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

VELETLEN_MAG = 20260926  # rogzitett mag -- a brief SS1 "rogzitett maggal" kovetelmenye
FELHASZNALOI_MINTA_DB = 5

VAK_UT = os.path.join(NAPLOK, 'FORDITAS_P4_vak.md')
KULCS_UT = os.path.join(NAPLOK, 'FORDITAS_P4_vak_kulcs.tsv')
FELHASZNALOI_UT = os.path.join(NAPLOK, 'FORDITAS_P4_minta_felhasznalo.md')

CIMKEK = ['X', 'Y', 'Z']


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

    vak_szakaszok = []
    kulcs_sorok = []
    minden_szocikk_info = []  # (strong, csoport, [(cimke, modell, forditas), ...], hianyzo_modellek)

    for sor in sorted(minta, key=lambda s: s['strong']):
        strong = sor['strong']
        forditasok = szocikk_forditasai(strong, kimenet)
        rng.shuffle(forditasok)  # szocikkenkent kulon veletlen sorrend
        cimzett = list(zip(CIMKEK, forditasok))  # [(cimke, (modell, forditas)), ...]

        osszes_modell = {r['modell'] for r in kimenet if r['strong'] == strong}
        van_modell = {m for m, _ in forditasok}
        hianyzo = sorted(osszes_modell - van_modell)

        info = []
        for cimke, (modell, forditas) in cimzett:
            info.append((cimke, modell, forditas))
            kulcs_sorok.append({'strong': strong, 'cimke': cimke, 'modell': modell})
        minden_szocikk_info.append((strong, sor['csoport'], info, hianyzo))

    # --- FORDITAS_P4_vak.md ---
    resz = []
    resz.append('# FORDITAS_P4_vak -- vak forditas-osszehasonlitas (FP5 bemenete)\n')
    resz.append('*A modellek neve rejtve (X/Y/Z); a cimkezes szocikkenkent veletlen, '
                 'rogzitett maggal (%d). A kulcs KULON fajlban: `FORDITAS_P4_vak_kulcs.tsv` '
                 '-- az FP5 alatt ne nyisd meg.*\n' % VELETLEN_MAG)
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

    # --- FORDITAS_P4_minta_felhasznalo.md -- 5 veletlen szocikk, kitoltendo tablaval ---
    strongok = [s['strong'] for s in minta]
    rng2 = random.Random(VELETLEN_MAG)  # kulon, de ugyanattol a rogzitett magtol induló sorozat
    minta5 = rng2.sample(sorted(strongok), FELHASZNALOI_MINTA_DB)

    info_map = {strong: (csoport, info) for strong, csoport, info, _ in minden_szocikk_info}

    resz2 = []
    resz2.append('# FORDITAS_P4_minta_felhasznalo -- felhasználói vak pontozás (5 szócikk)\n')
    resz2.append('*Ugyanaz a vak elrendezés, mint a `FORDITAS_P4_vak.md`-ben -- a modellek '
                  'neve itt sincs feltüntetve. Rögzített mag: %d, kiválasztott szócikkek: %s.*\n'
                  % (VELETLEN_MAG, ', '.join(minta5)))
    resz2.append('\n**Pontozás szócikkenként, X/Y/Z-nként (10 pont, a brief SS1 szerint):**\n')
    resz2.append('- pontosság 0-3 (kihagyás, betoldás, félreértés)\n')
    resz2.append('- terminológia 0-2\n')
    resz2.append('- magyar nyelvhelyesség 0-3\n')
    resz2.append('- formai szabályok 0-2\n')

    for strong in minta5:
        csoport, info = info_map[strong]
        forras = thayer.get(strong, {}).get('Teljes_szocikk', '(nincs forras)')
        resz2.append('\n---\n\n## %s (csoport: %s)\n' % (strong, csoport))
        resz2.append('**Forrás (Thayer, angol):**\n\n> %s\n' % forras.replace('\n', '\n> '))
        for cimke, modell, forditas in info:
            resz2.append('\n**%s fordítása:**\n\n%s\n' % (cimke, forditas))
            resz2.append('\n| Szempont | Pont |\n|---|---|\n'
                          '| pontosság (0-3) | |\n| terminológia (0-2) | |\n'
                          '| magyar nyelvhelyesség (0-3) | |\n| formai szabályok (0-2) | |\n'
                          '| **összesen (0-10)** | |\n')
    with open(FELHASZNALOI_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(''.join(resz2))
    print('irva:', FELHASZNALOI_UT, '(%d szocikk)' % len(minta5))


if __name__ == '__main__':
    main()
