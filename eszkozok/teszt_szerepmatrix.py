#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_szerepmatrix.py -- F78: a lexikonoldal 2. (Szótári háttér)
szakaszának szerep-sorrendű váza és az üres blokk jelölése (DT-F78a B változat,
DT-F78b szűkített hatókör).

Ellenőrzi:
  - a `szotar_szerepek.tsv` 26 soros, a 13-14. szerep mindkét nyelven `javaslat`;
    a SEMA 2.13 szövege ezzel egyezik;
  - a 2. szakasz minden szerepe megjelenik, a tábla sorrendjében (nyelv szerint;
    a mindkét nyelven azonos sorok a "Nyelvfüggetlen szerepek" alatt);
  - minden `nincs adatosítva` / `javaslat` szerep gépi `<!-- ÜRES-BLOKK: ... -->`
    jelölőt és látható zárójeles sort kap; az `adatosítva` szerep ott, ahol van
    tartalma vagy hivatkozása (görög 1., 2., 4., 5., 6., 8., 9.), nem;
  - a TWOT/domén/kiejtés sor a saját szerepe alatt áll (nem a Strong-fejlécben);
  - a rokon szavak (S5) belső szerkezete változatlan;
  - szerephez nem rendelt szótár ValueError-t ad (nincs néma elhagyás);
  - a licenc-állapot nem romlik (a szerepmátrix projekt-adat).

    python eszkozok/teszt_szerepmatrix.py
"""

import io
import os
import re
import sys
import unicodedata
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import general as G
import lexikon_general as LG

ROOT = G.ROOT
SZEREP_FEJ_RE = re.compile(r'^#### (\d+)\. (.+)$', re.M)
UROS_RE = re.compile(r'^<!-- ÜRES-BLOKK: (.+?) \| (.+?) -->$', re.M)


def _tsv_sorok():
    sorok = []
    with io.open(os.path.join(G.ADAT, 'szotar_szerepek.tsv'), encoding='utf-8') as f:
        for sor in f.read().split('\n'):
            if not sor or sor.startswith('#'):
                continue
            sorok.append(sor.split('\t'))
    fejlec, adat = sorok[0], sorok[1:]
    return [dict(zip(fejlec, r)) for r in adat]


_cache = {}


def _blokk(motivum_id):
    if motivum_id not in _cache:
        _, mot = G.tsv_beolvas(G.MOTIVUMOK_TSV)
        _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        m = next(x for x in mot if x['id'] == motivum_id)
        sorai = G.elofordulasok_id_szerint(elo)[motivum_id]
        tokenek = LG.motivum_strong_tokenek(sorai)
        szoveg, tiszt, parok = LG.blokk_szocikkek(m, tokenek, sorai)
        _cache[motivum_id] = (szoveg, tiszt, parok, tokenek)
    return _cache[motivum_id]


def _szakaszok(szoveg):
    """{'Görög': ..., 'Héber': ..., 'Nyelvfüggetlen': ..., 'Rokon': ...} az ### címek szerint."""
    out = {}
    reszek = re.split(r'^(?=### )', szoveg, flags=re.M)
    for r in reszek:
        if r.startswith('### Görög szavak'):
            out['gorog'] = r
        elif r.startswith('### Héber szavak'):
            out['heber'] = r
        elif r.startswith('### Nyelvfüggetlen szerepek'):
            out['kozos'] = r
        elif r.startswith('### Rokon szavak'):
            out['rokon'] = r
    return out


class TestMatrixTabla(unittest.TestCase):
    def test_26_sor_es_13_14_javaslat(self):
        sorok = _tsv_sorok()
        self.assertEqual(len(sorok), 26)
        for sz in ('13', '14'):
            ny = sorted(r['nyelv'] for r in sorok if r['sorrend'] == sz)
            self.assertEqual(ny, ['gorog', 'heber'], sz)
            for r in sorok:
                if r['sorrend'] == sz:
                    self.assertEqual(r['allapot'], 'javaslat')
        # sorrend-kulcs egyedi nyelvenként
        kulcsok = [(r['nyelv'], r['sorrend']) for r in sorok]
        self.assertEqual(len(kulcsok), len(set(kulcsok)))

    def test_sema_egyezik(self):
        with io.open(os.path.join(G.ADAT, 'SEMA.md'), encoding='utf-8') as f:
            sema = f.read()
        i = sema.index('### 2.13 `szotar_szerepek.tsv`')
        resz = sema[i:i + 4000]
        self.assertIn('13 szerep × 2 nyelv = 26 sor', resz)
        self.assertNotIn('22 sor', resz)
        self.assertIn('13. a „Károli-megfelelők', resz)


class TestVazIstentiszt(unittest.TestCase):
    def setUp(self):
        self.szoveg, self.tiszt, self.parok, self.tokenek = _blokk('ISTENTISZT-001')
        self.sz = _szakaszok(self.szoveg)
        self.tabla = _tsv_sorok()

    def _nyelv_sorrend(self, ny):
        return [(int(r['sorrend']), r['szerep']) for r in
                sorted((r for r in self.tabla if r['nyelv'] == ny), key=lambda r: int(r['sorrend']))]

    def test_sorrend_es_teljesseg(self):
        g = {int(r['sorrend']): r for r in self.tabla if r['nyelv'] == 'gorog'}
        h = {int(r['sorrend']): r for r in self.tabla if r['nyelv'] == 'heber'}
        kozos = {n for n in g if n in h and all(g[n][k] == h[n][k] for k in ('szerep', 'forras', 'allapot'))}
        self.assertEqual(kozos, {12, 13, 14})
        for ny, kulcs in (('gorog', 'gorog'), ('heber', 'heber')):
            var = [(int(n), s) for n, s in SZEREP_FEJ_RE.findall(self.sz[kulcs])]
            self.assertEqual(var, [x for x in self._nyelv_sorrend(ny) if x[0] not in kozos], ny)
        var = [(int(n), s) for n, s in SZEREP_FEJ_RE.findall(self.sz['kozos'])]
        self.assertEqual(var, [x for x in self._nyelv_sorrend('gorog') if x[0] in kozos])

    def _blokk_szerep(self, kulcs, n):
        resz = self.sz[kulcs]
        m = re.search(r'^#### %d\. .*?(?=^#### |\Z)' % n, resz, re.M | re.S)
        self.assertIsNotNone(m, (kulcs, n))
        return m.group(0)

    def test_ures_blokk_jeloles(self):
        for r in self.tabla:
            n = int(r['sorrend'])
            kulcs = 'kozos' if n >= 12 else r['nyelv']
            if n >= 12 and r['nyelv'] == 'heber':
                continue  # a nyelvfüggetlen sor egyszer jelenik meg
            b = self._blokk_szerep(kulcs, n)
            vannak = UROS_RE.findall(b)
            if (r['nyelv'], n) in LG.SZEREP_KEZI_2B:
                # DT-F78c 3.: kézi 2/b hivatkozás, nem üres blokk
                self.assertEqual(vannak, [], (r['nyelv'], n))
                self.assertIn('*Hivatkozás:', b)
                self.assertIn('l. 2/b', b)
            elif r['allapot'] in ('nincs adatosítva', 'javaslat'):
                self.assertEqual(len(vannak), 1, (r['nyelv'], n, b[:200]))
                self.assertEqual(vannak[0][1], r['allapot'])
                self.assertIn('(üres blokk:', b)
                self.assertIn('nincs kitöltve gyenge vagy asszociatív anyaggal', b)

    def test_adatositott_szerep_nem_ures(self):
        # a görög 1., 2., 4., 5., 6., 8., 9. adatosítva és van tartalma/hivatkozása
        for n in (1, 2, 4, 5, 6, 8, 9):
            b = self._blokk_szerep('gorog', n)
            self.assertNotIn('ÜRES-BLOKK', b, n)
        # az 5., 6., 8., 9.: hivatkozás (S4)
        for n in (5, 6, 8, 9):
            self.assertIn('*Hivatkozás:', self._blokk_szerep('gorog', n))

    def test_heber_tbesh_nincs_sor_jelolve(self):
        # adatosítva, de a tokenekhez nincs TBESH-sor: nem néma, jelölt üres blokk
        # DT83 (lezárva): a TBESH marad a forrás (adatosítva); H7121 mutatója a BDB 2.c (DT-F42a),
        # H8034 `adatosítva, nincs bekötve` (a #9 köti be); nincs TBESH-szöveg, nincs új adatsor
        b = self._blokk_szerep('heber', 1)
        self.assertEqual(len(UROS_RE.findall(b)), 2)
        self.assertTrue(all(a == 'adatosítva, nincs bekötve' for _, a in UROS_RE.findall(b)))
        self.assertRegex(b, r'\*\*H7121\*\* · \*\(üres blokk: a H7121 alapjelentését a BDB 2\.c adja \(DT-F42a\)')
        # a 2. szerep BDB-tartalma változatlan (H7121 2.c és 3., H8034 részlet)
        b2 = self._blokk_szerep('heber', 2)
        for cim in ('##### BDB H7121 — 2.c. jelentés', '##### BDB H7121 — 3. jelentés', '##### BDB H8034 — (részlet)'):
            self.assertIn(cim, b2)
        self.assertRegex(b, r'\*\*H8034\*\* · \*\(üres blokk: adatosítva, nincs bekötve; a bekötés a #9 dolga')
        self.assertNotIn('\n> ', b)
        self.assertNotIn('meglévő BDB-sor', b)

    def test_heber_adatositott_szerep_nem_hamisan_ures(self):
        # héber 2. (BDB), 4. (SDBH), 6. (LXX, hivatkozás): adatosítva, van tartalom -> nincs ÜRES-BLOKK
        for n in (2, 4, 6):
            self.assertNotIn('ÜRES-BLOKK', self._blokk_szerep('heber', n), n)

    def test_hivatkozasi_celok_leteznek(self):
        # a hivatkozott szakaszok a lexikonoldal vázában (sablon) ténylegesen megvannak
        sablon = LG.VAZ_SABLON
        self.assertIn('## 1. Előfordulások', sablon)
        self.assertIn('### 2/b', sablon)
        self.assertIn('## 3. LXX-fordítói döntések', sablon)
        # a görög 9. hivatkozása az 1. szakasz UBS-jelentés oszlopára mutat: az oszlop létezik
        self.assertIn('UBS-jelentés', LG.SZEREP_HIVATKOZAS[('gorog', 9)])
        import inspect
        self.assertIn('| UBS-jelentés |', inspect.getsource(LG.blokk_elofordulasok))

    def test_forrasszoveg_nem_szivarog_nem_forras_szerepbe(self):
        # idézőblokk ('> ') csak a forrás-szerepekben lehet (görög 1., 2., 8.; héber 1., 2.)
        forras = set(LG.SZEREP_SZOTAR)
        for r in self.tabla:
            n = int(r['sorrend'])
            kulcs = 'kozos' if n >= 12 else r['nyelv']
            if n >= 12 and r['nyelv'] == 'heber':
                continue
            if (r['nyelv'], n) in forras:
                continue
            self.assertNotIn('\n> ', self._blokk_szerep(kulcs, n), (r['nyelv'], n))

    def test_sajat_sor_a_szerep_alatt(self):
        self.assertIn('**TWOT:** 2063', self._blokk_szerep('heber', 3))
        self.assertIn('**Szemantikai domén:**', self._blokk_szerep('gorog', 4))
        self.assertIn('**Szemantikai domén:**', self._blokk_szerep('heber', 4))
        self.assertIn(unicodedata.normalize('NFC', 'ἐπικαλέω (epikaleō)'),
                      unicodedata.normalize('NFC', self._blokk_szerep('gorog', 10)))
        # a Strong-fejléc nem marad a fő törzsben (a rokon szavakon kívül)
        for kulcs in ('gorog', 'heber', 'kozos'):
            self.assertNotRegex(self.sz[kulcs], r'(?m)^### [GH]\d{4}')
            self.assertNotRegex(self.sz[kulcs], r'(?m)^\*\*TWOT:\*\*')

    def test_forras_blokk_szoveg_valtozatlan(self):
        # a forrásonkénti belső render (hu-sor, forrás-sor) megvan
        self.assertIn('##### TBESG G1941 — 1. jelentés', self.sz['gorog'])
        self.assertIn('*Forrás: konkordancia/TBESG.txt*', self.sz['gorog'])
        self.assertIn('##### BDB H7121 — 2.c. jelentés', self.sz['heber'])
        self.assertIn('##### BDB H8034 — (részlet)', self.sz['heber'])

    def test_rokon_szavak_szerkezete_valtozatlan(self):
        r = unicodedata.normalize('NFC', self.sz['rokon'])
        self.assertIn(unicodedata.normalize('NFC', '#### G0994 — βοάω (boaō)'), r)
        self.assertIn('**TWOT:** —', r)
        self.assertIn('**Szemantikai domén:**', r)
        self.assertIn('##### LSJ G2564 — (részlet)', r)

    def test_licenc_nem_romlik(self):
        self.assertFalse(self.tiszt)
        self.assertIn(('adat/szotar_szerepek.tsv', LG.LC('projekt_adat')), self.parok)
        self.assertIn('adat/szotar_szerepek.tsv', self.szoveg.split('\n')[0])

    def test_nincs_kitoltes_gyenge_anyaggal(self):
        # a nem adatosított szerep alatt nincs idézőblokk (forrás-szöveg)
        for ny, n in (('gorog', 3), ('gorog', 7), ('heber', 5), ('heber', 8), ('heber', 9)):
            self.assertNotIn('\n> ', self._blokk_szerep(ny, n))


class TestVazTeremt(unittest.TestCase):
    def test_teremt002_szotari_resz(self):
        szoveg, tiszt, parok, tokenek = _blokk('TEREMT-002')
        sz = _szakaszok(szoveg)
        self.assertEqual(tokenek, ['H0922', 'H8414'])
        self.assertIn('nincs görög Strong-tokenje', sz['gorog'])
        self.assertIn('<!-- ÜRES-NYELV: gorog | nincs Strong-token -->', sz['gorog'])
        self.assertNotIn('ÜRES-NYELV', sz['heber'])
        self.assertNotRegex(sz['gorog'], SZEREP_FEJ_RE)
        h = [(int(n), s) for n, s in SZEREP_FEJ_RE.findall(sz['heber'])]
        tabla = sorted((r for r in _tsv_sorok() if r['nyelv'] == 'heber' and int(r['sorrend']) < 12),
                       key=lambda r: int(r['sorrend']))
        self.assertEqual(h, [(int(r['sorrend']), r['szerep']) for r in tabla])
        # lexikon_hivatkozasok-sor nincs: az 1. és 2. szerep adatosítva, de nincs sor -> jelölt üres blokk
        self.assertIn('ÜRES-BLOKK: Alapjelentés | adatosítva, nincs bekötve', sz['heber'])
        self.assertIn('#9', sz['heber'])  # a #9 köti be (a TBESH-t; DT83)
        self.assertIn('ÜRES-BLOKK: Mélységi szócikk | adatosítva, nincs bekötve', sz['heber'])
        self.assertNotIn('\n> ', sz['heber'])
        # a TWOT és a domén megvan, a tokenhez kötve
        self.assertIn('**H8414** · **TWOT:**', sz['heber'])

    def test_szerephez_nem_rendelt_szotar_hiba(self):
        from unittest import mock
        eredeti = LG.lexikon_hivatkozasok_ehhez

        def hamis(strong):
            sorok = eredeti(strong)
            if strong == 'H7121':
                s = dict(sorok[0])
                s['szotar'] = 'LSJ'  # héber tokenhez görög-szótár: szerephez nem rendelt
                return sorok + [s]
            return sorok
        with mock.patch.object(LG, 'lexikon_hivatkozasok_ehhez', hamis):
            fl, tb = {'adat/lexikon_hivatkozasok.tsv': set()}, set()
            with self.assertRaises(ValueError):
                LG.szerep_vaz(['H7121'], fl, tb)


if __name__ == '__main__':
    unittest.main(verbosity=2)
