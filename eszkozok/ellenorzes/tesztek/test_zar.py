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
        self.assertEqual(self._maradt(), [])  # fő zár nem maradt (az állandó átvételi fájl nem zár)

    def test_atvetel_ujraolvas_es_friss_zarat_nem_torli(self):
        # ELLENOR_F188_2 1.: B elavultnak látta a zárat, közben A átvette és frisset írt; B átvétele az átvételi zár
        # alatt újraolvas, és A friss zárát nem törli
        import socket
        self._idegen_zar(gep=socket.gethostname(), pid=4242, azon='regi')
        a = self._zar(el_e=lambda pid: pid == os.getpid())
        b = self._zar(el_e=lambda pid: pid == os.getpid())
        self.assertTrue(b._elavult()[0])
        a.__enter__()
        self.assertFalse(b.atvesz())
        self.assertEqual(b._olvas()['azon'], a.azon)
        a.__exit__(None, None, None)
        self.assertEqual(self._maradt(), [])

    def test_iro_zar_nem_elavult(self):
        # az O_EXCL-lel létrehozott, még üres (íródó) fő zár a türelmi időn belül nem elavult; utána igen
        os.makedirs(os.path.dirname(self.ut), exist_ok=True)
        open(self.ut, 'w').close()
        z = self._zar()
        self.assertEqual(z._elavult()[0], False)
        regi = time.time() - FT.ZAR_TURELEM_MP - 5
        os.utime(self.ut, (regi, regi))
        self.assertEqual(z._elavult()[0], True)

    def _maradt(self):
        # a fő zár és bármely nem az állandó átvételi fájl
        return [n for n in os.listdir(os.path.dirname(self.ut)) if n != FT.ZAR_NEV + FT.ZAR_ATVETEL_UTOTAG]

    def test_os_zar_kizarja_a_masodik_atvevot(self):
        # DT-F188d (b), ELLENOR_F188_3 1.: az átvételi OS-zárat egyszerre egy példány tartja
        os.makedirs(os.path.dirname(self.ut), exist_ok=True)
        a, b = self._zar(), self._zar()
        self.assertTrue(a._atveteli_zar())
        self.assertFalse(b._atveteli_zar())
        a._atveteli_zar_el()
        self.assertTrue(b._atveteli_zar())
        b._atveteli_zar_el()
        self.assertTrue(os.path.exists(self.ut + FT.ZAR_ATVETEL_UTOTAG))  # az állandó fájl nem törlődik

    def test_osszeomlott_tarto_utan_felszabadul(self):
        # DT-F188d (b): az átvételi OS-zár birtokában os._exit-tel kilépő alfolyamat után a zár felszabadul
        import subprocess
        os.makedirs(os.path.dirname(self.ut), exist_ok=True)
        kod = ('import os, sys\n'
               'sys.path.insert(0, sys.argv[1])\n'
               'import futtat as FT\n'
               'z = FT.HelyiZar("osszeomlo", ut=sys.argv[2])\n'
               'assert z._atveteli_zar()\n'
               'print("tartom", flush=True)\n'
               'sys.stdin.readline()\n'
               'os._exit(0)\n')
        p = subprocess.Popen([sys.executable, '-c', kod, _ELLENORZES, self.ut], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, text=True, encoding='utf-8')
        try:
            self.assertEqual(p.stdout.readline().strip(), 'tartom')
            masik = self._zar()
            self.assertFalse(masik._atveteli_zar())  # a gyerek tartja
            p.stdin.write('\n')
            p.stdin.flush()
            p.wait(30)
        finally:
            if p.poll() is None:
                p.kill()
        masik = self._zar()
        self.assertTrue(masik._atveteli_zar())  # a rendszer feloldotta (nem engedte el, os._exit)
        masik._atveteli_zar_el()

    def test_varakozas_alszik_nem_porog(self):
        # DT-F188d (c): elavult fő zár, de az átvételi OS-zárat más tartja -> a váró nem hív atvesz-t pörögve
        import socket
        import threading
        self._idegen_zar(gep=socket.gethostname(), pid=4242, azon='regi')
        tarto = self._zar()
        self.assertTrue(tarto._atveteli_zar())
        hivas = [0]

        class Szamlalo(FT.HelyiZar):
            def atvesz(self):
                hivas[0] += 1
                return FT.HelyiZar.atvesz(self)
        z = Szamlalo('varo', ut=self.ut, varakozas=0.001, kiir=lambda s: None, el_e=lambda pid: pid == os.getpid())
        t = threading.Thread(target=lambda: (z.__enter__(), z.__exit__(None, None, None)))
        t.start()
        time.sleep(0.3)
        n = hivas[0]
        tarto._atveteli_zar_el()
        t.join(30)
        self.assertFalse(t.is_alive())
        self.assertLess(n, 0.3 / FT.ZAR_ROVID_ALVAS_MP + 5, 'pörög: %d atvesz-hívás 0,3 s alatt' % n)
        self.assertGreater(n, 0)
        self.assertEqual(self._maradt(), [])

    def _verseny(self, szalak_szama, korok, uj_erkezo_kesleltetes=None):
        import socket
        import threading
        for kor in range(korok):
            self._idegen_zar(gep=socket.gethostname(), pid=4242, azon='regi')
            bent, legtobb, hibak, kesz = [0], [0], [], [0]
            zar_lock = threading.Lock()
            n = szalak_szama + (1 if uj_erkezo_kesleltetes is not None else 0)
            indul = threading.Barrier(szalak_szama)

            def munka(kesleltetes=None):
                try:
                    if kesleltetes is None:
                        indul.wait()
                    else:
                        time.sleep(kesleltetes)  # újonnan érkező: az átvétel közben ér oda
                    z = FT.HelyiZar('verseny', ut=self.ut, varakozas=0.0005, kiir=lambda s: None,
                                    el_e=lambda pid: pid == os.getpid())  # a 4242 halott, a saját (közös) pid él
                    with z:
                        with zar_lock:
                            bent[0] += 1
                            legtobb[0] = max(legtobb[0], bent[0])
                        time.sleep(0.002)
                        with zar_lock:
                            bent[0] -= 1
                            kesz[0] += 1
                except Exception as e:  # pragma: no cover
                    hibak.append(e)
            szalak = [threading.Thread(target=munka) for _ in range(szalak_szama)]
            if uj_erkezo_kesleltetes is not None:
                szalak.append(threading.Thread(target=munka, args=((kor % 5) * uj_erkezo_kesleltetes,)))
            for t in szalak:
                t.start()
            for t in szalak:
                t.join(60)
            self.assertEqual(hibak, [], 'kör %d' % kor)
            self.assertEqual(kesz[0], n, 'kör %d: nem futott le mindenki' % kor)
            self.assertEqual(legtobb[0], 1, 'kör %d: egyszerre több tartó' % kor)
            self.assertEqual(self._maradt(), [], 'kör %d: maradt zárfájl' % kor)

    def test_verseny_ket_szal_egy_elavult_zarra(self):
        self._verseny(2, 20)

    def test_verseny_harom_szal_es_uj_erkezo(self):
        # ELLENOR_F188_2 1.: 3 szál egy elavult zárra, és egy negyedik, amely az átvétel közben érkezik; sok kör
        self._verseny(3, 40, uj_erkezo_kesleltetes=0.0005)

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
