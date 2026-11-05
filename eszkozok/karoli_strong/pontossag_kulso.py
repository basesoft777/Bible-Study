#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a független Strong-forrással (Bible-Discovery, Strong-os Károli) való
összevetés versadagjainak kijelölése.

A forrás zárt licencű: a bemásolt szövege csak a repón kívül, mérésre áll
(DT32-elv, DT-F172a). Ez a szkript csak az adagok VERSLISTÁJÁT írja (igehely,
a forrás valószínű számozása), a forrás szövegét nem.

--adag 1 : formátum-, kiadás- és számozás-próba: rétegenként 1 vers a rétegzett
           minta verseiből, csak olyan, amelynek Károli- és KJV-számozása azonos
           (Karoli_versmegfeleltetes.tsv igehely_kjv), 8–30 Károli-szóval;
           rögzített mag -> f172/kulso/adag_01.tsv

Használat: python eszkozok/karoli_strong/pontossag_kulso.py --adag 1
"""

import argparse
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import pontossag_minta as pm  # noqa: E402
import tokenek  # noqa: E402

KULSO = os.path.join(pm.GYOKER, 'f172', 'kulso')
MAG = 20261105


def kjv_szam():
    """{Károli-igehely: KJV 'fejezet:vers'} a KJV-osztályú sorokból."""
    d = {}
    with open(tokenek.VERSMEGF, encoding='utf-8') as f:
        fej = None
        for s in f:
            if s.startswith('#'):
                continue
            m = s.rstrip('\n').rstrip('\r').split('\t')
            if fej is None:
                fej = m
                continue
            r = dict(zip(fej, m))
            d[r['igehely_karoli']] = r['igehely_kjv']
    return d


def azonos_szamozas(v, kjv, usz=False):
    """A versmegfeleltetési tábla csak az ÓSZ-t fedi; az ÚSZ-ben a Károli- és a
    KJV-számozás versszinten azonos (a tábla hiánya nem eltérés)."""
    if v not in kjv:
        return usz
    return kjv[v] == v.rsplit(' ', 1)[1]


def adag1():
    karoli, _ = bemenet._adatok()
    kjv = kjv_szam()
    h2s = tokenek.konyv_hu_to_step()
    _, minta = pm._tabla(os.path.join(pm.KIMENET, 'minta.tsv'))
    reteg_vers = {}
    for r in minta:
        reteg_vers.setdefault(r['reteg'], set()).add(r['vers'])
    rnd = random.Random('%d:adag1' % MAG)
    sorok = []
    for rt in pm.RETEGEK:
        jelolt = sorted(v for v in reteg_vers[rt]
                        if azonos_szamozas(v, kjv, rt.startswith('USZ')) and 8 <= len(tokenek.tokenizal(karoli[v])) <= 30)
        v = rnd.choice(jelolt)
        konyv, hely = v.rsplit(' ', 1)
        fe, ve = hely.split(':')
        sorok.append([rt, v, '%s %s' % (konyv, hely), '%s.%s.%s' % (h2s[konyv], fe, ve),
                      str(len(tokenek.tokenizal(karoli[v])))])
    os.makedirs(KULSO, exist_ok=True)
    with open(os.path.join(KULSO, 'adag_01.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 külső összevetés, 1. adag (formátum-, kiadás- és számozás-próba) | '
                'forras=f172/minta.tsv, konkordancia/Karoli_versmegfeleltetes.tsv @ git:%s | ts=git:%s | '
                'manual (determinisztikus, mag=%d); a forrás szövege nem kerül ide\n' % (pm.git_head(), pm.git_head(), MAG))
        f.write('reteg\tvers_karoli\tforras_valoszinu\tstep\tkaroli_szo\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    for s in sorok:
        print('\t'.join(s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adag', type=int, required=True)
    a = ap.parse_args()
    if a.adag == 1:
        adag1()
    else:
        raise SystemExit('a 2. adagtól a versek az Opus-futás után jelölhetők ki (még nincs megírva)')


if __name__ == '__main__':
    main()
