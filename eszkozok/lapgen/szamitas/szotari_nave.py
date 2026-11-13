"""lapgen.szamitas.szotari_nave — a 4.12 pont (tematikus index) lapmodellje.

A tematikus index (Nave, 1897) témái közül szóba jön az, amely a motívum legalább `NAVE_MIN_VERS` versét érinti,
a motívumversek aránya a téma összes verséhez legalább `NAVE_MIN_ARANY`, és a motívum döntése nem tiltja (a
tiltott téma a tágabb kör felé mutat). Ha a motívumnak van kiválasztott témája, csak a kiválasztottak állnak a
lapon; különben a szóba jöhetők a kizártak nélkül. A pont csak akkor épül, ha a motívumnak van döntése.

A motívum verse itt a motívumsor igehelye, ahogy a táblában áll (a verstartomány nem bomlik versekre: a régi
szabály szerint a tartománnyal álló sor a tematikus index egyes verseivel nem egyezik).
"""
import collections
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import nave as nave_be
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, Lathato, Proveniencia, idezet, prov, proza


@dataclasses.dataclass(frozen=True)
class TemaNev:
    """Egy téma vagy altétel neve: magyarul, mögötte az angol eredeti; magyar név híján az angol áll (fordításra
    vár)."""
    angol: Lathato
    magyar: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class Altetel:
    nev: TemaNev
    versek: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class Tema:
    nev: TemaNev
    motivumversek: Tuple[Igehely, ...]
    temavers: int
    szazalek: float
    altetelek: Tuple[Altetel, ...]


@dataclasses.dataclass(frozen=True)
class Tematikus:
    temak: Tuple[Tema, ...]
    szoba_johet: int
    tiltott: int
    tagabb_kor: Optional[Lathato]   # a motívum tágabb köre (kézi próza), ha van tiltott téma
    eredeti: Proveniencia


def _nev(n):
    return TemaNev(idezet(n.angol), idezet(n.magyar) if n.magyar is not None else None)


def szamit(f, motivum):
    """A pont lapmodellje; None, ha a motívumnak nincs döntése a témákról, vagy egy téma sem áll a lapon."""
    index = nave_be.nave(f.b, motivum)
    if not index.dontesek:
        return None
    karoli = bemenet.b07_karoli(f.b)

    def rend(kod):
        return (karoli.sorrend(nave_be.vers(kod)), kod)

    tiltott = {t for t, d in index.dontesek.items() if d == nave_be.DONTES_TILTOTT}
    sajat = {s.igehely.kod for s in f.sorok}
    nevek, tema_vers = {}, collections.defaultdict(set)
    talalat = collections.OrderedDict()
    for tema_id, tema, cimke, versek in index.sorok:
        nevek[tema_id] = tema
        for vers in versek:
            tema_vers[tema_id].add(vers)
            if vers in sajat:
                lista = talalat.setdefault(tema_id, collections.OrderedDict()).setdefault(cimke, [])
                if vers not in lista:
                    lista.append(vers)
    jeloltek = []
    for tema_id, cimkek in talalat.items():
        motivumversek = sorted({v for versek in cimkek.values() for v in versek}, key=rend)
        arany = len(motivumversek) / len(tema_vers[tema_id])
        if len(motivumversek) < konfig.NAVE_MIN_VERS or arany < konfig.NAVE_MIN_ARANY or tema_id in tiltott:
            continue
        jeloltek.append((tema_id, motivumversek, arany,
                         [(c, sorted(v, key=rend)) for c, v in sorted(cimkek.items(), key=lambda x: x[0])]))
    jeloltek.sort(key=lambda t: (-len(t[1]), -t[2], t[0]))
    kivalasztott = {t for t, d in index.dontesek.items() if d == nave_be.DONTES_KIVALASZTOTT}
    temak = [t for t in jeloltek
             if (t[0] in kivalasztott if kivalasztott else index.dontesek.get(t[0]) != nave_be.DONTES_KIZART)]
    if not temak:
        return None
    tagabb = motivum_be.b02_motivum(f.b, motivum).folerendelt if tiltott else None
    return Tematikus(
        temak=tuple(Tema(
            nev=_nev(index.nev(tema_id, '', nevek[tema_id])),
            motivumversek=tuple(nave_be.vers(v) for v in motivumversek),
            temavers=len(tema_vers[tema_id]),
            szazalek=100 * arany,
            altetelek=tuple(Altetel(_nev(index.nev(tema_id, cimke, cimke)), tuple(nave_be.vers(v) for v in versek))
                            for cimke, versek in cimkek if cimke))
            for tema_id, motivumversek, arany, cimkek in temak),
        szoba_johet=len(jeloltek),
        tiltott=len(tiltott),
        tagabb_kor=proza(tagabb) if tagabb is not None else None,
        eredeti=prov('*(proveniencia: scope={} (id={}) | forras=Nave_basokant.tsv+{}+{} (eszkozok/szerep_nave.py) | '
                     'n={}', f.b.jegyzek_utvonal('B03'), motivum, f.b.jegyzek_utvonal('B70'),
                     f.b.jegyzek_utvonal('B71'), len(temak)))


def kapu(modell):
    """GK-21: a tematikus index pontja nem állhat üresen: ha a pont épül, van benne téma, és minden témának van
    motívumverse."""
    if modell is not None and (not modell.temak or any(not t.motivumversek for t in modell.temak)):
        raise KapuHiba('a tematikus index pontja üres, vagy egy témájának nincs motívumverse')
    return modell
