#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a független Strong-forrással (Bible-Discovery, Strong-os Károli) való
összevetés versadagjainak kijelölése.

A forrás zárt licencű: a bemásolt szövege csak a repón kívül, mérésre áll
(DT32-elv, DT-F172a). Ez a szkript csak az adagok VERSLISTÁJÁT írja (igehely,
a forrás valószínű számozása), a forrás szövegét nem.

A bemásolás egysége a teljes fejezet (Károli: „rész”), rétegenként egy
(DT-F172a (4″), a felhasználó: „max egy teljes rész tudok másolni”, „8 fejezet”).

--fejezetek : rétegenként az a fejezet, amelyben a legtöbb célpár van (a
              rétegzett minta párjai: előbb az Opus-eltérések, utána az összes
              célpár száma; döntetlennél a fejezet neve). Feltétel: a fejezet
              minden versének Károli- és KJV-száma azonos, és más Károli-vers nem
              esik a KJV-fejezetbe (ÚSZ: a tábla nem fedi, azonosnak vesszük);
              15–40 vers; nincs `kezi` (fuggoben) tokenje; a fejezetek
              különbözők. -> f172/kulso/fejezetek.tsv (a párok száma: összes és
              tartalmi, azaz nem morféma)

Használat: python eszkozok/karoli_strong/pontossag_kulso.py --fejezetek
"""

import argparse
import os
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


def fejezet_of(v):
    konyv, hely = v.rsplit(' ', 1)
    return '%s %s' % (konyv, hely.split(':')[0])


def fejezetek():
    karoli, _ = bemenet._adatok()
    kjv = kjv_szam()
    _, itelet = pm._tabla(os.path.join(pm.KIMENET, 'itelet_par.tsv'))
    # Károli-versek fejezetenként
    fej_versek = {}
    for v in karoli:
        fej_versek.setdefault(fejezet_of(v), []).append(v)
    # KJV-fejezetbe eső Károli-versek (ÓSZ)
    kjv_be = {}
    for v, k in kjv.items():
        if k and ':' in k:
            kjv_be.setdefault('%s %s' % (v.rsplit(' ', 1)[0], k.split(':')[0]), set()).add(v)
    # párok és kezi fejezetenként
    par, tart, kezi = {}, {}, set()
    for k in pm.konyvek():
        _, sorok = pm._tabla(os.path.join(pm.ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            f = fejezet_of(r['vers'])
            par[f] = par.get(f, 0) + 1
            s = r['strong']
            if not (s.startswith('H90') and len(s) == 5):
                tart[f] = tart.get(f, 0) + 1
        _, sz = pm._tabla(os.path.join(pm.ADAT, 'szavak_%s.tsv' % k))
        for r in sz:
            if r['allapot'] == 'fuggoben':
                kezi.add(fejezet_of(r['vers']))
    h2s = tokenek.konyv_hu_to_step()

    def alkalmas(f, usz):
        vv = fej_versek.get(f, [])
        if not (15 <= len(vv) <= 40) or f in kezi:
            return False
        if usz:
            return True
        if any(not azonos_szamozas(v, kjv) for v in vv):
            return False
        return kjv_be.get(f, set()) <= set(vv)

    valasztott, sorok = set(), []
    for rt in pm.RETEGEK:
        usz = rt.startswith('USZ')
        cel = {}
        for r in itelet:
            if r['reteg'] != rt:
                continue
            f = fejezet_of(r['vers'])
            d = cel.setdefault(f, [0, 0, 0])
            d[0] += r['helyes'] == '0' and r['morfema'] == '0'
            d[1] += r['helyes'] == '0'
            d[2] += 1
        jel = [f for f in cel if f not in valasztott and alkalmas(f, usz)]
        if not jel:
            raise SystemExit('nincs alkalmas fejezet: %s' % rt)
        f = sorted(jel, key=lambda f: (-cel[f][0], -cel[f][1], -cel[f][2], f))[0]
        valasztott.add(f)
        konyv, fe = f.rsplit(' ', 1)
        sorok.append([rt, f, '%s.%s' % (h2s[konyv], fe), str(len(fej_versek[f])), str(cel[f][2]), str(cel[f][1]),
                      str(cel[f][0]), str(par.get(f, 0)), str(tart.get(f, 0))])
    os.makedirs(KULSO, exist_ok=True)
    head = pm.git_head()
    with open(os.path.join(KULSO, 'fejezetek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=F172 külső összevetés fejezetei (Bible-Discovery, Strong-os Károli, régies) | '
                'forras=f172/itelet_par.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, adat/karoli_strong/ @ git:%s | '
                'ts=git:%s | manual (determinisztikus kiválasztás); a forrás szövege nem kerül ide\n' % (head, head))
        f.write('\t'.join(['reteg', 'fejezet', 'step', 'versek', 'celpar', 'celpar_elteres', 'celpar_elteres_tartalmi',
                           'par_osszes', 'par_tartalmi']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    for s in sorok:
        print('\t'.join(s))
    print('összes pár: %d, tartalmi: %d' % (sum(int(s[7]) for s in sorok), sum(int(s[8]) for s in sorok)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fejezetek', action='store_true')
    a = ap.parse_args()
    if not a.fejezetek:
        ap.error('--fejezetek')
    fejezetek()


if __name__ == '__main__':
    main()
