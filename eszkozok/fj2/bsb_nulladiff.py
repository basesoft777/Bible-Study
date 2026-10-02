#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_nulladiff.py -- F41 (FELADATOK #41, G6): a konkordancia/BSB_Strongs.tsv NULLA-DIFF igazolasa az erintetlen konyvekre.

Az alap (regi allapot) a `git show <alap>:konkordancia/BSB_Strongs.tsv` (alapertelmezett: main), az uj a munkafa fajlja. Mit vizsgal (mind split('\\t'), csv nelkul):
  1. FEJLEC: a regi fejlec oszlopai az ujban azonos neven, azonos sorrendben az elejen allnak (az uj fajl ketto tovabbi oszlopot kapott: `Angol szó állapota`, `Számozás`).
  2. KONYVSORREND: a regi fajl konyvei az ujban ugyanabban a relativ sorrendben allnak.
  3. ERINTETLEN KONYVEK: a konyv minden sora (a regi fajl MIND AZ OT oszlopa) bajtra azonos, ugyanabban a sorrendben; az uj ket oszlop ertekei ervenyesek
     (Angol szó állapota: forditva / elhagyva / ures_jelzo_nelkul; Számozás: tahot_szamozas / kjv_szamozas), a darabszamok kiirva.
  4. VALTOZOTT KONYVEK: soronkent az (Strong-szam, Angol szo) sorozat azonos a regiveL (csak az Igehely / Szosorszam valtozhat), a sorszam azonos; a valtozott
     fejezetek listaja (regi- es uj-fejezet).
  5. UJ KONYVEK: a regi fajlban nem voltak (sorszam).
Kimenet: naplok/F41_nulladiff.txt (a stdout-ra is). Hasznalat: python eszkozok/fj2/bsb_nulladiff.py [--alap main] [--ki naplok/F41_nulladiff.txt]
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ALLAPOTOK = ('forditva', 'elhagyva', 'ures_jelzo_nelkul')
SZAMOZASOK = ('tahot_szamozas', 'kjv_szamozas')


def regi_olvas(alap):
    r = subprocess.run(['git', 'show', '%s:konkordancia/BSB_Strongs.tsv' % alap], cwd=kozos.REPO, capture_output=True)
    if r.returncode != 0:
        raise SystemExit('HIBA: git show %s:konkordancia/BSB_Strongs.tsv: %s' % (alap, r.stderr.decode('utf-8', 'replace')))
    return r.stdout.decode('utf-8').split('\n')


def konyvenkent(sorok):
    """(fejlec_oszlopok, OrderedDict {konyv: [mezo-lista]}) a sorokbol (split('\\t'))."""
    fej = sorok[0].split('\t')
    ki = {}
    for s in sorok[1:]:
        if not s:
            continue
        m = s.split('\t')
        ki.setdefault(m[0].split('.')[0], []).append(m)
    return fej, ki


def fejezet(m):
    return int(m[0].split('.')[1])


def fut(alap, kimenet):
    alap_sha = subprocess.run(['git', 'rev-parse', alap], cwd=kozos.REPO, capture_output=True, text=True).stdout.strip()
    regi_fej, regi = konyvenkent(regi_olvas(alap))
    with open(os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv'), encoding='utf-8', newline='') as f:
        uj_sorok = f.read().split('\n')
    uj_fej, uj = konyvenkent(uj_sorok)
    sorok = ['# GENERÁLT: eszkozok/fj2/bsb_nulladiff.py — kézzel nem szerkesztendő.',
             '# alap: git %s (%s):konkordancia/BSB_Strongs.tsv vs a munkafa konkordancia/BSB_Strongs.tsv; futtatási parancs: python eszkozok/fj2/bsb_nulladiff.py --alap %s' % (alap, alap_sha[:12], alap),
             '# proveniencia: scope=BSB_Strongs.tsv teljes (alap vs munkafa) | forras=git %s + munkafa | ts=%s' % (alap_sha[:12], kozos.ma())]
    hiba = 0
    # 1. fejlec
    fej_ok = uj_fej[:len(regi_fej)] == regi_fej
    sorok.append('FEJLEC: regi=%s | uj=%s | a regi oszlopok az ujban azonos neven, sorrendben az elejen: %s' % (regi_fej, uj_fej, 'IGEN' if fej_ok else 'NEM'))
    hiba += 0 if fej_ok else 1
    # 2. konyvsorrend
    regi_sorrend = [k for k in regi if k in uj]
    uj_sorrend = [k for k in uj if k in regi]
    sorrend_ok = regi_sorrend == uj_sorrend and len(regi_sorrend) == len(regi)
    sorok.append('KONYVSORREND: a regi fajl %d konyve az ujban ugyanabban a relativ sorrendben: %s' % (len(regi), 'IGEN' if sorrend_ok else 'NEM'))
    hiba += 0 if sorrend_ok else 1
    azonos, valtozott, uj_konyvek = [], [], []
    n_regi = len(regi_fej)
    for k in uj:
        if k not in regi:
            uj_konyvek.append((k, len(uj[k])))
            continue
        r, u = regi[k], uj[k]
        ervenyes = all(len(m) == len(uj_fej) and m[n_regi] in ALLAPOTOK and m[n_regi + 1] in SZAMOZASOK for m in u)
        if not ervenyes:
            hiba += 1
            sorok.append('HIBA: %s: az uj oszlopok ertekei nem ervenyesek' % k)
        if [m[:n_regi] for m in u] == r:
            azonos.append((k, len(r), sum(1 for m in u if m[n_regi + 1] == 'kjv_szamozas')))
        else:
            seq_ok = len(r) == len(u) and all(a[2] == b[2] and a[3] == b[3] for a, b in zip(r, u))
            rs, us = {tuple(m) for m in r}, {tuple(m[:n_regi]) for m in u}
            fej_valt = sorted({fejezet(list(x)) for x in rs - us} | {fejezet(list(x)) for x in us - rs})
            valtozott.append((k, len(r), len(u), seq_ok, fej_valt, len(rs - us)))
            if not seq_ok:
                hiba += 1
    sorok.append('AZONOS (a regi fajl mind az %d oszlopa, bajtra, ugyanabban a sorrendben): %d konyv, %d sor' % (n_regi, len(azonos), sum(a[1] for a in azonos)))
    sorok.append('AZONOS konyvek: ' + ', '.join('%s(%d sor%s)' % (k, n, '; ebbol kjv_szamozas=%d' % kj if kj else '') for k, n, kj in azonos))
    sorok.append('VALTOZOTT (a felhasznaloi dontes szerinti atszamozas): %d konyv; ellenorzes: a sorszam es az (Strong-szam, Angol szo) sorozat soronkent azonos a regivel, csak az Igehely / Szosorszam valtozik' % len(valtozott))
    for k, nr, nu, seq_ok, fv, nd in valtozott:
        sorok.append('VALTOZOTT: %s: sorok regi=%d uj=%d; Strong+Angol szo sorozat azonos: %s; valtozott sorok (regi alakban): %d; erintett fejezetek (regi- vagy uj-szamozas): %s' % (k, nr, nu, 'IGEN' if seq_ok else 'NEM', nd, ' '.join(str(x) for x in fv)))
    sorok.append('UJ konyvek (a regi fajlban nem voltak): ' + ', '.join('%s(%d sor)' % x for x in uj_konyvek))
    sorok.append('OSSZESEN: regi %d sor, uj %d sor; hibak: %d' % (sum(len(v) for v in regi.values()), sum(len(v) for v in uj.values()), hiba))
    szoveg = '\n'.join(sorok) + '\n'
    with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print(szoveg)
    return hiba


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--alap', default='main')
    ap.add_argument('--ki', default=os.path.join(kozos.NAPLOK, 'F41_nulladiff.txt'))
    a = ap.parse_args()
    raise SystemExit(1 if fut(a.alap, a.ki) else 0)


if __name__ == '__main__':
    main()
