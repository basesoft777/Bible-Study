"""A regresszió tesztjei (F218a brief 8.1): szakasz-diff, engedély-összevetés darabszámmal, bemenet-hash őr."""
import hashlib
import os
import shutil
import tempfile
import unittest

from kozos import MiniRepo, tsv
from lapgen import regresszio as R

REFERENCIA = '\n'.join([
    '# Cím', '',
    '## 1. Első', '', 'első sor', 'második sor ts=2026-11-12', '',
    '## 2. Második', '', 'A sor', 'B sor', 'C sor', '',
]) + '\n'


def _sha(szoveg):
    return hashlib.sha256(szoveg.encode('utf-8')).hexdigest()


def _repo(engedelyek=(), referencia=REFERENCIA, bemenet='x\ty\n', rogzitett_bemenet=None):
    fajlok = {
        'lexikon/PROBA-001_TUDOMANYOS.md': referencia,
        'adat/be.tsv': bemenet,
        'naplok/F218_referencia.tsv': tsv(
            '# teszt', R.REFERENCIA_OSZLOPOK,
            ('referencia', '-', 'lexikon/PROBA-001_TUDOMANYOS.md', _sha(referencia), '%d' % len(referencia)),
            ('bemenet', 'B03', 'adat/be.tsv', _sha(rogzitett_bemenet if rogzitett_bemenet is not None else bemenet),
             '1')),
    }
    if engedelyek:
        fajlok['naplok/F218_elteres_engedely.tsv'] = tsv('# teszt', R.ENGEDELY_OSZLOPOK, *engedelyek)
    return MiniRepo(fajlok)


class Regresszio(unittest.TestCase):
    def setUp(self):
        self.uj = tempfile.mkdtemp(prefix='lapgen_uj_')
        self.repok = []

    def tearDown(self):
        shutil.rmtree(self.uj, ignore_errors=True)
        for repo in self.repok:
            repo.torol()

    def _meres(self, uj_szoveg, **kw):
        teljes = kw.pop('teljes', False)
        naplo = kw.pop('naplo', (('B03', 'adat/be.tsv', _sha(kw.get('bemenet', 'x\ty\n'))),
                                  ('B13', '-', '')))
        repo = _repo(**kw)
        self.repok.append(repo)
        with open(os.path.join(self.uj, 'PROBA-001_TUDOMANYOS.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj_szoveg)
        naplo_ut = os.path.join(self.uj, R.NAPLO_FAJLNEV % 'PROBA-001')
        if naplo is not None:
            with open(naplo_ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(tsv(R.NAPLO_OSZLOPOK, *naplo))
        elif os.path.isfile(naplo_ut):
            os.remove(naplo_ut)
        return R.meres('PROBA-001', self.uj, gyoker=repo.gyoker, teljes=teljes)

    def test_szakaszol(self):
        szakaszok = R.szakaszol(REFERENCIA)
        self.assertEqual([c for c, _ in szakaszok], [R.ELOSZO, '1. Első', '2. Második'])
        self.assertEqual(szakaszok[2][1], ['## 2. Második', '', 'A sor', 'B sor', 'C sor', ''])

    def test_reszleges_lap_egyezo_szakasszal(self):
        """Részleges lap: a kész szakasz egyezik, a többi „nincs kész”, nem BUKÁS."""
        e = self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n')
        self.assertFalse(e['bukas'])
        allapotok = {cim: allapot for cim, allapot, _d, _k in e['jelentesek']['TUDOMANYOS']}
        self.assertEqual(allapotok, {'1. Első': 'nincs kész', '2. Második': 'egyezik'})

    def test_teljes_modban_a_hianyzo_szakasz_bukas(self):
        e = self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', teljes=True)
        self.assertTrue(e['bukas'])

    def test_engedely_nelkuli_diff_bukas(self):
        e = self._meres('## 2. Második\n\nA sor\nB más\nC sor\n\n')
        self.assertTrue(e['bukas'])
        self.assertEqual(e['engedely_nelkul'], [('TUDOMANYOS', '2. Második', 'B sor', 'B más')])

    def test_sor_kotesu_engedely_darabszammal(self):
        """Minden diff-sor pontosan egy engedélysorhoz tartozik, és a darabszám egyezik az elvárttal."""
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'HN-01', 'sor', R.sor_hash('B sor'), R.sor_hash('B más'), '1', 'ok')]
        e = self._meres('## 2. Második\n\nA sor\nB más\nC sor\n\n', engedelyek=eng)
        self.assertFalse(e['bukas'])
        self.assertEqual(e['hasznalat'], {'E1': 1})

    def test_fel_nem_hasznalt_engedely_bukas(self):
        """A fel nem használt engedélysor is BUKÁS (tényleges 0 ≠ elvárt 1)."""
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'HN-01', 'sor', R.sor_hash('B sor'), R.sor_hash('B más'), '1', 'ok')]
        e = self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', engedelyek=eng)
        self.assertTrue(e['bukas'])
        self.assertEqual(e['engedely_hiba'], [('E1', 1, 0)])

    def test_tulhasznalt_engedely_bukas(self):
        """A túlhasznált engedélysor is BUKÁS: a minta két sorra illik, az elvárt darabszám egy."""
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'T', 'minta', r' sor$', ' más', '1', 'ok')]
        e = self._meres('## 2. Második\n\nA más\nB más\nC sor\n\n', engedelyek=eng)
        self.assertTrue(e['bukas'])
        self.assertEqual(e['engedely_hiba'], [('E1', 1, 2)])

    def test_minta_kotes_csak_a_cserevel_egyezo_sorra_illik(self):
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'T', 'minta', r'^B sor$', 'B más', '1', 'ok')]
        self.assertFalse(self._meres('## 2. Második\n\nA sor\nB más\nC sor\n\n', engedelyek=eng)['bukas'])
        self.assertTrue(self._meres('## 2. Második\n\nA sor\nB egészen más\nC sor\n\n', engedelyek=eng)['bukas'])

    def test_ket_engedelyre_illo_diff_bukas(self):
        """Ha egy diff-sor két engedélysorra is illik, nem tartozik pontosan egyhez: BUKÁS."""
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'T', 'minta', r'^B sor$', 'B más', '1', 'ok'),
               ('E2', 'TUDOMANYOS', '*', 'T', 'sor', R.sor_hash('B sor'), R.sor_hash('B más'), '1', 'ok')]
        self.assertTrue(self._meres('## 2. Második\n\nA sor\nB más\nC sor\n\n', engedelyek=eng)['bukas'])

    def test_beszuras_es_torles_engedellyel(self):
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'T', 'sor', '-', R.sor_hash('új sor'), '1', 'ok'),
               ('E2', 'TUDOMANYOS', '2. Második', 'T', 'sor', R.sor_hash('C sor'), '-', '1', 'ok')]
        e = self._meres('## 2. Második\n\nA sor\núj sor\nB sor\n\n', engedelyek=eng)
        self.assertEqual(sorted(e['hasznalat'].items()), [('E1', 1), ('E2', 1)])
        self.assertFalse(e['bukas'])

    def test_ok_kotes_egy_sor_egy_okra_darabszammal(self):
        """D19: egy szándékos eltérés okonként egy sorban: a törölt és a beszúrt sorok egy engedélyre, pontos számmal."""
        eng = [('O1', 'TUDOMANYOS', '2. Második', 'D19', 'ok', '*', '*', '3', 'D-teszt: a tábla helyett mondat')]
        e = self._meres('## 2. Második\n\nA sor\núj mondat\n\n', engedelyek=eng)
        self.assertFalse(e['bukas'])
        self.assertEqual(e['hasznalat'], {'O1': 3})

    def test_ok_kotes_a_nem_okhoz_kotott_elterest_jelzi(self):
        """Egy további, nem okhoz kötött eltérés a darabszámot elrontja: BUKÁS; más szakaszban engedély nélküli."""
        eng = [('O1', 'TUDOMANYOS', '2. Második', 'D19', 'ok', '*', '*', '3', 'D-teszt')]
        e = self._meres('## 2. Második\n\nA más\núj mondat\n\n', engedelyek=eng)
        self.assertTrue(e['bukas'])
        self.assertEqual(len(e['engedely_hiba']), 1)
        self.assertNotEqual(e['engedely_hiba'][0][2], 3)
        e = self._meres('## 1. Első\n\nelső sor\nmásik\n\n## 2. Második\n\nA sor\núj mondat\n\n',
                        engedelyek=eng)
        self.assertTrue(e['bukas'])

    def test_ok_kotes_oldalmintaja(self):
        """A `-` oldal hiányt kér, a reguláris kifejezés az oldal sorára illik."""
        eng = [('O1', 'TUDOMANYOS', '2. Második', 'D19', 'ok', r'^[BC] sor$', '-', '2', 'D-teszt: törlés')]
        self.assertFalse(self._meres('## 2. Második\n\nA sor\n\n', engedelyek=eng)['bukas'])
        self.assertTrue(self._meres('## 2. Második\n\nA sor\nB más\n\n', engedelyek=eng)['bukas'])

    def test_a_soronkenti_engedely_elobb_az_ok_utana(self):
        """Ha egy diff-sorra soronkénti és okonkénti engedély is illik, a soronkénti viszi; nem kettős illés."""
        eng = [('E1', 'TUDOMANYOS', '2. Második', 'T', 'sor', R.sor_hash('C sor'), '-', '1', 'ok'),
               ('O1', 'TUDOMANYOS', '2. Második', 'D19', 'ok', '*', '*', '2', 'D-teszt')]
        e = self._meres('## 2. Második\n\nA sor\nB más\n\n', engedelyek=eng)
        self.assertFalse(e['bukas'])
        self.assertEqual(sorted(e['hasznalat'].items()), [('E1', 1), ('O1', 2)])

    def test_a_meg_nem_kesz_szakasz_engedelye_nem_szamit(self):
        """Részleges lapnál a még el nem készült szakasz engedélysora nem BUKÁS."""
        eng = [('E9', 'TUDOMANYOS', '1. Első', 'T', 'sor', R.sor_hash('első sor'), R.sor_hash('x'), '1', 'ok')]
        self.assertFalse(self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', engedelyek=eng)['bukas'])

    def test_bemenet_hash_or(self):
        """A mérce bemenetének változása kimondott hibával megállítja a mérést."""
        with self.assertRaises(R.MerceHiba) as hiba:
            self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', rogzitett_bemenet='régi tartalom\n')
        self.assertIn('a mérce bemenete megváltozott: B03 adat/be.tsv', '%s' % hiba.exception)

    def test_naplo_or_ismeretlen_bemenet(self):
        """Ha az új generátor olyan fájlt olvasott, amely nincs a referencia-táblában, a mérés megáll; a nem
        fájl-bemenet (szabálymodul) sora nem számít."""
        jo = '## 2. Második\n\nA sor\nB sor\nC sor\n\n'
        self.assertFalse(self._meres(jo)['bukas'])
        with self.assertRaises(R.MerceHiba) as hiba:
            self._meres(jo, naplo=(('B03', 'adat/be.tsv', _sha('x\ty\n')), ('B67', 'adat/uj.tsv', _sha('z\n'))))
        self.assertIn('B67 adat/uj.tsv (nincs a referencia-táblában)', '%s' % hiba.exception)

    def test_naplo_or_mas_tartalom_es_hianyzo_naplo(self):
        """Más tartalommal olvasott bemenet és hiányzó olvasási napló is megállítja a mérést."""
        jo = '## 2. Második\n\nA sor\nB sor\nC sor\n\n'
        with self.assertRaises(R.MerceHiba) as hiba:
            self._meres(jo, naplo=(('B03', 'adat/be.tsv', _sha('más\n')),))
        self.assertIn('B03 adat/be.tsv (más tartalommal olvasva)', '%s' % hiba.exception)
        with self.assertRaises(R.MerceHiba) as hiba:
            self._meres(jo, naplo=None)
        self.assertIn('hiányzik az új generátor olvasási naplója', '%s' % hiba.exception)

    def test_hash_or_kivetel_b51(self):
        """N240: a B51 olvasási napló-sora nem vetődik össze (a lapon használt része a szakasz-diffben mérődik),
        a referencia-táblában álló B51-sor pedig kimondott hiba."""
        jo = '## 2. Második\n\nA sor\nB sor\nC sor\n\n'
        self.assertFalse(self._meres(jo, naplo=(('B03', 'adat/be.tsv', _sha('x\ty\n')),
                                                ('B51', 'DONTESEK.md', _sha('bármi\n'))))['bukas'])
        self.assertEqual(R.HASH_OR_KIVETEL, frozenset({'B51'}))
        repo = _repo()
        self.repok.append(repo)
        ut = os.path.join(repo.gyoker, *R.REFERENCIA_TSV.split('/'))
        with open(ut, 'a', encoding='utf-8', newline='') as f:
            f.write('bemenet\tB51\tDONTESEK.md\t%s\t1\n' % _sha('x\n'))
        with self.assertRaises(R.MerceHiba) as hiba:
            R.hash_or(repo.gyoker)
        self.assertIn('hash-őr kivétele', '%s' % hiba.exception)

    def test_a_naplo_fajlneve_egyezik_a_generatoreval(self):
        from lapgen import konfig
        self.assertEqual((R.NAPLO_FAJLNEV, R.NAPLO_OSZLOPOK), (konfig.NAPLO_FAJLNEV, konfig.NAPLO_OSZLOPOK))

    def test_hash_or_sorveg_fuggetlen(self):
        repo = _repo()
        self.repok.append(repo)
        ut = os.path.join(repo.gyoker, 'lexikon', 'PROBA-001_TUDOMANYOS.md')
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(REFERENCIA.replace('\n', '\r\n'))
        self.assertEqual(R.hash_or(repo.gyoker), 2)


if __name__ == '__main__':
    unittest.main(verbosity=1)


class HashOrKapu(unittest.TestCase):
    """A mérce hash-őre a push előtti kapuban és a CI-ben (a 6. ellenőrzés E1 tétele; az újraellenőrzés U3 tétele):
    csak a lapgenerátort vagy a mércéjét érintő változásra fut."""

    def test_erintett_utvonalak(self):
        from lapgen import hash_or_kapu as H
        self.assertEqual(H.erintett(['adat/motivumok.tsv', 'DONTESEK.md', 'eszkozok/lexikon_general.py']), [])
        self.assertEqual(H.erintett(['eszkozok\\lapgen\\fo.py','adat/lapgen_sablonok.tsv',
                                     'naplok/F218_referencia.tsv', 'naplok/F218_jelentes.md']),
                         ['eszkozok/lapgen/fo.py', 'adat/lapgen_sablonok.tsv', 'naplok/F218_referencia.tsv'])

    def test_nem_erinto_lista_nem_fut(self):
        from lapgen import hash_or_kapu as H
        d = tempfile.mkdtemp()
        try:
            lista = os.path.join(d, 'lista.txt')
            with open(lista, 'w', encoding='utf-8') as f:
                f.write('adat/motivumok.tsv\n')
            self.assertEqual(H.main(['--valtozott-lista', lista]), 0)
        finally:
            shutil.rmtree(d)


class Szamlalok(unittest.TestCase):
    """A brief 8.2/1 független számlálói (S9b; a 10. ellenőrzés 4. tétele): a lapon kimondott számok és a regresszió
    saját számlálása az adattáblákból, mindkét mintalapon."""

    @classmethod
    def setUpClass(cls):
        import datetime
        import kozos
        from lapgen import fo
        from lapgen.megjelenites.md.iro import lap_szoveg
        from lapgen.szoveg import MotivumId
        cls.konyvtar = tempfile.mkdtemp()
        for azonosito in kozos.MINTALAPOK:
            eredmeny = kozos.lap_keszit(azonosito, datetime.date(2026, 11, 13))
            with open(os.path.join(cls.konyvtar, '%s_TUDOMANYOS.md' % azonosito), 'w', encoding='utf-8',
                      newline='\n') as f:
                f.write(lap_szoveg(eredmeny.nezetek['TUDOMANYOS']))
        cls.gyoker = kozos.GYOKER
        cls.mintalapok = kozos.MINTALAPOK

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.konyvtar)

    def test_a_kuszob_egyezik_a_generatoreval(self):
        from lapgen import konfig
        self.assertEqual(R.TSK_KUSZOB, konfig.TSK_SZAVAZAT_KUSZOB)

    def test_mindket_lapon_egyeznek(self):
        """Minden kimondott szám egyezik a független számlálással; a Döntési út, a KH és az LXX számai mindkét
        lapon állnak, az ISTENTISZT-001-en a szópár-lánc is."""
        for azonosito in self.mintalapok:
            sorok = R.szamlalok(azonosito, self.konyvtar, self.gyoker)
            _szoveg, hiba = R.szamlalo_jelentes(sorok, azonosito)
            self.assertFalse(hiba, '%s: %s' % (azonosito, _szoveg))
            meglevo = {nev for nev, lapon, _s in sorok if lapon is not None}
            for nev in ('megvizsgált versek (1.)', 'KH: utalások összesen (6.)', 'ószövetségi versek (5.)',
                        'LXX: az összesítés összege (5.)', 'LXX: egyező versek (5.)', 'LXX: LXX-minusz (5.)'):
                self.assertIn(nev, meglevo, azonosito)
        self.assertIn('a szópár igéje a héber szövegben (9.)',
                      {nev for nev, lapon, _s in R.szamlalok('ISTENTISZT-001', self.konyvtar, self.gyoker)
                       if lapon is not None})

    def test_nincs_ismert_elteres(self):
        """N238: az LXX-összesítés független számlálója; az egyetlen ismert eltérés (N196) szerkesztői döntéssel
        (2026-11-23, részenként) megszűnt: az eltérés minden motívumnál BUKÁS."""
        self.assertEqual(R.ISMERT_ELTERES, {})
        nev = 'LXX: egyező versek (5.)'
        self.assertTrue(R.szamlalo_jelentes([(nev, 12, 13)], 'ISTENTISZT-001')[1])
        self.assertFalse(R.szamlalo_jelentes([(nev, 13, 13)], 'ISTENTISZT-001')[1])

    def test_az_elrontott_szamot_kimutatja(self):
        ut = os.path.join(self.konyvtar, 'ISTENTISZT-001_TUDOMANYOS.md')
        with open(ut, encoding='utf-8') as f:
            eredeti = f.read()
        try:
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(eredeti.replace('versre terjednek', 'versre terjednek', 1).replace(
                    'A motívum ószövetségi helyei 16 versre', 'A motívum ószövetségi helyei 17 versre', 1))
            _szoveg, hiba = R.szamlalo_jelentes(R.szamlalok('ISTENTISZT-001', self.konyvtar, self.gyoker))
            self.assertTrue(hiba)
        finally:
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(eredeti)
