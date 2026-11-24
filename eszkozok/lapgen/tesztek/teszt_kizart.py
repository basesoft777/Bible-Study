"""A „3. Kizárt és vizsgált helyek” szakasz (S9a).

A HAMART-001 mai lapjával való egyezést (az engedélysorokkal) a regresszió méri; itt független számlálással: a
táblák sorai pontosan a döntésnapló elutasított és nyitva maradt előfordulás-jelöltjei, forráscsoportonként a
forrás-mező szerint (a teszt maga olvassa a táblát, `split('\t')`); a szakasz kapuja a modellen megáll, ha a számok
nem egyeznek; a „Negatív kritérium” bekezdés helyett utalás áll a lap eleji meghatározásra (DT872); a döntésnapló
belső szövege (az összesítő sor eleje, a szerkesztői döntés idézete, a forrás-mező) nem kerül a látható lapra.
"""
import dataclasses
import datetime
import os
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import bemenet, fo
from lapgen.bemenet import vizsgalt as vizsgalt_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import JelolesFajta, VizsgaltCsoport, VizsgaltJegyzetFajta
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import kizart as SZ
from lapgen.szoveg import Fajta, MotivumId

DATUM = datetime.date(2026, 11, 13)
_LAPOK = {}


def _lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM).nezetek['TUDOMANYOS']
    return _LAPOK[azonosito]


def _szakasz(azonosito):
    """A 3. szakasz sorai (látható szöveg és teljes szöveg párban)."""
    ki, bent = [], False
    for sor in _lap(azonosito):
        if sor.szoveg.startswith('## '):
            bent = sor.szoveg.startswith('## 3. ')
        if bent:
            lathato = ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f not in (MEGJEGYZES, Fajta.HORGONY))
            ki.append((lathato, sor.szoveg))
    return ki


def _jeloltek(azonosito):
    """A döntésnapló elutasított és nyitva maradt előfordulás-jelöltjei, a teszt saját olvasásával."""
    with open(os.path.join(kozos.GYOKER, 'adat', 'jeloltek.tsv'), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [r for r in (dict(zip(fej, s.split('\t'))) for s in sorok[1:])
            if r['id'] == azonosito and r['jelolt_tipus'] == 'elofordulas' and r['dontes'] in ('elutasítva', 'nyitva')]


def _csoport(forras):
    """A forráscsoport a forrás-mező elejéből (a teszt saját, egyszerű szabálya)."""
    fo_resz = forras.split(' | ')[0]
    if fo_resz.startswith(('TSK/Károli-KH', 'Károli-KH')):
        return VizsgaltCsoport.KAROLI
    if fo_resz.startswith('TSK'):
        return VizsgaltCsoport.TSK
    if fo_resz.startswith(('négyforrásos audit', 'tematikus:', 'napló:')):
        return VizsgaltCsoport.SZERKESZTOI
    return VizsgaltCsoport.KERESES


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


class Szamlalok(unittest.TestCase):
    def test_a_tablak_sorai_a_dontesnaplo_sorai_csoportonkent(self):
        """Forráscsoportonként a tábla döntésnapló-sorainak száma a teszt saját számlálása, mindkét mintalapon."""
        for azonosito in MINTALAPOK:
            modell = SZ.szamit(_Korny(azonosito))
            vart = {}
            for r in _jeloltek(azonosito):
                c = _csoport(r['forras_kereses'])
                vart[c] = vart.get(c, 0) + 1
            self.assertEqual({t.csoport: t.sorok_szama for t in modell.tablak}, vart, azonosito)
            self.assertEqual(modell.sorok_szama, len(_jeloltek(azonosito)), azonosito)

    def test_a_tablak_sorrendje_a_csoportok_rendje(self):
        for azonosito in MINTALAPOK:
            modell = SZ.szamit(_Korny(azonosito))
            rend = [t.csoport for t in modell.tablak]
            self.assertEqual(rend, [c for c in SZ.CSOPORT_REND if c in rend], azonosito)

    def test_kapu_a_modellen_megall(self):
        """A szakasz kapuja: az okok és a forráscsoportok versszám-összege a kizárt versek száma."""
        modell = SZ.kapu(SZ.szamit(_Korny('HAMART-001')))
        okok = list(modell.okok)
        okok[0] = dataclasses.replace(okok[0], versszam=okok[0].versszam + 1)
        with self.assertRaises(SZ.KapuHiba):
            SZ.kapu(dataclasses.replace(modell, okok=tuple(okok)))
        forrasok = list(modell.forrasok)
        forrasok[0] = (forrasok[0][0], forrasok[0][1] + 1)
        with self.assertRaises(SZ.KapuHiba):
            SZ.kapu(dataclasses.replace(modell, forrasok=tuple(forrasok)))

    def test_az_okok_tablaja_versszam_szerint(self):
        for azonosito in MINTALAPOK:
            modell = SZ.szamit(_Korny(azonosito))
            szamok = [o.versszam for o in modell.okok]
            self.assertEqual(szamok, sorted(szamok, reverse=True), azonosito)


class Jeloles(unittest.TestCase):
    def test_a_tsk_sornak_nincs_jegyzete(self):
        """A cellát ismétlő jegyzet nem áll (a régi `ismetlo_jegyzet`): a TSK-ajánlás és a csoportos sor jegyzet
        nélküli."""
        for azonosito in MINTALAPOK:
            for s in vizsgalt_be.vizsgalt_sorok(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito)):
                if s.csoport is VizsgaltCsoport.TSK or s.jeloles.csoport_versszam is not None:
                    self.assertIsNone(s.jegyzet, s.igehely.kod)

    def test_a_negyforrasos_ellenorzes_jegyzete_a_naplo(self):
        sorok = vizsgalt_be.vizsgalt_sorok(bemenet.Bemenet(kozos.GYOKER), MotivumId('HAMART-001'))
        audit = [s for s in sorok if s.jeloles.fajta is JelolesFajta.AUDIT]
        self.assertTrue(audit)
        self.assertTrue(all(s.jegyzet.fajta is VizsgaltJegyzetFajta.NAPLO for s in audit))

    def test_ismeretlen_jeloles_bukas(self):
        """A le nem képezett jelölési forrás BemenetHiba: a lap nem találgat."""
        b = bemenet.Bemenet(kozos.GYOKER)
        with self.assertRaises(BemenetHiba):
            vizsgalt_be._jeloles(b, 'ismeretlen keresés X', 'ismeretlen keresés X', None, 'Ter 1:1')


    def test_a_megszoritas_kulcs_a_nevtablabol(self):
        """DT926: a szókeresés megszorítása kulcs (nem kézi szöveg), a névtábla `kereses_megszoritas` típusában
        ismert; ismeretlen megszorításnál BemenetHiba."""
        from lapgen.szoveg import Kulcs
        b = bemenet.Bemenet(kozos.GYOKER)
        sorok = vizsgalt_be.vizsgalt_sorok(b, MotivumId('HAMART-001'))
        megszoritott = [s for s in sorok if s.jegyzet is not None and s.jegyzet.megszoritas is not None]
        self.assertEqual(len(megszoritott), 9)
        self.assertTrue(all(isinstance(s.jegyzet.megszoritas, Kulcs) for s in megszoritott))
        with self.assertRaises(BemenetHiba):
            vizsgalt_be._jeloles(b, 'scan: H7843 Piél-alakok', 'scan: H7843 Piél-alakok', None, 'Ter 1:1')


class Lap(unittest.TestCase):
    def test_ism_a_3_szakasz_utal_nem_ismetel(self):
        """DT872: a „3. Kizárt és vizsgált helyek” szakasz végi „Negatív kritérium” bekezdése helyett utalás áll a
        lap eleji meghatározásra, a szakasz elején (az okok táblája előtt)."""
        for azonosito in MINTALAPOK:
            sorok = _szakasz(azonosito)
            self.assertFalse(any(l.startswith('**Negatív kritérium:**') for l, _t in sorok), azonosito)
            utalas = [i for i, (_l, t) in enumerate(sorok) if '](#mi-tartozik-ide)' in t]
            okok = [i for i, (l, _t) in enumerate(sorok) if l.startswith('**Az elutasítás okai:**')]
            self.assertEqual(len(utalas), 1, azonosito)
            self.assertLess(utalas[0], okok[0], azonosito)

    def test_a_kereszthivatkozasos_tabla_egyszer_all(self):
        """D15 (2): a kereszthivatkozásból vizsgált sorok táblája a 6. szakasz Minősítésében áll; a 3. szakaszban
        nincs TSK- vagy Károli-csoporttábla, helyette egy mondat hivatkozik a 6. szakaszra."""
        for azonosito in MINTALAPOK:
            sorok = _szakasz(azonosito)
            self.assertFalse([l for l, _t in sorok if l.startswith(('**TSK-ajánlás**', '**Károli-kereszthivatkozás**'))],
                             azonosito)
            hivatkozo = [t for l, t in sorok if l.startswith('A kereszthivatkozásból vizsgált ')]
            self.assertEqual(len(hivatkozo), 1, azonosito)
            self.assertIn('](#6-kereszthivatkozások)', hivatkozo[0], azonosito)

    def test_nincs_belso_szoveg_a_lathato_lapon(self):
        """A döntésnapló belső jelölése nem kerül a látható szövegbe: az összesítő sor nyers eleje, a szerkesztői
        döntés munkaszereplője, a forrás-mező kulcsszavai."""
        # a „blokk-kizárás” szó egy HAMART-indoklás kézi szövegében áll (a mai lapon is, betűre): az S9 megfigyelése,
        # a 218a végi listában; ezért nincs a tiltottak között
        tiltott = ('Összesítő sor', 'felhasználó', 'blokk-sor', 'teljesség-mérés', 'scan', 'napló:', 'scope=', 'forras=',
                   'DT564', 'Gépi keresés', 'Kutatói felvetés')
        for azonosito in MINTALAPOK:
            for lathato, _teljes in _szakasz(azonosito):
                for szo in tiltott:
                    self.assertNotIn(szo, lathato, '%s: %s' % (azonosito, lathato[:120]))

    def test_a_jegyzetek_a_tabla_alatt_szamozva(self):
        """A jegyzet a tábla alá kerül, a szakaszon belül folyamatos számmal; minden hivatkozott szám alatta áll."""
        for azonosito in MINTALAPOK:
            hivatkozott, fej = set(), []
            for _l, teljes in _szakasz(azonosito):
                for resz in teljes.split('<sup class="lj"><a href="#j-3-')[1:]:
                    hivatkozott.add(int(resz.split('"')[0]))
                if teljes.startswith('- <span class="lj-szam" id="j-3-'):
                    fej.append(int(teljes.split('id="j-3-')[1].split('"')[0]))
            self.assertEqual(fej, list(range(1, len(fej) + 1)), azonosito)
            self.assertEqual(hivatkozott, set(fej), azonosito)


if __name__ == '__main__':
    unittest.main(verbosity=1)
