#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_36.py -- az ellenoriz.py 36. szabályának tesztjei (F123.HAMART3): egy vers ugyanannál a
motívumnál nem lehet egyszerre előfordulás és egy csoportos kizárás (összesítő jelöltsor) tagja. Ideiglenes (a repón
kívüli) adat- és napló-könyvtárban fut; a valódi táblán a szabály RENDBEN.
    python eszkozok/teszt_ellenoriz_36.py
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
        'lista: naplok/F123_teljesseg_PROBA-001_blokkok.tsv (halo=strong, blokk=H0127) | scope=manual')


class Szabaly36(unittest.TestCase):
    def setUp(self):
        self.gy = tempfile.mkdtemp(prefix='teszt36_')
        self.adat = os.path.join(self.gy, 'adat')
        os.makedirs(self.adat)
        os.makedirs(os.path.join(self.gy, 'naplok'))

    def tearDown(self):
        shutil.rmtree(self.gy, ignore_errors=True)

    def ir(self, elo_helyek, tagok):
        with open(os.path.join(self.adat, 'elofordulasok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tigehely\n' + ''.join('PROBA-001\t%s\n' % h for h in elo_helyek))
        d = dict.fromkeys(JFEJ, '')
        d.update(id='PROBA-001', igehely='1Kir 7:46', forras_kereses=CSOP, dontes='elutasítva',
                 indoklas='Összesítő sor 2 versre (az első itt áll): a szó általános használatban áll.')
        with open(os.path.join(self.adat, 'jeloltek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\t'.join(JFEJ) + '\n' + '\t'.join(d[k] for k in JFEJ) + '\n')
        with open(os.path.join(self.gy, 'naplok', 'F123_teljesseg_PROBA-001_blokkok.tsv'), 'w', encoding='utf-8',
                  newline='\n') as f:
            f.write('halo\tblokk\tigehely\tgerinc_a_versben\n' + ''.join('strong\tH0127\t%s\tigen\n' % t for t in tagok))

    def test_utkozes_sertes(self):
        self.ir(['1Móz 7:3-4'], ['1Kir 7:46', '1Móz 7:4'])
        s = E.szabaly36_csoport_elofordulas(self.adat)
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('PROBA-001 1Móz 7:4', ' '.join(s.peldak))

    def test_nincs_utkozes(self):
        self.ir(['1Móz 7:23'], ['1Kir 7:46', '1Móz 7:4'])
        self.assertEqual(E.szabaly36_csoport_elofordulas(self.adat).verdict, 'RENDBEN')

    def test_valodi_tabla(self):
        self.assertEqual(E.szabaly36_csoport_elofordulas(os.path.join(GYOKER, 'adat')).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main()
