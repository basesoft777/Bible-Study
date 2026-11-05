#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_lektor_felulet.py -- F165: a lapnézet-építő (`lektor_felulet/lapnezet.py`) és a javaslat-feldolgozó
(`lektor_felulet/javaslatok.py`) egységtesztjei, ideiglenes könyvtárban (a repó adatát nem írja).

    python eszkozok/teszt_lektor_felulet.py
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HELY, 'lektor_felulet'))
sys.path.insert(0, HELY)
import lapnezet as N  # noqa: E402
import javaslatok as J  # noqa: E402

FEJ = '\t'.join(J.FEJLEC)
URL = 'https://claude.ai/artifact/TESZT'


def _olvas(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


def doc(**k):
    d = {'motivum': 'ISTENTISZT-001', 'hely': 'Kivonat', 'res': 'kivonat', 'forras_tipp': 'motivumok/X.md',
         'bekezdes': 'Az első mondat homályos. A második rendben.', 'regi': 'Az első mondat homályos.',
         'uj': 'Az első mondat világos.', 'ok': 'érthetőbb', 'gond': 'homályos', 'allapot': 'jóváhagyva',
         'javasolta': 'claude-opus-5-5', 'ts': '2026-11-05T10:00:00.000Z'}
    d.update(k)
    return d


class Lapnezet(unittest.TestCase):
    def test_kepessegek_nincs_onpublikalas(self):
        c = N.capabilities()
        self.assertEqual(set(c), {'sample', 'user', 'db'})
        self.assertNotIn('artifact', c)
        self.assertNotIn('self', c)
        self.assertEqual(c['db']['rules'], [{'path': 'javaslatok', 'read': 'view', 'write': 'owner'}])

    def test_sablon_helyorzok_es_szabalyok(self):
        with open(N.SABLON, encoding='utf-8') as f:
            s = f.read()
        for h in N.HELYORZOK:
            self.assertEqual(s.count(h), 1, h)
        # a lap önmagát nem írja át, a modell csak javasol
        self.assertNotIn("use('artifact')", s)
        self.assertNotIn('.publish(', s)
        self.assertIn("collection('javaslatok')", s)
        self.assertIn("allapot: 'jóváhagyva'", s)
        for g in ('homályos', 'pontatlan', 'szakszó', 'ellentmond az adatnak'):
            self.assertIn(g, s)

    def test_kezi_resek(self):
        t = ('# megj\nid\tres\tfejlec\tforras\ttanulmany\nA-001\tkivonat\t## Kivonat\ttanulmany\tmotivumok/A-001.md\n'
             'A-001\t2b\t### 2/b. X\tadat\t\nB-001\tkivonat\t## Kivonat\ttanulmany\tmotivumok/B-001.md\n')
        self.assertEqual(N.kezi_resek(t, 'A-001'), [{'fejlec': '## Kivonat', 'res': 'kivonat', 'forras': 'motivumok/A-001.md'}])

    def test_epit_munkafarol(self):
        html, meta = N.epit('ISTENTISZT-001')
        self.assertTrue(meta['kezi'])
        self.assertNotIn('__ADAT__', html)
        self.assertNotIn('</script>"', html)  # a beágyazott md nem zárhatja le a scriptet
        self.assertEqual(html.count('</script>'), 2)

    def test_kimenet_reponkivul(self):
        mentes = sys.argv
        sys.argv = ['lapnezet.py', 'ISTENTISZT-001', os.path.join(N.ROOT, 'x.html')]
        try:
            with self.assertRaises(ValueError):
                N.main()
        finally:
            sys.argv = mentes
        self.assertFalse(os.path.exists(os.path.join(N.ROOT, 'x.html')))


class Javaslatok(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='teszt_f165_')
        os.makedirs(os.path.join(self.tmp, 'motivumok'))
        with open(os.path.join(self.tmp, 'motivumok', 'X.md'), 'w', encoding='utf-8') as f:
            f.write('## Kivonat\n\nAz első mondat homályos. A második rendben.\n')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _be(self, docs):
        ut = os.path.join(self.tmp, 'be.json')
        with open(ut, 'w', encoding='utf-8') as f:
            json.dump(docs, f, ensure_ascii=False)
        return ut

    def test_dokumentum_alakok(self):
        self.assertEqual(J.dokumentumok([{'id': 'a', 'data': {'x': 1}}]), [('a', {'x': 1})])
        self.assertEqual(J.dokumentumok({'docs': [{'id': 'a', 'x': 1}]}), [('a', {'x': 1})])
        self.assertEqual(J.dokumentumok({'a': {'x': 1}}), [('a', {'x': 1})])

    def test_kiolvas_csere_es_tervezet(self):
        be = self._be([{'id': 'j1', 'data': doc()}, {'id': 'j2', 'data': doc(allapot='beírva')},
                       {'id': 'j3', 'data': doc(res='', forras_tipp='generált rész', ts='2026-11-05T11:00:00Z')}])
        ki = os.path.join(self.tmp, 'ki')
        r = J.kiolvas(be, URL, ki, root=self.tmp + '_masik')  # a kimenet a "repón" kívül
        self.assertEqual((r['osszes'], r['varo']), (3, 2))
        # a forrás a megadott gyökér alatt nincs: nincs csere
        self.assertEqual(r['csere'], 0)
        r = J.kiolvas(be, URL, os.path.join(self.tmp + '_ki'), root=self.tmp)
        self.assertEqual(r['csere'], 1)
        with open(os.path.join(self.tmp + '_ki', 'csere.tsv'), encoding='utf-8') as f:
            sorok = f.read().strip().split('\n')
        self.assertEqual(sorok[1].split('\t'), ['motivumok/X.md', 'Az első mondat homályos.', 'Az első mondat világos.'])
        with open(os.path.join(self.tmp + '_ki', 'naplo_tervezet.tsv'), encoding='utf-8') as f:
            t = [s.split('\t') for s in f.read().strip().split('\n')]
        self.assertEqual(t[0], J.FEJLEC)
        self.assertEqual([x[2] for x in t[1:]], ['próza', '?'])
        self.assertEqual(t[1][7], 'felhasználó')
        self.assertEqual(t[1][8], '2026.11.05')
        self.assertIn('forras=artifact:%s#javaslatok/j1' % URL, t[1][9])
        shutil.rmtree(self.tmp + '_ki')

    def test_kiolvas_hibas_javaslat_megall(self):
        be = self._be([{'id': 'j1', 'data': doc(gond='egyéb')}])
        with self.assertRaises(ValueError):
            J.kiolvas(be, URL, self.tmp + '_ki2', root=self.tmp)
        be = self._be([{'id': 'j1', 'data': doc(regi='nincs ilyen')}])
        with self.assertRaises(ValueError):
            J.kiolvas(be, URL, self.tmp + '_ki2', root=self.tmp)

    def test_javasolta_tier(self):
        self.assertEqual(J.javasolta(doc(javasolta='tier=complex')), 'claude (artifact, tier=complex)')
        self.assertEqual(J.javasolta(doc(javasolta='felhasználó')), 'felhasználó')

    def _naplo(self, *sorok):
        ut = os.path.join(self.tmp, 'naplo.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(('# megjegyzés', FEJ) + sorok) + '\n')
        return ut

    def _uj(self, sor):
        ut = os.path.join(self.tmp, 'uj.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(FEJ + '\n' + '\t'.join(sor[k] for k in J.FEJLEC) + '\n')
        return ut

    def test_hozzafuz(self):
        regi_sor = '\t'.join(['ISTENTISZT-001', 'h0', 'próza', 'homályos', 'a', 'b', 'claude-opus-5-5', 'felhasználó',
                              '2026.11.04', 'scope=manual | forras=chat:/lap-javit X | ts=2026-11-04'])
        naplo = self._naplo(regi_sor)
        eredeti = _olvas(naplo)
        sor = J.naplo_sor('j1', doc(), URL, 'próza')
        self.assertEqual(J.hozzafuz(self._uj(sor), naplo, {'ISTENTISZT-001'}), 1)
        uj = _olvas(naplo)
        self.assertTrue(uj.startswith(eredeti))
        # ugyanaz a kulcs még egyszer: megáll
        with self.assertRaises(ValueError):
            J.hozzafuz(self._uj(sor), naplo, {'ISTENTISZT-001'})

    def test_hozzafuz_osztalyozatlan_es_modell_jovahagyo(self):
        naplo = self._naplo()
        with self.assertRaises(ValueError):
            J.hozzafuz(self._uj(J.naplo_sor('j1', doc(), URL)), naplo, {'ISTENTISZT-001'})
        sor = J.naplo_sor('j1', doc(), URL, 'próza')
        sor['jovahagyta'] = 'claude-opus-5-5'
        with self.assertRaises(ValueError):
            J.hozzafuz(self._uj(sor), naplo, {'ISTENTISZT-001'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
