"""lapgen.bemenet.jelolt — a szegmentált idézet: a szótári szöveg és a generátor jelölései külön darabokban (S3b).

A 4.2 kártyájának szövege idézet (a BDB vagy a Thayer magyar fordítása), és benne a generátor jelölése áll: a motívum
helyének kiemelése, a rövidítés feloldása, a héber futam utáni irányjel, a Károli-számozás, a kiejtés. A régi
generátor ezeket szövegcserével szúrta be. Itt a szöveg darabok sora: idézet-darab (a forrás betűi, a forrás nevével) és
jelölés-darab (`Jeloles`: fajta és típusos adat, szabad szöveg nélkül). A jelölés látható alakja a megjelenítőben, a
sablontáblából készül; a festékpróba így a két fajtát külön látja.

A jelölések helyét a régi generátor szabályai adják, amelyek a teljes szövegen futó mintákkal dolgoznak (a minta a
korábban beszúrt jelöléseken át is lát). Ezért a `Jelolt` szövegként is olvasható (`szoveg()`): a jelölés-darab itt a
mintáknak egyenértékű belső alakkal áll (`belso`), amely a lapra soha nem kerül. A műveletek (beszúrás, burkolás,
forrásjavítás, törlés) pozícióra hatnak; jelölés belsejébe nem nyúlhatnak (kimondott hiba).

A forrásjavítás (átírás, betűsorrend, a digitalizálás jelei) a forrás betűit cseréli: a javított szöveg ugyanannak a
forrásnak az idézete, a javítótábla sora szerint (a modul ezt nem dönti el, csak végrehajtja).
"""
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import FeloldasFajta, JelFajta  # noqa: F401 (a modul nevei között is)


class Feloldas:
    """A rövidítés feloldásának fajtája és a címszó (`Szo`: alak és kiejtés, vagy None)."""
    __slots__ = ('fajta', 'cimszo')

    def __init__(self, fajta, cimszo=None):
        self.fajta, self.cimszo = fajta, cimszo


class Jeloles:
    """Egy jelölés-darab: fajta, típusos adat és a belső (mintaillesztési) alak."""
    __slots__ = ('fajta', 'adat', 'belso')

    def __init__(self, fajta, adat, belso):
        self.fajta, self.adat, self.belso = fajta, adat, belso

    def __repr__(self):
        return 'Jeloles(%s)' % self.fajta.value


class JeloltHiba(BemenetHiba):
    """A művelet jelölés belsejébe nyúlna, vagy idézet-darabot jelölésen át cserélne."""


class Jelolt:
    """Szegmentált idézet: [(None, szöveg)] idézet-darab vagy [(Jeloles, belső alak)]. A `forras` a B-azonosító, a
    `mezo` és a `hely` az idézet helye: a darabok ebből kapják a burkolójukat (`darabok`)."""

    def __init__(self, szoveg, forras, mezo, hely):
        self._d = [[None, szoveg]] if szoveg else []
        self.forras, self.mezo, self.hely = forras, mezo, hely

    # --- olvasás ---------------------------------------------------------------------------------------------
    def szoveg(self):
        """A teljes szöveg a jelölések belső alakjával (a mintaillesztéshez; a lapra nem kerül)."""
        return ''.join(d[1] for d in self._d)

    def __bool__(self):
        return bool(self._d)

    def idezet_szoveg(self):
        """Csak az idézet-darabok szövege (összevetéshez, kapuhoz)."""
        return ''.join(d[1] for d in self._d if d[0] is None)

    def darabok(self, b):
        """A darabok a megjelenítőnek: Forrasszoveg (idézet) vagy Jeloles."""
        return tuple(b.forrasszoveg(self.forras, self.mezo, d[1], self.hely) if d[0] is None else d[0]
                     for d in self._d)

    def jelolesek(self):
        return [d[0] for d in self._d if d[0] is not None]

    # --- a pozíciók -----------------------------------------------------------------------------------------
    def _hol(self, poz, beszuras=True):
        """(darab indexe, eltolás a darabon belül) a szöveg pozíciójához. Beszúrásnál a darabhatár megengedett
        (a jelölés előtt vagy után), a jelölés belseje nem."""
        kezd = 0
        for i, (jel, sz) in enumerate(self._d):
            veg = kezd + len(sz)
            if poz == kezd:
                return i, 0
            if kezd < poz < veg:
                if jel is not None:
                    raise JeloltHiba('a pozíció (%d) jelölés belsejébe esik (%s)' % (poz, jel.fajta.value))
                return i, poz - kezd
            kezd = veg
        if poz == kezd:
            return len(self._d), 0
        raise JeloltHiba('a pozíció (%d) a szövegen kívül esik' % poz)

    def _vag(self, poz):
        """Darabhatár a pozíción; visszaad: a határ utáni darab indexe."""
        i, off = self._hol(poz)
        if off:
            jel, sz = self._d[i]
            self._d[i:i + 1] = [[None, sz[:off]], [None, sz[off:]]]
            return i + 1
        return i

    # --- műveletek (mind pozíció szerint, a hívó a jobbról balra haladó sorrendet tartja) ------------------------
    def beszur(self, poz, jeloles):
        i = self._vag(poz)
        self._d.insert(i, [jeloles, jeloles.belso])

    def burkol(self, kezd, veg, nyito, zaro):
        """Az idézet [kezd, veg) része a két jelölés közé kerül."""
        self.beszur(veg, zaro)
        self.beszur(kezd, nyito)

    def _idezet_tartomany(self, kezd, veg):
        """A [kezd, veg) tartomány darabjai; mind idézet kell legyen."""
        i = self._vag(kezd)
        j = self._vag(veg) if veg > kezd else i
        for d in self._d[i:j]:
            if d[0] is not None:
                raise JeloltHiba('a forrásjavítás jelölésen át nyúlna (%s)' % d[0].fajta.value)
        return i, j

    def javit(self, kezd, veg, uj):
        """Forrásjavítás: az idézet [kezd, veg) része helyett `uj` (ugyanannak a forrásnak a javított alakja)."""
        i, j = self._idezet_tartomany(kezd, veg)
        self._d[i:j] = [[None, uj]] if uj else []
        self._osszevon()

    def cserel_jelolesre(self, kezd, veg, jeloles):
        """Az idézet [kezd, veg) része helyett jelölés áll (a Károli-számozás: a szám a jelölés adata)."""
        i, j = self._idezet_tartomany(kezd, veg)
        self._d[i:j] = [[jeloles, jeloles.belso]]

    def futamonkent(self, f):
        """Forrásjavítás idézet-futamonként (a futam a jelölések közti idézet-darab)."""
        for d in self._d:
            if d[0] is None:
                d[1] = f(d[1])
        self._osszevon()

    def torol_lrm_is(self, kezd, veg):
        """Az idézet [kezd, veg) része törlődik; a benne álló irányjel-jelölés is (a régi lánc a forrás belső
        számlálóját az előtte álló irányjellel együtt törölte)."""
        i = self._vag(kezd)
        j = self._vag(veg) if veg > kezd else i
        for d in self._d[i:j]:
            if d[0] is not None and d[0].fajta is not JelFajta.LRM:
                raise JeloltHiba('a törlés jelölésen át nyúlna (%s)' % d[0].fajta.value)
        del self._d[i:j]
        self._osszevon()

    def _osszevon(self):
        ki = []
        for d in self._d:
            if not d[1] and d[0] is None:
                continue
            if ki and d[0] is None and ki[-1][0] is None:
                ki[-1][1] += d[1]
            else:
                ki.append(d)
        self._d = ki

    def masolat(self):
        uj = Jelolt('', self.forras, self.mezo, self.hely)
        uj._d = [list(d) for d in self._d]
        return uj


def cserek(jelolt, talalatok):
    """Forrásjavítások alkalmazása: [(kezdet, vég, új szöveg)] a jelenlegi szövegen, jobbról balra."""
    for kezd, veg, uj in sorted(talalatok, key=lambda t: t[0], reverse=True):
        jelolt.javit(kezd, veg, uj)
