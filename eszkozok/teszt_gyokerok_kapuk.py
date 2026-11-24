#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gyokerok_kapuk.py -- F196 (és F240: az ellenoriz.py 44–48. szabálya, áladattal): az állítás–adat kapu (`eszkozok/ellenorzes/allitas_adat.py`) és a követelménylista-kapu
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


# ---------------------------------------------------------------------------------------------------------------------
# F240 (LXXBDB): az ellenoriz.py 44–48. szabálya és a két új modul (lxx_strong_javitas, bdb_konyvketto_javit), áladattal.
# A javítás előtti állapoton bukniuk kell, a javítotton nem (a független ellenőr kérése: a „régi állapoton bukik” próba
# reprodukálható legyen).

import shutil  # noqa: E402
import tempfile  # noqa: E402

import ellenoriz as E  # noqa: E402
import lxx_strong_javitas as LXJ  # noqa: E402
import bdb_konyvketto_javit as KK  # noqa: E402

_MACULA_FEJ = ['xml_id', 'ref', 'karoli', 'kk_mod', 'allapot', 'szo', 'lemma', 'strong', 'strong_x', 'strong_illesztes', 'morf',
               'szofaj', 'gloss', 'gorog_lxx', 'gorog_strong', 'gorog_lxx_forras', 'gorog_lxx_rahlfs']
_LXX_FEJ = ['igehely_lxx', 'igehely_kjv', 'igehely_karoli', 'karoli_ok', 'pozicio', 'szoalak', 'normalizalt', 'lemma', 'morf', 'strong',
            'strong_ok', 'proveniencia']


def _ir(ut, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join('\t'.join(s) for s in sorok) + '\n')


class LxxGyoker(object):
    """Áladat-gyökér: három vers, πρωὶ (G5459, a hibás címke) és μου (G3450, alakszám) a Macula-oldalon."""

    def __init__(self, javitva=False, alakszam=False):
        self.d = tempfile.mkdtemp(prefix='lxxbdb_')
        k = os.path.join(self.d, 'konkordancia')
        mac, lxx = [_MACULA_FEJ], [_LXX_FEJ]
        for n, ig in enumerate(('1Móz 1:5', '1Móz 1:8', '1Móz 1:13')):
            mac.append(['x%d' % n, '', ig, '', '', 'בֹּקֶר', '', 'H1242', '', '', '', '', '', 'πρωὶ', 'G5459', '', ''])
            mac.append(['y%d' % n, '', ig, '', '', 'אֱלֹהַי', '', 'H0430', '', '', '', '', '', 'μου', 'G3450', '', ''])
            lxx.append(['', '', ig, '', '1', 'πρωί', 'πρωι', 'πρωΐ', '', '4404', '', ''])
            lxx.append(['', '', ig, '', '2', 'μου', 'μου', 'ἐγώ', '', '1473', '', ''])
        _ir(os.path.join(k, 'Macula_heber_Genezis.tsv'), mac)
        _ir(os.path.join(k, 'LXX_OS', 'genesis.tsv'), lxx)
        _ir(os.path.join(k, 'Strong_szotar.tsv'), [['Strong-szám', 'Szótő', 'Kiejtés', 'Szófaj', 'Gyök/Származtatás', 'Jelentés'],
                                                   ['G5459', 'φωσφόρος', '', '', '', ''], ['G4404', 'πρωΐ', '', '', '', ''],
                                                   ['G3450', 'μου', '', '', '', ''], ['G1473', 'ἐγώ', '', '', '', '']])
        a = os.path.join(self.d, 'adat')
        _ir(os.path.join(a, 'kulso', 'lxx_bridge.tsv'), [['hebrew_strong', 'greek_strong', 'count'], ['H1242', 'G5459', '3'],
                                                         ['H0430', 'G3450', '3']])
        jav = [LXJ.JAVITAS_OSZLOPOK]
        if javitva:
            jav.append(['πρωι', 'G5459', 'G4404', 'masik_lemma', 'teszt', 'manual'])
        _ir(os.path.join(a, 'lxx_strong_javitas.tsv'), jav)
        gs = [['strong', 'rovid_jelentes', 'kategoria', 'kizaras_oka'], ['G1473', 'én', 'nevmas', 'teszt']]
        if alakszam:
            gs.append(['G3450', 'enyém', 'nevmas', 'teszt'])
        _ir(os.path.join(a, 'grammatikai_strongok.tsv'), gs)
        jel = [LXJ.JELOLT_OSZLOPOK]
        if javitva:
            jel.append(['G3450', 'μου', 'G1473', 'ἐγώ', '3', '3', 'μου', 'konvencio', 'teszt'])
        _ir(os.path.join(self.d, 'naplok', 'LXXBDB_lxx_jeloltek.tsv'), jel)
        self.adat = a

    def __enter__(self):
        return self

    def __exit__(self, *a):
        shutil.rmtree(self.d, ignore_errors=True)


class LxxStrongKapuk(unittest.TestCase):
    def test_alak_norm_es_javit(self):
        self.assertEqual(LXJ.alak_norm('πρωὶ'), LXJ.alak_norm('πρωί'))
        self.assertEqual(LXJ.javit('πρωὶ', 'G5459', {('πρωι', 'G5459'): ('G4404', '')}), ('G4404', True))
        self.assertEqual(LXJ.javit('μου', '3450', {}), ('G3450', False))

    def test_44_bukik_javitas_elott_es_atmegy_utana(self):
        with LxxGyoker() as g:
            s = E.szabaly44_lxx_macula_strong(g.adat)
            self.assertEqual(s.verdict, 'SÉRTÉS')
            self.assertTrue(any('G5459' in p for p in s.peldak))
        with LxxGyoker(javitva=True) as g:
            self.assertEqual(E.szabaly44_lxx_macula_strong(g.adat).verdict, 'RENDBEN')

    def test_45_nyelvtani_alakszam(self):
        with LxxGyoker(javitva=True) as g:
            self.assertEqual(E.szabaly45_lxx_nyelvtani(g.adat).verdict, 'SÉRTÉS')
        with LxxGyoker(javitva=True, alakszam=True) as g:
            self.assertEqual(E.szabaly45_lxx_nyelvtani(g.adat).verdict, 'RENDBEN')

    def test_bridge_kulonbseg_es_kuszob(self):
        with LxxGyoker(javitva=True) as g:
            br = {(r['hebrew_strong'], r['greek_strong']): int(r['count']) for r in LXJ.bridge_sorok(g.d)}
            self.assertNotIn(('H1242', 'G5459'), br)                  # 3 − 3 = 0: kiesik
            self.assertEqual(br.get(('H1242', 'G4404')), 3)           # új pár a teljes darabszámmal (≥ 3)

    def test_nyers_olvaso(self):
        d = tempfile.mkdtemp(prefix='lxxbdb_')
        try:
            _ir(os.path.join(d, 'eszkozok', 'x.py'), [["sorok('adat/kulso/lxx_bridge.tsv')"]])
            _ir(os.path.join(d, 'eszkozok', 'y.py'), [["import lxx_strong_javitas as LXJ"], ["LXJ.bridge_sorok(GY)"],
                                                      ["# forras=adat/kulso/lxx_bridge.tsv"]])
            self.assertEqual(E.lxx_nyers_olvasok(d), ['eszkozok/x.py'])
        finally:
            shutil.rmtree(d, ignore_errors=True)


class BdbKonyvkettoKapu(unittest.TestCase):
    def test_angol_jeloltek(self):
        j = KK.en_jeloltek('H0430', 'c. angels Psalm Psa 97:7 (x)')
        self.assertEqual([(x[1], x[5]) for x in j], [('Psalm Psa 97:7', 'javit')])
        j = KK.en_jeloltek('H0464', 'b. friend of Job Job 2:11')
        self.assertEqual([x[5] for x in j], ['marad'])
        self.assertEqual(KK.en_javit('c. angels Psalm Psa 97:7 (x)', KK.en_jeloltek('H0430', 'c. angels Psalm Psa 97:7 (x)')),
                         'c. angels Psa 97:7 (x)')

    def test_47_bukik_kettozesen(self):
        d = tempfile.mkdtemp(prefix='lxxbdb_')
        try:
            ford_fej = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forditas_hu', 'allapot', 'modell', 'datum',
                        'terminologia_verzio', 'megjegyzes']
            for en, hu, vart in (('c. angels Psalm Psa 97:7', 'c. angyalok Zsolt Zsolt 97:7', 'SÉRTÉS'),
                                 ('c. angels Psa 97:7', 'c. angyalok Zsolt 97:7', 'RENDBEN')):
                _ir(os.path.join(d, 'konkordancia', 'BDB_teljes_unabridged.tsv'),
                    [['Strong_padded', 'Strong_eredeti', 'Teljes_szocikk'], ['H0430', 'H430', en]])
                _ir(os.path.join(d, 'adat', 'forditasok.tsv'),
                    [ford_fej, ['BDB', 'H0430', 'H430', 'teljes', 'forditas_hu', 'x', hu, '', '', '', '', '']])
                self.assertEqual(E.szabaly47_bdb_konyvketto(os.path.join(d, 'adat')).verdict, vart, en)
        finally:
            shutil.rmtree(d, ignore_errors=True)


class VersJelentesKapu(unittest.TestCase):
    def _tabla(self, d, n):
        fej = ['strong', 'bdb_id', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz',
               'resz', 'utvonal', 'okkod', 'szurt', 'csoport', 'csoport_jel', 'proveniencia', 'bizonyossag']
        sorok = [fej] + [['H8415', '', str(i), str(i), 'Gen 1:%d' % i, '', '', '1Móz 1:%d' % i, '', '', '', '-/5', '', '', '', '', '',
                          'ketes:jp_illesztes'] for i in range(1, n + 1)]
        _ir(os.path.join(d, 'bdb_vers_jelentes.tsv'), sorok)

    def test_48_beragadt_futam(self):
        d = tempfile.mkdtemp(prefix='lxxbdb_')
        try:
            self._tabla(d, 11)
            self.assertEqual(E.vj_beragadt_futamok(d), [('H8415', '-/5', 11)])
            self.assertEqual(E.szabaly48_vj_beragadt(d).verdict, 'SÉRTÉS')
            self._tabla(d, 4)
            self.assertEqual(E.vj_beragadt_futamok(d), [])
            self.assertNotEqual(E.szabaly48_vj_beragadt(d).verdict, 'SÉRTÉS')
        finally:
            shutil.rmtree(d, ignore_errors=True)


class BdbKonyvfeloldasKapu(unittest.TestCase):
    """F240.L7: a „könyvszó + más könyv hivatkozása” minta (49. szabály) — a hiba bukik, a név és a kettőzés nem."""

    def test_minta(self):
        import bdb_konyvfeloldas_javit as KF
        self.assertEqual([x[0] for x in KF.en_maradek('H9999', 'Qal Perfect Joel 1Sam 4:13')], ['4:13'])
        self.assertEqual([x[0] for x in KF.en_maradek('H9999', 'on marchNum 2Chr 33:2')], ['33:2'])     # tapadt könyvszó
        self.assertEqual(KF.en_maradek('H0295', 'a chief of Dan Num 1:12'), [])                        # név, kivétel
        self.assertEqual(KF.en_maradek('H9999', '16t. Daniel; Ezra 5:11'), [])                          # darabszám-összegzés
        self.assertEqual(KF.en_maradek('H9999', 'angels Psalm Psa 97:7'), [])                           # kettőzés: a 47. méri
        self.assertEqual([x[0] for x in KF.hu_maradek('H9999', 'csak Jóel 1Sám 4:13')], ['4:13'])
        self.assertEqual(KF.hu_maradek('H9999', 'csak Jóel 4:13'), [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
