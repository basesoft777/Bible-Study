#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wlc_versek.py -- F41 (FELADATOK #41): a WLC (masszoreta) versszamozas gepi forrasa: a konkordancia/Macula_heber_*.tsv tablak (Macula Hebrew,
`ref` oszlop = 'GEN 1:1!1', a Macula (MT/WLC) szamozas; a `karoli` oszlopot NEM hasznaljuk, az KK-alapu Karoli-megfeleltetes).

Kozos modul: a bsb_import.py (a Pred/Ezs fejezethatar-igazolasa) es a bsb_wlc_versszam_ellenorzes.py hasznalja. Csak olvas; csv nelkul (split('\\t')).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# A Macula-kodok a Konyv_normalizalo_tabla elso 39 sorának (OSZ, kanonikus) sorrendjeben (a fajlnevek: eszkozok/f17/macula_import.py HEBER_KONYV_FAJL)
MACULA_KODOK = ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB',
                'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP',
                'HAG', 'ZEC', 'MAL']
MACULA_FAJL = {'GEN': 'Genezis', 'EXO': 'Exodus', 'LEV': 'Leviticus', 'NUM': 'Numeri', 'DEU': 'Deuteronomium',
               'JOS': 'Jozsue', 'JDG': 'Birak', 'RUT': 'Ruth', '1SA': 'Samuel_1', '2SA': 'Samuel_2',
               '1KI': 'Kiralyok_1', '2KI': 'Kiralyok_2', '1CH': 'Kronikak_1', '2CH': 'Kronikak_2',
               'EZR': 'Ezsdras', 'NEH': 'Nehemias', 'EST': 'Eszter', 'JOB': 'Job', 'PSA': 'Zsoltarok',
               'PRO': 'Peldabeszedek', 'ECC': 'Predikator', 'SNG': 'Enekek_Eneke', 'ISA': 'Ezsaias',
               'JER': 'Jeremias', 'LAM': 'Siralmak', 'EZK': 'Ezekiel', 'DAN': 'Daniel', 'HOS': 'Hoseas',
               'JOL': 'Joel', 'AMO': 'Amos', 'OBA': 'Abdias', 'JON': 'Jonas', 'MIC': 'Mikeas', 'NAM': 'Nahum',
               'HAB': 'Habakuk', 'ZEP': 'Sofonias', 'HAG': 'Aggeus', 'ZEC': 'Zakarias', 'MAL': 'Malakias'}

_REF = re.compile(r'(\w+) (\d+):(\d+)')


def macula_kod(step):
    """A Konyv_normalizalo_tabla STEP-kodjabol (pl. 'Gen', '1Sa') a Macula-kod (pl. 'GEN', '1SA'), az OSZ-konyvek kanonikus sorrendje szerint."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))
    lista = [s[0] for s in sorok[:39]]
    return MACULA_KODOK[lista.index(step)]


def wlc_konyv(kod):
    """{(fejezet, vers): set(Strong-szam int)}: a Macula-tabla `strong` oszlopa (H-szamok, a 9000-es prefixkodok nelkul). Az ures Strongu
    morfemak (pl. 'וְ' kotoszo) nem szamitanak, de a vers akkor is bekerul (ures halmazzal), ha minden szava ilyen."""
    ut = os.path.join(kozos.KONKORDANCIA, 'Macula_heber_%s.tsv' % MACULA_FAJL[kod])
    ki = {}
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('xml_id'):
                continue
            p = sor.rstrip('\n').split('\t')
            if len(p) < 8:
                continue
            m = _REF.match(p[1])
            if not m or m.group(1) != kod:
                continue
            kulcs = (int(m.group(2)), int(m.group(3)))
            h = ki.setdefault(kulcs, set())
            if p[7].startswith('H'):
                n = kozos.strong_szam(p[7])
                if n is not None and n < 9000:
                    h.add(n)
    return ki


def wlc_fejezet_max(wlc):
    """{fejezet: max vers}."""
    ki = {}
    for (f, v) in wlc:
        ki[f] = max(ki.get(f, 0), v)
    return ki


def vers_egyezik(wlc_halmaz, bsb_halmaz):
    """Versszintu szamozas-igazolas (F41, DT-F41f): igaz, ha a WLC-vers (nem ures) Strong-halmazanak TOBB MINT FELE a BSB-vers (Igehely-vers sorai) halmazaban van
    (azonos modszer, mint a bsb_import.versillesztes: hanyad > 0,5). A BSB-halmaz 9000-es prefixkodjai nem szamitanak."""
    if not wlc_halmaz:
        return False
    b = {n for n in bsb_halmaz if n < 9000}
    return len(wlc_halmaz & b) / len(wlc_halmaz) > 0.5
