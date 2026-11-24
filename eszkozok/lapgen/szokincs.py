"""lapgen.szokincs — a szókincs-kapu: a lapra kerülő kézi és sablonszöveg két hibája (F241.5b, D11 (1), D12, D15, D17).

Egy lista, egy hely: a lap minta-ellenőrzése (`olvasoi_kapu.MINTA_SZAKSZO`) is innen olvas. A kapu a forrásnál
mér (a tábla során, a generálás előtt), nem a kimeneten: a lap nem tisztít, a forrás javul.

- `SZAKSZO` — a tiltólista (D17 (1)): csak a magyarázatlan belső eljárásra utaló szavak; ezek a lap egyetlen
  szövegében sem állhatnak.
- `MASODIK_NEV` — a névazonosság (D17 (2)): egy fogalomra egy olvasói név a lapon, az, amelyet a lap bevezet. A
  kulcs a bevezetett név (a fölérendelt fogalomé a lap fejének felirata, `fej.tagabb`; a meghatározás szerkezetéé a
  meghatározás saját szava), az érték ugyanannak a fogalomnak a többi neve: ezek a forrásban nem állhatnak.
"""
import re

SZAKSZO = ('gerinc', 'token', 'proveniencia', 'kutatói hozzárendelés', 'Szövegigazolás nélkül', 'jelölt')
MASODIK_NEV = {
    'tágabb kör': ('fölérendelt fogalom', 'fölérendelt', 'felérendelt', 'tágabb fogalom', 'általánosabb fogalom',
                   'felsőbb fogalom'),
    'segítségül hívó szerkezet': ('invokáló szerkezet',),
}

_SZAKSZO_RX = re.compile(r'(?<!\w)(?:%s)' % '|'.join(re.escape(x) for x in SZAKSZO), re.I)
MASODIK_RX = re.compile(r'(?<!\w)(?:%s)' % '|'.join(
    re.escape(x) for x in sorted((n for nevek in MASODIK_NEV.values() for n in nevek), key=len, reverse=True)), re.I)
_TAGABB_NEV_RX = re.compile(r'^\*\*Az? ([^*]+)\*\*')


def talalatok(szoveg):
    """A szöveg szókincs-találatai: a tiltólista szavai és egy fogalom második nevei (a talált alakok, a szöveg
    sorrendjében); üres lista, ha a szöveg tiszta."""
    szoveg = szoveg or ''
    ki = [(m.start(), m.group(0)) for m in _SZAKSZO_RX.finditer(szoveg)]
    ki += [(m.start(), '%s (a lapon: %s)' % (m.group(0), bevezetett(m.group(0)))) for m in MASODIK_RX.finditer(szoveg)]
    return [t for _i, t in sorted(ki)]


def bevezetett(nev):
    return next(k for k, nevek in MASODIK_NEV.items() if nev.lower() in (n.lower() for n in nevek))


def tagabb_nev(fej_tagabb_mondat):
    """A fölérendelt fogalom olvasói neve a `fej.tagabb` sablonsor elejének félkövér címéből, névelő nélkül
    („tágabb kör”); None, ha a sor nem a megszokott alakú (a kapu ilyenkor hibát ad, nem találgat)."""
    m = _TAGABB_NEV_RX.match(fej_tagabb_mondat or '')
    return m.group(1).strip().lower() if m else None
