"""lapgen.megjelenites.md.kereszthiv — a „6. Kereszthivatkozások” szakasz és a Minősítés (S5).

Minden látható mondat a sablontáblából jön (`s6.*`); a vizsgált helyek indoklása kézi próza (a döntésnapló, változatlanul),
az ok cellakezdő alakja kézi adat (a névtábla `ok_cella` sora). A forrás- és a proveniencia-jelölés megjegyzésbe kerül.
"""
from lapgen import konfig
from lapgen.ertekek import AjanlasFajta, Dontes, Gyujtemeny, MegerositesFok
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import DETAILS_NYIT, DETAILS_ZAR, SUMMARY_NYIT, SUMMARY_ZAR
from lapgen.szoveg import prov, prov_fuz

AZONOSITO = 'kereszthivatkozasok'
_FEJLEC = ('s6.min.fejlec.igehely', 's6.min.fejlec.miert', 's6.min.fejlec.indok')
_FOK = {MegerositesFok.EROS: 's6.min.fok.eros', MegerositesFok.KOZEPES: 's6.min.fok.kozepes',
        MegerositesFok.GYENGE: 's6.min.fok.gyenge'}
_KAROLI_MIERT = {AjanlasFajta.TSK_KAROLI: ('s6.miert.tsk_karoli', 's6.miert.tsk_karoli.hely_nelkul'),
                 AjanlasFajta.KAROLI: ('s6.miert.karoli', 's6.miert.karoli.hely_nelkul')}
_DONTES_JEL = {Dontes.BEEPITVE: 's6.min.dontes.beepitve', Dontes.NYITVA: 's6.min.dontes.nyitva'}
_DONTES_SZAM = {Dontes.BEEPITVE: 's6.min.osszegzes.beepitve', Dontes.ELUTASITVA: 's6.min.osszegzes.elutasitva',
                Dontes.NYITVA: 's6.min.osszegzes.nyitva'}


def _bol(n):
    """A szám -ból/-ből ragja a kiejtett alak utolsó szava szerint (a régi `szam_bol`): a sablonkulcs vége."""
    n = abs(int(n))
    e, t10 = n % 10, (n // 10) % 10
    if e:
        return 'bol2' if e in (1, 2, 4, 5, 7, 9) else 'bol'
    if t10:
        return 'bol2' if t10 in (1, 4, 5, 7, 9) else 'bol'
    if n and n % 1000 == 0 and n % 1000000:
        return 'bol2'
    return 'bol'


def olvasoi(ny, m):
    """A szakasz olvasói bekezdése (a régi `olvasoi_kovetkeztetes.kereszthivatkozasok`)."""
    if not m.helyek:
        return ny.s('s6.olvasoi.nincs', n=m.n)
    return ny.s('s6.olvasoi', n=m.n, talalt=len(m.helyek), osszes=m.osszes, szazalek=m.szazalek)


def _hatokor(ny, m):
    mondatok = [ny.s('s6.hatokor', n=m.n, kuszob=m.kuszob, talalt=len(m.helyek), osszes=m.osszes)]
    if m.nem_vizsgalhato:
        mondatok.append(ny.s('s6.hatokor.tobb_vers', n=len(m.nem_vizsgalhato), helyek=m.nem_vizsgalhato))
    if m.kihagyott:
        mondatok.append(ny.s('s6.hatokor.kihagyott', n=len(m.kihagyott), db=sum(db for _h, db in m.kihagyott),
                             helyek=tuple(h for h, _db in m.kihagyott)))
    return ny.s('s6.hatokor.keret', mondatok=tuple(mondatok))


def _utalas(ny, u):
    if u.gyujtemeny is Gyujtemeny.TSK:
        return ny.s('s6.utalas.tsk', cel=u.cel, n=u.szavazat)
    return ny.s('s6.utalas.karoli', cel=u.cel)


# --- Minősítés ----------------------------------------------------------------------------------------------------

def min_olvasoi(ny, mi):
    """A Minősítés olvasói bekezdése (a régi `olvasoi_kovetkeztetes.minosites`, az új szerkezetű lap alakjában)."""
    if not mi.parok:
        return ny.s('s6.min.olvasoi.nincs')
    lelet = ny.s(ny.kulcs('s6.min.lelet', _bol(mi.n)), osszes=mi.osszes, parok=len(mi.parok), erintett=mi.erintett,
                 n=mi.n)
    resz = ny.s('s6.min.resz.fele' if mi.fele else 's6.min.resz', p=mi.szazalek)
    return ny.s('s6.min.olvasoi', lelet=lelet, resz=resz, fok=ny.s(_FOK[mi.fok]))


def _par(ny, p):
    if p.gyujtemeny is Gyujtemeny.TSK:
        return ny.s('s6.min.par.tsk', a=p.forras, b=p.cel, n=p.szavazat)
    return ny.s('s6.min.par.karoli', a=p.forras, b=p.cel)


def _szavazat(ny, tol, ig):
    return ny.s('szam', n=tol) if ig is None else ny.s('s6.miert.tartomany', tol=tol, ig=ig)


def miert(ny, a):
    """A „Miért került a vizsgálatba” cella (a régi `szerep_kizart.jeloles_oka` kereszthivatkozásos ágai, a lap
    végleges alakjában)."""
    if a.fajta is AjanlasFajta.TSK_ALACSONY:
        return ny.s('s6.miert.tsk.alacsony')
    if a.fajta in _KAROLI_MIERT:
        helyrol, hely_nelkul = _KAROLI_MIERT[a.fajta]
        return ny.s(helyrol, hely=a.forrasok[0]) if a.forrasok else ny.s(hely_nelkul)
    tobbi = []
    if a.szavazatok is not None:
        tobbi.append(ny.s('s6.miert.szavazat', ertekek=tuple(_szavazat(ny, t, i) for t, i in a.szavazatok)))
    elif a.talalat is not None:
        tobbi.append(ny.s('s6.miert.talalat', n=a.talalat))
    if a.karoli_is:
        tobbi.append(ny.s('s6.miert.karoli_is'))
    if not a.forrasok:
        return ny.s('s6.miert.tsk.hely_nelkul', tobbi=tuple(tobbi))
    elemek = (ny.s('s6.miert.forras', hely=a.forrasok[0]),) + tuple(
        ny.s('s6.miert.versresz', hely=h) for h in a.forrasok[1:])
    forras = ny.s('s6.miert.forrasok', elemek=elemek)
    if a.cel is not None:
        return ny.s('s6.miert.tsk.cel', forras=forras, cel=a.cel, tobbi=tuple(tobbi))
    return ny.s('s6.miert.tsk', forras=forras, tobbi=tuple(tobbi))


def _darab(ny, d):
    if d.strong is not None:
        h = d.strong
        if h.glossza is None:
            return ny.s('s6.strong.glossza_nelkul', szo=h.szo, strong=h.strong)
        return ny.s('s6.strong', szo=h.szo, strong=h.strong, glossza=h.glossza)
    if d.motivum is not None:
        return ny.s('s6.motivum', motivum=d.motivum)
    return d.proza


def _indok(ny, darabok):
    return ny.s('s6.indok', darabok=tuple(_darab(ny, d) for d in darabok))


def indok_cella(ny, j):
    """Az „Indok” cella: elutasított helynél az ok és az indoklás (az ok elhagyva, ha az indoklás eleje maga mondja
    ki), nyitott vagy beépített helynél a döntés jele és az indoklás."""
    indok = _indok(ny, j.indok) if j.indok else None
    if j.dontes is Dontes.ELUTASITVA:
        if j.ok is None:
            return indok
        return ny.s('s6.min.cella', eleje=j.ok, indok=indok) if indok else j.ok
    jel = ny.s(_DONTES_JEL[j.dontes])
    return ny.s('s6.min.cella', eleje=jel, indok=indok) if indok else jel


def _minosites(iro, ny, mi, keret, forrasok, kuszob):
    iro.cimsor(3, ny.s('cim.minosites'))
    iro.ures()
    K.olvasoi_bekezdes(iro, min_olvasoi(ny, mi))
    iro.sor(prov('GENERÁLT-RÉS: minosites | {} | forrás: {}', konfig.GENERATOR_JELOLO, forrasok.utvonalak))
    iro.ures()
    iro.sor(ny.s('s6.min.bevezeto', kuszob=kuszob))
    iro.ures()
    if mi.parok:
        iro.sor(ny.s('s6.min.parok', n=len(mi.parok)))
        iro.ures()
        for p in mi.parok:
            iro.sor(_par(ny, p))
    else:
        iro.sor(ny.s('s6.min.parok.nincs', kuszob=kuszob))
    iro.ures()
    if mi.jeloltek:
        iro.sor(DETAILS_NYIT)
        iro.sor(SUMMARY_NYIT, ny.s('s6.min.osszegzes', n=len(mi.jeloltek), dontesek=tuple(
            ny.s(_DONTES_SZAM[d], n=db) for d, db in mi.dontesek)), SUMMARY_ZAR)
        iro.ures()
        iro.tabla_sor(tuple(ny.s(k) for k in _FEJLEC))
        iro.tabla_elvalaszto(len(_FEJLEC))
        for j in mi.jeloltek:
            iro.tabla_sor((ny.s('s6.hely', hely=j.igehely), miert(ny, j.miert), indok_cella(ny, j)))
        iro.ures()
        iro.sor(DETAILS_ZAR)
    else:
        iro.sor(ny.s('s6.min.jeloltek.nincs'))
    iro.ures()
    if mi.kozos_olvasoi is not None:
        iro.sor(prov('közös forrásmegjelölés: {}', mi.kozos_olvasoi), prov('eredeti: {}', mi.kozos_eredeti))
        iro.ures()
    iro.sor(ny.s('s6.min.forras'), prov('eredeti: *Proveniencia: `scope=id:{} | forras={} | {}`*', keret.motivum,
                                         prov_fuz('+', forrasok.lista), keret.ts))
    iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, olvasoi(ny, modell))
    iro.sor(_hatokor(ny, modell))
    iro.ures()
    if not modell.helyek:
        iro.sor(ny.s('s6.ures'))
        iro.ures()
    for hely in modell.helyek:
        iro.cimsor(4, ny.s('s6.hely', hely=hely.igehely))
        for u in hely.utalasok:
            iro.sor(_utalas(ny, u))
        iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO)
    _minosites(iro, ny, modell.minosites, keret, forrasok, modell.kuszob)
