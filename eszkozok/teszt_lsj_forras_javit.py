#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_lsj_forras_javit.py -- F0.43: az `lsj_forras_javit.py` és az `adat/lsj_forras_javitas.tsv` tesztjei.

    python eszkozok/teszt_lsj_forras_javit.py

  séma és kapuk:  a betöltő elutasítja a hibás sort; a mai tábla ép és egyezik a nyers táblával
  alkalmazás:     a nyers `lsj` sorokra (a build olvasójával, `general.tsv_beolvas`) a csere és a kihagyás darabszáma
  tartalom:       a csere-szöveg nem pótszöveg; a kizárt és az elfogadott kézi sorok; a lemma-kulcsok
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import lsj_forras_javit as L  # noqa: E402

TABLA_FEJ = '\t'.join(L.FEJLEC)


def sor(**kw):
    r = {'strong': 'G0002', 'tipus': 'nincs_szocikk', 'osztaly': 'A1_nev_helyorzo', 'modul_hash': 'h', 'perseus_kulcs': '',
         'perseus_azonosito': '', 'modszer': 'gepi_nincs_lemma_egyezes', 'szoveg': '', 'jelzes': '', 'indoklas': 'ok',
         'proveniencia': 'scope=x | forras=y | ts=2026-11-24'}
    r.update(kw)
    return '\t'.join(r[o] for o in L.FEJLEC)


class Betolto(unittest.TestCase):
    def _tabla(self, *sorok, fej=TABLA_FEJ):
        import tempfile
        d = tempfile.mkdtemp()
        ut = os.path.join(d, 't.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# megjegyzés\n' + fej + '\n' + '\n'.join(sorok) + '\n')
        return ut

    def test_ep_sor_betoltheto(self):
        j = L.betolt(self._tabla(sor(), sor(strong='G0003', tipus='perseus_csere', szoveg='x', perseus_kulcs='k',
                                             perseus_azonosito='eng1#n1', modszer='gepi_lemma_egyezes')))
        self.assertEqual(sorted(j), ['G0002', 'G0003'])

    def test_hibas_sorok_elutasitva(self):
        for nev, s in (('ketszer', None), ('tipus', sor(tipus='torles')), ('modszer', sor(modszer='fejbol')),
                       ('csere_szoveg_nelkul', sor(tipus='perseus_csere')),
                       ('nincs_szoveggel', sor(szoveg='szöveg')),
                       ('csere_kulcs_nelkul', sor(tipus='perseus_csere', szoveg='x')),
                       ('szulo_jelzes_nelkul', sor(tipus='perseus_szulo', szoveg='x', perseus_kulcs='k', perseus_azonosito='e#n')),
                       ('jelzes_a_cserenel', sor(tipus='perseus_csere', szoveg='x', perseus_kulcs='k', perseus_azonosito='e#n',
                                                 jelzes='j')),
                       ('proveniencia_nelkul', sor(proveniencia='')), ('indoklas_nelkul', sor(indoklas='')),
                       ('strong', sor(strong='G2')), ('oszlopszam', sor() + '\tfelesleg')):
            with self.subTest(nev):
                sorok = (sor(), sor()) if s is None else (s,)
                with self.assertRaises(L.JavitasHiba):
                    L.betolt(self._tabla(*sorok))

    def test_fejlec_hiba(self):
        with self.assertRaises(L.JavitasHiba):
            L.betolt(self._tabla(sor(), fej='strong\ttipus'))


class Alkalmazas(unittest.TestCase):
    def test_csere_kihagyas_hash(self):
        nyers = [['G0001', 'G1', 'a'], ['G0002', 'G2', 'név-helyőrző'], ['G0003', 'G3', 'Strong-mondat'], ['G0004', 'G4', 'LSJ']]
        j = {'G0002': {'strong': 'G0002', 'tipus': 'nincs_szocikk', 'modul_hash': L.modul_hash('név-helyőrző'), 'szoveg': '', 'jelzes': ''},
             'G0003': {'strong': 'G0003', 'tipus': 'perseus_csere', 'modul_hash': L.modul_hash('Strong-mondat'), 'szoveg': 'LSJ-szöveg', 'jelzes': ''}}
        ki, db = L.alkalmaz(nyers, 0, 2, j)
        self.assertEqual([r[0] for r in ki], ['G0001', 'G0002', 'G0003', 'G0004'])
        self.assertEqual(ki[1][2], '', 'a nincs_szocikk sor üres szöveggel marad (az olvasó így ismeri fel a döntést)')
        self.assertEqual(ki[2][2], 'LSJ-szöveg')
        self.assertEqual(ki[0][2], 'a', 'a döntés nélküli sor változatlan')
        self.assertEqual(nyers[2][2], 'Strong-mondat', 'a bemenet nem módosul')
        self.assertEqual(db, {'perseus_csere': 1, 'perseus_szulo': 0, 'nincs_szocikk': 1})

    def test_szulo_jelzessel_elol(self):
        nyers = [['G0003', 'G3', 'Strong-mondat']]
        j = {'G0003': {'strong': 'G0003', 'tipus': 'perseus_szulo', 'modul_hash': L.modul_hash('Strong-mondat'),
                       'szoveg': 'ὅμοιος, α, ον', 'jelzes': 'Jelzés.'}}
        ki, db = L.alkalmaz(nyers, 0, 2, j)
        self.assertEqual(ki[0][2], 'Jelzés. ὅμοιος, α, ον')
        self.assertEqual(db['perseus_szulo'], 1)

    def test_megvaltozott_nyers_sor_megallit(self):
        j = {'G0002': {'strong': 'G0002', 'tipus': 'nincs_szocikk', 'modul_hash': L.modul_hash('régi'), 'szoveg': ''}}
        with self.assertRaises(L.JavitasHiba):
            L.alkalmaz([['G0002', 'G2', 'új szöveg']], 0, 2, j)

    def test_hianyzo_strong_megallit(self):
        j = {'G0009': {'strong': 'G0009', 'tipus': 'nincs_szocikk', 'modul_hash': 'h', 'szoveg': ''}}
        with self.assertRaises(L.JavitasHiba):
            L.alkalmaz([['G0002', 'G2', 'x']], 0, 2, j)


class MaiTabla(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j = L.betolt()

    def test_ellenorzes_zold(self):
        self.assertEqual(L.ellenoriz(), [])

    def test_darabszam_a_meres_szerint(self):
        """A #864 mérés A-osztályai (942) és a 2. osztály 82 sorából a `megtartas` nélküliek (68): mindegyik pontosan egyszer."""
        b = L.b_dontesek()
        tartott = {s for s, r in b.items() if r['dontes'] != 'megtartas'}
        self.assertEqual((len(b), len(tartott)), (82, 68))
        self.assertEqual(len(self.j), 942 + 68)
        self.assertEqual(set(self.j), set(L.osztalyok()) | tartott)
        self.assertFalse(set(L.osztalyok()) & set(b), 'az A- és a B-osztály külön halmaz')

    def test_a_build_olvasojaval(self):
        """A `sqlite_epit` olvasója (`general.tsv_beolvas`) ugyanazt a modul-lenyomatot adja, mint a nyers tábla."""
        fej, sorok = G.tsv_beolvas(os.path.join(L.ROOT, L.NYERS))
        rows = [[r[f] for f in fej] for r in sorok]
        ki, db = L.alkalmaz(rows, fej.index('Strong_padded'), fej.index('Teljes_szocikk'), self.j)
        self.assertEqual(len(ki), len(rows))
        self.assertEqual(sum(db.values()), 942 + 68)
        uresek = {r[0] for r in ki if not r[2].strip()}
        self.assertEqual(uresek, {s for s, r in self.j.items() if r['tipus'] == 'nincs_szocikk'})

    def test_a_csere_szoveg_nem_potszoveg(self):
        for s, r in self.j.items():
            if r['tipus'] == 'nincs_szocikk':
                continue
            sz = r['szoveg']
            self.assertNotIn('Defined by LSJ', sz, s)
            self.assertNotIn('no Definition found', sz, s)
            self.assertNotRegex(sz, r'\b(?:from|of) G\d{2,4}\b', s)
            self.assertRegex(sz[:3], r'[Ͱ-Ͽἀ-῿]', s)       # a szócikk görög fejszóval kezdődik
            self.assertNotRegex(sz, r'\s[,.;:)]', s)         # a jelölés-eltávolítás szóközei rendezve
            self.assertFalse(L.csonka(sz), s)

    def test_csere_kulcs_a_tbesg_lemmaval_egyezik(self):
        """A `gepi_lemma_egyezes` sor Perseus-kulcsa (Beta-kódból Unicode-ra) pontosan egyezik a TBESG-lemmával."""
        lemma = L.tbesg_lemmak(os.path.join(L.ROOT, L.TBESG))
        db = 0
        for s, r in self.j.items():
            if r['modszer'] == 'gepi_lemma_egyezes':
                db += 1
                kulcsok = {L.kulcs_pontos(L.beta_unicode(k)) for k in r['perseus_kulcs'].split(';')}
                self.assertEqual(kulcsok, {L.kulcs_pontos(lemma[s])}, s)
        self.assertGreater(db, 150)

    def test_kezi_kulcsok_megvannak(self):
        for s, k in L.KEZI_KULCS.items():
            self.assertEqual(self.j[s]['modszer'], 'kezi_lemma_valtozat', s)
            self.assertEqual(self.j[s]['perseus_kulcs'], k, s)
        self.assertEqual(self.j['G4326']['perseus_kulcs'], 'prosde/w2')       # προσδέω „szükséget szenved”, nem a „megköt”
        self.assertEqual(self.j['G4483']['perseus_kulcs'], 'e)rw=')           # ἐρῶ „mondani”, nem az ἐρέω „kérdez”
        self.assertEqual(self.j['G2748']['tipus'], 'nincs_szocikk')           # Kidron (helynév), nem a κέδρος (cédrus)

    def test_a_szerkesztoi_jeloles_es_a_morfema_hatar_megmarad(self):
        """A független ellenőrzés két szövegrontó hibája: a ⟨ ⟩ kiegészítés nem tűnhet el, a szigma morféma-határon nem szóvégi."""
        self.assertEqual(L.szocikk_szoveg('<foreign lang="greek">a)sfa/l&amp;lt;e&amp;gt;ia</foreign>').strip(), 'ἀσφάλ⟨ε⟩ια')
        self.assertEqual(L.beta_unicode('h(ss-a/omai'), 'ἡσσ-άομαι')
        for s, r in self.j.items():
            self.assertNotRegex(r['szoveg'], r'\wς-\w', s)
            self.assertNotIn('&lt;', r['szoveg'], s)

    def test_kezi_kizart_sorok(self):
        for s in L.KEZI_KIZART:
            self.assertEqual((self.j[s]['tipus'], self.j[s]['modszer']), ('nincs_szocikk', 'kezi_kizaras'), s)
        # a lapon szereplő szó: az ἐπικαλέω (G1941) valódi szócikket kap, nem „csak átirányít” szöveget
        self.assertEqual(self.j['G1941']['tipus'], 'perseus_csere')
        self.assertIn('invoke', self.j['G1941']['szoveg'])

    def test_nevek_nincs_szocikk(self):
        self.assertEqual(self.j['G0002']['tipus'], 'nincs_szocikk')   # Ἀαρών
        self.assertEqual(self.j['G3165']['tipus'], 'nincs_szocikk')   # μέ
        self.assertEqual(self.j['G1097']['tipus'], 'perseus_csere')   # γινώσκω ~ γιγνώσκω (a név-besorolás tévedése)


    def test_b_osztaly_darabszam_es_jelzes(self):
        """A szerkesztői döntés (2026-11-24): 36 pontos csere, 27 szülőszócikk kimondott jelzéssel, 5 nincs; 14 marad."""
        from collections import Counter
        b = Counter(r['dontes'] for r in L.b_dontesek().values())
        self.assertEqual(b, {'csere_pontos': 36, 'csere_szulo': 27, 'nincs_szocikk': 5, 'megtartas': 14})
        szulok = [r for r in self.j.values() if r['tipus'] == 'perseus_szulo']
        self.assertEqual(len(szulok), 27)
        for r in szulok:
            self.assertRegex(r['jelzes'], r'^Az LSJ-ben önálló szócikke nincs; a\(z\) \S+ szócikke, amely ezt az alakot tárgyalja\.$', r['strong'])
        self.assertIn('ὅμοιος', self.j['G3668']['jelzes'])      # ὁμοίως → ὅμοιος
        self.assertIn('πρέσβυς', self.j['G4245']['jelzes'])     # πρεσβύτερος → πρέσβυς
        for s in ('G0149', 'G0976', 'G1166'):                    # a megtartott sorok nincsenek a táblában
            self.assertNotIn(s, self.j)

    def test_b_pontos_cserek(self):
        self.assertEqual(self.j['G3041']['perseus_kulcs'], 'li/mnh')                       # λίμνη (nem λῐμήν)
        self.assertEqual(self.j['G1650']['perseus_kulcs'], 'e)/legxos1;e)/legxos2')         # ἔλεγχος, a hozzáfűzött ἐν nélkül
        self.assertNotIn('OF PLACE', self.j['G1650']['szoveg'])                              # az ἐν szócikke
        self.assertEqual(self.j['G0838']['tipus'], 'perseus_csere')                         # αὔξησις (nem γάρ)


class OlvasoJelzes(unittest.TestCase):
    """Az olvasó `szo.lsj` blokkja: a döntött `nincs_szocikk` sor kimondja a forrás határát, a döntés nélküli hiány a szokásos jelzést adja."""

    def test_dontott_nincs_vs_nincs_sor(self):
        import sqlite3
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'olvaso_szerver'))
        import lekerdezesek as Q
        con = sqlite3.connect(':memory:')
        con.execute('CREATE TABLE lsj (strong_padded TEXT, strong_eredeti TEXT, teljes_szocikk TEXT, strong TEXT)')
        con.executemany('INSERT INTO lsj VALUES (?,?,?,?)', [('G0002', 'G2', '', 'G0002'), ('G0004', 'G4', 'ἀβαρής, ές', 'G0004')])
        self.assertTrue(Q.lsj_dontott_nincs(con, 'G0002'))      # döntött: a modul pótszövege kiesett
        self.assertFalse(Q.lsj_dontott_nincs(con, 'G0004'))     # van szöveg
        self.assertFalse(Q.lsj_dontott_nincs(con, 'G6000'))     # nincs sor (nincs döntés): a szokásos üres jelzés
        self.assertEqual(Q.lsj(con, 'G0002'), '')

    def test_felirat_igaz_allitast_tesz(self):
        t = open(os.path.join(L.ROOT, 'eszkozok', 'olvaso_szerver', 'konfig', 'feliratok.tsv'), encoding='utf-8').read()
        sor = [x for x in t.split('\n') if x.startswith('lsj.nincs_szocikk\t')][0].split('\t')[1]
        self.assertIn('Perseus', sor)                           # a forrásról állít, nem az LSJ-ről általában
        self.assertNotIn('nincs megfelelő szócikk', sor)


class EpitesiAg(unittest.TestCase):
    """A `sqlite_epit.py` `lsj`-ága: a javítás a táblába épül, a darabszám a megjegyzésekbe kerül (mint a teljes építésben)."""

    def test_lsj_tabla_epitese(self):
        import sqlite_epit as S
        e = object.__new__(S.Epito)
        e.gyoker, e.mod, e.minta, e.norm_jelentes, e.megjegyzesek = L.ROOT, 'teljes', None, {}, []
        e.licenc_ellenorzes = lambda n, lic: True
        kapott = {}
        e.tabla = lambda nev, oszlopok, sorok, lic, indexek=(): kapott.update(sorok=[tuple(s) for s in sorok], oszlopok=oszlopok)
        e._altalanos_betolt('lsj', 'konkordancia/LSJ_teljes.tsv', 'Strong_padded', None, ['LSJ'])
        self.assertEqual([o[0] for o in kapott['oszlopok']], ['strong_padded', 'strong_eredeti', 'teljes_szocikk', 'strong'])
        d = {r[0]: r for r in kapott['sorok']}
        self.assertEqual(d['G0002'][2], '')                                  # Ἀαρών: üres szöveggel marad
        self.assertTrue(d['G1941'][2].startswith('ἐπικᾰλέω'))                 # a Perseus-szócikk
        self.assertTrue(d['G0264'][2].startswith('ἁμαρτάνω'))                # a döntés nélküli sor változatlan
        self.assertEqual(len(kapott['sorok']), len(L.nyers_tabla()))
        self.assertTrue(any(m.startswith('lsj_forras_javitas:') for m in e.megjegyzesek))


class Kulcsok(unittest.TestCase):
    def test_pontos_kulcs_ekezettel_egyezik(self):
        self.assertEqual(L.kulcs_pontos('ἐπικᾰλέω'), L.kulcs_pontos('ἐπικαλέω'))        # a hosszúságjel nem számít
        self.assertNotEqual(L.kulcs_pontos('εἷς'), L.kulcs_pontos('εἰς'))              # az ékezet igen
        self.assertNotEqual(L.kulcs_pontos('Σίμων'), L.kulcs_pontos('σίμων'))          # a név nem közszó
        self.assertEqual(L.kulcs_pontos('δοῦλος2'), L.kulcs_pontos('δοῦλος'))          # a homográf-szám nem számít

    def test_laza_kulcs_irasmod(self):
        self.assertEqual(L.kulcs_laza('γινώσκω'), L.kulcs_laza('γιγνώσκω'))
        self.assertEqual(L.kulcs_laza('κρείττων'), L.kulcs_laza('κρείσσων'))

    def test_csonka_szocikk(self):
        self.assertTrue(L.csonka('καταπλέω , lon.'))
        self.assertTrue(L.csonka('ἐπιδέχομαι, Ion. etc.'))
        self.assertFalse(L.csonka('ἐπενδύω, v. ἐπενδύνω.'))
        self.assertFalse(L.csonka('μία, fem. of εἷς (q. v.).'))

    def test_beta_unicode(self):
        self.assertEqual(L.beta_unicode('e)pikale/w'), 'ἐπικαλέω')
        self.assertEqual(L.beta_unicode('*)/efesos'), 'Ἔφεσος')


if __name__ == '__main__':
    unittest.main(verbosity=2)
