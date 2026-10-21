#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_general_ellenorzo.py -- F11 M2 (FELADATOK #11): a `general.py`
ellenorzo jeloloinek (ADAT-HIV: DT-F11d (b); ADAT-ÉRTÉK: DT-F11d (c)) es a
SEMA-kulcsok levezetesenek (sema_kulcsok(), F11.M2.11) tesztjei.

A kitalalt adattablak es a kitalalt SEMA ideiglenes, repon kivuli
konyvtarban allnak (tempfile); az eles adat/SEMA.md-t a teszt csak olvassa.
Futtatas: python eszkozok/teszt_general_ellenorzo.py
"""

import io
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ESZKOZOK)
import general as G  # noqa: E402

LEX = ('# próba\n'
       'strong\tszotar\tentry_id\tjelentes_szam\tszoveg_en\tforrasfajl\n'
       'H7121\tBDB\tH7121\t1\tcall\tx.tsv\n'
       'H7121\tBDB\tH7121\t2\tproclaim\tx.tsv\n'
       'H8034\tBDB\tH8034\t1\tname\tx.tsv\n'
       'H8034\tBDB\tH8034\t1\tname (duplikált)\tx.tsv\n')
ELOF = ('id\tigehely\tfo_elofordulas\tgerinc_elem\n'
        'PROBA-001\t1Móz 4:26\tA\tH7121\n'
        'PROBA-001\tZsolt 116:4\tA\tH7121\n'
        'PROBA-001\tJóel 2:32\tB\tH7121\n'
        'PROBA-001\tRóm 10:13\t\tG1941\n'
        'MAS-001\tMt 1:1\tC\tX\n')

POZITIV = [
    '<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotar=BDB; strong=H7121; entry_id=H7121; jelentes_szam=2 -->',
    '<!-- ADAT-HIV: adat/elofordulasok.tsv | igehely=Zsolt 116:4; id=PROBA-001 -->',
    'Négy sor: 4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->, két csoport: '
    '2<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count_distinct(fo_elofordulas; id=PROBA-001) -->.',
    'A H7121-en: 3<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001; gerinc_elem=H7121) -->',
]

NEGATIV = {
    'elírt mezőnév (b)': ('<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotr=BDB; strong=H7121; '
                          'entry_id=H7121; jelentes_szam=1 -->', 'elírt mezőnév'),
    'nulla egyező sor (b)': ('<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotar=BDB; strong=H7121; '
                             'entry_id=H7121; jelentes_szam=9 -->', '0 egyező sor'),
    'két egyező sor (b)': ('<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotar=BDB; strong=H8034; '
                           'entry_id=H8034; jelentes_szam=1 -->', '2 egyező sor'),
    'hiányos kulcs (b)': ('<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotar=BDB; strong=H7121 -->',
                          'hiányzik: entry_id, jelentes_szam'),
    'kulcson kívüli mező (b)': ('<!-- ADAT-HIV: elofordulasok.tsv | id=PROBA-001; igehely=1Móz 4:26; '
                                'gerinc_elem=H7121 -->', 'kulcson kívüli: gerinc_elem'),
    'kulcs nélküli tábla (b)': ('<!-- ADAT-HIV: auditok.tsv | id=PROBA-001 -->', 'nincs SEMA-kulcsa'),
    'nem mező=érték alak (b)': ('<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | BDB H7121 -->', 'rossz kulcs-alak'),
    'ismeretlen függvény (c)': ('5<!-- ADAT-ÉRTÉK: elofordulasok.tsv | sum(id=PROBA-001) -->',
                                'ismeretlen kifejezés'),
    'kódfuttatási kísérlet (c)': ('5<!-- ADAT-ÉRTÉK: elofordulasok.tsv | __import__(os) -->',
                                  'ismeretlen kifejezés'),
    'eltérő érték (c)': ('5<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                         'a prózában 5, a táblából számolt 4'),
    'nem karakterre egyező érték (c)': ('04<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                                        'eltérő érték'),
    'rossz szűrő: = nélkül (c)': ('4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id) -->', 'rossz szűrő'),
    'rossz szűrő: nem létező mező (c)': ('4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(idd=PROBA-001) -->',
                                         'rossz szűrő'),
    'rossz szűrő: count_distinct mező (c)': (
        '2<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count_distinct(nincs; id=PROBA-001) -->', 'rossz szűrő'),
    'üres szűrő (c)': ('4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count() -->', 'rossz szűrő'),
    'tört érték 2.5 (M2.11)': ('2.5<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                               'nem nemnegatív egész'),
    'tört érték 1,5 (M2.11)': ('1,5<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                               'nem nemnegatív egész'),
    'negatív érték -4 (M2.11)': ('-4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                                 'nem nemnegatív egész'),
    'betű előtte P4 (M2.11)': ('P4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                               'nem nemnegatív egész'),
    'összetett kifejezés (M2.11)': ('8<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001)'
                                    '+count(id=PROBA-001) -->', 'ismeretlen kifejezés'),
    'zárójel az argumentumban (M2.11)': ('4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=(PROBA-001)) -->',
                                         'ismeretlen kifejezés'),
    'hiányzó érték (c)': ('Szám: <!-- ADAT-ÉRTÉK: elofordulasok.tsv | count(id=PROBA-001) -->',
                          'nincs egész szám'),
}

VART_KULCSOK = {
    'motivumok.tsv': ('id',), 'elofordulasok.tsv': ('id', 'igehely'),
    'kapcsolatok.tsv': ('forras_igehely', 'cel_igehely', 'id'),
    'jeloltek.tsv': ('id', 'igehely', 'jelolt_tipus', 'cel_id'),  # DT-F127b
    'motivum_kapcsolatok.tsv': ('id_a', 'igehely_a', 'id_b', 'igehely_b'),  # DT-F127b, SEMA 2.33
    'lexikon_hivatkozasok.tsv': ('szotar', 'strong', 'entry_id', 'jelentes_szam'),
    'dontes_hatas.tsv': ('dontes_forras', 'erintett_fajl', 'tilos_minta'),
    'kiejtes_szabalyok.tsv': ('sorszam',), 'kiejtes_kivetelek.tsv': ('nyelv', 'alak'),
    'bdb_igehely_javitas.tsv': ('strong', 'forras_hivatkozas'),
    'bdb_aranyminta.tsv': ('strong', 'szakasz', 'resz', 'utvonal', 'szint'),
    'bdb_vers_jelentes.tsv': ('strong', 'sorszam'),
    'bdb_karoli.tsv': ('strong', 'tipus', 'karoli_alak'),
}


class EllenorzoJelolok(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='teszt_ellenorzo_')
        for nev, tartalom in (('lexikon_hivatkozasok.tsv', LEX), ('elofordulasok.tsv', ELOF),
                              ('auditok.tsv', 'id\tx\nPROBA-001\t1\n')):
            with io.open(os.path.join(cls.tmp, nev), 'w', encoding='utf-8', newline='') as f:
                f.write(tartalom)
        cls.ks = G.konyv_sorrend_betolt()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def fut(self, sor):
        return G.kinyeres_elemez('## 2. X\n\n' + sor + '\n', 'PROBA-001', [], self.ks, '2026.10.18',
                                 adat_konyvtar=self.tmp)

    def test_pozitiv(self):
        e = self.fut('\n'.join(POZITIV))
        self.assertEqual(e['hibak'], [])
        self.assertEqual(len(e['ellenorzo']), 5)
        self.assertTrue(all(x['allapot'] == 'rendben' for x in e['ellenorzo']), e['ellenorzo'])

    def test_negativ(self):
        self.assertEqual(len(NEGATIV), 22)
        for nev, (sor, vart) in NEGATIV.items():
            with self.subTest(eset=nev):
                e = self.fut(sor)
                self.assertEqual(len(e['hibak']), 1, e['hibak'])
                self.assertIn(vart, e['hibak'][0])


class SemaKulcsok(unittest.TestCase):

    def test_eles_sema(self):
        k = G.sema_kulcsok()
        for t, v in VART_KULCSOK.items():
            with self.subTest(tabla=t):
                self.assertEqual(k.get(t), v)
        for t in ('auditok.tsv', 'karoli_variancia.tsv', 'forditas_ubs.tsv'):
            with self.subTest(kulcs_nelkul=t):
                self.assertNotIn(t, k)
        # F127: 23 (a main-en a #127 előtt már 22 volt -- a 21-es elvárás elavult --,
        # a #127 a motivum_kapcsolatok.tsv-vel (SEMA 2.33) egyet ad hozzá)
        self.assertEqual(len(k), 23)

    def test_kitalalt_sema(self):
        tmp = tempfile.mkdtemp(prefix='teszt_sema_')
        try:
            ut = os.path.join(tmp, 'SEMA.md')
            with io.open(ut, 'w', encoding='utf-8') as f:
                f.write('## 2. Táblák\n\n### 2.1 `uj_tabla.tsv` — x\n\nKulcs: `a` + `b`. Szöveg `c`.\n\n'
                        '### 2.2 `kulcstalan.tsv`\n\nKulcs **nincs**.\n\n'
                        '### 2.3 `volt.tsv`\n\nKulcs (volt): `x`.\n')
            k = G.sema_kulcsok(ut)
            self.assertEqual(k.get('uj_tabla.tsv'), ('a', 'b'))
            self.assertNotIn('kulcstalan.tsv', k)
            self.assertNotIn('volt.tsv', k)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
