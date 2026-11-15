"""lapgen.bemenet.lxx — az „5. LXX-fordítói döntések” szakasz és a 4.6 (LXX-híd) bemenetei (S4).

- B35: a Septuaginta szövege versenként, a Károli-könyv elsődleges szövegváltozatának fájljából (a régi
  `karoli_to_primary_slug`, `lxx_os_karoli_index`);
- B37: az LXX-fordítói döntések teljes sorai (a megjelenő bizonyosság és típus szűrőjével, és a szűretlen tábla
  saját döntés-párjai: a régi `lxx_dontesek_index`, `sajat_dontes`);
- B38: a 4.11 visszhang-blokk ellenőrzött LXX-társításai (a régi `vh_lxx_index`).

A szövegek idézhető forrásszövegként jönnek; az igehely-számok egészek.
"""
import os
import re
import unicodedata

import lxx_os_import

from lapgen import konfig
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Strong

_LXX_VERS_RX = re.compile(r'(\d+):(\d+)$')
_DONTES_OSZLOPOK = ('igehely', 'lxx_igehely', 'heber_strong', 'gorog_lemma', 'gorog_strong', 'tipus', 'bizonyossag')
_VH_OSZLOPOK = ('motivum', 'strong', 'igehely', 'forras', 'lemma', 'kiejtes', 'ellenorzes')
_GOROG_STRONG_RX = re.compile(r'^G\d{4}$')
_HEBER_STRONG_RX = re.compile(r'^H\d{4}[a-z]?$')
TIPUS_MINUSZ = 'lxx_minusz'


def ekezet_nelkul(szoveg):
    """Összevetési kulcs: ékezet (kombináló jel) nélkül, kisbetűvel (a régi `_nfc_ekezet_nelkul`)."""
    return ''.join(c for c in unicodedata.normalize('NFD', szoveg or '') if not unicodedata.combining(c)).lower()


def lxx_vers(nyers):
    """A nyers LXX-igehely („Psalms (LXX) 13:1”) fejezete és verse egészként; None, ha nem ilyen alakú."""
    m = _LXX_VERS_RX.search(nyers or '')
    return (int(m.group(1)), int(m.group(2))) if m else None


class LxxSzo:
    """A Septuaginta egy szava a versben: az alak és a lemma (idézet), a Strong-szám (None: a forrás nem adja),
    a vers LXX-számozása (fejezet, vers) vagy None."""
    __slots__ = ('alak', 'lemma', 'strong', 'lxx_hely')

    def __init__(self, alak, lemma, strong, lxx_hely):
        self.alak, self.lemma, self.strong, self.lxx_hely = alak, lemma, strong, lxx_hely


def _vers_index(fajlok):
    """{(fájlnév a kiterjesztés nélkül, Károli-vers): ((LXX-igehely, alak, lemma, Strong-szám nyersen), …)}."""
    ki = {}
    for utvonal, fejlec, sorok in fajlok:
        if 'igehely_lxx' not in fejlec:
            continue   # a könyvtár segédtáblája
        try:
            lxx, karoli, alak, lemma, strong = (fejlec.index(o) for o in
                                                ('igehely_lxx', 'igehely_karoli', 'szoalak', 'lemma', 'strong'))
        except ValueError:
            raise BemenetHiba('B35 (%s): hiányzó oszlop' % utvonal) from None
        slug = os.path.splitext(os.path.basename(utvonal))[0]
        for sor in sorok:
            if len(sor) > strong and sor[karoli]:
                ki.setdefault((slug, sor[karoli]), []).append((sor[lxx], sor[alak], sor[lemma], sor[strong]))
    return {k: tuple(v) for k, v in ki.items()}


class Septuaginta:
    """A Septuaginta versei Károli-kulcson, a Károli-könyv elsődleges szövegváltozatából (F42, DT-F42f)."""

    def __init__(self, b, index):
        self._b, self._index = b, index

    @staticmethod
    def konyv_fajl(konyv):
        """A Károli-könyv elsődleges LXX-fájljának neve (a `lxx_os_import` térképe); None: nincs görög könyv."""
        return lxx_os_import.elsodleges_slug(konyv)

    def szavak(self, vers):
        """A vers szavai a Septuagintában (a fájl rendjében); üres, ha a versnek nincs sora (a versszámozás eltér).
        Ha a könyvnek nincs görög fájlja: None."""
        slug = self.konyv_fajl(vers.konyv)
        if slug is None:
            return None
        ki = []
        for lxx, alak, lemma, strong in self._index.get((slug, vers.kod), ()):
            st = Strong('G%04d' % int(strong)) if strong.strip().isdigit() else None
            ki.append(LxxSzo(self._b.forrasszoveg('B35', 'szoalak', alak, vers),
                             self._b.forrasszoveg('B35', 'lemma', lemma, vers), st, lxx_vers(lxx)))
        return tuple(ki)


def septuaginta(b):
    """B35 — a Septuaginta szövege versenként (az 5. szakasz összevetéséhez)."""
    def betolt():
        utvonalak = b._utvonalak('B35')
        if not utvonalak:
            raise BemenetHiba('B35: a Septuaginta szövegkiadásának egyetlen fájlja sincs meg')
        return Septuaginta(b, b._nagy_index('B35', utvonalak, _vers_index))
    return b.egyszer('B35:versek', betolt)


class Dontes:
    """Az LXX-fordítói döntések egy (megjelenő) sora: a héber szó Strong-száma (None: üres), a görög lemma
    (idézet vagy None), a görög Strong-szám (None: üres), a döntés LXX-igehelye (fejezet, vers) vagy None, LXX-minusz-e."""
    __slots__ = ('heber', 'lemma', 'gorog', 'lxx_hely', 'minusz')

    def __init__(self, heber, lemma, gorog, lxx_hely, minusz):
        self.heber, self.lemma, self.gorog, self.lxx_hely, self.minusz = heber, lemma, gorog, lxx_hely, minusz


class LxxDontesSorok:
    def __init__(self, megjeleno, sajat):
        self._megjeleno, self._sajat = megjeleno, sajat

    def vershez(self, vers):
        """A vers megjelenő döntései a tábla rendjében."""
        return self._megjeleno.get(vers.kod, ())

    def sajat(self, vers, heber):
        """Van-e a (vers, héber szó) párnak sora a szűretlen táblában (a régi `sajat_dontes`)."""
        return (vers.kod, heber.kod) in self._sajat


def dontes_sorok(b):
    """B37 — az LXX-fordítói döntések teljes sorai (a megjelenő szűrővel), és a szűretlen tábla (vers, héber szó)
    párjai."""
    def betolt():
        tabla = b._tabla('B37', oszlopok=_DONTES_OSZLOPOK)
        megjeleno, sajat = {}, set()
        for r in tabla.szotarak():
            heber = r['heber_strong'].strip()
            sajat.add((r['igehely'], heber))
            if r['bizonyossag'].strip() not in konfig.LXX_DONTES_BIZONYOSSAG \
                    or r['tipus'].strip() not in konfig.LXX_DONTES_TIPUS:
                continue
            gorog = r['gorog_strong'].strip()
            lemma = r['gorog_lemma'].strip()
            megjeleno.setdefault(r['igehely'], []).append(Dontes(
                Strong(heber) if _HEBER_STRONG_RX.match(heber) else None,
                b.forrasszoveg('B37', 'gorog_lemma', lemma, r['igehely']) if lemma else None,
                Strong(gorog) if _GOROG_STRONG_RX.match(gorog) else None,
                lxx_vers(r['lxx_igehely']) if r['lxx_igehely'].strip() else None,
                r['tipus'].strip() == TIPUS_MINUSZ))
        return LxxDontesSorok({k: tuple(v) for k, v in megjeleno.items()}, frozenset(sajat))
    return b.egyszer('B37:sorok', betolt)


class Tarsitas:
    """A 4.11 egy ellenőrzött LXX-társítása: a görög lemma (idézet; több lemma „ · ”-tal) és a kiejtése (idézet)."""
    __slots__ = ('lemma', 'kiejtes')

    def __init__(self, lemma, kiejtes):
        self.lemma, self.kiejtes = lemma, kiejtes

    def lemmak(self):
        """A lemma részei („βοάω · ἐπικαλέω”), összevetési kulcsként."""
        return [ekezet_nelkul(x.strip()) for x in self.lemma.ertek.split('·') if x.strip()]


def lxx_tarsitasok(b, motivum):
    """B38 — a motívum ellenőrzött LXX-társításai: {(Károli-vers kódja, héber Strong-kód): Tarsitas}; csak a
    lemmás, ellenőrzött sor (a 4.11 ugyanezeket írja)."""
    def betolt():
        ki = {}
        for r in b._tabla('B38', oszlopok=_VH_OSZLOPOK).szotarak():
            if r['motivum'] != motivum.kod or r['forras'] != 'lxx' or not r['lemma'].strip() \
                    or not r['ellenorzes'].strip():
                continue
            hely = r['igehely']
            ki[(hely, r['strong'])] = Tarsitas(b.forrasszoveg('B38', 'lemma', r['lemma'], hely),
                                               b.forrasszoveg('B38', 'kiejtes', r['kiejtes'], hely))
        return ki
    return b.egyszer('B38:lxx:%s' % motivum.kod, betolt)
