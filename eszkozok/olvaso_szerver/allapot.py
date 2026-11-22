"""Az olvasó-szerver indítási és lábléc-állapota (#100): ág, commit, adatbázis-építési idő, adatbázis-szinkron döntés.

Csak a szabványos könyvtárat használja (nem függ a Flasktól). Az ág és a commit megállapításához NEM hív `git`-et: a worktree-k `.git`
fájlja Windows-útra mutat (`gitdir: C:/…`), amit a WSL-beli `git` nem old fel; ezért a `HEAD`-et és a ref-eket maga olvassa (és a Windows-utat
`/mnt/c/…`-re fordítja, ha kell). Kivétel a **lemaradás** (F225): a commitok számát a csomagolt objektumokból csak a `git rev-list --count`
adja, ezért azt a `git` a már feloldott `--git-dir`-rel számolja, csak a ref-ek változásakor, háttérszálon (`lemaradas`).

Parancssor (az `indit.sh` hívja):
    python allapot.py dontes <forras.db> <cel.db>    # kiírja: <döntés>\\t<forrás epites_ts>\\t<cél epites_ts>
    python allapot.py git [<könyvtár>]               # kiírja: <ág>\\t<rövid commit>
    python allapot.py epites_ts <db>                 # kiírja: a meta.epites_ts-t (üres, ha nincs)
    python allapot.py forras <gyoker> <db>           # kiírja: <friss|regebbi|nincs_adat>	<változások száma>	<az első néhány változás> (#101)
    python allapot.py db_ellenoriz <db>              # kiírja: ok, vagy a hiba szövege (az új adatbázis ellenőrzése csere előtt, #101)
    python allapot.py epites_allapot <fájl>          # kiírja: <fut|kesz|elbukott|nincs>	<idő>	<üzenet> (az indító háttér-újraépítésének állapotfájlja, #101)
    python allapot.py lemaradas [<könyvtár>]         # kiírja: hány committal áll a HEAD az origin/main mögött (üres, ha nem állapítható meg)
    python allapot.py checkout [<könyvtár>]          # kiírja: <fo|elonezet>\t<a főcheckout gyökere>\t<a munkafa gyökere> (elonezet = linkelt worktree)
Döntések: `masol` (a forrás építési ideje eltér vagy a cél hiányzik/olvashatatlan), `azonos` (nincs másolás), `nincs_forras`
(a forrás hiányzik vagy nincs epites_ts: nem másolunk, a meglévő célt hagyjuk).
"""
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SZERVER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SZERVER_DIR)
import lekerdezesek                                  # noqa: E402  (stdlib-only modul; parancssori hívásnál a saját könyvtár nincs mindig a sys.path-on)
import forras_azonosito as FA                        # noqa: E402  (#101: stdlib-only, a szerverkönyvtárban áll; az `sqlite_epit.py` is ezt használja)
FO_AG = 'main'
ISMERETLEN = 'ismeretlen'


# -- adatbázis ------------------------------------------------------------------------------------------------------------
def db_epites_ts(ut):
    """A `meta.epites_ts` (csak olvasó kapcsolat, egyetlen kis lekérdezés: a fájl többi részét nem olvassa be). Hiányzó fájl, hiányzó
    tábla vagy hiányzó kulcs: üres szöveg."""
    if not ut or not os.path.isfile(ut):
        return ''
    try:
        con = sqlite3.connect('file:%s?mode=ro' % ut.replace('\\', '/'), uri=True)
        try:
            ts = lekerdezesek.meta(con).get('epites_ts')      # az SQL csak a lekerdezesek.py-ban áll (teszt_olvaso_szerver: test_sql_csak_a_lekerdezesekben)
        finally:
            con.close()
    except sqlite3.Error:
        return ''
    return str(ts) if ts is not None else ''


# -- az adat frissessége (#101) ---------------------------------------------------------------------------------------------
def db_forras_azonosito(ut):
    """Az adatbázis `meta` táblájába építéskor rögzített forrás-azonosító: {útvonal: (méret, mtime, sha256)}; üres, ha nincs (régi építés, hiányzó
    vagy olvashatatlan fájl). Az SQL csak a lekerdezesek.py-ban áll."""
    if not ut or not os.path.isfile(ut):
        return {}
    try:
        con = sqlite3.connect('file:%s?mode=ro' % ut.replace(chr(92), '/'), uri=True)
        try:
            meta = lekerdezesek.meta(con)
        finally:
            con.close()
    except sqlite3.Error:
        return {}
    return FA.meta_olvas(list(meta.items()))


def db_ellenoriz(ut):
    """Az újonnan épített adatbázis ellenőrzése a csere előtt: `ok`, vagy a hiba szövege. Feltételek: megnyitható, `quick_check` ép, van `epites_ts`
    és forrás-azonosító (`forras_osszeg`) a `meta` táblában."""
    if not ut or not os.path.isfile(ut):
        return 'nincs fájl'
    try:
        con = sqlite3.connect('file:%s?mode=ro' % ut.replace(chr(92), '/'), uri=True)
        try:
            ell = lekerdezesek.gyors_ellenorzes(con)
            meta = lekerdezesek.meta(con)
        finally:
            con.close()
    except sqlite3.Error as exc:
        return 'nem olvasható: %s' % exc
    if ell != ['ok']:
        return 'quick_check: %s' % '; '.join(str(x) for x in ell[:3])
    if not meta.get('epites_ts'):
        return 'nincs epites_ts'
    if not meta.get(FA.META_OSSZEG):
        return 'nincs forrás-azonosító'
    return 'ok'


def forras_allapot(gyoker, db, sha_tar=None):
    """(`friss` | `regebbi` | `nincs_adat`, változások): a `gyoker` forrásfájljai az adatbázis építésekor rögzítettekhez képest. Hiányzó adatbázis:
    `nincs_adat`. Az mtime+méret az előszűrő; eltérésnél a sha256 dönt (DT-F101a)."""
    return FA.osszehasonlit(gyoker, db_forras_azonosito(db), sha_tar)


_ADAT_TAR = {}                                           # (gyoker, db) -> (monotonic, (allapot, valtozasok)) | None, amíg az első számítás fut
_ADAT_SHA = {}                                           # a sha256-ok gyorsítótára (útvonal, méret, mtime) -> sha256
_ADAT_ZAR = threading.Lock()
ADAT_TTL = 3.0


def adat_allapot(gyoker, db, ttl=None, szinkron=False):
    """A `forras_allapot` háttérszálon, gyorsítótárral: a lap kiszolgálását soha nem tartja fel (452 fájl `stat`-ja a /mnt-n lassú lehet). Az érték
    legfeljebb `ttl` (alap: 3 s) + a számítás idejéig régi; az első híváskor None (még nem ismert). `szinkron=True`: helyben, a tesztekhez."""
    if not gyoker or not db:
        return None
    ttl = ADAT_TTL if ttl is None else ttl
    kulcs = (os.path.abspath(gyoker), os.path.abspath(db))
    if szinkron:
        ertek = forras_allapot(gyoker, db, _ADAT_SHA)
        with _ADAT_ZAR:
            _ADAT_TAR[kulcs] = (time.monotonic(), ertek)
        return ertek
    most = time.monotonic()
    with _ADAT_ZAR:
        van = _ADAT_TAR.get(kulcs, False)                # False: még nem számoltuk; None: az első számítás fut; (ts, érték): kész
        indit = van is False or (van is not None and most - van[0] >= ttl)
        if indit:                                        # a régi érték látszik tovább, és a következő számítás addig nem indul újra
            _ADAT_TAR[kulcs] = None if not van else (most, van[1])
    if indit:
        def _szal():
            try:
                ertek = forras_allapot(gyoker, db, _ADAT_SHA)
            except OSError:
                ertek = None
            with _ADAT_ZAR:
                _ADAT_TAR[kulcs] = (time.monotonic(), ertek)
        threading.Thread(target=_szal, daemon=True).start()
    with _ADAT_ZAR:
        van = _ADAT_TAR.get(kulcs)
    return van[1] if van else None


def epites_allapot(ut):
    """Az indító háttér-újraépítésének állapotfájlja (egy sor: `<állapot>	<idő>	<pid>	<üzenet>	<naplófájl>`): (állapot, idő, üzenet, napló).
    Állapot: `fut` | `kesz` | `elbukott` | `nincs` (nincs fájl). A `fut`, de már nem élő folyamat `elbukott` (megszakadt)."""
    szoveg = _olvas(ut) if ut else None
    if not szoveg:
        return 'nincs', '', '', ''
    r = (szoveg.splitlines() or [''])[0].split('	')
    r += [''] * (5 - len(r))
    allapot, ido, pid, uzenet, napló = r[:5]
    if allapot == 'fut' and pid.isdigit() and os.name == 'posix' and not os.path.exists('/proc/%s' % pid):
        return 'elbukott', ido, 'az újraépítés megszakadt (a folyamat már nem fut)', napló
    if allapot not in ('fut', 'kesz', 'elbukott'):
        return 'nincs', '', '', ''
    return allapot, ido, uzenet, napló


def szinkron_dontes(forras_db, cel_db):
    """(döntés, forrás_ts, cél_ts). A kulcs a `meta.epites_ts`, NEM a fájl mtime-ja (a másolás az mtime-ot átírja: M0 felmérés 3.)."""
    f = db_epites_ts(forras_db)
    c = db_epites_ts(cel_db)
    if not f:
        return 'nincs_forras', f, c
    return ('azonos' if f == c else 'masol'), f, c


# -- git (pusztán fájlolvasással) --------------------------------------------------------------------------------------------
_WIN_UT = re.compile(r'^([A-Za-z]):[\\/](.*)$')


def _posix_ut(ut):
    """`C:/Users/x` -> `/mnt/c/Users/x`, ha az eredeti nem létezik, de a /mnt/c-s alak igen (WSL); egyébként változatlan."""
    ut = ut.strip()
    if os.path.exists(ut):
        return ut
    m = _WIN_UT.match(ut)
    if m:
        alt = '/mnt/%s/%s' % (m.group(1).lower(), m.group(2).replace('\\', '/'))
        if os.path.exists(alt):
            return alt
    return ut


def _olvas(ut):
    try:
        with open(ut, encoding='utf-8') as f:
            return f.read().strip()
    except OSError:
        return None


def _git_konyvtar(kezdo):
    """A `.git` könyvtár (a worktree esetén a worktree saját gitdir-je) és a közös könyvtár; None, ha nincs."""
    d = os.path.abspath(kezdo)
    while True:
        g = os.path.join(d, '.git')
        if os.path.isdir(g):
            return g, g
        if os.path.isfile(g):
            sor = _olvas(g) or ''
            if sor.startswith('gitdir:'):
                gd = _posix_ut(sor[len('gitdir:'):].strip())
                kozos = gd
                cd = _olvas(os.path.join(gd, 'commondir'))
                if cd:
                    kozos = os.path.normpath(os.path.join(gd, cd))
                return gd, kozos
            return None
        szulo = os.path.dirname(d)
        if szulo == d:
            return None
        d = szulo


def _ref_hash(ref, gd, kozos):
    for alap in (gd, kozos):
        h = _olvas(os.path.join(alap, *ref.split('/')))
        if h:
            return h
    csomag = _olvas(os.path.join(kozos, 'packed-refs')) or ''
    for sor in csomag.splitlines():
        if sor and sor[0] not in '#^':
            reszek = sor.split(' ', 1)
            if len(reszek) == 2 and reszek[1].strip() == ref:
                return reszek[0]
    return None


def _git_teljes(kezdo):
    """(ág, teljes hash vagy None, gd, kozos); None, ha nincs git-könyvtár. Detached HEAD: ág = `(detached)`."""
    keres = _git_konyvtar(kezdo)
    if not keres:
        return None
    gd, kozos = keres
    head = _olvas(os.path.join(gd, 'HEAD'))
    if not head:
        return None
    if head.startswith('ref:'):
        ref = head[4:].strip()
        ag = ref[len('refs/heads/'):] if ref.startswith('refs/heads/') else ref
        return ag, _ref_hash(ref, gd, kozos), gd, kozos
    return '(detached)', head, gd, kozos


def git_allapot(kezdo=SZERVER_DIR):
    """(ág, rövid commit). Detached HEAD: ág = `(detached)`. Ha nem olvasható: (ISMERETLEN, ISMERETLEN)."""
    t = _git_teljes(kezdo)
    if not t:
        return ISMERETLEN, ISMERETLEN
    ag, h, _, _ = t
    return ag, (h[:8] if h else ISMERETLEN)


def checkout_szerep(kezdo=SZERVER_DIR):
    """(`fo` | `elonezet`, a főcheckout gyökere, a munkafa gyökere); None, ha nincs git-könyvtár. `elonezet`: linkelt worktree (a `.git` egy fájl,
    a gitdir és a közös könyvtár eltér); a főcheckout gyökere a közös `.git` könyvtár szülője."""
    keres = _git_konyvtar(kezdo)
    if not keres:
        return None
    gd, kozos = keres
    fo = os.path.dirname(kozos) if os.path.basename(kozos) == '.git' else kozos
    d = os.path.abspath(kezdo)
    while d and not os.path.exists(os.path.join(d, '.git')):
        szulo = os.path.dirname(d)
        if szulo == d:
            break
        d = szulo
    return ('fo' if os.path.normpath(gd) == os.path.normpath(kozos) else 'elonezet'), fo, d


# -- lemaradás az origin/main mögött (F225) ------------------------------------------------------------------------------------
FO_REF = 'refs/remotes/origin/main'
_SZAMOL = object()                                       # a háttérszál még számolja
_LEMARADAS_TAR = {}                                      # (gd, head, origin/main) -> int | None
_LEMARADAS_ZAR = threading.Lock()


def _commit_szam(gd, head, fo):
    """`git rev-list --count <head>..<fo>` a feloldott `--git-dir`-rel (a worktree `.git` fájlját a WSL-git nem oldaná fel); None, ha nem fut."""
    git = shutil.which('git')
    if not git:
        return None
    try:
        p = subprocess.run([git, '--git-dir=' + gd, '-c', 'safe.directory=*', 'rev-list', '--count', '%s..%s' % (head, fo)],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=60,
                           env=dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0'))
    except (OSError, subprocess.SubprocessError):
        return None
    return int(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip().isdigit() else None


def _tarol(kulcs, ertek):
    with _LEMARADAS_ZAR:
        _LEMARADAS_TAR[kulcs] = ertek
        for k in [k for k in _LEMARADAS_TAR if k != kulcs and _LEMARADAS_TAR[k] is not _SZAMOL][:-8]:
            del _LEMARADAS_TAR[k]                        # csak az utolsó néhány ref-állapot marad


def lemaradas(kezdo=SZERVER_DIR, szinkron=False):
    """Hány committal áll a HEAD az `origin/main` mögött (a legutóbbi fetch szerint); None, ha nem állapítható meg (nincs git, nincs `origin/main`,
    a git nem fut) vagy a háttérszál még számolja. A két ref hash-ét fájlolvasás adja (olcsó, 3 mp-enként is); a commitok számolása csak a hash-ek
    változásakor fut, háttérszálon, hogy a lap kiszolgálását ne tartsa fel (`szinkron=True`: helyben, a tesztekhez és a parancssorhoz)."""
    t = _git_teljes(kezdo)
    if not t or not t[1]:
        return None
    _, head, gd, kozos = t
    fo = _ref_hash(FO_REF, gd, kozos)
    if not fo:
        return None
    if head == fo:
        return 0
    kulcs = (gd, head, fo)
    if szinkron:
        ertek = _commit_szam(gd, head, fo)
        _tarol(kulcs, ertek)
        return ertek
    with _LEMARADAS_ZAR:
        van = _LEMARADAS_TAR.get(kulcs, False)
        if van is False:
            _LEMARADAS_TAR[kulcs] = _SZAMOL
    if van is False:
        def _szal():
            _tarol(kulcs, _commit_szam(gd, head, fo))
        threading.Thread(target=_szal, daemon=True).start()
        return None
    return None if van is _SZAMOL else van


# -- a lábléc ---------------------------------------------------------------------------------------------------------------
class Lablec:
    """A lap láblécének indítási állapota (folyamatonként egyszer számolva). `figyelmeztetesek`: magyar mondatok listája."""

    def __init__(self, kiadas, ag, commit, epites_ts, forras_ts='', figyelmeztetesek=None, lemaradas=None, adat=None, epites=None):
        self.adat = adat                                 # #101: (allapot, valtozasok) az adat frissességéről (None: nem ismert / nem ellenőrzött)
        self.epites = epites                             # #101: a háttér-újraépítés állapota (allapot, idő, üzenet, napló) vagy None
        self.lemaradas = lemaradas                       # F225: a HEAD committal mögötte az origin/main-nek (None: nem ismert)
        self.kiadas = kiadas
        self.ag = ag
        self.commit = commit
        self.epites_ts = epites_ts
        self.forras_ts = forras_ts
        self.figyelmeztetesek = list(figyelmeztetesek or [])

    @classmethod
    def keszit(cls, kiadas, epites_ts, kezdo=SZERVER_DIR, kornyezet=None):
        """`kornyezet` (alap: os.environ): `PARDES_FORRAS_DB` = a Windows-oldali (forrás) pardes.db útja — ha adott, a lábléc összeveti az
        építési idejét a futóéval; `PARDES_AG` / `PARDES_COMMIT` / `PARDES_LEMARADAS` felülírja a git-olvasást (tesztek, külső indító)."""
        env = os.environ if kornyezet is None else kornyezet
        ag, commit = git_allapot(kezdo)
        ag = env.get('PARDES_AG') or ag
        commit = env.get('PARDES_COMMIT') or commit
        forras_ts = db_epites_ts(env.get('PARDES_FORRAS_DB', '')) if env.get('PARDES_FORRAS_DB') else ''
        gyoker = env.get('PARDES_FORRAS_GYOKER')         # #101: a forrásfájlok gyökere; üres: az adat frissességét nem ellenőrizzük (előnézet, teszt)
        adat = adat_allapot(gyoker, env.get('PARDES_DB'), ttl=0.0) if gyoker and env.get('PARDES_DB') else None
        epites = epites_allapot(env['PARDES_EPITES_ALLAPOT']) if env.get('PARDES_EPITES_ALLAPOT') else None
        lem = env.get('PARDES_LEMARADAS')
        lem = int(lem) if lem is not None and lem.isdigit() else (None if lem is not None else lemaradas(kezdo))
        return cls(kiadas, ag, commit, epites_ts, forras_ts, figyelmeztetesek(ag, epites_ts, forras_ts, lem, adat, epites), lem, adat, epites)

    def szotar(self):
        return {'kiadas': self.kiadas, 'ag': self.ag, 'commit': self.commit, 'epites_ts': self.epites_ts, 'forras_ts': self.forras_ts,
                'lemaradas': self.lemaradas, 'figyelmeztetesek': self.figyelmeztetesek}

    def kulcs(self):
        """A gyorsítótár-kulcs része: a lábléc tartalma. Ha az ág, a commit vagy a figyelmeztetés változik, a kész lapok nem használhatók tovább."""
        return (self.ag, self.commit, self.epites_ts, self.forras_ts, self.lemaradas, tuple(self.figyelmeztetesek))   # az adat/építés a figyelmeztetésekben benne van


class LablecFigyelo:
    """Élő lábléc: a git-állapotot és a forrás-adatbázis építési idejét `ttl` másodpercenként újraolvassa (néhány kis fájlolvasás), így az ágváltás
    vagy a Windows-oldali adatbázis újraépítése újraindítás nélkül is látszik. A futó adatbázis `epites_ts`-e a folyamat élettartamára rögzített."""

    def __init__(self, kiadas, epites_ts, kezdo=SZERVER_DIR, kornyezet=None, ttl=3.0):
        self._args = (kiadas, epites_ts, kezdo, kornyezet)
        self.ttl = ttl
        self._zar = threading.Lock()
        self._t = None
        self._lablec = None

    def kap(self):
        with self._zar:
            most = time.monotonic()
            if self._lablec is None or most - self._t >= self.ttl:
                self._lablec = Lablec.keszit(*self._args)
                self._t = most
            return self._lablec


def adat_figyelmeztetesek(adat, epites):
    """#101: az adatbázis régebbi az adatnál / az újraépítés folyamatban van / elbukott. `adat`: `adat_allapot` értéke; `epites`: `epites_allapot` értéke."""
    ki = []
    if epites and epites[0] == 'fut':
        ki.append('Az adatbázis újraépítése folyamatban (kezdete: %s); kész után a parancsikon újraindításával az új adat látszik.' % (epites[1] or 'ismeretlen'))
    elif epites and epites[0] == 'elbukott':
        ki.append('Az adatbázis újraépítése elbukott (%s): %s%s' % (epites[1] or 'ismeretlen időpont', epites[2] or 'ismeretlen ok',
                                                                    '; napló: %s' % epites[3] if epites[3] else ''))
    if adat and adat[0] == 'regebbi':
        valt = adat[1]
        ki.append('Az adatbázis régebbi az adatnál (%d változott forrásfájl, pl.: %s): a parancsikon újraindítása újraépíti.' % (len(valt), '; '.join(valt[:3])))
    elif adat and adat[0] == 'nincs_adat':
        ki.append('Az adatbázis régi építésű (nincs forrás-azonosító a meta táblában): az adat frissessége nem ellenőrizhető; a parancsikon újraindítása újraépíti.')
    return ki


def figyelmeztetesek(ag, epites_ts, forras_ts='', lemaradas=None, adat=None, epites=None):
    """A lábléc figyelmeztetései. Az ág `main`-től eltérése, az adatbázis-másolat elavultsága (a forrás építési ideje újabb) és a lemaradás az
    `origin/main` mögött (F225; csak ha ismert és pozitív)."""
    ki = []
    if ag != FO_AG:
        if ag == ISMERETLEN:
            ki.append('Az ág nem állapítható meg.')
        else:
            ki.append('A szerver nem a main ágon áll (ág: %s): nem a lezárt, összefésült kódot futtatja.' % ag)
    if forras_ts and epites_ts and forras_ts > epites_ts:
        ki.append('Az adatbázis-másolat régebbi a Windows-oldalinál (%s < %s): indítsd újra a parancsikonnal.' % (epites_ts, forras_ts))
    elif forras_ts and epites_ts and forras_ts != epites_ts:
        ki.append('Az adatbázis-másolat építési ideje eltér a Windows-oldalitól (%s ≠ %s).' % (epites_ts, forras_ts))
    ki += adat_figyelmeztetesek(adat, epites)
    if lemaradas:
        if ag == FO_AG:
            ki.append('A futó checkout %d committal az origin/main mögött áll (az utolsó fetch szerint): a main legújabb változásai még nem látszanak; '
                      'a belso parancsikon újraindításakor az indító frissíti a főcheckoutot (tiszta munkafánál).' % lemaradas)
        else:
            ki.append('Az ág %d committal az origin/main mögött áll (az utolsó fetch szerint).' % lemaradas)
    return ki


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) == 3 and a[0] == 'dontes':
        d, f, c = szinkron_dontes(a[1], a[2])
        print('%s\t%s\t%s' % (d, f, c))
        return 0
    if a and a[0] == 'git' and len(a) <= 2:
        ag, commit = git_allapot(a[1] if len(a) == 2 else SZERVER_DIR)
        print('%s\t%s' % (ag, commit))
        return 0
    if a and a[0] == 'lemaradas' and len(a) <= 2:
        n = lemaradas(a[1] if len(a) == 2 else SZERVER_DIR, szinkron=True)
        print('' if n is None else n)
        return 0
    if a and a[0] == 'checkout' and len(a) <= 2:
        r = checkout_szerep(a[1] if len(a) == 2 else SZERVER_DIR)
        print('\t'.join(r) if r else 'ismeretlen\t\t')
        return 0
    if len(a) == 3 and a[0] == 'forras':
        allapot, valt = forras_allapot(a[1], a[2])
        print('%s\t%d\t%s' % (allapot, len(valt), '; '.join(valt[:3])))
        return 0
    if len(a) == 2 and a[0] == 'db_ellenoriz':
        print(db_ellenoriz(a[1]))
        return 0
    if len(a) == 2 and a[0] == 'epites_allapot':
        print('\t'.join(epites_allapot(a[1])))
        return 0
    if len(a) == 2 and a[0] == 'epites_ts':
        print(db_epites_ts(a[1]))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
