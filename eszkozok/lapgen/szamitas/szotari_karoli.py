"""lapgen.szamitas.szotari_karoli — a Károli-fordítás magyar szavai: a 4.13 (Károli-megfelelők) és a 4.14
(rejtett és hamis párhuzam) pont lapmodellje.

A motívum szava itt a motívumsor Strong-kombinációja (egy szó vagy szókapcsolat). A magyar szó szótári alakja a
Károli-szavak szótári alaktáblájából jön; a táblából hiányzó ragozott alak a vele egyező gyakoribb szótári alakba
olvad. A **kulcsszó** az a szótári alak, amely egy szó motívumhelyeinek legalább felében áll (legalább
`KULCS_MIN_SOR` helyen álló szónál), és amelyet a Károli–Strong párosítás nem csak más szóhoz köt. Ezzel mérhető
a **rejtett párhuzam** (a motívum szava áll, a kulcsszó nem) és a **hamis párhuzam** (a kulcsszó áll, a motívum
szava nem). A párosítás minden párja számít, szűrő és páronkénti jelölés nélkül (GK-19).

Mondatot a modul nem fogalmaz: a megjelenítő teszi a sablontáblából. A megjegyzésbe kerülő proveniencia itt
készül (a régi lap megjegyzésével egyező szerkezetben).
"""
import collections
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import karoli_szo as karoli_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.szamitas.szotari_tipusok import Szo
from lapgen.szoveg import Igehely, Lathato, Proveniencia, Strong, idezet, prov, prov_fuz


@dataclasses.dataclass(frozen=True)
class Megfelelo:
    """Egy magyar szócsalád: a szótári alak, a motívum helyein álló szóalakok és az igehelyek."""
    alak: Lathato
    szoalakok: Tuple[Lathato, ...]
    helyek: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class SzoMeres:
    """A motívum egy szava (vagy szókapcsolata) a magyar fordításban: a helyei száma, a leggyakoribb magyar szó
    és annak helyei."""
    szavak: Tuple[Szo, ...]
    helyek: int
    leggyakoribb: Lathato
    leggyakoribb_helyek: int


@dataclasses.dataclass(frozen=True)
class Megfelelok:
    """A 4.13 pont. A `merheto` a legalább `KAROLI_MIN_HELY` helyen álló szavak; közülük az `allando` szavakat a
    Károli többnyire ugyanazzal a magyar szóval fordítja, a `valtozo` szavakat váltakozó szavakkal."""
    hely_szam: int
    csaladok: Tuple[Megfelelo, ...]
    merheto: Tuple[SzoMeres, ...]
    tobbi: int
    allando: Tuple[Tuple[Szo, ...], ...]
    valtozo: Tuple[Tuple[Szo, ...], ...]
    eredeti: Proveniencia


@dataclasses.dataclass(frozen=True)
class Kulcsszavas:
    """A motívum egy szava a magyar kulcsszavaival."""
    szavak: Tuple[Szo, ...]
    kulcsszavak: Tuple[Lathato, ...]


@dataclasses.dataclass(frozen=True)
class Rejtett:
    """Rejtett párhuzam: a motívum helye, ahol a Károli nem a kulcsszóval fordít."""
    igehely: Igehely
    karoli_szo: Lathato
    szavak: Tuple[Szo, ...]
    hianyzo: Tuple[Lathato, ...]


@dataclasses.dataclass(frozen=True)
class HamisVers:
    """Hamis párhuzam egy verse; a `szavak` a motívum versben álló (másik) szavai."""
    vers: Igehely
    szavak: Tuple[Szo, ...]


@dataclasses.dataclass(frozen=True)
class HamisKonyv:
    elso: Igehely
    versek: Tuple[HamisVers, ...]


@dataclasses.dataclass(frozen=True)
class Mogott:
    """A hamis párhuzam verseiben a kulcsszó mögött leggyakrabban álló eredeti szó."""
    kulcsszo: Lathato
    szo: Szo
    versek: int


@dataclasses.dataclass(frozen=True)
class Parhuzam:
    """A 4.14 pont. Kulcsszó nélkül (`kulcsok` üres) a vizsgálat eredménye üres: a pont csak ezt mondja ki."""
    szavak_szama: int
    kulcsok: Tuple[Kulcsszavas, ...]
    rejtett: Tuple[Rejtett, ...]
    hamis_szam: int
    hamis: Tuple[HamisKonyv, ...]
    mogott: Tuple[Mogott, ...]
    talalat: int
    teves_szazalek: int
    eredeti: Optional[Proveniencia]


@dataclasses.dataclass(frozen=True)
class KaroliPontok:
    megfelelok: Optional[Megfelelok]
    parhuzam: Optional[Parhuzam]


def _komb(sor):
    return frozenset(s.kod for s in sor.strongok)


def _kombinaciok(sorok):
    """A sorok különböző Strong-kombinációi, a Strong-számok rendjében."""
    return sorted({_komb(s) for s in sorok if s.strongok}, key=lambda k: sorted(k))


class _Szamolo:
    """A két pont közös számításai egy motívumra."""

    def __init__(self, f):
        self.f, self.b = f, f.b
        self.alakok = karoli_be.b55_szotari_alakok(self.b)
        self.karoli = bemenet.b07_karoli(self.b)
        self._parok = None
        self._nyelvtani = None

    def szavak(self, sor):
        return karoli_be.szavak(sor.karoli_szo.ertek) if sor.karoli_szo is not None else []

    def egyezik(self, szo, kulcs):
        return self.alakok.egyezik(szo, kulcs, konfig.KAROLI_ELOTAG_MARADEK)

    def vers_kulcs(self, igehely):
        return (self.karoli.sorrend(igehely), igehely.kod)

    def parok(self, hely_kod):
        """A hely párjai a Károli–Strong párosításból: [(magyar szó, Strong-kód)]."""
        if self._parok is None:
            self._parok = szavak_be.b54_karoli_parok(self.b)
        return self._parok.parok(hely_kod)

    def nyelvtani(self, strong_kod):
        if self._nyelvtani is None:
            self._nyelvtani = karoli_be.b69_nyelvtani(self.b)
        return strong_kod in self._nyelvtani

    def megfelelok(self, sorok):
        """[(szótári alak, [szóalak], [igehely])] igehelyenként egyszer, gyakoriság, majd alak szerint. A ritkább
        szótári alak beolvad a gyakoribb, legalább 3 betűs alakba, ha minden szóalakja azzal egyezik."""
        hely, alak = {}, {}
        for s in sorok:
            for szo in self.szavak(s):
                lemma = self.alakok.lemma(szo)
                if lemma in karoli_be.NEM_KULCSSZO:
                    continue
                if szo not in alak.setdefault(lemma, []):
                    alak[lemma].append(szo)
                if s.igehely not in hely.setdefault(lemma, []):
                    hely[lemma].append(s.igehely)
        rend = sorted(hely, key=lambda l: (-len(hely[l]), l))
        for i in range(len(rend) - 1, -1, -1):
            lemma = rend[i]
            cel = next((c for c in rend[:i] if len(c) >= konfig.KAROLI_OLVADAS_MIN and c in hely and c != lemma
                        and all(self.egyezik(szo, c) for szo in alak[lemma])), None)
            if cel:
                alak[cel].extend(szo for szo in alak[lemma] if szo not in alak[cel])
                hely[cel].extend(h for h in hely[lemma] if h not in hely[cel])
                del hely[lemma]
        return sorted(((lemma, alak[lemma], sorted(h, key=self.vers_kulcs)) for lemma, h in hely.items()),
                      key=lambda x: (-len(x[2]), x[0]))

    def szocsalad(self, tetelek):
        """A tételek szócsaládonként: a ragozott maradék a rövidebb, legalább `KAROLI_CSALAD_MIN` betűs szótári
        alakba olvad („erőszakossággal” → „erőszak”)."""
        d = collections.OrderedDict((lemma, (list(a), list(h))) for lemma, a, h in tetelek)
        for lemma in sorted(d, key=len, reverse=True):
            alap = next((x for x in d if x != lemma and len(x) >= konfig.KAROLI_CSALAD_MIN and lemma.startswith(x)),
                        None)
            if alap:
                a, h = d.pop(lemma)
                d[alap][0].extend(szo for szo in a if szo not in d[alap][0])
                d[alap][1].extend(x for x in h if x not in d[alap][1])
        return sorted(((lemma, a, sorted(h, key=self.vers_kulcs)) for lemma, (a, h) in d.items()),
                      key=lambda x: (-len(x[2]), x[0]))

    def kulcsszavak(self, sorok):
        """{kombináció: [kulcsszó]} a legalább `KULCS_MIN_SOR` helyen álló kombinációkra."""
        ki = collections.OrderedDict()
        for k in _kombinaciok(sorok):
            csoport = [s for s in sorok if _komb(s) == k and self.szavak(s)]
            if len(csoport) < konfig.KAROLI_KULCS_MIN_SOR:
                continue
            jo = []
            for lemma, _a, helyek in self.megfelelok(csoport):
                if len(helyek) < konfig.KAROLI_KULCS_ARANY * len(csoport):
                    continue
                # a nem nyelvtani párok döntenek: ha van ilyen, és egyik sem a kombináció szava, a magyar szó
                # a motívum szaván kívül áll
                paros = [st for hely in helyek for magyar, st in self.parok(hely.kod)
                         if self.alakok.lemma(magyar) == lemma and not self.nyelvtani(st)]
                if paros and not any(st in k for st in paros):
                    continue
                jo.append(lemma)
            ki[k] = jo
        return ki

    def hianyzo(self, szoveg, kulcsszavak):
        szavak = karoli_be.szavak(szoveg)
        return [kulcs for kulcs in kulcsszavak if not any(self.egyezik(szo, kulcs) for szo in szavak)]

    def rejtett(self, sorok, kulcs):
        ki = []
        for s in sorok:
            v = kulcs.get(_komb(s))
            if not v or s.karoli_szo is None or not s.karoli_szo.ertek:
                continue
            hiany = self.hianyzo(s.karoli_szo.ertek, v)
            if hiany:
                ki.append((s, hiany))
        return sorted(ki, key=lambda x: self.vers_kulcs(x[0].igehely))

    def hamis(self, sorok, kulcs):
        """[(vers-kód, [a versben álló motívumszó Strong-kódja])]: a motívumon kívüli Károli-vers, amelyben valamely
        szó minden kulcsszava áll, de egyik kombináció sem teljes."""
        tahot, tagnt = szavak_be.b08_tahot(self.b), szavak_be.b09_tagnt(self.b)
        sajat = {vers.kod for s in sorok for vers in self.karoli.versek(s.igehely)}
        motivum_szavai = set().union(*kulcs)
        ki = []
        for vers_kod, szoveg in self.karoli.mind():
            if vers_kod in sajat:
                continue
            if not any(not self.hianyzo(szoveg, v) for v in kulcs.values()):
                continue
            strongok = {t[0] for t in tahot.sorok(vers_kod)} | {t[0] for t in tagnt.sorok(vers_kod)}
            if not any(k <= strongok for k in kulcs):
                ki.append((vers_kod, sorted(motivum_szavai & strongok)))
        return ki

    def mogott(self, hamis, kulcs):
        """{kulcsszó: [(Strong-kód, versszám)]}: a hamis párhuzam verseiben melyik (nem nyelvtani) szó áll a
        kulcsszó mögött a párosítás szerint, gyakoriság szerint (holtversenyben az elsőként látott elöl)."""
        ki = collections.OrderedDict()
        for kulcsszo in [szo for v in kulcs.values() for szo in v]:
            szamlalo = collections.Counter()
            for vers_kod, _szavak in hamis:
                szamlalo.update(sorted({st for magyar, st in self.parok(vers_kod)
                                        if self.egyezik(magyar, kulcsszo) and not self.nyelvtani(st)}))
            ki[kulcsszo] = szamlalo.most_common()
        return ki


def _kombo_szavak(f, k):
    return tuple(f.szo(Strong(kod)) for kod in sorted(k))


def _megfelelok(sz, sorok, motivum):
    f = sz.f
    tetelek = sz.megfelelok(sorok)
    hely_szam = sum(1 for s in sorok if s.karoli_szo is not None and s.karoli_szo.ertek)
    if not tetelek or not hely_szam:
        return None
    csaladok = sz.szocsalad(tetelek)
    szavankent = []
    for k in _kombinaciok(sorok):
        csoport = [s for s in sorok if _komb(s) == k and sz.szavak(s)]
        if csoport:
            szavankent.append((k, len(csoport), sz.szocsalad(sz.megfelelok(csoport))))
    szavankent.sort(key=lambda x: (-x[1], sorted(x[0])))
    merheto = [x for x in szavankent if x[1] >= konfig.KAROLI_MIN_HELY]
    return Megfelelok(
        hely_szam=hely_szam,
        csaladok=tuple(Megfelelo(idezet(sz.alakok.idezheto(lemma)),
                                 tuple(idezet(karoli_be.szoalak(f.b, szo)) for szo in a),
                                 tuple(h)) for lemma, a, h in csaladok),
        merheto=tuple(SzoMeres(_kombo_szavak(f, k), db, idezet(sz.alakok.idezheto(cs[0][0])), len(cs[0][2]))
                      for k, db, cs in merheto),
        tobbi=len(szavankent) - len(merheto),
        allando=tuple(_kombo_szavak(f, k) for k, db, cs in merheto
                      if len(cs[0][2]) / db >= konfig.KAROLI_ALLANDO),
        valtozo=tuple(_kombo_szavak(f, k) for k, db, cs in merheto
                      if len(cs[0][2]) / db < konfig.KAROLI_ALLANDO),
        eredeti=prov('*(proveniencia: scope={} (id={}, karoli_szo) | forras={}+{} (eszkozok/szerep_karoli.py) | n={}',
                     f.b.jegyzek_utvonal('B03'), motivum, f.b.jegyzek_utvonal('B03'), f.b.jegyzek_utvonal('B55'),
                     hely_szam))


def _parhuzam(sz, sorok):
    f = sz.f
    kulcs = collections.OrderedDict((k, v) for k, v in sz.kulcsszavak(sorok).items() if v)
    szavak_szama = len(_kombinaciok(sorok))
    if not kulcs:
        return Parhuzam(szavak_szama, (), (), 0, (), (), 0, 0, None)
    rejtett = sz.rejtett(sorok, kulcs)
    hamis = sz.hamis(sorok, kulcs)
    konyvek = collections.OrderedDict()
    for vers_kod, motivum_szavai in hamis:
        vers = Igehely(vers_kod)   # a Károli-fordítás saját verskulcsa (a könyv rövidítése a fordítás fájljáé)
        konyvek.setdefault(vers.konyv, []).append(
            HamisVers(vers, tuple(f.szo(Strong(kod)) for kod in motivum_szavai)))
    mogott = []
    for kulcsszo, lista in sz.mogott(hamis, kulcs).items():
        idegen = [(st, db) for st, db in lista if not any(st in k for k in kulcs)][:1]
        if idegen:
            mogott.append(Mogott(idezet(sz.alakok.idezheto(kulcsszo)), f.szo(Strong(idegen[0][0])), idegen[0][1]))
    talalat = sum(1 for s in sorok if _komb(s) in kulcs) - len(rejtett) + len(hamis)
    kulcs_belso = prov_fuz('; ', [prov('{}: {}', prov_fuz('+', [Strong(kod) for kod in sorted(k)]),
                                       prov_fuz(', ', [prov('„{}”', sz.alakok.idezheto(szo)) for szo in v]))
                                  for k, v in kulcs.items()])
    return Parhuzam(
        szavak_szama=szavak_szama,
        kulcsok=tuple(Kulcsszavas(_kombo_szavak(f, k), tuple(idezet(sz.alakok.idezheto(szo)) for szo in v))
                      for k, v in kulcs.items()),
        rejtett=tuple(Rejtett(s.igehely, idezet(s.karoli_szo), _kombo_szavak(f, _komb(s)),
                              tuple(idezet(sz.alakok.idezheto(szo)) for szo in hiany)) for s, hiany in rejtett),
        hamis_szam=len(hamis),
        hamis=tuple(HamisKonyv(versek[0].vers, tuple(versek)) for versek in konyvek.values()),
        mogott=tuple(mogott),
        talalat=talalat,
        teves_szazalek=round(100 * len(hamis) / talalat) if talalat else 0,
        eredeti=prov('*(proveniencia: scope=Károli teljes ({}) | forras=Karoli_1908.tsv+TAHOT_kivonat.tsv'
                     '+TAGNT_kivonat.tsv+{}+{}+{} (eszkozok/szerep_karoli.py) | n={}', kulcs_belso,
                     f.b.jegyzek_utvonal('B03'), f.b.jegyzek_utvonal('B55'), szavak_be.parositas_konyvtara(f.b),
                     len(hamis) + len(rejtett)))


def szamit(f, motivum):
    """A két pont lapmodellje; ha a motívumon a két pont nem épül (nincs jóváhagyva, vagy a soroknak nincs
    Károli-szava), mindkettő None."""
    if not karoli_be.b53_karoli_pontok(f.b, motivum) or not karoli_be.kotelezo_karoli_szo(f.sorok):
        return KaroliPontok(None, None)
    sz = _Szamolo(f)
    return KaroliPontok(_megfelelok(sz, f.sorok, motivum), _parhuzam(sz, f.sorok))
