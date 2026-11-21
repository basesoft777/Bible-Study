"""lapgen.megjelenites.md.resek — a kézi rések (S8b): a 4. szakasz „Miért fontos ez a lelet” rése, a 10. Értelmezés és a
11. Módszertan.

A rés címe és olvasói bevezetője a sablontáblából, a törzse a kézi forrásból változatlanul (`proza`). A kézi forrássor
helyén az olvasói forrássor (`res.forras`: a nevezett adatbemenetek olvasói neve a névtábla `forras` típusából), a nyers
sor megjegyzésben. A szakirodalom-sor a 12. szakaszra a szakaszrend számával hivatkozik (GK-10).
"""
from lapgen.ertekek import ResElemFajta
from lapgen.megjelenites.md import keret as K
from lapgen.szamitas.resek import RES_ERTELMEZES, RES_MIERT_FONTOS, RES_MODSZERTAN

AZONOSITO_MIERT_FONTOS, AZONOSITO_ERTELMEZES, AZONOSITO_MODSZERTAN = RES_MIERT_FONTOS, RES_ERTELMEZES, RES_MODSZERTAN
IDEZES = 'idezes'
KEZI_FORRASFAJL = 'kezi_forrasfajl'   # a névtábla típusa (bemenet.nyelv.KEZI_FORRASFAJL_TIPUS)


def _szakirodalom(keret, sz):
    ny = keret.ny
    if sz.szerzo is not None:
        return ny.s('res.szakirodalom', osszefoglalo=sz.osszefoglalo, szerzo=sz.szerzo, ev=sz.ev,
                    szakasz=keret.rend.sorszam(IDEZES))
    return ny.s('res.szakirodalom.hiany', osszefoglalo=sz.osszefoglalo, datum=sz.lekerdezve)


def _torzs(iro, keret, modell):
    ny = keret.ny
    for e in modell.elemek:
        if e.fajta is ResElemFajta.URES:
            iro.ures()
        elif e.fajta is ResElemFajta.PROZA:
            iro.sor(e.proza)
        elif e.fajta is ResElemFajta.FORRAS:
            nevek = tuple(ny.nev('forras' if f.jegyzekbeli else KEZI_FORRASFAJL, f.kulcs) for f in e.bemenetek)
            iro.sor(ny.s('res.forras', nevek=nevek), e.eredeti)
        else:
            iro.sor(_szakirodalom(keret, e.szakirodalom))
    iro.ures()


def megjelenit_miert_fontos(iro, modell, keret, forrasok):
    ny = keret.ny
    iro.cimsor(3, ny.s('cim.miert_fontos'))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('res.olvasoi.miert_fontos'))
    _torzs(iro, keret, modell)


def megjelenit_ertelmezes(iro, modell, keret, forrasok):
    K.szakasz_cim(iro, keret, AZONOSITO_ERTELMEZES)
    K.olvasoi_bekezdes(iro, keret.ny.s('res.olvasoi.ertelmezes'))
    _torzs(iro, keret, modell)


def megjelenit_modszertan(iro, modell, keret, forrasok):
    K.szakasz_cim(iro, keret, AZONOSITO_MODSZERTAN)
    K.olvasoi_bekezdes(iro, keret.ny.s('res.olvasoi.modszertan'))
    _torzs(iro, keret, modell)
