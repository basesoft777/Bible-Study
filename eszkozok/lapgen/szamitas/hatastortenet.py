"""lapgen.szamitas.hatastortenet — a „9. Hatástörténet: ókori fordítások és értelmezők” szakasz (S7).

Három rész: (1) az ószövetségi lánc ókori fordításai (Targum, Vulgata, LXX) lánc-szavanként, a LXX-alapvonallal; (2)
az újszövetségi helyek latin fordítása, szövegváltozatai és a görög szócsalád a lánc Septuagintájában; (3) a tanúk
(ókori értelmezők). A régi generátor szabályai: `blokk_visszhang`, `visszhang_cella`, `_visszhang_mondat_lxx`,
`_egyesites_mondat`, `lxx_alapvonal` (1); `blokk_hatas_usz`, `_usz_valtozatok` (2); `tanuk_lapra`, `blokk_hatas_tanuk`
(3); a lánc a 4.8 pont lánc-szavaiból (`nyelvi_hatter.lanc_szavak`; DT-F178g, a szópárra DT833). Mondatot nem fogalmaz:
a megjelenítő teszi a sablontáblából.

A forrás-állapot (GK-28): a Targum-oszlop a Targum-forrás tényleges lefedettségéből (B64) mondja ki, hol nincs
Targum-forrás; a régi kód ezt kódba írt könyvlistából vette, és a forrásban nem álló versre „nincs megfelelő szó”-t
mondott. A Peshitta mondata a forrás állapotából (B73) jön.
"""
import dataclasses
import datetime
import enum
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import hatastortenet as ht_be
from lapgen.bemenet import szotari as szotari_be
from lapgen.bemenet.motivum import lanc_mag
from lapgen.ertekek import ForrasAllapot, TanuForras
from lapgen.szamitas import nyelvi_hatter as nyelvi_hatter_sz
from lapgen.szamitas import szocikkek as szocikkek_sz
from lapgen.szamitas.szotari_tipusok import Szo
from lapgen.szoveg import Igehely, Kulcs, Lathato, Strong, idezet, proza


class Forditas(enum.Enum):
    TARGUM = konfig.FORRAS_TARGUM
    VULGATA = konfig.FORRAS_VULGATA
    LXX = konfig.FORRAS_LXX


FORDITASOK = (Forditas.TARGUM, Forditas.VULGATA, Forditas.LXX)


class Hiany(enum.Enum):
    """Miért nincs a versben a fordítás szava."""
    NINCS_SZO = 'nincs_szo'                     # ellenőrzött sor alak nélkül: a fordításban nincs megfelelő szó
    NINCS_ELLENORZOTT = 'nincs_ellenorzott'     # van sor, de nem ellenőrzött
    NINCS_KINYERES = 'nincs_kinyeres'           # a versre nincs sor: a megfelelő kinyerése nem történt meg


class CellaFajta(enum.Enum):
    NINCS_FORRAS = 'nincs_forras'     # a Targum-forrás egyik láncverset sem fedi
    NINCS_ADAT = 'nincs_adat'         # egyik versben sincs ellenőrzött szó
    KULONBOZO = 'kulonbozo'           # minden versben más szó
    TELJES = 'teljes'                 # minden versben ugyanaz a szó vagy szócsalád
    RESZ = 'resz'                     # a versek egy részében


@dataclasses.dataclass(frozen=True)
class OkoriSzo:
    """A fordítás szava a cellában: a lemma és a kiejtése (a Vulgatánál kiejtés nélkül)."""
    forditas: Forditas
    lemma: Lathato
    kiejtes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class Elteres:
    """Egy vers a cellában: a szava, vagy a hiánya."""
    hely: Igehely
    szo: Optional[OkoriSzo]
    hiany: Optional[Hiany]


@dataclasses.dataclass(frozen=True)
class OkoriCella:
    fajta: CellaFajta
    szavak: Tuple[OkoriSzo, ...]        # a fő szócsalád szavai (TELJES, RESZ)
    n: int
    nn: int                             # a láncversek száma (N)
    hiany: Optional[Hiany]              # NINCS_ADAT
    versek: Tuple[Elteres, ...]         # KULONBOZO: minden vers; RESZ: az eltérő versek
    mind_mas_szo: bool                  # RESZ: minden eltérő versben más szó áll
    targum_kivul: Tuple[Igehely, ...]   # a versek, amelyeket a Targum-forrás nem fed


class Sav(enum.Enum):
    """A LXX-alapvonal sávja (DT-F178d)."""
    SZOKASOS = 'szokasos'
    GYAKORI = 'gyakori'
    RITKA = 'ritka'


@dataclasses.dataclass(frozen=True)
class Alapvonal:
    sav: Sav
    szazalek: int
    nn: int          # a láncon kívüli versek száma
    talalat: int     # ezek közül ennyiben áll a szócsalád


class LxxFajta(enum.Enum):
    NINCS_ADAT = 'nincs_adat'       # a LXX-oszlopban nincs ellenőrzött szó
    ELTERES = 'elteres'             # a versek egy részében más szó vagy hiány
    NEM_MERHETO = 'nem_merheto'     # a héber szó a láncon kívül nem fordul elő
    ALAPVONAL = 'alapvonal'


@dataclasses.dataclass(frozen=True)
class LxxMondat:
    fajta: LxxFajta
    hiany: Optional[Hiany]
    mas: int
    nincs_szo: int
    hianyzo: int
    alapvonal: Optional[Alapvonal]
    szocsalad: bool


class EgyesitesFajta(enum.Enum):
    """Két héber lánc-szó egy szóval vagy szócsaláddal (DT-F178d, pontosítva)."""
    NEM_MERHETO_FORRAS = 'nem_merheto_forras'   # Targum, Vulgata: a láncon kívül ebből a forrásból nem mérhető
    NEM_MERHETO = 'nem_merheto'                 # LXX: valamelyik szónál nincs alapvonal
    SZOKASOS = 'szokasos'
    RITKA = 'ritka'
    GYAKORI = 'gyakori'


@dataclasses.dataclass(frozen=True)
class Egyesites:
    forditasok: Tuple[Forditas, ...]     # egy, vagy a Targum és a Vulgata összevonva
    fajta: EgyesitesFajta
    szavak: Tuple[Szo, ...]               # a két héber szó
    szocsalad: bool
    szazalekok: Tuple[int, ...]           # LXX: a két szó alapvonala százalékban


@dataclasses.dataclass(frozen=True)
class Utalas:
    szo: Szo


@dataclasses.dataclass(frozen=True)
class Mondat:
    """A „Mit mutat” cella egy mondata: pontosan egy mező nem üres."""
    egyesites: Optional[Egyesites] = None
    utalas: Optional[Utalas] = None
    lxx: Optional[LxxMondat] = None


@dataclasses.dataclass(frozen=True)
class OszSor:
    szo: Szo
    jelentes: Optional[Lathato]
    versek: Tuple[Igehely, ...]
    cellak: Tuple[OkoriCella, ...]       # Targum, Vulgata, LXX
    mondatok: Tuple['Mondat', ...]       # a „Mit mutat” cella mondatai, sorrendben


class BetoldasFajta(enum.Enum):
    BETOLDAS = 'betoldas'
    NINCS_BETOLDAS = 'nincs_betoldas'
    NINCS_ADAT = 'nincs_adat'


@dataclasses.dataclass(frozen=True)
class BetoldasCella:
    fajta: BetoldasFajta
    alak: Optional[Lathato]
    kiejtes: Optional[Lathato]
    jelentes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class BetoldasSor:
    hely: Igehely
    szo: Szo
    jelentes: Optional[Lathato]          # a héber szó rövid jelentése; híján a Strong-szám áll
    cellak: Tuple[BetoldasCella, ...]
    betoldok: Tuple[Forditas, ...]


@dataclasses.dataclass(frozen=True)
class OszTabla:
    szopar: bool
    mag_hely: Optional[Igehely]          # a lánc magjának egy verse (a könyv neve ebből), szópárnál None
    mag_elso: int
    mag_utolso: int
    sorok: Tuple[OszSor, ...]
    betoldasok: Tuple[BetoldasSor, ...]
    teljes: Tuple[int, ...]              # Targum, Vulgata, LXX: hány lánc-szót ad vissza minden versben egy szóval
    egyverses: Tuple[Szo, ...]
    par: Optional[Szo]                   # szópárnál a formula másik szava


@dataclasses.dataclass(frozen=True)
class UszVulgata:
    hely: Igehely
    alakok: Tuple[Lathato, ...]


@dataclasses.dataclass(frozen=True)
class UszValtozat:
    hely: Igehely
    alak: Lathato
    kiejtes: Optional[Lathato]
    kiadasok: Tuple[Lathato, ...]
    hianyzik: Tuple[Lathato, ...]
    mas: Optional[Lathato]
    mas_kiejtes: Optional[Lathato]


class UszMit(enum.Enum):
    EGYEZO = 'egyezo'           # a latin szócsalád a két szövetségben ugyanaz
    RESZBEN = 'reszben'         # a lánc Septuagintájában csak részben
    CSAK_USZ = 'csak_usz'       # a lánc Septuagintájában nincs összevethető vers
    NINCS = 'nincs'             # nincs latin szócsalád


@dataclasses.dataclass(frozen=True)
class UszSor:
    szavak: Tuple[Szo, ...]
    versek: Tuple[Igehely, ...]
    vulgata: Tuple[UszVulgata, ...]
    n: int
    nn: int
    valtozatok: Tuple[UszValtozat, ...]
    elo_versek: Tuple[Igehely, ...]
    elo_lemmak: Tuple[Lathato, ...]
    mit: UszMit
    csalad: Optional[Lathato]            # a fő latin szócsalád jele (a lemma eleje)
    osz_db: int                          # a lánc Septuagintájának összevethető versei
    osz_n: int                           # ezek közül ennyiben áll a latin szócsalád
    csaladon_belul: bool                 # a szövegváltozat ugyanabban a görög szócsaládban marad


@dataclasses.dataclass(frozen=True)
class UszTabla:
    szopar: bool
    mag_hely: Optional[Igehely]
    tematikus: Tuple[Igehely, ...]
    sorok: Tuple[UszSor, ...]
    egyezo: int
    peshitta: ForrasAllapot


@dataclasses.dataclass(frozen=True)
class Tanu:
    hely: Igehely
    tanu: Lathato
    mu: Lathato
    fejezet: Optional[int]
    resz: Optional[int]
    hagyomany: Kulcs
    kor: Optional[Lathato]
    kapcsolat: Lathato
    targyalt: Tuple[Igehely, ...]        # üres: a tanú a sor helyét tárgyalja (vagy versláncban idézi)
    forras: TanuForras
    lekerdezve: Optional[datetime.date]
    biblindex: bool


@dataclasses.dataclass(frozen=True)
class Tanuk:
    sorok: Tuple[Tanu, ...]
    helyek: int
    glossa: bool


@dataclasses.dataclass(frozen=True)
class Hatastortenet:
    osz: Optional[OszTabla]
    usz: Optional[UszTabla]
    tanuk: Tanuk


# --- az ószövetségi tábla --------------------------------------------------------------------------------------


def _okori_szo(forditas, sor):
    lemma = idezet(szocikkek_sz.tablaban(sor.lemmak[0]))
    if forditas is Forditas.TARGUM:
        kiejtes = sor.kiejtes_gepi
    elif forditas is Forditas.LXX:
        kiejtes = sor.kiejtesek[0] if sor.kiejtesek else None
    else:
        kiejtes = None
    return OkoriSzo(forditas, lemma, idezet(szocikkek_sz.tablaban(kiejtes)) if kiejtes is not None else None)


def _szo_kulcs(szo):
    return (szo.lemma, szo.kiejtes)


def _cella(forditas, sorok_f, versek):
    """A régi `visszhang_cella`: (cella, a fő szócsalád, a fő versek lemmái, az eltérő versek, a szócsaládok
    száma)."""
    nn = len(versek)
    jo = {}
    for r in sorok_f:
        if r.ellenorzott and r.van_alak:
            jo[r.igehely] = r
    ures = {r.igehely for r in sorok_f if r.ellenorzott and not r.van_alak}
    van_sor = {r.igehely for r in sorok_f}

    def hiany(h):
        if h in ures:
            return Hiany.NINCS_SZO
        return Hiany.NINCS_ELLENORZOTT if h in van_sor else Hiany.NINCS_KINYERES

    csaladok = []   # [(kulcs, [versek])] a megjelenés rendjében
    for h in versek:
        r = jo.get(h)
        if r is None:
            continue
        kulcs = next((i for i, (k, _v) in enumerate(csaladok) if k & r.csalad), None)
        if kulcs is None:
            csaladok.append((r.csalad, [h]))
        else:
            csaladok[kulcs][1].append(h)
    if not csaladok:
        fajta_hiany = Hiany.NINCS_ELLENORZOTT if sorok_f else Hiany.NINCS_KINYERES
        return OkoriCella(CellaFajta.NINCS_ADAT, (), 0, nn, fajta_hiany, (), False, ()), None, (), versek, 0
    fo, helyek = max(csaladok, key=lambda x: len(x[1]))
    n = len(helyek)
    lemmak = []
    for h in helyek:
        if jo[h].lemmak[0].ertek not in lemmak:
            lemmak.append(jo[h].lemmak[0].ertek)
    szavak, latott = [], set()
    for h in helyek:
        szo = _okori_szo(forditas, jo[h])
        if _szo_kulcs(szo) not in latott:
            latott.add(_szo_kulcs(szo))
            szavak.append(szo)
    tobbi = tuple(h for h in versek if h not in helyek)
    if n == 1 and len(csaladok) == len(jo) and nn > 1:
        kulonbozo = tuple(Elteres(h, _okori_szo(forditas, jo[h]), None) for h in versek if h in jo)
        return OkoriCella(CellaFajta.KULONBOZO, (), 1, nn, None, kulonbozo, False, ()), None, (), tobbi, len(jo)
    if n == nn:
        return OkoriCella(CellaFajta.TELJES, tuple(szavak), n, nn, None, (), False, ()), fo, tuple(lemmak), (), \
            len(csaladok)
    elteres = tuple(Elteres(h, _okori_szo(forditas, jo[h]), None) if h in jo else Elteres(h, None, hiany(h))
                    for h in tobbi)
    return OkoriCella(CellaFajta.RESZ, tuple(szavak), n, nn, None, elteres, all(h in jo for h in tobbi), ()), fo, \
        tuple(lemmak), tobbi, len(csaladok)


def _alapvonal(arany, nn):
    szazalek = int(round(arany * 100))
    talalat = int(round(arany * nn))
    if arany >= konfig.ALAPVONAL_SZOKASOS:
        sav = Sav.SZOKASOS
    elif arany >= konfig.ALAPVONAL_RITKA:
        sav = Sav.GYAKORI
    else:
        sav = Sav.RITKA
    return Alapvonal(sav, szazalek, nn, talalat)


def _lxx_mondat(e):
    cella = e['cella']
    if not cella.n:
        return LxxMondat(LxxFajta.NINCS_ADAT, cella.hiany, 0, 0, 0, None, False)
    if cella.n < cella.nn:
        return LxxMondat(LxxFajta.ELTERES, None, e['mas'], e['nincs_szo'], e['hianyzo'], None, False)
    if e['alap'][0] is None:
        return LxxMondat(LxxFajta.NEM_MERHETO, None, 0, 0, 0, None, False)
    return LxxMondat(LxxFajta.ALAPVONAL, None, 0, 0, 0, _alapvonal(*e['alap']), len(e['lemmak']) > 1)


def _egyesites(f, szo1, szo2, e1, e2):
    szocsalad = len(set(e1['lemmak'] + e2['lemmak'])) > 1
    if f is not Forditas.LXX:
        return Egyesites((f,), EgyesitesFajta.NEM_MERHETO_FORRAS, (szo1, szo2), szocsalad, ())
    alap = [x['alap'][0] for x in (e1, e2)]
    if any(a is None for a in alap):
        return Egyesites((f,), EgyesitesFajta.NEM_MERHETO, (szo1, szo2), szocsalad, ())
    szazalekok = tuple(int(round(a * 100)) for a in alap)
    if all(a >= konfig.ALAPVONAL_SZOKASOS for a in alap):
        fajta = EgyesitesFajta.SZOKASOS
    elif any(a < konfig.ALAPVONAL_RITKA for a in alap):
        fajta = EgyesitesFajta.RITKA
    else:
        fajta = EgyesitesFajta.GYAKORI
    return Egyesites((f,), fajta, (szo1, szo2), szocsalad, szazalekok)


def _osz(f, motivum):
    """Az ószövetségi tábla (a régi `blokk_visszhang`); None, ha a motívumnak nincs ókori fordítás-sora vagy lánca."""
    okori = ht_be.okori_sorok(f.b, motivum)
    lanc = nyelvi_hatter_sz.lanc_szavak(f, motivum)
    if not okori or not lanc:
        return None
    targum = ht_be.b64_targum(f.b)
    mag = lanc_mag(f.b, motivum, sorted(f.sorok, key=lambda s: s.fajl_sorszam), bemenet.b07_karoli(f.b))
    szopar = mag is None
    szavak = tuple(g for g, _v in lanc)
    lanc_versek = dict(lanc)
    minden = {v for vv in lanc_versek.values() for v in vv}
    betoldas_kulcs = sorted({(r.strong, r.igehely) for r in okori if r.betoldas and r.strong in szavak
                             and r.igehely in minden}, key=lambda k: (k[0].kod, k[1].kod))
    betoldas_halmaz = set(betoldas_kulcs)
    szo_cim = {g: nyelvi_hatter_sz.lanc_szo(f, g, lanc_versek[g]) for g in szavak}
    eredmeny = {}
    for s in szavak:
        versek = lanc_versek[s]
        ss = [r for r in okori if r.strong == s and r.igehely in versek and (s, r.igehely) not in betoldas_halmaz]
        for fd in FORDITASOK:
            fv = tuple(v for v in versek if fd is not Forditas.TARGUM or targum.fedi(v))
            kivul = tuple(v for v in versek if v not in fv)
            sf = [r for r in ss if r.forras == fd.value]
            if not fv:
                cella = OkoriCella(CellaFajta.NINCS_FORRAS, (), 0, 0, None, (), False, kivul)
                fo, lemmak, tobbi = None, (), ()
            else:
                cella, fo, lemmak, tobbi, _kul = _cella(fd, sf, fv)
                if kivul:
                    cella = OkoriCella(cella.fajta, cella.szavak, cella.n, cella.nn, cella.hiany, cella.versek,
                                       cella.mind_mas_szo, kivul)
            alap = (None, 0)
            if fd is Forditas.LXX and fo is not None and cella.n == cella.nn:
                alap = ht_be.lxx_alapvonal(f.b, s, fo, versek)
            mas = sum(1 for h in tobbi if any(r.igehely == h and r.ellenorzott and r.van_alak for r in sf))
            nincs_szo = sum(1 for h in tobbi if not any(r.igehely == h and r.ellenorzott and r.van_alak for r in sf)
                            and any(r.igehely == h and r.ellenorzott and not r.van_alak for r in sf))
            eredmeny[(s, fd)] = {'cella': cella, 'fo': fo, 'lemmak': lemmak, 'alap': alap, 'mas': mas,
                                 'nincs_szo': nincs_szo, 'hianyzo': len(tobbi) - mas - nincs_szo}
    egyesites, utal = {}, {}
    for fd in FORDITASOK:
        for i, s1 in enumerate(szavak):
            for s2 in szavak[i + 1:]:
                e1, e2 = eredmeny[(s1, fd)], eredmeny[(s2, fd)]
                if e1['fo'] is not None and e2['fo'] is not None and e1['cella'].n == e1['cella'].nn \
                        and e2['cella'].n == e2['cella'].nn and e1['fo'] & e2['fo'] and (s1, fd) not in egyesites \
                        and (s2, fd) not in utal:
                    egyesites[(s1, fd)] = _egyesites(fd, szo_cim[s1][0], szo_cim[s2][0], e1, e2)
                    utal[(s2, fd)] = s1
    egyverses = tuple(s for s in szavak if len(lanc_versek[s]) < 2)
    teljes = {fd: 0 for fd in FORDITASOK}
    sorok = []
    for s in szavak:
        mondatok = []
        for fd in FORDITASOK:
            e = eredmeny[(s, fd)]
            if e['cella'].nn and e['cella'].n == e['cella'].nn and s not in egyverses:
                teljes[fd] += 1
            if (s, fd) in egyesites:
                m = Mondat(egyesites=egyesites[(s, fd)])
            elif (s, fd) in utal:
                m = Mondat(utalas=Utalas(szo_cim[utal[(s, fd)]][0]))
            elif fd is Forditas.LXX:
                m = Mondat(lxx=_lxx_mondat(e))
            else:
                continue
            if m not in mondatok:
                mondatok.append(m)
        tv = [m for m in mondatok if m.egyesites is not None and m.egyesites.forditasok[0] is not Forditas.LXX]
        if len(tv) == 2 and (tv[0].egyesites.fajta, tv[0].egyesites.szavak) == (tv[1].egyesites.fajta,
                                                                                 tv[1].egyesites.szavak):
            e0 = tv[0].egyesites
            osszevont = Mondat(egyesites=Egyesites((Forditas.TARGUM, Forditas.VULGATA), e0.fajta, e0.szavak,
                                                   e0.szocsalad, e0.szazalekok))
            mondatok = [osszevont] + [m for m in mondatok if m not in tv]
        szo, jel = szo_cim[s]
        sorok.append(OszSor(szo, jel, lanc_versek[s], tuple(eredmeny[(s, fd)]['cella'] for fd in FORDITASOK),
                            tuple(mondatok)))
    betoldasok = []
    for s, h in betoldas_kulcs:
        cellak, betoldok = [], []
        for fd in FORDITASOK:
            r = next((x for x in okori if x.strong == s and x.igehely == h and x.forras == fd.value), None)
            if r is not None and r.ellenorzott and r.van_alak and r.betoldas:
                cellak.append(BetoldasCella(BetoldasFajta.BETOLDAS, idezet(szocikkek_sz.tablaban(r.alakok[0]))
                                            if len(r.alakok) == 1 else None,
                                            idezet(szocikkek_sz.tablaban(r.alak_kiejtes))
                                            if r.alak_kiejtes is not None else None,
                                            idezet(szocikkek_sz.tablaban(r.jelentes))
                                            if r.jelentes is not None else None))
                if len(r.alakok) != 1:
                    raise bemenet.BemenetHiba('9.: a betoldás sorának alakja nem egyetlen szó (%s, %s)'
                                              % (s.kod, h.kod))
                betoldok.append(fd)
            elif r is not None and r.ellenorzott:
                cellak.append(BetoldasCella(BetoldasFajta.NINCS_BETOLDAS, None, None, None))
            else:
                cellak.append(BetoldasCella(BetoldasFajta.NINCS_ADAT, None, None, None))
        betoldasok.append(BetoldasSor(h, f.szo(s), f.jelentes(s).magyar, tuple(cellak), tuple(betoldok)))
    elso = lanc[0][1][0]
    return OszTabla(szopar=szopar, mag_hely=None if szopar else elso,
                    mag_elso=0 if szopar else mag.elso, mag_utolso=0 if szopar else mag.utolso,
                    sorok=tuple(sorok), betoldasok=tuple(betoldasok),
                    teljes=tuple(teljes[fd] for fd in FORDITASOK),
                    egyverses=tuple(szo_cim[s][0] for s in egyverses),
                    par=_par(f, motivum) if szopar else None)


def _par(f, motivum):
    """A szópáros formula másik szava (a régi `par_nev`): a formula-elem második tagja."""
    for s in sorted(f.sorok, key=lambda x: x.fajl_sorszam):
        reszek = s.gerinc_reszek
        if len(reszek) == 2 and all(isinstance(r, Strong) and r.heber for r in reszek):
            return f.szo(reszek[1])
    return None


# --- az újszövetségi tábla -------------------------------------------------------------------------------------


def _usz(f, motivum, osz_tabla):
    okori = [r for r in ht_be.okori_sorok(f.b, motivum) if r.ellenorzott]
    usz = [r for r in okori if r.forras == konfig.FORRAS_VULGATA and not r.strong.heber]
    if not usz:
        return None
    karoli = bemenet.b07_karoli(f.b)
    sorrend = {}
    for i, s in enumerate(f.sorok):
        for v in karoli.versek(s.igehely):
            sorrend.setdefault(v, i)
    lemma = {}
    for r in usz:
        if r.strong not in lemma:
            gl = ht_be.tagnt_lemma(f.b, r.igehely, r.strong)
            if gl is not None:
                lemma[r.strong] = gl
    strongok = sorted({r.strong for r in usz},
                      key=lambda st: (min(sorrend.get(x.igehely, 999) for x in usz if x.strong == st), st.kod))
    tovek = {st: lemma[st].tovek if st in lemma else frozenset() for st in strongok}
    szarmazas = szotari_be.b42_szarmazas(f.b)
    csoportok = []
    for st in strongok:
        tagok = [c for c in csoportok if any(tovek[st] & tovek[x] or szarmazas.get(st.kod) == x.kod
                                             or szarmazas.get(x.kod) == st.kod for x in c[1])]
        cs_tovek, cs_strongok = set(tovek[st]), [st]
        for c in tagok:
            cs_strongok = c[1] + cs_strongok
            cs_tovek |= c[0]
            csoportok.remove(c)
        cs_strongok.sort(key=strongok.index)
        csoportok.append((cs_tovek, cs_strongok))
    csoportok.sort(key=lambda c: min(strongok.index(x) for x in c[1]))
    lanc = nyelvi_hatter_sz.lanc_szavak(f, motivum)
    lanc_par = {(s, v) for s, vv in lanc for v in vv}
    lxx = [r for r in okori if r.forras == konfig.FORRAS_LXX and r.van_alak and r.van_lemma
           and (r.strong, r.igehely) in lanc_par]
    osz_vulg = {(r.strong, r.igehely): r for r in okori if r.forras == konfig.FORRAS_VULGATA and r.strong.heber}
    valtozatok = ht_be.b41_valtozatok(f.b)
    kiejtes = f.kiejtes
    konyvek = f.konyvek
    sorok, egyezo = [], 0
    for cs_tovek, cs_strongok in csoportok:
        sorok_cs = sorted([r for r in usz if r.strong in cs_strongok], key=lambda r: sorrend.get(r.igehely, 999))
        versek = tuple(dict.fromkeys(r.igehely for r in sorok_cs))
        szavak = []
        for st in cs_strongok:
            gl = lemma.get(st)
            alak = idezet(szocikkek_sz.tablaban(gl.lemma)) if gl is not None else None
            k = kiejtes.gorog_gepi(gl.lemma) if gl is not None else None
            szavak.append(Szo(st, alak, idezet(szocikkek_sz.tablaban(k)) if k is not None else None))
        csal = {}
        jelek = {}
        for r in sorok_cs:
            sajat = set()
            for kulcs, jel in r.latin_jelek:
                if kulcs in sajat:
                    continue
                sajat.add(kulcs)
                csal[kulcs] = csal.get(kulcs, 0) + 1
                jelek.setdefault(kulcs, jel)
        fo = max(csal, key=lambda k: (csal[k], -list(csal).index(k))) if csal else None
        vv = {}
        for r in sorok_cs:
            vv.setdefault(r.igehely, []).append(r)
        n = sum(1 for rr in vv.values() if any(fo in r.latin_csalad for r in rr))
        vulg = tuple(UszVulgata(v, tuple(idezet(szocikkek_sz.tablaban(a)) for r in rr for a in r.alakok))
                     for v, rr in vv.items())
        valt, belul = [], False
        for v in versek:
            for x in valtozatok.versben(v, cs_strongok):
                valt.append(UszValtozat(v, idezet(szocikkek_sz.tablaban(x.alak)), _gepi(kiejtes, x.alak),
                                        tuple(idezet(k) for k in x.kiadasok), tuple(idezet(k) for k in x.hianyzik),
                                        idezet(szocikkek_sz.tablaban(x.mas)) if x.mas is not None else None,
                                        _gepi(kiejtes, x.mas) if x.mas is not None else None))
                if x.mas is not None and x.mas_tovek & cs_tovek:
                    belul = True
        elo = [r for r in lxx if r.tovek & cs_tovek]
        elo_versek = tuple(sorted(dict.fromkeys(r.igehely for r in elo), key=konyvek.rendezo_kulcs))
        elo_lemmak, latott = [], set()
        for r in elo:
            for x in r.lemmak:
                if x.ertek not in latott:
                    latott.add(x.ertek)
                    elo_lemmak.append(idezet(szocikkek_sz.tablaban(x)))
        osz = [osz_vulg.get((r.strong, r.igehely)) for r in elo]
        osz = [r for r in osz if r is not None and r.van_alak]
        osz_n = sum(1 for r in osz if fo is not None and fo in r.latin_csalad)
        if fo is not None and n == len(vv) and osz and osz_n == len(osz):
            mit = UszMit.EGYEZO
            egyezo += 1
        elif fo is not None and osz:
            mit = UszMit.RESZBEN
        elif fo is not None:
            mit = UszMit.CSAK_USZ
        else:
            mit = UszMit.NINCS
        sorok.append(UszSor(szavak=tuple(szavak), versek=versek, vulgata=vulg, n=n, nn=len(vv),
                            valtozatok=tuple(valt), elo_versek=elo_versek, elo_lemmak=tuple(elo_lemmak), mit=mit,
                            csalad=idezet(jelek[fo]) if fo is not None else None, osz_db=len(osz), osz_n=osz_n,
                            csaladon_belul=belul))
    tematikus = tuple(s.igehely for s in f.sorok if s.tematikus and konyvek.ujszovetsegi(s.igehely.konyv))
    szopar = osz_tabla is not None and osz_tabla.szopar
    return UszTabla(szopar=szopar, mag_hely=None if szopar or osz_tabla is None else osz_tabla.mag_hely,
                    tematikus=tematikus, sorok=tuple(sorok), egyezo=egyezo, peshitta=ht_be.b73_peshitta(f.b))


def _gepi(kiejtes, alak):
    k = kiejtes.gorog_gepi(alak)
    return idezet(szocikkek_sz.tablaban(k)) if k is not None else None


# --- a tanúk ------------------------------------------------------------------------------------------------


def _tanuk(f, motivum):
    """A lapra kerülő tanúk (a régi `tanuk_lapra`): ellenőrzött sor, Remez- vagy Sod-szintű hely, hagyományonként
    helyenként legfeljebb egy, a helyek sorrendjében."""
    szint = {}
    sorrend = {}
    for i, s in enumerate(f.sorok):
        szint[s.igehely] = s.pardes_szintek
        sorrend[s.igehely] = i
    hagy = konfig.TANU_HAGYOMANYOK
    jo = [r for r in ht_be.b39_tanuk(f.b, motivum) if r.ellenorzott
          and any(sz.ertek in konfig.TANU_SZINTEK for sz in szint.get(r.igehely, ()))]
    latott, tanuk = set(), []
    for r in sorted(jo, key=lambda r: (sorrend.get(r.igehely, 999), hagy.index(r.hagyomany.ertek))):
        if (r.igehely, r.hagyomany.ertek) in latott:
            continue
        latott.add((r.igehely, r.hagyomany.ertek))
        targyalt = () if r.forras is TanuForras.CHAIN_LINEAGE or r.tanu_helyek in ((), (r.igehely,)) \
            else r.tanu_helyek
        tanuk.append(Tanu(hely=r.igehely, tanu=proza(szocikkek_sz.tablaban(r.tanu)),
                          mu=idezet(szocikkek_sz.tablaban(r.mu)), fejezet=r.fejezet, resz=r.resz,
                          hagyomany=r.hagyomany,
                          kor=proza(szocikkek_sz.tablaban(r.kor)) if r.kor is not None else None,
                          kapcsolat=proza(szocikkek_sz.tablaban(r.kapcsolat)), targyalt=targyalt, forras=r.forras,
                          lekerdezve=r.lekerdezve, biblindex=r.biblindex))
    return Tanuk(tuple(tanuk), len({t.hely for t in tanuk}), any(t.forras is TanuForras.GLOSSA for t in tanuk))


def szamit(korny):
    """A 9. szakasz modellje."""
    f = szocikkek_sz.forrasok(korny.b, korny.motivum)
    osz = _osz(f, korny.motivum)
    return Hatastortenet(osz=osz, usz=_usz(f, korny.motivum, osz), tanuk=_tanuk(f, korny.motivum))
