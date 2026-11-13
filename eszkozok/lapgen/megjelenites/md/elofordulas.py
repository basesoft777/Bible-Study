"""lapgen.megjelenites.md.elofordulas — a „2. Előfordulások” szakasz és a „2.1 Az igehelyek szövege” pont.

Minden látható mondat a sablontáblából jön (`e2.*`, `e21.*` kulcsok); itt csak a szerkezet áll.
"""
from lapgen.ertekek import SzovetsegKod
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import horgony_jel

AZONOSITO = 'elofordulasok'
ALPONT_SZOVEG = 1   # a 2.1 pont sorszáma a szakaszon belül

_SZOVETSEG_SABLON = {
    SzovetsegKod.FOKENT_OSZ: 'e2.kov.fokent_osz',
    SzovetsegKod.FOKENT_USZ: 'e2.kov.fokent_usz',
    SzovetsegKod.MINDKETTO: 'e2.kov.mindketto',
    SzovetsegKod.CSAK_OSZ: 'e2.kov.csak_osz',
    SzovetsegKod.CSAK_USZ: 'e2.kov.csak_usz',
}


def _osszegzo(ny, o):
    """Az összegző mondat: lelet, megbízhatóság, következtetés."""
    if o.osz and o.usz:
        lelet = ny.s('e2.lelet.ket_szovetseg', n=o.helyek, konyvek=o.konyvek, osz=o.osz, usz=o.usz)
    elif o.osz:
        lelet = ny.s('e2.lelet.csak_osz', n=o.helyek, konyvek=o.konyvek, osz=o.osz)
    else:
        lelet = ny.s('e2.lelet.csak_usz', n=o.helyek, konyvek=o.konyvek, usz=o.usz)
    if o.helyek - o.magas:
        megb = ny.s('e2.megb.vegyes', magas=o.magas, tobbi=o.helyek - o.magas)
    else:
        megb = ny.s('e2.megb.mind', magas=o.magas)
    kov = []
    if o.sulypont_konyv is not None:
        kov.append(ny.s('e2.kov.sulypont', konyv=o.sulypont_konyv, n=o.helyek, db=o.sulypont_db))
    if o.szovetseg is SzovetsegKod.FOKENT_OSZ:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], usz=o.usz))
    elif o.szovetseg is SzovetsegKod.FOKENT_USZ:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], osz=o.osz))
    elif o.szovetseg is SzovetsegKod.MINDKETTO:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], osz=o.osz, usz=o.usz))
    else:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg]))
    if o.bizonytalan:
        kov.append(ny.s('e2.kov.bizonytalan'))
    return ny.s('e2.osszegzo', lelet=lelet, megb=megb, kov=tuple(kov))


def _tetel(iro, ny, tetel):
    iro.sor(horgony_jel(tetel.horgony))
    iro.sor(ny.s('e21.igehely', hely=tetel.igehely))
    for vers in tetel.versek:
        if vers.szoveg is not None:
            iro.sor(ny.s('e21.vers', szoveg=vers.szoveg))
        else:
            iro.sor(ny.s('e21.nincs_vers', vers=vers.vers))
    if tetel.kapcsolodas is not None:
        iro.sor(tetel.kapcsolodas)
    if tetel.funkcio is not None:
        iro.ures()
        iro.sor(ny.s('e21.funkcio', magyarazat=tetel.funkcio))
    iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    szakasz = keret.rend.sorszam(AZONOSITO)
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, _osszegzo(ny, modell.osszegzes))
    iro.sor(ny.s('e2.hatokor', n=modell.osszegzes.helyek, tabla=ny.nev('forras', 'B03'), szakasz=szakasz,
                 alpont=ALPONT_SZOVEG, cimketabla=ny.nev('forras', 'B16'), bdb=ny.nev('forras', 'B19'),
                 thayer=ny.nev('forras', 'B21'), datum=modell.jelentes_dontes))
    iro.ures()
    iro.cimsor(4, ny.s('cim.alpont', szakasz=szakasz, alpont=ALPONT_SZOVEG, cim=ny.s('cim.elofordulasok.szoveg')))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('e21.bevezeto'))
    for tetel in modell.tetelek:
        _tetel(iro, ny, tetel)
    K.blokk_zar(iro, keret, AZONOSITO)
