#!/usr/bin/env python3
"""teszt_bdb_tagolas.py — a BDB tagolása a szakasztáblából, egy forrásból (F182, 2. fázis, F33; N138).

Futtatás: python -m unittest eszkozok.teszt_bdb_tagolas  (a repó gyökeréből; Windowsról is, adatbázis nélkül)

- a `bdb_tagolas` fája az olvasó megjelenítőjének alakjában (szintetikus sorokon);
- valódi adaton: a HAMART-001 BDB-szavainak minden 2.29-pontja szerepel a megjelenített fában — az olvasóéban
  (`szeletelo_alak`) és a 4.2-es kártyáéban (`lexikon_general.bdb_gerinc_szocikkek`) is;
- repó-szinten regresszióőr: a fán kívüli 2.29-pont (a szakasztábla sorbelső feje és a táblában nem álló útvonal,
  N-F182b) nem nőhet a mért szám fölé;
- a kártya fán kívüli pontja nem kap kitalált nevet (`lexikon_general.fan_kivuli_pontok`).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import bdb_tagolas as BT  # noqa: E402

# A mért állapot (2026-11-11, a #185 utáni 2.29 és 2.30), repó-szinten, az olvasó fáján: (1) a fán kívüli 2.29-pont (az
# útvonal a fában nem áll: a szakasztábla sorbelső feje vagy a táblában nem álló útvonal; N-F182b); (2) a két szócikk azonos
# 2.29-címkéje miatt nem egyértelmű pont (a kártya a hely szerint dönt, az olvasó nem; N-F182c). A számok csak csökkenhetnek.
FAN_KIVUL_MERT = 440
KETERTELMU_MERT = 5368


def tsv(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s]


def _sor(sorszam, utvonal, jel='', szoveg='', szakasz='', resz='', alszocikk='0', jelolo='point', bdb_id='B1', gyak=''):
    return {'strong': 'H0000', 'bdb_id': bdb_id, 'sorszam': str(sorszam), 'alszocikk': alszocikk, 'szakasz': szakasz,
            'resz': resz, 'utvonal': utvonal, 'jelolo': jelolo, 'jel': jel, 'gyakorisag': gyak, 'szoveg': szoveg}


def _ref(t):
    return t.count(':')


class SzintetikusFa(unittest.TestCase):
    def setUp(self):
        self.sorok = [
            _sor(1, 'cim', szoveg='H0000. x'), _sor(2, 'fej', szoveg='אָב noun father', gyak='12', jelolo='fej'),
            _sor(3, 'Qal/-/-', 'Qal', 'say Gen 1:1', gyak='5'), _sor(4, 'Qal/1/-', '1', 'speak Gen 2:2'),
            _sor(5, 'Qal/1/a', 'a.', 'loudly Gen 3:3'), _sor(6, 'Qal/1/a', '', 'more Gen 3:4', jelolo='bekezdes'),
            _sor(7, 'Niph`al/-/-'.replace('`', "'"), "Niph`al", 'be said Ex 1:1'),
            _sor(8, 'fej', szoveg='II. מַר noun', szakasz='II', bdb_id='B2', jelolo='fej'),
            _sor(9, '-/1/-', '1', 'bitter Ps 1:1', szakasz='II', bdb_id='B2'),
        ]
        self.hu = {'4': {'szoveg_hu': '1 beszélni 1Móz 2:2', 'kategoria': 'horgonnyal'}}

    def test_torzsek_jelentesek_alpontok(self):
        a = BT.szeletelo_alak(self.sorok, self.hu, 'hu', lambda t: {'alap': t}, _ref)
        self.assertEqual([t['nev'] for t in a['torzsek']], ['Qal', "Niph'al"])
        q = a['torzsek'][0]
        self.assertEqual(q['db'], '5')
        self.assertEqual([j['jel'] for j in q['jelentesek']], ['', '1'])
        self.assertEqual(q['jelentesek'][1]['szoveg'], 'beszélni 1Móz 2:2')   # a magyar, a saját jele nélkül
        self.assertEqual(q['jelentesek'][1]['al'][0]['szoveg'], 'loudly Gen 3:3 more Gen 3:4')   # összevont bekezdés
        self.assertEqual(a['fej']['ossz'], '12')
        self.assertEqual(len(a['szakaszok']), 1)
        self.assertEqual(BT.szakasz_cimke(a['szakaszok'][0]), 'II')

    def test_pontok_a_2_29_kulcsaval(self):
        a = BT.szeletelo_alak(self.sorok, {}, 'en', lambda t: {}, _ref)
        p = BT.megjelenitett_pontok(a)
        for kulcs in [('', 'Qal/-'), ('', 'Qal/1'), ('', 'Qal/1/a'), ('', "Niph'al/-"), ('II', '-/1')]:
            self.assertIn(kulcs, p)

    def test_alcimszo_es_resz_cimkeje(self):
        sorok = [_sor(1, 'fej', szoveg='x', jelolo='fej'), _sor(2, '-/1/-', '1', 'a'),
                 _sor(3, 'fej', szoveg='מַר noun', alszocikk='1', jelolo='alcimszo'), _sor(4, '-/1/-', '1', 'b', alszocikk='1'),
                 _sor(5, '-/1/-', '1', 'c', szakasz='III', resz='I', bdb_id='B3')]
        sz = BT.szakasz_szerint(sorok)
        self.assertEqual(sz[2][0], 'h:' + BT.kons('מַר'))
        a = BT.szeletelo_alak(sorok, {}, 'en', lambda t: {}, _ref)
        cimkek = [BT.szakasz_cimke(x) for x in a['szakaszok']]
        self.assertEqual(cimkek, ['h:' + BT.kons('מַר'), 'III' + BT.RESZ_SEP + 'I'])

    def test_ketszer_allo_kulcs_nem_megjelenitett(self):
        # H7451-minta: két szócikk ugyanazzal a 2.29-címkével ('') — a kulcs nem egyértelmű
        sorok = [_sor(1, 'fej', szoveg='x', jelolo='fej'), _sor(2, '-/1/-', '1', 'a'),
                 _sor(3, 'fej', szoveg='y', jelolo='fej', bdb_id='B2'), _sor(4, '-/1/-', '1', 'b', bdb_id='B2')]
        a = BT.szeletelo_alak(sorok, {}, 'en', lambda t: {}, _ref)
        self.assertNotIn(('', '-/1'), BT.megjelenitett_pontok(a))

    def test_ut3(self):
        self.assertEqual(BT.ut3('-/1/-'), '-/1')
        self.assertEqual(BT.ut3('Qal/-/-'), 'Qal/-')
        self.assertEqual(BT.ut3('Qal.A/1/a/(1)'), 'Qal/1/a')
        self.assertEqual(BT.ut3('cim'), 'fej')


class ValodiAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sz, cls.hu, cls.vj = {}, {}, {}
        for r in tsv('adat/bdb_szakaszok.tsv'):
            cls.sz.setdefault(r['strong'], []).append(r)
        for r in tsv('adat/bdb_vers_jelentes.tsv'):
            cls.vj.setdefault(r['strong'], []).append(r)
        elo = tsv('adat/elofordulasok.tsv')
        cls.hamart = sorted({t for r in elo if r['id'] == 'HAMART-001' for t in (r.get('strong') or '').split('+')
                             if t.startswith('H')})

    def kivul(self, strong, egyertelmu=False):
        sorok = self.sz.get(strong)
        if not sorok:
            return []
        p = BT.megjelenitett_pontok(BT.szeletelo_alak(sorok, {}, 'en', lambda t: {}, _ref), egyertelmu)
        return [r for r in self.vj.get(strong, []) if r['utvonal'] not in ('fej', 'tagolatlan', 'cim')
                and BT.vers_kulcs(r) not in p]

    def test_hamart_minden_pont_a_faban(self):
        hiany = [(s, r['karoli_vers'], r['utvonal']) for s in self.hamart for r in self.kivul(s)]
        self.assertEqual(hiany, [])
        ket = sum(len(self.kivul(s, True)) for s in self.hamart)
        print('\n[F33] HAMART-001: a fán kívüli pont 0; azonos címke miatt nem egyértelmű az olvasóban: %d (N-F182c)' % ket)

    def test_repo_szintu_regresszioor(self):
        n = sum(len(self.kivul(s)) for s in self.sz)
        k = sum(len(self.kivul(s, True)) for s in self.sz) - n
        print('\n[F33] repó-szinten: a fán kívüli 2.29-pont %d (mért: %s); nem egyértelmű %d (mért: %s)'
              % (n, FAN_KIVUL_MERT, k, KETERTELMU_MERT))
        if FAN_KIVUL_MERT is not None:
            self.assertLessEqual(n, FAN_KIVUL_MERT)
            self.assertLessEqual(k, KETERTELMU_MERT)

    def test_kartya_minden_hamart_pont_a_faban(self):
        import lexikon_general as LG
        adat = LG.gerinc_adat()
        for s in self.hamart:
            szocikkek, _ = LG.bdb_gerinc_szocikkek(adat, s)
            fa = {LG.gerinc_utvonal_vag(k[1]) for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
            tagolt = any(sz['szakaszok'] for sz in szocikkek)
            for r in self.vj.get(s, []):
                if r['utvonal'] in ('fej', 'tagolatlan', 'cim') or not tagolt:
                    continue
                self.assertIn(LG.gerinc_utvonal_vag(r['utvonal']), fa, (s, r['karoli_vers'], r['utvonal']))

    def test_kartya_es_olvaso_ugyanaz_a_fa(self):
        # egy forrás: a kártya csomópontjai és az olvasóé ugyanazok az útvonalak (szócikkenként összevonva)
        import lexikon_general as LG
        adat = LG.gerinc_adat()
        for s in self.hamart:
            szocikkek, _ = LG.bdb_gerinc_szocikkek(adat, s)
            kartya = {BT.ut3(k[1]) for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
            a = BT.szeletelo_alak(self.sz.get(s, []), {}, 'en', lambda t: {}, _ref)
            olvaso = {p for _c, p in BT.megjelenitett_pontok(a)} if a else set()
            olvaso_db = set()
            if a:
                for x in [{'torzsek': a['torzsek']}] + a['szakaszok']:
                    for t in x['torzsek']:
                        for j in t['jelentesek']:
                            jp = '%s/%s' % (t['nev'] or '-', j['jel'] or '-')
                            olvaso_db.add(jp)
                            olvaso_db.update('%s/%s' % (jp, al['jel']) for al in j['al'])
            self.assertEqual(kartya - {'fej'}, olvaso_db, s)
            self.assertTrue(olvaso <= olvaso_db)


class KartyaFanKivul(unittest.TestCase):
    def test_fan_kivuli_pont_kiszurve(self):
        import lexikon_general as LG
        szocikkek = [{'bdb_id': 'B', 'fej': None, 'szakaszok': [(('B', '-/1/-'), '1', 'x', 'x', '')]}]
        vp = [('1Móz 1:1', ('B', '-/1/-')), ('1Móz 1:2', ('B', '-/1/b')), ('1Móz 1:3', ('B', 'fej'))]
        self.assertEqual(LG.fan_kivuli_pontok(vp, szocikkek), [('1Móz 1:2', ('B', '-/1/b'))])


if __name__ == '__main__':
    unittest.main()
