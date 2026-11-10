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
        sz = bont.szerkezet(d, osszevonas=False)  # a fejfelismerés; az összevonás: F186Fejek
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


def _ut(d, osszevonas=True):
    return [(x['utvonal'], x['jel'], x['plain'][:14])
            for x in bont.szerkezet('<div><p><b>G9 — x</b></p>' + d + '</div>', osszevonas=osszevonas)]


class F186Fejek(unittest.TestCase):
    """F186 T2: a seed-201 vak mérés hibaosztályai (naplok/F186_jelentes.md 3.), a forrás alakjával egyszerűsítve."""

    def test_k1_betu_szo_utan(self):
        # T029 G3360: „1. … and is used a. of time: …”; T044 G4487 „that a. so far forth”; T007 G3588 „participles a. gives”
        sz = _ut('<p><b>1.</b> it has the force of a preposition, and is used a. of time: '
                 '<ref onclick="bcv(54,6,14)">1Ti 6:14</ref>; b. of place: x</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/1/-', '-/1/a', '-/1/b'])
        self.assertEqual([x[1] for x in sz], ['', '1.', 'a.', 'b.'])

    def test_k1_bevezeto_bekezdesben(self):
        # T114 G5479: „joy, gladness; a: Luk 1:14” (kettősponttal); T171 G3367: „accordingly a. with an imperative”
        sz = _ut('<p>joy, gladness; a: <ref onclick="bcv(42,1,14)">Luk 1:14</ref></p>')
        self.assertEqual([x[0] for x in sz], ['cim', 'fej', '-/-/a'])
        self.assertEqual(sz[2][1], 'a:')

    def test_k1_mondatzaro_utan(self):
        # T191 G2192: „Joh 15:22, etc. h. of age”; T025 G3004: „…:12. h. with the dative … :18. i.: λέγω”
        sz = _ut('<p><b>g.</b> x, <ref onclick="bcv(43,15,22)">Joh 15:22</ref>, etc. h. of age: y</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/g', '-/-/h'])
        sz = _ut('<p><b>g.</b> x <ref onclick="bcv(43,3,12)">Joh 3:12</ref>. h. with the dative <ref onclick="bcv(43,3,18)">'
                 'Joh 3:18</ref>. i.:<ref0 class="word" entry="λέγω">λέγω</ref0> followed</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/g', '-/-/h', '-/-/i'])
        self.assertEqual(sz[3][1], 'i.')

    def test_k1_utalas_utan(self):
        # T159 G2228: „b. ἤ γάρ, see γάρ, I. at the end c. ἤ καί”
        sz = _ut('<p><b>b.</b> x, see y, I. at the end c. z</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/b', '-/-/c'])

    def test_k1_szam_es_betu(self):
        # T147 G0846: „e. … Joh 16:27 (… Xenophon). 2. When it gives Prominence, it answers a. to our emphatic he”
        sz = _ut('<p><b>1.</b> u</p><p><b>e.</b> self, <ref onclick="bcv(43,16,27)">Joh 16:27</ref> (Xenophon). '
                 '2. When it gives Prominence, it answers a. to our emphatic he: <ref onclick="bcv(40,1,21)">Mat 1:21</ref></p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/1/-', '-/1/e', '-/2/-', '-/2/a'])

    def test_k1_nem_fej(self):
        # a hivatkozás- és rövidítés-alakok nem nyitnak pontot (a teljes korpusz átnézett hamis jelöltjei)
        for d in ('<p><b>1.</b> x, Aristotle, h. a. 5, 19; y</p>',          # Historia animalium + szám
                  '<p><b>1.</b> x; cf. Bleek, Brief a. d. Heb 2:1</p>',      # „a. d.” rövidítés
                  '<p><b>1.</b> x, i. e. y; e. g. z</p>',                    # i. e., e. g.
                  '<p><b>1.</b> x (see in a. below); y</p>',                 # utalás
                  '<p><b>1.</b> x (cf. <b>χαίρω</b>, a.); y</p>',            # „)” követi
                  '<p><b>1.</b> x, cf. Winers Grammar, § 5, 1 a.; y</p>',    # szám előzi
                  '<p><b>1.</b> x (some refer this to a. in the sense); y</p>',  # „to” előzi
                  '<p>x, Plutarch, orac. def. c. 1. Sometimes y</p>',        # „c. 1.” fejezetszám
                  '<p>x, Winers Grammar, § 27, 6 N. 1. But y</p>'):          # „N. 1.” jegyzetszám
            sz = _ut(d)
            self.assertEqual(len(sz), 2, d)

    def test_k1b_vesszo_es_to_utan(self):
        # seed-202 U009 G4314 „πρός τινα or τί, a. properly”; U034/U180 G4396 „applied to a. the O. T. prophets”;
        # U140 G2307 „will, i. e., a. what one wishes”
        for d, ut in (('<p><b>1.</b> toward: <ref0 class="word" entry="τί">τί</ref0>, a. properly, after verbs</p>', '-/1/a'),
                      ('<p><b>1.</b> The title is applied to a. </i></b>the O. T. prophets</p>', '-/1/a'),
                      ('<p>will, i. e., a. what one wishes: <ref onclick="bcv(60,4,2)">1Pe 4:2</ref></p>', '-/-/a')):
            self.assertEqual(_ut(d)[-1][0], ut, d)

    def test_k1b_nem_fej(self):
        # zárójelen belül, felsorolt utalás, bekezdés végi jelölő, nagybetűs rövidítés, német „an d.”
        for d in ('<p><b>1.</b> x (some refer this to a. in the sense of farewell); y</p>',
                  '<p><b>1.</b> x, see ποιέω, I. 1 a. and b.; y</p>',
                  '<p><b>1.</b> x; see γωνία, a.</p>',
                  '<p><b>1.</b> x, cf. Hilgenfeld, Einl. in a. N. T., p. 487</p>',
                  '<p><b>1.</b> x, Bleek, Brief an a. Heb 2:2</p>'):
            self.assertEqual(len(_ut(d)), 2, d)

    def test_k1c_j_kimarad(self):
        # seed-202 U036 G3004, U165 G2192: a Thayer betűsora a „j”-t kihagyja (i → k)
        sz = _ut('<p><b>i.</b> x, <ref onclick="bcv(45,15,17)">Rom 15:17</ref>. k. ἔχειν τί is used of one</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/i', '-/-/k'])

    def test_k2b_utalas_zarojellel(self):
        # seed-202 U014 G1519: „<b>d.</b> at the end): Luk 20:20” — utalás-töredék, nem fej
        sz = _ut('<p><b>c.</b> u</p><p><b>d.</b> at the end): <ref onclick="bcv(42,20,20)">Luk 20:20</ref></p>'
                 '<p><b>d.</b> w</p><p><b>e.</b> above)).</p>', osszevonas=False)  # a fejdöntés, összevonás előtt
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/c', '-/-/c', '-/-/d', '-/-/d'])

    def test_k1_sorrend(self):
        # csak a várt következő jelölő nyit: a „c.” nem nyit, ha az aktuális betű „a”
        sz = _ut('<p><b>a.</b> x; and so c. other</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/-/a'])

    def test_osszevonas_hamis_fej_toredek(self):
        # ELLENOR_F186_2 1–2.: a G4151 4.a utáni „<b>b.</b> bb.; γεννάω, …” töredék nem külön `-/4/a` szakasz, hanem a 4.a része
        sz = _ut('<p><b>4.</b> u</p><p><b>a.</b> v (see βαπτίζω, II. b.</p><p><b>b.</b> bb.; γεννάω, 1 at the end) '
                 '<ref onclick="bcv(46,2,14)">1Co 2:14</ref></p><p><b>b.</b> w</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/4/-', '-/4/a', '-/4/b'])
        teljes = bont.szerkezet('<div><p><b>G9 — x</b></p><p><b>4.</b> u</p><p><b>a.</b> v (see βαπτίζω, II. b.</p><p><b>b.</b> '
                                'bb.; γεννάω</p></div>')
        self.assertEqual(teljes[2]['bekezdesek'], [3, 4])
        self.assertIn('v (see βαπτίζω, II. b. b. bb.; γεννάω', teljes[2]['plain'])

    def test_osszevonas_below_toredek(self):
        # G5590: a „c. below), 2Co 12:15.” utalás-töredék (K2b) az 1.b-hez tartozik, egy szakaszban
        sz = _ut('<p><b>1.</b> u</p><p><b>b.</b> life: x</p><p><b>c.</b> below), <ref onclick="bcv(47,12,15)">2Co 12:15</ref>.</p>'
                 '<p><b>c.</b> that in which there is life</p>')
        self.assertEqual([x[0] for x in sz], ['cim', '-/1/-', '-/1/b', '-/1/c'])

    def test_osszevonas_nelkul(self):
        # az összevonás előtti szerkezet (az F186.9 átkulcsolásának bemenete) változatlanul elérhető
        d = '<div><p><b>G9 — x</b></p><p><b>a.</b> v</p><p><b>b.</b> bb.; y</p></div>'
        self.assertEqual([x['utvonal'] for x in bont.szerkezet(d, osszevonas=False)], ['cim', '-/-/a', '-/-/a'])
        self.assertEqual([x['utvonal'] for x in bont.szerkezet(d)], ['cim', '-/-/a'])

    def test_k2_hamis_bekezdes_eleji_fej(self):
        # T145 G4151: „<b>b.</b> bb.; γεννάω, …” egy kettétört kereszthivatkozás töredéke; G1909: „<b>c.</b>)): as …”
        sz = _ut('<p><b>4.</b> u</p><p><b>a.</b> v (see βαπτίζω, II. b.</p><p><b>b.</b> bb.; γεννάω, 1 at the end) '
                 '<ref onclick="bcv(45,8,1)">Rom 8:1</ref></p><p><b>c.</b>)): as x</p><p><b>b.</b> w</p>', osszevonas=False)
        self.assertEqual([x[0] for x in sz], ['cim', '-/4/-', '-/4/a', '-/4/a', '-/4/a', '-/4/b'])
        self.assertEqual([x[1] for x in sz], ['', '4.', 'a.', '', '', 'b.'])


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
        # F186 K1: egy sor = egy szakasz (a bekezdés, vagy annak a bekezdésen belüli fejnél kezdődő része); a szakaszok
        # sima szövege bekezdésenként összefűzve a bekezdés sima szövege
        for sp, (topic, d) in a['lex'].items():
            seg = bont.szegmensek(d)
            sz = bont.szerkezet(d)
            sorok = a['st'][sp]
            self.assertEqual([int(r['sorszam']) for r in sorok], list(range(1, len(sz) + 1)), sp)
            self.assertEqual([r['forras'] for r in sorok], ['Thayer.lexicon:%s#%d' % (topic, i) for i in range(1, len(sz) + 1)])
            self.assertEqual(nows(''.join(x['plain'] for x in sz)), nows(''.join(bont.sima(s) for s in seg)), sp)
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
            plain = [x['plain'] for x in bont.szerkezet(a['lex'][sp][1])]
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
            plain = [x['plain'] for x in bont.szerkezet(a['lex'][sp][1])]
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
