"""DT-F22d mérése: a #22 Károli–Strong párosítás melyik következő könyve ad a
legtöbb Károli-adatot a #38 BDB-fordítás adatblokkjának (#56).

A #56 generátor (eszkozok/bdb_adatblokk.py) saját függvényeivel számol:
a lefedett könyvek a kész parok_*.tsv-k, az előfordulások a TAHOT_kivonat.tsv-ből.
Három szakaszt mér a naplok/BDB_FORDITAS_sorrend.tsv sorszámai szerint:
a 6. adagot (407–648, már lefordítva), a 7. adagot (649–969, a következő)
és a teljes hátralévő sort (649–).

Kategóriák szócikkenként: NINCS (nincs Károli-szóalak), kevés (1–4 pár),
van (>= 5 pár). Könyvenkénti nyereség: a NINCS/kevés szócikkek TAHOT-
előfordulásai az adott, még nem lefedett könyvben; mellette, hány NINCS-
szócikk kapna az adott könyvből legalább egy előfordulást.

Futtatás: python naplok/F22_konyvsorrend_meres.py
"""
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import bdb_adatblokk as B  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KEVES = 5
SZAKASZOK = [('6. adag (407–648)', 407, 648), ('7. adag (649–969)', 649, 969),
             ('hátralévő sor (649–)', 649, 10 ** 9)]


def sorrend():
    ki = []
    for m in B.tsv_sorok(B.SORREND_UT):
        if m[0].startswith('#') or m[0] == 'sorszam':
            continue
        ki.append((int(m[0]), m[1]))
    return ki


def konyv(vers):
    return vers.rsplit(' ', 1)[0]


def meres(strongok, lef, tah, par):
    kat = Counter()
    ossz = lefedett = 0
    nyer = Counter()       # NINCS/kevés szócikkek előfordulásai nem lefedett könyvben
    uj = Counter()         # NINCS-szócikkek száma, amelyek az adott könyvben előfordulnak
    for s in strongok:
        sz = B.strong_szam(s)
        t = tah.get(sz, {})
        p = len(par.get(sz, []))
        nincs = not B.karoli_alakok(sz)
        gyenge = nincs or p < KEVES
        kat['NINCS' if nincs else ('kevés' if p < KEVES else 'van')] += 1
        ossz += sum(t.values())
        lefedett += sum(db for v, db in t.items() if konyv(v) in lef)
        konyvei = set()
        for v, db in t.items():
            kv = konyv(v)
            if kv in lef:
                continue
            konyvei.add(kv)
            if gyenge:
                nyer[kv] += db
        if nincs:
            for kv in konyvei:
                uj[kv] += 1
    return kat, ossz, lefedett, nyer, uj


def main():
    lef = set(B.lefedett_konyvek())
    tah = B.tahot_versek()
    par = B.parok()
    sor = sorrend()
    print('scope=BDB_FORDITAS_sorrend.tsv; lefedett: %s | forras=eszkozok/bdb_adatblokk.py '
          '(adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv) | ts=%s'
          % (', '.join(sorted(lef)), B.ts_most()))
    for nev, a, b in SZAKASZOK:
        strongok = [s for n, s in sor if a <= n <= b]
        kat, ossz, lefedett, nyer, uj = meres(strongok, lef, tah, par)
        n = len(strongok)
        print('\n## %s — %d szócikk' % (nev, n))
        for k in ('van', 'kevés', 'NINCS'):
            print('  %-6s %5d  (%.1f%%)' % (k, kat[k], 100 * kat[k] / n if n else 0))
        print('  TAHOT-előfordulás: %d; lefedett könyvben: %d (%.1f%%)'
              % (ossz, lefedett, 100 * lefedett / ossz if ossz else 0))
        print('  könyv | NINCS/kevés szócikkek előfordulása | NINCS-szócikk, amely előfordul benne')
        for kv, db in nyer.most_common(12):
            print('  %-6s %6d %6d' % (kv, db, uj[kv]))
        if 'Bír' not in dict(nyer.most_common(12)):
            print('  %-6s %6d %6d   (a #22 jelenlegi következő könyve)' % ('Bír', nyer['Bír'], uj['Bír']))


if __name__ == '__main__':
    main()
