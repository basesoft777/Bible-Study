#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENKOR_dt569_igazolas.py -- a kiadott lapokon a kézi rész szövege nem változott-e (DT569; F123.GENKOR 5. lépés).

A `INDOKLAS_dt569_igazolas.py` a kézi részben álló minden változást kiírja. Az F123.GENKOR három generátor-változása
a kézi rész sorait is érinti, de a szövegüket nem:
    (1) a címsor „*(kézi)*” / „*(generált)*” jelölése lekerül (DT-F181c);
    (2) a rés generált olvasói bevezetője (a `<!-- olvasói -->` jelű sor) „A kutató írta.” nélkül áll (DT-F181c);
    (3) a szó és a kiejtés mellett álló Strong-szám jelölt alakra íródik (hivatkozás + felső index, DT-F181b).
Ez a szkript a két oldal kézi sorait ezek visszafordításával normalizálja (a jelölt Strong-alakot a forrás „kiejtés,
H4196” alakjára, a címsort jelölés nélkülire, az olvasói bevezetőt kihagyja), és a normalizált kézi sorokat veti össze.
Kilépési kód 1, ha a kézi részben ezeken túli változás van. Csak olvas.

    python naplok/GENKOR_dt569_igazolas.py [--rev REV] [ID ...]    # alapból: ISTENTISZT-001 ALVIL-001 ANTROP-001
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
sys.path.insert(0, os.path.join(os.path.dirname(ITT), 'eszkozok'))
import INDOKLAS_dt569_igazolas as I  # noqa: E402
import kiejtes_szoveg as KSZ  # noqa: E402

CIMJEL = re.compile(r' ?\*\((?:kézi|generált)(?:, ha van)?\)\*')
JELOLT = re.compile(r'\[([^\]]*)\]\(/szo/([HG]\d{4}[a-z]?)\)(\**)<sup class="strong"[^>]*>[^<]*</sup>')


def normal(sor):
    if re.match(r'^#{1,6}\s', sor):
        sor = CIMJEL.sub('', sor).rstrip()
    # „[mizbéah](/szo/H4196)<sup …>H4196</sup>” → „mizbéah, H4196”; a szó előtti zárójeles alak („ὄνομα (G3686)”)
    # és a szó előtti szám („H6089 עֶצֶב”) visszafordítása nem egyértelmű, ezért a szám nélküli szó a közös alak
    sor = JELOLT.sub(lambda m: m.group(1) + m.group(3), sor)
    sor = re.sub(r'\s?\((?:[HG]\d{4}[a-z]?)\)', '', sor)                         # „ὄνομα (G3686)”
    sor = re.sub(r',\s*(?<![\w+/])[HG]\d{4}[a-z]?(?![\w+/])(?=\s*[),;])', '', sor)  # „(kiejtés, H4196)”
    sor = re.sub(r'(?<=\w)\s+[HG]\d{4}[a-z]?(?=\))', '', sor)                    # „(szó, epikaleó G1941)”
    return re.sub(r'(?<![\w+/])[HG]\d{4}[a-z]?\s+(?=[֐-׿Ͱ-Ͽἀ-῿])', '', sor)         # „H6089 עֶצֶב”


def kezi_sorok(sorok):
    reszek = KSZ._sor_reszek(sorok)
    return [normal(s) for s, (gen, _f, _sz) in zip(sorok, reszek)
            if not gen and not s.rstrip().endswith('<!-- olvasói -->')]


def main():
    arg = sys.argv[1:]
    rev = 'origin/main'
    if arg[:1] == ['--rev']:
        rev, arg = arg[1], arg[2:]
    hiba = 0
    print('lap\tkézi sor (régi / új)\tnormalizálva eltér')
    for mid in arg or I.KIADOTT:
        regi, uj = kezi_sorok(I.szoveg(mid, rev)), kezi_sorok(I.szoveg(mid))
        elter = [(a, b) for a, b in zip(regi, uj) if a != b]
        if len(regi) != len(uj):
            elter.append(('(sorszám: %d)' % len(regi), '(sorszám: %d)' % len(uj)))
        print('%s\t%d / %d\t%d' % (mid, len(regi), len(uj), len(elter)))
        for a, b in elter[:10]:
            print('   régi: %s\n   új:   %s' % (a[:160], b[:160]))
        hiba |= bool(elter)
    return 1 if hiba else 0


if __name__ == '__main__':
    sys.exit(main())
