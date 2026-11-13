"""A bemeneti réteg tesztjei: jegyzék, fejléckapu, hiány, olvasási napló, névtábla (GK-23), sablontábla."""
import os
import unittest

import kozos
from kozos import JEGYZEK_FEJLEC, alap_minirepo, tsv
from lapgen import bemenet
from lapgen.bemenet.jegyzek import Bemenet, BemenetHiba
from lapgen.szoveg import Kulcs, MotivumId, SablonHiba


class Nevtabla(unittest.TestCase):
    def setUp(self):
        self.repo = alap_minirepo(
            nevek=[('megbizhatosag', 'magas', 'magas', 'uj'), ('forras', 'B07', 'a Károli-fordítás', 'uj')],
            sablonok=[('proba.mondat', 'A forrás: {f}.', 'f:nev(forras)', 'teszt', 'uj', 'var')])
        self.b = Bemenet(self.repo.gyoker)

    def tearDown(self):
        self.repo.torol()

    def test_gk23_ismeretlen_kulcs_kivetel(self):
        """GK-23: ismeretlen névtábla-kulcs kivétel; a kulcs soha nem kerül ki olvasói név helyett."""
        nevek = bemenet.b65_nevtabla(self.b)
        self.assertEqual(nevek.nev('megbizhatosag', 'magas').kulcs, 'magas')
        self.assertEqual(nevek.nev('megbizhatosag', Kulcs('magas', 'megbizhatosag')).kulcs, 'magas')
        with self.assertRaises(bemenet.NevHiba):
            nevek.nev('megbizhatosag', 'ismeretlen_kulcs')
        with self.assertRaises(bemenet.NevHiba):
            nevek.nev('nincs_ilyen_tipus', 'magas')

    def test_gk23_ismeretlen_sablonkulcs_kivetel(self):
        ny = bemenet.nyelv(self.b)
        with self.assertRaises(bemenet.NevHiba):
            ny.s('nincs.ilyen.mondat')

    def test_sablon_a_nevtablaval(self):
        from lapgen.megjelenites.md.iro import Lapiro
        ny = bemenet.nyelv(self.b)
        lap = Lapiro()
        lap.sor(ny.s('proba.mondat', f=ny.nev('forras', 'B07')))
        self.assertEqual(lap.kesz()[0].szoveg, 'A forrás: a Károli-fordítás.')


class TablaKapuk(unittest.TestCase):
    def test_ismetlodo_nevtabla_kulcs_bukas(self):
        repo = alap_minirepo(nevek=[('t', 'k', 'egy', 'uj'), ('t', 'k', 'kettő', 'uj')])
        try:
            with self.assertRaises(BemenetHiba):
                bemenet.b65_nevtabla(Bemenet(repo.gyoker))
        finally:
            repo.torol()

    def test_hibas_sablonsor_betolteskor_bukik(self):
        repo = alap_minirepo(sablonok=[('rossz', 'A {x} nincs leírva.', '-', 't', 'uj', 'var')])
        try:
            with self.assertRaises(SablonHiba):
                bemenet.b66_sablonok(Bemenet(repo.gyoker))
        finally:
            repo.torol()

    def test_hianyzo_oszlop_bukas(self):
        """Fejléckapu oszlopnév szerint: hiányzó oszlopnál BUKÁS."""
        repo = alap_minirepo(tovabbi={'adat/olvasoi_nevtabla.tsv': tsv(('tipus', 'kulcs', 'nev'), ('t', 'k', 'n'))})
        try:
            with self.assertRaises(BemenetHiba):
                bemenet.b65_nevtabla(Bemenet(repo.gyoker))
        finally:
            repo.torol()

    def test_gk06_hianyzo_kotelezo_bemenet_bukas(self):
        """GK-06: hiányzó kötelező bemeneti fájl BUKÁS, nem üres lista."""
        repo = alap_minirepo()
        try:
            os.remove(os.path.join(repo.gyoker, 'adat', 'lap_befagyasztas.tsv'))
            with self.assertRaises(BemenetHiba):
                bemenet.b59_befagyasztott(Bemenet(repo.gyoker))
        finally:
            repo.torol()

    def test_jegyzek_kapui(self):
        for sor in (('B65', 'x.tsv', 'ismétlődő', 'igen', '-', '-', 'aktiv', '-', '-', 'm'),
                    ('B70', 'x.tsv', 'rossz kötelező', 'talan', '-', '-', 'aktiv', '-', '-', 'm'),
                    ('B70', 'x.tsv', 'rossz állapot', 'igen', '-', '-', 'ismeretlen', '-', '-', 'm')):
            repo = alap_minirepo(jegyzek_sorok=[sor])
            try:
                with self.assertRaises(BemenetHiba):
                    Bemenet(repo.gyoker)
            finally:
                repo.torol()
        repo = alap_minirepo(tovabbi={'adat/lapgen_bemenetek.tsv': tsv(JEGYZEK_FEJLEC[:-1])})
        try:
            with self.assertRaises(BemenetHiba):
                Bemenet(repo.gyoker)
        finally:
            repo.torol()

    def test_ismeretlen_bemenet_azonosito(self):
        repo = alap_minirepo()
        try:
            with self.assertRaises(BemenetHiba):
                Bemenet(repo.gyoker)._tabla('B99')
        finally:
            repo.torol()


class OlvasasiNaplo(unittest.TestCase):
    def test_naplo_es_figyelo(self):
        """Minden olvasás a naplóba kerül (B-azonosító, útvonal, hash); a figyelő a blokk olvasásait gyűjti,
        a gyorsítótárból kiszolgáltakat is."""
        repo = alap_minirepo()
        try:
            b = Bemenet(repo.gyoker)
            bemenet.b59_befagyasztott(b)
            with b.figyel() as forrasok:
                self.assertEqual(bemenet.b59_befagyasztott(b), frozenset({MotivumId('FAGYOTT-001')}))
            self.assertEqual(forrasok, {'B59'})
            naplo = b.olvasasi_naplo()
            self.assertEqual([(o.b_id, o.utvonal) for o in naplo],
                             [('B68', 'adat/lapgen_bemenetek.tsv'), ('B59', 'adat/lap_befagyasztas.tsv')])
            self.assertEqual([len(o.sha256) for o in naplo], [64, 64])
        finally:
            repo.torol()

    def test_a_jegyzek_olvasasa_is_a_naploban_all(self):
        """A jegyzéktábla saját olvasása is naplózott olvasás (a jegyzék egy sora magára a jegyzékre mutat); ha
        nincs ilyen sor, a munkamenet nem nyílik meg. A blokk forráslistájába a jegyzék nem kerül."""
        repo = alap_minirepo()
        try:
            b = Bemenet(repo.gyoker)
            self.assertEqual([(o.b_id, o.utvonal) for o in b.olvasasi_naplo()],
                             [('B68', 'adat/lapgen_bemenetek.tsv')])
            with b.figyel() as forrasok:
                bemenet.b59_befagyasztott(b)
            self.assertEqual(forrasok, {'B59'})
        finally:
            repo.torol()
        jegyzek = tsv(JEGYZEK_FEJLEC,
                      ('B59', 'adat/lap_befagyasztas.tsv', 'befagyasztott', 'igen', '-', '-', 'aktiv', '-', '-', 'm'))
        repo = alap_minirepo(tovabbi={'adat/lapgen_bemenetek.tsv': jegyzek})
        try:
            with self.assertRaises(BemenetHiba):
                Bemenet(repo.gyoker)
        finally:
            repo.torol()

    def test_naplozas_nelkuli_olvasas_nincs(self):
        """A bemeneti réteg magjában egyetlen fájlnyitás áll (`_fajl`), és minden hívója naplóz; a párosítás (B54)
        könyv–fájl leképezése a valós adaton minden fájlt a naplóba ír."""
        import ast
        from kozos import fa
        nyitok = [c.lineno for c in ast.walk(fa('bemenet/jegyzek.py'))
                  if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == 'open']
        self.assertEqual(len(nyitok), 1)
        for fuggveny in ast.walk(fa('bemenet/jegyzek.py')):
            if not isinstance(fuggveny, ast.FunctionDef) or fuggveny.name == '_fajl':
                continue
            hivasok = {c.func.attr for c in ast.walk(fuggveny)
                       if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)}
            if '_fajl' in hivasok:
                self.assertIn('_naploz', hivasok, '%s: olvas, de nem naplóz' % fuggveny.name)
        from lapgen.bemenet import szavak
        b = Bemenet(kozos.GYOKER)
        szavak.b54_karoli_parok(b)
        naplozott = sorted(o.utvonal for o in b.olvasasi_naplo() if o.b_id == 'B54')
        self.assertEqual(naplozott, sorted(b._utvonalak('B54')))
        self.assertGreater(len(naplozott), 1)

    def test_hash_sorveg_fuggetlen(self):
        """A hash a sorvég-normalizált tartalomból számolódik: CRLF és LF fájl hash-e egyezik."""
        hashek = []
        for sorveg in ('\n', '\r\n'):
            repo = alap_minirepo()
            try:
                ut = os.path.join(repo.gyoker, 'adat', 'lap_befagyasztas.tsv')
                with open(ut, 'w', encoding='utf-8', newline='') as f:
                    f.write(sorveg.join(['id\tok\tdontes\tdatum', 'FAGYOTT-001\tok\td\t2026-11-12', '']))
                b = Bemenet(repo.gyoker)
                self.assertEqual(len(bemenet.b59_befagyasztott(b)), 1)
                hashek.append([o.sha256 for o in b.olvasasi_naplo() if o.b_id == 'B59'][0])
            finally:
                repo.torol()
        self.assertEqual(hashek[0], hashek[1])

    def test_festett_munkamenet_jelzoszavai(self):
        repo = alap_minirepo()
        try:
            b = Bemenet(repo.gyoker, festek=True)
            self.assertIn('ZZQB03_megjegyzesZZ', b.belso('B03', 'megjegyzes', 'belső szöveg').szoveg)
            self.assertEqual(b.festo.kategoriak['ZZQB03_megjegyzesZZ'], 'belso')
            self.assertEqual(b.kezi('B03', 'kapcsolodas', 'próza').szoveg, 'próza ZZQB03_kapcsolodasZZ')
            self.assertEqual(Bemenet(repo.gyoker).belso('B03', 'megjegyzes', 'x').szoveg, 'x')
            with self.assertRaises(BemenetHiba):
                b.kezi('B03', 'megjegyzes', 'ugyanaz a mező két kategóriában')
        finally:
            repo.torol()


class EloTablak(unittest.TestCase):
    def test_az_eles_tablak_betolthetok(self):
        """A repó három lapgen-táblája betölthető, minden sablonsor érvényes."""
        b = Bemenet(kozos.GYOKER)
        ny = bemenet.nyelv(b)
        self.assertIsNotNone(ny)
        self.assertIsInstance(bemenet.b59_befagyasztott(b), frozenset)


if __name__ == '__main__':
    unittest.main(verbosity=1)
