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
        """A felhasználó (2026-11-11): a lap elején egyszerűsített kolofon — a motívum, a negatív elhatárolás, a
        fölérendelt fogalom, olvasói alakban; a teljes azonosító tábla a Kolofonban."""
        eleje = self.lap.split('\n## Kivonat\n', 1)[0]
        for mezo in ('**A motívum.**', '**Mi tartozik ide, és mi nem.**', '**Fölérendelt fogalom**', '(#kolofon)'):
            self.assertIn(mezo, eleje)
        self.assertNotIn('| ID |', eleje)
        kolofon = self.lap.split('\n## Kolofon\n', 1)[1]
        for mezo in ('| ID | HAMART-001 |', '| Rövid cím |', '| Negatív kritérium |', '| Fölérendelt fogalom |'):
            self.assertIn(mezo, kolofon)
        self.assertIn('| Státusz | %s |' % LG.kiadasi_statusz('HAMART-001'), kolofon)
        for belso in ('| Kézi forrás |', '| Kereszthivatkozás-napló |'):
            self.assertNotIn(belso, kolofon)

    def test_sajat_adat_licence_a_nyilt_mag_szerint(self):
        """A felhasználó jelzése (2026-11-11): a nyílt magban kiadott saját adat nem „minden jog fenntartva”."""
        kolofon = self.lap.split('\n## Kolofon\n', 1)[1]
        for nev in ('Motívumtábla', 'Kapcsolat-tábla'):   # névelő nélkül (lap-javit HAMART-001)
            sor = [s for s in kolofon.split('\n') if s.startswith('| %s |' % nev)]
            self.assertTrue(sor and 'CC BY 4.0' in sor[0] and 'minden jog fenntartva' not in sor[0], nev)
        # az előfordulás-táblánál csak az adatoszlopok vannak a nyílt magban (ELLENOR_HAMART_lapkeret 1.)
        sor = [s for s in kolofon.split('\n') if s.startswith('| Motívum előfordulás-táblája |')]
        self.assertTrue(sor and 'adatoszlopok: CC BY 4.0' in sor[0] and 'magyarázat' in sor[0])
        sor = [s for s in kolofon.split('\n') if s.startswith('| Lexikon fordítástáblája |')]   # v8-átnézés, 4.
        self.assertTrue(sor and 'közkincs, minden jog fenntartva' not in sor[0])

    def test_olvasoi_licencek_generator(self):
        """ELLENOR_HAMART_lapkeret 1., 6.: a licenc-leképezés rontott bemenettel is (nem csak a commitolt lapon)."""
        projekt = LG.LC('projekt_adat')
        self.assertEqual(LG.olvasoi_licencek('adat/kapcsolatok.tsv', {projekt}), {LG.NYILT_MAG_LICENC})
        self.assertEqual(LG.olvasoi_licencek('adat/jeloltek.tsv', {projekt}), {LG.NYILT_MAG_LICENC})
        elo = LG.olvasoi_licencek('adat/elofordulasok.tsv', {projekt})
        self.assertTrue(len(elo) == 1 and 'magyarázat' in next(iter(elo)))
        ks = next(iter(LG.olvasoi_licencek('adat/karoli_strong', {projekt})))
        self.assertTrue(ks.startswith(LG.LC('Karoli_Strong_parok')) and (not LG.KAROLI_STRONG_DOI or LG.KAROLI_STRONG_DOI in ks))
        ford = next(iter(LG.olvasoi_licencek('adat/forditasok.tsv', {projekt, 'közkincs'})))
        self.assertNotIn('forrásszöveg közkincs', ford)
        self.assertIn('szótár saját soránál', ford)
        # a nyílt magon kívüli saját tábla licence nem változik
        self.assertEqual(LG.olvasoi_licencek('adat/tiltott_fordulatok.tsv', {projekt}), {projekt})
        self.assertNotIn('((', self.lap)

    def test_egyszerusitett_kolofon_az_adatbol(self):
        m = next(r for r in LG.G.tsv_beolvas(LG.os.path.join(LG.ADAT, 'motivumok.tsv'))[1] if r['id'] == 'HAMART-001')
        blokk = LG.egyszerusitett_kolofon(m)
        self.assertIn(m['negativ_kriterium'], blokk)
        self.assertIn(m['folerendelt_fogalom'][1:].rstrip('.'), blokk)
        import tablajegyzet as TJ   # a v8-átnézés (4.): az adatcella önreferáló „lap” fordulata a lapon olvasói alakban
        self.assertIn(TJ.onref_csere(blokk), self.lap)
        rontott = dict(m, negativ_kriterium='')
        self.assertIn('**Mi tartozik ide, és mi nem.** —', LG.egyszerusitett_kolofon(rontott))
        # lektor 1.: „A motívum.” nem a címet ismétli, hanem az azonosság hordozóját mondja
        self.assertNotIn('**A motívum.** %s' % m['cim'], blokk)
        self.assertIn(LG.AZONOSSAG_OLVASOI[m['azonossag_tipusa']], blokk)
        self.assertNotIn('hígul', blokk)

    def test_idezes_egy_helyen_helyorzo_nelkul(self):
        """A felhasználó döntései (2026-11-11): szerző, lexikon címe, kanonikus cím a beállításból; egy idézési forma
        (a Kolofonban), az Irodalomban mutató; nyers helyőrző nem áll; a HELYORZO kapu a rontott másolatra jelez."""
        self.assertIn('**Hogyan idézd.** %s: *%s*' % (LG.SZERZO_NEV, LG.LEXIKON_CIM_HU), self.lap)
        self.assertIn(LG.kanonikus_cim('HAMART-001'), self.lap)
        self.assertEqual(self.lap.count('**Hogyan idézd.**'), 1)
        self.assertIn('**Hogyan hivatkozz:** az idézési forma a [Kolofon](#kolofon)', self.lap)
        for nyers in ('<KANONIKUS_FORRAS_URL>', '[HELYŐRZŐ', '<DOI>', 'DOI: .'):
            self.assertNotIn(nyers, self.lap)
        import olvasoi_kapu as OK
        rontott = self.lap.replace(LG.kanonikus_cim('HAMART-001'), '<KANONIKUS_FORRAS_URL>', 1)
        regi = OK.KIVETEL_NELKUL
        OK.KIVETEL_NELKUL = True
        try:
            self.assertTrue(OK.ell_helyorzo(OK.tagol(rontott)))
            self.assertFalse(OK.ell_helyorzo(OK.tagol(self.lap)))
        finally:
            OK.KIVETEL_NELKUL = regi

    def test_modszertani_elvek_proza(self):
        self.assertNotIn('[A módszer Hays hét kritériumának tükrében](', self.lap)
        self.assertIn('**Módszertani elvek.** A bibliai intertextualitás-kutatás bevett mércéje', self.lap)
        self.assertNotIn('Rövid UI-címke', self.lathato)
        self.assertNotIn('publikálható (v1', self.lathato)

    def test_dontesi_ut_alcimek(self):
        """F182 javítókör (N155, DT760): az 1.1–1.2 alcím névszói, az 1.3–1.5 változatlan."""
        for c in ('### 1.1. A keresés tárgya', '### 1.2. A keresés forrásai', '### 1.3.', '### 1.4.', '### 1.5.'):
            self.assertIn(c, self.lap)
        self.assertNotIn('Mit keresünk', self.lap)
        self.assertNotIn('Hol kerestünk', self.lap)

    def test_a21_nincs_alkalmazas(self):
        self.assertNotIn('## 10. Alkalmazás', self.lap)
        # F183: a 9. szakasz a Hatástörténet, ezért a Módszertan a 11., az Irodalom a 12.
        self.assertIn('## 11. Módszertan és nyitott kérdések', self.lap)
        self.assertIn('## 12. Irodalom és idézés', self.lap)
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

    def test_szocikkhatar_kezi(self):
        """F182 javítókör (A17 / K56, DT761): a tételes szócikkhatár-javítás a következő szócikk fejénél vág; a forrás
        változásakor (a horgony nincs meg) a generálás megáll; a HAMART-001-en a 27. szabály nem jelez."""
        sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'bdb_jelolt'))
        import hu_illeszt as HI
        eredeti = dict(HI.SZOCIKKHATAR_KEZI)
        try:
            HI.SZOCIKKHATAR_KEZI.clear()
            HI.SZOCIKKHATAR_KEZI[('H1', '2')] = ('3', ' nőnemű főnév: x', 1, 'teszt')
            sor = lambda n, sz, k='0': ['H1', n, 'B', '', '', 'u', '', 'k', '', k, str(len(sz)), sz, 'h', 'p']
            ki = [sor('2', 'a vége. QQ nőnemű főnév: x y'), sor('3', '', '')]
            HI.szocikkhatar_kezi(ki, 'T')
            self.assertEqual(ki[0][11], 'a vége.')
            self.assertEqual(ki[1][11], 'QQ nőnemű főnév: x y')
            self.assertIn('scope=manual', ki[1][13])
            with self.assertRaises(HI.SzocikkhatarHiba):
                HI.szocikkhatar_kezi([sor('2', 'a vége, horgony nélkül'), sor('3', '', '')], 'T')
        finally:
            HI.SZOCIKKHATAR_KEZI.clear()
            HI.SZOCIKKHATAR_KEZI.update(eredeti)
        import ellenoriz as E
        _h, jelentes = E.gerinc_szocikk_hibak(os.path.join(GYOKER, 'adat'))
        self.assertEqual([j for j in jelentes if j.startswith('HAMART-001')], [])

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
        # F182 javítókör (DT760): a régi „1.2 Hol kerestünk” alcím már nem kivétel
        self.assertTrue(kapu(uj_lap('### 1.2. Hol kerestünk'), 'MI_HANG'))
        self.assertEqual(kapu(uj_lap('A helyek átnézésre kerültek. Alattuk és közöttük „vétkeztünk”.'), 'MI_HANG'), [])

    def test_nevelo(self):
        self.assertTrue(kapu(uj_lap('A arar önmagában nem a motívum, csak a adamá.'), 'NEVELO'))
        self.assertEqual(kapu(uj_lap('Az árar és az adámá; a föld.'), 'NEVELO'), [])

    def test_lista_nevelo(self):
        """lap-javit HAMART-001 (orkesztrátori tétel): lista- és táblaelem nem kezdődik kisbetűs névelővel."""
        for hibas in ('- a BDB-szótár (közkincs)', '| a Glossa Ordinaria | közkincs |', '* az LXX szövege'):
            self.assertTrue(kapu(uj_lap(hibas), 'LISTA_NEVELO'), hibas)
        for jo in ('- BDB-szótár (közkincs)', '| Glossa Ordinaria | közkincs |',
                   '1. **A föld elvesztése.** A szövetségi helyek.', 'A folyó szövegben a BDB-szótár áll.'):
            self.assertEqual(kapu(uj_lap(jo), 'LISTA_NEVELO'), [], jo)

    def test_nevelo_le_generator(self):
        """A generátor szabálya rontott bemenettel: a kisbetűs névelő lemarad, nagy kezdőbetű; a megjegyzés és a
        mondatkezdő „A” marad."""
        be = '\n'.join(['- a BDB-szótár (közkincs)', '| a föld színe | az ég | x |', '<!-- | a nyers | -->',
                        '1. A föld elvesztése.', '| a x <!-- a | b --> | y |'])
        ki = LG.nevelo_le(be).split('\n')
        self.assertEqual(ki[0], '- BDB-szótár (közkincs)')
        self.assertEqual(ki[1], '| Föld színe | Ég | x |')
        self.assertEqual(ki[2], '<!-- | a nyers | -->')
        self.assertEqual(ki[3], '1. A föld elvesztése.')
        self.assertEqual(ki[4], '| X <!-- a | b --> | y |')
        self.assertEqual(LG.olvasoi_forrasnev('adat/kapcsolatok.tsv'), 'a kapcsolat-tábla')
        self.assertEqual(LG.olvasoi_forrasnev('adat/kapcsolatok.tsv', nevelovel=False), 'Kapcsolat-tábla')
        self.assertEqual(LG.olvasoi_forrasnev('konkordancia/UBS_DBH_x.tsv'), 'az UBS Dictionary of Biblical Hebrew')
        self.assertEqual(kapu(LG.nevelo_le(uj_lap('- a BDB-szótár (közkincs)')), 'LISTA_NEVELO'), [])
        # ELLENOR_HAMART_lapjavit 4.: a mondat értékű cella a névelőt megtartja (nagybetűvel); a kódblokk védett
        ki = LG.nevelo_le('| a szótár a héber vagy a görög versszámozás szerint idézi a helyet | x |\n```\n- a kód\n```')
        self.assertEqual(ki.split('\n')[0], '| A szótár a héber vagy a görög versszámozás szerint idézi a helyet | x |')
        self.assertEqual(ki.split('\n')[2], '- a kód')

    def test_meghatarozas_kapu(self):
        """A felhasználó (2026-11-11): „hiányolom a motívum definíciót”: a „A motívum.” bekezdés és a Kolofon
        Meghatározás-sora; rontott bemenettel (üres, cím, csak az azonosság típusa, hiányzó Kolofon-sor)."""
        def lap(bek, kol='| Meghatározás | A bűn következménye a földre és az emberiségre terjed a lánc szavaival. |'):
            return uj_lap('x').replace('# 📖 X-001 — Minta', '# 📖 X-001 — Minta\n\n' + bek) + \
                '\n## Kolofon\n\n| Mező | Érték |\n|---|---|\n' + kol + '\n'
        jo = '**A motívum.** A bűn következménye a földre és az egész emberiségre terjed, hat szó láncán át.'
        self.assertEqual(kapu(lap(jo), 'MEGHATAROZAS'), [])
        for rossz in ('**A motívum.** Minta.', '**A motívum.**',
                      '**A motívum.** Szerkezeti motívum: azonosságát nem egyetlen szó adja, hanem egy szerkezet.'):
            self.assertTrue(kapu(lap(rossz), 'MEGHATAROZAS'), rossz)
        self.assertTrue(kapu(lap(jo, kol='| Azonosság típusa | x |'), 'MEGHATAROZAS'))
        self.assertIn('**Meghatározás**', self.lap.replace('| Meghatározás |', '**Meghatározás**')
                      if hasattr(self, 'lap') else _olvas(LAP).replace('| Meghatározás |', '**Meghatározás**'))

    def test_kh_masolt_kapu_rontott(self):
        """ELLENOR_HAMART_lapjavit: a KH_MASOLT kapu az új szerkezetű lapon BUKÁS-t ad a másolt listára."""
        lap = uj_lap('x').replace('## 2. Előfordulások', '## 6. Kereszthivatkozások\n\n#### Sof 1:9\n- Károli-KH: Mk 3:22-30')
        tal = [t for t in K.lap_meres(lap, kh=True, atvett=False, arany=False)[0] if t['azonosito'] == 'KH_MASOLT']
        self.assertTrue(tal and tal[0]['sulyossag'] == K.BUKAS, tal)

    def test_kh_reszlista_masolat(self):
        """Lektor 15.: a Sof 1:9 Károli-KH listája a Mt 12:22 listájának része (részlista-másolat); a történeti
        karantén-szabály (reszlista=False) nem látja, az új igen."""
        import karoli_kh_epseg as KHE
        kh, tsk = KHE.betolt()
        uj = KHE.gyanus_forrasok(kh, tsk)
        self.assertIn('Zep.1.9', uj)
        self.assertIn('Mat.12.22', uj['Zep.1.9'])
        self.assertNotIn('Zep.1.9', KHE.gyanus_forrasok(kh, tsk, reszlista=False))
        self.assertNotIn('Mat.12.22', uj)
        self.assertNotIn('#### Sof 1:9\n- Károli-KH', _olvas(LAP))

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


class Tablajegyzet(unittest.TestCase):
    """A felhasználó átnézése (2., 12.; „mehet így”): a jegyzetek és a forrássorok olvasói alakja, a 2. és 3. tábla
    jegyzetei a tábla alatt; a rejtett eredeti-megjegyzés marad."""

    def test_k_jegyzet(self):
        import tablajegyzet as TJ
        lath = ('forrás: TSK-ajánlás (1Móz 4:11, 4:12; szavazat: 2-4) · ‹K1› · döntés: szerkesztői döntés, 2026-10-18 '
                '· a kereszthivatkozások versszám-felmérése C. rész<!-- eredeti: E -->')
        self.assertEqual(TJ.olvasoi_jegyzet(lath), 'Forrás: TSK-ajánlás (1Móz 4:11, 4:12).')

    def test_e_jegyzet(self):
        import tablajegyzet as TJ
        lath = ('Forrás: ‹E1› · a héber szöveg (TAHOT) igazolja · a jelentés címkéje: BDB-példa: a BDB a Qal szakaszban '
                'maga idézi a helyet (a BDB-szótár versenkénti jelentései); ez a szerkesztői hozzárendelés (Qal → Qal) '
                'alá esik, a címke a finomabb útvonalé')
        self.assertEqual(TJ.olvasoi_jegyzet(lath),
                         'A héber szöveg (TAHOT) igazolja; a jelentés: a BDB a Qal szakaszban maga idézi a helyet.')

    def test_jegyzet_a_tabla_alatt(self):
        # a felhasználó v8-átnézése (1.): a táblajegyzet a tábla alatt, helyi számmal; a sorban csak a jel
        import tablajegyzet as TJ
        lap = '\n'.join(['## 2. Előfordulások', '', '| A | B |', '|---|---|', '| x[^1] | y[^1] |', '',
                         '[^1]: forrás: TSK-ajánlás (1Móz 4:11; szavazat: 2) · ‹K1›<!-- eredeti: E1 -->',
                         '[^k3]: forrás: Strong-keresés: אָרַר (árar) · ‹K1›', '',
                         '*A közös forrásmegjelölések: ‹K1› = forrás: a napló*<!-- eredeti: N -->', ''])
        ki = TJ.alkalmaz(lap)
        jel = '<sup class="lj"><a href="#j-2-1">2.1</a></sup>'
        self.assertIn('| x%s | y%s |' % (jel, jel), ki)
        self.assertIn('- <span class="lj-szam" id="j-2-1">2.1</span>Forrás: TSK-ajánlás (1Móz 4:11).<!-- eredeti: E1 -->',
                      ki)
        self.assertNotIn('[^1]', ki)
        # a táblában nem hivatkozott lábjegyzet a helyén marad
        self.assertIn('[^k3]: Forrás: szókeresés: אָרַר (árar).', ki)
        self.assertNotIn('‹K1›', re.sub(r'<!--.*?-->', '', ki, flags=re.S))
        self.assertIn('<!-- közös forrásmegjelölés: A közös forrásmegjelölések: ‹K1› = forrás: a napló --><!-- eredeti: N -->',
                      ki)

    def test_forras_sor(self):
        import tablajegyzet as TJ
        ki = TJ.alkalmaz('*Forrás: a lap munkaanyaga; a kapcsolat-tábla, 2026-11-12*<!-- eredeti: P -->')
        self.assertEqual(ki, '*Forrás: a kapcsolat-tábla.*<!-- eredeti: P -->')
        ki = TJ.alkalmaz('*(forrás: Nave tárgymutatója (1897); a Nave-témák magyar nevei, 2026-11-12)*<!-- eredeti: P -->')
        self.assertEqual(ki, '*(forrás: Nave tárgymutatója (1897); a Nave-témák magyar nevei)*<!-- eredeti: P -->')

    def test_a_lapon(self):
        lap = _olvas(LAP)
        lathato = re.sub(r'<!--.*?-->', '', lap, flags=re.S)
        for minta in (r'‹[A-Z]\d›', 'szerkesztői hozzárendelés', 'versszám-felmérése', r'\bU\d:'):
            self.assertIsNone(re.search(minta, lathato), minta)
        # a felhasználó átnézése (3.): a Jel 22:3 sora „— —” és gondolatjel-cella nélkül, a jegyzet egyszer, a görög
        # versnél nem a TAHOT-ra hivatkozik
        jel = next(s for s in lap.split('\n') if s.startswith('| [Jel 22:3]'))
        self.assertNotIn('— —', jel)
        self.assertNotIn('| — |', jel)
        refek = re.findall(r'href="#(j-[\d-]+)"', jel)
        self.assertEqual(len(refek), 1)
        jegyzet = next(s for s in lathato.split('\n') if 'id="%s"' % refek[0] in s)
        self.assertNotIn('TAHOT', jegyzet)


class KiadasElott(unittest.TestCase):
    """A kiadás előtti javítócsomag (a lektor és a Fable közös véleménye; a felhasználó: „Igen, egyben”, „Mindhármat”)."""

    def test_rag_es_nevelo(self):
        self.assertEqual([OK.szam_bol(n) for n in (46, 47, 100, 1000, 10, 3, 5, 112)],
                         ['ból', 'ből', 'ból', 'ből', 'ből', 'ból', 'ből', 'ből'])
        self.assertEqual([OK.nevelo_szam(n) for n in (1, 2, 5, 47, 50, 1000)], ['az', 'a', 'az', 'a', 'az', 'az'])
        self.assertIn('érint a 47-ből', OK.minosites(5, 6, 47, osszes=112, rag=True))
        self.assertIn('érint a 47-ból', OK.minosites(5, 6, 47, osszes=112))   # a régi lapok útja változatlan

    def test_lxx_hid(self):
        m = OK.lxx_hid(46, 6, 4, 1, 23, 11, 1, 0, ['az árar', 'a sáchat'])
        self.assertIn('két szón át vezet, az árar és a sáchat szaván', m)
        self.assertIn('ezek 11 megállapított versében', m)
        self.assertIn('11 versben a megfelelő nincs megállapítva és 1 versben a versszámozás', m)
        self.assertIn('szócsalád szerint 10/11 vers', m)
        self.assertNotIn('nem nyelvi', m)

    def test_szo_par_nelkul_nincs_kovetkeztetes(self):
        m = OK.lxx_szo_uj('a föld', 11, 0, 0, 0, 9, 0, 2, 0, False)
        self.assertIn('nincs újszövetségi párja', m)
        self.assertNotIn('Következtetés', m)

    def test_kiemeles_minden_motivumhely(self):
        sz = 'föld 1Móz 2:5, 9; 3:17, 23; 5:29'
        uj, t, h = LG.kiemel(sz, [('1Móz 3:17', 'a')], mark=True, extra={'1Móz 5:29', '1Móz 3:17'})
        self.assertIn('title="a motívum helye: 1Móz 5:29">5:29</mark>', uj)
        self.assertEqual(uj.count('<mark'), 2)
        self.assertEqual((t, h), (['a'], []))
        regi, _t, _h = LG.kiemel(sz, [('1Móz 3:17', 'a')], extra={'1Móz 5:29'})
        self.assertNotIn('5:29**', regi)

    def test_link_nevelo(self):
        import tablajegyzet as TJ
        self.assertEqual(TJ._szam_link_nevelo('az [2. Előfordulások](#2) és a [5. LXX](#5)'),
                         'a [2. Előfordulások](#2) és az [5. LXX](#5)')

    def test_kolofon_lektor(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            lek = os.path.join(d, 'lek.md')
            jav = os.path.join(d, 'jav.tsv')
            with io.open(lek, 'w', encoding='utf-8') as f:
                f.write('# x\n\nLektor: `lektor` subagent, `claude-fable-5-2`.\n\n## Lektor kérdései\n\n*kör (2026-11-11)*\n\n'
                        '**1. A › b**\n- x\n\n**2. C › d**\n\n## Orkesztrátori észrevételek\n\n**3. E**\n')
            with io.open(jav, 'w', encoding='utf-8') as f:
                f.write('id\thely\ttipus\tgond\tregi\tuj\tjavasolta\tjovahagyta\tdatum\tproveniencia\n'
                        'X-001\th\tpróza\thomályos\ta\tb\tclaude-opus-5-5\tfelhasználó\t2026.11.11\tscope=manual\n'
                        'X-001\th2\tpróza\thomályos\ta\tb\tclaude-opus-5-5\tfelhasználó\t2026.11.12\tscope=manual\n')
            sorok = LG.kolofon_lektor_uj('X-001', lektor_ut=lek, javitas_ut=jav)
        # a szerkesztői sor elöl (a felhasználó: „de ember hagyja jóvá és változtat”), a dátum tartományként
        self.assertEqual(sorok, ['| Szerkesztői átnézés és javítás | A teljes lapot a szerkesztő átnézte; a modell-lektor '
                                 'által jelzett helyek javítását ő hagyta jóvá, módosította vagy vetette el '
                                 '(2026.11.11–12) |',
                                 '| Modell-lektor (claude-fable-5-2) | 2 jelzett hely (2026.11.11) |'])
        self.assertEqual(LG._datum_tartomany(['2026-10-30', '2026-11-02']), '2026.10.30–2026.11.02')

    def test_a_lapon(self):
        lap = _olvas(LAP)
        lathato = re.sub(r'<!--.*?-->', '', lap, flags=re.S)
        self.assertNotIn('a kapcsolat nem nyelvi, csak tartalmi', lathato)
        self.assertNotIn('nem az újszövetségi szót használja', lathato)
        self.assertEqual(lathato.count('szóhíd két szón át vezet'), 3)          # a két 4.6 és az 5. szakasz
        self.assertIn('Ez a tábla a láncon belüli fordítói következetességet méri', lathato)
        self.assertIn('HCF (HistoricalChristianFaith', lathato)
        self.assertNotIn('az [2.', lathato)
        self.assertIn('érint a 47-ből', lathato)
        self.assertNotIn('leggyakoribb szava ugyanazokban', lathato)
        self.assertNotIn('| Emberi lektorálás |', lathato)
        self.assertRegex(lathato, r'\| Szerkesztői átnézés és javítás \|[^\n]*\n\| Modell-lektor \(claude-[\w.-]+\) \| '
                                  r'\d+ jelzett hely')
        jel = next(s for s in lap.split('\n') if s.startswith('| [Jel 22:3]'))
        self.assertIn('elátkozott — ', jel)
        self.assertIn(' (katathema) |', jel)
        self.assertIn('| G2652 |', jel)
        # az 5. szakasz: négy egyezés-érték, és a 4.6 szavankénti összege = az összesítés
        i = lap.index('## 5. LXX-fordítói döntések')
        ertekek = {s.split(' | ')[4] for s in lap[i:lap.index('## 6.', i)].split('\n')
                   if s.startswith('| ') and s.count(' | ') >= 5 and not s.startswith('| Igehely')}
        self.assertTrue({'egyező', 'ugyanaz a szócsalád', 'eltérő', 'nincs újszövetségi pár'} <= ertekek, ertekek)
        ossz = re.search(r'\*Összesítés: egyező=(\d+), ugyanaz a szócsalád=(\d+), eltérő=(\d+), nincs újszövetségi '
                         r'pár=(\d+)', lap)
        self.assertIsNotNone(ossz)
        mondatok = [s for s in lathato.split('\n') if 'ószövetségi versében áll' in s]

        def osszeg(minta):
            return sum(int(x) for s in mondatok for x in re.findall(r'(\d+) versben ' + minta, s))
        self.assertEqual(osszeg('ugyanaz a görög szó áll'), int(ossz.group(1)))
        self.assertEqual(osszeg('ugyanannak a szócsaládnak'), int(ossz.group(2)))
        # a 4.2: az 1Móz 5:29 az adámá (H0127) szócikkében is kiemelt (a sora az iccávón szaván áll)
        h0127 = lap[lap.index('##### H0127'):lap.index('##### H0423')]
        self.assertIn('title="a motívum helye: 1Móz 5:29"', h0127)


class TablaAlattiJegyzet(unittest.TestCase):
    """A felhasználó v8-átnézése (1.; „én ezt kértem, a lektor javaslatát vezesd végig”): a 2., 3. és 6. szakasz
    tábláinak jegyzetei közvetlenül a tábla alatt, helyi számozott listában; az azonos jegyzet egyszer."""

    def test_osszevonas_es_szamozas(self):
        import tablajegyzet as TJ
        lap = '\n'.join([
            '## 3. Kizárt', '', '| A |', '|---|', '| a[^k1] |', '| b[^k2] |', '| c[^k3] |', '', 'szöveg', '',
            '| B |', '|---|', '| d[^k4] |', '',
            '[^k1]: Forrás: X.<!-- eredeti: 1 -->', '[^k2]: Forrás: X.<!-- eredeti: 2 -->',
            '[^k3]: Forrás: Y.<!-- eredeti: 3 -->', '[^k4]: Forrás: X.<!-- eredeti: 4 -->', ''])
        ki = TJ.tabla_ala(lap)
        self.assertEqual(ki.count('id="j-3-1"'), 1)
        self.assertIn('| a<sup class="lj"><a href="#j-3-1">3.1</a></sup> |', ki)
        self.assertIn('| b<sup class="lj"><a href="#j-3-1">3.1</a></sup> |', ki)
        # az azonos szöveg egyszer, mindkét rejtett megjegyzéssel
        self.assertIn('- <span class="lj-szam" id="j-3-1">3.1</span>Forrás: X.<!-- eredeti: 1 --><!-- eredeti: 2 -->', ki)
        # a második tábla a szakaszon belül folytatja a számozást, és a listája a saját táblája alatt áll
        self.assertIn('id="j-3-3">3.3</span>Forrás: X.<!-- eredeti: 4 -->', ki)
        self.assertLess(ki.index('id="j-3-2"'), ki.index('szöveg'))
        self.assertGreater(ki.index('id="j-3-3"'), ki.index('| d'))
        self.assertNotIn('[^k', ki)

    def test_szamozatlan_szakasz_valtozatlan(self):
        import tablajegyzet as TJ
        lap = '\n'.join(['## Kolofon', '', '| A |', '|---|', '| a[^x] |', '', '[^x]: Forrás: X.', ''])
        self.assertEqual(TJ.tabla_ala(lap), lap)

    def test_a_lapon(self):
        lap = _olvas(LAP)
        self.assertEqual(re.findall(r'(?m)^\[\^[\w.-]+\]:', lap), [])
        szam = {}
        for m in re.finditer(r'(?m)^- <span class="lj-szam" id="j-(\d+)-\d+">', lap):
            szam[m.group(1)] = szam.get(m.group(1), 0) + 1
        # a Fable mérése: a 2. táblánál 47 helyett 18; a 3. szakasz táblái 270 helyett 46, a 6. 99 helyett 11
        self.assertEqual(szam, {'2': 18, '3': 46, '6': 11})
        celok = set(re.findall(r'id="(j-[\d-]+)"', lap))
        for h in set(re.findall(r'href="#(j-[\d-]+)"', lap)):
            self.assertIn(h, celok)


class Onreferencia(unittest.TestCase):
    """A felhasználó v8-átnézése (4. szabály): a „lap” szó az oldal önmagára utalásaként nem áll az olvasói szövegben."""

    def test_csere_a_megjegyzesen_kivul(self):
        import tablajegyzet as TJ
        ki = TJ.onref_csere('kérdés, amelyet a lap nem dönt el<!-- amelyet a lap nem dönt el -->')
        self.assertEqual(ki, 'kérdés, amelyet ez a vizsgálat nem dönt el<!-- amelyet a lap nem dönt el -->')

    def test_kapu_jelez(self):
        self.assertTrue(kapu(uj_lap('## 2. Előfordulások\n\nAzt a lap nem dönti el.\n'), 'ONREF'))
        self.assertFalse(kapu(uj_lap('## 2. Előfordulások\n\nA HODIT-001 motívum lapján áll.\n'), 'ONREF'))
        self.assertFalse(kapu(uj_lap('## Kolofon\n\nA lap technikai adatai.\n'), 'ONREF'))

    def test_a_lapon(self):
        import tablajegyzet as TJ
        lap = _olvas(LAP)
        self.assertEqual(TJ.onref_talalatok(lap), [])
        lathato = re.sub(r'<!--.*?-->|【.*?】|\*Proveniencia:.*?\*', '',
                         _olvas(os.path.join(GYOKER, 'motivumok', 'HAMART-001.md')), flags=re.S)
        self.assertIsNone(re.search(r'(?<![\w-])[Ll]ap(?:ja|on|ra|ról)?(?![\w-])', lathato))
        self.assertIn('Ez a szakasz azt mutatja meg, hogyan jutott el a vizsgálat az igehelyekig', lap)
        self.assertIn('A motívum 47 helyen, 54 versben áll: 23 a Genezisben', lap)


class GyorsKor(unittest.TestCase):
    """A kiadás előtti gyors kör (a felhasználó: „Gyors kör 1–4, utána kiadás”)."""

    def test_rovidített_sor_kiemelve(self):
        lap = _olvas(LAP)
        self.assertIn('lent 4, fent) <mark class="motivumhely" title="a motívum helye: 1Móz 12:3">1Móz 12:3</mark> …', lap)
        self.assertIn('átok alá vetni <mark class="motivumhely" title="a motívum helye: 1Móz 5:29">1Móz 5:29</mark> (J) …',
                      lap)
        # a kiemelő a folytatásos („3:17, 23”) és a könyvnév nélküli alakot is a teljes igehelyre köti
        ki = LG.kiemel('1Móz 3:17, 23 vö. 5:29', [], mark=True, extra=['1Móz 3:23', '1Móz 5:29'])[0]
        self.assertIn('title="a motívum helye: 1Móz 3:23">23</mark>', ki)
        self.assertIn('title="a motívum helye: 1Móz 5:29">5:29</mark>', ki)

    def test_kizarasok_horgony_a_cimre(self):
        lap = _olvas(LAP)
        mell = _olvas(os.path.join(GYOKER, 'lexikon', 'HAMART-001_KIZARASOK.md'))
        cimek = {LG._heading_slug(m.group(1)) for m in re.finditer(r'(?m)^#{2,4} (.*)$', mell)}
        linkek = re.findall(r'KIZARASOK\.md#([^)"\s]+)', lap)
        self.assertTrue(linkek)
        self.assertEqual([x for x in linkek if x not in cimek], [])
        self.assertEqual(LG.kizarasok_cim('amelyet a lap nem dönt el', 2), 'amelyet ez a vizsgálat nem dönt el — 2 vers')

    def test_kolofon_datum(self):
        lap = _olvas(LAP)
        self.assertRegex(lap, r'\| Szerkesztői átnézés és javítás \|[^\n|]*\(2026\.11\.11–12\) \|')
        self.assertIn('| Modell-lektor (claude-fable-5-2) | 43 jelzett hely (2026.11.11) |', lap)

    def test_szo_a_strong_mellett(self):
        import tablajegyzet as TJ
        minta = '\n'.join(['#### 4.5. Tömör', '', '**H0056** · x', '', '**G1311** · y', '', '#### 4.10. Kiejtés', '',
                           '**H0056** · אָבַל (ával)', ''])
        ki = TJ.strong_szo_elol(minta)
        self.assertIn('**אָבַל (ával)** — x · H0056', ki)
        self.assertIn('**G1311** · y', ki)
        self.assertIn('**אָבַל (ával)** · H0056', ki)
        lap = _olvas(LAP)
        hb = lap.split('\n### Héber szavak', 1)[1].split('\n### ', 1)[0]
        for alpont in ('4.5', '4.6', '4.10'):
            resz = hb.split('\n#### %s.' % alpont, 1)[1].split('\n#### ', 1)[0]
            self.assertIsNone(re.search(r'(?m)^\*\*H\d{4}\*\* ·', resz), alpont)
            self.assertRegex(resz, r'(?m)^\*\*אָבַל \(ával\)\*\* (?:— .* )?· H0056$')


if __name__ == '__main__':
    unittest.main()
