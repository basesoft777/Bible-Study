#!/usr/bin/env python
"""A magyar BDB-szakaszillesztés F144-es szabályainak tesztjei (eszkozok/bdb_jelolt/hu_illeszt.py, DT-F144a):
R2 (a vesszős kötetszámú siglum utáni számsor nem jelölő), R4 (a törzsnév a forrás szerinti előfordulás-indexéhez kötődik),
R3x (a sor első jelölője nem kötődhet a következő sor törzsneve mögé), és a részleges frissítés fejléc-jelölése.

Futtatás: python eszkozok/bdb_jelolt/teszt_hu_illeszt.py   (a „Valos” osztály az adat/bdb_szakaszok.tsv-t és az
adat/forditasok.tsv-t olvassa: H0001, H2199 (b), H7043 (c, R3x), H3499 (a)).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import hu_illeszt as hi  # noqa: E402


def sor(jel, szoveg, jelolo='point'):
    return {'jel': jel, 'jelolo': jelolo, 'szoveg': szoveg}


class Szabalyok(unittest.TestCase):
    def test_r2_vesszos_siglum(self):
        # H0001: „Sabean אב CIS^iv, 1, 37 1. 2 és mások” — a számsor a kötet lapszáma, nem jelölő
        hu = 'szabeus אב CIS^iv, 1, 37 1. 2 és mások; — 1 az egyén atyja 1Móz 2:24'
        poz = [p for p, j in hi.magyar_jelolok(hu) if j in ('1', '2')]
        self.assertEqual(poz, [hu.index('1 az egyén')])
        # a pontos kötetszámú siglum (4) változatlan, és a siglum nélküli számsor jelölő marad
        self.assertIn('2', [j for _, j in hi.magyar_jelolok('esetleg Che^Hpt. 2 nyomorúságban')])

    def test_r4_torzs_elofordulas_index(self):
        # a forrás egyszer említi a Hiph'ilt a sor előtt, ezért a jelölő a magyar második előfordulásához kötődik
        sorok = [sor('', 'x', 'fej'),
                 sor('Qal', 'cry; compare Hiph`il below'),
                 sor('Hiph`il', 'call out Judg 4:10')]
        hu = 'fej. Qal kiált; vö. a lenti Hiph`il. Hiph`il kihív Bír 4:10'
        e = hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(e[2][:3], ['illeszkedik', "T:Hiph'il", hu.rindex('Hiph`il')])

    def test_r4_index_nelkul_a_regi_viselkedes(self):
        # ha a forrás előtt nincs azonos törzsnév, az első előfordulás a kurzortól (a régi viselkedés)
        sorok = [sor('', 'x', 'fej'), sor('Hiph`il', 'call out Judg 4:10')]
        hu = 'fej. Hiph`il kihív Bír 4:10'
        self.assertEqual(hi.strong_illeszt(sorok, hu)[0][1][2], hu.index('Hiph`il'))

    def test_r3x_kovetkezo_torzs_moge_nem(self):
        # H7043-szerű: a „3” jelölő a magyarban csak a következő sor Pu`alja után (a ragozás személye) állna,
        # ezért a sor elakad, és a horgony-lépés a fejezet:versnél köti; a Pu`al a saját helyére kerül
        sorok = [sor('', 'x', 'fej'),
                 sor('3', 'with accusative Gen 8:21'),
                 sor('Pu`al', 'Imperfect 3 masculine singular Isa 65:20')]
        hu = 'fej. a dolog tárgyesetével 1Móz 8:21. Pu`al imperfectum 3. hímnemű egyes szám Ézs 65:20'
        e = hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(e[1][0], 'horgonnyal')
        self.assertEqual(e[2][:3], ['illeszkedik', 'T:Pu`al'.replace('`', "'"), hu.index('Pu`al')])

    def test_reszleges_jeloles_megmarad(self):
        # a korábbi részleges frissítés jelölése megmarad, az azonos Strong-halmazé cserélődik (ismételhető)
        fej = ('# GENERÁLT: x --ts 2026-10-18 — y.' + hi.RESZLEGES + ' H8034 (--strong, ts=2026-10-29; a, b); a többi.',
               '# forras: z', 'strong\tsorszam\tx')
        regi = '\n'.join(fej + ('H0001\t1\ta', 'H8034\t1\tb')) + '\n'
        uj = hi.reszleges_szoveg(regi, [['H0001', '1', 'A']], {'H0001'}, '2026-11-01')
        elso = uj.split('\n')[0]
        self.assertIn(hi.RESZLEGES + ' H8034 (--strong, ts=2026-10-29;', elso)
        self.assertIn(hi.RESZLEGES + ' H0001 (--strong, ts=2026-11-01;', elso)
        self.assertEqual(hi.reszleges_szoveg(uj, [['H0001', '1', 'A']], {'H0001'}, '2026-11-01'), uj)


class Valos(unittest.TestCase):
    """A javított szócikkek a mai adaton (adat/bdb_szakaszok.tsv + adat/forditasok.tsv, csak olvasva)."""

    @classmethod
    def setUpClass(cls):
        with open(hi.TABLA, encoding='utf-8', newline='') as f:
            s = f.read().split('\n')
        fej = s[2].split('\t')
        cls.tab = {}
        for x in s[3:]:
            if x:
                d = dict(zip(fej, x.split('\t')))
                cls.tab.setdefault(d['strong'], []).append(d)
        cls.ford = hi.forditasok()

    def _sor(self, st, sorszam):
        sorok, hu = self.tab[st], self.ford[st]['forditas_hu']
        e = hi.strong_illeszt(sorok, hu)[0]
        i = next(i for i, x in enumerate(sorok) if x['sorszam'] == sorszam)
        return e[i], hu

    def test_h0001_fejlec_szamtoredek(self):
        (kat, _, p), hu = self._sor('H0001', '3')
        self.assertEqual(kat, 'illeszkedik')
        self.assertTrue(hu[p:].startswith('1 az egyén atyja'), hu[p:p + 30])
        (kat, _, p), hu = self._sor('H0001', '4')
        self.assertTrue(hu[p:].startswith('2 Istenről'), hu[p:p + 30])

    def test_h2199_torzs_emlites_b(self):
        (kat, _, p), hu = self._sor('H2199', '13')
        self.assertTrue(hu[p:].startswith('Hiph`il imperfectum'), hu[p:p + 30])
        (kat, _, p), hu = self._sor('H2199', '14')
        self.assertTrue(hu[p:].startswith('1 hív'), hu[p:p + 30])

    def test_h7043_ragozasi_szemely_r3x(self):
        (kat, _, p), hu = self._sor('H7043', '15')
        self.assertEqual(kat, 'horgonnyal')
        self.assertTrue(hu[p:].startswith('3 a dolog'), hu[p:p + 30])
        (kat, _, p), hu = self._sor('H7043', '16')
        self.assertEqual(kat, 'illeszkedik')
        self.assertTrue(hu[p:].startswith('Pu`al'), hu[p:p + 30])

    def test_h3499_szerkezeti_kivetel_a(self):
        # (a): a „csak a jelölő” sorok forrássora is üres vagy legfeljebb 8 karakter — indokolt kivétel (A′ szerint nem hiba)
        import re
        sorok, hu = self.tab['H3499'], self.ford['H3499']['forditas_hu']
        e = hi.strong_illeszt(sorok, hu)[0]
        poz = sorted(set([0] + [x[2] for x in e if x[2] is not None]))
        for x, (kat, jel, p) in zip(sorok, e):
            if kat == 'illeszkedik' and x['jel']:
                kov = next((q for q in poz if q > p), len(hu))
                if len(hu[p:kov].strip()) <= len(x['jel']) + 3:
                    self.assertLessEqual(len(re.sub(r'<[^>]+>', '', x['szoveg']).strip()), 8, x['sorszam'])


class SzakaszEgyAzEgyhez(unittest.TestCase):
    """F123.BDBILL (DT-F123y): a szakaszonként fordított Strong `sz<n>` sorai igazolt 1:1-ben a szakasztábla soraihoz."""

    @staticmethod
    def _szak(*szovegek):
        import szakasz_bemenet as sb
        return [{'sorszam': i + 1, 'jel': '', 'utvonal': '', 'szoveg': t, 'hash': sb.sha1(t)} for i, t in enumerate(szovegek)]

    @staticmethod
    def _sz(n, hu, hash_):
        return {'jelentes_szam': 'sz%d' % n, 'forditas_hu': hu, 'forras_hash': hash_}

    def test_igazolt(self):
        szak = self._szak('1 animal:', 'a. in general')
        sz11, ok = hi.szakasz_egyezes([self._sz(1, '1 állat:', szak[0]['hash']), self._sz(2, 'a. általában', szak[1]['hash'])], szak)
        self.assertIsNone(ok)
        self.assertEqual(sz11, {1: '1 állat:', 2: 'a. általában'})

    def test_hash_elteres_nem_igazolt(self):
        szak = self._szak('1 animal:', 'a. in general')
        sz11, ok = hi.szakasz_egyezes([self._sz(1, '1 állat:', szak[0]['hash']), self._sz(2, 'a. általában', 'x')], szak)
        self.assertIsNone(sz11)
        self.assertIn('forras_hash', ok)

    def test_szakaszszam_elteres_nem_igazolt(self):
        szak = self._szak('1 animal:', 'a. in general')
        sz11, ok = hi.szakasz_egyezes([self._sz(1, '1 állat:', szak[0]['hash'])], szak)
        self.assertIsNone(sz11)
        self.assertIn('szakaszszám', ok)

    def test_szakasz_sorok_kezdet(self):
        # a hu_kezdet a közös összefűző szövegében (egy szóköz) áll, a széli szóköz nélkül
        sorok = [{'sorszam': '1'}, {'sorszam': '2'}]
        ki = hi.szakasz_sorok(sorok, {1: 'abc', 2: ' de'})
        ossz = ' '.join(['abc', ' de'])
        self.assertEqual([(k, h, ossz[p:p + len(t)], t) for k, h, p, t in ki],
                         [('szakasz', 'sz1', 'abc', 'abc'), ('szakasz', 'sz2', 'de', 'de')])


class SzakaszValos(unittest.TestCase):
    """A javítás a mai adaton: H2416 (BDB2718, a 13–19. sor korábban elcsúszott) és H1419 (a 3. sorban az 1.1 jel, a 4.
    `elakad` volt)."""

    @classmethod
    def setUpClass(cls):
        cls.sorok = dict(((r[0], r[1]), r) for r in hi.general('teszt', {'H2416', 'H1419'})[0])
        cls.ford = hi.forditasok()

    def _sz(self, st, n):
        return self.ford[st]['szakaszonkent'][n].strip()

    def test_h2416_13_19(self):
        self.assertIsNone(self.ford['H2416']['nem_igazolt'])
        for n in range(13, 20):
            r = self.sorok[('H2416', str(n))]
            self.assertEqual((r[7], r[8], r[11]), ('szakasz', 'sz%d' % n, self._sz('H2416', n)), n)
        self.assertEqual(self.sorok[('H2416', '13')][11], '1 állat, mint élő, tevékeny lény:')
        self.assertTrue(self.sorok[('H2416', '14')][11].startswith('a. általában'))
        self.assertTrue(self.sorok[('H2416', '19')][11].startswith('4 újjáéledés'))

    def test_h1419_3_4(self):
        r3, r4 = self.sorok[('H1419', '3')], self.sorok[('H1419', '4')]
        self.assertTrue(r3[11].startswith('1 méretben és kiterjedésben'), r3[11][:40])
        self.assertTrue(r4[11].startswith('2 számban'), r4[11][:40])
        self.assertEqual((r3[7], r4[7]), ('szakasz', 'szakasz'))


def bsor(bdb, jel, szoveg, jelolo='point', ut='-/1/-', sorszam='3'):
    return {'bdb_id': bdb, 'jel': jel, 'jelolo': jelolo, 'szoveg': szoveg, 'utvonal': ut, 'sorszam': sorszam}


class Szocikkhatar(unittest.TestCase):
    """F202.1 (C1; N147, N100, K56): a jelölő nélküli szócikkfej a magyarban a forrás címszavánál kezdődik."""

    def test_romai_es_cimszo_hatarnal(self):
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'רַע adjective', 'fej', 'fej'),
                 bsor('B1', '1', 'bad Gen 2:9'), bsor('B2', '', 'II. רַע noun masculine^Job 30:26 evil', 'fej', 'fej')]
        hu = 'רַע melléknév 1 rossz 1Móz 2:9; vö. רַע alább. II. רַע_126 hímnemű főnév^Jób 30:26 rossz'
        e = hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(e[3], ['jelolo_nelkul', 'II. רַע', hu.index('II. רַע')])

    def test_tobb_talalatbol_az_elso_tagolasjel_utani(self):
        # a címszó az előző szócikk szövegében is előfordul (utalásként), de nem tagolásjel után
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A noun', 'fej', 'fej'), bsor('B1', '1', 'see שׁחל below'),
                 bsor('B2', '', 'שׁחל (√ of following)', 'fej', 'fej')]
        hu = 'A főnév 1 l. lent שׁחל szót. שׁחל (a következő √-je)'
        e = hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(e[3][2], hu.rindex('שׁחל'))

    def test_tagolasjel_nelkul_az_utolso(self):
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A', 'fej', 'fej'), bsor('B1', '1', 'see above'),
                 bsor('B2', '', 'IV. צַר noun flint', 'fej', 'fej')]
        hu = 'A 1 vö. a IV. צַר-ral, l. fent IV. צַר [hímnemű] főnév: kova'
        self.assertEqual(hi.strong_illeszt(sorok, hu)[0][3][2], hu.rindex('IV. צַר'))

    def test_masodik_fej_nem_kot_az_elso_belsejebe(self):
        # H0520: „III. [אַמָּה]” és utána „[אַמָּה K^§ 51”: a második fej horgonya csak az első UTÁN állhat
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A', 'fej', 'fej'), bsor('B1', '1', 'cubit'),
                 bsor('B2', '', 'III. [אַמָּה] noun feminine', 'fej', 'fej'), bsor('B3', '', '[אַמָּה K^§ 51] noun', 'fej', 'fej')]
        hu = 'A 1 könyök. III. [אַמָּה] nőnemű főnév (kétes). [אַמָּה K^§ 51] nőnemű főnév'
        e = hi.strong_illeszt(sorok, hu)[0]
        self.assertEqual(e[3][2], hu.index('III. ['))
        self.assertEqual(e[4][2], hu.rindex('[אַמָּה'))

    def test_zarojeles_cimszo(self):
        # H0310 BDB3524: „(ו)ייחר Kt 2Sam 20:5”
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A', 'fej', 'fej'), bsor('B1', '1', 'after'),
                 bsor('B2', '', '(ו)ייחר Kt 2Sam 20:5', 'fej', 'fej')]
        hu = 'A 1 után. (ו)ייחר Kt 2Sám 20:5'
        self.assertEqual(hi.strong_illeszt(sorok, hu)[0][3][2], hu.index('(ו)'))

    def test_heber_cimszo_nelkul_valtozatlan(self):
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A', 'fej', 'fej'), bsor('B1', '1', 'thus'),
                 bsor('B2', '', 'adverb thus, as follows', 'fej', 'fej')]
        self.assertEqual(hi.strong_illeszt(sorok, 'A 1 így. határozószó: így')[0][3], ['jelolo_nelkul', '', None])

    def test_ugyanaz_a_szocikk_nem_hatar(self):
        sorok = [bsor('B1', '', 'x', 'cim', 'cim'), bsor('B1', '', 'A', 'fej', 'fej'), bsor('B1', '1', 'x'),
                 bsor('B1', '', 'רַע noun', 'bekezdes', '-/1/-')]
        self.assertIsNone(hi.strong_illeszt(sorok, 'A 1 x. רַע főnév')[0][3][2])


class SzocikkhatarValos(unittest.TestCase):
    """A commitolt táblákon: a szócikkhatáron át elnyelt sorok száma legfeljebb a mért maradék (F202.1 előtt 316 sor / 191
    Strong; utána 4 / 3: H3651 24 és a H9003 3–4 (a forrássor nem héber címszóval nyit, ill. a következő sor jelölője a fejre
    köt), H3754 4 (a 2.30 töredéke)); a HAMART-001 három szócikkhatára az általános szabályból, a kézi lista nélkül."""

    @classmethod
    def setUpClass(cls):
        def tsv(ut):
            with open(ut, encoding='utf-8', newline='') as f:
                s = f.read().split('\n')
            fej = s[2].split('\t')
            return [dict(zip(fej, x.rstrip('\r').split('\t'))) for x in s[3:] if x.strip()]
        cls.szak = tsv(hi.TABLA)
        cls.hu = tsv(hi.KI_UT)

    def test_felso_korlat(self):
        j = hi.szocikkhatar_jelentesek(self.szak, self.hu)
        self.assertLessEqual(len(j), 4, j)

    def test_hamart_szocikkhatarok(self):
        hu = {(r['strong'], r['sorszam']): r for r in self.hu}
        self.assertTrue(hu[('H2403', '18')]['szoveg_hu'].startswith('חַטָּיָא nőnemű főnév: bűnért való áldozat'))
        self.assertTrue(hu[('H7451', '18')]['szoveg_hu'].startswith('II. רַע_126 hímnemű főnév^Jób 30:26'))
        self.assertTrue(hu[('H7451', '23')]['szoveg_hu'].startswith('רָעָה_310 nőnemű főnév: rossz, nyomorúság'))
        self.assertNotIn('חַטָּיָא', hu[('H2403', '17')]['szoveg_hu'])
        self.assertEqual(hi.SZOCIKKHATAR_KEZI, {})


class Kapu(unittest.TestCase):
    """F123.BDBILL, DT-F123z: az `ellenoriz.py` 26. szabálya (`kapu_elteresek`) a mai adat másolatán, ideiglenes könyvtárban."""

    def setUp(self):
        import shutil
        import tempfile
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d)
        for f in ('bdb_szakaszok.tsv', 'forditasok.tsv', 'bdb_forras_javitas.tsv', 'bdb_szakasz_hu.tsv'):
            shutil.copy(os.path.join(os.path.dirname(hi.TABLA), f), self.d)

    def _cserel(self, fajl, fv):
        ut = os.path.join(self.d, fajl)
        with open(ut, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(fv(sorok)))

    def test_naprakesz_es_ts_fuggetlen(self):
        # a proveniencia ts-e és a fejléc nem számít
        self._cserel('bdb_szakasz_hu.tsv', lambda s: ['# x', '# y'] + s[2:3] + [x.replace('| ts=2026-11-03', '| ts=2020-01-01')
                                                                             for x in s[3:]])
        self.assertEqual(hi.kapu_elteresek(self.d), [])

    def test_hianyzo_strong(self):
        self._cserel('bdb_szakasz_hu.tsv', lambda s: [x for x in s if not x.startswith('H0509\t')])
        self.assertEqual(hi.kapu_elteresek(self.d), ['H0509: van BDB-fordítása, de a bdb_szakasz_hu.tsv-ben nincs sora'])

    def test_elavult_szakaszforditas(self):
        # a H2416 sz13 magyar szövege változik, a tábla nem: elavult
        self._cserel('forditasok.tsv', lambda s: [x.replace('\t1 állat, mint élő, tevékeny lény:\t', '\t1 állat:\t')
                                                  if x.startswith('BDB\tH2416\tH2416\tsz13\t') else x for x in s])
        h = hi.kapu_elteresek(self.d)
        self.assertEqual(len(h), 1)
        # a 13. sor szövege, és a hu_kezdet eltolódása miatt az utána következők is
        self.assertRegex(h[0], r'^H2416: \d+ sor elavult vagy eltér \(pl\. 13, ')

    def test_nem_bdb_sor_nem_bukik(self):
        self._cserel('forditasok.tsv', lambda s: s[:-1] + ['Thayer\tG9999\tG9999\tteljes\tforditas_hu\tx\tpróba\tsonnet\tm\td\tv\t', ''])
        self.assertEqual(hi.kapu_elteresek(self.d), [])


if __name__ == '__main__':
    unittest.main()
