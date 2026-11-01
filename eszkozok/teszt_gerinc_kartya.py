#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gerinc_kartya.py -- F124: a gerinc_kartya.py tesztjei (szintetikus adaton:
0 talalat, osszetett gerinc egy taggal, tag Strong szuroval es szuro nelkul,
--osszevet mindket listaja uresen is, --ir sorosszevetes) es a jelolt.py-val
valo egyezes a valos adaton (5 szakasz).

    python eszkozok/teszt_gerinc_kartya.py
"""

import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerinc_kartya as K  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = '2026-01-01T00:00Z'


def v(tahot=(), tagnt=()):
    return {'tahot': [{'strong': s, 'gloss': g} for s, g in tahot],
            'tagnt': [{'strong': s, 'gloss': g} for s, g in tagnt]}


MOTIVUMOK = [{'id': 'KIRALY-001', 'azonossag_tipusa': 'lexikai'},
             {'id': 'MENNY-001', 'azonossag_tipusa': 'lexikai'},
             {'id': 'ISTENTISZT-001', 'azonossag_tipusa': 'formulaikus'},
             {'id': 'HODIT-001', 'azonossag_tipusa': 'lexikai'}]


def elof(mid, igehely, strong, gerinc=None):
    return {'id': mid, 'igehely': igehely, 'strong': strong, 'gerinc_elem': gerinc or strong}


ELOF = [elof('KIRALY-001', '1Móz 1:20-21', 'H3548'),
        elof('MENNY-001', '1Móz 9:9', 'H1121+H0430'),
        elof('ISTENTISZT-001', '1Móz 9:9', 'H7121+H8034'),
        elof('HODIT-001', '1Móz 9:9', 'H7497'),
        # a gerinc_elem nem Strong: a `strong` oszlop a kulcs, es a cimke is az
        elof('HODIT-001', '1Móz 9:9', 'H8414+H0922', 'tohu+bohu'),
        ]

VERSEK = {
    ('1Móz', 1, 1): v(tahot=[('H3548', 'priest')]),                                  # egyszeru tag Strong: szuretlen_tag
    ('1Móz', 1, 2): v(tahot=[('H1121', 'son')]),                                     # egy_tag
    ('1Móz', 1, 3): v(tahot=[('H1121', 'sons'), ('H0430', 'God')]),                  # kollokacio
    ('1Móz', 1, 4): v(tahot=[('H7121', 'called'), ('H9003', 'on'), ('H8034', 'name'), ('H3068', 'LORD')]),
    ('1Móz', 1, 5): v(tahot=[('H8034', 'name')]),                                    # K0, kiszurve
    ('1Móz', 1, 6): v(tahot=[('H1111', 'x')]),                                       # nincs gerinc
    ('1Móz', 1, 7): v(tahot=[('H7497', 'giants')]),                                  # nem tag: szures ''
    ('1Móz', 1, 8): v(tahot=[('H9999', 'gram'), ('H8414', 'void')]),                 # H8414 egy_tag (H0922 nincs)
    ('1Móz', 1, 20): v(tahot=[('H3548', 'priest')]),                                 # tartomany szerint mar elofordulas
}
GRAMM = {'H9999'}
JELOLTEK = [{'id': 'HODIT-001', 'igehely': '1Móz 1:7', 'dontes': 'elutasítva'}]


def sorok(kulcsok=None, jeloltek=JELOLTEK):
    return K.kartya_sorok(VERSEK, GRAMM, MOTIVUMOK, ELOF, jeloltek, kulcsok)


def keres(ss, mid, vers, strong):
    return [s for s in ss if s['id'] == mid and s['igehely'] == '1Móz 1:%d' % vers and s['strong'] == strong]


class Kartya(unittest.TestCase):
    def test_tag_strong_szuretlen(self):
        s = keres(sorok(), 'KIRALY-001', 1, 'H3548')[0]
        self.assertEqual(s['szures'], 'szuretlen_tag')
        self.assertEqual(s['allapot'], 'új')

    def test_osszetett_egy_tag_es_kollokacio(self):
        ss = sorok()
        self.assertEqual(keres(ss, 'MENNY-001', 2, 'H1121')[0]['kollokacio'], 'egy_tag')
        self.assertEqual(keres(ss, 'MENNY-001', 3, 'H1121')[0]['kollokacio'], 'kollokáció')
        self.assertEqual(keres(ss, 'MENNY-001', 3, 'H0430')[0]['kollokacio'], 'kollokáció')

    def test_egyszeru_gerinc_nincs_kollokacio_jelzes(self):
        s = keres(sorok(), 'HODIT-001', 7, 'H7497')[0]
        self.assertEqual(s['kollokacio'], '')
        self.assertEqual(s['szures'], '')

    def test_szuro_atjut_es_kiszur(self):
        ss = sorok()
        a = keres(ss, 'ISTENTISZT-001', 4, 'H8034')[0]
        self.assertEqual((a['szures'], a['szures_ok']), ('atjutott', 'A_be_isten'))
        self.assertTrue(a['pozicionalis'])
        k = keres(ss, 'ISTENTISZT-001', 5, 'H8034')[0]
        self.assertEqual((k['szures'], k['szures_ok'], k['kollokacio']), ('kiszurve', 'K0_nincs_par', 'egy_tag'))

    def test_gerinc_elem_cimke_a_strong_oszlopbol(self):
        s = keres(sorok(), 'HODIT-001', 8, 'H8414')[0]
        self.assertEqual(s['gerinc_elem'], 'H8414+H0922')       # nem a magyar `tohu+bohu` cimke
        self.assertEqual(s['kollokacio'], 'egy_tag')

    def test_grammatikai_strong_kimarad(self):
        self.assertFalse([s for s in sorok() if s['strong'] == 'H9999'])

    def test_allapot_tartomany_es_jelolt(self):
        ss = sorok()
        self.assertEqual(keres(ss, 'KIRALY-001', 20, 'H3548')[0]['allapot'], 'már előfordulás')   # 1Móz 1:20-21
        self.assertEqual(keres(ss, 'HODIT-001', 7, 'H7497')[0]['allapot'], 'már jelölt: elutasítva')
        ss2 = sorok(jeloltek=[{'id': 'HODIT-001', 'igehely': '1Móz 1:7', 'dontes': 'nyitva'}])
        self.assertEqual(keres(ss2, 'HODIT-001', 7, 'H7497')[0]['allapot'], 'már jelölt: nyitva')

    def test_nulla_talalat(self):
        self.assertEqual(sorok([('1Móz', 1, 6)]), [])

    def test_proveniencia_nulla_talalatnal_is(self):
        prov = K.proveniencia('1Móz 1:6', VERSEK, GRAMM, ELOF, [], TS)
        self.assertTrue(prov[0].startswith('scope=range:1Móz 1:6 | forras='))
        self.assertIn('n=0', prov[0])
        for p in prov:
            self.assertIn('ts=%s' % TS, p)
            self.assertIn('scope=', p)
        # a szuro mindharom tagjara van sor, n=0-val is
        self.assertEqual(sum(1 for p in prov if 'szuro=DT283' in p), 3)

    def test_proveniencia_kollokacio_sor(self):
        ss = sorok([('1Móz', 1, 1), ('1Móz', 1, 2), ('1Móz', 1, 3)])
        prov = K.proveniencia('1Móz 1:1-3', VERSEK, GRAMM, ELOF, ss, TS)
        kol = [p for p in prov if 'strong=H1121+H0430' in p]
        self.assertEqual(len(kol), 1)
        self.assertIn('n=1', kol[0])      # csak az 1:3 vers hordozza mindket tagot

    def test_szoveg_szekciok(self):
        ss = sorok()
        prov = K.proveniencia('1Móz 1:1-20', VERSEK, GRAMM, ELOF, ss, TS)
        t = K.jelentes_szoveg('1Móz 1:1-20', ss, prov, TS)
        self.assertTrue(t.startswith('# GENERÁLT: gerinc_kartya.py'))
        self.assertIn('## Melléklet: a #110 szűrője által kiszűrt sorok', t)
        self.assertIn('kiszurve: K0_nincs_par', t)
        self.assertIn('`szuretlen_tag` sor', t)
        self.assertIn('## Proveniencia', t)

    def test_ures_szoveg_explicit(self):
        t = K.jelentes_szoveg('1Móz 1:6', [], K.proveniencia('1Móz 1:6', VERSEK, GRAMM, ELOF, [], TS), TS)
        self.assertIn('üres', t)


class Osszevetes(unittest.TestCase):
    BB = K.konyvenkent(VERSEK)

    @staticmethod
    def ks(*sorok_):
        return [{'tanulmany': 'genezis/X.md', 'igehely': ig, 'szo': szo, 'strong': st, 'datum': 'd'}
                for ig, szo, st in sorok_]

    def test_nincs_kulcsszo_sor(self):
        o = K.osszevet(sorok(), [], 'genezis/X.md', self.BB)
        self.assertFalse(o['van_kulcsszo'])
        t = K.jelentes_szoveg('x', sorok(), ['p'], TS, o, 'genezis/X.md')
        self.assertIn('nem végezhető el', t)

    def test_mindket_lista_ures(self):
        ss = [s for s in sorok() if s['szures'] != 'kiszurve']
        ks = self.ks(*[(s['igehely'], 'szó', s['strong']) for s in ss])
        o = K.osszevet(sorok(), ks, 'genezis\\X.md', self.BB)      # a visszajeles utvonal is egyezik
        self.assertTrue(o['van_kulcsszo'])
        self.assertEqual((o['kartya_nem_olvasas'], o['olvasas_nem_kartya']), ([], []))
        t = K.jelentes_szoveg('x', sorok(), ['p'], TS, o, 'genezis/X.md')
        self.assertIn('*(üres: a kártya minden sora szerepel a kulcsszó-táblázatban)*', t)
        self.assertIn('*(üres: minden kulcsszó egy meglévő gerinc-elemen áll)*', t)

    def test_kartya_talalt_olvasas_nem(self):
        ks = self.ks(('1Móz 1:1', 'pap', 'H3548'))
        o = K.osszevet(sorok(), ks, 'genezis/X.md', self.BB)
        ids = {(s['id'], s['igehely']) for s in o['kartya_nem_olvasas']}
        self.assertIn(('MENNY-001', '1Móz 1:3'), ids)
        self.assertNotIn(('KIRALY-001', '1Móz 1:1'), ids)
        self.assertEqual(o['olvasas_nem_kartya'], [])

    def test_olvasas_talalt_kartya_nem(self):
        ks = self.ks(('1Móz 1:6', 'kuszik', 'H1111'), ('1Móz 1:1', 'pap', 'H3548'))
        o = K.osszevet(sorok(), ks, 'genezis/X.md', self.BB)
        self.assertEqual([k['strong'] for k in o['olvasas_nem_kartya']], ['H1111'])

    def test_kiszurt_sor_nem_szamit_kartyatalalatnak(self):
        ks = self.ks(('1Móz 1:5', 'név', 'H8034'))
        o = K.osszevet(sorok(), ks, 'genezis/X.md', self.BB)
        self.assertEqual(len(o['olvasas_nem_kartya']), 1)

    def test_tartomany_kulcsszo(self):
        ks = self.ks(('1Móz 1:1-3', 'szavak', 'H3548'))
        o = K.osszevet(sorok(), ks, 'genezis/X.md', self.BB)
        self.assertEqual(o['olvasas_nem_kartya'], [])

    def test_mas_tanulmany_sorai_nem_szamitanak(self):
        ks = [{'tanulmany': 'genezis/MAS.md', 'igehely': '1Móz 1:6', 'szo': 'x', 'strong': 'H1111', 'datum': 'd'}]
        self.assertFalse(K.osszevet(sorok(), ks, 'genezis/X.md', self.BB)['van_kulcsszo'])


class Ir(unittest.TestCase):
    FEJLEC = ('id\tigehely\tforras_kereses\tdontes\tindoklas\tkaroli_szo\tazonositas_modja\tmegbizhatosag\t'
              'datum\tjelolt_tipus\tcel_id\tcel_igehely\tcel_alpont')

    def setUp(self):
        self.d = tempfile.mkdtemp(prefix='gerinc_ir_')
        self.addCleanup(shutil.rmtree, self.d, True)
        self.path = os.path.join(self.d, 'jeloltek.tsv')

    def ir(self, tartalom):
        with open(self.path, 'w', encoding='utf-8', newline='') as f:
            f.write(tartalom)

    def olvas(self):
        with open(self.path, 'rb') as f:
            return f.read()

    def test_csak_ujat_ir_nyitvaval(self):
        self.ir('# komment\n' + self.FEJLEC + '\n')
        irt = K.jeloltek_ir(self.d, '1Móz 1:1-20', sorok(), 'PROV', ma='2026-01-01')
        sz = self.olvas().decode('utf-8').split('\n')
        uj = [s for s in sz[2:] if s]
        self.assertTrue(uj)
        for sor in uj:
            m = sor.split('\t')
            self.assertEqual(m[3], 'nyitva')
            self.assertEqual(len(m), 13)
            self.assertIn('PROV', m[2])
        kulcs = set(irt)
        # szuretlen_tag es kiszurve sorok nem irodnak; az atjutott (A) igen;
        # a mar elofordulas es a mar jelolt (elutasitott) nem
        self.assertIn(('ISTENTISZT-001', '1Móz 1:4'), kulcs)
        self.assertNotIn(('ISTENTISZT-001', '1Móz 1:5'), kulcs)
        self.assertNotIn(('KIRALY-001', '1Móz 1:1'), kulcs)
        self.assertNotIn(('KIRALY-001', '1Móz 1:20'), kulcs)
        self.assertNotIn(('HODIT-001', '1Móz 1:7'), kulcs)
        self.assertTrue(all('beépítve' not in s and 'elutasítva' not in s for s in uj))

    def test_nem_duplikal(self):
        self.ir(self.FEJLEC + '\n')
        K.jeloltek_ir(self.d, 's', sorok(), 'P', ma='d')
        elso = self.olvas()
        self.assertEqual(K.jeloltek_ir(self.d, 's', sorok(), 'P', ma='d'), [])
        self.assertEqual(self.olvas(), elso)

    def test_sorosszevetes_eltereskor_megall(self):
        self.ir(self.FEJLEC + '\nHODIT-001\t1Móz 1:9\n')       # hibas oszlopszam
        elotte = self.olvas()
        with self.assertRaises(ValueError):
            K.jeloltek_ir(self.d, 's', sorok(), 'P', ma='d')
        self.assertEqual(self.olvas(), elotte)

    def test_crlf_megmarad(self):
        self.ir(self.FEJLEC + '\r\n')
        K.jeloltek_ir(self.d, 's', sorok(), 'P', ma='d')
        self.assertNotIn(b'\n', self.olvas().replace(b'\r\n', b''))


class Egyezes(unittest.TestCase):
    """A kartya jelolt.py-sorai (id, igehely, strong) azonosak a valos adaton."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')):
            raise unittest.SkipTest('nincs konkordancia')
        cls.versek = K.versek_betolt()

    def test_szakaszok(self):
        import jelolt as J
        adat = os.path.join(ROOT, 'adat')
        for sz in ('1Móz 6:1-8', '1Móz 17:1-27', 'Mt 24:37-39', 'Róm 10:9-14', '1Móz 7:1-24'):
            sorok_, prov, _ = K.futtat(sz, adat, versek=self.versek, ts=TS)
            j = {(x['id'], x['igehely'], x['strong']) for x in J.jelolt_sorok_szamit(sz, adat)}
            self.assertEqual(K.jelolt_parok(sorok_), j, sz)
            self.assertTrue(prov[0].startswith('scope=range:%s' % sz))

    def test_ures_szakasz_proveniencia(self):
        _, prov, szoveg = K.futtat('Mt 24:37-39', os.path.join(ROOT, 'adat'), versek=self.versek, ts=TS)
        self.assertIn('n=0', prov[0])
        self.assertIn('üres', szoveg)


if __name__ == '__main__':
    unittest.main()
