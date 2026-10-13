#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/nave_bontas.py -- F92: a Nave-hivatkozasok versekre bontasanak KOZOS szabalya.

A `Nave_basokant.tsv` `igehely` oszlopa KJV-szamozasu (`Jozs 21:4`, `2Moz 6:16-20`, `Zsolt 22`).
A szabaly egy helyen el: az epito (`sqlite_epit.py`, `nave_vers` tabla) ezt hasznalja. Az
olvasoi pilot (`olvaso_pilot/bovites.py`) a sajat peldanyan maradt (DT-F92a, 5.; N-F92a: a #76
kiolvasoja a kozos modult hasznalja, a pilot-peldany ott megszunik); a `teszt_olvaso_pilot.py`
D2-egyezesi tesztje orzi, hogy a ket peldany azonosat ad.

A szabaly:
  1. Hely-elemzes: `Konyv f[:v][-[f:]v]`. Fejezet-szintu hely (nincs vers) es nem
     ertelmezheto / ures hely NEM bomlik versekre: a `kihagyott` szamlalo viszi (semmi sem
     tunik el nemanak).
  2. A tartomany a Karoli-versek KJV-kulcsa szerint bomlik. Egy Karoli-vers KJV-kulcsa
     (a pilot `bovites.py` szabalyaval azonosan):
       (a) a LXX_OS `igehely_kjv` oszlopa (a `zsolt_felirat_eltolas` sorok kihagyasaval; a
           Karoli-versre az elso sor), ha `f:v` alaku;
       (b) ennek hianyaban a fejezet eltolasa (a fejezetben utoljara latott (a) szerinti
           vers KJV-versszama minusz Karoli-versszama);
       (c) egyebkent a `Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopa, vegul a
           Karoli-szam.
"""

import re

NAVE_HELY_RE = re.compile(r'^(\S+) (\d+)(?::(\d+))?(?:-(?:(\d+):)?(\d+))?$')
KAROLI_RE = re.compile(r'^(\S+) (\d+):(\d+)$')
CV_RE = re.compile(r'^(\d+):(\d+)$')

# a Nave/Karoli konyvkod-alias (a normalizalo tabla `JSir`-je, az adat-kulcs `Sir`)
KONYV_ALIAS = {'JSir': 'Sir'}


def hely_elemez(ertek):
    """-> ('vers', konyv, c1, v1, c2, v2) | ('fejezet', konyv, c) | None (ures / nem ertelmezheto)."""
    m = NAVE_HELY_RE.match((ertek or '').strip())
    if not m:
        return None
    konyv = KONYV_ALIAS.get(m.group(1), m.group(1))
    c1 = int(m.group(2))
    if m.group(3) is None:
        return ('fejezet', konyv, c1)
    v1 = int(m.group(3))
    c2 = int(m.group(4)) if m.group(4) else c1
    v2 = int(m.group(5)) if m.group(5) else v1
    return ('vers', konyv, c1, v1, c2, v2)


def _cv(s):
    m = CV_RE.match(s or '')
    return (int(m.group(1)), int(m.group(2))) if m else None


def karoli_szam(igehely):
    m = KAROLI_RE.match(igehely)
    return (KONYV_ALIAS.get(m.group(1), m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


class KjvRacs(object):
    """A Karoli-versek KJV-kulcsa es a (konyv, KJV-fejezet) -> [(KJV-vers, Karoli-igehely)] index.

    karoli_versek: a Karoli-igehelyek Karoli-sorrendben; lxx_kjv: {karoli_igehely: 'f:v' | ''}
    (a LXX_OS elso, nem felirat-eltolas sora); vm_kjv: {karoli_igehely: 'f:v'} (a
    Karoli_versmegfeleltetes.tsv `igehely_kjv` oszlopa)."""

    def __init__(self, karoli_versek, lxx_kjv, vm_kjv):
        self.kulcs = {}
        self.mod = {}
        eltolas = {}
        szamok = {}
        for ig in karoli_versek:
            a = karoli_szam(ig)
            if a is None:
                continue
            szamok[ig] = a
            k = _cv(lxx_kjv.get(ig, ''))
            if k:
                self.kulcs[ig] = k
                self.mod[ig] = 'LXX_OS'
                eltolas[(a[0], a[1])] = k[1] - a[2]
        for ig in karoli_versek:
            if ig in self.kulcs or ig not in szamok:
                continue
            a = szamok[ig]
            if (a[0], a[1]) in eltolas:
                self.kulcs[ig] = (a[1], a[2] + eltolas[(a[0], a[1])])
                self.mod[ig] = 'fejezet_eltolas'
            else:
                k = _cv(vm_kjv.get(ig, ''))
                self.kulcs[ig] = k or (a[1], a[2])
                self.mod[ig] = 'versmegfeleltetes' if k else 'karoli_szam'
        self.index = {}
        for ig in karoli_versek:
            if ig not in szamok:
                continue
            c, v = self.kulcs[ig]
            self.index.setdefault((szamok[ig][0], c), []).append((v, ig))

    def bont(self, konyv, c1, v1, c2, v2):
        """A KJV-tartomany Karoli-versei (a Karoli-sorrend fejezetenkent, vers szerint rendezve)."""
        ki = []
        for c in range(c1, c2 + 1):
            for v, ig in self.index.get((konyv, c), ()):
                if (c1, v1) <= (c, v) <= (c2, v2):
                    ki.append(ig)
        return ki


def nave_bont(sorok, racs):
    """sorok: a Nave_basokant.tsv dict-sorai (fajlsorrendben). Visszaad:
    (ki, kihagyott, bontott_sor): ki = [(forras_sor, sor_dict, karoli_igehely, tartomanyos)],
    kihagyott = {ok: darab} (forras-sorok), bontott_sor = a legalabb egy verssorra bontott
    forras-sorok szama. Invarians: len(sorok) == bontott_sor + sum(kihagyott.values())."""
    ki, kihagyott, bontott = [], {}, 0
    for i, r in enumerate(sorok, 1):
        h = hely_elemez(r['igehely'])
        if h is None:
            ok = 'igehely_nelkuli' if not (r['igehely'] or '').strip() else 'nem_ertelmezheto_hely'
            kihagyott[ok] = kihagyott.get(ok, 0) + 1
            continue
        if h[0] == 'fejezet':
            kihagyott['fejezet_szintu'] = kihagyott.get('fejezet_szintu', 0) + 1
            continue
        _, konyv, c1, v1, c2, v2 = h
        versek = racs.bont(konyv, c1, v1, c2, v2)
        if not versek:
            kihagyott['nincs_karoli_vers_a_tartomanyban'] = kihagyott.get('nincs_karoli_vers_a_tartomanyban', 0) + 1
            continue
        bontott += 1
        tart = (c1, v1) != (c2, v2)
        for ig in versek:
            ki.append((i, r, ig, 1 if tart else 0))
    return ki, kihagyott, bontott
