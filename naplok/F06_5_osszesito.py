#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F06 5. lepes: a jelentesbe kerulo szamok kigyujtese a naplok/F06_*.tsv kimenetekbol.
Minden szam, amit a naplok/F06_forras_jelentes.md idez, ennek a szkriptnek a kimenetebol
(vagy kozvetlenul egy F06_*.tsv soraibol) szarmazik. A '#'-sorokat kihagyja, split('\\t')-tel olvas.

    python naplok/F06_5_osszesito.py
"""
import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))


def olvas(nev):
    sorok = []
    for s in open(os.path.join(D, nev), encoding='utf-8'):
        s = s.rstrip('\n')
        if s and not s.startswith('#'):
            sorok.append(s.split('\t'))
    return sorok[0], sorok[1:]


# --- Macula, 87 hely
f, r = olvas('F06_macula_87_hely.tsv')
i = {n: k for k, n in enumerate(f)}
print('MACULA 87 hely: sorok=%d' % len(r))
for k, v in sorted(Counter(x[i['allapot']] for x in r).items()):
    print('  allapot %s = %d' % (k, v))
for k, v in sorted(Counter((x[i['allapot']], x[i['azonositas']]) for x in r).items()):
    print('  allapot x azonositas %s = %d' % (k, v))
print('  egyedi igehely a LXX_MEGFELELO sorokban: %d' % len({x[i['igehely']] for x in r if x[i['allapot']] == 'LXX_MEGFELELO'}))
print('  megjegyzes kitoltve (tobb heber talalat, eltero gorog Strong): %d' % sum(1 for x in r if x[i['megjegyzes']].startswith('tobb')))

# --- Macula lefedettseg
f, r = olvas('F06_macula_lefedettseg.tsv')
i = {n: k for k, n in enumerate(f)}
print('MACULA lefedettseg: konyv=%d ; lowfat-fajl osszesen=%d' % (len(r), sum(int(x[i['fajlok_lowfat']]) for x in r)))
ki = [x for x in r if x[i['kiemelt_1Sam_2Kron']] == 'igen']
print('  kiemelt 1Sam-2Kron: konyv=%d fajl=%d macula_versek=%d tahot_versek=%d kozos=%d' % (
    len(ki), sum(int(x[i['fajlok_lowfat']]) for x in ki), sum(int(x[i['macula_versek']]) for x in ki),
    sum(int(x[i['tahot_versek']]) for x in ki), sum(int(x[i['kozos_versek']]) for x in ki)))
print('  konyv 0 lowfat-fajllal: %d' % sum(1 for x in r if int(x[i['fajlok_lowfat']]) == 0))
print('  osszes macula_versek=%d tahot_versek=%d kozos=%d' % (
    sum(int(x[i['macula_versek']]) for x in r), sum(int(x[i['tahot_versek']]) for x in r), sum(int(x[i['kozos_versek']]) for x in r)))
print('  teljes egyezes (csak_macula=0 es csak_tahot=0) konyvek: %d' % sum(
    1 for x in r if x[i['csak_macula']] == '0' and x[i['csak_tahot']] == '0'))

# --- BSB
f, r = olvas('F06_bsb_genezis.tsv')
i = {n: k for k, n in enumerate(f)}
print('BSB: versek=%d ; allapot: %s' % (len(r), dict(Counter(x[i['allapot']] for x in r))))
f, r = olvas('F06_bsb_elteresek.tsv')
print('BSB elteresek: sorok=%d ; ok: %s' % (len(r), dict(Counter(x[1] for x in r))))
print('  elteresek, ahol a TAHOT 2895 (a BSB 2896): %d' % sum(1 for x in r if x[2] == '2895' and x[3] == '2896'))

# --- licenc
f, r = olvas('F06_licenc.tsv')
i = {n: k for k, n in enumerate(f)}
print('LICENC: szovegek=%d ; allapot: %s' % (len(r), dict(Counter(x[i['allapot']] for x in r))))
print('  licenc_tipus (kapun atment): %s' % dict(Counter(x[i['licenc_tipus']] for x in r if x[i['allapot']] == 'javaslat_kapun_atment')))
print('  nem ures idezet (kapun atment): %d' % sum(1 for x in r if x[i['allapot']] == 'javaslat_kapun_atment' and x[i['idezet']]))
f, r = olvas('F06_koltseg.tsv')
i = {n: k for k, n in enumerate(f)}
print('KOLTSEG: hivasok=%d ; osszeg=%.6f USD ; kiserlet=2 sorok=%d ; providerek=%s' % (
    len(r), sum(float(x[i['koltseg_usd']]) for x in r), sum(1 for x in r if x[i['kiserlet']] == '2'),
    sorted({x[i['provider']] for x in r})))
