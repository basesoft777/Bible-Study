#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_M0.py -- F38 (BDB_FORDITAS) M0 felmeres, csak olvas
(a naplok/BDB_FORDITAS_sorrend.tsv-n kivul semmit nem ir).

  1. Elofeltetel: az F34 merge-commitja (fa501c9) a main ose-e; a 13. kapu
     (fejezetszam) a forrason: a forras konyvrovidíteseit a 11. kapu
     lekepezesevel Karoli-alakra fordítva, szocikkenkent.
  2. Gyakorisag: konkordancia/TAHOT_kivonat.tsv (heber/arami OSZ szoveg,
     szavankenti Strong-cimke, CC BY 4.0) sorainak szama Strong-szamonkent;
     osszevetes: konkordancia/KJV_Strongs_teljes.tsv (kozkincs).
  3. Sorrend: gyakorisag szerint csokkeno, egyenlonel Strong-szam; a mar kesz
     (adat/forditasok.tsv BDB `teljes`) szocikkek kimaradnak.
  4. Szegmenshatarok a 20 000 karakter feletti szocikkekre.
  5. Adagok: M1 ~150 000 karakter, utana ~500 000.

    python naplok/BDB_FORDITAS_M0.py            # jelentes a stdout-ra + sorrend.tsv
    python naplok/BDB_FORDITAS_M0.py --nem-ir   # csak jelentes

TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import forditas_kapuk as K  # noqa: E402

BDB_UT = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
TAHOT_UT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
KJV_UT = os.path.join(REPO, 'konkordancia', 'KJV_Strongs_teljes.tsv')
FORDITASOK_UT = os.path.join(REPO, 'adat', 'forditasok.tsv')
MARADEK_UT = os.path.join(REPO, 'naplok', 'F34_M2_maradek.tsv')
SORREND_UT = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_sorrend.tsv')

F34_MERGE = 'fa501c9'
M1_CEL = 150000
ADAG_CEL = 500000
SZEGMENS_HATAR = 20000     # e folott szegmenshatarok kellenek (brief M0.3)
SZEGMENS_MAX = 10000       # egy szegmens legfeljebb ennyi karakter (javaslat)


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor and not sor.startswith('#'):
                yield sor.split('\t')


def padded(s):
    m = re.match(r'^H0*(\d{1,5})$', s.strip())
    return 'H%04d' % int(m.group(1)) if m else None


def bdb_betolt():
    it = tsv(BDB_UT)
    fej = next(it)
    assert fej[:3] == ['Strong_padded', 'Strong_eredeti', 'Teljes_szocikk'], fej
    return {m[0]: m[2] for m in it}


def gyakorisag(ut, oszlop_nev):
    it = tsv(ut)
    fej = next(it)
    i = fej.index(oszlop_nev)
    c = Counter()
    for m in it:
        p = padded(m[i]) if len(m) > i else None
        if p:
            c[p] += 1
    return c


def kesz_strongok():
    it = tsv(FORDITASOK_UT)
    fej = next(it)
    ix = {n: i for i, n in enumerate(fej)}
    return {m[ix['strong']] for m in it
            if m[ix['szotar']] == 'BDB' and m[ix['jelentes_szam']] == 'teljes'}


def f34_ellenorzes():
    def git(*a):
        return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    ki = {}
    for ref in ('origin/main', 'main', 'HEAD'):
        r = git('merge-base', '--is-ancestor', F34_MERGE, ref)
        ki[ref] = {0: 'igen', 1: 'nem'}.get(r.returncode, 'ismeretlen (%s)' % r.stderr.strip())
    return ki


def forras_fejezetszam(bdb):
    """A 13. kapu a forrason: a konyvnevvel jelolt igehelyek Karoli-alakra
    lekepezve (a 11. kapu lekepezese), majd K.ellenoriz_fejezetszam."""
    lek, f_minta, _ = K._konyv_mintak()
    jelzes = {}
    for sp, szoveg in bdb.items():
        hu = f_minta.sub(lambda m: lek[m.group(1)] + ' ', szoveg)
        e, r = K.ellenoriz_fejezetszam(hu)
        if e != 'RENDBEN':
            jelzes[sp] = r.split(': ', 1)[1]
    return jelzes


def szegmensek(szoveg):
    """Szegmenshatar-javaslat: strukturalis helyzetu (elotte `— `, `. `, `; `)
    tagolasjelolo vagy igetorzs-cimke elott vagunk, mohon, ugy, hogy egy
    szegmens legfeljebb SZEGMENS_MAX karakter legyen (ha van ra jelolt)."""
    jeloltek = []
    for p, j in K.jelolok_pozicioval(szoveg, True):
        if p > 0 and szoveg[max(0, p - 2):p] in ('— ', '. ', '; '):
            jeloltek.append((p, j))
    for m in K.TORZS_MINTA.finditer(szoveg):
        p = m.start()
        if p > 0 and szoveg[max(0, p - 2):p] in ('— ', '. ', '; '):
            jeloltek.append((p, m.group(1)))
    jeloltek = sorted(set(jeloltek))
    hatarok = []
    eleje = 0
    while len(szoveg) - eleje > SZEGMENS_MAX:
        bent = [(p, j) for p, j in jeloltek if eleje < p <= eleje + SZEGMENS_MAX]
        if not bent:
            utana = [(p, j) for p, j in jeloltek if p > eleje + SZEGMENS_MAX]
            if not utana:
                break
            bent = [utana[0]]
        p, j = bent[-1]
        hatarok.append((p, j))
        eleje = p
    return hatarok


def adagol(sorok):
    adag, osszeg = 1, 0
    cel = M1_CEL
    for s in sorok:
        if osszeg > 0 and osszeg + s['karakter'] > cel:
            adag += 1
            osszeg = 0
            cel = ADAG_CEL
        s['adag'] = adag
        osszeg += s['karakter']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nem-ir', action='store_true')
    args = ap.parse_args()

    print('== 1. Elofeltetel (F34)')
    for ref, v in f34_ellenorzes().items():
        print('  %s a(z) %s ose: %s' % (F34_MERGE, ref, v))
    bdb = bdb_betolt()
    print('  BDB szocikk: %d, karakter: %d' % (len(bdb), sum(map(len, bdb.values()))))
    jelzes = forras_fejezetszam(bdb)
    maradek = set()
    if os.path.exists(MARADEK_UT):
        it = tsv(MARADEK_UT)
        next(it)
        maradek = {m[0] for m in it}
    print('  13. kapu a forrason: %d szocikk jelez; ebbol az F34 maradek-listajan (N-F34) %d'
          % (len(jelzes), len(set(jelzes) & maradek)))
    for sp in sorted(jelzes):
        print('    %s%s: %s' % (sp, '' if sp in maradek else ' [NINCS a maradek-listan]', jelzes[sp]))

    print('== 2. Gyakorisag')
    tahot = gyakorisag(TAHOT_UT, 'Strong-szám')
    kjv = gyakorisag(KJV_UT, 'Strong-szám')
    print('  TAHOT: %d cimkezett szo, %d kulonbozo H-szam (ebbol a BDB-ben: %d)'
          % (sum(tahot.values()), len(tahot), len(set(tahot) & set(bdb))))
    print('  KJV:   %d cimkezett szo, %d kulonbozo H-szam (ebbol a BDB-ben: %d)'
          % (sum(kjv.values()), len(kjv), len(set(kjv) & set(bdb))))
    nulla = [sp for sp in bdb if tahot.get(sp, 0) == 0]
    print('  BDB-szocikk TAHOT-gyakorisag nelkul (0): %d' % len(nulla))

    def top(c, n):
        return [s for s, _ in sorted(((s, v) for s, v in c.items() if s in bdb),
                                     key=lambda x: (-x[1], x[0]))[:n]]
    for n in (50, 100, 500):
        print('  top-%d atfedes TAHOT~KJV: %d' % (n, len(set(top(tahot, n)) & set(top(kjv, n)))))

    print('== 3. Sorrend')
    kesz = kesz_strongok()
    print('  mar kesz (forditasok.tsv BDB teljes): %d' % len(kesz))
    sorok = [{'strong': sp, 'gyakorisag': tahot.get(sp, 0), 'karakter': len(sz)}
             for sp, sz in bdb.items() if sp not in kesz]
    sorok.sort(key=lambda s: (-s['gyakorisag'], s['strong']))
    for i, s in enumerate(sorok, 1):
        s['sorszam'] = i
    adagol(sorok)
    print('  forditando: %d szocikk, %d karakter' % (len(sorok), sum(s['karakter'] for s in sorok)))
    print('  2000 felett: %d; 20000 felett: %d'
          % (sum(1 for s in sorok if s['karakter'] > 2000), sum(1 for s in sorok if s['karakter'] > SZEGMENS_HATAR)))

    print('== 4. Szegmenshatarok (> %d karakter)' % SZEGMENS_HATAR)
    for s in sorok:
        if s['karakter'] > SZEGMENS_HATAR:
            h = szegmensek(bdb[s['strong']])
            pozok = [0] + [p for p, _ in h] + [s['karakter']]
            hosszak = [pozok[i + 1] - pozok[i] for i in range(len(pozok) - 1)]
            print('  %s (sorszam %d, %d kar.): %d szegmens; hatarok: %s; hosszak: %s'
                  % (s['strong'], s['sorszam'], s['karakter'], len(hosszak),
                     ', '.join('%d «%s»' % (p, j) for p, j in h), '/'.join(map(str, hosszak))))

    print('== 5. Adagok')
    adagok = Counter()
    adag_kar = Counter()
    for s in sorok:
        adagok[s['adag']] += 1
        adag_kar[s['adag']] += s['karakter']
    for a in sorted(adagok):
        tagok = [s for s in sorok if s['adag'] == a]
        print('  adag %2d: %4d szocikk, %7d karakter, sorszam %d-%d'
              % (a, adagok[a], adag_kar[a], tagok[0]['sorszam'], tagok[-1]['sorszam']))
    m1 = [s for s in sorok if s['adag'] == 1]
    print('  M1 (adag 1) tagjai: %s' % ', '.join('%s(%d/%d)' % (s['strong'], s['gyakorisag'], s['karakter']) for s in m1))

    if not args.nem_ir:
        with open(SORREND_UT, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# F38 M0 -- generalja: python naplok/BDB_FORDITAS_M0.py; gyakorisag: '
                     'konkordancia/TAHOT_kivonat.tsv (Strong-cimkenkenti sorszam); kesz sorok kimaradnak\n')
            fej = ['sorszam', 'strong', 'gyakorisag', 'karakter', 'adag']
            fh.write('\t'.join(fej) + '\n')
            for s in sorok:
                fh.write('\t'.join(str(s[m]) for m in fej) + '\n')
        print('irva: %s (%d sor)' % (os.path.relpath(SORREND_UT, REPO), len(sorok)))


if __name__ == '__main__':
    main()
