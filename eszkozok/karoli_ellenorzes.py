#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_ellenorzes.py — a régi (tartalom-alapú) Károli-szó + Strong párok ellenőrzése
a #22 gépi párosítása (adat/karoli_strong/parok_<könyv>.tsv) ellen. F65.

Ítélet soronként (elofordulasok.tsv sor: karoli_szo + strong + igehely):
  egyezik   — a sor minden Strongja előfordul a karoli_szo szavainak gépi párjai között
              ugyanazon a versen (igehely-tartományon);
  elter     — a karoli_szo szavai megvannak a versben, de a sor valamelyik Strongja nincs
              köztük (a gépi Strongok az eltéréslistába kerülnek);
  nincs_par — a karoli_szo egyetlen szava sincs a vers gépi párosításában
              (könyv hiányzik / szóalak eltér / vers hiányzik).
Az `egyezik` csak akkor `magas`, ha az egyező párok mind `magas` bizonyosságúak.

I/O: split('\\t') / '\\t'.join(), a csv modul tilos (CLAUDE.md).

Futtatás a repó gyökeréből:
    python eszkozok/karoli_ellenorzes.py --meres
    python eszkozok/karoli_ellenorzes.py --ellenorzes naplok/KAROLI_ELLENORZES_elteresek.tsv
    python eszkozok/karoli_ellenorzes.py --variancia adat/karoli_variancia.tsv
    python eszkozok/karoli_ellenorzes.py --frissit [--ir] [--motivum ID]
"""

import collections
import glob
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAROK_MINTA = os.path.join('adat', 'karoli_strong', 'parok_*.tsv')
ELOFORDULASOK = os.path.join('adat', 'elofordulasok.tsv')
JELOLTEK = os.path.join('adat', 'jeloltek.tsv')
UJ_MOD = 'szó-szintű-gépi'
REGI_MOD = 'tartalom-alapú'


def olvas(rel):
    """Tábla beolvasása: (megjegyzés-sorok, fejléc, sorok). A '#'-sorok megmaradnak."""
    with open(os.path.join(ROOT, rel), encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    return sorok


def tabla(rel):
    sorok = olvas(rel)
    i = 0
    while sorok[i].startswith('#'):
        i += 1
    # a fejléc az első nem-# sor (az elofordulasok.tsv-ben az első adatsor előtt)
    fej = sorok[i].split('\t')
    return sorok, i, fej


def token(s):
    s = s.casefold()
    return [t for t in re.findall(r"[^\W\d_]+", s)]


def strong_norm(s):
    m = re.match(r'^([HG])0*(\d+)', s.strip())
    return (m.group(1) + m.group(2).zfill(4)) if m else s.strip()


def betolt_parok():
    """vers -> [(hu_szo_token, strong, bizonyossag)]; könyv -> bizonyossag-szamlalo."""
    vers = collections.defaultdict(list)
    konyv_biz = {}
    for f in sorted(glob.glob(os.path.join(ROOT, PAROK_MINTA))):
        nev = os.path.basename(f)[len('parok_'):-4]
        c = collections.Counter()
        with open(f, encoding='utf-8', newline='') as fh:
            for l in fh:
                l = l.rstrip('\n')
                if l.startswith('#') or l.startswith('vers\t') or not l:
                    continue
                p = l.split('\t')
                vers[p[0]].append((p[2], p[5], p[6]))
                c[p[6]] += 1
        konyv_biz[nev] = c
    return vers, konyv_biz


def versek(igehely):
    """'1Móz 14:18-20' -> ['1Móz 14:18', ...]; '2Móz 19:6' -> ['2Móz 19:6']; fejezet-tartomány is."""
    m = re.match(r'^(\S+) (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$', igehely.strip())
    if not m:
        return None
    k, f1, v1, f2, v2 = m.groups()
    if v2 is None:
        return ['%s %s:%s' % (k, f1, v1)]
    if f2 is None or f2 == f1:
        return ['%s %s:%d' % (k, f1, v) for v in range(int(v1), int(v2) + 1)]
    return None  # fejezethatárt átlépő tartomány: nincs kibontva


def ellenoriz_sor(igehely, karoli_szo, strongok, vers):
    """-> (itelet, gepi_strongok_a_szavakra, bizonyossagok, megjegyzes)"""
    vl = versek(igehely)
    if vl is None:
        return 'nincs_par', [], [], 'igehely-tartomány nem bontható (%s)' % igehely
    par = [p for v in vl for p in vers.get(v, [])]
    if not par:
        return 'nincs_par', [], [], 'a vers/könyv nincs a gépi párosításban'
    toks = set(token(karoli_szo))
    talalt = [p for p in par if p[0].casefold() in toks]
    if not talalt:
        return 'nincs_par', [], [], 'a karoli_szo egyetlen szava sincs a versben'
    gepi = sorted({strong_norm(p[1]) for p in talalt})
    keresett = [strong_norm(s) for s in strongok]
    hianyzo = [s for s in keresett if s not in gepi]
    if hianyzo:
        return 'elter', gepi, sorted({p[2] for p in talalt}), 'hiányzó a gépi párokból: ' + ','.join(hianyzo)
    egyezo = [p for p in talalt if strong_norm(p[1]) in keresett]
    return 'egyezik', gepi, sorted({p[2] for p in egyezo}), ''


def regi_sorok():
    sorok, i, fej = tabla(ELOFORDULASOK)
    ix = {n: k for k, n in enumerate(fej)}
    ki = []
    for n in range(i + 1, len(sorok)):
        p = sorok[n].split('\t')
        if len(p) > ix['azonositas_modja'] and p[ix['azonositas_modja']] == REGI_MOD:
            ki.append((n, p, ix))
    return ki


def ellenorzes_futtat():
    vers, _ = betolt_parok()
    eredm = []
    for n, p, ix in regi_sorok():
        ig, szo = p[ix['igehely']], p[ix['karoli_szo']]
        st = [s for s in p[ix['strong']].split('+') if s]
        it, gepi, biz, mj = ellenoriz_sor(ig, szo, st, vers)
        eredm.append((n, p[0], ig, szo, p[ix['strong']], it, ','.join(gepi), ','.join(biz), mj))
    return eredm


def meres():
    vers, kb = betolt_parok()
    print('## bizonyossag-megoszlás könyvenként')
    for k, c in sorted(kb.items()):
        print('%s\t%s' % (k, dict(c)))
    er = ellenorzes_futtat()
    print('## elofordulasok.tsv tartalom-alapú sorok: %d' % len(er))
    print(collections.Counter(e[5] for e in er))
    kon = collections.Counter((e[2].split(' ')[0], e[5]) for e in er)
    for k in sorted(kon):
        print(k, kon[k])


def ir_eltereslista(ut):
    er = ellenorzes_futtat()
    fej = ['sor', 'id', 'igehely', 'karoli_szo', 'regi_strong', 'itelet', 'gepi_strongok', 'bizonyossag', 'megjegyzes']
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('# F65 M2: a tartalom-alapú sorok ellenőrzése a #22 gépi párosítása ellen | scope=manual | forras=adat/elofordulasok.tsv, adat/karoli_strong/parok_*.tsv | ts=manual (nem lekérdezés) | előállítás: eszkozok/karoli_ellenorzes.py\n')
        f.write('\t'.join(fej) + '\n')
        for e in er:
            f.write('\t'.join(str(x) for x in e) + '\n')
    print('írva:', ut, len(er), 'sor')


def variancia(ut):
    sz = collections.defaultdict(collections.Counter)  # (konyv,strong)->szoalak
    for f in sorted(glob.glob(os.path.join(ROOT, PAROK_MINTA))):
        k = os.path.basename(f)[len('parok_'):-4]
        with open(f, encoding='utf-8', newline='') as fh:
            for l in fh:
                l = l.rstrip('\n')
                if l.startswith('#') or l.startswith('vers\t') or not l:
                    continue
                p = l.split('\t')
                sz[(k, p[6], 'strong', strong_norm(p[5]))][p[2].casefold()] += 1
                sz[(k, p[6], 'szoalak', p[2].casefold())][strong_norm(p[5])] += 1
    return sz


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--meres':
        meres()
    elif a and a[0] == '--ellenorzes':
        ir_eltereslista(a[1])
    else:
        print(__doc__)
