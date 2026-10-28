"""F131.3.20: a `adat/bdb_vers_jelentes.tsv` (2.29) változása a DT-F131k (a) és a DT-F131l (A) javítása után — csak olvas.

A régi tábla a git HEAD-ből (vagy az első argumentum fájljából), az új a munkafa fájlja. Kimenet (stdout): sorszám, hozzáadott /
elveszett sor (kulcs: strong, poz, nyers, karoli_vers, utvonal — sorszám nélkül), az érintett Strongok, a régi sorok közül más
`sorszam`-ot kapók száma, az új sorok mintája, a H7121/H8034 változása, és az összevetés a memóriabeli A-méréssel
(`naplok/F131_bdb_tartomany_meres.py`: +1 438). TSV `split('\t')`.

    python naplok/F131_bdb_tartomany_valtozas.py [régi_tábla]
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
UT = os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv')


def sorok(szoveg):
    return [s.split('\t') for s in szoveg.split('\n')[3:] if s]


def kulcs(r):
    return (r[0], r[3], r[4], r[7], r[11])


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8', newline='') as f:
            regi = sorok(f.read())
        forras = sys.argv[1]
    else:
        regi = sorok(subprocess.run(['git', 'show', 'HEAD:adat/bdb_vers_jelentes.tsv'], cwd=GYOKER, capture_output=True,
                                    check=True).stdout.decode('utf-8'))
        forras = 'git HEAD'
    with open(UT, encoding='utf-8', newline='') as f:
        uj = sorok(f.read())
    print('proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes (régi: %s; új: munkafa) | forras=naplok/F131_bdb_tartomany_valtozas.py | ts=%s'
          % (forras, datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
    rc = collections.Counter(kulcs(r) for r in regi)
    uc = collections.Counter(kulcs(r) for r in uj)
    plusz, minusz = uc - rc, rc - uc
    print('sorok: régi %d, új %d; hozzáadott %d, elveszett %d' % (len(regi), len(uj), sum(plusz.values()), sum(minusz.values())))
    st = sorted({k[0] for k in plusz} | {k[0] for k in minusz})
    print('érintett Strong: %d; új Károli-igehely (nem üres): %d' % (len(st), len({(k[0], k[3]) for k in plusz if k[3]})))
    regi_sz = {}
    for r in regi:
        regi_sz.setdefault((r[0], kulcs(r)), []).append(r[2])
    eltolt = 0
    for r in uj:
        sz = regi_sz.get((r[0], kulcs(r)))
        if sz and r[2] not in sz:
            eltolt += 1
    print('a régi sorok közül más sorszámot kap: %d' % eltolt)
    i = {r[0]: r for r in uj}
    mod = collections.Counter(r[5] for r in uj if kulcs(r) in plusz)
    print('a hozzáadott sorok konyv_feloldas szerint: %s' % dict(mod))
    for k in sorted(minusz):
        print('  - %s poz=%s %r → %s (%s)' % (k[0], k[1], k[2], k[3] or '—', k[4]))
    for k in sorted(plusz)[:10]:
        print('  + %s poz=%s %r → %s (%s)' % (k[0], k[1], k[2], k[3] or '—', k[4]))
    for s in ('H7121', 'H8034'):
        for k in sorted(plusz):
            if k[0] == s:
                print('  [arany] + %s %r → %s (%s)' % (s, k[2], k[3], k[4]))
        for k in sorted(minusz):
            if k[0] == s:
                print('  [arany] - %s %r → %s (%s)' % (s, k[2], k[3], k[4]))
    for r in uj:
        if 'forras_javitas' in r[12]:
            print('  [forras_javitas] %s sorszam %s nyers %r → %s (%s) okkod %s' % (r[0], r[2], r[4], r[7], r[11], r[12]))


if __name__ == '__main__':
    main()
