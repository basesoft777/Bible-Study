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
        # DT-F107g (a) (2): a H3068 (M203) és a H8478 (M130) római feje fő tagolás. F185 (seed-101 M029, seed-102 M024): a H6440
        # „I. 1. face” / „II. פְּנֵי with prepositions” római feje is fő tagolás (`resz`; homonima-szakasz csak héber címszó előtt) —
        # a teszt a F185 óta elavult elvárása (szakasz I/II) F202.5-ben igazítva
        h = self.st['H6440']
        self.assertEqual(set(x['resz'] for x in h if x['sorszam'] not in ('1', '2', '3')), {'I', 'II'})
        self.assertEqual(set(x['szakasz'] for x in h), {''})
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
        h = [x['utvonal'] for x in self.st['H6440'] if x['resz'] == 'II']      # F185: a II. fő tagolás (F202.5)
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
        self.assertEqual(len(k), len(self.fj.KEZI) + len(self.fj.KEZI_HIVATKOZAS))
        for s in k:
            self.assertEqual(s['proveniencia'], 'manual')
            self.assertIn(s['hiba'], ('jelolo_hianyzik', 'hamis_jelolo', 'hivatkozas_kezi'))
            self.assertTrue(s['indok'] and s['forras_alak'] and s['javitott_alak'])

    def test_hivatkozas_kezi(self):
        # DT381 (a): H8034 „26:35” → 26:25, a 2.30 7. sorában, az első előfordulás; F123: H7585 „Prov 25:11” → 15:11 (10. sor);
        # F12 (DT-F12b (1)): H8414 „49:19” → 49:4 (4. sor)
        k = [s for s in self.sorok if s['hiba'] == 'hivatkozas_kezi']
        self.assertEqual([(s['strong'], s['sorszam'], s['elofordulas'], s['forras_alak'], s['javitott_alak']) for s in k],
                         [('H8034', '7', '1', '26:35', '26:25'), ('H7585', '10', '1', '25:11', '15:11'),
                          ('H8414', '4', '1', '49:19', '49:4'),
                          # F202.4 (N102): a H1004 könyvnév-hibás helyei, a javított alak a könyvvel
                          ('H1004', '17', '1', '10:20', '1Kir 12:20'), ('H1004', '17', '1', '10:26', '1Kir 12:26'),
                          ('H1004', '17', '1', '13:2', '1Kir 13:2'), ('H1004', '17', '1', '14:8', '1Kir 14:8')])

    def test_allapotok(self):
        self.assertEqual(set(s['allapot'] for s in self.sorok),
                         {'javitva', 'valodi_mem', 'jelolt_marad', 'kezi', 'valodi_sorrend'})
        for s in self.sorok:
            if s['allapot'] == 'kezi':
                continue
            self.assertEqual(bool(s['javitott_alak']), s['allapot'] == 'javitva')
            if s['allapot'] == 'javitva' and s['hiba'] == 'pe_mem':
                # a forrás (JSON) alakban nincs dagesses pe (DT-F107f)
                self.assertNotRegex(self.fj.norm(s['forras_alak']), 'פ[ְ-ׇ]*ּ')
                # a lexikon szerinti javításnak bdb_id kell; a tanús (F185 P4) javításnak a tanú `javit` ítélete
                self.assertTrue(s['bdb_id'] or s.get('tanu', '').split(';')[0].endswith(':javit'))

    def test_tanus_dontes(self):
        # F185 P4 (DT-F185c, DT-F185d): a tanús sorok mezője `<tanú>:<szint>:<ítélet>`; `javit` → javitva, különben jelolt_marad;
        # a rés/dálet belső döntése csak L1 (a vázszint körkörös); ellentmondásnál ketes
        t = [s for s in self.sorok if s.get('tanu')]
        self.assertTrue(t)
        for s in t:
            self.assertIn(s['hiba'], ('pe_mem', 'res_dalet'))
            elso = s['tanu'].split(';')[0]
            self.assertTrue(elso.startswith(('tahot/oshb:', 'sefaria-api 2026-11-10:')), s['tanu'])
            if 'ellentmondás' in s['tanu']:
                self.assertEqual(s['allapot'], 'jelolt_marad')
            elif elso.endswith(':javit'):
                self.assertEqual(s['allapot'], 'javitva')
            else:
                self.assertEqual(s['allapot'], 'jelolt_marad')
            if s['hiba'] == 'res_dalet' and elso.startswith('tahot/oshb:'):
                self.assertNotIn(':L2:', elso)

    def test_heber_sorrend_sorok(self):
        # DT-F131z: javitva csak tiszta, Biblia által igazolt tétel; az indokban a TAHOT-vers
        h = [s for s in self.sorok if s['hiba'] == 'heber_sorrend']
        self.assertEqual(set(s['allapot'] for s in h), {'javitva', 'valodi_sorrend', 'jelolt_marad'})
        szoveg = {(s['strong'], s['sorszam']): s for s in self.sorok}
        for s in h:
            self.assertEqual(bool(s['javitott_alak']), s['allapot'] == 'javitva')
            # a kézi szórend-sor proveniencia `manual` (CLAUDE.md 1. szabály; F202.5: az elvárás a kézi sorok óta elavult)
            self.assertTrue(s['elofordulas'].isdigit()
                            and (s['proveniencia'] == 'manual' or s['proveniencia'].startswith('scope=%s |' % s['strong'])))
            if s['allapot'] == 'javitva':
                self.assertNotRegex(s['forras_alak'], r'[,;.:0-9A-Za-z]')
                if s['proveniencia'] != 'manual':
                    self.assertIn('TAHOT', s['indok'])
                self.assertEqual(sorted(s['forras_alak'].replace(' ', '')), sorted(s['javitott_alak'].replace(' ', '')))
        self.assertTrue(szoveg)

    def test_heber_sorrend_h7121(self):
        import heber_sorrend as HS
        # a kulcs a mássalhangzó-váz (a pontozás sorrendje forrásonként eltérhet)
        h = {(s['sorszam'], HS.vaz(s['forras_alak'].replace(' ', '|'))): s for s in self.sorok
             if s['strong'] == 'H7121' and s['hiba'] == 'heber_sorrend'}
        s = h[('4', HS.vaz('גדול|בקול'))]
        self.assertEqual((s['allapot'], HS.vaz(s['javitott_alak'].replace(' ', '|'))), ('javitva', HS.vaz('בקול|גדול')))
        # a Qal 2.c kifejezése: a Biblia-próba nem dönt (mindkét alak illeszkedik), ezért a döntés szerint marad
        s = h[('8', HS.vaz('קיבשם'))]
        self.assertEqual(s['allapot'], 'jelolt_marad')
        javaslat = s['indok'].split('javaslata: ')[1]
        self.assertEqual((HS.vaz(javaslat), javaslat.count('׳'), javaslat.endswith('׳')), (HS.vaz('קבשםי'), 2, True))

    def test_heber_sorrend_szabaly(self):
        import heber_sorrend as HS
        # H7121 Qal 2.c: a BDB.lexicon darabjai (vizuális darabsorrend) és a JSON-alak
        self.assertEqual(HS.r0('׳ק י ׳בְּשֵׁם'), '׳בְּשֵׁם י ׳ק')
        self.assertEqual(HS.r_lex('׳ק י ׳בְּשֵׁם', ['׳', 'בְּשֵׁם י', ' ', '׳', 'ק']), 'ק׳ בְּשֵׁם י׳')
        self.assertEqual(HS.r_str('׳ק י ׳בְּשֵׁם'), 'ק׳ בְּשֵׁם י׳')
        self.assertEqual(HS.r_hib('גְּדוֺל בְּקוֺל', None), 'בְּקוֺל גְּדוֺל')
        self.assertIsNone(HS.r_lex('׳ק י', ['׳', 'ק']))     # a szerkezet nem vihető át
        self.assertTrue(HS.tiszta('בְּקוֺל גְּדוֺל'))
        self.assertFalse(HS.tiszta('ᵐ5 ׳ל'))
        self.assertFalse(HS.tiszta('דָּבָר, תּוֺרָה'))

    def test_atiras_szabaly(self):
        # DT-F164a: „e?®” → „e”, „°” → „ʾ”
        self.assertEqual(self.fj.atiras_szabaly('Sh®°ôl'), 'Sheʾôl')
        self.assertEqual(self.fj.atiras_szabaly('She®°ôl'), 'Sheʾôl')
        self.assertEqual(self.fj.atiras_szabaly('sh®°ôl'), 'sheʾôl')
        self.assertEqual([m.group(0) for m in self.fj.ATIRAS_ALAK.finditer('in Sh®°ôl). 30° fra-s®nhana')],
                         ['Sh®°ôl', 's®nhana'])

    def test_atiras_sorok(self):
        # B3: a „®”-t hordozó minden alak egy sor; javitva csak a BDB.lexicon által igazolt (Seól-család)
        # F123.GENKOR (DT-F181a): a kézi `atiras` sorok (`manual`) külön, l. test_kezi_szoveg_sorok
        kezi = [s for s in self.sorok if s['hiba'] == 'atiras' and s['proveniencia'] == 'manual']
        a = [s for s in self.sorok if s['hiba'] == 'atiras' and s['proveniencia'] != 'manual']
        self.assertEqual(len(set(s['strong'] for s in a)), 33)
        self.assertEqual(sorted(set(s['strong'] for s in kezi)), ['H2416', 'H7121'])
        for s in a:
            self.assertIn('®', s['forras_alak'])
            self.assertEqual(bool(s['javitott_alak']), s['allapot'] == 'javitva')
            self.assertIn(s['allapot'], ('javitva', 'jelolt_marad'))
            if s['allapot'] == 'javitva':
                self.assertEqual(s['javitott_alak'], self.fj.atiras_szabaly(s['forras_alak']))
                self.assertNotRegex(s['javitott_alak'], '[®°]')
        self.assertEqual(sorted(s['strong'] for s in a if s['allapot'] == 'jelolt_marad'), ['H2609', 'H6573', 'H7848'])
        self.assertIn(('H7585', 'She®°ôl', 'Sheʾôl'),
                      [(s['strong'], s['forras_alak'], s['javitott_alak']) for s in a])

    def test_kezi_szoveg_sorok(self):
        # F123.GENKOR (DT-F181a): a kézi `atiras` és `zarojel` sorok: javitva, `manual`, javított alakkal
        k = [s for s in self.sorok if s['hiba'] in ('atiras', 'zarojel') and s['proveniencia'] == 'manual']
        self.assertEqual(len(k), 7)
        for s in k:
            self.assertEqual(s['allapot'], 'javitva')
            self.assertTrue(s['javitott_alak'] and s['indok'])
        self.assertIn(('H7121', 'be summoned (compare Qal 5:', 'be summoned (compare Qal 5):'),
                      [(s['strong'], s['forras_alak'], s['javitott_alak']) for s in k])

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

    def test_osszefuzo_a_mai_adaton_valtozatlan(self):
        # F128 (DT-F128g (a)): a közös összefűzővel a tábla törzse (a `# forras` fejlécsor és a sorvég nélkül) azonos
        ts = self.sorok[0]['proveniencia'].rsplit('ts=', 1)[1]
        uj = ['\t'.join(s) for s in self.hi.general(ts)[0]]
        with open(self.hi.KI_UT, encoding='utf-8', newline='') as f:
            regi = [x.rstrip('\r') for x in f.read().split('\n')[3:] if x.strip()]
        self.assertEqual(uj, regi)

    def test_forditasok_szakaszsorokkal(self):
        # F128: a szakaszonként fordított Strong a `sz<sorszam>` sorok összefűzése, a hash a forrásnézeté
        import tempfile
        import szakasz_bemenet as sb
        fej = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forditas_hu', 'allapot']
        szak = sb.szakaszok('H0001')
        sorok = [['BDB', 'H0001', 'H1', 'teljes', 'forditas_hu', 'regi', 'régi', 'elavult']]
        sorok += [['BDB', 'H0001', 'H1', 'sz%d' % x['sorszam'], 'forditas_hu', x['hash'], 'm%d' % x['sorszam'], 'sonnet']
                  for x in reversed(szak)]
        sorok += [['BDB', 'H0002', 'H2', 'teljes', 'forditas_hu', 'h2', 'második', 'sonnet']]
        with tempfile.TemporaryDirectory() as tmp:
            ut = os.path.join(tmp, 'forditasok.tsv')
            with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(['# teszt', '\t'.join(fej)] + ['\t'.join(s) for s in sorok]) + '\n')
            f = self.hi.forditasok(ut)
        self.assertEqual(f['H0001']['forditas_hu'], ' '.join('m%d' % x['sorszam'] for x in szak))
        self.assertEqual(f['H0001']['forras_hash'], sb.sha1(sb.nezet(szak)))
        # F123.BDBILL (DT-F123y): az igazolt 1:1 sorszám szerint, a teljes sornál nincs szakaszos megfeleltetés
        self.assertEqual(f['H0001']['szakaszonkent'], dict((x['sorszam'], 'm%d' % x['sorszam']) for x in szak))
        self.assertEqual(f['H0002'], {'forditas_hu': 'második', 'forras_hash': 'h2', 'szakaszonkent': None, 'nem_igazolt': None})

    def test_forras_jelolok(self):
        self.assertEqual(self.hi.forras_jelolok('2. a.'), ['2', 'a'])
        self.assertEqual(self.hi.forras_jelolok('Hiph`il'), ["T:Hiph'il"])      # DT-F107b (d): kanonikus törzskulcs
        self.assertEqual(self.hi.forras_jelolok('II.'), ['II'])

    def _jelek(self, hu):
        return [j for _, j in self.hi.magyar_jelolok(hu)]

    def test_bovites_pozitiv(self):
        # DT-F107b (d): valós adatból — H0040, H5674, H0559, H6213/H5414
        self.assertIn('1', self._jelek('Gen 20:18 +? 1 Gerár királya 1Móz 20:2'))
        self.assertIn('j', self._jelek('használatban Zsolt 17:3. j. elmenni mellette'))
        self.assertIn("T:Hithpa'el", self._jelek('innen a lenti Hithpa`el, אָמִיר'))
        self.assertIn("T:Hithpa'el", self._jelek('a Hithpa`elben és a Hitpael-ben'))
        self.assertIn("T:Pe'al", self._jelek('6, 9 és máshol); — Pe`al imperfectum'))
        self.assertIn("T:Pa'el", self._jelek('עַסִּי ᵑ7 Pa`el összezúzni'))
        self.assertEqual(self.hi.forras_jelolok('Hithpa`el'), ["T:Hithpa'el"])
        self.assertEqual(self.hi.torzs_kulcs('Hitpael'), self.hi.torzs_kulcs('Hithpa`el'))

    def test_bovites_negativ(self):
        # a szövegközi betű vagy szám nem jelölő
        self.assertNotIn('2', self._jelek('és a 2 fiú elment'))
        self.assertNotIn('b', self._jelek('lásd a b) pontot'))
        self.assertNotIn('l', self._jelek('(de olv. עֲוֺנָמוֺ, l. a kommentárokat)'))       # H5869: „l.” = lásd
        self.assertNotIn('k', self._jelek('Ba^ZMG 1887, 632 k.) — יוֺם'))                 # H3117: „k.” = és a következő
        self.assertNotIn('q', self._jelek('a q. jelű kézirat'))                          # nem tagolásjel után
        for szo in ('papok királysága', 'puszta proszthetikus', 'pap (késői héber', 'Pentateuchusban'):
            self.assertFalse([j for j in self._jelek(szo) if j.startswith('T:')], szo)

    def test_kotetszamos_siglum(self):
        # hu_illeszt (4), ISTENTISZT-001 arany lap, 2026-10-29: a „Kö^ii. 1. 104” lapszám nem jelölő (H8034), a valódi
        # jelölő utána megmarad; a szerzői siglum és a záró zárójel utáni jel valódi jelölő lehet (H7442, H4557, H0450) —
        # a szabály ezeket nem dobja
        hu = 'vö. RS^K 213, 303 kk. Kö^ii. 1. 104; késői héber — név: 1 folyóé 1Móz 2:11'
        poz = [p for p, j in self.hi.magyar_jelolok(hu) if j == '1']
        self.assertEqual(poz, [hu.index('1 folyóé')])
        self.assertNotIn('1', self._jelek('(Kö^ii. 1. 512), óarámi'))
        self.assertIn('2', self._jelek('esetleg וָרֹק és köpés, Klo Che^Hpt. 2 nyomorúságban, JSir 2:19.'))
        self.assertIn('2', self._jelek('így ᵐ5 Di So^Kau. 2 elbeszélés, előadás'))
        self.assertIn('5', self._jelek('vö. RS^149). 5 az ember Istene'))
        # végig az illesztésen: a H8034 feje nem a lapszámnál vágódik el
        sorok = [{'jel': '', 'jelolo': 'fej', 'szoveg': ''}, {'jel': '1', 'jelolo': 'point', 'szoveg': 'of river Gen 2:11'}]
        eredmeny = self.hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(eredmeny[1][:3], ['illeszkedik', '1', hu.index('1 folyóé')])

    def test_reszleges_generalas(self):
        # --strong: a Strong-szűrt generálás sorai = a teljes generálás e Strongokra eső sorai (ISTENTISZT-001 arany lap,
        # 2026-10-29: H4397, H8034, H9004)
        csak = {'H4397', 'H8034', 'H9004'}
        teljes = [r for r in self.hi.general('2026-10-29')[0] if r[0] in csak]
        self.assertEqual(self.hi.general('2026-10-29', csak)[0], teljes)

    def test_reszleges_szoveg(self):
        # csak a megnevezett Strong sorai cserélődnek, a többi bájtra marad; a --ts megmarad, a jelölés ismételhető
        fej = ('# GENERÁLT: eszkozok/bdb_jelolt/hu_illeszt.py --ts 2026-10-18 — x.', '# forras: y', 'strong\tsorszam\tx')
        regi = '\n'.join(fej + ('H0001\t1\ta', 'H0002\t1\tb', 'H0002\t2\tc', 'H0003\t1\td')) + '\n'
        uj = self.hi.reszleges_szoveg(regi, [['H0002', '1', 'B'], ['H0002', '2', 'C']], {'H0002'}, '2026-10-29')
        s = uj.split('\n')
        self.assertEqual(s[3:], ['H0001\t1\ta', 'H0002\t1\tB', 'H0002\t2\tC', 'H0003\t1\td', ''])
        self.assertEqual(s[1:3], list(fej[1:]))
        self.assertTrue(s[0].startswith(fej[0] + self.hi.RESZLEGES + ' H0002 (--strong, ts=2026-10-29;'))
        self.assertEqual(s[0].split('--ts ')[1].split(' ')[0], '2026-10-18')
        ujra = self.hi.reszleges_szoveg(uj, [['H0002', '1', 'B'], ['H0002', '2', 'C']], {'H0002'}, '2026-10-29')
        self.assertEqual(ujra, uj)
        with self.assertRaises(ValueError):
            self.hi.reszleges_szoveg(regi, [['H0002', '1', 'B']], {'H0002'}, '2026-10-29')
        with self.assertRaises(ValueError):
            self.hi.reszleges_szoveg(regi.replace('\n', '\r\n'), [['H0002', '1', 'B'], ['H0002', '2', 'C']], {'H0002'}, 'x')

    def test_illesztes_es_horgony(self):
        sorok = [{'jelolo': 'fej', 'jel': '', 'szoveg': 'x'},
                 {'jelolo': 'point', 'jel': '1', 'szoveg': 'king of Gerar Gen 20:2'},
                 {'jelolo': 'point', 'jel': '2', 'szoveg': 'king of Gath'}]
        # a bővítés után a kérdőjel utáni szám jelölő (H0040)
        hu = 'fej szöveg +? 1 Gerár királya 1Móz 20:2. 2 Gát királya'
        e, szigoru, horgonyos = self.hi.strong_illeszt(sorok, hu)
        self.assertEqual([x[0] for x in e], ['jelolo_nelkul', 'illeszkedik', 'illeszkedik'])
        # felismerhetetlen jelölő (a szám a szóhoz tapad) — horgony a fejezet:versen, a saját jelölőnél kezdve
        hu = 'fej szöveg, + 1 Gerár királya 1Móz 20:2. 2 Gát királya'
        e, szigoru, horgonyos = self.hi.strong_illeszt(sorok, hu)
        self.assertEqual([x[0] for x in e], ['jelolo_nelkul', 'horgonnyal', 'illeszkedik'])
        self.assertEqual(hu[e[1][2]:].split(' ')[0], '1')
        self.assertEqual(horgonyos, 'horgonnyal')

    def test_kategoriak_es_hash(self):
        # F123.BDBILL (DT-F123y): a szakaszonként fordított Strong sorai `szakasz` kategóriájúak; `elakad` a mai adaton nincs
        kat = set(x['kategoria'] for x in self.sorok)
        self.assertIn('szakasz', kat)
        self.assertLessEqual(kat, {'szakasz', 'illeszkedik', 'horgonnyal', 'elakad', 'jelolo_nelkul'})
        for x in self.sorok:
            self.assertRegex(x['forditas_forras_hash'], r'^[0-9a-f]{40}$')
            self.assertEqual(bool(x['szoveg_hu']) or x['hu_kezdet'] == '' or x['hu_hossz'] == '0', True)
        self.assertEqual(len(set(x['strong'] for x in self.sorok)), 8090)

    def test_h0040(self):
        h = {x['sorszam']: x for x in self.sorok if x['strong'] == 'H0040'}
        self.assertTrue(h['3']['szoveg_hu'].startswith('1 Gerár'))
        self.assertEqual(h['4']['kategoria'], 'illeszkedik')

    def test_hash_sorveg_fuggetlen(self):
        # F128.21 (ELLENOR_F128 1.): a CRLF- és az LF-bájtsor azonos hash-t ad, a darabhatáron kettévágott \r\n-nél is
        import hashlib
        import tempfile
        lf = 'első sor\tא\nmásodik\tβ\n\nutolsó'.encode('utf-8')
        crlf = lf.replace(b'\n', b'\r\n')
        vart = hashlib.sha256(lf).hexdigest()
        self.assertEqual(self.hi.sha256_bajtok([lf]), vart)
        self.assertEqual(self.hi.sha256_bajtok([crlf]), vart)
        for i in range(1, len(crlf)):
            self.assertEqual(self.hi.sha256_bajtok([crlf[:i], crlf[i:]]), vart, i)
        self.assertEqual(self.hi.sha256_bajtok([b'a\r', b'b']), hashlib.sha256(b'a\rb').hexdigest())   # magányos \r marad
        self.assertEqual(self.hi.sha256_bajtok([b'a\r']), hashlib.sha256(b'a\r').hexdigest())
        with tempfile.TemporaryDirectory() as tmp:
            for nev, b in (('lf', lf), ('crlf', crlf)):
                with open(os.path.join(tmp, nev), 'wb') as fh:
                    fh.write(b)
            self.assertEqual(self.hi.sha256_fajl(os.path.join(tmp, 'lf')), self.hi.sha256_fajl(os.path.join(tmp, 'crlf')))
        # a forditas_kapuk.py hash-e az LF-blobé, a checkout sorvégétől függetlenül
        with open(os.path.join(GYOKER, 'eszkozok', 'forditas_kapuk.py'), 'rb') as fh:
            blob = fh.read().replace(b'\r\n', b'\n')
        self.assertEqual(self.hi.sha256_fajl(os.path.join(GYOKER, 'eszkozok', 'forditas_kapuk.py')),
                         hashlib.sha256(blob).hexdigest())

    def test_ellenoriz(self):
        with open(self.hi.KI_UT, encoding='utf-8') as f:
            ts = f.readline().split('--ts ')[1].split(' ')[0]
        r = subprocess.run([sys.executable, os.path.join(ITT, 'hu_illeszt.py'), '--ts', ts, '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class F185Fejek(unittest.TestCase):
    """F185 P1 (N103 (2), N106): a hamis bekezdés-eleji fej, a hivatkozással összetapadt betűfej, a jelöletlen alcímszó, a
    számozott pont alatti nagybetűs csoport és a bővített törzsnévlista. Az esetek a seed-101/102 ítéleteiből és a korpuszból."""

    @classmethod
    def setUpClass(cls):
        _, sorok = tabla()
        cls.t = {}
        for d in sorok:
            cls.t[(d['strong'], d['sorszam'])] = d

    def ut(self, strong, sorszam):
        return self.t[(strong, str(sorszam))]['utvonal']

    # --- egység: a környezeti szabály (a)–(d)
    def test_zarojel_belsejeben(self):
        # H2388 „(subject ׳י; but Co reads | Pi`el as Ezek 30:24) .”
        self.assertEqual(bont.hamis_fej_kornyezet('30:25 (subject ׳י; but Co reads', 'as Ezek 30:24) .', [('torzs', 'Pi`el')], {}), 'a')

    def test_above_below(self):
        self.assertEqual(bont.hamis_fej_kornyezet('On Hosea 4:8 see', 'above In H, Lev 23:19', [('szam', '1')], {}), 'b')

    def test_utalo_szo_csak_torzsnel(self):
        self.assertEqual(bont.hamis_fej_kornyezet('Est 3:8 (see', 'Est 3:8', [('torzs', 'Qal')], {}), 'c')
        # számfej utaló szó után valódi (H3205 „yet see | 2 less often beget:”, H1518 „compare | 2 transitive”)
        self.assertEqual(bont.hamis_fej_kornyezet('Deut 32:18 yet see', 'less often beget:', [('szam', '2')], {}), '')
        self.assertEqual(bont.hamis_fej_kornyezet('38:8, compare', 'transitive', [('szam', '2')], {}), '')

    def test_sorrendsertes_mondat_kozepen(self):
        # seed-101 M154 H2471 „burnt on the altar with | c. Lev 8:26”
        self.assertEqual(bont.hamis_fej_kornyezet('burnt on the altar with', 'Lev 8:26, but usually', [('betu', 'c.')], {'betu': 'd'}), 'd')
        # mondatzáró jel után, vagy „a.” újrakezdés: valódi (H2850 „usually | a. collective”)
        self.assertEqual(bont.hamis_fej_kornyezet('Exod 29:23 = Lev 8:26.', 'x', [('betu', 'c.')], {'betu': 'd'}), '')
        self.assertEqual(bont.hamis_fej_kornyezet('usually', 'collective', [('betu', 'a.')], {'betu': 'n'}), '')
        # a következő betű (sorrendben) valódi
        self.assertEqual(bont.hamis_fej_kornyezet('with', 'x', [('betu', 'e.')], {'betu': 'd'}), '')

    def test_hivatkozassal_tapadt_betufej(self):
        self.assertEqual(bont.hivatkozas_fej('<b>3b. b.</b> qualitatively', {'betu': 'a'})[:2], ('3b. b.', 'b'))
        self.assertEqual(bont.hivatkozas_fej('<b>3b, c. c.</b> x', {'betu': 'b'})[:2], ('3b, c. c.', 'c'))
        self.assertIsNone(bont.hivatkozas_fej('<b>3b. b.</b> x', {'betu': 'c'}))     # nem a várt betű

    def test_alcimszo_sub1_nelkul(self):
        self.assertTrue(bont.alcimszo_nyito(' <heb>סוֺפֵר סֹפֵר,</heb> <b>noun masculine</b> enumerator'))
        self.assertFalse(bont.alcimszo_nyito(' <heb>סוֺפֵר</heb> noun masculine enumerator'))

    def test_uj_torzsnevek(self):
        for nev in ('Hithpa`lel', 'Hithpo`lel', 'Po`lel', 'Hothpa`al', 'Pi`lel'):
            tok, _ = bont.fej_bont('<b>%s</b> Perfect' % nev)
            self.assertEqual(tok, [('torzs', nev)], nev)
        tok, _ = bont.fej_bont('<b>Hithpa.</b> x')
        self.assertEqual(tok, [])

    # --- a kiírt tábla (seed-101/102 esetek)
    def test_tabla_h2388_hiphil_folytatodik(self):
        # seed-102 M002/M221: a „(… Co reads Pi`el as Ezek 30:24)” nem törzsfej; a 4–6. pont a Hiph`il-é
        self.assertEqual(self.t[('H2388', '39')]['jel'], '')
        self.assertEqual([self.ut('H2388', n) for n in (40, 42, 43, 45)], ["Hiph'il/4/-", "Hiph'il/6/-", "Hiph'il/6/a", "Hiph'il/6/c"])

    def test_tabla_h2403_see_1_above(self):
        # N99 (HAMART): a „see 1 above” nem fej; a P fokozatai a 4. pont alpontjai
        self.assertEqual([self.ut('H2403', n) for n in (13, 14, 15, 16)], ['-/4/-', '-/4/a', '-/4/b', '-/4/c'])

    def test_tabla_h3117_below_3_below(self):
        # seed-102 M198/M201
        self.assertEqual([self.ut('H3117', n) for n in (10, 11, 12)], ['-/2/-', '-/2/d', '-/2/e'])

    def test_tabla_h3588_dr_nb(self):
        # seed-101 M004: „(see Dr N.B.) 2” nem fej; a 3. pont folytatódik
        self.assertEqual([self.ut('H3588', n) for n in (18, 19, 20)], ['-/3/a', '-/3/b', '-/3/c'])

    def test_tabla_h9004_hivatkozas_es_fej(self):
        # seed-101 M184: „see 3b. b.” = b.; a „(see היה II. 2 c)” nem fej
        self.assertEqual([self.ut('H9004', n) for n in (7, 8)], ['-/1/b', '-/1/b'])

    def test_tabla_h2471_sorrendsertes(self):
        # seed-101 M154
        self.assertEqual(self.ut('H2471', 9), '-/2/d')

    def test_tabla_h5676_csoport_a_szam_alatt(self):
        # seed-102 M226: „1 … A. east Jordan … B. West Jordan … 2”
        self.assertEqual([self.ut('H5676', n) for n in (5, 6, 7)], ['-.A/1/-', '-.B/1/-', '-/2/-'])

    def test_tabla_h7812_hithpalel(self):
        # seed-102 M223/M233
        self.assertEqual([self.ut('H7812', n) for n in (5, 6, 7)], ["Hithpa'lel/-/-", "Hithpa'lel/1/-", "Hithpa'lel/1/a"])

    def test_tabla_belso_fejek(self):
        # DT-F185b (a): a bekezdés közepi fej a sorbelső oszlopban (seed-102 M056/M194 H3452; seed-101 M117 H0539 a 2.31 kézi
        # soraival; M057 H4994 „3b, c. c.”; seed-102 M042 H5066 „, 1 human subject”); a sor `utvonal`-a a sor eleji állapot
        self.assertEqual(self.t[('H3452', '3')]['belso_fejek'].split('|')[1:], ['b.', '-/-/b'])
        self.assertEqual([f.split('|')[2] for f in self.t[('H0539', '8')]['belso_fejek'].split(';')], ["Niph'al/-/-", "Niph'al/1/-"])
        self.assertEqual(self.t[('H4994', '12')]['belso_fejek'].split('|')[1:], ['3b, c. c.', '-/4/c'])
        self.assertEqual(self.t[('H5066', '3')]['belso_fejek'].split('|')[1:], ['1', 'Qal/1/-'])
        self.assertEqual(self.ut('H3318', 3), 'Qal/1/-')     # 2.31 kézi: a hiányzó „Qal” a sor eleji jelölőhöz

    def test_forditasok_kulcsai_valtozatlanok(self):
        # DT-F185b (a), kötelező: a `forditasok.tsv` minden BDB `sz<n>` sorának kulcsa megvan, és a szakasz-nézet hash-e a sor
        # `forras_hash`-ével egyezik (az F185 előtt 29 311 / 29 311; a sorbelső fejek és a hamis fejek a `jel` + `szoveg`-et nem
        # változtatják)
        import re
        import szakasz_bemenet as sb
        ford = []
        with open(os.path.join(GYOKER, 'adat', 'forditasok.tsv'), encoding='utf-8') as f:
            for sor in f:
                m = sor.rstrip('\n').split('\t')
                if len(m) > 5 and m[0] == 'BDB' and re.match(r'^sz\d+$', m[3]):
                    ford.append((m[1], int(m[3][2:]), m[5]))
        h = {}
        for st in sorted({x[0] for x in ford}):
            for x in sb.szakaszok(st) or []:
                h[(st, int(x['sorszam']))] = x['hash']
        rossz = [x for x in ford if h.get(x[:2]) != x[2]]
        self.assertEqual(rossz, [])
        self.assertGreaterEqual(len(ford), 29311)

    def test_tabla_sorszam_nem_valtozik(self):
        # az F185 szabályai sort nem vágnak: a fordítások (`forditasok.tsv` sz<n>) és a 2.31 horgonyai érvényesek maradnak
        self.assertEqual(len(self.t), 36621)


class F202Szocikkhatar(unittest.TestCase):
    """F202.2 (C1/C2, N147): a nyitott zárójelet záró rövid blokk az előző szócikk vége, nem a következő szócikk-kezdet része."""

    @classmethod
    def setUpClass(cls):
        _, sorok = tabla()
        cls.t = {(d['strong'], d['sorszam']): d for d in sorok}

    def test_egyseg(self):
        self.assertTrue(bont.zarojel_folytatas('be rejected (compare Niph`al', 'Niph`al )'))
        self.assertTrue(bont.zarojel_folytatas('the reign of (compare מַלְכוּת', '2, מַמְלָכוּת 3).'))
        self.assertFalse(bont.zarojel_folytatas('closed (here) text', 'Niph`al )'))
        self.assertFalse(bont.zarojel_folytatas('open (here', 'II. [מָאַס] verb Niph`al flow (Aramaic id.)'))

    def test_valos(self):
        # (Strong, a töredék sorszáma, az előző szócikk, a következő szócikk feje)
        for st, n, elozo, kov in (('H3988', 9, 'BDB4494', 10), ('H4467', 6, 'BDB4679', None), ('H5973', 30, 'BDB6145', 31),
                                  ('H7704', 7, 'BDB8170', 8)):
            d = self.t[(st, str(n))]
            self.assertEqual(d['bdb_id'], elozo, (st, n))
            self.assertNotEqual(d['utvonal'], 'fej', (st, n))
            if kov:
                k = self.t[(st, str(kov))]
                self.assertNotEqual(k['bdb_id'], elozo, (st, kov))
                self.assertEqual(k['utvonal'], 'fej', (st, kov))


class Determinizmus(unittest.TestCase):
    def test_ellenoriz(self):
        with open(TABLA, encoding='utf-8') as f:
            ts = f.readline().split('--ts ')[1].split(' ')[0]
        r = subprocess.run([sys.executable, os.path.join(ITT, 'bont.py'), '--ts', ts, '--ellenoriz', '--lista', '0'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_javitas_ellenoriz(self):
        with open(os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv'), encoding='utf-8') as f:
            elso = f.readline()
        ts = elso.split('--ts ')[1].split(' ')[0]
        tsh = elso.split('--ts-heber-sorrend ')[1].split(' ')[0] if '--ts-heber-sorrend ' in elso else ts
        tsa = elso.split('--ts-atiras ')[1].split(' ')[0] if '--ts-atiras ' in elso else ts
        tsv = elso.split('--ts-hivatkozott-vers ')[1].split(' ')[0] if '--ts-hivatkozott-vers ' in elso else ts
        tst = elso.split('--ts-tanu ')[1].split(' ')[0] if '--ts-tanu ' in elso else ts
        # F185: a Sefaria-gyorsítótár nélkül (üres útvonal) a rögzített Sefaria-ítéletek maradnak (SEMA 2.31 `tanu`): a tábla
        # gyorsítótárral és anélkül is bájtra azonos
        r = subprocess.run([sys.executable, os.path.join(ITT, 'forras_javit.py'), '--ts', ts, '--ts-heber-sorrend', tsh,
                            '--ts-atiras', tsa, '--ts-hivatkozott-vers', tsv, '--ts-tanu', tst, '--sefaria-cache', '',
                            '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
