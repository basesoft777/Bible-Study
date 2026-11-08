#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_lektor_felulet.py -- F165: a lapnézet-építő (`lektor_felulet/lapnezet.py`) és a napló-hozzáfűző
(`lektor_felulet/lap_javitas_naplo.py`) egységtesztjei, ideiglenes könyvtárban (a repó adatát nem írja).

    python eszkozok/teszt_lektor_felulet.py
"""
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
import lap_javitas_naplo as J  # noqa: E402

FEJ = '\t'.join(J.FEJLEC)

MINTA = """# 📖 X-001 — Próba

## Kivonat

Első bekezdés.

Második bekezdés,
két sorban.

## 1. Előfordulások

### 1/a. Az igehelyek szövege

- tétel egy
- tétel kettő

```mermaid
graph TD

A --> B
```

| a | b |
|---|---|
| 1 | 2 |

## 1/b. Kizárt helyek

Kizárt.
"""


def _olvas(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


class Lapnezet(unittest.TestCase):
    def test_blokkok_es_jelek(self):
        bl = N.blokkok(MINTA)
        jelek = [b['jel'] for b in bl if b['jel']]
        self.assertEqual(jelek, ['Kivonat·1', 'Kivonat·2', '1·1', '1·2', '1·3', '1/b·1'])
        # a kódkerítésen belüli üres sor nem határ
        self.assertIn('A --> B', N.keres(bl, '1·2')['md'])
        self.assertIn('graph TD', N.keres(bl, '1·2')['md'])
        self.assertEqual(N.keres(bl, 'Kivonat·2')['md'], 'Második bekezdés,\nkét sorban.')
        self.assertEqual(N.keres(bl, '1·1')['hely'], '1. Előfordulások › 1/a. Az igehelyek szövege')
        # pontos jel kell; ponttal is elfogadja
        self.assertEqual(N.keres(bl, '1/b.1')['md'], 'Kizárt.')
        with self.assertRaises(ValueError):
            N.keres(bl, '9·9')

    def test_sablon_csak_nezet(self):
        s = _olvas(N.SABLON)
        for h in N.HELYORZOK:
            self.assertEqual(s.count(h), 1, h)
        # a nézet csak a lapot mutatja: nincs Claude-hívás, tár, önpublikálás
        for tilos in ("claude.use", 'sample', "'db'", '.publish(', 'textarea'):
            self.assertNotIn(tilos, s, tilos)

    def test_epit_munkafarol(self):
        html, meta, bl = N.epit('ISTENTISZT-001')
        self.assertTrue(sum(1 for b in bl if b['jel']) > 100)
        self.assertNotIn('__BLOKKOK__', html)
        self.assertEqual(html.count('</script>'), 2)  # a beágyazott md nem zárhatja le a scriptet
        # a blokkok együtt visszaadják a lap minden nem üres sorát
        sorok = [x for b in bl for x in b['md'].split('\n')]
        eredeti = [x for x in N.betolt('ISTENTISZT-001')[0].replace('\r\n', '\n').split('\n') if x.strip()]
        self.assertEqual([x for x in sorok if x.strip()], eredeti)

    def test_kimenet_reponkivul(self):
        mentes = sys.argv
        sys.argv = ['lapnezet.py', 'ISTENTISZT-001', os.path.join(N.ROOT, 'x.html')]
        try:
            with self.assertRaises(ValueError):
                N.main()
        finally:
            sys.argv = mentes
        self.assertFalse(os.path.exists(os.path.join(N.ROOT, 'x.html')))


def sor(**k):
    r = {'id': 'ISTENTISZT-001', 'hely': 'Kivonat·2', 'tipus': 'próza', 'gond': 'homályos', 'regi': 'a', 'uj': 'b',
         'javasolta': 'claude-opus-5-5', 'jovahagyta': 'felhasználó', 'datum': '2026.11.08',
         'proveniencia': 'scope=manual | forras=chat:/lap-javit ISTENTISZT-001 | ts=2026-11-08'}
    r.update(k)
    return r


class Naplo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='teszt_f165_')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _naplo(self, *sorok):
        ut = os.path.join(self.tmp, 'naplo.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(('# megjegyzés', FEJ) + sorok) + '\n')
        return ut

    def _uj(self, *rek):
        ut = os.path.join(self.tmp, 'uj.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join([FEJ] + ['\t'.join(r[k] for k in J.FEJLEC) for r in rek]) + '\n')
        return ut

    def test_hozzafuz_csak_bovit(self):
        naplo = self._naplo('\t'.join(sor(hely='h0', datum='2026.11.04')[k] for k in J.FEJLEC))
        eredeti = _olvas(naplo)
        self.assertEqual(J.hozzafuz(self._uj(sor()), naplo, {'ISTENTISZT-001'}), 1)
        self.assertTrue(_olvas(naplo).startswith(eredeti))
        with self.assertRaises(ValueError):  # ugyanaz a kulcs még egyszer
            J.hozzafuz(self._uj(sor()), naplo, {'ISTENTISZT-001'})

    def test_hibas_sor_iras_nelkul(self):
        naplo = self._naplo()
        eredeti = _olvas(naplo)
        for rossz in (sor(jovahagyta='claude-opus-5-5'), sor(gond='egyéb'), sor(tipus='?'), sor(id='NINCS-001')):
            with self.assertRaises(ValueError):
                J.hozzafuz(self._uj(rossz), naplo, {'ISTENTISZT-001'})
        self.assertEqual(_olvas(naplo), eredeti)


if __name__ == '__main__':
    unittest.main(verbosity=2)
