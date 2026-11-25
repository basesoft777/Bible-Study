"""F239 U2 — a határ-ellenőr 3. kérdésére: a Jób 41:31 összesítő sor indoklása kimondja a többi kilenc vers
Septuaginta-állapotát is (egyszeri szkript; a forrás: naplok/F239_U1_TEREMT-001_lxx_g0012.tsv, ahol a mecólá-blokk
versei közül csak a Jób 41:31 áll).

python naplok/F239_U2_jelolt_javit.py [--ir]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/jeloltek.tsv'
REGI = 'A Jób 41:31-ben a görög fordítás erre a szóra ἄβυσσος-t hoz, de a héberben nem a tehóm áll.'
UJ = ('A Jób 41:31-ben a görög fordítás erre a szóra ἄβυσσος-t hoz, de a héberben nem a tehóm áll; a többi kilenc '
      'versben (köztük a Jón 2:4, a Mik 7:19 és a Neh 9:11) a görög fordítás sem ἄβυσσος-t hoz.')


def main():
    with open(UT, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    talalat = [i for i, s in enumerate(sorok) if s.startswith('TEREMT-001\tJób 41:31\t') and REGI in s]
    if len(talalat) != 1:
        sys.exit('HIBA: %d találat (1 kell)' % len(talalat))
    i = talalat[0]
    uj = list(sorok)
    uj[i] = sorok[i].replace(REGI, UJ)
    print('sor %d: módosul' % (i + 1))
    if '--ir' in sys.argv:
        with open(UT, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(uj))
        with open(UT, encoding='utf-8', newline='') as f:
            vissza = f.read().split('\n')
        if vissza != uj or any(vissza[j] != sorok[j] for j in range(len(sorok)) if j != i):
            sys.exit('HIBA: visszaolvasás eltér')
        print('írva')


if __name__ == '__main__':
    main()
