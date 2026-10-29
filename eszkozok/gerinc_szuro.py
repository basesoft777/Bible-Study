#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerinc_szuro.py -- F124 (DT-F124a (2)): a #110 szuro-szabaly (DT283)
determinisztikus resze importalhato alakban, a gerinc-kartya es a
prioritasi terkep szamara.

A szabaly szovege es a mert eredmenyek: DONTESEK.md DT283,
naplok/SZURO_PILOT_ISTENTISZT_naplo.md 2. szakasz. A fuggvenyek az
`eszkozok/f110_szuro.py` (lezart F110, valtozatlan) `heber()`/`gorog()`
logikajat veszik at, de nem fix bemenetbol, hanem egy vers tokenlistajabol
dolgoznak, es modul-szinten nem futtatnak semmit.

Csak az ISTENTISZT-001 gerinc-elemeire (H7121+H8034, G1941) ad szabalyt;
minden mas motivum tag Strongjara a kartya `szuretlen_tag` jelzest ad
(DT184 (d)).

A szuro nem dont: a K osztaly (kiszurve) okkodot kap, az A/B osztaly
atjut, de kezi olvasasra (DT283 (a) pontositas: az A osztaly sem
automatikus bevetel).

Token: dict {'strong', 'gloss'} -- a TAHOT/TAGNT sor `Strong-szám` es
`Angol tükörfordítás` mezoje, fajlsorrendben.
"""

import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

MOTIVUM_ID = 'ISTENTISZT-001'

# --- a szabaly parameterei (DT283 / naplok/SZURO_PILOT_ISTENTISZT_naplo.md 2.) ---
ABLAK_H = 6      # H7121 es H8034 legfeljebb ennyi tokenre
ISTENNEV_H = {'H3068', 'H0430', 'H0136', 'H0410', 'H3050', 'H1168'}   # JHWH, Elohim, Adonaj, El, Jah, Baal
PASSZIV_H = re.compile(
    r'\b(is|was|were|are|has been|have been|had been|will be|be|may it be|let it be|they will be|being)\b'
    r'.*\b(called|named|proclaimed|summoned)\b|^named$|it has been named')
ISTEN_G = {'G2962', 'G2316', 'G2424', 'G3686', 'G3962', 'G5547'}      # Ur, Isten, Jezus, nev, Atya, Krisztus
JOGI_G = {'G2541', 'G4575'}                                           # Kaisar, Szebasztosz
PASSZIV_G = re.compile(r'\b(is|was|has been|having been|to be|be|is being)\s+called\b|\bbeing called\b')
ABLAK_G = 3
ABLAK_JOGI = 8

# A szurot kapo (motivum-id, Strong-tag) parok.
SZURT_TAGOK = {
    (MOTIVUM_ID, 'H7121'): 'heber',
    (MOTIVUM_ID, 'H8034'): 'heber',
    (MOTIVUM_ID, 'G1941'): 'gorog',
}

_RANG = {'A': 0, 'B': 1, 'K': 2}


def szuro_tipus(motivum_id, tag):
    """'heber' | 'gorog' | None -- van-e gepi szuro erre a (motivum, tag) parra."""
    return SZURT_TAGOK.get((motivum_id, tag))


def heber(tokenek):
    """(osztaly, okkod, indoklas) a vers H7121+H8034 szerkezetere (TAHOT-tokenek)."""
    S = [t['strong'] for t in tokenek]
    I = [i for i, s in enumerate(S) if s == 'H7121']
    J = [j for j, s in enumerate(S) if s == 'H8034']
    parok = [(i, j) for i in I for j in J if abs(i - j) <= ABLAK_H]
    if not parok:
        return ('K', 'K0_nincs_par',
                'a versben nincs egymástól %d tokenen belüli H7121+H8034 pár' % ABLAK_H)
    legjobb = None
    for i, j in parok:
        gloss = tokenek[i]['gloss'].strip()
        passz = bool(PASSZIV_H.search(gloss))
        be = j > 0 and S[j - 1] == 'H9003'
        obj = 'H0853' in S[min(i, j):max(i, j) + 1]
        al = 'H5921' in S[min(i, j):max(i, j) + 4]
        isten = any(s in ISTENNEV_H for s in S[j + 1:j + 4])
        if passz:
            r = ('K', 'K1_passziv', 'passzív/megnevezett ige (%s)%s' % (gloss, '; + עַל' if al else ''))
        elif not be:
            r = ('K', 'K2_nincs_be', 'nincs בְּ-előtag a שֵׁם előtt (%s)%s' % (
                'megnevezés: tárgyjel H0853' if obj else 'egyéb',
                '; isteni névvel: HATÁRESET' if isten else ''))
        elif isten:
            r = ('A', 'A_be_isten', 'aktív קרא + בְּ + שֵׁם + isteni névszó (%s)' % gloss)
        else:
            r = ('B', 'B_be_nem_nevszo',
                 'aktív קרא + בְּ + שֵׁם, de isteni névszó nincs a közelben: kézi olvasás (%s)' % gloss)
        if legjobb is None or _RANG[r[0]] < _RANG[legjobb[0]]:
            legjobb = r
    return legjobb


def gorog(tokenek):
    """(osztaly, okkod, indoklas) a vers G1941-tokenjeire (TAGNT-tokenek).
    Ha a versben nincs G1941, None."""
    S = [t['strong'] for t in tokenek]
    ki = []
    for i, s in enumerate(S):
        if s != 'G1941':
            continue
        gloss = tokenek[i]['gloss']
        kozel = set(S[max(0, i - ABLAK_G):i + ABLAK_G + 1])
        if PASSZIV_G.search(gloss):
            r = ('K', 'K1_passziv', 'passzív/megnevezett (%s)' % gloss)
        elif set(S[max(0, i - ABLAK_JOGI):i + ABLAK_JOGI + 1]) & JOGI_G:
            r = ('K', 'K3_jogi', 'jogi fellebbezés: Kaisar/Szebasztosz a környezetben (%s)' % gloss)
        elif kozel & ISTEN_G:
            r = ('A', 'A_aktiv_isten', 'aktív/középigés + isteni szó a környezetben (%s)' % gloss)
        else:
            r = ('B', 'B_nincs_isten',
                 'aktív/középigés, de isteni szó nincs a közelben: kézi olvasás (%s)' % gloss)
        ki.append(r)
    if not ki:
        return None
    ki.sort(key=lambda r: _RANG[r[0]])
    return ki[0]


def szur(motivum_id, tag, tahot_tokenek, tagnt_tokenek):
    """A (motivum, tag) pár szuro-eredmenye egy versre: (osztaly, okkod, indoklas),
    vagy None, ha nincs gepi szuro erre a parra."""
    tipus = szuro_tipus(motivum_id, tag)
    if tipus == 'heber':
        return heber(tahot_tokenek)
    if tipus == 'gorog':
        return gorog(tagnt_tokenek)
    return None
