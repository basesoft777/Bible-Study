"""A sablon-javítókör (2026-11-03, a felhasználó lapnézet-észrevételei) tesztjei: a generált lapokon nincs külön ⓘ a
lábjegyzet-jel mellett, nincs ikon a „Funkció” oszlopban, nincs 15 jegyű UBS-kód a cellában, a „Funkció:” sor új
bekezdésben áll, és a „Mit mutat ez a rész?” címke nem látszik (az olvasói bekezdést láthatatlan jel azonosítja)."""

import os
import re
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

AZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AZ)
import lexikon_general as LG  # noqa: E402
import proza_1a  # noqa: E402

LAPOK = ('ISTENTISZT-001', 'ALVIL-001', 'TEREMT-002')
IKON = re.compile('[\U0001F300-\U0001FAFF☀-➿]')


def lap(motivum):
    ut = os.path.join(AZ, '..', 'lexikon', '%s_TUDOMANYOS.md' % motivum)
    with open(ut, encoding='utf-8') as f:
        return f.read()


class Egyseg(unittest.TestCase):
    def test_ikon_nelkul(self):
        self.assertEqual(LG.ikon_nelkul('🌱 alap-előfordulás'), 'alap-előfordulás')
        self.assertEqual(LG.ikon_nelkul('⚡ élve alászállás'), 'élve alászállás')
        self.assertEqual(LG.ikon_nelkul('„idézet” marad'), '„idézet” marad')
        self.assertEqual(LG.ikon_nelkul(''), '')

    def test_olvasoi_bekezdes_cimke_nelkul(self):
        b = LG.olvasoi_bekezdes('Összefoglaló.')
        self.assertNotIn('Mit mutat', b)
        self.assertTrue(b.startswith(LG.OLVASOI_CIMKE))
        self.assertTrue(b.endswith('Összefoglaló.'))


class GeneraltLapok(unittest.TestCase):
    def test_nincs_kulon_info_jel_a_labjegyzet_mellett(self):
        for m in LAPOK:
            self.assertIsNone(re.search(r'ⓘ\s*\[\^', lap(m)), m)

    def test_nincs_ikon_a_tablaban_es_az_1a_ban(self):
        for m in LAPOK:
            for sor in lap(m).split('\n'):
                if sor.startswith('| [') or sor.startswith('Funkció:'):
                    self.assertIsNone(IKON.search(sor), (m, sor[:80]))

    def test_nincs_15_jegyu_kod_az_ubs_cellaban(self):
        for m in LAPOK:
            for sor in lap(m).split('\n'):
                if sor.startswith('| ['):
                    self.assertIsNone(re.search(r'`\d{15}`', sor), (m, sor[:80]))

    def test_funkcio_sor_uj_bekezdesben(self):
        for m in LAPOK:
            sorok = lap(m).split('\n')
            for i, sor in enumerate(sorok):
                if sor.startswith('Funkció:'):
                    self.assertEqual(sorok[i - 1], '', (m, i))

    def test_cimke_nem_latszik(self):
        for m in LAPOK:
            self.assertNotIn('Mit mutat ez a rész', lap(m), m)

    def test_az_1a_merő_tovabbra_is_olvassa_a_funkciot(self):
        for m in LAPOK:
            bl = proza_1a.blokkok(lap(m))
            self.assertTrue(bl)
            self.assertTrue(any(f for _i, _p, f in bl), m)


if __name__ == '__main__':
    unittest.main()
