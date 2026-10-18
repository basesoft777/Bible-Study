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
        # hozzáadott sor, vagy olyan törölt sor, amelynek jelölt-sora (címke + igehely) a próbában megvan
        eles = '## 2. Kapcsolatok\n| [Jób 1:1](#v) | magas · tartalom-alapú |\n'
        proba = '## 2. Kapcsolatok\n| [Jób 1:1](#v) | magas · szó-szintű-gépi |\nújabb sor\n'
        eredmeny = osztaly(eles, proba, 'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(eredmeny), {'torzscikk_res'})

    def test_torzscikk_torolt_sor_eltunik_ismeretlen(self):
        eles = '## 2. Kapcsolatok\n- **TSK-kereszthivatkozás** (szavazatszám): Róm 8:1 (5)\n'
        proba = '## 2. Kapcsolatok\nmás tartalom\n'
        eredmeny = osztaly(eles, proba, 'TESZT-001_TORZSCIKK.md')
        self.assertEqual(eredmeny[R.ISMERETLEN]['torolt'], ['- **TSK-kereszthivatkozás** (szavazatszám): Róm 8:1 (5)'])

    def test_licenc_es_lxx_torolt_sor_eltunik_ismeretlen(self):
        for blokk_nev in ('idezes', 'kolofon', 'lxx'):
            eles = blokk(blokk_nev, ['| Jób 1:1 | régi sor |'])
            proba = blokk(blokk_nev, ['teljesen más'])
            e = osztaly(eles, proba)
            self.assertEqual(e[R.ISMERETLEN]['torolt'], ['| Jób 1:1 | régi sor |'], blokk_nev)
        # #113 (2. hely): a licenc-blokkban a NEM licenc-szöveg cseréje nem licenc, hanem ismeretlen
        for blokk_nev in ('idezes', 'kolofon'):
            e2 = osztaly(blokk(blokk_nev, ['| Jób 1:1 | régi sor |']), blokk(blokk_nev, ['| Jób 1:1 | új sor |']))
            self.assertEqual(set(e2), {R.ISMERETLEN}, blokk_nev)
        # #113 (4. hely): az lxx blokkban az azonos fokú állapot-csere (egyező -> eltérő) ismeretlen
        e3 = osztaly(blokk('lxx', ['| Jób 1:1 | egyező |']), blokk('lxx', ['| Jób 1:1 | eltérő |']))
        self.assertEqual(set(e3), {R.ISMERETLEN})

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
        eles = blokk('elofordulasok', ['| [1Móz 44:31](#ige-1móz-44-31) | a koporsóba | magas · tartalom-alapú[^2] |'])
        proba = blokk('elofordulasok', ['| [1Móz 44:31](#ige-1móz-44-31) | a koporsóba | magas · szó-szintű-gépi[^2] |'])
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
        # #113 (5. hely): az új átírás a héber lemma mai kiejtése (adat/kiejtes_kivetelek.tsv: שְׁאוֹל -> seól)
        eles = blokk('szocikkek', ['**H7585** · שְׁאוֹל (she.ol)'])
        proba = blokk('szocikkek', ['**H7585** · שְׁאוֹל (seól)'])
        self.assertEqual(set(osztaly(eles, proba)), {'kiejtes'})
        # a fordított irányt (az új oldal nem a mai kiejtés) az adat nem igazolja: nem kiejtés
        self.assertNotIn('kiejtes', osztaly(proba, eles))

    def test_licenc_blokk_pár_nem_kiejtes(self):
        # latin zárójeles eltérés héber/görög írásjegy nélkül, licenc-blokkban: licenc (nem kiejtés)
        eles = blokk('idezes', ['- `adat/x.tsv` (projekt-adat)'])
        proba = blokk('idezes', ['- `adat/x.tsv` (minden jog fenntartva)'])
        self.assertEqual(set(osztaly(eles, proba)), {'licenc'})


class TovabbEl(unittest.TestCase):
    def test_tovabb_el_okai(self):
        sz = R.ProbaSzoveg(['| 1Móz 3:15 | valami hosszabb szöveg itt |', '**TWOT:** 959a', '- Károli-KH: Ézs 38:18',
                            '- TSK: 1Móz 3:15 (Votes: 20)', '**H7585** · **TWOT:** 2303c'])
        self.assertEqual(sz.tovabb_el('**TWOT:** 959a'), 'sor')
        self.assertEqual(sz.tovabb_el('- TSK: 1Móz 3:15 (Votes: 21)'), 'cimke_igehely')
        self.assertEqual(sz.tovabb_el('**TWOT:** 2303c'), 'ertek')
        self.assertIsNone(sz.tovabb_el('**Más:** 2303c'))
        self.assertIsNone(sz.tovabb_el('- TSK: Róm 12:11 (Votes: 35)'))
        # az igehely önmagában (más sorban, más címkével) nem elég: Ézs 38:18 csak Károli-KH sorban van
        self.assertIsNone(sz.tovabb_el('- TSK: Ézs 38:18 (Votes: 15)'))
        # a szigorúbb részlet-ág: csak egyetlen próba-sor része lehet
        self.assertIsNone(sz.tovabb_el('valami hosszabb szöveg itt és még sok minden más'))


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
        self.assertEqual(len(R.ISMERT_HIBA_TSK_VERSSZAM), 13)
        # az F87.3-lábnyom név szerinti, csak ALVIL-001 (3. javító menet)
        self.assertEqual(len(R.ATKULCSOLT_SOROK), 27)
        self.assertTrue(all(m == 'ALVIL-001' for m, _ in R.ATKULCSOLT_SOROK))
        self.assertTrue(set(R.ATKULCSOLT_SOROK.values()) <= set(R.ATKULCSOLT_KULCS))


class Parositas(unittest.TestCase):
    """DT-F09g (3. javító menet): kulcs szerinti, kizárólagos párosítás -- teljes kulcs, nem csak igehely."""

    def test_par_nelkuli_torles_ismeretlen_marad(self):
        eles = blokk('kereszthivatkozasok', ['#### Préd 9:10', '- TSK: Ézs 38:18 (Votes: 15)'])
        proba = blokk('kereszthivatkozasok', ['#### Préd 9:12', '- Károli-KH: 1Móz 3:15'])
        e = osztaly(eles, proba, 'TESZT-001_TUDOMANYOS.md')
        self.assertIn('- TSK: Ézs 38:18 (Votes: 15)', e[R.ISMERETLEN]['torolt'])

    def test_csak_igehelyre_egyezo_nem_par(self):
        # az Ézs 38:18 az új oldalon másik címkével (Károli-KH) és másik fejléc alatt áll: nem pár
        eles = blokk('kereszthivatkozasok', ['#### Préd 9:10', '- TSK: Ézs 38:18 (Votes: 15)'])
        proba = blokk('kereszthivatkozasok', ['#### Préd 9:12', '- Károli-KH: Ézs 38:18'])
        e = osztaly(eles, proba, 'TESZT-001_TUDOMANYOS.md')
        self.assertIn('- TSK: Ézs 38:18 (Votes: 15)', e[R.ISMERETLEN]['torolt'])
        self.assertNotIn('- Károli-KH: Ézs 38:18', e.get('elavult_adat', {}).get('torolt', []))

    def test_teljes_kulcs_egyezes_par(self):
        # azonos címke + fejléc + célpont, csak a szavazatszám változott: pár
        eles = blokk('kereszthivatkozasok', ['#### Préd 9:12', '- TSK: Ézs 38:18 (Votes: 15)'])
        proba = blokk('kereszthivatkozasok', ['#### Préd 9:12', '- TSK: Ézs 38:18 (Votes: 16)'])
        e = osztaly(eles, proba, 'TESZT-001_TUDOMANYOS.md')
        self.assertNotIn(R.ISMERETLEN, e)
        self.assertEqual(e['elavult_adat']['torolt'], ['- TSK: Ézs 38:18 (Votes: 15)'])

    def test_egy_hozzaadott_nem_ket_torles_parja(self):
        eles = blokk('elofordulasok', ['| [Jób 1:1](#a) | első | H0001 |', '| [Jób 1:1](#a) | második | H0001 |'])
        proba = blokk('elofordulasok', ['| [Jób 1:1](#a) | új | H0001 |'])
        e = osztaly(eles, proba, 'TESZT-001_TUDOMANYOS.md')
        # cellánkénti összevetés: az `első` -> `új` tartalomcsere ismeretlen fajta -> a pár `ismeretlen`
        self.assertEqual(e[R.ISMERETLEN]['torolt'], ['| [Jób 1:1](#a) | első | H0001 |'])
        # a hozzáadott sor egyetlen törlés párja: csak 1 ismeretlen hozzáadott sor
        self.assertEqual(e[R.ISMERETLEN]['hozzaadott'], ['| [Jób 1:1](#a) | új | H0001 |'])
        # a második törlésnek nincs (szabad) párja: a tovabb_el dönt, nem a pár
        self.assertEqual(sum(len(v['torolt']) for v in e.values()), 2)

    def test_kiejtes_par(self):
        eles = blokk('lxx', ['| [Zsolt 16:10](#v) | Zsolt(LXX) 15:10 | שְׁאוֹל | ᾅδην (ᾅδης, Hadēs G0086) | egyező |'])
        proba = blokk('lxx', ['| [Zsolt 16:10](#v) | Zsolt(LXX) 15:10 | שְׁאוֹל | ᾅδην (ᾅδης, Hadész G0086) | egyező |'])
        self.assertEqual(set(osztaly(eles, proba)), {'kiejtes'})

    def test_allapotvaltas_szerep(self):
        eles = '## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | nincs adatosítva |\n'
        proba = '## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | UBS DBH |\n'
        e = osztaly(eles, proba, 'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(e), {'szerep'})

    def test_metaadat_jeloles(self):
        e = osztaly(blokk('idezes', ['- Generálva: 2026-09-26']), blokk('idezes', ['- Generálva: 2026-10-17']))
        self.assertEqual(set(e), {'jeloles'})

    def test_ures_allapot_ellenorzott_csere(self):
        eles = blokk('kizart', ['Nincs kizárt vagy nyitva maradt jelölt a `jeloltek.tsv`-ben ehhez a motívumhoz.'])
        proba = blokk('kizart', ['- **Jer 4:23** (elutasítva, valami)'])
        self.assertEqual(set(osztaly(eles, proba)), {'elavult_adat'})
        # üres-állapot mondat valódi tartalom nélkül nem számít cserének
        proba2 = blokk('kizart', [])
        self.assertIn(R.ISMERETLEN, osztaly(eles, proba2))


class CellankentiOsszevetes(unittest.TestCase):
    """DT-F09g (4. javító menet): pár esetén a nem kulcs cellák minden eltérése ismert fajta kell legyen."""

    def test_tartalom_eltunik_ismeretlen(self):
        e = osztaly(blokk('elofordulasok', ['| [Jób 1:1](#a) | ᾅδου | H0001 |']),
                    blokk('elofordulasok', ['| [Jób 1:1](#a) | — | H0001 |']))
        self.assertEqual(e[R.ISMERETLEN]['torolt'], ['| [Jób 1:1](#a) | ᾅδου | H0001 |'])

    def test_helyorzo_tartalom(self):
        e = osztaly(blokk('lxx', ['| Jób 1:1 | — | G0001 |']), blokk('lxx', ['| Jób 1:1 | ᾅδου | G0001 |']))
        self.assertEqual(set(e), {'lxx_korpusz'})

    def test_hades_hadesz_kiejtes(self):
        e = osztaly(blokk('lxx', ['| Jób 1:1 | ᾅδου (ᾅδης, Hadēs G0001) | G0001 |']),
                    blokk('lxx', ['| Jób 1:1 | ᾅδου (ᾅδης, Hadész G0001) | G0001 |']))
        self.assertEqual(set(e), {'kiejtes'})

    def test_modszer_jelzo(self):
        e = osztaly(blokk('elofordulasok', ['| [Jób 1:1](#a) | x | magas · tartalom-alapú[^1] |']),
                    blokk('elofordulasok', ['| [Jób 1:1](#a) | x | magas · szó-szintű-gépi[^1] |']))
        self.assertEqual(set(e), {'elavult_adat'})

    def test_ket_cella_egyik_ismeretlen(self):
        # az 1. cella helyőrző -> tartalom (ismert), a 2. cella magyar szöveg cseréje (ismeretlen) -> a sor ismeretlen
        e = osztaly(blokk('lxx', ['| Jób 1:1 | — | régi | G0001 |']), blokk('lxx', ['| Jób 1:1 | ᾅδου | új | G0001 |']))
        self.assertEqual(set(e), {R.ISMERETLEN})

    def test_uj_mezo_hozzafuzese_nem_veszteseg(self):
        e = osztaly('## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | UBS |\n',
                    '## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | UBS | javaslat |\n',
                    'TESZT-001_TORZSCIKK.md')
        self.assertNotIn(R.ISMERETLEN, e)

    def test_mezo_eltunese_ismeretlen(self):
        e = osztaly('## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | UBS | javaslat |\n',
                    '## 5. Szótári háttér — szerepek és lefedettség\n| H7585 | TBESH | UBS |\n',
                    'TESZT-001_TORZSCIKK.md')
        self.assertIn(R.ISMERETLEN, e)

    def test_felhasznalo_elfogadva_nev_szerint(self):
        sor = '- LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) — CC BY-SA 3.0'
        eles = '## Források és licenc\n' + sor + '\n'
        proba = '## Források és licenc\n'
        e = osztaly(eles, proba, 'ISTENTISZT-001_TORZSCIKK.md')
        self.assertEqual(e['felhasznalo_elfogadva']['torolt'], [sor])
        # más fájlban ugyanez a sor nincs felsorolva: ismeretlen; hozzáadott irányban sem érvényes
        e2 = osztaly(eles, proba, 'KIRALY-001_TORZSCIKK.md')
        self.assertIn(R.ISMERETLEN, e2)

    def test_32_elfogadott_csoportok(self):
        import collections
        db = collections.Counter(R.FELHASZNALO_ELFOGADOTT.values())
        self.assertEqual(db['lsj_licencverzio_valtas'], 1)
        self.assertEqual(db['bdb_formatumvaltozas'], 2)
        self.assertEqual(db['joshua_forrasvaltas'], 2)
        self.assertEqual(db['kutatoi_azonositas_feloldodott'], 3)

    def test_leiro_valtozas_listan_kivul_ismeretlen(self):
        # a listán szereplő (ALVIL-001) leíró-bővülés elfogadott; ugyanaz a változás egy listán kívüli motívumnál ismeretlen
        regi = '*Ez a blokk a `[ID: %s]` motívum 2 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'
        uj = ('*Ez a blokk a `[ID: %s]` motívum 2 Strong-tokenjét fedi, szerepenként a szerepmátrix (`szotar_szerepek.tsv`) '
              'sorrendjében, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*')
        e = osztaly(blokk('szocikkek', [regi % 'ALVIL-001']), blokk('szocikkek', [uj % 'ALVIL-001']), 'ALVIL-001_TUDOMANYOS.md')
        self.assertEqual(e['felhasznalo_elfogadva']['torolt'], [regi % 'ALVIL-001'])
        self.assertNotIn(R.ISMERETLEN, e)
        e2 = osztaly(blokk('szocikkek', [regi % 'LISTAN-KIVUL-001']), blokk('szocikkek', [uj % 'LISTAN-KIVUL-001']),
                     'LISTAN-KIVUL-001_TUDOMANYOS.md')
        self.assertIn(R.ISMERETLEN, e2)

    def test_12_par_csoportjai(self):
        import collections
        db = collections.Counter(R.FELHASZNALO_ELFOGADOTT.values())
        self.assertEqual(db['leiro_mondat_bovult'], 8)
        self.assertEqual(db['f87_glossza_javitas'], 4)

    def test_elfogadott_sorok_szamolasa_nem_dict_ertekek(self):
        # SORokat számolunk (kulcsonkénti elvárt darabszám), nem a dict kulcsait/értékeit
        self.assertEqual(set(R.FELHASZNALO_DARAB), set(R.FELHASZNALO_ELFOGADOTT))
        self.assertEqual(sum(R.FELHASZNALO_DARAB.values()), 44)
        import collections
        sor_db = collections.Counter()
        for k, n in R.FELHASZNALO_DARAB.items():
            sor_db[R.FELHASZNALO_ELFOGADOTT[k]] += n
        self.assertEqual(dict(sor_db), {
            'forditas_ubs_forras_elavult': 14, 'joshua_forrasvaltas': 2, 'bdb_formatumvaltozas': 2,
            'lsj_licencverzio_valtas': 1, 'szamozas_elteres_fuggobe_valt': 6,
            'szamozas_elteres_helyorzo_feloldodott': 4, 'kutatoi_azonositas_feloldodott': 3,
            'leiro_mondat_bovult': 8, 'f87_glossza_javitas': 4})

    def test_darabszamon_felul_azonos_sor_ismeretlen(self):
        sor = '- LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) — CC BY-SA 3.0'
        self.assertEqual(R.FELHASZNALO_DARAB[('ISTENTISZT-001_TORZSCIKK.md', sor)], 1)
        eles = '## Források és licenc\n' + sor + '\n' + sor + '\n'
        e = osztaly(eles, '## Források és licenc\n', 'ISTENTISZT-001_TORZSCIKK.md')
        self.assertEqual(e['felhasznalo_elfogadva']['torolt'], [sor])
        self.assertEqual(e[R.ISMERETLEN]['torolt'], [sor])


SZOTARI = '## 5. Szótári háttér — szerepek és lefedettség\n'


def torzs5(*sorok):
    return SZOTARI + '\n'.join(sorok) + '\n'


def mai_forras(nyelv, sorrend):
    return next(r[3] for r in R._mai_matrix() if r[0] == nyelv and r[1] == sorrend)


class Szukites113(unittest.TestCase):
    """#113 (DT-F113a): minden ismert fajta a változás fajtája szerint dönt, nem a blokk szerint. Mindegyik
    negatív teszt a szűkített ágat éri: a korábbi feltételek (helyőrző, kiejtés, jelölés, kanon) nem fogják meg."""

    def _nem_korabbi_ag(self, a, b):
        self.assertNotIn(a.strip(), R._HELYORZO)
        self.assertFalse(R._kiejtes_kulonbseg(a, b))
        self.assertFalse(R._jeloles_kulonbseg(a, b))
        self.assertNotEqual(R._kanon(a), R._kanon(b))

    # --- 1. hely: szerep ---
    def test_szerep_szabad_mondat_ismeretlen(self):
        a, b = 'egy szabad magyar mondat a cellában', 'egy másik, szintén szabad mondat'
        self._nem_korabbi_ag(a, b)
        self.assertEqual(R._mezo_kat(a, b, 'szerep', '5. Szótári háttér', 'Teológiai szócikk', 1), R.ISMERETLEN)
        e = osztaly(torzs5('| Teológiai szócikk | %s | x |' % a), torzs5('| Teológiai szócikk | %s | x |' % b),
                    'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(e), {R.ISMERETLEN})

    def test_szerep_regi_matrix_forras_mai_renderelt_forras(self):
        # a #9 előtti mátrix (0d7e9dec) forrása -> a mai forrás renderelt alakja, ugyanabban a szerep-cellában
        regi = R.REGI_SZEREPMATRIX_0D7E9DEC[('gorog', 3)][1]
        uj = R._olvaso_forras(mai_forras('gorog', 3))
        self.assertNotEqual(regi, uj)
        e = osztaly(torzs5('| Teológiai szócikk | %s | x |' % regi), torzs5('| Teológiai szócikk | %s | x |' % uj),
                    'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(e), {'szerep'})

    def test_szerep_regi_tablan_kivuli_nev_ismeretlen(self):
        # a rögzített régi táblában nem szereplő név (pl. Cremer (1895)) nem számol el, akkor sem, ha az új oldal helyes
        uj = R._olvaso_forras(mai_forras('gorog', 3))
        self.assertEqual(R._mezo_kat('Cremer (1895)', uj, 'szerep', '5. Szótári háttér', 'Teológiai szócikk', 1),
                         R.ISMERETLEN)

    def test_ubs_dntg_mounce(self):
        # DT-F113a: `UBS DNTG` -> `Mounce` csak akkor szerep, ha mindkettő a mátrix forrásneve ÉS a cella szerepéhez
        # a mátrix ténylegesen ezt a cserét rendeli. A 9. (Versenkénti jelentés) görög cellában nem: ismeretlen.
        sz = '5. Szótári háttér'
        a = mai_forras('gorog', 4)          # UBS DNTG (Louw–Nida): mátrix-forrásnév, de a 4. szerepé
        b = mai_forras('gorog', 5)          # UBS DNTG glossza + ...; Mounce kiegészítő: mátrix-forrásnév, az 5. szerepé
        self._nem_korabbi_ag(a, b)
        self.assertEqual(R._mezo_kat(a, b, 'szerep', sz, 'Versenkénti jelentés', 1), R.ISMERETLEN)
        self.assertEqual(R._mezo_kat(R.REGI_SZEREPMATRIX_0D7E9DEC[('gorog', 9)][1], 'Mounce', 'szerep', sz,
                                     'Versenkénti jelentés', 1), R.ISMERETLEN)
        # a cella saját szerepének régi -> mai (renderelt) forrása viszont szerep (a 3. szerepnél a kettő eltér)
        self.assertEqual(R._mezo_kat(R.REGI_SZEREPMATRIX_0D7E9DEC[('gorog', 3)][1],
                                     R._olvaso_forras(mai_forras('gorog', 3)), 'szerep', sz, 'Teológiai szócikk', 1),
                         'szerep')

    def test_lefedettseg_cella_renderfuggveny(self):
        # lefedettség-cella: az új érték a renderfüggvény (szerep_lefedettseg_cella) értéke: H7121 héber 1. = BDB 2.c
        e = osztaly(torzs5('| H7121 | TBESH | BDB |'), torzs5('| H7121 | BDB 2.c (DT-F42a) | BDB |'),
                    'TESZT-001_TORZSCIKK.md')
        self.assertEqual(set(e), {'szerep'})
        # ugyanez a csere egy másik tokennél nem a renderfüggvény értéke: ismeretlen
        self.assertEqual(R._mezo_kat('TBESH', 'BDB 2.c (DT-F42a)', 'szerep', '5. Szótári háttér', 'H9999', 1),
                         R.ISMERETLEN)

    def test_jelmagyarazat_mondat_csere_ismeretlen(self):
        # a jelmagyarázat-mondat szabad szöveg: nincs cellája a mátrixban, a cseréje nem szerep-változás
        regi = 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` vagy `nincs adatosítva`.'
        uj = 'A cella értéke: forrás-hivatkozás, `a forrás nem tárgyalja`, `nincs forrás` vagy `javaslat`.'
        e = osztaly(torzs5(regi), torzs5(uj), 'TESZT-001_TORZSCIKK.md')
        self.assertIn(R.ISMERETLEN, e)

    # --- 2. hely: licenc ---
    def test_licenc_jelzo_csere(self):
        self.assertEqual(R._mezo_kat('- `adat/x.tsv` (projekt-adat)', '- `adat/x.tsv` (minden jog fenntartva)',
                                     'licenc', 'idezes'), 'licenc')
        self.assertEqual(R._mezo_kat('projekt-adat', 'minden jog fenntartva', 'licenc', 'kolofon'), 'licenc')

    def test_licenc_nem_licencszoveg_ismeretlen(self):
        self._nem_korabbi_ag('régi sor', 'új sor')
        self.assertEqual(R._mezo_kat('régi sor', 'új sor', 'licenc', 'idezes'), R.ISMERETLEN)
        # licencjelző -> nem licenc szöveg is ismeretlen
        self.assertEqual(R._mezo_kat('projekt-adat', 'valami más', 'licenc', 'kolofon'), R.ISMERETLEN)

    def test_licenc_bovult_lista(self):
        regi = '| `x.tsv` | `adat/x.tsv` | minden jog fenntartva | elofordulasok |'
        uj = '| `x.tsv` | `adat/x.tsv` | minden jog fenntartva | elofordulasok, szocikkek |'
        self.assertEqual(set(osztaly(blokk('kolofon', [regi]), blokk('kolofon', [uj]))), {'licenc'})

    def test_licenc_lista_tetel_kiesik_ismeretlen(self):
        self.assertEqual(R._mezo_kat('elofordulasok, szocikkek', 'szocikkek, kapcsolatok', 'licenc', 'kolofon'),
                         R.ISMERETLEN)
        regi = '| `x.tsv` | `adat/x.tsv` | minden jog fenntartva | elofordulasok, szocikkek |'
        uj = '| `x.tsv` | `adat/x.tsv` | minden jog fenntartva | szocikkek, kapcsolatok |'
        self.assertEqual(set(osztaly(blokk('kolofon', [regi]), blokk('kolofon', [uj]))), {R.ISMERETLEN})

    def test_licenc_ertekek_adatbol(self):
        # az adat/licencek.tsv `licenc` oszlopából: pl. `CC BY-SA 4.0` (SDBH), `közkincs` (vezető rész)
        self.assertIn('CC BY-SA 4.0', R._licenc_ertekek())
        self.assertIn('közkincs', R._licenc_ertekek())

    # --- 3. hely: szám ---
    def test_szam_igehely_ismeretlen(self):
        for a, b in (('Zsolt(LXX) 87:11', 'Zsolt(LXX) 87:12'), ('1Móz 3:16', '1Móz 3:17'), ('BDB 2.c', 'BDB 3.c')):
            self._nem_korabbi_ag(a, b)
            self.assertEqual(R._mezo_kat(a, b, 'lxx_korpusz', 'lxx'), R.ISMERETLEN, a)
        e = osztaly(blokk('lxx', ['| [Jób 1:1](#a) | Zsolt(LXX) 87:11 | G0001 |']),
                    blokk('lxx', ['| [Jób 1:1](#a) | Zsolt(LXX) 87:12 | G0001 |']))
        self.assertEqual(set(e), {R.ISMERETLEN})

    def test_szam_darabszam_elfogadott(self):
        self.assertTrue(R._darabszam_frissules('- TSK: Mt 6:33 (Votes: 15)', '- TSK: Mt 6:33 (Votes: 17)'))
        self.assertTrue(R._darabszam_frissules('*Összesítés: egyező=54, eltérő=0.*', '*Összesítés: egyező=57, eltérő=3.*'))
        self.assertTrue(R._darabszam_frissules('Kol 3:23 (71)', 'Kol 3:23 (72)'))
        self.assertTrue(R._darabszam_frissules('motívum 0 elutasított jelöltjét', 'motívum 2 elutasított jelöltjét'))
        self.assertTrue(R._darabszam_frissules('12', '14'))
        e = osztaly(blokk('kereszthivatkozasok', ['#### Préd 9:12', '- TSK: Ézs 38:18 (Votes: 15)']),
                    blokk('kereszthivatkozasok', ['#### Préd 9:12', '- TSK: Ézs 38:18 (Votes: 17)']))
        self.assertNotIn(R.ISMERETLEN, e)
        e2 = osztaly(blokk('lxx', ['*Összesítés: egyező=54, eltérő=0.*']), blokk('lxx', ['*Összesítés: egyező=57, eltérő=3.*']))
        self.assertNotIn(R.ISMERETLEN, e2)

    # --- 4. hely: LXX-állapot ---
    def test_lxx_azonos_fok_es_visszalepes_ismeretlen(self):
        for a, b in (('egyező', 'eltérő'), ('eltérő', 'egyező'), ('eltérő', 'kutatói azonosítás függőben'),
                     ('kutatói azonosítás függőben', 'szamozas_elteres')):
            self.assertEqual(R._mezo_kat(a, b, 'lxx_korpusz', 'lxx'), R.ISMERETLEN, (a, b))
            e = osztaly(blokk('lxx', ['| Jób 1:1 | %s |' % a]), blokk('lxx', ['| Jób 1:1 | %s |' % b]))
            self.assertEqual(set(e), {R.ISMERETLEN}, (a, b))

    def test_lxx_allapot_helyorzo_ismeretlen(self):
        self.assertEqual(R._mezo_kat('egyező', '—', 'lxx_korpusz', 'lxx'), R.ISMERETLEN)
        e = osztaly(blokk('lxx', ['| Jób 1:1 | egyező |']), blokk('lxx', ['| Jób 1:1 | — |']))
        self.assertIn(R.ISMERETLEN, e)

    def test_lxx_elore_lepes_elfogadott(self):
        for a, b in (('kutatói azonosítás függőben', 'eltérő'), ('szamozas_elteres', 'kutatói azonosítás függőben'),
                     ('—', 'egyező')):
            e = osztaly(blokk('lxx', ['| Jób 1:1 | %s |' % a]), blokk('lxx', ['| Jób 1:1 | %s |' % b]))
            self.assertEqual(set(e), {'lxx_korpusz'}, (a, b))

    def test_kanon_nem_olvasztja_az_allapotot(self):
        self.assertNotEqual(R._kanon('egyező'), R._kanon('eltérő'))
        self.assertEqual(R._kanon('magas · tartalom-alapú[^1]'), R._kanon('magas · szó-szintű-gépi[^1]'))

    # --- 5. hely: zárójeles átírás ---
    def test_kiejtes_magyar_szo_ismeretlen_par_agon(self):
        # az (1) lépés nem-None ága: a normalizált kulccsal párosított sor
        regi, uj = '**H3548** · כֹּהֵן (pap)', '**H3548** · כֹּהֵן (király)'
        self.assertEqual(R._kulcs(regi), R._kulcs(uj))          # az (1) lépésben párosul
        self.assertIsNone(R._par_kategoria(regi, uj))            # a szűkített (1) ág nem fogadja el
        e = osztaly(blokk('szocikkek', ['### Héber szavak: H3548', '#### 2. Mélységi szócikk', regi]),
                    blokk('szocikkek', ['### Héber szavak: H3548', '#### 2. Mélységi szócikk', uj]))
        self.assertEqual(set(e), {R.ISMERETLEN})

    def test_kiejtes_magyar_szo_ismeretlen_cella_agon(self):
        self.assertFalse(R._kiejtes_kulonbseg('כֹּהֵן (pap)', 'כֹּהֵן (király)'))
        self.assertEqual(R._mezo_kat('כֹּהֵן (pap)', 'כֹּהֵן (király)', 'lxx_korpusz', 'lxx'), R.ISMERETLEN)
        self.assertEqual(R._mezo_kat('ἀβύσσου (mélység)', 'ἀβύσσου (szakadék)', 'lxx_korpusz', 'lxx'), R.ISMERETLEN)
        e = osztaly(blokk('lxx', ['| Jób 1:1 | ἀβύσσου (mélység) | G0012 |']),
                    blokk('lxx', ['| Jób 1:1 | ἀβύσσου (szakadék) | G0012 |']))
        self.assertEqual(set(e), {R.ISMERETLEN})

    def test_kiejtes_eles_esetek(self):
        for a, b in (('ἐπικαλέσηται (epikalesētai)', 'ἐπικαλέσηται (epikaleszétai)'),
                     ('ἀβύσσου (abussou)', 'ἀβύσσου (abüsszú)'),
                     ('ᾅδου (ᾅδης, Hadēs G0086)', 'ᾅδου (ᾅδης, Hadész G0086)')):
            self.assertTrue(R._kiejtes_kulonbseg(a, b), a)
            self.assertEqual(R._par_kategoria(a, b), 'kiejtes', a)
            self.assertEqual(R._mezo_kat(a, b, 'lxx_korpusz', 'lxx'), 'kiejtes', a)

    def test_atirasnak_tunik(self):
        self.assertTrue(R._atirasnak_tunik('epikalesētai'))
        self.assertTrue(R._atirasnak_tunik("she.'ol"))
        self.assertFalse(R._atirasnak_tunik('ᾅδης'))
        self.assertFalse(R._atirasnak_tunik(''))

    def test_regi_matrix_kivonat(self):
        # a 0d7e9dec-mátrix rögzített kivonata: 26 sor, (nyelv, sorrend) -> (szerep, forrás, állapot)
        self.assertEqual(len(R.REGI_SZEREPMATRIX_0D7E9DEC), 26)
        self.assertEqual(R.REGI_SZEREPMATRIX_0D7E9DEC[('heber', 1)], ('Alapjelentés', 'TBESH', 'adatosítva'))


if __name__ == '__main__':
    unittest.main()
