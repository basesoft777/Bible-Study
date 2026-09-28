#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/apparatus_elemzes.py -- a "levalaszthato" reszek (zarojeles
szakirodalmi/klasszikus hivatkozas, igehely, kezirat-szigla) arany a teljes
Thayer korpuszon, atfedes nelkul szamolva (a felhasznalo korabbi kiegeszito
kerdese, a 7. lepeshez).

    python fp2/apparatus_elemzes.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')

# 1. zarojeles (nem egymasba agyazott) szakaszok -- szakirodalmi/klasszikus
#    hivatkozasok tobbsege ide esik (pl. "(Plato, legg. 2, 664 c.)")
ZAROJEL_MINTA = re.compile(r'\([^()]*\)')

# 2. igehely-hivatkozasok: konyvroviditas + fejezet:vers, tobbszoros
#    felsorolassal (pl. "Mat 24:12", "1Co 13:1-4, 1Co 13:8")
IGEHELY_MINTA = re.compile(
    r'\b[1-4]?[A-Z][a-zA-Z]*\.?\s*\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?(?:,\s*(?:[1-4]?[A-Z][a-zA-Z]*\.?\s*)?\d{1,3}(?::\d{1,3})?(?:[-–]\d{1,3})?)*'
)

# 3. kritikai-apparatus sziglak, onallo tokenkent
SZIGLA_MINTA = re.compile(r'\b(?:L|T|Tr|WH|Rec\.|R|G)\b')

# gorog/heber betus szakasz -- az ezt tartalmazo egyesitett apparatus-ivet
# KI KELL VENNI a "levalaszthato" mennyisegbol, mert a forras gorog/hebert
# szo szerint meg kell orizni (nem tehato helyorzo moge)
GOROG_HEBER_MINTA = re.compile(r'[Ͱ-Ͽἀ-῿]+|[֐-׿]+')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def _egyesitett_hossz(szoveg, mintak):
    intervallumok = []
    for minta in mintak:
        for m in minta.finditer(szoveg):
            if m.end() > m.start():
                intervallumok.append((m.start(), m.end()))
    if not intervallumok:
        return 0
    intervallumok.sort()
    egyesitett = [intervallumok[0]]
    for s, e in intervallumok[1:]:
        us, ue = egyesitett[-1]
        if s <= ue:
            egyesitett[-1] = (us, max(ue, e))
        else:
            egyesitett.append((s, e))
    return sum(e - s for s, e in egyesitett)


def _egyesitett_hossz_gorog_nelkul(szoveg, mintak):
    intervallumok = []
    for minta in mintak:
        for m in minta.finditer(szoveg):
            if m.end() > m.start():
                intervallumok.append([m.start(), m.end()])
    if not intervallumok:
        return 0
    intervallumok.sort()
    egyesitett = [intervallumok[0]]
    for s, e in intervallumok[1:]:
        if s <= egyesitett[-1][1]:
            egyesitett[-1][1] = max(egyesitett[-1][1], e)
        else:
            egyesitett.append([s, e])
    hossz = 0
    for s, e in egyesitett:
        if GOROG_HEBER_MINTA.search(szoveg[s:e]):
            continue  # gorog/heber tartalmu iv -- nem levalaszthato
        hossz += e - s
    return hossz


def main():
    thayer = [r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)]
    teljes_karakter = sum(len(t) for t in thayer)

    kulon_hosszak = {'zarojel': 0, 'igehely': 0, 'szigla': 0}
    egyesitett_osszesen = 0
    egyesitett_gorog_nelkul = 0
    for szoveg in thayer:
        kulon_hosszak['zarojel'] += sum(m.end() - m.start() for m in ZAROJEL_MINTA.finditer(szoveg))
        kulon_hosszak['igehely'] += sum(m.end() - m.start() for m in IGEHELY_MINTA.finditer(szoveg))
        kulon_hosszak['szigla'] += sum(m.end() - m.start() for m in SZIGLA_MINTA.finditer(szoveg))
        egyesitett_osszesen += _egyesitett_hossz(szoveg, [ZAROJEL_MINTA, IGEHELY_MINTA, SZIGLA_MINTA])
        egyesitett_gorog_nelkul += _egyesitett_hossz_gorog_nelkul(
            szoveg, [ZAROJEL_MINTA, IGEHELY_MINTA, SZIGLA_MINTA])

    print('=== "levalaszthato" apparatus-reszek arany a teljes Thayer korpuszon ===')
    print('teljes korpusz karakter:', teljes_karakter)
    for nev, h in kulon_hosszak.items():
        print('  %-10s onmagaban: %8d kar. (%.1f%%)' % (nev, h, 100 * h / teljes_karakter))
    print('  EGYESITETT (atfedes nelkul): %8d kar. (%.1f%%)'
          % (egyesitett_osszesen, 100 * egyesitett_osszesen / teljes_karakter))
    print('  EGYESITETT, GOROG/HEBER NELKUL (a valodi levalaszthato resz): %8d kar. (%.1f%%)'
          % (egyesitett_gorog_nelkul, 100 * egyesitett_gorog_nelkul / teljes_karakter))


if __name__ == '__main__':
    main()
