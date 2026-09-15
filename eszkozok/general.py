#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
general.py -- F4 G1: a motivumlexikon generatorainak vaza.

Az `adat/` reteg (kanonikus igazsagforras, l. adat/SEMA.md) determinisztikus
kepe markdown-blokkokra forditva. Alapelv (F4_GENERATOR_BRIEF.md D1): a
generator elso korben SEMMIT nem ir felul -- alapertelmezesben a --kimenet
konyvtar ala termel (alapertelmezes: generalt_proba/), es a kimenet maga a
diff. Az elesites (a marker-blokkok tenyleges beirasa az eles fajlokba) kulon
tetel (G7), kulon commit, kimenetenkent emberi jovahagyas utan -- ezt a
szkript soha nem vegzi el magatol.

Ez a fajl a G1 tetel: a CLI, az --ir/--kimenet biztonsagi kapcsolo, a
TSV I/O es a marker-blokk segedfuggvenyek. A tenyleges renderelok (G3: napl
o/index) kulon tetelben, kulon commit-ban kovetkeznek.

CLI:
    python eszkozok/general.py --cel {naplo,index,naplok,study,nyitott,mind}
                               [--id ID]
                               [--kimenet DIR]      # alapertelmezes: generalt_proba/
                               [--ir]               # csak ezzel ir eles fajlba
                               [--ellenoriz]         # nem ir; diffel, 1-gyel lep ki eltéresnel

--ir nelkul a szkript SOHA nem ir eles fajlba -- csak a --kimenet konyvtar
ala. Egyik --cel sincs meg megvalositva ebben a tetelben; futtatasuk 2-es
kilepesi koddal jelzi ezt, nem hamis sikerrel.

TSV-olvasas kizarolag split('\\t')-vel, iras '\\t'.join()-nal -- a `csv` modul
importja is tilos (CLAUDE.md, "TSV-olvasas" szakasz).

Futtatas a repo gyokerebol:
    python eszkozok/general.py --cel naplo
"""

import argparse
import datetime
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
MOTIVUMOK_TSV = os.path.join(ADAT, 'motivumok.tsv')
ELOFORDULASOK_TSV = os.path.join(ADAT, 'elofordulasok.tsv')
NAPLO_MD = os.path.join(ROOT, 'motivumlog', 'PaRDeS_motivumok.md')
INDEX_MD = os.path.join(ROOT, 'Lezart_tematikus_tanulmanyok_index.md')

TS = datetime.date.today().isoformat()

# A tablaban ma nem szereplo, de a naploban mar konyvkent hasznalt ujszovetsegi
# tokenek -- csak a ma ELOFORDULO alakok, nem az osszes bibliai konyv (l. a
# konyv_teszamentum() dokumentaciojat lent).
UJSZOVETSEGI_TOKENEK = {
    '1Kor', '1Pét', '1Thessz', '2Pét', '2Tim', 'ApCsel', 'Jelenések', 'Júd',
    'Luk', 'Lukács', 'Máté', 'Róm', 'Róma', 'Zsid',
}


# ---------------------------------------------------------------------------
# TSV I/O -- split('\t') / '\t'.join(), a csv modul nem hasznalhato ezeken a
# tablakon (CLAUDE.md, "TSV-olvasas" szakasz: a mezok szabad magyar szoveget
# tartalmaznak idezojelekkel, a csv ezt idezes-szintaxisnak veszi).
# ---------------------------------------------------------------------------

def tsv_beolvas(path):
    """(fejlec:list[str], sorok:list[dict]) -- '#' elotetsorok es ures sorok kihagyva."""
    with io.open(path, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    nyers_sorok = nyers.split(sorveg)
    if nyers_sorok and nyers_sorok[-1] == '':
        nyers_sorok = nyers_sorok[:-1]
    fejlec_idx = next(i for i, s in enumerate(nyers_sorok) if s and not s.startswith('#'))
    fejlec = nyers_sorok[fejlec_idx].split('\t')
    sorok = []
    for s in nyers_sorok[fejlec_idx + 1:]:
        if not s.strip() or s.startswith('#'):
            continue
        mezok = s.split('\t')
        if len(mezok) != len(fejlec):
            raise ValueError('oszlopszám-eltérés a %s fájlban: %r' % (path, s))
        sorok.append(dict(zip(fejlec, mezok)))
    return fejlec, sorok


def sorveg_elemez(path):
    """(domináns_sorvég, crlf_db, lf_db) -- a célfájl mai sorvég-arányának mérése (K7)."""
    with io.open(path, 'rb') as f:
        adat = f.read()
    crlf = adat.count(b'\r\n')
    lf_osszes = adat.count(b'\n')
    lf = lf_osszes - crlf
    domináns = '\r\n' if crlf > lf else '\n'
    return domináns, crlf, lf


def szoveg_beolvas(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def konyv_token(igehely):
    """A vezető könyvnév-token (pl. '1Móz', 'Zsolt', 'Lukács') a fejezet:vers előtt."""
    m = re.match(r'^(\d*[^\d\s]+)', igehely)
    return m.group(1) if m else igehely


def konyv_teszamentum(token):
    """'ÓSZ' vagy 'ÚSZ' -- kizárólag a ma az elofordulasok.tsv-ben ténylegesen
    előforduló könyv-tokenek alapján (UJSZOVETSEGI_TOKENEK), nem a teljes
    bibliai kánon alapján. Ha egy jövőbeli betöltés új könyvet hoz be, ezt a
    halmazt bővíteni kell -- a szkript ezt nem találja ki magától."""
    return 'ÚSZ' if token in UJSZOVETSEGI_TOKENEK else 'ÓSZ'


# ---------------------------------------------------------------------------
# Marker-blokkok
# ---------------------------------------------------------------------------

def blokk(cel_kulcs, forras_lista, hatokor_sor, torzs):
    fejl = '<!-- GENERÁLT-KEZDET: general.py --cel %s | forrás: %s | ts=%s -->' % (
        cel_kulcs, ', '.join(forras_lista), TS)
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    return '\n\n'.join([fejl, '*%s*' % hatokor_sor, torzs, veg])


def fejlec_stampel(cel, forras_lista):
    return '<!-- GENERÁLT: general.py --cel %s | forrás: %s | ts=%s -->' % (
        cel, ', '.join(forras_lista), TS)


# ---------------------------------------------------------------------------
# Adatszervezés -- a renderelők közös segédfüggvényei
# ---------------------------------------------------------------------------

def elofordulasok_id_szerint(elofordulasok):
    csoport = {}
    for sor in elofordulasok:
        csoport.setdefault(sor['id'], []).append(sor)
    return csoport


def fo_elofordulas_csoportok(sorok):
    """Egy ID sorai közül a fo_elofordulas mező distinct értékei, a sorokban
    való első megjelenés sorrendjében (l. adat/SEMA.md 2.2.3 -- csoportkulcs,
    nem igen/nem)."""
    latott = []
    for sor in sorok:
        cs = sor.get('fo_elofordulas', '')
        if cs and cs not in latott:
            latott.append(cs)
    return latott


# ---------------------------------------------------------------------------
# Kimenet-írás
# ---------------------------------------------------------------------------

def kimenet_ir(args, relativ_ut, tartalom, forras_ut_a_sorveghez):
    domináns, crlf, lf = sorveg_elemez(forras_ut_a_sorveghez)
    print('  sorvég a célfájlban (%s): CRLF=%d, LF=%d -> domináns=%r'
          % (os.path.relpath(forras_ut_a_sorveghez, ROOT), crlf, lf, domináns))

    cel_ut = os.path.join(args.kimenet, relativ_ut)
    if args.ellenoriz:
        print('  --ellenoriz: nincs írás (az első futásnál pirosnak számít, l. §3.1).')
        return cel_ut

    os.makedirs(os.path.dirname(cel_ut), exist_ok=True)
    sorok = tartalom.split('\n')
    with io.open(cel_ut, 'w', encoding='utf-8', newline='') as f:
        f.write(domináns.join(sorok))
    print('  megírva: %s (%d bájt)' % (os.path.relpath(cel_ut, ROOT), os.path.getsize(cel_ut)))
    return cel_ut


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog='general.py',
        description='A motivumlexikon generatorai -- F4_GENERATOR_BRIEF.md.',
    )
    p.add_argument('--cel', required=True,
                    choices=['naplo', 'index', 'naplok', 'study', 'nyitott', 'mind'])
    p.add_argument('--id', help='egyetlen motívum-ID-re szűkítés (opcionális)')
    p.add_argument('--kimenet', default=os.path.join(ROOT, 'generalt_proba'),
                    help='alapértelmezés: generalt_proba/')
    p.add_argument('--ir', action='store_true',
                    help='NÉLKÜLE a szkript soha nem ír éles fájlba -- ez a kapcsoló '
                         'ebben a fázisban (G1) még nem old fel semmit, mert az '
                         'élesítés G7 külön tétele')
    p.add_argument('--ellenoriz', action='store_true',
                    help='nem ír; a generált blokkot a célfájlban álló marker-blokkal '
                         'veti össze, eltérésnél/hiánynál 1-gyel lép ki')
    return p


# Egyik --cel sincs még megvalósítva -- ez a G1 tétel csak a vázat adja. A G3
# (naplo, index) a következő commit-ban, a G5/G6 (naplok, study, nyitott) a
# 2-3. menetben készül.
MEG_NEM_KESZ = {
    'naplo': 'G3 -- a következő tételben készül (motívumnapló renderelő).',
    'index': 'G4 -- a következő tételben készül (Lezárt tanulmányok index renderelő).',
    'naplok': 'G5 -- a 2. menetben készül (kereszthivatkozás-napló renderelő).',
    'study': 'G6 -- a 2. menetben készül (tematikus study 1. pont renderelő).',
    'nyitott': 'G7 -- a 3. menetben készül (NYITOTT_FELADATOK.md blokk-generátor).',
}


def main():
    args = build_parser().parse_args()

    if args.ir:
        print('FIGYELEM: --ir kapcsoló ebben a fázisban (G1) nem old fel semmit -- '
              'az élesítés a G7 külön tétele, külön emberi jóváhagyással. A kimenet '
              'továbbra is a --kimenet könyvtár alá megy.', file=sys.stderr)

    celok = ['naplo', 'index', 'naplok', 'study', 'nyitott'] if args.cel == 'mind' else [args.cel]
    vegso_kod = 0

    for cel in celok:
        print('%s: %s' % (cel, MEG_NEM_KESZ[cel]), file=sys.stderr)
        vegso_kod = max(vegso_kod, 2)

    return vegso_kod


if __name__ == '__main__':
    sys.exit(main())
