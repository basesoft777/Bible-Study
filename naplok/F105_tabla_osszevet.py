"""F105 (FELADATOK #105, DT-F105a): a javítótábla újragenerálása írás előtti összevetéssel.

A `forras_javit.general()` új sorait összeveti a mostani `adat/bdb_forras_javitas.tsv` soraival (a fejléc nélkül):
  - a meglévő `javitva` sorok (minden hibaosztály) nem változhatnak: ha bármelyik hiányzik vagy eltér, a szkript megáll, és
    nem ír;
  - a változás bontása: törölt / új sorok, (hiba, régi állapot → új állapot) szerint, a sor kulcsán (strong, sorszam, hiba,
    szo_sorszam, elofordulas, forras_alak).
Csak `--ir` mellett írja a táblát (a generátor saját `fajl_szoveg`-ével); a számokat a `--ki` fájlba is kiírja.
Futtatás: python naplok/F105_tabla_osszevet.py --ts 2026-10-18 --ts-heber-sorrend 2026-11-01 --ts-atiras 2026-11-03
          --ts-hivatkozott-vers 2026-11-10 --ki <fájl> [--ir]
"""
import argparse
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'bdb_jelolt'))
import forras_javit as FJ  # noqa: E402


def kulcs(s):
    return (s[0], s[1], s[3], s[4], s[5], s[6])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', required=True)
    ap.add_argument('--ts-heber-sorrend')
    ap.add_argument('--ts-atiras')
    ap.add_argument('--ts-hivatkozott-vers')
    ap.add_argument('--ki', required=True)
    ap.add_argument('--ir', action='store_true')
    a = ap.parse_args()
    with open(FJ.KI_UT, encoding='utf-8', newline='') as f:
        regi = [s.split('\t') for s in f.read().split('\n') if s and not s.startswith('#')][1:]
    uj, stat = FJ.general(a.ts, a.ts_heber_sorrend, a.ts_atiras, a.ts_hivatkozott_vers)
    r_k = collections.defaultdict(list)
    for s in regi:
        r_k[kulcs(s)].append(s)
    u_k = collections.defaultdict(list)
    for s in uj:
        u_k[kulcs(s)].append(s)
    hibak, c = [], collections.Counter()
    for k, rs in r_k.items():
        us = u_k.get(k, [])
        for r in rs:
            if r[8] == 'javitva' and r not in us:
                hibak.append(k)
        if not us:
            c['torolt|%s|%s' % (k[2], rs[0][8])] += len(rs)
        elif rs != us:
            for r, u in zip(rs, us):
                if r != u:
                    c['valtozott|%s|%s->%s' % (k[2], r[8], u[8])] += 1
    for k, us in u_k.items():
        if k not in r_k:
            c['uj|%s|%s' % (k[2], us[0][8])] += len(us)
    with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('regi_sor\t%d\nuj_sor\t%d\nvaltozatlan_javitva_serult\t%d\n' % (len(regi), len(uj), len(hibak)))
        for k, v in sorted(c.items()):
            f.write('%s\t%d\n' % (k, v))
        for k, v in sorted(stat.items()):
            f.write('stat|%s\t%d\n' % (k, v))
    print('régi: %d, új: %d, sérült javitva: %d; változás: %s' % (len(regi), len(uj), len(hibak), dict(c)))
    if hibak:
        print('MEGÁLL: meglévő javitva sor változna (%d), a tábla nem íródik' % len(hibak))
        return 1
    if a.ir:
        szoveg = FJ.fajl_szoveg(uj, a.ts, a.ts_heber_sorrend, a.ts_atiras, a.ts_hivatkozott_vers)
        with open(FJ.KI_UT, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('írva: %s' % FJ.KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
