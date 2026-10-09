#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.8 — a #22 kézi táblák adatsorainak kivezetése a TAHOT_kivonat átkulcsolása (F85.6) után (brief 4. tétel).

Az átkulcsolás után a TAHOT_kivonat Igehely-kulcsa maga a Károli-vers, ezért a Károli -> TAHOT kulcs-kompenzáló
sorok (`f22/versmegfeleltetes_kezi.tsv`: eltolt / nincs_karoli / torol) kétszeres eltolást okoznának, és az
`f22/versosszevonas.tsv` `eredeti` kulcsa már az eltolt tartalomra mutatna (a beolvasztott vers sorai a közös
Károli-kulcson vannak). Ez a szkript:
  - a két fájlból minden adatsort kivezet (a `#` megjegyzés-sorok és a fejléc marad, egy új megjegyzés-sor jelzi a
    kivezetést), az írás előtt ellenőrizve, hogy a megmaradó sorok bájtra az eredeti megfelelő sorai;
  - a kivezetett sorokat a `naplok/F85_kivezetett_sorok.tsv`-be listázza az átkulcsolt eset hivatkozásával
    (a `naplok/F85_kulcsvaltas.tsv` régi -> új kulcsa és sorszáma), és ellenőrzi, hogy a kompenzáló sor
    Károli-kulcsa megegyezik-e az átkulcsolt vers új kulcsával.
A detektor-lista (`f22/versmegfeleltetes.tsv`) nem itt készül: azt a `eszkozok/karoli_strong/versbeosztas.py`
generálja újra. Csak split('\\t') / '\\t'.join, a csv modul nincs használatban. A tokenek-modult nem importálja.

Használat:
    python eszkozok/tahot_verskulcs_kivezetes.py [--ir]            # az F85.8 egyszeri kivezetése (az f22 táblák F85.10 utáni alakján megtagadja)
    python eszkozok/tahot_verskulcs_kivezetes.py --archivum [--ref=REF] [--ir]   # a naplok/F85_kivezetett_sorok.tsv generálása (alapértelmezett REF: 0483fd9f~1)
"""
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEZI = os.path.join(ROOT, 'f22', 'versmegfeleltetes_kezi.tsv')
OSSZ = os.path.join(ROOT, 'f22', 'versosszevonas.tsv')
VALT = os.path.join(ROOT, 'naplok', 'F85_kulcsvaltas.tsv')
KI = os.path.join(ROOT, 'naplok', 'F85_kivezetett_sorok.tsv')
JEGYZET = '# F85.8: az adatsorok kivezetve (a TAHOT_kivonat Igehely-kulcsa az F85.6 óta Károli-kulcs); az eredeti sorok: naplok/F85_kivezetett_sorok.tsv\n'


def leall(u):
    print('LEÁLL (nem írtam semmit): ' + u)
    sys.exit(1)


def valtas():
    """{régi TAHOT-kulcs: (új kulcs, első sorszám a naplóban, típus)}"""
    d = {}
    with open(VALT, encoding='utf-8') as fh:
        for s in fh:
            if s.startswith('#') or s.startswith('sorszam\t'):
                continue
            p = s.rstrip('\n').split('\t')
            d.setdefault(p[1], (p[2], p[0], p[3]))
    return d


def szetvag(ut):
    b = open(ut, 'rb').read().decode('utf-8')
    if '\r' in b:
        leall('%s: váratlan CR' % ut)
    sorok = b.split('\n')
    if sorok[-1] != '':
        leall('%s: nincs záró újsor' % ut)
    return sorok[:-1]


def sorok_epit(fajl, sorok, v):
    """A kivezetendő adatsorok archív sorai: (kiírt sorok, egyezés-számláló, nem egyező sorok).
    `sorok`: a fájl sorai (megjegyzés, fejléc, adatsorok); a sorszám 1-alapú a fájlban."""
    kiirt, nem_egyezo = [], []
    egyezes = {'egyezik': 0, 'nem_egyezik': 0, 'nem_atkulcsolt': 0}
    fejlec_volt = False
    for n, s in enumerate(sorok, 1):
        if s.startswith('#'):
            continue
        if not fejlec_volt:
            fejlec_volt = True
            continue
        p = s.split('\t')
        if fajl.endswith('versmegfeleltetes_kezi.tsv'):
            k, e, t = (p + ['', '', ''])[:3]
            hu_tol = hu_ig = megj = ''
        else:
            k, hu_tol, hu_ig, e = p[0], p[1], p[2], p[3]
            megj, t = (p[4] if len(p) > 4 else ''), 'osszevonas'
        if e in v:
            uj, sz, tip = v[e]
            egy = 'egyezik' if (not k or uj == k) else 'nem_egyezik'
            if t in ('nincs_karoli', 'torol'):
                egy = 'egyezik' if k == '' or uj == k else egy
            hiv = 'a(z) %s TAHOT-vers -> %s (F85_kulcsvaltas.tsv %s. sor, %s)' % (e, uj, sz, tip)
        else:
            uj, sz, tip, egy = '', '', '', 'nem_atkulcsolt'
            hiv = '' if not e else 'a(z) %s TAHOT-vers kulcsa nem változott (nem átkulcsolt: azonos kulcs / bizonytalan / összevonás-partner)' % e
        egyezes[egy] += 1
        if egy == 'nem_egyezik':
            nem_egyezo.append((fajl, n, k, e, uj))
        kiirt.append([fajl, str(n), k, e, t, hu_tol, hu_ig, uj, sz, egy, hiv, megj])
    return kiirt, egyezes, nem_egyezo


def git_sorok(ref, ut):
    r = subprocess.run(['git', 'show', '%s:%s' % (ref, ut)], capture_output=True, cwd=ROOT)
    if r.returncode:
        leall('git show %s:%s sikertelen' % (ref, ut))
    b = r.stdout.decode('utf-8')
    if '\r' in b or not b.endswith('\n'):
        leall('%s:%s: váratlan CR / nincs záró újsor' % (ref, ut))
    return b.split('\n')[:-1]


ARCH_FEJ = ['forras_fajl', 'sor_a_regi_fajlban', 'karoli', 'eredeti', 'tipus', 'hu_tol', 'hu_ig', 'uj_kulcs', 'kulcsvaltas_sor', 'egyezes', 'atkulcsolt_eset', 'megjegyzes', 'allapot_F85_10_utan']
ARCH_HEAD = ('# GENERÁLT: eszkozok/tahot_verskulcs_kivezetes.py --archivum | a #22 kézi táblák (f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv) F85.8-ban kivezetett adatsorai '
             'az átkulcsolt eset hivatkozásával, és az F85.10 utáni állapotuk (allapot_F85_10_utan) | forras=%s (a kivezetés előtti f22 táblák), f22/versosszevonas.tsv (mai), naplok/F85_kulcsvaltas.tsv | ts=2026-10-09 | '
             'F85.13: a 7 `versosszevonas` sor az F85.10-ben visszakerült (er_tol/er_ig oszloppal), +2 új sor (Hós 1:11 + 2:1, Préd 2:26 + 2:25); nettó kivezetve 97 kézi sor '
             '(f22/versmegfeleltetes_kezi.tsv), a versosszevonas.tsv 7 -> 9 adatsor')


def archivum(ref):
    """A naplok/F85_kivezetett_sorok.tsv tartalma (sorok listája) a git-előzményből (ref: a kivezetés előtti állapot), a mai
    f22/versosszevonas.tsv-ből és a naplok/F85_kulcsvaltas.tsv-ből; az f22 táblákhoz nem nyúl."""
    v = valtas()
    kiirt = []
    for fajl in ('f22/versmegfeleltetes_kezi.tsv', 'f22/versosszevonas.tsv'):
        sorok = git_sorok(ref, fajl)
        sor, egyezes, nem_egyezo = sorok_epit(fajl, sorok, v)
        if nem_egyezo:
            leall('nem egyező kompenzáló sorok: %s' % nem_egyezo)
        kiirt += sor
    # a mai versosszevonas.tsv: melyik régi sor van meg (karoli, eredeti, hu_tol, hu_ig megegyezik) és mi új
    mai = szetvag(OSSZ)
    adat, fej_volt = [], False
    for n, s in enumerate(mai, 1):
        if s.startswith('#'):
            continue
        if not fej_volt:
            fej_volt = True
            continue
        adat.append((n, s.split('\t')))
    visszakerult = {(m[0], m[3], m[1], m[2]) for n, m in adat if len(m) > 6 and m[5]}
    ki = []
    for r in kiirt:
        if r[0].endswith('versosszevonas.tsv'):
            if (r[2], r[3], r[5], r[6]) not in visszakerult:
                leall('a kivezetett összevonás-sor nem került vissza: %s' % r[:4])
            ki.append(r + ['visszakerult_F85.10_er_tol_er_ig_oszloppal'])
        else:
            ki.append(r + ['kivezetve'])
    regi_kulcsok = {(r[2], r[3], r[5], r[6]) for r in kiirt if r[0].endswith('versosszevonas.tsv')}
    for n, m in adat:
        if (m[0], m[3], m[1], m[2]) not in regi_kulcsok:
            ki.append(['f22/versosszevonas.tsv', str(n), m[0], m[3], 'osszevonas', m[1], m[2], '', '', 'uj_sor',
                       'az F85.10-ben felvett összevonás-sor (a hu_tol–hu_ig a Károli-vers szavainak tokenizal-sorszáma); nem volt kivezetve', m[4], 'uj_felvett_F85.10'])
    return [ARCH_HEAD % ref, '\t'.join(ARCH_FEJ)] + ['\t'.join(r) for r in ki]


def main():
    if '--archivum' in sys.argv:
        ref = '0483fd9f~1'
        for a in sys.argv:
            if a.startswith('--ref='):
                ref = a[len('--ref='):]
        sorok = archivum(ref)
        print('archívum: %d adatsor (%s)' % (len(sorok) - 2, ref))
        if '--ir' in sys.argv:
            with open(KI, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(sorok) + '\n')
            print('írva: %s' % KI)
        else:
            mai = open(KI, encoding='utf-8').read().split('\n')[:-1]
            print('a mai fájl adatrészével (2. sortól) azonos: %s (%d / %d sor)' % (mai[1:] == sorok[1:], len(mai) - 1, len(sorok) - 1))
        return 0
    # --- az eredeti F85.8-mód: a kézi táblák adatsorainak kivezetése (egyszeri; az F85.8 óta lefutott) ---
    ir = '--ir' in sys.argv
    kezi_sorok, ossz_sorok = szetvag(KEZI), szetvag(OSSZ)
    if len(ossz_sorok[0:5]) and any(len(s.split('\t')) > 5 for s in ossz_sorok if not s.startswith('#')):
        leall('az f22 táblák már az F85.10 utáni alakban vannak (er_tol/er_ig); a kivezetés egyszeri volt (F85.8), nem futtatható újra. Az archívum: --archivum')
    v = valtas()
    uj_tartalom = {}
    kiirt = []
    for fajl, ut, sorok in (('f22/versmegfeleltetes_kezi.tsv', KEZI, kezi_sorok), ('f22/versosszevonas.tsv', OSSZ, ossz_sorok)):
        sor, egyezes, nem_egyezo = sorok_epit(fajl, sorok, v)
        if nem_egyezo:
            leall('a kivezetendő sorok egy része nem az átkulcsolt eltolást kompenzálta: %s' % nem_egyezo)
        kiirt += sor
        marad, fejlec_volt = [], False
        for s in sorok:
            if s.startswith('#') or not fejlec_volt:
                if not s.startswith('#'):
                    fejlec_volt = True
                marad.append(s)
        marad.append(JEGYZET.rstrip('\n'))
        uj_tartalom[ut] = ('\n'.join(marad) + '\n').encode('utf-8')
    print('kivezetendő sor: %d' % len(kiirt))
    if not ir:
        print('szárazon futott (--ir kell).')
        return 0
    for ut, b in uj_tartalom.items():
        open(ut, 'wb').write(b)
    print('írva: %s, %s; az archívum (naplok/F85_kivezetett_sorok.tsv) a --archivum móddal generálódik' % (KEZI, OSSZ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
