"""Az olvasó-szerver indítási és lábléc-állapota (#100): ág, commit, adatbázis-építési idő, adatbázis-szinkron döntés.

Csak a szabványos könyvtárat használja (nem függ a Flasktól), és NEM hív `git`-et: a worktree-k `.git` fájlja Windows-útra mutat
(`gitdir: C:/…`), amit a WSL-beli `git` nem old fel; ezért a `HEAD`-et és a ref-eket maga olvassa (és a Windows-utat `/mnt/c/…`-re
fordítja, ha kell).

Parancssor (az `indit.sh` hívja):
    python allapot.py dontes <forras.db> <cel.db>    # kiírja: <döntés>\\t<forrás epites_ts>\\t<cél epites_ts>
    python allapot.py git [<könyvtár>]               # kiírja: <ág>\\t<rövid commit>
    python allapot.py epites_ts <db>                 # kiírja: a meta.epites_ts-t (üres, ha nincs)
Döntések: `masol` (a forrás építési ideje eltér vagy a cél hiányzik/olvashatatlan), `azonos` (nincs másolás), `nincs_forras`
(a forrás hiányzik vagy nincs epites_ts: nem másolunk, a meglévő célt hagyjuk).
"""
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SZERVER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SZERVER_DIR)
import lekerdezesek                                  # noqa: E402  (stdlib-only modul; parancssori hívásnál a saját könyvtár nincs mindig a sys.path-on)
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


def git_allapot(kezdo=SZERVER_DIR):
    """(ág, rövid commit). Detached HEAD: ág = `(detached)`. Ha nem olvasható: (ISMERETLEN, ISMERETLEN)."""
    keres = _git_konyvtar(kezdo)
    if not keres:
        return ISMERETLEN, ISMERETLEN
    gd, kozos = keres
    head = _olvas(os.path.join(gd, 'HEAD'))
    if not head:
        return ISMERETLEN, ISMERETLEN
    if head.startswith('ref:'):
        ref = head[4:].strip()
        ag = ref[len('refs/heads/'):] if ref.startswith('refs/heads/') else ref
        h = _ref_hash(ref, gd, kozos)
        return ag, (h[:8] if h else ISMERETLEN)
    return '(detached)', head[:8]


# -- a lábléc ---------------------------------------------------------------------------------------------------------------
class Lablec:
    """A lap láblécének indítási állapota (folyamatonként egyszer számolva). `figyelmeztetesek`: magyar mondatok listája."""

    def __init__(self, kiadas, ag, commit, epites_ts, forras_ts='', figyelmeztetesek=None):
        self.kiadas = kiadas
        self.ag = ag
        self.commit = commit
        self.epites_ts = epites_ts
        self.forras_ts = forras_ts
        self.figyelmeztetesek = list(figyelmeztetesek or [])

    @classmethod
    def keszit(cls, kiadas, epites_ts, kezdo=SZERVER_DIR, kornyezet=None):
        """`kornyezet` (alap: os.environ): `PARDES_FORRAS_DB` = a Windows-oldali (forrás) pardes.db útja — ha adott, a lábléc összeveti az
        építési idejét a futóéval; `PARDES_AG` / `PARDES_COMMIT` felülírja a git-olvasást (tesztek, külső indító)."""
        env = os.environ if kornyezet is None else kornyezet
        ag, commit = git_allapot(kezdo)
        ag = env.get('PARDES_AG') or ag
        commit = env.get('PARDES_COMMIT') or commit
        forras_ts = db_epites_ts(env.get('PARDES_FORRAS_DB', '')) if env.get('PARDES_FORRAS_DB') else ''
        return cls(kiadas, ag, commit, epites_ts, forras_ts, figyelmeztetesek(ag, epites_ts, forras_ts))

    def szotar(self):
        return {'kiadas': self.kiadas, 'ag': self.ag, 'commit': self.commit, 'epites_ts': self.epites_ts, 'forras_ts': self.forras_ts,
                'figyelmeztetesek': self.figyelmeztetesek}


def figyelmeztetesek(ag, epites_ts, forras_ts=''):
    """A lábléc figyelmeztetései. Az ág `main`-től eltérése és az adatbázis-másolat elavultsága (a forrás építési ideje újabb)."""
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
    if len(a) == 2 and a[0] == 'epites_ts':
        print(db_epites_ts(a[1]))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
