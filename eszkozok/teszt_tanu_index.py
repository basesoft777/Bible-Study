#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_tanu_index.py -- F191: az eszkozok/tanu_index.py tesztjei.

    python eszkozok/teszt_tanu_index.py
    python -m unittest eszkozok/teszt_tanu_index.py

Egy kis szintetikus HCF-sqlite-ot es egy kis Sefaria-links CSV-t epit egy ideiglenes konyvtarba (a repon kivulre), azon
ellenorzi az atvezetest, a tartomany-ertelmezest, azt, hogy az idezetszoveg NEM kerul az indexbe, valamint a repoban levo
kesz tablak fejleceit, oszlopszamat es a HAMART-minta darabszamait.
"""
import os
import sqlite3
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tanu_index as T  # noqa: E402

IDEZET = 'EZ AZ IDEZET SZOVEGE NEM KERULHET AZ INDEXBE'


class KulcsTeszt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = T.Kulcs()

    def test_kjv_zsoltar_felirat_eltolas(self):
        # Károli Zsolt 3:2 = KJV 3:1 (a felirat a Károlinál 3:1)
        self.assertEqual(self.k.atvezet('Zsolt', 3, 1, 'kjv')[:2], (3, 2))

    def test_egyezo_vers(self):
        self.assertEqual(self.k.atvezet('1Móz', 3, 17, 'kjv'), (3, 17, 'egyezo'))
        self.assertEqual(self.k.atvezet('1Móz', 3, 17, 'mt'), (3, 17, 'egyezo'))

    def test_nt_feltetelezett(self):
        self.assertEqual(self.k.atvezet('Róm', 5, 12, 'kjv'), (5, 12, 'nt_feltetelezett'))

    def test_mt_joel_4(self):
        # a Jóel Károli 3:1 az MT 4:1 megfelelője
        self.assertEqual(self.k.atvezet('Jóel', 4, 1, 'mt')[:2], (3, 1))

    def test_szelesseg(self):
        self.assertEqual(self.k.szelesseg('1Móz', 3, 17, 3, 17), 1)
        self.assertEqual(self.k.szelesseg('1Móz', 3, 17, 3, 19), 3)
        self.assertEqual(self.k.szelesseg('1Móz', 3, 23, 4, 2), 2 + 2)   # 3:23, 3:24, 4:1, 4:2

    def test_igehely_parse(self):
        self.assertEqual(T.igehely_parse('1Móz 3:17'), ('1Móz', 3, 17))
        with self.assertRaises(ValueError):
            T.igehely_parse('1Móz 3')


class SefariaRefTeszt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = T.Kulcs()

    def r(self, s):
        return T.sefaria_tanakh_ref(s, self.k)

    def test_egy_vers(self):
        self.assertEqual(self.r('Genesis 3:17'), ('Gen', 3, 17, 3, 17))

    def test_vers_tartomany(self):
        self.assertEqual(self.r('Genesis 3:17-19'), ('Gen', 3, 17, 3, 19))

    def test_fejezethatar_tartomany(self):
        self.assertEqual(self.r('Genesis 3:17-4:2'), ('Gen', 3, 17, 4, 2))

    def test_fejezet(self):
        self.assertEqual(self.r('Genesis 3'), ('Gen', 3, 1, 3, self.k.chmax[('1Móz', 3)]))

    def test_fejezet_mt_hossz(self):
        # Jóel MT 3 = 5 vers (Károli Jóel 2:28–32): a fejezet vége az MT-hossz, nem a Károli-fejezeté
        self.assertEqual(self.r('Joel 3'), ('Jol', 3, 1, 3, 5))

    def test_nem_tanakh(self):
        self.assertIsNone(self.r('Bereshit Rabbah 20:10'))
        self.assertIsNone(self.r('Abarbanel on Amos 1:1:10'))

    def test_osszetett_nev(self):
        self.assertEqual(self.r('I Samuel 1:1')[0], '1Sa')
        self.assertEqual(self.r('Song of Songs 2:1')[0], 'Sng')


class EpitesTeszt(unittest.TestCase):
    def test_atyak_szoveg_nelkul(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, 'c.sqlite')
            con = sqlite3.connect(db)
            con.execute('create table father_meta (name, default_year, wiki_url, father_category, condemned_by_council)')
            con.execute('create table commentary (id, father_name, file_name, append_to_author_name, ts, book, '
                        'location_start, location_end, txt, source_url, source_title)')
            con.execute("insert into father_meta values ('Bede','735','u','Western & Medieval Theology',0)")
            rows = [
                ('a1a1a1a1a1-0001', 'Bede', 'f1', '', 735, 'genesis', 3000017, 3000017, IDEZET, 'http://x/1', 'Mű 1'),
                ('a2a2a2a2a2-0002', 'Bede', 'f2', '', 735, 'psalms', 3000001, 3000002, IDEZET, '', 'Zsolt'),
                ('a3a3a3a3a3-0003', 'Bede', 'f3', '', 735, 'wisdom', 1000001, 1000001, IDEZET, '', 'Apokrif'),
                ('bbbbbbbbbb-0004', 'Bede', 'f4', '', 735, 'romans', 5000012, 5000012, IDEZET, '', ''),
            ]
            con.executemany('insert into commentary values (?,?,?,?,?,?,?,?,?,?,?)', rows)
            con.commit()
            con.close()
            ki = os.path.join(d, 'atyak.tsv')
            n, kimarad, konyvek = T.epit_atyak(db, ki, '2026-11-11')
            self.assertEqual(n, 3)
            self.assertEqual(kimarad['nem_kanonikus_konyv'], 1)
            self.assertEqual(konyvek, {'wisdom': 1})
            for p in (ki, os.path.join(d, 'Tanu_atyak_mu.tsv')):
                with open(p, encoding='utf-8') as f:
                    self.assertNotIn(IDEZET, f.read())
            _, sorok = T.betolt(ki)
            self.assertEqual(len(sorok), 3)
            zs = [s for s in sorok if s['igehely_kezdet'].startswith('Zsolt')][0]
            self.assertEqual((zs['igehely_kezdet'], zs['igehely_veg']), ('Zsolt 3:2', 'Zsolt 3:3'))
            self.assertEqual(zs['atvezetes'], 'tabla')
            self.assertEqual(len(zs['hcf_id']), 10)
            for s in sorok:
                self.assertEqual(len(s), len(T.ATYAK_OSZLOPOK))

    def test_rabbinikus_szuro_es_csoportositas(self):
        import csv
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'links0.csv')
            with open(p, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerow(['Citation 1', 'Citation 2', 'Conection Type', 'Text 1', 'Text 2', 'Category 1', 'Category 2'])
                # Midrash, ket ref ugyanarra a (vers, mu) parra -> egy sor, darab=2
                w.writerow(['Bereshit Rabbah 20:10', 'Genesis 3:17', '', 'Bereshit Rabbah', 'Genesis', 'Midrash', 'Tanakh'])
                w.writerow(['Genesis 3:17', 'Bereshit Rabbah 20:11', '', 'Genesis', 'Bereshit Rabbah', 'Tanakh', 'Midrash'])
                # kozepkori kommentar a Talmudra: a Tanakh-oldal nem csupasz konyvnev -> kimarad
                w.writerow(['Abarbanel on Amos 1:1:10', 'Shabbat 92a:8', '', 'Abarbanel on Amos', 'Shabbat', 'Tanakh', 'Talmud'])
                # Targum
                w.writerow(['Onkelos Genesis 3:17', 'Genesis 3:17', 'targum', 'Onkelos Genesis', 'Genesis', 'Tanakh', 'Tanakh'])
                # nem rabbinikus kategoria
                w.writerow(['Tanya 1:1', 'Genesis 3:17', '', 'Tanya', 'Genesis', 'Chasidut', 'Tanakh'])
            ki = os.path.join(d, 'rabb.tsv')
            n, stat, _ = T.epit_rabb(d, ki, '2026-11-11', motivum_szukites=False)
            self.assertEqual(n, 2)
            _, sorok = T.betolt(ki)
            by = {s['kategoria']: s for s in sorok}
            self.assertEqual(by['Midrash']['darab'], '2')
            self.assertEqual(by['Midrash']['hely'], 'Bereshit Rabbah 20:10 ; Bereshit Rabbah 20:11')
            self.assertEqual(by['Targum']['mu'], 'Onkelos Genesis')
            self.assertEqual(by['Midrash']['igehely_kezdet'], '1Móz 3:17')
            self.assertEqual(by['Midrash']['igehely_veg'], '')

    def test_motivum_versek(self):
        k = T.Kulcs()
        kulcsok, rossz = T.motivum_versek(k)
        self.assertEqual(rossz, [])
        self.assertIn(k.rendkulcs('1Móz', 3, 17), kulcsok)


class KeszTablaTeszt(unittest.TestCase):
    """A repoban levo, generalt tablak (kell hozzajuk a konkordancia/Tanu_*.tsv)."""

    @classmethod
    def setUpClass(cls):
        cls.k = T.Kulcs()
        cls.oa, cls.a = T.betolt(T.ATYAK_TSV)
        cls.orab, cls.r = T.betolt(T.RABB_TSV)
        cls.om, cls.mu = T.betolt(T.MU_TSV)

    def test_oszlopok(self):
        self.assertEqual(self.oa, T.ATYAK_OSZLOPOK)
        self.assertEqual(self.orab, T.RABB_OSZLOPOK)
        self.assertEqual(self.om, T.MU_OSZLOPOK)

    def test_fejlec_proveniencia_es_licenc(self):
        for p in (T.ATYAK_TSV, T.RABB_TSV):
            with open(p, encoding='utf-8') as f:
                fej = ''.join(l for l in f if l.startswith('#'))
            self.assertIn('# GENERÁLT:', fej)
            self.assertIn('proveniencia: scope=', fej)
            self.assertIn('licenc:', fej)
            self.assertIn('sha256', fej)

    def test_mu_id_feloldhato(self):
        ids = {m['mu_id'] for m in self.mu}
        self.assertTrue(all(s['mu_id'] in ids for s in self.a))

    def test_nincs_hosszu_mezo(self):
        # egy idezetszoveg-szivargas hosszu mezot adna; a leghosszabb legitim mezo (mu-cim, URL) ennel rovidebb
        for s in self.a[:20000] + self.r:
            self.assertTrue(all(len(v) < 3000 for v in s.values()))
        self.assertTrue(all(len(v) < 3000 for m in self.mu for v in m.values()))

    def test_hamart_minta_atyak(self):
        # a felmeres szerinti pontos egyvers-darabszamok (HCF 2026-11-11)
        for vers, n in (('1Móz 3:17', 8), ('1Móz 4:7', 4), ('1Móz 4:11', 2), ('1Móz 6:5', 2), ('1Móz 6:11', 1)):
            pont = {s['atya'] for s in self.a if s['igehely_kezdet'] == vers and not s['igehely_veg']}
            self.assertEqual(len(pont), n, vers)

    def test_hamart_minta_rabbinikus(self):
        for vers in T.HAMART_VERSEK:
            pont = [s for s in self.r if s['igehely_kezdet'] == vers and not s['igehely_veg']]
            self.assertGreater(len(pont), 5, vers)
            self.assertTrue({s['kategoria'] for s in pont} <= {'Midrash', 'Talmud', 'Mishnah', 'Tosefta', 'Targum'})

    def test_fedo_sorok(self):
        a = T.fedo_sorok(self.a, '1Móz 3:18', self.k)
        self.assertTrue(any(s['atya'] == 'Ambrosiaster' for s in a))   # 3:17-18 tartomany


if __name__ == '__main__':
    unittest.main(verbosity=2)
