#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_render_diff_osztalyoz.py -- F09 (DT-F09g): a `render_diff_osztalyoz.py --proba` osztályozójának
tesztjei. Fő állítás: az `ismeretlen` kategória ELÉRHETŐ (nincs tartalék-kategória), és a K10 kategóriái
explicit feltételhez kötöttek.

    python eszkozok/teszt_render_diff_osztalyoz.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_diff_osztalyoz as R  # noqa: E402

KEZD = '<!-- GENERÁLT-KEZDET: general.py --cel lexikon#TESZT-001#%s | forrás: x | licenc: y | ts=2026-10-17 -->'
VEGE = '<!-- GENERÁLT-VÉGE: lexikon#TESZT-001#%s -->'


def blokk(nev, sorok):
    return '\n'.join([KEZD % nev] + list(sorok) + [VEGE % nev]) + '\n'


def osztaly(eles, proba, fajl='TESZT-001_TUDOMANYOS.md'):
    """{kategória: {'hozzaadott': [...], 'torolt': [...]}} egyszerű dict-ként."""
    return dict((k, dict(v)) for k, v in R.proba_osztalyoz(fajl, eles, proba).items())


class IsmeretlenElerheto(unittest.TestCase):
    def test_ismeretlen_blokk_ismeretlen(self):
        # ismeretlen generált blokk (nem szerepel a feltételek között): ismeretlen, nem tartalék
        eredmeny = osztaly(blokk('valami_uj', ['régi sor']), blokk('valami_uj', ['új sor']))
        self.assertEqual(set(eredmeny), {R.ISMERETLEN})
        self.assertEqual(eredmeny[R.ISMERETLEN]['torolt'], ['régi sor'])
        self.assertEqual(eredmeny[R.ISMERETLEN]['hozzaadott'], ['új sor'])
        self.assertNotIn(R.ISMERETLEN, R.PROBA_KATEGORIAK)

    def test_ismeretlen_szerep_ismeretlen(self):
        # a szerepmátrixban nem szereplő (nyelv, szerep) sorszám: nincs `szerep_vaz` tartalék
        eles = blokk('szocikkek', ['### Héber szavak: H0001'])
        proba = blokk('szocikkek', ['### Héber szavak: H0001', '#### 99. Ismeretlen szerep', 'valamilyen tartalom'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny['szerep_vaz']['hozzaadott'], ['#### 99. Ismeretlen szerep'])
        self.assertEqual(eredmeny[R.ISMERETLEN]['hozzaadott'], ['valamilyen tartalom'])

    def test_torzscikk_ismeretlen_szakasz(self):
        eles = '## 9. Valami új\nrégi\n'
        proba = '## 9. Valami új\núj\n'
        eredmeny = osztaly(eles, proba, 'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(eredmeny), {R.ISMERETLEN})

    def test_torzscikk_ismert_szakasz(self):
        eles = '## 2. Kapcsolatok\nrégi\n'
        proba = '## 2. Kapcsolatok\núj\n'
        eredmeny = osztaly(eles, proba, 'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(eredmeny), {'torzscikk_res'})

    def test_par_magyarazat_nelkul_ismeretlen(self):
        # azonos normalizált kulcs, latin zárójel-eltérés, de nincs héber/görög írásjegy és nincs blokk-kategória
        eles = blokk('uj_blokk', ['Valami (alfa) szöveg'])
        proba = blokk('uj_blokk', ['Valami (béta) szöveg'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(set(eredmeny), {R.ISMERETLEN})

    def test_main_kilepesi_kod_ismeretlennel(self):
        # a proba_main ÁLLJ-kóddal (2) lép ki, ha van ismeretlen
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            eles = os.path.join(tmp, 'eles')
            proba = os.path.join(tmp, 'proba', 'lexikon')
            os.makedirs(eles)
            os.makedirs(proba)
            for d in (eles, proba):
                with open(os.path.join(d, 'TESZT-001_TUDOMANYOS.md'), 'w', encoding='utf-8', newline='\n') as f:
                    f.write(blokk('valami_uj', ['régi sor']) if d == eles else blokk('valami_uj', ['új sor']))
            hash_ut = os.path.join(tmp, 'hash.tsv')
            with open(hash_ut, 'w', encoding='utf-8') as f:
                f.write('')
            tsv = os.path.join(tmp, 'diff.tsv')
            kod = R.proba_main(['--proba', os.path.join(tmp, 'proba'), '--eles', eles, '--tsv', tsv, '--hash', hash_ut])
            self.assertEqual(kod, 2)
            self.assertTrue(os.path.exists(os.path.join(tmp, 'diff_ismeretlen.tsv')))


class SzocikkekTorlesek(unittest.TestCase):
    def test_torolt_tartalmi_sor_tovabb_el(self):
        # a törölt tartalmi sor az új kimenetben máshol megvan: szerep_vaz (áthelyezés)
        eles = blokk('szocikkek', ['**TWOT:** 959a'])
        proba = blokk('szocikkek', ['### Héber szavak: H0001', '#### 3. Teológiai szócikk', '**H0001** · **TWOT:** 959a'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny['szerep_vaz']['torolt'], ['**TWOT:** 959a'])

    def test_torolt_tartalmi_sor_eltunik(self):
        # a törölt tartalmi sor sehol sem él tovább: ismeretlen (adatvesztés látszik)
        eles = blokk('szocikkek', ['**Szemantikai domén:** 004 Animals'])
        proba = blokk('szocikkek', ['### Héber szavak: H0001'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny[R.ISMERETLEN]['torolt'], ['**Szemantikai domén:** 004 Animals'])

    def test_torolt_fejlec_vaz(self):
        eles = blokk('szocikkek', ['#### Thayer G1944 — (teljes szócikk)'])
        proba = blokk('szocikkek', ['### Görög szavak: G1944'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny['szerep_vaz']['torolt'], ['#### Thayer G1944 — (teljes szócikk)'])

    def test_ures_ertek_sor_vaz(self):
        eles = blokk('szocikkek', ['**TWOT:** —'])
        proba = blokk('szocikkek', ['### Héber szavak: H0001'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny['szerep_vaz']['torolt'], ['**TWOT:** —'])


class ElavultAdat(unittest.TestCase):
    def test_torolt_adatsor_tovabb_el_elavult(self):
        eles = blokk('elofordulasok', ['| [1Móz 44:31](#ige-1móz-44-31) | a koporsóba — régi | Remez |'])
        proba = blokk('elofordulasok', ['| [1Móz 44:31](#ige-1móz-44-31) | a koporsóba — új | Remez |'])
        eredmeny = osztaly(eles, proba)
        self.assertIn('elavult_adat', eredmeny)
        self.assertNotIn(R.ISMERETLEN, eredmeny)

    def test_torolt_adatsor_eltunik_ismeretlen(self):
        # a törölt adatsor igehelye sehol sincs a próbában: eltűnt tartalom, nem igazolt elavulás
        eles = blokk('kereszthivatkozasok', ['- TSK: Róm 12:11 (Votes: 35)'])
        proba = blokk('kereszthivatkozasok', ['- TSK: 1Móz 3:15 (Votes: 20)'])
        eredmeny = osztaly(eles, proba)
        self.assertEqual(eredmeny[R.ISMERETLEN]['torolt'], ['- TSK: Róm 12:11 (Votes: 35)'])
        self.assertEqual(eredmeny['elavult_adat']['hozzaadott'], ['- TSK: 1Móz 3:15 (Votes: 20)'])

    def test_hozzaadott_adatsor_elavult(self):
        eredmeny = osztaly(blokk('kizart', []), blokk('kizart', ['- **Jer 4:23** (elutasítva, ...)']))
        self.assertEqual(eredmeny['elavult_adat']['hozzaadott'], ['- **Jer 4:23** (elutasítva, ...)'])

    def test_leiro_mondat_blokk_szerint(self):
        eles = blokk('kizart', ['*Ez a blokk a `[ID: TESZT-001]` motívum 0 jelöltjét fedi.*'])
        proba = blokk('kizart', ['*Ez a blokk a `[ID: TESZT-001]` motívum 2 jelöltjét fedi.*'])
        self.assertEqual(set(osztaly(eles, proba)), {'elavult_adat'})


class ForditasJelzoEsKiejtes(unittest.TestCase):
    def test_fordites_jelzo_csak_jelzo_kulonbseg(self):
        eles = blokk('szocikkek', ['#### 3. Teológiai szócikk', '*(fordítás függőben)*'])
        proba = blokk('szocikkek', ['#### 3. Teológiai szócikk', '*(fordításra vár)*'])
        self.assertEqual(osztaly(eles, proba)['fordites_jelzo'],
                         {'hozzaadott': ['*(fordításra vár)*'], 'torolt': ['*(fordítás függőben)*']})

    def test_kiejtes_heber_irassal(self):
        eles = blokk('szocikkek', ['**H7585** · שְׁאוֹל (seol)'])
        proba = blokk('szocikkek', ['**H7585** · שְׁאוֹל (she.ol)'])
        self.assertEqual(set(osztaly(eles, proba)), {'kiejtes'})

    def test_licenc_blokk_pár_nem_kiejtes(self):
        # latin zárójeles eltérés héber/görög írásjegy nélkül, licenc-blokkban: licenc (nem kiejtés)
        eles = blokk('idezes', ['- `adat/x.tsv` (projekt-adat)'])
        proba = blokk('idezes', ['- `adat/x.tsv` (minden jog fenntartva)'])
        self.assertEqual(set(osztaly(eles, proba)), {'licenc'})


class TovabbEl(unittest.TestCase):
    def test_tovabb_el_okai(self):
        sz = R.ProbaSzoveg(['| 1Móz 3:15 | valami hosszabb szöveg itt |', '**TWOT:** 959a'])
        self.assertEqual(sz.tovabb_el('**TWOT:** 959a'), 'sor')
        self.assertEqual(sz.tovabb_el('- TSK: 1Móz 3:15 (Votes: 20)'), 'igehely')
        self.assertEqual(sz.tovabb_el('**Címke:** 959a'), 'ertek')
        self.assertIsNone(sz.tovabb_el('- TSK: Róm 12:11 (Votes: 35)'))


class MegnevezettTablak(unittest.TestCase):
    """DT-F09g: az F87.3 átkulcsolás és az ismert TSK-versszám hiba csak név szerint felsorolt sorokra érvényes."""

    def test_atkulcsolt_sor_elavult(self):
        eles = blokk('kereszthivatkozasok', ['- Károli-KH: Jób 1:21'])
        proba = blokk('kereszthivatkozasok', ['- Károli-KH: 1Móz 3:15'])
        self.assertEqual(osztaly(eles, proba, 'ALVIL-001_TUDOMANYOS.md')['elavult_adat']['torolt'],
                         ['- Károli-KH: Jób 1:21'])

    def test_atkulcsolt_sor_mas_motivumban_ismeretlen(self):
        eles = blokk('kereszthivatkozasok', ['- Károli-KH: Jób 1:21'])
        proba = blokk('kereszthivatkozasok', ['- Károli-KH: 1Móz 3:15'])
        self.assertEqual(osztaly(eles, proba, 'TEREMT-001_TUDOMANYOS.md')[R.ISMERETLEN]['torolt'],
                         ['- Károli-KH: Jób 1:21'])

    def test_ismert_hiba_tsk(self):
        eles = blokk('kereszthivatkozasok', ['- TSK: Róm 12:11 (Votes: 35)', '- TSK: Róm 8:1 (Votes: 99)'])
        proba = blokk('kereszthivatkozasok', ['- Károli-KH: 1Móz 3:15'])
        e = osztaly(eles, proba, 'ALVIL-001_TUDOMANYOS.md')
        self.assertEqual(e['ismert_hiba_tsk_versszam']['torolt'], ['- TSK: Róm 12:11 (Votes: 35)'])
        # a táblán kívüli TSK-sor nem kap kivételt
        self.assertEqual(e[R.ISMERETLEN]['torolt'], ['- TSK: Róm 8:1 (Votes: 99)'])

    def test_tabla_merete(self):
        self.assertEqual(len(R.ISMERT_HIBA_TSK_VERSSZAM), 11)
        self.assertEqual(len(R.ATKULCSOLT_SOROK), 3)


if __name__ == '__main__':
    unittest.main()
