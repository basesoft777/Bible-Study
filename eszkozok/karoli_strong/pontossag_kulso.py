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


ELTERES_MAX = 60
EGYEZES_DB = 60
ADAG_VERS = 8


def adagok():
    """A 2. adagtól: a célpárok (DT-F172a (4)) versei.

    Célpár csak tartalmi (nem morféma) pár lehet: a forrás a H9001–H9049
    morféma-kódokat nem hordozza. Eltérés: a vak Opus-ellenőr halmazán kívüli
    gépi pár (legfeljebb 60, rögzített maggal); egyezés: 60 pár rétegenként
    egyenlő arányban (a maradék a nagyobb súlyú rétegekhez). A versek
    rétegsorrendben, 8-as adagokban; az 1. adag versei kimaradnak."""
    _, itelet = pm._tabla(os.path.join(pm.KIMENET, 'itelet_par.tsv'))
    tart = [r for r in itelet if r['morfema'] == '0']
    rnd = random.Random('%d:adagok' % MAG)
    elt = [r for r in tart if r['helyes'] == '0']
    if len(elt) > ELTERES_MAX:
        elt = sorted(rnd.sample(elt, ELTERES_MAX), key=lambda r: r['minta_id'])
    egy = []
    alap, maradek = divmod(EGYEZES_DB, len(pm.RETEGEK))
    for i, rt in enumerate(pm.RETEGEK):
        k = alap + (1 if i < maradek else 0)
        jel = [r for r in tart if r['helyes'] == '1' and r['reteg'] == rt]
        egy += sorted(rnd.sample(jel, min(k, len(jel))), key=lambda r: r['minta_id'])
    _, a1 = pm._tabla(os.path.join(KULSO, 'adag_01.tsv'))
    mar = {r['vers_karoli'] for r in a1}
    vers_cel = {}
    for tipus, rr in [('elteres', elt), ('egyezes', egy)]:
        for r in rr:
            vers_cel.setdefault(r['vers'], {'reteg': r['reteg'], 'celok': []})['celok'].append(
                '%s:%s' % (tipus, r['minta_id']))
    kjv = kjv_szam()
    h2s = tokenek.konyv_hu_to_step()
    sorrend = sorted((v for v in vers_cel if v not in mar),
                     key=lambda v: (pm.RETEGEK.index(vers_cel[v]['reteg']), v))
    kimaradt = sorted(v for v in vers_cel if v in mar)
    os.makedirs(KULSO, exist_ok=True)
    with open(os.path.join(KULSO, 'adagok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 külső összevetés, 2.+ adag (célpárok versei) | forras=f172/itelet_par.tsv @ git:%s | '
                'ts=git:%s | manual (determinisztikus, mag=%d; eltérés ≤%d, egyezés %d, tartalmi párok); '
                'az 1. adagban már szereplő vers: %s\n' % (pm.git_head(), pm.git_head(), MAG, ELTERES_MAX, EGYEZES_DB,
                                                          ', '.join(kimaradt) or '-'))
        f.write('adag\treteg\tvers_karoli\tforras_valoszinu\tstep\tcelok\n')
        for i, v in enumerate(sorrend):
            konyv, hely = v.rsplit(' ', 1)
            fe = kjv.get(v, hely) if v in kjv or not vers_cel[v]['reteg'].startswith('OSZ') else ''
            fv = ('%s %s' % (konyv, fe)) if fe else '(nincs KJV-megfelelő)'
            st = '%s.%s' % (h2s[konyv], fe.replace(':', '.')) if fe else ''
            f.write('\t'.join([str(2 + i // ADAG_VERS), vers_cel[v]['reteg'], v, fv, st,
                               ','.join(vers_cel[v]['celok'])]) + '\n')
    print('eltérés-cél %d, egyezés-cél %d, vers %d (+%d az 1. adagban), adag %d' % (
        len(elt), len(egy), len(sorrend), len(kimaradt), (len(sorrend) + ADAG_VERS - 1) // ADAG_VERS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adag', type=int)
    ap.add_argument('--adagok', action='store_true', help='a 2.+ adag versei (az Opus-futás után)')
    a = ap.parse_args()
    if a.adag == 1:
        adag1()
    elif a.adagok:
        adagok()
    else:
        ap.error('--adag 1 vagy --adagok')


if __name__ == '__main__':
    main()
