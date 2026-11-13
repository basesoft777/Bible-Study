"""lapgen.bemenet.elofordulas — a motívum előfordulás-sorai (B03) és a Károli-szöveg (B07).

A nyers mezők itt bomlanak típusos részekre: a `funkcio` címkére és magyarázatra, a `strong` Strong-számokra,
a `pardes_szint` szintekre, a `proveniencia` közös és egyedi részekre. A számítás már csak típusos értéket lát.
"""
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import Igazolas, Megbizhatosag
from lapgen.szoveg import Igehely, Strong

_OSZLOPOK = ('id', 'igehely', 'kapcsolodas', 'pardes_szint', 'funkcio', 'gerinc_elem', 'strong', 'lexikon_szotar',
             'lexikon_entry_id', 'jelentes_szam', 'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'proveniencia',
             'igazolas')
SAJAT_SZO_OSZLOP = 'sajat_szo'
_STRONG_RX = re.compile(r'^[HG]\d{4}[A-Za-z]?$')
_IKON_RX = re.compile(r'^[^\w"„(]+')
_TEMATIKUS_ELOTAG = 'tematikus:'
# A proveniencia-hármas alakja (`scope=… | forras=… | ts=…`, a lekérdezés további mezőivel), ahogy a lekérdező írja.
_ELV = r'\s\\?\|\s*'
_HARMAS_RX = re.compile(r'scope=[^|`\n]*?' + _ELV + r'forras=[^|`\n]*?(?:' + _ELV + r'(?!ts=)[a-z_]+=[^|`\n]*?)*'
                        + _ELV + r'ts=[0-9T:Z-]+(?:' + _ELV + r'csatorna=[a-z_]+)?')
_SCOPE_RX = re.compile(r'scope=([^|]*?)\s*\|')
_TS_RX = re.compile(r'ts=(\d{4}-\d{2}-\d{2})')


class ProvResz:
    """A proveniencia-mező egy darabja: közös hármas (`harmas` igaz) vagy a körülötte álló egyedi szöveg."""
    __slots__ = ('szoveg', 'harmas', 'kezi_szerkesztes', 'datum')

    def __init__(self, szoveg, harmas, kezi_szerkesztes=False, datum=None):
        self.szoveg, self.harmas, self.kezi_szerkesztes, self.datum = szoveg, harmas, kezi_szerkesztes, datum


class ElofordulasBe:
    """Az előfordulás-tábla egy sora, típusos mezőkkel."""
    __slots__ = ('igehely', 'kapcsolodas', 'pardes_szintek', 'funkcio_cimke', 'funkcio_magyarazat', 'gerinc_elem',
                 'tematikus', 'strongok', 'szotar', 'entry', 'jelentes_szam', 'karoli_szo', 'azonositas_modja',
                 'megbizhatosag', 'megbizhatosag_kulcs', 'proveniencia', 'prov_reszek', 'igazolas', 'igazolas_kulcs',
                 'sajat_szo')


def _strong_vagy_semmi(nyers):
    nyers = nyers.strip()
    return Strong(nyers) if _STRONG_RX.match(nyers) else None


def _felsorolas(osztaly, nyers, mezo, hely):
    if not nyers:
        return None
    try:
        return osztaly(nyers)
    except ValueError:
        raise BemenetHiba('B03: ismeretlen %s érték: %r (%s)' % (mezo, nyers, hely)) from None


def _prov_reszek(b, nyers):
    """A proveniencia-mező darabjai: a hármasok külön, hogy a közös hármas jelet kaphasson."""
    reszek, veg = [], 0
    for m in _HARMAS_RX.finditer(nyers):
        if m.start() > veg:
            reszek.append(ProvResz(b.belso('B03', 'proveniencia', nyers[veg:m.start()]), False))
        harmas = m.group(0).replace('\\|', '|')
        scope = _SCOPE_RX.search(harmas)
        ts = _TS_RX.search(harmas)
        reszek.append(ProvResz(b.belso('B03', 'proveniencia', harmas), True,
                               kezi_szerkesztes=bool(scope and scope.group(1).strip() == 'manual'),
                               datum=b.belso('B03', 'proveniencia', ts.group(1)) if ts else None))
        veg = m.end()
    if veg < len(nyers):
        reszek.append(ProvResz(b.belso('B03', 'proveniencia', nyers[veg:]), False))
    return tuple(reszek)


def b03_elofordulasok(b, motivum):
    """B03 — a motívum előfordulás-sorai kánoni sorrendben. Az opcionális `sajat_szo` oszlop a vers saját,
    nem lánc-szava (Strong-szám); ha az oszlop nincs a táblában, az érték hiányzik."""
    tabla = b._tabla('B03', oszlopok=_OSZLOPOK)
    idx = {o: tabla.oszlop(o) for o in _OSZLOPOK}
    sajat_i = tabla.oszlop(SAJAT_SZO_OSZLOP) if tabla.van(SAJAT_SZO_OSZLOP) else None
    konyvek = b63_konyvek(b)
    ki = []
    for sor in tabla.sorok:
        if sor[idx['id']] != motivum.kod:
            continue

        def mezo(nev):
            return sor[idx[nev]]

        e = ElofordulasBe()
        e.igehely = konyvek.igehely(mezo('igehely'))
        e.kapcsolodas = b.kezi('B03', 'kapcsolodas', mezo('kapcsolodas'))
        e.pardes_szintek = tuple(b.kulcs('B03', 'pardes_szint', sz.strip())
                                 for sz in mezo('pardes_szint').split('/') if sz.strip())
        funkcio = mezo('funkcio')
        cimke, elv, magyarazat = funkcio.partition(' — ')
        if funkcio and not elv:
            _eleje, elv2, utana = funkcio.partition(': ')
            magyarazat = utana if elv2 else funkcio
        e.funkcio_cimke = b.kezi('B03', 'funkcio', _IKON_RX.sub('', cimke))
        e.funkcio_magyarazat = b.kezi('B03', 'funkcio', _IKON_RX.sub('', magyarazat))
        e.gerinc_elem = b.kulcs('B03', 'gerinc_elem', mezo('gerinc_elem'))
        e.tematikus = mezo('gerinc_elem').startswith(_TEMATIKUS_ELOTAG)
        e.strongok = tuple(Strong(t) for t in (r.strip() for r in mezo('strong').split('+'))
                           if t and _STRONG_RX.match(t))
        e.szotar = b.kulcs('B03', 'lexikon_szotar', mezo('lexikon_szotar'))
        e.entry = _strong_vagy_semmi(mezo('lexikon_entry_id'))
        e.jelentes_szam = b.kulcs('B03', 'jelentes_szam', mezo('jelentes_szam'))
        e.karoli_szo = b.forrasszoveg('B03', 'karoli_szo', mezo('karoli_szo'), e.igehely)
        e.azonositas_modja = b.kulcs('B03', 'azonositas_modja', mezo('azonositas_modja'))
        e.megbizhatosag = _felsorolas(Megbizhatosag, mezo('megbizhatosag'), 'megbizhatosag', mezo('igehely'))
        e.megbizhatosag_kulcs = b.kulcs('B03', 'megbizhatosag', mezo('megbizhatosag'))
        e.proveniencia = b.belso('B03', 'proveniencia', mezo('proveniencia').strip())
        e.prov_reszek = _prov_reszek(b, mezo('proveniencia').strip())
        e.igazolas = _felsorolas(Igazolas, mezo('igazolas').strip(), 'igazolas', mezo('igehely'))
        e.igazolas_kulcs = b.kulcs('B03', 'igazolas', mezo('igazolas').strip())
        e.sajat_szo = _strong_vagy_semmi(sor[sajat_i]) if sajat_i is not None else None
        ki.append(e)
    ki.sort(key=lambda x: konyvek.rendezo_kulcs(x.igehely))
    return tuple(ki)


# --- B07: a Károli-szöveg ---------------------------------------------------------------------------------------

_KERESZT_RX = re.compile(r'^(.+?)\s+(\d+):(\d+)-(\d+):(\d+)$')
_SAV_RX = re.compile(r'^(.+?)\s+(\d+):(\d+)-(\d+)$')
_VERS_RX = re.compile(r'^(.+) (\d+):(\d+)$')


class Karoli:
    """A Károli-fordítás versei igehely szerint, és a tartomány verseinek feloldása."""

    def __init__(self, b, szovegek, konyvenkent):
        self._b, self._szovegek, self._konyvenkent = b, szovegek, konyvenkent

    def van(self, vers):
        return vers.kod in self._szovegek

    def szoveg(self, vers):
        """A vers szövege idézhető forrásszövegként; None, ha a vers nincs a Károliban."""
        nyers = self._szovegek.get(vers.kod)
        if nyers is None:
            return None
        return self._b.forrasszoveg('B07', 'szoveg', nyers, vers)

    def versek(self, igehely):
        """Egy igehely versei: maga az igehely, vagy a tartomány minden Károli-verse (fejezet, vers szerint)."""
        kod = igehely.kod
        if '-' not in kod:
            return (igehely,)
        m = _KERESZT_RX.match(kod)
        if m:
            konyv, c1, v1, c2, v2 = m.group(1).strip(), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
        else:
            m = _SAV_RX.match(kod)
            if not m:
                return (igehely,)
            konyv, c1, v1, v2 = m.group(1).strip(), int(m.group(2)), int(m.group(3)), int(m.group(4))
            c2 = c1
        talalat = [(c, v, kulcs) for c, v, kulcs in self._konyvenkent.get(konyv, ())
                   if (c1, v1) <= (c, v) <= (c2, v2)]
        if not talalat:
            return (igehely,)
        return tuple(Igehely(kulcs) for _c, _v, kulcs in sorted(talalat))


def b07_karoli(b):
    """B07 — a Károli-fordítás (1908) verseinek szövege."""
    tabla = b._tabla('B07', oszlopok=('Igehely', 'Károli-szöveg (teljes vers)'))
    i, sz = tabla.oszlop('Igehely'), tabla.oszlop('Károli-szöveg (teljes vers)')
    szovegek, konyvenkent = {}, {}
    for sor in tabla.sorok:
        szovegek[sor[i]] = sor[sz]
        m = _VERS_RX.match(sor[i])
        if m:
            konyvenkent.setdefault(m.group(1), []).append((int(m.group(2)), int(m.group(3)), sor[i]))
    return Karoli(b, szovegek, konyvenkent)
