#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_zaras3.py -- F38 zaromenet 3. kor (DT-F38g, 2026.10.02).

A naplok/ELLENOR_F38_zaras_2.md hat elteresenek kezelese:

  (1) H3772: a csonka mondat javitasa (a „fordítják” allitmany vissza, az RV-szo angolul);
  (2) H5674: az 1Kir 22:24 a BDB H7307 9a pontjaba tartozik -> nagybetus Szellem;
  (4) H4397: az RV sajat szava („angel”) angolul, a BDB megjegyzese („too specific”) lefordul;
  (5) H4264: `1Móz 33:816t.` -> `1Móz 33:8, összesen 16-szor`;
  (6) H2403: a megjegyzes jelolese „kezi javitas” (nem „gepi szabalyok a #28 soron”).
A (3) Szellem-szabaly pontositasa utan a Szellem-tabla ujranezese: SZELLEM_KOVETELT a
naplo vegleges tablajanak ellenorzo listaja (nagybetus helyek szoalakonkent, szocikkenkent).

A javitasok a javitasi listara (BDB_FORDITAS_zaras_javitasok.tsv) is kerulnek. A
BDB_FORDITAS_zaras.py --ir-t ujrafuttatni tilos (felulirna a listat).

    python naplok/BDB_FORDITAS_zaras3.py          # csak jelentes
    python naplok/BDB_FORDITAS_zaras3.py --ir
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402

KIMENET = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_zaras_javitasok.tsv')
JELOLES_F38 = 'F38.278: DT-F38g — az ellenőri eltérések kézi javítása'
JELOLES_H2403 = 'F38.274: DT-F38f (5) — kézi javítás (RV/AV-glossza); F38.278: a jelölés pontosítva (DT-F38g 6)'
JELOLES_28_REGI = 'F38.274: DT-F38f (1) — gépi szabályok a #28 soron (N t., tapadt könyvjelzés, RV/AV, Izráel)'

# (strong, szabaly, regi, uj, iras): a regi reszlet a forditasban pontosan egyszer all
KEZI3 = [
    ('H3772', 'rv_av_kezi', 'helyet rendszerint az RV made for thee a covenant with them,',
     'helyet rendszerint így fordítják: RV made for thee a covenant with them,', 'igen (kézi, DT-F38g 1)'),
    ('H5674', 'szellem_nagybetu', 'abszolút használatban és מֵאֵת 1Kir 22:24',
     'a Szellemről abszolút használatban és מֵאֵת 1Kir 22:24', 'igen (kézi, DT-F38g 2)'),
    ('H4397', 'rv_av_kezi', '(az angyal RV too specific)', '(az RV angel szava túl szűk)',
     'igen (kézi, DT-F38g 4)'),
    ('H4264', 'elofordulas', '1Móz 33:816t.', '1Móz 33:8, összesen 16-szor', 'igen (kézi, DT-F38g 5)'),
]
# a megjegyzes-javitas csak jelolesre: strong -> (regi jeloles, uj jeloles)
MEGJ3 = {'H2403': (JELOLES_28_REGI, JELOLES_H2403)}

# A Szellem-tabla (naplo, „Zárómenet, 3. kör”) szerinti nagybetus helyek:
# strong -> (nagybetus `Szellem*` szoalak, egy kontextus-reszlet, amely egyszer all)
SZELLEM_KOVETELT = {
    'H1320': [('Szellem', 'nem Szellem Ézs 31:3')],
    'H3947': [('Szellem', 'Ez 3:14 a Szellem felemelt')],
    'H5307': [('Szelleme', 'a ׳י Szelleme 11:5')],
    'H5414': [('Szellememet', 'Szellememet adom rá Ézs 42:1')],
    'H5650': [('Szellemmel', 'isteni Szellemmel')],
    'H5674': [('Szellemről', 'a Szellemről abszolút használatban és מֵאֵת 1Kir 22:24')],
    'H7307': [('Szellem', 'Di Bu: isteni Szellem, vö. 32:8'),
              ('Szelleme', 'c. ezért Isten Szelleme: 1Móz 6:3'),
              ('Szellem', 'prófétai Szellem, 9b)'),
              ('Szelleme', '9 Isten Szelleme (94-szer'),
              ('Szellem', 'az eksztatikus állapotban a Szellem megragadott'),
              ('Szellem', 'b. a Szellem mint a prófétákat'),
              ('Szellemet', 'úgy fogják fel az isteni Szellemet,')],
    'H7760': [('Szellemet', 'átvitt értelemben Szellemet (עַל) 4Móz 11:17')],
}
SZO = re.compile(r'Szellem\w*')


def szellem_ellenorzes(sorok_hu):
    """sorok_hu: strong -> forditas_hu. Eredmeny: (hibak, osszes nagybetus hely)."""
    hibak, osszes = [], 0
    for sp, hu in sorok_hu.items():
        var = SZELLEM_KOVETELT.get(sp, [])
        talalt = SZO.findall(hu)
        osszes += len(talalt)
        if sorted(talalt) != sorted(s for s, _ in var):
            hibak.append('%s: nagybetűs alakok %s, várt %s' % (sp, sorted(talalt), sorted(s for s, _ in var)))
        for szo, ctx in var:
            if hu.count(ctx) != 1:
                hibak.append('%s: a kontextus %d-szer áll: %s' % (sp, hu.count(ctx), ctx))
    for sp in SZELLEM_KOVETELT:
        if sp not in sorok_hu:
            hibak.append('%s: nincs a táblán' % sp)
    return hibak, osszes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    with open(E.FORDITASOK_UT, encoding='utf-8', newline='') as fh:
        sorok = fh.read().split('\n')
    assert sorok[-1] == ''
    sorok = sorok[:-1]
    ix = {n: i for i, n in enumerate(E.FORDITASOK_FEJLEC)}
    sor_ix = {}
    for i, s in enumerate(sorok):
        m = s.split('\t')
        if len(m) == 12 and m[0] == 'BDB' and m[3] == 'teljes':
            sor_ix[m[1]] = i
    javitasok = []
    for sp, nev, regi, uj, iras in KEZI3:
        i = sor_ix[sp]
        m = sorok[i].split('\t')
        hu = m[ix['forditas_hu']]
        db = hu.count(regi)
        if db != 1:
            raise SystemExit('%s: a regi reszlet %d-szer all (1 kell): %s' % (sp, db, regi))
        m[ix['forditas_hu']] = hu.replace(regi, uj)
        if JELOLES_F38 not in m[ix['megjegyzes']]:
            m[ix['megjegyzes']] = '; '.join(x for x in (m[ix['megjegyzes']], JELOLES_F38) if x)
        sorok[i] = '\t'.join(m)
        javitasok.append((sp, nev, regi, uj, '1', iras))
        print('%s | %s => %s' % (sp, regi, uj))
    for sp, (regi, uj) in MEGJ3.items():
        i = sor_ix[sp]
        m = sorok[i].split('\t')
        if m[ix['megjegyzes']].count(regi) != 1:
            raise SystemExit('%s: a megjegyzes-jeloles nem egyszer all' % sp)
        m[ix['megjegyzes']] = m[ix['megjegyzes']].replace(regi, uj)
        sorok[i] = '\t'.join(m)
        print('%s megjegyzes: %s' % (sp, uj))
    # kapuk (a sor sajat kiveteleivel) -- a javitott sorokon gatolo SERTES nem maradhat
    for sp in ('H3772', 'H5674', 'H4397', 'H4264', 'H2403'):
        m = sorok[sor_ix[sp]].split('\t')
        _, forras = E.forras_szoveg(sp)
        er = K.kapuk_futtat('BDB', forras, m[ix['forditas_hu']], bizonytalan=kivetelek(m[ix['megjegyzes']]))
        if not K.atment(er):
            raise SystemExit('%s: nem megy at a gatolo kapukon: %s' % (sp, [x for x in er if x[1] == 'SERTES']))
    hu_map = {sp: sorok[i].split('\t')[ix['forditas_hu']] for sp, i in sor_ix.items()}
    hibak, osszes = szellem_ellenorzes(hu_map)
    print('Szellem-ellenorzes: %d nagybetus hely, hiba: %s' % (osszes, hibak if hibak else 'nincs'))
    if hibak:
        raise SystemExit('a Szellem-tabla nem egyezik a tablaval')
    if args.ir:
        with open(E.FORDITASOK_UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(sorok) + '\n')
        with open(KIMENET, encoding='utf-8', newline='') as fh:
            ts = fh.read().split('\n')
        assert ts[0] == 'szocikk\tszabaly\tregi\tuj\tdb\tiras' and ts[-1] == ''
        ts = ts[:-1] + ['\t'.join(j) for j in javitasok]
        with open(KIMENET, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(ts) + '\n')
        print('adat/forditasok.tsv es a javitasi lista irva (+%d sor)' % len(javitasok))


if __name__ == '__main__':
    main()
