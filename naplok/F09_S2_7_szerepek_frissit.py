"""F09 S2.7: az adat/szotar_szerepek.tsv `allapot` es `forras` oszlopanak frissitese.

A tabla sor-szerkezete (26 adatsor, kulcs: nyelv + sorrend) nem valtozik; csak a kijelolt
sorok `forras` es `allapot` mezoje. Iras elott a sorok osszevetese: minden nem kijelolt sor,
a komment- es a fejlecsor bajtra valtozatlan, a kijelolt sorokban csak az 4. es 5. oszlop
(forras, allapot) terhet el. Ir: '\\t'.join, csv nelkul.

Hasznalat:
    python naplok/F09_S2_7_szerepek_frissit.py                 # szarazon: a kulonbseg listaja
    python naplok/F09_S2_7_szerepek_frissit.py --ir            # ir
    python naplok/F09_S2_7_szerepek_frissit.py --csak gorog7,heber5 --ir   # reszhalmaz
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TSV = os.path.join(ROOT, 'adat', 'szotar_szerepek.tsv')

# (nyelv, sorrend) -> (uj forras vagy None = valtozatlan, uj allapot)
CEL = {
    ('gorog', 3): (None, 'adatosítva'),
    ('gorog', 7): (None, 'adatosítva'),
    ('gorog', 10): ('kiejtes.py szabálytábla + adat/kiejtes_kivetelek.tsv (görög kivételek); a görög alak és lemma magyaros átírása', 'adatosítva'),
    ('heber', 3): (None, 'adatosítva'),
    ('heber', 5): (None, 'adatosítva'),
    ('heber', 7): (None, 'adatosítva'),
    ('heber', 8): (None, 'adatosítva'),
    ('heber', 9): ('UBS DBH versenkénti jelentés (az ÓSZ-i igehelyek MT-számozás szerint párosítva, konkordancia/Karoli_versmegfeleltetes.tsv); '
                   'BSB angol szószintű híd (konkordancia/BSB_Strongs.tsv, F16; csak a 36 importált ÓSZ-könyv, ÚSZ szándékosan nincs, a görög réteg a Macula (#87)) '
                   'és KJV angol szószintű híd (konkordancia/KJV_Strongs_teljes.tsv, F19, javaslat-állapotú; az eBible-ASV forráshibás, nincs a repóban, l. DT19/ELLENOR_F19): '
                   'a render ma csak az UBS DBH-t tölti (F09 S2.3), a BSB/KJV híd nincs renderelve', 'adatosítva'),
    ('heber', 10): (None, 'adatosítva'),
}


def main():
    csak = None
    for i, a in enumerate(sys.argv):
        if a == '--csak':
            csak = set(sys.argv[i + 1].split(','))
    with open(TSV, encoding='utf-8', newline='') as f:
        regi = f.read()
    assert '\r' not in regi, 'a tabla LF-es (eol=lf)'
    sorok = regi.split('\n')
    uj = []
    valtozott = []
    for sor in sorok:
        if not sor or sor.startswith('#') or sor.startswith('nyelv\t'):
            uj.append(sor)
            continue
        mezok = sor.split('\t')
        assert len(mezok) == 5, mezok
        kulcs = (mezok[0], int(mezok[1]))
        nev = '%s%d' % kulcs
        if kulcs in CEL and (csak is None or nev in csak):
            forras, allapot = CEL[kulcs]
            uj_mezok = list(mezok)
            if forras is not None:
                uj_mezok[3] = forras
            uj_mezok[4] = allapot
            if uj_mezok != mezok:
                valtozott.append((nev, mezok[4], allapot, forras is not None))
            uj.append('\t'.join(uj_mezok))
        else:
            uj.append(sor)
    uj_szoveg = '\n'.join(uj)
    # sor-osszevetes: ugyanannyi sor, a nem kijelolt sorok es az elso 3 mezo valtozatlan
    assert len(uj) == len(sorok)
    for a, b in zip(sorok, uj):
        if a != b:
            fa, fb = a.split('\t'), b.split('\t')
            assert fa[:3] == fb[:3], (a[:60], b[:60])
    for v in valtozott:
        print('valtozik: %s: allapot %s -> %s%s' % (v[0], v[1], v[2], ' (+forras)' if v[3] else ''))
    if '--ir' in sys.argv:
        with open(TSV, 'w', encoding='utf-8', newline='') as f:
            f.write(uj_szoveg)
        print('irva:', TSV)


if __name__ == '__main__':
    main()
