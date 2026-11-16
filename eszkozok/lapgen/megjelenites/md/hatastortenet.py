"""lapgen.megjelenites.md.hatastortenet — a „9. Hatástörténet: ókori fordítások és értelmezők” szakasz (S7).

Minden látható mondat a sablontáblából jön (`s9.*`); a fordítások szavai, a görög és a latin alakok, a mű címe idézet
(a visszhang-tábla, a görög szöveg és a tanúk táblája szerint), a tanú neve, kora és a „Mit lát” mondat kézi próza; a
lánc könyvének neve, a számszavak és a hagyományok neve a névtáblából. A szakaszban generált blokk-jelölő nincs (a mai
lapon sincs); a forrásai a Kolofonba kerülnek (S8).
"""
from lapgen import konfig
from lapgen.ertekek import ForrasAllapot, TanuForras
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.dontesi_ut import ALPONT_FORRASOK
from lapgen.megjelenites.md.iro import SORTORES
from lapgen.megjelenites.md.szocikkek import szo_iras
from lapgen.szamitas.hatastortenet import (BetoldasFajta, CellaFajta, Egyesites, EgyesitesFajta, Forditas, Hiany,
                                           LxxFajta, LxxMondat, Mondat, Sav, Utalas, UszMit)
from lapgen.szamitas.vizsgalat import KapuHiba

AZONOSITO = 'hatastortenet'
DONTESI_UT, ELOFORDULASOK, SZOCIKKEK, LXX = 'dontesi_ut', 'elofordulasok', 'szocikkek', 'lxx'
_LANC_KONYV = 'lanc_konyv'
_HIANY = {Hiany.NINCS_SZO: 's9.hiany.nincs_szo', Hiany.NINCS_ELLENORZOTT: 's9.hiany.nincs_ellenorzott',
          Hiany.NINCS_KINYERES: 's9.hiany.nincs_kinyeres'}
_NEV = {Forditas.TARGUM: 's9.nev.targum', Forditas.VULGATA: 's9.nev.vulgata', Forditas.LXX: 's9.nev.lxx'}
_NEV_NAGY = {(Forditas.TARGUM,): 's9.nev.nagy.targum', (Forditas.VULGATA,): 's9.nev.nagy.vulgata',
             (Forditas.LXX,): 's9.nev.nagy.lxx', (Forditas.TARGUM, Forditas.VULGATA): 's9.nev.nagy.tv'}
_KOVET = {Forditas.TARGUM: 's9.nev.targum', Forditas.VULGATA: 's9.nev.vulgata', Forditas.LXX: 's9.nev.septuaginta'}
_SAV = {(Sav.SZOKASOS, False): 's9.lxx.szokasos', (Sav.SZOKASOS, True): 's9.lxx.szokasos.szocsalad',
        (Sav.GYAKORI, False): 's9.lxx.gyakori', (Sav.GYAKORI, True): 's9.lxx.gyakori.szocsalad',
        (Sav.RITKA, False): 's9.lxx.ritka', (Sav.RITKA, True): 's9.lxx.ritka'}
_EGYESITES = {EgyesitesFajta.NEM_MERHETO: 's9.egy.nem_merheto', EgyesitesFajta.SZOKASOS: 's9.egy.szokasos',
              EgyesitesFajta.RITKA: 's9.egy.ritka', EgyesitesFajta.GYAKORI: 's9.egy.gyakori'}
_OSZ_FEJLEC = ('s9.osz.fejlec.szo', 's9.osz.fejlec.targum', 's9.osz.fejlec.vulgata', 's9.osz.fejlec.lxx',
               's9.osz.fejlec.mit')
_TANU_FEJLEC = ('s9.tanu.fejlec.hely', 's9.tanu.fejlec.tanu', 's9.tanu.fejlec.mit', 's9.tanu.fejlec.forras')
_TANU_FORRAS = {TanuForras.HCF: 's9.tanu.forras.hcf', TanuForras.SEFARIA: 's9.tanu.forras.sefaria'}


def _szamszo(ny, n):
    """A szám szóalakja a névtáblából (két, három …), híján a szám."""
    if ny.nevtabla.van('szamszo', str(n)):
        return ny.s('ertek.nev', n=ny.nev('szamszo', str(n)))
    return ny.s('s9.szam', n=n)


def _szo_nev(ny, szo):
    """A szó neve a prózában névelővel (a régi `_szo_nev`): a kiejtés, híján a szótári alak, híján a Strong-szám."""
    if szo.kiejtes is not None:
        return ny.s('s9.szo.nev', kiejtes=szo.kiejtes)
    if szo.alak is not None:
        return ny.s('s9.szo.nev.alak', alak=szo.alak)
    return ny.s('s9.szo.nev.strong', strong=szo.strong)


def _szo_kiejtes(szo):
    """A szó neve névelő nélkül (a két héber szó a zárójelben): a kiejtés, híján az alak."""
    return szo.kiejtes if szo.kiejtes is not None else szo.alak


def _okori_szo(ny, szo):
    if szo.forditas is Forditas.VULGATA:
        return ny.s('s9.szo.latin', lemma=szo.lemma)
    if szo.kiejtes is None:
        return ny.s('s9.szo.kiejtes_nelkul', lemma=szo.lemma)
    return ny.s('s9.szo', lemma=szo.lemma, kiejtes=szo.kiejtes)


def _vers(ny, e, rovid):
    szo = _okori_szo(ny, e.szo) if e.szo is not None else ny.s(_HIANY[e.hiany])
    return ny.s('s9.cella.vers.rovid', hely=e.hely, szo=szo) if rovid else ny.s('s9.cella.vers', hely=e.hely, szo=szo)


def _versek(ny, versek, rovid):
    return ny.s('s9.versek.rovid', versek=versek) if rovid else ny.s('s9.versek', versek=versek)


def _cella(ny, c, rovid):
    if c.fajta is CellaFajta.NINCS_FORRAS:
        return ny.s('s9.nincs_targum')
    if c.fajta is CellaFajta.NINCS_ADAT:
        szoveg = ny.s(_HIANY[c.hiany])
    elif c.fajta is CellaFajta.KULONBOZO:
        szoveg = ny.s('s9.cella.kulonbozo', db=_szamszo(ny, len(c.versek)),
                      versek=tuple(_vers(ny, e, rovid) for e in c.versek))
    elif c.fajta is CellaFajta.TELJES:
        szoveg = ny.s('s9.cella.teljes', szavak=tuple(_okori_szo(ny, s) for s in c.szavak), n=c.n, nn=c.nn)
    else:
        if c.mind_mas_szo:
            cimke = ny.s('s9.cimke.egy_mas' if len(c.versek) == 1 else 's9.cimke.mas')
        else:
            cimke = ny.s('s9.cimke.egy') if len(c.versek) == 1 else ny.s('s9.cimke.tobb',
                                                                       db=_szamszo(ny, len(c.versek)))
        szoveg = ny.s('s9.cella.resz', szavak=tuple(_okori_szo(ny, s) for s in c.szavak), n=c.n, nn=c.nn,
                      cimke=cimke, versek=tuple(_vers(ny, e, rovid) for e in c.versek))
    if c.targum_kivul:
        return ny.s('s9.cella.targum_kivul', cella=szoveg, versek=tuple(
            ny.s('s9.versek.rovid', versek=(v,)) if rovid else ny.s('s9.versek', versek=(v,)) for v in c.targum_kivul),
            nincs=ny.s('s9.nincs_targum'))
    return szoveg


def _lxx_mondat(ny, m):
    if m.fajta is LxxFajta.NINCS_ADAT:
        return ny.s('s9.lxx.nincs', hiany=ny.s(_HIANY[m.hiany]))
    if m.fajta is LxxFajta.ELTERES:
        reszek = []
        for db, kulcs, egy in ((m.mas, 's9.lxx.mas', 's9.lxx.mas.egy'),
                               (m.nincs_szo, 's9.lxx.nincs_szo', 's9.lxx.nincs_szo.egy'),
                               (m.hianyzo, 's9.lxx.hianyzo', 's9.lxx.hianyzo.egy')):
            if db:
                reszek.append(ny.s(egy) if db == 1 else ny.s(kulcs, n=db))
        return ny.s('s9.lxx.elteres', reszek=tuple(reszek))
    if m.fajta is LxxFajta.NEM_MERHETO:
        return ny.s('s9.lxx.nem_merheto')
    a = m.alapvonal
    return ny.s(_SAV[(a.sav, m.szocsalad)], nn=a.nn, x=a.talalat, p=a.szazalek)


def _egyesites(ny, m):
    nev = ny.s(_NEV_NAGY[m.forditasok])
    a, b = (_szo_kiejtes(s) for s in m.szavak)
    if m.fajta is EgyesitesFajta.NEM_MERHETO_FORRAS:
        return ny.s('s9.egy.forras', nev=nev, a=a, b=b)
    mivel = ny.s('s9.egy.szocsaladdal' if m.szocsalad else 's9.egy.szoval')
    if m.fajta is EgyesitesFajta.NEM_MERHETO:
        return ny.s('s9.egy.nem_merheto', nev=nev, a=a, b=b, mivel=mivel)
    szazalekok = tuple(ny.s('s9.egy.szazalek', szo=_szo_kiejtes(s), p=p) for s, p in zip(m.szavak, m.szazalekok))
    return ny.s(_EGYESITES[m.fajta], nev=nev, a=a, b=b, mivel=mivel, szazalekok=szazalekok)


def _mondat(ny, m):
    """Egy mondat a „Mit mutat” cellában (a modell `Mondat` burkolója, vagy maga a mondat)."""
    if isinstance(m, Mondat):
        m = m.egyesites or m.utalas or m.lxx
    if isinstance(m, Egyesites):
        return _egyesites(ny, m)
    if isinstance(m, Utalas):
        return ny.s('s9.utalas', szo=_szo_nev(ny, m.szo))
    if isinstance(m, LxxMondat):
        return _lxx_mondat(ny, m)
    raise KapuHiba('9.: ismeretlen mondatfajta a „Mit mutat” cellában: %s' % type(m).__name__)


def _osz_bevezeto(ny, o, keret):
    if o.szopar:
        kovetok = tuple(ny.s(_KOVET[fd]) for fd, db in zip((Forditas.TARGUM, Forditas.VULGATA, Forditas.LXX),
                                                             o.teljes) if db)
        kovet = ny.s('s9.osz.szopar.kovet', nevek=kovetok) if kovetok else ny.s('s9.osz.szopar.kovet.nincs')
        if o.par is None:
            raise KapuHiba('9.: a szópáros formula másik szava nem azonosítható')
        return ny.s('s9.osz.bevezeto.szopar', ige=_szo_nev(ny, o.sorok[0].szo), par=_szo_nev(ny, o.par),
                    n=len(o.sorok[0].versek), kovet=kovet)
    p = dict(konyv=ny.nev(_LANC_KONYV, o.mag_hely.konyv), n=len(o.sorok), d=keret.rend.sorszam(DONTESI_UT),
             p=ALPONT_FORRASOK, mag=o.mag_hely, elso=o.mag_elso, utolso=o.mag_utolso,
             e=keret.rend.sorszam(ELOFORDULASOK), m=len(o.sorok) - len(o.egyverses), t=o.teljes[0], v=o.teljes[1],
             l=o.teljes[2])
    if o.egyverses:
        return ny.s('s9.osz.bevezeto.egyverses', egyverses=tuple(_szo_nev(ny, s) for s in o.egyverses), **p)
    return ny.s('s9.osz.bevezeto', **p)


def _osz(iro, ny, o, keret):
    iro.cimsor(3, ny.s('cim.s9.osz'))
    iro.ures()
    K.olvasoi_bekezdes(iro, _osz_bevezeto(ny, o, keret))
    rovid = not o.szopar
    iro.tabla_sor(tuple(ny.s(k) for k in _OSZ_FEJLEC))
    iro.tabla_elvalaszto(len(_OSZ_FEJLEC))
    for s in o.sorok:
        cim = ny.s('s4.p8.rokon.cim', szo=szo_iras(ny, s.szo), jelentes=s.jelentes) if s.jelentes is not None \
            else szo_iras(ny, s.szo)
        iro.tabla_sor(((cim, SORTORES, _versek(ny, s.versek, rovid)),)
                      + tuple(_cella(ny, c, rovid) for c in s.cellak)
                      + (ny.s('s9.mit', mondatok=tuple(_mondat(ny, m) for m in s.mondatok)),))
    for bs in o.betoldasok:
        szo = bs.jelentes if bs.jelentes is not None else ny.s('s9.szo.nev.strong', strong=bs.szo.strong)
        hely = ny.s('s9.betoldas.hely', hely=bs.hely, szo=szo) if rovid \
            else ny.s('s9.betoldas.hely.teljes', hely=bs.hely, szo=szo)
        cellak = []
        for c in bs.cellak:
            if c.fajta is BetoldasFajta.BETOLDAS:
                if c.alak is None or c.jelentes is None:
                    raise KapuHiba('9.: a betoldás cellájához az alak és a jelentés kell')
                cellak.append(ny.s('s9.betoldas.cella', alak=c.alak, kiejtes=c.kiejtes, jelentes=c.jelentes)
                              if c.kiejtes is not None else
                              ny.s('s9.betoldas.cella.kiejtes_nelkul', alak=c.alak, jelentes=c.jelentes))
            elif c.fajta is BetoldasFajta.NINCS_BETOLDAS:
                cellak.append(ny.s('s9.betoldas.nincs'))
            else:
                cellak.append(ny.s('s9.hiany.nincs_ellenorzott'))
        mit = ny.s('s9.betoldas.mit', forditasok=tuple(ny.s(_NEV[fd]) for fd in bs.betoldok), szo=szo) \
            if bs.betoldok else ny.s('jel.nincs')
        iro.tabla_sor(((ny.s('s9.betoldas.cim'), SORTORES, hely),) + tuple(cellak) + (mit,))
    iro.ures()
    iro.sor(ny.s('s9.osz.lab', sz=round(konfig.ALAPVONAL_SZOKASOS * 100), r=round(konfig.ALAPVONAL_RITKA * 100)))
    iro.ures()
    link = ny.s('s9.szakasz_link', sz=keret.rend.sorszam(LXX), horgony=K.szakasz_horgony(keret, LXX))
    iro.sor(ny.s('s9.osz.meres', link=link))
    iro.ures()
    iro.sor(ny.s('s9.osz.rokon', sz=keret.rend.sorszam(SZOCIKKEK), p=konfig.PONT_NYELVI_HATTER))
    iro.ures()


_PESHITTA = {ForrasAllapot.NEM_VIZSGALT: 's9.peshitta.nem_vizsgalt'}


def _usz(iro, ny, u):
    iro.cimsor(3, ny.s('cim.s9.usz'))
    iro.ures()
    szopar = u.szopar
    if not szopar and u.mag_hely is None:
        raise KapuHiba('9.: az újszövetségi tábla a lánc ószövetségi táblája nélkül nem nevezheti meg a láncot')
    konyv = ny.nev(_LANC_KONYV, u.mag_hely.konyv) if not szopar else None
    n, e = len(u.sorok), u.egyezo
    if szopar:
        bevezeto = ny.s('s9.usz.bevezeto.szopar', n=n, e=e)
    elif u.tematikus:
        bevezeto = ny.s('s9.usz.bevezeto.tematikus', helyek=u.tematikus, konyv=konyv, n=n, e=e)
    else:
        bevezeto = ny.s('s9.usz.bevezeto', konyv=konyv, n=n, e=e)
    K.olvasoi_bekezdes(iro, bevezeto)
    fejlec = (ny.s('s9.usz.fejlec.szo'), ny.s('s9.usz.fejlec.vulgata'), ny.s('s9.usz.fejlec.valtozat'),
              ny.s('s9.usz.fejlec.lxx.szopar') if szopar else ny.s('s9.usz.fejlec.lxx', konyv=konyv),
              ny.s('s9.usz.fejlec.mit'))
    iro.tabla_sor(fejlec)
    iro.tabla_elvalaszto(len(fejlec))
    for s in u.sorok:
        szavak = ny.s('s9.usz.szavak', szavak=tuple(szo_iras(ny, sz) for sz in s.szavak))
        vulg = ny.s('s9.usz.vulg', versek=tuple(ny.s('s9.usz.vulg.vers', hely=v.hely, alakok=v.alakok)
                                                  for v in s.vulgata), n=s.n, nn=s.nn)
        valt = []
        for v in s.valtozatok:
            if v.kiejtes is None or (v.mas is not None and v.mas_kiejtes is None):
                raise KapuHiba('9.: a szövegváltozat alakjára nincs gépi kiejtés')
            if v.mas is not None:
                valt.append(ny.s('s9.usz.valt.mas', hely=v.hely, alak=v.alak, kiejtes=v.kiejtes, kiadasok=v.kiadasok,
                                 mas=v.mas, mas_kiejtes=v.mas_kiejtes, hianyzik=v.hianyzik))
            else:
                valt.append(ny.s('s9.usz.valt', hely=v.hely, alak=v.alak, kiejtes=v.kiejtes, kiadasok=v.kiadasok,
                                 hianyzik=v.hianyzik))
        valt_cella = ny.s('s9.usz.valtozatok', valtozatok=tuple(valt)) if valt             else ny.s('s9.usz.valt.nincs.szopar' if szopar else 's9.usz.valt.nincs')
        if s.elo_versek:
            lxx = ny.s('s9.usz.lxx', versek=tuple(_versek(ny, (v,), not szopar) for v in s.elo_versek),
                       lemmak=s.elo_lemmak)
        else:
            lxx = ny.s('s9.usz.lxx.nincs.szopar' if szopar else 's9.usz.lxx.nincs')
        csal = ny.s('s9.usz.csalad', c=s.csalad) if s.csalad is not None else None
        if s.mit is UszMit.EGYEZO:
            mit = ny.s('s9.usz.mit.egyezo.szopar', db=s.osz_db, csal=csal) if szopar \
                else ny.s('s9.usz.mit.egyezo', konyv=konyv, db=s.osz_db, csal=csal)
        elif s.mit is UszMit.RESZBEN:
            mit = ny.s('s9.usz.mit.reszben.szopar', n=s.n, nn=s.nn, csal=csal, db=s.osz_db, on=s.osz_n) if szopar \
                else ny.s('s9.usz.mit.reszben', n=s.n, nn=s.nn, csal=csal, konyv=konyv, db=s.osz_db, on=s.osz_n)
        elif s.mit is UszMit.CSAK_USZ:
            mit = ny.s('s9.usz.mit.csak_usz', n=s.n, nn=s.nn, csal=csal)
        else:
            mit = ny.s('jel.nincs')
        if s.csaladon_belul:
            mit = ny.s('s9.usz.mit.belul', mit=mit)
        iro.tabla_sor(((szavak, SORTORES, ny.s('s9.versek', versek=s.versek)), vulg, valt_cella, lxx, mit))
    iro.ures()
    if u.peshitta not in _PESHITTA:
        raise KapuHiba('9.: a Peshitta forrás-állapotára (%s) nincs mondat' % u.peshitta.value)
    peshitta = ny.s(_PESHITTA[u.peshitta])
    iro.sor(ny.s('s9.usz.lab.szopar', peshitta=peshitta) if szopar
            else ny.s('s9.usz.lab', konyv=konyv, peshitta=peshitta))
    iro.ures()


def _tanu_forras(ny, t):
    if t.forras is TanuForras.GLOSSA:
        return ny.s('s9.tanu.forras.glossa')
    if t.lekerdezve is None:
        raise KapuHiba('9.: a tanú sorához (%s) nincs lekérdezési dátum' % t.forras.value)
    if t.forras is TanuForras.CHAIN_LINEAGE:
        return ny.s('s9.tanu.forras.chain_lineage.biblindex' if t.biblindex else 's9.tanu.forras.chain_lineage',
                    datum=t.lekerdezve)
    return ny.s(_TANU_FORRAS[t.forras], datum=t.lekerdezve)


def _tanuk(iro, ny, tk):
    iro.cimsor(3, ny.s('cim.s9.tanu'))
    iro.ures()
    zaro = ny.s('s9.tanu.db', h=tk.helyek, n=len(tk.sorok)) if tk.sorok else ny.s('s9.tanu.nincs')
    hagyomanyok = tuple(ny.nev('tanu_hagyomany', h) for h in konfig.TANU_HAGYOMANYOK)
    K.olvasoi_bekezdes(iro, ny.s('s9.tanu.bevezeto', hagyomanyok=hagyomanyok, zaro=zaro))
    if tk.sorok:
        iro.tabla_sor(tuple(ny.s(k) for k in _TANU_FEJLEC))
        iro.tabla_elvalaszto(len(_TANU_FEJLEC))
        for t in tk.sorok:
            mu = ny.s('s9.tanu.mu.hely', mu=t.mu, fejezet=t.fejezet, resz=t.resz) if t.fejezet is not None else t.mu
            hagyomany = ny.nev('tanu_hagyomany', t.hagyomany.ertek)
            ki = ny.s('s9.tanu.ki.kor', tanu=t.tanu, mu=mu, hagyomany=hagyomany, kor=t.kor) if t.kor is not None \
                else ny.s('s9.tanu.ki', tanu=t.tanu, mu=mu, hagyomany=hagyomany)
            if t.forras is TanuForras.CHAIN_LINEAGE:
                mit = ny.s('s9.tanu.mit.egyutt', kapcsolat=t.kapcsolat)
            elif t.targyalt:
                mit = ny.s('s9.tanu.mit.targyalt', kapcsolat=t.kapcsolat, helyek=t.targyalt)
            else:
                mit = t.kapcsolat
            iro.tabla_sor((ny.s('e2.igehely_link', hely=t.hely, horgony=t.hely.horgony()), ki, mit,
                           _tanu_forras(ny, t)))
        iro.ures()
    iro.sor(ny.s('s9.tanu.lab'))
    iro.ures()
    if tk.glossa:
        iro.sor(ny.s('s9.tanu.glossa'))
        iro.ures()


def megjelenit(iro, modell, keret, forrasok):
    ny, m = keret.ny, modell
    K.szakasz_cim(iro, keret, AZONOSITO)
    K.olvasoi_bekezdes(iro, ny.s('s9.bevezeto'))
    if m.osz is not None:
        _osz(iro, ny, m.osz, keret)
    if m.usz is not None:
        _usz(iro, ny, m.usz)
    _tanuk(iro, ny, m.tanuk)
