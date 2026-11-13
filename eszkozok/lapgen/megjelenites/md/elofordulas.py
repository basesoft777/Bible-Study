"""lapgen.megjelenites.md.elofordulas — a „2. Előfordulások” szakasz és a „2.1 Az igehelyek szövege” pont.

Minden látható mondat a sablontáblából jön (`e2.*`, `e21.*` kulcsok); itt csak a szerkezet áll.
A tábla alatti jegyzet rövid, egysoros mondat a sor igazolásáról és a jelentéscímke indokáról; az azonos
szövegű jegyzet egyszer áll, több sor is mutathat rá. A teljes belső leírás megjegyzésben marad.
"""
from lapgen.ertekek import DbhOk, Igazolas, IndokFajta, JegyzetFajta, JelentesFajta, SzovetsegKod, UbsForras
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import horgony_jel, lj_fej, lj_hivatkozas
from lapgen.szoveg import prov

AZONOSITO = 'elofordulasok'
ALPONT_SZOVEG = 1   # a 2.1 pont sorszáma a szakaszon belül
FEJLEC = ('e2.fejlec.igehely', 'e2.fejlec.kulcsszo', 'e2.fejlec.jelentes', 'e2.fejlec.funkcio', 'e2.fejlec.pardes',
          'e2.fejlec.strong', 'e2.fejlec.ubs', 'e2.fejlec.megbizhatosag')

_SZOVETSEG_SABLON = {
    SzovetsegKod.FOKENT_OSZ: 'e2.kov.fokent_osz',
    SzovetsegKod.FOKENT_USZ: 'e2.kov.fokent_usz',
    SzovetsegKod.MINDKETTO: 'e2.kov.mindketto',
    SzovetsegKod.CSAK_OSZ: 'e2.kov.csak_osz',
    SzovetsegKod.CSAK_USZ: 'e2.kov.csak_usz',
}
_DBH_OK_SABLON = {
    DbhOk.NINCS_MEGFELELTETES: 'e2.dbh.ok.nincs_megfeleltetes',
    DbhOk.NEM_EGY_VERS: 'e2.dbh.ok.nem_egy_vers',
    DbhOk.SZAMOZAS_ELTERES: 'e2.dbh.ok.szamozas_elteres',
}
_IGAZOLAS_SABLON = {
    Igazolas.TAHOT_IGAZOLT: 'e2.igazolas.heber',
    Igazolas.TAGNT_IGAZOLT: 'e2.igazolas.gorog',
    Igazolas.NINCS: 'e2.igazolas.nincs',
}
_KUTATOI = (IndokFajta.KUTATOI, IndokFajta.KUTATOI_TAGABB)


def _osszegzo(ny, o):
    """Az összegző mondat: lelet, megbízhatóság, következtetés."""
    if o.osz and o.usz:
        lelet = ny.s('e2.lelet.ket_szovetseg', n=o.helyek, konyvek=o.konyvek, osz=o.osz, usz=o.usz)
    elif o.osz:
        lelet = ny.s('e2.lelet.csak_osz', n=o.helyek, konyvek=o.konyvek, osz=o.osz)
    else:
        lelet = ny.s('e2.lelet.csak_usz', n=o.helyek, konyvek=o.konyvek, usz=o.usz)
    if o.helyek - o.magas:
        megb = ny.s('e2.megb.vegyes', magas=o.magas, tobbi=o.helyek - o.magas)
    else:
        megb = ny.s('e2.megb.mind', magas=o.magas)
    kov = []
    if o.sulypont_konyv is not None:
        kov.append(ny.s('e2.kov.sulypont', konyv=o.sulypont_konyv, n=o.helyek, db=o.sulypont_db))
    if o.szovetseg is SzovetsegKod.FOKENT_OSZ:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], usz=o.usz))
    elif o.szovetseg is SzovetsegKod.FOKENT_USZ:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], osz=o.osz))
    elif o.szovetseg is SzovetsegKod.MINDKETTO:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg], osz=o.osz, usz=o.usz))
    else:
        kov.append(ny.s(_SZOVETSEG_SABLON[o.szovetseg]))
    if o.bizonytalan:
        kov.append(ny.s('e2.kov.bizonytalan'))
    return ny.s('e2.osszegzo', lelet=lelet, megb=megb, kov=tuple(kov))


# --- a tábla cellái ---------------------------------------------------------------------------------------------

def _alak(ny, a):
    if a.kiejtes is not None:
        return ny.s('e2.alak.kiejtessel', alak=a.alak, kiejtes=a.kiejtes)
    return ny.s('e2.alak', alak=a.alak)


def _kulcsszo(ny, sor):
    alakok = tuple(_alak(ny, a) for a in sor.alakok)
    if sor.tematikus_szo_nelkul:
        return sor.karoli_szo if sor.karoli_szo is not None else ny.s('jel.nincs')
    if sor.karoli_szo is None:
        return ny.s('e2.kulcsszo.csak_alak', alakok=alakok) if alakok else ny.s('jel.nincs')
    if not alakok:
        return ny.s('e2.kulcsszo.nincs_alak', karoli=sor.karoli_szo)
    return ny.s('e2.kulcsszo', karoli=sor.karoli_szo, alakok=alakok)


def _jelentes_token(ny, t, cellakezdo):
    """Egy szó jelentése; `cellakezdo`: a szöveg a cella elején áll (a címke és a sablonmondat cellakezdő
    alakja adat, illetve külön sablonsor; átírás nincs)."""
    if t.fajta in (JelentesFajta.CIMKE, JelentesFajta.GLOSSZA):
        cimke = t.cimke_cella if cellakezdo and t.cimke_cella is not None else t.cimke
        return ny.s('e2.jelentes.cimke', cimke=cimke, jel=t.jel)
    if t.fajta is JelentesFajta.SZOCIKK_EGESZE:
        kulcs = ny.kulcs('e2.jelentes.szocikk_egesze', 'cella') if cellakezdo else 'e2.jelentes.szocikk_egesze'
        if t.cimke is not None:
            return ny.s(kulcs, glossza=t.cimke)
        return ny.s(ny.kulcs(kulcs, 'ures'))
    if t.fajta is JelentesFajta.NINCS_CIMKE:
        return ny.s('e2.jelentes.nincs_cimke', jel=t.jel)
    return ny.s('e2.jelentes.nincs_hozzarendeles')


def _jelentes(ny, sor):
    if sor.tematikus_szo_nelkul or sor.sajat_szo:
        return ny.s('e2.jelentes.tematikus')
    if not sor.jelentes:
        return ny.s('jel.nincs')
    if len(sor.jelentes) == 1:
        return _jelentes_token(ny, sor.jelentes[0], True)
    return ny.s('e2.jelentes.tokenek', tokenek=tuple(
        ny.s('e2.jelentes.tokenenkent', strong=t.strong, tartalom=_jelentes_token(ny, t, False))
        for t in sor.jelentes))


def _ubs_glossza(ny, g, strong):
    if g.glossza is None:
        return ny.s('e2.dbh.nincs_a_tablaban')
    kulcs = 'e2.ubs.glossza.var' if g.forditasra_var else 'e2.ubs.glossza'
    elem = ny.s(kulcs, glossza=g.glossza, strong=strong)
    if g.nem_egyertelmu:
        elem = ny.s('e2.ubs.nem_egyertelmu', elem=elem)
    if g.mt_vers is not None:
        elem = ny.s('e2.ubs.mt', elem=elem, vers=g.mt_vers)
    return elem


def _dbh_ok(ny, ok):
    if ok.ok is DbhOk.NINCS_HIVATKOZAS:
        return ny.s('e2.dbh.ok.nincs_hivatkozas', vers=ok.vers)
    return ny.s(_DBH_OK_SABLON[ok.ok])


def _ubs(ny, cella):
    if cella.forras is UbsForras.NEM_ALKALMAZHATO:
        return ny.s('e2.ubs.tematikus')
    dbh = cella.forras is UbsForras.DBH
    if not cella.tokenek:
        return ny.s('e2.dbh.nincs_h_token' if dbh else 'e2.ubs.nincs_g_token')
    if dbh and not any(t.glosszak for t in cella.tokenek):
        elemek = []
        for t in cella.tokenek:
            okok = tuple(_dbh_ok(ny, o) for o in t.okok)
            elem = ny.s('e2.dbh.egyik_sem.okkal', okok=okok) if okok else ny.s('e2.dbh.egyik_sem.ok_nelkul')
            if elem not in elemek:
                elemek.append(elem)
        return ny.s('e2.dbh.egyik_sem', elemek=tuple(elemek))
    tartalmak = []
    for t in cella.tokenek:
        if t.glosszak:
            tartalom = ny.s('e2.ubs.lista', elemek=tuple(_ubs_glossza(ny, g, t.strong) for g in t.glosszak))
        elif dbh:
            okok = tuple(_dbh_ok(ny, o) for o in t.okok)
            tartalom = ny.s('e2.dbh.nincs_hivatkozas.okkal', okok=okok) if okok else ny.s('e2.dbh.nincs_hivatkozas')
        else:
            tartalom = None
        tartalmak.append((t.strong, tartalom))
    if len(tartalmak) == 1:
        return tartalmak[0][1] if tartalmak[0][1] is not None else ny.s('e2.ubs.nincs_hozzarendeles')
    return ny.s('e2.ubs.tokenek', tokenek=tuple(
        ny.s('e2.ubs.tokenenkent', strong=strong,
             tartalom=tartalom if tartalom is not None else ny.s('e2.ubs.nincs_hozzarendeles.token'))
        for strong, tartalom in tartalmak))


def _nev_vagy_jel(ny, tipus, kulcs):
    return ny.s('ertek.nev', n=ny.nev(tipus, kulcs)) if kulcs is not None else ny.s('jel.nincs')


def _cella(ny, tartalom, *jelek):
    """Egy táblacella: a tartalom változatlanul, utána az esetleges jegyzetjel."""
    return (tartalom,) + jelek


def _tabla_sor(iro, ny, sor, szakasz, jegyzetszam):
    jel = (lj_hivatkozas(szakasz, jegyzetszam),) if jegyzetszam else ()
    tematikus = sor.tematikus_szo_nelkul or sor.sajat_szo
    if sor.tematikus_szo_nelkul:
        strong = ny.s('e2.strong.nincs_lanc')
    else:
        strong = ny.s('e2.strong', strongok=sor.strongok) if sor.strongok else ny.s('jel.nincs')
    iro.tabla_sor((
        _cella(ny, ny.s('e2.igehely_link', hely=sor.igehely, horgony=sor.horgony)),
        _cella(ny, _kulcsszo(ny, sor)),
        _cella(ny, _jelentes(ny, sor), *(() if tematikus else jel)),
        _cella(ny, sor.funkcio_cimke if sor.funkcio_cimke is not None else ny.s('jel.nincs')),
        _cella(ny, ny.s('e2.pardes', szintek=tuple(ny.nev('pardes_szint', sz) for sz in sor.pardes_szintek))
               if sor.pardes_szintek else ny.s('jel.nincs')),
        _cella(ny, strong),
        _cella(ny, _ubs(ny, sor.ubs)),
        _cella(ny, ny.s('e2.megb_cella', megb=_nev_vagy_jel(ny, 'megbizhatosag', sor.megbizhatosag),
                        mod=_nev_vagy_jel(ny, 'azonositas_modja', sor.azonositas_modja)), *jel),
    ))


# --- a tábla alatti jegyzet -------------------------------------------------------------------------------------

def _igazolas(ny, jegyzet):
    """Az igazolás mondatkezdő alakban, vagy None, ha a sornak nincs igazolás-értéke."""
    if jegyzet.igazolas is None:
        return None
    if jegyzet.igazolas is Igazolas.HATOKORON_KIVUL:
        return ny.s('e2.igazolas.ujszovetsegi' if jegyzet.ujszovetsegi else 'e2.igazolas.nem_alkalmazhato')
    return ny.s(_IGAZOLAS_SABLON[jegyzet.igazolas])


def _tartomany(ny, indok):
    return ny.s('e2.jm.tartomanyban', tartomany=ny.s('e2.jm.tartomany', kezdo=indok.kezdo_vers, veg=indok.veg))


def _hanyszor(ny, indok):
    return ny.s('e2.jm.tobb_token', hanyszor=ny.nev('hanyszor', str(indok.darab)))


def _kutatoi(ny, indok):
    if indok.fej:
        return ny.s('e2.jm.kutatoi.fej', szotar=ny.nev('szotar', indok.szotar))
    return ny.s('e2.jm.kutatoi', szotar=ny.nev('szotar', indok.szotar), jel=indok.jel)


def _jelentes_mondat(ny, token):
    """Az egyszavas sor jegyzetének jelentés-része: a címke indoka, az első indok szerint; None, ha nincs mit
    mondani."""
    if not token.indokok:
        return None
    elso = token.indokok[0]
    fajtak = [i.fajta for i in token.indokok]
    if elso.fajta is IndokFajta.BDB_PELDA:
        return ny.s('e2.jm.bdb_pelda', szakasz=elso.szakaszok[0])
    if elso.fajta is IndokFajta.MASUTT_IS:
        return ny.s('e2.jm.masutt_is', szakaszok=ny.s('lista.vesszo', elemek=elso.szakaszok))
    if elso.fajta in _KUTATOI:
        return _kutatoi(ny, elso)
    if elso.fajta is IndokFajta.TAGOLATLAN:
        return ny.s('e2.jm.tagolatlan')
    if elso.fajta is IndokFajta.NINCS_LEKEPEZVE:
        return ny.s('e2.jm.nincs_lekepezve')
    if elso.fajta is IndokFajta.TOBB_TOKEN:
        return _hanyszor(ny, elso)
    if elso.fajta is IndokFajta.TARTOMANYBAN:
        return _tartomany(ny, elso)
    if elso.fajta is IndokFajta.NEM_AZONOSITHATO:
        return ny.s('e2.jm.nem_azonosithato')
    if elso.fajta is IndokFajta.FORRAS_JAVITAS and IndokFajta.BDB_PELDA in fajtak:
        return ny.s('e2.jm.sajtohiba', idezett=elso.idezett)
    if elso.fajta is IndokFajta.THAYER_PELDA and elso.darab:
        return ny.s('e2.jm.thayer_pelda', n=elso.darab)
    if elso.fajta is IndokFajta.THAYER_NEM_IDEZI:
        return ny.s('e2.jm.thayer_nem_idezi')
    return None


def _tomor(ny, token):
    """A többszavas (szópáros) sor jegyzetében egy szó rövid mondata: a cella tartalmát nem ismétli; None, ha a
    jegyzet erről a szóról nem mond semmit."""
    indokok = {i.fajta: i for i in reversed(token.indokok)}
    if IndokFajta.TARTOMANYBAN in indokok:
        return _tartomany(ny, indokok[IndokFajta.TARTOMANYBAN])
    if IndokFajta.TOBB_TOKEN in indokok:
        return _hanyszor(ny, indokok[IndokFajta.TOBB_TOKEN])
    if IndokFajta.FORRAS_JAVITAS in indokok and IndokFajta.BDB_PELDA in indokok:
        return ny.s('e2.jm.sajtohiba', idezett=indokok[IndokFajta.FORRAS_JAVITAS].idezett)
    if IndokFajta.BDB_PELDA in indokok:
        return ny.s('e2.jm.maga_idezi')
    if IndokFajta.TAGOLATLAN in indokok:
        return ny.s('e2.jm.tagolatlan')
    if IndokFajta.KUTATOI in indokok or IndokFajta.KUTATOI_TAGABB in indokok:
        thayer = indokok.get(IndokFajta.THAYER_PELDA)
        if thayer is not None and thayer.darab:
            return ny.s('e2.jm.szerkesztoi.thayer', n=thayer.darab)
        return ny.s('e2.jm.szerkesztoi')
    if IndokFajta.NINCS_LEKEPEZVE in indokok:
        return ny.s('e2.jm.nincs_lekepezve')
    if IndokFajta.NEM_AZONOSITHATO in indokok:
        return ny.s('e2.jm.nem_azonosithato')
    return None


def _jegyzet(ny, sor, szopar):
    """A sor jegyzetének látható mondata."""
    jegyzet = sor.jegyzet
    if jegyzet.fajta is JegyzetFajta.TEMATIKUS:
        return ny.s('e2.jegyzet.tematikus')
    if jegyzet.fajta is JegyzetFajta.TEMATIKUS_SAJAT:
        alak = sor.alakok[0]
        nyelv = 'heber' if alak.strong.heber else 'gorog'
        if alak.kiejtes is not None:
            return ny.s(ny.kulcs('e2.jegyzet.tematikus_sajat', nyelv), szo=alak.alak, kiejtes=alak.kiejtes)
        return ny.s(ny.kulcs('e2.jegyzet.tematikus_sajat', nyelv, 'kiejtes_nelkul'), szo=alak.alak)
    igazolas = _igazolas(ny, jegyzet)
    if szopar or len(sor.jelentes) > 1:
        mondatok = [igazolas] if igazolas is not None else []
        for token in sor.jelentes:
            tomor = _tomor(ny, token)
            if tomor is None:
                continue
            if len(sor.jelentes) > 1:
                mondatok.append(ny.s('e2.jegyzet.szavankent', strong=token.strong, mondat=tomor))
            else:
                mondatok.append(ny.s('e2.jegyzet.a_jelentes', mondat=tomor))
        if not mondatok:
            return ny.s('e2.jegyzet.ures')
        return ny.s('e2.jegyzet.mondatok', mondatok=tuple(mondatok))
    jelentes = _jelentes_mondat(ny, sor.jelentes[0]) if sor.jelentes else None
    if igazolas is not None and jelentes is not None:
        return ny.s('e2.jegyzet', igazolas=igazolas, jelentes=jelentes)
    if igazolas is not None:
        return ny.s('e2.jegyzet.csak_igazolas', igazolas=igazolas)
    if jelentes is not None:
        return ny.s('e2.jegyzet.csak_jelentes', jelentes=jelentes)
    return ny.s('e2.jegyzet.ures')


def _jegyzetek(ny, modell):
    """Az összevont jegyzetek: ([(sorszám, látható mondat, eredeti leírások)], soronként a jegyzet sorszáma).
    Az azonos mondatú jegyzet egyszer áll; a számozás az első hivatkozás sorrendje."""
    lista, hol, soronkent = [], {}, []
    for sor in modell.sorok:
        if sor.jegyzet is None:
            soronkent.append(0)
            continue
        mondat = _jegyzet(ny, sor, modell.szopar)
        if mondat not in hol:
            hol[mondat] = len(lista)
            lista.append((len(lista) + 1, mondat, []))
        szam, _mondat, eredetik = lista[hol[mondat]]
        if sor.jegyzet.eredeti not in eredetik:
            eredetik.append(sor.jegyzet.eredeti)
        soronkent.append(szam)
    return lista, soronkent


def _tetel(iro, ny, tetel):
    iro.sor(horgony_jel(tetel.horgony))
    iro.sor(ny.s('e21.igehely', hely=tetel.igehely))
    for vers in tetel.versek:
        if vers.szoveg is not None:
            iro.sor(ny.s('e21.vers', szoveg=vers.szoveg))
        else:
            iro.sor(ny.s('e21.nincs_vers', vers=vers.vers))
    if tetel.kapcsolodas is not None:
        iro.sor(tetel.kapcsolodas)
    if tetel.funkcio is not None:
        iro.ures()
        iro.sor(ny.s('e21.funkcio', magyarazat=tetel.funkcio))
    iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny = keret.ny
    szakasz = keret.rend.sorszam(AZONOSITO)
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.blokk_nyit(iro, keret, AZONOSITO, forrasok)
    K.olvasoi_bekezdes(iro, _osszegzo(ny, modell.osszegzes))
    iro.sor(ny.s('e2.hatokor', n=modell.osszegzes.helyek, tabla=ny.nev('forras', 'B03'), szakasz=szakasz,
                 alpont=ALPONT_SZOVEG, cimketabla=ny.nev('forras', 'B16'), bdb=ny.nev('forras', 'B19'),
                 thayer=ny.nev('forras', 'B21'), datum=modell.jelentes_dontes))
    iro.ures()
    jegyzetek, soronkent = _jegyzetek(ny, modell)
    iro.tabla_sor(tuple(ny.s(kulcs) for kulcs in FEJLEC))
    iro.tabla_elvalaszto(len(FEJLEC))
    for sor, jegyzetszam in zip(modell.sorok, soronkent):
        _tabla_sor(iro, ny, sor, szakasz, jegyzetszam)
    iro.ures()
    if jegyzetek:
        for szam, mondat, eredetik in jegyzetek:
            iro.sor(lj_fej(szakasz, szam), mondat, *(prov('eredeti: {}', e) for e in eredetik))
        iro.ures()
    if modell.kozos_olvasoi is not None:
        iro.sor(prov('közös forrásmegjelölés: {}', modell.kozos_olvasoi), prov('eredeti: {}', modell.kozos_eredeti))
        iro.ures()
    iro.sor(ny.s('e2.ubs_magyarazat', datum=modell.ubs_dontes, forditastabla=ny.nev('forras', 'B14'),
                 dbh=ny.nev('forras', 'B33'), megfeleltetes=ny.nev('forras', 'B34')))
    iro.ures()
    iro.cimsor(4, ny.s('cim.alpont', szakasz=szakasz, alpont=ALPONT_SZOVEG, cim=ny.s('cim.elofordulasok.szoveg')))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('e21.bevezeto'))
    for tetel in modell.tetelek:
        _tetel(iro, ny, tetel)
    K.blokk_zar(iro, keret, AZONOSITO)
