#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
k16_archiv_jeloles.py -- F4 K16 / D15: a forrasreteg archiv szakaszainak jelolese.

A het `motivumok/[ID].md`-ben harom szakasz tartalmat a D13 ota a GENERALT
blokk birtokolja (elofordulas-szam, statusz-cimke, index-sorszam). Ezek a
szakaszok a forrasretegben archiv szovegkent maradnak -- az ertekuk a
proveniencia, nem az allitas. A K16 ezert a FEJLECEKET jeloli meg; a szakaszok
SZOVEGE karakterre valtozatlan marad (az ALVIL-001 "4 elofordulas"-at sem
javitjuk, csak megjeloljuk).

    ## Tematikus áttekintés — a napló mai tétele          -> jelolendo
    ## Kulcsszó-index — a napló mai sora                  -> jelolendo
    ## Lezárt tanulmányok indexe — ...                    -> mar jelolt (F4.4)

A szkript idempotens: mar megjelolt fejlecet nem jelol ujra.

Ellenorzes (K16): a fajl a ket fejlec-sor kivetelevel karakterre valtozatlan.
Eltereskor a szkript MEGALL es nem ir (l. CLAUDE.md, tablat iro szkript).

Futtatas a repo gyokerebol:
    python eszkozok/k16_archiv_jeloles.py            # proba (nem ir)
    python eszkozok/k16_archiv_jeloles.py --ir       # ir
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTIVUMOK_DIR = os.path.join(ROOT, 'motivumok')

JELOLES = ('*(archív — a 2026-09-15-i kivonás előtti szöveg; '
           'a mérvadó érték a generált blokkban áll)*')

# Pontos fejlec-sorok, nem prefix-illesztes: a "Lezárt tanulmányok indexe"
# fejlec mar sajat *(archív: ...)* jelolest hordoz az F4.4-bol, azt nem irjuk at.
JELOLENDO_FEJLECEK = [
    '## Tematikus áttekintés — a napló mai tétele',
    '## Kulcsszó-index — a napló mai sora',
]

# K16 masodik fele kodban: a beolvasztas (F6 / a ⭐-proza befuzese a naplo
# generalt blokkjaba) kizarolag ezt a ket szakaszt olvashatja a forrasretegbol.
# L. eszkozok/general.py BEOLVASZTHATO_SZAKASZOK.


def fajlok():
    return sorted(f for f in os.listdir(MOTIVUMOK_DIR) if f.endswith('.md'))


def feldolgoz(szoveg, fajlnev):
    """Visszaad (uj_szoveg, jelolt_fejlecek, mar_jelolt_fejlecek)."""
    sorok = szoveg.split('\n')
    jelolt = []
    mar_jelolt = []
    for i, sor in enumerate(sorok):
        for fejlec in JELOLENDO_FEJLECEK:
            if sor == fejlec:
                sorok[i] = fejlec + ' ' + JELOLES
                jelolt.append(fejlec)
            elif sor == fejlec + ' ' + JELOLES:
                mar_jelolt.append(fejlec)
    return '\n'.join(sorok), jelolt, mar_jelolt


def igazol(regi, uj, fajlnev):
    """A ket szoveg a megjelolt fejlec-sorokon kivul karakterre azonos legyen."""
    r = regi.split('\n')
    u = uj.split('\n')
    if len(r) != len(u):
        return ['%s: sorszam valtozott (%d -> %d)' % (fajlnev, len(r), len(u))]
    hibak = []
    for i, (a, b) in enumerate(zip(r, u), start=1):
        if a == b:
            continue
        if a in JELOLENDO_FEJLECEK and b == a + ' ' + JELOLES:
            continue
        hibak.append('%s:%d: nem fejlec-sor valtozott meg: %r -> %r'
                     % (fajlnev, i, a, b))
    return hibak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true',
                    help='tenylegesen ir; nelkule csak probal')
    args = ap.parse_args()

    osszes_hiba = []
    osszes_jelolt = 0
    osszes_mar = 0
    valtozo = []

    for fajlnev in fajlok():
        ut = os.path.join(MOTIVUMOK_DIR, fajlnev)
        with io_open(ut) as fh:
            regi = fh.read()
        uj, jelolt, mar_jelolt = feldolgoz(regi, fajlnev)
        hibak = igazol(regi, uj, fajlnev)
        osszes_hiba.extend(hibak)
        osszes_jelolt += len(jelolt)
        osszes_mar += len(mar_jelolt)
        jelzo = 'JELOL %d, mar jelolt %d' % (len(jelolt), len(mar_jelolt))
        print('%-24s %s' % (fajlnev, jelzo))
        for f in JELOLENDO_FEJLECEK:
            if f not in jelolt and f not in mar_jelolt:
                osszes_hiba.append('%s: hianyzo fejlec: %s' % (fajlnev, f))
        if uj != regi:
            valtozo.append((ut, uj))

    print('')
    print('Osszesen: %d fejlec jelolve, %d mar jelolt volt, %d fajl valtozik.'
          % (osszes_jelolt, osszes_mar, len(valtozo)))

    if osszes_hiba:
        print('')
        print('MEGALLAS -- %d hiba:' % len(osszes_hiba))
        for h in osszes_hiba:
            print('  ' + h)
        return 1

    if not args.ir:
        print('(proba -- nem irt; --ir kell az iráshoz)')
        return 0

    for ut, uj in valtozo:
        with io_open(ut, 'w') as fh:
            fh.write(uj)
    # visszaolvasas
    for ut, uj in valtozo:
        with io_open(ut) as fh:
            if fh.read() != uj:
                print('MEGALLAS -- visszaolvasasi elteres: %s' % ut)
                return 1
    print('Kiirva es visszaolvasva: %d fajl.' % len(valtozo))
    return 0


def io_open(ut, mod='r'):
    import io
    return io.open(ut, mod, encoding='utf-8', newline='')


if __name__ == '__main__':
    sys.exit(main())
