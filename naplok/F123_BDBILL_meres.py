#!/usr/bin/env python
"""F123.BDBILL mérés: a `bdb_szakasz_hu.tsv` három állapota soronként (DT-F123y).

  T0 — a commitolt tábla (HEAD; a szkript a `--t0` fájlt olvassa, alapból `git show HEAD:adat/bdb_szakasz_hu.tsv`);
  T1 — a mai bemenetből, a régi logikával (`hu_illeszt.general(..., egy_az_egyhez=False)`: összefűzés + horgonyos újraszabdalás);
  T2 — a mai bemenetből, az új logikával (az igazolt `sz<n>` 1:1).

Mér: Strong- és sorszám, kategóriák, hány sor változik T1→T2 (a logika hatása) és T0→T2 (a teljes hatás), és hány sor hordozott
T0-ban / T1-ben a saját `sz<n>` sora helyett más szakasz szövegét („idegen”), vagy maradt üres saját fordítás mellett. A sor saját
szövege a T2 `szoveg_hu`-ja (= a saját `sz<n>` sor). Kimenet: stdout (a naplóba kivonat kerül). Fájlt nem ír.

Futtatás: python naplok/F123_BDBILL_meres.py [--t0 PATH] [--minta N]
"""
import argparse
import collections
import os
import random
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'bdb_jelolt'))
import hu_illeszt as hi  # noqa: E402

FEJ = hi.FEJLEC
KAT, SZ = FEJ.index('kategoria'), FEJ.index('szoveg_hu')


def t0_sorok(ut):
    if ut:
        with open(ut, encoding='utf-8', newline='') as f:
            szoveg = f.read()
    else:
        szoveg = subprocess.run(['git', 'show', 'HEAD:adat/bdb_szakasz_hu.tsv'], cwd=GYOKER, capture_output=True,
                                check=True).stdout.decode('utf-8')
    return [x.split('\t') for x in szoveg.split('\n')[3:] if x]


def kulcsolt(sorok):
    return collections.OrderedDict(((r[0], r[1]), r) for r in sorok)


def norm(t):
    return ' '.join((t or '').split())


def idegen(r, sajat, strong_sz):
    """'idegen' (a szöveg eleje más szakaszé, a sajátban nincs), 'ures' (saját fordítás van, a sor üres), 'reszleges' (a szöveg
    a saját szakasz szövegét csak részben fedi), 'azonos' — a saját szöveghez mérve."""
    t, s = norm(r[SZ]), norm(sajat)
    if not s:
        return 'azonos' if not t else 'reszleges'
    if not t:
        return 'ures'
    if t == s:
        return 'azonos'
    eleje = t[:25]
    if eleje in s:
        return 'reszleges'
    if any(eleje in norm(m) for m in strong_sz if norm(m) != s):
        return 'idegen'
    return 'reszleges'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t0')
    ap.add_argument('--minta', type=int, default=8)
    a = ap.parse_args()
    t0 = kulcsolt(t0_sorok(a.t0))
    t1 = kulcsolt(hi.general('meres', egy_az_egyhez=False)[0])
    t2 = kulcsolt(hi.general('meres')[0])
    sz11 = [k for k, r in t2.items() if r[KAT] == 'szakasz']
    sz_strong = sorted({k[0] for k in sz11})
    nem_igazolt = sorted({r[0] for r in t2.values() if '1:1 nem igazolt' in r[-1]})
    print('proveniencia: scope=bdb_szakasz_hu.tsv (T0 HEAD, T1 régi logika, T2 új logika) | forras=naplok/F123_BDBILL_meres.py '
          '+ eszkozok/bdb_jelolt/hu_illeszt.py@%s | ts=2026-11-03' % hi.kod_hash()[:12])
    for nev, t in (('T0', t0), ('T1', t1), ('T2', t2)):
        print('%s: Strong %d, sor %d; kategória %s' % (nev, len({k[0] for k in t}), len(t),
                                                       dict(collections.Counter(r[KAT] for r in t.values()))))
    print('szakaszos, igazolt 1:1 Strong: %d (sor %d); szakaszos, nem igazolt: %d %s'
          % (len(sz_strong), len(sz11), len(nem_igazolt), nem_igazolt[:20]))

    def valtozas(x, y, csak=None):
        ks = [k for k in y if (csak is None or k[0] in csak)]
        uj = [k for k in ks if k not in x]
        mas = [k for k in ks if k in x and norm(x[k][SZ]) != norm(y[k][SZ])]
        return uj, mas

    for nev, x in (('T1→T2 (a logika hatása)', t1), ('T0→T2 (a teljes hatás)', t0)):
        uj, mas = valtozas(x, t2)
        print('%s: új sor %d (%d Strong); szövegében változó sor %d (%d Strong)'
              % (nev, len(uj), len({k[0] for k in uj}), len(mas), len({k[0] for k in mas})))
    # kategória előtte → utána, a szakaszos Strongok sorain
    for nev, x in (('T1', t1), ('T0', t0)):
        atm = collections.Counter()
        osztaly = collections.Counter()
        osztaly_kat = collections.Counter()
        strong_idegen = collections.Counter()
        for k in sz11:
            if k not in x:
                continue
            atm[(x[k][KAT], t2[k][KAT])] += 1
        # Strongonként a saját sz-szövegek listája egyszer
        szovegek = collections.defaultdict(list)
        for k in sz11:
            szovegek[k[0]].append(t2[k][SZ])
        for k in sz11:
            if k not in x:
                continue
            o = idegen(x[k], t2[k][SZ], szovegek[k[0]])
            osztaly[o] += 1
            osztaly_kat[(x[k][KAT], o)] += 1
            if o == 'idegen':
                strong_idegen[k[0]] += 1
        print('%s → T2 kategória (szakaszos Strongok %s-beli sorai): %s' % (nev, nev, dict(atm)))
        print('%s sorai a saját sz<n> szöveghez mérve: %s' % (nev, dict(osztaly)))
        print('%s kategória × viszony: %s' % (nev, dict(sorted(osztaly_kat.items()))))
        print('%s: idegen szöveget hordozó sor %d, %d Strongban; legtöbb: %s'
              % (nev, osztaly['idegen'], len(strong_idegen), strong_idegen.most_common(10)))
    # szúrópróba: véletlen (rögzített mag) Strongok, ahol T1 és T2 eltér
    uj, mas = valtozas(t1, t2)
    ut = FEJ.index('utvonal')
    fejes = [k for k in mas if t2[k][ut] in ('cim', 'fej')]
    print('T1→T2 változó sor, ebből cím/fej (a cím saját sz1-et kap, a fej már nem hordozza a címet): %d; többi: %d (%d Strong)'
          % (len(fejes), len(mas) - len(fejes), len({k[0] for k in mas if t2[k][ut] not in ('cim', 'fej')})))
    mas = [k for k in mas if t2[k][ut] not in ('cim', 'fej')]
    jelolt = sorted({k[0] for k in mas})
    random.seed(123)
    minta = sorted(random.sample(jelolt, min(a.minta, len(jelolt)))) + (['H2416'] if 'H2416' in jelolt else [])
    print('\nszúrópróba (mag 123): %s' % minta)
    for st in minta:
        ks = [k for k in mas if k[0] == st][:2] if st != 'H2416' else [k for k in mas if k[0] == st and 13 <= int(k[1]) <= 19]
        for k in ks:
            print('  %s %s [%s → %s]' % (st, k[1], t1[k][KAT], t2[k][KAT]))
            print('    T1: %s' % norm(t1[k][SZ])[:110])
            print('    T2: %s' % norm(t2[k][SZ])[:110])


if __name__ == '__main__':
    main()
