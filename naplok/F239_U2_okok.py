"""F239 U2 — a TEREMT-001 két elutasítási oka a mintaszótárban, és a besorolás próbája (egyszeri szkript).

python naplok/F239_U2_okok.py        (próba: minden TEREMT-001 elutasított sor besorolható-e, melyik címkével)
python naplok/F239_U2_okok.py --ir   (a két sor hozzáfűzése az adat/elutasitasi_okok.tsv-hez, utána a próba)
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'eszkozok'))

import szerep_kizart as SZKZ  # noqa: E402

UT = 'adat/elutasitasi_okok.tsv'
PROV = ('scope=manual | forras=F239 U2, a TEREMT-001 jelöltdöntései (naplok/F239_hatar.md; a végrehajtó: '
        'claude-opus-5-5) | ts=2026-11-23')
UJ = [
    ['101', 'TEREMT-001', '^összesítő sor', 'a Károli mélység-szava más szót fordít (összesítő sor)',
     'a Károli „mély”, „mélység”, „örvény” vagy „fenékig” szava a versben nem a tehómot és nem az ἄβυσσος-t '
     'fordítja, hanem más mélység-szót (pl. a tenger mélye, verem, mély álom) vagy körülírást', PROV],
    ['102', 'TEREMT-001', '^a septuaginta többlete', 'a Septuaginta többlete, a héberben nincs tehóm',
     'a görög fordítás ἄβυσσος-t hoz, a héber versben viszont más szó áll, vagy a görög szöveg a héberen túl ismétel',
     PROV],
]


def main():
    if '--ir' in sys.argv:
        with open(UT, encoding='utf-8', newline='') as f:
            regi = f.read()
        if 'TEREMT-001\t^összesítő sor' in regi:
            sys.exit('HIBA: a sorok már benne vannak')
        if not regi.endswith('\n'):
            sys.exit('HIBA: a fájl nem sorvéggel végződik')
        uj = regi + ''.join('\t'.join(s) + '\n' for s in UJ)
        with open(UT, 'w', encoding='utf-8', newline='') as f:
            f.write(uj)
        with open(UT, encoding='utf-8', newline='') as f:
            if f.read()[:len(regi)] != regi:
                sys.exit('HIBA: a régi rész változott')
        print('írva: 2 sor')
    minta = SZKZ.okok('TEREMT-001', UT)
    db = collections.Counter()
    with open('adat/jeloltek.tsv', encoding='utf-8') as f:
        sorok = [s.rstrip('\n').split('\t') for s in f if not s.startswith('#')]
    fej = sorok[0]
    for m in sorok[1:]:
        r = dict(zip(fej, m))
        if r.get('id') != 'TEREMT-001' or r.get('dontes') != 'elutasítva':
            continue
        try:
            c = SZKZ.elutasitas_oka((r['indoklas'] or '').partition(' | ')[0], minta)
        except SZKZ.BeNemSorolhato as e:
            c = 'BE NEM SOROLHATÓ: %s' % e
        db[c] += 1
        print('  %-12s %s' % (r['igehely'], c))
    print(dict(db))


if __name__ == '__main__':
    main()
