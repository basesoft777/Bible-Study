#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/zsolt_felirat_halmaz.py -- F91 E2: a feliratos zsoltárok felirat-verseinek EGYETLEN, egy helyen definiált halmaza.

Definíció (DT-F91a; a felhasználó döntése, 2026-10-14): kizárólag a `konkordancia/Karoli_1908.tsv` és a
`konkordancia/KJV_Strongs_teljes.tsv` verszámaiból. Zsoltáronként d = Károli-maximumvers - KJV-maximumvers;
ahol d > 0, a felirat-versek a Zsolt c:1 .. c:d (a Károli az MT szerint számoz: a felirat számozott vers,
a KJV a feliratot nem számozza). Egyetlen kivétel: Zsolt 13 (a két maximum egyenlő, mégis eltolt, mert a KJV a
13:5-öt két versre bontja; az LXX_OS-etalon szerint a Károli 13:1 felirat-vers, d = 1) -- ez az EGYETLEN
rögzített konstans (KIVETELEK).

NEM az A-táblából (`Karoli_versmegfeleltetes.tsv`) és NEM az LXX_OS `karoli_ok` jelöléséből számol: ezek ennek
a halmaznak a fogyasztói/ellenőrzői, nem a forrásai (körkörös függés elkerülése, DT-F91d).

Használat: `import zsolt_felirat_halmaz as ZFH; ZFH.felirat_versek()` -> frozenset({'Zsolt 3:1', ...});
`ZFH.felirat_d()` -> {zsoltár: d}. Önellenőrzés: `python eszkozok/zsolt_felirat_halmaz.py`.
Olvasás: split('\\t') (a csv modul tilos ezeken a táblákon).
"""
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')

# A d-szabálytól eltérő, rögzített kivétel: {zsoltár: d}. Forrás: DT-F91a (az etalon szerinti kivétel).
KIVETELEK = {13: 1}

_cache = {}


def _sorok(path):
    with open(path, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def felirat_d():
    """-> {zsoltár: d} a felirat-hosszal (d >= 1) rendelkező zsoltárokra (a Zsolt 13 kivétellel)."""
    if 'd' in _cache:
        return dict(_cache['d'])
    kar = defaultdict(set)
    for ln in _sorok(os.path.join(K, 'Karoli_1908.tsv')):
        m = re.match(r'Zsolt (\d+):(\d+)\t', ln)
        if m:
            kar[int(m.group(1))].add(int(m.group(2)))
    kjv = defaultdict(set)
    for ln in _sorok(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
        m = re.match(r'Psa\.(\d+)\.(\d+)\t', ln)
        if m:
            kjv[int(m.group(1))].add(int(m.group(2)))
    d = {}
    for c in range(1, 151):
        dc = max(kar[c]) - max(kjv[c])
        assert dc >= 0, 'Zsolt %d: a Károli rövidebb a KJV-nél' % c
        if dc > 0:
            d[c] = dc
    for c, dc in KIVETELEK.items():
        assert c not in d, 'a kivétel (Zsolt %d) már a d-szabályból is feliratos' % c
        d[c] = dc
    _cache['d'] = d
    return dict(d)


def felirat_versek():
    """-> frozenset({'Zsolt c:v', ...}): a felirat-versek Károli-kulcsai."""
    return frozenset('Zsolt %d:%d' % (c, v) for c, dc in felirat_d().items() for v in range(1, dc + 1))


def onellenorzes():
    d = felirat_d()
    h = felirat_versek()
    assert len(h) == 67, len(h)
    assert len(d) == 63, len(d)                                      # 62 feliratos zsoltár + Zsolt 13
    assert sorted(c for c, dc in d.items() if dc == 2) == [51, 52, 54, 60], d
    assert sum(1 for dc in d.values() if dc == 1) == 59              # 58 (d = 1) + Zsolt 13
    assert sum(1 for c in d if c not in KIVETELEK) == 62
    return len(h), len(d)


if __name__ == '__main__':
    n, z = onellenorzes()
    print('felirat-halmaz: %d vers, %d zsoltár (62 d-szabály + %s kivétel): rendben' % (n, z, sorted(KIVETELEK)))
