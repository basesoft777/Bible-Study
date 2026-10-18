"""A `tsk_kulcs` átváltó egységtesztje (F114; F117.4: a kivételek helyett pozitív párok). Futtatás: python eszkozok/teszt_tsk_kulcs.py"""
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

    def test_kjv_vers_karoli_par(self):
        # F117 (DT-F117a): a Hós 2 pótolva; a szöveg-összevetés (naplok/F117_itelet.tsv): Károli Hós 2:22 = KJV 2:23
        self.assertEqual(T.kjv_to_karoli('Hós 2:23'), ['Hós 2:22'])
        # N-F117b: a Károli-összevonás második KJV-versének nincs saját Károli-verse -> explicit "nincs pár"
        # (Hós 1:11 = KJV 1:11 + 2:1; Jób 16:22 = KJV 16:22 + 17:1; naplok/F117_bizonytalan.md 3. pont)
        self.assertEqual(T.kjv_to_karoli('Hós 2:1'), [])
        self.assertEqual(T.kjv_to_karoli('Jób 17:1'), [])

    def test_egy_a_tobbhoz(self):
        # DT-F117c (3) (a): két Károli-vers egy KJV-versen — pontosan ez a két eset; más egy-a-többhöz nincs.
        T._betolt()
        tobb = {j: sorted(v) for j, v in T._J2K.items() if len(v) > 1}
        self.assertEqual(tobb, {'1Kir 22:43': ['1Kir 22:43', '1Kir 22:44'],
                                '1Sám 20:42': ['1Sám 20:42', '1Sám 20:43']})
        kj = [v for v in T._K2J.values() if v]
        self.assertEqual(len(kj) - len(set(kj)), 2)

    def test_mt_tartalek_szamlalas(self):
        # DT-F114d (b): MT|szamlalas, üres igehely_kjv -> az igehely_mt a KJV-kulcs
        self.assertEqual(T.karoli_to_kjv('1Sám 17:12'), '1Sám 17:12')
        self.assertEqual(T.kjv_to_karoli('1Sám 17:12'), ['1Sám 17:12'])
        self.assertEqual(T.kjv_to_karoli('Jer 33:15'), ['Jer 33:15'])

    def test_mt_tartalek_negativ(self):
        T._betolt()
        # nincs_sor: az F117 halmazán kívüli tábla-lyuk (naplok/F117_javitas_jelentes.md 5. pont) -> nincs pár.
        # FIGYELEM: ez a MAI, hiányos állapot (N-F117d: Károli Préd 9:1 = KJV Préd 8:16, Jób 39:1 = KJV Jób 38:39);
        # a pótláskor az elvárás megfordítandó (az N-F117d javításakor).
        self.assertIsNone(T.karoli_to_kjv('Préd 9:1'))
        self.assertIsNone(T.karoli_to_kjv('Jób 39:1'))
        # MT|lxx_os_etalon_f91 felirat: nincs KJV-pár, az MT-szám nem lesz KJV-kulcs
        self.assertIsNone(T.karoli_to_kjv('Zsolt 18:1'))
        self.assertIsNone(T.karoli_to_kjv('Zsolt 13:1'))
        # F117: a korábbi nincs_sor / KEZI|kezi_identitas_javitas sorok a szöveg-összevetés szerinti párt kapják
        # (naplok/F117_itelet.tsv): Károli Hós 14:3 = KJV 14:2; Jób 39:34 = KJV 40:1; Préd 9:21 = KJV 10:1
        self.assertEqual(T.kjv_to_karoli('Hós 14:2'), ['Hós 14:3'])
        self.assertEqual(T.karoli_to_kjv('Hós 14:2'), 'Hós 14:1')
        self.assertEqual(T.karoli_to_kjv('Jób 39:34'), 'Jób 40:1')
        self.assertEqual(T.karoli_to_kjv('Préd 9:21'), 'Préd 10:1')

    def test_1kir_22_par(self):
        # F117 (a korábbi kivétel helyett): Károli 1Kir 22:46–49 = KJV 22:45–48; 22:45 = KJV 22:44 (naplok/F117_itelet.tsv)
        for v in (46, 47, 48, 49):
            self.assertEqual(T.karoli_to_kjv('1Kir 22:%d' % v), '1Kir 22:%d' % (v - 1), v)
            self.assertEqual(T.kjv_to_karoli('1Kir 22:%d' % (v - 1)), ['1Kir 22:%d' % v], v)
        self.assertEqual(T.karoli_to_kjv('1Kir 22:45'), '1Kir 22:44')
        self.assertEqual(T.karoli_to_kjv('1Kir 22:54'), '1Kir 22:53')

    def test_kivetel_fejezetek_par(self):
        # F117 (a korábbi kivételek helyett), a szöveg-összevetés szerint (naplok/F117_itelet.tsv)
        vart = {'Ézs 3:1': 'Ézs 2:22', 'Ézs 3:26': 'Ézs 3:25', 'Jón 2:1': 'Jón 1:17', 'Jón 2:2': 'Jón 2:1',
                'Jón 2:3': 'Jón 2:2', 'Jón 2:9': 'Jón 2:8', 'Jón 2:10': 'Jón 2:9', '1Sám 24:1': '1Sám 23:29',
                '1Sám 24:2': '1Sám 24:1', '1Sám 24:22': '1Sám 24:21', '1Sám 20:43': '1Sám 20:42'}
        for k, j in vart.items():
            self.assertEqual(T.karoli_to_kjv(k), j, k)
        self.assertEqual(T.kjv_to_karoli('Jón 2:2'), ['Jón 2:3'])
        self.assertEqual(T.kjv_to_karoli('1Sám 24:1'), ['1Sám 24:2'])
        # a határon kívüli szomszéd nem változik
        self.assertEqual(T.karoli_to_kjv('1Sám 23:28'), '1Sám 23:28')
        self.assertEqual(T.karoli_to_kjv('Ézs 4:2'), 'Ézs 4:2')   # a pótolt Ézs 4 azonos számú
        self.assertEqual(T.NINCS_PAR_KIVETEL, frozenset())

    def test_f117_referencia_teljes(self):
        # Nem körkörös: az elvárás a kézi ítélet (naplok/F117_itelet.tsv), nem a tábla; az Ézs 64:1-nél a DT-F117c (2)
        p = os.path.join(T.REPO, 'naplok', 'F117_itelet.tsv')
        n = 0
        with open(p, encoding='utf-8') as f:
            for s in f:
                if s.startswith('#') or s.startswith('igehely_karoli'):
                    continue
                k, itelet = s.rstrip('\n').split('\t')[:2]
                kjv = itelet.split(';')[0]          # DT-F117c (2): összevont versnél az első KJV-vers
                self.assertEqual(T.karoli_to_kjv(k), '%s %s' % (k.rsplit(' ', 1)[0], kjv), k)
                n += 1
        self.assertEqual(n, 346)

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
            {'Igehely': 'Zsolt 18:1', 'Kapcsolódó igehely': 'Hós 2:1',
             'Kapcsolódó igehely magyar megjelenítése': 'Hós 2,1', 'Votes': '2'},
            {'Igehely': 'Mt 5:3', 'Kapcsolódó igehely': 'Lk 6:20',
             'Kapcsolódó igehely magyar megjelenítése': 'Lk 6,20', 'Votes': '9'},
        ]
        np = []
        ki = list(T.karoli_sorok(sorok, np))
        self.assertEqual([(o['Igehely'], o['Kapcsolódó igehely']) for o in ki],
                         [('Préd 9:12', 'Zsolt 16:10'), ('Zsolt 18:6', 'Zsolt 49:16'),
                          ('Zsolt 18:2', 'Hós 2:22'), ('Mt 5:3', 'Lk 6:20')])
        self.assertEqual(ki[1]['Kapcsolódó igehely magyar megjelenítése'], 'Zsolt 49,16')
        self.assertEqual(ki[1]['KJV Igehely'], 'Zsolt 18:5')
        # F117: a KJV Hós 2:23 -> Károli Hós 2:22 (a pótolt Hós 2); a KJV Hós 2:1 -> nincs Károli-pár (N-F117b)
        self.assertEqual([(r['Igehely'], r['Kapcsolódó igehely'], oldal) for r, oldal in np],
                         [('Zsolt 18:1', 'Hós 2:1', 'cel')])


if __name__ == '__main__':
    unittest.main()
