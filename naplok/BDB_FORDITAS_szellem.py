#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_szellem.py -- F38 zaromenet (DT25, DT-F38e): az isteni
szellem nagybetus: „Szent Szellem”, „Isten Szelleme”, „a Szellem”. Az emberi
szellem kisbetus marad.

A lista kezi atnezes eredmenye (a 269 BDB-szocikk osszes `szellem*` helye
atnezve; a H7307-tel kezdve): minden bejegyzes (strong, pont, regi, uj) egy
egyedi reszlet cserejet irja le. A script minden csere elott ellenorzi, hogy
a `regi` reszlet a sor fordításában pontosan egyszer all; elteresnel megall.

Csak az `F38 BDB_FORDITAS` megjegyzesu sorokat irja (a #28 kezi/opus sorai
nem valtoznak, ott a talalat csak listazva van: KIHAGYOTT_28).

    python naplok/BDB_FORDITAS_szellem.py            # csak jelentes
    python naplok/BDB_FORDITAS_szellem.py --ir
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

UT = E.FORDITASOK_UT
JELOLES = 'F38.268: az isteni Szellem nagybetűs (DT25)'

# (strong, pont, regi, uj, indok)
SZELLEM = [
    ('H7307', '3d', 'Di Bu: isteni szellem, vö. 32:8', 'Di Bu: isteni Szellem, vö. 32:8',
     'Jób 32:18 — Di és Bu szerint az isteni szellem (vö. Jób 32:8)'),
    ('H7307', '4c', 'c. ezért Isten szelleme: 1Móz 6:3', 'c. ezért Isten Szelleme: 1Móz 6:3',
     '„Isten szelleme”'),
    ('H7307', '6 (hivatkozás a 9b pontra)', 'de valószínűleg prófétai szellem, 9b)',
     'de valószínűleg prófétai Szellem, 9b)',
     'Ézs 59:21 — a 9b pont szerinti, a prófétákat tanításra indító (isteni) Szellem'),
    ('H7307', '9a', 'akit az eksztatikus állapotban a szellem megragadott',
     'akit az eksztatikus állapotban a Szellem megragadott',
     'Hós 9:7 — az eksztatikus állapotot ihlető isteni Szellem (a 9. pont: Isten Szelleme)'),
    ('H7307', '9b', 'b. a szellem mint a prófétákat tanítás vagy intés kimondására',
     'b. a Szellem mint a prófétákat tanítás vagy intés kimondására',
     'a 9. pont (Isten Szelleme) b. alpontja'),
    ('H7307', '9f', 'úgy fogják fel az isteni szellemet,', 'úgy fogják fel az isteni Szellemet,',
     '„isteni szellem”'),
    ('H5307', '(Ez 11:5)', 'a ׳י szelleme 11:5', 'a ׳י Szelleme 11:5',
     'Ez 11:5 — Jahve Szelleme'),
    ('H5414', '(Ézs 42:1)', 'szellememet adom rá Ézs 42:1', 'Szellememet adom rá Ézs 42:1',
     'Ézs 42:1 — Isten első személyű beszéde: „az én Szellemem”'),
    ('H3947', '(Ez 3:14)', 'Ez 3:14 a szellem felemelt', 'Ez 3:14 a Szellem felemelt',
     'Ez 3:14 — Jahve Szelleme (a 7307 9a pontja: Ezékielre vonatkozóan Ez 3:12, 14)'),
    ('H7760', '(4Móz 11:17)', 'átvitt értelemben szellemet (עַל) 4Móz 11:17',
     'átvitt értelemben Szellemet (עַל) 4Móz 11:17',
     '4Móz 11:17 — Isten Szelleme (a H7307 9a pontja is ide sorolja)'),
]

# Kozmetikai, nem modositott, de a felhasznalo dontesere vart helyek
# (a szellem istenre vonatkozasa nem egyertelmu, vagy a sor nem F38-as)
NEM_MODOSITOTT = [
    ('H4390', '2Móz 28:3; 31:3; 35:31', 'szellemmel betölteni',
     '31:3 isteni Szellem (Becalél), 28:3 viszont „a bölcsesség szelleme”; BDB nem dönt'),
    ('H1320', 'Ézs 31:3', 'a lovak hús, nem szellem',
     'a hús–szellem szembeállítás; nem egyértelműen Isten Szelleme'),
    ('H5674', '4Móz 5:14', 'a szellemről',
     'a féltékenység szelleme (קנאה רוח), nem isteni'),
    ('H7451', '2Sám 13:22 körül', 'az isteni szellemről, amely az őrjöngés és az erőszak eksztatikus állapotát',
     'a #28 sor (nem F38-as), a menet nem módosítja; ha kell: „az isteni Szellemről”'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    with open(UT, encoding='utf-8', newline='') as fh:
        sorok = fh.read().split('\n')
    assert sorok[-1] == ''
    sorok = sorok[:-1]
    ix = {n: i for i, n in enumerate(E.FORDITASOK_FEJLEC)}
    index = {}
    for i, s in enumerate(sorok):
        m = s.split('\t')
        if len(m) == 12 and m[0] == 'BDB' and m[3] == 'teljes':
            index[m[1]] = i
    irt = set()
    for strong, pont, regi, uj, indok in SZELLEM:
        sp = E.strong_padded(strong)
        i = index[sp]
        m = sorok[i].split('\t')
        if 'F38 BDB_FORDITAS' not in m[ix['megjegyzes']]:
            raise SystemExit('nem F38-as sor: %s' % sp)
        db = m[ix['forditas_hu']].count(regi)
        if db != 1:
            raise SystemExit('%s %s: a reszlet %d-szer all (1 kell): %s' % (sp, pont, db, regi))
        m[ix['forditas_hu']] = m[ix['forditas_hu']].replace(regi, uj)
        if JELOLES not in m[ix['megjegyzes']]:
            m[ix['megjegyzes']] = '; '.join(x for x in (m[ix['megjegyzes']], JELOLES) if x)
        sorok[i] = '\t'.join(m)
        irt.add(i)
        print('%s | %s | %s => %s' % (sp, pont, regi, uj))
    print('csere: %d, sor: %d' % (len(SZELLEM), len(irt)))
    if args.ir:
        with open(UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(sorok) + '\n')
        print('adat/forditasok.tsv irva')


if __name__ == '__main__':
    main()
