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
        with tempfile.TemporaryDirectory() as t:
            self.assertIn('nincs F7_*_BRIEF', L.dontesek_kartyak(DONTESEK, 't', {}, L.brief_besorolo(t))[1]['cimke_indok'])
        self.assertEqual(k[0]['motivum'], '#5 SZOTAR')
        self.assertIn('ts=2026-11-01', k[0]['proveniencia'])
        self.assertIn('Lehetőségek:', k[0]['kerdes'])

    def test_megallt_brief_csak_a_nyitott_pont(self):
        with tempfile.TemporaryDirectory() as t:
            for nev, all_ in (('F9_PROBA_BRIEF.md', 'megallt'), ('F8_MAS_BRIEF.md', 'lezarva')):
                with open(os.path.join(t, nev), 'w', encoding='utf-8', newline='') as f:
                    f.write(BRIEF % all_)
            k = L.megallt_briefek(t, '2026-11-01', {'F9': 'fejlesztoi'})
        self.assertEqual([r['kerdes_id'] for r in k], ['dontes:F9'])
        self.assertEqual(k[0]['cimke'], 'fejlesztoi')
        self.assertEqual(k[0]['cimke_indok'], 'kézi besorolás (dontes_szuro.tsv)')
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
        self.assertTrue(set(sz.values()) <= {'tartalmi', 'kiadoi', 'uzleti', 'fejlesztoi'})


def fejlec(**kv):
    return dict({'feladat': '1', 'kod': 'X', 'munka': '', 'ir': ''}, **kv)


class GepiKategoriaTeszt(unittest.TestCase):
    def test_ir_lista_idezojel_es_zarojel(self):
        self.assertEqual(L.ir_lista('[adat/a.tsv, "naplok/B_*.md", eszkozok/c.py]'), ['adat/a.tsv', 'naplok/B_*.md', 'eszkozok/c.py'])
        self.assertEqual(L.ir_lista(''), [])

    def test_tartalmi_adat_es_motivum(self):
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[adat/jeloltek.tsv]'))[0], 'tartalmi')
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[motivumok/ALVIL-001.md]'))[0], 'tartalmi')
        self.assertEqual(L.gepi_kategoria(fejlec(munka='ertelmezo', ir='[naplok/x.md]'))[0], 'tartalmi')

    def test_kiadoi(self):
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[adat/licencek.tsv]'))[0], 'kiadoi')
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[eszkozok/lektor_felulet/]'))[0], 'kiadoi')

    def test_uzleti(self):
        self.assertEqual(L.gepi_kategoria(fejlec(kod='ELOFIZETES_FEED', ir='[adat/SEMA.md]'))[0], 'uzleti')
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[eszkozok/feed_epit.py]'))[0], 'uzleti')
        self.assertEqual(L.gepi_kategoria(fejlec(kod='ELOFIZETES_FEED', ir='[adat/licencek.tsv]'))[0], 'kiadoi')

    def test_fejlesztoi(self):
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[eszkozok/x.py, .github/y.yml]'))[0], 'fejlesztoi')
        self.assertEqual(L.gepi_kategoria(fejlec(munka='folyamat', ir='[naplok/x.md]'))[0], 'fejlesztoi')

    def test_magasabb_nyer(self):
        self.assertEqual(L.gepi_kategoria(fejlec(munka='folyamat', ir='[eszkozok/x.py, adat/licencek.tsv]'))[0], 'kiadoi')
        self.assertEqual(L.gepi_kategoria(fejlec(ir='[adat/licencek.tsv, adat/forditasok.tsv]'))[0], 'tartalmi')

    def test_osztalyozatlan_es_indok(self):
        kat, indok = L.gepi_kategoria(fejlec(feladat='7', ir='[naplok/x.md]'))
        self.assertEqual(kat, 'osztalyozatlan')
        self.assertIn('#7', indok)
        self.assertIn('adat/jeloltek.tsv', L.gepi_kategoria(fejlec(ir='[adat/jeloltek.tsv]'))[1])

    def test_kezi_szuro_elsobbsege_es_regi_ertek(self):
        b = lambda szam: ('fejlesztoi', 'gépi')
        self.assertEqual(L.kategoria('DT2', {'DT2': 'tartalmi'}, b, '5')[0], 'tartalmi')
        self.assertEqual(L.kategoria('DT3', {}, b, '5')[0], 'fejlesztoi')
        self.assertEqual(L.kategoria('DT3', {}, b, '')[0], 'osztalyozatlan')
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, 'eszkozok', 'lektor_felulet'))
            with open(os.path.join(t, L.SZURO_UT), 'w', encoding='utf-8', newline='') as f:
                f.write('azonosito\tcimke\tmegjegyzes\nDT1\tuzleti\tx\nDT2\ttechnikai\ty\nDT3\ttartalmi\tz\n')
            self.assertEqual(L.szuro_beolvas(t), {'DT1': 'uzleti', 'DT2': 'fejlesztoi', 'DT3': 'tartalmi'})

    def test_lefele_vedelem(self):
        b = lambda szam: ('fejlesztoi', 'gépi')
        kat, indok = L.kategoria('DT2', {'DT2': 'tartalmi'}, b, '5')
        self.assertEqual(kat, 'tartalmi')
        self.assertIn('a kézi marad', indok)
        self.assertNotIn('a kézi marad', L.kategoria('DT2', {'DT2': 'fejlesztoi'}, b, '5')[1])
        self.assertNotIn('a kézi marad', L.kategoria('DT2', {'DT2': 'tartalmi'}, lambda z: ('tartalmi', 'g'), '5')[1])

    def test_motivum_hatar_tartalmi_jel(self):
        self.assertEqual(L.gepi_kategoria(fejlec(munka='adat', ir='[eszkozok/x.py, \"naplok/HATAR_*.md\"]'))[0], 'tartalmi')
        self.assertIn('felülbírálható', L.gepi_kategoria(fejlec(ir='[eszkozok/x.py]'))[1])

    def test_dontes_kartya_indokkal_es_briefbol(self):
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, 'F5_SZOTAR_BRIEF.md'), 'w', encoding='utf-8', newline='') as f:
                f.write('---\nfeladat: 5\nkod: SZOTAR\nmunka: adat\nir: [adat/forditasok.tsv]\n---\n')
            k = L.dontesek_kartyak(DONTESEK, 't', {'DT4': 'kiadoi'}, L.brief_besorolo(t))
        self.assertEqual((k[0]['cimke'], k[1]['cimke']), ('tartalmi', 'kiadoi'))
        self.assertIn('adat/forditasok.tsv', k[0]['cimke_indok'])
        self.assertEqual(k[1]['cimke_indok'], 'kézi besorolás (dontes_szuro.tsv)')


LEKTOR_MD = """# KIADAS X-001 — lektori kérdéslista

*Nem javítás.*

## Lefedettség

1. **(4. kérdés)** Kapcsolat 1Móz 4:26 → Sof 3:9 nincs a próza elemei között. Szándékos?

## Kivonat (5–19. sor)

2. **(1./2. kérdés)** 11. sor: a kritérium kivétel nélkül szerepel.

---

Ellenőrzött és nem kérdéses: semmi.

(proveniencia: scope=motivumok/X-001.md | forras=modell:claude-fable-5-1 | ts=2026-11-02T08:00Z)
"""

LISTA_MD = """## X-001

### Lefedettség (a próza nem nevezi meg)

| rovat | adat |
|---|---|
| kapcsolat | 18 |

Név nélküli elemek (a gyűjtő mondat N-jéig csoportosan fedett előfordulás nélkül):

- kapcsolat: 1Móz 4:26 → Sof 3:9 (Párhuzam)
- nyitott jelölt: Ézs 41:25 (elofordulas; F110 szűrő)

*A „Károli rejtett párhuzama” nem mérhető.*

### Egyenetlenség (blokkonként)

- ez már nem elem
"""


class KiadasTeszt(unittest.TestCase):
    def test_lektor_tetelek(self):
        k = L.lektor_kerdesek(LEKTOR_MD, 'X-001')
        self.assertEqual([r['kerdes_id'] for r in k], ['lektor:X-001:1', 'lektor:X-001:2'])
        self.assertEqual((k[0]['forras'], k[0]['hely']), ('lektor', 'Lefedettség'))
        self.assertIn('Szándékos?', k[0]['kerdes'])
        self.assertIn('forras=modell:claude-fable-5-1', k[1]['proveniencia'])
        self.assertNotIn('Ellenőrzött', ' '.join(r['kerdes'] for r in k))

    def test_lista_hianyok(self):
        k = L.lista_hianyok(LISTA_MD, 'X-001')
        self.assertEqual(len(k), 2)
        self.assertEqual({r['forras'] for r in k}, {'proza_lefedettseg'})
        self.assertEqual(k[1]['hely'], 'Ézs 41:25')
        self.assertTrue(k[0]['kerdes_id'].startswith('proza_lefedettseg:X-001:'))
        self.assertEqual(k[0]['proveniencia'], 'manual')
        # stabil azonosító újrafuttatásra
        self.assertEqual(k[0]['kerdes_id'], L.lista_hianyok(LISTA_MD, 'X-001')[0]['kerdes_id'])

    def test_general_a_ket_kiadas_fajlbol(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'KIADAS_X-001_lektor.md', LEKTOR_MD)
            irj(t, 'KIADAS_X-001_lista.md', LISTA_MD)
            sz, n, megj = L.general('X-001', t)
            self.assertEqual((n, megj), (4, ''))
            sz2, _n, _m = L.general('X-001', t)
            self.assertEqual(sz, sz2)
            m = L.beolvas(os.path.join(t, 'naplok', 'LEKTOR_X-001.tsv'))
            self.assertEqual({r['forras'] for r in m.values()}, {'lektor', 'proza_lefedettseg'})


OSSZ_TSV = "# megjegyzés\nkerdes_id\ttipus\tgond\tjavaslat\tproveniencia\nlektor:X-001:1\tnincs\tEgyszerű gond.\tA lektor nem javasolt konkrét javítást.\tmanual\n"


class OsszefoglaloTeszt(unittest.TestCase):
    def _irj_ossz(self, t, szoveg):
        os.makedirs(os.path.join(t, 'eszkozok', 'lektor_felulet'), exist_ok=True)
        with open(os.path.join(t, 'eszkozok', 'lektor_felulet', 'osszefoglalo_X-001.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def test_beolvas_es_ratolt(self):
        with tempfile.TemporaryDirectory() as t:
            self._irj_ossz(t, OSSZ_TSV)
            o = L.osszefoglalo_beolvas('X-001', t)
            self.assertEqual(o['lektor:X-001:1'][0], 'nincs')
            uj = L.osszefoglalo_ra(L.lektor_kerdesek(LEKTOR_MD, 'X-001'), o)
            self.assertEqual(uj[0]['gond'], 'Egyszerű gond.')
            self.assertEqual(uj[0]['javaslat_tipus'], 'nincs')
            self.assertEqual(uj[1].get('gond', ''), '')

    def test_ismeretlen_kerdes_es_hibas_tipus_hiba(self):
        with tempfile.TemporaryDirectory() as t:
            self._irj_ossz(t, OSSZ_TSV.replace('lektor:X-001:1', 'lektor:X-001:99'))
            o = L.osszefoglalo_beolvas('X-001', t)
            with self.assertRaises(ValueError):
                L.osszefoglalo_ra(L.lektor_kerdesek(LEKTOR_MD, 'X-001'), o)
            self._irj_ossz(t, OSSZ_TSV.replace('\tnincs\t', '\tvalami\t'))
            with self.assertRaises(ValueError):
                L.osszefoglalo_beolvas('X-001', t)

    def test_nincs_fajl_ures(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(L.osszefoglalo_beolvas('X-001', t), {})

    def test_az_istentiszt_mind_a_22_kerdesehez_van_osszefoglalo(self):
        szoveg, n, _m = L.general('ISTENTISZT-001', L.ROOT, ir=False)
        sorok = [x.split('\t') for x in szoveg.split('\n') if x and not x.startswith('#')][1:]
        fej = L.MEZOK
        gi, ti = fej.index('gond'), fej.index('javaslat_tipus')
        self.assertEqual(n, 22)
        self.assertTrue(all(r[gi].strip() and r[ti] in L.JAVASLAT_TIPUSOK for r in sorok))


class KiadasJelTeszt(unittest.TestCase):
    def test_forrasonkenti_kiadas(self):
        with tempfile.TemporaryDirectory() as t:
            irj(t, 'HATAR_X-001.md', HATAR)
            irj(t, 'KIADAS_X-001_lektor.md', LEKTOR_MD)
            irj(t, 'KIADAS_X-001_lista.md', LISTA_MD)
            L.general('X-001', t)
            m = L.beolvas(os.path.join(t, 'naplok', 'LEKTOR_X-001.tsv'))
        ki = {}
        for r in m.values():
            ki.setdefault(r['forras'], set()).add(r['kiadas'])
        self.assertEqual(ki, {'hatar': {'1'}, 'lektor': {'2'}, 'proza_lefedettseg': {'2'}})

    def test_dontes_nem_kiadas_kerdes(self):
        k = L.dontesek_kartyak(DONTESEK, 't')
        sorok, _e = L.osszefesul(k, {})
        self.assertEqual({r['kiadas'] for r in sorok}, {''})

    def test_regebbi_fejlec_is_beolvashato(self):
        with tempfile.TemporaryDirectory() as t:
            ut = os.path.join(t, 'LEKTOR_R.tsv')
            fej = L.MEZOK_V3
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write('\t'.join(fej) + '\n' + '\t'.join(['a:b:c', 'hatar', 'R', '', 'k', '', 'p', 'nyitva', '', '', 'tartalmi', '', '', '', '']) + '\n')
            r = L.beolvas(ut)['a:b:c']
            self.assertEqual(r['kiadas'], '')


class HatarJelenlegiTeszt(unittest.TestCase):
    """A határ-kártya „A jelenlegi határ” blokkja az adatból; hiányzó adatnál kimondja, nem tölti ki."""

    def _adat(self, t):
        os.makedirs(os.path.join(t, 'adat'))

        def irj_adat(nev, sz):
            with open(os.path.join(t, 'adat', nev), 'w', encoding='utf-8', newline='\n') as f:
                f.write(sz)
        irj_adat('motivumok.tsv', '# fej\nid\tcim\tnegativ_kriterium\tfolerendelt_fogalom\nX-001\tCím\t"idézőjeles" kritérium\ttágabb kör\n')
        irj_adat('elofordulasok.tsv', '# fej\nid\tigehely\tkapcsolodas\nX-001\tLuk 10:15\tbent levő hely\nY-001\tMt 16:18\tmás motívum\n')
        irj_adat('jeloltek.tsv', '# fej\nid\tigehely\tdontes\tindoklas\tjelolt_tipus\nX-001\tMt 16:18\telutasítva\tmás téma\t\n'
                 'X-001\tLuk 10:15\tbeépítve\tbent\t\n')

    def test_allapot_es_proveniencia(self):
        with tempfile.TemporaryDirectory() as t:
            self._adat(t)
            sz = L.hatar_jelenlegi('X-001', ['Mt 16:18', 'Luk 10:15', 'Ján 1:1'], t, ts='2026-11-02')
        s = sz.split(L.SORTORES)
        self.assertIn('Negatív kritérium: "idézőjeles" kritérium (`adat/motivumok.tsv:3`)', s[0])
        self.assertIn('Fölérendelt fogalom: tágabb kör', s[1])
        self.assertTrue(s[2].startswith('Mt 16:18: elutasítva — jelölt (`adat/jeloltek.tsv:3`'))
        self.assertTrue(s[3].startswith('Luk 10:15: bent van — előfordulás (`adat/elofordulasok.tsv:3`'))
        self.assertEqual(len([x for x in s if x.startswith('Luk 10:15')]), 1)  # a beépített jelölt nem ismétlődik
        self.assertIn('Ján 1:1: nincs sora', s[4])
        self.assertTrue(s[-1].startswith('(proveniencia: scope=') and 'talalt=2' in s[-1])

    def test_nincs_motivum_sor(self):
        with tempfile.TemporaryDirectory() as t:
            self._adat(t)
            sz = L.hatar_jelenlegi('Z-001', ['Mt 16:18'], t)
        self.assertIn('nem olvasható ki', sz)

    def test_kartya_igehelyei(self):
        k = {'kerdes': 'Cím: az Mt 16:18 kint, a Luk 10:15 bent ⏎ (a) 1Kor 15:55 ⏎ (b) Jel 1:18', 'hely': 'Mt 16:18'}
        self.assertEqual(L.kartya_igehelyek(k), ['Mt 16:18', 'Luk 10:15', '1Kor 15:55'])

    def test_kovetkezmeny_csak_hataron_es_parban(self):
        with tempfile.TemporaryDirectory() as t:
            d = os.path.join(t, 'eszkozok', 'lektor_felulet')
            os.makedirs(d)
            fej = 'kerdes_id\ttipus\tgond\tjavaslat\tproveniencia\tkov_elfogadom\tkov_elvetem\n'
            ut = os.path.join(d, 'osszefoglalo_X-001.tsv')

            def ir(sz):
                with open(ut, 'w', encoding='utf-8') as f:
                    f.write(fej + sz)
            ir('hatar:X-001:mK1\tnincs\tg\tj\tmanual\ta\tb\nlektor:X-001:1\tnincs\tg\tj\tmanual\t\t\n')
            self.assertEqual(L.osszefoglalo_beolvas('X-001', t)['hatar:X-001:mK1'][4:], ('a', 'b', '', ''))
            ir('lektor:X-001:1\tnincs\tg\tj\tmanual\ta\tb\n')
            with self.assertRaises(ValueError):
                L.osszefoglalo_beolvas('X-001', t)
            ir('hatar:X-001:mK1\tnincs\tg\tj\tmanual\ta\t\n')
            with self.assertRaises(ValueError):
                L.osszefoglalo_beolvas('X-001', t)

    def test_haromvalaszos_kartya(self):
        with tempfile.TemporaryDirectory() as t:
            d = os.path.join(t, 'eszkozok', 'lektor_felulet')
            os.makedirs(d)
            fej = 'kerdes_id\ttipus\tgond\tjavaslat\tproveniencia\tkov_elfogadom\tkov_elvetem\tgombok\tkov_harmadik\n'
            ut = os.path.join(d, 'osszefoglalo_X-001.tsv')

            def ir(sz):
                with open(ut, 'w', encoding='utf-8') as f:
                    f.write(fej + sz)
            ir('hatar:X-001:mK1\tnincs\tg\tj\tmanual\ta\tb\tKi | Marad | Részben\tc\nhatar:X-001:mK2\tnincs\tg\tj\tmanual\ta\tb\t\t\n')
            o = L.osszefoglalo_beolvas('X-001', t)
            self.assertEqual(o['hatar:X-001:mK1'][4:], ('a', 'b', 'Ki | Marad | Részben', 'c'))
            self.assertEqual(o['hatar:X-001:mK2'][6:], ('', ''))
            for rossz in ('Ki | Marad\tc', 'Ki | Marad | Részben\t', 'Ki |  | Részben\tc'):
                ir('hatar:X-001:mK1\tnincs\tg\tj\tmanual\ta\tb\t%s\n' % rossz)
                with self.assertRaises(ValueError):
                    L.osszefoglalo_beolvas('X-001', t)
            ir('hatar:X-001:mK1\tnincs\tg\tj\tmanual\t\t\tKi | Marad | Részben\tc\n')
            with self.assertRaises(ValueError):
                L.osszefoglalo_beolvas('X-001', t)

    def test_regi_fejlec_beolvashato(self):
        with tempfile.TemporaryDirectory() as t:
            ut = os.path.join(t, 'LEKTOR_X-001.tsv')
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write('# fej\n' + '\t'.join(L.MEZOK_V5) + '\n' + '\t'.join(['hatar:X-001:mK1'] + [''] * (len(L.MEZOK_V5) - 1)) + '\n')
            r = L.beolvas(ut)['hatar:X-001:mK1']
            self.assertEqual((r['gombok'], r['kov_harmadik']), ('', ''))


class LapnezetTeszt(unittest.TestCase):
    """A „lapnézet” link motívumonként (lapnezetek.tsv); ami nincs a táblában, annak nincs linkje."""

    def test_tabla_beolvasasa(self):
        import importlib
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lektor_felulet'))
        E = importlib.import_module('epit')
        with tempfile.TemporaryDirectory() as t:
            ut = os.path.join(t, 'lapnezetek.tsv')
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write('# megj\nmotivum\turl\tmegjegyzes\nA-001\thttps://x/a\t\nB-001\thttps://x/b\tm\n')
            self.assertEqual(E.lapnezetek(ut), {'A-001': 'https://x/a', 'B-001': 'https://x/b'})
            self.assertEqual(E.lapnezetek(os.path.join(t, 'nincs.tsv')), {})
            with open(ut, 'a', encoding='utf-8', newline='\n') as f:
                f.write('A-001\thttps://x/c\t\n')
            with self.assertRaises(ValueError):
                E.lapnezetek(ut)

    def test_a_repo_tablaja_es_a_sablon(self):
        import importlib
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lektor_felulet'))
        E = importlib.import_module('epit')
        n = E.lapnezetek()
        self.assertIn('ALVIL-001', n)
        self.assertNotEqual(n['ALVIL-001'], n.get('ISTENTISZT-001'))
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, 'naplok'))
            html = E.epit(nezetek={'A-001': 'https://x/a'}, root=t)
        self.assertIn('const LAP_URLOK = {"A-001": "https://x/a"};', html)
        self.assertNotIn('__LAP_URLOK__', html)


if __name__ == '__main__':
    unittest.main(verbosity=1)
