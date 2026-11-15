"""lapgen.bemenet.kartya_lap — a 4.2 Mélységi szócikk kártyáinak tartalma (S3b: BDB; S3c: Thayer).

Szavanként egy kártya, két réteggel. Az olvasói réteg: a jelentések rendje a szótár szerint (a motívumot hordozó
pont félkövér) és az, hogy a motívum helyein melyik pontban áll a szó. A szótári apparátus (összecsukva): a szócikk
feje, a hordozó szakaszok kibontva, a többi összecsukott futamokban, a szótár szövege szegmentált idézetként (a
`bemenet.kartya` lánca: kiemelés, forrásjavítás, irányjel, rövidítés-feloldás, Károli-számozás, majd a kész lap
lépései).

A kártya szövege a forrás szövegéből készül (glossza, első tagmondat, kiemelés, a régi lánc lépései), ezért ez a
bemeneti réteg része; a kimenet burkolókból (idézet, kézi szöveg) és jelölésekből áll, szabad szöveg nélkül. A lapmodellt a
`szamitas.kartya` állítja elő belőle, a mondat a megjelenítőben, a sablontáblából készül. A régi szabályok helye:
`naplok/F218_folytatas.md` „Az S3b terve”.
"""
import dataclasses
import re
from typing import Optional, Tuple

import szotari_glossza

from lapgen.bemenet import gerinc as gerinc_be
from lapgen.bemenet import kartya as K
from lapgen.bemenet.jelolt import Jelolt, JeloltHiba
from lapgen.szoveg import Igehely, Strong

SZOTAR_BDB, SZOTAR_THAYER = 'BDB', 'Thayer'
_TILTOTT_OSZLOPOK = ('magyar_alak', 'minta')
_FEJ, _TAGOLATLAN = 'fej', 'tagolatlan'


def b58_tiltott_fordulatok(b):
    """B58 — a tiltott fordulatok: [(magyar alak, lefordított minta)] (a régi `tiltott_talalatok` mintái, kis- és
    nagybetűtől függetlenül)."""
    def betolt():
        return tuple((r['magyar_alak'], re.compile(r['minta'], re.I))
                     for r in b._tabla('B58', oszlopok=_TILTOTT_OSZLOPOK).szotarak() if r['minta'])
    return b.egyszer('B58', betolt)


def _tiltott_kapu(k, strong, szocikkek, szotar):
    """GK-06 (az 5. ellenőrzés E4 tétele): a régi kártya a tiltott fordulatot tartalmazó magyar szöveg alá
    ⓘ-megjegyzést írt („ismert hiány: … tiltott fordulatot tartalmaz”); ez az ág nincs portolva, ezért a kártya
    ilyenkor kimondott hibával megáll (nem némán marad el a megjegyzés). A szöveg a fej és a szakaszok magyar
    szövege, ahogy a régi `gerinc_blokk` vizsgálta."""
    tiltott = b58_tiltott_fordulatok(k.b)
    talalat = []
    for sz in szocikkek:
        for elem in ([sz['fej']] if sz['fej'] else []) + list(sz['szakaszok']):
            hu = elem[2] or ''
            talalat.extend('%s (%s)' % (alak, elem[0]) for alak, minta in tiltott if minta.search(hu))
    if talalat:
        raise JeloltHiba('a(z) %s %s-szövege tiltott fordulatot tartalmaz (%s): a régi ⓘ-megjegyzés ága nincs '
                         'portolva; a javítás a fordítás újrafuttatása' % (strong.kod, szotar, '; '.join(talalat)))


# --- a modell ------------------------------------------------------------------------------------------------
@dataclasses.dataclass
class OlvasoiSor:
    """A jelentések rendjének egy sora. `fajta`: 'szocikk' (több szócikk neve), 'tagolatlan', 'szakasz'.
    `tartalom`: 'glossza' / 'csak_alak' / 'kulon' (a szakasz meghatározása)."""
    fajta: str
    behuzas: int = 0
    sorszam: int = 0
    arami: bool = False
    felkover: bool = False
    jel: object = None              # Forrasszoveg (a jel prózai alakja: „2.”)
    jel_nyers: object = None        # Forrasszoveg (a jel nyers alakja: „2”)
    jel_szam: bool = False          # a jel puszta szám (a pontozott alakja escape-elve áll)
    gondolatjel: bool = False       # a jel és a meghatározás között gondolatjel
    tartalom: str = 'glossza'
    glossza: object = None          # Forrasszoveg vagy Kezi (címke)
    hely_db: int = 0


@dataclasses.dataclass
class PontNev:
    """Egy pont neve a „motívum helyein” mondatban. `fajta`: 'szakasz', 'tagolatlan', 'csak_alakkent'."""
    fajta: str
    szocikk: Optional[Tuple[int, bool]] = None    # (a szócikk sorszáma, arámi-e), ha a szónak több szócikke van
    jel: object = None
    gondolatjel: bool = False
    glossza: object = None
    bizonytalan: Tuple[str, ...] = ()


@dataclasses.dataclass
class HelyCsoport:
    versek: Tuple[Igehely, ...]
    nevek: Tuple[PontNev, ...]


@dataclasses.dataclass
class Osszecsukott:
    """Összecsukott futam: egy szakasz (`jelek` egy elemű) vagy több; `glosszak` a summary meghatározásai."""
    jelek: Tuple[object, ...]       # Forrasszoveg (prózai alak: „2.”)
    glosszak: Tuple[object, ...]
    hely_db: int
    vazlatok: Tuple[Tuple[object, object], ...]     # (a jel nyers alakja, Jelolt vagy Kezi)


@dataclasses.dataclass
class AppElem:
    """Az apparátus egy bekezdése. `fajta`: 'fejcim', 'fej', 'szakasz', 'futam'."""
    fajta: str
    bek: object = None              # bemenet.kartya.Bekezdes (a lánc a szegmentált idézeten)
    adat: object = None


@dataclasses.dataclass
class Kartya:
    strong: Strong
    szotar: str
    olvasoi: Tuple[OlvasoiSor, ...]
    helyein: Tuple[HelyCsoport, ...]
    nem_idezett: Tuple[Igehely, ...]
    tartomanyban: Tuple[Igehely, ...]
    pont_nelkul: Tuple[Igehely, ...]
    apparatus: Tuple[AppElem, ...]
    megjegyzes: Tuple[object, ...]          # (vers, Tartomany, pontos jel Forrasszoveg)


# --- segédek -------------------------------------------------------------------------------------------------
def _melyseg(jel):
    return len([x for x in re.split(r'[ .]', jel) if x]) - 1


def _os_pont(a, b):
    if a[0] != b[0] or a[1] in (_FEJ, _TAGOLATLAN) or b[1] in (_FEJ, _TAGOLATLAN):
        return False
    pa, pb = K.utvonal_vag(a[1]).split('/'), K.utvonal_vag(b[1]).split('/')
    return len(pa) < len(pb) and pb[:len(pa)] == pa


def _helyek_pontjai(vers_pont, szocikkek):
    tagolatlan = {sz['bdb_id'] for sz in szocikkek if not sz['szakaszok']}
    pontok = {}
    for vers, k in vers_pont:
        if k[1] == _FEJ and k[0] in tagolatlan:
            k = (k[0], _TAGOLATLAN)
        lista = pontok.setdefault(vers, [])
        if k not in lista:
            lista.append(k)
    for vers, lista in pontok.items():
        if len(lista) > 1:
            lista[:] = [k for k in lista if k[1] != _FEJ] or lista
            lista[:] = [k for k in lista if not any(_os_pont(k, m) for m in lista)]
    return pontok


class Kornyezet:
    """A kártyák közös bemenetei: a gerinc, a Károli-szöveg, a motívum versei, a könyvek, a fordítástábla."""

    def __init__(self, b, g, karoli, motivum_versek, konyvek, forditasok):
        self.g, self.b, self.karoli, self.konyvek, self.forditasok = g, b, karoli, konyvek, forditasok
        self.motivum_versek = set(motivum_versek)

    def igehely(self, kod):
        return self.konyvek.igehely(kod)


# --- az olvasói réteg (a régi `bdb_olvasoi_reteg`) ---------------------------------------------------------------
def _olvasoi(k, strong, fa, p, hiv_db, szotar=SZOTAR_BDB):
    g = k.g
    thayer = szotar == SZOTAR_THAYER
    glossza_fn = szotari_glossza.thayer_glossza if thayer else szotari_glossza.olvasoi_glossza
    szocikkek, _elnyelt = fa
    fa_kulcsok = {sk for sz in szocikkek for sk, _j, _h, _a, _f in sz['szakaszok']}
    kint = [(v, kk) for v, kk in p.vers_pont if kk[1] not in (_FEJ, _TAGOLATLAN) and kk not in fa_kulcsok]
    vers_pont = [x for x in p.vers_pont if x not in kint]
    pont_nelkul = list(p.pont_nelkul) + [v for v, _k in kint]
    gyenge = {pk: sorted(o) for pk, o in p.gyenge.items() if pk not in p.eros}
    lathato = [sz for sz in szocikkek if sz['szakaszok'] or (sz['fej'] and sz['fej'][2])]
    tobb = len(lathato) > 1
    pontok = _helyek_pontjai(vers_pont, szocikkek)
    eros_k = {kk for v, lista in pontok.items() for kk in lista if not gyenge.get((v, kk))}
    felkover = {kk for kk in p.hordozo if kk in eros_k or not any(x == kk for _v, x in vers_pont)}
    nevek, sorok, lat = {}, [], set()
    fej0 = szocikkek[0]['fej'] if szocikkek else None
    fej_gl = szotari_glossza.thayer_fej_glossza(fej0[2]) if thayer and fej0 and fej0[2] else None
    for i, sz in enumerate(lathato, 1):
        szocikk = None
        behuz = 0
        if tobb:
            _szam, _cimszo, arami = g.szocikk_fejcim(strong.kod, sz['bdb_id'])
            szocikk = (i, arami)
            sorok.append(OlvasoiSor('szocikk', sorszam=i, arami=arami))
            behuz = 1
        if not sz['szakaszok']:
            fej_hu = sz['fej'][2] if sz['fej'] else ''
            gl = szotari_glossza.thayer_fej_glossza(fej_hu or '') if thayer else gerinc_be._fej_glossza(fej_hu or '')
            gl = _forras_ertek(k, szotar, strong, gl) if gl else None
            kk = (sz['bdb_id'], _TAGOLATLAN)
            nevek[kk] = PontNev('tagolatlan', szocikk=szocikk, glossza=gl)
            if sz['fej'] and sz['fej'][2]:
                hordoz = any(x[0] == sz['bdb_id'] for _v, x in vers_pont)
                sorok.append(OlvasoiSor('tagolatlan', behuzas=behuz, felkover=hordoz, glossza=gl))
            continue
        if fej_gl:
            kk = (sz['bdb_id'], _FEJ)
            fej_ertek = _forras_ertek(k, szotar, strong, fej_gl)
            nevek[kk] = PontNev('fej_eleje', glossza=fej_ertek)
            sorok.append(OlvasoiSor('fej_eleje', behuzas=behuz, felkover=any(kk in lista for lista in pontok.values()),
                                    glossza=fej_ertek))
        for kk, jel, hu, _angol, _kat in sz['szakaszok']:
            if kk in lat:
                continue
            lat.add(kk)
            cimke = g.cimke_nyers(szotar, strong.kod, kk)
            gl = glossza_fn(jel, cimke, hu)
            tartalom, n = 'glossza', 0
            if not gl and hu and thayer:
                tartalom = 'csak_parhuzam' if szotari_glossza.thayer_csak_alak(hu).endswith('párhuzamot közöl') \
                    else 'csak_alak_thayer'
            elif not gl and hu and K.alakkal_nyilik(szotari_glossza.vegyes_cim_nelkul(
                    jel, szotari_glossza.jelolo_levag(hu, jel))):
                gl = K.alak_utani_glossza(hu)
                if not gl:
                    tartalom, n = 'csak_alak', hiv_db.get(kk, 0)
            elif not gl and not hu and thayer:
                tartalom = 'forditasra_var'
            elif not gl:
                tartalom = 'kulon'
            gl_ertek = _glossza_ertek(k, szotar, strong, kk, jel, cimke, gl) if gl else None
            gondolatjel = jel[:1].isalpha()
            nevek[kk] = PontNev('szakasz', szocikk=szocikk, jel=g.jel(szotar, strong.kod, kk, prozai=True),
                                gondolatjel=gondolatjel, glossza=gl_ertek)
            sorok.append(OlvasoiSor('szakasz', behuzas=behuz + max(0, _melyseg(jel)), felkover=kk in felkover,
                                    jel=g.jel(szotar, strong.kod, kk, prozai=True),
                                    jel_nyers=g.jel(szotar, strong.kod, kk), jel_szam=jel.isdigit(),
                                    gondolatjel=(gl is not None and gondolatjel) or tartalom not in ('glossza', 'kulon'),
                                    tartalom=tartalom, glossza=gl_ertek, hely_db=n))
    csop, rend = {}, []
    for vers, lista in pontok.items():
        kulcs = tuple((kk, tuple(gyenge.get((vers, kk), ()))) for kk in lista)
        if kulcs not in csop:
            csop[kulcs] = []
            rend.append(kulcs)
        csop[kulcs].append(vers)
    helyein = []
    for kulcs in rend:
        nevsor = []
        for kk, okok in kulcs:
            if kk[1] == _FEJ:
                nev = (nevek.get(kk) if thayer else None) or PontNev('csak_alakkent')
            else:
                nev = nevek.get(kk) or PontNev('szakasz', jel=g.jel(szotar, strong.kod, kk, prozai=True))
            nevsor.append(dataclasses.replace(nev, bizonytalan=okok))
        helyein.append(HelyCsoport(tuple(k.igehely(v) for v in csop[kulcs]), tuple(nevsor)))
    pont_nelkul = [v for v in dict.fromkeys(pont_nelkul) if v not in pontok]
    return (tuple(sorok), tuple(helyein), tuple(k.igehely(v) for v in p.nem_idezett),
            tuple(k.igehely(v) for v, _t in p.tartomanyban), tuple(k.igehely(v) for v in pont_nelkul))


def _forras_ertek(k, szotar, strong, szoveg):
    """A szótár magyar szövegének részlete idézetként: a BDB-nél a szakasztábla fordítása (B18), a Thayernél a
    fordítástábla (B14)."""
    if szotar == SZOTAR_THAYER:
        return k.b.forrasszoveg('B14', 'forditas_hu', szoveg, strong)
    return k.b.forrasszoveg('B18', 'szoveg_hu', szoveg, strong)


def _glossza_ertek(k, szotar, strong, kk, jel, cimke, gl):
    """A meghatározás: a címke (kézi) változatlanul, ha a meghatározás maga a címke; különben a szótár szövegének
    részlete (idézet)."""
    if cimke:
        if gl != cimke:
            raise JeloltHiba('a(z) %s %s címkéjét a régi lap átalakítva írta (%r → %r): a címke a forrásban javítandó'
                             % (strong.kod, jel, cimke, gl))
        return k.g.cimke(szotar, strong.kod, kk)
    return _forras_ertek(k, szotar, strong, gl)


# --- az apparátus (a régi `gerinc_blokk` második fele és `gerinc_szakasz_lista`) ------------------------------------
def _jelolt(k, strong, szoveg, szotar=SZOTAR_BDB):
    if '\n' in szoveg:
        raise JeloltHiba('a(z) %s szótári szövege sortörést tartalmaz' % strong.kod)
    if szotar == SZOTAR_THAYER:
        return Jelolt(szoveg, 'B14', 'forditas_hu', strong)
    return Jelolt(szoveg, 'B18', 'szoveg_hu', strong)


def _futam_elem(k, strong, futam, szotar=SZOTAR_BDB):
    """Az összecsukott futam: a summary és a vázlatsorok; a bekezdés a régi keret-alakkal."""
    gls = [x[3] for x in futam if x[3]]
    if len(futam) == 1:
        jel, _kk, _v, gl, n, _ge, _m = futam[0]
        cim = ('%s — %s (%s)' % (gerinc_be.pontos_jel(jel), gl, _hely(n))) if gl else \
            '%s (%s)' % (gerinc_be.pontos_jel(jel), _hely(n))
    else:
        cim = '%s – %s (%d szakasz)%s' % (gerinc_be.pontos_jel(futam[0][0]), gerinc_be.pontos_jel(futam[-1][0]),
                                          len(futam), (': ' + ' · '.join(gls[:4]) + (' …' if len(gls) > 4 else ''))
                                          if gls else '')
    darabok = [K.Keret('<details>\n<summary>%s</summary>\n\n' % cim)]
    vazlatok = []
    for n, (jel, kk, vazlat, _gl, _db, _ge, megjelenito) in enumerate(futam):
        if n:
            darabok.append(K.Keret('\n'))
        darabok.append(K.Keret('- `%s` — ' % jel, '- %s — ' % jel))
        darabok.append(vazlat)
        vazlatok.append((k.g.jel(szotar, strong.kod, kk), megjelenito))
    darabok.append(K.Keret('\n\n</details>'))
    jelek = tuple(k.g.jel(szotar, strong.kod, f[1], prozai=True) for f in (futam[:1] if len(futam) == 1
                                                                           else (futam[0], futam[-1])))
    gl_ertekek = tuple(f[5] for f in futam if f[5] is not None)
    return AppElem('futam', K.Bekezdes(darabok), Osszecsukott(jelek, gl_ertekek, futam[0][4] if len(futam) == 1 else 0,
                                                            tuple(vazlatok)))


def _hely(n):
    return '%d hivatkozás' % n if n else 'hivatkozás nélkül'


def _szakasz_lista(k, strong, szakaszok, p, elnyelt, hiv_db, szotar=SZOTAR_BDB):
    """A szócikk szakaszai: a hordozó kibontva, a többi összecsukott futamokban."""
    thayer = szotar == SZOTAR_THAYER
    g = k.g
    elnyelo = {}
    for kk, hova in elnyelt.items():
        elnyelo.setdefault(hova, []).append(kk)
    ki, futam = [], []

    def lezar():
        if futam:
            ki.append(_futam_elem(k, strong, list(futam), szotar))
            del futam[:]

    for kk, jel, hu, angol, kat in szakaszok:
        cimke = g.cimke_nyers(szotar, strong.kod, kk)
        if kk in elnyelo or kk in elnyelt:
            raise JeloltHiba('a(z) %s szócikkhatáron átnyúló (elnyelt) szakasza: a mondata még nincs portolva' % strong.kod)
        if kk not in p.hordozo:
            if cimke:
                if szotari_glossza.vegyes_cim_nelkul(jel, cimke) != cimke:
                    raise JeloltHiba('a(z) %s %s címkéjét a régi lap átalakítva írta' % (strong.kod, jel))
                vazlat = g.cimke(szotar, strong.kod, kk)
                kiemelt = K.Keret(cimke)
            else:
                resz, cs = K.elso_tagmondat(hu or angol, csonkit_jel=True)
                resz = szotari_glossza.vegyes_cim_nelkul(jel, resz)
                if not hu:
                    raise JeloltHiba('a(z) %s %s szakaszának nincs magyar szövege: a vázlatsor angol ága nincs portolva'
                                     % (strong.kod, jel))
                vazlat = _jelolt(k, strong, resz, szotar)
                if cs:
                    vazlat.beszur(len(resz), K.csonk(cs))
                K.kiemel(vazlat, [], k.motivum_versek, k.igehely)
                kiemelt = vazlat
            gl = (szotari_glossza.thayer_glossza if thayer else szotari_glossza.olvasoi_glossza)(jel, cimke, hu)
            if not gl and not thayer:
                gl = K.gondolatjel_utani_glossza(hu)
            gl_ertek = _glossza_ertek(k, szotar, strong, kk, jel, cimke, gl) if gl else None
            futam.append((jel, kk, kiemelt, gl, hiv_db.get(kk, 0), gl_ertek, vazlat))
            continue
        lezar()
        if kat == 'horgonnyal':
            raise JeloltHiba('a(z) %s %s kibontott szakasza horgonnyal illesztett: a jelölése nincs portolva'
                             % (strong.kod, jel))
        if not hu:
            raise JeloltHiba('a(z) %s %s kibontott szakaszának nincs magyar szövege: a „fordításra vár” ág nincs '
                             'portolva' % (strong.kod, jel))
        idezet = _jelolt(k, strong, szotari_glossza.jelolo_levag(hu, jel), szotar)
        K.kiemel(idezet, p.celok.get(kk, []), k.motivum_versek, k.igehely)
        cim, cim_ertek = cimke, (g.cimke(szotar, strong.kod, kk) if cimke else None)
        if not cimke and thayer:
            cim = szotari_glossza.thayer_glossza(jel, '', hu)
            cim_ertek = _forras_ertek(k, szotar, strong, cim) if cim else None
        fej_regi = ('- **`%s` — %s**' % (jel, cim)) if cim else '- **`%s`**' % jel
        fej_kesz = ('- **%s — %s**' % (jel, cim)) if cim else '- **%s**' % jel
        bek = K.Bekezdes([K.Keret(fej_regi + '\n\n  > ', fej_kesz + '\n\n  > '), idezet])
        ki.append(AppElem('szakasz', bek, (g.jel(szotar, strong.kod, kk), cim_ertek, idezet)))
    lezar()
    return ki


def bdb_kartya(k, strong, kut_kulcsok, versek, cimszo):
    """Egy héber szó BDB-kártyája. `versek`: a szó motívumbeli versei (Károli-kulcsok, a sorok rendjében);
    `cimszo`: (a címszó és kiejtése a rövidítés feloldásához, a címszó első alapbetűje)."""
    g, st = k.g, strong.kod
    fa = g.kartya_fa(st)
    szocikkek, elnyelt = fa
    _tiltott_kapu(k, strong, szocikkek, SZOTAR_BDB)
    p = K.bdb_pontok(g, st, versek, kut_kulcsok, fa)
    hiv_db = K.hivatkozas_szam(g, st, fa)
    tobb = len(szocikkek) > 1
    app = []
    for i, sz in enumerate(szocikkek, 1):
        if tobb:
            szam, cimszo_nyers, arami = g.szocikk_fejcim(st, sz['bdb_id'])
            utana = ' · arámi' if arami else ''
            vege = '** *(a %s %d. BDB-szócikke a %d-ből)*' % (st, i, len(szocikkek))
            if cimszo_nyers:
                cimszo_j = Jelolt(cimszo_nyers, 'B17', 'cimszo', strong)
                darabok = [K.Keret('**BDB%d · ' % szam, '**BDB %d. szócikk · ' % szam), cimszo_j,
                           K.Keret(utana + vege)]
            else:
                cimszo_j = None
                darabok = [K.Keret('**BDB%d%s%s' % (szam, utana, vege), '**BDB %d. szócikk%s%s' % (szam, utana, vege))]
            app.append(AppElem('fejcim', K.Bekezdes(darabok), (szam, cimszo_j, arami, i, len(szocikkek))))
        fej = sz['fej']
        if fej and fej[2]:
            j = _jelolt(k, strong, fej[2])
            K.kiemel(j, p.fej_celok.get(sz['bdb_id'], []), k.motivum_versek, k.igehely)
            app.append(AppElem('fej', K.Bekezdes([K.Keret(K.FEJ_KERET), j]), j))
        elif fej:
            raise JeloltHiba('a(z) %s szócikkfeje magyar szöveg nélkül áll: az ág nincs portolva' % st)
        app.extend(_szakasz_lista(k, strong, sz['szakaszok'], p, elnyelt, hiv_db))
    # a kártya-lánc a régi bekezdéseken (a rövidítés, a Károli-számozás)
    terkep = g.karoli_terkep(st)
    for elem in app:
        K.forrasjavitas(elem.bek, st, g.javitasok)
        K.izolal(elem.bek)
        K.rovidites(elem.bek, cimszo[0], cimszo[1])
        K.karoli_szamozas(elem.bek, terkep, k.karoli.halmaz(), k.b, strong)
        K.azonosito_kapu(elem.bek)
    for elem in app:                         # a kész lap lépései: írásjel-takarítás, a BDB belső jelei
        elem.bek.kesz = True
        K.takaritas(elem.bek)
        K.belso_jelek_torlese(elem.bek)
    olvasoi, helyein, nem_idezett, tartomanyban, pont_nelkul = _olvasoi(k, strong, fa, p, hiv_db)
    megj = []
    for vers, tartomanyok in p.tartomanyban:
        for t in tartomanyok:
            if g.kulcs_jel(SZOTAR_BDB, st, t.kulcs) != gerinc_be.szakasz_jel(t.kulcs[1]):
                raise JeloltHiba('a(z) %s tartomány-megjegyzése több szócikkes szakaszra mutat: a megnevezése nincs '
                                 'portolva' % st)
            megj.append((k.igehely(vers), t, g.jel(SZOTAR_BDB, st, t.kulcs, prozai=True)))
    return Kartya(strong, SZOTAR_BDB, olvasoi, helyein, nem_idezett, tartomanyban, pont_nelkul, tuple(app),
                  tuple(megj))


def thayer_kartya(k, strong, kut_kulcsok, versek):
    """Egy görög szó Thayer-kártyája (az S3c-ből): ugyanaz a két réteg, a Thayer szakaszaival és a fordítástábla
    szövegével; rövidítés-feloldás és Károli-számozás nélkül (a régi lánc ezeket csak a BDB-n futtatta). Alatta az
    UBS-doménsor."""
    g, st = k.g, strong.kod
    fa = g.thayer_fa(st, k.forditasok)
    szocikkek, _elnyelt = fa
    _tiltott_kapu(k, strong, szocikkek, SZOTAR_THAYER)
    p = K.thayer_pontok(g, st, versek, kut_kulcsok, fa)
    hiv_db = g.thayer_hivatkozas_szam(st)
    sz = szocikkek[0]
    app = []
    fej = sz['fej']
    if fej and fej[2]:
        j = _jelolt(k, strong, fej[2], SZOTAR_THAYER)
        K.kiemel(j, p.fej_celok.get('', []), k.motivum_versek, k.igehely)
        app.append(AppElem('fej', K.Bekezdes([K.Keret(K.FEJ_KERET), j]), j))
    elif fej:
        raise JeloltHiba('a(z) %s Thayer-feje magyar szöveg nélkül áll: az ág nincs portolva' % st)
    app.extend(_szakasz_lista(k, strong, sz['szakaszok'], p, {}, hiv_db, SZOTAR_THAYER))
    for elem in app:
        K.azonosito_kapu(elem.bek)
    for elem in app:
        elem.bek.kesz = True
        K.takaritas(elem.bek)
        K.belso_jelek_torlese(elem.bek)
    olvasoi, helyein, nem_idezett, tartomanyban, pont_nelkul = _olvasoi(k, strong, fa, p, hiv_db, SZOTAR_THAYER)
    return Kartya(strong, SZOTAR_THAYER, olvasoi, helyein, nem_idezett, tartomanyban, pont_nelkul, tuple(app), ())


def kiejtes_menet(kartyak, latott, kiejto):
    """A kész lap kiejtés-pótlása a nyelvrész kártyáin, a lap rendjében: a vázlatsorok, a fejcímek és a kibontott
    szakaszok címsora (a régi lánc szerint ezek nem idézet-sorok). Utána a digitalizálás jelei (a régi 12. lépés)."""
    for kartya in kartyak:
        for elem in kartya.apparatus:
            if elem.fajta == 'fejcim':
                K.kiejtes_potlas(elem.bek, '', latott, kiejto)
            elif elem.fajta == 'futam':
                _sorok_menet(elem.bek, latott, kiejto)
            elif elem.fajta == 'szakasz':
                fej = elem.bek.darabok[0]
                K.latott_kulcsok(fej.kesz.split('\n')[0], latott)
    for kartya in kartyak:
        for elem in kartya.apparatus:
            K.digitalizalas_jelei(elem.bek)


def _sorok_menet(bek, latott, kiejto):
    """A futam vázlatsorai egyenként (a summary idézet-sor, kimarad)."""
    sorok = []
    akt = None
    for d in bek.darabok:
        if isinstance(d, K.Keret) and d.kesz.startswith('- '):
            akt = [d]
            sorok.append(akt)
        elif akt is not None and not (isinstance(d, K.Keret) and d.kesz.startswith('\n')):
            akt.append(d)
        else:
            akt = None
    for n, darabok in enumerate(sorok):
        sor = K.Bekezdes(darabok)
        sor.kesz = True
        kovetkezo = ''
        if n + 1 < len(sorok):
            kov = K.Bekezdes(sorok[n + 1])
            kov.kesz = True
            kovetkezo = kov.szoveg()
        K.kiejtes_potlas(sor, kovetkezo, latott, kiejto)
