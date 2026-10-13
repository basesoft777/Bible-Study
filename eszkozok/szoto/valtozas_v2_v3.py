"""F94.2 (FELADATOK #94): a v2 → v3 változás a teljes Károlin — a változott kimenetű alakok száma és rögzített
véletlen-maggal kiválasztott 30 változás a kézi átnézéshez (naplok/SZOTOVEZES_meres.md).

A korpusz-lexikon minden kisbetűs és mondat belsejében nagybetűs alakján fut (ugyanaz a halmaz, mint az átvétel
egyezés-próbájánál). Használat: python eszkozok/szoto/valtozas_v2_v3.py [--valtozat A] [--mag 20261013] [--n 30]"""
import argparse
import datetime
import hashlib
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import hibrid  # noqa: E402
import hibrid_v2  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--valtozat', default='A')
    ap.add_argument('--mag', type=int, default=20261013)
    ap.add_argument('--n', type=int, default=30)
    a = ap.parse_args()
    hibrid.valtozat(a.valtozat)
    hibrid_v2.valtozat('A' if a.valtozat == 'A' else 'C')
    alakok = sorted(set(hibrid.KIS) | set(hibrid.NAGY_BELUL))
    valt = []
    for w in alakok:
        r2, r3 = hibrid_v2.to(w), hibrid.to(w)
        if r2 != r3:
            valt.append((w, r2, r3, hibrid.KIS.get(w, 0) + hibrid.NAGY_BELUL.get(w, 0)))
    tok = sum(v[3] for v in valt)
    minta = random.Random(a.mag).sample(valt, min(a.n, len(valt)))
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
    print(f'A teljes Károli {len(alakok)} alakjából **{len(valt)}** alak kimenete változott (v2 {a.valtozat} → v3 {a.valtozat}), '
          f'{tok} előfordulás.\n')
    print(f'| # | alak | előfordulás | v2 | v3 |')
    print('|---|---|---|---|---|')
    for i, (w, r2, r3, n) in enumerate(sorted(minta), 1):
        print(f'| {i} | {w} | {n} | {r2} | {r3} |')
    print(f'\nscope=a korpusz-lexikon kisbetűs és mondat belsejében nagybetűs alakjai | forras=eszkozok/szoto/valtozas_v2_v3.py '
          f'(mag {a.mag}) + hibrid_v2.py (sha256:{h(os.path.join(ITT, "hibrid_v2.py"))}) + hibrid.py (sha256:{h(os.path.join(ITT, "hibrid.py"))}) '
          f'+ karoli_lexikon.tsv (sha256:{h(hibrid._LEX)}) | ts={ts}')


if __name__ == '__main__':
    main()
