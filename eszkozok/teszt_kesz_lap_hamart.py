"""F182 (3. menet): a kész lap követelménylistájának (`sablonok/KESZ_LAP_KOVETELMENY.md` (a)) HAMART-tételei — generátor-,
kapu- és laptesztek. A lapra vonatkozó esetek a commitolt `lexikon/HAMART-001_TUDOMANYOS.md`-t és a mellékletét
olvassák (a generált kimenet); a kapuesetek rontott mintán is jeleznek; a régi szerkezetű lap kódútja nem változik.

Futtatás: python -m unittest teszt_kesz_lap_hamart (az eszkozok/ könyvtárból), vagy a teszt_futtat.py körében.
"""
import io
import os
import re
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexikon_general as LG  # noqa: E402
import olvasoi_kapu as K  # noqa: E402
import olvasoi_kovetkeztetes as OK  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAP = os.path.join(GYOKER, 'lexikon', 'HAMART-001_TUDOMANYOS.md')
MELLEKLET = os.path.join(GYOKER, 'lexikon', 'HAMART-001_KIZARASOK.md')


def _olvas(ut):
    with io.open(ut, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n')


def uj_lap(torzs):
    return '\n'.join(['# 📖 X-001 — Minta', '', '## 1. Döntési út', '', 'Bevezető.', '', '## 2. Előfordulások', '',
                      torzs, ''])


def kapu(szoveg, azon):
    return [t for t in K.lap_meres(szoveg, kh=False, atvett=False, arany=False)[0] if t['azonosito'] == azon]


class Lap(unittest.TestCase):
    """A generált HAMART-001 lap (a commitolt kimenet)."""

    @classmethod
    def setUpClass(cls):
        cls.lap = _olvas(LAP)
        cls.lathato = re.sub(r'<!--.*?-->', '', cls.lap, flags=re.S)

    def test_a02_azonosito_tabla_a_lap_elejen(self):
        eleje = self.lap.split('\n## Kivonat\n', 1)[0]
        for mezo in ('| ID | HAMART-001 |', '| Rövid cím |', '| Negatív kritérium |', '| Fölérendelt fogalom |'):
            self.assertIn(mezo, eleje)
        self.assertIn('| Státusz | %s |' % LG.kiadasi_statusz('HAMART-001'), eleje)
        self.assertNotIn('Rövid UI-címke', self.lathato)
        self.assertNotIn('publikálható (v1', self.lathato)

    def test_dontesi_ut_alcimek(self):
        """F182 javítókör (N-F182g, DT-F182p): az 1.1–1.2 alcím névszói, az 1.3–1.5 változatlan."""
        for c in ('### 1.1. A keresés tárgya', '### 1.2. A keresés forrásai', '### 1.3.', '### 1.4.', '### 1.5.'):
            self.assertIn(c, self.lap)
        self.assertNotIn('Mit keresünk', self.lap)
        self.assertNotIn('Hol kerestünk', self.lap)

    def test_a21_nincs_alkalmazas(self):
        self.assertNotIn('## 10. Alkalmazás', self.lap)
        self.assertIn('## 10. Módszertan és nyitott kérdések', self.lap)
        self.assertIn('## 11. Irodalom és idézés', self.lap)
        self.assertNotIn('Alkalmazás és tanítványság', self.lathato)
        self.assertNotIn('A hívő számára', self.lathato)

    def test_b10_kolofon_forrastabla(self):
        kolofon = self.lap.split('\n## Kolofon\n', 1)[1]
        self.assertIn('| Forrás | Licenc | Szakasz |', kolofon)
        self.assertNotIn('| Forrás | Fájl |', kolofon)
        nevek = [s.split('|')[1].strip() for s in kolofon.split('\n')
                 if s.startswith('| ') and s.count('|') == 4 and not s.startswith('| Forrás')]
        self.assertEqual(len(nevek), len(set(nevek)), 'a forrás egyszer áll')

    def test_a26_a09_jelmagyarazat(self):
        self.assertIn('**A szótári pontok** (4. Szótári háttér)', self.lap)
        self.assertNotIn('lXX-híd', self.lap)            # F182 javítókör (ELLENOR_F182 #7)
        self.assertNotIn('károli-megfelelők', self.lap)
        self.assertNotIn('study-jából', self.lap)
        self.assertNotIn('a lap munkaanyaga alakú', self.lathato)

    def test_a08_es_kh_labjegyzet(self):
        for t in ('proveniencia: forrás:', '| igazolas:', 'jelentes_szam', '(4/b. rész)', '(4/c. rész)', 'napló: ',
                  'indoklás (nyers)', 'halo=', 'lanc ±1', 'csatorna=', 'szamozas_elteres', 'forras_kereses'):
            self.assertNotIn(t, self.lathato, t)
        self.assertIsNone(re.search(r'\(\d+(?:/[a-z])?\. rész\)', self.lathato))   # F182 javítókör: „(7. rész)” sem

    def test_olvasoi_atiras_nyers_jelek(self):
        """F182 javítókör (ELLENOR_F182 #5, #6): az olvasói átírás a napló-utalást és a nyers jeleket olvasói alakra írja."""
        for be, tilos in (('forrás: `négyforrásos audit a napló §7 szerint, retroaktív N14 betöltés`', 'rész)'),
                          ('*Proveniencia: scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | n=2 | ts=2026-11-02T13:17Z '
                           '| csatorna=cli*', 'csatorna'),
                          ('| Jer 51:46 | — | x | — | szamozas_elteres | Septuaginta |', 'szamozas_elteres'),
                          ('a minősített jelöltek (forras_kereses: TSK / Károli-KH).', 'forras_kereses')):
            ki = LG.olvasoi_atiras(be)
            self.assertNotIn(tilos, re.sub(r'<!--.*?-->', '', ki), ki)
            self.assertEqual(kapu(uj_lap(re.sub(r'<!--.*?-->', '', ki)), 'NYERS_JEL'), [], ki)
        self.assertIsNone(re.search(r'sorszám \d+(?:, \d+)*\)', self.lathato))

    def test_a24_413_414(self):
        self.assertIn('#### 4.13. Károli-megfelelők', self.lap)
        self.assertIn('#### 4.14. Rejtett / hamis párhuzam', self.lap)
        self.assertNotIn('(Ennél a pontnál a lap nem közöl adatot', self.lap.split('#### 4.13.', 1)[1].split('### Miért')[0])
        self.assertIn('ezzel a módszerrel nem mérhető', self.lap)
        self.assertNotIn('### A motívum kulcsszavai', self.lap)

    def test_413_lista_es_proza_egy_alapon(self):
        """F182 javítókör (ELLENOR_F182 #9): a 4.13 listája a prózával egy alapon (szócsaládonként) számol, és a
        szótári alak szó („megromlik”, nem „megroml”)."""
        p413 = self.lap.split('#### 4.13. Károli-megfelelők', 1)[1].split('#### 4.14.', 1)[0]
        m = re.search(r'a חָמָס \(chámász\) (\d+) helyéből (\d+) helyen „erőszak”', p413)
        self.assertIsNotNone(m)
        lista = re.search(r'^- \*\*erőszak\*\* \((\d+)\)', p413, re.M)
        self.assertIsNotNone(lista)
        self.assertEqual(lista.group(1), m.group(2))
        self.assertNotIn('**megroml**', p413)
        self.assertIn('**megromlik**', p413)
        n_proza = int(re.search(r'a Károli (\d+) különböző magyar szót használ \(szócsaládonként\)', p413).group(1))
        self.assertEqual(n_proza, len(re.findall(r'^- \*\*', p413, re.M)))

    def test_a15_rokon_tabla_a_48_ban(self):
        heber = self.lap.split('### Héber szavak', 1)[1]
        p48 = heber.split('#### 4.8. Nyelvi háttér', 1)[1].split('#### 4.9.', 1)[0]
        self.assertIn('##### Háttér: rokon nyelvek (BDB)', p48)
        self.assertNotIn('a 2. szerepben', p48)
        self.assertIn('#### 4.11. Visszhang: ókori fordítások\n', self.lap)

    def test_nincs_belso_utvonal(self):
        self.assertIsNone(re.search(r'(?<![\w./-])(?:adat|konkordancia|naplok)/\w', self.lathato))

    def test_a11_a12_magyar_cimek(self):
        self.assertIsNone(re.search(r'(?<![\w/])(?:kt|other)/[a-z]', self.lathato))
        self.assertNotIn('Destroy', self.lathato)
        self.assertNotIn('szónézet: /szo/', self.lathato)

    def test_a19_egy_forras(self):
        self.assertEqual(LG.lxx_egyforras_ellenoriz('HAMART-001', [
            s for s in self.lap.split('## 5. LXX-fordítói döntések', 1)[1].split('## 6.', 1)[0].split('\n')
            if s.startswith('| ') and not s.startswith('| Igehely')]), [])

    def test_olvasoi_kapu_0_bukas(self):
        tal = K.lap_meres(self.lap)[0]
        self.assertEqual([t for t in tal if t['sulyossag'] == K.BUKAS], [])


class Melleklet(unittest.TestCase):
    """A23: a kizárt helyek melléklete és a kapuja."""

    def test_melleklet_unio(self):
        m = _olvas(MELLEKLET)
        versek = []
        for sor in m.split('\n'):
            mm = re.match(r'^- \*\*(.+?)\*\* \(\d+\): (.*)$', sor)
            if mm:
                versek += ['%s %s' % (mm.group(1), v) for v in mm.group(2).split(', ')]
        szam = re.search(r'= ([\d  ]+) vers\.', m).group(1)
        self.assertEqual(len(versek), len(set(versek)))
        self.assertEqual(len(versek), int(re.sub(r'\D', '', szam)))

    def test_kapu_rontott_csoport(self):
        eredeti = LG.csoport_egyedi
        try:
            def rontott(mid):
                d = dict(eredeti(mid))
                h = next(iter(d))
                n, tagok = d[h]
                d[h] = (n, tagok[:-1])   # egy tag hiányzik
                return d
            LG.csoport_egyedi = rontott
            m = {'id': 'HAMART-001'}
            import general as G
            _, elo = G.tsv_beolvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv'))
            with self.assertRaises(LG.MellekletHiba):
                LG.kizarasok_adat(m, [r for r in elo if r['id'] == 'HAMART-001'])
        finally:
            LG.csoport_egyedi = eredeti


class Generator(unittest.TestCase):
    def test_alkalmazas_kivezetes_csak_hamart(self):
        self.assertTrue(LG.res_kivezetett('HAMART-001', 'alkalmazas'))
        self.assertFalse(LG.res_kivezetett('ISTENTISZT-001', 'alkalmazas'))

    def test_jelolt_labjegyzet(self):
        t = LG.jelolt_labjegyzet_olvasoi('forrás: TSK 1Móz 6:5 (25); Károli-KH is; napló: a motívum korábbi '
                                         'kereszthivatkozás-naplója (4/b. rész) | ‹K1›')
        self.assertEqual(t, 'forrás: TSK-ajánlás (1Móz 6:5; szavazat: 25); a Károli-kereszthivatkozás is · ‹K1›')
        self.assertNotIn('nyers', LG.jelolt_labjegyzet_olvasoi('forrás: x · indoklás (nyers): y'))

    def test_torzs_glossza(self):
        self.assertEqual(LG.gondolatjel_utani_glossza(
            'Hithpa`el — perfectum הִתְאַבֵּל 1Sám 15:35; participium מִתְאַבֵּל 1Sám 16:1; — gyászolni (többnyire próza)'),
            'gyászolni')
        self.assertEqual(LG.gondolatjel_utani_glossza('Niph`al: megromlani, elrontódni, perfectum 3.'),
                         'megromlani, elrontódni')

    def test_jelmagyarazat_kisbetu(self):
        """F182 javítókör (ELLENOR_F182 #7): a mozaikszó és a tulajdonnév nem lesz kisbetűs („lXX-híd”, „károli-…”)."""
        self.assertEqual(LG.kisbetus_kezdes('LXX-híd'), 'LXX-híd')
        self.assertEqual(LG.kisbetus_kezdes('Károli-megfelelők'), 'Károli-megfelelők')
        self.assertEqual(LG.kisbetus_kezdes('Alapjelentés'), 'alapjelentés')
        self.assertEqual(LG.kisbetus_kezdes('Rejtett / hamis párhuzam'), 'rejtett / hamis párhuzam')
        j = LG.szotari_pontok_jelmagyarazat()
        self.assertIn('4.6 LXX-híd', j)
        self.assertIn('4.13 Károli-megfelelők', j)
        self.assertNotIn('lXX', j)
        self.assertNotIn('károli', j)

    def test_bdb_fej_es_szamlalo(self):
        s = '**A szócikk feje (nyelvi háttér).** H7451. ra \' I. רַע‎_226 melléknév'
        s = LG.BDB_SZAMLALO_RX.sub('', LG.BDB_FEJ_NYERS_RX.sub(r'\1', s))
        self.assertEqual(s, '**A szócikk feje (nyelvi háttér).** I. רַע melléknév')

    def test_lxx_egyforras_rontott(self):
        idx = LG.vh_lxx_index('HAMART-001')
        (vers, st), (lemma, _k) = next(((k, v) for k, v in idx.items() if v[0] == 'γῆ'))
        kulcsszo = LG._heber_kulcsszo_strong(vers, st)
        sor = '| %s | %s | %s | ἄκανθα (akantha) | eltérő | Septuaginta |' % (vers, vers, kulcsszo)
        self.assertTrue(LG.lxx_egyforras_ellenoriz('HAMART-001', [sor]))

    def test_lxx_sajat_par_1moz_3_17(self):
        """F182 javítókör (ELLENOR_F182 #4): az 5. szakaszban a héber kulcsszó a saját LXX-párjával áll (1Móz 3:17:
        adámá ↔ γῆ), nem a vers egy másik motívumszavával (ἐπικατάρατος, az árar párja); a kapu a régi párosítást jelzi."""
        import general as G
        _, elo = G.tsv_beolvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv'))
        sorai = [r for r in elo if r['id'] == 'HAMART-001']
        tabla = LG.lxx_osszevetes(sorai, LG.motivum_strong_tokenek(sorai))[0]
        s317 = [s for s in tabla if s.startswith('| 1Móz 3:17 |')]
        self.assertEqual(len(s317), 1)
        self.assertIn('γῆ', s317[0])
        self.assertNotIn('ἐπικατάρατος', s317[0])
        self.assertNotIn('| egyező |', s317[0])
        self.assertEqual(LG.lxx_egyforras_ellenoriz('HAMART-001', tabla), [])
        kulcsszo = LG._heber_kulcsszo_strong('1Móz 3:17', 'H0127')
        rontott = '| 1Móz 3:17 | 1Móz 3:17 | %s | ἐπικατάρατος (epikataratosz) | egyező | Septuaginta |' % kulcsszo
        self.assertTrue(LG.lxx_egyforras_ellenoriz('HAMART-001', [rontott]))


class Kovetkeztetes(unittest.TestCase):
    def test_a03_sulypont_es_szovetseg(self):
        sz = OK.elofordulasok_uj(47, 41, 6, 14, [('1Móz', 23), ('Ez', 5)], 42, konyvnev=lambda k: 'Mózes első könyve')
        self.assertIn('súlypontja Mózes első könyve (47 helyből 23)', sz)
        self.assertIn('főként ószövetségi; az Újszövetségben 6 hely', sz)
        self.assertNotIn('mindkét szövetség', sz)

    def test_a07_harmadik_szemely(self):
        sz = OK.kizart_uj(236, 1506, 30, 1742, 0, [('ok', 887)], [('TSK-ajánlás', 99)], 47)
        self.assertIsNone(re.search(r'vizsgáltunk|kerestük|döntöttünk|megnéztük', sz))

    def test_a13_a20_versben_es_kis_elemszam(self):
        self.assertIn('46 versre terjednek', OK.lxx_uj(46, 7, 27, 0, 12))
        self.assertNotIn('Következtetés', OK.lxx_szo('az אָבַל (ával)', 3, 0, 0, 0, 3))

    def test_a14_sece_csak_parnal(self):
        sz = OK.sece_csoport('héber', [('a שָׁחַת (sáchat)', 7, ['διαφθείρω (diaftheiró)']), ('az אָבַל (ával)', 5, [])])
        self.assertEqual(sz.count('Következtetés'), 1)
        self.assertIsNone(OK.sece_csoport('héber', []))

    def test_a16_csoportositott_kis_elemszam(self):
        sz = OK.versenkenti_csoport('görög', 'újszövetségi', [('a x', 1, 0, ['Jel 11:18']), ('a y', 1, 1, [])], 2)
        self.assertNotIn('Következtetés', sz)
        self.assertIn('Jel 11:18', sz)


class Kapuk(unittest.TestCase):
    """Az új HIBA-kapuk: a rontott minta jelez, a régi szerkezetű lapon nem futnak."""

    def test_nyers_jel(self):
        for hibas in ('[^1]: proveniencia: forrás: x | igazolas: y', 'napló: a motívum naplója (4/b. rész)',
                      'tW: kt/curse', 'a szó: [szónézet: /szo/G1](/szo/G1)', '| adat/karoli_strong | x |', 'רַע‎_226 melléknév',
                      # F182 javítókör (ELLENOR_F182 #5, #6)
                      '[^k1]: forrás: a motívum kereszthivatkozás-naplójában (7. rész), utólagos betöltés',
                      '*Forrás: a héber szöveg, 2026-11-02 | csatorna=cli*', '| Jer 51:46 | — | x | — | szamozas_elteres |',
                      'a minősített jelöltek (forras_kereses: TSK / Károli-KH).'):
            self.assertTrue(kapu(uj_lap(hibas), 'NYERS_JEL'), hibas)
        self.assertEqual(kapu(uj_lap('Forrás: a jelöltek döntésnaplója, 2026-11-11.'), 'NYERS_JEL'), [])
        self.assertEqual(kapu('# X\n\n## 2. Előfordulások\n\nnapló: x\n', 'NYERS_JEL'), [])

    def test_mi_hang(self):
        self.assertTrue(kapu(uj_lap('A szavakat átnéztük, és a helyeket elbíráltuk.'), 'MI_HANG'))
        # F182 javítókör (DT-F182p): a régi „1.2 Hol kerestünk” alcím már nem kivétel
        self.assertTrue(kapu(uj_lap('### 1.2. Hol kerestünk'), 'MI_HANG'))
        self.assertEqual(kapu(uj_lap('A helyek átnézésre kerültek. Alattuk és közöttük „vétkeztünk”.'), 'MI_HANG'), [])

    def test_nevelo(self):
        self.assertTrue(kapu(uj_lap('A arar önmagában nem a motívum, csak a adamá.'), 'NEVELO'))
        self.assertEqual(kapu(uj_lap('Az árar és az adámá; a föld.'), 'NEVELO'), [])

    def test_indoklas(self):
        """F182 javítókör (ELLENOR_F182 #8): az indoklásban írás kiejtés nélkül, más sorra hivatkozás, munkajavaslat."""
        for hibas in ('| Jób 31:40 | x | **elutasítva** — tövis: más szavakat használt (חוֹחַ, בָּאְשָׁה) |',
                      '| Luk 1:6 | x | **elutasítva** — ok: Az „Isten előtt” (לִפְנֵי) kifejezés |',
                      '| Mt 13:7 | x | **elutasítva** — ok: kettős szókapcsolatával (ἄκανθα + τρίβολος együtt) |',
                      '| Ez 28:17 | x | **elutasítva** — ok: A hely az Ez 28:16 sorának folytatása. |',
                      '| Ez 7:6 | x | **elutasítva** — ok: önálló motívum-jelöltként érdemes lehet külön vizsgálatra |'):
            self.assertTrue(kapu(uj_lap(hibas), 'INDOKLAS'), hibas)
        for jo in ('| Jób 31:40 | x | **elutasítva** — tövis: (חוֹחַ (chóach) és בָּאְשָׁה (bosá)) |',
                   '| Róm 8:21 | x | **beépítve** — a romlás (φθορά, fthora) és az אֲדָמָה (adámá: föld) |',
                   '| Ez 7:23 | x | **beépítve** — מָלְאָה ... חָמָס (málá ... chámász) |',
                   '| Jób 14:1 | x | **elutasítva** — a rokon [עֶצֶב](/szo/H6089)<sup class="strong" title="H6089">H6089</sup> '
                   '(ecev) szót |',
                   'Prózában a חָמָס szó, döntéscella nélkül.'):
            self.assertEqual(kapu(uj_lap(jo), 'INDOKLAS'), [], jo)
        self.assertEqual(kapu('# X\n\n## 3. Kizárt\n\n| a | x | **elutasítva** — (לִפְנֵי) |\n', 'INDOKLAS'), [])

    def test_kov_ism(self):
        mondat = '**Következtetés:** a szó itt nem a motívum.'
        self.assertTrue(kapu(uj_lap('\n\n'.join([mondat] * 3)), 'KOV_ISM'))
        self.assertEqual(kapu(uj_lap('\n\n'.join([mondat] * 2)), 'KOV_ISM'), [])


if __name__ == '__main__':
    unittest.main()
