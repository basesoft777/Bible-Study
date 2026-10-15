"""F99 M2: a BDB igehely-hivatkozásainak feloldása (bdb_szelet.hivatkozasok, csomopont_savok, jelentespont) és a vers → jelentés tábla
(adat/bdb_vers_jelentes.tsv, bdb_vers_jelentes.py). A szabályok: DT-F99a (felhasználó, 2026-10-15). Csak olvas.

Futtatás: python eszkozok/teszt_futtat.py --fajl teszt_bdb_vers_jelentes (vagy közvetlenül; DB nem kell).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import bdb_szelet as B  # noqa: E402
import bdb_vers_jelentes as V  # noqa: E402


def sor(sorok, **kw):
    i = {k: n for n, k in enumerate(V.FEJ)}
    return [s for s in sorok if all(s[i[k]] == v for k, v in kw.items())]


class Hivatkozasok(unittest.TestCase):
    def test_kiirt_orokolt_folytatas(self):
        h = B.hivatkozasok('H9999. x אב noun father; — 1. father Gen 18:18, 25; 22:18 (P) Exod 4:2.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod']) for x in h],
                         [('1Móz', 18, 18, 'kiirt'), ('1Móz', 18, 25, 'folytatas'), ('1Móz', 22, 18, 'orokolt'), ('2Móz', 4, 2, 'kiirt')])

    def test_sigla_tapadt_kiszurendo_nemi_tanu_bibliai(self):
        h = B.hivatkozasok('H9999. x אב noun masculine^Gen 1:27 man (see Wetzst in De^Job 34:36), Gen 2:7.')
        ok = {(x['konyv'], x['c'], x['v']): x['okkod'] for x in h}
        self.assertEqual(ok[('1Móz', 1, 27)], '')
        self.assertEqual(ok[('Jób', 34, 36)], 'sigla_tapadt')
        self.assertEqual(ok[('1Móz', 2, 7)], '')
        h = B.hivatkozasok('H0226. oth אוֺת noun masculine_79 ^Exod 4:8 (feminine).')
        self.assertEqual(h[0]['okkod'], '')

    def test_nem_bibliai_es_utana_orokolt(self):
        h = B.hivatkozasok('H9999. x אב noun so Late Hebrew Yoma 5:1; 6:2.')
        self.assertTrue(all(x['okkod'] == 'nem_bibliai' for x in h), h)

    def test_egyfejezetes_konyv(self):
        h = B.hivatkozasok('H9999. x אב noun Obad 8; Obadiah 13.')
        self.assertEqual([(x['konyv'], x['c'], x['v']) for x in h], [('Abd', 1, 8), ('Abd', 1, 13)])

    def test_nincs_elozmeny(self):
        h = B.hivatkozasok('H9999. x אב noun see 4:5.')
        self.assertEqual((h[0]['konyv'], h[0]['okkod'], h[0]['konyv_mod']), (None, 'nincs_elozmeny', 'feloldhatatlan'))


class Jelentespont(unittest.TestCase):
    def test_alpont_es_fej(self):
        t = 'H9999. x אב noun father; — Gen 1:1; — 1 morning: a. of end Exod 10:13. b. of dawn Gen 29:25. 2 morrow Exod 16:19.'
        r = B.szeletel(t, 'אב')
        sav = B.csomopont_savok(t, r)
        pont = {(x['c'], x['v']): B.jelentespont(x['poz'], sav)[1] for x in B.hivatkozasok(t)}
        self.assertEqual(pont[(1, 1)], 'fej')
        self.assertEqual(pont[(10, 13)], '-/1/a')
        self.assertEqual(pont[(29, 25)], '-/1/b')
        self.assertEqual(pont[(16, 19)], '-/2')


class SzerkezetJavitas(unittest.TestCase):
    """F99 M2: a pont nélküli angol személyszám és a könyvnév része nem jelentés-sorszám; a „2 2nd son” jelölő (aranyminta 2.3/1–2)."""

    @classmethod
    def setUpClass(cls):
        cls.en, cls.lem = {}, {}
        for d in V.tsv_sorok(V.BDB_EN):
            if d['Strong_padded'] in ('H3615', 'H0776', 'H4908', 'H0029', 'H5022', 'H0157'):
                cls.en[d['Strong_padded']] = d['Teljes_szocikk']

    def jelek(self, s, torzs=None):
        r = B.szeletel(self.en[s])
        for t in r['torzsek']:
            if torzs is None or t['nev'] == torzs:
                return [(j['jel'], [a['jel'] for a in j['al']]) for j in t['jelentesek'] if j['jel']]

    def test_szemelyszam_nem_jelolo(self):
        self.assertEqual(self.jelek('H3615', 'Qal'), [('1', ['a', 'b', 'c', 'd']), ('2', ['a', 'b', 'c'])])
        self.assertTrue(B.szeletel(self.en['H0157'])['torzsek'][0]['jelentesek'][1]['szoveg'].startswith('human love'))

    def test_valodi_tobbes_jelentes_marad(self):
        self.assertIn(('5', []), self.jelek('H0776'))                           # „5 plural אֲרָצוֺת is almost wholly late”
        self.assertIn('3', [j for j, _ in self.jelek('H4908')])                 # „3 plural מִשְׁכָּנוֺת, dwellings”

    def test_konyvnev_szama_nem_jelolo_es_sorszamnev(self):
        self.assertEqual(self.jelek('H5022'), [])                                # „1 Kings 21”
        self.assertEqual([j for j, _ in self.jelek('H0029')], [str(i) for i in range(1, 9)])   # „2 Chronicles 13:23. 2 2nd son”


class Tabla(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sorok, _ = V.general('2026-10-15', ['H1242', 'H0006', 'H0015', 'H0196', 'H0226'])

    def test_minden_sorban_jelentespont_feloldasi_mod_es_proveniencia(self):
        i = {k: n for n, k in enumerate(V.FEJ)}
        for s in self.sorok:
            self.assertEqual(len(s), len(V.FEJ))
            self.assertTrue(s[i['utvonal']], s)
            self.assertIn(s[i['konyv_feloldas']], ('kiirt', 'orokolt', 'folytatas', 'feloldhatatlan'))
            self.assertTrue(s[i['proveniencia']].startswith('scope=%s | forras=bdb_vers_jelentes@' % s[0]), s)
            self.assertNotIn('manual', s[i['proveniencia']])
            if s[i['szurt']] == '1':
                self.assertEqual(s[i['karoli_vers']], '')

    def test_h1242_atkulcsolas_es_alpont(self):
        x = sor(self.sorok, strong='H1242', nyers='Lev 6:2')[0]
        i = {k: n for n, k in enumerate(V.FEJ)}
        self.assertEqual((x[i['mt_vers']], x[i['karoli_vers']], x[i['vers_feloldas']], x[i['utvonal']]),
                         ('3Móz 6:2', '3Móz 6:9', 'atkulcsolt', '-/1/a'))

    def test_tagolatlan_szocikk(self):
        x = sor(self.sorok, strong='H0196')[0]
        self.assertEqual(x[V.FEJ.index('utvonal')], 'tagolatlan')
        self.assertEqual(x[V.FEJ.index('karoli_vers')], 'Zak 11:15')

    def test_sigla_tapadt_kiszurve(self):
        x = sor(self.sorok, strong='H0015', nyers='Job 34:36')[0]
        self.assertEqual((x[V.FEJ.index('okkod')], x[V.FEJ.index('szurt')], x[V.FEJ.index('karoli_vers')]), ('sigla_tapadt', '1', ''))


@unittest.skipUnless(os.environ.get('PARDES_LASSU') or os.name == 'nt', 'a teljes újragenerálás lassú a /mnt/c-n (PARDES_LASSU=1 kapcsolja be)')
class Ujrageneralas(unittest.TestCase):
    def test_bajtra_azonos(self):
        with open(V.KI, encoding='utf-8', newline='') as f:
            regi = f.read()
        ts = regi.split('--ts ', 1)[1].split(' ', 1)[0]
        sorok, mh = V.general(ts)
        self.assertEqual(V.kiir(sorok, mh, ts), regi)


if __name__ == '__main__':
    unittest.main(verbosity=1)
