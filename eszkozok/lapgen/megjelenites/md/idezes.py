"""lapgen.megjelenites.md.idezes — „12. Irodalom és idézés” (S8c).

Minden látható mondat a sablontáblából (`irod.*`), minden forrásnév a névtáblából (`irod_szotar`,
`irod_szotar_forras`, `irod_adat`, `irod_kulso`), minden licenc a licencleltárból (idézet) vagy a licenc olvasói
alakjának sablonsorából jön. A Kolofon horgonya a címéből képződik (GK-10).
"""
from lapgen.ertekek import IrodLicenc
from lapgen.megjelenites.md import keret as K
from lapgen.szoveg import cim_horgony

AZONOSITO = 'idezes'
_PARAMETER_NELKUL = (IrodLicenc.NYILT_MAG, IrodLicenc.CHAIN_LINEAGE)


def licenc_szoveg(ny, licenc):
    """A forrássor egy licence a lapon (a 12. szakasz és a Kolofon forrástáblája közös alakja)."""
    if licenc.alak is IrodLicenc.LICENC:
        return licenc.cimke
    kulcs = ny.kulcs('irod.licenc', licenc.alak.value)
    if licenc.alak in _PARAMETER_NELKUL:
        return ny.s(kulcs)
    if licenc.alak is IrodLicenc.DOI:
        # a közlés DOI-ja a kiadási adatok egyetlen helyéről (a névtábla `kiadasi_adat` típusa, DT-F218y 1.)
        return ny.s(kulcs, cimke=licenc.cimke, doi=ny.nev('kiadasi_adat', 'karoli_strong_doi'))
    return ny.s(kulcs, cimke=licenc.cimke)


def _hivatkozas(ny, h):
    if h.doi is not None:
        return ny.s('irod.szakirodalom.doi', szerzo=h.szerzo, ev=h.ev, cim=h.cim, megjelenes=h.megjelenes, doi=h.doi)
    return ny.s('irod.szakirodalom.url', szerzo=h.szerzo, ev=h.ev, cim=h.cim, megjelenes=h.megjelenes, url=h.url)


def megjelenit(iro, m, keret, forrasok):
    ny = keret.ny
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, ny.s('irod.olvasoi'))
    iro.sor(ny.s('irod.hatokor'))
    iro.ures()
    kolofon = ny.s('cim.kolofon')
    iro.sor(ny.s('irod.hogyan', kolofon=kolofon, horgony=cim_horgony(kolofon)))
    iro.ures()
    iro.sor(ny.s('irod.szotarak'))
    for sz in m.szotarak:
        iro.sor(ny.s('irod.szotar', nev=ny.nev('irod_szotar', sz.nev),
                     forrasok=[ny.nev('irod_szotar_forras', f) for f in sz.forrasok],
                     licencek=[licenc_szoveg(ny, lic) for lic in sz.licencek]))
    iro.ures()
    if m.szakirodalom:
        iro.sor(ny.s('irod.szakirodalom'))
        iro.ures()
        for h in m.szakirodalom:
            iro.sor(_hivatkozas(ny, h))
        iro.ures()
    iro.sor(ny.s('irod.adatforrasok'))
    for a in m.adatforrasok:
        iro.sor(ny.s('irod.kulso' if a.kulso else 'irod.adat', nev=ny.nev('irod_kulso' if a.kulso else 'irod_adat', a.nev),
                     licencek=[licenc_szoveg(ny, lic) for lic in a.licencek]))
    iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO)
