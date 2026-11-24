"""lapgen.szamitas.kizart — a „3. Kizárt és vizsgált helyek” szakasz lapmodellje (S9a).

A számok a vizsgálat közös modelljéből jönnek (`szamitas.vizsgalat`: a „Döntési út” és a melléklet is ebből számol),
a táblák sorai a döntésnaplóból (`bemenet.vizsgalt`). A szakasz kapuja a modellen fut: az okok versszámainak összege
és a jelölési forráscsoportok versszámainak összege a kizárt versek száma.

A régi lap ugyanezt utólagos szövegcserékkel állította elő (a „Miért lett jelölt” cella, a csoportnevek, az összesítő
sor eleje, a táblajegyzet); itt a cella és a jegyzet a szerkezetből készül (`megjelenites.md.kizart`).
"""
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.bemenet import vizsgalt as vizsgalt_be
from lapgen.ertekek import Dontes, JelolesFajta, VizsgaltCsoport, VizsgaltJegyzetFajta
from lapgen.szamitas import vizsgalat
from lapgen.bemenet.nyelv import ok_cellaalakok, ok_leiras_cellaalakok
from lapgen.szamitas.kereszthiv import Miert, ajanlas_miert, indok_resz
from lapgen.szoveg import Igehely, Kulcs, Lathato, Proveniencia, Strong, idezet, prov, prov_fuz, proza

CSOPORT_REND = (VizsgaltCsoport.TSK, VizsgaltCsoport.KAROLI, VizsgaltCsoport.KERESES, VizsgaltCsoport.SZERKESZTOI)
# a kereszthivatkozásból vizsgált sorok táblája a 6. szakasz Minősítésében áll (`kereszthiv_jeloltek`, ugyanazokból a
# döntésnapló-sorokból); itt a csoport csak a számaival szerepel, a sorai nem ismétlődnek (F241.5b, D15 (2))
KH_CSOPORTOK = (VizsgaltCsoport.TSK, VizsgaltCsoport.KAROLI)
_NEVELOK = ('a ', 'az ')


class KapuHiba(vizsgalat.KapuHiba):
    """BUKÁS: a 3. szakasz számai nem egyeznek a vizsgálat modelljével."""


@dataclasses.dataclass(frozen=True)
class SzoNev:
    """A keresett szó a cellában: a szótári alak és a kiejtés (None: kimondott hiány)."""
    strong: Strong
    alak: Optional[Lathato]
    kiejtes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class Jeloles:
    """A „Miért került a vizsgálatba” cella szerkezete."""
    fajta: JelolesFajta
    ajanlas: Optional[Miert] = None
    szavak: Tuple[SzoNev, ...] = ()
    halok: Tuple[Kulcs, ...] = ()
    csoport_versszam: Optional[int] = None


@dataclasses.dataclass(frozen=True)
class Jegyzet:
    """A sor jegyzete (a cellán túli jelölési forrás)."""
    fajta: VizsgaltJegyzetFajta
    szavak: Tuple[SzoNev, ...] = ()
    megszoritas: Optional[Kulcs] = None
    korpuszok: Tuple[Kulcs, ...] = ()


@dataclasses.dataclass(frozen=True)
class TablaSor:
    """A forráscsoport táblájának egy sora; `veg`: az összevont versek utolsó versszáma (None, ha egy vers)."""
    igehely: Igehely
    veg: Optional[int]
    dontes: Dontes
    jeloles: Jeloles
    ok: Optional[Lathato]
    ok_ismetles: bool
    osszesito: Optional[int]
    szerkesztoi_zaro: bool
    indok: tuple
    jegyzet: Optional[Jegyzet]
    eredeti: Proveniencia            # a jegyzet megjegyzése: a forrás-mező, a proveniencia-farok, a döntés nyoma


@dataclasses.dataclass(frozen=True)
class CsoportTabla:
    csoport: VizsgaltCsoport
    sorok_szama: int                 # a döntésnapló sorai (az összevonás előtt)
    versszam: int
    sorok: Tuple[TablaSor, ...]      # üres, ha a tábla máshol áll (`masutt`)
    masutt: bool = False             # a sorok a 6. szakasz Minősítésének táblájában állnak (KH_CSOPORTOK)


@dataclasses.dataclass(frozen=True)
class OkSor:
    ok: Lathato                      # a címke, ahogy az adatban áll (a mondat belsejébe)
    cella: Optional[Lathato]         # a táblacella eleji alakja (névelővel kezdődő címkénél a névtábla `ok_cella`
                                     # sora); None: az ok nem a táblában, hanem a tábla alatti mondatban áll
    versszam: int
    leiras: Optional[Lathato]        # a megjegyzés (None: az ok mintaszótárában nincs)
    peldak: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class KizartSzakasz:
    helyek: int                      # a motívum helyei
    egyen: int
    csoport: int
    nyitva: int
    sorok_szama: int                 # a táblák döntésnapló-sorai összesen
    okok: Tuple[OkSor, ...]
    forrasok: Tuple[Tuple[VizsgaltCsoport, int], ...]
    ajanlas: bool                    # van-e kereszthivatkozás-ajánlásból jött vizsgált vers
    tablak: Tuple[CsoportTabla, ...]
    kozos_olvasoi: Optional[Proveniencia]
    kozos_eredeti: Optional[Proveniencia]


def _szonev(kiejtes, strong):
    szo = kiejtes.szotari(strong)
    if szo is None:
        return SzoNev(strong, None, None)
    return SzoNev(strong, idezet(vizsgalat.html_ben(szo.alak)),
                  idezet(vizsgalat.html_ben(szo.kiejtes)) if szo.kiejtes is not None else None)


def _ok_cella(ok, cella_alakok):
    """A táblacella eleji alak: névelővel kezdődő címkénél a névtábla `ok_cella` sora (lista- és táblaelem nem
    kezdődik névelővel, a régi `nevelo_le` szabálya), különben a címke maga."""
    if ok.cimke.ertek.startswith(_NEVELOK):
        alak = cella_alakok.get(ok.cimke.ertek)
        if alak is None:
            raise bemenet.BemenetHiba('a névtáblában nincs `ok_cella` sor ehhez az elutasítási okhoz: %s'
                                      % ok.cimke.ertek)
        return proza(alak)
    return proza(ok.cimke)


def _leiras(ok, leiras_alakok):
    """A „Mit jelent” cella: az ok megjegyzése; névelővel kezdődő megjegyzésnél a táblacella eleji alakban (a
    névtábla `ok_leiras_cella` sora: táblaelem nem kezdődik kisbetűs névelővel); None, ha az oknak nincs
    megjegyzése."""
    if ok.megjegyzes is None:
        return None
    if not ok.megjegyzes.ertek.startswith(_NEVELOK):
        return proza(ok.megjegyzes)
    alak = leiras_alakok.get(ok.cimke.ertek)
    if alak is None:
        raise bemenet.BemenetHiba('a névtáblában nincs `ok_leiras_cella` sor ehhez az elutasítási okhoz: %s'
                                  % ok.cimke.ertek)
    return proza(alak)


def _indok_ok(ok, cella_alakok):
    """Az „Indok” cella eleji ok: a névtábla `ok_cella` sora (a cella nagy kezdőbetűvel indul)."""
    alak = cella_alakok.get(ok.cimke.ertek)
    if alak is None:
        raise bemenet.BemenetHiba('a névtáblában nincs `ok_cella` sor ehhez az elutasítási okhoz: %s' % ok.cimke.ertek)
    return proza(alak)


def _osszevon(sorok):
    """Az egymást követő, azonos kulcsú sorok (ugyanaz a könyv és fejezet, a következő vers) egy sorba (a régi
    `szerep_kizart.osszevon`): [(az első sor, az utolsó versszám vagy None)]."""
    ki = []
    for s in sorok:
        if ki:
            elso, utolso = ki[-1]
            if (len(s.versek) == 1 and len(utolso.versek) == 1 and s.osszevonas_kulcs == elso.osszevonas_kulcs
                    and s.igehely.konyv == utolso.igehely.konyv and s.igehely.fejezet == utolso.igehely.fejezet
                    and s.igehely.vers == utolso.igehely.vers + 1):
                ki[-1] = (elso, s)
                continue
        ki.append((s, s))
    return [(elso, utolso.igehely.vers if utolso is not elso else None) for elso, utolso in ki]


def _suly(s, egyedi):
    """A sor versszáma a forráscsoport összegéhez: csoportos sornál a csoport egyedi versei (a vizsgálat modellje
    szerint: a más csoportban is álló vers egyszer számít), különben a versek (a tartomány kibontva). A cella a
    csoportos sor saját versszámát mondja (a forrás-mező szerint)."""
    if s.jeloles.csoport_versszam is not None:
        if s.igehely not in egyedi:
            raise KapuHiba('a 3. szakasz csoportos sora (%s) nincs a vizsgálat modelljében' % s.igehely.kod)
        return egyedi[s.igehely]
    return len(s.versek)


def szamit(korny):
    b, motivum = korny.b, korny.motivum
    v = vizsgalat.szamit(korny)
    sorok_be = vizsgalt_be.vizsgalt_sorok(b, motivum)
    kiejtes = szavak_be.kiejtes(b)
    rovid = motivum_be.rovid_jelentes(b)
    cella_alakok = ok_cellaalakok(b)
    leiras_alakok = ok_leiras_cellaalakok(b)
    egyedi = dict(v.csoport_egyedi)
    szavak = {}

    def szonevek(strongok):
        for st in strongok:
            if st not in szavak:
                szavak[st] = _szonev(kiejtes, st)
        return tuple(szavak[st] for st in strongok)

    # az okok táblája: a vizsgálat modelljének okai versszám szerint, egyenlőségnél a címke szerint
    peldak = {}
    for s in sorok_be:
        if s.ok is not None:
            lista = peldak.setdefault(s.ok.cimke.ertek, [])
            if s.igehely not in lista and len(lista) < konfig.KIZART_PELDA_DB:
                lista.append(s.igehely)
    okcsoportok = {}
    for o in v.csoport_okok + v.egyen_okok:
        kulcs = o.ok
        if kulcs in okcsoportok:
            elozo = okcsoportok[kulcs]
            okcsoportok[kulcs] = (elozo[0], elozo[1] + o.versszam)
        else:
            okcsoportok[kulcs] = (o, o.versszam)
    okok_be = {s.ok.cimke.ertek: s.ok for s in sorok_be if s.ok is not None}
    rendezett = []
    for o, n in okcsoportok.values():
        ok_be = next(x for x in okok_be.values() if proza(x.cimke) == o.ok)
        rendezett.append((-n, ok_be.cimke.ertek, ok_be, n))
    rendezett.sort(key=lambda x: (x[0], x[1]))
    # a táblában álló okok (a legnagyobbak) cellái; a többi ok a tábla alatti mondatban, csak a címkéjével
    okok = tuple(OkSor(ok=proza(ok_be.cimke), cella=_ok_cella(ok_be, cella_alakok) if i < konfig.KIZART_TABLA_OK_DB
                       else None, versszam=n,
                       leiras=_leiras(ok_be, leiras_alakok) if i < konfig.KIZART_TABLA_OK_DB else None,
                       peldak=tuple(peldak.get(ok_be.cimke.ertek, ())))
                 for i, (_r, _k, ok_be, n) in enumerate(rendezett))

    # a jegyzetek megjegyzései: a közös proveniencia-sorok jele (‹K1› …) az összevont sorok szerint
    csoportonkent = {c: [] for c in CSOPORT_REND}
    for s in sorok_be:
        csoportonkent[s.csoport].append(s)
    osszevont = {c: _osszevon(ss) for c, ss in csoportonkent.items()}
    nyers = []
    for c in CSOPORT_REND:
        if c in KH_CSOPORTOK:
            continue
        for elso, _veg in osszevont[c]:
            nyers.append(elso.jegyzet_nyers)
    szamlalo, peldany = {}, {}
    for szoveg in nyers:
        for h in set(vizsgalt_be.proveniencia_harmasok(szoveg)):
            szamlalo[h] = szamlalo.get(h, 0) + 1
    kozos = [h for h, db in sorted(szamlalo.items(), key=lambda x: (-x[1], x[0])) if db >= konfig.KOZOS_PROVENIENCIA_KUSZOB]
    sorszamok = {h: i for i, h in enumerate(kozos, 1)}
    jelek = {h: prov('‹K{}›', i) for h, i in sorszamok.items()}

    tablak, forrasok, sorszam = [], [], 0
    for c in CSOPORT_REND:
        if not csoportonkent[c]:
            continue
        versszam = sum(_suly(s, egyedi) for s in csoportonkent[c])
        forrasok.append((c, versszam))
        if c in KH_CSOPORTOK:
            tablak.append(CsoportTabla(csoport=c, sorok_szama=len(csoportonkent[c]), versszam=versszam, sorok=(),
                                       masutt=True))
            continue
        sorok = []
        for elso, veg in osszevont[c]:
            sorszam += 1
            j = elso.jeloles
            jeloles = Jeloles(fajta=j.fajta, ajanlas=ajanlas_miert(j.ajanlas) if j.ajanlas is not None else None,
                              szavak=szonevek(j.strongok), halok=j.halok,
                              csoport_versszam=j.csoport_versszam)
            jegyzet = None
            if elso.jegyzet is not None:
                g = elso.jegyzet
                jegyzet = Jegyzet(fajta=g.fajta, szavak=szonevek(g.strongok),
                                  megszoritas=g.megszoritas,
                                  korpuszok=g.korpuszok)
            ok = None
            if elso.ok is not None and not elso.ok_ismetles:
                ok = _indok_ok(elso.ok, cella_alakok)
            sorok.append(TablaSor(
                igehely=elso.igehely, veg=veg, dontes=elso.dontes, jeloles=jeloles, ok=ok,
                ok_ismetles=elso.ok_ismetles, osszesito=elso.osszesito, szerkesztoi_zaro=elso.szerkesztoi_zaro,
                indok=tuple(indok_resz(rovid, d) for d in elso.indok), jegyzet=jegyzet,
                eredeti=prov('[^k{}]: {}', sorszam, vizsgalt_be.proveniencia_csere(elso.jegyzet_nyers, sorszamok))))
        tablak.append(CsoportTabla(csoport=c, sorok_szama=len(csoportonkent[c]), versszam=versszam,
                                   sorok=tuple(sorok)))

    kozos_olvasoi = kozos_eredeti = None
    if kozos:
        olvasoi = {h: vizsgalt_be.prov_olvasoi(h) for h in kozos}
        if len(kozos) == 1 and szamlalo[kozos[0]] == len(nyers):
            h = kozos[0]
            kozos_olvasoi = prov('Minden sor forrásmegjelölése ({}): {}', jelek[h], olvasoi[h])
            kozos_eredeti = prov('*Minden sor forrásmegjelölése ({}): `{}`*', jelek[h], h)
        else:
            kozos_olvasoi = prov('A közös forrásmegjelölések: {}', prov_fuz(' · ', [
                prov('{} = {} ({} sor)', jelek[h], olvasoi[h], szamlalo[h]) for h in kozos]))
            kozos_eredeti = prov('*A közös forrásmegjelölések: {}*', prov_fuz(' · ', [
                prov('{} = `{}` ({} sor)', jelek[h], h, szamlalo[h]) for h in kozos]))

    return KizartSzakasz(
        helyek=v.helyek, egyen=v.egyen, csoport=v.csoport, nyitva=v.nyitva, sorok_szama=len(sorok_be),
        okok=okok, forrasok=tuple(forrasok), ajanlas=v.ajanlas > 0, tablak=tuple(tablak),
        kozos_olvasoi=kozos_olvasoi, kozos_eredeti=kozos_eredeti)


def kapu(m):
    """A szakasz kapuja: az okok versszámainak összege és a forráscsoportok versszámainak összege a kizárt versek
    száma (a vizsgálat modellje szerint)."""
    kizart = m.egyen + m.csoport + m.nyitva
    if sum(o.versszam for o in m.okok) != m.egyen + m.csoport:
        raise KapuHiba('a 3. szakasz okainak versszám-összege (%d) nem a kizárt versek száma (%d)'
                       % (sum(o.versszam for o in m.okok), m.egyen + m.csoport))
    if sum(n for _c, n in m.forrasok) != kizart:
        raise KapuHiba('a 3. szakasz jelölési forrásainak versszám-összege (%d) nem a vizsgált versek száma (%d)'
                       % (sum(n for _c, n in m.forrasok), kizart))
    if sum(t.sorok_szama for t in m.tablak) != m.sorok_szama:
        raise KapuHiba('a 3. szakasz tábláinak sorai nem fedik a döntésnapló sorait')
    return m
