#!/usr/bin/env python
"""A Thayer-fordítássorok átkulcsolásának tesztjei (F186, DT-F186b; eszkozok/thayer_jelolt/forditas_atkulcsol.py).

Futtatás: python eszkozok/thayer_jelolt/teszt_forditas_atkulcsol.py  (szintetikus adat; a `Mai` osztály a mai táblákat olvassa)
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import forditas_atkulcsol as FA  # noqa: E402

FEJ = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forditas_hu', 'allapot', 'modell', 'datum',
       'terminologia_verzio', 'megjegyzes']


def sor(jsz, h, allapot='sonnet', strong='G0001', szotar='Thayer'):
    return '\t'.join([szotar, strong, 'G1', jsz, 'forditas_hu', h, 'ford ' + jsz, allapot, 'm', 'd', '', ''])


def adat(sorok):
    return [(i, dict(zip(FEJ, s.split('\t')))) for i, s in enumerate(sorok)]


# a mai szakaszok: a régi 2. bekezdés kettévált (sz2 = első rész, új szöveg; sz3 = második rész), a régi 3. → sz4
MAI = [{'sorszam': 1, 'hash': 'A'}, {'sorszam': 2, 'hash': 'B1'}, {'sorszam': 3, 'hash': 'B2'}, {'sorszam': 4, 'hash': 'C'}]
ELSO = {1: 1, 2: 2, 3: 4}


class Terv(unittest.TestCase):
    def setUp(self):
        self.sorok = [sor('sz1', 'A'), sor('sz2', 'B'), sor('sz3', 'C'), sor('sz1', 'X', strong='H0001', szotar='BDB')]

    def terv(self, sorok=None, mai=MAI, elso=ELSO):
        return FA.terv(adat(sorok or self.sorok), lambda sp: mai, lambda sp: elso)

    def test_atkulcsolas_csak_azonos_hashnel(self):
        v = {(x['regi'], x['tipus'], x['uj']) for x in self.terv()}
        # sz1 változatlan (azonos hash a helyén); sz3 (C) → sz4, mert a C hash ott van; sz2 (B) szövege változott → elavult
        self.assertEqual(v, {(3, 'atkulcsol', 4), (2, 'elavult', 2)})

    def test_nincs_atkulcsolas_eltero_hashnel(self):
        # a régi sz3 hash-e (C') sehol nincs a mai szakaszok között: nem kulcsolható át, elavult
        v = self.terv([sor('sz1', 'A'), sor('sz2', 'B'), sor('sz3', "C'")])
        self.assertEqual({(x['regi'], x['tipus']) for x in v}, {(2, 'elavult'), (3, 'elavult')})

    def test_tobbertelmu_hash_nem_kulcsol(self):
        mai = MAI + [{'sorszam': 5, 'hash': 'C'}]
        v = self.terv(mai=mai, elso={1: 1, 2: 2, 3: 4, 4: 5})
        self.assertEqual({(x['regi'], x['tipus']) for x in v}, {(2, 'elavult'), (3, 'elavult')})

    def test_kezi_sor_nem_lehet_elavult(self):
        with self.assertRaises(SystemExit):
            self.terv([sor('sz1', 'A'), sor('sz2', 'B', allapot='kezi')])

    def test_utkozes_megall(self):
        # két régi sor ugyanarra a kulcsra kerülne
        with self.assertRaises(SystemExit):
            self.terv([sor('sz2', 'B'), sor('sz4', 'B1')], elso={2: 2, 4: 4})

    def test_elavult_es_mas_szotar_kimarad(self):
        v = self.terv([sor('sz1', 'A'), sor('sz2', 'B', allapot='elavult'), sor('sz1', 'X', strong='H0001', szotar='BDB')])
        self.assertEqual(v, [])


# ELLENOR_F186_2 1–2.: a második kör. Az összevonás előtt 5 szakasz; a 3. és a 4. összevonódik (új 3., új hash „CD”), az 5. → 4.
MAI2 = [{'sorszam': 1, 'hash': 'A'}, {'sorszam': 2, 'hash': 'B'}, {'sorszam': 3, 'hash': 'CD'}, {'sorszam': 4, 'hash': 'E'}]
TERKEP2 = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4}


class Osszevonas(unittest.TestCase):
    def terv(self, sorok):
        return FA.terv_osszevonas(adat(sorok), lambda sp: MAI2, lambda sp: TERKEP2)

    def test_atkulcsolas_csak_azonos_hashnel_es_osszefuzes(self):
        v = {(x['regi'], x['uj'], x['tipus'], len(x['tagok'])) for x in
             self.terv([sor('sz1', 'A'), sor('sz2', 'B'), sor('sz3', 'C'), sor('sz4', 'D'), sor('sz5', 'E')])}
        # sz1, sz2 változatlan; a 3.+4. összefűzve egy elavult sorrá az új sz3-on; sz5 (azonos hash) → sz4
        self.assertEqual(v, {(3, 3, 'osszefuz', 1), (5, 4, 'atkulcsol', 0)})

    def test_eltero_hash_elavul_nem_kulcsol(self):
        v = {(x['regi'], x['tipus']) for x in self.terv([sor('sz1', 'A'), sor('sz5', 'X')])}
        self.assertEqual(v, {(5, 'elavult')})

    def test_elavult_sor_athelyezve(self):
        v = {(x['regi'], x['uj'], x['tipus']) for x in self.terv([sor('sz5', 'X', allapot='elavult')])}
        self.assertEqual(v, {(5, 4, 'athelyez')})

    def test_kezi_osszevont_megall(self):
        with self.assertRaises(SystemExit):
            self.terv([sor('sz3', 'C', allapot='kezi'), sor('sz4', 'D')])

    def test_iras_bajtorzo_es_idempotens(self):
        regi = ['\t'.join(FEJ), sor('sz1', 'A'), sor('sz3', 'C'), sor('sz4', 'D'), sor('sz5', 'E'),
                sor('sz9', 'Z', szotar='BDB', strong='H0002')]
        v = FA.terv_osszevonas([(i, dict(zip(FEJ, s.split('\t')))) for i, s in enumerate(regi) if i],
                               lambda sp: MAI2, lambda sp: TERKEP2)
        uj, torol = FA.alkalmaz_osszevonas(regi, FEJ, v, '2026.11.10')
        FA.ellenoriz_iras_osszevonas(regi, uj, v, torol)
        self.assertEqual(torol, {3})
        self.assertEqual((uj[0], uj[1], uj[4]), (regi[0], regi[1], regi[5]))
        m = dict(zip(FEJ, uj[2].split('\t')))
        self.assertEqual((m['jelentes_szam'], m['allapot'], m['forditas_hu']), ('sz3', 'elavult', 'ford sz3 ford sz4'))
        m = dict(zip(FEJ, uj[3].split('\t')))
        self.assertEqual((m['jelentes_szam'], m['allapot'], m['forras_hash']), ('sz4', 'sonnet', 'E'))
        # újrafuttatva: a már átkulcsolt Strong kimarad
        v2 = FA.terv_osszevonas([(i, dict(zip(FEJ, s.split('\t')))) for i, s in enumerate(uj) if i],
                                lambda sp: MAI2, lambda sp: TERKEP2)
        self.assertEqual(v2, [])


class Iras(unittest.TestCase):
    def test_bajtorzo(self):
        regi = ['# fejléc-megjegyzés', '\t'.join(FEJ), sor('sz1', 'A'), sor('sz2', 'B'), sor('sz3', 'C'),
                sor('sz9', 'Z', szotar='BDB', strong='H0002')]
        v = FA.terv([(i, dict(zip(FEJ, s.split('\t')))) for i, s in enumerate(regi) if i > 1], lambda sp: MAI, lambda sp: ELSO)
        uj = FA.alkalmaz(regi, FEJ, v, '2026.11.10')
        FA.ellenoriz_iras(regi, uj, v, FEJ)
        for i in (0, 1, 2, 5):
            self.assertEqual(regi[i], uj[i])
        m3 = dict(zip(FEJ, uj[3].split('\t')))
        self.assertEqual((m3['jelentes_szam'], m3['allapot'], m3['forras_hash']), ('sz2', 'elavult', 'B'))
        m4 = dict(zip(FEJ, uj[4].split('\t')))
        self.assertEqual((m4['jelentes_szam'], m4['allapot'], m4['forras_hash'], m4['forditas_hu']), ('sz4', 'sonnet', 'C', 'ford sz3'))
        self.assertIn('F186', m4['megjegyzes'])

    def test_varatlan_elteres_megall(self):
        regi = ['\t'.join(FEJ), sor('sz1', 'A')]
        with self.assertRaises(SystemExit):
            FA.ellenoriz_iras(regi, ['\t'.join(FEJ), sor('sz1', 'A2')], [], FEJ)


class Mai(unittest.TestCase):
    def test_ujrafuttatva_nincs_teendo(self):
        # a forditasok.tsv átkulcsolása után a mai táblákon a terv üres (idempotens)
        szoveg, sorok, fej, adat_ = FA.beolvas(FA.FORDITASOK_UT)
        import bont
        import thayer_bemenet as TB
        lex = bont.lexikon_beolvas()
        self.assertEqual(FA.terv(adat_, TB.szakaszok, lambda sp: FA.bekezdes_elso(sp, lex)), [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
