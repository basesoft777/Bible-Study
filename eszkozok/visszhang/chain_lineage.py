#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_lineage.py -- a Chain Lineage Browser (Blidstein, Inowlocki, Verheyden) tényadat-lekérdezése a tanúréteghez
(F183, FELADATOK #183).

A böngésző (https://mblida.pythonanywhere.com/chain-lineages) az egyházatyák bibliai versláncait mutatja. Ez a szkript a
nyilvános JSON-végpontot kérdezi le egy verspárra (`q = "gen 3.14 + gal 3.13"`: mindkét vers a lánc magjában), és csak
TÉNYADATOT ad vissza: lánccsalád, mag-versek, szerző, mű, század, nyelv, a BiblIndex-tanúk száma. Szöveget nem kér és
nem tárol (a licenc nincs megadva; az adatbázisra külön jog vonatkozhat; a felhasználó döntése, 2026-11-11: csak
tényadat és hivatkozás).

    lekerdez "gen 3.14 + gal 3.13" [--max-szazad 8]
        a családok, amelyeknek MAGJÁBAN mindkét vers áll, és a tanúk, akik mindkét magverset idézik (core_cov = 1).
        Kimenet: tabulált sorok (csalad, mag, szerzo, mu, szazad, nyelv, n_bi) és a proveniencia-sor.

A lekérdezés eredménye a tanú-jelölt, nem a lap sora: a lapra csak az `adat/visszhang_tanuk.tsv` (SEMA 2.58) ellenőrzött
során át kerül (CLAUDE.md 2. szabály). Forrásmegjelölés a lapon: a böngésző és a bibliai hivatkozások eredete (BiblIndex,
Institut des Sources Chrétiennes, CNRS – HiSoMA, Lyon).
"""
import argparse
import datetime
import json
import sys
import urllib.parse
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ALAP = 'https://mblida.pythonanywhere.com/chain-lineages'
UA = {'User-Agent': 'pardes-lexikon-tanureteg/1.0 (tenyadat-lekerdezes)'}


def csaladok_url(q):
    return ALAP + '/api/families?' + urllib.parse.urlencode({'qtype': 'ref', 'q': q, 'limit': 60})


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as v:
        return json.loads(v.read().decode('utf-8'))


def mag(s):
    return {x.strip() for x in (s or '').split(';') if x.strip()}


def lekerdez(q, max_szazad=None):
    """[(family_id, mag, szerzo, mu, szazad, nyelv, n_bi)]: a családok, amelyek magjában a kérdés minden verse áll, és
    azok a tanúik, akik a mag minden versét idézik."""
    kerdes = {x.strip().lower() for x in q.replace('&', '+').split('+') if x.strip()}
    ki = []
    for f in get(csaladok_url(q)).get('families', []):
        m = mag(f.get('core'))
        if not kerdes <= m:
            continue
        d = get(ALAP + '/api/family/%d?group_thr=0.6' % f['family_id'])
        for w in d.get('witnesses', []):
            if w.get('core_cov') != 1.0 or w.get('secondary'):
                continue
            # század nélküli tanú a korhatáros lekérdezésben nem áll: a kora nem igazolható (üres eredmény, nem kitöltés)
            if max_szazad and (not w.get('century') or w['century'] > max_szazad):
                continue
            ki.append((f['family_id'], ' ; '.join(sorted(m)), w.get('author', ''), w.get('work', ''),
                       w.get('century'), w.get('language', ''), f.get('n_bi', 0)))
    return ki


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    al = p.add_subparsers(dest='parancs', required=True)
    lk = al.add_parser('lekerdez')
    lk.add_argument('q')
    lk.add_argument('--max-szazad', type=int, default=None)
    a = p.parse_args()
    sorok = lekerdez(a.q, a.max_szazad)
    print('\t'.join(('csalad', 'mag', 'szerzo', 'mu', 'szazad', 'nyelv', 'n_bi')))
    for s in sorok:
        print('\t'.join('' if x is None else str(x) for x in s))
    print('# scope=chain_lineage q="%s" | forras=%s | ts=%s | talalat=%d' % (
        a.q, csaladok_url(a.q), datetime.date.today().isoformat(), len(sorok)))


if __name__ == '__main__':
    main()
