#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/strong_util.py -- F62: egységes Strong-normalizáló (SEMA 1.2).

SEMA 1.2: `H` vagy `G` + négy számjegy, balról nullázva (`H0779`); több
Strong-szám egy cellában `+` jellel, sorrendben (`G0934+G2406`).

    strong_normalizal(s, nyelv=None, utotag='tilt') -> str
    strong_ervenyes(s, nyelv=None, utotag='tilt')   -> bool

Szabályok (F62 M0, a felhasználó által elfogadva):
  - kisbetű és körülvevő szóköz megengedett (`h779` -> `H0779`);
  - 1-4 jegy balról nullázódik (`H779` -> `H0779`);
  - előtag nélküli szám (`1078`) csak `nyelv='H'|'G'` megadásával fogadható,
    egyébként ValueError;
  - ötjegyű kód: vezető nullával a nulla elhagyható (`G00120` -> `G0120`);
    nem nullával kezdődő ötjegyű csak G-előtaggal érvényes és változatlan
    marad (G-kiegészítő kód: `G20447`, `G20833`, TAGNT; DT-F62b), H-nál
    ValueError; hosszabb is ValueError (a csonkolás nem normalizálás);
  - betűutótag (`H2967a`): `utotag='tilt'` (alapérték) esetén ValueError,
    `utotag='megtart'` esetén kisbetűs utótagként megmarad;
  - `+` láncot elemenként normalizál, a sorrendet megőrzi;
  - minden más (`A0002`, `H5653G`, `H0710,H0713`, `—`, üres, nem string)
    ValueError. Csendes csonkolás, javítás nincs.

`strong_ervenyes` a *szigorú* SEMA 1.2 alakot vizsgálja: igaz, ha a bemenet
már pontosan a normalizált alakja önmagának (nem kell hozzá javítás).
"""

import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_RESZ_RE = re.compile(r'^([HGhg]?)(\d+)([a-z]?)$')


def _resz(resz, nyelv, utotag):
    m = _RESZ_RE.match(resz)
    if not m:
        raise ValueError('érvénytelen Strong-szám: %r' % resz)
    elotag, szamjegyek, betu = m.groups()
    elotag = elotag.upper()
    if not elotag:
        if nyelv is None:
            raise ValueError('előtag nélküli Strong-szám (nyelv= nélkül): %r' % resz)
        elotag = nyelv
    elif nyelv is not None and elotag != nyelv:
        raise ValueError('a Strong-szám előtagja (%s) ellentmond a nyelv=%s kérésnek: %r'
                         % (elotag, nyelv, resz))
    if len(szamjegyek) == 5 and szamjegyek[0] == '0':
        szamjegyek = szamjegyek[1:]
    elif len(szamjegyek) == 5 and elotag == 'G':
        pass  # G-kiegészítő kód (G + öt számjegy, nem nullával kezdődik): változatlan
    elif len(szamjegyek) > 4:
        raise ValueError('a Strong-szám négynél több számjegyet tartalmaz, és nem G-kiegészítő kód: %r'
                         % resz)
    if int(szamjegyek) == 0:
        raise ValueError('a Strong-szám nulla: %r' % resz)
    if betu and utotag != 'megtart':
        raise ValueError('betűutótagos Strong-szám (utotag=tilt): %r' % resz)
    return '%s%04d%s' % (elotag, int(szamjegyek), betu)


def strong_normalizal(s, nyelv=None, utotag='tilt'):
    """Egy Strong-kód vagy `+` lánc -> SEMA 1.2 alak. Érvénytelen bemenetre ValueError."""
    if not isinstance(s, str):
        raise ValueError('a Strong-szám nem szöveg: %r' % (s,))
    if nyelv not in (None, 'H', 'G'):
        raise ValueError('nyelv csak None, H vagy G lehet: %r' % (nyelv,))
    if utotag not in ('tilt', 'megtart'):
        raise ValueError('utotag csak tilt vagy megtart lehet: %r' % (utotag,))
    s = s.strip()
    if not s:
        raise ValueError('üres Strong-szám')
    return '+'.join(_resz(r.strip(), nyelv, utotag) for r in s.split('+'))


def strong_ervenyes(s, nyelv=None, utotag='tilt'):
    """Igaz, ha `s` már pontosan SEMA 1.2 alakú (normalizálás nélkül is érvényes)."""
    try:
        return strong_normalizal(s, nyelv=nyelv, utotag=utotag) == s
    except ValueError:
        return False
