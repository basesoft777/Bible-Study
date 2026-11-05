# -*- coding: utf-8 -*-
"""F123 HAMART-001 U4: a kiejtés egységesítése a jóváhagyott alakra (adat/kiejtes_kivetelek.tsv: אָרַר árar,
אֲדָמָה adámá), az olvasói kapu ATIRAS-osztálya szerint. Csak a HAMART-001 sorai és a motívum forrása változik;
a Jer 51:25 prózájából kikerül a Jel 19:2-ből vett idézet (a kapu a fölötte álló verssel vet össze)."""
import io
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CSERE = [(re.compile(r'\barar\b'), 'árar'), (re.compile(r'\badamá\b'), 'adámá')]
JER_A = ', ahol a nagy parázna „a földet megrontotta az ő paráznaságával”.'
JER_B = ', ahol a nagy parázna ugyanígy a földet rontja meg.'


def javit(s):
    for rx, uj in CSERE:
        s = rx.sub(uj, s)
    return s.replace(JER_A, JER_B)


def tabla(ut):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(nl)
    n = 0
    for i, s in enumerate(sorok):
        if s.startswith('HAMART-001\t'):
            u = javit(s)
            n += u != s
            sorok[i] = u
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
    print(ut, n)


def fajl(ut):
    s = io.open(ut, encoding='utf-8', newline='').read()
    u = javit(s)
    io.open(ut, 'w', encoding='utf-8', newline='').write(u)
    print(ut, s != u)


for t in ('adat/elofordulasok.tsv', 'adat/motivumok.tsv'):  # a jeloltek.tsv régi indoklásai az elutasítási minták miatt maradnak
    tabla(t)
for f in ('motivumok/HAMART-001.md', 'naplok/F123_HAMART3_u3_adat.py'):
    fajl(f)
