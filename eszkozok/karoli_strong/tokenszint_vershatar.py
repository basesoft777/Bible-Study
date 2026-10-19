#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 (N-F22e) — tokenszintű vershatár-gyanú: a Károli-vers egy szakasza a szomszéd eredeti versben áll.

A versbeosztás-detektor (`versbeosztas.py`) versszinten dolgozik: a kulcsok egyezése nem zárja ki, hogy a
Károli és az eredeti (TAGNT/TAHOT) vers *határa* a mondaton belül máshol húzódik (2Kor 8:13–14, 2:12–13,
5:14–15, Zsid 1:1–2, Fil 3:13–14). Ez az eszköz a szomszédos versek hossz-többletét hasonlítja:

  többlet(v) = Károli-szószám(v) − k · eredeti-tokenszám(v),   k = a könyv Károli/eredeti aránya
  gyanú: két szomszédos vers (azonos fejezet) többlete ellentétes előjelű, és mindkettő abszolút értéke
         ≥ max(--min-abs, 3·σ) (σ = a többletek MAD-ból becsült szórása), a kisebb ≥ --min-arany × a nagyobb.

A kimenet JELÖLT-lista: a fordítási hosszkülönbség is adhat téves jelzést (pl. Róm 4:16–17: a határ
rendben van), ezért minden jelöltet a Károli- és az eredeti szöveg szemrevételezése dönt el. A hiányzó
jelzés nem bizonyíték (az eszköz csak a hosszarányra érzékeny). API és hálózat nélkül, determinisztikus.

Használat:
    python eszkozok/karoli_strong/tokenszint_vershatar.py                  # az egész ÚSZ, alap küszöb
    python eszkozok/karoli_strong/tokenszint_vershatar.py Róm 1Kor Jel     # könyvek
    python eszkozok/karoli_strong/tokenszint_vershatar.py --lazabb Róm     # --min-abs 4, --min-arany 0.4
    python eszkozok/karoli_strong/tokenszint_vershatar.py --szoveg Róm     # a jelöltek szövege is
"""
import argparse
import collections
import os
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

UJSZOVETSEG = ('Mt', 'Mk', 'Luk', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol', '1Thessz',
               '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pét', '2Pét', '1Ján', '2Ján', '3Ján',
               'Júd', 'Jel')


def igehely_kulcs(igehely):
    konyv, r = igehely.rsplit(' ', 1)
    fej, vers = r.split(':')
    return konyv, int(fej), int(vers)


def betolt():
    karoli = tokenek.betolt_karoli()
    eredeti = tokenek.betolt_eredeti(versmegf=False)
    return karoli, eredeti


def elemez(konyv, karoli, eredeti, min_abs=6.0, min_arany=0.5):
    """(arány, σ, [(vers_a, vers_b, többlet_a, többlet_b, hu_a, er_a, hu_b, er_b), ...])"""
    versek = [v for v in karoli if igehely_kulcs(v)[0] == konyv and v in eredeti]
    if not versek:
        return None, None, []
    hu = {v: len(tokenek.tokenizal(karoli[v])) for v in versek}
    er = {v: len(eredeti[v]) for v in versek}
    k = sum(hu.values()) / max(1, sum(er.values()))
    tobblet = {v: hu[v] - k * er[v] for v in versek}
    kozep = statistics.median(tobblet.values())
    mad = statistics.median(abs(x - kozep) for x in tobblet.values()) or 1.0
    szoras = 1.4826 * mad
    jeloltek = []
    for a, b in zip(versek, versek[1:]):
        if igehely_kulcs(a)[1] != igehely_kulcs(b)[1]:
            continue
        sa, sb = tobblet[a] - kozep, tobblet[b] - kozep
        if sa * sb < 0 and min(abs(sa), abs(sb)) >= max(min_abs, 3 * szoras) \
                and min(abs(sa), abs(sb)) / max(abs(sa), abs(sb)) >= min_arany:
            jeloltek.append((a, b, round(sa, 1), round(sb, 1), hu[a], er[a], hu[b], er[b]))
    return k, szoras, jeloltek


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('konyvek', nargs='*', help='könyvek (alap: az egész ÚSZ)')
    ap.add_argument('--min-abs', type=float, default=6.0)
    ap.add_argument('--min-arany', type=float, default=0.5)
    ap.add_argument('--lazabb', action='store_true', help='--min-abs 4 --min-arany 0.4')
    ap.add_argument('--szoveg', action='store_true', help='a jelöltek Károli- és eredeti szövege is')
    a = ap.parse_args(argv)
    min_abs, min_arany = (4.0, 0.4) if a.lazabb else (a.min_abs, a.min_arany)
    karoli, eredeti = betolt()
    ossz = 0
    for konyv in (a.konyvek or UJSZOVETSEG):
        k, szoras, jel = elemez(konyv, karoli, eredeti, min_abs, min_arany)
        if k is None:
            print('%-8s nincs adat' % konyv)
            continue
        print('%-8s arány %.3f  σ %.1f  jelölt %d' % (konyv, k, szoras, len(jel)))
        for j in jel:
            print('    %s → %s  többlet %+.1f / %+.1f  (Károli %d, eredeti %d | Károli %d, eredeti %d)' % (
                j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7]))
            if a.szoveg:
                for v in (j[0], j[1]):
                    print('        %s K: %s' % (v, karoli[v]))
                    print('        %s E: %s' % (v, ' '.join(w['alak'] for w in eredeti[v])))
        ossz += len(jel)
    print('összesen: %d jelölt (küszöb: abs ≥ %.0f, arány ≥ %.1f)' % (ossz, min_abs, min_arany))
    return 0


if __name__ == '__main__':
    sys.exit(main())
