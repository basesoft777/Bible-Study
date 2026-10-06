#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szamkiosztas.py -- F30 (#30): dontes- (DT), nyitott-tetel- (N) es
dontesnaplo- (D) szamok kiosztasa merge-kor.

Az agon csak helyorzo all: DT-F<nn>, N-F<nn>, D-F<nn> (tobb eseten `a`, `b`
betuvel: DT-F21a). A veglegesszamot ez az eszkoz osztja ki a main-en, a
`.github/workflows/szamkiosztas.yml` Action-bol: a helyorzok a definicios
helyuk fajlbeli sorrendjeben kapjak a kovetkezo szabad szamot, es a repo
osszes .md es .tsv fajljaban cserelodnek.

Definicios hely:
  DT-F..  a DONTESEK.md tablazatsora elso cellaja:  | DT-F21a | ...
  N-F..   a NYITOTT_FELADATOK.md felsorolasi sora:   - **N-F34b -- ...
  D-F..   a FELADATOK.md Dontesnaplo tablazatsora:   | D-F30 | ...
Olyan helyorzo, amelynek nincs definicios sora (csak hivatkozas), NEM kap
szamot, es a jelentesben "arva"-kent szerepel.

Kovetkezo szabad szam: a DONTESEK.md-ben elofordulo legnagyobb DT<n> + 1;
a NYITOTT_FELADATOK.md-ben elofordulo legnagyobb N<n> (1-3 jegyu) + 1; a
FELADATOK.md tablazatsorainak legnagyobb D<n> + 1. Kimaradt szamot nem
hasznal ujra.

Idempotens: helyorzo (definicios sor) nelkul nem valtoztat semmit.

CLI:
    python eszkozok/szamkiosztas.py --proba            # csak kiirja
    python eszkozok/szamkiosztas.py --ir               # irja a fajlokat
    python eszkozok/szamkiosztas.py --ir --uzenet-fajl commit_uzenet.txt
    python eszkozok/szamkiosztas.py --proba --gyoker KONYVTAR

Egy sor a `szamkiosztas-kihagy` jelolest tartalmazva (es a KIZART fajlok)
kimarad a cserebol: a szabalyt magyarazo dokumentumok peldai ne
cserelodjenek.
"""

import argparse
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAJL = {'DT': 'DONTESEK.md', 'N': 'NYITOTT_FELADATOK.md', 'D': 'FELADATOK.md'}

# Hatarok: elotte nem lehet betu/szam/kotojel, utana nem lehet betu/szam/kotojel.
# A kotojel utana is hatar: a briefek belso dontesnaploi `DT-F51-2`, `DT-F37-8`
# alakuak (F51 brief K0), ezek nem helyorzok -- a kotojel nelkul a sorszam elotti
# reszuk arva helyorzonek latszott, es egy kesobbi azonos nevu definicios sor
# felig atirta volna oket (konzisztencia-jelentes 2026-10-06, 2. talalat).
_HATAR_E = r'(?<![A-Za-z0-9-])'
_HATAR_U = r'(?![A-Za-z0-9-])'
HELYORZO = {
    k: re.compile(_HATAR_E + k + r'-F(\d+)([a-z]?)' + _HATAR_U)
    for k in ('DT', 'N', 'D')
}
_HELYORZO_BARMELY = re.compile(_HATAR_E + r'(?:DT|N|D)-F\d+[a-z]?' + _HATAR_U)

# definicios sor mintak (a sor elejen)
_DEF = {
    'DT': re.compile(r'^\|\s*(DT-F\d+[a-z]?)\s*\|'),
    'N': re.compile(r'^\s*(?:[-*]|\d+\.)\s*\**\s*(N-F\d+[a-z]?)' + _HATAR_U),
    'D': re.compile(r'^\|\s*(D-F\d+[a-z]?)\s*\|'),
}
_SZAM = {
    'DT': re.compile(r'\bDT(\d+)\b'),
    'N': re.compile(r'\bN(\d{1,3})\b'),
    'D': re.compile(r'^\|\s*D(\d+)\s*\|', re.M),
}

KIHAGY_JELOLES = 'szamkiosztas-kihagy'
# Oroklott helyorzok: a szabaly bevezetese (F30) elott mar a main-en allo
# helyorzok; amig itt vannak felsorolva, nem kapnak szamot (az elso kiosztas
# igy nem ir at tobb szaz sort tomegesen). A fajl torlese (vagy egy sor
# torlese) a kovetkezo futasra kiosztja a szamot. Egy sor = egy helyorzo.
OROKLOTT_FAJL = 'eszkozok/szamkiosztas_oroklott.txt'
KIZART = {
    'F30_SZAMOZAS_BRIEF.md',
    'eszkozok/szamkiosztas.py',
    'eszkozok/ellenorzes/szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_szamkiosztas.py',
}
KIZART_MAPPA = ('konkordancia/', 'generalt_proba/', '.git/')


def _olvas(ut):
    with open(ut, 'rb') as f:
        return f.read().decode('utf-8')


def _fajlok(gyoker):
    """A helyorzot tartalmazo .md/.tsv fajlok (gyokerhez viszonyitott, '/'-es utak)."""
    try:
        ki = subprocess.check_output(
            ['git', 'grep', '-l', '-I', '-E',
             r'(^|[^A-Za-z0-9-])(DT|N|D)-F[0-9]+', '--', '*.md', '*.tsv'],
            cwd=gyoker, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
        talalat = [s.strip() for s in ki.splitlines() if s.strip()]
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:       # nincs talalat
            talalat = []
        else:
            talalat = None
    except OSError:
        talalat = None
    if talalat is None or not os.path.isdir(os.path.join(gyoker, '.git')):
        talalat = []
        for mappa, almappak, fajlok in os.walk(gyoker):
            almappak[:] = [a for a in almappak if a != '.git']
            for nev in fajlok:
                if nev.endswith(('.md', '.tsv')):
                    talalat.append(os.path.relpath(os.path.join(mappa, nev), gyoker).replace(os.sep, '/'))
    return sorted(f for f in talalat
                  if f not in KIZART and not f.startswith(KIZART_MAPPA))


def _definiciok(gyoker, fajl_kulcs):
    """Rendezett, egyedi lista: a helyorzok a definicios soruk fajlbeli sorrendjeben."""
    ut = os.path.join(gyoker, FAJL[fajl_kulcs])
    if not os.path.exists(ut):
        return [], []
    lista, ketszer = [], []
    for sor in _olvas(ut).splitlines():
        m = _DEF[fajl_kulcs].match(sor)
        if not m:
            continue
        if m.group(1) in lista:
            if fajl_kulcs != 'N' and m.group(1) not in ketszer:
                ketszer.append(m.group(1))
        else:
            lista.append(m.group(1))
    return lista, ketszer


def _oroklott(gyoker):
    ut = os.path.join(gyoker, *OROKLOTT_FAJL.split('/'))
    if not os.path.exists(ut):
        return set()
    return {s.strip() for s in _olvas(ut).splitlines()
            if s.strip() and not s.lstrip().startswith('#')}


def _kovetkezo_szam(gyoker, kulcs):
    ut = os.path.join(gyoker, FAJL[kulcs])
    if not os.path.exists(ut):
        return 1
    szamok = [int(x) for x in _SZAM[kulcs].findall(_olvas(ut))]
    return (max(szamok) if szamok else 0) + 1


def terv(gyoker=ROOT):
    """Visszaad: (hozzarendeles {helyorzo: vegleges}, figyelmeztetesek [str], arvak [str])."""
    hozzarendeles, figy, arvak = {}, [], []
    mindenhol = set()
    for f in _fajlok(gyoker):
        for m in _HELYORZO_BARMELY.finditer(_olvas(os.path.join(gyoker, f))):
            mindenhol.add(m.group(0))
    oroklott = _oroklott(gyoker)
    for kulcs in ('DT', 'N', 'D'):
        defek, ketszer = _definiciok(gyoker, kulcs)
        defek = [h for h in defek if h not in oroklott]
        for h in ketszer:
            figy.append('a(z) %s helyorzo a %s fajlban tobbszor definialt (az elso sor szamit)'
                        % (h, FAJL[kulcs]))
        if not defek:
            continue
        n = _kovetkezo_szam(gyoker, kulcs)
        for h in defek:
            hozzarendeles[h] = '%s%d' % (kulcs, n)
            n += 1
    for h in sorted(mindenhol):
        if h not in hozzarendeles and h not in oroklott:
            arvak.append(h)
    return hozzarendeles, figy, arvak


def _csere_szoveg(szoveg, hozzarendeles):
    """Sorrol sorra; a kihagy-jelolesu sor valtozatlan. Visszaad: (uj_szoveg, db)."""
    db = 0

    def csere(m):
        nonlocal db
        uj = hozzarendeles.get(m.group(0))
        if uj is None:
            return m.group(0)
        db += 1
        return uj

    sorok = szoveg.splitlines(keepends=True)
    ki = []
    for sor in sorok:
        if KIHAGY_JELOLES in sor:
            ki.append(sor)
        else:
            ki.append(_HELYORZO_BARMELY.sub(csere, sor))
    return ''.join(ki), db


def alkalmaz(gyoker, hozzarendeles, ir):
    """Visszaad: {fajl: csere_db}. `ir` hamis: nem ir."""
    eredmeny = {}
    if not hozzarendeles:
        return eredmeny
    for f in _fajlok(gyoker):
        ut = os.path.join(gyoker, f)
        regi = _olvas(ut)
        uj, db = _csere_szoveg(regi, hozzarendeles)
        if db and uj != regi:
            eredmeny[f] = db
            if ir:
                with open(ut, 'wb') as fh:
                    fh.write(uj.encode('utf-8'))
    return eredmeny


def uzenet(hozzarendeles):
    return 'szamkiosztas: ' + ', '.join('%s → %s' % (h, v) for h, v in hozzarendeles.items())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--proba', action='store_true', help='csak kiirja, mit cserelne')
    g.add_argument('--ir', action='store_true', help='kiosztja a szamokat es irja a fajlokat')
    ap.add_argument('--gyoker', default=ROOT, help='a repo gyokere (alapertelmezes: ez a repo)')
    ap.add_argument('--uzenet-fajl', default=None,
                    help='--ir modban ide irja a commit-uzenetet (UTF-8), ha tortent csere')
    a = ap.parse_args()

    hozzarendeles, figy, arvak = terv(a.gyoker)
    for s in figy:
        print('FIGYELMEZTETES: ' + s)
    if arvak:
        print('Arva helyorzo (nincs definicios sor, nem kap szamot): ' + ', '.join(arvak))
    if not hozzarendeles:
        print('Nincs kiosztando helyorzo, nincs valtoztatas.')
        return 0
    print('%s kiosztas (%d helyorzo):' % ('Proba:' if a.proba else 'Kiosztas', len(hozzarendeles)))
    for h, v in hozzarendeles.items():
        print('  %s → %s' % (h, v))
    eredmeny = alkalmaz(a.gyoker, hozzarendeles, ir=a.ir)
    print('%s %d fajlt, osszesen %d cserevel:' %
          ('Erintene' if a.proba else 'Erintett', len(eredmeny), sum(eredmeny.values())))
    for f, db in sorted(eredmeny.items()):
        print('  %s (%d)' % (f, db))
    if a.ir and a.uzenet_fajl and eredmeny:
        with open(a.uzenet_fajl, 'wb') as fh:
            fh.write((uzenet(hozzarendeles) + '\n').encode('utf-8'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
