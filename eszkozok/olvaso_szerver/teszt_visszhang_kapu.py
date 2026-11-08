#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_visszhang_kapu.py -- F178.5 (DT-F178d, DT-F178e): a 4.11 visszhang-blokk regressziós
kapuja (`olvasoi_kapu.ell_visszhang`, V1–V7) és a blokk gépi szabályai (`lexikon_general`: a főnév igei töve, a
mássalhangzós átírás, a láncbeli jelentés). Arany minta: a HAMART-001 lapjának 4.11 blokkja — a kapu ott 0 BUKÁS-t ad;
szándékosan rontott másolaton szabályonként jelez. A `teszt_futtat.py --gyors` része.

    python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ESZKOZOK)
import olvasoi_kapu as K  # noqa: E402

LAP = os.path.join(os.path.dirname(ESZKOZOK), 'lexikon', 'HAMART-001_TUDOMANYOS.md')
OVATOS = 'hogy ez a szó szokásos fordítása-e, ebből a forrásból nem mérhető.'


def arany_blokk():
    """A HAMART-001 4.11 blokkja (a „#### 4.11.” címtől a „#### 4.12.” címig), a fölötte álló szakaszcímmel."""
    with open(LAP, encoding='utf-8') as f:
        t = f.read().replace('\r\n', '\n')
    a = t.index('#### 4.11. ')
    b = t.index('#### 4.12. ', a)
    return '## 4. Szótári háttér\n\n' + t[a:b]


def visszhang(szoveg):
    return [x for x in K.ell_visszhang(K.tagol(szoveg)) if x['sulyossag'] == K.BUKAS]


def szabalyok(szoveg):
    return {x['uzenet'].split(' ', 1)[0] for x in visszhang(szoveg)}


def sor(mit, lxx='γῆ (gé) · 4/4'):
    return '| X<br>1:1, 2:1 | a (a) · 2/2 | *b* · 2/2 | %s | %s |' % (lxx, mit)


def tabla(*sorok):
    return '## 4. Szótári háttér\n\n#### 4.11. Visszhang\n\n| Lánc-szó · versek | Targum | Vulgata | LXX | Mit mutat |\n' \
           '|---|---|---|---|---|\n' + '\n'.join(sorok) + '\n'


class Arany(unittest.TestCase):
    def test_hamart_4_11_tiszta(self):
        self.assertEqual([], visszhang(arany_blokk()))

    def test_hamart_teljes_lap_nincs_visszhang_bukas(self):
        with open(LAP, encoding='utf-8') as f:
            tal, _ = K.lap_meres(f.read(), kh=False, atvett=False, arany=False)
        self.assertFalse([t for t in tal if t['azonosito'] == 'VISSZHANG' and t['sulyossag'] == K.BUKAS])


class Rontott(unittest.TestCase):
    def setUp(self):
        self.b = arany_blokk()

    def test_v1_angol_maradek(self):
        r = self.b.replace('| megvet, meggyaláz |', '| megvet, meggyaláz; see be shaken |', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V1', szabalyok(r))

    def test_v2_ujheber_sor(self):
        r = self.b.rstrip('\n') + '\n| קָלַל (kálal) | újhéber קָלַל (kálal) | azonos a bibliai héberrel | — |\n'
        self.assertIn('V2', szabalyok(r))

    def test_v3_nincs_a_nem_azonositott_helyen(self):
        r = self.b.replace('a rokon írások lekérdezése a BDB-szócikket nem azonosította; a helyi BDB-szövegben rokon '
                           'nyelvi alak nem áll', 'a BDB-szócikkben nincs rokon nyelvi adat', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V3', szabalyok(r))

    def test_v3_azonositott_szocikknel_nincs_rendben(self):
        self.assertNotIn('V3', szabalyok(self.b))   # chámász: azonosított szócikk, rokon alak nélkül

    def test_v4_ugyanaz_a_szo_ket_lemmanal(self):
        r = tabla(sor('A LXX: ugyanaz a szó mind a 2 láncversben.', 'φθείρω (ftheiró) · καταφθείρω (kataftheiró) · 2/2'))
        self.assertIn('V4', szabalyok(r))
        self.assertNotIn('V4', szabalyok(tabla(sor('A LXX: ugyanaz a szócsalád mind a 2 láncversben.',
                                                   'φθείρω (ftheiró) · καταφθείρω (kataftheiró) · 2/2'))))

    def test_v5_kiemelt_alapvonal_nelkul(self):
        self.assertIn('V5', szabalyok(tabla(sor('**A Targum a láncban mindkét héber szót egy szóval adja vissza.**'))))
        self.assertNotIn('V5', szabalyok(tabla(sor('**LXX: a láncon kívül csak a versek 20%-ában (10 vers) ez áll: a '
                                                   'láncban más szót választ, mint máshol.**'))))

    def test_v6_ovatos_mondat_ismetlese_a_cellakban(self):
        """A b7494f2a hibája: az óvatos mondat soronként kétszer, négy sorban — a kapunak meg kell fognia."""
        mit = 'A Targum: ugyanaz a szó mind a 2 láncversben; %s A Vulgata: ugyanaz a szó mind a 2 láncversben; %s' % (
            OVATOS, OVATOS)
        self.assertIn('V6', szabalyok(tabla(sor(mit), sor(mit))))
        self.assertNotIn('V6', szabalyok(tabla(sor('LXX: a héber szó a láncon kívül nem fordul elő, az alapvonal '
                                                   'nem mérhető.'))))

    def test_v7_alapvonal_sav(self):
        rossz = tabla(sor('LXX: a láncon kívül a versek 46%-ában (50 vers) ez áll.'))
        jo = tabla(sor('LXX: a láncon kívül a versek 46%-ában (50 vers) ez áll: a szó gyakori, de nem kizárólagos '
                       'fordítása.'))
        self.assertIn('V7', szabalyok(rossz))
        self.assertNotIn('V7', szabalyok(jo))


class GepiSzabalyok(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import lexikon_general as LG
        cls.LG = LG

    def test_fonev_igei_tove(self):
        self.assertEqual('H2554', self.LG.bdb_to_strong('H2555'))   # חָמָס → חָמַס
        self.assertEqual('H6087', self.LG.bdb_to_strong('H6093'))   # עִצָּבוֹן → עָצַב
        self.assertIsNone(self.LG.bdb_to_strong('H2554'))           # ige: nincs töve

    def test_massalhangzos_atiras(self):
        self.assertEqual('k-l-l-m', self.LG.massalhangzos_atiras('קללם'))

    def test_lancbeli_jelentes_pielben(self):
        self.assertEqual('megátkozni (Piél)', self.LG.lanc_szo_jelentes('H7043', ['1Móz 8:21']))


if __name__ == '__main__':
    unittest.main()
