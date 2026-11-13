"""lapgen.bemenet.gerinc — a szótári gerinc: a szótárak tagolása, a szakaszcímkék és a szótárak saját példahelyei.

Bemenetek: B16 (a szótári szakaszok címketáblája és a szerkesztői jelentésszám leképezése), B17 (a BDB
szakaszai a zárójel-javítással), B18 (a BDB-szakaszok magyar szövege), B19 (a BDB versenkénti példahelyei),
B21 (a Thayer versenkénti példahelyei), B22 (a teljes angol BDB-szócikk: a példahely szócikkének
azonosításához).

A modul a forrás szerkezetét oldja fel: melyik szakasz melyik szócikké, melyik példahely melyik szakaszé.
A döntés (melyik címke kerül a sorra) a számítás dolga; a megjelenő szöveget (címke, szakaszjel, glossza) ez a
modul adja típusos értékként.

A táblák nyers sorai a réteget nem hagyják el: a számítás típusos értéket kap (`Peldahely`, `ThayerPelda`,
`Tartomany`), amelynek minden szövegmezője burkoló. Szabad szöveget idézetté burkoló általános függvény nincs:
a szakasz jele a szakasz kulcsából itt képződik (`Gerinc.jel`), a példahely forrásbeli alakja a tábla mezője.
"""
import re

import bdb_rovidites
import bdb_tagolas
import szotari_glossza

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.bemenet.nyelv import cimke_cellaalakok
from lapgen.bemenet.szavak import b08_tahot

SZOTAR_BDB = 'BDB'
SZOTAR_THAYER = 'Thayer'
_VERS_RX = re.compile(r'^(.+) (\d+):(\d+)$')
_LAPIT_RX = re.compile(r'(?<=[\s—])(\d{1,2})\.([a-l])\s')
_KULCS_RX = re.compile(r'^\s*([^\s(]+)\s*(?:\((.*)\))?\s*$')
_KEZDET_HOSSZ, _KEZDET_MIN = 40, 15
_UT_FEJ, _UT_CIM, _UT_TAGOLATLAN = 'fej', 'cim', 'tagolatlan'
# A BDB-szócikk fejének eleje: a homográf-szám (római szám, ponttal) és a héber címszó, ahogy a szótárban áll.
_HEBER = '\u0591-\u05F4\uFB1D-\uFB4F'
_CIMSZO_RX = re.compile(r'(?:^|(?<=\s))(?P<szam>(?:I{1,3}|IV|VI{0,3}|IX|X)\.\s)?(?P<szo>\[?[' + _HEBER + r']+\??\]?)'
                        r'(?=[\s,;:.]|$)')
_CIMSZO_ABLAK = 80


class GerincHiba(BemenetHiba):
    """A szótári gerinc adata ellentmond önmagának (pl. a szótár példahelye és a szerkesztői hozzárendelés
    egyike sem esik a másik alá): a futás megáll, választás és kitöltés nélkül."""


def utvonal_vag(utvonal):
    """A záró `/-` levágása: a példahely-tábla (`-/3`) és a szakasztábla (`-/3/-`) alakja így összevethető."""
    while utvonal.endswith('/-'):
        utvonal = utvonal[:-2]
    return utvonal


def szakasz_jel(utvonal):
    """A tagolási jel az útvonalból: `Qal/2/c` → `Qal 2.c`, `-/3/-` → `3`, `Qal/-/-` → `Qal`, `fej` → `fej`."""
    if '/' not in utvonal:
        return utvonal
    reszek = utvonal.split('/')
    felso, tobbi = reszek[0], [r for r in reszek[1:] if r and r != '-']
    szam = '.'.join(tobbi)
    if felso in ('', '-'):
        return szam or utvonal
    return ('%s %s' % (felso, szam)) if szam else felso


def ala_esik(finom, durva):
    f, d = utvonal_vag(finom), utvonal_vag(durva)
    return f == d or f.startswith(d + '/')


def kulcs_ala_esik(finom, durva):
    """Igaz, ha a `finom` szakasz a `durva` alá esik: azonos szócikkben, és az útvonala alá (vagy azonos vele)."""
    return finom[0] == durva[0] and ala_esik(finom[1], durva[1])


def kutatoi_kulcs(jelentes_szam):
    """(kulcs, minősítő): `2.c (tagadva)` → (`2.c`, `tagadva`); a minősítő nem a szó jelentése."""
    m = _KULCS_RX.match(jelentes_szam or '')
    if not m:
        return (jelentes_szam or '').strip(), ''
    return m.group(1), (m.group(2) or '').strip()


_HANYSZOR = {2: 'kétszer', 3: 'háromszor', 4: 'négyszer', 5: 'ötször'}
_MAGANHANGZO = 'aáeéiíoóöőuúüű'


def pontos_jel(jel):
    """A szakaszjel prózai alakja: a puszta szám sorszámnév-pontot kap („4” → „4.”)."""
    return jel + '.' if jel.isdigit() else jel


def szotaras_jel(szotar, jel):
    """A jel a szótár nevével, ha a szótár nem a BDB („Thayer 1”); a BDB jele magában áll."""
    return jel if szotar == SZOTAR_BDB else '%s %s' % (szotar, jel)


def hanyszor(n):
    """Hányszor áll a szó a versben, a belső leírás szavával."""
    return _HANYSZOR.get(n, '%d alkalommal' % n)


def nevelo(szo):
    """A határozott névelő a belső leírásban: számnál a kiolvasott alak szerint (az 1., az 5.; a 3.)."""
    szam = re.match(r'\d+', szo)
    if szam:
        n = int(szam.group(0))
        return 'az' if n == 1 or str(n)[0] == '5' or 1000 <= n < 2000 else 'a'
    return 'az' if szo[:1].lower() in _MAGANHANGZO else 'a'


def forras_javitott(pelda_sor):
    """Igaz, ha a példahely-sor versét a forrás sajtóhibája miatt kézi javítás adja."""
    return 'forras_javitas' in (pelda_sor.get('okkod') or '').split(',')


def lapit(szoveg):
    """A szócikk szövege abban az alakban, amelyre a példahelyek helye (`poz`) vonatkozik: sortörés helyett
    szóköz, „1.a” → „1. a.”."""
    return _LAPIT_RX.sub(r'\1. \2. ', (szoveg or '').replace('\n', ' ').strip())


def _fej_glossza(hu):
    """A tagolatlan szócikk meghatározása a fej magyar szövegéből: az első gondolatjel előtti utolsó (nem
    versszámbeli) kettőspont utáni rész."""
    s = hu or ''
    vege = re.search(r'\s[—–]\s', s)
    s = s[:vege.start()] if vege else s[:200]
    kp = [m for m in re.finditer(':', s)
          if not (m.start() and s[m.start() - 1].isdigit() and s[m.end():m.end() + 1].isdigit())]
    return szotari_glossza.olvasoi_glossza('', '', s[kp[-1].end():]) if kp else None


def _cella_alak_egyezik(cimke, alak):
    """Igaz, ha az `alak` a címke cellakezdő alakja: nagy kezdőbetűvel, a kezdő névelővel vagy anélkül."""
    kisbetus = alak[:1].lower() + alak[1:]
    nevelotlen = re.sub(r'^(?:a|az)\s+', '', cimke)
    return alak[:1].isupper() and kisbetus in (cimke, nevelotlen)


class Tartomany:
    """A BDB a verset csak egy verstartomány belsejében idézi: a szakasz kulcsa, a tartomány kezdő verse
    (igehely; a könyvnév a normalizáló táblán ellenőrizve) és utolsó versszáma, a forrás alakja. A szövegmezők
    burkolók (belső szöveg, illetve a forrás idézhető alakja)."""
    __slots__ = ('kulcs', 'kezdo_vers', 'veg', 'nyers', 'folytatas', 'sorszam')

    def __init__(self, kulcs, kezdo_vers, veg, nyers, folytatas, sorszam):
        self.kulcs, self.kezdo_vers, self.veg = kulcs, kezdo_vers, veg
        self.nyers, self.folytatas, self.sorszam = nyers, folytatas, sorszam


class Peldahely:
    """A BDB egy saját példahelye egy versre. `kulcs`: a példahely szakaszkulcsa, vagy None, ha nem
    azonosítható, melyik szócikk idézi a helyet (az `ok` ilyenkor a belső magyarázat); `idezett`: a hely a
    forrás saját alakjában (idézhető); `sorszam`, `karoli_vers`: belső mezők (csak megjegyzésbe kerülhetnek)."""
    __slots__ = ('kulcs', 'sorszam', 'idezett', 'karoli_vers', 'forras_javitott', 'ok')

    def __init__(self, kulcs, sorszam, idezett, karoli_vers, forras_javitott, ok):
        self.kulcs, self.sorszam, self.idezett = kulcs, sorszam, idezett
        self.karoli_vers, self.forras_javitott, self.ok = karoli_vers, forras_javitott, ok


class ThayerPelda:
    """A Thayer egy saját példahelye: a szakasz jele belső kulcsként, a tábla sorszáma, és ha a jel puszta szám,
    a jelentés száma (a lapon ez a szám állhat; a belső kulcs nem)."""
    __slots__ = ('jel', 'sorszam', 'jelentesszam')

    def __init__(self, jel, sorszam, jelentesszam):
        self.jel, self.sorszam, self.jelentesszam = jel, sorszam, jelentesszam


class Szocikk:
    """Egy szócikk megnevezése, ha a szakasz jele a szó több szócikkében is áll: a szótár (belső kulcs; olvasói
    neve a névtáblában), a szótár saját címszava a homográf-számával, szó szerint (`cimszo`; None, ha a szótár
    jelölése a szócikket nem különbözteti meg), és a szócikk sorszáma a szó szócikkei között, a szótár rendjében."""
    __slots__ = ('szotar', 'cimszo', 'sorszam')

    def __init__(self, szotar, cimszo, sorszam):
        self.szotar, self.cimszo, self.sorszam = szotar, cimszo, sorszam


class Gerinc:
    """A szótári gerinc indexei egy munkamenetben. A `_` kezdetű mezők a nyers táblasorok."""

    def __init__(self, b, cimke, bdb_sz, bdb_hu, bdb_vj, th_vj, bdb_en, zarojel, tahot, cella_alakok, konyvek):
        self._b, self._cimke, self._bdb_sz, self._bdb_hu = b, cimke, bdb_sz, bdb_hu
        self._konyvek = konyvek
        self._cella_alakok = cella_alakok
        for kulcs, alak in cella_alakok.items():
            nyers = (cimke.get(kulcs) or {}).get('cimke_hu') or ''
            if not nyers or not _cella_alak_egyezik(nyers, alak.ertek):
                raise GerincHiba('B65: a(z) %s cellakezdő alakja („%s”) nem a címke („%s”) cellakezdő alakja: a kettő '
                                 'csak a kezdő névelőben és a kezdőbetűben térhet el' % (kulcs, alak.ertek, nyers))
        self._bdb_vj, self._th_vj, self._bdb_en, self._zarojel, self._tahot = bdb_vj, th_vj, bdb_en, zarojel, tahot
        self._kezdet, self._poz_ok, self._vj_strong, self._fa = {}, {}, None, {}

    # --- a szócikkek és a szakaszok ------------------------------------------------------------------------

    def bdb_szocikkek(self, strong):
        """A Strong BDB-szócikkei a szakasztábla (a BDB) sorrendjében."""
        ki = []
        for r in sorted(self._bdb_sz.get(strong, []), key=lambda x: int(x['sorszam'])):
            if r['bdb_id'] not in ki:
                ki.append(r['bdb_id'])
        return ki

    def _utvonal_szocikkei(self, strong, utvonal):
        vag = utvonal_vag(utvonal)
        return {r['bdb_id'] for r in self._bdb_sz.get(strong, []) if utvonal_vag(r['utvonal']) == vag}

    def _tobb_szocikkben(self, szotar, strong, kulcs):
        """Igaz, ha a szakasz útvonala a Strong több BDB-szócikkében is áll (a jel magában nem egyértelmű)."""
        return szotar == SZOTAR_BDB and bool(kulcs[0]) and len(self._utvonal_szocikkei(strong, kulcs[1])) > 1

    def kulcs_jel(self, szotar, strong, kulcs):
        """A szakasz belső jele (`1.a`): rendezéshez, kereséshez és a megjegyzésbe kerülő belső leíráshoz. Ha az
        útvonal a Strong több BDB-szócikkében is áll, a szócikk belső azonosítójával; a lapra ez az alak nem
        kerül (a látható jel: `jel`, a szócikk megnevezése: `jel_szocikke`)."""
        jel = szakasz_jel(kulcs[1])
        if self._tobb_szocikkben(szotar, strong, kulcs):
            return '%s %s' % (kulcs[0], jel)
        return jel

    def _cimszavak(self, strong):
        """A Strong BDB-szócikkeinek címszava a szótár rendjében: [(szócikk, a fej elején álló megnevezés vagy
        None, a címszó, van-e homográf-szám)]. A megnevezés a forrás összefüggő részlete (homográf-szám és
        címszó), változtatás nélkül."""
        fejek = {}
        for r in self._bdb_sz.get(strong, []):
            if r['utvonal'] == _UT_FEJ:
                fejek.setdefault(r['bdb_id'], r.get('szoveg') or '')
        ki = []
        for bdb_id in self.bdb_szocikkek(strong):
            m = _CIMSZO_RX.search(fejek.get(bdb_id, '')[:_CIMSZO_ABLAK])
            ki.append((bdb_id, m.group(0), m.group('szo'), bool(m.group('szam'))) if m
                      else (bdb_id, None, None, False))
        return ki

    def jel_szocikke(self, szotar, strong, kulcs):
        """A szócikk megnevezése a szakasz jele mellé, ha a jel a szó több szócikkében is áll; különben None.
        A megnevezés a szótár saját címszava a homográf-számával, szó szerinti idézetként; ha a szótár jelölése a
        szócikket nem különbözteti meg (nincs címszó; a címszó másik szócikké is, és nincs homográf-szám; két
        szócikk megnevezése azonos), a `cimszo` None, és a szócikket a sorszáma nevezi meg. Belső azonosító a
        megnevezésben nem áll."""
        if not self._tobb_szocikkben(szotar, strong, kulcs):
            return None
        cimszavak = self._cimszavak(strong)
        sorszam = [c[0] for c in cimszavak].index(kulcs[0]) + 1
        _id, nev, szo, szamos = cimszavak[sorszam - 1]
        egyedi_nev = nev is not None and sum(1 for c in cimszavak if c[1] == nev) == 1
        egyedi_szo = szo is not None and sum(1 for c in cimszavak if c[2] == szo) == 1
        cimszo = (self._b.forrasszoveg('B17', 'cimszo', nev, strong)
                  if egyedi_nev and (szamos or egyedi_szo) else None)
        return Szocikk(self._b.kulcs('B17', 'szotar', szotar), cimszo, sorszam)

    def _sor_kezdetek(self, strong):
        if strong not in self._kezdet:
            s = lapit(self._bdb_en.get(strong, ''))
            ki, kurzor = [], 0
            for r in sorted(self._bdb_sz.get(strong, []), key=lambda x: int(x['sorszam'])):
                t = lapit(r.get('szoveg') or '')[:_KEZDET_HOSSZ]
                i = s.find(t, kurzor) if s and len(t) >= _KEZDET_MIN else -1
                ki.append((r['bdb_id'], i if i >= 0 else None))
                if i >= 0:
                    kurzor = i + 1
            self._kezdet[strong] = ki
        return self._kezdet[strong]

    def _poz_szocikkei(self, strong, poz):
        sorok = self._sor_kezdetek(strong)
        elotte = [k for k, (_b, i) in enumerate(sorok) if i is not None and i <= poz]
        utana = [k for k, (_b, i) in enumerate(sorok) if i is not None and i > poz]
        tol = elotte[-1] if elotte else 0
        ig = utana[0] if utana else len(sorok)
        return {sorok[k][0] for k in range(tol, ig)}

    def _vers_ut_szocikkei(self, strong, ut):
        sorok = self._bdb_sz.get(strong, [])
        if ut == _UT_FEJ:
            return {x['bdb_id'] for x in sorok if x['utvonal'] == _UT_FEJ}
        if ut == _UT_TAGOLATLAN:
            return {b for b in self.bdb_szocikkek(strong)
                    if all(x['utvonal'] in (_UT_CIM, _UT_FEJ) for x in sorok if x['bdb_id'] == b)}
        return self._utvonal_szocikkei(strong, ut)

    def _poz_megbizhato(self, strong):
        if self._vj_strong is None:
            idx = {}
            for (st, _v), sorok in self._bdb_vj.items():
                idx.setdefault(st, []).append(sorok)
            self._vj_strong = idx
        if strong not in self._poz_ok:
            ok = True
            for sorok in self._vj_strong.get(strong, []):
                for r in sorok:
                    if r['utvonal'] in (_UT_FEJ, _UT_TAGOLATLAN):
                        continue
                    ut_j = self._utvonal_szocikkei(strong, r['utvonal'])
                    try:
                        if len(ut_j) == 1 and not ut_j <= self._poz_szocikkei(strong, int(r.get('poz'))):
                            ok = False
                    except (TypeError, ValueError):
                        pass
            self._poz_ok[strong] = ok
        return self._poz_ok[strong]

    def pelda_szocikk(self, strong, r):
        """A példahely-sor szócikke: (bdb_id vagy None, a nem azonosíthatóság oka belső szövegként)."""
        ids = self.bdb_szocikkek(strong)
        if len(ids) <= 1:
            return (ids[0] if ids else None), ''
        ut = r['utvonal']
        ut_j = self._vers_ut_szocikkei(strong, ut)
        if len(ut_j) == 1:
            return next(iter(ut_j)), ''
        if not self._poz_megbizhato(strong):
            return None, ('a %s útvonal a %s szócikkei közül %s; a hivatkozás helye (`poz`) itt nem dönt, mert a 2.29 '
                          'és a 2.30 szócikkhatára a Strongban máshol eltér'
                          % (ut, strong, ('ezekben áll: ' + ', '.join(b for b in ids if b in ut_j)) if ut_j
                             else 'egyikben sem áll'))
        try:
            p_j = self._poz_szocikkei(strong, int(r.get('poz')))
        except (TypeError, ValueError):
            p_j = set(ids)
        j = (ut_j & p_j) if ut_j else p_j
        if len(j) == 1:
            return next(iter(j)), ''
        return None, ('a %s útvonal a %s szócikkében áll (%s), a hivatkozás helye (`poz` %s) szerint: %s'
                      % (ut, strong, ', '.join(b for b in ids if b in ut_j) or '—', r.get('poz'),
                         ', '.join(b for b in ids if b in p_j) or '—'))

    def kutatoi_szakasz(self, szotar, strong, kulcs):
        """A szerkesztői jelentésszám leképezése a szótár szakaszára: (bdb_id, szakasz) vagy None."""
        talalat = [(k[2], k[3]) for k, r in self._cimke.items()
                   if k[0] == szotar and k[1] == strong and r['lexikon_jelentes_szam'] == kulcs]
        if len(talalat) > 1:
            raise GerincHiba('B16: a(z) %s %s %s jelentésszám több szakaszra mutat: %s'
                             % (szotar, strong, kulcs, talalat))
        return talalat[0] if talalat else None

    def bdb_peldak(self, strong, vers):
        """A BDB saját példahelyei a versre, a fej és a cím nélkül: `Peldahely` értékek."""
        ki = []
        for r in self._bdb_vj.get((strong, vers), []):
            if r['utvonal'] in (_UT_FEJ, _UT_CIM):
                continue
            bdb_id, ok = self.pelda_szocikk(strong, r)
            ki.append(Peldahely(
                kulcs=self.pelda_kulcs(strong, bdb_id, r) if bdb_id is not None else None,
                sorszam=self._b.belso('B19', 'sorszam', r['sorszam']),
                idezett=self._b.forrasszoveg('B19', 'nyers', r['nyers'], vers),
                karoli_vers=self._b.belso('B19', 'karoli_vers', r['karoli_vers']),
                forras_javitott=forras_javitott(r),
                ok=self._b.belso('B19', 'szocikk_azonositas', ok)))
        return ki

    def _sor_utvonal(self, strong, bdb_id, vag_ut):
        for r in self._bdb_sz.get(strong, []):
            if r['bdb_id'] == bdb_id and utvonal_vag(r['utvonal']) == vag_ut:
                return r['utvonal']
        return None

    def pelda_kulcs(self, strong, bdb_id, r):
        """A példahely szakaszkulcsa: (bdb_id, a szakasztábla teljes útvonala)."""
        return (bdb_id, self._sor_utvonal(strong, bdb_id, utvonal_vag(r['utvonal'])) or r['utvonal'])

    def tartomanyban(self, strong, vers):
        """Ha a BDB a verset csak egy verstartomány belsejében idézi („1Kin 18:24-25”: a 18:25), a hely nem
        példahely, de a jegyzet ezt kimondja. Visszaad: a `Tartomany` értékek listája."""
        m = _VERS_RX.match(vers)
        if not m:
            return []
        konyv, c, v = m.group(1), int(m.group(2)), int(m.group(3))
        csoport = {}
        for (st, kv), sorok in self._bdb_vj.items():
            mk = _VERS_RX.match(kv) if st == strong else None
            if not mk or mk.group(1) != konyv or int(mk.group(2)) != c or int(mk.group(3)) >= v:
                continue
            for r in sorok:
                if r.get('vers_feloldas') == 'azonos' and r['utvonal'] not in (_UT_FEJ, _UT_CIM):
                    b, _ok = self.pelda_szocikk(strong, r)
                    if b is not None:
                        csoport.setdefault((b, utvonal_vag(r['utvonal']), r['nyers']), []).append(r)
        ki = []
        for (b, vag, nyers), sorok in sorted(csoport.items()):
            szoveg = ' '.join(' '.join(x for x in (sz.get('jel'), sz.get('szoveg')) if x)
                              for sz in self._bdb_sz.get(strong, [])
                              if sz['bdb_id'] == b and utvonal_vag(sz['utvonal']) == vag)
            elofordulas = list(re.finditer(r'(?<![\w:])' + re.escape(nyers) + r'(?![\d])', szoveg))
            sorok = sorted(sorok, key=lambda r: int(r['sorszam']))
            if len(elofordulas) != len(sorok):
                continue
            for r, e in zip(sorok, elofordulas):
                t = re.match(r'\s*[-–]\s*(\d+)(?![\d:])', szoveg[e.end():])
                if t and int(_VERS_RX.match(r['karoli_vers']).group(3)) < v <= int(t.group(1)):
                    kezd, mt = _VERS_RX.match(r['karoli_vers']), _VERS_RX.match(r['mt_vers'] or r['karoli_vers'])
                    veg = int(t.group(1)) + int(kezd.group(3)) - int(mt.group(3))
                    ki.append(Tartomany(
                        (b, r['utvonal']), self._konyvek.igehely(r['karoli_vers']), veg,
                        self._b.forrasszoveg('B19', 'nyers', nyers, vers),
                        self._b.belso('B17', 'tartomany_folytatas', t.group(0).strip()),
                        self._b.belso('B19', 'sorszam', r['sorszam'])))
        return ki

    def thayer_peldak(self, strong, versek):
        """A Thayer saját példahelyei a versekre: `ThayerPelda` értékek."""
        ki = []
        for v in versek:
            for r in self._th_vj.get((strong, v), []):
                jel = szakasz_jel(r['utvonal'])
                ki.append(ThayerPelda(self._b.kulcs('B21', 'utvonal', jel),
                                      self._b.belso('B21', 'sorszam', r['sorszam']),
                                      int(jel) if jel.isdigit() else None))
        return ki

    def token_szam(self, vers, strong):
        return self._tahot.token_szam(vers, strong)

    # --- megjelenő szöveg: címke, jel, glossza ---------------------------------------------------------------

    def cimke(self, szotar, strong, kulcs):
        """A szakasz jóváhagyott címkéje kézi szövegként, vagy None."""
        sor = self._cimke.get((szotar, strong) + kulcs)
        nyers = (sor or {}).get('cimke_hu') or ''
        return self._b.kezi('B16', 'cimke_hu', nyers) if nyers else None

    def cimke_cella(self, szotar, strong, kulcs):
        """A szakasz címkéje cellakezdő alakban, kézi szövegként: a névtábla `cimke_cella` sora, híján maga a
        címke (a címkét a generátor nem írja át)."""
        alak = self._cella_alakok.get((szotar, strong) + kulcs)
        return alak if alak is not None else self.cimke(szotar, strong, kulcs)

    def jel(self, szotar, strong, kulcs, prozai=False):
        """A szakasz jele idézhető forrásszövegként (a szótár saját tagolása): a cella alakjában („1.a”,
        „Qal 2.c”), `prozai` alakban a puszta szám sorszámnév-ponttal („4.”). A jel a szakasz kulcsából itt, a
        bemeneti rétegben képződik: a számítás kulcsot ad át, szöveget nem. A jel csak a szócikken belüli
        tagolást adja; ha több szócikkben is áll, a szócikket a `jel_szocikke` nevezi meg."""
        jel = szakasz_jel(kulcs[1])
        return self._b.forrasszoveg('B17' if szotar == SZOTAR_BDB else 'B16', 'szakasz_jel',
                                    pontos_jel(jel) if prozai else jel, strong)

    def _szocikk_fa(self, strong):
        if strong not in self._fa:
            hu = {r['sorszam']: self._bdb_hu[(strong, r['sorszam'])] for r in self._bdb_sz.get(strong, [])
                  if (strong, r['sorszam']) in self._bdb_hu}
            self._fa[strong] = bdb_tagolas.szocikkek(
                self._bdb_sz.get(strong, []), hu, szakasz_jel,
                lambda t: bdb_rovidites.zarojel_javit(t, strong, self._zarojel))[0]
        return self._fa[strong]

    def szakasz_glossza(self, strong, jel):
        """A BDB-szakasz olvasói glosszája a jele szerint (a kártya szabályával); None, ha nincs."""
        for sz in self._szocikk_fa(strong):
            for k, j, hu, _angol, _kat in sz['szakaszok']:
                if self.kulcs_jel(SZOTAR_BDB, strong, k) == jel:
                    cimke = (self._cimke.get((SZOTAR_BDB, strong) + k) or {}).get('cimke_hu') or ''
                    glossza = szotari_glossza.olvasoi_glossza(j, cimke, hu)
                    return self._b.forrasszoveg('B18', 'szoveg_hu', glossza, strong) if glossza else None
        return None

    def tagolatlan(self, strong):
        """(tagolatlan-e a Strong egyetlen BDB-szócikke, a fej glosszája vagy None)."""
        fa = self._szocikk_fa(strong)
        if len(fa) != 1 or fa[0]['szakaszok']:
            return False, None
        fej = fa[0]['fej']
        glossza = _fej_glossza(fej[2] if fej and fej[2] else '')
        return True, (self._b.forrasszoveg('B18', 'szoveg_hu', glossza, strong) if glossza else None)


def _sorok(b, b_id, oszlopok, utvonal=None):
    return b._tabla(b_id, utvonal=utvonal, oszlopok=oszlopok).szotarak()


def b16_szakasz_cimkek(b):
    """B16 — a szótári szakaszok címkéi és a szerkesztői jelentésszám leképezése; kulcs: szótár + Strong +
    szócikk + szakasz."""
    return {(r['szotar'], r['strong'], r['bdb_id'] or '', r['szakasz']): r
            for r in _sorok(b, 'B16', ('szotar', 'strong', 'bdb_id', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu'))}


def b17_bdb_szakaszok(b):
    """B17 — a BDB szakaszai Strong-számonként, és a forrás zárójel-javításai (a megjelenítés előtt
    kötelezően alkalmazva): (szakaszok, javítások)."""
    szakasz_ut, javitas_ut = b._utvonalak('B17')
    szakaszok = {}
    for r in _sorok(b, 'B17', ('strong', 'bdb_id', 'sorszam', 'utvonal', 'jel', 'szoveg'), szakasz_ut):
        szakaszok.setdefault(r['strong'], []).append(r)
    b._szoveg('B17', utvonal=javitas_ut)   # az olvasás naplózása; a javítótáblát a közös javító modul értelmezi
    return szakaszok, bdb_rovidites.zarojel_javitasok(b._teljes_utvonal(javitas_ut))


def b18_bdb_szakasz_hu(b):
    """B18 — a BDB-szakaszok magyar szövege; kulcs: Strong + sorszám."""
    return {(r['strong'], r['sorszam']): r
            for r in _sorok(b, 'B18', ('strong', 'sorszam', 'kategoria', 'szoveg_hu'))}


def b19_bdb_vers_jelentes(b):
    """B19 — a BDB saját példahelyei versenként (a kiszűrt és a Károli-vers nélküli sorok nélkül)."""
    ki = {}
    oszlopok = ('strong', 'sorszam', 'poz', 'nyers', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'utvonal', 'okkod',
                'szurt')
    for r in _sorok(b, 'B19', oszlopok):
        if r['szurt'] == '1' or not r['karoli_vers']:
            continue
        ki.setdefault((r['strong'], r['karoli_vers']), []).append(r)
    return ki


def b21_thayer_vers_jelentes(b):
    """B21 — a Thayer saját példahelyei versenként."""
    ki = {}
    for r in _sorok(b, 'B21', ('strong', 'sorszam', 'karoli_vers', 'utvonal')):
        if r['karoli_vers']:
            ki.setdefault((r['strong'], r['karoli_vers']), []).append(r)
    return ki


def b22_bdb_teljes(b):
    """B22 — a teljes angol BDB-szócikk Strong-számonként (a példahely helyének koordinátái erre vonatkoznak)."""
    tabla = b._tabla('B22', oszlopok=('Strong_padded', 'Teljes_szocikk'))
    s, t = tabla.oszlop('Strong_padded'), tabla.oszlop('Teljes_szocikk')
    return {sor[s]: sor[t] for sor in tabla.sorok}


def gerinc(b):
    """A szótári gerinc a munkamenethez."""
    def epit():
        szakaszok, zarojel = b17_bdb_szakaszok(b)
        return Gerinc(b, b16_szakasz_cimkek(b), szakaszok, b18_bdb_szakasz_hu(b), b19_bdb_vers_jelentes(b),
                      b21_thayer_vers_jelentes(b), b22_bdb_teljes(b), zarojel, b08_tahot(b),
                      cimke_cellaalakok(b), b63_konyvek(b))
    return b.egyszer('gerinc', epit)
