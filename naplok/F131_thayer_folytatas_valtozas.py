"""F131.8 (ELLENOR_SZOTARI_GERINC 2., 7.5a): a `adat/thayer_vers_jelentes.tsv` (2.35) változása a jelöletlen folytatás
felvétele után — csak olvas.

A régi tábla a `7d004296` commitból (a javítókör előtti head; vagy az első argumentum fájljából), az új a munkafa fájlja.
Kimenet (stdout): sorszám, hozzáadott / elveszett sor (kulcs: strong, szakasz, konyv, fejezet, vers, utvonal — sorszám
nélkül), az érintett Strongok, a régi sorok közül más `sorszam`-ot kapók száma, a `folytatas` jelű sorok száma, mintasorok,
a Károli-vers nélküli új sorok, és a G1941 változása. TSV `split('\t')`.

    python naplok/F131_thayer_folytatas_valtozas.py [régi_tábla]
"""
import collections
import datetime
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(GYOKER, 'adat', 'thayer_vers_jelentes.tsv')
REGI_COMMIT = '7d004296'
# oszlopok: strong sorszam szakasz konyv fejezet vers karoli_vers utvonal proveniencia


def sorok(szoveg):
    return [s.split('\t') for s in szoveg.split('\n')[3:] if s]


def kulcs(r):
    return (r[0], r[2], r[3], r[4], r[5], r[7])


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8', newline='') as f:
            regi = sorok(f.read())
        forras = sys.argv[1]
    else:
        regi = sorok(subprocess.run(['git', 'show', REGI_COMMIT + ':adat/thayer_vers_jelentes.tsv'], cwd=GYOKER,
                                    capture_output=True, check=True).stdout.decode('utf-8'))
        forras = 'git ' + REGI_COMMIT
    with open(UT, encoding='utf-8', newline='') as f:
        uj = sorok(f.read())
    print('proveniencia: scope=adat/thayer_vers_jelentes.tsv, teljes (régi: %s; új: munkafa) | '
          'forras=naplok/F131_thayer_folytatas_valtozas.py | ts=%s'
          % (forras, datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
    rc = collections.Counter(kulcs(r) for r in regi)
    uc = collections.Counter(kulcs(r) for r in uj)
    plusz, minusz = uc - rc, rc - uc
    print('sorok: régi %d, új %d; hozzáadott %d, elveszett %d'
          % (len(regi), len(uj), sum(plusz.values()), sum(minusz.values())))
    folyt = [r for r in uj if 'folytatas)' in r[8]]
    print('`folytatas` jelű sor: %d; szócikk (Strong): %d' % (len(folyt), len({r[0] for r in folyt})))
    st = sorted({k[0] for k in plusz} | {k[0] for k in minusz})
    print('érintett Strong: %d; új Károli-igehely (nem üres): %d'
          % (len(st), len({(r[0], r[6]) for r in folyt if r[6]})))
    regi_sz = {}
    for r in regi:
        regi_sz.setdefault(kulcs(r), []).append(r[1])
    eltolt = sum(1 for r in uj if regi_sz.get(kulcs(r)) and r[1] not in regi_sz[kulcs(r)])
    print('a régi sorok közül más sorszámot kap: %d' % eltolt)
    nincs = [r for r in folyt if not r[6]]
    print('a folytatás-sorok közül Károli-vers nélkül: %d' % len(nincs))
    for r in nincs:
        print('  [nincs Károli-vers] %s sorszam %s → %s %s:%s (%s)' % (r[0], r[1], r[3], r[4], r[5], r[7]))
    for r in folyt[:12]:
        print('  + %s sorszam %s szakasz %s → %s (%s)' % (r[0], r[1], r[2], r[6] or '—', r[7]))
    for r in uj:
        if r[0] == 'G1941' and 'folytatas)' in r[8]:
            print('  [G1941] + sorszam %s szakasz %s → %s (%s)' % (r[1], r[2], r[6], r[7]))
    for k in sorted(minusz):
        print('  - %s' % (k,))
    return 0


if __name__ == '__main__':
    sys.exit(main())
