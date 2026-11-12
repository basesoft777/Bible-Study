"""A bibliaválasztó (F210): a választható Bibliák regisztere és a fejezetlap szövegoszlopának modellje a nem Károli 1908-as
szövegekhez. Flask és SQL nélkül: az SQL a `lekerdezesek.py`-ban áll.

A Károli 1908 az alapnézet (döntés, 2026-10-22): a választás a `?biblia=<kód>` paraméterben él, a Károli kódja nem kerül a
címbe, így a meglévő Károli-útvonalak változatlanok. Két számozás van:
- `karoli`: a szöveg az adatbázisban a Károli-vers kulcsán áll (modern Károli, TAHOT, TAGNT, BSB; a KJV és a Septuaginta a
  meglévő leképező táblával), a lap a Károli-fejezetet mutatja, a versszám a Károlié;
- `forras`: a Targum és a Vulgata a forrás SAJÁT számozását hordozza (`konkordancia/VISSZHANG_README.md` 1.); a lap a forrás
  fejezetét és versszámát mutatja, és kimondja, hogy ez eltérhet a Károlitól. Versegyezést nem állítunk.
A Strong-jelölt szövegben a szó a szópanelt nyitja (a meglévő `?szo=` útvonal, a Károli-vers kontextusával); a Strong nélküli
szöveg (Targum, Vulgata) versenként olvasható.
"""
import re
import threading
from dataclasses import dataclass

import lekerdezesek as q

ALAP = 'karoli'
CSOPORTOK = (('magyar', 'Magyar'), ('eredeti', 'Eredeti nyelv'), ('angol', 'Angol'), ('okori', 'Ókori fordítás'))


@dataclass(frozen=True)
class Biblia:
    kod: str
    nev: str              # a választó gombja
    morzsa: str           # a fejléc morzsája („Károli 1908 · 1Móz 1”)
    csoport: str
    alcim: str            # a gomb kis sora (a mockup szerint)
    tabla: str            # az elérhetőség forrása (lekerdezesek.biblia_fejezetek_*)
    szamozas: str         # 'karoli' | 'forras'
    strong: bool          # szószintű Strong-jelölés (a KJV-é kiadásfüggő: a `kjv` tábla kizárható)
    lang: str
    irany: str            # 'ltr' | 'rtl'
    licenc_tablak: tuple  # a forrássor táblái (tabla_licenc)
    leiras: str           # a lap tetején álló jegy


BIBLIAK = (
    Biblia('karoli', 'Károli 1908', 'Károli 1908', 'magyar', 'alapnézet · Strong', 'vers', 'karoli', True, 'hu', 'ltr', ('vers',), ''),
    Biblia('modern', 'Modernizált Károli', 'Modernizált Károli', 'magyar', 'Strong', 'szoveg_modern', 'karoli', True, 'hu', 'ltr',
           ('szoveg_modern', 'token_modern', 'token_par'),
           'A Károli 1908 helyesírásban és igealakokban modernizált szövege (gépi szabálykészlet, #96); a szavak Strong-párja a Károli 1908-é.'),
    Biblia('tahot', 'Héber Ószövetség', 'Héber ÓSZ', 'eredeti', 'TAHOT · Strong', 'token_eredeti:H', 'karoli', True, 'he', 'rtl',
           ('token_eredeti',),
           'A héber (és arámi) maszoréta szöveg a TAHOT szerint, a Károli-versek kulcsán (a TAHOT kulcsa a Károli-vers). Az előtagok és a szuffixumok a TAHOT-ban külön tokenek; a nyelvtani elemre nem lehet koppintani.'),
    Biblia('tagnt', 'Görög Újszövetség', 'Görög ÚSZ', 'eredeti', 'TAGNT · Strong', 'token_eredeti:G', 'karoli', True, 'el', 'ltr',
           ('token_eredeti',), 'A görög Újszövetség a TAGNT szerint, a Károli-versek kulcsán.'),
    Biblia('lxx', 'Septuaginta', 'Septuaginta', 'eredeti', 'görög Ószövetség · Strong', 'lxx_token', 'karoli', True, 'el', 'ltr',
           ('lxx_token', 'lxx_versszam'),
           'A Septuaginta (lxx-morph) a Károli-versekhez rendelve, a meglévő versmegfeleltetés szerint; ahol az LXX számozása eltér, a vers elején áll. A Károli-vers nélküli LXX-szakasz itt nem jelenik meg.'),
    Biblia('kjv', 'KJV', 'KJV', 'angol', 'Strong', 'szoveg_kjv', 'karoli', True, 'en', 'ltr', ('szoveg_kjv', 'kjv'),
           'A King James Version (1769) szövege, a Károli-versek kulcsán (a versmegfeleltetés szerint).'),
    Biblia('bsb', 'BSB', 'BSB', 'angol', 'csak Ószövetség · Strong', 'bsb', 'karoli', True, 'en', 'ltr', ('bsb',),
           'A Berean Standard Bible ószövetségi szövege a Strong-táblából (szavanként, írásjel nélkül), a Károli-versek kulcsán; a forrásfájlból (BSB_Strongs.tsv) hiányzik a 2Sám, az Ezsd és a Dán.'),
    Biblia('targum', 'Targum', 'Targum', 'okori', 'arámi · csak Ószövetség · versenként', 'szoveg_targum', 'forras', False, 'arc', 'rtl',
           ('szoveg_targum',),
           'Targum Onkelosz (Tóra) és Targum Jonatán (Próféták), arámi, a Sefaria közkincs változata.'),
    Biblia('vulgata', 'Vulgata', 'Vulgata', 'okori', 'latin · versenként', 'szoveg_vulgata', 'forras', False, 'la', 'ltr',
           ('szoveg_vulgata',), 'A Vulgata Clementina (1598), latin, az eBible közkincs változata; a deuterokanonikus könyvek nélkül.'),
)
BIBLIA = {b.kod: b for b in BIBLIAK}
KODOK = tuple(BIBLIA)


def kod_kerese(ertek):
    """A `?biblia=` értéke: ismert kód, különben az alap. A Károli kódja is az alap (a címben nem áll)."""
    return ertek if ertek in BIBLIA else ALAP


def parameter(kod):
    """A cím lekérdezés-része a választott Bibliához ('' a Károlinál)."""
    return '' if kod == ALAP else 'biblia=' + kod


class Tar:
    """A Bibliák elérhetősége (könyvenként a fejezetek), lustán és egyszer számolva (szálbiztosan)."""

    def __init__(self, db, kozos):
        self.db, self.kozos = db, kozos
        self._fej = {ALAP: {kk: [f for f, _ in fl] for kk, fl in kozos.fejezet_szam.items()}}
        self._zar = threading.Lock()

    def van(self, b):
        """A Biblia táblái megvannak-e az adatbázisban (és a kiadás nem zárja ki őket)."""
        if b.kod == ALAP:
            return True
        t = b.tabla.split(':')[0]
        return t in self.kozos.licenc and t not in self.db.kizart

    def strong_is(self, b):
        if b.kod == 'kjv':
            return 'kjv' in self.kozos.licenc and 'kjv' not in self.db.kizart
        return b.strong

    def fejezetek(self, kod):
        """{kk: [fejezet]} a Biblia elérhető fejezetei ({} ha nincs az adatbázisban)."""
        if kod in self._fej:
            return self._fej[kod]
        b = BIBLIA[kod]
        with self._zar:
            if kod not in self._fej:
                if not self.van(b):
                    self._fej[kod] = {}
                elif b.szamozas == 'forras':
                    self._fej[kod] = q.biblia_fejezetek_forras(self.db.kapcsolat(), b.tabla)
                else:
                    self._fej[kod] = q.biblia_fejezetek_karoli_kulcs(self.db.kapcsolat(), b.tabla)
        return self._fej[kod]

    def cel(self, kod, kk, fej):
        """A választó gombjának célja: ugyanaz a könyv és fejezet, ha a Bibliában megvan; különben a könyv első fejezete; különben
        a Biblia első könyvének első fejezete. (slug, fejezet) vagy None."""
        fl = self.fejezetek(kod)
        if not fl:
            return None
        if kk in fl:
            return self.kozos.slug[kk], (fej if fej in fl[kk] else fl[kk][0])
        for kk2, _, _, _ in self.kozos.konyvek:
            if kk2 in fl:
                return self.kozos.slug[kk2], fl[kk2][0]
        return None


# ---------------------------------------------------------------------------------------------------------------------
# a szövegoszlop modellje (a sablon `szavak` makrója: {kiir, szokoz, fo}; a vers: {vers, ig, link, szavak, szoveg, jel})
# ---------------------------------------------------------------------------------------------------------------------
def _fo_strong(lanc, nyelvtani):
    """Az első nem nyelvtani Strong-szám a láncból (`H9003/H7225`, `H1234+H5678`), normalizálva; különben None."""
    for s in re.split(r'[/+,; ]+', lanc or ''):
        n = q.hnorm(s)
        if n and n not in nyelvtani:
            return n
    return None


def _tahot_szavak(tokenek, nyelvtani):
    """A TAHOT tokenjei olvasható szöveggé: az előtag (H9001–H9010) a következő szóhoz, a szuffixum és a hangsúlyos/irányjelölő
    végződés (H9011–H9049) az előzőhöz tapad, a makkef (H9014, ־) mindkét oldalon."""
    ki = []
    for i, (_, alak, lanc) in enumerate(tokenek):
        elso = (lanc or '').split('/')[0]
        n = q.hnorm(elso) or ''
        szam = int(n[1:5]) if n[:1] == 'H' and n[1:5].isdigit() else 0
        elotag = 9001 <= szam <= 9010
        if ki and (9011 <= szam <= 9049 or (alak.startswith('־'))):
            ki[-1]['szokoz'] = False
        ki.append({'kiir': alak, 'szokoz': not (elotag or alak.endswith('־') or szam == 9014), 'fo': _fo_strong(lanc, nyelvtani)})
    return ki


def _kjv_szavak(szoveg, cimkek, nyelvtani):
    """A KJV versszövegébe illeszti a Strong-címkés szavakat (sorrendben, szóhatáron); a nem illeszthető címke kimarad."""
    ki, pos = [], 0
    for szo, st in cimkek:
        fo = q.hnorm(st)
        if not szo or not fo or fo in nyelvtani:
            continue
        m = re.compile(r'(?<![A-Za-z])' + re.escape(szo) + r'(?![A-Za-z])').search(szoveg, pos)
        if not m:
            continue
        if m.start() > pos:
            ki.append({'kiir': szoveg[pos:m.start()], 'szokoz': False, 'fo': None})
        ki.append({'kiir': m.group(0), 'szokoz': False, 'fo': fo})
        pos = m.end()
    if pos < len(szoveg):
        ki.append({'kiir': szoveg[pos:], 'szokoz': False, 'fo': None})
    return ki


def _lxx_valaszt(tokenek):
    """Egy vers LXX-tokenjei egyetlen szövegformából: a nem változat-nevű (pl. `daniel`) a `-theodotion`, `-vaticanus-b` és
    hasonló változat előtt; több egyenrangúnál az első."""
    formak = []
    for t in tokenek:
        if t[0] not in formak:
            formak.append(t[0])
    if not formak:
        return []
    alap = [f for f in formak if not re.search(r'-(theodotion|vaticanus-b|sinaiticus)$', f)]
    forma = (alap or formak)[0]
    return [t for t in tokenek if t[0] == forma]


def fejezet_versek(con, kozos, b, kk, fej, karoli_versek, karoli_szavak, szofaj_fn, strong_is):
    """A nem Károli 1908-as Biblia fejezetének versei. `karoli_versek`: [(ig, vers, szoveg)] (a Károli-fejezet), `karoli_szavak`:
    a `lekerdezesek.fejezet_szavak` (a modern Károli Strong-párjaihoz), `szofaj_fn`: strongok -> szófaj-térkép."""
    ny = kozos.nyelvtani
    ki = []
    if b.szamozas == 'forras':
        for vers, forras_vers, forras_kulcs, szoveg in q.forras_fejezet(con, b.tabla, kk, fej):
            ki.append({'vers': vers, 'ig': None, 'link': False, 'szavak': [], 'szoveg': szoveg, 'jel': '',
                       'nincs_karoli': forras_kulcs == 'nem'})
        return ki
    if b.kod == 'modern':
        szoveg, tok = q.modern_fejezet(con, kk, fej)
        parok_ig = {ig: {sz: parok for sz, _, parok in lista} for ig, lista in karoli_szavak.items()}
        strongok = {p[2] for d in parok_ig.values() for parok in d.values() for p in parok}
        szofaj = szofaj_fn(strongok)
        for ig, v, _ in karoli_versek:
            if ig not in szoveg:
                continue
            tl = tok.get(ig, [])
            igaz = q.szovegbe_igazit(szoveg[ig], [a for _, a in tl])
            ws = []
            for (sz, _), (kiir, szokoz) in zip(tl, igaz):
                fo = q.fo_szo(parok_ig.get(ig, {}).get(sz, []), ny, szofaj)
                ws.append({'kiir': kiir, 'szokoz': szokoz, 'fo': fo[0] if fo else None, 'biz': fo[1] if fo else None})
            ki.append({'vers': v, 'ig': ig, 'link': True, 'szavak': ws, 'szoveg': szoveg[ig], 'jel': ''})
        return ki
    if b.kod in ('tahot', 'tagnt'):
        tok = q.eredeti_fejezet(con, kk, fej, 'H' if b.kod == 'tahot' else 'G')
        for ig, v, _ in karoli_versek:
            if ig not in tok:
                continue
            if b.kod == 'tahot':
                ws = _tahot_szavak(tok[ig], ny)
            else:
                ws = [{'kiir': alak, 'szokoz': True, 'fo': _fo_strong(lanc, ny)} for _, alak, lanc in tok[ig]]
            ki.append({'vers': v, 'ig': ig, 'link': True, 'szavak': ws, 'szoveg': '', 'jel': ''})
        return ki
    if b.kod == 'lxx':
        tok = q.lxx_fejezet(con, kk, fej)
        for ig, v, _ in karoli_versek:
            tl = _lxx_valaszt(tok.get(ig, []))
            if not tl:
                continue
            lxx_ig = []
            for t in tl:
                if t[1] and t[1] not in lxx_ig:
                    lxx_ig.append(t[1])
            szam = [x.rsplit(' ', 1)[-1] for x in lxx_ig]
            jel = '' if szam == ['%d:%d' % (fej, v)] else 'LXX ' + ', '.join(szam)
            ws = [{'kiir': szo, 'szokoz': True, 'fo': (q.hnorm(st) if q.hnorm(st) not in ny else None) if st else None} for _, _, szo, st in tl]
            ki.append({'vers': v, 'ig': ig, 'link': True, 'szavak': ws, 'szoveg': '', 'jel': jel})
        return ki
    if b.kod == 'kjv':
        szoveg, cimke = q.kjv_fejezet(con, kk, fej, strong_is)
        for ig, v, _ in karoli_versek:
            if ig not in szoveg:
                continue
            reszek = szoveg[ig]
            sz = ' '.join(s for _, s in reszek)
            szam = [r[0].split('.', 1)[-1].replace('.', ':') for r in reszek]
            jel = '' if szam == ['%d:%d' % (fej, v)] else 'KJV ' + ', '.join(szam)
            ws = _kjv_szavak(sz, cimke.get(ig, []), ny) if strong_is else []
            ki.append({'vers': v, 'ig': ig, 'link': True, 'szavak': ws, 'szoveg': sz, 'jel': jel})
        return ki
    if b.kod == 'bsb':
        tok = q.bsb_fejezet(con, kk, fej)
        for ig, v, _ in karoli_versek:
            if ig not in tok:
                continue
            ws = [{'kiir': szo, 'szokoz': True, 'fo': (q.hnorm(st) if q.hnorm(st) not in ny else None) if st else None} for szo, st in tok[ig]]
            ki.append({'vers': v, 'ig': ig, 'link': True, 'szavak': ws, 'szoveg': '', 'jel': ''})
        return ki
    raise ValueError('ismeretlen Biblia: %s' % b.kod)
