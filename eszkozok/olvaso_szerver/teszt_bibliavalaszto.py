"""A bibliaválasztó (F210) tesztjei: a könyvválasztó legfelső szintje a Biblia (a mockup `Mk_08_Konyvvalaszto`-ja), a morzsa a
választott Bibliát is mutatja, és mindegyik felvett Biblia egy fejezete olvasható (1Móz 1; az ÚSZ-ban Mt 1, ahol van).

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_bibliavalaszto` (a WSL-natív PARDES_DB-vel). Az adatbázis nélküli tesztek
(a héber tokenek összefűzése, a KJV-illesztés) mindig futnak; az adatbázisos teszt kihagyódik, ha az építő még nem vette fel a
szövegtáblákat (régi `pardes.db`).
"""
import html as html_modul
import os
import re
import sys
import unicodedata
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import bibliak
from teszt_olvaso_szerver import VAN_DB, VAN_FLASK, app_keszit

UJ_TABLAK = ('szoveg_modern', 'token_modern', 'szoveg_kjv')


class TestSegedek(unittest.TestCase):
    def test_kod_es_parameter(self):
        self.assertEqual(bibliak.kod_kerese('kjv'), 'kjv')
        self.assertEqual(bibliak.kod_kerese('asv'), 'karoli')          # az ASV nem választható (forráshibás, N29/D7)
        self.assertEqual(bibliak.kod_kerese(''), 'karoli')
        self.assertEqual(bibliak.parameter('karoli'), '')
        self.assertEqual(bibliak.parameter('vulgata'), 'biblia=vulgata')
        # csak szószintű Strong-kapcsolatú szöveg (a felhasználó, 2026-11-12): a Targum és a Vulgata nem választható
        self.assertEqual([b.kod for b in bibliak.BIBLIAK], ['karoli', 'modern', 'tahot', 'tagnt', 'lxx', 'kjv'])
        self.assertEqual(bibliak.kod_kerese('vulgata'), 'karoli')
        self.assertEqual(bibliak.kod_kerese('targum'), 'karoli')
        self.assertTrue(all(b.strong_tablak for b in bibliak.BIBLIAK))

    def test_tahot_osszefuzes(self):
        # 1Móz 1:1: בְּ + רֵאשִׁית (előtag a szóhoz), הַ + שָּׁמַיִם; a nyelvtani elemre nincs koppintás
        tok = [(1, 'בְּ', 'H9003'), (2, 'רֵאשִׁ֖ית', 'H7225'), (3, 'בָּרָ֣א', 'H1254'), (6, 'הַ', 'H9009'), (7, 'שָּׁמַ֖יִם', 'H8064'),
               (16, 'מִינ֔', 'H4327'), (17, 'וֹ', 'H9023')]
        ws = bibliak._tahot_szavak(tok, {'H9003', 'H9009', 'H9023'})
        self.assertEqual([w['szokoz'] for w in ws], [False, True, True, False, True, False, True])
        self.assertEqual([w['fo'] for w in ws], [None, 'H7225', 'H1254', None, 'H8064', 'H4327', None])

    def test_kjv_illesztes(self):
        ws = bibliak._kjv_szavak('In the beginning God created the heaven and the earth.',
                                 [('beginning', 'H7225'), ('God', 'H0430'), ('created', 'H1254'), ('nincs', 'H0001')], set())
        self.assertEqual(''.join(w['kiir'] for w in ws), 'In the beginning God created the heaven and the earth.')
        self.assertEqual([(w['kiir'], w['fo']) for w in ws if w['fo']], [('beginning', 'H7225'), ('God', 'H0430'), ('created', 'H1254')])

    def test_lxx_szovegforma(self):
        tl = [('daniel-theodotion', 'x', 'a', ''), ('daniel', 'y', 'b', ''), ('daniel', 'y', 'c', '')]
        self.assertEqual([t[2] for t in bibliak._lxx_valaszt(tl)], ['b', 'c'])


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestBibliavalaszto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_keszit()
        cls.gyar = cls.app.extensions['pardes']['gyar']
        hianyzo = [t for t in UJ_TABLAK if t not in cls.gyar.kozos.licenc]
        if hianyzo:
            raise unittest.SkipTest('a pardes.db-ből hiányzik az F210 tábla: %s (újraépítés kell: sqlite_epit.py --mod teljes)' % ', '.join(hianyzo))
        cls.c = cls.app.test_client()

    def h(self, u, kod=200):
        r = self.c.get(u)
        self.assertEqual(r.status_code, kod, u)
        return r.get_data(as_text=True)

    def fej(self, h):
        return h[h.index('<header class="fejlec navlap" id="navigacio">'):h.index('</header>')]

    def szoveg(self, h):
        m = re.search(r'<p class="folyo[^"]*" id="szoveg"[^>]*>(.*?)</p>\s*\n?\s*</section>', h, re.S)
        self.assertIsNotNone(m)
        return m.group(1)

    def test_a_valaszto_a_mockup_szerint(self):
        f = self.fej(self.h('/1Moz/1'))
        self.assertIn('<p class="valaszto-cim">Biblia és könyv kiválasztása</p>', f)
        self.assertIn('<span class="morzsa-biblia">Károli 1908 ·</span> 1Móz 1', f)
        # sorrend: Biblia → Könyv → Fejezet
        self.assertLess(f.index('class="bibliavalaszto"'), f.index('<div class="mufaj"'))
        self.assertLess(f.index('<div class="mufaj"'), f.index('id="fejezetracs"'))
        self.assertEqual(re.findall(r'<span class="biblia-csoport-cim">([^<]+)</span>', f), ['Magyar', 'Eredeti nyelv', 'Angol'])
        gombok = re.findall(r'<a class="biblia-gomb( itt)?" href="([^"]+)" data-biblia="(\w+)"', f)
        self.assertEqual([g[2] for g in gombok], [b.kod for b in bibliak.BIBLIAK])
        self.assertEqual([g[2] for g in gombok if g[0]], ['karoli'])
        cel = {g[2]: g[1] for g in gombok}
        self.assertEqual(cel['karoli'], '/1Moz/1')                  # a Károli útvonala változatlan, paraméter nélkül
        self.assertEqual(cel['tahot'], '/1Moz/1?biblia=tahot')
        self.assertEqual(cel['tagnt'], '/Mt/1?biblia=tagnt')         # az ÓSZ-ban nincs: a Biblia első fejezete
        for nincs in ('ASV', 'Targum', 'Vulgata', 'versenként'):
            self.assertNotIn(nincs, f)

    def test_karoli_utvonal_valtozatlan(self):
        h = self.h('/1Moz/1')
        self.assertIn('<p class="folyo" id="szoveg">', h)
        self.assertIn('<a class="konyvgomb itt" href="/1Moz" data-kk="1Móz"', h)
        self.assertNotIn('biblia=', self.szoveg(h))
        self.assertNotIn('class="biblia-jegy"', h)
        # ismeretlen kód: az alap (Károli), nem hiba
        self.assertIn('<span class="morzsa-biblia">Károli 1908 ·</span>', self.h('/1Moz/1?biblia=asv'))

    def test_minden_biblia_olvashato(self):
        for kod, ut, minta in (('modern', '/1Moz/1', 'Kezdetben'), ('tahot', '/1Moz/1', 'אֱלֹהִ֑ים'), ('lxx', '/1Moz/1', 'ἀρχῇ'),
                               ('kjv', '/1Moz/1', 'beginning'),
                               ('modern', '/Mt/1', 'Ábrahám'), ('tagnt', '/Mt/1', 'Βίβλος'), ('kjv', '/Mt/1', 'Abraham')):
            u = '%s?biblia=%s' % (ut, kod)
            h = self.h(u)
            sz = self.szoveg(h)
            self.assertIn(unicodedata.normalize('NFC', minta), unicodedata.normalize('NFC', html_modul.unescape(sz)), u)
            b = bibliak.BIBLIA[kod]
            self.assertIn('<span class="morzsa-biblia">%s ·</span>' % b.morzsa, h, u)
            self.assertIn('class="biblia-jegy"', h, u)
            linkek = re.findall(r'<a class="szo[^"]*" href="([^"]+)" data-strong="([HG]\d{4}[A-Z]?)"', sz)
            self.assertTrue(linkek, u)
            self.assertNotIn('&amp;amp;', sz, u)
            self.assertTrue(all('biblia=%s' % kod in l for l, _ in linkek), u)
            self.assertIn('szóra koppintva', h, u)
            # a fejezetrács és a lapozó a Bibliában marad
            self.assertIn('href="/%s/2?biblia=%s"' % (ut.split('/')[1], kod), h, u)

    def test_szopanel_a_biblia_szavarol(self):
        # TAHOT 1Móz 1:1 אֱלֹהִים → H0430: a szó-lap a Károli-vers kontextusával, a Bibliában maradva
        h = self.h('/1Moz/1/1?szo=H0430&ful=szo&biblia=tahot')
        self.assertIn('data-mod="szo"', h)
        self.assertIn('data-strong="H0430"', h)
        self.assertIn('data-bq="biblia=tahot"', h)
        r = self.c.get('/r/szo/H0430?ig=1Moz/1/1')
        self.assertEqual(r.status_code, 200)

    def test_strong_nelkuli_nincs(self):
        # a Strong nélküli szöveg nem választható: a régi kód az alapra (Károli) esik vissza, nem hiba
        for kod in ('targum', 'vulgata'):
            h = self.h('/Zsolt/23?biblia=%s' % kod)
            self.assertIn('<span class="morzsa-biblia">Károli 1908 ·</span>', h)
            self.assertNotIn('class="biblia-jegy"', h)
        # a TAHOT az Újszövetségben nem olvasható
        self.h('/Mt/1?biblia=tahot', 404)
        # az eltérő forrásszám a vers elején (LXX Zsolt 23 = LXX 22)
        self.assertIn('<span class="forras-versszam">LXX 22:1</span>', self.h('/Zsolt/23?biblia=lxx'))

    def test_kiadas_strong_reteg_nelkul(self):
        # a nyilvanos kiadásban a KJV Strong-címkéi kizártak (DT124): a KJV nem kerül a választóba, a címe 404
        app = app_keszit('nyilvanos')
        c = app.test_client()
        h = c.get('/1Moz/1').get_data(as_text=True)
        self.assertNotIn('data-biblia="kjv"', h)
        self.assertNotIn('data-biblia="bsb"', h)         # a BSB nem választható (F214: nem teljes)
        self.assertEqual(c.get('/1Moz/1?biblia=kjv').status_code, 404)

    def test_konyvracs_a_biblia_konyvei(self):
        f = self.fej(self.h('/1Moz/1?biblia=tahot'))
        konyvek = re.findall(r'<a class="konyvgomb[^"]*" href="([^"]+)" data-kk="([^"]+)"', f)
        # a héber ÓSZ csak az Ószövetség: az Újszövetség könyvei nincsenek a rácsban
        self.assertEqual(len(konyvek), 39)
        self.assertFalse({'Mt', 'Jel'} & {kk for _, kk in konyvek})
        self.assertTrue(all(h.endswith('?biblia=tahot') for h, _ in konyvek))
        self.assertIn('data-bq="?biblia=tahot"', f)


if __name__ == '__main__':
    unittest.main()
