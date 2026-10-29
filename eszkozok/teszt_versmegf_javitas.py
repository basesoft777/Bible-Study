"""A `versmegf_javitas` (F117, DT-F117a–e) egységtesztje. Futtatás: python eszkozok/teszt_versmegf_javitas.py

Két rész: (1) szintetikus táblán a felülírás, a pótlás, a rendezés, a halmaz-őr és a bemenet-ellenőrzés;
(2) a repó generált tábláján (a KK4 kimenetén) a javított sorok — egy pótolt fejezet, egy KEZI-pár, a Dán 3:31,
egy D-eltolás, egy D′-szomszéd, egy változatlan sor és egy KEZI + igehely_mt sor, valamint a Jóel F146-sorai
(DT-F146b) — és az idempotencia.
"""
import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import versmegf_javitas as V  # noqa: E402

FEJ = '\t'.join(V.FEJ)


def _csendes(*_a, **_k):
    pass


def tabla_sorok():
    with open(V.TABLA, encoding='utf-8', newline='') as f:
        s = f.read().split('\n')
    return s[:-1] if s and s[-1] == '' else s


def tabla_dict():
    return {l.split('\t')[0]: l.split('\t') for l in tabla_sorok() if l and not l.startswith('#') and not l.startswith('igehely_karoli\t')}


class Szintetikus(unittest.TestCase):
    ALAP = ['# GENERÁLT: teszt', FEJ,
            'Jón 1:1\t1:1\t\tKJV\tszamlalas\t',
            'Jón 2:1\t2:1\t2:1\tMT\ttvtms\t',
            'Jón 2:2\t2:2\t2:2\tMT\ttvtms\t']
    JAV = {'Jón 2:1': ('1:17', '2:1', 'MT', V.FORRAS, 'elozo: x'),
           'Jón 2:10': ('2:9', '2:10', 'MT', V.FORRAS, 'potolt: nincs_sor')}

    def test_felulir_potol_rendez(self):
        uj = V.javit(self.ALAP, javitas=self.JAV, naplo=_csendes)
        adat = [l for l in uj if not l.startswith('#') and l != FEJ]
        self.assertEqual([l.split('\t')[0] for l in adat], ['Jón 1:1', 'Jón 2:1', 'Jón 2:10', 'Jón 2:2'])
        self.assertEqual(adat[1], 'Jón 2:1\t1:17\t2:1\tMT\t%s\telozo: x' % V.FORRAS)
        self.assertEqual(adat[0], self.ALAP[2])   # változatlan
        self.assertEqual(adat[3], self.ALAP[4])   # változatlan
        self.assertEqual(sum(1 for l in uj if l.startswith(V.JEGYZET_ELO)), 1)

    def test_idempotens(self):
        uj = V.javit(self.ALAP, javitas=self.JAV, naplo=_csendes)
        self.assertEqual(V.javit(uj, javitas=self.JAV, naplo=_csendes), uj)

    def test_halmaz_or_negativ_kivul_valtozott(self):
        # F117.8 (8): a halmazon kívüli változás a valódi őrön elbukik
        uj = V.javit(self.ALAP, javitas=self.JAV, naplo=_csendes)
        rossz = [l.replace('Jón 1:1\t1:1\t', 'Jón 1:1\t1:2\t') if l.startswith('Jón 1:1\t') else l for l in uj]
        self.assertNotEqual(rossz, uj)
        with self.assertRaises(V.HalmazOrHiba):
            V.halmaz_or(self.ALAP, rossz, self.JAV.keys())
        V.halmaz_or(self.ALAP, uj, self.JAV.keys())   # a helyes kimenet átmegy

    def test_halmaz_or_negativ_torles_idegen_fejlec(self):
        uj = V.javit(self.ALAP, javitas=self.JAV, naplo=_csendes)
        with self.assertRaises(V.HalmazOrHiba):      # törölt halmazon kívüli sor
            V.halmaz_or(self.ALAP, [l for l in uj if not l.startswith('Jón 2:2\t')], self.JAV.keys())
        with self.assertRaises(V.HalmazOrHiba):      # idegen új kulcs
            V.halmaz_or(self.ALAP, uj + ['Jón 3:1\t3:1\t\tKJV\tszamlalas\t'], self.JAV.keys())
        with self.assertRaises(V.HalmazOrHiba):      # megváltozott (nem-F117) fejlécsor
            V.halmaz_or(self.ALAP, ['# GENERÁLT: más'] + uj[1:], self.JAV.keys())

    def test_belso_ures_sor_hiba(self):
        rossz = self.ALAP[:3] + [''] + self.ALAP[3:]
        with self.assertRaises(V.UresSorHiba):
            V.javit(rossz, javitas=self.JAV, naplo=_csendes)
        # a záró üres sor (fájlvégi sorvég) megengedett
        V.javit(self.ALAP + [''], javitas=self.JAV, naplo=_csendes)

    def test_rendezetlen_tabla_megall(self):
        rossz = self.ALAP[:2] + [self.ALAP[3], self.ALAP[2]]
        with self.assertRaises(AssertionError):
            V.javit(rossz, javitas=self.JAV, naplo=_csendes)

    def _bemenet(self, sor):
        f = tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.tsv', delete=False, newline='\n')
        f.write('# teszt\n' + FEJ + '\tproveniencia\n' + sor + '\n')
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_bemenet_kjv_osztaly_mt_nelkul(self):
        p = self._bemenet('Jón 2:1\t2:1\t2:1\tKJV\t%s\t-\tscope=manual' % V.FORRAS)
        with self.assertRaises(AssertionError):
            V.betolt(p)

    def test_bemenet_kezi_mt_kell(self):
        p = self._bemenet('Hós 2:1\t2:2\t\tKEZI\t%s\t-\tscope=manual' % V.FORRAS)
        with self.assertRaises(AssertionError):
            V.betolt(p)

    def test_bemenet_f146_kezi_kjv_azonos(self):
        # DT-F146b: macula_mt_f146-sorban a KEZI a Károli = KJV ≠ MT esetet is jelenti
        p = self._bemenet('Jóel 2:32	2:32	3:5	KEZI	%s	-	scope=gepi' % V.FORRAS_F146)
        self.assertEqual(V.betolt(p)['Jóel 2:32'][:3], ('2:32', '3:5', 'KEZI'))

    def test_bemenet_f146_kezi_mt_kell(self):
        for sor in ('Jóel 2:32	2:32		KEZI	%s	-	scope=gepi', 'Jóel 2:32	2:32	2:32	KEZI	%s	-	scope=gepi'):
            p = self._bemenet(sor % V.FORRAS_F146)
            with self.assertRaises(AssertionError):
                V.betolt(p)

    def test_bemenet_f117_kezi_kjv_azonos_tilos(self):
        # az F117-sorokra a DT-F117e szabály marad (KEZI: igehely_kjv ≠ Károli-szám)
        p = self._bemenet('Jóel 2:32	2:32	3:5	KEZI	%s	-	scope=gepi' % V.FORRAS)
        with self.assertRaises(AssertionError):
            V.betolt(p)

    def test_bemenet_rossz_forras(self):
        p = self._bemenet('Jón 2:3\t2:2\t2:3\tMT\tkezi\t-\tscope=manual')
        with self.assertRaises(AssertionError):
            V.betolt(p)


class GeneraltTabla(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tabla_dict()

    def sor(self, k):
        self.assertIn(k, self.t, k)
        return self.t[k][1:5]

    def test_potolt_fejezet_hos_14(self):
        self.assertEqual(self.sor('Hós 14:1'), ['13:16', '14:1', 'MT', V.FORRAS])
        self.assertEqual(self.sor('Hós 14:10'), ['14:9', '14:10', 'MT', V.FORRAS])
        self.assertEqual(sum(1 for k in self.t if k.startswith('Hós 14:')), 10)

    def test_kezi_par_pred_9_21(self):
        self.assertEqual(self.sor('Préd 9:21'), ['10:1', '10:1', 'KEZI', V.FORRAS])
        self.assertEqual(self.sor('Jób 39:34'), ['40:1', self.t['Jób 39:34'][2], 'KEZI', V.FORRAS])

    def test_dan_3_31(self):
        self.assertEqual(self.sor('Dán 3:31'), ['4:1', '3:31', 'MT', V.FORRAS])

    def test_d_eltolas_jon_2_3(self):
        self.assertEqual(self.sor('Jón 2:3'), ['2:2', '2:3', 'MT', V.FORRAS])
        self.assertEqual(self.sor('Ézs 3:1'), ['2:22', '2:22', 'KEZI', V.FORRAS])

    def test_d_vesszo_szomszed_1kir_22_45(self):
        self.assertEqual(self.sor('1Kir 22:45'), ['22:44', '22:45', 'MT', V.FORRAS])
        # 2-1 (DT-F117c (3) (a)): két Károli-vers ugyanazon a KJV-versen
        self.assertEqual(self.t['1Kir 22:43'][1], '22:43')
        self.assertEqual(self.t['1Kir 22:44'][1], '22:43')

    def test_valtozatlan_sor(self):
        self.assertEqual(self.t['1Móz 1:1'][1:5], ['1:1', '', 'KJV', 'szamlalas'])
        self.assertEqual(self.t['1Kir 22:42'][4] != V.FORRAS, True)

    def test_kezi_mt_sor_hos_2_1(self):
        # DT-F117e: KEZI kitöltött igehely_mt-vel — Károli ≠ KJV és ≠ MT
        self.assertEqual(self.sor('Hós 2:1'), ['2:2', '2:4', 'KEZI', V.FORRAS])

    def test_javitas_halmaz_teljes(self):
        jav = V.betolt()
        self.assertEqual(len(jav), 372)
        self.assertEqual(sum(1 for v in jav.values() if v[3] == V.FORRAS), 346)
        self.assertEqual(sum(1 for v in jav.values() if v[3] == V.FORRAS_F146), 26)
        for k, (kjv, mt, osz, forras, megj) in jav.items():
            self.assertEqual(self.t[k][1:6], [kjv, mt, osz, forras, megj], k)

    def test_idempotens_a_tablan(self):
        sorok = tabla_sorok()
        self.assertEqual(V.javit(sorok, naplo=_csendes), sorok)

    def test_fejlec_jegyzet(self):
        jegyzet = [l for l in tabla_sorok() if l.startswith(V.JEGYZET_ELO)]
        self.assertEqual(len(jegyzet), 1)
        self.assertIn('KEZI kitöltött igehely_mt-vel', jegyzet[0])
        self.assertIn('346 sor', jegyzet[0])
        f146 = [l for l in tabla_sorok() if l.startswith(V.JEGYZET_F146)]
        self.assertEqual(len(f146), 1)
        self.assertIn('26 sor', f146[0])

    def test_joel_f146(self):
        # DT-F146b: Károli 2:28–32 = MT 3:1–5, Károli 3:1–21 = MT 4:1–21; a 2:27 változatlan
        self.assertEqual(self.sor('Jóel 2:28'), ['2:28', '3:1', 'KEZI', V.FORRAS_F146])
        self.assertEqual(self.sor('Jóel 2:32'), ['2:32', '3:5', 'KEZI', V.FORRAS_F146])
        self.assertEqual(self.sor('Jóel 3:1'), ['3:1', '4:1', 'KEZI', V.FORRAS_F146])
        self.assertEqual(self.sor('Jóel 3:21'), ['3:21', '4:21', 'KEZI', V.FORRAS_F146])
        self.assertEqual(self.t['Jóel 2:27'][1:5], ['2:27', '', 'KJV', 'szamlalas'])
        self.assertEqual(sum(1 for k in self.t if k.startswith('Jóel ') and self.t[k][4] == V.FORRAS_F146), 26)


if __name__ == '__main__':
    unittest.main()
