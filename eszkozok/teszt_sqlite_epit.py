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
  determinizmus (G2), licenc-oszlopok (G6), `kapcsolodas` idezojelei (split-korut), G3
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


def sertett_szabalyok(sertesek):
    return sorted(s.cim.split('.')[0] for s in sertesek)


class Pozitiv(unittest.TestCase):
    def test_mai_adat_zold(self):
        sorok, sertesek = S.integritas(os.path.join(ROOT, 'adat'))
        self.assertEqual(sertesek, [], [s.sor_szoveg() for s in sertesek])
        self.assertEqual(len(sorok), 12)

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
                  'szabaly7_', 'szabaly8_', 'szabaly9_', 'szabaly10_', 'szabaly11_', 'szabaly13_'):
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


class Integracio(unittest.TestCase):
    """A kis minta ketszeri epitese (G2), licenc-oszlopok (G6), normalizalas, idezojelek."""

    @classmethod
    def setUpClass(cls):
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

    def test_g6_licenc_oszlopok_kitoltve(self):
        for (n,) in self.con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                     "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'fts_motivum_%'").fetchall():
            ures = self.con.execute('SELECT COUNT(*) FROM "%s" WHERE IFNULL(licenc_allapot,"")="" '
                                    'OR IFNULL(kereskedelmi,"")="" OR IFNULL(licenc_dataset,"")=""' % n).fetchone()[0]
            self.assertEqual(ures, 0, n)

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
            r = self.con.execute('SELECT DISTINCT licenc_dataset, licenc_allapot, kereskedelmi FROM "%s"' % t).fetchall()
            self.assertEqual(r, [(t, 'tisztazott', 'igen')])
        r = self.con.execute('SELECT DISTINCT licenc_dataset FROM motivumok').fetchall()
        self.assertEqual(r, [('projekt_adat',)])

    def test_tagnt_karoli_vers_nelkuli_kulcsok(self):
        nevek = {r[0] for r in self.con.execute(
            "SELECT nyers FROM normalizalas_jelentes WHERE tabla='TAGNT_kivonat.tsv'")}
        self.assertTrue({'Róm 3:31', '1Kor 3:23', 'Róm 8:39'} <= nevek)

    def test_kjv_es_tbes_betoltve(self):
        for t in ('kjv', 'tbesg', 'tbesh'):
            self.assertGreater(self.con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0], 1000, t)

    def test_probak_megegyeznek(self):
        for p in S.probak(self.a, ROOT):
            self.assertTrue(p['ok'], '%s: %s' % (p['pont'], p['megj']))


if __name__ == '__main__':
    unittest.main(verbosity=1)
