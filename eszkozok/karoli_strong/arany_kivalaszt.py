#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P1 — az Opus-aranyminta 60 versének kiválasztása a 200 verses mintából.

Kimenet: f21p/opus_arany_kivalasztas.tsv (generált; kézzel nem szerkesztendő).
A f21p/minta.tsv nem változik (a minta_general.py bájtazonossága és a
minta_ellenoriz.py érintetlen marad).

Brief (F21 P1): R1-ből 20, R2 és R3 együtt 20, R4-ből 20 vers. A brieffel nem
rögzített részletek a szkript rögzített döntései:

  * Egész kötegek: a minta 10 verses kötegei (kotegsz) nem törnek szét, tehát
    rétegcsoportonként 2 teljes köteg kerül az aranyba (6 köteg, 60 vers). Így a
    mérésnél az arany versei hívásonként is összevethetők.
  * Arányosság a rétegcsoporton belül, amennyire egész kötegekkel lehet:
      - R2+R3: egy tisztán R2-es és egy tisztán R3-as köteg (10 + 10 vers);
        a vegyes 13. köteg kimarad;
      - R4: egy tisztán evangéliumi és egy tisztán levél-köteg (10 + 10);
        a vegyes 18. köteg kimarad;
      - R1: két köteg két különböző könyvből (a 40/30/30-as könyvarány egész
        kötegekkel nem tartható; a két különböző könyv a legközelebbi közelítés).
  * A megengedett kötegpárok kanonikus (rendezett) listájából a húzás
    random.Random(MAG).choice, rétegcsoportonként ebben a sorrendben: R1,
    R2+R3, R4. A maggal és a minta.tsv-vel a kimenet bájtra azonos.

Futtatás a repó gyökeréből:
    python eszkozok/karoli_strong/arany_kivalaszt.py
"""

import itertools
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

MAG = 20260930
MINTA = os.path.join(tokenek.ROOT, 'f21p', 'minta.tsv')
KIMENET = os.path.join(tokenek.ROOT, 'f21p', 'opus_arany_kivalasztas.tsv')


def _kotegek(sorok):
    """kotegsz -> a köteg sorai (minta.tsv mezőlisták)."""
    k = {}
    for r in sorok:
        k.setdefault(int(r[4]), []).append(r)
    return k


def _tiszta(koteg, mezo_ertek):
    """Minden sor megfelel-e a (mezőindex, érték) feltételnek."""
    i, v = mezo_ertek
    return all(r[i] == v for r in koteg)


def megengedett_parok(kotegek):
    """Rétegcsoportonként a megengedett kötegpárok rendezett listája."""
    k1 = sorted(n for n, s in kotegek.items() if _tiszta(s, (2, 'R1')))
    r1 = []
    for a, b in itertools.combinations(k1, 2):
        ka = {tokenek.konyv_rovid(r[1]) for r in kotegek[a]}
        kb = {tokenek.konyv_rovid(r[1]) for r in kotegek[b]}
        if len(ka) == 1 and len(kb) == 1 and ka != kb:
            r1.append((a, b))
    r2 = sorted(n for n, s in kotegek.items() if _tiszta(s, (2, 'R2')))
    r3 = sorted(n for n, s in kotegek.items() if _tiszta(s, (2, 'R3')))
    ev = sorted(n for n, s in kotegek.items() if _tiszta(s, (3, 'evangelium')))
    lv = sorted(n for n, s in kotegek.items() if _tiszta(s, (3, 'level')))
    return [
        ('R1', r1),
        ('R2+R3', [(a, b) for a in r2 for b in r3]),
        ('R4', [(a, b) for a in ev for b in lv]),
    ]


def general():
    sorok = tokenek._sorok(MINTA)
    kotegek = _kotegek(sorok)
    rnd = random.Random(MAG)
    valasztott = []
    naplo = []
    for csoport, parok in megengedett_parok(kotegek):
        if not parok:
            raise SystemExit('nincs megengedett kötegpár: %s' % csoport)
        par = rnd.choice(parok)
        naplo.append((csoport, len(parok), par))
        valasztott.extend(par)
    ki = ['\t'.join(['sorsz', 'igehely', 'reteg', 'alreteg', 'kotegsz', 'retegcsoport'])]
    for n in sorted(valasztott):
        for r in kotegek[n]:
            csop = 'R2+R3' if r[2] in ('R2', 'R3') else r[2]
            ki.append('\t'.join([r[0], r[1], r[2], r[3], r[4], csop]))
    return ki, naplo


def main():
    ki, naplo = general()
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    for csoport, n, par in naplo:
        print('%s: %d megengedett pár, húzott kötegek: %s' % (csoport, n, list(par)))
    print('vers: %d -> %s' % (len(ki) - 1, KIMENET))


if __name__ == '__main__':
    main()
