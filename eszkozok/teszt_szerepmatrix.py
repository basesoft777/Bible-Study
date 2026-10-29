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

# F131 (DT272, DT371): az arany lapon (ISTENTISZT-001) a szótári gerinc a szerepmátrixot szűkíti
# (kapcsoló: LG.SZOTARI_GERINC_MOTIVUMOK). Ez a teszt a szerepmátrix ÁLTALÁNOS renderét vizsgálja
# (azt, amely a többi lapon él), az ISTENTISZT-001-et csak mint adatgazdag mintát használja, ezért a
# kapcsolót itt kikapcsolja. A gerinc-renderet az eszkozok/teszt_szotari_gerinc.py vizsgálja.
LG.SZOTARI_GERINC_MOTIVUMOK = frozenset()

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
            # a „kézi SECE-táblázatok a 2/b-ben” mutató megszűnt (ISTENTISZT-001 arany lap, 2026-10-29): a 2/b generált
            self.assertNotIn('l. 2/b', b, (r['nyelv'], n))
            if r['allapot'] in ('nincs adatosítva', 'javaslat'):
                self.assertEqual(len(vannak), 1, (r['nyelv'], n, b[:200]))
                self.assertEqual(vannak[0][1], r['allapot'])
                self.assertIn('(üres blokk:', b)
                self.assertIn('nincs kitöltve gyenge vagy asszociatív anyaggal', b)

    def test_adatositott_szerep_nem_ures(self):
        # a görög 1., 2., 4., 5., 6., 8., 9. adatosítva és van tartalma/hivatkozása
        for n in (1, 2, 4, 5, 6, 8, 9):
            b = self._blokk_szerep('gorog', n)
            self.assertNotIn('ÜRES-BLOKK', b, n)
        # a 6., 8., 9.: hivatkozás (S4); az 5. (F09 S2.4) az UBS DNTG + Mounce adatából épül
        for n in (6, 8, 9):
            self.assertIn('*Hivatkozás:', self._blokk_szerep('gorog', n))
        b5 = self._blokk_szerep('gorog', 5)
        self.assertIn('**G1941** · UBS DNTG: 4 jelentés', b5)
        self.assertIn('*Mounce (GK 2126):*', b5)

    def test_heber_tbesh_nincs_sor_jelolve(self):
        # F09 S2.2/S2.5b: a TBESH marad a forrás (adatosítva); a H7121 mutatója a BDB 2.c (DT-F42a,
        # a TBESH „részlet” sora nem kerül vissza), a H8034 TBESH-szövege megvan (DT187)
        b = self._blokk_szerep('heber', 1)
        self.assertEqual(len(UROS_RE.findall(b)), 1)
        self.assertTrue(all(a == 'adatosítva, nincs bekötve' for _, a in UROS_RE.findall(b)))
        self.assertRegex(b, r'\*\*H7121\*\* · \*\(üres blokk: a H7121 alapjelentését a BDB 2\.c adja \(DT-F42a\)')
        # a 2. szerep BDB-tartalma változatlan (H7121 2.c és 3., H8034 részlet)
        b2 = self._blokk_szerep('heber', 2)
        for cim in ('##### BDB H7121 — 2.c. jelentés', '##### BDB H7121 — 3. jelentés', '##### BDB H8034 — (részlet)'):
            self.assertIn(cim, b2)
        self.assertIn('##### TBESH H8034 — ', b)
        self.assertIn('1c) the Name (as designation of God)', b)
        # a H7121 TBESH „részlet” sora nem került vissza
        self.assertNotIn('##### TBESH H7121', b)
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
        # idézőblokk ('> ') csak a forrásszöveget idéző szerepekben lehet (görög 1., 2., 8.; héber 1., 2.; F09:
        # a 3. szerep tW-szövege mindkét nyelven, a héber 8. BDB-etimológiája)
        forras = set(LG.SZEREP_SZOTAR) | {('gorog', 3), ('heber', 3), ('heber', 8)}
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
        self.assertIn(unicodedata.normalize('NFC', 'ἐπικαλέω (epikaleó)'),
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
        self.assertIn(unicodedata.normalize('NFC', '#### G0994 — βοάω (boaó)'), r)
        self.assertIn('**TWOT:** —', r)
        self.assertIn('**Szemantikai domén:**', r)
        self.assertIn('##### LSJ G2564 — (részlet)', r)

    def test_licenc_nem_romlik(self):
        self.assertFalse(self.tiszt)
        self.assertIn(('adat/szotar_szerepek.tsv', LG.LC('projekt_adat')), self.parok)
        self.assertIn('adat/szotar_szerepek.tsv', self.szoveg.split('\n')[0])

    def test_nincs_kitoltes_gyenge_anyaggal(self):
        # a `javaslat` szerepek (12-14.) alatt nincs idézőblokk és nincs tartalom: csak jelölt üres blokk
        for n in (12, 13, 14):
            b = self._blokk_szerep('kozos', n)
            self.assertNotIn('\n> ', b)
            self.assertIn('ÜRES-BLOKK', b)
        # F09: nem marad `nincs adatosítva` szerep a táblában (a `javaslat` megengedett)
        self.assertEqual([r for r in self.tabla if r['allapot'] == 'nincs adatosítva'], [])


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
        self.assertIn('#12b', sz['heber'])  # a TEREMT-002 szótári bekötése a #12b-é (DT187)
        self.assertNotIn('#9 dolga', sz['heber'])
        self.assertIn('ÜRES-BLOKK: Mélységi szócikk | adatosítva, nincs bekötve', sz['heber'])
        for n in (1, 2):
            m = re.search(r'^#### %d\. .*?(?=^#### |\Z)' % n, sz['heber'], re.M | re.S)
            self.assertNotIn('\n> ', m.group(0), n)  # nincs szótári szöveg: a bekötés a #12b-é
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


class TestKiejtesF09(unittest.TestCase):
    """F09 S2.1 (K9): a 26 jóváhagyott héber lemma-kiejtés a kivételtáblában, a kódbeli KIEJT megszűnt."""

    def _kivetelek(self):
        sorok = []
        with io.open(os.path.join(G.ADAT, 'kiejtes_kivetelek.tsv'), encoding='utf-8') as f:
            for sor in f.read().split('\n'):
                if sor and not sor.startswith('#') and not sor.startswith('nyelv\t'):
                    sorok.append(sor.split('\t'))
        return sorok

    def test_26_heber_3_gorog_sor_egyedi_kulcs(self):
        sorok = self._kivetelek()
        self.assertEqual(sum(1 for r in sorok if r[0] == 'heber'), 26)
        self.assertEqual(sum(1 for r in sorok if r[0] == 'gorog'), 3)
        kulcsok = [(r[0], r[1]) for r in sorok]
        self.assertEqual(len(kulcsok), len(set(kulcsok)))

    def test_minden_jovahagyott_jelolt_ugyanazt_adja_vissza(self):
        jel = os.path.join(ROOT, 'naplok', 'SZOTAR_S1_heber_jeloltek.tsv')
        n = 0
        with io.open(jel, encoding='utf-8') as f:
            for sor in f.read().split('\n'):
                if not sor or sor.startswith('#') or sor.startswith('strong\t'):
                    continue
                m = sor.split('\t')
                lk = LG.lemma_kiejtes(m[0])
                self.assertIsNotNone(lk, m[0])
                self.assertEqual(lk[1], m[4], m[0])
                n += 1
        self.assertEqual(n, 26)

    def test_kodbeli_kiejt_tabla_megszunt(self):
        with io.open(os.path.join(ROOT, 'eszkozok', 'torzscikk_general.py'), encoding='utf-8') as f:
            self.assertEqual(f.read().count('KIEJT'), 0)

    def test_gorog_lemma_es_alak_magyaros(self):
        self.assertEqual(LG.lemma_kiejtes('G1941')[1], 'epikaleó')
        self.assertEqual(LG.gorog_magyaros('epikalesētai'), 'epikaleszétai')
        talalat = LG.kiejtes_ehhez('ApCsel 9:14', 'G1941')
        self.assertEqual(talalat[1], 'epikalúmenúsz')
        # héber alak: a STEP-átírás változatlan
        self.assertEqual(LG.kiejtes_ehhez('1Móz 4:26', 'H7121')[1], "k.Ro'")

    def test_heber_kiejtes_ket_azonos_step_atirasu_lemma(self):
        # H7496 és H7497 STEP-átírása azonos (ra.pah), a lemma-kulcs különbözteti meg
        self.assertEqual(LG.lemma_kiejtes('H7496')[1], 'refáím')
        self.assertEqual(LG.lemma_kiejtes('H7497')[1], 'ráfá')


def _nfc(s):
    return unicodedata.normalize('NFC', s)


class TestSeceMounceF09(unittest.TestCase):
    """F09 S2.4: SECE (7. szerep, mindkét nyelven) és Mounce (görög 5. szerep kiegészítője); DT189."""

    def _szerep(self, motivum_id, nyelv, n):
        szoveg = _blokk(motivum_id)[0]
        sz = _szakaszok(szoveg)[nyelv]
        m = re.search(r'^#### %d\. .*?(?=^#### |\Z)' % n, sz, re.M | re.S)
        return m.group(0)

    def test_sece_lista_szo_szerint_2b_mutato_nelkul(self):
        g = self._szerep('ISTENTISZT-001', 'gorog', 7)
        self.assertIn(_nfc('**G1941** · SECE — héber megfelelők (8): זָכַר, מָצָא, נָקַב, עָשָׂה, קָרָא, שׂוּם, שָׁכַן, שֻׁם'), _nfc(g))
        self.assertNotIn('ÜRES-BLOKK', g)
        # a „kézi SECE-táblázatok a 2/b-ben” mutató megszűnt (ISTENTISZT-001 arany lap, 2026-10-29): a 2/b generált
        self.assertNotIn('l. 2/b', g)
        self.assertNotIn('kézi SECE', g)
        h = self._szerep('ISTENTISZT-001', 'heber', 7)
        self.assertIn(_nfc('**H8034** · SECE — görög megfelelők (6): θρόνος, καλέω, καλός, καύχημα, ὄνομα, Σήμ'), _nfc(h))
        self.assertEqual([_nfc(x) for x in LG.sece_megfelelok('H7121')].count(_nfc('ἐπικαλέομαι')), 1)  # ismétlés nélkül

    def test_sece_hianyzo_lista_nem_targyalja(self):
        b = self._szerep('KIRALY-001', 'gorog', 7)
        self.assertIn('**G0282** · *a forrás nem tárgyalja* *(SECE: nincs héber megfelelő-lista)*', b)
        self.assertIsNone(LG.sece_megfelelok('G0282'))

    def test_mounce_glossza_jelolt_fordításra_var(self):
        b = self._szerep('ISTENTISZT-001', 'gorog', 5)
        self.assertIn(_nfc('*Mounce (GK 2126):* pluperfect, ἐπεκέκλητο (3 sg), to call on'), _nfc(b))
        self.assertIn('*(fordításra vár)*', b)
        self.assertEqual(LG.mcged_sor('G0012')['gk_szam'], 'G50012')
        # az UBS DNTG magyar glosszája a gyorsítótárból jön, ahol van
        self.assertIn('| hívni; nevezni |', b)


class TestLabjegyzetF09(unittest.TestCase):
    """F09 S2.7 / K11: kötelező forrásmegjelölések a kolofonban, szó szerint."""

    @classmethod
    def setUpClass(cls):
        _, mot = G.tsv_beolvas(G.MOTIVUMOK_TSV)
        _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        m = next(x for x in mot if x['id'] == 'ISTENTISZT-001')
        sorai = G.elofordulasok_id_szerint(elo)['ISTENTISZT-001']
        blokkok, _ = LG.render_lexikon_egy_id(m, sorai, G.konyv_sorrend_betolt(), set())
        cls.kolofon = blokkok['kolofon']
        cls.idezes = blokkok['idezes']

    def test_ubs_mondatok_szo_szerint(self):
        self.assertIn('(UBS Dictionary of Biblical Hebrew © United Bible Societies, 2023.  Adapted from '
                      'Semantic Dictionary of Biblical Hebrew © 2000-2023 United Bible Societies.)', self.kolofon)
        self.assertIn('(UBS Dictionary of New Testament Greek, © United Bible Societies, 2023.', self.kolofon)

    def test_mounce_twot_tw(self):
        self.assertIn('Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, '
                      'www.teknia.com/greek-dictionary', self.kolofon)
        self.assertIn('TWOT: Theological Wordbook of the Old Testament — csak a szócikk száma', self.kolofon)
        self.assertIn('The original work by unfoldingWord is available from unfoldingword.org/utw', self.kolofon)
        self.assertIn('Módosítás:', self.kolofon)  # a módosítás jelezve
        self.assertIn('CC BY-SA 4.0', self.kolofon)

    def test_unfoldingword_vedjegy_nem_szerepel(self):
        self.assertNotIn('®', self.kolofon)
        self.assertNotIn('®', self.idezes)
        self.assertNotIn('unfoldingWord®', _blokk('ISTENTISZT-001')[0])

    def test_lxx_parok_forrasmegjeloles(self):
        self.assertIn('lxx-morph, © Seth Kushniryk, CC BY 4.0', self.kolofon)

    def test_stepbible_egyszer_kulon_sorban(self):
        # a licencsor „.; ” határral fűzi az lxx-morph mögé; a kolofonban önálló, egyszeri sor
        stepbible = ('*Data created by www.STEPBible.org based on work at Tyndale House Cambridge '
                     '(CC BY 4.0)*')
        self.assertEqual(self.kolofon.count('Data created by www.STEPBible.org'), 1)
        self.assertIn('\n' + stepbible + '\n', self.kolofon + '\n')
        self.assertNotIn('.;', self.kolofon)
        self.assertIn('*lxx-morph, © Seth Kushniryk, CC BY 4.0, github.com/OpenScriptorium/lxx-morph.*',
                      self.kolofon)

    def test_megjelolesek_dolt_sora_lezart(self):
        # minden megjelölés-sor `*`-gal nyit és zár (a TWOT-sor is)
        for sor in self.kolofon.split('\n'):
            if sor.startswith('*') and not sor.startswith('**'):
                self.assertTrue(sor.rstrip().endswith('*'), sor)
        twot = [s for s in self.kolofon.split('\n') if s.startswith('*TWOT:')]
        self.assertEqual(len(twot), 1)
        self.assertTrue(twot[0].endswith('nem idézi.*'), twot[0])

    def test_megjeloles_reszek(self):
        self.assertEqual(LG.megjeloles_reszek('A, b.; Data created by X (CC BY 4.0)'),
                         ['A, b.', 'Data created by X (CC BY 4.0)'])
        self.assertEqual(LG.megjeloles_reszek('Egy mondat; vesszővel tovább.'),
                         ['Egy mondat; vesszővel tovább.'])


class TestTbeshF09(unittest.TestCase):
    """F09 S2.2 / S2.5b: a héber 1. szerep (TBESH) és a H8034 bekötése (DT187)."""

    def test_h8034_sor_szo_szerinti_a_forrasbol(self):
        sorok = [r for r in LG.lexikon_hivatkozasok_ehhez('H8034') if r['szotar'] == 'TBESH']
        self.assertEqual(len(sorok), 1)
        r = sorok[0]
        self.assertEqual((r['entry_id'], r['jelentes_szam'], r['forrasfajl']),
                         ('H8034', 'teljes', 'konkordancia/TBESH.txt'))
        raw = None
        with io.open(LG.TBESH_TXT, encoding='utf-8') as f:
            for sor in f:
                if sor.startswith('H8034\t'):
                    raw = sor.rstrip('\r\n').split('\t')[-1]
        tiszta = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw)).strip()
        self.assertIn(r['szoveg_en'], tiszta)

    def test_teremt002_tokenekhez_nincs_hivatkozas_sor(self):
        # DT187 (2): a TEREMT-002 szótári bekötése a #12b-é, adatsort a #9 nem ír
        for t in ('H8414', 'H0922'):
            self.assertEqual(LG.lexikon_hivatkozasok_ehhez(t), [], t)

    def test_konszolidalt_pontos_strong_sor_es_nem_targyalja(self):
        szoveg = _blokk('HAMART-001')[0]
        heber = _szakaszok(szoveg)['heber']
        m = re.search(r'^#### 1\. .*?(?=^#### |\Z)', heber, re.M | re.S).group(0)
        self.assertIn('##### TBESH H0127 — (konszolidált szócikk)', m)
        # DT-F09h kiegészítés: a betűutótagos alszócikk (H2403a/b) jelölten a blokkba kerül (D38)
        self.assertIn('##### TBESH H2403a — (konszolidált szócikk; alszócikk: H2403a)', m)
        self.assertIn('##### TBESH H2403b — (konszolidált szócikk; alszócikk: H2403b)', m)

    def test_alszocikk_bekerul_szemelynev_kimarad_hianyzo_nem_targyalja(self):
        # H2403: a/b alszócikk (közszó) bekerül
        self.assertEqual([r['strong'] for r in LG.tbesh_sorok_tokenhez('H2403')], ['H2403a', 'H2403b'])
        # H1121: a H1121a (ben, közszó) bekerül, a H1121b (Beno, személynév, N:N-M-P) kimarad
        self.assertEqual([r['strong'] for r in LG.tbesh_sorok_tokenhez('H1121')], ['H1121a'])
        m = _blokk('MENNY-001')[0]
        self.assertIn('alszócikk: H1121a', m)
        self.assertNotIn('H1121b', m)
        # az öt érintett token egyikénél sincs hamis „nem tárgyalja” a TBESH-nél
        for tok in ('H2403', 'H7451', 'H1121', 'H2416'):
            self.assertTrue(LG.tbesh_sorok_tokenhez(tok), tok)
            self.assertTrue(LG.szerep_token_adat_van('heber', 1, tok), tok)
        self.assertEqual([r['strong'] for r in LG.tbesh_sorok_tokenhez('H7451')], ['H7451a', 'H7451b', 'H7451c'])
        self.assertEqual([r['strong'] for r in LG.tbesh_sorok_tokenhez('H2416')], ['H2416a', 'H2416b', 'H2416c', 'H2416d', 'H2416e'])
        # H7497: mind tulajdonnév (N:) -> kiesik, de nem „nem tárgyalja”, hanem pontos jelzés
        self.assertEqual(LG.tbesh_sorok_tokenhez('H7497'), [])
        self.assertEqual(LG.tbesh_csak_tulajdonnev('H7497'), ['H7497a', 'H7497b'])
        ctx7 = {'fl': {}, 'szerep': 'Alapjelentés'}
        out7 = LG._tartalom_heber_tbesh('heber', 1, ['H7497'], {'H7497': {'forras_blokkok': []}}, ctx7)
        self.assertEqual(out7, ['**H7497** · *csak tulajdonnév-alszócikk: H7497a, H7497b* *(TBESH)*'])
        self.assertNotIn('nem tárgyalja', out7[0])
        sor = {'allapot': 'adatosítva', 'sorrend': '1', 'forras': 'TBESH'}
        self.assertEqual(LG.szerep_lefedettseg_cella('heber', sor, 'H7497'), 'csak tulajdonnév-alszócikk: H7497a, H7497b')
        # ténylegesen hiányzó token: marad a „nem tárgyalja”
        self.assertEqual(LG.tbesh_sorok_tokenhez('H9998'), [])
        ctx = {'fl': {}, 'szerep': 'Alapjelentés'}
        out = LG._tartalom_heber_tbesh('heber', 1, ['H9998'], {'H9998': {'forras_blokkok': []}}, ctx)
        self.assertEqual(out, ['**H9998** · %s *(TBESH)*' % LG.NEM_TARGYALJA])


class TestTbeshVerziozottF09(unittest.TestCase):
    """DT-F09h: a verziózott kimenet csak a TBESH.txt-ből dolgozik; a gitignore-olt _nyers/ fájl hiánya nem hiba."""

    def setUp(self):
        self._regi = (LG.TBESH_HELYI_LEXICON, LG._tbesh_konsz_cache, LG._tbesh_konsz_mod, LG._U.TBESH_KONSZOLIDALT)
        LG._tbesh_konsz_cache = None

    def tearDown(self):
        LG.TBESH_HELYI_LEXICON, LG._tbesh_konsz_cache, LG._tbesh_konsz_mod, LG._U.TBESH_KONSZOLIDALT = self._regi

    def test_hianyzo_nyers_fajl_nem_hiba(self):
        LG._U.TBESH_KONSZOLIDALT = os.path.join(os.path.dirname(__file__), 'nincs_ilyen_nyers', 'x.tsv')
        LG.TBESH_HELYI_LEXICON = True   # még helyi kéréssel sem hiba, ha a fájl nincs meg: TBESH.txt-re esik vissza
        sorok = LG.tbesh_konszolidalt().get('H0127', [])
        self.assertTrue(sorok)
        self.assertTrue(all(r['forras'] == 'txt' and r['_fajl'] == 'konkordancia/TBESH.txt' for r in sorok))

    def test_verziozott_mod_txt_forras_es_nincs_lexicon_jelzo(self):
        LG.TBESH_HELYI_LEXICON = False
        for r in [x for v in LG.tbesh_konszolidalt().values() for x in v]:
            self.assertEqual(r['forras'], 'txt')
        for mid in ('HAMART-001', 'TEREMT-001', 'MENNY-001'):
            szoveg = _blokk(mid)[0]
            self.assertNotIn('TBESH.lexicon', szoveg, mid)
            self.assertNotIn('_nyers', szoveg, mid)

    def test_helyi_lexicon_konszolidalt_tabla(self):
        if not os.path.isfile(LG._U.TBESH_KONSZOLIDALT):
            self.skipTest('a gitignore-olt konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv nincs meg (tiszta klón / CI; DT-F09h)')
        LG.TBESH_HELYI_LEXICON = True
        sorok = LG.tbesh_konszolidalt().get('H0127', [])
        self.assertTrue(sorok)
        self.assertTrue(all(r['_fajl'] == LG.TBESH_KONSZ_FAJL for r in sorok))

    def test_helyi_kimenet_csak_a_repon_kivul(self):
        import tempfile
        gy = G.ROOT
        for rossz in (os.path.join(gy, 'naplok', 'x'), os.path.join(gy, 'Generalt_proba', 'x'),
                      os.path.join(gy, 'GENERALT_PROBA', 'x'), os.path.join(gy, 'adat', 'x'), gy,
                      os.path.join(gy, 'naplok', '..', 'lexikon')):
            self.assertFalse(G.helyi_kimenet_engedett(rossz), rossz)
        self.assertTrue(G.helyi_kimenet_engedett(os.path.join(tempfile.gettempdir(), 'f09_helyi_teszt')))

    def test_helyi_lexicon_kapcsolo_nem_ir_verziozott_helyre(self):
        import subprocess
        gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'general.py')
        for extra in ([], ['--kimenet', os.path.join(os.path.dirname(gen), '..', 'generalt_proba', 'x')]):
            r = subprocess.run([sys.executable, gen, '--cel', 'lexikon', '--id', 'HAMART-001', '--helyi-lexicon'] + extra,
                               capture_output=True)
            self.assertNotEqual(r.returncode, 0, extra)
            self.assertIn('helyi-lexicon', r.stderr.decode('utf-8', 'replace'))


class TestTeologiaiF09(unittest.TestCase):
    """F09 S2.5: tW + TWOT (3. szerep), BDB-etimológia (héber 8.), LXX versszintű párok (héber 6.)."""

    def _szerep(self, motivum_id, nyelv, n):
        szoveg = _blokk(motivum_id)[0]
        sz = _szakaszok(szoveg)[nyelv]
        m = re.search(r'^#### %d\. .*?(?=^#### |\Z)' % n, sz, re.M | re.S)
        return m.group(0)

    def test_tw_mindket_nyelven_es_twot_hivatkozas(self):
        g = self._szerep('ISTENTISZT-001', 'gorog', 3)
        self.assertIn('**G1941** · tW: `kt/call-speakloudly`', g)
        self.assertIn('> The terms “call” and “call out,” in this sense, mean to speak loudly.', g)
        self.assertIn('*(fordításra vár)*', g)
        self.assertNotIn('®', g)  # az unfoldingWord® védjegy a származékos szövegben nem szerepel
        h = self._szerep('ISTENTISZT-001', 'heber', 3)
        self.assertIn('**H7121** · **TWOT:** 2063', h)
        self.assertIn('**H8034** · tW: `kt/pray`, `other/renown`, `other/report`', h)
        # egy szócikk egyszer áll, akkor is, ha két token hivatkozik rá (other/renown: H7121 és H8034)
        self.assertEqual(h.count('<summary>other/renown'), 1)

    def test_tw_hianyzo_szocikk_nem_targyalja(self):
        h = self._szerep('HODIT-001', 'heber', 3)
        self.assertIn('**H7496** · *a forrás nem tárgyalja* *(tW)*', h)  # rephaim: nincs tW-szócikk
        self.assertIn('**H7496** · **TWOT:**', h)

    def test_bdb_etimologia_hatarok(self):
        b = self._szerep('ISTENTISZT-001', 'heber', 8)
        self.assertIn('##### BDB H7121 — nyelvi háttér', b)
        self.assertIn('határ: gépi', b)
        self.assertIn('határ: jóváhagyott', b)  # H8034 kézi határ
        h = self._szerep('HAMART-001', 'heber', 8)
        self.assertIn('**H0779** · *a forrás nem tárgyalja* *(BDB: a szócikk feje nem ad nyelvi hátteret)*', h)
        # javaslat-állapotú határ nem renderelhető (D41): a tábla ma nem tartalmaz ilyet
        self.assertEqual([r for r in LG.bdb_etimologia().values() if r['allapot'] == 'javaslat'], [])

    def test_lxx_versszintu_parok_jelolve_es_hivatkozas_marad(self):
        b = self._szerep('ISTENTISZT-001', 'heber', 6)
        self.assertIn('*Hivatkozás: l. a 3. szakaszt (LXX-fordítói döntések).*', b)
        self.assertIn('Versszintű együtt-előfordulás, nem szóillesztés', b)
        self.assertIn('**H8034** · 764 vers az LXX_OS-ben', b)
        self.assertIn('Proveniencia (a tábla soraiból): scope=LXX_OS-versszint', b)
        # a görög oldalon nincs ilyen sor (a tábla héber-kulcsú)
        self.assertNotIn('versszint', self._szerep('ISTENTISZT-001', 'gorog', 6))


class TestUbsDbhF09(unittest.TestCase):
    """F09 S2.3: a héber 5. (tömör jelentés) és 9. (versenkénti jelentés) szerep az UBS DBH-ból."""

    def _szerep(self, motivum_id, n):
        szoveg = _blokk(motivum_id)[0]
        sz = _szakaszok(szoveg)['heber']
        m = re.search(r'^#### %d\. .*?(?=^#### |\Z)' % n, sz, re.M | re.S)
        return m.group(0)

    def test_tomor_jelentes_darabszamok_az_adatbol(self):
        b = self._szerep('ISTENTISZT-001', 5)
        jel, _hiv, darab = LG.ubs_dbh_adatok()
        for t in ('H7121', 'H8034'):
            ossz = sum(v for (s, _), v in darab.items() if s == t)
            self.assertIn('**%s** · UBS DBH: %d jelentés, %d hivatkozott hely' % (t, len(jel[t]), ossz), b)
        self.assertIn('19 jelentés', b)
        # F121 (DT393): a H7121 (19) és H8034 (5) minden DBH-jelentése lefordítva a gyorsítótárban
        self.assertNotIn('(fordításra vár)', b)
        self.assertIn('kiáltani', b)

    def test_versenkenti_jelentes_es_mt_szamozas(self):
        b = self._szerep('ISTENTISZT-001', 9)
        self.assertIn('| Zsolt 79:6 | H7121 | `006562001011000` — to acknowledge (a deity) | — |', b)
        # Zsolt 116:13 -- a Károli-szám eltér az MT-től? a megfeleltetés a táblából, nem találgatás
        self.assertNotIn('Róm 10:13', b)  # ÚSZ-sor nem kerül ide
        ures = self._szerep('ALVIL-001', 9)
        # Károli Préd 9:12: a versmegfeleltetésben nincs MT-vers -> nincs találgatás
        self.assertRegex(ures, r'\| Préd 9:12 \| H7585 \| — \| versszámozás-eltérés \(KEZI\)')

    def test_nem_usz_vers_kihagyva(self):
        b = self._szerep('HAMART-001', 9)
        for vers in ('Gal 3:10', 'Mk 7:21'):
            self.assertNotIn('| %s |' % vers, b)


if __name__ == '__main__':
    unittest.main(verbosity=2)
