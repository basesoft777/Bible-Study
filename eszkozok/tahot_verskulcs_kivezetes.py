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

Használat:  python eszkozok/tahot_verskulcs_kivezetes.py [--ir]
"""
import os
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


def main():
    ir = '--ir' in sys.argv
    v = valtas()
    kiirt = []
    uj_tartalom = {}
    egyezes = {'egyezik': 0, 'nem_egyezik': 0, 'nem_atkulcsolt': 0}
    nem_egyezo = []
    for fajl, ut in (('f22/versmegfeleltetes_kezi.tsv', KEZI), ('f22/versosszevonas.tsv', OSSZ)):
        sorok = szetvag(ut)
        marad, fejlec_volt = [], False
        for n, s in enumerate(sorok, 1):
            if s.startswith('#'):
                marad.append(s)
                continue
            if not fejlec_volt:
                fejlec_volt = True
                marad.append(s)
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
        marad.append(JEGYZET.rstrip('\n'))
        uj_tartalom[ut] = ('\n'.join(marad) + '\n').encode('utf-8')
        # ellenőrzés: a megmaradó sorok az eredeti sorok (sorrendben) + az új megjegyzés
        regi_fenn = [s for s in sorok if s.startswith('#')]
        if [s for s in marad[:-1] if s.startswith('#')] != regi_fenn:
            leall('%s: megjegyzés-sorok eltérnek' % ut)
    print('kivezetendő sor: %d (kézi tábla %d, összevonás %d)' % (len(kiirt), sum(1 for r in kiirt if r[0].endswith('kezi.tsv')), sum(1 for r in kiirt if r[0].endswith('osszevonas.tsv'))))
    print('az átkulcsolt esettel való egyezés (kompenzáló sor Károli-kulcsa = az átkulcsolt vers új kulcsa):', egyezes)
    for x in nem_egyezo:
        print('  NEM EGYEZIK:', x)
    if nem_egyezo:
        leall('a kivezetendő sorok egy része nem az átkulcsolt eltolást kompenzálta')
    if not ir:
        print('szárazon futott (--ir kell).')
        return 0
    for ut, b in uj_tartalom.items():
        open(ut, 'wb').write(b)
    with open(KI, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_kivezetes.py | a #22 kézi táblák (f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv) F85.8-ban kivezetett adatsorai az átkulcsolt eset hivatkozásával | forras=a HEAD~ állapot sorai, naplok/F85_kulcsvaltas.tsv | ts=2026-10-09\n')
        fh.write('forras_fajl\tsor_a_regi_fajlban\tkaroli\teredeti\ttipus\thu_tol\thu_ig\tuj_kulcs\tkulcsvaltas_sor\tegyezes\tatkulcsolt_eset\tmegjegyzes\n')
        for r in kiirt:
            fh.write('\t'.join(r) + '\n')
    print('írva: %s, %s, %s' % (KEZI, OSSZ, KI))
    return 0


if __name__ == '__main__':
    sys.exit(main())
