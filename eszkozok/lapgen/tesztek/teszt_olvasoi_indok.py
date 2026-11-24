"""Az olvasói indoklások táblája (B76) és a szókincs-kapu (F241.5b, D15).

A tábla kapuja betöltéskor fut: a valódi adaton átmegy; árva hash-nél, belső szónál (D17 (1)) és egy fogalom második
nevénél (névazonosság, D17 (2)) megáll. A lapra kerülő indoklás olvasói alak nélkül csak akkor állhat, ha átmegy a szókincs-kapun. A
szakszó-lista egy helyen áll (a lap minta-ellenőrzése is innen olvas). A B56 címkéje és megjegyzése a kapu alatt áll.
A kereszthivatkozásból vizsgált sorok a 3. és a 6. szakaszban ugyanazok a döntésnapló-sorok (a 3. szakasz ezért csak
hivatkozik a 6. táblájára, D15 (2)).
"""
import unittest

import kozos
from kozos import alap_minirepo, tsv
from lapgen import szokincs
from lapgen.bemenet import Bemenet
from lapgen.bemenet import dontes as dontes_be
from lapgen.bemenet import kereszthiv as kh_be
from lapgen.bemenet import olvasoi_indok as OI
from lapgen.bemenet import vizsgalt as vizsgalt_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import Dontes, VizsgaltCsoport
from lapgen.szoveg import MotivumId

_MOTIVUM = 'PROBA-001'
_INDOK = 'Név nélküli hívás, a fölérendelt fogalomhoz tartozik.'
_TISZTA = 'A versben nem áll a név.'
_FEJ_TAGABB = ('fej.tagabb', '**A tágabb kör** (ha egy hely csak ezen át tartozna ide, kimarad). {fol}.',
               'fol:lathato', 'fej', 'x', '-')


def _repo(olvasoi_sorok, b56_sorok=()):
    jegyzek = [
        ('B04', 'adat/jeloltek.tsv', 'j', 'igen', '-', '-', 'aktiv', '-', '-', 'manual'),
        ('B56', 'adat/elutasitasi_okok.tsv', 'o', 'igen', '-', '-', 'aktiv', '-', '-', 'manual'),
        ('B76', 'adat/olvasoi_indoklasok.tsv', 'oi', 'igen', '-', '-', 'aktiv', '-', '-', 'manual')]
    tovabbi = {
        'adat/jeloltek.tsv': tsv(dontes_be._JELOLT_OSZLOPOK,
                                 (_MOTIVUM, 'Zsolt 1:1', 'TSK Zsolt 2:2', 'elutasítva', _INDOK + ' | farok', 'elofordulas'),
                                 (_MOTIVUM, 'Zsolt 1:2', 'TSK Zsolt 2:2', 'elutasítva', _TISZTA, 'elofordulas')),
        'adat/olvasoi_indoklasok.tsv': tsv('# teszt', OI.OSZLOPOK, *olvasoi_sorok),
        'adat/elutasitasi_okok.tsv': tsv(('sorrend', 'id', 'minta', 'cimke', 'megjegyzes', 'proveniencia'),
                                         ('1', '*', 'hívás', 'név nélküli hívás', 'nem a formula', 'manual'),
                                         *b56_sorok),
    }
    return alap_minirepo(sablonok=[_FEJ_TAGABB], tovabbi=tovabbi, jegyzek_sorok=jegyzek)


def _sor(szoveg, h=None):
    return (_MOTIVUM, h or OI.indok_hash(_INDOK), szoveg, 'scope=manual | forras=teszt | ts=2026-11-24', 'teszt')


class Tabla(unittest.TestCase):
    def _betolt(self, olvasoi_sorok, b56_sorok=()):
        repo = _repo(olvasoi_sorok, b56_sorok)
        self.addCleanup(repo.torol)
        b = Bemenet(repo.gyoker)
        return b, OI.b76_olvasoi_indoklasok(b, MotivumId(_MOTIVUM))

    def test_az_olvasoi_alak_all_a_lapon(self):
        _b, oi = self._betolt([_sor('Név nélküli hívás, a tágabb körbe tartozik.')])
        self.assertEqual(oi.lapra(_INDOK, 'Zsolt 1:1'), ('Név nélküli hívás, a tágabb körbe tartozik.', 'B76',
                                                          'olvasoi_indoklas'))

    def test_tiszta_indoklas_olvasoi_alak_nelkul_marad(self):
        _b, oi = self._betolt([])
        self.assertEqual(oi.lapra(_TISZTA, 'Zsolt 1:2'), (_TISZTA, 'B04', 'indoklas_kh'))

    def test_belso_szo_olvasoi_alak_nelkul_megall(self):
        _b, oi = self._betolt([])
        with self.assertRaisesRegex(BemenetHiba, 'nincs olvasói alakja'):
            oi.lapra(_INDOK, 'Zsolt 1:1')

    def test_arva_sor_hiba(self):
        with self.assertRaisesRegex(BemenetHiba, 'árva sor'):
            self._betolt([_sor('Tiszta mondat.', h='0123456789ab')])

    def test_belso_szo_az_olvasoi_alakban_hiba(self):
        with self.assertRaisesRegex(BemenetHiba, 'belső szót'):
            self._betolt([_sor('A hely a jelöltek közé került.')])

    def test_a_folerendelt_fogalom_mas_neve_hiba(self):
        with self.assertRaisesRegex(BemenetHiba, 'belső szót'):
            self._betolt([_sor('A hely a tágabb fogalomhoz tartozik.')])
        with self.assertRaisesRegex(BemenetHiba, 'olvasói neve a lapon'):
            self._betolt([_sor('A hely a tágabb csoportba tartozik.')])

    def test_b56_cimkeje_es_megjegyzese_a_kapu_alatt(self):
        b, _oi = self._betolt([], b56_sorok=[('2', '*', 'x', 'más ok', 'a fölérendelt fogalom felé', 'manual')])
        with self.assertRaisesRegex(BemenetHiba, 'B56.*megjegyzes'):
            dontes_be.b56_okok(b, MotivumId(_MOTIVUM))


class ValodiAdat(unittest.TestCase):
    def test_a_tabla_kapuja_a_valodi_adaton(self):
        b = Bemenet(kozos.GYOKER)
        for azonosito in kozos.MINTALAPOK:
            OI.b76_olvasoi_indoklasok(b, MotivumId(azonosito))
            dontes_be.b56_okok(b, MotivumId(azonosito))

    def test_egy_szolista(self):
        import olvasoi_kapu
        self.assertIs(olvasoi_kapu.MINTA_SZAKSZO, szokincs.SZAKSZO)

    def test_a_tagabb_nev_a_sablontablabol(self):
        b = Bemenet(kozos.GYOKER)
        mondat = next(r['mondat'] for r in b._tabla('B66').szotarak() if r['kulcs'] == 'fej.tagabb')
        self.assertEqual(szokincs.tagabb_nev(mondat), 'tágabb kör')
        self.assertIn(szokincs.tagabb_nev(mondat), szokincs.MASODIK_NEV)

    def test_a_tiltolista_szukitett(self):
        """D17 (1): a tiltólista csak a magyarázatlan belső eljárásra utaló szavakat tartja; a fölérendelt fogalom
        neve nem tiltott szó, hanem második név (D17 (2))."""
        self.assertNotIn('fölérendelt fogalom', szokincs.SZAKSZO)
        self.assertNotIn('invokáló szerkezet', szokincs.SZAKSZO)
        self.assertEqual(szokincs.talalatok('a lánc szava, a szónézet'), [])
        self.assertEqual(szokincs.talalatok('a fölérendelt fogalomhoz'), ['fölérendelt fogalom (a lapon: tágabb kör)'])

    def test_a_kereszthivatkozasos_sorok_a_3_es_a_6_szakaszban_ugyanazok(self):
        """A 3. szakasz kereszthivatkozásos csoportjai (TSK, Károli) pontosan a 6. szakasz Minősítésének elutasított
        és nyitott sorai: ezért áll a táblájuk egyszer, a 6. szakaszban (D15 (2))."""
        b = Bemenet(kozos.GYOKER)
        for azonosito in kozos.MINTALAPOK:
            m = MotivumId(azonosito)
            harmadik = sorted((s.igehely.kod, s.dontes.value) for s in vizsgalt_be.vizsgalt_sorok(b, m)
                              if s.csoport in (VizsgaltCsoport.TSK, VizsgaltCsoport.KAROLI))
            hatodik = sorted((j.igehely.kod, j.dontes.value) for j in kh_be.kereszthiv_jeloltek(b, m)
                             if j.dontes in (Dontes.ELUTASITVA, Dontes.NYITVA))
            self.assertEqual(harmadik, hatodik, azonosito)


if __name__ == '__main__':
    unittest.main()
