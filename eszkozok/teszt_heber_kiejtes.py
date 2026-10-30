"""A gépi magyaros héber kiejtés tesztjei (eszkozok/heber_kiejtes.py; DT-F131y, N-F131w).

  python -m unittest -q eszkozok.teszt_heber_kiejtes

A két kalibráló minta esetei az `eszkozok/teszt_heber_kiejtes_esetek.tsv`-ben (generálja:
naplok/HEBER_KIEJTES_tesztesetek.py): az `egyezik` soroknál a kiejtés a felhasználó (illetve a 2. mintán a
jelölő) által elfogadott alakok egyike; az `ismert_elteres` soroknál a DT-F131y döntése tudatosan eltér a
jelöléstől, ott a mai kimenet van rögzítve (a változás így látszik).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heber_kiejtes as HK  # noqa: E402

ESETEK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'teszt_heber_kiejtes_esetek.tsv')


def esetek():
    with open(ESETEK, encoding='utf-8') as f:
        sorok = [l.rstrip('\r\n') for l in f if l.strip() and not l.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


class KalibraloMintak(unittest.TestCase):
    def test_elfogadott_alakok(self):
        hibak = []
        for e in esetek():
            if e['allapot'] != 'egyezik':
                continue
            ki = HK.kiejt(e['heber'], int(e['elotag_hossz']), e['makkef'] == 'igen')
            if ki not in e['elfogadott'].split('|'):
                hibak.append('%s/%s %s: %r nem elfogadott (%s)' % (e['minta'], e['sorszam'], e['heber'], ki, e['elfogadott']))
        self.assertEqual(hibak, [])

    def test_ismert_elteresek_rogzitve(self):
        for e in esetek():
            if e['allapot'] != 'ismert_elteres':
                continue
            self.assertTrue(e['ok'] and 'NINCS OK' not in e['ok'], e)
            self.assertEqual(HK.kiejt(e['heber'], int(e['elotag_hossz']), e['makkef'] == 'igen'), e['gepi'], e)

    def test_esetszam(self):
        es = esetek()
        self.assertEqual(len(es), 100)
        self.assertEqual(sum(e['allapot'] == 'egyezik' for e in es), 91)


class Szabalyok(unittest.TestCase):
    def test_r1_szamech_es_sin_sz(self):
        self.assertEqual(HK.kiejt('כִּסֵּא'), 'kisszé')          # כִּסֵּא
        self.assertEqual(HK.kiejt('עָשָׂה'), 'ászá')                 # עָשָׂה
        self.assertEqual(HK.kiejt('שֵׁם'), 'sém')                                # שֵׁם

    def test_r2_kamec_a_es_kiveteli_lista(self):
        self.assertEqual(HK.kiejt('הָיְתָה'), 'hájtá')         # הָיְתָה (R4: meteg nélkül néma)
        self.assertEqual(HK.kiejt('כָּל'), 'kol')                                # כָּל
        self.assertEqual(HK.kiejt('חָכְמָה'), 'chochmá')        # חָכְמָה
        self.assertEqual(HK.kiejt('שִׁבֳּלִים'), 'sibbolím')  # hátef-kámec

    def test_r3_seva_torokhang_elott(self):
        self.assertEqual(HK.kiejt('קִרְאוּ'), 'kireú')         # קִרְאוּ

    def test_r5_r5b_begadkefat(self):
        betu = 'בְשֵׁם'                                                # בְשֵׁם
        self.assertEqual(HK.kiejt(betu, elotag_hossz=1), 'vesém')                                    # ב-előtag: lágy
        self.assertEqual(HK.kiejt('בְרִית'), 'berít')                 # tő-kezdet: kemény
        self.assertEqual(HK.kiejt('וּבֹקֵעַ', elotag_hossz=1), 'úbókéa')  # R5b
        self.assertEqual(HK.kiejt('בְךָ', elotag_hossz=1), 'vechá')             # előtag + toldalék

    def test_r6_tetragramma(self):
        self.assertEqual(HK.kiejt('יְהוָה'), 'Jahve')
        self.assertEqual(HK.kiejt('לַיהוָה', elotag_hossz=1), 'la-Jahve')
        self.assertEqual(HK.kiejt('בַּיהוָה', elotag_hossz=1), 'ba-Jahve')

    def test_r7_jeruzsalem_minden_alakja(self):
        alap = 'יְרוּשָׁלִַם'           # יְרוּשָׁלִַם
        self.assertEqual(HK.kiejt(alap), 'jerúsálajim')
        self.assertEqual(HK.kiejt('ירוּשָׂלִָם'), 'jerúsálajim')  # sinnel, jod pont nélkül
        self.assertEqual(HK.kiejt('יְרוּשָׁלְַמָה'), 'jerúsálajmá')
        self.assertEqual(HK.kiejt('וּבִירוּשָׁלִַם', elotag_hossz=2), 'úvírúsálajim')

    def test_r8_chet(self):
        self.assertEqual(HK.kiejt('חָמָס'), 'chámász')

    def test_pontozatlan_nincs_kiejtes(self):
        self.assertEqual(HK.kiejt('קרא'), '')

    def test_teljes_szo(self):
        sorok = [{'Strong-szám': 'H9001', 'Ragozott alak': 'וַ', 'Kiejtés': 'va'},
                 {'Strong-szám': 'H7121', 'Ragozott alak': 'יִּקְרָא', 'Kiejtés': "i.yik.Ra'"},
                 {'Strong-szám': 'H0853', 'Ragozott alak': 'אֶת', 'Kiejtés': "'et-"},
                 {'Strong-szám': 'H8034', 'Ragozott alak': 'שְׁמ', 'Kiejtés': 'she.M'},
                 {'Strong-szám': 'H9023', 'Ragozott alak': 'וֹ', 'Kiejtés': 'o'}]
        alak, elotag, makkef = HK.teljes_szo(sorok, 1)
        self.assertEqual((elotag, makkef), (1, False))
        self.assertEqual(HK.kiejt(alak, elotag, makkef), 'vajjikrá')
        alak, elotag, makkef = HK.teljes_szo(sorok, 3)
        self.assertEqual(HK.kiejt(alak, elotag, makkef), 'semó')
        self.assertEqual(HK.teljes_szo(sorok, 2)[2], True)


if __name__ == '__main__':
    unittest.main()
