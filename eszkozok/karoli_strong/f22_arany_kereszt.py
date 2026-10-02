#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — DT-F22c háttér: a régi arany (konkordancia/Karoli_Strong_kivonat.tsv) kereszttáblája modellenként.

Minden régi-arany hármasra (igehely, Károli-kifejezés, Strong-összetevők) megmondja, hogy a Sonnet saját
válasza, a C (Gemini) saját válasza egyezik-e az arannyal (a halmaz-szabály: az arany-összetevők mind
szerepelnek a kifejezés tokenjeihez linkelt eredeti Strongok között), és ebből négyes kereszttáblát ad:
mindkettő egyezik / csak a Sonnet / csak a C / egyik sem. Azokat a hármasokat, ahol a vers valamelyik modell
oldalán kapuhibás (nincs válasz), külön számolja. Csak számot ír, API nélkül, determinisztikusan.

Használat:
    python eszkozok/karoli_strong/f22_arany_kereszt.py --konyv 1Móz --konyv 2Móz
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import egyesit  # noqa: E402
import f22_elemzes  # noqa: E402
import tokenek  # noqa: E402


def modell_strongok(nezet, ered_vers):
    """{hu_sorszam: set(strong)} egy modell nézetéből."""
    return {h: {ered_vers[e - 1]['strong'] for e in ers} for h, ers in nezet[0].items()}


def egyezik(tl, kif, osszetevok, strongok, ig):
    for i in f22_elemzes.kifejezes_helyek(tl, kif):
        linkelt = set()
        for j in range(len(kif)):
            linkelt |= strongok.get(i + j + 1, set())
        if osszetevok <= linkelt:
            return True
    return False


def szamol(konyv, karoli, ered):
    u = egyesit.utak(konyv)
    sv, cv = egyesit.jsonl_versek(u['sonnet']), egyesit.jsonl_versek(u['c'])
    versek = {ig for ig in karoli if ig.startswith(konyv + ' ')}
    t = {'ss': 0, 'sn': 0, 'ns': 0, 'nn': 0, 'nincs_valasz': 0, 'nincs_hely': 0}
    for ig, szo, strong in tokenek.regi_arany(versek):
        tl = tokenek.tokenizal(karoli[ig])
        kif = tokenek.tokenizal(szo)
        if not f22_elemzes.kifejezes_helyek(tl, kif):
            t['nincs_hely'] += 1
            continue
        s_ok = sv.get(ig, {}).get('allapot') == 'ok'
        c_ok = cv.get(ig, {}).get('allapot') == 'ok'
        if not (s_ok and c_ok) or ig not in ered:
            t['nincs_valasz'] += 1
            continue
        oss = set(strong.split('+'))
        s = egyezik(tl, kif, oss, modell_strongok(egyesit.vers_nezet(sv[ig]['obj']), ered[ig]), ig)
        c = egyezik(tl, kif, oss, modell_strongok(egyesit.vers_nezet(cv[ig]['obj']), ered[ig]), ig)
        t[('s' if s else 'n') + ('s' if c else 'n')] += 1
    return t


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', action='append', required=True)
    a = ap.parse_args(argv)
    karoli, ered = tokenek.betolt_karoli(), tokenek.betolt_eredeti()
    ossz = {}
    for k in a.konyv:
        t = szamol(k, karoli, ered)
        for x, v in t.items():
            ossz[x] = ossz.get(x, 0) + v
        n = t['ss'] + t['sn'] + t['ns'] + t['nn']
        print('%s: n=%d | mindkettő egyezik %d | csak a Sonnet %d | csak a C %d | egyik sem %d | (nincs választ: %d, a kifejezés nincs a versben: %d)'
              % (k, n, t['ss'], t['sn'], t['ns'], t['nn'], t['nincs_valasz'], t['nincs_hely']))
    t = ossz
    n = t['ss'] + t['sn'] + t['ns'] + t['nn']
    if len(a.konyv) > 1 and n:
        print('ÖSSZESEN: n=%d | mindkettő egyezik %d | csak a Sonnet %d | csak a C %d | egyik sem %d' % (n, t['ss'], t['sn'], t['ns'], t['nn']))
        print('Sonnet egyezés: %s; C egyezés: %s' % (f22_elemzes.pct(t['ss'] + t['sn'], n), f22_elemzes.pct(t['ss'] + t['ns'], n)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
