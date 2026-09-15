#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f46a_nyitott_atx_fejlecek.py -- F4.6a: a NYITOTT_FELADATOK.md ATX-fejlecei.

A fajlban ma EGYETLEN `#` sincs: a szakaszcimek csupasz szovegsorkent allnak.
Ez a G6 blokk elott javitando, kulonben a generalt blokk fejlece lenne az
egyetlen ATX-fejlec a fajlban -- egy generalt sor rangsorolna fole az egesz
kezi dokumentumot.

A szkript KIZAROLAG prefixet tesz a mar meglevo sorok ele (`# `, `## `,
`### `); egyetlen sor szovege sem valtozik, sor nem kerul be es nem tunik el
-- kiveve a blokk-horgony szakaszat, amely a lista vegere, a "Lezárva" ele
kerul (uj sorok, jelezve).

Futtatas a repo gyokerebol:
    python eszkozok/f46a_nyitott_atx_fejlecek.py           # proba
    python eszkozok/f46a_nyitott_atx_fejlecek.py --ir      # ir
"""

import argparse
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NYITOTT_MD = os.path.join(ROOT, 'NYITOTT_FELADATOK.md')

# (pontos sorszoveg, szint). Pontos egyezes, nem prefix -- es mindegyiknek
# EGYETLEN talalata lehet, kulonben megallas.
FEJLECEK = [
    ('Nyitott feladatok', 1),
    ('Nagy, tartalmi döntést igénylő tételek', 2),
    ('Kisebb, korábbról nyitva maradt tételek', 2),
    ('Migrálva a döntési fájl 8. szakaszából (F1.6, 2026.09.13)', 2),
    ('Lezárva', 2),
    ('2026.09.09-10 (chat-munkamenet, harmadik szakasz):', 3),
    ('2026.09.09 (chat-munkamenet, második szakasz):', 3),
    ('2026.09.09 (chat-munkamenet, első szakasz):', 3),
    ('2026.09.08 (chat-ellenőrzés):', 3),
    ('2026.09.07 (második folytatás):', 3),
    ('2026.09.07 (folytatólagos szakasz):', 3),
    ('2026.09.07 (korábbi szakasz):', 3),
]

# A generalt blokk horgonya -- ugyanaz a minta, mint az index-nel
# (general.py HORGONY). A "Lezárva" fejlec ELE kerul: a generalt tabla a
# nyitott tetelek koze tartozik, nem a lezartak koze.
HORGONY_SZAKASZ = [
    '## Adattáblából generált — nyitott jelöltek és motívum-státuszok',
    '',
    '<!-- A GENERÁLT BLOKK HELYE: nyitott -->',
    '',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()

    with io.open(NYITOTT_MD, encoding='utf-8', newline='') as fh:
        nyers = fh.read()
    crlf = nyers.count('\r\n')
    lf = nyers.count('\n') - crlf
    sorveg = '\r\n' if crlf > lf else '\n'
    print('sorvég: CRLF=%d, LF=%d -> domináns=%r' % (crlf, lf, sorveg))
    sorok = nyers.replace('\r\n', '\n').split('\n')

    if any(s.startswith('#') for s in sorok):
        print('MEGALLAS: a fájlban már van ATX-fejléc -- a szkript egyszer fut.')
        return 1

    hibak = []
    for szoveg, szint in FEJLECEK:
        n = sorok.count(szoveg)
        if n != 1:
            hibak.append('%r: %d találat (1 kell)' % (szoveg, n))
    if sorok.count(HORGONY_SZAKASZ[2]) != 0:
        hibak.append('a horgony már benne van')
    if hibak:
        print('MEGALLAS -- %d hiba:' % len(hibak))
        for h in hibak:
            print('  ' + h)
        return 1

    szint_szerint = dict(FEJLECEK)
    uj = []
    n_fejlec = 0
    for sor in sorok:
        if sor == 'Lezárva':
            uj.extend(HORGONY_SZAKASZ)
        if sor in szint_szerint:
            uj.append('#' * szint_szerint[sor] + ' ' + sor)
            n_fejlec += 1
            print('  %s%s' % ('#' * szint_szerint[sor] + ' ', sor))
            continue
        uj.append(sor)

    # Igazolas: a fejlec-sorokon kivul minden sor karakterre valtozatlan, es a
    # sorok sorrendje is -- a horgony-szakasz negy uj sorat leszamitva.
    ellenorzo = [s for s in uj if s not in HORGONY_SZAKASZ or s == '']
    # ures sor a horgonybol: pontos szamlalas helyett a fejlec-eltavolitassal
    # igazolunk
    vissza = []
    beszurva = 0
    i = 0
    while i < len(uj):
        if uj[i:i + len(HORGONY_SZAKASZ)] == HORGONY_SZAKASZ:
            i += len(HORGONY_SZAKASZ)
            beszurva += 1
            continue
        s = uj[i]
        if s.startswith('#'):
            s = s.lstrip('#').lstrip(' ')
        vissza.append(s)
        i += 1
    if beszurva != 1:
        print('MEGALLAS: a horgony-szakasz %d helyen illeszkedik.' % beszurva)
        return 1
    if vissza != sorok:
        for k, (a, b) in enumerate(zip(sorok, vissza), start=1):
            if a != b:
                print('MEGALLAS: %d. sor eltér: %r -> %r' % (k, a, b))
                return 1
        print('MEGALLAS: sorszám eltér (%d -> %d)' % (len(sorok), len(vissza)))
        return 1

    print('')
    print('%d fejléc, +%d sor a horgony-szakaszból, %d -> %d sor.'
          % (n_fejlec, len(HORGONY_SZAKASZ), len(sorok), len(uj)))

    if not args.ir:
        print('(proba -- nem irt)')
        return 0

    with io.open(NYITOTT_MD, 'w', encoding='utf-8', newline='') as fh:
        fh.write(sorveg.join(uj))
    with io.open(NYITOTT_MD, encoding='utf-8', newline='') as fh:
        if fh.read().replace('\r\n', '\n').split('\n') != uj:
            print('MEGALLAS: visszaolvasási eltérés.')
            return 1
    print('Kiírva és visszaolvasva: %s' % os.path.relpath(NYITOTT_MD, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
