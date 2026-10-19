#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22.10 (N-F22c) — az újrapárosítandó versek javító mintái könyvenként (API nélkül, determinisztikus).

Az F90 a `TAGNT_kivonat.tsv`-be pótolta a nyers `[..]` / `{..}` jelölésű szó-sorokat. A már párosított ÚSZ-könyvekben
azok a versek, amelyeknek az eredeti tokenlistája azóta eltér a `szavak_<könyv>.tsv` `er` soraitól, új modellhívást
kapnak (a javító menet mintája: `f22/minta_<könyv>_javito.tsv`, az `egyesit.py` ezt felülírásként olvassa). Azok a
versek, amelyeket az `f22/kezi_versek_<könyv>.tsv` kényszerített `kezi` állapotba, de az eredeti szövegük nem változott,
a régi (teljes görög szöveggel kapott) modellválaszt megtartják; a kényszer kivezetése külön lépés (a kimenet: --lista).

Használat:
    python eszkozok/karoli_strong/f22_nf22c_minta.py --lista            # csak a besorolás (írás nélkül)
    python eszkozok/karoli_strong/f22_nf22c_minta.py --ir               # a javító mintafájlok írása
"""
import argparse
import collections
import glob
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

# a már párosított ÚSZ-könyvek (22.8 próba, 22.9 A és B csomag); a 2Kor új futás, nem újrapárosítás
KONYVEK = ('Filem', '2Ján', '3Ján', 'Júd', 'Tit', '2Thessz', '2Pét', '2Tim', '1Thessz', 'Kol', 'Fil', '1Pét', '1Ján',
           'Jak', '1Tim', 'Gal', 'Ef', 'Zsid')


def regi_eredeti(konyv):
    """igehely -> a szavak_<könyv>.tsv `er` sorainak szövege (a párosításkor használt eredeti tokenlista)."""
    ut = os.path.join(tokenek.ROOT, 'adat', 'karoli_strong', 'szavak_%s.tsv' % sonnet_koteg.ascii_nev(konyv))
    ki = collections.defaultdict(list)
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    for s in sorok[1:]:
        m = s.split('\t')
        if m[1] == 'er':
            ki[m[0]].append(m[3])
    return ki


def kezi_kenyszer(konyv):
    ut = os.path.join(tokenek.F22 if hasattr(tokenek, 'F22') else os.path.join(tokenek.ROOT, 'f22'),
                      'kezi_versek_%s.tsv' % sonnet_koteg.ascii_nev(konyv))
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    return [s.split('\t')[0] for s in sorok[1:]]


def besorol(ered=None):
    """{könyv: {'ujra': [igehely], 'felold': [igehely]}}: `ujra` = az eredeti tokenlista változott (vagy a vers eredeti
    nélküli volt), `felold` = a `kezi` kényszer alatt álló, változatlan eredetijű vers."""
    ered = ered if ered is not None else tokenek.betolt_eredeti()
    ki = {}
    for k in KONYVEK:
        regi = regi_eredeti(k)
        ujra, felold = [], []
        for ig in sorted(set(i for i in ered if tokenek.igehely_bont(i) and tokenek.igehely_bont(i)[0] == k) | set(regi),
                         key=lambda i: tokenek.igehely_bont(i)[1:]):
            uj = [x['alak'] for x in ered.get(ig, [])]
            if uj and uj != regi.get(ig):
                ujra.append(ig)
        for ig in kezi_kenyszer(k):
            if ig not in ujra:
                felold.append(ig)
        if ujra or felold:
            ki[k] = {'ujra': ujra, 'felold': felold}
    return ki


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lista', action='store_true')
    ap.add_argument('--ir', action='store_true')
    a = ap.parse_args(argv)
    if not (a.lista or a.ir):
        ap.error('--lista vagy --ir kell')
    karoli, ered = tokenek.betolt_karoli(), tokenek.betolt_eredeti()
    b = besorol(ered)
    for k, d in b.items():
        print('%s: újrapárosítandó %s; kényszer kivezethető (változatlan eredeti) %s' % (k, d['ujra'] or '-', d['felold'] or '-'))
        if a.ir and d['ujra']:
            minta = [s for s in sonnet_koteg.minta_epit(k, karoli, ered) if s['igehely'] in set(d['ujra'])]
            minta = [dict(s, sorsz=i) for i, s in enumerate(minta, 1)]
            ut = sonnet_koteg.minta_ut(k + '_javito')
            sonnet_koteg.minta_ir(ut, minta)
            print('  írva: %s (%d vers)' % (os.path.relpath(ut, tokenek.ROOT), len(minta)))
    print('összesen: újrapárosítandó %d vers, kényszer kivezethető %d vers' % (
        sum(len(d['ujra']) for d in b.values()), sum(len(d['felold']) for d in b.values())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
