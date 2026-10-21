"""F127 B4: a DT-F127e döntésének végrehajtása (felhasználó, 2026-10-20, chat).

1. `adat/jeloltek.tsv`, a motívumközi sorok:
   - (b) ApCsel 2:21 → ALVIL-001 és (d) 1Móz 12:8 → HAMART-001: `beépítve`;
   - (a), (c): `nyitva` marad, a döntés indoklásával;
   - (e) Róm 10:12-14 → TEREMT-001: három külön jelölt (Róm 10:12, 10:13,
     10:14; F1), mind `nyitva`.
   Az indoklás elején a DT-F127e szövege szó szerint, utána a B2 mért szövege.
2. `adat/motivum_kapcsolatok.tsv`: a (b) 2 sora és a (d) 1 sora (F2), a
   `dontes_ref`-fel (ellenoriz.dontes_ref_szoveg) és a mérés proveniencia-sorával
   (naplok/F127_B2_szomszedsag.tsv).

Olvasás split('\\t'), írás '\\t'.join(). Írás előtt: a nem motívumközi sorok
bájtra változatlanok; eltérésnél nincs írás.

    python naplok/F127_B4_dontes_ir.py          # szárazfutás
    python naplok/F127_B4_dontes_ir.py --ir
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JEL = os.path.join(ROOT, 'adat', 'jeloltek.tsv')
MK = os.path.join(ROOT, 'adat', 'motivum_kapcsolatok.tsv')

FORRAS = 'DT-F127e (felhasználó, 2026-10-20, chat): '
# a DONTESEK.md DT-F127e sorából, szó szerint
DONTES = {
    'a': ('nyitva', 'nyitva: az alponthoz kötött jelölt a DT-F127b (C) szerint, amíg az ALVIL-001 alpontjának '
                    'nincs adatbeli azonosítója (a #123 ALVIL-001-ciklusa vezeti be).'),
    'b': ('beépítve', 'beépítve — bizonyosság `közepes`, PaRDeS-szint Remez; mért: azonos fejezet, 6, ill. 10 vers '
                      'távolság, mindkét oldal előfordulás a saját motívumában; a célversek az ALVIL-001 '
                      'tanulmányának 1. táblájában a motívum gerincén állnak (Zsolt 16:10 → ApCsel 2:27, 31); '
                      'funkció: a hívás ígéretének (2:21) alapja, hogy a Messiás nem marad a Seólban.'),
    'c': ('nyitva', 'nyitva: mért: azonos fejezet, 12–23 vers távolság; a HAMART-001 tanulmánya a 4:26-ot nem '
                    'tárgyalja, a kapcsolatot csak az ISTENTISZT-001 oldala olvassa — beépítve egyoldalú értelmezés '
                    'töltene ki hiányt (CLAUDE.md 3. szabály).'),
    'd': ('beépítve', 'beépítve — bizonyosság `közepes`, PaRDeS-szint Remez; mért: azonos fejezet, 5 vers távolság; '
                      'a HAMART-001 tanulmánya a 12:3-at az átok-lánc megfordításaként tárgyalja; funkció: a '
                      'megfordított lánc után az első oltár és hívás.'),
    'e': ('nyitva', 'nyitva: mért: azonos fejezet, 5–7 vers távolság; a TEREMT-001-ben a Róm 10:7 csak a 2/c. tábla '
                    'értelmezés nélküli listaeleme, és a Károli zárójeles magyarázata a mélységet a halállal köti — '
                    'előbb az kell, hogy a vers a TEREMT-001-hez tartozik-e. F1: három jelölt (Róm 10:12, 10:13, '
                    '10:14 külön sor, mert az ISTENTISZT-001-ben három külön előfordulás-sor; mindhárom nyitva).'),
}
SAJAT = {'Zsolt 116:4': 'a', 'ApCsel 2:21': 'b', '1Móz 4:26': 'c', '1Móz 12:8': 'd', 'Róm 10:12-14': 'e'}
E_TAVOLSAG = {'Róm 10:12': 5, 'Róm 10:13': 6, 'Róm 10:14': 7}
FUNKCIO = {
    'b': 'a hívás ígéretének (2:21) alapja, hogy a Messiás nem marad a Seólban',
    'd': 'a megfordított lánc után az első oltár és hívás',
}
# F2: kapcsolat-sor csak a funkciót hordozó célversre
KAPCSOLAT_CELOK = {'b': ['ApCsel 2:27', 'ApCsel 2:31'], 'd': ['1Móz 12:3']}
MERT_INDOKLAS = {
    ('b', 'ApCsel 2:27'): 'Mért: azonos fejezet (ApCsel 2), 6 vers távolság; mindkét vers előfordulás a saját motívumában.',
    ('b', 'ApCsel 2:31'): 'Mért: azonos fejezet (ApCsel 2), 10 vers távolság; mindkét vers előfordulás a saját motívumában.',
    ('d', '1Móz 12:3'): 'Mért: azonos fejezet (1Móz 12), 5 vers távolság; mindkét vers előfordulás a saját motívumában.',
}


def beolvas(path):
    with open(path, 'rb') as f:
        szoveg = f.read().decode('utf-8')
    if '\r' in szoveg:
        raise SystemExit('HIBA: CR a táblában: %s' % path)
    sorok = szoveg.split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    return sorok


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ir', action='store_true')
    a = p.parse_args()
    sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
    import ellenoriz as E

    # a mérés proveniencia-sorai
    prov = {}
    for s in beolvas(os.path.join(ROOT, 'naplok', 'F127_B2_szomszedsag.tsv')):
        if s.startswith('#') or s.startswith('jelolt\t'):
            continue
        m = s.split('\t')
        prov[(m[2], m[5])] = m[9]

    sorok = beolvas(JEL)
    fej = sorok[1].split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    uj_sorok = sorok[:2]
    valtozott = 0
    beepitett = {}
    for s in sorok[2:]:
        m = s.split('\t')
        if len(m) != len(fej) or m[ix['jelolt_tipus']] != 'motivumkozi':
            uj_sorok.append(s)
            continue
        k = SAJAT[m[ix['igehely']]]
        dontes, szoveg = DONTES[k]
        mert = m[ix['indoklas']]
        if k == 'e':
            for v in ('Róm 10:12', 'Róm 10:13', 'Róm 10:14'):
                n = list(m)
                n[ix['igehely']] = v
                n[ix['dontes']] = dontes
                n[ix['forras_kereses']] = ('motívumközi (F127 B2): naplok/F127_B2_meres.py — '
                                           + prov[(v, 'Róm 10:7')])
                n[ix['indoklas']] = (FORRAS + szoveg + ' Mért (B2): azonos fejezet (Róm 10), %d vers távolság a '
                                     'Róm 10:7-től; mindkét vers előfordulás a saját motívumában. A közös fejezet vagy '
                                     'szókészlet önmagában nem bizonyít szándékos utalást.' % E_TAVOLSAG[v])
                uj_sorok.append('\t'.join(n))
            valtozott += 1
            continue
        m[ix['dontes']] = dontes
        m[ix['indoklas']] = FORRAS + szoveg + ' Mért (B2): ' + mert
        uj_sorok.append('\t'.join(m))
        valtozott += 1
        if dontes == 'beépítve':
            beepitett[k] = dict(zip(fej, m))

    # ellenőrzés: a nem motívumközi sorok bájtra azonosak, sorrendben
    regi_nem = [s for s in sorok if s.split('\t')[ix['jelolt_tipus']:ix['jelolt_tipus'] + 1] != ['motivumkozi']]
    uj_nem = [s for s in uj_sorok if s.split('\t')[ix['jelolt_tipus']:ix['jelolt_tipus'] + 1] != ['motivumkozi']]
    if regi_nem != uj_nem:
        print('HIBA: a nem motívumközi sorok eltérnek -- nem írok')
        return 1
    print('jeloltek.tsv: %d motívumközi sor módosítva, az (e) 3 sorra bontva; összes sor %d → %d'
          % (valtozott, len(sorok) - 2, len(uj_sorok) - 2))

    # kapcsolat-sorok
    mk = beolvas(MK)
    mk_fej = mk[1].split('\t')
    if mk_fej != E.MOTIVUM_KAPCSOLAT_FEJLEC or len(mk) != 2:
        print('HIBA: a motivum_kapcsolatok.tsv nem az üres, séma szerinti tábla')
        return 1
    uj_mk = list(mk)
    for k in ('b', 'd'):
        j = beepitett[k]
        for cel in KAPCSOLAT_CELOK[k]:
            a_ = (j['cel_id'], cel)
            b_ = (j['id'], j['igehely'])
            (id_a, ig_a), (id_b, ig_b) = sorted([a_, b_])
            r = {'id_a': id_a, 'igehely_a': ig_a, 'alpont_a': '', 'id_b': id_b, 'igehely_b': ig_b, 'alpont_b': '',
                 'tipus': 'szomszédos', 'funkcio': FUNKCIO[k], 'bizonyossag': 'közepes', 'pardes_szint': 'Remez',
                 'indoklas': MERT_INDOKLAS[(k, cel)] + ' A közös fejezet önmagában nem bizonyít szándékos '
                                                      'utalást. Döntés: DT-F127e (felhasználó, 2026-10-20).',
                 'dontes_ref': E.dontes_ref_szoveg(j),
                 'proveniencia': prov[(j['igehely'], cel)]}
            uj_mk.append('\t'.join(r[f] for f in mk_fej))
            print('kapcsolat: %s %s ↔ %s %s' % (id_a, ig_a, id_b, ig_b))
    if not a.ir:
        print('szárazfutás')
        return 0
    with open(JEL, 'wb') as f:
        f.write(('\n'.join(uj_sorok) + '\n').encode('utf-8'))
    with open(MK, 'wb') as f:
        f.write(('\n'.join(uj_mk) + '\n').encode('utf-8'))
    print('írva: adat/jeloltek.tsv, adat/motivum_kapcsolatok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
