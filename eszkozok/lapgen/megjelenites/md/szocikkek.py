"""lapgen.megjelenites.md.szocikkek — a „Szótári háttér” szakasz: a váz, az áttekintő tábla és a szótári pontok.

Minden látható mondat a sablontáblából jön (`s4.*` kulcsok); itt csak a szerkezet áll. A pontok száma és rendje a
lapmodellből (a szótári pontok táblájából), a pont neve a névtáblából jön. A még el nem készült pont megjelenítője
hiányzik a `_PONTOK` táblából: a lap ilyenkor részleges, a pont kimarad.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.szamitas.szocikkek import Nyelv

AZONOSITO = 'szocikkek'
HATASTORTENET = 'hatastortenet'
FEJLEC_ATTEKINTES = ('s4.att.fejlec.szo', 's4.att.fejlec.jelentes', 's4.att.fejlec.lxx', 's4.att.fejlec.helyek')
PONT_NEV_TIPUS = 'szotari_pont'


def _bekezdes(iro, szoveg):
    iro.sor(szoveg)
    iro.ures()


def szo_iras(ny, szo):
    """A szó írással és zárójeles kiejtéssel; szótári alak híján a Strong-száma."""
    if szo.alak is None:
        return ny.s('d12.szo.strong', strong=szo.strong)
    if szo.kiejtes is None:
        return ny.s('d12.szo.kiejtes_nelkul', alak=szo.alak)
    return ny.s('d12.szo', alak=szo.alak, kiejtes=szo.kiejtes)


def szoveg_allapottal(ny, szoveg):
    """Egy rövid forrásszöveg a fordítás-állapot jelölésével (fordításra vár; felülvizsgálat alatt)."""
    if szoveg.forditasra_var:
        return ny.s('s4.forditasra_var', szoveg=szoveg.szoveg)
    if szoveg.elavult:
        return ny.s('s4.felulvizsgalat', szoveg=szoveg.szoveg)
    return szoveg.szoveg


def jelentes(ny, j):
    """A rövid jelentés: magyarul; magyar híján az angol eredeti, „fordításra vár” jelöléssel; ha az sincs, a
    hiány kimondva."""
    if j.magyar is not None:
        return ny.s('s4.felulvizsgalat', szoveg=j.magyar) if j.elavult else j.magyar
    if j.angol is not None:
        return ny.s('s4.forditasra_var', szoveg=j.angol)
    return ny.s('s4.jelentes.nincs')


def _pont_cim(iro, ny, szakasz, pont, cim=None):
    iro.cimsor(4, ny.s('cim.alpont', szakasz=szakasz, alpont=pont,
                       cim=cim if cim is not None else ny.s('ertek.nev', n=ny.nev(PONT_NEV_TIPUS, pont))))
    iro.ures()


# --- az áttekintő tábla ------------------------------------------------------------------------------------------


def _attekintes(iro, ny, szakasz, modell, keret):
    nyelvi = [p for resz in modell.nyelvek for p in resz.pontok]
    iro.cimsor(3, ny.s('cim.szocikkek.attekintes'))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('s4.att.bevezeto', n=len(modell.attekintes), szakasz=szakasz, elso=min(nyelvi),
                                 utolso=max(nyelvi)))
    iro.tabla_sor(tuple(ny.s(kulcs) for kulcs in FEJLEC_ATTEKINTES))
    iro.tabla_elvalaszto(len(FEJLEC_ATTEKINTES))
    hiany = False
    for sor in modell.attekintes:
        if sor.tars is None:
            tars = ny.s('jel.nincs')
        else:
            tars = ny.s('s4.att.tars' if sor.szo.strong.heber else 's4.att.tars.heberul', szo=szo_iras(ny, sor.tars),
                        n=sor.tars_versek)
        hiany = hiany or sor.jelentes.magyar is None
        iro.tabla_sor((szo_iras(ny, sor.szo), sor.jelentes.magyar if sor.jelentes.magyar is not None
                       else ny.s('jel.nincs'), tars, ny.s('s4.szam', n=sor.helyek)))
    iro.ures()
    _bekezdes(iro, ny.s('s4.att.labjegyzet.hiany' if hiany else 's4.att.labjegyzet', szakasz=szakasz,
                        pont=konfig.PONT_LXX_HID, hat=keret.rend.sorszam(HATASTORTENET),
                        hat_nev=ny.s('cim.hatastortenet.rovid')))


# --- az egyszerű pontok ------------------------------------------------------------------------------------------


def _alapjelentes(iro, ny, szakasz, resz, keret):
    K.olvasoi_bekezdes(iro, ny.s(ny.kulcs('s4.p1.bevezeto', resz.nyelv.value), licenc=resz.rovid_szotar_licenc))
    for sor in resz.alapjelentes:
        _bekezdes(iro, ny.s('s4.p1.sor', szo=szo_iras(ny, sor.szo), jelentes=jelentes(ny, sor.jelentes),
                            strong=sor.szo.strong))


def _tw_cim(ny, cim):
    if cim.forditasra_var:
        return ny.s('s4.p3.cim.var', cim=cim.szoveg)
    return ny.s('s4.p3.cim.felulvizsgalat' if cim.elavult else 's4.p3.cim', cim=cim.szoveg)


def _teologiai(iro, ny, szakasz, resz, keret):
    K.olvasoi_bekezdes(iro, ny.s(ny.kulcs('s4.p3.bevezeto', resz.nyelv.value), licenc=resz.tw_licenc))
    for sor in resz.teologiai:
        reszek = [_tw_cim(ny, cim) for cim in sor.cimek] or [ny.s('s4.p3.nincs')]
        if sor.twot is not None:
            reszek.append(ny.s('s4.p3.twot', szamok=sor.twot) if sor.twot else ny.s('s4.p3.twot.nincs'))
        _bekezdes(iro, ny.s('s4.p3.sor', szo=szo_iras(ny, sor.szo), reszek=tuple(reszek), strong=sor.szo.strong))


def _domen(iro, ny, szakasz, resz, keret):
    K.olvasoi_bekezdes(iro, ny.s('s4.p4.bevezeto'))
    for sor in resz.domen:
        if sor.domenek:
            _bekezdes(iro, ny.s('s4.p4.sor', szo=szo_iras(ny, sor.szo),
                                domenek=tuple(szoveg_allapottal(ny, d) for d in sor.domenek)))
        else:
            _bekezdes(iro, ny.s('s4.p4.sor.nincs', szo=szo_iras(ny, sor.szo)))
        if sor.elemzetlen:
            iro.sor(ny.s('s4.p4.elemzetlen', n=len(sor.elemzetlen)), *sor.elemzetlen)
            iro.ures()


def _tomor(iro, ny, szakasz, resz, keret):
    K.olvasoi_bekezdes(iro, ny.s('s4.p5.bevezeto'))
    szavak = tuple(ny.s('s4.szonezet', szo=szo_iras(ny, szo), strong=szo.strong) for szo in resz.szavak)
    if resz.nyelv is Nyelv.GOROG:
        _bekezdes(iro, ny.s('s4.p5.gorog', szavak=szavak, szakasz=szakasz, pont=konfig.PONT_DOMEN,
                            forras=ny.nev('forras', 'B32')))
    else:
        _bekezdes(iro, ny.s('s4.p5.heber', szavak=szavak, forras=ny.nev('forras', 'B33')))


def _kiejtes(iro, ny, szakasz, resz, keret):
    K.olvasoi_bekezdes(iro, ny.s('s4.p10.bevezeto'))
    for szo in resz.szavak:
        _bekezdes(iro, ny.s('s4.p10.sor', szo=szo_iras(ny, szo), strong=szo.strong))


_PONTOK = {
    konfig.PONT_ALAPJELENTES: _alapjelentes,
    konfig.PONT_TEOLOGIAI: _teologiai,
    konfig.PONT_DOMEN: _domen,
    konfig.PONT_TOMOR: _tomor,
    konfig.PONT_KIEJTES: _kiejtes,
}


def _nyelvresz(iro, ny, szakasz, resz, keret):
    nyelv = resz.nyelv.value
    if not resz.szavak:
        iro.cimsor(3, ny.s(ny.kulcs('cim.szocikkek.nyelv', nyelv, 'ures')))
        iro.ures()
        K.olvasoi_bekezdes(iro, ny.s(ny.kulcs('s4.nyelv', nyelv, 'ures')))
        _bekezdes(iro, ny.s(ny.kulcs('s4.nyelv', nyelv, 'ures', 'megjegyzes')))
        return
    iro.cimsor(3, ny.s(ny.kulcs('cim.szocikkek.nyelv', nyelv), strongok=tuple(szo.strong for szo in resz.szavak)))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s(ny.kulcs('s4.nyelv', nyelv), szavak=tuple(szo_iras(ny, szo) for szo in resz.szavak),
                                 szakasz=szakasz, elso=min(resz.pontok), utolso=max(resz.pontok)))
    for pont in resz.pontok:
        if pont not in _PONTOK:
            continue   # a pont megjelenítője még nem készült el (részleges lap)
        _pont_cim(iro, ny, szakasz, pont)
        _PONTOK[pont](iro, ny, szakasz, resz, keret)


def _kozos(iro, ny, szakasz, modell, keret):
    iro.cimsor(3, ny.s('cim.szocikkek.kozos'))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('s4.kozos.bevezeto'))
    # a visszhang pontja egysoros mutató a Hatástörténet szakaszára; a címe és a horgonya a szakaszrendből jön
    _pont_cim(iro, ny, szakasz, konfig.PONT_VISSZHANG,
              ny.s('s4.p11.cim', szam=keret.rend.sorszam(HATASTORTENET), nev=ny.s('cim.hatastortenet.rovid'),
                   horgony=K.szakasz_horgony(keret, HATASTORTENET)))


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    szakasz = keret.rend.sorszam(AZONOSITO)
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    darabok, listak, foszotarak = [], [], []
    for nyelv, szotar in ((Nyelv.HEBER, konfig.FO_SZOTAR_HEBER), (Nyelv.GOROG, konfig.FO_SZOTAR_GOROG)):
        szavak = tuple(szo for szo in modell.szavak if szo.strong.heber == (nyelv is Nyelv.HEBER))
        if szavak:
            darabok.append(ny.s(ny.kulcs('s4.bevezeto.darab', nyelv.value), n=len(szavak)))
            listak.append(ny.s(ny.kulcs('s4.bevezeto.lista', nyelv.value),
                               szavak=tuple(szo_iras(ny, szo) for szo in szavak)))
            foszotarak.append(ny.s(ny.kulcs('s4.bevezeto.fo', nyelv.value), szotar=ny.nev('szotar', szotar)))
    K.olvasoi_bekezdes(iro, ny.s('s4.bevezeto', darabok=tuple(darabok), listak=tuple(listak), szakasz=szakasz,
                                 pont=konfig.PONT_MELYSEGI, foszotarak=tuple(foszotarak)))
    _bekezdes(iro, ny.s('s4.hatokor', n=len(modell.szavak)))
    _attekintes(iro, ny, szakasz, modell, keret)
    for resz in modell.nyelvek:
        _nyelvresz(iro, ny, szakasz, resz, keret)
    _kozos(iro, ny, szakasz, modell, keret)
    K.blokk_zar(iro, keret, AZONOSITO)
