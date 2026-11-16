"""lapgen.szamitas.lxx — az „5. LXX-fordítói döntések” szakasz lapmodellje és a 4.6 (LXX-híd) számai (S4).

A motívum ószövetségi helyeit versenként veti össze a Septuagintával (a régi `lxx_osszevetes`,
`_lxx_ujraminosit`, `lxx_egyforras_ellenoriz`). Egy vers ítélete:

- **egyező**: a versben a motívum egy görög szava áll (a héber kulcsszó 4.11 szerinti saját párjára szűrve);
- különben a megjelenő fordítói döntés sora (hídszóra váltott versben csak a hídszóé): **eltérő** (LXX-minuszt
  **LXX-minusz**, ha a döntés szerint a szó a görögből hiányzik);
- különben a 4.11 ellenőrzött társítása: **eltérő**, „(társítás)” jellel;
- különben **a megfelelő nincs megállapítva**; a vers nélküli LXX-szöveg: **versszámozás miatt nem párosítva**.

Az újraminősítés: az eltérő ítélet **nincs újszövetségi pár**, ha a sor egyik héber szavának sincs a motívumban
újszövetségi párja (a kétnyelvű szótár és a szócsalád szerint), és **ugyanaz a szócsalád**, ha a görög megfelelő a
motívum egy görög szavának szócsaládjába tartozik. A szakasz táblája, összesítése és a 4.6 szavankénti mondata
ugyanebből az ítéletsorból számol (egy mérce).

A hídszó (F212 Sz3): ha a sor szavai között nincs újszövetségi párral bíró szó, de a versben áll ilyen, a vers
kulcsszava az lesz.
"""
import dataclasses
import enum
from dataclasses import replace as _felulir
import re
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import elofordulas as elofordulas_be
from lapgen.bemenet import lxx as lxx_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.szamitas.szotari_tipusok import Szo
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, Lathato, Proveniencia, Strong, idezet

_GOROG_SZO_RX = re.compile('[Ͱ-Ͽἀ-῿]+')


class Itelet(enum.Enum):
    EGYEZO = 'egyezo'
    SZOCSALAD = 'szocsalad'
    ELTERO = 'eltero'
    NINCS_PAR = 'nincs_par'
    MINUSZ = 'minusz'
    FUGGOBEN = 'fuggoben'
    SZAMOZAS = 'szamozas'


class GorogFajta(enum.Enum):
    SZOVEG = 'szoveg'          # a Septuaginta szövegének szava (alak, lemma, Strong)
    DONTES = 'dontes'          # a fordítói döntés lemmája
    TARSITAS = 'tarsitas'      # a 4.11 ellenőrzött társítása
    MINUSZ = 'minusz'          # a fordítói döntés szerint a görögből hiányzik
    NINCS = 'nincs'


@dataclasses.dataclass(frozen=True)
class Kulcsszo:
    """A héber kulcsszó írása és kiejtése (idézetek); a kiejtés None: kimondott hiány."""
    alak: Lathato
    kiejtes: Optional[Lathato] = None


@dataclasses.dataclass(frozen=True)
class Gorog:
    """A görög megfelelő. `alak` csak a Septuaginta szövegének szavánál; `alak_kiejtes` a szakaszban először álló
    alak kiejtés-pótlása (a régi kész lap szabálya), egyébként None. `strong` és `glossza` a szónézet-hivatkozáshoz."""
    fajta: GorogFajta
    alak: Optional[Lathato] = None
    alak_kiejtes: Optional[Lathato] = None
    lemma: Optional[Lathato] = None
    kiejtes: Optional[Lathato] = None
    strong: Optional[Strong] = None
    glossza: Optional[Lathato] = None


@dataclasses.dataclass(frozen=True)
class LxxHely:
    """A vers LXX-igehelye: a fejezet és a vers; `elter` igaz, ha a számozás eltér a Károliétól."""
    fej: int
    vers: int
    elter: bool


@dataclasses.dataclass(frozen=True)
class LxxSor:
    vers: Igehely
    lxx: Optional[LxxHely]
    heber: Optional[Kulcsszo]
    gorog: Gorog
    itelet: Itelet


@dataclasses.dataclass(frozen=True)
class Szamlalo:
    egyezo: int = 0
    szocsalad: int = 0
    eltero: int = 0
    nincs_par: int = 0
    minusz: int = 0
    fuggoben: int = 0
    szamozas: int = 0

    def osszes(self):
        return sum(getattr(self, m.value) for m in Itelet)


@dataclasses.dataclass(frozen=True)
class SzoSzamlalo:
    strong: Strong
    szamlalo: Szamlalo


@dataclasses.dataclass(frozen=True)
class HidFok(enum.Enum):
    """A híd erőssége: a szócsaládos egyezés aránya a párral bíró versekben (`konfig.LXX_HID_*`)."""
    EROS = 'eros'
    RESZLEGES = 'reszleges'
    GYENGE = 'gyenge'


def hid_fok(szamlalo):
    """A híd erőssége a számlálóból (a régi `lxx_hid_jelzo`); None, ha a motívumnak nincs párral bíró verse."""
    par_n = szamlalo.egyezo + szamlalo.szocsalad + szamlalo.eltero
    if not par_n:
        return None
    arany = (szamlalo.egyezo + szamlalo.szocsalad) / par_n
    if arany >= konfig.LXX_HID_EROS:
        return HidFok.EROS
    return HidFok.RESZLEGES if arany >= konfig.LXX_HID_RESZLEGES else HidFok.GYENGE


@dataclasses.dataclass(frozen=True)
class Osszevetes:
    """Az 5. szakasz modellje és a 4.6 számai. `par_szavak`: a motívum újszövetségi párral bíró héber szavai;
    `fok`: a híd erőssége (None: nincs párral bíró vers)."""
    sorok: Tuple[LxxSor, ...]
    szamlalo: Szamlalo
    szavankent: Tuple[SzoSzamlalo, ...]
    par_szavak: Tuple[Strong, ...]
    gorog_szavak: Tuple[Strong, ...]
    par_nevek: Tuple[Szo, ...] = ()    # a párral bíró szavak szótári alakja (a mondatokhoz)
    fok: Optional[HidFok] = None


def _szamlalo(itelet_lista):
    db = {m: 0 for m in Itelet}
    for it in itelet_lista:
        db[it] += 1
    return Szamlalo(**{m.value: n for m, n in db.items()})


class _Szamito:
    def __init__(self, f):
        from lapgen.szamitas import szotari_sece
        self.f = f
        self.szeptuaginta = lxx_be.septuaginta(f.b)
        self.dontesek = lxx_be.dontes_sorok(f.b)
        self.tarsitas = lxx_be.lxx_tarsitasok(f.b, f.motivum)
        self.karoli = bemenet.b07_karoli(f.b)
        szavak = sorted({st for s in f.sorok for st in s.strongok}, key=lambda st: st.kod)
        self.gorog = tuple(st for st in szavak if not st.heber)
        self.sece = szotari_sece.szamolo(f, szavak)
        self.par = tuple(h for h in szavak if h.heber and self._van_par(h))
        self.latott = set()

    def _van_par(self, h):
        """A régi `lxx_par_tokenek`: a héber szó megfelelője (SECE) a motívum görög szava, vagy annak szócsaládja."""
        eq = self.sece.megfelelo_strongok(h)
        return any(x in self.gorog for x in eq) or any(self.sece.csalad(e, x) for e in eq for x in self.gorog)

    def heber_szo(self, vers, strong):
        sz = self.f.kiejtes.ragozott((vers,), strong, utolso=True)
        if sz is None:
            return None
        return Kulcsszo(idezet(sz.alak), idezet(sz.kiejtes) if sz.kiejtes is not None else None)

    def _kulcsszo_tokenek(self, sor_tokenek, vers):
        if not self.par or any(h in self.par for h in sor_tokenek):
            return sor_tokenek
        hid = [h for h in self.par if self.heber_szo(vers, h) is not None]
        return (hid[0],) if hid else sor_tokenek

    def _lxx_hely(self, vers, hely):
        if hely is None:
            raise KapuHiba('5.: a(z) %s LXX-igehelye nem fejezet:vers alakú' % vers.kod)
        return LxxHely(hely[0], hely[1], hely != (vers.fejezet, vers.vers))

    def _gorog_kiejtes(self, strong, lemma):
        if strong is not None:
            szotari = self.f.kiejtes.szotari(strong)
            if szotari is not None and szotari.kiejtes is not None:
                return idezet(szotari.kiejtes)
        gepi = self.f.kiejtes.gorog_gepi(lemma)
        return idezet(gepi) if gepi is not None else None

    def _glossza(self, strong):
        return _glossza_f(self.f, strong) if strong is not None else None

    def _potlas(self, strong, alak):
        """A szakaszban először álló Septuaginta-alak kiejtése (a régi kész lap kiejtés-pótlása)."""
        kulcs = alak.ertek
        if kulcs in self.latott:
            return None
        self.latott.add(kulcs)
        kiejtes = self.f.kiejtes.alak_kiejtes(strong, alak) if strong is not None else None
        if kiejtes is None:
            gepi = self.f.kiejtes.gorog_gepi(alak)
            return idezet(gepi) if gepi is not None else None
        return idezet(kiejtes)

    def _latott(self, lemma):
        self.latott.add(lemma.ertek)

    def vers_itelet(self, vers, sor_tokenek):
        """(heber_tokenek, LxxSor az újraminősítés előtt, a görög megfelelő nyers szövegei az összevetéshez)."""
        tokenek = self._kulcsszo_tokenek(sor_tokenek, vers)
        heber = next((h for h in (self.heber_szo(vers, t) for t in tokenek) if h is not None), None)
        szavak = self.szeptuaginta.szavak(vers)
        if szavak is None:
            raise KapuHiba('5.: a(z) %s könyvének nincs Septuaginta-fájlja az `lxx_os_import` könyvtérképe szerint '
                           '(lehetséges ok a könyvnév eltérő alakja: a térkép a Siralmak könyvét `Sir` alakban ismeri, a '
                           'normalizáló tábla `JSir` alakban); a „nincs Septuaginta-könyv” ág nincs portolva' % vers.kod)
        if not szavak:
            return tokenek, LxxSor(vers, None, heber, Gorog(GorogFajta.NINCS), Itelet.SZAMOZAS), ()
        lxx = self._lxx_hely(vers, szavak[0].lxx_hely)
        egyezo = [w for w in szavak if w.strong is not None and w.strong in self.gorog]
        if egyezo:
            sajat = {lxx_be.ekezet_nelkul(self.tarsitas[(vers.kod, t.kod)].lemma.ertek) for t in tokenek
                     if (vers.kod, t.kod) in self.tarsitas}
            if sajat:
                egyezo = [w for w in egyezo if lxx_be.ekezet_nelkul(w.lemma.ertek) in sajat]
        if egyezo:
            w = egyezo[0]
            lemma_kulcs = lxx_be.ekezet_nelkul(w.lemma.ertek)
            par = next((t for t in tokenek if (vers.kod, t.kod) in self.tarsitas
                        and lxx_be.ekezet_nelkul(self.tarsitas[(vers.kod, t.kod)].lemma.ertek) == lemma_kulcs), None)
            if par is not None and self.heber_szo(vers, par) is not None:
                heber = self.heber_szo(vers, par)
            gorog = Gorog(GorogFajta.SZOVEG, alak=idezet(w.alak), alak_kiejtes=self._potlas(w.strong, w.alak),
                          lemma=idezet(w.lemma), kiejtes=self._gorog_kiejtes(w.strong, w.lemma), strong=w.strong,
                          glossza=self._glossza(w.strong))
            self._latott(w.lemma)
            return tokenek, LxxSor(vers, lxx, heber, gorog, Itelet.EGYEZO), (w.alak.ertek, w.lemma.ertek)
        dontesek = self.dontesek.vershez(vers)
        if tokenek is not sor_tokenek:
            dontesek = tuple(d for d in dontesek if d.heber in tokenek)
        if dontesek:
            d = dontesek[0]
            if d.lxx_hely is not None:
                lxx = self._lxx_hely(vers, d.lxx_hely)
            if d.minusz:
                return tokenek, LxxSor(vers, lxx, heber, Gorog(GorogFajta.MINUSZ), Itelet.MINUSZ), ()
            if d.lemma is None:
                raise KapuHiba('5.: a(z) %s fordítói döntésének nincs görög lemmája' % vers.kod)
            self._latott(d.lemma)
            gorog = Gorog(GorogFajta.DONTES, lemma=idezet(d.lemma), kiejtes=self._gorog_kiejtes(d.gorog, d.lemma),
                          strong=d.gorog, glossza=self._glossza(d.gorog))
            return tokenek, LxxSor(vers, lxx, heber, gorog, Itelet.ELTERO), (d.lemma.ertek,)
        par = next(((t, self.tarsitas[(vers.kod, t.kod)]) for t in tokenek if (vers.kod, t.kod) in self.tarsitas), None)
        if par is not None:
            t, ta = par
            if self.heber_szo(vers, t) is not None:
                heber = self.heber_szo(vers, t)
            self._latott(ta.lemma)
            return tokenek, LxxSor(vers, lxx, heber, Gorog(GorogFajta.TARSITAS, lemma=idezet(ta.lemma),
                                                           kiejtes=idezet(ta.kiejtes)), Itelet.ELTERO),                 (ta.lemma.ertek,)
        return tokenek, LxxSor(vers, lxx, heber, Gorog(GorogFajta.NINCS), Itelet.FUGGOBEN), ()

    def csalad_cella(self, nyers):
        """A görög megfelelő valamely szava a motívum egy görög szavának szócsaládjába tartozik-e (a régi
        `_lxx_csalad_cella`). `nyers`: a megfelelő görög szövegei (alak, lemma)."""
        szavak = [w for x in nyers for w in _GOROG_SZO_RX.findall(x)]
        for t in self.gorog:
            tovek = self.f.kiejtes.gorog_tovek(t)
            if tovek and any(szavak_be.gorog_alak_tovek(w) & tovek for w in szavak):
                return True
        return False


def _ujraminosit(szamito, sor, tokenek, nyers):
    if sor.itelet is not Itelet.ELTERO:
        return sor
    if not any(h in szamito.par for h in tokenek):
        return _felulir(sor, itelet=Itelet.NINCS_PAR)
    if szamito.csalad_cella(nyers):
        return _felulir(sor, itelet=Itelet.SZOCSALAD)
    return sor


def osszevetes(f):
    """Az összevetés a motívum ószövetségi sorain (a tábla rendjében), versenként."""
    szamito = _Szamito(f)
    if not szamito.gorog:
        raise bemenet.BemenetHiba('5.: a motívumnak nincs görög szava; a régi lánc erre más mondatot írt (`lxx_olvasoi`, '
                                  'görög szó nélkül): az ág nincs portolva')
    sorok, szamolt, nyers_gorog = [], [], []
    for s in sorted(f.sorok, key=lambda x: x.fajl_sorszam):
        if f.konyvek.ujszovetsegi(s.igehely.konyv):
            continue
        sor_tokenek = tuple(st for st in s.strongok if st.heber)
        for vers in szamito.karoli.versek(s.igehely):
            tokenek, sor, nyers = szamito.vers_itelet(vers, sor_tokenek)
            sor = _ujraminosit(szamito, sor, tokenek, nyers)
            sorok.append(sor)
            nyers_gorog.append(nyers)
            szamolt.append((tokenek, sor.itelet))
    szavankent = {}
    for tokenek, it in szamolt:
        for h in tokenek:
            szavankent.setdefault(h, []).append(it)
    szamlalo = _szamlalo(it for _t, it in szamolt)
    modell = Osszevetes(
        sorok=tuple(sorok), szamlalo=szamlalo,
        szavankent=tuple(SzoSzamlalo(h, _szamlalo(lista)) for h, lista in szavankent.items()),
        par_szavak=szamito.par, gorog_szavak=szamito.gorog,
        par_nevek=tuple(f.szo(h) for h in szamito.par), fok=hid_fok(szamlalo))
    _kapu_szavankent(modell, szamolt, f.motivum)
    _kapu_egyforras(szamito, modell, nyers_gorog, f.motivum)
    return modell


def _kapu_szavankent(modell, szamolt, motivum):
    """A szavankénti összeg egyszavas soroknál az összesítés (a régi `_lxx_ujraminosit` kapuja)."""
    if all(len(t) == 1 for t, _i in szamolt):
        for m in Itelet:
            osszeg = sum(getattr(sz.szamlalo, m.value) for sz in modell.szavankent)
            if osszeg != getattr(modell.szamlalo, m.value):
                raise KapuHiba('%s: a 4.6 szavankénti összege (%s=%d) eltér az 5. szakasz összesítésétől (%d)'
                               % (motivum.kod, m.value, osszeg, getattr(modell.szamlalo, m.value)))


def _kapu_egyforras(szamito, modell, nyers_gorog, motivum):
    """F182 (A19, K72; a régi `lxx_egyforras_ellenoriz`): ugyanarra a (vers, héber szó) párra az 5. szakasz és a 4.11
    nem adhat eltérő LXX-megfelelőt."""
    elter = []
    for sor, nyers in zip(modell.sorok, nyers_gorog):
        if sor.itelet not in (Itelet.EGYEZO, Itelet.ELTERO, Itelet.SZOCSALAD, Itelet.NINCS_PAR) or sor.heber is None:
            continue
        g_szavak = {lxx_be.ekezet_nelkul(w) for x in nyers for w in _GOROG_SZO_RX.findall(x)}
        for (v, st), ta in szamito.tarsitas.items():
            if v != sor.vers.kod or szamito.heber_szo(sor.vers, Strong(st)) != sor.heber:
                continue
            if not all(x in g_szavak for x in ta.lemmak()):
                elter.append((v, st))
    if elter:
        raise KapuHiba('%s: az 5. szakasz és a 4.11 LXX-megfelelője eltér: %r' % (motivum.kod, elter))


def szamit(korny):
    """Az 5. szakasz modellje: az összevetés a motívum ószövetségi sorain. A számítás itt újra fut (a 4.6 a 4. szakasz
    forrásaiból számol): a szakasz forrásfigyelése (GK-07) így a saját olvasásait látja; a bemenetek beolvasása
    gyorsítótárazott, csak az összevetés fut kétszer."""
    from lapgen.szamitas import szocikkek
    f = szocikkek.forrasok(korny.b, korny.motivum)
    if not any(not f.konyvek.ujszovetsegi(s.igehely.konyv) for s in f.sorok):
        raise bemenet.BemenetHiba('5.: a motívumnak nincs ószövetségi előfordulása; az üres blokk ága nincs portolva')
    return osszevetes(f)


# --- a 4.6 (LXX-híd): a két nyelvrész pontja ugyanabból az összevetésből -------------------------------------------
@dataclasses.dataclass(frozen=True)
class SzoMondat:
    """A héber szó 4.6-os mondatának adatai: a szó, a számlálója, van-e a motívumban újszövetségi párja, és jár-e
    a mondathoz következtetés (párral bíró szónál legalább `konfig.LXX_SZO_MIN` vers, és a szócsaládos egyezés aránya
    legalább `konfig.LXX_SZO_ARANY`)."""
    szo: Szo
    szamlalo: Szamlalo
    van_par: bool
    kovetkeztetes: bool = False


def szo_kovetkeztetes(szamlalo, van_par):
    """A 4.6 szavankénti mondatának következtetése (a régi `lxx_szo_uj` küszöbe)."""
    n = szamlalo.osszes()
    return van_par and n >= konfig.LXX_SZO_MIN and (szamlalo.egyezo + szamlalo.szocsalad) / n >= konfig.LXX_SZO_ARANY


@dataclasses.dataclass(frozen=True)
class TarsElem:
    szo: Szo
    glossza: Optional[Lathato]
    versek: int


@dataclasses.dataclass(frozen=True)
class Tarslista:
    """A héber szó versszintű görög társai (ugyanaz a mérce, mint az Áttekintésé). `versek` None: a táblában a szónak
    nincs sora (a forrás nem tárgyalja)."""
    szo: Szo
    versek: Optional[int]
    parral: int
    tarsak: Tuple[TarsElem, ...]


@dataclasses.dataclass(frozen=True)
class LxxHid:
    """A 4.6 pont egy nyelvrészen. `szavak`: a nyelvrész szavai; `mondatok` és `tarslistak` csak héberül."""
    osszevetes: Osszevetes
    szavak: Tuple[Szo, ...]
    mondatok: Tuple[SzoMondat, ...] = ()
    tarslistak: Tuple[Tarslista, ...] = ()
    proveniencia: Optional[Proveniencia] = None


def hid(f, osszevetes_modell, sajat, heber, tarsulas):
    """A 4.6 pont a nyelvrész szavaira (`sajat`). Héberül szavanként a mondat (az összevetés szavankénti
    számlálójából) és a társlista (a `tarsulas` mércéjével)."""
    szavak = tuple(f.szo(s) for s in sajat)
    if not heber:
        return LxxHid(osszevetes_modell, szavak)
    szamlalok = {sz.strong: sz.szamlalo for sz in osszevetes_modell.szavankent}
    mondatok, tarslistak, proveniencia = [], [], None
    for s in sajat:
        if s not in szamlalok or not szamlalok[s].osszes():
            raise KapuHiba('4.6: a(z) %s szónak nincs sora az 5. szakaszban: az ág nincs portolva' % s.kod)
        van_par = s in osszevetes_modell.par_szavak
        mondatok.append(SzoMondat(f.szo(s), szamlalok[s], van_par, szo_kovetkeztetes(szamlalok[s], van_par)))
        versek = tarsulas.parok_versek(s)
        if versek is None:
            tarslistak.append(Tarslista(f.szo(s), None, 0, ()))
            continue
        if proveniencia is None:
            proveniencia = tarsulas.proveniencia(s)
        elemek = tuple(TarsElem(f.szo(g), _glossza_f(f, g), kozos)
                       for g, kozos in tarsulas.tarsak(s)[:konfig.LXX_PAROK_TOP])
        tarslistak.append(Tarslista(f.szo(s), len(versek), sum(1 for gs in versek.values() if gs), elemek))
    if tarslistak and proveniencia is None:
        raise KapuHiba('4.6: a motívum egyik héber szavának sincs sora a versszintű párok táblájában; a régi lánc a '
                       'forrás-sort ekkor is kiírta: az ág nincs portolva')
    egyezes_kapu(mondatok, osszevetes_modell.szamlalo, elofordulas_be.szopar_motivum(f.sorok), f.motivum)
    return LxxHid(osszevetes_modell, szavak, tuple(mondatok), tuple(tarslistak), proveniencia)


def egyezes_kapu(mondatok, szamlalo, szopar, motivum):
    """GK-04 (a régi `lxx_egyezes_kapu`, F212 Sz1, F194): a héber 4.6 szavankénti mondatainak versszáma az 5. szakasz
    összesítésével egyezik. Egyes szavas motívumnál a szavankénti számok összege a versek száma; szópáros (formulaikus)
    motívumnál a pár minden tagja minden versben áll, ezért mindegyik mondat a teljes versszámot mondja. A rövid mondatok,
    az összegző és a görög 4.6 számai ugyanabból a számlálóból jönnek, köztük eltérés nem keletkezhet."""
    n = szamlalo.osszes()
    szamok = [m.szamlalo.osszes() for m in mondatok]
    if not szamok:
        return
    if szopar:
        if any(x != n for x in szamok):
            raise KapuHiba('%s: a héber 4.6 szavankénti száma (szópár) %r eltér az 5. szakasz összesítésétől (%d)'
                           % (motivum.kod, tuple(szamok), n))
    elif sum(szamok) != n:
        raise KapuHiba('%s: a héber 4.6 szavankénti összege (%d) eltér az 5. szakasz összesítésétől (%d)'
                       % (motivum.kod, sum(szamok), n))


def _glossza_f(f, strong):
    magyar = f.rovid.jelentes(strong).magyar
    return idezet(f.tablaban(magyar)) if magyar is not None else None
