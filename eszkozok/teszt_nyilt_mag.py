#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A nyilt_mag_export.py és a nyilt_mag_kapu.py tesztjei (F162).

Pozitív: a teljes magon generált csomag 0 BUKÁS-t ad, és az export determinisztikus. Negatív: a belső jel, az
angol maradék, a hiányzó kódkönyv-sor, a kizárt licencű forrás, a hiányzó „ismert hibák” szám és a megváltoztatott
fájl mind BUKÁS-t ad. Egységtesztek a leképezésekre.

Használat: python eszkozok/teszt_nyilt_mag.py
"""
import copy
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nyilt_mag_export as E  # noqa: E402
import nyilt_mag_kapu as G  # noqa: E402


def bukasok(fajlok, azon=None):
    t = G.mer(fajlok, ujra=False)
    return [x for x in t if x.suly == G.BUKAS and (azon is None or x.azon == azon)]


class Alap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fajlok, cls.info = E.export('nyilt_mag')

    def uj(self):
        return copy.deepcopy(self.fajlok)

    def sor_csere(self, fajlok, rel, ertek, ujra, n=0):
        """Az `ertek` első előfordulását cseréli a megadott fájlban (az adatsorokban)."""
        sz = fajlok[rel]
        self.assertIn(ertek, sz)
        fajlok[rel] = sz.replace(ertek, ujra, 1)
        return fajlok


class Pozitiv(Alap):
    def test_teljes_mag_0_bukas(self):
        self.assertEqual([], [(x.azon, x.fajl, x.uzenet) for x in bukasok(self.fajlok)])

    def test_export_bajtazonos(self):
        masik, _ = E.export('nyilt_mag')
        self.assertEqual(self.fajlok, masik)

    def test_kotelezo_fajlok(self):
        for rel in G.KOTELEZO:
            self.assertIn(rel, self.fajlok)

    def test_nincs_nyitva_sor_es_nincs_feloldatlan_dt(self):
        self.assertEqual([], self.info['feloldatlan_dt'])
        self.assertEqual(self.info['stat']['kizarasok.tsv'] + self.info['stat']['beepitesi_dontesek.tsv'] + 0,
                         self.info['stat']['kizarasok.tsv'] + self.info['stat']['beepitesi_dontesek.tsv'])

    def test_ismert_hibak_mert_szam(self):
        h = self.fajlok['ISMERT_HIBAK.md']
        self.assertIn('Károli', h)
        self.assertIn(str(E.kh_meres()['gyanus']), h)

    def test_csoportos_kizaras_versszam_egyezik_a_tagokkal(self):
        _, kiz = G.tsv_sorok(self.fajlok['kizarasok.tsv'])
        _, tagok = G.tsv_sorok(self.fajlok['kizaras_csoportok.tsv'])
        db = {}
        for _, d in tagok:
            k = (d['motivum_azonosito'], d['csoport_sor_igehely'])
            db[k] = db.get(k, 0) + 1
        csoportos = [(d['motivum_azonosito'], d['igehely'], int(d['csoport_versszam'])) for _, d in kiz
                     if d['csoport_versszam']]
        self.assertTrue(csoportos)
        self.assertIn('ISTENTISZT-001', {c[0] for c in csoportos})
        for mid, ig, n in csoportos:
            self.assertEqual(n, db.get((mid, ig), 0), (mid, ig))

    def test_antrop_osztaly_jeloles_es_kulon_sor(self):
        # az ANTROP-001 `(osztaly=…)` jelölése is tag-listát ad; a héber pár 60 verséből a két „külön sor”
        # (Jób 12:10, Jón 4:8) saját kizárás-sor, nem csoport-tag: 58
        _, tagok = G.tsv_sorok(self.fajlok['kizaras_csoportok.tsv'])
        heber_par = {d['igehely'] for _, d in tagok
                     if (d['motivum_azonosito'], d['csoport_sor_igehely']) == ('ANTROP-001', '1Kir 1:29')}
        self.assertEqual(58, len(heber_par))
        self.assertIn('1Kir 1:29', heber_par)
        self.assertNotIn('Jób 12:10', heber_par)
        self.assertNotIn('Jón 4:8', heber_par)
        self.assertEqual([], E.CSOPORT_ELTERES)

    def test_kizart_forras_listaja_kimondva(self):
        for ds in ('MCGED', 'KJV_Strongs_teljes', 'Heber_ETCBC_modulok'):
            self.assertIn(ds, self.info['kizartak'])
            self.assertIn(ds, self.fajlok['OLVASSEL.md'])

    def test_sdbh_csak_a_kulon_retegben(self):
        for rel, sz in self.fajlok.items():
            if rel.startswith('cc_by_sa_reteg/') or rel in G.KIZART_NEV_KIVETEL or rel == 'kodkonyv.tsv':
                continue
            self.assertNotIn('SDBH', sz, rel)
            self.assertNotIn('SDGNT', sz, rel)
        self.assertIn('szemantikai_domenek.tsv', ' '.join(self.fajlok))

    def test_licenc_allapotok(self):
        lic = E.Licenc()
        self.assertEqual('kizart', lic.allapot('MCGED')[0])
        self.assertEqual('kizart', lic.allapot('Heber_ETCBC_modulok')[0])
        self.assertEqual('kizart', lic.allapot('KJV_Strongs_teljes')[0])
        self.assertEqual('sa_reteg', lic.allapot('SDBH')[0])
        self.assertEqual('engedett', lic.allapot('TAHOT')[0])
        self.assertEqual('kizart', lic.allapot('nincs_ilyen_dataset')[0])


class Egyseg(unittest.TestCase):
    def test_horgony(self):
        self.assertEqual(('szóbázis', 'H7585'), E.horgony('H7585'))
        self.assertEqual(('közös szóbázis', 'H7121 + H8034'), E.horgony('H7121+H8034'))
        self.assertEqual(('kollokáció (szópár egy versben)', 'málé + chámász'), E.horgony('málé+chámász'))
        self.assertEqual(('tematikus kapcsolat', '1Móz 3:17'), E.horgony('tematikus:1Móz 3:17'))
        self.assertEqual('LXX-híd', E.horgony('LXX:ᾅδης←H7585')[0])

    def test_prov_parse_es_manual(self):
        p = E.prov_parse('scope=manual | forras=Rafaim_tematikus.md | ts=2026-09-08')
        self.assertEqual({'scope': 'manual', 'forras': 'Rafaim_tematikus.md', 'ts': '2026-09-08'}, p)
        self.assertEqual('kézi döntés, lekérdezés nélkül', E.scope_ford(p['scope']))
        self.assertEqual('teljes ószövetségi szöveg (TAHOT)', E.scope_ford('TAHOT-teljes'))

    def test_forras_fordit(self):
        lic = E.Licenc()
        nev, dsek, kiz = E.forras_fordit('Rafaim_tematikus.md', lic)
        self.assertEqual('a motívum kézi tematikus tanulmánya', nev)
        nev, dsek, kiz = E.forras_fordit('TAHOT_kivonat.tsv+TAGNT_kivonat.tsv', lic)
        self.assertEqual(['TAGNT', 'TAHOT'], dsek)
        self.assertNotIn('.tsv', nev)

    def test_tisztit_belso_jelek(self):
        dn = E.Dontesnaplo({'DT476': {'kerdes': '', 'dontes': ''}})
        dn.gyujt('(DT476 K2)')
        dn.kioszt()
        t = E.tisztit('a név nélküli sorok kikerülnek (DT476 K2), `adat/jeloltek.tsv`, a gerinc egy eleme, manual, '
                      'a H0779-scan szerint, Isa.34.11', dn)
        self.assertIn('NYD-001', t)
        for tilos in ('DT476', 'jeloltek', 'gerinc', 'manual', 'scan', 'Isa.', '.tsv'):
            self.assertNotIn(tilos, t)
        self.assertIn('Ézs 34:11', t)

    def test_egy_mondat_vagas(self):
        hosszu = ('Első mondat, elég hosszú ahhoz, hogy vágni kelljen, mert sok szó áll benne. ' * 8).strip()
        r = E.egy_mondat(hosszu, 200)
        self.assertLessEqual(len(r), 205)


class Negativ(Alap):
    def test_belso_dt(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', 'a koporsóba', 'a koporsóba (DT476)')
        self.assertTrue(bukasok(f, 'BELSO'))

    def test_belso_gerinc_elem_es_scope(self):
        f = self.uj()
        f['kizarasok.tsv'] += 'ALVIL-001\t1Móz 1:1\telofordulas\t\t\tok\tgerinc_elem H7585 scope=manual\t\t\t\t\t\t\t\n'
        t = bukasok(f, 'BELSO')
        self.assertTrue(any('gerinc_elem' in x.uzenet or 'scope=' in x.uzenet for x in t))

    def test_belso_fajlnev(self):
        f = self.sor_csere(self.uj(), 'motivumok.tsv', 'Hádész (Seol)', 'Hádész (Seol) naplok/valami.md')
        self.assertTrue(bukasok(f, 'BELSO'))

    def test_angol_marado(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', 'a koporsóba', 'a study koporsóba')
        self.assertTrue(bukasok(f, 'ANGOL'))

    def test_kodkonyv_hianyzo_oszlop(self):
        f = self.uj()
        f['kodkonyv.tsv'] = '\n'.join(s for s in f['kodkonyv.tsv'].split('\n')
                                      if not s.startswith('motivumok.tsv\tcim\t'))
        self.assertTrue(bukasok(f, 'KODKONYV'))

    def test_kodkonyv_hianyzo_ertek(self):
        f = self.uj()
        f['kodkonyv.tsv'] = '\n'.join(s for s in f['kodkonyv.tsv'].split('\n')
                                      if not s.startswith('elofordulasok.tsv\tmegbizhatosag\tmagas\t'))
        self.assertTrue(bukasok(f, 'KODKONYV'))

    def test_kodkonyv_egynyelvu(self):
        f = self.uj()
        sorok = f['kodkonyv.tsv'].split('\n')
        for i, s in enumerate(sorok):
            if s.startswith('motivumok.tsv\tcim\t'):
                m = s.split('\t')
                m[4] = m[3]
                sorok[i] = '\t'.join(m)
        f['kodkonyv.tsv'] = '\n'.join(sorok)
        self.assertTrue(bukasok(f, 'KODKONYV'))

    def test_kizart_licenc(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', 'a koporsóba', 'a koporsóba (MCGED szerint)')
        self.assertTrue(bukasok(f, 'LICENC'))
        g = self.sor_csere(self.uj(), 'elofordulasok.tsv', 'a koporsóba', 'a koporsóba (Heber_ETCBC_modulok)')
        self.assertTrue(bukasok(g, 'LICENC'))

    def test_sdbh_a_reteg_kivul(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', 'a koporsóba', 'a koporsóba (SDBH domén)')
        self.assertTrue(bukasok(f, 'LICENC'))

    def test_reteg_attribucio_nelkul(self):
        f = self.uj()
        f['cc_by_sa_reteg/OLVASSEL.md'] = '# réteg\n'
        self.assertTrue(bukasok(f, 'RETEG'))

    def test_hianyzo_ismert_hibak(self):
        f = self.uj()
        f['ISMERT_HIBAK.md'] = '# Ismert hibák\n\nnincs\n'
        self.assertTrue(bukasok(f, 'HIBAK'))

    def test_hibas_mert_szam(self):
        f = self.uj()
        gy = str(E.kh_meres()['gyanus'])
        f['ISMERT_HIBAK.md'] = f['ISMERT_HIBAK.md'].replace(gy, '0')
        self.assertTrue(bukasok(f, 'HIBAK'))

    def test_feloldatlan_dontes(self):
        f = self.uj()
        f['kizarasok.tsv'] += 'ALVIL-001\t1Móz 1:1\telofordulas\t\t\tok\tindok NYD-999\t\t\t\t\t\t\t\n'
        self.assertTrue(bukasok(f, 'HIVATKOZAS'))

    def test_ismeretlen_motivum(self):
        f = self.sor_csere(self.uj(), 'kapcsolatok.tsv', 'KIRALY-001', 'ISMERETLEN-001')
        self.assertTrue(bukasok(f, 'HIVATKOZAS'))

    def test_csoport_tag_nelkul(self):
        f = self.uj()
        f['kizaras_csoportok.tsv'] = '\n'.join(s for s in f['kizaras_csoportok.tsv'].split('\n')
                                                if not s.startswith('ANTROP-001\t1Kir 1:29\t'))
        t = bukasok(f, 'CSOPORT')
        self.assertTrue(any('ANTROP-001 1Kir 1:29' in x.idezet for x in t))

    def test_csoport_tagszam_elter(self):
        f = self.uj()
        f['kizaras_csoportok.tsv'] += 'ANTROP-001\t1Kir 1:29\t1Móz 1:1\n'
        self.assertTrue(bukasok(f, 'CSOPORT'))

    def test_csoport_tag_arva(self):
        f = self.uj()
        f['kizaras_csoportok.tsv'] += 'ANTROP-001\t1Móz 1:1\t1Móz 1:1\n'
        self.assertTrue(any('nem létező' in x.uzenet for x in bukasok(f, 'CSOPORT')))

    def test_ellenorzo_osszeg(self):
        f = self.sor_csere(self.uj(), 'motivumok.tsv', 'Hádész (Seol)', 'Hádész (Seol)!')
        self.assertTrue(bukasok(f, 'BAJTAZONOS'))

    def test_ujragenerals_elteres(self):
        f = self.uj()
        f['OLVASSEL.md'] += 'kézi módosítás\n'
        t = G.ell_ujragenerals(f, 'nyilt_mag')
        self.assertTrue(any(x.fajl == 'OLVASSEL.md' for x in t))

    def test_github_url(self):
        f = self.uj()
        f['OLVASSEL.md'] += 'forrás: https://github.com/valaki/repo\n'
        self.assertTrue(bukasok(f, 'KANONIKUS'))

    def test_hianyzo_helyorzo(self):
        f = self.uj()
        f['OLVASSEL.md'] = f['OLVASSEL.md'].replace('<KANONIKUS_FORRAS_URL>', 'x')
        self.assertTrue(bukasok(f, 'KANONIKUS'))

    def test_termekreteg_kapcsolodas_oszlop(self):
        f = self.uj()
        sz = f['elofordulasok.tsv'].split('\n')
        sz[1] = sz[1].replace('funkcio', 'kapcsolodas\tfunkcio', 1)
        f['elofordulasok.tsv'] = '\n'.join(sz)
        self.assertTrue(bukasok(f, 'TERMEKRETEG'))

    def test_termekreteg_funkcio_magyarazat(self):
        f = self.uj()
        f['elofordulasok.tsv'] = f['elofordulasok.tsv'].replace('\tismétlődés\t', '\tismétlődés — magyarázat\t', 1)
        self.assertTrue(bukasok(f, 'TERMEKRETEG'))

    def test_funkcio_cimke(self):
        self.assertEqual(('alap-előfordulás', False), E.funkcio_cimke('🌱 alap-előfordulás — a motívum legelső megjelenése'))
        self.assertEqual(('ismétlődés', False), E.funkcio_cimke('🔁 ismétlődés'))
        self.assertEqual(('', True), E.funkcio_cimke('prototípus: ' + 'hosszú próza ' * 8))
        self.assertEqual(('', False), E.funkcio_cimke(''))

    def test_hianyzo_fajl(self):
        f = self.uj()
        del f['dontesnaplo.tsv']
        self.assertTrue(bukasok(f, 'BAJTAZONOS'))

    # --- F170.1: OSIS-kulcs (kapu (a))
    def test_osis_hibas_kulcs(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', '\t1Kgs.18.24\t', '\t1Kgs.18.25\t')
        self.assertTrue(bukasok(f, 'OSIS'))

    def test_osis_hianyzo_kulcs(self):
        f = self.sor_csere(self.uj(), 'kizarasok.tsv', '\t1Kgs.13.31\t', '\t\t')
        self.assertTrue(bukasok(f, 'OSIS'))

    def test_osis_ismeretlen_konyvkod(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', '\t1Kgs.18.24\t', '\t1Ki.18.24\t')
        self.assertTrue(bukasok(f, 'OSIS'))

    def test_osis_hianyzo_oszlop(self):
        f = self.uj()
        f['kapcsolatok.tsv'] = f['kapcsolatok.tsv'].replace('\tcel_igehely_osis', '\tcel_osis', 1)
        self.assertTrue(bukasok(f, 'OSIS'))


class Osis(unittest.TestCase):
    def test_lekepezes(self):
        self.assertEqual('1Kgs.13.31', E.osis('1Kir 13:31'))
        self.assertEqual('Gen.4.10-Gen.4.11', E.osis('1Móz 4:10-11'))
        self.assertEqual('Acts.2.27 Acts.2.31', E.osis('ApCsel 2:27; ApCsel 2:31'))
        self.assertEqual('Lam.3.58', E.osis('Sir 3:58'))
        self.assertEqual('Ps.16.10', E.osis('Zsolt 16:10'))
        self.assertEqual('', E.osis(''))

    def test_lekepezhetetlen_megall(self):
        with self.assertRaises(SystemExit):
            E.osis('1Énokh 1:9')
        with self.assertRaises(SystemExit):
            E.osis('1Móz 3')

    def test_66_konyv(self):
        self.assertEqual(66, len(E.hu_osis()))
        self.assertEqual(66, len(set(E.hu_osis().values())))


if __name__ == '__main__':
    unittest.main(verbosity=1)
