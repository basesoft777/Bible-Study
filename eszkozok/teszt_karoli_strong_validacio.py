#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — az emberi validáció mintájának és kiértékelőjének tesztjei.

A válaszfájlok kitaláltak (a tesztben generált műítéletek); valódi ellenőri ítélet
nincs bennük. A kimenet ideiglenes könyvtárba megy, a repón kívülre.

Futtatás: python eszkozok/teszt_karoli_strong_validacio.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_validacio_kiertekel as ki  # noqa: E402
import karoli_strong_validacio_minta as vm  # noqa: E402

SZKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong_validacio_kiertekel.py')


def _export(nev, minta, hash_, itelet_of):
    v = {}
    for r in minta:
        it = itelet_of(r)
        if it:
            v[r['tetel_id']] = {'itelet': it[0], 'hibatipus': it[1], 'helyes_forras': [], 'megjegyzes': 'teszt',
                                'karoli': len(it) > 2, 'karoli_megj': 'kitalált észrevétel' if len(it) > 2 else '',
                                'segedeszkoz': it[3] if len(it) > 3 else ''}
    return {'oldal': 'F175.V1', 'minta_hash': hash_, 'minta_meret': len(minta), 'ellenor': nev,
            'sorrend': [r['tetel_id'] for r in minta], 'valaszok': v}


class Statisztika(unittest.TestCase):
    def test_wilson(self):
        p, lo, hi = ki.wilson(0, 10)
        self.assertEqual(p, 0.0)
        self.assertAlmostEqual(lo, 0.0, places=6)
        self.assertAlmostEqual(hi, 0.2775, places=4)
        p, lo, hi = ki.wilson(95, 100)
        self.assertAlmostEqual(lo, 0.8882, places=3)
        self.assertAlmostEqual(hi, 0.9785, places=3)

    def test_kappa(self):
        self.assertAlmostEqual(ki.kappa([('a', 'a'), ('b', 'b')] * 5, ('a', 'b'))[0], 1.0)
        # klasszikus példa: 20 a/a, 5 a/b, 10 b/a, 15 b/b -> po=0.7, pe=0.5, kappa=0.4
        p = [('a', 'a')] * 20 + [('a', 'b')] * 5 + [('b', 'a')] * 10 + [('b', 'b')] * 15
        k, po, n = ki.kappa(p, ('a', 'b'))
        self.assertAlmostEqual(po, 0.7)
        self.assertAlmostEqual(k, 0.4)
        self.assertEqual(n, 50)

    def test_legnagyobb_maradek(self):
        d = vm.legnagyobb_maradek({'x': 1, 'y': 1, 'z': 1}, 10)
        self.assertEqual(sum(d.values()), 10)
        self.assertEqual(d, {'x': 4, 'y': 3, 'z': 3})


VAN_LETET = os.path.exists(ki.MINTA)


@unittest.skipUnless(VAN_LETET, 'a minta a repón kívüli letétben van (DT-F175vh)')
class Minta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.minta = ki.tabla(ki.MINTA)

    def test_meret_es_retegek(self):
        par = [r for r in self.minta if r['tipus'] == 'par']
        nelkul = [r for r in self.minta if r['tipus'] == 'parnelkuli']
        self.assertEqual(len([r for r in par if r['reszminta'] == 'alap']), 300)
        self.assertEqual(len([r for r in par if r['reszminta'] == 'tulminta']),
                         72 - len([r for r in par if r['reszminta'] == 'alap' and r['elteres'] == '1']))
        self.assertEqual(len([r for r in par if r['elteres'] == '1']), 72)   # a #172 összes modell-eltérése
        self.assertEqual(len(nelkul), 80)
        self.assertEqual(len([r for r in par if r['reszminta'] == 'nehez']), 45)
        self.assertEqual(len([r for r in self.minta if r['tipus'] == 'kimaradt']), 55)
        self.assertEqual(len({r['tetel_id'] for r in self.minta}), len(self.minta))
        self.assertNotIn('csali', {r['reszminta'] for r in self.minta})   # a csalik külön, a letétben
        self.assertEqual(len({r['csoport'] for r in par}), 7)
        self.assertEqual(len({r['csoport'] for r in nelkul}), 7)
        self.assertTrue(all(r['f172_id'] for r in par if r['reszminta'] in ('alap', 'tulminta')))

    def test_kiemeles_a_szon_all(self):
        for r in self.minta:
            self.assertEqual(r['hu_vers'][int(r['hu_kezdet']):int(r['hu_veg'])], r['hu_szo'], r['tetel_id'])
            if r['tipus'] == 'par':
                tok = json.loads(r['er_tokenek_json'])
                self.assertEqual(tok[int(r['er_sorszam']) - 1]['a'], r['er_szo'], r['tetel_id'])

    def test_utmutato_peldai_mintan_kivul(self):
        # az útmutató egyetlen példaverse sem szerepelhet a mintában vagy a csalik között (K1)
        import re
        versek = {r['vers'] for r in self.minta}
        if os.path.exists(ki.LETET_ALAP):
            _, cs = ki.tabla(ki.LETET_ALAP)
            versek |= {r['vers'] for r in cs}
        with open(os.path.join(ki.VALIDACIO, 'UTMUTATO.md'), encoding='utf-8') as f:
            szoveg = f.read()
        hivatkozott = set(re.findall(r'(\d?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6} \d+:\d+)', szoveg))
        self.assertGreater(len(hivatkozott), 5)
        self.assertEqual(sorted(hivatkozott & versek), [])

    def test_hash_fnv(self):
        # a JS-oldali FNV-1a (UTF-16 kódegységeken) Python-mása; az oldal értékével az Oldal-teszt veti össze
        self.assertEqual(len(ki.minta_hash(self.minta)), 8)


@unittest.skipUnless(VAN_LETET, 'a minta a repón kívüli letétben van (DT-F175vh)')
class Kiertekeles(unittest.TestCase):
    """Végponttól végpontig, kitalált ítéletekkel."""

    @classmethod
    def setUpClass(cls):
        _, cls.minta = ki.tabla(ki.MINTA)
        cls.h = ki.minta_hash(cls.minta)
        cls.tmp = tempfile.mkdtemp(prefix='ksval_teszt_')
        par = [r['tetel_id'] for r in cls.minta if r['tipus'] == 'par' and r['reszminta'] == 'alap']
        nelkul = [r['tetel_id'] for r in cls.minta if r['tipus'] == 'parnelkuli']
        cls.b_hibas = set(par[:10])           # B: 10 pár hibás
        cls.b_bizonytalan = set(par[10:12])   # B: 2 pár bizonytalan
        cls.a_hibas = set(par[:4])            # A: 4 pár hibás (ezekben B-vel egyezik)
        cls.kimaradt = set(nelkul[:3])        # mindkettő: 3 pár nélküli szónak van eredetije

        cls.karoli_a = set(par[20:23])        # A: 3 tételnél fordítói jelölő (helyes ítélettel)

        def a_of(r):
            t = r['tetel_id']
            if t in cls.karoli_a:
                return ('helyes', '', True, 'BDB')
            if t in cls.a_hibas:
                return ('hibas', 'rossz_forrasszo')
            if t in cls.kimaradt:
                return ('hibas', 'kimaradt_par')
            return ('helyes', '')

        def b_of(r):
            t = r['tetel_id']
            if t in cls.b_hibas:
                return ('hibas', 'folosleges_par')
            if t in cls.b_bizonytalan:
                return ('bizonytalan', '')
            if t in cls.kimaradt:
                return ('hibas', 'kimaradt_par')
            return ('helyes', '')

        cls.fa = os.path.join(cls.tmp, 'Teszt_A_valaszok.json')
        cls.fb = os.path.join(cls.tmp, 'Teszt_B_valaszok.json')
        for ut, nev, f in ((cls.fa, 'Teszt A', a_of), (cls.fb, 'Teszt B', b_of)):
            with open(ut, 'w', encoding='utf-8') as fh:
                json.dump(_export(nev, cls.minta, cls.h, f), fh, ensure_ascii=False)

    def _fut(self, *extra, fajlok=None):
        ki_dir = os.path.join(self.tmp, 'ki_%d_%d' % (len(extra), len(fajlok or [1, 2])))
        felallas = [] if (fajlok and len(fajlok) == 1) or any(x in extra for x in ('--kulso', '--szerzo')) else ['--ket-kulso']
        r = subprocess.run([sys.executable, SZKRIPT] + (fajlok or [self.fa, self.fb]) + ['--kimenet', ki_dir, '--csali-nelkul'] + felallas + list(extra),
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(ki_dir, 'kiertekeles.md'), encoding='utf-8') as f:
            md = f.read()
        _, elt = ki.tabla(os.path.join(ki_dir, 'eltero_tetelek.tsv'))
        return md, elt, ki_dir

    def test_eltero_es_pontossag(self):
        md, elt, ki_dir = self._fut()
        self.assertEqual(len(elt), 8)   # 6 hibás-vs-helyes + 2 bizonytalan
        self.assertIn('| A (Teszt A) | 300 | 296 | 4 | 0 | 98.67%', md)
        self.assertIn('| B (Teszt B) | 300 | 288 | 10 | 2 | 96.64%', md)
        self.assertIn('| B (Teszt B) · konzervatív | 300 | 288 | 10 | 2 | 96.00%', md)   # a bizonytalan hibásnak számít
        # döntés nélkül a döntött minta csak az egyező tételeket tartalmazza
        self.assertIn('| **döntött minta** | 292 | 288 | 4 | 0 |', md)
        self.assertIn('| A (Teszt A) | 80 | 77 | 3 | 0 | 3.75%', md)
        self.assertIn('döntésre vár: 8', md)
        # a fordítói jelölő külön: nem rontja a pontosságot, külön fájlban áll
        self.assertIn('| A (Teszt A) | 3 | 3 | 0 | 3 |', md)
        _, ks = ki.tabla(os.path.join(ki_dir, 'karoli_szabad_forditas.tsv'))
        self.assertEqual(sorted(r['tetel_id'] for r in ks), sorted(self.karoli_a))
        _, sg = ki.tabla(os.path.join(ki_dir, 'segedeszkoz.tsv'))
        self.assertEqual(sorted(r['tetel_id'] for r in sg), sorted(self.karoli_a))
        self.assertIn('| A (Teszt A) | 3 | BDB (3) |', md)
        # az új rétegek külön becsléssel
        self.assertIn('| A (Teszt A) | 45 | 45 | 0 | 0 | 100.00%', md)     # nehéz réteg
        self.assertIn('| A (Teszt A) | 55 | 55 | 0 | 0 | 0.00%', md)       # kimaradt párok: kimaradási arány
        # többszavas bontás: a döntött 292 pár egy- és többszavasra oszlik
        n1 = sum(1 for r in self.minta if r['tipus'] == 'par' and r['reszminta'] == 'alap' and not r['tobbszavas']
                 and r['tetel_id'] not in (self.b_hibas | self.b_bizonytalan) - self.a_hibas)
        self.assertIn('| egyszavas (1:1) | %d |' % n1, md)

    def test_harmadik_dontes_es_modell(self):
        _, elt, ki_dir = self._fut()
        # a harmadik döntés: minden eltérőnél "helyes"
        ut = os.path.join(self.tmp, 'dontes.tsv')
        with open(os.path.join(ki_dir, 'eltero_tetelek.tsv'), encoding='utf-8') as f:
            sorok = [s.rstrip('\n') for s in f]
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            for s in sorok:
                if s.startswith('#') or s.startswith('tetel_id'):
                    f.write(s + '\n')
                else:
                    m = s.split('\t')
                    m[ki.ELTERO_FEJ.index('dontes')] = 'helyes'
                    f.write('\t'.join(m) + '\n')
        md, _, _ = self._fut('--dontes', ut, '--modell-f172')
        self.assertIn('| **döntött minta** | 300 | 296 | 4 | 0 | 98.67%', md)
        self.assertIn('döntésre vár: 0', md)
        self.assertIn('| **döntött minta** · párok, alapminta | 300 |', md)   # a #172 mind a 300 párra ad ítéletet
        self.assertIn('| **döntött minta** · párok, a #172 72 eltérése | 72 |', md)

    def test_ketfazisu_becsles(self):
        n1, d, w = ki.f172_fazis1()
        # minden pár helyes -> 100%
        mind = {r['tetel_id']: 'helyes' for r in self.minta if r['tipus'] == 'par'}
        e, _ = ki.ketfazisu(self.minta, mind)
        self.assertAlmostEqual(e[0], 1.0)
        # a modell-eltérések mind hibásak, a többi helyes -> Σ W_h (1 − d_h/n'_h), vagyis a #172-es súlyozott arány
        it = {r['tetel_id']: ('hibas' if r['elteres'] == '1' else 'helyes') for r in self.minta if r['tipus'] == 'par'}
        e, _ = ki.ketfazisu(self.minta, it)
        vart = sum(w[h] * (1 - d.get(h, 0) / n1[h]) for h in n1)
        self.assertAlmostEqual(e[0], vart, places=9)
        self.assertLess(e[1], e[0])
        self.assertGreater(e[2], e[0])
        # konzervatív: a bizonytalan hibás
        it2 = dict(it)
        alap_egyezo = [r['tetel_id'] for r in self.minta if r['tipus'] == 'par' and r['reszminta'] == 'alap' and r['elteres'] == '0']
        it2[alap_egyezo[0]] = 'bizonytalan'
        self.assertLess(ki.ketfazisu(self.minta, it2, konzervativ=True)[0][0], ki.ketfazisu(self.minta, it2)[0][0])

    def test_kulso_es_hozzatartozo(self):
        md, elt, _ = self._fut('--kulso', '2')
        self.assertIn('B (Teszt B, külső)', md)
        self.assertIn('A (Teszt A, hozzátartozó)', md)
        self.assertNotIn('döntött minta', md)
        # a fő szám a külső ellenőré: a 2a táblában az ő sora áll elöl
        i_b = md.index('| B (Teszt B, külső) | 300 |')
        i_a = md.index('| A (Teszt A, hozzátartozó) | 300 |')
        self.assertLess(i_b, i_a)
        self.assertIn('| a közös blokk (csalik nélkül) | 300 |', md)   # kappa a közös blokkon, csalik nélkül
        self.assertEqual(len(elt), 8)

    def test_minimumvaltozat_csalival(self):
        # 200 alapminta-pár + a 72 eltérés + 10 kitalált csali (a minta egy szűkített másolata)
        fej, sorok = ki.tabla(ki.MINTA)
        alap = [r for r in sorok if r['tipus'] == 'par' and r['reszminta'] == 'alap' and r['elteres'] == '0'][:188]
        elter = [r for r in sorok if r['elteres'] == '1']
        csali = []
        for i, r in enumerate(alap[:10], 1):
            csali.append(dict(r, tetel_id='C%03d' % i, reszminta='csali', elteres='', kozos='0'))
        uj = alap + elter + csali
        ut = os.path.join(self.tmp, 'minimum_minta.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# kitalált minimumváltozat (teszt)\n' + '\t'.join(fej) + '\n')
            for r in uj:
                f.write('\t'.join(r[k] for k in fej) + '\n')
        h = ki.minta_hash(uj)
        fa = os.path.join(self.tmp, 'min_A.json')
        with open(fa, 'w', encoding='utf-8') as f:
            json.dump(_export('Min A', uj, h, lambda r: ('hibas', 'egyeb') if r['reszminta'] == 'csali' and r['tetel_id'] != 'C010'
                              else ('helyes', '')), f, ensure_ascii=False)
        md, _, _ = self._fut('--minta', ut, fajlok=[fa])
        self.assertIn('2d. Csalik', md)
        self.assertIn('| A (Min A) | 10 | 9 | 1 | 0 | 90.00%', md)
        self.assertNotIn('a küszöb', md)   # 9/10 a 80%-os küszöb fölött van
        n_alap = sum(1 for r in uj if r['reszminta'] == 'alap')
        self.assertIn('| A (Min A) | %d | %d | 0 | 0 | 100.00%%' % (n_alap, n_alap), md)   # a csali nem számít az alapmintába
        self.assertIn('Ebben a mintában nincs nehéz réteg.', md)

    def test_csali_letetbol(self):
        # kitalált letét: 3 mintapár csaliként, a minta fejlécében a letét SHA-256-jával
        import hashlib
        fej, sorok = ki.tabla(ki.MINTA)
        csalik = [dict(r, tetel_id='Z%03d' % i, reszminta='csali', kozos='0')
                  for i, r in enumerate([x for x in sorok if x['tipus'] == 'par'][:3], 1)]
        letet = os.path.join(self.tmp, 'letet.tsv')
        with open(letet, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# kitalált letét (teszt)\n' + '\t'.join(fej) + '\n')
            for r in csalik:
                f.write('\t'.join(r[k] for k in fej) + '\n')
        with open(letet, 'rb') as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        ut = os.path.join(self.tmp, 'minta_csalival.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# kitalált minta | csali: 3 tétel (csali_sha256=%s)\n' % sha + '\t'.join(fej) + '\n')
            for r in sorok:
                f.write('\t'.join(r[k] for k in fej) + '\n')
        egyutt = sorted(sorok + csalik, key=lambda r: r['tetel_id'])
        fa = os.path.join(self.tmp, 'csali_A.json')
        with open(fa, 'w', encoding='utf-8') as f:
            json.dump(_export('Csali A', egyutt, ki.minta_hash(egyutt),
                              lambda r: ('hibas', 'rossz_forrasszo') if r['reszminta'] == 'csali' else ('helyes', '')), f,
                      ensure_ascii=False)
        ki_dir = os.path.join(self.tmp, 'ki_csali')
        r = subprocess.run([sys.executable, SZKRIPT, fa, '--minta', ut, '--csali', letet, '--kimenet', ki_dir],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(ki_dir, 'kiertekeles.md'), encoding='utf-8') as f:
            md = f.read()
        self.assertIn('| A (Csali A) | 3 | 3 | 0 | 0 | 100.00%', md)
        # rossz letét (más SHA): elutasítás
        with open(letet, 'a', encoding='utf-8') as f:
            f.write('\n')
        r = subprocess.run([sys.executable, SZKRIPT, fa, '--minta', ut, '--csali', letet, '--kimenet', ki_dir],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(r.returncode, 0)

    def test_ember_gep_es_erzekenyseg(self):
        # kitalált fagyasztott gépi tábla az alapminta párjaira: 3 bíráló, mind „helyes”, kivéve az A által hibásnak
        # ítélt 4 párt, ahol 0 bíráló
        import hashlib
        alap = [r for r in self.minta if r['tipus'] == 'par' and r['reszminta'] == 'alap']
        ut = os.path.join(self.tmp, 'gepi.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# kitalált gépi tábla (teszt)\nvers\thu_sorszam\ter_sorszam\tbiralo_1\tbiralo_2\tbiralo_3\n')
            for r in alap:
                x = '0' if r['tetel_id'] in self.a_hibas else '1'
                f.write('\t'.join([r['vers'], r['hu_sorszam'], r['er_sorszam'], x, x, x]) + '\n')
        with open(ut, 'rb') as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        md, _, _ = self._fut('--gepi', ut, '--gepi-sha256', sha, fajlok=[self.fa])
        self.assertIn('## 8. Ember–gép eltérések (tájékoztató; a fő számot nem módosítja)', md)
        self.assertIn('A külső ellenőr 4 párt ítélt hibásnak (alapminta); ezek közül 0-t mind a(z) 3 modell-bíráló '
                      'helyesnek ítélte. A fordított eset 0 pár.', md)
        self.assertNotIn('alsó becslés', md)
        # érzékenység: p = 296/300, f = 0, m = 20% -> π = (p − m)/(1 − m) = 98.33%
        self.assertIn('| 2a = 98.67% | 0.00% | 20.00% | 98.33% |', md)
        self.assertIn('## 10. A „hibás” ítéletek együttjárása', md)
        # rossz SHA: elutasítás
        r = subprocess.run([sys.executable, SZKRIPT, self.fa, '--csali-nelkul', '--gepi', ut, '--gepi-sha256', '0' * 64,
                            '--kimenet', os.path.join(self.tmp, 'x3')], capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(r.returncode, 0)

    def test_masodik_ito_oldala(self):
        # a második ítélő oldala (közös blokk + az összes alapminta-pár) exportját is elfogadja
        resz = [r for r in self.minta if r['kozos'] == '1' or (r['tipus'] == 'par' and r['reszminta'] == 'alap')]
        self.assertEqual(sum(1 for r in resz if r['tipus'] == 'par' and r['reszminta'] == 'alap'), 300)
        fm = os.path.join(self.tmp, 'masodik.json')
        with open(fm, 'w', encoding='utf-8') as f:
            json.dump(_export('Második', resz, ki.minta_hash(resz), lambda r: ('helyes', '')), f, ensure_ascii=False)
        md, _, _ = self._fut('--kulso', '1', fajlok=[self.fa, fm])
        self.assertIn('| párok, alapminta | 300 |', md)   # az egyezés mind a 300 alappáron

    def test_szerzoi_es_egy_ellenor(self):
        md, _, _ = self._fut('--szerzo', '2')
        self.assertIn('B (Teszt B, szerző)', md)
        self.assertIn('A (Teszt A, külső)', md)
        self.assertNotIn('döntött minta', md)
        self.assertIn('## 4. A két ítélő egyezése', md)
        self.assertIn('döntnök nincs', md)
        r = subprocess.run([sys.executable, SZKRIPT, self.fa, self.fb, '--csali-nelkul', '--szerzo', '2', '--dontes', self.fa,
                            '--kimenet', os.path.join(self.tmp, 'x2')], capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(r.returncode, 0)   # szerzői ellenőrnél nincs harmadik döntés
        md, elt, _ = self._fut(fajlok=[self.fa])
        self.assertNotIn('## 4.', md)          # egy ellenőrnél nincs kappa
        self.assertEqual(len(elt), 0)
        self.assertIn('| A (Teszt A) | 300 | 296 | 4 | 0 | 98.67%', md)

    def test_rossz_hash_elutasitva(self):
        rossz = os.path.join(self.tmp, 'rossz.json')
        with open(self.fa, encoding='utf-8') as f:
            d = json.load(f)
        d['minta_hash'] = '0'
        with open(rossz, 'w', encoding='utf-8') as f:
            json.dump(d, f)
        r = subprocess.run([sys.executable, SZKRIPT, rossz, self.fb, '--csali-nelkul', '--ket-kulso', '--kimenet', os.path.join(self.tmp, 'x')],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(r.returncode, 0)


class Alaktan(unittest.TestCase):
    """A Macula-kódok olvasható alakja (eszkozok/karoli_strong_morf.py)."""

    def test_heber(self):
        import karoli_strong_morf as km
        self.assertEqual(km.heber('Vqp3ms'), 'ige, qal perfectum, E/3 hn.')
        self.assertEqual(km.heber('Ncfsc'), 'főnév, nn. e.sz. status constr.')
        self.assertEqual(km.heber('Sp2ms'), 'névmási rag, E/2 hn.')
        self.assertEqual(km.heber('Pdxms'), 'mutató névmás, hn. e.sz.')
        # a törzsbetű arámiban mást jelent; vegyes versben nem nevezzük meg
        self.assertEqual(km.heber('VPp3ms', km.arami_vers('Dán 5:23')), 'ige, itpaal perfectum, E/3 hn.')
        self.assertEqual(km.heber('VPp3ms', km.arami_vers('1Móz 1:1')), 'ige, pual perfectum, E/3 hn.')
        self.assertEqual(km.heber('VPp3ms', km.arami_vers('Dán 2:4')), 'ige, törzs: P perfectum, E/3 hn.')
        self.assertIsNone(km.heber('Xyz'))

    def test_gorog(self):
        import karoli_strong_morf as km
        self.assertEqual(km.gorog('V-PAP-NSM'), 'ige, praesens act. part., nom. e.sz. hn.')
        self.assertEqual(km.gorog('V-2AAI-3S'), 'ige, aoristus (2.) act. ind., E/3')
        self.assertEqual(km.gorog('T-GSF'), 'névelő, gen. e.sz. nn.')
        self.assertEqual(km.gorog('V-RAN-ATT'), 'ige, perfectum act. inf.')
        self.assertIsNone(km.gorog('Z-QQ'))

    def test_minta_tokenjei(self):
        _, minta = ki.tabla(ki.MINTA)
        tk = [x for r in minta for x in json.loads(r['er_tokenek_json'])]
        self.assertTrue(all(x['k'] for x in tk))                      # átírás mindenütt
        self.assertTrue(all(x['mh'] for x in tk if x['m']))           # minden meglévő kód megfejtve
        self.assertLess(sum(1 for x in tk if not x['m']) / len(tk), 0.05)


class Oldal(unittest.TestCase):
    """Az ellenorzo.html szkriptje Node-on: kitöltés, emlékeztető, export, betöltés tiszta állapotba,
    tételenkénti időbélyeges összefésülés, idegen minta és más ellenőr fájlja."""

    @unittest.skipUnless(shutil.which('node'), 'nincs node')
    def test_betoltes_es_osszefesules(self):
        proba = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong_validacio_oldal_proba.js')
        # az oldal a letét mappájában készül, a repón kívül (a csalik miatt); nélküle (pl. a CI-ben) a próba kimarad
        oldal = os.path.join(os.path.dirname(ki.LETET_ALAP), 'ellenorzo.html')
        if not os.path.exists(oldal):
            self.skipTest('nincs ellenőrző oldal a letétben')
        r = subprocess.run(['node', proba, oldal], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('RENDBEN', r.stdout)
        # az oldal minta-azonosítója = a kiértékelőé (különben a kiértékelő elutasítaná az exportot)
        # (a csalik a repón kívüli letétben vannak: letét nélkül, pl. a CI-ben, ez az összevetés kimarad)
        _, minta = ki.tabla(ki.MINTA)
        if not os.path.exists(ki.LETET_ALAP):
            self.skipTest('nincs letétfájl')
        minta = ki.csali_hozzaad(ki.MINTA, minta, ki.LETET_ALAP)
        self.assertIn('minta_hash: ' + ki.minta_hash(minta), r.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
