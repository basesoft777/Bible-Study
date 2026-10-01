#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a futások összesítése (kapuhiba, költség); a jelentés számai innen jönnek.

Olvas: f22/valaszok/sonnet/<könyv>.jsonl, f22/valaszok/c/<könyv>.jsonl, f22/futasnaplo.tsv.
Nem hív hálózatot. A kapuhiba versszinten: `elso_probara` = az első próbálkozásra nem ment át a
kapun (probalkozas=2 vagy végleg hibás), `vegleg` = a második után is kapuhibás.

Használat:
    python eszkozok/karoli_strong/f22_statisztika.py --konyv 1Móz [--ig-koteg 14] [--vetit 1533]
"""

import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sonnet_koteg  # noqa: E402

F22 = sonnet_koteg.F22


def sorok(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def kapu_stat(sor_lista, ig_koteg=None):
    vers = elso = vegleg = kotegek = 0
    for s in sor_lista:
        if ig_koteg is not None and s['koteg'] > ig_koteg:
            continue
        kotegek += 1
        for v in s['versek'].values():
            vers += 1
            if v['allapot'] != 'ok' or v['probalkozas'] == 2:
                elso += 1
            if v['allapot'] != 'ok':
                vegleg += 1
    return {'kotegek': kotegek, 'versek': vers, 'elso_probara': elso, 'vegleg': vegleg}


def naplo(ut, ig_koteg=None, futas=None):
    if not os.path.exists(ut):
        return {'hivas': 0, 'koltseg': 0.0, 'be': 0, 'ki': 0, 'gond': 0}
    with open(ut, encoding='utf-8') as f:
        sz = [x.rstrip('\n').rstrip('\r').split('\t') for x in f if x.strip()]
    fej = sz[0]
    ki = {'hivas': 0, 'koltseg': 0.0, 'be': 0, 'ki': 0, 'gond': 0}
    for r in sz[1:]:
        d = dict(zip(fej, r))
        if futas and d['futas'] != futas:
            continue
        if ig_koteg is not None and int(d['koteg']) > ig_koteg:
            continue
        ki['hivas'] += 1
        ki['koltseg'] += float(d['koltseg_usd'])
        ki['be'] += int(d['bemenet_token'])
        ki['ki'] += int(d['kimenet_token'])
        ki['gond'] += int(d['gondolkodas_token'])
    return ki


def pct(a, b):
    return '%.1f%% (%d/%d)' % (100.0 * a / b, a, b) if b else 'n.é. (0/0)'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', required=True)
    ap.add_argument('--ig-koteg', type=int, default=None, help='csak a legfeljebb ennyedik kötegig')
    ap.add_argument('--vetit', type=int, default=None, help='vetítés erre a versszámra (a mért versszámból)')
    a = ap.parse_args(argv)
    nev = sonnet_koteg.ascii_nev(a.konyv)
    s = kapu_stat(sorok(sonnet_koteg.valasz_ut(a.konyv)), a.ig_koteg)
    c = kapu_stat(sorok(os.path.join(F22, 'valaszok', 'c', '%s.jsonl' % nev)), a.ig_koteg)
    for nm, x in (('Sonnet', s), ('C', c)):
        print('%s: %d köteg, %d vers; kapuhiba első próbára %s; végleg %s' % (
            nm, x['kotegek'], x['versek'], pct(x['elso_probara'], x['versek']), pct(x['vegleg'], x['versek'])))
    n = naplo(os.path.join(F22, 'futasnaplo.tsv'), a.ig_koteg, 'c/%s' % nev)
    print('C költség: %.6f USD, %d hívás, bemenet %d, kimenet %d (ebből gondolkodás %d) token'
          % (n['koltseg'], n['hivas'], n['be'], n['ki'], n['gond']))
    if a.vetit and c['versek']:
        print('C költség vetítve %d versre: %.4f USD' % (a.vetit, n['koltseg'] * a.vetit / c['versek']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
