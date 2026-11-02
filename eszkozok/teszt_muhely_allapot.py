#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: a muhely_allapot.py tesztjei -- a nyilvanos JSON csak feherlistas mezot hordoz; hianyzo/hibas mero nem zold."""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import muhely_allapot as M  # noqa: E402


def minta_belso():
    allapotok = ['zold', 'zold', 'zold', 'piros', 'piros', 'nincs_mero', 'hiba', 'piros']
    krit = []
    for i, al in enumerate(allapotok, 1):
        k = {'sorszam': i, 'nev': 'ellenoriz.py k%d' % i, 'allapot': al, 'szam': {'n': 3},
             'ertek': 'titkos hibaszöveg', 'reszlet': ['döntésre váró kérdés szövege'],
             'proveniencia': 'scope=x | forras=y | ts=z', 'olvasoi_nev': M.OLV_NEV[i],
             'olvasoi_allapot': M.OLV_ALLAPOT[al]}
        k['olvasoi_szoveg'] = M.olvasoi_kapu(k)
        krit.append(k)
    st = {'cim': 'C', 'tema': 'T', 'pardes_szint': 'Drash', 'terjedelem_szo': 1, 'kotet': None,
          'negativ_kriterium': 'NEG-KRIT', 'folerendelt_fogalom': 'FOLEREND', 'elofordulas_osz': 1, 'elofordulas_usz': 1, 'kapcsolatok_db': 0, 'forditasi_lefedettseg': 1.0,
          'lektori_kerdes': '3 nyitott', 'utolso_generalas_commit': 'abc', 'verzio': 'v1',
          'kotet_megjegyzes': 'nincs kötet-adat', 'kotet_olvasoi': M.OLV_KOTET}
    return {
        '_generalt': 'eszkozok/muhely_allapot.py — feed_belso.json', 'generalva': 't', 'commit': 'abc',
        'rendszer': 'r', 'elvetett_jeloltek_osszesen': 0,
        'merok_osszesen': {'motivum_db': 1, 'kesz_db': 0, 'kapu_zold': 3, 'kapu_ossz': 8, 'nyitott_jelolt': 4},
        'heti_tortenes': [{'datum': '2026-11-01', 'motivum': 'X-001', 'esemeny': 'jelölt-döntés: beépítve', 'db': 2,
                           'olvasoi_esemeny': '2 igehely bekerült a motívumba'}],
        'pr_hiba': 'belső', 'ellenoriz_hiba': 'belső',
        'motivumok': [{'id': 'X-001', 'cim': 'c', 'tema': 't', 'pardes_szint': 'p', 'allasfokozat': 'ellenőrzés',
                       'allasfokozat_olvasoi': M.OLV_ALLAS['ellenőrzés'], 'olvasoi_mondat': 'x vizsgálat alatt',
                       'olvasoi_mondat_nyilvanos': M.olvasoi_mondat_nyilvanos(2, 3, 3),
                       'kriteriumok': krit, 'zold_db': 3, 'ossz_db': 8, 'nyitott_jelolt_db': 4,
                       'elvetett_jelolt_db': 3, 'beepitett_jelolt_db': 1, 'stash': st,
                       'prémium_mező': 'PRÉMIUM', 'elvetett_jeloltek': ['x'], 'nyitott_pr': [{'szam': 1}],
                       'tsv_statusz': 'publikálható', 'új_mező_alapból_belső': 'x'}],
    }


# a nyilvános rétegben nem szerepelhet akadályt, hibát vagy nyitott munkát jelző szó (DT-F156j)
TILTOTT_SZAVAK = ('piros', 'munka van hátra', 'nincs mérő', 'nincs_mero', 'még nem vizsgáltuk', 'megállt', 'hiba',
                  'nyitott', 'vizsgálat alatt', 'vár', 'akadály', 'blokkol', 'nem teljesül', 'hiányzik',
                  'folyamatban', 'döntésre', 'szurke')


class Teszt(unittest.TestCase):
    def test_nyilvanos_csak_feherlista(self):
        ny = M.nyilvanos(minta_belso())
        self.assertTrue(set(ny) <= set(M.FEHERLISTA_TOP))
        m = ny['motivumok'][0]
        self.assertTrue(set(m) <= set(M.FEHERLISTA_MOTIVUM))
        for k in m['teljesult_lepesek']:
            self.assertTrue(set(k) <= set(M.FEHERLISTA_KRITERIUM))
        self.assertTrue(set(m['stash']) <= set(M.FEHERLISTA_STASH))
        # DT-F156e: a Stash leírása a negatív kritériumot és a fölérendelt fogalmat is hordozza
        self.assertEqual(m['stash']['negativ_kriterium'], 'NEG-KRIT')
        self.assertEqual(m['stash']['folerendelt_fogalom'], 'FOLEREND')
        self.assertEqual(set(ny['merok_osszesen']), {'motivum_db', 'kesz_db', 'kapu_zold', 'kapu_ossz'})
        szoveg = repr(ny)
        for tiltott in ('PRÉMIUM', 'döntésre váró', 'titkos hibaszöveg', 'új_mező_alapból_belső', 'pr_hiba',
                        'ellenoriz_hiba', "'nyitott_pr'", "'elvetett_jeloltek'", 'ellenoriz.py', 'jelölt-döntés',
                        "'esemeny'", "'kriteriumok'", 'nyitott_jelolt', 'lektori_kerdes'):
            self.assertNotIn(tiltott, szoveg)

    def test_nyilvanos_csak_elorehaladas(self):
        ny = M.nyilvanos(minta_belso())
        m = ny['motivumok'][0]
        # csak a teljesült lépés látszik (3 a 8-ból), a többi nem
        self.assertEqual([k['sorszam'] for k in m['teljesult_lepesek']], [1, 2, 3])
        # az állapotlánc semleges: kész / aktuális / következő
        self.assertEqual([x['allapot'] for x in m['lanc']], ['kesz', 'kesz', 'aktualis', 'kovetkezo', 'kovetkezo'])
        olvashato = repr(ny).lower()
        for szo in TILTOTT_SZAVAK:
            self.assertNotIn(szo, olvashato, szo)

    def test_olvasoi_szoveg_nem_tartalmaz_belso_szot(self):
        belso_szavak = ('gerinc', 'ellenoriz', 'futtat', 'nulla-diff', 'DT', 'nincs_mero', '.py', 'CI', 'E2', 'jelölt',
                        'tsv')
        szovegek = list(M.OLV_NEV.values()) + list(M.OLV_ALLAPOT.values()) + list(M.OLV_ZOLD.values()) +             list(M.OLV_NINCS.values()) + list(M.OLV_ALLAS.values()) + [M.OLV_KOTET]
        for sz in range(1, len(M.KRITERIUMOK) + 1):
            for al in ('zold', 'piros', 'nincs_mero', 'hiba'):
                szovegek.append(M.olvasoi_kapu({'sorszam': sz, 'allapot': al,
                                                'szam': {'n': 3, 'kiejtes': 1, 'fordit': 2, 'blokk': 1}}))
        for sz in szovegek:
            for szo in belso_szavak:
                self.assertNotIn(szo, sz, sz)

    def test_lektor_zart(self):
        self.assertTrue(M.lektor_zart({'allapot': 'megvalaszolva'}))
        self.assertFalse(M.lektor_zart({'allapot': 'nyitva'}))
        self.assertFalse(M.lektor_zart({'allapot': ''}))
        self.assertFalse(M.lektor_zart({}))

    def test_lektor_meroi_a_valos_tablan(self):
        # nem létező tábla -> nincs mérő
        self.assertEqual(M.kriterium_7('NEMLETEZO-999')['allapot'], M.NINCS)

    def test_motivumkozi_jelolt_nem_blokkol(self):
        self.assertTrue(M.blokkolo_jelolt({'dontes': 'nyitva', 'jelolt_tipus': 'elofordulas'}))
        self.assertFalse(M.blokkolo_jelolt({'dontes': 'nyitva', 'jelolt_tipus': 'motivumkozi'}))
        self.assertFalse(M.blokkolo_jelolt({'dontes': 'beépítve', 'jelolt_tipus': 'elofordulas'}))
        jel = [{'id': 'X-001', 'igehely': 'Róm 1:1', 'dontes': 'nyitva', 'jelolt_tipus': 'motivumkozi',
                'indoklas': 'x'}]
        k = M.kriterium_4('X-001', jel)
        self.assertEqual(k['allapot'], M.ZOLD)
        self.assertEqual(k['szam']['kozi'], 1)

    def test_jelmagyarazat_nem_kiejtes_koteles(self):
        hianyok = [(81, 'Jelmagyarázat és rövidítések', 'generált', 'י׳', 'első előfordulás', None),
                   (900, 'Kivonat', 'kézi', 'קָרָא', 'első előfordulás', None)]
        self.assertEqual([h[3] for h in M.kiejtes_szuro(hianyok)], ['קָרָא'])

    def test_feladat_blokkol_csak_sajat_fajl_es_sajat_pont(self):
        fej = {'allapot': 'megallt', 'ir': 'motivumok/X-001.md, naplok/y.md'}
        self.assertTrue(M.feladat_blokkol(fej, '4. lépés ⛔ X-001: döntés', 'X-001'))
        self.assertFalse(M.feladat_blokkol(fej, '4. lépés ⛔ Y-002: döntés', 'X-001'))
        self.assertFalse(M.feladat_blokkol(dict(fej, ir='naplok/X-001_valami.md'), '⛔ X-001', 'X-001'))
        self.assertFalse(M.feladat_blokkol(dict(fej, allapot='lezarva'), '⛔ X-001', 'X-001'))

    def test_motivum_kesz_nem_blokkol(self):
        # DT-F123n: a több motívumot író brief kész motívuma nem függő munka; a többi motívuma blokkol
        fej = {'feladat': '9', 'allapot': 'megallt', 'ir': '[motivumok/X-001.md, motivumok/Y-002.md]',
               'motivum_kesz': '[X-001]'}
        szoveg = '⛔ X-001: alpont · ⛔ Y-002: határ'.replace(' · ', '\n')
        self.assertFalse(M.feladat_blokkol(fej, szoveg, 'X-001'))
        self.assertTrue(M.feladat_blokkol(fej, szoveg, 'Y-002'))
        self.assertTrue(M.feladat_blokkol(dict(fej, motivum_kesz=''), szoveg, 'X-001'))
        # a feladat nyitott 🟡 DT-je, amely a kész motívumot nevezi meg, mégis blokkol; más feladaté vagy lezárt nem
        dt = [{'id': 'DT1', 'feladat': 9, 'nyitott': True, 'kerdes': 'X-001 alpontja?'}]
        self.assertTrue(M.feladat_blokkol(fej, szoveg, 'X-001', dt))
        self.assertFalse(M.feladat_blokkol(fej, szoveg, 'X-001', [dict(dt[0], nyitott=False)]))
        self.assertFalse(M.feladat_blokkol(fej, szoveg, 'X-001', [dict(dt[0], feladat=8)]))
        self.assertFalse(M.feladat_blokkol(fej, szoveg, 'X-001', [dict(dt[0], kerdes='Y-002?')]))

    def test_kriterium_8_kesz_motivum_tajekoztato(self):
        fejlecek = {9: {'feladat': '9', 'allapot': 'megallt', 'ir': '[motivumok/X-001.md]', 'motivum_kesz': '[X-001]',
                        '_fajl': 'F123_MIGRACIO2_BRIEF.md'}}
        e = M.kriterium_8('X-001', fejlecek, [])
        self.assertEqual(e['allapot'], M.ZOLD)
        self.assertTrue(any('motivum_kesz' in r for r in e['reszlet']))

    def test_masodik_kiadas_nem_blokkol(self):
        self.assertTrue(M.masodik_kiadas({'forras': 'lektor'}))
        self.assertTrue(M.masodik_kiadas({'forras': 'proza_lefedettseg'}))
        self.assertFalse(M.masodik_kiadas({'forras': 'hatar'}))
        sz = M.olvasoi_kapu({'sorszam': 7, 'allapot': 'zold', 'szam': {'n': 0, 'kiadas2': 3}})
        self.assertIn('2. kiadáshoz: 3 kérdés', sz)
        self.assertNotIn('2. kiadáshoz', M.olvasoi_kapu({'sorszam': 7, 'allapot': 'zold', 'szam': {'n': 0}}))

    def test_nyilvanos_szovegek_nem_akadalyt_jeloznek(self):
        szovegek = list(M.OLV_ALLAS.values()) + [M.OLV_KOTET] + M.LANC
        szovegek += [M.OLV_NEV[i] for i in M.OLV_NEV] + list(M.OLV_ZOLD.values())
        szovegek += [M.olvasoi_mondat_nyilvanos(33, 0, 8), M.olvasoi_mondat_nyilvanos(1, 9, 0)]
        szovegek += [M.olvasoi_esemeny({'esemeny': e, 'db': 2}) for e in
                     ('jelölt-döntés: beépítve', 'jelölt-döntés: elutasítva', 'állapot: publikálható (v3)')]
        for sz in szovegek:
            for szo in TILTOTT_SZAVAK:
                self.assertNotIn(szo, sz.lower(), sz)

    def test_a_valos_nyilvanos_json_csak_elorehaladas(self):
        ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'generalt', 'muhely',
                          'feed_nyilvanos.json')
        if not os.path.exists(ut):
            self.skipTest('nincs generált kimenet')
        import json
        with open(ut, encoding='utf-8') as f:
            d = json.load(f)
        for m in d['motivumok']:
            m.pop('stash', None)  # a Stash tartalmi leírása (negatív kritérium) szabad szöveg, nem állapotjelzés
        olvashato = json.dumps(d, ensure_ascii=False).lower()
        for szo in TILTOTT_SZAVAK:
            self.assertNotIn(szo, olvashato, szo)
        for m in d['motivumok']:
            self.assertNotIn('kriteriumok', m)
            self.assertTrue(all('olvasoi_szoveg' in k for k in m['teljesult_lepesek']))

    def test_olvasoi_mondat(self):
        self.assertEqual(M.olvasoi_mondat(33, 6, 92, 3),
                         '33 igehely feldolgozva, 6 vizsgálat alatt, 92 kizárva; a kilenc ellenőrzési lépésből 3 teljesül.')
        self.assertEqual(M.olvasoi_mondat(8, 0, 0, 1),
                         '8 igehely feldolgozva, nincs vizsgálat alatt álló igehely; a kilenc ellenőrzési lépésből 1 teljesül.')

    def test_kilenc_kapu(self):
        """DT-F156k: a 9. kapu az olvasói kapu; minden kapunak van olvasói neve és szövege."""
        self.assertEqual([k[0] for k in M.KRITERIUMOK], list(range(1, 10)))
        for sz in range(1, 10):
            self.assertIn(sz, M.OLV_NEV)
            self.assertIn(sz, M.OLV_ZOLD)
            self.assertIn(sz, M.OLV_NINCS)

    def test_kriterium_9_atnezes_nelkul_nem_zold(self):
        """A 9. kapu a felhasználó vizuális átnézése nélkül akkor sem zöld, ha a gépi kapu 0 BUKÁS-t adna."""
        eredeti = M.vizualis_atnezes
        try:
            M.vizualis_atnezes = lambda m: None
            k = M.kriterium_9('ISTENTISZT-001')
            self.assertEqual(k['allapot'], M.PIROS)
            self.assertEqual(k['szam']['atnezes'], 0)
            self.assertIn('emberi átnézése', M.olvasoi_kapu(dict(k, sorszam=9)))
        finally:
            M.vizualis_atnezes = eredeti

    def test_atnezes_ervenyessege(self):
        """SEMA 2.48: csak a lap mai commitjáról, a felhasználótól, szó szerinti idézettel érvényes."""
        c = 'abcdef1234567890'
        jo = {'id': 'X-001', 'lap_commit': 'abcdef1', 'ki': 'felhasználó', 'idezet': 'Igen, így jó.'}
        self.assertTrue(M.atnezes_ervenyes(jo, 'X-001', c))
        self.assertFalse(M.atnezes_ervenyes(dict(jo, idezet=' '), 'X-001', c))
        self.assertFalse(M.atnezes_ervenyes(dict(jo, ki='claude-opus-5-5'), 'X-001', c))
        self.assertFalse(M.atnezes_ervenyes(dict(jo, lap_commit='0000000'), 'X-001', c))  # a lap azóta változott
        self.assertFalse(M.atnezes_ervenyes(dict(jo, lap_commit='abc'), 'X-001', c))
        self.assertFalse(M.atnezes_ervenyes(jo, 'Y-001', c))

    def test_kiadott_lap_a_stashben_marad(self):
        """DT-F156m: a kiadott lap a Stash-ben marad; ha egy kapu piros, kimondja a következő kiadás javítandóit."""
        self.assertIsNone(M.kiadas_allapot(0, False))
        self.assertEqual(M.kiadas_allapot(1, True), 'Az 1. kiadás érvényes.')
        self.assertEqual(M.kiadas_allapot(1, False), 'Az 1. kiadás érvényes; a 2. kiadás javítandói nyitottak.')
        self.assertEqual(M.kiadas_allapot(4, False), 'A 4. kiadás érvényes; az 5. kiadás javítandói nyitottak.')
        self.assertEqual(M.allasfokozat({'statusz': 'publikálható'}, 8, 9, {}, kiadas=1), 'lezárt (stash)')
        self.assertEqual(M.allasfokozat({'statusz': 'feldolgozás alatt'}, 8, 9, {}, kiadas=0), 'feldolgozás')
        self.assertGreaterEqual(M.kiadas_szam('ISTENTISZT-001'), 1)
        self.assertIn('kiadas_allapot', M.FEHERLISTA_STASH)

    def test_kriterium_9_nincs_lap(self):
        self.assertEqual(M.kriterium_9('NEMLETEZO-999')['allapot'], M.NINCS)

    def test_olvasoi_esemeny(self):
        self.assertEqual(M.olvasoi_esemeny({'esemeny': 'állapot: publikálható (v3)', 'db': 1}),
                         'A motívum lapja új változatot kapott (3. változat)')

    def test_hianyzo_mero_nem_zold(self):
        k = M.kriterium_7('NEMLETEZO-999')
        self.assertEqual(k['allapot'], M.NINCS)
        self.assertNotEqual(k['allapot'], M.ZOLD)

    def test_hianyzo_hatar_fajl_nem_zold(self):
        self.assertEqual(M.kriterium_5('NEMLETEZO-999')['allapot'], M.NINCS)

    def test_nem_futott_ellenoriz_hiba(self):
        self.assertEqual(M.kriterium_1('X-001', None, 1, 'hiba')['allapot'], M.HIBA)

    def test_globalis_serules_nem_zold(self):
        blokkok = [{'nev': '1. x', 'verdikt': 'SÉRTÉS', 'szoveg': ['**1. x**: SÉRTÉS -- valami']}]
        self.assertEqual(M.kriterium_1('X-001', blokkok, 0, '')['allapot'], M.PIROS)

    def test_proveniencia_forma(self):
        self.assertRegex(M.prov('mero', 'X-001'), r'^scope=motivum:X-001 \| forras=mero \| ts=\d{4}-')

    def test_datum(self):
        self.assertEqual(M.datum_iso('2026.09.13'), '2026-09-13')
        self.assertEqual(M.datum_iso('2026-10-21T09:18Z'), '2026-10-21')
        self.assertIsNone(M.datum_iso('x'))


if __name__ == '__main__':
    unittest.main()
