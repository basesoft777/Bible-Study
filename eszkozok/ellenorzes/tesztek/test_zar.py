#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_zar.py -- F188 (T4/T5/T6 kiegészítés): a közös helyi ellenőrzés-zár (`futtat.py` `HelyiZar`) és a lassú
tesztek érintettsége (`eszkozok/teszt_futtat.py` `LASSU_LEFEDETT`, `erintett_lassu`). A zár ideiglenes
könyvtárban (a `~/.pardes/`-hez nem nyúl).

Futtatás a repó gyökeréből:
    python eszkozok/ellenorzes/tesztek/test_zar.py
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile
import time
import unittest

_ITT = os.path.dirname(os.path.abspath(__file__))
_ELLENORZES = os.path.dirname(_ITT)
_REPO = os.path.dirname(os.path.dirname(_ELLENORZES))
sys.path.insert(0, _ELLENORZES)

import futtat as FT  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def _teszt_futtat():
    spec = importlib.util.spec_from_file_location('teszt_futtat_modul', os.path.join(_REPO, 'eszkozok', 'teszt_futtat.py'))
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


class ZarTeszt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='zar_teszt_')
        self.ut = os.path.join(self.tmp, 'al', FT.ZAR_NEV)
        self.uzenetek = []
        self._gh = os.environ.pop('GITHUB_ACTIONS', None)

    def tearDown(self):
        if self._gh is not None:
            os.environ['GITHUB_ACTIONS'] = self._gh
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _zar(self, **kw):
        kw.setdefault('kiir', self.uzenetek.append)
        kw.setdefault('alvas', lambda mp: None)
        return FT.HelyiZar('teszt', ut=self.ut, **kw)

    def _idegen_zar(self, **adat):
        os.makedirs(os.path.dirname(self.ut), exist_ok=True)
        alap = {'pid': 999999, 'gep': 'masik-gep', 'ts': time.time(), 'leiras': 'más futás', 'kezdet': 'most'}
        alap.update(adat)
        with open(self.ut, 'w', encoding='utf-8') as f:
            json.dump(alap, f)

    def test_megszerez_es_elenged(self):
        with self._zar():
            self.assertTrue(os.path.exists(self.ut))
            with open(self.ut, encoding='utf-8') as f:
                self.assertEqual(json.load(f)['pid'], os.getpid())
        self.assertFalse(os.path.exists(self.ut))

    def test_var_amig_foglalt(self):
        self._idegen_zar()
        hivas = []

        def alvas(mp):
            hivas.append(mp)
            if len(hivas) == 3:
                os.remove(self.ut)  # a másik futás közben végez
        with self._zar(alvas=alvas):
            pass
        self.assertEqual(len(hivas), 3)
        self.assertEqual(sum(1 for u in self.uzenetek if u.startswith('[zár] vár:')), 1, self.uzenetek)
        self.assertTrue(any('más futás' in u for u in self.uzenetek))
        self.assertTrue(any(u.startswith('[zár] megszerezve') for u in self.uzenetek))

    def test_holt_pid_feloldja(self):
        import socket
        self._idegen_zar(gep=socket.gethostname(), pid=4242)
        with self._zar(el_e=lambda pid: False):
            pass
        self.assertTrue(any('elavult zár átvéve' in u and 'nem él' in u for u in self.uzenetek), self.uzenetek)
        self.assertEqual([n for n in os.listdir(os.path.dirname(self.ut)) if 'elavult' in n], [])

    def test_atvetel_nem_lopja_el_a_friss_zarat(self):
        # ELLENOR_F188 4.: B elavultnak látta a zárat, közben A átvette és frisset írt; B átvétele nem veheti el A-ét
        import socket
        self._idegen_zar(gep=socket.gethostname(), pid=4242, azon='regi')
        b = self._zar(el_e=lambda pid: False)
        elavult = b._olvas()
        a = self._zar(el_e=lambda pid: False)
        a.__enter__()  # A átveszi és saját zárat ír
        self.assertEqual(a._olvas()['azon'], a.azon)
        self.assertFalse(b.atvesz(elavult))
        self.assertEqual(b._olvas()['azon'], a.azon)  # A zára a helyén maradt
        a.__exit__(None, None, None)
        self.assertFalse(os.path.exists(self.ut))

    def test_verseny_ket_szal_egy_elavult_zarra(self):
        # ELLENOR_F188 4.: két szál egyszerre talál egy elavult zárat; egyszerre legfeljebb egy tarthatja
        import socket
        import threading
        for _ in range(20):
            self._idegen_zar(gep=socket.gethostname(), pid=4242, azon='regi')
            bent, legtobb, hibak = [0], [0], []
            zar_lock = threading.Lock()
            indul = threading.Barrier(2)

            def munka():
                try:
                    indul.wait()
                    z = FT.HelyiZar('verseny', ut=self.ut, varakozas=0.001, kiir=lambda s: None,
                                    el_e=lambda pid: pid == os.getpid())  # a 4242 halott, a saját (közös) pid él
                    with z:
                        with zar_lock:
                            bent[0] += 1
                            legtobb[0] = max(legtobb[0], bent[0])
                        time.sleep(0.01)
                        with zar_lock:
                            bent[0] -= 1
                except Exception as e:  # pragma: no cover
                    hibak.append(e)
            szalak = [threading.Thread(target=munka) for _ in range(2)]
            for t in szalak:
                t.start()
            for t in szalak:
                t.join(30)
            self.assertEqual(hibak, [])
            self.assertEqual(legtobb[0], 1)
            self.assertFalse(os.path.exists(self.ut))

    def test_idokorlat_feloldja(self):
        self._idegen_zar(ts=time.time() - (FT.ZAR_ALAP_KORLAT_PERC + 5) * 60)
        with self._zar(el_e=lambda pid: True):
            pass
        self.assertTrue(any('korlát' in u for u in self.uzenetek), self.uzenetek)

    def test_elo_masik_gep_nem_elavult(self):
        self.assertEqual(FT.zar_elavult({'pid': 1, 'gep': 'masik', 'ts': 1000.0}, most=1000.0 + 60,
                                        korlat_perc=120, gep='ez', el_e=lambda p: False), (False, ''))

    def test_github_alatt_nincs_zar(self):
        os.environ['GITHUB_ACTIONS'] = 'true'
        try:
            with self._zar():
                self.assertFalse(os.path.exists(self.ut))
        finally:
            os.environ.pop('GITHUB_ACTIONS', None)

    def test_mas_zarjat_nem_torli(self):
        z = self._zar()
        z.__enter__()
        self._idegen_zar()  # közben valaki felülírta (pl. elavultnak vette)
        z.__exit__(None, None, None)
        self.assertTrue(os.path.exists(self.ut))

    def test_zar_helye(self):
        regi = os.environ.get(FT.ZAR_KONYVTAR_VALTOZO)
        try:
            os.environ.pop(FT.ZAR_KONYVTAR_VALTOZO, None)
            self.assertEqual(FT.zar_ut(), os.path.join(os.path.expanduser('~'), '.pardes', 'ellenorzes.zar'))
            os.environ[FT.ZAR_KONYVTAR_VALTOZO] = self.tmp
            self.assertEqual(FT.zar_ut(), os.path.join(self.tmp, 'ellenorzes.zar'))
        finally:
            if regi is None:
                os.environ.pop(FT.ZAR_KONYVTAR_VALTOZO, None)
            else:
                os.environ[FT.ZAR_KONYVTAR_VALTOZO] = regi


class LassuTesztTeszt(unittest.TestCase):
    def test_lefedett_lista_egy_helyen(self):
        TF = _teszt_futtat()
        self.assertEqual(set(TF.LASSU_LEFEDETT), set(TF.LASSU))

    def test_erintettseg(self):
        TF = _teszt_futtat()
        self.assertEqual(TF.erintett_lassu(['eszkozok/ellenorzes/szabalyok.py', 'MUNKAMENET.md']),
                         {f: False for f in TF.LASSU_LEFEDETT})
        self.assertEqual(TF.erintett_lassu(['eszkozok/olvaso_szerver/arculat.py']),
                         {f: True for f in TF.LASSU_LEFEDETT})
        self.assertEqual(TF.erintett_lassu(['eszkozok/olvaso_szerver_regi.py']),
                         {f: False for f in TF.LASSU_LEFEDETT})

    def test_olvaso_pilot_es_fuggesek(self):
        # ELLENOR_F188 2.: a blokkok.py az olvaso_pilot/bdb_szelet.py-t tölti be, a teszt_szintek az olvaso_pilot/adat.py-t
        TF = _teszt_futtat()
        for ut in ('eszkozok/olvaso_pilot/bdb_szelet.py', 'eszkozok/olvaso_pilot/adat.py', 'eszkozok/bdb_rovidites.py',
                   'eszkozok/bdb_konyv_javit.py', 'eszkozok/bdb_jelolt/szakasz_bemenet.py'):
            self.assertEqual(TF.erintett_lassu([ut]), {f: True for f in TF.LASSU_LEFEDETT}, ut)
        # a teszt_szintek a TSV-kből épít (pilot JSON), a teszt_arculat nem
        self.assertEqual(TF.erintett_lassu(['adat/elofordulasok.tsv']),
                         {'teszt_szintek.py': True, 'teszt_arculat.py': False})

    def test_olvaso_szerver_fajlutas_betoltesei_a_listan(self):
        # statikus őr: az olvasó-szerver nem-teszt moduljainak fájlútról / import_module-lal betöltött modulja a listán áll
        import re
        TF = _teszt_futtat()
        szerver = os.path.join(_REPO, 'eszkozok', 'olvaso_szerver')
        kell = set()
        for nev in os.listdir(szerver):
            if not nev.endswith('.py') or nev.startswith('teszt_'):
                continue
            with open(os.path.join(szerver, nev), encoding='utf-8') as f:
                szoveg = f.read()
            if "'olvaso_pilot'" in szoveg:
                kell.add('eszkozok/olvaso_pilot/x.py')
            if "'bdb_jelolt'" in szoveg:
                kell.add('eszkozok/bdb_jelolt/x.py')
            for m in re.findall(r"_eszkoz_modul\('(\w+)'\)|import_module\('(\w+)'\)", szoveg):
                kell.add('eszkozok/%s.py' % (m[0] or m[1]))
        self.assertTrue(kell)
        for ut in sorted(kell):
            self.assertTrue(all(TF.erintett_lassu([ut]).values()), ut)


if __name__ == '__main__':
    unittest.main(verbosity=1)
