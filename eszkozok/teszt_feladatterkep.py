#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_feladatterkep.py -- F53_FELADATTERKEP_BRIEF.md: az `eszkozok/feladatterkep.py`
tesztjei. Ideiglenes konyvtarban felepitett fixture-repo (git nelkul), plusz a
valodi repon futo, git-fuggo ellenorzesek (ezek git nelkul kimaradnak).

Futtatas: python eszkozok/teszt_feladatterkep.py
"""

import os
import re
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402
import feladatterkep as T  # noqa: E402


def brief(szam, kod, allapot, fugg=None, kov='/kovetkezo', fazis='1', ir=None, extra=''):
    sorok = ['---', 'feladat: %d' % szam, 'cim: Cim %s' % kod, 'kod: %s' % kod,
             'tipus: feladat', 'fazis: %s' % fazis, 'modell: sonnet',
             'allapot: %s' % allapot, 'ad: ad %s' % kod, 'kovetkezo: %s' % kov,
             'olvas: []', 'ir: [%s]' % (ir or 'ki/%s.txt' % kod.lower()),
             'munka: folyamat']
    if fugg:
        sorok.append('fugg: [%s]' % ', '.join(str(x) for x in fugg))
    sorok.append(extra) if extra else None
    sorok += ['---', '', '# %s' % kod, '']
    return '\n'.join(sorok)


MUNKATERV = """# Munkaterv

## 2. Döntési előfeltételek

| # | döntés | javasolt irány | melyik feladatot oldja fel |
| --- | --- | --- | --- |
| DT-X1 | Javasolt, még nincs felvéve | igen | TERV\\_EGY |
| DT-X2 | Már a DONTESEK-ben | nem | TERV\\_EGY |

## 4. Feladatlista

| # | név | cél | bemenet | kimenet | kis minta | függ | menet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | TERV\\_EGY | Egy tervezett feladat célja | x | y | z | ALFA, DT-X1 | 1 |
| — | ALFA | Már FELADATOK-sor, kimarad | x | y | z | — | 1 |

## 4a. Térkép

**Tervezett**

| # | fázis | mire ül |
| --- | --- | --- |
| TERV\\_EGY | 2. render | ALFA |

## 5. Hullámok

| hullám | feladatok | miért együtt | ⛔ a végén |
| --- | --- | --- | --- |
| 1 | ALFA; TERV\\_EGY | mert | kapu egy |
| után | #2 → BETA | mert | kapu két |
"""

DONTESEK = """# DONTESEK.md

| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |
|---|---|---|---|---|---|---|---|
| DT-A | #1 ALFA | nyitott kérdés | — | — | 🟡 | | |
| DT-B | #2 BETA | alkalmazásra vár | — | — | 🟢 | igen | |
| DT-C | #3 GAMMA | kész kérdés | — | — | ✅ | igen | `n.md` |
| DT-D | #3 GAMMA | szabad szöveg | tartalmaz | ilyet: |Δ| ≥ 10 | — | ✅ | igen | `n.md` |
| DT-X2 | TERV | már felvett | — | — | 🟡 | | |
"""

KARTYAK = ('kod\treszletes\troviden\tforras\n'
           'ALFA\tRészletes alfa.\tRöviden alfa.\tkezi-teszt\n'
           'NINCSILYEN\tSzöveg kártya nélkül.\tRöviden.\tkezi-teszt\n')


class FixtureAlap(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix='teszt_terkep_')
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.ir('F01_ALFA_BRIEF.md', brief(1, 'ALFA', 'nem_indult'))
        self.ir('F02_BETA_BRIEF.md', brief(2, 'BETA', 'fut'))
        self.ir('F03_GAMMA_BRIEF.md', brief(3, 'GAMMA', 'megallt', kov='Te: dönts'))
        self.ir('F04_DELTA_BRIEF.md', brief(4, 'DELTA', 'nem_indult', fugg=[1]))
        self.ir('F05_EPSZ_BRIEF.md', brief(5, 'EPSZ', 'lezarva'))
        self.ir('F06_ZETA_BRIEF.md', brief(6, 'ZETA', 'brief_kell'))
        self.ir('MUNKATERV.md', MUNKATERV)
        self.ir('DONTESEK.md', DONTESEK)
        os.makedirs(os.path.join(self.dir, 'eszkozok'))
        self.ir('eszkozok/feladatterkep_kartyak.tsv', KARTYAK)

    def ir(self, nev, szoveg):
        ut = os.path.join(self.dir, nev)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)

    def adat(self):
        return T.epit(self.dir, main_all={})


class TesztAllapotok(FixtureAlap):
    def test_allapot_besorolas(self):
        k = {x['kulcs']: x for x in self.adat()['kartyak']}
        self.assertEqual(k['ALFA']['allapot'], 'ready')
        self.assertEqual(k['BETA']['allapot'], 'run')
        self.assertEqual(k['GAMMA']['allapot'], 'stop')
        self.assertEqual(k['DELTA']['allapot'], 'wait')
        self.assertEqual(k['ZETA']['allapot'], 'idle')
        self.assertNotIn('EPSZ', k)           # kesz: nincs kartya

    def test_fugg_szoveg_a_feladatokbol(self):
        k = {x['kulcs']: x for x in self.adat()['kartyak']}
        self.assertEqual(k['DELTA']['fugg'], '#1')
        self.assertEqual(k['ALFA']['fugg'], '—')

    def test_csempek(self):
        cs = {c['kulcs']: c['db'] for c in self.adat()['csempek']}
        self.assertEqual((cs['ready'], cs['run'], cs['stop'], cs['wait']), (1, 1, 1, 1))
        self.assertEqual(cs['plan'], 1)       # TERV_EGY
        self.assertEqual(cs['dt'], 2)         # DT-A, DT-X2 (nyitott)


class TesztNemPotol(FixtureAlap):
    def test_leiras_nelkuli_kartya_jelolt(self):
        d = self.adat()
        k = {x['kulcs']: x for x in d['kartyak']}
        self.assertFalse(k['ALFA']['leiras_hiany'])
        self.assertEqual(k['ALFA']['roviden'], 'Röviden alfa.')
        for kod in ('BETA', 'GAMMA', 'DELTA', 'ZETA', 'TERV_EGY'):
            self.assertTrue(k[kod]['leiras_hiany'], kod)
            self.assertEqual((k[kod]['reszletes'], k[kod]['roviden']), ('', ''), kod)
            self.assertIsNone(k[kod]['leiras_forras'], kod)
        self.assertIn('BETA', d['kartya_tabla']['leiras_nelkul'])
        self.assertEqual(d['kartya_tabla']['felhasznalatlan'], ['NINCSILYEN'])

    def test_oszlopszam_eltero_dontes_ellenorizendo(self):
        dd = self.adat()['dontesek']
        self.assertEqual([x['id'] for x in dd['ellenorizendo']], ['DT-D'])
        ell = dd['ellenorizendo'][0]
        self.assertNotEqual(ell['oszlopszam'], ell['fejlec_oszlopszam'])
        self.assertEqual(ell['allapot'], 'ellenorizendo')

    def test_dontes_listak(self):
        dd = self.adat()['dontesek']
        self.assertEqual([x['id'] for x in dd['nyitott']], ['DT-A', 'DT-X2'])
        self.assertEqual([x['id'] for x in dd['alkalmazasra_var']], ['DT-B'])
        self.assertEqual(dd['kesz_db'], 1)    # DT-C
        # a MUNKATERV javasolt DT-je csak akkor, ha a DONTESEK-ben nincs
        self.assertEqual([x['id'] for x in dd['javasolt']], ['DT-X1'])

    def test_tervezett_csak_ha_nincs_a_feladatokban(self):
        k = {x['kulcs']: x for x in self.adat()['kartyak']}
        self.assertTrue(k['TERV_EGY']['tervezett'])
        self.assertEqual(k['TERV_EGY']['allapot'], 'plan')
        self.assertEqual(k['TERV_EGY']['fazis'], '2')
        self.assertFalse(k['ALFA']['tervezett'])      # a FELADATOK-sor nyer
        self.assertEqual(sum(1 for x in self.adat()['kartyak'] if x['kod'] == 'ALFA'), 1)

    def test_hullamok(self):
        h = self.adat()['hullamok']
        self.assertEqual([x['nev'] for x in h], ['1. hullám', 'Után'])
        self.assertEqual([(e['szoveg'], e['allapot']) for e in h[0]['elemek']],
                         [('ALFA', 'ready'), ('TERV_EGY', 'plan')])
        self.assertEqual(h[0]['kapu'], 'kapu egy')
        self.assertEqual([(e['szoveg'], e['allapot']) for e in h[1]['elemek']],
                         [('#2', 'run'), ('BETA', 'run')])

    def test_terkep(self):
        t = self.adat()['terkep']
        self.assertIn('T4["#4 DELTA"]:::wait', t)
        self.assertIn('T4 --> T1', t)
        self.assertIn('P_TERV_EGY --> T1', t)         # kod-fuggeses a MUNKATERV-bol
        self.assertNotIn('T5', t)                     # kesz feladat nincs a terkepen
        self.assertIn('T1 --> D_DT_A', t)             # a DONTESEK `Feladat` oszlopabol
        self.assertIn('D_DT_A{{"DT-A"}}:::dt', t)
        self.assertNotIn('DT_X1', t)                  # a javasolt (fel nem vett) DT nem csomopont


class TesztIdempotens(FixtureAlap):
    def test_ketszer_azonos_bajtok(self):
        a = T.json_szoveg(self.adat())
        b = T.json_szoveg(self.adat())
        self.assertEqual(a.encode('utf-8'), b.encode('utf-8'))
        self.assertFalse(re.search(r'\d{2}:\d{2}:\d{2}', a), 'futási időbélyeg a kimenetben')

    def test_main_ketszer_azonos(self):
        ki1, ki2 = os.path.join(self.dir, 'k1'), os.path.join(self.dir, 'k2')
        for ki in (ki1, ki2):
            T.main(['--gyoker', self.dir, '--kimenet', ki, '--csak-json'])
        with open(os.path.join(ki1, T.JSON_NEV), 'rb') as f1, \
                open(os.path.join(ki2, T.JSON_NEV), 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())


class TesztHtml(FixtureAlap):
    def test_html_ketszer_azonos_es_json_beagyazva(self):
        a = T.html_szoveg(self.adat())
        b = T.html_szoveg(self.adat())
        self.assertEqual(a.encode('utf-8'), b.encode('utf-8'))
        self.assertIn('<!-- GENERÁLT: eszkozok/feladatterkep.py — kézzel ne szerkeszd -->', a)
        self.assertIn('data-tema="dark"', a)                 # nem a data-theme
        self.assertNotIn('data-theme', a)
        self.assertIn('"kulcs":"ALFA"', a)                   # a beágyazott JSON
        self.assertFalse(re.search(r'\d{2}:\d{2}:\d{2}', a))

    def test_html_nem_zarja_le_a_scriptet_az_adat(self):
        d = self.adat()
        d['kartyak'][0]['cim'] = 'x </script><b>y'
        a = T.html_szoveg(d)
        self.assertEqual(a.count('</script>'), 4)             # a sablon négy scriptje
        self.assertIn('\\u003c/script>', a)

    def test_felirat_puszta_faziskod_helyett_cim(self):
        self.ir('F07_F07_BRIEF.md', brief(7, 'F07', 'nem_indult'))
        t = self.adat()['terkep']
        self.assertNotIn('#7 F07', t)
        self.assertIn('#7 Cim F07', t)                       # a cim eleje
        self.assertIn('#4 DELTA', t)                         # a valodi nev marad

    def test_elvalaszto_a_kartyan_belul_nem_log(self):
        h = T.html_szoveg(self.adat())
        self.assertNotIn('class="arrow"', h)
        self.assertIn('class="sep"', h)
        self.assertIn('const kov = D.sor[i+1]', h)           # az utolso kartya utan nincs

    def _md_js(self, bemenet):
        """A lap md() fuggvenye node-ban (ha nincs node: kihagyva)."""
        import json
        import subprocess
        if not shutil.which('node'):
            self.skipTest('nincs node')
        h = T.html_szoveg(self.adat())
        kod = '\n'.join(l for l in h.splitlines()
                        if re.match(r'(const esc|const MD|const md|const plain|const clip) ', l))
        js = kod + '\nconst be=%s;\nprocess.stdout.write(JSON.stringify(be.map(md)));' % json.dumps(bemenet)
        ut = os.path.join(self.dir, 'md_teszt.js')
        with open(ut, 'w', encoding='utf-8') as f:
            f.write(js)
        r = subprocess.run(['node', ut], capture_output=True, check=True)
        return json.loads(r.stdout.decode('utf-8'))

    def test_markdown_inline_xss_biztos(self):
        ki = self._md_js(['SQLITE\\_EPIT', '`kod`', '*(forrás: x)*', '**vastag**',
                          '<script>alert(1)</script>', '`<b>`', '*<img src=x onerror=1>*'])
        self.assertEqual(ki[0], 'SQLITE_EPIT')
        self.assertEqual(ki[1], '<code>kod</code>')
        self.assertEqual(ki[2], '<em>(forrás: x)</em>')
        self.assertEqual(ki[3], '<strong>vastag</strong>')
        self.assertEqual(ki[4], '&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertEqual(ki[5], '<code>&lt;b&gt;</code>')
        self.assertNotIn('<img', ki[6])

    def test_main_ket_kimenetet_ir(self):
        ki = os.path.join(self.dir, 'ki')
        T.main(['--gyoker', self.dir, '--kimenet', ki])
        self.assertTrue(os.path.isfile(os.path.join(ki, T.JSON_NEV)))
        self.assertTrue(os.path.isfile(os.path.join(ki, T.HTML_NEV)))


class TesztTsvSzabaly(unittest.TestCase):
    def test_csv_modul_nincs_importalva(self):
        ut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feladatterkep.py')
        with open(ut, encoding='utf-8') as f:
            forras = f.read()
        self.assertIsNone(re.search(r'^\s*(import\s+csv|from\s+csv\s+import)', forras, re.M))

    def test_kartya_tsv_fejlec_es_oszlopszam(self):
        ut = os.path.join(T.REPO, T.KARTYAK_TSV)
        with open(ut, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        self.assertEqual(sorok[0], 'kod\treszletes\troviden\tforras')
        kodok = []
        for sor in sorok[1:]:
            if sor:
                self.assertEqual(len(sor.split('\t')), 4, sor[:40])
                kodok.append(sor.split('\t')[0])
        self.assertEqual(len(kodok), len(set(kodok)), 'kettős kód a táblában')


@unittest.skipUnless(os.path.isdir(os.path.join(T.REPO, '.git'))
                     or os.path.isfile(os.path.join(T.REPO, '.git')), 'nincs git')
class TesztValodiRepo(unittest.TestCase):
    """A teljesseg ellenorzese a valodi repon (7.2): minden nyitott feladat es
    nem kesz dontes megjelenik."""

    @classmethod
    def setUpClass(cls):
        cls.main_all = F.main_allapotok(T.REPO)
        cls.adat = T.epit(T.REPO, main_all=cls.main_all)

    def test_minden_nyitott_feladat_kartya_azonos_allapottal(self):
        briefek = F.briefek_beolvas(T.REPO)
        by = {b.szam: b for b in briefek if b.szam is not None and b.fej}
        kartyak = {k['szam']: k for k in self.adat['kartyak'] if k['szam'] is not None}
        nyitott = [b for b in by.values()
                   if b.fej.get('tipus') in ('feladat', 'naplozas')
                   and F.statusz(b, self.main_all) != 'kesz']
        self.assertTrue(nyitott)
        for b in nyitott:
            self.assertIn(b.szam, kartyak, '#%d nincs kártya' % b.szam)
            self.assertEqual(kartyak[b.szam]['brief_allapot'], F.statusz(b, self.main_all))
        # a FELADATOK.md-be generalt tablak sorai (ugyanabbol a forrasbol)
        blokk = F.blokkok(briefek, T.REPO, main_all=self.main_all)
        for cel in ('fazis1', 'fazis2', 'folyamat'):
            for sor in blokk[cel].split('\n'):
                m = re.match(r'^\|\s*(\d+)\s*\|', sor)
                if m:
                    self.assertIn(int(m.group(1)), kartyak, 'FELADATOK #%s' % m.group(1))

    def test_minden_nem_kesz_dontes_megjelenik(self):
        with open(os.path.join(T.REPO, 'DONTESEK.md'), encoding='utf-8', newline='') as f:
            szoveg = f.read()
        jelen = set()
        for lista in ('nyitott', 'alkalmazasra_var', 'ellenorizendo'):
            jelen |= set(d['id'] for d in self.adat['dontesek'][lista])
        for sor in szoveg.split('\n'):
            if not sor.startswith('| DT') and not sor.startswith('| N'):
                continue
            azon = sor.split('|')[1].strip()
            cellak = T.sor_cellak(sor)
            if len(cellak) == 8 and cellak[5].strip().startswith('✅'):
                continue
            self.assertIn(azon, jelen, azon)

    def test_kartya_nelkuli_feladat_jelolt(self):
        for k in self.adat['kartyak']:
            if k['leiras_hiany']:
                self.assertEqual(k['reszletes'], '')
                self.assertEqual(k['roviden'], '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
