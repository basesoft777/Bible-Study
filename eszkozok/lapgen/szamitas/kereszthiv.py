"""lapgen.szamitas.kereszthiv — a „6. Kereszthivatkozások” szakasz és a Minősítés lapmodellje (S5).

A szakasz a motívum helyeit veti össze a két hagyományos gyűjteménnyel (TSK, legalább a küszöbnyi szavazattal; a
Károli-fordítás megerősített utalásai), helyenként. A Minősítés ugyanezekből az utalásokból azokat számolja, amelyek a
motívum két saját helyét kötik össze, és felsorolja a kereszthivatkozásból vizsgált helyeket a döntésükkel.

A régi generátor szabályai (`blokk_kereszthivatkozasok`, `adatres_minosites`, `minosites_jelolt_sorok`) szerint; a
számok egyetlen helyen képződnek, és a kapu a modellen ellenőrzi őket. A szövegvizsgálat (az ok és az indoklás
egyezése, a forrásnév) a bemeneti rétegé.
"""
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import kereszthiv as kh_be
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.nyelv import ok_cellaalakok
from lapgen.ertekek import AjanlasFajta, Dontes, Gyujtemeny  # noqa: F401 (a megjelenítő innen veszi)
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, Lathato, MotivumId, Proveniencia, Strong, idezet, prov, prov_fuz, proza


@dataclasses.dataclass(frozen=True)
class KhUtalas:
    """Egy kereszthivatkozás egy forrásversről: a cél, a gyűjtemény és (a TSK-nál) a szavazatszám."""
    cel: Igehely
    gyujtemeny: Gyujtemeny
    szavazat: Optional[int]


@dataclasses.dataclass(frozen=True)
class KhHely:
    """Egy hely, amelyről legalább egy utalás indul: előbb a TSK utalásai (csökkenő szavazatszám szerint), utána a
    Károli-fordításéi."""
    igehely: Igehely
    utalasok: Tuple[KhUtalas, ...]


@dataclasses.dataclass(frozen=True)
class MinPar:
    """Külső megerősítés: utalás a motívum egyik saját helyéről egy másikra."""
    forras: Igehely
    cel: Igehely
    gyujtemeny: Gyujtemeny
    szavazat: Optional[int]


@dataclasses.dataclass(frozen=True)
class Miert:
    """A jelölés oka: a gyűjtemény, a forrásverse(i), a célhely, a szavazatszámok ((tól, ig) párok), a forráshely
    TSK-találatainak száma, és hogy a Károli is ajánlja-e."""
    fajta: AjanlasFajta
    forrasok: Tuple[Igehely, ...]
    cel: Optional[Igehely]
    szavazatok: Optional[Tuple[Tuple[int, Optional[int]], ...]]
    talalat: Optional[int]
    karoli_is: bool


@dataclasses.dataclass(frozen=True)
class StrongHiv:
    """Strong-hivatkozás a kézi indoklásban: a szó (kézi), a Strong-szám és a rövid magyar jelentés (ha van)."""
    szo: Lathato
    strong: Strong
    glossza: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class IndokResz:
    """Az indoklás egy darabja: kézi próza, motívum-hivatkozás vagy Strong-hivatkozás (pontosan egy áll)."""
    proza: Optional[Lathato] = None
    motivum: Optional[MotivumId] = None
    strong: Optional[StrongHiv] = None


@dataclasses.dataclass(frozen=True)
class MinJelolt:
    """A kereszthivatkozásból vizsgált hely: a jelölés oka, a döntés, az ok cellakezdő alakja (elutasított helynél,
    ha a cellában áll), és az indoklás darabjai."""
    igehely: Igehely
    miert: Miert
    dontes: Dontes
    ok: Optional[Lathato]
    indok: Tuple[IndokResz, ...]


@dataclasses.dataclass(frozen=True)
class Minosites:
    parok: Tuple[MinPar, ...]
    erintett: int
    n: int
    osszes: int
    jeloltek: Tuple[MinJelolt, ...]
    dontesek: Tuple[Tuple[Dontes, int], ...]
    kozos_olvasoi: Optional[Proveniencia]
    kozos_eredeti: Optional[Proveniencia]


@dataclasses.dataclass(frozen=True)
class KhSzakasz:
    n: int
    helyek: Tuple[KhHely, ...]
    nem_vizsgalhato: Tuple[Igehely, ...]
    kihagyott: Tuple[Tuple[Igehely, int], ...]
    osszes: int
    kuszob: int
    minosites: Minosites


def _utalas(u):
    return KhUtalas(u.cel, u.gyujtemeny, u.szavazat)


def _miert(a):
    return Miert(a.fajta, tuple(a.forrasok), a.cel, a.szavazatok, a.talalat, a.karoli_is)


def _resz(rovid, d):
    if d.motivum is not None:
        return IndokResz(motivum=d.motivum)
    if d.strong is not None:
        magyar = rovid.jelentes(d.strong).magyar
        return IndokResz(strong=StrongHiv(proza(d.kezi), d.strong, idezet(magyar) if magyar is not None else None))
    return IndokResz(proza=proza(d.kezi))


def _kozos(jeloltek):
    """A jelöltsorok közös forrásmegjelölése (a régi `kozos_proveniencia`, ‹M› előtaggal): (olvasói, eredeti), mindkettő
    megjegyzésbe kerül."""
    szamlalo, peldany = {}, {}
    for j in jeloltek:
        if j.prov is not None:
            szamlalo[j.prov.kulcs] = szamlalo.get(j.prov.kulcs, 0) + 1
            peldany.setdefault(j.prov.kulcs, j.prov)
    kozos = [k for k, db in sorted(szamlalo.items(), key=lambda x: (-x[1], x[0]))
             if db >= konfig.KOZOS_PROVENIENCIA_KUSZOB]
    if not kozos:
        return None, None
    if len(kozos) == 1 and szamlalo[kozos[0]] == len(jeloltek):
        p = peldany[kozos[0]]
        return (prov('Minden sor forrásmegjelölése (‹M1›): {}', p.olvasoi),
                prov('*Minden sor forrásmegjelölése (‹M1›): `{}`*', p.harmas))
    return (prov('A közös forrásmegjelölések: {}', prov_fuz(' · ', [
                prov('‹M{}› = {} ({} sor)', i, peldany[k].olvasoi, szamlalo[k]) for i, k in enumerate(kozos, 1)])),
            prov('*A közös forrásmegjelölések: {}*', prov_fuz(' · ', [
                prov('‹M{}› = `{}` ({} sor)', i, peldany[k].harmas, szamlalo[k]) for i, k in enumerate(kozos, 1)])))


def _minosites(b, motivum, sorok, utalasok, osszes):
    """A Minősítés: a motívum két saját helyét összekötő utalások (a motívum sorainak rendjében, a TSK a forrás
    sorrendjében, utána a Károli), és a kereszthivatkozásból vizsgált helyek."""
    halmaz = frozenset(sor.igehely for sor in sorok)
    parok, latott = [], set()
    for sor in sorok:
        a = sor.igehely
        for u in utalasok.get(a, ()):
            kulcs = (a, u.cel, u.gyujtemeny, u.szavazat)
            if u.cel in halmaz and u.cel != a and kulcs not in latott:
                latott.add(kulcs)
                parok.append(MinPar(a, u.cel, u.gyujtemeny, u.szavazat))
    erintett = frozenset(x for p in parok for x in (p.forras, p.cel))
    jeloltek_be = kh_be.kereszthiv_jeloltek(b, motivum)
    cella = ok_cellaalakok(b)
    rovid = motivum_be.rovid_jelentes(b)
    jeloltek = []
    for j in jeloltek_be:
        ok = None
        if j.ok is not None and not j.ok_ismetles:
            alak = cella.get(j.ok.cimke.ertek)
            ok = proza(alak if alak is not None else j.ok.cimke)
        jeloltek.append(MinJelolt(j.igehely, _miert(j.ajanlas), j.dontes, ok, tuple(_resz(rovid, d) for d in j.indok)))
    dontesek = tuple((d, sum(1 for j in jeloltek if j.dontes is d))
                     for d in (Dontes.BEEPITVE, Dontes.ELUTASITVA, Dontes.NYITVA))
    kozos_olvasoi, kozos_eredeti = _kozos(jeloltek_be)
    return Minosites(parok=tuple(parok), erintett=len(erintett), n=len(sorok), osszes=osszes,
                     jeloltek=tuple(jeloltek), dontesek=tuple(x for x in dontesek if x[1]),
                     kozos_olvasoi=kozos_olvasoi, kozos_eredeti=kozos_eredeti)


def szamit(korny):
    b, motivum = korny.b, korny.motivum
    sorok = bemenet.b03_elofordulasok(b, motivum)
    if not sorok:
        raise bemenet.BemenetHiba('B03: a motívumnak nincs előfordulás-sora')
    konyvek = bemenet.b63_konyvek(b)
    kuszob = konfig.TSK_SZAVAZAT_KUSZOB
    helyek, nem_vizsgalhato, kihagyott, utalasok = [], [], [], {}
    for igehely in sorted((sor.igehely for sor in sorok), key=konyvek.rendezo_kulcs):
        if konyvek.step_vers(igehely) is None:
            nem_vizsgalhato.append(igehely)
            continue
        kh, elvetett = kh_be.b43_karoli_kh(b, igehely)
        if elvetett:
            kihagyott.append((igehely, elvetett))
        tsk = tuple(_utalas(u) for u in kh_be.b44_tsk(b, igehely, kuszob))
        kh = tuple(_utalas(u) for u in kh)
        utalasok[igehely] = tsk + kh        # a Minősítés a forrás sorrendjében párosít
        mind = tuple(sorted(tsk, key=lambda u: -u.szavazat)) + kh   # a lapon csökkenő szavazatszám szerint
        if mind:
            helyek.append(KhHely(igehely, mind))
    osszes = sum(len(h.utalasok) for h in helyek)
    return KhSzakasz(n=len(sorok), helyek=tuple(helyek), nem_vizsgalhato=tuple(nem_vizsgalhato),
                     kihagyott=tuple(kihagyott), osszes=osszes, kuszob=kuszob,
                     minosites=_minosites(b, motivum, sorok, utalasok, osszes))


def kapu(m):
    """A szakasz számegyezése a modellen: a felsorolt és a versenként nem vizsgálható helyek együtt sem több, mint a
    motívum helyei, és egy hely legfeljebb egyszer áll (GK-A1); az összes utalás a felsoroltak összege; a Minősítés
    párjai a felsorolt utalások közül valók; a döntések összege a vizsgált helyek száma. Eltérésnél KapuHiba."""
    felsorolt_helyek = [h.igehely for h in m.helyek] + list(m.nem_vizsgalhato)
    if len(felsorolt_helyek) > m.n or len(frozenset(felsorolt_helyek)) != len(felsorolt_helyek):
        raise KapuHiba('6.: a felsorolt (%d) és a versenként nem vizsgálható (%d) helyek között ismétlődés van, vagy '
                       'több, mint a motívum %d helye' % (len(m.helyek), len(m.nem_vizsgalhato), m.n))
    if sum(len(h.utalasok) for h in m.helyek) != m.osszes or m.minosites.osszes != m.osszes:
        raise KapuHiba('6.: az utalások összege nem a kimondott szám (%d)' % m.osszes)
    felsorolt = frozenset((h.igehely, u.cel, u.gyujtemeny, u.szavazat) for h in m.helyek for u in h.utalasok)
    mi = m.minosites
    for p in mi.parok:
        if (p.forras, p.cel, p.gyujtemeny, p.szavazat) not in felsorolt:
            raise KapuHiba('Minősítés: a %s → %s pár nem áll a 6. szakasz utalásai között' % (p.forras.kod, p.cel.kod))
    if mi.erintett > mi.n or (mi.parok and mi.erintett < 2):
        raise KapuHiba('Minősítés: az érintett helyek száma (%d) nem lehetséges' % mi.erintett)
    if sum(db for _d, db in mi.dontesek) != len(mi.jeloltek):
        raise KapuHiba('Minősítés: a döntések összege nem a vizsgált helyek száma (%d)' % len(mi.jeloltek))
    return m
