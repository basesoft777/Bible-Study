#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nevelo.py -- a magyar határozott névelő (a/az) a kiejtés szerint, számok előtt is (F175, N-F175b).

Közös segédmodul a nyílt csomagok exportereinek és kapuinak (`karoli_strong_export.py`, `karoli_modern_export.py`
és a kapuik NEVELO pontja). A szabály a felhasználó átnézése alapján (2026-11-12): „Az 598 715”, „Az 1 600”,
„az 1. kiadás”, „a 34”. Az el nem döntött „a(z)” alak hiba.
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# névelő + szám (ezres tagolással vagy anélkül, sorszámnévvel is: „az 1. kiadás”); a szám után nem állhat betű
NEVELO_SZAM_RX = re.compile(r'(?<![\w(])([Aa]z?) (\d{1,3}(?: \d{3})+|\d+)(?![\w(])')
MAGANHANGZO = 'aáeéiíoóöőuúüűAÁEÉIÍOÓÖŐUÚÜŰ'


def szam_nevelo(szam):
    """A szám elé illő névelő a kiejtés szerint: „az”, ha a kiejtés magánhangzóval kezdődik (egy, öt, ezer, ötven,
    ötszáz, egymillió…; sorszámnévként első, ötödik, ezredik…), egyébként „a”. A vezető számcsoport dönt: az 5-tel
    kezdődő csoport mindig „öt…”; az 1-gyel kezdődő akkor „egy/ezer/egymillió/első”, ha a hossza 3k+1 (1, 1 600,
    1908, 1 234 567), a 1x és 1xx „tíz/tizen/száz” (15, 150, 12 345). A tagolás nélkül írt négyjegyű szám (1908)
    egyetlen csoport, ezért ugyanez a szabály dönt róla („az 1908-as”)."""
    vezeto = szam.split(' ')[0]
    return 'az' if vezeto[0] == '5' or (vezeto[0] == '1' and len(vezeto) % 3 == 1) else 'a'


def szo_nevelo(szo):
    """A szó (vagy szám) elé illő névelő."""
    if szo[:1].isdigit():
        return szam_nevelo(szo)
    return 'az' if szo[:1] in MAGANHANGZO else 'a'


def nevelos(szo, nagy=False):
    """A szó a névelőjével („a Logosz-lexikon”, „az 598 715”); `nagy`: mondatkezdő nagybetűvel."""
    n = szo_nevelo(szo)
    return '%s %s' % (n.capitalize() if nagy else n, szo)


def nevelo_javit(szoveg):
    """Magyar szövegben a szám előtti névelőt a kiejtéshez igazítja (a nagybetűt megtartja)."""
    def csere(m):
        uj = szam_nevelo(m.group(2))
        return (uj.capitalize() if m.group(1)[0] == 'A' else uj) + ' ' + m.group(2)
    return NEVELO_SZAM_RX.sub(csere, szoveg)


def nevelo_hibak(szoveg):
    """A szám előtti hibás névelők listája (a kapuk használják), és a kiejtés szerint el nem döntött „a(z)” alak."""
    ki = ['%s %s' % (m.group(1), m.group(2)) for m in NEVELO_SZAM_RX.finditer(szoveg)
          if m.group(1).lower() != szam_nevelo(m.group(2))]
    ki += ['a(z)' for _ in re.finditer(r'\b[Aa]\(z\)', szoveg)]
    return ki
