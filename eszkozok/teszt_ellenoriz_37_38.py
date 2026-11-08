#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_37_38.py -- az ellenoriz.py 37. és 38. szabályának tesztjei (F123.HAMART3 javítókör,
2026-11-08): (37) a beépített sor indoklása nem illik a motívum saját csoportos kizárási okára; (38) strukturális vagy
fogalmi hordozón a beépítés nem „csak e szó miatt”. Ideiglenes (a repón kívüli) adatkönyvtárban fut; a valódi táblán
mindkét szabály RENDBEN.
    python eszkozok/teszt_ellenoriz_37_38.py
"""
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ellenoriz as E  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JFEJ = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'karoli_szo', 'azonositas_modja', 'megbizhatosag',
        'datum', 'jelolt_tipus', 'cel_id', 'cel_igehely', 'cel_alpont', 'dontes_ref']
CSOP = ('F123 U1 teljesség-mérés, Strong-háló, blokk-sor (DT564 minta): 2 vers, a sor igehelye a blokk egy verse; a '
        'lista: naplok/F123_teljesseg_PROBA-001_blokkok.tsv (halo=strong, blokk=H0779) | scope=manual')


def sor(**kw):
    d = dict.fromkeys(JFEJ, '')
    d.update(id='PROBA-001', jelolt_tipus='elofordulas', **kw)
    return '\t'.join(d[k] for k in JFEJ)


class Alap(unittest.TestCase):
    def setUp(self):
        self.gy = tempfile.mkdtemp(prefix='teszt3738_')
        self.adat = os.path.join(self.gy, 'adat')
        os.makedirs(self.adat)

    def tearDown(self):
        shutil.rmtree(self.gy, ignore_errors=True)

    def ir(self, jelolt_sorok, tipus='strukturális', elo=None):
        with open(os.path.join(self.adat, 'jeloltek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\t'.join(JFEJ) + '\n' + '\n'.join(jelolt_sorok) + '\n')
        with open(os.path.join(self.adat, 'elutasitasi_okok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('sorrend\tid\tminta\tcimke\tmegjegyzes\tproveniencia\n'
                    '113\tPROBA-001\temberi átkozódás\temberi átkozódás, nem a lánc\tx\tscope=manual\n'
                    '119\tPROBA-001\tchámász\taz erőszak szava más használatban\tx\tscope=manual\n')
        with open(os.path.join(self.adat, 'motivumok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tazonossag_tipusa\nPROBA-001\t%s\n' % tipus)
        with open(os.path.join(self.adat, 'elofordulasok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tigehely\tgerinc_elem\n' + ''.join('PROBA-001\t%s\t%s\n' % x for x in (elo or [])))


class Szabaly37(Alap):
    CSOPORTOS = sor(igehely='1Kir 7:46', forras_kereses=CSOP, dontes='elutasítva',
                    indoklas='Összesítő sor 2 versre: emberi átkozódás, a lánc nélkül.')

    def test_csoportos_okra_illo_beepites_sertes(self):
        self.ir([self.CSOPORTOS, sor(igehely='1Móz 9:25', dontes='beépítve',
                                     indoklas='emberi átkozódás egy leszármazottra, mégis a lánc folytatása')])
        s = E.szabaly37_beepitett_csoportos_ok(self.adat)
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('PROBA-001 1Móz 9:25', ' '.join(s.peldak))

    def test_egyenkenti_ok_nem_csoportos(self):
        # a chámász-ok csak egyenkénti sorban áll: a beépített sor szava nem ütközik vele
        self.ir([self.CSOPORTOS, sor(igehely='Zsolt 1:1', dontes='elutasítva', indoklas='chámász általános használatban'),
                 sor(igehely='Ez 7:23', dontes='beépítve', indoklas='a chámász a „megtelt” igével, a kollokáció')])
        self.assertEqual(E.szabaly37_beepitett_csoportos_ok(self.adat).verdict, 'RENDBEN')

    def test_valodi_tabla(self):
        self.assertEqual(E.szabaly37_beepitett_csoportos_ok(os.path.join(GYOKER, 'adat')).verdict, 'RENDBEN')


class Szabaly38(Alap):
    def test_csak_szoegyezes_sertes(self):
        self.ir([sor(igehely='Gal 3:10', dontes='beépítve', indoklas='a görög Ószövetség ugyanazt a szót használja')])
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'SÉRTÉS')

    def test_mondat_eleji_nagybetu(self):
        self.ir([sor(igehely='Jer 2:2', dontes='beépítve', indoklas='Ugyanaz az ige áll, mint a Genezisben.')])
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'SÉRTÉS')

    def test_kifejezett_csak_e_szo_miatt(self):
        self.ir([sor(igehely='Jer 1:1', dontes='beépítve', indoklas='csak e szó miatt áll itt, a lánc visszhangja')])
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'SÉRTÉS')

    def test_szerkezeti_jeggyel_rendben(self):
        self.ir([sor(igehely='1Móz 6:17', dontes='beépítve',
                     indoklas='ugyanaz az ige, mint a 6:12-ben: a tükörítélet szerkezete')])
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'RENDBEN')

    def test_lexikai_hordozon_nem_fut(self):
        self.ir([sor(igehely='Gal 3:10', dontes='beépítve', indoklas='ugyanazt a szót használja')], tipus='lexikai')
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'RENDBEN')

    def test_tematikus_sor_kimarad(self):
        self.ir([sor(igehely='Jel 22:3', dontes='beépítve', indoklas='ugyanaz a szó')],
                elo=[('Jel 22:3', 'tematikus:1Móz 3:17')])
        self.assertEqual(E.szabaly38_csak_szo(self.adat).verdict, 'RENDBEN')

    def test_valodi_tabla(self):
        self.assertEqual(E.szabaly38_csak_szo(os.path.join(GYOKER, 'adat')).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main()
