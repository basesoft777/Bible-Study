"""lapgen.bemenet.szakirodalom — a vitatott pontok lektorált szakirodalma (B75, `adat/vitatott_forrasok.tsv`).

Csak az ellenőrzött sor számít (üres `ellenorzes`: a lapon nem áll, a régi `vitatott_forrasok` szabálya). Az
összefoglaló kézi próza (saját szavas összefoglalás, idézet nincs). A szerző a lap mondatában a vezetéknevével áll: a
réteg ezt a mező szerkezetéből bontja (az első szerző neve, annak utolsó tagja; a régi `szakirodalom_beszur`), a
szöveget nem írja át.
"""
import datetime

from lapgen.bemenet.jegyzek import BemenetHiba

_OSZLOPOK = ('motivum', 'pont', 'szerzo', 'ev', 'osszefoglalo', 'lekerdezve', 'ellenorzes')
_SZERZO_ELVALASZTO = ','


class VitatottForras:
    """Egy vitatott pont szakirodalom-sora: a pont címe (kulcs), a szerző vezetékneve (kézi; None: hiány-sor), az év,
    az összefoglaló (kézi) és a lekérdezés dátuma."""
    __slots__ = ('pont', 'szerzo', 'ev', 'osszefoglalo', 'lekerdezve')

    def __init__(self, pont, szerzo, ev, osszefoglalo, lekerdezve):
        self.pont, self.szerzo, self.ev, self.osszefoglalo, self.lekerdezve = pont, szerzo, ev, osszefoglalo, lekerdezve


def b75_vitatott_forrasok(b, motivum):
    """B75 — a motívum ellenőrzött szakirodalom-sorai, a tábla rendjében."""
    tabla = b._tabla('B75', oszlopok=_OSZLOPOK)
    ki = []
    for r in tabla.szotarak():
        if r['motivum'] != motivum.kod or not r['ellenorzes'].strip():
            continue
        try:
            lekerdezve = datetime.date.fromisoformat(r['lekerdezve'].strip())
            ev = int(r['ev']) if r['ev'].strip() else None
        except ValueError as hiba:
            raise BemenetHiba('B75: hibás dátum vagy év (%s, %s): %s' % (motivum.kod, r['pont'], hiba))
        szerzo = r['szerzo'].strip()
        if szerzo and ev is None:
            raise BemenetHiba('B75: szerzővel álló sor év nélkül (%s, %s)' % (motivum.kod, r['pont']))
        vezeteknev = szerzo.split(_SZERZO_ELVALASZTO)[0].split()[-1] if szerzo else None
        ki.append(VitatottForras(
            pont=b.kulcs('B75', 'pont', r['pont'].strip()),
            szerzo=b.kezi('B75', 'szerzo', vezeteknev) if vezeteknev else None,
            ev=ev, osszefoglalo=b.kezi('B75', 'osszefoglalo', r['osszefoglalo'].strip()), lekerdezve=lekerdezve))
    return tuple(ki)
