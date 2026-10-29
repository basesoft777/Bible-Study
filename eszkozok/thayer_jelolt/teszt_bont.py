#!/usr/bin/env python
"""A Thayer szakasztábla bontójának tesztjei (F132 M1, eszkozok/thayer_jelolt/bont.py; kulcs.py).

Futtatás: python eszkozok/thayer_jelolt/teszt_bont.py   (a táblás tesztek a kiírt adat/thayer_szakaszok.tsv-t és a
forrásokat olvassák; a determinizmus-teszt a --ellenoriz módot hívja, kb. 10–20 s).
"""
import collections
import os
import re
import subprocess
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import bont  # noqa: E402
import kulcs  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'thayer_szakaszok.tsv')


def tabla():
    with open(TABLA, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]


_CACHE = {}


def adatok():
    if not _CACHE:
        fej, sorok = tabla()
        _CACHE['fej'], _CACHE['sorok'] = fej, sorok
        _CACHE['lex'] = bont.lexikon_beolvas()
        _CACHE['tsv'] = bont.tsv_beolvas()
        st = collections.OrderedDict()
        for r in sorok:
            st.setdefault(r['strong'], []).append(r)
        _CACHE['st'] = st
    return _CACHE


def nows(s):
    return re.sub(r'\s+', '', s)


class Kulcs(unittest.TestCase):
    def test_pad(self):
        self.assertEqual(kulcs.strong_pad('G12'), 'G0012')
        self.assertEqual(kulcs.strong_pad('G0012'), 'G0012')
        self.assertEqual(kulcs.strong_pad('g1941'), 'G1941')
        self.assertEqual(kulcs.strong_pad('G5624'), 'G5624')
        for rossz in ('H12', 'G', 'G12a', 'G0', 'info', '', None, 'G12345'):
            self.assertIsNone(kulcs.strong_pad(rossz), rossz)

    def test_eredeti(self):
        self.assertEqual(kulcs.strong_eredeti('G0012'), 'G12')
        self.assertEqual(kulcs.strong_eredeti('G12'), 'G12')

    def test_negy_gerincszo_nem_nema(self):
        # M0: normalizálás nélkül ez a négy gerincszó néma nem-találat
        st = adatok()['st']
        for s in ('G12', 'G86', 'G282', 'G813'):
            self.assertIn(kulcs.strong_pad(s), st)

    def test_egyetlen_normalizalo(self):
        # DT-F132b (4): a thayer_jelolt-ban csak a kulcs.py normalizál (nincs saját %04d-kitöltés)
        for fn in os.listdir(ITT):
            if fn.endswith('.py') and fn != 'kulcs.py' and not fn.startswith('teszt_'):
                with open(os.path.join(ITT, fn), encoding='utf-8') as f:
                    self.assertNotRegex(f.read(), r"'G%04d'|\"G%04d\"|zfill\(4\)", fn)


class Egyseg(unittest.TestCase):
    def test_szegmens_lezaratlan_p(self):
        d = '<div></p><p><p><b>G1 — x</b></p>, tovább <i>y</i> </p><p><b>1.</b> egy</p></div>'
        self.assertEqual([bont.sima(s) for s in bont.szegmensek(d)], ['G1 — x', ', tovább y', '1. egy'])

    def test_szerkezet_szintek(self):
        d = ('<div><p><b>G9 — x</b></p><p>fej</p><p>A. első</p><p><span class="lexheading">I.</span> r</p>'
             '<p><b>1.</b> sz</p><p><b>a.</b> b</p><p>örökölt</p><p><b>2.</b> k</p><p>B. második</p><p>D. nem fej</p></div>')
        sz = bont.szerkezet(d)
        self.assertEqual([x['utvonal'] for x in sz],
                         ['cim', 'fej', 'A/-/-', 'A.I/-/-', 'A.I/1/-', 'A.I/1/a', 'A.I/1/a', 'A.I/2/-', 'B/-/-', 'B/-/-'])
        self.assertEqual([x['jel'] for x in sz], ['', '', 'A.', 'I.', '1.', 'a.', '', '2.', 'B.', ''])

    def test_illeszt_egyezik_es_reszleges(self):
        sz = bont.szerkezet('<p><b>G9 — x</b></p><p><b>1.</b> alfa béta</p><p><b>2.</b> gamma</p>')
        self.assertEqual(bont.illeszt(sz, 'G9 — x 1. alfa  béta 2. gamma'),
                         ('egyezik', ['G9 — x', '1. alfa  béta', '2. gamma']))
        kat, t = bont.illeszt(sz, 'G9 — x 1. alfa 2. gamma')
        self.assertEqual(kat, 'reszleges')
        self.assertEqual(t[2], '2. gamma')
        self.assertEqual(bont.illeszt(sz, None), ('sikertelen', ['', '', '']))


class Tabla(unittest.TestCase):
    def test_fejlec(self):
        with open(TABLA, encoding='utf-8') as f:
            a, b = f.readline(), f.readline()
        self.assertTrue(a.startswith('# GENERÁLT: eszkozok/thayer_jelolt/bont.py --ts '))
        self.assertTrue(b.startswith('# forras: konkordancia/lexikonok_nyers/Thayer.lexicon@'))
        self.assertEqual(adatok()['fej'], bont.FEJLEC)

    def test_minden_bekezdes_egy_sorban(self):
        a = adatok()
        self.assertEqual(set(a['st']), set(a['lex']))
        n = 0
        for sp, (topic, d) in a['lex'].items():
            seg = bont.szegmensek(d)
            sorok = a['st'][sp]
            self.assertEqual([int(r['sorszam']) for r in sorok], list(range(1, len(seg) + 1)), sp)
            self.assertEqual([r['forras'] for r in sorok], ['Thayer.lexicon:%s#%d' % (topic, i) for i in range(1, len(seg) + 1)])
            n += len(seg)
        self.assertEqual(n, 17093)  # a forrás <p>-száma (M0)

    def test_kulcs_strong_padded(self):
        for r in adatok()['sorok']:
            self.assertRegex(r['strong'], r'^G\d{4}$')

    def test_osszefuzes_a_tsv_szoveg(self):
        # egyező illesztésnél a sorok (jel + szoveg) összefűzése = a TSV szövege, és soronként = a bekezdés sima szövege
        a = adatok()
        egyezik = 0
        for sp, sorok in a['st'].items():
            if sorok[0]['illesztes'] != 'egyezik':
                continue
            egyezik += 1
            self.assertEqual(nows(''.join(r['jel'] + r['szoveg'] for r in sorok)), nows(a['tsv'][sp]), sp)
            plain = [bont.sima(s) for s in bont.szegmensek(a['lex'][sp][1])]
            self.assertEqual([nows(r['jel'] + r['szoveg']) for r in sorok], [nows(p) for p in plain], sp)
        self.assertGreaterEqual(egyezik, 5400)

    def test_reszleges_explicit(self):
        st = adatok()['st']
        kat = collections.Counter(s[0]['illesztes'] for s in st.values())
        self.assertEqual(set(kat) - {'egyezik', 'javitassal', 'reszleges', 'sikertelen'}, set())
        for sp, sorok in st.items():
            self.assertEqual(len({r['illesztes'] for r in sorok}), 1, sp)

    def test_g1941_aranyminta(self):
        # kézzel ellenőrizve (napló, M1): 7 bekezdés, 5 számozott fej
        s = adatok()['st']['G1941']
        self.assertEqual([r['utvonal'] for r in s], ['cim', 'fej', '-/1/-', '-/2/-', '-/3/-', '-/4/-', '-/5/-'])
        self.assertEqual([r['jel'] for r in s], ['', '', '1.', '2.', '3.', '4.', '5.'])
        self.assertEqual(s[0]['szoveg'], 'G1941 — ἐπικαλέω')
        self.assertTrue(s[2]['szoveg'].startswith('to put a name upon, to surname:'))
        self.assertTrue(s[6]['szoveg'].startswith('Hebraistically'))
        self.assertEqual({r['illesztes'] for r in s}, {'egyezik'})

    def test_proveniencia(self):
        for r in adatok()['sorok']:
            self.assertRegex(r['proveniencia'], r'^scope=%s \| forras=thayer_jelolt/bont\.py \(fejléc\) \| ts=\d{4}-\d\d-\d\d$' % r['strong'])

    def test_nincs_tab_sortores(self):
        with open(TABLA, encoding='utf-8', newline='') as f:
            for s in f.read().split('\n')[3:]:
                if s:
                    self.assertEqual(len(s.split('\t')), len(bont.FEJLEC))
                    self.assertNotIn('\r', s)


class Javitas(unittest.TestCase):
    """DT-F132i (2): adat/thayer_forras_javitas.tsv (SEMA 2.38) és a javított nézet (thayer_bemenet.szakaszok)."""

    def jav(self):
        with open(bont.JAV_UT, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        fej = sorok[2].split('\t')
        return [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]

    def test_tizenot_lyuk_javitva(self):
        j = self.jav()
        self.assertEqual(len(j), 15)
        self.assertEqual({r['allapot'] for r in j}, {'javitva'})
        self.assertEqual(sum(int(r['hossz']) for r in j), 2715)  # M1: 2 715 karakter szóközök nélkül
        self.assertIn('G4151', {r['strong'] for r in j})
        for r in j:
            self.assertRegex(r['proveniencia'], r'^scope=%s \| forras=thayer_jelolt/forras_javit\.py \(fejléc\) \| ts=\d{4}-\d\d-\d\d$'
                             % r['strong'])

    def test_tabla_nyers_hatar_pontos(self):
        # a szakasztábla nyers marad: a javitassal Strong sorainak összefűzése = a TSV szövege (szóközök nélkül)
        a = adatok()
        n = 0
        for sp, sorok in a['st'].items():
            if sorok[0]['illesztes'] != 'javitassal':
                continue
            n += 1
            self.assertEqual(nows(''.join(r['jel'] + r['szoveg'] for r in sorok)), nows(a['tsv'][sp]), sp)
        self.assertEqual(n, 15)

    def test_nezet_a_lexikon_szovege(self):
        # a javított nézet soronként = a lexikonbekezdés címkék nélküli szövege (szóközök nélkül)
        import thayer_bemenet as TB
        a = adatok()
        for r in self.jav():
            sp = r['strong']
            nezet = TB.szakaszok(sp)
            plain = [bont.sima(s) for s in bont.szegmensek(a['lex'][sp][1])]
            self.assertEqual([nows(x['szoveg']) for x in nezet], [nows(p) for p in plain], sp)
            self.assertIn(r['javitott_alak'], nezet[int(r['sorszam']) - 1]['szoveg'])

    def test_g4151(self):
        import thayer_bemenet as TB
        self.assertTrue(TB.szakaszok('G4151')[5]['szoveg'].endswith('1Co 14:15, 1Co 14:16.'))
        self.assertNotIn('1Co 14:16.', adatok()['st']['G4151'][5]['szoveg'])

    def test_rossz_elotte_hibat_dob(self):
        import thayer_bemenet as TB
        r = {'strong': 'G4151', 'sorszam': '6', 'illesztes': 'javitassal', 'szoveg': 'x' * 5000}
        with self.assertRaises(ValueError):
            TB.javitott_szoveg(r, TB.javitas_olvas())

    def test_javitas_nelkul_reszleges(self):
        # javítótábla nélkül a bontó a 15 Strongot `reszleges`-nek írja (a régi viselkedés)
        _, stat, _ = bont.general('2026-10-25', jav_ut=None)
        self.assertEqual((stat['reszleges'], stat['javitassal']), (15, 0))

    def test_crlf_bemenet(self):
        # a CRLF-es tábla és javítótábla (Windows, autocrlf) ugyanazt adja, mint az LF-es: a '\r' nem kerül a kulcsba
        # (E19, test_szabalyok: KeyError 'illesztes')
        import tempfile
        import thayer_bemenet as TB
        tabla = ('# GENERALT: teszt\nstrong\tsorszam\tutvonal\tjel\tszoveg\tillesztes\n'
                 'G0086\t1\tcim\t\tG86 - a\tegyezik\nG0086\t2\t-/1/-\t1.\tb\tegyezik\n')
        jav = ('# GENERALT: teszt\nstrong\tsorszam\tsor_poz\tjavitott_alak\telotte\tallapot\n'
               'G0540\t2\t1\tX\te\tjavitva\n')
        with tempfile.TemporaryDirectory() as tmp:
            eredmeny = {}
            for nev, vegz in (('lf', '\n'), ('crlf', '\r\n')):
                t, j = os.path.join(tmp, nev + '_t.tsv'), os.path.join(tmp, nev + '_j.tsv')
                for ut, tart in ((t, tabla), (j, jav)):
                    with open(ut, 'w', encoding='utf-8', newline='') as f:
                        f.write(tart.replace('\n', vegz))
                eredmeny[nev] = (TB.szakaszok('G0086', t, j), TB.javitas_olvas(j))
            self.assertEqual(eredmeny['crlf'], eredmeny['lf'])
            self.assertEqual([x['illesztes'] for x in eredmeny['crlf'][0]], ['egyezik', 'egyezik'])
            self.assertEqual(eredmeny['crlf'][1], {('G0540', '2'): (1, 'X', 'e')})

    def test_forras_javit_ellenoriz(self):
        r = subprocess.run([sys.executable, os.path.join(ITT, 'forras_javit.py'), '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class Determinizmus(unittest.TestCase):
    def test_ellenoriz(self):
        r = subprocess.run([sys.executable, os.path.join(ITT, 'bont.py'), '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
