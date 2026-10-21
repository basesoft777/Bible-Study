#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f110_szuro.py — F110: a DT-F110a szűrő-szabály determinisztikus része az
ISTENTISZT-001 új helyeire (H7121+H8034 168 hely; G1941 21 hely).
Csak szimulál: a naplok/F110_szuro_szimulacio.tsv-t írja; az adat/jeloltek.tsv-hez
nem nyúl (azt a jóváhagyott szabály után a F110 5. lépése írja).
Olvasás: split('\t') (nem csv).
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

# --- a szabály paraméterei (a naplo 2. szakaszával azonos) ---
ABLAK = 6                       # H7121 és H8034 legfeljebb ennyi tokenre
ISTENNEV_H = {'H3068', 'H0430', 'H0136', 'H0410', 'H3050', 'H1168'}   # JHWH, Elohim, Adonaj, El, Jah, Baál
PASSZIV_H = re.compile(r'\b(is|was|were|are|has been|have been|had been|will be|be|may it be|let it be|they will be|being)\b.*\b(called|named|proclaimed|summoned)\b|^named$|it has been named')
ISTEN_G = {'G2962', 'G2316', 'G2424', 'G3686', 'G3962', 'G5547'}   # Úr, Isten, Jézus, név, Atya, Krisztus
JOGI_G = {'G2541', 'G4575'}      # Kaisar, Szebasztosz
PASSZIV_G = re.compile(r'\b(is|was|has been|having been|to be|be|is being)\s+called\b|\bbeing called\b')
ABLAK_G = 3
ABLAK_JOGI = 8   # a jogi fellebbezés tárgya (Kaisar/Szebasztosz) távolabb is állhat


def beolvas(fn):
    by = defaultdict(list)
    for i, l in enumerate(open(ROOT / 'konkordancia' / fn, encoding='utf-8')):
        if i == 0:
            continue
        p = l.rstrip('\n').split('\t')
        by[p[0]].append(p)
    return by


def heber(vers, tahot):
    t = tahot[vers]
    S = [p[1] for p in t]
    I = [i for i, s in enumerate(S) if s == 'H7121']
    J = [j for j, s in enumerate(S) if s == 'H8034']
    pairs = [(i, j) for i in I for j in J if abs(i - j) <= ABLAK]
    if not pairs:
        return 'K', 'K0_nincs_par', 'a versben nincs egymástól %d tokenen belüli H7121+H8034 pár' % ABLAK
    best = None
    for i, j in pairs:
        gloss = t[i][6].strip()
        passz = bool(PASSZIV_H.search(gloss))
        be = j > 0 and S[j - 1] == 'H9003'
        obj = 'H0853' in S[min(i, j):max(i, j) + 1]
        al = 'H5921' in S[min(i, j):max(i, j) + 4]
        isten = any(s in ISTENNEV_H for s in S[j + 1:j + 4])
        if passz:
            r = ('K', 'K1_passziv', 'passzív/megnevezett ige (%s)%s' % (gloss, '; + עַל' if al else ''))
        elif not be:
            r = ('K', 'K2_nincs_be', 'nincs בְּ-előtag a שֵׁם előtt (%s)%s' % ('megnevezés: tárgyjel H0853' if obj else 'egyéb', '; isteni névvel: HATÁRESET' if isten else ''))
        elif isten:
            r = ('A', 'A_be_isten', 'aktív קרא + בְּ + שֵׁם + isteni névszó (%s)' % gloss)
        else:
            r = ('B', 'B_be_nem_nevszo', 'aktív קרא + בְּ + שֵׁם, de isteni névszó nincs a közelben: kézi olvasás (%s)' % gloss)
        rang = {'A': 0, 'B': 1, 'K': 2}[r[0]]
        if best is None or rang < best[0]:
            best = (rang, r)
    return best[1]


def gorog(vers, tagnt):
    t = tagnt[vers]
    S = [p[1] for p in t]
    out = []
    for i, s in enumerate(S):
        if s != 'G1941':
            continue
        gloss = t[i][6]
        kozel = set(S[max(0, i - ABLAK_G):i + ABLAK_G + 1])
        if PASSZIV_G.search(gloss):
            r = ('K', 'K1_passziv', 'passzív/megnevezett (%s)' % gloss)
        elif set(S[max(0, i - ABLAK_JOGI):i + ABLAK_JOGI + 1]) & JOGI_G:
            r = ('K', 'K3_jogi', 'jogi fellebbezés: Kaisar/Szebasztosz a környezetben (%s)' % gloss)
        elif kozel & ISTEN_G:
            r = ('A', 'A_aktiv_isten', 'aktív/középigés + isteni szó a környezetben (%s)' % gloss)
        else:
            r = ('B', 'B_nincs_isten', 'aktív/középigés, de isteni szó nincs a közelben: kézi olvasás (%s)' % gloss)
        out.append(r)
    out.sort(key=lambda r: {'A': 0, 'B': 1, 'K': 2}[r[0]])
    return out[0]


def main():
    inp = [l.rstrip('\n').split('\t') for l in open(ROOT / 'naplok/F110_bemenet.tsv', encoding='utf-8')][1:]
    tahot, tagnt = beolvas('TAHOT_kivonat.tsv'), beolvas('TAGNT_kivonat.tsv')
    res = []
    for csoport, vers, _ in inp:
        r = heber(vers, tahot) if csoport.startswith('H') else gorog(vers, tagnt)
        res.append((csoport, vers) + r)
    with open(ROOT / 'naplok/F110_szuro_szimulacio.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('# GENERALT: eszkozok/f110_szuro.py | bemenet=naplok/F110_bemenet.tsv | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | a jeloltek.tsv-t nem irja\n')
        f.write('csoport\tigehely\tosztaly\tokkod\tindoklas\n')
        for r in res:
            f.write('\t'.join(r) + '\n')
    c = Counter((r[0], r[2], r[3]) for r in res)
    for k, n in sorted(c.items()):
        print(n, k)
    print({g: sum(n for k, n in c.items() if k[0] == g) for g in ('H7121+H8034', 'G1941')})


main()
