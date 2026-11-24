"""lapgen.megjelenites.md.kizart — a „3. Kizárt és vizsgált helyek” szakasz (S9a).

Minden látható mondat a sablontáblából jön (`k3.*`; a „Miért került a vizsgálatba” cella kereszthivatkozásos alakja
és az indoklás darabjai a Minősítéséi: `s6.*`); az ok címkéje és megjegyzése, valamint az indoklás kézi adat. A
lap eleji meghatározást a szakasz nem ismétli, hivatkozik rá (DT872); a kereszthivatkozásból vizsgált sorok táblája
a 6. szakasz Minősítésében áll, itt egy mondat hivatkozik rá (F241.5b, D15 (2)). A jegyzet a tábla alá kerül, az azonos
mondatú jegyzet egyszer áll; a forrás-mező, a proveniencia-farok és a döntés nyoma a jegyzet megjegyzésében marad.
"""
from lapgen import konfig
from lapgen.ertekek import Dontes, JelolesFajta, VizsgaltJegyzetFajta
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md import kereszthiv as md_kh
from lapgen.megjelenites.md.iro import lj_fej, lj_hivatkozas
from lapgen.szakaszok import KRITERIUM_HORGONY
from lapgen.szoveg import prov

AZONOSITO = 'kizart'
_OKOK_FEJLEC = ('k3.okok.fejlec.ok', 'k3.okok.fejlec.vers', 'k3.okok.fejlec.leiras', 'k3.okok.fejlec.pelda')
_TABLA_FEJLEC = ('s6.min.fejlec.igehely', 's6.min.fejlec.miert', 's6.min.fejlec.indok')
_SZAVAS = {JelolesFajta.SZO: 'k3.miert.szo', JelolesFajta.SZOCSALAD: 'k3.miert.szocsalad',
           JelolesFajta.SZOPAR: 'k3.miert.szopar'}
_EGYSZERU = {JelolesFajta.LANC: 'k3.miert.lanc', JelolesFajta.FRAZIS: 'k3.miert.frazis',
             JelolesFajta.AUDIT: 'k3.miert.audit', JelolesFajta.TEMATIKUS: 'k3.miert.tematikus',
             JelolesFajta.NAPLO: 'k3.miert.naplo'}


def _szo(ny, sz):
    if sz.alak is None:
        return ny.s('k3.szo.szotar_nelkul', strong=sz.strong)
    if sz.kiejtes is None:
        return ny.s('k3.szo.kiejtes_nelkul', alak=sz.alak)
    return ny.s('k3.szo', alak=sz.alak, kiejtes=sz.kiejtes)


def miert(ny, j):
    """A „Miért került a vizsgálatba” cella."""
    if j.fajta is JelolesFajta.AJANLAS:
        return md_kh.miert(ny, j.ajanlas)
    if j.fajta in _SZAVAS:
        return ny.s(_SZAVAS[j.fajta], szavak=tuple(_szo(ny, sz) for sz in j.szavak))
    if j.fajta is JelolesFajta.TELJESSEG:
        halok = tuple(ny.nev('halo_kereses', h) for h in j.halok)
        if j.csoport_versszam is not None:
            if halok:
                return ny.s('k3.miert.teljesseg.halo.csoport', halok=halok, n=j.csoport_versszam)
            return ny.s('k3.miert.teljesseg.csoport', n=j.csoport_versszam)
        if halok:
            return ny.s('k3.miert.teljesseg.halo', halok=halok)
        return ny.s('k3.miert.teljesseg')
    return ny.s(_EGYSZERU[j.fajta])


def jegyzet(ny, g):
    """A sor jegyzetének mondata."""
    if g.fajta is VizsgaltJegyzetFajta.SZOKERESES:
        return ny.s('k3.jegyzet.szokereses', szavak=tuple(_szo(ny, sz) for sz in g.szavak),
                    megszoritas=ny.nev('kereses_megszoritas', g.megszoritas))
    korpuszok = tuple(ny.nev('korpusz', k) for k in g.korpuszok)
    if g.fajta is VizsgaltJegyzetFajta.KERESES_KORPUSZ:
        return ny.s('k3.jegyzet.kereses', strongok=tuple(sz.strong for sz in g.szavak),
                    korpuszok=korpuszok)
    if g.fajta is VizsgaltJegyzetFajta.LANC:
        return ny.s('k3.jegyzet.lanc', korpuszok=korpuszok)
    if g.fajta is VizsgaltJegyzetFajta.ADATTABLAK:
        return ny.s('e2.jegyzet.ures')
    if g.fajta is VizsgaltJegyzetFajta.TELJESSEG_EGYENKENT:
        return ny.s('k3.jegyzet.teljesseg_egyenkent')
    return ny.s('k3.jegyzet.naplo')


def indok_cella(ny, s):
    """Az „Indok” cella: az ok (a névtábla cellakezdő alakjában; elhagyva, ha az indoklás eleje maga mondja ki),
    nyitott sornál a döntés jele, utána az indoklás az összesítő sor elejével és a szerkesztői záró mondattal."""
    indok = ny.s('s6.indok', darabok=tuple(md_kh.indok_darab(ny, d) for d in s.indok)) if s.indok else None
    if indok is not None and s.osszesito is not None:
        indok = ny.s('k3.indok.osszesito', n=s.osszesito, indok=indok)
    if indok is not None and s.szerkesztoi_zaro:
        indok = ny.s('k3.indok.szerkesztoi_zaro', indok=indok)
    if s.dontes is Dontes.NYITVA:
        eleje = ny.s('s6.min.dontes.nyitva')
    else:
        eleje = s.ok
    if eleje is None:
        return indok
    return ny.s('s6.min.cella', eleje=eleje, indok=indok) if indok is not None else eleje


def _hely(ny, s):
    if s.veg is not None:
        return ny.s('k3.hely.tartomany', hely=s.igehely, veg=s.veg)
    return ny.s('s6.hely', hely=s.igehely)


def olvasoi(ny, m):
    """A szakasz olvasói bekezdése (a régi `olvasoi_kovetkeztetes.kizart_uj`)."""
    vizsgalt = m.egyen + m.csoport + m.nyitva
    elutasitva = m.egyen + m.csoport
    reszek = [ny.s('k3.olv.eleje.motivummal', n=m.helyek, v=vizsgalt) if m.helyek
              else ny.s('k3.olv.eleje', v=vizsgalt)]
    if m.csoport:
        reszek.append(ny.s('k3.olv.kereses.ajanlas' if m.ajanlas else 'k3.olv.kereses'))
    else:
        reszek.append(ny.s('k3.olv.jeloltkent'))
    if m.nyitva:
        reszek.append(ny.s('k3.olv.nyitott', e=elutasitva, ny=m.nyitva))
    else:
        reszek.append(ny.s('k3.olv.egyik_sem'))
    if m.csoport:
        reszek.append(ny.s('k3.olv.bontas.kozulük' if m.nyitva else 'k3.olv.bontas', e=m.egyen, c=m.csoport))
    elif not m.nyitva:
        reszek.append(ny.s('k3.olv.pont'))
    if len(m.okok) > 1:
        reszek.append(ny.s('k3.olv.ok2', a=m.okok[0].ok, n=m.okok[0].versszam, b=m.okok[1].ok, m=m.okok[1].versszam))
    elif m.okok:
        reszek.append(ny.s('k3.olv.ok1', a=m.okok[0].ok, n=m.okok[0].versszam))
    if m.forrasok:
        reszek.append(ny.s('k3.olv.forrasok', elemek=tuple(
            ny.s('k3.forras.elem', csoport=ny.nev('vizsgalt_csoport', c), n=n)
            for c, n in sorted(m.forrasok, key=lambda x: -x[1]) if n)))
    kov = []
    if m.helyek:
        arany = vizsgalt / m.helyek
        if round(arany) <= konfig.KIZART_ATLAG_HATAR:
            raise ValueError('a 3. szakasz arány-mondata (legfeljebb %d-szeres arány) nincs leképezve'
                             % konfig.KIZART_ATLAG_HATAR)
        kov.append(ny.s('k3.kov.atlag', x=round(arany), v=vizsgalt, n=m.helyek))
    if m.okok and elutasitva:
        hatar = m.okok[0].versszam / elutasitva >= konfig.KIZART_HATAR_KUSZOB
        kulcs = 'k3.kov.hatar' if hatar else 'k3.kov.tobb'
        kulcs += '.elso' if not kov else ''
        kov.append(ny.s(kulcs, ok=m.okok[0].ok) if hatar else ny.s(kulcs))
    if kov:
        reszek.append(ny.s('k3.olv.kov', elemek=tuple(kov)))
    return ny.s('k3.olvasoi', reszek=tuple(reszek))


def _okok(iro, ny, m):
    if not m.okok:
        iro.sor(ny.s('k3.okok.nincs'))
        iro.ures()
        return
    iro.sor(ny.s('k3.okok.cim'))
    iro.ures()
    iro.tabla_sor(tuple(ny.s(k) for k in _OKOK_FEJLEC))
    iro.tabla_elvalaszto(len(_OKOK_FEJLEC))
    for o in m.okok[:konfig.KIZART_TABLA_OK_DB]:
        iro.tabla_sor((o.cella, ny.s('szam', n=o.versszam), o.leiras if o.leiras is not None else ny.s('jel.nincs'),
                       ny.s('k3.okok.peldak', peldak=o.peldak) if o.peldak else ny.s('jel.nincs')))
    iro.ures()
    tobbi = m.okok[konfig.KIZART_TABLA_OK_DB:]
    if tobbi:
        iro.sor(ny.s('k3.okok.tobbi', n=len(tobbi), v=sum(o.versszam for o in tobbi), elemek=tuple(
            ny.s('k3.okok.tobbi.elem', ok=o.ok, n=o.versszam) for o in tobbi)))
        iro.ures()


def _tabla(iro, ny, t, szakasz, jegyzetek):
    """Egy forráscsoport táblája és alatta a jegyzetei. `jegyzetek`: [(mondat, sorszám, megjegyzések)] a szakaszra
    folyamatos számozással (a hívó listája; itt bővül)."""
    if t.versszam != t.sorok_szama:
        iro.sor(ny.s('k3.csoport.cim.vers', csoport=ny.nev('vizsgalt_csoport', t.csoport), n=t.sorok_szama,
                     v=t.versszam))
    else:
        iro.sor(ny.s('k3.csoport.cim', csoport=ny.nev('vizsgalt_csoport', t.csoport), n=t.sorok_szama))
    iro.ures()
    iro.tabla_sor(tuple(ny.s(k) for k in _TABLA_FEJLEC))
    iro.tabla_elvalaszto(len(_TABLA_FEJLEC))
    helyi = []
    for s in t.sorok:
        cella = (miert(ny, s.jeloles),)
        if s.jegyzet is not None:
            mondat = jegyzet(ny, s.jegyzet)
            talalt = next((x for x in jegyzetek if x[0] == mondat), None)
            if talalt is None:
                talalt = (mondat, len(jegyzetek) + 1, [])
                jegyzetek.append(talalt)
                helyi.append(talalt)
            elif talalt not in helyi:
                helyi.append(talalt)
            if s.eredeti not in talalt[2]:
                talalt[2].append(s.eredeti)
            cella += (lj_hivatkozas(szakasz, talalt[1]),)
        iro.tabla_sor((_hely(ny, s), cella, indok_cella(ny, s)))
    iro.ures()
    if helyi:
        for mondat, szam, eredetik in helyi:
            iro.sor(lj_fej(szakasz, szam), mondat, *(prov('eredeti: {}', e) for e in eredetik))
        iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    szakasz = keret.rend.sorszam(AZONOSITO)
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    if not modell.tablak:
        K.olvasoi_bekezdes(iro, ny.s('k3.olvasoi.ures'))
        iro.sor(ny.s('k3.ures'))
        iro.ures()
    else:
        K.olvasoi_bekezdes(iro, olvasoi(ny, modell))
        iro.sor(ny.s('k3.hatokor', n=modell.sorok_szama, tabla=ny.nev('forras', 'B04')))
        iro.ures()
        iro.sor(ny.s('k3.kriterium', cim=ny.s('fej.hatar.cim'), horgony=KRITERIUM_HORGONY))
        iro.ures()
        _okok(iro, ny, modell)
        if modell.nyitva:
            iro.sor(ny.s('k3.nyitott', n=modell.nyitva))
            iro.ures()
        iro.sor(ny.s('k3.forras', elemek=tuple(ny.s('k3.forras.elem', csoport=ny.nev('vizsgalt_csoport', c), n=n)
                                               for c, n in modell.forrasok if n)))
        iro.ures()
        masutt = [t for t in modell.tablak if t.masutt]
        if masutt:
            iro.sor(ny.s('k3.kh_masutt', n=sum(t.sorok_szama for t in masutt), elemek=tuple(
                ny.s('k3.forras.elem', csoport=ny.nev('vizsgalt_csoport', t.csoport), n=t.sorok_szama)
                for t in masutt), cim=K.szamozott_cim(keret, md_kh.AZONOSITO),
                horgony=K.szakasz_horgony(keret, md_kh.AZONOSITO), minosites=ny.s('cim.minosites')))
            iro.ures()
        jegyzetek = []
        for t in modell.tablak:
            if not t.masutt:
                _tabla(iro, ny, t, szakasz, jegyzetek)
    if modell.kozos_olvasoi is not None:
        iro.sor(prov('közös forrásmegjelölés: {}', modell.kozos_olvasoi), prov('eredeti: {}', modell.kozos_eredeti))
        iro.ures()
    K.blokk_zar(iro, keret, AZONOSITO)
