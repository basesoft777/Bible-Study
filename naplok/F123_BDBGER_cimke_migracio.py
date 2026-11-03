"""F123.BDBGER: a `szotar_szakasz_cimke.tsv` (SEMA 2.40) átkulcsolása: új `bdb_id` oszlop a `strong` után.

Régi kulcs: szotar + strong + szakasz. Új kulcs: szotar + strong + bdb_id + szakasz. A BDB-sor `bdb_id`-je az a
szócikk, amelyben a `bdb_szakaszok.tsv` (2.30) a szakasz útvonalát hordozza (a záró `/-` levágásával összevetve);
ha ez nem pontosan egy szócikk, a szkript megáll, választás nélkül. A Thayer- és a TBESG-sor `bdb_id`-je üres.

Írás előtt és után összevet: a sorok száma és sorrendje, és minden régi mező változatlan; csak a beszúrt oszlop új.
A leképezést (régi kulcs → új kulcs) kiírja (`naplok/F123_BDBGER_cimke_lekepezes.tsv`).

    python naplok/F123_BDBGER_cimke_migracio.py            # szárazon: csak a leképezés
    python naplok/F123_BDBGER_cimke_migracio.py --ir       # írja a táblát
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'szotar_szakasz_cimke.tsv')
SZAKASZOK = os.path.join(ROOT, 'adat', 'bdb_szakaszok.tsv')
LEKEPEZES = os.path.join(ROOT, 'naplok', 'F123_BDBGER_cimke_lekepezes.tsv')
REGI_FEJ = ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu', 'proveniencia', 'megjegyzes']
UJ_FEJ = ['szotar', 'strong', 'bdb_id', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu', 'proveniencia', 'megjegyzes']


def vag(ut):
    while ut.endswith('/-'):
        ut = ut[:-2]
    return ut


def sorok_be(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    s = nyers.split(sorveg)
    if s and s[-1] == '':
        s = s[:-1]
    return s, sorveg


def main():
    ir = '--ir' in sys.argv
    sz_sorok, _ = sorok_be(SZAKASZOK)
    sz_sorok = [s for s in sz_sorok if s and not s.startswith('#')]
    fej = sz_sorok[0].split('\t')
    utak = {}
    for s in sz_sorok[1:]:
        if not s or s.startswith('#'):
            continue
        r = dict(zip(fej, s.split('\t')))
        utak.setdefault((r['strong'], vag(r['utvonal'])), set()).add(r['bdb_id'])
    sorok, sorveg = sorok_be(TABLA)
    if sorok[0].split('\t') != REGI_FEJ:
        raise SystemExit('megállás: a fejléc nem a régi: %s' % sorok[0])
    uj, lek, hibak = ['\t'.join(UJ_FEJ)], ['\t'.join(['szotar', 'strong', 'szakasz', 'regi_kulcs', 'uj_kulcs', 'bdb_id_jeloltek'])], []
    for s in sorok[1:]:
        m = s.split('\t')
        if len(m) != len(REGI_FEJ):
            raise SystemExit('megállás: mezőszám: %r' % s)
        if m[0] == 'BDB':
            j = sorted(utak.get((m[1], vag(m[2])), set()))
            if len(j) != 1:
                hibak.append('%s %s %s: a szakasz %d szócikkben áll (%s)' % (m[0], m[1], m[2], len(j), ', '.join(j)))
                b = ''
            else:
                b = j[0]
        else:
            j, b = [], ''
        uj.append('\t'.join(m[:2] + [b] + m[2:]))
        lek.append('\t'.join([m[0], m[1], m[2], '%s|%s|%s' % (m[0], m[1], m[2]), '%s|%s|%s|%s' % (m[0], m[1], b, m[2]),
                              ','.join(j)]))
    if hibak:
        raise SystemExit('megállás, nem egyértelmű szócikk:\n' + '\n'.join(hibak))
    # összevetés: minden régi mező változatlan, a sorrend is
    for a, b in zip(sorok[1:], uj[1:]):
        ma, mb = a.split('\t'), b.split('\t')
        if mb[:2] + mb[3:] != ma:
            raise SystemExit('megállás: a sor megváltozna: %r' % a)
    if len(uj) != len(sorok):
        raise SystemExit('megállás: sorszám')
    with open(LEKEPEZES, 'w', encoding='utf-8', newline='') as f:
        f.write('# F123.BDBGER: a szotar_szakasz_cimke.tsv régi kulcsa → új kulcsa (scope=adat/szotar_szakasz_cimke.tsv | '
                'forras=naplok/F123_BDBGER_cimke_migracio.py + adat/bdb_szakaszok.tsv | ts=2026-11-03)\n')
        f.write('\n'.join(lek) + '\n')
    print('sorok: %d, ebből BDB: %d, mind egyértelmű' % (len(sorok) - 1, sum(1 for s in sorok[1:] if s.startswith('BDB\t'))))
    if ir:
        with open(TABLA, 'w', encoding='utf-8', newline='') as f:
            f.write(sorveg.join(uj) + sorveg)
        vissza, _ = sorok_be(TABLA)
        if vissza != uj:
            raise SystemExit('megállás: a visszaolvasott tábla eltér')
        print('írva: %s' % TABLA)


if __name__ == '__main__':
    main()
