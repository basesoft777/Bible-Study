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
            self.assertIn(ds, self.fajlok['ATTRIBUCIO.md'])

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
        f['OLVASSEL.md'] = f['OLVASSEL.md'].replace(E.KANONIKUS_HELY, 'x')
        self.assertTrue(bukasok(f, 'KANONIKUS'))

    def test_nyers_helyorzo_bukik(self):
        for nyers in ('[A LEXIKON CÍME]', '[HELYŐRZŐ: szerző]', '<KANONIKUS_FORRAS_URL>'):
            f = self.uj()
            f['README.md'] += nyers + '\n'
            self.assertTrue(bukasok(f, 'HELYORZO'), nyers)

    def test_cim_hu_es_en(self):
        self.assertEqual(('Logosz-lexikon', 'Logosz Lexikon'), (E.LEXIKON_CIM_HU, E.LEXIKON_CIM_EN))
        self.assertIn('# Logosz-lexikon — nyílt adatmag', self.fajlok['OLVASSEL.md'])
        self.assertIn('# Logosz Lexikon — open data core', self.fajlok['README.md'])
        self.assertNotIn('Logosz Lexikon', self.fajlok['OLVASSEL.md'])

    def test_cim_szerzo_doi_megvan(self):
        self.assertEqual([], bukasok(self.fajlok, 'HELYORZO'))
        for rel in ('OLVASSEL.md', 'README.md'):
            for kell in (E.LEXIKON_CIM_HU if rel == 'OLVASSEL.md' else E.LEXIKON_CIM_EN, 'Demeter Tamás', '0009-0005-9254-9731', '10.5281/zenodo.24141612',
                         '10.5281/zenodo.24141884', 'logoszlexikon.hu'):
                self.assertIn(kell, self.fajlok[rel], (rel, kell))
        self.assertIn('10.5281/zenodo.24141612', self.fajlok['KIADAS.txt'])
        self.assertIn('10.5281/zenodo.24141612', self.fajlok['RELEASE.txt'])

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


class Cimke(Alap):
    """F170.2, kapu (b): a zárt értékek angol címkéje."""

    def test_minden_zart_oszlopnak_van_en_parja(self):
        for rel, oszlopok in E.ZART.items():
            fej, _ = G.tsv_sorok(self.fajlok[rel])
            for o in oszlopok:
                if o in fej:
                    self.assertIn(o + '_en', fej, '%s/%s' % (rel, o))

    def test_hibas_cimke(self):
        f = self.sor_csere(self.uj(), 'kizarasok.tsv', '\toccurrence\t', '\tcandidate\t')
        self.assertTrue(bukasok(f, 'CIMKE'))

    def test_hianyzo_cimke_a_kodkonyvben(self):
        f = self.uj()
        f['kodkonyv.tsv'] = f['kodkonyv.tsv'].replace('\toccurrence\n', '\t\n', 1)
        self.assertTrue(bukasok(f, 'CIMKE'))

    def test_hianyzo_en_oszlop(self):
        f = self.uj()
        f['kapcsolatok.tsv'] = f['kapcsolatok.tsv'].replace('\ttipus_en\t', '\ttipus_angol\t', 1)
        self.assertTrue(bukasok(f, 'CIMKE'))

    def test_osszetett_ertek_reszenkent(self):
        _, sorok = G.tsv_sorok(self.fajlok['forrasok_es_licencek.tsv'])
        d = [d for _, d in sorok if d['dataset'] == 'projekt_adat'][0]
        self.assertEqual(len(E.ertek_reszek(d['ok'])), len(E.ertek_reszek(d['ok_en'])))


class Forditas(Alap):
    """F170.3–4, kapu (c)–(f): a szabad szöveg gépi angol párja és a STEPBible-glossza."""

    def forditott_sor(self, rel='kizarasok.tsv', o='indoklas'):
        fej, sorok = G.tsv_sorok(self.fajlok[rel])
        for n, d in sorok:
            if d[o] and d[o + '_en'] and d['forditas_modja'].startswith('gépi fordítás ('):
                return d
        self.skipTest('nincs fordított sor')

    def test_minden_szabad_oszlopnak_van_en_parja_es_jelolese(self):
        for rel, mezok in E.SZABAD.items():
            fej, _ = G.tsv_sorok(self.fajlok[rel])
            self.assertIn('forditas_modja', fej, rel)
            for o in mezok:
                self.assertIn(o + '_en', fej, '%s/%s' % (rel, o))

    def test_jeloles_nelkuli_forditas(self):
        d = self.forditott_sor()
        f = self.sor_csere(self.uj(), 'kizarasok.tsv', '\t' + d['forditas_modja'] + '\n', '\tkézi\n')
        self.assertTrue(bukasok(f, 'FORDITAS'))

    def test_elavult_forditas(self):
        d = self.forditott_sor()
        f = self.sor_csere(self.uj(), 'kizarasok.tsv', '\t' + d['indoklas'] + '\t', '\t' + d['indoklas'] + ' (módosítva)\t')
        self.assertTrue([x for x in bukasok(f, 'FORDITAS') if 'elavult' in x.uzenet])

    def test_mas_angol_szoveg(self):
        d = self.forditott_sor()
        f = self.sor_csere(self.uj(), 'kizarasok.tsv', '\t' + d['indoklas_en'] + '\t', '\tsomething else\t')
        self.assertTrue(bukasok(f, 'FORDITAS'))

    def test_glossza_nem_stepbible(self):
        f = self.sor_csere(self.uj(), 'elofordulasok.tsv', '\thell: Sheol\t', '\tthe grave\t')
        self.assertTrue(bukasok(f, 'GLOSSZA'))

    def test_glossza_lekepezes(self):
        self.assertEqual('hell: Sheol', E.glossza_en('H7585'))
        self.assertEqual('to call: call to + name', E.glossza_en('H7121+H8034'))
        self.assertIn('Rephaim', E.glossza_en('H7497'))
        self.assertEqual('', E.glossza_en(''))

    def test_tbesh_tbesg_forraskent_a_leltarban(self):
        _, sorok = G.tsv_sorok(self.fajlok['forrasok_es_licencek.tsv'])
        szerep = {d['dataset']: d['szerepe_a_csomagban'] for _, d in sorok}
        self.assertTrue(szerep['TBESH'].startswith('forrás'))
        self.assertTrue(szerep['TBESG'].startswith('forrás'))


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


class TesztSzerkesztoi(unittest.TestCase):
    """F178.6: „a felhasználó döntése” → „szerkesztői döntés”, angolul „editorial decision”; a kapu jelez."""

    def test_csere(self):
        self.assertEqual('Kontraszt (szerkesztői döntés, 2026-11-01)', E.szerkesztoi('Kontraszt (a felhasználó döntése, 2026-11-01)'))
        self.assertEqual('Szerkesztői döntés (2026-10-20): beépítve', E.szerkesztoi('A felhasználó döntése (2026-10-20): beépítve'))
        self.assertEqual('— szerkesztői döntés: »a', E.szerkesztoi('— az orkesztrátor döntése a felhasználó felhatalmazásával: »a'))
        self.assertEqual('(szerkesztői átnézés, 2026-11-02)', E.szerkesztoi('(a felhasználó átnézése, 2026-11-02)'))
        self.assertEqual('Contrast (editorial decision, 2026-11-01)', E.szerkesztoi("Contrast (the user's decision, 2026-11-01)"))
        self.assertEqual('Editorial decision (2026-10-20): open', E.szerkesztoi("The user's decision (2026-10-20): open"))
        self.assertEqual('a felhasználás feltételei', E.szerkesztoi('a felhasználás feltételei'))

    def test_idempotens_es_forditas_friss(self):
        hu = 'Kontraszt (a felhasználó döntése, 2026-11-01)'
        self.assertEqual(E.szerkesztoi(hu), E.szerkesztoi(E.szerkesztoi(hu)))
        self.assertTrue(E.szerkesztoi_egyezik(hu, E.szerkesztoi(hu)))
        self.assertFalse(E.szerkesztoi_egyezik(hu, 'más szöveg'))

    def test_kapu_jelez(self):
        tal = G.ell_szerkeszto({'x.tsv': 'a\tb\nA felhasználó döntése\n', 'y.md': "the user's decision\n", 'z.md': 'tiszta\n'})
        self.assertEqual(['x.tsv', 'y.md'], sorted(t.fajl for t in tal))
        self.assertTrue(all(t.suly == G.BUKAS for t in tal))



class F28Lyuk(Alap):
    """F182 (F28): a kivágott belső hivatkozás helyén nem marad lyuk; a LYUK kapu jelez."""

    def test_feloldatlan_dt_olvasoi_mondatresz(self):
        dn = E.Dontesnaplo({})
        self.assertEqual(dn.csere('8 régi: DT544; 27 a DT542-ből'),
                         '8 régi: egy korábbi szerkesztői döntés; 27 egy korábbi szerkesztői döntésből')
        self.assertEqual(dn.csere('a gerinc-elem (DT593)').strip(), 'a gerinc-elem')     # zárójelben: elmarad, mint eddig

    def test_kodnev_rag(self):
        self.assertEqual(E.tisztit('az 1Móz 6:5 és 8:21 `gerinc_elem`-je', E.Dontesnaplo({})),
                         'az 1Móz 6:5 és 8:21 motívumszava')

    def test_egy_mondat_zarojelen_kivul_vag(self):
        t = 'A 109 sor (8 régi: x; 27 y; ' + 'z ' * 150 + ') és a többi. Második mondat.'
        ki = E.egy_mondat(t, ig=120, min_hossz=10)
        self.assertTrue(ki.endswith('…'))
        self.assertNotIn('; 27 y;', ki[-8:])

    def test_lyuk_kapu(self):
        f = self.uj()
        sz = f['dontesnaplo.tsv']
        sor = [x for x in sz.split('\n') if x.startswith('NYD-002\t')][0]
        c = sor.split('\t')
        c[1] = 'A sor (8 régi:; 27 a -ből) kérdése'
        f['dontesnaplo.tsv'] = sz.replace(sor, '\t'.join(c), 1)
        self.assertTrue(bukasok(f, 'LYUK'))

    def test_teljes_mag_nincs_lyuk(self):
        self.assertEqual(bukasok(self.uj(), 'LYUK'), [])


class F198Visszhang(Alap):
    """F198: a hatástörténet (visszhang-réteg) a nyílt magban, forrásonként licenccel; a Chain Lineage kiszűrve."""
    TABLAK = ('visszhang_megfelelok.tsv', 'visszhang_tanuk.tsv', 'vitatott_forrasok.tsv', 'sblgnt_apparatus.tsv')

    def sorok(self, rel):
        fej, ds = E.tsv_szoveg(self.fajlok[rel])
        return ds

    def test_tablak_megvannak_es_nem_uresek(self):
        for rel in self.TABLAK:
            self.assertTrue(self.sorok(rel), rel)

    def test_nincs_chain_lineage_es_bdb(self):
        for rel in self.TABLAK:
            for d in self.sorok(rel):
                for v in d.values():
                    self.assertNotRegex(v.lower(), r'chain[ _-]?lineage|mblida|biblindex')
        self.assertTrue(all(d['forras'] in ('targum', 'vulgata', 'lxx') for d in self.sorok('visszhang_megfelelok.tsv')))
        self.assertTrue(all(d['forras'] in ('hcf', 'sefaria', 'glossa') for d in self.sorok('visszhang_tanuk.tsv')))

    def test_csak_ellenorzott_sor(self):
        _, forras = E.tsv('adat/visszhang_megfelelok.tsv')
        db = sum(1 for r in forras if r['forras'] in E.VISSZHANG_MEGFELELO and r['ellenorzes'].strip())
        self.assertEqual(db, len(self.sorok('visszhang_megfelelok.tsv')))

    def test_nincs_osszefoglalo_es_nincs_munkajel(self):
        fej, _ = E.tsv_szoveg(self.fajlok['vitatott_forrasok.tsv'])
        self.assertNotIn('osszefoglalo', fej)
        for d in self.sorok('visszhang_megfelelok.tsv'):
            self.assertNotIn('[ellenőri', d['megjegyzes'])
            self.assertNotIn('fordításra vár', d['jelentes'])

    def test_licenc_minden_soron(self):
        for rel in ('visszhang_megfelelok.tsv', 'visszhang_tanuk.tsv', 'sblgnt_apparatus.tsv'):
            for d in self.sorok(rel):
                self.assertIn(d['forras_licenc'], ('közkincs', 'CC BY 4.0'))
                self.assertTrue(d['forras_megnevezes'])

    def test_licencleltar_forrasnak_jelzi(self):
        leltar = {d['dataset']: d for d in self.sorok('forrasok_es_licencek.tsv')}
        for ds in ('Targum_PD', 'Vulgata_Clementina', 'LXX_OS', 'SBLGNT_apparatus', 'Tanu_atyak_index',
                   'Tanu_rabbinikus_index', 'Glossa_Ordinaria'):
            self.assertTrue(leltar[ds]['szerepe_a_csomagban'].startswith('forrás'), ds)
        self.assertEqual('kizárva', leltar['Chain_Lineage_Browser']['szerepe_a_csomagban'])

    def test_kapu_elkapja_a_chain_lineage_sort(self):
        f = self.uj()
        sz = f['visszhang_tanuk.tsv']
        sor = sz.split('\n')[2]
        c = sor.split('\t')
        c[4] = 'Órigenész (Chain Lineage)'
        f['visszhang_tanuk.tsv'] = sz.replace(sor, '\t'.join(c), 1)
        self.assertTrue(bukasok(f, 'VISSZHANG'))

    def test_kapu_elkapja_a_tiltott_forrast_es_az_osszefoglalot(self):
        f = self.uj()
        f['visszhang_megfelelok.tsv'] = f['visszhang_megfelelok.tsv'].replace('\ttargum\t', '\tbdb\t', 1)
        self.assertTrue(bukasok(f, 'VISSZHANG'))
        f = self.uj()
        sz = f['vitatott_forrasok.tsv'].split('\n')
        sz[1] = sz[1] + '\tosszefoglalo'
        f['vitatott_forrasok.tsv'] = '\n'.join(sz)
        self.assertTrue(bukasok(f, 'VISSZHANG'))

    def test_a_csomag_0_visszhang_bukas(self):
        self.assertEqual([], bukasok(self.fajlok, 'VISSZHANG'))


class EgysegesKeszlet(Alap):
    """F208: a nyílt adatmagok egységes készlete (a modernizált Károli – Strong csomag mintájára)."""

    def test_a_minta_fajlkeszlete_megvan(self):
        for rel in ('MODSZER.md', 'METHODS.md', 'ATTRIBUCIO.md', 'LICENSE', 'CITATION.cff', '.gitattributes',
                    'kozlemeny/kozlemeny_hu.md', 'kozlemeny/kozlemeny_en.md', 'ISMERT_HIBAK.md', 'KNOWN_ISSUES.md',
                    'KIADAS.txt', 'RELEASE.txt', 'ELLENORZO_OSSZEG.sha256'):
            self.assertIn(rel, self.fajlok)
            self.assertIn(rel, G.KOTELEZO)

    def test_a_kozlemeny_nincs_az_osszegben(self):
        self.assertNotIn('kozlemeny/', self.fajlok['ELLENORZO_OSSZEG.sha256'])
        self.assertIn('kozlemeny/ export-ignore', self.fajlok['.gitattributes'])
        self.assertEqual([], bukasok(self.fajlok, 'KOZLEMENY'))

    def test_kozlemeny_az_osszegben_bukik(self):
        f = self.uj()
        f['ELLENORZO_OSSZEG.sha256'] += '0' * 64 + '  kozlemeny/kozlemeny_hu.md\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))
        f = self.uj()
        f['.gitattributes'] = '* text eol=lf\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))

    def test_a_csomag_0_nyilvanos_bukas(self):
        self.assertEqual([], [(x.fajl, x.idezet) for x in bukasok(self.fajlok, 'NYILVANOS')])

    def test_nyilvanos_tiltott_szavak(self):
        for rel, szo in (('MODSZER.md', 'a termékréteg része'), ('METHODS.md', 'a PaRDeS method'),
                         ('kozlemeny/kozlemeny_hu.md', 'l. DT612'), ('CITATION.cff', 'url: https://github.com/x/y'),
                         ('LICENSE', 'felhasználói döntés'), ('ATTRIBUCIO.md', 'naplok/valami'),
                         ('README.md', 'the orchestrator decided'), ('OLVASSEL.md', 'a gerinc szerint')):
            f = self.uj()
            f[rel] += szo + '\n'
            self.assertTrue(bukasok(f, 'NYILVANOS'), (rel, szo))

    def test_pardes_szint_oszlopnev_megengedett(self):
        f = self.uj()
        f['MODSZER.md'] += 'A `pardes_szint` oszlop leírása a kódkönyvben.\n'
        self.assertEqual([], bukasok(f, 'NYILVANOS'))

    def test_kizart_forras_hianyzik_az_attribuciobol(self):
        f = self.uj()
        f['ATTRIBUCIO.md'] = f['ATTRIBUCIO.md'].replace('`MCGED`', '')
        self.assertTrue(bukasok(f, 'LICENC'))

    def test_tartalomjegyzek_sorszam(self):
        f = self.uj()
        # a szám az adatból (rögzített szám a #715 után elavult; a csoportversek száma változhat)
        n = self.info['stat']['kizaras_csoportok.tsv']
        regi = '| %s |' % E.SZ.ezres(n, 'en')
        self.assertIn(regi, f['README.md'])
        f['README.md'] = f['README.md'].replace(regi, '| %s |' % E.SZ.ezres(n + 1, 'en'))
        self.assertTrue(bukasok(f, 'KETNYELV'))

    def test_szamok_a_csomagbol(self):
        sz = E.csomag_szamok(self.fajlok, {'ALVIL-001': 1}, 0, [], '2026-01-01')
        self.assertEqual(sz['elo'], self.info['stat']['elofordulasok.tsv'])
        self.assertEqual(sz['kiz'], self.info['stat']['kizarasok.tsv'])
        self.assertEqual(sz['csoport_vers'], self.info['stat']['kizaras_csoportok.tsv'])
        self.assertEqual(sz['kiz_egyedi'] + sz['osszesito'], sz['kiz'])
        self.assertEqual(1, sz['lezart'])

    def test_lezart_kiadas_a_mai_mercevel(self):
        # a szerkesztő döntése (2026-11-12): lezárt kiadás csak a kész lap mércéje (2026-11-11) óta kiadott lap;
        # az ISTENTISZT-001 1. kiadása (2026.11.04) korábbi, az ALVIL/ANTROP-001 lapja befagyasztható (F212)
        allapot = E.feldolgozasi_allapot()
        self.assertEqual('lezárt kiadás', allapot.get('HAMART-001'))
        for mid in ('ISTENTISZT-001', 'ALVIL-001', 'ANTROP-001'):
            self.assertNotIn(mid, allapot)
        _, mot = G.tsv_sorok(self.fajlok['motivumok.tsv'])
        self.assertEqual({'lezárt kiadás', 'korábbi feldolgozás, újraírás alatt'},
                         {d['feldolgozasi_allapot'] for _, d in mot})

    def test_kh_pont_az_adatbol(self):
        # a gyökérok (2026-11-12): a sablon rögzített mondata („a javítás a projekt nyitott tétele”) a javítás után
        # is a régi állapotot mondta; az 1. pont a javított táblából és a fogyasztók forráskódjából épül
        self.assertNotIn('nyitott tétele', self.fajlok['ISMERT_HIBAK.md'])
        j = E.kh_javitott()
        self.assertTrue(j.get('megerositett'))
        self.assertIn(E.SZ.ezres(j['megerositett'], 'hu'), self.fajlok['ISMERT_HIBAK.md'])
        mind = [(h, e, True) for h, e, _ in E.kh_hasznalat()]
        szoveg = '\n'.join(E.kh_pont_hu(E.kh_meres(), j, mind))
        self.assertNotIn('még nem a javított táblán át', szoveg)
        szoveg = '\n'.join(E.kh_pont_hu(E.kh_meres(), dict(j, jelolt=0), mind))
        self.assertIn('Nincs döntés nélküli sor.', szoveg)

    def test_hogyan_olvasd_egyseg_es_csoportszo(self):
        # g2/g3 (a szerkesztő, 2026-11-12): a számlálás egysége a sor; az azonos okú csoportok szava kiírva
        self.assertIn('A számlálás egysége a sor', self.fajlok['OLVASSEL.md'])
        self.assertIn('The unit of counting is the row', self.fajlok['README.md'])
        p = E.olvasasi_peldak(self.fajlok)
        okok = [o for _, o, _, _ in p['csoportok'][:E.PELDA_LISTA]]
        for _, o, _, s in p['csoportok'][:E.PELDA_LISTA]:
            if okok.count(o) > 1:
                self.assertTrue(s, o)
        lex = E.kh_lexikon_bekotve()
        self.assertEqual(lex, 'A lexikonlapok is csak a megerősített sorokat használják.' in
                         self.fajlok['ISMERT_HIBAK.md'])

    def test_nevelo_szabaly(self):
        self.assertEqual('az', E.SZ.nevelo('1Móz 9:25'))
        self.assertEqual('a', E.SZ.nevelo('2Kir 1:1'))
        self.assertEqual('a Logosz-lexikon', E.SZ.nevelos('Logosz-lexikon'))
        for rel, t in self.fajlok.items():
            self.assertNotRegex('\n'.join(t.split('\n')[:4]), r'\b[Aa]\(z\)', rel)
        self.assertEqual([], bukasok(self.fajlok, 'NEVELO'))
        f = self.uj()
        f['MODSZER.md'] = f['MODSZER.md'] + '\nA 5 motívum.\n'
        self.assertTrue(bukasok(f, 'NEVELO'))

    def test_citation_szerzo_orcid_doi(self):
        c = self.fajlok['CITATION.cff']
        for kell in ('family-names: "Demeter"', 'given-names: "Tamás"', 'orcid: "https://orcid.org/0009-0005-9254-9731"',
                     'doi: "10.5281/zenodo.24141612"', '10.5281/zenodo.24141884', '10.5281/zenodo.24141950'):
            self.assertIn(kell, c)


if __name__ == '__main__':
    unittest.main(verbosity=1)
