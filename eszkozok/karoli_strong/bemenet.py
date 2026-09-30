#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 — a modell bemenetének összeállítása (prompt + versblokkok).

A versblokk formája a fő brief (F22 22.1) szerint:

    VERS: 1Móz 1:1
    KÁROLI (számozott szavak): 1 Kezdetben | 2 teremté | ...
    EREDETI (számozott szavak): 1 בְּ H9003 [in] | 2 רֵאשִׁית H7225 [beginning] | ...
    KJV-TÁMPONT: In the beginning{H7225} God{H0430} ...

  * a Strong-szám a bemenetben tájékoztató, a kimenetben tilos;
  * ÚSZ-ben a nem TR-es sor `[nem TR]` jelölést kap;
  * a KJV-TÁMPONT sor csak akkor áll ott, ha a kjv paraméter igaz ÉS van
    KJV-támpont a versre (a pilotban csak az R1 könyveire).

A prompt szövege az f21p/prompt_v1.md PROMPT-KEZDET és PROMPT-VÉGE jelölői
közötti rész (a fájl többi része dokumentáció, nem megy ki a modellnek); a
{{VERSBLOKK:<igehely>}} helyőrzők helyére a példavers bemenete kerül.

A modul csak olvas; nem hív hálózatot, nem kezel titkot.
"""

import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

PROMPT_UT = os.path.join(tokenek.ROOT, 'f21p', 'prompt_v1.md')
PROMPT_V2_UT = os.path.join(tokenek.ROOT, 'f21p', 'prompt_v2.md')   # F21.12, az F3V2 futáshoz
PROMPT_V3_UT = os.path.join(tokenek.ROOT, 'f21p', 'prompt_v3.md')   # F21.42, az F3V3 és a SONNETV3 futáshoz (P3c)
KEZDET = '<!-- PROMPT-KEZDET -->'
VEGE = '<!-- PROMPT-VÉGE -->'

_CACHE = {}


def _adatok():
    if not _CACHE:
        _CACHE['karoli'] = tokenek.betolt_karoli()
        _CACHE['ered'] = tokenek.betolt_eredeti()
    return _CACHE['karoli'], _CACHE['ered']


def vers_adat(igehely):
    """Egy vers adatai a kapuhoz és a bemenethez."""
    karoli, ered = _adatok()
    return {
        'igehely': igehely,
        'karoli_tokenek': tokenek.tokenizal(karoli[igehely]),
        'eredeti': ered[igehely],
    }


def versblokk(igehely, kjv=True):
    """A modell bemenetének egy versblokkja (szöveg)."""
    d = vers_adat(igehely)
    k = ' | '.join('%d %s' % (i, t) for i, t in enumerate(d['karoli_tokenek'], 1))
    e_reszek = []
    for w in d['eredeti']:
        s = '%d %s %s [%s]' % (w['sorsz'], w['alak'], w['strong'], w['tukor'])
        if w['nem_tr']:
            s += ' [nem TR]'
        e_reszek.append(s)
    sorok = ['VERS: %s' % igehely,
             'KÁROLI (számozott szavak): %s' % k,
             'EREDETI (számozott szavak): %s' % ' | '.join(e_reszek)]
    if kjv:
        t = tokenek.kjv_tamapont(igehely)
        if t:
            sorok.append('KJV-TÁMPONT: %s' % t)
    return '\n'.join(sorok)


def prompt_utasitas(prompt_ut=None):
    """Az utasításrész a prompt-fájl jelölői között (alapértelmezés: prompt_v1.md)."""
    with open(prompt_ut or PROMPT_UT, encoding='utf-8') as f:
        s = f.read()
    a = s.index(KEZDET) + len(KEZDET)
    b = s.index(VEGE)
    szoveg = s[a:b].strip('\n')
    # a példabemenetek nincsenek kézzel beírva (a héber/görög alakok kódolása
    # törékeny): {{VERSBLOKK:<igehely>}} -> versblokk(igehely, kjv=True)
    return re.sub(r'\{\{VERSBLOKK:([^}]+)\}\}', lambda m: versblokk(m.group(1), kjv=True), szoveg)


def prompt_sha256(prompt_ut=None):
    return hashlib.sha256(prompt_utasitas(prompt_ut).encode('utf-8')).hexdigest()


def kotegek(igehelyek, meret=10):
    """Az igehelyek 10-es kötegei (F21 P0.3: 10 vers / hívás)."""
    return [igehelyek[i:i + meret] for i in range(0, len(igehelyek), meret)]


def kotegszoveg(igehelyek, kjv=True, prompt_ut=None):
    """Egy hívás teljes felhasználói üzenete: utasítás + versblokkok."""
    blokkok = '\n\n'.join(versblokk(ig, kjv) for ig in igehelyek)
    return '%s\n\n=== A FELDOLGOZANDÓ VERSEK (%d) ===\n\n%s\n' % (prompt_utasitas(prompt_ut), len(igehelyek), blokkok)


if __name__ == '__main__':
    ig = sys.argv[1] if len(sys.argv) > 1 else '1Móz 1:1'
    print(versblokk(ig, kjv=True))
