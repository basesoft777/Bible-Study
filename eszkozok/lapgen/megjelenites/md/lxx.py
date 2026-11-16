"""lapgen.megjelenites.md.lxx — az „5. LXX-fordítói döntések” szakasz (S4).

Minden látható mondat a sablontáblából jön (`s5.*`); a szöveg a lapmodell idézeteiből. Az olvasói bekezdés a szóhíd
összegzése (a régi `olvasoi_kovetkeztetes.lxx_hid`); a 4.6 mondatai ugyanezt a számlálót olvassák.
"""
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.szocikkek import szo_nevelovel
from lapgen.szamitas.lxx import GorogFajta, Itelet
from lapgen.szoveg import prov

AZONOSITO = 'lxx'
_SZAMNEV_MAX = 10
_FEJLEC = ('s5.fejlec.vers', 's5.fejlec.lxx', 's5.fejlec.heber', 's5.fejlec.gorog', 's5.fejlec.itelet')
_HATASTORTENET = 'hatastortenet'


def szamnev(ny, n):
    """A szám szóval (egy … tíz), fölötte számjeggyel (a régi `_SZAMNEV`)."""
    return ny.s(ny.kulcs('szamnev', str(n))) if 1 <= n <= _SZAMNEV_MAX else ny.s('szam', n=n)


def jelzo(ny, fok):
    """A híd erőssége (a modell fokozata; a régi `lxx_hid_jelzo`)."""
    return ny.s(ny.kulcs('s5.jelzo', fok.value))


def hid_bekezdes(ny, m):
    """Az 5. szakasz olvasói bekezdése (a régi `lxx_hid`)."""
    sz = m.szamlalo
    n = sz.osszes()
    mondatok = [ny.s('s5.hid.n', n=n)]
    par_n = sz.egyezo + sz.szocsalad + sz.eltero
    nevek = tuple(szo_nevelovel(ny, szo) for szo in m.par_nevek)
    if nevek:
        reszek = tuple(ny.s(k, n=db) for k, db in (('s5.hid.egyezo', sz.egyezo), ('s5.hid.szocsalad', sz.szocsalad),
                                                    ('s5.hid.eltero', sz.eltero)) if db)
        szn = szamnev(ny, len(nevek))
        mondatok.append(ny.s('s5.hid.par', szamnev=szn, nevek=nevek, n=par_n, reszek=reszek) if reszek
                        else ny.s('s5.hid.par.ures', szamnev=szn, nevek=nevek, n=par_n))
    if sz.nincs_par:
        mondatok.append(ny.s('s5.hid.nincs_par.tobbi' if nevek else 's5.hid.nincs_par.mind', n=sz.nincs_par))
    tobbi = tuple(ny.s(k, n=db) for k, db in (('s5.hid.fuggoben', sz.fuggoben), ('s5.hid.szamozas', sz.szamozas),
                                               ('s5.hid.minusz', sz.minusz)) if db)
    if tobbi:
        mondatok.append(ny.s('s5.hid.tobbi', elemek=tobbi))
    if par_n:
        mondatok.append(ny.s('s5.hid.kov', szamnev=szamnev(ny, len(nevek)),
                             jelzo=jelzo(ny, m.fok), a=sz.egyezo + sz.szocsalad, b=par_n))
    return ny.s('s5.hid', mondatok=tuple(mondatok))


def _hivatkozas(ny, g):
    if g.kiejtes is None:
        raise ValueError('5.: a görög megfelelőnek nincs kiejtése')
    if g.strong is None:
        return g.kiejtes
    if g.glossza is None:
        return ny.s('s5.strong.glossza_nelkul', kiejtes=g.kiejtes, strong=g.strong)
    return ny.s('s5.strong', kiejtes=g.kiejtes, strong=g.strong, glossza=g.glossza)


def _gorog(ny, g):
    if g.fajta is GorogFajta.SZOVEG:
        hiv = _hivatkozas(ny, g)
        if g.alak_kiejtes is not None:
            return ny.s('s5.gorog.szoveg.potlas', alak=g.alak, potlas=g.alak_kiejtes, lemma=g.lemma, hiv=hiv)
        return ny.s('s5.gorog.szoveg', alak=g.alak, lemma=g.lemma, hiv=hiv)
    if g.fajta is GorogFajta.DONTES:
        return ny.s('s5.gorog.dontes', lemma=g.lemma, hiv=_hivatkozas(ny, g))
    if g.fajta is GorogFajta.TARSITAS:
        return ny.s('s5.gorog.tarsitas', lemma=g.lemma, kiejtes=g.kiejtes)
    if g.fajta is GorogFajta.MINUSZ:
        return ny.s('s5.gorog.minusz')
    return ny.s('jel.nincs')


def _lxx(ny, sor):
    if sor.lxx is None:
        return ny.s('jel.nincs')
    return ny.s('s5.lxx.elter' if sor.lxx.elter else 's5.lxx', konyv=sor.vers, fej=sor.lxx.fej, vers=sor.lxx.vers)


def _heber(ny, h):
    if h is None:
        return ny.s('jel.nincs')
    if h.kiejtes is None:
        return ny.s('d12.szo.kiejtes_nelkul', alak=h.alak)
    return ny.s('d12.szo', alak=h.alak, kiejtes=h.kiejtes)


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, hid_bekezdes(ny, modell))
    iro.sor(ny.s('s5.bevezeto'))
    iro.ures()
    iro.tabla_sor(tuple(ny.s(k) for k in _FEJLEC))
    iro.tabla_elvalaszto(len(_FEJLEC))
    for sor in modell.sorok:
        iro.tabla_sor((ny.s('s5.vers', vers=sor.vers), _lxx(ny, sor), _heber(ny, sor.heber), _gorog(ny, sor.gorog),
                       ny.s(ny.kulcs('s5.itelet', sor.itelet.value))))
    iro.ures()
    iro.sor(ny.s('s5.magyarazat', szakasz=keret.rend.sorszam(_HATASTORTENET)))
    iro.ures()
    sz = modell.szamlalo
    iro.sor(ny.s('s5.osszesites', **{it.value: getattr(sz, it.value) for it in Itelet}))
    iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO)


# --- a 4.6 (LXX-híd) ------------------------------------------------------------------------------------------------
_RESZ_NINCS_PAR = (('s4.p6.resz.minusz', 'minusz'), ('s4.p6.resz.fuggoben', 'fuggoben'),
                   ('s4.p6.resz.szamozas', 'szamozas'))
_RESZ_PAR = (('s4.p6.resz.egyezo', 'egyezo'), ('s4.p6.resz.szocsalad', 'szocsalad'), ('s4.p6.resz.mas', 'eltero'),
             ('s4.p6.resz.minusz', 'minusz'), ('s4.p6.resz.fuggoben', 'fuggoben'), ('s4.p6.resz.szamozas', 'szamozas'))


def rovid_mondat(ny, m, keret):
    """A 4.6 olvasói mondata mindkét nyelvrészen (a régi `lxx_hid_rovid`), az 5. szakaszra mutató hivatkozással."""
    sz = m.szamlalo
    par_n = sz.egyezo + sz.szocsalad + sz.eltero
    cim, horgony = K.szamozott_cim(keret, AZONOSITO), K.szakasz_horgony(keret, AZONOSITO)
    if not m.par_nevek or not par_n:
        return ny.s('s4.p6.rovid.ures', cim=cim, horgony=horgony)
    return ny.s('s4.p6.rovid', szamnev=szamnev(ny, len(m.par_nevek)),
                nevek=tuple(szo_nevelovel(ny, szo) for szo in m.par_nevek),
                jelzo=jelzo(ny, m.fok), a=sz.egyezo + sz.szocsalad, b=par_n, cim=cim,
                horgony=horgony)


def _szo_mondat(ny, mondat, szo_nagy):
    sz = mondat.szamlalo
    n, nev = sz.osszes(), szo_nagy(ny, mondat.szo)
    if not mondat.van_par:
        reszek = ((ny.s('s4.p6.resz.mas', n=sz.nincs_par + sz.eltero),) if sz.nincs_par + sz.eltero else ()) + tuple(
            ny.s(k, n=getattr(sz, m)) for k, m in _RESZ_NINCS_PAR if getattr(sz, m))
        return (ny.s('s4.p6.szo.nincs_par', nev=nev, n=n, reszek=reszek) if reszek
                else ny.s('s4.p6.szo.nincs_par.ures', nev=nev, n=n))
    reszek = tuple(ny.s(k, n=getattr(sz, m)) for k, m in _RESZ_PAR if getattr(sz, m))
    lelet = ny.s('s4.p6.szo', nev=nev, n=n, reszek=reszek) if reszek else ny.s('s4.p6.szo.ures', nev=nev, n=n)
    if mondat.kovetkeztetes:
        return ny.s('s4.p6.szo.kovetkeztetes', lelet=lelet, a=sz.egyezo + sz.szocsalad, n=n)
    return lelet


def _tars_elem(ny, elem):
    if elem.szo.alak is None or elem.szo.kiejtes is None:
        raise ValueError('4.6: a(z) %s társnak nincs szótári alakja vagy kiejtése: az ág nincs portolva' % elem.szo.strong)
    if elem.glossza is None:
        hiv = ny.s('s5.strong.glossza_nelkul', kiejtes=elem.szo.kiejtes, strong=elem.szo.strong)
    else:
        hiv = ny.s('s5.strong', kiejtes=elem.szo.kiejtes, strong=elem.szo.strong, glossza=elem.glossza)
    return ny.s('s4.p6.tars.elem', lemma=elem.szo.alak, hiv=hiv, n=elem.versek)


def hid(iro, ny, keret, hid_modell, szo_iras, szo_nagy, bekezdes):
    """A 4.6 pont egy nyelvrészen."""
    m = hid_modell.osszevetes
    K.olvasoi_bekezdes(iro, rovid_mondat(ny, m, keret))
    if not hid_modell.mondatok:
        sz = m.szamlalo
        szavak = tuple(szo_iras(ny, szo) for szo in hid_modell.szavak)
        bekezdes(iro, ny.s('s4.p6.gorog', szavak=szavak, n=sz.osszes(), e=sz.egyezo, c=sz.szocsalad) if sz.szocsalad
                 else ny.s('s4.p6.gorog.csalad_nelkul', szavak=szavak, n=sz.osszes(), e=sz.egyezo))
        return
    for mondat in hid_modell.mondatok:
        bekezdes(iro, _szo_mondat(ny, mondat, szo_nagy))
    bekezdes(iro, ny.s('s4.p6.tars.bevezeto'))
    for t in hid_modell.tarslistak:
        szo = szo_iras(ny, t.szo)
        if t.versek is None:
            bekezdes(iro, ny.s('s4.p6.tars.nincs', szo=szo, strong=t.szo.strong))
        elif t.tarsak:
            bekezdes(iro, ny.s('s4.p6.tars', szo=szo, n=t.versek, p=t.parral,
                               tarsak=tuple(_tars_elem(ny, e) for e in t.tarsak), strong=t.szo.strong))
        else:
            bekezdes(iro, ny.s('s4.p6.tars.ures', szo=szo, n=t.versek, p=t.parral, strong=t.szo.strong))
    if hid_modell.proveniencia is not None:
        iro.sor(ny.s('s4.p6.forras'), prov('eredeti: *Proveniencia (a tábla soraiból): {}*', hid_modell.proveniencia))
        iro.ures()
