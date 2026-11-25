"""F239 U2 — a szerkesztő 2026-11-23-i döntéseinek két adatváltozása (egyszeri szkript).

DT-F239c: a kizárási szabály szövege (`adat/motivumok.tsv`, TEREMT-001 `negativ_kriterium`): az ÚSZ-ben a görög
          ἄβυσσος szó, a Septuaginta tehóm-fordításának szava (a tagság nem változik).
DT-F239d: a `Jel 20:1-3` tartomány-sor kettéválik: Jel 20:1 és Jel 20:3 (a 20:2-ben a szó nem áll), az
          `adat/elofordulasok.tsv`-ben és az `adat/jeloltek.tsv` beépített sorában is, a régi sor helyén.

python naplok/F239_U2_szerkesztoi_dontes.py [--ir]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

REGI_KRIT = '(ÚSZ-ben az LXX-közvetített ἄβυσσος (abüsszosz) megfelelőjét)'
UJ_KRIT = '(az Újszövetségben a görög ἄβυσσος (abüsszosz) szót, a Septuaginta tehóm-fordításának szavát)'
SCAN = ('scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0012 | n=9 | ts=2026-11-23T11:57Z')
DONTES = 'a Jel 20:1-3 sor kettéválasztása: szerkesztői döntés (a felhasználó, 2026-11-23)'

# igehely → (kapcsolodas / indoklás, karoli_szo)
UJ_VERSEK = [
    ('Jel 20:1', 'ἄβυσσος (abüsszosz) — az angyal leszáll a mennyből, nála a mélység kulcsa és a lánc',
     'a mélységnek kulcsa'),
    ('Jel 20:3', 'ἄβυσσος (abüsszosz) — a sárkányt a mélységbe veti, bezárja és lepecsételi ezer évre',
     'a mélységbe'),
]


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok))
    if olvas(ut) != sorok:
        sys.exit('HIBA: visszaolvasás eltér: %s' % ut)


def fej(sorok):
    i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    return i, {n: j for j, n in enumerate(sorok[i].split('\t'))}


def egy(sorok, elotag):
    t = [i for i, s in enumerate(sorok) if s.startswith(elotag)]
    if len(t) != 1:
        sys.exit('HIBA: %d sor kezdődik így (1 kell): %r' % (len(t), elotag))
    return t[0]


def main():
    irj = '--ir' in sys.argv
    kesz = []

    ut = 'adat/motivumok.tsv'
    s = olvas(ut)
    i = egy(s, 'TEREMT-001\t')
    if s[i].count(REGI_KRIT) != 1:
        sys.exit('HIBA: a régi kritérium-szöveg nem pontosan egyszer áll')
    u = list(s)
    u[i] = s[i].replace(REGI_KRIT, UJ_KRIT)
    kesz.append((ut, s, u, {i}))

    ut = 'adat/elofordulasok.tsv'
    s = olvas(ut)
    _, k = fej(s)
    i = egy(s, 'TEREMT-001\tJel 20:1-3\t')
    regi = s[i].split('\t')
    uj = []
    for hely, leiras, ksz in UJ_VERSEK:
        m = list(regi)
        m[k['igehely']], m[k['kapcsolodas']], m[k['karoli_szo']] = hely, leiras, ksz
        m[k['proveniencia']] = SCAN   # a döntés nyoma a jelölt-sorban (ellenoriz.py 3.: csak kulcs=érték)
        uj.append('\t'.join(m))
    u = s[:i] + uj + s[i + 1:]
    kesz.append((ut, s, u, None))

    ut = 'adat/jeloltek.tsv'
    s = olvas(ut)
    _, k = fej(s)
    i = egy(s, 'TEREMT-001\tJel 20:1-3\t')
    regi = s[i].split('\t')
    uj = []
    for hely, leiras, ksz in UJ_VERSEK:
        m = list(regi)
        m[k['igehely']], m[k['indoklas']], m[k['karoli_szo']] = hely, leiras, ksz
        m[k['forras_kereses']] = 'F239 U2, %s; a szó gépi keresése: %s' % (DONTES, SCAN)
        m[k['datum']] = '2026.11.23'
        m[k['dontes_ref']] = 'DT-F239d · naplok/F239_hatar.md 6. pont (K4)'
        uj.append('\t'.join(m))
    u = s[:i] + uj + s[i + 1:]
    kesz.append((ut, s, u, None))

    for ut, s, u, _ in kesz:
        print('%s: %d → %d sor' % (ut, len(s), len(u)))
    if irj:
        for ut, _, u, _ in kesz:
            ir(ut, u)
        print('írva')


if __name__ == '__main__':
    main()
