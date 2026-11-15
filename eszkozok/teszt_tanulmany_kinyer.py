#!/usr/bin/env python3
"""teszt_tanulmany_kinyer.py — az igehelyenkénti jelölt blokkok kinyerője (F205 M3, DT803).

A blokkok fixture-ök; a jelölt- és a motívumtábla a repón kívüli ideiglenes mappában áll. A versmegfeleltetés, a
javított Károli-KH index és a könyv-normalizáló a repó valós táblái (csak olvasva). A repóban fájl nem keletkezik és
nem változik (`test_repo_erintetlen`).

Futtatás: python -m unittest eszkozok.teszt_tanulmany_kinyer  (a repó gyökeréből)
"""
import hashlib
import io
import os
import subprocess
import sys
import tempfile
import unittest

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import general as G  # noqa: E402
import tanulmany_kinyer as TK  # noqa: E402
import tanulmany_regiszter as TR  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FEJLEC_MA = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'karoli_szo', 'azonositas_modja',
             'megbizhatosag', 'datum', 'jelolt_tipus', 'cel_id', 'cel_igehely', 'cel_alpont', 'dontes_ref']
FEJLEC_M5 = FEJLEC_MA + ['targy']
MOTIVUMOK = {'HAMART-001', 'ISTENTISZT-001'}
DATUM = '2026.11.15'
VERSMEGF = TK.versmegfeleltetes()

FUNK = ('- **funkció:** Az özönvíz utáni ígéret a föld további megátkozását zárja ki, de az ember szívének '
        'gonoszságát változatlannak nevezi.')
NEG = '- **negatív próba:** nem — a versben a föld szava áll, és az átok kérdéséről szól.'
JP = ('- **jelentéspont:** H7043 · szótár: BDB, pont nélkül [scope=H7043 | forras=bdb_vers_jelentes.py | '
      'ts=2026-11-10] · olvasat: itt a qalal ige áll, nem az árar · eltér: nem mérhető — a szótár-sor pontot nem ad')
VITA = '- **vita:** üres — a versre nincs nevesíthető képviselőjű vita'
VH = ('- **visszhang:** latin · Szent Ambrus · On Noah and the Ark 22.80 · Isten irgalmaként magyarázza, hogy a föld '
      'nem kap újabb átkot. · hcf')
VSZ = ('- **versszámozás:** azonos — Károli 8:21 = KJV 8:21 [scope=1Móz 8:21 | forras=Karoli_versmegfeleltetes.tsv | '
       'ts=2026-11-12]')
PONTOK = [FUNK, NEG, JP, VITA, VH, VSZ]


def blokk(igehely='1Móz 8:21', motivum='HAMART-001', gerinc='H0127', pontok=None):
    return '\n'.join(['<!-- IGEHELY-BLOKK: %s | motivum: %s | gerinc: %s -->' % (igehely, motivum, gerinc)]
                     + (PONTOK if pontok is None else pontok) + ['<!-- IGEHELY-BLOKK-VÉGE -->'])


def tanulmany(*blokkok, cim='# 1Mózes 8:20–22 — Próba', negyedik=''):
    reszek = [cim, '']
    if negyedik:
        reszek += ['## 4. Kapcsolódó igehelyek', '', negyedik, '']
    reszek += ['## 4/b. Igehelyenkénti jelölt blokkok', ''] + list(blokkok)
    return '\n'.join(reszek) + '\n'


def futtat(szoveg, fejlec=FEJLEC_MA, jeloltek=(), kh=None):
    return TK.kinyer(szoveg, 'genezis/proba.md', fejlec, list(jeloltek), MOTIVUMOK, DATUM, versmegf=VERSMEGF, kh=kh)


_KAR = []


def kar():
    if not _KAR:
        _KAR.append((TR.Karoli(TR.karoli_kulcsok()), TK.kh_index()))
    return _KAR[0]


class Elemzes(unittest.TestCase):
    def test_sablon_mintaja_hibatlan(self):
        """A 2. sablon 4/b. mintája (kódblokkban áll) a kinyerőn és a szövegkapukon hibátlanul megy át."""
        with io.open(os.path.join(GYOKER, 'sablonok', '2_PaRDeS_bovitett_sablon.md'), encoding='utf-8') as f:
            s = f.read()
        self.assertEqual(TK.blokkok_elemez(s), ([], []), 'a kódblokk belseje nem blokk')
        i = s.index('<!-- IGEHELY-BLOKK: 1Móz 8:21')
        j = s.index(TK.BLOKK_VEGE, i) + len(TK.BLOKK_VEGE)
        e = futtat(tanulmany(s[i:j]))
        self.assertEqual(e['hibak'], [])
        self.assertEqual(e['figyelmeztetesek'], [])
        self.assertEqual(len(e['uj_sorok']), 1)
        self.assertEqual([s['jelolt_tipus'] for s in e['varakozo']], ['jelentespont', 'visszhang'])

    def test_hianyzo_pont(self):
        e = futtat(tanulmany(blokk(pontok=PONTOK[:-1])))
        self.assertTrue(any('hiányzó pont: versszámozás' in h for h in e['hibak']), e['hibak'])

    def test_ures_ok_nelkul(self):
        e = futtat(tanulmany(blokk(pontok=PONTOK[:3] + ['- **vita:** üres'] + PONTOK[4:])))
        self.assertTrue(any('ok nélkül' in h for h in e['hibak']), e['hibak'])

    def test_sorrend_es_ismetles(self):
        e = futtat(tanulmany(blokk(pontok=[NEG, FUNK] + PONTOK[2:])))
        self.assertTrue(any('sorrendje' in h for h in e['hibak']), e['hibak'])
        e = futtat(tanulmany(blokk(pontok=[FUNK, FUNK] + PONTOK[1:])))
        self.assertTrue(any('funkció pont többször' in h for h in e['hibak']), e['hibak'])

    def test_parositatlan_jelolo(self):
        nyitott = '\n'.join(blokk().split('\n')[:-1])
        e = futtat(tanulmany(nyitott))
        self.assertTrue(any('nyitva maradt' in h for h in e['hibak']), e['hibak'])
        e = futtat(tanulmany(TK.BLOKK_VEGE))
        self.assertTrue(any('nyitó jelölő nélkül' in h for h in e['hibak']), e['hibak'])
        e = futtat(tanulmany(nyitott + '\n' + blokk('1Móz 8:22')))
        self.assertTrue(any('zárása előtt' in h for h in e['hibak']), e['hibak'])
        e = futtat(tanulmany('Szöveg <!-- IGEHELY-BLOKK: 1Móz 8:21 | motivum: — | gerinc: — --> közben'))
        self.assertTrue(any('nem a saját sorában' in h for h in e['hibak']), e['hibak'])

    def test_hibas_mezoszam(self):
        rossz = '- **visszhang:** latin · Szent Ambrus · egy mondat.'
        e = futtat(tanulmany(blokk(pontok=PONTOK[:4] + [rossz, VSZ])))
        self.assertTrue(any('öt mezője' in h for h in e['hibak']), e['hibak'])
        rossz = PONTOK[2].replace('H7043', 'qalal')
        e = futtat(tanulmany(blokk(pontok=PONTOK[:2] + [rossz] + PONTOK[3:])))
        self.assertTrue(any('nem Strong-szám' in h for h in e['hibak']), e['hibak'])

    def test_funkcio_nem_kerek_mondat(self):
        e = futtat(tanulmany(blokk(pontok=['- **funkció:** az ígéret'] + PONTOK[1:])))
        self.assertTrue(any('nem kerek mondat' in h for h in e['hibak']), e['hibak'])


class Kinyeres(unittest.TestCase):
    def test_elofordulas_sor(self):
        e = futtat(tanulmany(blokk()))
        self.assertEqual(e['hibak'], [])
        (s,) = e['uj_sorok']
        self.assertEqual(s['jelolt_tipus'], 'elofordulas')
        self.assertEqual(s['dontes'], 'nyitva')
        self.assertEqual(s['forras_kereses'], 'scope=manual | forras=genezis/proba.md#1Móz 8:21 | ts=%s' % DATUM)
        self.assertEqual(s['dontes_ref'], 'gerinc: H0127; negativ_proba: nem')
        self.assertTrue(s['indoklas'].startswith('Az özönvíz utáni ígéret'))
        self.assertTrue(s['indoklas'].endswith('A versben a föld szava áll, és az átok kérdéséről szól.'))

    def test_uj_fajtak_varakoznak_a_sema_elott(self):
        """A `targy` oszlop és az új jelolt_tipus az M5 sémájával jön; addig a sor várakozik, nem íródik."""
        e = futtat(tanulmany(blokk()))
        self.assertEqual({s['jelolt_tipus'] for s in e['varakozo']}, {'jelentespont', 'visszhang'})
        self.assertEqual({s['jelolt_tipus'] for s in e['uj_sorok']}, {'elofordulas'})

    def test_uj_fajtak_a_semaval(self):
        regi = G.JELOLT_TIPUSOK
        G.JELOLT_TIPUSOK = regi + ('jelentespont', 'vita', 'visszhang', 'versszam')
        try:
            e = futtat(tanulmany(blokk()), fejlec=FEJLEC_M5)
        finally:
            G.JELOLT_TIPUSOK = regi
        self.assertEqual(e['varakozo'], [])
        tipusok = {s['jelolt_tipus']: s for s in e['uj_sorok']}
        self.assertEqual(set(tipusok), {'elofordulas', 'jelentespont', 'visszhang'})
        self.assertEqual(tipusok['jelentespont']['targy'], 'H7043')
        self.assertEqual(tipusok['visszhang']['targy'], 'latin:Szent Ambrus')
        self.assertIn('scope=H7043', tipusok['jelentespont']['dontes_ref'])
        for s in e['uj_sorok']:
            self.assertEqual(s['dontes'], 'nyitva')
            self.assertTrue(s['forras_kereses'].startswith('scope=manual | '))

    def test_ismetelheto_pont(self):
        jp2 = JP.replace('H7043', 'H0127')
        e = futtat(tanulmany(blokk(pontok=PONTOK[:3] + [jp2] + PONTOK[3:])))
        self.assertEqual(e['hibak'], [])
        self.assertEqual(sorted(s['targy'] for s in e['varakozo'] if s['jelolt_tipus'] == 'jelentespont'),
                         ['H0127', 'H7043'])
        e = futtat(tanulmany(blokk(pontok=PONTOK[:3] + [JP] + PONTOK[3:])))
        self.assertTrue(any('ugyanazzal a tárggyal' in h for h in e['hibak']), e['hibak'])

    def test_ures_pontbol_nincs_sor(self):
        uresek = ['- **%s:** üres — nincs anyag' % p for p in TK.PONTOK]
        e = futtat(tanulmany(blokk(gerinc='—', pontok=uresek)))
        self.assertEqual((e['hibak'], e['uj_sorok'], e['varakozo']), ([], [], []))

    def test_hianyzo_gerinc(self):
        e = futtat(tanulmany(blokk(gerinc='—')))
        self.assertTrue(any('gerinc-elem hiányzik' in h for h in e['hibak']), e['hibak'])

    def test_uj_motivum_kihagyva(self):
        e = futtat(tanulmany(blokk(motivum='új'), blokk('1Móz 8:22', motivum='—', gerinc='—')))
        self.assertEqual(e['hibak'], [])
        self.assertEqual((e['uj_sorok'], e['varakozo']), ([], []))
        self.assertEqual([k['motivum'] for k in e['kihagyott']], ['új', '—'])

    def test_ismeretlen_motivum(self):
        e = futtat(tanulmany(blokk(motivum='NINCS-999')))
        self.assertTrue(any('nincs az adat/motivumok.tsv-ben' in h for h in e['hibak']), e['hibak'])

    def test_ket_blokk_egy_versre(self):
        e = futtat(tanulmany(blokk(), blokk()))
        self.assertTrue(any('már áll blokk' in h for h in e['hibak']), e['hibak'])

    def test_utkozes_meglevo_kulccsal(self):
        meglevo = {k: '' for k in FEJLEC_MA}
        meglevo.update({'id': 'HAMART-001', 'igehely': '1Móz 8:21', 'dontes': 'beépítve',
                        'jelolt_tipus': 'elofordulas'})
        e = futtat(tanulmany(blokk()), jeloltek=[meglevo])
        self.assertEqual(e['hibak'], [])
        self.assertEqual([u['tipus'] for u in e['utkozesek']], ['elofordulas'])
        self.assertEqual(e['uj_sorok'], [])

    def test_szovegkapu_bukas(self):
        rossz = '- **funkció:** A vers a gerinc egyik eleme, a adamá szóval.'
        e = futtat(tanulmany(blokk(pontok=[rossz] + PONTOK[1:])))
        kapu = [h for h in e['hibak'] if h.startswith('szövegkapu BUKÁS')]
        self.assertTrue(any('BELSO' in h for h in kapu), kapu)
        self.assertTrue(any('NEVELO' in h for h in kapu), kapu)
        rossz = '- **negatív próba:** nem — ezt a jelölt-táblában a DT803 szerint érdemes lehet külön vizsgálni.'
        e = futtat(tanulmany(blokk(pontok=[FUNK, rossz] + PONTOK[2:])))
        self.assertTrue(any('szövegkapu BUKÁS' in h for h in e['hibak']), e['hibak'])

    def test_general_kinyerese_valtozatlan(self):
        """A motivumok/ forrás kinyerése (general.kinyeres_elemez) a tanulmány-kinyerés után is a régi alakot adja."""
        futtat(tanulmany(blokk()))
        r = G.kinyeres_elemez('## Előfordulások\n<!-- JELÖLT: 1Móz 8:21 | gerinc: H0127 | Egy indoklás. -->\n',
                              'HAMART-001', [], G.konyv_sorrend_betolt(), DATUM)
        (s,) = r['uj_sorok']
        self.assertEqual(s['forras_kereses'], 'scope=manual | forras=motivumok/HAMART-001.md#Előfordulások | ts=%s'
                         % DATUM)
        self.assertEqual(s['dontes_ref'], 'gerinc: H0127')


class Versszamozas(unittest.TestCase):
    def test_osz_egyezik(self):
        e = futtat(tanulmany(blokk()))
        self.assertEqual([r['allapot'] for r in e['ellenorzo']], ['egyezik'])
        self.assertEqual(e['elteresek'], [])

    def test_osz_elter_tabla_vitatasa(self):
        """Jóel 2:28: a tábla szerint az MT-ben 3:1; az „azonos” blokk ELTÉR, és versszam jelölt lesz belőle."""
        vsz = '- **versszámozás:** azonos — Károli 2:28 = MT 2:28 [scope=Jóel 2:28 | forras=x | ts=2026-11-15]'
        e = futtat(tanulmany(blokk('Jóel 2:28', pontok=PONTOK[:5] + [vsz]), cim='# Jóel 2:28 — Próba'))
        self.assertEqual([r['allapot'] for r in e['ellenorzo']], ['ELTÉR'])
        self.assertEqual(len(e['elteresek']), 1)
        self.assertIn('versszam', [s['jelolt_tipus'] for s in e['varakozo']])

    def test_osz_proveniencia_nelkul(self):
        vsz = '- **versszámozás:** azonos — Károli 8:21 = KJV 8:21'
        e = futtat(tanulmany(blokk(pontok=PONTOK[:5] + [vsz])))
        self.assertTrue(any('proveniencia' in f for f in e['figyelmeztetesek']), e['figyelmeztetesek'])

    def test_usz_kezi_jelolt(self):
        vsz = '- **versszámozás:** a Károli 3:23 a görög kiadásokban is 3:23, a fejezethatár azonos.'
        e = futtat(tanulmany(blokk('Róm 3:23', pontok=PONTOK[:5] + [vsz]), cim='# Róma 3:23 — Próba'))
        self.assertEqual(e['ellenorzo'], [])
        (s,) = [s for s in e['varakozo'] if s['jelolt_tipus'] == 'versszam']
        self.assertEqual(s['dontes_ref'], 'versszámozás: scope=manual')


class KaroliKH(unittest.TestCase):
    def test_megerositett_jelolt_es_nem_kh(self):
        """1Móz 48:4 → 1Móz 28:13 a javított indexben `jelolt`; 1Móz 48:4 → 1Móz 28:14 `megerositett` (a tábla
        mai állapota); a Ján 3:16 nem Károli-KH-ja a szakasznak. A szakasz egyetlen vers: az 1Móz 48:3 → 28:13
        `megerositett`, és a szakasz bármely versének megerősített KH-ja elég."""
        negyedik = ('> 🔗 *1Móz 28:13* (kulcsszó: ígéret)\n\n> 🔗 *1Móz 28:14* (kulcsszó: ígéret)\n\n'
                    '**További igazolt kapcsolódások:** Ján 3:16 (szeretet)')
        szoveg = tanulmany(blokk('1Móz 48:4', pontok=['- **%s:** üres — nincs anyag' % p for p in TK.PONTOK]),
                           cim='# 1Mózes 48:4 — Próba', negyedik=negyedik)
        idx = kar()[1]
        szintek = {k: sz for _, _, _, sz, k in idx['Gen.48.4']}
        self.assertEqual(szintek.get('Gen.28.13'), 'jelolt')
        self.assertEqual(szintek.get('Gen.28.14'), 'megerositett')
        e = futtat(szoveg, kh=kar())
        self.assertEqual(e['hibak'], [], 'a KH-jelzés nem bukás')
        jelz, ossz = e['kh']
        self.assertEqual(ossz, {'idezett': 3, 'megerositett': 1, 'nem_kh': 1})
        self.assertEqual([j['idezett'] for j in jelz], ['1Móz 28:13'])
        self.assertEqual({sz for _, sz, _ in jelz[0]['talalat']}, {'jelolt'})
        e = futtat(szoveg.replace('1Mózes 48:4 —', '1Mózes 48:1–7 —'), kh=kar())
        self.assertEqual(e['kh'][0], [], 'az 1Móz 48:3 → 28:13 megerősített: a szakasz bármely verséé elég')

    def test_feloldhatatlan_sor_figyelmeztet(self):
        szoveg = tanulmany(blokk(), negyedik='> 🔗 *Ismeretlenkönyv 2:4* (kulcsszó: nyelv)')
        e = futtat(szoveg, kh=kar())
        self.assertTrue(any('nincs feloldható igehely' in f for f in e['figyelmeztetesek']), e['figyelmeztetesek'])


class Futas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='f205_kinyer_')
        self.jeloltek = os.path.join(self.tmp, 'jeloltek.tsv')
        self.motivumok = os.path.join(self.tmp, 'motivumok.tsv')
        self.forras = os.path.join(self.tmp, 'proba_bovitett.md')
        meglevo = ['HODIT-001', '5Móz 1:4', 'TSK', 'nyitva', 'Egy meglévő sor.', '', '', '', '2026.09.13',
                   'elofordulas', '', '', '', '']
        with io.open(self.jeloltek, 'w', encoding='utf-8', newline='') as f:
            f.write('# fejléc-megjegyzés\r\n' + '\t'.join(FEJLEC_MA) + '\r\n' + '\t'.join(meglevo) + '\r\n')
        with io.open(self.motivumok, 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tcim\nHAMART-001\tBűn\n')

    def cli(self, szoveg, *extra):
        with io.open(self.forras, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        return subprocess.run([sys.executable, os.path.join(GYOKER, 'eszkozok', 'tanulmany_kinyer.py'), self.forras,
                               '--jeloltek', self.jeloltek, '--motivumok', self.motivumok, '--ts', '2026-11-15']
                              + list(extra), capture_output=True, text=True, encoding='utf-8', cwd=self.tmp)

    def bajtok(self):
        with open(self.jeloltek, 'rb') as f:
            return f.read()

    def test_szaraz_futas_nem_ir(self):
        elotte = self.bajtok()
        r = self.cli(tanulmany(blokk()))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('**Állapot:** javaslat', r.stdout)
        self.assertEqual(self.bajtok(), elotte)

    def test_ir_csak_jelolt_sort(self):
        elotte = self.bajtok()
        jelentes = os.path.join(self.tmp, 'jelentes.md')
        r = self.cli(tanulmany(blokk()), '--ir', '--jelentes', jelentes)
        self.assertEqual(r.returncode, 0, r.stderr)
        utana = self.bajtok()
        self.assertTrue(utana.startswith(elotte), 'a meglévő sorok bájtra változatlanok')
        uj = utana[len(elotte):].decode('utf-8').split('\r\n')
        self.assertEqual(uj[-1], '')
        (sor,) = [dict(zip(FEJLEC_MA, s.split('\t'))) for s in uj[:-1]]
        self.assertEqual((sor['jelolt_tipus'], sor['dontes']), ('elofordulas', 'nyitva'))
        self.assertEqual(sor['forras_kereses'], 'scope=manual | forras=proba_bovitett.md#1Móz 8:21 | ts=2026.11.15')
        self.assertEqual(sorted(os.listdir(self.tmp)), ['jelentes.md', 'jeloltek.tsv', 'motivumok.tsv',
                                                         'proba_bovitett.md'])
        with io.open(jelentes, encoding='utf-8') as f:
            self.assertIn('Várakozó jelölt-sorok', f.read())
        r = self.cli(tanulmany(blokk()), '--ir')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.bajtok(), utana, 'újrafuttatás: ütközés, nincs új sor')
        self.assertIn('már a táblában', r.stdout)

    def test_hiba_eseten_nem_ir(self):
        elotte = self.bajtok()
        r = self.cli(tanulmany(blokk(pontok=PONTOK[:-1])), '--ir')
        self.assertEqual(r.returncode, 1)
        self.assertIn('NEM íródik', r.stderr)
        self.assertEqual(self.bajtok(), elotte)


class Repo(unittest.TestCase):
    def test_repo_erintetlen(self):
        """A tesztek a repó egyetlen fájlját sem írják: az adat/jeloltek.tsv bájtra a futás előtti."""
        ut = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
        with open(ut, 'rb') as f:
            elotte = hashlib.sha256(f.read()).hexdigest()
        futtat(tanulmany(blokk()))
        with open(ut, 'rb') as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), elotte)


if __name__ == '__main__':
    unittest.main()
