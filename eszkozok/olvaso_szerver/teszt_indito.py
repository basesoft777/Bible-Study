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
import forras_azonosito as FA

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
        L = allapot.Lablec.keszit('belso', '2026-10-14T09:35:00Z', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abcd1234', 'PARDES_FORRAS_DB': f, 'PARDES_LEMARADAS': '0'})
        self.assertEqual((L.kiadas, L.ag, L.commit, L.epites_ts, L.forras_ts), ('belso', 'main', 'abcd1234', '2026-10-14T09:35:00Z', '2026-10-15T08:00:00Z'))
        self.assertEqual(len(L.figyelmeztetesek), 1)
        self.assertIn('régebbi', L.figyelmeztetesek[0])

    def test_keszit_forras_nelkul_nincs_adatbazis_figyelmeztetes(self):
        L = allapot.Lablec.keszit('belso', '2026-10-14T09:35:00Z', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abcd1234', 'PARDES_LEMARADAS': '0'})
        self.assertEqual(L.figyelmeztetesek, [])


class TesztLablecFigyelo(unittest.TestCase):
    def test_ttl_alatt_a_regi_allapot_marad_utana_az_uj(self):
        env = {'PARDES_AG': 'main', 'PARDES_COMMIT': 'aaaaaaaa', 'PARDES_LEMARADAS': '0'}
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
        reg = {k: os.environ.get(k) for k in ('PARDES_AG', 'PARDES_COMMIT', 'PARDES_FORRAS_DB', 'PARDES_LEMARADAS')}
        self.addCleanup(lambda: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v) for k, v in reg.items()])
        os.environ['PARDES_AG'], os.environ['PARDES_COMMIT'] = 'main', 'abcd1234'
        os.environ['PARDES_LEMARADAS'] = '0'                                     # a valódi checkout lemaradásától független (F225)
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


GIT = shutil.which('git')


def git(konyvtar, *args):
    """Egy valódi `git`-hívás ideiglenes repón; a kimenet levágva."""
    p = subprocess.run([GIT, '-C', konyvtar, '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false', '-c', 'core.autocrlf=false', *args],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    assert p.returncode == 0, (args, p.stdout)
    return p.stdout.strip()


def ideiglenes_repo(t, nev='r', commitok=4):
    """Ideiglenes repó `main` ággal és `commitok` üres committal; `origin/main` a csúcson. Visszaadja a könyvtárat és a commit-hash-eket (régi → új)."""
    r = os.path.join(t, nev)
    os.makedirs(r)
    git(r, 'init', '-q', '-b', 'main')
    hash_ek = []
    for i in range(commitok):
        git(r, 'commit', '-q', '--allow-empty', '-m', 'c%d' % i)
        hash_ek.append(git(r, 'rev-parse', 'HEAD'))
    git(r, 'update-ref', allapot.FO_REF, hash_ek[-1])
    return r, hash_ek


@unittest.skipUnless(GIT, 'a lemaradás tesztjéhez git kell')
class TesztLemaradas(unittest.TestCase):
    """F225: hány committal áll a HEAD az origin/main mögött; ideiglenes repón, valódi git-tel."""

    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='indito_lem_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.r, self.h = ideiglenes_repo(self.t)

    def test_azonos_hash_nulla_git_nelkul(self):
        self.assertEqual(allapot.lemaradas(self.r, szinkron=True), 0)

    def test_a_haromcommitos_lemaradas(self):
        git(self.r, 'reset', '-q', '--hard', self.h[0])                       # a HEAD a legrégebbi committon, az origin/main a csúcson
        self.assertEqual(allapot.lemaradas(self.r, szinkron=True), 3)

    def test_csomagolt_objektumokkal_is(self):
        git(self.r, 'reset', '-q', '--hard', self.h[1])
        git(self.r, 'gc', '-q', '--prune=now')
        git(self.r, 'pack-refs', '--all')                                      # a ref-ek is packed-refs-ben
        self.assertFalse(os.path.exists(os.path.join(self.r, '.git', 'refs', 'remotes', 'origin', 'main')))
        self.assertEqual(allapot.lemaradas(self.r, szinkron=True), 2)

    def test_worktree_a_gitdir_fajlon_at(self):
        # a linkelt worktree `.git` FÁJL: a számolás a feloldott --git-dir-rel megy; a worktree saját HEAD-je számít
        git(self.r, 'branch', 'regi', self.h[1])
        wt = os.path.join(self.t, 'wt')
        git(self.r, 'worktree', 'add', '-q', wt, 'regi')
        self.assertTrue(os.path.isfile(os.path.join(wt, '.git')))
        self.assertEqual(allapot.lemaradas(wt, szinkron=True), 2)
        self.assertEqual(allapot.lemaradas(self.r, szinkron=True), 0, 'a főcheckout HEAD-je a csúcson áll')

    def test_nincs_origin_main_ismeretlen(self):
        git(self.r, 'update-ref', '-d', allapot.FO_REF)
        self.assertIsNone(allapot.lemaradas(self.r, szinkron=True))

    def test_nincs_git_konyvtar_ismeretlen(self):
        ures = os.path.join(self.t, 'ures')
        os.makedirs(ures)
        if allapot._git_konyvtar(ures) is not None:
            self.skipTest('az ideiglenes könyvtár fölött git-repó van')
        self.assertIsNone(allapot.lemaradas(ures, szinkron=True))

    def test_hatterszal_nem_blokkol_es_a_vegen_ad_erteket(self):
        git(self.r, 'reset', '-q', '--hard', self.h[0])
        elso = allapot.lemaradas(self.r)
        self.assertIn(elso, (None, 3), 'az első hívás nem várja meg a git-et (None), legfeljebb ha már kész')
        ertek = elso
        for _ in range(100):
            if ertek == 3:
                break
            time.sleep(0.05)
            ertek = allapot.lemaradas(self.r)
        self.assertEqual(ertek, 3)

    def test_a_szam_csak_ref_valtozaskor_szamolodik_ujra(self):
        git(self.r, 'reset', '-q', '--hard', self.h[0])
        self.assertEqual(allapot.lemaradas(self.r, szinkron=True), 3)
        hivasok = []
        eredeti = allapot._commit_szam
        allapot._commit_szam = lambda *a: hivasok.append(a) or 99
        self.addCleanup(setattr, allapot, '_commit_szam', eredeti)
        self.assertEqual(allapot.lemaradas(self.r), 3, 'ugyanazokkal a ref-ekkel a tárból jön')
        self.assertEqual(hivasok, [])
        git(self.r, 'update-ref', allapot.FO_REF, self.h[2])                  # a ref változott: újra kell számolni
        allapot.lemaradas(self.r, szinkron=True)
        self.assertEqual(len(hivasok), 1)

    def test_checkout_szerep_fo_es_worktree(self):
        git(self.r, 'branch', 'ag', self.h[1])
        wt = os.path.join(self.t, 'wt')
        git(self.r, 'worktree', 'add', '-q', wt, 'ag')
        szerep, fo, mf = allapot.checkout_szerep(self.r)
        self.assertEqual((szerep, os.path.normpath(fo), os.path.normpath(mf)), ('fo', os.path.normpath(self.r), os.path.normpath(self.r)))
        szerep, fo, mf = allapot.checkout_szerep(wt)
        self.assertEqual((szerep, os.path.normpath(fo), os.path.normpath(mf)), ('elonezet', os.path.normpath(self.r), os.path.normpath(wt)))

    def test_a_figyelmeztetes_szovege_main_es_ag(self):
        f = allapot.figyelmeztetesek('main', 'ts', '', 201)
        self.assertEqual(len(f), 1)
        self.assertIn('201 committal az origin/main mögött', f[0])
        self.assertIn('fetch', f[0])
        g = allapot.figyelmeztetesek('claude/x', 'ts', '', 5)
        self.assertEqual(len(g), 2)
        self.assertIn('Az ág 5 committal az origin/main mögött', g[1])
        for lem in (0, None):
            self.assertEqual(allapot.figyelmeztetesek('main', 'ts', '', lem), [])

    def test_a_lablec_kulcsa_es_kornyezeti_felulirasa(self):
        a = allapot.Lablec('belso', 'main', 'aaaaaaaa', 'ts', lemaradas=0)
        b = allapot.Lablec('belso', 'main', 'aaaaaaaa', 'ts', lemaradas=7, figyelmeztetesek=['f'])
        self.assertNotEqual(a.kulcs(), b.kulcs())
        L = allapot.Lablec.keszit('belso', 'ts', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abcd1234', 'PARDES_LEMARADAS': '201'})
        self.assertEqual(L.lemaradas, 201)
        self.assertEqual(len(L.figyelmeztetesek), 1)
        self.assertIn('201 committal', L.figyelmeztetesek[0])
        self.assertIsNone(allapot.Lablec.keszit('belso', 'ts', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'x', 'PARDES_LEMARADAS': 'nem'}).lemaradas)


class _InditAlap(unittest.TestCase):
    """Az `indit.sh` tesztjeinek közös váza: ideiglenes adatbázisok, előkészítő mód (szerver nélkül), a valódi checkout védelme."""

    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='indito_sh_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.f = os.path.join(self.t, 'forras', 'pardes.db')
        self.c = os.path.join(self.t, 'wsl', 'pardes.db')
        os.makedirs(os.path.dirname(self.f))
        os.makedirs(os.path.dirname(self.c))

    def _fut(self, port=0, kiadas='belso', cel=D, **env):
        """Az `indit.sh` futtatása előkészítő módban. Alapból NEM előnézet és nincs főcheckout-frissítés (PARDES_ELONEZET=0, PARDES_FRISSIT=0): a
        szkript a tesztet futtató checkoutban áll, amelyet a teszt nem frissíthet és nem kezelhet előnézetként; az F225 tesztjei ezt felülírják."""
        kornyezet = dict(os.environ, PARDES_FORRAS_DB=self.f, PARDES_DB=self.c, PARDES_PY=sys.executable, PARDES_ZAR=os.path.join(self.t, 'zar'),
                         PARDES_INDIT_CSAK_ELOKESZIT='1', PYTHONIOENCODING='utf-8', PARDES_ELONEZET='0', PARDES_FRISSIT='0',
                         PARDES_EPIT='0', PARDES_EPIT_ZAR=os.path.join(self.t, 'epit.zar'),
                         PARDES_EPITES_ALLAPOT=os.path.join(self.t, 'epites_allapot.tsv'), PARDES_EPITES_NAPLO=os.path.join(self.t, 'epites.log'))
        kornyezet.pop('PARDES_FRISSITVE', None)
        kornyezet.update(env)
        for k in [k for k, v in kornyezet.items() if v is None]:
            del kornyezet[k]
        p = subprocess.run(['bash', os.path.join(cel, 'indit.sh'), kiadas, str(port or self._szabad_port())], env=kornyezet, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, encoding='utf-8', timeout=120)
        return p.returncode, p.stdout

    @staticmethod
    def _szabad_port():
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]


@unittest.skipUnless(POSIX, 'az indit.sh tesztjéhez POSIX, bash, fuser és flock kell (WSL)')
class TesztInditSh(_InditAlap):
    """Az `indit.sh` előkészítő módban: leállítás + szinkron, szerver nélkül."""

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


def szkript_repo(t):
    """Ideiglenes főcheckout (F225): `origin.git` (bare), `fo` (a main ágon, az indító három szkriptje commitolva és pusholva), `masik` (második klón,
    amellyel az origin-re új commit megy). Visszaadja (fo, masik, fo_cel) útját; `fo_cel` az `indit.sh` könyvtára a főcheckoutban."""
    origin = os.path.join(t, 'origin.git')
    os.makedirs(origin)
    git(origin, 'init', '-q', '--bare', '-b', 'main')
    git(t, 'clone', '-q', origin, 'fo')
    fo = os.path.join(t, 'fo')
    git(fo, 'checkout', '-q', '-B', 'main')
    fo_cel = os.path.join(fo, 'eszkozok', 'olvaso_szerver')
    os.makedirs(fo_cel)
    for n in ('indit.sh', 'allapot.py', 'lekerdezesek.py', 'forras_azonosito.py', 'epit_hatter.sh'):
        shutil.copy(os.path.join(D, n), os.path.join(fo_cel, n))
    git(fo, 'add', '-A')
    git(fo, 'commit', '-q', '-m', 'szkriptek')
    git(fo, 'push', '-q', '-u', 'origin', 'main')
    git(t, 'clone', '-q', origin, 'masik')
    return fo, os.path.join(t, 'masik'), fo_cel


def origin_commit(masik, fajl='uj.txt', tartalom='x\n'):
    """Új commit az origin main ágán a második klónból; visszaadja az új hash-t."""
    git(masik, 'pull', '-q', '--ff-only', 'origin', 'main')
    with open(os.path.join(masik, fajl), 'a', encoding='utf-8', newline='') as f:
        f.write(tartalom)
    git(masik, 'add', '-A')
    git(masik, 'commit', '-q', '-m', 'origin: ' + fajl)
    git(masik, 'push', '-q', 'origin', 'main')
    return git(masik, 'rev-parse', 'HEAD')


@unittest.skipUnless(POSIX and GIT, 'az indit.sh tesztjéhez POSIX, bash, fuser, flock és git kell (WSL)')
class TesztInditFrissites(_InditAlap):
    """F225: a főcheckout frissítése induláskor (`git fetch` + `merge --ff-only`), ideiglenes repón; a valódi checkoutot a teszt nem érinti."""

    def setUp(self):
        super().setUp()
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        self.fo, self.masik, self.cel = szkript_repo(self.t)

    def _fo_fut(self, **env):
        env.setdefault('PARDES_FRISSIT', '1')
        return self._fut(cel=self.cel, **env)

    def _hash(self, ref='HEAD'):
        return git(self.fo, 'rev-parse', ref)

    def test_tiszta_munkafan_elorelep_es_az_uj_szkripttel_indul_ujra(self):
        elotte = self._hash()
        # az origin commitja az indit.sh-t is módosítja: az újraindított futásnak már az új szkriptet kell látnia
        with open(os.path.join(self.cel, 'indit.sh'), encoding='utf-8') as fh:
            szoveg = fh.read()
        masik_sh = os.path.join(self.masik, 'eszkozok', 'olvaso_szerver', 'indit.sh')
        git(self.masik, 'pull', '-q', '--ff-only', 'origin', 'main')
        with open(masik_sh, 'w', encoding='utf-8', newline='') as fh:
            fh.write(szoveg.replace('if [ "${PARDES_INDIT_CSAK_ELOKESZIT:-}" = "1" ]; then', 'naplo "FRISSÍTETT_SZKRIPT_FUT"\nif [ "${PARDES_INDIT_CSAK_ELOKESZIT:-}" = "1" ]; then', 1))
        git(self.masik, 'add', '-A')
        git(self.masik, 'commit', '-q', '-m', 'indit.sh változik')
        git(self.masik, 'push', '-q', 'origin', 'main')
        uj = git(self.masik, 'rev-parse', 'HEAD')
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('a főcheckout előrelépett: %s -> %s' % (elotte[:8], uj[:8]), ki)
        self.assertIn('újraindítás a frissített indit.sh-val', ki)
        self.assertEqual(ki.count('FRISSÍTETT_SZKRIPT_FUT'), 1, ki)
        self.assertEqual(self._hash(), uj)

    def test_naprakesz_nem_lep_es_nem_indul_ujra(self):
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('a főcheckout naprakész', ki)
        self.assertNotIn('újraindítás', ki)

    def test_piszkos_munkafan_kihagyja_de_a_fetch_lefut(self):
        elotte = self._hash()
        with open(os.path.join(self.cel, 'allapot.py'), 'a', encoding='utf-8', newline='') as f:
            f.write('# kézi módosítás\n')
        uj = origin_commit(self.masik)
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('a munkafa nem tiszta', ki)
        self.assertIn('allapot.py', ki, 'a napló megnevezi a módosított fájlt')
        self.assertEqual(self._hash(), elotte, 'piszkos munkafán nincs előreléptetés')
        self.assertEqual(self._hash('refs/remotes/origin/main'), uj, 'a fetch lefutott: a lábléc lemaradás-jelzése friss origin/main-nel igaz')
        with open(os.path.join(self.cel, 'allapot.py'), encoding='utf-8') as f:
            self.assertTrue(f.read().endswith('# kézi módosítás\n'), 'a kézi módosítás érintetlen')

    def test_koveteten_fajl_nem_akadaly(self):
        with open(os.path.join(self.fo, 'jegyzet.txt'), 'w', encoding='utf-8') as f:
            f.write('követetlen\n')
        uj = origin_commit(self.masik)
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertEqual(self._hash(), uj, ki)

    def test_nem_main_agon_kihagyja_fetch_nelkul(self):
        git(self.fo, 'checkout', '-q', '-b', 'masik-ag')
        regi = self._hash('refs/remotes/origin/main')
        uj = origin_commit(self.masik)
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('nem a main ágon áll (ág: masik-ag)', ki)
        self.assertEqual(self._hash('refs/remotes/origin/main'), regi, 'a nem main ágon a fetch sem fut')
        self.assertNotEqual(regi, uj)

    def test_nem_belso_kiadasnal_kihagyja(self):
        origin_commit(self.masik)
        elotte = self._hash()
        kod, ki = self._fut(cel=self.cel, kiadas='nyilvanos', PARDES_FRISSIT='1')
        self.assertEqual(kod, 0, ki)
        self.assertIn('csak a belso kiadásnál', ki)
        self.assertEqual(self._hash(), elotte)

    def test_eltavolodott_main_nem_lep_elore(self):
        with open(os.path.join(self.fo, 'helyi.txt'), 'w', encoding='utf-8') as f:
            f.write('helyi\n')
        git(self.fo, 'add', '-A')
        git(self.fo, 'commit', '-q', '-m', 'helyi, nem pusholt')
        helyi = self._hash()
        origin_commit(self.masik)
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('nem léptethető előre', ki)
        self.assertEqual(self._hash(), helyi, 'a helyi commit megmarad, nincs összefésülés')

    def test_sikertelen_fetch_nem_allitja_meg_az_inditast(self):
        git(self.fo, 'remote', 'set-url', 'origin', os.path.join(self.t, 'nincs_ilyen.git'))
        kod, ki = self._fo_fut()
        self.assertEqual(kod, 0, ki)
        self.assertIn('a git fetch sikertelen', ki)

    def test_frissit_0_kikapcsol_fetch_nelkul(self):
        regi = self._hash('refs/remotes/origin/main')
        origin_commit(self.masik)
        kod, ki = self._fo_fut(PARDES_FRISSIT='0')
        self.assertEqual(kod, 0, ki)
        self.assertIn('PARDES_FRISSIT=0', ki)
        self.assertEqual(self._hash('refs/remotes/origin/main'), regi)

    def test_az_elonezet_nem_huzza_a_focheckoutot(self):
        git(self.fo, 'branch', 'elo')
        wt = os.path.join(self.t, 'wt')
        git(self.fo, 'worktree', 'add', '-q', wt, 'elo')
        origin_commit(self.masik)
        elotte = self._hash()
        kod, ki = self._fut(cel=os.path.join(wt, 'eszkozok', 'olvaso_szerver'), PARDES_ELONEZET=None, PARDES_FRISSIT='1')
        self.assertEqual(kod, 0, ki)
        self.assertIn('frissítés: kihagyva — előnézeti mód', ki)
        self.assertEqual(self._hash(), elotte)

    def test_sikertelen_status_nem_tiszta_munkafa(self):
        # a git status hibája (időtúllépés, hiba) nem jelenthet „tiszta” munkafát: a merge nem futhat
        hibas = os.path.join(self.t, 'git_hibas_status.sh')
        with open(hibas, 'w', encoding='utf-8', newline='\n') as f:
            f.write('#!/bin/bash\nfor a in "$@"; do [ "$a" = status ] && { echo "fatal: proba" >&2; exit 128; }; done\nexec git "$@"\n')
        os.chmod(hibas, 0o755)
        elotte = self._hash()
        origin_commit(self.masik)
        kod, ki = self._fo_fut(PARDES_GIT=hibas)
        self.assertEqual(kod, 0, ki)
        self.assertIn('a git status sikertelen', ki)
        self.assertEqual(self._hash(), elotte, 'hibás status mellett nincs előreléptetés')

    def test_a_valodi_checkout_ellen_alapbol_vedett(self):
        # a _fut alapja PARDES_FRISSIT=0: a tesztet futtató checkout soha nem húzódik le
        kod, ki = self._fut()
        self.assertIn('PARDES_FRISSIT=0', ki)


@unittest.skipUnless(POSIX and GIT, 'az indit.sh tesztjéhez POSIX, bash, fuser, flock és git kell (WSL)')
class TesztInditElonezet(_InditAlap):
    """F225: az előnézeti mód két védelme és a forrás-adatbázis alapja, linkelt worktree-ben (ideiglenes repón)."""

    def setUp(self):
        super().setUp()
        self.fo, self.masik, fo_cel = szkript_repo(self.t)
        self.wt = os.path.join(self.t, 'wt')
        git(self.fo, 'worktree', 'add', '-q', self.wt, '-b', 'ag')
        self.cel = os.path.join(self.wt, 'eszkozok', 'olvaso_szerver')

    def _elo(self, port=0, **env):
        env.setdefault('PARDES_ELONEZET', None)                                   # automatikus felismerés a `.git` fájlból
        return self._fut(port=port, cel=self.cel, **env)

    def _figyel(self, cwd, port):
        regi = subprocess.Popen([sys.executable, '-c', 'import socket,time\ns=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);'
                                 's.bind(("127.0.0.1",%d));s.listen();time.sleep(60)' % port], cwd=cwd)
        self.addCleanup(lambda: (regi.poll() is None) and regi.kill())
        for _ in range(50):
            with socket.socket() as sk:
                if sk.connect_ex(('127.0.0.1', port)) == 0:
                    break
            time.sleep(0.1)
        return regi

    def test_ervenytelen_elonezet_ertek_hiba_nem_nem_elonezet(self):
        # egy elgépelt érték nem kapcsolhatja ki némán a védelmet (a közös másolat felülírása, idegen példány leállítása)
        kis_db(self.f, '2026-10-15T08:00:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        elotte = os.stat(self.c)
        kod, ki = self._elo(PARDES_ELONEZET='true')
        self.assertEqual(kod, 2, ki)
        self.assertIn('PARDES_ELONEZET', ki)
        self.assertNotIn('MÁSOLÁS', ki)
        self.assertEqual(elotte.st_mtime_ns, os.stat(self.c).st_mtime_ns)

    def test_worktreebol_automatikusan_elonezet(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        kod, ki = self._elo()
        self.assertEqual(kod, 0, ki)
        self.assertIn('mód: ELŐNÉZET', ki)

    def test_a_fo_checkout_nem_elonezet(self):
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        kod, ki = self._fut(cel=os.path.join(self.fo, 'eszkozok', 'olvaso_szerver'), PARDES_ELONEZET=None)
        self.assertEqual(kod, 0, ki)
        self.assertNotIn('ELŐNÉZET', ki)

    def test_a_kozos_masolatba_nem_ir(self):
        kis_db(self.f, '2026-10-15T08:00:00Z', extra='ujabb')                      # a forrás újabb: főcheckoutban ez másolást jelentene
        kis_db(self.c, '2026-10-14T09:35:00Z', extra='kozos')
        elotte = os.stat(self.c)
        with open(self.c, 'rb') as fh:
            tartalom = fh.read()
        kod, ki = self._elo()
        self.assertEqual(kod, 0, ki)
        self.assertIn('NINCS másolás', ki)
        self.assertNotIn('MÁSOLÁS', ki)
        utana = os.stat(self.c)
        self.assertEqual((elotte.st_ino, elotte.st_mtime_ns, elotte.st_size), (utana.st_ino, utana.st_mtime_ns, utana.st_size))
        with open(self.c, 'rb') as fh:
            self.assertEqual(fh.read(), tartalom)
        self.assertEqual(sorted(os.listdir(os.path.dirname(self.c))), ['pardes.db'], 'ideiglenes másolat sem maradhat')

    def test_a_kozos_masolat_hianyaban_hiba_masolas_nelkul(self):
        kis_db(self.f, '2026-10-15T08:00:00Z')
        kod, ki = self._elo()
        self.assertNotEqual(kod, 0)
        self.assertIn('HIBA: nincs adatbázis-másolat', ki)
        self.assertFalse(os.path.exists(self.c), 'előnézet nem hozza létre a közös másolatot')

    def test_a_forras_alapja_a_fo_checkout_pardes_db_je(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        fo_db = os.path.join(self.fo, 'pardes.db')
        kis_db(fo_db, '2026-10-15T08:00:00Z')
        kod, ki = self._elo(PARDES_FORRAS_DB=None)
        self.assertEqual(kod, 0, ki)
        self.assertIn(fo_db, ki)

    def test_idegen_peldanyt_nem_allit_le(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        port = self._szabad_port()
        idegen = self._figyel(self.t, port)                                       # a munkakönyvtára nem ez a checkout
        kod, ki = self._elo(port=port)
        self.assertEqual(kod, 3, ki)
        self.assertIn('idegen példány', ki)
        self.assertIn('szabad port', ki)
        self.assertIsNone(idegen.poll(), 'az idegen példánynak életben kell maradnia')

    def test_a_fo_checkout_peldanyat_sem_allitja_le_elonezetbol(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        port = self._szabad_port()
        fo_peldany = self._figyel(os.path.join(self.fo, 'eszkozok', 'olvaso_szerver'), port)
        kod, ki = self._elo(port=port)
        self.assertEqual(kod, 3, ki)
        self.assertIsNone(fo_peldany.poll())

    def test_a_sajat_checkout_regi_peldanyat_leallitja(self):
        kis_db(self.c, '2026-10-14T09:35:00Z')
        port = self._szabad_port()
        sajat = self._figyel(self.cel, port)
        kod, ki = self._elo(port=port)
        self.assertEqual(kod, 0, ki)
        self.assertIn('leállt', ki)
        self.assertIsNotNone(sajat.wait(timeout=10))

    def test_a_fo_checkout_inditasa_nem_valtozott_idegen_peldanyt_is_leallit(self):
        # a parancsikon (főcheckout, nem előnézet) továbbra is bármit leállít a portján (a tükör újraindítása)
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        port = self._szabad_port()
        regi = self._figyel(self.t, port)
        kod, ki = self._fut(port=port)
        self.assertEqual(kod, 0, ki)
        self.assertIsNotNone(regi.wait(timeout=10))


class TesztElonezetAlkalmazas(unittest.TestCase):
    """F225: az önfrissítő előnézet a valódi alkalmazáson (Flask és pardes.db kell; enélkül kimarad, kifejezetten jelölve): kulcs-végpont, kliensszkript,
    csak a `belso` kiadásban, a CSP változatlan, a lap tetejének figyelmeztetése."""

    KORNYEZET = ('PARDES_AG', 'PARDES_COMMIT', 'PARDES_FORRAS_DB', 'PARDES_LEMARADAS')

    @classmethod
    def setUpClass(cls):
        try:
            import flask  # noqa: F401
        except ImportError:
            raise unittest.SkipTest('nincs Flask: az előnézet alkalmazás-tesztje kimarad (nem zöld)')
        cls.db = os.environ.get('PARDES_DB') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(D))), 'pardes.db')
        if not os.path.isfile(cls.db):
            raise unittest.SkipTest('nincs pardes.db (%s): az előnézet alkalmazás-tesztje kimarad (nem zöld)' % cls.db)
        import alkalmazas
        cls.alk = alkalmazas

    def setUp(self):
        reg = {k: os.environ.get(k) for k in self.KORNYEZET}
        self.addCleanup(lambda: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v) for k, v in reg.items()])
        os.environ.update(PARDES_AG='main', PARDES_COMMIT='abcd1234', PARDES_LEMARADAS='0')
        os.environ.pop('PARDES_FORRAS_DB', None)

    def _kliens(self, kiadas='belso'):
        app = self.alk.letrehoz(self.db, kiadas)
        app.extensions['pardes']['gyar'].lablec.ttl = 0                         # minden kérésnél újraolvas
        return app, app.test_client()

    def test_a_kulcs_vegpont_belsoben_json_adatbazis_nelkul(self):
        app, c = self._kliens('belso')
        gyar = app.extensions['pardes']['gyar']

        def tilos(*a, **k):
            raise AssertionError('a kulcs-végpont nem olvashat adatbázist')
        gyar.db.kapcsolat = tilos                                              # a /statusz ezen át olvas; a kulcs-végpontnak nem kell
        r = c.get('/elonezet/kulcs')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.headers['Content-Type'].startswith('application/json'))
        self.assertEqual(r.headers['Cache-Control'], 'no-store')
        j = r.get_json()
        for kulcs in ('azonosito', 'kod_verzio', 'arculat_hash', 'lablec', 'adatbazis_kulcs', 'ag', 'commit', 'lemaradas'):
            self.assertIn(kulcs, j)
        self.assertEqual((j['kod_verzio'], j['arculat_hash'], j['adatbazis_kulcs']), (gyar.kod_verzio, gyar.arculat.hash, gyar.kozos.adatbazis_kulcs))
        self.assertEqual((j['ag'], j['commit'], j['lemaradas']), ('main', 'abcd1234', 0))
        self.assertEqual(c.get('/elonezet/kulcs').get_json()['azonosito'], j['azonosito'], 'változatlan állapotnál stabil')

    def test_az_azonosito_valtozik_az_allapottal(self):
        app, c = self._kliens('belso')
        a = c.get('/elonezet/kulcs').get_json()['azonosito']
        os.environ['PARDES_AG'] = 'claude/valami'                              # ágváltás
        b = c.get('/elonezet/kulcs').get_json()['azonosito']
        os.environ['PARDES_AG'] = 'main'
        os.environ['PARDES_LEMARADAS'] = '5'                                   # lemaradás
        d = c.get('/elonezet/kulcs').get_json()['azonosito']
        self.assertEqual(len({a, b, d}), 3)
        gyar = app.extensions['pardes']['gyar']
        gyar.kod_verzio = 'masik'                                              # kódváltozás (az újratöltő újraindítása után)
        self.assertNotEqual(c.get('/elonezet/kulcs').get_json()['azonosito'], d)

    def test_a_lap_a_kiindulo_azonositot_hordozza(self):
        app, c = self._kliens('belso')
        azon = c.get('/elonezet/kulcs').get_json()['azonosito']
        h = c.get('/1Moz/1/1').get_data(as_text=True)
        self.assertIn('<script src="/elonezet/elonezet.js?v=%s" data-azonosito="%s" defer></script>' % (azon, azon), h)

    def test_csak_a_belso_kiadasban(self):
        for kiadas in ('nyilvanos', 'kereskedelmi'):
            with self.subTest(kiadas=kiadas):
                app, c = self._kliens(kiadas)
                self.assertEqual(c.get('/elonezet/kulcs').status_code, 404)
                self.assertEqual(c.get('/elonezet/elonezet.js').status_code, 404, 'a kliens nem szolgálható ki más kiadásban')
                self.assertEqual(c.get('/statikus/elonezet.js').status_code, 404, 'nem is a mindenkinek kiszolgált statikus/-ban áll')
                self.assertEqual(c.get('/tervezo/elonezet.js').status_code, 404)
                h = c.get('/1Moz/1/1').get_data(as_text=True)
                self.assertNotIn('elonezet.js', h)
                self.assertNotIn('data-azonosito', h)
                self.assertFalse(app.extensions['pardes']['gyar'].elonezet)
        app, c = self._kliens('belso')
        self.assertEqual(c.get('/elonezet/kulcs').status_code, 200)

    def test_a_csp_nem_lazul(self):
        app, c = self._kliens('belso')
        for ut in ('/1Moz/1/1', '/elonezet/kulcs', '/elonezet/elonezet.js'):
            r = c.get(ut)
            self.assertEqual(r.headers['Content-Security-Policy'], self.alk.CSP, ut)
        self.assertIn("script-src 'self'", self.alk.CSP)
        self.assertNotIn('unsafe', self.alk.CSP)
        h = c.get('/1Moz/1/1').get_data(as_text=True)
        import re
        for tag in re.findall(r'<script\b[^>]*>', h):
            self.assertIn('src=', tag, 'inline szkript nem lehet: ' + tag)

    def test_a_kliens_kiszolgalva_es_tartalma(self):
        app, c = self._kliens('belso')
        r = c.get('/elonezet/elonezet.js')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.headers['Content-Type'].startswith('text/javascript'))
        self.assertEqual(c.get('/statikus/elonezet.js').status_code, 404)
        js = r.get_data(as_text=True)
        for resz in ('/elonezet/kulcs', 'data-tervezo', 'location.reload', 'visibilitychange', 'data-azonosito', 'document.hidden'):
            self.assertIn(resz, js)
        self.assertNotIn('classList', js, 'a kliens nem vezet be CSS-osztályt (regiszter-őr)')
        self.assertNotIn('className', js)
        self.assertNotIn('innerHTML', js)

    @unittest.skipUnless(shutil.which('node'), 'nincs node: a szintaxis-ellenőrzés kimarad')
    def test_a_kliens_szintaxisa(self):
        p = subprocess.run(['node', '--check', os.path.join(D, 'tervezo_statikus', 'elonezet.js')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_a_figyelt_fajlok_kozt_a_tervezo_statikus_es_a_kliens(self):
        fajlok = [f.replace(os.sep, '/') for f in self.alk.figyelt_fajlok()]
        self.assertTrue(any(f.endswith('tervezo_statikus/tervezo.js') for f in fajlok))
        self.assertTrue(any(f.endswith('tervezo_statikus/tervezo.css') for f in fajlok))
        self.assertTrue(any(f.endswith('tervezo_statikus/elonezet.js') for f in fajlok))
        self.assertFalse(any(os.path.basename(f).startswith('arculat.json') for f in fajlok), 'az arculat.json továbbra sem figyelt')

    def test_a_lap_tetejen_is_megjelenik_a_figyelmeztetes_regisztralt_osztallyal(self):
        import re
        app, c = self._kliens('belso')
        os.environ['PARDES_AG'] = 'claude/valami'
        os.environ['PARDES_LEMARADAS'] = '12'
        h = c.get('/1Moz/1/1').get_data(as_text=True)
        fej = h.index('<header')
        felso = h[h.index('>', h.index('<body')) + 1:fej]                      # a <body> címke után, a fejlécig
        self.assertIn('role="status"', felso)
        self.assertIn('Figyelem:', felso)
        self.assertIn('claude/valami', felso)
        self.assertIn('12 committal az origin/main mögött', felso)
        self.assertEqual(set(re.findall(r'class="([^"]*)"', felso)), {'labjegyzet'}, 'csak a regisztrált osztály')
        self.assertIn('Figyelem:', h[h.index('<footer'):], 'a lábléc figyelmeztetése megmarad')

    def test_main_ag_naprakeszen_nincs_felso_sav(self):
        app, c = self._kliens('belso')
        h = c.get('/1Moz/1/1').get_data(as_text=True)
        self.assertNotIn('role="status"', h)
        self.assertNotIn('Figyelem:', h)


def windows_temp_wsl():
    """A Windows ideiglenes könyvtára WSL-útként; None, ha nem WSL vagy nincs `cmd.exe`/`wslpath`."""
    if not (shutil.which('cmd.exe') and shutil.which('wslpath') and shutil.which('git.exe') and os.path.isdir('/mnt/c')):
        return None
    try:
        win = subprocess.run(['cmd.exe', '/c', 'echo %TEMP%'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=20, cwd='/mnt/c').stdout.strip()
        ut = subprocess.run(['wslpath', '-u', win], stdout=subprocess.PIPE, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    return ut if ut and os.path.isdir(ut) else None


@unittest.skipUnless(POSIX and GIT and windows_temp_wsl(), 'a git.exe-s úthoz WSL, Windows-git és a Windows ideiglenes könyvtára kell')
class TesztInditGitExe(_InditAlap):
    """F225: a /mnt/<meghajtó> alatti főcheckoutnál az indító a Windows-oldali `git.exe`-t hívja (a WSL-git ott ~85 s és hamisan piszkos); a PARDES_GIT
    nélküli, automatikus választás végig, valódi git.exe-vel, a Windows-meghajtón lévő ideiglenes repón."""

    def setUp(self):
        super().setUp()
        self.w = tempfile.mkdtemp(prefix='indito_exe_', dir=windows_temp_wsl())
        self.addCleanup(shutil.rmtree, self.w, True)
        kis_db(self.f, '2026-10-14T09:35:00Z')
        kis_db(self.c, '2026-10-14T09:35:00Z')
        self.fo, self.masik, self.cel = szkript_repo(self.w)
        # a git.exe a Linux-útvonalú távolit nem érti: a főcheckout origin-je Windows-útvonal (a második klón a Linux-úton ír ugyanabba a bare repóba)
        win = subprocess.run(['wslpath', '-m', os.path.join(self.w, 'origin.git')], stdout=subprocess.PIPE, text=True).stdout.strip()
        git(self.fo, 'remote', 'set-url', 'origin', win)

    def test_automatikus_git_exe_elorelep_es_piszkosnal_kihagy(self):
        elotte = git(self.fo, 'rev-parse', 'HEAD')
        uj = origin_commit(self.masik)
        kod, ki = self._fut(cel=self.cel, PARDES_FRISSIT='1')
        self.assertEqual(kod, 0, ki)
        self.assertIn('a főcheckout előrelépett: %s -> %s' % (elotte[:8], uj[:8]), ki)
        self.assertEqual(git(self.fo, 'rev-parse', 'HEAD'), uj)
        # piszkos munkafa: a git.exe is észleli, és nincs előreléptetés
        with open(os.path.join(self.cel, 'allapot.py'), 'a', encoding='utf-8', newline='') as f:
            f.write('# kézi módosítás\n')
        uj2 = origin_commit(self.masik, fajl='masodik.txt')
        kod, ki = self._fut(cel=self.cel, PARDES_FRISSIT='1')
        self.assertEqual(kod, 0, ki)
        self.assertIn('a munkafa nem tiszta', ki)
        self.assertEqual(git(self.fo, 'rev-parse', 'HEAD'), uj)
        self.assertNotEqual(uj, uj2)


# -- #101: az adat frissessége és az automatikus újraépítés -------------------------------------------------------------------
def adat_gyoker(ut, fajlok=None):
    """Kis forrásfa (`adat/`, `konkordancia/`) az `ut` alatt."""
    for r, tartalom in (fajlok or {'adat/a.tsv': 'egy\tketto\n', 'adat/b.tsv': 'x\ty\n', 'konkordancia/k.tsv': 'strong\tszo\nH1\talef\n'}).items():
        f = os.path.join(ut, *r.split('/'))
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w', encoding='utf-8', newline='') as fh:
            fh.write(tartalom)
    return ut


def db_forras_azonositoval(ut, gyoker, ts='2026-11-22T10:00:00Z'):
    """Kis adatbázis, amelynek `meta` táblája a `gyoker` mostani forrás-azonosítóját tárolja (mintha az építő írta volna)."""
    kis_db(ut, ts)
    con = sqlite3.connect(ut)
    con.executemany('INSERT INTO meta VALUES (?, ?)', FA.meta_sorok(FA.azonosito(gyoker)))
    con.commit()
    con.close()


class TesztForrasAzonosito(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='forras_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.g = adat_gyoker(os.path.join(self.t, 'gy'))
        self.db = os.path.join(self.t, 'x.db')
        db_forras_azonositoval(self.db, self.g)

    def _all(self):
        return allapot.forras_allapot(self.g, self.db)

    def test_valtozatlan_friss(self):
        self.assertEqual(self._all(), ('friss', []))

    def test_csak_az_mtime_valtozik_a_sha256_dont_friss(self):
        # kicsekkoláskor / másoláskor az mtime tartalomváltozás nélkül is módosul: nem indulhat felesleges építés (DT-F101a)
        f = os.path.join(self.g, 'adat', 'a.tsv')
        os.utime(f, (time.time() - 5000, time.time() - 5000))
        self.assertEqual(self._all(), ('friss', []))

    def test_azonos_meretu_tartalomvaltozas_regebbi(self):
        f = os.path.join(self.g, 'konkordancia', 'k.tsv')
        with open(f, 'w', encoding='utf-8', newline='') as fh:
            fh.write('strong\tszo\nH1\tbet!\n')                 # ugyanannyi bájt, más tartalom
        os.utime(f, (time.time() + 100, time.time() + 100))
        allapot_, valt = self._all()
        self.assertEqual(allapot_, 'regebbi')
        self.assertEqual(valt, ['konkordancia/k.tsv (módosult)'])

    def test_meretvaltozas_regebbi(self):
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        self.assertEqual(self._all(), ('regebbi', ['adat/b.tsv (módosult)']))

    def test_uj_es_torolt_fajl_regebbi(self):
        adat_gyoker(self.g, {'adat/uj.tsv': 'a\n'})
        os.remove(os.path.join(self.g, 'adat', 'b.tsv'))
        allapot_, valt = self._all()
        self.assertEqual(allapot_, 'regebbi')
        self.assertEqual(valt, ['adat/b.tsv (törölt)', 'adat/uj.tsv (új)'])

    def test_nem_forras_fajl_nem_szamit(self):
        # dokumentáció (.md), LLM-hívásnapló (.jsonl), .html: az építő nem olvassa, a változásuk nem kérhet újraépítést (ELLENOR_F101)
        for n in ('adat/x.db', 'adat/x.tmp', 'adat/.rejtett', 'adat/SEMA.md', 'adat/hivas.jsonl', 'konkordancia/README.md', 'konkordancia/o.html'):
            adat_gyoker(self.g, {n: 'barmi'})
        adat_gyoker(self.g, {'motivumlog/m.md': 'nem forras', 'motivumok/m.txt': 'nem .md'})
        self.assertEqual(self._all(), ('friss', []))

    def test_a_tanulmanyszoveg_valtozasa_regebbi(self):
        # az építő a `motivumok/`, `tematikus_lezart/` stb. `.md` fájljait az FTS-be tölti: a változásuk után az adatbázis elavult (ELLENOR_F101)
        adat_gyoker(self.g, {'motivumok/m.md': 'elso\n'})
        db_forras_azonositoval(self.db, self.g)
        self.assertEqual(self._all(), ('friss', []))
        with open(os.path.join(self.g, 'motivumok', 'm.md'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('masodik\n')
        self.assertEqual(self._all(), ('regebbi', ['motivumok/m.md (módosult)']))

    def test_regi_adatbazis_forras_azonosito_nelkul(self):
        kis_db(self.db, '2026-11-22T10:00:00Z')
        self.assertEqual(self._all(), ('nincs_adat', []))
        self.assertEqual(allapot.forras_allapot(self.g, os.path.join(self.t, 'nincs.db')), ('nincs_adat', []))

    def test_az_osszeg_a_tartalomtol_fugg(self):
        a = FA.osszeg(FA.azonosito(self.g))
        self.assertEqual(a, FA.osszeg(FA.azonosito(self.g)))
        with open(os.path.join(self.g, 'adat', 'a.tsv'), 'w', encoding='utf-8', newline='') as fh:
            fh.write('masik\ttartalom\n')
        self.assertNotEqual(a, FA.osszeg(FA.azonosito(self.g)))

    def test_a_sha_gyorsitotar_nem_hasheli_ujra(self):
        f = os.path.join(self.g, 'adat', 'a.tsv')
        os.utime(f, (time.time() - 5000, time.time() - 5000))
        tar = {}
        self.assertEqual(allapot.forras_allapot(self.g, self.db, tar)[0], 'friss')
        self.assertEqual(len(tar), 1)
        sha = list(tar.values())[0]
        k = list(tar)[0]
        tar[k] = 'hamis'                                        # ha a gyorsítótárat használja, az eltérést a hamis érték okozza
        self.assertEqual(allapot.forras_allapot(self.g, self.db, tar)[0], 'regebbi')
        self.assertNotEqual(sha, 'hamis')

    def test_cli_forras(self):
        p = subprocess.run([sys.executable, os.path.join(D, 'allapot.py'), 'forras', self.g, self.db], stdout=subprocess.PIPE, text=True, encoding='utf-8')
        self.assertEqual(p.stdout.strip().split('\t')[:2], ['friss', '0'])


class TesztAdatAllapotLablec(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix='adatlablec_')
        self.addCleanup(shutil.rmtree, self.t, True)
        self.g = adat_gyoker(os.path.join(self.t, 'gy'))
        self.db = os.path.join(self.t, 'x.db')
        db_forras_azonositoval(self.db, self.g)

    def test_szinkron_es_hatterszal_ugyanazt_adja(self):
        self.assertEqual(allapot.adat_allapot(self.g, self.db, szinkron=True), ('friss', []))
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        allapot.adat_allapot(self.g, self.db, ttl=0.0)           # háttérszámítás indul
        ertek = None
        for _ in range(100):
            ertek = allapot.adat_allapot(self.g, self.db, ttl=3600.0)
            if ertek and ertek[0] == 'regebbi':
                break
            time.sleep(0.05)
        self.assertEqual(ertek, ('regebbi', ['adat/b.tsv (módosult)']))

    def test_figyelmeztetes_regebbi_az_adatnal(self):
        ki = allapot.figyelmeztetesek('main', 'T', 'T', None, ('regebbi', ['adat/a.tsv (módosult)', 'adat/b.tsv (új)']), None)
        self.assertEqual(len(ki), 1)
        self.assertIn('régebbi az adatnál', ki[0])
        self.assertIn('2 változott forrásfájl', ki[0])
        self.assertIn('adat/a.tsv (módosult)', ki[0])

    def test_friss_adat_nincs_figyelmeztetes(self):
        self.assertEqual(allapot.figyelmeztetesek('main', 'T', 'T', None, ('friss', []), None), [])
        self.assertEqual(allapot.figyelmeztetesek('main', 'T', 'T', None, None, None), [])

    def test_regi_epites_figyelmeztet(self):
        ki = allapot.figyelmeztetesek('main', 'T', 'T', None, ('nincs_adat', []), None)
        self.assertEqual(len(ki), 1)
        self.assertIn('nincs forrás-azonosító', ki[0])

    def test_epites_folyamatban_es_elbukott(self):
        ki = allapot.figyelmeztetesek('main', 'T', 'T', None, None, ('fut', '2026-11-22T10:00:00', '', ''))
        self.assertIn('újraépítése folyamatban', ki[0])
        self.assertIn('2026-11-22T10:00:00', ki[0])
        ki = allapot.figyelmeztetesek('main', 'T', 'T', None, None, ('elbukott', '2026-11-22T10:05:00', 'INTEGRITÁS-SÉRTÉS', '/x/epites.log'))
        self.assertIn('elbukott', ki[0])
        self.assertIn('INTEGRITÁS-SÉRTÉS', ki[0])
        self.assertIn('/x/epites.log', ki[0])
        self.assertEqual(allapot.figyelmeztetesek('main', 'T', 'T', None, None, ('kesz', 'x', '', '')), [])

    def test_keszit_a_kornyezetbol(self):
        env = {'PARDES_FORRAS_GYOKER': self.g, 'PARDES_DB': self.db, 'PARDES_AG': 'main', 'PARDES_COMMIT': 'abc', 'PARDES_LEMARADAS': '0'}
        allapot.adat_allapot(self.g, self.db, szinkron=True)
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        allapot.adat_allapot(self.g, self.db, szinkron=True)
        l = allapot.Lablec.keszit('belso', '2026-11-22T10:00:00Z', kornyezet=env)
        self.assertTrue(any('régebbi az adatnál' in f for f in l.figyelmeztetesek), l.figyelmeztetesek)
        self.assertEqual(l.adat[0], 'regebbi')
        # környezeti változó nélkül (előnézet, teszt) nincs adat-ellenőrzés
        l2 = allapot.Lablec.keszit('belso', '2026-11-22T10:00:00Z', kornyezet={'PARDES_AG': 'main', 'PARDES_COMMIT': 'abc', 'PARDES_LEMARADAS': '0'})
        self.assertIsNone(l2.adat)
        self.assertEqual(l2.figyelmeztetesek, [])

    def test_epites_allapot_fajl(self):
        f = os.path.join(self.t, 'allapot.tsv')
        self.assertEqual(allapot.epites_allapot(f)[0], 'nincs')
        with open(f, 'w', encoding='utf-8', newline='') as fh:
            fh.write('kesz\t2026-11-22T10:00:00\t1\tkész\t/n.log\n')
        self.assertEqual(allapot.epites_allapot(f), ('kesz', '2026-11-22T10:00:00', 'kész', '/n.log'))
        with open(f, 'w', encoding='utf-8', newline='') as fh:
            fh.write('fut\t2026-11-22T10:00:00\t%d\tfut\t/n.log\n' % os.getpid())
        self.assertEqual(allapot.epites_allapot(f)[0], 'fut')
        if os.name == 'posix':
            with open(f, 'w', encoding='utf-8', newline='') as fh:
                fh.write('fut\t2026-11-22T10:00:00\t4194999\tfut\t/n.log\n')       # nem élő pid: megszakadt, nem „fut”
            self.assertEqual(allapot.epites_allapot(f)[0], 'elbukott')

    def test_db_ellenoriz(self):
        self.assertEqual(allapot.db_ellenoriz(self.db), 'ok')
        kis_db(self.db, '2026-11-22T10:00:00Z')
        self.assertEqual(allapot.db_ellenoriz(self.db), 'nincs forrás-azonosító')
        kis_db(self.db, None)
        self.assertEqual(allapot.db_ellenoriz(self.db), 'nincs epites_ts')
        self.assertEqual(allapot.db_ellenoriz(os.path.join(self.t, 'nincs.db')), 'nincs fájl')
        with open(self.db, 'wb') as fh:
            fh.write(b'ez nem adatbazis' * 100)
        self.assertNotEqual(allapot.db_ellenoriz(self.db), 'ok')


@unittest.skipUnless(POSIX, 'az indit.sh tesztjéhez POSIX, bash, fuser és flock kell (WSL)')
class TesztInditUjraepites(_InditAlap):
    """Az `indit.sh` (2b) lépése és az `epit_hatter.sh`: háttér-újraépítés hamis építővel (kis adatbázis), a valódi forráshoz nem nyúl."""

    EPIT_PARANCS = (
        'python3 - "$1" <<"PY"\n'
        'import sqlite3, sys, os\n'
        'ut = sys.argv[1]\n'
        'con = sqlite3.connect(ut)\n'
        'con.execute("CREATE TABLE meta (kulcs TEXT PRIMARY KEY, ertek TEXT)")\n'
        'con.execute("INSERT INTO meta VALUES (?, ?)", ("epites_ts", "2026-11-22T11:00:00Z"))\n'
        'con.execute("INSERT INTO meta VALUES (?, ?)", ("forras_osszeg", "x"))\n'
        'con.commit(); con.close()\n'
        'PY\n')

    def setUp(self):
        super().setUp()
        self.g = adat_gyoker(os.path.join(self.t, 'gy'))
        self.allapot_f = os.path.join(self.t, 'epites_allapot.tsv')

    def _epit(self, **env):
        kod, ki = self._fut(PARDES_EPIT='1', PARDES_ADAT_GYOKER=self.g, PARDES_EPIT_PARANCS=env.pop('parancs', self.EPIT_PARANCS), **env)
        return kod, ki

    def _vegere_var(self):
        for _ in range(1500):
            a = allapot.epites_allapot(self.allapot_f)[0]
            if a in ('kesz', 'elbukott'):
                return a
            time.sleep(0.05)
        return allapot.epites_allapot(self.allapot_f)[0]

    def test_friss_adat_nem_epit(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        kod, ki = self._epit()
        self.assertEqual(kod, 0, ki)
        self.assertIn('adat: az adatbázis friss', ki)
        self.assertNotIn('INDUL', ki)
        self.assertFalse(os.path.exists(self.allapot_f))

    def test_regebbi_adat_hatterben_ujraepit_a_windows_oldali_peldanyt_cserel_a_wsl_masolat_nem(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        kod, ki = self._epit()
        self.assertEqual(kod, 0, ki)
        self.assertIn('az adatbázis régebbi az adatnál (1 változás', ki)
        self.assertIn('újraépítés: INDUL a háttérben', ki)
        self.assertEqual(self._vegere_var(), 'kesz', open(os.path.join(self.t, 'epites.log'), encoding='utf-8').read())
        # a futó szerver alatt a WSL-másolat nem változik (ELLENOR_F101); a Windows-oldali példány az új, a következő indítás szinkronizálja
        self.assertEqual(allapot.db_epites_ts(self.f), '2026-11-22T11:00:00Z')
        self.assertEqual(allapot.db_epites_ts(self.c), '2026-11-22T10:00:00Z')
        self.assertEqual([n for n in os.listdir(os.path.dirname(self.c)) if '.epit.' in n or '.forras.' in n], [])
        kod2, ki2 = self._fut(PARDES_EPIT='0')
        self.assertIn('MÁSOLÁS', ki2)
        self.assertEqual(allapot.db_epites_ts(self.c), '2026-11-22T11:00:00Z')
        self.assertIn('másolás a Windows-oldalra', allapot.epites_allapot(self.allapot_f)[2])

    def test_az_epites_elbukasakor_a_regi_adatbazis_erintetlen(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        elotte = open(self.c, 'rb').read()
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        kod, ki = self._epit(parancs='echo "INTEGRITÁS-SÉRTÉS: teszt"; exit 1')
        self.assertEqual(kod, 0, ki)
        self.assertEqual(self._vegere_var(), 'elbukott')
        a = allapot.epites_allapot(self.allapot_f)
        self.assertIn('INTEGRITÁS-SÉRTÉS', a[2])
        self.assertEqual(open(self.c, 'rb').read(), elotte)
        self.assertEqual(allapot.db_epites_ts(self.f), '2026-11-22T10:00:00Z')
        # a lábléc elbukott figyelmeztetést ad
        self.assertTrue(any('elbukott' in f for f in allapot.figyelmeztetesek('main', 'T', 'T', None, None, a)))

    def test_hibas_uj_adatbazis_nem_cserel(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        elotte = open(self.c, 'rb').read()
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        self._epit(parancs='head -c 2000 /dev/urandom > "$1"')   # nem adatbázis, de az építő „sikeresnek” jelzi
        self.assertEqual(self._vegere_var(), 'elbukott')
        self.assertEqual(open(self.c, 'rb').read(), elotte)

    def test_ket_egyideju_inditas_egy_epitest_indit(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        lassu = 'sleep 25; ' + self.EPIT_PARANCS
        _, ki1 = self._epit(parancs=lassu)
        _, ki2 = self._epit(parancs=lassu)
        self.assertIn('INDUL a háttérben', ki1)
        self.assertIn('már fut egy másik építés', ki2)
        self.assertNotIn('INDUL', ki2)
        self.assertEqual(self._vegere_var(), 'kesz')

    def test_elonezetben_nem_epit(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        with open(os.path.join(self.g, 'adat', 'b.tsv'), 'a', encoding='utf-8', newline='') as fh:
            fh.write('uj\tsor\n')
        kod, ki = self._epit(PARDES_ELONEZET='1')
        self.assertIn('újraépítés: kihagyva — előnézeti mód', ki)
        self.assertFalse(os.path.exists(self.allapot_f))

    def test_epit_hatter_kezi_modja_a_zarat_veszi_es_kiirja_a_naplot(self):
        # a „PaRDeS adatbázis újraépítése” asztali parancsikon belépési pontja: `epit_hatter.sh --kezi`
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        env = dict(os.environ, PARDES_GYOKER=self.g, PARDES_PY=sys.executable, PARDES_DB=self.c, PARDES_FORRAS_DB=self.f, PARDES_EPITES_ALLAPOT=self.allapot_f,
                   PARDES_EPITES_NAPLO=os.path.join(self.t, 'kezi.log'), PARDES_EPIT_ZAR=os.path.join(self.t, 'kezi.zar'), PARDES_EPIT_PARANCS=self.EPIT_PARANCS)
        p = subprocess.run(['bash', os.path.join(D, 'epit_hatter.sh'), '--kezi'], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                           timeout=120)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('[epit]', p.stdout)
        self.assertEqual(allapot.epites_allapot(self.allapot_f)[0], 'kesz')
        self.assertEqual(allapot.db_epites_ts(self.f), '2026-11-22T11:00:00Z')
        # zár alatt: a második kézi indítás nem épít
        zar = open(os.path.join(self.t, 'kezi.zar'), 'w')
        import fcntl
        fcntl.flock(zar, fcntl.LOCK_EX | fcntl.LOCK_NB)
        p2 = subprocess.run(['bash', os.path.join(D, 'epit_hatter.sh'), '--kezi'], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                            timeout=120)
        zar.close()
        self.assertNotEqual(p2.returncode, 0)
        self.assertIn('már fut egy másik újraépítés', p2.stdout)

    def test_kezi_ujraepites_frissnel_is_epit(self):
        db_forras_azonositoval(self.c, self.g, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        kod, ki = self._epit(PARDES_EPIT_KEZI='1')
        self.assertIn('kézi újraépítés kérve', ki)
        self.assertEqual(self._vegere_var(), 'kesz')

    def test_regi_adatbazis_forras_azonosito_nelkul_ujraepul(self):
        kis_db(self.c, '2026-11-22T10:00:00Z')
        kis_db(self.f, '2026-11-22T10:00:00Z')
        kod, ki = self._epit()
        self.assertIn('régi építés', ki)
        self.assertEqual(self._vegere_var(), 'kesz')


if __name__ == '__main__':
    unittest.main(verbosity=2)
