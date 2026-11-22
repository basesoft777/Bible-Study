"""lapgen.megjelenites.md.kolofon — a Kolofon (S8d).

Minden látható mondat a sablontáblából (`kolofon.*`), minden név a névtáblából (a forrásnevek: `kolofon_szotar`,
`irod_adat`, `irod_kulso`; az azonosság típusa: `azonossag_tipus`; a kiadási adatok: `kiadasi_adat`), minden licenc a
licencleltárból (idézet) vagy a licenc olvasói alakjának sablonsorából jön (a 12. szakasz `irod.licenc.*` sorai). A
szakaszok neve és a lap eleji meghatározás horgonya a szakaszrendből (GK-10). A „Negatív kritérium” sor helyén
hivatkozás áll a lap elejére (DT874, 9. tétel; a kritérium egyetlen teljes helye a lap eleje).
"""
from lapgen.megjelenites.md import idezes as md_idezes
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import VIZSZINTES_VONAL
from lapgen.szakaszok import KRITERIUM_HORGONY
from lapgen.szamitas.kolofon import Szerzoseg

AZONOSITO = 'kolofon'
KIADASI_ADAT = 'kiadasi_adat'
# a motívumtábla kézi mezőinek helye a táblában: a mező a cím előtt (ui_cimke) vagy a cím után áll
_ELOTTE = ('ui_cimke',)
_CIM_UTAN = ('tema', 'pardes_szint')


def _kiadasi(ny, kulcs):
    return ny.nev(KIADASI_ADAT, kulcs)


def _datumok(ny, datumok):
    """Egy dátum, vagy a dátumok tartománya (azonos hónapban a vég napja, különben a teljes vég)."""
    elso, utolso = datumok[0], datumok[-1]
    if elso == utolso:
        return ny.s('kolofon.datum', datum=elso)
    if (elso.year, elso.month) == (utolso.year, utolso.month):
        return ny.s('kolofon.datum.tartomany', elso=elso, nap=utolso)
    return ny.s('kolofon.datum.tartomany.hosszu', elso=elso, utolso=utolso)


def _szerzoseg(ny, m):
    if m.szerzoseg is Szerzoseg.GENERALT:
        torzs = ny.s('kolofon.szerzoseg.generalt')
    else:
        resek = [ny.s('cim.' + r) for r in m.resek]
        if m.szerzoseg is Szerzoseg.KIADATLAN:
            torzs = ny.s('kolofon.szerzoseg.kiadatlan', resek=resek)
        else:
            if m.proza_modell is not None:
                kezdet = ny.s('kolofon.szerzoseg.ai', resek=resek, modell=m.proza_modell)
            else:
                kezdet = ny.s('kolofon.szerzoseg.kezi', resek=resek)
            torzs = ny.s('kolofon.szerzoseg.kiadott', kezdet=kezdet,
                         jovahagyas=ny.s('kolofon.jovahagyas.korabbi', datum=m.jovahagyas))
    return ny.s('kolofon.szerzoseg', torzs=torzs)


def _hogyan(ny, m, keret):
    alap = dict(szerzo=_kiadasi(ny, 'szerzo'), lexikon=_kiadasi(ny, 'lexikon_cim'), cim=m.cim,
                motivum=keret.motivum, url=_kiadasi(ny, 'kanonikus_alap'), doi=_kiadasi(ny, 'nyilt_mag_doi'))
    if m.kiadasok:
        u = m.kiadasok[-1]
        return ny.s('kolofon.hogyan', kiadas=u.szam, datum=u.datum, **alap)
    if keret.datum is not None:
        return ny.s('kolofon.hogyan.kiadatlan', datum=keret.datum, **alap)
    return ny.s('kolofon.hogyan.kiadatlan.datum_nelkul', **alap)


def _hatokor(ny, m):
    mondatok = [ny.s('kolofon.hatokor.alap')]
    if m.kozel_keleti:
        mondatok.append(ny.s('kolofon.hatokor.kozel_keleti'))
        if m.kozel_keleti_emlites is not None:
            mondatok.append(ny.s('kolofon.hatokor.emlites', emlites=m.kozel_keleti_emlites))
    return ny.s('kolofon.hatokor', mondatok=mondatok)


def _ertek(ny, ertek):
    return ertek if ertek is not None else ny.s('kolofon.ures')


def _tabla(iro, ny, m, keret):
    mezok = dict(m.mezok)
    sorok = [('kolofon.mezo.id', ny.s('kolofon.ertek.motivum', motivum=keret.motivum))]
    sorok += [('kolofon.mezo.' + mezo, _ertek(ny, mezok.get(mezo))) for mezo in _ELOTTE]
    sorok.append(('kolofon.mezo.cim', m.cim))
    sorok += [('kolofon.mezo.' + mezo, _ertek(ny, mezok.get(mezo))) for mezo in _CIM_UTAN]
    if m.kiadasok:
        statusz = ny.s('kolofon.statusz', kiadas=m.kiadasok[-1].szam, datum=m.kiadasok[-1].datum)
    else:
        statusz = ny.s('kolofon.nincs_kiadva')
    sorok.append(('kolofon.mezo.statusz', statusz))
    sorok.append(('kolofon.mezo.meghatarozas', _ertek(ny, m.meghatarozas)))
    sorok.append(('kolofon.mezo.azonossag',
                  ny.s('kolofon.ertek.nev', nev=ny.nev('azonossag_tipus', m.azonossag)) if m.azonossag is not None else ny.s('kolofon.ures')))
    sorok.append(('kolofon.mezo.kriterium', ny.s('kolofon.ertek.kriterium', cim=ny.s('fej.hatar.cim'),
                                                 horgony=KRITERIUM_HORGONY)))
    sorok.append(('kolofon.mezo.folerendelt', m.folerendelt))
    sorok.append(('kolofon.mezo.sablon_verzio', mezok.get('sablon_verzio') or ny.s('kolofon.nincs_rogzitve')))
    if keret.datum is not None:
        sorok.append(('kolofon.mezo.generalva', ny.s('kolofon.ertek.datum', datum=keret.datum)))
    if m.kiadasok:
        sorok.append(('kolofon.mezo.kiadas', ny.s('kolofon.ertek.szam', n=m.kiadasok[-1].szam)))
        sorok.append(('kolofon.mezo.proza_modell', m.proza_modell if m.proza_modell is not None
                      else ny.s('kolofon.nincs_rogzitve')))
    else:
        sorok.append(('kolofon.mezo.kiadas', ny.s('kolofon.nincs_kiadva')))
        sorok.append(('kolofon.mezo.proza_modell', ny.s('kolofon.nincs_kiadva')))
    iro.tabla_sor((ny.s('kolofon.tabla.mezo'), ny.s('kolofon.tabla.ertek')))
    iro.tabla_elvalaszto(2)
    for cimke, ertek in sorok:
        iro.tabla_sor((ny.s(cimke), ertek))
    # a szerkesztői sor áll elöl, utána a modell-lektoré (a felhasználó, 2026-11-12: „de ember hagyja jóvá és változtat”)
    if m.javitasok:
        iro.tabla_sor((ny.s('kolofon.mezo.szerkesztoi'),
                       ny.s('kolofon.szerkesztoi', datum=_datumok(ny, m.javitasok))))
    if m.lektor is not None:
        cimke = ny.s('kolofon.mezo.lektor', modell=m.lektor.modell)
        if m.lektor.datum is not None:
            ertek = ny.s('kolofon.lektor', db=m.lektor.db, datum=m.lektor.datum)
        else:
            ertek = ny.s('kolofon.lektor.datum_nelkul', db=m.lektor.db)
        iro.tabla_sor((cimke, ertek))
    iro.ures()


def _valtozasjegyzek(iro, ny, m):
    iro.sor(ny.s('kolofon.valtozas.cim'))
    iro.ures()
    if not m.kiadasok:
        iro.sor(ny.s('kolofon.valtozas.nincs'))
        iro.ures()
        return
    iro.tabla_sor((ny.s('kolofon.valtozas.kiadas'), ny.s('kolofon.valtozas.datum'), ny.s('kolofon.valtozas.mi')))
    iro.tabla_elvalaszto(3)
    for k in m.kiadasok:
        iro.tabla_sor((ny.s('kolofon.ertek.szam', n=k.szam), ny.s('kolofon.datum', datum=k.datum), k.valtozas))
    iro.ures()


def _forrastabla(iro, ny, m, keret):
    iro.tabla_sor((ny.s('kolofon.forras.forras'), ny.s('kolofon.forras.licenc'), ny.s('kolofon.forras.szakasz')))
    iro.tabla_elvalaszto(3)
    for f in m.forrasok:
        szakaszok = sorted({keret.rend.szulo(a) for a in f.szakaszok}, key=keret.rend.sorszam)
        iro.tabla_sor((ny.s('kolofon.ertek.nev', nev=ny.nev(f.nev_tipus, f.nev)),
                       ny.s('kolofon.lista', elemek=[md_idezes.licenc_szoveg(ny, lic) for lic in f.licencek]),
                       ny.s('kolofon.lista', elemek=[_szakasz_nev(ny, keret, a) for a in szakaszok])))
    iro.ures()


def _szakasz_nev(ny, keret, azonosito):
    """A szakasz neve a forrástáblában: a szakaszrend sorszáma és a cím; ha a címnek van rövid alakja (`cim.<…>.rovid`,
    pl. „Hatástörténet”), az (a régi `KOLOFON_SZAKASZNEV`)."""
    rovid = keret.rend.cim_kulcs(azonosito) + '.rovid'
    if ny.s.van(rovid):
        return ny.s('cim.szamozott', sorszam=keret.rend.sorszam(azonosito), cim=ny.s(rovid))
    return K.szamozott_cim(keret, azonosito)


def _megjelolesek(iro, ny, m):
    for mj in m.megjelolesek:
        if mj.sablon is None:
            iro.sor(ny.s('kolofon.megjeloles', szoveg=mj.szoveg))
        else:
            kulcs = ny.kulcs('kolofon.megjeloles', mj.sablon)
            parameterek = {'cimke': mj.cimke} if 'cimke' in ny.s.sor(kulcs).parameterek else {}
            iro.sor(ny.s(kulcs, **parameterek))
        iro.ures()


def megjelenit(iro, m, keret, forrasok):
    ny = keret.ny
    iro.cimsor(2, ny.s('cim.kolofon'))
    iro.ures()
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, ny.s('kolofon.olvasoi'))
    iro.sor(ny.s('kolofon.hatokor_blokk'))
    iro.ures()
    iro.sor(_szerzoseg(ny, m))
    iro.ures()
    iro.sor(_hogyan(ny, m, keret))
    iro.ures()
    iro.sor(ny.s('kolofon.modszer'))
    iro.ures()
    iro.sor(_hatokor(ny, m))
    iro.ures()
    _tabla(iro, ny, m, keret)
    _valtozasjegyzek(iro, ny, m)
    iro.sor(VIZSZINTES_VONAL)
    iro.ures()
    _forrastabla(iro, ny, m, keret)
    _megjelolesek(iro, ny, m)
    K.blokk_zar(iro, keret, AZONOSITO, lap_vege=True)   # a Kolofon a lap utolsó szakasza
