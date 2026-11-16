"""lapgen.szamitas.elofordulas — a „2. Előfordulások” szakasz és a „2.1 Az igehelyek szövege” pont lapmodellje.

Tiszta számítás: a bemeneti réteg típusos soraiból számokat, felsorolás-értékeket, idézeteket és prózát ad;
mondatot nem fogalmaz (azt a megjelenítő teszi a sablontáblából).
"""
import dataclasses
import datetime
from dataclasses import replace as modositott
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import elofordulas as elofordulas_be
from lapgen.bemenet import gerinc as gerinc_be
from lapgen.bemenet import szavak, ubs
from lapgen.ertekek import DbhOk, Igazolas, JegyzetFajta, Megbizhatosag, SzovetsegKod, UbsForras
from lapgen.szamitas import szotari_gerinc
from lapgen.szamitas.szotari_gerinc import TokenJelentes
from lapgen.szoveg import (Horgony, Igehely, Kulcs, Lathato, Nev, Proveniencia, Strong, idezet, prov, prov_fuz,
                           proza)


@dataclasses.dataclass(frozen=True)
class Osszegzes:
    """Az összegző mondat számai és következtetés-kódjai."""
    helyek: int
    osz: int
    usz: int
    konyvek: int
    magas: int
    sulypont_konyv: Optional[Nev]
    sulypont_db: int
    szovetseg: SzovetsegKod
    bizonytalan: bool


@dataclasses.dataclass(frozen=True)
class VersSzoveg:
    """Egy vers Károli-szövege; a `szoveg` hiánya kimondott hiány (a vers nincs a Károliban)."""
    vers: Igehely
    szoveg: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class IgehelyTetel:
    """A 2.1 pont egy tétele: az igehely szövege, a hozzá írt próza és a funkció magyarázata."""
    igehely: Igehely
    horgony: Horgony
    versek: Tuple[VersSzoveg, ...]
    kapcsolodas: Optional[Lathato]
    funkcio: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class SzoAlak:
    """A motívumot hordozó szó a versben: a ragozott alak és a kiejtése."""
    strong: Strong
    alak: Lathato
    kiejtes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class UbsGlossza:
    """Az UBS-cella egy jelentése. `glossza` hiánya: a hivatkozott jelentés nincs a szótár táblájában."""
    glossza: Optional[Lathato]
    forditasra_var: bool
    nem_egyertelmu: bool
    mt_vers: Optional[Igehely]


@dataclasses.dataclass(frozen=True)
class UbsOk:
    """Miért nincs héber UBS-hivatkozás: az ok, és ahol van, a keresett masszoréta vers."""
    ok: DbhOk
    vers: Optional[Igehely]


@dataclasses.dataclass(frozen=True)
class UbsToken:
    strong: Strong
    glosszak: Tuple[UbsGlossza, ...]
    okok: Tuple[UbsOk, ...]


@dataclasses.dataclass(frozen=True)
class UbsCella:
    """Az „UBS-jelentés” cella: szavanként a hivatkozott jelentések; üres `tokenek`: a sornak nincs ilyen szava."""
    forras: UbsForras
    tokenek: Tuple[UbsToken, ...]


@dataclasses.dataclass(frozen=True)
class SorJegyzet:
    """A sor jegyzete: az igazolás, a jegyzet fajtája és a teljes belső leírás (megjegyzésbe kerül)."""
    fajta: JegyzetFajta
    igazolas: Optional[Igazolas]
    ujszovetsegi: bool
    eredeti: Proveniencia


@dataclasses.dataclass(frozen=True)
class ElofordulasSor:
    """A 2. tábla egy sora."""
    igehely: Igehely
    horgony: Horgony
    karoli_szo: Optional[Lathato]
    alakok: Tuple[SzoAlak, ...]
    tematikus_szo_nelkul: bool
    sajat_szo: bool
    funkcio_cimke: Optional[Lathato]
    pardes_szintek: Tuple[Kulcs, ...]
    strongok: Tuple[Strong, ...]
    ubs: UbsCella
    megbizhatosag: Optional[Kulcs]
    azonositas_modja: Optional[Kulcs]
    jelentes: Tuple[TokenJelentes, ...]
    jegyzet: Optional[SorJegyzet]


@dataclasses.dataclass(frozen=True)
class ElofordulasSzakasz:
    osszegzes: Osszegzes
    jelentes_dontes: datetime.date
    ubs_dontes: datetime.date
    szopar: bool
    sorok: Tuple[ElofordulasSor, ...]
    kozos_olvasoi: Optional[Proveniencia]
    kozos_eredeti: Optional[Proveniencia]
    tetelek: Tuple[IgehelyTetel, ...]


def _osszegzes(sorok, konyvek):
    n = len(sorok)
    usz = sum(1 for s in sorok if konyvek.ujszovetsegi(s.igehely.konyv))
    osz = n - usz
    konyv_db = {}
    for s in sorok:
        konyv_db[s.igehely.konyv] = konyv_db.get(s.igehely.konyv, 0) + 1
    rangsor = sorted(konyv_db.items(), key=lambda x: (-x[1], x[0]))
    magas = sum(1 for s in sorok if s.megbizhatosag is Megbizhatosag.MAGAS)
    sulypont = rangsor[0] if rangsor and rangsor[0][1] / n >= konfig.SULYPONT_KUSZOB else None
    if usz and osz and usz / n < konfig.SZOVETSEG_KUSZOB:
        szovetseg = SzovetsegKod.FOKENT_OSZ
    elif usz and osz and osz / n < konfig.SZOVETSEG_KUSZOB:
        szovetseg = SzovetsegKod.FOKENT_USZ
    elif usz and osz:
        szovetseg = SzovetsegKod.MINDKETTO
    else:
        szovetseg = SzovetsegKod.CSAK_OSZ if osz else SzovetsegKod.CSAK_USZ
    return Osszegzes(
        helyek=n, osz=osz, usz=usz, konyvek=len(konyv_db), magas=magas,
        sulypont_konyv=konyvek.nev(sulypont[0]) if sulypont else None,
        sulypont_db=sulypont[1] if sulypont else 0,
        szovetseg=szovetseg,
        bizonytalan=magas / n < konfig.BIZONYTALAN_KUSZOB)


def _tetel(sor, karoli):
    versek = tuple(VersSzoveg(vers, idezet(karoli.szoveg(vers)) if karoli.van(vers) else None)
                   for vers in karoli.versek(sor.igehely))
    return IgehelyTetel(
        igehely=sor.igehely, horgony=sor.igehely.horgony(), versek=versek,
        kapcsolodas=proza(sor.kapcsolodas) if sor.kapcsolodas else None,
        funkcio=proza(sor.funkcio_magyarazat) if sor.funkcio_magyarazat else None)


class _Forrasok:
    """A sorok számításához kellő bemenetek egy helyen (a függvények paraméterlistája helyett)."""

    def __init__(self, b):
        self.konyvek = bemenet.b63_konyvek(b)
        self.karoli = bemenet.b07_karoli(b)
        self.kiejtes = szavak.kiejtes(b)
        self.forditasok = ubs.b14_forditasok(b)
        self.dntg = ubs.b32_ubs_dntg(b)
        self.dbh = ubs.b33_ubs_dbh(b)
        self.versmegfeleltetes = ubs.b34_versmegfeleltetes(b)
        self.gerinc = gerinc_be.gerinc(b)
        self.szotar_thayer = gerinc_be.SZOTAR_THAYER
        self._b = b

    def utvonal(self, b_id, sorszam=0):
        return self._b.jegyzek_utvonal(b_id, sorszam)

    def szotar_kulcs(self, szotar):
        return self._b.kulcs('B03', 'lexikon_szotar', szotar)


def _alakok(strongok, versek, karoli_szo, f):
    ki = []
    for strong in strongok:
        szo = f.kiejtes.ragozott(versek, strong, karoli_szo if karoli_szo else None)
        if szo is not None:
            ki.append(SzoAlak(strong, idezet(szo.alak), idezet(szo.kiejtes) if szo.kiejtes is not None else None))
    return tuple(ki)


def _glossza(f, szotar, strong, lexid, jelentes_szam, angol, hely):
    """A rövid glossza magyarul a fordítástáblából; ha nincs, az angol eredeti (fordításra vár)."""
    forditas = f.forditasok.forditas(szotar, strong.kod, lexid, jelentes_szam, konfig.UBS_GLOSSZA_MEZO, hely)
    if forditas is None:
        return idezet(angol), True
    if forditas.elavult:
        raise bemenet.BemenetHiba('B14: elavult fordítás az UBS-cellában (%s %s); a jelölése a fordítás-állapot '
                                  'szeletével készül el' % (szotar, strong.kod))
    return idezet(forditas.szoveg), False


def _ubs_dntg(igehely, strongok, usz_versek, f):
    """Újszövetségi sor: szavanként az UBS görög szótár versre hivatkozott jelentései."""
    tartomany = len(usz_versek) > 1
    tokenek = []
    for strong in strongok:
        lexidek = f.dntg.lexidek(usz_versek, strong.kod)
        egyertelmu = len(lexidek) == 1 and not tartomany
        glosszak = []
        for lexid in lexidek:
            jelentes = f.dntg.jelentes(strong.kod, lexid, igehely)
            if jelentes is None or not jelentes[0]:
                continue
            szoveg, var = _glossza(f, konfig.SZOTAR_UBS_DNTG, strong, lexid, jelentes[0], jelentes[1], igehely)
            glosszak.append(UbsGlossza(szoveg, var, not egyertelmu, None))
        tokenek.append(UbsToken(strong, tuple(glosszak), ()))
    return UbsCella(UbsForras.DNTG, tuple(tokenek))


def _ubs_dbh(igehely, strongok, versek, f):
    """Ószövetségi sor: szavanként az UBS héber szótár jelentései, a Károli-vers masszoréta megfelelőjén."""
    tokenek = []
    for strong in strongok:
        if not strong.heber:
            continue
        glosszak, okok = [], []
        for vers in versek:
            mt, ok = f.versmegfeleltetes.mt_vers(vers)
            if mt is None:
                okok.append(UbsOk(ok, None))
                continue
            lexidek = f.dbh.lexidek(strong.kod, mt.kod)
            if not lexidek:
                okok.append(UbsOk(DbhOk.NINCS_HIVATKOZAS, mt))
            for lexid in lexidek:
                angol = f.dbh.glosszak(strong.kod, lexid, igehely)
                if angol is None:
                    elem = UbsGlossza(None, False, False, None)
                else:
                    szoveg, var = _glossza(f, konfig.SZOTAR_UBS_DBH, strong, lexid, konfig.NINCS_JELENTESSZAM,
                                           angol, igehely)
                    elem = UbsGlossza(szoveg, var, False, mt if mt != vers else None)
                if elem not in glosszak:   # tartomány-sornál a versek ugyanazt a jelentést adják
                    glosszak.append(elem)
        tokenek.append(UbsToken(strong, tuple(glosszak), tuple(okok)))
    return UbsCella(UbsForras.DBH, tuple(tokenek))


def _ubs_cella(sor, versek, f):
    """A sor „UBS-jelentés” cellája: újszövetségi sornál a görög, ószövetséginél a héber UBS-szótárból."""
    mutatott = (sor.sajat_szo,) if sor.sajat_szo is not None else sor.strongok
    if sor.tematikus and not sor.strongok and sor.sajat_szo is None:
        return UbsCella(UbsForras.NEM_ALKALMAZHATO, ())
    usz_versek = ubs.usz_versek(sor.igehely, f.konyvek)
    if usz_versek is not None:
        return _ubs_dntg(sor.igehely, mutatott, usz_versek, f)
    return _ubs_dbh(sor.igehely, mutatott, versek, f)


class _UbsForrasok:
    """Az UBS-cella bemenetei (a 2. tábla teljes bemenetkészlete nélkül)."""

    def __init__(self, b):
        self.konyvek = bemenet.b63_konyvek(b)
        self.karoli = bemenet.b07_karoli(b)
        self.forditasok = ubs.b14_forditasok(b)
        self.dntg = ubs.b32_ubs_dntg(b)
        self.dbh = ubs.b33_ubs_dbh(b)
        self.versmegfeleltetes = ubs.b34_versmegfeleltetes(b)


def ubs_cellak(b, sorok):
    """Az előfordulás-sorok UBS-cellái ugyanazzal a számítással, amellyel a 2. tábla készül: [(sor, cella)]. A
    Szótári háttér versenkénti pontja ebből számol, nem a kiírt cella szövegéből."""
    f = _UbsForrasok(b)
    return tuple((sor, _ubs_cella(sor, f.karoli.versek(sor.igehely), f)) for sor in sorok)


def _sor(sor, f):
    versek = f.karoli.versek(sor.igehely)
    mutatott = (sor.sajat_szo,) if sor.sajat_szo is not None else sor.strongok
    szo_nelkul = sor.tematikus and not sor.strongok and sor.sajat_szo is None
    ubs_cella = _ubs_cella(sor, versek, f)
    return ElofordulasSor(
        igehely=sor.igehely, horgony=sor.igehely.horgony(),
        karoli_szo=idezet(sor.karoli_szo) if sor.karoli_szo else None,
        alakok=() if szo_nelkul else _alakok(mutatott, versek, sor.karoli_szo, f),
        tematikus_szo_nelkul=szo_nelkul,
        sajat_szo=sor.sajat_szo is not None,
        funkcio_cimke=proza(sor.funkcio_cimke) if sor.funkcio_cimke else None,
        pardes_szintek=sor.pardes_szintek,
        strongok=mutatott,
        ubs=ubs_cella,
        megbizhatosag=sor.megbizhatosag_kulcs if sor.megbizhatosag_kulcs else None,
        azonositas_modja=sor.azonositas_modja if sor.azonositas_modja else None,
        jelentes=tuple(szotari_gerinc.token_jelentes(f.gerinc, f, sor, strong, versek) for strong in sor.strongok),
        jegyzet=None)


def _jelentes_leiras(sor):
    """A sor jelentéscímkéjének belső leírása (megjegyzésbe kerül), vagy None, ha nincs mit mondani."""
    if not sor.jelentes:
        if sor.sajat_szo and sor.alakok:
            alak = sor.alakok[0]
            szo = prov('{} ({})', alak.alak, alak.kiejtes) if alak.kiejtes is not None else prov('{}', alak.alak)
            return prov('Tematikus hely: a vers {} szava, a {} nem a lánc szava',
                        'héber' if alak.strong.heber else 'görög', szo)
        return prov('a sornak nincs Strong-tokenje')
    reszek = []
    for token in sor.jelentes:
        leiras = prov_fuz('; ', [indok.prov for indok in token.indokok])
        if leiras:
            reszek.append(prov('{} — {}', token.strong, leiras) if len(sor.jelentes) > 1 else leiras)
    return prov_fuz(' · ', reszek) if reszek else None


def _jegyzet_fajta(sor):
    if sor.jelentes:
        return JegyzetFajta.SZOKASOS
    return JegyzetFajta.TEMATIKUS_SAJAT if sor.sajat_szo and sor.alakok else JegyzetFajta.TEMATIKUS


def _jegyzetekkel(sorok_be, sorok, f):
    """A sorok a jegyzetükkel, és a közös forrásmegjelölés két alakja (olvasói és eredeti; mindkettő
    megjegyzésbe kerül). A legalább két jegyzetben álló proveniencia-hármas jelet kap (‹E1›, ‹E2› …, gyakoriság
    szerint), a jegyzetben a helyén a jel áll; a proveniencia nem vész el, csak nem ismétlődik."""
    leirasok = [_jelentes_leiras(sor) for sor in sorok]
    jegyzetes = [bool(be.proveniencia) or bool(be.igazolas_kulcs) or leiras is not None
                 for be, leiras in zip(sorok_be, leirasok)]
    szamlalo, peldany = {}, {}
    for be, van in zip(sorok_be, jegyzetes):
        if not van:
            continue
        for kulcs in {resz.szoveg.ertek for resz in be.prov_reszek if resz.harmas}:
            szamlalo[kulcs] = szamlalo.get(kulcs, 0) + 1
        for resz in be.prov_reszek:
            if resz.harmas:
                peldany.setdefault(resz.szoveg.ertek, resz)
    kozos = [kulcs for kulcs, db in sorted(szamlalo.items(), key=lambda x: (-x[1], x[0]))
             if db >= konfig.KOZOS_PROVENIENCIA_KUSZOB]
    jel = {kulcs: prov('‹E{}›', i) for i, kulcs in enumerate(kozos, start=1)}
    ki, sorszam = [], 0
    for be, sor, leiras, van in zip(sorok_be, sorok, leirasok, jegyzetes):
        if not van:
            ki.append(sor)
            continue
        sorszam += 1
        forras = prov_fuz('', [jel[resz.szoveg.ertek] if resz.harmas and resz.szoveg.ertek in jel else resz.szoveg
                               for resz in be.prov_reszek])
        teljes = prov('proveniencia: {} | igazolas: {}', forras if forras else '—',
                      be.igazolas_kulcs if be.igazolas_kulcs else '—')
        if leiras is not None:
            teljes = prov('{} | jelentés-címke: {}', teljes, leiras)
        ki.append(modositott(sor, jegyzet=SorJegyzet(
            fajta=_jegyzet_fajta(sor), igazolas=be.igazolas,
            ujszovetsegi=f.konyvek.ujszovetsegi(be.igehely.konyv),
            eredeti=prov('[^{}]: {}', sorszam, teljes))))
    if not kozos:
        return tuple(ki), None, None

    def olvasoi(kulcs):
        resz = peldany[kulcs]
        nev = 'kézi szerkesztés' if resz.kezi_szerkesztes else 'a lap munkaanyaga'
        return prov('forrás: {}, {}', nev, resz.datum) if resz.datum is not None else prov('forrás: {}', nev)

    if len(kozos) == 1 and szamlalo[kozos[0]] == sorszam:
        k = kozos[0]
        return (tuple(ki), prov('Minden sor forrásmegjelölése ({}): {}', jel[k], olvasoi(k)),
                prov('*Minden sor forrásmegjelölése ({}): `{}`*', jel[k], peldany[k].szoveg))
    return (tuple(ki),
            prov('A közös forrásmegjelölések: {}', prov_fuz(' · ', [
                prov('{} = {} ({} sor)', jel[k], olvasoi(k), szamlalo[k]) for k in kozos])),
            prov('*A közös forrásmegjelölések: {}*', prov_fuz(' · ', [
                prov('{} = `{}` ({} sor)', jel[k], peldany[k].szoveg, szamlalo[k]) for k in kozos])))


def szamit(korny):
    """A szakasz lapmodellje. Előfordulás nélküli motívumnál BemenetHiba: a szakasz nem állhat üresen."""
    b = korny.b
    sorok = bemenet.b03_elofordulasok(b, korny.motivum)
    if not sorok:
        raise bemenet.BemenetHiba('B03: a motívumnak nincs előfordulás-sora')
    f = _Forrasok(b)
    dontesek = bemenet.b51_dontesek(b)
    modell_sorok, kozos_olvasoi, kozos_eredeti = _jegyzetekkel(sorok, tuple(_sor(sor, f) for sor in sorok), f)
    return ElofordulasSzakasz(
        osszegzes=_osszegzes(sorok, f.konyvek),
        jelentes_dontes=dontesek.datum(konfig.DONTES_JELENTES_FUNKCIO),
        ubs_dontes=dontesek.datum(konfig.DONTES_UBS_SZONEZET),
        szopar=elofordulas_be.szopar_motivum(sorok),
        sorok=modell_sorok,
        kozos_olvasoi=kozos_olvasoi,
        kozos_eredeti=kozos_eredeti,
        tetelek=tuple(_tetel(sor, f.karoli) for sor in sorok))
