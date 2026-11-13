"""lapgen.megjelenites.md.dontesi_ut — az „1. Döntési út” szakasz (1.1–1.5).

Minden látható mondat a sablontáblából jön (`d1.*` … `d15.*` kulcsok; a közös címek a melléklet `kz.*` kulcsai);
itt csak a szerkezet áll. A lenyíló blokkok egy sorban állnak, a jelölésük a sablonmondat része. A kizárási ok
címkéje és leírása, a funkció magyarázata és a nyitott kérdések kézi próza; a példavers idézet.
"""
from lapgen.ertekek import MaradtFajta
from lapgen.megjelenites.md import keret as K
from lapgen.szakaszok import KRITERIUM_HORGONY
from lapgen.szoveg import cim_horgony

AZONOSITO = 'dontesi_ut'
ERTELMEZES, MODSZERTAN = 'ertelmezes', 'modszertan'
ALPONT_TARGY, ALPONT_FORRASOK, ALPONT_KIESETT, ALPONT_MARADT, ALPONT_HATAR = 1, 2, 3, 4, 5
FEJLEC_FORRASOK = ('d12.fejlec.kereses', 'd12.fejlec.vers', 'd12.fejlec.mit')
FEJLEC_KIESETT = ('d13.fejlec.lepes', 'd13.fejlec.vers', 'd13.fejlec.miert')


def _alpont(iro, ny, szakasz, alpont, cim_kulcs):
    iro.cimsor(3, ny.s('cim.alpont', szakasz=szakasz, alpont=alpont, cim=ny.s(cim_kulcs)))
    iro.ures()


def _bekezdes(iro, szoveg):
    iro.sor(szoveg)
    iro.ures()


def _szo(ny, szo):
    """A lánc egy szava: a szótári alak a kiejtésével; szótári alak híján a Strong-száma."""
    if szo.alak is None:
        return ny.s('d12.szo.strong', strong=szo.strong)
    if szo.kiejtes is None:
        return ny.s('d12.szo.kiejtes_nelkul', alak=szo.alak)
    return ny.s('d12.szo', alak=szo.alak, kiejtes=szo.kiejtes)


def _targy(iro, ny, szakasz, targy):
    _alpont(iro, ny, szakasz, ALPONT_TARGY, 'cim.dontesi_ut.targy')
    # A kritérium szövege itt nem áll: egyetlen teljes helye a lap eleje (DT-F218n). Ide hivatkozás, a keresett
    # elemek megszámolva és mutató kerül: a szavak, a kizárás okai és a megmaradt helyek alpontjára.
    hatar = dict(cim=ny.s('fej.hatar.cim'), horgony=KRITERIUM_HORGONY, szakasz=szakasz, kiesett=ALPONT_KIESETT,
                 maradt=ALPONT_MARADT)
    if not (targy.heber or targy.gorog):
        _bekezdes(iro, ny.s('d11.targy.szavak_nelkul', **hatar))
        return
    elemek = []
    if targy.heber:
        elemek.append(ny.s('d11.elem.heber', n=targy.heber))
    if targy.gorog:
        elemek.append(ny.s('d11.elem.gorog', n=targy.gorog))
    if targy.szoparok:
        elemek.append(ny.s('d11.elem.szopar', n=targy.szoparok))
    _bekezdes(iro, ny.s('d11.targy', elemek=tuple(elemek), forrasok=ALPONT_FORRASOK, **hatar))


def _forrasok(iro, ny, szakasz, modell, keret):
    v = modell.vizsgalat
    _alpont(iro, ny, szakasz, ALPONT_FORRASOK, 'cim.dontesi_ut.forrasok')
    if modell.szavak:
        szavak = tuple(ny.s('d12.szo.jelentessel', szo=_szo(ny, szo), jelentes=szo.jelentes)
                       if szo.jelentes is not None else _szo(ny, szo) for szo in modell.szavak)
        _bekezdes(iro, ny.s('d12.szavak', szavak=szavak))
    iro.tabla_sor(tuple(ny.s(kulcs) for kulcs in FEJLEC_FORRASOK))
    iro.tabla_elvalaszto(len(FEJLEC_FORRASOK))
    for kereses in (v.keresesek or ()):
        iro.tabla_sor((ny.s('ertek.nev', n=ny.nev('halo', kereses.kulcs)), ny.s('d1.szam', n=kereses.versszam),
                       ny.s('ertek.nev', n=ny.nev('halo_leiras', kereses.kulcs))))
    if v.ajanlas:
        iro.tabla_sor((ny.s('d12.ajanlas.nev'), ny.s('d1.szam', n=v.ajanlas), ny.s('d12.ajanlas.mit')))
    iro.tabla_sor((ny.s('d12.osszesen.nev'), ny.s('d1.szam.kiemelt', n=v.osszes), ny.s('d12.osszesen.mit')))
    iro.ures()
    if v.keresesek is not None:
        _bekezdes(iro, ny.s('d12.forrassorok', motivum=keret.motivum,
                            horgony=cim_horgony(ny.s('kz.forrassorok.cim'))))


def _melleklet_horgony(ny, ok):
    """Az ok címsorának horgonya a mellékletben: ugyanabból a címből, amelyet a melléklet kiír."""
    return cim_horgony(ny.s('kz.ok_cim', ok=ok.ok, n=ok.versszam))


def _kiesett(iro, ny, szakasz, modell, keret):
    v = modell.vizsgalat
    _alpont(iro, ny, szakasz, ALPONT_KIESETT, 'cim.dontesi_ut.kiesett')
    iro.tabla_sor(tuple(ny.s(kulcs) for kulcs in FEJLEC_KIESETT))
    iro.tabla_elvalaszto(len(FEJLEC_KIESETT))
    iro.tabla_sor((ny.s('d13.osszes.nev'), ny.s('d1.szam.kiemelt', n=v.osszes),
                   ny.s('d13.osszes.miert', szakasz=szakasz, alpont=ALPONT_FORRASOK)))
    iro.tabla_sor((ny.s('d13.csoport.nev'), ny.s('d1.szam.kiemelt', n=v.csoport),
                   ny.s('d13.csoport.miert', okok=len(v.csoport_okok))))
    iro.tabla_sor((ny.s('d13.egyen.nev'), ny.s('d1.szam.kiemelt', n=v.egyen),
                   ny.s('d13.egyen.miert', okok=len(v.egyen_okok))))
    iro.tabla_sor((ny.s('d13.bent.nev'), ny.s('d1.szam.kiemelt', n=v.bent), ny.s('d13.bent.miert', helyek=v.helyek)))
    if v.nyitva:
        iro.tabla_sor((ny.s('d13.nyitva.nev'), ny.s('d1.szam.kiemelt', n=v.nyitva), ny.s('jel.nincs')))
    iro.ures()
    if v.nyitva:
        _bekezdes(iro, ny.s('d13.osszeadas.nyitva', bent=v.bent, csoport=v.csoport, egyen=v.egyen, nyitva=v.nyitva,
                            osszes=v.osszes))
    else:
        _bekezdes(iro, ny.s('d13.osszeadas', bent=v.bent, csoport=v.csoport, egyen=v.egyen, osszes=v.osszes,
                            nyitva=v.nyitva))
    if v.csoport_okok:
        iro.cimsor(4, ny.s('kz.cim.csoport'))
        iro.ures()
        for ok in v.csoport_okok:
            horgony = _melleklet_horgony(ny, ok)
            if ok.versszam == 1:
                melleklet = ny.s('d13.melleklet.egy', motivum=keret.motivum, horgony=horgony)
            else:
                melleklet = ny.s('d13.melleklet.mind', n=ok.versszam, motivum=keret.motivum, horgony=horgony)
            peldak = tuple(ny.s('d13.pelda', hely=p.igehely, szoveg=p.szoveg) for p in ok.peldak)
            if peldak:
                iro.sor(ny.s('d13.csoport.blokk', ok=ok.ok, n=ok.versszam, leiras=ok.leiras,
                             peldak=ny.s('d13.peldak', peldak=peldak), melleklet=melleklet))
            else:
                iro.sor(ny.s('d13.csoport.blokk.pelda_nelkul', ok=ok.ok, n=ok.versszam, leiras=ok.leiras,
                             melleklet=melleklet))
        iro.ures()
    if v.egyen_okok:
        iro.cimsor(4, ny.s('kz.cim.egyen'))
        iro.ures()
        for ok in v.egyen_okok:
            iro.sor(ny.s('d13.egyen.blokk', ok=ok.ok, n=ok.versszam, leiras=ok.leiras, versek=ok.versek,
                         motivum=keret.motivum, horgony=_melleklet_horgony(ny, ok)))
        iro.ures()


def _csoport_nev(ny, csoport):
    if csoport.fajta is MaradtFajta.TEMATIKUS:
        return ny.s('d14.nev.tematikus')
    if csoport.fajta is MaradtFajta.NEVES_SZOPAR:
        return ny.s('d14.nev.szopar', reszek=csoport.nevek)
    nev = ny.s('d14.nev.szavak', szavak=tuple(_szo(ny, szo) for szo in csoport.szavak))
    if len(csoport.szavak) == 1 and csoport.szavak[0].jelentes is not None:
        return ny.s('d14.nev.jelentessel', szo=nev, jelentes=csoport.szavak[0].jelentes)
    return nev


def _bontas(ny, csoport):
    """A helyek megoszlása: a Genezis, az Ószövetség többi könyve, az Újszövetség."""
    if len(csoport.helyek) == 1:
        if csoport.genezis:
            return ny.s('d14.egy.gen')
        return ny.s('d14.egy.usz') if csoport.ujszovetseg else ny.s('d14.egy.osz')
    reszek = []
    if csoport.genezis:
        reszek.append(ny.s('d14.resz.gen', n=csoport.genezis))
    if csoport.oszovetseg:
        reszek.append(ny.s('d14.resz.osz', n=csoport.oszovetseg))
    if csoport.ujszovetseg:
        reszek.append(ny.s('d14.resz.usz', n=csoport.ujszovetseg))
    return ny.s('d14.bontas', n=len(csoport.helyek), reszek=tuple(reszek))


def _maradt(iro, ny, szakasz, modell):
    _alpont(iro, ny, szakasz, ALPONT_MARADT, 'cim.dontesi_ut.maradt')
    for csoport in modell.maradt:
        helyek = tuple(ny.s('d14.hely', horgony=h.horgony, hely=h.igehely, magyarazat=h.magyarazat)
                       if h.magyarazat is not None else ny.s('d14.hely.magyarazat_nelkul', horgony=h.horgony,
                                                             hely=h.igehely) for h in csoport.helyek)
        iro.sor(ny.s('d14.blokk', nev=_csoport_nev(ny, csoport), n=len(csoport.helyek), bontas=_bontas(ny, csoport),
                     helyek=helyek))
    iro.ures()


def _hatar(iro, ny, szakasz, modell, keret):
    _alpont(iro, ny, szakasz, ALPONT_HATAR, 'cim.dontesi_ut.hatar')
    if modell.hataresetek:
        _bekezdes(iro, ny.s('d15.hataresetek', helyek=tuple(
            ny.s('d15.hatareset', hely=h.igehely, horgony=h.horgony, megb=ny.nev('megbizhatosag', h.megbizhatosag))
            for h in modell.hataresetek)))
    if modell.kerdesek:
        for kerdes in modell.kerdesek:
            iro.sor(ny.s('d15.kerdes', kerdes=kerdes))
        iro.ures()
        _bekezdes(iro, ny.s('d15.kifejtes', e_szam=keret.rend.sorszam(ERTELMEZES),
                            e_cim=ny.s(keret.rend.cim_kulcs(ERTELMEZES)), m_szam=keret.rend.sorszam(MODSZERTAN),
                            m_cim=ny.s(keret.rend.cim_kulcs(MODSZERTAN))))
    if not modell.hataresetek and not modell.kerdesek:
        _bekezdes(iro, ny.s('d15.nincs'))


def megjelenit(iro, modell, keret, forrasok):
    ny, v = keret.ny, modell.vizsgalat
    szakasz = keret.rend.sorszam(AZONOSITO)
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    # a szakasz elején egy magyarázó sor áll (a számoló bevezető); a korábbi második, hatókör-sor kimaradt (DT-F218n)
    K.olvasoi_bekezdes(iro, ny.s('d1.bevezeto', osszes=v.osszes, bent=v.bent))
    _targy(iro, ny, szakasz, modell.targy)
    _forrasok(iro, ny, szakasz, modell, keret)
    _kiesett(iro, ny, szakasz, modell, keret)
    _maradt(iro, ny, szakasz, modell)
    _hatar(iro, ny, szakasz, modell, keret)
    K.blokk_zar(iro, keret, AZONOSITO)
