"""lapgen.bemenet.jovahagyas — a szerzői jóváhagyás frissessége kiadás módban (GK-27, T9; N221, DT933 (1)).

A szerző jóváhagyása a lap egy változatára szól (`adat/lap_atnezesek.tsv`, SEMA 2.48: `lap_commit`), és tartalmilag
a kézi prózára és a motívum adatára (DT933 (1)). A frissesség három esete:

- **friss** — a legutóbbi érvényes átnézés `lap_commit`-ja a lap (`lexikon/<ID>_TUDOMANYOS.md`) mai utolsó commitja;
- **csak generált változás** — a lap azóta változott, de a jóváhagyás tárgya nem: a motívum kézi bemeneteinek
  lenyomata (`konfig.JOVAHAGYAS_BEMENETEK`: a kézi forrás egésze és az adattáblák motívumsorai) a jóváhagyott
  commitban és ma azonos. Ez új nézést nem kér, csak változásjegyzék-sort (a kiadás sora, `kiadasok.tsv`; a
  kiadott lap új kiadás nélküli változását az E28 őrzi);
- **elavult** — a kézi próza vagy a motívum adata a jóváhagyott változat óta változott: új nézés kell.

Érvényes átnézés-sor (SEMA 2.48): `ki` = `felhasználó`, nem üres `idezet`, és a `lap_commit` őse a mai HEAD-nek; több
ilyen sor közül a legutóbbi (dátum, azonos napon a táblabeli sorrend szerint).

A git-olvasás és a lenyomat nem tartalmi olvasás: nem kerül az olvasási naplóba (a frissességi kapuk mintájára,
`bemenet/frissesseg.py`). Csak kiadás módban fut; munka módban a mondat a korábbi változatot mondja, git nélkül.
"""
import enum
import hashlib
import subprocess

from lapgen import konfig
from lapgen.bemenet.jegyzek import ID_HELYORZO, BemenetHiba

_ATNEZES_OSZLOPOK = ('id', 'lap_commit', 'datum', 'ki', 'idezet')
_COMMIT_MIN = 7


class Frissesseg(enum.Enum):
    FRISS = 'friss'
    CSAK_GENERALT = 'csak_generalt'
    ELAVULT = 'elavult'
    NINCS_ATNEZES = 'nincs_atnezes'   # nincs érvényes szerzői átnézés-sor (vagy egyik sem őse a HEAD-nek)
    NINCS_LAP = 'nincs_lap'           # a lap nincs a repóban (nincs utolsó commitja)


class Jovahagyas:
    """A frissesség eredménye: az állapot, az összevetett átnézés commitja és dátuma, a lap mai utolsó commitja."""
    __slots__ = ('allapot', 'atnezes_commit', 'atnezes_datum', 'lap_commit')

    def __init__(self, allapot, atnezes_commit=None, atnezes_datum=None, lap_commit=None):
        self.allapot, self.atnezes_commit = allapot, atnezes_commit
        self.atnezes_datum, self.lap_commit = atnezes_datum, lap_commit

    @property
    def kiadhato(self):
        return self.allapot in (Frissesseg.FRISS, Frissesseg.CSAK_GENERALT)


def lap_utvonal(motivum):
    return '%s/%s_%s.md' % (konfig.CEL_NEV, motivum.kod, konfig.NEZET_TUDOMANYOS)


class Git:
    """A repó git-olvasása (csak olvas). A teszt hamis olvasót adhat helyette (ugyanezzel a négy metódussal)."""

    def __init__(self, gyoker):
        self.gyoker = gyoker

    def _git(self, *args):
        try:
            return subprocess.run(('git', '-C', self.gyoker) + args, capture_output=True, check=False)
        except OSError as e:
            raise BemenetHiba('GK-27: a git nem futtatható (%s): a jóváhagyás frissessége nem mérhető' % e) from None

    def utolso_commit(self, utvonal):
        r = self._git('log', '-1', '--format=%H', '--', utvonal)
        if r.returncode != 0:
            raise BemenetHiba('GK-27: git log hiba (%s): %s' % (utvonal, r.stderr.decode('utf-8', 'replace').strip()))
        return r.stdout.decode('ascii').strip() or None

    def teljes(self, commit):
        """A commit teljes hash-e; None, ha nincs ilyen commit."""
        r = self._git('rev-parse', '--verify', '--quiet', commit + '^{commit}')
        return r.stdout.decode('ascii').strip() if r.returncode == 0 else None

    def ose_a_headnek(self, commit):
        return self._git('merge-base', '--is-ancestor', commit, 'HEAD').returncode == 0

    def tartalom(self, commit, utvonal):
        """A fájl sorvég-normalizált szövege a commitban; None, ha a fájl ott nem állt."""
        r = self._git('show', '%s:%s' % (commit, utvonal))
        if r.returncode != 0:
            return None
        return r.stdout.replace(b'\r\n', b'\n').decode('utf-8')


def _motivum_resz(utvonal, szoveg, kod):
    """A fájl motívumra eső része: az `<ID>`-s útvonalnál (a motívum saját fájlja) az egész; táblánál a fejléc (az első
    nem `#` sor) és azok a sorok, amelyeknek valamely cellája pontosan a motívum azonosítója."""
    if szoveg is None:
        return '\x00nincs'
    if ID_HELYORZO in utvonal:
        return szoveg
    sorok = [s for s in szoveg.split('\n') if s.strip() and not s.startswith('#')]
    if not sorok:
        return ''
    return '\n'.join([sorok[0]] + [s for s in sorok[1:] if kod in s.split('\t')])


def lenyomat(b, motivum, olvas):
    """A motívum kézi bemeneteinek lenyomata (sha256): `olvas(útvonal)` a fájl szövege (None, ha nincs). A bemenetek
    a `konfig.JOVAHAGYAS_BEMENETEK` jegyzéksorai; az útvonal-minta `<ID>`-je a motívum."""
    h = hashlib.sha256()
    for b_id in konfig.JOVAHAGYAS_BEMENETEK:
        for minta in (u.strip() for u in b.jegyzek_sor(b_id).utvonal.split(';')):
            if '*' in minta:
                raise BemenetHiba('GK-27: a jóváhagyás bemenete nem lehet glob (%s: %s)' % (b_id, minta))
            utvonal = minta.replace(ID_HELYORZO, motivum.kod)
            resz = _motivum_resz(minta, olvas(utvonal), motivum.kod)
            h.update(('%s\t%s\t%s\n' % (b_id, utvonal, hashlib.sha256(resz.encode('utf-8')).hexdigest()))
                     .encode('utf-8'))
    return h.hexdigest()


def _munkafa_olvaso(b):
    def olvas(utvonal):
        try:
            return b._fajl(utvonal, tarol=False)[0]
        except BemenetHiba:
            return None
    return olvas


def _atnezesek(b, motivum):
    """A motívum érvényes szerzői átnézés-sorai (lap_commit, dátum szöveg, sorszám) a táblabeli sorrendben."""
    _kiadas_ut, atnezes_ut, _javitas_ut = b._utvonalak('B48')
    ki = []
    for i, sor in enumerate(b._tabla('B48', utvonal=atnezes_ut, oszlopok=_ATNEZES_OSZLOPOK).szotarak()):
        commit = sor['lap_commit'].strip()
        if (sor['id'] == motivum.kod and sor['ki'] == konfig.SZERZO_ATNEZES and sor['idezet'].strip()
                and len(commit) >= _COMMIT_MIN):
            ki.append((commit, sor['datum'].strip(), i))
    return ki


def _datum_kulcs(datum):
    return datum.replace('-', '.')


def frissesseg(b, motivum, git=None):
    """GK-27 (T9): a szerzői jóváhagyás frissessége a lap mai állapotához (l. a modul leírását)."""
    git = git or Git(b.gyoker)
    lap = lap_utvonal(motivum)
    utolso = git.utolso_commit(lap)
    if utolso is None:
        return Jovahagyas(Frissesseg.NINCS_LAP)
    ervenyes = []
    for commit, datum, i in _atnezesek(b, motivum):
        teljes = git.teljes(commit)
        if teljes is not None and git.ose_a_headnek(teljes):
            ervenyes.append((teljes, datum, i))
    if not ervenyes:
        return Jovahagyas(Frissesseg.NINCS_ATNEZES, lap_commit=utolso)
    for teljes, datum, _i in ervenyes:
        if teljes == utolso:
            return Jovahagyas(Frissesseg.FRISS, teljes, datum, utolso)
    teljes, datum, _i = max(ervenyes, key=lambda e: (_datum_kulcs(e[1]), e[2]))
    akkor = lenyomat(b, motivum, lambda u: git.tartalom(teljes, u))
    ma = lenyomat(b, motivum, _munkafa_olvaso(b))
    allapot = Frissesseg.CSAK_GENERALT if akkor == ma else Frissesseg.ELAVULT
    return Jovahagyas(allapot, teljes, datum, utolso)
