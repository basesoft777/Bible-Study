#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a Károli–Strong párosítás pontosságmérésének kerete és rétegzett mintája.

Két kimenet:
  * f172/keret.tsv — rétegenként a pársorok száma (a mintavételi keret), a
    rétegsúly, a morféma-Strongú (H9001–H9049) és a nem-TR párok száma,
    valamint leíró számként a kimaradt `kezi` (fuggoben) tokenek és a
    párosítatlan (betoldas / forditatlan) tokenek száma a `szavak_*.tsv`-ből;
  * f172/minta.tsv — rétegenként egyszerű véletlen minta a pársorokból
    (rögzített mag; a pársorok a fájlok és a sorok rögzített sorrendjében).

Rétegek (F172 brief 2.3): ÓSZ — Mózes öt könyve (csak `alacsony`), történeti,
költői és bölcsességi, próféták; az 1–2Móz `magas` (S+C) sorai külön réteg;
ÚSZ — evangéliumok és ApCsel, levelek, Jelenések. A könyvcsoport a
F22 műfaji besorolását követi (Préd, Én, Sir a költőiekhez; Dán a prófétákhoz).

Az `adat/karoli_strong/` csak olvasott. Olvasás `split('\\t')`, írás
`'\\t'.join()` (a `csv` modul tilos, CLAUDE.md).

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong/pontossag_minta.py [--darab 200] [--mag 20261105]
    python eszkozok/karoli_strong/pontossag_minta.py --csak-keret
"""

import argparse
import os
import random
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ADAT = os.path.join(GYOKER, 'adat', 'karoli_strong')
KIMENET = os.path.join(GYOKER, 'f172')
MAG = 20261105
DARAB = 200

# fájlnév-könyv -> könyvcsoport
CSOPORT = {}
for _k in ['1Moz', '2Moz', '3Moz', '4Moz', '5Moz']:
    CSOPORT[_k] = 'OSZ_mozes'
for _k in ['Jozs', 'Bir', 'Ruth', '1Sam', '2Sam', '1Kir', '2Kir', '1Kron', '2Kron',
           'Ezsd', 'Neh', 'Eszt']:
    CSOPORT[_k] = 'OSZ_tortenet'
for _k in ['Job', 'Zsolt', 'Peld', 'Pred', 'En', 'Sir']:
    CSOPORT[_k] = 'OSZ_koltoi'
for _k in ['Ezs', 'Jer', 'Ez', 'Dan', 'Hos', 'Joel', 'Amos', 'Abd', 'Jon', 'Mik', 'Nah',
           'Hab', 'Sof', 'Hag', 'Zak', 'Mal']:
    CSOPORT[_k] = 'OSZ_profeta'
for _k in ['Mt', 'Mk', 'Luk', 'Jan', 'ApCsel']:
    CSOPORT[_k] = 'USZ_evangelium'
for _k in ['Rom', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol', '1Thessz', '2Thessz', '1Tim',
           '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pet', '2Pet', '1Jan', '2Jan', '3Jan', 'Jud']:
    CSOPORT[_k] = 'USZ_level'
CSOPORT['Jel'] = 'USZ_jelenesek'

RETEGEK = ['OSZ_mozes_magas', 'OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta',
           'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']

MINTA_FEJ = ['minta_id', 'reteg', 'konyv', 'vers', 'hu_sorszam', 'hu_szo', 'er_sorszam',
             'er_szo', 'strong', 'bizonyossag', 'forras', 'morfema', 'nem_tr']


def _tabla(ut):
    """(fejléc, sorok) — a `#`-kezdetű sorokat átugorja."""
    fej, sorok = None, []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
            else:
                sorok.append(dict(zip(fej, m)))
    return fej, sorok


def konyvek():
    ki = sorted(f[len('parok_'):-len('.tsv')] for f in os.listdir(ADAT)
                if f.startswith('parok_') and f.endswith('.tsv'))
    hiany = [k for k in ki if k not in CSOPORT]
    if hiany:
        raise SystemExit('ismeretlen könyv(ek) a keretben: %s' % ', '.join(hiany))
    return ki


def nem_tr_kulcsok():
    _, sorok = _tabla(os.path.join(ADAT, 'nem_tr_parositott.tsv'))
    return {(r['vers'], r['er_sorszam']) for r in sorok}


def reteg_of(konyv, bizonyossag):
    cs = CSOPORT[konyv]
    if cs == 'OSZ_mozes' and bizonyossag == 'magas':
        return 'OSZ_mozes_magas'
    return cs


def keret_parok():
    """A mintavételi keret: minden pársor a rétegével, rögzített sorrendben."""
    ntr = nem_tr_kulcsok()
    ki = []
    for k in konyvek():
        _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            s = r['strong']
            ki.append({
                'reteg': reteg_of(k, r['bizonyossag']), 'konyv': k, 'vers': r['vers'],
                'hu_sorszam': r['hu_sorszam'], 'hu_szo': r['hu_szo'],
                'er_sorszam': r['er_sorszam'], 'er_szo': r['er_szo'], 'strong': s,
                'bizonyossag': r['bizonyossag'], 'forras': r['forras'],
                'morfema': '1' if (s.startswith('H90') and len(s) == 5) else '0',
                'nem_tr': '1' if (r['vers'], r['er_sorszam']) in ntr else '0',
            })
    return ki


def szavak_leiro():
    """Rétegenként (könyvcsoport szerint) a kezi és a párosítatlan tokenek száma."""
    ki = {}
    for k in konyvek():
        cs = CSOPORT[k]
        d = ki.setdefault(cs, {'hu': 0, 'er': 0, 'betoldas': 0, 'forditatlan': 0,
                               'fuggoben': 0, 'kezi_vers': set()})
        _, sorok = _tabla(os.path.join(ADAT, 'szavak_%s.tsv' % k))
        for r in sorok:
            d[r['oldal']] = d.get(r['oldal'], 0) + 1
            a = r['allapot']
            if a in ('betoldas', 'forditatlan', 'fuggoben'):
                d[a] += 1
            if a == 'fuggoben':
                d['kezi_vers'].add(r['vers'])
    return ki


def mintavetel(keret, darab=DARAB, mag=MAG):
    """Rétegenként egyszerű véletlen minta (rétegenként saját, a magból
    származtatott generátor, így egy réteg mérete nem hat a többire)."""
    reteg_sorok = {}
    for r in keret:
        reteg_sorok.setdefault(r['reteg'], []).append(r)
    ki = []
    for i, rt in enumerate(RETEGEK):
        sorok = reteg_sorok.get(rt, [])
        rnd = random.Random('%d:%s' % (mag, rt))
        n = min(darab, len(sorok))
        idx = sorted(rnd.sample(range(len(sorok)), n))
        for j, x in enumerate(idx):
            r = dict(sorok[x])
            r['minta_id'] = '%s-%03d' % (rt, j + 1)
            ki.append(r)
    return ki


def git_head():
    try:
        return subprocess.check_output(['git', '-C', GYOKER, 'rev-parse', '--short', 'HEAD'],
                                       text=True).strip()
    except Exception:
        return 'ismeretlen'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--darab', type=int, default=DARAB)
    ap.add_argument('--mag', type=int, default=MAG)
    ap.add_argument('--csak-keret', action='store_true')
    a = ap.parse_args()

    os.makedirs(KIMENET, exist_ok=True)
    keret = keret_parok()
    leiro = szavak_leiro()
    head = git_head()
    ossz = len(keret)

    szam = {}
    for r in keret:
        d = szam.setdefault(r['reteg'], {'n': 0, 'morfema': 0, 'nem_tr': 0, 'versek': set()})
        d['n'] += 1
        d['morfema'] += int(r['morfema'])
        d['nem_tr'] += int(r['nem_tr'])
        d['versek'].add(r['vers'])

    prov = ('# MANUAL: scope=F172 mintavételi keret (adat/karoli_strong/parok_*.tsv pársorai) | '
            'forras=adat/karoli_strong/parok_*.tsv, szavak_*.tsv, nem_tr_parositott.tsv @ %s | '
            'ts=git:%s | manual (determinisztikus számlálás; a párok modell-kimenet, javaslat) | '
            'a kezi/betoldas/forditatlan/fuggoben oszlopok könyvcsoport-szintűek, leíró számok' % (head, head))
    with open(os.path.join(KIMENET, 'keret.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(['reteg', 'parsor', 'suly', 'versek', 'morfema_par', 'nem_tr_par',
                           'csoport_hu_token', 'csoport_er_token', 'csoport_betoldas',
                           'csoport_forditatlan', 'csoport_fuggoben', 'csoport_kezi_vers']) + '\n')
        for rt in RETEGEK:
            d = szam.get(rt, {'n': 0, 'morfema': 0, 'nem_tr': 0, 'versek': set()})
            cs = 'OSZ_mozes' if rt == 'OSZ_mozes_magas' else rt
            lw = leiro.get(cs, {})
            # a könyvcsoport leíró számai csak a csoport első rétegsorán állnak
            if rt == 'OSZ_mozes_magas':
                lw_s = ['', '', '', '', '', '']
            else:
                lw_s = [str(lw.get('hu', 0)), str(lw.get('er', 0)), str(lw.get('betoldas', 0)),
                        str(lw.get('forditatlan', 0)), str(lw.get('fuggoben', 0)),
                        str(len(lw.get('kezi_vers', ())))]
            f.write('\t'.join([rt, str(d['n']), '%.6f' % (d['n'] / ossz), str(len(d['versek'])),
                               str(d['morfema']), str(d['nem_tr'])] + lw_s) + '\n')
        f.write('\t'.join(['OSSZES', str(ossz), '1.000000',
                           str(len({r['vers'] for r in keret})),
                           str(sum(int(r['morfema']) for r in keret)),
                           str(sum(int(r['nem_tr']) for r in keret))] + [''] * 6) + '\n')
    print('keret: %d pársor, %d réteg -> f172/keret.tsv' % (ossz, len(szam)))
    for rt in RETEGEK:
        d = szam.get(rt)
        print('  %-16s %7d  (%.2f%%)  morféma %d' % (rt, d['n'], 100.0 * d['n'] / ossz, d['morfema']))

    if a.csak_keret:
        return
    minta = mintavetel(keret, a.darab, a.mag)
    prov = ('# MANUAL: scope=F172 rétegzett minta (rétegenként %d pársor, mag=%d) | '
            'forras=f172/keret.tsv, adat/karoli_strong/parok_*.tsv @ %s | ts=git:%s | '
            'manual (determinisztikus mintavétel; a párok modell-kimenet, javaslat)' % (a.darab, a.mag, head, head))
    with open(os.path.join(KIMENET, 'minta.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(MINTA_FEJ) + '\n')
        for r in minta:
            f.write('\t'.join(r[k] for k in MINTA_FEJ) + '\n')
    print('minta: %d pársor -> f172/minta.tsv' % len(minta))


if __name__ == '__main__':
    main()
