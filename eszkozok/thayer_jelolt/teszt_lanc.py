#!/usr/bin/env python
"""A Thayer szakaszonkénti fordítási láncának tesztjei (F132; az M3 előfeltételei, fordítás nélkül).

thayer_bemenet.py (betöltő), szolista.py (DT-F132h), thayer_kapuk.py (16_sigla), sigla_gyujt.py, adatblokk.py, forditas.py
(prompt, szakaszsorok, beírás ideiglenes másolaton). Futtatás: python eszkozok/thayer_jelolt/teszt_lanc.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import adatblokk  # noqa: E402
import forditas as F  # noqa: E402
import sigla_gyujt  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402
import thayer_kapuk as TK  # noqa: E402

GYOKER = TB.GYOKER


def tsv_ir(ut, fej, sorok, megj=None):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        if megj:
            f.write('# ' + megj + '\n')
        f.write('\t'.join(fej) + '\n')
        for r in sorok:
            f.write('\t'.join(r.get(m, '') for m in fej) + '\n')


class Betolto(unittest.TestCase):
    def test_kozos_fuggvenyek_a_128_bol(self):
        # DT-F132d (1): importálva, nem másolva
        self.assertEqual(TB.token(3), '⟪3⟫')
        self.assertEqual(TB.jelentes_szam(3), 'sz3')
        self.assertIs(TB.csoportok, TB.K.csoportok)
        self.assertTrue(TB.K.__file__.endswith(os.path.join('bdb_jelolt', 'szakasz_bemenet.py')))

    def test_g1941(self):
        s = TB.szakaszok('G1941')
        self.assertEqual([x['sorszam'] for x in s], list(range(1, 8)))
        self.assertTrue(s[2]['szoveg'].startswith('1. to put a name upon'))
        self.assertEqual(s[2]['hash'], TB.sha1(s[2]['szoveg']))
        self.assertEqual(TB.szakaszok('G12'), TB.szakaszok('G0012'))
        self.assertIsNone(TB.szakaszok('G99999'))

    def test_ellenoriz(self):
        hibak, stat, _ = TB.ellenoriz()
        self.assertEqual(hibak, [])
        self.assertEqual(stat['szakasz'], 17093)


class Szolista(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_gerinc_halmaz_normalizalt(self):
        g = szolista.gerinc_strongok()
        self.assertTrue(all(k.startswith('G') and len(k) == 5 for k in g))
        self.assertIn('G0012', g)
        self.assertEqual(g['G1941'], 10)

    def test_dinamikus_es_kihagyas(self):
        elof = os.path.join(self.tmp, 'e.tsv')
        tsv_ir(elof, ['id', 'igehely', 'strong'], [{'id': '1', 'igehely': 'Mt 1:1', 'strong': 'G12+H1'},
                                                   {'id': '2', 'igehely': 'Mt 1:2', 'strong': 'G0813'},
                                                   {'id': '3', 'igehely': 'Mt 1:3', 'strong': 'G99999'}])
        sz = TB.szakaszok('G0813')
        ford = os.path.join(self.tmp, 'f.tsv')
        sorok = [{'szotar': 'Thayer', 'strong': 'G0813', 'jelentes_szam': 'sz%d' % x['sorszam'], 'mezo': 'forditas_hu',
                  'forras_hash': x['hash'], 'forditas_hu': 'x', 'allapot': 'sonnet'} for x in sz]
        tsv_ir(ford, F.FEJLEC, sorok)
        l = {r['strong']: r for r in szolista.lista('t', elof, ford)}
        self.assertEqual(set(l), {'G0012', 'G0813'})   # a G99999 nem érvényes Strong-alak
        self.assertEqual((l['G0813']['statusz'], l['G0813']['ok']), ('kihagyva', 'kesz'))
        self.assertEqual((l['G0012']['statusz'], l['G0012']['ok']), ('forditando', 'nincs_szakaszos'))
        self.assertTrue(l['G0012']['proveniencia'].startswith('scope=G0012 | forras=thayer_jelolt/szolista.py'))
        # elavult hash -> újra fordítandó; elavult állapot -> nem érvényes
        sorok[0]['forras_hash'] = 'regi'
        tsv_ir(ford, F.FEJLEC, sorok)
        self.assertEqual(szolista.lista('t', elof, ford)[1]['ok'], 'elavult_hash')
        sorok[0]['forras_hash'] = sz[0]['hash']
        sorok[1]['allapot'] = 'elavult'
        tsv_ir(ford, F.FEJLEC, sorok)
        self.assertEqual(szolista.lista('t', elof, ford)[1]['ok'], 'hianyos')

    def test_mai_lista(self):
        l = szolista.lista('t')
        self.assertGreaterEqual(len(l), 13)
        self.assertTrue(all(r['statusz'] in ('forditando', 'kihagyva') for r in l))


class Sigla(unittest.TestCase):
    def test_kapu(self):
        s = [{'forrasalak': 'cf.', 'allapot': 'besorolt', 'magyar_alak': 'vö.'},
             {'forrasalak': 'WH', 'allapot': 'besorolt', 'magyar_alak': TK.VALTOZATLAN},
             {'forrasalak': 'Rec.', 'allapot': 'jelolt', 'magyar_alak': ''}]
        self.assertEqual(TK.ellenoriz_sigla('cf. WH', 'vö. WH', s)[0], 'RENDBEN')
        self.assertEqual(TK.ellenoriz_sigla('cf. WH', 'lásd WH', s)[0], 'SERTES')
        self.assertEqual(TK.ellenoriz_sigla('WH', 'Westcott–Hort', s)[0], 'SERTES')
        self.assertEqual(TK.ellenoriz_sigla('Rec. text', 'szöveg', s)[0], 'JELZES')
        self.assertEqual(TK.ellenoriz_sigla('semmi', 'semmi', s)[0], 'RENDBEN')

    def test_kapu_javaslat_es_nincs_egyseges(self):
        # DT-F132j (3): a jóváhagyatlan javaslat nem gátol (besorolatlan); a besorolt `nincs_egyseges` nem ellenőrzött
        s = [{'forrasalak': 'Rec.', 'allapot': 'javaslat', 'magyar_alak': TK.VALTOZATLAN},
             {'forrasalak': 'N.', 'allapot': 'besorolt', 'magyar_alak': TK.NINCS_EGYSEGES}]
        self.assertEqual(TK.ellenoriz_sigla('Rec. N. T.', 'Újszövetség', s), ('JELZES', '0 besorolt sigla rendben; 1 besorolatlan '
                                                                               'sigla a forrásban (nem gátol)'))
        self.assertEqual(TK.ellenoriz_sigla('N. T.', 'Újszövetség', s), ('RENDBEN', '0 besorolt sigla rendben'))

    def test_kapu_besorolt_ures_alak_jelez(self):
        # ELLENOR_F132 4.: a besorolt, üres magyar_alak kitöltetlen besorolás -> JELZES (nem csendes, nem gátol)
        s = [{'forrasalak': 'N.', 'allapot': 'besorolt', 'magyar_alak': ''},
             {'forrasalak': 'cf.', 'allapot': 'besorolt', 'magyar_alak': 'vö.'}]
        e, r = TK.ellenoriz_sigla('cf. N. T.', 'vö. Újszövetség', s)
        self.assertEqual(e, 'JELZES')
        self.assertIn('1 besorolt sigla rendben', r)
        self.assertIn('1 besorolt sigla üres magyar_alak-kal, kitöltetlen', r)
        self.assertIn('N.', r)
        self.assertTrue(TK.atment([('16_sigla', e, r)]))
        # a SERTES elsőbb: a besorolt alak hiánya gátol akkor is, ha kitöltetlen sor is van
        self.assertEqual(TK.ellenoriz_sigla('cf. N. T.', 'lásd Újszövetség', s)[0], 'SERTES')
        # a forrásban nem álló kitöltetlen sor nem számít
        self.assertEqual(TK.ellenoriz_sigla('cf. x', 'vö. x', s), ('RENDBEN', '1 besorolt sigla rendben'))

    def test_kapu_egybetus_sigla_tobbtagu_rovidites(self):
        # ELLENOR_F132 3.: az egybetűs sigla a betű-pont-(szóköz-)betű-pont láncban nem találat
        for alak, szoveg in (('T', 'N. T.'), ('T', 'O. T. 12'), ('T', 'N.T.'), ('R', 'R. V. reads'), ('V', 'A. V.'),
                             ('G', 'G. L. Hahn'), ('L', 'G. L. Hahn')):
            self.assertIsNone(TK._re(alak).search(szoveg), (alak, szoveg))
        for alak, szoveg in (('T', 'G L T Tr WH'), ('T', 'T WH; cf. N. T.'), ('T', 'Gen. T'), ('G', 'R G'), ('L', 'L T Tr'),
                             ('R', 'R G, N. T.')):
            self.assertIsNotNone(TK._re(alak).search(szoveg), (alak, szoveg))
        self.assertIsNone(TK._re('Tr').search('Trench'))
        s = [{'forrasalak': a, 'allapot': 'besorolt', 'magyar_alak': TK.VALTOZATLAN} for a in ('R', 'G', 'L', 'T')]
        # negatív: a forrás egyetlen T-je az N. T.-ben áll -> nincs mit ellenőrizni (korábban hamis SERTES)
        self.assertEqual(TK.ellenoriz_sigla('see N. T. i. 12', 'l. Újszövetség i. 12', s), ('RENDBEN', '0 besorolt sigla rendben'))
        self.assertEqual(TK.ellenoriz_sigla('so R. V.; G. L. Hahn', 'így az angol revideált fordítás; Hahn', s)[0], 'RENDBEN')
        # pozitív: az önálló sigla továbbra is ellenőrzött, a fordítás láncbeli betűje nem pótolja
        self.assertEqual(TK.ellenoriz_sigla('G L T Tr WH', 'G L T Tr WH', s), ('RENDBEN', '3 besorolt sigla rendben'))
        self.assertEqual(TK.ellenoriz_sigla('T WH; N. T.', 'WH; N. T.', s)[0], 'SERTES')

    def test_kapusor(self):
        e = TK.kapuk_futtat_thayer('⟪1⟫ a', '⟪1⟫ a')
        nevek = [n for n, _, _ in e]
        for n in ('14_szakasz', '15_tiltott', '16_sigla'):
            self.assertIn(n, nevek)

    def test_tabla_determinisztikus_es_kezi_vedett(self):
        r = subprocess.run([sys.executable, os.path.join(ITT, 'sigla_gyujt.py'), '--ellenoriz'], capture_output=True, text=True,
                           encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        regi = sigla_gyujt.regi_tabla()
        gy = sigla_gyujt.gyujt()
        egy = next(iter(regi))
        regi[egy] = dict(regi[egy], tipus='kiadás-sigla', magyar_alak=TK.VALTOZATLAN, allapot='besorolt')
        uj = sigla_gyujt.osszefesul(gy, regi, 't')
        self.assertIsNone(sigla_gyujt.kezi_valtozatlan(regi, uj))
        self.assertEqual(uj[0]['allapot'], 'besorolt')
        self.assertEqual(len(uj), len(regi))

    def test_tabla_sema(self):
        for r in TK.sigla_betolt():
            self.assertIn(r['gyujtes'], ('minta', 'kiadas_sigla', 'rovidites'))
            self.assertIn(r['allapot'], ('jelolt', 'javaslat', 'besorolt'))
            if r['allapot'] in ('javaslat', 'besorolt'):
                # ELLENOR_F132 4.: a besorolás magyar_alak-ja nem üres: alak, `változatlan` vagy `nincs_egyseges`
                self.assertTrue(r['magyar_alak'], r['forrasalak'])
            if r['allapot'] == 'javaslat':
                # modell-javaslat: nem lekérdezés, a proveniencia `manual`, modellnévvel (CLAUDE.md 1. szabály)
                self.assertRegex(r['besorolas_proveniencia'], r'forras=manual — modell-javaslat \(claude-[\w.-]+\), nem lekérdezés')
                self.assertTrue(r['tipus'])

    def test_javaslat_a_terminologiaval_osszhangban(self):
        # ahol a terminológiai szójegyzék kapus kulcsa a forrásalak, a javasolt magyar alak a szójegyzéké
        term = {}
        for r in adatblokk.terminologia():
            if r.get('kapu') == 'igen':
                term.setdefault(r.get('angol', ''), r.get('magyar', ''))
        n = 0
        for r in TK.sigla_betolt():
            if r['allapot'] in ('javaslat', 'besorolt') and r['forrasalak'] in term:
                n += 1
                self.assertEqual(r['magyar_alak'], term[r['forrasalak']], r['forrasalak'])
        self.assertGreaterEqual(n, 9)

    def test_javaslat_lefedi_a_gerincet(self):
        # DT-F132j (3): minden, a gerincszavakban előforduló jelölt kapott javaslatot (vagy már besorolt)
        for r in TK.sigla_betolt():
            if int(r['gerinc_elofordulas']) > 0:
                self.assertIn(r['allapot'], ('javaslat', 'besorolt'), r['forrasalak'])


class Adatblokk(unittest.TestCase):
    def test_g1941_reszei(self):
        b = adatblokk.blokk('G1941', ts='T')
        for jel in ('**1. Károli-szóalakok**', '**2. Az idézett versek', '**3. Siglák', '**4. Nyelvközi híd**'):
            self.assertIn(jel, b)
        self.assertEqual(b.count('*proveniencia: scope=G0012') + b.count('*proveniencia: scope=G1941'), 4)
        self.assertIn('Mt, Mk, Luk, Ján, ApCsel', b)          # a párosítás le nem fedett ÚSZ-könyvei, explicit
        self.assertIn('1Pét 1:17 „És ha Atyának hívjátok őt', b)
        self.assertIn('= H7121', b)
        self.assertIn('`cf.` [besorolatlan a sigla-táblában; a terminológia szerint: `vö.`]', b)

    def test_sigla_nincs_egyseges(self):
        # ELLENOR_F132 4.: a besorolt `nincs_egyseges` sor nem alakként jelenik meg, hanem explicit jelöléssel
        eredeti = TK.sigla_betolt
        TK.sigla_betolt = lambda ut=None: [{'forrasalak': 'cf.', 'allapot': 'besorolt', 'magyar_alak': TK.NINCS_EGYSEGES,
                                            'jelentes': 'próba'}]
        try:
            b = adatblokk.blokk('G1941', ts='T')
        finally:
            TK.sigla_betolt = eredeti
        self.assertIn('`cf.` [nincs egységes magyar alak: a szövegkörnyezet szerint — próba]', b)
        self.assertNotIn('→ `nincs_egyseges`', b)

    def test_csoportonkent(self):
        sz = TB.szakaszok('G1941')
        b = adatblokk.blokk('G1941', [sz[6]], ts='T')
        self.assertIn('⟪7⟫ Róm 10:13', b)
        self.assertNotIn('⟪3⟫', b)

    def test_javitassal_jelzes(self):
        # DT-F132i (2): a G4151 szövege a javítótáblával teljes — tájékoztató sor, nem „a hiányt ne pótold” figyelmeztetés
        b = adatblokk.blokk('G4151', TB.szakaszok('G4151')[:2], ts='T')
        self.assertIn('DT-F132i (2)', b)
        self.assertNotIn('FIGYELEM', b)

    def test_nincs(self):
        self.assertEqual(adatblokk.blokk('G99999'), 'nincs adatblokk')


class Lanc(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_prompt_v5_1(self):
        # DT-F132k (2): a Thayer a v5.1-et használja; a v5.1 = a v5 szó szerint + egyetlen új blokk; a v5 a BDB-é marad
        self.assertTrue(F.PROMPT_UT.endswith(os.path.join('forditas', 'prompt_v5_1.md')))
        with open(F.PROMPT_UT, encoding='utf-8') as fh:
            v51 = fh.read()
        with open(F.E.PROMPT_V5_UT, encoding='utf-8') as fh:
            v5 = fh.read()
        self.assertNotIn('v5.1', v5)
        blokk_eleje = '## Kiegészítő szabály (v5.1) — Thayer-szócikk'
        vege = '## Ideiglenes terminológia (kötelező megfeleltetés'
        torzs = v51.split('*A v5.0 fejléce, változatlanul:*\n\n', 1)[1]
        i, j = torzs.index(blokk_eleje), torzs.index(vege)
        self.assertEqual(torzs[:i] + torzs[j:], v5)
        p = F.prompt_epit('G1941', TB.szakaszok('G1941'))
        self.assertIn(blokk_eleje, p)
        self.assertNotIn('Verziónapló (v5.1)', p)  # a jelölő fölötti rész nem kerül a promptba

    def test_prompt(self):
        sz = TB.szakaszok('G1941')
        p = F.prompt_epit('G1941', sz)
        self.assertNotIn('{{', p)
        self.assertIn('Strong-szám: G1941', p)
        self.assertIn('### Adatblokk — Thayer G1941', p)
        self.assertIn('⟪1⟫ G1941 — ἐπικαλέω', p)
        self.assertIn('Thayer', p)

    def test_szakasz_sorok(self):
        sz = TB.szakaszok('G0813')
        szoveg = ' '.join('%s m%d' % (TB.token(x['sorszam']), x['sorszam']) for x in sz)
        s = F.szakasz_sorok('G0813', sz, szoveg, 'sonnet', 'claude-sonnet-x', '2026.10.25', 'v4', '')
        self.assertEqual([r['jelentes_szam'] for r in s], ['sz%d' % x['sorszam'] for x in sz])
        self.assertEqual([r['forras_hash'] for r in s], [x['hash'] for x in sz])
        self.assertEqual({r['entry_id'] for r in s}, {'G813'})
        with self.assertRaises(SystemExit):
            F.szakasz_sorok('G0813', sz, '⟪1⟫ csak egy', 'sonnet', 'm', 'd', 'v', '')

    def _munka(self, sp, allapot='sonnet'):
        sz = TB.szakaszok(sp)
        szoveg = ' '.join('%s m%d' % (TB.token(x['sorszam']), x['sorszam']) for x in sz)
        mu = os.path.join(self.tmp, 'munka.tsv')
        tsv_ir(mu, F.FEJLEC, F.szakasz_sorok(sp, sz, szoveg, allapot, 'claude-sonnet-x', '2026.10.25', 'v4', ''), 'munka')
        return mu

    def _forditasok(self):
        ut = os.path.join(self.tmp, 'forditasok.tsv')
        shutil.copy(F.FORDITASOK_UT, ut)
        with open(ut, encoding='utf-8', newline='') as f:
            return ut, f.read()

    def test_beir_opus_regi_elavul(self):
        mu = self._munka('G0813')
        ut, eredeti = self._forditasok()
        with self.assertRaises(SystemExit):        # --regi-elavult nélkül megáll (DT-F132c (i))
            F.beir(['G0813'], 'sonnet', '2026.10.25', munka_ut=mu, forditasok_ut=ut)
        n = F.beir(['G0813'], 'sonnet', '2026.10.25', regi_elavult=True, munka_ut=mu, forditasok_ut=ut)
        with open(ut, encoding='utf-8', newline='') as f:
            uj = f.read().split('\n')
        regi = eredeti.split('\n')
        valt = [i for i, s in enumerate(regi[:-1]) if uj[i] != s]
        self.assertEqual(len(valt), 1)                      # csak a régi teljes sor
        self.assertIn('\tG0813\tG813\tteljes\t', uj[valt[0]])
        self.assertIn('\telavult\t', uj[valt[0]])
        self.assertEqual(n, 1 + len(TB.szakaszok('G0813')))

    def test_beir_kezi_marad(self):
        mu = self._munka('G1941')
        ut, eredeti = self._forditasok()
        with self.assertRaises(SystemExit):        # DT-F132c (ii): kezi régi sor mellett csak --kezi-marad
            F.beir(['G1941'], 'sonnet', '2026.10.25', regi_elavult=True, munka_ut=mu, forditasok_ut=ut)
        F.beir(['G1941'], 'sonnet', '2026.10.25', kezi_marad=True, munka_ut=mu, forditasok_ut=ut)
        with open(ut, encoding='utf-8', newline='') as f:
            uj = f.read()
        self.assertTrue(uj.startswith(eredeti))         # a régi sorok bájtra azonosak, csak hozzáfűzés
        sorok = [dict(zip(F.FEJLEC, s.split('\t'))) for s in uj.split('\n') if s.startswith('Thayer\tG1941\t')]
        self.assertEqual(TB.strong_magyar(sorok)[1], 'teljes')   # a kezi teljes sor az érvényes


if __name__ == '__main__':
    unittest.main(verbosity=1)
