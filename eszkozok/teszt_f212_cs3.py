"""teszt_f212_cs3.py -- F212 (CS3 generátor-kör): az egyezés-kapu, a Kolofon forrásoszlop-kapuja, az ismétlő jegyzet
szűrése, a befagyasztott lapok jegyzéke és a műhelyszó-kapu új szavai.

Futtatás: python eszkozok/teszt_f212_cs3.py
"""
import os
import sys
import tempfile
import unittest

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)

import lap_befagyasztas as LB  # noqa: E402
import lexikon_general as LG  # noqa: E402
import olvasoi_kapu as K  # noqa: E402
import olvasoi_kovetkeztetes as OK  # noqa: E402
import tablajegyzet as TJ  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

OSSZESITES = ('*Összesítés: egyező=7, ugyanaz a szócsalád=6, eltérő=1, nincs újszövetségi pár=20, LXX-minusz=0, '
              'a megfelelő nincs megállapítva=11, versszámozás miatt nem párosítva=1.*')


class Egyezeskapu(unittest.TestCase):
    def lap(self, rovid='13/14', osszeg='A motívum ószövetségi helyei 46 versre terjednek.', nincs='20'):
        return '\n\n'.join([
            'A szóhíd két szón át vezet, és ott erős: szócsalád szerint %s vers.' % rovid,
            '%s A többi szónak a motívumban nincs újszövetségi párja (%s vers), ott egyezés nem várható.' % (osszeg, nincs),
            'A motívum görög szavai (x) az ószövetségi helyek 46 verséből 7 versben állnak a Septuaginta szövegében is; '
            'további 6 versben ugyanannak a szócsaládnak egy másik tagja áll.',
            'Az x a motívum 40 ószövetségi versében áll.', 'Az y a motívum 6 ószövetségi versében áll.', OSSZESITES])

    def test_egyezo_lap_atmegy(self):
        m = LG.lxx_egyezes_kapu(self.lap(), 'X-001')
        self.assertEqual((m['n'], m['egyezo'], m['szocsalad'], m['szavankent']), (46, 7, 6, 46))

    def test_eltero_arany_bukik(self):
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(rovid='10/11'), 'X-001')

    def test_eltero_osszeg_bukik(self):
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(osszeg='A motívum ószövetségi helyei 45 versre terjednek.'), 'X-001')

    def test_eltero_nincs_par_bukik(self):
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(nincs='23'), 'X-001')

    def test_hibas_osszesites_nem_enged_at(self):
        lap = '## 5. LXX-fordítói döntések\n\n*Összesítés: egyező=7, más címke=6.*'
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(lap, 'X-001')

    def test_hely_egyseg_kapu(self):
        att = '\n'.join([LG.ATTEKINTO_CIM, '', '| Szó (kiejtés) | Alapjelentés | LXX-megfelelő | Helyek a motívumban |',
                         '|---|---|---|---|', '| חָמָס (chámász) | erőszak | — | 12 |', ''])
        jo = ('<summary><strong>חָמָס (chámász) — erőszak</strong> — 2 hely</summary>\n'
              '<summary><strong>szópár: málé + chámász</strong> — 10 hely</summary>\n' + att)
        self.assertEqual(LG.hely_egyseg_kapu(jo, 'X-001'), 1)
        with self.assertRaises(ValueError):
            LG.hely_egyseg_kapu(jo.replace('— 10 hely', '— 9 hely'), 'X-001')

    def test_osszesites_nelkul_nem_mer(self):
        self.assertEqual(LG.lxx_egyezes_kapu('nincs LXX-szakasz', 'X-001'), {})

    def test_rovid_mondat_ugyanabbol(self):
        s = OK.lxx_hid_rovid(7, 6, 1, ['az árar', 'a sáchat'], '[5.](#5)')
        self.assertIn('szócsalád szerint 13/14 vers', s)
        self.assertIn('erős', s)


class KolofonKapu(unittest.TestCase):
    def test_nevelo_nelkul_atmegy(self):
        sorok = ['| Forrás | Licenc | Szakasz |', '|---|---|---|', '| BDB-szótár | közkincs | 4. |']
        self.assertEqual(LG.kolofon_forrasoszlop_kapu(sorok), sorok)

    def test_nevelovel_bukik(self):
        for rossz in ('| a BDB-szótár | közkincs | 4. |', '| Az ókori tanúk táblája | x | 9. |'):
            with self.assertRaises(ValueError):
                LG.kolofon_forrasoszlop_kapu(['| Forrás | Licenc | Szakasz |', '|---|---|---|', rossz])

    def test_bdb_egy_nev(self):
        self.assertEqual(LG.olvasoi_forrasnev('adat/bdb_vers_jelentes.tsv', nevelovel=False),
                         LG.olvasoi_forrasnev('adat/bdb_szakaszok.tsv', nevelovel=False))


class IsmetloJegyzet(unittest.TestCase):
    def test_ismetlo(self):
        sor = '| Jer 17:9 | TSK-ajánlás az 1Móz 6:5 helyről, 25 szavazat (a Károli is ajánlja) | x |'
        self.assertTrue(TJ.ismetlo_jegyzet('Forrás: TSK-ajánlás (1Móz 6:5); a Károli-kereszthivatkozás is.', sor))
        self.assertTrue(TJ.ismetlo_jegyzet('Forrás: csoportos kizárás, 573 vers.',
                                           '| 1Kir 1:52 | keresés; a csoportosan kizárt 573 vers közül az első | x |'))

    def test_tobbletet_hordozo_marad(self):
        sor = '| Jer 17:9 | TSK-ajánlás az 1Móz 6:5 helyről, 25 szavazat | x |'
        self.assertFalse(TJ.ismetlo_jegyzet('Forrás: TSK-ajánlás (1Móz 6:5); a Károli-kereszthivatkozás is.', sor))
        self.assertFalse(TJ.ismetlo_jegyzet('Forrás: a motívum korábbi kereszthivatkozás-naplója.', sor))


class Befagyasztas(unittest.TestCase):
    def test_tabla(self):
        with tempfile.TemporaryDirectory() as d:
            ut = os.path.join(d, 'lap_befagyasztas.tsv')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write('id\tok\tdontes\tdatum\nX-001\túj cikk\tx\t2026-11-12\n')
            self.assertEqual(LB.befagyasztott_idk(ut), {'X-001'})
            self.assertEqual(LB.befagyasztott_idk(os.path.join(d, 'nincs.tsv')), set())

    def test_hibas_fejlec(self):
        with tempfile.TemporaryDirectory() as d:
            ut = os.path.join(d, 'lap_befagyasztas.tsv')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write('id\tok\n')
            with self.assertRaises(ValueError):
                LB.sorok(ut)

    def test_a_repo_hetet_fagyaszt(self):
        # F194 (DT-F194j): az ISTENTISZT-001 a 2. kiadásig, az újraírt generátorig befagyasztva
        self.assertEqual(LB.befagyasztott_idk(), {'KIRALY-001', 'TEREMT-001', 'ALVIL-001', 'MENNY-001', 'ANTROP-001',
                                                  'HODIT-001', 'TEREMT-002', 'ISTENTISZT-001'})


class Munkaszo(unittest.TestCase):
    def test_uj_szavak(self):
        for szoveg in ('*Ez a blokk a motívum 47 igehely-sorát fedi.*', '- TSK: Mik 7:17 (Votes: 17)',
                       'gépi teljesség-mérés (Strong-háló)', '*Proveniencia (a tábla soraiból): x*',
                       'a motívum láncverseiben', '*ⓘ Kutatói megjegyzés: x.*'):
            self.assertTrue(any(rx.search(szoveg) for rx, _n in K.MUNKASZAVAK), szoveg)

    def test_olvasoi_alak_tiszta(self):
        for szoveg in ('*A táblázat a motívum 47 igehelyét sorolja fel.*', '- TSK: Mik 7:17 (17 szavazat)',
                       'a motívum szavainak teljes bibliai keresése (a héber vagy görög szó)'):
            self.assertFalse(any(rx.search(szoveg) for rx, _n in K.MUNKASZAVAK), szoveg)


class TeljessegKapu(unittest.TestCase):
    """F212: a teljesség-mérés forrássora nem a lap törzsében, a mérés Strong-halmaza a motívum mai halmaza."""

    def setUp(self):
        import general as G
        self.sorai = [r for r in G.tsv_beolvas(os.path.join(os.path.dirname(ESZKOZOK), 'adat', 'elofordulasok.tsv'))[1]
                      if r['id'] == 'HAMART-001']

    def test_a_repo_lapja_atmegy(self):
        lap = open(os.path.join(os.path.dirname(ESZKOZOK), 'lexikon', 'HAMART-001_TUDOMANYOS.md'), encoding='utf-8').read()
        self.assertTrue(LG.teljesseg_kapu(lap, 'HAMART-001', self.sorai))

    def test_forrassor_a_torzsben_bukik(self):
        with self.assertRaises(ValueError):
            LG.teljesseg_kapu('x<!-- scope=TAHOT-teljes+TAGNT-teljes | n=1 -->', 'HAMART-001', self.sorai)

    def test_elavult_halmaz_bukik(self):
        with self.assertRaises(ValueError):
            LG.teljesseg_kapu('', 'HAMART-001', self.sorai[:1])


class KaroliKhHozzaferes(unittest.TestCase):
    """F212 (a Károli-KH döntés): a nyers Károli-KH tábla egyetlen hozzáférési pontja (E40) és a lap Károli-KH sorai."""

    def futtat(self, fajlok):
        sys.path.insert(0, os.path.join(ESZKOZOK, 'ellenorzes'))
        import szabalyok as S
        with tempfile.TemporaryDirectory() as d:
            for rel, tartalom in fajlok.items():
                ut = os.path.join(d, *rel.split('/'))
                os.makedirs(os.path.dirname(ut), exist_ok=True)
                with open(ut, 'w', encoding='utf-8') as f:
                    f.write(tartalom)
            return S.e40_karoli_kh_hozzaferes(root=d)

    def test_nyers_megnyitas_hiba(self):
        t = self.futtat({'eszkozok/uj_fogyaszto.py': "x = open('konkordancia/Karoli_kereszthivatkozasok.tsv')\n"})
        self.assertEqual(len(t), 1)

    def test_engedelyezett_es_proveniencia_nem_hiba(self):
        t = self.futtat({'eszkozok/karoli_kh_szuro.py': "open('konkordancia/Karoli_kereszthivatkozasok.tsv')\n",
                         'eszkozok/lap.py': "F = ['konkordancia/Karoli_kereszthivatkozasok.tsv']  # forrásnév\n",
                         'eszkozok/olvaso_pilot/a.py': "open('konkordancia/Karoli_kereszthivatkozasok.tsv')\n"})
        self.assertEqual(t, [])

    def test_a_lap_kh_sorai_megerositettek(self):
        import karoli_kh_szuro as KHS
        idx = LG.kh_index()
        for forras, sorok in idx.items():
            for r in sorok:
                self.assertTrue(KHS.elfogad(forras, r['Kapcsolódó igehely']), (forras, r['Kapcsolódó igehely']))


if __name__ == '__main__':
    unittest.main()
