#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kuszob.py -- F8.4: a B1 kuszobfigyelo onallo eszkoze (F8_BRIEF.md G5).

A fo elofordulas-szamlalast a general.py adja (fo_elofordulas_csoportok);
ez a szkript CSAK a kuszob-osszevetest es a kilepesi kodot teszi hozza --
a general.py naploblokkja (render_naplo_kuszob) nem valtozik.

Atlepes = fo elofordulas >= 3 ES ures `forras_study`. A `forras_study` azt
meri, amit a B1 kerdez (van-e mar tematikus study) -- egy motivumnak lehet
harom vagy tobb fo elofordulasa ugy is, hogy mar van study-ja: az nem
atlepes, csak egy mar feldolgozott motivum.

CLI:
    python eszkozok/kuszob.py [--adat DIR] [--md FILE]

Kilepesi kod: 0 = nincs atlepes, 1 = van atlepes, 2 = hiba.
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')


def kuszob_sorok(adat_dir):
    """[{id, cim, n_fo, forras_study_kitoltott, atlepes}] -- id szerint rendezve."""
    _, motivumok = G.tsv_beolvas(os.path.join(adat_dir, 'motivumok.tsv'))
    _, elofordulasok = G.tsv_beolvas(os.path.join(adat_dir, 'elofordulasok.tsv'))
    elof_id_szerint = G.elofordulasok_id_szerint(elofordulasok)

    sorok = []
    for m in sorted(motivumok, key=lambda r: r['id']):
        sorai = elof_id_szerint.get(m['id'], [])
        n_fo = len(G.fo_elofordulas_csoportok(sorai))
        forras_study = (m.get('forras_study') or '').strip()
        kitoltott = bool(forras_study)
        atlepes = n_fo >= 3 and not kitoltott
        sorok.append({
            'id': m['id'],
            'cim': m.get('cim') or '',
            'n_fo': n_fo,
            'forras_study_kitoltott': kitoltott,
            'atlepes': atlepes,
        })
    return sorok


def jelentes_szoveg(sorok):
    n_atlepes = sum(1 for s in sorok if s['atlepes'])
    sorlista = ['# Kuszobfigyelo (B1) -- eszkozok/kuszob.py', '',
                'Atlepes = fo elofordulas >= 3 ES ures `forras_study`.', '',
                '| Motivum-ID | Cim | Fo elofordulas | forras_study | Atlepes |',
                '|---|---|---|---|---|']
    for s in sorok:
        sorlista.append('| %s | %s | %d | %s | %s |' % (
            s['id'], s['cim'], s['n_fo'],
            'kitöltött' if s['forras_study_kitoltott'] else 'üres',
            'igen' if s['atlepes'] else 'nem'))
    sorlista.append('')
    sorlista.append('Összesen %d ID; %d átlépés.' % (len(sorok), n_atlepes))
    return '\n'.join(sorlista) + '\n'


def main():
    parser = argparse.ArgumentParser(description='F8.4 -- B1 kuszobfigyelo')
    parser.add_argument('--adat', default=ALAPERTELMEZETT_ADAT,
                         help='az adat/ konyvtar (alapertelmezes: a repo adat/-ja)')
    parser.add_argument('--md', default=None, help='a jelentes Markdown fajlba is')
    args = parser.parse_args()

    try:
        sorok = kuszob_sorok(args.adat)
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    szoveg = jelentes_szoveg(sorok)
    print(szoveg)

    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)

    sys.exit(1 if any(s['atlepes'] for s in sorok) else 0)


if __name__ == '__main__':
    main()
