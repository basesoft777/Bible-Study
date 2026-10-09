#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tahot_job41_potlas.py — F84.2 (FELADATOK #84, N-F83a): a Károli Jób 41:1-34
héber sorainak átvétele a TAHOT_kivonat_nyitott_esetek.tsv-ből a
TAHOT_kivonat.tsv-be, Károli-kulccsal ("Jób 41:n").

Mit csinál:
  - a nyitott esetek 332 sorából (10 oszlop) a 0. oszlop (Job.41.n) -> "Jób 41:n"
    kulcsot és a 4-9. oszlopot veszi át (7 oszlopos fő kivonati sor);
  - a sorokat a "Jób 40:..." blokk utolsó sora után, a "Jób 42:1" elé szúrja,
    versenként az eredeti szósorrendben;
  - a nyitott fájlból a 332 sort törli, a fejléc marad (DT-F84a (a) 1.).

Biztonság (írás előtt, eltérésnél leáll):
  - a fő kivonat minden meglévő sora bájtazonos marad (a sorvégek is: LF);
  - a beszúrt sorok száma = a nyitott fájl adatsorainak száma = 332;
  - a nyitott fájl minden sora Job.41.n (n = 1-34), státusza ADATMINOSEGI_GYANU;
  - a fő kivonatban előtte 0 "Jób 41:" sor van.

Olvasás split('\\t'), írás '\\t'.join(); a csv modul nem használható (CLAUDE.md).
Használat: python eszkozok/tahot_job41_potlas.py [--ir]   (--ir nélkül szárazon fut)
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FO = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')
NY = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat_nyitott_esetek.tsv')
VART = 332


def leall(uzenet):
    print('LEÁLLÁS: ' + uzenet)
    sys.exit(1)


def beolvas(utvonal):
    with open(utvonal, 'rb') as f:
        nyers = f.read()
    if b'\r' in nyers:
        leall('CR a sorvégen: ' + utvonal)
    if not nyers.endswith(b'\n'):
        leall('hiányzó záró újsor: ' + utvonal)
    return nyers.decode('utf-8').split('\n')[:-1]


def main():
    ir = '--ir' in sys.argv
    fo = beolvas(FO)
    ny = beolvas(NY)
    fejlec_ny, ny_sorok = ny[0], ny[1:]
    if len(ny_sorok) != VART:
        leall('a nyitott fájl adatsorainak száma %d, nem %d' % (len(ny_sorok), VART))

    uj = []
    for s in ny_sorok:
        m = s.split('\t')
        if len(m) != 10:
            leall('nem 10 oszlopos sor: ' + s)
        mt = re.fullmatch(r'Job\.41\.(\d+)', m[0])
        if not mt or not 1 <= int(mt.group(1)) <= 34:
            leall('nem Job.41.n kulcs: ' + m[0])
        if m[2] != 'ADATMINOSEGI_GYANU':
            leall('váratlan státusz: ' + m[2])
        uj.append(('Jób 41:%s' % mt.group(1), '\t'.join(['Jób 41:' + mt.group(1)] + m[4:10])))
    versek = [int(k.split(':')[1]) for k, _ in uj]
    if versek != sorted(versek) or set(versek) != set(range(1, 35)):
        leall('a versek nem növekvő, teljes 1-34 sorrendben állnak')
    uj_sorok = [s for _, s in uj]

    if any(s.startswith('Jób 41:') for s in fo):
        leall('a fő kivonatban már van Jób 41 sor')
    idx40 = [i for i, s in enumerate(fo) if s.startswith('Jób 40:')]
    if not idx40 or idx40 != list(range(idx40[0], idx40[-1] + 1)):
        leall('a Jób 40 blokk nem folytonos')
    p = idx40[-1] + 1
    if not fo[p].startswith('Jób 42:1\t'):
        leall('a Jób 40 blokk után nem Jób 42:1 áll: ' + fo[p][:20])

    uj_fo = fo[:p] + uj_sorok + fo[p:]
    # összevetés: a meglévő sorok bájtazonosak és ugyanabban a sorrendben
    if uj_fo[:p] != fo[:p] or uj_fo[p + VART:] != fo[p:] or len(uj_fo) != len(fo) + VART:
        leall('a meglévő sorok nem maradtak azonosak')
    print('beszúrási pont: %d. fájlsor után (a Jób 40:24 utolsó sora), beszúrt sorok: %d, új sorszám: %d'
          % (p, len(uj_sorok), len(uj_fo) - 1))
    print('nyitott fájl: %d adatsor törlődik, a fejléc marad' % len(ny_sorok))
    if not ir:
        print('szárazon futott (--ir nélkül), semmi sem íródott')
        return
    with open(FO, 'wb') as f:
        f.write(('\n'.join(uj_fo) + '\n').encode('utf-8'))
    with open(NY, 'wb') as f:
        f.write((fejlec_ny + '\n').encode('utf-8'))
    print('kész')


if __name__ == '__main__':
    main()
