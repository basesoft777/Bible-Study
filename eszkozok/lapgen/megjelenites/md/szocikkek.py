"""lapgen.megjelenites.md.szocikkek — a „Szótári háttér” szakasz: a váz, az áttekintő tábla és a szótári pontok.

Minden látható mondat a sablontáblából jön (`s4.*` kulcsok); itt csak a szerkezet áll. A pontok száma és rendje a
lapmodellből (a szótári pontok táblájából), a pont neve a névtáblából jön. A még el nem készült pont megjelenítője
hiányzik a `_PONTOK` táblából: a lap ilyenkor részleges, a pont kimarad.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.szamitas.szocikkek import Nyelv

AZONOSITO = 'szocikkek'
HATASTORTENET, ELOFORDULASOK = 'hatastortenet', 'elofordulasok'
FEJLEC_ATTEKINTES = ('s4.att.fejlec.szo', 's4.att.fejlec.jelentes', 's4.att.fejlec.lxx', 's4.att.fejlec.helyek')
FEJLEC_SECE = ('s4.p7.fejlec.szo', 's4.p7.fejlec.kiejtes', 's4.p7.fejlec.strong', 's4.p7.fejlec.jelentes')
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


def jelentes(ny, j, tablaban=False):
    """A rövid jelentés: magyarul; magyar híján az angol eredeti, „fordításra vár” jelöléssel; ha az sincs, a
    hiány kimondva (táblacellában a hiány jele áll)."""
    if j.magyar is not None:
        return ny.s('s4.felulvizsgalat', szoveg=j.magyar) if j.elavult else j.magyar
    if j.angol is not None:
        return ny.s('s4.forditasra_var', szoveg=j.angol)
    return ny.s('jel.nincs') if tablaban else ny.s('s4.jelentes.nincs')


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


def szo_nevelovel(ny, szo):
    """A szó írással és kiejtéssel, határozott névelővel (a névelő a kiejtés szerint): „az אָבַל (ával)”."""
    if szo.alak is None:
        return ny.s('d12.szo.strong', strong=szo.strong)
    if szo.kiejtes is None:
        return ny.s('s4.szo.nevelovel.kiejtes_nelkul', alak=szo.alak)
    return ny.s('s4.szo.nevelovel', alak=szo.alak, kiejtes=szo.kiejtes)


def _szo_nagy_nevelovel(ny, szo):
    """Mondatkezdő alak: a névelő nagybetűvel („Az אָרַר (árar)”)."""
    if szo.alak is None:
        return ny.s('d12.szo.strong', strong=szo.strong)
    if szo.kiejtes is None:
        return ny.s('s4.szo.nevelovel.nagy.kiejtes_nelkul', alak=szo.alak)
    return ny.s('s4.szo.nevelovel.nagy', alak=szo.alak, kiejtes=szo.kiejtes)


def _alany(ny, szavak):
    """Mondatkezdő felsorolás: az első szó nagybetűs névelővel, a többi kisbetűssel."""
    return tuple(_szo_nagy_nevelovel(ny, szo) if i == 0 else szo_nevelovel(ny, szo) for i, szo in enumerate(szavak))


def _jelenteses(ny, j, szo):
    return ny.s('s4.szo.jelentessel', szo=szo, jelentes=j.jelentes) if j.jelentes is not None else szo


def _helyek(ny, helyek, tovabbi=False):
    elemek = [ny.s('s4.hely', hely=hely) for hely in helyek]
    if tovabbi:
        elemek.append(ny.s('s4.tovabbiak'))
    return tuple(elemek)


def _sece_bevezeto(ny, resz):
    nyelv, sece = resz.nyelv.value, resz.sece
    mondatok = [ny.s(ny.kulcs('s4.p7.bevezeto', nyelv))]
    for cs in sece.csaladok:
        mondatok.append(ny.s(
            's4.p7.csalad', szo=_szo_nagy_nevelovel(ny, cs.szo),
            megfelelo=_jelenteses(ny, cs.megfelelo, szo_iras(ny, cs.megfelelo.szo)),
            tagok=tuple(_jelenteses(ny, t, szo_nevelovel(ny, t.szo)) for t in cs.tagok), helyek=_helyek(ny, cs.helyek)))
    for p in sece.pontosak:
        if resz.nyelv is Nyelv.HEBER:
            mondatok.append(ny.s('s4.p7.pontos.heber' if len(p.megfelelok) > 1 else 's4.p7.pontos.heber.egy',
                                 szavak=_alany(ny, p.szavak), megfelelok=tuple(szo_iras(ny, m) for m in p.megfelelok),
                                 helyek=_helyek(ny, p.helyek)))
        else:
            mondatok.append(ny.s('s4.p7.pontos.gorog' if len(p.szavak) > 1 else 's4.p7.pontos.gorog.egy',
                                 szavak=_alany(ny, p.szavak),
                                 megfelelok=tuple(szo_nevelovel(ny, m) for m in p.megfelelok),
                                 helyek=_helyek(ny, p.helyek, p.tovabbi)))
    if sece.maradek.value != 'nincs':
        mondatok.append(ny.s(ny.kulcs('s4.p7.zaro', sece.maradek.value)))
    return ny.s('s4.mondatok', mondatok=tuple(mondatok))


def _sece_sor(ny, sor):
    if not sor.strongok:
        return (sor.szo, ny.s('jel.nincs'), ny.s('jel.nincs'), ny.s('jel.nincs'))
    szo = ny.s('s4.p7.szo.motivum', szo=sor.szo) if sor.motivum_szava else sor.szo
    kiejtes = sor.kiejtes if sor.kiejtes is not None else ny.s('jel.nincs')
    if len(sor.strongok) == 1:
        return (szo, kiejtes, ny.s('d12.szo.strong', strong=sor.strongok[0]),
                jelentes(ny, sor.jelentesek[0], tablaban=True))
    return (szo, kiejtes, ny.s('s4.p7.strongok', strongok=sor.strongok),
            ny.s('s4.p7.jelentesek', elemek=tuple(
                ny.s('e2.jelentes.tokenenkent', strong=st, tartalom=jelentes(ny, j, tablaban=True))
                for st, j in zip(sor.strongok, sor.jelentesek))))


def _masik_nyelv(iro, ny, szakasz, resz, keret):
    nyelv = resz.nyelv.value
    K.olvasoi_bekezdes(iro, _sece_bevezeto(ny, resz))
    for tabla in resz.sece.tablak:
        if tabla.sorok is None:
            _bekezdes(iro, ny.s(ny.kulcs('s4.p7.nincs_lista', nyelv), strong=tabla.szo.strong))
            continue
        if tabla.szo.alak is None:
            cim = ny.s(ny.kulcs('s4.p7.tabla_cim', nyelv, 'csak_strong'), strong=tabla.szo.strong, n=len(tabla.sorok))
        else:
            cim = ny.s(ny.kulcs('s4.p7.tabla_cim', nyelv), strong=tabla.szo.strong, szo=szo_iras(ny, tabla.szo),
                       n=len(tabla.sorok))
        _bekezdes(iro, cim)
        iro.tabla_sor(tuple(ny.s(kulcs) for kulcs in FEJLEC_SECE))
        iro.tabla_elvalaszto(len(FEJLEC_SECE))
        for sor in tabla.sorok:
            iro.tabla_sor(_sece_sor(ny, sor))
        iro.ures()
    if resz.sece.tablak:
        _bekezdes(iro, ny.s('s4.p7.labjegyzet', heber=ny.nev('forras', 'B15'), gorog=ny.nev('forras', 'B14')))


def _versenkenti_bevezeto(ny, nyelv, v):
    """A versenkénti pont összegző mondata: lelet (mely szavak jelentése egyértelmű a helyén), és ahol az elemszám
    engedi, következtetés."""
    vannak = [s for s in v.szavak if s.helyek]
    if not vannak:
        return ny.s('s4.p9.bevezeto.ures')
    egy = [s for s in vannak if s.egy == s.helyek]
    tobb = [s for s in vannak if s.egy < s.helyek]
    if not tobb:
        lelet = ny.s(ny.kulcs('s4.p9.lelet.mind', nyelv), n=v.hely_szam)
    else:
        kivetelek = tuple(ny.s('s4.p9.kivetel', szo=szo_nevelovel(ny, s.szo), helyek=s.nem_egy) for s in tobb)
        if egy:
            lelet = ny.s(ny.kulcs('s4.p9.lelet.vegyes', nyelv), egy=tuple(szo_nevelovel(ny, s.szo) for s in egy),
                         tobb=kivetelek, n=len({hely for s in tobb for hely in s.nem_egy}), ossz=v.hely_szam)
        else:
            lelet = ny.s(ny.kulcs('s4.p9.lelet.egyik_sem', nyelv), tobb=kivetelek)
    if v.fok is None:
        return lelet
    return ny.s('s4.p9.kovetkeztetessel', lelet=lelet, kov=ny.s(ny.kulcs('s4.p9.kov', v.fok.value)))


def _versenkent(iro, ny, szakasz, resz, keret):
    nyelv, v = resz.nyelv.value, resz.versenkent
    K.olvasoi_bekezdes(iro, _versenkenti_bevezeto(ny, nyelv, v))
    _bekezdes(iro, ny.s('s4.p9.mutato', szam=keret.rend.sorszam(ELOFORDULASOK),
                        cim=ny.s(keret.rend.cim_kulcs(ELOFORDULASOK)),
                        horgony=K.szakasz_horgony(keret, ELOFORDULASOK),
                        forras=ny.nev('forras', 'B32' if resz.nyelv is Nyelv.GOROG else 'B33')))
    for s in v.szavak:
        if not s.helyek:
            _bekezdes(iro, ny.s(ny.kulcs('s4.p9.sor.nincs', nyelv), szo=szo_iras(ny, s.szo), strong=s.szo.strong))
            continue
        reszek = [ny.s(kulcs, n=n) for kulcs, n in (('s4.p9.egy', s.egy), ('s4.p9.tobb', s.tobb),
                                                    ('s4.p9.nincs', s.helyek - s.egy - s.tobb)) if n]
        _bekezdes(iro, ny.s(ny.kulcs('s4.p9.sor', nyelv), szo=szo_iras(ny, s.szo), strong=s.szo.strong, n=s.helyek,
                            reszek=tuple(reszek)))


_PONTOK = {
    konfig.PONT_ALAPJELENTES: _alapjelentes,
    konfig.PONT_TEOLOGIAI: _teologiai,
    konfig.PONT_DOMEN: _domen,
    konfig.PONT_TOMOR: _tomor,
    konfig.PONT_MASIK_NYELV: _masik_nyelv,
    konfig.PONT_VERSENKENT: _versenkent,
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
