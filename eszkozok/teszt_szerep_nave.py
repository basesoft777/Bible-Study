"""Az `eszkozok/szerep_nave.py` tesztjei: a 12. szerep (Tematikus index, Nave) jelöltképzése és választása.

Futtatás: python -m unittest -q eszkozok.teszt_szerep_nave
Szintetikus adaton (befecskendezett Nave-sorok, döntések) és két motívum valódi adatán (ISTENTISZT-001, KIRALY-001).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import szerep_nave as SN  # noqa: E402

SORAI = [{'id': 'T-1', 'igehely': h} for h in ('1Móz 1:1', '1Móz 1:2', '1Móz 1:3')]
# T1: 3 motívumvers / 3 témavers; T2: 2 / 300 (0,7%); T3: 1 vers; T4: 2 / 4, tartománnyal; T5: 2 / 10
NAVE = ([('T1', 'EGY', 'a', ['1Móz 1:1']), ('T1', 'EGY', 'b', ['1Móz 1:2', '1Móz 1:3'])]
        + [('T2', 'KETTO', '', ['1Móz 1:1', '1Móz 1:2'] + ['2Móz 1:%d' % i for i in range(1, 299)])]
        + [('T3', 'HAROM', '', ['1Móz 1:1'])]
        + [('T4', 'NEGY', '', SN.versek('1Móz 1:2-3') + ['2Móz 2:1', '2Móz 2:2'])]
        + [('T5', 'OT', '', ['1Móz 1:1', '1Móz 1:3'] + ['2Móz 3:%d' % i for i in range(1, 9)])])


def olvas_motivum(mid):
    with open(os.path.join(SN.GYOKER, 'adat', 'elofordulasok.tsv'), encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:] if x.split('\t')[0] == mid]


class Szintetikus(unittest.TestCase):
    def test_tartomany(self):
        self.assertEqual(SN.versek('1Móz 1:2-4'), ['1Móz 1:2', '1Móz 1:3', '1Móz 1:4'])
        self.assertEqual(SN.versek('1Móz 1:2'), ['1Móz 1:2'])

    def test_jeloltkepzes(self):
        j = SN.jeloltek(SORAI, tiltott=set(), nave=NAVE)
        self.assertEqual([t['tema_id'] for t in j], ['T1', 'T4', 'T5'])    # T2: 0,7% < 1%; T3: 1 vers
        self.assertEqual(j[0]['cimkek'], {'a': ['1Móz 1:1'], 'b': ['1Móz 1:2', '1Móz 1:3']})
        self.assertEqual([t['tema_id'] for t in SN.jeloltek(SORAI, tiltott={'T4'}, nave=NAVE)], ['T1', 'T5'])
        self.assertEqual([t['tema_id'] for t in SN.jeloltek(SORAI, min_vers=1, min_arany=0, tiltott=set(), nave=NAVE)],
                         ['T1', 'T4', 'T5', 'T2', 'T3'])                  # azonos versszámnál az arány dönt

    def test_valasztas(self):
        d = {'T1': ('kivalasztott', ''), 'T5': ('kivalasztott', ''), 'T4': ('kizart', 'x')}
        self.assertEqual([t['tema_id'] for t in SN.nave_temak(SORAI, d, nave=NAVE)], ['T1', 'T5'])
        d = {'T4': ('kizart', 'x')}                                        # választás nélkül: minden jelölt, a kizárt nélkül
        self.assertEqual([t['tema_id'] for t in SN.nave_temak(SORAI, d, nave=NAVE)], ['T1', 'T5'])
        d = {'T1': ('tiltott', 'x')}
        self.assertEqual([t['tema_id'] for t in SN.nave_temak(SORAI, d, nave=NAVE)], ['T4', 'T5'])

    def test_magyar_nev_hash(self):
        nevek = {('T1', ''): ('egy', SN.sha1('EGY')), ('T5', ''): ('öt', SN.sha1('MÁS'))}
        self.assertEqual(SN._hu(nevek, 'T1', '', 'EGY'), 'egy (*EGY*)')
        self.assertIn(SN.FORDITASRA_VAR, SN._hu(nevek, 'T5', '', 'OT'))   # elavult hash: fordításra vár


class ValodiAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ist = olvas_motivum('ISTENTISZT-001')
        cls.kir = olvas_motivum('KIRALY-001')

    def test_istentiszt_dontesek(self):
        d = SN.tema_dontesek('ISTENTISZT-001')
        self.assertEqual(sorted(t for t, (x, _i) in d.items() if x == 'tiltott'),
                         ['NAVE-3933', 'NAVE-3934', 'NAVE-4881', 'NAVE-5174'])
        self.assertEqual(sum(1 for x, _i in d.values() if x == 'kivalasztott'), 8)

    def test_istentiszt_halmaz(self):
        self.assertEqual(len(SN.jeloltek(self.ist)), 18)
        self.assertEqual(sorted(t['tema'] for t in SN.nave_temak(self.ist)),
                         sorted(['PRAYERLESSNESS', 'IDOL', 'GLORY', 'REVIVALS', 'TESTIMONY', 'OBLIGATION', 'SEEKERS',
                                 'PENITENT']))

    def test_kjv_karoli_megfeleltetes(self):
        # a Nave KJV Ézs 64:7-e a Károli Ézs 64:6 (nave_bontas.py, mint az olvasó nave_vers-e): a PRAYERLESSNESS 3 motívumverse
        t = next(x for x in SN.jeloltek(self.ist) if x['tema_id'] == 'NAVE-3936')
        self.assertEqual(t['motivumversek'], ['Zsolt 79:6', 'Ézs 64:6', 'Jer 10:25'])
        # a fejezet-szintű hely nem bomlik: az OBLIGATION témaverse nem számolja az 5Móz 6–11 fejezeteit egységként
        o = next(x for x in SN.jeloltek(self.ist) if x['tema_id'] == 'NAVE-3621')
        self.assertTrue(all(':' in v for v in SN.nave_sorai()[0][3]))
        self.assertEqual(len(o['motivumversek']), 2)

    def test_minden_dontes_jelolt(self):
        # minden kivalasztott/kizart sor a mai jelöltek között van (különben a döntés elavult)
        jel = {t['tema_id'] for t in SN.jeloltek(self.ist)}
        for t, (x, _i) in SN.tema_dontesek('ISTENTISZT-001').items():
            if x != 'tiltott':
                self.assertIn(t, jel, t)

    def test_masodik_motivum(self):
        # döntés nélkül minden jelölt áll; a szabály paraméterei érvényesek
        self.assertEqual(SN.tema_dontesek('KIRALY-001'), {})
        temak = SN.nave_temak(self.kir)
        self.assertEqual([t['tema_id'] for t in temak], [t['tema_id'] for t in SN.jeloltek(self.kir)])
        for t in temak:
            self.assertGreaterEqual(len(t['motivumversek']), SN.MIN_VERS)
            self.assertGreaterEqual(t['arany'], SN.MIN_ARANY)

    def test_blokk_12(self):
        b = SN.blokk_12(self.ist, '2026-10-29')
        self.assertIn('a 18 jelöltből a motívumhoz kiválasztott 8 téma', b[0])
        self.assertEqual(b[1].count('\n- '), 7)
        self.assertRegex(b[-1], r'scope=.* \| forras=.* \| n=8 \| ts=2026-10-29')


if __name__ == '__main__':
    unittest.main()
