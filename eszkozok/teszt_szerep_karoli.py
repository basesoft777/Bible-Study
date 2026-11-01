"""Az `eszkozok/szerep_karoli.py` tesztjei: a 13. (Károli-megfelelők) és a 14. (Rejtett / hamis párhuzam) szerep.

Futtatás: python -m unittest -q eszkozok.teszt_szerep_karoli
Szintetikus adaton (befecskendezett szótárialak-tábla, párosítás, versek, Strongok) és két motívum valódi adatán
(ISTENTISZT-001, KIRALY-001).
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
import szerep_karoli as SK  # noqa: E402

TABLA = {'segítségűl': 'segítségül', 'segítségül': 'segítségül', 'hívják': 'hív', 'hívá': 'hív', 'hívni': 'hívni',
         'nevét': 'név', 'nevedet': 'név', 'Úrnak': 'úr', 'Urat': 'úr', 'kiáltá': 'kiált'}


def sor(hely, strong, karoli):
    return {'id': 'TESZT-001', 'igehely': hely, 'strong': strong, 'karoli_szo': karoli}


SORAI = [sor('V 1:1', 'H1+H2', 'segítségűl hívá az Úrnak nevét'),
         sor('V 1:2', 'H1+H2', 'segítségül hívni az Úrnak nevét'),
         sor('V 1:3', 'H1+H2', 'segítségül hívják a te nevedet'),
         sor('V 1:4', 'H1+H2', 'nevén kiáltá az Urat'),
         sor('U 1:1', 'G1', 'hívják')]
PAROK = {'V 1:1': [('segítségűl', 'H9003'), ('hívá', 'H1'), ('Úrnak', 'H3068'), ('nevét', 'H2')],
         'V 1:2': [('Úrnak', 'H3068')]}


def olvas_motivum(mid):
    with open(os.path.join(SK.GYOKER, 'adat', 'elofordulasok.tsv'), encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:] if x.split('\t')[0] == mid]


class Szintetikus(unittest.TestCase):
    def test_lemma_es_szavak(self):
        self.assertEqual(SK.lemma('segítségűl', TABLA), 'segítségül')
        self.assertEqual(SK.lemma('Ismeretlen', TABLA), 'ismeretlen')
        self.assertEqual(SK.szavak('segítségül hívja ... nevemet'), ['segítségül', 'hívja', 'nevemet'])

    def test_egyezik_elotag(self):
        self.assertTrue(SK.egyezik('hívni', 'hív', TABLA))        # a tábla igealak-hiánya
        self.assertTrue(SK.egyezik('hívnám', 'hív', TABLA))
        self.assertFalse(SK.egyezik('rendeléseit', 'rend', TABLA))  # 3 betűnél hosszabb maradék

    def test_13_osszevonas_es_nevelo(self):
        m = {l: (a, h) for l, a, h in SK.karoli_megfelelok(SORAI, TABLA)}
        self.assertNotIn('az', m)
        self.assertNotIn('a', m)
        self.assertEqual(m['segítségül'][0], ['segítségűl', 'segítségül'])
        self.assertNotIn('hívni', m)                              # beolvadt a hív-be
        self.assertEqual(m['hív'][1], ['U 1:1', 'V 1:1', 'V 1:2', 'V 1:3'])   # a Károliban ismeretlen hely: betűrendben
        self.assertEqual(m['név'][1], ['V 1:1', 'V 1:2', 'V 1:3'])

    def test_kulcs_kombinacionkent_es_parszuro(self):
        k = SK.kulcsszavak(SORAI, tabla=TABLA, parositas=PAROK)
        self.assertEqual(list(k), [frozenset({'H1', 'H2'})])        # a G1 egysoros: nincs kulcs (KULCS_MIN_SOR)
        self.assertIn('segítségül', k[frozenset({'H1', 'H2'})])     # a nyelvtani pár (H9003) nem dönt
        self.assertNotIn('úr', k[frozenset({'H1', 'H2'})])          # csak idegen Strongra (H3068) párosul

    def test_rejtett(self):
        k = SK.kulcsszavak(SORAI, tabla=TABLA, parositas=PAROK)
        r = SK.rejtett_parhuzamok(SORAI, tabla=TABLA, kulcs=k)
        self.assertEqual([x[0] for x in r], ['V 1:4'])
        self.assertIn('segítségül', r[0][3])

    def test_hamis(self):
        k = SK.kulcsszavak(SORAI, tabla=TABLA, parositas=PAROK)
        versek = [('V 1:1', 'x'), ('V 2:1', 'segítségül hívá az ő nevét'), ('V 2:2', 'segítségül hívá a nevét'),
                  ('V 2:3', 'hívá a nevét')]
        strongok = {'V 2:1': {'H1', 'H2'}, 'V 2:2': {'H1'}, 'V 2:3': set()}
        h = SK.hamis_parhuzamok(SORAI, versek=versek, strongok=strongok, tabla=TABLA, kulcs=k)
        self.assertEqual([x[0] for x in h], ['V 2:2'])            # 2:1 gerinces, 2:3-ból hiányzik a kulcsszó, 1:1 saját
        self.assertEqual(h[0][2], ['H1'])                          # a részleges gerinc kiíródik


class ValodiAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ist = olvas_motivum('ISTENTISZT-001')
        cls.kir = olvas_motivum('KIRALY-001')

    def test_istentiszt_kulcs(self):
        k = SK.kulcsszavak(self.ist)
        self.assertEqual(sorted(k[frozenset({'G1941'})]), ['hív', 'segítségül'])
        self.assertEqual(sorted(k[frozenset({'H7121', 'H8034'})]), ['hív', 'név', 'segítségül'])

    def test_istentiszt_rejtett(self):
        self.assertEqual(sorted(x[0] for x in SK.rejtett_parhuzamok(self.ist)),
                         sorted(['1Pét 1:17', 'Ézs 12:4', '2Móz 33:19', '2Móz 34:5']))

    def test_istentiszt_hamis_gerinc_nelkul(self):
        st = SK.vers_strongok()
        sajat = {s['igehely'] for s in self.ist}
        h = SK.hamis_parhuzamok(self.ist)
        self.assertTrue(h)
        for hely, _, _g in h:
            self.assertNotIn(hely, sajat)
            self.assertFalse({'H7121', 'H8034'} <= st.get(hely, set()) or 'G1941' in st.get(hely, set()), hely)

    def test_masodik_motivum(self):
        b13, b14 = SK.blokk_13(self.kir, 'T'), SK.blokk_14(self.kir, 'T')
        self.assertTrue(b13)
        helyek = {s['igehely'] for s in self.kir}
        for l, _a, h in SK.karoli_megfelelok(self.kir):
            self.assertTrue(set(h) <= helyek, l)
        k = SK.kulcsszavak(self.kir)
        for komb in k:
            self.assertGreaterEqual(sum(1 for s in self.kir if SK._komb(s) == komb), SK.KULCS_MIN_SOR)
        self.assertTrue(b14)
        self.assertEqual(SK.blokk_14(self.kir, 'T'), b14)          # determinisztikus

    def test_kanonikus_sorrend(self):
        # a versek a Károli-fájl sorrendjében (nem a motívumtábla sorrendjében): Róm 10:12 a 10:13 és a 10:14 előtt
        h = dict((l, hs) for l, _a, hs in SK.karoli_megfelelok(self.ist))['hív']
        self.assertEqual(h, sorted(h, key=SK.vers_kulcs))
        self.assertLess(h.index('Róm 10:12'), h.index('Róm 10:14'))
        self.assertEqual(SK.vers_kulcs('1Móz 14:18-20')[0], SK.vers_kulcs('1Móz 14:18')[0])

    def test_blokk_13_szpa_es_proveniencia(self):
        b = SK.blokk_13(self.ist, '2026-10-29')
        # ISTENTISZT-001 arany lap, 2026-10-29: a SzPA-join felfüggesztve (adat/funkcio_kapcsolok.tsv) — a „+SZPA” sor nem áll
        self.assertFalse(SK.szpa_aktiv())
        self.assertFalse(any('+SZPA' in x for x in b))
        self.assertRegex(b[-1], r'scope=.* \| forras=.* \| n=33 \| ts=2026-10-29')


if __name__ == '__main__':
    unittest.main()
