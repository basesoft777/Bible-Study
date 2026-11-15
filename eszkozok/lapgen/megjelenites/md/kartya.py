"""lapgen.megjelenites.md.kartya — a 4.2 Mélységi szócikk kártyái.

Minden látható mondat a sablontáblából jön (`s4.p2.*`); a szótári szöveg a lapmodell darabjaiból: az idézet-darab
látható szöveg, a jelölés-darab a fajtája szerinti sablonsor (az irányjel szerkezeti jel). A HTML-megjegyzés (az
apparátus jelölője) proveniencia.
"""
from lapgen.ertekek import FeloldasFajta, JelFajta
from lapgen.megjelenites.md import iro as I
from lapgen.megjelenites.md import keret as K
from lapgen.szamitas.kartya import AppFajta, OlvasoiFajta, PontFajta, Tartalom
from lapgen.szoveg import prov

_SZOCIKK_KULCS = {1: 's4.p2.szocikk.1', 2: 's4.p2.szocikk.2', 3: 's4.p2.szocikk.3', 4: 's4.p2.szocikk.4',
                  5: 's4.p2.szocikk.5', 6: 's4.p2.szocikk.6'}
_ABBR = {FeloldasFajta.JAHVE: 's4.p2.jel.abbr.jahve', FeloldasFajta.ALTALANOS: 's4.p2.jel.abbr.altalanos'}
_EGYSZERU = {JelFajta.MARK_ZAR: 's4.p2.jel.mark.zar', JelFajta.ABBR_ZAR: 's4.p2.jel.abbr.zar',
             JelFajta.NINCS_KAROLI: 's4.p2.jel.nincs_karoli', JelFajta.FELULVIZSGALAT: 's4.p2.jel.felulvizsgalat'}
_TARTALOM = {Tartalom.KULON: 's4.p2.olv.sor.kulon', Tartalom.CSAK_ALAK_THAYER: 's4.p2.olv.sor.csak_alak.ures',
             Tartalom.CSAK_PARHUZAM: 's4.p2.olv.sor.csak_parhuzam', Tartalom.FORDITASRA_VAR: 's4.p2.olv.sor.forditasra_var'}


def darabok(ny, jelek, szo_fn):
    """A szegmentált idézet darabjai a lapra: Lathato és (az irányjelnél) Jel."""
    ki = []
    for d in jelek:
        if d.fajta is JelFajta.IDEZET:
            ki.append(d.ertek)
        elif d.fajta is JelFajta.MARK_NYIT:
            ki.append(ny.s('s4.p2.jel.mark', vers=d.vers))
        elif d.fajta is JelFajta.ABBR_NYIT:
            if d.feloldas is FeloldasFajta.CIMSZO:
                ki.append(ny.s('s4.p2.jel.abbr.cimszo', szo=szo_fn()))
            elif d.feloldas is FeloldasFajta.JAHVE_CIMSZO:
                ki.append(ny.s('s4.p2.jel.abbr.jahve_cimszo', szo=szo_fn()))
            else:
                ki.append(ny.s(_ABBR[d.feloldas]))
        elif d.fajta in _EGYSZERU:
            ki.append(ny.s(_EGYSZERU[d.fajta]))
        elif d.fajta is JelFajta.LRM:
            ki.append(I.IRANYJEL)
        elif d.fajta is JelFajta.KAROLI:
            ki.append(_karoli(ny, d.karoli))
        elif d.fajta is JelFajta.KIEJTES:
            ki.append(ny.s('s4.p2.jel.kiejtes', kiejtes=d.ertek))
        elif d.fajta is JelFajta.CSONK:
            ki.append(ny.s('s4.p2.jel.csonk.tapadt' if d.tapadt else 's4.p2.jel.csonk'))
        else:
            raise ValueError(d.fajta)
    return ki


def _karoli(ny, k):
    """A Károli-számozás jelölése: a hivatkozás Károli-alakja (könyvvel, fejezettel vagy csak a vers) és az eredeti szám."""
    if k.konyv is not None:
        return ny.s('s4.p2.jel.karoli.konyv', konyv=k.konyv, fej=k.fej, vers=k.vers, efej=k.eredeti_fej,
                    evers=k.eredeti_vers)
    if k.fej is not None:
        return ny.s('s4.p2.jel.karoli.fejezet', fej=k.fej, vers=k.vers, efej=k.eredeti_fej, evers=k.eredeti_vers)
    return ny.s('s4.p2.jel.karoli.vers', vers=k.vers, efej=k.eredeti_fej, evers=k.eredeti_vers)


def _gl(ny, glossza):
    """A meghatározás a lapra (E2): a forrás részletei között a kihagyás helye, a csonkolt meghatározás után a
    csonkolás jele sablonsor."""
    if glossza is None:
        return None
    ki = glossza.reszek[0]
    for resz in glossza.reszek[1:]:
        ki = ny.s('s4.p2.glossza.kihagyas', elotte=ki, utana=resz)
    if glossza.csonk:
        ki = ny.s('s4.p2.glossza.csonk', glossza=ki)
    return ny.s('s4.felulvizsgalat', szoveg=ki) if glossza.felulvizsgalat else ki


def _versek(ny, versek):
    ki, elozo = [], None
    for v in versek:
        ki.append(ny.s('s4.p2.vers.resz', vers=v) if v.konyv == elozo else ny.s('s4.p2.vers', vers=v))
        elozo = v.konyv
    return ny.s('lista.vesszo', elemek=tuple(ki))


def _szocikk_nev(ny, sorszam, arami):
    nev = ny.s(_SZOCIKK_KULCS.get(sorszam, 's4.p2.szocikk.tovabbi'))
    return ny.s('s4.p2.szocikk.arami', nev=nev) if arami else nev


def _pont_nev(ny, nev):
    if nev.fajta is PontFajta.CSAK_ALAKKENT:
        pont = ny.s('s4.p2.pont.csak_alakkent')
    elif nev.fajta is PontFajta.FEJ_ELEJE:
        pont = ny.s('s4.p2.pont.fej_eleje', glossza=_gl(ny, nev.glossza))
    elif nev.fajta is PontFajta.TAGOLATLAN:
        pont = (ny.s('s4.p2.pont.tagolatlan', glossza=_gl(ny, nev.glossza)) if nev.glossza is not None
                else ny.s('s4.p2.pont.tagolatlan.ures'))
    elif nev.glossza is None:
        pont = ny.s('s4.p2.pont.jel', jel=nev.jel)
    else:
        pont = ny.s('s4.p2.pont.gondolatjel' if nev.gondolatjel else 's4.p2.pont.szokoz', jel=nev.jel,
                    glossza=_gl(ny, nev.glossza))
    if nev.szocikk_sorszam and nev.fajta in (PontFajta.SZAKASZ, PontFajta.TAGOLATLAN):
        pont = ny.s('s4.p2.pont.szocikkel', szocikk=_szocikk_nev(ny, nev.szocikk_sorszam, nev.szocikk_arami),
                    pont=pont)
    if nev.bizonytalan:
        pont = ny.s('s4.p2.pont.bizonytalan', pont=pont,
                    okok=tuple(ny.s(ny.kulcs('s4.p2.bizonytalan', ok.value)) for ok in nev.bizonytalan))
    return pont


def _olvasoi_sor(iro, ny, sor):
    behuz = I.behuzas(sor.behuzas)
    if sor.fajta is OlvasoiFajta.SZOCIKK:
        iro.sor(behuz, ny.s('s4.p2.olv.szocikk', nev=_szocikk_nev(ny, sor.sorszam, sor.arami)))
        return
    if sor.fajta is OlvasoiFajta.FEJ_ELEJE:
        iro.sor(behuz, ny.s('s4.p2.olv.fej_eleje.felkover' if sor.felkover else 's4.p2.olv.fej_eleje.sima',
                            glossza=_gl(ny, sor.glossza)))
        return
    if sor.fajta is OlvasoiFajta.TAGOLATLAN:
        kulcs = 's4.p2.olv.tagolatlan.felkover' if sor.felkover else 's4.p2.olv.tagolatlan.sima'
        iro.sor(behuz, ny.s(kulcs, glossza=_gl(ny, sor.glossza)) if sor.glossza is not None else ny.s(ny.kulcs(kulcs, 'ures')))
        return
    if sor.felkover:
        jel = ny.s('s4.p2.olv.jel.felkover', jel=sor.jel)
    elif sor.jel_szam:
        jel = ny.s('s4.p2.olv.jel.szam', jel=sor.jel_nyers)
    else:
        jel = sor.jel
    if sor.tartalom is Tartalom.CSAK_ALAK:
        mondat = (ny.s('s4.p2.olv.sor.csak_alak', jel=jel, n=sor.hely_db) if sor.hely_db
                  else ny.s('s4.p2.olv.sor.csak_alak.ures', jel=jel))
    elif sor.tartalom in _TARTALOM:
        mondat = ny.s(_TARTALOM[sor.tartalom], jel=jel)
    else:
        mondat = ny.s('s4.p2.olv.sor.gondolatjel' if sor.gondolatjel else 's4.p2.olv.sor.szokoz', jel=jel,
                      glossza=_gl(ny, sor.glossza))
    iro.sor(behuz, mondat)


def _helyein(iro, ny, kartya):
    if kartya.helyein:
        csop = tuple(ny.s('s4.p2.helyein.csoport', versek=_versek(ny, c.versek),
                          nevek=tuple(_pont_nev(ny, n) for n in c.nevek)) for c in kartya.helyein)
        reszek = [ny.s('s4.p2.helyein', csoportok=csop)]
    else:
        reszek = [ny.s('s4.p2.helyein.ures')]
    for kulcs, versek in (('nem_idezi', kartya.nem_idezett), ('tartomany', kartya.tartomanyban),
                          ('pont_nelkul', kartya.pont_nelkul)):
        if versek:
            reszek.append(ny.s(ny.kulcs('s4.p2.helyein', kulcs), versek=_versek(ny, versek)))
    iro.sor(*reszek)
    iro.ures()


def _futam(iro, ny, oc, szo_fn):
    iro.sor(I.DETAILS_NYIT)
    if len(oc.jelek) == 1:
        hiv = ny.s('s4.p2.app.hiv', n=oc.hely_db) if oc.hely_db else ny.s('s4.p2.app.hiv.nincs')
        cim = (ny.s('s4.p2.app.summary.egy', jel=oc.jelek[0], glossza=_gl(ny, oc.glosszak[0]), hiv=hiv)
               if oc.glosszak else ny.s('s4.p2.app.summary.egy.ures', jel=oc.jelek[0], hiv=hiv))
    elif not oc.glosszak:
        cim = ny.s('s4.p2.app.summary.tobb.ures', elso=oc.jelek[0], utolso=oc.jelek[1], n=len(oc.vazlatok))
    else:
        cim = ny.s('s4.p2.app.summary.tobb.tovabb' if len(oc.glosszak) > 4 else 's4.p2.app.summary.tobb',
                   elso=oc.jelek[0], utolso=oc.jelek[1], n=len(oc.vazlatok), glosszak=tuple(_gl(ny, g) for g in oc.glosszak[:4]))
    iro.sor(I.SUMMARY_NYIT, cim, I.SUMMARY_ZAR)
    iro.ures()
    for v in oc.vazlatok:
        eleje = ny.s('s4.p2.app.vazlat.eleje', jel=v.jel)
        if v.cimke is not None:
            iro.sor(eleje, v.cimke)
        else:
            iro.sor(eleje, *darabok(ny, v.darabok, szo_fn))
    iro.ures()
    iro.sor(I.DETAILS_ZAR)


def _app_elem(iro, ny, elem, kartya, szo_fn):
    if elem.fajta is AppFajta.FEJCIM:
        kulcs = 's4.p2.app.fejcim' if elem.van_cimszo else 's4.p2.app.fejcim.ures'
        if elem.arami:
            kulcs = ny.kulcs(kulcs, 'arami')
        if elem.van_cimszo:
            iro.sor(ny.s(ny.kulcs(kulcs, 'eleje'), szam=elem.szam), *darabok(ny, elem.darabok, szo_fn),
                    ny.s(ny.kulcs(kulcs, 'vege'), strong=kartya.strong, i=elem.sorszam, n=elem.osszes))
        else:
            iro.sor(ny.s(kulcs, szam=elem.szam, strong=kartya.strong, i=elem.sorszam, n=elem.osszes))
    elif elem.fajta is AppFajta.FEJ:
        iro.sor(ny.s('s4.p2.app.fej.eleje'), *darabok(ny, elem.darabok, szo_fn))
    elif elem.fajta is AppFajta.SZAKASZ:
        iro.sor(ny.s('s4.p2.app.szakasz.cimke', jel=elem.jel, cimke=_gl(ny, elem.cim)) if elem.cim is not None
                else ny.s('s4.p2.app.szakasz', jel=elem.jel))
        iro.ures()
        iro.sor(ny.s('s4.p2.app.idezet.eleje'), *darabok(ny, elem.darabok, szo_fn))
    else:
        _futam(iro, ny, elem.futam, szo_fn)
    iro.ures()


def kartya(iro, ny, kartya, szo, szo_iras, allapot_fn):
    """Egy szó kártyája: a cím, az olvasói réteg és az összecsukott apparátus; a görög kártya alatt a doménsor."""
    def szo_fn():
        return szo_iras(ny, szo)
    nyelv = 'heber' if kartya.strong.heber else 'gorog'
    iro.cimsor(5, ny.s(ny.kulcs('s4.p2.cim', nyelv), strong=kartya.strong, szo=szo_iras(ny, szo)))
    iro.ures()
    iro.sor(ny.s(ny.kulcs('s4.p2.rend', nyelv)))
    iro.ures()
    for sor in kartya.olvasoi:
        _olvasoi_sor(iro, ny, sor)
    iro.ures()
    _helyein(iro, ny, kartya)
    iro.sor(prov('APPARATUS-KEZDET: {}', kartya.strong))
    iro.ures()
    iro.sor(I.DETAILS_NYIT)
    iro.sor(I.SUMMARY_NYIT, ny.s('s4.p2.app.cim'), I.SUMMARY_ZAR)
    iro.ures()
    if kartya.forras is not None:
        iro.sor(ny.s('s4.p2.app.thayer_forras'), kartya.forras)
        iro.ures()
    for elem in kartya.apparatus:
        _app_elem(iro, ny, elem, kartya, szo_fn)
    if kartya.megjegyzes:
        reszek = tuple(ny.s('s4.p2.app.tartomany', vers=m.vers, jel=m.jel, kezdo=m.kezdo, veg=m.veg, nyers=m.nyers,
                            folytatas=m.folytatas) for m in kartya.megjegyzes)
        iro.sor(ny.s('s4.p2.app.megjegyzes', reszek=reszek))
        iro.ures()
    iro.sor(ny.s(ny.kulcs('s4.p2.app.teljes', nyelv), strong=kartya.strong))
    iro.ures()
    iro.sor(I.DETAILS_ZAR)
    iro.ures()
    iro.sor(prov('APPARATUS-VÉGE: {}', kartya.strong))
    iro.ures()
    if kartya.ubs is not None:
        elemek = tuple(ny.s('s4.p2.ubs.elem', kod=e.kod, glossza=allapot_fn(ny, e.szoveg)) for e in kartya.ubs)
        iro.sor(ny.s('s4.p2.ubs', elemek=elemek) if elemek else ny.s('s4.p2.ubs.nincs'))
        iro.ures()


def melysegi(iro, ny, resz, szo_iras, allapot_fn):
    """A 4.2 pont egy nyelvrészen."""
    nyelv = resz.nyelv.value
    K.olvasoi_bekezdes(iro, ny.s(ny.kulcs('s4.p2.bevezeto', nyelv)))
    iro.sor(ny.s(ny.kulcs('s4.p2.bevezeto.dolt', nyelv)))
    iro.ures()
    szavak = {szo.strong: szo for szo in resz.szavak}
    for k in resz.kartyak:
        kartya(iro, ny, k, szavak[k.strong], szo_iras, allapot_fn)
