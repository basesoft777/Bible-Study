"""A lap kerete, első rész (S8a): a lap eleje, a Kivonat, a Tartalomjegyzék és a Jelmagyarázat.

A HAMART-001 mai lapjával való bájt-egyezést a regresszió méri (`regresszio.py`); itt a szerkezeti követelmények:
GK-10 (a szakaszszám és a horgony a szakaszrendből: a szakaszrend cseréje után sem keletkezik hibás belső link),
GK-A13 (a lap címe a motívumtábla mai címe), a lap eleji meghatározás horgonya (DT872), a Kivonat rése (a kézi forrás
változatlanul), és a Jelmagyarázat szakaszszámai.
"""
import datetime
import os
import re
import unittest

import kozos
from lapgen import bemenet, fo, konfig, szakaszok
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.nyelv import folerendelt_mondatkezdo
from lapgen.megjelenites.md import eleje as MD
from lapgen.megjelenites.md.iro import Lapiro
from lapgen.szamitas import eleje as SZ
from lapgen.szoveg import MotivumId, kiiras

HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'
_DATUM = datetime.date(2026, 11, 13)
_LINK_RX = re.compile(r'\]\(#([^)\s]+)\)')
_ID_RX = re.compile(r'id="([^"]+)"')
_CIM_RX = re.compile(r'^#{1,5} (.*)$')
_TILTOTT_RX = re.compile(r'[^\w\- ]')


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


def _keret(rend=None):
    b = bemenet.Bemenet(kozos.GYOKER)
    return fo.Keret(bemenet.nyelv(b), MotivumId(HAMART), rend or fo.szakaszrend(), 'ts=2026-11-13', fo.Mod.MUNKA, b)


def _horgonyok(sorok):
    """A lap belső célpontjai: a címsorok horgonya (a `cim_horgony` szabálya szerint) és az `id` attribútumok."""
    ki = set()
    for sor in sorok:
        m = _CIM_RX.match(sor)
        if m:
            ki.add(_TILTOTT_RX.sub('', m.group(1).lower()).strip().replace(' ', '-'))
        ki.update(_ID_RX.findall(sor))
    return ki


def _hibas_linkek(sorok):
    """A lap belső linkjei, amelyeknek nincs célpontja a lapon (a link szövegével együtt)."""
    celok = _horgonyok(sorok)
    return sorted({h for sor in sorok for h in _LINK_RX.findall(sor) if h not in celok})


def _lap(azonosito, friss=False):
    """A lap sorai; `friss`: a közös gyorsítótár nélkül (a szakaszrendet átíró teszt, GK-10)."""
    eredmeny = (fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM) if friss
                else kozos.lap_keszit(azonosito, _DATUM))
    return [s.szoveg for s in eredmeny.nezetek[konfig.NEZET_TUDOMANYOS]]


class LapEleje(unittest.TestCase):

    def test_gk_a13_a_cim_a_motivumtablabol(self):
        """GK-A13: a lap címsora a motívumtábla mai címe (a meglévő lap nem bemenet)."""
        for azonosito in kozos.MINTALAPOK:
            korny = _Korny(azonosito)
            m = SZ.szamit_fej(korny)
            self.assertEqual(kiiras(m.cim).szoveg, motivum_be.b02_motivum(korny.b, korny.motivum).cim.ertek)
            iro = Lapiro()
            MD.megjelenit_fej(iro, m, _keret(), None)
            cimsor = [s.szoveg for s in iro.kesz() if s.szoveg.startswith('# ')]
            self.assertEqual(len(cimsor), 1)
            self.assertTrue(cimsor[0].endswith(' — ' + kiiras(m.cim).szoveg), cimsor[0])

    def test_ism_a_lap_eleji_meghatarozas_horgonyt_kap(self):
        """DT872: a lap eleji meghatározás a `szakaszok.KRITERIUM_HORGONY` horgonyt kapja, a címe a `fej.hatar.cim`
        sablonsorból jön, a sorban a kritérium egészben áll; a lap eleje be van kötve, így a kritérium kapuja
        mindkét mintalap teljes lapján a „pontosan egyszer” módban fut (DT895)."""
        self.assertTrue(fo.szakaszrend().kesz(fo.FEJ))
        for azonosito in kozos.MINTALAPOK:
            lap = '\n'.join(_lap(azonosito))
            self.assertEqual(lap.count('id="%s"' % szakaszok.KRITERIUM_HORGONY.kod), 1, azonosito)
        korny = _Korny(HAMART)
        m = SZ.szamit_fej(korny)
        iro = Lapiro()
        MD.megjelenit_fej(iro, m, _keret(), None)
        sorok = [s.szoveg for s in iro.kesz()]
        horgonyos = [s for s in sorok if 'id="%s"' % szakaszok.KRITERIUM_HORGONY.kod in s]
        self.assertEqual(len(horgonyos), 1)
        self.assertIn('**Mi tartozik ide, és mi nem.** ' + kiiras(m.kriterium).szoveg, horgonyos[0])

    def test_a_tagabb_kor_mondatkezdo_alakja_adat(self):
        """A tágabb kör a lap elején mondatkezdő alakban áll; az alak a névtábla `folerendelt_mondatkezdo` sora
        (DT869 elve: a végleges alak az adatban), a mező kisbetűs alakja (a 4.12 bevezetője) változatlan. Kapu: az
        alak a mezőtől csak a kezdőbetűben térhet el."""
        b = bemenet.Bemenet(kozos.GYOKER)
        for azonosito in kozos.MINTALAPOK:
            sor = motivum_be.b02_motivum(b, MotivumId(azonosito))
            self.assertTrue(sor.folerendelt.ertek[0].islower())
            adat = folerendelt_mondatkezdo(b, MotivumId(azonosito), sor.folerendelt.ertek)
            self.assertIsNotNone(adat, azonosito)
            self.assertEqual(sor.folerendelt_mondatkezdo.ertek, adat.ertek)
            self.assertEqual(adat.ertek[1:], sor.folerendelt.ertek[1:])
        with self.assertRaises(bemenet.BemenetHiba):
            folerendelt_mondatkezdo(b, MotivumId(HAMART), 'a bűn és következményei általában, más szöveg')
        self.assertIsNone(folerendelt_mondatkezdo(b, MotivumId('NINCS-001'), 'x'))

    def test_hianyzo_kriterium_bukas(self):
        """GK-06: üres kritérium vagy tágabb kör a lap elején BUKÁS (kötelező elem)."""
        korny = _Korny(HAMART)
        eredeti = motivum_be.b02_motivum

        def ures(b, motivum):
            sor = eredeti(b, motivum)
            sor.kriterium = None
            return sor
        motivum_be.b02_motivum = ures
        try:
            with self.assertRaises(bemenet.BemenetHiba):
                SZ.szamit_fej(korny)
        finally:
            motivum_be.b02_motivum = eredeti


class Kivonat(unittest.TestCase):

    def test_a_kivonat_a_kezi_res_valtozatlanul(self):
        """A Kivonat a kézi forrás rése: soronként a jelölők közötti szöveg, a két szélső üres sor nélkül."""
        for azonosito in kozos.MINTALAPOK:
            res = motivum_be.kezi_res(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), SZ.RES_KIVONAT)
            with open(os.path.join(kozos.GYOKER, 'motivumok', '%s.md' % azonosito), encoding='utf-8') as f:
                forras = f.read()
            torzs = re.search(r'(?ms)^<!-- RÉS-KEZDET: kivonat -->\s*\n(.*?)^<!-- RÉS-VÉGE: kivonat -->',
                              forras).group(1).strip('\n')
            self.assertEqual('\n'.join(s.kezi.ertek if s.kezi is not None else '' for s in res.sorok), torzs)

    def test_ismeretlen_res_nincs(self):
        """A jegyzékben nem álló rés: None (az opcionális rés hiányát a hívó mondja ki)."""
        self.assertIsNone(motivum_be.kezi_res(bemenet.Bemenet(kozos.GYOKER), MotivumId(HAMART), 'nincs_ilyen_res'))


class Szakaszrend(unittest.TestCase):

    def test_tartalomjegyzek_a_szakaszrendbol(self):
        """A Tartalomjegyzék a nézet minden szakaszát sorolja (a lap elején, önmagán és az alrészeken kívül), a szakaszrend
        számával és horgonyával."""
        keret = _keret()
        elemek = MD.tartalom_elemek(keret)
        leirok = [l for l in keret.rend.mind() if l.nezet == konfig.NEZET_TUDOMANYOS
                  and l.azonosito not in MD.NEM_LISTAZOTT and not l.alresz]
        self.assertEqual(len(elemek), len(leirok))
        self.assertEqual(len(elemek), 15)

    def test_gk10_szakaszszam_es_horgony_a_modellbol(self):
        """GK-10: három pár számozott szakasz cseréje után (a 3↔4., az 5↔6. és a 7↔9.: a Szótári háttér és a
        Hatástörténet is mozog) a lapon nem keletkezik új hibás belső link, és a cserélt szakaszokra mutató linkek az
        új számot viselik. (A még el nem készült szakaszokra mutató link mindkét lapon hibás; ezek halmaza a
        szakaszszám nélkül nem változhat.)"""
        alap = _lap(HAMART)
        eredeti_rend = szakaszok._rend
        szakaszok._rend = _cserelt_rend
        try:
            uj = _lap(HAMART, friss=True)   # a cserélt szakaszrenddel: nem a gyorsítótárból
        finally:
            szakaszok._rend = eredeti_rend
        for elem in ('- [3. Szótári háttér](#3-szótári-háttér)', '- [5. Kereszthivatkozások](#5-kereszthivatkozások)',
                     '- [6. LXX-fordítói döntések](#6-lxx-fordítói-döntések)',
                     '- [7. Hatástörténet: ókori fordítások és értelmezők](#7-hatástörténet-ókori-fordítások-és-értelmezők)',
                     '- [9. Kapcsolatok](#9-kapcsolatok)'):
            self.assertIn(elem, uj)

        def szam_nelkul(linkek):
            return sorted(re.sub(r'^\d+-', '', h) for h in linkek)
        self.assertEqual(szam_nelkul(_hibas_linkek(uj)), szam_nelkul(_hibas_linkek(alap)))
        self.assertEqual(len(_hibas_linkek(uj)), len(_hibas_linkek(alap)))

    def test_jelmagyarazat_szakaszszamai_a_szakaszrendbol(self):
        """A Jelmagyarázat szakaszszámai (a szótári pontok, a 4.11 mutatója, a Hatástörténet) a szakaszrend számát
        viselik, látható szövegként is: az alaprenden (4 és 9) és a cserélt renden (3 és 7)."""
        for rend, s4, s9 in ((None, 4, 9), (_cserelt_szakaszrend(), 3, 7)):
            keret = _keret(rend)
            self.assertEqual((keret.rend.sorszam(MD.SZOCIKKEK), keret.rend.sorszam(MD.HATASTORTENET)), (s4, s9))
            iro = Lapiro()
            MD.megjelenit_jelmagyarazat(iro, SZ.Ures(), keret, fo._forrasok(keret.b, bemenet.b01_licencek(keret.b), ()))
            szoveg = '\n'.join(s.szoveg for s in iro.kesz())
            self.assertIn('**A szótári pontok** (%d. Szótári háttér)' % s4, szoveg)
            self.assertIn('%d.10 kiejtés (magyaros); %d.11 visszhang: ókori fordítások (a %d. szakaszban)'
                          % (s4, s4, s9), szoveg)
            self.assertIn('A %d.1–%d.10 nyelvenként, szavanként áll, a %d.11–%d.14 a motívum egészére vonatkozik.'
                          % (s4, s4, s4, s4), szoveg)
            self.assertIn('olvasatát a %d. szakasz mutatja' % s9, szoveg)
            self.assertIn('licenc: minden jog fenntartva', szoveg)


_CSEREK = (('kizart', 'szocikkek'), ('lxx', 'kereszthivatkozasok'), ('kapcsolatok', 'hatastortenet'))


def _cserelt_rend():
    """A szakaszrend három cserével (`_CSEREK`), újraszámozva: a `szakaszok._rend` helyére. Az alrész a szülőjével
    együtt mozog (a szakaszrend ellenőrzi a szomszédságot)."""
    eredeti = list(_EREDETI_REND())
    alreszek = {l.alresz: l for l in eredeti if l.alresz is not None}
    rend = [l for l in eredeti if l.alresz is None]
    for a, b in _CSEREK:
        i = next(k for k, l in enumerate(rend) if l.azonosito == a)
        j = next(k for k, l in enumerate(rend) if l.azonosito == b)
        rend[i], rend[j] = rend[j], rend[i]
    for szulo, alresz in alreszek.items():
        rend.insert(next(k for k, l in enumerate(rend) if l.azonosito == szulo) + 1, alresz)
    szam = 0
    for leiro in rend:
        leiro.sorszam = None
        if leiro.szamozott:
            szam += 1
            leiro.sorszam = szam
    return tuple(rend)


_EREDETI_REND = szakaszok._rend


def _cserelt_szakaszrend():
    eredeti = szakaszok._rend
    szakaszok._rend = _cserelt_rend
    try:
        return fo.szakaszrend()
    finally:
        szakaszok._rend = eredeti


if __name__ == '__main__':
    unittest.main()
