#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A bekötés-összevetés (bekotesi_leltar.py --osszevet) logikájának tesztje: ami az alapon látszott, az az ágon is látsszon.

Szintetikus alap- és ág-állapotokkal fut (adatbázis, git és Flask nélkül), így a gyors sorban mindig lefut. A valódi összevetést a push előtti
kapu (`push_elott.py`) futtatja a helyi `pardes.db`-n és a `git merge-base origin/main HEAD` alapján.
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import bekotesi_leltar as B  # noqa: E402


def blokk(id_, nezet='szó', latszik=True, jegyzet=(), hely='szó-panel'):
    return {'id': id_, 'nezet': nezet, 'latszik': latszik, 'jegyzet': list(jegyzet), 'hely': hely}


def allapot(blokkok, tablak):
    """blokkok: [blokk]; tablak: {tábla: {nézet: [blokk-azonosító]}}; egy adatkészlet (X) az összes táblával."""
    by = {b['id']: b for b in blokkok}
    L = {'blokkok': blokkok, 'tablak': []}
    for t, nez in tablak.items():
        L['tablak'].append({'tabla': t, 'tokenek': ['X'], 'nezetek': {n: [by[i] for i in ids] for n, ids in nez.items()}})
    ds = [('X', {'tablak': L['tablak']})]
    return B.latszo(L, ds)


ALAP_B = [blokk('szo.a'), blokk('szo.b'), blokk('vers.c', 'vers', hely='Vers fül')]
ALAP_T = {'t1': {'szó': ['szo.a']}, 't2': {'szó': ['szo.b']}, 't3': {'vers': ['vers.c']}}


class TesztOsszevet(unittest.TestCase):
    def hibak(self, ag_b, ag_t, kiv=()):
        el = B.osszevet(allapot(ALAP_B, ALAP_T), allapot(ag_b, ag_t))
        return el, B.kivetel_szerint(el, list(kiv))

    def test_valtozatlan_nincs_elteres(self):
        el, (hibak, _) = self.hibak(ALAP_B, ALAP_T)
        self.assertEqual((el, hibak), ([], []))

    def test_javulas_nem_hiba(self):
        ag_b = ALAP_B + [blokk('szo.uj')]
        el, (hibak, _) = self.hibak(ag_b, dict(ALAP_T, t4={'szó': ['szo.uj']}))
        self.assertEqual(hibak, [])

    def test_blokk_eltunik_a_tabla_es_az_adatkeszlet_kovetkezmeny(self):
        el, (hibak, _) = self.hibak([b for b in ALAP_B if b['id'] != 'szo.a'], {k: v for k, v in ALAP_T.items() if k != 't1'})
        self.assertEqual([(e['szint'], e['kulcs']) for e in hibak], [('blokk', 'szo.a')])
        self.assertIn('hiányzik a regiszterből', hibak[0]['ok'])
        self.assertTrue(all(e['magyarazott'] for e in el if e['szint'] != 'blokk'))
        self.assertTrue(any(e['szint'] == 'tabla' and e['kulcs'] == 't1' for e in el))

    def test_tabla_kikerul_a_blokkbol_tablaszintu_hiba(self):
        """A blokk megvan, de a táblát már nem olvassa (vagy nem sorolja fel): a blokkszint nem látja, a táblaszint igen."""
        el, (hibak, _) = self.hibak(ALAP_B, dict(ALAP_T, t1={}))
        self.assertEqual([(e['szint'], e['kulcs'], e['nezet']) for e in hibak], [('tabla', 't1', 'szó')])

    def test_feltetelhez_kotott_rosszabb(self):
        ag_b = [dict(b, jegyzet=['üres eredménynél rejtve']) if b['id'] == 'szo.b' else b for b in ALAP_B]
        el, (hibak, _) = self.hibak(ag_b, ALAP_T)
        self.assertEqual([(e['szint'], e['kulcs']) for e in hibak], [('blokk', 'szo.b')])
        self.assertIn('feltételhez kötve', hibak[0]['ok'])

    def test_kiadasi_kizaras_nem_feltetel(self):
        ag_b = [dict(b, jegyzet=['kizárva a(z) nyilvános kiadásból']) if b['id'] == 'szo.b' else b for b in ALAP_B]
        el, (hibak, _) = self.hibak(ag_b, ALAP_T)
        self.assertEqual(hibak, [])

    def test_nem_latszik_hiba(self):
        ag_b = [dict(b, latszik=False) if b['id'] == 'vers.c' else b for b in ALAP_B]
        el, (hibak, _) = self.hibak(ag_b, dict(ALAP_T, t3={}))
        self.assertEqual([(e['szint'], e['kulcs']) for e in hibak], [('blokk', 'vers.c')])

    def test_masik_ful(self):
        ag_b = [dict(b, hely='Témák fül') if b['id'] == 'vers.c' else b for b in ALAP_B]
        el, (hibak, _) = self.hibak(ag_b, ALAP_T)
        self.assertEqual([(e['szint'], e['kulcs']) for e in hibak], [('blokk', 'vers.c')])
        self.assertIn('másik fülre', hibak[0]['ok'])

    def test_ful_valtas_ha_a_main_sem_a_vers_fulon_volt_nem_hiba(self):
        alap_b = [dict(b, hely='Témák fül') if b['id'] == 'vers.c' else b for b in ALAP_B]
        ag_b = [dict(b, hely='Kereszthiv. fül') if b['id'] == 'vers.c' else b for b in ALAP_B]
        self.assertEqual(B.osszevet(allapot(alap_b, ALAP_T), allapot(ag_b, ALAP_T)), [])

    def test_kivetel_illik(self):
        ag_b = [b for b in ALAP_B if b['id'] != 'szo.a']
        ag_t = {k: v for k, v in ALAP_T.items() if k != 't1'}
        el, (hibak, kivetelesek) = self.hibak(ag_b, ag_t, [('blokk', 'szo.a', '*', 'a szerkesztő döntése: a blokk összevonva a szo.b-be')])
        self.assertEqual(hibak, [])
        self.assertEqual(len(kivetelesek), 1)

    def test_kivetel_masik_nezetre_nem_illik(self):
        ag_b = [b for b in ALAP_B if b['id'] != 'szo.a']
        ag_t = {k: v for k, v in ALAP_T.items() if k != 't1'}
        el, (hibak, _) = self.hibak(ag_b, ag_t, [('blokk', 'szo.a', 'vers', 'a szerkesztő döntése: a blokk összevonva a szo.b-be')])
        self.assertEqual(len(hibak), 1)

    def test_a_kivetel_fajl_olvashato_es_az_indok_kotelezo(self):
        B.kivetelek_beolvas()                                         # a valódi fájl: a fejléc és a sorok rendben
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            ut = os.path.join(t, 'k.tsv')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write('szint\tkulcs\tnezet\tindok\nblokk\tszo.a\t*\trövid\n')
            with self.assertRaises(ValueError):
                B.kivetelek_beolvas(ut)
            with open(ut, 'w', encoding='utf-8') as f:
                f.write('szint\tkulcs\tnezet\tindok\nblokk\tszo.a\t*\ta szerkesztő döntése, egy sor indokkal\n')
            self.assertEqual(len(B.kivetelek_beolvas(ut)), 1)


class TesztBlokkcim(unittest.TestCase):
    """A leltár az `F('kulcs')`-os blokkcímet a `konfig/feliratok.tsv` magyar szövegére oldja fel (nem `None`, nem nyers kulcs)."""

    def test_literal_es_felirat_kulcs(self):
        import ast
        csomo = lambda k: ast.parse(k, mode='eval').body
        self.assertEqual(B.blokk_cim(csomo("'Károli-szöveg'")), 'Károli-szöveg')
        self.assertEqual(B.blokk_cim(csomo("F('blokk.szo.thayer')")), B.feliratok_hu()['blokk.szo.thayer'])
        self.assertEqual(B.blokk_cim(csomo("F('nincs.ilyen.kulcs')")), "F('nincs.ilyen.kulcs')")
        self.assertEqual(B.blokk_cim(csomo("valami(1)")), '?')

    def test_a_harom_blokk_cime_a_regiszterben(self):
        cim = {b['id']: b['cim'] for b in B.regiszter_beolvas(B._parse('blokkok.py'))}
        self.assertEqual(cim['szo.magyar_gorog'], 'Szótár: Thayer-szócikk')
        self.assertEqual(cim['szo.tbesg'], 'TBESG (forrásszöveg)')
        self.assertEqual(cim['szo.thayer'], 'Thayer, angol (forrásszöveg)')

    def test_egy_blokk_cime_sem_nyers_kulcs_vagy_ismeretlen(self):
        for b in B.regiszter_beolvas(B._parse('blokkok.py')):
            self.assertIsInstance(b['cim'], str, b['id'])
            self.assertFalse(b['cim'] in ('', '?') or b['cim'].startswith('F('), '%s: feloldatlan blokkcím: %r' % (b['id'], b['cim']))


if __name__ == '__main__':
    unittest.main()
