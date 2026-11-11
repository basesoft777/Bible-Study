"""F197: a harmadik tanú (Sefaria BDB) összevetési szabályának és kapcsolójának tesztjei.
Futtatás: python eszkozok/teszt_futtat.py (a gyorsítótár és a hálózat nélkül fut)."""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_sefaria_tanu as S  # noqa: E402
import bdb_vers_jelentes as V  # noqa: E402


class Osszevet(unittest.TestCase):
    def test_egyezik_torzs_rovidites(self):
        self.assertEqual(S.osszevet('', '', "Hiph'il/1/a", '1||Hiph./1/a', False), 'egyezik')

    def test_szam_hiany_elteres(self):
        # a „fej” ↔ „1.”: a szám hiánya is eltérés (seed-103 s103-N013 osztálya)
        self.assertEqual(S.osszevet('', '', 'fej', '1||-/1/-', False), 'elter')
        self.assertEqual(S.osszevet('', '', 'fej', '1||-/-/-', False), 'egyezik')

    def test_betu_csak_ha_mindketto(self):
        self.assertEqual(S.osszevet('', '', '-/1/b', '1||-/1/-', False), 'egyezik')
        self.assertEqual(S.osszevet('', '', '-/1/b', '1||-/1/c', False), 'elter')

    def test_torzs_elter(self):
        self.assertEqual(S.osszevet('', '', 'Qal/2', '1||Hiph./2/-', False), 'elter')

    def test_homonima_nem_szamit(self):
        # v2: a Sefaria felső indexe nem a BDB római száma (H2022 הַר: a BDB-ben számozatlan, a Sefariában „²”)
        self.assertEqual(S.osszevet('', '', '-/1/h', '2||-/1/h', False), 'egyezik')
        self.assertEqual(S.osszevet('I', '', '-/1/f', '2||-/1/f', True), 'egyezik')

    def test_resz(self):
        self.assertEqual(S.osszevet('', 'I', '-/1/f', '2|II|-/1/f', False), 'elter')
        self.assertEqual(S.osszevet('', '', '-/1/f', '2|II|-/1/f', False), 'egyezik')

    def test_torzs_hiany(self):
        # v3: a táblában kifejezetten törzs nélküli számozott pont ↔ Sefaria-törzs: eltérés (s103-N061); a fej nem
        self.assertEqual(S.osszevet('II', '', '-/2', '2||Pi./2/-', True), 'elter')
        self.assertEqual(S.osszevet('', '', 'fej', '1||Qal/-/-', False), 'egyezik')
        self.assertEqual(S.osszevet('', '', '-/2', '1||-/2/-', False), 'egyezik')

    def test_barmely(self):
        self.assertEqual(S.osszevet('', '', '-/4/a', '1||-/1/-;1||-/4/a', False), 'egyezik')

    def test_nincs(self):
        self.assertEqual(S.osszevet('', '', '-/4/a', '', False), 'nincs')

    def test_ref_versek(self):
        self.assertEqual(S.ref_versek('I Samuel 25:37'), ['1Sám 25:37'])
        self.assertEqual(S.ref_versek('Exodus 20:9-10'), ['2Móz 20:9', '2Móz 20:10'])
        self.assertEqual(S.ref_versek('BDB, אוֹרָה'), [])

    def test_fa_utak(self):
        e = {'content': {'senses': [
            {'definition': 'pf. <a data-ref="Genesis 1:1">Gn 1:1</a>'},
            {'form': 'Qal', 'senses': [
                {'num': '1.', 'senses': [{'num': 'a.', 'senses': [{'definition': '<a data-ref="Exodus 2:3">x</a>'}]}]},
                {'num': '2.', 'senses': [{'num': '(1)', 'definition': '<a data-ref="Exodus 2:4">x</a>'}]}]}]}}
        self.assertEqual(S.fa_utak(e), [('1Móz 1:1', ('', '', '', '')), ('2Móz 2:3', ('', 'Qal', '1', 'a')),
                                        ('2Móz 2:4', ('', 'Qal', '2', ''))])


class Kapcsolo(unittest.TestCase):
    def test_alapbol_kikapcsolva(self):
        # DT-F197a: a HAMART kiadása alatt a 2.29 nem változhat; a bekapcsolás külön lépés
        self.assertFalse(V.SEFARIA_TANU)

    def test_itelet_mas_vers(self):
        tanu = {('H0001', '3'): ('1Móz 1:1', 'pontos', '1||-/1/-')}
        self.assertEqual(S.itelet(tanu, 'H0001', 3, '1Móz 1:2', '', '', '-/1'), 'nincs')
        self.assertEqual(S.itelet(tanu, 'H0001', 3, '1Móz 1:1', '', '', '-/1'), 'egyezik')


if __name__ == '__main__':
    unittest.main()
