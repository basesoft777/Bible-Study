"""Tesztváz (F218.3): a brief 7. pontjának még meg nem írt követelményei, név + docstring + `skip` alakban.

A teszt törzse azzal a szelettel íródik meg, amelyik a követelményt teljesíti; akkor a függvény innen a szelet
tesztfájljába költözik. A `skip` oka megnevezi a szeletet. A 218b/218c-re tartozó követelmények nincsenek itt.
"""
import datetime
import re
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import fo
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szoveg import Fajta, MotivumId

S2, S3, S4, S5, S6, S7, S8, S9 = ('S2 (F218.5)', 'S3 (F218.6)', 'S4 (F218.7)', 'S5 (F218.8)', 'S6 (F218.9)',
                                  'S7 (F218.10)', 'S8 (F218.11)', 'S9 (F218.12)')
# a T6 mondata (a párosítás mért pontossága egyszer, a Módszertanban) nyitott, döntéssel elhalasztva: a
# felhasználó 2026-11-21-én „Később, a validáció után”; a JOHD-validáció után, a validált számmal (N-F218v)
S8_GK19 = ('GK-19 (T6): nyitott, döntéssel elhalasztva (2026-11-21, „Később, a validáció után”; N-F218v); '
           'a mondat a JOHD-validáció után kerül a lapra')
HELY_EGYSEG = ('218c (a leendő #238; N234, az orkesztrátor döntése (DT924), 2026-11-22): a névvel megadott szópár (1.4, '
               '`málé+chámász`) tagjait a modell nem köti Strong-számhoz; a kapu '
               'ehhez a bemeneti rétegben kér feloldást (N-tétel)')


# A hibanapló példányainak szövegmintái (brief 7.3): HN → [(minta, lapszöveg-részlet a hibás lapról)]. A részlet a
# mintára BUKÁS-t ad (a minta megfogja); az új lap látható szövegén az elvárt találatszám 0. A minták forrása az
# alapmérés táblája (`naplok/F218_jelentes.md` „F218.1 — alapmérés”).
HN_MINTAK = {
    'HN-02': [(r'A formula nincs a versben: Nincs meg a formula',
               'A formula nincs a versben: Nincs meg a formula a versben, a szó önállóan áll')],
    # HN-03 (DT925 (2) (a), S9c): a forrásnév a mondat közepén, zárójelben; a zárójel után a sorban még szöveg áll
    # (a sor végén álló zárójel, pl. a 12. szakasz forrásjegyzékének „(forrásnév, licenc)” megjegyzése, nem mondatközi)
    'HN-03': [(r'(?m)\((?:a|az|A|Az) [^()\n]*(?:BDB|Thayer|TBESG|TBESH|STEPBible|MCGED|SDBH|LSJ|SECE)[^()\n]*szótár'
               r'[^()\n]*\)(?![ \t]*$)',
               'a szó jelentése (a BDB-szótár szerint) a megművelt föld')],
    'HN-04': [(r'hivatkozas_kezi|negativ_kriterium|szerkesztő-chat|\bkollokacio\b',
               'a javítás forrása: hivatkozas_kezi,; kollokacio … szerkesztő-chat … negativ_kriterium')],
    'HN-05': [(r'felhasználó|orkesztrátor', 'a felhasználó döntése szerint'),
              (r'felhasználó|orkesztrátor', 'az orkesztrátor jóváhagyta')],
    'HN-06': [(r'\bgerinc', 'a motívum gerince a héber szó')],
    'HN-07': [(r'\bsz\d+ sorok', 'a Thayer-fordításból (a 4. kör, sz12 sorok,; kézi)')],
    'HN-08': [(r'\bDT-?F?\d+', 'a jelentés és a funkció szétválasztása (F131, DT272 (d))'),
              (r'(?<![\w&/])#\d{2,3}\b', 'a #142 tétel szerint'),
              (r'\bN\d+\b', 'nyitott kérdés: N59'),
              (r'\(G\d{1,3}\)', 'a generátor szabálya (G10)'),
              (r'\bF\d{2,3}\b', 'a címketábla (F131) szerint')],
    'HN-09': [(r'\bH\d{4}\. [a-z]', 'H7121. qara קָרָא hív, kiált'),
              (r'[\u0590-\u05FF]_\d{2,4}\b', 'אָדָם_560 hímnemű főnév')],
    'HN-10': [(r'Karoli_kereszthivatkozasok\.tsv', 'forrás: konkordancia/Karoli_kereszthivatkozasok.tsv')],
    'HN-15': [(r'magyar rövid glossza-tábla a görögre még nincs',
               'A magyar rövid glossza-tábla a görögre még nincs meg.')],
}
# Az új lap kész szakaszain már ma mért esetek (a HN-03 az S9c óta, DT925 (2) (a)).
HN_MERT = ('HN-02', 'HN-03', 'HN-04', 'HN-05', 'HN-06', 'HN-07', 'HN-08', 'HN-09', 'HN-10', 'HN-15')
_DATUM = datetime.date(2026, 11, 13)


def _lathato_szoveg(azonosito):
    """A mintalap kész szakaszainak látható szövege (a megjegyzések és a link-célpontok nélkül: a horgony a
    Markdown-link célja, az olvasó nem látja; a Tartalomjegyzék „#10-értelmezés” horgonya nem tételszám), nézetenként
    összefűzve."""
    eredmeny = kozos.lap_keszit(azonosito, _DATUM)
    return '\n'.join(''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f not in (MEGJEGYZES, Fajta.HORGONY))
                     for sorok in eredmeny.nezetek.values() for sor in sorok)


class HibanaploMintak(unittest.TestCase):
    def test_a_mintak_megfogjak_a_hibas_lapszoveget(self):
        """Minden HN-minta BUKÁS-t ad a hibás lapról vett szövegrészleten (a minta él, nem üres)."""
        for hn, mintak in HN_MINTAK.items():
            for minta, reszlet in mintak:
                self.assertTrue(re.search(minta, reszlet), '%s: %s' % (hn, minta))

    def test_a_kesz_szakaszokon_nincs_hn_talalat(self):
        """Az új lap kész szakaszainak látható szövegén a már mért HN-esetek száma 0, mindkét mintalapon
        (szeletenként bővül: a lap a kész szakaszokkal nő)."""
        for azonosito in MINTALAPOK:
            szoveg = _lathato_szoveg(azonosito)
            talalatok = [(hn, m.group(0)) for hn in HN_MERT for minta, _reszlet in HN_MINTAK[hn]
                         for m in re.finditer(minta, szoveg)]
            self.assertEqual(talalatok, [], azonosito)


class Szerkezeti(unittest.TestCase):
    @unittest.skip(HELY_EGYSEG)
    def test_gk04_hely_egyseg_kapu(self):
        """GK-04, a `hely_egyseg` része (a régi `hely_egyseg_kapu`, F212 Sz4): a szavanként az 1.4 csoportjainak
        helyszáma (szópárban is) és az Áttekintés „Helyek a motívumban” oszlopa egyezik, a modellen, mindkét mintalapon.
        Az `lxx_egyezes` része kész (`teszt_lxx.py` `Gk04`)."""


    @unittest.skip(S8_GK19)
    def test_gk19_karoli_parositas(self):
        """GK-19 (T6): a párosítás mért pontossága egyszer, a Módszertanban áll, a konfigból. (A másik két fele
        kész: minden pár számít, és a 4.13–4.14 látható szövegében nincs bizonyossági címke és páronkénti jelölés:
        `teszt_szotari_karoli.py`.)"""


if __name__ == '__main__':
    unittest.main(verbosity=1)
