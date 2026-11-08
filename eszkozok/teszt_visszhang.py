#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_visszhang.py -- F176 (VISSZHANG_ADAT) tesztek:
  * az arany-kapu (nyilt_mag_kapu.py ARANY) a 0,5% / 2% / 6% mesterseges esetre a harom szintet adja
    (rendben / FIGYELMEZTETES / BUKAS), a hatarertekeken (1,0% es 5,0%) meg nem lep at;
  * a BDB-gyorsitotar masodik futasa nem ker le ujra (a "nincs rokon iras" a fejlecben rogzul, nem sor);
  * a BDB-token szetvalogatas (arab / etiop / szir, Unicode-blokk szerint; heber es latin nem);
  * az ot visszhang-tabla szerkezete: oszlopszam, igehely-forma, a README tetelszama egyezik a sorszammal,
    a THGNT-szoveg nem szerepel, a Vulgata-lábjegyzet nem szerepel, a HAMART-001 elso futasanak elvart eredmenye.
    (A tablateszteket csak akkor futtatja, ha a tablak a repoban megvannak.)

    python eszkozok/teszt_visszhang.py
"""
import os
import re
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(HELY)
sys.path.insert(0, HELY)
sys.path.insert(0, os.path.join(HELY, 'visszhang'))

import nyilt_mag_kapu as KAPU  # noqa: E402
import bdb_rokon as B  # noqa: E402
import kozos as KZ  # noqa: E402

KONK = os.path.join(GYOKER, 'konkordancia')


def olvas(nev):
    return KZ.olvas_tsv(os.path.join(KONK, nev))


def szoveg_fajl(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


class AranyKapu(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.readme = os.path.join(self.tmp, 'README.md')
        # a tetelszam a README gepi tablajabol jon (1000-1000 tetel); a kapu a fajlt innen olvassa
        with open(self.readme, 'w', encoding='utf-8') as f:
            f.write('| dataset | fajl | tetel | sha256 | licenc |\n|---|---|---|---|---|\n')
            for n in ('TesztA', 'TesztB', 'TesztC', 'TesztD', 'TesztE'):
                f.write('| %s | konkordancia/%s.tsv | 1000 | x | y |\n' % (n, n))
        self.regi = KAPU.VISSZHANG_README
        KAPU.VISSZHANG_README = self.readme

    def tearDown(self):
        KAPU.VISSZHANG_README = self.regi

    def csomag(self, darabok):
        sorok = ['motivum_azonosito\tforras_dataset\tszotar']
        for n, d in darabok.items():
            sorok += ['X-001\t%s\t' % n] * d
        return {'elofordulasok.tsv': '# GENERÁLT\n' + '\n'.join(sorok) + '\n'}

    def test_harom_szint(self):
        # 5 / 1000 = 0,5% ; 20 / 1000 = 2% ; 60 / 1000 = 6%
        ki = KAPU.ell_arany(self.csomag({'TesztA': 5, 'TesztB': 20, 'TesztC': 60}))
        szint = {t.idezet: t.suly for t in ki}
        self.assertNotIn('TesztA', szint)                         # 0,5% -> semmi
        self.assertEqual(szint['TesztB'], KAPU.FIGY)              # 2% -> FIGYELMEZTETES
        self.assertEqual(szint['TesztC'], KAPU.BUKAS)             # 6% -> BUKAS
        self.assertTrue(any(s.startswith('TesztC: 60 / 1000 = 6.00%') for s in KAPU.ARANY_INFO))

    def test_hatarertek_nem_lep_at(self):
        ki = KAPU.ell_arany(self.csomag({'TesztD': 10, 'TesztE': 50}))     # 1,0% es 5,0%
        szint = {t.idezet: t.suly for t in ki}
        self.assertNotIn('TesztD', szint)                         # pontosan 1% meg rendben
        self.assertEqual(szint['TesztE'], KAPU.FIGY)              # pontosan 5% meg csak FIGYELMEZTETES, nem BUKAS

    def test_szint_fuggveny(self):
        self.assertEqual(KAPU.arany_szint(5, 1000)[1], 'rendben')
        self.assertEqual(KAPU.arany_szint(20, 1000)[1], 'figy')
        self.assertEqual(KAPU.arany_szint(60, 1000)[1], 'hiba')
        self.assertEqual(KAPU.arany_szint(1, 0)[1], 'ismeretlen')

    def test_ismeretlen_tetelszam_figyelmeztet(self):
        ki = KAPU.ell_arany(self.csomag({'NincsTetelszam': 3}))
        szint = {t.idezet: t.suly for t in ki}
        self.assertEqual(szint['NincsTetelszam'], KAPU.FIGY)      # nem ellenorizheto arany: FIGYELMEZTETES, nem csend
        self.assertTrue(any(s.startswith('NincsTetelszam: 3 / ?') for s in KAPU.ARANY_INFO))

    def test_tobbforrasu_sor(self):
        cs = {'elofordulasok.tsv': 'motivum_azonosito\tforras_dataset\tszotar\nX-001\tTesztA; TesztB\tTesztA\n'}
        KAPU.ell_arany(cs)
        info = ' | '.join(KAPU.ARANY_INFO)
        self.assertIn('TesztA: 1 / 1000', info)                   # egy sor egyszer szamit, akkor is, ha ketszer nevezi
        self.assertIn('TesztB: 1 / 1000', info)

    def test_readme_tabla_olvasasa(self):
        t = KAPU.visszhang_tetelszamok(szoveg_fajl(os.path.join(KONK, 'VISSZHANG_README.md')))
        for n in ('Targum_PD', 'Vulgata_Clementina', 'SBLGNT_apparatus', 'TAGNT_valtozatok', 'BDB_rokon_irasok'):
            self.assertIn(n, t)
        self.assertEqual(t['BDB_rokon_irasok'][1], 'sor')


class BdbToken(unittest.TestCase):
    def test_iras_szerinti_szetvalogatas(self):
        szoveg = 'Arabic سحت extirpate; Ethiopic ሰሐጠ: injure; Aramaic שחת , ܫܚܛ (assim.) Greek θεός shachath'
        ki = B.tokenek(szoveg)
        nyelvek = [n for n, _, _ in ki]
        self.assertEqual(nyelvek, ['arab', 'etióp', 'szír'])      # heber, gorog, latin nem
        self.assertEqual(ki[0][1], 'سحت')

    def test_latin_heber_nem_token(self):
        self.assertEqual(B.tokenek('shachath שחת θεός'), [])


class BdbGyorsitotar(unittest.TestCase):
    ENTRY = [{'parent_lexicon': 'BDB Dictionary', 'headword': 'x', 'rid': 'BDBT1', 'strong_numbers': ['7843'],
              'content': {'senses': [{'definition': 'destroy; Arabic سحت extirpate; Ethiopic ሰሐጠ: injure; Syriac ܫܚܛ mutilate'}]}}]

    def setUp(self):
        self.ki = os.path.join(tempfile.mkdtemp(), 'BDB_rokon_irasok.tsv')
        self.hivas = []

    def lekero(self, szo, volt):
        self.hivas.append(szo)
        # a H7843 talal; a H2555 BDB-szocikket talal, de nincs benne rokon irast
        if szo == B.fejszo('H2555'):
            return [{'parent_lexicon': 'BDB Dictionary', 'headword': 'y', 'strong_numbers': ['2555'],
                     'content': {'senses': [{'definition': 'violence'}]}}]
        return self.ENTRY

    def nem_hivhato(self, szo, volt):
        raise AssertionError('a gyorsitotar-talalatnal nem szabad lekerdezni: %s' % szo)

    def test_masodik_futas_nem_kerdez(self):
        jel, keres, sorok = B.fut(['H7843', 'H2555'], self.ki, self.lekero)
        self.assertEqual(keres, 2)
        self.assertEqual(len(sorok), 3)                            # arab, etiop, szir
        self.assertEqual(sorted(s[2] for s in sorok), ['arab', 'etióp', 'szír'])
        szoveg = szoveg_fajl(self.ki)
        self.assertIn('# lekérdezve: H2555 | ', szoveg)            # a "nincs rokon iras" a fejlecben van ...
        self.assertIn('rokon_írás_sor=0', szoveg)
        self.assertEqual(sum(1 for s in szoveg.split('\n') if s.startswith('H2555\t')), 0)   # ... nem sorkent
        # masodik futas: semmi lekeres
        jel2, keres2, sorok2 = B.fut(['H7843', 'H2555'], self.ki, self.nem_hivhato)
        self.assertEqual(keres2, 0)
        self.assertEqual(len(sorok2), 3)
        self.assertEqual([j[1] for j in jel2], ['gyorsítótárban', 'gyorsítótárban'])
        # a fajl bajtra azonos (determinisztikus)
        self.assertEqual(szoveg_fajl(self.ki), szoveg)

    def test_uj_strong_csak_az_hianyzot_kerdezi(self):
        B.fut(['H7843'], self.ki, self.lekero)
        n0 = len(self.hivas)
        jel, keres, sorok = B.fut(['H7843', 'H2555'], self.ki, self.lekero)
        self.assertEqual(keres, 1)
        self.assertEqual(len(self.hivas) - n0, 1)

    def test_egybetus_token_kiszurve(self):
        adat = [{'parent_lexicon': 'BDB Dictionary', 'headword': 'x', 'strong_numbers': ['7843'],
                 'content': {'senses': [{'definition': 'Aramaic שחת , ܫܚܛ (assim. of ܬ ) mutilate'}]}}]
        sorok = B.feldolgoz('H7843', adat, '2026-11-08')
        self.assertEqual([s[3] for s in sorok], ['ܫܚܛ'])           # az egybetus "ܬ" nem rokon szoalak

    def test_kontextus_max_120(self):
        jel, keres, sorok = B.fut(['H7843'], self.ki, self.lekero)
        for s in sorok:
            self.assertLessEqual(len(s[4]), 120)
            self.assertIn('scope=', s[5])
            self.assertIn('forras=', s[5])
            self.assertIn('ts=', s[5])


@unittest.skipUnless(all(os.path.exists(os.path.join(KONK, n)) for n in (
    'Targum_PD.tsv', 'Vulgata_Clementina.tsv', 'SBLGNT_apparatus.tsv', 'TAGNT_valtozatok.tsv', 'BDB_rokon_irasok.tsv')),
    'a visszhang-tablak nincsenek a repoban')
class Tablak(unittest.TestCase):
    IGEHELY = re.compile(r'^[1-5]?[^\W\d_]+ [0-9]+:[0-9]+$')

    def sorok(self, nev):
        fej, sorok = olvas(nev)
        return fej, sorok

    def test_readme_tetelszam_egyezik(self):
        t = KAPU.visszhang_tetelszamok(szoveg_fajl(os.path.join(KONK, 'VISSZHANG_README.md')))
        for n, nev in (('Targum_PD', 'Targum_PD.tsv'), ('Vulgata_Clementina', 'Vulgata_Clementina.tsv'),
                       ('SBLGNT_apparatus', 'SBLGNT_apparatus.tsv'), ('TAGNT_valtozatok', 'TAGNT_valtozatok.tsv')):
            self.assertEqual(t[n][1], len(self.sorok(nev)[1]), n)

    def test_igehely_es_oszlopok(self):
        for nev in ('Targum_PD.tsv', 'Vulgata_Clementina.tsv', 'SBLGNT_apparatus.tsv', 'TAGNT_valtozatok.tsv'):
            fej, sorok = self.sorok(nev)
            self.assertIn('igehely', fej)
            self.assertIn('forras_kulcs', fej)
            self.assertNotIn('', fej)
            for d in sorok:
                self.assertRegex(d['igehely'], self.IGEHELY, '%s: %r' % (nev, d['igehely']))
                self.assertIn(d['forras_kulcs'], ('igen', 'nem'))

    def test_targum_csak_pd_es_ket_targum(self):
        fej, sorok = self.sorok('Targum_PD.tsv')
        self.assertEqual({d['targum'] for d in sorok}, {'Onkelos', 'Jonatan'})
        self.assertEqual(len({d['forras_mu'] for d in sorok}), 26)
        szoveg = szoveg_fajl(os.path.join(KONK, 'Targum_PD.tsv'))
        self.assertIn('license=Public Domain', szoveg)
        self.assertTrue(all(d['szoveg'] for d in sorok))
        kulcs = [d['igehely'] + '|' + d['targum'] for d in sorok]
        self.assertEqual(len(kulcs), len(set(kulcs)))              # nincs ketszer ugyanaz a vers

    def test_vulgata_nincs_labjegyzet(self):
        fej, sorok = self.sorok('Vulgata_Clementina.tsv')
        for d in sorok:
            self.assertNotIn(chr(92), d['szoveg'])                 # nincs USFM-jeloles / labjegyzet
            self.assertTrue(d['szoveg'])
        self.assertEqual(len({d['forras_vers'].split()[0] for d in sorok}), 66)
        k = [d['igehely'] for d in sorok]
        self.assertEqual(len(k), len(set(k)))

    def test_sblgnt_csak_apparatus(self):
        fej, sorok = self.sorok('SBLGNT_apparatus.tsv')
        self.assertEqual(fej, ['igehely', 'forras_vers', 'sorszam', 'forras_kulcs', 'jegyzet'])
        self.assertTrue(all(d['jegyzet'] for d in sorok))
        self.assertTrue(any('WH' in d['jegyzet'] for d in sorok))
        self.assertEqual(len({d['forras_vers'].rsplit(' ', 1)[0] for d in sorok}), 27)

    def test_tagnt_pontos_utotag(self):
        # a fejezet.vers alaku utotag (Byz«x14.24) is levagodik a nevbol: a kiadas nem hianyzik, hanem mozgatott
        import re as _re
        fej, sorok = self.sorok('TAGNT_valtozatok.tsv')
        n = 0
        for d in sorok:
            for e in d['kiadasok'].split('+'):
                m = _re.match(r'^(.*?)((?:[»«]\d+(?:\.\d+)?)+)$', e)
                if not m:
                    continue
                n += 1
                self.assertNotIn(m.group(1), d['hianyzik_ebbol'].split(), d['igehely'])
                self.assertIn(e, d['mozgatas'].split(), d['igehely'])
        self.assertGreaterEqual(n, 53)
        r = [d for d in sorok if '«14.24' in d['kiadasok']]
        self.assertEqual(len(r), 20)
        self.assertTrue(all(d['hianyzik_ebbol'] == 'SBL' and d['mozgatas'] == 'Byz«14.24' for d in r))

    def test_tagnt_nincs_thgnt_szoveg(self):
        fej, sorok = self.sorok('TAGNT_valtozatok.tsv')
        self.assertNotIn('Spelling variants', ' '.join(fej))
        self.assertNotIn('meaning_variants', fej)
        self.assertIn('jelentesvaltozat', fej)
        # a csak-Tyn szo gorog mezoje ures (a szoveg THGNT-eredetu lenne)
        tyn = [d for d in sorok if set(d['kiadasok'].split('+')) <= {'Tyn'}]
        self.assertTrue(tyn)
        self.assertTrue(all(d['gorog'] == '' for d in tyn))
        for d in sorok:
            self.assertTrue(d['kiadasok'])
            self.assertIn(d['szamozas'], ('nrsv', 'kjv', 'egyeb', 'na'))
            self.assertRegex(d['szo_sorszam'], r'^#[0-9]+$')
        # a teljes halmaz + NKO sor nincs a kimenetben
        teljes = 'NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz'
        self.assertFalse([d for d in sorok if d['kiadasok'] == teljes and d['tipus'] == 'NKO'])

    def test_bdb_rokon_hamart(self):
        fej, sorok = olvas('BDB_rokon_irasok.tsv')
        self.assertEqual(fej, ['strong', 'sefaria_ref', 'nyelv', 'szoalak', 'kontextus', 'proveniencia'])
        szoveg = szoveg_fajl(os.path.join(KONK, 'BDB_rokon_irasok.tsv'))
        lek = {s.split(' | ')[0][len('# lekérdezve: '):] for s in szoveg.split('\n') if s.startswith('# lekérdezve: ')}
        for st in ('H0779', 'H0127', 'H6093', 'H2403', 'H2555', 'H7843', 'H6975', 'H1863'):
            self.assertIn(st, lek)
        h7843 = {d['nyelv'] for d in sorok if d['strong'] == 'H7843'}
        self.assertEqual(h7843, {'arab', 'etióp', 'szír'})                  # elvart: a H7843-ra mindharom megvan
        for st in ('H2555', 'H6093', 'H6975'):                              # elvart: nincs rokon szo
            self.assertFalse([d for d in sorok if d['strong'] == st], st)
        for d in sorok:
            self.assertLessEqual(len(d['kontextus']), 120)
            self.assertIn(d['nyelv'], ('arab', 'etióp', 'szír'))
            self.assertEqual({B.irasa(c) for c in d['szoalak'] if B.irasa(c)}, {d['nyelv']})


if __name__ == '__main__':
    unittest.main(verbosity=2)
