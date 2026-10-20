"""F127 B2: a pilot öt motívumközi jelöltje a `jeloltek.tsv`-be (dontes=nyitva).

A forras_kereses mezőbe a mérés (naplok/F127_B2_meres.py) proveniencia-sora
kerül, a naplok/F127_B2_szomszedsag.tsv-ből kiolvasva; az indoklás csak a mért
szomszédságot mondja ki (a közös fejezet nem bizonyít szándékos utalást).
Írás: general.jeloltek_hozzafuz (a meglévő sorok bájtra változatlanok).

    python naplok/F127_B2_jeloltek_ir.py          # szárazfutás
    python naplok/F127_B2_jeloltek_ir.py --ir
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import general as G  # noqa: E402

DATUM = '2026.10.20'
KOZOS = ('A közös fejezet vagy szókészlet önmagában nem bizonyít szándékos utalást; '
         'a jelölt csak a mért szomszédságot rögzíti (felmérés: naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md %s).')

# jelölt: (saját igehely, cél, cél-igehelyek, cél-alpont, indoklás)
JELOLTEK = {
    'a': ('Zsolt 116:4', 'ALVIL-001', ['Zsolt 116:3'], 'kiáltás a Seól szorításából',
          'Mért szomszédság: azonos fejezet (Zsolt 116), 1 vers távolság; a Zsolt 116:3 az ALVIL-001, a 116:4 '
          'az ISTENTISZT-001 előfordulása. Javasolt kapcsolat-típus: szomszédos. Célszint: az ALVIL-001 '
          '„kiáltás a Seól szorításából” ↳ alpontja (a #123 Seól-határ-döntése, DT-F123d); az alpontnak még '
          'nincs adatbeli azonosítója, ezért a jelölt a DT-F127b (C) szerint nyitva marad. ' + KOZOS % '3.'),
    'b': ('ApCsel 2:21', 'ALVIL-001', ['ApCsel 2:27', 'ApCsel 2:31'], '',
          'Mért szomszédság: azonos fejezet (ApCsel 2), 6, ill. 10 vers távolság; az ApCsel 2:27 és 2:31 az '
          'ALVIL-001, a 2:21 az ISTENTISZT-001 előfordulása. Javasolt kapcsolat-típus: szomszédos. Célszint: '
          'az ALVIL-001 egésze. Hogy a három vers ugyanabban a beszédben áll, az nem adat, hanem a szöveg '
          'olvasata (értelmezés). ' + KOZOS % '3.'),
    'c': ('1Móz 4:26', 'HAMART-001', ['1Móz 4:2-3', '1Móz 4:7', '1Móz 4:10-11', '1Móz 4:12', '1Móz 4:14'], '',
          'Mért szomszédság: azonos fejezet (1Móz 4); a HAMART-001 öt előfordulás-sora a fejezetben 12–23 '
          'vers távolságra áll a 4:26-tól, a fejezet utolsó verse a 4:26. Javasolt kapcsolat-típus: szomszédos. '
          'Célszint: a HAMART-001 egésze. ' + KOZOS % '4.'),
    'd': ('1Móz 12:8', 'HAMART-001', ['1Móz 12:3'], '',
          'Mért szomszédság: azonos fejezet (1Móz 12), 5 vers távolság; az 1Móz 12:3 a HAMART-001, a 12:8 az '
          'ISTENTISZT-001 előfordulása. Javasolt kapcsolat-típus: szomszédos. Célszint: a HAMART-001 egésze. '
          + KOZOS % '4.'),
    'e': ('Róm 10:12-14', 'TEREMT-001', ['Róm 10:7'], '',
          'Mért szomszédság: azonos fejezet (Róm 10), a Róm 10:12, 10:13 és 10:14 (mindhárom az ISTENTISZT-001 '
          'előfordulása) 5, 6, ill. 7 vers távolságra a Róm 10:7-től (a TEREMT-001 előfordulása). Javasolt '
          'kapcsolat-típus: szomszédos. Célszint: a TEREMT-001 egésze. A felmérés maga óvatosságot kér: a '
          'TEREMT-001 tanulmánya a Róm 10:7-et csak a 2/c. táblában, „Remez/Drash” szinttel sorolja fel, '
          'értelmezés nélkül. ' + KOZOS % '5.'),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ir', action='store_true')
    a = p.parse_args()
    # a mérés proveniencia-sorai jelöltenként
    prov = {}
    with open(os.path.join(ROOT, 'naplok', 'F127_B2_szomszedsag.tsv'), encoding='utf-8') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        if r['id_elofordulas'] != 'igen' or r['cel_elofordulas'] != 'igen':
            print('HIBA: nem előfordulás: %s' % s)
            return 1
        prov.setdefault(r['jelolt'], []).append(r['proveniencia'])
    uj = []
    for k, (ig, cel, celok, alpont, indoklas) in JELOLTEK.items():
        uj.append({
            'id': 'ISTENTISZT-001', 'igehely': ig,
            'forras_kereses': 'motívumközi (F127 B2): naplok/F127_B2_meres.py — ' + '; '.join(prov[k]),
            'dontes': 'nyitva', 'indoklas': indoklas,
            'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': '', 'datum': DATUM,
            'jelolt_tipus': 'motivumkozi', 'cel_id': cel, 'cel_igehely': '; '.join(celok), 'cel_alpont': alpont,
        })
    for r in uj:
        print('%s · %s → %s · %s%s' % (r['id'], r['igehely'], r['cel_id'], r['cel_igehely'],
                                         (' (alpont: %s)' % r['cel_alpont']) if r['cel_alpont'] else ''))
    if not a.ir:
        print('szárazfutás: %d jelölt' % len(uj))
        return 0
    kod, uzenet = G.jeloltek_hozzafuz(G.JELOLTEK_TSV, uj)
    print(uzenet)
    return kod


if __name__ == '__main__':
    sys.exit(main())
