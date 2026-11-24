#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gepsor.py -- a gép közös FIFO-sorának (`eszkozok/gepsor.py`) tesztjei. A sor ideiglenes könyvtárban fut (a `~/.pardes/`-hez
nem nyúl).

Futtatás a repó gyökeréből:
    python eszkozok/teszt_gepsor.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)

import gepsor  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GEP = gepsor.socket.gethostname()
PLAT = gepsor.platform_jel()


class GepsorTeszt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='gepsor_teszt_')
        self.kv = os.path.join(self.tmp, 'gepsor')
        self.uzenetek = []
        self._env = {k: os.environ.pop(k, None) for k in ('GITHUB_ACTIONS', gepsor.TARTVA_VALTOZO, gepsor.ZAR_TARTVA_VALTOZO)}

    def tearDown(self):
        for k, v in self._env.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _jegy(self, nev, **adat):
        os.makedirs(self.kv, exist_ok=True)
        alap = {'pid': 4242, 'indulas': 1, 'gep': GEP, 'platform': PLAT, 'leiras': 'más futás', 'ts': time.time(),
                'kezdet': 'most', 'munkakonyvtar': 'x'}
        alap.update(adat)
        with open(os.path.join(self.kv, nev), 'w', encoding='utf-8') as f:
            json.dump(alap, f)
        return nev

    def _sor(self, **kw):
        kw.setdefault('kiir', self.uzenetek.append)
        kw.setdefault('alvas', lambda mp: None)
        return gepsor.Sor('teszt', konyvtar=self.kv, **kw)

    # --- alapeset -------------------------------------------------------------------------------------------------------
    def test_ures_sor_azonnal_fut_es_kilepeskor_torli_a_jegyet(self):
        with self._sor() as s:
            self.assertEqual(gepsor.jegyek(self.kv), [s.jegy])
            self.assertEqual(os.environ.get(gepsor.TARTVA_VALTOZO), s.jegy)
        self.assertEqual(gepsor.jegyek(self.kv), [])
        self.assertIsNone(os.environ.get(gepsor.TARTVA_VALTOZO))

    def test_a_jegy_atomi_es_teljes(self):
        s = self._sor()
        nev = s.beall()
        adat = gepsor.jegy_olvas(self.kv, nev)
        self.assertEqual(adat['pid'], os.getpid())
        self.assertEqual(adat['gep'], GEP)
        self.assertEqual(adat['platform'], PLAT)
        self.assertEqual([n for n in os.listdir(self.kv) if n.endswith('.tmp')], [])

    def test_github_es_ujrabelepes_nem_all_sorba(self):
        os.environ['GITHUB_ACTIONS'] = 'true'
        with self._sor() as s:
            self.assertIsNone(s.jegy)
        os.environ.pop('GITHUB_ACTIONS')
        os.environ[gepsor.TARTVA_VALTOZO] = 'kulso'
        with self._sor() as s:
            self.assertIsNone(s.jegy)
        self.assertEqual(gepsor.jegyek(self.kv), [])

    def test_zar_alatt_nem_all_sorba(self):
        """Holtpont-védelem: a helyi ellenőrzés-zár alatt futó folyamat nem áll sorba (különben az E28 a sorra, a sor eleje a zárra várna)."""
        os.environ[gepsor.ZAR_TARTVA_VALTOZO] = 'zar-azon'
        with self._sor() as s:
            self.assertIsNone(s.jegy)
        self.assertEqual(gepsor.jegyek(self.kv), [])
        self.assertTrue(any('holtpont-védelem' in u for u in self.uzenetek), self.uzenetek)

    def test_a_helyi_zar_jelzi_a_tartast(self):
        """A `HelyiZar` a tartás alatt beállítja a `PARDES_ZAR_TARTVA`-t (a gyerekfolyamatok öröklik), kilépéskor törli."""
        import importlib.util
        spec = importlib.util.spec_from_file_location('futtat_zar', os.path.join(ITT, 'ellenorzes', 'futtat.py'))
        sys.path.insert(0, os.path.join(ITT, 'ellenorzes'))
        FT = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(FT)
        self.assertEqual(FT.ZAR_TARTVA_VALTOZO, gepsor.ZAR_TARTVA_VALTOZO)
        with FT.HelyiZar('teszt', ut=os.path.join(self.tmp, 'zar', 'ellenorzes.zar'), kiir=lambda s: None):
            self.assertTrue(os.environ.get(gepsor.ZAR_TARTVA_VALTOZO))
            with self._sor() as s:
                self.assertIsNone(s.jegy)
        self.assertIsNone(os.environ.get(gepsor.ZAR_TARTVA_VALTOZO))

    # --- várakozás, sorrend ---------------------------------------------------------------------------------------------
    def test_elo_elozo_utan_var_es_sorra_kerul(self):
        elo = self._jegy('00000000000000000001_4242_aa.jegy')
        korok = []

        def alvas(_mp):
            korok.append(1)
            if len(korok) == 3:
                os.remove(os.path.join(self.kv, elo))   # az előző végzett

        with self._sor(alvas=alvas, folyamat_fn=lambda pid: (True, 1)) as s:
            self.assertEqual(gepsor.jegyek(self.kv), [s.jegy])
        self.assertEqual(len(korok), 3)
        self.assertTrue(any('2. a gép sorában' in u for u in self.uzenetek), self.uzenetek)
        self.assertTrue(any('sorra került' in u for u in self.uzenetek))

    def test_fifo_a_kesobb_erkezo_nem_elozi_meg(self):
        s1 = self._sor(folyamat_fn=lambda pid: (True, None))
        s1.beall()
        time.sleep(0.01)
        s2 = self._sor(folyamat_fn=lambda pid: (True, None))
        s2.beall()
        self.assertEqual(s1.elottem(), [])
        self.assertEqual([n for n, _ in s2.elottem()], [s1.jegy])

    # --- halott jegy ----------------------------------------------------------------------------------------------------
    def test_halott_pid_jegyet_torli(self):
        self._jegy('00000000000000000001_4242_aa.jegy')
        with self._sor(folyamat_fn=lambda pid: (pid == os.getpid(), None)) as s:
            self.assertEqual(gepsor.jegyek(self.kv), [s.jegy])
        self.assertTrue(any('halott jegy törölve' in u for u in self.uzenetek), self.uzenetek)

    def test_ujrahasznosult_pid_halottnak_szamit(self):
        self._jegy('00000000000000000001_4242_aa.jegy', indulas=111)
        el, ok = gepsor.jegy_el(gepsor.jegy_olvas(self.kv, '00000000000000000001_4242_aa.jegy'),
                                folyamat_fn=lambda pid: (True, 222))
        self.assertFalse(el)
        self.assertIn('újrahasznosult', ok)

    def test_elo_pid_jegyet_soha_nem_torli(self):
        nev = self._jegy('00000000000000000001_4242_aa.jegy', ts=time.time() - 10 * 3600)   # tíz órás, de él
        self.assertFalse(gepsor.halott_torol(self.kv, nev, folyamat_fn=lambda pid: (True, 1)))
        self.assertIn(nev, gepsor.jegyek(self.kv))
        # a váró is csak jelez (FIGYELEM), nem töröl
        korok = []

        def alvas(_mp):
            korok.append(1)
            if len(korok) == 2:
                raise KeyboardInterrupt

        s = self._sor(alvas=alvas, folyamat_fn=lambda pid: (True, 1))
        with self.assertRaises(KeyboardInterrupt):
            s.__enter__()
        self.assertIn(nev, gepsor.jegyek(self.kv))
        self.assertTrue(any('FIGYELEM' in u and 'nem törli' in u for u in self.uzenetek), self.uzenetek)

    def test_torles_elott_ujraolvas(self):
        """A pid ellenőrzése a törlés pillanatában történik: ha az első nézéskor halott, de a törlés előtti újraolvasáskor él
        (pl. a vizsgálat közben más tartalom), nem töröl."""
        nev = self._jegy('00000000000000000001_4242_aa.jegy')
        hivasok = []

        def folyamat_fn(pid):
            hivasok.append(pid)
            return (True, 1)

        self.assertFalse(gepsor.halott_torol(self.kv, nev, folyamat_fn=folyamat_fn))
        self.assertEqual(hivasok, [4242])
        self.assertIn(nev, gepsor.jegyek(self.kv))

    def test_mas_gep_vagy_platform_jegyet_nem_torli(self):
        n1 = self._jegy('00000000000000000001_4242_aa.jegy', gep='masik-gep')
        n2 = self._jegy('00000000000000000002_4242_bb.jegy', platform='nt' if PLAT == 'posix' else 'posix')
        halott = lambda pid: (False, None)  # noqa: E731
        self.assertFalse(gepsor.halott_torol(self.kv, n1, folyamat_fn=halott))
        self.assertFalse(gepsor.halott_torol(self.kv, n2, folyamat_fn=halott))
        self.assertEqual(gepsor.jegyek(self.kv), [n1, n2])

    def test_olvashatatlan_jegyet_nem_torli(self):
        os.makedirs(self.kv, exist_ok=True)
        with open(os.path.join(self.kv, '00000000000000000001_1_aa.jegy'), 'w') as f:
            f.write('{nem json')
        self.assertFalse(gepsor.halott_torol(self.kv, '00000000000000000001_1_aa.jegy', folyamat_fn=lambda pid: (False, None)))

    # --- valódi folyamatok ----------------------------------------------------------------------------------------------
    def test_valodi_folyamat_azonossag(self):
        el, indulas = gepsor.folyamat(os.getpid())
        self.assertTrue(el)
        p = subprocess.Popen([sys.executable, '-c', 'pass'])
        p.wait()
        el2, _ = gepsor.folyamat(p.pid)
        # a halott pid-et a rendszer újra kioszthatja; ha mégis él, más az indulási ideje
        if el2:
            self.assertNotEqual(gepsor.folyamat(p.pid)[1], indulas)
        self.assertFalse(gepsor.folyamat(0)[0])
        self.assertFalse(gepsor.folyamat('x')[0])

    def test_valodi_halott_folyamat_jegye_felszabadul(self):
        kod = ('import sys; sys.path.insert(0, %r); import gepsor; s = gepsor.Sor("halott", konyvtar=%r); s.beall(); '
               'print(s.jegy)') % (ITT, self.kv)
        r = subprocess.run([sys.executable, '-c', kod], capture_output=True, encoding='utf-8')
        halott_jegy = r.stdout.strip()
        self.assertIn(halott_jegy, gepsor.jegyek(self.kv))
        with self._sor(folyamat_fn=gepsor.folyamat) as s:
            self.assertEqual(gepsor.jegyek(self.kv), [s.jegy])

    def test_valodi_folyamatok_sorrendben_futnak(self):
        """Három folyamat egymás után áll be; a futásuk nem fedi át egymást, és az érkezés sorrendjében fut."""
        naplo = os.path.join(self.tmp, 'naplo.txt')
        kod = ('import sys, time; sys.path.insert(0, %r); import gepsor\n'
               'with gepsor.Sor(sys.argv[1], konyvtar=%r, varakozas=0.05):\n'
               '    open(%r, "a").write("be " + sys.argv[1] + "\\n"); time.sleep(0.4)\n'
               '    open(%r, "a").write("ki " + sys.argv[1] + "\\n")\n') % (ITT, self.kv, naplo, naplo)
        procok = []
        for i in range(3):
            env = dict(os.environ)
            env.pop(gepsor.TARTVA_VALTOZO, None)
            env.pop(gepsor.ZAR_TARTVA_VALTOZO, None)
            procok.append(subprocess.Popen([sys.executable, '-c', kod, str(i)], env=env))
            # a következő csak akkor indul, ha az előző jegye már a sorban van
            hatar = time.time() + 20
            while len(gepsor.jegyek(self.kv)) < i + 1 and time.time() < hatar:
                time.sleep(0.02)
        for p in procok:
            self.assertEqual(p.wait(timeout=60), 0)
        with open(naplo) as f:
            sorok = f.read().split()
        self.assertEqual(sorok, ['be', '0', 'ki', '0', 'be', '1', 'ki', '1', 'be', '2', 'ki', '2'])
        self.assertEqual(gepsor.jegyek(self.kv), [])

    def test_futtat_parancs_kilepesi_kodja(self):
        os.environ[gepsor.KONYVTAR_VALTOZO] = self.tmp
        try:
            self.assertEqual(gepsor.main(['futtat', '--leiras', 'x', '--', sys.executable, '-c', 'import sys; sys.exit(3)']), 3)
            self.assertEqual(gepsor.main(['futtat', '--', sys.executable, '-c', 'pass']), 0)
            self.assertEqual(gepsor.main(['futtat']), 2)
            self.assertEqual(gepsor.main(['allapot']), 0)
        finally:
            os.environ.pop(gepsor.KONYVTAR_VALTOZO, None)
        self.assertEqual(gepsor.jegyek(self.kv), [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
