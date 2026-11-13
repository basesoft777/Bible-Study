"""lapgen.megjelenites.md.szotari_karoli — a 4.13 (Károli-megfelelők) és a 4.14 (rejtett és hamis párhuzam) pont.

Minden látható mondat a sablontáblából jön (`s4.p13.*`, `s4.p14.*`); itt csak a szerkezet áll. A magyar szó
(szótári alak, szóalak) idézet, az eredeti szó írása és kiejtése idézet; a forrásnevek a névtáblából jönnek.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import DETAILS_NYIT, DETAILS_ZAR, SUMMARY_NYIT, SUMMARY_ZAR
from lapgen.szoveg import prov

FORRASOK_MEGFELELOK = ('B03', 'B55')
FORRASOK_PARHUZAM = ('B07', 'B08', 'B09', 'B03', 'B55')


def _bekezdes(iro, szoveg):
    iro.sor(szoveg)
    iro.ures()


def forrassor(iro, ny, keret, forrasok, eredeti):
    """A pont záró forrássora: a látható forrásnevek, mögötte megjegyzésben a belső proveniencia."""
    iro.sor(ny.s('s4.forrassor', forrasok=tuple(ny.s('ertek.nev', n=ny.nev('forras', b_id)) for b_id in forrasok)),
            prov('eredeti: {} | {})*', eredeti, keret.ts))
    iro.ures()


def _kombo(ny, szo_iras, szavak):
    """A motívum szava (vagy szókapcsolata) névelő nélkül: a szavak írással és kiejtéssel."""
    return ny.s('d14.nev.szavak', szavak=tuple(szo_iras(ny, szo) for szo in szavak))


def _kombo_nevelovel(ny, szo_iras, szo_nevelovel, szavak):
    """Ugyanez határozott névelővel (a névelő az első szó kiejtése szerint)."""
    return ny.s('d14.nev.szavak', szavak=(szo_nevelovel(ny, szavak[0]),) + tuple(szo_iras(ny, szo)
                                                                                  for szo in szavak[1:]))


def _idezett(ny, szo):
    return ny.s('s4.idezett', szo=szo)


def megfelelok(iro, ny, modell, keret, szo_iras, szo_nevelovel):
    """A 4.13 pont törzse (a pont címe után)."""
    m = modell
    nevelovel = lambda szavak: _kombo_nevelovel(ny, szo_iras, szo_nevelovel, szavak)   # noqa: E731
    if m.merheto:
        mondatok = [ny.s('s4.p13.lelet', n=m.hely_szam, m=len(m.csaladok), minimum=konfig.KAROLI_MIN_HELY,
                         reszek=tuple(ny.s('s4.p13.resz', szo=nevelovel(s.szavak), db=s.helyek,
                                           k=s.leggyakoribb_helyek, magyar=s.leggyakoribb) for s in m.merheto))]
    else:
        mondatok = [ny.s('s4.p13.lelet.nincs', n=m.hely_szam, m=len(m.csaladok), legfeljebb=konfig.KAROLI_MIN_HELY - 1)]
    if m.tobbi:
        mondatok.append(ny.s('s4.p13.tobbi', k=m.tobbi, minimum=konfig.KAROLI_MIN_HELY))
    if m.merheto:
        kov = []
        if m.allando:
            kov.append(ny.s('s4.p13.kov.allando.tobb' if len(m.allando) > 1 else 's4.p13.kov.allando.egy',
                            szavak=tuple(nevelovel(k) for k in m.allando)))
        if m.valtozo:
            kov.append(ny.s('s4.p13.kov.valtozo.tobb' if len(m.valtozo) > 1 else 's4.p13.kov.valtozo.egy',
                            szavak=tuple(nevelovel(k) for k in m.valtozo)))
        mondatok.append(ny.s('s4.p13.kovetkeztetes', reszek=tuple(kov)))
    mondatok.append(ny.s('s4.p13.zaro'))
    K.olvasoi_bekezdes(iro, ny.s('s4.mondatok', mondatok=tuple(mondatok)))
    _bekezdes(iro, ny.s('s4.p13.hatokor', tabla=ny.nev('forras', 'B03'), alakok=ny.nev('forras', 'B55')))
    for csalad in m.csaladok:
        iro.sor(ny.s('s4.p13.sor', alak=csalad.alak, n=len(csalad.helyek), szoalakok=csalad.szoalakok,
                     helyek=csalad.helyek))
    iro.ures()
    forrassor(iro, ny, keret, FORRASOK_MEGFELELOK, m.eredeti)


def _bevezeto(ny, szakasz, m, szo_iras, szo_nevelovel):
    nevelovel = lambda szavak: _kombo_nevelovel(ny, szo_iras, szo_nevelovel, szavak)   # noqa: E731
    mondatok = [ny.s('s4.p14.modszer', minimum=konfig.KAROLI_KULCS_MIN_SOR, osszes=m.szavak_szama, n=len(m.kulcsok),
                     nevek=tuple(ny.s('s4.p14.kulcs', szo=nevelovel(k.szavak),
                                      kulcsszavak=tuple(_idezett(ny, szo) for szo in k.kulcsszavak))
                                 for k in m.kulcsok),
                     szakasz=szakasz, pont=konfig.PONT_KAROLI)]
    if m.rejtett:
        mondatok.append(ny.s('s4.p14.rejtett.lelet', n=len(m.rejtett), peldak=tuple(
            ny.s('s4.p14.rejtett.pelda', hely=r.igehely, szo=r.karoli_szo)
            for r in m.rejtett[:konfig.KAROLI_REJTETT_PELDA])))
    else:
        mondatok.append(ny.s('s4.p14.rejtett.nincs'))
    if m.hamis_szam and m.mogott:
        mondatok.append(ny.s('s4.p14.hamis.lelet', n=m.hamis_szam, mogott=tuple(
            ny.s('s4.p14.mogott', idezett=_idezett(ny, g.kulcsszo), eredeti=nevelovel((g.szo,)), db=g.versek)
            for g in m.mogott)))
    elif m.hamis_szam:
        mondatok.append(ny.s('s4.p14.hamis.lelet.par_nelkul', n=m.hamis_szam))
    else:
        mondatok.append(ny.s('s4.p14.hamis.nincs'))
    if not m.rejtett and not m.hamis_szam:
        mondatok.append(ny.s('s4.p14.kov.megbizhato'))
    else:
        kulcsszavak = tuple(ny.s('s4.idezett.nevelovel', idezett=_idezett(ny, szo))
                            for k in m.kulcsok for szo in k.kulcsszavak)
        if m.rejtett:
            mondatok.append(ny.s('s4.p14.kov.rejtettel', kulcsszavak=kulcsszavak, talalat=m.talalat,
                                 szazalek=m.teves_szazalek, rejtett=len(m.rejtett)))
        else:
            mondatok.append(ny.s('s4.p14.kov', kulcsszavak=kulcsszavak, talalat=m.talalat, szazalek=m.teves_szazalek))
    return ny.s('s4.mondatok', mondatok=tuple(mondatok))


def parhuzam(iro, ny, szakasz, modell, keret, szo_iras, szo_nevelovel):
    """A 4.14 pont törzse (a pont címe után)."""
    m = modell
    if not m.kulcsok:
        K.olvasoi_bekezdes(iro, ny.s('s4.p14.nincs_kulcsszo'))
        return
    K.olvasoi_bekezdes(iro, _bevezeto(ny, szakasz, m, szo_iras, szo_nevelovel))
    _bekezdes(iro, ny.s('s4.p14.kulcsszavak', kulcsok=tuple(
        ny.s('s4.p14.kulcs', szo=_kombo(ny, szo_iras, k.szavak),
             kulcsszavak=tuple(_idezett(ny, szo) for szo in k.kulcsszavak)) for k in m.kulcsok)))
    _bekezdes(iro, ny.s('s4.p14.rejtett.cim', n=len(m.rejtett)))
    if m.rejtett:
        for r in m.rejtett:
            iro.sor(ny.s('s4.p14.rejtett.sor', hely=r.igehely, szo=r.karoli_szo, eredeti=_kombo(ny, szo_iras, r.szavak),
                         kulcsszavak=tuple(_idezett(ny, szo) for szo in r.hianyzo)))
        iro.ures()
    _bekezdes(iro, ny.s('s4.p14.hamis.cim', n=m.hamis_szam))
    if m.hamis:
        hosszu = m.hamis_szam > konfig.KAROLI_HAMIS_NYITVA
        if hosszu:
            iro.sor(DETAILS_NYIT)
            iro.sor(SUMMARY_NYIT, ny.s('s4.p14.lista_cim', n=m.hamis_szam), SUMMARY_ZAR)
            iro.ures()
        for konyv in m.hamis:
            versek = tuple(ny.s('s4.p14.vers.szoval', vers=v.vers, szavak=tuple(szo_iras(ny, szo) for szo in v.szavak))
                           if v.szavak else ny.s('s4.p14.vers', vers=v.vers) for v in konyv.versek)
            iro.sor(ny.s('s4.p14.konyv_sor', konyv=konyv.elso, versek=versek, db=len(konyv.versek)))
        iro.ures()
        if hosszu:
            iro.sor(DETAILS_ZAR)
            iro.ures()
    forrassor(iro, ny, keret, FORRASOK_PARHUZAM, m.eredeti)
