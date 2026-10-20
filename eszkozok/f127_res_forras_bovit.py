"""F127 A3 (DT-F127a): az `adat/res_forras.tsv` bővítése motívumonként két
sorral (`alkalmazas`, `tanitoi`), az `ertelmezes` sor után.

- ISTENTISZT-001 (migrált): `forras=tanulmany`, a forrás, ill. a tanítói fájl;
- a többi motívum: `forras=adat`, rögzített átmeneti mondattal (a jelölőket a
  #123 ciklusai teszik a forrásba), a mondat a motívum tematikus tanulmányának
  5. pontjára mutat (az `ertelmezes` sor `tanulmany` mezője).

Olvasás split('\\t'), írás '\\t'.join() (CLAUDE.md, TSV-szabály). Írás előtt
a meglévő sorokat összeveti az eredetivel; eltérésnél nem ír.

    python eszkozok/f127_res_forras_bovit.py        # szárazfutás
    python eszkozok/f127_res_forras_bovit.py --ir
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'adat', 'res_forras.tsv')

FEJLEC_ALKALMAZAS = '### Alkalmazás és tanítványság *(kézi)*'
FEJLEC_TANITOI = '### Tanítói egyezés *(kézi)*'
MIGRALT = {
    'ISTENTISZT-001': ('motivumok/ISTENTISZT-001.md',
                       'motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md'),
}
MONDAT_ALK = ('Az alkalmazási rész a motívum migrációjával kerül a lapra (#123); addig a '
              '`%s` „5. Alkalmazás és tanítványság” szakaszában áll.')
MONDAT_TAN = ('A tanítói egyezés a motívum migrációjával kerül a lapra (#123); addig a '
              '`%s` „5. Alkalmazás és tanítványság” szakaszában áll.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ir', action='store_true')
    a = p.parse_args()
    with open(TSV, 'rb') as f:
        nyers = f.read()
    szoveg = nyers.decode('utf-8')
    if '\r' in szoveg:
        print('HIBA: CR a táblában')
        return 1
    sorok = szoveg.split('\n')
    veg_ures = sorok[-1] == ''
    if veg_ures:
        sorok = sorok[:-1]
    if any(s.split('\t')[1:2] in (['alkalmazas'], ['tanitoi']) for s in sorok):
        print('a tábla már tartalmazza az új réseket -- nincs teendő')
        return 0
    uj = []
    hozzaadott = 0
    for s in sorok:
        uj.append(s)
        m = s.split('\t')
        if len(m) == 5 and m[1] == 'ertelmezes':
            mid = m[0]
            if mid in MIGRALT:
                forras_ut, tanitoi_ut = MIGRALT[mid]
                for rel in (forras_ut, tanitoi_ut):
                    if not os.path.exists(os.path.join(ROOT, rel)):
                        print('HIBA: nincs ilyen fájl: %s' % rel)
                        return 1
                uj.append('\t'.join([mid, 'alkalmazas', FEJLEC_ALKALMAZAS, 'tanulmany', forras_ut]))
                uj.append('\t'.join([mid, 'tanitoi', FEJLEC_TANITOI, 'tanulmany', tanitoi_ut]))
            else:
                tan = m[4]
                with open(os.path.join(ROOT, tan), encoding='utf-8') as f:
                    if '\n## 5. Alkalmazás és tanítványság' not in f.read():
                        print('HIBA: %s: nincs „5. Alkalmazás és tanítványság” szakasz' % tan)
                        return 1
                uj.append('\t'.join([mid, 'alkalmazas', FEJLEC_ALKALMAZAS, 'adat', MONDAT_ALK % tan]))
                uj.append('\t'.join([mid, 'tanitoi', FEJLEC_TANITOI, 'adat', MONDAT_TAN % tan]))
            hozzaadott += 2
    # sor-összevetés: a régi sorok sorrendben, változatlanul megvannak
    regi_maradt = [s for s in uj if s.split('\t')[1:2] not in (['alkalmazas'], ['tanitoi'])]
    if regi_maradt != sorok:
        print('HIBA: a meglévő sorok eltérnek az eredetitől -- nem írok')
        return 1
    if any(len(s.split('\t')) != 5 for s in uj[1:] if not s.startswith('#')):
        print('HIBA: mezőszám')
        return 1
    print('új sor: %d; régi sor változatlan: %d' % (hozzaadott, len(sorok)))
    if a.ir:
        with open(TSV, 'wb') as f:
            f.write(('\n'.join(uj) + ('\n' if veg_ures else '')).encode('utf-8'))
        print('írva: adat/res_forras.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
