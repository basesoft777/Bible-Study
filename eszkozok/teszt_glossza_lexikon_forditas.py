#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_glossza_lexikon_forditas.py -- F121: a mankók (szójegyzék-egyenérték, Károli-alakok, BDB-egyezés) és a
UBS_DBH forrásszöveg-feloldó tesztje. Hermetikus: ideiglenes könyvtár.

    python eszkozok/teszt_glossza_lexikon_forditas.py
"""
import os
import shutil
import sys
import tempfile
import unittest
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossza_lexikon_forditas as G  # noqa: E402


def sor(mezo='glosszak_hu', hu='nevezni; nevet adni', strong='H7121'):
    return {'szotar': 'UBS_DBH', 'strong': strong, 'entry_id': '006562001008000', 'jelentes_szam': G.EM_DASH, 'mezo': mezo,
            'forditas_hu': hu, 'megjegyzes': ''}


class Segedek(unittest.TestCase):
    def test_elemek_zarojel_nelkul(self):
        self.assertEqual(G.elemek('to acknowledge (a deity); to name'), ['to acknowledge', 'to name'])
        self.assertEqual(G.elemek(' ; '), [])

    def test_tovek_toldalekolas_ellen(self):
        self.assertIn('kiál', G.tovek('kiáltani'))
        self.assertIn('neve', G.tovek('nevezni; nevet adni'))
        self.assertNotIn('valaki', {t for t in G.tovek('valakinek lenni')})   # kötőszó/általános szó kimarad

    def test_ellenorzendo_szavak(self):
        self.assertEqual(G.ellenorzendo_szavak('glosszak_hu', 'találkozni'), 'találkozni')
        self.assertEqual(G.ellenorzendo_szavak('definicio_hu', 'szó szerint: kiáltani; innen: = olyan cselekvés'), 'kiáltani')
        self.assertEqual(G.ellenorzendo_szavak('definicio_hu', '= olyan cselekvés, amellyel emberek'), '')   # leíró definíció


class Szojegyzek(unittest.TestCase):
    TABLA = {'to name': Counter({'nevezni': 3}), 'authority': Counter({'hatalom': 1})}

    def test_egyezik(self):
        a, _ = G.szojegyzek_ellenorzes(sor(hu='nevezni; nevet adni'), 'to name; to call', self.TABLA)
        self.assertEqual(a, 'egyezik')

    def test_utkozik_versengo_alak(self):
        a, r = G.szojegyzek_ellenorzes(sor(hu='név; felhatalmazás'), 'name; authority', self.TABLA)
        self.assertEqual(a, 'utkozik')
        self.assertIn('hatalom', r)

    def test_nincs_adat_es_definicio(self):
        self.assertEqual(G.szojegyzek_ellenorzes(sor(hu='keresni'), 'to look for', self.TABLA)[0], 'nincs_adat')
        self.assertEqual(G.szojegyzek_ellenorzes(sor(mezo='definicio_hu'), 'x', self.TABLA)[0], 'nem_glossza')


class Karoli(unittest.TestCase):
    def setUp(self):
        self.mappa = tempfile.mkdtemp()
        with open(os.path.join(self.mappa, 'parok_1Moz.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('vers\thu_sorszam\thu_szo\ter_sorszam\ter_szo\tstrong\tbizonyossag\tforras\n')
            for st, szo in (('H7121', 'Nevezé'), ('H7121', 'nevezé'), ('H7121', 'kiálta'), ('H8034', 'neve'), ('G1941', 'segítségül')):
                f.write('\t'.join(['1Móz 1:1', '1', szo, '1', 'x', st, 'magas', 'teszt']) + '\n')
            f.write('\t'.join(['1Móz 1:2', '1', 'nullás', '1', 'x', 'H0430', 'magas', 'teszt']) + '\n')   # a nullával kitöltött alak is egyezik

    def tearDown(self):
        shutil.rmtree(self.mappa)

    def test_alakok_strongra_nullakkal_is(self):
        c = G.karoli_alakok_strongra('H7121', self.mappa)
        self.assertEqual(c['nevezé'], 2)
        self.assertEqual(G.karoli_alakok_strongra('H430', self.mappa)['nullás'], 1)       # H430 ~ H0430
        self.assertEqual(G.karoli_alakok_strongra('G1941', self.mappa)['segítségül'], 1)

    def test_egyezik_es_nem_talal(self):
        k = G.karoli_alakok_strongra('H7121', self.mappa)
        self.assertEqual(G.karoli_ellenorzes(sor(hu='nevezni; nevet adni'), k)[0], 'egyezik')
        self.assertEqual(G.karoli_ellenorzes(sor(hu='találkozni'), k)[0], 'nem_talal')
        self.assertEqual(G.karoli_ellenorzes(sor(mezo='definicio_hu', hu='= olyan cselekvés'), k)[0], 'nincs_ellenorzendo')


class Bdb(unittest.TestCase):
    def test_egyezes_es_nem_heber(self):
        self.assertEqual(G.bdb_ellenorzes(sor(hu='kiáltani'), 'hívni, kiáltani, olvasni')[0], 'egyezik')
        self.assertEqual(G.bdb_ellenorzes(sor(hu='keresni'), 'hívni, kiáltani')[0], 'nem_talal')
        self.assertEqual(G.bdb_ellenorzes(sor(strong='G1941'), 'x')[0], 'nem_heber')


class DbhForras(unittest.TestCase):
    def test_feloldo_az_elso_sort_adja(self):
        mappa = tempfile.mkdtemp()
        try:
            with open(os.path.join(mappa, 'UBS_DBH_jelentesek.tsv'), 'w', encoding='utf-8', newline='') as f:
                f.write('# GENERALT\nstrong\tlexid\tdefinicio_rovid\tglosszak\n')
                f.write('H8034\t1\tELSO\tname\nH8034\t1\tMASODIK\tname2\n')
            idx = G.dbh_forras_idx(mappa)
            self.assertEqual(idx[('H8034', '1', 'definicio_hu')], 'ELSO')
            self.assertEqual(idx[('H8034', '1', 'glosszak_hu')], 'name')
            self.assertEqual(G.forras_szoveg_dbh({'szotar': 'UBS_DBH', 'jelentes_szam': G.EM_DASH, 'strong': 'H8034',
                                                  'entry_id': '1', 'mezo': 'definicio_hu'}, idx), 'ELSO')
            self.assertIsNone(G.forras_szoveg_dbh({'szotar': 'BDB', 'jelentes_szam': G.EM_DASH, 'strong': 'H8034',
                                                   'entry_id': '1', 'mezo': 'definicio_hu'}, idx))
        finally:
            shutil.rmtree(mappa)


class TovabbiForras(unittest.TestCase):
    """F121 (DT-F121k): a TBESH/TBESG/tW/MCGED/LSJ/BDB-nyelvi háttér sor forrásszövege a konkordancia-fájlokból."""

    def setUp(self):
        self.m = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.m)

        def ir(nev, szoveg):
            with open(os.path.join(self.m, nev), 'w', encoding='utf-8', newline='') as f:
                f.write(szoveg)
        ir('TBESH.txt', 'H7585\tH7585 =\tH7585\tשְׁאוֹל\tshe.ol\tN:N--L\thell: Sheol\tSheol, underworld<br>1a) the underworld<br>\n')
        ir('TBESG.txt', "G0086\tG0086 =\tG0086\tᾍδης\tHadēs\tG:N-M\thell: Hades\t <b>ᾅδης</b> <BR />__1. <ref='Luk.16.23'>Luk.16:23;</ref>\n")
        ir('tW_szocikkek.tsv', 'tw_id\tkategoria\tcim\tstrong\tszoveg\tforras_commit\n'
           'kt/hades\tkt\tHades\tH7585+G0086\t# Hades\\n\\ntext\tabc\n')
        ir('MCGED_teljes.tsv', 'strong\tgk_szam\tlemma_gorog\tatirat\tgyakorisag\tglossza\nG0086\tG50087\tx\ty\t1\tthe abode of the dead\n')
        ir('LSJ_teljes.tsv', 'Strong_padded\tStrong_eredeti\tTeljes_szocikk\nG0086\tG86\tLSJ-szöveg\n')
        ir('BDB_etimologia_kezi_hatarok.tsv', 'strong\tallapot\tnyelvi_hatter\tszocikk_hossz\thatar_pozicio\nH7585\tx\tH7585. sheol\t5\t5\n')

    def _f(self, szotar, strong, eid, jsz, mezo):
        return G.tovabbi_forras({'szotar': szotar, 'strong': strong, 'entry_id': eid, 'jelentes_szam': jsz, 'mezo': mezo}, self.m, {})

    def test_tbes_7_8_oszlop_tisztitva(self):
        self.assertEqual(self._f('TBESH', 'H7585', 'H7585', 'teljes', 'forditas_hu'), 'hell: Sheol Sheol, underworld 1a) the underworld')
        self.assertEqual(self._f('TBESG', 'G0086', 'G0086', 'teljes', 'forditas_hu'), "hell: Hades ᾅδης __1. Luk.16:23;")

    def test_tw_elso_strong_a_kulcs(self):
        self.assertEqual(self._f('tW_szocikkek', 'H7585', 'kt/hades', G.EM_DASH, 'forditas_hu'), '# Hades\\n\\ntext')
        self.assertIsNone(self._f('tW_szocikkek', 'G0086', 'kt/hades', G.EM_DASH, 'forditas_hu'))

    def test_mcged_lsj_bdb(self):
        self.assertEqual(self._f('MCGED', 'G0086', 'G50087', G.EM_DASH, 'glosszak_hu'), 'the abode of the dead')
        self.assertEqual(self._f('LSJ', 'G0086', 'G0086', 'teljes', 'forditas_hu'), 'LSJ-szöveg')
        self.assertEqual(self._f('BDB', 'H7585', 'H7585', 'nyelvi_hatter', 'forditas_hu'), 'H7585. sheol')

    def test_tbesg_rovid_a_7_oszlop_strongonkent_az_elso_sor(self):
        with open(os.path.join(self.m, 'TBESG.txt'), 'a', encoding='utf-8', newline='') as f:
            f.write('G0071\tG0071 =\tG0071\tἄγω\tagō\tG:V\t to bring \tdef\nG0071a\tx\tx\tx\tx\tG:V\tMÁSIK\tdef\n')
        self.assertEqual(self._f('TBESG', 'G0071', 'G0071', 'rovid', 'glosszak_hu'), 'to bring')
        self.assertIsNone(self._f('TBESG', 'G0071', 'G0072', 'rovid', 'glosszak_hu'))
        self.assertIsNone(self._f('TBESH', 'H7585', 'H7585', 'rovid', 'glosszak_hu'))

    def test_negativ_ismeretlen_kulcs_vagy_mezo(self):
        self.assertIsNone(self._f('BDB', 'H7585', 'H7585', 'teljes', 'forditas_hu'))      # a teljes szócikk más feloldó dolga
        self.assertIsNone(self._f('LSJ', 'G0086', 'G86', 'teljes', 'forditas_hu'))
        self.assertIsNone(self._f('TBESH', 'H9999', 'H9999', 'teljes', 'forditas_hu'))
        self.assertIsNone(self._f('Thayer', 'G0086', 'G86', 'teljes', 'forditas_hu'))


class Kulcsszo(unittest.TestCase):
    def test_kulcs_a_forrasban_es_karoli_bdb(self):
        s = {'strong': 'H7585'}
        term = [('Sheol', 'Seol'), ('underworld', 'alvilág'), ('see', 'l.'), ('hell', 'pokol')]
        ki = G.kulcsszo_ellenorzes(s, 'Sheol, the underworld; see hell', term, Counter({'seolba': 5, 'pokol': 2}), 'az alvilág')
        self.assertEqual(ki, [('Sheol', 'Seol', 'egyezik', 'nem_talal'), ('underworld', 'alvilág', 'nem_talal', 'egyezik'),
                              ('hell', 'pokol', 'egyezik', 'nem_talal')])        # a 'see' -> 'l.': nincs tartalmas tő, kimarad
        self.assertEqual(G.kulcsszo_ellenorzes({'strong': 'G0086'}, 'hell', term, Counter({'pokol': 3}), '')[0][3], 'nem_heber')


class Lista(unittest.TestCase):
    """F203 (N-F12e): a lista csak a lapon látszó hiányt listázza, a repóba nem ír, és render nélkül megáll."""

    def test_latszo_es_rejtett_hiany(self):
        hivasok = {('BDB', 'H0127', 'H0127', '3', 'forditas_hu'): (False, G.JELOLO % 0),
                   ('TBESG', 'G3956', 'G3956', 'rovid', 'glosszak_hu'): (False, G.JELOLO % 1),
                   ('UBS_DBH', 'H0127', 'x', G.EM_DASH, 'glosszak_hu'): (True, None)}
        latszo, rejtett = G.latszo_hianyok(hivasok, 'title="G3956 · %s"' % (G.JELOLO % 1))
        self.assertEqual(latszo, [('TBESG', 'G3956', 'G3956', 'rovid', 'glosszak_hu')])
        self.assertEqual(rejtett, [('BDB', 'H0127', 'H0127', '3', 'forditas_hu')])

    def test_jelolo_nem_elotag_utkozes(self):
        # a jelölő zárt (⟦GLF:1⟧ nem része a ⟦GLF:12⟧-nek), így az 1-es kulcs nem látszik a 12-es jelölőtől
        hivasok = {('A',): (False, G.JELOLO % 1), ('B',): (False, G.JELOLO % 12)}
        self.assertEqual(G.latszo_hianyok(hivasok, G.JELOLO % 12), ([('B',)], [('A',)]))

    def test_kimenet_nem_a_repoban(self):
        d = tempfile.mkdtemp()
        try:
            self.assertEqual(G.kimeneti_ut(d), os.path.join(d, G.LISTA_NEV))
            self.assertFalse(os.path.abspath(G.kimeneti_ut(d)).startswith(G.GYOKER))
            self.assertEqual(G.kimeneti_ut(d, '/x/y.tsv'), '/x/y.tsv')
        finally:
            shutil.rmtree(d)

    def test_render_nelkul_megall(self):
        regi = G.lista_keszit
        G.lista_keszit = lambda mid, kim: {}
        d = tempfile.mkdtemp()
        try:
            with self.assertRaises(SystemExit):
                G.lista('NINCS-001', d)
            self.assertEqual(os.listdir(d), [])
        finally:
            G.lista_keszit = regi
            shutil.rmtree(d)

    def test_kimenet_a_repoban_tilos(self):
        with self.assertRaises(SystemExit):
            G.lista('X-001', os.path.join(G.GYOKER, 'naplok'))

    def test_szakasz_cimke_levezet_alapkimenete_a_repon_kivul(self):
        import szakasz_cimke_levezet as SCL
        self.assertFalse(os.path.abspath(SCL.ki_ut_alap('ALVIL-001')).startswith(G.GYOKER))


if __name__ == '__main__':
    unittest.main(verbosity=2)
