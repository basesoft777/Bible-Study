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


if __name__ == '__main__':
    unittest.main()
