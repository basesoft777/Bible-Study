"""lapgen.megjelenites.md.szotari_nave — a 4.12 pont (tematikus index: témák és igehely-hivatkozások).

Minden látható mondat a sablontáblából jön (`s4.p12.*`). A téma magyar neve idézet a nevek táblájából, mögötte
rámutatásra az angol eredeti; magyar név híján az angol áll „fordításra vár” jelöléssel.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.szotari_karoli import forrassor

FORRASOK = ('B57', 'B70', 'B71')


def _nev(ny, nev):
    if nev.magyar is None:
        return ny.s('s4.forditasra_var', szoveg=nev.angol)
    return ny.s('s4.p12.nev', angol=nev.angol, magyar=nev.magyar)


def _pelda(ny, nev):
    """A bevezető példája: a téma magyar neve (a rámutatásra látszó angol nélkül)."""
    return nev.magyar if nev.magyar is not None else ny.s('s4.forditasra_var', szoveg=nev.angol)


def tematikus(iro, ny, modell, keret):
    """A 4.12 pont törzse (a pont címe után)."""
    m = modell
    pelda = _pelda(ny, m.temak[0].nev)
    if m.tagabb_kor is not None:
        K.olvasoi_bekezdes(iro, ny.s('s4.p12.bevezeto.tagabb', n=len(m.temak), pelda=pelda, tagabb=m.tagabb_kor))
    else:
        K.olvasoi_bekezdes(iro, ny.s('s4.p12.bevezeto', n=len(m.temak), pelda=pelda))
    iro.sor(ny.s('s4.p12.hatokor', minimum=konfig.NAVE_MIN_VERS, szazalek=konfig.NAVE_MIN_SZAZALEK, tiltott=m.tiltott,
                 jelolt=m.szoba_johet, n=len(m.temak), dontesek=ny.nev('forras', 'B70')))
    iro.ures()
    for tema in m.temak:
        iro.sor(ny.s('s4.p12.tema', nev=_nev(ny, tema.nev), mv=len(tema.motivumversek), tv=tema.temavers,
                     szazalek=tema.szazalek, versek=tema.motivumversek))
        for altetel in tema.altetelek:
            iro.sor(ny.s('s4.p12.altetel', nev=_nev(ny, altetel.nev), versek=altetel.versek))
    iro.ures()
    forrassor(iro, ny, keret, FORRASOK, m.eredeti)
