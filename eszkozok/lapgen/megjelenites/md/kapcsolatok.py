"""lapgen.megjelenites.md.kapcsolatok — a „7. Kapcsolatok” szakasz, az Alátámasztás és a „8. Kapcsolódó motívumok”
szakasz (S6).

Minden látható mondat a sablontáblából jön (`s7.*`, `s8.*`); a funkció és az indoklás kézi próza (a kapcsolat-tábla és
a motívumközi tábla cellája, változatlanul; a cellakezdő alak az adatban, DT869); a típus, a bizonyosság és a
PaRDeS-szint olvasói neve a névtáblából. A forrás- és a proveniencia-jelölés megjegyzésbe kerül.
"""
from lapgen import konfig
from lapgen.ertekek import KapcsolatBiztossag, KapcsolatSzerkezet
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import (DETAILS_NYIT, DETAILS_ZAR, KOD_ZAR, LINK_NYIT, MERMAID_CSUCS_ZAR, MERMAID_GRAF,
                                        MERMAID_NYIT, SUMMARY_NYIT, SUMMARY_ZAR, lap_link_zar, mermaid_csucs_nyit,
                                        mermaid_el_nyit, mermaid_el_zar)
from lapgen.szoveg import prov, prov_fuz

AZONOSITO = 'kapcsolatok'
AZONOSITO_KAPCSOLODO = 'kapcsolodo'
ELOFORDULASOK = 'elofordulasok'   # a helyek saját PaRDeS-szintje itt áll (a hatókör-mondat hivatkozik rá)
_TIPUS, _TIPUS_MONDAT, _MK_TIPUS = 'kapcsolat_tipus', 'kapcsolat_tipus_mondat', 'motivumkozi_tipus'
_FEJLEC = ('s7.fejlec.forras', 's7.fejlec.cel', 's7.fejlec.tipus', 's7.fejlec.funkcio', 's7.fejlec.bizonyossag',
           's7.fejlec.pardes')
_ALAT_FEJLEC = ('s7.alat.fejlec.kapcsolat', 's7.alat.fejlec.alatamasztas')
_MK_FEJLEC = ('s8.fejlec.motivum', 's8.fejlec.itt', 's8.fejlec.ott', 's8.fejlec.tipus', 's8.fejlec.funkcio',
              's8.fejlec.bizonyossag', 's8.fejlec.pardes', 's8.fejlec.indoklas')
_SZERKEZET = {KapcsolatSzerkezet.LANC: 's7.szerk.lanc',
              KapcsolatSzerkezet.TULNYOMO_PARHUZAM: 's7.szerk.tulnyomo_parhuzam',
              KapcsolatSzerkezet.TOBBFELE: 's7.szerk.tobbfele'}
_BIZTOSSAG = {KapcsolatBiztossag.SZINTE_MIND: 's7.biz.szinte_mind', KapcsolatBiztossag.TOBBSEG: 's7.biz.tobbseg',
              KapcsolatBiztossag.FELE: 's7.biz.fele', KapcsolatBiztossag.KOZEPES_TOBBSEG: 's7.biz.kozepes_tobbseg',
              KapcsolatBiztossag.KEVES: 's7.biz.keves'}


def _vagy_jel(ny, ertek):
    return ertek if ertek is not None else ny.s('jel.nincs')


def _pardes(ny, szintek):
    return ny.s('e2.pardes', szintek=tuple(ny.nev('pardes_szint', sz) for sz in szintek)) if szintek \
        else ny.s('jel.nincs')


def _nev(ny, tipus, kulcs):
    return ny.s('ertek.nev', n=ny.nev(tipus, kulcs))


def olvasoi(ny, m):
    """A 7. szakasz olvasói bekezdése (a régi `olvasoi_kovetkeztetes.kapcsolatok`, az új szerkezetű lap alakjában)."""
    if not m.n:
        return ny.s('s7.olvasoi.ures')
    tipusok = tuple(ny.s('s7.tipus_db', n=db, tipus=ny.nev(_TIPUS_MONDAT, t)) for t, db in m.tipusok)
    if m.n == m.magas:
        lelet = ny.s('s7.lelet.mind_magas', n=m.n, cs=len(m.csomopontok), tipusok=tipusok, magas=m.magas)
    elif m.alacsony:
        lelet = ny.s('s7.lelet.alacsony', n=m.n, cs=len(m.csomopontok), tipusok=tipusok, magas=m.magas,
                     kozepes=m.kozepes, alacsony=m.alacsony)
    else:
        lelet = ny.s('s7.lelet', n=m.n, cs=len(m.csomopontok), tipusok=tipusok, magas=m.magas, kozepes=m.kozepes)
    if m.szerkezet is KapcsolatSzerkezet.TULNYOMO:
        szerk = ny.s('s7.szerk.tulnyomo', tipus=ny.nev(_TIPUS_MONDAT, m.fo_tipus))
    else:
        szerk = ny.s(_SZERKEZET[m.szerkezet])
    return ny.s('s7.olvasoi', lelet=lelet, szerk=szerk, biz=ny.s(_BIZTOSSAG[m.biztossag]))


def _graf(iro, ny, m):
    iro.sor(DETAILS_NYIT)
    iro.sor(SUMMARY_NYIT, ny.s('s7.graf.cim'), SUMMARY_ZAR)
    iro.ures()
    iro.sor(MERMAID_NYIT)
    iro.sor(MERMAID_GRAF)
    for i, hely in enumerate(m.csomopontok, 1):
        iro.sor(mermaid_csucs_nyit(i), ny.s('s7.hely', hely=hely), MERMAID_CSUCS_ZAR)
    for el in m.elek:
        iro.sor(mermaid_el_nyit(el.forras), _nev(ny, _TIPUS, el.tipus), mermaid_el_zar(el.cel))
    iro.sor(KOD_ZAR)
    iro.ures()
    iro.sor(DETAILS_ZAR)
    iro.ures()


def _par(ny, par):
    return ny.s('s7.par', a=par[0], b=par[1])


def _alatamasztas(iro, ny, m, keret, forrasok):
    a = m.alatamasztas
    iro.cimsor(3, ny.s('cim.alatamasztas'))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('s7.alat.olvasoi'))
    iro.sor(prov('GENERÁLT-RÉS: alatamasztas | {} | forrás: {}', konfig.GENERATOR_JELOLO, forrasok.utvonalak))
    iro.ures()
    if not m.n:
        iro.sor(ny.s('s7.alat.nincs'))
        iro.ures()
    else:
        iro.sor(ny.s('s7.alat.bevezeto'))
        iro.ures()
        if a.sorok:
            iro.tabla_sor(tuple(ny.s(k) for k in _ALAT_FEJLEC))
            iro.tabla_elvalaszto(len(_ALAT_FEJLEC))
            for s in a.sorok:
                iro.tabla_sor((ny.s('s7.alat.parok', parok=tuple(_par(ny, p) for p in s.parok)), s.indok))
            iro.ures()
            iro.sor(ny.s('s7.alat.modszer'), *a.megjegyzesek)
            iro.ures()
            if a.nelkul:
                iro.sor(ny.s('s7.alat.indoklas_nelkul', n=len(a.nelkul), parok=tuple(_par(ny, p) for p in a.nelkul)))
                iro.ures()
        else:
            iro.sor(ny.s('s7.alat.nincs_indoklas', n=m.n))
            iro.ures()
    iro.sor(ny.s('s7.alat.forras'), prov('eredeti: *Proveniencia: `scope=id:{} | forras={} | {}`*', keret.motivum,
                                          prov_fuz('+', forrasok.lista), keret.ts))
    iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny, m = keret.ny, modell
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, olvasoi(ny, m))
    if m.n:
        iro.sor(ny.s('s7.hatokor', n=m.n, cs=len(m.csomopontok), szakasz=keret.rend.sorszam(ELOFORDULASOK)))
        iro.ures()
        iro.tabla_sor(tuple(ny.s(k) for k in _FEJLEC))
        iro.tabla_elvalaszto(len(_FEJLEC))
        for s in m.sorok:
            iro.tabla_sor((ny.s('s7.hely', hely=s.forras), ny.s('s7.hely', hely=s.cel), _nev(ny, _TIPUS, s.tipus),
                           _vagy_jel(ny, s.funkcio), _nev(ny, 'megbizhatosag', s.bizonyossag), _pardes(ny, s.pardes)))
        iro.ures()
        _graf(iro, ny, m)
    else:
        iro.sor(ny.s('s7.ures'))
        iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO)
    _alatamasztas(iro, ny, m, keret, forrasok)


# --- 8. Kapcsolódó motívumok ----------------------------------------------------------------------------------

def olvasoi_kapcsolodo(ny, m):
    """A 8. szakasz olvasói bekezdése (a régi `olvasoi_kovetkeztetes.kapcsolodo`)."""
    if not m.sorok:
        if m.nyitott_ossz:
            return ny.s('s8.olvasoi.nincs.nyitott', nyitott=m.nyitott_ossz)
        return ny.s('s8.olvasoi.nincs')
    motivumok = tuple(ny.s('s8.motivum_db', motivum=mot, n=db) for mot, db in m.motivumok)
    if len(m.tipusok) == 1:
        tipus = ny.s('s8.tipus.mind', tipus=ny.nev(_MK_TIPUS, m.tipusok[0]))
    else:
        tipus = ny.s('s8.tipus.tobb', tipusok=tuple(ny.nev(_MK_TIPUS, t) for t in m.tipusok))
    if m.nyitott_ossz:
        lelet = ny.s('s8.lelet.nyitott', n=len(m.sorok), m=len(m.motivumok), motivumok=motivumok, tipus=tipus,
                     nyitott=m.nyitott_ossz)
    else:
        lelet = ny.s('s8.lelet', n=len(m.sorok), m=len(m.motivumok), motivumok=motivumok, tipus=tipus)
    kov = ny.s('s8.kov.szomszedos' if m.csak_szomszedos else 's8.kov.tartalmi')
    return ny.s('s8.olvasoi', lelet=lelet, kov=kov)


def megjelenit_kapcsolodo(iro, modell, keret, forrasok):
    ny, m = keret.ny, modell
    K.szakasz_cim(iro, keret, AZONOSITO_KAPCSOLODO)
    K.blokk_nyit(iro, keret, AZONOSITO_KAPCSOLODO, forrasok)
    K.olvasoi_bekezdes(iro, olvasoi_kapcsolodo(ny, m))
    iro.sor(ny.s('s8.hatokor', datum=m.dontes_datum))
    iro.ures()
    if m.sorok:
        iro.tabla_sor(tuple(ny.s(k) for k in _MK_FEJLEC))
        iro.tabla_elvalaszto(len(_MK_FEJLEC))
        for s in m.sorok:
            link = (LINK_NYIT, ny.s('s8.motivum', motivum=s.masik), lap_link_zar(s.masik, konfig.NEZET_TUDOMANYOS))
            iro.tabla_sor((link, ny.s('s7.hely', hely=s.itt), ny.s('s7.hely', hely=s.ott), _nev(ny, _MK_TIPUS, s.tipus),
                           _vagy_jel(ny, s.funkcio), _nev(ny, 'megbizhatosag', s.bizonyossag), _pardes(ny, s.pardes),
                           _vagy_jel(ny, s.indok)))
    else:
        iro.sor(ny.s('s8.nincs'))
    iro.ures()
    if m.nyitott:
        iro.sor(ny.s('s8.nyitott', n=m.nyitott_ossz,
                     elemek=tuple(ny.s('s8.nyitott.elem', motivum=mot, n=db) for mot, db in m.nyitott)))
        iro.ures()
    iro.sor(ny.s('s8.forras'), prov('eredeti: *Proveniencia: `scope=id:{} | forras={} | {}`*', keret.motivum,
                                     prov_fuz('+', forrasok.lista), keret.ts))
    iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO_KAPCSOLODO)
