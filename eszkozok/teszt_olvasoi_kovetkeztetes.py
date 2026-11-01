"""Az olvasói szövegek (lelet + következtetés) tesztje: eszkozok/olvasoi_kovetkeztetes.py.

A felhasználó, 2026-10-30: „mindig vanjuk le a következtetést a találtakból . a magyarázó szöveg az adatokból
induljon.” — minden szöveg a számokkal kezd, és a rögzített szabály szerinti következtetéssel zár.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import olvasoi_kovetkeztetes as OK  # noqa: E402


class Fokok(unittest.TestCase):
    def test_kuszobok(self):
        self.assertEqual([OK.fok(x) for x in (0.95, 0.9, 0.8, 0.67, 0.6, 0.5, 0.49)],
                         ['szinte', 'szinte', 'tobbseg', 'tobbseg', 'fele', 'fele', 'keves'])

    def test_szorzo(self):
        self.assertEqual(OK._szorzo(93 / 33), 'majdnem háromszor annyi')
        self.assertEqual(OK._szorzo(2.3), 'több mint kétszer annyi')
        self.assertEqual(OK._szorzo(3.0), 'háromszor annyi')
        self.assertEqual(OK._szorzo(1.5), 'másfélszer annyi')
        self.assertEqual(OK._szorzo(1.0), 'körülbelül annyi')
        self.assertEqual(OK._szorzo(0.1), 'kevesebb')


class Szovegek(unittest.TestCase):
    def test_lelet_elol_kovetkeztetes_vegul(self):
        szovegek = [
            OK.elofordulasok(33, 23, 10, 16, [('1Móz', 5), ('Zsolt', 5)], 32),
            OK.kizart(93, 92, 1, [('a formula nincs a versben', 40), ('névadás', 9)], [('TSK-ajánlás', 18)], 33),
            OK.kulcsszavak([('héber', ['a kárá', 'a sém'], 23), ('görög', ['az epikaleó'], 10)]),
            OK.lxx(23, 19, 3, 1, 0, 'az epikaleó'),
            OK.kereszthivatkozasok(33, 24, 107),
            OK.minosites(20, 17, 33, osszes=107),
            OK.kapcsolatok(25, 31, [('Párhuzam', 22), ('Beteljesedés', 2), ('Variáns', 1)], 19),
            OK.kapcsolodo([('ALVIL-001', 'szomszédos', 'közepes')], 5),
            OK.sece('az epikaleó', 8, ['a kárá']),
            OK.versenkenti([('az epikaleó', 10, 9, 'újszövetségi')]),
        ]
        for sz in szovegek:
            self.assertRegex(sz.split(OK.KOVETKEZTETES)[0], r'\d', sz)  # a lelet számmal, a következtetés előtt
            self.assertIn(OK.KOVETKEZTETES, sz)
            self.assertNotIn('gerinc', sz)

    def test_elofordulasok(self):
        sz = OK.elofordulasok(33, 23, 10, 16, [('1Móz', 5), ('Zsolt', 5)], 32)
        self.assertIn('(23 ószövetségi, 10 újszövetségi hely)', sz)
        self.assertIn('a legtöbb hely: 1Móz és Zsolt (5-5)', sz)
        self.assertIn('mindkét szövetségben', sz)
        self.assertIn('szinte mind biztosan', sz)
        self.assertIn('csak az Ószövetségben', OK.elofordulasok(5, 5, 0, 2, [('Zsolt', 4)], 2))

    def test_kizart_hatar(self):
        self.assertIn('ez az ok húzza meg: „a formula nincs a versben”',
                      OK.kizart(93, 92, 1, [('a formula nincs a versben', 40)], [], 33))
        self.assertIn('több ok együtt', OK.kizart(10, 10, 0, [('a', 3), ('b', 3)], [], 5))

    def test_kulcsszavak(self):
        self.assertIn('az Ószövetségben két szó együttes jelenléte kell a motívumhoz, az Újszövetségben egy szó elég',
                      OK.kulcsszavak([('görög', ['az epikaleó'], 10), ('héber', ['a kárá', 'a sém'], 23)]))
        self.assertIn('mindkét szövetségben egyetlen szó jelzi a motívumot',
                      OK.kulcsszavak([('héber', ['a seól'], 64), ('görög', ['a Hadész'], 8)]))

    def test_lxx(self):
        self.assertIn('a legtöbb helyen (83%)', OK.lxx(23, 19, 3, 1, 0, 'az epikaleó'))
        self.assertIn('nem nyelvi, csak tartalmi', OK.lxx(10, 2, 8, 0, 0, ''))

    def test_minosites(self):
        self.assertIn('a fele (52%)', OK.minosites(20, 17, 33, osszes=107))
        self.assertIn('gyenge', OK.minosites(21, 19, 72, osszes=124))
        self.assertIn('nincs független külső megerősítése', OK.minosites(0, 0, 10))

    def test_kapcsolatok(self):
        self.assertIn('túlnyomórészt párhuzamos', OK.kapcsolatok(25, 31, [('Párhuzam', 22), ('Variáns', 3)], 19))
        self.assertIn('beteljesedésbe tartó láncot', OK.kapcsolatok(4, 5, [('Beteljesedés', 3), ('Párhuzam', 1)], 4))

    def test_kapcsolodo(self):
        self.assertIn('csak szövegközelség', OK.kapcsolodo([('X', 'szomszédos', 'közepes')], 0))
        self.assertIn('tartalmi kapcsolattal', OK.kapcsolodo([('X', 'tematikus', 'magas')], 0))

    def test_sece(self):
        self.assertIn('megerősíti', OK.sece('az epikaleó', 8, ['a kárá']))
        self.assertIn('hanem a kárá felel meg', OK.sece('a sém', 6, [], tars='a kárá'))
        self.assertIn('nem ismeri', OK.sece('a sém', 6, []))

    def test_ures(self):
        self.assertIsNone(OK.elofordulasok(0, 0, 0, 0, [], 0))
        self.assertIsNone(OK.lxx(0, 0, 0, 0, 0, ''))
        self.assertIsNone(OK.versenkenti([('az epikaleó', 0, 0, 'újszövetségi')]))


if __name__ == '__main__':
    unittest.main()
