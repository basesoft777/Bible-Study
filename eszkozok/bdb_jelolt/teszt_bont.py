#!/usr/bin/env python
"""A BDB szakasztábla bontójának tesztjei (F107, eszkozok/bdb_jelolt/bont.py).

Futtatás: python eszkozok/bdb_jelolt/teszt_bont.py   (a táblás és a determinizmus-teszt a kiírt
adat/bdb_szakaszok.tsv-t olvassa; a determinizmus-teszt kb. fél perc, a --ellenoriz módot hívja).
"""
import os
import subprocess
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import bont  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')


def tabla():
    with open(TABLA, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]


class Egyseg(unittest.TestCase):
    def test_blokkok_sub1_es_kivul(self):
        b = bont.json_blokkok('<div><p><b>H1. x</b></p><p> a</p>kint<p style="sub1">al</p></div>')
        self.assertEqual([(bont.sima(h), s) for h, s in b], [('H1. x', False), ('a', False), ('kint', False), ('al', True)])

    def test_fej_tobb_szint(self):
        tok, mar = bont.fej_bont('<b>2. a.</b> march')
        self.assertEqual(tok, [('szam', '2.'), ('betu', 'a.')])
        self.assertEqual(bont.sima(mar), 'march')

    def test_fej_torzs_nagybetu(self):
        tok, _ = bont.fej_bont('<b>Hiph`il A.</b> Perfect')
        self.assertEqual(tok, [('torzs', 'Hiph`il'), ('nagy', 'A.')])

    def test_fej_maradek_a_szovegbe(self):
        tok, mar = bont.fej_bont('<b>1. proper name</b>, of a location')
        self.assertEqual(tok, [('szam', '1.')])
        self.assertEqual(bont.sima(mar), 'proper name, of a location')

    def test_glossza_nem_fej(self):
        tok, _ = bont.fej_bont('<b>king of Gerar</b> Gen 20:2')
        self.assertEqual(tok, [])

    def test_sima_sub_kimarad_sup_marad(self):
        self.assertEqual(bont.sima('<b>2</b><sub>46</sub> x CIS<sup>iv</sup>'), '2 x CIS^iv')
        self.assertEqual(bont.gyakorisag_kivesz('<b>2</b><sub>46</sub> x', True), ['46'])

    def test_kezdet_szorend_fuggetlen(self):
        a = ['h:\u05d3\u05e8\u05db\u05de\u05d5\u05e0', 'h:\u05d0\u05d3\u05e8', 'prosthetic', 'noun']
        b = ['h:\u05d0\u05d3\u05e8', 'h:\u05d3\u05e8\u05db\u05de\u05d5\u05e0', 'prosthetic', 'noun']
        self.assertEqual(bont.eleje_hasonlo(a, b), 1.0)

    def test_pe_mem_egy_vaz(self):
        # a JSON dagesses mem-je és a lexikon dagesses pe-je ugyanazt a vázat adja (csak illesztéshez)
        self.assertEqual(bont.heber_vaz('\u05de\u05bc\u05b7\u05e8'), bont.heber_vaz('\u05e4\u05bc\u05b7\u05e8'))

    def test_kombinalt_fej_szokoz_nelkul(self):
        # F107.22: a „1.a.” két token (H7626)
        tok, mar = bont.fej_bont('<b>1.a.</b> rod, staff')
        self.assertEqual(tok, [('szam', '1.'), ('betu', 'a.')])

    def test_hamis_fej_bekezdestores_utan(self):
        # DT-F107g (a) (1): a fej után „)”, „,”, „;”, „]” — hivatkozás, nem fej (H7121, H3615, H0068)
        for h in ('<b>Pu`al</b>); with name of Baal', '<b>3</b> ); marble', '<b>Qal</b>, afterwards'):
            tok, mar = bont.fej_bont(h)
            self.assertFalse(bont.fej_valodi(tok, mar), h)
        tok, mar = bont.fej_bont('<b>2</b> tribe; — absolute')
        self.assertTrue(bont.fej_valodi(tok, mar))

    def test_bekezdesen_beluli_fej(self):
        # DT-F107g (a) (3): M243 H1129, és a hivatkozás nem vág
        r = bont.kozepfej_bont('— <i>build</i>, <b>1</b> (literal) with')
        self.assertEqual(len(r), 2)
        self.assertTrue(r[1].startswith('<b>1</b>'))
        self.assertEqual(len(bont.kozepfej_bont('Gen 1:1 (see <b>2</b>); x')), 1)
        self.assertEqual(len(bont.kozepfej_bont('compare Qal 42:10, <b>Pi`el</b> 38:7')), 1)
        # bekezdés végi fej: csak ha a következő blokk fejjel nyit (H3615)
        self.assertEqual(len(bont.kozepfej_bont('Lev 26:16; — <b>1</b> ', '<b>a.</b> complete')), 2)
        self.assertEqual(len(bont.kozepfej_bont('Lev 26:16; — <b>1</b> ', 'complete')), 1)

    def test_lexikon_szerint_hivatkozas(self):
        # DT-F107h (a): a lexikonban a fej szövegen belül, hivatkozó szó után — hivatkozás; blokkot nyitó előfordulás — fej
        lex = bont.lexikon_fejek('the verb was originally <b>Qal</b>, afterwards pointed as <b>Niph`al</b> to avoid the '
                                 'expression see the face</p><div class="point"><b>Niph`al</b> Perfect be seen gone away')
        tok, mar = bont.fej_bont('<b>Niph`al</b> to avoid the expression see the face')
        self.assertTrue(bont.lexikon_szerint_hivatkozas({'fejek': lex}, tok, mar))
        tok, mar = bont.fej_bont('<b>Niph`al</b> Perfect be seen gone away')
        self.assertFalse(bont.lexikon_szerint_hivatkozas({'fejek': lex}, tok, mar))
        # „— <b>Qal</b> Perfect”: szövegen belül, de nem hivatkozó szó után — fej (a szűkítés oka, F107.29)
        lex = bont.lexikon_fejek('verb gather (food) — <b>Qal</b> Perfect of ant Prov 6:8')
        tok, mar = bont.fej_bont('<b>Qal</b> Perfect of ant Prov 6:8')
        self.assertFalse(bont.lexikon_szerint_hivatkozas({'fejek': lex}, tok, mar))

    def test_cimfolytatas(self):
        self.assertEqual(bont.cimfolytatas_nelkul(['or', 'shettayim', 'h:x', 'noun']), ['h:x', 'noun'])
        self.assertEqual(bont.cimfolytatas_nelkul(['noun', 'masculine']), ['noun', 'masculine'])


class Tabla(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fej, cls.sorok = tabla()
        cls.st = {}
        for s in cls.sorok:
            cls.st.setdefault(s['strong'], []).append(s)

    def test_fejlec(self):
        self.assertEqual(self.fej, bont.FEJLEC)

    def test_minden_json_strong(self):
        self.assertEqual(len(self.st), 8090)

    def test_strong_sorszam_egyedi(self):
        kulcs = [(s['strong'], s['sorszam']) for s in self.sorok]
        self.assertEqual(len(kulcs), len(set(kulcs)))

    def test_nem_egyezo_bdb_nelkul(self):
        for s in self.sorok:
            if s['illesztes'] in bont.BDB_NELKUL:
                self.assertEqual(s['bdb_id'], '', s['strong'])
                self.assertNotIn(s['jelolo'], ('section', 'remarks'), s['strong'])
            else:
                self.assertTrue(s['bdb_id'].startswith('BDB'), s['strong'])

    def test_h0040_tagolas(self):
        ut = [(s['utvonal'], s['jelolo'], s['jel']) for s in self.st['H0040']][:5]
        self.assertEqual(ut, [('cim', 'cim', ''), ('fej', 'fej', ''), ('-/1/-', 'point', '1'), ('-/2/-', 'point', '2'),
                              ('-/3/-', 'point', '3')])

    def test_h8057_gyakorisag(self):
        s = [x for x in self.st['H8057'] if x['utvonal'] == '-/2/-'][0]
        self.assertEqual((s['jel'], s['gyakorisag']), ('2', '46'))
        self.assertTrue(s['szoveg'].startswith('(especially Psalms'))

    def test_h7626_forrashiba_marad(self):
        # a „145:” a nyers JSON-ban is a szövegben áll (forráshiba): a tábla nem javítja
        self.assertTrue(any(x['szoveg'].startswith('145:tribe') for x in self.st['H7626']))

    def test_h5117_torzs_nagybetu(self):
        self.assertIn("Hiph'il.A/1/a", [x['utvonal'] for x in self.st['H5117']])

    def test_homonima_szakasz(self):
        # DT-F107g (a) (2): a H6440 „I.”, „II.” szakasz (resz üres); a H3068 (M203) és a H8478 (M130) római feje fő tagolás
        h = self.st['H6440']
        self.assertEqual(set(x['szakasz'] for x in h if x['sorszam'] not in ('1', '2', '3')), {'I', 'II'})
        self.assertEqual(set(x['resz'] for x in h), {''})
        self.assertIn('II', [x['resz'] for x in self.st['H3068']])
        self.assertIn('II', [x['resz'] for x in self.st['H8478']])

    def test_hamis_fej_a_tablaban(self):
        # H7121: a „(compare Pu`al)” nem törzsfej; a Qal 3. jelentése a Qal alatt
        self.assertIn('Qal/3/a', [x['utvonal'] for x in self.st['H7121']])
        self.assertNotIn('Pu\'al/-/d', [x['utvonal'] for x in self.st['H7121']])

    def test_bekezdesen_beluli_fej_a_tablaban(self):
        self.assertIn('Qal/1/i', [x['utvonal'] for x in self.st['H1129']])        # M243
        self.assertIn("Pi'el/1/a", [x['utvonal'] for x in self.st['H3615']])      # bekezdés végi fej

    def test_negyedik_szabaly_a_tablaban(self):
        # DT-F107h (a): a H6440 II. szakaszában a hamis „Niph`al” után a 4–8. jelentés a szakaszé; a H0430 „3” fej marad
        h = [x['utvonal'] for x in self.st['H6440'] if x['szakasz'] == 'II']
        self.assertIn('-/4/a', h)
        self.assertIn('-/8/b', h)
        self.assertNotIn("Niph'al/4/a", h)
        self.assertIn('-/3/-', [x['utvonal'] for x in self.st['H0430']])

    def test_proveniencia(self):
        for s in self.sorok[:2000]:
            self.assertTrue(s['proveniencia'].startswith('scope=%s | forras=' % s['strong']))
            self.assertIn('| ts=', s['proveniencia'])


class Javitas(unittest.TestCase):
    """adat/bdb_forras_javitas.tsv (forras_javit.py, DT-F107f (a))."""

    @classmethod
    def setUpClass(cls):
        import forras_javit
        cls.fj = forras_javit
        with open(forras_javit.KI_UT, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        fej = sorok[2].split('\t')
        cls.sorok = [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]

    def test_mem_dagesh_hely_es_csere(self):
        szo = 'מַּר'                      # mem + dagesh + patah + resh
        self.assertEqual(self.fj.mem_dagesh_helyek(szo), [0])
        self.assertEqual(self.fj.cserel(szo, [0])[0], 'פ')
        self.assertEqual(self.fj.mem_dagesh_helyek('מַר'), [])

    def test_norm_kantillacio_nelkul(self):
        self.assertEqual(self.fj.norm('מָ֑ר'), 'מָר')

    def test_kezi_sorok(self):
        k = [s for s in self.sorok if s['allapot'] == 'kezi']
        self.assertEqual(len(k), len(self.fj.KEZI))
        for s in k:
            self.assertEqual(s['proveniencia'], 'manual')
            self.assertIn(s['hiba'], ('jelolo_hianyzik', 'hamis_jelolo'))
            self.assertTrue(s['indok'] and s['forras_alak'] and s['javitott_alak'])

    def test_allapotok(self):
        self.assertEqual(set(s['allapot'] for s in self.sorok), {'javitva', 'valodi_mem', 'jelolt_marad', 'kezi'})
        for s in self.sorok:
            if s['allapot'] == 'kezi':
                continue
            self.assertEqual(bool(s['javitott_alak']), s['allapot'] == 'javitva')
            if s['allapot'] == 'javitva' and s['hiba'] == 'pe_mem':
                # a forrás (JSON) alakban nincs dagesses pe (DT-F107f)
                self.assertNotRegex(self.fj.norm(s['forras_alak']), 'פ[ְ-ׇ]*ּ')
                self.assertTrue(s['bdb_id'])

    def test_minta_mishpat(self):
        self.assertTrue(any(s['strong'] == 'H2835' and s['allapot'] == 'javitva'
                            and self.fj.norm(s['javitott_alak']) == self.fj.norm('מִשְׁפַּט')
                            for s in self.sorok))


class Nezet(unittest.TestCase):
    """nezet_general.py és a hivatkozas-sorok (DT-F107c (d))."""

    @classmethod
    def setUpClass(cls):
        import nezet_general
        cls.ng = nezet_general

    def test_mem_csere_ket_alakban(self):
        self.assertEqual(self.ng.mem_csere_szoban('מַּר', 1), 'פַּר')
        self.assertEqual(self.ng.mem_csere_szoban('מַּר', 1), 'פַּר')
        self.assertIsNone(self.ng.mem_csere_szoban('מַר', 1))

    def test_tobb_mem_egy_szoban(self):
        szo = 'מִּמָּ'
        uj, hiba = self.ng.pe_mem_sorban('x ' + szo, [{'szo_sorszam': '1', 'elofordulas': '1'},
                                                     {'szo_sorszam': '1', 'elofordulas': '2'}])
        self.assertEqual(hiba, 0)
        self.assertEqual(uj, 'x פִּפָּ')

    def test_token_elofordulas_egesz_token(self):
        import forras_javit
        self.assertEqual(len(forras_javit.token_elofordulas('Gen 1:1; Genesis Gen 2:2', 'Gen')), 2)

    def test_hivatkozas_sorok(self):
        import forras_javit
        with open(forras_javit.KI_UT, encoding='utf-8', newline='') as f:
            s = f.read().split('\n')
        fej = s[2].split('\t')
        h = [dict(zip(fej, x.split('\t'))) for x in s[3:] if x and x.split('\t')[3] == 'hivatkozas']
        self.assertTrue(h)
        for d in h:
            self.assertEqual(d['allapot'], 'javitva')
            self.assertRegex(d['indok'], r'F34|F46')
            self.assertTrue(d['sorszam'])

    def test_nezet_csak_jovahagyott_elteres(self):
        nezet, tab, stat = self.ng.general(False)
        self.assertEqual(stat['hivatkozas_sikertelen'], 0)
        s, _ = self.ng.osszevet(nezet, tab, False)
        self.assertEqual(set(s) - {'azonos', 'sub', 'szokoz', 'forras_html', 'nincs_a_nezetben'}, set())


class HuIlleszt(unittest.TestCase):
    """hu_illeszt.py és az adat/bdb_szakasz_hu.tsv (7. lépés)."""

    @classmethod
    def setUpClass(cls):
        import hu_illeszt
        cls.hi = hu_illeszt
        with open(hu_illeszt.KI_UT, encoding='utf-8', newline='') as f:
            s = f.read().split('\n')
        fej = s[2].split('\t')
        cls.sorok = [dict(zip(fej, x.split('\t'))) for x in s[3:] if x]

    def test_forras_jelolok(self):
        self.assertEqual(self.hi.forras_jelolok('2. a.'), ['2', 'a'])
        self.assertEqual(self.hi.forras_jelolok('Hiph`il'), ['T:Hiph'])
        self.assertEqual(self.hi.forras_jelolok('II.'), ['II'])

    def test_illesztes_es_horgony(self):
        sorok = [{'jelolo': 'fej', 'jel': '', 'szoveg': 'x'},
                 {'jelolo': 'point', 'jel': '1', 'szoveg': 'king of Gerar Gen 20:2'},
                 {'jelolo': 'point', 'jel': '2', 'szoveg': 'king of Gath'}]
        hu = 'fej szöveg +? 1 Gerár királya 1Móz 20:2. 2 Gát királya'
        e, szigoru, horgonyos = self.hi.strong_illeszt(sorok, hu)
        self.assertEqual([x[0] for x in e], ['jelolo_nelkul', 'horgonnyal', 'illeszkedik'])
        self.assertEqual(hu[e[1][2]:].split(' ')[0], '1')      # a horgonyolt szakasz a saját jelölőjénél kezdődik
        self.assertEqual(horgonyos, 'horgonnyal')

    def test_kategoriak_es_hash(self):
        self.assertEqual(set(x['kategoria'] for x in self.sorok), {'illeszkedik', 'horgonnyal', 'elakad', 'jelolo_nelkul'})
        for x in self.sorok:
            self.assertRegex(x['forditas_forras_hash'], r'^[0-9a-f]{40}$')
            self.assertEqual(bool(x['szoveg_hu']) or x['hu_kezdet'] == '' or x['hu_hossz'] == '0', True)
        self.assertEqual(len(set(x['strong'] for x in self.sorok)), 674)

    def test_h0040(self):
        h = {x['sorszam']: x for x in self.sorok if x['strong'] == 'H0040'}
        self.assertTrue(h['3']['szoveg_hu'].startswith('1 Gerár'))
        self.assertEqual(h['4']['kategoria'], 'illeszkedik')

    def test_ellenoriz(self):
        with open(self.hi.KI_UT, encoding='utf-8') as f:
            ts = f.readline().split('--ts ')[1].split(' ')[0]
        r = subprocess.run([sys.executable, os.path.join(ITT, 'hu_illeszt.py'), '--ts', ts, '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class Determinizmus(unittest.TestCase):
    def test_ellenoriz(self):
        with open(TABLA, encoding='utf-8') as f:
            ts = f.readline().split('--ts ')[1].split(' ')[0]
        r = subprocess.run([sys.executable, os.path.join(ITT, 'bont.py'), '--ts', ts, '--ellenoriz', '--lista', '0'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_javitas_ellenoriz(self):
        with open(os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv'), encoding='utf-8') as f:
            ts = f.readline().split('--ts ')[1].split(' ')[0]
        r = subprocess.run([sys.executable, os.path.join(ITT, 'forras_javit.py'), '--ts', ts, '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
