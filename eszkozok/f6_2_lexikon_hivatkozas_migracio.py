#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f6_2_lexikon_hivatkozas_migracio.py — F6_BRIEF.md F6.2 tétel a).

A `bdb_entry_id` oszlop csak BDB-re képes; a görög oldalnak nincs helye
benne. Ez a migráció ugyanarra a pozícióra két oszlopot tesz:

    bdb_entry_id  ->  lexikon_szotar, lexikon_entry_id

Ha a régi érték nem üres: lexikon_szotar = "BDB", lexikon_entry_id = a régi
érték. Ha üres: mindkettő üres. Minden más mező, a komment-sorok is,
byte-azonosak maradnak.

I/O — FONTOS: sima split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md
"TSV-olvasás" szakasza; az igazolas_migracio.py mintájára).

Futtatás a repó gyökeréből:
    python eszkozok/f6_2_lexikon_hivatkozas_migracio.py         # szárazon
    python eszkozok/f6_2_lexikon_hivatkozas_migracio.py --ir    # ténylegesen ír
"""

import collections
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')


def main():
    ir = '--ir' in sys.argv

    with io.open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()

    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    vege_ujsor = nyers.endswith(sorveg)
    sorok = nyers.split(sorveg)
    if vege_ujsor:
        sorok = sorok[:-1]

    fejlec_idx = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fejlec_idx].split('\t')

    if 'lexikon_szotar' in fejlec:
        print('A migráció már lefutott (a lexikon_szotar oszlop létezik). Nincs teendő.')
        return 0
    if 'bdb_entry_id' not in fejlec:
        print('HIBA: a bdb_entry_id oszlop nincs a fejlécben.', file=sys.stderr)
        return 1

    i_bdb = fejlec.index('bdb_entry_id')
    uj_fejlec = fejlec[:i_bdb] + ['lexikon_szotar', 'lexikon_entry_id'] + fejlec[i_bdb + 1:]

    hibak = []
    kimenet = list(sorok[:fejlec_idx])
    kimenet.append('\t'.join(uj_fejlec))
    szamlalo = collections.Counter()
    entry_id_ertekkeszlet = collections.Counter()

    for sorszam, nyers_sor in enumerate(sorok[fejlec_idx + 1:], start=fejlec_idx + 2):
        if not nyers_sor.strip():
            kimenet.append(nyers_sor)
            continue
        if nyers_sor.startswith('#'):
            kimenet.append(nyers_sor)
            continue

        mezok = nyers_sor.split('\t')
        if len(mezok) != len(fejlec):
            hibak.append('%d. sor: %d oszlop %d helyett' % (sorszam, len(mezok), len(fejlec)))
            continue

        regi_ertek = mezok[i_bdb]
        if regi_ertek:
            lexikon_szotar, lexikon_entry_id = 'BDB', regi_ertek
            szamlalo['BDB'] += 1
            entry_id_ertekkeszlet[regi_ertek] += 1
        else:
            lexikon_szotar, lexikon_entry_id = '', ''
            szamlalo['ures'] += 1

        uj_mezok = mezok[:i_bdb] + [lexikon_szotar, lexikon_entry_id] + mezok[i_bdb + 1:]
        kimenet.append('\t'.join(uj_mezok))

    print('Sorok: %d' % (len(sorok) - fejlec_idx - 1))
    print('  lexikon_szotar=BDB: %d' % szamlalo['BDB'])
    print('  üres: %d' % szamlalo['ures'])
    print('  lexikon_entry_id értékkészlet:', dict(entry_id_ertekkeszlet))

    if hibak:
        print('\nHIBA (%d) — nem írtam semmit:' % len(hibak))
        for h in hibak[:20]:
            print('  ' + h)
        return 1

    # bájthűség-próba: az érintett oszlopon kívül minden mezőnek azonosnak kell lennie
    ellenorzott = 0
    for eredeti, uj in zip(sorok[fejlec_idx + 1:], kimenet[fejlec_idx + 1:]):
        if not eredeti.strip() or eredeti.startswith('#'):
            continue
        a = eredeti.split('\t')
        b = uj.split('\t')
        # b-ben egy oszloppal tobb van; az i_bdb pozíció előtti/utáni részt vetjük össze
        b_elotte = b[:i_bdb]
        b_lexikon_szotar = b[i_bdb]
        b_lexikon_entry_id = b[i_bdb + 1]
        b_utana = b[i_bdb + 2:]

        a_elotte = a[:i_bdb]
        a_regi = a[i_bdb]
        a_utana = a[i_bdb + 1:]

        if a_elotte != b_elotte:
            hibak.append('%d. sor: bájthűség sérült a bdb_entry_id előtti mezőkben' % (sorok.index(eredeti) + 1))
        if a_utana != b_utana:
            hibak.append('%d. sor: bájthűség sérült a bdb_entry_id utáni mezőkben' % (sorok.index(eredeti) + 1))
        if a_regi:
            if b_lexikon_szotar != 'BDB' or b_lexikon_entry_id != a_regi:
                hibak.append('%d. sor: lexikon_szotar/entry_id nem egyezik a régi bdb_entry_id-vel' % (sorok.index(eredeti) + 1))
        else:
            if b_lexikon_szotar != '' or b_lexikon_entry_id != '':
                hibak.append('%d. sor: lexikon_szotar/entry_id nem üres, holott a régi bdb_entry_id üres volt' % (sorok.index(eredeti) + 1))
        ellenorzott += 1

    if hibak:
        print('\nHIBA — nem írtam semmit:')
        for h in hibak[:20]:
            print('  ' + h)
        return 1

    print('\nHiba nincs. Bájthűség ellenőrizve %d soron.' % ellenorzott)
    if not ir:
        print('Szárazon futott. Tényleges íráshoz: --ir')
        return 0

    with io.open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(kimenet) + (sorveg if vege_ujsor else ''))
    print('Megírva: adat/elofordulasok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
