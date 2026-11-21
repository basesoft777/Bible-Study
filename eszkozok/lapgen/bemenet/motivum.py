"""lapgen.bemenet.motivum — a motívum saját sora, a szavak rövid jelentése és a kézi forrás nyitott kérdései.

Bemenetek: B02 (a motívumok táblája: cím, negatív kritérium, fölérendelt fogalom, meghatározás, az azonosság típusa,
a kézi forrás útvonala), B15 (a héber szavak rövid magyar
jelentése), B14 (a görög szavak rövid magyar jelentése a fordítástáblából), B47 (a rések forrásjegyzéke és a motívum
kézi forrása).

A negatív kritérium kézi próza: a réteg csak szerkezetileg bontja két részre (ami ide tartozik; ami nem), a szöveget
nem írja át. A kézi forrásból a vitatott pontok és a nyitott kérdések címe és első mondata szó szerinti részletként
jön (a forrás nézete).
"""
import fnmatch
import re

from lapgen import konfig
from lapgen.bemenet import szavak
from lapgen.bemenet.nyelv import KEZI_FORRASFAJL_TIPUS, b65_nevtabla, folerendelt_mondatkezdo
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.ubs import b14_forditasok

_MOTIVUM_OSZLOPOK = ('id', 'cim', 'negativ_kriterium', 'folerendelt_fogalom', 'meghatarozas', 'azonossag_tipusa',
                     'forras_study')
_FORRAS_ELVALASZTO = ';'
_NEM_TARTOZIK = 'Nem tartozik ide'
_ZAROJEL_ELOTT = ' ('
_MONDATVEG = '.'
_GLOSSZA_OSZLOPOK = ('strong', 'fo', 'glossza_hu', 'glossza_en')
_FO = 'igen'
_SZOTAR_TBESG, _ROVID, _GLOSSZA_MEZO = 'TBESG', 'rovid', 'glosszak_hu'
_RES_OSZLOPOK = ('id', 'res', 'forras', 'tanulmany')
_RES_KEZI = 'tanulmany'
_RES_ERTELMEZES, _RES_MODSZERTAN = 'ertelmezes', 'modszertan'
_RES_RX = r'(?ms)^<!-- RÉS-KEZDET: %s -->\s*\n(.*?)^<!-- RÉS-VÉGE: %s -->'
_VITATOTT_RX = re.compile(r'(?ms)^### ⚠️ Vitatott pontok\s*\n(.*?)(?=^### |\Z)')
_VITATOTT_TETEL_RX = re.compile(r'(?m)^(\*\*[^*]+?\.?\*\*\s+[^.!?]+[.!?])')
_NYITOTT_RX = re.compile(r'(?ms)^### Nyitott kérdések[^\n]*\n(.*?)(?=^### |\Z)')
_NYITOTT_TETEL_RX = re.compile(r'(?m)^\d+\.\s+(\*\*[^*]+?\.?\*\*\s+[^.!?]+[.!?])')


class MotivumSor:
    """A motívum sora: a cím, a negatív kritérium két része (ami ide tartozik; ami nem) és egészben, a fölérendelt
    fogalom (a mező alakjában és mondatkezdő alakban), a meghatározás, kézi prózaként; az azonosság típusa kulcsként
    (a névtábla `azonossag` sora adja az olvasói mondatot); a kézi forrás útvonala(i) (csak proveniencia). A hiányzó
    rész None."""
    __slots__ = ('cim', 'ide_tartozik', 'nem_tartozik', 'kriterium', 'folerendelt', 'folerendelt_mondatkezdo',
                 'meghatarozas', 'azonossag', 'forras_study')

    def __init__(self, cim, ide_tartozik, nem_tartozik, folerendelt, kriterium=None, folerendelt_mondatkezdo=None,
                 meghatarozas=None, azonossag=None, forras_study=()):
        self.cim, self.ide_tartozik, self.nem_tartozik, self.folerendelt = cim, ide_tartozik, nem_tartozik, folerendelt
        self.kriterium, self.folerendelt_mondatkezdo = kriterium, folerendelt_mondatkezdo
        self.meghatarozas, self.azonossag, self.forras_study = meghatarozas, azonossag, tuple(forras_study)


def b02_motivum(b, motivum):
    """B02 — a motívum sora. A cím és a fölérendelt fogalom a mondatzáró pont nélkül áll az adatban (a pontot a
    sablonmondat teszi ki): ha ponttal végződik, BemenetHiba (a réteg nem vág le a szövegből)."""
    tabla = b._tabla('B02', oszlopok=_MOTIVUM_OSZLOPOK)
    sorok = [r for r in tabla.szotarak() if r['id'] == motivum.kod]
    if len(sorok) != 1:
        raise BemenetHiba('B02: a motívumnak pontosan egy sora legyen (%s: %d)' % (motivum.kod, len(sorok)))
    sor = sorok[0]
    cim, kriterium, fol = sor['cim'].strip(), sor['negativ_kriterium'].strip(), sor['folerendelt_fogalom'].strip()
    if not cim:
        raise BemenetHiba('B02: üres cím (%s)' % motivum.kod)
    for nev, ertek in (('cim', cim), ('folerendelt_fogalom', fol)):
        if ertek.endswith(_MONDATVEG):
            raise BemenetHiba('B02: a `%s` mező ponttal végződik (%s): a pontot a lap mondata teszi ki, az adatban '
                              'ne álljon' % (nev, motivum.kod))
    eleje, elvalaszto, tobbi = kriterium.partition(_NEM_TARTOZIK)
    megh, tipus = sor['meghatarozas'].strip(), sor['azonossag_tipusa'].strip()
    forrasok = [u.strip() for u in sor['forras_study'].split(_FORRAS_ELVALASZTO) if u.strip()]
    return MotivumSor(
        cim=b.kezi('B02', 'cim', cim),
        ide_tartozik=b.kezi('B02', 'negativ_kriterium', eleje.strip()) if eleje.strip() else None,
        nem_tartozik=b.kezi('B02', 'negativ_kriterium', elvalaszto + tobbi) if elvalaszto else None,
        folerendelt=b.kezi('B02', 'folerendelt_fogalom', fol) if fol else None,
        kriterium=b.kezi('B02', 'negativ_kriterium', kriterium) if kriterium else None,
        # a lap elején a mondat a mezővel kezdődik: a mondatkezdő alak adat (a névtábla sora, DT869), sor híján a mező
        folerendelt_mondatkezdo=(folerendelt_mondatkezdo(b, motivum, fol)
                                 or b.kezi('B02', 'folerendelt_fogalom', fol)) if fol else None,
        meghatarozas=b.kezi('B02', 'meghatarozas', megh) if megh else None,
        azonossag=b.kulcs('B02', 'azonossag_tipusa', tipus) if tipus else None,
        forras_study=[b.utvonal_ertek('B02', u) for u in forrasok])


def kriterium_szoveg(b, motivum):
    """A motívum kritériumának teljes szövege (B02, `negativ_kriterium`), a két rész egyben; üres mezőnél None.
    A kritérium kapuja kapja (lapgen.ismetles): látható szöveg ebből az értékből nem lesz."""
    sor = b02_motivum(b, motivum)
    reszek = [resz.ertek for resz in (sor.ide_tartozik, sor.nem_tartozik) if resz is not None]
    return ' '.join(reszek) if reszek else None


_LANC_MAG_RX = re.compile(r'\baz? (\S+) (\d+)[–-](\d+)\.? láncára\b')
_PESAT = 'peshat'


class LancMag:
    """A motívum Pesat-gerince: a könyv és a fejezet-tartomány (a régi `lanc_mag`)."""
    __slots__ = ('konyv', 'elso', 'utolso')

    def __init__(self, konyv, elso, utolso):
        self.konyv, self.elso, self.utolso = konyv, elso, utolso

    def tartalmazza(self, igehely):
        return igehely.konyv == self.konyv and self.elso <= igehely.fejezet <= self.utolso


def lanc_mag(b, motivum, sorok, karoli):
    """A motívum Pesat-gerince (a régi `lanc_mag` szabálya): (1) ha a kritérium megnevezi a láncot („az 1Móz 3–9
    láncára”), az; (2) különben a Pesat-szintű sorok fejezet-tartománya az első Pesat-sor könyvében (a sorok a tábla
    rendjében); (3) Pesat-sor nélkül None. A kritérium kézi szövegéből csak a hivatkozás szerkezete jön (könyv,
    két fejezetszám), a szöveg nem kerül a lapra."""
    m = _LANC_MAG_RX.search(kriterium_szoveg(b, motivum) or '')
    if m:
        return LancMag(m.group(1), int(m.group(2)), int(m.group(3)))
    pesat = [v for s in sorok if any(_PESAT in szint.ertek.lower() for szint in s.pardes_szintek)
             for v in karoli.versek(s.igehely)]
    if not pesat:
        return None
    konyv = pesat[0].konyv
    fejezetek = [v.fejezet for v in pesat if v.konyv == konyv]
    return LancMag(konyv, min(fejezetek), max(fejezetek))


def tagabb_kor_rovid(b, motivum):
    """A tágabb kör rövid alakja kézi prózaként: a mező szövege az első zárójeles kiegészítésig (a 4.12 bevezetője
    ezt idézi; a zárójeles pontosítás csak a lap elején áll). None, ha a mező üres. A réteg a szöveget nem írja át:
    szerkezetileg bont, ahogy a kritérium két részét is."""
    sor = b02_motivum(b, motivum)
    if sor.folerendelt is None:
        return None
    return b.kezi('B02', 'folerendelt_fogalom', sor.folerendelt.ertek.split(_ZAROJEL_ELOTT)[0])


class Rovid:
    """Egy szó rövid jelentése: a magyar szöveg, vagy magyar híján az angol eredeti (fordításra vár). Mindkettő
    hiánya: a szótárnak nincs rövid jelentése a szóra. Az `elavult` jelzi, hogy a magyar fordítás forrása azóta
    megváltozott (T5)."""
    __slots__ = ('magyar', 'angol', 'elavult')

    def __init__(self, magyar, angol, elavult=False):
        self.magyar, self.angol, self.elavult = magyar, angol, elavult


class RovidJelentes:
    """A szavak rövid jelentése egy úton (GK-16): héberül a héber glosszatábla fő sora, görögül a fordítástábla
    rövid glosszája; magyar híján a forrás angol szava áll, kimondott hiányként."""

    def __init__(self, b, heber, forditasok, angol):
        self._b, self._heber, self._forditasok, self._angol = b, heber, forditasok, angol

    def jelentes(self, strong):
        """A szó rövid jelentése (`Rovid`): a magyar szöveg, vagy az angol eredeti, vagy egyik sem."""
        if strong.heber:
            magyar, angol = self._heber.get(strong.kod, ('', ''))
            if magyar:
                return Rovid(self._b.forrasszoveg('B15', 'glossza_hu', magyar, strong), None)
            return Rovid(None, self._b.forrasszoveg('B15', 'glossza_en', angol, strong) if angol else None)
        forditas = self._forditasok.forditas(_SZOTAR_TBESG, strong.kod, strong.kod, _ROVID, _GLOSSZA_MEZO, strong)
        if forditas is not None:
            return Rovid(forditas.szoveg, None, forditas.elavult)
        angol = self._angol.get(strong.kod)
        return Rovid(None, self._b.forrasszoveg('B10', 'rovid_angol', angol, strong) if angol else None)

    def magyar(self, strong):
        """A szó rövid magyar jelentése, vagy None (angol szöveg innen nem jön)."""
        return self.jelentes(strong).magyar


def b15_heber_glosszak(b):
    """B15 — a héber szavak rövid jelentése (a tábla fő sora: `fo` = igen): {Strong: (magyar, angol)}."""
    def betolt():
        tabla = b._tabla('B15', oszlopok=_GLOSSZA_OSZLOPOK)
        s, f, g, e = (tabla.oszlop(o) for o in _GLOSSZA_OSZLOPOK)
        return {sor[s]: (sor[g], sor[e]) for sor in tabla.sorok if sor[f] == _FO}
    return b.egyszer('B15', betolt)


def rovid_jelentes(b):
    """A rövid jelentés szolgáltatása a munkamenethez (egy út a héber és a görög szóra)."""
    return b.egyszer('rovid_jelentes', lambda: RovidJelentes(b, b15_heber_glosszak(b), b14_forditasok(b),
                                                             szavak.b10_lemmak(b)[2]))


def b47_resek(b, motivum):
    """B47 — a motívum kézi résének törzsei a kézi forrásból, a forrásjegyzék szerint: {rés: szöveg} (a jelölők közötti
    szöveg, változatlanul). Csak a kézi forrásból jövő rés számít, és a jegyzékben álló útvonal a motívum kézi forrása
    kell legyen (más útvonal BemenetHiba). A jegyzékben álló, de a forrásban jelölő nélküli rés nem kerül bele. Ez a B47
    egyetlen olvasója; a nyitott kérdések és a kézi rések ebből dolgoznak (GK-01)."""
    jegyzek_ut, forras_ut = b._utvonalak('B47', motivum)
    tabla = b._tabla('B47', utvonal=jegyzek_ut, oszlopok=_RES_OSZLOPOK)
    szoveg, ki = None, {}
    for sor in tabla.szotarak():
        if sor['id'] != motivum.kod or sor['forras'] != _RES_KEZI:
            continue
        if sor['tanulmany'] != forras_ut:
            raise BemenetHiba('B47: a(z) %s rés forrása (%s) nem a motívum kézi forrása (%s)'
                              % (sor['res'], sor['tanulmany'], forras_ut))
        if szoveg is None:
            szoveg = b._szoveg('B47', utvonal=forras_ut)
        torzs = re.search(_RES_RX % (re.escape(sor['res']), re.escape(sor['res'])), szoveg)
        if torzs is not None:
            ki[sor['res']] = torzs.group(1)
    return ki


def nyitott_kerdesek(b, motivum):
    """A motívum kézi forrásának vitatott pontjai és nyitott kérdései (a B47-ből): mindegyikből a félkövér cím és az első
    mondat, szó szerinti részletként (kézi próza), a forrás rendjében: előbb az `ertelmezes` rés „Vitatott pontok”
    pontjai, azután a `modszertan` rés „Nyitott kérdések” listája.

    A rések forrását a forrásjegyzék mondja meg (`b47_resek`). Hiányzó rés vagy pont nem hiba: üres eredmény."""
    resek = b47_resek(b, motivum)
    ki = []
    for res, blokk_rx, tetel_rx in ((_RES_ERTELMEZES, _VITATOTT_RX, _VITATOTT_TETEL_RX),
                                    (_RES_MODSZERTAN, _NYITOTT_RX, _NYITOTT_TETEL_RX)):
        torzs = resek.get(res)
        blokk = blokk_rx.search(torzs) if torzs is not None else None
        for reszlet in (tetel_rx.findall(blokk.group(1)) if blokk else ()):
            ki.append(b.kezi('B47', 'nyitott_kerdes', reszlet.strip()))
    return tuple(ki)


class ResSor:
    """A kézi rés egy sora, szerkezetileg bontva (a szöveg nem változik):

    - próza: `kezi` (Kezi), és ha a sor egy vitatott pont nyitó sora (a „### ⚠️ Vitatott pontok” alatt, félkövér
      címmel), a pont címe `pont` kulcsként (a szakirodalom-sor ehhez a bekezdéshez kötődik);
    - üres sor: minden mező None;
    - kézi forrássor („*Proveniencia: … | forras=… | …*”): `eredeti` (Belso: a sor nyers alakja, csak megjegyzésbe) és
      `bemenetek` (a `forras=` értékeiben nevezett adatfájlok, az első előfordulás rendjében: (jegyzékbeli-e, kulcs)
      párok; a kulcs a jegyzék azonosítója, vagy a generátor által nem olvasott fájlnál a névtábla
      `kezi_forrasfajl` sorának kulcsa, a fájl útvonala);
    - belső sor (a kézi forrás kiadható nézetéből kimaradó, saját soros elem: `<!-- ADAT-NÉZET: … | SZINT: belso -->`,
      `<!-- ADAT-HIV: … -->`, egysoros `【NAPLO …】` blokk; a régi `general.forras_nezet` szabálya): `belso` igaz; a
      lapra nem kerül."""
    __slots__ = ('kezi', 'pont', 'eredeti', 'bemenetek', 'belso')

    def __init__(self, kezi=None, pont=None, eredeti=None, bemenetek=(), belso=False):
        self.kezi, self.pont, self.eredeti, self.bemenetek, self.belso = kezi, pont, eredeti, tuple(bemenetek), belso


class Res:
    """Egy kézi rés törzse soronként (`ResSor`), a jelölők közötti szöveg; a két szélső üres sor nem tartozik
    hozzá."""
    __slots__ = ('res', 'sorok')

    def __init__(self, res, sorok):
        self.res, self.sorok = res, tuple(sorok)


_PROV_SOR_RX = re.compile(r'^\*Proveniencia: (.*)\*$')
_PROV_FORRAS_RX = re.compile(r'forras=([^|]+)')
_PROV_ELVALASZTO_RX = re.compile(r'[+,;]\s*')
_PROV_ZAROJEL_RX = re.compile(r'\s*\(.*$')
_FAJLNEV_RX = re.compile(r'^[\w./-]+\.\w+$')
_BELSO_JELOLO_RX = re.compile(r'^(?:<!-- ADAT-NÉZET: .*\| SZINT: belso -->|<!-- ADAT-HIV: .* -->)$')
_NAPLO_NYITO = ('【NAPLO', '【NAPLÓ')
_VITATOTT_CIM = '### ⚠️ Vitatott pontok'
_ALCIM_ELEJE = '### '
_PONT_RX = re.compile(r'^\*\*(.+?)\.\*\*')


def _jegyzek_utvonalak(b):
    """A jegyzék adatfájljai: {útvonal vagy glob-minta: B-azonosító} (a több útvonalú sor minden útvonala; az `<ID>`
    alakú útvonal nem, az a motívum saját fájlja)."""
    ki = {}
    for b_id in b.jegyzek_azonositok():
        for ut in b.jegyzek_sor(b_id).utvonal.split(';'):
            ut = ut.strip()
            if ut and '<' not in ut:
                ki[ut] = b_id
    return ki


def _naplo_sor(sor):
    """Egysoros, kiegyensúlyozott `【NAPLO …】` blokk (a sor eleje és vége a blokk határa)."""
    if not sor.startswith(_NAPLO_NYITO) or not sor.endswith('】'):
        return False
    melyseg = 0
    for i, c in enumerate(sor):
        melyseg += (c == '【') - (c == '】')
        if melyseg == 0:
            return i == len(sor) - 1
    return False


def _forrassor_bemenetei(b, sor, utvonalak):
    """A kézi forrássor `forras=` értékeiben nevezett adatfájlok jegyzék-azonosítója, az első előfordulás rendjében. A
    réteg szerkezetileg bont (a `+`, `,`, `;` elválasztó és a zárójeles megjegyzés mentén); a nem fájlnév érték
    (kódrészlet, szabad szöveg) nem forrás. A fájlnév vagy a jegyzék útvonala, vagy annak fájlneve; a kódfájl (a
    lekérdezés szkriptje) és az archívumfájl (`konfig.KEZI_FORRAS_KOD_KITERJESZTES`, `KEZI_FORRAS_ARCHIVUM`) nem
    adatforrás. Más, a jegyzékben nem álló fájl BemenetHiba: a
    forrássor nem hivatkozhat a lapon meg nem nevezhető adatra (GK-06, GK-07), kivéve, ha a fájlnak névtábla-sora van
    (`kezi_forrasfajl`: a szerző lekérdezése olvasta, a generátor nem)."""
    nev_szerint = {}
    for ut, b_id in utvonalak.items():
        if '*' not in ut:
            nev_szerint.setdefault(ut.rsplit('/', 1)[-1], set()).add(b_id)
    mintak = [(ut, b_id) for ut, b_id in utvonalak.items() if '*' in ut]
    kezi_fajlok = set(b65_nevtabla(b).nyers_nevek(KEZI_FORRASFAJL_TIPUS))
    ki = []
    for ertek in _PROV_FORRAS_RX.findall(sor):
        for token in _PROV_ELVALASZTO_RX.split(ertek.strip()):
            token = _PROV_ZAROJEL_RX.sub('', token).strip()
            if (not token or not _FAJLNEV_RX.match(token) or token.endswith(konfig.KEZI_FORRAS_KOD_KITERJESZTES)
                    or token.startswith(konfig.KEZI_FORRAS_ARCHIVUM)):
                continue
            if token in utvonalak:
                jeloltek = {utvonalak[token]}
            else:
                jeloltek = nev_szerint.get(token, set()) | {b_id for ut, b_id in mintak if fnmatch.fnmatchcase(token, ut)}
            if not jeloltek and token in kezi_fajlok:
                elem = (False, token)
            elif len(jeloltek) == 1:
                elem = (True, next(iter(jeloltek)))
            else:
                raise BemenetHiba('B47: a kézi forrássor %r fájlja nem egyértelmű jegyzékbeli bemenet (%d találat), és '
                                  'nincs `%s` névtábla-sora' % (token, len(jeloltek), KEZI_FORRASFAJL_TIPUS))
            if elem not in ki:
                ki.append(elem)
    return ki


def kezi_res(b, motivum, res):
    """A motívum egy kézi résének törzse soronként, szerkezetileg bontva (`Res`, a `b47_resek`-ből), vagy None, ha a
    rés a jegyzékben nem a kézi forrásból jön, vagy a forrásban nincs jelölője (opcionális rés: a hívó mondja ki a
    hiányt). Ismeretlen HTML-megjegyzés a rés sorában BemenetHiba (a lap nem kaphat meg nem nevezett jelölőt)."""
    torzs = b47_resek(b, motivum).get(res)
    if torzs is None:
        return None
    reszek = torzs.split('\n')
    while reszek and not reszek[0].strip():
        reszek.pop(0)
    while reszek and not reszek[-1].strip():
        reszek.pop()
    utvonalak, sorok, vitatott = _jegyzek_utvonalak(b), [], False
    for r in reszek:
        if not r.strip():
            sorok.append(ResSor())
            continue
        if r.startswith(_ALCIM_ELEJE):
            vitatott = r.strip() == _VITATOTT_CIM
        prov = _PROV_SOR_RX.match(r)
        if prov:
            sorok.append(ResSor(eredeti=b.belso('B47', 'kezi_forrassor', r),
                                bemenetek=[(j, b.kulcs('B47', 'forras', k)) for j, k in _forrassor_bemenetei(b, r, utvonalak)]))
        elif _BELSO_JELOLO_RX.match(r) or _naplo_sor(r):
            sorok.append(ResSor(belso=True))
        elif r.lstrip().startswith('<!--') or '【' in r:
            raise BemenetHiba('B47: ismeretlen jelölő a(z) %s rés soraiban (%s): %s' % (res, motivum.kod, r[:80]))
        else:
            pont = _PONT_RX.match(r) if vitatott else None
            sorok.append(ResSor(kezi=b.kezi('B47', res, r),
                                pont=b.kulcs('B47', 'vitatott_pont', pont.group(1)) if pont else None))
    return Res(res, sorok)
