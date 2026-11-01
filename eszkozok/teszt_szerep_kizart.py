"""Az 1/b. blokk olvasói formájának tesztjei (eszkozok/szerep_kizart.py; ISTENTISZT-001 arany lap, 2026-10-29).

  python -m unittest -q eszkozok.teszt_szerep_kizart
"""
import collections
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import szerep_kizart as SZKZ  # noqa: E402


class TestJelolesOka(unittest.TestCase):
    def test_tsk_szavazattal(self):
        c, t = SZKZ.jeloles_oka('TSK 1Móz 4:26 (Votes=42) | scope=x')
        self.assertEqual(c, 'TSK-ajánlás')
        self.assertEqual(t, 'TSK-ajánlás az 1Móz 4:26 helyről, 42 szavazat')

    def test_tsk_es_karoli(self):
        c, t = SZKZ.jeloles_oka('TSK/Károli-KH Zsolt 99:6')
        self.assertEqual((c, t), ('Károli-kereszthivatkozás', 'TSK- és Károli-kereszthivatkozás a Zsolt 99:6 helyről'))

    def test_gepi_strong_kereses(self):
        c, t = SZKZ.jeloles_oka('scan H7121')
        self.assertEqual((c, t), ('Gépi keresés', 'gépi Strong-keresés: H7121'))

    def test_be_nem_sorolhato_egyeb(self):
        c, t = SZKZ.jeloles_oka('valami más')
        self.assertEqual((c, t), ('Egyéb', 'valami más'))


class TestElutasitasOka(unittest.TestCase):
    def test_mintaszotar_sorrend_es_egyeb(self):
        minta = SZKZ.okok('ISTENTISZT-001')
        self.assertTrue(minta)
        self.assertEqual(SZKZ.elutasitas_oka('passzív szerkezet, K1_passziv', minta),
                         'passzív szerkezet vagy megnevezés (negatív kritérium)')
        self.assertEqual(SZKZ.elutasitas_oka('semmi ilyen', minta), SZKZ.EGYEB_OK)
        # ELLENOR_ISTENTISZT_OLVASOI 1.: a jogi fellebbezés a negatív kritérium „passzív/megnevezés jellegű vagy jogi
        # használat” szövege előtt illeszkedik
        self.assertEqual(SZKZ.elutasitas_oka('K3_jogi: fellebbez; negatív kritérium: passzív/megnevezés jellegű vagy '
                                             'jogi használat', minta), 'jogi fellebbezés')

    def test_nevelo(self):
        self.assertEqual(SZKZ.nevelo('1Krón 16:8'), 'az')
        self.assertEqual(SZKZ.nevelo('Zsolt 99:6'), 'a')
        self.assertEqual(SZKZ.nevelo('Ézs 12:4'), 'az')


class TestBlokkTorzs(unittest.TestCase):
    def test_csoport_labjegyzet_osszesito(self):
        sorok = [
            {'igehely': 'Zsolt 99:6', 'forras_kereses': 'TSK/Károli-KH Zsolt 99:6', 'dontes': 'elutasítva',
             'indoklas': 'semmi ilyen | scope=manual'},
            {'igehely': '1Móz 4:26', 'forras_kereses': 'scan H7121', 'dontes': 'nyitva', 'indoklas': 'kérdés'},
        ]
        tablak, labj, ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        self.assertEqual(len(labj), 2)
        self.assertIn('[^k1]', ''.join(tablak))
        self.assertEqual(ossz['egyeb'], ['Zsolt 99:6'])
        self.assertEqual(ossz['ok'], collections.Counter({SZKZ.EGYEB_OK: 1, 'nyitott döntés': 1}))
        sor = SZKZ.osszesito_sor(ossz)
        self.assertIn('egyéb 1 (Zsolt 99:6)', sor)
        self.assertIn('**Nyitott döntés:** 1', sor)
        self.assertIn('scope=manual', labj[0])


class TestKozosProveniencia(unittest.TestCase):
    """F152 B.2: a blokkban ismétlődő proveniencia-sor egyszer áll, jellel; nem vész el."""
    P = 'scope=manual | forras=napló.md | ts=2026-10-11'

    def test_minden_sor(self):
        uj, megj = SZKZ.kozos_proveniencia(['forrás: `A | %s`' % self.P, 'forrás: `B | %s`' % self.P], 'K')
        self.assertEqual(uj, ['forrás: `A | ‹K1›`', 'forrás: `B | ‹K1›`'])
        self.assertEqual(megj, '*Minden sor forrásmegjelölése (‹K1›): `%s`*' % self.P)

    def test_reszleges_es_egyedi(self):
        q = 'scope=x | forras=y.md | ts=2026-09-05'
        uj, megj = SZKZ.kozos_proveniencia(['A \\| %s' % self.P.replace('|', '\\|'), 'B | %s' % self.P,
                                            'C | %s' % q, 'D'], 'M')
        self.assertEqual(uj, ['A \\| ‹M1›', 'B | ‹M1›', 'C | %s' % q, 'D'])   # az egyszer álló a helyén marad
        self.assertIn('‹M1› = `%s` (2 sor)' % self.P, megj)
        self.assertNotIn(q, megj)

    def test_nincs_ismetles(self):
        s = ['A | %s' % self.P, 'B']
        self.assertEqual(SZKZ.kozos_proveniencia(s, 'E'), (s, ''))

    def test_lekerdezes_mezoi(self):
        # a lekerdez.py hat mezős sora (strong=, n=, ts=, csatorna=) is egy proveniencia (ELLENOR_F152, B.2)
        p = 'scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G1941 | n=31 | ts=2026-10-17T16:58Z | csatorna=cli'
        uj, megj = SZKZ.kozos_proveniencia(['a · %s' % p, 'b · %s' % p], 'K')
        self.assertEqual(uj, ['a · ‹K1›', 'b · ‹K1›'])
        self.assertIn(p, megj)


class TestOsszevon(unittest.TestCase):
    """F152 B.3: az egymást követő, azonos indoklású versek egy sorban, tartományként."""

    def test_tartomany(self):
        t = ('Károli-kereszthivatkozás', '**elutasítva** — névadás: x', 'forrás: `K`')
        sorok = [('1Móz 25:%d' % v,) + t for v in (21, 22, 23)] + [('1Móz 25:25',) + t, ('1Móz 26:1',) + t]
        ki = SZKZ.osszevon(sorok)
        self.assertEqual([k[0] for k in ki], ['1Móz 25:21–23', '1Móz 25:25', '1Móz 26:1'])
        self.assertEqual(ki[0][1:], t)

    def test_elteres_nem_von_ossze(self):
        a = ('1Móz 25:21', 'K', 'x', 'f1')
        b = ('1Móz 25:22', 'K', 'x', 'f2')   # más lábjegyzet
        self.assertEqual(SZKZ.osszevon([a, b]), [a, b])

    def test_blokk_torzs_osszevon(self):
        sor = {'forras_kereses': 'Károli-KH ApCsel 2:21', 'dontes': 'elutasítva', 'indoklas': 'névadás, NEM releváns'}
        sorok = [dict(sor, igehely='1Móz 25:%d' % v) for v in range(21, 27)]
        tablak, labj, _ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        self.assertEqual(len(labj), 1)
        self.assertIn('| 1Móz 25:21–26 |', tablak[1])
        self.assertIn('(6)', tablak[0])


if __name__ == '__main__':
    unittest.main()
