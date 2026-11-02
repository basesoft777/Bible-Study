#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_lektor_kerdesek.py -- F157: a `lektor_kerdesek.py` egységtesztjei (szintetikus HATAR-fájlon, ideiglenes könyvtárban).

    python eszkozok/teszt_lektor_kerdesek.py
"""
import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lektor_kerdesek as L  # noqa: E402

HATAR = """# HATAR_X-001.md

*(proveniencia: scope=gepi | forras=motivum_hatar.py | ts=2026-01-01)*

## Gépi rész

### 1. Részhalmaz-vizsgálat

- **K1 (reszhalmaz)** A mind a 3 verse benne van B-ben: részhalmaz-e?
  - közös helyek (3), soronként a két idézett sor:
    - 1Móz 1:1 — A: sor

### 2. Negatív kritérium

- **N1** A 2Móz 3:4 versében nincs meg a gerinc.
  - sor: x
- **E1** (nem ellenőrizhető, nem kérdés) valami

## Modelles rész

<!-- MODELLES-KEZDET -->
**2 kérdés.**

**K1 — Következetlen határ: első.**
(a) Állítás.
(b) `adat/jeloltek.tsv:598` (ApCsel 7:59, elutasítva): „idézet”.

**K2 — Hígulás: második.**
(a) Más.

*Nem kérdés (ellenőrizve, rendben):* semmi.

(proveniencia: scope=modell | forras=modell:x | ts=2026-01-02)

**Felhasználói besorolás** *(DT)*

- K2: marad így.
<!-- MODELLES-VEGE -->
"""


def irj(root, nev, szoveg):
    os.makedirs(os.path.join(root, 'naplok'), exist_ok=True)
    with open(os.path.join(root, 'naplok', nev), 'w', encoding='utf-8', newline='') as f:
        f.write(szoveg)


class GeneralasTeszt(unittest.TestCase):
    def test_kerdesek_es_mezok(self):
        k = L.hatar_kerdesek(HATAR, 'X-001')
        self.assertEqual([r['kerdes_id'] for r in k],
                         ['hatar:X-001:gK1', 'hatar:X-001:gN1', 'hatar:X-001:mK1', 'hatar:X-001:mK2'])
        self.assertEqual(k[2]['hely'], 'ApCsel 7:59')
        self.assertIn('scope=modell', k[2]['proveniencia'])
        self.assertIn('scope=gepi', k[0]['proveniencia'])
        self.assertEqual(k[3]['_besorolas'], 'marad így.')
        self.assertNotIn('Nem kérdés', k[3]['kerdes'])
        self.assertTrue(all('\t' not in r['kerdes'] and '\n' not in r['kerdes'] for r in k))

    def test_crlf_ugyanaz(self):
        self.assertEqual(L.hatar_kerdesek(HATAR, 'X-001'), L.hatar_kerdesek(HATAR.replace('\n', '\r\n'), 'X-001'))

    def test_stabil_id_es_bajtra_azonos_ujragenerales(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'HATAR_X-001.md', HATAR)
            a = L.general('X-001', t)[0]
            b = L.general('X-001', t)[0]
            self.assertEqual(a, b)
            self.assertTrue(a.startswith('# GENERÁLT'))
            with open(os.path.join(t, 'naplok', 'LEKTOR_X-001.tsv'), encoding='utf-8', newline='') as f:
                self.assertEqual(f.read(), a)

    def test_besorolas_megvalaszolva_a_tobbi_nyitva(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'HATAR_X-001.md', HATAR)
            L.general('X-001', t)
            m = L.beolvas(os.path.join(t, 'naplok', 'LEKTOR_X-001.tsv'))
            self.assertEqual(m['hatar:X-001:mK2']['allapot'], 'megvalaszolva')
            self.assertEqual(m['hatar:X-001:mK1']['allapot'], 'nyitva')

    def test_valasz_mezok_megorzese(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'HATAR_X-001.md', HATAR)
            L.general('X-001', t)
            ut = os.path.join(t, 'naplok', 'LEKTOR_X-001.tsv')
            m = L.beolvas(ut)
            m['hatar:X-001:mK1'].update(allapot='atvezetve', valasz='elvetem', atvezetes='PR #1')
            sorok = list(m.values())
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(L.tsv_szoveg('X-001', sorok))
            # a forrás kérdése változik (id marad): a válasz-mezők bájtra maradnak
            irj(t, 'HATAR_X-001.md', HATAR.replace('Állítás.', 'Más állítás.'))
            L.general('X-001', t)
            u = L.beolvas(ut)['hatar:X-001:mK1']
            self.assertEqual((u['allapot'], u['valasz'], u['atvezetes']), ('atvezetve', 'elvetem', 'PR #1'))
            self.assertIn('Más állítás.', u['kerdes'])

    def test_eltunt_valaszolt_sor_megall(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'HATAR_X-001.md', HATAR)
            L.general('X-001', t)
            irj(t, 'HATAR_X-001.md', HATAR.replace('**K2 — Hígulás: második.**\n(a) Más.\n', ''))
            with self.assertRaises(ValueError):
                L.general('X-001', t)

    def test_nem_letezo_forras_ures_nem_hiba(self):
        with tempfile.TemporaryDirectory() as t:
            szoveg, n, megj = L.general('NINCS-001', t)
            self.assertEqual(n, 0)
            self.assertIn('nincs forrásfájl', megj)
            self.assertEqual(szoveg.split('\n')[1], '\t'.join(L.MEZOK))

    def test_modelles_resz_nelkuli_forras(self):
        k = L.hatar_kerdesek('# x\n\n## Gépi rész\n\n**0 kérdés.**\n\n## Modelles rész\n\nnem futott\n', 'Y-001')
        self.assertEqual(k, [])


class ProzaJavaslatTeszt(unittest.TestCase):
    def test_sor_es_kotelezo_mezok(self):
        r = L.proza_javaslat_sor('X-001', 'a1', '1Móz 1:1', 'Az adatból ez következik, de a lap nem mondja ki: legyen róla mondat?',
                                 'adat/elofordulasok.tsv:40', 'scope=elofordulasok.tsv | forras=manual | ts=2026-11-01')
        self.assertEqual(r['forras'], 'proza_javaslat')
        self.assertEqual(r['allapot'], 'nyitva')
        self.assertIn('Adatsor: adat/elofordulasok.tsv:40', r['kerdes'])
        self.assertEqual(r['valaszlehetosegek'], L.PROZA_VALASZLEHETOSEGEK)
        for rossz in (('', 'p'), ('adat/x.tsv:1', '')):
            with self.assertRaises(ValueError):
                L.proza_javaslat_sor('X-001', 'a2', '', 'k', *rossz)

    def test_ismeretlen_forras_megall_es_javaslat_megorzodik(self):
        r = L.proza_javaslat_sor('X-001', 'a1', '', 'k', 'adat/x.tsv:1', 'manual')
        self.assertEqual(L.tsv_szoveg('X-001', [r]).split('\n')[2].split('\t')[1], 'proza_javaslat')
        regi = {r['kerdes_id']: dict(r, allapot='megvalaszolva', valasz='legyen mondat')}
        sorok, eltunt = L.osszefesul([dict(r)], regi)
        self.assertEqual((sorok[0]['allapot'], sorok[0]['valasz'], eltunt), ('megvalaszolva', 'legyen mondat', []))


DONTESEK = (
    "# DONTESEK\n| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |\n|---|---|---|---|---|---|---|---|\n"
    "| DT1 | #5 SZOTAR (x) | Mi legyen? | a · b | a | ✅ | **a** | n |\n"
    "| DT2 | #5 SZOTAR (y) | Kérdés | 1. egy · 2. kettő | 2. | 🟡 | — | n |\n"
    "| DT3 | #9 X (z) | Furcsa | o | j | 🟢 eldöntve | d | n |\n"
    "| DT4 | #7 Y (w) | Kérdés | a | b | és | pipe | 🟡 | — | n |\n"
)

BRIEF = "---\nfeladat: 9\nkod: PROBA\nallapot: %s\nkovetkezo: \"Te: dönts a K-ról\"\n---\n## 4. Lépések (⛔ a kötelező megállások)\n1. ⛔ döntsd el az X-et\n2. ⛔ A feloldva\n"


class DontesTeszt(unittest.TestCase):
    def test_nyitott_tetelek_furcsa_sorral(self):
        k = L.dontesek_kartyak(DONTESEK, '2026-11-01', {'DT2': 'tartalmi'})
        self.assertEqual([r['kerdes_id'] for r in k], ['dontes:DT2', 'dontes:DT4'])
        self.assertEqual((k[0]['cimke'], k[1]['cimke']), ('tartalmi', 'osztalyozatlan'))
        self.assertEqual(k[0]['motivum'], '#5 SZOTAR')
        self.assertIn('ts=2026-11-01', k[0]['proveniencia'])
        self.assertIn('Lehetőségek:', k[0]['kerdes'])

    def test_megallt_brief_csak_a_nyitott_pont(self):
        with tempfile.TemporaryDirectory() as t:
            for nev, all_ in (('F9_PROBA_BRIEF.md', 'megallt'), ('F8_MAS_BRIEF.md', 'lezarva')):
                with open(os.path.join(t, nev), 'w', encoding='utf-8', newline='') as f:
                    f.write(BRIEF % all_)
            k = L.megallt_briefek(t, '2026-11-01', {'F9': 'technikai'})
        self.assertEqual([r['kerdes_id'] for r in k], ['dontes:F9'])
        self.assertEqual(k[0]['cimke'], 'technikai')
        self.assertIn('döntsd el az X-et', k[0]['kerdes'])
        self.assertNotIn('feloldva', k[0]['kerdes'])
        self.assertIn('Te: dönts a K-ról', k[0]['kerdes'])

    def test_lezart_kartya_elhagyhato_a_megvalaszolatlan_nem(self):
        k = L.dontesek_kartyak(DONTESEK, 't')
        regi = {r['kerdes_id']: dict(r, allapot='atvezetve', valasz='x', atvezetes='PR') for r in k}
        self.assertEqual(L.osszefesul([], regi)[1], [])
        regi['dontes:DT2']['allapot'] = 'megvalaszolva'
        self.assertEqual(L.osszefesul([], regi)[1], ['dontes:DT2'])

    def test_regi_fejlec_beolvashato(self):
        with tempfile.TemporaryDirectory() as t:
            ut = os.path.join(t, 'LEKTOR_R.tsv')
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write('\t'.join(L.MEZOK_REGI) + '\n' + '\t'.join(['a:b:c', 'hatar', 'R', '', 'k', '', 'p', 'nyitva', '', '']) + '\n')
            self.assertEqual(L.beolvas(ut)['a:b:c']['cimke'], '')

    def test_szuro_fajl_ervenyes(self):
        sz = L.szuro_beolvas(L.ROOT)
        self.assertTrue(sz)
        self.assertTrue(set(sz.values()) <= {'tartalmi', 'uzleti', 'technikai'})


if __name__ == '__main__':
    unittest.main(verbosity=1)
