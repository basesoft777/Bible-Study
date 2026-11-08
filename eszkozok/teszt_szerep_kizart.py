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

    def test_be_nem_sorolhato_megall(self):
        # F123.EGYEB: „egyéb” csoport nincs; a be nem sorolható forrás megállítja a generálást
        with self.assertRaises(SZKZ.BeNemSorolhato):
            SZKZ.jeloles_oka('valami más')
        self.assertNotIn('Egyéb', SZKZ.CSOPORTOK)

    def test_teljesseg_meres_gepi(self):
        c, t = SZKZ.jeloles_oka('F123 U1 teljesség-mérés, blokk-kizárás (9_ v1, 2. szabály; DT503 mintája): 58 vers, '
                                'az első itt; a lista: naplok/x.tsv | scope=manual | forras=y | ts=2026-11-03')
        self.assertEqual((c, t), ('Gépi keresés', 'gépi teljesség-mérés; csoportos kizárás: 58 vers, az első itt'))
        c, t = SZKZ.jeloles_oka('F123 U1 teljesség-mérés, szótár (BDB H7585 sorszam 58; Thayer G0086 sorszam 2) és '
                                'LXX-többlet háló (naplok/x.md) | scope=manual')
        self.assertEqual(t, 'gépi teljesség-mérés (szótári háló, Septuaginta-többlet háló)')
        c, t = SZKZ.jeloles_oka('F123 U1 teljesség-mérés, Strong-háló, N-F63e-függő, blokk-sor (DT-F123o minta): 7 vers, '
                                'a sor igehelye a blokk egy verse | scope=manual')
        self.assertEqual(t, 'gépi teljesség-mérés (Strong-háló); csoportos kizárás: 7 vers, az első itt')

    def test_szopar_csalad_lanc_frazis(self):
        self.assertEqual(SZKZ.jeloles_oka('rokon (G4151|G4152) × (G5590|G5591) ±1 vers | scope=TAGNT-teljes'),
                         ('Gépi keresés', 'gépi szópár-keresés: G4151/G4152 + G5590/G5591 (±1 vers)'))
        self.assertEqual(SZKZ.jeloles_oka('csalad G1312 | scope=TAGNT-teljes')[1],
                         'gépi Strong-keresés a szócsaládban: G1312')
        self.assertEqual(SZKZ.jeloles_oka('lanc ±1 | scope=TAHOT-teljes')[0], 'Gépi keresés')
        self.assertEqual(SZKZ.jeloles_oka('pozíció-alapú frázis-keresés + BDB/TSK/LXX audit, retroaktív F3.1 '
                                          'betöltés')[0], 'Gépi keresés')

    def test_lekerdezes_provenienciaja_altalanos_szabaly(self):
        # ismeretlen alakú, de lekérdezés-proveniencia (nem `manual` scope): gépi keresés
        self.assertEqual(SZKZ.jeloles_oka('uj_kereses X | scope=TAHOT-teljes | forras=y | ts=z'),
                         ('Gépi keresés', 'gépi keresés'))
        with self.assertRaises(SZKZ.BeNemSorolhato):
            SZKZ.jeloles_oka('ismeretlen | scope=manual | forras=y | ts=z')


class TestElutasitasOka(unittest.TestCase):
    def test_mintaszotar_sorrend_es_egyeb(self):
        minta = SZKZ.okok('ISTENTISZT-001')
        self.assertTrue(minta)
        self.assertEqual(SZKZ.elutasitas_oka('passzív szerkezet, K1_passziv', minta),
                         'passzív szerkezet vagy megnevezés (negatív kritérium)')
        with self.assertRaises(SZKZ.BeNemSorolhato):
            SZKZ.elutasitas_oka('semmi ilyen', minta)
        # F123.EGYEB: a DT478 JHVH-elhatárolás saját kategóriát kap
        self.assertEqual(SZKZ.elutasitas_oka('DT478 (a felhasználó): a besém után nem a JHVH (H3068) szó áll', minta),
                         'nem JHVH áll a név után')
        # ELLENOR_ISTENTISZT_OLVASOI 1.: a jogi fellebbezés a negatív kritérium „passzív/megnevezés jellegű vagy jogi
        # használat” szövege előtt illeszkedik
        self.assertEqual(SZKZ.elutasitas_oka('K3_jogi: fellebbez; negatív kritérium: passzív/megnevezés jellegű vagy '
                                             'jogi használat', minta), 'jogi fellebbezés')

    def test_nevelo(self):
        self.assertEqual(SZKZ.nevelo('1Krón 16:8'), 'az')
        self.assertEqual(SZKZ.nevelo('Zsolt 99:6'), 'a')
        self.assertEqual(SZKZ.nevelo('Ézs 12:4'), 'az')


class TestBlokkTorzs(unittest.TestCase):
    def test_be_nem_sorolhato_sor_megallitja_a_blokkot(self):
        sorok = [{'igehely': 'Zsolt 99:6', 'forras_kereses': 'TSK/Károli-KH Zsolt 99:6', 'dontes': 'elutasítva',
                  'indoklas': 'semmi ilyen | scope=manual'},
                 {'igehely': 'Zsolt 1:1', 'forras_kereses': 'valami más', 'dontes': 'nyitva', 'indoklas': 'kérdés'}]
        self.assertEqual(SZKZ.hianyok(sorok, 'ISTENTISZT-001'),
                         [('Zsolt 99:6', 'elutasítási ok'), ('Zsolt 1:1', 'jelölési forrás')])
        with self.assertRaises(SZKZ.BeNemSorolhato):
            SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')

    def test_csoport_labjegyzet_osszesito(self):
        sorok = [
            {'igehely': 'Zsolt 99:6', 'forras_kereses': 'TSK/Károli-KH Zsolt 99:6', 'dontes': 'elutasítva',
             'indoklas': 'tartalmilag NEM releváns | scope=manual'},
            {'igehely': '1Móz 4:26', 'forras_kereses': 'scan H7121', 'dontes': 'nyitva', 'indoklas': 'kérdés'},
        ]
        tablak, labj, ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        self.assertEqual(len(labj), 2)
        self.assertIn('[^k1]', ''.join(tablak))
        self.assertEqual(ossz['ok'], collections.Counter({'tartalmilag nem kapcsolódik': 1, 'nyitott döntés': 1}))
        sor = SZKZ.osszesito_sor(ossz)
        self.assertIn('| tartalmilag nem kapcsolódik | 1 | a vers témája más | Zsolt 99:6 |', sor)
        self.assertEqual(SZKZ.olvasoi_ok('más szó áll a versben (összesítő sor)'), 'más szó áll a versben')
        self.assertNotIn('egyéb', sor)
        self.assertIn('**Nyitott döntés:** 1', sor)
        self.assertIn('scope=manual', labj[0])


class TestVersszam(unittest.TestCase):
    """F123.TUD1B: az összesítő sor versszáma a `forras_kereses`-ből, a mondat verseket számol."""
    CSOP = ('F123 U1 teljesség-mérés, Károli-szó háló, blokk-kizárás (DT564): 33 vers, az első itt; a lista: '
            'naplok/x.tsv | scope=manual | forras=y | ts=2026-11-02')

    def test_csoport_versszam(self):
        self.assertEqual(SZKZ.csoport_versszam(self.CSOP), 33)
        self.assertEqual(SZKZ.csoport_versszam('F123 U1 teljesség-mérés, Strong-háló, blokk-sor (DT564 minta): 573 '
                                               'vers, a sor igehelye a blokk egy verse | scope=manual'), 573)
        self.assertIsNone(SZKZ.csoport_versszam('scan H7121 | scope=x'))
        self.assertIsNone(SZKZ.csoport_versszam('scan | scope=x: 5 vers'))   # a proveniencia-farok nem számít

    def test_vizsgalt_versek(self):
        sorok = [
            {'igehely': '1Móz 1:2', 'forras_kereses': self.CSOP, 'dontes': 'elutasítva'},
            {'igehely': 'Luk 9:55-56', 'forras_kereses': 'scan', 'dontes': 'elutasítva'},
            {'igehely': 'Luk 9:55', 'forras_kereses': 'scan', 'dontes': 'elutasítva'},
            {'igehely': 'Zsolt 1:1', 'forras_kereses': 'scan', 'dontes': 'nyitva'},
        ]
        self.assertEqual(SZKZ.vizsgalt_versek(sorok), {'egyenkent': 3, 'csoport_vers': 33, 'csoport_sor': 1,
                                                       'osszes': 36, 'elutasitva': 35, 'nyitva': 1})

    def test_osszesito_sulyozott(self):
        sorok = [{'igehely': '1Móz 1:2', 'forras_kereses': self.CSOP, 'dontes': 'elutasítva',
                  'indoklas': 'Összesítő sor 33 versre (az első itt áll): tartalmilag NEM releváns'},
                 {'igehely': 'Zsolt 99:6', 'forras_kereses': 'scan H7121', 'dontes': 'elutasítva',
                  'indoklas': 'tartalmilag NEM releváns'}]
        tablak, _labj, ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        self.assertEqual(ossz['ok']['tartalmilag nem kapcsolódik'], 34)
        self.assertIn('**Gépi keresés** (2 sor, 34 vers)', tablak)

    def test_indok_strong(self):
        # F123.TUD1B (3): a latin betűs szó utáni zárójeles Strong-szám a #624 szerinti jelölt alakot kapja
        t = SZKZ.indok_strong('a besém után nem JHVH (H3068) áll', lambda s: s + ' · Úr')
        self.assertEqual(t, 'a besém után nem [JHVH](/szo/H3068)<sup class="strong" title="H3068 · Úr">H3068</sup> áll')
        self.assertEqual(SZKZ.indok_strong(t), t)                       # idempotens
        for valtozatlan in ('a Strong-szám (H7121)', 'láncban (H7121+H8034)', 'TAHOT: H9020 i',
                            'de ὄνομα (G3686) nélkül', 'אֶל (H0413) + יְהוָה'):   # a héber/görög szó a strong_ki-é
            self.assertEqual(SZKZ.indok_strong(valtozatlan), valtozatlan)
        import olvasoi_utofeldolg as OU
        self.assertEqual(OU.csupasz_strongok(t), [])

    def test_versszam_hibak(self):
        jo = {'id': 'X', 'igehely': '1Móz 1:2', 'forras_kereses': self.CSOP,
              'indoklas': 'Összesítő sor 33 versre (az első itt áll): …'}
        self.assertEqual(SZKZ.versszam_hibak([jo, {'id': 'X', 'igehely': 'Zsolt 1:1', 'forras_kereses': 'scan',
                                                   'indoklas': 'más'}]), [])
        nincs = dict(jo, forras_kereses='F123 U1 teljesség-mérés | scope=manual')
        elter = dict(jo, indoklas='Összesítő sor 34 versre: …')
        h = SZKZ.versszam_hibak([nincs, elter])
        self.assertEqual(len(h), 2)
        self.assertIn('nem hordoz versszámot', h[0][2])
        self.assertIn('a forrásban 33, az indoklásban 34', h[1][2])


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


class TestOlvasoiIndok(unittest.TestCase):
    """Az indoklás olvasói alakja: belső jelölés nem kerül a lapra (olvasói kapu, 2026-11-02)."""

    def test_dontes_azonosito_es_minosito_zarojel(self):
        t = ('DT478 (a felhasználó, 2026-11-01: „Csak ahol JHVH áll”): a besém után nem a JHVH (H3068) szó áll, '
             'hanem névmási rag')
        self.assertEqual(SZKZ.olvasoi_indok(t), 'a besém után nem a JHVH (H3068) szó áll, hanem névmási rag')

    def test_belso_zarojel_elmarad_az_ok_marad(self):
        t = 'Minősítési mérce (a #123 2e. 4. küszöbdöntése, 2026-10-28; orkesztrátor): a halálveszélyben lévő maga kiált'
        self.assertEqual(SZKZ.olvasoi_indok(t), 'Minősítési mérce: a halálveszélyben lévő maga kiált')

    def test_szuro_osztaly_kifejezes(self):
        t = 'F110 szűrő (DT283), A osztály, kézi olvasás: Károli: „Én pedig az Istent hívom” — eskü'
        self.assertEqual(SZKZ.olvasoi_indok(t), 'Károli: „Én pedig az Istent hívom” — eskü')

    def test_angol_cimke_es_kod(self):
        self.assertEqual(SZKZ.olvasoi_indok('K1_passziv: nevezett (was called); passzív'), 'nevezett; passzív')
        self.assertEqual(SZKZ.olvasoi_indok('nem a jelen scan tárgya — dokumentálva'),
                         'nem a jelen keresés tárgya — dokumentálva')
        self.assertEqual(SZKZ.olvasoi_indok('nélkül (`motivumok.tsv` `folerendelt_fogalom`) történik'), 'nélkül történik')

    def test_tiszta_szoveg_valtozatlan(self):
        t = 'a vers névadás („nevezék nevét Ézsaunak”), nem segítségül hívás'
        self.assertEqual(SZKZ.olvasoi_indok(t), t)

    def test_nem_menthet_none(self):
        self.assertIsNone(SZKZ.olvasoi_indok('DT283 N59'))

    def test_cella_proveniencia_farka_marad(self):
        c = SZKZ.indok_cella('DT476 K2 (a felhasználó): a név nélküli forma | scope=manual | forras=x | ts=2026-11-01')
        self.assertTrue(c.startswith('a név nélküli forma'))
        self.assertIn('scope=manual', c)
        self.assertNotIn('DT476', c)

    def test_blokk_torzs_nyers_indoklas_labjegyzetben(self):
        sorok = [{'igehely': 'Zak 13:9', 'dontes': 'elutasítva', 'forras_kereses': 'scan H7121',
                  'indoklas': 'DT478 (a felhasználó): nem a JHVH (H3068) szó áll, névmási rag áll | scope=manual | forras=x | ts=2026-11-01'}]
        ki, labj, _ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        tabla = chr(10).join(ki)
        self.assertNotIn('DT478', tabla)
        self.assertIn('névmási rag áll', tabla)
        self.assertIn('indoklás (nyers): DT478', labj[0])


if __name__ == '__main__':
    unittest.main()
