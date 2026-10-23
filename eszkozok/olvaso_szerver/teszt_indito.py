"""Az indító (#100) tesztjei: az adatbázis-szinkron döntése, a git-állapot olvasása, a lábléc-figyelmeztetések és az `indit.sh`.

Futtatás (bárhol; a Flask nem kell, a lábléc-sablon tesztjéhez a Jinja2 kell, enélkül az a teszt kimarad, kifejezetten jelölve):
    python eszkozok/olvaso_szerver/teszt_indito.py
Az `indit.sh` tesztjei csak POSIX-on (WSL) futnak, és csak az "előkészítés" módot használják (`PARDES_INDIT_CSAK_ELOKESZIT=1`: leállítás +
szinkron, szerver nélkül). Minden adatbázis ideiglenes és kicsi (néhány KB); a valódi `pardes.db`-hez nem nyúl.
"""
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import allapot

POSIX = os.name == 'posix' and shutil.which('bash') is not None and shutil.which('fuser') is not None and shutil.which('flock') is not None


def kis_db(ut, ts, extra=None):
    """Kis SQLite-adatbázis `meta(kulcs, ertek)` táblával; ts=None: nincs epites_ts sor; extra: a tartalom megkülönböztetésére."""
    if os.path.exists(ut):
        os.remove(ut)
    con = sqlite3.connect(ut)
    con.execute('CREATE TABLE meta (kulcs TEXT PRIMARY KEY, ertek TEXT)')
    if ts is not None:
        con.execute('INSERT INTO meta VALUES (?, ?)', ('epites_ts', ts))
    if extra:
        con.execute('INSERT INTO meta VALUES (?, ?)', ('megjegyzes', extra))
    con.commit()
    con.close()


class TesztSzinkronDontes(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='indito_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.f = os.path.join(self.t, 'forras.db')
        self.c = os.path.join(self.t, 'cel.db')

    def test_azonos_ts_nincs_masolas(self):
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        self.assertEqual(allapot.szinkron_dontes(self.f, self.c)[0], 'azonos')

    def test_azonos_ts_eltero_mtime_is_azonos(self):
        # a szinkron-kulcs az epites_ts, NEM az mtime: a másolás átírja az mtime-ot (M0 felmérés 3.)
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        os.utime(self.c, (time.time() - 86400, time.time() - 86400))
        self.assertNotEqual(os.path.getmtime(self.f), os.path.getmtime(self.c))
        self.assertEqual(allapot.szinkron_dontes(self.f, self.c)[0], 'azonos')

    def test_eltero_ts_masol(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        d, f, c = allapot.szinkron_dontes(self.f, self.c)
        self.assertEqual((d, f, c), ('masol', '2026-10-15T08:00:00Z', '2026-10-14T09:35:00Z'))

    def test_hianyzo_cel_masol(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        self.assertEqual(allapot.szinkron_dontes(self.f, os.path.join(self.t, 'nincs.db'))[0], 'masol')

    def test_hianyzo_forras_nem_masol(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        self.assertEqual(allapot.szinkron_dontes(os.path.join(self.t, 'nincs.db'), self.c)[0], 'nincs_forras')

    def test_forras_epites_ts_nelkul_nem_masol(self):
        kis_db(self.f, None)
        kis_db(self.c, '2026-10-14T09:35:00Z')
        self.assertEqual(allapot.szinkron_dontes(self.f, self.c)[0], 'nincs_forras')

    def test_nem_sqlite_cel_olvashatatlan_masol(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        with open(self.c, 'wb') as fh:
            fh.write(b'ez nem adatbazis' * 100)
        self.assertEqual(allapot.szinkron_dontes(self.f, self.c)[0], 'masol')

    def test_az_epites_ts_olvasasa_nem_modositja_a_fajlt(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        elotte = (os.path.getmtime(self.f), os.path.getsize(self.f))
        allapot.db_epites_ts(self.f)
        self.assertEqual(elotte, (os.path.getmtime(self.f), os.path.getsize(self.f)))


class TesztGit(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='indito_git_')
        self.addCleanup(shutil.rmtree, self.t, True)

    def _ir(self, *reszek, tartalom=''):
        ut = os.path.join(self.t, *reszek)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(tartalom)
        return ut

    def test_ag_es_commit_a_ref_fajlbol(self):
        self._ir('r', '.git', 'HEAD', tartalom='ref: refs/heads/claude/valami\n')
        self._ir('r', '.git', 'refs', 'heads', 'claude', 'valami', tartalom='0123456789abcdef0123456789abcdef01234567\n')
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'r')), ('claude/valami', '01234567'))

    def test_packed_refs(self):
        self._ir('r', '.git', 'HEAD', tartalom='ref: refs/heads/main\n')
        self._ir('r', '.git', 'packed-refs', tartalom='# pack-refs with: peeled\nabcdef0123456789abcdef0123456789abcdef01 refs/heads/main\n^1111111111111111111111111111111111111111\n')
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'r')), ('main', 'abcdef01'))

    def test_detached_head(self):
        self._ir('r', '.git', 'HEAD', tartalom='fedcba9876543210fedcba9876543210fedcba98\n')
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'r')), ('(detached)', 'fedcba98'))

    def test_worktree_gitdir_fajl_es_commondir(self):
        # a worktree `.git` FÁJLja a gitdir-re mutat; a ref a közös könyvtárban van (commondir): a WSL-beli `git` ezt nem tudja olvasni
        kozos = os.path.join(self.t, 'fo', '.git')
        self._ir('fo', '.git', 'refs', 'heads', 'claude', 'ag', tartalom='1122334455667788990011223344556677889900\n')
        gd = self._ir('fo', '.git', 'worktrees', 'wt', 'HEAD', tartalom='ref: refs/heads/claude/ag\n')
        self._ir('fo', '.git', 'worktrees', 'wt', 'commondir', tartalom='../..\n')
        self._ir('wt', '.git', tartalom='gitdir: %s\n' % os.path.dirname(gd).replace('\\', '/'))
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'wt')), ('claude/ag', '11223344'))
        self.assertTrue(os.path.isdir(kozos))

    def test_almappabol_is_megtalalja(self):
        self._ir('r', '.git', 'HEAD', tartalom='ref: refs/heads/main\n')
        self._ir('r', '.git', 'refs', 'heads', 'main', tartalom='aaaaaaaa00000000000000000000000000000000\n')
        os.makedirs(os.path.join(self.t, 'r', 'a', 'b'))
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'r', 'a', 'b')), ('main', 'aaaaaaaa'))

    def test_nincs_git_ismeretlen(self):
        os.makedirs(os.path.join(self.t, 'ures'))
        # a temp könyvtár fölött lehet git-repó (pl. a felhasználói könyvtár); a .git-et kizáró gyökérrel a függvény nem talál semmit
        if allapot._git_konyvtar(os.path.join(self.t, 'ures')) is not None:
            self.skipTest('az ideiglenes könyvtár fölött git-repó van')
        self.assertEqual(allapot.git_allapot(os.path.join(self.t, 'ures')), (allapot.ISMERETLEN, allapot.ISMERETLEN))

    def test_a_valodi_repo_olvashato(self):
        ag, commit = allapot.git_allapot(D)
        self.assertNotEqual(ag, allapot.ISMERETLEN)
        self.assertRegex(commit, r'^[0-9a-f]{8}$')


class TesztLablec(unittest.TestCase):
    def test_main_azonos_adatbazis_nincs_figyelmeztetes(self):
        self.assertEqual(allapot.figyelmeztetesek('main', '2026-10-14T09:35:00Z', '2026-10-14T09:35:00Z'), [])

    def test_nem_main_ag_figyelmeztet(self):
        f = allapot.figyelmeztetesek('claude/tervezo-mod', '2026-10-14T09:35:00Z', '2026-10-14T09:35:00Z')
        self.assertEqual(len(f), 1)
        self.assertIn('claude/tervezo-mod', f[0])
        self.assertIn('main', f[0])

    def test_regebbi_masolat_figyelmeztet(self):
        f = allapot.figyelmeztetesek('main', '2026-10-14T09:35:00Z', '2026-10-15T08:00:00Z')
        self.assertEqual(len(f), 1)
        self.assertIn('régebbi', f[0])

    def test_ismeretlen_ag_figyelmeztet(self):
        self.assertTrue(allapot.figyelmeztetesek(allapot.ISMERETLEN, 'x'))

    def test_nincs_forras_ts_nincs_adatbazis_figyelmeztetes(self):
        self.assertEqual(allapot.figyelmeztetesek('main', '2026-10-14T09:35:00Z', ''), [])

    def test_keszit_a_kornyezetbol(self):
        t = tempfile.mkdtemp(prefix='indito_lab_')
        self.addCleanup(shutil.rmtree, t, True)
        f = os.path.join(t, 'forras.db')
        kis_db(f, '2026-10-15T08:00:00Z')
        L = allapot.Lablec.keszit('belso', '2026-10-14T09:35:00Z', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abcd1234', 'PARDES_FORRAS_DB': f})
        self.assertEqual((L.kiadas, L.ag, L.commit, L.epites_ts, L.forras_ts), ('belso', 'main', 'abcd1234', '2026-10-14T09:35:00Z', '2026-10-15T08:00:00Z'))
        self.assertEqual(len(L.figyelmeztetesek), 1)
        self.assertIn('régebbi', L.figyelmeztetesek[0])

    def test_keszit_forras_nelkul_nincs_adatbazis_figyelmeztetes(self):
        L = allapot.Lablec.keszit('belso', '2026-10-14T09:35:00Z', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abcd1234'})
        self.assertEqual(L.figyelmeztetesek, [])


class TesztLablecFigyelo(unittest.TestCase):
    def test_ttl_alatt_a_regi_allapot_marad_utana_az_uj(self):
        env = {'PARDES_AG': 'main', 'PARDES_COMMIT': 'aaaaaaaa'}
        f = allapot.LablecFigyelo('belso', 'ts', kornyezet=env, ttl=3600)
        self.assertEqual(f.kap().ag, 'main')
        env['PARDES_AG'] = 'claude/masik'
        self.assertEqual(f.kap().ag, 'main', 'a ttl alatt nem olvas újra')
        f.ttl = 0
        L = f.kap()
        self.assertEqual(L.ag, 'claude/masik')
        self.assertEqual(len(L.figyelmeztetesek), 1)

    def test_a_kulcs_valtozik_az_allapottal(self):
        a = allapot.Lablec('belso', 'main', 'aaaaaaaa', 'ts')
        b = allapot.Lablec('belso', 'claude/x', 'aaaaaaaa', 'ts', figyelmeztetesek=['f'])
        self.assertNotEqual(a.kulcs(), b.kulcs())
        self.assertEqual(a.kulcs(), allapot.Lablec('belso', 'main', 'aaaaaaaa', 'ts').kulcs())


class TesztLablecAlkalmazas(unittest.TestCase):
    """A lábléc a valódi alkalmazáson, mindhárom kiadásban (Flask és pardes.db kell; enélkül kimarad, kifejezetten jelölve)."""

    @classmethod
    def setUpClass(cls):
        try:
            import flask  # noqa: F401
        except ImportError:
            raise unittest.SkipTest('nincs Flask: a lábléc alkalmazás-tesztje kimarad (nem zöld)')
        cls.db = os.environ.get('PARDES_DB') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(D))), 'pardes.db')
        if not os.path.isfile(cls.db):
            raise unittest.SkipTest('nincs pardes.db (%s): a lábléc alkalmazás-tesztje kimarad (nem zöld)' % cls.db)
        import alkalmazas
        cls.alk = alkalmazas

    def _kliens(self, kiadas):
        app = self.alk.letrehoz(self.db, kiadas)
        app.extensions['pardes']['gyar'].lablec.ttl = 0                         # minden kérésnél újraolvas
        return app, app.test_client()

    def test_mindharom_kiadasban_ag_commit_epites_ts_es_az_uj_allapot_azonnal_latszik(self):
        reg = {k: os.environ.get(k) for k in ('PARDES_AG', 'PARDES_COMMIT', 'PARDES_FORRAS_DB')}
        self.addCleanup(lambda: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v) for k, v in reg.items()])
        os.environ['PARDES_AG'], os.environ['PARDES_COMMIT'] = 'main', 'abcd1234'
        os.environ.pop('PARDES_FORRAS_DB', None)
        for kiadas in ('belso', 'nyilvanos', 'kereskedelmi'):
            with self.subTest(kiadas=kiadas):
                app, c = self._kliens(kiadas)
                ts = app.extensions['pardes']['gyar'].kozos.meta.get('epites_ts', '')
                r = c.get('/1Moz/1/1')
                self.assertEqual(r.status_code, 200)
                h = r.get_data(as_text=True)
                for resz in ('ág: <b>main</b>', '<code>abcd1234</code>', 'adatbázis építve: ' + ts, 'Kiadás: <b>%s</b>' % kiadas):
                    self.assertIn(resz, h)
                self.assertNotIn('Figyelem:', h)
                etag_main = r.headers['ETag']
                os.environ['PARDES_AG'] = 'claude/valami'                       # ágváltás: újraindítás nélkül új lábléc, új ETag, nem a régi lap a gyorsítótárból
                r2 = c.get('/1Moz/1/1')
                h2 = r2.get_data(as_text=True)
                self.assertIn('ág: <b>claude/valami</b>', h2)
                self.assertIn('Figyelem:', h2)
                self.assertNotEqual(r2.headers['ETag'], etag_main)
                self.assertEqual(c.get('/1Moz/1/1', headers={'If-None-Match': etag_main}).status_code, 200, 'a régi ETag-gel nem járhat 304')
                os.environ['PARDES_AG'] = 'main'

    def test_regebbi_adatbazis_masolat_figyelmeztet(self):
        t = tempfile.mkdtemp(prefix='indito_app_')
        self.addCleanup(shutil.rmtree, t, True)
        f = os.path.join(t, 'forras.db')
        kis_db(f, '2999-01-01T00:00:00Z')
        reg = {k: os.environ.get(k) for k in ('PARDES_AG', 'PARDES_COMMIT', 'PARDES_FORRAS_DB')}
        self.addCleanup(lambda: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v) for k, v in reg.items()])
        os.environ.update(PARDES_AG='main', PARDES_COMMIT='abcd1234', PARDES_FORRAS_DB=f)
        app, c = self._kliens('belso')
        h = c.get('/').get_data(as_text=True)
        self.assertIn('Az adatbázis-másolat régebbi', h)


class TesztLablecSablon(unittest.TestCase):
    """Az `alap.html` lábléce a valódi sablonból (csak Jinja2 kell, Flask és adatbázis nem)."""

    @classmethod
    def setUpClass(cls):
        try:
            import jinja2
        except ImportError:
            raise unittest.SkipTest('nincs Jinja2: a lábléc-sablon tesztje kimarad (nem zöld)')
        cls.env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(D, 'sablonok')), autoescape=jinja2.select_autoescape(['html']),
                                     trim_blocks=True, lstrip_blocks=True)

    def _lap(self, **kw):
        ctx = dict(cim='x', arculat_hash='h', reteg='', il=False, kiadas='belso', epites_ts='2026-10-14T09:35:00Z', tervezo=False, szint_vezerlo=False)
        ctx.update(kw)
        # az alap.html blokk-sablon: a `tartalom` blokk üres marad
        return self.env.get_template('alap.html').render(**ctx)

    def _lablec(self, h):
        i = h.index('<footer')
        return h[i:h.index('</footer>', i)]

    def test_lablec_ag_commit_epites_kiadas(self):
        L = allapot.Lablec('belso', 'main', 'abcd1234', '2026-10-14T09:35:00Z')
        s = self._lablec(self._lap(lablec=L))
        for resz in ('belso', 'ág: <b>main</b>', '<code>abcd1234</code>', '2026-10-14T09:35:00Z'):
            self.assertIn(resz, s)
        self.assertNotIn('Figyelem', s)

    def test_lablec_figyelmeztetes_nem_main_agon(self):
        L = allapot.Lablec('belso', 'claude/x', 'abcd1234', 'ts', figyelmeztetesek=allapot.figyelmeztetesek('claude/x', 'ts'))
        s = self._lablec(self._lap(lablec=L))
        self.assertIn('Figyelem', s)
        self.assertIn('claude/x', s)

    def test_lablec_nelkul_valtozatlan(self):
        s = self._lablec(self._lap(lablec=None))
        self.assertIn('Kiadás: <b>belso</b> · adatbázis építve: 2026-10-14T09:35:00Z', s)
        self.assertNotIn('ág:', s)

    def test_a_lablec_nem_vezet_be_uj_osztalyt(self):
        # a regiszter-őr (#98): a lábléc csak a már regisztrált `labjegyzet` osztályt használja
        h = self._lap(lablec=allapot.Lablec('belso', 'x', 'y', 'z', figyelmeztetesek=['f']))
        s = self._lablec(h)
        import re
        self.assertEqual(set(re.findall(r'class="([^"]*)"', s)), {'labjegyzet'})


@unittest.skipUnless(POSIX, 'az indit.sh tesztjéhez POSIX, bash, fuser és flock kell (WSL)')
class TesztInditSh(unittest.TestCase):
    """Az `indit.sh` előkészítő módban: leállítás + szinkron, szerver nélkül."""

    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='indito_sh_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.f = os.path.join(self.t, 'forras', 'pardes.db')
        self.c = os.path.join(self.t, 'wsl', 'pardes.db')
        os.makedirs(os.path.dirname(self.f))
        os.makedirs(os.path.dirname(self.c))

    def _fut(self, port=0, **env):
        kornyezet = dict(os.environ, PARDES_FORRAS_DB=self.f, PARDES_DB=self.c, PARDES_PY=sys.executable, PARDES_ZAR=os.path.join(self.t, 'zar'),
                         PARDES_INDIT_CSAK_ELOKESZIT='1', PYTHONIOENCODING='utf-8')
        kornyezet.update(env)
        p = subprocess.run(['bash', os.path.join(D, 'indit.sh'), 'belso', str(port or self._szabad_port())], env=kornyezet, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, encoding='utf-8', timeout=60)
        return p.returncode, p.stdout

    @staticmethod
    def _szabad_port():
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]

    def test_eltero_ts_masol_atomi_atnevezessel(self):
        kis_db(self.f, '2026-10-15T08:00:00Z', extra='uj')
        kis_db(self.c, '2026-10-14T09:35:00Z', extra='regi')
        regi_fajl = open(self.c, 'rb')                                          # egy másik példány nyitva tartja a régi állományt
        self.addCleanup(regi_fajl.close)
        regi_tartalom = regi_fajl.read()
        kod, ki = self._fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('MÁSOLÁS', ki)
        self.assertEqual(allapot.db_epites_ts(self.c), '2026-10-15T08:00:00Z')
        regi_fajl.seek(0)
        self.assertEqual(regi_fajl.read(), regi_tartalom, 'az átnevezés a nyitott régi állományt nem csonkolhatja')
        self.assertEqual(os.listdir(os.path.dirname(self.c)), ['pardes.db'], 'nem maradhat ideiglenes fájl')

    def test_azonos_ts_nincs_masolas(self):
        kis_db(self.f, '2026-10-14T09:35:00Z', extra='forras')
        kis_db(self.c, '2026-10-14T09:35:00Z', extra='masolat')
        elotte = os.stat(self.c)
        kod, ki = self._fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('NINCS másolás', ki)
        self.assertNotIn('MÁSOLÁS', ki)
        utana = os.stat(self.c)
        self.assertEqual((elotte.st_ino, elotte.st_mtime_ns, elotte.st_size), (utana.st_ino, utana.st_mtime_ns, utana.st_size))

    def test_hianyzo_masolat_masol(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        kod, ki = self._fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('MÁSOLÁS', ki)
        self.assertEqual(allapot.db_epites_ts(self.c), '2026-10-15T08:00:00Z')

    def test_hianyzo_forras_marad_a_masolat(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        kod, ki = self._fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('NINCS másolás', ki)
        self.assertEqual(allapot.db_epites_ts(self.c), '2026-10-14T09:35:00Z')

    def test_semmilyen_adatbazis_hiba(self):
        kod, ki = self._fut()
        self.assertNotEqual(kod, 0)
        self.assertIn('HIBA', ki)

    def test_a_porton_futo_regi_peldany_leall(self):
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        port = self._szabad_port()
        regi = subprocess.Popen([sys.executable, '-c', 'import socket,time\ns=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);'
                                 's.bind(("127.0.0.1",%d));s.listen();time.sleep(60)' % port])
        self.addCleanup(lambda: (regi.poll() is None) and regi.kill())
        for _ in range(50):                                                     # megvárjuk, hogy hallgasson
            with socket.socket() as s:
                if s.connect_ex(('127.0.0.1', port)) == 0:
                    break
            time.sleep(0.1)
        kod, ki = self._fut(port=port)
        self.assertEqual(kod, 0, ki)
        self.assertIn('régi példány', ki)
        self.assertIn('leállt', ki)
        self.assertIsNotNone(regi.wait(timeout=10), 'a régi példánynak meg kellett halnia')

    def test_nincs_regi_peldany_kiirva(self):
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        kod, ki = self._fut()
        self.assertIn('nem futott régi példány', ki)

    def test_ervenytelen_hivas(self):
        p = subprocess.run(['bash', os.path.join(D, 'indit.sh'), 'ismeretlen', '8765'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        self.assertEqual(p.returncode, 2)
        p = subprocess.run(['bash', os.path.join(D, 'indit.sh'), 'belso', 'abc'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        self.assertEqual(p.returncode, 2)

    def test_az_indit_sh_lf_sorvegu(self):
        with open(os.path.join(D, 'indit.sh'), 'rb') as f:
            self.assertNotIn(b'\r', f.read(), 'a CRLF-es shell-szkript WSL-ben nem fut (a .gitattributes *.sh eol=lf gondoskodik róla)')


if __name__ == '__main__':
    unittest.main(verbosity=2)
