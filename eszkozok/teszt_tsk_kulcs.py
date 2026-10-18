"""A `tsk_kulcs` átváltó egységtesztje (F114). Futtatás: python eszkozok/teszt_tsk_kulcs.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tsk_kulcs as T  # noqa: E402


class KulcsTeszt(unittest.TestCase):
    def test_pred_9_12(self):
        self.assertEqual(T.karoli_to_kjv('Préd 9:12'), 'Préd 9:10')
        self.assertEqual(T.kjv_to_karoli('Préd 9:10'), ['Préd 9:12'])

    def test_zsolt_18_6(self):
        self.assertEqual(T.karoli_to_kjv('Zsolt 18:6'), 'Zsolt 18:5')
        self.assertEqual(T.kjv_to_karoli('Zsolt 18:6'), ['Zsolt 18:7'])

    def test_zsoltarfelirat_nincs_par(self):
        self.assertIsNone(T.karoli_to_kjv('Zsolt 18:1'))   # felirat: nincs KJV-pár
        self.assertEqual(T.kjv_to_karoli('Zsolt 18:1'), ['Zsolt 18:2'])

    def test_4moz_13_34(self):
        self.assertEqual(T.karoli_to_kjv('4Móz 13:34'), '4Móz 13:33')
        self.assertEqual(T.kjv_to_karoli('4Móz 13:33'), ['4Móz 13:34'])

    def test_kjv_vers_karoli_par_nelkul(self):
        self.assertEqual(T.kjv_to_karoli('Hós 2:23'), [])  # explicit "nincs pár"

    def test_egy_a_tobbhoz(self):
        # A tábla ma kölcsönösen egyértelmű (nincs egy-a-többhöz eset); a teszt ezt rögzíti.
        T._betolt()
        self.assertTrue(all(len(v) == 1 for v in T._J2K.values()))
        kj = [v for v in T._K2J.values() if v]
        self.assertEqual(len(kj), len(set(kj)))

    def test_mt_tartalek_szamlalas(self):
        # DT-F114d (b): MT|szamlalas, üres igehely_kjv -> az igehely_mt a KJV-kulcs
        self.assertEqual(T.karoli_to_kjv('1Sám 17:12'), '1Sám 17:12')
        self.assertEqual(T.kjv_to_karoli('1Sám 17:12'), ['1Sám 17:12'])
        self.assertEqual(T.kjv_to_karoli('Jer 33:15'), ['Jer 33:15'])

    def test_mt_tartalek_negativ(self):
        T._betolt()
        # nincs_sor (a Károli-versnek nincs sora a táblában): nincs pár
        self.assertEqual(T.kjv_to_karoli('Hós 14:2'), [])
        # MT|lxx_os_etalon_f91 felirat: nincs KJV-pár, az MT-szám nem lesz KJV-kulcs
        self.assertIsNone(T.karoli_to_kjv('Zsolt 18:1'))
        # KEZI|kezi_identitas_javitas és KJV|lxx_os_etalon_f91 (felirat): nincs pár
        for v in ('Jób 39:34', 'Préd 9:21', 'Zsolt 13:1'):
            self.assertIsNone(T.karoli_to_kjv(v), v)

    def test_1kir_22_kivetel_nincs_par(self):
        # scope=manual kivétel: az MT-tartalék itt eltolt párt adna
        for v in (46, 47, 48, 49):
            self.assertIsNone(T.karoli_to_kjv('1Kir 22:%d' % v), v)
            self.assertEqual(T.kjv_to_karoli('1Kir 22:%d' % v), [], v)
        self.assertEqual(T.karoli_to_kjv('1Kir 22:45'), '1Kir 22:45')

    def test_azonos_vers(self):
        self.assertEqual(T.karoli_to_kjv('1Móz 1:1'), '1Móz 1:1')
        self.assertEqual(T.kjv_to_karoli('1Móz 1:1'), ['1Móz 1:1'])

    def test_usz_azonossag_kimondott_korlat(self):
        self.assertFalse(T.fedett_konyv('Mt 5:3'))
        self.assertEqual(T.karoli_to_kjv('Jel 12:18'), 'Jel 12:18')
        self.assertEqual(T.kjv_to_karoli('Jel 13:1'), ['Jel 13:1'])

    def test_nem_ertelmezheto(self):
        self.assertIsNone(T.karoli_to_kjv('1Móz 1'))
        self.assertEqual(T.kjv_to_karoli('1Móz'), [])

    def test_karoli_sorok(self):
        sorok = [
            {'Igehely': 'Préd 9:10', 'Kapcsolódó igehely': 'Zsolt 16:10',
             'Kapcsolódó igehely magyar megjelenítése': 'Zsolt 16,10', 'Votes': '71'},
            {'Igehely': 'Zsolt 18:5', 'Kapcsolódó igehely': 'Zsolt 49:15',
             'Kapcsolódó igehely magyar megjelenítése': 'Zsolt 49,15', 'Votes': '20'},
            {'Igehely': 'Zsolt 18:1', 'Kapcsolódó igehely': 'Hós 2:23',
             'Kapcsolódó igehely magyar megjelenítése': 'Hós 2,23', 'Votes': '3'},
            {'Igehely': 'Mt 5:3', 'Kapcsolódó igehely': 'Lk 6:20',
             'Kapcsolódó igehely magyar megjelenítése': 'Lk 6,20', 'Votes': '9'},
        ]
        np = []
        ki = list(T.karoli_sorok(sorok, np))
        self.assertEqual([(o['Igehely'], o['Kapcsolódó igehely']) for o in ki],
                         [('Préd 9:12', 'Zsolt 16:10'), ('Zsolt 18:6', 'Zsolt 49:16'),
                          ('Mt 5:3', 'Lk 6:20')])
        self.assertEqual(ki[1]['Kapcsolódó igehely magyar megjelenítése'], 'Zsolt 49,16')
        self.assertEqual(ki[1]['KJV Igehely'], 'Zsolt 18:5')
        # Zsolt 18:1 (KJV) -> Károli 18:2, a cél Hós 2:23 -> nincs Károli-pár
        self.assertEqual([(r['Igehely'], oldal) for r, oldal in np], [('Zsolt 18:1', 'cel')])


if __name__ == '__main__':
    unittest.main()
