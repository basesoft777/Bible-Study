"""F127 B1 (DT-F127b (i), DT-F127d (1)): az `adat/jeloltek.tsv` kulcsbővítése.

Négy új oszlop a sor végén: `jelolt_tipus` (`elofordulas` | `motivumkozi`),
`cel_id`, `cel_igehely`, `cel_alpont`. A kulcs `id + igehely + jelolt_tipus +
cel_id`. A meglévő sorok `jelolt_tipus=elofordulas`, a másik három mező üres.

Olvasás split('\\t'), írás '\\t'.join() (CLAUDE.md, TSV-szabály). Írás előtt
ellenőrzi, hogy minden régi sor első 9 mezője bájtra azonos marad, és csak a
négy új mező kerül a végére; eltérésnél nem ír.

    python eszkozok/f127_jeloltek_bovit.py        # szárazfutás
    python eszkozok/f127_jeloltek_bovit.py --ir
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'adat', 'jeloltek.tsv')

REGI_FEJLEC = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas',
               'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'datum']
UJ_MEZOK = ['jelolt_tipus', 'cel_id', 'cel_igehely', 'cel_alpont']
REGI_KOMMENT = '# A kereszthivatkozas-naplo gepi alakja. Kulcs: id + igehely. Sema: adat/SEMA.md 2.4'
UJ_KOMMENT = ('# A kereszthivatkozas-naplo gepi alakja. Kulcs: id + igehely + jelolt_tipus + cel_id '
              '(DT277). Sema: adat/SEMA.md 2.4')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ir', action='store_true')
    a = p.parse_args()
    with open(TSV, 'rb') as f:
        szoveg = f.read().decode('utf-8')
    if '\r' in szoveg:
        print('HIBA: CR a táblában')
        return 1
    sorok = szoveg.split('\n')
    veg_ures = sorok[-1] == ''
    if veg_ures:
        sorok = sorok[:-1]
    if sorok[0] != REGI_KOMMENT:
        print('HIBA: váratlan első sor: %r' % sorok[0][:120])
        return 1
    if sorok[1].split('\t') != REGI_FEJLEC:
        if sorok[1].split('\t') == REGI_FEJLEC + UJ_MEZOK:
            print('a tábla már bővítve -- nincs teendő')
            return 0
        print('HIBA: váratlan fejléc')
        return 1
    uj = [UJ_KOMMENT, '\t'.join(REGI_FEJLEC + UJ_MEZOK)]
    adat = 0
    for s in sorok[2:]:
        if not s or s.startswith('#'):
            uj.append(s)
            continue
        m = s.split('\t')
        if len(m) != len(REGI_FEJLEC):
            print('HIBA: mezőszám %d: %r' % (len(m), s[:100]))
            return 1
        uj.append('\t'.join(m + ['elofordulas', '', '', '']))
        adat += 1
    # sor-összevetés
    for regi, ujs in zip(sorok[2:], uj[2:]):
        if regi and not regi.startswith('#'):
            if ujs != regi + '\telofordulas\t\t\t':
                print('HIBA: sor-eltérés: %r' % regi[:100])
                return 1
        elif regi != ujs:
            print('HIBA: komment/üres sor eltér')
            return 1
    kulcsok = {}
    for ujs in uj[2:]:
        if not ujs or ujs.startswith('#'):
            continue
        m = ujs.split('\t')
        k = (m[0], m[1], m[9], m[10])
        kulcsok[k] = kulcsok.get(k, 0) + 1
    dupla = [k for k, n in kulcsok.items() if n > 1]
    print('adatsor: %d; mind `elofordulas`; régi 9 mező bájtra azonos: igen; kulcsismétlés (id+igehely+jelolt_tipus+cel_id): %d'
          % (adat, len(dupla)))
    for k in dupla[:10]:
        print('  ismétlődő kulcs: %s' % ' · '.join(k))
    if a.ir:
        with open(TSV, 'wb') as f:
            f.write(('\n'.join(uj) + ('\n' if veg_ures else '')).encode('utf-8'))
        print('írva: adat/jeloltek.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
