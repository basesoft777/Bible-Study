#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brief_lezaras.py tesztjei: a lezaras feltetele, az N-tetel lezarasa, a ket kapu (ideiglenes git-repokon)."""

import os
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brief_lezaras as B  # noqa: E402
import feladatok as F  # noqa: E402
import gepi_commit_uzenet as U  # noqa: E402


def git(cwd, *a):
    return subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'core.autocrlf=false',
                           '-c', 'i18n.commitEncoding=UTF-8'] + list(a),
                          cwd=cwd, capture_output=True, check=True).stdout.decode('utf-8')


def brief(szam=900, allapot='megallt', kovetkezo='Te: a draft PR áttekintése; a merge a felhasználóé',
          ag='claude/proba-x', lezar=None, tipus='feladat', pr=None):
    sorok = ['---', 'feladat: %d' % szam, 'cim: Próba', 'kod: PROBA', 'tipus: %s' % tipus, 'fazis: folyamat',
             'modell: sonnet', 'allapot: %s' % allapot, 'ad: próba', 'kovetkezo: "%s"' % kovetkezo,
             'munka: folyamat', 'ir: [x.py]', 'fugg: []']
    if ag:
        sorok.append('ag: %s' % ag)
    if pr is not None:
        sorok.append('pr: %s' % pr)
    if lezar is not None:
        sorok.append('lezar: [%s]' % ', '.join(lezar))
    sorok += ['---', '', '# Próba', '']
    return '\n'.join(sorok)


NYITOTT_MINTA = '\n'.join([
    '# Nyitott feladatok', '',
    '## Kisebb tételek',
    '* **N200 — a próba-tétel címe.** Leírás.',
    '- **N-F200d — helyőrzős tétel.** Leírás.',
    '* **N201 — LEZÁRVA (2026-11-11, DT1) — már lezárt tétel.** Leírás.',
    '* **N202 — egy másik tétel.** Leírás.', ''])


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = self.tmp.name
        git(self.r, 'init', '-q', '-b', 'main')
        self.ir('NYITOTT_FELADATOK.md', NYITOTT_MINTA)
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'init')

    def tearDown(self):
        self.tmp.cleanup()

    def ir(self, nev, szoveg):
        with open(os.path.join(self.r, nev), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def olvas(self, nev):
        with open(os.path.join(self.r, nev), encoding='utf-8', newline='') as f:
            return f.read()

    def pr_merge(self, ag, szam, fajlok, uzenet=None):
        """Agat nyit, a fajlokat commitolja, --no-ff merge a GitHub formaju uzenettel."""
        git(self.r, 'checkout', '-q', '-b', ag)
        for nev, szoveg in fajlok.items():
            self.ir(nev, szoveg)
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'munka')
        git(self.r, 'checkout', '-q', 'main')
        git(self.r, 'merge', '--no-ff', '-q', '-m', uzenet or 'Merge pull request #%d from basesoft777/%s' % (szam, ag), ag)


class Feltetel(Alap):
    def test_csak_merge_hatra_lezar(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief()})
        lezar, kihagy = B.lezarando(self.r)
        self.assertEqual([(b.szam, pr) for b, pr in lezar], [(900, 701)])
        self.assertEqual(kihagy, [])

    def test_mas_teendo_nem_zar(self):
        for i, kov in enumerate(['Te: draft PR; utána a második lépés; merge a felhasználóé',
                                 'Te: a merge a felhasználóé; döntés DT500',
                                 'Te: merge; nyitva N-F900a',
                                 'Te: a draft PR áttekintése',          # a merge nincs megnevezve
                                 'Folytatás: a draft PR; a merge a felhasználóé',
                                 'a merge a felhasználóé']):           # nem `Te:`
            self.pr_merge('claude/p%d' % i, 710 + i, {'F9%02d_P_BRIEF.md' % i: brief(901 + i, kovetkezo=kov, ag='claude/p%d' % i)})
        lezar, kihagy = B.lezarando(self.r)
        self.assertEqual(lezar, [])
        self.assertEqual(len(kihagy), 6)

    def test_allapot_es_tipus(self):
        self.pr_merge('claude/a', 720, {'F910_A_BRIEF.md': brief(910, allapot='dontesre_var', ag='claude/a'),
                                        'F911_B_BRIEF.md': brief(911, allapot='nem_indult', ag='claude/a')})
        lezar, _ = B.lezarando(self.r)
        self.assertEqual(lezar, [])

    def test_nincs_merge_nem_zar(self):
        git(self.r, 'checkout', '-q', '-b', 'claude/nyitott')
        self.ir('F920_N_BRIEF.md', brief(920, ag='claude/nyitott'))
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'munka')
        git(self.r, 'checkout', '-q', 'main')
        git(self.r, 'checkout', '-q', 'claude/nyitott')
        lezar, _ = B.lezarando(self.r)
        self.assertEqual(lezar, [])      # nincs PR-merge a tortenetben

    def test_pr_mezovel_is_talal(self):
        self.pr_merge('claude/masik-nev', 730, {'F930_P_BRIEF.md': brief(930, ag=None, pr=730)})
        lezar, _ = B.lezarando(self.r)
        self.assertEqual([b.szam for b, _ in lezar], [930])

    def test_a_merge_utan_valtozott_allapot_nem_zar(self):
        self.pr_merge('claude/proba-x', 740, {'F940_V_BRIEF.md': brief(940)})
        # a merge utan a menet folytatodott: uj `kovetkezo`
        self.ir('F940_V_BRIEF.md', brief(940, kovetkezo='Te: a második PR; merge a felhasználóé'))
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'folytatas')
        lezar, kihagy = B.lezarando(self.r)
        self.assertEqual(lezar, [])
        self.assertIn('valtozott', kihagy[0][1])

    def test_a_merge_utani_nem_fejlec_valtozas_nem_akadaly(self):
        self.pr_merge('claude/proba-x', 750, {'F950_T_BRIEF.md': brief(950)})
        self.ir('F950_T_BRIEF.md', self.olvas('F950_T_BRIEF.md') + '\nÚj törzssor (szamkiosztas).\n')
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'szamkiosztas: DT-F1 → DT1')
        lezar, _ = B.lezarando(self.r)
        self.assertEqual([b.szam for b, _ in lezar], [950])

    def test_lezar_mezo_ismeretlen_kulcskent_nem_akadaly(self):
        # a fejlec-elemzo meg nem ismeri a `lezar:` kulcsot -> hibak nem ures, de nem akadaly
        self.pr_merge('claude/proba-x', 760, {'F960_L_BRIEF.md': brief(960, lezar=['N200'])})
        lezar, _ = B.lezarando(self.r)
        self.assertEqual([b.szam for b, _ in lezar], [960])

    def test_lezar_lista_alakjai(self):
        self.assertEqual(B.lezar_lista(brief(lezar=['N200', 'N-F200d'])), ['N200', 'N-F200d'])
        self.assertEqual(B.lezar_lista(brief()), [])
        self.assertEqual(B.lezar_lista(brief(lezar=[])), [])


class NyitottLezaras(unittest.TestCase):
    def test_lezaras_a_mintara(self):
        uj, jel = B.nyitott_lezar(NYITOTT_MINTA, ['N200', 'N-F200d'], '2026-11-15', 701, 900)
        self.assertEqual(jel, {'N200': 'lezarva', 'N-F200d': 'lezarva'})
        self.assertIn('* **N200 — LEZÁRVA (2026-11-15, a #701 PR merge-ével, F900) — a próba-tétel címe.** Leírás.', uj)
        self.assertIn('- **N-F200d — LEZÁRVA (2026-11-15, a #701 PR merge-ével, F900) — helyőrzős tétel.** Leírás.', uj)
        self.assertEqual(uj.count('LEZÁRVA'), 3)         # + a mar lezart N201

    def test_mar_lezart_es_ismeretlen(self):
        uj, jel = B.nyitott_lezar(NYITOTT_MINTA, ['N201', 'N999'], '2026-11-15', 701, 900)
        self.assertEqual(jel, {'N201': 'mar_lezart', 'N999': 'nincs'})
        self.assertEqual(uj, NYITOTT_MINTA)

    def test_nem_szamjegy_elotag_nem_ut_ossze(self):
        # az `N20` nem lehet az `N200` sora
        uj, jel = B.nyitott_lezar(NYITOTT_MINTA, ['N20'], '2026-11-15', 701, 900)
        self.assertEqual(jel, {'N20': 'nincs'})

    def test_idempotens(self):
        egyszer, _ = B.nyitott_lezar(NYITOTT_MINTA, ['N200'], '2026-11-15', 701, 900)
        ketszer, jel = B.nyitott_lezar(egyszer, ['N200'], '2026-11-16', 702, 901)
        self.assertEqual(egyszer, ketszer)
        self.assertEqual(jel, {'N200': 'mar_lezart'})

    def test_nyitva_maradt(self):
        self.assertTrue(B.nyitva_maradt(NYITOTT_MINTA, 'N200'))
        self.assertFalse(B.nyitva_maradt(NYITOTT_MINTA, 'N201'))
        self.assertIsNone(B.nyitva_maradt(NYITOTT_MINTA, 'N999'))

    def test_crlf_megmarad(self):
        uj = B.brief_lezar_szoveg(brief().replace('\n', '\r\n'), 701, '2026-11-15')
        self.assertEqual(uj.count('\n'), uj.count('\r\n'))      # nincs kevert sorveg
        self.assertIn('allapot: lezarva\r\n', uj)

    def test_brief_lezaras_szovege(self):
        uj = B.brief_lezar_szoveg(brief(), 701, '2026-11-15')
        fej, _, hibak = F.fejlec_elemez(uj)
        self.assertEqual(fej['allapot'], 'lezarva')
        self.assertIn('PR #701', fej['kovetkezo'])
        self.assertEqual(hibak, [])


class Vegrehajtas(Alap):
    def kesz(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief(lezar=['N200', 'N-F200d'])})

    def test_szaraz_nem_ir(self):
        self.kesz()
        elotte = (self.olvas('F900_PROBA_BRIEF.md'), self.olvas('NYITOTT_FELADATOK.md'))
        lezar, _, sorok = B.vegrehajt(self.r, szaraz=True, datum='2026-11-15')
        self.assertEqual(len(lezar), 1)
        self.assertEqual((self.olvas('F900_PROBA_BRIEF.md'), self.olvas('NYITOTT_FELADATOK.md')), elotte)
        self.assertIn('1 brief zárna le', sorok[-1])
        self.assertIn('2 N-tétel zárna le', sorok[-1])

    def test_ir_es_masodik_futas_idempotens(self):
        self.kesz()
        uzenet = os.path.join(self.r, 'uzenet.txt')
        B.vegrehajt(self.r, szaraz=False, datum='2026-11-15', uzenet_fajl=uzenet)
        fej, _, hibak = F.fejlec_elemez(self.olvas('F900_PROBA_BRIEF.md'))
        self.assertEqual(fej['allapot'], 'lezarva')
        self.assertEqual(self.olvas('NYITOTT_FELADATOK.md').count('LEZÁRVA'), 3)
        with open(uzenet, encoding='utf-8') as f:
            self.assertIn('#900', f.read())
        elso = (self.olvas('F900_PROBA_BRIEF.md'), self.olvas('NYITOTT_FELADATOK.md'))
        lezar, _, _ = B.vegrehajt(self.r, szaraz=False, datum='2026-11-16')
        self.assertEqual(lezar, [])
        self.assertEqual((self.olvas('F900_PROBA_BRIEF.md'), self.olvas('NYITOTT_FELADATOK.md')), elso)

    def test_lezar_az_nem_lezart_marad_ha_nincs_merge(self):
        # nem merge-elt brief N-tetele nem zarul
        git(self.r, 'checkout', '-q', '-b', 'claude/nyitott')
        self.ir('F901_N_BRIEF.md', brief(901, ag='claude/nyitott', lezar=['N202']))
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'munka')
        B.vegrehajt(self.r, szaraz=False, datum='2026-11-15')
        self.assertEqual(self.olvas('NYITOTT_FELADATOK.md'), NYITOTT_MINTA)


class Kapu(Alap):
    def test_mergelt_de_nem_lezart(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief()})
        j = B.kapu_jelentesek(self.r)
        self.assertEqual(len(j), 1)
        self.assertIn('#701', j[0][1])
        self.assertIn('nem `lezarva`', j[0][1])

    def test_nyitva_maradt_lezar_tetel(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief(allapot='lezarva', kovetkezo='lezárva',
                                                                         lezar=['N200', 'N201'])})
        j = B.kapu_jelentesek(self.r)
        self.assertEqual(len(j), 1)
        self.assertIn('N200', j[0][1])

    def test_tiszta_allapot_nincs_jelentes(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief(allapot='lezarva', kovetkezo='lezárva',
                                                                         lezar=['N201'])})
        self.assertEqual(B.kapu_jelentesek(self.r), [])

    def test_a_vegrehajtas_utan_a_kapu_tiszta(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': brief(lezar=['N200'])})
        self.assertEqual(len(B.kapu_jelentesek(self.r)), 1)
        B.vegrehajt(self.r, szaraz=False, datum='2026-11-15')
        self.assertEqual(B.kapu_jelentesek(self.r), [])


class LezarMezo(Alap):
    """B resz: a `lezar` fejlecmezo a semaban, a kapu az `ellenoriz` kimenetben (JELENTES, nem HIBA)."""

    def fejjel(self, **kw):
        return brief(**kw).replace('munka: folyamat', 'munka: folyamat\nsav: SYSTEMS')

    def test_a_mezo_lista_es_az_elemzo_ismeri(self):
        fej, _, hibak = F.fejlec_elemez(self.fejjel(lezar=['N200', 'N-F200d']))
        self.assertEqual(fej['lezar'], ['N200', 'N-F200d'])
        self.assertEqual(hibak, [])

    def test_ervenytelen_azonosito_hiba(self):
        self.ir('F980_X_BRIEF.md', self.fejjel(szam=980, lezar=['N200', 'DT12']))
        hibak = F.ellenoriz(F.briefek_beolvas(self.r), self.r)
        self.assertEqual([h for h in hibak if 'lezar' in h[1]][0][0], 'F980_X_BRIEF.md')
        self.assertTrue(any("'DT12'" in h[1] for h in hibak))

    def test_ervenyes_azonosito_nem_hiba(self):
        self.ir('F981_X_BRIEF.md', self.fejjel(szam=981, lezar=['N200', 'N-F200d']))
        hibak = F.ellenoriz(F.briefek_beolvas(self.r), self.r)
        self.assertEqual([h for h in hibak if 'lezar' in h[1]], [])

    def test_cli_jelentes_nem_hiba(self):
        self.pr_merge('claude/proba-x', 701, {'F900_PROBA_BRIEF.md': self.fejjel(lezar=['N200'])})
        p = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feladatok.py'),
                            '--gyoker', self.r, 'ellenoriz'], capture_output=True)
        ki = p.stdout.decode('utf-8')
        self.assertIn('JELENTÉS\tF900_PROBA_BRIEF.md\t', ki)
        self.assertNotIn('HIBA\t', ki)
        self.assertEqual(p.returncode, 0)


class CommitUzenet(unittest.TestCase):
    def test_torzs_hozzafuzve_az_elso_sor_valtozatlan(self):
        u = U.uzenet(['FELADATOK.md', 'F900_P_BRIEF.md'], None, 'brief-lezárás: #900')
        self.assertTrue(u.startswith('FELADATOK.md frissítés (gép)\n'))
        self.assertTrue(u.rstrip().endswith('brief-lezárás: #900'))
        self.assertEqual(U.uzenet(['FELADATOK.md']), U.uzenet(['FELADATOK.md'], None, None))


class MergeTerkep(Alap):
    def test_github_merge_es_squash(self):
        self.pr_merge('claude/a', 5, {'F1_A_BRIEF.md': brief(1, ag='claude/a')})
        self.ir('x.txt', 'x')
        git(self.r, 'add', '-A')
        git(self.r, 'commit', '-qm', 'Squash-olt valtozas (#6)')
        t = B.pr_merge_terkep(self.r)
        self.assertEqual([(x[2], x[3]) for x in t], [(6, None), (5, 'claude/a')])

    def test_pr_szam_fejbol(self):
        self.assertEqual(B.pr_szam_fejbol({'pr': '666'}), 666)
        self.assertEqual(B.pr_szam_fejbol({'pr': 'https://github.com/o/r/pull/351'}), 351)
        self.assertIsNone(B.pr_szam_fejbol({}))


if __name__ == '__main__':
    unittest.main(verbosity=1)
