#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_M1_nezet.py -- F38 (BDB_FORDITAS) megallasi pont: egy
adag kapueredmenyei (az adat/forditasok.tsv BDB `teljes` soraibol, a
vegleges kapusoron ujrafuttatva) es a mintaszocikkek forras-forditas nezete
(az emeles.py egymas_mellett fuggvenyevel). Csak olvas; a kimenet a stdout
(markdown), a naplo kezi szakaszaba illesztendo.

    python naplok/BDB_FORDITAS_M1_nezet.py --adag 1 --minta 5 --seed 38

A minta: a szocikkek hossz szerint harmadolva, mindegyik harmadbol egy,
a maradek a tobbibol, random.Random(seed)-del -- reprodukalhato.
TSV: split('\\t') (CLAUDE.md).
"""

import argparse
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402

SORREND_UT = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_sorrend.tsv')
NEVEK = ['1_gorog_heber', '2_versszam', '3_karoli_roviditesek', '4_formazas', '5_terminologia',
         '6_hosszarany', '8_idezojel', '9_tagolas', '10_torzs', '11_konyvek', '12_szentlelek',
         '13_fejezetszam']


def adag_strongok(adag):
    it = E.tsv_sorok(SORREND_UT)
    fej = None
    ki = []
    for m in it:
        if m[0].startswith('#'):
            continue
        if fej is None:
            fej = m
            continue
        r = dict(zip(fej, m))
        if r['adag'] == str(adag):
            ki.append(r['strong'])
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adag', type=int, required=True)
    ap.add_argument('--minta', type=int, default=5)
    ap.add_argument('--seed', type=int, default=38)
    args = ap.parse_args()

    strongok = adag_strongok(args.adag)
    ford = {r['strong']: r for r in E.tsv_dict_sorok(E.FORDITASOK_UT)
            if r['szotar'] == 'BDB' and r['jelentes_szam'] == 'teljes'}
    sorok = []
    for sp in strongok:
        _, forras = E.forras_szoveg(sp)
        r = ford.get(sp)
        if r is None:
            sorok.append((sp, len(forras), None, None, None))
            continue
        kiv = []
        if 'bizonytalan_feloldasok):' in (r.get('megjegyzes') or ''):
            kiv = [x.strip() for x in r['megjegyzes'].split('bizonytalan_feloldasok):', 1)[1].split(',')]
        eredm = {n: (e, d) for n, e, d in K.kapuk_futtat('BDB', forras, r['forditas_hu'], kiv)}
        sorok.append((sp, len(forras), r, eredm, kiv))

    kesz = [s for s in sorok if s[2] is not None]
    print('### Kapueredmények (adag %d, %d/%d szócikk kész)' % (args.adag, len(kesz), len(sorok)))
    print()
    print('| Strong | Forrás kar. | Fordítás kar. | ' + ' | '.join(n.split('_', 1)[0] for n in NEVEK) + ' | Átment |')
    print('|---|---|---|' + '---|' * len(NEVEK) + '---|')
    for sp, hossz, r, eredm, kiv in sorok:
        if r is None:
            print('| %s | %d | — | %s | nincs fordítás |' % (sp, hossz, ' | '.join('—' for _ in NEVEK)))
            continue
        cellak = []
        for n in NEVEK:
            e, d = eredm.get(n, ('—', ''))
            cellak.append(e + (' (%s)' % d if n == '6_hosszarany' else ''))
        ok = all(eredm[n][0] != 'SERTES' for n in K.GATOLO if n in eredm)
        print('| %s | %d | %d | %s | %s |' % (sp, hossz, len(r['forditas_hu']), ' | '.join(cellak),
                                             'igen' if ok else 'NEM'))
    print()
    print('Összesen: forrás %d, fordítás %d karakter.' % (
        sum(s[1] for s in kesz), sum(len(s[2]['forditas_hu']) for s in kesz)))
    jelzesek = [(s[0], s[3]['13_fejezetszam'][1]) for s in kesz if s[3]['13_fejezetszam'][0] != 'RENDBEN']
    if jelzesek:
        print()
        print('13. kapu (JELZES, nem gátoló): ' + '; '.join('%s — %s' % j for j in jelzesek) + '.')
    kivetelek = [(s[0], ', '.join(s[4])) for s in kesz if s[4]]
    if kivetelek:
        print()
        print('Terminológia-kivétel: ' + '; '.join('%s — %s' % k for k in kivetelek) + '.')

    # minta
    rnd = random.Random(args.seed)
    rendezett = sorted(kesz, key=lambda s: s[1])
    n = len(rendezett)
    harmadok = [rendezett[:n // 3], rendezett[n // 3:2 * n // 3], rendezett[2 * n // 3:]]
    minta = [rnd.choice(h) for h in harmadok if h]
    maradek = [s for s in rendezett if s not in minta]
    minta += rnd.sample(maradek, max(0, min(args.minta, n) - len(minta)))
    minta.sort(key=lambda s: s[1])
    print()
    print('### Minta (%d szócikk, seed=%d, hossz szerinti harmadokból): %s' % (
        len(minta), args.seed, ', '.join('%s (%d)' % (s[0], s[1]) for s in minta)))
    for sp, hossz, r, eredm, kiv in minta:
        _, forras = E.forras_szoveg(sp)
        print()
        print('#### %s (%d → %d karakter)' % (sp, hossz, len(r['forditas_hu'])))
        print()
        print('`forras_hash=%s` · `allapot=%s` · `modell=%s` · `terminologia_verzio=%s`'
              % (r['forras_hash'], r['allapot'], r['modell'], r['terminologia_verzio']))
        print()
        for sor in E.egymas_mellett(forras, r['forditas_hu']):
            print(sor)


if __name__ == '__main__':
    main()
