#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_sqlite_epit.py -- F79 M2: az `sqlite_epit.py` tesztjei.

    python eszkozok/teszt_sqlite_epit.py

  pozitiv:      a mai adat integritasa zold
  negativ:      szandekosan rontott ideiglenes masolaton a SEMA 3. szabalyainak
                sertese megallitja az epitest (1-6., 8., + 9., 13.); a 7. szabaly jelentes
  normalizalas: STEP-alaku sor a magyar kulcson elerheto; Lam -> Sir; a nem leKepezheto
                sor a jelentesben
  determinizmus (G2), tablaszintu licenc (G4, F89), `kapcsolodas` idezojelei (split-korut), G3
"""

import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import sqlite_epit as S  # noqa: E402
import nave_bontas as NB  # noqa: E402

ROOT = S.ROOT


def masolat(tmp):
    """A repo adat/ kis tablai + a 13. szabaly szocikk-forrasai egy ideiglenes gyokerbe."""
    cel = os.path.join(tmp, 'adat')
    os.makedirs(cel)
    for f in os.listdir(os.path.join(ROOT, 'adat')):
        src = os.path.join(ROOT, 'adat', f)
        if f.endswith('.tsv') and f != 'karoli_variancia.tsv':
            shutil.copy(src, os.path.join(cel, f))
    kon = os.path.join(tmp, 'konkordancia')
    os.makedirs(kon)
    for f in ('Thayer_teljes.tsv', 'BDB_teljes_unabridged.tsv', 'UBS_DNTG_jelentesek.tsv'):
        shutil.copy(os.path.join(ROOT, 'konkordancia', f), os.path.join(kon, f))
    return tmp


def modosit(gyoker, fajl, fn):
    """fn(fejlec:list, sorok:list[list]) -> a sorok modositva helyben; a #-sorok maradnak."""
    p = os.path.join(gyoker, 'adat', fajl)
    with open(p, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    i = next(k for k, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[i].rstrip('\r').split('\t')
    adat = [s.rstrip('\r').split('\t') for s in sorok[i + 1:]]
    fn(fej, adat)
    ki = sorok[:i + 1] + ['\t'.join(r) for r in adat if r != ['']]
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(ki) + '\n')


def kezi_mt_or_kihagy():
    """F117.8 (6) (DT-F117f (a)): ha a VALÓS versmegfeleltető táblán az sqlite_epit KEZI+igehely_mt-őre leállítana,
    -> a kihagyás oka (str), különben None. Csak a VersmegfKeziMt-et kezeli; az N-F117a javításával magától megszűnik."""
    sorok = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv'))[1]
    try:
        S.kezi_mt_or(sorok)
    except S.VersmegfKeziMt as e:
        return 'N-F117a: az sqlite_epit KEZI+igehely_mt-őre (DT-F117f) a valós táblán leállít; az N-F117a javításakor visszaveendő [%s]' % str(e)[:120]
    return None


def sertett_szabalyok(sertesek):
    return sorted(s.cim.split('.')[0] for s in sertesek)


class Pozitiv(unittest.TestCase):
    def test_mai_adat_zold(self):
        sorok, sertesek = S.integritas(os.path.join(ROOT, 'adat'))
        self.assertEqual(sertesek, [], [s.sor_szoveg() for s in sertesek])
        # #11 S2: + a 15. (DT183) es a 16. (DT250) fejlec-szabaly; F127: + a 2/b. (DT-F127b)
        self.assertEqual(len(sorok), 15)

    def test_g3_nincs_csv_modul(self):
        with open(os.path.join(ROOT, 'eszkozok', 'sqlite_epit.py'), encoding='utf-8') as f:
            kod = f.read()
        self.assertNotIn('import csv', kod)
        self.assertNotIn('csv.reader', kod)
        self.assertNotIn('csv.writer', kod)

    def test_g1_gitignore(self):
        with open(os.path.join(ROOT, '.gitignore'), encoding='utf-8') as f:
            sorok = [s.strip() for s in f]
        self.assertIn('pardes.db', sorok)
        self.assertIn('pardes*.db.epit', sorok)

    def test_g4_szabalyok_az_ellenorizbol(self):
        # az integritas() az ellenoriz modul szabaly-fuggvenyeit hivja, nem masolja
        import inspect
        forras = inspect.getsource(S.integritas)
        for n in ('szabaly1_', 'szabaly2_', 'szabaly3_', 'szabaly4_', 'szabaly5_', 'szabaly6_',
                  'szabaly7_', 'szabaly8_', 'szabaly9_', 'szabaly10_', 'szabaly11_', 'szabaly13_',
                  'szabaly15_', 'szabaly16_'):
            self.assertIn('E.' + n, forras)


class Negativ(unittest.TestCase):
    """Minden SEMA 3. szabaly sertese megallitja az epitest (G4)."""

    def futtat(self, mutacio, szabaly):
        tmp = tempfile.mkdtemp()
        try:
            masolat(tmp)
            mutacio(tmp)
            sorok, sertesek = S.integritas(os.path.join(tmp, 'adat'))
            self.assertIn(szabaly, sertett_szabalyok(sertesek),
                          [s.sor_szoveg() for s in sorok])
            return tmp
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_baseline_a_masolaton_zold(self):
        tmp = tempfile.mkdtemp()
        try:
            masolat(tmp)
            _, sertesek = S.integritas(os.path.join(tmp, 'adat'))
            self.assertEqual(sertesek, [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_1_hivatkozasi_epseg(self):
        def m(t):
            modosit(t, 'elofordulasok.tsv', lambda f, r: r[0].__setitem__(f.index('id'), 'NINCS-999'))
        self.futtat(m, '1')

    def test_2_nincs_kozvetlen_ut(self):
        def m(t):
            def fn(fej, sorok):
                _, eo = G.tsv_beolvas(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
                kulcs = (eo[0]['id'], eo[0]['igehely'])
                for r in sorok:
                    if len(r) == len(fej) and (r[fej.index('id')], r[fej.index('igehely')]) == kulcs:
                        r[fej.index('dontes')] = 'nyitva'
            modosit(t, 'jeloltek.tsv', fn)
        self.futtat(m, '2')

    def test_3_proveniencia(self):
        def m(t):
            modosit(t, 'elofordulasok.tsv', lambda f, r: r[0].__setitem__(f.index('proveniencia'), ''))
        self.futtat(m, '3')

    def test_4_gerinc_elem(self):
        def m(t):
            modosit(t, 'elofordulasok.tsv', lambda f, r: r[0].__setitem__(f.index('gerinc_elem'), ''))
        self.futtat(m, '4')

    def test_5_karoli_triplet(self):
        def m(t):
            def fn(fej, sorok):
                for r in sorok:
                    if len(r) == len(fej) and r[fej.index('karoli_szo')].strip():
                        r[fej.index('azonositas_modja')] = ''
                        return
            modosit(t, 'elofordulasok.tsv', fn)
        self.futtat(m, '5')

    def test_6_gate_kenyszer(self):
        def m(t):
            def fn(fej, sorok):
                for r in sorok:
                    if len(r) == len(fej) and r[fej.index('statusz')] in ('publikálható', 'véglegesített'):
                        r[fej.index('negativ_kriterium')] = ''
                        return
            modosit(t, 'motivumok.tsv', fn)
        self.futtat(m, '6')

    def test_8_dataset_lefedettseg(self):
        def m(t):
            def fn(fej, sorok):
                uj = dict((k, '') for k in fej)
                uj.update({'study_tipus': 'tematikus', 'dataset': 'ZZZ_teszt',
                           'fajl': 'konkordancia/ZZZ_teszt.tsv', 'kotelezoseg': 'mindig',
                           'feltetel': '—', 'allapot': 'elerheto'})
                sorok.append([uj[k] for k in fej])
            modosit(t, 'datasetek.tsv', fn)
        self.futtat(m, '8')

    def test_9_teljes_jelentes_szam(self):
        def m(t):
            modosit(t, 'elofordulasok.tsv', lambda f, r: r[0].__setitem__(f.index('jelentes_szam'), 'teljes'))
        self.futtat(m, '9')

    def test_10_lxx_dontesek(self):
        def m(t):
            modosit(t, 'lxx_dontesek.tsv', lambda f, r: r[0].__setitem__(f.index('tipus'), 'ervenytelen_tipus'))
        self.futtat(m, '10')

    def test_11_res_forras_egyezes(self):
        def m(t):
            modosit(t, 'res_forras.tsv', lambda f, r: r[0].__setitem__(f.index('tanulmany'), 'tematikus_lezart/NINCS_ILYEN.md'))
        self.futtat(m, '11')

    def test_az_epites_a_10_szabaly_serteskor_is_megall(self):
        tmp = tempfile.mkdtemp()
        try:
            masolat(tmp)
            modosit(tmp, 'lxx_dontesek.tsv', lambda f, r: r[0].__setitem__(f.index('tipus'), 'ervenytelen_tipus'))
            ki = os.path.join(tmp, 'x.db')
            self.assertEqual(S.main(['--gyoker', tmp, '--kimenet', ki]), 1)
            self.assertFalse(os.path.exists(ki))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_13_forditasi_gyorsitotar(self):
        def m(t):
            def fn(fej, sorok):
                sorok.append(list(sorok[0]))   # azonos kulcsu ketto
            modosit(t, 'forditasok.tsv', fn)
        self.futtat(m, '13')

    def test_az_epites_serteskor_nem_ir_fajlt(self):
        tmp = tempfile.mkdtemp()
        try:
            masolat(tmp)
            modosit(tmp, 'elofordulasok.tsv', lambda f, r: r[0].__setitem__(f.index('gerinc_elem'), ''))
            ki = os.path.join(tmp, 'x.db')
            kod = S.main(['--gyoker', tmp, '--kimenet', ki])
            self.assertEqual(kod, 1)
            self.assertFalse(os.path.exists(ki))
            self.assertFalse(os.path.exists(ki + '.epit'))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class KeziMtOr(unittest.TestCase):
    """F117.5 (DT-F117f (a)): KEZI osztályú sor kitöltött igehely_mt-vel -> az építés leáll (N-F117a)."""
    FEJ = 'igehely_karoli\tigehely_kjv\tigehely_mt\tosztaly\tforras\tmegjegyzes'

    def _gyoker(self, sorok):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        os.makedirs(os.path.join(tmp, 'konkordancia'))
        with open(os.path.join(tmp, 'konkordancia', 'Karoli_versmegfeleltetes.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# teszt-fixtúra\n' + self.FEJ + '\n' + '\n'.join(sorok) + '\n')
        return tmp

    def test_kezi_kitoltott_mt_leall(self):
        g = self._gyoker(['Hós 2:1\t2:2\t2:4\tKEZI\tszoveg_osszevetes_f117\t-',
                          '1Móz 1:1\t1:1\t\tKJV\tszamlalas\t'])
        ep = S.Epito(g, os.path.join(g, 'x.db'), 'minta')
        with self.assertRaises(S.VersmegfKeziMt) as cm:
            ep._bsb_szamozas()
        self.assertIn('1 KEZI', str(cm.exception))
        self.assertIn('Hós 2:1', str(cm.exception))
        self.assertIn('N-F117a', str(cm.exception))

    def test_kezi_ures_mt_mt_es_kjv_nem_all_le(self):
        sorok = [{'igehely_karoli': 'Préd 9:20', 'igehely_kjv': '9:18', 'igehely_mt': '', 'osztaly': 'KEZI'},
                 {'igehely_karoli': 'Jón 2:3', 'igehely_kjv': '2:2', 'igehely_mt': '2:3', 'osztaly': 'MT'},
                 {'igehely_karoli': '1Móz 1:1', 'igehely_kjv': '1:1', 'igehely_mt': '', 'osztaly': 'KJV'}]
        S.kezi_mt_or(sorok)   # nem dob
        g = self._gyoker(['Préd 9:20\t9:18\t\tKEZI\tkezi\traw=9:18', 'Jón 2:3\t2:2\t2:3\tMT\tszoveg_osszevetes_f117\t-',
                          '1Móz 1:1\t1:1\t\tKJV\tszamlalas\t'])
        ep = S.Epito(g, os.path.join(g, 'y.db'), 'minta')
        # az őr átengedi; utána a fixtúrából hiányzó BSB-forrás (és csak az) állítja meg az építést
        with self.assertRaises(FileNotFoundError) as cm:
            ep._bsb_szamozas()
        self.assertIn('BSB_Strongs.tsv', str(cm.exception.filename))


class Normalizalas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = S.Konyvek(G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'))[1])

    def test_step_igehely(self):
        self.assertEqual(self.k.step_igehely('Gen.1.1'), '1Móz 1:1')
        self.assertEqual(self.k.step_igehely('1Ki.8.9'), '1Kir 8:9')

    def test_siralmak_alias(self):
        self.assertEqual(self.k.step_igehely('Lam.2.8'), 'Sir 2:8')

    def test_nem_lekepezheto(self):
        self.assertIsNone(self.k.step_igehely('LXX.Gen.46.20'))
        self.assertIsNone(self.k.step_igehely('[Act.26.7]'))
        self.assertIsNone(self.k.step_igehely('Xyz.1.1'))

    def test_tartomany(self):
        self.assertEqual(self.k.step_tartomany('Gen.2.4-Gen.2.5'), ('1Móz 2:4', '1Móz 2:5'))
        self.assertEqual(self.k.step_tartomany('Gen.2.4'), ('1Móz 2:4', '1Móz 2:4'))
        self.assertIsNone(self.k.step_tartomany('Gen.2.4-Foo.1.1'))

    def test_hu_igehely(self):
        self.assertEqual(S.hu_igehely_parse('1Móz 14:18-20'), ('1Móz', 14, 18, 14, 20))
        self.assertEqual(S.hu_igehely_parse('1Móz 4:25-5:32'), ('1Móz', 4, 25, 5, 32))
        self.assertEqual(S.hu_igehely_parse('JSir 1:1'), ('Sir', 1, 1, 1, 1))
        self.assertIsNone(S.hu_igehely_parse('nem igehely'))


class TipnrUtotag(unittest.TestCase):
    """F88 (DT111): a TIPNR-betöltő utótag-szabálya, G3 (a)-(e)."""

    def test_nagybetus_utotag(self):
        self.assertEqual(S.tipnr_strong_szetvalaszt('G2424G'), ('G2424', 'G'))
        self.assertEqual(S.tipnr_strong_szetvalaszt('H3063N'), ('H3063', 'N'))

    def test_kisbetus_utotag(self):
        self.assertEqual(S.tipnr_strong_szetvalaszt('H5838z'), ('H5838', 'z'))

    def test_utotag_nelkuli_valtozatlan(self):
        self.assertEqual(S.tipnr_strong_szetvalaszt('H0175'), ('H0175', ''))
        self.assertEqual(S.tipnr_strong_szetvalaszt('H175'), ('H0175', ''))

    def test_nem_ertelmezheto_valueerror(self):
        for rossz in ('—', '', 'X123G', 'G2424G+H0001', 'G0000G', 'H12345A'):
            with self.assertRaises(ValueError, msg=rossz):
                S.tipnr_strong_szetvalaszt(rossz)

    def test_strong_util_tilt_tovabbra_is_elutasit(self):
        import strong_util as SU
        with self.assertRaises(ValueError):
            SU.strong_normalizal('G2424G')
        with self.assertRaises(ValueError):
            SU.strong_normalizal('H5838z')


class Integracio(unittest.TestCase):
    """A kis minta ketszeri epitese (G2), tablaszintu licenc (G4, F89), normalizalas, idezojelek."""

    @classmethod
    def setUpClass(cls):
        # F117.8 (6): a közös építés a valós táblán fut; ha az őr (DT-F117f) leállítaná, az egész osztály kihagyva,
        # kimondott okkal -- csak ebben a helyzetben (az N-F117a javításával magától visszaáll)
        ok = kezi_mt_or_kihagy()
        if ok:
            raise unittest.SkipTest(ok)
        cls.tmp = tempfile.mkdtemp()
        cls.a = os.path.join(cls.tmp, 'a.db')
        cls.b = os.path.join(cls.tmp, 'b.db')
        for ki in (cls.a, cls.b):
            kod = S.main(['--mod', 'minta', '--kimenet', ki])
            assert kod == 0, kod
        cls.con = sqlite3.connect(cls.a)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_g2_determinisztikus(self):
        ha, hb = S.tablak_hash(self.a), S.tablak_hash(self.b)
        self.assertEqual(ha, hb)
        self.assertGreater(len(ha), 30)

    def _tablak(self):
        return [n for (n,) in self.con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'fts_motivum_%'").fetchall()]

    def test_g4_nincs_licenc_oszlop_az_adattablakban(self):
        # F89 / DT113: a licenc tablaszintu; egyik adattablanak (az FTS-t is beleertve) sincs licenc-oszlopa
        tiltott = {'licenc_allapot', 'kereskedelmi', 'licenc_dataset'}
        for n in self._tablak():
            if n == 'tabla_licenc':
                continue
            oszlopok = {r[1] for r in self.con.execute('PRAGMA table_info("%s")' % n)}
            self.assertFalse(oszlopok & tiltott, n)

    def test_g4_minden_tablanak_pontosan_egy_tabla_licenc_sora(self):
        tablak = self._tablak()
        self.assertIn('tabla_licenc', tablak)
        sorok = self.con.execute('SELECT tabla, COUNT(*) FROM tabla_licenc GROUP BY tabla').fetchall()
        self.assertEqual(sorted(n for n, _ in sorok), sorted(tablak))
        self.assertTrue(all(d == 1 for _, d in sorok))
        ures = self.con.execute("SELECT COUNT(*) FROM tabla_licenc WHERE IFNULL(licenc_allapot,'')='' "
                                "OR IFNULL(kereskedelmi,'')='' OR IFNULL(licenc_dataset,'')='' "
                                "OR IFNULL(cimke,'')=''").fetchone()[0]
        self.assertEqual(ures, 0)

    def test_g4_karoli_strong_tablak_sajat_licencsora(self):
        for t, ds in (('token_par', 'Karoli_Strong_parok'), ('token_karoli', 'Karoli_Strong_szavak'),
                      ('frazis_pozicio', 'Karoli_Strong_parok')):
            r = self.con.execute('SELECT licenc_dataset, licenc_allapot, kereskedelmi, cimke '
                                 'FROM tabla_licenc WHERE tabla=?', (t,)).fetchall()
            self.assertEqual(r, [(ds, 'tisztazott', 'igen', 'minden jog fenntartva')], t)

    def test_g4_legszigorubb_ertek(self):
        # egy szarmaztatott tabla a forrasai kozul a legszigorubb erteket kapja (DT109 (2c))
        ep = S.Epito(ROOT, os.path.join(self.tmp, 'd.db'), 'minta')
        ep.licencek = {
            'A': {'allapot': 'kozkincs', 'kereskedelmi': 'igen', 'cimke': 'kozkincs'},
            'B': {'allapot': 'tisztazatlan', 'kereskedelmi': 'nem', 'cimke': 'tisztazatlan'},
            'C': {'allapot': 'tisztazott', 'kereskedelmi': 'feltetelesen', 'cimke': 'kozkincs'},
        }
        self.assertEqual(ep.licenc_feloldas(['A', 'B', 'C']),
                         ('tisztazatlan', 'nem', 'A+B+C', 'kozkincs; tisztazatlan'))
        self.assertEqual(ep.licenc_feloldas(['A', 'C']), ('tisztazott', 'feltetelesen', 'A+C', 'kozkincs'))
        # a valodi leltar: a strong_parok (TAHOT, TAGNT, projekt_adat) egyutt tisztazott/igen
        r = self.con.execute("SELECT licenc_allapot, kereskedelmi FROM tabla_licenc WHERE tabla='strong_parok'").fetchone()
        self.assertEqual(r, ('tisztazott', 'igen'))

    def test_g4_zart_csomagbol_kizarando_cimkek_megkulonboztethetok(self):
        # a CC BY-SA (SDBH, SDGNT, UBS, LSJ, tW) es az MCGED sora a cimkerol felismerheto, a sajat adat nem
        _, licencsorok = S.G.tsv_beolvas(os.path.join(ROOT, 'adat', 'licencek.tsv'))
        ep = S.Epito(ROOT, os.path.join(self.tmp, 'e.db'), 'minta')
        ep.licencek = {r['dataset']: r for r in licencsorok}
        for k in ('SDBH', 'SDGNT', 'UBS_DBH', 'UBS_DNTG', 'LSJ', 'tW_szocikkek'):
            self.assertEqual(ep.licenc_feloldas([k])[3], 'CC BY-SA 4.0', k)
        self.assertEqual(ep.licenc_feloldas(['MCGED'])[3], '© Mounce 1993')
        for k in ('projekt_adat', 'Karoli_Strong_parok', 'Karoli_Strong_szavak', 'karoli_variancia'):
            self.assertEqual(ep.licenc_feloldas([k])[0:2], ('tisztazott', 'igen'), k)
            self.assertEqual(ep.licenc_feloldas([k])[3], 'minden jog fenntartva', k)

    def test_g6_ismeretlen_licenc_nem_kap_alaperteket(self):
        # licencsor nelkuli tabla nem epul be (a mintaban nincs ilyen, a mechanizmus kozvetlenul)
        ep = S.Epito(ROOT, os.path.join(self.tmp, 'c.db'), 'minta')
        ep.licencek = {}
        ep.con = sqlite3.connect(':memory:')
        self.assertFalse(ep.tabla('x', [('a', 'TEXT')], [('1',)], ['nincs_ilyen']))
        self.assertEqual(ep.kihagyott[0][0], 'x')

    def test_step_sor_a_magyar_kulcson(self):
        r = self.con.execute("SELECT step_nyers FROM kh WHERE igehely='1Móz 1:1' LIMIT 1").fetchone()
        self.assertIsNotNone(r)
        self.assertEqual(r[0], 'Gen.1.1')

    def test_siralmak_a_sir_kulcson(self):
        n = self.con.execute("SELECT COUNT(*) FROM kh WHERE step_nyers LIKE 'Lam.%' AND igehely LIKE 'Sir %'").fetchone()[0]
        self.assertGreater(n, 0)
        for t in ('kh', 'tipnr'):
            self.assertEqual(self.con.execute("SELECT COUNT(*) FROM %s WHERE igehely LIKE 'JSir%%'" % t).fetchone()[0], 0)

    def test_tipnr_utotag_oszlopok(self):
        """G3 (a)-(c) az épített mintán; (d) a megmaradt NULL név szerint a jelentésben."""
        sorok = self.con.execute("SELECT strong, utotag, strong_nyers FROM tipnr").fetchall()
        self.assertTrue(sorok)
        van_utotagos = van_nelkuli = False
        for s, u, ny in sorok:
            if s is None:
                continue
            self.assertEqual(s + (u or ''), S.strong_normalizal(ny[:-1]) + ny[-1] if u else S.strong_normalizal(ny))
            if u:
                van_utotagos = True
                self.assertTrue(ny.endswith(u) and ny != s)
            else:
                van_nelkuli = True
                self.assertEqual(s, S.strong_normalizal(ny))
        self.assertTrue(van_utotagos and van_nelkuli)
        r = self.con.execute("SELECT strong, utotag, strong_nyers FROM tipnr WHERE strong_nyers='H0040G' LIMIT 1").fetchone()
        self.assertEqual(r, ('H0040', 'G', 'H0040G'))
        null_sor = self.con.execute("SELECT COUNT(*) FROM tipnr WHERE strong IS NULL").fetchone()[0]
        jelentes = self.con.execute("SELECT COALESCE(SUM(darab),0) FROM normalizalas_jelentes "
                                    "WHERE tabla='tipnr' AND ok='Strong-szám nem normalizálható'").fetchone()[0]
        self.assertEqual(null_sor, jelentes)

    def test_nem_lekepezheto_a_jelentesben(self):
        r = self.con.execute("SELECT darab FROM normalizalas_jelentes WHERE tabla='tipnr' "
                             "AND nyers='LXX.Gen.46.20'").fetchone()
        self.assertIsNotNone(r)
        self.assertEqual(r[0], 2)

    def test_kapcsolodas_idezojelei_megmaradnak(self):
        _, sorok = G.tsv_beolvas(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
        forras = sorted((r['id'], r['igehely'], r['kapcsolodas']) for r in sorok)
        db = sorted(self.con.execute('SELECT id, igehely, kapcsolodas FROM elofordulasok').fetchall())
        self.assertEqual(forras, db)
        # fuggetlen nyers olvasas: a `kapcsolodas` a 3. oszlop (index 2), split('\t')
        with open(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'), encoding='utf-8', newline='') as f:
            nyers = [s.rstrip('\r\n').split('\t') for s in f if s.strip() and not s.startswith('#')][1:]
        nyers_idezojeles = sum(1 for m in nyers if m[2].startswith('"'))
        db_idezojeles = self.con.execute(
            "SELECT COUNT(*) FROM elofordulasok WHERE substr(kapcsolodas,1,1)='\"'").fetchone()[0]
        self.assertGreater(nyers_idezojeles, 0)
        self.assertEqual(db_idezojeles, nyers_idezojeles)   # a mert szam a CLAUDE.md-ben 79 volt; ma ennyi

    def test_strong_parok_teljes(self):
        n = self.con.execute('SELECT COUNT(*) FROM strong_parok').fetchone()[0]
        self.assertGreater(n, 100000)
        r = self.con.execute("SELECT n FROM strong_parok WHERE a='H0922' AND b='H8414'").fetchone()
        self.assertIsNotNone(r)
        self.assertGreaterEqual(r[0], 3)

    def test_fts_regi_forras_jelolve(self):
        n = self.con.execute("SELECT COUNT(*) FROM fts_motivum WHERE regi_forras=1").fetchone()[0]
        self.assertGreater(n, 0)
        m = self.con.execute("SELECT COUNT(*) FROM fts_motivum WHERE regi_forras=0").fetchone()[0]
        self.assertGreater(m, 0)
        talalat = self.con.execute("SELECT COUNT(*) FROM fts_motivum WHERE fts_motivum MATCH 'tehom OR mélység'").fetchone()[0]
        self.assertGreater(talalat, 0)

    def test_karoli_strong_kivonat_betoltve_es_jelentes(self):
        self.assertGreater(self.con.execute('SELECT COUNT(*) FROM karoli_strong_kivonat').fetchone()[0], 300)
        r = self.con.execute("SELECT darab FROM normalizalas_jelentes WHERE tabla='karoli_strong_kivonat' "
                             "AND nyers='Jób 17:16'").fetchone()
        self.assertIsNotNone(r)

    def test_adat_tabla_sajat_licence(self):
        for t in ('morf_kulcs_heber', 'morf_nyelv_aramai'):
            r = self.con.execute('SELECT licenc_dataset, licenc_allapot, kereskedelmi FROM tabla_licenc '
                                 'WHERE tabla=?', (t,)).fetchall()
            self.assertEqual(r, [(t, 'tisztazott', 'igen')])
        r = self.con.execute("SELECT licenc_dataset, licenc_allapot, kereskedelmi, cimke FROM tabla_licenc "
                             "WHERE tabla='motivumok'").fetchall()
        self.assertEqual(r, [('projekt_adat', 'tisztazott', 'igen', 'minden jog fenntartva')])

    def test_tagnt_karoli_vers_nelkuli_kulcsok(self):
        nevek = {r[0] for r in self.con.execute(
            "SELECT nyers FROM normalizalas_jelentes WHERE tabla='TAGNT_kivonat.tsv'")}
        self.assertTrue({'Róm 3:31', '1Kor 3:23', 'Róm 8:39'} <= nevek)
        darab = self.con.execute("SELECT SUM(darab) FROM normalizalas_jelentes WHERE tabla='TAGNT_kivonat.tsv' "
                                 "AND ok LIKE 'nincs ilyen Károli-vers%'").fetchone()[0]
        # a kis mintában a token_eredeti csak a minta verseit tartalmazza; a jelentés a teljes TAGNT-ra szól


    def test_kjv_es_tbes_betoltve(self):
        for t in ('kjv', 'tbesg', 'tbesh'):
            self.assertGreater(self.con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0], 1000, t)

    def test_probak_megegyeznek(self):
        for p in S.probak(self.a, ROOT):
            self.assertTrue(p['ok'], '%s: %s' % (p['pont'], p['megj']))

    # -- F92 (DT-F92a): az olvasoi lapok hiany-tablai ------------------------------------------
    def _meta_dict(self):
        return dict(self.con.execute('SELECT kulcs, ertek FROM meta').fetchall())

    def test_f92_ujtablak_betoltve_es_licenccel(self):
        for t, ds in (('token_macula', 'Macula_heber'), ('lxx_token', 'LXX_OS'), ('bdb_alias', 'BDB+projekt_adat'),
                      ('nave_vers', 'Nave_basokant+Karoli_versmegfeleltetes+LXX_OS'),
                      ('lxx_versszam', 'LXX_OS+Versifikacios_tablak+Karoli_versmegfeleltetes')):
            self.assertGreater(self.con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0], 100, t)
            r = self.con.execute('SELECT licenc_dataset FROM tabla_licenc WHERE tabla=?', (t,)).fetchall()
            self.assertEqual(r, [(ds,)], t)
            self.assertTrue(self.con.execute('SELECT 1 FROM meta WHERE kulcs=?', ('hash:' + t,)).fetchone(), t)
        # a bdb_alias meta-sorban latszik a ket osszetevo
        self.assertEqual(self._meta_dict()['bdb_alias:licenc_osszetevok'], 'BDB+projekt_adat')

    def test_f92_sorszamok_a_forrassal(self):
        gen = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'Macula_heber_Genezis.tsv'))[1]
        db = sum(1 for r in gen if r['karoli'].startswith('1Móz ') and ';' not in r['karoli'])
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM token_macula WHERE igehely LIKE '1Móz %'").fetchone()[0], db)
        lx = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'LXX_OS', 'genesis.tsv'))[1]
        db = sum(1 for r in lx if r['igehely_karoli'].startswith('1Móz '))
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM lxx_token WHERE karoli_igehely LIKE '1Móz %'").fetchone()[0], db)
        al = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'BDB_strong_alias.tsv'))[1]
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM bdb_alias').fetchone()[0], len(al))

    def test_f92_nave_semmi_nem_tunik_el_nemanak(self):
        m = self._meta_dict()
        nave = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'Nave_basokant.tsv'))[1]
        kihagyott = sum(int(v) for k, v in m.items()
                        if k.startswith('nave_vers:kihagyott:'))
        self.assertEqual(int(m['nave_vers:nave_basokant_sor']), len(nave))
        self.assertEqual(int(m['nave_vers:bontott_forras_sor']) + kihagyott, len(nave))
        self.assertEqual(int(m['nave_vers:kihagyott_osszes']), kihagyott)
        # fejezet-szintu es igehely nelkuli sor nem kerul a nave_vers-be (a kihagyott szamuk egyezik a forrassal)
        self.assertEqual(int(m['nave_vers:kihagyott:fejezet_szintu']),
                         sum(1 for r in nave if NB.hely_elemez(r['igehely'])
                             and NB.hely_elemez(r['igehely'])[0] == 'fejezet'))
        self.assertEqual(int(m['nave_vers:kihagyott:igehely_nelkuli']),
                         sum(1 for r in nave if not r['igehely'].strip()))
        self.assertEqual(self.con.execute(
            "SELECT COUNT(*) FROM nave_vers WHERE nave_hely='' OR igehely IS NULL OR igehely=''").fetchone()[0], 0)
        jel = {ok: d for ok, d in self.con.execute(
            "SELECT nyers, darab FROM normalizalas_jelentes WHERE tabla='nave_vers'")}
        self.assertEqual(jel['fejezet_szintu'], int(m['nave_vers:kihagyott:fejezet_szintu']))

    def test_f92_nave_bontas_modul(self):
        karoli = ['Zsolt 22:1', 'Zsolt 22:2', 'Zsolt 22:3', 'Zsolt 23:1']
        racs = NB.KjvRacs(karoli, {}, {'Zsolt 22:1': '22:2', 'Zsolt 22:2': '22:3', 'Zsolt 22:3': '22:4'})
        self.assertEqual(racs.bont('Zsolt', 22, 2, 22, 3), ['Zsolt 22:1', 'Zsolt 22:2'])   # KJV-szamozas szerint
        self.assertEqual(NB.hely_elemez('2Móz 6:16-20'), ('vers', '2Móz', 6, 16, 6, 20))
        self.assertEqual(NB.hely_elemez('Zsolt 22'), ('fejezet', 'Zsolt', 22))
        self.assertIsNone(NB.hely_elemez(''))
        sorok = [{'igehely': 'Zsolt 22:2'}, {'igehely': 'Zsolt 22'}, {'igehely': ''}, {'igehely': 'Zsolt 99:1'}]
        ki, kih, bontott = NB.nave_bont(sorok, racs)
        self.assertEqual(len(sorok), bontott + sum(kih.values()))
        self.assertEqual((bontott, sum(kih.values())), (1, 3))

    def test_f92_lxx_versszam_minden_ot_versre(self):
        # DT-F92b: a terkep nem forras -- csak LXX_OS vagy nincs; a terkep erteke a nem kanonikus terkep_ertek oszlopban
        self.assertTrue({f for (f,) in self.con.execute('SELECT DISTINCT forras FROM lxx_versszam')} <= {'LXX_OS', 'nincs'})
        # a kitoltetlen hiany ures lxx_igehely-vel
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM lxx_versszam WHERE forras='nincs' "
                                          "AND lxx_igehely!=''").fetchone()[0], 0)
        # minden 1Moz-vers (TAHOT heber token) legalabb egy sorral szerepel
        hi = self.con.execute("SELECT COUNT(DISTINCT igehely) FROM token_eredeti WHERE nyelv='H' "
                              "AND igehely LIKE '1Móz %' AND van_vers=1").fetchone()[0]
        van = self.con.execute("SELECT COUNT(DISTINCT karoli_igehely) FROM lxx_versszam "
                               "WHERE karoli_igehely LIKE '1Móz %'").fetchone()[0]
        self.assertEqual(van, hi)
        m = self._meta_dict()
        self.assertGreaterEqual(int(m['lxx_versszam:sor:LXX_OS'])
                                + int(m['lxx_versszam:sor:nincs']), int(m['lxx_versszam:ot_vers']))

    def test_f92_lxx_szovegforma_parhuzamos_formak(self):
        # ellenor UJ-1: a Dan/Bir/Jozs parhuzamos LXX-szovegformai nem fesulhetnek ossze
        ep = S.Epito(ROOT, os.path.join(self.tmp, 'f.db'), 'minta')
        formak = {}
        for r in ep._lxx_os_fajlok():
            if r['igehely_karoli']:
                formak.setdefault(r['igehely_karoli'], set()).add(r['_fajl'])
        tobb = {ig: f for ig, f in formak.items() if len(f) > 1}
        self.assertTrue(any('daniel' in f and 'daniel-theodotion' in f for f in tobb.values()))
        self.assertTrue(any('judges' in f and 'judges-vaticanus-b' in f for f in tobb.values()))
        self.assertTrue(any('joshua' in f and 'joshua-vaticanus-b' in f for f in tobb.values()))
        # az oszlop a minta-adatbazisban: a szovegforma a fajlnev, minden sornak van
        ertekek = {x for (x,) in self.con.execute('SELECT DISTINCT szovegforma FROM lxx_token')}
        self.assertIn('genesis', ertekek)
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM lxx_token WHERE IFNULL(szovegforma,'')=''").fetchone()[0], 0)
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM lxx_versszam WHERE forras='LXX_OS' "
                                          "AND IFNULL(szovegforma,'')=''").fetchone()[0], 0)
        # ahol a minta tartalmaz tobbformas verset, az lxx_versszam kulon sort ad formankent
        for ig, n in self.con.execute("SELECT karoli_igehely, COUNT(DISTINCT szovegforma) FROM lxx_token "
                                      "GROUP BY karoli_igehely HAVING COUNT(DISTINCT szovegforma)>1"):
            self.assertGreaterEqual(self.con.execute("SELECT COUNT(DISTINCT szovegforma) FROM lxx_versszam "
                                                     "WHERE karoli_igehely=? AND forras='LXX_OS'", (ig,)).fetchone()[0], n)

    def test_f92_terkep_nem_meghatarozhato_nem_esik_ki_nemanan(self):
        m = self._meta_dict()
        sorok = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'LXX_versificacios_terkep.tsv'))[1]
        nm = sum(1 for r in sorok if r['KJV_igehely'] == 'NEM_MEGHATAROZHATO')
        self.assertGreater(nm, 0)
        self.assertEqual(int(m['lxx_versszam:terkep_nem_meghatarozhato_sor']), nm)
        jel = self.con.execute("SELECT darab FROM normalizalas_jelentes WHERE tabla='lxx_versszam' "
                               "AND nyers='NEM_MEGHATAROZHATO'").fetchone()
        self.assertEqual(jel[0], nm)
        # a terkep-sorok minden kulcsa szamolt (F91, DT-F91b): NEM_MEGHATAROZHATO + KJV-kulcs (a KJV-kulcs vagy
        # atvalthato Karoli-versre, vagy 'karoli_nelkul')
        kulcsok = {r['KJV_igehely'] for r in sorok} - {'NEM_MEGHATAROZHATO'}
        self.assertEqual(int(m['lxx_versszam:terkep_kjv_kulcs']), len(kulcsok))
        self.assertLessEqual(int(m['lxx_versszam:terkep_kjv_kulcs_karoli_nelkul']), len(kulcsok))
        self.assertEqual(int(m['lxx_versszam:terkep_ot_vers']) + int(m['lxx_versszam:terkep_nem_ot_vers']),
                         int(m['lxx_versszam:terkep_karoli_kulcs']))
        # a terkep oszlopa KJV_igehely (nem Karoli_igehely): az atnevezes utan a regi nev nincs
        self.assertIn('KJV_igehely', sorok[0])
        self.assertNotIn('Karoli_igehely', sorok[0])

    def test_f92_macula_ketertelmu_strong_pozicio_sorrendben(self):
        rossz = self.con.execute("SELECT COUNT(*) FROM token_macula WHERE strong IS NOT NULL AND igehely!='' "
                                 "AND (strong_poz IS NULL OR strong_n IS NULL OR strong_poz<1 OR strong_poz>strong_n)").fetchone()[0]
        self.assertEqual(rossz, 0)
        for ig, st, n, k, mx in self.con.execute(
                "SELECT igehely, strong, MAX(strong_n), COUNT(*), COUNT(DISTINCT strong_poz) FROM token_macula "
                "WHERE strong IS NOT NULL AND igehely!='' GROUP BY igehely, strong"):
            self.assertEqual((k, mx), (n, n), (ig, st))
        self.assertGreater(int(self._meta_dict()['token_macula:ketertelmu_vers_strong_csoport']), 0)

    def test_f115_macula_chi_xi_javitas(self):
        """F115 / DT-F115a: a Macula `greek` chi<->xi hibája az importban javítva; a forrásalak és a Rahlfs-minőségjelölés megmarad."""
        csere = str.maketrans({'χ': 'ξ', 'ξ': 'χ', 'Χ': 'Ξ', 'Ξ': 'Χ'})
        # (1) 1Móz 1:1 bereshit: a forrás ἀρξῇ, a javított ἀρχῇ; a minősítés a DB-ben mért érték
        sor = self.con.execute("SELECT lxx_szo, lxx_szo_forras, lxx_szo_rahlfs FROM token_macula "
                               "WHERE igehely='1Móz 1:1' AND strong='H7225'").fetchall()
        self.assertTrue(sor)
        self.assertEqual(sor[0][0], 'ἀρχῇ')
        self.assertEqual(sor[0][1], 'ἀρξῇ')
        self.assertEqual(sor[0][2], 'rahlfs_igazolt')  # a DB-ben mért érték (F115, 2026-10-18)
        # (2) jelölten üres mező nincs
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM token_macula WHERE COALESCE(lxx_szo_forras,'')!='' "
                                          "AND COALESCE(lxx_szo,'')=''").fetchone()[0], 0)
        # (3) chi/xi-mentes sorban a minősítés üres és lxx_szo = lxx_szo_forras
        ures = 0
        for szo, forras, rahlfs in self.con.execute("SELECT lxx_szo, lxx_szo_forras, lxx_szo_rahlfs FROM token_macula "
                                                    "WHERE COALESCE(lxx_szo_forras,'')!=''"):
            van = any(c in 'χξΧΞ' for c in forras)
            if not van:
                self.assertEqual((szo, rahlfs or ''), (forras, ''))
            else:
                # (4) chi/xi-s sorban lxx_szo = a forrás chi<->xi cseréje, és van minősítés
                self.assertEqual(szo, forras.translate(csere))
                self.assertTrue(rahlfs)
                ures += 1
        self.assertGreater(ures, 0)
        m = self._meta_dict()
        self.assertEqual(sum(int(v) for k, v in m.items() if k.startswith('token_macula:lxx_szo_rahlfs:')), ures)

    def test_f92_magyar_szo_index(self):
        self.assertEqual(S.szo_kis('Kép,'), 'kép')
        self.assertEqual(S.szo_kis('Isten-s'), 'istens')
        for sql in ("SELECT * FROM token_karoli WHERE szo_kis='kép'",
                    "SELECT * FROM token_par WHERE hu_szo_kis='kép'",
                    "SELECT a.igehely FROM token_karoli a JOIN token_karoli b ON a.igehely=b.igehely "
                    "AND a.oldal=b.oldal AND b.sorszam=a.sorszam+1 WHERE a.szo_kis='segítségül' AND b.szo_kis='hív'"):
            terv = ' '.join(r[3] for r in self.con.execute('EXPLAIN QUERY PLAN ' + sql))
            self.assertIn('USING', terv, sql)
            self.assertIn('INDEX', terv, sql)
        for szo, kis in self.con.execute('SELECT szo, szo_kis FROM token_karoli LIMIT 2000'):
            self.assertEqual(S.szo_kis(szo), kis)
        for szo, kis in self.con.execute('SELECT hu_szo, hu_szo_kis FROM token_par LIMIT 2000'):
            self.assertEqual(S.szo_kis(szo), kis)

    # -- F95: szotari alak (DT-F95a) -----------------------------------------------------------
    def _szoto_tsv(self):
        return G.tsv_beolvas(os.path.join(ROOT, 'adat', 'szoto', 'karoli_szotari_alak.tsv'))[1]

    def test_f95_szotari_alak_sorszam_licenc_hash(self):
        sorok = self._szoto_tsv()
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM szotari_alak').fetchone()[0], len(sorok))
        # a Karoli valodi *alak* szava nem veszik el fejlecnek
        self.assertEqual(self.con.execute("SELECT szotari_alak FROM szotari_alak WHERE alak='alak'").fetchall(),
                         [('alak',)])
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM szotari_alak WHERE modszer='simplemma'").fetchone()[0], 0)
        for t in ('szotari_alak', 'szotari_kereso', 'szotari_token_kotojeles'):
            self.assertEqual(self.con.execute('SELECT COUNT(*) FROM tabla_licenc WHERE tabla=?', (t,)).fetchone()[0], 1, t)
        self.assertEqual(self.con.execute("SELECT licenc_dataset FROM tabla_licenc WHERE tabla='szotari_alak'").fetchone()[0],
                         'szoto_tablak')
        meta = dict(self.con.execute('SELECT kulcs, ertek FROM meta').fetchall())
        self.assertEqual(meta['szotari_alak:forras_sor'], str(len(sorok)))
        self.assertTrue(meta['hash:szotari_alak'].startswith('%d|' % len(sorok)))
        db, h = S.tablak_hash(self.a)['szotari_alak']
        self.assertEqual((db, h), (len(sorok), meta['hash:szotari_alak'].split('|')[1]))

    def test_f95_kereso_negy_mezo(self):
        sorok = self._szoto_tsv()
        n = self.con.execute('SELECT COUNT(*) FROM szotari_kereso').fetchone()[0]
        self.assertGreaterEqual(n, len(sorok))
        ures = self.con.execute("SELECT COUNT(*) FROM szotari_kereso WHERE keresoalak='' OR mezok=''").fetchone()[0]
        self.assertEqual(ures, 0)
        # mind a negy mezo kereshető: szotari, mai, alapige, tovabbi
        mezok = ' '.join(m for (m,) in self.con.execute('SELECT DISTINCT mezok FROM szotari_kereso'))
        for m in ('szotari', 'mai', 'alapige', 'tovabbi'):
            self.assertIn(m, mezok)
        # a nagybetus lemma kisbetus keresessel is megvan
        self.assertGreater(self.con.execute(
            "SELECT COUNT(*) FROM szotari_kereso k JOIN szotari_alak a ON a.alak=k.alak "
            "WHERE k.keresoalak='isten' AND a.szotari_alak='Isten'").fetchone()[0], 0)

    def test_f95_index_hasznalat(self):
        for sql in ("SELECT * FROM szotari_alak WHERE alak='Isten'",
                    "SELECT * FROM szotari_alak WHERE szotari_alak='ember'",
                    "SELECT * FROM szotari_kereso WHERE keresoalak='ember'",
                    "SELECT t.igehely, t.sorszam FROM szotari_kereso k JOIN token_karoli t ON t.szo=k.alak "
                    "AND t.oldal='hu' WHERE k.keresoalak='ember'"):
            terv = ' '.join(r[3] for r in self.con.execute('EXPLAIN QUERY PLAN ' + sql))
            self.assertIn('INDEX', terv, sql)
            self.assertNotIn('SCAN t', terv, sql)
            self.assertNotIn('SCAN k', terv, sql)
            self.assertNotIn('SCAN szotari_alak', terv, sql)

    def test_f95_kotojeles_segedtabla(self):
        meta = dict(self.con.execute('SELECT kulcs, ertek FROM meta').fetchall())
        db = self.con.execute('SELECT COUNT(*) FROM szotari_token_kotojeles').fetchone()[0]
        self.assertGreater(db, 0)
        # minden darab egy kotojeles alakhoz tartozik, es a tokenek a token_karoli-ban megvannak
        rossz = self.con.execute(
            "SELECT COUNT(*) FROM szotari_token_kotojeles k WHERE k.alak NOT LIKE '%-%' OR NOT EXISTS "
            "(SELECT 1 FROM token_karoli t WHERE t.igehely=k.igehely AND t.oldal='hu' AND t.sorszam=k.sorszam)").fetchone()[0]
        self.assertEqual(rossz, 0)
        nem_pontos = self.con.execute('SELECT COUNT(DISTINCT igehely||sorszam) FROM szotari_token_kotojeles '
                                      'WHERE pontos_talalat=0').fetchone()[0]
        self.assertEqual(str(nem_pontos), meta['szotari_token:kotojeles_feloldott_nem_pontos'])
        # a pontos talalat nelkuli hu tokenek = a feloldottak + a feloldhatatlanok
        self.assertEqual(int(meta['szotari_token:pontos_alak_nem_talal']),
                         nem_pontos + int(meta['szotari_token:nem_oldodik_fel']))
        alakok = {r['alak'] for r in self._szoto_tsv()}
        nem = [szo for (szo,) in self.con.execute("SELECT szo FROM token_karoli WHERE oldal='hu'") if szo not in alakok]
        self.assertEqual(len(nem), int(meta['szotari_token:pontos_alak_nem_talal']))

    def test_f95_frissesseg_d5_felveszi_a_forras_tsv_t(self):
        sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'olvaso_pilot'))
        import db_meres as DM
        rel = 'adat/szoto/karoli_szotari_alak.tsv'
        for t in ('szotari_alak', 'szotari_kereso', 'szotari_token_kotojeles'):
            self.assertIn(rel, DM.TSV_FORRAS[t])
            self.assertIn(t, DM.D5_TOVABBI)
        self.assertEqual(DM.EGYEZO_SORSZAM['szotari_alak'], rel)
        # a D5 sorszam-szamlalasa (# sorok es fejlec nelkul) = a minta meta-sora
        self.assertEqual(str(DM.tsv_sorok(rel)),
                         dict(self.con.execute('SELECT kulcs, ertek FROM meta')).get('szotari_alak:forras_sor'))


class FeliratHalmaz(unittest.TestCase):
    """F91 E2: az egyetlen, Karoli+KJV verszamokbol szamolt felirat-halmaz (zsolt_felirat_halmaz.py)."""

    def test_halmaz_67_vers_63_zsoltar(self):
        import zsolt_felirat_halmaz as ZFH
        self.assertEqual(ZFH.onellenorzes(), (67, 63))
        d = ZFH.felirat_d()
        self.assertEqual(sorted(c for c, x in d.items() if x == 2), [51, 52, 54, 60])
        self.assertIn('Zsolt 13:1', ZFH.felirat_versek())      # az etalon szerinti kivetel
        self.assertNotIn('Zsolt 13:2', ZFH.felirat_versek())

    def test_a_tabla_felirat_sorai_a_halmaz(self):
        # az A-tabla (Karoli_versmegfeleltetes.tsv) `felirat` megjegyzesu sorai = a halmaz (fogyaszto, nem forras)
        import zsolt_felirat_halmaz as ZFH
        sorok = G.tsv_beolvas(os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv'))[1]
        a = {r['igehely_karoli'] for r in sorok if r['igehely_karoli'].startswith('Zsolt ')
             and r['megjegyzes'].startswith('felirat')}
        self.assertEqual(a, set(ZFH.felirat_versek()))

    def test_a_felirat_versnek_nincs_terkep_erteke_a_db_ben(self):
        ok = kezi_mt_or_kihagy()   # F117.8 (6): csak az őr (DT-F117f) helyzetében kihagyva, kimondott okkal
        if ok:
            self.skipTest(ok)
        import zsolt_felirat_halmaz as ZFH
        tmp = tempfile.mkdtemp()
        try:
            ki = os.path.join(tmp, 'f.db')
            self.assertEqual(S.main(['--mod', 'minta', '--kimenet', ki]), 0)
            con = sqlite3.connect(ki)
            rossz = [ig for (ig, t) in con.execute("SELECT karoli_igehely, terkep_ertek FROM lxx_versszam")
                     if ig in ZFH.felirat_versek() and t]
            con.close()
            self.assertEqual(rossz, [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)



class OshlGyokcsalad(unittest.TestCase):
    """F99 M1: az OSHL-index gyökcsalád-oszlopai (etym_tipus, etym_cel, gyok) a pardes.db-be kerülnek, oshl_id-indexszel;
    a darabszámok egyeznek az M0.4 mérésével (naplok/BDB_SZELETELO_M0.md 5. szakasz)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        e = S.Epito(S.ROOT, os.path.join(cls.tmp, 'o.db'), 'teljes')
        e.con = sqlite3.connect(':memory:')
        _, licencsorok = G.tsv_beolvas(os.path.join(e.adat, 'licencek.tsv'))
        e.licencek = {r['dataset']: r for r in licencsorok}
        e._altalanos_betolt('oshl_lexikalis_index', 'konkordancia/OSHL_lexikalis_index.tsv', 'strong', None, ['OSHL'])
        cls.con = e.con

    @classmethod
    def tearDownClass(cls):
        cls.con.close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_az_uj_oszlopok_a_tablaban(self):
        oszl = [r[1] for r in self.con.execute('PRAGMA table_info(oshl_lexikalis_index)')]
        for o in ('etym_tipus', 'etym_cel', 'gyok'):
            self.assertIn(o, oszl)

    def test_darabszamok_az_m0_meres_szerint(self):
        db = dict(self.con.execute('SELECT etym_tipus, COUNT(*) FROM oshl_lexikalis_index GROUP BY etym_tipus'))
        self.assertEqual(db, {'main': 2643, 'sub': 4368, 'single': 574, '—': 2636})
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM oshl_lexikalis_index WHERE etym_tipus='main' AND gyok<>'—'").fetchone()[0], 2458)

    def test_oshl_id_index(self):
        ix = [r[0] for r in self.con.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='oshl_lexikalis_index'")]
        self.assertTrue(any('oshl_id' in (x or '') for x in ix), ix)

    def test_minta_h1242_csaladja(self):
        cel = self.con.execute("SELECT etym_tipus, etym_cel FROM oshl_lexikalis_index WHERE strong='H1242'").fetchone()
        self.assertEqual(cel, ('sub', 'bxk'))
        gy = self.con.execute("SELECT strong, etym_tipus, etym_cel FROM oshl_lexikalis_index WHERE oshl_id='bxk'").fetchone()
        self.assertEqual(gy[0], 'H1239')
        self.assertEqual(gy[1], 'main')
        self.assertEqual(set(gy[2].split(',')), {'blz', 'bxl', 'bxm', 'bxn', 'bxo'})

    def test_minta_h3915_nincs_csalad(self):
        self.assertEqual(self.con.execute("SELECT etym_tipus FROM oshl_lexikalis_index WHERE strong='H3915'").fetchone()[0], 'single')


class F140Licenc(unittest.TestCase):
    """F140 (K8, DT-F140b): a `glosszak_heber_hu` tabla licenc-bejegyzese; az epites nem kell hozza (az Integracio
    osztaly az N-F117a-ig kihagyott), a bejegyzes es a feloldas kozvetlenul vizsgalhato."""

    def test_glosszak_heber_hu_tbesh_tahot_forrasjelolessel(self):
        self.assertEqual(S.ADAT_LICENC['glosszak_heber_hu'], ['TBESH', 'TAHOT', 'projekt_adat'])
        _, licencsorok = S.G.tsv_beolvas(os.path.join(ROOT, 'adat', 'licencek.tsv'))
        tmp = tempfile.mkdtemp()
        try:
            ep = S.Epito(ROOT, os.path.join(tmp, 'k8.db'), 'minta')
            ep.licencek = {r['dataset']: r for r in licencsorok}
            allapot, kereskedelmi, dataset, cimke = ep.licenc_feloldas(S.ADAT_LICENC['glosszak_heber_hu'])
            for k in ('TBESH', 'TAHOT', 'projekt_adat'):
                self.assertIn(k, dataset)
            self.assertIn('CC BY 4.0', cimke)
            # a sima projekt_adat nem hordozza a forrasjelolest: a bejegyzes nelkul ez toltodne be
            self.assertNotIn('CC BY 4.0', ep.licenc_feloldas(['projekt_adat'])[3])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=1)
