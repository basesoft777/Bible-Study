"""A HAMART-001 kritériumának formai átírása (DT-F218n, kézi tételek; az orkesztrátor döntése a felhasználó
felhatalmazásával, 2026-11-13): a kritérium 2–3 mondatra tagolódott, a zárójeles magyar szólista kimaradt, a
megnevezés egységes („fájdalom és fáradság”), az újszövetségi mérce a „Károli alapszövege” szavakkal áll. **A feltételek
nem változhatnak**: a régi és az új szöveg ugyanazt a Strong-, szópár- és kizárás-halmazt adja.

A halmazok a szövegből, szerkezetileg jönnek: a „Nem tartozik ide” előtti rész zárójeleiből az eredeti nyelvű szavak
(a héber szó kiejtése, a görög szó alakja), a pontosvesszős zárójelből a szópárok, a „Nem tartozik ide” utáni
zárójelből a kizárások. A Strong-szám a szótári alakból és a kiejtésből jön (`Kiejtes.szotari`, a lánc szavain): a
halmaz így nem a szöveg szavain, hanem a mögöttük álló szótári szavakon egyezik.

A Kivonat a kritériumot nem mondja újra (a 9-es sablon v2.3 szabálya): a kézi forrás Kivonat-résében a kritérium
egyetlen 12 szavas részlete sem áll. Ez a teljes lap kapujának (`lapgen.ismetles`) előőre, a Kivonat szeletéig (S8).
"""
import os
import re
import unicodedata
import unittest

import kozos
from lapgen import bemenet, ismetles, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.szoveg import MotivumId, Strong

HAMART = MotivumId('HAMART-001')

# A kritérium a DT-F218n kézi tételei előtt (adat/motivumok.tsv, HAMART-001, `negativ_kriterium`; a 6b935da5 commit
# szövege). Csak összevetési minta: a lapra nem kerül.
REGI_KRITERIUM = (
    'A versben az 1Mózes 3–9. fejezetének szóláncából (átok, föld, fáradság, bűn, erőszak, romlás) egy szó áll — '
    'héberül az átok (árar), a föld (adámá), a fájdalom és fáradság (iccávón), a bűn (chattát), az erőszak (chámász) '
    'vagy a romlás igéje (sáchat); görögül az átkozott (ἐπικατάρατος, epikataratosz), az átok (κατάρα, katara) vagy a '
    'romlás szócsaládja (φθείρω, ftheiró) —, vagy a lánc szópárja (tövis és bogáncs; megtelt erőszakkal), vagy az '
    'erőszak szava a hallás igéjével ugyanabban a versben, és a hely ezen a szón át az 1Móz 3–9 láncára utal vissza: '
    'az átkot a földön, a föld romlását, az erőszakkal megtelt földet vagy a föld színéről való eltörlést mondja ki, '
    'ismétli vagy fordítja meg. Nem tartozik ide a hely, amelyben a szó általános használatban áll (bűnáldozat, föld '
    'mint ország vagy talaj, katonai pusztítás, rituális vagy emberi átkozódás, az erőszak a megtelés és a hallás szava '
    'nélkül, romlandó test), és az sem, amely az átkot vagy a föld elvesztését a szövetség rendjében, a szövetség '
    'megszegésének büntetéseként mondja ki. A lánc szavai nélkül csak az a néhány hely tartozik ide, amely ugyanezt a '
    'szerkezetet más szavakkal mondja ki; ezeket a vizsgálat egyenként, tematikus helyként veszi fel. Az újszövetségi '
    'helyeknél a Textus Receptus a mérce.')

_ZAROJEL = re.compile(r'\(([^()]*)\)')
_GOROG = re.compile(r'[Ͱ-Ͽἀ-῿]')
_ERŐSZAK_HALLAS = re.compile(r'az erőszak szava a hallás igéjével ugyanabban a versben')
_SZOVETSEG = re.compile(r'az átkot vagy a föld elvesztését a szövetség rendjében, a szövetség megszegésének '
                        r'büntetéseként mondja ki')
_LANC = re.compile(r'\baz? (\S+) (\d+)[–-](\d+)\.? láncára\b')   # a régi generátor `_LANC_MAG_RE` mintája
_NEM = 'Nem tartozik ide'


def _nfc(szoveg):
    return unicodedata.normalize('NFC', szoveg)


def _szotar():
    """{kiejtés vagy görög alak: Strong} a motívum lánc-szavain (a hordozó elemek Strong-részei), a szótári alak és a
    kiejtés a motívum versei szerint (ugyanaz az út, mint az 1.2 pontban)."""
    b = bemenet.Bemenet(kozos.GYOKER)
    sorok = list(bemenet.b03_elofordulasok(b, HAMART))
    karoli = bemenet.b07_karoli(b)
    versek = tuple(v for s in sorok for v in karoli.versek(s.igehely))
    kiejtes = szavak_be.kiejtes(b)
    terkep = {}
    for s in sorok:
        for resz in s.gerinc_reszek:
            if isinstance(resz, Strong):
                szo = kiejtes.szotari(resz, versek)
                if szo is None:
                    continue
                terkep[_nfc(szo.alak.ertek)] = resz.kod
                if szo.kiejtes is not None:
                    terkep[_nfc(szo.kiejtes.ertek)] = resz.kod
    return terkep


def elemek(szoveg, szotar):
    """(Strong-halmaz, szópár-halmaz, kizárás-halmaz, ismeretlen zárójeles eredeti szavak) a kritérium szövegéből."""
    ide, _sep, nem = szoveg.partition(_NEM)
    strongok, szoparok, ismeretlen = set(), set(), set()
    for zarojel in _ZAROJEL.findall(ide):
        if ';' in zarojel:
            szoparok.update(resz.strip() for resz in zarojel.split(';'))
            continue
        tagok = [t.strip() for t in zarojel.split(',')]
        eredeti = [t for t in tagok if _GOROG.search(t)] or (tagok if len(tagok) == 1 else [])
        for t in eredeti:
            if _nfc(t) in szotar:
                strongok.add(szotar[_nfc(t)])
            elif _GOROG.search(t) or ' ' not in t:
                ismeretlen.add(t)
    if _ERŐSZAK_HALLAS.search(ide):
        szoparok.add('erőszak + hallás')
    kizarasok = set()
    for zarojel in _ZAROJEL.findall(nem):
        kizarasok.update(t.strip() for t in zarojel.split(','))
    if _SZOVETSEG.search(nem):
        kizarasok.add('a szövetség rendje')
    return strongok, szoparok, kizarasok, ismeretlen


class KriteriumFormaiAtirasa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.szotar = _szotar()
        cls.mai = motivum_be.kriterium_szoveg(bemenet.Bemenet(kozos.GYOKER), HAMART)

    def test_a_regi_mintabol_a_halmazok_ki_is_jonnek(self):
        """Az összevetés nem üres halmazokon áll: a régi szövegből kilenc szótári szó, három szópár-elem és hét
        kizárás jön ki, és nincs a lánc szavai között ismeretlen eredeti nyelvű szó."""
        strongok, szoparok, kizarasok, ismeretlen = elemek(REGI_KRITERIUM, self.szotar)
        self.assertEqual(strongok, {'H0779', 'H0127', 'H6093', 'H2403', 'H2555', 'H7843', 'G1944', 'G2671', 'G5351'})
        self.assertEqual(szoparok, {'tövis és bogáncs', 'megtelt erőszakkal', 'erőszak + hallás'})
        self.assertEqual(len(kizarasok), 7)
        self.assertIn('a szövetség rendje', kizarasok)
        self.assertEqual(ismeretlen, set())

    def test_a_feltetelek_nem_valtoztak(self):
        """A mai kritérium ugyanazt a Strong-, szópár- és kizárás-halmazt adja, mint a régi."""
        regi = elemek(REGI_KRITERIUM, self.szotar)
        mai = elemek(self.mai, self.szotar)
        self.assertEqual(mai[0], regi[0], 'a Strong-halmaz változott')
        self.assertEqual(mai[1], regi[1], 'a szópár-halmaz változott')
        self.assertEqual(mai[2], regi[2], 'a kizárás-halmaz változott')
        self.assertEqual(mai[3], set())

    def test_a_lanc_es_a_merce_megmaradt(self):
        """A lánc megnevezése (a régi generátor Pesat-gerince ebből jön: `lanc_mag`) és a tematikus helyek mondata
        változatlan; az újszövetségi mérce a Károli alapszövegével áll."""
        self.assertEqual(_LANC.search(self.mai).groups(), _LANC.search(REGI_KRITERIUM).groups())
        self.assertIn('A lánc szavai nélkül csak az a néhány hely tartozik ide, amely ugyanezt a szerkezetet más '
                      'szavakkal mondja ki; ezeket a vizsgálat egyenként, tematikus helyként veszi fel.', self.mai)
        self.assertIn('Az újszövetségi helyeknél a Károli alapszövege, a Textus Receptus a mérce.', self.mai)

    def test_a_forma(self):
        """Nincs zárójeles magyar szólista, a megnevezés egységes, és a „Nem tartozik ide” előtti rész 2–3 mondat."""
        self.assertNotIn('(átok, föld, fáradság, bűn, erőszak, romlás)', self.mai)
        ide = self.mai.partition(_NEM)[0]
        self.assertNotRegex(ide, r'(?<!fájdalom és )fáradság')
        mondatok = [m for m in re.split(r'(?<=[.])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ])', ide.strip()) if m]
        self.assertIn(len(mondatok), (2, 3))


class AKivonatNemIsmetel(unittest.TestCase):
    def test_a_kivonatban_nincs_kriterium_reszlet(self):
        """A kézi forrás Kivonat-résében a kritérium egyetlen 12 szavas részlete sem áll (a 9-es sablon v2.3
        „Egy szabály, egy teljes hely” szabálya; a DT-F218n 1., 3., 5. és 7. kézi tétele)."""
        with open(os.path.join(kozos.GYOKER, 'motivumok', 'HAMART-001.md'), encoding='utf-8') as f:
            forras = f.read()
        kivonat = forras.split('<!-- RÉS-KEZDET: kivonat -->')[1].split('<!-- RÉS-VÉGE: kivonat -->')[0]
        kriterium = motivum_be.kriterium_szoveg(bemenet.Bemenet(kozos.GYOKER), HAMART)
        k = [sz.alak for sz in ismetles.szavak(kriterium)]
        ablak = konfig.KRITERIUM_ABLAK
        keresett = {tuple(k[i:i + ablak]) for i in range(len(k) - ablak + 1)}
        talalt = []
        for bekezdes in kivonat.split('\n'):
            w = [sz.alak for sz in ismetles.szavak(bekezdes)]
            talalt.extend(' '.join(w[i:i + ablak]) for i in range(len(w) - ablak + 1)
                          if tuple(w[i:i + ablak]) in keresett)
        self.assertEqual(talalt, [])

    def test_a_regi_kivonaton_a_proba_megfogna(self):
        """A próba él: a DT-F218n előtti Kivonat-mondat (a kritérium szűkített másolata) a régi kritériummal 12 szavas
        egyezést ad."""
        regi_mondat = ('vagy az erőszak szava a hallás igéjével ugyanabban a versben, és a hely ezen a szón át az '
                       '1Mózes 3–9. fejezetének láncára utal vissza: az átkot a földön, a föld romlását, az '
                       'erőszakkal megtelt földet vagy a föld színéről való eltörlést mondja ki')
        k = [sz.alak for sz in ismetles.szavak(REGI_KRITERIUM)]
        ablak = konfig.KRITERIUM_ABLAK
        keresett = {tuple(k[i:i + ablak]) for i in range(len(k) - ablak + 1)}
        w = [sz.alak for sz in ismetles.szavak(regi_mondat)]
        self.assertTrue(any(tuple(w[i:i + ablak]) in keresett for i in range(len(w) - ablak + 1)))


if __name__ == '__main__':
    unittest.main()
