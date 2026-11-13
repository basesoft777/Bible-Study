"""lapgen.bemenet.konyvek — a könyvek rendje, szövetsége és teljes neve (B63).

A normalizáló tábla sorrendje maga a kánoni sorrend; az Újszövetség a tábla záró 27 sora (Máté–Jelenések).
Könyvnév csak innen jön: a kódban könyvnév-alias nincs (GK-17).
"""
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Igehely, Nev, SzovegHiba

_OSZLOPOK = ('STEPBible-rövidítés', 'Magyar rövidítés', 'Teljes magyar könyvnév')
_USZ_ELSO, _USZ_UTOLSO, _USZ_DB = 'Mat', 'Rev', 27
NEV_TIPUS = 'konyv'


class Konyvek:
    def __init__(self, sorrend, ujszovetsegi, nevek):
        self._sorrend, self._ujszovetsegi, self._nevek = sorrend, ujszovetsegi, nevek

    def ismert(self, konyv):
        return konyv in self._sorrend

    def sorszam(self, konyv):
        try:
            return self._sorrend[konyv]
        except KeyError:
            raise BemenetHiba('B63: ismeretlen könyvnév: %s (a normalizáló táblában nincs ilyen rövidítés)'
                              % konyv) from None

    def ujszovetsegi(self, konyv):
        self.sorszam(konyv)
        return konyv in self._ujszovetsegi

    def nev(self, konyv):
        """A könyv teljes magyar neve névtábla-elemként."""
        self.sorszam(konyv)
        return self._nevek[konyv]

    def rendezo_kulcs(self, igehely):
        """Kánoni rendezőkulcs: (könyv sorszáma, fejezet, vers); tartománynál a kezdőpont."""
        return (self.sorszam(igehely.konyv), igehely.fejezet, igehely.vers)

    def igehely(self, nyers):
        """Igehely a nyers alakból; ismeretlen könyv vagy hibás alak BemenetHiba."""
        try:
            hely = Igehely(nyers.strip())
        except SzovegHiba as hiba:
            raise BemenetHiba('érvénytelen igehely: %r (%s)' % (nyers, hiba)) from None
        self.sorszam(hely.konyv)
        return hely


def b63_konyvek(b):
    """B63 — a könyvnév-normalizáló tábla: kánoni sorrend, szövetség, teljes név."""
    tabla = b._tabla('B63', oszlopok=_OSZLOPOK)
    step, rov, teljes = (tabla.oszlop(o) for o in _OSZLOPOK)
    sorrend, nevek, stepek = {}, {}, []
    for i, sor in enumerate(tabla.sorok):
        if sor[rov] in sorrend:
            raise BemenetHiba('B63: ismétlődő magyar rövidítés: %s' % sor[rov])
        sorrend[sor[rov]] = i
        nevek[sor[rov]] = Nev(NEV_TIPUS, sor[rov], sor[teljes])
        stepek.append(sor[step])
    if _USZ_ELSO not in stepek or stepek[-1] != _USZ_UTOLSO or len(stepek) - stepek.index(_USZ_ELSO) != _USZ_DB:
        raise BemenetHiba('B63: az Újszövetség nem a tábla záró %d sora' % _USZ_DB)
    ujszov = frozenset(sor[rov] for sor in tabla.sorok[stepek.index(_USZ_ELSO):])
    return Konyvek(sorrend, ujszov, nevek)
