"""lapgen.szamitas.kapcsolatok — a „7. Kapcsolatok” szakasz, az Alátámasztás és a „8. Kapcsolódó motívumok” szakasz
lapmodellje (S6).

A 7. szakasz a motívum igehely-párjainak kapcsolatait adja (a tábla sorrendjében), a gráf csomópontjait kánoni
sorrendben, és a típusok, a bizonyosság megoszlásából a következtetést (a régi `blokk_kapcsolatok`,
`olvasoi_kovetkeztetes.kapcsolatok`). Az Alátámasztás az azonos indoklású sorokat egy sorba vonja (a tábla
sorrendjében, az első előfordulás helyén; a régi `adatres_alatamasztas`). A 8. szakasz a motívumközi kapcsolatokat és
a döntésre váró motívumközi jelöltek számát adja (a régi `kapcsolodo_torzs`, `olvasoi_kovetkeztetes.kapcsolodo`).

A számok egyetlen helyen képződnek; a kapuk a modellen ellenőrzik őket.
"""
import dataclasses
import datetime
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import kapcsolat as kapcsolat_be
from lapgen.ertekek import (KapcsolatBiztossag, KapcsolatSzerkezet, KapcsolatTipus, Megbizhatosag,
                            MotivumKapcsolatTipus)
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, Kulcs, Lathato, MotivumId, Proveniencia, prov, prov_fuz, proza


@dataclasses.dataclass(frozen=True)
class KapcsolatSor:
    forras: Igehely
    cel: Igehely
    tipus: KapcsolatTipus
    funkcio: Optional[Lathato]
    bizonyossag: Megbizhatosag
    pardes: Tuple[Kulcs, ...]


@dataclasses.dataclass(frozen=True)
class GrafEl:
    """A gráf egy éle: a forrás és a cél csomópontjának sorszáma (1-től) és a kapcsolat típusa."""
    forras: int
    cel: int
    tipus: KapcsolatTipus


@dataclasses.dataclass(frozen=True)
class AlatSor:
    """Az Alátámasztás egy sora: az azonos indoklású kapcsolatok (forrás, cél) párjai és az indoklás."""
    parok: Tuple[Tuple[Igehely, Igehely], ...]
    indok: Lathato


@dataclasses.dataclass(frozen=True)
class Alatamasztas:
    sorok: Tuple[AlatSor, ...]
    nelkul: Tuple[Tuple[Igehely, Igehely], ...]   # a rögzített indoklás nélküli kapcsolatok
    megjegyzesek: Tuple[Proveniencia, ...]        # az indoklások döntés- és forrásmegjelölése a döntések dátumával


@dataclasses.dataclass(frozen=True)
class KapcsolatSzakasz:
    n: int
    csomopontok: Tuple[Igehely, ...]              # a kapcsolt igehelyek kánoni sorrendben
    sorok: Tuple[KapcsolatSor, ...]
    elek: Tuple[GrafEl, ...]
    tipusok: Tuple[Tuple[KapcsolatTipus, int], ...]   # csökkenő darabszám szerint
    magas: int
    kozepes: int
    alacsony: int
    szerkezet: Optional[KapcsolatSzerkezet]
    fo_tipus: Optional[KapcsolatTipus]
    biztossag: Optional[KapcsolatBiztossag]
    alatamasztas: Alatamasztas


@dataclasses.dataclass(frozen=True)
class MotivumKapcsolatSor:
    masik: MotivumId
    itt: Igehely
    ott: Igehely
    tipus: MotivumKapcsolatTipus
    funkcio: Optional[Lathato]
    bizonyossag: Megbizhatosag
    pardes: Tuple[Kulcs, ...]
    indok: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class KapcsolodoSzakasz:
    sorok: Tuple[MotivumKapcsolatSor, ...]
    motivumok: Tuple[Tuple[MotivumId, int], ...]     # a kapcsolatok száma motívumonként
    tipusok: Tuple[MotivumKapcsolatTipus, ...]       # a előforduló típusok
    csak_szomszedos: bool
    nyitott: Tuple[Tuple[MotivumId, int], ...]       # a döntésre váró motívumközi jelöltek motívumonként
    nyitott_ossz: int
    dontes_datum: datetime.date                     # a motívumközi kapcsolatok döntésének dátuma


def _proza(kezi):
    return proza(kezi) if kezi is not None else None


def _szerkezet(n, tipusok):
    fo_t, fo_n = tipusok[0]
    if fo_t is KapcsolatTipus.BETELJESEDES and fo_n / n >= konfig.KAPCSOLAT_LANC:
        return KapcsolatSzerkezet.LANC
    if fo_n / n >= konfig.KAPCSOLAT_TULNYOMO:
        return (KapcsolatSzerkezet.TULNYOMO_PARHUZAM if fo_t is KapcsolatTipus.PARHUZAM
                else KapcsolatSzerkezet.TULNYOMO)
    return KapcsolatSzerkezet.TOBBFELE


def _biztossag(n, magas, kozepes):
    arany = magas / n
    if arany >= konfig.KAPCSOLAT_SZINTE_MIND:
        return KapcsolatBiztossag.SZINTE_MIND
    if arany >= konfig.KAPCSOLAT_TOBBSEG:
        return KapcsolatBiztossag.TOBBSEG
    if arany >= konfig.KAPCSOLAT_FELE:
        return KapcsolatBiztossag.FELE
    return KapcsolatBiztossag.KOZEPES_TOBBSEG if 2 * kozepes > n else KapcsolatBiztossag.KEVES


def _alatamasztas(b, kapcsolatok):
    csoportok, index, nelkul, farkak, dontesek = [], {}, [], [], set()
    for k in kapcsolatok:
        par = (k.forras, k.cel)
        if k.indok is None:
            nelkul.append(par)
            continue
        kulcs = (k.indok, k.farok)
        if kulcs not in index:
            index[kulcs] = len(csoportok)
            csoportok.append((k.indok, []))
            if k.farok is not None and k.farok not in farkak:
                farkak.append(k.farok)
            dontesek.update(k.dontesek)
        csoportok[index[kulcs]][1].append(par)
    datumok = []
    if dontesek:
        d = bemenet.b51_dontesek(b)
        datumok = sorted({d.datum(x) for x in dontesek})
    megjegyzesek = tuple(prov('{} ({})', f, prov_fuz(', ', datumok)) if datumok else prov('{}', f) for f in farkak)
    return Alatamasztas(sorok=tuple(AlatSor(tuple(parok), proza(indok)) for indok, parok in csoportok),
                        nelkul=tuple(nelkul), megjegyzesek=megjegyzesek)


def szamit(korny):
    """A 7. szakasz és az Alátámasztás modellje."""
    b = korny.b
    kapcsolatok = kapcsolat_be.b45_kapcsolatok(b, korny.motivum)
    konyvek = bemenet.b63_konyvek(b)
    helyek = frozenset(x for k in kapcsolatok for x in (k.forras, k.cel))
    csomopontok = tuple(sorted(helyek, key=lambda h: (konyvek.rendezo_kulcs(h), h.kod)))
    sorszam = {h: i for i, h in enumerate(csomopontok, 1)}
    n = len(kapcsolatok)
    db = {}
    for k in kapcsolatok:
        db[k.tipus] = db.get(k.tipus, 0) + 1
    tipusok = tuple(sorted(db.items(), key=lambda x: (-x[1], x[0].value)))
    magas = sum(1 for k in kapcsolatok if k.bizonyossag is Megbizhatosag.MAGAS)
    kozepes = sum(1 for k in kapcsolatok if k.bizonyossag is Megbizhatosag.KOZEPES)
    return KapcsolatSzakasz(
        n=n, csomopontok=csomopontok,
        sorok=tuple(KapcsolatSor(k.forras, k.cel, k.tipus, _proza(k.funkcio), k.bizonyossag, k.pardes)
                    for k in kapcsolatok),
        elek=tuple(GrafEl(sorszam[k.forras], sorszam[k.cel], k.tipus) for k in kapcsolatok),
        tipusok=tipusok, magas=magas, kozepes=kozepes, alacsony=n - magas - kozepes,
        szerkezet=_szerkezet(n, tipusok) if n else None, fo_tipus=tipusok[0][0] if n else None,
        biztossag=_biztossag(n, magas, kozepes) if n else None,
        alatamasztas=_alatamasztas(b, kapcsolatok))


def kapu(m):
    """A 7. szakasz számegyezése a modellen: a típusok és a bizonyossági szintek összege a kapcsolatok száma; minden
    él két csomópontja létező, és minden csomópont legalább egy élen áll; az Alátámasztás minden kapcsolatot pontosan
    egyszer sorol fel (soraiban vagy az indoklás nélküliek között). Eltérésnél KapuHiba."""
    if sum(db for _t, db in m.tipusok) != m.n or m.magas + m.kozepes + m.alacsony != m.n or m.alacsony < 0:
        raise KapuHiba('7.: a típusok vagy a bizonyossági szintek összege nem a kapcsolatok száma (%d)' % m.n)
    if len(m.elek) != m.n or any(not (1 <= e.forras <= len(m.csomopontok) and 1 <= e.cel <= len(m.csomopontok))
                                 for e in m.elek):
        raise KapuHiba('7.: a gráf élei nem a kapcsolatok, vagy nem létező csomópontra mutatnak')
    if {i for e in m.elek for i in (e.forras, e.cel)} != set(range(1, len(m.csomopontok) + 1)):
        raise KapuHiba('7.: a gráfnak van él nélküli csomópontja')
    a = m.alatamasztas
    felsorolt = [p for s in a.sorok for p in s.parok] + list(a.nelkul)
    if sorted(felsorolt, key=lambda p: (p[0].kod, p[1].kod)) != sorted(((s.forras, s.cel) for s in m.sorok),
                                                                     key=lambda p: (p[0].kod, p[1].kod)):
        raise KapuHiba('Alátámasztás: a felsorolt párok nem pontosan a 7. szakasz kapcsolatai')
    return m


def szamit_kapcsolodo(korny):
    """A 8. szakasz modellje."""
    b = korny.b
    sorok = tuple(MotivumKapcsolatSor(r.masik, r.itt, r.ott, r.tipus, _proza(r.funkcio), r.bizonyossag, r.pardes,
                                      _proza(r.indok))
                  for r in kapcsolat_be.b46_motivum_kapcsolatok(b, korny.motivum))
    db = {}
    for r in sorok:
        db[r.masik] = db.get(r.masik, 0) + 1
    tipusok = tuple(sorted({r.tipus for r in sorok}, key=lambda t: t.value))
    nyitott = kapcsolat_be.motivumkozi_nyitott(b, korny.motivum)
    return KapcsolodoSzakasz(
        sorok=sorok, motivumok=tuple(sorted(db.items(), key=lambda x: x[0].kod)), tipusok=tipusok,
        csak_szomszedos=tipusok == (MotivumKapcsolatTipus.SZOMSZEDOS,), nyitott=nyitott,
        nyitott_ossz=sum(x for _m, x in nyitott),
        dontes_datum=bemenet.b51_dontesek(b).datum(konfig.DONTES_MOTIVUMKOZI))


def kapu_kapcsolodo(m):
    """A 8. szakasz számegyezése: a motívumonkénti darabszámok összege a sorok száma, illetve a döntésre váró
    jelöltek összege a kimondott szám. Eltérésnél KapuHiba."""
    if sum(x for _m, x in m.motivumok) != len(m.sorok) or sum(x for _m, x in m.nyitott) != m.nyitott_ossz:
        raise KapuHiba('8.: a motívumonkénti darabszámok összege nem egyezik')
    return m
