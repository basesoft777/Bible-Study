#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/forditas_kapuk.py -- F28_EMELES_BRIEF.md E3: a teljes szotari
szocikk-forditasok (Thayer, BDB) gepi kapui, az fp2/kapuk.py alapjan.

Az fp2/kapuk.py a naplok/FORDITAS_P4_ellenoriz.py fuggvenyeit importalja;
ez a modul ugyanigy tesz (1-6. ellenorzes), es hozzaadja a brief harom uj
kapujat:

  idezojel   az idezojel-parok szama egyezik (forras: ASCII " / 2 + “;
             forditas: „ + » nyito jelek)
  tagolas    a jelentesszamok es betujelek (1., 2., a., b., α., I., II.)
             sorozata azonos -- enelkul a render nem tud jelentest kivagni
  torzs      (csak BDB) az igetorzs-cimkek (Qal, Niph., Pi., Pu., Hiph.,
             Hoph., Hithp. es a ritkabbak) azonos sorrendben

Eredmeny: RENDBEN | SERTES | JELZES. A SERTES kapuhiba (E4: egy
onujraproba, utana naplok/EMELES_bukottak.tsv); a JELZES (hosszarany)
nem gatol.

Konyvtarkent:

    from forditas_kapuk import kapuk_futtat
    eredmenyek = kapuk_futtat('BDB', forras, forditas, bizonytalan=[])

Parancssorbol (fajlon at):

    python eszkozok/forditas_kapuk.py --szotar BDB --forras f.txt --forditas h.txt
"""

import argparse
import importlib.util
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_spec = importlib.util.spec_from_file_location(
    'forditas_p4_ellenoriz', os.path.join(REPO, 'naplok', 'FORDITAS_P4_ellenoriz.py'))
_p4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_p4)

TERMINOLOGIA_UT = os.path.join(REPO, 'adat', 'terminologia.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

GATOLO = ['1_gorog_heber', '2_versszam', '3_karoli_roviditesek', '4_formazas',
          '5_terminologia', '8_idezojel', '9_tagolas', '10_torzs']


# ---------------------------------------------------------------------------
# idezojel
# ---------------------------------------------------------------------------

def idezojel_parok_forras(szoveg):
    return szoveg.count('"') // 2 + szoveg.count('“')


def idezojel_parok_forditas(szoveg):
    return szoveg.count('„') + szoveg.count('»')


def ellenoriz_idezojel(forras, forditas):
    a, b = idezojel_parok_forras(forras), idezojel_parok_forditas(forditas)
    if a == b:
        return 'RENDBEN', '%d par' % a
    reszlet = 'forras %d par, forditas %d par' % (a, b)
    if forras.count('"') % 2:
        reszlet += ' (a forras ASCII-idezojeleinek szama paratlan: %d)' % forras.count('"')
    return 'SERTES', reszlet


# ---------------------------------------------------------------------------
# tagolas
# ---------------------------------------------------------------------------

# Tagolas-jelolok. A forras oldalon szukebb, a forditas oldalon tagabb a
# kinyeres, es a kapu RESZSOROZATOT vizsgal: a forras minden jelolojenek
# a forras sorrendjeben meg kell jelennie a forditasban. A forditas
# hozzaadhat sorszamneveket (a magyar `14. §`, `835. o.`, `VIII. kötet`,
# `1. aorisztosz` nem forrasbeli tagolas), de forrasjelolot nem hagyhat el
# es nem cserelhet fel -- a render ezekre vag.
#
#   pontozott szam:    1.  2.          (elotte szokoz/sorkezdet/—/( , utana szokoz)
#   pont nelkuli szam: 3 proclaim      (BDB; elotte `. `, `; `, `: `, `— `, `) `,
#                                       utana kisbetus szo, de nem nyelvtani cimke)
#   betujel:           a.  b.          (a-i; elotte szokoz; nem `i. e.`, `e. g.`,
#                                       nem `c. 100` = circa)
#   romai:             I.  II.         (nem `A. V.` / `R. V.`)
#   zarojeles:         (1) (α) (I)

_PONT_SZAM = re.compile(r'(?:(?<=^)|(?<=[\s(—]))(\d{1,2})\.(?=\s)')
_SZAM_PONT_NELKUL = re.compile(r'(?<=[.;:—)] )(\d{1,2})(?= ([a-zá-ű]\w*))')
_BETU = re.compile(r'(?:(?<=^)|(?<=\s))([a-i])\.(?=\s)')
_ROMAI = re.compile(r'(?:(?<=^)|(?<=[\s(—]))([IVX]{1,4})\.(?=[\s,;)])')
_ZAROJELES = re.compile(r'\(([α-ω]|\d{1,2}|[IVX]{1,4})\)')

# a pont nelkuli szam utan allo nyelvtani cimkek (a forras BDB-alakjai): ezek
# nem tagolas (`3 feminine singular`, `2 accusative`)
_NYELVTANI = {'masculine', 'feminine', 'singular', 'plural', 'accusative', 'person',
              'common', 'dual', 'times', 't'}
_HIVATKOZAS_ELOTAG = re.compile(r'(?:\bp|\bpp|\bvol|\bNo|\bed|§)\.? $')


def _jelolok(szoveg, forras_oldal):
    talalat = []  # (pozicio, jel)
    for m in _PONT_SZAM.finditer(szoveg):
        talalat.append((m.start(), m.group(1)))
    for m in _SZAM_PONT_NELKUL.finditer(szoveg):
        if forras_oldal and m.group(2).lower() in _NYELVTANI:
            continue
        if forras_oldal and _HIVATKOZAS_ELOTAG.search(szoveg[max(0, m.start() - 6):m.start()]):
            continue  # p. 27 c., vol. 2 -- oldal-/kotetszam, nem tagolas
        talalat.append((m.start(), m.group(1)))
    for m in _BETU.finditer(szoveg):
        jel = m.group(1)
        utana = szoveg[m.end():m.end() + 4].lstrip()
        elotte = szoveg[max(0, m.start() - 3):m.start()]
        if jel == 'e' and (elotte.endswith('i. ') or utana.startswith('g.')):
            continue  # i. e. / e. g.
        if jel == 'i' and utana.startswith('e.'):
            continue  # i. e.
        if jel == 'c' and utana[:1].isdigit():
            continue  # c. 100 = circa
        talalat.append((m.start(), jel))
    for m in _ROMAI.finditer(szoveg):
        elotte = szoveg[max(0, m.start() - 3):m.start()]
        if m.group(1) == 'V' and elotte in ('A. ', 'R. '):
            continue  # A. V. / R. V.
        talalat.append((m.start(), m.group(1)))
    for m in _ZAROJELES.finditer(szoveg):
        talalat.append((m.start(), '(%s)' % m.group(1)))
    return [j for _, j in sorted(talalat)]


def tagolas_sorozat(szoveg):
    """A forras tagolas-jeloloi, sorrendben."""
    return _jelolok(szoveg, forras_oldal=True)


def tagolas_sorozat_forditas(szoveg):
    return _jelolok(szoveg, forras_oldal=False)


def ellenoriz_tagolas(forras, forditas):
    a = tagolas_sorozat(forras)
    b = tagolas_sorozat_forditas(forditas)
    j = 0
    for i, jel in enumerate(a):
        while j < len(b) and b[j] != jel:
            j += 1
        if j == len(b):
            return 'SERTES', ('a forras %d jelolojebol a(z) %d. (%s) nem talalhato a forditasban a helyen; '
                              'kornyezet a forrasban: %s'
                              % (len(a), i + 1, jel, ' '.join(a[max(0, i - 3):i + 3])))
        j += 1
    return 'RENDBEN', '%d forrasjelolo (forditas %d)' % (len(a), len(b))


# ---------------------------------------------------------------------------
# torzs (BDB)
# ---------------------------------------------------------------------------

TORZS_MINTA = re.compile(
    r'(?<![A-Za-z])'
    r'(Qal|Niph(?:al)?|Pi(?:el)?|Pu(?:al)?|Hiph(?:il)?|Hoph(?:al)?|Hithp(?:a(?:el|lpel)|o(?:lel|el)|eel|ael)?'
    r'|Hithpo|Hishtaph(?:el)?|Pilp(?:el)?|Pilel|Pulal|Pol(?:el|al)?|Po(?:el|al)?|Pōʿ(?:ēl|al)|Pōl(?:ēl|al)'
    r'|Palp(?:al)?|Pealal|Tiph(?:el)?|Nithp(?:ael)?)'
    r'(?![A-Za-z])')


def torzs_sorozat(szoveg):
    return [m.group(1)[:4] for m in TORZS_MINTA.finditer(szoveg)]


def ellenoriz_torzs(forras, forditas):
    a, b = torzs_sorozat(forras), torzs_sorozat(forditas)
    if a == b:
        return 'RENDBEN', ' '.join(a)
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return 'SERTES', ('forras %d cimke, forditas %d cimke; elso elteres a %d. cimkenel: forras %s | forditas %s'
                      % (len(a), len(b), i + 1,
                         ' '.join(a[i:i + 6]) or '-', ' '.join(b[i:i + 6]) or '-'))


# ---------------------------------------------------------------------------
# osszes kapu
# ---------------------------------------------------------------------------

_KAROLI = None
_TERM = None


def _betolt():
    global _KAROLI, _TERM
    if _KAROLI is None:
        _KAROLI = {r['Magyar rövidítés'] for r in _p4.tsv_dict_sorok(KAROLI_UT)}
        _TERM = list(_p4.tsv_dict_sorok(TERMINOLOGIA_UT))
    return _KAROLI, _TERM


def kapuk_futtat(szotar, forras, forditas, bizonytalan=()):
    """[(nev, eredmeny, reszlet), ...]"""
    karoli, term = _betolt()
    ki = [
        ('1_gorog_heber',) + _p4.ellenoriz_1_gorog_heber(forras, forditas),
        ('2_versszam',) + _p4.ellenoriz_2_versszam(forras, forditas),
        ('3_karoli_roviditesek',) + _p4.ellenoriz_3_karoli_roviditesek(forditas, karoli),
        ('4_formazas',) + _p4.ellenoriz_4_formazas(forras, forditas),
        ('5_terminologia',) + _p4.ellenoriz_5_terminologia(forras, forditas, term, list(bizonytalan)),
        ('6_hosszarany',) + _p4.ellenoriz_6_hosszarany(forras, forditas),
        ('8_idezojel',) + ellenoriz_idezojel(forras, forditas),
        ('9_tagolas',) + ellenoriz_tagolas(forras, forditas),
    ]
    if szotar == 'BDB':
        ki.append(('10_torzs',) + ellenoriz_torzs(forras, forditas))
    return ki


def atment(eredmenyek):
    return all(e != 'SERTES' for n, e, _ in eredmenyek if n in GATOLO)


def main():
    ap = argparse.ArgumentParser(description='F28 E3 forditasi kapuk')
    ap.add_argument('--szotar', required=True, choices=['Thayer', 'BDB'])
    ap.add_argument('--forras', required=True)
    ap.add_argument('--forditas', required=True)
    args = ap.parse_args()
    with open(args.forras, encoding='utf-8') as fh:
        forras = fh.read()
    with open(args.forditas, encoding='utf-8') as fh:
        forditas = fh.read()
    eredm = kapuk_futtat(args.szotar, forras, forditas)
    for n, e, r in eredm:
        print('%-22s %-8s %s' % (n, e, r))
    print('ATMENT' if atment(eredm) else 'BUKOTT')
    sys.exit(0 if atment(eredm) else 1)


if __name__ == '__main__':
    main()
