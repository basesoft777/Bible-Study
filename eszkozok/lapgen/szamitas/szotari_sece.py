"""lapgen.szamitas.szotari_sece — a „Megfelelők a másik nyelven” pont: a kétnyelvű szótár (SECE) megfelelői.

Két rész: (1) a híd a motívum héber és görög szavai között (mely szó megfelelője a motívum saját szava a másik
nyelven; héber szónál a görög megfelelő szócsaládja is számít), (2) szavanként a megfelelők táblája (szó, kiejtés,
Strong-szám, rövid jelentés). A szótár csak a szóalakot adja: a Strong-szám a rövid szótárak lemmáiból és a
kétnyelvű szótár címszavaiból párosul. Mondatot nem fogalmaz: azt a megjelenítő teszi a sablontáblából.
"""
import dataclasses
import enum
from typing import Optional, Tuple

from lapgen import konfig
from lapgen.bemenet import szotari as szotari_be
from lapgen.szamitas.szotari_tipusok import Jelentes, Szo
from lapgen.szoveg import Igehely, Lathato, Strong, idezet


class Maradek(enum.Enum):
    """A híd záró mondata: minden szónak van kapcsolata; a többinek nincs; egyiknek sincs."""
    NINCS = 'nincs'
    TOBBI = 'tobbi'
    MIND = 'mind'


@dataclasses.dataclass(frozen=True)
class SeceSor:
    """A megfelelők táblájának egy sora. Üres `strongok`: a szóalakhoz nem párosul Strong-szám."""
    szo: Lathato
    motivum_szava: bool
    kiejtes: Optional[Lathato]
    strongok: Tuple[Strong, ...]
    jelentesek: Tuple[Jelentes, ...]   # a Strong-számok rendjében


@dataclasses.dataclass(frozen=True)
class SeceTabla:
    """Egy szó megfelelői; `sorok` None: a szótár a szóra nem ad megfelelő-listát."""
    szo: Szo
    sorok: Optional[Tuple[SeceSor, ...]]


@dataclasses.dataclass(frozen=True)
class JelentesesSzo:
    szo: Szo
    jelentes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class HidCsalad:
    """Héber szó, amelynek görög megfelelője nem a motívum szava, de a szócsaládjából a motívum szavai állnak az
    Újszövetségben."""
    szo: Szo
    megfelelo: JelentesesSzo
    tagok: Tuple[JelentesesSzo, ...]
    helyek: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class HidPontos:
    """Szavak, amelyeknek a megfelelője a motívum saját szava a másik nyelven; `tovabbi`: a helyek listája csonka."""
    szavak: Tuple[Szo, ...]
    megfelelok: Tuple[Szo, ...]
    helyek: Tuple[Igehely, ...]
    tovabbi: bool


@dataclasses.dataclass(frozen=True)
class Sece:
    csaladok: Tuple[HidCsalad, ...]
    pontosak: Tuple[HidPontos, ...]
    maradek: Maradek
    tablak: Tuple[SeceTabla, ...]


class _Szamolo:
    def __init__(self, f, szavak):
        self.f = f
        self.sece = szotari_be.b28_sece(f.b)
        self.index = szotari_be.lemma_strong_index(f.b, f.kiejtes.lemmak())
        self.szarmazas = szotari_be.b42_szarmazas(f.b)
        self.sajat = frozenset(szavak)
        # a motívum szavai az előfordulás-tábla rendjében (az első előfordulásuk szerint)
        self.rendben = []
        for sor in sorted(f.sorok, key=lambda s: s.fajl_sorszam):
            self.rendben.extend(st for st in sor.strongok if st not in self.rendben)

    def parosul(self, alak, masik_heber):
        """A szóalakhoz párosuló Strong-számok a másik nyelven."""
        return tuple(Strong(kod) for kod in self.index.get(szotari_be.nfc(alak.ertek), ())
                     if kod.startswith('H') == masik_heber)

    def megfelelo_strongok(self, strong):
        """A szó megfelelőinek Strong-számai a szótár rendjében, ismétlés nélkül."""
        ki = []
        for alak in self.sece.megfelelok(strong) or ():
            ki.extend(st for st in self.parosul(alak, not strong.heber) if st not in ki)
        return ki

    def csalad(self, a, b):
        """Egy szócsaládba tartozik-e a két görög szó: közös tő, vagy az egyik a másik származéka."""
        ta, tb = self.f.kiejtes.gorog_tovek(a), self.f.kiejtes.gorog_tovek(b)
        if ta is None or tb is None:
            return False
        return bool(ta & tb) or self.szarmazas.get(a.kod) == b.kod or self.szarmazas.get(b.kod) == a.kod

    def helyek(self, strongok, ujszovetsegi):
        """A szavak helyei a megnevezett szövetségben, a tábla rendjében, ismétlés nélkül."""
        ki = []
        for strong in strongok:
            for sor in sorted(self.f.sorok, key=lambda s: s.fajl_sorszam):
                if strong in sor.strongok and self.f.konyvek.ujszovetsegi(sor.igehely.konyv) == ujszovetsegi \
                        and sor.igehely not in ki:
                    ki.append(sor.igehely)
        return ki

    def jelenteses(self, strong):
        magyar = self.f.rovid.jelentes(strong).magyar   # a mondatban csak a magyar jelentés áll; hiánya nem jelölt
        return JelentesesSzo(self.f.szo(strong), idezet(self.f.tablaban(magyar)) if magyar is not None else None)

    def tabla(self, strong):
        megfelelok = self.sece.megfelelok(strong)
        if megfelelok is None:
            return SeceTabla(self.f.szo(strong), None)
        sorok = []
        for alak in megfelelok:
            strongok = self.parosul(alak, not strong.heber)
            kiejtes = self.f.kiejtes.alak_kiejtes(strongok[0], alak, self.f.versek) if strongok else None
            sorok.append(SeceSor(
                szo=idezet(self.f.tablaban(alak)), motivum_szava=any(st in self.sajat for st in strongok),
                kiejtes=idezet(self.f.tablaban(kiejtes)) if kiejtes is not None else None,
                strongok=strongok, jelentesek=tuple(self.f.jelentes(st) for st in strongok)))
        return SeceTabla(self.f.szo(strong), tuple(sorok))


def szamit(f, nyelv_heber, sajat, szavak):
    """A pont modellje egy nyelv szavaira (`sajat`); `szavak`: a motívum minden szava."""
    sz = _Szamolo(f, szavak)
    masik = [st for st in sz.rendben if st.heber != nyelv_heber]
    csaladok, csoportok, van = [], {}, 0
    for strong in sajat:
        megfelelok = sz.megfelelo_strongok(strong)
        pontos = tuple(st for st in megfelelok if st in masik)
        if pontos:
            csoportok.setdefault(pontos, []).append(strong)
            van += 1
            continue
        if nyelv_heber:
            csaladi = [e for e in megfelelok if any(sz.csalad(e, g) for g in masik)]
            if csaladi:
                tagok = [g for g in masik if sz.csalad(csaladi[0], g)]
                csaladok.append(HidCsalad(
                    szo=f.szo(strong), megfelelo=sz.jelenteses(csaladi[0]),
                    tagok=tuple(sz.jelenteses(g) for g in tagok),
                    helyek=tuple(sz.helyek(tagok, True)[:konfig.HID_HELYEK])))
                van += 1
    pontosak = []
    for pontos, tagok in csoportok.items():
        helyek = sz.helyek(pontos, nyelv_heber)
        pontosak.append(HidPontos(
            szavak=tuple(f.szo(st) for st in tagok), megfelelok=tuple(f.szo(st) for st in pontos),
            helyek=tuple(helyek[:konfig.HID_HELYEK]), tovabbi=len(helyek) > konfig.HID_HELYEK))
    maradek = Maradek.NINCS if van >= len(sajat) else (Maradek.TOBBI if van else Maradek.MIND)
    return Sece(tuple(csaladok), tuple(pontosak), maradek, tuple(sz.tabla(strong) for strong in sajat))
