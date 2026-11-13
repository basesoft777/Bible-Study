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
        repo = _repo(**kw)
        self.repok.append(repo)
        with open(os.path.join(self.uj, 'PROBA-001_TUDOMANYOS.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj_szoveg)
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

    def test_a_meg_nem_kesz_szakasz_engedelye_nem_szamit(self):
        """Részleges lapnál a még el nem készült szakasz engedélysora nem BUKÁS."""
        eng = [('E9', 'TUDOMANYOS', '1. Első', 'T', 'sor', R.sor_hash('első sor'), R.sor_hash('x'), '1', 'ok')]
        self.assertFalse(self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', engedelyek=eng)['bukas'])

    def test_bemenet_hash_or(self):
        """A mérce bemenetének változása kimondott hibával megállítja a mérést."""
        with self.assertRaises(R.MerceHiba) as hiba:
            self._meres('## 2. Második\n\nA sor\nB sor\nC sor\n\n', rogzitett_bemenet='régi tartalom\n')
        self.assertIn('a mérce bemenete megváltozott: B03 adat/be.tsv', '%s' % hiba.exception)

    def test_hash_or_sorveg_fuggetlen(self):
        repo = _repo()
        self.repok.append(repo)
        ut = os.path.join(repo.gyoker, 'lexikon', 'PROBA-001_TUDOMANYOS.md')
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(REFERENCIA.replace('\n', '\r\n'))
        self.assertEqual(R.hash_or(repo.gyoker), 2)


if __name__ == '__main__':
    unittest.main(verbosity=1)
