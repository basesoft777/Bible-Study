#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visszaeses_kapu.py -- „ne legyen visszaesés a régi laphoz képest” (DT952, 0. kapu): egy lap új kiadása előtt az új
és a régi (a main-en kiadott) lapot ugyanazokkal az olvasói kapukkal méri, és BUKÁS-t ad, ha az új lapon bármely
kategóriában több a találat, mint a régin.

A szerkesztő célja (2026-11-08): „fontos hogy most már visszaesés ne legyen innen”. A korábbi helyettesítő mérce (a
bájtra azonos kimenet) a régi lap hibáit is megőrizte; ez a kapu a célt méri közvetlenül: a régi lap hibáit nem kell
lemásolni, az egyezés nem cél, csak egyik olvasói hibafajtából sem lehet több.

Kategóriák (mindkét lapon ugyanazzal a szabállyal):
- az olvasói kapu (`olvasoi_kapu.lap_meres`) minden ellenőrzése azonosító és súlyosság szerint (BUKÁS és FIGYELMEZTETÉS
  külön kategória), benne a MINTA, a kerek próza (PROZA_1A, átvett), a lábjegyzet és a VISSZHANG; a darabszám a
  csoportosított találatok `db` összege;
- FORDITASRA_VAR: a „fordításra vár” előfordulása a látható szövegben (a HTML-megjegyzésen kívül).
Mindkét lap az új szerkezet szigorú szabályával mérődik (kivétel nélkül, F178.4): a régi szerkezetű lap kivett szakaszai
(Tartalomjegyzék, Jelmagyarázat, Kolofon) itt nem mentesülnek, mert az olvasó mindkét lapon mindent lát.

Használat:
    python eszkozok/visszaeses_kapu.py ID --uj UJ_LAP [--regi REGI_LAP | --regi-ref REF] [--json FAJL]
A régi lap alapból a `REF:lexikon/<ID>_TUDOMANYOS.md` (REF: `origin/main`, ha nincs, `main`).
Kilépési kód: 0 = egyik kategóriában sem több; 1 = BUKÁS (a kategóriák listájával); 2 = hívási hiba.
"""

import argparse
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import olvasoi_kapu as OK  # noqa: E402

FORDITASRA_VAR = 'FORDITASRA_VAR'
_MINDIG = re.compile('')     # az új szerkezet jele helyett: minden lap a szigorú szabállyal mérődik


def kategoriak(szoveg):
    """{kategória: darab} egy lapszövegen. A kategória `<azonosító> <súlyosság>` vagy FORDITASRA_VAR."""
    eredeti = OK.UJ_SZERKEZET_RX
    OK.UJ_SZERKEZET_RX = _MINDIG
    try:
        talalatok, _megj = OK.lap_meres(szoveg)
    finally:
        OK.UJ_SZERKEZET_RX = eredeti
    ki = {}
    for t in talalatok:
        k = '%s %s' % (t['azonosito'], t['sulyossag'])
        ki[k] = ki.get(k, 0) + t.get('db', 1)
    lathato = re.sub(r'<!--.*?-->', '', szoveg, flags=re.S)
    n = lathato.count('fordításra vár')
    if n:
        ki[FORDITASRA_VAR] = n
    return ki


def osszevet(regi_szoveg, uj_szoveg):
    """[(kategória, régi, új)] minden kategóriára (rendezve); a visszaesés az, ahol új > régi."""
    regi, uj = kategoriak(regi_szoveg), kategoriak(uj_szoveg)
    return [(k, regi.get(k, 0), uj.get(k, 0)) for k in sorted(set(regi) | set(uj))]


def visszaesesek(sorok):
    return [s for s in sorok if s[2] > s[1]]


def regi_lap(azonosito, ref=None):
    """A régi (kiadott) lap szövege a git-refből; None, ha nincs (új lap: nincs mihez mérni)."""
    utvonal = 'lexikon/%s_TUDOMANYOS.md' % azonosito
    for r in ([ref] if ref else ['origin/main', 'main']):
        p = subprocess.run(['git', 'show', '%s:%s' % (r, utvonal)], cwd=GYOKER, capture_output=True)
        if p.returncode == 0:
            return p.stdout.decode('utf-8')
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description='Az új lap visszaesése a régihez képest, az olvasói kapuk kategóriái szerint')
    ap.add_argument('id')
    ap.add_argument('--uj', required=True, help='az új lap (pl. a kiadás módban generált lexikon/<ID>_TUDOMANYOS.md)')
    ap.add_argument('--regi', help='a régi lap fájlja (alapból a --regi-ref lexikon/<ID>_TUDOMANYOS.md-je)')
    ap.add_argument('--regi-ref', help='a régi lap git-refje (alapból origin/main, ha nincs: main)')
    ap.add_argument('--json', help='a kategóriánkénti összevetés JSON-fájlba')
    a = ap.parse_args(argv)
    try:
        with open(a.uj, encoding='utf-8') as f:
            uj = f.read()
        if a.regi:
            with open(a.regi, encoding='utf-8') as f:
                regi = f.read()
        else:
            regi = regi_lap(a.id, a.regi_ref)
    except OSError as e:
        print('HIBA: %s' % e, file=sys.stderr)
        return 2
    if regi is None:
        print('NINCS RÉGI LAP\t%s\tnincs kiadott lap, nincs mihez mérni (új lap)' % a.id)
        return 0
    sorok = osszevet(regi, uj)
    rossz = visszaesesek(sorok)
    if a.json:
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'id': a.id, 'kategoriak': [{'kategoria': k, 'regi': r, 'uj': u} for k, r, u in sorok],
                       'visszaeses': [k for k, _r, _u in rossz]}, f, ensure_ascii=False, indent=1)
    for k, r, u in sorok:
        jel = 'TÖBB' if u > r else ('kevesebb' if u < r else '')
        print('%-28s régi %4d · új %4d  %s' % (k, r, u, jel))
    if rossz:
        print('BUKÁS\t%s\tvisszaesés a régi laphoz képest %d kategóriában: %s'
              % (a.id, len(rossz), ', '.join('%s (%d → %d)' % s for s in rossz)))
        return 1
    print('RENDBEN\t%s\tegyik kategóriában sincs több találat, mint a régi lapon' % a.id)
    return 0


if __name__ == '__main__':
    sys.exit(main())
