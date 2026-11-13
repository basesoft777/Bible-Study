"""lapgen.megjelenites.md.kizarasok — a kizárt és vizsgált versek melléklete (külön nézet: `<ID>_KIZARASOK.md`).

Minden látható mondat a sablontáblából jön (`kz.*` kulcsok); az ok címkéje és leírása kézi adat. A teljesség-mérés
forrássora proveniencia: megjegyzésben áll, a látható sor a keresés olvasói nevét és versszámát adja.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import DETAILS_NYIT, DETAILS_ZAR, SUMMARY_NYIT, SUMMARY_ZAR
from lapgen.szoveg import prov

AZONOSITO = 'kizarasok_melleklet'
DONTESI_UT = 'dontesi_ut'
ALPONT_FORRASOK = 2   # a Döntési út „A keresés forrásai” pontja


def _ok(iro, ny, ok):
    iro.ures()
    iro.cimsor(3, ny.s('kz.ok_cim', ok=ok.ok, n=ok.versszam))
    iro.ures()
    iro.sor(ok.leiras)
    iro.ures()
    hosszu = ok.versszam > konfig.KIZARASOK_NYITVA_HATAR
    if hosszu:
        iro.sor(DETAILS_NYIT)
        iro.sor(SUMMARY_NYIT, ny.s('kz.lista_cim', n=ok.versszam), SUMMARY_ZAR)
        iro.ures()
    for konyv in ok.konyvek:
        iro.sor(ny.s('kz.konyv_sor', konyv=konyv.elso, db=len(konyv.versek), versek=konyv.versek))
    if hosszu:
        iro.ures()
        iro.sor(DETAILS_ZAR)


def megjelenit(iro, modell, keret, forrasok):
    ny, v = keret.ny, modell.vizsgalat
    kizart = v.csoport + v.egyen
    iro.sor(prov('GENERÁLT: {} | melléklet: {}', konfig.GENERATOR_JELOLO, keret.motivum))
    iro.ures()
    iro.cimsor(1, ny.s('kz.cim', motivum=keret.motivum))
    iro.ures()
    iro.sor(ny.s('kz.bevezeto', motivum=keret.motivum, horgony=K.szakasz_horgony(keret, DONTESI_UT), bent=v.bent,
                 kizart=kizart))
    iro.ures()
    iro.sor(ny.s('kz.osszeadas', csoport=v.csoport, egyen=v.egyen, kizart=kizart))
    for cim, okok in (('kz.cim.csoport', modell.csoport), ('kz.cim.egyen', modell.egyen)):
        if not okok:
            continue
        iro.ures()
        iro.cimsor(2, ny.s(cim))
        for ok in okok:
            _ok(iro, ny, ok)
    if v.keresesek is not None:
        iro.ures()
        iro.cimsor(2, ny.s('kz.forrassorok.cim'))
        iro.ures()
        iro.sor(ny.s('kz.forrassorok.bevezeto', szakasz=keret.rend.sorszam(DONTESI_UT), alpont=ALPONT_FORRASOK))
        iro.ures()
        for kereses in v.keresesek:
            iro.sor(ny.s('kz.forrassorok.kereses', kereses=ny.nev('halo', kereses.kulcs), n=kereses.versszam),
                    kereses.forrassor)
    iro.ures()
    if keret.datum is not None:
        iro.sor(ny.s('kz.forras', datum=keret.datum))
    else:
        iro.sor(ny.s('kz.forras.datum_nelkul'))
