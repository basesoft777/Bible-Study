#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gyokerok_kapuk.py -- F196: az állítás–adat kapu (`eszkozok/ellenorzes/allitas_adat.py`) és a követelménylista-kapu
(`eszkozok/ellenorzes/kovetelmeny_kapu.py`) tesztjei.

A tiszta esetek áladattal futnak (gyorsak); a `Valodi` osztály a commitolt HAMART-001 lapot és a valódi adatot méri,
és egy rontott lapmásolaton is (a gyökérok-példa: „nincs rögzített kapcsolat” 56 kapcsolat-sor mellett).

Futtatás a repó gyökeréből:
    python eszkozok/teszt_gyokerok_kapuk.py
"""

import io
import os
import sys
import unittest

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ITT)
sys.path.insert(0, os.path.join(_ITT, 'ellenorzes'))

import allitas_adat as A  # noqa: E402
import kovetelmeny_kapu as K  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(_ITT)


class AlAdat(object):
    """Álnév-adat: `ertek(kulcs)` a szótárból; hiányzó kulcs: NemMerheto. A melléklet listája a `mell` kulcson."""

    def __init__(self, ertekek, mell=None):
        self.ertekek = ertekek
        self.mell = mell or {'csoport': {}, 'egyen': {}}

    def ertek(self, kulcs):
        if kulcs not in self.ertekek:
            raise A.NemMerheto('nincs: %r' % (kulcs,))
        return self.ertekek[kulcs]

    def _melleklet(self):
        return self.mell


def allapotok(eredmeny):
    return [(r.azonosito, r.lapon, r.adatban, r.allapot) for r in eredmeny]


# ---------------------------------------------------------------------------
# Állítás–adat kapu
# ---------------------------------------------------------------------------

class SzamEsSzoveg(unittest.TestCase):
    def test_szam_ezres_tagolas(self):
        self.assertEqual(A.szam('1 742'), 1742)
        self.assertEqual(A.szam('1 796'), 1796)
        self.assertEqual(A.szam('56'), 56)

    def test_lathato_megtartja_a_sorszamot(self):
        szoveg = 'a\n<!-- rejtett\n56 kapcsolat 2 helyet köt össze -->\nb'
        lat = A.lathato(szoveg)
        self.assertEqual(lat.count('\n'), szoveg.count('\n'))
        self.assertNotIn('56 kapcsolat', lat)


class AllitasAdat(unittest.TestCase):
    def test_gyokerok_pelda_nincs_kapcsolat_56_sor_mellett(self):
        """A memória gyökérok-példája: a lap „nincs rögzített kapcsolat”-ot mond, a tábla 56 sort tartalmaz."""
        e = A.meres_szoveg('### Alátámasztás\n\nA motívumhoz nincs rögzített kapcsolat.\n', AlAdat({'kapcs': 56}))
        self.assertEqual(allapotok(e), [('NINCS_KAPCS', 0, 56, A.ELTER)])
        self.assertEqual(e[0].sor, 3)

    def test_lxx_osszesito_uj_cimkekkel(self):
        """ELLENOR_F196 2.: az új szerkezetű lap 5. táblájának összesítője olvasói címkékkel."""
        szov = ('*Összesítés: egyező=6, eltérő=28, LXX-minusz=0, a megfelelő nincs megállapítva=11, versszámozás miatt '
                'nem párosítva=1.*')
        e = A.meres_szoveg(szov, AlAdat({'lxx_egyezo': 6, 'lxx_eltero': 28, 'lxx_minusz': 0, 'lxx_fuggoben': 11,
                                         'lxx_szamozas': 2}))
        self.assertEqual([(r.lapon, r.adatban) for r in e if r.allapot == A.ELTER], [(1, 2)])
        self.assertEqual(len(e), 5)

    def test_nincs_mondat_ures_adatnal_egyezik(self):
        e = A.meres_szoveg('Ehhez a motívumhoz nincs rögzített kapcsolat.', AlAdat({'kapcs': 0}))
        self.assertEqual(allapotok(e), [('NINCS_KAPCS', 0, 0, A.EGYEZIK)])

    def test_kapcsolat_osszegzes_es_tipusok(self):
        szov = ('56 kapcsolat 42 helyet köt össze: 43 párhuzam, 7 kontraszt, 6 variáns; 26 magas, 30 alacsonyabb '
                'bizonyosságú.')
        adat = {'kapcs': 56, 'kapcs_csomopont': 42, 'kapcs_magas': 26, 'kapcs_alacsonyabb': 30,
                ('kapcs_tipus', 'párhuzam'): 43, ('kapcs_tipus', 'kontraszt'): 7, ('kapcs_tipus', 'variáns'): 6}
        e = A.meres_szoveg(szov, AlAdat(adat))
        self.assertEqual(len(e), 7)
        self.assertTrue(all(r.allapot == A.EGYEZIK for r in e))
        adat[('kapcs_tipus', 'kontraszt')] = 8
        e = A.meres_szoveg(szov, AlAdat(adat))
        self.assertEqual([(r.leiras, r.lapon, r.adatban) for r in e if r.allapot == A.ELTER],
                         [('a 7. összegzés: típusonként [kontraszt]', 7, 8)])

    def test_megjegyzesben_allo_szam_nem_allitas(self):
        e = A.meres_szoveg('<!-- A motívumhoz nincs rögzített kapcsolat. -->', AlAdat({'kapcs': 56}))
        self.assertEqual(e, [])

    def test_nem_merheto_nem_egyezes(self):
        e = A.meres_szoveg('A motívumhoz nincs rögzített kapcsolat.', AlAdat({}))
        self.assertEqual(e[0].allapot, A.NEM_MERHETO)

    def test_lxx_opcionalis_tagok(self):
        szov = ('A motívum ószövetségi helyei 46 versre terjednek; ezek közül 6 versben a görög fordítás (Septuaginta) '
                'ugyanazt a szót használja, mint az Újszövetség; 28 versben mást, 12 versben a megfelelő nincs '
                'megállapítva.')
        e = A.meres_szoveg(szov, AlAdat({'lxx_n': 46, 'lxx_egyezo': 6, 'lxx_eltero': 28, 'lxx_egyeb': 11}))
        self.assertEqual([(r.lapon, r.adatban) for r in e if r.allapot == A.ELTER], [(12, 11)])
        self.assertEqual(len(e), 4)   # a hiányzó „görögből hiányzik” tag nem mér

    def test_elofordulas_es_kivonat(self):
        szov = ('A motívum 47 igehelyen fordul elő, 14 bibliai könyvben (41 ószövetségi, 6 újszövetségi hely). 42 hely '
                'azonosítása magas megbízhatóságú, 5 alacsonyabb.\n\nA lap 47 helyet sorol fel 54 versben: 23-at a '
                'Genezisből, 18-at az Ószövetség többi könyvéből és 6-ot az Újszövetségből.')
        adat = {'hely': 47, 'konyv': 14, 'osz': 41, 'usz': 6, 'magas': 42, 'vers': 54, 'genezis': 23, 'osz_tobbi': 18}
        e = A.meres_szoveg(szov, AlAdat(adat))
        self.assertTrue(e and all(r.allapot == A.EGYEZIK for r in e), allapotok(e))
        adat['vers'] = 53
        self.assertEqual([r.lapon for r in A.meres_szoveg(szov, AlAdat(adat)) if r.allapot == A.ELTER], [54])

    def test_lenyithato_ok_az_alcim_szerint(self):
        """Ugyanaz az ok csoportos és egyenkénti is lehet: az 1.3 alcíme dönti el, melyik számhoz mér."""
        sor = '<details><summary><strong>emberi átkozódás</strong> — %d vers</summary></details>'
        szov = '#### Csoportosan kizárt versek\n\n%s\n\n#### Egyenként elutasított versek\n\n%s' % (sor % 1, sor % 9)
        adat = {('csoport_ok', 'emberi átkozódás'): 1, ('egyen_ok', 'emberi átkozódás'): 9}
        e = A.meres_szoveg(szov, AlAdat(adat))
        self.assertEqual([(r.lapon, r.allapot) for r in e], [(1, A.EGYEZIK), (9, A.EGYEZIK)])

    def test_melleklet_listaja_tagonkent(self):
        szov = ('## Csoportosan kizárt versek, okonként\n\n### más szó — 3 vers\n\n<details>\n\n'
                '- **1Kir** (2): 1:52, 2:8\n- **Jób** (1): 3:8\n\n</details>\n')
        adat = AlAdat({('csoport_ok', 'más szó'): 3, ('mell_ok', ('csoport', 'más szó')): 3},
                      mell={'csoport': {'más szó': ['1Kir 1:52', '1Kir 2:8', 'Jób 3:9']}, 'egyen': {}})
        e = A.meres_szoveg(szov, adat, 'melleklet')
        az = {r.azonosito: r for r in e}
        self.assertEqual(az['MELL_OK'].allapot, A.EGYEZIK)
        self.assertEqual(az['MELL_LISTA'].allapot, A.EGYEZIK)
        self.assertEqual(az['MELL_LISTA_TAG'].allapot, A.ELTER)
        self.assertIn('1 vers csak a mellékletben, 1 csak az adatban', az['MELL_LISTA_TAG'].megjegyzes)

    def test_jelentes_es_kilepesi_kod(self):
        e = {'X-001': {'lap': A.meres_szoveg('A motívumhoz nincs rögzített kapcsolat.', AlAdat({'kapcs': 5})),
                       'melleklet': [], 'hiba': None}}
        j = A.jelentes(e)
        self.assertIn('1 állítás: 0 egyezik, 1 eltér, 0 nem mérhető.', j)
        regi = A.meres
        try:
            A.meres = lambda mid: e[mid]
            self.assertEqual(A.main(['X-001']), 0)          # JELENTÉS: nem gátol
            self.assertEqual(A.main(['X-001', '--szigoru']), 1)
        finally:
            A.meres = regi


class Valodi(unittest.TestCase):
    """A commitolt HAMART-001 lap a valódi adaton (lassabb, ~10 mp)."""

    @classmethod
    def setUpClass(cls):
        cls.adat = A.Adat('HAMART-001')
        with io.open(os.path.join(GYOKER, 'lexikon', 'HAMART-001_TUDOMANYOS.md'), encoding='utf-8') as f:
            cls.lap = f.read()

    def test_a_kapcsolat_kulcs_a_generator_tablajabol(self):
        import lexikon_general as LG
        self.assertEqual(self.adat.ertek('kapcs'), sum(1 for r in LG.kapcsolatok_sorok() if r['id'] == 'HAMART-001'))
        self.assertEqual(self.adat.ertek('osszes'), LG.dontesi_ut_adat(self.adat.m, self.adat.sorai)['osszes'])

    def test_rontott_lap_jelez(self):
        e = A.meres_szoveg(self.lap + '\n\nA motívumhoz nincs rögzített kapcsolat.\n', self.adat)
        rossz = [r for r in e if r.azonosito == 'NINCS_KAPCS']
        self.assertEqual(len(rossz), 1)
        self.assertEqual(rossz[0].allapot, A.ELTER)
        self.assertGreater(rossz[0].adatban, 0)
        n = self.adat.ertek('hely')
        regi = '%d helyet sorol fel' % n
        if regi in self.lap:   # a Kivonat próza: ha a mondat átfogalmazódik, ez a rész nem mér
            e = A.meres_szoveg(self.lap.replace(regi, '%d helyet sorol fel' % (n + 1)), self.adat)
            self.assertTrue(any(r.azonosito == 'KIVONAT_HELY_VERS' and r.allapot == A.ELTER for r in e))


# ---------------------------------------------------------------------------
# Követelménylista-kapu
# ---------------------------------------------------------------------------

OLV = {'ATIRAS', 'ATIRAS_VALT', 'KIVONAT_SZAM', 'BELSO', 'VISSZHANG', 'KOLOFON'}


class Cella(unittest.TestCase):
    def cel(self, c):
        return K.szabalyok_a_cellabol(c, OLV)

    def test_ember(self):
        for c in ('lektor', 'szerkesztő', 'lektor (a menetnaplóból)', 'gépi: nincs',
                  'gépi: nincs (a 4.11-ben a `strong_valtozat_versben`)', 'gépi: tervezett (F18 (c))',
                  'gépi: `teszt_olvasoi_kovetkeztetes.py` (tervezett)'):
            self.assertEqual(self.cel(c)[0], K.EMBER, c)

    def test_ellenoriz_szamok(self):
        o, sz, _ = self.cel('gépi: `ellenoriz.py` 36., 37., 38.')
        self.assertEqual((o, [s.azon for s in sz]), (K.GEPI, ['36', '37', '38']))
        self.assertEqual([s.azon for s in self.cel('gépi: `ellenoriz.py` 2/b')[1]], ['2/b'])
        self.assertEqual([s.azon for s in self.cel('gépi: 39. (a döntés-commit frissíti az ujjlenyomatot)')[1]], ['39'])

    def test_vegyes(self):
        sz = self.cel('gépi: ATIRAS (BUKÁS), ATIRAS_VALT (FIGY), `ellenoriz.py` 22. (JELENTÉS)')[1]
        self.assertEqual(sz, [K.Szabaly('ellenoriz', '22'), K.Szabaly('olvasoi', 'ATIRAS'),
                              K.Szabaly('olvasoi', 'ATIRAS_VALT')])
        sz = self.cel('gépi: a #182 42. szabálya (F31), CI E19')[1]
        self.assertEqual(sz, [K.Szabaly('ellenoriz', '42'), K.Szabaly('ci', 'E19')])
        self.assertEqual(self.cel('gépi: V7 (csak a 4.11); egyébként lektor')[1], [K.Szabaly('visszhang', 'V7')])
        self.assertEqual(self.cel('gépi: az állítás–adat kapu (`allitas_adat.py`)')[1],
                         [K.Szabaly('allitas', 'allitas_adat')])

    def test_olvasoi_kapu_egesze_es_vegyes_cella(self):
        """ELLENOR_F196 3.: a K03 „olvasói kapu (Feed 9)” szabálya; a vegyes cella „részben gépi” jelölést kap."""
        o, sz, megj = self.cel('gépi: olvasói kapu (Feed 9), `ellenoriz.py` 40.')
        self.assertIn(K.Szabaly('olvasoi_egesz', 'BUKÁS'), sz)
        self.assertFalse(megj.startswith('részben gépi'))
        for c in ('gépi: BELSO; lektor', 'gépi: grep a markerre; CI E11', 'gépi: BELSO; a mért számra: nincs'):
            self.assertTrue(self.cel(c)[2].startswith('részben gépi'), c)

    def test_nem_gyujtheto(self):
        for c in ('gépi: az F24 kapuja', 'gépi: az F27 (b) kapuja (a #182 2. fázisa)', 'gépi: a lap 1.2 táblája',
                  'gépi + szerkesztő'):
            self.assertEqual(self.cel(c)[0], K.NEM_GYUJTHETO, c)

    def test_lista_beolvasasa(self):
        sorok = K.lista_sorai()
        self.assertGreaterEqual(len(sorok), 100)
        self.assertEqual(sorok[0].k, 'K01')
        self.assertTrue(all(s.ellenorzes for s in sorok))

    def test_escape_pipe(self):
        self.assertEqual(K.cellak('| K1 | a \\| b | c |'), ['K1', 'a \\| b', 'c'])


class AlFuttato(object):
    def __init__(self, eredmenyek):
        self.e = eredmenyek

    def eredmeny(self, sz):
        return self.e.get(sz, (True, '', False))


class KovetelmenyMeres(unittest.TestCase):
    def sorok(self):
        S = K.Sor
        return [S('K01', 'egész lap', 'a', 'f', 'gépi: BELSO', '**teljesül** — x'),
                S('K02', 'egész lap', 'b', 'f', 'gépi: `ellenoriz.py` 40., KIVONAT_SZAM', '**teljesül**'),
                S('K03', 'Kivonat', 'c', 'f', 'lektor', '**teljesül**'),
                S('K04', 'Kivonat', 'd', 'f', 'gépi: az F24 kapuja', '**részben**')]

    def test_n_per_m_es_lista(self):
        f = AlFuttato({K.Szabaly('olvasoi', 'KIVONAT_SZAM'): (False, '2 találat (FIGYELMEZTETÉS)', False)})
        e = K.meres('HAMART-001', self.sorok(), futtato=f)
        self.assertEqual(K.osszegzo_sor('HAMART-001', e),
                         'HAMART-001: 1/2 követelmény teljesül (gépi) — az 1 nem teljesülőből 0 gátló szintű, '
                         '1 csak figyelmeztetés')
        j = K.jelentes('HAMART-001', e)
        self.assertIn('| K02 | egész lap | figyelmeztetés | KIVONAT_SZAM: 2 találat (FIGYELMEZTETÉS) | teljesül |', j)
        self.assertIn('K02 (lista: teljesül, gép: nem teljesül, figyelmeztetés)', j)
        self.assertIn('1 ember ellenőrzi, 1 gépi, de a kapu nem gyűjti', j)

    def test_gatlo_szint(self):
        f = AlFuttato({K.Szabaly('olvasoi', 'BELSO'): (False, '1 találat (BUKÁS)', True),
                       K.Szabaly('olvasoi', 'KIVONAT_SZAM'): (False, '2 találat (FIGYELMEZTETÉS)', False)})
        e = K.meres('X-001', self.sorok(), futtato=f)
        self.assertEqual([(m.sor.k, m.kemeny) for m in e if m.osztaly == K.GEPI], [('K01', True), ('K02', False)])
        self.assertIn('2 nem teljesülőből 1 gátló szintű, 1 csak figyelmeztetés', K.osszegzo_sor('X-001', e))

    def test_lapra_nem_futo_ci_szabaly_nem_teljesul(self):
        """ELLENOR_F196 1.: az E19 és az E34 a lapfájlra nem mér: nem gyűjthető, nem „teljesül”."""
        f = K.Futtato('HAMART-001')
        for e in ('E19', 'E34'):
            self.assertIsNone(f.ci_eredmeny(e)[0], e)

    def test_csupa_nem_merheto_allitas_nem_teljesul(self):
        """ELLENOR_F196 4.: csupa nem mérhető állításnál az állítás–adat szabály nem gyűjthető."""
        regi = A.meres
        try:
            A.meres = lambda mid: {'lap': [A.Eredmeny('X', 'x', 'lap', 1, 0, None, A.NEM_MERHETO, '')],
                                   'melleklet': [], 'hiba': None}
            self.assertIsNone(K.Futtato('X-001').allitas_eredmeny()[0])
        finally:
            A.meres = regi

    def test_nem_gyujtott_szabaly_nem_teljesules(self):
        f = AlFuttato({K.Szabaly('olvasoi', 'BELSO'): (None, 'hiba', None)})
        e = K.meres('X-001', self.sorok()[:1], futtato=f)
        self.assertEqual(e[0].osztaly, K.NEM_GYUJTHETO)
        self.assertEqual(K.osszegzo_sor('X-001', e), 'X-001: 0/0 követelmény teljesül (gépi)')


if __name__ == '__main__':
    unittest.main(verbosity=1)
