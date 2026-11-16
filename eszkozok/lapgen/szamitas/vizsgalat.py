"""lapgen.szamitas.vizsgalat — a vizsgálat számai: mi tartozik a motívumhoz, mi esett ki és miért.

Közös modell a „Döntési út” szakaszhoz és a kizárt versek mellékletéhez: mindkettő ebből számol, ezért a számaik
egyeznek. Minden vers egyszer számít: a motívum versei, a csoportosan kizárt versek, az egyenként elutasított
versek és a döntésre váró versek egymást kizáró halmazok.

A kapu (`kapu`) a modellen fut, nem a kiírt szövegen: a számok összeadódnak, a csoportos okok verslistája
igazolja a versszámot, egy vers sem áll kétszer, és a motívum verse nem áll a kizártak között.
"""
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import dontes as dontes_be
from lapgen.bemenet.dontes import Dontes
from lapgen.szoveg import Igehely, Kulcs, Lathato, Proveniencia, idezet, prov, proza


class KapuHiba(bemenet.BemenetHiba):
    """BUKÁS: a lapmodell számai nem egyeznek. A lap nem íródik ki."""


_HTML_JELEK = ('<', '>', '&')


def html_ben(burkolo):
    """Kapu a HTML-jelölésű (lenyíló) blokkba kerülő kézi szövegre és idézetre: `<`, `>` vagy `&` jel nem állhat
    benne. A generátor a szöveget nem írja át, így át sem kódolja: az ilyen szöveg a forrásban javítandó."""
    if burkolo is not None and any(jel in burkolo.ertek for jel in _HTML_JELEK):
        raise bemenet.BemenetHiba('a(z) `%s` mező szövege HTML-jelet tartalmaz (<, > vagy &), ezért lenyíló blokkba '
                                  'nem kerülhet: %s' % (burkolo.mezo, burkolo.ertek[:80]))
    return burkolo


@dataclasses.dataclass(frozen=True)
class Pelda:
    """Egy csoportosan kizárt vers példaként: az igehely és a Károli-szövege."""
    igehely: Igehely
    szoveg: Lathato


@dataclasses.dataclass(frozen=True)
class OkCsoport:
    """Egy elutasítási ok versei. `versszam`: a döntésnaplóból számolt versszám; `versek`: a versek listája
    (csoportos oknál a csoportlistából, egyenkénti oknál a döntésnaplóból)."""
    ok: Lathato
    leiras: Lathato
    versszam: int
    versek: Tuple[Igehely, ...]
    peldak: Tuple[Pelda, ...] = ()


@dataclasses.dataclass(frozen=True)
class Kereses:
    """A teljesség-mérés egy keresése: a kulcsa (olvasói neve a névtáblában), a versszáma és a forrássora."""
    kulcs: Kulcs
    versszam: int
    forrassor: Proveniencia


@dataclasses.dataclass(frozen=True)
class Vizsgalat:
    bent: int                                   # a motívum versei (a tartomány-sorok versenként)
    helyek: int                                 # a motívum helyei (előfordulás-sorok)
    csoport: int                                # csoportosan kizárt versek
    egyen: int                                  # egyenként elbírált és elutasított versek
    nyitva: int                                 # döntésre váró versek
    osszes: int                                 # megvizsgált versek, minden vers egyszer
    ajanlas: int                                # kereszthivatkozás-gyűjtemény ajánlásából jött versek
    bent_versek: Tuple[Igehely, ...]
    csoport_okok: Tuple[OkCsoport, ...]
    egyen_okok: Tuple[OkCsoport, ...]
    keresesek: Optional[Tuple[Kereses, ...]]    # None: a motívumnak nincs teljesség-mérése (kimondott hiány)


def _tagok(jelolt, lista, kulon):
    """A csoportos sor tagjai a csoportlistából; None, ha a lista nem igazolja a sor versszámát."""
    if jelolt.osszesito_versszam is None:
        raise bemenet.BemenetHiba('B04: a csoportos sor indoklása nem nevezi meg a versszámot: %s'
                                  % jelolt.igehely.kod)
    if lista is None or jelolt.lista_blokk is None:
        return None
    tagok = [t for t in lista.tagok(jelolt.lista_oszlop, jelolt.lista_blokk, jelolt.lista_halo) if t not in kulon]
    if len(tagok) != jelolt.osszesito_versszam or len(tagok) != jelolt.csoport_versszam:
        return None
    return tagok


def _okcsoport(ok, versszam, versek, peldak=()):
    html_ben(ok.cimke)
    html_ben(ok.megjegyzes)
    return OkCsoport(ok=proza(ok.cimke), leiras=proza(ok.megjegyzes if ok.megjegyzes is not None else ok.cimke),
                     versszam=versszam, versek=tuple(dontes_be.vers_igehely(v) for v in versek), peldak=tuple(peldak))


def szamit(korny):
    """A vizsgálat modellje a döntésnaplóból, az előfordulás-sorokból és a teljesség-mérésből."""
    b, motivum = korny.b, korny.motivum
    sorok = bemenet.b03_elofordulasok(b, motivum)
    jeloltek = dontes_be.b04_jeloltek(b, motivum)
    okok = dontes_be.b56_okok(b, motivum)
    karoli = bemenet.b07_karoli(b)
    mai_strongok = frozenset(strong.kod for sor in sorok for strong in sor.strongok)
    keresesek = dontes_be.b05_teljesseg(b, motivum, mai_strongok)
    lista = dontes_be.b06_csoportlista(b, motivum)
    donteses = (Dontes.ELUTASITVA, Dontes.NYITVA)

    bent = []
    for sor in sorok:
        bent.extend(v for v in dontes_be.tartomany_versei(sor.igehely.kod) if v not in bent)
    bent_halmaz = frozenset(bent)

    # a csoportos sorok egyedi tagjai: a két csoportban is álló vers a döntésnaplóban előbb álló csoportnál számít
    kulon = frozenset(j.igehely.kod for j in jeloltek if j.kulon_sor and j.osszesito_versszam is None)
    latott, egyedi = set(), {}
    for j in jeloltek:
        if j.csoport_versszam is None or j.dontes not in donteses:
            continue
        tagok = _tagok(j, lista, kulon)
        if tagok is None:
            egyedi[j.igehely.kod] = (j.csoport_versszam, None)
            continue
        ujak = [t for t in tagok if t not in latott]
        latott.update(ujak)
        egyedi[j.igehely.kod] = (len(ujak), ujak)

    ok_szerint, csoport_db, csoport_tagok, csoport_peldak, egyen = {}, {}, {}, {}, {}
    csoport = nyitva_csoportos = ajanlas = 0
    for j in jeloltek:
        if j.dontes not in donteses:
            continue
        n = j.csoport_versszam
        if n is not None and j.igehely.kod in egyedi:
            n = egyedi[j.igehely.kod][0]
        ok = okok.besorol(j.indoklas) if j.dontes is Dontes.ELUTASITVA else None
        versei = dontes_be.tartomany_versei(j.igehely.kod)
        if j.ajanlas:
            ajanlas += n or len(versei)
        if n is not None:
            if ok is None:
                nyitva_csoportos += n
                continue
            kulcs = ok.cimke.ertek
            ok_szerint[kulcs] = ok
            csoport += n
            csoport_db[kulcs] = csoport_db.get(kulcs, 0) + n
            tagok = egyedi.get(j.igehely.kod, (n, None))[1]
            if tagok is None:
                raise bemenet.BemenetHiba('B06: %s: a csoport %d versének taglistája nem igazolja a számot'
                                          % (j.igehely.kod, j.csoport_versszam))
            csoport_tagok.setdefault(kulcs, []).extend(tagok)
            csoport_peldak.setdefault(kulcs, []).append(j.igehely)
            continue
        for vers in versei:
            if vers in bent_halmaz:
                continue
            allapot = egyen.setdefault(vers, [set(), None])
            allapot[0].add(j.dontes)
            if ok is not None and allapot[1] is None:
                allapot[1] = ok
    nyitva = nyitva_csoportos + sum(1 for dontesek, _ok in egyen.values() if Dontes.NYITVA in dontesek)
    egyen_versek = {}
    for vers, (dontesek, ok) in egyen.items():
        if Dontes.NYITVA not in dontesek and ok is not None:
            ok_szerint[ok.cimke.ertek] = ok
            egyen_versek.setdefault(ok.cimke.ertek, []).append(vers)
    n_egyen = sum(len(vv) for vv in egyen_versek.values())

    def peldak(kulcs):
        ki = []
        for hely in csoport_peldak[kulcs][:konfig.CSOPORT_PELDA_DB]:
            szoveg = karoli.szoveg(hely)
            if szoveg is not None:
                ki.append(Pelda(hely, idezet(html_ben(szoveg))))
        return ki

    return Vizsgalat(
        bent=len(bent), helyek=len(sorok), csoport=csoport, egyen=n_egyen, nyitva=nyitva,
        osszes=len(bent) + n_egyen + csoport + nyitva, ajanlas=ajanlas,
        bent_versek=tuple(dontes_be.vers_igehely(v) for v in bent),
        csoport_okok=tuple(_okcsoport(ok_szerint[k], n, csoport_tagok[k], peldak(k))
                           for k, n in sorted(csoport_db.items(), key=lambda x: (-x[1], x[0]))),
        egyen_okok=tuple(_okcsoport(ok_szerint[k], len(vv), vv)
                         for k, vv in sorted(egyen_versek.items(), key=lambda x: (-len(x[1]), x[0]))),
        keresesek=None if keresesek is None else tuple(
            Kereses(k.kulcs, k.versszam, prov('{}', k.forrassor)) for k in keresesek))


def kapu(v):
    """A vizsgálat számegyezés-kapuja a modellen (GK-09, GK-21, a melléklet-kapu). Eltérésnél KapuHiba."""
    for ok in v.csoport_okok + v.egyen_okok:
        if len(ok.versek) != ok.versszam:
            raise KapuHiba('a vizsgálat számai nem egyeznek: egy ok verslistája %d vers, a versszáma %d'
                           % (len(ok.versek), ok.versszam))
    kizartak = [vers for ok in v.csoport_okok + v.egyen_okok for vers in ok.versek]
    if len(kizartak) != len(frozenset(kizartak)):
        raise KapuHiba('a vizsgálat számai nem egyeznek: %d kizárt vers többször áll'
                       % (len(kizartak) - len(frozenset(kizartak))))
    if sum(ok.versszam for ok in v.csoport_okok) != v.csoport or sum(ok.versszam for ok in v.egyen_okok) != v.egyen:
        raise KapuHiba('a vizsgálat számai nem egyeznek: az okok versszámainak összege nem a csoportosan kizárt '
                       '(%d) és az egyenként elutasított (%d) versek száma' % (v.csoport, v.egyen))
    if frozenset(kizartak) & frozenset(v.bent_versek):
        raise KapuHiba('a vizsgálat számai nem egyeznek: %d vers a motívumhoz is tartozik, és kizártként is áll'
                       % len(frozenset(kizartak) & frozenset(v.bent_versek)))
    if len(v.bent_versek) != v.bent or v.bent + v.csoport + v.egyen + v.nyitva != v.osszes:
        raise KapuHiba('a vizsgálat számai nem egyeznek: %d + %d + %d + %d nem %d'
                       % (v.bent, v.csoport, v.egyen, v.nyitva, v.osszes))
    return v
